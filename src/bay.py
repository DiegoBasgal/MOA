__version__ = "0.1"
__author__ = "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da operação do Bay."

import logging
import traceback

from condicionador import *
from funcoes.leitura import *
from dicionarios.const import *

from usina import Usina
from conector import ClientesUsina as cli
from funcoes.escrita import EscritaModBusBit as EMB

logger = logging.getLogger("__main__")

class Bay(Usina):

    clp = cli.clp
    rele = cli.rele

    tensao_fase_a: "LeituraModbus" = LeituraModbus(
        rele["BAY"],
        REG_RELE["BAY"]["TENSAO_FASE_A"],
        descricao="[BAY][RELE] Leitura Tensão Fase A"
    )
    tensao_fase_b: "LeituraModbus" = LeituraModbus(
        rele["BAY"],
        REG_RELE["BAY"]["TENSAO_FASE_B"],
        descricao="[BAY][RELE] Leitura Tensão Fase B"
    )
    tensao_fase_c: "LeituraModbus" = LeituraModbus(
        rele["BAY"],
        REG_RELE["BAY"]["TENSAO_FASE_C"],
        descricao="[BAY][RELE] Leitura Tensão Fase C"
    )
    tensao_vs: "LeituraModbus" = LeituraModbus(
        rele["BAY"],
        REG_RELE["BAY"]["TENSAO_VS"],
        descricao="[BAY][RELE] Leitura Tensão VS"
    )

    condicionadores: "list[CondicionadorBase]" = []
    condicionadores_essenciais: "list[CondicionadorBase]" = []

    @classmethod
    def resetar_emergencia(cls) -> "bool":
        return

    @classmethod
    def fechar_dj_bay(cls) -> "bool":
        flags = 0
        try:
            if cls.se.dj_se.valor:
                logger.info("[BAY] O Disjuntor de Linha da Subestação está fechado! Acionando comando de abertura...")

                if not EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["CMD_SE_ABRE_52L"], bit=1, valor=0):
                    logger.warning("[BAY] Não foi possível realizar a abertura do Disjuntor de Linha da Subestação!")
                    flags += 1

            if not cls.mola_carregada.valor: 
                logger.warning("[BAY] A mola do Disjuntor está descarregada!")
                flags += 1

            if not cls.secc_fechada.valor:
                logger.warning("[BAY] A Seccionadora está aberta!")
                flags += 1

            if not cls.barra_morta.valor and cls.barra_viva.valor:
                logger.warning("[BAY] Foi identificada uma leitura de corrente na barra!")
                flags += 1

            if not cls.linha_morta.valor and cls.linha_viva.valor:
                logger.warning("[BAY] Foi identificada uma leitura de corrente na linha!")
                flags += 1

            logger.warning(f"[BAY] Foram identificadas \"{flags}\" condições de bloqueio ao realizar fechamento do Disjuntor. Favor normalizar.") \
                if flags > 0 else logger.debug("[BAY] Condições de fechamento Dj Bay OK! Fechando disjuntor...")

            return False if flags > 0 else True
        
        except Exception:
            logger.exception(f"[BAY] Houve um erro ao verificar as pré-condições de fechameto do Dijuntor do Bay.")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False

    @classmethod
    def verificar_dj_bay(cls) -> "bool":
        try:
            if not cls.dj_bay.valor:
                logger.warning("[BAY] O Disjuntor do Bay está aberto!")
                return False
            else:
                return True

        except Exception:
            logger.exception(f"[BAY] Houve um erro ao realizar a leitura do status do Disjuntor do Bay.")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False

    @classmethod
    def verificar_tensao_trifasica(cls) -> "bool":
        try:
            if (TENSAO_FASE_BAY_BAIXA < cls.tensao_fase_a < TENSAO_FASE_BAY_ALTA) \
                and (TENSAO_FASE_BAY_BAIXA < cls.tensao_fase_b < TENSAO_FASE_BAY_ALTA) \
                and (TENSAO_FASE_BAY_BAIXA < cls.tensao_fase_c < TENSAO_FASE_BAY_ALTA):
                return True
            else:
                logger.warning("[BAY] Tensão trifásica fora do limite.")
                return False

        except Exception:
            logger.exception(f"[BAY] Houve um erro ao realizar a verificação da tensão trifásica.")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False
    
    @classmethod
    def verificar_condicionadores(cls) -> "list[CondicionadorBase]":
        if True in (condic.ativo for condic in cls.condicionadores_essenciais):
            condics_ativos = [condic for condics in [cls.condicionadores_essenciais, cls.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            logger.info("[BAY] Foram detectados condicionadores ativos!")
            [logger.info(f"[BAY] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade]}\".") for condic in condics_ativos]
            logger.debug("")

            return condics_ativos
        else:
            return []

    @classmethod
    def carregar_leituras(cls) -> "None":
        # Status Dijuntores
        cls.dj_bay = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["DJ_LINHA_FECHADO"], bit=0, descricao="[BAY][RELE] Disjuntor Bay Status")
        
        # Pré-condições de fechamento do Disjuntor do Bay
        cls.mola_carregada = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["DJ_MOLA_CARREGADA"], bit=1, descricao="[BAY][RELE] Disjuntor Mola Carregada")
        cls.secc_fechada = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["SECC_FECHADA"], bit=4, descricao="[BAY][RELE] Seccionadora Fechada")
        cls.barra_morta = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["ID_BARRA_MORTA"], bit=7, descricao="[BAY][RELE] Identificação Barra Morta")
        cls.barra_viva = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["ID_BARRA_VIVA"], bit=1, descricao="[BAY][RELE] Identificação Barra Viva")
        cls.linha_morta = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["ID_LINHA_MORTA"], bit=1, descricao="[BAY][RELE] Identificação Linha Morta")
        cls.linha_viva = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["ID_LINHA_VIVA"], bit=0, descricao="[BAY][RELE] Identificação Linha Viva")

        ## CONDICIONADORES RELÉS
        cls.leitura_secc_aberta = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["SECC_FECHADA"], bit=4, invertido=True, descricao="[BAY][RELE] Seccionadora Aberta")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_secc_aberta, CONDIC_INDISPONIBILIZAR))

        cls.leitura_falha_abertura_djl = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["FALHA_ABERTURA_DJL"], bit=1, descricao="[BAY][RELE] Disjuntor Linha Falha Abertura")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_falha_abertura_djl, CONDIC_INDISPONIBILIZAR))