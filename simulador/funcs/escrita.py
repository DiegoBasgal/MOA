from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder as BPD
from pyModbusTCP.server import DataBank as DB

class Escrita:

    @classmethod
    def escrever_bit(cls, reg: "int", valor: "int") -> "None":

        raw = DB.get_words(reg[0])
        raw_dec_1 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)
        raw_dec_2 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)

        if reg[1] >= 16:
            raw_aux = DB.get_words(reg[0])
            raw_aux_dec_1 = BPD.fromRegisters(raw_aux, byteorder=Endian.Big, wordorder=Endian.Little)
            raw_aux_dec_2 = BPD.fromRegisters(raw_aux, byteorder=Endian.Big, wordorder=Endian.Little)
            lista_int = [int(bit) for bits in [raw_dec_2.decode_bits(2), raw_dec_1.decode_bits(1), raw_aux_dec_2.decode_bits(2), raw_aux_dec_1.decode_bits(1)] for bit in bits]

        else:
            lista_int = [int(bit) for bits in [raw_dec_2.decode_bits(2), raw_dec_1.decode_bits(1)] for bit in bits]

        for i in range(len(lista_int)):
            if reg[1] == i:
                lista_int[i] = valor
                break

        v = sum(val*(2**x) for x, val in enumerate(lista_int))

        DB.set_words(reg[0], [v])