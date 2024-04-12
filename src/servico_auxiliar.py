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
import src.conectores.banco_dados as bd
import src.funcoes.condicionadores as c
import src.conectores.servidores as serv

from time import sleep
from datetime import datetime

from src.dicionarios.const import *
from src.dicionarios.reg_elipse import *


logger = logging.getLogger("logger")


class ServicoAuxiliar:

    # ATRIBUIÇÃO DE VARIÁVEIS
    bd: "bd.BancoDados" = None

    status_dj_tsa = lei.LeituraModbusBit(
        serv.Servidores.clp["SA"],
        REG_SASE["DISJUNTOR_TSA_FECHADO"],
        descricao="[SA]  Status Disjuntor SA"
    )

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_ativos: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []


    @classmethod
    def resetar_emergencia(cls) -> "bool":
        try:
            res = esc.EscritaModBusBit.escrever_bit(serv.Servidores.clp["SA"], REG_SASE["CMD_REARME_FALHAS"], valor=1)
            return res

        except Exception:
            logger.error(f"[SA]  Houve um erro ao realizar o Reset de Emergência.")
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
                logger.debug(f"[SA]  Foram detectados Condicionadores ativos no Serviço Auxiliar!")
            else:
                logger.debug(f"[SA]  Ainda há Condicionadores ativos no Serviço Auxiliar!")

            for condic in condics_ativos:
                if condic.teste:
                    logger.debug(f"[SA]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\", Obs.: \"TESTE\"")
                    continue

                elif condic in cls.condicionadores_ativos:
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
                    sleep(1)
                    autor += 1

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
            logger.warning("[SA]  Sinal de falha de leitura de Supervisor de Tensão identificado. Favor verificar.")

        if cls.l_sup_tensao_tsa_falha.valor:
            logger.warning("[SA]  Sinal de falha de leitura de Tensão do Serviço Auxiliar identificado. Favor verificar.")

        if cls.l_disj_gmg_fechado.valor:
            logger.warning("[SA]  O Disjuntor do Grupo Motor Gerador foi fechado. Favor verificar.")

        if cls.l_disjs_modo_remoto.valor:
            logger.warning("[SA]  Os Disjuntores do Serviço Auxiliar entraram em Modo Remoto. Favor verificar.")

        if cls.l_poco_dren_nv_alto.valor:
            logger.warning("[SA]  O nível do Poço de Drenagem está Alto. Favor verificar.")

        if cls.l_dren_boias_discrepancia.valor:
            logger.warning("[SA]  Sinal de Discrepância nas Boias de Drenagem identificado. Favor verificar.")

        if cls.l_poco_dren_nv_muito_baixo.valor:
            logger.warning("[SA]  O nível do Poço de Drenagem está Muito Baixo. Favor verificar.")

        if cls.l_dren_bomba_1_indisp.valor:
            logger.warning("[SA]  A Bomba de Drenagem 1 entrou em modo Indisponível. Favor verificar.")

        if cls.l_dren_bomba_2_indisp.valor:
            logger.warning("[SA]  A Bomba de Drenagem 2 entrou em modo Indisponível. Favor verificar.")

        if cls.l_esgot_bomba_1_falha.valor:
            logger.warning("[SA]  Sinal de falha na Bomba de Esgotamento 1 identificado. Favor verificar.")

        if cls.l_esgot_bomba_2_falha.valor:
            logger.warning("[SA]  Sinal de falha na Bomba de Esgotamento 2 identificado. Favor verificar.")

        if cls.l_esgot_bomba_1_indisp.valor:
            logger.warning("[SA]  A Bomba de Esgotamento 1 entrou em modo Indisponível. Favor verificar.")

        if cls.l_poco_dren_bomba_1_defeito.valor:
            logger.warning("[SA]  Sinal de defeito na Bomba de Drenagem 1 identificado. Favor verificar.")

        if cls.l_poco_dren_bomba_2_defeito.valor:
            logger.warning("[SA]  Sinal de defeito na Bomba de Drenagem 2 identificado. Favor verificar.")

        if cls.l_sfa_falha_abrir_limpeza_elem_1.valor:
            logger.warning("[SA]  Sinal de falha ao abrir a Limpeza do Elemento 1 do Sistema de Filtragem A identificado. Favor verificar.")

        if cls.l_sfa_falha_fechar_limpeza_elem_1.valor:
            logger.warning("[SA]  Sinal de falha ao fechar a Limpeza do Elemento 1 do Sistema de Filtragem A identificado. Favor verificar.")

        if cls.l_sfa_falha_fechar_limpeza_elem_2.valor:
            logger.warning("[SA]  Sinal de falha ao fechar a Limpeza do Elemento 2 do Sistema de Filtragem A identificado. Favor verificar.")

        if cls.l_sfa_falha_abrir_entra_elem_1.valor:
            logger.warning("[SA]  Sinal de falha ao abrir a Entrada do Elemento 1 do Sistema de Filtragem A identificado. Favor verificar.")

        if cls.l_sfa_falha_fechar_entra_elem_1.valor:
            logger.warning("[SA]  Sinal de falha ao fechar a Entrada do Elemento 1 do Sistema de Filtragem A identificado. Favor verificar.")

        if cls.l_sfa_falha_abrir_entra_elem_2.valor:
            logger.warning("[SA]  Sinal de falha ao abrir a Entrada do Elemento 2 do Sistema de Filtragem A identificado. Favor verificar.")

        if cls.l_sfa_falha_fechar_entra_elem_2.valor:
            logger.warning("[SA]  Sinal de falha ao fechar a Entrada do Elemento 2 do Sistema de Filtragem A identificado. Favor verificar.")

        if cls.l_sfb_falha_abrir_limpeza_elem_1.valor:
            logger.warning("[SA]  Sinal de falha ao abrir a Limpeza do Elemento 1 do Sistema de Filtragem B identificado. Favor verificar.")

        if cls.l_sfb_falha_fechar_limpeza_elem_1.valor:
            logger.warning("[SA]  Sinal de falha ao fechar a Limpeza do Elemento 1 do Sistema de Filtragem B identificado. Favor verificar.")

        if cls.l_sfb_falha_abrir_limpeza_elem_2.valor:
            logger.warning("[SA]  Sinal de falha ao abrir a Limpeza do Elemento 2 do Sistema de Filtragem B identificado. Favor verificar.")

        if cls.l_sfb_falha_fechar_limpeza_elem_2.valor:
            logger.warning("[SA]  Sinal de falha ao fechar a Limpeza do Elemento 2 do Sistema de Filtragem B identificado. Favor verificar.")

        if cls.l_sfb_falha_abrir_entra_elem_1.valor:
            logger.warning("[SA]  Sinal de falha ao abrir a Entrada do Elemento 1 do Sistema de Filtragem B identificado. Favor verificar.")

        if cls.l_sfb_falha_fechar_entra_elem_1.valor:
            logger.warning("[SA]  Sinal de falha ao fechar a Entrada do Elemento 1 do Sistema de Filtragem B identificado. Favor verificar.")

        if cls.l_sfb_falha_abrir_entra_elem_2.valor:
            logger.warning("[SA]  Sinal de falha ao abrir a Entrada do Elemento 2 do Sistema de Filtragem B identificado. Favor verificar.")

        if cls.l_sfb_falha_fechar_entra_elem_2.valor:
            logger.warning("[SA]  Sinal de falha ao fechar a Entrada do Elemento 2 do Sistema de Filtragem B identificado. Favor verificar.")

        if cls.l_nv_jusante_alto.valor:
            logger.warning("[SA]  O Nível Jusante está Alto. Favor verificar.")

        if cls.l_nv_jusante_muito_baixo.valor:
            logger.warning("[SA]  O Nível Jusante está Muito Baixo. Favor verificar.")

        if cls.l_nv_jusante_falha_leitura.valor:
            logger.warning("[SA]  Sinal de falha de leitura de Nível Jusante identificado. Favor verificar.")

        if cls.l_sfa_press_lado_sujo_falha_leitura.valor:
            logger.warning("[SA]  Sinal de falha de leitura no lado sujo do Sistema de Filtragem A identificado. Favor verificar.")

        if cls.l_sfa_press_lado_limpo_falha_leitura.valor:
            logger.warning("[SA]  Sinal de falha de leitura no lado limpo do Sistema de Filtragem A identificado. Favor verificar.")

        if cls.l_sfb_press_lado_sujo_falha_leitura.valor:
            logger.warning("[SA]  Sinal de falha de leitura no lado sujo do Sistema de Filtragem B identificado. Favor verificar.")

        if cls.l_sfb_press_lado_limpo_falha_leitura.valor:
            logger.warning("[SA]  Houve uma falha de leitura no lado limpo do Sistema de Filtragem B. Favor verificar.")

        if cls.l_sfa_press_lado_sujo_baixo.valor:
            logger.warning("[SA]  A Pressão do lado sujo do Sistema de Filtragem A está Baixa. Favor verificar.")

        if cls.l_sfa_press_lado_limpo_baixo.valor:
            logger.warning("[SA]  A Pressão do lado limpo do Sistema de Filtragem A está Baixa. Favor verificar.")

        if cls.l_sfa_press_lado_sujo_muito_baixo.valor:
            logger.warning("[SA]  A Pressão do lado sujo do Sistema de Filtragem A está Muito Baixa. Favor verificar.")

        if cls.l_sfa_press_lado_limpo_muito_baixo.valor:
            logger.warning("[SA]  A Pressão do lado limpo do Sistema de Filtragem A está Muito Baixa. Favor verificar.")

        if cls.l_sfb_press_lado_sujo_baixo.valor:
            logger.warning("[SA]  A Pressão do lado sujo do Sistema de Filtragem B está Baixa. Favor verificar.")

        if cls.l_sfb_press_lado_limpo_baixo.valor:
            logger.warning("[SA]  A Pressão do lado limpo do Sistema de Filtragem B está Baixa. Favor verificar.")

        if cls.l_sfb_press_lado_sujo_muito_baixo.valor:
            logger.warning("[SA]  A Pressão do lado sujo do Sistema de Filtragem B está Muito Baixa. Favor verificar.")

        if cls.l_sfb_press_lado_limpo_muito_baixo.valor:
            logger.warning("[SA]  A Pressão do lado limpo do Sistema de Filtragem B está Muito Baixa. Favor verificar.")

        # if cls.l_esgot_bomba_2_indisp.valor:
        #     logger.warning("[SA]  A Bomba de Esgotamento 2 entrou em modo Indisponível. Favor verificar.")

        if cls.l_sfa_falha_abrir_limpeza_elem_2.valor:
            logger.warning("[SA]  Sinal de falha ao abrir a Limpeza do Elemento 2 do Sistema de Filtragem A identificado. Favor verificar.")

        if cls.l_sup_tensao_gmg_falha.valor and cls.l_sup_tensao_tsa_falha.valor:
            logger.warning("[SA]  Sinal falha de leitura de Tensão do Grupo Motor Gerador identificado. Favor verificar.")


        # WHATSAPP + VOIP
        if cls.l_disj_gmg_trip.valor and not d.voip["DJ_GMG_TRIP"][0]:
            logger.warning("[SA]  Sinal de Trip do Grupo Motor Gerador identificado. Favor verificar.")
            d.voip["DJ_GMG_TRIP"][0] = True
        elif not cls.l_disj_gmg_trip.valor and d.voip["DJ_GMG_TRIP"][0]:
            d.voip["DJ_GMG_TRIP"][0] = False

        if cls.l_dps_gmg_falha.valor and not d.voip["SA_ED_PSA_DPS_GMG"][0]:
            logger.warning("[SA]  Sinal de falha do Grupo Motor Gerador identificado. Favor verificar.")
            d.voip["SA_ED_PSA_DPS_GMG"][0] = True
        elif not cls.l_dps_gmg_falha.valor and d.voip["SA_ED_PSA_DPS_GMG"][0]:
            d.voip["SA_ED_PSA_DPS_GMG"][0] = False

        if cls.l_carreg_baterias_falha.valor and not d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"][0]:
            logger.warning("[SA]  Sinal de falha do Carregador de Baterias identificado. Favor verificar.")
            d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"][0] = True
        elif not cls.l_carreg_baterias_falha.valor and d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"][0]:
            d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"][0] = False

        if cls.l_sfa_press_lado_sujo_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"][0]:
            logger.warning("[SA]  A Pressão do lado sujo do Sistema de Filtragem A está Alta. Favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"][0] = True
        elif not cls.l_sfa_press_lado_sujo_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"][0] = False

        if cls.l_sfa_press_lado_limpo_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"][0]:
            logger.warning("[SA]  A Pressão do lado limpo do Sistema de Filtragem A está Alta. Favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"][0] = True
        elif not cls.l_sfa_press_lado_limpo_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"][0] = False

        if cls.l_sfa_press_lado_sujo_muito_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"][0]:
            logger.warning("[SA]  A Pressão do lado sujo do Sistema de Filtragem A está Muito Alta. Favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"][0] = True
        elif not cls.l_sfa_press_lado_sujo_muito_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"][0] = False

        if cls.l_sfa_press_lado_limpo_muito_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0]:
            logger.warning("[SA]  A pressão do lado limpo do Sistema de Filtragem A está Muito Alta. Favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"][0] = True
        elif not cls.l_sfa_press_lado_limpo_muito_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0] = False

        if cls.l_sfb_press_lado_sujo_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"][0]:
            logger.warning("[SA]  A pressão do lado sujo do Sistema de Filtragem B está Alta. Favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"][0] = True
        elif not cls.l_sfb_press_lado_sujo_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"][0] = False

        if cls.l_sfb_press_lado_limpo_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"][0]:
            logger.warning("[SA]  A Pressão do lado limpo do Sistema de Filtragem B está Alta. Favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"][0] = True
        elif not cls.l_sfb_press_lado_limpo_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"][0] = False

        if cls.l_sfb_press_lado_sujo_muito_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"][0]:
            logger.warning("[SA]  A Pressão do lado sujo do Sistema de Filtragem B está Muito Alta. Favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"][0] = True
        elif not cls.l_sfb_press_lado_sujo_muito_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"][0] = False

        if cls.l_sfb_press_lado_limpo_muito_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0]:
            logger.warning("[SA]  A Pressão do lado limpo do Sistema de Filtragem B está Muito Alta. Favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"][0] = True
        elif not cls.l_sfb_press_lado_limpo_muito_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"][0] = False


    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """
        cls.l_disj_gmg_fechado = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["DISJUNTOR_GMG_FECHADO"], descricao="[SA]  Disjuntor Grupo Motor Gerador Fechado")


        ## CONDICIONADORES ESSENCIAIS
        cls.l_bloq_rele_86btbf = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["RELE_BLOQUEIO_86BTBF"], descricao="[SA]  Bloqueio 86BTBF Relé SA")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_bloq_rele_86btbf, CONDIC_NORMALIZAR, teste=True))

        cls.l_bloq_botao_86btbf = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["BOTAO_BLOQUEIO_86BTBF"], descricao="[SA]  Botão Bloqueio 86BTBF Relé SA Pressionado")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_bloq_botao_86btbf, CONDIC_NORMALIZAR, teste=True))

        cls.l_prtva1_50bf = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["PRTVA1_50_BF"], descricao="[SA]  Bloqueio Relé 50BF PRTVA 1")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_prtva1_50bf, CONDIC_NORMALIZAR, teste=True))

        cls.l_prtva2_50bf = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["PRTVA2_50BF"], descricao="[SA]  Bloqueio Relé 50BF PRTVA 2")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_prtva2_50bf, CONDIC_NORMALIZAR, teste=True))


        ## CONDICIONADORES NORMAIS
        cls.l_disj_tsa_trip = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["DISJUNTOR_TSA_TRIP"], descricao="[SA]  Trip Disjuntor Serviço Auxiliar")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_disj_tsa_trip, CONDIC_INDISPONIBILIZAR))

        cls.l_poco_dren_nivel_muito_alto = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["POCO_DRENAGEM_SENSOR_NIVEL_MUITO_ALTO"], descricao="[SA]  Poço de Drenagem Nível Muito Alto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_poco_dren_nivel_muito_alto, CONDIC_INDISPONIBILIZAR, teste=True))

        cls.l_nv_jusante_muito_alto = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["NIVEL_JUSANTE_MUITO_ALTO"], descricao="[SA]  Nível Jusante Muito Alto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_nv_jusante_muito_alto, CONDIC_INDISPONIBILIZAR))

        cls.l_dps_tsa = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["DPS_TSA"], descricao="[SA]  Dispositivo de Proteção de Surto Serviço Auxiliar")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_dps_tsa, CONDIC_INDISPONIBILIZAR, teste=True))

        cls.l_disj_gmg_falha_abrir = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["GMG_DISJUNTOR_FALHA_ABRIR"], descricao="[SA]  Falha Abertura Disjuntor Grupo Motor Gerador")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_disj_gmg_falha_abrir, CONDIC_INDISPONIBILIZAR))

        cls.l_disj_tsa_falha_fechar = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["GMG_DISJUNTOR_FALHA_FECHAR"], descricao="[SA]  Falha Fechamento Disjuntor Serviço Auxiliar")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_disj_tsa_falha_fechar, CONDIC_INDISPONIBILIZAR))

        cls.l_disj_tsa_falha_abrir = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["TSA_DISJUNTOR_FALHA_ABRIR"], descricao="[SA]  Falha Abertura Disjuntor Serviço Auxiliar")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_disj_tsa_falha_abrir, CONDIC_INDISPONIBILIZAR))

        cls.l_bloq_50bf_atuado = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["BLOQUEIO_50BF_ATUADO"], descricao="[SA]  Bloqueio 50BF Relé SA Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_bloq_50bf_atuado, CONDIC_INDISPONIBILIZAR))

        cls.l_bloq_86btlsa_atuado = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["BLOQUEIO_86BTLSA_ATUADO"], descricao="[SA]  Bloqueio 86BTLSA Relé SA Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_bloq_86btlsa_atuado, CONDIC_INDISPONIBILIZAR))


        ## WHATSAPP/VOIP
        cls.l_dps_gmg_falha = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["DPS_GMG"], descricao="[SA]  Falha Grupo Motor Gerador")
        cls.l_disj_gmg_trip = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["DISJUNTOR_GMG_TRIP"], descricao="[SA]  Trip Disjuntor Grupo Motor Gerador")
        cls.l_carreg_baterias_falha = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["CARREGADOR_BATERIAS_FALHA"], descricao="[SA]  Falha Carregador de Baterias")
        cls.l_disj_gmg_falha_fechar = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["GMG_DISJUNTOR_FALHA_FECHAR"], descricao="[SA]  Falha Fechamento Disjuntor Grupo Motor Gerador")
        cls.l_disjs_modo_remoto = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["DISJUNTORES_MODO_REMOTO"], descricao="[SA]  Disjuntores em Modo Remoto")

        cls.l_sfa_press_lado_sujo_alto = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["PSA_SFA_PRESSAO_LADO_SUJO_ALTO"], descricao="[SA]  Pressão Sistema de Filtragem A Lado Sujo Alta")
        cls.l_sfa_press_lado_limpo_alto = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"], descricao="[SA]  Pressão Sistema de Filtragem A Lado Limpo Alta")
        cls.l_sfa_press_lado_sujo_muito_alto = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"], descricao="[SA]  Pressão Sistema de Filtragem A Lado Sujo Muito Alta")
        cls.l_sfa_press_lado_limpo_muito_alto = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"], descricao="[SA]  Pressão Sistema de Filtragem A Lado Limpo Muito Alta")

        cls.l_sfb_press_lado_sujo_alto = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["PSA_SFB_PRESSAO_LADO_SUJO_ALTO"], descricao="[SA]  Pressão Sistema de Filtragem B Lado Sujo Alta")
        cls.l_sfb_press_lado_limpo_alto = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"], descricao="[SA]  Pressão Sistema de Filtragem B Lado Limpo Alta")
        cls.l_sfb_press_lado_sujo_muito_alto = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO"], descricao="[SA]  Pressão Sistema de Filtragem B Lado Sujo Muito Alta")
        cls.l_sfb_press_lado_limpo_muito_alto = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"], descricao="[SA]  Pressão Sistema de Filtragem B Lado Limpo Muito Alta")

        cls.l_sup_tensao_falha = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SUPERVISOR_TENSAO_FALHA"], descricao="[SA]  Falha Tensão pelo Supervisório")
        cls.l_sup_tensao_tsa_falha = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SUPERVISOR_TENSAO_TSA_FALHA"], descricao="[SA]  Falha Tensão Serviço Auxiliar pelo Supervisório")
        cls.l_sup_tensao_gmg_falha = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SUPERVISOR_TENSAO_GMG_FALHA"], descricao="[SA]  Falha Tensão Grupo Motor Gerador pelo Supervisório")

        cls.l_poco_dren_nv_alto = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["POCO_DRENAGEM_SENSOR_NIVEL_MUITO_ALTO"], descricao="[SA]  Poço de Drenagem Nível Alto")
        cls.l_dren_boias_discrepancia = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["DRENAGEM_BOIAS_DISCREPANCIA"], descricao="[SA]  Dicrepância Boias de Drenagem")
        cls.l_poco_dren_nv_muito_baixo = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["POCO_DRENAGEM_SENSOR_NIVEL_MUITO_BAIXO"], descricao="[SA]  Poço de Drenagem Nível Muito Baixo")

        cls.l_dren_bomba_1_indisp = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["DRENAGEM_BOMBA_1_INDISPONIVEL"], descricao="[SA]  Bomba de Drenagem 1 Indisponível")
        cls.l_dren_bomba_2_indisp = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["DRENAGEM_BOMBA_2_INDISPONIVEL"], descricao="[SA]  Bomba de Drenagem 2 Indisponível")
        cls.l_esgot_bomba_1_falha = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["ESGOTAMENTO_BOMBA_1_FALHA"], descricao="[SA]  Falha Bomba de Esgotamento 1")
        cls.l_esgot_bomba_2_falha = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["ESGOTAMENTO_BOMBA_2_FALHA"], descricao="[SA]  Falha Bomba de Esgotamento 2")
        cls.l_esgot_bomba_1_indisp = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["ESGOTAMENTO_BOMBA_1_INDISPONIVEL"], descricao="[SA]  Bomba de Esgotamento 1 Indisponível")
        cls.l_esgot_bomba_2_indisp = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["ESGOTAMENTO_BOMBA_2_INDISPONIVEL"], descricao="[SA]  Bomba de Esgotamento 2 Indisponível")
        cls.l_poco_dren_bomba_1_defeito = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["POCO_DRENAGEM_BOMBA_1_DEFEITO"], descricao="[SA]  Defeito Bomba 1 Poço de Drenagem")
        cls.l_poco_dren_bomba_2_defeito = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["POCO_DRENAGEM_BOMBA_2_DEFEITO"], descricao="[SA]  Defeito Bomba 2 Poço de Drenagem")

        cls.l_sfa_limp_elem_1_aberta = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_LIMPEZA_ELEMENTO_1_ABERTA"], descricao="[SA]  Sistema de Filtragem A Elemento 1 Aberto")
        cls.l_sfa_limp_elem_2_aberta = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_LIMPEZA_ELEMENTO_2_ABERTA"], descricao="[SA]  Sistema de Filtragem A Elemento 2 Aberto")
        cls.l_sfa_entra_elem_1_aberta = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_ENTRADA_ELEMENTO_1_ABERTA"], descricao="[SA]  Sistema de Filtragem A Entrada Elemento 1 Aberto")
        cls.l_sfa_entra_elem_2_aberta = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_ENTRADA_ELEMENTO_2_ABERTA"], descricao="[SA]  Sistema de Filtragem A Entrada Elemento 2 Aberto")
        cls.l_sfa_falha_abrir_limpeza_elem_1 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_ELEMENTO_1_FALHA_ABRIR_LIMPEZA"], descricao="[SA]  Falha Abrir Limpeza do Elemento 1 do Sistema de Filtragem A")
        cls.l_sfa_falha_fechar_limpeza_elem_1 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_ELEMENTO_1_FALHA_FECHAR_LIMPEZA"], descricao="[SA]  Falha Fechar limpeza do Elemento 1 do Sistema de Filtragem A")
        cls.l_sfa_falha_abrir_entra_elem_1 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_ELEMENTO_1_FALHA_ABRIR_ENTRADA"], descricao="[SA]  Falha Abrir Entrada Elemento 1 do Sistema de Filtragem A")
        cls.l_sfa_falha_fechar_entra_elem_1 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_ELEMENTO_1_FALHA_FECHAR_ENTRADA"], descricao="[SA]  Falha Fechar Entrada Elemento 1 do Sistema de Filtragem A")
        cls.l_sfa_falha_abrir_limpeza_elem_2 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_ELEMENTO_2_FALHA_ABRIR_LIMPEZA"], descricao="[SA]  Falha Abrir Limpeza do Elemento 2 do Sistema de Filtragem A")
        cls.l_sfa_falha_fechar_limpeza_elem_2 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_ELEMENTO_2_FALHA_FECHAR_LIMPEZA"], descricao="[SA]  Falha Fechar limpeza do Elemento 2 do Sistema de Filtragem A")
        cls.l_sfa_falha_abrir_entra_elem_2 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_ELEMENTO_2_FALHA_ABRIR_ENTRADA"], descricao="[SA]  Falha Abrir Entrada Elemento 2 do Sistema de Filtragem A")
        cls.l_sfa_falha_fechar_entra_elem_2 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_ELEMENTO_2_FALHA_FECHAR_ENTRADA"], descricao="[SA]  Falha Fechar Entrada Elemento 2 do Sistema de Filtragem A")

        cls.l_sfb_limp_elem_1_aberta = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_LIMPEZA_ELEMENTO_1_ABERTA"], descricao="[SA]  Sistema de Filtragem B Elemento 1 Aberto")
        cls.l_sfb_limp_elem_2_aberta = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_LIMPEZA_ELEMENTO_2_ABERTA"], descricao="[SA]  Sistema de Filtragem B Elemento 2 Aberto")
        cls.l_sfb_entra_elem_1_aberta = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_ENTRADA_ELEMENTO_1_ABERTA"], descricao="[SA]  Sistema de Filtragem B Entrada Elemento 1 Aberto")
        cls.l_sfb_entra_elem_2_aberta = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_ENTRADA_ELEMENTO_2_ABERTA"], descricao="[SA]  Sistema de Filtragem B Entrada Elemento 2 Aberto")
        cls.l_sfb_falha_abrir_limpeza_elem_1 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_ELEMENTO_1_FALHA_ABRIR_LIMPEZA"], descricao="[SA]  Falha Abrir Limpeza do Elemento 1 do Sistema de Filtragem B")
        cls.l_sfb_falha_fechar_limpeza_elem_1 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_ELEMENTO_1_FALHA_FECHAR_LIMPEZA"], descricao="[SA]  Falha Fechar limpeza do Elemento 1 do Sistema de Filtragem B")
        cls.l_sfb_falha_abrir_entra_elem_1 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_ELEMENTO_1_FALHA_ABRIR_ENTRADA"], descricao="[SA]  Falha Abrir Entrada Elemento 1 do Sistema de Filtragem B")
        cls.l_sfb_falha_fechar_entra_elem_1 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_ELEMENTO_1_FALHA_FECHAR_ENTRADA"], descricao="[SA]  Falha Fechar Entrada Elemento 1 do Sistema de Filtragem B")
        cls.l_sfb_falha_abrir_limpeza_elem_2 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_ELEMENTO_2_FALHA_ABRIR_LIMPEZA"], descricao="[SA]  Falha Abrir Limpeza do Elemento 2 do Sistema de Filtragem B")
        cls.l_sfb_falha_fechar_limpeza_elem_2 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_ELEMENTO_2_FALHA_FECHAR_LIMPEZA"], descricao="[SA]  Falha Fechar limpeza do Elemento 2 do Sistema de Filtragem B")
        cls.l_sfb_falha_abrir_entra_elem_2 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_ELEMENTO_2_FALHA_ABRIR_ENTRADA"], descricao="[SA]  Falha Abrir Entrada Elemento 2 do Sistema de Filtragem B")
        cls.l_sfb_falha_fechar_entra_elem_2 = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_ELEMENTO_2_FALHA_FECHAR_ENTRADA"], descricao="[SA]  Falha Fechar Entrada Elemento 2 do Sistema de Filtragem B")

        cls.l_nv_jusante_alto = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["PSA_NIVEL_JUSANTE_ALTO"], descricao="[SA]  Nível Jusante Alto")
        cls.l_nv_jusante_muito_baixo = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["NIVEL_JUSANTE_MUITO_BAIXO"], descricao="[SA]  Nível Jusante Muito Baixo")
        cls.l_nv_jusante_falha_leitura = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["NIVEL_JUSANTE_FALHA_LEITURA"], descricao="[SA]  Falha Leitura Nível Jusante")

        cls.l_sfa_press_lado_sujo_falha_leitura = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_PRESSAO_LADO_SUJO_FALHA_LEITURA"], descricao="[SA]  Falha Leitura Pressão Sistema de Filtragem A Lado Sujo")
        cls.l_sfa_press_lado_limpo_falha_leitura = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_PRESSAO_LADO_LIMPO_FALHA_LEITURA"], descricao="[SA]  Falha Leitura Pressão Sistema de Filtragem A Lado Limpo")

        cls.l_sfb_press_lado_sujo_falha_leitura = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_PRESSAO_LADO_SUJO_FALHA_LEITURA"], descricao="[SA]  Falha Leitura Pressão Sistema de Filtragem B Lado Sujo")
        cls.l_sfb_press_lado_limpo_falha_leitura = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_PRESSAO_LADO_LIMPO_FALHA_LEITURA"], descricao="[SA]  Falha Leitura Pressão Sistema de Filtragem B Lado Limpo")

        cls.l_sfa_press_lado_sujo_baixo = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_PRESSAO_LADO_SUJO_BAIXO"], descricao="[SA]  Pressão Sistema de Filtragem A Lado Sujo Baixo")
        cls.l_sfa_press_lado_limpo_baixo = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_PRESSAO_LADO_LIMPO_BAIXO"], descricao="[SA]  Pressão Sistema de Filtragem A Lado Limpo Baixo")
        cls.l_sfa_press_lado_sujo_muito_baixo = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_PRESSAO_LADO_SUJO_MUITO_BAIXO"], descricao="[SA]  Pressão Sistema de Filtragem A Lado Sujo Muito Baixo")
        cls.l_sfa_press_lado_limpo_muito_baixo = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFA_PRESSAO_LADO_LIMPO_MUITO_BAIXO"], descricao="[SA]  Pressão Sistema de Filtragem A Lado Limpo Muito Baixo")

        cls.l_sfb_press_lado_sujo_baixo = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_PRESSAO_LADO_SUJO_BAIXO"], descricao="[SA]  Pressão Sistema de Filtragem A Lado Sujo Baixo")
        cls.l_sfb_press_lado_limpo_baixo = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_PRESSAO_LADO_LIMPO_BAIXO"], descricao="[SA]  Pressão Sistema de Filtragem A Lado Limpo Baixo")
        cls.l_sfb_press_lado_sujo_muito_baixo = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_PRESSAO_LADO_SUJO_MUITO_BAIXO"], descricao="[SA]  Pressão Sistema de Filtragem A Lado Sujo Muito Baixo")
        cls.l_sfb_press_lado_limpo_muito_baixo = lei.LeituraModbusBit(serv.Servidores.clp["SA"], REG_SASE["SFB_PRESSAO_LADO_LIMPO_MUITO_BAIXO"], descricao="[SA]  Pressão Sistema de Filtragem A Lado Limpo Muito Baixo")