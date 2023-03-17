import pytz
import logging
import traceback

from time import sleep, time
from threading import Thread
from datetime import  datetime

from leituras import *
from ocorrencias import *
from dicionarios.reg import *
from dicionarios.const import *
from clients import ClpClients
from unidade_geracao import UnidadeDeGeracao
from conector import ConectorCampo, ConectorBancoDados

logger = logging.getLogger("__main__")

class Usina:
    def __init__(
            self,
            sd=None,
            cfg=None,
            clp: ClpClients=None,
            oco: OcorrenciasUg=None,
            con: ConectorCampo=None,
            db: ConectorBancoDados=None,
            ugs: list([UnidadeDeGeracao])=None,
        ):

        # VERIFICAÇÃO DE ARGUMENTOS
        if not sd or not cfg:
            logger.warning("[USN] Houve um erro ao carregar arquivos de configuração (\"cfg.json\" | \"shared_dict\").")
            raise ValueError
        else:
            self.dict = sd
            self.cfg = cfg

        if not db or not con or not clp:
            logger.warning("[USN] Não foi possível carregar classes de conexão com clps | campo | banco de dados.")
            raise ConnectionError
        else:
            self.db = db
            self.con = con
            self.clp = clp
            self.clp_moa = clp.clp_dict[0]
            self.clp_usn = clp.clp_dict[1]
            self.clp_tda = clp.clp_dict[2]

        if not oco:
            logger.warning("[USN] Não foi possível carregar classe de ocorrências")
            raise ReferenceError
        else:
            self.oco = oco

        if not ugs:
            logger.warning("[USN] Não foi possível carregar instâncias das unidades de geração.")
            raise ValueError
        else:
            self.ugs = ugs
            self.ug1 = ugs[0]
            self.ug2 = ugs[1]

        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS
        # Numéricas
        self._tentativas_normalizar: int = 0
        self._potencia_alvo_anterior: int = -1

        # Booleanas
        self._modo_autonomo: bool = False

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS
        # Numéricas
        self.estado_moa: int = 0

        self.pot_disp: int = 0
        self.ug_operando: int = 0

        self.status_tensao: int = 0

        self.modo_de_escolha_das_ugs: int = 0

        self.controle_p: float = 0
        self.controle_i: float = 0
        self.controle_d: float = 0

        self.erro_nv: float = 0
        self.erro_nv_anterior: float = 0
        self.nv_montante_recente: float = 0

        # Booleanas
        self.borda_emerg: bool = False

        self.timer_tensao: bool = False

        self.tentar_normalizar: bool = True
        self.normalizar_forcado: bool = False
        self.dict["GLB"]["avisado_eletrica"]: bool = False

        self.db_emergencia: bool = False
        self.clp_emergencia: bool = False

        self.aguardando_reservatorio: bool = False

        # Datetime
        self.ts_last_ping_tda: datetime = self.get_time()
        self.ultima_tentativa_norm: datetime = self.get_time()

        # EXECUÇÃO FINAL INIT
        self.ler_valores()
        self.controle_inicial()
        self.normalizar_usina()
        self.escrever_valores()

    @property
    def nv_montante(self) -> float:
        return LeituraModbus(
            "Nível Montante",
            self.clp_tda,
            TDA["REG_TDA_NivelMaisCasasAntes"],
            1 / 10000,
            819.2,
            op=4,
        ).valor

    @property
    def tensao_rs(self) -> float:
        return LeituraModbus(
            "Tensão R",
            self.clp_usn,
            SA["REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_AB"],
            1000,
            op=4,
        ).valor

    @property
    def tensao_st(self) -> float:
        return LeituraModbus(
            "Tensão S",
            self.clp_usn,
            SA["REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_BC"],
            1000,
            op=4,
        ).valor

    @property
    def tensao_tr(self) -> float:
        return LeituraModbus(
            "Tensão T",
            self.clp_usn,
            SA["REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_CA"],
            1000,
            op=4,
        ).valor

    @property
    def potencia_ativa_kW(self) -> int:
        return LeituraModbus(
            "Potência MP/MR",
            self.clp_usn,
            SA["REG_SA_RetornosAnalogicos_MWR_PM_810_Potencia_Ativa"],
            1,
            op=4,
        ).valor

    @property
    def modo_autonomo(self) -> bool:
        return self._modo_autonomo

    @modo_autonomo.setter
    def modo_autonomo(self, var: bool) -> None:
        self._modo_autonomo = var
        self.db.update_modo_moa(self._modo_autonomo)

    @property
    def tentativas_normalizar(self) -> int:
        return self._tentativas_normalizar

    @tentativas_normalizar.setter
    def tentativas_normalizar(self, var: int) -> None:
        self._tentativas_normalizar = var

    @property
    def pot_alvo_anterior(self) -> float:
        return self._potencia_alvo_anterior

    @pot_alvo_anterior.setter
    def pot_alvo_anterior(self, var):
        self._potencia_alvo_anterior = var

    def get_time(self) -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def ajustar_ie_padrao(self) -> int:
        return [sum(ug.leitura_potencia) for ug in self.ugs] / self.cfg["pot_maxima_alvo"]

    def acionar_emergencia(self) -> None:
        self.clp_emergencia = True
        self.con.acionar_emergencia()

    def heartbeat(self) -> None:
        try:
            agora = self.get_time()
            ano = int(agora.year)
            mes = int(agora.month)
            dia = int(agora.day)
            hor = int(agora.hour)
            mnt = int(agora.minute)
            seg = int(agora.second)
            mil = int(agora.microsecond / 1000)
            self.clp_moa.write_multiple_registers(0, [ano, mes, dia, hor, mnt, seg, mil])
            self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_STATUS"], [self.estado_moa])
            self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_MODE"], [self.modo_autonomo])

            if self.modo_autonomo:
                self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_EMERG"], [self.clp_emergencia])
                self.clp_moa.write_multiple_registers(MOA["REG_MOA_OUT_SETPOINT"], [int(sum(ug.setpoint)) for ug in self.ugs])
                self.clp_moa.write_multiple_registers(MOA["REG_MOA_OUT_TARGET_LEVEL"], [int((self.cfg["nv_alvo"] - 820.9) * 1000)])

                if self.dict["GLB"]["avisado_eletrica"] and not self.borda_emerg:
                    self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_BLOCK_UG1"], [1],)
                    self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_BLOCK_UG2"], [1],)
                    self.borda_emerg = True

                elif not self.dict["GLB"]["avisado_eletrica"] and self.borda_emerg:
                    self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_BLOCK_UG1"], [0],)
                    self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_BLOCK_UG2"], [0],)
                    self.borda_emerg = False

                if self.clp_moa.read_coils(MOA["REG_MOA_IN_HABILITA_AUTO"])[0] == 1:
                    self.clp_moa.write_single_coil(MOA["REG_MOA_IN_HABILITA_AUTO"], [1])
                    self.clp_moa.write_single_coil(MOA["REG_MOA_IN_DESABILITA_AUTO"], [0])
                    self.modo_autonomo = 1
                elif self.clp_moa.read_coils(MOA["REG_MOA_IN_DESABILITA_AUTO"])[0] == 1:
                    self.clp_moa.write_single_coil(MOA["REG_MOA_IN_HABILITA_AUTO"], [0])
                    self.clp_moa.write_single_coil(MOA["REG_MOA_IN_DESABILITA_AUTO"], [1])
                    self.modo_autonomo = 0

                for ug in self.ugs:
                    if self.clp_moa.read_coils(MOA[f"REG_MOA_OUT_BLOCK_UG{ug.id}"])[0] == 1:
                        self.clp_moa.write_single_coil(MOA[f"REG_MOA_OUT_BLOCK_UG{ug.id}"], [1])
                    elif self.clp_moa.read_coils(MOA[f"REG_MOA_OUT_BLOCK_UG{ug.id}"])[0] == 0:
                        self.clp_moa.write_single_coil(MOA[f"REG_MOA_OUT_BLOCK_UG{ug.id}"], [0])

            elif not self.modo_autonomo:
                self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_EMERG"], [0])
                self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_SETPOINT"], [0])
                self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_TARGET_LEVEL"], [0])
                [self.clp_moa.write_single_coil(MOA[f"REG_MOA_OUT_BLOCK_UG{ug.id}"], [0]) for ug in self.ugs]

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def ler_valores(self) -> None:
        self.clp.ping_clps()
        try:
            if self.clp_moa.read_coils(MOA["REG_MOA_IN_EMERG"])[0] == 1 and not self.dict["GLB"]["avisado_eletrica"]:
                self.dict["GLB"]["avisado_eletrica"] = True
                self.oco.verificar_condicionadores()

            elif self.clp_moa.read_coils(MOA["REG_MOA_IN_EMERG"])[0] == 0 and self.dict["GLB"]["avisado_eletrica"]:
                self.dict["GLB"]["avisado_eletrica"] = True

            if self.clp_moa.read_coils(MOA["REG_MOA_IN_EMERG_UG1"])[0] == 1 or self.clp_moa.read_coils(MOA["REG_MOA_IN_EMERG_UG2"])[0] == 1:
                self.oco.verificar_condicionadores()

            if self.clp_moa.read_coils(MOA["REG_MOA_IN_HABILITA_AUTO"])[0] == 1:
                self.clp_moa.write_single_coil(MOA["REG_MOA_IN_HABILITA_AUTO"], [1])
                self.clp_moa.write_single_coil(MOA["REG_MOA_IN_DESABILITA_AUTO"], [0])
                self.modo_autonomo = True

            if self.clp_moa.read_coils(MOA["REG_MOA_IN_DESABILITA_AUTO"])[0] == 1:
                self.clp_moa.write_single_coil(MOA["REG_MOA_IN_HABILITA_AUTO"], [0])
                self.clp_moa.write_single_coil(MOA["REG_MOA_IN_DESABILITA_AUTO"], [1])
                self.modo_autonomo = False

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao tentar ler valores modbus no CLP MOA. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

        self.heartbeat()
        self.atualizar_montante_recente()

        parametros = self.db.get_parametros_usina()
        self.atualizar_cfg(parametros)
        self.atualizar_parametros_db(parametros)

        for ug in self.ugs: 
            self.oco.atualizar_limites_condicionadores(parametros, ug)

    def escrever_valores(self) -> None:
        try:
            self.db.update_valores_usina(
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),  # timestamp
                1 if self.aguardando_reservatorio else 0,  # aguardando_reservatorio
                True,  # DEPRECATED clp_online
                self.nv_montante if not self.dict["GLB"]["tda_offline"] else 0, # nv_montante
                1 if self.ug1.disponivel else 0,  # ug1_disp
                self.ug1.leitura_potencia.valor,  # ug1_pot
                self.ug1.setpoint,  # ug1_setpot
                self.ug1.etapa_atual,  # ug1_sinc
                self.ug1.leitura_horimetro.valor,  # ug1_tempo
                1 if self.ug2.disponivel else 0,  # ug2_disp
                self.ug2.leitura_potencia.valor,  # ug2_pot
                self.ug2.setpoint,  # ug2_setpot
                self.ug2.etapa_atual,  # ug2_sinc
                self.ug2.leitura_horimetro.valor,  # ug2_tempo
            )

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao inserir os valores no banco. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

        try:
            self.db.insert_debug(
                self.get_time().timestamp(),
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
                self.controle_p if not self.dict["GLB"]["tda_offline"] else 0,
                self.controle_i if not self.dict["GLB"]["tda_offline"] else 0,
                self.controle_d if not self.dict["GLB"]["tda_offline"] else 0,
                self.controle_ie if not self.dict["GLB"]["tda_offline"] else 0,
                self.ug1.setpoint,
                self.ug1.leitura_potencia.valor,
                self.ug2.setpoint,
                self.ug2.leitura_potencia.valor,
                self.nv_montante_recente if not self.dict["GLB"]["tda_offline"] else 0,
                self.erro_nv if not self.dict["GLB"]["tda_offline"] else [sum(ug.erro_press_cx) for ug in self.ugs] / 2,
                1 if self.modo_autonomo else 0,
                self.cfg["cx_kp"],
                self.cfg["cx_ki"],
                self.cfg["cx_kie"],
                0 if not self.dict["GLB"]["tda_offline"] else [sum(ug.cx_controle_ie) for ug in self.ugs] / 2,
            )

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao inserir dados DEBUG do controle de potência normal no banco. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def atualizar_montante_recente(self) -> None:
        if not self.dict["GLB"]["tda_offline"]:
            self.nv_montante_recente = self.nv_montante
            self.erro_nv_anterior = self.erro_nv
            self.erro_nv = self.nv_montante_recente - self.cfg["nv_alvo"]

    def atualizar_parametros_db(self, parametros) -> None:
        try:
            self.db_emergencia = True if int(parametros["emergencia_acionada"]) == 1 else False
            logger.debug("[USN] Emergência acionada.")

            self.modo_autonomo = True if int(parametros["modo_autonomo"]) == 1 else False
            logger.debug(f"[USN] Modo autonomo que o banco respondeu: {int(parametros['modo_autonomo'])}")

            if not self.modo_de_escolha_das_ugs == int(parametros["modo_de_escolha_das_ugs"]):
                self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
                logger.info(f"[USN] O modo de prioridade das ugs foi alterado (#{self.modo_de_escolha_das_ugs}).")

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao ler e atualizar os parâmetros do Banco de Dados. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def atualizar_cfg(self, parametros) -> None:
        try:
            self.cfg["TDA_slave_ip"] = parametros["clp_tda_ip"]
            self.cfg["kp"] = float(parametros["kp"])
            self.cfg["ki"] = float(parametros["ki"])
            self.cfg["kd"] = float(parametros["kd"])
            self.cfg["kie"] = float(parametros["kie"])
            self.cfg["cx_kp"] = float(parametros["cx_kp"])
            self.cfg["cx_ki"] = float(parametros["cx_ki"])
            self.cfg["cx_kie"] = float(parametros["cx_kie"])
            self.cfg["press_cx_alvo"] = float(parametros["press_cx_alvo"])
            self.cfg["nv_alvo"] = float(parametros["nv_alvo"])
            self.cfg["nv_minimo"] = float(parametros["nv_minimo"])
            self.cfg["pot_maxima_alvo"] = float(parametros["pot_nominal"])
            self.cfg["pot_maxima_ug"] = float(parametros["pot_nominal_ug"])
            self.cfg["pot_maxima_usina"] = float(parametros["pot_nominal_ug"]) * 2

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao atualizar o arquivo de configuração \"cfg.json\". Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def normalizar_usina(self) -> bool:
        logger.debug("[USN] Normalizando...")
        logger.debug(f"[USN] Última tentativa: {self.ultima_tentativa_norm}. Tensão na linha: RS->{self.tensao_rs:2.1f}kV / ST->{self.tensao_st:2.1f}kV / TR->{self.tensao_tr:2.1f}kV")

        if not self.verificar_tensao():
            return False

        elif (self.tentar_normalizar and (self.get_time() - self.ultima_tentativa_norm).seconds >= 60 * self.tentativas_normalizar) or self.normalizar_forcado:
            self.ultima_tentativa_norm = self.get_time()
            self.tentativas_normalizar += 1
            self.db_emergencia = False
            self.clp_emergencia = False
            self.con.normalizar_emergencia()
            self.db.update_remove_emergencia()
            return True

        else:
            logger.debug("[USN] A normalização foi executada menos de 1 minuto atrás.")

    def verificar_tensao(self) -> bool:
        try:
            if (TENSAO_LINHA_BAIXA < self.tensao_rs < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < self.tensao_st < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < self.tensao_tr < TENSAO_LINHA_ALTA):
                return True
            else:
                logger.warning("[USN] Tensão da linha fora do limite.")
                return False

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao realizar a verificação da tensão na linha. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def aguardar_tensao(self) -> bool:
        if self.status_tensao == 0:
            self.status_tensao = 1
            logger.debug("[USN] Iniciando o timer para a normalização da tensão na linha.")
            Thread(target=lambda: self.timeout_tensao(600)).start()

        elif self.status_tensao == 2:
            logger.info("[USN] Tensão na linha reestabelecida.")
            self.status_tensao = 0
            return True

        elif self.status_tensao == 3:
            logger.critical("[USN] Não foi possível reestabelecer a tensão na linha. Acionando emergência")
            self.status_tensao = 0
            return False

        else:
            logger.debug("[USN] A tensão na linha ainda está fora.")

    def timeout_tensao(self, delay) -> None:
        while time() <= time() + delay:
            if self.verificar_tensao():
                self.status_tensao = 2
                return
            sleep(time() - (time() - 15))
        self.status_tensao = 3

    def ajuste_potencia(self, pot_alvo) -> float:
        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs: ug.setpoint = 0
            return 0

        logger.debug(f"[USN] Potência no medidor = {self.potencia_ativa_kW:0.3f}")
        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])
        pot_medidor = max(pot_aux, min(self.potencia_ativa_kW, self.cfg["pot_maxima_usina"]))

        try:
            if pot_medidor > self.cfg["pot_maxima_alvo"]:
                pot_alvo = self.pot_alvo_anterior * (1 - ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))
        except TypeError as te:
            logger.exception(f"[USN] A comunicação com os MFs falharam. Exception: \"{repr(te)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

        self.pot_alvo_anterior = pot_alvo

        logger.debug(f"[USN] Pot alvo pós ajuste: {pot_alvo:0.3f}")
        self.distribuir_potencia(pot_alvo)
        return pot_alvo

    def distribuir_potencia(self, pot_alvo) -> None:
        ugs = self.controle_ugs_disponiveis()
        logger.debug(f"[USN] UG{[ug.id for ug in self.ugs]}")

        self.pot_disp = [sum(ug.setpoint_maximo) for ug in self.ugs if not ug.manual]
        ajuste_manual = min(max(0, [sum(ug.leitura_potencia) for ug in self.ugs if ug.manual]))

        if ugs is None or not len(ugs):
            return

        logger.debug(f"[USN] Distribuindo: {pot_alvo - ajuste_manual:0.3f}")
        sp = (pot_alvo - ajuste_manual) / self.cfg["pot_maxima_usina"]

        self.__split1 = True if sp > (0) else self.__split1
        self.__split2 = (True if sp > (0.5 + self.cfg["margem_pot_critica"]) else self.__split2)

        self.__split2 = False if sp < (0.5) else self.__split2
        self.__split1 = False if sp < (self.cfg["pot_minima"] / self.cfg["pot_maxima_usina"]) else self.__split1

        logger.debug(f"[USN] SP<-{sp}")
        if len(ugs) == 2:
            if self.__split2:
                logger.debug("[USN] Split 2")
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = sp * ugs[1].setpoint_maximo

            elif self.__split1:
                logger.debug("[USN] Split 1")
                sp = sp * 2 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = 0

        elif len(ugs) == 1:
            if self.__split1 or self.__split2:
                logger.debug("[USN] Split 1B")
                sp = sp * 2 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo

        else:
            for ug in ugs: 
                ug.setpoint = 0

    def controle_inicial(self) -> None:
        self.ug_operando += [1 for ug in self.ugs if ug.etapa_atual == UG_SINCRONIZADA]

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False

        self.controle_ie = [sum(ug.leitura_potencia.valor) / self.cfg["pot_maxima_alvo"] if self.cfg["saida_ie_inicial"] == "auto" else self.cfg["saida_ie_inicial"] for ug in self.ugs]

    def controle_potencia(self) -> None:
        logger.debug("-------------------------------------------------------------------------")
        logger.debug(f"[USN] NÍVEL -> Leitura: {self.nv_montante_recente:0.3f}; Alvo: {self.cfg['nv_alvo']:0.3f}")

        self.controle_p = self.cfg["kp"] * self.erro_nv
        self.controle_i = max(min((self.cfg["ki"] * self.erro_nv) + self.controle_i, 0.8), 0)
        self.controle_d = self.cfg["kd"] * (self.erro_nv - self.erro_nv_anterior)
        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))
        logger.debug(f"[USN] PID -> {saida_pid:0.3f} P:{self.controle_p:0.3f} + I:{self.controle_i:0.3f} + D:{self.controle_d:0.3f}; ERRO={self.erro_nv}")

        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)
        logger.debug(f"[USN] IE: {self.controle_ie:0.3f}")
        logger.debug("")

        self.controle_i = 1 - self.controle_p if self.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03) else 0
        self.controle_ie = 1 if self.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03) else min(self.controle_ie, 0.3)

        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"],), self.cfg["pot_minima"],)
        logger.debug(f"[USN] Potência alvo: {pot_alvo:0.3f}")

        pot_alvo = self.ajuste_potencia(pot_alvo)
        self.escrever_valores()

    def controle_ugs_disponiveis(self) -> list:
        ls = [ug for ug in self.ugs if ug.disponivel and not ug.etapa_atual == UG_PARANDO]

        if self.modo_de_escolha_das_ugs == MODO_ESCOLHA_MANUAL:
            ls = sorted(ls, key=lambda y: (-1 * y.leitura_potencia.valor, -1 * y.setpoint, y.prioridade,))
            logger.debug("")
            logger.debug("[USN] UGs disponíveis em ordem (prioridade):")
        else:
            ls = sorted(ls, key=lambda y: (y.leitura_horimetro.valor, -1 * y.leitura_potencia.valor, -1 * y.setpoint,))
            logger.debug("")
            logger.debug("[USN] UGs disponíveis em ordem (horas-máquina):")

        return ls

    def controle_reservatorio(self) -> int:
        # Reservatório acima do nível máximo
        if self.nv_montante >= self.cfg["nv_maximo"]:
            logger.info("[USN] Nível montante acima do máximo.")
            if self.nv_montante_recente >= NIVEL_MAXIMORUM:
                logger.critical(f"[USN] Nivel montante ({self.nv_montante_recente:3.2f}) atingiu o maximorum!")
                self.distribuir_potencia(0)
                return NV_FLAG_EMERGENCIA
            else:
                self.controle_i = 0.5
                self.controle_ie = 0.5
                self.distribuir_potencia(self.cfg["pot_maxima_usina"])
                for ug in self.ugs: ug.step()

        # Reservatório abaixo do nível mínimo
        elif self.nv_montante < self.cfg["nv_minimo"] and not self.aguardando_reservatorio:
            logger.info("[USN] Nível montante abaixo do mínimo.")
            self.aguardando_reservatorio = True
            self.distribuir_potencia(0)
            if self.nv_montante_recente < NIVEL_FUNDO_RESERVATORIO:
                if not self.ping(self.dict["IP"]["TDA_slave_ip"]):
                    return NV_FLAG_TDAOFFLINE
                else:
                    logger.critical(f"[USN] Nivel montante ({self.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                    return NV_FLAG_EMERGENCIA

        # Aguardando nível do reservatório
        elif self.aguardando_reservatorio:
            if self.nv_montante > self.cfg["nv_alvo"]:
                logger.debug("[USN] Nível montante dentro do limite de operação.")
                self.aguardando_reservatorio = False
            else:
                
                return NV_FLAG_AGUARDANDO

        # Reservatório Normal
        else:
            self.controle_potencia()
            for ug in self.ugs: ug.step()

        return NV_FLAG_NORMAL