import sys
import logging
import OpenOPC
import traceback

from reg import BAY, TESTE

logger = logging.getLogger("__main__")

class ConversorOpc:
    def __init__(self, opc=None, dados: dict=None) -> None:
        if not dados or not opc:
            logger.warning("Não foi possível iniciar os argumentos da classe. Encerrando conversor...")
            logger.debug(f"Tracebak: {traceback.print_stack}")
        else:
            self.dados = dados
            self.opc: OpenOPC.client = opc
        
        self._antigo = {}
        self.carregar_dados_iniciais()

    @property
    def antigo(self) -> dict[str, bool]:
        return self._antigo
   
    @antigo.setter
    def antigo(self, val:  dict[str, bool]) -> None:
        self._antigo = val

    def detectar_mudanca(self) -> list:
        valores = []
        try:
            for (n1, r), (n2, v) in zip(TESTE.items(), self.antigo.items()):
                leitura = self.opc.read(TESTE[r], group='Group0')[0]
                if TESTE == self.antigo and self.antigo[v2] != leitura:
                    logger.debug("Mudança detectada!")
                    logger.debug(f"Leitura -> TESTE: {TESTE[k1]}, Valor: {self.antigo[v2]} -> {leitura}")
                    self.antigo[v2] = leitura
                    key = self.registar_mudanca(self.antigo[k2], self.antigo[v2])
                    valores.append(key)
                else:
                    logger.debug("Nenhuma mudança...")

            return valores if valores is not None else []

        except Exception:
            logger.exception(f"Erro ao detectar mudanças. Traceback: {traceback.print_stack}")
            return []

    def registar_mudanca(self, reg, val) -> str:
        for n, v in self.dados.items():
            if self.dados == reg and self.dados[n] != val:
                self.dados[n] = val
                logger.info(f"[JSON] Dado: {self.dados[n]}, alterado. Valor: {self.dados[n]}")
                return self.dados[n]

    def carregar_dados_iniciais(self) -> None:
        logger.debug("Carregando dados inciais...")
        for n, r in TESTE.items():
            self.antigo = n
            self.antigo[n] = self.opc.read(TESTE[r], group='Group0')[0]
            logger.debug(f"Dado: {self.antigo} -> Valor: {self.antigo[n]}, carregado.")