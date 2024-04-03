import pytz
import logging
import traceback

import src.mensageiro.dict as vd
import src.dicionarios.dict as d

from time import time, sleep
from datetime import datetime

import src.funcoes.leitura as lei
import src.funcoes.condicionador as c
import src.conectores.servidores as srv

from src.dicionarios.reg import *
from src.dicionarios.const import *

import src.conectores.banco_dados as bd


logger = logging.getLogger("logger")


class ServicoAuxiliar:

    clp = srv.Servidores.clp
    bd: "bd.BancoDados" = None

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_ativos: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []


    @staticmethod
    def get_time() -> "datetime":
        """
        Função para obter data e hora atual.
        """

        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

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
                logger.debug(f"[SA]  Foram detectados Condicionadores ativos na Subestação!")
            else:
                logger.debug(f"[SA]  Ainda há Condicionadores ativos na Subestação!")

            for condic in condics_ativos:
                # if condic.teste:
                #     logger.debug(f"[SA]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\", Obs.: \"TESTE\"")
                #     continue

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
                    autor += 1
                    sleep(1)

            logger.debug("")
            return condics_ativos

        else:
            cls.condicionadores_ativos = []
            return []


    @classmethod
    def leitura_temporizada(cls) -> None:
        """
        Função para consulta de acionamentos da usina e avisos através do mecanismo
        de acionamento temporizado.
        """
        return

        if cls.l_trip_dj52E.valor != 0:
            logger.warning("[SA]  O Disjuntor do Gerador Diesel de Emergência QLCF identificou um sinal de TRIP, favor verificar.")

        if cls.l_trip_dj_agrupamento.valor != 0:
            logger.warning("[SA]  O sensor do Disjuntor de Agrupamento QLCF identificou um sinal de trip, favor verificar.")

        if cls.l_subtensao_barramento_geral.valor != 0:
            logger.warning("[SA]  O sensor de Subtensão do Barramento Geral QCAP foi acionado, favor verificar.")

        if cls.l_alarme_GMG.valor != 0:
            logger.warning("[SA]  O alarme do Grupo Motor Gerador foi acionado, favor verificar.")

        if cls.l_trip_GMG.valor != 0:
            logger.warning("[SA]  O sensor de TRIP do Grupo Motor Gerador foi acionado, favor verificar.")

        if cls.l_operacao_GMG.valor != 0:
            logger.warning("[SA]  O sensor de operação do Grupo Motor Gerador foi acionado, favor verificar.")

        if cls.l_comb_baixo_GMG.valor != 0:
            logger.warning("[SA]  O sensor de de combustível do Grupo Motor Gerador retornou que o nível está baixo, favor reabastercer o gerador.")

        if cls.l_falha_acion_bomba_dren_1.valor != 0:
            logger.warning("[SA]  O sensor da Bomba de Drenagem 1 identificou uma falha no acionamento, favor verificar.")

        if cls.l_falha_acion_bomba_dren_2.valor != 0:
            logger.warning("[SA]  O sensor da Bomba de Drenagem 2 identificou uma falha no acionamento, favor verificar.")

        if cls.l_falha_acion_bomba_dren_3.valor != 0:
            logger.warning("[SA]  O sensor da Bomba de Drenagem 3 identificou uma falha no acionamento, favor verificar.")

        if cls.l_falha_aciona_GMG.valor != 0:
            logger.warning("[SA]  O sensor do Grupo Motor Gerador identificou uma falha no acionamento, favor verificar.")

        if cls.l_falha_comuni_SE_TDA.valor != 0 and not vd.voip_dict["FALHA_COMUM_SETDA"][0]:
            logger.warning("[SA]  Houve uma falha de comunicação com o CLP da Subestação e o CLP da Tomada da Água, favor verificar")
            vd.voip_dict["FALHA_COMUM_SETDA"][0] = True
        elif cls.l_falha_comuni_SE_TDA.valor == 0 and vd.voip_dict["FALHA_COMUM_SETDA"][0]:
            vd.voip_dict["FALHA_COMUM_SETDA"][0] = False
            vd.voip_dict["FALHA_COMUM_SETDA"][1] = 0

        if cls.l_dj52E_fechado.valor != 0 and not vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0]:
            logger.warning("[SA]  O Disjuntor do Gerador Diesel de Emergência QLCF foi fechado.")
            vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0] = True
        elif cls.l_dj52E_fechado.valor == 0 and vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0]:
            vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0] = False
            vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][1] = 0

        if cls.l_bombas_dren_modo_auto.valor != 1 and not vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0]:
            logger.warning("[SA]  O poço de drenagem da Usina entrou em modo remoto, favor verificar.")
            vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0] = True
        elif cls.l_bombas_dren_modo_auto.valor == 1 and vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0]:
            vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0] = False
            vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][1] = 0

        return


    @classmethod
    def carregar_leituras(cls) -> None:
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """

        return

        # Leituras Periódicas
        cls.l_trip_dj52E = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QLCF_DJ_52E_TRIP"], descr="[SA] Trip Disjuntor 52E")
        cls.l_dj52E_fechado = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCAP_DJ_52E_FECHADO"], descr="[SA] Disjuntor 52E Fechado")
        cls.l_trip_dj_agrupamento = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QLCF_TRIP_DJ_AGRUP"], descr="[SA] Disjuntor Agrupamento Trip")
        cls.l_trip_GMG = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["GMG_TRIP"], descr="[SA] Trip GMG")
        cls.l_alarme_GMG = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["GMG_ALARME"], descr="[SA] Alarme GMG")
        cls.l_operacao_GMG = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["GMG_OPERACAO"], descr="[SA] Operação GMG")
        cls.l_comb_baixo_GMG = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["GMG_BAIXO_COMBs"], descr="[SA] Combustível Baixo GMG")
        cls.l_falha_aciona_GMG = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["GMG_FALHA_ACION"], descr="[SA] Falha Acionamento GMG")
        cls.l_falha_comuni_SE_TDA = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["SE_TDA_FALHA_COMUNICA"], descr="[SA] Falha Comunicação CLPs SE TDA ")
        cls.l_bombas_dren_modo_auto = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCADE_BOMBAS_DREN_AUTO"], descr="[SA] Bombas Drenagem Modo Automático")
        cls.l_falha_acion_bomba_dren_1 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCADE_BOMBA_DREN1_FALHA"], descr="[SA] Falha Acionamento Bomba Drenagem 1")
        cls.l_falha_acion_bomba_dren_2 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCADE_BOMBA_DREN2_FALHA"], descr="[SA] Falha Acionamento Bomba Drenagem 2")
        cls.l_falha_acion_bomba_dren_3 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCADE_BOMBA_DREN3_FALHA"], descr="[SA] Falha Acionamento Bomba Drenagem 3")
        cls.l_subtensao_barramento_geral = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCAP_SUBTENSAO_BARRA_GERAL"], descr="[SA] Subtensão Barramento Geral")

        # CONDICIONADORES ESSENCIAIS
        # cls.l_tensao_presente_TSA = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCAP_TENSAO_PRES_TSA"], descr="[SA] Tensão Presente TSA")
        # cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_tensao_presente_TSA, CONDIC_NORMALIZAR))

        cls.l_trip_MRU3 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["MRU3_TRIP"], descr="[SA] Trip MRU3")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_trip_MRU3, CONDIC_INDISPONIBILIZAR))

        cls.l_trip_MRL1 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["MRL1_TRIP"], descr="[SA] Trip MRL1")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_trip_MRL1, CONDIC_INDISPONIBILIZAR))

        cls.l_trip_dj52E1 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCADE_DJ_52E1_TRIP"], descr="[SA] Trip Dijuntor 52E1")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_trip_dj52E1, CONDIC_INDISPONIBILIZAR))

        # CONDICIONADORES
        cls.l_falha_MRU3 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["MRU3_FALHA"], descr="[SA] Falha MRU3")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_MRU3, CONDIC_INDISPONIBILIZAR))

        cls.l_falta_125Vcc_CTE = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["CTE_FALTA_125VCC"], descr="[SA] Falta 125 Vcc CTE")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falta_125Vcc_CTE, CONDIC_INDISPONIBILIZAR))

        cls.l_secc_CSA1_aberta = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["CSA1_SECC_ABERTA"], descr="[SA] Seccionadora CSA1 Aberta")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_secc_CSA1_aberta, CONDIC_INDISPONIBILIZAR))

        cls.l_fusivel_queimado_CSA1 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["CSA1_FUSIVEL_QUEIMADO"], descr="[SA] CSA1 Fusível Queimado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_fusivel_queimado_CSA1, CONDIC_INDISPONIBILIZAR))

        cls.l_falta_tensao_125Vcc_CSA1 = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["CSA1_FALTA_TENSAO_125VCC"], descr="[SA] Falta Tensão 125 Vcc CSA1")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falta_tensao_125Vcc_CSA1, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_dj_protecao_TP = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["FALHA_DJ_TPS_PROT"], descr="[SA] Falha Disjuntor Proteção Transformador Potencial")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_dj_protecao_TP, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_dj_sincr_TP = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["FALHA_DJ_TPS_SINCR"], descr="[SA] Falha Disjuntor Sincronizador Transformador Potencial")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_dj_sincr_TP, CONDIC_INDISPONIBILIZAR))

        cls.l_nv_4_QCADE = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCADE_NV_4"], descr="[SA] Drenagem CA Nível 4")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_nv_4_QCADE, CONDIC_INDISPONIBILIZAR))

        cls.l_nivel_muito_alto_QCADE = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCADE_NV_MUITO_ALTO"], descr="[SA] Nível Muito Alto Drenagem CA")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_nivel_muito_alto_QCADE, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_220VCA_QCADE = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCADE_FALHA_220VCA"], descr="[SA] Falha 220 VCA Drenagem CA")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_220VCA_QCADE, CONDIC_INDISPONIBILIZAR))

        cls.l_trip_dj72E_QCCP = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCCP_DJ_72E_TRIP"], descr="[SA] Trip Disjuntor 72E QCCP")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_trip_dj72E_QCCP, CONDIC_INDISPONIBILIZAR))

        cls.l_falta_125Vcc_QCCP = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCCP_FALTA_125VCC"], descr="[SA] Falta 125 Vcc QCCP")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falta_125Vcc_QCCP, CONDIC_INDISPONIBILIZAR))

        cls.l_trip_dj_agrup_QCCP = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCCP_TRIP_DJ_AGRUP"], descr="[SA] Trip Disjuntor Agrupamento QCCP")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_trip_dj_agrup_QCCP, CONDIC_INDISPONIBILIZAR))

        cls.l_falta_125Vcc_QCAP = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCAP_FALTA_125VCC"], descr="[SA] Falta 125 Vcc CA Principal")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falta_125Vcc_QCAP, CONDIC_INDISPONIBILIZAR))

        cls.l_trip_dj_agrup_QCAP = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCAP_TRIP_DJ_AGRUP"], descr="[SA] Trip Disjuntor Agrupamento CA Principal")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_trip_dj_agrup_QCAP, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_dj_52A1_QCAP = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCAP_DJ_52A1_FALHA"], descr="[SA] Falha Disjuntor 52A1 CA Principal")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_dj_52A1_QCAP, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_dj_52E_QCAP = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["QCAP_DJ_52E_FALHA"], descr="[SA] Falha Disjuntor 52E CA Principal")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_dj_52E_QCAP, CONDIC_INDISPONIBILIZAR))

        # cls.l_dj_GMG_fechado = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["GMG_DJ_FECHADO"], descr="[SA] Disjuntor GMG Fechado")
        # cls.condicionadores.append(c.CondicionadorBase(cls.l_dj_GMG_fechado, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_CLP = lei.LeituraModbusCoil(cls.clp["SA"], REG_SA["CLP_FALHA_COMUNICA"], descr="[SA] Falha CLP SA")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_falha_CLP, CONDIC_INDISPONIBILIZAR))
        return

