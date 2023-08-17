from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

from src.dicionarios.reg import *
from src.funcoes.leitura import LeituraModbus, LeituraModbusFloat

from src.conectores.servidores import Servidores

class Teste:
    def __init__(self) -> None:

        self.clp = Servidores.clp
        self.rele = Servidores.rele

        self.leitura_potencia_ug1 = LeituraModbus(
            self.rele["UG1"],
            REG_RELE["UG"]["RELE_UG1_P"],
            op=3,
            descr="[UG1] Potência Ativa"
        )

        self.leitura_nv_montante = LeituraModbusFloat(
            self.clp["TDA"],
            REG_GERAL["GERAL_EA_NIVEL_MONTANTE_GRADE"]
        )

    @property
    def leitura_nv_montante(self) -> float:
        return self.leitura_nv_montante.valor

    @ property
    def leitura_pot(self) -> int:
        return self.leitura_potencia_ug1.valor


teste = Teste()

while True:
    try:
        print(f"Leitura de potência UG1: {teste.leitura_potencia_ug1.valor}")
    except KeyboardInterrupt:
        break