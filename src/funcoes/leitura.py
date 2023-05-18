import logging

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class LeituraModbus:
    def __init__(self, clp: ModbusClient, reg: int, escala: float=None, fundo_escala: float=0, op: int=3, descr: str=None):

        if descr is None:
            raise ValueError(f"[LER] A descrição da Leitura é obrigatória para informações de controle.")

        if clp is None:
            logger.error(f"[LER] Não foi possível carregar a variável do CLP na instância de Leitura: \"{descr}\".")
            raise ValueError
        else:
            self.__clp = clp

        if reg is None:
            logger.error(f"[LER] Não foi possivel carregar o valor de registrador instância de Leitura: \"{descr}\".")
            raise ValueError
        else:
            self.__reg = reg

        self.__op = op
        self.__escala = escala
        self.__fundo_escala = fundo_escala
        self._descr = descr

    def __str__(self) -> str:
        return f"Leitura {self._descr}, Valor: {self.valor}"

    @property
    def valor(self) -> int:
        return (self.raw * self.__escala) + self.__fundo_escala

    @property
    def raw(self) -> int:
        try:
            if self.__op == 3:
                ler = self.__clp.read_input_registers(self.__reg)[0]
            elif self.__op == 4:
                ler = self.__clp.read_holding_registers(self.__reg)[0]
            else:
                return 0 if ler is None else ler

        except Exception:
            logger.error(f"[LER] Não foi possivel realizar a Leitura do dado RAW no registrador: \"{self._descr}\".")
            raise ValueError

    @property
    def descr(self) -> str:
        return self._descr

class LeituraModbusBit(LeituraModbus):
    def __init__(self, clp, reg, bit: int=None, invertido: bool=None, descr=None) -> None:
        super().__init__(clp, reg, descr)

        if bit is None:
            logger.error(f"[LER] Não foi possível carregar o valor do bit na instância de Leitura: \"{self._descr}\".")
        else:
            self.__bit = bit

        self.__invertido = False if invertido is not None else invertido

    @property
    def valor(self) -> bool:
        ler_bit = self.raw & 2**self.__bit
        return not ler_bit if self.__invertido else ler_bit


class LeituraSoma:
    def __init__(self, leituras: "list[LeituraModbus]"=None, min_zero: bool=False) -> None:

        if leituras < 2 or leituras is None:
            logger.error("[LER] A \"LeituraSoma\" precisa de 2 ou mais leituras para o argumento \"leituras\".")
            raise ValueError
        else:
            self.__leituras = leituras

        self.__min_is_zero = min_zero

    @property
    def valor(self) -> int:
        if self.__min_is_zero:
            return max(0, [sum(leitura.valor for leitura in self.__leituras)])
        else:
            return [sum(leitura.valor for leitura in self.__leituras)]