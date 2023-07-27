__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__description__ = "Este módulo corresponde a implementação da operação do BAY de comunicação."

import logging
import traceback
import threading

from time import time, sleep

from funcoes.leitura import *
from dicionarios.const import *
from funcoes.condicionador import *

from usina import Usina
from subestacao import Subestacao as SE
from conectores.servidores import Servidores
from funcoes.escrita import EscritaModBusBit as EMB

logger = logging.getLogger("logger")

class Bay(Usina):

    # ATRIBUIÇÃO DE VARIÁVEIS

    clp = Servidores.clp
    rele = Servidores.rele

    tensao_vs = LeituraModbus(
        rele["BAY"],
        REG_RELE["BAY"]["LT_VS"],
        descricao="[BAY][RELE] Leitura Tensão VS"
    )
    tensao_vab = LeituraModbus(
        rele["BAY"],
        REG_RELE["BAY"]["LT_FASE_A"],
        descricao="[BAY][RELE] Leitura Tensão Fase A"
    )
    tensao_vbc = LeituraModbus(
        rele["BAY"],
        REG_RELE["BAY"]["LT_FASE_B"],
        descricao="[BAY][RELE] Leitura Tensão Fase B"
    )
    tensao_vca = LeituraModbus(
        rele["BAY"],
        REG_RELE["BAY"]["LT_FASE_C"],
        descricao="[BAY][RELE] Leitura Tensão Fase C"
    )
    dj_linha_bay = LeituraModbusBit(
        rele["SE"],
        REG_RELE["SE"]["DJL_FECHADO"],
        bit=0,
        descricao="[BAY][RELE] Disjuntor Bay Status"
    )
    potencia_medidor_usina = LeituraModbus(
        clp["SA"],
        999,
        escala=1,
        op=4
    )

    condicionadores: "list[CondicionadorBase]" = []
    condicionadores_essenciais: "list[CondicionadorBase]" = []

    @classmethod
    def resetar_emergencia(cls) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = cls.rele["BAY"].write_single_coil(REG_RELE["BAY"]["RELE_RST_TRP"], [1])
            return res

        except Exception:
            logger.exception(f"[BAY] Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False

    @classmethod
    def fechar_dj_linha(cls) -> "bool":
        """
        Função para acionar comando de fechamento do Disjuntor do BAY de comunicação.

        Verifica se o disjuntor do BAY está aberto. Caso esteja, chama o método de verificação
        de condições de fechamento. Caso não haja nenhum problema com a verificação, aciona o
        comando de fechamento, senão, avisa o operador da falha.
        Caso o Disjuntor já estja fechado, apenas registra nos LOGs e retorna.
        """

        try:
            if not cls.dj_linha_bay.valor:
                logger.info("[BAY] O Disjuntor do Bay está aberto! Realizando fechamento...")
                if cls.verificar_dj_linha():
                    EMB.escrever_bit(cls.rele["BAY"], REG_RELE["BAY"]["DJL_CMD_FECHAR"], bit=2, valor=1)
                    return True
                else:
                    logger.warning("[BAY] Não foi possível realizar o fechamento do Disjuntor do BAY.")
                    return False
            else:
                logger.debug("[BAY] O Disjuntor do BAY já está fechado.")
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
        logger.info("[BAY] Verificando condições de fechamento do Disjuntor do BAY...")

        try:
            if SE.dj_linha_se.valor:
                logger.info("[BAY] Disjuntor da Subestação fechado! Acionando comando de abertura...")

                if not EMB.escrever_bit(cls.clp["SA"], REG_CLP["SE"]["DJL_CMD_ABRIR"], bit=1, valor=0):
                    logger.warning("[BAY] Não foi possível realizar a abertura do Disjuntor de Linha da Subestação!")
                    flags += 1

            if not cls.verificar_tensao_trifasica():
                flags += 1

            if cls.tensao_vs.valor != 0:
                logger.warning("[BAY] Foi identificada uma leitura de Tensão VS!")
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

            logger.warning(f"[BAY] Foram identificadas \"{flags}\" condições de bloqueio ao realizar fechamento do Disjuntor do BAY. Favor normalizar.") \
                if flags > 0 else logger.debug("[BAY] Condições de fechamento Dj Bay OK! Fechando disjuntor...")

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
            logger.debug("[SE] Iniciando o timer para a normalização da tensão na linha.")
            threading.Thread(target=lambda: cls.temporizar_tensao(600)).start()

        elif cls.status_tensao == TENSAO_REESTABELECIDA:
            logger.info("[SE] Tensão na linha reestabelecida.")
            cls.status_tensao = TENSAO_VERIFICAR
            return True

        elif cls.status_tensao == TENSAO_FORA:
            logger.critical("[SE] Não foi possível reestabelecer a tensão na linha. Acionando emergência")
            cls.status_tensao = TENSAO_VERIFICAR
            return False

        else:
            logger.debug("[SE] A tensão na linha ainda está fora.")

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
            logger.info("[BAY] Foram detectados condicionadores ativos!")
            [logger.info(f"[BAY] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade]}\".") for condic in condics_ativos]
            logger.debug("")

            return condics_ativos
        else:
            return []

    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de leituras necesárias para a operação.
        """

        # Pré-condições de fechamento do Disjuntor do Bay
        cls.secc_fechada = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["SECC_FECHADA"], bit=4, descricao="[BAY][RELE] Seccionadora Fechada")
        cls.linha_viva = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["ID_LINHA_VIVA"], bit=0, descricao="[BAY][RELE] Identificação Linha Viva")
        cls.barra_viva = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["ID_BARRA_VIVA"], bit=1, descricao="[BAY][RELE] Identificação Barra Viva")
        cls.linha_morta = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["ID_LINHA_MORTA"], bit=1, descricao="[BAY][RELE] Identificação Linha Morta")
        cls.barra_morta = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["ID_BARRA_MORTA"], bit=7, descricao="[BAY][RELE] Identificação Barra Morta")
        cls.mola_carregada = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["DJL_MOLA_CARREGADA"], bit=1, descricao="[BAY][RELE] Disjuntor Mola Carregada")

        ## CONDICIONADORES RELÉS
        cls.leitura_secc_aberta = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["SECC_FECHADA"], bit=4, invertido=True, descricao="[BAY][RELE] Seccionadora Aberta")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_secc_aberta, CONDIC_INDISPONIBILIZAR))

        cls.leitura_falha_abertura_djl = LeituraModbusBit(cls.rele["BAY"], REG_RELE["BAY"]["DJL_FLH_ABERTURA"], bit=1, descricao="[BAY][RELE] Disjuntor Linha Falha Abertura")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_falha_abertura_djl, CONDIC_INDISPONIBILIZAR))