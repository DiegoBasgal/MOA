__version__ = "0.1"
__author__ = "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da operação do Bay."

from usina import *

logger = logging.getLogger("__main__")

class Bay(Usina):
    def __init__(self) -> ...:
        super().__init__(self)

        self.__tensao_fase_a = LeituraModbus(self.rele["BAY"], REG_RELE["BAY"]["TENSAO_FASE_A"], descricao="RELE_BAY_TENSAO_FASE_A")
        self.__tensao_fase_b = LeituraModbus(self.rele["BAY"], REG_RELE["BAY"]["TENSAO_FASE_B"], descricao="RELE_BAY_TENSAO_FASE_B")
        self.__tensao_fase_c = LeituraModbus(self.rele["BAY"], REG_RELE["BAY"]["TENSAO_FASE_C"], descricao="RELE_BAY_TENSAO_FASE_C")
        self.__tensao_vs = LeituraModbus(self.rele["BAY"], REG_RELE["BAY"]["TENSAO_VS"], descricao="RELE_BAY_TENSAO_VS")

        self._condicionadores = []
        self._condicionadores_essenciais = []

        self.iniciar_leituras_condicionadores()
    
    @property
    def tensao_fase_a(self) -> int:
        return self.__tensao_fase_a.valor
    
    @property
    def tensao_fase_b(self) -> int:
        return self.__tensao_fase_b.valor
    
    @property
    def tensao_fase_c(self) -> int:
        return self.__tensao_fase_c.valor
    
    @property
    def tensao_vs(self) -> int:
        return self.__tensao_vs.valor

    @property
    def condicionadores(self) -> "list[CondicionadorBase]":
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[CondicionadorBase]") -> None:
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[CondicionadorBase]":
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[CondicionadorBase]") -> None:
        self._condicionadores_essenciais = var


    def verificar_condicionadores(self) -> int:
        return

    def resetar_emergencia(self) -> bool:
        return

    def verificar_tensao_trifasica(self) -> bool:
        try:
            if (TENSAO_FASE_BAY_BAIXA < self.tensao_fase_a < TENSAO_FASE_BAY_ALTA) \
                and (TENSAO_FASE_BAY_BAIXA < self.tensao_fase_b < TENSAO_FASE_BAY_ALTA) \
                and (TENSAO_FASE_BAY_BAIXA < self.tensao_fase_c < TENSAO_FASE_BAY_ALTA):
                return True
            else:
                logger.warning("[BAY] Tensão trifásica fora do limite.")
                return False

        except Exception as e:
            logger.exception(f"[BAY] Houve um erro ao realizar a verificação da tensão trifásica. Exception: \"{repr(e)}\"")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False

    def verificar_status_DjBay(self) -> bool:
        try:
            if not self.dj_bay.valor:
                logger.warning("[BAY] O Disjuntor do Bay está aberto!")
                return False
            else:
                return True

        except Exception as e:
            logger.exception(f"[BAY] Houve um erro ao realizar a leitura do status do Disjuntor do Bay. Exception: \"{repr(e)}\"")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False

    def realizar_fechamento_DjBay(self) -> bool:
        flags = 0
        try:
            if self.se.dj_se.valor:
                logger.info("[BAY] O Disjuntor 52L da subestação está fechado! Acionando comando de abertura...")

                if not EscritaModBusBit.escrever_bit(self.clp["SA"], REG_CLP["SE"]["CMD_SE_ABRE_52L"], bit=1, valor=0):
                    logger.warning("[BAY] Não foi possível realizar a abertura do Disjuntor 52L da subestação!")
                    flags += 1

            if not self.mola_carregada.valor: 
                logger.warning("[BAY] A mola do Disjuntor está descarregada!")
                flags += 1

            if not self.secc_fechada.valor:
                logger.warning("[BAY] A seccionadora está aberta!")
                flags += 1

            if not self.barra_morta.valor and self.barra_viva.valor:
                logger.warning("[BAY] Foi identificada leitura de corrente na barra!")
                flags += 1

            if not self.linha_morta.valor and self.linha_viva.valor:
                logger.warning("[BAY] Foi identificada lietura de corrente na linha!")
                flags += 1

            logger.warning(f"[SE] Foram identificadas \"{flags}\" condições de bloqueio ao realizar fechamento do Disjuntor. Favor normalizar.") \
                if flags > 0 else logger.debug("[SE] Condições de fechamento Dj Bay OK! Fechando disjuntor...")

            return False if flags > 0 else True
        
        except Exception as e:
            logger.exception(f"[BAY] Houve um erro ao verificar as pré-condições de fechameto do Dijuntor do Bay. Exception: \"{repr(e)}\"")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False

    def iniciar_leituras_condicionadores(self) -> None:
        # Status Dijuntores
        self.dj_bay = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["DJ_LINHA_FECHADO"], bit=0, descricao="RELE_BAY_DJ_LINHA_FECHADO")
        
        # Pré-condições de fechamento do Disjuntor do Bay
        self.mola_carregada = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["DJ_MOLA_CARREGADA"], bit=1, descricao="RELE_BAY_MOLA_CARREGADA")
        self.secc_fechada = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["SECC_FECHADA"], bit=4, descricao="RELE_BAY_SECCIONADORA_FECHADA")
        self.barra_morta = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["ID_BARRA_MORTA"], bit=7, descricao="RELE_BAY_ID_BARRA_MORTA")
        self.barra_viva = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["ID_BARRA_VIVA"], bit=1, descricao="RELE_BAY_ID_BARRA_VIVA")
        self.linha_morta = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["ID_LINHA_MORTA"], bit=1, descricao="RELE_BAY_ID_LINHA_MORTA")
        self.linha_viva = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["ID_LINHA_VIVA"], bit=0, descricao="RELE_BAY_ID_LINHA_MORTA")

        ## CONDICIONADORES RELÉS
        self.leitura_secc_aberta = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["SECC_FECHADA"], bit=4, invertido=True, descricao="RELE_BAY_SECCIONADORA_ABERTA")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_secc_aberta, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_abertura_djl = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["FALHA_ABERTURA_DJL"], bit=1, descricao="RELE_BAY_FALHA_ABERTURA_DJL")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_falha_abertura_djl, CONDIC_INDISPONIBILIZAR))