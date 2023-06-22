import json
import logging
import os.path

from sys import stdout
from time import sleep
from datetime import datetime, timedelta
from pyModbusTCP.client import ModbusClient

from src.mensageiro.msg_log_handler import MensageiroHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not os.path.exists(os.path.join(os.path.dirname(__file__), "logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

fh = logging.FileHandler(os.path.join(os.path.dirname(__file__), "logs", "watchdog.log"))
ch = logging.StreamHandler(stdout)
mh = MensageiroHandler()

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [WATCHDOG] %(message)s")
logFormatterSimples = logging.Formatter("[%(levelname)-5.5s] [WATCHDOG] %(message)s")

fh.setFormatter(logFormatter)
ch.setFormatter(logFormatter)
mh.setFormatter(logFormatterSimples)
fh.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)
mh.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(mh)

config_file = os.path.join(os.path.dirname(__file__), "watchdog_config.json")
with open(config_file, "r") as file:
    config = json.load(file)
logger.debug(f"Config: {config}")

timestamp = 0
moa_halted = False
modbus_client = ModbusClient(
    host=config["ip_slave"],
    port=config["port_slave"],
    timeout=config["timeout_modbus"],
    unit_id=config["unit_id"],
    auto_open=False,
    auto_close=False,
)

while True:
    logger.debug(f"Pooling HB @ {config['ip_slave']}:{config['port_slave']}")

    try:
        if modbus_client.open():
            regs = modbus_client.read_holding_registers(0, 7)
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
            logger.debug(f"HB em {timestamp.strftime('%Y-%m-%d, %H:%M:%S')}!")

            if (datetime.now() - timestamp) > timedelta(seconds=config["timeout_moa"]):
                if not moa_halted:
                    moa_halted = True
                    logger.warning(f"Conexão do MOA em {config['nome_usina']} com {config['nome_local']} falhou ({timestamp.strftime('%Y-%m-%d, %H:%M:%S')})! Tentando novamente a cada {config['timeout_moa']}s.")
                sleep(config["timeout_moa"])
            else:
                if moa_halted:
                    moa_halted = False
                    logger.info(f"O coração voltou a bater em  {timestamp.strftime('%Y-%m-%d, %H:%M:%S')}.")
        else:
            raise ConnectionError("modbus_client.open() failed.")

    except ConnectionError as e:
        logger.warning(f"Erro de conexão do MOA em {config['nome_usina']} com {config['nome_local']}. A última do atualização do HB foi em {timestamp.strftime('%Y-%m-%d, %H:%M:%S')}. Exception: {e}")
        continue
    except Exception as e:
        logger.warning(f"Exeption durante a conexão do MOA em {config['nome_usina']} com {config['nome_local']}. A última do atualização do HB foi em {timestamp.strftime('%Y-%m-%d, %H:%M:%S')}. Exception: {e}")
        continue
    finally:
        modbus_client.close()
        sleep(config["timeout_moa"])
