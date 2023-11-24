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
        descricao="[SE]  Tensão Fase RS"
    )
    tensao_s = lei.LeituraModbus(
        clp["SA"],
        REG_SE["TENSAO_ST"],
        escala=1000,
        descricao="[SE]  Tensão Fase ST"
    )
    tensao_t = lei.LeituraModbus(
        clp["SA"],
        REG_SE["TENSAO_TR"],
        escala=1000,
        descricao="[SE]  Tensão Fase TR"
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
            logger.debug("[SE]  Iniciando o temporizador de normalização da tensão na linha.")
            threading.Thread(target=lambda: cls.temporizar_tensao(30)).start()

        elif cls.status_tensao == TENSAO_REESTABELECIDA:
            logger.info("[SE]  Tensão na linha reestabelecida.")
            cls.status_tensao = TENSAO_VERIFICAR
            return True

        elif cls.status_tensao == TENSAO_FORA:
            logger.critical("[SE]  Não foi possível reestabelecer a tensão na linha. Acionando emergência")
            cls.status_tensao = TENSAO_VERIFICAR
            return False

        else:
            logger.debug("[SE]  A tensão na linha ainda está fora.")


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

        cls.l_alm_01_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme01_00"], descricao="[SE]  PACP - Botão de Emergência Pressionado (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_01_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme01_01"], descricao="[SE]  Emergência Supervisório Pressionada (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_01_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme01_12"], descricao="[SE]  Relé de Proteção SEL787 - TRIP")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_01_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme01_13"], descricao="[SE]  Relé de Proteção SEL787 - Falha 50/62BF")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_01_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme01_14"], descricao="[SE]  Relé de Proteção SEL787 - Falha de Hardware")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_00"], descricao="[SE]  Relé de Proteção SEL311C - TRIP")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_01"], descricao="[SE]  Relé de Proteção SEL311C - Falha 50/62BF")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_02"], descricao="[SE]  Relé de Proteção SEL311C - Falha de Hardware")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_04"], descricao="[SE]  Relé de Proteção 59N - Alarme")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_05"], descricao="[SE]  Relé de Proteção 59N - Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_07"], descricao="[SE]  Relé de Bloqueio 86BF (Falha Disjuntor) - Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_08"], descricao="[SE]  Relé de Bloqueio 86TE (Proteções do Trafo Elevador) - Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_11"], descricao="[SE]  Seccionadora 89L - Lâmina de Terra Fechada")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_12"], descricao="[SE]  Seccionadora 89L - Lâmina de Terra Bloqueada")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_13"], descricao="[SE]  Seccionadora 89L - Atenção! Chave em Modo Local")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_00"], descricao="[SE]  Disjuntor 52L - Falha na Abertura")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_01"], descricao="[SE]  Disjuntor 52L - Falha no Fechamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_02"], descricao="[SE]  Disjuntor 52L - Inconsistência Status Aberto/Fechado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_03"], descricao="[SE]  Disjuntor 52L - Falta Tensão Vcc")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_04"], descricao="[SE]  Disjuntor 52L - Mola Descarregada")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_05"], descricao="[SE]  Disjuntor 52L - Alarme Pressão Baixa Gás SF6")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_06"], descricao="[SE]  Disjuntor 52L - Trip Pressão Baixa Gás SF6 ( Impedimento do Fechamento 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_07"], descricao="[SE]  Disjuntor 52L - Atenção! Chave em Modo Local")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_08"], descricao="[SE]  Disjuntor 52L - Falha no Circuito do Motor de Carregamento da Mola")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_02"], descricao="[SE]  Trafo Elevador - Alarme Relé Buchholz")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_03"], descricao="[SE]  Trafo Elevador - Trip Relé Buchholz Bloqueio (Bloqueio 86TE)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_04"], descricao="[SE]  Trafo Elevador - Trip Nível de Óleo Baixo (Bloqueio 86TE)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_05"], descricao="[SE]  Trafo Elevador - Alarme Nível de Óleo Alto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_06"], descricao="[SE]  Trafo Elevador - Alarme Sobretemperatura do Óleo")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_07"], descricao="[SE]  Trafo Elevador - Trip Sobretemperatura do Óleo (Bloqueio 86TE)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_08"], descricao="[SE]  Trafo Elevador - Alarme Sobretemperatura do Enrolamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_09"], descricao="[SE]  Trafo Elevador - Trip Sobretemperatura do Enrolamento (Bloqueio 86TE)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_10"], descricao="[SE]  Trafo Elevador - Alarme Válvula de Alívio de Pressão")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_11"], descricao="[SE]  Trafo Elevador - Trip Válvula de Alívio de Pressão (Bloqueio 86TE)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_12"], descricao="[SE]  Trafo Elevador - Falha Relé Monitor de Temperatura")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_13"], descricao="[SE]  Trafo Elevador - Trip Pressão Súbita (Bloqueio 86TE)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_14"], descricao="[SE]  Trafo Elevador - Falha Ventilação Forçada")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_09_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme09_07"], descricao="[SE]  PACP-SE - Sensor de Fumaça Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_09_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_09_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme09_08"], descricao="[SE]  PACP-SE - Sensor de Fumaça Desconectado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_09_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_12_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme12_03"], descricao="[SE]  PDSA-CC - Alimentação Painel do Trafo Elevador - Disj. Q125.7 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_12_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_14_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme14_07"], descricao="[SE]  PDSA-CA - Alimentação do Painel PACP-SE - Disj. Q220.6 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_14_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_16_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme16_04"], descricao="[SE]  Disjuntor 52L - Alimentação Motor de Carregamento da Mola - Disj. F1 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_16_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_16_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme16_05"], descricao="[SE]  Disjuntor 52L - Alimentação Circuito de Aquecimento - Disj. F2 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_16_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_16_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme16_06"], descricao="[SE]  Seccionadora 89L - Alimentação Circuito de Comando - Disj. F1 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_16_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_16_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme16_07"], descricao="[SE]  Seccionadora 89L - Alimentação Motor de Acionamento - Disj. F3 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_16_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_16_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme16_08"], descricao="[SE]  Seccionadora 89L - Alimentação Motor de Acionamento  - Disj. F3 Inconsistência")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_16_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_16_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme16_09"], descricao="[SE]  Seccionadora 89L - Alimentação Motor de Acionamento  - Disj. F3 Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_16_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_18_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme18_04"], descricao="[SE]  PACP-SE - Falha de Comunicação com o Relé de Proteção SEL311C")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_18_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme18_05"], descricao="[SE]  PACP-SE - Falha de Comunicação com o Relé de Proteção SEL787")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_18_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme18_13"], descricao="[SE]  Relé de Proteção SEL311C - Sobrecorrente Temporizada de Fase (51P) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_18_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme18_14"], descricao="[SE]  Relé de Proteção SEL311C - Sobrecorrente Residual Temporizada (51G) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_18_b_15 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme18_15"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Fase Zona 01 (21P_Z1) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_15, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme19_00"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Fase Zona 02 (21P_Z2) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme19_01"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Fase Zona 03 Reversa (21P_Z3R) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme19_02"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Neutro Zona 01 (21N_Z1) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme19_03"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Neutro Zona 02 (21N_Z2) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme19_04"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Neutro Zona 03 Reversa (21N_Z3R) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme19_05"], descricao="[SE]  Relé de Proteção SEL311C - Proteção SubTensão (27P) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_15 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme19_15"], descricao="[SE]  Relé de Proteção SEL787 - Proteção Diferencial (87T) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_15, CONDIC_NORMALIZAR))

        cls.l_alm_20_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme20_00"], descricao="[SE]  Relé de Proteção SEL787 - Sobrecorrente Instantânea Lado de Baixa (50P_BT) (Abertura 52L) ")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_20_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme20_01"], descricao="[SE]  Relé de Proteção SEL787 - Sobrecorrente Temporizada de Neutro (51N) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_20_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme20_02"], descricao="[SE]  Relé de Proteção SEL787 - Sobrecorrente Temporizada Lado de Baixa (51P_BT) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_20_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme20_03"], descricao="[SE]  Relé de Proteção SEL787 - Sobrecorrente Temporizada Lado de Alta (51P_AT) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_20_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme20_04"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSG-U1 ou CPS-U1 Aberta (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_20_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme20_05"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSG-U2 ou CPS-U2 Aberta (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_20_b_15 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme20_15"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSG-U3 ou CPS-U3 Aberta (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_15, CONDIC_NORMALIZAR))

        cls.l_alm_21_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme21_00"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSG-U4 ou CPS-U4 Aberta (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_21_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_21_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme21_01"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSA-01 ou CSA-02 Aberta (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_21_b_01, CONDIC_NORMALIZAR))

        return