"""
Leituras.

Versão 0.1 -> Utiliza o protocolo ModBusTCP
Versão 0.2 -> Utiliza o protocolo OPC

Esse módulo corresponde a implementação das leituras, dos valores de campo.
"""
__version__ = "0.2"
__authors__ = "Lucas Lavratti", "Diego Basgal"

import logging
from opcua import Client
from pyModbusTCP.client import ModbusClient

from dicionarios.reg import *

class LeituraBase:
    """
    Classe implementa a base para leituras. É "Abstrata" assim por se dizer...
    """

    def __init__(self, descr: str) -> None:
        self.__valor = None
        self.logger = logging.getLogger("__main__")

    @property
    def valor(self):
        raise NotImplementedError("Deve ser implementado na classe herdeira.")

    @property
    def raw(self):
        raise NotImplementedError("Deve ser implementado na classe herdeira.")

class LeituraOPC(LeituraBase):
    def __init__(self, opc_client: Client, registrador: str, escala: float = 1):
        super().__init__()
        self.__opc_client = opc_client
        self.__registrador = registrador
        self.__escala = escala
   
    @property
    def raw(self) -> int:
        try:
            self.__opc_client.connect()
            aux = self.__opc_client.get_node(self.__registrador)
            valor = aux.get_value()
            if valor is not None:
                return valor
            else:
                return 0
        except:
            return 0
   
    @property
    def valor(self) -> float:
        return self.raw * self.__escala

class LeituraOPCBit(LeituraOPC):
    def __init__(self, opc_client: Client, registrador: str, bit: int, invertido: bool=False):
        super().__init__(opc_client, registrador)
        self.__bit = bit
        self.__invertido = invertido

    @property
    def valor(self) -> bool:
        aux = self.raw & 2**self.__bit
        if self.__invertido:
            aux = not aux
        return aux

class LeituraModbus(LeituraBase):
    """
    Classe implementa a base para leituras da unidade da geração utilizando modbus.
    """

    def __init__(
        self,
        modbus_client: ModbusClient,
        registrador: int,
        escala: float = 1,
        fundo_de_escala: float = 0,
        op: int = 3,
    ):
        super().__init__()
        self.__modbus_client = modbus_client
        self.__registrador = registrador
        self.__escala = escala
        self.__fundo_de_escala = fundo_de_escala
        self.__op = op

    @property
    def valor(self) -> float:
        """
        Valor

        Returns:
            float: valor já tratado
        """
        return (self.raw * self.__escala) + self.__fundo_de_escala

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
                if self.__op == 3:
                    aux = self.__modbus_client.read_holding_registers(
                        self.__registrador
                    )[0]
                elif self.__op == 4:
                    aux = self.__modbus_client.read_input_registers(self.__registrador)[
                        0
                    ]
                if aux is not None:
                    return aux
                else:
                    return 0
            else:
                raise ConnectionError("Erro na conexão modbus.")
        except:
            # ! TODO Tratar exceptions
            # O que deve retornar caso não consiga comunicar?
            # raise NotImplementedError
            return 0
            pass

class LeituraModbusBit(LeituraModbus):
    """
    Classe implementa a leituras de bits de registradores da unidade da geração utilizando modbus.
    """

    def __init__(
        self,
        modbus_client: ModbusClient,
        registrador: int,
        bit: int,
        invertido: bool = False,
    ):
        super().__init__(modbus_client, registrador)
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

class LeituraSoma(LeituraBase):
    def __init__(
        self,
        leitura_A: LeituraBase,
        leitura_B: LeituraBase,
        min_is_zero=True,
    ):
        super().__init__()
        self.__leitura_A = leitura_A
        self.__leitura_B = leitura_B
        self.__min_is_zero = min_is_zero

    @property
    def valor(self) -> float:
        """
        Valor

        Returns:
            float: leitura_A + leitura_B
        """
        if self.__min_is_zero:
            return max(0, self.__leitura_A.valor + self.__leitura_B.valor)
        else:
            return self.__leitura_A.valor + self.__leitura_B.valor


class LeiturasUSN:
    def __init__(self):
        self.client = Client("opc.tcp://EOP:4845")

        self.nv_montante = LeituraOPC(self.client, REG_OPC["NIVEL_MONTANTE"])
        
        self.tensao_rs = LeituraOPC(self.client, REG_OPC["LT_VAB"])

        self.tensao_st = LeituraOPC(self.client, REG_OPC["LT_VBC"])

        self.tensao_tr = LeituraOPC(self.client, REG_OPC["LT_VCA"])
        
        self.potencia_ativa_kW = LeituraOPC(
            "Potências de MP e MR",
            self.client,
            "ns=7;s=CLP_SA."
        )