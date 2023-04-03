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
    dados = arquivo = os.path.join(os.path.dirname(__file__), "dados.json")
    with open(arquivo, "r") as file:
        dados = json.load(file)

    _ultimo_autor: int

    _semaforo = Semaphore(1)

    @property
    def semaforo(cls) -> Semaphore:
        return cls._semaforo._value

    @semaforo.setter
    def semaforo(cls, sinal: int) -> None:
        if sinal == VERDE:
            cls._semaforo.release()
        elif sinal == VERMELHO:
            cls._semaforo.acquire()
        else:
            raise ValueError("[CNV] Sinal inexistente")

    @property
    def ultimo_autor(cls) -> int:
        return cls._ultimo_autor

    @ultimo_autor.setter
    def ultimo_autor(cls, autor: int) -> int:
        if autor in (OPC_DA, OPC_UA):
            cls._ultimo_autor = autor
        else:
            raise ValueError("[CNV] Autor inexistente")

    def registar_mudanca(cls, reg, val, autor, forcar_autoria=False) -> list[str]:
        alterados = []

        if autor != cls.ultimo_autor or forcar_autoria:
            forcar_autoria = False

            for n in cls.dados:
                if cls.dados == reg and cls.dados[n] != val:
                    cls.dados[n] = val
                    logger.info(f"[CNV][JSN] Dado: {cls.dados[n]}, alterado. Valor: {cls.dados[n]}, Autor: {AUTOR_STR_DCT[autor]}")
                    alterados.append(cls.dados[n])

            cls.ultimo_autor = autor
            return alterados
        else:
            logger.debug(f"[CNV] Não foi possível registrar a mudança pois autor atual ({AUTOR_STR_DCT[autor]}) é o mesmo que o último.")
            return alterados


class ExternoParaNativo(Conversor):
    def __init__(cls, dados, opc_da: OpcDa=None) -> None:
        super().__init__(dados)
        if opc_da is None:
            logger.warning("[CNV][OPC] Não foi possível iniciar o cliente OPC DA. Encerrando conversor...")
            sys.exit(1)
        else: 
            cls.opc_da = opc_da

        cls._valores_antigos = []

    @property
    def valores_antigos(cls) -> list[tuple[str, bool]]:
        return cls._valores_antigos

    @valores_antigos.setter
    def valores_antigos(cls, tupla: tuple[str, bool]) -> None:
        if [tuplas[0] for tuplas in cls.valores_antigos].index(tupla[0]):
            cls._valores_antigos.remove(tupla)
        cls._valores_antigos.append(tupla)

    def carregar_dados_iniciais(cls) -> None:
        logger.debug("[CNV][OPC] Carregando dados inciais...")
        for nome, reg in TESTE.items():
            leitura = bool(cls.opc_da.read(TESTE[reg], group='Group0')[0])
            cls.valores_antigos = [nome, leitura]
            logger.debug(f"[CNV][OPC] Dado: {nome} -> Valor: {leitura}, carregado.")
        logger.debug(cls.valores_antigos)

    def detectar_mudanca(cls) -> list[str]:
        valores = []
        flag_forcar = 0

        for reg in TESTE:
            leitura = bool(cls.opc_da.read(TESTE[reg], group='Group0')[0])

            for nome, valor in cls.valores_antigos:
                if nome == reg and valor != leitura:
                    logger.debug("[CNV][OPC] Mudança na leitura detectada! Verificando autor do último registro.")

                    if cls.ultimo_autor == OPC_DA:
                        logger.debug("[CNV][OPC] Mesmo autor da última mudança (\"OPC_DA\"). Forçando autoria.")
                        cls.valores_antigos[nome] = leitura
                        valores.append([cls.valores_antigos[nome], leitura])
                    elif cls.ultimo_autor == OPC_UA:

            else:
                logger.debug("[CNV][OPC] Nenhuma mudança...")

        return valores if valores is not None else []


class NativoParaExterno(Conversor):
    def __init__(cls, dados) -> None:
        super().__init__(dados)

        cls._valores_antigos = []

    @property
    def valores_antigos(cls) -> list[tuple[str, bool]]:
        return cls._valores_antigos

    @valores_antigos.setter
    def valores_antigos(cls, tupla: tuple[str, bool]) -> None:
        if [tuplas[0] for tuplas in cls.valores_antigos].index(tupla[0]):
            cls._valores_antigos.remove(tupla)
        cls._valores_antigos.append(tupla)

    def copiar_dados_inciais(cls) -> None:
        for nome, valor in cls.dados.items():
            cls.valores_antigos = [nome, valor]
            logger.debug(f"[CNV][MOA] Dado: {nome} -> Valor: {valor}, copiado.")
        logger.debug(cls.valores_antigos)

    def detectar_mudanca(cls) -> list[str]:
        valores = []
        flag_forcar = 0

        for n1, v1 in cls.dados.items():
            for n2, v2 in cls.valores_antigos:
                if n1 == n2 and v1 != v2:
                    logger.debug("[CNV][MOA] Mudança na leitura detectada! Verificando autor do último registro.")

                    if cls.ultimo_autor == OPC_UA:
                        logger.debug("[CNV][MOA] Mesmo autor da última mudança (\"OPC_UA\"). Forçando autoria.")
                        cls.valores_antigos[n2] = leitura
                        valores.append([cls.valores_antigos[nome], leitura])
            else:
                logger.debug("[CNV][MOA] Nenhuma mudança...")

        return valores if valores is not None else []