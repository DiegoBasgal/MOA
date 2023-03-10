import pytz
import logging
import subprocess

from time import sleep, time
from datetime import  datetime
from pyModbusTCP.client import ModbusClient

from leituras import *
from conector import *
from ocorrencias import *
from dicionarios.reg import *
from dicionarios.const import *
from unidade_geracao import UnidadeDeGeracao

logger = logging.getLogger("__main__")

class Usina:
    def __init__(
            self,
            shared_dict=None,
            con: FieldConnector=None,
            db: DatabaseConnector=None,
            ugs: list([UnidadeDeGeracao])=None,
            ocorrencias: Ocorrencias=None,
        ):

        if not shared_dict:
            logger.warning("[USN] Não foi possível carregar o dicionário compartilhado.")
            raise ValueError
        else:
            self.dict = shared_dict

        if not db:
            logger.warning("[USN] Não foi possível estabelecer a conexão com o banco de dados.")
            raise ConnectionError
        else:
            self.db = db

        if not con:
            logger.warning("[USN] Não foi possível estabelecer a conexão com as leituras de campo.")
            raise ConnectionError
        else:
            self.con = con

        if not ocorrencias:
            logger.warning("[USN] Não foi possível obter a instância da classe de ocorrências")
            raise ReferenceError
        else:
            self.ocorrencias = ocorrencias

        if not ugs:
            logger.warning("[USN] Não foi possível estabelecer a conexão com as leituras de campo.")
            raise ValueError
        else:
            self.ugs = ugs
            self.ug1 = ugs[0]
            self.ug2 = ugs[1]
            CondicionadorBase.ugs = ugs

        # Variáveis protegidas
        self._potencia_alvo_anterior = -1

        # Variáveis públicas
        self.erro_nv = 0
        self.pot_disp = 0
        self.state_moa = 0
        self.controle_p = 0
        self.controle_i = 0
        self.controle_d = 0
        self.ug_operando = 0
        self.modo_autonomo = 1
        self.erro_nv_anterior = 0
        self.nv_montante_recente = 0
        self.nv_montante_anterior = 0
        self.db_emergencia_acionada = 0
        self.clp_emergencia_acionada = 0
        self.modo_de_escolha_das_ugs = 0
        self.aguardando_reservatorio = 0
        self.tentativas_de_normalizar = 0

        self.tensao_ok = True
        self.borda_ping = False
        self.borda_tensao = None
        self.timer_tensao = False
        self.acionar_voip = False
        self.borda_in_emerg = False
        self.avisado_em_eletrica = False
        self.deve_tentar_normalizar = True
        self.deve_normalizar_forcado = False

        self.ts_nv = []
        self.condicionadores = []
        self.nv_montante_recentes = []
        self.nv_montante_anteriores = []
        self.condicionadores_essenciais = []

        self.ts_last_ping_tda = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        self.ts_ultima_tentativa_normalizacao = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

        self.clp_moa = ModbusClient(
            host=self.dict.IP["MOA_slave_ip"],
            port=self.dict.IP["MOA_slave_porta"],
            unit_id=1,
            timeout=0.5,
            auto_open=True,
            auto_close=True
        )
        self.clp_sa = ModbusClient(
            host=self.dict.IP["USN_slave_ip"],
            port=self.dict.IP["USN_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True
        )
        self.clp_tda = ModbusClient(
            host=self.dict.IP["TDA_slave_ip"],
            port=self.dict.IP["TDA_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True
        )

        for ug in self.ugs:
            if ug.etapa_atual == UNIDADE_SINCRONIZADA:
                self.ug_operando += 1

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False

        if self.dict.CFG["saida_ie_inicial"] == "auto":
            self.controle_ie = (self.ug1.leitura_potencia.valor + self.ug2.leitura_potencia.valor) / self.dict.CFG["pot_maxima_alvo"]
        else:
            self.controle_ie = self.dict.CFG["saida_ie_inicial"]

        self.controle_i = self.controle_ie

        self.ler_valores()
        self.escrever_valores()
        self.normalizar_emergencia()

    @property
    def nv_montante(self) -> float:
        try:
            return LeituraModbus(
                "Nível Montante",
                self.clp_tda,
                TDA["REG_TDA_NivelMaisCasasAntes"],
                1 / 10000,
                819.2,
                op=4,
            ).valor
        except Exception as e:
            logger.exception(f"[USN] Houve um erro na leitura de nível montante. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")
            return 0

    @property
    def tensao_rs(self) -> float:
        try:
            return LeituraModbus(
                "Tensão R",
                self.clp_sa,
                SA["REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_AB"],
                1000,
                op=4,
            ).valor
        except Exception as e:
            logger.exception(f"[USN] Houve um erro na leitura de Tensão RS. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")
            return 0

    @property
    def tensao_st(self) -> float:
        try:
            return LeituraModbus(
                "Tensão S",
                self.clp_sa,
                SA["REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_BC"],
                1000,
                op=4,
            ).valor
        except Exception as e:
            logger.exception(f"[USN] Houve um erro na leitura de Tensão RS. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")
            return 0

    @property
    def tensao_tr(self) -> float:
        try:
            return LeituraModbus(
                "Tensão T",
                self.clp_sa,
                SA["REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_CA"],
                1000,
                op=4,
            ).valor
        except Exception as e:
            logger.exception(f"[USN] Houve um erro na leitura de Tensão TR. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")
            return 0

    @property
    def potencia_ativa_kW(self) -> int:
        try:
            return LeituraModbus(
                "Potência MP/MR",
                self.clp_sa,
                SA["REG_SA_RetornosAnalogicos_MWR_PM_810_Potencia_Ativa"],
                1,
                op=4,
            ).valor
        except Exception as e:
            logger.exception(f"[USN] Houve um erro na leitura de potência dos medidores MP/MR. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")
            return 0

    @property
    def get_modo_autonomo(self) -> int:
        return self.modo_autonomo

    @property
    def pot_alvo_anterior(self) -> float:
        return self._potencia_alvo_anterior

    @pot_alvo_anterior.setter
    def pot_alvo_anterior(self, var):
        self._potencia_alvo_anterior = var

    def get_time(self) -> object:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def entrar_em_modo_manual(self) -> None:
        self.modo_autonomo = 0
        self.db.update_modo_manual()

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
            self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_STATUS"], [self.state_moa])
            self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_MODE"], [self.modo_autonomo])

            if self.modo_autonomo == 1:
                self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_EMERG"], [self.clp_emergencia_acionada])
                self.clp_moa.write_multiple_registers(MOA["REG_MOA_OUT_SETPOINT"], [int(self.ug1.setpoint + self.ug2.setpoint)])
                self.clp_moa.write_multiple_registers(MOA["REG_MOA_OUT_TARGET_LEVEL"], [int((self.dict.CFG["nv_alvo"] - 820.9) * 1000)])

                if self.avisado_em_eletrica and not self.borda_in_emerg:
                    self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_BLOCK_UG1"], [1],)
                    self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_BLOCK_UG2"], [1],)
                    self.borda_in_emerg = True

                elif not self.avisado_em_eletrica and self.borda_in_emerg:
                    self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_BLOCK_UG1"], [0],)
                    self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_BLOCK_UG2"], [0],)
                    self.borda_in_emerg = False

                if self.clp_moa.read_coils(MOA["REG_MOA_IN_HABILITA_AUTO"])[0] == 1:
                    self.clp_moa.write_single_coil(MOA["REG_MOA_IN_HABILITA_AUTO"], [1])
                    self.clp_moa.write_single_coil(MOA["REG_MOA_IN_DESABILITA_AUTO"], [0])
                    self.modo_autonomo = 1
                elif self.clp_moa.read_coils(MOA["REG_MOA_IN_DESABILITA_AUTO"])[0] == 1:
                    self.clp_moa.write_single_coil(MOA["REG_MOA_IN_HABILITA_AUTO"], [0])
                    self.clp_moa.write_single_coil(MOA["REG_MOA_IN_DESABILITA_AUTO"], [1])
                    self.modo_autonomo = 0
                    self.entrar_em_modo_manual()

                if self.clp_moa.read_coils(MOA["REG_MOA_OUT_BLOCK_UG1"])[0] == 1:
                    self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_BLOCK_UG1"], [1])
                elif self.clp_moa.read_coils(MOA["REG_MOA_OUT_BLOCK_UG1"])[0] == 0:
                    self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_BLOCK_UG1"], [0])

                if self.clp_moa.read_coils(MOA["REG_MOA_OUT_BLOCK_UG2"])[0] == 1:
                    self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_BLOCK_UG2"], [1])
                elif self.clp_moa.read_coils(MOA["REG_MOA_OUT_BLOCK_UG2"])[0] == 0:
                    self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_BLOCK_UG2"], [0])

            elif self.modo_autonomo == 0:
                self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_EMERG"], [0])
                self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_TARGET_LEVEL"], [0])
                self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_SETPOINT"], [0])
                self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_BLOCK_UG1"], [0])
                self.clp_moa.write_single_coil(MOA["REG_MOA_OUT_BLOCK_UG2"], [0])
        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def ler_valores(self) -> None:
        self.ping_clps()
        try:
            if self.clp_moa.read_coils(MOA["REG_MOA_IN_EMERG"])[0] == 1 and not self.avisado_em_eletrica:
                self.avisado_em_eletrica = True
                self.ocorrencias.verificar_condicionadores_ug()

            elif self.clp_moa.read_coils(MOA["REG_MOA_IN_EMERG"])[0] == 0 and self.avisado_em_eletrica:
                self.avisado_em_eletrica = False

            if self.clp_moa.read_coils(MOA["REG_MOA_IN_EMERG_UG1"])[0] == 1 or self.clp_moa.read_coils(MOA["REG_MOA_IN_EMERG_UG2"])[0] == 1:
                self.ocorrencias.verificar_condicionadores_ug()

            if self.clp_moa.read_coils(MOA["REG_MOA_IN_HABILITA_AUTO"])[0] == 1:
                self.clp_moa.write_single_coil(MOA["REG_MOA_IN_HABILITA_AUTO"], [1])
                self.clp_moa.write_single_coil(MOA["REG_MOA_IN_DESABILITA_AUTO"], [0])
                self.modo_autonomo = 1

            if self.clp_moa.read_coils(MOA["REG_MOA_IN_DESABILITA_AUTO"])[0] == 1:
                self.clp_moa.write_single_coil(MOA["REG_MOA_IN_HABILITA_AUTO"], [0])
                self.clp_moa.write_single_coil(MOA["REG_MOA_IN_DESABILITA_AUTO"], [1])
                self.modo_autonomo = 0
                self.entrar_em_modo_manual()
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
            valores = [
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),  # timestamp
                1 if self.aguardando_reservatorio else 0,  # aguardando_reservatorio
                True,  # DEPRECATED clp_online
                self.nv_montante if not self.dict.CFG["tda_offline"] else 0,  # nv_montante
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
            ]
            self.db.update_valores_usina(valores)
        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao inserir os valores no banco. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def atualizar_montante_recente(self) -> None:
        if not self.dict.GLB["tda_offline"]:
            self.nv_montante_recente = self.nv_montante
            self.erro_nv_anterior = self.erro_nv
            self.erro_nv = self.nv_montante_recente - self.dict.CFG["nv_alvo"]

    def atualizar_parametros_db(self, parametros) -> None:
        try:
            self.db_emergencia_acionada = int(parametros["emergencia_acionada"])
            logger.debug("[USN] Emergência acionada.")

            self.modo_autonomo = int(parametros["modo_autonomo"])
            logger.debug(f"[USN] Modo autonomo que o banco respondeu: {int(parametros['modo_autonomo'])}")

            if not self.modo_de_escolha_das_ugs == int(parametros["modo_de_escolha_das_ugs"]):
                self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
                logger.info(f"[USN] O modo de prioridade das ugs foi alterado (#{self.modo_de_escolha_das_ugs}).")
        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao ler e atualizar os parâmetros do Banco de Dados. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def atualizar_cfg(self, parametros) -> None:
        try:
            self.dict.CFG["TDA_slave_ip"] = parametros["clp_tda_ip"]
            self.dict.CFG["kp"] = float(parametros["kp"])
            self.dict.CFG["ki"] = float(parametros["ki"])
            self.dict.CFG["kd"] = float(parametros["kd"])
            self.dict.CFG["kie"] = float(parametros["kie"])
            self.dict.CFG["cx_kp"] = float(parametros["cx_kp"])
            self.dict.CFG["cx_ki"] = float(parametros["cx_ki"])
            self.dict.CFG["cx_kie"] = float(parametros["cx_kie"])
            self.dict.CFG["press_cx_alvo"] = float(parametros["press_cx_alvo"])
            self.dict.CFG["nv_alvo"] = float(parametros["nv_alvo"])
            self.dict.CFG["nv_minimo"] = float(parametros["nv_minimo"])
            self.dict.CFG["pot_maxima_alvo"] = float(parametros["pot_nominal"])
            self.dict.CFG["pot_maxima_ug"] = float(parametros["pot_nominal_ug"])
            self.dict.CFG["pot_maxima_usina"] = float(parametros["pot_nominal_ug"]) * 2

            for ug in self.ugs:
                ug.prioridade = int(parametros[f"ug{ug.id}_prioridade"])

        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao atualizar o arquivo de configuração \"cfg.json\". Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def atualizar_limites_condicionadores(self, parametros) -> None:
        for ug in self.ugs:
            try:
                ug.prioridade = int(parametros[f"ug{ug.id}_prioridade"])
                ug.condicionador_temperatura_fase_r_ug.valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{ug.id}"])
                ug.condicionador_temperatura_fase_r_ug.valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{ug.id}"])
                ug.condicionador_temperatura_fase_s_ug.valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{ug.id}"])
                ug.condicionador_temperatura_fase_s_ug.valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{ug.id}"])
                ug.condicionador_temperatura_fase_t_ug.valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{ug.id}"])
                ug.condicionador_temperatura_fase_t_ug.valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{ug.id}"])
                ug.condicionador_temperatura_nucleo_gerador_1_ug.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_1_ug{ug.id}"])
                ug.condicionador_temperatura_nucleo_gerador_1_ug.valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_1_ug{ug.id}"])
                ug.condicionador_temperatura_nucleo_gerador_2_ug.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_2_ug{ug.id}"])
                ug.condicionador_temperatura_nucleo_gerador_2_ug.valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_2_ug{ug.id}"])
                ug.condicionador_temperatura_nucleo_gerador_3_ug.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_3_ug{ug.id}"])
                ug.condicionador_temperatura_nucleo_gerador_3_ug.valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_3_ug{ug.id}"])
                ug.condicionador_temperatura_mancal_casq_rad_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_casq_rad_ug{ug.id}"])
                ug.condicionador_temperatura_mancal_casq_rad_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_casq_rad_ug{ug.id}"])
                ug.condicionador_temperatura_mancal_casq_comb_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_casq_comb_ug{ug.id}"])
                ug.condicionador_temperatura_mancal_casq_comb_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_casq_comb_ug{ug.id}"])
                ug.condicionador_temperatura_mancal_escora_comb_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_escora_comb_ug{ug.id}"])
                ug.condicionador_temperatura_mancal_escora_comb_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_escora_comb_ug{ug.id}"])
                ug.condicionador_caixa_espiral_ug.valor_base = float(parametros[f"alerta_caixa_espiral_ug{ug.id}"])
                ug.condicionador_caixa_espiral_ug.valor_limite = float(parametros[f"limite_caixa_espiral_ug{ug.id}"])

            except Exception as e:
                logger.exception(f"[USN] Houve um erro ao atualizar os limites de temperaturas dos condicionadores. Exception: \"{repr(e)}\"")
                logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def acionar_emergencia(self) -> None:
        self.con.acionar_emergencia()
        self.clp_emergencia_acionada = 1

    def normalizar_emergencia(self) -> bool:
        logger.debug("[USN] Normalizando...")
        logger.debug(f"[USN] Última tentativa: {self.ts_ultima_tentativa_normalizacao}. Tensão na linha: RS->{self.tensao_rs:2.1f}kV / ST->{self.tensao_st:2.1f}kV / TR->{self.tensao_tr:2.1f}kV")

        if not self.verificar_tensao():
            return False

        elif self.deve_normalizar_forcado or (self.deve_tentar_normalizar and (self.get_time() - self.ts_ultima_tentativa_normalizacao).seconds >= 60 * self.tentativas_de_normalizar):
            self.tentativas_de_normalizar += 1
            self.ts_ultima_tentativa_normalizacao = self.get_time()
            self.db_emergencia_acionada = 0
            self.clp_emergencia_acionada = 0
            self.con.normalizar_emergencia()
            self.db.update_remove_emergencia()
            return True

        else:
            logger.debug("[USN] A normalização foi executada menos de 1 minuto atrás.")
            return False

    def verificar_tensao(self) -> bool:
        try:
            if (self.dict.CFG["TENSAO_LINHA_BAIXA"] < self.tensao_rs < self.dict.CFG["TENSAO_LINHA_ALTA"]) \
                and (self.dict.CFG["TENSAO_LINHA_BAIXA"] < self.tensao_st < self.dict.CFG["TENSAO_LINHA_ALTA"]) \
                and (self.dict.CFG["TENSAO_LINHA_BAIXA"] < self.tensao_tr < self.dict.CFG["TENSAO_LINHA_ALTA"]):
                self.tensao_ok = True
                return True
            else:
                self.tensao_ok = False
                logger.warning("[USN] Tensão da linha fora do limite.")
                return False
        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao realizar a verificação da tensão na linha. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    def aguardar_tensao(self) -> bool:
        if not self.tensao_ok and self.borda_tensao is None:
            self.borda_tensao = True
            logger.debug("[USN] Iniciando o timer para a normalização da tensão na linha.")
            Thread(target=lambda: self.timeout_tensao(600)).start()

        elif self.timer_tensao and self.borda_tensao:
            logger.info("[USN] Tensão na linha reestabelecida.")
            self.borda_tensao = None
            self.tensao_ok = True
            return True

        elif not self.timer_tensao and self.borda_tensao:
            logger.critical("[USN] Não foi possível reestabelecer a tensão na linha. Acionando emergência")
            self.borda_tensao = None
            self.tensao_ok = False
            return False

        else:
            logger.debug("[USN] A tensão na linha ainda está fora.")

    def timeout_tensao(self, delay) -> None:
        while time() <= time() + delay:
            if self.verificar_tensao():
                self.timer_tensao = True
                return
            sleep(time() - (time() - 15))
        self.timer_tensao = False

    def distribuir_potencia(self, pot_alvo) -> float:
        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs: ug.setpoint = 0
            return 0

        pot_medidor = self.potencia_ativa_kW
        logger.debug(f"[USN] Potência no medidor = {pot_medidor:0.3f}")

        pot_aux = self.dict.CFG["pot_maxima_alvo"] - (self.dict.CFG["pot_maxima_usina"] - self.dict.CFG["pot_maxima_alvo"])
        pot_medidor = max(pot_aux, min(pot_medidor, self.dict.CFG["pot_maxima_usina"]))

        try:
            if pot_medidor > self.dict.CFG["pot_maxima_alvo"]:
                pot_alvo = self.pot_alvo_anterior * (1 - ((pot_medidor - self.dict.CFG["pot_maxima_alvo"]) / self.dict.CFG["pot_maxima_alvo"]))
        except TypeError as te:
            logger.exception(f"[USN] A comunicação com os MFs falharam. Exception: \"{repr(te)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

        self.pot_alvo_anterior = pot_alvo

        logger.debug(f"[USN] Pot alvo pós ajuste: {pot_alvo:0.3f}")

        ugs = self.lista_de_ugs_disponiveis()
        self.pot_disp = 0
        self.ajuste_manual = 0

        for ug in ugs:
            logger.debug(f"[USN] UG{ug.id}")
            self.pot_disp += ug.cfg[f"pot_maxima_ug{ugs[0].id}"]
            if ug.manual:
                self.ajuste_manual += min(max(0, ug.leitura_potencia), 0)

        if ugs is None:
            return False
        elif len(ugs) == 0:
            return False

        logger.debug(f"[USN] Distribuindo: {pot_alvo - self.ajuste_manual:0.3f}")

        sp = (pot_alvo - self.ajuste_manual) / self.dict.CFG["pot_maxima_usina"]

        self.__split1 = True if sp > (0) else self.__split1
        self.__split2 = (True if sp > (0.5 + self.dict.CFG["margem_pot_critica"]) else self.__split2)

        self.__split2 = False if sp < (0.5) else self.__split2
        self.__split1 = False if sp < (self.dict.CFG["pot_minima"] / self.dict.CFG["pot_maxima_usina"]) else self.__split1

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

            else:
                for ug in ugs: ug.setpoint = 0

        elif len(ugs) == 1:
            if self.__split1 or self.__split2:
                logger.debug("[USN] Split 1B")
                sp = sp * 2 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo

            else:
                for ug in ugs: ug.setpoint = 0

        return pot_alvo

    def lista_de_ugs_disponiveis(self) ->  list:
        ls = []
        for ug in self.ugs:
            if ug.disponivel and not ug.etapa_atual == UNIDADE_PARANDO:
                ls.append(ug)

        if self.modo_de_escolha_das_ugs == MODO_ESCOLHA_MANUAL:
            ls = sorted(ls, key=lambda y: (-1 * y.leitura_potencia.valor, -1 * y.setpoint, y.prioridade,))
            logger.debug("")
            logger.debug("[USN] UGs disponíveis em ordem (prioridade):")
        else:
            ls = sorted(ls, key=lambda y: (y.leitura_horimetro.valor, -1 * y.leitura_potencia.valor, -1 * y.setpoint,))
            logger.debug("")
            logger.debug("[USN] UGs disponíveis em ordem (horas-máquina):")

        return ls

    def controle_normal(self) -> None:
        logger.debug("-------------------------------------------------------------------------")

        self.controle_p = self.dict.CFG["kp"] * self.erro_nv
        self.controle_i = max(min((self.dict.CFG["ki"] * self.erro_nv) + self.controle_i, 0.8), 0)
        self.controle_d = self.dict.CFG["kd"] * (self.erro_nv - self.erro_nv_anterior)
        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))

        logger.debug(f"[USN] NÍVEL -> Leitura: {self.nv_montante_recente:0.3f}; Alvo: {self.dict.CFG['nv_alvo']:0.3f}")
        logger.debug(f"[USN] PID -> {saida_pid:0.3f} P:{self.controle_p:0.3f} + I:{self.controle_i:0.3f} + D:{self.controle_d:0.3f}; ERRO={self.erro_nv}")

        self.controle_ie = max(min(saida_pid + self.controle_ie * self.dict.CFG["kie"], 1), 0)

        logger.debug(f"[USN] IE: {self.controle_ie:0.3f}")
        logger.debug("")

        if self.nv_montante_recente >= (self.dict.CFG["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if self.nv_montante_recente <= (self.dict.CFG["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        pot_alvo = max(min(round(self.dict.CFG["pot_maxima_usina"] * self.controle_ie, 5), self.dict.CFG["pot_maxima_usina"],), self.dict.CFG["pot_minima"],)

        logger.debug(f"[USN] Potência alvo: {pot_alvo:0.3f}")

        try:
            self.db.insert_debug(
                self.get_time().timestamp(),
                self.dict.CFG["kp"],
                self.dict.CFG["ki"],
                self.dict.CFG["kd"],
                self.dict.CFG["kie"],
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
                self.ug1.setpoint,
                self.ug1.leitura_potencia.valor,
                self.ug2.setpoint,
                self.ug2.leitura_potencia.valor,
                self.nv_montante_recente,
                self.erro_nv,
                self.modo_autonomo,
                self.dict.CFG["cx_kp"],
                self.dict.CFG["cx_ki"],
                self.dict.CFG["cx_kie"],
                0,
            )
        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao inserir dados DEBUG do controle de potência normal no banco. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

        pot_alvo = self.distribuir_potencia(pot_alvo)

    def ping(self, host) -> bool:
        ping = False
        for i in range(2):
            ping = ping or (subprocess.call(["ping", "-c", "1", "-w", "1", host], stdout=subprocess.PIPE) == 0)
            if not ping:
                pass
        return ping

    def ping_clps(self) -> None:
        try:
            if not self.ping(self.dict.IP["TDA_slave_ip"]):
                self.dict.CFG["tda_offline"] = True
                if self.dict.CFG["tda_offline"] and not self.borda_ping:
                    self.borda_ping = True
                    logger.warning("[USN] CLP TDA não respondeu a tentativa de comunicação!")
            elif self.ping(self.dict.IP["TDA_slave_ip"]) and self.borda_ping:
                logger.info("[USN] Comunicação com o CLP TDA reestabelecida.")
                self.borda_ping = False
                self.dict.GLB["tda_offline"] = False

            if not self.ping(self.dict.IP["USN_slave_ip"]):
                logger.warning("[USN] CLP SA não respondeu a tentativa de comunicação!")
            if not self.ping(self.dict.IP["UG1_slave_ip"]):
                logger.warning("[USN] CLP UG1 não respondeu a tentativa de comunicação!")
            if not self.ping(self.dict.IP["UG2_slave_ip"]):
                logger.warning("[USN] CLP UG2 não respondeu a tentativa de comunicação!")
        except Exception as e:
            logger.exception(f"[USN] Houve um erro ao executar o ping dos CLPs da usina. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")

    
