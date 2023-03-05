import os
import json
import pytz
import logging
import threading
import subprocess

from time import sleep, time
from datetime import  datetime, timedelta
from pyModbusTCP.client import ModbusClient

from src.leituras import *
from src.conector import *
from src.constantes import *
from src.registradores import *
from src.condicionadores import *
from src.unidade_geracao import UnidadeDeGeracao

logger = logging.getLogger("__main__")

class Usina:
    def __init__(self, cfg=None, db=None, con=None):

        if not cfg:
            logger.warning("Um dicionário de configuração é necessário")
        else:
            config_file = os.path.join(os.path.dirname(__file__), "cfg.json")
            with open(config_file, "r") as file:
                self.cfg = json.load(file)

        if not db:
            logger.warning("Não foi possível estabelecer a conexão com o banco de dados")
        else:
            self.db = DatabaseConnector()

        if not con:
            logger.warning("Não foi possível iniciar as configuações de campo")
        else:
            self.con = FieldConnector(self.cfg)

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
        self.agendamentos_atrasados = 0
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

        self.ts_last_ping_tda = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        self.ts_ultima_tentativa_normalizacao = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

        self.clp_moa = ModbusClient(
            host=self.cfg["moa_slave_ip"],
            port=self.cfg["moa_slave_porta"],
            unit_id=1,
            timeout=0.5,
            auto_open=True,
            auto_close=True
        )
        self.clp_sa = ModbusClient(
            host=cfg["USN_slave_ip"],
            port=cfg["USN_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True
        )
        self.clp_tda = ModbusClient(
            host=cfg["TDA_slave_ip"],
            port=cfg["TDA_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True
        )

        self.tensao_rs = LeituraModbus(
            "Tensão R",
            self.clp_sa,
            SA["REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_AB"],
            1000,
            op=4,
        )
        self.tensao_st = LeituraModbus(
            "Tensão S",
            self.clp_sa,
            SA["REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_BC"],
            1000,
            op=4,
        )
        self.tensao_tr = LeituraModbus(
            "Tensão T",
            self.clp_sa,
            SA["REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_CA"],
            1000,
            op=4,
        )
        self.potencia_ativa_kW = LeituraModbus(
            "Potência MP/MR",
            self.clp_sa,
            SA["REG_SA_RetornosAnalogicos_MWR_PM_810_Potencia_Ativa"],
            1,
            op=4,
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
    def get_ugs(self) -> list:
        return self.ugs

    @property
    def get_time(self) -> object:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

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
    def pot_alvo_anterior(self) -> float:
        return self._potencia_alvo_anterior

    @pot_alvo_anterior.setter
    def pot_alvo_anterior(self, var):
        self._potencia_alvo_anterior = var

    def heartbeat(self) -> None:
        agora = self.get_time

        ano = int(agora.year)
        mes = int(agora.month)
        dia = int(agora.day)
        hor = int(agora.hour)
        mnt = int(agora.minute)
        seg = int(agora.second)
        mil = int(agora.microsecond / 1000)
        self.clp_moa.write_multiple_registers(0, [ano, mes, dia, hor, mnt, seg, mil])
        self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_STATUS"], [self.state_moa])
        self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_MODE"], [self.modo_autonomo])

        if self.modo_autonomo == 1:
            self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_EMERG"], [self.clp_emergencia_acionada])
            self.clp_moa.write_multiple_registers(self.cfg["REG_MOA_OUT_SETPOINT"], [int(self.ug1.setpoint + self.ug2.setpoint)])
            self.clp_moa.write_multiple_registers(self.cfg["REG_MOA_OUT_TARGET_LEVEL"], [int((self.cfg["nv_alvo"] - 820.9) * 1000)])

            if self.avisado_em_eletrica and not self.borda_in_emerg:
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG1"], [1],)
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG2"], [1],)
                self.borda_in_emerg = True

            elif not self.avisado_em_eletrica and self.borda_in_emerg:
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG1"], [0],)
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG2"], [0],)
                self.borda_in_emerg = False

            if self.clp_moa.read_coils(self.cfg["REG_MOA_IN_HABILITA_AUTO"])[0] == 1:
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_IN_HABILITA_AUTO"], [1])
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_IN_DESABILITA_AUTO"], [0])
                self.modo_autonomo = 1
            elif self.clp_moa.read_coils(self.cfg["REG_MOA_IN_DESABILITA_AUTO"])[0] == 1:
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_IN_HABILITA_AUTO"], [0])
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_IN_DESABILITA_AUTO"], [1])
                self.modo_autonomo = 0
                self.entrar_em_modo_manual()

            if self.clp_moa.read_coils(self.cfg["REG_MOA_OUT_BLOCK_UG1"])[0] == 1:
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG1"], [1])
            elif self.clp_moa.read_coils(self.cfg["REG_MOA_OUT_BLOCK_UG1"])[0] == 0:
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG1"], [0])

            if self.clp_moa.read_coils(self.cfg["REG_MOA_OUT_BLOCK_UG2"])[0] == 1:
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG2"], [1])
            elif self.clp_moa.read_coils(self.cfg["REG_MOA_OUT_BLOCK_UG2"])[0] == 0:
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG2"], [0])

        elif self.modo_autonomo == 0:
            self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_EMERG"], [0])
            self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_TARGET_LEVEL"], [0])
            self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_SETPOINT"], [0])
            self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG1"], [0])
            self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG2"], [0])

    def ler_valores(self) ->  None:
        if not ping(self.cfg["TDA_slave_ip"]):
            self.TDA_Offline = True
            if self.TDA_Offline and not self.borda_ping:
                self.borda_ping = True
                logger.warning("CLP TDA não respondeu a tentativa de comunicação!")

        elif ping(self.cfg["TDA_slave_ip"]) and self.borda_ping:
            logger.info("Comunicação com o CLP TDA reestabelecida.")
            self.borda_ping = False
            self.TDA_Offline = False
        
        if not ping(self.cfg["USN_slave_ip"]):
            logger.warning("CLP SA não respondeu a tentativa de comunicação!")

        if not ping(self.cfg["UG1_slave_ip"]):
            logger.warning("CLP UG1 não respondeu a tentativa de comunicação!")

        if not ping(self.cfg["UG2_slave_ip"]):
            logger.warning("CLP UG2 não respondeu a tentativa de comunicação!")

        if not self.TDA_Offline:
            self.nv_montante_recente = self.nv_montante

            self.erro_nv_anterior = self.erro_nv
            self.erro_nv = self.nv_montante_recente - self.cfg["nv_alvo"]

        parametros = self.db.get_parametros_usina()

        self.db_emergencia_acionada = int(parametros["emergencia_acionada"])

        logger.debug(f"Modo autonomo que o banco respondeu: {int(parametros['modo_autonomo'])}")
        self.modo_autonomo = int(parametros["modo_autonomo"])

        if not self.modo_de_escolha_das_ugs == int(parametros["modo_de_escolha_das_ugs"]):
            self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
            logger.info(f"O modo de prioridade das ugs foi alterado (#{self.modo_de_escolha_das_ugs}).")

        if self.clp_moa.read_coils(self.cfg["REG_MOA_IN_EMERG"])[0] == 1 and not self.avisado_em_eletrica:
            self.avisado_em_eletrica = True
            for ug in self.ugs: ug.ler_condicionadores = True

        elif self.clp_moa.read_coils(self.cfg["REG_MOA_IN_EMERG"])[0] == 0 and self.avisado_em_eletrica:
            self.avisado_em_eletrica = False
            for ug in self.ugs: ug.ler_condicionadores = False

        self.ug1.ler_condicionadores = True if self.clp_moa.read_coils(self.cfg["REG_MOA_IN_EMERG_UG1"])[0] == 1 else False

        self.ug2.ler_condicionadores = True if self.clp_moa.read_coils(self.cfg["REG_MOA_IN_EMERG_UG2"])[0] == 1 else False

        if self.clp_moa.read_coils(self.cfg["REG_MOA_IN_HABILITA_AUTO"])[0] == 1:
            self.clp_moa.write_single_coil(self.cfg["REG_MOA_IN_HABILITA_AUTO"], [1])
            self.clp_moa.write_single_coil(self.cfg["REG_MOA_IN_DESABILITA_AUTO"], [0])
            self.modo_autonomo = 1

        if self.clp_moa.read_coils(self.cfg["REG_MOA_IN_DESABILITA_AUTO"])[0] == 1:
            self.clp_moa.write_single_coil(self.cfg["REG_MOA_IN_HABILITA_AUTO"], [0])
            self.clp_moa.write_single_coil(self.cfg["REG_MOA_IN_DESABILITA_AUTO"], [1])
            self.modo_autonomo = 0
            self.entrar_em_modo_manual()

        self.heartbeat()
        self.atualizar_cfg(parametros)
        self.atualizar_limites_operacao(parametros)

    def escrever_valores(self) -> None:
        try:
            valores = [
                self.get_time.strftime("%Y-%m-%d %H:%M:%S"),  # timestamp
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
        except Exception as e:
            logger.exception(e)

    def atualizar_cfg(self, parametros) -> None:
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

            except KeyError as e:
                logger.exception(e)

    def acionar_emergencia(self):
        self.con.acionar_emergencia()
        self.clp_emergencia_acionada = 1

    def normalizar_emergencia(self):
        logger.debug("Normalizando (e verificações)")
        logger.debug(f"Ultima tentativa: {self.ts_ultima_tentativa_normalizacao}. Tensão na linha: RS {self.tensao_rs.valor:2.1f}kV ST{self.tensao_st.valor:2.1f}kV TR{self.tensao_tr.valor:2.1f}kV")

        if not(self.cfg["TENSAO_LINHA_BAIXA"] < self.tensao_rs.valor < self.cfg["TENSAO_LINHA_ALTA"] \
            and self.cfg["TENSAO_LINHA_BAIXA"] < self.tensao_st.valor < self.cfg["TENSAO_LINHA_ALTA"] \
            and self.cfg["TENSAO_LINHA_BAIXA"] < self.tensao_tr.valor < self.cfg["TENSAO_LINHA_ALTA"]):
            self.tensao_ok = False
            return False

        elif self.deve_normalizar_forcado or (self.deve_tentar_normalizar and (self.get_time - self.ts_ultima_tentativa_normalizacao).seconds >= 60 * self.tentativas_de_normalizar):
            self.tentativas_de_normalizar += 1
            self.ts_ultima_tentativa_normalizacao = self.get_time
            logger.info("Normalizando Usina")
            self.con.TDA_Offline = True if self.TDA_Offline else False
            self.con.normalizar_emergencia()
            self.clp_emergencia_acionada = 0
            logger.info("Normalizando Banco de Dados")
            self.db.update_remove_emergencia()
            self.db_emergencia_acionada = 0
            return True

        else:
            logger.debug("A normalização foi executada menos de 1 minuto atrás.")
            self.tensao_ok = True
            return False

    def aguardar_tensao(self, delay):
        logger.warning("Iniciando o timer para a normalização da tensão na linha")
        while time() <= time() + delay:
            sleep(time() - (time() - 15))
            if (self.cfg["TENSAO_LINHA_BAIXA"] < self.tensao_rs.valor < self.cfg["TENSAO_LINHA_ALTA"] \
                and self.cfg["TENSAO_LINHA_BAIXA"] < self.tensao_st.valor < self.cfg["TENSAO_LINHA_ALTA"] \
                and self.cfg["TENSAO_LINHA_BAIXA"] < self.tensao_tr.valor < self.cfg["TENSAO_LINHA_ALTA"]):
                logger.info("Tensão na linha reestabelecida.")
                self.timer_tensao = True
                return True
        logger.warning("Não foi possível reestabelecer a tensão na linha")
        self.timer_tensao = False
        return False

    def get_agendamentos_pendentes(self):
        agendamentos_pendentes = []
        agendamentos = self.db.get_agendamentos_pendentes()

        for agendamento in agendamentos:
            ag = list(agendamento)
            ag[1] = ag[1] - timedelta(0, 60 * 60 * 3)
            agendamentos_pendentes.append(ag)

        return agendamentos_pendentes

    def verificar_agendamentos(self):
        agora = self.get_time
        agendamentos = self.get_agendamentos_pendentes()

        limite_entre_agendamentos_iguais = 300
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
        logger.debug(f"Data: {agendamentos[i-1][1].strftime('%Y-%m-%d %H:%M:%S')}  Criado por: {agendamentos[i-1][6]}  Comando: {agendamentos[i-1][3]}")

        if len(agendamentos) == 0:
            return True

        self.agendamentos_atrasados = 0

        for agendamento in agendamentos:
            if agora > agendamento[1]:
                segundos_adiantados = 0
                segundos_passados = (agora - agendamento[1]).seconds
                logger.debug(segundos_passados)
            else:
                segundos_adiantados = (agendamento[1] - agora).seconds
                segundos_passados = 0

            if segundos_passados > 240:
                logger.warning(f"Agendamento #{agendamento[0]} Atrasado! ({agendamento[3]}).")
                self.agendamentos_atrasados += 1

            if segundos_passados > 300 or self.agendamentos_atrasados > 3:
                logger.info("Os agendamentos estão muito atrasados!")
                if agendamento[3] == AGENDAMENTO_INDISPONIBILIZAR:
                    logger.warning("Acionando emergência!")
                    self.acionar_emergencia()
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    return False
                elif agendamento[3] == AGENDAMENTO_ALTERAR_NV_ALVO or AGENDAMENTO_ALTERAR_POT_LIMITE_TODAS_AS_UGS or AGENDAMENTO_BAIXAR_POT_UGS_MINIMO or AGENDAMENTO_NORMALIZAR_POT_UGS_MINIMO or AGENDAMENTO_AGUARDAR_RESERVATORIO or AGENDAMENTO_NORMALIZAR_ESPERA_RESERVATORIO:
                    logger.info("Não foi possível executar o agendamento! Favor re-agendar")
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    return False
                elif agendamento[3] in AGENDAMENTO_LISTA_BLOQUEIO_UG1:
                    logger.info("Indisponibilizando UG1")
                    self.ug1.forcar_estado_indisponivel()
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    return False
                elif agendamento[3] in AGENDAMENTO_LISTA_BLOQUEIO_UG2:
                    logger.info("Indisponibilizando UG2")
                    self.ug2.forcar_estado_indisponivel()
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    return False
                else:
                    logger.info("Agendamento não encontrado! Retomando operação...")
                    return False

            if segundos_adiantados <= 60 and not bool(agendamento[4]):
                logger.info(f"Executando gendamento: {agendamento[0]} - Comando: {agendamento[3]} - Data: {agendamento[9]}.")

                if self.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_autmoatico"]:
                    obs = "Este agendamento não tem efeito com o módulo em modo autônomo. Executado sem realizar nenhuma ação"
                    logger.warning(obs)
                    self.db.update_agendamento(agendamento[0], True, obs)
                    return True

                if not self.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_manual"]:
                    obs = "Este agendamento não tem efeito com o módulo em modo manual. Executado sem realizar nenhuma ação"
                    logger.warning(obs)
                    self.db.update_agendamento(agendamento[0], True, obs)
                    return True

                if agendamento[3] == AGENDAMENTO_INDISPONIBILIZAR:
                    logger.info("Indisponibilizando a usina (comando via agendamento).")
                    for ug in self.ugs: ug.forcar_estado_indisponivel()
                    while (not self.ugs[0].etapa_atual == UNIDADE_PARADA and not self.ugs[1].etapa_atual == UNIDADE_PARADA):
                        self.ler_valores()
                        logger.debug("Indisponibilizando Usina... \n(freezing for 10 seconds)")
                        sleep(10)
                    self.acionar_emergencia()
                    logger.debug("Emergência pressionada após indizponibilização agendada mudando para modo manual para evitar normalização automática.")
                    self.entrar_em_modo_manual()

                if agendamento[3] == AGENDAMENTO_ALTERAR_NV_ALVO:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                    except Exception as e:
                        logger.info(f"Valor inválido no comando #{agendamento[0]} ({agendamento[3]} é inválido).")
                    self.cfg["nv_alvo"] = novo

                if agendamento[3] == AGENDAMENTO_BAIXAR_POT_UGS_MINIMO:
                    try:
                        self.cfg["pot_maxima_ug1"] = self.cfg["pot_minima"]
                        self.cfg["pot_maxima_ug2"] = self.cfg["pot_minima"]
                        for ug in self.ugs:
                            if ug.etapa_atual == UNIDADE_PARADA or ug.etapa_alvo == UNIDADE_PARADA:
                                logger.debug(f"A UG{ug.id} já está no estado parada/parando.")
                            else:
                                logger.debug(f"Enviando o setpoint mínimo ({self.cfg['pot_minima']}) para a UG{ug.id}")
                                ug.enviar_setpoint(self.cfg["pot_minima"])

                    except Exception as e:
                        logger.info(f"Traceback: {repr(e)}")

                if agendamento[3] == AGENDAMENTO_NORMALIZAR_POT_UGS_MINIMO:
                    try:
                        self.cfg["pot_maxima_ug1"] = self.cfg["pot_maxima_ug"]
                        self.cfg["pot_maxima_ug2"] = self.cfg["pot_maxima_ug"]
                        for ug in self.ugs: ug.enviar_setpoint(self.cfg["pot_maxima_ug"])

                    except Exception as e:
                        logger.debug(f"Traceback: {repr(e)}")

                if agendamento[3] == AGENDAMENTO_AGUARDAR_RESERVATORIO:
                    logger.debug("Ativando estado de espera de nível do reservatório")
                    self.aguardando_reservatorio = 1

                if agendamento[3] == AGENDAMENTO_NORMALIZAR_ESPERA_RESERVATORIO:
                    logger.debug("Desativando estado de espera de nível do reservatório")
                    self.aguardando_reservatorio = 0

                if agendamento[3] == AGENDAMENTO_UG1_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug1"] = novo
                        self.ug1.pot_disponivel = novo
                    except Exception as e:
                        logger.info(f"Valor inválido no comando #{agendamento[0]} ({agendamento[3]} é inválido)")

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_MANUAL:
                    self.ug1.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_DISPONIVEL:
                    self.ug1.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug1.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_RESTRITO:
                    self.ug1.forcar_estado_restrito()

                if agendamento[3] == AGENDAMENTO_UG1_TEMPO_ESPERA_RESTRITO:
                    self.ug1.norma_agendada = True
                    novo = agendamento[5].split(":")
                    tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                    self.ug1.tempo_normalizar = tempo

                if agendamento[3] == AGENDAMENTO_UG2_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug2"] = novo
                        self.ug2.pot_disponivel = novo
                    except Exception as e:
                        logger.info(f"Valor inválido no comando #{agendamento[0]} ({agendamento[3]} é inválido)")

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_MANUAL:
                    self.ug2.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_DISPONIVEL:
                    self.ug2.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug2.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_RESTRITO:
                    self.ug2.forcar_estado_restrito()
                
                if agendamento[3] == AGENDAMENTO_UG2_TEMPO_ESPERA_RESTRITO:
                    self.ug2.norma_agendada = True
                    novo = agendamento[5].split(":")
                    tempo = (int(novo[0]) * 3600) + (int(novo[1]) * 60)
                    self.ug2.tempo_normalizar = tempo

                if agendamento[3] == AGENDAMENTO_ALTERAR_POT_LIMITE_TODAS_AS_UGS:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug1"] = novo
                        self.ug1.pot_disponivel = novo
                        self.cfg["pot_maxima_ug2"] = novo
                        self.ug2.pot_disponivel = novo
                    except Exception as e:
                        logger.info(f"Valor inválido no comando #{agendamento[0]} ({agendamento[3]} é inválido)")

                self.db.update_agendamento(int(agendamento[0]), 1)
                logger.info(f"O comando #{agendamento[0]} - {agendamento[5]} foi executado.")
                self.con.reconhecer_emergencia()
                self.escrever_valores()

    def distribuir_potencia(self, pot_alvo):
        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs: ug.setpoint = 0
            return 0

        logger.debug(f"Pot alvo = {pot_alvo}")

        pot_medidor = self.potencia_ativa_kW.valor
        logger.debug(f"Pot no medidor = {pot_medidor}")

        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])

        pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

        try:
            if pot_medidor > self.cfg["pot_maxima_alvo"]:
                pot_alvo = self.pot_alvo_anterior * (1 - ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))
        except TypeError as e:
            logger.info("A comunicação com os MFs falharam.")

        self.pot_alvo_anterior = pot_alvo

        logger.debug(f"Pot alvo após ajuste medidor = {pot_alvo}")

        ugs = self.lista_de_ugs_disponiveis()
        self.pot_disp = 0
        self.ajuste_manual = 0

        logger.debug("lista_de_ugs_disponiveis:")
        for ug in ugs:
            logger.debug(f"UG{ug.id}")
            self.pot_disp += ug.cfg[f"pot_maxima_ug{ugs[0].id}"]
            if ug.manual:
                self.ajuste_manual += min(max(0, ug.leitura_potencia), 0)

        if ugs is None:
            return False
        elif len(ugs) == 0:
            return False

        logger.debug(f"Distribuindo {pot_alvo - self.ajuste_manual}")

        sp = (pot_alvo - self.ajuste_manual) / self.cfg["pot_maxima_usina"]

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
                for ug in ugs: ug.setpoint = 0

        elif len(ugs) == 1:
            if self.__split1 or self.__split2:
                logger.debug("Split 1B")
                sp = sp * 2 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo

            else:
                for ug in ugs: ug.setpoint = 0

        for ug in self.ugs: logger.debug(f"UG{ug.id} SP:{ug.setpoint}")

        return pot_alvo

    def lista_de_ugs_disponiveis(self):
        ls = []
        for ug in self.ugs:
            if ug.disponivel and not ug.etapa_atual == UNIDADE_PARANDO:
                ls.append(ug)

        if self.modo_de_escolha_das_ugs == MODO_ESCOLHA_MANUAL:
            ls = sorted(ls, key=lambda y: (-1 * y.leitura_potencia.valor, -1 * y.setpoint, y.prioridade,))
        else:
            ls = sorted(ls, key=lambda y: (y.leitura_horimetro.valor, -1 * y.leitura_potencia.valor, -1 * y.setpoint,))

        return ls

    def controle_normal(self):
        logger.debug("-------------------------------------------------")

        self.controle_p = self.cfg["kp"] * self.erro_nv
        self.controle_i = max(min((self.cfg["ki"] * self.erro_nv) + self.controle_i, 0.8), 0)
        self.controle_d = self.cfg["kd"] * (self.erro_nv - self.erro_nv_anterior)
        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))

        logger.debug(f"Alvo: {self.cfg['nv_alvo']:0.3f}, Recente: {self.nv_montante_recente:0.3f}")
        logger.debug(f"PID: {saida_pid:0.3f} <-- P:{self.controle_p:0.3f} + I:{self.controle_i:0.3f} + D:{self.controle_d:0.3f}; ERRO={self.erro_nv}")

        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)

        logger.debug(f"IE: {self.controle_ie:0.3f}")

        if self.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if self.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"],), self.cfg["pot_minima"],)
        
        logger.debug(f"Pot alvo: {pot_alvo:0.3f}")
        logger.debug(f"Nv alvo: {self.cfg['nv_alvo']:0.3f}")

        try:
            self.db.insert_debug(
                self.get_time.timestamp(),
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

    def entrar_em_modo_manual(self):
        self.modo_autonomo = 0
        self.db.update_modo_manual()

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
        self.condicionadores.append(CondicionadorBase(self.leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup) )

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
            logger.warning("O sensor de TRIP do Grupo Motor Gerador foi acionado, favor verificar.")

        if LeituraModbusCoil("Alarme GMG", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_GMG_Alarme"]).valor != 0:
            logger.warning("O alarme do Grupo Motor Gerador foi acionado, favor verificar.")

        if LeituraModbusCoil("Sensor Operação GMG", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_GMG_Operacao"]).valor != 0:
            logger.warning("O sensor de operação do Grupo Motor Gerador foi acionado, favor verificar.")

        if LeituraModbusCoil("Baixo Combustível GMG", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_GMG_BaixoComb"]).valor != 0:
            logger.warning("O sensor de de combustível baixo do Grupo Motor Gerador foi acionado, favor reabastercer.")

        if LeituraModbusCoil("Falha Acionamento GMG", self.clp_sa, SA["REG_SA_RetornosDigitais_MXR_SA_GMG_FalhaAcion"]).valor != 0:
            logger.warning("O sensor do Grupo Motor Gerador identificou uma falha no acionamento, favor verificar.")

        if LeituraModbusCoil("TRIP Disjuntor 52E QLCF", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QLCF_Disj52ETrip"]).valor != 0:
            logger.warning("O Disjuntor do Gerador Diesel de Emergência QLCF identificou um sinal de TRIP, favor verificar.")

        if LeituraModbusCoil("TRIP Agrupamento QLCF", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QLCF_TripDisjAgrup"]).valor != 0:
            logger.warning("O sensor do Disjuntor de Agrupamento QLCF identificou um sinal de trip, favor verificar.")

        if LeituraModbusCoil("Falha Acionamento Bomba 1", self.clp_sa, SA["REG_SA_RetornosDigitais_MXR_BbaDren1_FalhaAcion"]).valor != 0:
            logger.warning("O sensor da Bomba de Drenagem 1 identificou uma falha no acionamento, favor verificar.")

        if LeituraModbusCoil("Falha Acionamento Bomba 2", self.clp_sa, SA["REG_SA_RetornosDigitais_MXR_BbaDren2_FalhaAcion"]).valor != 0:
            logger.warning("O sensor da Bomba de Drenagem 2 identificou uma falha no acionamento, favor verificar.")

        if LeituraModbusCoil("Falha Acionamento Bomba 3", self.clp_sa, SA["REG_SA_RetornosDigitais_MXR_BbaDren3_FalhaAcion"]).valor != 0:
            logger.warning("O sensor da Bomba de Drenagem 3 identificou uma falha no acionamento, favor verificar.")

        if LeituraModbusCoil("Sensor Barramento Geral QCAP", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_SubtensaoBarraGeral"]).valor != 0:
            logger.warning("O sensor de Subtensão do Barramento Geral QCAP foi acionado, favor verificar.")

        leitura_FalhaComunSETDA = LeituraModbusCoil("Falha Comunicação CLPs SA e TDA", self.clp_sa, SA["REG_SA_RetornosDigitais_MXR_FalhaComunSETDA"])
        if leitura_FalhaComunSETDA.valor != 0 and not VOIP["TDA_FalhaComum"]:
            logger.warning("Houve uma falha de comunicação com o CLP da Subestação e o CLP da Tomada da Água, favor verificar")
            VOIP["TDA_FalhaComum"] = True
            self.acionar_voip = True
        elif leitura_FalhaComunSETDA.valor == 0 and VOIP["TDA_FalhaComum"]:
            VOIP["TDA_FalhaComum"] = False

        leitura_QCAP_Disj52EFechado = LeituraModbusCoil("Disjuntor 52E QLCF Fechado", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52EFechado"])
        if leitura_QCAP_Disj52EFechado.valor == 1 and not VOIP["Disj_GDE_QCAP_Fechado"]:
            logger.warning("O Disjuntor do Gerador Diesel de Emergência QLCF foi fechado.")
            VOIP["Disj_GDE_QCAP_Fechado"] = True
            self.acionar_voip = True
        elif leitura_QCAP_Disj52EFechado.valor == 0 and VOIP["Disj_GDE_QCAP_Fechado"]:
            VOIP["Disj_GDE_QCAP_Fechado"] = False

        leitura_QCADE_BombasDng_Auto = LeituraModbusCoil("Bombas Modo Remoto", self.clp_sa, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_BombasDng_Auto"])
        if leitura_QCADE_BombasDng_Auto.valor == 0 and not VOIP["BombasDngRemoto"]:
            logger.warning("O poço de drenagem da Usina saiu do modo remoto, favor verificar.")
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
