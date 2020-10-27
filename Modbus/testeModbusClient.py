from time import sleep
from datetime import datetime
from pyModbusTCP.client import ModbusClient

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

ip_slave = "172.21.15.13"
porta_slave = 502

def escrever_no_log(linha):
    linha = "'{}','".format(datetime.now().strftime("%H:%M:%S"))+linha+"'\n"
    print(linha)
    with open('log.csv', 'a+') as file:
        file.write(linha)
    return 0


client = ModbusClient(host=ip_slave,
                      port=porta_slave,
                      auto_open=True,
                      auto_close=True,
                      timeout=5,
                      unit_id=1)

#Inicio do código
escrever_no_log("Iniciando")

regs = [0]*8
alarme = [False]*8
alarme_flag = False
alarme_flag_2 = False
flags = 0
contador_reg4 = 0
contador_reg6 = 2

while True:

    # Lê os registradores
    regs = client.read_holding_registers(0, 8)

    # REG0-2 rand 0 - 1000, tem alarme de HIGH se >900
    for i in range(3):
        if not alarme[i] and regs[i] > 900:
            escrever_no_log("REG{} mudou para HIGH (>900).".format(i))
            alarme[i] = True
        if alarme[i] and regs[i] <= 900:
            escrever_no_log("REG{} normalizado.".format(i))
            alarme[i] = False

    # REG3 tem flags, alerta na flag 2 (2x0000000000000100)
    if not alarme_flag and (regs[3] & 4):
        escrever_no_log("Flag2 mudou para HIGH.")
        alarme_flag = True
    if alarme_flag and not (regs[3] & 4):
        escrever_no_log("Flag2 mudou para LOW.")
        alarme_flag = False

    # REG5 rand 0 - 1000, tem alarme de HIGH se >900
    i = 5
    if not alarme[i] and regs[i] > 900:
        escrever_no_log("REG{} mudou para HIGH (>900).".format(i))
        alarme[i] = True
    if alarme[i] and regs[i] <= 900:
        escrever_no_log("REG{} normalizado.".format(i))
        alarme[i] = False

    # REG7 tem flags, alerta na flag 0 + flag 6 (2x0000000001000001)
    # A Flag0 sempre vai estar em HIGH nesse reg
    if not alarme_flag_2 and (regs[7] & 65):
        escrever_no_log("Flag6 mudou para HIGH.")
        alarme_flag_2 = True
    if alarme_flag_2 and not (regs[7] & 65):
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



