__author__ = "Diego Basgal"
__credits__ = "Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal"

__version__ = "0.1"
__status__ = "Development"
__maintainer__ = "Diego Basgal"
__email__ = "diego.garcia@ritmoenergia.com.br"
__description__ = "Este módulo corresponde a implementação do conversor de protocolos."

import sys
import logging
import traceback

from threading import Semaphore

from OpenOPC import client as OpcDa

from dicionarios.reg import *
from dicionarios.const import *

logger = logging.getLogger("__main__")

class Conversor:
    def __init__(self, dados: dict[str, bool]=None) -> None:
        if None in (dados):
            logger.warning("[CNV] Não foi possível carregar o arquivo de Dados \".json\". Encerrando conversor...")
            sys.exit(1)
        else:
            self.dados = dados

            self._ultimo_autor: int

            self._semaforo = Semaphore(1)

    @property
    def semaforo(self) -> Semaphore:
        return self._semaforo._value

    @semaforo.setter
    def semaforo(self, sinal: int) -> None:
        if sinal == VERDE:
            self._semaforo.release()
        elif sinal == VERMELHO:
            self._semaforo.acquire()
        else:
            raise ValueError("[CNV] Sinal inexistente")

    @property
    def ultimo_autor(self) -> int:
        return self._ultimo_autor

    @ultimo_autor.setter
    def ultimo_autor(self, autor: int) -> int:
        if autor in (OPC_DA, OPC_UA):
            self._ultimo_autor = autor
        else:
            raise ValueError("[CNV] Autor inexistente")

    def registar_mudanca(self, reg, val, autor, forcar_autoria=False) -> list[str]:
        alterados = []

        if autor != self.ultimo_autor or forcar_autoria:
            forcar_autoria = False

            for n in self.dados:
                if self.dados == reg and self.dados[n] != val:
                    self.dados[n] = val
                    logger.info(f"[CNV][JSN] Dado: {self.dados[n]}, alterado. Valor: {self.dados[n]}, Autor: {AUTOR_STR_DCT[autor]}")
                    alterados.append(self.dados[n])

            self.ultimo_autor = autor
            return alterados
        else:
            logger.debug(f"[CNV] Não foi possível registrar a mudança pois autor atual ({AUTOR_STR_DCT[autor]}) é o mesmo que o último.")
            return alterados


class ExternoParaNativo(Conversor):
    def __init__(self, dados, opc_da: OpcDa=None) -> None:
        super().__init__(dados)
        if opc_da is None:
            logger.warning("[CNV][OPC] Não foi possível iniciar o cliente OPC DA. Encerrando conversor...")
            sys.exit(1)
        else: 
            self.opc_da = opc_da

        self._valores_antigos = []

    @property
    def valores_antigos(self) -> list[tuple[str, bool]]:
        return self._valores_antigos

    @valores_antigos.setter
    def valores_antigos(self, tupla: tuple[str, bool]) -> None:
        if [tuplas[0] for tuplas in self.valores_antigos].index(tupla[0]):
            self._valores_antigos.remove(tupla)
        self._valores_antigos.append(tupla)

    def carregar_dados_iniciais(self) -> None:
        logger.debug("[CNV][OPC] Carregando dados inciais...")
        for nome, reg in TESTE.items():
            leitura = bool(self.opc_da.read(TESTE[reg], group='Group0')[0])
            self.valores_antigos = [nome, leitura]
            logger.debug(f"[CNV][OPC] Dado: {nome} -> Valor: {leitura}, carregado.")
        logger.debug(self.valores_antigos)

    def detectar_mudanca(self) -> list[str]:
        valores = []
        flag_forcar = 0

        for reg in TESTE:
            leitura = bool(self.opc_da.read(TESTE[reg], group='Group0')[0])

            for nome, valor in self.valores_antigos:
                if nome == reg and valor != leitura:
                    logger.debug("[CNV][OPC] Mudança na leitura detectada! Verificando autor do último registro.")

                    if self.ultimo_autor == OPC_DA:
                        logger.debug("[CNV][OPC] Mesmo autor da última mudança (\"OPC_DA\"). Forçando autoria.")
                        self.valores_antigos[nome] = leitura
                        valores.append([self.valores_antigos[nome], leitura])
                    elif self.ultimo_autor == OPC_UA:

            else:
                logger.debug("[CNV][OPC] Nenhuma mudança...")

        return valores if valores is not None else []


class NativoParaExterno(Conversor):
    def __init__(self, dados) -> None:
        super().__init__(dados)

        self._valores_antigos = []

    @property
    def valores_antigos(self) -> list[tuple[str, bool]]:
        return self._valores_antigos

    @valores_antigos.setter
    def valores_antigos(self, tupla: tuple[str, bool]) -> None:
        if [tuplas[0] for tuplas in self.valores_antigos].index(tupla[0]):
            self._valores_antigos.remove(tupla)
        self._valores_antigos.append(tupla)

    def copiar_dados_inciais(self) -> None:
        for nome, valor in self.dados.items():
            self.valores_antigos = [nome, valor]
            logger.debug(f"[CNV][MOA] Dado: {nome} -> Valor: {valor}, copiado.")
        logger.debug(self.valores_antigos)

    def detectar_mudanca(self) -> list[str]:
        valores = []
        flag_forcar = 0

        for n1, v1 in self.dados.items():
            for n2, v2 in self.valores_antigos:
                if n1 == n2 and v1 != v2:
                    logger.debug("[CNV][MOA] Mudança na leitura detectada! Verificando autor do último registro.")

                    if self.ultimo_autor == OPC_UA:
                        logger.debug("[CNV][MOA] Mesmo autor da última mudança (\"OPC_UA\"). Forçando autoria.")
                        self.valores_antigos[n2] = leitura
                        valores.append([self.valores_antigos[nome], leitura])
            else:
                logger.debug("[CNV][MOA] Nenhuma mudança...")

        return valores if valores is not None else []