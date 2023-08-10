__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Tomada da Água."

import logging
import traceback

import src.dicionarios.dict as dct

from src.funcoes.leitura import *
from src.funcoes.condicionadores import *

from src.comporta import Comporta
from src.conectores.servidores import Servidores
from src.funcoes.escrita import EscritaModBusBit as EMB

logger = logging.getLogger("logger")

class TomadaAgua:

    # ATRIBUIÇÃO DE VARIÁVEIS

    clp = Servidores.clp

    cfg: "dict" = {}

    cp: "dict[str, Comporta]" = {}
    cp["CP1"] = Comporta(1)
    cp["CP2"] = Comporta(2)

    nivel_montante = LeituraModbus(
        clp["TDA"],
        REG_CLP["TDA"]["NV_MONTANTE"],
        descricao="[TDA] Leitura Nível Montante"
    )
    status_limpa_grades = LeituraModbus(
        clp["TDA"],
        REG_CLP["TDA"]["LG_OPE_MANUAL"],
        descricao="[TDA] Status Limpa Grades"
    )
    status_valvula_borboleta = LeituraModbus(
        clp["TDA"],
        REG_CLP["TDA"]["VB_FECHANDO"],
        descricao="[TDA] Status Válvula Borboleta"
    )
    status_unidade_hidraulica = LeituraModbusBit(
        clp["TDA"],
        REG_CLP["TDA"]["UH_DISPONIVEL"],
        descricao="[TDA] Status Unidade Hidáulica"
    )

    erro_nivel: "float" = 0
    erro_nivel_anterior: "float" = 0
    nivel_montante_anterior: "float" = 0

    condicionadores: "list[CondicionadorBase]" = []
    condicionadores_essenciais: "list[CondicionadorBase]" = []

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

        if cls.nivel_montante >= cls.cfg["nv_maximo"]:
            logger.debug("[TDA] Nível montante acima do máximo.")

            if cls.nivel_montante_anterior >= NIVEL_MAXIMORUM:
                logger.critical(f"[TDA] Nivel montante ({cls.nivel_montante_anterior:3.2f}) atingiu o maximorum!")
                return NV_EMERGENCIA
            else:
                cls.controle_i = 0.5
                cls.controle_ie = 0.5
                cls.ajuste_potencia(cls.cfg["pot_maxima_usina"])

                for ug in cls.ugs:
                    ug.step()

        elif cls.nivel_montante <= cls.cfg["nv_minimo"] and not cls.aguardando_reservatorio:
            logger.debug("[TDA] Nível montante abaixo do mínimo.")
            cls.aguardando_reservatorio = True
            cls.distribuir_potencia(0)

            for ug in cls.ugs:
                ug.step()

            if cls.nivel_montante_anterior <= NIVEL_FUNDO_RESERVATORIO:
                logger.critical(f"[TDA] Nivel montante ({cls.nivel_montante_anterior:3.2f}) atingiu o fundo do reservatorio!")
                return NV_EMERGENCIA

        elif cls.aguardando_reservatorio:
            if cls.nivel_montante >= cls.cfg["nv_alvo"]:
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
        cls.leitura_sem_emergencia_tda = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["SEM_EMERGENCIA"], invertido=True, descricao="[TDA] Emergência")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_sem_emergencia_tda, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Normalizar
        cls.leitura_ca_com_tensao = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["CA_COM_TENSAO"], invertido=True, descricao="[TDA] Tensão CA Status ")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_ca_com_tensao, CONDIC_NORMALIZAR))

        cls.leitura_falha_ligar_bomba_uh = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["UH_FLH_LIGAR_BOMBA"], descricao="[TDA] UHTDA Falha Ligar Bomba")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_falha_ligar_bomba_uh, CONDIC_NORMALIZAR))

        # LEITURA PERIÓDICA
        cls.leitura_falha_atuada_lg = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["LG_FLH_ATUADA"], descricao="[TDA] Limpa Grades Falha")
        cls.leitura_falha_nivel_montante = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["NV_MONTANTE_LER_FLH"], descricao="[TDA] Nível Montante Falha")
        cls.leitura_filtro_limpo_uh = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["UH_FILTRO_LIMPO"], invertido=True, descricao="[TDA] UHTDA Filtro Sujo")
        cls.leitura_lg_operacao_manual = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["LG_OPE_MANUAL"], descricao="[TDA] Limpa Grades Operação Manual")
        cls.leitura_nivel_jusante_comporta_1 = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_CP1"], descricao="[TDA] Nível Justante Comporta 1")
        cls.leitura_nivel_jusante_comporta_2 = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_CP2"], descricao="[TDA] Nível Justante Comporta 2")
        cls.leitura_nivel_jusante_grade_comporta_1 = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_GRADE_CP1_LER_FLH"], descricao="[TDA] Nível Justante Comporta 1 Falha")
        cls.leitura_nivel_jusante_grade_comporta_2 = LeituraModbusBit(cls.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_GRADE_CP2_LER_FLH"], descricao="[TDA] Nível Justante Comporta 2 Falha")
