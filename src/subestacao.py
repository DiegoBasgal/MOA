__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Subestação."

import pytz
import logging
import traceback

import src.servico_auxiliar as sa

import src.dicionarios.dict as d
import src.funcoes.escrita as esc
import src.funcoes.leitura as lei
import src.funcoes.condicionadores as c
import src.conectores.servidores as serv

from time import sleep, time
from threading import Thread
from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class Subestacao:

    potencia_ativa = lei.LeituraModbus(
        serv.Servidores.rele["SE"],
        REG_RELE["SE"]["P"],
        descricao="[SE]  Potência Ativa"
    )
    tensao_rs = lei.LeituraModbus(
        serv.Servidores.rele["SE"],
        REG_RELE["SE"]["VAB"],
        descricao="[SE]  Tensão RS"
    )
    tensao_st = lei.LeituraModbus(
        serv.Servidores.rele["SE"],
        REG_RELE["SE"]["VBC"],
        descricao="[SE]  Tensão ST"
    )
    tensao_tr = lei.LeituraModbus(
        serv.Servidores.rele["SE"],
        REG_RELE["SE"]["VCA"],
        descricao="[SE]  Tensão TR"
    )

    status_dj_linha = lei.LeituraModbusBit(
        serv.Servidores.clp["SA"],
        REG_SASE["SE_DISJUNTOR_LINHA_FECHADO"],
        descricao="[SE]  Status Disjuntor Linha"
    )

    status_tensao: "int" = 0

    timer_tensao: "bool" = False

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []


    @classmethod
    def fechar_dj_linha(cls) -> "bool":
        try:
            if cls.status_dj_linha.valor:
                return True

            elif not sa.ServicoAuxiliar.status_dj_tsa.valor:
                logger.info("[SE]  Não foi possível fechar o Disjuntor de Linha, pois o Disjuntor do SA está aberto")
                return False

            else:
                logger.info(f"[SE]  O Disjuntor de Linha está aberto!")
                logger.info(f"[SE]  Enviando comando:                   \"FECHAR DISJUNTOR LINHA\"")
                logger.debug("")
                res = esc.EscritaModBusBit.escrever_bit(serv.Servidores.clp["SA"], REG_SASE["CMD_DISJ_LINHA_FECHA"], valor=1)
                return res

        except Exception:
            logger.error("[SE]  Houver um erro ao fechar o Disjuntor de Linha.")
            logger.debug(traceback.format_exc())
            return False


    @classmethod
    def verificar_tensao(cls) -> "bool":
        """
        Função para verificação de Tensão na linha da Subestação.
        """

        try:
            if (TENSAO_LINHA_BAIXA <= cls.tensao_rs.valor <= TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA <= cls.tensao_st.valor <= TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA <= cls.tensao_tr.valor <= TENSAO_LINHA_ALTA):
                return True
            else:
                logger.warning("[SE]  Tensão da linha fora do limite")
                return False

        except Exception:
            logger.error("[SE]  Houve um erro ao realizar a verificação da tensão na linha.")
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
            logger.debug("[SE]  Iniciando o timer para a normalização da tensão na linha")
            Thread(target=lambda: cls.temporizar_espera_tensao(600)).start()

        elif cls.status_tensao == TENSAO_REESTABELECIDA:
            logger.info("[SE]  Tensão na linha reestabelecida.")
            cls.status_tensao = TENSAO_VERIFICAR
            return True

        elif cls.status_tensao == TENSAO_FORA:
            logger.critical("[SE]  Não foi possível reestabelecer a tensão na linha. Acionando emergência!")
            cls.status_tensao = TENSAO_VERIFICAR
            return False

        else:
            logger.debug("[SE]  A tensão na linha ainda está fora")


    @classmethod
    def temporizar_espera_tensao(cls, seg: "int") -> "None":
        """
        Função de temporizador para espera de normalização de tensão da linha de transmissão.
        """

        delay = time() + seg

        while time() <= delay:
            if cls.verificar_tensao():
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

        if True in (condic.ativo for condic in cls.condicionadores_essenciais):
            condics_ativos = [condic for condics in [cls.condicionadores_essenciais, cls.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if cls.condicionadores_ativos == []:
                logger.warning(f"[SE]  Foram detectados Condicionadores ativos na Subestação!")
            else:
                logger.info(f"[SE]  Ainda há Condicionadores ativos na Subestação!")

            for condic in condics_ativos:
                if condic in cls.condicionadores_ativos or condic.teste:
                    logger.debug(f"[SE]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\".{' Obs.: \"TESTE\"' if condic.teste else None}")
                    continue
                else:
                    logger.warning(f"[SE]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    cls.condicionadores_ativos.append(condic)
                sleep(1)

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

        # WHATSAPP
        if cls.l_teste_whats.valor:
            logger.warning("[SA]  Leitura Teste Mensageiro WhatsApp ativada.")

        # WHATSAPP + VOIP
        if cls.l_teste_voip.valor and not d.voip["SE_L_TESTE_VOIP"][0]:
            logger.warning("[SA]  Leitura Teste Mensageiro Voip ativada.")
            d.voip["SE_L_TESTE_VOIP"][0] = True
        elif not cls.l_teste_voip.valor and d.voip["SE_L_TESTE_VOIP"][0]:
            d.voip["SE_L_TESTE_VOIP"][0] = False


    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """

        ## CONDICIONADORES ESSENCIAIS
        cls.l_teste_ce_normalizar = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["RELE_BLOQUEIO_86BTBF"], descricao="[SE]  Condicionador Essencial Teste Normalizar")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_teste_ce_normalizar, CONDIC_NORMALIZAR))

        ## CONDICIONADORES
        cls.l_teste_c_normalizar = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["BOTAO_BLOQUEIO_86BTBF"], descricao="[SE]  Condicionador Teste Normalizar")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_teste_c_normalizar, CONDIC_NORMALIZAR))

        cls.l_teste_c_indisponibilizar = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["DISJUNTOR_TSA_TRIP"], descricao="[SE]  Condicionador Essencial Teste Indisponibilizar")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_teste_c_normalizar, CONDIC_INDISPONIBILIZAR))

        ## WHATSAPP/VOIP
        cls.l_teste_voip = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["DISJUNTOR_GMG_TRIP"], descricao="[SE]  Leitura Teste Voip")
        cls.l_teste_whats = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SUPERVISOR_TENSAO_FALHA"], descricao="[SE]  Leitura Teste WhatsApp")