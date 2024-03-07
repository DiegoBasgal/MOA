import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from logging.config import fileConfig

from src.dicionarios.reg import *


fileConfig("/opt/operacao-autonoma/testes/log_testes.ini")
log = logging.getLogger("teste")


l_posicao: "dict[str, l.LeituraModbus]" = {}

for u in range(2):
    l_posicao[f'CP{u+1}'] = l.LeituraModbus(
        client=s.Servidores.clp['SA'],
        registrador=165 + 12764 if u+1==1 else 167 + 12764,
        descricao=f"[AD][CP{u+1}] Posição"
    )


while True:
    for u in range(2):
        log.debug(f"{l_posicao[f'CP{u+1}'].descricao}: {l_posicao[f'CP{u+1}'].valor}")
        log.debug("")
    log.debug("")
    sleep(8)