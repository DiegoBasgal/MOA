import logging
import traceback

from time import sleep
from pyModbusTCP.client import ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder as BPD

from src.dicionarios.const import *

logger = logging.getLogger("__main__")

class LeituraModbus:
    def __init__(self, cli: "ModbusClient"=None, reg: "int"=None, op: "int"=None, escala: "float"=1, fundo_escala: "float"=0, descr: "str"=None):

        self.__cli = cli
        self.__escala = escala
        self.__fundo_escala = fundo_escala
        self.__op = 3 if op is None else op
        self.__reg = reg[0] if isinstance(reg, list) else reg

        self._descr = descr

    def __str__(self) -> "str":
        return f"Leitura {self._descr}, Valor: {self.valor}"

    @property
    def descr(self) -> "str":
        return self._descr

    @property
    def valor(self) -> "int | float":
        try:
            return (self.raw * self.__escala) + self.__fundo_escala

        except Exception:
            logger.error(f"[LER] Error ao calcular o valor da Leitura do registrador: \"{self.descr}\"")
            logger.info(f"[LER] Retornando dado Raw: {self.raw}...")
            sleep(TIMEOUT_PADRAO)
            return self.raw

    @property
    def raw(self) -> int:
        try:
            if self.__op == 3:
                ler = self.__cli.read_holding_registers(self.__reg)[0]
            elif self.__op == 4:
                ler = self.__cli.read_input_registers(self.__reg)[0]
            else:
                return 0

            return 0 if ler is None else ler

        except Exception:
            logger.error(f"[LER] Não foi possivel realizar a Leitura do dado RAW no registrador: \"{self._descr}\". Retornando 0.")
            logger.debug(traceback.format_exc())
            return 0

class LeituraModbusCoil:
    def __init__(self, cli: "ModbusClient"=None, reg: "int | list[int, int]"=None, op: "int"=1, descr: "str"=None) -> None:

        self.__op = op
        self.__cli = cli
        self.__reg = reg[0] if isinstance(reg, list) else reg

        self._descr = descr

    def __str__(self) -> "str":
        return f"Leitura {self._descr}, Valor: {self.valor}"

    @property
    def descr(self) -> "str":
        return self._descr

    @property
    def valor(self) -> "int":
        try:
            if self.__op == 1:
                raw = self.__cli.read_coils(self.__reg)[0]

            elif self.__op == 2:
                raw = self.__cli.read_discrete_inputs(self.__reg)[0]

            return 0 if raw is None else raw

        except Exception:
            logger.error(f"[LER] Não foi possivel realizar a Leitura Coil do dado RAW no registrador: \"{self._descr}\". Retornando 0.")
            logger.debug(traceback.format_exc())
            sleep(1)
            return 0


class LeituraModbusBit(LeituraModbus):
    def __init__(self, cli: "ModbusClient"=None, reg: "list[int, int]"=None, op: "int"=3, invertido: "bool"=None, descr: "str"=None) -> None:
        super().__init__(cli, reg, op, descr)

        self.__cli = cli
        self.__reg = reg[0]
        self.__bit = reg[1]
        self.__invertido = False if invertido is not None else invertido

        self._descr = descr

    @property
    def valor(self) -> "bool | None":
        try:
            raw = self.__cli.read_holding_registers(self.__reg)
            raw_dec_1 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)
            raw_dec_2 = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)

            if self.__bit >= 16:
                raw_aux = self.__cli.read_holding_registers(self.__reg + 1)
                raw_aux_dec_1 = BPD.fromRegisters(raw_aux, byteorder=Endian.Big, wordorder=Endian.Little)
                raw_aux_dec_2 = BPD.fromRegisters(raw_aux, byteorder=Endian.Big, wordorder=Endian.Little)
                lista_bits = [bit for bits in [raw_dec_2.decode_bits(2), raw_dec_1.decode_bits(1), raw_aux_dec_2.decode_bits(2), raw_aux_dec_1.decode_bits(1)] for bit in bits]

            else:
                lista_bits = [bit for bits in [raw_dec_2.decode_bits(2), raw_dec_1.decode_bits(1)] for bit in bits]

            for i in range(len(lista_bits)):
                if self.__bit == i:
                    return not lista_bits[i] if self.__invertido else lista_bits[i]

        except Exception:
            logger.error(f"[LER] houve um erro ao realizar a conversão do dado Raw para Biário. Retornando \"None\"...")
            logger.debug(traceback.format_exc())
            sleep(0)
            return None

class LeituraModbusFloat(LeituraModbus):
    def __init__(self, cli: "ModbusClient"=None, reg: "int"=None, op: "int"=3, descr: "str"=None):
        super().__init__(cli, reg, op, descr)

        self.__cli = cli
        self.__reg = reg[0] if isinstance(reg, list) else reg

    @property
    def valor(self) -> "int | float":
        try:
            raw = self.__cli.read_holding_registers(self.__reg)

            decoder = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)
            
            return decoder.decode_32bit_float()

        except Exception:
            logger.error(f"[LER] Houve um erro ao converter os valores Decimais para Float. Retornando 0.")
            logger.debug(traceback.format_exc())
            sleep(1)
            return 0

class LeituraSoma:
    def __init__(self, leituras: "list[LeituraModbus]"=None, min_zero: "bool"=False) -> None:

        if leituras is None:
            logger.error("[LER] A \"LeituraSoma\" precisa de 2 ou mais leituras para o argumento \"leituras\".")
            raise ValueError
        else:
            self.__leituras = leituras

        self.__min_is_zero = min_zero

    @property
    def valor(self) -> "int":
        try:
            if self.__min_is_zero:
                ret = sum(leitura.valor for leitura in self.__leituras)
                return max(0, ret)

        except Exception:
            logger.error(f"[LER] Houve um erro ao realizar a soma das Leituras. Retornando 0.")
            logger.debug(traceback.format_exc())
            sleep(1)
            return 0