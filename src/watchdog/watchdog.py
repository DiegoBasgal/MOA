"""
watchdog.py

Este módulo funciona como cão de guarda para o módulo de operação autônoma, lendo o heartbeat e enviando avisos conforme necessário.
As configurações desde módulo estão no arquivo "watchdog_config.json"

"""

from datetime import datetime, timedelta
from pyModbusTCP.client import ModbusClient
from src.mensageiro.mensageiro_log_handler import MensageiroHandler
from sys import stdout
from time import sleep
import json
import logging
import os.path

# Inicializando o logger principal
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if not os.path.exists("logs/"):
    os.mkdir("logs/")
fh = logging.FileHandler("logs/watchdog.log")  # log para arquivo
ch = logging.StreamHandler(stdout)  # log para linha de comando
mh = MensageiroHandler()  # log para telegram e voip
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

# Carrega as configurações
config_file = os.path.join(os.path.dirname(__file__), 'watchdog_config.json')
with open(config_file, 'r') as file:
    config = json.load(file)
logger.debug("Config: {}".format(config))

# Inicialização
timestamp = 0
moa_halted = False
modbus_client = ModbusClient(host=config['ip_slave'],
                             port=config['port_slave'],
                             timeout=config['timeout_modbus'],
                             unit_id=config['unit_id'],
                             auto_open=False,
                             auto_close=False)

# Ciclo de verificação do MOA
while True:
    # Continuar verificando até término do processo.
    logger.debug("Pooling HB @ {}:{}".format(config['ip_slave'], config['port_slave']))

    # Podem ocorrer erros durtante a comunicação.
    try:
        if modbus_client.open():
            # Se há conexão, lê os registradores do HB
            regs = modbus_client.read_holding_registers(0, 7)
            modbus_client.close()
            if regs is None:
                # Se os registradores estiverem vazios, levantar uma exception deste erro
                raise ConnectionError

            # Monta o datetime do HB
            year = regs[0]
            month = regs[1]
            day = regs[2]
            hour = regs[3]
            minute = regs[4]
            second = regs[5]
            micros = regs[6]
            timestamp = datetime(year, month, day, hour, minute, second, micros)
            logger.debug("HB em {}!".format(timestamp.strftime("%Y-%m-%d, %H:%M:%S")))

            # Verifica-se se o HB é antigo
            if (datetime.now() - timestamp) > timedelta(seconds=config['timeout_moa']):
                # Se for mais velho que o timeout o moa está travado.
                if not moa_halted:
                    # Avisar da primeira vez
                    moa_halted = True
                    logger.warning("O MOA está sem pulso desde {}! Tentando novamente a cada {}s.".format(timestamp.strftime("%Y-%m-%d, %H:%M:%S"), config['timeout_moa']))
                # Espera antes de testar novamente
                sleep(config['timeout_moa'])
            else:
                # Se foir mais novo que o timeout o moa não está sendo considerado como travado.
                if moa_halted:
                    # Se estav antes, avisar que voltou a respoder.
                    moa_halted = False
                    logger.info("O coração voltou a bater em  {}.".format(timestamp.strftime("%Y-%m-%d, %H:%M:%S")))
        else:
            # Se a conexão não abriu, levantar uma exception deste erro
            raise ConnectionError("modbus_client.open() failled.")

    # Captura de exceptions durtante a comunicação. Caso ocorrom, continuar o loop.
    except ConnectionError as e:
        logger.warning("Erro de conexão com o MOA. A última do atualização do HB foi em {}. Exception: {}".format(
            timestamp.strftime("%Y-%m-%d, %H:%M:%S"), e))
        continue
    except Exception as e:
        logger.warning("Exception {} durante a conexão com o MOA".format(e))
        continue
    finally:
        # Fecha a comunicação e espera antes da próxima comunicação
        modbus_client.close()
        sleep(config['timeout_moa'])
