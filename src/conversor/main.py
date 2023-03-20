
import os
import sys
import json
import pytz
import OpenOPC
import logging
import traceback
# import pywintypes
import logging.handlers as handlers

from time import sleep
from datetime import datetime

from client import ConversorOpc

# pywintypes.datetime = pywintypes.TimeType

# Criar pasta para logs
if not os.path.exists(os.path.join(os.path.dirname(__file__), "logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

# Método para conversão de data/horário GMT:-03:00 (Brasil)
def timeConverter() -> datetime:
    tz = pytz.timezone("Brazil/East")
    return datetime.now(tz).timetuple()

# Método de leitura do arquivo de dados json
def leitura_json() -> dict:
    arquivo = os.path.join(os.path.dirname(__file__), "dados.json")
    with open(arquivo, "r") as file:
        return json.load(file)

# Método de escrever no arquivo de dados json após mudanças
def escrita_json(valor) -> None:
    arquivo = os.path.join(os.path.dirname(__file__), "dados.json")
    with open(arquivo, "w") as file:
        json.dump(valor, file, indent=4)

# Método para criar logger principal
def criar_logger() -> logging:
    logger = logging.getLogger(__name__)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(logging.NOTSET)

    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] [OPC-DA] %(message)s")
    logFormatter.converter = timeConverter

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

    return logger

if __name__ == "__main__":
    logger = criar_logger()

    logger.info("Iniciando tradutor OPC DA.")
    tentativas: int = 0

    while tentativas <= 3:
        tentativas += 1
        try:
            logger.info("Carregando arquivos de dados (\"dados.json\").")
            dados = leitura_json

        except Exception as e:
            logger.exception(f"Houve um erro ao carregar o arquivo de dados. Exception: \"{repr(e)}\"")
            logger.exception(f"Traceback: {traceback.print_stack}")
            sleep(2)
            continue

        try:
            logger.info("Iniciando servidor de comunicação OPC DA / DNP 3.0")
            opc = OpenOPC.client()
            opc.connect('Elipse.OPCSvr.1')

        except Exception as e:
            logger.exception(f"Houve um erro ao inciar o servidro OPC DA. Exception: \"{repr(e)}\"")
            logger.exception(f"Traceback: {traceback.print_stack}")
            sleep(2)
            continue

        try:
            logger.info("Inciando classe de comunicação OPC DA / DNP 3.0")
            com = ConversorOpc(opc, dados)

        except Exception as e:
            logger.exception(f"Houve um erro ao instanciar a classe de comunicação. Exception: \"{repr(e)}\"")
            logger.exception(f"Traceback: {traceback.print_stack}")
            sleep(2)
            continue

    logger.info("Inicialização completa, executando processo de conversação OPC DA.")

    while True:
        try:
            mudancas: list = com.detectar_mudanca()
            [escrita_json(dados[key]) for key in mudancas if mudancas != []]
            sleep(3)
        except Exception:
            logger.exception("Erro no loop principal. Encerrando tradutor...")
            sys.exit(1)