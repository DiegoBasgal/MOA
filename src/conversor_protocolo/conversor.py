import sys
import logging
import traceback

from threading import Semaphore

from OpenOPC import client as OpcDa

from reg import BAY, TESTE

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

            self.forcar_autoria: bool = False


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

    def registar_mudanca(self, reg, val, autor) -> list[str]:
        alterados = []

        if autor != self.ultimo_autor or self.forcar_autoria:
            self.forcar_autoria = False
            if self.semaforo == VERDE:
                self.semaforo = VERMELHO

                for n in self.dados:
                    if self.dados == reg and self.dados[n] != val:
                        self.dados[n] = val
                        logger.info(f"[CNV][JSON] Dado: {self.dados[n]}, alterado. Valor: {self.dados[n]}, Autor: {AUTOR_STR_DCT[autor]}")
                        alterados.append(self.dados[n])

                self.ultimo_autor = autor
                self.semaforo = VERDE

            else:
                logger.debug(f"[CNV] O método de escrita está sendo utilizado pelo \"{AUTOR_STR_DCT[OPC_DA] if autor == OPC_UA else AUTOR_STR_DCT[OPC_UA]}\".")
                logger.debug(f"[CNV] Aguardando para escrever...")
                return self
        else:
            logger.debug(f"[CNV] Não foi possível registrar a mudança pois autor atual ({AUTOR_STR_DCT[autor]}) é o mesmo que o último.")
            return []



class ExternoParaNativo(Conversor):
    def __init__(self, dados, opc_da: OpcDa=None) -> None:
        super().__init__(dados)
        if opc_da is None:
            logger.warning("Não foi possível iniciar o cliente OPC DA. Encerrando conversor...")
            sys.exit(1)
        else: 
            self.opc_da = opc_da

        self._valores_antigos = []

    @property
    def valores_antigos(self) -> list[str, bool]:
        return self._valores_antigos

    @valores_antigos.setter
    def valores_antigos(self, val: list[str, bool]) -> None:
        self._valores_antigos = val

    def carregar_dados_iniciais(self) -> None:
        logger.debug("Carregando dados inciais...")
        for n, r in TESTE.items():
            self.valores_antigos = n
            self.valores_antigos[n] = self.opc_da.read(TESTE[r], group='Group0')[0]
            logger.debug(f"Dado: {self.valores_antigos} -> Valor: {self.valores_antigos[n]}, carregado.")

    def detectar_mudanca(self) -> list[str]:
        valores = []
        for (n1, r), (n2, v) in zip(TESTE.items(), self.valores_antigos.items()):
            leitura = self.opc_da.read(TESTE[r], group='Group0')[0]
            if TESTE == self.valores_antigos and self.valores_antigos[v] != leitura:
                logger.debug("Mudança detectada!")
                logger.debug(f"Leitura -> TESTE: {TESTE[n1]}, Valor: {self.valores_antigos[v]} -> {leitura}")
                self.valores_antigos[v] = leitura
                key = self.registar_mudanca(self.valores_antigos[n2], self.valores_antigos[v])
                valores.append(key)
            else:
                logger.debug("Nenhuma mudança...")

        return valores if valores is not None else []


class NativoParaExterno(Conversor):
    def __init__(self, dados) -> None:
        super().__init__(dados)

        self._valores_antigos = []

    @property
    def valores_antigos(self) -> list[str, bool]:
        return self._valores_antigos

    @valores_antigos.setter
    def valores_antigos(self, val: list[str, bool]) -> None:
        self._valores_antigos = val