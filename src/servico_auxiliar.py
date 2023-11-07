__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação do Serviço Auxiliar."

import pytz
import logging
import traceback

import src.dicionarios.dict as dct

from datetime import datetime

from src.funcoes.leitura import *
from src.dicionarios.const import *
from src.funcoes.condicionadores import *

from src.conectores.servidores import Servidores
from src.conectores.banco_dados import BancoDados
from src.funcoes.escrita import EscritaModBusBit as EMB


logger = logging.getLogger("logger")


class ServicoAuxiliar:
    def __init__(self, serv: "Servidores"=None, bd: "BancoDados"=None) -> None:
        pass
        # ATRIBUIÇÃO DE VARIÁVEIS

        self.__bd = bd

        self.clp = serv.clp

        self.condicionadores: "list[CondicionadorBase]" = []
        self.condicionadores_essenciais: "list[CondicionadorBase]" = []
        self.condicionadores_ativos: "list[CondicionadorBase]" = []


    def resetar_emergencia(self) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = EMB.escrever_bit(self.clp["SA"], REG_CLP["SA"]["BARRA_CA_RST_FLH"], valor=1)
            res = EMB.escrever_bit(self.clp["SA"], REG_CLP["SA"]["SIS_AGUA_RST_FLH"], valor=1)
            res = EMB.escrever_bit(self.clp["SA"], REG_CLP["SE"]["BLQ_GERAL_FLH_SA_REARME"], valor=1)
            return res

        except Exception:
            logger.exception(f"[SA]  Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(f"[SA]  Traceback: {traceback.format_exc()}")
            return False


    def verificar_condicionadores(self) -> "list[CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if self.condicionadores_ativos == []:
                logger.warning(f"[SA]  Foram detectados Condicionadores ativos no Serviço Auxiliar!")

            else:
                logger.info(f"[SA]  Ainda há Condicionadores ativos no Serviço Auxiliar!")

            for condic in condics_ativos:
                if condic in self.condicionadores_ativos:
                    logger.debug(f"[SA]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue
                else:
                    logger.warning(f"[SA]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    self.__bd.update_alarmes([datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descricao])

            logger.debug("")
            return condics_ativos

        else:
            self.condicionadores_ativos = []
            return []


    def verificar_leituras(self) -> "None":
        """
        Função para verificação de leituras por acionamento temporizado.

        Verifica leituras específcas para acionamento da manuteção. As leituras são disparadas
        em períodos separados por um tempo pré-definido.
        """

        if self.l_falha_bomba_dren_1.valor:
            logger.warning("[SA]  Houve uma falha na bomba 1 do poço de drenagem. Favor verificar.")

        if self.l_falha_bomba_dren_2.valor:
            logger.warning("[SA]  Houve uma falha na bomba 2 do poço de drenagem. Favor verificar.")

        if self.l_falha_bomba_dren_3.valor:
            logger.warning("[SA]  Houve uma falha na bomba 3 do poço de drenagem. Favor verificar.")

        if self.l_sis_agua_falha_ligar_bomba.valor:
            logger.warning("[SA]  Houve uma falha ao ligar a bomba do sistema de água. Favor verificar.")

        if self.l_djs_barra_sel_remoto.valor:
            logger.warning("[SA]  Os disjuntores da barra seletora saíram do modo remoto. Favor verificar.")

        if not self.l_sis_agua_bomba_disp.valor:
            logger.warning("[SA]  Foi identificado que a bomba do sistema de água está indisponível. Favor verificar.")

        if self.l_poco_dren_dicrepancia.valor:
            logger.warning("[SA]  Foram identificados sinais inconsistentes nas boias do poço de drenagem. Favor verificar.")

        if self.l_falha_partida_gmg.valor and not dct.voip["GMG_FALHA_PARTIR"][0]:
            logger.warning("[SA]  Houve uma falha ao partir o Gerador Diesel. Favor verificar.")
            dct.voip["GMG_FALHA_PARTIR"][0] = True
        elif not self.l_falha_partida_gmg.valor and dct.voip["GMG_FALHA_PARTIR"][0]:
            dct.voip["GMG_FALHA_PARTIR"][0] = False

        if self.l_falha_parada_gmg.valor and not dct.voip["GMG_FALHA_PARAR"][0]:
            logger.warning("[SA]  Houve uma falha ao parar o Gerador Diesel. Favor verificar.")
            dct.voip["GMG_FALHA_PARAR"][0] = True
        elif not self.l_falha_parada_gmg.valor and dct.voip["GMG_FALHA_PARAR"][0]:
            dct.voip["GMG_FALHA_PARAR"][0] = False

        if self.l_gmg_manual.valor and not dct.voip["GMG_OPERACAO_MANUAL"][0]:
            logger.warning("[SA]  O Gerador Diesel saiu do modo remoto. Favor verificar.")
            dct.voip["GMG_OPERACAO_MANUAL"][0] = True
        elif not self.l_gmg_manual.valor and dct.voip["GMG_OPERACAO_MANUAL"][0]:
            dct.voip["GMG_OPERACAO_MANUAL"][0] = False

        if not self.l_52SA1_sem_falha.valor and not dct.voip["52SA1_SEM_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha com o disjuntor 52SA1 do transformador do SA. Favor verificar.")
            dct.voip["52SA1_SEM_FALHA"][0] = True
        elif self.l_52SA1_sem_falha.valor and dct.voip["52SA1_SEM_FALHA"][0]:
            dct.voip["52SA1_SEM_FALHA"][0] = False

        if not self.l_52SA2_sem_falha.valor and not dct.voip["52SA2_SEM_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha com o disjuntor 52SA2 do Gerador Diesel. Favor verificar.")
            dct.voip["52SA2_SEM_FALHA"][0] = True
        elif self.l_52SA2_sem_falha.valor and dct.voip["52SA2_SEM_FALHA"][0]:
            dct.voip["52SA2_SEM_FALHA"][0] = False

        if not self.l_52SA3_sem_falha.valor and not dct.voip["52SA3_SEM_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciais. Favor verificar.")
            dct.voip["52SA3_SEM_FALHA"][0] = True
        elif self.l_52SA3_sem_falha.valor and dct.voip["52SA3_SEM_FALHA"][0]:
            dct.voip["52SA3_SEM_FALHA"][0] = False

        if self.l_falha_bomba_filtragem.valor and not dct.voip["FILTRAGEM_BOMBA_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha na bomba de filtragem. Favor verificar.")
            dct.voip["FILTRAGEM_BOMBA_FALHA"][0] = True
        elif not self.l_falha_bomba_filtragem.valor and dct.voip["FILTRAGEM_BOMBA_FALHA"][0]:
            dct.voip["FILTRAGEM_BOMBA_FALHA"][0] = False

        if self.l_nivel_alto_poco_dren.valor and not dct.voip["POCO_DRENAGEM_NIVEL_ALTO"][0]:
            logger.warning("[SA]  Nível do poço de drenagem alto. Favor verificar.")
            dct.voip["POCO_DRENAGEM_NIVEL_ALTO"][0] = True
        elif not self.l_nivel_alto_poco_dren.valor and dct.voip["POCO_DRENAGEM_NIVEL_ALTO"][0]:
            dct.voip["POCO_DRENAGEM_NIVEL_ALTO"][0] = False

        if self.l_falha_bomba_dren_uni.valor and not dct.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha na bomba de drenagem. Favor verificar.")
            dct.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0] = True
        elif not self.l_falha_bomba_dren_uni.valor and dct.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0]:
            dct.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0] = False

        if self.l_nivel_muito_alto_poco_dren.valor and not dct.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0]:
            logger.warning("[SA]  Nível do poço de drenagem está muito alto. Favor verificar.")
            dct.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0] = True
        elif not self.l_nivel_muito_alto_poco_dren.valor and dct.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0]:
            dct.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0] = False

        if self.l_alarme_sis_incendio_atuado.valor and not dct.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0]:
            logger.warning("[SA]  O alarme do sistema de incêndio foi acionado. Favor verificar.")
            dct.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0] = True
        elif not self.l_alarme_sis_incendio_atuado.valor and dct.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0]:
            dct.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0] = False

        if self.l_alarme_sis_seguranca_atuado.valor and not dct.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0]:
            logger.warning("[SA]  O alarme do sistem de seguraça foi acionado. Favor verificar.")
            dct.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0] = True
        elif not self.l_alarme_sis_seguranca_atuado.valor and dct.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0]:
            dct.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0] = False

        if self.l_falha_tubo_succao_bomba_recalque.valor and not dct.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha na sucção da bomba de recalque. Favor verificar.")
            dct.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0] = True
        elif not self.l_falha_tubo_succao_bomba_recalque.valor and dct.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0]:
            dct.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0] = False


    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """

        # CONDICIONADORES ESSENCIAIS
        self.l_bloq_geral = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["BLQ_GERAL"], descricao="[SA]  Bloqueio Geral Acionado")
        self.condicionadores_essenciais.append(CondicionadorBase(self.l_bloq_geral, CONDIC_NORMALIZAR))


        # CONDICIONADORES
        self.l_reti_subtensao = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["RETI_SUBTEN"], descricao="[SA]  Retificador Subtensão")
        self.condicionadores.append(CondicionadorBase(self.l_reti_subtensao, CONDIC_NORMALIZAR))

        self.l_reti_sobretensao = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["RETI_SOBRETEN"], descricao="[SA]  Retificador Sobretensão")
        self.condicionadores.append(CondicionadorBase(self.l_reti_sobretensao, CONDIC_NORMALIZAR))

        self.l_reti_sobrecorrente_saida = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["RETI_SOBRECO_SAIDA"], descricao="[SA]  Retificador Sobrecorrente Saída")
        self.condicionadores.append(CondicionadorBase(self.l_reti_sobrecorrente_saida, CONDIC_NORMALIZAR))

        self.l__reti_sobrecorrente_baterias = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["RETI_SOBRECO_BATERIAS"], descricao="[SA]  Retificador Sobrecorrente Baterias")
        self.condicionadores.append(CondicionadorBase(self.l__reti_sobrecorrente_baterias, CONDIC_NORMALIZAR))

        self.l_sis_agua_falha_pressurizar_filtroA = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SIS_AGUA_FLH_PRESSURIZAR_FILTRO_A"], descricao="[SA]  Sistema Água Falha Pressurizar Filtro A")
        self.condicionadores.append(CondicionadorBase(self.l_sis_agua_falha_pressurizar_filtroA, CONDIC_NORMALIZAR))

        self.l_sis_agua_falha_pressostato_filtroA = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SIS_AGUA_FLH_PRESSOSTATO_FILTRO_A"], descricao="[SA]  Sistema Água Falha Pressostato Filtro A")
        self.condicionadores.append(CondicionadorBase(self.l_sis_agua_falha_pressostato_filtroA, CONDIC_NORMALIZAR))

        self.l_sis_agua_falha_pressurizar_fitroB = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SIS_AGUA_FLH_PRESSURIZAR_FILTRO_B"], descricao="[SA]  Sistema Água Falha Pressurizar Filtro B")
        self.condicionadores.append(CondicionadorBase(self.l_sis_agua_falha_pressurizar_fitroB, CONDIC_NORMALIZAR))

        self.l_sis_agua_falha_pressostato_filtroB = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SIS_AGUA_FLH_PRESSOSTATO_FILTRO_B"], descricao="[SA]  Sistema Água Falha Pressostato Filtro B")
        self.condicionadores.append(CondicionadorBase(self.l_sis_agua_falha_pressostato_filtroB, CONDIC_NORMALIZAR))

        self.l_falha_52SA1 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DJ52SA1_SEM_FLH"], descricao="[SA]  Disjuntor 52SA1 Falha")
        self.condicionadores.append(CondicionadorBase(self.l_falha_52SA1, CONDIC_INDISPONIBILIZAR))

        self.l_72SA1_fechado = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DJ72SA1_FECHADO"], invertido=True, descricao="[SA]  Disjuntor 72SA1 Aberto")
        self.condicionadores.append(CondicionadorBase(self.l_72SA1_fechado, CONDIC_INDISPONIBILIZAR))

        self.l_djs24VCC_fechados = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DJS_24VCC_FECHADOS"], descricao="[SA]  Disjuntores 24Vcc Abertos")
        self.condicionadores.append(CondicionadorBase(self.l_djs24VCC_fechados, CONDIC_INDISPONIBILIZAR))

        self.l_djs125VCC_fechados = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DJS_125VCC_FECHADOS"], descricao="[SA]  Disjuntores 125Vcc Abertos")
        self.condicionadores.append(CondicionadorBase(self.l_djs125VCC_fechados, CONDIC_INDISPONIBILIZAR))

        self.l_cmd_24VCC_tensao = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["CMD_24VCC_COM_TENSAO"], descricao="[SA]  Comando 24Vcc Sem Tensão")
        self.condicionadores.append(CondicionadorBase(self.l_cmd_24VCC_tensao, CONDIC_INDISPONIBILIZAR))

        self.l_cmd_125VCC_tensao = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["CMD_125VCC_COM_TENSAO"], descricao="[SA]  Comando 125Vcc Sem Tensão")
        self.condicionadores.append(CondicionadorBase(self.l_cmd_125VCC_tensao, CONDIC_INDISPONIBILIZAR))

        self.l_alimentacao_125VCC_tensao = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["ALIM_125VCC_COM_TENSAO"], descricao="[SA]  Alimentação 125Vcc Sem Tensão")
        self.condicionadores.append(CondicionadorBase(self.l_alimentacao_125VCC_tensao, CONDIC_INDISPONIBILIZAR))

        self.l_falha_abertura_52SA1 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DJ52SA1_FLH_ABRIR"], descricao="[SA]  Disjuntor 52SA1 Falha Abertura")
        self.condicionadores.append(CondicionadorBase(self.l_falha_abertura_52SA1, CONDIC_INDISPONIBILIZAR))

        self.l_fechamento_52SA1 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DJ52SA1_FLH_FECHAR"], descricao="[SA]  Disjuntor 52SA1 Falha Fechamento")
        self.condicionadores.append(CondicionadorBase(self.l_fechamento_52SA1, CONDIC_INDISPONIBILIZAR))

        self.l_falha_abertura_52SA2 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DJ52SA2_FLH_ABRIR"], descricao="[SA]  Disjuntor 52SA2 Falha Abertura")
        self.condicionadores.append(CondicionadorBase(self.l_falha_abertura_52SA2, CONDIC_INDISPONIBILIZAR))

        self.l_falha_fechamento_52SA2 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DJ52SA2_FLH_FECHAR"], descricao="[SA]  Disjuntor 52SA2 Falha Fechamento")
        self.condicionadores.append(CondicionadorBase(self.l_falha_fechamento_52SA2, CONDIC_INDISPONIBILIZAR))

        self.l_falha_abertura_52SA3 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DJ52SA3_FLH_ABRIR"], descricao="[SA]  Disjuntor 52SA3 Falha Abertura")
        self.condicionadores.append(CondicionadorBase(self.l_falha_abertura_52SA3, CONDIC_INDISPONIBILIZAR))

        self.l_falha_fechamento_52SA3 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DJ52SA3_FLH_FECHAR"], descricao="[SA]  Disjuntor 52SA3 Falha Fechamento")
        self.condicionadores.append(CondicionadorBase(self.l_falha_fechamento_52SA3, CONDIC_INDISPONIBILIZAR))

        self.l_reti_fusivel_queimado = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["RETI_FUSIVEL_QUEIMADO"], descricao="[SA]  Retificador Fusível Queimado")
        self.condicionadores.append(CondicionadorBase(self.l_reti_fusivel_queimado, CONDIC_INDISPONIBILIZAR))

        self.l_reti_fuga_terra_pos = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["RETI_FUGA_TERRA_POSITIVO"], descricao="[SA]  Retificador Fuga Terra Positivo")
        self.condicionadores.append(CondicionadorBase(self.l_reti_fuga_terra_pos, CONDIC_INDISPONIBILIZAR))

        self.l_reti_fuga_terra_neg = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["RETI_FUGA_TERRA_NEGATIVO"], descricao="[SA]  Retificador Fuga Terra Negativo")
        self.condicionadores.append(CondicionadorBase(self.l_reti_fuga_terra_neg, CONDIC_INDISPONIBILIZAR))


        # LEITURA PERIÓDICA
        self.l_sis_agua_bomba_disp = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SIS_AGUA_BOMBA_DISPONIVEL"], invertido=True, descricao="[SA]  Sistem Água Bomba Disponível")

        self.l_falha_bomba_dren_1 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["BOMBA_DREN_1_FLH"], descricao="[SA]  Bomba Drenagem 1 Falha")
        self.l_falha_bomba_dren_2 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["BOMBA_DREN_2_FLH"], descricao="[SA]  Bomba Drenagem 2 Falha")
        self.l_falha_bomba_dren_3 = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["BOMBA_DREN_3_FLH"], descricao="[SA]  Bomba Drenagem 3 Falha")
        self.l_poco_dren_dicrepancia = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["POCO_DREN_DISCRE_BOIAS"], descricao="[SA]  Boias Poço Drenagem Discrepância")
        self.l_sis_agua_falha_ligar_bomba = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SIS_AGUA_FLH_LIGA_BOMBA"], descricao="[SA]  Sistema Água Falha Ligar Bomba")
        self.l_djs_barra_sel_remoto = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DJS_BARRA_SELETORA_REMOTO"], descricao="[SA]  Disjuntores Barra Seletora Modo Remoto")

        self.l_52SA1_sem_falha = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DJ52SA1_SEM_FLH"], invertido=True, descricao="[SA]  Disjuntor 52SA1 Sem Falha")
        self.l_52SA2_sem_falha = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DJ52SA2_SEM_FLH"], invertido=True, descricao="[SA]  Disjuntor 52SA2 Sem Falha")
        self.l_52SA3_sem_falha = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["DJ52SA3_SEM_FLH"], invertido=True, descricao="[SA]  Disjuntor 52SA3 Sem Falha")

        self.l_falha_parada_gmg = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["GMG_FLH_PARAR"], descricao="[SA]  Grupo Motor Gerador Falha Parada")
        self.l_falha_partida_gmg = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["GMG_FLH_PARTIR"], descricao="[SA]  Grupo Motor Gerador Falha Partida")
        self.l_gmg_manual = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["GMG_OPERACAO_MANUAL"], descricao="[SA]  Grupo Motor Gerador Modo Operação Manual")
        self.l_falha_bomba_filtragem = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["BOMBA_FILT_FLH"], descricao="[SA]  Bomba Filtragem Falha")
        self.l_nivel_alto_poco_dren = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["POCO_DREN_NV_ALTO"], descricao="[SA]  Poço Drenagem Nível Alto")
        self.l_falha_bomba_dren_uni = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["BOMBA_DREN_UNIDADES_FLH"], descricao="[SA]  Bomba Drenagem Unidades Falha")
        self.l_alarme_sis_incendio_atuado = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SIS_INCENDIO_ALM_ATUADO"], descricao="[SA]  Sistem Incêndio Alarme Atuado")
        self.l_alarme_sis_seguranca_atuado = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["SIS_SEGURANCA_ALM_ATUADO"], descricao="[SA]  Sistema Segurança Alarme Atuado")
        self.l_nivel_muito_alto_poco_dren = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["POCO_DREN_NV_MUITO_ALTO"], descricao="[SA]  Poço Drenagem Nível Muito Alto")
        self.l_falha_tubo_succao_bomba_recalque = LeituraModbusBit(self.clp["SA"], REG_CLP["SA"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"], descricao="[SA]  Bomba Recalque Falha Tubo Sucção")