__version__ = "0.1"
__author__ = "Lucas Lavratti"

from usina import usina
from leituras import *

class CondicionadorBase:
    def __init__(self, descr: str, gravidade: int, leitura: LeituraBase, ug_id: int = None, estados: list = None):
        self.__descr = descr
        self.__leitura = leitura
        self.__gravidade = gravidade
        self.__ugs = usina.get_ugs()
        self.__ug_id = ug_id if ug_id is not None else None
        self.__estados = estados if estados is not None else []

    def __str__(self):
        return f"Condicionador: {self.__descr}, Gravidade: {self.__gravidade}"
    
    @property
    def descr(self):
        return self.__descr

    @property
    def leitura(self):
        return self.__leitura.valor

    @property
    def ativo(self) -> bool:
        for ug in self.__ugs:
            if ug.id == self.__ug_id and ug.etapa_atual in self.__estados:
                return False if self.leitura == 0 else True
            elif ug.id == self.__ug_id and self.__estados == []:
                return False if self.leitura == 0 else True
            else:
                return False

    @property
    def valor(self) -> float:
        return self.ativo * 1.0

    @property
    def gravidade(self) -> int:
        return self.__gravidade

class CondicionadorExponencial(CondicionadorBase):
    def __init__(
        self,
        descr: str,
        gravidade: int,
        leitura: LeituraBase,
        valor_base: float,
        valor_limite: float,
        ordem: float = (1 / 4),
    ):
        super().__init__(descr, gravidade, leitura, ug_id=None, estados=None)
        self.__ordem = ordem
        self.__valor_base = valor_base
        self.__valor_limite = valor_limite

    @property
    def valor_base(self):
        return self.__valor_base

    @valor_base.setter
    def valor_base(self, var):
        self.__valor_base = var

    @property
    def valor_limite(self):
        return self.__valor_limite

    @valor_limite.setter
    def valor_limite(self, var):
        self.__valor_limite = var

    @property
    def ordem(self):
        return self.__ordem

    @ordem.setter
    def ordem(self, var):
        self.__ordem = var

    @property
    def ativo(self) -> bool:
        for ug in self.__ugs:
            if ug.id == self.__ug_id and ug.etapa_atual in self.__estados:
                return True if self.valor >= 1 else False
            elif ug.id == self.__ug_id and self.__estados == []:
                return True if self.valor >= 1 else False
            else:
                return False

    @property
    def valor(self) -> float:
        v_temp = float(self.leitura)

        if v_temp > self.valor_base and  v_temp < self.valor_limite:
            aux = (1 - (((self.valor_limite - v_temp) / (self.valor_limite - self.valor_base)) ** (self.ordem)).real)
            return max(min(aux, 1), 0)

        if self.leitura > self.valor_limite:
            return 1

        else:
            return 0

class CondicionadorExponencialReverso(CondicionadorBase):
    def __init__(
        self,
        descr: str,
        gravidade: int,
        leitura: LeituraBase,
        valor_base: float,
        valor_limite: float,
        ordem: float = 2,
    ):
        super().__init__(descr, gravidade, leitura, ug_id=None, estados=None)
        self.__ordem = ordem
        self.__valor_base = valor_base
        self.__valor_limite = valor_limite

    @property
    def valor_base(self) -> float:
        return self.__valor_base

    @valor_base.setter
    def valor_base(self, var):
        self.__valor_base = var

    @property
    def valor_limite(self) -> float:
        return self.__valor_limite

    @valor_limite.setter
    def valor_limite(self, var):
        self.__valor_limite = var

    @property
    def ordem(self):
        return self.__ordem

    @ordem.setter
    def ordem(self, var):
        self.__ordem = var

    @property
    def valor(self) -> float:
        v_temp = float(self.leitura)

        if v_temp < 1:
            return 0

        elif self.valor_limite < v_temp < self.valor_base:
            aux = (1 - (((self.valor_limite - v_temp) / (self.valor_limite - self.valor_base))** (self.ordem)).real)
            return max(min(aux, 1), 0)

        elif v_temp <= self.valor_limite:
            return 1

        else:
            return 0
