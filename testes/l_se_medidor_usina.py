import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from logging.config import fileConfig

from src.dicionarios.reg import *


fileConfig("/opt/operacao-autonoma/testes/log_testes.ini")
log = logging.getLogger("teste")


medidor_usina = l.LeituraModbus(
    s.Servidores.clp["SA"],
    35 + 12764,
    descricao="[SE] Leitura Medidor Usina"
)


while True:
    log.debug(f"{medidor_usina.descricao}: {medidor_usina.valor}")
    log.debug("")
    sleep(5)