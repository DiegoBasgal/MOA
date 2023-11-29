__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação do Serviço Auxiliar."

import pytz
import logging
import traceback

import src.funcoes.leitura as lei
import src.dicionarios.dict as dct
import src.conectores.banco_dados as bd
import src.funcoes.condicionadores as c
import src.conectores.servidores as serv

from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class ServicoAuxiliar:

    # ATRIBUIÇÃO DE VARIÁVEIS

    bd: "bd.BancoDados"=None

    clp = serv.Servidores.clp

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []


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
                logger.warning(f"[SA]  Foram detectados Condicionadores ativos no Serviço Auxiliar!")

            else:
                logger.info(f"[SA]  Ainda há Condicionadores ativos no Serviço Auxiliar!")

            for condic in condics_ativos:
                if condic in cls.condicionadores_ativos:
                    logger.debug(f"[SA]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue

                else:
                    logger.warning(f"[SA]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
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

        cls.l_alm_01_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme01_02"], descricao="[SA]  PDSA-CC - Falta Tensão Vcc Carregador de Baterias 01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_01_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme01_03"], descricao="[SA]  PDSA-CC - Falta Tensão Vcc Carregador de Baterias 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_01_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme01_07"], descricao="[SA]  PINV - Controlador Boost 01 - Sobretensão no Link 540Vcc")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_01_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme01_08"], descricao="[SA]  PINV - Controlador Boost 01 - Subtensão no Link 540Vcc")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_01_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme01_09"], descricao="[SA]  Compressor de AR - Pressão Baixa")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_01_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme01_10"], descricao="[SA]  Compressor de AR - Pressão Alta")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_01_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme01_11"], descricao="[SA]  PINV - Controlador Boost 01 - Sobre Disparo IGBT")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_01_b_15 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme01_15"], descricao="[SA]  PINV - Controlador Boost 01 - Sub Disparo IGBT")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_15, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme02_03"], descricao="[SA]  PINV - Controlador Boost 01 - Sobrecorrente no Link 125Vcc")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_03, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_02_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme02_06"], descricao="[SA]  PINV - Controlador Boost 01 - Subcorrente no Link 125Vcc")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme02_09"], descricao="[SA]  PINV - Controlador Boost 01 - Falha no Circuito de Potência")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme02_10"], descricao="[SA]  PINV - Controlador Boost 01 - Falha Acionamento Contator 1K2")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme02_14"], descricao="[SA]  PINV - Controlador Boost 01 - Falha na Pré-Carga")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_15 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme02_15"], descricao="[SA]  PINV - Controlador Boost 01 - Falha Acionamento Contator 1K1")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_15, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme03_09"], descricao="[SA]  Falta de Fase Fonte 01 (TSA-01)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme03_10"], descricao="[SA]  Falta de Fase Fonte 02 (TSA-02 ou Rede Celesc)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme03_11"], descricao="[SA]  Falta de Fase Fonte 03 (Grupo Diesel)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme03_12"], descricao="[SA]  Falha nas Fontes")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme03_13"], descricao="[SA]  Atenção Comandos em Modo Manual")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme03_14"], descricao="[SA]  Falta de Fase Fonte 04 (TSA-02)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_15 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme03_15"], descricao="[SA]  Falta de Fase Fonte 05 (Rede Celesc)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_15, CONDIC_NORMALIZAR))

        cls.l_alm_04_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme04_00"], descricao="[SA]  Atenção Quadro de Transferência em Modo Local")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_04_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_04_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme04_01"], descricao="[SA]  Trafo Auxiliar TSA-01 - Alarme Sobretemperatura do Enrolamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_04_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_04_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme04_02"], descricao="[SA]  Trafo Auxiliar TSA-01 - Trip Sobretemperatura do Enrolamento (Efetuar Troca Para o TSA-02)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_04_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_04_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme04_03"], descricao="[SA]  Trafo Auxiliar TSA-01 - Falha Relé Monitor de Temperatura")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_04_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_04_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme04_04"], descricao="[SA]  PINV - Controlador Boost 01 - Falha na Realimentação")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_04_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_04_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme04_05"], descricao="[SA]  Trafo Auxiliar TSA-02 - Alarme Sobretemperatura do Enrolamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_04_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_04_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme04_06"], descricao="[SA]  Trafo Auxiliar TSA-02 - Trip Sobretemperatura do Enrolamento (Efetuar Troca Para o TSA-01)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_04_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_04_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme04_07"], descricao="[SA]  Trafo Auxiliar TSA-02 - Falha Relé Monitor de Temperatura")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_04_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_04_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme04_08"], descricao="[SA]  PINV - Controlador Boost 02 - Sobretensão no Link 540Vcc")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_04_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_04_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme04_09"], descricao="[SA]  PINV - Controlador Boost 02 - Subtensão no Link 540Vcc")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_04_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme05_00"], descricao="[SA]  PINV - Controlador Boost 02 - Sobre Disparo IGBT")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme05_01"], descricao="[SA]  PINV - Controlador Boost 02 - Sub Disparo IGBT")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_15 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme05_15"], descricao="[SA]  PINV - Controlador Boost 02 - Sobrecorrente no Link 125Vcc")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_15, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_06_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme06_00"], descricao="[SA]  PINV - Controlador Boost 02 - Subcorrente no Link 125Vcc")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_06_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_06_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme06_01"], descricao="[SA]  PINV - Controlador Boost 02 - Falha no Circuito de Potência")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_06_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_06_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme06_02"], descricao="[SA]  PINV - Controlador Boost 02 - Falha Acionamento Contator 1K2")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_06_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_06_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme06_03"], descricao="[SA]  Carregador de Baterias 01 - Fuga Terra Polo Positivo ou Negativo")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_06_b_03, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_06_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme06_04"], descricao="[SA]  Carregador de Baterias 01 - Falha Alarme no Retificador")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_06_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_06_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme06_05"], descricao="[SA]  Carregador de Baterias 01 - Sub/Sobretensão Vcc")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_06_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_06_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme06_06"], descricao="[SA]  Carregador de Baterias 01 - Ausência de Tensão CA ou Tensão Baixa nas Baterias")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_06_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_06_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme06_07"], descricao="[SA]  PINV - Controlador Boost 02 - Falha na Pré-Carga")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_06_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_06_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme06_08"], descricao="[SA]  PINV - Controlador Boost 02 - Falha Acionamento Contator 1K1")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_06_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_06_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme06_09"], descricao="[SA]  PINV - Controlador Boost 02 - Falha na Realimentação")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_06_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_06_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme06_11"], descricao="[SA]  Carregador de Baterias 02 - Fuga Terra Polo Positivo ou Negativo")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_06_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_06_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme06_12"], descricao="[SA]  Carregador de Baterias 02 - Falha Alarme no Retificador")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_06_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_06_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme06_13"], descricao="[SA]  Carregador de Baterias 02 - Sub/Sobretensão Vcc")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_06_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_06_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme06_14"], descricao="[SA]  Carregador de Baterias 02 - Ausência de Tensão CA ou Tensão Baixa nas Baterias")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_06_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_07_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme07_01"], descricao="[SA]  Drenagem - Nível do Poço Alto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_07_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_07_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme07_02"], descricao="[SA]  Drenagem - Nível do Poço Muito Alto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_07_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_07_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme07_03"], descricao="[SA]  Drenagem - Nível do Poço Inundação ( Bloquio 86H nas UGs*)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_07_b_03, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_07_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme07_04"], descricao="[SA]  Drenagem - Falta Alimentação CA nos Relés de Nível")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_07_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_07_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme07_05"], descricao="[SA]  Drenagem - Bomba 01 Falha no Acionamento ")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_07_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_07_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme07_06"], descricao="[SA]  Drenagem - Bomba 02 Falha no Acionamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_07_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_07_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme07_07"], descricao="[SA]  Drenagem - Bomba 03 Falha no Acionamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_07_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_07_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme07_11"], descricao="[SA]  Injeção de Água no Selo Mecânico - Falha no Acionamento da Bomba 01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_07_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_07_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme07_12"], descricao="[SA]  Injeção de Água no Selo Mecânico - Falha no Acionamento da Bomba 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_07_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_07_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme07_13"], descricao="[SA]  Sistema de Água de Serviço - Falha no Acionamento da Bomba 01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_07_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_07_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme07_14"], descricao="[SA]  Sistema de Água de Serviço - Falha no Acionamento da Bomba 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_07_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_07_b_15 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme07_15"], descricao="[SA]  Sistema de Água de Serviço - Falha na Abertura da Válvula de Entrada do Filtro 01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_07_b_15, CONDIC_NORMALIZAR))

        cls.l_alm_08_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_00"], descricao="[SA]  Sistema de Água de Serviço - Falha no Fechamento da Válvula de Entrada do Filtro 01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_08_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_08_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_01"], descricao="[SA]  Sistema de Água de Serviço - Falha na Abertura da Válvula de Entrada do Filtro 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_08_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_08_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_02"], descricao="[SA]  Sistema de Água de Serviço - Falha no Fechamento da Válvula de Entrada do Filtro 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_08_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_08_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_03"], descricao="[SA]  Sistema de Água de Serviço - Falha na Abertura da Válvula de Entrada da Torre de Resfriamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_08_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_08_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_04"], descricao="[SA]  Sistema de Água de Serviço - Falha no Fechamento da Válvula de Entrada da Torre de Resfriamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_08_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_08_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_05"], descricao="[SA]  Sistema de Água de Serviço - Falha na Abertura da Válvula de Saída da Torre de Resfriamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_08_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_08_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_06"], descricao="[SA]  Sistema de Água de Serviço - Falha no Fechamento da Válvula de Saída da Torre de Resfriamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_08_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_08_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_07"], descricao="[SA]  Sistema de Água de Serviço - Botão de Emergência do Filtro 01 Acionado")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_alm_08_b_07, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_08_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_08"], descricao="[SA]  Sistema de Água de Serviço - Trip Disjuntor Filtro 01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_08_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_08_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_09"], descricao="[SA]  Sistema de Água de Serviço - Perda de Carga no Filtro 01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_08_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_08_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_10"], descricao="[SA]  Sistema de Água de Serviço - Falta de Fase CA no Filtro 01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_08_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_08_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_11"], descricao="[SA]  Sistema de Água de Serviço - Botão de Emergência do Filtro 02 Acionado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_08_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_08_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_12"], descricao="[SA]  Sistema de Água de Serviço - Trip Disjuntor Filtro 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_08_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_08_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_13"], descricao="[SA]  Sistema de Água de Serviço - Perda de Carga no Filtro 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_08_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_08_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme08_14"], descricao="[SA]  Sistema de Água de Serviço - Falta de Fase CA no Filtro 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_08_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_09_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme09_00"], descricao="[SA]  Sensor de Presença Sala Supervisório Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_09_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_09_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme09_01"], descricao="[SA]  Sensor de Presença Saída Cozinha Banheiro Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_09_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_09_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme09_02"], descricao="[SA]  Sensor de Presença Almoxarifado Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_09_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_09_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme09_03"], descricao="[SA]  Sensor de Presença Área de Montagem Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_09_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_09_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme09_04"], descricao="[SA]  Sensor de Presença Sala de Cubículos Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_09_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_09_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme09_09"], descricao="[SA]  PDSA-CA - Sensor de Fumaça Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_09_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_09_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme09_10"], descricao="[SA]  PDSA-CA - Sensor de Fumaça Desconectado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_09_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_09_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme09_11"], descricao="[SA]  PDSA-CC - Sensor de Fumaça Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_09_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_09_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme09_12"], descricao="[SA]  PDSA-CC - Sensor de Fumaça Desconectado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_09_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_10_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme10_00"], descricao="[SA]  PACP-SE - Alimentação Relés de Nível do Poço de Drenagem - Disj. Q220.1 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_10_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_10_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme10_01"], descricao="[SA]  PACP-SE - Alimentação Circuitos de Comando - Disj. Q125.0 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_10_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_10_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme10_02"], descricao="[SA]  PACP-SE - Alimentação Relé de Proteção 59N - Disj. Q125.1 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_10_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_10_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme10_03"], descricao="[SA]  PACP-SE - Alimentação Relés de Proteção SEL311C e SEL787 - Disj. Q125.2 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_10_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_10_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme10_04"], descricao="[SA]  PACP-SE - Alimentação Circuitos de Comando Seccionadora 89L - Disj. Q125.4 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_10_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_10_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme10_05"], descricao="[SA]  PACP-SE - Alimentação Circuito de Bloqueio Lâmina de Terra - Disj. Q125.5 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_10_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_10_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme10_06"], descricao="[SA]  PACP-SE - Alimentação Circuito de Comando Disjuntor 52L - Disj. Q125.6 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_10_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_10_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme10_07"], descricao="[SA]  PACP-SE - Alimentação Motor Carregamento da Mola do Disjuntor 52L - Disj. Q125.7 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_10_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_11_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_00"], descricao="[SA]  CSA-U1 - Alimentação Circuitos de Sinalização - Disj. Q125.0 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_11_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_01"], descricao="[SA]  CSA-U2 - Alimentação Circuitos de Sinalização - Disj. Q125.0 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_11_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_02"], descricao="[SA]  CB01 - Carregador de Baterias 01 - Disj. Q1/Q2/Q3 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_11_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_03"], descricao="[SA]  CB01 - Carregador de Baterias 01 - Disj. Q1/Q2/Q3 Inconsistência")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_11_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_04"], descricao="[SA]  CB01 - Carregador de Baterias 01 - Disj. Q1/Q2/Q3 Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_11_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_05"], descricao="[SA]  CB02 - Carregador de Baterias 02 - Disj. Q1/Q2/Q3 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_11_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_06"], descricao="[SA]  CB02 - Carregador de Baterias 02 - Disj. Q1/Q2/Q3 Inconsistência")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_11_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_07"], descricao="[SA]  CB02 - Carregador de Baterias 02 - Disj. Q1/Q2/Q3 Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_11_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_08"], descricao="[SA]  PDSA-CC - Alimentação Principal CB01 - Disj. Q125.E1 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_11_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_09"], descricao="[SA]  PDSA-CC - Alimentação Principal CB01 - Disj. Q125.E1 Inconsistência")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_11_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_10"], descricao="[SA]  PDSA-CC - Alimentação Principal CB01 - Disj. Q125.E1 Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_10, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_11_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_11"], descricao="[SA]  PDSA-CC - Alimentação Principal CB02 - Disj. Q125.E2 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_11_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_12"], descricao="[SA]  PDSA-CC - Alimentação Principal CB02 - Disj. Q125.E2 Inconsistência")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_11_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_13"], descricao="[SA]  PDSA-CC - Alimentação Principal CB02 - Disj. Q125.E2 Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_13, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_11_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_14"], descricao="[SA]  PDSA-CC - Alimentação Inversor 125Vcc/220Vca - Disj. Q125.1 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_14, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_11_b_15 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme11_15"], descricao="[SA]  PDSA-CC - Alimentação do Painel PDSA-CA - Disj. Q125.3 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_11_b_15, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_12_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme12_00"], descricao="[SA]  PDSA-CC - Alimentação do Rack de Comunicação - Disj. Q125.4 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_12_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_12_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme12_04"], descricao="[SA]  PDSA-CC - Alimentação Monitor de Temperatura do TSA-01 - Disj. Q125.8 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_12_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_12_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme12_05"], descricao="[SA]  PDSA-CC - Alimentação Monitor de Temperatura do TSA-02 - Disj. Q125.9 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_12_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_12_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme12_06"], descricao="[SA]  PDSA-CC - Alimentação Reserva - Disj. Q125.10 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_12_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_14_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme14_03"], descricao="[SA]  PDSA-CA - Alimentação Bomba Drenagem 01 - Disj. QM1 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_14_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_14_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme14_04"], descricao="[SA]  PDSA-CA - Alimentação Bomba Drenagem 02 - Disj. QM2 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_14_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_14_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme14_05"], descricao="[SA]  PDSA-CA - Alimentação Bomba Drenagem 03 - Disj. QM3 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_14_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_14_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme14_06"], descricao="[SA]  PDSA-CA - Alimentação da Bomba de Esgotamento - Disj. QM4 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_14_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_14_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme14_08"], descricao="[SA]  PDSA-CA - Alimentação 125Vcc Principal - Disj. Q125.0 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_14_b_08, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_14_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme14_09"], descricao="[SA]  PDSA-CA - Alimentação 380Vca Principal - Disj. Q380.0 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_14_b_09, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_14_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme14_10"], descricao="[SA]  PDSA-CA - Alimentação 380Vca Principal - Disj. Q380.0 Inconsistência")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_14_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_14_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme14_11"], descricao="[SA]  PDSA-CA - Alimentação 380Vca Principal - Disj. Q380.0 Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_14_b_11, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_14_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme14_12"], descricao="[SA]  PDSA-CA - Alimentação do Painel PCTA - Disj. Q380.1 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_14_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_14_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme14_13"], descricao="[SA]  PDSA-CA - Alimentação do Painel PCTA - Disj. Q380.1 Inconsistência")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_14_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_14_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme14_14"], descricao="[SA]  PDSA-CA - Alimentação do Painel PCTA - Disj. Q380.1 Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_14_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_14_b_15 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme14_15"], descricao="[SA]  PDSA-CA - Alimentação da Ponte Rolante - Disj. Q380.2 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_14_b_15, CONDIC_NORMALIZAR))

        cls.l_alm_15_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme15_00"], descricao="[SA]  PDSA-CA - Alimentação da Ponte Rolante - Disj. Q380.2 Inconsistência")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_15_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_15_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme15_01"], descricao="[SA]  PDSA-CA - Alimentação da Ponte Rolante - Disj. Q380.2 Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_15_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_15_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme15_02"], descricao="[SA]  PDSA-CA - Alimentação Monovia de Jusante - Disj. Q380.3 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_15_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_15_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme15_03"], descricao="[SA]  PDSA-CA - Alimentação do Quadro QDLCF - Disj. Q380.4 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_15_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_15_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme15_04"], descricao="[SA]  PDSA-CA - Alimentação do Quadro QDLCF - Disj. Q380.4 Inconsistência")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_15_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_15_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme15_05"], descricao="[SA]  PDSA-CA - Alimentação do Quadro QDLCF - Disj. Q380.4 Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_15_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_15_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme15_06"], descricao="[SA]  PDSA-CA - Alimentação do Elevador da Casa de Força - Disj. Q380.5 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_15_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_15_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme15_07"], descricao="[SA]  PDSA-CA - Alimentação do Painel PCAD - Disj. Q380.6 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_15_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_15_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme15_08"], descricao="[SA]  PDSA-CA - Alimentação Sistema de Retrolavagem do Filtro 01 - Disj. Q380.7 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_15_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_15_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme15_09"], descricao="[SA]  PDSA-CA - Alimentação Sistema de Retrolavagem do Filtro 02 - Disj. Q380.8 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_15_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_15_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme15_10"], descricao="[SA]  PDSA-CA - Alimentação do Carregador de Baterias 01 - Disj. Q380.9 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_15_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_15_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme15_11"], descricao="[SA]  PDSA-CA - Alimentação do Carregador de Baterias 02 - Disj. Q380.10 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_15_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_16_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme16_10"], descricao="[SA]  PDSA-CA - Alimentação Bomba 01 Injeção Água Selo Mecânico - Disj. QM5 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_16_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_16_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme16_11"], descricao="[SA]  PDSA-CA - Alimentação Bomba 02 Injeção Água Selo Mecânico - Disj. QM6 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_16_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_16_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme16_12"], descricao="[SA]  PDSA-CA - Alimentação Bomba 01 Água Serviço - Disj. QM7 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_16_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_16_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme16_13"], descricao="[SA]  PDSA-CA - Alimentação Bomba 02 Água Serviço - Disj. QM8 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_16_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_16_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme16_14"], descricao="[SA]  PDSA-CA - Alimentação UCP Bombas de Drenagem - Disj. Q220.11 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_16_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_16_b_15 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme16_15"], descricao="[SA]  PDSA-CA - Alimentação Torre de Resfriamento - Disj. Q380.11 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_16_b_15, CONDIC_NORMALIZAR))

        cls.l_alm_17_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme17_00"], descricao="[SA]  PDSA-CA - Alimentação Compressor de Ar - Disj. Q380.12 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_17_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_17_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme17_01"], descricao="[SA]  PDSA-CA - Alimentação do Guincho da Bomba de Esgotamento - Disj. Q380.13 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_17_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_17_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme17_02"], descricao="[SA]  PDSA-CA - Alimentação Alimentação do Quadro QDLSE - Disj. Q380.14 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_17_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_17_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme17_03"], descricao="[SA]  PACP-SE - Alimentação Válvulas Sistema de Água de Refrigeração -  Disj. Q125.8 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_17_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_17_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme17_04"], descricao="[SA]  PDSA-CC - Alimentação do Painel PINV - Disj. Q125.11 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_17_b_04, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_17_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme17_05"], descricao="[SA]  PINV - Alimentação Boost 01 - Disj. Q125.0 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_17_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_17_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme17_06"], descricao="[SA]  PINV - Alimentação Boost 02 - Disj. Q125.1 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_17_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_17_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme17_07"], descricao="[SA]  PINV - Alimentação Fonte 125/24Vcc (Ventilação Forçada e Switch) - Disj. Q125.2 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_17_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_17_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme17_09"], descricao="[SA]  Sistema de Água - Caixa D'Água 01 - Nível de água abaixo de 50%")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_17_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_17_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme17_10"], descricao="[SA]  Sistema de Água - Caixa D'Água 02 - Nível de água abaixo de 50%")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_17_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_17_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme17_11"], descricao="[SA]  PINV - Falha/Watchdog Controlador Boost 01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_17_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_17_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme17_12"], descricao="[SA]  PINV - Falha/Watchdog Controlador Boost 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_17_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_17_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme17_13"], descricao="[SA]  PINV - Falta Tensão 125Vcc")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_17_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_17_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme17_14"], descricao="[SA]  PINV - Fusível Entrada Link 125Vcc Aberto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_17_b_14, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_18_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme18_00"], descricao="[SA]  Erro de Leitura na entrada analógica do Nível de Jusante")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_18_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme18_01"], descricao="[SA]  Erro de Leitura na entrada analógica da Pressão do Sistema de Ar Comprimido")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_18_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme18_03"], descricao="[SA]  PACP-SE - Falha de Comunicação com o Controlador Boost 01 do PINV")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_18_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme18_06"], descricao="[SA]  PACP-SE - Falha de Comunicação com o Multimedidor MIB-7000C do Serviço Auxiliar")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_18_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme18_07"], descricao="[SA]  PACP-SE - Falha de Comunicação com o Grupo Diesel Ceraça ComAP")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_18_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme18_08"], descricao="[SA]  PACP-SE - Falha de Comunicação com o Carregador de Baterias 01 Modelo TPRe")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_18_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme18_09"], descricao="[SA]  PACP-SE - Falha de Comunicação com o Carregador de Baterias 02 Modelo TPRe")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_18_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme18_10"], descricao="[SA]  PACP-SE - Falha de Comunicação com o Controlador Boost 02 do PINV")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_18_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme18_11"], descricao="[SA]  Grupo Diesel - Nível de combustível menor que 30%")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_18_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme18_12"], descricao="[SA]  Grupo Diesel - Botão de Emergência Pressionado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme19_06"], descricao="[SA]  Carregador de Baterias 01 - Sobretensão Vca Entrada do Carregador")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme19_07"], descricao="[SA]  Carregador de Baterias 01 - Subtensão Vca Entrada do Carregador")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme19_08"], descricao="[SA]  Carregador de Baterias 01 - Alarme")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme19_09"], descricao="[SA]  Carregador de Baterias 01 - Sobretensão nas Baterias")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme19_10"], descricao="[SA]  Carregador de Baterias 01 - Subtensão nas Baterias")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme19_11"], descricao="[SA]  Carregador de Baterias 01 - Sobretensão Vcc Saída do Carregador")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme19_12"], descricao="[SA]  Carregador de Baterias 01 - Subtensão Vcc Saída do Carregador")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme19_13"], descricao="[SA]  Carregador de Baterias 01 - Fuga Terra - Positivo à Terra")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_13, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_19_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme19_14"], descricao="[SA]  Carregador de Baterias 01 - Fuga Terra - Negativo à Terra")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_14, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_20_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme20_06"], descricao="[SA]  Carregador de Baterias 02 - Sobretensão Vca Entrada do Carregador")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_20_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme20_07"], descricao="[SA]  Carregador de Baterias 02 - Subtensão Vca Entrada do Carregador")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_20_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme20_08"], descricao="[SA]  Carregador de Baterias 02 - Alarme")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_20_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme20_09"], descricao="[SA]  Carregador de Baterias 02 - Sobretensão nas Baterias")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_20_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme20_10"], descricao="[SA]  Carregador de Baterias 02 - Subtensão nas Baterias")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_20_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme20_11"], descricao="[SA]  Carregador de Baterias 02 - Sobretensão Vcc Saída do Carregador")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_20_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme20_12"], descricao="[SA]  Carregador de Baterias 02 - Subtensão Vcc Saída do Carregador")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_20_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme20_13"], descricao="[SA]  Carregador de Baterias 02 - Fuga Terra - Positivo à Terra")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_13, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_20_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme20_14"], descricao="[SA]  Carregador de Baterias 02 - Fuga Terra - Negativo à Terra")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_14, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_21_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme21_02"], descricao="[SA]  Torre de Resfriamento - Botão de Emergência Acionado")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_alm_21_b_02, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_21_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme21_03"], descricao="[SA]  Torre de Resfriamento - Trip Disjuntor Motor do Ventilador")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_21_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_21_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme21_06"], descricao="[SA]  Drenagem - Sem Fluxo de Água na Saída da Bomba 01 ")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_21_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_21_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme21_07"], descricao="[SA]  Drenagem - Sem Fluxo de Água na Saída da Bomba 02 ")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_21_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_21_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme21_08"], descricao="[SA]  Drenagem - Sem Fluxo de Água na Saída da Bomba 03  ")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_21_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_21_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme21_09"], descricao="[SA]  Injeção de Água no Selo Mecânico - Sem Fluxo de Água na Saída da Bomba 01 ")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_21_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_21_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme21_10"], descricao="[SA]  Injeção de Água no Selo Mecânico - Sem Fluxo de Água na Saída da Bomba 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_21_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_21_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme21_11"], descricao="[SA]  Sistema de Água de Serviço - Sem Fluxo de Água na Saída da Bomba 01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_21_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_21_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SA["Alarme21_12"], descricao="[SA]  Sistema de Água de Serviço - Sem Fluxo de Água na Saída da Bomba 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_21_b_12, CONDIC_NORMALIZAR))

        return