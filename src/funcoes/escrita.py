import logging
import traceback

from time import sleep
from pyModbusTCP.utils import *
from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class EscritaModBusBit:

    @classmethod
    def escrever_bit(cls, clp: "ModbusClient", reg: "int | list[int, int]", valor: "int", tamanho: int= 16, descr: "str"=None) -> "bool":
        try:
            lista_int = []
            raw = clp.read_holding_registers(reg[0])[0]

            if tamanho > 16:
                if reg[1] < 16:
                    raw_aux = clp.read_holding_registers(reg[0] + 1)[0]
                    conv = get_bits_from_int(raw)
                    conv_aux = get_bits_from_int(raw_aux)
                    lista_bits = conv + conv_aux

                elif reg[1] > 15:
                    raw_aux = clp.read_holding_registers(reg[0] - 1)[0]
                    conv = get_bits_from_int(raw)
                    conv_aux = get_bits_from_int(raw_aux)
                    lista_bits = conv_aux + conv
            else:
                lista_bits = get_bits_from_int(raw)

            for i in lista_bits:
                aux = 1 if i else 0
                lista_int.append(aux)

            for i in range(len(lista_int)):
                if reg[1] == i:
                    lista_int[i] = valor
                    break

            v = sum(val*(2**x) for x, val in enumerate(lista_int))
            # logger.debug("")
            # logger.debug(f"[ESCRITA TESTE] DESCRIÇÃO: \"{descr}\" | VALOR RAW: {raw}")
            # logger.debug(f"[ESCRITA TESTE] BITS (ALTERADA):                     {lista_int}")
            # logger.debug(f"[ESCRITA TESTE] CONVERSÃO (DECIMAL):                 {v}")
            res = clp.write_single_register(reg[0], v)
            # sleep(1)
            return res

        except Exception:
            logger.error(f"[ESC] Houve um erro ao realizar a escrita bit.")
            logger.debug(f"{traceback.format_exc()}")
            return False