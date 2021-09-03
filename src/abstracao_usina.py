import json
import logging
import os
from datetime import datetime, timedelta
from cmath import sqrt
from time import sleep

from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import DataBank

from src.database_connector import Database

logger = logging.getLogger('__main__')


class Usina:

    def __init__(self):
        # Carrega o arquivo de configuração inicial
        config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_file, 'r') as file:
            self.cfg = json.load(file)

        # Inicializa Objs da usina
        self.ug1 = UnidadeDeGeracao(1)
        self.ug2 = UnidadeDeGeracao(2)
        self.ugs = [self.ug1, self.ug2]
        self.comporta = Comporta()

        # Define as vars inciais
        self.clp_online = False
        self.clp_ip = self.cfg['clp_ip']
        self.clp_porta = self.cfg['clp_porta']
        self.modbus_clp = ModbusClient(
            host=self.clp_ip,
            port=self.clp_porta,
            timeout=1, # Para debug colocar baixo (1s)
            unit_id=1,
            auto_open=True,
            auto_close=True)

        self.modbus_server_ip = self.cfg['moa_slave_ip']
        self.modbus_server_porta = self.cfg['moa_slave_porta']
        self.timeout_padrao = self.cfg['timeout_padrao']
        self.timeout_emergencia = self.cfg['timeout_emergencia']
        self.nv_minimo = self.cfg['nv_minimo']
        self.nv_maximo = self.cfg['nv_maximo']
        self.nv_religamento = self.cfg['nv_religamento']
        self.nv_alvo = self.cfg['nv_alvo']
        self.kp = self.cfg['kp']
        self.ki = self.cfg['ki']
        self.kd = self.cfg['kd']
        self.kie = self.cfg['kie']
        self.controle_ie = self.cfg['saida_ie_inicial']
        self.n_movel_L = self.cfg['n_movel_L']
        self.n_movel_R = self.cfg['n_movel_R']

        # Outras vars
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

        # Estabelece as conexões iniciais com CLP e DB
        try:
            self.ler_valores()
        except Exception as e:
            raise e

    def ler_valores(self):

        # CLP

        # Tenta abrir uma conexão
        if self.modbus_clp.open():
            # Se conectou, lê, fecha a conexão e atribui os vales certos.
            regs = self.modbus_clp.read_holding_registers(0, 101)
            if regs is None:
                # Se os regs estiverem vazios, a conexão falhou
                self.clp_online = False
                raise ConnectionError

            # USN
            self.clp_emergencia_acionada = regs[self.cfg['ENDERECO_CLP_USINA_FLAGS']]
            self.nv_montante = round((regs[self.cfg['ENDERECO_CLP_NV_MONATNTE']] * 0.001) + 620, 2)
            self.pot_medidor = round((regs[self.cfg['ENDERECO_CLP_MEDIDOR']] * 0.001), 3)
            self.clp_online = True
            if self.nv_montante_recente < 1:
                self.nv_montante_recentes = [self.nv_montante] * self.n_movel_R
                self.nv_montante_anteriores = [self.nv_montante] * self.n_movel_L
            self.nv_montante_recentes.append(self.nv_montante)
            self.nv_montante_recentes = self.nv_montante_recentes[1:]
            self.nv_montante_recente = sum(self.nv_montante_recentes) / self.cfg['n_movel_R']
            self.nv_montante_anteriores.append(self.nv_montante)
            self.nv_montante_anteriores = self.nv_montante_anteriores[1:]
            self.nv_montante_anterior = sum(self.nv_montante_anteriores) / self.cfg['n_movel_L']
            self.erro_nv = self.nv_alvo - self.nv_montante_recente
            self.erro_nv_anterior = self.nv_alvo - self.nv_montante_anterior

            # UG1
            self.ug1.flag = int(regs[self.cfg['ENDERECO_CLP_UG1_FLAGS']])
            self.ug1.potencia = int(regs[self.cfg['ENDERECO_CLP_UG1_POTENCIA']]) / 1000
            self.ug1.horas_maquina = int(regs[self.cfg['ENDERECO_CLP_UG1_MINUTOS']]) / 60
            self.ug1.perda_na_grade = int(regs[self.cfg['ENDERECO_CLP_UG1_PERGA_GRADE']]) / 100
            self.ug1.temp_mancal = int(regs[self.cfg['ENDERECO_CLP_UG1_T_MANCAL']]) / 10

            # Ug2
            self.ug2.flag = int(regs[self.cfg['ENDERECO_CLP_UG2_FLAGS']])
            self.ug2.potencia = int(regs[self.cfg['ENDERECO_CLP_UG2_POTENCIA']]) / 1000
            self.ug2.horas_maquina = int(regs[self.cfg['ENDERECO_CLP_UG2_MINUTOS']]) / 60
            self.ug2.perda_na_grade = int(regs[self.cfg['ENDERECO_CLP_UG2_PERGA_GRADE']]) / 100
            self.ug2.temp_mancal = int(regs[self.cfg['ENDERECO_CLP_UG2_T_MANCAL']]) / 10

            self.modbus_clp.close()

        else:
            # Se não conectou, a clp não está online.
            self.clp_online = False
            raise ConnectionError

        # DB
        #
        # Ler apenas os parametros que estao disponiveis no django
        #  - Botão de emergência
        #  - Limites de operação das UGS
        #  - Modo autonomo
        #  - Modo de prioridade UGS
        #  - Niveis de operação da comporta
        
        parametros = {}
        try:
            with Database() as db:
                parametros = db.get_parametros_usina()
        except Exception as e:
            raise e
        
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

        # Modo autonomo
        self.modo_autonomo = int(parametros["modo_autonomo"])

        # Modo de prioridade UGS
        if not self.modo_de_escolha_das_ugs == int(parametros["modo_de_escolha_das_ugs"]):
            self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
            logger.info("O modo de prioridade na escolha das ugs foi alterado (#{}).".format(self.modo_de_escolha_das_ugs))

        # Niveis de operação da comporta
        self.comporta.pos_0['anterior'] = float(parametros["nv_comporta_pos_0_ant"])
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
        self.comporta.pos_5['proximo'] = float(parametros["nv_comporta_pos_5_prox"])

        # Parametros banco
        self.kp = float(parametros['kp'])
        self.ki = float(parametros['ki'])
        self.kd = float(parametros['kd'])
        self.kie = float(parametros['kie'])
        self.n_movel_L = float(parametros['n_movel_L'])
        self.n_movel_R = float(parametros['n_movel_R'])

    def escrever_valores(self):

        # CLP
        if self.modbus_clp.open():


            # UG1
            self.modbus_clp.write_single_register(self.cfg['ENDERECO_CLP_UG1_FLAGS'], self.ug1.flag)
            self.modbus_clp.write_single_register(self.cfg['ENDERECO_CLP_UG1_SETPOINT'], int(self.ug1.setpoint * 1000))

            # UG2
            self.modbus_clp.write_single_register(self.cfg['ENDERECO_CLP_UG2_FLAGS'], self.ug2.flag)
            self.modbus_clp.write_single_register(self.cfg['ENDERECO_CLP_UG2_SETPOINT'], int(self.ug2.setpoint * 1000))

            # Comporta
            self.modbus_clp.write_single_register(self.cfg['ENDERECO_CLP_COMPORTA_POS'], int(self.comporta.pos_comporta))

            self.modbus_clp.close()

        else:
            # Se não conectou, a clp não está online.
            self.clp_online = False
            raise ConnectionError

        # DB
        # Escreve no banco
        with Database() as db:
            q = """ UPDATE parametros_moa_parametrosusina
                     SET
                     timestamp = '{}',
                     aguardando_reservatorio = {},
                     clp_online = {},
                     nv_montante = {},
                     pot_disp = {},
                     ug1_disp = {},
                     ug1_pot = {},
                     ug1_setpot = {},
                     ug1_sinc = {},
                     ug1_tempo = {},
                     ug2_disp = {},
                     ug2_pot = {},
                     ug2_setpot = {},
                     ug2_sinc = {},
                     ug2_tempo = {},
                     pos_comporta = {},
                     ug1_perda_grade = {},
                     ug1_temp_mancal = {},
                     ug2_perda_grade = {},
                     ug2_temp_mancal = {}        
                     WHERE id = 1; 
                     """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
                                )
            db.execute(q)

    def acionar_emergencia_clp(self):
        if self.modbus_clp.open():
            self.modbus_clp.write_single_register(self.cfg['ENDERECO_CLP_USINA_FLAGS'], int(1))
            self.modbus_clp.close()
        else:
            # Se não conectou, a clp não está online.
            self.clp_online = False
            raise ConnectionError

    def normalizar_emergencia_clp(self):
        if self.modbus_clp.open():
            self.modbus_clp.write_single_register(self.cfg['ENDERECO_CLP_USINA_FLAGS'], int(0))
            self.modbus_clp.close()
        else:
            # Se não conectou, a clp não está online.
            self.clp_online = False
            raise ConnectionError

    def heartbeat(self):
        agora = datetime.now()
        ano = int(agora.year)
        mes = int(agora.month)
        dia = int(agora.day)
        hor = int(agora.hour)
        mnt = int(agora.minute)
        seg = int(agora.second)
        mil = int(agora.microsecond / 1000)
        DataBank.set_words(0, [ano, mes, dia, hor, mnt, seg, mil])
        DataBank.set_words(self.cfg['ENDERECO_LOCAL_NV_MONATNTE'], [int((self.nv_montante - 620) * 1000)])
        DataBank.set_words(self.cfg['ENDERECO_LOCAL_NV_ALVO'], [int((self.nv_alvo - 620) * 1000)])
        DataBank.set_words(self.cfg['ENDERECO_LOCAL_NV_RELIGAMENTO'], [int((self.nv_religamento - 620) * 1000)])
        DataBank.set_words(self.cfg['ENDERECO_LOCAL_UG1_POT'], [int(self.ug1.potencia * 1000)])
        DataBank.set_words(self.cfg['ENDERECO_LOCAL_UG1_SETPOINT'], [int(self.ug1.setpoint * 1000)])
        DataBank.set_words(self.cfg['ENDERECO_LOCAL_UG1_DISP'], [int(self.ug1.disponivel)])
        DataBank.set_words(self.cfg['ENDERECO_LOCAL_UG2_POT'], [int(self.ug2.potencia * 1000)])
        DataBank.set_words(self.cfg['ENDERECO_LOCAL_UG2_SETPOINT'], [int(self.ug2.setpoint * 1000)])
        DataBank.set_words(self.cfg['ENDERECO_LOCAL_UG2_DISP'], [int(self.ug2.disponivel)])
        clp_online = 1 if self.clp_online else 0
        DataBank.set_words(self.cfg['ENDERECO_LOCAL_CLP_ONLINE'], [int(clp_online)])
        # Todo DataBank.set_words(self.cfg['ENDERECO_LOCAL_STATUS_MOA'], [int(self.status_moa)])

    def get_agendamentos_pendentes(self):
        """
        Retorna os agendamentos pendentes para a usina.
        :return: list[] agendamentos
        """
        agendamentos = []
        with Database() as db:
            agendamentos = db.get_agendamentos_pendentes()
        return agendamentos

    def verificar_agendamentos(self):
        """
        Verifica os agendamentos feitos pelo django no banco de dados e lida com eles, executando, etc...
        """
        agora = datetime.now()
        agora = agora - timedelta(seconds=agora.second, microseconds=agora.microsecond)
        futuro = agora + timedelta(minutes=1)
        agendamentos = self.get_agendamentos_pendentes()

        if len(agendamentos) == 0:
            return True

        atraso = False
        for agendamento in agendamentos:
            if agendamento[1] < agora:
                atraso = True
                logger.warning("Agendamento #{} Atrasado! ({}).".format(agendamento[0], agendamento[2]))
                self.agendamentos_atrasados += 1
            if agendamento[1] < agora - timedelta(minutes=2):
                self.agendamentos_atrasados = 999
        if not atraso:
            self.agendamentos_atrasados = 0

        if self.agendamentos_atrasados > 3:
            logger.info("Os agendamentos estão muito atrasados! Acionando emergência.")
            self.acionar_emergencia_clp()
            return False

        for agendamento in agendamentos:
            if agendamento[1] < futuro and not bool(agendamento[3]):
                # Está na hora e ainda não foi executado. Executar!
                logger.info("Executando gendamento #{} - {}.".format(agendamento[0], agendamento[2]))

                # Exemplo Case agendamento:
                AGENDAMENTO_INDISPONIBILIZAR = 2
                if agendamento[2] == AGENDAMENTO_INDISPONIBILIZAR:
                    # Coloca em emergência
                    logger.info("Indisponibilizando a usina (comando via agendamento).")
                    try:
                        # atualiza o banco
                        q = "UPDATE agendamentos_agendamento " \
                            "SET executado = 1 " \
                            "WHERE id = {}".format(int(agendamento[0]))
                        q2 = """UPDATE parametros_moa_parametrosusina
                                           SET emergencia_acionada = '{}'
                                           WHERE id = 1; """.format(1 if self.emergencia_acionada else 0)
                        with Database() as db:
                            db.execute(q)
                            db.execute(q2)
                    except Exception as e:
                        logger.error(e)
                        continue
                    finally:
                        # finalmente, aciona no clp
                        self.acionar_emergencia_clp()

                # Após executar, indicar no banco de dados
                q = "UPDATE agendamentos_agendamento " \
                    "SET executado = 1 " \
                    "WHERE id = {}".format(int(agendamento[0]))
                with Database() as db:
                    db.execute(q)
                logger.info("O comando #{} - {} foi executado.".format(agendamento[0], agendamento[2]))

            else:
                # Ainda não é a hora de executar.
                pass

    def distribuir_potencia(self, pot_alvo):

        self.pot_disp = 0
        if self.ug1.disponivel:
            self.pot_disp += self.cfg['pot_maxima_ug']
        if self.ug2.disponivel:
            self.pot_disp += self.cfg['pot_maxima_ug']

        if self.pot_medidor > self.cfg['pot_maxima_alvo'] and pot_alvo > (self.cfg['pot_maxima_alvo']* 0.95):
            pot_alvo = pot_alvo * 0.99 * (self.cfg['pot_maxima_alvo'] / self.pot_medidor)

        if pot_alvo < self.cfg['pot_minima']:
            self.ug1.mudar_setpoint(0)
            self.ug2.mudar_setpoint(0)
        else:
            pot_alvo = min(pot_alvo, self.pot_disp)
            if self.ug1.sincronizada and self.ug2.sincronizada and pot_alvo > (2 * self.cfg['pot_minima']):
                self.ug1.mudar_setpoint(pot_alvo / 2)
                self.ug2.mudar_setpoint(pot_alvo / 2)
            elif (pot_alvo > (self.cfg['pot_maxima_ug'] + self.cfg['margem_pot_critica'])) and (abs(self.erro_nv) > 0.05) \
                    and self.ug1.disponivel and self.ug2.disponivel:
                self.ug1.mudar_setpoint(pot_alvo / 2)
                self.ug2.mudar_setpoint(pot_alvo / 2)
            else:
                pot_alvo = min(pot_alvo, self.cfg['pot_maxima_ug'])
                ugs = self.lista_de_ugs_disponiveis()
                if len(ugs) > 0:
                    ugs[0].mudar_setpoint(pot_alvo)
                    for ug in ugs[1:]:
                        ug.mudar_setpoint(0)
                else:
                    for ug in ugs:
                        ug.mudar_setpoint(0)

    def lista_de_ugs_disponiveis(self):
        """
        Retorn uma lista de ugs disponiveis conforme a ordenação selecionada
        """
        ls = []
        for ug in self.ugs:
            if ug.disponivel:
                ls.append(ug)

        if self.modo_de_escolha_das_ugs == 2:
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
        :param erro_nivel: Float
        :return: Sinal de controle proporcional
        """

        # Calcula PID
        logger.debug("Alvo: {:0.3f}, Recente: {:0.3f}, Anterior: {:0.3f}".format(self.nv_alvo, self.nv_montante_recente, self.nv_montante_anterior))

        self.controle_p = self.kp * self.erro_nv
        self.controle_i = res = max(min((self.ki * self.erro_nv) + self.controle_i, 0.8), 0)
        self.controle_d = self.kd*(self.erro_nv -self.erro_nv_anterior)
        saida_pid = self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3)
        logger.debug("PID: {:0.3f}, P:{:0.3f}, I:{:0.3f}, D:{:0.3f}".format(saida_pid, self.controle_p, self.controle_i, self.controle_d))

        # Calcula o integrador de estabilidade e limita
        self.controle_ie = max(min(saida_pid * self.kie + self.controle_ie, 1), 0)
        if self.nv_maximo - self.nv_montante_recente < 0.01:
            self.controle_ie = min(self.controle_ie, 0.8)

        # Arredondamento e limitação
        pot_alvo = max(min(round(self.cfg['pot_maxima_usina'] * self.controle_ie, 2), self.cfg['pot_maxima_usina']), self.cfg['pot_minima'])
        self.distribuir_potencia(pot_alvo)


class UnidadeDeGeracao:

    def __init__(self, id_ug):

        self.id_da_ug = id_ug
        self.flag = 0
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

    def normalizar(self, flag=0b1):
        #Normaliza a ug

        if self.flag & flag:
            self.flag = self.flag - flag
            logger.info("UG {} normalizada a flag {}.".format(self.id_da_ug, flag))

    def indisponibilizar(self, flag=0b1, descr="Sem descrição adcional"):
        #Indisponibiliza a ug

        if not self.flag & flag:
            logger.info("Indisponibilizando UG {}. Flag ({}) ({})".format(self.id_da_ug, flag, descr))
            self.flag += flag

    def atualizar_estado(self):
        """
        Atualiza o estado da ug conforme as vars dela. Executa o "Comportamento" da ug.
        """

        if self.flag and self.disponivel:
            logger.warning("UG {} indisponivel. Flag {}.".format(self.id_da_ug, self.flag))
            self.disponivel = False

        if not self.flag and not self.disponivel:
            logger.warning("UG {} disponivel. Flag {}.".format(self.id_da_ug, self.flag))
            self.disponivel = True

        self.sincronizada = True if self.potencia > 0 else False

        # todo Verificações
        if self.temp_mancal >= self.temp_mancal_max:
            self.indisponibilizar(0b10,
                                  "Temperatura do mancal excedida (atual:{}; max:{})".format(self.temp_mancal,
                                                                                             self.temp_mancal_max))
        else:
            self.normalizar(0b10)

        if self.perda_na_grade >= self.perda_na_grade_max:
            self.indisponibilizar(0b100,
                                  "Perda máxima na grade excedida (atual:{}; max:{})".format(self.perda_na_grade,
                                                                                            self.perda_na_grade_max))
        else:
            self.normalizar(0b100)


    def mudar_setpoint(self, alvo):

        alvo = max(alvo, 0)

        if self.temp_mancal > self.temp_mancal_max:
            alvo = 0
        elif self.perda_na_grade > self.perda_na_grade_max:
            alvo = 0
        else:
            if self.temp_mancal > self.temp_mancal_alerta:
                alvo *= sqrt(sqrt(
                    1 - ((self.temp_mancal - self.temp_mancal_alerta) / (self.temp_mancal_max - self.temp_mancal_alerta))))
            if self.perda_na_grade > self.perda_na_grade_alerta:
                alvo *= sqrt(
                    sqrt(1 - ((self.perda_na_grade - self.perda_na_grade_alerta) / (
                            self.perda_na_grade_max - self.perda_na_grade_alerta))))
        self.setpoint = alvo.real


class Comporta:

    def __init__(self):
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
        estado_alvo = self.pos_comporta
        for pos in self.posicoes:
            if (nv_montante < pos['anterior']) and (pos['pos'] <= self.pos_comporta) and (self.pos_comporta >= 1):
                estado_alvo = pos['pos'] - 1
                break
            if (nv_montante >= pos['proximo']) and (pos['pos'] >= self.pos_comporta) and (self.pos_comporta < 5):
                estado_alvo = pos['pos'] + 1
        if not estado_alvo == self.pos_comporta:
            self.pos_comporta = estado_alvo
            logger.info("Mudança de setpoint da comprota para {} (atual:{})".format(estado_alvo, self.pos_comporta))
