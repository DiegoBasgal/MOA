__version__ = "0.1"
__author__ = "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da operação do Bay."

from Usina import *

logger = logging.getLogger("__main__")

class Bay(Usina):
    def __init__(self) -> ...:
        super(Usina, self).__init__(self)


    def verificar_status_DJs(self) -> bool:
        return

    def resetar_emergencia(self) -> bool:
        return

    def verificar_tensao_trifasica(self) -> bool:
        return