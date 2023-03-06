import os
import json
import pytz
import logging
import threading
import subprocess

from time import sleep, time
from datetime import  datetime
from pyModbusTCP.client import ModbusClient

from src.reg import *
from src.const import *
from src.leituras import *
from src.conector import *
from src.condicionadores import *
from src.unidade_geracao import UnidadeDeGeracao

logger = logging.getLogger("__main__")

class Usina:
    def __init__(self, cfg=None, db=None, con=None):

        if not cfg:
            logger.warning("[USN] Um dicionário de configuração é necessário")
        else:
            self.cfg = cfg

        if not db:
            logger.warning("[USN] Não foi possível estabelecer a conexão com o banco de dados")
        else:
            self.db = db

        if not con:
            logger.warning("[USN] Não foi possível iniciar as configuações de campo")
        else:
            self.con = con

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
        self.timer_tensao = None
        self.TDA_Offline = False
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

        self.ug1 = UnidadeDeGeracao(1, cfg=self.cfg)
        self.ug2 = UnidadeDeGeracao(2, cfg=self.cfg)
        self.ugs = [self.ug1, self.ug2]
        CondicionadorBase.set_ugs(self.ugs)

        self.ts_last_ping_tda = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        self.ts_ultima_tentativa_normalizacao = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

        self.clp_moa = ModbusClient(
            host=CFG["moa_slave_ip"],
            port=CFG["moa_slave_porta"],
            unit_id=1,
            timeout=0.5,
            auto_open=True,
            auto_close=True
        )
        self.clp_sa = ModbusClient(
            host=CFG["USN_slave_ip"],
            port=CFG["USN_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True
        )
        self.clp_tda = ModbusClient(
            host=CFG["TDA_slave_ip"],
            port=CFG["TDA_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True
        )
        # threading.Thread(target=lambda: self.leitura_condicionadores()).start()

        for ug in self.ugs:
            if ug.etapa_atual == UNIDADE_SINCRONIZADA:
                self.ug_operando += 1

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False

        if self.cfg["saida_ie_inicial"] == "auto":
            self.controle_ie = (self.ug1.leitura_potencia.valor + self.ug2.leitura_potencia.valor) / self.cfg["pot_maxima_alvo"]
        else:
            self.controle_ie = self.cfg["saida_ie_inicial"]

        self.controle_i = self.controle_ie

        parametros = self.db.get_parametros_usina()
        self.atualizar_limites_operacao(parametros)
        self.escrever_valores()

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
        except Exception:
            logger.exception(f"[USN] Houve um erro na leitura de nível montante.\nTraceback: {traceback.print_stack}")
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
        except Exception:
            logger.exception(f"[USN] Houve um erro na leitura de Tensão RS.\nTraceback: {traceback.print_stack}")
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
        except Exception:
            logger.exception(f"[USN] Houve um erro na leitura de Tensão RS.\nTraceback: {traceback.print_stack}")
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
        except Exception:
            logger.exception(f"[USN] Houve um erro na leitura de Tensão TR.\nTraceback: {traceback.print_stack}")
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
        except Exception:
            logger.exception(f"[USN] Houve um erro na leitura de potência dos medidores MP/MR.\nTraceback: {traceback.print_stack}")
            return 0

    @property
    def get_ugs(self) -> list:
        return self.ugs

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
                self.clp_moa.write_multiple_registers(MOA["REG_MOA_OUT_TARGET_LEVEL"], [int((self.cfg["nv_alvo"] - 820.9) * 1000)])

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
        except Exception:
            logger.exception(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA.\nTraceback: {traceback.print_stack}")

    def ler_valores(self) ->  None:
        self.ping_clps()
        try:
            if self.clp_moa.read_coils(MOA["REG_MOA_IN_EMERG"])[0] == 1 and not self.avisado_em_eletrica:
                self.avisado_em_eletrica = True
                for ug in self.ugs: ug.ler_condicionadores = True

            elif self.clp_moa.read_coils(MOA["REG_MOA_IN_EMERG"])[0] == 0 and self.avisado_em_eletrica:
                self.avisado_em_eletrica = False
                for ug in self.ugs: ug.ler_condicionadores = False

            self.ug1.ler_condicionadores = True if self.clp_moa.read_coils(MOA["REG_MOA_IN_EMERG_UG1"])[0] == 1 else False

            self.ug2.ler_condicionadores = True if self.clp_moa.read_coils(MOA["REG_MOA_IN_EMERG_UG2"])[0] == 1 else False

            if self.clp_moa.read_coils(MOA["REG_MOA_IN_HABILITA_AUTO"])[0] == 1:
                self.clp_moa.write_single_coil(MOA["REG_MOA_IN_HABILITA_AUTO"], [1])
                self.clp_moa.write_single_coil(MOA["REG_MOA_IN_DESABILITA_AUTO"], [0])
                self.modo_autonomo = 1

            if self.clp_moa.read_coils(MOA["REG_MOA_IN_DESABILITA_AUTO"])[0] == 1:
                self.clp_moa.write_single_coil(MOA["REG_MOA_IN_HABILITA_AUTO"], [0])
                self.clp_moa.write_single_coil(MOA["REG_MOA_IN_DESABILITA_AUTO"], [1])
                self.modo_autonomo = 0
                self.entrar_em_modo_manual()
        except Exception:
            logger.exception(f"[USN] Houve um erro ao tentar ler valores modbus no CLP MOA.\nTraceback: {traceback.print_stack}")

        self.heartbeat()
        self.atualizar_montante_recente()

        parametros = self.db.get_parametros_usina()
        self.atualizar_cfg(parametros)
        self.atualizar_parametros_db(parametros)
        self.atualizar_limites_operacao(parametros)

    def escrever_valores(self) -> None:
        try:
            valores = [
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),  # timestamp
                1 if self.aguardando_reservatorio else 0,  # aguardando_reservatorio
                True,  # DEPRECATED clp_online
                self.nv_montante if not self.TDA_Offline else 0,  # nv_montante
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
        except Exception:
            logger.exception(f"[USN] Houve um erro ao inserir os valores no banco.\n Traceback: {traceback.print_stack}")

    def ping_clps(self) -> None:
        try:
            if not ping(CFG["TDA_slave_ip"]):
                self.TDA_Offline = True
                if self.TDA_Offline and not self.borda_ping:
                    self.borda_ping = True
                    logger.warning("[USN] CLP TDA não respondeu a tentativa de comunicação!")
            elif ping(CFG["TDA_slave_ip"]) and self.borda_ping:
                logger.info("[USN] Comunicação com o CLP TDA reestabelecida.")
                self.borda_ping = False
                self.TDA_Offline = False

            if not ping(CFG["USN_slave_ip"]):
                logger.warning("[USN] CLP SA não respondeu a tentativa de comunicação!")
            if not ping(CFG["UG1_slave_ip"]):
                logger.warning("[USN] CLP UG1 não respondeu a tentativa de comunicação!")
            if not ping(CFG["UG2_slave_ip"]):
                logger.warning("[USN] CLP UG2 não respondeu a tentativa de comunicação!")
        except Exception:
            logger.exception(f"[USN] Houve um erro ao executar o ping dos CLPs da usina.\nTraceback: {traceback.print_stack}")

    def atualizar_montante_recente(self) -> None:
        if not self.TDA_Offline:
            self.nv_montante_recente = self.nv_montante
            self.erro_nv_anterior = self.erro_nv
            self.erro_nv = self.nv_montante_recente - self.cfg["nv_alvo"]

    def atualizar_cfg(self, parametros) -> None:
        try:
            self.cfg["TDA_slave_ip"] = parametros["clp_tda_ip"]
            self.cfg["kp"] = float(parametros["kp"])
            self.cfg["ki"] = float(parametros["ki"])
            self.cfg["kd"] = float(parametros["kd"])
            self.cfg["kie"] = float(parametros["kie"])
            self.cfg["nv_alvo"] = float(parametros["nv_alvo"])
            self.cfg["nv_minimo"] = float(parametros["nv_minimo"])
            self.cfg["pot_maxima_alvo"] = float(parametros["pot_nominal"])
            self.cfg["pot_maxima_ug"] = float(parametros["pot_nominal_ug"])
            self.cfg["pot_maxima_usina"] = float(parametros["pot_nominal_ug"]) * 2
            self.cfg["cx_kp"] = float(parametros["cx_kp"])
            self.cfg["cx_ki"] = float(parametros["cx_ki"])
            self.cfg["cx_kie"] = float(parametros["cx_kie"])
            self.cfg["press_cx_alvo"] = float(parametros["press_cx_alvo"])
        except Exception:
            logger.exception(f"[USN] Houve um erro ao atualizar o arquivo de configuração \"cfg.json\".\nTraceback: {traceback.print_stack}")

    def atualizar_parametros_db(self, parametros) -> None:
        try:
            self.db_emergencia_acionada = int(parametros["emergencia_acionada"])
            logger.debug("[USN] Emergência acionada.")

            self.modo_autonomo = int(parametros["modo_autonomo"])
            logger.debug(f"[USN] Modo autonomo que o banco respondeu: {int(parametros['modo_autonomo'])}")

            if not self.modo_de_escolha_das_ugs == int(parametros["modo_de_escolha_das_ugs"]):
                self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
                logger.info(f"[USN] O modo de prioridade das ugs foi alterado (#{self.modo_de_escolha_das_ugs}).")
        except Exception:
            logger.exception(f"[USN] Houve um erro ao ler e atualizar os parâmetros do Banco de Dados.\nTraceback: {traceback.print_stack}")

    def atualizar_limites_operacao(self, parametros) -> None:
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
            except Exception:
                logger.exception(f"[USN] Houve um erro ao tentar atualizar parâmetros de base e limite dos condicionadores.\nTraceback: {traceback.print_stack}")

    def acionar_emergencia(self) -> None:
        self.con.acionar_emergencia()
        self.clp_emergencia_acionada = 1

    def normalizar_emergencia(self) -> bool:
        logger.debug("[USN] Normalizando...")
        logger.debug(f"[USN] Última tentativa: {self.ts_ultima_tentativa_normalizacao}. Tensão na linha: RS->{self.tensao_rs:2.1f}kV / ST->{self.tensao_st:2.1f}kV / TR->{self.tensao_tr:2.1f}kV")
        if not self.verificar_tensao():
            self.tensao_ok = False
            return False

        elif self.deve_normalizar_forcado or (self.deve_tentar_normalizar and (self.get_time() - self.ts_ultima_tentativa_normalizacao).seconds >= 60 * self.tentativas_de_normalizar):
            self.tentativas_de_normalizar += 1
            self.ts_ultima_tentativa_normalizacao = self.get_time()
            self.con.TDA_Offline = True if self.TDA_Offline else False
            self.db_emergencia_acionada = 0
            self.clp_emergencia_acionada = 0
            self.con.normalizar_emergencia()
            self.db.update_remove_emergencia()
            return True

        else:
            logger.debug("[USN] A normalização foi executada menos de 1 minuto atrás.")
            self.tensao_ok = True
            return False

    def verificar_tensao(self) -> bool:
        if (self.cfg["TENSAO_LINHA_BAIXA"] < self.tensao_rs < self.cfg["TENSAO_LINHA_ALTA"]) \
            and (self.cfg["TENSAO_LINHA_BAIXA"] < self.tensao_st < self.cfg["TENSAO_LINHA_ALTA"]) \
            and (self.cfg["TENSAO_LINHA_BAIXA"] < self.tensao_tr < self.cfg["TENSAO_LINHA_ALTA"]):
            return True
        else:
            return False

    def aguardar_tensao(self, delay) -> bool:
        logger.warning("[USN] Iniciando o timer para a normalização da tensão na linha")
        while time() <= time() + delay:
            if self.verificar_tensao():
                logger.info("[USN] Tensão na linha reestabelecida.")
                self.timer_tensao = True
                return True
            sleep(time() - (time() - 15))
        logger.warning("[USN] Não foi possível reestabelecer a tensão na linha.")
        self.timer_tensao = False
        return False

    def distribuir_potencia(self, pot_alvo) -> float:
        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs: ug.setpoint = 0
            return 0

        pot_medidor = self.potencia_ativa_kW
        logger.debug(f"[USN] Potência no medidor = {pot_medidor:0.3f}")

        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])

        pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

        try:
            if pot_medidor > self.cfg["pot_maxima_alvo"]:
                pot_alvo = self.pot_alvo_anterior * (1 - ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))
        except TypeError:
            logger.exception("[USN] A comunicação com os MFs falharam.")

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

        sp = (pot_alvo - self.ajuste_manual) / self.cfg["pot_maxima_usina"]

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

        self.controle_p = self.cfg["kp"] * self.erro_nv
        self.controle_i = max(min((self.cfg["ki"] * self.erro_nv) + self.controle_i, 0.8), 0)
        self.controle_d = self.cfg["kd"] * (self.erro_nv - self.erro_nv_anterior)
        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))

        logger.debug(f"[USN] NÍVEL -> Leitura: {self.nv_montante_recente:0.3f}; Alvo: {self.cfg['nv_alvo']:0.3f}")
        logger.debug(f"[USN] PID -> {saida_pid:0.3f} P:{self.controle_p:0.3f} + I:{self.controle_i:0.3f} + D:{self.controle_d:0.3f}; ERRO={self.erro_nv}")

        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)

        logger.debug(f"[USN] IE: {self.controle_ie:0.3f}")
        logger.debug("")

        if self.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if self.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"],), self.cfg["pot_minima"],)
        
        logger.debug(f"[USN] Potência alvo: {pot_alvo:0.3f}")

        try:
            self.db.insert_debug(
                self.get_time().timestamp(),
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
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
                self.cfg["cx_kp"],
                self.cfg["cx_ki"],
                self.cfg["cx_kie"],
                0,
            )
        except Exception as e:
            logger.exception(e)

        pot_alvo = self.distribuir_potencia(pot_alvo)

    def leitura_condicionadores(self):
        leitura_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA = LeituraModbusCoil("EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA.descr, DEVE_NORMALIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA))

        leitura_EntradasDigitais_MXI_SA_SEL787_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_SEL787_Trip", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_SEL787_Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_SEL787_Trip.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_SEL787_Trip))

        leitura_EntradasDigitais_MXI_SA_SEL311_Trip = LeituraModbusCoil( "EntradasDigitais_MXI_SA_SEL311_Trip", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_SEL311_Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_SEL311_Trip.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_SEL311_Trip))

        leitura_EntradasDigitais_MXI_SA_MRU3_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRU3_Trip", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_MRU3_Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_MRU3_Trip.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_MRU3_Trip))

        leitura_EntradasDigitais_MXI_SA_MRL1_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRL1_Trip", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_MRL1_Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_MRL1_Trip.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_MRL1_Trip))

        leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip) )

        if not self.TDA_Offline:
            leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETrip = LeituraModbusCoil("EntradasDigitais_MXI_TDA_QcataDisj52ETrip", self.clp_tda, TDA["REG_TDA_EntradasDigitais_MXI_QcataDisj52ETrip"], )
            self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETrip.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETrip))

            leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai = LeituraModbusCoil("EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai", self.clp_tda, TDA["REG_TDA_EntradasDigitais_MXI_QcataDisj52ETripDisjSai"], )
            self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai))

            leitura_EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA = LeituraModbusCoil("EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA", self.clp_tda, TDA["REG_TDA_EntradasDigitais_MXI_QcataDisj52EFalha380VCA"], )
            self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA))

        leitura_EntradasDigitais_MXI_SA_MRU3_Falha = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRU3_Falha", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_MRU3_Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_MRU3_Falha.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_MRU3_Falha))

        leitura_EntradasDigitais_MXI_SA_SEL787_FalhaInterna = LeituraModbusCoil( "EntradasDigitais_MXI_SA_SEL787_FalhaInterna", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_SEL787_FalhaInterna"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_SEL787_FalhaInterna.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_SEL787_FalhaInterna) )

        leitura_EntradasDigitais_MXI_SA_SEL311_Falha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_SEL311_Falha", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_SEL311_Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_SEL311_Falha.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_SEL311_Falha) )

        leitura_EntradasDigitais_MXI_SA_CTE_Falta125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CTE_Falta125Vcc", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_CTE_Falta125Vcc"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CTE_Falta125Vcc.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CTE_Falta125Vcc) )

        leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeTempOleo", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento = ( LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeDesligamento", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento) )

        leitura_EntradasDigitais_MXI_SA_TE_Falha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_Falha", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_TE_Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_Falha.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_Falha) )

        leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsProt = LeituraModbusCoil( "EntradasDigitais_MXI_SA_FalhaDisjTPsProt", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsProt"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsProt.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsProt) )

        leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr = LeituraModbusCoil( "EntradasDigitais_MXI_SA_FalhaDisjTPsSincr", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr) )

        leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CSA1_Secc_Aberta", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta) )

        leitura_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CSA1_FusivelQueimado", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado) )

        leitura_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc) )

        leitura_EntradasDigitais_MXI_SA_QCADE_Nivel4 = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_Nivel4", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_Nivel4"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCADE_Nivel4.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCADE_Nivel4) )

        leitura_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto) )

        leitura_EntradasDigitais_MXI_SA_QCADE_Falha220VCA = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_Falha220VCA", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_Falha220VCA"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCADE_Falha220VCA.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCADE_Falha220VCA) )

        leitura_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCCP_Disj72ETrip", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip) )

        leitura_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCCP_Falta125Vcc", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc) )

        leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup) )

        leitura_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_Falta125Vcc", self.clclp_sap, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc) )

        leitura_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup) )

        leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha) )

        leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_Disj52EFalha", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha) )

        leitura_EntradasDigitais_MXI_SA_GMG_DisjFechado = LeituraModbusCoil( "EntradasDigitais_MXI_SA_GMG_DisjFechado", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_GMG_DisjFechado"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_GMG_DisjFechado.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_GMG_DisjFechado) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets = LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets", self.clp_sa, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets"], )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00", self.clp_sa, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01", self.clp_sa, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02", self.clp_sa, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03", self.clp_sa, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04", self.clp_sa, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05", self.clp_sa, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06", self.clp_sa, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07", self.clp_sa, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07) )

        leitura_RetornosDigitais_MXR_DJ1_FalhaInt = LeituraModbusCoil( "RetornosDigitais_MXR_DJ1_FalhaInt", self.clp_sa, SA["REG_SA_RetornosDigitais_MXR_DJ1_FalhaInt"], )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosDigitais_MXR_DJ1_FalhaInt.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_DJ1_FalhaInt) )

        leitura_RetornosDigitais_MXR_CLP_Falha = LeituraModbusCoil("RetornosDigitais_MXR_CLP_Falha", self.clp_sa, SA["REG_SA_RetornosDigitais_MXR_CLP_Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosDigitais_MXR_CLP_Falha.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_CLP_Falha) )

        return True

    def leituras_por_hora(self):
        if LeituraModbusCoil("TRIP GMG",self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_GMG_Trip"]).valor != 0:
            logger.warning("[USN] O sensor de TRIP do Grupo Motor Gerador foi acionado, favor verificar.")

        if LeituraModbusCoil("Alarme GMG", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_GMG_Alarme"]).valor != 0:
            logger.warning("[USN] O alarme do Grupo Motor Gerador foi acionado, favor verificar.")

        if LeituraModbusCoil("Sensor Operação GMG", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_GMG_Operacao"]).valor != 0:
            logger.warning("[USN] O sensor de operação do Grupo Motor Gerador foi acionado, favor verificar.")

        if LeituraModbusCoil("Baixo Combustível GMG", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_GMG_BaixoComb"]).valor != 0:
            logger.warning("[USN] O sensor de de combustível baixo do Grupo Motor Gerador foi acionado, favor reabastercer.")

        if LeituraModbusCoil("Falha Acionamento GMG", self.clp_sa, SA["REG_SA_RetornosDigitais_MXR_SA_GMG_FalhaAcion"]).valor != 0:
            logger.warning("[USN] O sensor do Grupo Motor Gerador identificou uma falha no acionamento, favor verificar.")

        if LeituraModbusCoil("TRIP Disjuntor 52E QLCF", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QLCF_Disj52ETrip"]).valor != 0:
            logger.warning("[USN] O Disjuntor do Gerador Diesel de Emergência QLCF identificou um sinal de TRIP, favor verificar.")

        if LeituraModbusCoil("TRIP Agrupamento QLCF", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QLCF_TripDisjAgrup"]).valor != 0:
            logger.warning("[USN] O sensor do Disjuntor de Agrupamento QLCF identificou um sinal de trip, favor verificar.")

        if LeituraModbusCoil("Falha Acionamento Bomba 1", self.clp_sa, SA["REG_SA_RetornosDigitais_MXR_BbaDren1_FalhaAcion"]).valor != 0:
            logger.warning("[USN] O sensor da Bomba de Drenagem 1 identificou uma falha no acionamento, favor verificar.")

        if LeituraModbusCoil("Falha Acionamento Bomba 2", self.clp_sa, SA["REG_SA_RetornosDigitais_MXR_BbaDren2_FalhaAcion"]).valor != 0:
            logger.warning("[USN] O sensor da Bomba de Drenagem 2 identificou uma falha no acionamento, favor verificar.")

        if LeituraModbusCoil("Falha Acionamento Bomba 3", self.clp_sa, SA["REG_SA_RetornosDigitais_MXR_BbaDren3_FalhaAcion"]).valor != 0:
            logger.warning("[USN] O sensor da Bomba de Drenagem 3 identificou uma falha no acionamento, favor verificar.")

        if LeituraModbusCoil("Sensor Barramento Geral QCAP", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_SubtensaoBarraGeral"]).valor != 0:
            logger.warning("[USN] O sensor de Subtensão do Barramento Geral QCAP foi acionado, favor verificar.")

        leitura_FalhaComunSETDA = LeituraModbusCoil("Falha Comunicação CLPs SA e TDA", self.clp_sa, SA["REG_SA_RetornosDigitais_MXR_FalhaComunSETDA"])
        if leitura_FalhaComunSETDA.valor != 0 and not VOIP["TDA_FalhaComum"]:
            logger.warning("[USN] Houve uma falha de comunicação com o CLP da Subestação e o CLP da Tomada da Água, favor verificar")
            VOIP["TDA_FalhaComum"] = True
            self.acionar_voip = True
        elif leitura_FalhaComunSETDA.valor == 0 and VOIP["TDA_FalhaComum"]:
            VOIP["TDA_FalhaComum"] = False

        leitura_QCAP_Disj52EFechado = LeituraModbusCoil("Disjuntor 52E QLCF Fechado", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52EFechado"])
        if leitura_QCAP_Disj52EFechado.valor == 1 and not VOIP["Disj_GDE_QCAP_Fechado"]:
            logger.warning("[USN] O Disjuntor do Gerador Diesel de Emergência QLCF foi fechado.")
            VOIP["Disj_GDE_QCAP_Fechado"] = True
            self.acionar_voip = True
        elif leitura_QCAP_Disj52EFechado.valor == 0 and VOIP["Disj_GDE_QCAP_Fechado"]:
            VOIP["Disj_GDE_QCAP_Fechado"] = False

        leitura_QCADE_BombasDng_Auto = LeituraModbusCoil("Bombas Modo Remoto", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_BombasDng_Auto"])
        if leitura_QCADE_BombasDng_Auto.valor == 0 and not VOIP["BombasDngRemoto"]:
            logger.warning("[USN] O poço de drenagem da Usina saiu do modo remoto, favor verificar.")
            VOIP["BombasDngRemoto"] = True
            self.acionar_voip = True
        elif leitura_QCADE_BombasDng_Auto.valor == 1 and VOIP["BombasDngRemoto"]:
            VOIP["BombasDngRemoto"] = False

        return True

def ping(host):
    ping = False
    for i in range(2):
        ping = ping or (subprocess.call(["ping", "-c", "1", "-w", "1", host], stdout=subprocess.PIPE) == 0)
        if not ping:
            pass
    return ping
