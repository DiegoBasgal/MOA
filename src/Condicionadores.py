"""
Condicionadores.

Esse módulo corresponde a implementação dos condicionadores (alarmes/limites)
dos valores de campo.
"""
__version__ = "0.1"
__author__ = "Lucas Lavratti"

from src.Leituras import *


class CondicionadorBase:
    ...


class CondicionadorExponencial(CondicionadorBase):
    ...


class CondicionadorBase:
    """
    Classe implementa a base para condicionadores. É "Abstrata" assim por se dizer...
    """

    def __init__(self, descr: str, gravidade: int, leitura: LeituraBase):
        self.__descr = descr
        self.__gravidade = gravidade
        self.__leitura = leitura

    def __str__(self):
        return "Condicionador {}, Gravidade: {}, Ativo: {}, Valor: {}".format(
            self.__descr, self.__gravidade, self.ativo, self.valor
        )

    @property
    def descr(self):
        return self.__descr

    @property
    def leitura(self):
        return self.__leitura

    @property
    def ativo(self) -> bool:
        """
        Retorna se o condicionador está ativo ou não.
        Por padrão retorna ativo para qualquer valor diferente de 0.

        Returns:
            bool: True se ativo, False caso contrário
        """
        return False if self.__leitura.valor == 0 else True

    @property
    def valor(self) -> float:
        """
        Valor normalizado, entre 0 e 1 de quão "Ativo" está o condicionador.
        Por padrão retorna o mesmo que o booleano ativo, mas numéricamente.

        Returns:
            float: valor normalizado
        """
        return self.ativo * 1.0

    @property
    def gravidade(self) -> int:
        """
        Gravidade do condicionador

        DEVE_INDISPONIBILIZAR = 2
        DEVE_NORMALIZAR = 1
        DEVE_IGNORAR = 0

        Returns:
            int: gravidade
        """
        return self.__gravidade


class CondicionadorExponencial(CondicionadorBase):
    """
    Implementação básica de limtes operacionais contínuos segundo curva exponencial de decaimento
    """

    def __init__(
        self,
        descr: str,
        gravidade: int,
        leitura: LeituraBase,
        valor_base: float,
        valor_limite: float,
        ordem: float = (1 / 4),
    ):
        super().__init__(descr, gravidade, leitura)
        self.__valor_base = valor_base
        self.__valor_limite = valor_limite
        self.__ordem = ordem

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
        """
        Retorna se o condicionador está ativo ou não.

        Returns:
            bool: True se atenuação >= 100%, False caso contrário
        """
        return True if self.valor >= 1 else False

    @property
    def valor(self) -> float:
        """
        Valor relativo a quantidade de atenuação

        Returns:
            float: Valor de 0 a 1 (inclusivo) relativo a atenuacao após limitação operacional
        """
        v_temp = float(self.leitura.valor)
        if v_temp > self.valor_base and  v_temp < self.valor_limite:
            aux = (
                1
                - (
                    (
                        (self.valor_limite - v_temp)
                        / (self.valor_limite - self.valor_base)
                    )
                    ** (self.ordem)
                ).real
            )
            return max(
                min(aux, 1),
                0,
            )
        if self.leitura.valor > self.valor_limite:
            return 1
        else:
            return 0
