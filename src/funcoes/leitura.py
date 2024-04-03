import socket
import struct
import logging
import traceback

from src.dicionarios.reg import *
from pyModbusTCP.utils import crc16
from pyModbusTCP.client import ModbusClient


logger = logging.getLogger("logger")


class LeituraModbus:
    def __init__(self, cliente: "ModbusClient", registrador: "int", escala: "float"=1, fundo_escala: "float"=0, op: "int"=3, descricao: "str"=None):

        # PRIVADAS
        self.__cliente = cliente
        self.__registrador = registrador
        self.__escala = escala
        self.__fundo_escala = fundo_escala
        self.__op = op
        self.__descricao = descricao

    @property
    def cliente(self) -> "ModbusClient":
        # PROPRIEDADE -> Retorna a instância do Cliente Modbus
        return self.__cliente
    
    @property
    def registrador(self) -> "int":
        # PROPRIEDADE -> Retorna o Registrador da Leitura
        return self.__registrador

    @property
    def descricao(self) -> "str":
        # PROPRIEDADE -> Retorna a descrição da Leitura
        return self.__descricao

    @property
    def valor(self) -> "float":
        # PROPRIEDADE -> Retorna Valor calculado com escala e fundo de escala.
        return (self.raw * self.__escala) + self.__fundo_escala

    @property
    def raw(self) -> "int":
        # PROPRIEDADE -> Retorna Valor raw baseado no tipo de operação ModBus.
        try:
            if self.__cliente.open():
                if self.__op == 3:
                    lei = self.__cliente.read_holding_registers(self.__registrador)[0]
                elif self.__op == 4:
                    lei = self.__cliente.read_input_registers(self.__registrador)[0]

                return 0 if lei == None else lei

        except Exception:
            logger.error(f"[LEI] Houve um erro de Leitura do REG: {self.__descricao}")
            return 0


class LeituraModbusCoil(LeituraModbus):
    def __init__(self, cliente: "ModbusClient", registrador: "int", invertido: "bool" = False, descricao: "str"=None):
        super().__init__(cliente, registrador, descricao)

        # PRIVADAS
        self.__invertido = invertido

    @property
    def valor(self) -> "float":
        # PROPRIEDADE -> Retorna Valor normal ou invertido.
        if self.__invertido:
            return False if self.raw else True
        else:
            return True if self.raw else False

    @property
    def raw(self) -> "int":
        # PROPRIEDADE -> Retorna Valor raw ModBus.
        try:
            if self.cliente.open():
                lei = self.cliente.read_discrete_inputs(self.registrador)[0]

                return 0 if lei == None else lei

        except Exception:
            logger.debug(f"[LEI] Houve um erro na Leitura Coil do REG: {self.descricao}")
            logger.debug(traceback.format_exc())
            return 0


class LeituraModbusBit(LeituraModbus):
    def __init__(self, cliente: "ModbusClient", registrador: "int", bit: "int", invertido: "bool"=False, descricao: "str"=None,):
        super().__init__(descricao, cliente, registrador)

        # PRIVADAS
        self.__bit = bit
        self.__invertido = invertido


    @property
    def valor(self) -> "bool":
        # PROPRIEDADE -> Retorna Valor Bit ModBus.
        aux = self.raw & 2**self.__bit
        if self.__invertido:
            aux = not aux
        return aux


class LeituraDelta(LeituraModbus):
    def __init__(self, leitura_A: "LeituraModbus", leitura_B: "LeituraModbus", min_zero:"bool"=True, descricao: "str"=None):
        super().__init__(descricao)

        self.__leitura_A = leitura_A
        self.__leitura_B = leitura_B
        self.__min_zero = min_zero

    @property
    def valor(self) -> "float":
        # PROPRIEDADE -> Retorna Valor subtraído ModBus.
        val = self.__leitura_A.valor - self.__leitura_B.valor
        return max(0, val) if self.__min_zero else val


class LeituraSoma:
    def __init__(self, leituras: "list[LeituraModbus]", min_zero: "bool"=True, descricao: "str"=None,):

        # PRIVADAS
        self.__leituras = leituras
        self.__min_zero = min_zero


    @property
    def valor(self) -> float:
        # PROPRIEDADE -> Retorna Valor de soma de duas leituras ModBus.
        val = sum(leitura.valor for leitura in self.__leituras)
        return max(0, val) if self.__min_zero else val


class LeituraComposta:
    def __init__(self, leituras: "list[LeituraModbus]", descricao: "str"=None):

        # PRIVADAS
        self.__leituras = leituras


    @property
    def valor(self) -> "float":
        # PROPRIEDADE -> Retorna Valor composto de duas ou mais leituras ModBus.
        res = 0
        cont = 0
        for leitura in self.__leituras:
            if leitura is not None and leitura.valor:
                res += 2**cont
            cont += 1

        return res



class LeituraNBRPower(LeituraModbus):
    def __init__(self, ip_1: "str"="localhost", port_1: "int"=502, ip_2: "str"=None, port_2: "int"=None, escala: "float"=1, descricao: "str"=None):
        super().__init__(escala, descricao)

        # PRIVADAS
        self.__ip_2 = ip_2 if ip_2 is not None else ip_1
        self.__port_2 = port_2 if port_2 is not None else port_1

        self.__ip_1 = ip_1
        self.__port_1 = port_1
        self.__escala = float(escala)


    @property
    def valor(self) -> float:
        # PROPRIEDADE -> Retorna Valor calculado com escala.
        return self.raw * self.__escala

    @property
    def raw(self) -> int:
        # PROPRIEDADE -> Retorna Valor raw utilizando funções de conversão de valores
        # hexadecimais e funções de utilidade e conversão ModBus.

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


    def bcd_to_i(self, i):
        value = i & 0xF
        value += ((i >> 4) & 0xF) * 10
        value += ((i >> 8) & 0xF) * 100
        value += ((i >> 12) & 0xF) * 1000
        return value


    def add_crc(self, data):
        crc = hex(crc16(data))
        crc = bytes.fromhex(crc[4] + crc[5] + crc[2] + crc[3])
        return data + crc
