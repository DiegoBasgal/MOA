__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação do Serviço Auxiliar."

import pytz
import logging
import traceback
import threading

import src.dicionarios.dict as d
import src.funcoes.leitura as lei
import src.funcoes.escrita as esc
import src.conectores.banco_dados as bd
import src.funcoes.condicionadores as c
import src.conectores.servidores as serv

from time import sleep, time
from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class ServicoAuxiliar:

    # ATRIBUIÇÃO DE VARIÁVEIS

    clp = serv.Servidores.clp
    bd: "bd.BancoDados" = None

    status_dj_tsa = lei.LeituraModbusBit(
        clp["SA"],
        REG_SASE["SA"]["SA_ED_PSA_DIJS_TSA_FECHADO"],
        descricao="[USN] Status Disjuntor SA"
    )

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []


    @classmethod
    def resetar_emergencia(cls) -> "None":
        try:
            logger.info(f"[SA]  Enviando comando:                   \"RESET EMERGÊNCIA\"")
            esc.EscritaModBusBit.escrever_bit(cls.clp["SA"], REG_SASE["SA"]["SA_CD_REARME_FALHAS"], valor=1)

        except Exception:
            logger.error(f"[SA]  Houve um erro ao realizar o Reset Geral.")
            logger.debug(traceback.format_exc())


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
                logger.warning(f"[SA]  Foram detectados Condicionadores ativos na Subestação!")
            else:
                logger.info(f"[SA]  Ainda há Condicionadores ativos na Subestação!")

            for condic in condics_ativos:
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
        if cls.l_sup_tensao_falha.valor:
            logger.warning("[SA]  Houve uma falha com a leitura de tensão supervisor, favor verificar.")

        if cls.l_sup_tensao_tsa_falha.valor:
            logger.warning("[SA]  Houve uma falha com a leitura de tensão do Serviço Auxiliar, favor verificar.")

        if cls.l_sup_tensao_gmg_falha.valor:
            logger.warning("[SA]  Houve uma falha com a leitura de tensão do Grupo Motor Gerador, favor verificar.")

        if cls.l_disj_gmg_fechado.valor:
            logger.warning("[SA]  Foi identificado que o Disjuntor do Grupo Motor Gerador, favor verificar.")

        if cls.l_disjs_modo_remoto.valor:
            logger.warning("[SA]  Foi identificado que os Disjuntores entraram em modo remoto, favor verificar.")

        if cls.l_poco_dren_nv_alto.valor:
            logger.warning("[SA]  O nível do Poço de Drenagem está alto, favor verificar.")

        if cls.l_dren_boias_discrepancia.valor:
            logger.warning("[SA]  Foi identificada uma discrepância nas Boias de Drenagem, favor verificar.")

        if cls.l_poco_dren_nv_muito_baixo.valor:
            logger.warning("[SA]  O nível do Poço de Drenagem está muito baixo, favor verificar.")

        if cls.l_dren_bomba_1_indisp.valor:
            logger.warning("[SA]  A Bomba de Drenagem 1 entrou em modo indisponível, favor verificar.")

        if cls.l_dren_bomba_2_indisp.valor:
            logger.warning("[SA]  A Bomba de Drenagem 2 entrou em modo indisponível, favor verificar.")

        if cls.l_esgot_bomba_1_falha.valor:
            logger.warning("[SA]  Foi identificado uma falha com a Bomba de Esgotamento 1, favor verificar.")

        if cls.l_esgot_bomba_2_falha.valor:
            logger.warning("[SA]  Foi identificado uma falha com a Bomba de Esgotamento 2, favor verificar.")

        if cls.l_esgot_bomba_1_indisp.valor:
            logger.warning("[SA]  A Bomba de Esgotamento 1 entrou em modo indisponível, favor verificar.")

        if cls.l_esgot_bomba_2_indisp.valor:
            logger.warning("[SA]  A Bomba de Esgotamento 2 entrou em modo indisponível, favor verificar.")

        if cls.l_poco_dren_bomba_1_defeito.valor:
            logger.warning("[SA]  Foi dentificado um defeito na Bomba de Drenagem 1, favor verificar.")

        if cls.l_poco_dren_bomba_2_defeito.valor:
            logger.warning("[SA]  Foi dentificado um defeito na Bomba de Drenagem 2, favor verificar.")

        if cls.l_sfa_limp_elem_1_aberta.valor:
            logger.warning("[SA]  Foi identificado que o Elemento de Limpeza 1 do Sistema de Filtragem A foi aberto, favor verificar.")

        if cls.l_sfa_limp_elem_2_aberta.valor:
            logger.warning("[SA]  Foi identificado que o Elemento de Limpeza 2 do Sistema de Filtragem A foi aberto, favor verificar.")

        if cls.l_sfa_entra_elem_1_aberta.valor:
            logger.warning("[SA]  Foi identificado que a Entrada do Elemento 1 do Sistema de Filtragem A foi aberto, favor verificar.")

        if cls.l_sfa_entra_elem_2_aberta.valor:
            logger.warning("[SA]  Foi identificado que a Entrada do Elemento 2 do Sistema de Filtragem A foi aberto, favor verificar.")

        if cls.l_sfa_falha_abrir_limpeza_elem_1.valor:
            logger.warning("[SA]  Houve uma falha ao abrir a Limpeza do Elemento 1 do Sistema de Filtragem A, favor verificar.")

        if cls.l_sfa_falha_fechar_limpeza_elem_1.valor:
            logger.warning("[SA]  Houve uma falha ao fechar a Limpeza do Elemento 1 do Sistema de Filtragem A, favor verificar.")

        if cls.l_sfa_falha_abrir_limpeza_elem_2.valor:
            logger.warning("[SA]  Houve uma falha ao abrir a Limpeza do Elemento 2 do Sistema de Filtragem A, favor verificar.")

        if cls.l_sfa_falha_fechar_limpeza_elem_2.valor:
            logger.warning("[SA]  Houve uma falha ao fechar a Limpeza do Elemento 2 do Sistema de Filtragem A, favor verificar.")

        if cls.l_sfa_falha_abrir_entra_elem_1.valor:
            logger.warning("[SA]  Houve uma falha ao abrir a Entrada do Elemento 1 do Sistema de Filtragem A, favor verificar.")

        if cls.l_sfa_falha_fechar_entra_elem_1.valor:
            logger.warning("[SA]  Houve uma falha ao fechar a Entrada do Elemento 1 do Sistema de Filtragem A, favor verificar.")

        if cls.l_sfa_falha_abrir_entra_elem_2.valor:
            logger.warning("[SA]  Houve uma falha ao abrir a Entrada do Elemento 2 do Sistema de Filtragem A, favor verificar.")

        if cls.l_sfa_falha_fechar_entra_elem_2.valor:
            logger.warning("[SA]  Houve uma falha ao fechar a Entrada do Elemento 2 do Sistema de Filtragem A, favor verificar.")

        if cls.l_sfb_limp_elem_1_aberta.valor:
            logger.warning("[SA]  Foi identificado que o Elemento de Limpeza 1 do Sistema de Filtragem B foi aberto, favor verificar.")

        if cls.l_sfb_limp_elem_2_aberta.valor:
            logger.warning("[SA]  Foi identificado que o Elemento de Limpeza 2 do Sistema de Filtragem B foi aberto, favor verificar.")

        if cls.l_sfb_entra_elem_1_aberta.valor:
            logger.warning("[SA]  Foi identificado que a Entrada do Elemento 1 do Sistema de Filtragem B foi aberto, favor verificar.")

        if cls.l_sfb_entra_elem_2_aberta.valor:
            logger.warning("[SA]  Foi identificado que a Entrada do Elemento 2 do Sistema de Filtragem B foi aberto, favor verificar.")

        if cls.l_sfb_falha_abrir_limpeza_elem_1.valor:
            logger.warning("[SA]  Houve uma falha ao abrir a Limpeza do Elemento 1 do Sistema de Filtragem B, favor verificar.")

        if cls.l_sfb_falha_fechar_limpeza_elem_1.valor:
            logger.warning("[SA]  Houve uma falha ao fechar a Limpeza do Elemento 1 do Sistema de Filtragem B, favor verificar.")

        if cls.l_sfb_falha_abrir_limpeza_elem_2.valor:
            logger.warning("[SA]  Houve uma falha ao abrir a Limpeza do Elemento 2 do Sistema de Filtragem B, favor verificar.")

        if cls.l_sfb_falha_fechar_limpeza_elem_2.valor:
            logger.warning("[SA]  Houve uma falha ao fechar a Limpeza do Elemento 2 do Sistema de Filtragem B, favor verificar.")

        if cls.l_sfb_falha_abrir_entra_elem_1.valor:
            logger.warning("[SA]  Houve uma falha ao abrir a Entrada do Elemento 1 do Sistema de Filtragem B, favor verificar.")

        if cls.l_sfb_falha_fechar_entra_elem_1.valor:
            logger.warning("[SA]  Houve uma falha ao fechar a Entrada do Elemento 1 do Sistema de Filtragem B, favor verificar.")

        if cls.l_sfb_falha_abrir_entra_elem_2.valor:
            logger.warning("[SA]  Houve uma falha ao abrir a Entrada do Elemento 2 do Sistema de Filtragem B, favor verificar.")

        if cls.l_sfb_falha_fechar_entra_elem_2.valor:
            logger.warning("[SA]  Houve uma falha ao fechar a Entrada do Elemento 2 do Sistema de Filtragem B, favor verificar.")

        if cls.l_nv_jusante_alto.valor:
            logger.warning("[SA]  Foi identificado que o Nível Jusante está alto, favor verificar.")

        if cls.l_nv_jusante_muito_baixo.valor:
            logger.warning("[SA]  Foi identificado que o Nível Jusante está muito baixo, favor verificar.")

        if cls.l_nv_jusante_falha_leitura.valor:
            logger.warning("[SA]  Houve uma falha na leitura de Nível Jusante, favor verificar.")

        if cls.l_sfa_press_lado_sujo_falha_leitura.valor:
            logger.warning("[SA]  Houve uma falha de leitura no lado sujo do Sistema de Filtragem A, favor verificar.")

        if cls.l_sfa_press_lado_limpo_falha_leitura.valor:
            logger.warning("[SA]  Houve uma falha de leitura no lado limpo do Sistema de Filtragem A, favor verificar.")

        if cls.l_sfb_press_lado_sujo_falha_leitura.valor:
            logger.warning("[SA]  Houve uma falha de leitura no lado sujo do Sistema de Filtragem B, favor verificar.")

        if cls.l_sfb_press_lado_limpo_falha_leitura.valor:
            logger.warning("[SA]  Houve uma falha de leitura no lado limpo do Sistema de Filtragem B, favor verificar.")

        if cls.l_sfa_press_lado_sujo_baixo.valor:
            logger.warning("[SA]  Foi identificado que a pressão do lado sujo do Sistema de Filtragem A está baixa, favor verificar.")

        if cls.l_sfa_press_lado_limpo_baixo.valor:
            logger.warning("[SA]  Foi identificado que a pressão do lado limpo do Sistema de Filtragem A está baixa, favor verificar.")

        if cls.l_sfa_press_lado_sujo_muito_baixo.valor:
            logger.warning("[SA]  Foi identificado que a pressão do lado sujo do Sistema de Filtragem A está muito baixa, favor verificar.")

        if cls.l_sfa_press_lado_limpo_muito_baixo.valor:
            logger.warning("[SA]  ,Foi identificado que a pressão do lado limpo do Sistema de Filtragem A está muito baixa favor verificar.")

        if cls.l_sfb_press_lado_sujo_baixo.valor:
            logger.warning("[SA]  Foi identificado que a pressão do lado sujo do Sistema de Filtragem B está baixa, favor verificar.")

        if cls.l_sfb_press_lado_limpo_baixo.valor:
            logger.warning("[SA]  Foi identificado que a pressão do lado limpo do Sistema de Filtragem B está baixa, favor verificar.")

        if cls.l_sfb_press_lado_sujo_muito_baixo.valor:
            logger.warning("[SA]  Foi identificado que a pressão do lado sujo do Sistema de Filtragem B está muito baixa, favor verificar.")

        if cls.l_sfb_press_lado_limpo_muito_baixo.valor:
            logger.warning("[SA]  Foi identificado que a pressão do lado limpo do Sistema de Filtragem B está muito baixa, favor verificar.")

        # WHATSAPP + VOIP
        if cls.l_disj_gmg_trip.valor and not d.voip["SA_ED_PSA_DISJ_GMG_TRIP"][0]:
            logger.warning("[SA]  Foi identificado um sinal de Trip do Grupo Motor Gerador, favor verificar.")
            d.voip["SA_ED_PSA_DISJ_GMG_TRIP"][0] = True
        elif not cls.l_disj_gmg_trip.valor and d.voip["SA_ED_PSA_DISJ_GMG_TRIP"][0]:
            d.voip["SA_ED_PSA_DISJ_GMG_TRIP"][0] = False

        if cls.l_dps_gmg_falha.valor and not d.voip["SA_ED_PSA_DPS_GMG"][0]:
            logger.warning("[SA]  Houve uma falha com o Grupo Motor Gerador, favor verificar.")
            d.voip["SA_ED_PSA_DPS_GMG"][0] = True
        elif not cls.l_dps_gmg_falha.valor and d.voip["SA_ED_PSA_DPS_GMG"][0]:
            d.voip["SA_ED_PSA_DPS_GMG"][0] = False

        if cls.l_carreg_baterias_falha.valor and not d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"][0]:
            logger.warning("[SA]  Houve uma falha com o Carregador de Baterias, favor verificar.")
            d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"][0] = True
        elif not cls.l_carreg_baterias_falha.valor and d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"][0]:
            d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"][0] = False

        if cls.l_sfa_press_lado_sujo_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"][0]:
            logger.warning("[SA]  Foi identificado que a pressão do lado sujo do Sistema de Filtragem A está alto, favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"][0] = True
        elif not cls.l_sfa_press_lado_sujo_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"][0] = False

        if cls.l_sfa_press_lado_limpo_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"][0]:
            logger.warning("[SA]  Foi identificado que a pressão do lado limpo do Sistema de Filtragem A está alto, favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"][0] = True
        elif not cls.l_sfa_press_lado_limpo_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"][0] = False

        if cls.l_sfa_press_lado_sujo_muito_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"][0]:
            logger.warning("[SA]  Foi identificado que a pressão do lado sujo do Sistema de Filtragem A está muito alto, favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"][0] = True
        elif not cls.l_sfa_press_lado_sujo_muito_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"][0] = False

        if cls.l_sfa_press_lado_limpo_muito_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0]:
            logger.warning("[SA]  Foi identificado que a pressão do lado limpo do Sistema de Filtragem A está muito alto, favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"][0] = True
        elif not cls.l_sfa_press_lado_limpo_muito_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0] = False

        if cls.l_sfb_press_lado_sujo_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"][0]:
            logger.warning("[SA]  Foi identificado que a pressão do lado sujo do Sistema de Filtragem B está alto, favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"][0] = True
        elif not cls.l_sfb_press_lado_sujo_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"][0] = False

        if cls.l_sfb_press_lado_limpo_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"][0]:
            logger.warning("[SA]  Foi identificado que a pressão do lado limpo do Sistema de Filtragem B está alto, favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"][0] = True
        elif not cls.l_sfb_press_lado_limpo_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"][0] = False

        if cls.l_sfb_press_lado_sujo_muito_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"][0]:
            logger.warning("[SA]  Foi identificado que a pressão do lado sujo do Sistema de Filtragem B está muito alto, favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"][0] = True
        elif not cls.l_sfb_press_lado_sujo_muito_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"][0] = False

        if cls.l_sfb_press_lado_limpo_muito_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0]:
            logger.warning("[SA]  Foi identificado que a pressão do lado limpo do Sistema de Filtragem B está muito alto, favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"][0] = True
        elif not cls.l_sfb_press_lado_limpo_muito_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"][0] = False


    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """

        ## CONDICIONADORES ESSENCIAIS
        cls.l_bloq_rele_86btbf = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_RELE_BLOQUEIO_86BTBF"], descricao="[USN] Bloqueio 86BTBF Relé SA")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_bloq_rele_86btbf, CONDIC_NORMALIZAR))

        cls.l_bloq_botao_86btbf = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_BOTAO_BLOQUEIO_86BTBF"], descricao="[USN] Botão Bloqueio 86BTBF Relé SA pressionado")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_bloq_botao_86btbf, CONDIC_NORMALIZAR))

        cls.l_prtva1_50bf = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_PRTVA1_50BF"], descr="[USN] Bloqueio Relé 50BF PRTVA 1")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_prtva1_50bf, CONDIC_NORMALIZAR))

        cls.l_prtva2_50bf = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_PRTVA2_50BF"], descr="[USN] Bloqueio Relé 50BF PRTVA 2")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_prtva2_50bf, CONDIC_NORMALIZAR))


        ## CONDICIONADORES NORMAIS
        cls.l_disj_tsa_trip = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_DISJ_TSA_TRIP"], descricao="[USN] Trip Disjuntor Serviço Auxiliar")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_disj_tsa_trip, CONDIC_INDISPONIBILIZAR))

        cls.l_poco_dren_nivel_muito_alto = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_ALTO"], descricao="[USN] Poço de Drenagem Nível Muito Alto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_poco_dren_nivel_muito_alto, CONDIC_INDISPONIBILIZAR))

        cls.l_nv_jusante_muito_alto = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_NIVEL_JUSANTE_MUITO_ALTO"], descricao="[USN] Nível Jusante Muito Alto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_nv_jusante_muito_alto, CONDIC_INDISPONIBILIZAR))

        cls.l_dps_tsa = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_DPS_TSA"], descricao="[USN] Falha Disjuntor Serviço Auxiliar")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dps_tsa, CONDIC_INDISPONIBILIZAR))

        cls.l_disj_gmg_falha_abrir = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_GMG_DISJ_FALHA_ABRIR"], descricao="[USN] Falha Abertura Disjuntor Grupo Motor Gerador")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_disj_gmg_falha_abrir, CONDIC_INDISPONIBILIZAR))

        cls.l_disj_tsa_falha_fechar = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_TSA_DISJ_FALHA_FECHAR"], descricao="[USN] Falha Fechamento Disjuntor Serviço Auxiliar")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_disj_tsa_falha_fechar, CONDIC_INDISPONIBILIZAR))

        cls.l_disj_tsa_falha_abrir = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_TSA_DISJ_FALHA_ABRIR"], descricao="[USN] Falha Abertura Disjuntor Serviço Auxiliar")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_disj_tsa_falha_abrir, CONDIC_INDISPONIBILIZAR))

        cls.l_bloq_50bf_atuado = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_BLOQUEIO_50BF_ATUADO"], descricao="[USN] Bloqueio 50BF Relé SA Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_bloq_50bf_atuado, CONDIC_INDISPONIBILIZAR))

        cls.l_bloq_86btlsa_atuado = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_BLOQUEIO_86BTLSA_ATUADO"], descricao="[USN] Bloqueio 86BTLSA Relé SA Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_bloq_86btlsa_atuado, CONDIC_INDISPONIBILIZAR))

        cls.l_bloq_stt_50bf = lei.LeituraModbusCoil(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_STT_BLOQUEIO_50BF"], descricao="[USN] Status Bloqueio 50BF Relé SA")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_bloq_stt_50bf, CONDIC_INDISPONIBILIZAR))

        cls.l_bloq_stt_86btlsa = lei.LeituraModbusCoil(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_STT_BLOQUEIO_86BTLSA"], descricao="[USN] Status Bloqueio 86BTLSA Relé SA")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_bloq_stt_86btlsa, CONDIC_INDISPONIBILIZAR))


        ## WHATSAPP/VOIP
        cls.l_dps_gmg_falha = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_DPS_GMG"], descricao="[USN] Falha Grupo Motor Gerador")
        cls.l_disj_gmg_trip = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_DISJ_GMG_TRIP"], descricao="[USN] Trip Disjuntor Grupo Motor Gerador")
        cls.l_carreg_baterias_falha = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"], descricao="[USN] Falha Carregador de Baterias")
        cls.l_disj_gmg_falha_fechar = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_GMG_DISJ_FALHA_FECHAR"], descricao="[USN] Falha Fechamento Disjuntor Grupo Motor Gerador")
        cls.l_disj_gmg_fechado = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_DIJS_GMG_FECHADO"], descricao="[USN] Disjuntor Grupo Motor Gerador Fechado")
        cls.l_disjs_modo_remoto = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_DISJUNTORES_MODO_REMOTO"], descricao="[USN] Disjuntores em Modo Remoto")

        cls.l_sfa_press_lado_sujo_alto = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"], descricao="[USN] Pressão Sistema de Filtragem A Lado Sujo Alta")
        cls.l_sfa_press_lado_limpo_alto = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"], descricao="[USN] Pressão Sistema de Filtragem A Lado Limpo Alta")
        cls.l_sfa_press_lado_sujo_muito_alto = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"], descricao="[USN] Pressão Sistema de Filtragem A Lado Sujo Muito Alta")
        cls.l_sfa_press_lado_limpo_muito_alto = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"], descricao="[USN] Pressão Sistema de Filtragem A Lado Limpo Muito Alta")

        cls.l_sfb_press_lado_sujo_alto = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"], descricao="[USN] Pressão Sistema de Filtragem B Lado Sujo Alta")
        cls.l_sfb_press_lado_limpo_alto = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"], descricao="[USN] Pressão Sistema de Filtragem B Lado Limpo Alta")
        cls.l_sfb_press_lado_sujo_muito_alto = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"], descricao="[USN] Pressão Sistema de Filtragem B Lado Sujo Muito Alta")
        cls.l_sfb_press_lado_limpo_muito_alto = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO"], descricao="[USN] Pressão Sistema de Filtragem B Lado Limpo Muito Alta")

        cls.l_sup_tensao_falha = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SUPERVISOR_TENSAO_FALHA"], descricao="[USN] Falha Tensão pelo Supervisório")
        cls.l_sup_tensao_tsa_falha = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SUPERVISOR_TENSAO_TSA_FALHA"], descricao="[USN] Falha Tensão Serviço Auxiliar pelo Supervisório")
        cls.l_sup_tensao_gmg_falha = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SUPERVISOR_TENSAO_GMG_FALHA"], descricao="[USN] Falha Tensão Grupo Motor Gerador pelo Supervisório")

        cls.l_poco_dren_nv_alto = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_ALTO"], descricao="[USN] Poço de Drenagem Nível Alto")
        cls.l_dren_boias_discrepancia = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_DREANGEM_BOIAS_DISCREPANCIA"], descricao="[USN] Dicrepância Boias de Drenagem")
        cls.l_poco_dren_nv_muito_baixo = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_BAIXO"], descricao="[USN] Poço de Drenagem Nível Muito Alto")

        cls.l_dren_bomba_1_indisp = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_DREANGEM_BOMBA_1_INDISP"], descricao="[USN] Bomba de Drenagem 1 Indisponível")
        cls.l_dren_bomba_2_indisp = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_DREANGEM_BOMBA_2_INDISP"], descricao="[USN] Bomba de Drenagem 2 Indisponível")
        cls.l_esgot_bomba_1_falha = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_ESGOTAMENTO_BOMBA_1_FALHA"], descricao="[USN] Falha Bomba de Esgotamento 1")
        cls.l_esgot_bomba_2_falha = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_ESGOTAMENTO_BOMBA_2_FALHA"], descricao="[USN] Falha Bomba de Esgotamento 2") # TODO -> verificar invertido
        cls.l_esgot_bomba_1_indisp = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_ESGOTAMENTO_BOMBA_1_INDISP"], descricao="[USN] Bomba de Esgotamento 1 Indisponível")
        cls.l_esgot_bomba_2_indisp = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_ESGOTAMENTO_BOMBA_2_INDISP"], descricao="[USN] Bomba de Esgotamento 2 Indisponível")
        cls.l_poco_dren_bomba_1_defeito = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_POCO_DRENAGEM_BOMBA_1_DEFEITO"], descricao="[USN] Defeito Bomba 1 Poço de Drenagem")
        cls.l_poco_dren_bomba_2_defeito = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_POCO_DRENAGEM_BOMBA_2_DEFEITO"], descricao="[USN] Defeito Bomba 2 Poço de Drenagem")

        cls.l_sfa_limp_elem_1_aberta = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFA_LIMPEZA_ELEMENTO_1_ABERTA"], descricao="[USN] Sistema de Filtragem A Elemento 1 Aberto")
        cls.l_sfa_limp_elem_2_aberta = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFA_LIMPEZA_ELEMENTO_2_ABERTA"], descricao="[USN] Sistema de Filtragem A Elemento 2 Aberto")
        cls.l_sfa_entra_elem_1_aberta = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFA_ENTRADA_ELEMENTO_1_ABERTA"], descricao="[USN] Sistema de Filtragem A Entrada Elemento 1 Aberto") # TODO -> verificar invertido
        cls.l_sfa_entra_elem_2_aberta = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFA_ENTRADA_ELEMENTO_2_ABERTA"], descricao="[USN] Sistema de Filtragem A Entrada Elemento 2 Aberto")
        cls.l_sfa_falha_abrir_limpeza_elem_1 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_ABRIR_LIMPEZA_ELEM_1"], descricao="[USN] Falha Abrir Limpeza do Elemento 1 do Sistema de Filtragem A")
        cls.l_sfa_falha_fechar_limpeza_elem_1 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_FECHAR_LIMPEZA_ELEM_1"], descricao="[USN] Falha Fechar limpeza do Elemento 1 do Sistema de Filtragem A")
        cls.l_sfa_falha_abrir_entra_elem_1 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_ABRIR_ENTRADA_ELEM_1"], descricao="[USN] Falha Abrir Entrada Elemento 1 do Sistema de Filtragem A")
        cls.l_sfa_falha_fechar_entra_elem_1 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_FECHAR_ENTRADA_ELEM_1"], descricao="[USN] Falha Fechar Entrada Elemento 1 do Sistema de Filtragem A")
        cls.l_sfa_falha_abrir_limpeza_elem_2 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_ABRIR_LIMPEZA_ELEM_2"], descricao="[USN] Falha Abrir Limpeza do Elemento 2 do Sistema de Filtragem A")
        cls.l_sfa_falha_fechar_limpeza_elem_2 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_FECHAR_LIMPEZA_ELEM_2"], descricao="[USN] Falha Fechar limpeza do Elemento 2 do Sistema de Filtragem A")
        cls.l_sfa_falha_abrir_entra_elem_2 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_ABRIR_ENTRADA_ELEM_2"], descricao="[USN] Falha Abrir Entrada Elemento 2 do Sistema de Filtragem A")
        cls.l_sfa_falha_fechar_entra_elem_2 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_FECHAR_ENTRADA_ELEM_2"], descricao="[USN] Falha Fechar Entrada Elemento 2 do Sistema de Filtragem A")

        cls.l_sfb_limp_elem_1_aberta = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFB_LIMPEZA_ELEMENTO_1_ABERTA"], descricao="[USN] Sistema de Filtragem B Elemento 1 Aberto") # TODO -> verificar invertido
        cls.l_sfb_limp_elem_2_aberta = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFB_LIMPEZA_ELEMENTO_2_ABERTA"], descricao="[USN] Sistema de Filtragem B Elemento 2 Aberto")
        cls.l_sfb_entra_elem_1_aberta = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFB_ENTRADA_ELEMENTO_1_ABERTA"], descricao="[USN] Sistema de Filtragem B Entrada Elemento 1 Aberto")
        cls.l_sfb_entra_elem_2_aberta = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFB_ENTRADA_ELEMENTO_2_ABERTA"], descricao="[USN] Sistema de Filtragem B Entrada Elemento 2 Aberto")
        cls.l_sfb_falha_abrir_limpeza_elem_1 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_ABRIR_LIMPEZA_ELEM_1"], descricao="[USN] Falha Abrir Limpeza do Elemento 1 do Sistema de Filtragem B")
        cls.l_sfb_falha_fechar_limpeza_elem_1 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_FECHAR_LIMPEZA_ELEM_1"], descricao="[USN] Falha Fechar limpeza do Elemento 1 do Sistema de Filtragem B")
        cls.l_sfb_falha_abrir_entra_elem_1 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_ABRIR_ENTRADA_ELEM_1"], descricao="[USN] Falha Abrir Entrada Elemento 1 do Sistema de Filtragem B") # TODO -> verificar invertido
        cls.l_sfb_falha_fechar_entra_elem_1 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_FECHAR_ENTRADA_ELEM_1"], descricao="[USN] Falha Fechar Entrada Elemento 1 do Sistema de Filtragem B")
        cls.l_sfb_falha_abrir_limpeza_elem_2 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_ABRIR_LIMPEZA_ELEM_2"], descricao="[USN] Falha Abrir Limpeza do Elemento 2 do Sistema de Filtragem B")
        cls.l_sfb_falha_fechar_limpeza_elem_2 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_FECHAR_LIMPEZA_ELEM_2"], descricao="[USN] Falha Fechar limpeza do Elemento 2 do Sistema de Filtragem B")
        cls.l_sfb_falha_abrir_entra_elem_2 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_ABRIR_ENTRADA_ELEM_2"], descricao="[USN] Falha Abrir Entrada Elemento 2 do Sistema de Filtragem B")
        cls.l_sfb_falha_fechar_entra_elem_2 = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_FECHAR_ENTRADA_ELEM_2"], descricao="[USN] Falha Fechar Entrada Elemento 2 do Sistema de Filtragem B")

        cls.l_nv_jusante_alto = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_NIVEL_JUSANTE_ALTO"], descricao="[USN] Nível Jusante Alto")
        cls.l_nv_jusante_muito_baixo = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_NIVEL_JUSANTE_MUITO_BAIXO"], descricao="[USN] Nível Jusante Muito Baixo")
        cls.l_nv_jusante_falha_leitura = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_NIVEL_JUSANTE_FALHA_LEITURA"], descricao="[USN] Falha Leitura Nível Jusante")

        cls.l_sfa_press_lado_sujo_falha_leitura = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_FALHA_LEITURA"], descricao="[USN] Falha Leitura Pressão Sistema de Filtragem A Lado Sujo")
        cls.l_sfa_press_lado_limpo_falha_leitura = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_FALHA_LEITURA"], descricao="[USN] Falha Leitura Pressão Sistema de Filtragem A Lado Limpo")

        cls.l_sfb_press_lado_sujo_falha_leitura = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_FALHA_LEITURA"], descricao="[USN] Falha Leitura Pressão Sistema de Filtragem B Lado Sujo")
        cls.l_sfb_press_lado_limpo_falha_leitura = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_FALHA_LEITURA"], descricao="[USN] Falha Leitura Pressão Sistema de Filtragem B Lado Limpo")

        cls.l_sfa_press_lado_sujo_baixo = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_BAIXO"], descricao="[USN] Pressão Sistema de Filtragem A Lado Sujo Baixo")
        cls.l_sfa_press_lado_limpo_baixo = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_BAIXO"], descricao="[USN] Pressão Sistema de Filtragem A Lado Limpo Baixo")
        cls.l_sfa_press_lado_sujo_muito_baixo = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_BAIXO"], descricao="[USN] Pressão Sistema de Filtragem A Lado Sujo Muito Baixo")
        cls.l_sfa_press_lado_limpo_muito_baixo = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_BAIXO"], descricao="[USN] Pressão Sistema de Filtragem A Lado Limpo Muito Baixo")

        cls.l_sfb_press_lado_sujo_baixo = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_BAIXO"], descricao="[USN] Pressão Sistema de Filtragem A Lado Sujo Baixo")
        cls.l_sfb_press_lado_limpo_baixo = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_BAIXO"], descricao="[USN] Pressão Sistema de Filtragem A Lado Limpo Baixo")
        cls.l_sfb_press_lado_sujo_muito_baixo = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_BAIXO"], descricao="[USN] Pressão Sistema de Filtragem A Lado Sujo Muito Baixo")
        cls.l_sfb_press_lado_limpo_muito_baixo = lei.LeituraModbusBit(cls.clp["SA"], REG_SASE["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_BAIXO"], descricao="[USN] Pressão Sistema de Filtragem A Lado Limpo Muito Baixo")