__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Subestação."

import pytz
import logging
import traceback
import threading

import src.dicionarios.dict as d
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

    clp = serv.Servidores.clp
    bd: "bd.BancoDados" = None

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
    dj_linha = lei.LeituraModbusBit(
        clp["SA"],
        REG_SE["DJ52L_FECHADO"],
        descricao="[SE]  Status Disjuntor Linha"
    )

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []
    condicionadores_ativos: "list[c.CondicionadorBase]" = []


    @classmethod
    def fechar_dj_linha(cls) -> "bool":
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
            if not cls.l_dj52l_condicao.valor:
                logger.warning(f"[SE]  Sem condição de fechamento do Disjuntor.")
                flags += 1

            if not cls.l_dj52l_mola.valor:
                logger.warning(f"[SE]  A Mola do Disjunto não está carregada.")
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

        if cls.dj52l_modo_local.valor and not d.voip["DJ52L_MODO_LOCAL"][0]:
            logger.warning(f"[SE]  Foi identificado que o Disjuntor 52L entrou em Modo Local. Favor verificar.")
            d.voip["DJ52L_MODO_LOCAL"][0] = True
        elif not cls.dj52l_modo_local.valor and d.voip["DJ52L_MODO_LOCAL"][0]:
            d.voip["DJ52L_MODO_LOCAL"][0] = False

        if cls.dj52l_alim125vcc_motor.valor and not d.voip["DJ52L_ALIM125VCC_MOTOR"][0]:
            logger.warning(f"[SE]  Foi identificado um desligamento do Motor de Alimentação 125VCC do Disjuntor 52L. Favor verificar.")
            d.voip["DJ52L_ALIM125VCC_MOTOR"][0] = True
        elif not cls.dj52l_alim125vcc_motor.valor and d.voip["DJ52L_ALIM125VCC_MOTOR"][0]:
            d.voip["DJ52L_ALIM125VCC_MOTOR"][0] = False

        if cls.dj52l_falta_vcc.valor and not d.voip["DJ52L_FALTA_VCC"][0]:
            logger.warning(f"[SE]  Foi identificado uma falta de Alimentação (VCC) do Disjuntor 52L na PCH Ado Popinhak. Favor verificar.")
            d.voip["DJ52L_FALTA_VCC"][0] = True
        elif not cls.dj52l_falta_vcc.valor and d.voip["DJ52L_FALTA_VCC"][0]:
            d.voip["DJ52L_FALTA_VCC"][0] = False

        if cls.dj52l_gas_sf6_1.valor and not d.voip["DJ52L_GAS_SF6_1"][0]:
            logger.warning(f"[SE]  Foi identificado um acionamento do Alarme de Gás SF6 1 do Disjuntor 52L. Favor verificar.")
            d.voip["DJ52L_GAS_SF6_1"][0] = True
        elif not cls.dj52l_gas_sf6_1.valor and d.voip["DJ52L_GAS_SF6_1"][0]:
            d.voip["DJ52L_GAS_SF6_1"][0] = False

        if cls.secc_modo_local.valor and not d.voip["SECC_MODO_LOCAL"][0]:
            logger.warning(f"[SE]  Foi identificado que a Seccionadora entrou em Modo Local. Favor verificar.")
            d.voip["SECC_MODO_LOCAL"][0] = True
        elif not cls.secc_modo_local.valor and d.voip["SECC_MODO_LOCAL"][0]:
            d.voip["SECC_MODO_LOCAL"][0] = False

        if cls.secc_lam_fechada.valor and not d.voip["SECC_LAMINA_FECHADA"][0]:
            logger.warning(f"[SE]  Foi identificado que a Lâmina da Seccionadora foi Fechada. Favor verificar.")
            d.voip["SECC_LAMINA_FECHADA"][0] = True
        elif not cls.secc_lam_fechada.valor and d.voip["SECC_LAMINA_FECHADA"][0]:
            d.voip["SECC_LAMINA_FECHADA"][0] = False

        if cls.secc_cmd_alim_vcc.valor and not d.voip["SECC_ALIM_VCC_CMD"][0]:
            logger.warning(f"[SE]  Foi identificado um acionamento do Comando de Alimentação (VCC) da Seccionadora. Favor verificar.")
            d.voip["SECC_ALIM_VCC_CMD"][0] = True
        elif not cls.secc_cmd_alim_vcc.valor and d.voip["SECC_ALIM_VCC_CMD"][0]:
            d.voip["SECC_ALIM_VCC_CMD"][0] = False

        if cls.secc_bloq_alim_vcc.valor and not d.voip["SECC_ALIM_VCC_BLOQ"][0]:
            logger.warning(f"[SE]  Foi identificado um bloqueio na Alimentação (VCC) da Seccionadora. Favor verificar.")
            d.voip["SECC_ALIM_VCC_BLOQ"][0] = True
        elif not cls.secc_bloq_alim_vcc.valor and d.voip["SECC_ALIM_VCC_BLOQ"][0]:
            d.voip["SECC_ALIM_VCC_BLOQ"][0] = False

        if cls.l_dj_17.valor and not d.voip["DJ_17"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Circuitos de Sinalização CSA-U1. Favor verificar.")
            d.voip["DJ_17"][0] = True
        elif not cls.l_dj_17.valor and d.voip["DJ_17"][0]:
            d.voip["DJ_17"][0] = False

        if cls.l_dj_18.valor and not d.voip["DJ_18"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Circuitos de Sinalização CSA-U2. Favor verificar.")
            d.voip["DJ_18"][0] = True
        elif not cls.l_dj_18.valor and d.voip["DJ_18"][0]:
            d.voip["DJ_18"][0] = False

        if cls.l_dj_26.valor and not d.voip["DJ_26"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação do Cubículo CSA-U1. Favor verificar.")
            d.voip["DJ_26"][0] = True
        elif not cls.l_dj_26.valor and d.voip["DJ_26"][0]:
            d.voip["DJ_26"][0] = False

        if cls.l_dj_27.valor and not d.voip["DJ_27"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação do Cubículo CSA-U2. Favor verificar.")
            d.voip["DJ_27"][0] = True
        elif not cls.l_dj_27.valor and d.voip["DJ_27"][0]:
            d.voip["DJ_27"][0] = False

        if cls.l_dj_29.valor and not d.voip["DJ_29"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Monitor de Temperatura do TSA-01. Favor verificar.")
            d.voip["DJ_29"][0] = True
        elif not cls.l_dj_29.valor and d.voip["DJ_29"][0]:
            d.voip["DJ_29"][0] = False

        if cls.l_dj_30.valor and not d.voip["DJ_30"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Monitor de Temperatura do TSA-02. Favor verificar.")
            d.voip["DJ_30"][0] = True
        elif not cls.l_dj_30.valor and d.voip["DJ_30"][0]:
            d.voip["DJ_30"][0] = False

        if cls.l_dj_31.valor and not d.voip["DJ_31"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Reserva PDSA-CC. Favor verificar.")
            d.voip["DJ_31"][0] = True
        elif not cls.l_dj_31.valor and d.voip["DJ_31"][0]:
            d.voip["DJ_31"][0] = False

        if cls.l_dj_34.valor and not d.voip["DJ_34"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação do Quadro Q49-U1. Favor verificar.")
            d.voip["DJ_34"][0] = True
        elif not cls.l_dj_34.valor and d.voip["DJ_34"][0]:
            d.voip["DJ_34"][0] = False

        if cls.l_dj_41.valor and not d.voip["DJ_41"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação do Quadro Q49-U2. Favor verificar.")
            d.voip["DJ_41"][0] = True
        elif not cls.l_dj_41.valor and d.voip["DJ_41"][0]:
            d.voip["DJ_41"][0] = False

        if cls.l_dj_48.valor and not d.voip["DJ_48"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação do Quadro Q49-U3. Favor verificar.")
            d.voip["DJ_48"][0] = True
        elif not cls.l_dj_48.valor and d.voip["DJ_48"][0]:
            d.voip["DJ_48"][0] = False

        if cls.l_dj_55.valor and not d.voip["DJ_55"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação do Quadro Q49-U4. Favor verificar.")
            d.voip["DJ_55"][0] = True
        elif not cls.l_dj_55.valor and d.voip["DJ_55"][0]:
            d.voip["DJ_55"][0] = False

        if cls.l_dj_60.valor and not d.voip["DJ_60"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Bomba Drenagem 01. Favor verificar.")
            d.voip["DJ_60"][0] = True
        elif not cls.l_dj_60.valor and d.voip["DJ_60"][0]:
            d.voip["DJ_60"][0] = False

        if cls.l_dj_61.valor and not d.voip["DJ_61"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Bomba Drenagem 02. Favor verificar.")
            d.voip["DJ_61"][0] = True
        elif not cls.l_dj_61.valor and d.voip["DJ_61"][0]:
            d.voip["DJ_61"][0] = False

        if cls.l_dj_62.valor and not d.voip["DJ_62"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Bomba Drenagem 03. Favor verificar.")
            d.voip["DJ_62"][0] = True
        elif not cls.l_dj_62.valor and d.voip["DJ_62"][0]:
            d.voip["DJ_62"][0] = False

        if cls.l_dj_63.valor and not d.voip["DJ_63"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação do Compressor de AR. Favor verificar.")
            d.voip["DJ_63"][0] = True
        elif not cls.l_dj_63.valor and d.voip["DJ_63"][0]:
            d.voip["DJ_63"][0] = False

        if cls.l_dj_67.valor and not d.voip["DJ_67"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação do Painel PCTA. Favor verificar.")
            d.voip["DJ_67"][0] = True
        elif not cls.l_dj_67.valor and d.voip["DJ_67"][0]:
            d.voip["DJ_67"][0] = False

        if cls.l_dj_71.valor and not d.voip["DJ_71"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação do Elevador da Casa de Força. Favor verificar.")
            d.voip["DJ_71"][0] = True
        elif not cls.l_dj_71.valor and d.voip["DJ_71"][0]:
            d.voip["DJ_71"][0] = False

        if cls.l_dj_72.valor and not d.voip["DJ_72"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação do Painel PCAD. Favor verificar.")
            d.voip["DJ_72"][0] = True
        elif not cls.l_dj_72.valor and d.voip["DJ_72"][0]:
            d.voip["DJ_72"][0] = False

        if cls.l_dj_73.valor and not d.voip["DJ_73"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Sistema de Retrolavagem do Filtro 01. Favor verificar.")
            d.voip["DJ_73"][0] = True
        elif not cls.l_dj_73.valor and d.voip["DJ_73"][0]:
            d.voip["DJ_73"][0] = False

        if cls.l_dj_74.valor and not d.voip["DJ_74"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Sistema de Retrolavagem do Filtro 02. Favor verificar.")
            d.voip["DJ_74"][0] = True
        elif not cls.l_dj_74.valor and d.voip["DJ_74"][0]:
            d.voip["DJ_74"][0] = False

        if cls.l_dj_75.valor and not d.voip["DJ_75"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação do Carregador de Baterias 01. Favor verificar.")
            d.voip["DJ_75"][0] = True
        elif not cls.l_dj_75.valor and d.voip["DJ_75"][0]:
            d.voip["DJ_75"][0] = False

        if cls.l_dj_76.valor and not d.voip["DJ_76"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação do Carregador de Baterias 02. Favor verificar.")
            d.voip["DJ_76"][0] = True
        elif not cls.l_dj_76.valor and d.voip["DJ_76"][0]:
            d.voip["DJ_76"][0] = False

        if cls.l_dj_89.valor and not d.voip["DJ_89"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Bomba 01 Injeção Água Selo Mecânico. Favor verificar.")
            d.voip["DJ_89"][0] = True
        elif not cls.l_dj_89.valor and d.voip["DJ_89"][0]:
            d.voip["DJ_89"][0] = False

        if cls.l_dj_90.valor and not d.voip["DJ_90"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Bomba 02 Injeção Água Selo Mecânico. Favor verificar.")
            d.voip["DJ_90"][0] = True
        elif not cls.l_dj_90.valor and d.voip["DJ_90"][0]:
            d.voip["DJ_90"][0] = False

        if cls.l_dj_91.valor and not d.voip["DJ_91"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Bomba 01 Água Serviço. Favor verificar.")
            d.voip["DJ_91"][0] = True
        elif not cls.l_dj_91.valor and d.voip["DJ_91"][0]:
            d.voip["DJ_91"][0] = False

        if cls.l_dj_92.valor and not d.voip["DJ_92"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Bomba 02 Água Serviço. Favor verificar.")
            d.voip["DJ_92"][0] = True
        elif not cls.l_dj_92.valor and d.voip["DJ_92"][0]:
            d.voip["DJ_92"][0] = False

        if cls.l_dj_93.valor and not d.voip["DJ_93"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação UCP Bombas de Drenagem. Favor verificar.")
            d.voip["DJ_93"][0] = True
        elif not cls.l_dj_93.valor and d.voip["DJ_93"][0]:
            d.voip["DJ_93"][0] = False

        if cls.l_dj_94.valor and not d.voip["DJ_94"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Torre de Resfriamento. Favor verificar.")
            d.voip["DJ_94"][0] = True
        elif not cls.l_dj_94.valor and d.voip["DJ_94"][0]:
            d.voip["DJ_94"][0] = False

        if cls.l_dj_95.valor and not d.voip["DJ_95"][0]:
            logger.warning("[SE]  Foi identificado um desligamento do Disjuntor de Alimentação Compressor de Ar. Favor verificar.")
            d.voip["DJ_95"][0] = True
        elif not cls.l_dj_95.valor and d.voip["DJ_95"][0]:
            d.voip["DJ_95"][0] = False


    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """

        cls.l_dj52l_mola = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["DJ52L_MOLA_CARREGADA"], descricao="[SE]  DJ52L - Mola Carregada")
        cls.l_dj52l_condicao = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["DJ52L_COND_FECHAMENTO"], descricao="[SE]  DJ52L - Condição de Fechamento")



        cls.l_alm_01_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme01_00"], descricao="[SE]  PACP - Botão de Emergência Pressionado (Abertura 52L)")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_alm_01_b_00, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_01_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme01_01"], descricao="[SE]  Emergência Supervisório Pressionada (Abertura 52L)")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_alm_01_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_01_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme01_12"], descricao="[SE]  Relé de Proteção SEL787 - TRIP")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_alm_01_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_00"], descricao="[SE]  Relé de Proteção SEL311C - TRIP")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_alm_02_b_00, CONDIC_NORMALIZAR))


        cls.dj52l_gas_sf6_2 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["DJ52L_GAS_SF6_2"], invertido=True, descricao="[SE]  Disjuntor 52L Gás SF6 2")
        cls.condicionadores.append(c.CondicionadorBase(cls.dj52l_gas_sf6_2, CONDIC_INDISPONIBILIZAR))

        cls.dj52l_flh_abertura = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["DJ52L_FALHA_ABERTURA"], descricao="[SE]  Disjuntor 52L Falha Abertura")
        cls.condicionadores.append(c.CondicionadorBase(cls.dj52l_flh_abertura, CONDIC_INDISPONIBILIZAR))

        cls.secc_89l_aberta = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["SECC_89L_ABERTA"], descricao="[SE]  Seccionadora 89L Aberta")
        cls.condicionadores.append(c.CondicionadorBase(cls.secc_89l_aberta, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_01_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme01_13"], descricao="[SE]  Relé de Proteção SEL787 - Falha 50/62BF")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_13, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_01_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme01_14"], descricao="[SE]  Relé de Proteção SEL787 - Falha de Hardware")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_01_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_01"], descricao="[SE]  Relé de Proteção SEL311C - Falha 50/62BF")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_01, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_02_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_02"], descricao="[SE]  Relé de Proteção SEL311C - Falha de Hardware")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_04"], descricao="[SE]  Relé de Proteção 59N - Alarme")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_05"], descricao="[SE]  Relé de Proteção 59N - Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_05, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_02_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_07"], descricao="[SE]  Relé de Bloqueio 86BF (Falha Disjuntor) - Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_07, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_02_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_08"], descricao="[SE]  Relé de Bloqueio 86TE (Proteções do Trafo Elevador) - Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_08, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_02_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_11"], descricao="[SE]  Seccionadora 89L - Lâmina de Terra Fechada")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_12"], descricao="[SE]  Seccionadora 89L - Lâmina de Terra Bloqueada")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_02_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme02_13"], descricao="[SE]  Seccionadora 89L - Atenção! Chave em Modo Local")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_02_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_00"], descricao="[SE]  Disjuntor 52L - Falha na Abertura")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_00, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_03_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_01"], descricao="[SE]  Disjuntor 52L - Falha no Fechamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_02"], descricao="[SE]  Disjuntor 52L - Inconsistência Status Aberto/Fechado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_02, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_03_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_03"], descricao="[SE]  Disjuntor 52L - Falta Tensão Vcc")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_04"], descricao="[SE]  Disjuntor 52L - Mola Descarregada")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_05"], descricao="[SE]  Disjuntor 52L - Alarme Pressão Baixa Gás SF6")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_06"], descricao="[SE]  Disjuntor 52L - Trip Pressão Baixa Gás SF6 ( Impedimento do Fechamento 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_06, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_03_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_07"], descricao="[SE]  Disjuntor 52L - Atenção! Chave em Modo Local")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_03_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme03_08"], descricao="[SE]  Disjuntor 52L - Falha no Circuito do Motor de Carregamento da Mola")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_03_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_02"], descricao="[SE]  Trafo Elevador - Alarme Relé Buchholz")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_02, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_05_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_03"], descricao="[SE]  Trafo Elevador - Trip Relé Buchholz Bloqueio (Bloqueio 86TE)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_03, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_05_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_04"], descricao="[SE]  Trafo Elevador - Trip Nível de Óleo Baixo (Bloqueio 86TE)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_04, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_05_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_05"], descricao="[SE]  Trafo Elevador - Alarme Nível de Óleo Alto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_06 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_06"], descricao="[SE]  Trafo Elevador - Alarme Sobretemperatura do Óleo")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_07"], descricao="[SE]  Trafo Elevador - Trip Sobretemperatura do Óleo (Bloqueio 86TE)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_07, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_05_b_08 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_08"], descricao="[SE]  Trafo Elevador - Alarme Sobretemperatura do Enrolamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_09 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_09"], descricao="[SE]  Trafo Elevador - Trip Sobretemperatura do Enrolamento (Bloqueio 86TE)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_09, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_05_b_10 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_10"], descricao="[SE]  Trafo Elevador - Alarme Válvula de Alívio de Pressão")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_11 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_11"], descricao="[SE]  Trafo Elevador - Trip Válvula de Alívio de Pressão (Bloqueio 86TE)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_11, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_05_b_12 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_12"], descricao="[SE]  Trafo Elevador - Falha Relé Monitor de Temperatura")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_05_b_13 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_13"], descricao="[SE]  Trafo Elevador - Trip Pressão Súbita (Bloqueio 86TE)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_13, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_05_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme05_14"], descricao="[SE]  Trafo Elevador - Falha Ventilação Forçada")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_05_b_14, CONDIC_NORMALIZAR))

        cls.l_alm_09_b_07 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme09_07"], descricao="[SE]  PACP-SE - Sensor de Fumaça Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_09_b_07, CONDIC_INDISPONIBILIZAR))

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
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_13, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_18_b_14 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme18_14"], descricao="[SE]  Relé de Proteção SEL311C - Sobrecorrente Residual Temporizada (51G) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_14, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_18_b_15 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme18_15"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Fase Zona 01 (21P_Z1) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_18_b_15, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_19_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme19_00"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Fase Zona 02 (21P_Z2) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_00, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_19_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme19_01"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Fase Zona 03 Reversa (21P_Z3R) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_01, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_19_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme19_02"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Neutro Zona 01 (21N_Z1) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_02, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_19_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme19_03"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Neutro Zona 02 (21N_Z2) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_03, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_19_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme19_04"], descricao="[SE]  Relé de Proteção SEL311C - Proteção de Distância de Neutro Zona 03 Reversa (21N_Z3R) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_04, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_19_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme19_05"], descricao="[SE]  Relé de Proteção SEL311C - Proteção SubTensão (27P) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_19_b_15 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme19_15"], descricao="[SE]  Relé de Proteção SEL787 - Proteção Diferencial (87T) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_19_b_15, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_20_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme20_00"], descricao="[SE]  Relé de Proteção SEL787 - Sobrecorrente Instantânea Lado de Baixa (50P_BT) (Abertura 52L) ")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_00, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_20_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme20_01"], descricao="[SE]  Relé de Proteção SEL787 - Sobrecorrente Temporizada de Neutro (51N) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_01, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_20_b_02 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme20_02"], descricao="[SE]  Relé de Proteção SEL787 - Sobrecorrente Temporizada Lado de Baixa (51P_BT) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_02, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_20_b_03 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme20_03"], descricao="[SE]  Relé de Proteção SEL787 - Sobrecorrente Temporizada Lado de Alta (51P_AT) (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_03, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_20_b_04 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme20_04"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSG-U1 ou CPS-U1 Aberta (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_04, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_20_b_05 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme20_05"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSG-U2 ou CPS-U2 Aberta (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_05, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_20_b_15 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme20_15"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSG-U3 ou CPS-U3 Aberta (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_20_b_15, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_21_b_00 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme21_00"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSG-U4 ou CPS-U4 Aberta (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_21_b_00, CONDIC_INDISPONIBILIZAR))

        cls.l_alm_21_b_01 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["Alarme21_01"], descricao="[SE]  Relé de Proteção SEL787 - Grade de Proteção das Portas CSA-01 ou CSA-02 Aberta (Abertura 52L)")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_21_b_01, CONDIC_INDISPONIBILIZAR))

        cls.l_dj_02 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_02"], descricao="[SE]  PACP-SE - Alimentação Circuitos de Comando - Disj. Q125.0")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dj_02, CONDIC_INDISPONIBILIZAR))

        cls.l_dj_04 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_04"], descricao="[SE]  PACP-SE - Alimentação Relés de Proteção SEL311C e SEL787 - Disj. Q125.2")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dj_04, CONDIC_INDISPONIBILIZAR))

        cls.l_dj_07 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_07"], descricao="[SE]  PACP-SE - Alimentação Circuito de Comando Disjuntor 52L - Disj. Q125.6")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dj_07, CONDIC_INDISPONIBILIZAR))

        cls.l_dj_08 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_08"], descricao="[SE]  PACP-SE - Alimentação Motor Carregamento da Mola do Disjuntor 52L - Disj. Q125.7")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dj_08, CONDIC_INDISPONIBILIZAR))

        cls.l_dj_24 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_24"], descricao="[SE]  PDSA-CC - Alimentação do Painel PDSA-CA - Disj. Q125.3")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dj_24, CONDIC_INDISPONIBILIZAR))

        cls.l_dj_28 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_28"], descricao="[SE]  PDSA-CC - Alimentação Painel do Trafo Elevador - Disj. Q125.7")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dj_28, CONDIC_INDISPONIBILIZAR))

        cls.l_dj_65 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_65"], descricao="[SE]  PDSA-CA - Alimentação 125Vcc Principal - Disj. Q125.0")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dj_65, CONDIC_INDISPONIBILIZAR))


        # Lógicas "um depende do outro"
        cls.l_dj_19 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_19"], descricao="[SE]  CB01 - Carregador de Baterias 01 - Disj. Q1/Q2/Q3") # Voip + whats (Depende do condic abaixo)
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dj_19, CONDIC_INDISPONIBILIZAR))

        cls.l_dj_20 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_20"], descricao="[SE]  CB02 - Carregador de Baterias 02 - Disj. Q1/Q2/Q3") # Voip + whats (Depende do condic acima)
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dj_20, CONDIC_INDISPONIBILIZAR))


        cls.l_dj_21 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_21"], descricao="[SE]  PDSA-CC - Alimentação Principal CB01 - Disj. Q125.E1") # Voip + whats (Depende do condic abaixo)
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dj_21, CONDIC_INDISPONIBILIZAR))

        cls.l_dj_22 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_22"], descricao="[SE]  PDSA-CC - Alimentação Principal CB02 - Disj. Q125.E2") # Voip + whats (Depende do condic acima)
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dj_22, CONDIC_INDISPONIBILIZAR))


        cls.l_dj_99 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_99"], descricao="[SE]  PINV - Alimentação Boost 01 - Disj. Q125.0") # Voip + whats (Depende do condic abaixo)
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dj_99, CONDIC_INDISPONIBILIZAR))

        cls.l_dj_100 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_100"], descricao="[SE]  PINV - Alimentação Boost 02 - Disj. Q125.1") # Voip + whats (Depende do condic acima)
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dj_100, CONDIC_INDISPONIBILIZAR))


        ## MENSAGEIRO
        cls.dj52l_modo_local = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["DJ52L_MODO_LOCAL"], descricao="[SE]  Disjuntor 52L Modo Local")
        cls.dj52l_alim125vcc_motor = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["DJ52L_ALIM125VCC_MOTOR"], invertido=True, descricao="[SE]  Disjuntor 52L Motor Alimentação 125VCC Desligado")
        cls.dj52l_falta_vcc = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["DJ52L_FALTA_VCC"], descricao="[SE]  Disjuntor 52L Falta VCC")
        cls.dj52l_gas_sf6_1 = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["DJ52L_GAS_SF6_1"], invertido=True, descricao="[SE]  Disjuntor 52L Gás SF6 1")
        cls.secc_modo_local = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["SECC_MODO_LOCAL"], descricao="[SE]  Seccionadora Modo Local")
        cls.secc_lam_fechada = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["SECC_LAMINA_FECHADA"], descricao="[SE]  Seccionadora Lamina Fechada")
        cls.secc_cmd_alim_vcc = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["SECC_ALIM_VCC_CMD"], descricao="[SE]  Seccionadora Comando Alimentação VCC Acionado")
        cls.secc_bloq_alim_vcc = lei.LeituraModbusBit(cls.clp["SA"], REG_SE["SECC_ALIM_VCC_BLOQ"], descricao="[SE]  Seccionadora Comando Alimentação VCC Bloqueio")

        cls.l_dj_17 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_17"], descricao="[SE]  CSA-U1 - Alimentação Circuitos de Sinalização - Disj. Q125.0")
        cls.l_dj_18 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_18"], descricao="[SE]  CSA-U2 - Alimentação Circuitos de Sinalização - Disj. Q125.0")
        cls.l_dj_26 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_26"], descricao="[SE]  PDSA-CC - Alimentação do Cubículo CSA-U1 - Disj. Q125.5")
        cls.l_dj_27 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_27"], descricao="[SE]  PDSA-CC - Alimentação do Cubículo CSA-U2 - Disj. Q125.6")
        cls.l_dj_29 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_29"], descricao="[SE]  PDSA-CC - Alimentação Monitor de Temperatura do TSA-01 - Disj. Q125.8")
        cls.l_dj_30 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_30"], descricao="[SE]  PDSA-CC - Alimentação Monitor de Temperatura do TSA-02 - Disj. Q125.9")
        cls.l_dj_31 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_31"], descricao="[SE]  PDSA-CC - Alimentação Reserva - Disj. Q125.10")
        cls.l_dj_34 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_34"], descricao="[SE]  PDSA-CC - Alimentação do Quadro Q49-U1 - Disj. 1Q125.2")
        cls.l_dj_41 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_41"], descricao="[SE]  PDSA-CC - Alimentação do Quadro Q49-U2 - Disj. 2Q125.2")
        cls.l_dj_48 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_48"], descricao="[SE]  PDSA-CC - Alimentação do Quadro Q49-U3 - Disj. 3Q125.2")
        cls.l_dj_55 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_55"], descricao="[SE]  PDSA-CC - Alimentação do Quadro Q49-U4 - Disj. 4Q125.2")
        cls.l_dj_60 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_60"], descricao="[SE]  PDSA-CA - Alimentação Bomba Drenagem 01 - Disj. QM1")
        cls.l_dj_61 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_61"], descricao="[SE]  PDSA-CA - Alimentação Bomba Drenagem 02 - Disj. QM2")
        cls.l_dj_62 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_62"], descricao="[SE]  PDSA-CA - Alimentação Bomba Drenagem 03 - Disj. QM3")
        cls.l_dj_63 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_63"], descricao="[SE]  PDSA-CA - Alimentação do Compressor de AR - Disj. QM4")
        cls.l_dj_67 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_67"], descricao="[SE]  PDSA-CA - Alimentação do Painel PCTA - Disj. Q380.1")
        cls.l_dj_71 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_71"], descricao="[SE]  PDSA-CA - Alimentação do Elevador da Casa de Força - Disj. Q380.5")
        cls.l_dj_72 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_72"], descricao="[SE]  PDSA-CA - Alimentação do Painel PCAD - Disj. Q380.6")
        cls.l_dj_73 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_73"], descricao="[SE]  PDSA-CA - Alimentação Sistema de Retrolavagem do Filtro 01 - Disj. Q380.7")
        cls.l_dj_74 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_74"], descricao="[SE]  PDSA-CA - Alimentação Sistema de Retrolavagem do Filtro 02 - Disj. Q380.8")
        cls.l_dj_75 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_75"], descricao="[SE]  PDSA-CA - Alimentação do Carregador de Baterias 01 - Disj. Q380.9")
        cls.l_dj_76 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_76"], descricao="[SE]  PDSA-CA - Alimentação do Carregador de Baterias 02 - Disj. Q380.10")
        cls.l_dj_89 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_89"], descricao="[SE]  PDSA-CA - Alimentação Bomba 01 Injeção Água Selo Mecânico - Disj. QM5")
        cls.l_dj_90 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_90"], descricao="[SE]  PDSA-CA - Alimentação Bomba 02 Injeção Água Selo Mecânico - Disj. QM6")
        cls.l_dj_91 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_91"], descricao="[SE]  PDSA-CA - Alimentação Bomba 01 Água Serviço - Disj. QM7")
        cls.l_dj_92 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_92"], descricao="[SE]  PDSA-CA - Alimentação Bomba 02 Água Serviço - Disj. QM8")
        cls.l_dj_93 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_93"], descricao="[SE]  PDSA-CA - Alimentação UCP Bombas de Drenagem - Disj. Q220.11")
        cls.l_dj_94 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_94"], descricao="[SE]  PDSA-CA - Alimentação Torre de Resfriamento - Disj. Q380.11")
        cls.l_dj_95 = lei.LeituraModbus(cls.clp["SA"], REG_SE["DJ_95"], descricao="[SE]  PDSA-CA - Alimentação Compressor de Ar - Disj. Q380.12")