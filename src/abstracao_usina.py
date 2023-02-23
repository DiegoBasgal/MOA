import pytz
import logging
import threading
import subprocess
from src.codes import *
from time import sleep, time
from src.Condicionadores import *
from src.UG1 import UnidadeDeGeracao1
from src.UG2 import UnidadeDeGeracao2
from pyModbusTCP.client import ModbusClient
from datetime import  datetime, timedelta

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
            from src.field_connector import FieldConnector
            self.con = FieldConnector(self.cfg)

        if leituras:
            self.leituras = leituras
        else:
            from src.Leituras import LeituraModbus
            from src.LeiturasUSN import LeiturasUSN
            from src.Leituras import LeituraModbusBit
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
        self.ug_operando = 0

        for ug in self.ugs:
            if ug.etapa_atual == UNIDADE_SINCRONIZADA:
                self.ug_operando += 1

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False

        self.tensao_ok = True
        self.timer_tensao = None
        self.TDA_Offline = False
        self.acionar_voip = False
        self.TDA_FalhaComum = False
        self.BombasDngRemoto = True
        self.avisado_em_eletrica = False
        self.Disj_GDE_QCAP_Fechado = False
        self.deve_tentar_normalizar = True
        self.deve_normalizar_forcado = False
        self.deve_ler_condicionadores = False

        self.clp_moa = ModbusClient(
            host=self.cfg["moa_slave_ip"],
            port=self.cfg["moa_slave_porta"],
            unit_id=1,
            timeout=0.5)

        self.clp = ModbusClient(
            host=self.cfg["USN_slave_ip"],
            port=self.cfg["USN_slave_porta"],
            timeout=0.5,
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

        self.cfg["cx_kp"] = float(parametros["cx_kp"])
        self.cfg["cx_ki"] = float(parametros["cx_ki"])
        self.cfg["cx_kie"] = float(parametros["cx_kie"])
        self.cfg["press_cx_alvo"] = float(parametros["press_cx_alvo"])

        # Le o CLP MOA
        if self.clp_moa.read_coils(self.cfg["REG_MOA_IN_EMERG"])[0] == 1 and self.avisado_em_eletrica==False:
            self.avisado_em_eletrica = True
            for ug in self.ugs:
                ug.deve_ler_condicionadores = True

        elif self.clp_moa.read_coils(self.cfg["REG_MOA_IN_EMERG"])[0] == 0 and self.avisado_em_eletrica==True:
            self.avisado_em_eletrica = False
            for ug in self.ugs:
                ug.deve_ler_condicionadores = False

        if self.clp_moa.read_coils(self.cfg["REG_MOA_IN_EMERG_UG1"])[0] == 1:
            self.ug1.deve_ler_condicionadores = True

        elif self.clp_moa.read_coils(self.cfg["REG_MOA_IN_EMERG_UG2"])[0] == 1:
            self.ug2.deve_ler_condicionadores = True

        else:
            for ug in self.ugs:
                ug.deve_ler_condicionadores = False
        
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

                ug.condicionador_temperatura_nucleo_gerador_2_ug.valor_base = float(parametros["alerta_temperatura_nucleo_gerador_2_ug{}".format(ug.id)])
                ug.condicionador_temperatura_nucleo_gerador_2_ug.valor_limite = float(parametros["limite_temperatura_nucleo_gerador_2_ug{}".format(ug.id)])

                ug.condicionador_temperatura_nucleo_gerador_3_ug.valor_base = float(parametros["alerta_temperatura_nucleo_gerador_3_ug{}".format(ug.id)])
                ug.condicionador_temperatura_nucleo_gerador_3_ug.valor_limite = float(parametros["limite_temperatura_nucleo_gerador_3_ug{}".format(ug.id)])

                ug.condicionador_temperatura_mancal_casq_rad_ug.valor_base = float(parametros["alerta_temperatura_mancal_casq_rad_ug{}".format(ug.id)])
                ug.condicionador_temperatura_mancal_casq_rad_ug.valor_limite = float(parametros["limite_temperatura_mancal_casq_rad_ug{}".format(ug.id)])

                ug.condicionador_temperatura_mancal_casq_comb_ug.valor_base = float(parametros["alerta_temperatura_mancal_casq_comb_ug{}".format(ug.id)])
                ug.condicionador_temperatura_mancal_casq_comb_ug.valor_limite = float(parametros["limite_temperatura_mancal_casq_comb_ug{}".format(ug.id)])

                ug.condicionador_temperatura_mancal_escora_comb_ug.valor_base = float(parametros["alerta_temperatura_mancal_escora_comb_ug{}".format(ug.id)])
                ug.condicionador_temperatura_mancal_escora_comb_ug.valor_limite = float(parametros["limite_temperatura_mancal_escora_comb_ug{}".format(ug.id)])

                ug.condicionador_caixa_espiral_ug.valor_base = float(parametros["alerta_caixa_espiral_ug{}".format(ug.id)])
                ug.condicionador_caixa_espiral_ug.valor_limite = float(parametros["limite_caixa_espiral_ug{}".format(ug.id)])

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
        self.clp_moa.write_multiple_registers(0, [ano, mes, dia, hor, mnt, seg, mil])
        self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_STATUS"], [self.state_moa])
        self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_MODE"], [self.modo_autonomo])

        if self.modo_autonomo == 1:
            self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_EMERG"], [1 if self.clp_emergencia_acionada else 0],)
            self.clp_moa.write_multiple_registers(self.cfg["REG_MOA_OUT_TARGET_LEVEL"], [int((self.cfg["nv_alvo"] - 820.9) * 1000)])
            self.clp_moa.write_multiple_registers(self.cfg["REG_MOA_OUT_SETPOINT"], [int(self.ug1.setpoint + self.ug2.setpoint)], )

            if self.avisado_em_eletrica==True and self.aux==1:
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG1"], [1],)
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG2"], [1],)
                self.aux=0
            elif self.avisado_em_eletrica==False and self.aux==0:
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG1"], [0],)
                self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG2"], [0],)
                self.aux=1

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
                        logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))

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
                        logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))

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
        self.ajuste_manual = 0

        logger.debug("lista_de_ugs_disponiveis:")
        for ug in ugs:
            logger.debug("UG{}".format(ug.id))
            self.pot_disp += ug.cfg["pot_maxima_ug{}".format(ugs[0].id)]
            if ug.manual:
                self.ajuste_manual += min(max(0, ug.leitura_potencia), 0)
        if ugs is None:
            return False
        elif len(ugs) == 0:
            return False

        logger.debug("Distribuindo {}".format(pot_alvo - self.ajuste_manual))

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
            if ug.disponivel and not ug.etapa_atual == UNIDADE_PARANDO:
                ls.append(ug)

        if self.modo_de_escolha_das_ugs == MODO_ESCOLHA_MANUAL:
            # escolher por maior prioridade primeiro
            ls = sorted(ls, key=lambda y: (-1 * y.leitura_potencia.valor, -1 * y.setpoint, y.prioridade,),)
        else:
            # escolher por menor horas_maquina primeiro
            ls = sorted(ls, key=lambda y: (y.leitura_horimetro.valor, -1 * y.leitura_potencia.valor, -1 * y.setpoint,),)
            print("")
            print(ls)
            print("")
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
        """
        
        #Lista de condicionadores essenciais que devem ser lidos a todo momento
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        self.leitura_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA = LeituraModbusCoil("EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA, )
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.leitura_EntradasDigitais_MXI_SA_SEL787_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_SEL787_Trip", self.clp, REG_SA_EntradasDigitais_MXI_SA_SEL787_Trip, )
        x = self.leitura_EntradasDigitais_MXI_SA_SEL787_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_SEL311_Trip = LeituraModbusCoil( "EntradasDigitais_MXI_SA_SEL311_Trip", self.clp, REG_SA_EntradasDigitais_MXI_SA_SEL311_Trip, )
        x = self.leitura_EntradasDigitais_MXI_SA_SEL311_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        # MRU3 é o relé de bloqueio 27/59N
        self.leitura_EntradasDigitais_MXI_SA_MRU3_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRU3_Trip", self.clp, REG_SA_EntradasDigitais_MXI_SA_MRU3_Trip, )
        x = self.leitura_EntradasDigitais_MXI_SA_MRU3_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        # MRL1 é o relé de bloqueio 86T
        self.leitura_EntradasDigitais_MXI_SA_MRL1_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRL1_Trip", self.clp, REG_SA_EntradasDigitais_MXI_SA_MRL1_Trip, )
        x = self.leitura_EntradasDigitais_MXI_SA_MRL1_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip, )
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip
        self.condicionadores_essenciais.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        
        #Lista de condiconadores que deverão ser lidos apenas quando houver uma chamada de leitura
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        if not self.TDA_Offline:
            self.leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETrip = LeituraModbusCoil("EntradasDigitais_MXI_TDA_QcataDisj52ETrip", self.clp, REG_TDA_EntradasDigitais_MXI_QcataDisj52ETrip, )
            x = self.leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETrip
            self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

            self.leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai = LeituraModbusCoil("EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai", self.clp, REG_TDA_EntradasDigitais_MXI_QcataDisj52ETripDisjSai, )
            x = self.leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai
            self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

            self.leitura_EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA = LeituraModbusCoil("EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA", self.clp, REG_TDA_EntradasDigitais_MXI_QcataDisj52EFalha380VCA, )
            x = self.leitura_EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA
            self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        # MRU3 é o relé de bloqueio 27/59N
        self.leitura_EntradasDigitais_MXI_SA_MRU3_Falha = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRU3_Falha", self.clp, REG_SA_EntradasDigitais_MXI_SA_MRU3_Falha, )
        x = self.leitura_EntradasDigitais_MXI_SA_MRU3_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_SEL787_FalhaInterna = LeituraModbusCoil( "EntradasDigitais_MXI_SA_SEL787_FalhaInterna", self.clp, REG_SA_EntradasDigitais_MXI_SA_SEL787_FalhaInterna, )
        x = self.leitura_EntradasDigitais_MXI_SA_SEL787_FalhaInterna
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_SEL311_Falha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_SEL311_Falha", self.clp, REG_SA_EntradasDigitais_MXI_SA_SEL311_Falha, )
        x = self.leitura_EntradasDigitais_MXI_SA_SEL311_Falha
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_CTE_Falta125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CTE_Falta125Vcc", self.clp, REG_SA_EntradasDigitais_MXI_SA_CTE_Falta125Vcc, )
        x = self.leitura_EntradasDigitais_MXI_SA_CTE_Falta125Vcc
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta", self.clp, REG_SA_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta, )
        x = self.leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas", self.clp, REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas, )
        x = self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo", self.clp, REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo, )
        x = self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao", self.clp, REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao, )
        x = self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeTempOleo", self.clp, REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo, )
        x = self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento = ( LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento", self.clp, REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento, ) )
        x = self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeDesligamento", self.clp, REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento, )
        x = self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_TE_Falha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_Falha", self.clp, REG_SA_EntradasDigitais_MXI_SA_TE_Falha, )
        x = self.leitura_EntradasDigitais_MXI_SA_TE_Falha
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsProt = LeituraModbusCoil( "EntradasDigitais_MXI_SA_FalhaDisjTPsProt", self.clp, REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsProt, )
        x = self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsProt
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr = LeituraModbusCoil( "EntradasDigitais_MXI_SA_FalhaDisjTPsSincr", self.clp, REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr, )
        x = self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CSA1_Secc_Aberta", self.clp, REG_SA_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta, )
        x = self.leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CSA1_FusivelQueimado", self.clp, REG_SA_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado, )
        x = self.leitura_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc", self.clp, REG_SA_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc, )
        x = self.leitura_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_QCADE_Nivel4 = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_Nivel4", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCADE_Nivel4, )
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_Nivel4
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto, )
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_QCADE_Falha220VCA = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_Falha220VCA", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCADE_Falha220VCA, )
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_Falha220VCA
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        # Verificar
        self.leitura_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCCP_Disj72ETrip", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip, )
        x = self.leitura_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCCP_Falta125Vcc", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc, )
        x = self.leitura_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup, )
        x = self.leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup 
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_Falta125Vcc", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc, )
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup, )
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha, )
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_Disj52EFalha", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha, )
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_EntradasDigitais_MXI_SA_GMG_DisjFechado = LeituraModbusCoil( "EntradasDigitais_MXI_SA_GMG_DisjFechado", self.clp, REG_SA_EntradasDigitais_MXI_SA_GMG_DisjFechado, )
        x = self.leitura_EntradasDigitais_MXI_SA_GMG_DisjFechado
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets = LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets", self.clp, REG_SA_RetornosAnalogicos_MWR_SEL787_Targets, )
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00", self.clp, REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00, ) )
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01", self.clp, REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01, ) )
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02", self.clp, REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02, ) )
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03", self.clp, REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03, ) )
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04", self.clp, REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04, ) )
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05", self.clp, REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05, ) )
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06", self.clp, REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06, ) )
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07", self.clp, REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07, ) )
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RetornosDigitais_MXR_DJ1_FalhaInt = LeituraModbusCoil( "RetornosDigitais_MXR_DJ1_FalhaInt", self.clp, REG_SA_RetornosDigitais_MXR_DJ1_FalhaInt, )
        x = self.leitura_RetornosDigitais_MXR_DJ1_FalhaInt
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RetornosDigitais_MXR_CLP_Falha = LeituraModbusCoil( "RetornosDigitais_MXR_CLP_Falha", self.clp, REG_SA_RetornosDigitais_MXR_CLP_Falha, )
        x = self.leitura_RetornosDigitais_MXR_CLP_Falha
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        return True
        """

    def leituras_por_hora(self):
        """
        self.leitura_EntradasDigitais_MXI_SA_QLCF_Disj52ETrip = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QLCF_Disj52ETrip", self.clp, REG_SA_EntradasDigitais_MXI_SA_QLCF_Disj52ETrip)
        if self.leitura_EntradasDigitais_MXI_SA_QLCF_Disj52ETrip.valor != 0:
            logger.warning("O Disjuntor do Gerador Diesel de Emergência QLCF identificou um sinal de TRIP, favor verificar.")
        
        self.leitura_EntradasDigitais_MXI_SA_QLCF_TripDisjAgrup = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QLCF_TripDisjAgrup", self.clp, REG_SA_EntradasDigitais_MXI_SA_QLCF_TripDisjAgrup)
        if self.leitura_EntradasDigitais_MXI_SA_QLCF_TripDisjAgrup.valor != 0:
            logger.warning("O sensor do Disjuntor de Agrupamento QLCF identificou um sinal de trip, favor verificar.")

        self.leitura_EntradasDigitais_MXI_SA_QCAP_SubtensaoBarraGeral = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_SubtensaoBarraGeral", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCAP_SubtensaoBarraGeral)
        if self.leitura_EntradasDigitais_MXI_SA_QCAP_SubtensaoBarraGeral.valor != 0:
            logger.warning("O sensor de Subtensão do Barramento Geral QCAP foi acionado, favor verificar.")

        self.leitura_EntradasDigitais_MXI_SA_GMG_Alarme = LeituraModbusCoil( "EntradasDigitais_MXI_SA_GMG_Alarme", self.clp, REG_SA_EntradasDigitais_MXI_SA_GMG_Alarme)
        if self.leitura_EntradasDigitais_MXI_SA_GMG_Alarme.valor != 0:
            logger.warning("O alarme do Grupo Motor Gerador foi acionado, favor verificar.")

        self.leitura_EntradasDigitais_MXI_SA_GMG_Trip = LeituraModbusCoil( "EntradasDigitais_MXI_SA_GMG_Trip", self.clp, REG_SA_EntradasDigitais_MXI_SA_GMG_Trip)
        if self.leitura_EntradasDigitais_MXI_SA_GMG_Trip.valor != 0:
            logger.warning("O sensor de TRIP do Grupo Motor Gerador foi acionado, favor verificar.")

        self.leitura_EntradasDigitais_MXI_SA_GMG_Operacao = LeituraModbusCoil( "EntradasDigitais_MXI_SA_GMG_Operacao", self.clp, REG_SA_EntradasDigitais_MXI_SA_GMG_Operacao)
        if self.leitura_EntradasDigitais_MXI_SA_GMG_Operacao.valor != 0:
            logger.warning("O sensor de operação do Grupo Motor Gerador foi acionado, favor verificar.")

        self.leitura_EntradasDigitais_MXI_SA_GMG_BaixoComb = LeituraModbusCoil( "EntradasDigitais_MXI_SA_GMG_BaixoComb", self.clp, REG_SA_EntradasDigitais_MXI_SA_GMG_BaixoComb)
        if self.leitura_EntradasDigitais_MXI_SA_GMG_BaixoComb.valor != 0:
            logger.warning("O sensor de de combustível do Grupo Motor Gerador, retornou que o nível está baixo, favor reabastercer o gerador.")
        
        self.leitura_RetornosDigitais_MXR_BbaDren1_FalhaAcion = LeituraModbusCoil( "RetornosDigitais_MXR_BbaDren1_FalhaAcion", self.clp, REG_SA_RetornosDigitais_MXR_BbaDren1_FalhaAcion)
        if self.leitura_RetornosDigitais_MXR_BbaDren1_FalhaAcion.valor != 0:
            logger.warning("O sensor da Bomba de Drenagem 1 identificou uma falha no acionamento, favor verificar.")

        self.leitura_RetornosDigitais_MXR_BbaDren2_FalhaAcion = LeituraModbusCoil( "RetornosDigitais_MXR_BbaDren2_FalhaAcion", self.clp, REG_SA_RetornosDigitais_MXR_BbaDren2_FalhaAcion)
        if self.leitura_RetornosDigitais_MXR_BbaDren2_FalhaAcion.valor != 0:
            logger.warning("O sensor da Bomba de Drenagem 2 identificou uma falha no acionamento, favor verificar.")
        
        self.leitura_RetornosDigitais_MXR_BbaDren3_FalhaAcion = LeituraModbusCoil( "RetornosDigitais_MXR_BbaDren3_FalhaAcion", self.clp, REG_SA_RetornosDigitais_MXR_BbaDren3_FalhaAcion)
        if self.leitura_RetornosDigitais_MXR_BbaDren3_FalhaAcion.valor != 0:
            logger.warning("O sensor da Bomba de Drenagem 3 identificou uma falha no acionamento, favor verificar.")
        
        self.leitura_RetornosDigitais_MXR_SA_GMG_FalhaAcion = LeituraModbusCoil( "RetornosDigitais_MXR_SA_GMG_FalhaAcion", self.clp, REG_SA_RetornosDigitais_MXR_SA_GMG_FalhaAcion)
        if self.leitura_RetornosDigitais_MXR_SA_GMG_FalhaAcion.valor != 0:
            logger.warning("O sensor do Grupo Motor Gerador identificou uma falha no acionamento, favor verificar.")
        
        self.leitura_RetornosDigitais_MXR_FalhaComunSETDA = LeituraModbusCoil( "RetornosDigitais_MXR_FalhaComunSETDA", self.clp, REG_SA_RetornosDigitais_MXR_FalhaComunSETDA)
        if self.leitura_RetornosDigitais_MXR_FalhaComunSETDA.valor != 0 and self.TDA_FalhaComum==False:
            logger.warning("Houve uma falha de comunicação com o CLP da Subestação e o CLP da Tomada da Água, favor verificar")
            self.TDA_FalhaComum = True
            self.acionar_voip = True
        elif self.leitura_RetornosDigitais_MXR_FalhaComunSETDA == 0 and self.TDA_FalhaComum == True:
            self.TDA_FalhaComum = False

        self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFechado = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_Disj52EFechado", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52EFechado)
        if self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFechado.valor == 1 and self.Disj_GDE_QCAP_Fechado==False:
            logger.warning("O Disjuntor do Gerador Diesel de Emergência QLCF foi fechado.")
            self.Disj_GDE_QCAP_Fechado = True
            self.acionar_voip = True
        elif self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFechado.valor == 0 and self.Disj_GDE_QCAP_Fechado==True:
            self.Disj_GDE_QCAP_Fechado = False

        self.leitura_EntradasDigitais_MXI_SA_QCADE_BombasDng_Auto = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_BombasDng_Auto", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCADE_BombasDng_Auto)
        if self.leitura_EntradasDigitais_MXI_SA_QCADE_BombasDng_Auto.valor == 0 and self.BombasDngRemoto==True:
            logger.warning("O poço de drenagem da Usina saiu do modo remoto, favor verificar.")
            self.BombasDngRemoto=False
            self.acionar_voip = True
        elif self.leitura_EntradasDigitais_MXI_SA_QCADE_BombasDng_Auto.valor == 1 and self.BombasDngRemoto==False:
            self.BombasDngRemoto=True

        return True
        """

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
