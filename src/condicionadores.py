__version__ = "0.1"
__author__ = "Lucas Lavratti"

from leituras import *
from unidade_geracao import UnidadeDeGeracao

class CondicionadorBase:
    def __init__(self, leitura: LeituraBase, gravidade: int=2, etapas: list=[], ug_id: int=None, descr: str=None):
        self.__etapas = etapas
        self.__leitura = leitura
        self.__gravidade = gravidade
        self.__descr = leitura.descr
        self.__ug_id = ug_id if ug_id is not None else None

        self._ugs: list[UnidadeDeGeracao]

    def __str__(self):
        return f"Condicionador: {self.descr}, Gravidade: {self.gravidade}"

    @property
    def leitura(self) -> int | float:
        return self.__leitura.valor

    @property
    def descr(self) -> str:
        return self.__descr

    @property
    def gravidade(self) -> int:
        return self.__gravidade

    @property
    def etapas(self) -> list:
        return self.__etapas

    @property
    def ug_id(self) -> int:
        return self.__ug_id

    @property
    def valor(self) -> int | float:
        return self.ativo * 1.0

    @property
    def ativo(self) -> bool:
        if self.ug_id or self.etapas:
            ug: UnidadeDeGeracao = [x if x.id == self.ug_id else None for x in self.ugs]
            return False if ug is not None and ug.etapa_atual in self.etapas and self.leitura == 0 else False
        else:
            return False if self.leitura == 0 else True

    @property
    def ugs(self) -> list[UnidadeDeGeracao]:
        return self._ugs

    @ugs.setter
    def ugs(self, var: list[UnidadeDeGeracao]) -> None:
        self._ugs = var

class CondicionadorExponencial(CondicionadorBase):
    def __init__(
            self,
            leitura: LeituraBase,
            gravidade: int=2,
            valor_base: float=100,
            valor_limite: float=200,
            ordem: float=(1 / 4),
            descr: str=None
        ):
        super().__init__(leitura, gravidade, descr)
        self.__ordem = ordem
        self.__valor_base = valor_base
        self.__valor_limite = valor_limite

    @property
    def valor_base(self) -> int | float:
        return self.__valor_base

    @property
    def valor_limite(self) -> int | float:
        return self.__valor_limite

    @property
    def ordem(self) -> int | float:
        return self.__ordem

    @property
    def ativo(self) -> bool:
        if self.ug_id and self.etapas:
            ug: UnidadeDeGeracao = [x if x.id == self.ug_id else None for x in self.ugs]
            return True if ug is not None and ug.etapa_atual in self.etapas and self.valor >= 1 else False
        else:
            return True if self.valor >= 1 else False

    @property
    def valor(self) -> int | float:
        if self.leitura > self.valor_base and  self.leitura < self.valor_limite:
            aux = (1 - (((self.valor_limite - self.leitura) / (self.valor_limite - self.valor_base)) ** (self.ordem)).real)
            return max(min(aux, 1), 0)
        else:
            return 1 if self.leitura > self.valor_limite else 0

class CondicionadorExponencialReverso(CondicionadorBase):
    def __init__(
            self,
            leitura: LeituraBase,
            gravidade: int=2,
            valor_base: float=16,
            valor_limite: float=15.5,
            ordem: float=2,
            descr: str=None
        ):
        super().__init__(leitura, gravidade, descr)
        self.__ordem = ordem
        self.__valor_base = valor_base
        self.__valor_limite = valor_limite

    @property
    def valor_base(self) -> int | float:
        return self.__valor_base

    @property
    def valor_limite(self) -> int | float:
        return self.__valor_limite

    @property
    def ordem(self) -> int | float:
        return self.__ordem

    @property
    def valor(self) -> int | float:
        if self.valor_limite < self.leitura < self.valor_base:
            aux = (1 - (((self.valor_limite - self.leitura) / (self.valor_limite - self.valor_base))** (self.ordem)).real)
            return max(min(aux, 1), 0)

        else:
            return 0 if self.leitura < 1 or self.leitura >= self.valor_limite else 1
