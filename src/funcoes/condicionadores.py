__version__ = "0.2"
__author__ = "Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da lógica de Condicionadores."

import src.unidade_geracao as ug
import src.funcoes.leitura as lei

from src.dicionarios.const import *


class CondicionadorBase:
    def __init__(self, leitura: "lei.LeituraModbus", gravidade: "int"=1, etapas: "list"=[], id_unidade: "int"=None, leitura_conjunta: "lei.LeituraModbus"=None) -> "None":

        self.__leitura = leitura
        self.__gravidade = gravidade
        self.__descricao = leitura.descricao

        self.__etapas = etapas
        self.__id_unidade = id_unidade
        self.__leitura_conjunta = leitura_conjunta

        self._ugs: "list[ug.UnidadeGeracao]" = []

    def __str__(self) -> "str":
        """
        Função que retorna string com detalhes do condicionador para logger.
        """

        return f"Condicionador: {self.__descricao}, Gravidade: {CONDIC_STR_DCT[self.gravidade]}"

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
            ug: "ug.UnidadeGeracao" = [ug if ug.id == self.__id_unidade else None for ug in self.ugs]
            return False if ug is not None and ug.etapa_atual in self.__etapas and self.leitura == 0 else False
        elif self.__leitura_conjunta != None:
            return False if self.leitura == 0 and self.__leitura_conjunta.valor == 0 else True
        else:
            return False if self.leitura == 0 else True

    @property
    def ugs(self) -> "list[ug.UnidadeGeracao]":
        # PROPRIEDADE -> Retrona a lista de instâncias das Unidades de Geração.

        return self._ugs

    @ugs.setter
    def ugs(self, var: "list[ug.UnidadeGeracao]") -> "None":
        # SETTER -> Atribui a nova lista de instâncias das Unidades de Geração.

        self._ugs = var


class CondicionadorExponencial(CondicionadorBase):
    def __init__(self, leitura: "lei.LeituraModbus", gravidade: "int"=2, valor_base: "float"=100, valor_limite: "float"=200, ordem: "float"=(1/4)) -> "None":
        super().__init__(leitura, gravidade)

        self.__ordem = ordem
        self.__valor_base = valor_base
        self.__valor_limite = valor_limite


    @property
    def valor_base(self) -> "float":
        # PROPRIEDADE -> Retrona o Valor Base do Condicionador.

        return self.__valor_base

    @valor_base.setter
    def valor_base(self, val: "float") -> "None":
        # SETTER -> Atribui o novo Valor Base do Condicionador.

        self.__valor_base = val

    @property
    def valor_limite(self) -> "float":
        # PROPRIEDADE -> Retrona o Valor Limite do Condicionador.

        return self.__valor_limite

    @valor_limite.setter
    def valor_limite(self, val: "float") -> "None":
        # SETTER -> Atribui o novo Valor Limite do Condicionador.

        self.__valor_limite = val

    @property
    def ordem(self) -> "float":
        # PROPRIEDADE -> Retorna o valor da Ordem do Condicionador.

        return self.__ordem

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


class CondicionadorExponencialReverso(CondicionadorExponencial):
    def __init__(self, leitura: "lei.LeituraModbus", gravidade: "int"=2, valor_base: "float"=100, valor_limite: "float"=200, ordem: "float"=(1/4)) -> "None":
        super().__init__(leitura, gravidade, valor_base, valor_limite, ordem)

    @property
    def valor(self) -> "float":
        # PROPRIEDADE -> Retrona o Valor do Condicionador.

        if self.valor_limite < self.leitura < self.valor_base:
            aux = (1 - (((self.valor_limite - self.leitura) / (self.valor_limite - self.valor_base))** (self.ordem)).real)
            return max(min(aux, 1), 0)

        else:
            return 0 if self.leitura < 1 or self.leitura >= self.valor_limite else 1
