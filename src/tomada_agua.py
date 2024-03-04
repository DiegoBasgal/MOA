__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Tomada da Água."

import pytz
import logging
import traceback

import src.dicionarios.dict as d
import src.funcoes.leitura as lei
import src.funcoes.condicionadores as c
import src.conectores.servidores as serv

from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *
from src.dicionarios.compartilhado import *


logger = logging.getLogger("logger")


class TomadaAgua:

    # ATRIBUIÇÃO DE VARIÁVEIS
    clp = serv.Servidores.clp

    dct_tda['nivel_montante'] = lei.LeituraModbus(
        clp["TDA"],
        REG_TDA["NV_BARRAGEM"],
        descricao="[TDA] Leitura Nível Montante",
        escala=0.001,
        fundo_escala=800,
    )


    @classmethod
    def atualizar_montante(cls) -> "None":
        """
        Função para atualizar valores anteriores de nível montante e erro de cálculo para
        cálculos futuros de ajuste de potência.
        """

        dct_tda['nivel_montante_anterior'] = dct_tda['nivel_montante'].valor
        dct_tda['erro_nivel_anterior'] = dct_tda['erro_nivel']
        dct_tda['erro_nivel'] = dct_tda['nivel_montante_anterior'] - dct_usn['CFG']["nv_alvo"]


    @classmethod
    def verificar_condicionadores(cls) -> "list[c.CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

        autor = 0

        if True in (condic.ativo for condic in dct_tda['condicionadores_essenciais']):
            condics_ativos = [condic for condics in [dct_tda['condicionadores_essenciais'], dct_tda['condicionadores']] for condic in condics if condic.ativo]

            logger.debug("")
            if dct_tda['condicionadores_ativos'] == []:
                logger.warning(f"[TDA] Foram detectados Condicionadores ativos na Tomada da Água!")
            else:
                logger.info(f"[TDA] Ainda há Condicionadores ativos na Tomada da Água!")

            for condic in condics_ativos:
                if condic in dct_tda['condicionadores_ativos']:
                    logger.debug(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue

                else:
                    logger.warning(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    dct_tda['condicionadores_ativos'].append(condic)
                    dct_usn['BD'].update_alarmes([
                        datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor == 0 else ""
                    ])

            logger.debug("")
            return condics_ativos

        else:
            dct_tda['condicionadores_ativos'] = []
            return []


    @classmethod
    def verificar_leituras(cls) -> "None":
        """
        Função para verificação de leituras por acionamento temporizado.

        Verifica leituras específcas para acionamento da manuteção. As leituras são disparadas
        em períodos separados por um tempo pré-definido.
        """

        if cls.l_alm_22_b_00.valor:
            logger.warning("[TDA] Foi identificada uma autação do Relé por Falta de Fase CA. Favor verificar.")

        if cls.l_alm_22_b_06.valor:
            logger.warning("[TDA] Foi identificado que o Filtro de Retorno da UHTA 01 está sujo. Favor verificar.")

        if cls.l_alm_22_b_07.valor:
            logger.warning("[TDA] Foi identificado que o Nível de Óleo da UHTA 01 está crítico. Favor verificar.")

        if cls.l_alm_22_b_09.valor:
            logger.warning("[TDA] Foi identificado um Alarme de Sobretemperatura do Óleo da UHTA 01. Favor verificar.")

        if cls.l_alm_22_b_14.valor:
            logger.warning("[TDA] Foi identificada uma Falha no Acionamento da Bomba de Óleo 01 da UHTA 01. Favor verificar.")

        if cls.l_alm_22_b_15.valor:
            logger.warning("[TDA] Foi identificado que o Disjunotr QM1 da UHTA 01 foi Aberto. Favor verificar.")

        if cls.l_alm_23_b_01.valor:
            logger.warning("[TDA] Foi identificada uma Falha no Acionamento da Bomba de Óleo 02 da UHTA 01. Favor verificar.")

        if cls.l_alm_23_b_02.valor:
            logger.warning("[TDA] Foi identificado que o Disjunotr QM2 da UHTA 01 foi Aberto. Favor verificar.")

        if cls.l_alm_24_b_05.valor:
            logger.warning("[TDA] Foi identificado que o Filtro de Retorno da UHTA 02 está sujo. Favor verificar.")

        if cls.l_alm_24_b_06.valor:
            logger.warning("[TDA] Foi identificado que o Nível de Óleo da UHTA 02 está crítico. Favor verificar.")

        if cls.l_alm_24_b_08.valor:
            logger.warning("[TDA] Foi identificado um Alarme de Sobretemperatura do Óleo da UHTA 02. Favor verificar.")

        if cls.l_alm_24_b_13.valor:
            logger.warning("[TDA] Foi identificada uma Falha no Acionamento da Bomba de Óleo 01 da UHTA 02. Favor verificar.")

        if cls.l_alm_22_b_14.valor:
            logger.warning("[TDA] Foi identificado que o Disjunotr QM3 da UHTA 02 foi Aberto. Favor verificar.")

        if cls.l_alm_25_b_00.valor:
            logger.warning("[TDA] Foi identificada uma Falha no Acionamento da Bomba de Óleo 02 da UHTA 02. Favor verificar.")

        if cls.l_alm_25_b_01.valor:
            logger.warning("[TDA] Foi identificado que o Disjunotr QM4 da UHTA 02 foi Aberto. Favor verificar.")

        if cls.l_alm_26_b_01.valor:
            logger.warning("[TDA] Foi identificada uma atuação do Sensor de Fumaça. Favor verificar.")

        if cls.l_alm_26_b_07.valor:
            logger.warning("[TDA] Foi identificado um erro de Leitura na Entrada Analógica da Temperatura do Óleo da UHTA 01. Favor verificar.")

        if cls.l_alm_26_b_08.valor:
            logger.warning("[TDA] Foi identificado um erro de Leitura na Entrada Analógica do Nível do Óleo da UHTA 01. Favor verificar.")

        if cls.l_alm_26_b_09.valor:
            logger.warning("[TDA] Foi identificado um erro de Leitura na Entrada Analógica da Temperatura do Óleo da UHTA 02. Favor verificar.")

        if cls.l_alm_26_b_10.valor:
            logger.warning("[TDA] Foi identificado um erro de Leitura na Entrada Analógica do Nível do Óleo da UHTA 02. Favor verificar.")

        if cls.l_alm_26_b_11.valor:
            logger.warning("[TDA] Foi identificado um erro de Leitura na Entrada Analógica da posição da Comporta 01. Favor verificar.")

        if cls.l_alm_26_b_12.valor:
            logger.warning("[TDA] Foi identificado um erro de Leitura na Entrada Analógica da posição da Comporta 02. Favor verificar.")

        if cls.l_alm_26_b_13.valor:
            logger.warning("[TDA] Foi identificado um erro de Leitura na Entrada Analógica da posição da Comporta 03. Favor verificar.")

        if cls.l_alm_26_b_14.valor:
            logger.warning("[TDA] Foi identificado um erro de Leitura na Entrada Analógica da posição da Comporta 04. Favor verificar.")


        if cls.l_uhta01_nv_oleo_ll.valor and not d.voip["UHTA01_NIVEL_OLEO_LL"][0]:
            logger.warning("[TDA] Foi identificado que o nível do Óleo da UHTA 1 está Muito Baixo. Favor verificar.")
            d.voip["UHTA01_NIVEL_OLEO_LL"][0] = True
        elif not cls.l_uhta01_nv_oleo_ll.valor and d.voip["UHTA01_NIVEL_OLEO_LL"][0]:
            d.voip["UHTA01_NIVEL_OLEO_LL"][0] = False

        if cls.l_uhta01_nv_oleo_hh.valor and not d.voip["UHTA01_NIVEL_OLEO_HH"][0]:
            logger.warning("[TDA] Foi identificado que o nível do Óleo da UHTA 1 está Muito Alto. Favor verificar.")
            d.voip["UHTA01_NIVEL_OLEO_HH"][0] = True
        elif not cls.l_uhta01_nv_oleo_hh.valor and d.voip["UHTA01_NIVEL_OLEO_HH"][0]:
            d.voip["UHTA01_NIVEL_OLEO_HH"][0] = False

        if cls.l_uhta01_temp_oleo_h.valor and not d.voip["UHTA01_TEMP_OLEO_H"][0]:
            logger.warning("[TDA] Foi identificado que a temperatura do Óleo da UHTA 1 está Alta. Favor verificar.")
            d.voip["UHTA01_TEMP_OLEO_H"][0] = True
        elif not cls.l_uhta01_temp_oleo_h.valor and d.voip["UHTA01_TEMP_OLEO_H"][0]:
            d.voip["UHTA01_TEMP_OLEO_H"][0] = False

        if cls.l_uhta01_temp_oleo_hh.valor and not d.voip["UHTA01_TEMP_OLEO_HH"][0]:
            logger.warning("[TDA] Foi identificado que a temperatura do Óleo da UHTA 1 está Muito Alta. Favor verificar.")
            d.voip["UHTA01_TEMP_OLEO_HH"][0] = True
        elif not cls.l_uhta01_temp_oleo_hh.valor and d.voip["UHTA01_TEMP_OLEO_HH"][0]:
            d.voip["UHTA01_TEMP_OLEO_HH"][0] = False

        if cls.l_uhta02_nv_oleo_ll.valor and not d.voip["UHTA02_NIVEL_OLEO_LL"][0]:
            logger.warning("[TDA] Foi identificado que o nível do Óleo da UHTA 2 está Muito Baixo. Favor verificar.")
            d.voip["UHTA02_NIVEL_OLEO_LL"][0] = True
        elif not cls.l_uhta02_nv_oleo_ll.valor and d.voip["UHTA02_NIVEL_OLEO_LL"][0]:
            d.voip["UHTA02_NIVEL_OLEO_LL"][0] = False

        if cls.l_uhta02_nv_oleo_hh.valor and not d.voip["UHTA02_NIVEL_OLEO_HH"][0]:
            logger.warning("[TDA] Foi identificado que o nível do Óleo da UHTA 2 está Muito Alto. Favor verificar.")
            d.voip["UHTA02_NIVEL_OLEO_HH"][0] = True
        elif not cls.l_uhta02_nv_oleo_hh.valor and d.voip["UHTA02_NIVEL_OLEO_HH"][0]:
            d.voip["UHTA02_NIVEL_OLEO_HH"][0] = False

        if cls.l_uhta02_temp_oleo_h.valor and not d.voip["UHTA02_TEMP_OLEO_H"][0]:
            logger.warning("[TDA] Foi identificado que a temperatura do Óleo da UHTA 2 está Alta. Favor verificar.")
            d.voip["UHTA02_TEMP_OLEO_H"][0] = True
        elif not cls.l_uhta02_temp_oleo_h.valor and d.voip["UHTA02_TEMP_OLEO_H"][0]:
            d.voip["UHTA02_TEMP_OLEO_H"][0] = False

        if cls.l_uhta02_temp_oleo_hh.valor and not d.voip["UHTA02_TEMP_OLEO_HH"][0]:
            logger.warning("[TDA] Foi identificado que a temperatura do Óleo da UHTA 2 está Muito Alta. Favor verificar.")
            d.voip["UHTA02_TEMP_OLEO_HH"][0] = True
        elif not cls.l_uhta02_temp_oleo_hh.valor and d.voip["UHTA02_TEMP_OLEO_HH"][0]:
            d.voip["UHTA02_TEMP_OLEO_HH"][0] = False

        if cls.l_pcta_falta_fase.valor and not d.voip["PCTA_FALTA_FASE"][0]:
            logger.warning("[TDA] Foi identificada uma falta de Fase no Painel da Tomada da Água. Favor verificar.")
            d.voip["PCTA_FALTA_FASE"][0] = True
        elif not cls.l_pcta_falta_fase.valor and d.voip["PCTA_FALTA_FASE"][0]:
            d.voip["PCTA_FALTA_FASE"][0] = False

        if (dct_tda['nivel_montante'].valor < dct_usn['CFG']["nv_minimo"]) and cls.l_pcta_modo_remoto.valor and not d.voip["PCTA_MODO_REMOTO"][0]:
            logger.warning("[TDA] Foi identificado que o Painel da Tomada da Água entrou em Modo Remoto. Favor verificar.")
            d.voip["PCTA_MODO_REMOTO"][0] = True
        elif not cls.l_pcta_modo_remoto.valor and d.voip["PCTA_MODO_REMOTO"][0]:
            d.voip["PCTA_MODO_REMOTO"][0] = False


    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """

        cls.l_alm_01_b_04 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme01_04"], descricao="[TDA] Falha no CLP (Trip 86H UGs)")
        dct_tda['condicionadores_essenciais'].append(c.CondicionadorBase(cls.l_alm_01_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_01_b_05 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme01_05"], descricao="[TDA] Falha Alimentação do CLP (Trip 86H UGs)")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_01_b_05, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_01_b_06 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme01_06"], descricao="[TDA] Falha Alimentação do CLP Temporizada")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_01_b_06, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_22_b_00 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_00"], descricao="[TDA] Relé Falta de Fase CA Atuado")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_22_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_22_b_03 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_03"], descricao="[TDA] UHTA01 - Pressão de Óleo Baixa")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_22_b_03, CONDIC_NORMALIZAR))


        # OS CONDICIONADORES DESSE BLOCO SÃO RELACIONADOS A UG1 E UG2
        cls.l_alm_22_b_04 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_04"], descricao="[TDA] UHTA01 - Pressão de Óleo Alta na Linha da Comporta 01")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_22_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_22_b_05 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_05"], descricao="[TDA] UHTA01 - Pressão de Óleo Alta na Linha da Comporta 02")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_22_b_05, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_22_b_06 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_06"], descricao="[TDA] UHTA01 - Filtro de Retorno Sujo")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_22_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_22_b_07 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_07"], descricao="[TDA] UHTA01 - Nível de Óleo Crítico")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_22_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_22_b_08 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_08"], descricao="[TDA] UHTA01 - Nível de Óleo Alto")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_22_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_22_b_09 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_09"], descricao="[TDA] UHTA01 - Sobretemperatura do Óleo - Alarme")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_22_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_22_b_14 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_14"], descricao="[TDA] UHTA01 - Bomba de Óleo 01 - Falha no Acionamento")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_22_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_22_b_15 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme22_15"], descricao="[TDA] UHTA01 - Bomba de Óleo 01 - Disjuntor QM1 Aberto")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_22_b_15, CONDIC_NORMALIZAR))

        cls.l_alm_23_b_01 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_01"], descricao="[TDA] UHTA01 - Bomba de Óleo 02 - Falha no Acionamento")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_23_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_23_b_02 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_02"], descricao="[TDA] UHTA01 - Bomba de Óleo 02 - Disjuntor QM2 Aberto")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_23_b_02, CONDIC_NORMALIZAR))

        # OS CONDICIONADORES DESSE BLOCO SÃO RELACIONADOS A UG1
        cls.l_alm_23_b_04 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_04"], descricao="[TDA] Comporta 01 - Falha na Abertura")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_23_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_23_b_05 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_05"], descricao="[TDA] Comporta 01 - Falha no Fechamento")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_23_b_05, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_23_b_06 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_06"], descricao="[TDA] Comporta 01 - Falha no Cracking")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_23_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_23_b_07 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_07"], descricao="[TDA] Comporta 01 - Falha na Reposição")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_23_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_23_b_08 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_08"], descricao="[TDA] Comporta 01 - Falha nos Sensores de Posição")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_23_b_08, CONDIC_NORMALIZAR))

        # OS CONDICIONADORES DESSE BLOCO SÃO RELACIONADOS A UG2
        cls.l_alm_23_b_11 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_11"], descricao="[TDA] Comporta 02 - Falha na Abertura")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_23_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_23_b_12 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_12"], descricao="[TDA] Comporta 02 - Falha no Fechamento")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_23_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_23_b_13 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_13"], descricao="[TDA] Comporta 02 - Falha no Cracking")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_23_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_23_b_14 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_14"], descricao="[TDA] Comporta 02 - Falha na Reposição")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_23_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_23_b_15 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme23_15"], descricao="[TDA] Comporta 02 - Falha nos Sensores de Posição")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_23_b_15, CONDIC_NORMALIZAR))

        # OS CONDICIONADORES DESSE BLOCO SÃO RELACIONADOS A UG3 E UG4
        cls.l_alm_24_b_02 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_02"], descricao="[TDA] UHTA02 - Pressão de Óleo Baixa")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_24_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_24_b_03 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_03"], descricao="[TDA] UHTA02 - Pressão de Óleo Alta na Linha da Comporta 03")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_24_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_24_b_04 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_04"], descricao="[TDA] UHTA02 - Pressão de Óleo Alta na Linha da Comporta 04")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_24_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_24_b_05 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_05"], descricao="[TDA] UHTA02 - Filtro de Retorno Sujo")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_24_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_24_b_06 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_06"], descricao="[TDA] UHTA02 - Nível de Óleo Crítico")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_24_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_24_b_07 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_07"], descricao="[TDA] UHTA02 - Nível de Óleo Alto")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_24_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_24_b_08 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_08"], descricao="[TDA] UHTA02 - Sobretemperatura do Óleo - Alarme")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_24_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_24_b_10 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_10"], descricao="[TDA] UHTA02 - Botão de Emergência Acionado")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_24_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_24_b_13 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_13"], descricao="[TDA] UHTA02 - Bomba de Óleo 01 - Falha no Acionamento")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_24_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_24_b_14 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme24_14"], descricao="[TDA] UHTA02 - Bomba de Óleo 01 - Disjuntor QM3 Aberto")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_24_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_25_b_00 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_00"], descricao="[TDA] UHTA02 - Bomba de Óleo 02 - Falha no Acionamento")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_25_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_25_b_01 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_01"], descricao="[TDA] UHTA02 - Bomba de Óleo 02 - Disjuntor QM4 Aberto")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_25_b_01, CONDIC_NORMALIZAR))

        # OS CONDICIONADORES DESSE BLOCO SÃO RELACIONADOS A UG3
        cls.l_alm_25_b_03 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_03"], descricao="[TDA] Comporta 03 - Falha na Abertura")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_25_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_25_b_04 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_04"], descricao="[TDA] Comporta 03 - Falha no Fechamento")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_25_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_25_b_05 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_05"], descricao="[TDA] Comporta 03 - Falha no Cracking")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_25_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_25_b_06 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_06"], descricao="[TDA] Comporta 03 - Falha na Reposição")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_25_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_25_b_07 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_07"], descricao="[TDA] Comporta 03 - Falha nos Sensores de Posição")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_25_b_07, CONDIC_NORMALIZAR))

        # OS CONDICIONADORES DESSE BLOCO SÃO RELACIONADOS A UG4
        cls.l_alm_25_b_10 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_10"], descricao="[TDA] Comporta 04 - Falha na Abertura")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_25_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_25_b_11 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_11"], descricao="[TDA] Comporta 04 - Falha no Fechamento")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_25_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_25_b_12 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_12"], descricao="[TDA] Comporta 04 - Falha no Cracking")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_25_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_25_b_13 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_13"], descricao="[TDA] Comporta 04 - Falha na Reposição")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_25_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_25_b_14 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme25_14"], descricao="[TDA] Comporta 04 - Falha nos Sensores de Posição")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_25_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_26_b_01 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_01"], descricao="[TDA] Sensor de Fumaça Atuado")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_26_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_26_b_02 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_02"], descricao="[TDA] Sensor de Fumaça Desconectado")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_26_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_26_b_04 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_04"], descricao="[TDA] Sensor de Presença Atuado")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_26_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_26_b_05 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_05"], descricao="[TDA] Sensor de Presença Inibido")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_26_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_26_b_07 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_07"], descricao="[TDA] Erro de Leitura na entrada analógica da temperatura do Óleo da UHTA01")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_26_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_26_b_08 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_08"], descricao="[TDA] Erro de Leitura na entrada analógica do nível de óleo da UHTA01")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_26_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_26_b_09 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_09"], descricao="[TDA] Erro de Leitura na entrada analógica da temperatura do Óleo da UHTA02")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_26_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_26_b_10 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_10"], descricao="[TDA] Erro de Leitura na entrada analógica do nível de óleo da UHTA02")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_26_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_26_b_11 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_11"], descricao="[TDA] Erro de Leitura na entrada analógica da posição da comporta 01")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_26_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_26_b_12 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_12"], descricao="[TDA] Erro de Leitura na entrada analógica da posição da comporta 02")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_26_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_26_b_13 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_13"], descricao="[TDA] Erro de Leitura na entrada analógica da posição da comporta 03")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_26_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_26_b_14 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme26_14"], descricao="[TDA] Erro de Leitura na entrada analógica da posição da comporta 04")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_26_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_27_b_00 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme27_00"], descricao="[TDA] Grade 01 Suja")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_27_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_27_b_01 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme27_01"], descricao="[TDA] Grade 02 Suja")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_27_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_27_b_02 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme27_02"], descricao="[TDA] Grade 03 Suja")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_27_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_27_b_03 = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["Alarme27_03"], descricao="[TDA] Grade 04 Suja")
        dct_tda['condicionadores'].append(c.CondicionadorBase(cls.l_alm_27_b_03, CONDIC_NORMALIZAR))


        ## MENSAGEIRO
        cls.l_uhta01_nv_oleo_ll = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["UHTA01_NIVEL_OLEO_LL"], descricao="[TDA] UHTA01 Nível do Óleo Muito Baixo")
        cls.l_uhta01_nv_oleo_hh = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["UHTA01_NIVEL_OLEO_HH"], descricao="[TDA] UHTA01 Nível do Óleo Muito Alto")
        cls.l_uhta01_temp_oleo_h = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["UHTA01_TEMP_OLEO_H"], descricao="[TDA] UHTA01 Temperatura do Óleo Alta")
        cls.l_uhta01_temp_oleo_hh = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["UHTA01_TEMP_OLEO_HH"], descricao="[TDA] UHTA01 Temperatura do Óleo Muito Alta")
        cls.l_uhta02_nv_oleo_ll = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["UHTA02_NIVEL_OLEO_LL"], descricao="[TDA] UHTA02 Nível do Óleo Muito Baixo")
        cls.l_uhta02_nv_oleo_hh = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["UHTA02_NIVEL_OLEO_HH"], descricao="[TDA] UHTA02 Nível do Óleo Muito Alto")
        cls.l_uhta02_temp_oleo_h = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["UHTA02_TEMP_OLEO_H"], descricao="[TDA] UHTA02 Temperatura do Óleo Alta")
        cls.l_uhta02_temp_oleo_hh = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["UHTA02_TEMP_OLEO_HH"], descricao="[TDA] UHTA02 Temperatura do Óleo Muito Alta")
        cls.l_pcta_falta_fase = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["PCTA_FALTA_FASE"], descricao="[TDA] Painel TDA Falta Fase")
        cls.l_pcta_modo_remoto = lei.LeituraModbusBit(cls.clp["TDA"], REG_TDA["PCTA_MODO_REMOTO"], descricao="[TDA] Painel TDA Modo Remoto")
