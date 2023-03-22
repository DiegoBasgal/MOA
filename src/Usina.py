import pytz
import logging
import threading
import subprocess

from time import sleep, time
from datetime import  datetime, timedelta

from condicionadores import *
from dicionarios.reg import *
from dicionarios.dict import *
from dicionarios.const import *

from leitura import *
from conector import *

from unidade_geracao import UnidadeDeGeracao

logger = logging.getLogger("__main__")

class Usina:
    def __init__(
            self, 
            sd: dict | None = ...,
            cfg: dict | None = ...,
            cln: ClientsUsn | None = ...,
            con: ConectorCampo | None = ...,
            db: ConectorBancoDados | None = ...,
            ugs: list[UnidadeDeGeracao] | None = ...
        ):

        if None in (sd, cfg):
            logger.warning("[USN] Não foi possível carregar os arquivos de configuração e dicionário compartilhado.")
            raise ValueError
        else:
            self.cfg = cfg
            self.dict = sd

        if None in (db, con, cln):
            logger.warning("[USN] Não foi possível conectar às classes de conexão de campo e banco de dados.")
            raise ConnectionError
        else:
            self.db = db
            self.con = con
            self.cln = cln
            self.opc = cln.opc_client
            self.clp_moa = cln.clp_dict["clp_moa"]

        if ugs is None:
            logger.warning("[USN] Não foi possível carregar instâncias das unidades de geração.")
            raise ImportError
        else:
            self.ugs = ugs
            self.ug1 = ugs[0]
            self.ug2 = ugs[1]

        # ATRIBUIÇÃO DE VARIÀVEIS PRIVADAS
        self.__split1: bool = False
        self.__split2: bool = False

        self.__condicionadores: list[CondicionadorBase]
        self.__condicionadores_essenciais: list[CondicionadorBase]
        
        self.__tensao_rs = LeituraOpc(self.cln, OPC_UA["LT_VAB"])
        self.__tensao_st = LeituraOpc(self.cln, OPC_UA["LT_VBC"])
        self.__tensao_tr = LeituraOpc(self.cln, OPC_UA["LT_VCA"])
        self.__nv_montante = LeituraOpc(self.cln, OPC_UA["NIVEL_MONTANTE"])
        self.__potencia_ativa_kW = LeituraOpc(self.cln, "ns=7;s=CLP_SA.")

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

        self.modo_de_escolha_das_ugs: int = 0

        self.controle_p: float = 0
        self.controle_i: float = 0
        self.controle_d: float = 0

        self.erro_nv: float = 0
        self.erro_nv_anterior: float = 0
        self.nv_montante_recente: float = 0
        self.nv_montante_anterior: float = 0

        # Define as vars inciais
        self.ts_last_ping_tda = self.get_time
        self.ts_ultima_tentativa_normalizacao = self.get_time

        self.ts_nv = []
        self.nv_montante_recentes = []
        self.nv_montante_anteriores = []

        self.pot_disp = 0
        self.state_moa = 0
        self.pot_alvo_anterior = -1
        self.db_emergencia_acionada = 0
        self.clp_emergencia = 0
        self.aguardando_reservatorio = 0
        self.agendamentos_atrasados = 0

        self.borda_emerg: bool = False
        self.acionar_voip: bool = False
        self.tensao_emerg_comporta: bool = True
        self.normalizar_forcado: bool = False

        self.ler_valores()
        self.controle_inicial()
        self.normalizar_usina()
        self.escrever_valores()

    # Getters de variáveis PRIVADAS
    @property
    def tensao_rs(self) -> int | float:
        return self.__tensao_rs.valor

    @property
    def tensao_st(self) -> int | float:
        return self.__tensao_st.valor

    @property
    def tensao_tr(self) -> int | float:
        return self.__tensao_tr.valor

    @property
    def nv_montante(self) -> int | float:
        return self.__nv_montante.valor

    @property
    def potencia_ativa_kW(self) -> int | float:
        return self.__potencia_ativa_kW.valor

    @property
    def condicionadores(self) -> list[CondicionadorBase]:
        return self.__condicionadores

    @property
    def condicionadores_essenciais(self) -> list[CondicionadorBase]:
        return self.__condicionadores_essenciais


    # Getters e Setters de variáveis PROTEGIDAS
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
    def pot_alvo_anterior(self) -> int | float:
        return self._potencia_alvo_anterior

    @pot_alvo_anterior.setter
    def pot_alvo_anterior(self, var: int | float):
        self._potencia_alvo_anterior = var


    def get_time(self) -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def ajustar_ie_padrao(self) -> int:
        return [sum(ug.leitura_potencia) for ug in self.ugs] / self.cfg["pot_maxima_alvo"]

    def acionar_emergencia(self) -> None:
        self.clp_emergencia = True
        self.con.acionar_emergencia()

    def controle_inicial(self) -> None:
        self.ug_operando += [1 for ug in self.ugs if ug.etapa_atual == UG_SINCRONIZADA]

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False

        self.controle_ie = self.ajustar_ie_padrao() if self.cfg["saida_ie_inicial"] == "auto" else self.cfg["saida_ie_inicial"]

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
            self.clp_moa.write_single_coil(MB["MOA"]["MOA_OUT_STATUS"], [self.estado_moa])
            self.clp_moa.write_single_coil(MB["MOA"]["MOA_OUT_MODE"], [self.modo_autonomo])

            if self.modo_autonomo:
                self.clp_moa.write_single_coil(MB["MOA"]["OUT_EMERG"], [self.clp_emergencia])
                self.clp_moa.write_multiple_registers(MB["MOA"]["OUT_SETPOINT"], [int(sum(ug.setpoint)) for ug in self.ugs])
                self.clp_moa.write_multiple_registers(MB["MOA"]["OUT_TARGET_LEVEL"], [int((self.cfg["nv_alvo"] - 800) * 1000)])

                if self.dict["GLB"]["avisado_eletrica"] and not self.borda_emerg:
                    [self.clp_moa.write_single_coil(MB["MOA"][f"OUT_BLOCK_UG{ug.id}"], [1]) for ug in self.ugs]
                    self.borda_emerg = True

                elif not self.dict["GLB"]["avisado_eletrica"] and self.borda_emerg:
                    [self.clp_moa.write_single_coil(MB["MOA"][f"OUT_BLOCK_UG{ug.id}"], [0]) for ug in self.ugs]
                    self.borda_emerg = False

                if self.clp_moa.read_coils(MB["MOA"]["IN_HABILITA_AUTO"])[0] == 1:
                    self.clp_moa.write_single_coil(MB["MOA"]["IN_HABILITA_AUTO"], [1])
                    self.clp_moa.write_single_coil(MB["MOA"]["IN_DESABILITA_AUTO"], [0])
                    self.modo_autonomo = True

                elif self.clp_moa.read_coils(MB["MOA"]["IN_DESABILITA_AUTO"])[0] == 1:
                    self.clp_moa.write_single_coil(MB["MOA"]["IN_HABILITA_AUTO"], [0])
                    self.clp_moa.write_single_coil(MB["MOA"]["IN_DESABILITA_AUTO"], [1])
                    self.modo_autonomo = False

                for ug in self.ugs:
                    if self.clp_moa.read_coils(MB["MOA"][f"OUT_BLOCK_UG{ug.id}"])[0] == 1:
                        self.clp_moa.write_single_coil(MB["MOA"][f"OUT_BLOCK_UG{ug.id}"], [1])
                    elif self.clp_moa.read_coils(MB["MOA"][f"OUT_BLOCK_UG{ug.id}"])[0] == 0:
                        self.clp_moa.write_single_coil(MB["MOA"][f"OUT_BLOCK_UG{ug.id}"], [0])

            elif not self.modo_autonomo:
                self.clp_moa.write_single_coil(MB["MOA"]["OUT_EMERG"], [0])
                self.clp_moa.write_single_coil(MB["MOA"]["OUT_SETPOINT"], [0])
                self.clp_moa.write_single_coil(MB["MOA"]["OUT_TARGET_LEVEL"], [0])
                [self.clp_moa.write_single_coil(MB["MOA"][f"OUT_BLOCK_UG{ug.id}"], [0]) for ug in self.ugs]

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def ler_valores(self) -> None:
        self.cln.ping_clients()
        try:
            if self.clp_moa.read_coils(MB["MOA"]["IN_EMERG"])[0] == 1 and not self.dict["GLB"]["avisado_eletrica"]:
                self.dict["GLB"]["avisado_eletrica"] = True
                for ug in self.ugs:
                    ug.deve_ler_condicionadores = True

            elif self.clp_moa.read_coils(MB["MOA"]["IN_EMERG"])[0] == 0 and self.dict["GLB"]["avisado_eletrica"]:
                self.dict["GLB"]["avisado_eletrica"] = True

            if self.clp_moa.read_coils(MB["MOA"]["IN_EMERG_UG1"])[0] == 1:
                self.ug1.deve_ler_condicionadores = True

            if self.clp_moa.read_coils(MB["MOA"]["IN_EMERG_UG2"])[0] == 1:
                self.ug2.deve_ler_condicionadores = True

            if self.clp_moa.read_coils(MB["MOA"]["IN_HABILITA_AUTO"])[0] == 1:
                self.clp_moa.write_single_coil(MB["MOA"]["IN_HABILITA_AUTO"], [1])
                self.clp_moa.write_single_coil(MB["MOA"]["IN_DESABILITA_AUTO"], [0])

            if self.clp_moa.read_coils(MB["MOA"]["IN_DESABILITA_AUTO"])[0] == 1:
                self.clp_moa.write_single_coil(MB["MOA"]["IN_HABILITA_AUTO"], [0])
                self.clp_moa.write_single_coil(MB["MOA"]["IN_DESABILITA_AUTO"], [1])

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao tentar ler valores modbus no CLP MOA. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

        self.heartbeat()
        self.atualizar_montante_recente()

        parametros = self.db.get_parametros_usina()
        self.atualizar_cfg(parametros)
        self.atualizar_parametros_db(parametros)
        self.atualizar_limites_condicionadores(parametros)

    def escrever_valores(self) -> None:
        try:
            self.db.update_valores_usina(
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),  # timestamp
                1 if self.aguardando_reservatorio else 0,  # aguardando_reservatorio
                True,  # DEPRECATED clp_online
                self.nv_montante if not self.dict["GLB"]["tda_offline"] else 0, # nv_montante
                1 if self.ug1.disponivel else 0,  # ug1_disp
                self.ug1.leitura_potencia,  # ug1_pot
                self.ug1.setpoint,  # ug1_setpot
                self.ug1.etapa_atual,  # ug1_sinc
                self.ug1.leitura_horimetro,  # ug1_tempo
                1 if self.ug2.disponivel else 0,  # ug2_disp
                self.ug2.leitura_potencia,  # ug2_pot
                self.ug2.setpoint,  # ug2_setpot
                self.ug2.etapa_atual,  # ug2_sinc
                self.ug2.leitura_horimetro,  # ug2_tempo
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
                self.ug1.leitura_potencia,
                self.ug2.setpoint,
                self.ug2.leitura_potencia,
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
            self.cfg["kp"] = float(parametros["kp"])
            self.cfg["ki"] = float(parametros["ki"])
            self.cfg["kd"] = float(parametros["kd"])
            self.cfg["kie"] = float(parametros["kie"])

            self.cfg["pt_kp"] = float(parametros["pt_kp"])
            self.cfg["pt_ki"] = float(parametros["pt_ki"])
            self.cfg["pt_kie"] = float(parametros["pt_kie"])
            self.cfg["press_turbina_alvo"] = float(parametros["press_turbina_alvo"])

            self.cfg["nv_alvo"] = float(parametros["nv_alvo"])
            self.cfg["nv_minimo"] = float(parametros["nv_minimo"])

            self.cfg["pot_maxima_alvo"] = float(parametros["pot_nominal"])
            self.cfg["pot_maxima_ug"] = float(parametros["pot_nominal_ug"])
            self.cfg["pot_maxima_usina"] = float(parametros["pot_nominal_ug"]) * 2

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao atualizar o arquivo de configuração \"cfg.json\". Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def atualizar_limites_condicionadores(self, db):
        parametros = db
        for ug in self.ugs:
            try:
                ug.prioridade = int(parametros["ug{}_prioridade".format(ug.id)])
                
                ug.condicionador_temperatura_fase_r_ug.valor_base = float(parametros["alerta_temperatura_fase_r_ug{}".format(ug.id)])
                ug.condicionador_temperatura_fase_r_ug.valor_limite = float(parametros["limite_temperatura_fase_r_ug{}".format(ug.id)])

                ug.condicionador_temperatura_fase_s_ug.valor_base = float(parametros["alerta_temperatura_fase_s_ug{}".format(ug.id)])
                ug.condicionador_temperatura_fase_s_ug.valor_limite = float(parametros["limite_temperatura_fase_s_ug{}".format(ug.id)])

                ug.condicionador_temperatura_fase_t_ug.valor_base = float(parametros["alerta_temperatura_fase_t_ug{}".format(ug.id)])
                ug.condicionador_temperatura_fase_t_ug.valor_limite = float(parametros["limite_temperatura_fase_t_ug{}".format(ug.id)])

                ug.condicionador_temperatura_nucleo_gerador_1_ug.valor_base = float(parametros["alerta_temperatura_nucleo_gerador_1_ug{}".format(ug.id)])
                ug.condicionador_temperatura_nucleo_gerador_1_ug.valor_limite = float(parametros["limite_temperatura_nucleo_gerador_1_ug{}".format(ug.id)])

                ug.condicionador_temperatura_mancal_guia_ug.valor_base = float(parametros["alerta_temperatura_mancal_guia_ug{}".format(ug.id)])
                ug.condicionador_temperatura_mancal_guia_ug.valor_limite = float(parametros["limite_temperatura_mancal_guia_ug{}".format(ug.id)])

                ug.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base = float(parametros["alerta_temperatura_mancal_guia_interno_1_ug{}".format(ug.id)])
                ug.condicionador_temperatura_mancal_guia_interno_1_ug.valor_limite = float(parametros["limite_temperatura_mancal_guia_interno_1_ug{}".format(ug.id)])

                ug.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base = float(parametros["alerta_temperatura_mancal_guia_interno_2_ug{}".format(ug.id)])
                ug.condicionador_temperatura_mancal_guia_interno_2_ug.valor_limite = float(parametros["limite_temperatura_mancal_guia_interno_2_ug{}".format(ug.id)])

                ug.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base = float(parametros["alerta_temperatura_patins_mancal_comb_1_ug{}".format(ug.id)])
                ug.condicionador_temperatura_patins_mancal_comb_1_ug.valor_limite = float(parametros["limite_temperatura_patins_mancal_comb_1_ug{}".format(ug.id)])
                
                ug.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base = float(parametros["alerta_temperatura_patins_mancal_comb_2_ug{}".format(ug.id)])
                ug.condicionador_temperatura_patins_mancal_comb_2_ug.valor_limite = float(parametros["limite_temperatura_patins_mancal_comb_2_ug{}".format(ug.id)])

                ug.condicionador_temperatura_mancal_casq_comb_ug.valor_base = float(parametros["alerta_temperatura_mancal_casq_comb_ug{}".format(ug.id)])
                ug.condicionador_temperatura_mancal_casq_comb_ug.valor_limite = float(parametros["limite_temperatura_mancal_casq_comb_ug{}".format(ug.id)])
                
                ug.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base = float(parametros["alerta_temperatura_mancal_contra_esc_comb_ug{}".format(ug.id)])
                ug.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_limite = float(parametros["limite_temperatura_mancal_contra_esc_comb_ug{}".format(ug.id)])

                ug.condicionador_pressao_turbina_ug.valor_base = float(parametros["alerta_pressao_turbina_ug{}".format(ug.id)])
                ug.condicionador_pressao_turbina_ug.valor_limite = float(parametros["limite_pressao_turbina_ug{}".format(ug.id)])

            except KeyError as e:
                logger.exception(e)

    def acionar_emergencia(self):
        self.con.acionar_emergencia()
        self.clp_emergencia = 1

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
            threading.Thread(target=lambda: self.timeout_tensao(600)).start()

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
                for ug in self.ugs:
                    ug.step()

        # Reservatório abaixo do nível mínimo
        elif self.nv_montante <= self.cfg["nv_minimo"] and not self.aguardando_reservatorio:
            logger.info("[USN] Nível montante abaixo do mínimo.")
            self.aguardando_reservatorio = True
            self.distribuir_potencia(0)
            if self.nv_montante_recente <= NIVEL_FUNDO_RESERVATORIO:
                if not self.clp.ping(self.dict["IP"]["TDA_slave_ip"]):
                    return NV_FLAG_TDAOFFLINE
                else:
                    logger.critical(f"[USN] Nivel montante ({self.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                    return NV_FLAG_EMERGENCIA

        # Aguardando nível do reservatório
        elif self.aguardando_reservatorio:
            if self.nv_montante >= self.cfg["nv_alvo"]:
                logger.debug("[USN] Nível montante dentro do limite de operação.")
                self.aguardando_reservatorio = False
            else:
                return NV_FLAG_AGUARDANDO

        # Reservatório Normal
        else:
            self.controle_potencia()
            for ug in self.ugs: ug.step()

        return NV_FLAG_NORMAL

    def distribuir_potencia(self, pot_alvo):
        
        if self.potencia_alvo_anterior == -1:
            self.potencia_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs:
                ug.setpoint = 0
            return 0

        logger.debug("Pot alvo = {}".format(pot_alvo))

        pot_medidor = self.leituras.potencia_ativa_kW.valor
        logger.debug("Pot no medidor = {}".format(pot_medidor))

        # implementação nova
        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])

        pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

        try:
            if pot_medidor > self.cfg["pot_maxima_alvo"]:
                pot_alvo = self.pot_alvo_anterior * (1 - ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))

        except TypeError as e:
            logger.info("A comunicação com os MFs falharam.")

        self.pot_alvo_anterior = pot_alvo
        
        logger.debug("Pot alvo após ajuste medidor = {}".format(pot_alvo))

        ugs = self.lista_de_ugs_disponiveis()
        self.pot_disp = 0

        logger.debug("lista_de_ugs_disponiveis:")
        for ug in ugs:
            logger.debug("UG{}".format(ug.id))
            self.pot_disp += ug.cfg["pot_maxima_ug{}".format(ugs[0].id)]
        if ugs is None:
            return False
        elif len(ugs) == 0:
            return False

        logger.debug("Distribuindo {}".format(pot_alvo))

        sp = pot_alvo / self.cfg["pot_maxima_usina"]

        self.__split1 = True if sp > (0) else self.__split1
        self.__split2 = (True if sp > (0.5 + self.cfg["margem_pot_critica"]) else self.__split2)

        self.__split2 = False if sp < (0.5) else self.__split2
        self.__split1 = False if sp < (self.cfg["pot_minima"] / self.cfg["pot_maxima_usina"]) else self.__split1

        logger.debug(f"Sp {sp}")
        if len(ugs) == 2:

            if self.__split2:
                logger.debug("Split 2")
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = sp * ugs[1].setpoint_maximo

            elif self.__split1:
                logger.debug("Split 1")
                sp = sp * 2 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = 0
            else:
                for ug in ugs:
                    ug.setpoint = 0

        elif len(ugs) == 1:
            if self.__split1 or self.__split2:
                logger.debug("Split 1B")
                sp = sp * 2 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo

            else:
                for ug in ugs:
                    ug.setpoint = 0

        for ug in self.ugs:
            logger.debug("UG{} SP:{}".format(ug.id, ug.setpoint))

        return pot_alvo

    def lista_de_ugs_disponiveis(self):
        """
        Retorn uma lista de ugs disponiveis conforme a ordenação selecionada
        """
        ls = []
        for ug in self.ugs:
            if ug.disponivel:
                ls.append(ug)

        if self.modo_de_escolha_das_ugs == MODO_ESCOLHA_MANUAL:
            # escolher por maior prioridade primeiro
            ls = sorted(
                ls,
                key=lambda y: (
                    -1 * y.etapa_atual,
                    y.prioridade,
                    -1 * y.leitura_potencia.valor,
                    -1 * y.setpoint,
                ),
            )
        else:
            # escolher por menor horas_maquina primeiro
            ls = sorted(
                ls,
                key=lambda y: (
                    -1 * y.etapa_atual,
                    y.leitura_horimetro.valor,
                    -1 * y.leitura_potencia.valor,
                    -1 * y.setpoint,
                ),
            )
        return ls

    def controle_normal(self):
        """
        Controle PID
        https://en.wikipedia.org/wiki/PID_controller#Proportional
        """
        logger.debug("-------------------------------------------------")

        # Calcula PID
        logger.debug("Alvo: {:0.3f}, Recente: {:0.3f}".format(self.cfg["nv_alvo"], self.nv_montante_recente))
        self.controle_p = self.cfg["kp"] * self.erro_nv
        self.controle_i = max(min((self.cfg["ki"] * self.erro_nv) + self.controle_i, 0.8), 0)
        self.controle_d = self.cfg["kd"] * (self.erro_nv - self.erro_nv_anterior)
        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))
        logger.debug("PID: {:0.3f} <-- P:{:0.3f} + I:{:0.3f} + D:{:0.3f}; ERRO={}".format(
                saida_pid,
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.erro_nv,))

        # Calcula o integrador de estabilidade e limita
        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)

        if self.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if self.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        logger.debug("IE: {:0.3f}".format(self.controle_ie))

        # Arredondamento e limitação
        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"],), self.cfg["pot_minima"],)

        logger.debug("Pot alvo: {:0.3f}".format(pot_alvo))
        logger.debug("Nv alvo: {:0.3f}".format(self.cfg["nv_alvo"]))

    def get_agendamentos_pendentes(self):
        """
        Retorna os agendamentos pendentes para a usina.
        :return: list[] agendamentos

        agora = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        agora = agora - timedelta(seconds=agora.second, microseconds=agora.microsecond)
        """
        agendamentos_pendentes = []
        agendamentos = self.db.get_agendamentos_pendentes()

        for agendamento in agendamentos:
            ag = list(agendamento)
            # ag -> [id, data, observacao, comando_id, executado, campo_auxiliar, criado_por, modificado_por, ts_criado, ts_modificado]
            ag[1] = ag[1] - timedelta(0, 60 * 60 * 3)
            agendamentos_pendentes.append(ag)
        return agendamentos_pendentes

    def verificar_agendamentos(self):
        """
        Verifica os agendamentos feitos pelo django no banco de dados e lida com eles, executando, etc...
        """
        agora = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        agendamentos = self.get_agendamentos_pendentes()

        # resolve os agendamentos muito juntos
        limite_entre_agendamentos_iguais = 300 # segundos
        agendamentos = sorted(agendamentos, key=lambda x:(x[3], x[1]))
        i = 0
        j = len(agendamentos)
        while i < j - 1:

            if agendamentos[i][3] == agendamentos[i+1][3] and (agendamentos[i+1][1] - agendamentos[i][1]).seconds < limite_entre_agendamentos_iguais:
                ag_concatenado = agendamentos.pop(i)
                obs = "Este agendamento foi concatenado ao seguinte por motivos de temporização."
                logger.warning(obs)
                self.db.update_agendamento(ag_concatenado[0], True, obs)
                i -= 1

            i += 1
            j = len(agendamentos)

        i = len(agendamentos)
        logger.debug("Data: {}  Criado por: {}  Comando: {}".format(agendamentos[i-1][1].strftime("%Y-%m-%d %H:%M:%S"), agendamentos[i-1][6], agendamentos[i-1][3]))

        if len(agendamentos) == 0:
            return True

        self.agendamentos_atrasados = 0

        for agendamento in agendamentos:
            # ag -> [id, data, observacao, comando_id, executado, campo_auxiliar, criado_por, modificado_por, ts_criado, ts_modificado]
            if agora > agendamento[1]:
                segundos_adiantados = 0
                segundos_passados = (agora - agendamento[1]).seconds
                logger.debug(segundos_passados)
            else:
                segundos_adiantados = (agendamento[1] - agora).seconds
                segundos_passados = 0

            
            if segundos_passados > 240:
                logger.warning("Agendamento #{} Atrasado! ({}).".format(agendamento[0], agendamento[3]))
                self.agendamentos_atrasados += 1

            if segundos_passados > 5 or self.agendamentos_atrasados > 3:
                logger.info("Os agendamentos estão muito atrasados!")
                if agendamento[3] == AGN_INDISPONIBILIZAR:
                    logger.warning("Acionando emergência!")
                    self.acionar_emergencia()
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    return False
                elif agendamento[3] == AGN_ALTERAR_NV_ALVO or agendamento[3] == AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS or agendamento[3] == AGN_BAIXAR_POT_UGS_MINIMO or agendamento[3] == AGN_NORMALIZAR_POT_UGS_MINIMO:
                    logger.info("Não foi possível executar o agendamento! Favor re-agendar")
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    return False
                elif agendamento[3] in AGN_LST_BLOQUEIO_UG1:
                    logger.info("Indisponibilizando UG1")
                    self.ug1.forcar_estado_indisponivel()
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    return False
                elif agendamento[3] in AGN_LST_BLOQUEIO_UG2:
                    logger.info("Indisponibilizando UG2")
                    self.ug2.forcar_estado_indisponivel()
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    return False
                else:
                    logger.info("Agendamento não encontrado! Retomando operação...")
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="Agendamento inexistente.")
                    return False


            if segundos_adiantados <= 60 and not bool(agendamento[4]):
                # Está na hora e ainda não foi executado. Executar!
                logger.info("Executando gendamento: {} - Comando: {} - Data: .".format(agendamento[0], agendamento[3], agendamento[9]))

                # se o MOA estiver em autonomo e o agendamento não for executavel em autonomo
                #   marca como executado e altera a descricao
                #   proximo
                if (self.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_autmoatico"]):
                    obs = "Este agendamento não tem efeito com o módulo em modo autônomo. Executado sem realizar nenhuma ação"
                    logger.warning(obs)
                    self.db.update_agendamento(agendamento[0], True, obs)
                    return True

                # se o MOA estiver em manual e o agendamento não for executavel em manual
                #   marca como executado e altera a descricao
                #   proximo
                if (not self.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_manual"]):
                    obs = "Este agendamento não tem efeito com o módulo em modo manual. Executado sem realizar nenhuma ação"
                    logger.warning(obs)
                    self.db.update_agendamento(agendamento[0], True, obs)
                    return True

                if agendamento[3] == AGN_INDISPONIBILIZAR:
                    # Coloca em emergência
                    logger.info("Indisponibilizando a usina (comando via agendamento).")
                    for ug in self.ugs:
                        ug.forcar_estado_indisponivel()
                    while (not self.ugs[0].etapa_atual == UG_PARADA and not self.ugs[1].etapa_atual == UG_PARADA):
                        self.ler_valores()
                        logger.debug("Indisponibilizando Usina... \n(freezing for 10 seconds)")
                        sleep(10)
                    self.acionar_emergencia()
                    logger.debug("Emergência pressionada após indizponibilização agendada mudando para modo manual para evitar normalização automática.")
                    self.entrar_em_modo_manual()

                if agendamento[3] == AGN_ALTERAR_NV_ALVO:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                    except Exception as e:
                        logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))

                    self.cfg["nv_alvo"] = novo

                if agendamento[3] == AGN_BAIXAR_POT_UGS_MINIMO:
                    try:
                        self.cfg["pot_maxima_ug1"] = self.cfg["pot_minima"]
                        self.cfg["pot_maxima_ug2"] = self.cfg["pot_minima"]
                        for ug in self.ugs:
                            if ug.etapa_atual == UG_PARADA or ug.etapa_alvo == UG_PARADA:
                                logger.debug("A UG{} já está no estado parada/parando.".format(ug.id))
                            else:
                                logger.debug("Enviando o setpoint mínimo ({}) para a UG{}".format(self.cfg["pot_minima"], ug.id))
                                ug.enviar_setpoint(self.cfg["pot_minima"])

                    except Exception as e:
                        logger.info("Traceback: {}".format(repr(e)))

                if agendamento[3] == AGN_NORMALIZAR_POT_UGS_MINIMO:
                    try:
                        self.cfg["pot_maxima_ug1"] = self.cfg["pot_maxima_ug"]
                        self.cfg["pot_maxima_ug2"] = self.cfg["pot_maxima_ug"]
                        for ug in self.ugs:
                            ug.enviar_setpoint(self.cfg["pot_maxima_ug"])

                    except Exception as e:
                        logger.debug("Traceback: {}".format(repr(e)))

                if agendamento[3] == AGN_UG1_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug1"] = novo
                        self.ug1.pot_disponivel = novo
                    except Exception as e:
                        logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))

                if agendamento[3] == AGN_UG1_FORCAR_ESTADO_MANUAL:
                    self.ug1.forcar_estado_manual()

                if agendamento[3] == AGN_UG1_FORCAR_ESTADO_DISPONIVEL:
                    self.ug1.forcar_estado_disponivel()

                if agendamento[3] == AGN_UG1_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug1.forcar_estado_indisponivel()

                if agendamento[3] == AGN_UG1_FORCAR_ESTADO_RESTRITO:
                    self.ug1.forcar_estado_restrito()

                if agendamento[3] == AGN_UG2_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug2"] = novo
                        self.ug2.pot_disponivel = novo
                    except Exception as e:
                        logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))

                if agendamento[3] == AGN_UG2_FORCAR_ESTADO_MANUAL:
                    self.ug2.forcar_estado_manual()

                if agendamento[3] == AGN_UG2_FORCAR_ESTADO_DISPONIVEL:
                    self.ug2.forcar_estado_disponivel()

                if agendamento[3] == AGN_UG2_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug2.forcar_estado_indisponivel()

                if agendamento[3] == AGN_UG2_FORCAR_ESTADO_RESTRITO:
                    self.ug2.forcar_estado_restrito()

                if agendamento[3] == AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug1"] = novo
                        self.ug1.pot_disponivel = novo
                        self.cfg["pot_maxima_ug2"] = novo
                        self.ug2.pot_disponivel = novo
                    except Exception as e:
                        logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))

                # Após executar, indicar no banco de dados
                self.db.update_agendamento(int(agendamento[0]), 1)
                logger.info("O comando #{} - {} foi executado.".format(agendamento[0], agendamento[5]))
                self.con.reconhecer_emergencia()
                self.escrever_valores()


    def verificar_condicionadores(self) -> int:
        if self.dict["GLB"]["avisado_eletrica"] or [condic.ativo for condic in self.condicionadores_essenciais]:
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]
            condic_flag = [CONDIC_NORMALIZAR for condic in condics_ativos if condic.gravidade == CONDIC_NORMALIZAR]
            condic_flag = [CONDIC_INDISPONIBILIZAR for condic in condics_ativos if condic.gravidade == CONDIC_INDISPONIBILIZAR]

            logger.warning("[USN]")

    def leitura_condicionadores(self):
        
        # Essenciais
        self.leitura_in_emergencia = self.clp_moa.read_coils(MB["MOA"]["IN_EMERG"])[0]
        x = self.leitura_in_emergencia
        self.condicionadores_essenciais.append(CondicionadorBase("MOA_IN_EMERG", CONDIC_INDISPONIBILIZAR, x,))

        self.leitura_sem_emergencia_tda = LeituraOPCBit(self.opc, OPC_UA["TDA"]["SEM_EMERGENCIA"], 24, True)
        x = self.leitura_sem_emergencia_tda
        self.condicionadores_essenciais.append(CondicionadorBase("SEM_EMERGENCIA_TDA - bit 24", CONDIC_NORMALIZAR, x))
        
        self.leitura_sem_emergencia_sa = LeituraOPCBit(self.opc, OPC_UA["SA"]["SEM_EMERGENCIA"], 13, True)
        x = self.leitura_sem_emergencia_sa
        self.condicionadores_essenciais.append(CondicionadorBase("SEM_EMERGENCIA_SA - bit 13", CONDIC_NORMALIZAR, x))

        self.leitura_rele_linha_atuado = LeituraOPCBit(self.opc, OPC_UA["SE"]["RELE_LINHA_ATUADO"], 14)
        x = self.leitura_rele_linha_atuado
        self.condicionadores_essenciais.append(CondicionadorBase("RELE_LINHA_ATUADO - bit 14", CONDIC_NORMALIZAR, x))


        # Gerais
        self.leitura_fusivel_queimado_retificador = LeituraOPCBit(self.opc, OPC_UA["SA"]["RETIFICADOR_FUSIVEL_QUEIMADO"], 2)
        x = self.leitura_fusivel_queimado_retificador
        self.condicionadores.append(CondicionadorBase("RETIFICADOR_FUSIVEL_QUEIMADO - bit 02", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_fuga_terra_positivo_retificador = LeituraOPCBit(self.opc, OPC_UA["SA"]["RETIFICADOR_FUGA_TERRA_POSITIVO"], 5)
        x = self.leitura_fuga_terra_positivo_retificador
        self.condicionadores.append(CondicionadorBase("RETIFICADOR_FUGA_TERRA_POSITIVO - bit 05", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_fuga_terra_negativo_retificador = LeituraOPCBit(self.opc, OPC_UA["SA"]["RETIFICADOR_FUGA_TERRA_NEGATIVO"], 6)
        x = self.leitura_fuga_terra_negativo_retificador
        self.condicionadores.append(CondicionadorBase("RETIFICADOR_FUGA_TERRA_NEGATIVO - bit 06", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_52sa1_sem_falha = LeituraOPCBit(self.opc, OPC_UA["SA"]["52SA1_SEM_FALHA"], 31, True)
        x = self.leitura_52sa1_sem_falha
        self.condicionadores.append(CondicionadorBase("52SA1_SEM_FALHA - bit 31", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_sa_72sa1_fechado = LeituraOPCBit(self.opc, OPC_UA["SA"]["SA_72SA1_FECHADO"], 10, True)
        x = self.leitura_sa_72sa1_fechado
        self.condicionadores.append(CondicionadorBase("SA_72SA1_FECHADO - bit 10", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_disj_125vcc_fechados = LeituraOPCBit(self.opc, OPC_UA["SA"]["DISJUNTORES_125VCC_FECHADOS"], 11, True)
        x = self.leitura_disj_125vcc_fechados
        self.condicionadores.append(CondicionadorBase("DISJUNTORES_125VCC_FECHADOS - bit 11", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_disj_24vcc_fechados = LeituraOPCBit(self.opc, OPC_UA["SA"]["DISJUNTORES_24VCC_FECHADOS"], 12, True)
        x = self.leitura_disj_24vcc_fechados
        self.condicionadores.append(CondicionadorBase("DISJUNTORES_24VCC_FECHADOS - bit 12", CONDIC_INDISPONIBILIZAR, x))
        
        self.leitura_alimentacao_125vcc_com_tensao = LeituraOPCBit(self.opc, OPC_UA["SA"]["COM_TENSAO_ALIMENTACAO_125VCC"], 13, True)
        x = self.leitura_alimentacao_125vcc_com_tensao
        self.condicionadores.append(CondicionadorBase("COM_TENSAO_ALIMENTACAO_125VCC - bit 13", CONDIC_INDISPONIBILIZAR, x))
        
        self.leitura_comando_125vcc_com_tensao = LeituraOPCBit(self.opc, OPC_UA["SA"]["COM_TENSAO_COMANDO_125VCC"], 14, True)
        x = self.leitura_comando_125vcc_com_tensao
        self.condicionadores.append(CondicionadorBase("COM_TENSAO_COMANDO_125VCC - bit 14", CONDIC_INDISPONIBILIZAR, x))
        
        self.leitura_comando_24vcc_com_tensao = LeituraOPCBit(self.opc, OPC_UA["SA"]["COM_TENSAO_COMANDO_24VCC"], 15, True)
        x = self.leitura_comando_24vcc_com_tensao
        self.condicionadores.append(CondicionadorBase("COM_TENSAO_COMANDO_24VCC - bit 15", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_abrir_52sa1 = LeituraOPCBit(self.opc, OPC_UA["SA"]["FALHA_ABRIR_52SA1"], 0)
        x = self.leitura_falha_abrir_52sa1
        self.condicionadores.append(CondicionadorBase("FALHA_ABRIR_52SA1 - bit 00", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_fechar_52sa1 = LeituraOPCBit(self.opc, OPC_UA["SA"]["FALHA_FECHAR_52SA1"], 1)
        x = self.leitura_falha_fechar_52sa1
        self.condicionadores.append(CondicionadorBase("FALHA_FECHAR_52SA1 - bit 01", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_abrir_52sa2 = LeituraOPCBit(self.opc, OPC_UA["SA"]["FALHA_ABRIR_52SA2"], 3)
        x = self.leitura_falha_abrir_52sa2
        self.condicionadores.append(CondicionadorBase("FALHA_ABRIR_52SA2 - bit 03", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_fechar_52sa2 = LeituraOPCBit(self.opc, OPC_UA["SA"]["FALHA_FECHAR_52SA2"], 4)
        x = self.leitura_falha_fechar_52sa2
        self.condicionadores.append(CondicionadorBase("FALHA_FECHAR_52SA2 - bit 04", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_abrir_52sa3 = LeituraOPCBit(self.opc, OPC_UA["SA"]["FALHA_ABRIR_52SA3"], 5)
        x = self.leitura_falha_abrir_52sa3
        self.condicionadores.append(CondicionadorBase("FALHA_ABRIR_52SA3 - bit 05", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_fechar_52sa3 = LeituraOPCBit(self.opc, OPC_UA["SA"]["FALHA_FECHAR_52SA3"], 6)
        x = self.leitura_falha_fechar_52sa3
        self.condicionadores.append(CondicionadorBase("FALHA_FECHAR_52SA3 - bit 06", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_89l_fechada = LeituraOPCBit(self.opc, OPC_UA["SE"]["89L_FECHADA"], 12, True)
        x = self.leitura_89l_fechada
        self.condicionadores.append(CondicionadorBase("89L_FECHADA - bit 12", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_oleo_te = LeituraOPCBit(self.opc, OPC_UA["SE"]["TE_TRIP_TEMPERATURA_OLEO"], 19)
        x = self.leitura_trip_temp_oleo_te
        self.condicionadores.append(CondicionadorBase("TE_TRIP_TEMPERATURA_OLEO - bit 19", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_enrol_te = LeituraOPCBit(self.opc, OPC_UA["SE"]["TE_TRIP_TEMPERATURA_ENROLAMENTO"], 20)
        x = self.leitura_trip_temp_enrol_te
        self.condicionadores.append(CondicionadorBase("TE_TRIP_TEMPERATURA_ENROLAMENTO - bit 20", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_alarme_rele_buchholz = LeituraOPCBit(self.opc, OPC_UA["SE"]["TE_ALARME_RELE_BUCHHOLZ"], 22)
        x = self.leitura_alarme_rele_buchholz
        self.condicionadores.append(CondicionadorBase("TE_ALARME_RELE_BUCHHOLZ - bit 22", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_rele_buchholz = LeituraOPCBit(self.opc, OPC_UA["SE"]["TE_TRIP_RELE_BUCHHOLZ"], 23)
        x = self.leitura_trip_rele_buchholz
        self.condicionadores.append(CondicionadorBase("TE_TRIP_RELE_BUCHHOLZ - bit 23", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_alivio_pressao = LeituraOPCBit(self.opc, OPC_UA["SE"]["TE_TRIP_ALIVIO_PRESSAO"], 24)
        x = self.leitura_trip_alivio_pressao
        self.condicionadores.append(CondicionadorBase("TE_TRIP_ALIVIO_PRESSAO - bit 24", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_atuacao_rele_linha_bf = LeituraOPCBit(self.opc, OPC_UA["SE"]["RELE_LINHA_ATUACAO_BF"], 16)
        x = self.leitura_atuacao_rele_linha_bf
        self.condicionadores.append(CondicionadorBase("RELE_LINHA_ATUACAO_BF - bit 16", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_rele_te_atuado = LeituraOPCBit(self.opc, OPC_UA["SE"]["TE_RELE_ATUADO"], 17)
        x = self.leitura_rele_te_atuado
        self.condicionadores.append(CondicionadorBase("TE_RELE_ATUADO - bit 17", CONDIC_INDISPONIBILIZAR, x))
        
        self.leitura_86bf_atuado = LeituraOPCBit(self.opc, OPC_UA["SE"]["86BF_ATUADO"], 19)
        x = self.leitura_86bf_atuado
        self.condicionadores.append(CondicionadorBase("86BF_ATUADO - bit 19", CONDIC_INDISPONIBILIZAR, x))
        
        self.leitura_86t_atuado = LeituraOPCBit(self.opc, OPC_UA["SE"]["86T_ATUADO"], 20)
        x = self.leitura_86t_atuado
        self.condicionadores.append(CondicionadorBase("86T_ATUADO - bit 20", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_super_bobinas_reles_bloq = LeituraOPCBit(self.opc, OPC_UA["SE"]["SUPERVISAO_BOBINAS_RELES_BLOQUEIOS"], 21)
        x = self.leitura_super_bobinas_reles_bloq
        self.condicionadores.append(CondicionadorBase("SUPERVISAO_BOBINAS_RELES_BLOQUEIOS - bit 21", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_comando_abertura_52l = LeituraOPCBit(self.opc, OPC_UA["SE"]["FALHA_COMANDO_ABERTURA_52L"], 1)
        x = self.leitura_falha_comando_abertura_52l
        self.condicionadores.append(CondicionadorBase("FALHA_COMANDO_ABERTURA_52L - bit 01", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_comando_fechamento_52l = LeituraOPCBit(self.opc, OPC_UA["SE"]["FALHA_COMANDO_FECHAMENTO_52L"], 2)
        x = self.leitura_falha_comando_fechamento_52l
        self.condicionadores.append(CondicionadorBase("FALHA_COMANDO_FECHAMENTO_52L - bit 02", CONDIC_INDISPONIBILIZAR, x))


        # Normalizar
        self.leitura_retificador_subtensao = LeituraOPCBit(self.opc, OPC_UA["SA"]["RETIFICADOR_SUBTENSAO"], 31)
        x = self.leitura_retificador_subtensao
        self.condicionadores.append(CondicionadorBase("RETIFICADOR_SUBTENSAO - bit 31", CONDIC_NORMALIZAR, x))
        
        self.leitura_ca_com_tensao = LeituraOPCBit(self.opc, OPC_UA["TDA"]["COM_TENSAO_CA"], 11, True)
        x = self.leitura_ca_com_tensao
        self.condicionadores.append(CondicionadorBase("COM_TENSAO_CA - bit 11", CONDIC_NORMALIZAR, x))

        self.leitura_falha_ligar_bomba_uh = LeituraOPCBit(self.opc, OPC_UA["TDA"]["UH_FALHA_LIGAR_BOMBA"], 2)
        x = self.leitura_falha_ligar_bomba_uh
        self.condicionadores.append(CondicionadorBase("UH_FALHA_LIGAR_BOMBA - bit 02", CONDIC_NORMALIZAR, x))

        self.leitura_retificador_sobretensao = LeituraOPCBit(self.opc, OPC_UA["SA"]["RETIFICADOR_SOBRETENSAO"], 30)
        x = self.leitura_retificador_sobretensao
        self.condicionadores.append(CondicionadorBase("RETIFICADOR_SOBRETENSAO - bit 30", CONDIC_NORMALIZAR, x))

        self.leitura_retificador_sobrecorrente_saida = LeituraOPCBit(self.opc, OPC_UA["SA"]["RETIFICADOR_SOBRECORRENTE_SAIDA"], 0)
        x = self.leitura_retificador_sobrecorrente_saida
        self.condicionadores.append(CondicionadorBase("RETIFICADOR_SOBRECORRENTE_SAIDA - bit 00", CONDIC_NORMALIZAR, x))

        self.leitura_retificador_sobrecorrente_baterias = LeituraOPCBit(self.opc, OPC_UA["SA"]["RETIFICADOR_SOBRECORRENTE_BATERIAS"], 1)
        x = self.leitura_retificador_sobrecorrente_baterias
        self.condicionadores.append(CondicionadorBase("RETIFICADOR_SOBRECORRENTE_BATERIAS - bit 01", CONDIC_NORMALIZAR, x))

        self.leitura_falha_sistema_agua_pressurizar_fa = LeituraOPCBit(self.opc, OPC_UA["SA"]["SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_A"], 3)
        x = self.leitura_falha_sistema_agua_pressurizar_fa
        self.condicionadores.append(CondicionadorBase("SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_A - bit 03", CONDIC_NORMALIZAR, x))

        self.leitura_falha_sistema_agua_pressostato_fa = LeituraOPCBit(self.opc, OPC_UA["SA"]["SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_A"], 4)
        x = self.leitura_falha_sistema_agua_pressostato_fa
        self.condicionadores.append(CondicionadorBase("SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_A - bit 04", CONDIC_NORMALIZAR, x))

        self.leitura_falha_sistema_agua_pressurizar_fb = LeituraOPCBit(self.opc, OPC_UA["SA"]["SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_B"], 5)
        x = self.leitura_falha_sistema_agua_pressurizar_fb
        self.condicionadores.append(CondicionadorBase("SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_B - bit 05", CONDIC_NORMALIZAR, x))
        
        self.leitura_falha_sistema_agua_pressostato_fb = LeituraOPCBit(self.opc, OPC_UA["SA"]["SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_B"], 6)
        x = self.leitura_falha_sistema_agua_pressostato_fb
        self.condicionadores.append(CondicionadorBase("SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_B - bit 06", CONDIC_NORMALIZAR, x))

        return True

    def leituras_por_hora(self):
        # Telegram

        self.leitura_filtro_limpo_uh = LeituraOPCBit(self.opc, OPC_UA["TDA"]["UH_FILTRO_LIMPO"], 13, True)
        if not self.leitura_filtro_limpo_uh:
            logger.warning("O filtro da UH da TDA está sujo. Favor realizar limpeza/troca.")

        self.leitura_ca_com_tensao = LeituraOPCBit(self.opc, OPC_UA["TDA"]["COM_TENSAO_CA"], 11, True)
        if not self.leitura_ca_com_tensao:
            logger.warning("Foi dentificado que o CA da tomada da água está sem tensão. Favor verificar.")

        self.leitura_lg_operacao_manual = LeituraOPCBit(self.opc, OPC_UA["TDA"]["LG_OPERACAO_MANUAL"], 0)
        if self.leitura_lg_operacao_manual:
            logger.warning("Foi identificado que o Limpa Grades entrou em operação manual. Favor verificar.")

        self.leitura_nivel_jusante_comporta_1 = LeituraOPCBit(self.opc, OPC_UA["TDA"]["NIVEL_JUSANTE_COMPORTA_1"], 2)
        if self.leitura_nivel_jusante_comporta_1:
            logger.warning("Houve uma falha no sensor de nível jusante da comporta 1. Favor verificar.")

        self.leitura_nivel_jusante_comporta_2 = LeituraOPCBit(self.opc, OPC_UA["TDA"]["NIVEL_JUSANTE_COMPORTA_2"], 4)
        if self.leitura_nivel_jusante_comporta_2:
            logger.warning("Houve uma falha no sensor de nível jusante da comporta 2. Favor verificar.")

        self.leitura_nivel_jusante_grade_comporta_1 = LeituraOPCBit(self.opc, OPC_UA["TDA"]["FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_1"], 1)
        if self.leitura_nivel_jusante_grade_comporta_1:
            logger.warning("Houve uma falha no sensor de nível jusante grade da comporta 1. Favor verificar.")

        self.leitura_nivel_jusante_grade_comporta_2 = LeituraOPCBit(self.opc, OPC_UA["TDA"]["FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_2"], 3)
        if self.leitura_nivel_jusante_grade_comporta_2:
            logger.warning("Houve uma falha no sensor de nível jusante grade da comporta 2. Favor verificar.")
        
        self.leitura_falha_bomba_drenagem_1 = LeituraOPCBit(self.opc, OPC_UA["SA"]["DRENAGEM_BOMBA_1_FALHA"], 0)
        if self.leitura_falha_bomba_drenagem_1:
            logger.warning("Houve uma falha na bomba 1 do poço de drenagem. Favor verificar.")
        
        self.leitura_falha_bomba_drenagem_2 = LeituraOPCBit(self.opc, OPC_UA["SA"]["DRENAGEM_BOMBA_2_FALHA"], 2)
        if self.leitura_falha_bomba_drenagem_2:
            logger.warning("Houve uma falha na bomba 2 do poço de drenagem. Favor verificar.")
        
        self.leitura_falha_bomba_drenagem_3 = LeituraOPCBit(self.opc, OPC_UA["SA"]["DRENAGEM_BOMBA_3_FALHA"], 4)
        if self.leitura_falha_bomba_drenagem_3:
            logger.warning("Houve uma falha na bomba 3 do poço de drenagem. Favor verificar.")

        self.leitura_djs_barra_seletora_remoto = LeituraOPCBit(self.opc, OPC_UA["SA"]["DISJUNTORES_BARRA_SELETORA_REMOTO"], 9)
        if self.leitura_djs_barra_seletora_remoto:
            logger.warning("Os disjuntores da barra seletora saíram do modo remoto. Favor verificar.")

        self.leitura_discrepancia_boia_poco_drenagem = LeituraOPCBit(self.opc, OPC_UA["SA"]["DRENAGEM_DISCREPANCIA_BOIAS_POCO"], 9)
        if self.leitura_discrepancia_boia_poco_drenagem:
            logger.warning("Foram identificados sinais inconsistentes nas boias do poço de drenagem. Favor verificar.")

        self.leitura_falha_ligar_bomba_sis_agua = LeituraOPCBit(self.opc, OPC_UA["SA"]["SISTEMA_AGUA_FALHA_LIGA_BOMBA"], 1)
        if self.leitura_falha_ligar_bomba_sis_agua:
            logger.warning("Houve uma falha ao ligar a bomba do sistema de água. Favor verificar.")

        self.leitura_bomba_sis_agua_disp = LeituraOPCBit(self.opc, OPC_UA["SA"]["SISTEMA_AGUA_BOMBA_DISPONIVEL"], 0, True)
        if not self.leitura_bomba_sis_agua_disp:
            logger.warning("Foi identificado que a bomba do sistema de água está indisponível. Favor verificar.")

        self.leitura_seletora_52l_remoto = LeituraOPCBit(self.opc, OPC_UA["SE"]["52L_SELETORA_REMOTO"], 10, True)
        if not self.leitura_seletora_52l_remoto:
            logger.warning("O Disjuntor 52L saiu do modo remoto. Favor verificar.")

        self.leitura_falha_temp_oleo_te = LeituraOPCBit(self.opc, OPC_UA["SE"]["TE_FALHA_TEMPERATURA_OLEO"], 1)
        if self.leitura_falha_temp_oleo_te:
            logger.warning("Houve uma falha de leitura de temperatura do óleo do transformador elevador. Favor verificar.")

        self.leitura_falha_temp_enrolamento_te = LeituraOPCBit(self.opc, OPC_UA["SE"]["TE_FALHA_TEMPERATURA_ENROLAMENTO"], 2)
        if self.leitura_falha_temp_enrolamento_te:
            logger.warning("Houve uma falha de leitura de temperatura do enrolamento do transformador elevador. Favor verificar.")


        # Telegram + Voip
        self.leitura_falha_atuada_lg = LeituraOPCBit(self.opc, OPC_UA["TDA"]["LG_FALHA_ATUADA"], 31)
        if self.leitura_falha_atuada_lg and not self.dict["VOIP"]["LG_FALHA_ATUADA"]:
            logger.warning("Foi identificado que o limpa grades está em falha. Favor verificar.")
            self.dict["VOIP"]["LG_FALHA_ATUADA"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_atuada_lg and self.dict["VOIP"]["LG_FALHA_ATUADA"]:
            self.dict["VOIP"]["LG_FALHA_ATUADA"] = False

        self.leitura_falha_nivel_montante = LeituraOPCBit(self.opc, OPC_UA["TDA"]["FALHA_NIVEL_MONTANTE"], 0)
        if self.leitura_falha_nivel_montante and not self.dict["VOIP"]["FALHA_NIVEL_MONTANTE"]:
            logger.warning("Houve uma falha na leitura de nível montante. Favor verificar.")
            self.dict["VOIP"]["FALHA_NIVEL_MONTANTE"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_nivel_montante and self.dict["VOIP"]["FALHA_NIVEL_MONTANTE"]:
            self.dict["VOIP"]["FALHA_NIVEL_MONTANTE"] = False

        self.leitura_falha_bomba_filtragem = LeituraOPCBit(self.opc, OPC_UA["SA"]["FILTRAGEM_BOMBA_FALHA"], 6)
        if self.leitura_falha_bomba_filtragem and not self.dict["VOIP"]["FILTRAGEM_BOMBA_FALHA"]:
            logger.warning("Houve uma falha na bomba de filtragem. Favor verificar.")
            self.dict["VOIP"]["FILTRAGEM_BOMBA_FALHA"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_bomba_filtragem and self.dict["VOIP"]["FILTRAGEM_BOMBA_FALHA"]:
            self.dict["VOIP"]["FILTRAGEM_BOMBA_FALHA"] = False

        self.leitura_falha_bomba_drenagem_uni = LeituraOPCBit(self.opc, OPC_UA["SA"]["DRENAGEM_UNIDADES_BOMBA_FALHA"], 12)
        if self.leitura_falha_bomba_drenagem_uni and not self.dict["VOIP"]["DRENAGEM_UNIDADES_BOMBA_FALHA"]:
            logger.warning("Houve uma falha na bomba de drenagem. Favor verificar.")
            self.dict["VOIP"]["DRENAGEM_UNIDADES_BOMBA_FALHA"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_bomba_drenagem_uni and self.dict["VOIP"]["DRENAGEM_UNIDADES_BOMBA_FALHA"]:
            self.dict["VOIP"]["DRENAGEM_UNIDADES_BOMBA_FALHA"] = False

        self.leitura_falha_tubo_succao_bomba_recalque = LeituraOPCBit(self.opc, OPC_UA["SA"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"], 14)
        if self.leitura_falha_tubo_succao_bomba_recalque and not self.dict["VOIP"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"]:
            logger.warning("Houve uma falha na sucção da bomba de recalque. Favor verificar.")
            self.dict["VOIP"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_tubo_succao_bomba_recalque and self.dict["VOIP"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"]:
            self.dict["VOIP"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"] = False

        self.leitura_nivel_muito_alto_poco_drenagem = LeituraOPCBit(self.opc, OPC_UA["SA"]["POCO_DRENAGEM_NIVEL_MUITO_ALTO"], 25)
        if self.leitura_nivel_muito_alto_poco_drenagem and not self.dict["VOIP"]["POCO_DRENAGEM_NIVEL_MUITO_ALTO"]:
            logger.warning("Nível do poço de drenagem está muito alto. Favor verificar.")
            self.dict["VOIP"]["POCO_DRENAGEM_NIVEL_MUITO_ALTO"] = True
            self.acionar_voip = True
        elif not self.leitura_nivel_muito_alto_poco_drenagem and self.dict["VOIP"]["POCO_DRENAGEM_NIVEL_MUITO_ALTO"]:
            self.dict["VOIP"]["POCO_DRENAGEM_NIVEL_MUITO_ALTO"] = False

        self.leitura_nivel_alto_poco_drenagem = LeituraOPCBit(self.opc, OPC_UA["SA"]["POCO_DRENAGEM_NIVEL_ALTO"], 26)
        if self.leitura_nivel_alto_poco_drenagem and not self.dict["VOIP"]["POCO_DRENAGEM_NIVEL_ALTO"]:
            logger.warning("Nível do poço de drenagem alto. Favor verificar.")
            self.dict["VOIP"]["POCO_DRENAGEM_NIVEL_ALTO"] = True
            self.acionar_voip = True
        elif not self.leitura_nivel_alto_poco_drenagem and self.dict["VOIP"]["POCO_DRENAGEM_NIVEL_ALTO"]:
            self.dict["VOIP"]["POCO_DRENAGEM_NIVEL_ALTO"] = False

        self.leitura_sem_falha_52sa1 = LeituraOPCBit(self.opc, OPC_UA["SA"]["52SA1_SEM_FALHA"], 31, True)
        if not self.leitura_sem_falha_52sa1 and not self.dict["VOIP"]["52SA1_SEM_FALHA"]:
            logger.warning("Houve uma falha com o disjuntor 52SA1 do transformador do SA. Favor verificar.")
            self.dict["VOIP"]["52SA1_SEM_FALHA"] = True
        elif self.leitura_sem_falha_52sa1 and self.dict["VOIP"]["52SA1_SEM_FALHA"]:
            self.dict["VOIP"]["52SA1_SEM_FALHA"] = False

        self.leitura_sem_falha_52sa2 = LeituraOPCBit(self.opc, OPC_UA["SA"]["52SA2_SEM_FALHA"], 1, True)
        if not self.leitura_sem_falha_52sa2 and not self.dict["VOIP"]["52SA2_SEM_FALHA"]:
            logger.warning("Houve uma falha com o disjuntor 52SA2 do Gerador Diesel. Favor verificar.")
            self.dict["VOIP"]["52SA2_SEM_FALHA"] = True
            self.acionar_voip = True
        elif self.leitura_sem_falha_52sa2 and self.dict["VOIP"]["52SA2_SEM_FALHA"]:
            self.dict["VOIP"]["52SA2_SEM_FALHA"] = False

        self.leitura_sem_falha_52sa3 = LeituraOPCBit(self.opc, OPC_UA["SA"]["52SA3_SEM_FALHA"], 3, True)
        if not self.leitura_sem_falha_52sa3 and not self.dict["VOIP"]["52SA3_SEM_FALHA"]:
            logger.warning("Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciais. Favor verificar.")
            self.dict["VOIP"]["52SA3_SEM_FALHA"] = True
            self.acionar_voip = True
        elif self.leitura_sem_falha_52sa3 and self.dict["VOIP"]["52SA3_SEM_FALHA"]:
            self.dict["VOIP"]["52SA3_SEM_FALHA"] = False

        self.leitura_alarme_sistema_incendio_atuado = LeituraOPCBit(self.opc, OPC_UA["SA"]["SISTEMA_INCENDIO_ALARME_ATUADO"], 6)
        if self.leitura_alarme_sistema_incendio_atuado and not self.dict["VOIP"]["SISTEMA_INCENDIO_ALARME_ATUADO"]:
            logger.warning("O alarme do sistema de incêndio foi acionado. Favor verificar.")
            self.dict["VOIP"]["SISTEMA_INCENDIO_ALARME_ATUADO"] = True
            self.acionar_voip = True
        elif not self.leitura_alarme_sistema_incendio_atuado and self.dict["VOIP"]["SISTEMA_INCENDIO_ALARME_ATUADO"]:
            self.dict["VOIP"]["SISTEMA_INCENDIO_ALARME_ATUADO"] = False

        self.leitura_alarme_sistema_seguraca_atuado = LeituraOPCBit(self.opc, OPC_UA["SA"]["SISTEMA_SEGURANCA_ALARME_ATUADO"], 7)
        if self.leitura_alarme_sistema_seguraca_atuado and not self.dict["VOIP"]["SISTEMA_SEGURANCA_ALARME_ATUADO"]:
            logger.warning("O alarme do sistem de seguraça foi acionado. Favor verificar.")
            self.dict["VOIP"]["SISTEMA_SEGURANCA_ALARME_ATUADO"] = True
            self.acionar_voip = True
        elif not self.leitura_alarme_sistema_seguraca_atuado and self.dict["VOIP"]["SISTEMA_SEGURANCA_ALARME_ATUADO"]:
            self.dict["VOIP"]["SISTEMA_SEGURANCA_ALARME_ATUADO"] = False

        self.leitura_falha_partir_gmg = LeituraOPCBit(self.opc, OPC_UA["SA"]["GMG_FALHA_PARTIR"], 6)
        if self.leitura_falha_partir_gmg and not self.dict["VOIP"]["GMG_FALHA_PARTIR"]:
            logger.warning("Houve uma falha ao partir o Gerador Diesel. Favor verificar.")
            self.dict["VOIP"]["GMG_FALHA_PARTIR"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_partir_gmg and self.dict["VOIP"]["GMG_FALHA_PARTIR"]:
            self.dict["VOIP"]["GMG_FALHA_PARTIR"] = False

        self.leitura_falha_parar_gmg = LeituraOPCBit(self.opc, OPC_UA["SA"]["GMG_FALHA_PARAR"], 7)
        if self.leitura_falha_parar_gmg and not self.dict["VOIP"]["GMG_FALHA_PARAR"]:
            logger.warning("Houve uma falha ao parar o Gerador Diesel. Favor verificar.")
            self.dict["VOIP"]["GMG_FALHA_PARAR"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_parar_gmg and self.dict["VOIP"]["GMG_FALHA_PARAR"]:
            self.dict["VOIP"]["GMG_FALHA_PARAR"] = False

        self.leitura_operacao_manual_gmg = LeituraOPCBit(self.opc, OPC_UA["SA"]["GMG_OPERACAO_MANUAL"], 10)
        if self.leitura_operacao_manual_gmg and not self.dict["VOIP"]["GMG_OPERACAO_MANUAL"]:
            logger.warning("O Gerador Diesel saiu do modo remoto. Favor verificar.")
            self.dict["VOIP"]["GMG_OPERACAO_MANUAL"] = True
            self.acionar_voip = True
        elif not self.leitura_operacao_manual_gmg and self.dict["VOIP"]["GMG_OPERACAO_MANUAL"]:
            self.dict["VOIP"]["GMG_OPERACAO_MANUAL"] = False

        self.leitura_alarme_temp_enrolamento_te = LeituraOPCBit(self.opc, OPC_UA["SE"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"], 20)
        if self.leitura_alarme_temp_enrolamento_te and not self.dict["VOIP"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"]:
            logger.warning("A temperatura do enrolamento do transformador elevador está alta. Favor verificar.")
            self.dict["VOIP"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"] = True
            self.acionar_voip = True
        elif not self.leitura_alarme_temp_enrolamento_te and self.dict["VOIP"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"]:
            self.dict["VOIP"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"] = False

        self.leitura_alm_temp_enrolamento_te = LeituraOPCBit(self.opc, OPC_UA["SE"]["TE_ALM_TEMPERATURA_ENROLAMENTO"], 2)
        if self.leitura_alm_temp_enrolamento_te and not self.dict["VOIP"]["TE_ALM_TEMPERATURA_ENROLAMENTO"]:
            logger.warning("A temperatura do enrolamento do transformador elevador está alta. Favor verificar.")
            self.dict["VOIP"]["TE_ALM_TEMPERATURA_ENROLAMENTO"] = True
            self.acionar_voip = True
        elif not self.leitura_alm_temp_enrolamento_te and self.dict["VOIP"]["TE_ALM_TEMPERATURA_ENROLAMENTO"]:
            self.dict["VOIP"]["TE_ALM_TEMPERATURA_ENROLAMENTO"] = False

        self.leitura_alarme_temperatura_oleo_te = LeituraOPCBit(self.opc, OPC_UA["SE"]["TE_ALARME_TEMPERATURA_OLEO"], 18)
        if self.leitura_alarme_temperatura_oleo_te and not self.dict["VOIP"]["TE_ALARME_TEMPERATURA_OLEO"]:
            logger.warning("A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            self.dict["VOIP"]["TE_ALARME_TEMPERATURA_OLEO"] = True
            self.acionar_voip = True
        elif not self.leitura_alarme_temperatura_oleo_te and self.dict["VOIP"]["TE_ALARME_TEMPERATURA_OLEO"]:
            self.dict["VOIP"]["TE_ALARME_TEMPERATURA_OLEO"] = False

        self.leitura_alm_temperatura_oleo_te = LeituraOPCBit(self.opc, OPC_UA["SE"]["TE_ALM_TEMPERATURA_OLEO"], 1)
        if self.leitura_alm_temperatura_oleo_te and not self.dict["VOIP"]["TE_ALM_TEMPERATURA_OLEO"]:
            logger.warning("A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            self.dict["VOIP"]["TE_ALM_TEMPERATURA_OLEO"] = True
            self.acionar_voip = True
        elif not self.leitura_alm_temperatura_oleo_te and self.dict["VOIP"]["TE_ALM_TEMPERATURA_OLEO"]:
            self.dict["VOIP"]["TE_ALM_TEMPERATURA_OLEO"] = False

        self.leitura_nivel_oleo_muito_alto_te = LeituraOPCBit(self.opc, OPC_UA["SE"]["TE_NIVEL_OLEO_MUITO_ALTO"], 26)
        if self.leitura_nivel_oleo_muito_alto_te and not self.dict["VOIP"]["TE_NIVEL_OLEO_MUITO_ALTO"]:
            logger.warning("O nível do óleo do transformador elevador está muito alto. Favor verificar.")
            self.dict["VOIP"]["TE_NIVEL_OLEO_MUITO_ALTO"] = True
            self.acionar_voip = True
        elif not self.leitura_nivel_oleo_muito_alto_te and self.dict["VOIP"]["TE_NIVEL_OLEO_MUITO_ALTO"]:
            self.dict["VOIP"]["TE_NIVEL_OLEO_MUITO_ALTO"] = False

        self.leitura_nivel_oleo_muito_baixo_te = LeituraOPCBit(self.opc, OPC_UA["SE"]["TE_NIVEL_OLEO_MUITO_BAIXO"], 27)
        if self.leitura_nivel_oleo_muito_baixo_te and not self.dict["VOIP"]["TE_NIVEL_OLEO_MUITO_BAIXO"]:
            logger.warning("O nível de óleo do tranformador elevador está muito baixo. Favor verificar.")
            self.dict["VOIP"]["TE_NIVEL_OLEO_MUITO_BAIXO"] = True
            self.acionar_voip = True
        elif not self.leitura_nivel_oleo_muito_baixo_te and self.dict["VOIP"]["TE_NIVEL_OLEO_MUITO_BAIXO"]:
            self.dict["VOIP"]["TE_NIVEL_OLEO_MUITO_BAIXO"] = False
