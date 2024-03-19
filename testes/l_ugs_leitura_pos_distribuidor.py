import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from logging.config import fileConfig

from src.dicionarios.reg import *


fileConfig("/opt/operacao-autonoma/testes/log_testes.ini")
log = logging.getLogger("teste")


l_distribuidor: "dict[str, l.LeituraModbus]" = {}

for u in range(4):
    l_distribuidor[f'UG{u+1}'] = l.LeituraModbus(
        client=s.Servidores.clp[f'UG{u+1}'],
        registrador=47 + 12764,
        escala=0.1,
        descricao=f"[UG{u+1}] Posição Distribuidor"
    )


while True:
    for u in range(4):
        log.debug(f"{l_distribuidor[f'UG{u+1}'].descricao}: {l_distribuidor[f'UG{u+1}'].valor:0.2f} %")
        log.debug("")
    log.debug("")
    sleep(8)