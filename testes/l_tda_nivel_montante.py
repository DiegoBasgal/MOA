import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from logging.config import fileConfig

from src.dicionarios.reg import *


fileConfig("/opt/operacao-autonoma/testes/log_testes.ini")
log = logging.getLogger("teste")


l_nivel_montante = l.LeituraModbus(
    client=s.Servidores.clp['SA'],
    registrador=12766,
    escala=0.01,
    fundo_escala=800,
    descricao=f"[TDA] Nível Montante"
)


while True:
    log.debug(f"{l_nivel_montante.descricao}: {l_nivel_montante.valor}")
    log.debug("")
    sleep(8)