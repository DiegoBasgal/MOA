__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__description__ = "Este módulo corresponde a implementação da operação das Comportas da Tomada da Água."

import logging
import traceback

from time import time

from funcoes.leitura import *
from dicionarios.const import *

from tomada_agua import TomadaAgua
from funcoes.escrita import EscritaModBusBit as EMB

logger = logging.getLogger("logger")

class Comporta(TomadaAgua):
    def __init__(self, id: "int"=None) -> "None":

        # VERIFICAÇÃO DE ARGUMENTOS

        if not id or id < 1:
            raise ValueError(f"[CP{self.id}] A Comporta deve ser instanciada com um valor maior que \"0\".")
        else:
            self.__id = id

        # ATRIBUIÇÃO DE VAIRÁVEIS
        # PRIVADAS
        self.__aberta = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_ABERTA"],
            bit=17
        )
        self.__fechada = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_FECHADA"],
            bit=18
        )
        self.__cracking = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_CRACKING"],
            bit=25
        )
        self.__remoto = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_REMOTO"],
            bit=22
        )
        self.__operando = LeituraModbus(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_COMPORTA_OPERANDO"],
            bit=14
        )
        self.__permissao = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_PERMISSIVOS_OK"],
            bit=31,
            invertido=True
        )
        self.__bloqueio = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_BLOQUEIO_ATUADO"],
            bit=31,
            invertido=True
        )

        # PÚBLICAS
        self.pressao_equalizada = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_PRESSAO_EQUALIZADA"],
            bit=4
        )
        self.aguardando_cmd_abertura = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_AGUARDANDO_COMANDO_ABERTURA"],
            bit=3
        )

    @property
    def id(self) -> "int":
        return self.__id

    @property
    def operando(self) -> "bool":
        return self.__operando.valor

    @property
    def bloqueio(self) -> "bool":
        return self.__bloqueio.valor

    @property
    def permissao(self) -> "bool":
        return self.__permissao.valor

    @property
    def etapa(self) -> "int":
        try:
            if self.__fechada.valor:
                return CP_FECHADA
            elif self.__aberta.valor:
                return CP_ABERTA
            elif self.__cracking.valor:
                return CP_CRACKING
            elif self.__remoto.valor:
                return CP_REMOTO
            else:
                logger.debug(f"[CP{self.id}] Comporta em Etapa inconsistente.")
                return 99

        except Exception:
            logger.error(f"[TDA][CP{self.id}] Houve um erro ao verificar a Etapa da Comporta.")
            return 99

    @property
    def comporta_adjacente(self) -> "Comporta":
        return self._comporta_adjacente

    @comporta_adjacente.setter
    def comporta_adjacente(self, var: "Comporta"):
        self._comporta_adjacente = var

    def resetar_emergencia(self) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = EMB.escrever_bit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CMD_REARME_FALHAS"], bit=0, valor=1)
            return res

        except Exception:
            logger.error(f"[TDA][CP{self.id}] Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def rearme_falhas(self) -> "bool":
        try:
            res = EMB.escrever_bit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CMD_REARME_FALHAS"], bit=0, valor=1)
            return res

        except Exception:
            logger.error(f"[TDA][CP{self.id}] Houve um erro ao realizar o Rearme de Falhas da Comporta.")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def abrir(self) -> "None":
        try:
            if self.etapa == CP_ABERTA:
                logger.debug(f"[TDA][CP{self.id}] A comporta {self.id} já está aberta")

            elif self.verificar_condicoes():
                if self.pressao_equalizada.valor and self.aguardando_cmd_abertura.valor:
                    logger.debug(f"[TDA][CP{self.id}] Enviando comando de abertura para a comporta {self.id}")

                    EMB.escrever_bit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CMD_ABERTURA_TOTAL"], bit=2, valor=1)

        except Exception:
            logger.error(f"[TDA][CP{self.id}] Houve um erro ao Abrir a Comporta.")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.format_exc()}")

    def fechar(self) -> "None":
        try:
            if self.etapa == CP_FECHADA:
                logger.debug(f"[TDA][CP{self.id}] A comporta {self.id} já está fechada")

            else:
                EMB.escrever_bit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CMD_FECHAMENTO"], bit=3, valor=1)

        except Exception:
            logger.error(f"[TDA][CP{self.id}] Houve um erro ao fechar a comporta.")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.format_exc()}")

    def operar_cracking(self) -> "None":
        try:
            if self.etapa == CP_CRACKING:
                logger.debug(f"[TDA][CP{self.id}] A comporta {self.id} já está em cracking")

            elif self.verificar_condicoes():
                logger.debug(f"[TDA][CP{self.id}] Enviando comando de cracking para a comporta {self.id}")

                EMB.escrever_bit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CMD_ABERTURA_CRACKING"], bit=1, valor=1)

        except Exception:
            logger.error(f"[TDA][CP{self.id}] Houve um erro ao realizar a Operação de Cracking da Comporta.")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.format_exc()}")

    def aguardar_pressao_uh(self) -> "None":
        try:
            logger.debug(f"[TDA][CP{self.id}] Iniciando o timer para equilização da pressão da UH")

            while time() < (time() + 120):
                if self.pressao_equalizada.valor:
                    logger.debug(f"[TDA][CP{self.id}] Pressão equalizada, saindo do timer")
                    return

            logger.warning(f"[TDA][CP{self.id}] Estourou o timer de equalização de pressão da unidade hidráulica")
            self.borda_pressao = True

        except Exception:
            logger.error(f"[TDA][CP{self.id}] Houve um erro ao verificar a Pressão da Unidade Hidráulica da Comporta.")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.format_exc()}")

    def verificar_condicoes(self) -> "bool":
        """
        Função para verificação de Pré-Condições de Operação da Comporta.

        Acionao comando de Rearmes de falhas para daí começar a verificação.
        # TODO -> Adicionar ordem de verificações para operação das comportas.
        """
        
        self.rearme_falhas()

        try:
            if self.status_unidade_hidraulica.valor and not self.permissao and not self.bloqueio:

                if self.comporta_adjacente.operando in (2, 4, 32) or self.status_valvula_borboleta != 0 or self.status_limpa_grades != 0:
                    logger.debug(f"[TDA][CP{self.id}] Não há condições para operar a comporta {self.id}")

                    if self.comporta_adjacente.operando != 0:
                        logger.debug(f"[TDA][CP{self.id}] A comporta {self.comporta_adjacente.id} está repondo") if self.comporta_adjacente.operando == 2 else None
                        logger.debug(f"[TDA][CP{self.id}] A comporta {self.comporta_adjacente.id} está abrindo") if self.comporta_adjacente.operando == 4 else None
                        logger.debug(f"[TDA][CP{self.id}] A comporta {self.comporta_adjacente.id} está em cracking") if self.comporta_adjacente.operando == 32 else None
                        return False

                    elif self.status_limpa_grades != 0:
                        logger.debug(f"[TDA][CP{self.id}] O limpa grades está em operação")
                        return False

                    elif self.status_valvula_borboleta.valor != 0:
                        logger.debug(f"[TDA][CP{self.id}] A Válvula Borboleta está em operação")
                        return False

                    else:
                        logger.debug(f"[TDA][CP{self.id}] Aguardando Normalização")
                        return False

            elif not self.status_unidade_hidraulica.valor:
                logger.debug(f"[TDA][CP{self.id}] A Unidade Hidráulica está indisponível")
                return False

            elif self.bloqueio:
                logger.debug(f"[TDA][CP{self.id}] A Comporta ainda possui \"Bloqueios\" ativos")
                return False

            elif self.permissao:
                logger.debug(f"[TDA][CP{self.id}] A Comporta ainda possui \"Permissivos\" inválidos")
                return False

        except Exception:
            logger.error(f"[TDA][CP{self.id}] Houve um erro ao verificar as Pré-condições de Operação da Comporta.")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.format_exc()}")