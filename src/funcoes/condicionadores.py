import src.unidade_geracao as ug
import src.funcoes.leitura as lei

from src.dicionarios.const import *

class CondicionadorBase:
    def __init__(self, leitura: "lei.LeituraModbus", gravidade: "int"=CONDIC_NORMALIZAR, etapas: "list"=[], ug: "ug.UnidadeDeGeracao"=None, teste: "bool"=False):

        self.__leitura = leitura
        self.__gravidade = gravidade
        self.__descricao = leitura.descricao

        self.__ug = ug
        self.__etapas = etapas

        self.__teste = teste


    def __str__(self) -> "str":
        return f"Condicionador: {self.descricao}, Gravidade: {CONDIC_STR_DCT[self.gravidade]}"

    @property
    def leitura(self) -> "float":
        return self.__leitura.valor

    @property
    def gravidade(self) -> "int":
        return self.__gravidade

    @property
    def descricao(self) -> "str":
        return self.__descricao

    @property
    def valor(self) -> "float":
        return self.ativo * 1.0

    @property
    def ativo(self) -> "bool":
        if self.__ug and self.__etapas:
            if self.__ug.etapa_atual in self.__etapas:
                return False if self.leitura == 0 else True
            else:
                return False
        else:
            return False if self.leitura == 0 else True

    @property
    def teste(self) -> "bool":
        # PROPRIEDADE -> Retorna se o Condicionador está com a Flag de Teste

        return self.__teste



class CondicionadorExponencial(CondicionadorBase):
    def __init__(self, leitura: "lei.LeituraModbus", gravidade: "int"=CONDIC_NORMALIZAR, valor_base: "float"=100, valor_limite: "float"=200, ordem: "float"=(1/4), teste: "bool"=False):
        super().__init__(leitura, gravidade, teste)

        self.__ordem = ordem
        self.__valor_base = valor_base
        self.__valor_limite = valor_limite
        self.__descricao = leitura.descricao

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
    def ordem(self) -> "float":
        return self.__ordem

    @ordem.setter
    def ordem(self, val: "float") -> "None":
        self.__ordem = val

    @property
    def ativo(self) -> "bool":
        return True if self.valor >= 1 else False

    @property
    def valor(self) -> "float":
        if self.leitura > self.valor_base and self.leitura < self.valor_limite:
            aux = (1 - (((self.valor_limite - self.leitura) / (self.valor_limite - self.valor_base)) ** (self.__ordem)).real)
            return max(min(aux, 1), 0)
        else:
            return 1 if self.leitura >= self.valor_limite else 0


class CondicionadorPotenciaReativa(CondicionadorBase):
    def __init__(self, leitura: "lei.LeituraModbus", valor_base: "float"=1, valor_limite: "float"=1.05, teste: "bool"=False):
        super().__init__(leitura, teste)

        self.__valor_base = valor_base
        self.__valor_limite = valor_limite
        self.__descricao = leitura.descricao

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