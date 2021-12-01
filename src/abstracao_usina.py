import logging
from time import sleep
import pyodbc

from datetime import date, datetime, timedelta
from cmath import sqrt

from pyModbusTCP.server import DataBank

from field_connector import FieldConnector

logger = logging.getLogger('__main__')

AGENDAMENTO_INDISPONIBILIZAR = 1
AGENDAMENTO_ALETRAR_NV_ALVO = 2
AGENDAMENTO_INDISPONIBILIZAR_UG_1 = 101
AGENDAMENTO_ALETRAR_POT_ALVO_UG_1 = 102
AGENDAMENTO_INDISPONIBILIZAR_UG_2 = 201
AGENDAMENTO_ALETRAR_POT_ALVO_UG_2 = 202
AGENDAMENTO_DISPARAR_MENSAGEM_TESTE = 777
MODO_ESCOLHA_MANUAL = 2


class Usina:

    def __init__(self, cfg=None, db=None, con=None):

        if not cfg or not db:
            raise ValueError
        else:
            self.cfg = cfg
            self.db = db

        if not con:
            self.con = FieldConnector(self.cfg)
        else:
            self.con = con

        self.state_moa = 1

        # Inicializa Objs da usina
        self.ug1 = UnidadeDeGeracao(1, self.con)
        self.ug2 = UnidadeDeGeracao(2, self.con)
        self.ugs = [self.ug1, self.ug2]
        self.comporta = Comporta(self.con)
        self.avisado_em_eletrica = False

        # Define as vars inciais
        self.clp_online = False
        self.timeout_padrao = self.cfg['timeout_padrao']
        self.timeout_emergencia = self.cfg['timeout_emergencia']
        self.nv_fundo_reservatorio = self.cfg['nv_fundo_reservatorio']
        self.nv_minimo = self.cfg['nv_minimo']
        self.nv_maximo = self.cfg['nv_maximo']
        self.nv_maximorum = self.cfg['nv_maximorum']
        self.nv_alvo = self.cfg['nv_alvo']
        self.kp = self.cfg['kp']
        self.ki = self.cfg['ki']
        self.kd = self.cfg['kd']
        self.kie = self.cfg['kie']
        self.kimedidor = 0
        self.controle_ie = self.cfg['saida_ie_inicial']
        self.n_movel_l = self.cfg['n_movel_L']
        self.n_movel_r = self.cfg['n_movel_R']

        # Outras vars
        self.ts_ultima_tesntativa_de_normalizacao = datetime.now()
        self.state_moa = 0
        self.controle_p = 0
        self.controle_i = 0
        self.controle_d = 0
        self.clp_emergencia_acionada = 0
        self.db_emergencia_acionada = 0
        self.nv_montante = 0
        self.pot_medidor = 0
        self.modo_autonomo = 1
        self.modo_de_escolha_das_ugs = 0
        self.nv_montante_recente = 0
        self.nv_montante_recentes = []
        self.nv_montante_anterior = 0
        self.nv_montante_anteriores = []
        self.erro_nv = 0
        self.erro_nv_anterior = 0
        self.aguardando_reservatorio = 0
        self.pot_disp = 0
        self.agendamentos_atrasados = 0
        self.deve_tentar_normalizar = True
        self.tentativas_de_normalizar = 0

        pars = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        self.kp,
                        self.ki,
                        self.kd,
                        self.kie,
                        self.n_movel_l,
                        self.n_movel_r,
                        self.nv_alvo
                        ]
        self.con.open()
        self.db.update_parametros_usina(pars)

    def ler_valores(self):

        # CLP
        # regs = [0]*40000
        # aux = self.clp.read_sequential(40000, 101)
        # regs += aux
        # USN
        # self.clp_emergencia_acionada = regs[self.cfg['ENDERECO_CLP_USINA_FLAGS']]
        # self.nv_montante = round((regs[self.cfg['ENDERECO_CLP_NV_MONATNTE']] * 0.001) + 620, 2)
        # self.pot_medidor = round((regs[self.cfg['ENDERECO_CLP_MEDIDOR']] * 0.001), 3)


        #self.con.open()
        self.clp_online = True
        self.clp_emergencia_acionada = self.con.get_emergencia_acionada()
        self.nv_montante = self.con.get_nv_montante()
        self.pot_medidor = self.con.get_pot_medidor()
        self.tensao_na_linha = self.con.get_tensao_na_linha()
        if self.tensao_na_linha < 30000 and self.modo_autonomo == 1 and not self.clp_emergencia_acionada:
            self.clp_emergencia_acionada = True
        # UG1
        self.ug1.flag = self.con.get_flag_ug1()
        self.ug1.sincronizada = self.con.get_sincro_ug1()
        self.ug1.potencia = self.con.get_potencia_ug1()
        self.ug1.potencia_minima = self.cfg['pot_minima']
        self.ug1.horas_maquina = self.con.get_horas_ug1()
        self.ug1.perda_na_grade = self.con.get_perda_na_grade_ug1()
        self.ug1.temp_mancal = self.con.get_temperatura_do_mancal_ug1()
        # Ug2
        self.ug2.flag = self.con.get_flag_ug2()
        self.ug2.sincronizada = self.con.get_sincro_ug2()
        self.ug2.potencia = self.con.get_potencia_ug2()
        self.ug2.potencia_minima = self.cfg['pot_minima']
        self.ug2.horas_maquina = self.con.get_horas_ug2()
        self.ug2.perda_na_grade = self.con.get_perda_na_grade_ug2()
        self.ug2.temp_mancal = self.con.get_temperatura_do_mancal_ug2()

        if self.con.get_flag_falha52L():
            self.acionar_emergencia()

        #self.con.close()

        if self.nv_montante_recente < 1:
            self.nv_montante_recentes = [self.nv_montante] * int(self.n_movel_r)
            self.nv_montante_anteriores = [self.nv_montante] * int(self.n_movel_l)
        self.nv_montante_recentes.append(self.nv_montante)
        self.nv_montante_recentes = self.nv_montante_recentes[1:]
        self.nv_montante_recente = sum(self.nv_montante_recentes) / self.cfg['n_movel_R']
        self.nv_montante_anteriores.append(self.nv_montante)
        self.nv_montante_anteriores = self.nv_montante_anteriores[1:]
        self.nv_montante_anterior = sum(self.nv_montante_anteriores) / self.cfg['n_movel_L']
        self.erro_nv = self.nv_montante_recente - self.nv_alvo
        self.erro_nv_anterior = self.nv_montante_anterior - self.nv_alvo

        # DB
        #
        # Ler apenas os parametros que estao disponiveis no django
        #  - Botão de emergência
        #  - Limites de operação das UGS
        #  - Modo autonomo
        #  - Modo de prioridade UGS
        #  - Niveis de operação da comporta

        parametros = self.db.get_parametros_usina()

        # Botão de emergência
        self.db_emergencia_acionada = int(parametros["emergencia_acionada"])

        # Limites de operação das UGS
        # UG1
        self.ug1.perda_na_grade_alerta = float(parametros["ug1_perda_grade_alerta"])
        self.ug1.perda_na_grade_max = float(parametros["ug1_perda_grade_maxima"])
        self.ug1.prioridade = int(parametros["ug1_prioridade"])
        self.ug1.temp_mancal_alerta = float(parametros["ug1_temp_alerta"])
        self.ug1.temp_mancal_max = float(parametros["ug1_temp_maxima"])
        # UG2
        self.ug2.perda_na_grade_alerta = float(parametros["ug2_perda_grade_alerta"])
        self.ug2.perda_na_grade_max = float(parametros["ug2_perda_grade_maxima"])
        self.ug2.prioridade = int(parametros["ug2_prioridade"])
        self.ug2.temp_mancal_alerta = float(parametros["ug2_temp_alerta"])
        self.ug2.temp_mancal_max = float(parametros["ug2_temp_maxima"])

        # nv_minimo
        self.nv_minimo = float(parametros["nv_minimo"])

        # Modo autonomo
        logging.debug("Modo autonomo que o banco respondeu: {}".format(int(parametros["modo_autonomo"])))
        self.modo_autonomo = int(parametros["modo_autonomo"])
        # Modo de prioridade UGS
        if not self.modo_de_escolha_das_ugs == int(parametros["modo_de_escolha_das_ugs"]):
            self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
            logger.info("O modo de prioridade das ugs foi alterado (#{}).".format(self.modo_de_escolha_das_ugs))

        # Niveis de operação da comporta
        # self.comporta.pos_0['anterior'] = float(parametros["nv_comporta_pos_0_ant"])
        self.comporta.pos_0['proximo'] = float(parametros["nv_comporta_pos_0_prox"])
        self.comporta.pos_1['anterior'] = float(parametros["nv_comporta_pos_1_ant"])
        self.comporta.pos_1['proximo'] = float(parametros["nv_comporta_pos_1_prox"])
        self.comporta.pos_2['anterior'] = float(parametros["nv_comporta_pos_2_ant"])
        self.comporta.pos_2['proximo'] = float(parametros["nv_comporta_pos_2_prox"])
        self.comporta.pos_3['anterior'] = float(parametros["nv_comporta_pos_3_ant"])
        self.comporta.pos_3['proximo'] = float(parametros["nv_comporta_pos_3_prox"])
        self.comporta.pos_4['anterior'] = float(parametros["nv_comporta_pos_4_ant"])
        self.comporta.pos_4['proximo'] = float(parametros["nv_comporta_pos_4_prox"])
        self.comporta.pos_5['anterior'] = float(parametros["nv_comporta_pos_5_ant"])
        # self.comporta.pos_5['proximo'] = float(parametros["nv_comporta_pos_5_prox"])

        # Parametros banco
        self.nv_alvo = float(parametros['nv_alvo'])
        self.kp = float(parametros['kp'])
        self.ki = float(parametros['ki'])
        self.kd = float(parametros['kd'])
        self.kie = float(parametros['kie'])
        self.n_movel_l = float(parametros['n_movel_L'])
        self.n_movel_r = float(parametros['n_movel_R'])

        # Le o databank interno
        
        if DataBank.get_words(self.cfg['REG_MOA_IN_EMERG'])[0] != 0:
            if not self.avisado_em_eletrica:
                self.avisado_em_eletrica = True
                logger.warning("Emergência elétrica detectada ler coils de alarme...")
        else:
            self.avisado_em_eletrica = False

        if DataBank.get_words(self.cfg['REG_MOA_IN_HABILITA_AUTO'])[0] == 1:
            DataBank.set_words(self.cfg['REG_MOA_IN_HABILITA_AUTO'], [0])
            DataBank.set_words(self.cfg['REG_MOA_IN_DESABILITA_AUTO'], [0])
            self.modo_autonomo = 1
        
        if DataBank.get_words(self.cfg['REG_MOA_IN_DESABILITA_AUTO'])[0] == 1 or self.modo_autonomo == 0:
            DataBank.set_words(self.cfg['REG_MOA_IN_HABILITA_AUTO'], [0])
            DataBank.set_words(self.cfg['REG_MOA_IN_DESABILITA_AUTO'], [0])
            self.modo_autonomo = 0
            self.entrar_em_modo_manual()

        # ajuste inicial ie
        if self.controle_ie == 'auto':
            self.controle_ie = (self.ug1.potencia + self.ug2.potencia) / self.cfg['pot_maxima_alvo']

        self.heartbeat()


    def escrever_valores(self):
        
        # CLP
        #self.con.open()           
        self.con.set_pos_comporta(int(self.comporta.pos_comporta))

        # DB
        # Escreve no banco
        # Paulo: mover lógica de escrever no banco para um método em DBService
        valores = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                1 if self.aguardando_reservatorio else 0,
                1 if self.clp_online else 0,
                self.nv_montante,
                self.pot_disp,
                1 if self.ug1.disponivel else 0,
                self.ug1.potencia,
                self.ug1.setpoint,
                1 if self.ug1.sincronizada else 0,
                self.ug1.horas_maquina,
                1 if self.ug2.disponivel else 0,
                self.ug2.potencia,
                self.ug2.setpoint,
                1 if self.ug2.sincronizada else 0,
                self.ug2.horas_maquina,
                self.comporta.pos_comporta,
                self.ug1.perda_na_grade,
                self.ug1.temp_mancal,
                self.ug2.perda_na_grade,
                self.ug2.temp_mancal,
                ]
        self.db.update_valores_usina(valores)

    def acionar_emergencia(self):
        #self.con.open()        
        self.con.acionar_emergencia()
        #self.con.close()
        self.clp_emergencia_acionada = 1


    def normalizar_emergencia(self):
        
        logger.info("Verificando condições para normalização")
        
        logger.info("Ultima tentativa: {}. Tensão na linha: {:2.1f}kV.".format(self.ts_ultima_tesntativa_de_normalizacao, self.tensao_na_linha/1000))

        if not (self.cfg['TENSAO_LINHA_BAIXA'] < self.tensao_na_linha < self.cfg['TENSAO_LINHA_ALTA']):
           logger.warn("Tensão na linha fora do limite." )
        elif self.deve_tentar_normalizar \
            and (datetime.now() - self.ts_ultima_tesntativa_de_normalizacao).seconds >= 60 * self.tentativas_de_normalizar:
            self.tentativas_de_normalizar += 1
            self.ts_ultima_tesntativa_de_normalizacao = datetime.now()
            logger.info("Normalizando a Usina")
            #self.con.open()
            self.con.normalizar_emergencia()
            #self.con.close()
            self.clp_emergencia_acionada = 0
            logger.info("Normalizando as UGS")
            for ug in self.ugs:
                ug.normalizar()
            logger.info("Normalizando no banco")
            self.db.update_remove_emergencia()
            self.db_emergencia_acionada = 0
            return True
        else:
            return False
            
    def heartbeat(self):

        ts = datetime.now().timestamp()
        try:
            logger.debug("Inserting in db")
            ma = 1 if self.modo_autonomo else 0
            self.db.insert_debug(ts, self.kp, self.ki, self.kd, self.kie, self.controle_p, self.controle_i, self.controle_d, self.controle_ie,
                                self.ug1.setpoint, self.ug1.potencia, self.ug2.setpoint, self.ug2.potencia, self.nv_montante_recente, self.erro_nv, ma)
        except Exception as e:
            pass

        agora = datetime.now()
        ano = int(agora.year)
        mes = int(agora.month)
        dia = int(agora.day)
        hor = int(agora.hour)
        mnt = int(agora.minute)
        seg = int(agora.second)
        mil = int(agora.microsecond / 1000)
        DataBank.set_words(0, [ano, mes, dia, hor, mnt, seg, mil])
        DataBank.set_words(self.cfg['REG_MOA_OUT_STATUS'], [self.state_moa])
        DataBank.set_words(self.cfg['REG_MOA_OUT_MODE'], [self.modo_autonomo])
        if self.modo_autonomo:
            DataBank.set_words(self.cfg['REG_MOA_OUT_EMERG'], [1 if self.clp_emergencia_acionada else 0])
            DataBank.set_words(self.cfg['REG_MOA_OUT_TARGET_LEVEL'], [self.nv_alvo-620]*1000)
            DataBank.set_words(self.cfg['REG_MOA_OUT_SETPOINT'], [self.ug1.setpoint + self.ug2.setpoint])
            DataBank.set_words(self.cfg['REG_MOA_OUT_BLOCK_UG1'], [1 if self.ug1.flag and self.clp_emergencia_acionada else 0])
            DataBank.set_words(self.cfg['REG_MOA_OUT_BLOCK_UG2'], [1 if self.ug2.flag and self.clp_emergencia_acionada else 0])
        else:
            DataBank.set_words(self.cfg['REG_MOA_OUT_EMERG'], [0])
            DataBank.set_words(self.cfg['REG_MOA_OUT_TARGET_LEVEL'], [0])
            DataBank.set_words(self.cfg['REG_MOA_OUT_SETPOINT'], [0])
            DataBank.set_words(self.cfg['REG_MOA_OUT_BLOCK_UG1'], [0])
            DataBank.set_words(self.cfg['REG_MOA_OUT_BLOCK_UG2'], [0])

    def get_agendamentos_pendentes(self):
        """
        Retorna os agendamentos pendentes para a usina.
        :return: list[] agendamentos
        
        agora = datetime.now()
        agora = agora - timedelta(seconds=agora.second, microseconds=agora.microsecond)
        """
        agendamentos_pendentes = []
        agendamentos = self.db.get_agendamentos_pendentes()
        for agendamento in agendamentos:
            ag = list(agendamento)
            ag[1] = ag[1] - timedelta(0, 60*60*3)
            agendamentos_pendentes.append(ag)
        return agendamentos_pendentes

    def verificar_agendamentos(self):
        """
        Verifica os agendamentos feitos pelo django no banco de dados e lida com eles, executando, etc...
        """
        agora = datetime.now()
        agendamentos = self.get_agendamentos_pendentes()
        
        logger.debug(agendamentos)

        if len(agendamentos) == 0:
            return True

        self.agendamentos_atrasados = 0
        for agendamento in agendamentos:
            if agora > agendamento[1]:
                segundos_passados = (agora - agendamento[1]).seconds
                logger.debug(segundos_passados)
                if segundos_passados > 60:
                    logger.warning("Agendamento #{} Atrasado! ({} - {}).".format(agendamento[0], agendamento[3], agendamento))
                    self.agendamentos_atrasados += 1
                if segundos_passados > 300 or self.agendamentos_atrasados > 3:
                    logger.info("Os agendamentos estão muito atrasados! Acionando emergência.")
                    self.acionar_emergencia()
                    return False
            else:
                segundos_adiantados = (agendamento[1]-agora).seconds
                if segundos_adiantados <= 60 and not bool(agendamento[4]):
                    # Está na hora e ainda não foi executado. Executar!
                    logger.info("Executando gendamento #{} - {}.".format(agendamento[0], agendamento))

                    # Exemplo Case agendamento:
                    if agendamento[3] == AGENDAMENTO_DISPARAR_MENSAGEM_TESTE:
                        # Coloca em emergência
                        logger.info("Disparando mensagem teste (comando via agendamento).")
                        self.disparar_mensagem_teste()

                    if agendamento[3] == AGENDAMENTO_INDISPONIBILIZAR:
                        # Coloca em emergência
                        logger.info("Indisponibilizando a usina (comando via agendamento).")
                        for ug in self.ugs:
                            ug.indisponibilizar()
                        while not self.ugs[0].parado and not self.ugs[1].parado:
                            self.ler_valores()
                            logger.debug("Indisponibilizando Usina... \n(freezing for 10 seconds)")
                            sleep(10)
                        self.acionar_emergencia()
                    
                    if agendamento[3] == AGENDAMENTO_ALETRAR_NV_ALVO:
                        try:
                            novo = float(agendamento[2].replace(",", "."))
                        except Exception as e:
                            logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))
                        self.nv_alvo = novo
                        pars = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            self.kp,
                            self.ki,
                            self.kd,
                            self.kie,
                            self.n_movel_l,
                            self.n_movel_r,
                            self.nv_alvo
                            ]
                        self.db.update_parametros_usina(pars)
                        self.escrever_valores()
                    
                    if agendamento[3] == AGENDAMENTO_ALETRAR_POT_ALVO_UG_1:
                        try:
                            novo = float(agendamento[2].replace(",", "."))
                        except Exception as e:
                            logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))
                        self.ug1.pot_disponivel = novo
                    
                    if agendamento[3] == AGENDAMENTO_INDISPONIBILIZAR_UG_1:
                        self.ug1.indisponibilizar()   
        
                    if agendamento[3] == AGENDAMENTO_ALETRAR_POT_ALVO_UG_2:
                        try:
                            novo = float(agendamento[2].replace(",", "."))
                        except Exception as e:
                            logger.info("Valor inválido no comando #{} ({} é inválido).".format(agendamento[0], agendamento[3]))
                        self.ug2.pot_disponivel = novo
                    
                    if agendamento[3] == AGENDAMENTO_INDISPONIBILIZAR_UG_2:
                        self.ug2.indisponibilizar()   


                    # Após executar, indicar no banco de dados
                    self.db.update_agendamento(int(agendamento[0]), 1)
                    logger.info("O comando #{} - {} foi executado.".format(agendamento[0], agendamento[2]))
                    self.escrever_valores()

    def distribuir_potencia(self, pot_alvo):

        if pot_alvo < 0.1:
            for ug in self.ugs:
                ug.mudar_setpoint(0)
                ug.parar()
            return True

        self.pot_disp = 0
        if self.ug1.disponivel:
            self.pot_disp += self.cfg['pot_maxima_ug']
        if self.ug2.disponivel:
            self.pot_disp += self.cfg['pot_maxima_ug']

        if self.pot_medidor > self.cfg['pot_maxima_alvo'] and pot_alvo > (self.cfg['pot_maxima_alvo'] * 0.95):
            self.kimedidor += - 0.0001 * (pot_alvo - self.pot_medidor) 
            pot_alvo = pot_alvo - 0.5 * (pot_alvo - self.pot_medidor) + self.kimedidor

        ugs = self.lista_de_ugs_disponiveis()
        
        if ugs is None:
            return False
        elif len(ugs) == 0:
            return False
        elif len(ugs) == 1:
            pot_alvo = min(pot_alvo, self.cfg['pot_maxima_ug'])
            ugs[0].mudar_setpoint(pot_alvo)
            return False
        else:

            logger.debug("Distribuindo {}".format(pot_alvo))
            if 0.1 < pot_alvo < self.cfg['pot_minima']:
                logger.debug("0.1 < {} < self.cfg['pot_minima']".format(pot_alvo))
                if len(ugs) > 0:
                    ugs[0].mudar_setpoint(self.cfg['pot_minima'])
                    for ug in ugs[1:]:
                        ug.mudar_setpoint(0)
            else:
                pot_alvo = min(pot_alvo, self.pot_disp)
                logger.debug("Alvo =  {}".format(pot_alvo))
                if self.ug1.sincronizada and self.ug2.sincronizada and pot_alvo > (2 * self.cfg['pot_minima']):
                    logger.debug("Dividir entre as ugs (cada = {})".format(pot_alvo / len(ugs)))
                    for ug in ugs:
                        ug.mudar_setpoint(pot_alvo / len(ugs))

                elif ((pot_alvo > (self.cfg['pot_maxima_ug'] + self.cfg['margem_pot_critica']))
                        and (abs(self.erro_nv) > 0.02) and self.ug1.disponivel and self.ug2.disponivel):
                    ugs[0].mudar_setpoint(self.cfg['pot_maxima_ug'])
                    for ug in ugs[1:]:
                            ug.mudar_setpoint(pot_alvo/len(ugs))
                
                elif pot_alvo < self.cfg['pot_maxima_ug'] - self.cfg['margem_pot_critica']:
                    logger.debug("{} < self.cfg['pot_maxima_ug'] - self.cfg['margem_pot_critica']".format(pot_alvo))
                    ugs[0].mudar_setpoint(pot_alvo)
                    for ug in ugs[1:]:
                        ug.mudar_setpoint(0)
                
                else:
                    pot_alvo = min(pot_alvo, self.cfg['pot_maxima_ug'])
                    if len(ugs) > 0:
                        for ug in ugs[1:]:
                            ug.mudar_setpoint(0)
                        ugs[0].mudar_setpoint(pot_alvo)
                
                for ug in self.ugs:
                    logger.debug("UG{} SP:{}".format(ug.id_da_ug, ug.setpoint))

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
            ls = sorted(ls, key=lambda y: (not y.sincronizada, not y.setpoint, not y.prioridade, y.horas_maquina))
        else:
            # escolher por menor horas_maquina primeiro
            ls = sorted(ls, key=lambda y: (not y.sincronizada, not y.setpoint, y.horas_maquina, not y.prioridade,))
        return ls

    def controle_normal(self):
        """
        Controle PID
        https://en.wikipedia.org/wiki/PID_controller#Proportional
        """
        logger.debug("-------------------------------------------------")
        
        # Calcula PID
        logger.debug("Alvo: {:0.3f}, Recente: {:0.3f}, Anterior: {:0.3f}".format(self.nv_alvo, self.nv_montante_recente,
                                                                                 self.nv_montante_anterior))
        if abs(self.erro_nv) <= 0.01:
            self.controle_p = self.kp * 0.5 * self.erro_nv 
        else:
            self.controle_p = self.kp * self.erro_nv 
        self.controle_i = max(min((self.ki * self.erro_nv) + self.controle_i, 0.8), 0)
        self.controle_d = self.kd * (self.erro_nv - self.erro_nv_anterior)
        saida_pid = self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3)
        logger.debug("PID: {:0.3f} <-- P:{:0.3f} + I:{:0.3f} + D:{:0.3f}; ERRO={}".format(saida_pid, self.controle_p, self.controle_i,
                                                                            self.controle_d, self.erro_nv))

        # Calcula o integrador de estabilidade e limita
        self.controle_ie = max(min(saida_pid + self.controle_ie * self.kie, 1), 0)

        if self.nv_montante_recente >= (self.nv_maximo - 0.03):
            self.controle_ie = 1
            self.controle_i = min(max(self.controle_i, 0.8), self.controle_i)

        if self.nv_montante_recente <= (self.nv_minimo + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        logger.debug("IE: {:0.3f}".format(self.controle_ie))

        # Arredondamento e limitação
        pot_alvo = max(min(round(self.cfg['pot_maxima_usina'] * self.controle_ie, 5), self.cfg['pot_maxima_usina']),
                       self.cfg['pot_minima'])
        
        logger.debug("Pot alvo: {:0.3f}".format(pot_alvo))
        logger.debug("Nv alvo: {:0.3f}".format(self.nv_alvo))
        ts = datetime.now().timestamp()
        try:
            logger.debug("Inserting in db")
            ma = 1 if self.modo_autonomo else 0
            self.db.insert_debug(ts, self.kp, self.ki, self.kd, self.kie, self.controle_p, self.controle_i, self.controle_d, self.controle_ie,
                                self.ug1.setpoint, self.ug1.potencia, self.ug2.setpoint, self.ug2.potencia, self.nv_montante_recente, self.erro_nv, ma)
        except Exception as e:
            passlogger.debug("-------------------------------------------------")

        self.distribuir_potencia(pot_alvo)

    def disparar_mensagem_teste(self):
        logger.debug("Este e um teste!")
        logger.info("Este e um teste!")
        logger.warning("Este e um teste!")
        logger.error("Este e um teste!")
        logger.critical("Este e um teste!")

    def entrar_em_modo_manual(self):
        self.modo_autonomo = 0
        self.db.update_modo_manual()

class UnidadeDeGeracao:

    def __init__(self, id_ug, con):

        self.con = con
        self.deve_tentar_normalizar = True
        self.tentativas_de_normalizar = 0
        self.id_da_ug = id_ug
        self.flag = False
        self.disponivel = True
        self.horas_maquina = 0
        self.potencia = 0
        self.prioridade = 0
        self.temp_mancal = 0
        self.temp_mancal_max = 0
        self.perda_na_grade = 0
        self.perda_na_grade_max = 0
        self.setpoint = 0
        self.sincronizada = False
        self.perda_na_grade_alerta = 0
        self.temp_mancal_alerta = 0
        self.pot_disponivel = 0
        self.potencia_minima = 0
        self.ts_ultima_tesntativa_de_normalizacao = datetime.now()
        self.partir = True
        self.partindo = False
        self.parando = False
        self.parado = True


    def voltar_a_tentar_resetar(self):
        self.deve_tentar_normalizar = True
        self.tentativas_de_normalizar = 0

    def normalizar(self):
        logger.info("Normalização UG {}".format(self.id_da_ug))
        self.tentativas_de_normalizar += 1
        self.ts_ultima_tesntativa_de_normalizacao = datetime.now()
        self.flag = False
        #self.con.open()        
        self.con.normalizar_emergencia()           
        #self.con.close()        

    def parar(self):
        if self.id_da_ug == 1:
            #self.con.open()        
            self.con.parar_ug1()
            #self.con.close()        
        if self.id_da_ug == 2:
            self.con.parar_ug2() 
            

    def indisponibilizar(self):
        # Indisponibiliza a ug
        self.flag = True
        self.parando = True
        self.disponivel = False
        if self.id_da_ug == 1:
            #self.con.open()        
            self.con.parar_ug1()
            if self.parado:
                self.con.acionar_emergencia_ug1()
            #self.con.close()        
        if self.id_da_ug == 2:
            self.con.parar_ug2() 
            if self.parado:
                self.con.acionar_emergencia_ug2()

    def atualizar_estado(self):
        """
        Atualiza o estado da ug conforme as vars dela. Executa o "Comportamento" da ug.
        """
        if not self.parando:

            if self.flag and self.disponivel:
                logger.warning("UG {} indisponivel.".format(self.id_da_ug))
                self.disponivel = False

            if not self.flag and not self.disponivel:
                logger.info("UG {} disponivel.".format(self.id_da_ug))
                self.disponivel = True
                self.tentativas_de_normalizar = 0
                if not self.deve_tentar_normalizar:
                    self.deve_tentar_normalizar = True
                    logger.info("Comportamento de normalização automática ligado.")

            # todo Verificações

            if self.temp_mancal >= self.temp_mancal_max:
                self.indisponibilizar()

            if self.perda_na_grade >= self.perda_na_grade_max:
                self.indisponibilizar()

            if self.perda_na_grade < self.perda_na_grade_alerta \
                and self.flag \
                and self.deve_tentar_normalizar \
                and self.tentativas_de_normalizar <= 3  \
                and (datetime.now() - self.ts_ultima_tesntativa_de_normalizacao).seconds >= 60 * self.tentativas_de_normalizar: 
                logger.info("Tentativa de normalização #{:d}".format(self.tentativas_de_normalizar))
                self.normalizar()

            if self.tentativas_de_normalizar > 3 and self.deve_tentar_normalizar:
                self.deve_tentar_normalizar = False
                logger.info("Tentativas de normalização excedidas! MOA não irá mais tentar.")

            if self.id_da_ug == 1:
                self.parado = self.con.get_ug1_parada()
            if self.id_da_ug == 2:
                self.parado = self.con.get_ug2_parada()

            if self.parado:
                self.parando = False


    def mudar_setpoint(self, alvo):          

        alvo = max(alvo, 0)
        

        if self.temp_mancal > self.temp_mancal_max:
            alvo = 0
        elif self.perda_na_grade > self.perda_na_grade_max:
            alvo = 0
        else:
            if self.temp_mancal > self.temp_mancal_alerta:
                alvo *= sqrt(sqrt(
                    1 - ((self.temp_mancal - self.temp_mancal_alerta) /
                         (self.temp_mancal_max - self.temp_mancal_alerta))))
            if self.perda_na_grade > self.perda_na_grade_alerta:
                alvo *= sqrt(
                    sqrt(1 - ((self.perda_na_grade - self.perda_na_grade_alerta) / (
                        self.perda_na_grade_max - self.perda_na_grade_alerta))))
        self.setpoint = alvo.real
        if self.setpoint  < self.potencia_minima:
            self.setpoint  = 0

        logger.debug("UG{} Partindo:{}, Sincronizada:{}, Parada:{}".format(self.id_da_ug, self.partindo, self.sincronizada, self.parado))

        if self.parando:
            if self.id_da_ug == 1:
                self.parado = self.con.get_ug1_parada()
            if self.id_da_ug == 2:
                self.parado = self.con.get_ug2_parada()

            if self.parado:
                self.parando = False
                
        if self.setpoint < 1 and not self.partindo and not self.parado:
            self.parando = True
            if self.id_da_ug == 1:
                self.con.parar_ug1()  
            if self.id_da_ug == 2:
                self.con.parar_ug2()  
        elif not self.parando:
            if self.setpoint >= 1:
                
                if self.id_da_ug == 1:
                    if not self.sincronizada:
                        self.con.partir_ug1()
                        if not self.partindo:
                            logger.info("Partindo UG1")       
                        self.partindo = True
                    elif self.sincronizada:
                        self.partindo = False
                    self.con.set_ug1_setpoint(int(self.setpoint * 1000))
            
                if self.id_da_ug == 2:
                    if not self.sincronizada:
                        self.con.partir_ug2() 
                        if not self.partindo:
                            logger.info("Partindo UG2")  
                        self.partindo = True
                    elif self.sincronizada:
                        self.partindo = False
                    self.con.set_ug2_setpoint(int(self.setpoint * 1000))



class Comporta:

    def __init__(self, con):
        self.con = con
        self.pos_comporta = 0
        self.pos_0 = {'pos': 0, 'anterior': 0.0, 'proximo': 0.0}
        self.pos_1 = {'pos': 1, 'anterior': 0.0, 'proximo': 0.0}
        self.pos_2 = {'pos': 2, 'anterior': 0.0, 'proximo': 0.0}
        self.pos_3 = {'pos': 3, 'anterior': 0.0, 'proximo': 0.0}
        self.pos_4 = {'pos': 4, 'anterior': 0.0, 'proximo': 0.0}
        self.pos_5 = {'pos': 5, 'anterior': 0.0, 'proximo': 0.0}
        self.posicoes = [self.pos_0, self.pos_1, self.pos_2,
                         self.pos_3, self.pos_4, self.pos_5]

    def atualizar_estado(self, nv_montante):

        self.posicoes = [self.pos_0, self.pos_1, self.pos_2,
                            self.pos_3, self.pos_4, self.pos_5]

        if not 0 <= self.pos_comporta <= 5:
            raise IndexError("Pos comporta invalida {}".format(self.pos_comporta))

        estado_atual = self.posicoes[self.pos_comporta]
        pos_alvo = self.pos_comporta
        if nv_montante < self.pos_1['anterior']:
            pos_alvo = 0
        else:
            if nv_montante < estado_atual['anterior']:
                pos_alvo = self.pos_comporta - 1
            elif nv_montante >= estado_atual['proximo']:
                pos_alvo = self.pos_comporta + 1
            pos_alvo = min(max(0, pos_alvo), 5)
        if not pos_alvo == self.pos_comporta:
            logger.info("Mudança de setpoint da comprota para {} (atual:{})".format(pos_alvo, self.pos_comporta))
            self.pos_comporta = pos_alvo

        return pos_alvo
