__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação do Serviço Auxiliar."

import pytz
import logging
import traceback

import src.dicionarios.dict as d
import src.funcoes.leitura as lei
import src.funcoes.escrita as esc
import src.conectores.servidores as srv
import src.conectores.banco_dados as bd
import src.funcoes.condicionadores as c

from time import sleep
from datetime import datetime

from src.dicionarios.const import *
from src.dicionarios.reg_elipse import *


logger = logging.getLogger("logger")


class ServicoAuxiliar:
    def __init__(self, serv: "srv.Servidores"=None, bd: "bd.BancoDados"=None) -> None:

        # ATRIBUIÇÃO DE VARIÁVEIS

        self.bd = bd
        self.clp = serv.clp

        self.condicionadores: "list[c.CondicionadorBase]" = []
        self.condicionadores_essenciais: "list[c.CondicionadorBase]" = []
        self.condicionadores_ativos: "list[c.CondicionadorBase]" = []


    def resetar_emergencia(self) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = esc.EscritaModBusBit.escrever_bit(self.clp["SA"], REG_CLP["SA_SE"]["COMANDO_RESET_FALHAS_BARRA_SERVICOS_AUXILIARES"], valor=1)
            res = esc.EscritaModBusBit.escrever_bit(self.clp["SA"], REG_CLP["SA_SE"]["COMANDO_RESET_FALHAS_SISTEMA_AGUA"], valor=1)
            return res

        except Exception:
            logger.exception(f"[SA]  Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(f"[SA]  Traceback: {traceback.format_exc()}")
            return False


    def verificar_condicionadores(self) -> "list[c.CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

        autor = 0

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if self.condicionadores_ativos == []:
                logger.debug(f"[SA]  Foram detectados Condicionadores ativos no Serviço Auxiliar!")
            else:
                logger.debug(f"[SA]  Ainda há Condicionadores ativos no Serviço Auxiliar!")

            for condic in condics_ativos:
                if condic.teste:
                    logger.debug(f"[SA]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\", Obs.: \"TESTE\"")
                    continue

                elif condic in self.condicionadores_ativos:
                    logger.debug(f"[SA]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue

                else:
                    logger.warning(f"[SA]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    self.bd.update_alarmes([
                        datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor == 0 else ""
                    ])
                    sleep(1)
                    autor += 1

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

        if self.l_falha_partida_gmg.valor and not d.voip["GMG_FALHA_PARTIR"][0]:
            logger.warning("[SA]  Houve uma falha ao partir o Gerador Diesel. Favor verificar.")
            d.voip["GMG_FALHA_PARTIR"][0] = True
        elif not self.l_falha_partida_gmg.valor and d.voip["GMG_FALHA_PARTIR"][0]:
            d.voip["GMG_FALHA_PARTIR"][0] = False

        if self.l_falha_parada_gmg.valor and not d.voip["GMG_FALHA_PARAR"][0]:
            logger.warning("[SA]  Houve uma falha ao parar o Gerador Diesel. Favor verificar.")
            d.voip["GMG_FALHA_PARAR"][0] = True
        elif not self.l_falha_parada_gmg.valor and d.voip["GMG_FALHA_PARAR"][0]:
            d.voip["GMG_FALHA_PARAR"][0] = False

        if self.l_gmg_manual.valor and not d.voip["GMG_OPERACAO_MANUAL"][0]:
            logger.warning("[SA]  O Gerador Diesel saiu do modo remoto. Favor verificar.")
            d.voip["GMG_OPERACAO_MANUAL"][0] = True
        elif not self.l_gmg_manual.valor and d.voip["GMG_OPERACAO_MANUAL"][0]:
            d.voip["GMG_OPERACAO_MANUAL"][0] = False

        if not self.l_52SA1_sem_falha.valor and not d.voip["52SA1_SEM_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha com o disjuntor 52SA1 do transformador do SA. Favor verificar.")
            d.voip["52SA1_SEM_FALHA"][0] = True
        elif self.l_52SA1_sem_falha.valor and d.voip["52SA1_SEM_FALHA"][0]:
            d.voip["52SA1_SEM_FALHA"][0] = False

        if not self.l_52SA2_sem_falha.valor and not d.voip["52SA2_SEM_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha com o disjuntor 52SA2 do Gerador Diesel. Favor verificar.")
            d.voip["52SA2_SEM_FALHA"][0] = True
        elif self.l_52SA2_sem_falha.valor and d.voip["52SA2_SEM_FALHA"][0]:
            d.voip["52SA2_SEM_FALHA"][0] = False

        if not self.l_52SA3_sem_falha.valor and not d.voip["52SA3_SEM_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciais. Favor verificar.")
            d.voip["52SA3_SEM_FALHA"][0] = True
        elif self.l_52SA3_sem_falha.valor and d.voip["52SA3_SEM_FALHA"][0]:
            d.voip["52SA3_SEM_FALHA"][0] = False

        if self.l_falha_bomba_filtragem.valor and not d.voip["FILTRAGEM_BOMBA_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha na bomba de filtragem. Favor verificar.")
            d.voip["FILTRAGEM_BOMBA_FALHA"][0] = True
        elif not self.l_falha_bomba_filtragem.valor and d.voip["FILTRAGEM_BOMBA_FALHA"][0]:
            d.voip["FILTRAGEM_BOMBA_FALHA"][0] = False

        if self.l_nivel_alto_poco_dren.valor and not d.voip["POCO_DRENAGEM_NIVEL_ALTO"][0]:
            logger.warning("[SA]  Nível do poço de drenagem alto. Favor verificar.")
            d.voip["POCO_DRENAGEM_NIVEL_ALTO"][0] = True
        elif not self.l_nivel_alto_poco_dren.valor and d.voip["POCO_DRENAGEM_NIVEL_ALTO"][0]:
            d.voip["POCO_DRENAGEM_NIVEL_ALTO"][0] = False

        if self.l_falha_bomba_dren_uni.valor and not d.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha na bomba de drenagem. Favor verificar.")
            d.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0] = True
        elif not self.l_falha_bomba_dren_uni.valor and d.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0]:
            d.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0] = False

        if self.l_nivel_muito_alto_poco_dren.valor and not d.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0]:
            logger.warning("[SA]  Nível do poço de drenagem está muito alto. Favor verificar.")
            d.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0] = True
        elif not self.l_nivel_muito_alto_poco_dren.valor and d.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0]:
            d.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0] = False

        if self.l_alarme_sis_incendio_atuado.valor and not d.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0]:
            logger.warning("[SA]  O alarme do sistema de incêndio foi acionado. Favor verificar.")
            d.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0] = True
        elif not self.l_alarme_sis_incendio_atuado.valor and d.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0]:
            d.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0] = False

        if self.l_alarme_sis_seguranca_atuado.valor and not d.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0]:
            logger.warning("[SA]  O alarme do sistem de seguraça foi acionado. Favor verificar.")
            d.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0] = True
        elif not self.l_alarme_sis_seguranca_atuado.valor and d.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0]:
            d.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0] = False


    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """

        # CONDICIONADORES ESSENCIAIS
        self.l_bloq_geral = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["BLOQUEIO_86T"], descricao="[SA]  Bloqueio Geral Acionado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_bloq_geral, CONDIC_NORMALIZAR))


        # CONDICIONADORES
        self.l_sis_agua_falha_pressurizar_filtroA = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["SISTEMA_AGUA_FALHA_PRESSURIZAR_SAIDA_FILTRO_A"], descricao="[SA]  Sistema Água Falha Pressurizar Filtro A")
        self.condicionadores.append(c.CondicionadorBase(self.l_sis_agua_falha_pressurizar_filtroA, CONDIC_NORMALIZAR))

        self.l_sis_agua_falha_pressostato_filtroA = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_A"], descricao="[SA]  Sistema Água Falha Pressostato Filtro A")
        self.condicionadores.append(c.CondicionadorBase(self.l_sis_agua_falha_pressostato_filtroA, CONDIC_NORMALIZAR))

        self.l_sis_agua_falha_pressurizar_fitroB = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["SISTEMA_AGUA_FALHA_PRESSURIZAR_SAIDA_FILTRO_B"], descricao="[SA]  Sistema Água Falha Pressurizar Filtro B")
        self.condicionadores.append(c.CondicionadorBase(self.l_sis_agua_falha_pressurizar_fitroB, CONDIC_NORMALIZAR))

        self.l_sis_agua_falha_pressostato_filtroB = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_B"], descricao="[SA]  Sistema Água Falha Pressostato Filtro B")
        self.condicionadores.append(c.CondicionadorBase(self.l_sis_agua_falha_pressostato_filtroB, CONDIC_NORMALIZAR))

        self.l_72SA1_fechado = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DISJUNTOR_GERAL_CORRENTE_CONTINUA_125VCC_72SA1_FECHADO"], descricao="[SA]  Disjuntor 72SA1 Aberto")
        self.condicionadores.append(c.CondicionadorBase(self.l_72SA1_fechado, CONDIC_INDISPONIBILIZAR))

        self.l_falha_abertura_52SA1 = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DISJUNTOR_SERVICOS_AUXILIARES_52SA1_FALHA_ABERTURA"], descricao="[SA]  Disjuntor 52SA1 Falha Abertura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_abertura_52SA1, CONDIC_INDISPONIBILIZAR))

        self.l_fechamento_52SA1 = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DISJUNTOR_SERVICOS_AUXILIARES_52SA1_FALHA_FECHAMENTO"], descricao="[SA]  Disjuntor 52SA1 Falha Fechamento")
        self.condicionadores.append(c.CondicionadorBase(self.l_fechamento_52SA1, CONDIC_INDISPONIBILIZAR))

        self.l_falha_abertura_52SA2 = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DISJUNTOR_GERADOR_DIESEL_52SA2_FALHA_ABERTURA"], descricao="[SA]  Disjuntor 52SA2 Falha Abertura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_abertura_52SA2, CONDIC_INDISPONIBILIZAR))

        self.l_falha_fechamento_52SA2 = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DISJUNTOR_GERADOR_DIESEL_52SA2_FALHA_FECHAMENTO"], descricao="[SA]  Disjuntor 52SA2 Falha Fechamento")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_fechamento_52SA2, CONDIC_INDISPONIBILIZAR))

        self.l_falha_abertura_52SA3 = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DISJUNTOR_INTERLIGACAO_BARRAS_52SA3_FALHA_ABERTURA"], descricao="[SA]  Disjuntor 52SA3 Falha Abertura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_abertura_52SA3, CONDIC_INDISPONIBILIZAR))

        self.l_falha_fechamento_52SA3 = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DISJUNTOR_INTERLIGACAO_BARRAS_52SA3_FALHA_FECHAMENTO"], descricao="[SA]  Disjuntor 52SA3 Falha Fechamento")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_fechamento_52SA3, CONDIC_INDISPONIBILIZAR))


        self.l_reti_subtensao = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["RETIFICADOR_SUBTENSAO_CC"], invertido=True, descricao="[SA]  Retificador Subtensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_reti_subtensao, CONDIC_NORMALIZAR))

        self.l_reti_sobretensao = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["RETIFICADOR_SOBRETENSAO_CC"], invertido=True, descricao="[SA]  Retificador Sobretensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_reti_sobretensao, CONDIC_NORMALIZAR))

        self.l_reti_fusivel_queimado = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["RETIFICADOR_FUSIVEL_QUEIMADO"], invertido=True, descricao="[SA]  Retificador Fusível Queimado")
        self.condicionadores.append(c.CondicionadorBase(self.l_reti_fusivel_queimado, CONDIC_INDISPONIBILIZAR))

        self.l_reti_fuga_terra_pos = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["RETIFICADOR_FUGA_TERRA_POSITIVO"], invertido=True, descricao="[SA]  Retificador Fuga Terra Positivo")
        self.condicionadores.append(c.CondicionadorBase(self.l_reti_fuga_terra_pos, CONDIC_INDISPONIBILIZAR))

        self.l_reti_fuga_terra_neg = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["RETIFICADOR_FUGA_TERRA_NEGATIVO"], invertido=True, descricao="[SA]  Retificador Fuga Terra Negativo")
        self.condicionadores.append(c.CondicionadorBase(self.l_reti_fuga_terra_neg, CONDIC_INDISPONIBILIZAR))

        self.l_reti_sobrecorrente_saida = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["RETIFICADOR_SOBRECORRENTE_SAIDA"], invertido=True, descricao="[SA]  Retificador Sobrecorrente Saída")
        self.condicionadores.append(c.CondicionadorBase(self.l_reti_sobrecorrente_saida, CONDIC_NORMALIZAR))

        self.l__reti_sobrecorrente_baterias = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["RETIFICADOR_SOBRECORRENTE_BATERIAS"], invertido=True, descricao="[SA]  Retificador Sobrecorrente Baterias")
        self.condicionadores.append(c.CondicionadorBase(self.l__reti_sobrecorrente_baterias, CONDIC_NORMALIZAR))

        self.l_falha_52SA1 = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DISJUNTOR_52SA1_TRANSFORMADOR_SERVICOS_AUXILIARES_FALHA"], invertido=True, descricao="[SA]  Disjuntor 52SA1 Falha")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_52SA1, CONDIC_INDISPONIBILIZAR))

        self.l_djs24VCC_fechados = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DISJUNTORES_CORRENTE_CONTINUA_24VCC_ABERTOS"], invertido=True, descricao="[SA]  Disjuntores 24Vcc Abertos")
        self.condicionadores.append(c.CondicionadorBase(self.l_djs24VCC_fechados, CONDIC_INDISPONIBILIZAR))

        self.l_djs125VCC_fechados = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DISJUNTORES_CORRENTE_CONTINUA_125VCC_ABERTOS"], invertido=True, descricao="[SA]  Disjuntores 125Vcc Abertos")
        self.condicionadores.append(c.CondicionadorBase(self.l_djs125VCC_fechados, CONDIC_INDISPONIBILIZAR))

        self.l_cmd_24VCC_tensao = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["SUBTENSAO_COMANDO_SERVICOS_AUXILIARES_24VCC"], invertido=True, descricao="[SA]  Comando 24Vcc Sem Tensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_cmd_24VCC_tensao, CONDIC_INDISPONIBILIZAR))

        self.l_cmd_125VCC_tensao = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["SUBTENSAO_COMANDO_SERVICOS_AUXILIARES_125VCC"], invertido=True, descricao="[SA]  Comando 125Vcc Sem Tensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_cmd_125VCC_tensao, CONDIC_INDISPONIBILIZAR))

        self.l_alimentacao_125VCC_tensao = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["SUBTENSAO_ALIMENTACAO_SERVICOS_AUXILIARES_125VCC"], invertido=True, descricao="[SA]  Alimentação 125Vcc Sem Tensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_alimentacao_125VCC_tensao, CONDIC_INDISPONIBILIZAR))


        # LEITURA PERIÓDICA
        self.l_sis_agua_bomba_disp = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["SISTEMA_AGUA_BOMBA_DISPONIVEL"], descricao="[SA]  Sistem Água Bomba Disponível")
        self.l_falha_bomba_dren_1 = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DRENAGEM_BOMBA_1_FALHA"], descricao="[SA]  Bomba Drenagem 1 Falha")
        self.l_falha_bomba_dren_2 = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DRENAGEM_BOMBA_2_FALHA"], descricao="[SA]  Bomba Drenagem 2 Falha")
        self.l_falha_bomba_dren_3 = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DRENAGEM_BOMBA_3_FALHA"], descricao="[SA]  Bomba Drenagem 3 Falha")
        self.l_poco_dren_dicrepancia = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DRENAGEM_DISCREPANCIA_SINAIS_NIVEL"], descricao="[SA]  Boias Poço Drenagem Discrepância")
        self.l_sis_agua_falha_ligar_bomba = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["SISTEMA_AGUA_FALHA_LIGAR_BOMBA"], descricao="[SA]  Sistema Água Falha Ligar Bomba")
        self.l_djs_barra_sel_remoto = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["SELETORA_DISJUNTORES_BARRA_SERVICOS_AUXILIARES_EM_REMOTO"], descricao="[SA]  Disjuntores Barra Seletora Modo Remoto")

        self.l_52SA1_sem_falha = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DISJUNTOR_52SA1_TRANSFORMADOR_SERVICOS_AUXILIARES_FALHA"], invertido=True, descricao="[SA]  Disjuntor 52SA1 Sem Falha")
        self.l_52SA2_sem_falha = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DISJUNTOR_52SA2_GERADOR_DIESEL_DE_EMERGENCIA_FALHA"], invertido=True, descricao="[SA]  Disjuntor 52SA2 Sem Falha")
        self.l_52SA3_sem_falha = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DISJUNTOR_52SA3_INTERLIGACAO_BARRAS_FALHA"], invertido=True, descricao="[SA]  Disjuntor 52SA3 Sem Falha")

        self.l_falha_parada_gmg = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["GERADOR_DIESEL_DE_EMERGENCIA_FALHA_PARADA"], descricao="[SA]  Grupo Motor Gerador Falha Parada")
        self.l_falha_partida_gmg = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["GERADOR_DIESEL_DE_EMERGENCIA_FALHA_PARTIDA"], descricao="[SA]  Grupo Motor Gerador Falha Partida")
        self.l_gmg_manual = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["GERADOR_DIESEL_DE_EMERGENCIA_OPERACAO_REMOTA_MANUAL"], descricao="[SA]  Grupo Motor Gerador Modo Operação Manual")
        self.l_falha_bomba_filtragem = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DRENAGEM_BOMBA_1_FALHA"], descricao="[SA]  Bomba Filtragem Falha")
        self.l_nivel_alto_poco_dren = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DRENAGEM_NIVEL_ALTO"], descricao="[SA]  Poço Drenagem Nível Alto")
        self.l_falha_bomba_dren_uni = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["BOMBA_ESGOTAMENTO_UNIDADES_FALHA"], descricao="[SA]  Bomba Drenagem Unidades Falha")
        self.l_alarme_sis_incendio_atuado = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["SINAL_DO_SISTEMA_DE_INCENDIO"], descricao="[SA]  Sistem Incêndio Alarme Atuado")
        self.l_alarme_sis_seguranca_atuado = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["SINAL_DO_SISTEMA_DE_SEGURANCA"], descricao="[SA]  Sistema Segurança Alarme Atuado")
        self.l_nivel_muito_alto_poco_dren = lei.LeituraModbusBit(self.clp["SA"], REG_CLP["SA_SE"]["DRENAGEM_NIVEL_MUITO_ALTO"], descricao="[SA]  Poço Drenagem Nível Muito Alto")