__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__description__ = "Este módulo corresponde a implementação da operação do BAY de comunicação."

import logging
import traceback
import threading

import src.subestacao as se

from time import time, sleep

from src.funcoes.leitura import *
from src.dicionarios.const import *
from src.funcoes.condicionadores import *

from src.conectores.servidores import Servidores
from src.funcoes.escrita import EscritaModBusBit as EMB

logger = logging.getLogger("logger")

class Bay:

    # ATRIBUIÇÃO DE VARIÁVEIS

    mp = Servidores.mp
    mr = Servidores.mr
    clp = Servidores.clp
    rele = Servidores.rele

    status_tensao: "int" = TENSAO_VERIFICAR

    tensao_vs = LeituraModbus(
        rele["BAY"],
        REG_RELE["BAY"]["LT_VS"],
        descricao="[BAY][RELE] Leitura Tensão VS"
    )
    tensao_vab = LeituraModbus(
        rele["BAY"],
        REG_RELE["BAY"]["LT_FASE_A"],
        escala=1000,
        descricao="[BAY][RELE] Leitura Tensão Fase A"
    )
    tensao_vbc = LeituraModbus(
        rele["BAY"],
        REG_RELE["BAY"]["LT_FASE_B"],
        escala=1000,
        descricao="[BAY][RELE] Leitura Tensão Fase B"
    )
    tensao_vca = LeituraModbus(
        rele["BAY"],
        REG_RELE["BAY"]["LT_FASE_C"],
        escala=1000,
        descricao="[BAY][RELE] Leitura Tensão Fase C"
    )
    dj_linha_bay = LeituraModbusBit(
        rele["BAY"],
        REG_RELE["BAY"]["DJL_FECHADO"],
        descricao="[BAY][RELE] Disjuntor Bay Status"
    )
    potencia_mp = LeituraModbus(
        mp,
        REG_MEDIDOR["LT_P_MP"],
        escala=1,
        op=3,
        descricao="[BAY][MP] Leitura Medidor Principal"
    )
    potencia_mr = LeituraModbus(
        mr,
        REG_MEDIDOR["LT_P_MR"],
        escala=0.001,
        op=3,
        descricao="[BAY][MP] Leitura Medidor Principal"
    )

    condicionadores: "list[CondicionadorBase]" = []
    condicionadores_ativos: "list[CondicionadorBase]" = []
    condicionadores_essenciais: "list[CondicionadorBase]" = []

    @classmethod
    def resetar_emergencia(cls) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = EMB.escrever_bit(cls.rele["BAY"], REG_RELE["BAY"]["RELE_RST_TRP"], valor=1)
            return res

        except Exception:
            logger.exception(f"[BAY] Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False

    @classmethod
    def fechar_dj_linha(cls) -> "int":
        """
        Função para acionar comando de fechamento do Disjuntor do BAY de comunicação.

        Verifica se o disjuntor do BAY está aberto. Caso esteja, chama o método de verificação
        de condições de fechamento. Caso não haja nenhum problema com a verificação, aciona o
        comando de fechamento, senão, avisa o operador da falha.
        Caso o Disjuntor já estja fechado, apenas registra nos LOGs e retorna.
        """

        try:
            if not cls.dj_linha_bay.valor:
                logger.info("[BAY] O Disjuntor do Bay está Aberto!")

                if cls.verificar_dj_linha():
                    logger.debug(f"[BAY] Enviando comando:                   \"FECHAR DISJUNTOR\"")
                    logger.debug("")
                    EMB.escrever_bit(cls.rele["BAY"], REG_RELE["BAY"]["DJL_CMD_FECHAR"], valor=1)
                    return True

                else:
                    logger.warning("[BAY] Não foi possível fechar do Disjuntor do BAY.")
                    logger.debug("")
                    return False

            else:
                return True

        except Exception:
            logger.exception(f"[BAY] Houve um erro ao realizar a leitura do status do Disjuntor do Bay.")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False

    @classmethod
    def verificar_dj_linha(cls) -> "bool":
        """
        Função para verificação de condições de fechamento do Disjuntor do BAY.

        Verifica se o Disjuntor da Subestação está fechado e caso esteja, aciona o comando de abertura.
        Logo em seguida, verifica as seguintes condições:
        - Se há ausência de tensão trifásica;
        - Se há presença de tensão VS;
        - Se a mola do Disjuntor está carregada;
        - Se a Seccionadora está fechada;
        - Se há qualquer leitura de corrente na barra (Barra Morta = False & Barra Viva = True);
        - Se há qualquer leitura de corrente na linha (Linha Morta = False & Linha Viva = True).
        Caso qualquer das condições acima retornar diferente do esperado, avisa o operador e impede o
        comando de fechamento do Disjuntor.
        """

        flags = 0
        logger.info("[BAY] Verificando Condições do Disjuntor BAY...")

        try:
            if not cls.secc_fechada.valor:
                logger.warning("[BAY] A Seccionadora está Aberta!")
                flags += 1

            if se.Subestacao.dj_linha_se.valor:
                logger.info("[BAY] Disjuntor da Subestação Fechado!")
                logger.debug(f"[BAY] Enviando comando:                   \"ABRIR DISJUNTOR SE\"")
                res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["DJL_CMD_ABRIR"], valor=1)

                if not res:
                    logger.warning("[BAY] Não foi possível realizar a abertura do Disjuntor de Linha da Subestação!")
                    flags += 1

            if not cls.barra_morta.valor and cls.barra_viva.valor:
                logger.warning(f"[BAY] Foi identificada uma Leitura de Tensão na Barra! Tensão VS -> {cls.tensao_vs.valor}")
                flags += 1

            if not cls.linha_morta.valor and cls.linha_viva.valor:
                logger.warning("[BAY] Foi identificada uma leitura de Tensão na linha!")
                flags += 1

            if not cls.mola_carregada.valor:
                logger.warning("[BAY] A mola do Disjuntor está descarregada!")
                flags += 1

            logger.warning(f"[BAY] Foram identificadas \"{flags}\" condições de bloqueio ao realizar fechamento do Disjuntor do BAY. Favor normalizar.") \
                if flags > 0 else logger.debug("[BAY] Condições de Fechamento Validadas.")

            return False if flags > 0 else True

        except Exception:
            logger.exception(f"[BAY] Houve um erro ao verificar as pré-condições de fechameto do Disjuntor do Bay.")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False

    @classmethod
    def verificar_tensao_trifasica(cls) -> "bool":
        """
        Função para verificação de Tensão trifásica na linha do BAY.
        """

        try:
            if (TENSAO_FASE_BAY_BAIXA < cls.tensao_vab.valor < TENSAO_FASE_BAY_ALTA) \
                and (TENSAO_FASE_BAY_BAIXA < cls.tensao_vbc.valor < TENSAO_FASE_BAY_ALTA) \
                and (TENSAO_FASE_BAY_BAIXA < cls.tensao_vca.valor < TENSAO_FASE_BAY_ALTA):
                return True
            else:
                logger.warning("[BAY] Tensão trifásica fora do limite.")
                return False

        except Exception:
            logger.exception(f"[BAY] Houve um erro ao realizar a verificação da tensão trifásica.")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False

    @classmethod
    def aguardar_tensao(cls) -> "bool":
        """
        Função para normalização após a queda de tensão da linha de transmissão.

        Primeiramente, caso haja uma queda, será chamada a função com o temporizador de
        espera com tempo pré-definido. Caso a tensão seja reestabelecida dentro do limite
        de tempo, é chamada a funcão de normalização da Usina. Se o temporizador passar do
        tempo, é chamada a função de acionamento de emergência e acionado tropedo de emergência
        por Voip.
        """

        if cls.status_tensao == TENSAO_VERIFICAR:
            cls.status_tensao = TENSAO_AGUARDO
            logger.debug("[BAY] Iniciando o temporizador de normalização da tensão na linha.")
            threading.Thread(target=lambda: cls.temporizar_tensao(600)).start()

        elif cls.status_tensao == TENSAO_REESTABELECIDA:
            logger.info("[BAY] Tensão na linha reestabelecida.")
            cls.status_tensao = TENSAO_VERIFICAR
            return True

        elif cls.status_tensao == TENSAO_FORA:
            logger.critical("[BAY] Não foi possível reestabelecer a tensão na linha. Acionando emergência")
            cls.status_tensao = TENSAO_VERIFICAR
            return False

        else:
            logger.debug("[BAY] A tensão na linha ainda está fora.")

    @classmethod
    def temporizar_tensao(cls, delay: "int") -> "None":
        """
        Função de temporizador para espera de normalização de tensão da linha de transmissão.
        """

        while time() <= time() + delay:
            if cls.verificar_tensao_trifasica():
                cls.status_tensao = TENSAO_REESTABELECIDA
                return
            sleep(time() - (time() - 15))
        cls.status_tensao = TENSAO_FORA

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
            if cls.condicionadores_ativos == []:
                logger.warning(f"[BAY] Foram detectados Condicionadores ativos no Bay!")

            else:
                logger.info(f"[BAY] Ainda há Condicionadores ativos no Bay!")

            for condic in condics_ativos:
                if condic in cls.condicionadores_ativos:
                    logger.debug(f"[BAY] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue
                else:
                    logger.warning(f"[BAY] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    cls.condicionadores_ativos.append(condic)

            logger.debug("")
            return condics_ativos

        else:
            cls.condicionadores_ativos = []
            return []

    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de leituras necesárias para a operação.
        """

        # Pré-condições de fechamento do Disjuntor do Bay
        cls.secc_fechada = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["SECC_FECHADA"], descricao="[BAY][RELE] Seccionadora Fechada")
        cls.linha_viva = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["ID_LINHA_VIVA"], descricao="[BAY][RELE] Identificação Linha Viva")
        cls.barra_viva = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["ID_BARRA_VIVA"], descricao="[BAY][RELE] Identificação Barra Viva")
        cls.linha_morta = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["ID_LINHA_MORTA"], descricao="[BAY][RELE] Identificação Linha Morta")
        cls.barra_morta = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["ID_BARRA_MORTA"], descricao="[BAY][RELE] Identificação Barra Morta")
        cls.mola_carregada = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["DJL_MOLA_CARREGADA"], descricao="[BAY][RELE] Disjuntor Mola Carregada")


        # TODO -> remover após testes do simulador
        cls.aux_sim = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["CONDIC"], descricao="[BAY][SIM] Trip Teste Simulador")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.aux_sim, CONDIC_NORMALIZAR))


        ## CONDICIONADORES RELÉS
        return
        cls.secc_aberta = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["SECC_FECHADA"], invertido=True, descricao="[BAY][RELE] Seccionadora Aberta")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.secc_aberta, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_abertura_dj = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["DJL_FLH_ABERTURA"], descricao="[BAY][RELE] Disjuntor Linha Falha Abertura")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.l_falha_abertura_dj, CONDIC_INDISPONIBILIZAR))