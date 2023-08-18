from leitura import LeituraBase

class LeituraComposta(LeituraBase):
    def __init__(self, leituras: "list[LeituraBase]"=None, descr: "str"=None):
        super().__init__(descr)

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__leituras = leituras

    @property
    def valor(self) -> "float":
        # PROPRIEDADE -> Retorna Valor composto de duas ou mais leituras ModBus.

        res = 0
        count = 0
        for l in self.__leituras:
            if l is not None and l.valor:
                res += 2**count
            count += 1
        return res