from datetime import datetime
from random import random, randint
from time import sleep
from pyModbusTCP.server import ModbusServer, DataBank
import os
'''
    Simulador de CLP/Modbus
    REG0: Número aleatório entre 0 e 1000
    REG1: Número aleatório entre 0 e 1000
    REG2: Número aleatório entre 0 e 1000
    REG3: Flag aleatório
    REG4: Leitura int 
    REG5: Leitura int 
    REG6: Leitura bin 
    REG7: Leitura bin 
'''

ip = "172.21.15.13"
porta = 502

print("Iniciando Servidor/Slave Modbus ")

server = ModbusServer(host=ip, port=porta, no_block=True)
try:
    server.start()
    print("Servidor iniciado ({}:{})".format(ip, porta))
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        DataBank.set_words(0, [int(random()*1000), int(random()*1000), int(random()*1000)])
        DataBank.set_words(3, [int(2**(randint(0, 15)))])
        regs = DataBank.get_words(0, 8)

        print("TIME {}\n"
              "REG0 {: >16} | CLP\n"
              "REG1 {: >16} | CLP\n"
              "REG2 {: >16} | CLP\n"
              "REG3 {:016b} | CLP\n"
              "REG4 {: >16} | MOA\n"
              "REG5 {: >16} | E3 \n"
              "REG6 {:016b} | MOA\n"
              "REG7 {:016b} | E3 ".format(datetime.now(), *regs))

        # bit 15 do reg6 (MOA que controla)
        if(regs[6] >= 2 ** 15):
            print("MOA disparou o bit 15 do REG6!")

        # bit 15 do reg7 (E3 que controla
        if (regs[7] >= 2 ** 15):
            print("Elipse E3 disparou o bit 15 do REG7!")

        sleep(0.1)

finally:
    print("Servidor fechado")
