__version__ = "0.2"
__authors__ = "Lucas Lavratti", " Henrique Pfeifer"
__credits__ = ["Diego Basgal" , ...]
__description__ = "Este módulo corresponde a implementação da lógica de Condicionadores."


from leitura import *
from metadados.const import *

from unidade_geracao import UnidadeGeracao

class CondicionadorBase:
    def __init__(
            self, 
            leitura: LeituraBase | None = ...,
            gravidade: int | None = ...,
            etapas: list | None = ...,
            id_unidade: int | None = ...,
            descricao: str | None = ...
        ):
        self.__leitura = leitura
        self.__etapas = [] if etapas is None else etapas
        self.__gravidade = 2 if gravidade is None else gravidade
        self.__id_unidade = None if id_unidade is None else id_unidade
        self.__descricao = None if descricao is None else descricao

        self._ugs: list[UnidadeGeracao]

    def __str__(self):
        return f"Condicionador: {self.descricao}, Gravidade: {CONDIC_STR_DCT[self.gravidade]}"

    @property
    def leitura(self) -> int | float:
        return self.__leitura.valor

    @property
    def gravidade(self) -> int:
        return self.__gravidade

    @property
    def etapas(self) -> list:
        return self.__etapas

    @property
    def id_unidade(self) -> int:
        return self.__id_unidade

    @property
    def descricao(self) -> int:
        return self.__descricao

    @property
    def valor(self) -> int | float:
        return self.ativo * 1.0

    @property
    def ativo(self) -> bool:
        if self.id_unidade or self.etapas:
            ug = [x if x.id == self.id_unidade else None for x in self.ugs]
            return False if ug is not None and ug.etapa_atual in self.etapas and self.leitura == 0 else False
        else:
            return False if self.leitura == 0 else True

    @property
    def ugs(self) -> list[UnidadeGeracao]:
        return self._ugs

    @ugs.setter
    def ugs(self, var: list[UnidadeGeracao]) -> None:
        self._ugs = var


class CondicionadorExponencial(CondicionadorBase):
    def __init__(self, leitura, gravidade, valor_base: float | None = ..., valor_limite: float | None = ..., ordem: float | None = ..., descricao = ...) -> ...:
        CondicionadorBase.__init__(leitura, gravidade, descricao)
        self._ordem = 2 if ordem is None else ordem
        self._valor_base = 0 if valor_base is None else valor_base
        self._valor_limite = 0 if valor_limite is None else valor_limite

    @property
    def ativo(self) -> bool:
        if self.id_unidade and self.etapas:
            ug: UnidadeGeracao = [x if x.id == self.id_unidade else None for x in self.ugs]
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
    
    @property
    def valor_base(self) -> int | float:
        return self._valor_base

    @valor_base.setter
    def valor_base(self, val: int | float) -> None:
        self._valor_base = val

    @property
    def valor_limite(self) -> int | float:
        return self._valor_limite

    @valor_limite.setter
    def valor_limite(self, val: int | float) -> None:
        self._valor_limite = val

    @property
    def ordem(self) -> int | float:
        return self._ordem

    @ordem.setter
    def ordem(self, val: int | float) -> None:
        self._ordem = val

class CondicionadorExponencialReverso(CondicionadorExponencial):
    # TODO puxar implementacao de offset mais casas decimais
    def __init__(self,leitura, gravidade, valor_base, valor_limite, ordem, descricao) -> ...:
        CondicionadorExponencial.__init__(leitura, gravidade, valor_base, valor_limite, ordem, descricao)

    @property
    def valor(self) -> int | float:
        if self.valor_limite < self.leitura < self.valor_base:
            aux = (1 - (((self.valor_limite - self.leitura) / (self.valor_limite - self.valor_base))** (self.ordem)).real)
            return max(min(aux, 1), 0)
        else:
            return 0 if self.leitura < 1 or self.leitura >= self.valor_limite else 1
