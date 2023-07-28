from pyModbusTCP.server import DataBank

class Leitura:
    def __init__(self, databank: "DataBank"=None) -> "None":

        self.__db = databank

    def ler_bit(self, registrador: "int", bit: "int", invertido: "bool") -> "bool":

        ler = self.__db.get_words(registrador)[0]

        v_bit = ler & 2**bit

        return not v_bit if invertido else v_bit