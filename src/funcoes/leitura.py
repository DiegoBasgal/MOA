__version__ = "0.2"
__author__ = "Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal"
__description__ = "Este módulo corresponde a implementação de leituras de registradores."

import logging
import traceback

from time import sleep
from pyModbusTCP.client import ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder as BPD

from src.dicionarios.reg import *


logger = logging.getLogger("logger")


class LeituraModbus:
    def __init__(self, client: "ModbusClient"=None, registrador: "int"=None, escala: "float"=1, fundo_escala: "float"=0, op: "int"=3, descricao: "str"=None) -> "None":

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__client = client
        self.__registrador = registrador

        self.__op = op
        self.__escala = escala
        self.__fundo_escala = fundo_escala
        self.__descricao = descricao


    def __str__(self) -> "str":
        """
        Função que retorna string com detalhes da leitura para logger.
        """

        return f"Leitura {self.__descricao}, Valor: {self.valor}"

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
                if ler is None:
                    ler2 = self.__client.read_holding_registers(self.__registrador)[0]
                    return ler2
                else:
                    return ler

            elif self.__op == 4:
                ler = self.__client.read_input_registers(self.__registrador)[0]
                return ler

        except Exception:
            logger.error(f"[LEI] Houve um erro na leitura RAW -> INT do REG: {self.__descricao} | Endereço: {self.__registrador}")
            logger.debug(traceback.format_exc())
            return 0

    @property
    def valor(self) -> "int":
        # PROPRIEDADE -> Retorna Valor calculado com escala e fundo de escala.

        return (self.raw * self.__escala) + self.__fundo_escala


class LeituraModbusBit(LeituraModbus):
    def __init__(self, client: "ModbusClient", registrador: "list[int, int]", invertido: "bool"=False, descricao: "str"=None) -> "None":
        super().__init__(client, registrador, descricao)

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS
        self.__client = client
        self.__reg = registrador[0]
        self.__bit = registrador[1]
        self.__invertido = invertido
        self.__descricao = descricao

    @property
    def registrador(self) -> "int":
    # PROPRIEDADE -> Retorna o registrador

        return self.__registrador

    @property
    def descricao(self) -> "str":
        # PROPRIEDADE -> Retrona a Descrição da Leitura.

        return self.__descricao

    @property
    def raw(self) -> "list":
        # PROPRIEDADE -> Retorna Valor raw baseado no tipo de operação ModBus.

        try:
            if self.__client.open():
                ler = self.__client.read_holding_registers(int(self.__reg), 2)
                self.__client.close()
                return ler

        except Exception:
            logger.error(f"[LEI] Erro na Leitura RAW -> BIT do REG: {self.__reg} | Bit: {self.__bit}")
            logger.debug(traceback.format_exc())
            sleep(1)

    @property
    def valor(self) -> "bool":
        # PROPRIEDADE -> Retorna Valor Bit em booleano ModBus.

        try:
            leitura = self.raw

            dec_1 = BPD.fromRegisters(leitura, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
            dec_2 = BPD.fromRegisters(leitura, byteorder=Endian.BIG, wordorder=Endian.LITTLE)

            lbit = [int(bit) for bits in [reversed(dec_1.decode_bits(1)), reversed(dec_2.decode_bits(2))] for bit in bits]

            lbit_r = [b for b in reversed(lbit)]

            for i in range(len(lbit_r)):
                if self.__bit == i:
                    return not lbit_r[i] if self.__invertido else lbit_r[i]

        except Exception:
            logger.debug(f"[LEI] Erro na Leitura BIT do REG: {self.__descricao} | Endereço: {self.__reg} | Bit: {self.__bit}")
            logger.debug(traceback.format_exc())
            sleep(1)
            return None


class LeituraModbusFloat(LeituraModbus):
    def __init__(self, client: "ModbusClient"=None, registrador: "int"=None, escala: "float"=1, descricao: "str"=None):
        super().__init__(client, registrador, descricao)

        # ATRIBUIÇÃO DE VAIRÁVEIS PRIVADAS

        self.__client = client
        self.__reg = registrador
        self.__escala = escala

    @property
    def valor(self) -> "float":
        # PROPRIEDADE -> Retorna o valor tradado de leitura em Float.

        try:
            raw = self.__client.read_holding_registers(self.__reg + 1, 2)

            dec = BPD.fromRegisters(raw, byteorder=Endian.BIG, wordorder=Endian.LITTLE)

            val = dec.decode_32bit_float() * self.__escala

            return val

        except Exception:
            logger.debug(f"[LEI] Erro na Leitura FLOAT do REG: {self.descricao} | Endereço: {self.__reg}")
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