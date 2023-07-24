__version__ = "0.2"
__author__ = "Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da lógica de Condicionadores."

from funcoes.leitura import *
from dicionarios.const import *

from unidade_geracao import UnidadeGeracao

class CondicionadorBase:
    def __init__(self, leitura: "LeituraModbus"=None, gravidade: "int"=None, etapas: "list"=None, id_unidade: "int"=None) -> "None":

        self.__leitura = leitura
        self.__gravidade = 2 if gravidade is None else gravidade
        self.__descricao = leitura.descricao

        self.__etapas = [] if etapas is None else etapas
        self.__id_unidade = None if id_unidade is None else id_unidade

        self._ugs: "list[UnidadeGeracao]"

    def __str__(self) -> "str":
        """
        Função que retorna string com detalhes do condicionador para logger.
        """

        return f"Condicionador: {self.descricao}, Gravidade: {CONDIC_STR_DCT[self.gravidade]}"

    @property
    def leitura(self) -> "float":
        # PROPRIEDADE -> Retrona o valor crú de Leitura do Condicionador.

        return self.__leitura.valor

    @property
    def gravidade(self) -> "int":
        # PROPRIEDADE -> Retrona a Gravidade do Condicionador.

        return self.__gravidade

    @property
    def descricao(self) -> "int":
        # PROPRIEDADE -> Retrona a Descrição do Condicionador.

        return self.__descricao

    @property
    def valor(self) -> "float":
        # PROPRIEDADE -> Retrona o valor tratado de Leitura do Condicionador.

        return self.ativo * 1.0

    @property
    def ativo(self) -> "bool":
        # PROPRIEDADE -> Retrona se o Condicionaor está Ativo.

        if self.__id_unidade and self.__etapas:
            for ug in self.ugs:
                if ug.id == self.__id_unidade and ug.etapa_atual in self.__etapas:
                    return False if self.leitura == 0 else True
            else:
                return False

        else:
            return False if self.leitura == 0 else True

    @property
    def ugs(self) -> "list[UnidadeGeracao]":
        # PROPRIEDADE -> Retrona a lista de instâncias das Unidades de Geração.

        return self._ugs

    @ugs.setter
    def ugs(self, var: "list[UnidadeGeracao]") -> "None":
        # SETTER -> Atribui a nova lista de instâncias das Unidades de Geração.

        self._ugs = var


class CondicionadorExponencial(CondicionadorBase):
    def __init__(self, leitura, gravidade, valor_base: "float"=None, valor_limite: "float"=None, ordem: "float"=None) -> "None":
        super().__init__(leitura, gravidade)

        self._ordem = 2 if ordem is None else ordem
        self._valor_base = 0 if valor_base is None else valor_base
        self._valor_limite = 0 if valor_limite is None else valor_limite

    @property
    def ativo(self) -> "bool":
        # PROPRIEDADE -> Retrona se o Condicionaor está Ativo.

        return True if self.valor >= 1 else False

    @property
    def valor(self) -> "float":
        # PROPRIEDADE -> Retrona o valor tratado de Leitura do Condicionador.

        if self.leitura > self.valor_base and  self.leitura < self.valor_limite:
            aux = (1 - (((self.valor_limite - self.leitura) / (self.valor_limite - self.valor_base)) ** (self.ordem)).real)
            return max(min(aux, 1), 0)

        else:
            return 1 if self.leitura > self.valor_limite else 0

    @property
    def ordem(self) -> "float":
        # PROPRIEDADE -> Retrona a Ordem do Condicionador.

        return self._ordem

    @ordem.setter
    def ordem(self, val: "float") -> "None":
        # SETTER -> Atribui o novo valor de Ordem do Condicionador.

        self._ordem = val

    @property
    def valor_base(self) -> "float":
        # PROPRIEDADE -> Retrona o Valor Base do Condicionador.

        return self._valor_base

    @valor_base.setter
    def valor_base(self, val: "float") -> "None":
        # SETTER -> Atribui o novo Valor Base do Condicionador.

        self._valor_base = val

    @property
    def valor_limite(self) -> "float":
        # PROPRIEDADE -> Retrona o Valor Limite do Condicionador.

        return self._valor_limite

    @valor_limite.setter
    def valor_limite(self, val: "float") -> "None":
        # SETTER -> Atribui o novo Valor Limite do Condicionador.

        self._valor_limite = val


class CondicionadorExponencialReverso(CondicionadorExponencial):
    def __init__(self ,leitura, gravidade, valor_base, valor_limite, ordem) -> "None":
        super().__init__(leitura, gravidade, valor_base, valor_limite, ordem)

    @property
    def valor(self) -> "float":
        # PROPRIEDADE -> Retrona o Valor do Condicionador.

        if self.valor_limite < self.leitura < self.valor_base:
            aux = (1 - (((self.valor_limite - self.leitura) / (self.valor_limite - self.valor_base))** (self.ordem)).real)
            return max(min(aux, 1), 0)

        else:
            return 0 if self.leitura < 1 or self.leitura >= self.valor_limite else 1
