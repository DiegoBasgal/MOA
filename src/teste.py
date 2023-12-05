from pyModbusTCP.client import ModbusClient

from src.funcoes.leitura import *
from src.dicionarios.const import *

clp_tda = ModbusClient(
    host="192.168.20.140",
    port=503,
    unit_id=1,
    timeout=0.5
)

clp_tda.open()

l_nv_beL_weL = LeituraModbusFloat(
    clp_tda,
    30,
    byteorder=END_LITTLE,
    wordorder=END_LITTLE,
    descricao="Leitura Nível | B.e.L | W.e.L"
)
l_nv_beB_weL = LeituraModbusFloat(
    clp_tda,
    30,
    byteorder=END_BIG,
    wordorder=END_LITTLE,
    descricao="Leitura Nível | B.e.B | W.e.L"
)
l_nv_beL_weB = LeituraModbusFloat(
    clp_tda,
    30,
    byteorder=END_LITTLE,
    wordorder=END_BIG,
    descricao="Leitura Nível | B.e.L | W.e.B"
)
l_nv_beL_weB = LeituraModbusFloat(
    clp_tda,
    30,
    byteorder=END_BIG,
    wordorder=END_BIG,
    descricao="Leitura Nível | B.e.B | W.e.B"
)


print(f"{l_nv_beL_weL.descricao} = {l_nv_beL_weL.valor}")
print(f"{l_nv_beB_weL.descricao} = {l_nv_beB_weL.valor}")
print(f"{l_nv_beL_weB.descricao} = {l_nv_beL_weB.valor}")
print(f"{l_nv_beL_weB.descricao} = {l_nv_beL_weB.valor}")