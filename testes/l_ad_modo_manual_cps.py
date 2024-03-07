import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from logging.config import fileConfig

from src.dicionarios.reg import *


fileConfig("/opt/operacao-autonoma/testes/log_testes.ini")
log = logging.getLogger("teste")


l_modo_manual: "dict[str, l.LeituraModbusBit]" = {}

for u in range(2):
    l_modo_manual[f'CP{u+1}'] = l.LeituraModbusBit(
        client=s.Servidores.clp['AD'],
        registrador=[164 + 12764, 5] if u+1==1 else [166 + 12764, 5],
        invertido=True,
        descricao=f"[AD][CP{u+1}] Modo Manual"
    )


while True:
    for u in range(2):
        log.debug(f"{l_modo_manual[f'CP{u+1}'].descricao}: {l_modo_manual[f'CP{u+1}'].valor}")
        log.debug("")
    log.debug("")
    sleep(8)