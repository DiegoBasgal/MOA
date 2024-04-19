import src.funcoes.leitura as l
import src.dicionarios.dict as d
import src.conectores.servidores as s

from time import sleep
from pyModbusTCP.client import ModbusClient

from src.dicionarios.reg_elipse import *

clp = ModbusClient(
    host=d.ips["SA_ip"],
    port=503,
    unit_id=1,
    timeout=0.5
)

clp.open()

l_teste = l.LeituraModbusBit(clp, REG_CLP["SA_SE"]["DISJUTOR_52L_FECHADO"], invertido=True, descricao="DISJUTOR_52L_FECHADO")
# l_teste = l.LeituraModbusBit(clp, REG_CLP["SA_SE"]["COM_TENSAO_LINHA_EXTERNA"], descricao="COM_TENSAO_LINHA_EXTERNA")

while True:
    print(f"{l_teste.descricao} -> {l_teste.valor}")
    sleep(2)
