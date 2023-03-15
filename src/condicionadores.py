__version__ = "0.1"
__author__ = "Lucas Lavratti"

from leituras import *

class CondicionadorBase:
    def __init__(self, descr: str, gravidade: int, leitura: LeituraBase, ug_id: int = None, etapas: list = None):
        self.__descr = descr
        self.__leitura = leitura
        self.__gravidade = gravidade

        self._ugs = []

        self.ug_id = ug_id if ug_id is not None else None
        self.etapas = etapas if etapas is not None else []

    def __str__(self):
        return f"Condicionador: {self.__descr}, Gravidade: {self.__gravidade}"

    @property
    def descr(self):
        return self.__descr

    @property
    def leitura(self):
        return self.__leitura

    @property
    def ativo(self) -> bool:
        if self.ug_id or self.etapas:
            ug = [x if x.id == self.ug_id else None for x in self.ugs]
            return True if ug is not None and ug.etapa_atual in self.etapas and self.leitura.valor == 0 else False
        else:
            return False if self.leitura.valor == 0 else True

    @property
    def valor(self) -> float:
        return self.ativo * 1.0

    @property
    def gravidade(self) -> int:
        return self.__gravidade

    @property
    def ugs(self) -> list:
        return self.__ugs

    @ugs.setter
    def ugs(self, ugs: list) -> None:
        self.__ugs = ugs

class CondicionadorExponencial(CondicionadorBase):
    def __init__(
        self,
        descr: str,
        gravidade: int,
        leitura: LeituraBase,
        valor_base: float,
        valor_limite: float,
        ordem: float = (1 / 4),
        ug_id: int = None,
        etapas: list = None
    ):
        super().__init__(descr, gravidade, leitura, ug_id, etapas)
        self._ordem = ordem
        self._valor_base = valor_base
        self._valor_limite = valor_limite

    @property
    def valor_base(self):
        return self._valor_base

    @valor_base.setter
    def valor_base(self, var):
        self._valor_base = var

    @property
    def valor_limite(self):
        return self._valor_limite

    @valor_limite.setter
    def valor_limite(self, var):
        self._valor_limite = var

    @property
    def ordem(self):
        return self._ordem

    @ordem.setter
    def ordem(self, var):
        self._ordem = var

    @property
    def ativo(self) -> bool:
        if self.ug_id and self.etapas:
            ug = [x if x.id == self.ug_id else None for x in self.ugs]
            return True if ug is not None and ug.etapa_atual in self.etapas and self.valor >= 1 else False
        else:
            return True if self.valor >= 1 else False

    @property
    def valor(self) -> float:
        v_temp = float(self.leitura.valor)

        if v_temp > self.valor_base and  v_temp < self.valor_limite:
            aux = (1 - (((self.valor_limite - v_temp) / (self.valor_limite - self.valor_base)) ** (self.ordem)).real)
            return max(min(aux, 1), 0)

        if self.leitura.valor > self.valor_limite:
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
        super().__init__(descr, gravidade, leitura)
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
