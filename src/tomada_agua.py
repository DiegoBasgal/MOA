__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Tomada da Água."

import logging
import traceback

import dicionarios.dict as dct

from condicionador import *
from funcoes.leitura import *

from usina import Usina
from conector import ClientesUsina as cli
from funcoes.escrita import EscritaModBusBit as EMB

logger = logging.getLogger("__main__")

class TomadaAgua(Usina):

    # ATRIBUIÇÃO DE VARIÁVEIS

    clp = cli.clp

    erro_nv: "float" = 0
    erro_nv_anterior: "float" = 0
    nv_montante_recente: "float" = 0
    nv_montante_anterior: "float" = 0

    condicionadores: "list[CondicionadorBase]" = []
    condicionadores_essenciais: "list[CondicionadorBase]" = []

    nv_montante: "LeituraModbus" = LeituraModbus(
        clp["TDA"],
        REG_CLP["TDA"]["NIVEL_MONTANTE"],
        descricao="[TDA] Leitura Nível Montante"
    )
    status_lg: "LeituraModbus" = LeituraModbus(
        clp["TDA"],
        REG_CLP["TDA"]["LG_OPERACAO_MANUAL"],
        descricao="[TDA] Status Limpa Grades"
    )
    status_vb: "LeituraModbus" = LeituraModbus(
        clp["TDA"],
        REG_CLP["TDA"]["VB_FECHANDO"],
        descricao="[TDA] Status Válvula Borboleta"
    )
    status_uh: "LeituraModbusBit" = LeituraModbusBit(
        clp["TDA"],
        REG_CLP["TDA"]["UH_UNIDADE_HIDRAULICA_DISPONIVEL"],
        bit=1,
        descricao="[TDA] Status Unidade Hidáulica"
    )

    @classmethod
    def resetar_emergencia(cls) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = EMB.escrever_bit(cls.clp["TDA"], REG_CLP["TDA"]["VB_CMD_RESET_FALHAS"], bit=0, valor=1)
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

        cls.nv_montante_recente = cls.nv_montante
        cls.erro_nv_anterior = cls.erro_nv
        cls.erro_nv = cls.nv_montante_recente - cls.cfg["nv_alvo"]

    @classmethod
    def controlar_reservatorio(cls) -> "int":
        """
        Função para controle de níveis do reservatório.

        Realiza a leitura de nível montante e determina qual condição entrar. Se
        o nível estiver acima do máximo, verifica se atingiu o Maximorum. Nesse
        caso é acionada a emergência da Usina, porém se for apenas vertimento,
        distribui a potência máxima para as Unidades.
        Caso a leitura retornar que o nível está abaixo do mínimo, verifica antes
        se atingiu o fundo do reservatório, nesse caso é acionada a emergência.
        Se o valor ainda estiver acima do nível de fundo, será distribuída a
        potência 0 para todas as Unidades e aciona a espera pelo nível.
        Caso a leitura esteja dentro dos limites normais, é chamada a função para
        calcular e distribuir a potência para as Unidades.
        """

        if cls.nv_montante >= cls.cfg["nv_maximo"]:
            logger.debug("[TDA] Nível montante acima do máximo.")

            if cls.nv_montante_recente >= NIVEL_MAXIMORUM:
                logger.critical(f"[TDA] Nivel montante ({cls.nv_montante_recente:3.2f}) atingiu o maximorum!")
                return NV_EMERGENCIA
            else:
                cls.controle_i = 0.5
                cls.controle_ie = 0.5
                cls.ajuste_potencia(cls.cfg["pot_maxima_usina"])

                for ug in cls.ugs:
                    ug.step()

        elif cls.nv_montante <= cls.cfg["nv_minimo"] and not cls.aguardando_reservatorio:
            logger.debug("[TDA] Nível montante abaixo do mínimo.")
            cls.aguardando_reservatorio = True
            cls.distribuir_potencia(0)

            for ug in cls.ugs:
                ug.step()

            if cls.nv_montante_recente <= NIVEL_FUNDO_RESERVATORIO:
                logger.critical(f"[TDA] Nivel montante ({cls.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                return NV_EMERGENCIA

        elif cls.aguardando_reservatorio:
            if cls.nv_montante >= cls.cfg["nv_alvo"]:
                logger.debug("[TDA] Nível montante dentro do limite de operação.")
                cls.aguardando_reservatorio = False

        else:
            cls.controle_potencia()

            for ug in cls.ugs:
                ug.step()

        return NV_NORMAL

    @classmethod
    def verificar_condicionadores(cls) -> "list[CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

        if True in (condic.ativo for condic in cls.condicionadores_essenciais):
            condics_ativos = [condic for condics in [cls.condicionadores_essenciais, cls.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            logger.warning("[TDA] Foram detectados condicionadores ativos!")
            [logger.info(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade]}\".") for condic in condics_ativos]
            logger.debug("")

            return condics_ativos
        else:
            return []

    @classmethod
    def verificar_leituras(cls) -> "None":
        """
        Função para verificação de leituras por acionamento temporizado.

        Verifica leituras específcas para acionamento da manuteção. As leituras são disparadas
        em períodos separados por um tempo pré-definido.
        """

        if not cls.leitura_filtro_limpo_uh.valor:
            logger.warning("[TDA] O filtro da UH da TDA está sujo. Favor realizar limpeza/troca.")

        if cls.leitura_nivel_jusante_comporta_1.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 1. Favor verificar.")

        if cls.leitura_nivel_jusante_comporta_2.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 2. Favor verificar.")

        if not cls.leitura_ca_com_tensao.valor:
            logger.warning("[TDA] Foi dentificado que o CA da tomada da água está sem tensão. Favor verificar.")

        if cls.leitura_lg_operacao_manual.valor:
            logger.warning("[TDA] Foi identificado que o Limpa Grades entrou em operação manual. Favor verificar.")

        if cls.leitura_nivel_jusante_grade_comporta_1.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 1. Favor verificar.")

        if cls.leitura_nivel_jusante_grade_comporta_2.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 2. Favor verificar.")

        if cls.leitura_falha_atuada_lg.valor and not dct.voip["LG_FALHA_ATUADA"][0]:
            logger.warning("[TDA] Foi identificado que o limpa grades está em falha. Favor verificar.")
            dct.voip["LG_FALHA_ATUADA"][0] = True
        elif not cls.leitura_falha_atuada_lg.valor and dct.voip["LG_FALHA_ATUADA"][0]:
            dct.voip["LG_FALHA_ATUADA"][0] = False

        if cls.leitura_falha_nivel_montante.valor and not dct.voip["FALHA_NIVEL_MONTANTE"][0]:
            logger.warning("[TDA] Houve uma falha na leitura de nível montante. Favor verificar.")
            dct.voip["FALHA_NIVEL_MONTANTE"][0] = True
        elif not cls.leitura_falha_nivel_montante.valor and dct.voip["FALHA_NIVEL_MONTANTE"][0]:
            dct.voip["FALHA_NIVEL_MONTANTE"][0] = False

    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """

        # CONDICIONADORES ESSENCIAIS
        # Normalizar
        cls.leitura_sem_emergencia_tda = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["SEM_EMERGENCIA"], bit=24, invertido=True, descricao="[TDA] Emergência")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_sem_emergencia_tda, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Normalizar
        cls.leitura_ca_com_tensao = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["COM_TENSAO_CA"], bit=11, invertido=True, descricao="[TDA] Tensão CA Status ")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_ca_com_tensao, CONDIC_NORMALIZAR))

        cls.leitura_falha_ligar_bomba_uh = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["UH_FALHA_LIGAR_BOMBA"], bit=2, descricao="[TDA] UHTDA Falha Ligar Bomba")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_falha_ligar_bomba_uh, CONDIC_NORMALIZAR))

        # LEITURA PERIÓDICA
        cls.leitura_falha_atuada_lg = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["LG_FALHA_ATUADA"], bit=31, descricao="[TDA] Limpa Grades Falha")
        cls.leitura_falha_nivel_montante = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["FALHA_NIVEL_MONTANTE"], bit=0, descricao="[TDA] Nível Montante Falha")
        cls.leitura_filtro_limpo_uh = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["UH_FILTRO_LIMPO"], bit=13, invertido=True, descricao="[TDA] UHTDA Filtro Sujo")
        cls.leitura_lg_operacao_manual = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["LG_OPERACAO_MANUAL"], bit=0, descricao="[TDA] Limpa Grades Operação Manual")
        cls.leitura_nivel_jusante_comporta_1 = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["NIVEL_JUSANTE_COMPORTA_1"], bit=2, descricao="[TDA] Nível Justante Comporta 1")
        cls.leitura_nivel_jusante_comporta_2 = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["NIVEL_JUSANTE_COMPORTA_2"], bit=4, descricao="[TDA] Nível Justante Comporta 2")
        cls.leitura_nivel_jusante_grade_comporta_1 = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_1"], bit=1, descricao="[TDA] Nível Justante Comporta 1 Falha")
        cls.leitura_nivel_jusante_grade_comporta_2 = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_2"], bit=3, descricao="[TDA] Nível Justante Comporta 2 Falha")
