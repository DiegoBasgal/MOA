
from time import sleep, time
from opcua import Client as OpcClient

from leitura import *
from escrita import *
from dicionarios.reg import *
from dicionarios.dict import *
from dicionarios.const import *

from clients import ClientsUsn
from comporta import Comporta

class Comporta:
    logger = logging.getLogger("__main__")

    def __init__(
            self,
            id: int | None = ...,
            clients: ClientsUsn | None = ...,
            escrita: list[EscritaBase] | None = ...
        ) -> ...:

        if not id or id < 1:
            raise ValueError(f"[CP{self.id}] A Comporta deve ser instanciada com um valor maior que \"0\".")
        else:
            self.id = id

        if not clients:
            raise ValueError(f"[CP{self.id}] Não foi possível carregar as conexões de campo (\"Clients\")")
        else:
            self.opc = clients

        self.__aberta = LeituraOpcBit(self.opc, OPC_UA["TDA"][f"CP{self.id}_ABERTA"], 17)
        self.__fechada = LeituraOpcBit(self.opc, OPC_UA["TDA"][f"CP{self.id}_FECHADA"], 18)
        self.__cracking = LeituraOpcBit(self.opc, OPC_UA["TDA"][f"CP{self.id}_CRACKING"], 25)
        self.__remoto = LeituraOpcBit(self.opc, OPC_UA["TDA"][f"CP{self.id}_REMOTO"], 22)

        self.__status = LeituraOpc(self.opc, OPC_UA["TDA"][f"CP{self.id}_COMPORTA_OPERANDO"])
        self.__permissao = LeituraOpcBit(self.opc, OPC_UA["TDA"][f"CP{self.id}_PERMISSIVOS_OK"], 31, True)
        self.__bloqueio = LeituraOpcBit(self.opc, OPC_UA["TDA"][f"CP{self.id}_BLOQUEIO_ATUADO"], 31, True)

        self._lista_comportas: list[Comportas] = []

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
    def lista_comportas(self) -> list[Comportas]:
        return self._lista_comportas

    @lista_comportas.setter
    def lista_comportas(self, var: list[Comportas]):
        self._lista_comportas = var


    def rearme_falhas_comporta(self) -> bool:
        try:
            return EscritaOPCBit(self.opc, OPC_UA["TDA"]["CP{}_CMD_REARME_FALHAS".format(self.id)], 0, 1)
        except Exception as e:
            raise(e)

    def abrir_comporta(self) -> bool:
        try:
            if self.etapa_comporta == CP_ABERTA:
                logger.debug("[CP{0}] A comporta {0} já está aberta".format(self.id))
                return True
            elif self.verificar_precondicoes_comporta():
                press_equalizada = LeituraOpcBit(self.opc, OPC_UA["TDA"]["CP{}_PRESSAO_EQUALIZADA".format(self.id)], 4)
                aguardando_cmd_abert = LeituraOpcBit(self.opc, OPC_UA["TDA"]["CP{}_AGUARDANDO_COMANDO_ABERTURA".format(self.id)], 3)
                if press_equalizada.valor and aguardando_cmd_abert.valor:
                    logger.debug("[CP{0}] Enviando comando de abertura para a comporta {0}".format(self.id))
                    response = EscritaOPCBit(self.opc, OPC_UA["TDA"]["CP{}_CMD_ABERTURA_TOTAL".format(self.id)], 1, 1)
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise(e)
        else:
            return response

    def fechar_comporta(self) -> bool:
        try:
            if self.etapa_comporta == CP_FECHADA:
                logger.debug("[CP{0}] A comporta {0} já está fechada".format(self.id))
                return True
            else:
                response = EscritaOPCBit(self.opc, OPC_UA["TDA"]["CP{}_CMD_FECHAMENTO".format(self.id)], 3, 1)
        except Exception as e:
            raise(e)
        else:
            return response

    def cracking_comporta(self) -> bool:
        try:
            if self.etapa_comporta == CP_CRACKING:
                logger.debug("[CP{0}] A comporta {} já está em cracking".format(self.id))
                return True
            elif self.verificar_precondicoes_comporta():
                logger.debug("[CP{0}] Enviando comando de cracking para a comporta {0}".format(self.id))
                response = EscritaOPCBit(self.opc, OPC_UA["TDA"]["CP{}_CMD_ABERTURA_CRACKING".format(self.id)], 1, 1)
            else:
                return False
        except Exception as e:
            raise(e)
        else:
            return response
    
    def verificar_pressao(self) -> bool:
        timer = time() + 120
        try:
            logger.info(f"[CP{self.id}] Iniciando o timer para equilização da pressão da UH")
            while time() < timer:
                if LeituraOpcBit(Client(CFG["client"]), OPC_UA["TDA"]["CP{}_PRESSAO_EQUALIZADA"], 4).valor:
                    logger.debug(f"[CP{self.id}] Pressão equalizada, saindo do timer")
                    self.timer_press = True
                    return True
            logger.warning(f"[CP{self.id}] Estourou o timer de equalização de pressão da unidade hidráulica")
            self.forcar_estado_indisponivel()
            self.timer_press = True
        except Exception as e:
            raise(e)
        return False

    def verificar_precondicoes_comporta(self) -> bool:
        self.rearme_falhas_comporta()
        try:
            if self.status_unidade_hidraulica and not self.permissao_comporta and not self.bloqueio_comporta:
                if self.status_outra_comporta == (2 or 4 or 32) or self.status_valvula_borboleta != 0 or self.status_limpa_grades != 0:
                    logger.debug("[CP{0}] Não há condições para operar a comporta {0}".format(self.id))
                    if self.status_outra_comporta != 0:
                        logger.debug("[CP{}] A comporta {} está repondo".format(self.id, 2 if self.id == 1 else 1)) if self.status_outra_comporta == 2 else None
                        logger.debug("[CP{}] A comporta {} está abrindo".format(self.id, 2 if self.id == 1 else 1)) if self.status_outra_comporta == 4 else None
                        logger.debug("[CP{}] A comporta {} está em cracking".format(self.id, 2 if self.id == 1 else 1)) if self.status_outra_comporta == 32 else None
                        return False
                    elif self.status_limpa_grades != 0:
                        logger.debug("[CP{}] O limpa grades está em operação".format(self.id))
                        return False
                    elif self.status_valvula_borboleta != 0:
                        logger.debug("[CP{}] A válvula borboleta está em operação".format(self.id))
                        return False
                    else:
                        logger.debug("[CP{}] Favor aguardar normalização".format(self.id))
                        return False
            elif not self.status_unidade_hidraulica:
                logger.debug("[CP{}] A Unidade Hidráulica ainda não está disponível".format(self.id))
                return False
            elif self.bloqueio_comporta:
                logger.debug("[CP{0}] A comporta {0} ainda possui bloqueios ativados".format(self.id))
                return False
            elif self.permissao_comporta:
                logger.debug("[CP{0}] A permissão da comporta {0} ainda não foi concedida".format(self.id))
                return False
        except Exception as e:
            raise(e)
        else:
            return True
