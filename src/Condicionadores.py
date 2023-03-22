__author__ = "Lucas Lavratti", "Diego Basgal"
__credits__ = "Lucas Lavratti" , "Diego Basgal"

__version__ = "0.2"
__status__ = "Development"
__maintainer__ = "Diego Basgal"
__email__ = "diego.garcia@ritmoenergia.com.br"
__description__ = "Este módulo corresponde a implementação de acionamento de condicionadores de campo."


from leitura import *
from unidade_geracao import UnidadeDeGeracao

class CondicionadorBase:
    def __init__(
            self, 
            leitura: LeituraBase | None = ...,
            gravidade: int | None = ..., 
            etapas: list | None = ...,
            ug_id: int | None = ...
        ):
        self.__leitura = leitura
        self.__ug_id = None if ug_id is None else ug_id
        self.__etapas = [] if etapas is None else etapas
        self.__gravidade = 2 if gravidade is None else gravidade

        self._ugs: list[UnidadeDeGeracao]

    def __str__(self):
        return f"Condicionador: {self.descr}, Gravidade: {self.gravidade}"

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
    def __init__(self, leitura, gravidade, valor_base: float | None = ..., valor_limite: float | None = ..., ordem: float | None = ...) -> ...:
        CondicionadorBase.__init__(leitura, gravidade)
        self._ordem = 2 if ordem is None else ordem
        self._valor_base = 0 if valor_base is None else valor_base
        self._valor_limite = 0 if valor_limite is None else valor_limite

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
    def __init__(self,leitura, gravidade, valor_base, valor_limite, ordem) -> ...:
        CondicionadorExponencial.__init__(leitura, gravidade, valor_base, valor_limite, ordem)

    @property
    def valor(self) -> int | float:
        if self.valor_limite < self.leitura < self.valor_base:
            aux = (1 - (((self.valor_limite - self.leitura) / (self.valor_limite - self.valor_base))** (self.ordem)).real)
            return max(min(aux, 1), 0)
        else:
            return 0 if self.leitura < 1 or self.leitura >= self.valor_limite else 1
