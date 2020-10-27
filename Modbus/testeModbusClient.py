from time import sleep
from datetime import datetime
from pyModbusTCP.client import ModbusClient
import modbusconfig

'''
    REG0: Leitura int
    REG1: Leitura int
    REG2: Leitura int
    REG3: Leitura bin
    REG4: Escrita int : 1000->1009
    REG5: Leitura int 
    REG6: Escrita bin : 2 -> 2**15
    REG7: Leitura bin
'''

slave_ip = modbusconfig.SLAVE_IP
slave_porta = modbusconfig.SLAVE_PORT
temporizador = modbusconfig.DEFAULT_REFRESH_RATE


def escrever_no_log(linha):

    '''
    Esta função deve ser refeita.
    '''

    linha = "'{}','".format(datetime.now().strftime("%H:%M:%S"))+linha+"'\n"
    print(linha)
    with open('log.csv', 'a+') as file:
        file.write(linha)
    return 0


client = ModbusClient(host=slave_ip,
                      port=slave_porta,
                      auto_open=True,
                      auto_close=True,
                      timeout=5,
                      unit_id=1)

#Inicio do código
escrever_no_log("Iniciando")

REGS = [0] * 8
alarme = [False]*8
alarme_flag = False
alarme_flag_2 = False
flags = 0
contador_reg4 = 0
contador_reg6 = 2

while True:

    # Lê os registradores
    REGS = client.read_holding_registers(0, 8)

    # REG0-2 rand 0 - 1000, tem alarme de HIGH se >900
    for i in range(3):
        if not alarme[i] and REGS[i] > 900:
            escrever_no_log("REG{} mudou para HIGH (>900).".format(i))
            alarme[i] = True
        if alarme[i] and REGS[i] <= 900:
            escrever_no_log("REG{} normalizado.".format(i))
            alarme[i] = False

    # REG3 tem flags, alerta na flag 2 (2x0000000000000100)
    if not alarme_flag and (REGS[3] & 4):
        escrever_no_log("Flag2 mudou para HIGH.")
        alarme_flag = True
    if alarme_flag and not (REGS[3] & 4):
        escrever_no_log("Flag2 mudou para LOW.")
        alarme_flag = False

    # REG5 rand 0 - 1000, tem alarme de HIGH se >900
    i = 5
    if not alarme[i] and REGS[i] > 900:
        escrever_no_log("REG{} mudou para HIGH (>900).".format(i))
        alarme[i] = True
    if alarme[i] and REGS[i] <= 900:
        escrever_no_log("REG{} normalizado.".format(i))
        alarme[i] = False

    # REG7 tem flags, alerta na flag 0 + flag 6 (2x0000000001000001)
    # A Flag0 sempre vai estar em HIGH nesse reg
    if not alarme_flag_2 and (REGS[7] & 65):
        escrever_no_log("Flag6 mudou para HIGH.")
        alarme_flag_2 = True
    if alarme_flag_2 and not (REGS[7] & 65):
        escrever_no_log("Flag6 mudou para LOW.")
        alarme_flag_2 = False

    # Escrita nos registradores

    # REG4 é escrito sequencialmente com 1000 a 1009
    client.write_multiple_registers(4, [(contador_reg4+1000)])
    contador_reg4 += 1
    if contador_reg4 > 9:
        contador_reg4 = 0

    # REG6 é escrito sequencialemnte flags de 0 a 15 (2**15)
    client.write_multiple_registers(6, [contador_reg6])
    contador_reg6 = contador_reg6 << 1
    if contador_reg6 >= 2**16:
        contador_reg6 = 2

    sleep(0.5)



