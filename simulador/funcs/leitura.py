import traceback

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder as BPD
from pyModbusTCP.server import DataBank as DB

class Leitura:

    @classmethod
    def ler_bit(self, reg: "list[int, int]", invertido: "bool"=False) -> "int":

        try:
            raw = DB.get_words(reg[0])
            dec_1 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)
            dec_2 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)

            lbit = [int(bit) for bits in [reversed(dec_1.decode_bits(1)), reversed(dec_2.decode_bits(2))] for bit in bits]

            lbit_r = [b for b in reversed(lbit)]

            for i in range(len(lbit_r)):
                if reg[1] == i:
                    return not int(lbit_r[i]) if invertido else int(lbit_r[i])

        except Exception:
            print(f"[LEI] Erro ao realizar a Leitura do Bit: {reg[1]} | REG: {reg}")
            print(traceback.format_exc())
            return None