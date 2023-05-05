"""
Leituras.

Esse módulo corresponde a implementação das leituras, dos valores de campo.
"""
__version__ = "0.1"
__author__ = "Lucas Lavratti"

import socket
import struct
import logging
from dicionarios.regs import *
from pyModbusTCP.utils import crc16
from pyModbusTCP.client import ModbusClient

def bcd_to_i(i):
    value = i & 0xF
    value += ((i >> 4) & 0xF) * 10
    value += ((i >> 8) & 0xF) * 100
    value += ((i >> 12) & 0xF) * 1000
    return value

def add_crc(data):
    crc = hex(crc16(data))
    crc = bytes.fromhex(crc[4] + crc[5] + crc[2] + crc[3])
    return data + crc

class LeituraBase:
    ...

class LeituraModbus(LeituraBase):
    ...

class LeituraModbusBit(LeituraBase):
    ...

class LeituraDelta(LeituraBase):
    ...

class LeituraDebug(LeituraBase):
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
        return f"Leitura {self.__descr}, Valor: {self.valor}, Raw: {self.raw}"

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
        op: int = 3,
    ):
        super().__init__(descr)
        self.__descr = descr
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

class LeituraModbusCoil(LeituraBase):
    """
    Classe implementa a base para leituras da unidade da geração utilizando modbus.
    """

    def __init__(
        self,
        descr: str,
        modbus_client: ModbusClient,
        registrador: int,
        invertido: bool = False,
    ):
        super().__init__(descr)
        self.__descr = descr
        self.__modbus_client = modbus_client
        self.__registrador = registrador
        self.__invertido = invertido

    @property
    def valor(self) -> float:
        """
        Valor

        Returns:
            float: valor já tratado
        """
        if self.__invertido:
            return False if self.raw else True
        else:
            return True if self.raw else False

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
                aux = self.__modbus_client.read_discrete_inputs(self.__registrador)[0]
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
    def __init__(
        self,
        descr: str,
        leitura_A: LeituraBase,
        leitura_B: LeituraBase,
        min_is_zero=True,
    ):
        super().__init__(descr)
        self.__leitura_A = leitura_A
        self.__leitura_B = leitura_B
        self.__min_is_zero = min_is_zero

    @property
    def valor(self) -> float:
        """
        Valor

        Returns:
            float: leitura_A - leitura_B
        """
        if self.__min_is_zero:
            return max(0, self.__leitura_A.valor - self.__leitura_B.valor)
        else:
            return self.__leitura_A.valor - self.__leitura_B.valor

class LeituraSoma(LeituraBase):
    def __init__(
        self,
        descr: str,
        leitura_A: LeituraBase,
        leitura_B: LeituraBase,
        min_is_zero=True,
    ):
        super().__init__(descr)
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

class LeituraComposta(LeituraBase):
    def __init__(
        self,
        descr: str,
        leitura1: LeituraBase,
        leitura2: LeituraBase = None,
        leitura3: LeituraBase = None,
        leitura4: LeituraBase = None,
        leitura5: LeituraBase = None,
        leitura6: LeituraBase = None,
        leitura7: LeituraBase = None,
        leitura8: LeituraBase = None,
    ):
        super().__init__(descr)
        self.__leitura1 = leitura1
        self.__leitura2 = leitura2
        self.__leitura3 = leitura3
        self.__leitura4 = leitura4
        self.__leitura5 = leitura5
        self.__leitura6 = leitura6
        self.__leitura7 = leitura7
        self.__leitura8 = leitura8

    @property
    def valor(self) -> float:
        """
        Valor

        Returns:
            float: 1*leitura1 + 2*leitura2 + 4*leitura3 + 8*leitura4...
        """
        res = 0
        if self.__leitura1 is not None:
            if self.__leitura1.valor:
                res += 2**0
        if self.__leitura2 is not None:
            if self.__leitura2.valor:
                res += 2**1
        if self.__leitura3 is not None:
            if self.__leitura3.valor:
                res += 2**2
        if self.__leitura4 is not None:
            if self.__leitura4.valor:
                res += 2**3
        if self.__leitura5 is not None:
            if self.__leitura5.valor:
                res += 2**4
        if self.__leitura6 is not None:
            if self.__leitura6.valor:
                res += 2**5
        if self.__leitura7 is not None:
            if self.__leitura7.valor:
                res += 2**6
        if self.__leitura8 is not None:
            if self.__leitura8.valor:
                res += 2**7
        return res

class LeituraDebug(LeituraBase):
    def __init__(self, descr: str) -> None:
        super().__init__(descr)

    @property
    def valor(self) -> float:
        return self.__valor

    @valor.setter
    def valor(self, var):
        self.__valor = var

class LeituraNBRPower(LeituraBase):
    def __init__(
        self,
        descr: str,
        ip_1: str = "localhost",
        port_1: int = 502,
        ip_2: str = None,
        port_2: int = None,
        escala: float = 1,
    ):
        super().__init__(descr)

        self.__ip_1 = ip_1
        self.__port_1 = port_1
        self.__escala = float(escala)

        if ip_2 is not None:
            self.__ip_2 = ip_2
        else:
            self.__ip_2 = ip_1

        if port_2 is not None:
            self.__port_2 = port_2
        else:
            self.__port_2 = port_1

    @property
    def valor(self) -> float:
        return self.raw * self.__escala

    @property
    def raw(self) -> int:
        try:
            sock = socket.socket()
            sock.settimeout(5)
            sock.connect((self.__ip_2, self.__port_2))
            data = bytes.fromhex(
                "019914000001020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
            )
            data = add_crc(data)
            sock.send(data)
            response = sock.recv(1024)
            sock.close()
            response = response[1:]
            return float(struct.unpack("f", response[64:68])[0])
        except Exception:
            self.logger.debug("Socket timed out")
            try:
                sock = socket.socket()
                sock.settimeout(5)
                sock.connect((self.__ip_2, self.__port_2))
                data = bytes.fromhex(
                    "019914000001020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                )
                data = add_crc(data)
                sock.send(data)
                response = sock.recv(1024)
                sock.close()
                response = response[1:]
                return float(struct.unpack("f", response[64:68])[0])
            except Exception:
                self.logger.debug("Socket timed out")
                return 0
        return 0
