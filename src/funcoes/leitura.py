__version__ = "0.2"
__author__ = "Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal"
__description__ = "Este módulo corresponde a implementação de leituras de registradores."

import logging
import traceback

from time import sleep
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder as BPD
from pyModbusTCP.client import ModbusClient

from src.dicionarios.reg import *

logger = logging.getLogger("logger")

class LeituraModbus:
    def __init__(self, client: "ModbusClient", registrador: "int", escala: "float"=None, fundo_escala: "float"=None, op: "int"=None, descricao: "str"= None) -> "None":

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__client = client
        self.__registrador = registrador

        self.__op = 3 if op is None else op
        self.__escala = 1 if escala is None else escala
        self.__fundo_escala = 0 if fundo_escala is None else fundo_escala
        self.__descricao = None if descricao is None else descricao

    def __str__(self) -> "str":
        """
        Função que retorna string com detalhes da leitura para logger.
        """

        return f"Leitura {self.__descricao}, Valor: {self.valor}"

    @property
    def valor(self) -> "int":
        # PROPRIEDADE -> Retorna Valor calculado com escala e fundo de escala.

        return (self.raw * self.__escala) + self.__fundo_escala

    @property
    def descricao(self) -> "str":
        # PROPRIEDADE -> Retrona a Descrição da Leitura.

        return self.__descricao

    @property
    def raw(self) -> "int":
        # PROPRIEDADE -> Retorna Valor raw baseado no tipo de operação ModBus.

        try:
            if self.__op == 3:
                ler = self.__client.read_holding_registers(self.__registrador)[0]

            elif self.__op == 4:
                ler = self.__client.read_input_registers(self.__registrador)[0]

            else:
                return 0 if ler is None else ler

        except Exception:
            logger.error(f"[LEI] Houve um erro ao realizar a leitura do Registrador: {self.__registrador}")
            logger.debug(f"[LEI] Traceback: {traceback.format_exc()}")
            return 0


class LeituraModbusBit(LeituraModbus):
    def __init__(self, client: "ModbusClient", registrador: "list[int, int]", invertido: "bool"=None, descricao: "str"=None) -> "None":
        super().__init__(client, registrador, descricao)

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS
        self.__client = client
        self.__reg = registrador[0]
        self.__bit = registrador[1]
        self.__invertido = False if invertido is not None else invertido

    @property
    def valor(self) -> "bool":
        # PROPRIEDADE -> Retorna Valor Bit em booleano ModBus.

        try:
            raw = self.__client.read_holding_registers(self.__reg, 2)
            print('')
            print('')
            print(f'RAW: {raw}')
            print('')
            print('')
            dec_1 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)
            dec_2 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)

            lbit = [int(bit) for bits in [reversed(dec_1.decode_bits(1)), reversed(dec_2.decode_bits(2))] for bit in bits]

            lbit_r = [b for b in reversed(lbit)]

            for i in range(len(lbit_r)):
                if self.__bit == i:
                    return not lbit_r[i] if self.__invertido else lbit_r[i]

        except Exception:
            logger.error(f"[LEI] Houve um erro ao realizar a Leitura de valores Bit do registrador: {self.__reg}.")
            logger.debug(traceback.format_exc())
            sleep(1)
            return None


class LeituraModbusFloat(LeituraModbus):
    def __init__(self, client: "ModbusClient"=None, registrador: "int"=None, op: "int"=3, descricao: "str"=None):
        super().__init__(client, registrador, op, descricao)

        # ATRIBUIÇÃO DE VAIRÁVEIS PRIVADAS

        self.__reg = registrador[0] if isinstance(registrador, list) else registrador

    @property
    def valor(self) -> "float":
        # PROPRIEDADE -> Retorna o valor tradado de leitura em Float.

        try:
            raw = self.__client.read_holding_registers(self.__reg, 2)
            dec = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)

            return dec.decode_32bit_float()

        except Exception:
            logger.error(f"[LEI] Houve um erro ao realizar a Leitura de valores Float do registrador: {self.__reg}.")
            logger.debug(traceback.format_exc())
            sleep(1)
            return 0

class LeituraSoma:
    def __init__(self, leituras: "list[LeituraModbus]"=None, min_zero: "bool"=None) -> "None":

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__leituras = leituras
        self.__min_is_zero = False if min_zero is None else min_zero

    @property
    def valor(self) -> "int":
        # PROPRIEDADE -> Retorna Valor de soma de duas leituras ModBus.

        if self.__min_is_zero:
            return max(0, [sum(leitura.valor for leitura in self.__leituras)])

        else:
            return [sum(leitura.valor for leitura in self.__leituras)]