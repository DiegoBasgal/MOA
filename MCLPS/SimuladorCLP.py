from datetime import datetime
from random import random, randint
from time import sleep
from pyModbusTCP.server import ModbusServer, DataBank
import os
import CLPconfig

'''
    Simulador de CLP com comunicação Modbus
'''


print("Iniciando Servidor/Slave Modbus ")

ip = CLPconfig.SLAVE_IP
porta = CLPconfig.SLAVE_PORT
temporizador = CLPconfig.CLP_REFRESH_RATE

REG = [0] * 7  # 16 registradores
'''
    Detalhamento dos conteúdos dos registradores

    REG[0]:     nivel_montante
    REG[1]:     potencia_ug1
    REG[2]:     energia_ug1
    REG[3]:     potencia_ug2
    REG[4]:     energia_ug2
    REG[5]:     comporta_value
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
    while True:
        # Limpa a interface de linha
        os.system('cls' if os.name == 'nt' else 'clear')

        # Escreve os valores rand de REG0 - REG2
        DataBank.set_words()

        # Carrega os REGs, da memória, sem conectar.
        REGS = DataBank.get_words(0, 10)

        print("###########\n"
              "#  PyCLP  #\n"
              "###########\n\n"
              "Servidor/Slave ModbusTCP em {}:{}\n\n"
              "TIME {}\n\n"
              "REG0 {: >16} | nivel_montante\n"
              "REG1 {: >16} | potencia_ug1\n"
              "REG2 {: >16} | energia_ug1\n"
              "REG3 {: >16} | potencia_ug1\n"
              "REG4 {: >16} | energia_ug1\n"
              "REG5 {: >16} | comporta_value\n"
              "REG6 {:016b} | comporta_flags\n".format(ip, porta, datetime.now(), *REGS))

        # Espera antes de atualizar o estado da "CLP"
        sleep(temporizador)

finally:
    # Finaly para caso o servidor de problema aviar que fechou.
    print("Servidor fechado")
