import logging

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class EscritaModBusBit:

    @classmethod
    def escrever_bit(cls, clp: ModbusClient, reg: str, bit: int, valor: int) -> bool:
        try:
            raw = clp.read_coils(reg)[0]
            bin = [int(x) for x in list('{0:0b}'.format(raw))]

            for i in range(len(bin)):
                if bit == i:
                    bin[i] = valor
                    break

            v = sum(val*(2**x) for x, val in enumerate(reversed(bin)))
            res = clp.write_single_coil(clp, [v])
            return res

        except Exception:
            raise ValueError(f"[ESC] Houve um erro ao realizar a escrita.")