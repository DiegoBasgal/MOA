import logging
import traceback

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder as BPD
from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class EscritaModBusBit:

    @classmethod
    def escrever_bit(cls, clp: "ModbusClient", reg: "list[int, int]", valor: "int") -> "bool":
        try:
            raw = clp.read_holding_registers(reg[0])
            raw_dec_1 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)
            raw_dec_2 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)

            if reg[1] >= 16:
                raw_aux = clp.read_holding_registers(reg[0] + 1)
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

            res = clp.write_single_register(reg[0], v)
            return res

        except Exception:
            logger.error(f"[ESC] Houve um erro ao realizar a escrita bit.")
            logger.debug(f"{traceback.format_exc()}")
            return False