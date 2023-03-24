__author__ = "Diego Basgal"
__credits__ = "Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal"

__version__ = "0.1"
__status__ = "Development"
__maintainer__ = "Diego Basgal"
__email__ = "diego.garcia@ritmoenergia.com.br"
__description__ = "Este módulo corresponde a implementação da operação de comportas."

import logging
import traceback

from time import  time

from leitura import *
from dicionarios.reg import *
from dicionarios.const import *

from comporta import Comporta
from setores import TomadaAgua

logger = logging.getLogger("__main__")

class Comporta(TomadaAgua):
    def __init__(self, id: int | None = ...) -> ...:
        # VERIFICAÇÃO DE ARGUMENTOS
        if not id or id < 1:
            raise ValueError(f"[CP{self.id}] A Comporta deve ser instanciada com um valor maior que \"0\".")
        else:
            self.__id = id

        # ATRIBUIÇÃO DE VAIRÁVEIS PRIVADAS
        # Leituras
        self.__aberta = LeituraOpcBit(self.opc, OPC_UA["TDA"][f"CP{self.id}_ABERTA"], 17)
        self.__fechada = LeituraOpcBit(self.opc, OPC_UA["TDA"][f"CP{self.id}_FECHADA"], 18)
        self.__cracking = LeituraOpcBit(self.opc, OPC_UA["TDA"][f"CP{self.id}_CRACKING"], 25)
        self.__remoto = LeituraOpcBit(self.opc, OPC_UA["TDA"][f"CP{self.id}_REMOTO"], 22)

        self.__status = LeituraOpc(self.opc, OPC_UA["TDA"][f"CP{self.id}_COMPORTA_OPERANDO"])
        self.__permissao = LeituraOpcBit(self.opc, OPC_UA["TDA"][f"CP{self.id}_PERMISSIVOS_OK"], 31, True)
        self.__bloqueio = LeituraOpcBit(self.opc, OPC_UA["TDA"][f"CP{self.id}_BLOQUEIO_ATUADO"], 31, True)

        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS
        # Instâncias das comportas
        self._lista_comportas: list[Comporta] = []

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS
        # Instância(s) da(s) outra(s) comporta(s)
        self.cp2 = self.lista_comportas[1]

        # Leituras
        self.press_equalizada = LeituraOpcBit(self.opc, OPC_UA["TDA"][f"CP{self.id}_PRESSAO_EQUALIZADA"], 4)
        self.aguardando_cmd_abert = LeituraOpcBit(self.opc, OPC_UA["TDA"][f"CP{self.id}_AGUARDANDO_COMANDO_ABERTURA"], 3)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def etapa_comporta(self) -> int:
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
                logger.debug(f"[CP{self.id}] Comporta em etapa inconsistente.")
                return 99
        except ValueError(f"[CP{self.id}] Comporta retornou valor de etapa inválido.") \
            or ConnectionError(f"[CP{self.id}] Falha na comunicação com a comporta."):
            return 99

    @property
    def status_comporta(self) -> int:
        try:
            return self.__status.valor
        except ValueError(f"[CP{self.id}] Comporta retornou valor de status inválido.") \
            or ConnectionError(f"[CP{self.id}] Falha na comunicação com a comporta."):
            return 99

    @property
    def permissao_comporta(self) -> int:
        try:
            return self.__permissao.valor
        except ValueError(f"[CP{self.id}] Comporta retornou valor de permissivo inválido.") \
            or ConnectionError(f"[CP{self.id}] Falha na comunicação com a comporta."):
            return 99

    @property
    def bloqueio_comporta(self) -> int:
        try:
            return self.__bloqueio.valor
        except ValueError(f"[CP{self.id}] Comporta retornou valor de bloqueio inválido.") \
            or ConnectionError(f"[CP{self.id}] Falha na comunicação com a comporta."):
            return 99

    @property
    def lista_comportas(self) -> list[Comporta]:
        return self._lista_comportas

    @lista_comportas.setter
    def lista_comportas(self, var: list[Comporta]):
        self._lista_comportas = var


    def rearme_falhas_comporta(self) -> bool:
        try:
            return self.e_opc_bit.escrever(self.opc, OPC_UA["TDA"][f"CP{self.id}_CMD_REARME_FALHAS"], 0, 1)
        except Exception as e:
            raise(e)

    def abrir_comporta(self) -> None:
        try:
            if self.etapa_comporta == CP_ABERTA:
                logger.debug(f"[TDA][CP{self.id}] A comporta {self.id} já está aberta")
                return
            elif self.verificar_precondicoes_comporta():
                if self.press_equalizada.valor and self.aguardando_cmd_abert.valor:
                    logger.debug(f"[TDA][CP{self.id}] Enviando comando de abertura para a comporta {self.id}")
                    self.e_opc_bit.escrever(self.opc, OPC_UA["TDA"][f"CP{self.id}_CMD_ABERTURA_TOTAL"], 1, 1)
                    return
        except Exception as e:
            logger.exception(f"[TDA][CP{self.id}] Houve um erro ao abrir a comporta. Exception: \"{repr(e)}\"")
            logger.exception(f"[TDA][CP{self.id}] Traceback: {traceback.print_stack}")

    def fechar_comporta(self) -> None:
        try:
            if self.etapa_comporta == CP_FECHADA:
                logger.debug(f"[TDA][CP{self.id}] A comporta {self.id} já está fechada")
                return
            else:
                self.e_opc_bit.escrever(self.opc, OPC_UA["TDA"][f"CP{self.id}_CMD_FECHAMENTO"], 3, 1)
                return

        except Exception as e:
            logger.exception(f"[TDA][CP{self.id}] Houve um erro ao fechar a comporta. Exception: \"{repr(e)}\"")
            logger.exception(f"[TDA][CP{self.id}] Traceback: {traceback.print_stack}")

    def cracking_comporta(self) -> None:
        try:
            if self.etapa_comporta == CP_CRACKING:
                logger.debug(f"[TDA][CP{self.id}] A comporta {self.id} já está em cracking")
                return
            elif self.verificar_precondicoes_comporta():
                logger.debug(f"[TDA][CP{self.id}] Enviando comando de cracking para a comporta {self.id}")
                self.e_opc_bit.escrever(self.opc, OPC_UA["TDA"][f"CP{self.id}_CMD_ABERTURA_CRACKING"], 1, 1)
                return

        except Exception as e:
            logger.exception(f"[TDA][CP{self.id}] Houve um erro ao realizar o cracking da comporta. Exception: \"{repr(e)}\"")
            logger.exception(f"[TDA][CP{self.id}] Traceback: {traceback.print_stack}")

    def verificar_pressao(self) -> None:
        try:
            logger.info(f"[TDA][CP{self.id}] Iniciando o timer para equilização da pressão da UH")
            while time() < time() + 120:
                if self.press_equalizada.valor:
                    logger.debug(f"[TDA][CP{self.id}] Pressão equalizada, saindo do timer")
                    self.timer_press = True
                    return
            logger.warning(f"[TDA][CP{self.id}] Estourou o timer de equalização de pressão da unidade hidráulica")
            self.timer_press = True

        except Exception as e:
            logger.exception(f"[TDA][CP{self.id}] Houve um erro ao verificar a pressão da UH da comporta. Exception: \"{repr(e)}\"")
            logger.exception(f"[TDA][CP{self.id}] Traceback: {traceback.print_stack}")

    def verificar_precondicoes_comporta(self) -> bool:
        self.rearme_falhas_comporta()
        try:
            if self.unidade_hidraulica and not self.permissao_comporta and not self.bloqueio_comporta:
                if self.cp2.status_comporta in (2, 4, 32) or self.valvula_borboleta != 0 or self.limpa_grades != 0:
                    logger.debug(f"[TDA][CP{self.id}] Não há condições para operar a comporta {self.id}")
                    if self.cp2.status_comporta != 0:
                        logger.debug(f"[TDA][CP{self.id}] A comporta {self.cp2.id} está repondo") if self.cp2.status_comporta == 2 else None
                        logger.debug(f"[TDA][CP{self.id}] A comporta {self.cp2.id} está abrindo") if self.cp2.status_comporta == 4 else None
                        logger.debug(f"[TDA][CP{self.id}] A comporta {self.cp2.id} está em cracking") if self.cp2.status_comporta == 32 else None
                        return False
                    elif self.limpa_grades != 0:
                        logger.debug(f"[TDA][CP{self.id}] O limpa grades está em operação")
                        return False
                    elif self.valvula_borboleta != 0:
                        logger.debug(f"[TDA][CP{self.id}] A válvula borboleta está em operação")
                        return False
                    else:
                        logger.debug(f"[TDA][CP{self.id}] Favor aguardar normalização")
                        return False
            elif not self.unidade_hidraulica:
                logger.debug(f"[TDA][CP{self.id}] A Unidade Hidráulica ainda não está disponível")
                return False
            elif self.bloqueio_comporta:
                logger.debug(f"[TDA][CP{self.id}] A comporta {self.id} ainda possui bloqueios ativados")
                return False
            elif self.permissao_comporta:
                logger.debug(f"[TDA][CP{self.id}] A permissão da comporta {self.id} ainda não foi concedida")
                return False
        except Exception as e:
            raise(e)
        else:
            return True
