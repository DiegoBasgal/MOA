from src.conector import ClientesUsina

from src.funcoes.leitura import *
from src.dicionarios.reg import *


class Teste:
    def __init__(self) -> None:

        self.rele = ClientesUsina.rele

        self.leitura_potencia_ug1 = LeituraModbus(
            self.rele["UG1"],
            REG_RELE["UG"]["RELE_UG1_P"],
            op=3,
            descr="[UG1] Potência Ativa"
        )
    
    @ property
    def leitura_pot(self) -> int:
        return self.leitura_potencia_ug1.valor


teste = Teste()

while True:
    try:
        print(f"Leitura de potência UG1: {teste.leitura_potencia_ug1.valor}")
    except KeyboardInterrupt:
        break