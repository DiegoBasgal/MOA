import pytz
import logging
import traceback

import src.dicionarios.dict as d

from time import time
from datetime import datetime

from src.funcoes.leitura import *
from src.condicionadores import *
from src.dicionarios.reg import *
from src.dicionarios.const import *
from src.dicionarios.reg_old import *

from src.banco_dados import BancoDados


logger = logging.getLogger("logger")

class OcorrenciasUsn:
    def __init__(self, clp: "dict[str, ModbusClient]"=None, db: "BancoDados"=None) -> "None":

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__db = db
        self.__clp = clp


        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS

        self._condicionadores: "list[CondicionadorBase]" = []
        self._condicionadores_essenciais: "list[CondicionadorBase]" = []


        # FINALIZAÇÃO DO __INIT__

        self.carregar_leituras()

    @property
    def condicionadores(self) -> "list[CondicionadorBase]":
        # PROPRIEDADE -> Retrona a lista de condicionadores da Usina.

        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[CondicionadorBase]") -> "None":
        # SETTER -> Atrubui a nova lista de condicionadores da Usina.

        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[CondicionadorBase]":
        # PROPRIEDADE -> Retrona a lista de condicionadores essenciais da Usina.

        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[CondicionadorBase]") -> "None":
        # SETTER -> Atrubui a nova lista de condicionadores essenciais da Usina.

        self._condicionadores_essenciais = var

    def verificar_condicionadores(self) -> "int":
        """
        Função para a verificação de acionamento de condicionadores e determinação
        de gravidade.

        Itera sobre a lista de condicionadores da Usina e verifica se algum está
        ativo. Caso esteja, verifica o nível de gravidade e retorna o valor para
        a determinação do passo seguinte.
        Caso não haja nenhum condicionador ativo, apenas retorna o valor de ignorar.
        """

        flag = CONDIC_IGNORAR
        v = []

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condicionadores_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            for condic in condicionadores_ativos:
                if condic.gravidade == CONDIC_NORMALIZAR:
                    flag = CONDIC_NORMALIZAR
                elif condic.gravidade == CONDIC_INDISPONIBILIZAR:
                    flag = CONDIC_INDISPONIBILIZAR

            logger.debug("")
            logger.warning(f"[OCO-USN] Foram detectados condicionadores ativos na Usina:")
            [logger.warning(f"[OCO-USN] Descrição: \"{condic.descr}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"") for condic in condicionadores_ativos]
            logger.debug("")

            # for condic in condicionadores_ativos:
            #     v = [datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descr]
            #     self.__db.update_alarmes(v)

            return flag
        return flag

    def verificar_leituras(self) -> "None":
        """
        Função para consulta de acionamentos da usina e avisos através do mecanismo
        de acionamento temporizado.
        """

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
            logger.warning("[OCO-USN] Foi identificado uma falha com a Bomba de Esgotamento 1, favor verificar.")

        if self.leitura_ED_esgot_bomba_2_falha.valor:
            logger.warning("[OCO-USN] Foi identificado uma falha com a Bomba de Esgotamento 2, favor verificar.")

        if self.leitura_ED_esgot_bomba_1_indisp.valor:
            logger.warning("[OCO-USN] A Bomba de Esgotamento 1 entrou em modo indisponível, favor verificar.")

        if self.leitura_ED_esgot_bomba_2_indisp.valor:
            logger.warning("[OCO-USN] A Bomba de Esgotamento 2 entrou em modo indisponível, favor verificar.")

        if self.leitura_ED_poco_dren_bomba_1_defeito.valor:
            logger.warning("[OCO-USN] Foi dentificado um defeito na Bomba de Drenagem 1, favor verificar.")

        if self.leitura_ED_poco_dren_bomba_2_defeito.valor:
            logger.warning("[OCO-USN] Foi dentificado um defeito na Bomba de Drenagem 2, favor verificar.")

        if self.leitura_ED_sfa_limp_elem_1_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que o Elemento de Limpeza 1 do Sistema de Filtragem A foi aberto, favor verificar.")

        if self.leitura_ED_sfa_limp_elem_2_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que o Elemento de Limpeza 2 do Sistema de Filtragem A foi aberto, favor verificar.")

        if self.leitura_ED_sfa_entra_elem_1_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que a Entrada do Elemento 1 do Sistema de Filtragem A foi aberto, favor verificar.")

        if self.leitura_ED_sfa_entra_elem_2_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que a Entrada do Elemento 2 do Sistema de Filtragem A foi aberto, favor verificar.")

        if self.leitura_ED_sfa_falha_abrir_limpeza_elem_1.valor:
            logger.warning("[OCO-USN] Houve uma falha ao abrir a Limpeza do Elemento 1 do Sistema de Filtragem A, favor verificar.")

        if self.leitura_ED_sfa_falha_fechar_limpeza_elem_1.valor:
            logger.warning("[OCO-USN] Houve uma falha ao fechar a Limpeza do Elemento 1 do Sistema de Filtragem A, favor verificar.")

        if self.leitura_ED_sfa_falha_abrir_limpeza_elem_2.valor:
            logger.warning("[OCO-USN] Houve uma falha ao abrir a Limpeza do Elemento 2 do Sistema de Filtragem A, favor verificar.")

        if self.leitura_ED_sfa_falha_fechar_limpeza_elem_2.valor:
            logger.warning("[OCO-USN] Houve uma falha ao fechar a Limpeza do Elemento 2 do Sistema de Filtragem A, favor verificar.")

        if self.leitura_ED_sfa_falha_abrir_entra_elem_1.valor:
            logger.warning("[OCO-USN] Houve uma falha ao abrir a Entrada do Elemento 1 do Sistema de Filtragem A, favor verificar.")

        if self.leitura_ED_sfa_falha_fechar_entra_elem_1.valor:
            logger.warning("[OCO-USN] Houve uma falha ao fechar a Entrada do Elemento 1 do Sistema de Filtragem A, favor verificar.")

        if self.leitura_ED_sfa_falha_abrir_entra_elem_2.valor:
            logger.warning("[OCO-USN] Houve uma falha ao abrir a Entrada do Elemento 2 do Sistema de Filtragem A, favor verificar.")

        if self.leitura_ED_sfa_falha_fechar_entra_elem_2.valor:
            logger.warning("[OCO-USN] Houve uma falha ao fechar a Entrada do Elemento 2 do Sistema de Filtragem A, favor verificar.")

        if self.leitura_ED_sfb_limp_elem_1_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que o Elemento de Limpeza 1 do Sistema de Filtragem B foi aberto, favor verificar.")

        if self.leitura_ED_sfb_limp_elem_2_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que o Elemento de Limpeza 2 do Sistema de Filtragem B foi aberto, favor verificar.")

        if self.leitura_ED_sfb_entra_elem_1_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que a Entrada do Elemento 1 do Sistema de Filtragem B foi aberto, favor verificar.")

        if self.leitura_ED_sfb_entra_elem_2_aberta.valor:
            logger.warning("[OCO-USN] Foi identificado que a Entrada do Elemento 2 do Sistema de Filtragem B foi aberto, favor verificar.")

        if self.leitura_ED_sfb_falha_abrir_limpeza_elem_1.valor:
            logger.warning("[OCO-USN] Houve uma falha ao abrir a Limpeza do Elemento 1 do Sistema de Filtragem B, favor verificar.")

        if self.leitura_ED_sfb_falha_fechar_limpeza_elem_1.valor:
            logger.warning("[OCO-USN] Houve uma falha ao fechar a Limpeza do Elemento 1 do Sistema de Filtragem B, favor verificar.")

        if self.leitura_ED_sfb_falha_abrir_limpeza_elem_2.valor:
            logger.warning("[OCO-USN] Houve uma falha ao abrir a Limpeza do Elemento 2 do Sistema de Filtragem B, favor verificar.")

        if self.leitura_ED_sfb_falha_fechar_limpeza_elem_2.valor:
            logger.warning("[OCO-USN] Houve uma falha ao fechar a Limpeza do Elemento 2 do Sistema de Filtragem B, favor verificar.")

        if self.leitura_ED_sfb_falha_abrir_entra_elem_1.valor:
            logger.warning("[OCO-USN] Houve uma falha ao abrir a Entrada do Elemento 1 do Sistema de Filtragem B, favor verificar.")

        if self.leitura_ED_sfb_falha_fechar_entra_elem_1.valor:
            logger.warning("[OCO-USN] Houve uma falha ao fechar a Entrada do Elemento 1 do Sistema de Filtragem B, favor verificar.")

        if self.leitura_ED_sfb_falha_abrir_entra_elem_2.valor:
            logger.warning("[OCO-USN] Houve uma falha ao abrir a Entrada do Elemento 2 do Sistema de Filtragem B, favor verificar.")

        if self.leitura_ED_sfb_falha_fechar_entra_elem_2.valor:
            logger.warning("[OCO-USN] Houve uma falha ao fechar a Entrada do Elemento 2 do Sistema de Filtragem B, favor verificar.")

        if self.leitura_EA_nv_montante_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que o Nível Montante está baixo, favor verificar.")

        if self.leitura_EA_nv_jusante_alto.valor:
            logger.warning("[OCO-USN] Foi identificado que o Nível Jusante está alto, favor verificar.")

        if self.leitura_EA_nv_jusante_muito_baixo.valor:
            logger.warning("[OCO-USN] Foi identificado que o Nível Jusante está muito baixo, favor verificar.")

        if self.leitura_EA_nv_jusante_falha_leitura.valor:
            logger.warning("[OCO-USN] Houve uma falha na leitura de Nível Jusante, favor verificar.")

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

        # WHATSAPP + VOIP
        if self.leitura_ED_disj_gmg_trip.valor and not d.voip["SA_ED_PSA_DISJ_GMG_TRIP"][0]:
            logger.warning("[OCO-USN] Foi identificado um sinal de Trip do Grupo Motor Gerador, favor verificar.")
            d.voip["SA_ED_PSA_DISJ_GMG_TRIP"][0] = True
        elif not self.leitura_ED_disj_gmg_trip.valor and d.voip["SA_ED_PSA_DISJ_GMG_TRIP"][0]:
            d.voip["SA_ED_PSA_DISJ_GMG_TRIP"][0] = False

        if self.leitura_ED_dps_gmg_falha.valor and not d.voip["SA_ED_PSA_DPS_GMG"][0]:
            logger.warning("[OCO-USN] Houve uma falha com o Grupo Motor Gerador, favor verificar.")
            d.voip["SA_ED_PSA_DPS_GMG"][0] = True
        elif not self.leitura_ED_dps_gmg_falha.valor and d.voip["SA_ED_PSA_DPS_GMG"][0]:
            d.voip["SA_ED_PSA_DPS_GMG"][0] = False

        if self.leitura_ED_carreg_baterias_falha.valor and not d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"][0]:
            logger.warning("[OCO-USN] Houve uma falha com o Carregador de Baterias, favor verificar.")
            d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"][0] = True
        elif not self.leitura_ED_carreg_baterias_falha.valor and d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"][0]:
            d.voip["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"][0] = False

        if self.leitura_EA_nv_montante_muito_baixo.valor and not d.voip["SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO"][0]:
            logger.warning("[OCO-USN] Foi identificado que o Nível Montante está Muito Baixo, favor verificar.")
            d.voip["SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO"][0] = True
        elif not self.leitura_EA_nv_montante_muito_baixo.valor and d.voip["SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO"][0]:
            d.voip["SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO"][0] = False

        if self.leitura_EA_sfa_press_lado_sujo_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"][0]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado sujo do Sistema de Filtragem A está alto, favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"][0] = True
        elif not self.leitura_EA_sfa_press_lado_sujo_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"][0] = False

        if self.leitura_EA_sfa_press_lado_limpo_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"][0]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado limpo do Sistema de Filtragem A está alto, favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"][0] = True
        elif not self.leitura_EA_sfa_press_lado_limpo_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"][0] = False

        if self.leitura_EA_sfa_press_lado_sujo_muito_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"][0]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado sujo do Sistema de Filtragem A está muito alto, favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"][0] = True
        elif not self.leitura_EA_sfa_press_lado_sujo_muito_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"][0] = False

        if self.leitura_EA_sfa_press_lado_limpo_muito_alto.valor and not d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado limpo do Sistema de Filtragem A está muito alto, favor verificar.")
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"][0] = True
        elif not self.leitura_EA_sfa_press_lado_limpo_muito_alto.valor and d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0] = False

        if self.leitura_EA_sfb_press_lado_sujo_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"][0]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado sujo do Sistema de Filtragem B está alto, favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"][0] = True
        elif not self.leitura_EA_sfb_press_lado_sujo_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"][0] = False

        if self.leitura_EA_sfb_press_lado_limpo_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"][0]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado limpo do Sistema de Filtragem B está alto, favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"][0] = True
        elif not self.leitura_EA_sfb_press_lado_limpo_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"][0] = False

        if self.leitura_EA_sfb_press_lado_sujo_muito_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"][0]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado sujo do Sistema de Filtragem B está muito alto, favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"][0] = True
        elif not self.leitura_EA_sfb_press_lado_sujo_muito_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"][0] = False

        if self.leitura_EA_sfb_press_lado_limpo_muito_alto.valor and not d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0]:
            logger.warning("[OCO-USN] Foi identificado que a pressão do lado limpo do Sistema de Filtragem B está muito alto, favor verificar.")
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"][0] = True
        elif not self.leitura_EA_sfb_press_lado_limpo_muito_alto.valor and d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO"][0]:
            d.voip["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO_MUITO_ALTO"][0] = False

        return

    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """

        ### Leituras para acionamento temporizado por chamada Voip
        ## CONDICIONADORES ESSENCIAIS
        # ENTRADAS DIGITAIS
        # Diversos

        leitura_ED_bloq_rele_86btbf = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_RELE_BLOQUEIO_86BTBF"], descr="[USN] Bloqueio 86BTBF Relé SA")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_bloq_rele_86btbf, CONDIC_NORMALIZAR))

        leitura_ED_bloq_botao_86btbf = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_BOTAO_BLOQUEIO_86BTBF"], descr="[USN] Botão Bloqueio 86BTBF Relé SA pressionado")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_bloq_botao_86btbf, CONDIC_NORMALIZAR))

        leitura_ED_prtva1_50bf = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_PRTVA1_50BF"], descr="[USN] Bloqueio Relé 50BF PRTVA 1")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_prtva1_50bf, CONDIC_NORMALIZAR))

        leitura_ED_prtva2_50bf = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_PRTVA2_50BF"], descr="[USN] Bloqueio Relé 50BF PRTVA 2")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_prtva2_50bf, CONDIC_NORMALIZAR))

        leitura_ED_disj_linha_aberto = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SE_DISJ_LINHA_ABERTO"], descr="[USN] Disjuntor de Linha Aberto")
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ED_disj_linha_aberto, CONDIC_NORMALIZAR))


        ## CONDICIONADORES NORMAIS
        # Trip
        leitura_ED_disj_tsa_trip = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_DISJ_TSA_TRIP"], descr="[USN] Trip Disjuntor Serviço Auxiliar")
        self.condicionadores.append(CondicionadorBase(leitura_ED_disj_tsa_trip, CONDIC_INDISPONIBILIZAR))
        
        # TODO -> Verificar as seguintes leituras de condicionadores
        '''
        # # Temperatura, Nível e Pressão
        # leitura_ED_te_temp_muito_alta = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_TE_TEMPERATURA_MUITO_ALTA"], descr="[USN] Trasformador Elevador Temperatura Alta") # TODO -> Verificar invertido
        # self.condicionadores.append(CondicionadorBase(leitura_ED_te_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        # leitura_ED_te_eleva_temp_muito_alta = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_TE_TEMPERATURA_ALTA"], descr="[USN] Trasformador Elevador Temperatura Muito Alta")
        # self.condicionadores.append(CondicionadorBase(leitura_ED_te_eleva_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        # leitura_ED_te_press_muito_alta = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_TE_PRESSAO_MUITO_ALTA"], descr="[USN] Trasformador Elevador Pressão Muito Alta")
        # self.condicionadores.append(CondicionadorBase(leitura_ED_te_press_muito_alta, CONDIC_INDISPONIBILIZAR))

        # leitura_ED_oleo_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_NIVEL_OLEO_MUITO_BAIXO"], descr="[USN] Trasformador Elevador Óleo Muito Baixo")
        # self.condicionadores.append(CondicionadorBase(leitura_ED_oleo_muito_baixo, CONDIC_INDISPONIBILIZAR))

        # leitura_ED_poco_dren_nivel_muito_alto = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_ALTO"], descr="[USN] Poço de Drenagem Nível Muito Alto")
        # self.condicionadores.append(CondicionadorBase(leitura_ED_poco_dren_nivel_muito_alto, CONDIC_INDISPONIBILIZAR))

        # leitura_ED_nv_jusante_muito_alto = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_NIVEL_JUSANTE_MUITO_ALTO"], descr="[USN] Nível Jusante Muito Alto")
        # self.condicionadores.append(CondicionadorBase(leitura_ED_nv_jusante_muito_alto, CONDIC_INDISPONIBILIZAR))

        # Falhas
        # leitura_ED_dps_tsa = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_DPS_TSA"], descr="[USN] Falha Disjuntor Serviço Auxiliar")
        # self.condicionadores.append(CondicionadorBase(leitura_ED_dps_tsa, CONDIC_INDISPONIBILIZAR))

        # leitura_ED_disj_gmg_falha_abrir = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_GMG_DISJ_FALHA_ABRIR"], descr="[USN] Falha Abertura Disjuntor Grupo Motor Gerador")
        # self.condicionadores.append(CondicionadorBase(leitura_ED_disj_gmg_falha_abrir, CONDIC_INDISPONIBILIZAR))

        # leitura_ED_disj_tsa_falha_fechar = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_TSA_DISJ_FALHA_FECHAR"], descr="[USN] Falha Fechamento Disjuntor Serviço Auxiliar")
        # self.condicionadores.append(CondicionadorBase(leitura_ED_disj_tsa_falha_fechar, CONDIC_INDISPONIBILIZAR))

        # leitura_ED_disj_tsa_falha_abrir = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_TSA_DISJ_FALHA_ABRIR"], descr="[USN] Falha Abertura Disjuntor Serviço Auxiliar")
        # self.condicionadores.append(CondicionadorBase(leitura_ED_disj_tsa_falha_abrir, CONDIC_INDISPONIBILIZAR))

        # leitura_ED_disj_se_falha_fechar = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SE_DISJ_FALHA_FECHAR"], descr="[USN] Falha Fechamento Disjuntor de Linha")
        # self.condicionadores.append(CondicionadorBase(leitura_ED_disj_se_falha_fechar, CONDIC_INDISPONIBILIZAR))

        # leitura_ED_disj_se_falha_abrir = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SE_DISJ_FALHA_ABRIR"], descr="[USN] Falha Abertura Disjuntor de Linha")
        # self.condicionadores.append(CondicionadorBase(leitura_ED_disj_se_falha_abrir, CONDIC_INDISPONIBILIZAR))

        # Bloqueios
        # leitura_ED_bloq_50bf_atuado = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_BLOQUEIO_50BF_ATUADO"], descr="[USN] Bloqueio 50BF Relé SA Atuado")
        # self.condicionadores.append(CondicionadorBase(leitura_ED_bloq_50bf_atuado, CONDIC_INDISPONIBILIZAR))

        # leitura_ED_bloq_86btlsa_atuado = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_BLOQUEIO_86BTLSA_ATUADO"], descr="[USN] Bloqueio 86BTLSA Relé SA Atuado")
        # self.condicionadores.append(CondicionadorBase(leitura_ED_bloq_86btlsa_atuado, CONDIC_INDISPONIBILIZAR))
        '''

        leitura_ED_bloq_stt_50bf = LeituraModbusCoil(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_STT_BLOQUEIO_50BF"], descr="[USN] Status Bloqueio 50BF Relé SA")
        self.condicionadores.append(CondicionadorBase(leitura_ED_bloq_stt_50bf, CONDIC_INDISPONIBILIZAR))

        leitura_ED_bloq_stt_86btlsa = LeituraModbusCoil(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_STT_BLOQUEIO_86BTLSA"], descr="[USN] Status Bloqueio 86BTLSA Relé SA")
        self.condicionadores.append(CondicionadorBase(leitura_ED_bloq_stt_86btlsa, CONDIC_INDISPONIBILIZAR))



        # ### OUTRAS LEITURAS
        # ## WHATSAPP + VOIP
        # ENTRADAS DIGITAIS
        self.leitura_ED_dps_gmg_falha = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_DPS_GMG"], descr="[USN] Falha Grupo Motor Gerador")
        self.leitura_ED_disj_gmg_trip = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_DISJ_GMG_TRIP"], descr="[USN] Trip Disjuntor Grupo Motor Gerador")
        self.leitura_ED_carreg_baterias_falha = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_CARREGADOR_BATERIAS_FALHA"], descr="[USN] Falha Carregador de Baterias")
        self.leitura_ED_disj_gmg_falha_fechar = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_GMG_DISJ_FALHA_FECHAR"], descr="[USN] Falha Fechamento Disjuntor Grupo Motor Gerador")

        # ENTRADAS ANALÓGICAS
        self.leitura_EA_nv_montante_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO"], descr="[USN] Nível Montante Muito Baixo")

        self.leitura_EA_sfa_press_lado_sujo_alto = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO"], descr="[USN] Pressão Sistema de Filtragem A Lado Sujo Alta")
        self.leitura_EA_sfa_press_lado_limpo_alto = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO"], descr="[USN] Pressão Sistema de Filtragem A Lado Limpo Alta")
        self.leitura_EA_sfa_press_lado_sujo_muito_alto = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO"], descr="[USN] Pressão Sistema de Filtragem A Lado Sujo Muito Alta")
        self.leitura_EA_sfa_press_lado_limpo_muito_alto = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO"], descr="[USN] Pressão Sistema de Filtragem A Lado Limpo Muito Alta")

        self.leitura_EA_sfb_press_lado_sujo_alto = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO"], descr="[USN] Pressão Sistema de Filtragem B Lado Sujo Alta")
        self.leitura_EA_sfb_press_lado_limpo_alto = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO"], descr="[USN] Pressão Sistema de Filtragem B Lado Limpo Alta")
        self.leitura_EA_sfb_press_lado_sujo_muito_alto = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO"], descr="[USN] Pressão Sistema de Filtragem B Lado Sujo Muito Alta")
        self.leitura_EA_sfb_press_lado_limpo_muito_alto = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO"], descr="[USN] Pressão Sistema de Filtragem B Lado Limpo Muito Alta")

        ## WHATSAPP
        # ENTRADAS DIGITAIS
        self.leitura_ED_sup_tensao_falha = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SUPERVISOR_TENSAO_FALHA"], descr="[USN] Falha Tensão pelo Supervisório")
        self.leitura_ED_sup_tensao_tsa_falha = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SUPERVISOR_TENSAO_TSA_FALHA"], descr="[USN] Falha Tensão Serviço Auxiliar pelo Supervisório")
        self.leitura_ED_sup_tensao_gmg_falha = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SUPERVISOR_TENSAO_GMG_FALHA"], descr="[USN] Falha Tensão Grupo Motor Gerador pelo Supervisório")

        self.leitura_ED_disj_gmg_fechado = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_DIJS_GMG_FECHADO"], descr="[USN] Disjuntor Grupo Motor Gerador Fechado")
        self.leitura_ED_disjs_modo_remoto = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_DISJUNTORES_MODO_REMOTO"], descr="[USN] Disjuntores em Modo Remoto")

        self.leitura_ED_poco_dren_nv_alto = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_ALTO"], descr="[USN] Poço de Drenagem Nível Alto")
        self.leitura_ED_dren_boias_discrepancia = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_DREANGEM_BOIAS_DISCREPANCIA"], descr="[USN] Dicrepância Boias de Drenagem")
        self.leitura_ED_poco_dren_nv_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_BAIXO"], descr="[USN] Poço de Drenagem Nível Muito Alto")

        self.leitura_ED_dren_bomba_1_indisp = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_DREANGEM_BOMBA_1_INDISP"], descr="[USN] Bomba de Drenagem 1 Indisponível")
        self.leitura_ED_dren_bomba_2_indisp = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_DREANGEM_BOMBA_2_INDISP"], descr="[USN] Bomba de Drenagem 2 Indisponível")
        self.leitura_ED_esgot_bomba_1_falha = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_ESGOTAMENTO_BOMBA_1_FALHA"], descr="[USN] Falha Bomba de Esgotamento 1")
        self.leitura_ED_esgot_bomba_2_falha = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_ESGOTAMENTO_BOMBA_2_FALHA"], descr="[USN] Falha Bomba de Esgotamento 2") # TODO -> verificar invertido
        self.leitura_ED_esgot_bomba_1_indisp = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_ESGOTAMENTO_BOMBA_1_INDISP"], descr="[USN] Bomba de Esgotamento 1 Indisponível")
        self.leitura_ED_esgot_bomba_2_indisp = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_ESGOTAMENTO_BOMBA_2_INDISP"], descr="[USN] Bomba de Esgotamento 2 Indisponível")
        self.leitura_ED_poco_dren_bomba_1_defeito = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_POCO_DRENAGEM_BOMBA_1_DEFEITO"], descr="[USN] Defeito Bomba 1 Poço de Drenagem")
        self.leitura_ED_poco_dren_bomba_2_defeito = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_POCO_DRENAGEM_BOMBA_2_DEFEITO"], descr="[USN] Defeito Bomba 2 Poço de Drenagem")

        self.leitura_ED_sfa_limp_elem_1_aberta = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFA_LIMPEZA_ELEMENTO_1_ABERTA"], descr="[USN] Sistema de Filtragem A Elemento 1 Aberto")
        self.leitura_ED_sfa_limp_elem_2_aberta = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFA_LIMPEZA_ELEMENTO_2_ABERTA"], descr="[USN] Sistema de Filtragem A Elemento 2 Aberto")
        self.leitura_ED_sfa_entra_elem_1_aberta = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFA_ENTRADA_ELEMENTO_1_ABERTA"], descr="[USN] Sistema de Filtragem A Entrada Elemento 1 Aberto") # TODO -> verificar invertido
        self.leitura_ED_sfa_entra_elem_2_aberta = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFA_ENTRADA_ELEMENTO_2_ABERTA"], descr="[USN] Sistema de Filtragem A Entrada Elemento 2 Aberto")
        self.leitura_ED_sfa_falha_abrir_limpeza_elem_1 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_ABRIR_LIMPEZA_ELEM_1"], descr="[USN] Falha Abrir Limpeza do Elemento 1 do Sistema de Filtragem A")
        self.leitura_ED_sfa_falha_fechar_limpeza_elem_1 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_FECHAR_LIMPEZA_ELEM_1"], descr="[USN] Falha Fechar limpeza do Elemento 1 do Sistema de Filtragem A")
        self.leitura_ED_sfa_falha_abrir_entra_elem_1 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_ABRIR_ENTRADA_ELEM_1"], descr="[USN] Falha Abrir Entrada Elemento 1 do Sistema de Filtragem A")
        self.leitura_ED_sfa_falha_fechar_entra_elem_1 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_FECHAR_ENTRADA_ELEM_1"], descr="[USN] Falha Fechar Entrada Elemento 1 do Sistema de Filtragem A")
        self.leitura_ED_sfa_falha_abrir_limpeza_elem_2 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_ABRIR_LIMPEZA_ELEM_2"], descr="[USN] Falha Abrir Limpeza do Elemento 2 do Sistema de Filtragem A")
        self.leitura_ED_sfa_falha_fechar_limpeza_elem_2 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_FECHAR_LIMPEZA_ELEM_2"], descr="[USN] Falha Fechar limpeza do Elemento 2 do Sistema de Filtragem A")
        self.leitura_ED_sfa_falha_abrir_entra_elem_2 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_ABRIR_ENTRADA_ELEM_2"], descr="[USN] Falha Abrir Entrada Elemento 2 do Sistema de Filtragem A")
        self.leitura_ED_sfa_falha_fechar_entra_elem_2 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFA_FALHA_FECHAR_ENTRADA_ELEM_2"], descr="[USN] Falha Fechar Entrada Elemento 2 do Sistema de Filtragem A")

        self.leitura_ED_sfb_limp_elem_1_aberta = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFB_LIMPEZA_ELEMENTO_1_ABERTA"], descr="[USN] Sistema de Filtragem B Elemento 1 Aberto") # TODO -> verificar invertido
        self.leitura_ED_sfb_limp_elem_2_aberta = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFB_LIMPEZA_ELEMENTO_2_ABERTA"], descr="[USN] Sistema de Filtragem B Elemento 2 Aberto")
        self.leitura_ED_sfb_entra_elem_1_aberta = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFB_ENTRADA_ELEMENTO_1_ABERTA"], descr="[USN] Sistema de Filtragem B Entrada Elemento 1 Aberto")
        self.leitura_ED_sfb_entra_elem_2_aberta = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFB_ENTRADA_ELEMENTO_2_ABERTA"], descr="[USN] Sistema de Filtragem B Entrada Elemento 2 Aberto")
        self.leitura_ED_sfb_falha_abrir_limpeza_elem_1 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_ABRIR_LIMPEZA_ELEM_1"], descr="[USN] Falha Abrir Limpeza do Elemento 1 do Sistema de Filtragem B")
        self.leitura_ED_sfb_falha_fechar_limpeza_elem_1 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_FECHAR_LIMPEZA_ELEM_1"], descr="[USN] Falha Fechar limpeza do Elemento 1 do Sistema de Filtragem B")
        self.leitura_ED_sfb_falha_abrir_entra_elem_1 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_ABRIR_ENTRADA_ELEM_1"], descr="[USN] Falha Abrir Entrada Elemento 1 do Sistema de Filtragem B") # TODO -> verificar invertido
        self.leitura_ED_sfb_falha_fechar_entra_elem_1 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_FECHAR_ENTRADA_ELEM_1"], descr="[USN] Falha Fechar Entrada Elemento 1 do Sistema de Filtragem B")
        self.leitura_ED_sfb_falha_abrir_limpeza_elem_2 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_ABRIR_LIMPEZA_ELEM_2"], descr="[USN] Falha Abrir Limpeza do Elemento 2 do Sistema de Filtragem B")
        self.leitura_ED_sfb_falha_fechar_limpeza_elem_2 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_FECHAR_LIMPEZA_ELEM_2"], descr="[USN] Falha Fechar limpeza do Elemento 2 do Sistema de Filtragem B")
        self.leitura_ED_sfb_falha_abrir_entra_elem_2 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_ABRIR_ENTRADA_ELEM_2"], descr="[USN] Falha Abrir Entrada Elemento 2 do Sistema de Filtragem B")
        self.leitura_ED_sfb_falha_fechar_entra_elem_2 = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_ED_PSA_SFB_FALHA_FECHAR_ENTRADA_ELEM_2"], descr="[USN] Falha Fechar Entrada Elemento 2 do Sistema de Filtragem B")

        # ENTRADAS ANALÓGICAS
        self.leitura_EA_nv_montante_baixo = LeituraModbusBit(self.__clp["TDA"], REG["CONDIC_SA"]["SA_EA_PSA_NIVEL_MONTANTE_BAIXO"], descr="[USN] Nível Montante Baixo") # TODO -> verificar se alterar o clp adiantou
        self.leitura_EA_nv_jusante_alto = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_NIVEL_JUSANTE_ALTO"], descr="[USN] Nível Jusante Alto")
        self.leitura_EA_nv_jusante_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_NIVEL_JUSANTE_MUITO_BAIXO"], descr="[USN] Nível Jusante Muito Baixo")
        self.leitura_EA_nv_jusante_falha_leitura = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_NIVEL_JUSANTE_FALHA_LEITURA"], descr="[USN] Falha Leitura Nível Jusante")

        self.leitura_EA_sfa_press_lado_sujo_falha_leitura = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_FALHA_LEITURA"], descr="[USN] Falha Leitura Pressão Sistema de Filtragem A Lado Sujo")
        self.leitura_EA_sfa_press_lado_limpo_falha_leitura = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_FALHA_LEITURA"], descr="[USN] Falha Leitura Pressão Sistema de Filtragem A Lado Limpo")

        self.leitura_EA_sfb_press_lado_sujo_falha_leitura = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_FALHA_LEITURA"], descr="[USN] Falha Leitura Pressão Sistema de Filtragem B Lado Sujo")
        self.leitura_EA_sfb_press_lado_limpo_falha_leitura = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_FALHA_LEITURA"], descr="[USN] Falha Leitura Pressão Sistema de Filtragem B Lado Limpo")

        self.leitura_EA_sfa_press_lado_sujo_baixo = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_BAIXO"], descr="[USN] Pressão Sistema de Filtragem A Lado Sujo Baixo")
        self.leitura_EA_sfa_press_lado_limpo_baixo = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_BAIXO"], descr="[USN] Pressão Sistema de Filtragem A Lado Limpo Baixo")
        self.leitura_EA_sfa_press_lado_sujo_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_BAIXO"], descr="[USN] Pressão Sistema de Filtragem A Lado Sujo Muito Baixo")
        self.leitura_EA_sfa_press_lado_limpo_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_BAIXO"], descr="[USN] Pressão Sistema de Filtragem A Lado Limpo Muito Baixo")

        self.leitura_EA_sfb_press_lado_sujo_baixo = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_BAIXO"], descr="[USN] Pressão Sistema de Filtragem A Lado Sujo Baixo")
        self.leitura_EA_sfb_press_lado_limpo_baixo = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_BAIXO"], descr="[USN] Pressão Sistema de Filtragem A Lado Limpo Baixo")
        self.leitura_EA_sfb_press_lado_sujo_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_BAIXO"], descr="[USN] Pressão Sistema de Filtragem A Lado Sujo Muito Baixo")
        self.leitura_EA_sfb_press_lado_limpo_muito_baixo = LeituraModbusBit(self.__clp["SA"], REG["CONDIC_SA"]["SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_BAIXO"], descr="[USN] Pressão Sistema de Filtragem A Lado Limpo Muito Baixo")

        return

class OcorrenciasUg:
    def __init__(self, ug, clp: "dict[str, ModbusClient]"=None, db: "BancoDados"=None):

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__ug = ug
        self.__db = db
        self.__clp = clp

        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS

        self._temperatura_base: int = 100
        self._temperatura_limite: int = 200

        self._condicionadores: "list[CondicionadorBase]" = []
        self._condicionadores_essenciais: "list[CondicionadorBase]" = []

        self._leitura_dict: "dict[str, LeituraModbus]" = {}
        self._condic_dict: "dict[str, CondicionadorBase]" = {}


        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.leitura_voip: "dict[str, LeituraModbus]" = {}


        # FINALIZAÇÃO DO __INIT__

        self.carregar_leituras()

    @property
    def temperatura_base(self) -> "int":
        # PROPRIEDADE -> Retrona o valor de temperaturas base da Unidade.

        return self._temperatura_base

    @temperatura_base.setter
    def temperatura_base(self, var: "int") -> None:
        # SETTER -> Atrubui o novo valor de temperaturas base da Unidade.

        self._temperatura_base = var

    @property
    def temperatura_limite(self) -> "int":
        # PROPRIEDADE -> Retrona o valor de temperaturas limite da Unidade.

        return self._temperatura_limite

    @temperatura_limite.setter
    def temperatura_limite(self, var: "int") -> None:
        # SETTER -> Atrubui o novo valor de temperaturas limite da Unidade.

        self._temperatura_limite = var

    @property
    def condic_dict(self) -> "dict[str, CondicionadorExponencial]":
        # PROPRIEDADE -> Retrona o dicionário de condicionadores da Unidade.

        return self._condic_dict

    @condic_dict.setter
    def condic_dict(self, var: "dict[str, CondicionadorExponencial]") -> None:
        # SETTER -> Atrubui o novo dicionário de condicionadores da Unidade.

        self._condic_dict = var

    @property
    def leitura_dict(self) -> "dict[str, LeituraModbus]":
        # PROPRIEDADE -> Retrona o dicionário de leituras da Unidade.

        return self._leitura_dict

    @leitura_dict.setter
    def leitura_dict(self, var: "dict[str, LeituraModbus]") -> None:
        # SETTER -> Atrubui o novo dicionário de leituras da Unidade.

        self._leitura_dict = var

    @property
    def condicionadores(self) -> "list[CondicionadorBase]":
        # PROPRIEDADE -> Retrona a lista de condicionadores da Unidade.

        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[CondicionadorBase]") -> None:
        # SETTER -> Atrubui a nova lista de condicionadores da Unidade.

        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[CondicionadorBase]":
        # PROPRIEDADE -> Retrona a lista de condicionadores essenciais da Unidade.

        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[CondicionadorBase]") -> None:
        # SETTER -> Atrubui a nova lista de condicionadores essenciais da Unidade.

        self._condicionadores_essenciais = var

    def verificar_condicionadores(self) -> "int":
        """
        Função para a verificação de acionamento de condicionadores e determinação
        de gravidade.

        Itera sobre a lista de condicionadores da Unidade e verifica se algum está
        ativo. Caso esteja, verifica o nível de gravidade e retorna o valor para
        a determinação do passo seguinte.
        Caso não haja nenhum condicionador ativo, apenas retorna o valor de ignorar.
        """

        flag = CONDIC_IGNORAR
        v = []

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condicionadores_ativos = [x for y in [self.condicionadores_essenciais, self.condicionadores] for x in y if x.ativo]

            for condic in condicionadores_ativos:
                if condic.gravidade == CONDIC_NORMALIZAR:
                    flag = CONDIC_NORMALIZAR
                elif condic.gravidade == CONDIC_AGUARDAR:
                    flag = CONDIC_AGUARDAR
                elif condic.gravidade == CONDIC_INDISPONIBILIZAR:
                    flag = CONDIC_INDISPONIBILIZAR

            logger.debug("")
            logger.warning(f"[OCO-UG{self.__ug.id}] Foram detectados condicionadores ativos na UG:")
            [logger.warning(f"[OCO-UG{self.__ug.id}] Descrição: \"{condic.descr}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"") for condic in condicionadores_ativos]
            logger.debug("")

            # for condic in condicionadores_ativos:
            #     v = [datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descr]
            #     self.__db.update_alarmes(v)

            return flag
        return flag

    def atualizar_limites_condicionadores(self, parametros: "dict") -> "None":
        """
        Função para extração de valores do Banco de Dados da Interface WEB e atribuição
        de novos limites de operação de condicionadores.
        """
        try:
            self.condic_dict[f"tmp_fase_r_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_fase_s_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_fase_t_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_nucleo_gerador_1_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_1_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_nucleo_gerador_2_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_2_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_nucleo_gerador_3_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_3_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_casq_rad_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_casq_rad_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_casq_comb_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_casq_comb_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_escora_comb_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_escora_comb_ug{self.__ug.id}"])

            self.condic_dict[f"tmp_fase_s_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_fase_r_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_fase_t_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_nucleo_gerador_1_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_1_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_nucleo_gerador_2_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_2_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_nucleo_gerador_3_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_3_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_casq_rad_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_casq_rad_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_casq_comb_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_casq_comb_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_escora_comb_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_escora_comb_ug{self.__ug.id}"])

        except Exception:
            logger.error(f"[OCO-UG{self.__ug.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores.")
            logger.debug(f"{traceback.format_exc()}")

    def controlar_limites_operacao(self) -> "None":
        """
        Função para verificação de limites de operação da Unidade.

        Verifica os valores base e limite da Unidade, pré-determinados na interface
        WEB, e avisa o operador caso algum valor ultrapasse o estipulado.
        """

        ld = self.leitura_dict
        cd = self.condic_dict

        if ld[f"tmp_fase_r_ug{self.__ug.id}"].valor >= cd[f"tmp_fase_r_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[UG{self.__ug.id}] A temperatura de Fase R da UG passou do valor base! ({cd[f'tmp_fase_r_ug{self.__ug.id}'].valor_base} C) | Leitura: {ld[f'tmp_fase_r_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_fase_r_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_fase_r_ug{self.__ug.id}"].valor_limite - cd[f"tmp_fase_r_ug{self.__ug.id}"].valor_base) + cd[f"tmp_fase_r_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[UG{self.__ug.id}] A temperatura de Fase R da UG está muito próxima do limite! ({cd[f'tmp_fase_r_ug{self.__ug.id}'].valor_limite} C) | Leitura: {ld[f'tmp_fase_r_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_fase_s_ug{self.__ug.id}"].valor >= cd[f"tmp_fase_s_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[UG{self.__ug.id}] A temperatura de Fase S da UG passou do valor base! ({cd[f'tmp_fase_s_ug{self.__ug.id}'].valor_base} C) | Leitura: {ld[f'tmp_fase_s_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_fase_s_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_fase_s_ug{self.__ug.id}"].valor_limite - cd[f"tmp_fase_s_ug{self.__ug.id}"].valor_base) + cd[f"tmp_fase_s_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[UG{self.__ug.id}] A temperatura de Fase S da UG está muito próxima do limite! ({cd[f'tmp_fase_s_ug{self.__ug.id}'].valor_limite} C) | Leitura: {ld[f'tmp_fase_s_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_fase_t_ug{self.__ug.id}"].valor >= cd[f"tmp_fase_t_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[UG{self.__ug.id}] A temperatura de Fase T da UG passou do valor base! ({cd[f'tmp_fase_t_ug{self.__ug.id}'].valor_base} C) | Leitura: {ld[f'tmp_fase_t_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_fase_t_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_fase_t_ug{self.__ug.id}"].valor_limite - cd[f"tmp_fase_t_ug{self.__ug.id}"].valor_base) + cd[f"tmp_fase_t_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[UG{self.__ug.id}] A temperatura de Fase T da UG está muito próxima do limite! ({cd[f'tmp_fase_t_ug{self.__ug.id}'].valor_limite} C) | Leitura: {ld[f'tmp_fase_t_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_nucleo_gerador_1_ug{self.__ug.id}"].valor >= cd[f"tmp_nucleo_gerador_1_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[UG{self.__ug.id}] A temperatura do Núcleo Gerador 1 da UG passou do valor base! ({cd[f'tmp_nucleo_gerador_1_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_nucleo_gerador_1_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_nucleo_gerador_1_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_nucleo_gerador_1_ug{self.__ug.id}"].valor_limite - cd[f"tmp_nucleo_gerador_1_ug{self.__ug.id}"].valor_base) + cd[f"tmp_nucleo_gerador_1_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[UG{self.__ug.id}] A temperatura do Núcleo Gerador 1 da UG está muito próxima do limite! ({cd[f'tmp_nucleo_gerador_1_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_nucleo_gerador_1_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_nucleo_gerador_2_ug{self.__ug.id}"].valor >= cd[f"tmp_nucleo_gerador_2_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[UG{self.__ug.id}] A temperatura do Núcleo Gerador 2 da UG passou do valor base! ({cd[f'tmp_nucleo_gerador_2_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_nucleo_gerador_2_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_nucleo_gerador_2_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_nucleo_gerador_2_ug{self.__ug.id}"].valor_limite - cd[f"tmp_nucleo_gerador_2_ug{self.__ug.id}"].valor_base) + cd[f"tmp_nucleo_gerador_2_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[UG{self.__ug.id}] A temperatura do Núcleo Gerador 2 da UG está muito próxima do limite! ({cd[f'tmp_nucleo_gerador_2_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_nucleo_gerador_2_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_nucleo_gerador_3_ug{self.__ug.id}"].valor >= cd[f"tmp_nucleo_gerador_3_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[UG{self.__ug.id}] A temperatura do Núcleo Gerador 3 da UG passou do valor base! ({cd[f'tmp_nucleo_gerador_3_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_nucleo_gerador_3_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_nucleo_gerador_3_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_nucleo_gerador_3_ug{self.__ug.id}"].valor_limite - cd[f"tmp_nucleo_gerador_3_ug{self.__ug.id}"].valor_base) + cd[f"tmp_nucleo_gerador_3_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[UG{self.__ug.id}] A temperatura do Núcleo Gerador 3 da UG está muito próxima do limite! ({cd[f'tmp_nucleo_gerador_3_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_nucleo_gerador_3_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_casq_rad_ug{self.__ug.id}"].valor >= cd[f"tmp_mancal_casq_rad_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[UG{self.__ug.id}] A temperatura do Mancal Casquilho Radial da UG passou do valor base! ({cd[f'tmp_mancal_casq_rad_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_mancal_casq_rad_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_casq_rad_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_mancal_casq_rad_ug{self.__ug.id}"].valor_limite - cd[f"tmp_mancal_casq_rad_ug{self.__ug.id}"].valor_base) + cd[f"tmp_mancal_casq_rad_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[UG{self.__ug.id}] A temperatura do Mancal Casquilho Radial da UG está muito próxima do limite! ({cd[f'tmp_mancal_casq_rad_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_mancal_casq_rad_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_casq_comb_ug{self.__ug.id}"].valor >= cd[f"tmp_mancal_casq_comb_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[UG{self.__ug.id}] A temperatura do Mancal Casquilho Combinado da UG passou do valor base! ({cd[f'tmp_mancal_casq_comb_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_mancal_casq_comb_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_casq_comb_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_mancal_casq_comb_ug{self.__ug.id}"].valor_limite - cd[f"tmp_mancal_casq_comb_ug{self.__ug.id}"].valor_base) + cd[f"tmp_mancal_casq_comb_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[UG{self.__ug.id}] A temperatura do Mancal Casquilho Combinado da UG está muito próxima do limite! ({cd[f'tmp_mancal_casq_comb_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_mancal_casq_comb_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_escora_comb_ug{self.__ug.id}"].valor >= cd[f"tmp_mancal_escora_comb_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[UG{self.__ug.id}] A temperatura do Mancal Escora Combinado da UG passou do valor base! ({cd[f'tmp_mancal_escora_comb_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_mancal_escora_comb_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_escora_comb_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_mancal_escora_comb_ug{self.__ug.id}"].valor_limite - cd[f"tmp_mancal_escora_comb_ug{self.__ug.id}"].valor_base) + cd[f"tmp_mancal_escora_comb_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[UG{self.__ug.id}] A temperatura do Mancal Escora Combinado da UG está muito próxima do limite! ({cd[f'tmp_mancal_escora_comb_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_mancal_escora_comb_ug{self.__ug.id}'].valor} C")

    def verificar_leituras(self) -> "None":
        """
        Função para consulta de acionamentos da Unidade e avisos através do mecanismo
        de acionamento temporizado.
        """

        # WHATSAPP
        if self.leitura_rt_selec_modo_controle_isol.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o comando no RT de seleção de modo de controle isolado, favor verificar.")

        if self.leitura_alarme_rele.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma leitura de alarme do relé, favor verificar.")

        if self.leitura_rv_alarme.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma leitura de alarme do RV, favor verificar.")

        if self.leitura_rv_pot_nula.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma leitura de potência nula no RV, favor verificar.")

        if self.leitura_rt_alarme.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma leitura de alarme no RT, favor verificar.")

        if self.leitura_dispo_prot_surto.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma leitura do dispositivo de proteção de surto, favor verificar.")

        if self.leitura_uhrv_bomba_defeito.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado um defeito na bomba da UHRV, favor verificar.")

        if self.leitura_uhlm_bomba_defeito.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado um defeito na bomba da UHLM, favor verificar.")

        if self.leitura_resis_aquec_gerad_defeito.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado um defeito com a resistência do aquecedor do Gerador, favor verificar.")

        if self.leitura_tristores_temp_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura de Tristores está alta, favor verificar.")

        if self.leitura_crowbar_temp_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Crowbar está alta, favor verificar.")

        if self.leitura_trafo_exci_temp_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Transformador de Excitação está alta, favor verificar.")

        if self.leitura_uhrv_oleo_temp_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Óleo da UHRV está alta, favor verificar.")

        if self.leitura_gerad_fase_a_temp_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura de Fase A do Gerador está alta, favor verificar.")

        if self.leitura_gerad_fase_b_temp_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura de Fase B do Gerador está alta, favor verificar.")

        if self.leitura_gerad_fase_c_temp_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura de Fase C do Gerador está alta, favor verificar.")

        if self.leitura_gerad_nucleo_1_temp_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Núcleo 1 do Gerador está alta, favor verificar.")

        if self.leitura_gerad_nucleo_2_temp_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Núcleo 2 do Gerador está alta, favor verificar.")

        if self.leitura_gerad_nucleo_3_temp_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Núcleo 3 do Gerador está alta, favor verificar.")

        if self.leitura_mancal_guia_casq_temp_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Mancal Guia Casquilho está alta, favor verificar.")

        if self.leitura_mancal_comb_casq_temp_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Mancal Combinado Casquilho está alta, favor verificar.")

        if self.leitura_mancal_comb_esc_temp_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Mancal Combinado Escora está alta, favor verificar.")

        if self.leitura_falha_leit_nv_jusante.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura do Nível Jusante, favor verificar.")

        if self.leitura_sinal_nv_jusante_muito_alto.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que o Nível Jusante está muito alto, favor verificar.")

        if self.leitura_sinal_nv_jusante_alto.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que o Nível Jusante está alto, favor verificar.")

        if self.leitura_uhrv_pressao_oleo_baixa.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a pressão do óleo da UHRV está baixa, favor verificar.")

        if self.leitura_sinal_nv_jusante_baixo.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que o Nível Jusante está baixo, favor verificar.")

        if self.leitura_uhrv_pressao_oleo_muito_baixa.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a pressão do óleo da UHRV está muito baixa, favor verificar.")

        if self.leitura_sinal_nv_jusante_muito_baixo.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que o Nível Jusante está muito baixo, favor verificar.")

        if self.leitura_alarme_contro_dif_grade.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma leitura de alarme do controle de diferencial de grade, favor verificar.")

        if self.leitura_resis_aquec_gerad_indisp.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a resistência do aquecedor do gerador está indisponível, favor verificar.")

        if self.leitura_uhlm_unidade_manut.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a UHLM entrou em modo de manutenção, favor verificar.")

        if self.leitura_rv_modo_manut.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que o RV entrou em modo de manutenção, favor verificar.")

        if self.leitura_rv_girando_gir_indev.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que o Rv está girando com giro indevido, favor verificar.")

        if self.leitura_rt_alar_1_sobretensao.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 de sobretensão do RT, favor verificar.")

        if self.leitura_rt_alar_1_subtensao.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 de subtensão do RT, favor verificar.")

        if self.leitura_rt_alar_1_sobrefrequencia.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 de sobrefrequência do RT, favor verificar.")

        if self.leitura_rt_alar_1_subfrequencia.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 de subfrequência do RT, favor verificar.")

        if self.leitura_rt_alar_1_lim_sup_pot_reativa.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 limite superior de potência reativa do RT, favor verificar.")

        if self.leitura_rt_alar_1_lim_inf_pot_reativa.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 limite inferior de potência reativa do RT, favor verificar.")

        if self.leitura_rt_alar_1_lim_sup_fator_pot.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 limite superior de fator de potência do RT, favor verificar.")

        if self.leitura_rt_alar_1_lim_inf_fator_pot.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 limite inferior de fator de potência do RT, favor verificar.")

        if self.leitura_rt_alar_1_variacao_tensao.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 variação de tensao do RT, favor verificar.")

        if self.leitura_rt_alar_1_pot_ativa_reversa.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 potência ativa reversa do RT, favor verificar.")

        if self.leitura_rt_alar_1_sobrecorr_term.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 sobrecorrente terminal do RT, favor verificar.")

        if self.leitura_rt_alar_1_lim_sup_corr_excitacao.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 limite superior corrente de excitação do RT, favor verificar.")

        if self.leitura_rt_alar_1_lim_inf_corr_exci.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 limite inferior corrente de excitação do RT, favor verificar.")

        if self.leitura_rt_alar_1_temp_muito_alta_rotor.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 temperatura muito alta do rotor do RT, favor verificar.")

        if self.leitura_rt_alar_1_pres_tens_term_aus_corr_exci.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 presença de tensão terminal e ausência de corrente de excitação no RT, favor verificar.")

        if self.leitura_rt_alar_1_pres_corr_exci_aus_tens_term.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 1 presença de corrente de excitação e ausenência de tensão terminal no RT, favor verificar.")

        if self.leitura_rt_alar_2_falha_contro_corr_exci.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 2 falha de controle de corrente de excitação do RT, favor verificar.")

        if self.leitura_rt_alar_2_falha_contro_tens_term.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do alarme 2 falha de controle de tensão terminal do RT, favor verificar.")

        if self.leitura_uhrv_oleo_nv_muito_baixo.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que o óleo da UHRV está com o nível muito baixo, favor verificar.")

        if self.leitura_uhrv_filtro_oleo_sujo.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que o filtro de óleo da UHRV está sujo, favor verificar.")

        if self.leitura_urhv_press_crit.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a pressão da UHRV está em nível crítico, favor verificar.")

        if self.leitura_uhrv_oleo_nv_muito_alto.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que o óleo da UHRV está com o nível muito alto, favor verificar.")

        if self.leitura_uhlm_oleo_nv_muito_baixo.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que o óleo da UHLM está com o nível muito baixo, favor verificar.")

        if self.leitura_uhlm_press_linha_lubrifi.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado a falta de pressão de lubrificação de linha da UHLM, favor verificar.")

        if self.leitura_uhlm_fluxo_troc_calor.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado a falta de fluxo do trocador de calor da UHLM, favor verificar.")

        if self.leitura_qbag_escova_polo_pos_desgas.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a escova do polo positivo QBAG está desgastada, favor verificar.")

        if self.leitura_qbag_escova_polo_neg_desgas.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a escova do polo negativo QBAG está desgastada, favor verificar.")

        if self.leitura_tristor_temp_muito_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura de Tristores está muito alta, favor verificar.")

        if self.leitura_crowbar_temp_muito_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Crowbar está muito alta, favor verificar.")

        if self.leitura_trafo_exci_temp_muito_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Transformado de excitação está muito alta, favor verificar.")

        if self.leitura_uhrv_temp_oleo_muito_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do óleo da UHRV está muito alta, favor verificar.")

        if self.leitura_gera_fase_a_temp_muito_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura de Fase A do Gerador está muito alta, favor verificar.")

        if self.leitura_gera_fase_b_temp_muito_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura de Fase B do Gerador está muito alta, favor verificar.")

        if self.leitura_gera_fase_c_temp_muito_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura de Fase C do Gerador está muito alta, favor verificar.")

        if self.leitura_gera_nucleo_1_temp_muito_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Núcleo 1 do Gerador está muito alta, favor verificar.")

        if self.leitura_gera_nucleo_2_temp_muito_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Núcleo 2 do Gerador está muito alta, favor verificar.")

        if self.leitura_gera_nucleo_3_temp_muito_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Núcleo 3 do Gerador está muito alta, favor verificar.")

        if self.leitura_mancal_guia_casq_temp_muito_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Mancal Guia Casquilho está muito alta, favor verificar.")

        if self.leitura_mancal_comb_casq_temp_muito_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Mancal Combinado Casquilho está muito alta, favor verificar.")

        if self.leitura_mancal_comb_esc_temp_muito_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a temperatura do Mancal Combinado Escora está muito alta, favor verificar.")

        if self.leitura_uhrv_press_oleo_falha_leitura.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura de pressão do óleo da UHRV, favor verificar.")

        if self.leitura_uhrv_press_oleo_muito_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a pressão do óleo da UHRV está muito alta, favor verificar.")

        if self.leitura_uhrv_press_oleo_alta.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado que a pressão do óleo da UHRV está alta, favor verificar.")

        if self.leitura_contro_trip_dif_grade.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado um acionamento de Trip do Controle de Diferencial de Grade, favor verificar.")

        if self.leitura_resis_aquec_gera_falha_deslig.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha no desligamento da resistência do aquecedor do gerador, favor verificar.")

        if self.leitura_uhlm_bomba_1_falha_ligar.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha ao ligar a Bomba 1 da UHLM, favor verificar.")

        if self.leitura_uhlm_bomba_1_falha_deslig.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha no desligamento da Bomba 1 da UHLM, favor verificar.")

        if self.leitura_ulhm_falha_pressos.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha no pressostato da UHLM, favor verificar.")

        if self.leitura_rv_falha_partir.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha ao partir o RV, favor verificar.")

        if self.leitura_rv_falha_desab.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha ao desabilitar o RV, favor verificar.")

        if self.leitura_rv_falha_parar_maqu.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha ao parar a máquina pelo RV, favor verificar.")

        if self.leitura_rt_falha_partir.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha ao partir a máquina pelo RT, favor verificar.")

        if self.leitura_rt_falha_desab.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha ao desabilitar o RT, favor verificar.")

        if self.leitura_valv_borb_falha_fechar.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha no fechamento da válvula borboleta, favor verificar.")

        if self.leitura_valv_borb_dicrep_senso.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma discrepância no sensor da válvula borboleta, favor verificar.")

        if self.leitura_vavl_bypass_discrep_senso.valor:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma discrepância no sensor da válvula bypass, favor verificar.")


        # WHATSAPP + VOIP
        if self.leitura_val_bypass_falha_abrir.valor and not d.voip[f"UG{self.__ug.id}_ED_BYPASS_FALHA_ABRIR"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha ao abrir a Válvula Bypass, favor verificar.")
            d.voip[f"UG{self.__ug.id}_ED_BYPASS_FALHA_ABRIR"][0] = True
        elif not self.leitura_val_bypass_falha_abrir.valor and d.voip[f"UG{self.__ug.id}_ED_BYPASS_FALHA_ABRIR"][0]:
            d.voip[f"UG{self.__ug.id}_ED_BYPASS_FALHA_ABRIR"][0] = False

        if self.leitura_val_bypass_falha_fechar.valor and not d.voip[f"UG{self.__ug.id}_ED_BYPASS_FALHA_FECHAR"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha ao fechar a Válvula Bypass, favor verificar.")
            d.voip[f"UG{self.__ug.id}_ED_BYPASS_FALHA_FECHAR"][0] = True
        elif not self.leitura_val_bypass_falha_fechar.valor and d.voip[f"UG{self.__ug.id}_ED_BYPASS_FALHA_FECHAR"][0]:
            d.voip[f"UG{self.__ug.id}_ED_BYPASS_FALHA_FECHAR"][0] = False

        if self.leitura_falha_fechar_distrib.valor and not d.voip[f"UG{self.__ug.id}_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha ao fechar o Distribuidor, favor verificar.")
            d.voip[f"UG{self.__ug.id}_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR"][0] = True
        elif not self.leitura_falha_fechar_distrib.valor and d.voip[f"UG{self.__ug.id}_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR"][0]:
            d.voip[f"UG{self.__ug.id}_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR"][0] = False

        if self.leitura_cmd_uhrv_modo_manuten.valor and not d.voip[f"UG{self.__ug.id}_CD_CMD_UHRV_MODO_MANUTENCAO"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do comando do modo de manutenção da UHRV, favor verificar.")
            d.voip[f"UG{self.__ug.id}_CD_CMD_UHRV_MODO_MANUTENCAO"][0] = True
        elif not self.leitura_cmd_uhrv_modo_manuten.valor and d.voip[f"UG{self.__ug.id}_CD_CMD_UHRV_MODO_MANUTENCAO"][0]:
            d.voip[f"UG{self.__ug.id}_CD_CMD_UHRV_MODO_MANUTENCAO"][0] = False

        if self.leitura_cmd_uhlm_modo_manuten.valor and not d.voip[f"UG{self.__ug.id}_CD_CMD_UHLM_MODO_MANUTENCAO"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado o acionamento do comando do modo de manutenção da UHLM, favor verificar.")
            d.voip[f"UG{self.__ug.id}_CD_CMD_UHLM_MODO_MANUTENCAO"][0] = True
        elif not self.leitura_cmd_uhlm_modo_manuten.valor and d.voip[f"UG{self.__ug.id}_CD_CMD_UHLM_MODO_MANUTENCAO"][0]:
            d.voip[f"UG{self.__ug.id}_CD_CMD_UHLM_MODO_MANUTENCAO"][0] = False

        if self.leitura_falha_leit_temp_tristores.valor and not d.voip[f"UG{self.__ug.id}_EA_TRISTORES_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura de temperatura de Tristores, favor verificar.")
            d.voip[f"UG{self.__ug.id}_EA_TRISTORES_TEMP_FALHA_LEITURA"][0] = True
        elif not self.leitura_falha_leit_temp_tristores.valor and d.voip[f"UG{self.__ug.id}_EA_TRISTORES_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.__ug.id}_EA_TRISTORES_TEMP_FALHA_LEITURA"][0] = False

        if self.leitura_falha_leit_temp_crowbar.valor and not d.voip[f"UG{self.__ug.id}_EA_CROWBAR_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura de temperatura do Crowbar, favor verificar.")
            d.voip[f"UG{self.__ug.id}_EA_CROWBAR_TEMP_FALHA_LEITURA"][0] = True
        elif not self.leitura_falha_leit_temp_crowbar.valor and d.voip[f"UG{self.__ug.id}_EA_CROWBAR_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.__ug.id}_EA_CROWBAR_TEMP_FALHA_LEITURA"][0] = False

        if self.leitura_falha_leit_temp_trafo_exci.valor and not d.voip[f"UG{self.__ug.id}_EA_TRAFO_EXCITACAO_FALHA_LEITURA"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura de temperatura do Transformador de Excitação, favor verificar.")
            d.voip[f"UG{self.__ug.id}_EA_TRAFO_EXCITACAO_FALHA_LEITURA"][0] = True
        elif not self.leitura_falha_leit_temp_trafo_exci.valor and d.voip[f"UG{self.__ug.id}_EA_TRAFO_EXCITACAO_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.__ug.id}_EA_TRAFO_EXCITACAO_FALHA_LEITURA"][0] = False

        if self.leitura_falha_leit_temp_uhrv_temp_oleo.valor and not d.voip[f"UG{self.__ug.id}_EA_UHRV_TEMP_OLEO_FALHA_LEITURA"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura de temperatura do Óleo da UHRV, favor verificar.")
            d.voip[f"UG{self.__ug.id}_EA_UHRV_TEMP_OLEO_FALHA_LEITURA"][0] = True
        elif not self.leitura_falha_leit_temp_uhrv_temp_oleo.valor and d.voip[f"UG{self.__ug.id}_EA_UHRV_TEMP_OLEO_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.__ug.id}_EA_UHRV_TEMP_OLEO_FALHA_LEITURA"][0] = False

        if self.leitura_falha_leit_temp_gerad_fase_a.valor and not d.voip[f"UG{self.__ug.id}_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura de temperatura de Fase A do gerador, favor verificar.")
            d.voip[f"UG{self.__ug.id}_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA"][0] = True
        elif not self.leitura_falha_leit_temp_gerad_fase_a.valor and d.voip[f"UG{self.__ug.id}_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.__ug.id}_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA"][0] = False

        if self.leitura_falha_leit_temp_gerad_fase_b.valor and not d.voip[f"UG{self.__ug.id}_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura de temperatura de Fase B do gerador, favor verificar.")
            d.voip[f"UG{self.__ug.id}_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA"][0] = True
        elif not self.leitura_falha_leit_temp_gerad_fase_b.valor and d.voip[f"UG{self.__ug.id}_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.__ug.id}_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA"][0] = False

        if self.leitura_falha_leit_temp_gerad_fase_c.valor and not d.voip[f"UG{self.__ug.id}_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura de temperatura de Fase C do gerador, favor verificar.")
            d.voip[f"UG{self.__ug.id}_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA"][0] = True
        elif not self.leitura_falha_leit_temp_gerad_fase_c.valor and d.voip[f"UG{self.__ug.id}_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.__ug.id}_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA"][0] = False

        if self.leitura_falha_leit_temp_gerad_nucleo_1.valor and not d.voip[f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura de temperatura do Núcleo 1 do Gerador, favor verificar.")
            d.voip[f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA"][0] = True
        elif not self.leitura_falha_leit_temp_gerad_nucleo_1.valor and d.voip[f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA"][0] = False

        if self.leitura_falha_leit_temp_gerad_nucleo_2.valor and not d.voip[f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_2_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura de temperatura do Núcleo 2 do Gerador, favor verificar.")
            d.voip[f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_2_FALHA_LEITURA"][0] = True
        elif not self.leitura_falha_leit_temp_gerad_nucleo_2.valor and d.voip[f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_2_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_2_FALHA_LEITURA"][0] = False

        if self.leitura_falha_leit_temp_gerad_nucleo_3.valor and not d.voip[f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura de temperatura do Núcleo 3 do Gerador, favor verificar.")
            d.voip[f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA"][0] = True
        elif not self.leitura_falha_leit_temp_gerad_nucleo_3.valor and d.voip[f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA"][0] = False

        if self.leitura_falha_leit_temp_mancal_guia_casq.valor and not d.voip[f"UG{self.__ug.id}_EA_MANCAL_GUIA_CASQUILHO_FALHA_LEITURA"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura de temperatura do Mancal Guia Casquilho, favor verificar.")
            d.voip[f"UG{self.__ug.id}_EA_MANCAL_GUIA_CASQUILHO_FALHA_LEITURA"][0] = True
        elif not self.leitura_falha_leit_temp_mancal_guia_casq.valor and d.voip[f"UG{self.__ug.id}_EA_MANCAL_GUIA_CASQUILHO_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.__ug.id}_EA_MANCAL_GUIA_CASQUILHO_FALHA_LEITURA"][0] = False

        if self.leitura_falha_leit_temp_mancal_comb_casq.valor and not d.voip[f"UG{self.__ug.id}_EA_MANCAL_COMBINADO_CASQUILHO_FALHA_LEITURA"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura de temperatura do Mancal Combinado Casquilho, favor verificar.")
            d.voip[f"UG{self.__ug.id}_EA_MANCAL_COMBINADO_CASQUILHO_FALHA_LEITURA"][0] = True
        elif not self.leitura_falha_leit_temp_mancal_comb_casq.valor and d.voip[f"UG{self.__ug.id}_EA_MANCAL_COMBINADO_CASQUILHO_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.__ug.id}_EA_MANCAL_COMBINADO_CASQUILHO_FALHA_LEITURA"][0] = False

        if self.leitura_falha_leit_temp_mancal_comb_esc.valor and not d.voip[f"UG{self.__ug.id}_EA_MANCAL_COMBINADO_ESCORA_FALHA_LEITURA"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha na leitura de temperatura do Mancal Combinado Escora, favor verificar.")
            d.voip[f"UG{self.__ug.id}_EA_MANCAL_COMBINADO_ESCORA_FALHA_LEITURA"][0] = True
        elif not self.leitura_falha_leit_temp_mancal_comb_esc.valor and d.voip[f"UG{self.__ug.id}_EA_MANCAL_COMBINADO_ESCORA_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.__ug.id}_EA_MANCAL_COMBINADO_ESCORA_FALHA_LEITURA"][0] = False

        if self.leitura_resis_quec_gerador_falha_ligar.valor and not d.voip[f"UG{self.__ug.id}_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR"][0]:
            logger.warning(f"[OCO-UG{self.__ug.id}] Foi identificado uma falha ao ligar a resistência do aquecedor do gerador, favor verificar.")
            d.voip[f"UG{self.__ug.id}_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR"][0] = True
        elif not self.leitura_resis_quec_gerador_falha_ligar.valor and d.voip[f"UG{self.__ug.id}_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR"][0]:
            d.voip[f"UG{self.__ug.id}_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR"][0] = False

        return

    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Unidade.
        """

        # Fase R
        self.leitura_dict[f"tmp_fase_r_ug{self.__ug.id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug.id}"],
            REG_UG[f"UG{self.__ug.id}_EA_TEMPERATURA_GERADOR_FASE_A"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_fase_r_ug{self.__ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_fase_r_ug{self.__ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_r_ug{self.__ug.id}"])

        # Fase S
        self.leitura_dict[f"tmp_fase_s_ug{self.__ug.id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug.id}"],
            REG_UG[f"UG{self.__ug.id}_EA_TEMPERATURA_GERADOR_FASE_B"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_fase_s_ug{self.__ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_fase_s_ug{self.__ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_s_ug{self.__ug.id}"])

        # Fase T
        self.leitura_dict[f"tmp_fase_t_ug{self.__ug.id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug.id}"],
            REG_UG[f"UG{self.__ug.id}_EA_TEMPERATURA_GERADOR_FASE_C"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_fase_t_ug{self.__ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_fase_t_ug{self.__ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_t_ug{self.__ug.id}"])

        # Nucleo Gerador 1
        self.leitura_dict[f"tmp_nucleo_gerador_1_ug{self.__ug.id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug.id}"],
            REG_UG[f"UG{self.__ug.id}_EA_TEMPERATURA_GERADOR_NUCLEO_1"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_nucleo_gerador_1_ug{self.__ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_nucleo_gerador_1_ug{self.__ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_nucleo_gerador_1_ug{self.__ug.id}"])

        # Nucleo Gerador 2
        self.leitura_dict[f"tmp_nucleo_gerador_2_ug{self.__ug.id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug.id}"],
            REG_UG[f"UG{self.__ug.id}_EA_TEMPERATURA_GERADOR_NUCLEO_2"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_nucleo_gerador_2_ug{self.__ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_nucleo_gerador_2_ug{self.__ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_nucleo_gerador_2_ug{self.__ug.id}"])

        # Nucleo Gerador 3
        self.leitura_dict[f"tmp_nucleo_gerador_3_ug{self.__ug.id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug.id}"],
            REG_UG[f"UG{self.__ug.id}_EA_TEMPERATURA_GERADOR_NUCLEO_3"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_nucleo_gerador_3_ug{self.__ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_nucleo_gerador_3_ug{self.__ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_nucleo_gerador_3_ug{self.__ug.id}"])

        # Mancal Casquilho Radial
        self.leitura_dict[f"tmp_mancal_casq_rad_ug{self.__ug.id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug.id}"],
            REG_UG[f"UG{self.__ug.id}_EA_TEMPERATURA_MANCAL_GUIA_CASQUILHO"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_mancal_casq_rad_ug{self.__ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_mancal_casq_rad_ug{self.__ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_casq_rad_ug{self.__ug.id}"])

        # Mancal Casquilho Combinado
        self.leitura_dict[f"tmp_mancal_casq_comb_ug{self.__ug.id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug.id}"],
            REG_UG[f"UG{self.__ug.id}_EA_TEMPERATURA_MANCAL_COMBINADO_CASQUILHO"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_mancal_casq_comb_ug{self.__ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_mancal_casq_comb_ug{self.__ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_casq_comb_ug{self.__ug.id}"])

        # Mancal Escora Combinado
        self.leitura_dict[f"tmp_mancal_escora_comb_ug{self.__ug.id}"] = LeituraModbus(
            self.__clp[f"UG{self.__ug.id}"],
            REG_UG[f"UG{self.__ug.id}_EA_TEMPERATURA_MANCAL_COMBINADO_ESCORA"],
            escala=0.001,
            op=4
        )
        self.condic_dict[f"tmp_mancal_escora_comb_ug{self.__ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"tmp_mancal_escora_comb_ug{self.__ug.id}"]
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_escora_comb_ug{self.__ug.id}"])


        # Leituras de condicionadores essenciais que serão lidos a cada ciclo das UGs
        ## CONDICINOADORES ESSENCIAIS GERAIS
        self.leitura_rele_bloq_86eh = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_RELE_BLOQUEIO_86EH"], descr=f"[UG{self.__ug.id}] Relé Bloqueio 86EH")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_bloq_86eh, CONDIC_NORMALIZAR))

        self.leitura_bloq_86e = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_STT_BLOQUEIO_86E"], descr=f"[UG{self.__ug.id}] Bloqueio 86E")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_bloq_86e, CONDIC_NORMALIZAR))

        self.leitura_bloq_86h = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_STT_BLOQUEIO_86H"], descr=f"[UG{self.__ug.id}] Bloqueio 86H")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_bloq_86h, CONDIC_NORMALIZAR))

        self.leitura_status_bloq_86m = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_STT_BLOQUEIO_86M"], descr=f"[UG{self.__ug.id}] Status Bloqueio 86M")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_status_bloq_86m, CONDIC_NORMALIZAR))

        self.leitura_rt_falha_2_bloq_externo = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_2_BLOQ_EXTERNO"], descr=f"[UG{self.__ug.id}] RT Falha 2 Bloqueio Externo")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rt_falha_2_bloq_externo, CONDIC_NORMALIZAR))

        self.leitura_rele_trip_prot_gerad = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_RELE_PROT_GERADOR_TRIP"], descr=f"[UG{self.__ug.id}] Relé Trip Proteção Gerador")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_trip_prot_gerad, CONDIC_NORMALIZAR))

        self.leitura_rv_trip = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_RV_TRIP"], descr=f"[UG{self.__ug.id}] RV Trip")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rv_trip, CONDIC_NORMALIZAR))

        self.leitura_rt_trip = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_RT_TRIP"], descr=f"[UG{self.__ug.id}] RT Trip")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rt_trip, CONDIC_NORMALIZAR))


        ## CONDICIONADORES NORMALIZAR
        self.leitura_val_bypass_falha_abrir = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_BYPASS_FALHA_ABRIR"], descr=f"[UG{self.__ug.id}] Válvula Bypass Falha Abrir")
        self.condicionadores.append(CondicionadorBase(self.leitura_val_bypass_falha_abrir, CONDIC_NORMALIZAR))

        self.leitura_val_bypass_falha_fechar = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_BYPASS_FALHA_FECHAR"], descr=f"[UG{self.__ug.id}] Válvula Bypass Falha Fechar")
        self.condicionadores.append(CondicionadorBase(self.leitura_val_bypass_falha_fechar, CONDIC_NORMALIZAR))

        self.leitura_rv_alarme_sobrefrequncia = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_ALARME_SOBREFREQUENCIA"], descr=f"[UG{self.__ug.id}] RV Alarme Sobrefrequência")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_alarme_sobrefrequncia, CONDIC_NORMALIZAR))

        self.leitura_rv_alarme_subfrequencia = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_ALARME_SUBFREQUENCIA"], descr=f"[UG{self.__ug.id}] RV Alarme Subfrequência")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_alarme_subfrequencia, CONDIC_NORMALIZAR))

        self.leitura_rv_falha_1 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_1"], descr=f"[UG{self.__ug.id}] RV Falha 1")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_1, CONDIC_NORMALIZAR))

        # TODO -> Verificar
        # self.leitura_botao_bloq_86eh = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_BOTAO_BLOQUEIO_86EH"], descr=f"[UG{self.__ug.id}] Botão Bloqueio 86EH")
        # self.condicionadores.append(CondicionadorBase(self.leitura_botao_bloq_86eh, CONDIC_NORMALIZAR))

        self.leitura_valv_borb_falha_abertura = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_BROBOLETA_FALHA_ABRIR"], descr=f"[UG{self.__ug.id}] Válvula Borboleta Falha Abertura")
        self.condicionadores.append(CondicionadorBase(self.leitura_valv_borb_falha_abertura, CONDIC_NORMALIZAR))


        # ## CONDICIONADORES INDISPONIBILIZAR
        # ENTRADAS DIGITAIS
        self.leitura_status_rv = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_STT_RV"], descr=f"[UG{self.__ug.id}] RV Status")
        self.condicionadores.append(CondicionadorBase(self.leitura_status_rv, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_fechar_distrib = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR"], descr=f"[UG{self.__ug.id}] Falha Fechamento Distribuidor")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_fechar_distrib, CONDIC_INDISPONIBILIZAR))

        self.leitura_contro_trip_dif_grade = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_CONTROLE_TRIP_DIFERENCIAL_GRADE"], descr=f"[UG{self.__ug.id}] Contorle Trip Diferencial Grade")
        self.condicionadores.append(CondicionadorBase(self.leitura_contro_trip_dif_grade, CONDIC_INDISPONIBILIZAR))

        self.leitura_resis_aquec_gera_falha_deslig = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_DESLIGAR"], descr=f"[UG{self.__ug.id}] Resistência Aquecedor Gerador Falha Desligar")
        self.condicionadores.append(CondicionadorBase(self.leitura_resis_aquec_gera_falha_deslig, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_partir = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_RV_FALHA_AO_PARTIR"], descr=f"[UG{self.__ug.id}] RV Falha Partir")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_partir, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_desab = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_RV_FALHA_AO_DESABILITAR"], descr=f"[UG{self.__ug.id}] RV Falha Desabilitar")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_desab, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_parar_maqu = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_RV_FALHA_AO_PARAR_MAQUINA"], descr=f"[UG{self.__ug.id}] RV Falha Parar Máquina")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_parar_maqu, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_partir = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_RT_FALHA_AO_PARTIR"], descr=f"[UG{self.__ug.id}] RT Falha Partir")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_partir, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_desab = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_RT_FALHA_AO_DESABILITAR"], descr=f"[UG{self.__ug.id}] RT Falha Desabilitar")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_desab, CONDIC_INDISPONIBILIZAR))

        self.leitura_valv_borb_falha_fechar = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_BORBOLETA_FALHA_FECHAR"], descr=f"[UG{self.__ug.id}] Válvula Borboleta Falha Fechar")
        self.condicionadores.append(CondicionadorBase(self.leitura_valv_borb_falha_fechar, CONDIC_INDISPONIBILIZAR))

        self.leitura_valv_borb_dicrep_senso = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_BORBOLETA_DISCREPANCIA_SENSORES"], descr=f"[UG{self.__ug.id}] Válvula Borboleta Discrepância Sensores")
        self.condicionadores.append(CondicionadorBase(self.leitura_valv_borb_dicrep_senso, CONDIC_INDISPONIBILIZAR))

        self.leitura_vavl_bypass_discrep_senso = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_BYPASS_DISCREPANCIA_SENSORES"], descr=f"[UG{self.__ug.id}] Válvula Bypass Discrepância Sensores")
        self.condicionadores.append(CondicionadorBase(self.leitura_vavl_bypass_discrep_senso, CONDIC_INDISPONIBILIZAR))

        # UG_STT_ENTRADAS_DIGITAIS
        self.leitura_uhrv_oleo_nv_muito_baixo = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_UHRV_OLEO_NIVEL_MUITO_BAIXO"], descr=f"[UG{self.__ug.id}] UHRV Óleo Nível Muito Baixo")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhrv_oleo_nv_muito_baixo, CONDIC_INDISPONIBILIZAR))

        self.leitura_uhrv_filtro_oleo_sujo = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_UHRV_FILTRO_OLEO_SUJO"], descr=f"[UG{self.__ug.id}] UHRV Filtro Óleo Sujo")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhrv_filtro_oleo_sujo, CONDIC_INDISPONIBILIZAR))

        self.leitura_urhv_press_crit = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_UHRV_PRESSAO_CRITICA"], descr=f"[UG{self.__ug.id}] UHRV Pressão Crítica")
        self.condicionadores.append(CondicionadorBase(self.leitura_urhv_press_crit, CONDIC_INDISPONIBILIZAR))

        self.leitura_uhrv_oleo_nv_muito_alto = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_UHLM_OLEO_NIVEL_MUITO_ALTO"], descr=f"[UG{self.__ug.id}] UHRV Óleo Nível Muito Alto")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhrv_oleo_nv_muito_alto, CONDIC_INDISPONIBILIZAR))

        self.leitura_uhlm_oleo_nv_muito_baixo = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_UHLM_OLEO_NIVEL_MUITO_BAIXO"], descr=f"[UG{self.__ug.id}] UHLM Óleo Nível Muito Baixo")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhlm_oleo_nv_muito_baixo, CONDIC_INDISPONIBILIZAR))

        # TODO -> Verificar
        self.leitura_uhlm_press_linha_lubrifi = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_UHLM_PRESSAO_LINHA_LUBRIFICACAO"], descr=f"[UG{self.__ug.id}] UHLM Pressão Linha Lubrificação")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhlm_press_linha_lubrifi, CONDIC_NORMALIZAR))

        # TODO n-> Verificar
        self.leitura_uhlm_fluxo_troc_calor = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_UHLM_FLUXO_TROCADOR_CALOR"], descr=f"[UG{self.__ug.id}] UHLM Fluxo Trocador Calor")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhlm_fluxo_troc_calor, CONDIC_NORMALIZAR))

        # TODO -> Verificar
        self.leitura_qbag_escova_polo_pos_desgas = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_QBAG_ESCOVA_POLO_POSITIVO_DESGASTADA"], descr=f"[UG{self.__ug.id}] QBAG Escova Polo Positivo Desgastada")
        self.condicionadores.append(CondicionadorBase(self.leitura_qbag_escova_polo_pos_desgas, CONDIC_INDISPONIBILIZAR))

        self.leitura_qbag_escova_polo_neg_desgas = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_QBAG_ESCOVA_POLO_NEGATIVO_DESGASTADA"], descr=f"[UG{self.__ug.id}] QBAG Escova Polo Negativo Desgastada")
        self.condicionadores.append(CondicionadorBase(self.leitura_qbag_escova_polo_neg_desgas, CONDIC_INDISPONIBILIZAR))

        self.leitura_rele_prot_gerad_50bf = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_RELE_PROT_GERADOR_50BF"], descr=f"[UG{self.__ug.id}] Relé Proteção Gerador 50BF")
        self.condicionadores.append(CondicionadorBase(self.leitura_rele_prot_gerad_50bf, CONDIC_INDISPONIBILIZAR))

        self.leitura_disj_tps_protecao = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_DISJUNTOR_TPS_PROTECAO"], descr=f"[UG{self.__ug.id}] Disjuntor TPS Proteção")
        self.condicionadores.append(CondicionadorBase(self.leitura_disj_tps_protecao, CONDIC_INDISPONIBILIZAR))

        # TODO -> Verificar
        self.leitura_uhrv_pressao_freio = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_UHRV_PRESSAO_FREIO"], descr=f"[UG{self.__ug.id}] UHRV Pressão Freio")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhrv_pressao_freio, CONDIC_NORMALIZAR))

        self.leitura_rv_falha_hab = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_RV_FALHA_AO_HABILITAR"], descr=f"[UG{self.__ug.id}] RV Falha Habilitar")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_hab, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_hab = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_RT_FALHA_AO_HABILITAR"], descr=f"[UG{self.__ug.id}] RT Falha Habilitar")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_hab, CONDIC_INDISPONIBILIZAR))

        # UHRV
        # TODO -> Verificar
        self.leitura_uhrv_bomba_1_indisp = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_UHRV_BOMBA_1_INDISPONIVEL"], descr=f"[UG{self.__ug.id}] UHRV Bomba 1 Indisponível") # TODO -> Verificar invertido
        self.condicionadores.append(CondicionadorBase(self.leitura_uhrv_bomba_1_indisp, CONDIC_INDISPONIBILIZAR))

        self.leitura_uhrv_bomba_1_falha_ligar = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_UHRV_BOMBA_1_FALHA_AO_LIGAR"], descr=f"[UG{self.__ug.id}] UHRV Falha Ligar")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhrv_bomba_1_falha_ligar, CONDIC_INDISPONIBILIZAR))

        self.leitura_uhrv_filtro_oleo_sujo = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_UHRV_FILTRO_OLEO_SUJO"], descr=f"[UG{self.__ug.id}] UHRV Filtro Óleo Sujo")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhrv_filtro_oleo_sujo, CONDIC_INDISPONIBILIZAR))

        # UHLM
        self.leitura_uhlm_bomba_1_falha_ligar = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_UHLM_BOMBA_1_FALHA_LIGAR"], descr=f"[UG{self.__ug.id}] UHLM Bomba 1 Falha Ligar")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhlm_bomba_1_falha_ligar, CONDIC_INDISPONIBILIZAR))

        self.leitura_uhlm_bomba_1_falha_deslig = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_UHLM_BOMBA_1_FALHA_DESLIGAR"], descr=f"[UG{self.__ug.id}] UHLM Bomba 1 Falha Desligar")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhlm_bomba_1_falha_deslig, CONDIC_INDISPONIBILIZAR))

        self.leitura_ulhm_falha_pressos = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_UHLM_FALHA_PRESSOSTATO"], descr=f"[UG{self.__ug.id}] UHLM Falha Pressostato")
        self.condicionadores.append(CondicionadorBase(self.leitura_ulhm_falha_pressos, CONDIC_INDISPONIBILIZAR))

        self.leitura_uhlm_bomba_1_indisp = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_UHLM_BOMBA_1_INDISPONIVEL"], descr=f"[UG{self.__ug.id}] UHLM Bomba 1 Indisponível")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhlm_bomba_1_indisp, CONDIC_INDISPONIBILIZAR))

        self.leitura_uhlm_bomba_1_falha_pressurizar = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_UHLM_BOMBA_1_FALHA_PRESSURIZAR"], descr=f"[UG{self.__ug.id}] UHLM Bomba 1 Falha Pressurizar")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhlm_bomba_1_falha_pressurizar, CONDIC_INDISPONIBILIZAR))

        self.leitura_ulhm_filtro_sujo = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_UHLM_FILTRO_SUJO"], descr=f"[UG{self.__ug.id}] UHLM Filtro Sujo")
        self.condicionadores.append(CondicionadorBase(self.leitura_ulhm_filtro_sujo, CONDIC_INDISPONIBILIZAR))

        # RV
        self.leitura_rv_girando_gir_indev = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_1_GIRANDO_SEM_REG_GIRO_INDEV"], descr=f"[UG{self.__ug.id}] Falha RV Girando Sem Registro de Giro Indevido")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_girando_gir_indev, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_1_sobrefreq_inst = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_1_SOBREFREQ_INSTANT"], descr=f"[UG{self.__ug.id}] RV Falha 1 Sobrefrequência Instantânea")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_1_sobrefreq_inst, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_1_sobrefreq_tempor = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_1_SOBREFREQ_TEMPOR"], descr=f"[UG{self.__ug.id}] RV Falha 1 Sobrefrequência Temporizada")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_1_sobrefreq_tempor, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_1_subfreq_tempor = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_1_SUBFREQ_TEMPORIZADA"], descr=f"[UG{self.__ug.id}] RV Falha 1 Subfrequência Temporizada")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_1_subfreq_tempor, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_1_leit_pos_distrib = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_1_LEIT_POS_DISTRIBUIDOR"], descr=f"[UG{self.__ug.id}] RV Falha 1 Leitura Posição Distribuidor")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_1_leit_pos_distrib, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_1_leit_pot_ativa = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_1_LEIT_POTENCIA_ATIVA"], descr=f"[UG{self.__ug.id}] RV Falha 1 Leitura Potência Ativa")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_1_leit_pot_ativa, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_1_leit_refer_pot = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_1_LEIT_REFERENCIA_POTENCIA"], descr=f"[UG{self.__ug.id}] RV Falha 1 Leitura Referência Potência")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_1_leit_refer_pot, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_1_nv_montante_muito_baixo = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_1_NV_MONTANTE_MUITO_BAIXO"], descr=f"[UG{self.__ug.id}] RV Falha 1 Nível Montante Muito Baixo")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_1_nv_montante_muito_baixo, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_1_control_pos_distribu = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_1_CONTROLE_POS_DISTRIBUIDOR"], descr=f"[UG{self.__ug.id}] RV Falha 1 Controle Posição Distribuidor")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_1_control_pos_distribu, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_1_ruido_med_veloc_princi = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_1_RUIDO_MED_VELOC_PRINCIPAL"], descr=f"[UG{self.__ug.id}] RV Falha 1 Ruído Medição Velocidade Principal")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_1_ruido_med_veloc_princi, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_1_ruido_med_veloc_retag = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_1_RUIDO_MED_VELOC_RETAGUARDA"], descr=f"[UG{self.__ug.id}] RV Falha 1 Ruído Medição Velocidade Retaguarda")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_1_ruido_med_veloc_retag, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_2_perda_med_veloc_retag = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_2_PERDA_MED_VELOC_RETAGUARDA"], descr=f"[UG{self.__ug.id}] RV Falha 2 Perda Medição Velocidade Retaguarda")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_2_perda_med_veloc_retag, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_2_tempo_excess_partida = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_2_TEMPO_EXCESSIVO_PARTIDA"], descr=f"[UG{self.__ug.id}] RV Falha 2 Tempo Excessivo Partida")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_2_tempo_excess_partida, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_2_tempo_excess_parada = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_2_TEMPO_EXCESSIVO_PARADA"], descr=f"[UG{self.__ug.id}] RV Falha 2 Tempo Excessivo Parada")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_2_tempo_excess_parada, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_2_dif_med_velo_princ_retag = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_2_DIF_MED_VELO_PRINCIPAL_RETAGUARDA"], descr=f"[UG{self.__ug.id}] RV Falha 2 Diferença Medição Velocidade Principal Retaguarda")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_2_dif_med_velo_princ_retag, CONDIC_INDISPONIBILIZAR))

        self.leitura_rv_falha_1_perda_med_velo_princ = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RV_FALHA_1_PERDA_MED_VELOC_PRINCIPAL"], descr=f"[UG{self.__ug.id}] RV Falha 1 Perda Medição Velocidade Principal")
        self.condicionadores.append(CondicionadorBase(self.leitura_rv_falha_1_perda_med_velo_princ, CONDIC_INDISPONIBILIZAR))

        # RT
        self.leitura_rt_crowbar_inativo = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ED_CROWBAR_INATIVO"], descr=f"[UG{self.__ug.id}] RT Crowbar Inativo")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_crowbar_inativo, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_sobretensao = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_SOBRETENSAO"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Sobretensão")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_sobretensao, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_subtensao = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_SUBTENSAO"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Subtensão")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_subtensao, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_sobrefrequencia = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_SOBREFREQUENCIA"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Sobrefrequência")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_sobrefrequencia, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_subfrequencia = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_SUBFREQUENCIA"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Subfrequência")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_subfrequencia, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_lim_sup_pot_reativa = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_LIMITE_SUP_POT_REATIVA"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Limite Superior Potência Reativa")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_lim_sup_pot_reativa, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_lim_inf_pot_reativa = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_LIMITE_INF_POT_REATIVA"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Limite Inferior Potência Reativa")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_lim_inf_pot_reativa, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_lim_sup_fator_pot = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_LIMITE_SUP_FATOR_POTENCIA"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Limite Superior Fator Potência")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_lim_sup_fator_pot, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_lim_inf_fator_pot = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_LIMITE_INF_FATOR_POTENCIA"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Limite Inferior Fator Potência")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_lim_inf_fator_pot, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_variacao_tensao = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_VARIACAO_TENSAO"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Variação de Tensão")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_variacao_tensao, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_pot_ativa_reversa = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_POTENCIA_ATIVA_REVERSA"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Potência Ativa Reversa")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_pot_ativa_reversa, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_sobrecorr_term = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_SOBRECORRENTE_TERMINAL"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Sobrecorrente Terminal")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_sobrecorr_term, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_lim_sup_corr_excitacao = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_LIMITE_SUP_CORRENTE_EXCITACAO"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Limite Superior Corrente Excitação")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_lim_sup_corr_excitacao, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_lim_inf_corr_exci = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_LIMITE_INF_CORRENTE_EXCITACAO"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Limite Inferior Corrente Excitação")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_lim_inf_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_temp_muito_alta_rotor = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_TEMP_MUITO_ALTA_ROTOR"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Temperatura Muito Alta Rotor")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_temp_muito_alta_rotor, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_pres_tens_term_aus_corr_exci = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_PRES_TENS_TERM_AUSEN_CORR_EXCI"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Presença Tensão Terminal Ausente Corrente Excitação")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_pres_tens_term_aus_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_1_pres_corr_exci_aus_tens_term = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_1_PRES_CORR_EXCI_AUSEN_TENS_TERM"], descr=f"[UG{self.__ug.id}] RT Alarmes 1 Presença Corrente Excitação Ausente Tensão Terminal")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_1_pres_corr_exci_aus_tens_term, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_2_falha_contro_corr_exci = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_2_FALHA_CONTROLE_CORRENTE_EXCI"], descr=f"[UG{self.__ug.id}] RT Alarmes 2 Falha Controle Corrente Excitação")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_2_falha_contro_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_2_falha_contro_tens_term = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_2_FALHA_CONTROLE_TENSAO_TERM"], descr=f"[UG{self.__ug.id}] RT Alarmes 2 Falha Controle Tensão Terminal")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_2_falha_contro_tens_term, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_2_crowbar_atuado_regul_hab = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_2_CROWBAR_ATUADO_REGUL_HABIL"], descr=f"[UG{self.__ug.id}] RT Alarme 2 Crowbar Atuado Regulador Habilitado")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_2_crowbar_atuado_regul_hab, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_2_falha_hab_drive_excit = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_2_FALHA_HABIL_DRIVE_EXCI"], descr=f"[UG{self.__ug.id}] RT Alarme 2 Falha Habilitar Drive Excitação")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_2_falha_hab_drive_excit, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_2_falha_fechar_contator_campo = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_2_FALHA_FECHAR_CONTATOR_CAMPO"], descr=f"[UG{self.__ug.id}] RT Alarme 2 Falha Fechar Contator Campo")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_2_falha_fechar_contator_campo, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_2_falha_corr_exci_pre_exci_ativa = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_2_FALHA_CORR_EXCI_PRE_EXCI_ATIVA"], descr=f"[UG{self.__ug.id}] RT Alarme 2 Falha Corrente Excitação Pré Excitação Ativa")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_2_falha_corr_exci_pre_exci_ativa, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_2_perda_med_pot_reat = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_2_PERDA_MEDICAO_POTENCIA_REATIVA"], descr=f"[UG{self.__ug.id}] RT Alarme 2 Perda Medição Potência Reativa")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_2_perda_med_pot_reat, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_2_perda_med_tens_term = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_2_PERDA_MEDICAO_TENSAO_TERMINAL"], descr=f"[UG{self.__ug.id}] RT Alarme 2 Perda Medição Tensão Terminal")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_2_perda_med_tens_term, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_2_perda_med_corr_exci = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_2_PERDA_MEDICAO_CORRENTE_EXCI"], descr=f"[UG{self.__ug.id}] RT Alarme 2 Perda Medição Corrente Excitação")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_2_perda_med_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_ruido_intrumen_reat = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_2_RUIDO_INSTRUMEN_REATIVO"], descr=f"[UG{self.__ug.id}] RT Alarme 2 Ruído Leitura Intrumentador Reativo")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_ruido_intrumen_reat, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_ruido_intrumen_tensao = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_2_RUIDO_INSTRUMEN_TENSAO"], descr=f"[UG{self.__ug.id}] RT Alarme 2 Ruído Leitura Intrumentador Tensão")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_ruido_intrumen_tensao, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_ruido_intrumen_exci_princ = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_2_RUIDO_INSTRUMEN_EXCI_PRINCI"], descr=f"[UG{self.__ug.id}] RT Alarme 2 Ruído Leitura Intrumentador Excitação Principal")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_ruido_intrumen_exci_princ, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_alar_ruido_intrumen_exci_retag = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ALARMES_2_RUIDO_INSTRUMEN_EXCI_RETAG"], descr=f"[UG{self.__ug.id}] RT Alarme 2 Ruído Leitura Intrumentador Excitação Retaguarda")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_alar_ruido_intrumen_exci_retag, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_sobretensao = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_SOBRETENSAO"], descr=f"[UG{self.__ug.id}] RT Falha 1 Sobretensão")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_sobretensao, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_subtensao = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_SUBTENSAO"], descr=f"[UG{self.__ug.id}] RT Falha 1 Subtensão")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_subtensao, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_sobrefreq = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_SOBREFREQUENCIA"], descr=f"[UG{self.__ug.id}] RT Falha 1 Sobrefrequência")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_sobrefreq, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_subfreq = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_SUBFREQUENCIA"], descr=f"[UG{self.__ug.id}] RT Falha 1 Subfrequência")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_subfreq, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_lim_sup_pot_reat = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_LIMITE_SUP_POT_REATIVA"], descr=f"[UG{self.__ug.id}] RT Falha 1 Limite Superior Potência Reativa")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_lim_sup_pot_reat, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_lim_inf_pot_reat = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_LIMITE_INF_POT_REATIVA"], descr=f"[UG{self.__ug.id}] RT Falha 1 Limite Inferior Potência Reativa")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_lim_inf_pot_reat, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_lim_sup_fator_pot = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_LIMITE_SUP_FATOR_POT"], descr=f"[UG{self.__ug.id}] RT Falha 1 Limite Superior Fator Potência")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_lim_sup_fator_pot, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_lim_inf_fator_pot = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_LIMITE_INF_FATOR_POT"], descr=f"[UG{self.__ug.id}] RT Falha 1 Limite Inferior Fator Potência")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_lim_inf_fator_pot, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_sobretensao_inst = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_SOBRETENSAO_INST"], descr=f"[UG{self.__ug.id}] RT Falha 1 Sobretensão Instantânea")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_sobretensao_inst, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_variacao_tensao = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_VARIACAO_TENSAO"], descr=f"[UG{self.__ug.id}] RT Falha 1 Variação Tensão")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_variacao_tensao, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_pot_ativ_reversa = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_POT_ATIVA_REVERSA"], descr=f"[UG{self.__ug.id}] RT Falha 1 Potência Ativa Reversa")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_pot_ativ_reversa, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_sobrecorr_term = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_SOBRECORRENTE_TERMINAL"], descr=f"[UG{self.__ug.id}] RT Falha 1 Sobrecorrente Terminal")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_sobrecorr_term, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_lim_sup_corr_exci = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_LIMITE_SUP_CORRENTE_EXCITACAO"], descr=f"[UG{self.__ug.id}] RT Falha 1 Limite Superior Corrente Excitação")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_lim_sup_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_lim_inf_corr_exci = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_LIMITE_INF_CORRENTE_EXCITACAO"], descr=f"[UG{self.__ug.id}] RT Falha 1 Limite Inferior Corrente Excitação")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_lim_inf_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_lim_sup_tensao_exci = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_LIMITE_SUP_TENSAO_EXCITACAO"], descr=f"[UG{self.__ug.id}] RT Falha 1 Limite Superior Tensão Excitação")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_lim_sup_tensao_exci, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_1_lim_inf_tensao_exci = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_1_LIMITE_INF_TENSAO_EXCITACAO"], descr=f"[UG{self.__ug.id}] RT Falha 1 Limite Inferior Tensão Excitação")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_1_lim_inf_tensao_exci, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_2_temp_muito_alta_rotor = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_2_TEMP_MUITO_ALTA_ROTOR"], descr=f"[UG{self.__ug.id}] RT Falha 2 Temperatura Muito Alta Rotor")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_2_temp_muito_alta_rotor, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_2_pres_tens_term_aus_corr_exci = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_2_PRES_TENS_TERM_AUSEN_CORR_EXCI"], descr=f"[UG{self.__ug.id}] RT Falha 2 Presença Tensão Terminal Ausente Corrente Excitação")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_2_pres_tens_term_aus_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_2_pres_corr_exci_aus_tens_term = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_2_PRES_CORR_EXCI_AUSEN_TENS_TERM"], descr=f"[UG{self.__ug.id}] RT Falha 2 Presença Corrente Excitação Ausente Tensão Terminal")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_2_pres_corr_exci_aus_tens_term, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_2_control_corr_exci = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_2_CONTROLE_CORR_EXCI"], descr=f"[UG{self.__ug.id}] RT Falha 2 Controle Corrente Excitação")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_2_control_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_2_tensao_term = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_2_TENSAO_TERMINAL"], descr=f"[UG{self.__ug.id}] RT Falha 2 Tensão Terminal")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_2_tensao_term, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_2_crowbar_atuado_regu_hab = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_2_CROWBAR_ATUADO_REGULADOR_HABI"], descr=f"[UG{self.__ug.id}] RT Falha 2 Crowbar Atuado Regulador Habilitado")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_2_crowbar_atuado_regu_hab, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_2_hab_drive_exci = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_2_HABI_DRIVE_EXCITACAO"], descr=f"[UG{self.__ug.id}] RT Falha 2 Habilitar Drive Excitação")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_2_hab_drive_exci, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_2_fechar_contator_campo = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_2_FECHAR_CONTATOR_CAMPO"], descr=f"[UG{self.__ug.id}] RT Falha 2 Fechar Contator Campo")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_2_fechar_contator_campo, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_2_corr_exci_pre_exci_ativa = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_2_CORR_EXCITA_PRE_EXCXITA_ATIVA"], descr=f"[UG{self.__ug.id}] RT Falha 2 Corrente Excitação Pré Excitada Ativa")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_2_corr_exci_pre_exci_ativa, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_2_excess_pre_exci = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_2_EXCESSIVO_PRE_EXCITACAO"], descr=f"[UG{self.__ug.id}] RT Falha 2 Excessivo Pré Excitação")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_2_excess_pre_exci, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_2_excess_parada = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_2_EXCESSIVO_PARADA"], descr=f"[UG{self.__ug.id}] RT Falha 2 Excessivo Parada")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_2_excess_parada, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_3_perda_med_pot_reativa = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_3_PERDA_MED_POT_REATIVA"], descr=f"[UG{self.__ug.id}] RT Falha 3 Perda Medição Potência Reativa")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_3_perda_med_pot_reativa, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_3_perda_med_tensao_term = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_3_PERDA_MED_TENSAO_TERM"], descr=f"[UG{self.__ug.id}] RT Falha 3 Perda Medição Tensão Terminal")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_3_perda_med_tensao_term, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_3_perda_med_corr_exci_princ = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_3_PERDA_MED_CORR_EXCI_PRINCI"], descr=f"[UG{self.__ug.id}] RT Falha 3 Perda Medição Corrente Excitação Principal")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_3_perda_med_corr_exci_princ, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_3_perda_med_corr_exci_retag = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_3_PERDA_MED_CORR_EXCI_RETAG"], descr=f"[UG{self.__ug.id}] RT Falha 3 Perda Medição Corrente Excitação Retaguarda")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_3_perda_med_corr_exci_retag, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_3_ruido_leit_instrum_reativo = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_3_RUIDO_INSTRUM_REATIVO"], descr=f"[UG{self.__ug.id}] RT Falha 3 Ruído Leitura Instrumentador Reativo")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_3_ruido_leit_instrum_reativo, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_3_ruido_leit_instrum_tensao = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_3_RUIDO_INSTRUM_TENSAO"], descr=f"[UG{self.__ug.id}] RT Falha 3 Ruído Leitura Instrumentador Tensão")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_3_ruido_leit_instrum_tensao, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_3_ruido_leit_instrum_principal = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_3_RUIDO_INSTRUM_EXCI_PRINCI"], descr=f"[UG{self.__ug.id}] RT Falha 3 Ruído Leitura Instrumentador Principal")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_3_ruido_leit_instrum_principal, CONDIC_INDISPONIBILIZAR))

        self.leitura_rt_falha_3_ruido_leit_instrum_retag = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_FALHAS_3_RUIDO_INSTRUM_EXCI_RETAG"], descr=f"[UG{self.__ug.id}] RT Falha 3 Ruído Leitura Instrumentador Retaguarda")
        self.condicionadores.append(CondicionadorBase(self.leitura_rt_falha_3_ruido_leit_instrum_retag, CONDIC_INDISPONIBILIZAR))


        # ENTRADAS ANALÓGICAS
        self.leitura_tristor_temp_muito_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_TRISTORES_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug.id}] Tristores Temperatura Muito Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_tristor_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.leitura_crowbar_temp_muito_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_CROWBAR_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug.id}] Crowbar Temperatura Muito Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_crowbar_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.leitura_trafo_exci_temp_muito_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_TRAFO_EXCITACAO_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug.id}] Transformador Excitação Temperatura Muito Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_trafo_exci_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.leitura_uhrv_temp_oleo_muito_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_UHRV_OLEO_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug.id}] UHRV Óleo Temperatura Muito Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhrv_temp_oleo_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.leitura_gera_fase_a_temp_muito_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_FASE_A_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug.id}] Gerador Fase A Temperatura Muito Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_gera_fase_a_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.leitura_gera_fase_b_temp_muito_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_FASE_B_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug.id}] Gerador Fase B Temperatura Muito Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_gera_fase_b_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.leitura_gera_fase_c_temp_muito_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_FASE_C_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug.id}] Gerador Fase C Temperatura Muito Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_gera_fase_c_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.leitura_gera_nucleo_1_temp_muito_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_1_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug.id}] Gerador Núcleo 1 Temperatura Muito Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_gera_nucleo_1_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.leitura_gera_nucleo_2_temp_muito_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_2_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug.id}] Gerador Núcleo 2 Temperatura Muito Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_gera_nucleo_2_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.leitura_gera_nucleo_3_temp_muito_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_3_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug.id}] Gerador Núcleo 3 Temperatura Muito Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_gera_nucleo_3_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.leitura_mancal_guia_casq_temp_muito_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_MANCAL_GUIA_CASQUILHO_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug.id}] Mancal Guia Casquilho Temperatura Muito Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_mancal_guia_casq_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.leitura_mancal_comb_casq_temp_muito_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_MANCAL_COMBINADO_CASQUILHO_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug.id}] Mancal Combinado Casquilho Temperatura Muito Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_mancal_comb_casq_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.leitura_mancal_comb_esc_temp_muito_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_MANCAL_COMBINADO_ESCORA_TEMP_MUITO_ALTA"], descr=f"[UG{self.__ug.id}] Mancal Combinado Escora Temperatura Muito Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_mancal_comb_esc_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.leitura_uhrv_press_oleo_falha_leitura = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_UHRV_PRESSAO_OLEO_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] UHRV Pressão Óleo Falha Leitura")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhrv_press_oleo_falha_leitura, CONDIC_INDISPONIBILIZAR))

        self.leitura_uhrv_press_oleo_muito_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_UHRV_PRESSAO_OLEO_MUITO_ALTO"], descr=f"[UG{self.__ug.id}] UHRV Pressão Óleo Muito Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhrv_press_oleo_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.leitura_uhrv_press_oleo_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_UHRV_PRESSAO_OLEO_ALTO"], descr=f"[UG{self.__ug.id}] UHRV Pressão Óleo Alta")
        self.condicionadores.append(CondicionadorBase(self.leitura_uhrv_press_oleo_alta, CONDIC_INDISPONIBILIZAR))


        # ## WHATSAPP + VOIP
        self.leitura_cmd_uhrv_modo_manuten = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_CD_CMD_UHRV_MODO_MANUTENCAO"], descr=f"[UG{self.__ug.id}] UHRV Comando Modo Manutenção")
        self.leitura_cmd_uhlm_modo_manuten = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_CD_CMD_UHLM_MODO_MANUTENCAO"], descr=f"[UG{self.__ug.id}] UHLM Comando Modo Manutenção")
        self.leitura_resis_quec_gerador_falha_ligar = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR"], descr=f"[UG{self.__ug.id}] ")

        self.leitura_falha_leit_temp_tristores = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_TRISTORES_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] Tristores Temperatura Falha Leitura")
        self.leitura_falha_leit_temp_crowbar = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_CROWBAR_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] Crowbar Temperatura Falha Leitura")
        self.leitura_falha_leit_temp_uhrv_temp_oleo = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_UHRV_TEMP_OLEO_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] UHRV Temperatura Óleo Falha Leitura")
        self.leitura_falha_leit_temp_trafo_exci = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_TRAFO_EXCITACAO_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] Transformador Excitação Temperatura Falha Leitura")
        self.leitura_falha_leit_temp_gerad_fase_a = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] Gerador Fase A Temperatura Falha Leitura")
        self.leitura_falha_leit_temp_gerad_fase_b = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] Gerador Fase B Temperatura Falha Leitura")
        self.leitura_falha_leit_temp_gerad_fase_c = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] Gerador Fase C Temperatura Falha Leitura")
        self.leitura_falha_leit_temp_gerad_nucleo_1 = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] Gerador Núcleo 1 Temperatura Falha Leitura")
        self.leitura_falha_leit_temp_gerad_nucleo_2 = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_2_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] Gerador Núcleo 2 Temperatura Falha Leitura")
        self.leitura_falha_leit_temp_gerad_nucleo_3 = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] Gerador Núcleo 3 Temperatura Falha Leitura")
        self.leitura_falha_leit_temp_mancal_guia_casq = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_MANCAL_GUIA_CASQUILHO_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] Mancal Guia Casquilho temperatura Falha Leitura")
        self.leitura_falha_leit_temp_mancal_comb_esc = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_MANCAL_COMBINADO_ESCORA_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] Mancal Combinado Escora Temperatura Falha Leitura")
        self.leitura_falha_leit_temp_mancal_comb_casq = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_MANCAL_COMBINADO_CASQUILHO_TEMP_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] Mancal Combinado Casquilho Temperatura Falha Leitura")

        # ## WHATSAPP
        self.leitura_rv_alarme = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_RV_ALARME"], descr=f"[UG{self.__ug.id}] RV Alarme")
        self.leitura_rt_alarme = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_RT_ALARME"], descr=f"[UG{self.__ug.id}] RT Alarme")
        self.leitura_alarme_rele = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_SD_RELE_ALARME"], descr=f"[UG{self.__ug.id}] Alarme Relé")
        self.leitura_rv_pot_nula = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_RV_POTENCIA_NULA"], descr=f"[UG{self.__ug.id}] RV Potência Nula")
        self.leitura_uhrv_bomba_defeito = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_UHRV_BOMBA_DEFEITO"], descr=f"[UG{self.__ug.id}] UHRV Bomba Defeito") # TODO -> Verificar invertido
        self.leitura_uhlm_bomba_defeito = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_UHLM_BOMBA_DEFEITO"], descr=f"[UG{self.__ug.id}] UHLM Bomba Defeito")
        self.leitura_dispo_prot_surto = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_DISPOSITIVO_PROTECAO_SURTO"], descr=f"[UG{self.__ug.id}] Dispositivo Proteção Surto")
        self.leitura_rt_selec_modo_controle_isol = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_RT_ED_SELEC_MODO_CONTROLE_ISOLADO"], descr=f"[UG{self.__ug.id}] RT Selecionado Modo Controle Isolado")
        self.leitura_resis_aquec_gerad_defeito = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_PRTVA_RESISTENCIA_AQUEC_GERADOR_DEFEITO"], descr=f"[UG{self.__ug.id}] Resistência Aquecimento Gerador Defeito")

        self.leitura_crowbar_temp_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_CROWBAR_TEMP_ALTA"], descr=f"[UG{self.__ug.id}] Temperatura Alta")
        self.leitura_tristores_temp_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_TRISTORES_TEMP_ALTA"], descr=f"[UG{self.__ug.id}] Temperatura Alta")
        self.leitura_uhrv_oleo_temp_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_UHRV_OLEO_TEMP_ALTA"], descr=f"[UG{self.__ug.id}] Temperatura Alta")
        self.leitura_trafo_exci_temp_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_TRAFO_EXCITACAO_TEMP_ALTA"], descr=f"[UG{self.__ug.id}] Temperatura Alta")
        self.leitura_gerad_fase_a_temp_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_FASE_A_TEMP_ALTA"], descr=f"[UG{self.__ug.id}] Gerador Fase A Temperatura Alta")
        self.leitura_gerad_fase_b_temp_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_FASE_B_TEMP_ALTA"], descr=f"[UG{self.__ug.id}] Gerador Fase B Temperatura Alta")
        self.leitura_gerad_fase_c_temp_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_FASE_C_TEMP_ALTA"], descr=f"[UG{self.__ug.id}] Gerador Fase C Temperatura Alta")
        self.leitura_gerad_nucleo_1_temp_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_1_TEMP_ALTA"], descr=f"[UG{self.__ug.id}] Gerador Núcleo 1 Temperatura Alta")
        self.leitura_gerad_nucleo_2_temp_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_2_TEMP_ALTA"], descr=f"[UG{self.__ug.id}] Gerador Núcleo 2 Temperatura Alta")
        self.leitura_gerad_nucleo_3_temp_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_GERADOR_NUCLEO_3_TEMP_ALTA"], descr=f"[UG{self.__ug.id}] Gerador Núcleo 3 Temperatura Alta")
        self.leitura_mancal_guia_casq_temp_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_MANCAL_GUIA_CASQUILHO_TEMP_ALTA"], descr=f"[UG{self.__ug.id}] Mancal Guia Casquilho Temperatura Alta")
        self.leitura_mancal_comb_esc_temp_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_MANCAL_COMBINADO_ESCORA_TEMP_ALTA"], descr=f"[UG{self.__ug.id}] Mancal Combinado Escora Temperatura Alta")
        self.leitura_mancal_comb_casq_temp_alta = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_MANCAL_COMBINADO_CASQUILHO_TEMP_ALTA"], descr=f"[UG{self.__ug.id}] Mancal Combinado Casquilho Temperatura Alta")

        self.leitura_rv_modo_manut = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_RV_MODO_MANUTENCAO"], descr=f"[UG{self.__ug.id}] RV Modo Manutenção")
        self.leitura_uhlm_unidade_manut = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_UHLM_UNIDADE_MANUTENCAO"], descr=f"[UG{self.__ug.id}] UHLM Unidade Manutenção")
        self.leitura_sinal_nv_jusante_alto = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_SINAL_NIVEL_JUSANTE_ALTO"], descr=f"[UG{self.__ug.id}] Nível Jusante Sinal Alto")
        self.leitura_uhrv_pressao_oleo_baixa = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_UHRV_PRESSAO_OLEO_BAIXA"], descr=f"[UG{self.__ug.id}] UHRV Pressão Óleo Baixa")
        self.leitura_sinal_nv_jusante_baixo = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_SINAL_NIVEL_JUSANTE_BAIXA"], descr=f"[UG{self.__ug.id}] Nível Jusante Sinal Baixo")
        self.leitura_falha_leit_nv_jusante = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_SINAL_NIVEL_JUSANTE_FALHA_LEITURA"], descr=f"[UG{self.__ug.id}] Nível Jusante Falha Leitura")
        self.leitura_sinal_nv_jusante_muito_alto = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_SINAL_NIVEL_JUSANTE_MUITO_ALTO"], descr=f"[UG{self.__ug.id}] Nível Jusante Sinal Muito Alto")
        self.leitura_uhrv_pressao_oleo_muito_baixa = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_UHRV_PRESSAO_OLEO_MUITO_BAIXA"], descr=f"[UG{self.__ug.id}] UHRV Pressão Óleo Muito Baixa")
        self.leitura_alarme_contro_dif_grade = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_CONTROLE_ALARME_DIFERENCIAL_GRADE"], descr=f"[UG{self.__ug.id}] Alarme Controle Diferencial Grade")
        self.leitura_sinal_nv_jusante_muito_baixo = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_EA_SINAL_NIVEL_JUSANTE_MUITO_BAIXA"], descr=f"[UG{self.__ug.id}] Nível Jusante Sinal Muito Baixo")
        self.leitura_resis_aquec_gerad_indisp = LeituraModbusBit(self.__clp[f"UG{self.__ug.id}"], REG["CONDIC_UG"][f"UG{self.__ug.id}_ED_RESISTENCIA_AQUEC_GERADOR_INDISPONIVEL"], descr=f"[UG{self.__ug.id}] Resistência Aquecimento Gerador Indisponível")
        # # "UG1_RV_ESTADO_OPERACAO" -> CONTROLE MANUAL DISTRIBUIDOR = 14
        # # "UG1_RV_ESTADO_OPERACAO" -> CONTROLE MANUAL ROTOR = 15
