from datetime import datetime
from time import sleep
from pyModbusTCP.server import ModbusServer, DataBank
import os
import MCLPS.CLP_config as CLPconfig
import MCLPS.connector_db as db

'''
    Simulador de CLP com comunicação Modbus
'''


print("Iniciando Servidor/Slave Modbus ")

ip = CLPconfig.SLAVE_IP
porta = CLPconfig.SLAVE_PORT
# temporizador = CLPconfig.CLP_REFRESH_RATE
temporizador = 0

REG = [0] * 7  # 16 registradores
'''
    Detalhamento dos conteúdos dos registradores

    REG[0]:     nivel_montante  [620 + X mm]
    REG[1]:     potencia_ug1    [X kw]
    REG[2]:     energia_ug1     [RAW]
    REG[3]:     potencia_ug2    [X kw]
    REG[4]:     energia_ug2     [RAW]
    REG[5]:     comporta_value  [RAW]
    REG[6]:     comporta_flags  [0]:fechada
                                [1]:pos1
                                [2]:pos2
                                [3]:pos3
                                [4]:pos4
                                [5]:aberta)
'''

server = ModbusServer(host=ip, port=porta, no_block=True)
try:

    server.start()

    a = 0
    amostras = db.get_amostras()

    while True:
        # Limpa a interface de linha
        os.system('cls' if os.name == 'nt' else 'clear')

        # Escreve os valores nos regs da CLP
        temporizador = (amostras[a+1][0] - amostras[a][0]).total_seconds()/CLPconfig.ESCALA_DE_TEMPO
        # Arruma a escala
        amostras[a][1] = int((amostras[a][1] - 620) * 100)*10
        amostras[a][2] = int(amostras[a][2])
        amostras[a][3] = int(amostras[a][3])
        amostras[a][4] = int(amostras[a][4])
        amostras[a][5] = int(amostras[a][5])
        flags_comporta = 0
        if amostras[a][7] != 0:
            flags_comporta += 0x1
        if amostras[a][8] != 0:
            flags_comporta += 0x2
        if amostras[a][9] != 0:
            flags_comporta += 0x4
        if amostras[a][10] != 0:
            flags_comporta += 0x8
        if amostras[a][11] != 0:
            flags_comporta += 0x16
        if amostras[a][12] != 0:
            flags_comporta += 0x32

        DataBank.set_words(0, amostras[a][1:7]+[flags_comporta])
        a = a + 1

        # Carrega os REGs, da memória, sem conectar.
        REGS = DataBank.get_words(0, 10)

        print("###########\n"
              "#  PyCLP  #\n"
              "###########\n\n"
              "Servidor/Slave ModbusTCP em {}:{}\n\n"
              "TIME {}\n\n"
              "REG0  {: >16} | nivel_montante (-620m + Xmm)\n"
              "REG1  {: >16} | potencia_ug1 (kW)\n"
              "REG2  {: >16} | energia_ug1 (RAW)\n"
              "REG3  {: >16} | potencia_ug2 (kW)\n"
              "REG4  {: >16} | energia_ug2 (RAW)\n"
              "REG5  {: >16} | comporta_value (RAW)\n"
              "REG6  {:016b} | comporta_flags ([fechada][p1]..[p5][aberta])\n".format(ip, porta, datetime.now(), *REGS))

        # Espera antes de atualizar o estado da "CLP"
        # Alterado para esperar o tempo nescessário para simular as amostras
        print("Tempo real entre amostras:    {:>8.3f}s".format(temporizador*CLPconfig.ESCALA_DE_TEMPO))
        print("Tempo até próxima atualização:  {:>6.3f}s".format(temporizador))
        sleep(temporizador)

finally:
    # Finaly para caso o servidor de problema aviar que fechou.
    print("Servidor fechado")
