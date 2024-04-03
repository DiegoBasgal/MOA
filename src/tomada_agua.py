import pytz
import logging
import numpy as np

import src.dicionarios.dict as d
import src.funcoes.leitura as lei
import src.funcoes.condicionador as c
import src.conectores.servidores as srv
import src.conectores.banco_dados as bd

from time import sleep
from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class TomadaAgua:

    cfg = None
    clp = srv.Servidores.clp
    bd: "bd.BancoDados" = None

    erro_nv: "float" = 0
    ema_anterior: "float" = -1
    erro_nv_anterior: "float" = 0
    nv_montante_recente: "float" = 0
    nv_montante_anterior: "float" = 0

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_ativos: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []

    l_nivel_montante: "lei.LeituraModbus" = lei.LeituraModbus(
        clp["TDA"],
        REG_TDA["NV_ANTES_GRADE"],
        escala=0.0001,
        fundo_escala=400,
        op=4,
        descricao="[TDA] Nível Montante"
    )


    @staticmethod
    def get_time() -> "datetime":
        """
        Função para obter data e hora atual.
        """

        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    @classmethod
    def resetar_tda(cls) -> None:
        """
        Função para reset da Tomada da Água. Envia o comando de reset para o
        CLP - TDA.
        """

        if not d.glb["TDA_Offline"]:
            cls.clp["TDA"].write_single_coil(REG_TDA["CMD_RESET_GERAL"], [1])
            cls.clp["TDA"].write_single_coil(REG_TDA["CMD_DESAB_CTRL_NIVEL"], [1])
            cls.clp["TDA"].write_single_coil(REG_TDA["CMD_DESAB_RELIGA_52L"], [1])
        else:
            logger.debug("[USN] Não é possível resetar a TDA pois o CLP da TDA se encontra offline")


    @classmethod
    def calcular_ema_montante(cls, ema_anterior, periodo=40, smoothing=5, casas_decimais=5) -> "float":
        constante = smoothing / (1 + periodo)

        ema = cls.l_nivel_montante.valor * constante + ema_anterior * (1 - constante)
        ema = np.round(ema, casas_decimais)

        return ema


    @classmethod
    def atualizar_valores_montante(cls) -> "None":
        """
        Função para atualização de valores anteriores e erro de nível montante.
        """

        if cls.ema_anterior == -1:
            cls.ema_anterior = 0
            cls.nv_montante_recente = cls.l_nivel_montante.valor

        # Filtro para variações de nível abruptas, maiores do que 20 cm entre uma amostra e outra
        elif abs(cls.l_nivel_montante.valor - cls.nv_montante_recente) > 0.2:
            cls.nv_montante_recente = cls.l_nivel_montante.valor

        else:
            ema = cls.calcular_ema_montante(cls.nv_montante_recente)
            cls.nv_montante_recente = ema

        cls.erro_nv_anterior = cls.erro_nv
        cls.erro_nv = cls.nv_montante_recente - cls.cfg["nv_alvo"]


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
                logger.debug(f"[TDA] Foram detectados Condicionadores ativos na Subestação!")
            else:
                logger.debug(f"[TDA] Ainda há Condicionadores ativos na Subestação!")

            for condic in condics_ativos:
                # if condic.teste:
                #     logger.debug(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\", Obs.: \"TESTE\"")
                #     continue

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
                    autor += 1
                    sleep(1)

            logger.debug("")
            return condics_ativos

        else:
            cls.condicionadores_ativos = []
            return []


    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """
        return

        cls.l_trip_dj_52E_QCTA = lei.LeituraModbusCoil(cls.clp["TDA"], REG_SA["DJ_52E_TRIP"], descricao="[TDA] Trip Disjuntor 52E")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_trip_dj_52E_QCTA, CONDIC_INDISPONIBILIZAR))

        cls.l_trip_dj_52E_dj_saida = lei.LeituraModbusCoil(cls.clp["TDA"], REG_SA["DJ_52E_TRIP_DJ_SAIDA"], descricao="[TDA] Trip Disjuntor 52E Saída")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_trip_dj_52E_dj_saida, CONDIC_INDISPONIBILIZAR))

        # cls.l_falha_380VCA_dj_52E = lei.LeituraModbusCoil(cls.clp["TDA"], REG_SA["DJ_52E_FALHA_380VCA"], descricao="[TDA] Falha 380 VCA Disjuntor 52E")
        # cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_380VCA_dj_52E, CONDIC_INDISPONIBILIZAR))