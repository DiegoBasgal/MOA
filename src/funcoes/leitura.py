__version__ = "0.2"
__author__ = "Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal"
__description__ = "Este módulo corresponde a implementação de leituras de registradores."

import logging
import traceback

from pyModbusTCP.client import ModbusClient

from dicionarios.reg import *

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
                ler = self.__client.read_input_registers(self.__registrador)[0]

            elif self.__op == 4:
                ler = self.__client.read_holding_registers(self.__registrador)[0]

            else:
                return 0 if ler is None else ler

        except Exception:
            logger.error(f"[LEI] Houve um erro ao realizar a leitura do Registrador: {self.__registrador}")
            logger.debug(f"[LEI] Traceback: {traceback.format_exc()}")
            return 0


class LeituraModbusBit(LeituraModbus):
    def __init__(self, client, registrador, bit: "int"=None, invertido: "bool"=None, descricao: "str"=None) -> "None":
        super().__init__(client, registrador, descricao)

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__bit = bit
        self.__invertido = False if invertido is not None else invertido

    @property
    def valor(self) -> "bool":
        # PROPRIEDADE -> Retorna Valor Bit ModBus.

        ler_bit = self.raw & 2**self.__bit
        return not ler_bit if self.__invertido else ler_bit


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