__version__ = "0.1"
__author__ = "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da operação da Tomada da Água."

from usina import *

logger = logging.getLogger("__main__")

class TomadaAgua(Usina):
    def __init__(self, *args, **kwargs) -> ...:
        super().__init__(self, *args, **kwargs)

        self.__nv_montante = LeituraModbus(self.clp["TDA"], REG_CLP["TDA"]["NIVEL_MONTANTE"], descricao="TDA_NIVEL_MONTANTE")
        self.__status_lp = LeituraModbus(self.clp["TDA"], REG_CLP["TDA"]["LG_OPERACAO_MANUAL"], descricao="TDA_LG_OPERACAO_MANUAL")
        self.__status_vb = LeituraModbus(self.clp["TDA"], REG_CLP["TDA"]["VB_FECHANDO"], descricao="TDA_VB_FECHANDO")
        self.__status_uh = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["UH_UNIDADE_HIDRAULICA_DISPONIVEL"], bit=1, descricao="TDA_UH_UNIDADE_HIDRAULICA_DISPONIVEL")

        self._condicionadores = []
        self._condicionadores_essenciais = []

        self.erro_nv: float = 0
        self.erro_nv_anterior: float = 0
        self.nv_montante_recente: float = 0
        self.nv_montante_anterior: float = 0

    @property
    def nv_montante(self) -> float:
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
        if not self.leitura_filtro_limpo_uh.valor:
            logger.warning("[TDA] O filtro da UH da TDA está sujo. Favor realizar limpeza/troca.")

        if self.leitura_nivel_jusante_comporta_1.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 1. Favor verificar.")

        if self.leitura_nivel_jusante_comporta_2.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 2. Favor verificar.")

        if not self.leitura_ca_com_tensao.valor:
            logger.warning("[TDA] Foi dentificado que o CA da tomada da água está sem tensão. Favor verificar.")

        if self.leitura_lg_operacao_manual.valor:
            logger.warning("[TDA] Foi identificado que o Limpa Grades entrou em operação manual. Favor verificar.")

        if self.leitura_nivel_jusante_grade_comporta_1.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 1. Favor verificar.")

        if self.leitura_nivel_jusante_grade_comporta_2.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 2. Favor verificar.")


        if self.leitura_falha_atuada_lg.valor and not Dicionarios.voip["LG_FALHA_ATUADA"][0]:
            logger.warning("[TDA] Foi identificado que o limpa grades está em falha. Favor verificar.")
            Dicionarios.voip["LG_FALHA_ATUADA"][0] = True
        elif not self.leitura_falha_atuada_lg.valor and Dicionarios.voip["LG_FALHA_ATUADA"][0]:
            Dicionarios.voip["LG_FALHA_ATUADA"][0] = False

        if self.leitura_falha_nivel_montante.valor and not Dicionarios.voip["FALHA_NIVEL_MONTANTE"][0]:
            logger.warning("[TDA] Houve uma falha na leitura de nível montante. Favor verificar.")
            Dicionarios.voip["FALHA_NIVEL_MONTANTE"][0] = True
        elif not self.leitura_falha_nivel_montante.valor and Dicionarios.voip["FALHA_NIVEL_MONTANTE"][0]:
            Dicionarios.voip["FALHA_NIVEL_MONTANTE"][0] = False

    def iniciar_leituras_condicionadores(self) -> None:
        # CONDICIONADORES ESSENCIAIS
        # Normalizar
            # Bit Invertido
        self.leitura_sem_emergencia_tda = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["SEM_EMERGENCIA"], bit=24, invertido=True, descricao="TDA_SEM_EMERGENCIA")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_sem_emergencia_tda, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Normalizar
            # Bit Invertido
        self.leitura_ca_com_tensao = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["COM_TENSAO_CA"], bit=11, invertido=True, descricao="TDA_COM_TENSAO_CA")
        self.condicionadores.append(CondicionadorBase(self.leitura_ca_com_tensao, CONDIC_NORMALIZAR))

            # Bit Normal
        self.leitura_falha_ligar_bomba_uh = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["UH_FALHA_LIGAR_BOMBA"], bit=2, descricao="TDA_UH_FALHA_LIGAR_BOMBA")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_ligar_bomba_uh, CONDIC_NORMALIZAR))


        # LEITURAS PARA LEITURA PERIÓDICA
        # Telegram
            # Bit Invertido
        self.leitura_ca_com_tensao = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["COM_TENSAO_CA"], bit=11, invertido=True, descricao="TDA_COM_TENSAO_CA")
        self.leitura_filtro_limpo_uh = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["UH_FILTRO_LIMPO"], bit=13, invertido=True, descricao="TDA_UH_FILTRO_LIMPO")

            # Bit Normal
        self.leitura_lg_operacao_manual = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["LG_OPERACAO_MANUAL"], bit=0, descricao="TDA_LG_OPERACAO_MANUAL")
        self.leitura_nivel_jusante_comporta_1 = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["NIVEL_JUSANTE_COMPORTA_1"], bit=2, descricao="TDA_NIVEL_JUSANTE_COMPORTA_1")
        self.leitura_nivel_jusante_comporta_2 = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["NIVEL_JUSANTE_COMPORTA_2"], bit=4, descricao="TDA_NIVEL_JUSANTE_COMPORTA_2")
        self.leitura_nivel_jusante_grade_comporta_1 = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_1"], bit=1, descricao="TDA_FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_1")
        self.leitura_nivel_jusante_grade_comporta_2 = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_2"], bit=3, descricao="TDA_FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_2")

        # Telegram + Voip
            # Bit Normal
        self.leitura_falha_atuada_lg = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["LG_FALHA_ATUADA"], bit=31, descricao="TDA_LG_FALHA_ATUADA")
        self.leitura_falha_nivel_montante = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["FALHA_NIVEL_MONTANTE"], bit=0, descricao="TDA_FALHA_NIVEL_MONTANTE")
