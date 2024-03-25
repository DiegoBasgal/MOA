
import src.unidade_geracao as u
import src.funcoes.leitura as lei


class CondicionadorBase:
    def __init__(self, leitura: "lei.LeituraModbus", gravidade: "int"=2, etapas: "list"=[], ug_id: "int"=None):

        # PRIVADAS
        self.__leitura = leitura
        self.__gravidade = gravidade
        self.__descricao = leitura.descricao

        self.__ug_id = ug_id
        self.__etapas = etapas

        self.__ugs = []


    def __str__(self) -> "str":
        """
        Função que retorna string com detalhes do condicionador para logger.
        """

        return f"Condicionador {self.__descricao}, Gravidade: {self.__gravidade}"

    @property
    def leitura(self) -> "float":
        # PROPRIEDADE -> Retrona o valor crú de leitura do condicionador.
        return self.__leitura.valor

    @property
    def gravidade(self) -> "int":
        # PROPRIEDADE -> Retrona a gravidade do condicionador.
        return self.__gravidade

    @property
    def descricao(self) -> "str":
        # PROPRIEDADE -> Retrona a descrição do condicionador.
        return self.__descricao

    @property
    def valor(self) -> "float":
        # PROPRIEDADE -> Retrona o valor tratado de leitura do condicionador.
        return self.ativo * 1.0

    @property
    def ativo(self) -> "bool":
        # PROPRIEDADE -> Retrona se o condicionaor está ativo.
        if self.__ug_id and self.__etapas:
            for ug in self.ugs:
                if ug.id == self.__ug_id and ug.etapa_atual in self.__etapas:
                    return False if self.leitura == 0 else True
            else:
                return False
        else:
            return False if self.leitura == 0 else True

    @property
    def ugs(self) -> "list[u.UnidadeGeracao]":
        return self.__ugs

    @ugs.setter
    def ugs(self, var: "list[u.UnidadeGeracao]") -> "None":
        self.__ugs = var


class CondicionadorExponencial(CondicionadorBase):
    def __init__(self, leitura: "lei.LeituraModbus", gravidade: "int"=2, valor_base: "float"=100, valor_limite: "float"=200, ordem: "float"=(1/4)):
        super().__init__(leitura, gravidade)

        # PRIVADAS
        self.__ordem = ordem
        self.__valor_base = valor_base
        self.__valor_limite = valor_limite


    @property
    def valor_base(self) -> "float":
        # PROPRIEDADE -> Retrona o valor base do condicionador.
        return self.__valor_base

    @valor_base.setter
    def valor_base(self, var) -> "None":
        # SETTER -> Atribui o novo valor base do condicionador.
        self.__valor_base = var

    @property
    def valor_limite(self) -> "float":
        # PROPRIEDADE -> Retrona o valor limite do condicionador.
        return self.__valor_limite

    @valor_limite.setter
    def valor_limite(self, var) -> "None":
        # SETTER -> Atribui o novo valor limite do condicionador.
        self.__valor_limite = var

    @property
    def ordem(self) -> "float":
        # PROPRIEDADE -> Retrona a ordem do condicionador.
        return self.__ordem

    @ordem.setter
    def ordem(self, var) -> "None":
        # SETTER -> Atribui o novo valor de ordem do condicionador.
        self.__ordem = var

    @property
    def ativo(self) -> "bool":
        # PROPRIEDADE -> Retrona se o condicionador está ativo.
        return True if self.valor >= 1 else False

    @property
    def valor(self) -> "float":
        # PROPRIEDADE -> Retrona o valor do condicionador.
        v_temp = float(self.leitura)

        if v_temp > self.valor_base and  v_temp < self.valor_limite:
            aux = (1 - (((self.valor_limite - v_temp) / (self.valor_limite - self.valor_base)) ** (self.ordem)).real)
            return max(min(aux, 1), 0)
        else:
            return 1 if self.leitura > self.valor_limite else 0


class CondicionadorExponencialReverso(CondicionadorBase):
    def __init__(self, leitura: "lei.LeituraBase", gravidade: "int"=2, valor_base: "float"=16.5, valor_limite: "float"=14, ordem: "float"=2, descricao: "str"=None):
        super().__init__(leitura, gravidade, descricao)

        # PRIVADAS
        self.__ordem = ordem
        self.__valor_base = valor_base
        self.__valor_limite = valor_limite


    @property
    def valor_base(self) -> "float":
        # PROPRIEDADE -> Retrona o valor base do condicionador.
        return self.__valor_base

    @valor_base.setter
    def valor_base(self, var) -> "None":
        # SETTER -> Atribui o novo valor base do condicionador.
        self.__valor_base = var

    @property
    def valor_limite(self) -> "float":
        # PROPRIEDADE -> Retrona o valor limite do condicionador.
        return self.__valor_limite

    @valor_limite.setter
    def valor_limite(self, var) -> "None":
        # SETTER -> Atribui o novo valor limite do condicionador.
        self.__valor_limite = var

    @property
    def ordem(self) -> "float":
        # PROPRIEDADE -> Retrona a ordem do condicionador.
        return self.__ordem

    @ordem.setter
    def ordem(self, var) -> "None":
        # SETTER -> Atribui o novo valor de ordem do condicionador.
        self.__ordem = var

    @property
    def valor(self) -> float:
        # PROPRIEDADE -> Retrona o valor do condicionador.
        v_temp = float(self.leitura)

        if v_temp < 1:
            return 0

        elif self.valor_limite < v_temp < self.valor_base:
            aux = (1 - (((self.valor_limite - v_temp) / (self.valor_limite - self.valor_base))** (self.ordem)).real)
            return max(min(aux, 1), 0)
        else:
            return 1 if v_temp <= self.valor_limite else 0
