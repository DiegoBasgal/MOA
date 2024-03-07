import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from logging.config import fileConfig

from src.dicionarios.reg import *


fileConfig("/opt/operacao-autonoma/testes/log_testes.ini")
log = logging.getLogger("teste")


l_etapa_alvo: "dict[str, l.LeituraModbus]" = {}
l_etapa_atual: "dict[str, l.LeituraModbus]" = {}

for u in range(4):
    l_etapa_alvo[f'UG{u+1}'] = l.LeituraModbus(
        client=s.Servidores.clp[f'UG{u+1}'],
        registrador=12773,
        descricao=f"[UG{u+1}] Etapa Alvo"
    )
    l_etapa_atual[f'UG{u+1}'] = l.LeituraModbus(
        client=s.Servidores.clp[f'UG{u+1}'],
        registrador=12774,
        descricao=f"[UG{u+1}] Etapa Atual"
    )


while True:
    for u in range(4):
        log.debug(f"{l_etapa_atual[f'UG{u+1}'].descricao}: {l_etapa_atual[f'UG{u+1}'].valor}")
        log.debug(f"{l_etapa_alvo[f'UG{u+1}'].descricao}:  {l_etapa_alvo[f'UG{u+1}'].valor}")
        log.debug("")
    log.debug("")
    sleep(8)