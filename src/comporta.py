__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__description__ = "Este módulo corresponde a implementação da operação das Comportas da Tomada da Água."

import logging
import traceback
import threading

import src.tomada_agua as tda

from time import time

from src.funcoes.leitura import *
from src.dicionarios.const import *
from src.conectores.servidores import Servidores

from src.funcoes.escrita import EscritaModBusBit as EMB


logger = logging.getLogger("logger")


class Comporta:
    def __init__(self, id: "int"=None, serv:"Servidores"=None, tda:"tda.TomadaAgua"=None) -> "None":

        # VERIFICAÇÃO DE ARGUMENTOS

        if not id or id < 1:
            raise ValueError(f"[CP{self.id}] A Comporta deve ser instanciada com um valor maior que \"0\".")
        else:
            self.__id = id

        self.tda = tda
        self.clp = serv.clp

        # ATRIBUIÇÃO DE VAIRÁVEIS PRIVADAS

        self.__aberta = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_ABERTA"],
            descricao=f"[CP{self.id}] Aberta"
        )
        self.__fechada = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_FECHADA"],
            descricao=f"[CP{self.id}] Fechada"
        )
        self.__cracking = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_CRACKING"],
            descricao=f"[CP{self.id}] Craking"
        )
        self.__manual = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_REMOTO"],
            descricao=f"[CP{self.id}] Modo Remoto"
        )
        self.__operando = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_OPERANDO"],
            descricao=f"[CP{self.id}] Operando"
        )
        self.__permissao = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_PERMISSIVOS_OK"],
            invertido=True,
            descricao=f"[CP{self.id}] Permissivos"
        )
        self.__bloqueio = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_BLQ_ATUADO"],
            descricao=f"[CP{self.id}] Bloqueio Atuado"
        )
        self.__pressao_equalizada = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_PRESSAO_EQUALIZADA"],
            descricao=f"[CP{self.id}] Pressão Equalizada"
        )
        self.__aguardando_abertura = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"][f"CP{self.id}_AGUARDANDO_CMD_ABERTURA"],
            descricao=f"[CP{self.id}] Aguardando Comando Abertura"
        )

        # ATRIBUIÇÃO DE VAIRÁVEIS PÚBLICAS

        self.borda_pressao: "bool" = False

    @property
    def id(self) -> "int":
        # PROPRIEDADE -> Retorna o ID da Comporta.

        return self.__id

    @property
    def operando(self) -> "bool":
        # PROPRIEDADE -> Retorna se a Comporta está Operando.

        return self.__operando.valor

    @property
    def bloqueio(self) -> "bool":
        # PROPRIEDADE -> Retorna se a Comporta possui Bloqueios Ativos.

        return self.__bloqueio.valor

    @property
    def permissao(self) -> "bool":
        # PROPRIEDADE -> Retorna se a Comporta possui Permissões de Operação.

        return self.__permissao.valor

    @property
    def pressao_equalizada(self) -> "bool":
        # PROPRIEDADE -> Retorna se a Comporta possui Permissões de Operação.

        return self.__pressao_equalizada.valor

    @property
    def aguardando_abertura(self) -> "bool":
        # PROPRIEDADE -> Retorna se a Comporta possui Permissões de Operação.

        return self.__aguardando_abertura.valor

    @property
    def etapa(self) -> "int":
        # PROPRIEDADE -> Retorna a etapa atual da operação da Comporta.

        try:
            if self.__fechada.valor:
                return CP_FECHADA
            elif self.__aberta.valor:
                return CP_ABERTA
            elif self.__cracking.valor:
                return CP_CRACKING
            elif self.__manual.valor:
                return CP_MANUAL
            elif self.operando:
                return CP_OPERANDO
            else:
                return CP_INCONSISTENTE

        except Exception:
            logger.error(f"[CP{self.id}] Houve um erro ao verificar a Etapa da Comporta.")
            return CP_INCONSISTENTE

    @property
    def comporta_adjacente(self) -> "Comporta":
        # PROPRIEDADE -> Retorna a instância da Comporta Adjacente.

        return self._comporta_adjacente

    @comporta_adjacente.setter
    def comporta_adjacente(self, var: "Comporta") -> "None":
        # SETTER -> Atribui a nova instância da Comporta Adjacente.

        self._comporta_adjacente = var

    def resetar_emergencia(self) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = EMB.escrever_bit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CMD_REARME_FLH"], valor=1)
            return res

        except Exception:
            logger.error(f"[CP{self.id}] Houve um erro ao realizar o Reset de Emergência da Comporta {self.id}.")
            logger.debug(traceback.format_exc())
            return False

    def abrir(self) -> "None":
        """
        Função para acionar comando de abertura da Comporta.

        Verifica se a comporta está aberta, caso não esteja, chama a função de verificação de condições
        de operação de comporta para depois, acionar o comando, caso as condições estejam de acordo.
        """

        try:
            if self.etapa == CP_ABERTA:
                logger.debug(f"[CP{self.id}]          A comporta já está Aberta")

            elif self.verificar_condicoes():
                if self.pressao_equalizada and self.aguardando_abertura:
                    logger.debug(f"[CP{self.id}]          Enviando comando:          \"ABRIR\"")

                    EMB.escrever_bit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CMD_ABERTURA_TOTAL"], valor=1)

        except Exception:
            logger.error(f"[CP{self.id}] Houve um erro ao acionar o comando de Abertura da Comporta {self.id}.")
            logger.debug(traceback.format_exc())

    def fechar(self) -> "bool":
        """
        Função para acionar comando de fechamento da Comporta.

        Verifica se a Comporta está fechada e caso não esteja, aciona o comando de fechamento.
        """

        try:
            if self.etapa == CP_FECHADA:
                logger.debug("")
                logger.debug(f"[CP{self.id}]          A Comporta já está Fechada")
                return True

            else:
                logger.debug("")
                logger.debug(f"[CP{self.id}]          Enviando comando:          \"FECHAR\"")
                res = EMB.escrever_bit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CMD_FECHAMENTO"], valor=1)
                return 

        except Exception:
            logger.error(f"[CP{self.id}] Houve um erro acionar o comando de Fechamento da Comporta {self.id}.")
            logger.debug(traceback.format_exc())

    def operar_cracking(self) -> "None":
        """
        Função para acionamento do comando de Cracking da Comporta.

        Vericfica se a Comporta já está em Cracking, caso não esteja, chama a função de verificação de
        condições de operação da Comporta para depois, acionar o comando de Cracking, caso as condições
        estejam de acordo.
        """

        try:
            if self.etapa == CP_CRACKING:
                logger.debug(f"[CP{self.id}]          A Comporta já está em Cracking")

            elif self.verificar_condicoes():
                logger.debug(f"[CP{self.id}]          Enviando comando:          \"CRACKING\"")

                EMB.escrever_bit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CMD_ABERTURA_CRACKING"], valor=1)

                threading.Thread(target=lambda: self.aguardar_pressao_uh()).start()

        except Exception:
            logger.error(f"[CP{self.id}] Houve um erro ao realizar a Operação de Cracking da Comporta {self.id}.")
            logger.debug(traceback.format_exc())

    def aguardar_pressao_uh(self) -> "None":
        """
        Função de temporização de espera da equalização da pressão da Unidade Hidráulica para
        operação da Comporta.
        """

        sleep(5)

        logger.debug(f"[CP{self.id}]          Verificação MOA:           \"Equalização de Pressão UH\"")
        delay = time() + 120

        while time() < delay:
            if self.pressao_equalizada:
                logger.debug(f"[CP{self.id}]          Verificação MOA:           \"UH Pressão Equalizada\"")
                return None

            else:
                sleep(2)

        logger.warning(f"[CP{self.id}]          Verificação MOA:           \"Equalização UH Ultrapassou o Tempo Limite!\"")
        self.borda_pressao = True

    def verificar_condicoes(self) -> "bool":
        """
        Função para verificação de Pré-Condições de Operação da Comporta.

        Aciona o comando de Rearmes de falhas e caso o comando retorne verdadeiro, continua com a
        verificação de condições.
        Verifica se a comporta possui algum bloqueio ou falta permissivos, se sim, avisa o operador
        e passa a verificar as condições que podem ter causado a falta de condições verdadeiras.
        Dentro da falta de condições, verifica se o limpa grades ou a válvula borboleta ou a outra
        comporta estão em operação. Dependendo da condição, avisa o operador com o caso específico e
        retorna Falso.
        Caso os bloqueios e permissivos estjam de acordo, verifica se a Unidade Hidráulica está
        disponível e caso não esteja, avisa o operador e retorna Falso.
        Caso todas as condições estjam de acordo com a operação, retorna Verdadeiro para o acionamento
        do comando da comporta desejado.
        """

        if not self.resetar_emergencia():
            return False

        try:
            if self.bloqueio or self.permissao:
                if self.aguardando_abertura:
                    return True
                else:
                    logger.debug(f"[CP{self.id}]          Sem condições para operar a Comporta!")

                    logger.debug(f"[CP{self.id}]          Ainda há \"Bloqueios\" Ativos") if self.bloqueio else None
                    logger.debug(f"[CP{self.id}]          Ainda há \"Permissivos\" Inválidos") if self.permissao else None

                if self.tda.status_valvula_borboleta.valor or self.tda.status_limpa_grades.valor or self.comporta_adjacente.operando in (2, 4, 32):
                    logger.debug(f"[CP{self.id}]          Limpa Grades Operando") if self.tda.status_limpa_grades.valor != 0 else None
                    logger.debug(f"[CP{self.id}]          Válvula Borboleta Operando") if self.tda.status_valvula_borboleta.valor != 0 else None

                    logger.debug(f"[CP{self.id}]          Comporta {self.comporta_adjacente.id} Repondo") if self.comporta_adjacente.operando == 2 else None
                    logger.debug(f"[CP{self.id}]          Comporta {self.comporta_adjacente.id} Abrindo") if self.comporta_adjacente.operando == 4 else None
                    logger.debug(f"[CP{self.id}]          Comporta {self.comporta_adjacente.id} Operando Cracking") if self.comporta_adjacente.operando == 32 else None
                    return False

                else:
                    return False

            elif not self.tda.status_unidade_hidraulica.valor:
                logger.debug(f"[CP{self.id}]          Unidade Hidráulica:        \"Indisponível\"")
                return False

            else:
                return True

        except Exception:
            logger.error(f"[CP{self.id}] Houve um erro ao verificar as Pré-condições de Operação da Comporta {self.id}.")
            logger.debug(traceback.format_exc())
            return False