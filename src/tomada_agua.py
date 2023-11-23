__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Tomada da Água."

import logging
import traceback

import src.funcoes.leitura as lei
import src.funcoes.condicionadores as c
import src.conectores.servidores as serv

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class TomadaAgua:

    # ATRIBUIÇÃO DE VARIÁVEIS

    clp = serv.Servidores.clp

    cfg: "dict" = {}
    aguardando_reservatorio: "int" = 0

    nivel_montante = lei.LeituraModbus(
        clp["TDA"],
        REG_TDA["NV_BARRAGEM"],
        descricao="[TDA] Leitura Nível Montante",
        escala=0.01
    )

    erro_nivel: "float" = 0
    erro_nivel_anterior: "float" = 0
    nivel_montante_anterior: "float" = 0

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []


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

    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """
        return
