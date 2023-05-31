import struct
import logging
import traceback

from pyModbusTCP.utils import decode_ieee, word_list_to_long
from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class LeituraModbus:
    def __init__(self, clp: ModbusClient, reg: "int | list[int, int]", escala: float=1, fundo_escala: float=0, op: int=3, decode: bool=False, descr: str=None):

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
        self.__decode_nv = decode
        self._descr = descr

    def __str__(self) -> str:
        return f"Leitura {self._descr}, Valor: {self.valor}"

    @property
    def valor(self) -> float:
        return (self.raw * self.__escala) + self.__fundo_escala

    @property
    def raw(self) -> "int | float":
        try:
            if self.__decode_nv:
                raw_1 = self.__clp.read_holding_registers(self.__reg)[0]
                raw_2 = self.__clp.read_holding_registers(self.__reg + 1)[0]

                n = 16
                aux = (raw_1 / (2 ** n))
                while aux < 1:
                    n = n - 1
                    aux = (raw_1 / (2 ** n))

                n = n + 1
                bin_1 = str('{0:0b}'.format(raw_1))

                if (n) < 16:
                    for _ in range(16 - n):
                        aux_b1 = bin_1
                        bin_1 = '0' + aux_b1

                bin_2 = '{0:0b}'.format(raw_2)
                bin_conv = int((bin_2 + bin_1), 2)

                ret = self.ieee_754_conversion(bin_conv, exp_len=8, mant_len=23)
                print(f"Nível Montatante: {ret}")
                return None

            elif self.__op == 3:
                ler = self.__clp.read_holding_registers(self.__reg)[0]
            elif self.__op == 4:
                ler = self.__clp.read_input_registers(self.__reg)[0]

            return 0 if ler is None else ler

        except Exception:
            logger.error(f"[LER] Não foi possivel realizar a Leitura do dado RAW no registrador: \"{self._descr}\".")
            raise ValueError

    @property
    def descr(self) -> str:
        return self._descr

    def ieee_754_conversion(self, bin, sgn_len=1, exp_len=8, mant_len=23):
        try:
            if bin >= 2 ** (sgn_len + exp_len + mant_len):
                raise ValueError("Number bin is longer than prescribed parameters allows")

            sign = (bin & (2 ** sgn_len - 1) * (2 ** (exp_len + mant_len))) >> (exp_len + mant_len)
            exponent_raw = (bin & ((2 ** exp_len - 1) * (2 ** mant_len))) >> mant_len
            mantissa = bin & (2 ** mant_len - 1)

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
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return None

class LeituraModbusBit(LeituraModbus):
    def __init__(self, clp, reg: "list[int, int]", invertido: bool=None, descr=None) -> None:
        super().__init__(clp, reg, descr)

        self.__bit = reg[1]
        self.__invertido = False if invertido is not None else invertido

    @property
    def valor(self) -> bool:
        ler_bit = self.raw & 2**self.__bit
        return not ler_bit if self.__invertido else ler_bit

class LeituraSoma:
    def __init__(self, leituras: "list[LeituraModbus]"=None, min_zero: bool=False, decode: bool=False) -> None:

        if leituras is None:
            logger.error("[LER] A \"LeituraSoma\" precisa de 2 ou mais leituras para o argumento \"leituras\".")
            raise ValueError
        else:
            self.__leituras = leituras

        self.__decode_nv = decode
        self.__min_is_zero = min_zero

    @property
    def valor(self) -> int:
        if self.__min_is_zero:
            return max(0, [sum(leitura.valor for leitura in self.__leituras)])
        elif self.__decode_nv:
            return decode_ieee(sum(leitura.valor for leitura in self.__leituras))