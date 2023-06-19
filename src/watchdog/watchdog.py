"""
watchdog.py

Este módulo funciona como cão de guarda para o módulo de operação autônoma, lendo o heartbeat e enviando avisos conforme necessário.
As configurações desde módulo estão no arquivo "watchdog_config.json"

"""

import logging
import os.path

from time import sleep
from mariadb.connectionpool import *
from datetime import datetime, timedelta

from src.mensageiro.msg_log_handler import MensageiroHandler

if not os.path.exists(os.path.join(os.path.dirname(__file__), "logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(os.path.join(os.path.dirname(__file__), "logs", "watchdog.log"))
mh = MensageiroHandler()

logFormatterSimples = logging.Formatter("[%(levelname)-5.5s] [WATCHDOG] %(message)s")

fh.setFormatter(logFormatterSimples)
mh.setFormatter(logFormatterSimples)

fh.setLevel(logging.DEBUG)
mh.setLevel(logging.INFO)

logger.addHandler(fh)
logger.addHandler(mh)

timestamp = 0
moa_halted = False

config = {
    "ip_banco": "192.168.0.111",
    "porta_banco": 3306,
    "timeout_moa": 30,
    "nome_usina": "SEB",
    "nome_local": "Casa de Força"
}

cnx = mariadb.ConnectionPool(
    pool_name="my_pool",
    pool_size=10,
    pool_validation_interval=250,
    host='192.168.0.111',
    port=3306,
    user='moa',
    password='&264H3$M@&z$',
    database='debug'
)

while True:

    try:
        if conn := cnx.get_connection():
            conn.cursor.execute('SELECT ts FROM moa_debug ORDER BY ts DESC LIMIT 1;')
            val = conn.cursor.fetchone()[0]
            conn.close()

            if val is None:
                logger.warning("Não foi possível extrair o timestamp do banco.")

            if (datetime.now() - timestamp) > timedelta(seconds=config["timeout_moa"]):
                if not moa_halted:
                    moa_halted = True
                    logger.warning(f"Conexão do MOA em {config['nome_usina']} com {config['nome_local']} falhou ({timestamp.strftime('%Y-%m-%d, %H:%M:%S')})! Tentando novamente a cada {config['timeout_moa']}s.")
                sleep(config["timeout_moa"])

            else:
                if moa_halted:
                    moa_halted = False
                    logger.info(f"O coração voltou a bater em {timestamp.strftime('%Y-%m-%d, %H:%M:%S')}.")
        else:
            raise ConnectionError("modbus_client.open() failed.")

    except Exception as e:
        logger.warning(f"Exeption durante a conexão do MOA em {config['nome_usina']} com {config['nome_local']}. A última do atualização do HB foi em {timestamp.strftime('%Y-%m-%d, %H:%M:%S')}. Exception: {e}")
        continue

    finally:
        modbus_client.close()
        sleep(config["timeout_moa"])


