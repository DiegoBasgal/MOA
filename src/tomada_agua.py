__version__ = "0.1"
__author__ = "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da operação da Tomada da Água."

from usina import *

logger = logging.getLogger("__main__")

class TomadaAgua(Usina):
    def __init__(self, *args, **kwargs) -> ...:
        super().__init__(self, *args, **kwargs)

        self.__nv_montante = LeituraOpc(OPC_UA["TDA"]["NIVEL_MONTANTE"])
        self.__status_lp = LeituraOpc(OPC_UA["TDA"]["LG_OPERACAO_MANUAL"])
        self.__status_vb = LeituraOpc(OPC_UA["TDA"]["VB_FECHANDO"])
        self.__status_uh = LeituraOpcBit(OPC_UA["TDA"]["UH_UNIDADE_HIDRAULICA_DISPONIVEL"], 1)

        self._condicionadores = []
        self._condicionadores_essenciais = []

        self.erro_nv: int | float = 0
        self.erro_nv_anterior: int | float = 0
        self.nv_montante_recente: int | float = 0
        self.nv_montante_anterior: int | float = 0

    @property
    def nv_montante(self) -> int | float:
        return self.__nv_montante.valor

    @property
    def limpa_grades(self) -> int:
        try:
            return self.__status_lp.valor
        except ValueError(f"[TDA] O limpa grades retornou valor de status inválido.") \
            or ConnectionError(f"[TDA] Falha na comunicação com o limpa grades."):
            return 99

    @property
    def valvula_borboleta(self) -> int:
        try:
            return self.__status_vb.valor
        except ValueError(f"[TDA] O limpa grades retornou valor de status inválido.") \
            or ConnectionError(f"[TDA] Falha na comunicação com o limpa grades."):
            return 99

    @property
    def unidade_hidraulica(self) -> int:
        try:
            return self.__status_uh.valor
        except ValueError(f"[TDA] A unidade hidráulica retornou valor de status inválido.") \
            or ConnectionError(f"[TDA] Falha na comunicação com a unidade hidráulica."):
            return 99

    @property
    def condicionadores(self) -> list[CondicionadorBase]:
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: list[CondicionadorBase]) -> None:
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> list[CondicionadorBase]:
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: list[CondicionadorBase]) -> None:
        self._condicionadores_essenciais = var

    def atualizar_montante_recente(self) -> None:
        if not self.glb_dict["tda_offline"]:
            self.nv_montante_recente = self.tda.nv_montante
            self.erro_nv_anterior = self.erro_nv
            self.erro_nv = self.nv_montante_recente - self.cfg["nv_alvo"]

    def controle_reservatorio(self) -> int:
        # Reservatório acima do nível máximo
        if self.tda.nv_montante >= self.cfg["nv_maximo"]:
            logger.info("[USN] Nível montante acima do máximo.")

            if self.nv_montante_recente >= NIVEL_MAXIMORUM:
                logger.critical(f"[USN] Nivel montante ({self.nv_montante_recente:3.2f}) atingiu o maximorum!")
                return NV_FLAG_EMERGENCIA

            else:
                self.controle_i = 0.5
                self.controle_ie = 0.5
                self.distribuir_potencia(self.cfg["pot_maxima_usina"])

        # Reservatório abaixo do nível mínimo
        elif self.tda.nv_montante <= self.cfg["nv_minimo"] and not self.aguardando_reservatorio:
            logger.info("[USN] Nível montante abaixo do mínimo.")
            self.aguardando_reservatorio = True
            self.distribuir_potencia(0)

            if self.nv_montante_recente <= NIVEL_FUNDO_RESERVATORIO:
                logger.critical(f"[USN] Nivel montante ({self.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                return NV_FLAG_EMERGENCIA

        # Aguardando nível do reservatório
        elif self.aguardando_reservatorio:
            if self.tda.nv_montante >= self.cfg["nv_alvo"]:
                logger.debug("[USN] Nível montante dentro do limite de operação.")
                self.aguardando_reservatorio = False

        # Reservatório Normal
        else:
            self.controle_potencia()

        [ug.step() for ug in self.ugs]

        return NV_FLAG_NORMAL

    def verificar_condicionadores(self) -> int:
        if [condic.ativo for condic in self.condicionadores_essenciais]:
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]
            condic_flag = [CONDIC_NORMALIZAR for condic in condics_ativos if condic.gravidade == CONDIC_NORMALIZAR]
            condic_flag = [CONDIC_INDISPONIBILIZAR for condic in condics_ativos if condic.gravidade == CONDIC_INDISPONIBILIZAR]

            if condic_flag in (CONDIC_NORMALIZAR, CONDIC_INDISPONIBILIZAR):
                logger.info("[SA] Foram detectados condicionadores ativos!")
                [logger.info(f"[SA] Condicionador: \"{condic.descricao}\", Gravidade: \"{condic.gravidade}\".") for condic in condics_ativos]
        return condic_flag

    def leitura_periodica(self) -> None:
        if not self.leitura_filtro_limpo_uh:
            logger.warning("[TDA] O filtro da UH da TDA está sujo. Favor realizar limpeza/troca.")

        if self.leitura_nivel_jusante_comporta_1:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 1. Favor verificar.")

        if self.leitura_nivel_jusante_comporta_2:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 2. Favor verificar.")

        if not self.leitura_ca_com_tensao:
            logger.warning("[TDA] Foi dentificado que o CA da tomada da água está sem tensão. Favor verificar.")

        if self.leitura_lg_operacao_manual:
            logger.warning("[TDA] Foi identificado que o Limpa Grades entrou em operação manual. Favor verificar.")

        if self.leitura_nivel_jusante_grade_comporta_1:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 1. Favor verificar.")

        if self.leitura_nivel_jusante_grade_comporta_2:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 2. Favor verificar.")


        if self.leitura_falha_atuada_lg and not self.voip_dict["LG_FALHA_ATUADA"]:
            logger.warning("[TDA] Foi identificado que o limpa grades está em falha. Favor verificar.")
            self.voip_dict["LG_FALHA_ATUADA"] = True
        elif not self.leitura_falha_atuada_lg and self.voip_dict["LG_FALHA_ATUADA"]:
            self.voip_dict["LG_FALHA_ATUADA"] = False

        if self.leitura_falha_nivel_montante and not self.voip_dict["FALHA_NIVEL_MONTANTE"]:
            logger.warning("[TDA] Houve uma falha na leitura de nível montante. Favor verificar.")
            self.voip_dict["FALHA_NIVEL_MONTANTE"] = True
        elif not self.leitura_falha_nivel_montante and self.voip_dict["FALHA_NIVEL_MONTANTE"]:
            self.voip_dict["FALHA_NIVEL_MONTANTE"] = False

    def iniciar_leituras_condicionadores(self) -> None:
        # CONDICIONADORES ESSENCIAIS
        # Normalizar
            # Bit Invertido
        self.leitura_sem_emergencia_tda = LeituraOpcBit(OPC_UA["TDA"]["SEM_EMERGENCIA"], 24, True, "TDA_SEM_EMERGENCIA")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_sem_emergencia_tda, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Normalizar
            # Bit Invertido
        self.leitura_ca_com_tensao = LeituraOpcBit(OPC_UA["TDA"]["COM_TENSAO_CA"], 11, True, "TDA_COM_TENSAO_CA")
        self.condicionadores.append(CondicionadorBase(self.leitura_ca_com_tensao, CONDIC_NORMALIZAR))

            # Bit Normal
        self.leitura_falha_ligar_bomba_uh = LeituraOpcBit(OPC_UA["TDA"]["UH_FALHA_LIGAR_BOMBA"], 2, "TDA_UH_FALHA_LIGAR_BOMBA")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_ligar_bomba_uh, CONDIC_NORMALIZAR))


        # LEITURAS PARA LEITURA PERIÓDICA
        # Telegram
            # Bit Invertido
        self.leitura_ca_com_tensao = LeituraOpcBit(OPC_UA["TDA"]["COM_TENSAO_CA"], 11, True)
        self.leitura_filtro_limpo_uh = LeituraOpcBit(OPC_UA["TDA"]["UH_FILTRO_LIMPO"], 13, True)

            # Bit Normal
        self.leitura_lg_operacao_manual = LeituraOpcBit(OPC_UA["TDA"]["LG_OPERACAO_MANUAL"], 0)
        self.leitura_nivel_jusante_comporta_1 = LeituraOpcBit(OPC_UA["TDA"]["NIVEL_JUSANTE_COMPORTA_1"], 2)
        self.leitura_nivel_jusante_comporta_2 = LeituraOpcBit(OPC_UA["TDA"]["NIVEL_JUSANTE_COMPORTA_2"], 4)
        self.leitura_nivel_jusante_grade_comporta_1 = LeituraOpcBit(OPC_UA["TDA"]["FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_1"], 1)
        self.leitura_nivel_jusante_grade_comporta_2 = LeituraOpcBit(OPC_UA["TDA"]["FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_2"], 3)

        # Telegram + Voip
            # Bit Normal
        self.leitura_falha_atuada_lg = LeituraOpcBit(OPC_UA["TDA"]["LG_FALHA_ATUADA"], 31)
        self.leitura_falha_nivel_montante = LeituraOpcBit(OPC_UA["TDA"]["FALHA_NIVEL_MONTANTE"], 0)


class Comporta(TomadaAgua):
    def __init__(self, id: int | None = ...) -> ...:
        # VERIFICAÇÃO DE ARGUMENTOS
        if not id or id < 1:
            raise ValueError(f"[CP{self.id}] A Comporta deve ser instanciada com um valor maior que \"0\".")
        else:
            self.__id = id

        # ATRIBUIÇÃO DE VAIRÁVEIS
        # Privadas
        self.__aberta = LeituraOpcBit(OPC_UA["TDA"][f"CP{self.id}_ABERTA"], 17)
        self.__fechada = LeituraOpcBit(OPC_UA["TDA"][f"CP{self.id}_FECHADA"], 18)
        self.__cracking = LeituraOpcBit(OPC_UA["TDA"][f"CP{self.id}_CRACKING"], 25)
        self.__remoto = LeituraOpcBit(OPC_UA["TDA"][f"CP{self.id}_REMOTO"], 22)

        self.__status = LeituraOpc( OPC_UA["TDA"][f"CP{self.id}_COMPORTA_OPERANDO"])
        self.__permissao = LeituraOpcBit(OPC_UA["TDA"][f"CP{self.id}_PERMISSIVOS_OK"], 31, True)
        self.__bloqueio = LeituraOpcBit(OPC_UA["TDA"][f"CP{self.id}_BLOQUEIO_ATUADO"], 31, True)

        # PÚBLICAS
        self.press_equalizada = LeituraOpcBit(OPC_UA["TDA"][f"CP{self.id}_PRESSAO_EQUALIZADA"], 4)
        self.aguardando_cmd_abert = LeituraOpcBit(OPC_UA["TDA"][f"CP{self.id}_AGUARDANDO_COMANDO_ABERTURA"], 3)

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
    def lista_comportas(self) -> list["Comporta"]:
        return self._lista_comportas

    @lista_comportas.setter
    def lista_comportas(self, var: list["Comporta"]):
        self._lista_comportas = var


    def resetar_emergencia(self) -> bool:
        return self.escrita_opc.escrever_bit(OPC_UA["TDA"][f"CP{self.id}_CMD_REARME_FALHAS"], valor=1, bit=0)

    def rearme_falhas_comporta(self) -> bool:
        try:
            return self.escrita_opc.escrever(self.opc, OPC_UA["TDA"][f"CP{self.id}_CMD_REARME_FALHAS"], 0, 1)
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
                    self.escrita_opc.escrever(self.opc, OPC_UA["TDA"][f"CP{self.id}_CMD_ABERTURA_TOTAL"], 1, 1)
                    return

        except Exception as e:
            logger.exception(f"[TDA][CP{self.id}] Houve um erro ao abrir a comporta. Exception: \"{repr(e)}\"")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.print_stack}")

    def fechar_comporta(self) -> None:
        try:
            if self.etapa_comporta == CP_FECHADA:
                logger.debug(f"[TDA][CP{self.id}] A comporta {self.id} já está fechada")
                return
            else:
                self.escrita_opc.escrever(self.opc, OPC_UA["TDA"][f"CP{self.id}_CMD_FECHAMENTO"], 3, 1)
                return

        except Exception as e:
            logger.exception(f"[TDA][CP{self.id}] Houve um erro ao fechar a comporta. Exception: \"{repr(e)}\"")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.print_stack}")

    def cracking_comporta(self) -> None:
        try:
            if self.etapa_comporta == CP_CRACKING:
                logger.debug(f"[TDA][CP{self.id}] A comporta {self.id} já está em cracking")
                return
            elif self.verificar_precondicoes_comporta():
                logger.debug(f"[TDA][CP{self.id}] Enviando comando de cracking para a comporta {self.id}")
                self.escrita_opc.escrever(self.opc, OPC_UA["TDA"][f"CP{self.id}_CMD_ABERTURA_CRACKING"], 1, 1)
                return

        except Exception as e:
            logger.exception(f"[TDA][CP{self.id}] Houve um erro ao realizar o cracking da comporta. Exception: \"{repr(e)}\"")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.print_stack}")

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
            logger.exception(f"[TDA][CP{self.id}] Houve um erro ao verificar a pressão da UH da comporta. Exception: \"{repr(e)}\"")
            logger.debug(f"[TDA][CP{self.id}] Traceback: {traceback.print_stack}")

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
            raise(e)
        else:
            return True