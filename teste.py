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


l_1 = l.LeituraModbusBit(s.Servidores.clp['SA'], REG_SASE["CARREGADOR_BATERIAS_FALHA"], descricao="[SA] Falha Carregador de Baterias")
# l_2 = l.LeituraModbusBit(s.Servidores.clp['UG1'], REG_UG["UG1"]["VB_VALVULA_BORBOLETA_FECHADA"], descricao="[UG1] Valvula Borboleta Fechada")
# l_3 = l.LeituraModbusBit(s.Servidores.clp['UG1'], REG_UG["UG1"]["VB_VALVULA_BYPASS_ABERTA"], descricao="[UG1] Valvula Bypass Aberta")
# l_4 = l.LeituraModbusBit(s.Servidores.clp['UG1'], REG_UG["UG1"]["VB_VALVULA_BYPASS_FECHADA"], descricao="[UG1] Valvula Bypass Fechada")
# pd_b2p = l.LeituraModbusBit(s.Servidores.clp['SA'], REG_SASE["POCO_DRENAGEM_BOMBA_2_AUTOMATICO"], descricao="[SA]  Poço de Drenagem Bomba 2 Automático")

while True:
    logger.debug(f"{l_1.descricao} -> {l_1.valor}")
    # logger.debug(f"{l_2.descricao} -> {l_2.valor}")
    # logger.debug(f"{l_3.descricao} -> {l_3.valor}")
    # logger.debug(f"{l_4.descricao} -> {l_4.valor}")
    print("")
    sleep(2)