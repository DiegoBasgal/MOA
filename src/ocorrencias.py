import logging
import traceback
import src.dicionarios.dict as d

from time import sleep, time

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
        """if self.leitura_ED_GMG_Trip.valor != 0:
            logger.warning("[OCO-USN] O sensor de TRIP do Grupo Motor Gerador foi acionado, favor verificar.")

        if self.leitura_QCADE_BombasDng_Auto.valor == 0 and not d.voip["BombasDngRemoto"]:
            logger.warning("[OCO-USN] O poço de drenagem da Usina saiu do modo remoto, favor verificar.")
            d.voip["BombasDngRemoto"] = True
        elif self.leitura_QCADE_BombasDng_Auto.valor == 1 and d.voip["BombasDngRemoto"]:
            d.voip["BombasDngRemoto"] = False"""
        return

    def carregar_leituras(self) -> None:
        # Leituras para acionamento temporizado por chamada Voip
        # Leituras de Condicionadores
        leitura_CD_disj_linha_abre = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_CD_DISJ_LINHA_ABRE"], descr="SA_CD_DISJ_LINHA_ABRE")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_CD_disj_linha_abre, CONDIC_NORMALIZAR))

    """
        leitura_ED_disj_linha_aberto = LeituraModbusBit(REG_SA["SA_ED_PSA_SE_DISJ_LINHA_ABERTO"], self.__clp["SA"], descr="SA_CD_DISJ_LINHA_ABRE")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_linha_aberto, CONDIC_NORMALIZAR))

        leitura_ED_rele_linha_trip = LeituraModbusBit(REG_SA["SA_ED_PSA_SE_RELE_LINHA_TRIP"], self.__clp["SA"], descr="SA_ED_PSA_SE_RELE_LINHA_TRIP")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_rele_linha_trip, CONDIC_NORMALIZAR))


        leitura_ED_botao_bloq_86btbf = LeituraModbusBit(REG_SA["SA_ED_PSA_BOTAO_BLOQUEIO_86BTBF"], self.__clp["SA"], descr="SA_ED_PSA_BOTAO_BLOQUEIO_86BTBF")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_botao_bloq_86btbf, CONDIC_INDISPONIBILIZAR))

        leitura_ED_disj_tsa_trip = LeituraModbusBit(REG_SA["SA_ED_PSA_DISJ_TSA_TRIP"], self.__clp["SA"], descr="SA_ED_PSA_DISJ_TSA_TRIP")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_tsa_trip, CONDIC_INDISPONIBILIZAR))

        leitura_ED_rele_bloq_86btbf = LeituraModbusBit(REG_SA["SA_ED_PSA_RELE_BLOQUEIO_86BTBF"], self.__clp["SA"], descr="SA_ED_PSA_RELE_BLOQUEIO_86BTBF")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_rele_bloq_86btbf, CONDIC_INDISPONIBILIZAR))

        leitura_ED_dps_tsa = LeituraModbusBit(REG_SA["SA_ED_PSA_DPS_TSA"], self.__clp["SA"], descr="SA_ED_PSA_DPS_TSA")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_dps_tsa, CONDIC_INDISPONIBILIZAR))

        leitura_ED_poco_dren_nivel_muito_alto = LeituraModbusBit(REG_SA["SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_ALTO"], self.__clp["SA"], descr="SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_ALTO")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_poco_dren_nivel_muito_alto, CONDIC_INDISPONIBILIZAR))

        leitura_ED_trafo_eleva_temp_muito_alto = LeituraModbusBit(REG_SA["SA_ED_PSA_TRAFO_ELEVADOR_TEMP_MUITO_ALTA"], self.__clp["SA"], descr="SA_ED_PSA_TRAFO_ELEVADOR_TEMP_MUITO_ALTA")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_trafo_eleva_temp_muito_alto, CONDIC_INDISPONIBILIZAR))

        leitura_ED_te_temp_muito_alta = LeituraModbusBit(REG_SA["SA_ED_PSA_TE_TEMPERATURA_MUIT_ALTA"], self.__clp["SA"], descr="SA_ED_PSA_TE_TEMPERATURA_MUIT_ALTA")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_te_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        leitura_ED_te_press_muito_alta = LeituraModbusBit(REG_SA["SA_ED_PSA_TE_PRESSAO_MUITO_ALTA"], self.__clp["SA"], descr="SA_ED_PSA_TE_PRESSAO_MUITO_ALTA")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_te_press_muito_alta, CONDIC_INDISPONIBILIZAR))

        leitura_ED_oleo_muito_baixo = LeituraModbusBit(REG_SA["SA_ED_PSA_OLEO_MUITO_BAIXO"], self.__clp["SA"], descr="SA_ED_PSA_OLEO_MUITO_BAIXO")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_oleo_muito_baixo, CONDIC_INDISPONIBILIZAR))

        leitura_ED_prtva1_50bf = LeituraModbusBit(REG_SA["SA_ED_PSA_PRTVA1_50BF"], self.__clp["SA"], descr="SA_ED_PSA_PRTVA1_50BF")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_prtva1_50bf, CONDIC_INDISPONIBILIZAR))

        leitura_ED_prtva2_50bf = LeituraModbusBit(REG_SA["SA_ED_PSA_PRTVA2_50BF"], self.__clp["SA"], descr="SA_ED_PSA_PRTVA2_50BF")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_prtva2_50bf, CONDIC_INDISPONIBILIZAR))

        leitura_ED_se_rele_linha_falha = LeituraModbusBit(REG_SA["SA_ED_PSA_SE_RELE_LINHA_FALHA"], self.__clp["SA"], descr="SA_ED_PSA_SE_RELE_LINHA_FALHA")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_se_rele_linha_falha, CONDIC_INDISPONIBILIZAR))

        leitura_ED_se_rele_linha_50bf = LeituraModbusBit(REG_SA["SA_ED_PSA_SE_RELE_LINHA_50BF"], self.__clp["SA"], descr="SA_ED_PSA_SE_RELE_LINHA_50BF")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_se_rele_linha_50bf, CONDIC_INDISPONIBILIZAR))

        leitura_ED_nv_jusnate_muito_alto = LeituraModbusBit(REG_SA["SA_EA_PSA_NIVEL_JUSANTE_MUITO_ALTO"], self.__clp["SA"], descr="SA_EA_PSA_NIVEL_JUSANTE_MUITO_ALTO")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_nv_jusnate_muito_alto, CONDIC_INDISPONIBILIZAR))

        leitura_ED_disj_gmg_falha_abrir = LeituraModbusBit(REG_SA["SA_ED_PSA_GMG_DISJ_FALHA_ABRIR"], self.__clp["SA"], descr="SA_ED_PSA_GMG_DISJ_FALHA_ABRIR")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_gmg_falha_abrir, CONDIC_INDISPONIBILIZAR))

        leitura_ED_disj_tsa_falha_fechar = LeituraModbusBit(REG_SA["SA_ED_PSA_TSA_DISJ_FALHA_FECHAR"], self.__clp["SA"], descr="SA_ED_PSA_TSA_DISJ_FALHA_FECHAR")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_tsa_falha_fechar, CONDIC_INDISPONIBILIZAR))

        leitura_ED_disj_tsa_falha_abrir = LeituraModbusBit(REG_SA["SA_ED_PSA_TSA_DISJ_FALHA_ABRIR"], self.__clp["SA"], descr="SA_ED_PSA_TSA_DISJ_FALHA_ABRIR")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_tsa_falha_abrir, CONDIC_INDISPONIBILIZAR))

        leitura_ED_disj_se_falha_fechar = LeituraModbusBit(REG_SA["SA_ED_PSA_SE_DISJ_FALHA_FECHAR"], self.__clp["SA"], descr="SA_ED_PSA_SE_DISJ_FALHA_FECHAR")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_se_falha_fechar, CONDIC_INDISPONIBILIZAR))

        leitura_ED_disj_se_falha_abrir = LeituraModbusBit(REG_SA["SA_ED_PSA_SE_DISJ_FALHA_ABRIR"], self.__clp["SA"], descr="SA_ED_PSA_SE_DISJ_FALHA_ABRIR")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_se_falha_abrir, CONDIC_INDISPONIBILIZAR))

        leitura_ED_stt_bloqueio_50bf = LeituraModbusBit(REG_SA["SA_ED_STT_BLOQUEIO_50BF"], self.__clp["SA"], descr="SA_ED_STT_BLOQUEIO_50BF")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_stt_bloqueio_50bf, CONDIC_INDISPONIBILIZAR))

        leitura_ED_bloq_50bf_atuado = LeituraModbusBit(REG_SA["SA_ED_BLOQUEIO_50BF_ATUADO"], self.__clp["SA"], descr="SA_ED_BLOQUEIO_50BF_ATUADO")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_bloq_50bf_atuado, CONDIC_INDISPONIBILIZAR))

        leitura_ED_stt_bloq_86btlsa = LeituraModbusBit(REG_SA["SA_ED_STT_BLOQUEIO_86BTLSA"], self.__clp["SA"], descr="SA_ED_STT_BLOQUEIO_86BTLSA")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_stt_bloq_86btlsa, CONDIC_INDISPONIBILIZAR))

        leitura_ED_bloq_86btlsa_atuado = LeituraModbusBit(REG_SA["SA_ED_BLOQUEIO_86BTLSA_ATUADO"], self.__clp["SA"], descr="SA_ED_BLOQUEIO_86BTLSA_ATUADO")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_bloq_86btlsa_atuado, CONDIC_INDISPONIBILIZAR))

        leitura_CD_disj_gmg_fecha = LeituraModbusBit(REG_SA["SA_CD_DISJ_GMG_FECHA"], self.__clp["SA"], descr="SA_CD_DISJ_GMG_FECHA")
        leitura_CD_disj_linha_abre = LeituraModbusBit(REG_SA["SA_CD_DISJ_LINHA_ABRE"], self.__clp["SA"], descr="SA_CD_DISJ_LINHA_ABRE")
        leitura_CD_sf_manual = LeituraModbusBit(REG_SA["SA_CD_SF_MANUAL"], self.__clp["SA"], descr="SA_CD_SF_MANUAL")
        leitura_ED_bt_bloq_86btbf = LeituraModbusBit(REG_SA["SA_ED_PSA_BOTAO_BLOQUEIO_86BTBF"], self.__clp["SA"], descr="SA_ED_PSA_BOTAO_BLOQUEIO_86BTBF") # Telegram + Voip
        leitura_ED_disjs_modo_remoto = LeituraModbusBit(REG_SA["SA_ED_PSA_DISJUNTORES_MODO_REMOTO"], self.__clp["SA"], descr="SA_ED_PSA_DISJUNTORES_MODO_REMOTO")
        leitura_ED_disj_tsa_trip = LeituraModbusBit(REG_SA["SA_ED_PSA_DISJ_TSA_TRIP"], self.__clp["SA"], descr="SA_ED_PSA_DISJ_TSA_TRIP") # Telegram + Voip
        leitura_ED_disj_gmg_trip = LeituraModbusBit(REG_SA["SA_ED_PSA_DISJ_GMG_TRIP"], self.__clp["SA"], descr="SA_ED_PSA_DISJ_GMG_TRIP") # Telegram + Voip
        leitura_ED_rele_bloq_86btbf = LeituraModbusBit(REG_SA["SA_ED_PSA_RELE_BLOQUEIO_86BTBF"], self.__clp["SA"], descr="SA_ED_PSA_RELE_BLOQUEIO_86BTBF") # Telegram + Voip
        leitura_ED_carreg_baterias_falha = LeituraModbusBit(REG_SA["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"], self.__clp["SA"], descr="SA_ED_PSA_CARREGADOR_BATERIAS_FALHA") # Telegram + Voip
        leitura_ED_conv_fibra_falha = LeituraModbusBit(REG_SA["SA_ED_PSA_CONVERSOR_FIBRA_FALHA"], self.__clp["SA"], descr="SA_ED_PSA_CONVERSOR_FIBRA_FALHA") # Telegram + Voip
        leitura_ED_sup_tensao_falha = LeituraModbusBit(REG_SA["SA_ED_PSA_SUPERVISOR_TENSAO_FALHA"], self.__clp["SA"], descr="SA_ED_PSA_SUPERVISOR_TENSAO_FALHA")
        leitura_ED_dps_tsa_falha = LeituraModbusBit(REG_SA["SA_ED_PSA_DPS_TSA"], self.__clp["SA"], descr="SA_ED_PSA_DPS_TSA") # Telegram + Voip
        leitura_ED_dps_gmg_falha = LeituraModbusBit(REG_SA["SA_ED_PSA_DPS_GMG"], self.__clp["SA"], descr="SA_ED_PSA_DPS_GMG") # Telegram + Voip
        leitura_ED_poco_dren_bomba_1_defeito = LeituraModbusBit(REG_SA["SA_ED_PSA_POCO_DRENAGEM_BOMBA_1_DEFEITO"], self.__clp["SA"], descr="SA_ED_PSA_POCO_DRENAGEM_BOMBA_1_DEFEITO")
        leitura_ED_poco_dren_bomba_2_defeito = LeituraModbusBit(REG_SA["SA_ED_PSA_POCO_DRENAGEM_BOMBA_2_DEFEITO"], self.__clp["SA"], descr="SA_ED_PSA_POCO_DRENAGEM_BOMBA_2_DEFEITO")
        leitura_ED_poco_esgot_bomba_1_defeito = LeituraModbusBit(REG_SA["SA_ED_PSA_POCO_ESGOTAMENTO_BOMBA_1_DEFEITO"], self.__clp["SA"], descr="SA_ED_PSA_POCO_ESGOTAMENTO_BOMBA_1_DEFEITO")
        leitura_ED_poco_esgot_bomba_2_defeito = LeituraModbusBit(REG_SA["SA_ED_PSA_POCO_ESGOTAMENTO_BOMBA_2_DEFEITO"], self.__clp["SA"], descr="SA_ED_PSA_POCO_ESGOTAMENTO_BOMBA_2_DEFEITO")
        leitura_ED_poco_dren_nv_muito_baixo = LeituraModbusBit(REG_SA["SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_BAIXO"], self.__clp["SA"], descr="SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_BAIXO")
        leitura_ED_poco_dren_nv_alto = LeituraModbusBit(REG_SA["SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_ALTO"], self.__clp["SA"], descr="SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_ALTO")
        leitura_ED_poco_dren_nv_muito_alto = LeituraModbusBit(REG_SA["SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_ALTO"], self.__clp["SA"], descr="SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_ALTO")
        leitura_ED_disj_gmg_fechado = LeituraModbusBit(REG_SA["SA_ED_PSA_DIJS_GMG_FECHADO"], self.__clp["SA"], descr="SA_ED_PSA_DIJS_GMG_FECHADO")
        leitura_ED_sup_tensao_tsa_falha = LeituraModbusBit(REG_SA["SA_ED_PSA_SUPERVISOR_TENSAO_TSA_FALHA"], self.__clp["SA"], descr="SA_ED_PSA_SUPERVISOR_TENSAO_TSA_FALHA")
        leitura_ED_sup_tensao_gmg_falha = LeituraModbusBit(REG_SA["SA_ED_PSA_SUPERVISOR_TENSAO_GMG_FALHA"], self.__clp["SA"], descr="SA_ED_PSA_SUPERVISOR_TENSAO_GMG_FALHA")
        leitura_ED_trafo_temp_muito_alta = LeituraModbusBit(REG_SA["SA_ED_PSA_TRAFO_ELEVADOR_TEMP_MUITO_ALTA"], self.__clp["SA"], descr="SA_ED_PSA_TRAFO_ELEVADOR_TEMP_MUITO_ALTA")
        leitura_ED_se_disj_linha_aberto = LeituraModbusBit(REG_SA["SA_ED_PSA_SE_DISJ_LINHA_ABERTO"], self.__clp["SA"], descr="SA_ED_PSA_SE_DISJ_LINHA_ABERTO")  # Telegram + Voip
        leitura_ED_te_temp_muito_alta = LeituraModbusBit(REG_SA["SA_ED_PSA_TE_TEMPERATURA_MUIT_ALTA"], self.__clp["SA"], descr="SA_ED_PSA_TE_TEMPERATURA_MUIT_ALTA")
        leitura_ED_te_press_muito_alta = LeituraModbusBit(REG_SA["SA_ED_PSA_TE_PRESSAO_MUITO_ALTA"], self.__clp["SA"], descr="SA_ED_PSA_TE_PRESSAO_MUITO_ALTA")
        leitura_ED_oleo_muito_baixo = LeituraModbusBit(REG_SA["SA_ED_PSA_OLEO_MUITO_BAIXO"], self.__clp["SA"], descr="SA_ED_PSA_OLEO_MUITO_BAIXO")
        leitura_ED_prtva1_50bf = LeituraModbusBit(REG_SA["SA_ED_PSA_PRTVA1_50BF"], self.__clp["SA"], descr="SA_ED_PSA_PRTVA1_50BF")
        leitura_ED_prtva2_50bf = LeituraModbusBit(REG_SA["SA_ED_PSA_PRTVA2_50BF"], self.__clp["SA"], descr="SA_ED_PSA_PRTVA2_50BF")
        leitura_ED_sfa_entra_elem_1_aberta = LeituraModbusBit(REG_SA["SA_ED_PSA_SFA_ENTRADA_ELEMENTO_1_ABERTA"], self.__clp["SA"], descr="SA_ED_PSA_SFA_ENTRADA_ELEMENTO_1_ABERTA")
        leitura_ED_sfa_entra_elem_2_aberta = LeituraModbusBit(REG_SA["SA_ED_PSA_SFA_ENTRADA_ELEMENTO_2_ABERTA"], self.__clp["SA"], descr="SA_ED_PSA_SFA_ENTRADA_ELEMENTO_2_ABERTA")
        leitura_ED_sfa_limp_elem_1_aberta = LeituraModbusBit(REG_SA["SA_ED_PSA_SFA_LIMPEZA_ELEMENTO_1_ABERTA"], self.__clp["SA"], descr="SA_ED_PSA_SFA_LIMPEZA_ELEMENTO_1_ABERTA")
        leitura_ED_sfa_limp_elem_2_aberta = LeituraModbusBit(REG_SA["SA_ED_PSA_SFA_LIMPEZA_ELEMENTO_2_ABERTA"], self.__clp["SA"], descr="SA_ED_PSA_SFA_LIMPEZA_ELEMENTO_2_ABERTA")
        leitura_ED_sfb_entra_elem_1_aberta = LeituraModbusBit(REG_SA["SA_ED_PSA_SFB_ENTRADA_ELEMENTO_1_ABERTA"], self.__clp["SA"], descr="SA_ED_PSA_SFB_ENTRADA_ELEMENTO_1_ABERTA")
        leitura_ED_sfb_entra_elem_2_aberta = LeituraModbusBit(REG_SA["SA_ED_PSA_SFB_ENTRADA_ELEMENTO_2_ABERTA"], self.__clp["SA"], descr="SA_ED_PSA_SFB_ENTRADA_ELEMENTO_2_ABERTA")
        leitura_ED_sfb_limp_elem_1_aberta = LeituraModbusBit(REG_SA["SA_ED_PSA_SFB_LIMPEZA_ELEMENTO_1_ABERTA"], self.__clp["SA"], descr="SA_ED_PSA_SFB_LIMPEZA_ELEMENTO_1_ABERTA")
        leitura_ED_sfb_limp_elem_2_aberta = LeituraModbusBit(REG_SA["SA_ED_PSA_SFB_LIMPEZA_ELEMENTO_2_ABERTA"], self.__clp["SA"], descr="SA_ED_PSA_SFB_LIMPEZA_ELEMENTO_2_ABERTA")
        leitura_ED_se_rele_linha_trip = LeituraModbusBit(REG_SA["SA_ED_PSA_SE_RELE_LINHA_TRIP"], self.__clp["SA"], descr="SA_ED_PSA_SE_RELE_LINHA_TRIP")  # Telegram + Voip
        leitura_ED_se_rele_linha_falha = LeituraModbusBit(REG_SA["SA_ED_PSA_SE_RELE_LINHA_FALHA"], self.__clp["SA"], descr="SA_ED_PSA_SE_RELE_LINHA_FALHA")
        leitura_EA_nv_jusante_falha_leitura = LeituraModbusBit(REG_SA["SA_EA_PSA_NIVEL_JUSANTE_FALHA_LEITURA"], self.__clp["SA"], descr="SA_EA_PSA_NIVEL_JUSANTE_FALHA_LEITURA")
        leitura_EA_sfa_press_lado_limpo_falha_leitura = LeituraModbusBit(REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_FALHA_LEITURA"], self.__clp["SA"], descr="SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_FALHA_LEITURA")
        leitura_EA_sfa_press_lado_sujo_falha_leitura = LeituraModbusBit(REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_FALHA_LEITURA"], self.__clp["SA"], descr="SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_FALHA_LEITURA")
        leitura_EA_sfb_press_lado_limpo_falha_leitura = LeituraModbusBit(REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_FALHA_LEITURA"], self.__clp["SA"], descr="SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_FALHA_LEITURA")
        leitura_EA_sfb_press_lado_sujo_falha_leitura = LeituraModbusBit(REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_FALHA_LEITURA"], self.__clp["SA"], descr="SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_FALHA_LEITURA")
        leitura_EA_nv_jusante_2_falha_leitura = LeituraModbusBit(REG_SA["SA_EA_PSA_NIVEL_JUSANTE_2_FALHA_LEITURA"], self.__clp["SA"], descr="SA_EA_PSA_NIVEL_JUSANTE_2_FALHA_LEITURA")
        leitura_EA_sfb_press_lado_sujo_falha_leitura = LeituraModbusBit(REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_FALHA_LEITURA"], self.__clp["SA"], descr="SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_FALHA_LEITURA")
        leitura_EA_nv_jusante_muito_alto = LeituraModbusBit(REG_SA["SA_EA_PSA_NIVEL_JUSANTE_MUITO_ALTO"], self.__clp["SA"], descr="SA_EA_PSA_NIVEL_JUSANTE_MUITO_ALTO")  # Telegram + Voip
        leitura_EA_sfa_press_lado_limpo_alto = LeituraModbusBit(REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"], self.__clp["SA"], descr="SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO") # Telegram + Voip
        leitura_EA_sfa_press_lado_sujo_alto = LeituraModbusBit(REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"], self.__clp["SA"], descr="SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO") # Telegram + Voip
        leitura_EA_sfb_press_lado_limpo_alto = LeituraModbusBit(REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"], self.__clp["SA"], descr="SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO") # Telegram + Voip
        leitura_EA_sfb_press_lado_sujo_alto = LeituraModbusBit(REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"], self.__clp["SA"], descr="SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO") # Telegram + Voip
        leitura_EA_sfa_press_lado_limpo_muito_alto = LeituraModbusBit(REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"], self.__clp["SA"], descr="SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO") # Telegram + Voip
        leitura_EA_sfa_press_lado_sujo_muito_alto = LeituraModbusBit(REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"], self.__clp["SA"], descr="SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO") # Telegram + Voip
        leitura_EA_sfb_press_lado_limpo_muito_alto = LeituraModbusBit(REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO"], self.__clp["SA"], descr="SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO") # Telegram + Voip
        leitura_EA_sfb_press_lado_sujo_muito_alto = LeituraModbusBit(REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"], self.__clp["SA"], descr="SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO") # Telegram + Voip
        leitura_EA_nv_jusante_alto = LeituraModbusBit(REG_SA["SA_EA_PSA_NIVEL_JUSANTE_ALTO"], self.__clp["SA"], descr="SA_EA_PSA_NIVEL_JUSANTE_ALTO")
        leitura_EA_nv_montante_baixo = LeituraModbusBit(REG_SA["SA_EA_PSA_NIVEL_MONTANTE_BAIXO"], self.__clp["SA"], descr="SA_EA_PSA_NIVEL_MONTANTE_BAIXO")
        leitura_EA_nv_jusante_2_baixo = LeituraModbusBit(REG_SA["SA_EA_PSA_NIVEL_JUSANTE_2_BAIXO"], self.__clp["SA"], descr="SA_EA_PSA_NIVEL_JUSANTE_2_BAIXO")
        leitura_EA_sfa_press_lado_limpo_baixo = LeituraModbusBit(REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_BAIXO"], self.__clp["SA"], descr="SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_BAIXO")
        leitura_EA_sfa_press_lado_limpo_baixo = LeituraModbusBit(REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_BAIXO"], self.__clp["SA"], descr="SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_BAIXO")
        leitura_EA_sfa_press_lado_sujo_baixo = LeituraModbusBit(REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_BAIXO"], self.__clp["SA"], descr="SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_BAIXO")
        leitura_EA_sfB_press_lado_limpo_baixo = LeituraModbusBit(REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_BAIXO"], self.__clp["SA"], descr="SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_BAIXO")
        leitura_EA_sfB_press_lado_sujo_baixo = LeituraModbusBit(REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_BAIXO"], self.__clp["SA"], descr="SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_BAIXO")
        leitura_EA_sfa_press_lado_limpo_muito_baixo = LeituraModbusBit(REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_BAIXO"], self.__clp["SA"], descr="SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_BAIXO")
        leitura_EA_sfa_press_lado_sujo_muito_baixo = LeituraModbusBit(REG_SA["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_BAIXO"], self.__clp["SA"], descr="SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_BAIXO")
        leitura_EA_sfB_press_lado_limpo_muito_baixo = LeituraModbusBit(REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_BAIXO"], self.__clp["SA"], descr="SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_BAIXO")
        leitura_EA_sfB_press_lado_sujo_muito_baixo = LeituraModbusBit(REG_SA["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_BAIXO"], self.__clp["SA"], descr="SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_BAIXO")
        leitura_EA_nv_jusante_muito_baixo = LeituraModbusBit(REG_SA["SA_EA_PSA_NIVEL_JUSANTE_MUITO_BAIXO"], self.__clp["SA"], descr="SA_EA_PSA_NIVEL_JUSANTE_MUITO_BAIXO")
        leitura_EA_nv_montante_muito_baixo = LeituraModbusBit(REG_SA["SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO"], self.__clp["SA"], descr="SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO") # Telegram + Voip
        leitura_EA_nv_jusante_2_muito_baixo = LeituraModbusBit(REG_SA["SA_EA_PSA_NIVEL_JUSANTE_2_MUITO_BAIXO"], self.__clp["SA"], descr="SA_EA_PSA_NIVEL_JUSANTE_2_MUITO_BAIXO")
        leitura_ED_dren_bomba_1_indisp = LeituraModbusBit(REG_SA["SA_ED_PSA_DREANGEM_BOMBA_1_INDISP"], self.__clp["SA"], descr="SA_ED_PSA_DREANGEM_BOMBA_1_INDISP")
        leitura_ED_dren_bomba_2_indisp = LeituraModbusBit(REG_SA["SA_ED_PSA_DREANGEM_BOMBA_2_INDISP"], self.__clp["SA"], descr="SA_ED_PSA_DREANGEM_BOMBA_2_INDISP")
        leitura_ED_dren_boias_discrepancia = LeituraModbusBit(REG_SA["SA_ED_PSA_DREANGEM_BOIAS_DISCREPANCIA"], self.__clp["SA"], descr="SA_ED_PSA_DREANGEM_BOIAS_DISCREPANCIA")
        leitura_ED_esgot_bomba_1_indisp = LeituraModbusBit(REG_SA["SA_ED_PSA_ESGOTAMENTO_BOMBA_1_INDISP"], self.__clp["SA"], descr="SA_ED_PSA_ESGOTAMENTO_BOMBA_1_INDISP")
        leitura_ED_esgot_bomba_2_indisp = LeituraModbusBit(REG_SA["SA_ED_PSA_ESGOTAMENTO_BOMBA_2_INDISP"], self.__clp["SA"], descr="SA_ED_PSA_ESGOTAMENTO_BOMBA_2_INDISP")
        leitura_ED_esgot_bomba_1_falha = LeituraModbusBit(REG_SA["SA_ED_PSA_ESGOTAMENTO_BOMBA_1_FALHA"], self.__clp["SA"], descr="SA_ED_PSA_ESGOTAMENTO_BOMBA_1_FALHA")
        leitura_ED_esgot_bomba_2_falha = LeituraModbusBit(REG_SA["SA_ED_PSA_ESGOTAMENTO_BOMBA_2_FALHA"], self.__clp["SA"], descr="SA_ED_PSA_ESGOTAMENTO_BOMBA_2_FALHA")
        leitura_ED_disj_gmg_falha_fechar = LeituraModbusBit(REG_SA["SA_ED_PSA_GMG_DISJ_FALHA_FECHAR"], self.__clp["SA"], descr="SA_ED_PSA_GMG_DISJ_FALHA_FECHAR") # Telegram + Voip
        leitura_ED_disj_gmg_falha_abrir = LeituraModbusBit(REG_SA["SA_ED_PSA_GMG_DISJ_FALHA_ABRIR"], self.__clp["SA"], descr="SA_ED_PSA_GMG_DISJ_FALHA_ABRIR") # Telegram + Voip
        leitura_ED_disj_tsa_falha_fechar = LeituraModbusBit(REG_SA["SA_ED_PSA_TSA_DISJ_FALHA_FECHAR"], self.__clp["SA"], descr="SA_ED_PSA_TSA_DISJ_FALHA_FECHAR")
        leitura_ED_disj_tsa_falha_abrir = LeituraModbusBit(REG_SA["SA_ED_PSA_TSA_DISJ_FALHA_ABRIR"], self.__clp["SA"], descr="SA_ED_PSA_TSA_DISJ_FALHA_ABRIR")
        leitura_ED_sfa_falha_abrir_entra_elem = LeituraModbusBit(REG_SA["SA_ED_PSA_SFA_FALHA_ABRIR_ENTRADA_ELEM"], self.__clp["SA"], descr="SA_ED_PSA_SFA_FALHA_ABRIR_ENTRADA_ELEM")
        leitura_ED_sfa_falha_fechar_entra_elem = LeituraModbusBit(REG_SA["SA_ED_PSA_SFA_FALHA_FECHAR_ENTRADA_ELEM"], self.__clp["SA"], descr="SA_ED_PSA_SFA_FALHA_FECHAR_ENTRADA_ELEM")
        leitura_ED_sfb_falha_abrir_entra_elem = LeituraModbusBit(REG_SA["SA_ED_PSA_SFB_FALHA_ABRIR_ENTRADA_ELEM"], self.__clp["SA"], descr="SA_ED_PSA_SFB_FALHA_ABRIR_ENTRADA_ELEM")
        leitura_ED_sfb_falha_fechar_entra_elem = LeituraModbusBit(REG_SA["SA_ED_PSA_SFB_FALHA_FECHAR_ENTRADA_ELEM"], self.__clp["SA"], descr="SA_ED_PSA_SFB_FALHA_FECHAR_ENTRADA_ELEM")
        leitura_ED_sfa_falha_abrir_retrolavagem = LeituraModbusBit(REG_SA["SA_ED_PSA_SFA_FALHA_ABRIR_RETROLAVAGEM"], self.__clp["SA"], descr="SA_ED_PSA_SFA_FALHA_ABRIR_RETROLAVAGEM")
        leitura_ED_sfa_falha_fechar_retrolavagem = LeituraModbusBit(REG_SA["SA_ED_PSA_SFA_FALHA_FECHAR_RETROLAVAGEM"], self.__clp["SA"], descr="SA_ED_PSA_SFA_FALHA_FECHAR_RETROLAVAGEM")
        leitura_ED_sfb_falha_abrir_retrolavagem = LeituraModbusBit(REG_SA["SA_ED_PSA_SFB_FALHA_ABRIR_RETROLAVAGEM"], self.__clp["SA"], descr="SA_ED_PSA_SFB_FALHA_ABRIR_RETROLAVAGEM")
        leitura_ED_sfb_falha_fechar_retrolavagem = LeituraModbusBit(REG_SA["SA_ED_PSA_SFB_FALHA_FECHAR_RETROLAVAGEM"], self.__clp["SA"], descr="SA_ED_PSA_SFB_FALHA_FECHAR_RETROLAVAGEM")
        leitura_ED_stt_bloq_50bf = LeituraModbusBit(REG_SA["SA_ED_STT_BLOQUEIO_50BF"], self.__clp["SA"], descr="SA_ED_STT_BLOQUEIO_50BF")  # Telegram + Voip
        leitura_ED_stt_bloq_50bf_atuado = LeituraModbusBit(REG_SA["SA_ED_STT_BLOQUEIO_50BF_ATUADO"], self.__clp["SA"], descr="SA_ED_STT_BLOQUEIO_50BF_ATUADO")  # Telegram + Voip
        leitura_ED_stt_bloq_86btlsa = LeituraModbusBit(REG_SA["SA_ED_STT_BLOQUEIO_86BTLSA"], self.__clp["SA"], descr="SA_ED_STT_BLOQUEIO_86BTLSA")  # Telegram + Voip
        leitura_ED_stt_bloq_86btlsa_atuado = LeituraModbusBit(REG_SA["SA_ED_BLOQUEIO_86BTLSA_ATUADO"], self.__clp["SA"], descr="SA_ED_BLOQUEIO_86BTLSA_ATUADO")  # Telegram + Voip
    """


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
        leitura_ED_nv_montante_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG_SA["SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO"], descr="SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_nv_montante_muito_baixo, CONDIC_AGUARDAR))
