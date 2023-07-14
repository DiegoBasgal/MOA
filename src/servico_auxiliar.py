__version__ = "0.2"
__authors__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação dos setores da Usina."

import logging
import traceback

import dicionarios.dict as dct

from condicionador import *
from funcoes.leitura import *
from dicionarios.const import *

from usina import Usina
from conector import ClientesUsina as cli
from funcoes.escrita import EscritaModBusBit as EMB

logger = logging.getLogger("__main__")

class ServicoAuxiliar(Usina):
    
    clp = cli.clp

    condicionadores: "list[CondicionadorBase]" = []
    condicionadores_essenciais: "list[CondicionadorBase]" = []
    
    def resetar_emergencia(cls) -> "bool":
        try:
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SA"]["RESET_FALHAS_BARRA_CA"], bit=0, valor=1)
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SA"]["RESET_FALHAS_SISTEMA_AGUA"], bit=1, valor=1)
            res = EMB.escrever_bit(cls.clp["SA"], REG_CLP["SA"]["REARME_BLOQUEIO_GERAL_E_FALHAS_SA"], bit=23, valor=1)
            return res

        except Exception:
            logger.exception(f"[SA] Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(f"[SA] Traceback: {traceback.format_exc()}")
            return False

    def verificar_condicionadores(cls) -> "list[CondicionadorBase]":
        if [condic.ativo for condic in cls.condicionadores_essenciais]:
            condics_ativos = [condic for condics in [cls.condicionadores_essenciais, cls.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            logger.warning("[SA] Foram detectados condicionadores ativos!")
            [logger.info(f"[SA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade]}\".") for condic in condics_ativos]
            logger.debug("")

            return condics_ativos
        else:
            return []

    def verificar_leituras(cls) -> "None":
        if cls.leitura_falha_bomba_drenagem_1.valor:
            logger.warning("[SA] Houve uma falha na bomba 1 do poço de drenagem. Favor verificar.")
        
        if cls.leitura_falha_bomba_drenagem_2.valor:
            logger.warning("[SA] Houve uma falha na bomba 2 do poço de drenagem. Favor verificar.")

        if cls.leitura_falha_bomba_drenagem_3.valor:
            logger.warning("[SA] Houve uma falha na bomba 3 do poço de drenagem. Favor verificar.")

        if cls.leitura_falha_ligar_bomba_sis_agua.valor:
            logger.warning("[SA] Houve uma falha ao ligar a bomba do sistema de água. Favor verificar.")

        if cls.leitura_djs_barra_seletora_remoto.valor:
            logger.warning("[SA] Os disjuntores da barra seletora saíram do modo remoto. Favor verificar.")

        if not cls.leitura_bomba_sis_agua_disp.valor:
            logger.warning("[SA] Foi identificado que a bomba do sistema de água está indisponível. Favor verificar.")

        if cls.leitura_discrepancia_boia_poco_drenagem.valor:
            logger.warning("[SA] Foram identificados sinais inconsistentes nas boias do poço de drenagem. Favor verificar.")

        if cls.leitura_falha_partir_gmg.valor and not dct.voip["GMG_FALHA_PARTIR"][0]:
            logger.warning("[SA] Houve uma falha ao partir o Gerador Diesel. Favor verificar.")
            dct.voip["GMG_FALHA_PARTIR"][0] = True
        elif not cls.leitura_falha_partir_gmg.valor and dct.voip["GMG_FALHA_PARTIR"][0]:
            dct.voip["GMG_FALHA_PARTIR"][0] = False

        if cls.leitura_falha_parar_gmg.valor and not dct.voip["GMG_FALHA_PARAR"][0]:
            logger.warning("[SA] Houve uma falha ao parar o Gerador Diesel. Favor verificar.")
            dct.voip["GMG_FALHA_PARAR"][0] = True
        elif not cls.leitura_falha_parar_gmg.valor and dct.voip["GMG_FALHA_PARAR"][0]:
            dct.voip["GMG_FALHA_PARAR"][0] = False

        if cls.leitura_operacao_manual_gmg.valor and not dct.voip["GMG_OPERACAO_MANUAL"][0]:
            logger.warning("[SA] O Gerador Diesel saiu do modo remoto. Favor verificar.")
            dct.voip["GMG_OPERACAO_MANUAL"][0] = True
        elif not cls.leitura_operacao_manual_gmg.valor and dct.voip["GMG_OPERACAO_MANUAL"][0]:
            dct.voip["GMG_OPERACAO_MANUAL"][0] = False

        if not cls.leitura_sem_falha_52sa1.valor and not dct.voip["52SA1_SEM_FALHA"][0]:
            logger.warning("[SA] Houve uma falha com o disjuntor 52SA1 do transformador do SA. Favor verificar.")
            dct.voip["52SA1_SEM_FALHA"][0] = True
        elif cls.leitura_sem_falha_52sa1.valor and dct.voip["52SA1_SEM_FALHA"][0]:
            dct.voip["52SA1_SEM_FALHA"][0] = False

        if not cls.leitura_sem_falha_52sa2.valor and not dct.voip["52SA2_SEM_FALHA"][0]:
            logger.warning("[SA] Houve uma falha com o disjuntor 52SA2 do Gerador Diesel. Favor verificar.")
            dct.voip["52SA2_SEM_FALHA"][0] = True
        elif cls.leitura_sem_falha_52sa2.valor and dct.voip["52SA2_SEM_FALHA"][0]:
            dct.voip["52SA2_SEM_FALHA"][0] = False

        if not cls.leitura_sem_falha_52sa3.valor and not dct.voip["52SA3_SEM_FALHA"][0]:
            logger.warning("[SA] Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciais. Favor verificar.")
            dct.voip["52SA3_SEM_FALHA"][0] = True
        elif cls.leitura_sem_falha_52sa3.valor and dct.voip["52SA3_SEM_FALHA"][0]:
            dct.voip["52SA3_SEM_FALHA"][0] = False

        if cls.leitura_falha_bomba_filtragem.valor and not dct.voip["FILTRAGEM_BOMBA_FALHA"][0]:
            logger.warning("[SA] Houve uma falha na bomba de filtragem. Favor verificar.")
            dct.voip["FILTRAGEM_BOMBA_FALHA"][0] = True
        elif not cls.leitura_falha_bomba_filtragem.valor and dct.voip["FILTRAGEM_BOMBA_FALHA"][0]:
            dct.voip["FILTRAGEM_BOMBA_FALHA"][0] = False

        if cls.leitura_nivel_alto_poco_drenagem.valor and not dct.voip["POCO_DRENAGEM_NIVEL_ALTO"][0]:
            logger.warning("[SA] Nível do poço de drenagem alto. Favor verificar.")
            dct.voip["POCO_DRENAGEM_NIVEL_ALTO"][0] = True
        elif not cls.leitura_nivel_alto_poco_drenagem.valor and dct.voip["POCO_DRENAGEM_NIVEL_ALTO"][0]:
            dct.voip["POCO_DRENAGEM_NIVEL_ALTO"][0] = False

        if cls.leitura_falha_bomba_drenagem_uni.valor and not dct.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0]:
            logger.warning("[SA] Houve uma falha na bomba de drenagem. Favor verificar.")
            dct.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0] = True
        elif not cls.leitura_falha_bomba_drenagem_uni.valor and dct.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0]:
            dct.voip["DRENAGEM_UNIDADES_BOMBA_FALHA"][0] = False

        if cls.leitura_nivel_muito_alto_poco_drenagem.valor and not dct.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0]:
            logger.warning("[SA] Nível do poço de drenagem está muito alto. Favor verificar.")
            dct.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0] = True
        elif not cls.leitura_nivel_muito_alto_poco_drenagem.valor and dct.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0]:
            dct.voip["POCO_DRENAGEM_NIVEL_MUITO_ALTO"][0] = False

        if cls.leitura_alarme_sistema_incendio_atuado.valor and not dct.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0]:
            logger.warning("[SA] O alarme do sistema de incêndio foi acionado. Favor verificar.")
            dct.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0] = True
        elif not cls.leitura_alarme_sistema_incendio_atuado.valor and dct.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0]:
            dct.voip["SISTEMA_INCENDIO_ALARME_ATUADO"][0] = False

        if cls.leitura_alarme_sistema_seguraca_atuado.valor and not dct.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0]:
            logger.warning("[SA] O alarme do sistem de seguraça foi acionado. Favor verificar.")
            dct.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0] = True
        elif not cls.leitura_alarme_sistema_seguraca_atuado.valor and dct.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0]:
            dct.voip["SISTEMA_SEGURANCA_ALARME_ATUADO"][0] = False
            
        if cls.leitura_falha_tubo_succao_bomba_recalque.valor and not dct.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0]:
            logger.warning("[SA] Houve uma falha na sucção da bomba de recalque. Favor verificar.")
            dct.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0] = True
        elif not cls.leitura_falha_tubo_succao_bomba_recalque.valor and dct.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0]:
            dct.voip["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"][0] = False

    def carregar_leituras(cls) -> "None":
        # CONDICIONADORES ESSENCIAIS
        # Normalizar
        cls.leitura_sem_emergencia_sa = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SEM_EMERGENCIA"], bit=13, invertido=True, descricao="[SA] Emergência")
        cls.condicionadores_essenciais.append(CondicionadorBase(cls.leitura_sem_emergencia_sa, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Normalizar
        cls.leitura_retificador_subtensao = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["RETIFICADOR_SUBTENSAO"], bit=31, descricao="[SA] Retificador Subtensão")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_retificador_subtensao, CONDIC_NORMALIZAR))

        cls.leitura_retificador_sobretensao = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["RETIFICADOR_SOBRETENSAO"], bit=30, descricao="[SA] Retificador Sobretensão")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_retificador_sobretensao, CONDIC_NORMALIZAR))

        cls.leitura_retificador_sobrecorrente_saida = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["RETIFICADOR_SOBRECORRENTE_SAIDA"], bit=0, descricao="[SA] Retificador Sobrecorrente Saída")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_retificador_sobrecorrente_saida, CONDIC_NORMALIZAR))

        cls.leitura_retificador_sobrecorrente_baterias = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["RETIFICADOR_SOBRECORRENTE_BATERIAS"], bit=1, descricao="[SA] Retificador Sobrecorrente Baterias")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_retificador_sobrecorrente_baterias, CONDIC_NORMALIZAR))

        cls.leitura_falha_sistema_agua_pressurizar_fa = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_A"], bit=3, descricao="[SA] Sistema Água Falha Pressurizar Filtro A")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_falha_sistema_agua_pressurizar_fa, CONDIC_NORMALIZAR))

        cls.leitura_falha_sistema_agua_pressostato_fa = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_A"], bit=4, descricao="[SA] Sistema Água Falha Pressostato Filtro A")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_falha_sistema_agua_pressostato_fa, CONDIC_NORMALIZAR))

        cls.leitura_falha_sistema_agua_pressurizar_fb = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_B"], bit=5, descricao="[SA] Sistema Água Falha Pressurizar Filtro B")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_falha_sistema_agua_pressurizar_fb, CONDIC_NORMALIZAR))

        cls.leitura_falha_sistema_agua_pressostato_fb = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_B"], bit=6, descricao="[SA] Sistema Água Falha Pressostato Filtro B")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_falha_sistema_agua_pressostato_fb, CONDIC_NORMALIZAR))

        # Indisponibilizar
        cls.leitura_52sa1_sem_falha = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["52SA1_SEM_FALHA"], bit=31, invertido=True, descricao="[SA] Disjuntor 52SA1 Sem Falha")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_52sa1_sem_falha, CONDIC_INDISPONIBILIZAR))

        cls.leitura_sa_72sa1_fechado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SA_72SA1_FECHADO"], bit=10, invertido=True, descricao="[SA] Disjuntor 72SA1 Fechado")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_sa_72sa1_fechado, CONDIC_INDISPONIBILIZAR))

        cls.leitura_disj_24vcc_fechados = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DISJUNTORES_24VCC_FECHADOS"], bit=12, invertido=True, descricao="[SA] Disjuntores 24Vcc Fechados")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_disj_24vcc_fechados, CONDIC_INDISPONIBILIZAR))

        cls.leitura_disj_125vcc_fechados = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DISJUNTORES_125VCC_FECHADOS"], bit=11, invertido=True, descricao="[SA] Disjuntores 125Vcc Fechados")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_disj_125vcc_fechados, CONDIC_INDISPONIBILIZAR))
        
        cls.leitura_comando_24vcc_com_tensao = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["COM_TENSAO_COMANDO_24VCC"], bit=15, invertido=True, descricao="[SA] Comando 24Vcc Com Tensão")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_comando_24vcc_com_tensao, CONDIC_INDISPONIBILIZAR))
        
        cls.leitura_comando_125vcc_com_tensao = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["COM_TENSAO_COMANDO_125VCC"], bit=14, invertido=True, descricao="[SA] Comando 125Vcc Com Tensão")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_comando_125vcc_com_tensao, CONDIC_INDISPONIBILIZAR))
        
        cls.leitura_alimentacao_125vcc_com_tensao = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["COM_TENSAO_ALIMENTACAO_125VCC"], bit=13, invertido=True, descricao="[SA] Alimentação 125Vcc Com Tensão")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_alimentacao_125vcc_com_tensao, CONDIC_INDISPONIBILIZAR))

        cls.leitura_falha_abrir_52sa1 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["FALHA_ABRIR_52SA1"], bit=0, descricao="[SA] Disjuntor 52SA1 Falha Abertura")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_falha_abrir_52sa1, CONDIC_INDISPONIBILIZAR))

        cls.leitura_falha_fechar_52sa1 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["FALHA_FECHAR_52SA1"], bit=1, descricao="[SA] Disjuntor 52SA1 Falha Fechamento")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_falha_fechar_52sa1, CONDIC_INDISPONIBILIZAR))

        cls.leitura_falha_abrir_52sa2 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["FALHA_ABRIR_52SA2"], bit=3, descricao="[SA] Disjuntor 52SA2 Falha Abertura")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_falha_abrir_52sa2, CONDIC_INDISPONIBILIZAR))

        cls.leitura_falha_fechar_52sa2 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["FALHA_FECHAR_52SA2"], bit=4, descricao="[SA] Disjuntor 52SA2 Falha Fechamento")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_falha_fechar_52sa2, CONDIC_INDISPONIBILIZAR))

        cls.leitura_falha_abrir_52sa3 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["FALHA_ABRIR_52SA3"], bit=5, descricao="[SA] Disjuntor 52SA3 Falha Abertura")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_falha_abrir_52sa3, CONDIC_INDISPONIBILIZAR))

        cls.leitura_falha_fechar_52sa3 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["FALHA_FECHAR_52SA3"], bit=6, descricao="[SA] Disjuntor 52SA3 Falha Fechamento")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_falha_fechar_52sa3, CONDIC_INDISPONIBILIZAR))

        cls.leitura_fusivel_queimado_retificador = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["RETIFICADOR_FUSIVEL_QUEIMADO"], bit=2, descricao="[SA] Retificador Fusível Queimado")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_fusivel_queimado_retificador, CONDIC_INDISPONIBILIZAR))

        cls.leitura_fuga_terra_positivo_retificador = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["RETIFICADOR_FUGA_TERRA_POSITIVO"], bit=5, descricao="[SA] Retificador Fuga Terra Positivo")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_fuga_terra_positivo_retificador, CONDIC_INDISPONIBILIZAR))

        cls.leitura_fuga_terra_negativo_retificador = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["RETIFICADOR_FUGA_TERRA_NEGATIVO"], bit=6, descricao="[SA] Retificador Fuga Terra Negativo")
        cls.condicionadores.append(CondicionadorBase(cls.leitura_fuga_terra_negativo_retificador, CONDIC_INDISPONIBILIZAR))

        # LEITURA PERIODICA
        cls.leitura_bomba_sis_agua_disp = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SISTEMA_AGUA_BOMBA_DISPONIVEL"], bit=0, invertido=True, descricao="[SA] Sistem Água Bomba Disponível")

        cls.leitura_falha_bomba_drenagem_1 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DRENAGEM_BOMBA_1_FALHA"], bit=0, descricao="[SA] Bomba Drenagem 1 Falha")
        cls.leitura_falha_bomba_drenagem_2 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DRENAGEM_BOMBA_2_FALHA"], bit=2, descricao="[SA] Bomba Drenagem 2 Falha")
        cls.leitura_falha_bomba_drenagem_3 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DRENAGEM_BOMBA_3_FALHA"], bit=4, descricao="[SA] Bomba Drenagem 3 Falha")
        cls.leitura_falha_ligar_bomba_sis_agua = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SISTEMA_AGUA_FALHA_LIGA_BOMBA"], bit=1, descricao="[SA] Sistema Água Falha Ligar Bomba")
        cls.leitura_djs_barra_seletora_remoto = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DISJUNTORES_BARRA_SELETORA_REMOTO"], bit=9, descricao="[SA] Disjuntores Barra Seletora Modo Remoto")
        cls.leitura_discrepancia_boia_poco_drenagem = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DRENAGEM_DISCREPANCIA_BOIAS_POCO"], bit=9, descricao="[SA] Boias Poço Drenagem Discrepância")

        cls.leitura_sem_falha_52sa1 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["52SA1_SEM_FALHA"], bit=31, invertido=True, descricao="[SA] Disjuntor 52SA1 Sem Falha")
        cls.leitura_sem_falha_52sa2 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["52SA2_SEM_FALHA"], bit=1, invertido=True, descricao="[SA] Disjuntor 52SA2 Sem Falha")
        cls.leitura_sem_falha_52sa3 = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["52SA3_SEM_FALHA"], bit=3, invertido=True, descricao="[SA] Disjuntor 52SA3 Sem Falha")

        cls.leitura_falha_parar_gmg = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["GMG_FALHA_PARAR"], bit=7, descricao="[SA] Grupo Motor Gerador Falha Parada")
        cls.leitura_falha_partir_gmg = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["GMG_FALHA_PARTIR"], bit=6, descricao="[SA] Grupo Motor Gerador Falha Partida")
        cls.leitura_operacao_manual_gmg = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["GMG_OPERACAO_MANUAL"], bit=10, descricao="[SA] Grupo Motor Gerador Modo Operação Manual")
        cls.leitura_falha_bomba_filtragem = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["FILTRAGEM_BOMBA_FALHA"], bit=6, descricao="[SA] Bomba Filtragem Falha")
        cls.leitura_nivel_alto_poco_drenagem = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["POCO_DRENAGEM_NIVEL_ALTO"], bit=26, descricao="[SA] Poço Drenagem Nível Alto")
        cls.leitura_falha_bomba_drenagem_uni = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["DRENAGEM_UNIDADES_BOMBA_FALHA"], bit=12, descricao="[SA] Bomba Drenagem Unidades Falha")
        cls.leitura_alarme_sistema_incendio_atuado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SISTEMA_INCENDIO_ALARME_ATUADO"], bit=6, descricao="[SA] Sistem Incêndio Alarme Atuado")
        cls.leitura_alarme_sistema_seguraca_atuado = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["SISTEMA_SEGURANCA_ALARME_ATUADO"], bit=7, descricao="[SA] Sistema Segurança Alarme Atuado")
        cls.leitura_nivel_muito_alto_poco_drenagem = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["POCO_DRENAGEM_NIVEL_MUITO_ALTO"], bit=25, descricao="[SA] Poço Drenagem Nível Muito Alto")
        cls.leitura_falha_tubo_succao_bomba_recalque = LeituraModbusBit(cls.clp["SA"], REG_CLP["SA"]["BOMBA_RECALQUE_TUBO_SUCCAO_FALHA"], bit=14, descricao="[SA] Bomba Recalque Falha Tubo Sucção")