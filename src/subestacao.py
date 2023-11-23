__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Subestação."

import pytz
import logging
import traceback
import threading

import src.funcoes.leitura as lei
import src.conectores.banco_dados as bd
import src.funcoes.condicionadores as c
import src.conectores.servidores as serv

from time import sleep, time
from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class Subestacao:

    # ATRIBUIÇÃO DE VARIÁVEIS

    bd: "bd.BancoDados" = None
    clp = serv.Servidores.clp

    tensao_r = lei.LeituraModbus(
        clp["SA"],
        REG_SE["TENSAO_RS"],
        escala=1000,
        descricao="[SE]  Tensão Fase U"
    )
    tensao_s = lei.LeituraModbus(
        clp["SA"],
        REG_SE["TENSAO_ST"],
        escala=1000,
        descricao="[SE]  Tensão Fase V"
    )
    tensao_t = lei.LeituraModbus(
        clp["SA"],
        REG_SE["TENSAO_TR"],
        escala=1000,
        descricao="[SE]  Tensão Fase W"
    )
    medidor_usina = lei.LeituraModbus(
        clp["SA"],
        REG_SE["POTENCIA_ATIVA_MEDIA"],
        descricao="[SE]  Leitura Medidor Usina"
    )
    dj_linha = lei.LeituraModbus(
        clp["SA"],
        REG_SE["STATUS_DJ52L"],
        descricao="[SE]  Status Disjuntor Linha"
    )

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []
    condicionadores_ativos: "list[c.CondicionadorBase]" = []


    @classmethod
    def fechar_dj_linha(cls) -> "int":
        """
        Função para acionamento do comando de fechamento do Disjuntor de Linha.

        Verifica se o Disjuntor de Linha está fechado e caso não estja, chama a função de verificação
        de condições de fechamento do Disjuntor. Caso retorne que o Disjuntor do BAY está aberto, sinaliza
        para a função de normalização da usina, que há a necessidade de realizar o fchamento do Disjuntor
        do BAY. Caso a verificação retorne que há uma falha com as condições, sinaliza que houve uma falha
        e impede o fechamento do Disjuntor. Caso o Disjuntor já esteja fechado, avisa o operador e retorna
        o sinal de fechamento OK.
        """

        try:
            if not cls.dj_linha.valor:
                logger.info("[SE]  O Disjuntor da Subestação está aberto!")

                if cls.verificar_dj_linha():
                    logger.debug(f"[SE]  Enviando comando:                   \"FECHAR DISJUNTOR\"")
                    logger.debug("")
                    cls.clp["SA"].write_single_register(REG_SE["CMD_FECHAR_DJ52L"], 1)
                    return True

                else:
                    logger.warning("[SE]  Não foi possível realizar o fechamento do Disjuntor.")
                    logger.debug("")
                    return False

            else:
                return True

        except Exception:
            logger.exception(f"[SE]  Houve um erro ao realizar o fechamento do Disjuntor de Linha.")
            logger.debug(traceback.format_exc())
            return False


    @classmethod
    def verificar_dj_linha(cls) -> "bool":
        """
        Função para verificação de condições de fechamento do Disjuntor de Linha.

        Verifica as seguintes condições:

        Caso qualquer das condições acima retornar diferente do esperado, avisa o operador e impede o
        comando de fechamento do Disjuntor.
        """

        flags = 0
        logger.debug("[SE]  Verificando Condições do Disjuntor SE...")

        try:
            flags += 1

            logger.warning(f"[SE]  Foram identificadas \"{flags}\" condições de bloqueio ao realizar fechamento do Disjuntor. Favor normalizar.") \
                if flags > 0 else logger.debug("[SE]  Condições de Fechamento Validadas.")

            return False if flags > 0 else True

        except Exception:
            logger.exception(f"[SE]  Houve um erro ao verificar as pré-condições de fechameto do Dijuntor de Linha.")
            logger.debug(traceback.format_exc())
            return False


    @classmethod
    def verificar_tensao_trifasica(cls) -> "bool":
        """
        Função para verificação de Tensão na linha da Subestação.
        """

        try:
            if (TENSAO_LINHA_BAIXA < cls.tensao_r.valor < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < cls.tensao_s.valor < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < cls.tensao_t.valor < TENSAO_LINHA_ALTA):
                return True

            else:
                logger.warning("[SE]  Tensão da linha fora do limite.")
                return False

        except Exception:
            logger.exception(f"[SE]  Houve um erro ao realizar a verificação da tensão na linha.")
            logger.debug(traceback.format_exc())
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
            threading.Thread(target=lambda: cls.temporizar_tensao(30)).start()

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
    def temporizar_tensao(cls, seg: "int") -> "None":
        """
        Função de temporizador para espera de normalização de tensão da linha de transmissão.
        """

        delay = time() + seg

        while time() <= delay:
            if cls.verificar_tensao_trifasica():
                cls.status_tensao = TENSAO_REESTABELECIDA
                return
            sleep(time() - (time() - 15))
        cls.status_tensao = TENSAO_FORA


    @classmethod
    def verificar_condicionadores(cls) -> "list[c.CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

        autor = 0

        if True in (condic.ativo for condic in cls.condicionadores_essenciais):
            condics_ativos = [condic for condics in [cls.condicionadores_essenciais, cls.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if cls.condicionadores_ativos == []:
                logger.warning(f"[SE]  Foram detectados Condicionadores ativos na Subestação!")

            else:
                logger.info(f"[SE]  Ainda há Condicionadores ativos na Subestação!")

            for condic in condics_ativos:
                if condic in cls.condicionadores_ativos:
                    logger.debug(f"[SE]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue

                else:
                    logger.warning(f"[SE]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    cls.condicionadores_ativos.append(condic)
                    cls.bd.update_alarmes([
                        datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor == 0 else ""
                    ])

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

    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """

        return