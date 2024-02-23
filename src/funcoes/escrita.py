__version__ = "0.1"
__authors__ = "Diego Basgal", "Henrique Pfeifer"
__description__ = "Este módulo corresponde a implementação de escrita em registradores."

import logging
import traceback

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder as BPD
from pyModbusTCP.client import ModbusClient


logger = logging.getLogger("logger")


class EscritaModBusBit:

    @classmethod
    def escrever_bit(cls, client: "ModbusClient", registrador: "list[int, int]", valor: "int") -> "bool":
        """
        Função para escrever novo valor de Bit do Registrador.

        Realiza a leitura do valor inteiro do registrador, para depois convertê-lo para
        binário e criar a lista de bits. Logo em seguida itera sobre a lista e troca o
        valor quando o bit for correspondente ao bit da lista. Depois converte a lista
        em inteiro novamente, para realizar a escrita no Registrador.
        """

        try:
            raw = client.read_holding_registers(registrador[0], 2)
            dec_1 = BPD.fromRegisters(raw, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
            dec_2 = BPD.fromRegisters(raw, byteorder=Endian.BIG, wordorder=Endian.LITTLE)

            lbit = [int(bit) for bits in [reversed(dec_1.decode_bits(1)), reversed(dec_2.decode_bits(2))] for bit in bits]

            lbit_r = [b for b in reversed(lbit)]

            for i in range(len(lbit_r)):
                if registrador[1] == i:
                    lbit_r[i] = valor
                    break

            v = sum(val*(2**x) for x, val in enumerate(lbit_r))
            res = client.write_single_register(registrador[0], v)
            return res

        except Exception:
            logger.debug(f"[ESC] Houve um erro ao realizar a Escrita no REG: {registrador}")
            logger.debug(traceback.format_exc())
            return False
