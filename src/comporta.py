from usina import *

class Comporta(TomadaAgua):
    def __init__(self, id: int = None) -> ...:
        # VERIFICAÇÃO DE ARGUMENTOS
        if not id or id < 1:
            raise ValueError(f"[CP{self.id}] A Comporta deve ser instanciada com um valor maior que \"0\".")
        else:
            self.__id = id

        # ATRIBUIÇÃO DE VAIRÁVEIS
        # Privadas
        self.__aberta = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_ABERTA"], 17)
        self.__fechada = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_FECHADA"], 18)
        self.__cracking = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CRACKING"], 25)
        self.__remoto = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_REMOTO"], 22)

        self.__status = LeituraModbus(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_COMPORTA_OPERANDO"])
        self.__permissao = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_PERMISSIVOS_OK"], 31, True)
        self.__bloqueio = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_BLOQUEIO_ATUADO"], 31, True)

        # PÚBLICAS
        self.press_equalizada = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_PRESSAO_EQUALIZADA"], 4)
        self.aguardando_cmd_abert = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_AGUARDANDO_COMANDO_ABERTURA"], 3)

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
    def lista_comportas(self) -> "list[Comporta]":
        return self._lista_comportas

    @lista_comportas.setter
    def lista_comportas(self, var: "list[Comporta]"):
        self._lista_comportas = var


    def resetar_emergencia(self) -> bool:
        return EscritaModBusBit.escrever_bit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CMD_REARME_FALHAS"], bit=0, valor=1)

    def rearme_falhas_comporta(self) -> bool:
        try:
            return EscritaModBusBit.escrever_bit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CMD_REARME_FALHAS"], bit=0, valor=1)
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
                    EscritaModBusBit.escrever_bit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CMD_ABERTURA_TOTAL"], bit=2, valor=1)
                    return

        except Exception as e:
            logger.error(f"[TDA][CP{self.id}] Houve um erro ao abrir a comporta. Exception: \"{repr(e)}\"")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.format_exc()}")

    def fechar_comporta(self) -> None:
        try:
            if self.etapa_comporta == CP_FECHADA:
                logger.debug(f"[TDA][CP{self.id}] A comporta {self.id} já está fechada")
                return
            else:
                EscritaModBusBit.escrever_bit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CMD_FECHAMENTO"], bit=3, valor=1)
                return

        except Exception as e:
            logger.error(f"[TDA][CP{self.id}] Houve um erro ao fechar a comporta. Exception: \"{repr(e)}\"")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.format_exc()}")

    def cracking_comporta(self) -> None:
        try:
            if self.etapa_comporta == CP_CRACKING:
                logger.debug(f"[TDA][CP{self.id}] A comporta {self.id} já está em cracking")
                return
            elif self.verificar_precondicoes_comporta():
                logger.debug(f"[TDA][CP{self.id}] Enviando comando de cracking para a comporta {self.id}")
                EscritaModBusBit.escrever_bit(self.clp["TDA"], REG_CLP["TDA"][f"CP{self.id}_CMD_ABERTURA_CRACKING"], bit=1, valor=1)
                return

        except Exception as e:
            logger.error(f"[TDA][CP{self.id}] Houve um erro ao realizar o cracking da comporta. Exception: \"{repr(e)}\"")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.format_exc()}")

    def verificar_pressao(self) -> None:
        try:
            logger.info(f"[TDA][CP{self.id}] Iniciando o timer para equilização da pressão da UH")
            while time() < (time() + 120):
                if self.press_equalizada.valor:
                    logger.debug(f"[TDA][CP{self.id}] Pressão equalizada, saindo do timer")
                    return
            logger.warning(f"[TDA][CP{self.id}] Estourou o timer de equalização de pressão da unidade hidráulica")
            self.borda_pressao = True

        except Exception as e:
            logger.error(f"[TDA][CP{self.id}] Houve um erro ao verificar a pressão da UH da comporta. Exception: \"{repr(e)}\"")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.format_exc()}")

    def verificar_precondicoes_comporta(self) -> bool:
        self.rearme_falhas_comporta()
        try:
            if self.unidade_hidraulica and not self.permissao_comporta and not self.bloqueio_comporta:
                if self.c in (2, 4, 32) or self.valvula_borboleta != 0 or self.limpa_grades != 0:
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
            logger.error(f"[TDA][CP{self.id}] Houve um erro ao verificar as pré-condições da comporta.")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.format_exc()}")
        else:
            return True