import socket
import struct
import logging

from pyModbusTCP.utils import crc16
from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class LeituraBase:
    def __init__(self, descr: str) -> None:
        self.__descr = descr
        self.__valor = None

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
        return self.__descr

class LeituraModbus(LeituraBase):
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
        return (self.raw * self.__escala) + self.__fundo_de_escala

    @property
    def raw(self) -> int:
        try:
            if self.__modbus_client.open():
                if self.__op == 3:
                    aux = self.__modbus_client.read_holding_registers(self.__registrador)[0]
                elif self.__op == 4:
                    aux = self.__modbus_client.read_input_registers(self.__registrador)[0]
                if aux is not None:
                    return aux
                else:
                    return 0
            else:
                raise ConnectionError("Erro na conexão modbus.")
        except:
            return 0

class LeituraModbusCoil(LeituraBase):
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
        if self.__invertido:
            return False if self.raw else True
        else:
            return True if self.raw else False

    @property
    def raw(self) -> int:
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
            return 0

class LeituraModbusBit(LeituraModbus):
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
        self.__escala = float(escala)
        self.__ip_2 = ip_2 if ip_2 is not None else ip_1
        self.__port_2 = port_2 if port_2 is not None else port_1

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
            data = self.add_crc(data)
            sock.send(data)
            response = sock.recv(1024)
            sock.close()
            response = response[1:]
            return float(struct.unpack("f", response[64:68])[0])
        except Exception:
            logger.debug("Socket timed out")
            try:
                sock = socket.socket()
                sock.settimeout(5)
                sock.connect((self.__ip_2, self.__port_2))
                data = bytes.fromhex(
                    "019914000001020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                )
                data = self.add_crc(data)
                sock.send(data)
                response = sock.recv(1024)
                sock.close()
                response = response[1:]
                return float(struct.unpack("f", response[64:68])[0])
            except Exception:
                logger.debug("Socket timed out")
                return 0

    def add_crc(self, data):
        crc = hex(crc16(data))
        crc = bytes.fromhex(crc[4] + crc[5] + crc[2] + crc[3])
        return data + crc
