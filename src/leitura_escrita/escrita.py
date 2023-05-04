__version__ = "0.1"
__authors__ = "Diego Basgal", "Henrique Pfeifer"
__description__ = "Este módulo corresponde a implementação de escrita em registradores."

import logging

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class EscritaModBusBit:
    
    @classmethod
    def escrever_bit(cls, client: ModbusClient, registrador: str, bit: int, valor: int) -> bool:
        try:
            raw = client.read_coils(registrador)[0]
            bin = [int(x) for x in list('{0:0b}'.format(raw))]
            for i in range(len(bin)):
                if bit == i:
                    bin[i] = valor
                    break
            v = sum(val*(2**x) for x, val in enumerate(reversed(bin)))
            res = client.write_single_coil(registrador, [v])
            return res

        except Exception:
            raise ValueError(f"[ESC] Houve um erro ao realizar a escrita bit no registrador ModBus: \"{registrador}\"")