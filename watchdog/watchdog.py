import json
import logging
import os.path
from sys import stdout

from pyModbusTCP.client import ModbusClient
from datetime import datetime, timedelta
from time import sleep

# Inicializando o logger principal
from mensageiro.mensageiro_log_handler import MensageiroHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("MOA.log")
ch = logging.StreamHandler(stdout)
mh = MensageiroHandler()
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logFormatterSimples = logging.Formatter("[%(levelname)-5.5s]  %(message)s")
fh.setFormatter(logFormatter)
ch.setFormatter(logFormatter)
mh.setFormatter(logFormatterSimples)
fh.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)
mh.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(mh)

# Carrega as configurações e vars
config_file = os.path.join(os.path.dirname(__file__), 'watchdog_config.json')
with open(config_file, 'r') as file:
    config = json.load(file)
logger.debug("Config: {}".format(config))

modbus_client = ModbusClient(host=config['ip_slave'], port=config['port_slave'],
                             timeout=config['timeout_modbus'], unit_id=config['unit_id'],
                             auto_open=False, auto_close=False)

timestamp = []
moa_halted = False
while True:

    logger.debug("Pooling HB @ {}:{}".format(config['ip_slave'], config['port_slave']))
    try:
        if modbus_client.open():

            regs = modbus_client.read_holding_registers(0, 100)
            modbus_client.close()
            if regs is None:
                raise ConnectionError

            year = regs[0]
            month = regs[1]
            day = regs[2]
            hour = regs[3]
            minute = regs[4]
            second = regs[5]
            micros = regs[6]

            timestamp = datetime(year, month, day, hour, minute, second, micros)

        if (datetime.now() - timestamp) > timedelta(seconds=config['timeout_moa']):
            if not moa_halted:
                moa_halted = True
                logger.warning("O MOA está sem pulso desde {}! Tentando novamente a cada {}s.".format(timestamp.strftime("%Y-%m-%d, %H:%M:%S"), config['timeout_moa']))
            sleep(config['timeout_moa'])
        else:
            if moa_halted:
                moa_halted = False
                logger.info("O coração voltou a bater em  {}.".format(timestamp.strftime("%Y-%m-%d, %H:%M:%S"), config['timeout_moa']))


    except ConnectionError as e:
        logger.warning("Erro de conexão com o MOA. A última do atualização do HB foi em {}".format(e, timestamp.strftime("%Y-%m-%d, %H:%M:%S")))
    except Exception as e:
        logger.warning("Exception {} durante a conexão com o MOA".format(e))
    finally:
        modbus_client.close()
