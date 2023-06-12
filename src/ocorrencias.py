import logging
import traceback

import src.dicionarios.dict as d

from src.funcoes.leitura import *
from src.condicionadores import *
from src.dicionarios.reg import *
from src.dicionarios.const import *

from src.unidade_geracao import UnidadeDeGeracao

logger = logging.getLogger("__main__")

class OcorrenciasUsn:
    def __init__(self, clp: "dict[str, ModbusClient]"=None) -> None:

        self._condicionadores: "list[CondicionadorBase]" = []
        self._condicionadores_essenciais: "list[CondicionadorBase]" = []

        self.__clp = clp
        self.flag: int = CONDIC_IGNORAR

        self.carregar_leituras()

    @property
    def condicionadores(self) -> "list[CondicionadorBase]":
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[CondicionadorBase]") -> None:
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[CondicionadorBase]":
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[CondicionadorBase]") -> None:
        self._condicionadores_essenciais = var

    def verificar_condicionadores(self) -> int:
        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condicionadores_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            self.flag = [CONDIC_NORMALIZAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_NORMALIZAR]
            self.flag = [CONDIC_INDISPONIBILIZAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_INDISPONIBILIZAR]

            logger.warning(f"[OCO-USN] Foram detectados condicionadores ativos na Usina:")
            [logger.warning(f"[OCO-USN] Descrição: \"{condic.descr}\", Gravidade: {CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}") for condic in condicionadores_ativos]

        return self.flag

    def leitura_temporizada(self) -> None:

        # WHATSAPP
        if self.leitura_ED_sup_tensao_falha.valor:
            logger.warning("[OCO-USN] Houve uma falha com a leitura de tensão supervisor, favor verificar.")

        if self.leitura_ED_sup_tensao_tsa_falha.valor:
            logger.warning("[OCO-USN] Houve uma falha com a leitura de tensão do Serviço Auxiliar, favor verificar.")

        if self.leitura_ED_sup_tensao_gmg_falha.valor:
            logger.warning("[OCO-USN] Houve uma falha com a leitura de tensão do Grupo Motor Gerador, favor verificar.")

        if self.leitura_EA_nv_montante_muito_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que o Nível Montante está muito baixo, favor verificar.")

        if self.leitura_ED_disj_gmg_fechado.valor:
            logger.warning("[OCO-USN] Foi identificado que o Disjuntor do Grupo Motor Gerador, favor verificar.")

        if self.leitura_ED_disjs_modo_remoto.valor:
            logger.warning("[OCO-USN] Foi identificado que os Disjuntores entraram em modo remoto, favor verificar.")

        if self.leitura_ED_poco_dren_nv_alto.valor:
            logger.warning("[OCO-USN] O nível do Poço de Drenagem está alto, favor verificar.")

        if self.leitura_ED_dren_boias_discrepancia.valor:
            logger.warning("[OCO-USN] Foi identificada uma discrepância nas Boias de Drenagem, favor verificar.")

        if self.leitura_ED_poco_dren_nv_muito_baixo.valor:
            logger.warning("[OCO-USN] O nível do Poço de Drenagem está muito baixo, favor verificar.")

        if self.leitura_ED_dren_bomba_1_indisp.valor:
            logger.warning("[OCO-USN] A Bomba de Drenagem 1 entrou em modo indisponível, favor verificar.")

        if self.leitura_ED_dren_bomba_2_indisp.valor:
            logger.warning("[OCO-USN] A Bomba de Drenagem 2 entrou em modo indisponível, favor verificar.")

        if self.leitura_ED_esgot_bomba_1_falha.valor:
            logger.warning("[OCO-USN] A Bomba de Esgotamento 1 entrou em modo indisponível, favor verificar.")

        if self.leitura_ED_esgot_bomba_2_falha.valor:
            logger.warning("[OCO-USN] A Bomba de Esgotamento 2 entrou em modo indisponível, favor verificar.")

        if self.leitura_ED_esgot_bomba_1_indisp.valor:
            logger.warning("[OCO-USN] A Bomba de Esgotamento 1 entrou em modo indisponível, favor verificar.")

        if self.leitura_ED_esgot_bomba_2_indisp.valor:
            logger.warning("[OCO-USN] A Bomba de Esgotamento 2 entrou em modo indisponível, favor verificar.")

        if self.leitura_ED_poco_dren_bomba_1_defeito.valor:
            logger.warning("[OCO-USN] Foi dentificado um defeito na Bomba de Drenagem 1, favor verificar.")

        if self.leitura_ED_poco_dren_bomba_2_defeito.valor:
            logger.warning("[OCO-USN] Foi dentificado um defeito na Bomba de Drenagem 2, favor verificar.")

        if self.leitura_ED_poco_esgot_bomba_1_defeito.valor:
            logger.warning("[OCO-USN] Foi dentificado um defeito na Bomba de Esgotamento 1, favor verificar.")

        if self.leitura_ED_poco_esgot_bomba_2_defeito.valor:
            logger.warning("[OCO-USN] Foi dentificado um defeito na Bomba de Esgotamento 2, favor verificar.")

        if self.leitura_ED_sfa_limp_elem_1_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que o Elemento de Limpeza 1 do Sistema de Filtragem A foi aberto, favor verificar.")

        if self.leitura_ED_sfa_limp_elem_2_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que o Elemento de Limpeza 2 do Sistema de Filtragem A foi aberto, favor verificar.")

        if self.leitura_ED_sfa_entra_elem_1_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que a Entrada do Elemento 1 do Sistema de Filtragem A foi aberto, favor verificar.")

        if self.leitura_ED_sfa_entra_elem_2_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que a Entrada do Elemento 2 do Sistema de Filtragem A foi aberto, favor verificar.")

        if self.leitura_ED_sfa_falha_abrir_retrolavagem.valor:
            logger.warning("[OCO-USN] Houve uma falha ao abrir a Retrolavagem do Sistema de Filtragem A, favor verificar.")

        if self.leitura_ED_sfa_falha_fechar_retrolavagem.valor:
            logger.warning("[OCO-USN] Houve uma falha ao fechar a Retrolavagem do Sistema de Filtragem A, favor verificar.")

        if self.leitura_ED_sfa_falha_abrir_entra_elem.valor:
            logger.warning("[OCO-USN] Houve uma falha ao abrir a Entrada do Elemento do Sistema de Filtragem A, favor verificar.")

        if self.leitura_ED_sfa_falha_fechar_entra_elem.valor:
            logger.warning("[OCO-USN] Houve uma falha ao fechar a Entrada do Elemento do Sistema de Filtragem A, favor verificar.")

        if self.leitura_ED_sfb_limp_elem_1_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que o Elemento de Limpeza 1 do Sistema de Filtragem B foi aberto, favor verificar.")

        if self.leitura_ED_sfb_limp_elem_2_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que o Elemento de Limpeza 2 do Sistema de Filtragem B foi aberto, favor verificar.")

        if self.leitura_ED_sfb_entra_elem_1_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que a Entrada do Elemento 1 do Sistema de Filtragem B foi aberto, favor verificar.")

        if self.leitura_ED_sfb_entra_elem_2_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que a Entrada do Elemento 2 do Sistema de Filtragem B foi aberto, favor verificar.")

        if self.leitura_ED_sfb_falha_abrir_entra_elem.valor:
            logger.warning("[OCO-USN] Houve uma falha ao abrir a Entrada do Elemento do Sistema de Filtragem B, favor verificar.")

        if self.leitura_ED_sfb_falha_fechar_entra_elem.valor:
            logger.warning("[OCO-USN] Houve uma falha ao fechar a Entrada do Elemento do Sistema de Filtragem A, favor verificar.")

        if self.leitura_ED_sfb_falha_abrir_retrolavagem.valor:
            logger.warning("[OCO-USN] Houve uma falha ao abrir a Retrolavagem do Sistema de Filtragem B, favor verificar.")

        if self.leitura_ED_sfb_falha_fechar_retrolavagem.valor:
            logger.warning("[OCO-USN] Houve uma falha ao fechar a Retrolavagem do Sistema de Filtragem B, favor verificar.")

        if self.leitura_EA_nv_montante_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que o Nível Montante está baixo, favor verificar.")

        if self.leitura_EA_nv_jusante_alto.valor:
            logger.warning("[OCO-USN] Foi identificado que o Nível Jusante está alto, favor verificar.")

        if self.leitura_EA_nv_jusante_muito_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que o Nível Jusante está muito baixo, favor verificar.")

        if self.leitura_EA_nv_jusante_2_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que o Nível Jusante 2 está baixo, favor verificar.")

        if self.leitura_EA_nv_jusante_2_muito_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que o Nível Jusante 2 está muito baixo, favor verificar.")

        if self.leitura_EA_nv_jusante_falha_leitura.valor:
            logger.warning("[OCO-USN] Houve uma falha na leitura de Nível Jusante, favor verificar.")

        if self.leitura_EA_nv_jusante_2_falha_leitura.valor:
            logger.warning("[OCO-USN] Houve uma falha na leitura de Nível Jusante 2, favor verificar.")

        if self.leitura_EA_sfa_press_lado_sujo_falha_leitura.valor:
            logger.warning("[OCO-USN] Houve uma falha de leitura no lado sujo do Sistema de Filtragem A, favor verificar.")

        if self.leitura_EA_sfa_press_lado_limpo_falha_leitura.valor:
            logger.warning("[OCO-USN] Houve uma falha de leitura no lado limpo do Sistema de Filtragem A, favor verificar.")

        if self.leitura_EA_sfb_press_lado_sujo_falha_leitura.valor:
            logger.warning("[OCO-USN] Houve uma falha de leitura no lado sujo do Sistema de Filtragem B, favor verificar.")

        if self.leitura_EA_sfb_press_lado_limpo_falha_leitura.valor:
            logger.warning("[OCO-USN] Houve uma falha de leitura no lado limpo do Sistema de Filtragem B, favor verificar.")

        if self.leitura_EA_sfa_press_lado_sujo_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado sujo do Sistema de Filtragem A está baixa, favor verificar.")

        if self.leitura_EA_sfa_press_lado_limpo_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado limpo do Sistema de Filtragem A está baixa, favor verificar.")

        if self.leitura_EA_sfa_press_lado_sujo_muito_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado sujo do Sistema de Filtragem A está muito baixa, favor verificar.")

        if self.leitura_EA_sfa_press_lado_limpo_muito_baixo.valor:
            logger.warning("[OCO-USN] ,Foi identificado que a pressão do lado limpo do Sistema de Filtragem A está muito baixa favor verificar.")

        if self.leitura_EA_sfb_press_lado_sujo_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado sujo do Sistema de Filtragem B está baixa, favor verificar.")

        if self.leitura_EA_sfb_press_lado_limpo_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado limpo do Sistema de Filtragem B está baixa, favor verificar.")

        if self.leitura_EA_sfb_press_lado_sujo_muito_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado sujo do Sistema de Filtragem B está muito baixa, favor verificar.")

        if self.leitura_EA_sfb_press_lado_limpo_muito_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado limpo do Sistema de Filtragem B está muito baixa, favor verificar.")



        # wHATSAPP + VOIP
        if self.leitura_ED_disj_gmg_trip.valor and not d.voip["SA_ED_PSA_DISJ_GMG_TRIP"]:
            logger.warning("[OCO-USN] Foi identificado um sinal de Trip do Grupo Motor Gerador, favor verificar.")
            d.voip["SA_ED_PSA_DISJ_GMG_TRIP"] = True
        elif not self.leitura_ED_disj_gmg_trip.valor and d.voip["SA_ED_PSA_DISJ_GMG_TRIP"]:
            d.voip["SA_ED_PSA_DISJ_GMG_TRIP"] = False

        if self.leitura_ED_dps_gmg_falha.valor and not d.voip["SA_ED_PSA_DPS_GMG"]:
            logger.warning("[OCO-USN] Houve uma falha com o Grupo Motor Gerador, favor verificar.")
            d.voip["SA_ED_PSA_DPS_GMG"] = True
        elif not self.leitura_ED_dps_gmg_falha.valor and d.voip["SA_ED_PSA_DPS_GMG"]:
            d.voip["SA_ED_PSA_DPS_GMG"] = False

        if self.leitura_ED_conv_fibra_falha.valor and not d.voip["SA_ED_PSA_CONVERSOR_FIBRA_FALHA"]:
            logger.warning("[OCO-USN] Houve uma falha com o Conversor de Fibra, favor verificar.")
            d.voip["SA_ED_PSA_CONVERSOR_FIBRA_FALHA"] = True
        elif not self.leitura_ED_conv_fibra_falha.valor and d.voip["SA_ED_PSA_CONVERSOR_FIBRA_FALHA"]:
            d.voip["SA_ED_PSA_CONVERSOR_FIBRA_FALHA"] = False

        if self.leitura_ED_carreg_baterias_falha.valor and not d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"]:
            logger.warning("[OCO-USN] Houve uma falha com o Carregador de Baterias, favor verificar.")
            d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"] = True
        elif not self.leitura_ED_carreg_baterias_falha.valor and d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"]:
            d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"] = False

        if self.leitura_EA_nv_montante_muito_baixo.valor and not d.voip["SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO"]:
            logger.warning("[OCO-USN] Foi identificado que o Nível Montante está Muito Baixo, favor verificar.")
            d.voip["SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO"] = True
        elif not self.leitura_EA_nv_montante_muito_baixo.valor and d.voip["SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO"]:
            d.voip["SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO"] = False

        if self.leitura_EA_sfa_press_lado_sujo_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado sujo do Sistema de Filtragem A está alto, favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"] = True
        elif not self.leitura_EA_sfa_press_lado_sujo_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"] = False

        if self.leitura_EA_sfa_press_lado_limpo_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado limpo do Sistema de Filtragem A está alto, favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"] = True
        elif not self.leitura_EA_sfa_press_lado_limpo_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"] = False

        if self.leitura_EA_sfa_press_lado_sujo_muito_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado sujo do Sistema de Filtragem A está muito alto, favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"] = True
        elif not self.leitura_EA_sfa_press_lado_sujo_muito_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"] = False

        if self.leitura_EA_sfa_press_lado_limpo_muito_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado limpo do Sistema de Filtragem A está muito alto, favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"] = True
        elif not self.leitura_EA_sfa_press_lado_limpo_muito_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"] = False

        if self.leitura_EA_sfb_press_lado_sujo_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado sujo do Sistema de Filtragem B está alto, favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"] = True
        elif not self.leitura_EA_sfb_press_lado_sujo_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"] = False

        if self.leitura_EA_sfb_press_lado_limpo_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado limpo do Sistema de Filtragem B está alto, favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"] = True
        elif not self.leitura_EA_sfb_press_lado_limpo_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"] = False

        if self.leitura_EA_sfb_press_lado_sujo_muito_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado sujo do Sistema de Filtragem B está muito alto, favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"] = True
        elif not self.leitura_EA_sfb_press_lado_sujo_muito_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"] = False

        if self.leitura_EA_sfb_press_lado_limpo_muito_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado limpo do Sistema de Filtragem B está muito alto, favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"] = True
        elif not self.leitura_EA_sfb_press_lado_limpo_muito_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"] = False

        return

    def carregar_leituras(self) -> None:
        ### Leituras para acionamento temporizado por chamada Voip
        ## CONDICIONADORES ESSENCIAIS
        # ENTRADAS DIGITAIS
        # Diversos
        leitura_ED_prtva1_50bf = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_PRTVA1_50BF"], descr="[OCO-USN] Bloqueio Relé 50BF PRTVA 1")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_prtva1_50bf, CONDIC_INDISPONIBILIZAR))

        leitura_ED_prtva2_50bf = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_PRTVA2_50BF"], descr="[OCO-USN] Bloqueio Relé 50BF PRTVA 2")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_prtva2_50bf, CONDIC_INDISPONIBILIZAR))

        leitura_ED_disj_linha_aberto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SE_DISJ_LINHA_ABERTO"], descr="[OCO-USN] Disjuntor de Linha Aberto")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_linha_aberto, CONDIC_NORMALIZAR))

        # Trip
        leitura_ED_disj_tsa_trip = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_DISJ_TSA_TRIP"], descr="[OCO-USN] Trip Disjuntor Serviço Auxiliar")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_tsa_trip, CONDIC_INDISPONIBILIZAR))

        leitura_ED_rele_linha_trip = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SE_RELE_LINHA_TRIP"], descr="[OCO-USN] Trip Relé de Linha")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_rele_linha_trip, CONDIC_NORMALIZAR))

        # Temperatura, Nível e Pressão
        leitura_ED_te_temp_muito_alta = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_TE_TEMPERATURA_MUIT_ALTA"], descr="[OCO-USN] Trasformador Elevador Temperatura Alta")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_te_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        leitura_ED_te_eleva_temp_muito_alta = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_TRAFO_ELEVADOR_TEMP_MUITO_ALTA"], descr="[OCO-USN] Trasformador Elevador Temperatura Muito Alta")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_te_eleva_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        leitura_ED_te_press_muito_alta = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_TE_PRESSAO_MUITO_ALTA"], descr="[OCO-USN] Trasformador Elevador Pressão Muito Alta")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_te_press_muito_alta, CONDIC_INDISPONIBILIZAR))

        leitura_ED_oleo_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_OLEO_MUITO_BAIXO"], descr="[OCO-USN] Trasformador Elevador Óleo Muito Baixo")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_oleo_muito_baixo, CONDIC_INDISPONIBILIZAR))

        leitura_ED_poco_dren_nivel_muito_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_ALTO"], descr="[OCO-USN] Poço de Drenagem Nível Muito Alto")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_poco_dren_nivel_muito_alto, CONDIC_INDISPONIBILIZAR))

        leitura_ED_nv_jusante_muito_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_NIVEL_JUSANTE_MUITO_ALTO"], descr="[OCO-USN] Nível Jusante Muito Alto")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_nv_jusante_muito_alto, CONDIC_INDISPONIBILIZAR))

        # Falhas
        leitura_ED_dps_tsa = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_DPS_TSA"], descr="[OCO-USN] Falha Disjuntor Serviço Auxiliar")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_dps_tsa, CONDIC_INDISPONIBILIZAR))

        leitura_ED_disj_gmg_falha_abrir = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_GMG_DISJ_FALHA_ABRIR"], descr="[OCO-USN] Falha Abertura Disjuntor Grupo Motor Gerador")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_gmg_falha_abrir, CONDIC_INDISPONIBILIZAR))

        leitura_ED_disj_tsa_falha_fechar = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_TSA_DISJ_FALHA_FECHAR"], descr="[OCO-USN] Falha Fechamento Disjuntor Serviço Auxiliar")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_tsa_falha_fechar, CONDIC_INDISPONIBILIZAR))

        leitura_ED_disj_tsa_falha_abrir = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_TSA_DISJ_FALHA_ABRIR"], descr="[OCO-USN] Falha Abertura Disjuntor Serviço Auxiliar")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_tsa_falha_abrir, CONDIC_INDISPONIBILIZAR))

        leitura_ED_disj_se_falha_fechar = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SE_DISJ_FALHA_FECHAR"], descr="[OCO-USN] Falha Fechamento Disjuntor de Linha")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_se_falha_fechar, CONDIC_INDISPONIBILIZAR))

        leitura_ED_disj_se_falha_abrir = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SE_DISJ_FALHA_ABRIR"], descr="[OCO-USN] Falha Abertura Disjuntor de Linha")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_se_falha_abrir, CONDIC_INDISPONIBILIZAR))

        leitura_ED_se_rele_linha_falha = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SE_RELE_LINHA_FALHA"], descr="[OCO-USN] Falha Relé de Linha")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_se_rele_linha_falha, CONDIC_INDISPONIBILIZAR))

        # Bloqueios
        leitura_ED_bloq_stt_50bf = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_STT_BLOQUEIO_50BF"], descr="[OCO-USN] Status Bloqueio 50BF Relé SA")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_bloq_stt_50bf, CONDIC_INDISPONIBILIZAR))

        leitura_ED_bloq_50bf_atuado = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_BLOQUEIO_50BF_ATUADO"], descr="[OCO-USN] Bloqueio 50BF Relé SA Atuado")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_bloq_50bf_atuado, CONDIC_INDISPONIBILIZAR))

        leitura_ED_bloq_stt_86btlsa = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_STT_BLOQUEIO_86BTLSA"], descr="[OCO-USN] Status Bloqueio 86BTLSA Relé SA")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_bloq_stt_86btlsa, CONDIC_INDISPONIBILIZAR))

        leitura_ED_bloq_86btlsa_atuado = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_BLOQUEIO_86BTLSA_ATUADO"], descr="[OCO-USN] Bloqueio 86BTLSA Relé SA Atuado")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_bloq_86btlsa_atuado, CONDIC_INDISPONIBILIZAR))

        leitura_ED_bloq_rele_86btbf = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_RELE_BLOQUEIO_86BTBF"], descr="[OCO-USN] Bloqueio 86BTBF Relé SA")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_bloq_rele_86btbf, CONDIC_INDISPONIBILIZAR))

        leitura_ED_bloq_botao_86btbf = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_BOTAO_BLOQUEIO_86BTBF"], descr="[OCO-USN] Botão Bloqueio 86BTBF Relé SA pressionado")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_bloq_botao_86btbf, CONDIC_INDISPONIBILIZAR))

        leitura_ED_se_rele_linha_50bf = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SE_RELE_LINHA_50BF"], descr="[OCO-USN] Bloqueio 50BF Relé Linha")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_se_rele_linha_50bf, CONDIC_INDISPONIBILIZAR))



        ### OUTRAS LEITURAS
        ## WHATSAPP + VOIP
        # ENTRADAS DIGITAIS
        self.leitura_ED_dps_gmg_falha = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_DPS_GMG"], descr="[OCO-USN] Falha Grupo Motor Gerador")
        self.leitura_ED_disj_gmg_trip = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_DISJ_GMG_TRIP"], descr="[OCO-USN] Trip Disjuntor Grupo Motor Gerador")
        self.leitura_ED_conv_fibra_falha = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_CONVERSOR_FIBRA_FALHA"], descr="[OCO-USN] Falha Conversor de Fibra")
        self.leitura_ED_carreg_baterias_falha = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"], descr="[OCO-USN] Falha Carregador de Baterias")
        self.leitura_ED_disj_gmg_falha_fechar = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_GMG_DISJ_FALHA_FECHAR"], descr="[OCO-USN] Falha Fechamento Disjuntor Grupo Motor Gerador")

        # ENTRADAS ANALÓGICAS
        self.leitura_EA_nv_montante_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO"], descr="[OCO-USN] Nível Montante Muito Baixo")

        self.leitura_EA_sfa_press_lado_sujo_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Sujo Alta")
        self.leitura_EA_sfa_press_lado_limpo_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Limpo Alta")
        self.leitura_EA_sfa_press_lado_sujo_muito_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Sujo Muito Alta")
        self.leitura_EA_sfa_press_lado_limpo_muito_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Limpo Muito Alta")

        self.leitura_EA_sfb_press_lado_sujo_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem B Lado Sujo Alta")
        self.leitura_EA_sfb_press_lado_limpo_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem B Lado Limpo Alta")
        self.leitura_EA_sfb_press_lado_sujo_muito_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem B Lado Sujo Muito Alta")
        self.leitura_EA_sfb_press_lado_limpo_muito_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem B Lado Limpo Muito Alta")

        ## WHATSAPP
        # ENTRADAS DIGITAIS
        self.leitura_ED_sup_tensao_falha = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SUPERVISOR_TENSAO_FALHA"], descr="[OCO-USN] Falha Tensão pelo Supervisório")
        self.leitura_ED_sup_tensao_tsa_falha = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SUPERVISOR_TENSAO_TSA_FALHA"], descr="[OCO-USN] Falha Tensão Serviço Auxiliar pelo Supervisório")
        self.leitura_ED_sup_tensao_gmg_falha = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SUPERVISOR_TENSAO_GMG_FALHA"], descr="[OCO-USN] Falha Tensão Grupo Motor Gerador pelo Supervisório")

        self.leitura_ED_disj_gmg_fechado = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_DIJS_GMG_FECHADO"], descr="[OCO-USN] Disjuntor Grupo Motor Gerador Fechado")
        self.leitura_ED_disjs_modo_remoto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_DISJUNTORES_MODO_REMOTO"], descr="[OCO-USN] Disjuntores em Modo Remoto")

        self.leitura_ED_poco_dren_nv_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_ALTO"], descr="[OCO-USN] Poço de Drenagem Nível Alto")
        self.leitura_ED_dren_boias_discrepancia = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_DREANGEM_BOIAS_DISCREPANCIA"], descr="[OCO-USN] Dicrepância Boias de Drenagem")
        self.leitura_ED_poco_dren_nv_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_BAIXO"], descr="[OCO-USN] Poço de Drenagem Nível Muito Alto")

        self.leitura_ED_dren_bomba_1_indisp = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_DREANGEM_BOMBA_1_INDISP"], descr="[OCO-USN] Bomba de Drenagem 1 Indisponível")
        self.leitura_ED_dren_bomba_2_indisp = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_DREANGEM_BOMBA_2_INDISP"], descr="[OCO-USN] Bomba de Drenagem 2 Indisponível")
        self.leitura_ED_esgot_bomba_1_falha = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_ESGOTAMENTO_BOMBA_1_FALHA"], descr="[OCO-USN] Falha Bomba de Esgotamento 1")
        self.leitura_ED_esgot_bomba_2_falha = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_ESGOTAMENTO_BOMBA_2_FALHA"], descr="[OCO-USN] Falha Bomba de Esgotamento 2")
        self.leitura_ED_esgot_bomba_1_indisp = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_ESGOTAMENTO_BOMBA_1_INDISP"], descr="[OCO-USN] Bomba de Esgotamento 1 Indisponível")
        self.leitura_ED_esgot_bomba_2_indisp = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_ESGOTAMENTO_BOMBA_2_INDISP"], descr="[OCO-USN] Bomba de Esgotamento 2 Indisponível")
        self.leitura_ED_poco_dren_bomba_1_defeito = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_POCO_DRENAGEM_BOMBA_1_DEFEITO"], descr="[OCO-USN] Defeito Bomba 1 Poço de Drenagem")
        self.leitura_ED_poco_dren_bomba_2_defeito = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_POCO_DRENAGEM_BOMBA_2_DEFEITO"], descr="[OCO-USN] Defeito Bomba 2 Poço de Drenagem")
        self.leitura_ED_poco_esgot_bomba_1_defeito = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_POCO_ESGOTAMENTO_BOMBA_1_DEFEITO"], descr="[OCO-USN] Defeito Bomba 1 Poço de Esgotamento")
        self.leitura_ED_poco_esgot_bomba_2_defeito = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_POCO_ESGOTAMENTO_BOMBA_2_DEFEITO"], descr="[OCO-USN] Defeito Bomba 2 Poço de Esgotamento")

        self.leitura_ED_sfa_limp_elem_1_aberta = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFA_LIMPEZA_ELEMENTO_1_ABERTA"], descr="[OCO-USN] Sistema de Filtragem A Elemento 1 Aberto")
        self.leitura_ED_sfa_limp_elem_2_aberta = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFA_LIMPEZA_ELEMENTO_2_ABERTA"], descr="[OCO-USN] Sistema de Filtragem A Elemento 2 Aberto")
        self.leitura_ED_sfa_entra_elem_1_aberta = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFA_ENTRADA_ELEMENTO_1_ABERTA"], descr="[OCO-USN] Sistema de Filtragem A Entrada Elemento 1 Aberto")
        self.leitura_ED_sfa_entra_elem_2_aberta = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFA_ENTRADA_ELEMENTO_2_ABERTA"], descr="[OCO-USN] Sistema de Filtragem A Entrada Elemento 2 Aberto")
        self.leitura_ED_sfa_falha_abrir_retrolavagem = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFA_FALHA_ABRIR_RETROLAVAGEM"], descr="[OCO-USN] Falha Abrir Retrolavagem Sistema de Filtragem A")
        self.leitura_ED_sfa_falha_fechar_retrolavagem = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFA_FALHA_FECHAR_RETROLAVAGEM"], descr="[OCO-USN] Falha Fechar Retrolavagem Sistema de Filtragem A")
        self.leitura_ED_sfa_falha_abrir_entra_elem = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFA_FALHA_ABRIR_ENTRADA_ELEM"], descr="[OCO-USN] Falha Abrir Entrada Elemento Sistema de Filtragem A")
        self.leitura_ED_sfa_falha_fechar_entra_elem = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFA_FALHA_FECHAR_ENTRADA_ELEM"], descr="[OCO-USN] Falha Fechar Entrada Elemento Sistema de Filtragem A")

        self.leitura_ED_sfb_limp_elem_1_aberta = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFB_LIMPEZA_ELEMENTO_1_ABERTA"], descr="[OCO-USN] Sistema de Filtragem B Elemento 1 Aberto")
        self.leitura_ED_sfb_limp_elem_2_aberta = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFB_LIMPEZA_ELEMENTO_2_ABERTA"], descr="[OCO-USN] Sistema de Filtragem B Elemento 2 Aberto")
        self.leitura_ED_sfb_entra_elem_1_aberta = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFB_ENTRADA_ELEMENTO_1_ABERTA"], descr="[OCO-USN] Sistema de Filtragem B Entrada Elemento 1 Aberto")
        self.leitura_ED_sfb_entra_elem_2_aberta = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFB_ENTRADA_ELEMENTO_2_ABERTA"], descr="[OCO-USN] Sistema de Filtragem B Entrada Elemento 2 Aberto")
        self.leitura_ED_sfb_falha_abrir_entra_elem = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFB_FALHA_ABRIR_ENTRADA_ELEM"], descr="[OCO-USN] Falha Abrir Retrolavagem Sistema de Filtragem B")
        self.leitura_ED_sfb_falha_fechar_entra_elem = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFB_FALHA_FECHAR_ENTRADA_ELEM"], descr="[OCO-USN] Falha Fechar Retrolavagem Sistema de Filtragem B")
        self.leitura_ED_sfb_falha_abrir_retrolavagem = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFB_FALHA_ABRIR_RETROLAVAGEM"], descr="[OCO-USN] Falha Abrir Entrada Elemento Sistema de Filtragem B")
        self.leitura_ED_sfb_falha_fechar_retrolavagem = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_SFB_FALHA_FECHAR_RETROLAVAGEM"], descr="[OCO-USN] Falha Fechar Entrada Elemento Sistema de Filtragem B")

        # ENTRADAS ANALÓGICAS
        self.leitura_EA_nv_montante_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_NIVEL_MONTANTE_BAIXO"], descr="[OCO-USN] Nível Montante Baixo")
        self.leitura_EA_nv_jusante_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_NIVEL_JUSANTE_ALTO"], descr="[OCO-USN] Nível Jusante Alto")
        self.leitura_EA_nv_jusante_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_NIVEL_JUSANTE_MUITO_BAIXO"], descr="[OCO-USN] Nível Jusante Muito Baixo")
        self.leitura_EA_nv_jusante_2_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_NIVEL_JUSANTE_2_BAIXO"], descr="[OCO-USN] Nível Jusante 2 Baixo")
        self.leitura_EA_nv_jusante_2_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_NIVEL_JUSANTE_2_MUITO_BAIXO"], descr="[OCO-USN] Nível Jusante 2 Muito Baixo")
        self.leitura_EA_nv_jusante_falha_leitura = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_NIVEL_JUSANTE_FALHA_LEITURA"], descr="[OCO-USN] Falha Leitura Nível Jusante")
        self.leitura_EA_nv_jusante_2_falha_leitura = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_NIVEL_JUSANTE_2_FALHA_LEITURA"], descr="[OCO-USN] Falha Leitura Nível Jusante 2")

        self.leitura_EA_sfa_press_lado_sujo_falha_leitura = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_FALHA_LEITURA"], descr="[OCO-USN] Falha Leitura Pressão Sistema de Filtragem A Lado Sujo")
        self.leitura_EA_sfa_press_lado_limpo_falha_leitura = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_FALHA_LEITURA"], descr="[OCO-USN] Falha Leitura Pressão Sistema de Filtragem A Lado Limpo")

        self.leitura_EA_sfb_press_lado_sujo_falha_leitura = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_FALHA_LEITURA"], descr="[OCO-USN] Falha Leitura Pressão Sistema de Filtragem B Lado Sujo")
        self.leitura_EA_sfb_press_lado_limpo_falha_leitura = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_FALHA_LEITURA"], descr="[OCO-USN] Falha Leitura Pressão Sistema de Filtragem B Lado Limpo")

        self.leitura_EA_sfa_press_lado_sujo_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_BAIXO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Sujo Baixo")
        self.leitura_EA_sfa_press_lado_limpo_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_BAIXO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Limpo Baixo")
        self.leitura_EA_sfa_press_lado_sujo_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_BAIXO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Sujo Muito Baixo")
        self.leitura_EA_sfa_press_lado_limpo_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_BAIXO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Limpo Muito Baixo")

        self.leitura_EA_sfb_press_lado_sujo_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_BAIXO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Sujo Baixo")
        self.leitura_EA_sfb_press_lado_limpo_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_BAIXO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Limpo Baixo")
        self.leitura_EA_sfb_press_lado_sujo_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_BAIXO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Sujo Muito Baixo")
        self.leitura_EA_sfb_press_lado_limpo_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_BAIXO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Limpo Muito Baixo")


class OcorrenciasUg:
    def __init__(self, ug_id: int, clp: "dict[str, ModbusClient]"=None):

        self.__ug_id = ug_id
        self.__clp = clp

        self._temperatura_base: int = 100
        self._temperatura_limite: int = 200

        self._condicionadores: "list[CondicionadorBase]" = []
        self._condicionadores_essenciais: "list[CondicionadorBase]" = []

        self._leitura_dict: "dict[str, LeituraModbus]" = {}
        self._condic_dict: "dict[str, CondicionadorBase]" = {}

        self.flag: int = CONDIC_IGNORAR

        self.carregar_leituras()

    @property
    def temperatura_base(self) -> int:
        return self._temperatura_base

    @temperatura_base.setter
    def temperatura_base(self, var: int) -> None:
        self._temperatura_base = var

    @property
    def temperatura_limite(self) -> int:
        return self._temperatura_limite

    @temperatura_limite.setter
    def temperatura_limite(self, var: int) -> None:
        self._temperatura_limite = var

    @property
    def condic_dict(self) -> "dict[str, CondicionadorExponencial]":
        return self._condic_dict

    @condic_dict.setter
    def condic_dict(self, var: "dict[str, CondicionadorExponencial]") -> None:
        self._condic_dict = var

    @property
    def leitura_dict(self) -> "dict[str, LeituraModbus]":
        return self._leitura_dict

    @leitura_dict.setter
    def leitura_dict(self, var: "dict[str, LeituraModbus]") -> None:
        self._leitura_dict = var

    @property
    def condicionadores(self) -> "list[CondicionadorBase]":
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[CondicionadorBase]") -> None:
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[CondicionadorBase]":
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[CondicionadorBase]") -> None:
        self._condicionadores_essenciais = var

    def verificar_condicionadores(self) -> int:
        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condicionadores_ativos = [x for y in [self.condicionadores_essenciais, self.condicionadores] for x in y if x.ativo]

            self.flag = [CONDIC_NORMALIZAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_NORMALIZAR]
            self.flag = [CONDIC_AGUARDAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_AGUARDAR]
            self.flag = [CONDIC_INDISPONIBILIZAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_INDISPONIBILIZAR]

            logger.warning(f"[OCO-UG{self.__ug_id}] Foram detectados condicionadores ativos na UG:")
            [logger.warning(f"[OCO-UG{self.__ug_id}] Descrição: \"{condic.descr}\", Gravidade: {CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}") for condic in condicionadores_ativos]

        return self.flag

    def atualizar_limites_condicionadores(self, parametros) -> None:
        try:
            self.condic_dict[f"tmp_fase_r_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_fase_s_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_fase_t_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_nucleo_gerador_1_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_1_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_nucleo_gerador_2_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_2_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_nucleo_gerador_3_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_3_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_casq_rad_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_casq_rad_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_casq_comb_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_casq_comb_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_escora_comb_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_escora_comb_ug{self.__ug_id}"])

            self.condic_dict[f"tmp_fase_s_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_fase_r_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_fase_t_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_nucleo_gerador_1_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_1_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_nucleo_gerador_2_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_2_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_nucleo_gerador_3_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_3_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_casq_rad_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_casq_rad_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_casq_comb_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_casq_comb_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_escora_comb_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_escora_comb_ug{self.__ug_id}"])

        except Exception:
            logger.error(f"[OCO-UG{self.__ug_id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores.")
            logger.debug(f"[OCO-UG{self.__ug_id}] Traceback: {traceback.format_exc()}")

    def controle_limites_operacao(self) -> None:
        # TODO adicionar borda no caso de ter disparado a mensagem num tempo pre definido
        ld = self.leitura_dict
        cd = self.condic_dict

        if ld[f"tmp_fase_r_ug{self.__ug_id}"].valor >= cd[f"tmp_fase_r_ug{self.__ug_id}"].valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura de Fase R da UG passou do valor base! ({cd[f'tmp_fase_r_ug{self.__ug_id}'].valor_base} C) | Leitura: {ld[f'tmp_fase_r_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_fase_r_ug{self.__ug_id}"].valor >= 0.9*(cd[f"tmp_fase_r_ug{self.__ug_id}"].valor_limite - cd[f"tmp_fase_r_ug{self.__ug_id}"].valor_base) + cd[f"tmp_fase_r_ug{self.__ug_id}"].valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura de Fase R da UG está muito próxima do limite! ({cd[f'tmp_fase_r_ug{self.__ug_id}'].valor_limite} C) | Leitura: {ld[f'tmp_fase_r_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_fase_s_ug{self.__ug_id}"].valor >= cd[f"tmp_fase_s_ug{self.__ug_id}"].valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura de Fase S da UG passou do valor base! ({cd[f'tmp_fase_s_ug{self.__ug_id}'].valor_base} C) | Leitura: {ld[f'tmp_fase_s_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_fase_s_ug{self.__ug_id}"].valor >= 0.9*(cd[f"tmp_fase_s_ug{self.__ug_id}"].valor_limite - cd[f"tmp_fase_s_ug{self.__ug_id}"].valor_base) + cd[f"tmp_fase_s_ug{self.__ug_id}"].valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura de Fase S da UG está muito próxima do limite! ({cd[f'tmp_fase_s_ug{self.__ug_id}'].valor_limite} C) | Leitura: {ld[f'tmp_fase_s_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_fase_t_ug{self.__ug_id}"].valor >= cd[f"tmp_fase_t_ug{self.__ug_id}"].valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura de Fase T da UG passou do valor base! ({cd[f'tmp_fase_t_ug{self.__ug_id}'].valor_base} C) | Leitura: {ld[f'tmp_fase_t_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_fase_t_ug{self.__ug_id}"].valor >= 0.9*(cd[f"tmp_fase_t_ug{self.__ug_id}"].valor_limite - cd[f"tmp_fase_t_ug{self.__ug_id}"].valor_base) + cd[f"tmp_fase_t_ug{self.__ug_id}"].valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura de Fase T da UG está muito próxima do limite! ({cd[f'tmp_fase_t_ug{self.__ug_id}'].valor_limite} C) | Leitura: {ld[f'tmp_fase_t_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_nucleo_gerador_1_ug{self.__ug_id}"].valor >= cd[f"tmp_nucleo_gerador_1_ug{self.__ug_id}"].valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Núcleo Gerador 1 da UG passou do valor base! ({cd[f'tmp_nucleo_gerador_1_ug{self.__ug_id}'].valor_base} C) | Leitura: {cd[f'tmp_nucleo_gerador_1_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_nucleo_gerador_1_ug{self.__ug_id}"].valor >= 0.9*(cd[f"tmp_nucleo_gerador_1_ug{self.__ug_id}"].valor_limite - cd[f"tmp_nucleo_gerador_1_ug{self.__ug_id}"].valor_base) + cd[f"tmp_nucleo_gerador_1_ug{self.__ug_id}"].valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Núcleo Gerador 1 da UG está muito próxima do limite! ({cd[f'tmp_nucleo_gerador_1_ug{self.__ug_id}'].valor_limite} C) | Leitura: {cd[f'tmp_nucleo_gerador_1_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_nucleo_gerador_2_ug{self.__ug_id}"].valor >= cd[f"tmp_nucleo_gerador_2_ug{self.__ug_id}"].valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Núcleo Gerador 2 da UG passou do valor base! ({cd[f'tmp_nucleo_gerador_2_ug{self.__ug_id}'].valor_base} C) | Leitura: {cd[f'tmp_nucleo_gerador_2_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_nucleo_gerador_2_ug{self.__ug_id}"].valor >= 0.9*(cd[f"tmp_nucleo_gerador_2_ug{self.__ug_id}"].valor_limite - cd[f"tmp_nucleo_gerador_2_ug{self.__ug_id}"].valor_base) + cd[f"tmp_nucleo_gerador_2_ug{self.__ug_id}"].valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Núcleo Gerador 2 da UG está muito próxima do limite! ({cd[f'tmp_nucleo_gerador_2_ug{self.__ug_id}'].valor_limite} C) | Leitura: {cd[f'tmp_nucleo_gerador_2_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_nucleo_gerador_3_ug{self.__ug_id}"].valor >= cd[f"tmp_nucleo_gerador_3_ug{self.__ug_id}"].valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Núcleo Gerador 3 da UG passou do valor base! ({cd[f'tmp_nucleo_gerador_3_ug{self.__ug_id}'].valor_base} C) | Leitura: {cd[f'tmp_nucleo_gerador_3_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_nucleo_gerador_3_ug{self.__ug_id}"].valor >= 0.9*(cd[f"tmp_nucleo_gerador_3_ug{self.__ug_id}"].valor_limite - cd[f"tmp_nucleo_gerador_3_ug{self.__ug_id}"].valor_base) + cd[f"tmp_nucleo_gerador_3_ug{self.__ug_id}"].valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Núcleo Gerador 3 da UG está muito próxima do limite! ({cd[f'tmp_nucleo_gerador_3_ug{self.__ug_id}'].valor_limite} C) | Leitura: {cd[f'tmp_nucleo_gerador_3_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_mancal_casq_rad_ug{self.__ug_id}"].valor >= cd[f"tmp_mancal_casq_rad_ug{self.__ug_id}"].valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Mancal Casquilho Radial da UG passou do valor base! ({cd[f'tmp_mancal_casq_rad_ug{self.__ug_id}'].valor_base} C) | Leitura: {cd[f'tmp_mancal_casq_rad_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_mancal_casq_rad_ug{self.__ug_id}"].valor >= 0.9*(cd[f"tmp_mancal_casq_rad_ug{self.__ug_id}"].valor_limite - cd[f"tmp_mancal_casq_rad_ug{self.__ug_id}"].valor_base) + cd[f"tmp_mancal_casq_rad_ug{self.__ug_id}"].valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Mancal Casquilho Radial da UG está muito próxima do limite! ({cd[f'tmp_mancal_casq_rad_ug{self.__ug_id}'].valor_limite} C) | Leitura: {cd[f'tmp_mancal_casq_rad_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_mancal_casq_comb_ug{self.__ug_id}"].valor >= cd[f"tmp_mancal_casq_comb_ug{self.__ug_id}"].valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Mancal Casquilho Combinado da UG passou do valor base! ({cd[f'tmp_mancal_casq_comb_ug{self.__ug_id}'].valor_base} C) | Leitura: {cd[f'tmp_mancal_casq_comb_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_mancal_casq_comb_ug{self.__ug_id}"].valor >= 0.9*(cd[f"tmp_mancal_casq_comb_ug{self.__ug_id}"].valor_limite - cd[f"tmp_mancal_casq_comb_ug{self.__ug_id}"].valor_base) + cd[f"tmp_mancal_casq_comb_ug{self.__ug_id}"].valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Mancal Casquilho Combinado da UG está muito próxima do limite! ({cd[f'tmp_mancal_casq_comb_ug{self.__ug_id}'].valor_limite} C) | Leitura: {cd[f'tmp_mancal_casq_comb_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_mancal_escora_comb_ug{self.__ug_id}"].valor >= cd[f"tmp_mancal_escora_comb_ug{self.__ug_id}"].valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Mancal Escora Combinado da UG passou do valor base! ({cd[f'tmp_mancal_escora_comb_ug{self.__ug_id}'].valor_base} C) | Leitura: {cd[f'tmp_mancal_escora_comb_ug{self.__ug_id}'].valor} C")

        if ld[f"tmp_mancal_escora_comb_ug{self.__ug_id}"].valor >= 0.9*(cd[f"tmp_mancal_escora_comb_ug{self.__ug_id}"].valor_limite - cd[f"tmp_mancal_escora_comb_ug{self.__ug_id}"].valor_base) + cd[f"tmp_mancal_escora_comb_ug{self.__ug_id}"].valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Mancal Escora Combinado da UG está muito próxima do limite! ({cd[f'tmp_mancal_escora_comb_ug{self.__ug_id}'].valor_limite} C) | Leitura: {cd[f'tmp_mancal_escora_comb_ug{self.__ug_id}'].valor} C")

    def leitura_temporizada(self) -> None:
        return

    def carregar_leituras(self) -> None:
        # Leituras de condicionadores com limites de operção checados a cada ciclo
        # Fase R
        self.leitura_dict[f"tmp_fase_r_ug{self.__ug_id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug_id}"],
            REG_UG[f"UG{self.__ug_id}_EA_TEMPERATURA_GERADOR_FASE_A"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_fase_r_ug{self.__ug_id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_fase_r_ug{self.__ug_id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_r_ug{self.__ug_id}"])

        # Fase S
        self.leitura_dict[f"tmp_fase_s_ug{self.__ug_id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug_id}"],
            REG_UG[f"UG{self.__ug_id}_EA_TEMPERATURA_GERADOR_FASE_B"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_fase_s_ug{self.__ug_id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_fase_s_ug{self.__ug_id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_s_ug{self.__ug_id}"])

        # Fase T
        self.leitura_dict[f"tmp_fase_t_ug{self.__ug_id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug_id}"],
            REG_UG[f"UG{self.__ug_id}_EA_TEMPERATURA_GERADOR_FASE_C"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_fase_t_ug{self.__ug_id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_fase_t_ug{self.__ug_id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_t_ug{self.__ug_id}"])

        # Nucleo Gerador 1
        self.leitura_dict[f"tmp_nucleo_gerador_1_ug{self.__ug_id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug_id}"],
            REG_UG[f"UG{self.__ug_id}_EA_TEMPERATURA_GERADOR_NUCLEO_1"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_nucleo_gerador_1_ug{self.__ug_id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_nucleo_gerador_1_ug{self.__ug_id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_nucleo_gerador_1_ug{self.__ug_id}"])

        # Nucleo Gerador 2
        self.leitura_dict[f"tmp_nucleo_gerador_2_ug{self.__ug_id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug_id}"],
            REG_UG[f"UG{self.__ug_id}_EA_TEMPERATURA_GERADOR_NUCLEO_2"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_nucleo_gerador_2_ug{self.__ug_id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_nucleo_gerador_2_ug{self.__ug_id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_nucleo_gerador_2_ug{self.__ug_id}"])

        # Nucleo Gerador 3
        self.leitura_dict[f"tmp_nucleo_gerador_3_ug{self.__ug_id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug_id}"],
            REG_UG[f"UG{self.__ug_id}_EA_TEMPERATURA_GERADOR_NUCLEO_3"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_nucleo_gerador_3_ug{self.__ug_id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_nucleo_gerador_3_ug{self.__ug_id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_nucleo_gerador_3_ug{self.__ug_id}"])

        # Mancal Casquilho Radial
        self.leitura_dict[f"tmp_mancal_casq_rad_ug{self.__ug_id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug_id}"],
            REG_UG[f"UG{self.__ug_id}_EA_TEMPERATURA_MANCAL_GUIA_CASQUILHO"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_mancal_casq_rad_ug{self.__ug_id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_mancal_casq_rad_ug{self.__ug_id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_casq_rad_ug{self.__ug_id}"])

        # Mancal Casquilho Combinado
        self.leitura_dict[f"tmp_mancal_casq_comb_ug{self.__ug_id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug_id}"],
            REG_UG[f"UG{self.__ug_id}_EA_TEMPERATURA_MANCAL_COMBINADO_CASQUILHO"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_mancal_casq_comb_ug{self.__ug_id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_mancal_casq_comb_ug{self.__ug_id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_casq_comb_ug{self.__ug_id}"])

        # Mancal Escora Combinado
        self.leitura_dict[f"tmp_mancal_escora_comb_ug{self.__ug_id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug_id}"],
            REG_UG[f"UG{self.__ug_id}_EA_TEMPERATURA_MANCAL_COMBINADO_ESCORA"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_mancal_escora_comb_ug{self.__ug_id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_mancal_escora_comb_ug{self.__ug_id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_escora_comb_ug{self.__ug_id}"])


        # Leituras de condicionadores essenciais que serão lidos a cada ciclo das UGs

        ## CONDICIONADORES NORMALIZAR
        # WHATS + VOIP
        self.leitura_val_bypass_falha_abrir = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_BYPASS_FALHA_ABRIR"], descr=f"[UG{self.__ug_id}] Válvula Bypass Falha Abrir")
        self.condicionadores_essenciais.append(self.leitura_val_bypass_falha_abrir, CONDIC_NORMALIZAR)

        self.leitura_val_bypass_falha_fechar = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_BYPASS_FALHA_FECHAR"], descr=f"[UG{self.__ug_id}] Válvula Bypass Falha Fechar")
        self.condicionadores_essenciais.append(self.leitura_val_bypass_falha_fechar, CONDIC_NORMALIZAR)

        # WHATS
        self.leitura_rv_alarme_sobrefrequncia = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_ALARME_SOBREFREQUENCIA"], descr=f"[UG{self.__ug_id}] RV Alarme Sobrefrequência")
        self.condicionadores_essenciais.append(self.leitura_rv_alarme_sobrefrequncia, CONDIC_NORMALIZAR)

        self.leitura_rv_alarme_subfrequencia = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_ALARME_SUBFREQUENCIA"], descr=f"[UG{self.__ug_id}] RV Alarme Subfrequência")
        self.condicionadores_essenciais.append(self.leitura_rv_alarme_subfrequencia, CONDIC_NORMALIZAR)

        self.leitura_rv_falha_1 = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_1"], descr=f"[UG{self.__ug_id}] RV Falha 1")
        self.condicionadores_essenciais.append(self.leitura_rv_falha_1, CONDIC_NORMALIZAR)

        self.leitura_botao_bloq_86eh = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_BOTAO_BLOQUEIO_86EH"], descr=f"[UG{self.__ug_id}] Botão Bloqueio 86EH")
        self.condicionadores_essenciais.append(self.leitura_botao_bloq_86eh, CONDIC_NORMALIZAR)

        self.leitura_rele_bloq_86eh = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_RELE_BLOQUEIO_86EH"], descr=f"[UG{self.__ug_id}] Relé Bloqueio 86EH")
        self.condicionadores_essenciais.append(self.leitura_rele_bloq_86eh, CONDIC_NORMALIZAR)

        self.leitura_valv_borb_falha_abertura = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_BROBOLETA_FALHA_ABRIR"], descr=f"[UG{self.__ug_id}] Válvula Borboleta Falha Abertura")
        self.condicionadores_essenciais.append(self.leitura_valv_borb_falha_abertura, CONDIC_NORMALIZAR)

        self.leitura_bloq_86e = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_STT_BLOQUEIO_86E"], descr=f"[UG{self.__ug_id}] Bloqueio 86E")
        self.condicionadores_essenciais.append(self.leitura_bloq_86e, CONDIC_NORMALIZAR)

        self.leitura_bloq_86h = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_STT_BLOQUEIO_86H"], descr=f"[UG{self.__ug_id}] Bloqueio 86H")
        self.condicionadores_essenciais.append(self.leitura_bloq_86h, CONDIC_NORMALIZAR)
        # "UG1_RT_ESTADO_OPERACAO" -> EMERGENCIA = 16
        # "UG1_RV_ESTADO_OPERACAO" -> EMERGENCIA = 16


        ## CONDICIONADORES INDISPONIBILIZAR
        # WHATS + VOIP
        self.leitura_falha_fechar_distrib = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR"], descr=f"[UG{self.__ug_id}] Falha Fechamento Distribuidor")
        self.condicionadores_essenciais.append(self.leitura_falha_fechar_distrib, CONDIC_INDISPONIBILIZAR)

        # WHATS
        self.leitura_rv_girando_gir_indev = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_1_GIRANDO_SEM_REG_GIRO_INDEV"], descr=f"[UG{self.__ug_id}] Falha RV Girando Sem Registro de Giro Indevido")
        self.condicionadores_essenciais.append(self.leitura_rv_girando_gir_indev, CONDIC_INDISPONIBILIZAR)

        self.leitura_rt_alar_1_sobretensao = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_SOBRETENSAO"], descr=f"[UG{self.__ug_id}] RT Alarmes 1 Sobretensão")
        self.condicionadores_essenciais.append(self.leitura_rt_alar_1_sobretensao, CONDIC_INDISPONIBILIZAR)

        self.leitura_rt_alar_1_subtensao = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_SUBTENSAO"], descr=f"[UG{self.__ug_id}] RT Alarmes 1 Subtensão")
        self.condicionadores_essenciais.append(self.leitura_rt_alar_1_subtensao, CONDIC_INDISPONIBILIZAR)

        self.leitura_rt_alar_1_sobrefrequencia = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_SOBREFREQUENCIA"], descr=f"[UG{self.__ug_id}] RT Alarmes 1 Sobrefrequência")
        self.condicionadores_essenciais.append(self.leitura_rt_alar_1_sobrefrequencia, CONDIC_INDISPONIBILIZAR)

        self.leitura_rt_alar_1_subfrequencia = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_SUBFREQUENCIA"], descr=f"[UG{self.__ug_id}] RT Alarmes 1 Subfrequência")
        self.condicionadores_essenciais.append(self.leitura_rt_alar_1_subfrequencia, CONDIC_INDISPONIBILIZAR)

        self.leitura_rt_alar_1_lim_sup_pot_reativa = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_LIMITE_SUP_POT_REATICA"], descr=f"[UG{self.__ug_id}] RT Alarmes 1 Limite Superior Potência Reativa")
        self.condicionadores_essenciais.append(self.leitura_rt_alar_1_lim_sup_pot_reativa, CONDIC_INDISPONIBILIZAR)

        self.leitura_rt_alar_1_lim_inf_pot_reativa = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_LIMITE_INF_POT_REATIAVA"], descr=f"[UG{self.__ug_id}] RT Alarmes 1 Limite Inferior Potência Reativa")
        self.condicionadores_essenciais.append(self.leitura_rt_alar_1_lim_inf_pot_reativa, CONDIC_INDISPONIBILIZAR)

        self.leitura_rt_alar_1_lim_sup_fator_pot = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_LIMITE_SUP_FATOR_POTENCIA"], descr=f"[UG{self.__ug_id}] RT Alarmes 1 Limite Superior Fator Potência")
        self.condicionadores_essenciais.append(self.leitura_rt_alar_1_lim_sup_fator_pot, CONDIC_INDISPONIBILIZAR)

        self.leitura_rt_alar_1_lim_inf_fator_pot = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_LIMITE_INF_FATOR_POTENCIA"], descr=f"[UG{self.__ug_id}] RT Alarmes 1 Limite Inferior Fator Potência")
        self.condicionadores_essenciais.append(self.leitura_rt_alar_1_lim_inf_fator_pot, CONDIC_INDISPONIBILIZAR)

        self.leitura_rt_alar_1_variacao_tensao = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_VARIACAO_TENSAO"], descr=f"[UG{self.__ug_id}] RT Alarmes 1 Variação de Tensão")
        self.condicionadores_essenciais.append(self.leitura_rt_alar_1_variacao_tensao, CONDIC_INDISPONIBILIZAR)

        self.leitura_rt_alar_1_pot_ativa_reversa = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_POTENCIA_ATIVA_REVERSA"], descr=f"[UG{self.__ug_id}] RT Alarmes 1 Potência Ativa Reversa")
        self.condicionadores_essenciais.append(self.leitura_rt_alar_1_pot_ativa_reversa, CONDIC_INDISPONIBILIZAR)

        self.leitura_rt_alar_1_sobrecorr_term = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_SOBRECORRENTE_TERMINAL"], descr=f"[UG{self.__ug_id}] RT Alarmes 1 Sobrecorrente Terminal")
        self.condicionadores_essenciais.append(self.leitura_rt_alar_1_sobrecorr_term, CONDIC_INDISPONIBILIZAR)

        self.leitura_rt_alar_1_lim_sup_corr_excitacao = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_LIMITE_SUP_CORRENTE_EXCITACAO"], descr=f"[UG{self.__ug_id}] RT Alarmes 1 Limite Superior Corrente Excitação")
        self.condicionadores_essenciais.append(self.leitura_rt_alar_1_lim_sup_corr_excitacao, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_LIMITE_INF_CORRENTE_EXCITACAO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_TEMP_MUITO_ALTA_ROTOR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_PRES_TENS_TERM_AUSEN_CORR_EXCI"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_1_PRES_CORR_EXCI_AUSEN_TENS_TERM"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_2_FALHA_CONTROLE_CORRENTE_EXCI"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_2_FALHA_CONTROLE_TENSAO_TERM"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_UHRV_OLEO_NIVEL_MUITO_BAIXO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_UHRV_FILTRO_OLEO_SUJO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_UHRV_PRESSAO_CRITICA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_UHLM_OLEO_NIVEL_MUITO_ALTO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_UHLM_OLEO_NIVEL_MUITO_BAIXO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_UHLM_PRESSAO_LINHA_LUBRIFICACAO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_UHLM_FILTRO_OLEO_SUJO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_UHLM_FLUXO_TROCADOR_CALOR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_QBAG_ESCOVA_POLO_POSITIVO_DESGASTADA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_QBAG_ESCOVA_POLO_NEGATICO_DESGASTADA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_PSA_POCO_DRENAGEM_NIVEL_MUITO_ALTO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_TRISTORES_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_CROWBAR_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_TRAFO_EXCITACAO_MUITO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_UHRV_TEMP_OLEO_MUITO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_FASE_A_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_FASE_B_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_FASE_C_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_NUCLEO_1_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_NUCLEO_2_MUITO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_NUCLEO_3_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_MANCAL_GUIA_CASQUILHO_MUITO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_MANCAL_COMBINADO_CASQUILHO_MUITO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_MANCAL_COMBINADO_ESCORA_MUITO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_UHRV_PRESSAO_OLEO_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_UHRV_PRESSAO_OLEO_MUITO_ALTO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_UHRV_PRESSAO_OLEO_ALTO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_CONTROLE_TRIP_DIFERENCIAL_GRADE"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_DESLIGAR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_UHRV_FALHA_AO_DESLIGAR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_UHLM_BOMBA_1_FALHA_LIGAR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_UHLM_BOMBA_1_FALHA_DESLIGAR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_UHLM_FALHA_PRESSOSTATO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_RV_FALHA_AO_PARTIR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_RV_FALHA_AO_DESABILITAR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_RV_FALHA_AO_PARAR_MAQUINA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_RT_FALHA_AO_PARTIR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_RT_FALHA_AO_DESABILITAR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_BORBOLETA_FALHA_FECHAR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_BORBOLETA_DISCREPANCIA_SENSORES"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_BYPASS_DISCREPANCIA_SENSORES"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        # Demais
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ED_CROWBAR_INATIVO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_1_SOBREFREQ_INSTANT"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_1_SOBREFREQ_TEMPOR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_1_SUBFREQ_TEMPORIZADA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_1_LEIT_POS_DISTRIBUIDOR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_1_LEIT_POTENCIA_ATIVA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_1_LEIT_REFERENCIA_POTENCIA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_1_NV_MONTANTE_MUITO_BAIXO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_1_CONTROLE_POS_DISTRIBUIDOR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_1_RUIDO_MED_VELOC_PRINCIPAL"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_1_RUIDO_MED_VELOC_RETAGUARDA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_2_PERDA_MED_VELOC_RETAGUARDA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_2_TEMPO_EXCESSIVO_PARTIDA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_2_TEMPO_EXCESSIVO_PARADA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_2_DIF_MED_VELO_PRINCIPAL_RETAGUARDA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RV_FALHA_1_PERDA_MED_VELOC_PRINCIPAL"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_2_CROWBAR_ATUADO_REGUL_HABIL"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_2_FALHA_HABIL_DRIVE_EXCI"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_2_FALHA_FECHAR_CONTATOR_CAMPO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_2_FALHA_CORR_EXCI_PRE_EXCI_ATIVA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_2_PERDA_MEDICAO_POTENCIA_REATIVA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_2_PERDA_MEDICAO_TENSAO_TERMINAL"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_2_PERDA_MEDICAO_CORRENTE_EXCI"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_2_RUIDO_INSTRUMEN_REATIVO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_2_RUIDO_INSTRUMEN_TENSAO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_2_RUIDO_INSTRUMEN_EXCI_PRINCI"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ALARMES_2_RUIDO_INSTRUMEN_EXCI_RETAG"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_SOBRETENSAO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_SUBTENSAO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_SOBREFREQUENCIA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_SUBFREQUENCIA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_LIMITE_SUP_POT_REATIVA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_LIMITE_INF_POT_REATIVA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_LIMITE_SUP_FATOR_POT"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_LIMITE_INF_FATOR_POT"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_SOBRETENSAO_INST"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_VARIACAO_TENSAO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_POT_ATIVA_REVERSA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_SOBRECORRENTE_TERMINAL"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_LIMITE_SUP_CORRENTE_EXCITACAO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_LIMITE_INF_CORRENTE_EXCITACAO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_LIMITE_SUP_TENSAO_EXCITACAO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_1_LIMITE_INF_TENSAO_EXCITACAO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_2_TEMP_MUITO_ALTA_ROTOR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_2_PRES_TENS_TERM_AUSEN_CORR_EXCI"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_2_PRES_CORR_EXCI_AUSEN_TENS_TERM"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_2_CONTROLE_CORR_EXCI"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_2_TENSAO_TERMINAL"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_2_CROWBAR_ATUADO_REGULADOR_HABI"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_2_HABI_DRIVE_EXCITACAO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_2_FECHAR_CONTATOR_CAMPO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_2_CORR_EXCITA_PRE_EXCXITA_ATIVA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_2_EXCESSIVO_PRE_EXCITACAO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_2_EXCESSIVO_PARADA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_2_EXCESSIVO_PARTIDA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_2_BLOQ_EXTERNO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_3_PERDA_MED_POT_REATIVA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_3_PERDA_MED_TENSAO_TERM"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_3_PERDA_MED_CORR_EXCI_PRINCI"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_3_PERDA_MED_CORR_EXCI_RETAG"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_3_RUIDO_INSTRUM_REATIVO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_3_RUIDO_INSTRUM_TENSAO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_3_RUIDO_INSTRUM_PRINCI"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_FALHAS_3_RUIDO_INSTRUM_RETAG"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_RELE_PROT_GERADOR_FALHA"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_RELE_PROT_GERADOR_TRIP"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_RELE_PROT_GERADOR_50BF"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_RV_TRIP"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_RT_TRIP"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_DISJUNTOR_TPS_PROTECAO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_DISJUNTOR_TPS_SINCRO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_UHRV_PRESSAO_FREIO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_PSA_BLOQUEIO_86BTBF"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_UHRV_INDISPONIVEL"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_UHRV_FALHA_AO_LIGAR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_UHRV_FALHA_AO_PRESSURIZAR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_UHRV_FILTRO_OLEO_SUJO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_UHLM_BOMBA_1_INDISPONIVEL"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_UHLM_BOMBA_1_FALHA_PRESSURIZAR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_UHLM_FILTRO_SUJO"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_STT_RV"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_RV_FALHA_AO_HABILITAR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_RT_FALHA_AO_HABILITAR"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)

        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_STT_BLOQUEIO_86M"], descr=f"[UG{self.__ug_id}] ")
        self.condicionadores_essenciais.append(self.leitura_, CONDIC_INDISPONIBILIZAR)


        ## WHATSAPP + VOIP
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_CD_CMD_UHRV_MODO_MANUTENCAO"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_CD_CMD_UHLM_MODO_MANUTENCAO"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_TRISTORES_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_CROWBAR_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_TRAFO_EXCITACAO_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_UHRV_TEMP_OLEO_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_NUCLEO_2_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_MANCAL_GUIA_CASQUILHO_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_MANCAL_COMBINADO_CASQUILHO_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_MANCAL_COMBINADO_ESCORA_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR"], descr=f"[UG{self.__ug_id}] ")

        ## WHATSAPP
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_ED_SELEC_MODO_CONTROLE_ISOLADO"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_RT_SD_RELE_ALARME"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_RV_ALARME"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_RV_POTENCIA_NULA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_RT_ALARME"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_DISPOSITIVO_PROTECAO_SURTO"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_UHRV_BOMBA_DEFEITO"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_UHLM_BOMBA_DEFEITO"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_PRTVA_RESISTENCIA_AQUEC_GERADOR_DEFEITO"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_TRISTORES_TEMP_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_CROWBAR_TEMP_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_TRAFO_EXCITACAO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_UHRV_TEMP_OLEO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_FASE_A_TEMP_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_FASE_B_TEMP_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_FASE_C_TEMP_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_NUCLEO_1_TEMP_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_NUCLEO_2_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_GERADOR_NUCLEO_3_TEMP_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_MANCAL_GUIA_CASQUILHO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_MANCAL_COMBINADO_CASQUILHO_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_MANCAL_COMBINADO_ESCORA_ALTA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_SINAL_NIVEL_JUSANTE_FALHA_LEITURA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_SINAL_NIVEL_JUSANTE_MUITO_ALTO"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_SINAL_NIVEL_JUSANTE_ALTO"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_UHRV_PRESSAO_OLEO_BAIXA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_SINAL_NIVEL_JUSANTE_BAIXA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_UHRV_PRESSAO_OLEO_MUITO_BAIXA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_EA_SINAL_NIVEL_JUSANTE_MUITO_BAIXA"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_CONTROLE_ALARME_DIFERENCIAL_GRADE"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_RESISTENCIA_AQUEC_GERADOR_INDISPONIVEL"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_UHLM_UNIDADE_MANUTENCAO"], descr=f"[UG{self.__ug_id}] ")
        self.leitura_ = LeituraModbusBit(self.__clp[f"UG{self.__ug_id}"], REG_UG[f"UG{self.__ug_id}_ED_RV_MODO_MANUTENCAO"], descr=f"[UG{self.__ug_id}] ")
        # "UG1_RV_ESTADO_OPERACAO" -> CONTROLE MANUAL DISTRIBUIDOR = 14
        # "UG1_RV_ESTADO_OPERACAO" -> CONTROLE MANUAL ROTOR = 15
