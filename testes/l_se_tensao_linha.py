import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from logging.config import fileConfig

from src.dicionarios.reg import *


fileConfig("/opt/operacao-autonoma/testes/log_testes.ini")
log = logging.getLogger("teste")


l_tensao_r = l.LeituraModbus(
    s.Servidores.clp['SA'],
    25 + 12764,
    escala=0.01,
    descricao="[SE] Tensão Fase RS"
)
l_tensao_s = l.LeituraModbus(
    s.Servidores.clp['SA'],
    26 + 12764,
    escala=0.01,
    descricao="[SE] Tensão Fase ST"
)
l_tensao_t = l.LeituraModbus(
    s.Servidores.clp['SA'],
    27 + 12764,
    escala=0.01,
    descricao="[SE] Tensão Fase TR"
)


while True:
    log.debug(f"{l_tensao_r.descricao}: {l_tensao_r.valor}")
    log.debug("")
    log.debug(f"{l_tensao_s.descricao}: {l_tensao_s.valor}")
    log.debug("")
    log.debug(f"{l_tensao_t.descricao}: {l_tensao_t.valor}")
    log.debug("")
    sleep(5)