import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from sys import stderr
from time import sleep
from logging import handlers

from src.dicionarios.reg_elipse import *

rootLogger = logging.getLogger()
if (rootLogger.hasHandlers()):
    rootLogger.handlers.clear()
rootLogger.setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()
logger.setLevel(logging.NOTSET)

logFormatter = logging.Formatter("%(asctime)s [SIM] %(message)s")

ch = logging.StreamHandler(stderr)  # log para sdtout
ch.setFormatter(logFormatter)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

fh = handlers.TimedRotatingFileHandler(filename="/opt/operacao-autonoma/logs/teste.log", when='midnight', interval=1, backupCount=7)
fh.setFormatter(logFormatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


l_tensoes = s.Servidores.rele["SE"].read_holding_registers(REG_RELE["SE"]["VAB"], 3)

logger.debug(f"[RELE][SE] VAB -> {l_tensoes[0]/1000 * 173.21 * 115}")
logger.debug(f"[RELE][SE] VBC -> {l_tensoes[1]/1000 * 173.21 * 115}")
logger.debug(f"[RELE][SE] VCA -> {l_tensoes[2]/1000 * 173.21 * 115}")