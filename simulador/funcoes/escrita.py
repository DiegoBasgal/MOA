from pyModbusTCP.server import DataBank

class Escrita:
    def __init__(self, databank: "DataBank"=None) -> "None":

        self.__db = databank

    def escrever_bit(self, registrador: "int", bit: "int", valor: "int", invertido: "bool") -> "None":

        ler = self.__db.get_words(registrador)[0]
        bin = [int(x) for x in list('{0:0b}'.format(ler))]

        for i in range(len(bin)):
            if bit == i:
                bin[i] = valor
                break

        if invertido:
            v = sum(val*(2**x) for x, val in enumerate(bin))
        else:
            v = sum(val*(2**x) for x, val in enumerate(reversed(bin)))

        self.__db.set_words(registrador, [v])