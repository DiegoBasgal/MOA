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

        if self.leitura_ED_sup_tensao_falha.valor:
            logger.warning("[OCO-USN] Houve uma falha com a leitura de tensão supervisor, favor verificar.")

        if self.leitura_ED_sup_tensao_tsa_falha.valor:
            logger.warning("[OCO-USN] Houve uma falha com a leitura de tensão do Serviço Auxiliar, favor verificar.")

        if self.leitura_ED_sup_tensao_gmg_falha.valor:
            logger.warning("[OCO-USN] Houve uma falha com a leitura de tensão do Grupo Motor Gerador, favor verificar.")

        if self.leitura_EA_nv_montante_muito_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que o Nível Montante está muito baixo, favor verificar.")

        if self.leitura_ED_disj_gmg_fechado.valor:
            logger.warning("[OCO-USN] Foi identificado que o diajuntor d, favor verificar.")

        if self.leitura_ED_disjs_modo_remoto.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_poco_dren_nv_alto.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_dren_boias_discrepancia.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_poco_dren_nv_muito_baixo.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_dren_bomba_1_indisp.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_dren_bomba_2_indisp.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_esgot_bomba_1_falha.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_esgot_bomba_2_falha.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_esgot_bomba_1_indisp.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_esgot_bomba_2_indisp.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_poco_dren_bomba_1_defeito.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_poco_dren_bomba_2_defeito.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_poco_esgot_bomba_1_defeito.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_poco_esgot_bomba_2_defeito.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfa_limp_elem_1_aberta.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfa_limp_elem_2_aberta.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfa_entra_elem_1_aberta.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfa_entra_elem_2_aberta.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfa_falha_abrir_retrolavagem.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfa_falha_fechar_retrolavagem.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfa_falha_abrir_entra_elem.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfa_falha_fechar_entra_elem.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfb_limp_elem_1_aberta.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfb_limp_elem_2_aberta.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfb_entra_elem_1_aberta.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfb_entra_elem_2_aberta.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfb_falha_abrir_entra_elem.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfb_falha_fechar_entra_elem.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfb_falha_abrir_retrolavagem.valor:
            logger.warning("[OCO-USN] , favor verificar.")

        if self.leitura_ED_sfb_falha_fechar_retrolavagem.valor:
            logger.warning("[OCO-USN] , favor verificar.")






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
        ## TELEGRAM + VOIP
        # ENTRADAS DIGITAIS
        self.leitura_ED_dps_gmg_falha = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_DPS_GMG"], descr="[OCO-USN] Falha Grupo Motor Gerador") # Telegram + Voip
        self.leitura_ED_disj_gmg_trip = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_DISJ_GMG_TRIP"], descr="[OCO-USN] Trip Disjuntor Grupo Motor Gerador") # Telegram + Voip
        self.leitura_ED_conv_fibra_falha = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_CONVERSOR_FIBRA_FALHA"], descr="[OCO-USN] Falha Conversor de Fibra") # Telegram + Voip
        self.leitura_ED_carreg_baterias_falha = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"], descr="[OCO-USN] Falha Carregador de Baterias") # Telegram + Voip
        self.leitura_ED_disj_gmg_falha_fechar = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_ED_PSA_GMG_DISJ_FALHA_FECHAR"], descr="[OCO-USN] Falha Fechamento Disjuntor Grupo Motor Gerador") # Telegram + Voip

        # ENTRADAS ANALÓGICAS
        self.leitura_EA_nv_montante_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO"], descr="[OCO-USN] Nível Montante Muito Baixo") # Telegram + Voip

        self.leitura_EA_sfa_press_lado_sujo_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Sujo Alta") # Telegram + Voip
        self.leitura_EA_sfa_press_lado_limpo_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Limpo Alta") # Telegram + Voip
        self.leitura_EA_sfa_press_lado_sujo_muito_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Sujo Muito Alta") # Telegram + Voip
        self.leitura_EA_sfa_press_lado_limpo_muito_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem A Lado Limpo Muito Alta") # Telegram + Voip

        self.leitura_EA_sfb_press_lado_sujo_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem B Lado Sujo Alta") # Telegram + Voip
        self.leitura_EA_sfb_press_lado_limpo_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem B Lado Limpo Alta") # Telegram + Voip
        self.leitura_EA_sfb_press_lado_sujo_muito_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem B Lado Sujo Muito Alta") # Telegram + Voip
        self.leitura_EA_sfb_press_lado_limpo_muito_alto = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO"], descr="[OCO-USN] Pressão Sistema de Filtragem B Lado Limpo Muito Alta") # Telegram + Voip

        ## TELEGRAM
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
        """if self.leitura_ED_FreioPastilhaGasta.valor != 0:
            logger.warning(f"[OCO-UG{self.__ug_id}] O sensor de Freio da UG retornou que a Pastilha está gasta, favor considerar troca.")

        if self.leitura_ED_FreioCmdRemoto.valor == 0 and not d.voip[f"UG{self.__ug_id}_FreioCmdRemoto"]:
            logger.warning(f"[OCO-UG{self.__ug_id}] O freio da UG saiu do modo remoto, favor analisar a situação.")
            d.voip[f"UG{self.__ug_id}_FreioCmdRemoto"] = True
        elif self.leitura_ED_FreioCmdRemoto.valor == 1 and d.voip[f"UG{self.__ug_id}_FreioCmdRemoto"]:
            d.voip[f"UG{self.__ug_id}_FreioCmdRemoto"] = False"""
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