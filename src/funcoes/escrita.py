import logging
import traceback

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class EscritaModBusBit:

    @classmethod
    def escrever_bit(cls, clp: "ModbusClient", reg: "int | list[int, int]", valor: "int", descr: "str"=None) -> "bool":
        try:
            print("")
            print(f"[LER] MODO DEBUG:")
            print("")

            raw = clp.read_holding_registers(reg[0])[0]

            print("")
            print(f"[LER] Registrador:                           {descr} (Endrereço {reg[0]} | Bit {reg[1]})")
            print(f"[LER] Dado RAW:                              {raw}")

            conv_bin = [int(x) for x in list('{0:0b}'.format(raw))]

            print(f"[LER] Dado convertido RAW -> BIN:            {[int(x) for x in list('{0:0b}'.format(raw))]}")

            for i in range(len(conv_bin)):
                if reg[1] == i:
                    conv_bin[i] = valor
                    break

            v = sum(val*(2**x) for x, val in enumerate(reversed(conv_bin)))

            print("")
            print(f"[LER] Escrevendo dado convertido BIN -> INT: {v}")

            res = clp.write_single_register(reg[0], v)
            print(f"[LER] Retorno da tentativa de escrita: {res}")
            print("")
            print("")
            return res

        except Exception:
            logger.error(f"[ESC] Houve um erro ao realizar a escrita.")
            logger.debug(f"[ESC] Traceback: {traceback.format_exc}")
            return False