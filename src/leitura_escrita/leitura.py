__version__ = "0.2"
__author__ = "Lucas Lavratti", " Henrique Pfeifer"
__credits__ = ["Diego Basgal" , ...]
__description__ = "Este módulo corresponde a implementação de leituras de registradores."

from opcua import Client as OpcClient
from pyModbusTCP.client import ModbusClient

from dicionarios.reg import *

# Classes de Leitura Opc UA
class LeituraOpc:
    def __init__(self, registrador: str | None = ..., escala: int | float = ..., descricao: str | None = ...) -> ...:
        if registrador is None:
            raise ValueError("[LEI] A Leitura precisa de um valor para o argumento \"registrador\".")
        else:
            self.__registrador = registrador

            self.__client: OpcClient = None
            self.__escala = 1 if escala is None else escala
            self.__descricao = None if descricao is None else descricao

    def __str__(self) -> str:
        return f"Leitura {self.__descricao}, Valor: {self.valor}"

    @property
    def raw(self) -> int:
        try:
            valor = self.__client.get_node(self.__registrador).get_value()
            return valor if valor is not None else 0
        except ValueError("[LEI-OPC] Erro ao carregar dado \"raw\" do cliente Opc"):
            return 0

    @property
    def valor(self) -> float:
        return self.raw * self.__escala

    @property
    def client(self) -> OpcClient:
        return self.__client

    @property
    def descricao(self) -> str:
        return self.__descricao

    @client.setter
    def client(self, cln: OpcClient) -> None:
        self.__client = cln


class LeituraOpcBit(LeituraOpc):
    def __init__(self, registrador, bit: int = ..., invertido: bool = ..., descricao = ...) -> ...:
        LeituraOpc.__init__(self, registrador, descricao)
        if bit is None:
            raise ValueError("[LEI-OPC] A Leitura Opc Bit precisa de um valor para o argumento \"bit\".")
        else:
            self.__bit = bit

        self.__invertido = False if invertido is not None else invertido

    @property
    def valor(self) -> bool:
        ler_bit = self.raw & 2**self.__bit
        return not ler_bit if self.__invertido else ler_bit



# Classes de Leitura ModBus
class LeituraModbus:
    def __init__(self, client: ModbusClient, registrador: int, escala: int | float = ..., fundo_de_escala: int | float = ..., op: int = ..., descricao: str | None = ...):
        if client is None:
            raise ValueError(f"[LEI] Não foi possível carregar a conexão com o cliente (\"{type(client).__name__}\").")
        else:
            self.__client = client

        if registrador is None:
            raise ValueError("[LEI] A Leitura precisa de um valor para o argumento \"registrador\".")
        else:
            self.__registrador = registrador

            self.__escala = 1 if escala is None else escala

        if not isinstance(fundo_de_escala, int | float):
            raise TypeError("[LEI-MB] Tipagem de argumento inválida. O argumento \"fundo de escala\" deve ser \"int\" ou \"float\".")
        else:
            self.__fundo_de_escala = 0 if fundo_de_escala is None else fundo_de_escala

        if not isinstance(op, int):
            raise TypeError("[LEI-MB] Tipagem de argumento inválida. o argumento \"op\" deve ser \"int\".")
        else:
            self.__op = 3 if op is None else op

        self.__descricao = None if descricao is None else descricao

    def __str__(self) -> str:
        return f"Leitura {self.__descricao}, Valor: {self.valor}"

    @property
    def valor(self) -> int | float:
        return (self.raw * self.__escala) + self.__fundo_de_escala

    @property
    def raw(self) -> int | float:
        try:
            if self.__op == 3:
                ler = self.__client.read_holding_registers(self.__registrador)[0]
            elif self.__op == 4:
                ler = self.__client.read_input_registers(self.__registrador)[0]
            else:
                return 0 if ler is None else ler
        except ConnectionError("[LEI-MB] Erro ao conectar ao cliente ModBus.") \
            or ValueError("[LEI-MB] Erro ao carregar o dado \"raw\" do cliente ModBus."):
            return 0
    
    @property
    def descricao(self) -> str:
        return self.__descricao

class LeituraModbusBit(LeituraModbus):
    def __init__(self, client, registrador: int, bit: int = ..., invertido: bool = ..., descricao = ...):
        LeituraModbus.__init__(client, registrador, descricao)
        if bit is None:
            raise ValueError("[LEI-MB] A Leitura ModBus Bit precisa de um valor para o argumento \"bit\".")
        elif not type(bit):
            raise TypeError("[LEI-MB] Tipagem de argumento inválida. O argumento \"bit\" deve ser \"int\".")
        else:
            self.__bit = bit

        if not type(bit):
            raise TypeError("[LEI-MB] Tipagem de argumento inválida. O argumento \"invertido\" deve ser \"bool\".")
        else:
            self.__invertido = False if invertido is not None else invertido

    @property
    def valor(self) -> bool:
        ler_bit = self.raw & 2**self.__bit
        return not ler_bit if self.__invertido else ler_bit


class LeituraSoma:
    def __init__(self, leituras: list[LeituraOpc | LeituraModbus] = ..., min_zero: bool = ...):
        super().__init__()
        if leituras < 2 or leituras is None:
            raise ValueError("[LEI-SOM] A Leitura Soma precisa de \"2 ou mais\" leituras para o argumento \"leituras\".")
        elif not type(leituras):
            raise ValueError("[LEI-SOM] Tipagem de argumento inválida. O argumento \"leituras\" deve ser uma lista com \"Leituras(Base, Opc, ModBus, ...)\".")
        else:
            self.__leituras = leituras

        if not type(min_zero):
            raise TypeError("[LEI-SOM] Tipagem de argumento inválida. O argumento \"min_zero\" deve ser \"bool\".")
        else:
            self.__min_is_zero = False if min_zero is None else min_zero

    @property
    def valor(self) -> int | float:
        if self.__min_is_zero:
            return max(0, [sum(leitura.valor for leitura in self.__leituras)])
        else:
            return [sum(leitura.valor for leitura in self.__leituras)]