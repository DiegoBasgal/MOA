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
        
        self._antigo: dict[str, bool] = {}
        self.carregar_dados_iniciais()

    @property
    def antigo(self) -> dict:
        return self._antigo
   
    @antigo.setter
    def antigo(self, val:  dict) -> None:
        self._antigo = val

    def detectar_mudanca(self) -> list:
        valores = []
        try:
            for (k1, r), (k2, v2) in zip(TESTE.items(), self.antigo.items()):
                leitura = self.opc.read(TESTE[k1], group=0)
                if TESTE[k1] == self.antigo[k2] and self.antigo[v2] != leitura:
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
        for key, val in self.dados.items():
            if self.dados[key] == reg and self.dados[val] != val:
                self.dados[val] = val
                logger.info(f"[JSON] Dado: {self.dados[key]}, alterado. Valor: {self.dados[val]}")
                return self.dados[key]

    def carregar_dados_iniciais(self) -> None:
        logger.debug("Carregando dados inciais...")
        for k, v in zip(TESTE.items(), self.antigo.items()):
            logger.debug("entrei")
            self.antigo[k] = TESTE[k]
            self.antigo[k][0] = self.opc.read(TESTE[k], group=0)
            logger.debug(f"Dado: {self.antigo[k]} -> Valor: {self.antigo[k][v]}, carregado.")