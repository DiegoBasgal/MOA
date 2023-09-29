__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação do Serviço Auxiliar."

import logging
import traceback

import src.dicionarios.dict as dct

from src.funcoes.leitura import *
from src.dicionarios.const import *
from src.funcoes.condicionadores import *

from src.conectores.servidores import Servidores
from src.funcoes.escrita import EscritaModBusBit as EMB

logger = logging.getLogger("logger")

class ServicoAuxiliar:

    # ATRIBUIÇÃO DE VARIÁVEIS

    clp = Servidores.clp

    condicionadores: "list[CondicionadorBase]" = []
    condicionadores_essenciais: "list[CondicionadorBase]" = []

    @classmethod
    def resetar_emergencia(cls) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SA"]["BARRA_CA_RST_FLH"], valor=1)
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SA"]["SIS_AGUA_RST_FLH"], valor=1)
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SA"]["BLQ_GERAL_FLH_SA_REARME"], valor=1)
            return res

        except Exception:
            logger.exception(f"[SA]  Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(f"[SA]  Traceback: {traceback.format_exc()}")
            return False

    @classmethod
    def verificar_condicionadores(cls) -> "list[CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

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

        if cls.l_falha_bomba_dren_1.valor:
            logger.warning("[SA]  Houve uma falha na bomba 1 do poço de drenagem. Favor verificar.")

        if cls.l_falha_bomba_dren_2.valor:
            logger.warning("[SA]  Houve uma falha na bomba 2 do poço de drenagem. Favor verificar.")

        if cls.l_falha_bomba_dren_3.valor:
            logger.warning("[SA]  Houve uma falha na bomba 3 do poço de drenagem. Favor verificar.")

        if cls.l_sis_agua_falha_ligar_bomba.valor:
            logger.warning("[SA]  Houve uma falha ao ligar a bomba do sistema de água. Favor verificar.")

        if cls.l_djs_barra_sel_remoto.valor:
            logger.warning("[SA]  Os disjuntores da barra seletora saíram do modo remoto. Favor verificar.")

        if not cls.l_sis_agua_bomba_disp.valor:
            logger.warning("[SA]  Foi identificado que a bomba do sistema de água está indisponível. Favor verificar.")

        if cls.l_poco_dren_dicrepancia.valor:
            logger.warning("[SA]  Foram identificados sinais inconsistentes nas boias do poço de drenagem. Favor verificar.")

        if cls.l_falha_partida_gmg.valor and not dct.voip["GMG_FALHA_PARTIR"][0]:
            logger.warning("[SA]  Houve uma falha ao partir o Gerador Diesel. Favor verificar.")
            dct.voip["GMG_FALHA_PARTIR"][0] = True
        elif not cls.l_falha_partida_gmg.valor and dct.voip["GMG_FALHA_PARTIR"][0]:
            dct.voip["GMG_FALHA_PARTIR"][0] = False

        if cls.l_falha_parada_gmg.valor and not dct.voip["GMG_FALHA_PARAR"][0]:
            logger.warning("[SA]  Houve uma falha ao parar o Gerador Diesel. Favor verificar.")
            dct.voip["GMG_FALHA_PARAR"][0] = True
        elif not cls.l_falha_parada_gmg.valor and dct.voip["GMG_FALHA_PARAR"][0]:
            dct.voip["GMG_FALHA_PARAR"][0] = False

        if cls.l_gmg_manual.valor and not dct.voip["GMG_OPERACAO_MANUAL"][0]:
            logger.warning("[SA]  O Gerador Diesel saiu do modo remoto. Favor verificar.")
            dct.voip["GMG_OPERACAO_MANUAL"][0] = True
        elif not cls.l_gmg_manual.valor and dct.voip["GMG_OPERACAO_MANUAL"][0]:
            dct.voip["GMG_OPERACAO_MANUAL"][0] = False

        if not cls.l_52SA1_sem_falha.valor and not dct.voip["52SA1_SEM_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha com o disjuntor 52SA1 do transformador do SA. Favor verificar.")
            dct.voip["52SA1_SEM_FALHA"][0] = True
        elif cls.l_52SA1_sem_falha.valor and dct.voip["52SA1_SEM_FALHA"][0]:
            dct.voip["52SA1_SEM_FALHA"][0] = False

        if not cls.l_52SA2_sem_falha.valor and not dct.voip["52SA2_SEM_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha com o disjuntor 52SA2 do Gerador Diesel. Favor verificar.")
            dct.voip["52SA2_SEM_FALHA"][0] = True
        elif cls.l_52SA2_sem_falha.valor and dct.voip["52SA2_SEM_FALHA"][0]:
            dct.voip["52SA2_SEM_FALHA"][0] = False

        if not cls.l_52SA3_sem_falha.valor and not dct.voip["52SA3_SEM_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciais. Favor verificar.")
            dct.voip["52SA3_SEM_FALHA"][0] = True
        elif cls.l_52SA3_sem_falha.valor and dct.voip["52SA3_SEM_FALHA"][0]:
            dct.voip["52SA3_SEM_FALHA"][0] = False

        if cls.l_falha_bomba_filtragem.valor and not dct.voip["FILTRAGEM_BOMBA_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha na bomba de filtragem. Favor verificar.")
            dct.voip["FILTRAGEM_BOMBA_FALHA"][0] = True
        elif not cls.l_falha_bomba_filtragem.valor and dct.voip["FILTRAGEM_BOMBA_FALHA"][0]:
            dct.voip["FILTRAGEM_BOMBA_FALHA"][0] = False

        if cls.l_nivel_alto_poco_dren.valor and not dct.voip["POCO_DRENAGEM_NIVEL_ALTO"][0]:
            logger.warning("[SA]  Nível do poço de drenagem alto. Favor verificar.")
            dct.voip["POCO_DRENAGEM_NIVEL_ALTO"][0] = True
        elif not cls.l_nivel_alto_poco_dren.valor and dct.voip["POCO_DRENAGEM_NIVEL_ALTO"][0]:
            dct.voip["POCO_DRENAGEM_NIVEL_ALTO"][0] = False

        if cls.l_falha_bomba_dren_uni.valor and not dct.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha na bomba de drenagem. Favor verificar.")
            dct.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0] = True
        elif not cls.l_falha_bomba_dren_uni.valor and dct.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0]:
            dct.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0] = False

        if cls.l_nivel_muito_alto_poco_dren.valor and not dct.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0]:
            logger.warning("[SA]  Nível do poço de drenagem está muito alto. Favor verificar.")
            dct.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0] = True
        elif not cls.l_nivel_muito_alto_poco_dren.valor and dct.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0]:
            dct.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0] = False

        if cls.l_alarme_sis_incendio_atuado.valor and not dct.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0]:
            logger.warning("[SA]  O alarme do sistema de incêndio foi acionado. Favor verificar.")
            dct.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0] = True
        elif not cls.l_alarme_sis_incendio_atuado.valor and dct.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0]:
            dct.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0] = False

        if cls.l_alarme_sis_seguranca_atuado.valor and not dct.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0]:
            logger.warning("[SA]  O alarme do sistem de seguraça foi acionado. Favor verificar.")
            dct.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0] = True
        elif not cls.l_alarme_sis_seguranca_atuado.valor and dct.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0]:
            dct.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0] = False

        # if cls.l_falha_tubo_succao_bomba_recalque.valor and not dct.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0]:
        #     logger.warning("[SA]  Houve uma falha na sucção da bomba de recalque. Favor verificar.")
        #     dct.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0] = True
        # elif not cls.l_falha_tubo_succao_bomba_recalque.valor and dct.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0]:
        #     dct.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0] = False

    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """
        return
        ### CONDICIONADORES ESSENCIAIS
        ## NORMALIZAR
        cls.l_emergencia = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SEM_EMERGENCIA"], invertido=True, descricao="[SA]  Emergência")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.l_emergencia, CONDIC_NORMALIZAR))

        ### CONDICIONADORES
        ## NORMALIZAR

        # Retificador
        cls.l_reti_subtensao = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["RETI_SUBTEN"], descricao="[SA]  Retificador Subtensão")
        cls.condicionadores.append(CondicionadorBase(cls.l_reti_subtensao, CONDIC_NORMALIZAR))

        cls.l_reti_sobretensao = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["RETI_SOBRETEN"], descricao="[SA]  Retificador Sobretensão")
        cls.condicionadores.append(CondicionadorBase(cls.l_reti_sobretensao, CONDIC_NORMALIZAR))

        cls.l_reti_sobrecorrente_saida = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["RETI_SOBRECO_SAIDA"], descricao="[SA]  Retificador Sobrecorrente Saída")
        cls.condicionadores.append(CondicionadorBase(cls.l_reti_sobrecorrente_saida, CONDIC_NORMALIZAR))

        cls.l__reti_sobrecorrente_baterias = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["RETI_SOBRECO_BATERIAS"], descricao="[SA]  Retificador Sobrecorrente Baterias")
        cls.condicionadores.append(CondicionadorBase(cls.l__reti_sobrecorrente_baterias, CONDIC_NORMALIZAR))

        # Sistema de Água
        cls.l_sis_agua_falha_pressurizar_filtroA = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SIS_AGUA_FLH_PRESSURIZAR_FILTRO_A"], descricao="[SA]  Sistema Água Falha Pressurizar Filtro A")
        cls.condicionadores.append(CondicionadorBase(cls.l_sis_agua_falha_pressurizar_filtroA, CONDIC_NORMALIZAR))

        cls.l_sis_agua_falha_pressostato_filtroA = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SIS_AGUA_FLH_PRESSOSTATO_FILTRO_A"], descricao="[SA]  Sistema Água Falha Pressostato Filtro A")
        cls.condicionadores.append(CondicionadorBase(cls.l_sis_agua_falha_pressostato_filtroA, CONDIC_NORMALIZAR))

        cls.l_sis_agua_falha_pressurizar_fitroB = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SIS_AGUA_FLH_PRESSURIZAR_FILTRO_B"], descricao="[SA]  Sistema Água Falha Pressurizar Filtro B")
        cls.condicionadores.append(CondicionadorBase(cls.l_sis_agua_falha_pressurizar_fitroB, CONDIC_NORMALIZAR))

        cls.l_sis_agua_falha_pressostato_filtroB = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SIS_AGUA_FLH_PRESSOSTATO_FILTRO_B"], descricao="[SA]  Sistema Água Falha Pressostato Filtro B")
        cls.condicionadores.append(CondicionadorBase(cls.l_sis_agua_falha_pressostato_filtroB, CONDIC_NORMALIZAR))

        ## INDISPONIBILIZAR

        # Disjuntores
        cls.l_falha_52SA1 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DJ52SA1_SEM_FLH"], invertido=True, descricao="[SA]  Disjuntor 52SA1 Sem Falha")
        cls.condicionadores.append(CondicionadorBase(cls.l_falha_52SA1, CONDIC_INDISPONIBILIZAR))

        cls.l_72SA1_fechado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DJ72SA1_FECHADO"], invertido=True, descricao="[SA]  Disjuntor 72SA1 Fechado")
        cls.condicionadores.append(CondicionadorBase(cls.l_72SA1_fechado, CONDIC_INDISPONIBILIZAR))

        cls.l_djs24VCC_fechados = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DJS_24VCC_FECHADOS"], invertido=True, descricao="[SA]  Disjuntores 24Vcc Fechados")
        cls.condicionadores.append(CondicionadorBase(cls.l_djs24VCC_fechados, CONDIC_INDISPONIBILIZAR))

        cls.l_djs125VCC_fechados = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DJS_125VCC_FECHADOS"], invertido=True, descricao="[SA]  Disjuntores 125Vcc Fechados")
        cls.condicionadores.append(CondicionadorBase(cls.l_djs125VCC_fechados, CONDIC_INDISPONIBILIZAR))

        cls.l_cmd_24VCC_tensao = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["CMD_24VCC_COM_TENSAO"], invertido=True, descricao="[SA]  Comando 24Vcc Com Tensão")
        cls.condicionadores.append(CondicionadorBase(cls.l_cmd_24VCC_tensao, CONDIC_INDISPONIBILIZAR))

        cls.l_cmd_125VCC_tensao = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["CMD_125VCC_COM_TENSAO"], invertido=True, descricao="[SA]  Comando 125Vcc Com Tensão")
        cls.condicionadores.append(CondicionadorBase(cls.l_cmd_125VCC_tensao, CONDIC_INDISPONIBILIZAR))

        cls.l_alimentacao_125VCC_tensao = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["ALIM_125VCC_COM_TENSAO"], invertido=True, descricao="[SA]  Alimentação 125Vcc Com Tensão")
        cls.condicionadores.append(CondicionadorBase(cls.l_alimentacao_125VCC_tensao, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_abertura_52SA1 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DJ52SA1_FLH_ABRIR"], descricao="[SA]  Disjuntor 52SA1 Falha Abertura")
        cls.condicionadores.append(CondicionadorBase(cls.l_falha_abertura_52SA1, CONDIC_INDISPONIBILIZAR))

        cls.l_fechamento_52SA1 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DJ52SA1_FLH_FECHAR"], descricao="[SA]  Disjuntor 52SA1 Falha Fechamento")
        cls.condicionadores.append(CondicionadorBase(cls.l_fechamento_52SA1, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_abertura_52SA2 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DJ52SA2_FLH_ABRIR"], descricao="[SA]  Disjuntor 52SA2 Falha Abertura")
        cls.condicionadores.append(CondicionadorBase(cls.l_falha_abertura_52SA2, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_fechamento_52SA2 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DJ52SA2_FLH_FECHAR"], descricao="[SA]  Disjuntor 52SA2 Falha Fechamento")
        cls.condicionadores.append(CondicionadorBase(cls.l_falha_fechamento_52SA2, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_abertura_52SA3 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DJ52SA3_FLH_ABRIR"], descricao="[SA]  Disjuntor 52SA3 Falha Abertura")
        cls.condicionadores.append(CondicionadorBase(cls.l_falha_abertura_52SA3, CONDIC_INDISPONIBILIZAR))

        cls.l_falha_fechamento_52SA3 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DJ52SA3_FLH_FECHAR"], descricao="[SA]  Disjuntor 52SA3 Falha Fechamento")
        cls.condicionadores.append(CondicionadorBase(cls.l_falha_fechamento_52SA3, CONDIC_INDISPONIBILIZAR))

        # Retificador
        cls.l_reti_fusivel_queimado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["RETI_FUSIVEL_QUEIMADO"], descricao="[SA]  Retificador Fusível Queimado")
        cls.condicionadores.append(CondicionadorBase(cls.l_reti_fusivel_queimado, CONDIC_INDISPONIBILIZAR))

        cls.l_reti_fuga_terra_pos = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["RETI_FUGA_TERRA_POSITIVO"], descricao="[SA]  Retificador Fuga Terra Positivo")
        cls.condicionadores.append(CondicionadorBase(cls.l_reti_fuga_terra_pos, CONDIC_INDISPONIBILIZAR))

        cls.l_reti_fuga_terra_neg = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["RETI_FUGA_TERRA_NEGATIVO"], descricao="[SA]  Retificador Fuga Terra Negativo")
        cls.condicionadores.append(CondicionadorBase(cls.l_reti_fuga_terra_neg, CONDIC_INDISPONIBILIZAR))

        # LEITURA PERIODICA
        cls.l_sis_agua_bomba_disp = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SIS_AGUA_BOMBA_DISPONIVEL"], invertido=True, descricao="[SA]  Sistem Água Bomba Disponível")

        cls.l_falha_bomba_dren_1 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["BOMBA_DREN_1_FLH"], descricao="[SA]  Bomba Drenagem 1 Falha")
        cls.l_falha_bomba_dren_2 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["BOMBA_DREN_2_FLH"], descricao="[SA]  Bomba Drenagem 2 Falha")
        cls.l_falha_bomba_dren_3 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["BOMBA_DREN_3_FLH"], descricao="[SA]  Bomba Drenagem 3 Falha")
        cls.l_poco_dren_dicrepancia = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["POCO_DREN_DISCRE_BOIAS"], descricao="[SA]  Boias Poço Drenagem Discrepância")
        cls.l_sis_agua_falha_ligar_bomba = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SIS_AGUA_FLH_LIGA_BOMBA"], descricao="[SA]  Sistema Água Falha Ligar Bomba")
        cls.l_djs_barra_sel_remoto = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DJS_BARRA_SELETORA_REMOTO"], descricao="[SA]  Disjuntores Barra Seletora Modo Remoto")

        cls.l_52SA1_sem_falha = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DJ52SA1_SEM_FLH"], invertido=True, descricao="[SA]  Disjuntor 52SA1 Sem Falha")
        cls.l_52SA2_sem_falha = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DJ52SA2_SEM_FLH"], invertido=True, descricao="[SA]  Disjuntor 52SA2 Sem Falha")
        cls.l_52SA3_sem_falha = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DJ52SA3_SEM_FLH"], invertido=True, descricao="[SA]  Disjuntor 52SA3 Sem Falha")

        cls.l_falha_parada_gmg = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["GMG_FLH_PARAR"], descricao="[SA]  Grupo Motor Gerador Falha Parada")
        cls.l_falha_partida_gmg = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["GMG_FLH_PARTIR"], descricao="[SA]  Grupo Motor Gerador Falha Partida")
        cls.l_gmg_manual = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["GMG_OPERACAO_MANUAL"], descricao="[SA]  Grupo Motor Gerador Modo Operação Manual")
        cls.l_falha_bomba_filtragem = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["BOMBA_FILT_FLH"], descricao="[SA]  Bomba Filtragem Falha")
        cls.l_nivel_alto_poco_dren = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["POCO_DREN_NV_ALTO"], descricao="[SA]  Poço Drenagem Nível Alto")
        cls.l_falha_bomba_dren_uni = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["BOMBA_DREN_UNIDADES_FLH"], descricao="[SA]  Bomba Drenagem Unidades Falha")
        cls.l_alarme_sis_incendio_atuado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SIS_INCENDIO_ALM_ATUADO"], descricao="[SA]  Sistem Incêndio Alarme Atuado")
        cls.l_alarme_sis_seguranca_atuado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SIS_SEGURANCA_ALM_ATUADO"], descricao="[SA]  Sistema Segurança Alarme Atuado")
        cls.l_nivel_muito_alto_poco_dren = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["POCO_DREN_NV_MUITO_ALTO"], descricao="[SA]  Poço Drenagem Nível Muito Alto")
        # cls.l_falha_tubo_succao_bomba_recalque = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"],, descricao="[SA]  Bomba Recalque Falha Tubo Sucção")