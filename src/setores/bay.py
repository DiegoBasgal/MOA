__version__ = "0.1"
__author__ = "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da operação do Bay."

import logging

from conversor.conversor import NativoParaExterno

logger = logging.getLogger("__main__")

class Bay:
    def __init__(
            self,
            conversor: NativoParaExterno | None = ...
        ) -> ...:

        if None in (conversor):
            logger.warning("[BAY] Erro ao carregar argumentos da classe \"ConectorBay\".")
            raise ImportError
        else:
            self.cnv = conversor

    def verificar_status_DJs(self) -> bool:
        return

    def resetar_emergencia(self) -> bool:
        return

    def verificar_tensao_trifasica(self) -> bool:
        return