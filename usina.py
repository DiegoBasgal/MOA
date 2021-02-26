import logging
import mysql.connector
import socket
from datetime import datetime, timedelta
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import DataBank


###########################
# Inicializando o logging #
###########################
logger = logging.getLogger('__main__')

#########
# CONST #
#########

# Constantes referentes aos códigos de  agendamento
AGENDAMENTO_RESET_PARMAETROS = 1
AGENDAMENTO_INDISPONIBILIZAR = 2
AGENDAMENTO_NORMALIZAR = 3
AGENDAMENTO_INDISPONIBILIZAR_UG_1 = 10
AGENDAMENTO_NORMALIZAR_UG_1 = 11
AGENDAMENTO_INDISPONIBILIZAR_UG_2 = 20
AGENDAMENTO_NORMALIZAR_UG_2 = 21

# Constante referentes ao modbus com a CLP
ENDERECO_CLP_NV_MONATNTE = 0
ENDERECO_CLP_UG1_FLAGS = 20
ENDERECO_CLP_UG1_HORAS = 23
ENDERECO_CLP_UG1_SETPOINT = 22
ENDERECO_CLP_UG1_POTENCIA = 21
ENDERECO_CLP_UG2_FLAGS = 30
ENDERECO_CLP_UG2_HORAS = 33
ENDERECO_CLP_UG2_SETPOINT = 32
ENDERECO_CLP_UG2_POTENCIA = 3
ENDERECO_CLP_USINA_FLAGS = 100

# Constante referentes ao databank local para acesso via modbus
ENDERECO_LOCAL_NV_MONATNTE = 9
ENDERECO_LOCAL_NV_ALVO = 10
ENDERECO_LOCAL_NV_RELIGAMENTO = 11
ENDERECO_LOCAL_UG1_POT = 19
ENDERECO_LOCAL_UG1_SETPOINT = 20
ENDERECO_LOCAL_UG1_DISP = 21
ENDERECO_LOCAL_UG2_POT = 29
ENDERECO_LOCAL_UG2_SETPOINT = 30
ENDERECO_LOCAL_UG2_DISP = 31
ENDERECO_LOCAL_CLP_ONLINE = 99
ENDERECO_LOCAL_STATUS_MOA = 100

########
# Vars #
########
modbus_clp = ModbusClient()


###########
# Classes #
###########

class UnidadeDeGeracao:
    """
    Classe UnidadeDeGeração

    Atributos:
        disponivel : bool
        horas_maquina : int
        id_da_ug : int
        potencia : float
        prioridade : int (Maior num = maior prioridade)
        setpoint : float
        sincronizada : bool

    Métodos:
        __init__(self, id_ug)
            Inicia a ug com o id informado

        indisponibilizar(self)
            Indisponibiliza a ug

        normalizar(self)
            Normaliza a ug

    """

    disponivel = True
    horas_maquina = 0
    id_da_ug = 0
    potencia = 0
    prioridade = 0
    registrador_flags = 0
    registrador_setpoint = 0
    registrador_potencia = 0
    setpoint = 0
    sincronizada = False

    def __init__(self, id_ug):
        """
        Inicia a ug
        """

        self.id_da_ug = id_ug

        if id_ug == 1:
            enderecos = [ENDERECO_CLP_UG1_FLAGS, ENDERECO_CLP_UG1_HORAS,
                         ENDERECO_CLP_UG1_SETPOINT, ENDERECO_CLP_UG1_POTENCIA]
        elif id_ug == 2:
            enderecos = [ENDERECO_CLP_UG2_FLAGS, ENDERECO_CLP_UG2_HORAS,
                         ENDERECO_CLP_UG2_SETPOINT, ENDERECO_CLP_UG2_POTENCIA]
        else:
            # Se no houver a mquina com o id informado, parar imediatamente
            raise SyntaxError

        self.registrador_flags = enderecos[0]
        self.registrador_horas = enderecos[1]
        self.registrador_potencia = enderecos[2]
        self.registrador_setpoint = enderecos[3]

    def normalizar(self):
        """
        Normaliza a ug
        """
        self.disponivel = True
        modbus_clp.write_single_register(self.registrador_flags, 0)

    def indisponibilizar(self):
        """
        Indisponibiliza a ug
        """

        self.disponivel = False
        modbus_clp.write_single_register(self.registrador_flags, 1)


class Usina:

    status_moa = 0  # Menor que 10 é bom
    emergencia_acionada = False
    emergencia_elipse_acionada = False
    modo_manual_elipse_acionado = False
    estado_anterior_modo_manual_elipse = False
    modo_autonomo = True
    aguardando_reservatorio = False
    clp_online = False
    clp_ip = ''
    clp_porta = 0
    modbus_server_ip = ''
    modbus_server_porta = 0
    kp = 0
    ki = 0
    kd = 0
    kie = 0
    margem_pot_critica = 0
    modo_de_escolha_das_ugs = 0
    n_movel_L = 0
    n_movel_R = 0
    nv_alvo = 0
    nv_maximo = 0
    nv_minimo = 0
    nv_montante = 0
    nv_religamento = 0
    posicao_comporta = 0
    pot_minima = 0
    pot_nominal = 0
    pot_nominal_ug = 2.5
    pot_disp = 0
    timer_erro = 0

    ug1 = UnidadeDeGeracao(1)
    ug2 = UnidadeDeGeracao(2)
    ugs = ug1, ug2

    valor_ie_inicial = 0.3
    mysql_config = {
        'host': "172.21.15.12",
        'user': "root",
        'passwd': "11Marco2020@",
        'db': "django_db",
        'charset': 'utf8',
        'autocommit': True,
    }

    def __init__(self):
        """
        Inicia a ug
        """
        self.modbus_server_ip = get_ip_local()
        self.ler_valores()
        self.status_moa = 7

        global modbus_clp
        modbus_clp = ModbusClient(host=self.clp_ip, port=self.clp_porta,
                                  timeout=5, unit_id=1, auto_open=True, auto_close=False)

    def ler_valores(self):
        """
        Atualiza os valores armazenados localmente segundo o estado da usina (via banco e modbus)
        """

        # grava alguns valores anteriores para detectar bordas
        estado_anterior_emergencia_elipse = self.emergencia_elipse_acionada
        estado_anterior_modo_manual_elipse = self.modo_manual_elipse_acionado
        modo_de_escolha_das_ugs_ant = self.modo_de_escolha_das_ugs

        # Verifica qual é o ip local dessa máquina
        self.modbus_server_ip = get_ip_local()

        # Lê os valores da usina que estão no banco de dados
        q = "SELECT * FROM parametros_moa_parametrosusina WHERE id = 1"
        mydb = mysql.connector.connect(**self.mysql_config)
        mycursor = mydb.cursor()
        mycursor.execute(q)
        parametros = mycursor.fetchone()

        self.clp_ip = parametros[1]
        self.clp_porta = int(parametros[2])
        self.modbus_server_porta = int(parametros[4])
        self.kp = float(parametros[5])
        self.ki = float(parametros[6])
        self.kd = float(parametros[7])
        self.kie = float(parametros[8])
        self.margem_pot_critica = float(parametros[9])
        self.n_movel_L = int(parametros[10])
        self.n_movel_R = int(parametros[11])
        self.nv_alvo = float(parametros[12])
        self.nv_maximo = float(parametros[13])
        self.nv_minimo = float(parametros[14])
        self.nv_religamento = float(parametros[16])
        self.pot_minima = float(parametros[18])
        self.pot_nominal = float(parametros[19])
        self.pot_nominal_ug = float(parametros[20])
        self.timer_erro = int(parametros[22])
        self.emergencia_acionada = int(parametros[35])
        self.modo_autonomo = bool(parametros[36])
        self.ug1.prioridade = int(parametros[40])
        self.ug2.prioridade = int(parametros[41])
        self.modo_de_escolha_das_ugs = int(parametros[42])

        # Comunicação modbus
        global modbus_clp
        modbus_clp = ModbusClient(host=self.clp_ip, port=self.clp_porta, timeout=5, unit_id=1, auto_open=True,
                                  auto_close=False)

        # Tenta abrir uma conexão
        if modbus_clp.open():

            # Se conectou, lê, fecha a conexão e atribui os vales certos.
            regs = modbus_clp.read_holding_registers(0, 100)
            modbus_clp.close()
            if regs is None:
                # Se os regs estiverem vazios, a conexão falhou
                self.clp_online = False
                raise ConnectionError

            # clp online
            self.clp_online = True

            # nv_montante
            self.nv_montante = round((regs[ENDERECO_CLP_NV_MONATNTE] * 0.001) + 620, 2)

            # ToDo Essa parte pode/deve ser movida para dentro do objeto UnidadeDeGeracao

            # ug1
            self.ug1.disponivel = not bool(regs[ENDERECO_CLP_UG1_FLAGS])
            self.ug1.potencia = regs[ENDERECO_CLP_UG1_POTENCIA] / 1000
            self.ug1.sincronizada = True if self.ug1.potencia > 0 else False
            self.ug1.horas_maquina = regs[ENDERECO_CLP_UG1_HORAS] / 60

            # ug2
            self.ug2.disponivel = not bool(regs[ENDERECO_CLP_UG2_FLAGS])
            self.ug2.potencia = regs[ENDERECO_CLP_UG2_POTENCIA] / 1000
            self.ug2.sincronizada = True if self.ug2.potencia > 0 else False
            self.ug2.horas_maquina = regs[ENDERECO_CLP_UG2_HORAS] / 60

        else:

            # Se não conectou, a clp não está online.
            self.clp_online = False
            raise ConnectionError

        # Verifica a pot que est disponível para ser trabalhada
        self.pot_disp = 0
        if self.ug1.disponivel:
            self.pot_disp += 2.5
        if self.ug2.disponivel:
            self.pot_disp += 2.5

        # Verifica o acionamento do modo de emergência pelo elipse
        self.emergencia_elipse_acionada = True if DataBank.get_words(1000, 1)[0] > 0 else False
        if not (self.emergencia_elipse_acionada == estado_anterior_emergencia_elipse):
            # Mudou! Atualizar.
            self.emergencia_acionada = not self.emergencia_elipse_acionada
            q = """UPDATE parametros_moa_parametrosusina
                   SET emergencia_acionada = '{}'
                   WHERE id = 1; """.format(1 if self.emergencia_acionada else 0)
            mydb = mysql.connector.connect(**self.mysql_config)
            mycursor = mydb.cursor()
            mycursor.execute(q)

        # Verifica o acionamento do modo manual pelo elipse
        self.modo_manual_elipse_acionado = True if DataBank.get_words(1001, 1)[0] > 0 else False
        # Mudou! Atualizar.
        if not (self.modo_manual_elipse_acionado == estado_anterior_modo_manual_elipse):
            self.modo_autonomo = not self.modo_manual_elipse_acionado
            q = """UPDATE parametros_moa_parametrosusina
                   SET modo_autonomo = '{}'
                   WHERE id = 1; """.format(1 if self.modo_autonomo else 0)
            mydb = mysql.connector.connect(**self.mysql_config)
            mycursor = mydb.cursor()
            mycursor.execute(q)

        # Verifica o modo de escolha das ugs
        if not (modo_de_escolha_das_ugs_ant == self.modo_de_escolha_das_ugs):
            logger.info("O modo de prioridade na escolha das ugs foi alterado (#{})."
                        .format(self.modo_de_escolha_das_ugs))

    def escrever_valores(self):
        """
        Escreve os valores que a usina deve seguir (via banco e modbus)
        """
        
        # Usar try pois podem ocorrer erros de escrita
        try:
            
            agora = datetime.now()
            ano = int(agora.year)
            mes = int(agora.month)
            dia = int(agora.day)
            hor = int(agora.hour)
            mnt = int(agora.minute)
            seg = int(agora.second)
            mil = int(agora.microsecond / 1000)

            DataBank.set_words(0, [ano, mes, dia, hor, mnt, seg, mil])
            DataBank.set_words(ENDERECO_LOCAL_NV_MONATNTE, [int((self.nv_montante - 620) * 1000)])
            DataBank.set_words(ENDERECO_LOCAL_NV_ALVO, [int((self.nv_alvo - 620) * 1000)])
            DataBank.set_words(ENDERECO_LOCAL_NV_RELIGAMENTO, [int((self.nv_religamento - 620) * 1000)])
            DataBank.set_words(ENDERECO_LOCAL_UG1_POT, [int(self.ug1.potencia * 1000)])
            DataBank.set_words(ENDERECO_LOCAL_UG1_SETPOINT, [int(self.ug1.setpoint * 1000)])
            DataBank.set_words(ENDERECO_LOCAL_UG1_DISP, [int(self.ug1.disponivel)])
            DataBank.set_words(ENDERECO_LOCAL_UG2_POT, [int(self.ug2.potencia * 1000)])
            DataBank.set_words(ENDERECO_LOCAL_UG2_SETPOINT, [int(self.ug2.setpoint * 1000)])
            DataBank.set_words(ENDERECO_LOCAL_UG2_DISP, [int(self.ug2.disponivel)])
    
            clp_online = 1 if self.clp_online else 0
            DataBank.set_words(ENDERECO_LOCAL_CLP_ONLINE, [int(clp_online)])
            DataBank.set_words(ENDERECO_LOCAL_STATUS_MOA, [int(self.status_moa)])

            # Escreve no banco
            q = """ UPDATE parametros_moa_parametrosusina
                    SET
                    timestamp = '{}',
                    status_moa = '{}',
                    aguardando_reservatorio = {},
                    clp_online = {},
                    nv_montante = {},
                    posicao_comporta = {},
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
                    ug2_tempo = {}
                    WHERE id = 1; 
                    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               self.status_moa,
                               1 if self.aguardando_reservatorio else 0,
                               1 if self.clp_online else 0,
                               self.nv_montante,
                               self.posicao_comporta,
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
                               self.ug2.horas_maquina)

            mydb = mysql.connector.connect(**self.mysql_config)
            mycursor = mydb.cursor()
            mycursor.execute(q)

            # Comunicação modbus
            if modbus_clp.open():
                # Atribuir potência para as ugs
                modbus_clp.write_single_register(ENDERECO_CLP_UG1_SETPOINT, int(self.ug1.setpoint * 1000))
                modbus_clp.write_single_register(ENDERECO_CLP_UG2_SETPOINT, int(self.ug2.setpoint * 1000))
                modbus_clp.close()
            else:
                self.clp_online = False
                raise ConnectionError

        except Exception as e:
            logger.error("Erro ao escrever variaveis de saida. {}".format(e))

    def acionar_emergerncia_clp(self):
        """
        Aciona a emergência na CLP
        """
        if modbus_clp.open():
            modbus_clp.write_single_register(ENDERECO_CLP_USINA_FLAGS, int(1))
            modbus_clp.close()
        else:
            self.clp_online = False
            raise ConnectionError

    def normalizar_emergencia_clp(self):
        """
        Normaliza a emergência na CLP
        """

        if modbus_clp.open():
            modbus_clp.write_single_register(ENDERECO_CLP_USINA_FLAGS, int(0))
            modbus_clp.close()
        else:
            self.clp_online = False
            raise ConnectionError

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
            ls = sorted(ls, key=lambda y: (not y.sincronizada, not y.prioridade, y.horas_maquina))
        else:
            # escolher por menor horas_maquina primeiro
            ls = sorted(ls, key=lambda y: (not y.sincronizada, y.horas_maquina, not y.prioridade,))

        return ls

    def verificar_agendamentos(self):
        """
        Verifica os agendamentos feitos pelo django no banco de dados e lida com eles, executando, etc...
        """

        agora = datetime.now()
        agora = agora - timedelta(seconds=agora.second, microseconds=agora.microsecond)
        futuro = agora + timedelta(minutes=1)

        # Lê do banco
        q = """SELECT id, DATE_SUB(data, INTERVAL 3 HOUR), comando_id, executado
                FROM agendamentos_agendamento
                WHERE executado = 0"""
        mydb = mysql.connector.connect(**self.mysql_config)
        mycursor = mydb.cursor()
        mycursor.execute(q)
        agendamentos = mycursor.fetchall()

        for agendamento in agendamentos:

            if agendamento[1] < agora:
                # Já passou
                # ToDo Veridicar comportamento para agendamentos passados, (executados ou atrasados)
                # Deve-se executar alguma verificação caso já tenha passado da hora?
                # Ex. Caso no tenha sido executado no minuto certo devido a rede, deve tentar executar ou ignorar?
                pass

            elif agendamento[1] < futuro and not bool(agendamento[3]):
                # Está na hora e ainda não foi eecutado. Executar!
                logger.info("Executando gendamento #{} - {}.".format(agendamento[0], agendamento[2]))

                # Case agendamento:

                if agendamento[2] == AGENDAMENTO_INDISPONIBILIZAR:
                    # Coloca em emerg^encia
                    logger.info("Indisponibilizando a usina (comando via agendamento).")
                    self.emergencia_acionada = True
                    try:
                        # atualiza o banco
                        q = "UPDATE agendamentos_agendamento " \
                            "SET executado = 1 " \
                            "WHERE id = {}".format(int(agendamento[0]))
                        q2 = """UPDATE parametros_moa_parametrosusina
                                           SET emergencia_acionada = '{}'
                                           WHERE id = 1; """.format(1 if self.emergencia_acionada else 0)

                        mydb = mysql.connector.connect(**self.mysql_config)
                        mycursor = mydb.cursor()
                        mycursor.execute(q)
                        mycursor.execute(q2)

                    except Exception as e:
                        logger.error(e)
                        continue
                    finally:
                        # finalmente, aciona no clp
                        self.acionar_emergerncia_clp()

                elif agendamento[2] == AGENDAMENTO_NORMALIZAR:
                    # normalizar usina
                    logger.info("Normalizando a usina (comando via agendamento).")
                    self.emergencia_acionada = False
                    try:
                        # atualiza o banco
                        q = """UPDATE parametros_moa_parametrosusina
                                           SET emergencia_acionada = '{}'
                                           WHERE id = 1; """.format(1 if self.emergencia_acionada else 0)

                        mydb = mysql.connector.connect(**self.mysql_config)
                        mycursor = mydb.cursor()
                        mycursor.execute(q)
                        self.ug1.disponivel = True
                        self.ug2.disponivel = True
                        client = ModbusClient(host=self.clp_ip, port=self.clp_porta, timeout=5, unit_id=1)
                        if client.open():
                            client.write_single_register(ENDERECO_CLP_UG1_FLAGS, 0)
                            client.write_single_register(ENDERECO_CLP_UG2_FLAGS, 0)
                            client.write_single_register(ENDERECO_CLP_USINA_FLAGS, 0)
                            client.close()

                    except Exception as e:
                        logger.error(e)
                        continue

                elif agendamento[2] == AGENDAMENTO_RESET_PARMAETROS:
                    try:
                        q = """ UPDATE parametros_moa_parametrosusina
                                                            SET clp_ip = '172.21.15.13',
                                                            clp_porta = 502,
                                                            modbus_server_ip = '172.21.15.12',
                                                            modbus_server_porta = 5002,
                                                            kp = -20.000,
                                                            ki = -0.300,
                                                            kd = - 50.000,
                                                            kie = 0.500,
                                                            margem_pot_critica = 0.500,
                                                            n_movel_L = 60,
                                                            n_movel_R = 6,
                                                            nv_alvo = 643.250,
                                                            nv_maximo = 643.500,
                                                            nv_minimo = 643.000,
                                                            nv_religamento = 643.250,
                                                            pot_minima = 1.000,
                                                            pot_nominal = 5.000,
                                                            pot_nominal_ug = 2.500,
                                                            pot_disp = 5.000,
                                                            timer_erro = 30,
                                                            valor_ie_inicial = 0.500,
                                                            timestamp = '{}',
                                                            ug1_prioridade = 0,
                                                            ug2_prioridade = 0,
                                                            modo_de_escolha_das_ugs = 1
                                                            WHERE id = 1; """.format(
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                        mydb = mysql.connector.connect(**self.mysql_config)
                        mycursor = mydb.cursor()
                        mycursor.execute(q)

                    except Exception as e:
                        logger.error(e)
                        continue

                elif agendamento[2] == AGENDAMENTO_INDISPONIBILIZAR_UG_1:
                    logger.info("Indisponibilizando a UG1 (comando via agendamento).")
                    self.ug1.indisponibilizar()

                elif agendamento[2] == AGENDAMENTO_INDISPONIBILIZAR_UG_2:
                    logger.info("Indisponibilizando a UG2 (comando via agendamento).")
                    self.ug2.indisponibilizar()

                elif agendamento[2] == AGENDAMENTO_NORMALIZAR_UG_1:
                    logger.info("Normalizando a UG1 (comando via agendamento).")
                    self.ug1.normalizar()


                elif agendamento[2] == AGENDAMENTO_NORMALIZAR_UG_2:
                    logger.info("Normalizando a UG2 (comando via agendamento).")
                    self.ug2.normalizar()

                # fim case agendamento

                # Após executar, indicar no banco de dados
                q = "UPDATE agendamentos_agendamento " \
                    "SET executado = 1 " \
                    "WHERE id = {}".format(int(agendamento[0]))
                mydb = mysql.connector.connect(**self.mysql_config)
                mycursor = mydb.cursor()
                mycursor.execute(q)
                logger.info("O comando #{} - {} foi executado.".format(agendamento[0], agendamento[2]))

            else:
                # Ainda não é a hora de executar.
                pass


def get_ip_local():
    s = 0
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        temp = s.getsockname()[0]
    except Exception:
        temp = 'localhost'
    finally:
        s.close()
    return temp
