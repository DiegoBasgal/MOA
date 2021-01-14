# Import site é necessário para funcionar fora da IDE devido a necessidade de adicionar o diretório ao PATH
import math
import site
site.addsitedir('..')

from datetime import datetime
from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
import logging
import MCLPS.CLP_config as CLPconfig
import MCLPS.connector_db as db
import os
import threading
import usina

'''
    Simulador de CLP com comunicação Modbus
'''

# Constantes
ESCALA_DE_TEMPO = 120

PLOTAR_GRAFICO_DEBBUG = True


# +-------------------------------------------------------------------------------------------------------------------+
# | Comportamento do reservatório                                                                                     |
# +-------------------------------------------------------------------------------------------------------------------+
class ComportamentoReal:
    
    setpoint_ug1 = 0
    setpoint_ug2 = 0
    comp_flags = 0
    comp_fechada = 0
    comp_p1 = 0
    comp_p2 = 0
    comp_p3 = 0
    comp_p4 = 0
    comp_aberta = 0
    nv_montante = 0
    volume = 0
    pot_ug1 = 0
    pot_ug2 = 0
    sinc_ug1 = 0
    sinc_ug2 = 0

    def __init__(self):

        self.volume = 192300
        self.atualiza_nv_montante()
        self.pot_ug1 = 0
        self.pot_ug2 = 0
        self.setpoint_ug1 = 0
        self.setpoint_ug2 = 0
        self.sinc_ug1 = 0
        self.sinc_ug2 = 0

    def atualiza_nv_montante(self):
        nv = - 0.0000000002 * ((self.volume / 1000) ** 4) + 0.0000002 * ((self.volume / 1000) ** 3) - 0.0001 * (
                    (self.volume / 1000) ** 2) + 0.0331 * (self.volume / 1000) + 639.43
        self.nv_montante = nv
        return nv

    def comportamento_reservatorio(self):

        logging.info("Comportamento_reservatório rodando")
        amostras = db.get_amostras_afluente()

        while True:

            logging.info("Simuladndo a partir do inicio da tabela de afluentes")
            logging.debug("T simulação (s); Afluente; Efluente; Turbinado; Nv_montante")

            t0 = datetime.now()
            t1 = datetime.now()
            segundos_simulados = 0
            segundos_simulados_ant = 0
            a = 0
            while a in range(len(amostras) - 1):

                segundos_reais = (datetime.now()-t0).total_seconds()
                segundos_simulados_ant = segundos_simulados
                segundos_simulados = segundos_reais * ESCALA_DE_TEMPO
                delta_t_sim = segundos_simulados - segundos_simulados_ant
                sleep(0.001)  # tick

                if (amostras[a][0] - amostras[0][0]).total_seconds() < segundos_simulados:
                    a += 1
                    t_c = (datetime.now() - t1).total_seconds()
                    t_a = (amostras[a + 1][0] - amostras[a][0]).total_seconds()
                    if t_c > 0:
                        logging.debug("Escala da simulação: {:2.3f}".format(t_a / t_c))
                    t1 = datetime.now()

                else:

                    # Acerta as UGS

                    #ug1
                    if self.setpoint_ug1 >= 1:
                        self.sinc_ug1 += 0.2 * (delta_t_sim / 60)
                        if self.sinc_ug1 >= 1:
                            self.sinc_ug1 = 1
                            var_ug1_por_minuto = (self.setpoint_ug1 - self.pot_ug1) / (delta_t_sim / 60)
                            var_ug1_por_minuto = math.copysign(min(0.625, abs(var_ug1_por_minuto)), var_ug1_por_minuto)
                            self.pot_ug1 += (var_ug1_por_minuto / 60) * delta_t_sim
                            self.pot_ug1 = max(1, self.pot_ug1)
                    else:
                        self.sinc_ug1 = 0
                        self.pot_ug1 -= (0.625 / 60) * delta_t_sim
                        self.pot_ug1 = max(0, self.pot_ug1)
           
                    #ug2
                    if self.setpoint_ug2 >= 1:
                        self.sinc_ug2 += 0.2 * (delta_t_sim / 60)
                        if self.sinc_ug2 >= 1:
                            self.sinc_ug2 = 1
                            var_ug2_por_minuto = (self.setpoint_ug2 - self.pot_ug2) / (delta_t_sim / 60)
                            var_ug2_por_minuto = math.copysign(min(0.625, abs(var_ug2_por_minuto)), var_ug2_por_minuto)
                            self.pot_ug2 += (var_ug2_por_minuto / 60) * delta_t_sim
                            self.pot_ug2 = max(1, self.pot_ug2)
                    else:
                        self.sinc_ug2 = 0
                        self.pot_ug2 -= (0.625 / 60) * delta_t_sim
                        self.pot_ug2 = max(0, self.pot_ug2)

                    # Acerta as Vazoes
                    q_aflu = amostras[a][1]
                    #q_aflu = 5.8623152  # 1UG@1,5MW + SANI@1/2NVMAX
                    q_vert = usina.q_vertimento(self.nv_montante)
                    q_comp = usina.q_comporta(self.comp_fechada, self.comp_p1, self.comp_p2, self.comp_p3, self.comp_p4,
                                              self.comp_aberta, self.nv_montante)
                    q_sani = usina.q_sanitaria(self.nv_montante)
                    q_turb = usina.q_turbinada(self.pot_ug1, self.pot_ug2)
                    q_eflu = q_vert + q_comp + q_sani + q_turb
                    q_liquida = q_aflu - q_eflu

                    # Acerta o NV
                    self.volume += q_liquida * delta_t_sim
                    if self.volume < 0:
                        self.volume = 0
                    self.atualiza_nv_montante()

                    # print("Simulando...")

                    # para grafico de debbug
                    if PLOTAR_GRAFICO_DEBBUG:
                        fp = open('debug.out', 'w+')
                        fp.write("{:15.0f} {:5.5f} {:5.5f} {:5.5f} {:5.5f} {:5.5f}\n".format(segundos_simulados,  q_aflu, self.nv_montante, self.pot_ug1,
                                                                                     self.pot_ug2, self.setpoint_ug1+self.setpoint_ug2))
                        fp.close()

                    logging.debug(("{:15.0f};{:5.5f};{:5.5f};{:5.5f};{:5.5f};{:5.5f}\n".format(segundos_simulados,  q_aflu, self.nv_montante, self.pot_ug1,
                                                                                     self.pot_ug2, self.setpoint_ug1+self.setpoint_ug2)))
            logging.info("Final das amostras")


def plotar_debug():
    from MCLPS import plotar_debbug


# +-------------------------------------------------------------------------------------------------------------------+
# | MAIN                                                                                                              |
# +-------------------------------------------------------------------------------------------------------------------+
if __name__ == "__main__":

    # Inicializando o logging
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)
    # LOG to file
    fileHandler = logging.FileHandler("simulador_clp.log", mode='w+')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    # LOG to console
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    if PLOTAR_GRAFICO_DEBBUG:
        t_plotar_debug = threading.Thread(target=plotar_debug)
        t_plotar_debug.daemon = False
        t_plotar_debug.start()
        sleep(2)

    # Inicialização dos comportamentos
    logging.info("Simulador iniciado. Iniciando Threads")

    comportamento_usina = ComportamentoReal()
    t_comportamento_reservatorio = threading.Thread(target=comportamento_usina.comportamento_reservatorio)
    t_comportamento_reservatorio.daemon = False
    t_comportamento_reservatorio.start()


    ########################
    # Comportamento da CLP #
    ########################

    logging.info("Iniciando Comportamento do clp")

    logging.info("Iniciando Servidor/Slave Modbus ")
    ip = CLPconfig.SLAVE_IP
    porta = CLPconfig.SLAVE_PORT
    temporizador = CLPconfig.CLP_REFRESH_RATE
    REGS = [0] * 7  # 16 registradores
    '''
        Detalhamento dos conteúdos dos registradores

        REGS[0]:    nivel_montante  [620 + X mm]
        REGS[1]:    setpoint ug1    [X kw]
        REGS[2]:    FLAGS_ug1     [RAW]
        REGS[3]:    setpoint ug2    [X kw]
        REGS[4]:    FLAGS_ug2     [RAW]
        REGS[5]:    comp_value  [RAW]
        REGS[6]:    comp_flags  [0]:fechada
                                    [1]:pos1
                                    [2]:pos2
                                    [3]:pos3
                                    [4]:pos4
                                    [5]:aberta)
        8 Pot REAL UG1
        9 Pot REAL UG2

    '''

    server = ModbusServer(host=ip, port=porta, no_block=True)
    try:
        server.start()
        while True:
            # Limpa a interface de linha
            os.system('cls' if os.name == 'nt' else 'clear')
            print("CLP rodando...")
            # Carrega os REGs, da memória, sem conectar.
            REGS = DataBank.get_words(0, 10)

            # Entradas da CLP
            comportamento_usina.setpoint_ug1 = (int(REGS[1])/1000)
            comportamento_usina.setpoint_ug2 = (int(REGS[3])/1000)
            comportamento_usina.comp_flags = REGS[5]
            comportamento_usina.comp_fechada = REGS[6] & 0b00000001
            comportamento_usina.comp_p1 = REGS[6] & 0b00000010
            comportamento_usina.comp_p2 = REGS[6] & 0b00000100
            comportamento_usina.comp_p3 = REGS[6] & 0b00001000
            comportamento_usina.comp_p4 = REGS[6] & 0b00010000
            comportamento_usina.comp_aberta = REGS[6] & 0b00100000

            # Saidas da CLP
            DataBank.set_words(0, [int((comportamento_usina.nv_montante - 620) * 100) * 10])
            DataBank.set_words(8, [int(comportamento_usina.pot_ug1 * 1000)])
            DataBank.set_words(9, [int(comportamento_usina.pot_ug2 * 1000)])
            sleep(temporizador)

    except Exception as e:
        logging.error("Erro na execução do CLP: {}".format(e))
    finally:
        logging.info("O comportamento_clp parou")
        pass

    logging.info("Final da Main")
