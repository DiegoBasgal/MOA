from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder as BPD
from pyModbusTCP.server import DataBank as DB

class Leitura:

    @classmethod
    def ler_bit(self, reg: "int", invertido: "bool"=False) -> "bool":

        raw = DB.get_words(reg)

        raw_dec_1 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)
        raw_dec_2 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)

        if reg[1] >= 16:
            raw_aux = DB.get_words(reg)
            raw_aux_dec_1 = BPD.fromRegisters(raw_aux, byteorder=Endian.Big, wordorder=Endian.Little)
            raw_aux_dec_2 = BPD.fromRegisters(raw_aux, byteorder=Endian.Big, wordorder=Endian.Little)
            lista_bits = [bit for bits in [raw_dec_2.decode_bits(2), raw_dec_1.decode_bits(1), raw_aux_dec_2.decode_bits(2), raw_aux_dec_1.decode_bits(1)] for bit in bits]

        else:
            lista_bits = [bit for bits in [raw_dec_2.decode_bits(2), raw_dec_1.decode_bits(1)] for bit in bits]

        for i in range(len(lista_bits)):
            if reg[1] == i:
                return not lista_bits[i] if invertido else lista_bits[i]