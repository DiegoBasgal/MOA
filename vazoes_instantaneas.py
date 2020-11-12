from time import sleep
from datetime import datetime
from pyModbusTCP.client import ModbusClient
import MCLPS.CLP_config as CLPconfig
import logging
import usina


# Inicializando o logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler_loggin = logging.FileHandler('log_q_afluente.log')
# formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
# file_handler_loggin.setFormatter(formatter)
logger.addHandler(file_handler_loggin)

slave_ip = CLPconfig.SLAVE_IP
slave_porta = CLPconfig.SLAVE_PORT
temporizador = CLPconfig.CLP_REFRESH_RATE*2
primeira_amostra = True

client = ModbusClient(host=slave_ip,
                      port=slave_porta,
                      auto_open=True,
                      auto_close=True,
                      timeout=5,
                      unit_id=1)
while True:
    # Lê os registradores
    clp_conectada = True
    REGS = client.read_holding_registers(0, 7)
    if not REGS:
        if clp_conectada:
            logger.error("Erro na comunicação com a CLP, verifique a conexão.")
        clp_conectada = False
    else:
        if not clp_conectada:
            logger.info('Conexão reestabelecida com a CLP.')
            clp_conectada = True

        nv_montante = usina.nv_montante_zero + REGS[0]/usina.nv_montante_escala
        if primeira_amostra:
            primeira_amostra = False
        else:
            nv_montante_anterior = nv_montante
            nv_montante = usina.nv_montante_zero + REGS[0]/usina.nv_montante_escala
            pot_ug1 = REGS[1]/1000
            pot_ug2 = REGS[3]/1000
            estado_comporta = REGS[6]

            print(temporizador, nv_montante, pot_ug1, pot_ug2, estado_comporta)
            print(usina.q_afluente(temporizador, pot_ug1, pot_ug2, nv_montante,
                                   nv_montante_anterior, estado_comporta))

    sleep(temporizador)

