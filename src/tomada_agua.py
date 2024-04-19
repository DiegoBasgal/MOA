__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Tomada da Água."

import logging
import traceback

import src.usina as usn
import src.dicionarios.dict as d
import src.funcoes.leitura as lei
import src.funcoes.escrita as esc
import src.funcoes.condicionadores as c
import src.conectores.servidores as serv

from time import sleep

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class TomadaAgua:

    nv_montante = lei.LeituraModbusFloat(
        serv.Servidores.clp["TDA"],
        REG_TDA["NIVEL_MONTANTE_GRADE"],
        descricao="[TDA] Nível Montante"
    )
    nv_jusante = lei.LeituraModbusFloat(
        serv.Servidores.clp["TDA"],
        REG_TDA["NIVEL_JUSANTE_GRADE"],
        descricao="[TDA] Nível Jusante Grade"
    )

    erro_nv: "float" = 0
    erro_nv_anterior: "float" = 0
    nv_montante_recente: "float" = 0
    nv_montante_anterior: "float" = 0

    aguardando_reservatorio: "bool" = False

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []
    condicionadores_atenuadores: "list[c.CondicionadorBase]" = []


    @classmethod
    def atualizar_valores_montante(cls) -> "None":
        l_nivel = cls.nv_montante.valor

        cls.nv_montante_recente = l_nivel if 820 < l_nivel < 825 else cls.nv_montante_recente
        cls.erro_nv_anterior = cls.erro_nv
        cls.erro_nv = cls.nv_montante_recente - usn.Usina.cfg["nv_alvo"]


    @classmethod
    def controlar_reservatorio(cls) -> "int":
        """
        Função para controle de níveis do reservatório.

        Realiza a leitura de nível montante e determina qual condição entrar. Se
        o nível estiver acima do máximo, verifica se atingiu o Maximorum. Nesse
        caso é acionada a emergência da Usina, porém se for apenas vertimento,
        distribui a potência máxima para as Unidades.
        Caso a leitura retornar que o nível está abaixo do mínimo, verifica antes
        se atingiu o fundo do reservatório, nesse caso é acionada a emergência.
        Se o valor ainda estiver acima do nível de fundo, será distribuída a
        potência 0 para todas as Unidades e aciona a espera pelo nível.
        Caso a leitura esteja dentro dos limites normais, é chamada a função para
        calcular e distribuir a potência para as Unidades.
        """

        l_nivel = cls.nv_montante.valor

        if (l_nivel in (None, 0, 0.0) or l_nivel <= 800) and not cls.borda_erro_ler_nv:
            logger.info(f"[TDA] Erro de Leitura de Nível Montante identificada! Acionando espera pelo Reservatório.")
            cls.borda_erro_ler_nv = True
            cls.aguardando_reservatorio = True

        elif l_nivel >= usn.Usina.cfg["nv_maximo"] and not cls.aguardando_reservatorio:
            logger.debug("[TDA] Nível Montante acima do Máximo.")
            logger.debug(f"[TDA]          Leitura:                   {l_nivel:0.3f}")
            logger.debug("")

            if cls.nv_montante_anterior >= NIVEL_MAXIMORUM:
                logger.critical(f"[TDA] Nivel Montante ({cls.nv_montante_anterior:3.2f}) atingiu o Maximorum!")
                logger.debug("")
                return NV_EMERGENCIA
            else:
                cls.controle_i = 0.9
                cls.controle_ie = 0.5
                usn.Usina.ajustar_potencia(usn.Usina.cfg["pot_maxima_usina"])

                for ug in usn.Usina.ugs:
                    ug.step()

        elif l_nivel <= usn.Usina.cfg["nv_minimo"] and not cls.aguardando_reservatorio:
            logger.debug("[TDA] Nível Montante abaixo do Mínimo.")
            logger.debug(f"[TDA]          Leitura:                   {l_nivel:0.3f}")
            logger.debug("")
            cls.aguardando_reservatorio = True
            usn.Usina.distribuir_potencia(0)

            for ug in usn.Usina.ugs:
                ug.step()

            if cls.nv_montante_anterior <= NIVEL_FUNDO_RESERVATORIO:
                logger.critical(f"[TDA] Nível Montante ({cls.nv_montante_anterior:3.2f}) atingiu o fundo do reservatorio!")
                logger.debug("")
                return NV_EMERGENCIA

        elif cls.aguardando_reservatorio:
            logger.debug("[TDA] Aguardando Nível Montante...")
            logger.debug(f"[TDA]          Leitura:                   {l_nivel:0.3f}")
            logger.debug(f"[TDA]          Nível de Religamento:      {usn.Usina.cfg['nv_religamento']:0.3f}")
            logger.debug("")

            if l_nivel >= usn.Usina.cfg["nv_religamento"]:
                logger.debug("[TDA] Nível Montante dentro do limite de operação.")
                logger.debug(f"[TDA]          Leitura:                   {l_nivel:0.3f}")
                logger.debug("")
                cls.aguardando_reservatorio = False

        else:
            usn.Usina.controlar_potencia()

            for ug in usn.Usina.ugs:
                ug.step()

        return NV_NORMAL


    @classmethod
    def resetar_emergencia(cls) -> "bool":
        try:
            logger.info(f"[TDA] Enviando comando:                   \"RESET EMERGÊNCIA\"")
            res = esc.EscritaModBusBit.escrever_bit(serv.Servidores.clp["TDA"], REG_TDA["CMD_RESET_GERAL"], valor=1)
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

        if True in (condic.ativo for condic in cls.condicionadores_essenciais):
            condics_ativos = [condic for condics in [cls.condicionadores_essenciais, cls.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if cls.condicionadores_ativos == []:
                logger.warning(f"[TDA] Foram detectados Condicionadores ativos na Tomada da Água!")
            else:
                logger.info(f"[TDA] Ainda há Condicionadores ativos na Tomada da Água!")

            for condic in condics_ativos:
                if condic in cls.condicionadores_ativos or condic.teste:
                    logger.debug(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\".{' Obs.: \"TESTE\"' if condic.teste else None}")
                    continue
                else:
                    logger.warning(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
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
            logger.warning("[TDA] Leitura Teste Mensageiro WhatsApp ativada.")

        # WHATSAPP + VOIP
        if cls.l_teste_voip.valor and not d.voip["TDA_L_TESTE_VOIP"][0]:
            logger.warning("[TDA] Leitura Teste Mensageiro Voip ativada.")
            d.voip["TDA_L_TESTE_VOIP"][0] = True
        elif not cls.l_teste_voip.valor and d.voip["TDA_L_TESTE_VOIP"][0]:
            d.voip["TDA_L_TESTE_VOIP"][0] = False


    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """
        
        cls.l_diferencial_grade = lei.LeituraSubtracao([cls.nv_montante, cls.nv_jusante], descricao="[TDA] Diferencial de Grade")
        cls.c_diferencial_grade = c.CondicionadorExponencial(cls.l_diferencial_grade, CONDIC_INDISPONIBILIZAR, valor_base=0.3, valor_limite=0.4, ordem=4)
        cls.condicionadores_atenuadores.append(cls.c_diferencial_grade)

        ## CONDICIONADORES ESSENCIAIS
        cls.l_teste_ce_normalizar = lei.LeituraModbusBit(serv.Servidores.clp["TDA"], REG_TDA["CONDIC_E_NORMALIZAR"], descricao="[TDA] Condicionador Essencial Teste Normalizar")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_teste_ce_normalizar, CONDIC_NORMALIZAR))

        ## CONDICIONADORES
        cls.l_teste_c_normalizar = lei.LeituraModbusBit(serv.Servidores.clp["TDA"], REG_TDA["CONDIC_NORMALIZAR"], descricao="[TDA] Condicionador Teste Normalizar")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_teste_c_normalizar, CONDIC_NORMALIZAR))

        cls.l_teste_c_indisponibilizar = lei.LeituraModbusBit(serv.Servidores.clp["TDA"], REG_TDA["CONDIC_INDISPONIBILIZAR"], descricao="[TDA] Condicionador Essencial Teste Indisponibilizar")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_teste_c_indisponibilizar, CONDIC_INDISPONIBILIZAR))

        ## WHATSAPP/VOIP
        cls.l_teste_voip = lei.LeituraModbusBit(serv.Servidores.clp["TDA"], REG_TDA["L_VOIP"], descricao="[TDA] Leitura Teste Voip")
        cls.l_teste_whats = lei.LeituraModbusBit(serv.Servidores.clp["TDA"], REG_TDA["L_WHATS"], descricao="[TDA] Leitura Teste WhatsApp")