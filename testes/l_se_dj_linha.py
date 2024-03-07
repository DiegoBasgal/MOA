import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from logging.config import fileConfig

from src.dicionarios.reg import *


fileConfig("/opt/operacao-autonoma/testes/log_testes.ini")
log = logging.getLogger("teste")


l_dj_linha = l.LeituraModbusBit(
    s.Servidores.clp['SA'],
    [21 + 12764, 1],
    descricao="[SE] Disjuntor Linha"
)

while True:
    log.debug(f"{l_dj_linha.descricao}: {l_dj_linha.valor}")
    log.debug("")
    sleep(5)