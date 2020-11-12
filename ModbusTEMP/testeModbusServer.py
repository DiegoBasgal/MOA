from datetime import datetime
from random import random, randint
from time import sleep
from pyModbusTCP.server import ModbusServer, DataBank
import os
import modbusconfig
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
print("Iniciando Servidor/Slave Modbus ")

ip = modbusconfig.SLAVE_IP
porta = modbusconfig.SLAVE_PORT
temporizador = modbusconfig.CLP_REFRESH_RATE

REG = [0] * 10  # 10 registradores

server = ModbusServer(host=ip, port=porta, no_block=True)
try:
    server.start()
    while True:
        # Limpa a interface de linha
        os.system('cls' if os.name == 'nt' else 'clear')

        # Escreve os valores rand de REG0 - REG2
        DataBank.set_words(0, [int(random()*1000), int(random()*1000), int(random()*1000)])
        # Escreve (apenas) uma flag aleatória
        DataBank.set_words(3, [int(2**(randint(0, 15)))])

        # Carrega os REGs, da memória, sem conectar.
        REGS = DataBank.get_words(0, 10)

        print("###########\n"
              "#  PyCLP  #\n"
              "###########\n\n"
              "Servidor/Slave ModbusTCP em {}:{}\n\n"
              "TIME {}\n\n"
              "REG0 {: >16} | CLP\n"
              "REG1 {: >16} | CLP\n"
              "REG2 {: >16} | CLP\n"
              "REG3 {:016b} | CLP\n"
              "REG4 {: >16} | MOA\n"
              "REG5 {: >16} | E3 \n"
              "REG6 {:016b} | MOA\n"
              "REG7 {:016b} | E3 \n"
              "REG8 {:016b} | HB MOA \n"
              "REG9 {:016b} | HM E3 \n".format(ip, porta, datetime.now(), *REGS))

        # Verifica o bit 15 do reg6 (MOA que controla)
        if REGS[6] & (2**15):
            print("MOA disparou o bit 15 do REG6!")

        # Verifica o bit 15 do reg7 (E3 que controla
        if REGS[7] & (2**15):
            print("Elipse E3 disparou o bit 15 do REG7!")

        # Verifica o bit 0 do reg8 (HB MOA)
        if REGS[8]:
            print("MOA ONLINE")

        # Verifica o bit 0 do reg9 (HB E3)
        if REGS[9]:
            print("E3 ONLINE")

        # Reinicia o HB MOA e HB E3
        DataBank.set_words(8, [0, 0])

        # Espera antes de atualizar o estado da "CLP"
        sleep(temporizador)

finally:
    # Finaly para caso o servidor de problema aviar que fechou.
    print("Servidor fechado")
