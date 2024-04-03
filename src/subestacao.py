import pytz
import logging
import threading
import traceback

import src.funcoes.leitura as lei
import src.funcoes.condicionador as c
import src.conectores.servidores as srv
import src.conectores.banco_dados as bd

from time import time, sleep
from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class Subestacao:

    clp = srv.Servidores.clp
    bd: "bd.BancoDados" = None

    status_tensao: "int" = 0

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_ativos: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []

    l_potencia_medidor: "lei.LeituraModbus" = lei.LeituraModbus(
        clp["SA"],
        REG_SA["PM810_POT_ATIVA"],
        op=4,
        descricao="[SE]  Leitura Potência Medidor Usina"
    )
    l_tensao_rs: "lei.LeituraModbus" = lei.LeituraModbus(
        clp["SA"],
        REG_SA["PM810_TENSAO_AB"],
        escala=100,
        op=4,
        descricao="[SE]  Leitura Tensão RS"
    )
    l_tensao_st: "lei.LeituraModbus" = lei.LeituraModbus(
        clp["SA"],
        REG_SA["PM810_TENSAO_BC"],
        escala=100,
        op=4,
        descricao="[SE]  Leitura Tensão ST"
    )
    l_tensao_tr: "lei.LeituraModbus" = lei.LeituraModbus(
        clp["SA"],
        REG_SA["PM810_TENSAO_CA"],
        escala=100,
        op=4,
        descricao="[SE]  Leitura Tensão TR"
    )


    @staticmethod
    def get_time() -> "datetime":
        """
        Função para obter data e hora atual.
        """

        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    @classmethod
    def verificar_tensao(cls) -> "bool":
        """
        Função para verificação de limites de tensão da linha de transmissão.
        """

        try:
            if (TENSAO_LINHA_BAIXA < cls.l_tensao_rs.valor < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < cls.l_tensao_st.valor < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < cls.l_tensao_tr.valor < TENSAO_LINHA_ALTA):
                return True
            else:
                logger.warning("[SE]  Tensão da linha fora do limite.")
                return False

        except Exception:
            logger.error(f"[SE]  Houve um erro ao realizar a verificação da tensão na linha.")
            logger.debug(traceback.format_exc())
            return False


    @classmethod
    def aguardar_tensao(cls) -> "bool":
        """
        Função para normalização após a queda de tensão da linha de transmissão.

        Primeiramente, caso haja uma queda, será chamada a função com o timer de
        espera com tempo pré determinado. Caso a tensão seja reestabelecida
        dentro do limite de tempo, é chamada a funcão de normalização da Usina.
        Se o timer passar do tempo, é chamada a função de acionamento de emergência
        e acionado chamada de emergência por Voip.
        """

        if cls.status_tensao == TENSAO_VERIFICAR:
            cls.status_tensao = TENSAO_AGUARDO
            logger.debug("[SE]  Iniciando o timer para a normalização da tensão na linha.")
            threading.Thread(target=lambda: cls.temporizar_aguardo_tensao(600)).start()

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
    def temporizar_aguardo_tensao(cls, delay: "int") -> "None":
        """
        Função de temporizador para espera de normalização de tensão da linha de
        transmissão.
        """

        while time() <= time() + delay:
            if cls.verificar_tensao():
                cls.status_tensao = TENSAO_REESTABELECIDA
                return
            sleep(time() - (time() - 15))
        cls.status_tensao = TENSAO_FORA


    @classmethod
    def fechar_dj_linha(cls) -> "bool":
        """
        Função para acionamento do comando de fechamento do Disjuntor 52L (Linha).

        Primeiramente, chama a função de verificação de bloqueios de fechamento,
        caso não haja nenhuma condição, envia o comando para o CLP - SA.
        """

        try:
            if cls.verificar_permissivos_djl():
                return False
            else:
                res = cls.clp["SA"].write_single_coil(REG_SA["CMD_FECHA_DJL"], [1])
                return res

        except Exception:
            logger.error(f"[SE]  Houver um erro ao fechar o Disjuntor de Linha.")
            logger.debug(traceback.format_exc())


    @classmethod
    def verificar_permissivos_djl(cls) -> "bool":
        """
        Função para verificação das condições de fechamento do Disjuntor 52L (Linha).
        """

        return True

        flags = 0

        if cls.clp["SA"].read_discrete_inputs(REG_SA["DJL_ALM_PRESS_BAIXA"])[0] == 1:
            logger.debug("[SE]  O Alarme de Pressão Baixa do Gás do Disjuntor está ativo.")
            flags += 1

        if cls.clp["SA"].read_discrete_inputs(REG_SA["DJL_FALHA"])[0] == 1:
            logger.debug("[SE]  Há uma Falha Interna no Disjuntor")
            flags += 1

        if cls.clp["SA"].read_discrete_inputs(REG_SA["DJL_BLOQ_PRESS_BAIXA"])[0] == 1:
            logger.debug("[SE]  O Bloqueio de Pressão Baica do Gás do Disjuntor está ativo.")
            flags += 1

        if cls.clp["SA"].read_discrete_inputs(REG_SA["DJL_LOCAL"])[0] == 1:
            logger.debug("[SE]  O Disjuntor está em Modo Local.")
            flags += 1

        if cls.clp["SA"].read_discrete_inputs(REG_SA["DJL_MOLA_DESCARREGADA"])[0] == 1:
            logger.debug("[SE]  Mola do Disjuntor está Descarregada.")
            flags += 1

        if cls.clp["SA"].read_discrete_inputs(REG_SA["DJL_SUP_BOB_ABERT1"])[0] == 0:
            logger.debug("[SE]  DisjDJ1_SuperBobAbert1")
            flags += 1

        if cls.clp["SA"].read_discrete_inputs(REG_SA["DJL_SUP_BOB_ABERT2"])[0] == 0:
            logger.debug("[SE]  DisjDJ1_SuperBobAbert2")
            flags += 1

        if cls.clp["SA"].read_discrete_inputs(REG_SA["DJL_SUP_125VCC_CI_MOT"])[0] == 0:
            logger.debug("[SE]  DisjDJ1_Super125VccCiMot")
            flags += 1

        if cls.clp["SA"].read_discrete_inputs(REG_SA["DJL_SUP_125VCC_CI_COM"])[0] == 0:
            logger.debug("[SE]  DisjDJ1_Super125VccCiCom")
            flags += 1

        if cls.clp["SA"].read_discrete_inputs(REG_SA["DJL_SUP_125VCC_BOFEAB1"])[0] == 0:
            logger.debug("[SE]  DisjDJ1_Sup125VccBoFeAb1")
            flags += 1

        if cls.clp["SA"].read_discrete_inputs(REG_SA["DJL_SUP_125VCC_BOFEAB2"])[0] == 0:
            logger.debug("[SE]  DisjDJ1_Sup125VccBoFeAb2")
            flags += 1

        if flags > 0:
            logger.warning(f"[SE]  Foram detectados bloqueios ao fechar o Dj52L. Número de bloqueios: \"{flags}\".")
            return True
        else:
            return False


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
                logger.debug(f"[SE]  Foram detectados Condicionadores ativos na Subestação!")
            else:
                logger.debug(f"[SE]  Ainda há Condicionadores ativos na Subestação!")

            for condic in condics_ativos:
                # if condic.teste:
                #     logger.debug(f"[SE]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\", Obs.: \"TESTE\"")
                #     continue

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
                    autor += 1
                    sleep(1)

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

        return

        cls.l_trip_SEL311 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["SEL311_TRIP"], descricao="[SE] Trip SEL311")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_trip_SEL311, CONDIC_INDISPONIBILIZAR))

        cls.l_trip_SEL787 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["SEL787_TRIP"], descricao="[SE] Trip SEL787")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_trip_SEL787, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_SEL311 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["SEL311_FALHA"], descricao="[SE] Falha SEL311")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_SEL311, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_interna_SEL787 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["SEL787_FALHA"], descricao="[SE] Falha SEL787")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_interna_SEL787, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_interna_DJ52l = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["DJL_FALHA"], descricao="[SE] Falha Interna Disjuntor 52L")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_interna_DJ52l, CONDIC_INDISPONIBILIZAR))

        cls.l_secc_89TE_aberta = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["CTE_SECC_89TE_ABERTA"], descricao="[SE] Seccionadora 89TE Aberta")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_secc_89TE_aberta, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_TE = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["TE_FALHA"], descricao="[SE] Falha TE")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_TE, CONDIC_INDISPONIBILIZAR))

        cls.l_alarme_gas_TE = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["TE_ALM_DETEC_GAS"], descricao="[SE] Alarme Detector Gás TE")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alarme_gas_TE, CONDIC_INDISPONIBILIZAR))

        cls.l_alarme_temp_oleo_TE = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["TE_ALM_TEMP_OLEO"], descricao="[SE] Alarme Temperatura Óleo TE")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alarme_temp_oleo_TE, CONDIC_INDISPONIBILIZAR))

        cls.l_alarme_desligamento_TE = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["TE_ALM_DESLIGAMENTO"], descricao="[SE] Alarme Desligamento TE")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alarme_desligamento_TE, CONDIC_INDISPONIBILIZAR))

        cls.l_alarme_nv_max_oleo_TE = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["TE_ALM_NV_MAX_OLEO"], descricao="[SE] Alarme Nível Máximo Óleo TE")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alarme_nv_max_oleo_TE, CONDIC_INDISPONIBILIZAR))

        cls.l_alarme_alivio_pressao_TE = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["TE_ALM_ALIVIO_PRESSAO"], descricao="[SE] Alarme Alívio Pressão TE")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alarme_alivio_pressao_TE, CONDIC_INDISPONIBILIZAR))

        cls.l_alarme_temp_enrola_TE = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["TE_ALM_TEMP_ENROLA"], descricao="[SE] Alarme Temperatura Enrolamento TE")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alarme_temp_enrola_TE, CONDIC_INDISPONIBILIZAR))

        cls.l_targets_SEL787 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["SEL787_TARGET"], descricao="[SE] Targets SEL787")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_targets_SEL787, CONDIC_INDISPONIBILIZAR))

        cls.l_targets_SEL787_bit00 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["SEL787_TARGET_B00"], descricao="[SE] Targets SEL787 Bit 00")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_targets_SEL787_bit00, CONDIC_INDISPONIBILIZAR))

        # cls.l_targets_SEL787_bit01 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["SEL787_TARGET_B01"], descricao="[SE] Targets SEL787 Bit 01")
        # cls.condicionadores.append(c.CondicionadorBase(cls.l_targets_SEL787_bit01, CONDIC_INDISPONIBILIZAR))

        cls.l_targets_SEL787_bit02 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["SEL787_TARGET_B02"], descricao="[SE] Targets SEL787 Bit 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_targets_SEL787_bit02, CONDIC_INDISPONIBILIZAR))

        cls.l_targets_SEL787_bit03 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["SEL787_TARGET_B03"], descricao="[SE] Targets SEL787 Bit 03")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_targets_SEL787_bit03, CONDIC_INDISPONIBILIZAR))

        cls.l_targets_SEL787_bit04 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["SEL787_TARGET_B04"], descricao="[SE] Targets SEL787 Bit 04")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_targets_SEL787_bit04, CONDIC_INDISPONIBILIZAR))

        # cls.l_targets_SEL787_bit05 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["SEL787_TARGET_B05"], descricao="[SE] Targets SEL787 Bit 05")
        # cls.condicionadores.append(c.CondicionadorBase(cls.l_targets_SEL787_bit05, CONDIC_INDISPONIBILIZAR))

        # cls.l_targets_SEL787_bit06 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["SEL787_TARGET_B06"], descricao="[SE] Targets SEL787 Bit 06")
        # cls.condicionadores.append(c.CondicionadorBase(cls.l_targets_SEL787_bit06, CONDIC_INDISPONIBILIZAR))

        cls.l_targets_SEL787_bit07 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["SEL787_TARGET_B07"], descricao="[SE] Targets SEL787 Bit 07")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_targets_SEL787_bit07, CONDIC_INDISPONIBILIZAR))

