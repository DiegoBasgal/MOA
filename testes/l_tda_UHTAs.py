import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from logging.config import fileConfig

from src.dicionarios.reg import *


fileConfig("/opt/operacao-autonoma/testes/log_testes.ini")
log = logging.getLogger("teste")


l_uhta_operando: "dict[str, l.LeituraModbus]" = {}

for u in range(2):
    l_uhta_operando[f'UHTA{u+1}'] = l.LeituraModbusBit(
        client=s.Servidores.clp['SA'],
        registrador=[12915, 0],
        descricao=f"[TDA][UHTA{u+1}] Operando"
    )


while True:
    for u in range(2):
        log.debug(f"{l_uhta_operando[f'UHTA{u+1}'].descricao}: {l_uhta_operando[f'UHTA{u+1}'].valor}")
        log.debug("")
    log.debug("")
    sleep(8)