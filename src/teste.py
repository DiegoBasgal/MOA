from dicionarios.reg import *
from funcoes.leitura import LeituraModbusBit

from pyModbusTCP.client import ModbusClient

clp = ModbusClient("192.168.10.109", 502, 1, 0.5, None, True, True)

res = LeituraModbusBit(clp, REG_GERAL["GERAL_CD_RESET_GERAL"], False, "Comando Reset Geral")

print(res.valor)