"""
Leituras.

Esse módulo corresponde a implementação das leituras, dos valores de campo.
"""
__version__ = "0.1"
__author__ = "Lucas Lavratti"

import logging
from pyModbusTCP.client import ModbusClient
from modbus_mapa_antigo import *


class LeituraBase:
    ...


class LeituraModbus(LeituraBase):
    ...


class LeituraModbusBit(LeituraBase):
    ...


class LeituraBase:
    """
    Classe implementa a base para leituras. É "Abstrata" assim por se dizer...
    """

    def __init__(self, descr: str) -> None:
        self.__descr = descr
        self.__valor = None
        self.logger = logging.getLogger("__main__")

    def __str__(self):
        return "Leitura {}, Valor: {}, Raw: {}".format(
            self.__descr, self.valor, self.raw
        )

    @property
    def valor(self):
        raise NotImplementedError("Deve ser implementado na classe herdeira.")

    @property
    def raw(self):
        raise NotImplementedError("Deve ser implementado na classe herdeira.")

    @property
    def descr(self) -> str:
        """
        Descrição do limite em questão.

        Returns:
            str: descr
        """
        return self.__descr


class LeituraModbus(LeituraBase):
    """
    Classe implementa a base para leituras da unidade da geração utilizando modbus.
    """

    def __init__(
        self,
        descr: str,
        modbus_client: ModbusClient,
        registrador: int,
        escala: float = 1,
        fundo_de_escala: float = 0,
    ):
        super().__init__(descr)
        self.__descr = descr
        self.__modbus_client = modbus_client
        self.__registrador = registrador
        self.__escala = escala
        self.__fundo_de_escala = fundo_de_escala

    @property
    def valor(self) -> float:
        """
        Valor

        Returns:
            float: valor já tratado
        """
        return (self.raw * self.__escala) - self.__fundo_de_escala

    @property
    def raw(self) -> int:
        """
        Raw Dado Crú
        Retorna o valor como lido da CLP, o inteiro unsigned contido no registrador

        Raises:
            ConnectionError: Erro caso a conexão falhe
            NotImplementedError: [description]

        Returns:
            int: [description]
        """
        try:
            if self.__modbus_client.open():
                aux = self.__modbus_client.read_holding_registers(self.__registrador)[0]
                if aux is not None:
                    return aux
                else:
                    return 0
            else:
                raise ConnectionError("Erro na conexãp modbus.")
        except:
            # ! TODO Tratar exceptions
            # O que deve retornar caso não consiga comunicar?
            raise NotImplementedError


class LeituraModbusBit(LeituraModbus):
    """
    Classe implementa a leituras de bits de registradores da unidade da geração utilizando modbus.
    """

    def __init__(
        self,
        descr: str,
        modbus_client: ModbusClient,
        registrador: int,
        bit: int,
        invertido: bool = False,
    ):
        super().__init__(descr, modbus_client, registrador)
        self.__bit = bit
        self.__invertido = invertido

    @property
    def valor(self) -> bool:
        """
        Valor

        Returns:
            bool: valor já tratado
        """
        aux = self.raw & 2**self.__bit
        if self.__invertido:
            aux = not aux
        return aux


class LeituraDelta(LeituraBase):
    def __init__(self, descr: str, leitura_A: LeituraBase, leitura_B: LeituraBase):
        super().__init__(descr)
        self.__leitura_A = leitura_A
        self.__leitura_B = leitura_B

    @property
    def valor(self) -> float:
        """
        Valor

        Returns:
            float: leitura_A - leitura_B
        """
        return self.__leitura_A.valor - self.__leitura_B.valor
