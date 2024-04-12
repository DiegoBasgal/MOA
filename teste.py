import src.funcoes.leitura as l
import src.conectores.servidores as s

from time import sleep
from src.dicionarios.reg_elipse import *


# pot_medidor = l.LeituraModbus(clp, REG_RELE["SE"]["P"], descricao="[SE][RELE] Potência no Medidor da Usina")

while True:
    print(f"{65535 - s.Servidores.rele['SE'].read_holding_registers(REG_RELE['SE']['P'], 2)[1]}")
    sleep(2)