__version__ = "0.2"
__author__ = "Lucas Lavratti", "Diego Basgal"
__description__ = "Este módulo corresponde a implementação do Watchdog do MOA."

import time
import os.path
import traceback
import logging
import logging.handlers as handlers

from datetime import datetime

from mariadb.connectionpool import *
from mensageiro.msg_log_handler import MensageiroHandler


rootLogger = logging.getLogger()
if (rootLogger.hasHandlers()):
    rootLogger.handlers.clear()
rootLogger.setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()
logger.setLevel(logging.NOTSET)

if not os.path.exists(os.path.join(os.path.dirname(__file__), "logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] [WATCHDOG] %(message)s")
logFormatterSimples = logging.Formatter("[WATCHDOG] %(message)s")

fh = handlers.TimedRotatingFileHandler(os.path.join(os.path.dirname(__file__),"logs","WATCHDOG.log"),when='midnight',interval=1,backupCount=7)
fh.setFormatter(logFormatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

mh = MensageiroHandler()
mh.setFormatter(logFormatterSimples)
mh.setLevel(logging.INFO)
logger.addHandler(mh)

timestamp = 0
moa_halted = False

config = {
    "timeout_moa": 60,
    "nome_usina": "Covó"
}

cnx = mariadb.ConnectionPool(
    host='192.168.70.20',
    user='watchdog',
    password='HEz4eYfeLXShTY',
    database='debug',
    pool_name="Watchdog",
    pool_size=10,
    pool_validation_interval=250,
)

while True:
    try:
        if conn := cnx.get_connection():
            cursor = conn.cursor()
            cursor.execute('SELECT ts FROM moa_debug ORDER BY ts DESC LIMIT 1;')
            timestamp = cursor.fetchone()[0]
            conn.commit()

            if timestamp in (None, 0):
                raise ValueError("Não foi possível extrair o timestamp do Banco de Dabos.")
            
            if (time.time() - timestamp) > config["timeout_moa"]:
                if not moa_halted:
                    moa_halted = True
                    logger.warning(f"Comunicação com MOA em {config['nome_usina']}, falhou às: \"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\"!")
                    logger.info(f"Tentando novamente à cada: {config['timeout_moa']}s.")
                    conn.close()

                time.sleep(config["timeout_moa"])

            else:
                logger.debug("MOA Rodando...")
                conn.close()

                if moa_halted:
                    moa_halted = False
                    logger.info(f"Comunicação com MOA re-estabelecida em: \"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\".")

        else:
            raise ConnectionError("Erro ao conectar com o banco de dados MariaDB.")

    except Exception as e:
        logger.warning(f"Houve um erro com o Watchdog MOA em {config['nome_usina']}.")
        logger.info(f"A última do atualização foi em: \"{timestamp}\".")
        logger.debug(traceback.format_exc())
        continue

    finally:
        conn.close()
        time.sleep(config["timeout_moa"])