import logging
import traceback

from time import sleep
from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class LeituraModbus:
    def __init__(self, clp: "ModbusClient", reg: "int", escala: "float"=1, fundo_escala: "float"=0, op: "int"=3, descr: "str"=None):

        if clp is None:
            logger.error(f"[LER] Não foi possível carregar a variável do CLP na instância de Leitura: \"{descr}\".")
            raise ValueError
        else:
            self.__clp = clp

        if reg is None:
            logger.error(f"[LER] Não foi possivel carregar o valor de registrador instância de Leitura: \"{descr}\".")
            raise ValueError
        else:
            self.__reg = reg[0] if isinstance(reg, list) else reg

        self.__op = op
        self.__escala = escala
        self.__fundo_escala = fundo_escala

        self._descr = descr

    def __str__(self) -> "str":
        return f"Leitura {self._descr}, Valor: {self.valor}"

    @property
    def valor(self) -> "int | float":
        try:
            return (self.raw * self.__escala) + self.__fundo_escala

        except Exception:
            logger.error(f"[LER] Error ao calcular o valor da Leitura do registrador: \"{self.descr}\"")
            logger.debug("")
            logger.info(f"[LER] Retornando dado Raw: {self.raw}...")
            sleep(1)
            return self.raw

    @property
    def raw(self) -> "int":
        try:
            if self.__op == 3:
                ler = self.__clp.read_holding_registers(self.__reg)[0]

            elif self.__op == 4:
                ler = self.__clp.read_input_registers(self.__reg)[0]

            return 0 if ler is None else ler

        except Exception:
            logger.error(f"[LER] Não foi possivel realizar a Leitura do dado RAW no registrador: \"{self._descr}\".")
            logger.debug(f"[LER] Traceback: {traceback.format_exc()}")
            logger.debug("")
            logger.info(f"[LER] Retornando 0...")
            return 0

    @property
    def descr(self) -> "str":
        return self._descr

class LeituraModbusCoil:
    def __init__(self, clp: "ModbusClient", reg: "int | list[int, int]", op: "int"=1, descr: "str"=None) -> None:

        if clp is None:
            logger.error(f"[LER] Não foi possível carregar a variável do CLP na instância de Leitura: \"{descr}\"")
            raise ValueError
        else:
            self.__clp = clp

        if reg is None:
            logger.error(f"[LER] Não foi possivel carregar o valor de registrador instância de Leitura: \"{descr}\"")
            raise ValueError
        else:
            self.__reg = reg[0] if isinstance(reg, list) else reg

        self.__op = op

        self._descr = descr

    def __str__(self) -> "str":
        return f"Leitura {self._descr}, Valor: {self.valor}"

    @property
    def valor(self) -> "int":
        return self.raw

    @property
    def raw(self) -> "int":
        try:
            if self.__op == 1:
                ler = self.__clp.read_coils(self.__reg)[0]

            elif self.__op == 2:
                ler = self.__clp.read_discrete_inputs(self.__reg)[0]

            return 0 if ler is None else ler

        except Exception:
            logger.error(f"[LER] Não foi possivel realizar a Leitura Coil do dado RAW no registrador: \"{self._descr}\"")
            logger.debug(f"[LER] Traceback: {traceback.format_exc()}")
            logger.debug("")
            logger.info(f"[LER] Retornando 0...")
            sleep(1)
            return 0

    @property
    def descr(self) -> "str":
        return self._descr


class LeituraModbusBit(LeituraModbus, LeituraModbusCoil):
    def __init__(self, clp: "ModbusClient", reg: "int | list[int, int]"=None, op: "int"=3, descr: "str"=None, invertido: "bool"=None) -> None:
        super().__init__(clp, reg, op, descr)

        self.__bit = reg[1]
        self.__invertido = False if invertido is not None else invertido

    @property
    def valor(self) -> "bool | None":
        try:
            ler_bit = self.raw & 2**self.__bit

            return not ler_bit if self.__invertido else ler_bit

        except Exception:
            logger.error(f"[LER] houve um erro ao realizar a conversão do dado Raw para Biário.")
            logger.debug(f"[LER] Traceback: {traceback.format_exc()}")
            logger.debug("")
            logger.info(f"[LER] Retornando \"None\"...")
            sleep(0)
            return None

class LeituraModbusFloat(LeituraModbus):
    def __init__(self, clp: "ModbusClient"=None, reg: "int"=None, op: "int"=3, descr: "str"=None):
        super().__init__(clp, reg, op, descr)
        self.__clp = clp
        self.__reg = reg[0] if isinstance(reg, list) else reg

    @property
    def raw_1(self) -> "int":
        return self.__clp.read_holding_registers(self.__reg)[0]

    @property
    def raw_2(self) -> "int":
        return self.__clp.read_holding_registers(self.__reg + 1)[0]

    @property
    def valor(self) -> "int | float":
        try:
            n = 16
            aux = (self.raw_1 / (2 ** n))

            bin_1 = str('{0:0b}'.format(self.raw_1))
            bin_2 = '{0:0b}'.format(self.raw_2)

            while aux < 1:
                n = n - 1
                aux = (self.raw_1 / (2 ** n))

            n = n + 1

            if (n) < 16:
                for _ in range(16 - n):
                    aux = bin_1
                    bin_1 = '0' + aux

            bin_conv = int((bin_2 + bin_1), 2)
            ret = self.ieee_754_conversion(bin_conv, exp_len=8, mant_len=23)

            return 0 if ret is None else ret

        except Exception:
            logger.error(f"[LER] Houve um erro ao converter os valores Decimais para Float")
            logger.debug(f"[LER] Traceback: {traceback.format_exc()}")
            logger.debug("")
            logger.info(f"[LER] Retornando 0...")
            sleep(1)
            return 0

    def ieee_754_conversion(self, binary, sgn_len=1, exp_len=8, mant_len=23) -> "int | float":
        try:
            if binary >= 2 ** (sgn_len + exp_len + mant_len):
                raise ValueError("[LER] O número binário é maior que o permitido, descrito nos parâmetros")

            sign = (binary & (2 ** sgn_len - 1) * (2 ** (exp_len + mant_len))) >> (exp_len + mant_len)
            exponent_raw = (binary & ((2 ** exp_len - 1) * (2 ** mant_len))) >> mant_len
            mantissa = binary & (2 ** mant_len - 1)

            sign_mult = 1
            if sign == 1:
                sign_mult = -1

            if exponent_raw == 2 ** exp_len - 1:
                if mantissa == 2 ** mant_len - 1:
                    return float('nan')

                return sign_mult * float('inf')

            exponent = exponent_raw - (2 ** (exp_len - 1) - 1)

            if exponent_raw == 0:
                    mant_mult = 0
            else:
                mant_mult = 1

            for b in range(mant_len - 1, -1, -1):
                if mantissa & (2 ** b):
                    mant_mult += 1 / (2 ** (mant_len - b))

            return sign_mult * (2 ** exponent) * mant_mult

        except Exception:
            logger.error(f"[LER] Erro na conversão de binário para Float")
            logger.debug(f"[LER] Traceback: {traceback.format_exc()}")
            logger.debug("")
            logger.info(f"[LER] Retornando 0...")
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
            logger.error(f"[LER] Houve um erro ao realizar a soma das Leituras")
            logger.debug(f"[LER] Traceback: {traceback.format_exc()}")
            logger.debug("")
            logger.info(f"[LER] Retornando 0...")
            sleep(1)
            return 0