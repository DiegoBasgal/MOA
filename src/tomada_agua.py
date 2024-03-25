import pytz
import logging
import numpy as np

import src.dicionarios.dict as d
import src.funcoes.leitura as lei
import src.funcoes.condicionador as c
import src.conectores.servidores as srv
import src.conectores.banco_dados as bd

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
        fundo_de_escala=400,
        op=4,
        descr="[TDA] Nível Montante"
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
    def verificar_condicionadores(cls) -> "int":
        """
        Função para a verificação de acionamento de condicionadores e determinação
        de gravidade.

        Itera sobre a lista de condicionadores da Usina e verifica se algum está
        ativo. Caso esteja, verifica o nível de gravidade e retorna o valor para
        a determinação do passo seguinte.
        Caso não haja nenhum condicionador ativo, apenas retorna o valor de ignorar.
        """

        flag = CONDIC_IGNORAR
        autor_i = autor_n = 0

        if True in (condic.ativo for condic in cls.condicionadores_essenciais):
            condicionadores_ativos = [condic for condics in [cls.condicionadores_essenciais, cls.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            logger.warning(f"[TDA] Foram detectados condicionadores ativos na Usina!") if cls.condicionadores_ativos == [] else logger.info(f"[TDA] Ainda há condicionadores ativos na Usina!")

            for condic in condicionadores_ativos:
                if condic in cls.condicionadores_ativos:
                    logger.debug(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue

                elif condic.gravidade == CONDIC_INDISPONIBILIZAR:
                    logger.warning(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    cls.bd.update_alarmes([cls.get_time().strftime("%Y-%m-%d %H:%M:%S"), condic.gravidade, condic.descricao, "X" if autor_i == 0 else ""])
                    autor_i += 1

                elif condic.gravidade == CONDIC_NORMALIZAR:
                    logger.warning(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    cls.bd.update_alarmes([cls.get_time().strftime("%Y-%m-%d %H:%M:%S"), condic.gravidade, condic.descricao, "X" if autor_i == 0 and autor_n == 0 else ""])
                    autor_n += 1

                cls.condicionadores_ativos.append(condic)

                if flag == CONDIC_INDISPONIBILIZAR:
                    continue
                else:
                    flag = condic.gravidade

            logger.debug("")
            return flag

        else:
            cls.condicionadores_ativos = []
            return flag


    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """

        cls.l_trip_dj_52E_QCTA = lei.LeituraModbusCoil(cls.clp["TDA"], REG_SA["DJ_52E_TRIP"], descr="[TDA] Trip Disjuntor 52E")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_trip_dj_52E_QCTA, CONDIC_INDISPONIBILIZAR))

        cls.l_trip_dj_52E_dj_saida = lei.LeituraModbusCoil(cls.clp["TDA"], REG_SA["DJ_52E_TRIP_DJ_SAIDA"], descr="[TDA] Trip Disjuntor 52E Saída")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_trip_dj_52E_dj_saida, CONDIC_INDISPONIBILIZAR))

        # cls.l_falha_380VCA_dj_52E = lei.LeituraModbusCoil(cls.clp["TDA"], REG_SA["DJ_52E_FALHA_380VCA"], descr="[TDA] Falha 380 VCA Disjuntor 52E")
        # cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_380VCA_dj_52E, CONDIC_INDISPONIBILIZAR))