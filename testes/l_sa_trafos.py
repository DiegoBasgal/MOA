import logging

import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from logging.config import fileConfig


fileConfig("/opt/operacao-autonoma/testes/log_testes.ini")
log = logging.getLogger("teste")


l_trip_tsa1 = l.LeituraModbusBit(
    client=s.Servidores.clp["SA"],
    registrador=[14203, 2],
    descricao="[SA]  Trafo Serviço Auxiliar 01 - Trip Sobretemperatura do Enrolamento"
)

l_trip_tsa2 = l.LeituraModbusBit(
    client=s.Servidores.clp["SA"],
    registrador=[14203, 6], 
    descricao="[SA]  Trafo Serviço Auxiliar 02 - Trip Sobretemperatura do Enrolamento"
)


while True:
    log.debug(f"{l_trip_tsa1.descricao}: {l_trip_tsa1.valor}")
    log.debug(f"{l_trip_tsa2.descricao}: {l_trip_tsa2.valor}")
    log.debug("")
    sleep(8)