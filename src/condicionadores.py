from src.funcoes.leitura import *
from src.funcoes.leitura import LeituraModbus
from src.unidade_geracao import UnidadeDeGeracao

class CondicionadorBase:
    def __init__(self, leitura: "LeituraModbus", gravidade: "int"=2, etapas: "list"=[], ug: "UnidadeDeGeracao"=None, descr: "str"=None):

        self.__leitura = leitura
        self.__gravidade = gravidade
        self.__descr = leitura.descr

        self.__ug = ug
        self.__etapas = etapas

    def __str__(self) -> "str":
        return f"Condicionador: {self.descr}, Gravidade: {self.__gravidade}"

    @property
    def leitura(self) -> "float":
        return self.__leitura.valor

    @property
    def gravidade(self) -> 'int':
        return self.__gravidade

    @property
    def descr(self) -> "str":
        return self.__descr

    @property
    def valor(self) -> "float":
        return self.ativo * 1.0

    @property
    def ativo(self) -> "bool":
        if self.__ug:
            return False if self.__ug.etapa_atual in self.__etapas and self.leitura == 0 else True
        else:
            return False if self.leitura == 0 else True


class CondicionadorExponencial(CondicionadorBase):
    def __init__(self, leitura: "LeituraModbus", gravidade: "int"=2, valor_base: "float"=100, valor_limite: "float"=200, ordem: "float"=(1/4), descr: "str"=None):
        super().__init__(leitura, gravidade, descr)

        self.__ordem = ordem
        self.__valor_base = valor_base
        self.__valor_limite = valor_limite

    @property
    def valor_base(self) -> "float":
        return self.__valor_base

    @valor_base.setter
    def valor_base(self, val: "float") -> "None":
        self.__valor_base = val

    @property
    def valor_limite(self) -> "float":
        return self.__valor_limite

    @valor_limite.setter
    def valor_limite(self, val: "float") -> "None":
        self.__valor_limite = val

    @property
    def ativo(self) -> "bool":
        if self.__ug:
            return True if self.__ug.etapa_atual in self.__etapas and self.valor >= 1 else False
        else:
            return True if self.valor >= 1 else False

    @property
    def valor(self) -> "float":
        if self.leitura > self.valor_base and  self.leitura < self.valor_limite:
            aux = (1 - (((self.valor_limite - self.leitura) / (self.valor_limite - self.valor_base)) ** (self.__ordem)).real)
            return max(min(aux, 1), 0)
        else:
            return 1 if self.leitura > self.valor_limite else 0


class CondicionadorPotenciaReativa(CondicionadorBase):
    def __init__(self, leitura: "LeituraModbus", valor_base: "float"=1, valor_limite: "float"=1.05, descr: "str"=None):
        super().__init__(leitura, descr)

        self.__valor_base = valor_base
        self.__valor_limite = valor_limite

    @property
    def valor_base(self) -> "float":
        return self.__valor_base

    @valor_base.setter
    def valor_base(self, val: "float") -> "None":
        self.__valor_base = val

    @property
    def valor_limite(self) -> "float":
        return self.__valor_limite

    @valor_limite.setter
    def valor_limite(self, val: "float") -> "None":
        self.__valor_limite = val

    @property
    def valor(self) -> "float":
        v_temp = float(self.leitura)

        if v_temp < self.valor_base:
            return 0

        # elif self.valor_limite < v_temp < self.valor_base:
        #     aux = (1 - (((self.valor_limite - v_temp) / (self.valor_limite - self.valor_base))** (self.ordem)).real)
        #     return max(min(aux, 1), 0,)

        elif v_temp < self.valor_limite:
            return 1