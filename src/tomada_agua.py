__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Tomada da Água."

import pytz
import logging
import traceback

import src.dicionarios.dict as d
import src.funcoes.leitura as lei
import src.funcoes.escrita as esc
import src.conectores.banco_dados as bd
import src.funcoes.condicionadores as c
import src.conectores.servidores as serv

from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class TomadaAgua:

    # ATRIBUIÇÃO DE VARIÁVEIS
    bd: "bd.BancoDados"=None
    clp = serv.Servidores.clp
    cfg: "dict" = {}

    nv_montante = lei.LeituraModbusFloat(
        clp["TDA"],
        REG_TDA["NV_MONTANTE_GRADE"],
        descricao="[TDA] Nível Montante"
    )
    nv_jusante = lei.LeituraModbusFloat(
        clp["TDA"],
        REG_TDA["NV_JUSANTE_GRADE"],
        descricao="[TDA] Nível Jusante Grade"
    )

    erro_nv: "float" = 0
    erro_nv_anterior: "float" = 0
    nv_montante_recente: "float" = 0
    nv_montante_anterior: "float" = 0

    aguardando_reservatorio: "bool" = False

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []


    @classmethod
    def atualizar_valores_montante(cls) -> "None":

        cls.nv_montante_recente = cls.nv_montante.valor if 820 < cls.nv_montante.valor < 825 else cls.nv_montante_recente
        cls.erro_nv_anterior = cls.erro_nv
        cls.erro_nv = cls.nv_montante_recente - cls.cfg["nv_alvo"]


    @classmethod
    def resetar_emergencia(cls) -> "bool":
        try:
            logger.info(f"[TDA] Enviando comando:                   \"RESET EMERGÊNCIA\"")
            res = esc.EscritaModBusBit.escrever_bit(cls.clp["TDA"], REG_TDA["CMD_RESET_GERAL"], valor=1)
            return res

        except Exception:
            logger.error(f"[TDA] Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(traceback.format_exc())


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
                logger.warning(f"[TDA] Foram detectados Condicionadores ativos na Subestação!")
            else:
                logger.info(f"[TDA] Ainda há Condicionadores ativos na Subestação!")

            for condic in condics_ativos:
                if condic in cls.condicionadores_ativos:
                    logger.debug(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue

                else:
                    logger.warning(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
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
        Função para consulta de acionamentos da usina e avisos através do mecanismo
        de acionamento temporizado.
        """
        return

        if cls.l_nv_montante_muito_baixo.valor:
            logger.warning("[TDA] Foi identificado que o Nível Montante está muito baixo, favor verificar.")

        if cls.l_nv_montante_baixo.valor:
            logger.warning("[TDA] Foi identificado que o Nível Montante está baixo, favor verificar.")

        if cls.l_nv_montante_muito_baixo.valor and not d.voip["NV_MONTANTE_GRADE_MUITO_BAIXO"][0]:
            logger.warning("[TDA] Foi identificado que o Nível Montante está Muito Baixo, favor verificar.")
            d.voip["NV_MONTANTE_GRADE_MUITO_BAIXO"][0] = True
        elif not cls.l_nv_montante_muito_baixo.valor and d.voip["NV_MONTANTE_GRADE_MUITO_BAIXO"][0]:
            d.voip["NV_MONTANTE_GRADE_MUITO_BAIXO"][0] = False


    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """
        return

        cls.l_nv_montante_baixo = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["NV_MONTANTE_GRADE_BAIXO"], descricao="[TDA] Nível Montante Baixo")
        cls.l_nv_montante_muito_baixo = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["NV_MONTANTE_GRADE_MUITO_BAIXO"], descricao="[TDA] Nível Montante Muito Baixo")