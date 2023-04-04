__author__ = "Diego Basgal"
__credits__ = "Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal"

__version__ = "0.1"
__status__ = "Development"
__maintainer__ = "Diego Basgal"
__email__ = "diego.garcia@ritmoenergia.com.br"
__description__ = "Este módulo corresponde a implementação do conversor de protocolos."

import os
import sys
import json
import logging
import traceback

from threading import Semaphore

from OpenOPC import client as OpcDa

from dicionarios.reg import *
from dicionarios.const import *

logger = logging.getLogger("__main__")

class Conversor:
    def __init__(self, dados: dict[str, bool] | None = ...) -> None:
        if not dados:
            logger.warning("[CNV] Não foi possível carregar o arquivo de Dados \".json\". Encerrando conversor...")
            sys.exit(1)
        else:
            self.dados = dados

        self._ultimo_autor: int
        self._valores_antigos: dict[str, bool] = {}

        self._semaforo = Semaphore(1)

    @property
    def semaforo(self) -> Semaphore:
        return self._semaforo._value

    @semaforo.setter
    def semaforo(self, sinal: int) -> None:
        if sinal == VERDE:
            self.semaforo.release()
        elif sinal == VERMELHO:
            self.semaforo.acquire()

    @property
    def ultimo_autor(self) -> int:
        return self._ultimo_autor

    @ultimo_autor.setter
    def ultimo_autor(self, autor: int) -> int:
        if autor in (OPC_DA, OPC_UA):
            self._ultimo_autor = autor

    @property
    def valores_antigos(self, nome) -> dict[str, bool]:
        return self._valores_antigos[nome]

    @valores_antigos.setter
    def valores_antigos(self, nome: str, valor: bool) -> None:
        if nome not in self._valores_antigos.keys():
            raise ValueError("[CNV] ")
        else:
            self._valores_antigos[nome] = valor


    

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










class ExternoNativo(Conversor):
    def __init__(self, dados) -> None:
        super().__init__(dados)

        self._opc_da: OpcDa

    @property
    def opc_da(self) -> OpcDa:
        return self._opc_da

    @opc_da.setter
    def opc_da(self, client: OpcDa) -> None:
        self._opc_da = client


    def carregar_dados_iniciais(self) -> None:
        logger.debug("[CNV][OPC] Carregando dados inciais...")

        for nome, reg in TESTE.items():
            leitura = bool(self.opc_da.read(reg, group='Group0')[0])
            self.dados[nome] = leitura
            self.valores_antigos[nome] = leitura
            logger.debug(f"[CNV][OPC] Dado: {nome} -> Valor: {leitura}, carregado.")

        with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'w') as file:
            json.dump(self.dados, file)

        self.ultimo_autor = OPC_DA

    def detectar_mudanca(self) -> bool:
        for (n1, reg), (n2, valor) in zip(TESTE.items(), self.valores_antigos.items()):
            ler = bool(self.opc_da.read(reg, group='Group0')[0])

            if n1 == n2 and ler != valor:
                logger.info()

















class NativoExterno(Conversor):
    def __init__(self, dados) -> None:
        super().__init__(dados)
