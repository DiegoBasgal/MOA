__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Tomada da Água."

import logging
import traceback

import src.dicionarios.dict as dct
import src.funcoes.condicionadores as c

from src.funcoes.leitura import *
from src.dicionarios.const import *

from src.comporta import Comporta
from src.conectores.servidores import Servidores
from src.funcoes.escrita import EscritaModBusBit as EMB

logger = logging.getLogger("logger")

class TomadaAgua:

    # ATRIBUIÇÃO DE VARIÁVEIS

    clp = Servidores.clp

    cfg: "dict" = {}
    aguardando_reservatorio: "int" = 0

    cp: "dict[str, Comporta]" = {}
    cp["CP1"] = Comporta(1)
    cp["CP2"] = Comporta(2)

    cp["CP1"].comporta_adjacente = cp["CP2"]
    cp["CP2"].comporta_adjacente = cp["CP1"]

    nivel_montante = LeituraModbus(
        clp['TDA'],
        REG_CLP["TDA"]["NV_MONTANTE"],
        descricao="[TDA] Leitura Nível Montante",
        escala=0.01
    )
    status_limpa_grades = LeituraModbusBit(
        clp["TDA"],
        REG_CLP["TDA"]["LG_OPE_MANUAL"],
        descricao="[TDA] Status Limpa Grades",
    )
    status_valvula_borboleta = LeituraModbusBit(
        clp["TDA"],
        REG_CLP["TDA"]["VB_FECHANDO"],
        descricao="[TDA] Status Válvula Borboleta",
    )
    status_unidade_hidraulica = LeituraModbusBit(
        clp["TDA"],
        REG_CLP["TDA"]["UH_DISPONIVEL"],
        descricao="[TDA] Status Unidade Hidáulica",
    )

    erro_nivel: "float" = 0
    erro_nivel_anterior: "float" = 0
    nivel_montante_anterior: "float" = 0

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []

    @classmethod
    def resetar_emergencia(cls) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = EMB.escrever_bit(cls.clp["TDA"], REG_CLP["TDA"]["VB_CMD_RST_FLH"], valor=1)
            return res

        except Exception:
            logger.error("[TDA] Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(f"[TDA] Traceback: {traceback.format_exc()}")

        return False

    @classmethod
    def atualizar_montante(cls) -> "None":
        """
        Função para atualizar valores anteriores de nível montante e erro de cálculo para
        cálculos futuros de ajuste de potência.
        """

        cls.nivel_montante_anterior = cls.nivel_montante.valor
        cls.erro_nivel_anterior = cls.erro_nivel
        cls.erro_nivel = cls.nivel_montante_anterior - cls.cfg["nv_alvo"]

    @classmethod
    def verificar_condicionadores(cls) -> "list[c.CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

        if True in (condic.ativo for condic in cls.condicionadores_essenciais):
            condics_ativos = [condic for condics in [cls.condicionadores_essenciais, cls.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if cls.condicionadores_ativos == []:
                logger.warning(f"[TDA] Foram detectados Condicionadores ativos na Tomada da Água!")

            else:
                logger.info(f"[TDA] Ainda há Condicionadores ativos na Tomada da Água!")

            for condic in condics_ativos:
                if condic in cls.condicionadores_ativos:
                    logger.debug(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue
                else:
                    logger.warning(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    cls.condicionadores_ativos.append(condic)

            logger.debug("")
            return condics_ativos

        else:
            cls.condicionadores_ativos = []
            return []

    @classmethod
    def verificar_leituras(cls) -> "None":
        """
        Função para verificação de leituras por acionamento temporizado.

        Verifica leituras específcas para acionamento da manuteção. As leituras são disparadas
        em períodos separados por um tempo pré-definido.
        """
        return

        if not cls.l_filtro_limpo_uh.valor:
            logger.warning("[TDA] O filtro da UH da TDA está sujo. Favor realizar limpeza/troca.")

        if cls.l_nvl_jusante_cp1.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 1. Favor verificar.")

        if cls.l_nv_jusante_cp2.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 2. Favor verificar.")

        if not cls.l_ca_tensao.valor:
            logger.warning("[TDA] Foi dentificado que o CA da tomada da água está sem tensão. Favor verificar.")

        if cls.l_lg_manual.valor:
            logger.warning("[TDA] Foi identificado que o Limpa Grades entrou em operação manual. Favor verificar.")

        if cls.l_nv_jusante_grade_cp1.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 1. Favor verificar.")

        if cls.l_nv_jusante_grade_cp2.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 2. Favor verificar.")

        if cls.l_falha_atuada_lg.valor and not dct.voip["LG_FALHA_ATUADA"][0]:
            logger.warning("[TDA] Foi identificado que o limpa grades está em falha. Favor verificar.")
            dct.voip["LG_FALHA_ATUADA"][0] = True
        elif not cls.l_falha_atuada_lg.valor and dct.voip["LG_FALHA_ATUADA"][0]:
            dct.voip["LG_FALHA_ATUADA"][0] = False

        if cls.l_falha_ler_nv_montante.valor and not dct.voip["FALHA_NIVEL_MONTANTE"][0]:
            logger.warning("[TDA] Houve uma falha na leitura de nível montante. Favor verificar.")
            dct.voip["FALHA_NIVEL_MONTANTE"][0] = True
        elif not cls.l_falha_ler_nv_montante.valor and dct.voip["FALHA_NIVEL_MONTANTE"][0]:
            dct.voip["FALHA_NIVEL_MONTANTE"][0] = False

    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """
        return
        # CONDICIONADORES ESSENCIAIS
        # Normalizar
        cls.l_sem_emergencia = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["SEM_EMERGENCIA"], invertido=True, descricao="[TDA] Emergência")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_sem_emergencia, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Normalizar
        cls.l_ca_tensao = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["CA_COM_TENSAO"], invertido=True, descricao="[TDA] Tensão CA Status ")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_ca_tensao, CONDIC_NORMALIZAR))

        cls.l_falha_ligar_bomba_uh = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["UH_FLH_LIGAR_BOMBA"], descricao="[TDA] UHTDA Falha Ligar Bomba")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_ligar_bomba_uh, CONDIC_NORMALIZAR))

        # LEITURA PERIÓDICA
        cls.l_falha_atuada_lg = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["LG_FLH_ATUADA"], descricao="[TDA] Limpa Grades Falha")
        cls.l_falha_ler_nv_montante = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["NV_MONTANTE_LER_FLH"], descricao="[TDA] Nível Montante Falha")
        cls.l_filtro_limpo_uh = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["UH_FILTRO_LIMPO"], invertido=True, descricao="[TDA] UHTDA Filtro Sujo")
        cls.l_lg_manual = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["LG_OPE_MANUAL"], descricao="[TDA] Limpa Grades Operação Manual")
        cls.l_nvl_jusante_cp1 = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_CP1"], descricao="[TDA] Nível Justante Comporta 1")
        cls.l_nv_jusante_cp2 = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_CP2"], descricao="[TDA] Nível Justante Comporta 2")
        cls.l_nv_jusante_grade_cp1 = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_GRADE_CP1_LER_FLH"], descricao="[TDA] Nível Justante Comporta 1 Falha")
        cls.l_nv_jusante_grade_cp2 = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_GRADE_CP2_LER_FLH"], descricao="[TDA] Nível Justante Comporta 2 Falha")
