from src.Leituras import *

class CondicionadorBase:
    ...

class CondicionadorExponencial(CondicionadorBase):
    ...

class CondicionadorExponencialReverso(CondicionadorBase):
    ...

class CondicionadorBase:
    def __init__(self, descr: str, gravidade: int, leitura: LeituraBase, ug_id: int = None, etapas: list = None):
        self.__descr = descr
        self.__gravidade = gravidade
        self.__leitura = leitura
        self.__ugs = []
        self.__ug_id = ug_id if ug_id is not None else None
        self.__etapas = etapas if etapas is not None else []

    def __str__(self):
        return f"Condicionador {self.__descr}, Gravidade: {self.__gravidade}, Ativo: {self.ativo}, Valor: {self.valor}"

    @property
    def descr(self):
        return self.__descr

    @property
    def leitura(self):
        return self.__leitura

    @property
    def ativo(self) -> bool:
        if self.__ug_id and self.__etapas:
            for ug in self.ugs:
                if ug.id == self.__ug_id and ug.etapa_atual in self.__etapas:
                    return False if self.leitura.valor == 0 else True
            else:
                return False

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
        ug_id: int = None,
        ordem: float = (1 / 4),
        etapas: list = None,
        *args,
        **kwargs
    ):
        super().__init__(descr, gravidade, leitura, *args, **kwargs)
        self.__etapas == etapas if etapas is not None else []
        self.__valor_base = valor_base
        self.__valor_limite = valor_limite
        self.__ordem = ordem
        self.__ug_id = ug_id

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
        return True if self.valor >= 1 else False
    
    @property
    def valor(self) -> float:
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


class CondicionadorExponencialReverso(CondicionadorBase):
    def __init__(
        self,
        descr: str,
        gravidade: int,
        leitura: LeituraBase,
        valor_base: float,
        valor_limite: float,
        ug_id: int = None,
        ordem: float = 2,
        *args,
        **kwargs
    ):
        super().__init__(descr, gravidade, leitura, *args, **kwargs)
        self.__valor_base = valor_base
        self.__valor_limite = valor_limite
        self.__ordem = ordem
        self.__ug_id = ug_id

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
        v_temp = float(self.leitura.valor)
        
        if v_temp < 1:
            return 0
        elif self.valor_limite < v_temp < self.valor_base:
            aux = (1 - (((self.valor_limite - v_temp) / (self.valor_limite - self.valor_base))** (self.ordem)).real)
            return max(min(aux, 1), 0,)

        elif v_temp <= self.valor_limite:
            return 1
        else:
            return 0
