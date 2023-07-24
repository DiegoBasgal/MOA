__version__ = "0.1"
__authors__ = "Diego Basgal", "Henrique Pfeifer"
__description__ = "Este módulo corresponde a implementação de escrita em registradores."

import logging
import traceback

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("logger")

class EscritaModBusBit:

    @classmethod
    def escrever_bit(cls, client: "ModbusClient", registrador: "str", bit: "int", valor: "int") -> "bool":
        """
        Função para escrever novo valor de Bit do Registrador.

        Realiza a leitura do valor inteiro do registrador, para depois convertê-lo para
        binário e criar a lista de bits. Logo em seguida itera sobre a lista e troca o
        valor quando o bit for correspondente ao bit da lista. Depois converte a lista
        em inteiro novamente, para realizar a escrita no Registrador.
        """

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
            logger.error(f"[ESC] Houve um erro ao realizar a Leitura do REG: {registrador}, Bit: {bit} do Servidor: {client}")
            logger.debug(f"[ESC] Traceback: {traceback.format_exc()}")
            return False