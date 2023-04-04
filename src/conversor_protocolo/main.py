
import os
import sys
import json
import pytz
import OpenOPC
import logging
import traceback
# import pywintypes
import logging.handlers as handlers

from sys import stderr
from time import sleep
from datetime import datetime

from conversor import *

# pywintypes.datetime = pywintypes.TimeType

# Criar pasta para logs
if not os.path.exists(os.path.join(os.path.dirname(__file__), "logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

# Método para conversão de data/horário GMT:-03:00 (Brasil)
def timeConverter(*args):
    return datetime.now(tz).timetuple()

# Método para criar logger principal
rootLogger = logging.getLogger()
if rootLogger.hasHandlers():
    rootLogger.handlers.clear()
rootLogger.setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)
if logger.hasHandlers():
    logger.handlers.clear()
logger.setLevel(logging.NOTSET)

tz = pytz.timezone("Brazil/East")
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] [OPC-DA] %(message)s")
logFormatter.converter = timeConverter

ch = logging.StreamHandler(stderr)
ch.setFormatter(logFormatter)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

# Criar arquivo de log OPC_DA
fh = handlers.TimedRotatingFileHandler(
    os.path.join(os.path.dirname(__file__), "logs", "OPC_DA.log"),
    when="midnight",
    interval=1,
    backupCount=7,
)
fh.setFormatter(logFormatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

main_conversor: bool = False

if main_conversor:
    tentativas: int = 0
    pronto: bool = False

    logger.info(f"Iniciando tradutor OPC DA.")

    while not pronto:
        tentativas += 1
        logger.debug(f"Tentativa -> {tentativas}/3")
        if tentativas == 3:
            logger.critical("Numero de tentativas excedidas na incialização. Encerrando conversor...")
            sys.exit(1)
        else:
            try:
                logger.info("Carregando arquivos de dados (\"dados.json\").")

                arquivo = os.path.join(os.path.dirname(__file__), "dados.json")
                with open(arquivo, "r") as file:
                    dados = json.load(file)

            except Exception as e:
                logger.exception(f"Houve um erro ao carregar o arquivo de dados. Exception: \"{repr(e)}\"")
                logger.debug(f"Traceback: {traceback.print_stack}")
                sleep(2)
                continue

            try:
                logger.info("Iniciando servidor de comunicação OPC DA / DNP 3.0")
                opc = OpenOPC.client()
                opc.connect('Elipse.OPCSvr.1')

            except Exception as e:
                logger.exception(f"Houve um erro ao inciar o servidro OPC DA. Exception: \"{repr(e)}\"")
                logger.debug(f"Traceback: {traceback.print_stack}")
                sleep(2)
                continue

            try:
                logger.info("Inciando classe de comunicação OPC DA / DNP 3.0")
                com = ExternoParaNativo(dados)
                com.opc_da = opc

            except Exception as e:
                logger.exception(f"Houve um erro ao instanciar a classe de comunicação. Exception: \"{repr(e)}\"")
                logger.debug(f"Traceback: {traceback.print_stack}")
                sleep(2)
                continue

            pronto = True

    logger.info("Inicialização completa, executando processo de conversação OPC DA.")

    while True:
        try:
            logger.debug("Nova leitura.")
            mudancas = com.detectar_mudanca()
            if mudancas != []:
                logger.debug("mudanca")
                [escrita_json(dados[key]) for key in mudancas]
            sleep(3)
        except Exception:
            logger.exception("Erro no loop principal. Encerrando tradutor...")
            sys.exit(1)