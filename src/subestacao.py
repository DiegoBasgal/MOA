__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Subestação."

import pytz
import logging
import traceback

import src.servico_auxiliar as sa

import src.funcoes.escrita as esc
import src.funcoes.leitura as lei
import src.funcoes.condicionadores as c
import src.conectores.banco_dados as bd
import src.conectores.servidores as serv

from time import sleep, time
from threading import Thread
from datetime import datetime

from src.dicionarios.reg_elipse import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class Subestacao:

    # ATRIBUIÇÃO DE VARIÁVEIS
    potencia_ativa = lei.LeituraModbus(
        serv.Servidores.rele["SE"],
        REG_RELE["SE"]["P"],
        descricao="[SE]  Potência Ativa"
    )
    status_dj_linha = lei.LeituraModbusBit(
        serv.Servidores.clp["SA"],
        REG_SASE["SE_DISJUNTOR_LINHA_FECHADO"],
        descricao="[SE]  Status Disjuntor Linha"
    )

    status_tensao: "int" = 0

    timer_tensao: "bool" = False

    leituras_tensao: "list[int]" = []

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_ativos: "list[c.CondicionadorBase]" = []
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
                sa.ServicoAuxiliar.resetar_emergencia()
                sleep(1)
                res = esc.EscritaModBusBit.escrever_bit(serv.Servidores.clp["SA"], REG_SASE["CMD_DISJ_LINHA_FECHA"], valor=1)
                return res

        except Exception:
            logger.error("[SE]  Houver um erro ao fechar o Disjuntor de Linha.")
            logger.debug(traceback.format_exc())
            return False


    @classmethod
    def verificar_se(cls) -> "int":
        """
        Função para verificação do Bay e Subestação.

        Apresenta a leitura de tensão VAB, VBC, VCA do Bay e Subestação.
        Caso haja uma falta de tensão na linha da subestação, aciona o temporizador
        para retomada em caso de queda de tensão. Caso a tensão esteja normal, tenta
        realizar o fechamento dos disjuntores do Bay e depois da Subestação. Caso
        haja um erro com o fechamento dos disjuntores, aciona a normalização da usina
        senão, sinaliza que está tudo correto para a máquina de estados do MOA.
        """

        try:
            if not cls.verificar_tensao() and not sa.ServicoAuxiliar.status_dj_tsa.valor:
                logger.debug("")
                logger.debug(f"[SE]  Tensão Subestação:            RS -> \"{cls.leituras_tensao[0]/1000 * 173.21 * 115:2.1f} V\" | ST -> \"{cls.leituras_tensao[1]/1000 * 173.21 * 115:2.1f} V\" | TR -> \"{cls.leituras_tensao[2]/1000 * 173.21 * 115:2.1f} V\"")
                logger.debug("")
                return DJS_FALTA_TENSAO

            elif not cls.fechar_dj_linha():
                return DJS_FALHA

            else:
                return DJS_OK

        except Exception:
            return DJS_FALTA_TENSAO


    @classmethod
    def verificar_tensao(cls) -> "bool":
        """
        Função para verificação de Tensão na linha da Subestação.
        """

        try:
            cls.leituras_tensao = serv.Servidores.rele["SE"].read_holding_registers(REG_RELE["SE"]["VAB"], 3)

            if (TENSAO_LINHA_BAIXA <= cls.leituras_tensao[0]/1000 * 173.21 * 115 <= TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA <= cls.leituras_tensao[1]/1000 * 173.21 * 115 <= TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA <= cls.leituras_tensao[2]/1000 * 173.21 * 115 <= TENSAO_LINHA_ALTA):
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

        autor = 0

        if True in (condic.ativo for condic in cls.condicionadores_essenciais):
            condics_ativos = [condic for condics in [cls.condicionadores_essenciais, cls.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if cls.condicionadores_ativos == []:
                logger.warning(f"[SE]  Foram detectados Condicionadores ativos na Subestação!")
            else:
                logger.info(f"[SE]  Ainda há Condicionadores ativos na Subestação!")

            for condic in condics_ativos:
                if condic.teste:
                    logger.debug(f"[SE]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\", Obs.: \"TESTE\"")
                    continue

                elif condic in cls.condicionadores_ativos:
                    logger.debug(f"[SE]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue

                else:
                    logger.warning(f"[SE]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    cls.condicionadores_ativos.append(condic)
                    bd.BancoDados.update_alarmes([
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
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """

        ## CONDICIONADORES ESSENCIAIS
        cls.l_disj_linha_aberto = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SE_DISJUNTOR_LINHA_ABERTO"], descricao="[SE]  Disjuntor de Linha Aberto")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_disj_linha_aberto, CONDIC_NORMALIZAR))

        # cls.l_rele_alm_led1_50ou51 = lei.LeituraModbusBit(serv.Servidores.rele["SE"], REG_RELE["SE"]["LED1_50_51"], invertido=True, descricao="[RELE][SE] Alarme LED 1 50 ou 51")
        # cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_alm_led1_50ou51, CONDIC_INDISPONIBILIZAR))

        # cls.l_rele_alm_led2_67N = lei.LeituraModbusBit(serv.Servidores.rele["SE"], REG_RELE["SE"]["LED2_67N"], invertido=True, descricao="[RELE][SE]  Alarme LED 2 67N")
        # cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_alm_led2_67N, CONDIC_INDISPONIBILIZAR))

        # cls.l_rele_alm_led6_50BF = lei.LeituraModbusBit(serv.Servidores.rele["SE"], REG_RELE["SE"]["LED6_50BF"], invertido=True, descricao="[RELE][SE]  Alarme LED 6 50BF")
        # cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_alm_led6_50BF, CONDIC_INDISPONIBILIZAR))

        # cls.l_rele_alm_led10_59N = lei.LeituraModbusBit(serv.Servidores.rele["SE"], REG_RELE["SE"]["LED10_59N"], invertido=True, descricao="[RELE][SE]  Alarme LED 10 59N")
        # cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_rele_alm_led10_59N, CONDIC_INDISPONIBILIZAR))

        # ## CONDICIONADORES NORMAIS
        # cls.l_rele_alm_led3 = lei.LeituraModbusBit(serv.Servidores.rele["SE"], REG_RELE["SE"]["LED3"], invertido=True, descricao="[RELE][SE]  Alarme LED 3")
        # cls.condicionadores.append(c.CondicionadorBase(cls.l_rele_alm_led3, CONDIC_INDISPONIBILIZAR))

        # cls.l_rele_alm_led4_78 = lei.LeituraModbusBit(serv.Servidores.rele["SE"], REG_RELE["SE"]["LED4_78"], invertido=True, descricao="[RELE][SE]  Alarme LED 4 78")
        # cls.condicionadores.append(c.CondicionadorBase(cls.l_rele_alm_led4_78, CONDIC_INDISPONIBILIZAR))

        # cls.l_rele_alm_led5 = lei.LeituraModbusBit(serv.Servidores.rele["SE"], REG_RELE["SE"]["LED5"], invertido=True, descricao="[RELE][SE]  Alarme LED 5")
        # cls.condicionadores.append(c.CondicionadorBase(cls.l_rele_alm_led5, CONDIC_INDISPONIBILIZAR))

        # cls.l_rele_alm_led7_81 = lei.LeituraModbusBit(serv.Servidores.rele["SE"], REG_RELE["SE"]["LED7_81"], invertido=True, descricao="[RELE][SE]  Alarme LED 7 81")
        # cls.condicionadores.append(c.CondicionadorBase(cls.l_rele_alm_led7_81, CONDIC_INDISPONIBILIZAR))

        # cls.l_rele_alm_led8_27 = lei.LeituraModbusBit(serv.Servidores.rele["SE"], REG_RELE["SE"]["LED8_27"], invertido=True, descricao="[RELE][SE]  Alarme LED 8 27")
        # cls.condicionadores.append(c.CondicionadorBase(cls.l_rele_alm_led8_27, CONDIC_INDISPONIBILIZAR))

        # cls.l_rele_alm_led9_59 = lei.LeituraModbusBit(serv.Servidores.rele["SE"], REG_RELE["SE"]["LED9_59"], invertido=True, descricao="[RELE][SE]  Alarme LED 9 59")
        # cls.condicionadores.append(c.CondicionadorBase(cls.l_rele_alm_led9_59, CONDIC_INDISPONIBILIZAR))

        cls.l_te_temp_muito_alta = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["TE_TEMPERATURA_MUITO_ALTA"], descricao="[SE]  Trasformador Elevador Temperatura Alta") # TODO -> Verificar invertido
        cls.condicionadores.append(c.CondicionadorBase(cls.l_te_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        cls.l_te_press_muito_alta = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["TE_PRESSAO_MUITO_ALTA"], descricao="[SE]  Trasformador Elevador Pressão Óleo Muito Alta")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_te_press_muito_alta, CONDIC_INDISPONIBILIZAR))

        cls.l_oleo_muito_baixo = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["TE_NIVEL_OLEO_MUITO_BAIXO"], descricao="[SE]  Trasformador Elevador Nível Óleo Muito Baixo")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_oleo_muito_baixo, CONDIC_INDISPONIBILIZAR))

        cls.l_disj_se_falha_fechar = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SE_DISJUNTOR_FALHA_FECHAR"], descricao="[SE]  Falha Fechamento Disjuntor de Linha")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_disj_se_falha_fechar, CONDIC_INDISPONIBILIZAR))

        cls.l_disj_se_falha_abrir = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SE_DISJUNTOR_FALHA_ABRIR"], descricao="[SE]  Falha Abertura Disjuntor de Linha")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_disj_se_falha_abrir, CONDIC_INDISPONIBILIZAR))