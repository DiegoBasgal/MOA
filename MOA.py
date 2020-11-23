from time import sleep
from time import time_ns
from datetime import datetime
from pyModbusTCP.client import ModbusClient
import MCLPS.CLP_config as CLPconfig
import logging
import usina

## Inicializando o logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)
# LOG to file
fileHandler = logging.FileHandler("simulador_clp.log")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)
# LOG to console
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

slave_ip = CLPconfig.SLAVE_IP
slave_porta = CLPconfig.SLAVE_PORT
temporizador = CLPconfig.CLP_REFRESH_RATE*2
primeira_amostra = True
nv_montante_anterior = 0

client = ModbusClient(host=slave_ip,
                      port=slave_porta,
                      timeout=5,
                      unit_id=1)

t0 = time_ns()

while True:
    logging.info('Estabelecendo conexão com a CLP')
    client.open()
    if client.is_open():
        logging.info('Estabelecida conexão com a CLP')
        try:
            while client.is_open():
                # Lê os registradores
                REGS = client.read_holding_registers(0, 7)

                nv_montante = usina.nv_montante_zero + REGS[0]/usina.nv_montante_escala
                if primeira_amostra:
                    primeira_amostra = False
                else:
                    nv_montante_anterior = nv_montante
                    nv_montante = usina.nv_montante_zero + REGS[0]/usina.nv_montante_escala

                if nv_montante <= 643.3:
                    pot_ug1 = 0
                    pot_ug2 = 0

                if nv_montante > 643.49:
                    pot_ug1 = 2500
                    pot_ug2 = 0

                estado_comporta = 0
                client.write_single_register(1, pot_ug1)
                client.write_single_register(3, pot_ug2)
                client.write_single_register(5, estado_comporta)
                client.write_single_register(6, estado_comporta)

                delta_t = (time_ns() - t0) * (10 ** 9)
                t0 = time_ns()

                print(nv_montante, pot_ug1, pot_ug2, estado_comporta,
                      usina.q_afluente(delta_t, pot_ug1/1000, pot_ug2/1000, nv_montante, nv_montante_anterior, estado_comporta))

                sleep(0.1)
        except KeyboardInterrupt:
            logging.info('O usuário interrompeu a aplicação via teclado (pressionado ctrl+c?).')
            break
        finally:
            client.close()
    else:
        logging.error("Erro na comunicação com a CLP, verifique a conexão.")
        sleep(5)

