import pytz
import logging
import threading
import subprocess

from opcua import Client
from time import sleep, time
from pyModbusTCP.server import DataBank
from pyModbusTCP.client import ModbusClient
from datetime import  datetime, timedelta

from src.VAR_REG import *
from src.Condicionadores import *
from src.UG1 import UnidadeDeGeracao1
from src.UG2 import UnidadeDeGeracao2
from src.Conector import Database, FieldConnector
from src.Leituras import LeituraOPC, LeiturasUSN, LeituraOPCBit

logger = logging.getLogger("__main__")

class Usina:
    def __init__(self, cfg=None, db=None, con=None, leituras=None):

        if not cfg or not db:
            raise ValueError
        else:
            self.cfg = cfg
            self.db = db

        if con:
            self.con = con
        else:
            self.con = FieldConnector(self.cfg)

        if leituras:
            self.leituras = leituras
        else:
            self.leituras = LeiturasUSN(self.cfg)

        self.state_moa = 1

        # Inicializa Objs da usina
        self.ug1 = UnidadeDeGeracao1(1, cfg=self.cfg, leituras_usina=self.leituras)
        self.ug2 = UnidadeDeGeracao2(2, cfg=self.cfg, leituras_usina=self.leituras)
        self.ugs = [self.ug1, self.ug2]

        # Define as vars inciais
        self.ts_last_ping_tda = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        self.ts_ultima_tentativa_normalizacao = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

        self.ts_nv = []
        self.condicionadores = []
        self.nv_montante_recentes = []
        self.nv_montante_anteriores = []
        self.condicionadores_essenciais = []

        self.aux = 1
        self.erro_nv = 0
        self.aux_ping = 0
        self.pot_disp = 0
        self.state_moa = 0
        self.controle_p = 0
        self.controle_i = 0
        self.controle_d = 0
        self.modo_autonomo = 1
        self.erro_nv_anterior = 0
        self.pot_alvo_anterior = -1
        self.nv_montante_recente = 0
        self.nv_montante_anterior = 0
        self.db_emergencia_acionada = 0
        self.potencia_alvo_anterior = -1
        self.clp_emergencia_acionada = 0
        self.modo_de_escolha_das_ugs = 0
        self.aguardando_reservatorio = 0
        self.agendamentos_atrasados = 0
        self.tentativas_de_normalizar = 0

        self.__split1 = False
        self.__split2 = False
        self.tensao_ok = True
        self.timer_tensao = None
        self.TDA_Offline = False
        self.acionar_voip = False
        self.TDA_FalhaComum = False
        self.BombasDngRemoto = True
        self.avisado_em_eletrica = False
        self.tensao_emerg_comporta = True
        self.Disj_GDE_QCAP_Fechado = False
        self.deve_tentar_normalizar = True
        self.deve_normalizar_forcado = False
        self.deve_ler_condicionadores = False

        self.client = Client(self.cfg["opc_server"])

        self.clp = ModbusClient(
            host=self.cfg["USN_slave_ip"],
            port=self.cfg["USN_slave_porta"],
            timeout=5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )

        threading.Thread(target=lambda: self.leitura_condicionadores()).start()
        
        self.escrever_valores()

        # ajuste inicial ie
        if self.cfg["saida_ie_inicial"] == "auto":
            self.controle_ie = (self.ug1.leitura_potencia.valor + self.ug2.leitura_potencia.valor) / self.cfg["pot_maxima_alvo"]
        
        else:
            self.controle_ie = self.cfg["saida_ie_inicial"]

        self.controle_i = self.controle_ie

        # ajuste inicial SP
        logger.debug("self.ug1.leitura_potencia.valor -> {}".format(self.ug1.leitura_potencia.valor))
        logger.debug("self.ug2.leitura_potencia.valor -> {}".format(self.ug2.leitura_potencia.valor))

        parametros = self.db.get_parametros_usina()
        self.atualizar_limites_operacao(parametros)

    @property
    def nv_montante(self):
        return self.leituras.nv_montante.valor

    def ler_valores(self):

        parametros = self.db.get_parametros_usina()
        self.cfg["TDA_slave_ip"] = parametros["clp_tda_ip"]

        # -> Verifica conexão com CLP Tomada d'água
        if not ping(self.cfg["TDA_slave_ip"]):
            self.TDA_Offline = True
            if self.TDA_Offline and self.aux_ping == 0:
                self.aux_ping = 1
                logger.warning("CLP TDA não respondeu a tentativa de comunicação!")
        elif ping(self.cfg["TDA_slave_ip"]) and self.aux_ping == 1:
            logger.info("Comunicação com o CLP TDA reestabelecida.")
            self.aux_ping = 0
            self.TDA_Offline = False
        
        # -> Verifica conexão com CLP Sub
        if not ping(self.cfg["USN_slave_ip"]):
            logger.warning("CLP 'USN' (PACP) não respondeu a tentativa de comunicação!")

        # -> Verifica conexão com CLP UG#
        if not ping(self.cfg["UG1_slave_ip"]):
            logger.warning("CLP UG1 não respondeu a tentativa de comunicação!")
            self.ug1.forcar_estado_restrito()

        if not ping(self.cfg["UG2_slave_ip"]):
            logger.warning("CLP UG2 não respondeu a tentativa de comunicação!")
            self.ug2.forcar_estado_restrito()

        self.clp_online = True
        self.clp_emergencia_acionada = 0

        if not self.TDA_Offline:
            if self.nv_montante_recente < 1:
                self.nv_montante_recentes = [self.leituras.nv_montante.valor] * 240

            self.nv_montante_recentes.append(round(self.leituras.nv_montante.valor, 2))
            self.nv_montante_recentes = self.nv_montante_recentes[1:]

            # VERIFICAR SE O CÁLCULO SEGUINTE SERÁ USADO EM CAMPO
            smoothing = 5
            ema = [sum(self.nv_montante_recentes) / len(self.nv_montante_recentes)]
            for nv in self.nv_montante_recentes:
                ema.append((nv * (smoothing / (1 + len(self.nv_montante_recentes)))) + ema[-1] * (1 - (smoothing / (1 + len(self.nv_montante_recentes)))))

            self.nv_montante_recente = ema[-1]  # REMOVER SEB
            self.nv_montante_recente = self.leituras.nv_montante.valor

            self.erro_nv_anterior = self.erro_nv
            self.erro_nv = self.nv_montante_recente - self.cfg["nv_alvo"]

        # Botão de emergência
        self.db_emergencia_acionada = int(parametros["emergencia_acionada"])

        # Limites de operação das UGS
        self.atualizar_limites_operacao(parametros)

        # nv_minimo
        self.cfg["nv_minimo"] = float(parametros["nv_minimo"])

        # Modo autonomo
        logger.debug("Modo autonomo que o banco respondeu: {}".format(int(parametros["modo_autonomo"])))
        self.modo_autonomo = int(parametros["modo_autonomo"])

        # Modo de prioridade UGS
        if not self.modo_de_escolha_das_ugs == int(parametros["modo_de_escolha_das_ugs"]):
            self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
            logger.info("O modo de prioridade das ugs foi alterado (#{}).".format(self.modo_de_escolha_das_ugs))

        # Parametros banco
        self.cfg["nv_alvo"] = float(parametros["nv_alvo"])
        self.cfg["kp"] = float(parametros["kp"])
        self.cfg["ki"] = float(parametros["ki"])
        self.cfg["kd"] = float(parametros["kd"])
        self.cfg["kie"] = float(parametros["kie"])
        self.cfg["pot_maxima_usina"] = float(parametros["pot_nominal_ug"]) * 2
        self.cfg["pot_maxima_alvo"] = float(parametros["pot_nominal"])
        self.cfg["pot_maxima_ug"] = float(parametros["pot_nominal_ug"])

        self.cfg["pt_kp"] = float(parametros["pt_kp"])
        self.cfg["pt_ki"] = float(parametros["pt_ki"])
        self.cfg["pt_kie"] = float(parametros["pt_kie"])
        self.cfg["press_turbina_alvo"] = float(parametros["press_turbina_alvo"])

        # Le o databank interno
        if DataBank.get_words(REG_MB["MOA"]["IN_EMERG"])[0] == 1 and self.avisado_em_eletrica==False:
            self.avisado_em_eletrica = True
            for ug in self.ugs:
                ug.deve_ler_condicionadores = True

        elif DataBank.get_words(REG_MB["MOA"]["IN_EMERG"])[0] == 0 and self.avisado_em_eletrica==True:
            self.avisado_em_eletrica = False
            for ug in self.ugs:
                ug.deve_ler_condicionadores = False

        if DataBank.get_words(REG_MB["MOA"]["IN_EMERG_UG1"])[0] == 1:
            self.ug1.deve_ler_condicionadores = True

        elif DataBank.get_words(REG_MB["MOA"]["IN_EMERG_UG2"])[0] == 1:
            self.ug2.deve_ler_condicionadores = True

        else:
            for ug in self.ugs:
                ug.deve_ler_condicionadores = False
        
        if DataBank.get_words(REG_MB["MOA"]["IN_HABILITA_AUTO"])[0] == 1:
            DataBank.set_words(REG_MB["MOA"]["IN_HABILITA_AUTO"], [1])
            DataBank.set_words(REG_MB["MOA"]["IN_DESABILITA_AUTO"], [0])
            self.modo_autonomo = 1

        if DataBank.get_words(REG_MB["MOA"]["IN_DESABILITA_AUTO"])[0] == 1:
            DataBank.set_words(REG_MB["MOA"]["IN_HABILITA_AUTO"], [0])
            DataBank.set_words(REG_MB["MOA"]["IN_DESABILITA_AUTO"], [1])
            self.modo_autonomo = 0
            self.entrar_em_modo_manual()

        self.heartbeat()

    def escrever_valores(self):

        if self.modo_autonomo:
            self.con.modifica_controles_locais()
        # DB
        # Escreve no banco
        # Paulo: mover lógica de escrever no banco para um método em DBService
        try:
            valores = [
                datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None).strftime("%Y-%m-%d %H:%M:%S"),  # timestamp
                1 if self.aguardando_reservatorio else 0,  # aguardando_reservatorio
                True,  # DEPRECATED clp_online
                self.nv_montante if not self.TDA_Offline else 0,  # nv_montante
                1 if self.ug1.disponivel else 0,  # ug1_disp
                self.ug1.leitura_potencia.valor,  # ug1_pot
                self.ug1.setpoint,  # ug1_setpot
                self.ug1.etapa_atual,  # ug1_sinc
                self.ug1.leitura_horimetro_hora.valor,  # ug1_tempo
                1 if self.ug2.disponivel else 0,  # ug2_disp
                self.ug2.leitura_potencia.valor,  # ug2_pot
                self.ug2.setpoint,  # ug2_setpot
                self.ug2.etapa_atual,  # ug2_sinc
                self.ug2.leitura_horimetro_hora.valor,  # ug2_tempo
            ]
            self.db.update_valores_usina(valores)

        except Exception as e:
            logger.exception(e)

    def atualizar_limites_operacao(self, db):
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
        self.clp_emergencia_acionada = 1

    def normalizar_emergencia(self):
        logger.debug("Normalizando (e verificações)")
        logger.debug("Ultima tentativa: {}. Tensão na linha: RS {:2.1f}kV ST{:2.1f}kV TR{:2.1f}kV.".format(
                self.ts_ultima_tentativa_normalizacao,
                self.leituras.tensao_rs.valor / 1000,
                self.leituras.tensao_st.valor / 1000,
                self.leituras.tensao_tr.valor / 1000,))

        if not(self.cfg["TENSAO_LINHA_BAIXA"] < self.leituras.tensao_rs.valor < self.cfg["TENSAO_LINHA_ALTA"] \
            and self.cfg["TENSAO_LINHA_BAIXA"] < self.leituras.tensao_st.valor < self.cfg["TENSAO_LINHA_ALTA"] \
            and self.cfg["TENSAO_LINHA_BAIXA"] < self.leituras.tensao_tr.valor < self.cfg["TENSAO_LINHA_ALTA"]):
            self.tensao_ok = False
            return False

        elif self.deve_normalizar_forcado or (self.deve_tentar_normalizar and (datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None) - self.ts_ultima_tentativa_normalizacao).seconds >= 60 * self.tentativas_de_normalizar):
            self.tentativas_de_normalizar += 1
            self.ts_ultima_tentativa_normalizacao = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
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
        temporizador = time() + delay
        logger.warning("Iniciando o timer para a normalização da tensão na linha")
    
        while time() <= temporizador:
            sleep(time() - (time() - 15))
            if (self.cfg["TENSAO_LINHA_BAIXA"] < self.leituras.tensao_rs.valor < self.cfg["TENSAO_LINHA_ALTA"] \
                and self.cfg["TENSAO_LINHA_BAIXA"] < self.leituras.tensao_st.valor < self.cfg["TENSAO_LINHA_ALTA"] \
                and self.cfg["TENSAO_LINHA_BAIXA"] < self.leituras.tensao_tr.valor < self.cfg["TENSAO_LINHA_ALTA"]):
                logger.info("Tensão na linha reestabelecida.")
                self.timer_tensao = True
                return True
        
        logger.warning("Não foi possível reestabelecer a tensão na linha")
        self.timer_tensao = False
        return False

    def heartbeat(self):

        agora = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

        ano = int(agora.year)
        mes = int(agora.month)
        dia = int(agora.day)
        hor = int(agora.hour)
        mnt = int(agora.minute)
        seg = int(agora.second)
        mil = int(agora.microsecond / 1000)
        DataBank.set_words(0, [ano, mes, dia, hor, mnt, seg, mil])
        DataBank.set_words(REG_MB["MOA"]["OUT_STATUS"], [self.state_moa])
        DataBank.set_words(REG_MB["MOA"]["OUT_MODE"], [self.modo_autonomo])

        if self.modo_autonomo == 1:
            DataBank.set_words(REG_MB["MOA"]["OUT_EMERG"], [1 if self.clp_emergencia_acionada else 0],)
            DataBank.set_words(REG_MB["MOA"]["OUT_TARGET_LEVEL"], [int((self.cfg["nv_alvo"] - 461.37) * 1000)])
            DataBank.set_words(REG_MB["MOA"]["OUT_SETPOINT"], [int(self.ug1.setpoint + self.ug2.setpoint)], )

            if self.avisado_em_eletrica==True and self.aux==1:
                DataBank.set_words(REG_MB["MOA"]["OUT_BLOCK_UG1"], [1],)
                DataBank.set_words(REG_MB["MOA"]["OUT_BLOCK_UG2"], [1],)
                self.aux=0
            elif self.avisado_em_eletrica==False and self.aux==0:
                DataBank.set_words(REG_MB["MOA"]["OUT_BLOCK_UG1"], [0],)
                DataBank.set_words(REG_MB["MOA"]["OUT_BLOCK_UG2"], [0],)
                self.aux=1

            if DataBank.get_words(REG_MB["MOA"]["IN_HABILITA_AUTO"])[0] == 1:
                DataBank.set_words(REG_MB["MOA"]["IN_HABILITA_AUTO"], [1])
                DataBank.set_words(REG_MB["MOA"]["IN_DESABILITA_AUTO"], [0])
                self.modo_autonomo = 1

            elif DataBank.get_words(REG_MB["MOA"]["IN_DESABILITA_AUTO"])[0] == 1:
                DataBank.set_words(REG_MB["MOA"]["IN_HABILITA_AUTO"], [0])
                DataBank.set_words(REG_MB["MOA"]["IN_DESABILITA_AUTO"], [1])
                self.modo_autonomo = 0
                self.entrar_em_modo_manual()

            if DataBank.get_words(REG_MB["MOA"]["OUT_BLOCK_UG1"])[0] == 1:
                DataBank.set_words(REG_MB["MOA"]["OUT_BLOCK_UG1"], [1])

            elif DataBank.get_words(REG_MB["MOA"]["OUT_BLOCK_UG1"])[0] == 0:
                DataBank.set_words(REG_MB["MOA"]["OUT_BLOCK_UG1"], [0])

            if DataBank.get_words(REG_MB["MOA"]["OUT_BLOCK_UG2"])[0] == 1:
                DataBank.set_words(REG_MB["MOA"]["OUT_BLOCK_UG2"], [1])

            elif DataBank.get_words(REG_MB["MOA"]["OUT_BLOCK_UG2"])[0] == 0:
                DataBank.set_words(REG_MB["MOA"]["OUT_BLOCK_UG2"], [0])

        elif self.modo_autonomo == 0:
            DataBank.set_words(REG_MB["MOA"]["OUT_EMERG"], [0])
            DataBank.set_words(REG_MB["MOA"]["OUT_TARGET_LEVEL"], [0])
            DataBank.set_words(REG_MB["MOA"]["OUT_SETPOINT"], [0])
            DataBank.set_words(REG_MB["MOA"]["OUT_BLOCK_UG1"], [0])
            DataBank.set_words(REG_MB["MOA"]["OUT_BLOCK_UG2"], [0])
            

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
                if agendamento[3] == AGENDAMENTO_INDISPONIBILIZAR:
                    logger.warning("Acionando emergência!")
                    self.acionar_emergencia()
                    self.db.update_agendamento(int(agendamento[0]), 1, obs="AGENDAMENTO NÃO EXECUTADO POR CONTA DE ATRASO!")
                    return False
                elif agendamento[3] == AGENDAMENTO_ALTERAR_NV_ALVO or agendamento[3] == AGENDAMENTO_ALTERAR_POT_LIMITE_TODAS_AS_UGS or agendamento[3] == AGENDAMENTO_BAIXAR_POT_UGS_MINIMO or agendamento[3] == AGENDAMENTO_NORMALIZAR_POT_UGS_MINIMO:
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

                # Exemplo Case agendamento:
                if agendamento[3] == AGENDAMENTO_DISPARAR_MENSAGEM_TESTE:
                    # Coloca em emergência
                    logger.debug("Disparando mensagem teste (comando via agendamento).")
                    self.disparar_mensagem_teste()

                if agendamento[3] == AGENDAMENTO_INDISPONIBILIZAR:
                    # Coloca em emergência
                    logger.info("Indisponibilizando a usina (comando via agendamento).")
                    for ug in self.ugs:
                        ug.forcar_estado_indisponivel()
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
                        logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))

                    self.cfg["nv_alvo"] = novo

                if agendamento[3] == AGENDAMENTO_BAIXAR_POT_UGS_MINIMO:
                    try:
                        self.cfg["pot_maxima_ug1"] = self.cfg["pot_minima"]
                        self.cfg["pot_maxima_ug2"] = self.cfg["pot_minima"]
                        for ug in self.ugs:
                            if ug.etapa_atual == UNIDADE_PARADA or ug.etapa_alvo == UNIDADE_PARADA:
                                logger.debug("A UG{} já está no estado parada/parando.".format(ug.id))
                            else:
                                logger.debug("Enviando o setpoint mínimo ({}) para a UG{}".format(self.cfg["pot_minima"], ug.id))
                                ug.enviar_setpoint(self.cfg["pot_minima"])

                    except Exception as e:
                        logger.info("Traceback: {}".format(repr(e)))

                if agendamento[3] == AGENDAMENTO_NORMALIZAR_POT_UGS_MINIMO:
                    try:
                        self.cfg["pot_maxima_ug1"] = self.cfg["pot_maxima_ug"]
                        self.cfg["pot_maxima_ug2"] = self.cfg["pot_maxima_ug"]
                        for ug in self.ugs:
                            ug.enviar_setpoint(self.cfg["pot_maxima_ug"])

                    except Exception as e:
                        logger.debug("Traceback: {}".format(repr(e)))

                if agendamento[3] == AGENDAMENTO_UG1_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug1"] = novo
                        self.ug1.pot_disponivel = novo
                    except Exception as e:
                        logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_MANUAL:
                    self.ug1.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_DISPONIVEL:
                    self.ug1.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug1.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_RESTRITO:
                    self.ug1.forcar_estado_restrito()

                if agendamento[3] == AGENDAMENTO_UG2_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug2"] = novo
                        self.ug2.pot_disponivel = novo
                    except Exception as e:
                        logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_MANUAL:
                    self.ug2.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_DISPONIVEL:
                    self.ug2.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug2.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_RESTRITO:
                    self.ug2.forcar_estado_restrito()

                if agendamento[3] == AGENDAMENTO_ALTERAR_POT_LIMITE_TODAS_AS_UGS:
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
                self.con.somente_reconhecer_emergencia()
                self.escrever_valores()

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
                    -1 * y.leitura_potencia.valor,
                    -1 * y.setpoint,
                    y.prioridade,
                ),
            )
        else:
            # escolher por menor horas_maquina primeiro
            ls = sorted(
                ls,
                key=lambda y: (
                    -1 * y.leitura_potencia.valor,
                    -1 * y.setpoint,
                    y.leitura_horimetro.valor,
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
        ts = datetime.now().timestamp()
        try:
            ts = datetime.now().timestamp()
            logger.debug("Inserting in db")
            ma = 1 if self.modo_autonomo else 0
            self.db.insert_debug(
                ts,
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
                ma,
                self.cfg["pt_kp"],
                self.cfg["pt_ki"],
                self.cfg["pt_kie"],
                0,
            )
        except Exception as e:
            logger.exception(e)

        pot_alvo = self.distribuir_potencia(pot_alvo)

    def entrar_em_modo_manual(self):
        self.modo_autonomo = 0
        self.db.update_modo_manual()
    
    def leitura_condicionadores(self):
        
        # Essenciais
        self.leitura_in_emergencia = DataBank.get_words(REG_MB["MOA"]["IN_EMERG"])[0]
        x = self.leitura_in_emergencia
        self.condicionadores_essenciais.append(CondicionadorBase("MOA_IN_EMERG", DEVE_INDISPONIBILIZAR, x,))

        self.leitura_sem_emergencia_tda = LeituraOPCBit(self.client, REG_OPC["TDA"]["SEM_EMERGENCIA"], 24, True)
        x = self.leitura_sem_emergencia_tda
        self.condicionadores_essenciais.append(CondicionadorBase("SEM_EMERGENCIA_TDA - bit 24", DEVE_NORMALIZAR, x))
        
        self.leitura_sem_emergencia_sa = LeituraOPCBit(self.client, REG_OPC["SA"]["SEM_EMERGENCIA"], 13, True)
        x = self.leitura_sem_emergencia_sa
        self.condicionadores_essenciais.append(CondicionadorBase("SEM_EMERGENCIA_SA - bit 13", DEVE_NORMALIZAR, x))

        self.leitura_rele_linha_atuado = LeituraOPCBit(self.client, REG_OPC["SE"]["RELE_LINHA_ATUADO"], 14)
        x = self.leitura_rele_linha_atuado
        self.condicionadores_essenciais.append(CondicionadorBase("RELE_LINHA_ATUADO - bit 14", DEVE_NORMALIZAR, x))


        # Gerais
        self.leitura_fusivel_queimado_retificador = LeituraOPCBit(self.client, REG_OPC["SA"]["RETIFICADOR_FUSIVEL_QUEIMADO"], 2)
        x = self.leitura_fusivel_queimado_retificador
        self.condicionadores.append(CondicionadorBase("RETIFICADOR_FUSIVEL_QUEIMADO - bit 02", DEVE_INDISPONIBILIZAR, x))

        self.leitura_fuga_terra_positivo_retificador = LeituraOPCBit(self.client, REG_OPC["SA"]["RETIFICADOR_FUGA_TERRA_POSITIVO"], 5)
        x = self.leitura_fuga_terra_positivo_retificador
        self.condicionadores.append(CondicionadorBase("RETIFICADOR_FUGA_TERRA_POSITIVO - bit 05", DEVE_INDISPONIBILIZAR, x))

        self.leitura_fuga_terra_negativo_retificador = LeituraOPCBit(self.client, REG_OPC["SA"]["RETIFICADOR_FUGA_TERRA_NEGATIVO"], 6)
        x = self.leitura_fuga_terra_negativo_retificador
        self.condicionadores.append(CondicionadorBase("RETIFICADOR_FUGA_TERRA_NEGATIVO - bit 06", DEVE_INDISPONIBILIZAR, x))

        self.leitura_52sa1_sem_falha = LeituraOPCBit(self.client, REG_OPC["SA"]["52SA1_SEM_FALHA"], 31, True)
        x = self.leitura_52sa1_sem_falha
        self.condicionadores.append(CondicionadorBase("52SA1_SEM_FALHA - bit 31", DEVE_INDISPONIBILIZAR, x))

        self.leitura_sa_72sa1_fechado = LeituraOPCBit(self.client, REG_OPC["SA"]["SA_72SA1_FECHADO"], 10, True)
        x = self.leitura_sa_72sa1_fechado
        self.condicionadores.append(CondicionadorBase("SA_72SA1_FECHADO - bit 10", DEVE_INDISPONIBILIZAR, x))

        self.leitura_disj_125vcc_fechados = LeituraOPCBit(self.client, REG_OPC["SA"]["DISJUNTORES_125VCC_FECHADOS"], 11, True)
        x = self.leitura_disj_125vcc_fechados
        self.condicionadores.append(CondicionadorBase("DISJUNTORES_125VCC_FECHADOS - bit 11", DEVE_INDISPONIBILIZAR, x))

        self.leitura_disj_24vcc_fechados = LeituraOPCBit(self.client, REG_OPC["SA"]["DISJUNTORES_24VCC_FECHADOS"], 12, True)
        x = self.leitura_disj_24vcc_fechados
        self.condicionadores.append(CondicionadorBase("DISJUNTORES_24VCC_FECHADOS - bit 12", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_alimentacao_125vcc_com_tensao = LeituraOPCBit(self.client, REG_OPC["SA"]["COM_TENSAO_ALIMENTACAO_125VCC"], 13, True)
        x = self.leitura_alimentacao_125vcc_com_tensao
        self.condicionadores.append(CondicionadorBase("COM_TENSAO_ALIMENTACAO_125VCC - bit 13", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_comando_125vcc_com_tensao = LeituraOPCBit(self.client, REG_OPC["SA"]["COM_TENSAO_COMANDO_125VCC"], 14, True)
        x = self.leitura_comando_125vcc_com_tensao
        self.condicionadores.append(CondicionadorBase("COM_TENSAO_COMANDO_125VCC - bit 14", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_comando_24vcc_com_tensao = LeituraOPCBit(self.client, REG_OPC["SA"]["COM_TENSAO_COMANDO_24VCC"], 15, True)
        x = self.leitura_comando_24vcc_com_tensao
        self.condicionadores.append(CondicionadorBase("COM_TENSAO_COMANDO_24VCC - bit 15", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_abrir_52sa1 = LeituraOPCBit(self.client, REG_OPC["SA"]["FALHA_ABRIR_52SA1"], 0)
        x = self.leitura_falha_abrir_52sa1
        self.condicionadores.append(CondicionadorBase("FALHA_ABRIR_52SA1 - bit 00", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_fechar_52sa1 = LeituraOPCBit(self.client, REG_OPC["SA"]["FALHA_FECHAR_52SA1"], 1)
        x = self.leitura_falha_fechar_52sa1
        self.condicionadores.append(CondicionadorBase("FALHA_FECHAR_52SA1 - bit 01", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_abrir_52sa2 = LeituraOPCBit(self.client, REG_OPC["SA"]["FALHA_ABRIR_52SA2"], 3)
        x = self.leitura_falha_abrir_52sa2
        self.condicionadores.append(CondicionadorBase("FALHA_ABRIR_52SA2 - bit 03", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_fechar_52sa2 = LeituraOPCBit(self.client, REG_OPC["SA"]["FALHA_FECHAR_52SA2"], 4)
        x = self.leitura_falha_fechar_52sa2
        self.condicionadores.append(CondicionadorBase("FALHA_FECHAR_52SA2 - bit 04", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_abrir_52sa3 = LeituraOPCBit(self.client, REG_OPC["SA"]["FALHA_ABRIR_52SA3"], 5)
        x = self.leitura_falha_abrir_52sa3
        self.condicionadores.append(CondicionadorBase("FALHA_ABRIR_52SA3 - bit 05", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_fechar_52sa3 = LeituraOPCBit(self.client, REG_OPC["SA"]["FALHA_FECHAR_52SA3"], 6)
        x = self.leitura_falha_fechar_52sa3
        self.condicionadores.append(CondicionadorBase("FALHA_FECHAR_52SA3 - bit 06", DEVE_INDISPONIBILIZAR, x))

        self.leitura_89l_fechada = LeituraOPCBit(self.client, REG_OPC["SE"]["89L_FECHADA"], 12, True)
        x = self.leitura_89l_fechada
        self.condicionadores.append(CondicionadorBase("89L_FECHADA - bit 12", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_oleo_te = LeituraOPCBit(self.client, REG_OPC["SE"]["TE_TRIP_TEMPERATURA_OLEO"], 19)
        x = self.leitura_trip_temp_oleo_te
        self.condicionadores.append(CondicionadorBase("TE_TRIP_TEMPERATURA_OLEO - bit 19", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_enrol_te = LeituraOPCBit(self.client, REG_OPC["SE"]["TE_TRIP_TEMPERATURA_ENROLAMENTO"], 20)
        x = self.leitura_trip_temp_enrol_te
        self.condicionadores.append(CondicionadorBase("TE_TRIP_TEMPERATURA_ENROLAMENTO - bit 20", DEVE_INDISPONIBILIZAR, x))

        self.leitura_alarme_rele_buchholz = LeituraOPCBit(self.client, REG_OPC["SE"]["TE_ALARME_RELE_BUCHHOLZ"], 22)
        x = self.leitura_alarme_rele_buchholz
        self.condicionadores.append(CondicionadorBase("TE_ALARME_RELE_BUCHHOLZ - bit 22", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_rele_buchholz = LeituraOPCBit(self.client, REG_OPC["SE"]["TE_TRIP_RELE_BUCHHOLZ"], 23)
        x = self.leitura_trip_rele_buchholz
        self.condicionadores.append(CondicionadorBase("TE_TRIP_RELE_BUCHHOLZ - bit 23", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_alivio_pressao = LeituraOPCBit(self.client, REG_OPC["SE"]["TE_TRIP_ALIVIO_PRESSAO"], 24)
        x = self.leitura_trip_alivio_pressao
        self.condicionadores.append(CondicionadorBase("TE_TRIP_ALIVIO_PRESSAO - bit 24", DEVE_INDISPONIBILIZAR, x))

        self.leitura_atuacao_rele_linha_bf = LeituraOPCBit(self.client, REG_OPC["SE"]["RELE_LINHA_ATUACAO_BF"], 16)
        x = self.leitura_atuacao_rele_linha_bf
        self.condicionadores.append(CondicionadorBase("RELE_LINHA_ATUACAO_BF - bit 16", DEVE_INDISPONIBILIZAR, x))

        self.leitura_rele_te_atuado = LeituraOPCBit(self.client, REG_OPC["SE"]["TE_RELE_ATUADO"], 17)
        x = self.leitura_rele_te_atuado
        self.condicionadores.append(CondicionadorBase("TE_RELE_ATUADO - bit 17", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_86bf_atuado = LeituraOPCBit(self.client, REG_OPC["SE"]["86BF_ATUADO"], 19)
        x = self.leitura_86bf_atuado
        self.condicionadores.append(CondicionadorBase("86BF_ATUADO - bit 19", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_86t_atuado = LeituraOPCBit(self.client, REG_OPC["SE"]["86T_ATUADO"], 20)
        x = self.leitura_86t_atuado
        self.condicionadores.append(CondicionadorBase("86T_ATUADO - bit 20", DEVE_INDISPONIBILIZAR, x))

        self.leitura_super_bobinas_reles_bloq = LeituraOPCBit(self.client, REG_OPC["SE"]["SUPERVISAO_BOBINAS_RELES_BLOQUEIOS"], 21)
        x = self.leitura_super_bobinas_reles_bloq
        self.condicionadores.append(CondicionadorBase("SUPERVISAO_BOBINAS_RELES_BLOQUEIOS - bit 21", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_comando_abertura_52l = LeituraOPCBit(self.client, REG_OPC["SE"]["FALHA_COMANDO_ABERTURA_52L"], 1)
        x = self.leitura_falha_comando_abertura_52l
        self.condicionadores.append(CondicionadorBase("FALHA_COMANDO_ABERTURA_52L - bit 01", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_comando_fechamento_52l = LeituraOPCBit(self.client, REG_OPC["SE"]["FALHA_COMANDO_FECHAMENTO_52L"], 2)
        x = self.leitura_falha_comando_fechamento_52l
        self.condicionadores.append(CondicionadorBase("FALHA_COMANDO_FECHAMENTO_52L - bit 02", DEVE_INDISPONIBILIZAR, x))


        # Normalizar
        self.leitura_retificador_subtensao = LeituraOPCBit(self.client, REG_OPC["SA"]["RETIFICADOR_SUBTENSAO"], 31)
        x = self.leitura_retificador_subtensao
        self.condicionadores.append(CondicionadorBase("RETIFICADOR_SUBTENSAO - bit 31", DEVE_NORMALIZAR, x))
        
        self.leitura_ca_com_tensao = LeituraOPCBit(self.client, REG_OPC["TDA"]["COM_TENSAO_CA"], 11, True)
        x = self.leitura_ca_com_tensao
        self.condicionadores.append(CondicionadorBase("COM_TENSAO_CA - bit 11", DEVE_NORMALIZAR, x))

        self.leitura_falha_ligar_bomba_uh = LeituraOPCBit(self.client, REG_OPC["TDA"]["UH_FALHA_LIGAR_BOMBA"], 2)
        x = self.leitura_falha_ligar_bomba_uh
        self.condicionadores.append(CondicionadorBase("UH_FALHA_LIGAR_BOMBA - bit 02", DEVE_NORMALIZAR, x))

        self.leitura_retificador_sobretensao = LeituraOPCBit(self.client, REG_OPC["SA"]["RETIFICADOR_SOBRETENSAO"], 30)
        x = self.leitura_retificador_sobretensao
        self.condicionadores.append(CondicionadorBase("RETIFICADOR_SOBRETENSAO - bit 30", DEVE_NORMALIZAR, x))

        self.leitura_retificador_sobrecorrente_saida = LeituraOPCBit(self.client, REG_OPC["SA"]["RETIFICADOR_SOBRECORRENTE_SAIDA"], 0)
        x = self.leitura_retificador_sobrecorrente_saida
        self.condicionadores.append(CondicionadorBase("RETIFICADOR_SOBRECORRENTE_SAIDA - bit 00", DEVE_NORMALIZAR, x))

        self.leitura_retificador_sobrecorrente_baterias = LeituraOPCBit(self.client, REG_OPC["SA"]["RETIFICADOR_SOBRECORRENTE_BATERIAS"], 1)
        x = self.leitura_retificador_sobrecorrente_baterias
        self.condicionadores.append(CondicionadorBase("RETIFICADOR_SOBRECORRENTE_BATERIAS - bit 01", DEVE_NORMALIZAR, x))

        self.leitura_falha_sistema_agua_pressurizar_fa = LeituraOPCBit(self.client, REG_OPC["SA"]["SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_A"], 3)
        x = self.leitura_falha_sistema_agua_pressurizar_fa
        self.condicionadores.append(CondicionadorBase("SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_A - bit 03", DEVE_NORMALIZAR, x))

        self.leitura_falha_sistema_agua_pressostato_fa = LeituraOPCBit(self.client, REG_OPC["SA"]["SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_A"], 4)
        x = self.leitura_falha_sistema_agua_pressostato_fa
        self.condicionadores.append(CondicionadorBase("SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_A - bit 04", DEVE_NORMALIZAR, x))

        self.leitura_falha_sistema_agua_pressurizar_fb = LeituraOPCBit(self.client, REG_OPC["SA"]["SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_B"], 5)
        x = self.leitura_falha_sistema_agua_pressurizar_fb
        self.condicionadores.append(CondicionadorBase("SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_B - bit 05", DEVE_NORMALIZAR, x))
        
        self.leitura_falha_sistema_agua_pressostato_fb = LeituraOPCBit(self.client, REG_OPC["SA"]["SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_B"], 6)
        x = self.leitura_falha_sistema_agua_pressostato_fb
        self.condicionadores.append(CondicionadorBase("SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_B - bit 06", DEVE_NORMALIZAR, x))

        return True

    def leituras_por_hora(self):
        # Telegram

        self.leitura_filtro_limpo_uh = LeituraOPCBit(self.client, REG_OPC["TDA"]["UH_FILTRO_LIMPO"], 13, True)
        if not self.leitura_filtro_limpo_uh:
            logger.warning("O filtro da UH da TDA está sujo. Favor realizar limpeza/troca.")

        self.leitura_ca_com_tensao = LeituraOPCBit(self.client, REG_OPC["TDA"]["COM_TENSAO_CA"], 11, True)
        if not self.leitura_ca_com_tensao:
            logger.warning("Foi dentificado que o CA da tomada da água está sem tensão. Favor verificar.")

        self.leitura_lg_operacao_manual = LeituraOPCBit(self.client, REG_OPC["TDA"]["LG_OPERACAO_MANUAL"], 0)
        if self.leitura_lg_operacao_manual:
            logger.warning("Foi identificado que o Limpa Grades entrou em operação manual. Favor verificar.")

        self.leitura_nivel_jusante_comporta_1 = LeituraOPCBit(self.client, REG_OPC["TDA"]["NIVEL_JUSANTE_COMPORTA_1"], 2)
        if self.leitura_nivel_jusante_comporta_1:
            logger.warning("Houve uma falha no sensor de nível jusante da comporta 1. Favor verificar.")

        self.leitura_nivel_jusante_comporta_2 = LeituraOPCBit(self.client, REG_OPC["TDA"]["NIVEL_JUSANTE_COMPORTA_2"], 4)
        if self.leitura_nivel_jusante_comporta_2:
            logger.warning("Houve uma falha no sensor de nível jusante da comporta 2. Favor verificar.")

        self.leitura_nivel_jusante_grade_comporta_1 = LeituraOPCBit(self.client, REG_OPC["TDA"]["FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_1"], 1)
        if self.leitura_nivel_jusante_grade_comporta_1:
            logger.warning("Houve uma falha no sensor de nível jusante grade da comporta 1. Favor verificar.")

        self.leitura_nivel_jusante_grade_comporta_2 = LeituraOPCBit(self.client, REG_OPC["TDA"]["FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_2"], 3)
        if self.leitura_nivel_jusante_grade_comporta_2:
            logger.warning("Houve uma falha no sensor de nível jusante grade da comporta 2. Favor verificar.")
        
        self.leitura_falha_bomba_drenagem_1 = LeituraOPCBit(self.client, REG_OPC["SA"]["DRENAGEM_BOMBA_1_FALHA"], 0)
        if self.leitura_falha_bomba_drenagem_1:
            logger.warning("Houve uma falha na bomba 1 do poço de drenagem. Favor verificar.")
        
        self.leitura_falha_bomba_drenagem_2 = LeituraOPCBit(self.client, REG_OPC["SA"]["DRENAGEM_BOMBA_2_FALHA"], 2)
        if self.leitura_falha_bomba_drenagem_2:
            logger.warning("Houve uma falha na bomba 2 do poço de drenagem. Favor verificar.")
        
        self.leitura_falha_bomba_drenagem_3 = LeituraOPCBit(self.client, REG_OPC["SA"]["DRENAGEM_BOMBA_3_FALHA"], 4)
        if self.leitura_falha_bomba_drenagem_3:
            logger.warning("Houve uma falha na bomba 3 do poço de drenagem. Favor verificar.")

        self.leitura_djs_barra_seletora_remoto = LeituraOPCBit(self.client, REG_OPC["SA"]["DISJUNTORES_BARRA_SELETORA_REMOTO"], 9)
        if self.leitura_djs_barra_seletora_remoto:
            logger.warning("Os disjuntores da barra seletora saíram do modo remoto. Favor verificar.")

        self.leitura_discrepancia_boia_poco_drenagem = LeituraOPCBit(self.client, REG_OPC["SA"]["DRENAGEM_DISCREPANCIA_BOIAS_POCO"], 9)
        if self.leitura_discrepancia_boia_poco_drenagem:
            logger.warning("Foram identificados sinais inconsistentes nas boias do poço de drenagem. Favor verificar.")

        self.leitura_falha_ligar_bomba_sis_agua = LeituraOPCBit(self.client, REG_OPC["SA"]["SISTEMA_AGUA_FALHA_LIGA_BOMBA"], 1)
        if self.leitura_falha_ligar_bomba_sis_agua:
            logger.warning("Houve uma falha ao ligar a bomba do sistema de água. Favor verificar.")

        self.leitura_bomba_sis_agua_disp = LeituraOPCBit(self.client, REG_OPC["SA"]["SISTEMA_AGUA_BOMBA_DISPONIVEL"], 0, True)
        if not self.leitura_bomba_sis_agua_disp:
            logger.warning("Foi identificado que a bomba do sistema de água está indisponível. Favor verificar.")

        self.leitura_seletora_52l_remoto = LeituraOPCBit(self.client, REG_OPC["SE"]["52L_SELETORA_REMOTO"], 10, True)
        if not self.leitura_seletora_52l_remoto:
            logger.warning("O Disjuntor 52L saiu do modo remoto. Favor verificar.")

        self.leitura_falha_temp_oleo_te = LeituraOPCBit(self.client, REG_OPC["SE"]["TE_FALHA_TEMPERATURA_OLEO"], 1)
        if self.leitura_falha_temp_oleo_te:
            logger.warning("Houve uma falha de leitura de temperatura do óleo do transformador elevador. Favor verificar.")

        self.leitura_falha_temp_enrolamento_te = LeituraOPCBit(self.client, REG_OPC["SE"]["TE_FALHA_TEMPERATURA_ENROLAMENTO"], 2)
        if self.leitura_falha_temp_enrolamento_te:
            logger.warning("Houve uma falha de leitura de temperatura do enrolamento do transformador elevador. Favor verificar.")


        # Telegram + Voip
        self.leitura_falha_atuada_lg = LeituraOPCBit(self.client, REG_OPC["TDA"]["LG_FALHA_ATUADA"], 31)
        if self.leitura_falha_atuada_lg and not VOIP["LG_FALHA_ATUADA"]:
            logger.warning("Foi identificado que o limpa grades está em falha. Favor verificar.")
            VOIP["LG_FALHA_ATUADA"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_atuada_lg and VOIP["LG_FALHA_ATUADA"]:
            VOIP["LG_FALHA_ATUADA"] = False

        self.leitura_falha_nivel_montante = LeituraOPCBit(self.client, REG_OPC["TDA"]["FALHA_NIVEL_MONTANTE"], 0)
        if self.leitura_falha_nivel_montante and not VOIP["FALHA_NIVEL_MONTANTE"]:
            logger.warning("Houve uma falha na leitura de nível montante. Favor verificar.")
            VOIP["FALHA_NIVEL_MONTANTE"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_nivel_montante and VOIP["FALHA_NIVEL_MONTANTE"]:
            VOIP["FALHA_NIVEL_MONTANTE"] = False

        self.leitura_falha_bomba_filtragem = LeituraOPCBit(self.client, REG_OPC["SA"]["FILTRAGEM_BOMBA_FALHA"], 6)
        if self.leitura_falha_bomba_filtragem and not VOIP["FILTRAGEM_BOMBA_FALHA"]:
            logger.warning("Houve uma falha na bomba de filtragem. Favor verificar.")
            VOIP["FILTRAGEM_BOMBA_FALHA"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_bomba_filtragem and VOIP["FILTRAGEM_BOMBA_FALHA"]:
            VOIP["FILTRAGEM_BOMBA_FALHA"] = False

        self.leitura_falha_bomba_drenagem_uni = LeituraOPCBit(self.client, REG_OPC["SA"]["DRENAGEM_UNIDADES_BOMBA_FALHA"], 12)
        if self.leitura_falha_bomba_drenagem_uni and not VOIP["DRENAGEM_UNIDADES_BOMBA_FALHA"]:
            logger.warning("Houve uma falha na bomba de drenagem. Favor verificar.")
            VOIP["DRENAGEM_UNIDADES_BOMBA_FALHA"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_bomba_drenagem_uni and VOIP["DRENAGEM_UNIDADES_BOMBA_FALHA"]:
            VOIP["DRENAGEM_UNIDADES_BOMBA_FALHA"] = False

        self.leitura_falha_tubo_succao_bomba_recalque = LeituraOPCBit(self.client, REG_OPC["SA"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"], 14)
        if self.leitura_falha_tubo_succao_bomba_recalque and not VOIP["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"]:
            logger.warning("Houve uma falha na sucção da bomba de recalque. Favor verificar.")
            VOIP["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_tubo_succao_bomba_recalque and VOIP["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"]:
            VOIP["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"] = False

        self.leitura_nivel_muito_alto_poco_drenagem = LeituraOPCBit(self.client, REG_OPC["SA"]["POCO_DRENAGEM_NIVEL_MUITO_ALTO"], 25)
        if self.leitura_nivel_muito_alto_poco_drenagem and not VOIP["POCO_DRENAGEM_NIVEL_MUITO_ALTO"]:
            logger.warning("Nível do poço de drenagem está muito alto. Favor verificar.")
            VOIP["POCO_DRENAGEM_NIVEL_MUITO_ALTO"] = True
            self.acionar_voip = True
        elif not self.leitura_nivel_muito_alto_poco_drenagem and VOIP["POCO_DRENAGEM_NIVEL_MUITO_ALTO"]:
            VOIP["POCO_DRENAGEM_NIVEL_MUITO_ALTO"] = False

        self.leitura_nivel_alto_poco_drenagem = LeituraOPCBit(self.client, REG_OPC["SA"]["POCO_DRENAGEM_NIVEL_ALTO"], 26)
        if self.leitura_nivel_alto_poco_drenagem and not VOIP["POCO_DRENAGEM_NIVEL_ALTO"]:
            logger.warning("Nível do poço de drenagem alto. Favor verificar.")
            VOIP["POCO_DRENAGEM_NIVEL_ALTO"] = True
            self.acionar_voip = True
        elif not self.leitura_nivel_alto_poco_drenagem and VOIP["POCO_DRENAGEM_NIVEL_ALTO"]:
            VOIP["POCO_DRENAGEM_NIVEL_ALTO"] = False

        self.leitura_sem_falha_52sa1 = LeituraOPCBit(self.client, REG_OPC["SA"]["52SA1_SEM_FALHA"], 31, True)
        if not self.leitura_sem_falha_52sa1 and not VOIP["52SA1_SEM_FALHA"]:
            logger.warning("Houve uma falha com o disjuntor 52SA1 do transformador do SA. Favor verificar.")
            VOIP["52SA1_SEM_FALHA"] = True
        elif self.leitura_sem_falha_52sa1 and VOIP["52SA1_SEM_FALHA"]:
            VOIP["52SA1_SEM_FALHA"] = False

        self.leitura_sem_falha_52sa2 = LeituraOPCBit(self.client, REG_OPC["SA"]["52SA2_SEM_FALHA"], 1, True)
        if not self.leitura_sem_falha_52sa2 and not VOIP["52SA2_SEM_FALHA"]:
            logger.warning("Houve uma falha com o disjuntor 52SA2 do Gerador Diesel. Favor verificar.")
            VOIP["52SA2_SEM_FALHA"] = True
            self.acionar_voip = True
        elif self.leitura_sem_falha_52sa2 and VOIP["52SA2_SEM_FALHA"]:
            VOIP["52SA2_SEM_FALHA"] = False

        self.leitura_sem_falha_52sa3 = LeituraOPCBit(self.client, REG_OPC["SA"]["52SA3_SEM_FALHA"], 3, True)
        if not self.leitura_sem_falha_52sa3 and not VOIP["52SA3_SEM_FALHA"]:
            logger.warning("Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciais. Favor verificar.")
            VOIP["52SA3_SEM_FALHA"] = True
            self.acionar_voip = True
        elif self.leitura_sem_falha_52sa3 and VOIP["52SA3_SEM_FALHA"]:
            VOIP["52SA3_SEM_FALHA"] = False

        self.leitura_alarme_sistema_incendio_atuado = LeituraOPCBit(self.client, REG_OPC["SA"]["SISTEMA_INCENDIO_ALARME_ATUADO"], 6)
        if self.leitura_alarme_sistema_incendio_atuado and not VOIP["SISTEMA_INCENDIO_ALARME_ATUADO"]:
            logger.warning("O alarme do sistema de incêndio foi acionado. Favor verificar.")
            VOIP["SISTEMA_INCENDIO_ALARME_ATUADO"] = True
            self.acionar_voip = True
        elif not self.leitura_alarme_sistema_incendio_atuado and VOIP["SISTEMA_INCENDIO_ALARME_ATUADO"]:
            VOIP["SISTEMA_INCENDIO_ALARME_ATUADO"] = False

        self.leitura_alarme_sistema_seguraca_atuado = LeituraOPCBit(self.client, REG_OPC["SA"]["SISTEMA_SEGURANCA_ALARME_ATUADO"], 7)
        if self.leitura_alarme_sistema_seguraca_atuado and not VOIP["SISTEMA_SEGURANCA_ALARME_ATUADO"]:
            logger.warning("O alarme do sistem de seguraça foi acionado. Favor verificar.")
            VOIP["SISTEMA_SEGURANCA_ALARME_ATUADO"] = True
            self.acionar_voip = True
        elif not self.leitura_alarme_sistema_seguraca_atuado and VOIP["SISTEMA_SEGURANCA_ALARME_ATUADO"]:
            VOIP["SISTEMA_SEGURANCA_ALARME_ATUADO"] = False

        self.leitura_falha_partir_gmg = LeituraOPCBit(self.client, REG_OPC["SA"]["GMG_FALHA_PARTIR"], 6)
        if self.leitura_falha_partir_gmg and not VOIP["GMG_FALHA_PARTIR"]:
            logger.warning("Houve uma falha ao partir o Gerador Diesel. Favor verificar.")
            VOIP["GMG_FALHA_PARTIR"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_partir_gmg and VOIP["GMG_FALHA_PARTIR"]:
            VOIP["GMG_FALHA_PARTIR"] = False

        self.leitura_falha_parar_gmg = LeituraOPCBit(self.client, REG_OPC["SA"]["GMG_FALHA_PARAR"], 7)
        if self.leitura_falha_parar_gmg and not VOIP["GMG_FALHA_PARAR"]:
            logger.warning("Houve uma falha ao parar o Gerador Diesel. Favor verificar.")
            VOIP["GMG_FALHA_PARAR"] = True
            self.acionar_voip = True
        elif not self.leitura_falha_parar_gmg and VOIP["GMG_FALHA_PARAR"]:
            VOIP["GMG_FALHA_PARAR"] = False

        self.leitura_operacao_manual_gmg = LeituraOPCBit(self.client, REG_OPC["SA"]["GMG_OPERACAO_MANUAL"], 10)
        if self.leitura_operacao_manual_gmg and not VOIP["GMG_OPERACAO_MANUAL"]:
            logger.warning("O Gerador Diesel saiu do modo remoto. Favor verificar.")
            VOIP["GMG_OPERACAO_MANUAL"] = True
            self.acionar_voip = True
        elif not self.leitura_operacao_manual_gmg and VOIP["GMG_OPERACAO_MANUAL"]:
            VOIP["GMG_OPERACAO_MANUAL"] = False

        self.leitura_alarme_temp_enrolamento_te = LeituraOPCBit(self.client, REG_OPC["SE"]["TE_ALARME_TEMPERATURA_ENROLAMENTO"], 20)
        if self.leitura_alarme_temp_enrolamento_te and not VOIP["TE_ALARME_TEMPERATURA_ENROLAMENTO"]:
            logger.warning("A temperatura do enrolamento do transformador elevador está alta. Favor verificar.")
            VOIP["TE_ALARME_TEMPERATURA_ENROLAMENTO"] = True
            self.acionar_voip = True
        elif not self.leitura_alarme_temp_enrolamento_te and VOIP["TE_ALARME_TEMPERATURA_ENROLAMENTO"]:
            VOIP["TE_ALARME_TEMPERATURA_ENROLAMENTO"] = False

        self.leitura_alm_temp_enrolamento_te = LeituraOPCBit(self.client, REG_OPC["SE"]["TE_ALM_TEMPERATURA_ENROLAMENTO"], 2)
        if self.leitura_alm_temp_enrolamento_te and not VOIP["TE_ALM_TEMPERATURA_ENROLAMENTO"]:
            logger.warning("A temperatura do enrolamento do transformador elevador está alta. Favor verificar.")
            VOIP["TE_ALM_TEMPERATURA_ENROLAMENTO"] = True
            self.acionar_voip = True
        elif not self.leitura_alm_temp_enrolamento_te and VOIP["TE_ALM_TEMPERATURA_ENROLAMENTO"]:
            VOIP["TE_ALM_TEMPERATURA_ENROLAMENTO"] = False

        self.leitura_alarme_temperatura_oleo_te = LeituraOPCBit(self.client, REG_OPC["SE"]["TE_ALARME_TEMPERATURA_OLEO"], 18)
        if self.leitura_alarme_temperatura_oleo_te and not VOIP["TE_ALARME_TEMPERATURA_OLEO"]:
            logger.warning("A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            VOIP["TE_ALARME_TEMPERATURA_OLEO"] = True
            self.acionar_voip = True
        elif not self.leitura_alarme_temperatura_oleo_te and VOIP["TE_ALARME_TEMPERATURA_OLEO"]:
            VOIP["TE_ALARME_TEMPERATURA_OLEO"] = False

        self.leitura_alm_temperatura_oleo_te = LeituraOPCBit(self.client, REG_OPC["SE"]["TE_ALM_TEMPERATURA_OLEO"], 1)
        if self.leitura_alm_temperatura_oleo_te and not VOIP["TE_ALM_TEMPERATURA_OLEO"]:
            logger.warning("A temperatura do óleo do transformador elevador está alta. Favor verificar.")
            VOIP["TE_ALM_TEMPERATURA_OLEO"] = True
            self.acionar_voip = True
        elif not self.leitura_alm_temperatura_oleo_te and VOIP["TE_ALM_TEMPERATURA_OLEO"]:
            VOIP["TE_ALM_TEMPERATURA_OLEO"] = False

        self.leitura_nivel_oleo_muito_alto_te = LeituraOPCBit(self.client, REG_OPC["SE"]["TE_NIVEL_OLEO_MUITO_ALTO"], 26)
        if self.leitura_nivel_oleo_muito_alto_te and not VOIP["TE_NIVEL_OLEO_MUITO_ALTO"]:
            logger.warning("O nível do óleo do transformador elevador está muito alto. Favor verificar.")
            VOIP["TE_NIVEL_OLEO_MUITO_ALTO"] = True
            self.acionar_voip = True
        elif not self.leitura_nivel_oleo_muito_alto_te and VOIP["TE_NIVEL_OLEO_MUITO_ALTO"]:
            VOIP["TE_NIVEL_OLEO_MUITO_ALTO"] = False

        self.leitura_nivel_oleo_muito_baixo_te = LeituraOPCBit(self.client, REG_OPC["SE"]["TE_NIVEL_OLEO_MUITO_BAIXO"], 27)
        if self.leitura_nivel_oleo_muito_baixo_te and not VOIP["TE_NIVEL_OLEO_MUITO_BAIXO"]:
            logger.warning("O nível de óleo do tranformador elevador está muito baixo. Favor verificar.")
            VOIP["TE_NIVEL_OLEO_MUITO_BAIXO"] = True
            self.acionar_voip = True
        elif not self.leitura_nivel_oleo_muito_baixo_te and VOIP["TE_NIVEL_OLEO_MUITO_BAIXO"]:
            VOIP["TE_NIVEL_OLEO_MUITO_BAIXO"] = False

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    https://stackoverflow.com/questions/2953462/pinging-servers-in-python
    """
    ping = False
    for i in range(2):
        ping = ping or (subprocess.call(["ping", "-c", "1", "-w", "1", host], stdout=subprocess.PIPE) == 0)
        if not ping:
            pass
    return ping
