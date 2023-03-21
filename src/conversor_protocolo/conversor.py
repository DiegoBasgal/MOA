import sys
import logging
import traceback

from opcua import Client as OpcUa
from OpenOPC import client as OpcDa

from reg import BAY, TESTE

logger = logging.getLogger("__main__")

class Conversor:
    def __init__(self, opc_da: OpcDa=None, opc_ua: OpcUa=None, dados: dict=None) -> None:
        if None in (opc_da, opc_ua, dados):
            logger.warning("Não foi possível iniciar os argumentos da classe. Encerrando conversor...")
            sys.exit(1)
        else:
            self.dados = dados
            self.opc_da = opc_da
            self.opc_ua = opc_ua

            SINAL_UA = 2
            SINAL_DA = 1
            SINAL_LIVRE = 0

            self._sinalizar: int[0| 1 | 2] = 0

        DAparaUA.carregar_dados_iniciais()

    @property
    def sinalizar(self) -> int:
        return self._sinalizar

    @sinalizar.setter
    def sinalizar(self, val: int[0 | 1 | 2]) -> None:
        self._sinalizar = val


    def registar_mudanca(self, reg, val) -> list[str]:
        for n, v in self.dados.items():
            if self.dados == reg and self.dados[n] != val:
                self.dados[n] = val
                logger.info(f"[JSON] Dado: {self.dados[n]}, alterado. Valor: {self.dados[n]}")
                return self.dados[n]


class DAparaUA(Conversor):
    def __init__(self, opc_da=None, dados: dict=None) -> None:
        super().__init__(opc_da, dados)

        self._valores_antigos = []

    @property
    def valores_antigos(self) -> list[str, bool]:
        return self._valores_antigos

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
            if TESTE == self.valores_antigos and self.valores_antigos[v2] != leitura:
                logger.debug("Mudança detectada!")
                logger.debug(f"Leitura -> TESTE: {TESTE[k1]}, Valor: {self.valores_antigos[v2]} -> {leitura}")
                self.valores_antigos[v2] = leitura
                key = self.registar_mudanca(self.valores_antigos[k2], self.valores_antigos[v2])
                valores.append(key)
            else:
                logger.debug("Nenhuma mudança...")

        return valores if valores is not None else []


class UAparaDA(Conversor):
    def __init__(self, opc_ua=None, dados: dict=None) -> None:
        super().__init__(opc_ua, dados)