import logging
import traceback

from pyModbusTCP.utils import *
from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class EscritaModBusBit:

    @classmethod
    def escrever_bit(cls, clp: "ModbusClient", reg: "int | list[int, int]", valor: "int", tamanho: int= 16, descr: "str"=None) -> "bool":
        try:
            raw = clp.read_holding_registers(reg[0])[0]
            # logger.debug("")
            # logger.debug(f"[ESCRITA TESTE] DESCRIÇÃO: \"{descr}\" | REGISTRADOR: {reg} | VALOR RAW: {raw}")

            if tamanho > 16:
                # logger.debug(f"[ESCRITA TESTE] LISTA > \"16 BITS\"")
                if reg[1] < 16:
                    raw_aux = clp.read_holding_registers(reg[0] + 1)[0]
                    conv = get_bits_from_int(raw)
                    conv_aux = get_bits_from_int(raw_aux)
                    lista_bits = conv + conv_aux
                    # logger.debug(f"[ESCRITA TESTE] LISTA DE BITS CONVERTIDA DE DECIMAL: {lista_bits}")

                elif reg[1] > 15:
                    raw_aux = clp.read_holding_registers(reg[0] - 1)[0]
                    conv = get_bits_from_int(raw)
                    conv_aux = get_bits_from_int(raw_aux)
                    lista_bits = conv_aux + conv
                    # logger.debug(f"[ESCRITA TESTE] LISTA DE BITS CONVERTIDA DE DECIMAL: {lista_bits}")
            else:
                # logger.debug(f"[ESCRITA TESTE] LISTA < \"16 BITS\"")
                lista_bits = get_bits_from_int(raw)

            lista_int = []
            for i in lista_bits:
                aux = 1 if i else 0
                lista_int.append(aux)
            # logger.debug(f"[ESCRITA TESTE] LISTA DE BITS CONVERTIDA DE BOOL PARA INT: {lista_int}")

            for i in range(len(lista_int)):
                if reg[1] == i:
                    #logger.debug(f"[ESCRITA TESTE] BIT: {i}")
                    #logger.debug(f"[ESCRITA TESTE] VALOR ANTIGO: {lista_int[i]}")
                    #logger.debug(f"[ESCRITA TESTE] VALOR NOVO: {valor}")
                    lista_int[i] = valor
                    # logger.debug(f"[ESCRITA TESTE] LISTA INT ALTERADA: {lista_int}")
                    break

            v = sum(val*(2**x) for x, val in enumerate(lista_int))
            # logger.debug(f"[ESCRITA TESTE] CONVERSÃO DE BITS PARA DECIMAL: {v}")
            # logger.debug("")
            res = clp.write_single_register(reg[0], v)
            return res

        except Exception:
            logger.error(f"[ESC] Houve um erro ao realizar a escrita.")
            logger.debug(f"[ESC] Traceback: {traceback.format_exc()}")
            return False