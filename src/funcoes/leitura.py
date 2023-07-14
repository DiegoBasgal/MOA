__version__ = "0.2"
__author__ = "Lucas Lavratti", " Henrique Pfeifer"
__credits__ = ["Diego Basgal" , ...]
__description__ = "Este módulo corresponde a implementação de leituras de registradores."

from pyModbusTCP.client import ModbusClient

from dicionarios.reg import *

class LeituraModbus:
    def __init__(self, client: ModbusClient, registrador: int, escala: int | float = ..., fundo_escala: int | float = 0, op: int = ..., descricao: str | None = ...):
        if client is None:
            raise ValueError(f"[LEI] Não foi possível carregar a conexão com o cliente (\"{type(client).__name__}\").")
        else:
            self.__client = client

        if registrador is None:
            raise ValueError("[LEI] A Leitura precisa de um valor para o argumento \"registrador\".")
        else:
            self.__registrador = registrador

        self.__op = 3 if op is None else op
        self.__escala = 1 if escala is None else escala
        self.__fundo_escala = 0 if fundo_escala is None else fundo_escala
        self.__descricao = None if descricao is None else descricao

    def __str__(self) -> str:
        return f"Leitura {self.__descricao}, Valor: {self.valor}"

    @property
    def valor(self) -> int:
        return (self.raw * self.__escala) + self.__fundo_escala

    @property
    def raw(self) -> int:
        try:
            if self.__op == 3:
                ler = self.__client.read_input_registers(self.__registrador)[0]
            elif self.__op == 4:
                ler = self.__client.read_holding_registers(self.__registrador)[0]
            else:
                return 0 if ler is None else ler

        except Exception:
            raise ValueError(f"[LEI] Houve um erro ao realizar a leitura do registrador ModBus: {self.__registrador}")

    @property
    def descricao(self) -> str:
        return self.__descricao

class LeituraModbusBit(LeituraModbus):
    def __init__(self, client, registrador, bit: int = ..., invertido: bool = ..., descricao = ...):
        LeituraModbus.__init__(client, registrador, descricao)
        if bit is None:
            raise ValueError("[LEI-MB] A Leitura ModBus Bit precisa de um valor para o argumento \"bit\".")
        else:
            self.__bit = bit

        self.__invertido = False if invertido is not None else invertido

    @property
    def valor(self) -> bool:
        ler_bit = self.raw & 2**self.__bit
        return not ler_bit if self.__invertido else ler_bit


class LeituraSoma:
    def __init__(self, leituras: list[LeituraModbus] = ..., min_zero: bool = ...):
        super().__init__()
        if leituras < 2 or leituras is None:
            raise ValueError("[LEI-SOM] A Leitura Soma precisa de \"2 ou mais\" leituras para o argumento \"leituras\".")
        else:
            self.__leituras = leituras

        self.__min_is_zero = False if min_zero is None else min_zero

    @property
    def valor(self) -> int:
        if self.__min_is_zero:
            return max(0, [sum(leitura.valor for leitura in self.__leituras)])
        else:
            return [sum(leitura.valor for leitura in self.__leituras)]