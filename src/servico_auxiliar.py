__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação do Serviço Auxiliar."

import logging
import traceback

import src.dicionarios.dict as d
import src.funcoes.leitura as lei
import src.funcoes.escrita as esc
import src.funcoes.condicionadores as c
import src.conectores.servidores as serv

from time import sleep

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class ServicoAuxiliar:

    status_dj_tsa = lei.LeituraModbusBit(
        serv.Servidores.clp["SA"],
        REG_SASE["DISJUNTOR_TSA_FECHADO"],
        descricao="[SA]  Status Disjuntor SA"
    )

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_ativos: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []


    @classmethod
    def resetar_emergencia(cls) -> "bool":
        try:
            res = esc.EscritaModBusBit.escrever_bit(serv.Servidores.clp["SA"], REG_SASE["CMD_REARME_FALHAS"], valor=1)
            return res

        except Exception:
            logger.error(f"[SA]  Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(traceback.format_exc())


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
                logger.debug(f"[SA]  Foram detectados Condicionadores ativos no Serviço Auxiliar!")
            else:
                logger.debug(f"[SA]  Ainda há Condicionadores ativos no Serviço Auxiliar!")

            for condic in condics_ativos:
                if condic in cls.condicionadores_ativos or condic.teste:
                    logger.debug(f"[SA]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\".{' Obs.: \"TESTE\"' if condic.teste else None}")
                    continue
                else:
                    logger.warning(f"[SA]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
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
        if cls.l_teste_voip.valor and not d.voip["SA_L_TESTE_VOIP"][0]:
            logger.warning("[SA]  Leitura Teste Mensageiro Voip ativada.")
            d.voip["SA_L_TESTE_VOIP"][0] = True
        elif not cls.l_teste_voip.valor and d.voip["SA_L_TESTE_VOIP"][0]:
            d.voip["SA_L_TESTE_VOIP"][0] = False


    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """

        ## CONDICIONADORES ESSENCIAIS
        cls.l_teste_ce_normalizar = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SA_CONDIC_E_NORMALIZAR"], descricao="[SA]  Condicionador Essencial Teste Normalizar")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_teste_ce_normalizar, CONDIC_NORMALIZAR))

        ## CONDICIONADORES
        cls.l_teste_c_normalizar = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SA_CONDIC_NORMALIZAR"], descricao="[SA]  Condicionador Teste Normalizar")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_teste_c_normalizar, CONDIC_NORMALIZAR))

        cls.l_teste_c_indisponibilizar = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SA_CONDIC_INDISPONIBILIZAR"], descricao="[SA]  Condicionador Essencial Teste Indisponibilizar")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_teste_c_normalizar, CONDIC_INDISPONIBILIZAR))


        ## WHATSAPP/VOIP
        cls.l_teste_voip = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SA_L_VOIP"], descricao="[SA]  Leitura Teste Voip")
        cls.l_teste_whats = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SA_L_WHATS"], descricao="[SA]  Leitura Teste WhatsApp")
