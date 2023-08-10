import logging
import traceback

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder as BPD
from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class EscritaModBusBit:

    @classmethod
    def escrever_bit(cls, clp: "ModbusClient", reg: "list[int, int]", valor: "int", descr=None) -> "bool":
        try:
            raw = clp.read_holding_registers(reg[0])
            dec_1 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)
            dec_2 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)

            if reg[1] > 15:
                bit = reg[1] - 16
                raw_aux = clp.read_holding_registers(reg[0] + 1)
                aux_dec_1 = BPD.fromRegisters(raw_aux, byteorder=Endian.Big, wordorder=Endian.Little)
                aux_dec_2 = BPD.fromRegisters(raw_aux, byteorder=Endian.Big, wordorder=Endian.Little)
                lbit = [int(bit) for bits in [reversed(aux_dec_1.decode_bits(1)), reversed(aux_dec_2.decode_bits(2))] for bit in bits]

            else:
                bit = reg[1]
                lbit = [int(bit) for bits in [reversed(dec_1.decode_bits(1)), reversed(dec_2.decode_bits(2))] for bit in bits]

            lbit_r = [b for b in reversed(lbit)]

            for i in range(len(lbit_r)):
                if bit == i:
                    lbit_r[i] = valor
                    break

            v = sum(val*(2**x) for x, val in enumerate(lbit_r))

            if reg[1] > 15:
                res = clp.write_single_register(reg[0] + 1, v)

            else:
                res = clp.write_single_register(reg[0], v)

            return res

        except Exception:
            logger.error(f"[ESC] Houve um erro ao realizar a escrita bit.")
            logger.debug(f"{traceback.format_exc()}")
            return False