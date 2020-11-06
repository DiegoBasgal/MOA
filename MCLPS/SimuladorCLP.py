from datetime import datetime
from random import random, randint
from time import sleep
from pyModbusTCP.server import ModbusServer, DataBank
import os
import modbusconfig

'''
    Simulador de CLP com comunicação Modbus
'''


print("Iniciando Servidor/Slave Modbus ")

ip = modbusconfig.SLAVE_IP
porta = modbusconfig.SLAVE_PORT
temporizador = modbusconfig.CLP_REFRESH_RATE

REG = [0] * 16  # 16 registradores
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
    REG[7]:     Vazio
    REG[8]:     Vazio
    REG[9]:     Vazio
    REG[10]:    Vazio
    REG[11]:    Vazio
    REG[12]:    Vazio
    REG[13]:    Vazio
    REG[14]:    Vazio
    REG[15]:    Vazio


'''

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
              "DEC:\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {: >16}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n"
              "REG0  {:016b}\n".format(ip, porta, datetime.now(), *REGS,*REGS))

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
