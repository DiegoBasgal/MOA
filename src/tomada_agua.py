__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Tomada da Água."

import pytz
import logging
import traceback

import src.funcoes.leitura as lei
import src.conectores.banco_dados as bd
import src.funcoes.condicionadores as c
import src.conectores.servidores as serv

from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class TomadaAgua:

    # ATRIBUIÇÃO DE VARIÁVEIS

    clp = serv.Servidores.clp

    cfg: "dict" = {}

    bd: "bd.BancoDados" = None

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

        autor = 0

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

        cls.l_alm_01_04 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme01_04"], descricao="[TDA] Falha no CLP (Trip 86H UGs)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_04, CONDIC_NORMALIZAR))

        cls.l_alm_01_05 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme01_05"], descricao="[TDA] Falha Alimentação do CLP (Trip 86H UGs)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_05, CONDIC_NORMALIZAR))

        cls.l_alm_01_06 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme01_06"], descricao="[TDA] Falha Alimentação do CLP Temporizada")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_06, CONDIC_NORMALIZAR))

        cls.l_alm_22_00 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_00"], descricao="[TDA] Relé Falta de Fase CA Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_22_00, CONDIC_NORMALIZAR))

        cls.l_alm_22_03 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_03"], descricao="[TDA] UHTA01 - Pressão de Óleo Baixa")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_22_03, CONDIC_NORMALIZAR))

        cls.l_alm_22_04 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_04"], descricao="[TDA] UHTA01 - Pressão de Óleo Alta na Linha da Comporta 01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_22_04, CONDIC_NORMALIZAR))

        cls.l_alm_22_05 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_05"], descricao="[TDA] UHTA01 - Pressão de Óleo Alta na Linha da Comporta 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_22_05, CONDIC_NORMALIZAR))

        cls.l_alm_22_06 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_06"], descricao="[TDA] UHTA01 - Filtro de Retorno Sujo")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_22_06, CONDIC_NORMALIZAR))

        cls.l_alm_22_07 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_07"], descricao="[TDA] UHTA01 - Nível de Óleo Crítico")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_22_07, CONDIC_NORMALIZAR))

        cls.l_alm_22_08 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_08"], descricao="[TDA] UHTA01 - Nível de Óleo Alto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_22_08, CONDIC_NORMALIZAR))

        cls.l_alm_22_09 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_09"], descricao="[TDA] UHTA01 - Sobretemperatura do Óleo - Alarme")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_22_09, CONDIC_NORMALIZAR))

        cls.l_alm_22_10 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_10"], descricao="[TDA] UHTA01 - Sobretemperatura do Óleo - Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_22_10, CONDIC_NORMALIZAR))

        cls.l_alm_22_11 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_11"], descricao="[TDA] UHTA01 - Botão de Emergência Acionado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_22_11, CONDIC_NORMALIZAR))

        cls.l_alm_22_14 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_14"], descricao="[TDA] UHTA01 - Bomba de Óleo 01 - Falha no Acionamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_22_14, CONDIC_NORMALIZAR))

        cls.l_alm_22_15 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_15"], descricao="[TDA] UHTA01 - Bomba de Óleo 01 - Disjuntor QM1 Aberto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_22_15, CONDIC_NORMALIZAR))

        cls.l_alm_23_01 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_01"], descricao="[TDA] UHTA01 - Bomba de Óleo 02 - Falha no Acionamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_23_01, CONDIC_NORMALIZAR))

        cls.l_alm_23_02 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_02"], descricao="[TDA] UHTA01 - Bomba de Óleo 02 - Disjuntor QM2 Aberto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_23_02, CONDIC_NORMALIZAR))

        cls.l_alm_23_04 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_04"], descricao="[TDA] Comporta 01 - Falha na Abertura")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_23_04, CONDIC_NORMALIZAR))

        cls.l_alm_23_05 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_05"], descricao="[TDA] Comporta 01 - Falha no Fechamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_23_05, CONDIC_NORMALIZAR))

        cls.l_alm_23_06 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_06"], descricao="[TDA] Comporta 01 - Falha no Cracking")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_23_06, CONDIC_NORMALIZAR))

        cls.l_alm_23_07 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_07"], descricao="[TDA] Comporta 01 - Falha na Reposição")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_23_07, CONDIC_NORMALIZAR))

        cls.l_alm_23_08 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_08"], descricao="[TDA] Comporta 01 - Falha nos Sensores de Posição")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_23_08, CONDIC_NORMALIZAR))

        cls.l_alm_23_11 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_11"], descricao="[TDA] Comporta 02 - Falha na Abertura")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_23_11, CONDIC_NORMALIZAR))

        cls.l_alm_23_12 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_12"], descricao="[TDA] Comporta 02 - Falha no Fechamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_23_12, CONDIC_NORMALIZAR))

        cls.l_alm_23_13 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_13"], descricao="[TDA] Comporta 02 - Falha no Cracking")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_23_13, CONDIC_NORMALIZAR))

        cls.l_alm_23_14 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_14"], descricao="[TDA] Comporta 02 - Falha na Reposição")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_23_14, CONDIC_NORMALIZAR))

        cls.l_alm_23_15 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_15"], descricao="[TDA] Comporta 02 - Falha nos Sensores de Posição")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_23_15, CONDIC_NORMALIZAR))

        cls.l_alm_24_02 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_02"], descricao="[TDA] UHTA02 - Pressão de Óleo Baixa")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_24_02, CONDIC_NORMALIZAR))

        cls.l_alm_24_03 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_03"], descricao="[TDA] UHTA02 - Pressão de Óleo Alta na Linha da Comporta 03")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_24_03, CONDIC_NORMALIZAR))

        cls.l_alm_24_04 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_04"], descricao="[TDA] UHTA02 - Pressão de Óleo Alta na Linha da Comporta 04")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_24_04, CONDIC_NORMALIZAR))

        cls.l_alm_24_05 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_05"], descricao="[TDA] UHTA02 - Filtro de Retorno Sujo")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_24_05, CONDIC_NORMALIZAR))

        cls.l_alm_24_06 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_06"], descricao="[TDA] UHTA02 - Nível de Óleo Crítico")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_24_06, CONDIC_NORMALIZAR))

        cls.l_alm_24_07 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_07"], descricao="[TDA] UHTA02 - Nível de Óleo Alto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_24_07, CONDIC_NORMALIZAR))

        cls.l_alm_24_08 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_08"], descricao="[TDA] UHTA02 - Sobretemperatura do Óleo - Alarme")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_24_08, CONDIC_NORMALIZAR))

        cls.l_alm_24_09 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_09"], descricao="[TDA] UHTA02 - Sobretemperatura do Óleo - Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_24_09, CONDIC_NORMALIZAR))

        cls.l_alm_24_10 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_10"], descricao="[TDA] UHTA02 - Botão de Emergência Acionado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_24_10, CONDIC_NORMALIZAR))

        cls.l_alm_24_13 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_13"], descricao="[TDA] UHTA02 - Bomba de Óleo 01 - Falha no Acionamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_24_13, CONDIC_NORMALIZAR))

        cls.l_alm_24_14 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_14"], descricao="[TDA] UHTA02 - Bomba de Óleo 01 - Disjuntor QM3 Aberto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_24_14, CONDIC_NORMALIZAR))

        cls.l_alm_25_00 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_00"], descricao="[TDA] UHTA02 - Bomba de Óleo 02 - Falha no Acionamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_25_00, CONDIC_NORMALIZAR))

        cls.l_alm_25_01 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_01"], descricao="[TDA] UHTA02 - Bomba de Óleo 02 - Disjuntor QM4 Aberto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_25_01, CONDIC_NORMALIZAR))

        cls.l_alm_25_03 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_03"], descricao="[TDA] Comporta 03 - Falha na Abertura")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_25_03, CONDIC_NORMALIZAR))

        cls.l_alm_25_04 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_04"], descricao="[TDA] Comporta 03 - Falha no Fechamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_25_04, CONDIC_NORMALIZAR))

        cls.l_alm_25_05 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_05"], descricao="[TDA] Comporta 03 - Falha no Cracking")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_25_05, CONDIC_NORMALIZAR))

        cls.l_alm_25_06 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_06"], descricao="[TDA] Comporta 03 - Falha na Reposição")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_25_06, CONDIC_NORMALIZAR))

        cls.l_alm_25_07 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_07"], descricao="[TDA] Comporta 03 - Falha nos Sensores de Posição")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_25_07, CONDIC_NORMALIZAR))

        cls.l_alm_25_10 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_10"], descricao="[TDA] Comporta 04 - Falha na Abertura")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_25_10, CONDIC_NORMALIZAR))

        cls.l_alm_25_11 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_11"], descricao="[TDA] Comporta 04 - Falha no Fechamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_25_11, CONDIC_NORMALIZAR))

        cls.l_alm_25_12 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_12"], descricao="[TDA] Comporta 04 - Falha no Cracking")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_25_12, CONDIC_NORMALIZAR))

        cls.l_alm_25_13 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_13"], descricao="[TDA] Comporta 04 - Falha na Reposição")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_25_13, CONDIC_NORMALIZAR))

        cls.l_alm_25_14 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_14"], descricao="[TDA] Comporta 04 - Falha nos Sensores de Posição")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_25_14, CONDIC_NORMALIZAR))

        cls.l_alm_26_01 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_01"], descricao="[TDA] Sensor de Fumaça Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_26_01, CONDIC_NORMALIZAR))

        cls.l_alm_26_02 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_02"], descricao="[TDA] Sensor de Fumaça Desconectado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_26_02, CONDIC_NORMALIZAR))

        cls.l_alm_26_04 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_04"], descricao="[TDA] Sensor de Presença Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_26_04, CONDIC_NORMALIZAR))

        cls.l_alm_26_05 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_05"], descricao="[TDA] Sensor de Presença Inibido")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_26_05, CONDIC_NORMALIZAR))

        cls.l_alm_26_07 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_07"], descricao="[TDA] Erro de Leitura na entrada analógica da temperatura do Óleo da UHTA01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_26_07, CONDIC_NORMALIZAR))

        cls.l_alm_26_08 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_08"], descricao="[TDA] Erro de Leitura na entrada analógica do nível de óleo da UHTA01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_26_08, CONDIC_NORMALIZAR))

        cls.l_alm_26_09 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_09"], descricao="[TDA] Erro de Leitura na entrada analógica da temperatura do Óleo da UHTA02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_26_09, CONDIC_NORMALIZAR))

        cls.l_alm_26_10 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_10"], descricao="[TDA] Erro de Leitura na entrada analógica do nível de óleo da UHTA02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_26_10, CONDIC_NORMALIZAR))

        cls.l_alm_26_11 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_11"], descricao="[TDA] Erro de Leitura na entrada analógica da posição da comporta 01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_26_11, CONDIC_NORMALIZAR))

        cls.l_alm_26_12 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_12"], descricao="[TDA] Erro de Leitura na entrada analógica da posição da comporta 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_26_12, CONDIC_NORMALIZAR))

        cls.l_alm_26_13 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_13"], descricao="[TDA] Erro de Leitura na entrada analógica da posição da comporta 03")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_26_13, CONDIC_NORMALIZAR))

        cls.l_alm_26_14 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_14"], descricao="[TDA] Erro de Leitura na entrada analógica da posição da comporta 04")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_26_14, CONDIC_NORMALIZAR))

        cls.l_alm_27_00 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme27_00"], descricao="[TDA] Grade 01 Suja")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_27_00, CONDIC_NORMALIZAR))

        cls.l_alm_27_01 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme27_01"], descricao="[TDA] Grade 02 Suja")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_27_01, CONDIC_NORMALIZAR))

        cls.l_alm_27_02 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme27_02"], descricao="[TDA] Grade 03 Suja")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_27_02, CONDIC_NORMALIZAR))

        cls.l_alm_27_03 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme27_03"], descricao="[TDA] Grade 04 Suja")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_27_03, CONDIC_NORMALIZAR))

        return
