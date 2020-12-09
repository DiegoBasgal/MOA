# Import site é necessário para funcionar fora da IDE devido a necessidade de adicionar o diretório ao PATH
import site
from math import copysign

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
ESCALA_DE_TEMPO = 10

# Globais
q_afluente = 0
nv_montante = 0
pot_ug1 = 1
pot_ug2 = 0
comporta_flags = 0
comporta_fechada = True
comporta_p1 = False
comporta_p2 = False
comporta_p3 = False
comporta_p4 = False
comporta_aberta = False


# +-------------------------------------------------------------------------------------------------------------------+
# | Comportamento do reservatório                                                                                     |
# +-------------------------------------------------------------------------------------------------------------------+
def comportamento_reservatorio():

    logging.info("Thread comportamento_reservatório iniciada")

    global nv_montante
    global q_afluente
    volume = 192300
    q_vert = 0
    q_comp = 0
    q_sani = 0
    q_turb = 0
    q_eflu = 0
    q_liquida = 0
    nv_montante = - 0.0000000002 * ((volume / 1000) ** 4) + 0.0000002 * ((volume / 1000) ** 3) - 0.0001 * (
            (volume / 1000) ** 2) + 0.0331 * ((volume / 1000)) + 639.43
    nv_montante = round(nv_montante, 2)

    amostras = db.get_amostras_afluente()

    while True:

        logging.info("Simuladndo a partir do inpicio da tabela de afluentes")
        logging.debug("T simulação (s); Afluente; Efluente; Turbinado; Nv_montante")
        t0 = datetime.now()
        segundos_simulados = 0
        a = 0
        while a in range(len(amostras) - 1):
            segundos_reais = (datetime.now()-t0).total_seconds()
            segundos_simulados = segundos_reais * ESCALA_DE_TEMPO
            if (amostras[a][0] - amostras[0][0]).total_seconds() > segundos_simulados:
                a += 1

            # TODO usar q_afluente da tabela!
            # q_afluente = amostras[a][1]
            q_afluente = (DataBank.get_words(7, 1)[0]/1000)
            q_vert = usina.q_vertimento(nv_montante)
            q_comp = usina.q_comporta(comporta_fechada, comporta_p1, comporta_p2, comporta_p3, comporta_p4,
                                      comporta_aberta, nv_montante)
            q_sani = usina.q_sanitaria(nv_montante)
            q_turb = usina.q_turbinada(pot_ug1, pot_ug2)
            q_eflu = (q_vert + q_comp + q_sani + q_turb)
            q_liquida = q_afluente - q_eflu
            volume += q_liquida * ESCALA_DE_TEMPO
            if volume < 0 : volume = 0
            nv_montante = - 0.0000000002 * ((volume / 1000) ** 4) + 0.0000002 * ((volume / 1000) ** 3) - 0.0001 * ((volume / 1000) ** 2) + 0.0331 * (volume / 1000) + 639.43
            nv_montante = round(nv_montante, 3)
            sleep(0.1)

            # para grafico de debbug
            fp = open('debug.out', 'w+')
            fp.write("{:15.0f} {:5.5f} {:5.5f} {:5.5f} {:5.5f}\n".format(segundos_simulados,  q_afluente, nv_montante, pot_ug1, pot_ug2))
            fp.close()
            logging.debug(("{:15.0f};{:5.5f};{:5.5f};{:5.5f};{:5.5f}\n".format(segundos_simulados,  q_afluente, nv_montante, pot_ug1, pot_ug2)).replace(".",","))
            #segundos_reais = (datetime.now()-t0).total_seconds()
            #print(segundos_simulados/segundos_reais)
        logging.info("Final das amostras")


# +-------------------------------------------------------------------------------------------------------------------+
# | Comportamento do CLP                                                                                              |
# +-------------------------------------------------------------------------------------------------------------------+
def comportamento_clp():
    global q_afluente
    global nv_montante
    global pot_ug1
    global pot_ug2
    global comporta_flags
    global comporta_fechada
    global comporta_p1
    global comporta_p2
    global comporta_p3
    global comporta_p4
    global comporta_aberta

    logging.info("Thread comportamento_clp iniciada")
    logging.info("Iniciando Servidor/Slave Modbus ")

    ip = CLPconfig.SLAVE_IP
    porta = CLPconfig.SLAVE_PORT
    temporizador = CLPconfig.CLP_REFRESH_RATE
    REGS = [0] * 7  # 16 registradores
    '''
        Detalhamento dos conteúdos dos registradores
    
        REGS[0]:    nivel_montante  [620 + X mm]
        REGS[1]:    potencia_ug1    [X kw]
        REGS[2]:    FLAGS_ug1     [RAW]
        REGS[3]:    potencia_ug2    [X kw]
        REGS[4]:    FLAGS_ug2     [RAW]
        REGS[5]:    comporta_value  [RAW]
        REGS[6]:    comporta_flags  [0]:fechada
                                    [1]:pos1
                                    [2]:pos2
                                    [3]:pos3
                                    [4]:pos4
                                    [5]:aberta)
    '''

    server = ModbusServer(host=ip, port=porta, no_block=True)
    try:

        server.start()

        while True:
            # Limpa a interface de linha
            os.system('cls' if os.name == 'nt' else 'clear')

            # Carrega os REGs, da memória, sem conectar.
            REGS = DataBank.get_words(0, 10)

            # Entradas da CLP
            pot_ug1 = (pot_ug1*14 + (int(REGS[1])/1000))/15
            pot_ug2 = (pot_ug2*14 + (int(REGS[3])/1000))/15

            comporta_flags = REGS[5]
            comporta_fechada = REGS[6] & 0b00000001
            comporta_p1 = REGS[6] & 0b00000010
            comporta_p2 = REGS[6] & 0b00000100
            comporta_p3 = REGS[6] & 0b00001000
            comporta_p4 = REGS[6] & 0b00010000
            comporta_aberta = REGS[6] & 0b00100000
            q_afluente = REGS[7]/1000

            # Saidas da CLP
            DataBank.set_words(0, [int((nv_montante - 620) * 1000)])
            DataBank.set_words(7, [int(q_afluente * 1000)])

            print("###########\n"
                  "#  PyCLP  #\n"
                  "###########\n\n"
                  "Servidor/Slave ModbusTCP em {}:{}\n\n"
                  "TIME {}\n\n"
                  "REG0  {: >16} | nivel_montante (-620m + Xmm)\n"
                  "REG1  {: >16} | potencia_ug1 (kW)\n"
                  "REG2  {:016b} | FLAGS_ug1 (BIN)\n"
                  "REG3  {: >16} | potencia_ug2 (kW)\n"
                  "REG4  {:016b} | FLAGS_ug2 (BIN)\n"
                  "REG5  {: >16} | comporta_value (RAW)\n"
                  "REG6  {:016b} | comporta_flags ([fechada][p1]..[p5][aberta])\n".format(ip, porta, datetime.now(),
                                                                                          *REGS))

            sleep(temporizador)
    finally:
        pass

    logging.info("Thread comportamento_clp chegou ao final")


def plotar_debug():
    sleep(5)
    from MCLPS import plotar_debbug

# +-------------------------------------------------------------------------------------------------------------------+
# | MAIN                                                                                                              |
# +-------------------------------------------------------------------------------------------------------------------+
if __name__ == "__main__":
    # Inicializando o logging
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)
    # LOG to file
    fileHandler = logging.FileHandler("simulador_clp.log", mode='w+')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    # LOG to console
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    # Inicialização dos comportamentos
    t_plotar_debug = threading.Thread(target=plotar_debug)
    t_plotar_debug.daemon = False
    t_plotar_debug.start()
    sleep(5)


    logging.info("Simulador iniciado. Iniciando Threads")

    t_comportamento_clp = threading.Thread(target=comportamento_clp)
    t_comportamento_clp.daemon = False
    t_comportamento_clp.start()

    t_comportamento_reservatorio = threading.Thread(target=comportamento_reservatorio)
    t_comportamento_reservatorio.daemon = False
    t_comportamento_reservatorio.start()

    logging.info("Final da Main")
