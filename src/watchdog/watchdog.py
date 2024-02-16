import logging
import os.path

from time import sleep
from mariadb.connectionpool import *
from logging.config import fileConfig
from datetime import datetime, timedelta

if not os.path.exists(os.path.join(os.path.dirname(__file__), "logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

fileConfig("/opt/operacao-autonoma/logger_config.ini")
logger = logging.getLogger("logger")

timestamp = 0
moa_halted = False

config = {
    "timeout_moa": 30,
    "nome_usina": "SEB",
    "nome_local": "Casa de Força"
}

cnx = mariadb.ConnectionPool(
    pool_name="watchdog",
    pool_size=2,
    pool_validation_interval=250,
    host='192.168.0.113',
    port=3306,
    user='supervisorio',
    password='8z43WW3sHPRnfg',
    database='debug'
)

while True:
    try:
        if conn := cnx.get_connection():
            conn.cursor.execute('SELECT ts FROM moa_debug ORDER BY ts DESC LIMIT 1;')
            timestamp = conn.cursor.fetchone()[0]
            conn.close()

            if timestamp in (None, 0):
                logger.warning("Não foi possível extrair o timestamp do banco.")

            if (datetime.now() - timestamp) > timedelta(seconds=config["timeout_moa"]):
                if not moa_halted:
                    moa_halted = True
                    logger.warning(f"Conexão do MOA em {config['nome_usina']} / {config['nome_local']} falhou ({timestamp.strftime('%Y-%m-%d, %H:%M:%S')})! Tentando novamente a cada {config['timeout_moa']}s.")
                sleep(config["timeout_moa"])

            else:
                if moa_halted:
                    moa_halted = False
                    logger.info(f"O coração voltou a bater em {timestamp.strftime('%Y-%m-%d, %H:%M:%S')}.")
        else:
            raise ConnectionError("Erro ao conectar com o banco de dados MariaDB.")

    except Exception as e:
        logger.warning(f"Exeption durante a conexão do MOA em {config['nome_usina']} / {config['nome_local']}. A última do atualização foi em {timestamp.strftime('%Y-%m-%d, %H:%M:%S')}. Exception: {e}")
        continue

    finally:
        conn.close()
        sleep(config["timeout_moa"])