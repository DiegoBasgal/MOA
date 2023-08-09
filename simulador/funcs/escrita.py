import traceback

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder as BPD
from pyModbusTCP.server import DataBank as DB

class Escrita:

    @classmethod
    def escrever_bit(cls, reg: "list[int, int]", valor: "int") -> "None":

        try:
            raw = DB.get_words(reg[0])
            dec_1 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)
            dec_2 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)

            lbit = [int(bit) for bits in [reversed(dec_1.decode_bits(1)), reversed(dec_2.decode_bits(2))] for bit in bits]

            lbit_r = [b for b in reversed(lbit)]

            for i in range(len(lbit_r)):
                if reg[1] == i:
                    lbit_r[i] = valor
                    break

            v = sum(val*(2**x) for x, val in enumerate(lbit_r))

            DB.set_words(reg[0], [v])

        except Exception:
            print(f"[ESC] Erro ao realizar a Escrita do Bit: {reg[1]} | REG: {reg}")
            print(traceback.format_exc())