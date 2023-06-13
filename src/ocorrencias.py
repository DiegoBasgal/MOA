import logging
import traceback

import src.mensageiro.dict as vd
import src.dicionarios.dict as d

from src.funcoes.leitura import *
from src.condicionadores import *
from src.dicionarios.reg import *
from src.dicionarios.const import *

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
        if self.leitura_ED_SA_QLCF_Disj52ETrip.valor != 0 and not vd.voip_dict["SA_QLCF_DISJ_52E_TRIP"][0]:
            logger.warning("O Disjuntor do Gerador Diesel de Emergência QLCF identificou um sinal de TRIP, favor verificar.")
            vd.voip_dict["SA_QLCF_DISJ_52E_TRIP"][0] = True
        elif self.leitura_ED_SA_QLCF_Disj52ETrip.valor == 0 and vd.voip_dict["SA_QLCF_DISJ_52E_TRIP"][0]:
            vd.voip_dict["SA_QLCF_DISJ_52E_TRIP"][0] = False

        if self.leitura_ED_SA_QLCF_TripDisjAgrup.valor != 0 and not vd.voip_dict["SA_QLCF_TRIP_DISJ_AGRUP"][0]:
            logger.warning("O sensor do Disjuntor de Agrupamento QLCF identificou um sinal de trip, favor verificar.")
            vd.voip_dict["SA_QLCF_TRIP_DISJ_AGRUP"][0] = True
        elif self.leitura_ED_SA_QLCF_TripDisjAgrup.valor == 0 and vd.voip_dict["SA_QLCF_TRIP_DISJ_AGRUP"][0]:
            vd.voip_dict["SA_QLCF_TRIP_DISJ_AGRUP"][0] = False

        if self.leitura_ED_SA_QCAP_SubtensaoBarraGeral.valor != 0 and not vd.voip_dict["SA_QCAP_SUBTENSAO_BARRA_GERAL"][0]:
            logger.warning("O sensor de Subtensão do Barramento Geral QCAP foi acionado, favor verificar.")
            vd.voip_dict["SA_QCAP_SUBTENSAO_BARRA_GERAL"][0] = True
        elif self.leitura_ED_SA_QCAP_SubtensaoBarraGeral.valor == 0 and vd.voip_dict["SA_QCAP_SUBTENSAO_BARRA_GERAL"][0]:
            vd.voip_dict["SA_QCAP_SUBTENSAO_BARRA_GERAL"][0] = False

        if self.leitura_ED_SA_GMG_Alarme.valor != 0 and not vd.voip_dict["SA_GMG_ALARME"][0]:
            logger.warning("O alarme do Grupo Motor Gerador foi acionado, favor verificar.")
            vd.voip_dict["SA_GMG_ALARME"][0] = True
        elif self.leitura_ED_SA_GMG_Alarme.valor == 0 and vd.voip_dict["SA_GMG_ALARME"][0]:
            vd.voip_dict["SA_GMG_ALARME"][0] = False

        if self.leitura_ED_SA_GMG_Trip.valor != 0 and not vd.voip_dict["SA_GMG_TRIP"][0]:
            logger.warning("O sensor de TRIP do Grupo Motor Gerador foi acionado, favor verificar.")
            vd.voip_dict["SA_GMG_TRIP"][0] = True
        elif self.leitura_ED_SA_GMG_Trip.valor == 0 and vd.voip_dict["SA_GMG_TRIP"][0]:
            vd.voip_dict["SA_GMG_TRIP"][0] = False

        if self.leitura_ED_SA_GMG_Operacao.valor != 0 and not vd.voip_dict["SA_GMG_OPERACAO"][0]:
            logger.warning("O sensor de operação do Grupo Motor Gerador foi acionado, favor verificar.")
            vd.voip_dict["SA_GMG_OPERACAO"][0] = True
        elif self.leitura_ED_SA_GMG_Operacao.valor == 0 and vd.voip_dict["SA_GMG_OPERACAO"][0]:
            vd.voip_dict["SA_GMG_OPERACAO"][0] = False

        if self.leitura_ED_SA_GMG_BaixoComb.valor != 0 and not vd.voip_dict["SA_GMG_BAIXO_COMB"][0]:
            logger.warning("O sensor de de combustível do Grupo Motor Gerador retornou que o nível está baixo, favor reabastercer o gerador.")
            vd.voip_dict["SA_GMG_BAIXO_COMB"][0] = True
        elif self.leitura_ED_SA_GMG_BaixoComb.valor == 0 and vd.voip_dict["SA_GMG_BAIXO_COMB"][0]:
            vd.voip_dict["SA_GMG_BAIXO_COMB"][0] = False

        if self.leitura_RD_BbaDren1_FalhaAcion.valor != 0 and not vd.voip_dict["BBA_DREN_1_FALHA_ACION"][0]:
            logger.warning("O sensor da Bomba de Drenagem 1 identificou uma falha no acionamento, favor verificar.")
            vd.voip_dict["BBA_DREN_1_FALHA_ACION"][0] = True
        elif self.leitura_RD_BbaDren1_FalhaAcion.valor == 0 and vd.voip_dict["BBA_DREN_1_FALHA_ACION"][0]:
            vd.voip_dict["BBA_DREN_1_FALHA_ACION"][0] = False

        if self.leitura_RD_BbaDren2_FalhaAcion.valor != 0 and not vd.voip_dict["BBA_DREN_2_FALHA_ACION"][0]:
            logger.warning("O sensor da Bomba de Drenagem 2 identificou uma falha no acionamento, favor verificar.")
            vd.voip_dict["BBA_DREN_2_FALHA_ACION"][0] = True
        elif self.leitura_RD_BbaDren2_FalhaAcion.valor == 0 and vd.voip_dict["BBA_DREN_2_FALHA_ACION"][0]:
            vd.voip_dict["BBA_DREN_2_FALHA_ACION"][0] = False

        if self.leitura_RD_BbaDren3_FalhaAcion.valor != 0 and not vd.voip_dict["BBA_DREN_3_FALHA_ACION"][0]:
            logger.warning("O sensor da Bomba de Drenagem 3 identificou uma falha no acionamento, favor verificar.")
            vd.voip_dict["BBA_DREN_3_FALHA_ACION"][0] = True
        elif self.leitura_RD_BbaDren3_FalhaAcion.valor == 0 and vd.voip_dict["BBA_DREN_3_FALHA_ACION"][0]:
            vd.voip_dict["BBA_DREN_3_FALHA_ACION"][0] = False

        if self.leitura_RD_SA_GMG_FalhaAcion.valor != 0 and not vd.voip_dict["SA_GMG_FALHA_ACION"][0]:
            logger.warning("O sensor do Grupo Motor Gerador identificou uma falha no acionamento, favor verificar.")
            vd.voip_dict["SA_GMG_FALHA_ACION"][0] = True
        elif self.leitura_RD_SA_GMG_FalhaAcion.valor == 0 and vd.voip_dict["SA_GMG_FALHA_ACION"][0]:
            vd.voip_dict["SA_GMG_FALHA_ACION"][0] = False

        if self.leitura_RD_FalhaComunSETDA.valor == 1 and not vd.voip_dict["FALHA_COMUM_SETDA"][0]:
            logger.warning("Houve uma falha de comunicação com o CLP da Subestação e o CLP da Tomada da Água, favor verificar")
            vd.voip_dict["FALHA_COMUM_SETDA"][0] = True
        elif self.leitura_RD_FalhaComunSETDA.valor == 0 and vd.voip_dict["FALHA_COMUM_SETDA"][0]:
            vd.voip_dict["FALHA_COMUM_SETDA"][0] = False

        if self.leitura_ED_SA_QCAP_Disj52EFechado.valor == 1 and not vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0]:
            logger.warning("O Disjuntor do Gerador Diesel de Emergência QLCF foi fechado.")
            vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0] = True
        elif self.leitura_ED_SA_QCAP_Disj52EFechado.valor == 0 and vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0]:
            vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0] = False

        if self.leitura_ED_SA_QCADE_BombasDng_Auto.valor == 0 and not vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0]:
            logger.warning("O poço de drenagem da Usina entrou em modo remoto, favor verificar.")
            vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0] = True
        elif self.leitura_ED_SA_QCADE_BombasDng_Auto.valor == 1 and vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0]:
            vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0] = False

        return

    def carregar_leituras(self) -> None:
        ### Leituras para acionamento temporizado por chamada Voip
        ## CONDICIONADORES ESSENCIAIS
                # Leituras para acionamento periódico
        self.leitura_ED_SA_GMG_Trip = LeituraModbusCoil("ED_SA_GMG_Trip", self.__clp["SA"], REG["SA_ED_GMG_Trip"])
        self.leitura_ED_SA_GMG_Alarme = LeituraModbusCoil("ED_SA_GMG_Alarme", self.__clp["SA"], REG["SA_ED_GMG_Alarme"])
        self.leitura_ED_SA_GMG_Operacao = LeituraModbusCoil("ED_SA_GMG_Operacao", self.__clp["SA"], REG["SA_ED_GMG_Operacao"])
        self.leitura_RD_FalhaComunSETDA = LeituraModbusCoil("RD_FalhaComunSETDA", self.__clp["SA"], REG["SA_RD_FalhaComunSETDA"])
        self.leitura_ED_SA_GMG_BaixoComb = LeituraModbusCoil("ED_SA_GMG_BaixoComb", self.__clp["SA"], REG["SA_ED_GMG_BaixoComb"])
        self.leitura_RD_SA_GMG_FalhaAcion = LeituraModbusCoil("RD_SA_GMG_FalhaAcion", self.__clp["SA"], REG["SA_RD_GMG_FalhaAcion"])
        self.leitura_ED_SA_QLCF_Disj52ETrip = LeituraModbusCoil("ED_SA_QLCF_Disj52ETrip", self.__clp["SA"], REG["SA_ED_QLCF_Disj52ETrip"])
        self.leitura_RD_BbaDren1_FalhaAcion = LeituraModbusCoil("RD_BbaDren1_FalhaAcion", self.__clp["SA"], REG["SA_RD_BbaDren1_FalhaAcion"])
        self.leitura_RD_BbaDren2_FalhaAcion = LeituraModbusCoil("RD_BbaDren2_FalhaAcion", self.__clp["SA"], REG["SA_RD_BbaDren2_FalhaAcion"])
        self.leitura_RD_BbaDren3_FalhaAcion = LeituraModbusCoil("RD_BbaDren3_FalhaAcion", self.__clp["SA"], REG["SA_RD_BbaDren3_FalhaAcion"])
        self.leitura_ED_SA_QLCF_TripDisjAgrup = LeituraModbusCoil("ED_SA_QLCF_TripDisjAgrup", self.__clp["SA"], REG["SA_ED_QLCF_TripDisjAgrup"])
        self.leitura_ED_SA_QCAP_Disj52EFechado = LeituraModbusCoil("ED_SA_QCAP_Disj52EFechado", self.__clp["SA"], REG["SA_ED_QCAP_Disj52EFechado"])
        self.leitura_ED_SA_QCADE_BombasDng_Auto = LeituraModbusCoil("ED_SA_QCADE_BombasDng_Auto", self.__clp["SA"], REG["SA_ED_QCADE_BombasDng_Auto"])
        self.leitura_ED_SA_QCAP_SubtensaoBarraGeral = LeituraModbusCoil("ED_SA_QCAP_SubtensaoBarraGeral", self.__clp["SA"], REG["SA_ED_QCAP_SubtensaoBarraGeral"])

        ### CONDICIONADORES ESSENCIAIS
        self.leitura_ED_SA_QCAP_TensaoPresenteTSA = LeituraModbusCoil("ED_SA_QCAP_TensaoPresenteTSA", self.__clp["SA"], REG["SA_ED_QCAP_TensaoPresenteTSA"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_QCAP_TensaoPresenteTSA.descr, CONDIC_NORMALIZAR, self.leitura_ED_SA_QCAP_TensaoPresenteTSA))

        self.leitura_ED_SA_SEL787_Trip = LeituraModbusCoil("ED_SA_SEL787_Trip", self.__clp["SA"], REG["SA_ED_SEL787_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_SEL787_Trip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_SEL787_Trip))

        self.leitura_ED_SA_SEL311_Trip = LeituraModbusCoil("ED_SA_SEL311_Trip", self.__clp["SA"], REG["SA_ED_SEL311_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_SEL311_Trip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_SEL311_Trip))

        self.leitura_ED_SA_MRU3_Trip = LeituraModbusCoil("ED_SA_MRU3_Trip", self.__clp["SA"], REG["SA_ED_MRU3_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_MRU3_Trip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_MRU3_Trip))

        self.leitura_ED_SA_MRL1_Trip = LeituraModbusCoil("ED_SA_MRL1_Trip", self.__clp["SA"], REG["SA_ED_MRL1_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_MRL1_Trip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_MRL1_Trip))

        self.leitura_ED_SA_QCADE_Disj52E1Trip = LeituraModbusCoil("ED_SA_QCADE_Disj52E1Trip", self.__clp["SA"], REG["SA_ED_QCADE_Disj52E1Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Disj52E1Trip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCADE_Disj52E1Trip))

        ### CONDICIONADORES NORMAIS
        if not self.TDA_Offline:
            self.leitura_ED_TDA_QcataDisj52ETrip = LeituraModbusCoil("ED_TDA_QcataDisj52ETrip", self.__clp["TDA"], REG["TDA_ED_QcataDisj52ETrip"])
            self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52ETrip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_TDA_QcataDisj52ETrip))

            self.leitura_ED_TDA_QcataDisj52ETripDisjSai = LeituraModbusCoil("ED_TDA_QcataDisj52ETripDisjSai", self.__clp["TDA"], REG["TDA_ED_QcataDisj52ETripDisjSai"])
            self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52ETripDisjSai.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_TDA_QcataDisj52ETripDisjSai))

            self.leitura_ED_TDA_QcataDisj52EFalha380VCA = LeituraModbusCoil("ED_TDA_QcataDisj52EFalha380VCA", self.__clp["TDA"], REG["TDA_ED_QcataDisj52EFalha380VCA"])
            self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52EFalha380VCA.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_TDA_QcataDisj52EFalha380VCA))

        self.leitura_ED_SA_MRU3_Falha = LeituraModbusCoil("ED_SA_MRU3_Falha", self.__clp["SA"], REG["SA_ED_MRU3_Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_MRU3_Falha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_MRU3_Falha))

        self.leitura_ED_SA_SEL787_FalhaInterna = LeituraModbusCoil("ED_SA_SEL787_FalhaInterna", self.__clp["SA"], REG["SA_ED_SEL787_FalhaInterna"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_SEL787_FalhaInterna.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_SEL787_FalhaInterna))

        self.leitura_ED_SA_SEL311_Falha = LeituraModbusCoil("ED_SA_SEL311_Falha", self.__clp["SA"], REG["SA_ED_SEL311_Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_SEL311_Falha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_SEL311_Falha))

        self.leitura_ED_SA_CTE_Falta125Vcc = LeituraModbusCoil("ED_SA_CTE_Falta125Vcc", self.__clp["SA"], REG["SA_ED_CTE_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CTE_Falta125Vcc.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_CTE_Falta125Vcc))

        self.leitura_ED_SA_CTE_Secc89TE_Aberta = LeituraModbusCoil("ED_SA_CTE_Secc89TE_Aberta", self.__clp["SA"], REG["SA_ED_CTE_Secc89TE_Aberta"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CTE_Secc89TE_Aberta.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_CTE_Secc89TE_Aberta))

        self.leitura_ED_SA_TE_AlarmeDetectorGas = LeituraModbusCoil("ED_SA_TE_AlarmeDetectorGas", self.__clp["SA"], REG["SA_ED_TE_AlarmeDetectorGas"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeDetectorGas.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeDetectorGas))

        self.leitura_ED_SA_TE_AlarmeNivelMaxOleo = LeituraModbusCoil("ED_SA_TE_AlarmeNivelMaxOleo", self.__clp["SA"], REG["SA_ED_TE_AlarmeNivelMaxOleo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeNivelMaxOleo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeNivelMaxOleo))

        self.leitura_ED_SA_TE_AlarmeAlivioPressao = LeituraModbusCoil("ED_SA_TE_AlarmeAlivioPressao", self.__clp["SA"], REG["SA_ED_TE_AlarmeAlivioPressao"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeAlivioPressao.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeAlivioPressao))

        self.leitura_ED_SA_TE_AlarmeTempOleo = LeituraModbusCoil("ED_SA_TE_AlarmeTempOleo", self.__clp["SA"], REG["SA_ED_TE_AlarmeTempOleo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeTempOleo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeTempOleo))

        self.leitura_ED_SA_TE_AlarmeTempEnrolamento = LeituraModbusCoil("ED_SA_TE_AlarmeTempEnrolamento", self.__clp["SA"], REG["SA_ED_TE_AlarmeTempEnrolamento"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeTempEnrolamento.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeTempEnrolamento))

        self.leitura_ED_SA_TE_AlarmeDesligamento = LeituraModbusCoil("ED_SA_TE_AlarmeDesligamento", self.__clp["SA"], REG["SA_ED_TE_AlarmeDesligamento"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeDesligamento.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeDesligamento))

        self.leitura_ED_SA_TE_Falha = LeituraModbusCoil("ED_SA_TE_Falha", self.__clp["SA"], REG["SA_ED_TE_Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_Falha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_TE_Falha))

        self.leitura_ED_SA_FalhaDisjTPsProt = LeituraModbusCoil("ED_SA_FalhaDisjTPsProt", self.__clp["SA"], REG["SA_ED_FalhaDisjTPsProt"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_FalhaDisjTPsProt.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_FalhaDisjTPsProt))

        self.leitura_ED_SA_FalhaDisjTPsSincr = LeituraModbusCoil("ED_SA_FalhaDisjTPsSincr", self.__clp["SA"], REG["SA_ED_FalhaDisjTPsSincr"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_FalhaDisjTPsSincr.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_FalhaDisjTPsSincr))

        self.leitura_ED_SA_CSA1_Secc_Aberta = LeituraModbusCoil("ED_SA_CSA1_Secc_Aberta", self.__clp["SA"], REG["SA_ED_CSA1_Secc_Aberta"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_Secc_Aberta.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_CSA1_Secc_Aberta))

        self.leitura_ED_SA_CSA1_FusivelQueimado = LeituraModbusCoil("ED_SA_CSA1_FusivelQueimado", self.__clp["SA"], REG["SA_ED_CSA1_FusivelQueimado"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_FusivelQueimado.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_CSA1_FusivelQueimado))

        self.leitura_ED_SA_CSA1_FaltaTensao125Vcc = LeituraModbusCoil("ED_SA_CSA1_FaltaTensao125Vcc", self.__clp["SA"], REG["SA_ED_CSA1_FaltaTensao125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_FaltaTensao125Vcc.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_CSA1_FaltaTensao125Vcc))

        self.leitura_ED_SA_QCADE_Nivel4 = LeituraModbusCoil("ED_SA_QCADE_Nivel4", self.__clp["SA"], REG["SA_ED_QCADE_Nivel4"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Nivel4.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCADE_Nivel4))

        self.leitura_ED_SA_QCADE_NivelMuitoAlto = LeituraModbusCoil("ED_SA_QCADE_NivelMuitoAlto", self.__clp["SA"], REG["SA_ED_QCADE_NivelMuitoAlto"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_NivelMuitoAlto.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCADE_NivelMuitoAlto))

        self.leitura_ED_SA_QCADE_Falha220VCA = LeituraModbusCoil("ED_SA_QCADE_Falha220VCA", self.__clp["SA"], REG["SA_ED_QCADE_Falha220VCA"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Falha220VCA.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCADE_Falha220VCA))

        # Verificar
        self.leitura_ED_SA_QCCP_Disj72ETrip = LeituraModbusCoil("ED_SA_QCCP_Disj72ETrip", self.__clp["SA"], REG["SA_ED_QCCP_Disj72ETrip"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_Disj72ETrip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCCP_Disj72ETrip))

        self.leitura_ED_SA_QCCP_Falta125Vcc = LeituraModbusCoil("ED_SA_QCCP_Falta125Vcc", self.__clp["SA"], REG["SA_ED_QCCP_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_Falta125Vcc.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCCP_Falta125Vcc))

        self.leitura_ED_SA_QCCP_TripDisjAgrup = LeituraModbusCoil("ED_SA_QCCP_TripDisjAgrup", self.__clp["SA"], REG["SA_ED_QCCP_TripDisjAgrup"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_TripDisjAgrup.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCCP_TripDisjAgrup))

        self.leitura_ED_SA_QCAP_Falta125Vcc = LeituraModbusCoil("ED_SA_QCAP_Falta125Vcc", self.__clp["SA"], REG["SA_ED_QCAP_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Falta125Vcc.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCAP_Falta125Vcc))

        self.leitura_ED_SA_QCAP_TripDisjAgrup = LeituraModbusCoil("ED_SA_QCAP_TripDisjAgrup", self.__clp["SA"], REG["SA_ED_QCAP_TripDisjAgrup"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_TripDisjAgrup.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCAP_TripDisjAgrup))

        self.leitura_ED_SA_QCAP_Disj52A1Falha = LeituraModbusCoil("ED_SA_QCAP_Disj52A1Falha", self.__clp["SA"], REG["SA_ED_QCAP_Disj52A1Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Disj52A1Falha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCAP_Disj52A1Falha))

        self.leitura_ED_SA_QCAP_Disj52EFalha = LeituraModbusCoil("ED_SA_QCAP_Disj52EFalha", self.__clp["SA"], REG["SA_ED_QCAP_Disj52EFalha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Disj52EFalha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCAP_Disj52EFalha))

        self.leitura_ED_SA_GMG_DisjFechado = LeituraModbusCoil("ED_SA_GMG_DisjFechado", self.__clp["SA"], REG["SA_ED_GMG_DisjFechado"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_GMG_DisjFechado.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_GMG_DisjFechado))

        self.leitura_RD_DJ1_FalhaInt = LeituraModbusCoil("RD_DJ1_FalhaInt", self.__clp["SA"], REG["SA_RD_DJ1_FalhaInt"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_DJ1_FalhaInt.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_DJ1_FalhaInt))

        self.leitura_RD_CLP_Falha = LeituraModbusCoil("RD_CLP_Falha", self.__clp["SA"], REG["SA_RD_FalhaComuCLP"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_CLP_Falha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_CLP_Falha))

        self.leitura_RA_SEL787_Targets = LeituraModbusCoil("RA_SEL787_Targets", self.__clp["SA"], REG["SA_RA_SEL787_Targets"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets))

        self.leitura_RA_SEL787_Targets_Links_Bit00 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit00", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit00"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit00.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit00))

        self.leitura_RA_SEL787_Targets_Links_Bit01 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit01", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit01"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit01.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit01))

        self.leitura_RA_SEL787_Targets_Links_Bit02 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit02", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit02"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit02.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit02))

        self.leitura_RA_SEL787_Targets_Links_Bit03 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit03", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit03"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit03.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit03))

        self.leitura_RA_SEL787_Targets_Links_Bit04 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit04", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit04"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit04.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit04))

        self.leitura_RA_SEL787_Targets_Links_Bit05 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit05", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit05"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit05.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit05))

        self.leitura_RA_SEL787_Targets_Links_Bit06 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit06", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit06"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit06.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit06))

        self.leitura_RA_SEL787_Targets_Links_Bit07 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit07", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit07"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit07.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit07))

        return


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

        self.leitura_voip: "dict[str, LeituraModbus]" = {}

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
            self.condic_dict[f"tmp_nucleo_estator_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_nucleo_estator_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_rad_dia_1_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_rad_dia_1_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_rad_dia_2_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_rad_dia_2_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_rad_tra_1_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_rad_tra_1_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_rad_tra_2_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_rad_tra_2_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_saida_de_ar_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_saida_de_ar_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_guia_escora_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_guia_escora_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_guia_radial_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_guia_radial_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_guia_contra_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_guia_contra_ug{self.__ug_id}"])
            self.condic_dict[f"caixa_espiral_ug{self.__ug_id}"].valor_base = float(parametros[f"alerta_caixa_espiral_ug{self.__ug_id}"])

            self.condic_dict[f"tmp_fase_r_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_fase_s_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_fase_t_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_nucleo_estator_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_nucleo_estator_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_rad_dia_1_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_rad_dia_1_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_rad_dia_2_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_rad_dia_2_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_rad_tra_1_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_rad_tra_1_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_rad_tra_2_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_rad_tra_2_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_saida_de_ar_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_saida_de_ar_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_guia_escora_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_guia_escora_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_guia_radial_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_guia_radial_ug{self.__ug_id}"])
            self.condic_dict[f"tmp_mancal_guia_contra_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_guia_contra_ug{self.__ug_id}"])
            self.condic_dict[f"caixa_espiral_ug{self.__ug_id}"].valor_limite = float(parametros[f"limite_caixa_espiral_ug{self.__ug_id}"])

        except Exception:
            logger.error(f"[OCO-UG{self.__ug_id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores.")
            logger.debug(f"[OCO-UG{self.__ug_id}] Traceback: {traceback.format_exc()}")

    def controle_limites_operacao(self) -> None:
        # TODO adaptar
        ld = self.leitura_dict
        cd = self.condic_dict

        """
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

        if self.leitura_temperatura_fase_R.valor >= self.condicionador_temperatura_fase_r_ug.valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura de Fase R da UG passou do valor base! ({self.condicionador_temperatura_fase_r_ug.valor_base}C) | Leitura: {self.leitura_temperatura_fase_R.valor}C")
        if self.leitura_temperatura_fase_R.valor >= 0.9*(self.condicionador_temperatura_fase_r_ug.valor_limite - self.condicionador_temperatura_fase_r_ug.valor_base) + self.condicionador_temperatura_fase_r_ug.valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura de Fase R da UG está muito próxima do limite! ({self.condicionador_temperatura_fase_r_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_fase_R.valor}C")

        if self.leitura_temperatura_fase_S.valor >= self.condicionador_temperatura_fase_s_ug.valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura de Fase S da UG passou do valor base! ({self.condicionador_temperatura_fase_s_ug.valor_base}C) | Leitura: {self.leitura_temperatura_fase_S.valor}C")
        if self.leitura_temperatura_fase_S.valor >= 0.9*(self.condicionador_temperatura_fase_s_ug.valor_limite - self.condicionador_temperatura_fase_s_ug.valor_base) + self.condicionador_temperatura_fase_s_ug.valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura de Fase S da UG está muito próxima do limite! ({self.condicionador_temperatura_fase_s_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_fase_S.valor}C")

        if self.leitura_temperatura_fase_T.valor >= self.condicionador_temperatura_fase_t_ug.valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura de Fase T da UG passou do valor base! ({self.condicionador_temperatura_fase_t_ug.valor_base}C) | Leitura: {self.leitura_temperatura_fase_T.valor}C")
        if self.leitura_temperatura_fase_T.valor >= 0.9*(self.condicionador_temperatura_fase_t_ug.valor_limite - self.condicionador_temperatura_fase_t_ug.valor_base) + self.condicionador_temperatura_fase_t_ug.valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura de Fase T da UG está muito próxima do limite! ({self.condicionador_temperatura_fase_t_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_fase_T.valor}C")

        if self.leitura_temperatura_nucleo.valor >= self.condicionador_temperatura_nucleo_estator_ug.valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Núcleo Estator da UG passou do valor base! ({self.condicionador_temperatura_nucleo_estator_ug.valor_base}C) | Leitura: {self.leitura_temperatura_nucleo.valor}C")
        if self.leitura_temperatura_nucleo.valor >= 0.9*(self.condicionador_temperatura_nucleo_estator_ug.valor_limite - self.condicionador_temperatura_nucleo_estator_ug.valor_base) + self.condicionador_temperatura_nucleo_estator_ug.valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Núcleo Estator da UG está muito próxima do limite! ({self.condicionador_temperatura_nucleo_estator_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_nucleo.valor}C")

        if self.leitura_temperatura_mrd1.valor >= self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Mancal Radial Dianteiro 1 da UG passou do valor base! ({self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mrd1.valor}C")
        if self.leitura_temperatura_mrd1.valor >= 0.9*(self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_limite - self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_base) + self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Mancal Radial Dianteiro 1 da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mrd1.valor}C")

        if self.leitura_temperatura_mrt1.valor >= self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Mancal Radial Traseiro 1 da UG passou do valor base! ({self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mrt1.valor}C")
        if self.leitura_temperatura_mrt1.valor >= 0.9*(self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_limite - self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_base) + self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Mancal Radial Traseiro 1 da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mrt1.valor}C")

        if self.leitura_temperatura_mrd2.valor >= self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Mancal Radial Dianteiro 2 da UG passou do valor base! ({self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mrd2.valor}C")
        if self.leitura_temperatura_mrd2.valor >= 0.9*(self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_limite - self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_base) + self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Mancal Radial Dianteiro 2 da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mrd2.valor}C")

        if self.leitura_temperatura_mrt2.valor >= self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Mancal Radial Traseiro 2 da UG passou do valor base! ({self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mrt2.valor}C")
        if self.leitura_temperatura_mrt2.valor >= 0.9*(self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_limite - self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_base) + self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Mancal Radial Traseiro 2 da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mrt2.valor}C")

        if self.leitura_temperatura_saida_de_ar.valor >= self.condicionador_temperatura_saida_de_ar_ug.valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura da Saída de Ar da UG passou do valor base! ({self.leitura_temperatura_saida_de_ar.valor}C) | Leitura: {self.condicionador_temperatura_saida_de_ar_ug.valor_base}C")
        if self.leitura_temperatura_saida_de_ar.valor >= 0.9*(self.condicionador_temperatura_saida_de_ar_ug.valor_limite - self.condicionador_temperatura_saida_de_ar_ug.valor_base) + self.condicionador_temperatura_saida_de_ar_ug.valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura da Saída de Ar da UG está muito próxima do limite! ({self.condicionador_temperatura_saida_de_ar_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_saida_de_ar.valor}C")

        if self.leitura_temperatura_guia_radial.valor >= self.condicionador_temperatura_mancal_guia_radial_ug.valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Mancal Guia Radial da UG passou do valor base! ({self.condicionador_temperatura_mancal_guia_radial_ug.valor_base}C) | Leitura: {self.leitura_temperatura_guia_radial.valor}C")
        if self.leitura_temperatura_guia_radial.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_radial_ug.valor_limite - self.condicionador_temperatura_mancal_guia_radial_ug.valor_base) + self.condicionador_temperatura_mancal_guia_radial_ug.valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Mancal Guia Radial da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_guia_radial_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_guia_radial.valor}C")

        if self.leitura_temperatura_guia_escora.valor >= self.condicionador_temperatura_mancal_guia_escora_ug.valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Mancal Guia Escora da UG passou do valor base! ({self.condicionador_temperatura_mancal_guia_escora_ug.valor_base}C) | Leitura: {self.leitura_temperatura_guia_escora.valor}C")
        if self.leitura_temperatura_guia_escora.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_escora_ug.valor_limite - self.condicionador_temperatura_mancal_guia_escora_ug.valor_base) + self.condicionador_temperatura_mancal_guia_escora_ug.valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Mancal Guia Escora da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_guia_escora_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_guia_escora.valor}C")

        if self.leitura_temperatura_guia_contra_escora.valor >= self.condicionador_temperatura_mancal_guia_contra_ug.valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Mancal Guia Contra Escora da UG passou do valor base! ({self.condicionador_temperatura_mancal_guia_contra_ug.valor_base}C) | Leitura: {self.leitura_temperatura_guia_contra_escora.valor}C")
        if self.leitura_temperatura_guia_contra_escora.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_contra_ug.valor_limite - self.condicionador_temperatura_mancal_guia_contra_ug.valor_base) + self.condicionador_temperatura_mancal_guia_contra_ug.valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Mancal Guia Contra Escora da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_guia_contra_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_guia_contra_escora.valor}C")

        if self.leitura_temperatura_oleo_trafo.valor >= self.condicionador_leitura_temperatura_oleo_trafo.valor_base:
            logger.warning(f"[UG{self.__ug_id}] A temperatura do Óleo do Transformador Elevador da UG passou do valor base! ({self.condicionador_leitura_temperatura_oleo_trafo.valor_base}C) | Leitura: {self.leitura_temperatura_oleo_trafo.valor}C")
        if self.leitura_temperatura_oleo_trafo.valor >= 0.9*(self.condicionador_leitura_temperatura_oleo_trafo.valor_limite - self.condicionador_leitura_temperatura_oleo_trafo.valor_base) + self.condicionador_leitura_temperatura_oleo_trafo.valor_base:
            logger.critical(f"[UG{self.__ug_id}] A temperatura do Óleo do Transformador Elevador da UG está muito próxima do limite! ({self.condicionador_leitura_temperatura_oleo_trafo.valor_limite}C) | Leitura: {self.leitura_temperatura_oleo_trafo.valor}C")

        if self.leitura_caixa_espiral.valor <= self.condicionador_caixa_espiral_ug.valor_base and self.leitura_caixa_espiral.valor != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            logger.warning(f"[UG{self.__ug_id}] A pressão Caixa Espiral da UG passou do valor base! ({self.condicionador_caixa_espiral_ug.valor_base:03.2f} KGf/m2) | Leitura: {self.leitura_caixa_espiral.valor:03.2f}")
        if self.leitura_caixa_espiral.valor <= 16.1 and self.leitura_caixa_espiral.valor != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            logger.critical(f"[UG{self.__ug_id}] A pressão Caixa Espiral da UG está muito próxima do limite! ({self.condicionador_caixa_espiral_ug.valor_limite:03.2f} KGf/m2) | Leitura: {self.leitura_caixa_espiral.valor:03.2f} KGf/m2")
        """


    def leitura_temporizada(self) -> None:
        if self.leitura_voip["leitura_ED_FreioPastilhaGasta"].valor != 0 and not vd.voip_dict[f"FREIO_PASTILHA_GASTA_UG{self.__ug_id}"][0]:
            logger.warning(f"[UG{self.__ug_id}] O sensor de Freio da UG retornou que a Pastilha está gasta, favor considerar troca.")
            vd.voip_dict[f"FREIO_PASTILHA_GASTA_UG{self.__ug_id}"][0] = True
        elif self.leitura_voip["leitura_ED_FreioPastilhaGasta"].valor == 0 and vd.voip_dict[f"FREIO_PASTILHA_GASTA_UG{self.__ug_id}"][0]:
            vd.voip_dict[f"FREIO_PASTILHA_GASTA_UG{self.__ug_id}"][0] = False

        if self.leitura_voip["leitura_ED_FiltroPresSujo75Troc"].valor != 0 and not vd.voip_dict[f"FILTRO_PRES_SUJO_75_TROC_UG{self.__ug_id}"][0]:
            logger.warning(f"[UG{self.__ug_id}] O sensor do Filtro de Pressão UHRV retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"FILTRO_PRES_SUJO_75_TROC_UG{self.__ug_id}"][0] = True
        elif self.leitura_voip["leitura_ED_FiltroPresSujo75Troc"].valor == 0 and vd.voip_dict[f"FILTRO_PRES_SUJO_75_TROC_UG{self.__ug_id}"][0]:
            vd.voip_dict[f"FILTRO_PRES_SUJO_75_TROC_UG{self.__ug_id}"][0] = False

        if self.leitura_voip["leitura_ED_FiltroRetSujo75Troc"].valor != 0 and not vd.voip_dict[f"FILTRO_RET_SUJO_75_TROC_UG{self.__ug_id}"][0]:
            logger.warning(f"[UG{self.__ug_id}] O sensor do Filtro de Retorno UHRV retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"FILTRO_RET_SUJO_75_TROC_UG{self.__ug_id}"][0] = True
        elif self.leitura_voip["leitura_ED_FiltroRetSujo75Troc"].valor == 0 and vd.voip_dict[f"FILTRO_RET_SUJO_75_TROC_UG{self.__ug_id}"][0]:
            vd.voip_dict[f"FILTRO_RET_SUJO_75_TROC_UG{self.__ug_id}"][0] = False

        if self.leitura_voip["leitura_ED_UHLMFilt1PresSujo75Troc"].valor != 0 and not vd.voip_dict[f"UHLM_FILTR_1_PRES_SUJO_75_TROC_UG{self.__ug_id}"][0]:
            logger.warning(f"[UG{self.__ug_id}] O sensor do Filtro 1 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"UHLM_FILTR_1_PRES_SUJO_75_TROC_UG{self.__ug_id}"][0] = True
        elif self.leitura_voip["leitura_ED_UHLMFilt1PresSujo75Troc"].valor == 0 and vd.voip_dict[f"UHLM_FILTR_1_PRES_SUJO_75_TROC_UG{self.__ug_id}"][0]:
            vd.voip_dict[f"UHLM_FILTR_1_PRES_SUJO_75_TROC_UG{self.__ug_id}"][0] = False

        if self.leitura_voip["leitura_ED_UHLMFilt2PresSujo75Troc"].valor != 0 and not vd.voip_dict[f"UHLM_FILTR_2_PRES_SUJO_75_TROC_UG{self.__ug_id}"][0]:
            logger.warning(f"[UG{self.__ug_id}] O sensor do Filtro 2 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"UHLM_FILTR_2_PRES_SUJO_75_TROC_UG{self.__ug_id}"][0] = True
        elif self.leitura_voip["leitura_ED_UHLMFilt2PresSujo75Troc"].valor == 0 and vd.voip_dict[f"UHLM_FILTR_2_PRES_SUJO_75_TROC_UG{self.__ug_id}"][0]:
            vd.voip_dict[f"UHLM_FILTR_2_PRES_SUJO_75_TROC_UG{self.__ug_id}"][0] = False

        if self.leitura_voip["leitura_ED_FiltroPressaoBbaMecSj75"].valor != 0 and not vd.voip_dict[f"FILTRO_PRESSAO_BBA_MEC_SJ_75_UG{self.__ug_id}"][0]:
            logger.warning(f"[UG{self.__ug_id}] O sensor do Filtro de Pressão da Bomba Mecânica retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"FILTRO_PRESSAO_BBA_MEC_SJ_75_UG{self.__ug_id}"][0] = True
        elif self.leitura_voip["leitura_ED_FiltroPressaoBbaMecSj75"].valor == 0 and vd.voip_dict[f"FILTRO_PRESSAO_BBA_MEC_SJ_75_UG{self.__ug_id}"][0]:
            vd.voip_dict[f"FILTRO_PRESSAO_BBA_MEC_SJ_75_UG{self.__ug_id}"][0] = False

        if self.leitura_voip["leitura_ED_TripPartRes"].valor != 0 and not vd.voip_dict[f"TRIP_PART_RES_UG{self.__ug_id}"][0]:
            logger.warning(f"[UG{self.__ug_id}] O sensor TripPartRes retornou valor 1.")
            vd.voip_dict[f"TRIP_PART_RES_UG{self.__ug_id}"][0] = True
        elif self.leitura_voip["leitura_ED_TripPartRes"].valor == 0 and vd.voip_dict[f"TRIP_PART_RES_UG{self.__ug_id}"][0]:
            vd.voip_dict[f"TRIP_PART_RES_UG{self.__ug_id}"][0] = False

        if self.leitura_voip["leitura_ED_FreioCmdRemoto"].valor != 1:
            logger.debug(f"[UG{self.__ug_id}] O freio da UG saiu do modo remoto, favor analisar a situação.")

        if self.leitura_voip[f"leitura_ED_QCAUG{self.__ug_id}_Remoto"].valor != 1:
            logger.debug(f"[UG{self.__ug_id}] O compressor da UG saiu do modo remoto, favor analisar a situação.")

        return

    def carregar_leituras(self) -> None:
        # Leituras de condicionadores com limites de operção checados a cada ciclo
        self.leitura_voip["leitura_ED_FreioPastilhaGasta"] = LeituraModbusCoil(
            "ED_FreioPastilhaGasta",
            self.__clp[f"UG{self.__ug_id}"],
            REG[f"UG{self.__ug_id}_ED_FreioPastilhaGasta"]
        )
        self.leitura_voip["leitura_ED_FiltroPresSujo75Troc"] = LeituraModbusCoil(
            "ED_FiltroPresSujo75Troc",
            self.__clp[f"UG{self.__ug_id}"],
            REG[f"UG{self.__ug_id}_ED_FiltroPresSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_FiltroRetSujo75Troc"] = LeituraModbusCoil(
            "ED_FiltroRetSujo75Troc",
            self.__clp[f"UG{self.__ug_id}"],
            REG[f"UG{self.__ug_id}_ED_FiltroRetSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_UHLMFilt1PresSujo75Troc"] = LeituraModbusCoil(
            "ED_UHLMFilt1PresSujo75Troc",
            self.__clp[f"UG{self.__ug_id}"],
            REG[f"UG{self.__ug_id}_ED_UHLMFilt1PresSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_UHLMFilt2PresSujo75Troc"] = LeituraModbusCoil(
            "ED_UHLMFilt2PresSujo75Troc",
            self.__clp[f"UG{self.__ug_id}"],
            REG[f"UG{self.__ug_id}_ED_UHLMFilt2PresSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_FiltroPressaoBbaMecSj75"] = LeituraModbusCoil(
            "ED_FiltroPressaoBbaMecSj75",
            self.__clp[f"UG{self.__ug_id}"],
            REG[f"UG{self.__ug_id}_ED_Filt1PresBbaMecSj75Troc"]
        )
        self.leitura_voip["leitura_ED_TripPartRes"] = LeituraModbusCoil(
            "ED_TripPartRes",
            self.__clp[f"UG{self.__ug_id}"],
            REG[f"UG{self.__ug_id}_ED_TripPartRes"]
        )
        self.leitura_voip["leitura_ED_FreioCmdRemoto"] = LeituraModbusCoil(
            "ED_FreioCmdRemoto",
            self.__clp[f"UG{self.__ug_id}"],
            REG[f"UG{self.__ug_id}_ED_FreioCmdRemoto"]
        )
        self.leitura_voip[f"leitura_ED_QCAUG{self.__ug_id}_Remoto"] = LeituraModbusCoil(
            f"ED_QCAUG{self.__ug_id}_Remoto",
            self.__clp[f"UG{self.__ug_id}"],
            REG[f"UG{self.__ug_id}_ED_QCAUG{self.__ug_id}_Remoto"]
        )

        ### CONDICIONADORES ESSENCIAIS
        # R
        self.leitura_temperatura_fase_R = LeituraModbus("Temperatura fase R", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RA_Temperatura_01"], op=4)
        self.condicionador_temperatura_fase_r_ug = CondicionadorExponencial(self.leitura_temperatura_fase_R.descr, CONDIC_INDISPONIBILIZAR, self.leitura_temperatura_fase_R, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_r_ug)

        # S
        self.leitura_temperatura_fase_S = LeituraModbus("Temperatura fase S", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RA_Temperatura_02"], op=4)
        self.condicionador_temperatura_fase_s_ug = CondicionadorExponencial(self.leitura_temperatura_fase_S.descr, CONDIC_INDISPONIBILIZAR, self.leitura_temperatura_fase_S, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_s_ug)

        # T
        self.leitura_temperatura_fase_T = LeituraModbus("Temperatura fase T", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RA_Temperatura_03"], op=4)
        self.condicionador_temperatura_fase_t_ug = CondicionadorExponencial(self.leitura_temperatura_fase_T.descr, CONDIC_INDISPONIBILIZAR, self.leitura_temperatura_fase_T, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_t_ug)

        # Nucleo estator
        self.leitura_temperatura_nucleo = LeituraModbus("Temperatura núcelo do estator", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RA_Temperatura_04"], op=4)
        self.condicionador_temperatura_nucleo_estator_ug = CondicionadorExponencial(self.leitura_temperatura_nucleo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_temperatura_nucleo, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_nucleo_estator_ug)

        # MRD 1
        self.leitura_temperatura_mrd1 = LeituraModbus("Temperatura mancal radial dianteiro", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RA_Temperatura_05"], op=4)
        self.condicionador_temperatura_mancal_rad_dia_1_ug = CondicionadorExponencial(self.leitura_temperatura_mrd1.descr, CONDIC_INDISPONIBILIZAR, self.leitura_temperatura_mrd1, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_dia_1_ug)

        # MRT 1
        self.leitura_temperatura_mrt1 = LeituraModbus("Temperatura mancal radial traseiro", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RA_Temperatura_06"], op=4)
        self.condicionador_temperatura_mancal_rad_tra_1_ug = CondicionadorExponencial(self.leitura_temperatura_mrt1.descr, CONDIC_INDISPONIBILIZAR, self.leitura_temperatura_mrt1, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_tra_1_ug)

        # MRD 2
        self.leitura_temperatura_mrd2 = LeituraModbus("Temperatura mancal radial dianteiro 2", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RA_Temperatura_07"], op=4)
        self.condicionador_temperatura_mancal_rad_dia_2_ug = CondicionadorExponencial(self.leitura_temperatura_mrd2.descr, CONDIC_INDISPONIBILIZAR, self.leitura_temperatura_mrd2, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_dia_2_ug)

        # MRT 2
        self.leitura_temperatura_mrt2 = LeituraModbus("Temperatura mancal radial traseiro 2", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RA_Temperatura_08"], op=4)
        self.condicionador_temperatura_mancal_rad_tra_2_ug = CondicionadorExponencial(self.leitura_temperatura_mrt2.descr, CONDIC_INDISPONIBILIZAR, self.leitura_temperatura_mrt2, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_tra_2_ug)

        # Saída de ar
        self.leitura_temperatura_saida_de_ar = LeituraModbus("Saída de ar", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RA_Temperatura_10"], op=4)
        self.condicionador_temperatura_saida_de_ar_ug = CondicionadorExponencial(self.leitura_temperatura_saida_de_ar.descr, CONDIC_INDISPONIBILIZAR, self.leitura_temperatura_saida_de_ar, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_saida_de_ar_ug)

        # Mancal Guia Radial
        self.leitura_temperatura_guia_radial = LeituraModbus("Mancal Guia Radial", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RA_TempMcGuiaRadial"])
        self.condicionador_temperatura_mancal_guia_radial_ug = CondicionadorExponencial(self.leitura_temperatura_guia_radial.descr, CONDIC_INDISPONIBILIZAR, self.leitura_temperatura_guia_radial, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_radial_ug)

        # Mancal Guia escora
        self.leitura_temperatura_guia_escora = LeituraModbus("Mancal Guia escora", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RA_TempMcGuiaEscora"])
        self.condicionador_temperatura_mancal_guia_escora_ug = CondicionadorExponencial(self.leitura_temperatura_guia_escora.descr, CONDIC_INDISPONIBILIZAR, self.leitura_temperatura_guia_escora, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_escora_ug)

        # Mancal Guia contra_escora
        self.leitura_temperatura_guia_contra_escora = LeituraModbus("Mancal Guia contra_escora", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RA_TempMcGuiaContraEscora"])
        self.condicionador_temperatura_mancal_guia_contra_ug = (CondicionadorExponencial(self.leitura_temperatura_guia_contra_escora.descr, CONDIC_INDISPONIBILIZAR, self.leitura_temperatura_guia_contra_escora, 100, 200))
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_contra_ug)

        # Óleo do Transformador Elevador
        self.leitura_temperatura_oleo_trafo = LeituraModbus("Óleo do Transformador Elevador", self.__clp["SA"], REG["SA_EA_TE_TempOleo"], escala=0.1, op=4)
        self.condicionador_leitura_temperatura_oleo_trafo = CondicionadorExponencial(self.leitura_temperatura_oleo_trafo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_temperatura_oleo_trafo, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_leitura_temperatura_oleo_trafo)

        ## Comandos Digitais
        # GERAL
        self.leitura_CD_EmergenciaViaSuper = LeituraModbusCoil("CD_EmergenciaViaSuper", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_CD_EmergenciaViaSuper"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_CD_EmergenciaViaSuper.descr, CONDIC_NORMALIZAR, self.leitura_CD_EmergenciaViaSuper))

        ## Retornos Digitais
        # TRIPS
        self.leitura_RD_TripEletrico = LeituraModbusCoil("RD_TripEletrico", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_TripEletrico"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_RD_TripEletrico.descr, CONDIC_NORMALIZAR, self.leitura_RD_TripEletrico))

        self.leitura_RD_700G_Trip = LeituraModbusCoil("RD_700G_Trip", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_700G_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_RD_700G_Trip.descr, CONDIC_NORMALIZAR, self.leitura_RD_700G_Trip, self.__ug_id))

        self.leitura_RD_TripMecanico = LeituraModbusCoil("RD_TripMecanico", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_TripMecanico"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_RD_TripMecanico.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripMecanico))

        ## Entradas Digitais
        # TRIPS
        self.leitura_ED_RV_Trip = LeituraModbusCoil("ED_RV_Trip", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_RV_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_RV_Trip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_RV_Trip))

        self.leitura_ED_AVR_Trip = LeituraModbusCoil("ED_AVR_Trip", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_AVR_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_AVR_Trip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_AVR_Trip))

        # RELÉS
        self.leitura_ED_SEL700G_Atuado = LeituraModbusCoil("ED_SEL700G_Atuado", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_SEL700G_Atuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SEL700G_Atuado.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SEL700G_Atuado))

        self.leitura_ED_ReleBloqA86MAtuado = LeituraModbusCoil("ED_ReleBloqA86MAtuado", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_ReleBloqA86MAtuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_ReleBloqA86MAtuado.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_ReleBloqA86MAtuado))

        self.leitura_ED_ReleBloqA86HAtuado = LeituraModbusCoil("ED_ReleBloqA86HAtuado", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_ReleBloqA86HAtuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_ReleBloqA86HAtuado.descr, CONDIC_NORMALIZAR, self.leitura_ED_ReleBloqA86HAtuado, self.__ug_id, [UG_SINCRONIZADA]))


        ### CONDICIONADORES NORMAIS
        # Entradas Digitais
        # SA -> UG
        self.leitura_ED_SA_FalhaDisjTPsSincrG2 = LeituraModbusCoil(f"ED_SA_FalhaDisjTPsSincrG{self.__ug_id}", self.__clp["SA"], REG["SA_ED_FalhaDisjTPsSincrG2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_FalhaDisjTPsSincrG2.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_FalhaDisjTPsSincrG2))

        self.leitura_ED_SA_DisjDJ1_AlPressBaixa = LeituraModbusCoil("ED_SA_DisjDJ1_AlPressBaixa", self.__clp["SA"], REG["SA_ED_DisjDJ1_AlPressBaixa"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_DisjDJ1_AlPressBaixa.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_DisjDJ1_AlPressBaixa))

        self.leitura_ED_SA_DisjDJ1_BloqPressBaixa = LeituraModbusCoil("ED_SA_DisjDJ1_BloqPressBaixa", self.__clp["SA"], REG["SA_ED_DisjDJ1_BloqPressBaixa"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_DisjDJ1_BloqPressBaixa.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_DisjDJ1_BloqPressBaixa))

        # TRIPS
        self.leitura_ED_UHRV_TripBomba1 = LeituraModbusCoil("ED_UHRV_TripBomba1", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_UHRV_TripBomba1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_TripBomba1.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHRV_TripBomba1))

        self.leitura_ED_UHRV_TripBomba2 = LeituraModbusCoil("ED_UHRV_TripBomba2", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_UHRV_TripBomba2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_TripBomba2.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHRV_TripBomba2))

        self.leitura_ED_UHLM_TripBomba1 = LeituraModbusCoil("ED_UHLM_TripBomba1", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_UHLM_TripBomba1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_TripBomba1.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_TripBomba1))

        self.leitura_ED_UHLM_TripBomba2 = LeituraModbusCoil("ED_UHLM_TripBomba2", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_UHLM_TripBomba2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_TripBomba2.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_TripBomba2))

        self.leitura_ED_QCAUG_TripDisj52A1 = LeituraModbusCoil("ED_QCAUG_TripDisj52A1", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_QCAUG_TripDisj52A1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_QCAUG_TripDisj52A1.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_QCAUG_TripDisj52A1))

        self.leitura_ED_TripAlimPainelFreio = LeituraModbusCoil("ED_TripAlimPainelFreio", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_TripAlimPainelFreio"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_TripAlimPainelFreio.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_TripAlimPainelFreio))

        self.leitura_ED_QCAUG_TripDisjAgrup = LeituraModbusCoil("ED_QCAUG_TripDisjAgrup", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_QCAUG_TripDisjAgrup"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_QCAUG_TripDisjAgrup.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_QCAUG_TripDisjAgrup))

        # FALHAS
        self.leitura_ED_AVR_FalhaInterna = LeituraModbusCoil("ED_AVR_FalhaInterna", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_AVR_FalhaInterna"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_AVR_FalhaInterna.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_AVR_FalhaInterna))

        self.leitura_ED_SEL700G_FalhaInterna = LeituraModbusCoil("ED_SEL700G_FalhaInterna", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_SEL700G_FalhaInterna"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SEL700G_FalhaInterna.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SEL700G_FalhaInterna))

        self.leitura_ED_QCAUG_Falha380VcaPainel = LeituraModbusCoil("ED_QCAUG_Falha380VcaPainel", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_QCAUG_Falha380VcaPainel"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_QCAUG_Falha380VcaPainel.descr, CONDIC_NORMALIZAR, self.leitura_ED_QCAUG_Falha380VcaPainel))

        # FALTAS
        self.leitura_ED_Falta125Vcc = LeituraModbusCoil("ED_Falta125Vcc", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_Falta125Vcc.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_Falta125Vcc))

        self.leitura_ED_Falta125VccCom = LeituraModbusCoil("ED_Falta125VccCom", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_Falta125VccCom"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_Falta125VccCom.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_Falta125VccCom))

        self.leitura_ED_FaltaFluxoOleoMc = LeituraModbusCoil("ED_FaltaFluxoOleoMc", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_FaltaFluxoOleoMc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FaltaFluxoOleoMc.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_FaltaFluxoOleoMc))

        self.leitura_ED_Falta125VccAlimVal = LeituraModbusCoil("ED_Falta125VccAlimVal", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_Falta125VccAlimVal"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_Falta125VccAlimVal.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_Falta125VccAlimVal))

        self.leitura_ED_UHLM_FaltaFluxTroc = LeituraModbusCoil("ED_UHLM_FaltaFluxTroc", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_UHLM_FaltaFluxTroc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FaltaFluxTroc.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_FaltaFluxTroc))

        self.leitura_ED_UHLM_FaltaPressTroc = LeituraModbusCoil("ED_UHLM_FaltaPressTroc", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_UHLM_FaltaPressTroc"]) # TODO retornar para DEVE_INDISPONIBILZIAR
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FaltaPressTroc.descr, CONDIC_NORMALIZAR, self.leitura_ED_UHLM_FaltaPressTroc))

        # Controle UHRV
        self.leitura_ED_UHRV_NivOleominimoPos36 = LeituraModbusCoil("ED_UHRV_NivOleominimoPos36", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_UHRV_NivOleominimoPos36"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_NivOleominimoPos36.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHRV_NivOleominimoPos36))

        self.leitura_ED_UHRV_NivOleoCriticoPos35 = LeituraModbusCoil("ED_UHRV_NivOleoCriticoPos35", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_UHRV_NivOleoCriticoPos35"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_NivOleoCriticoPos35.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHRV_NivOleoCriticoPos35))

        # Controle UHLM
        self.leitura_ED_UHLM_FluxoMcTras = LeituraModbusCoil("ED_UHLM_FluxoMcTras", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_UHLM_FluxoMcTras"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FluxoMcTras.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_FluxoMcTras))

        self.leitura_ED_UHLM_NivelminOleo = LeituraModbusCoil("ED_UHLM_NivelminOleo", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_UHLM_NivelminOleo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_NivelminOleo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_NivelminOleo))

        self.leitura_ED_UHLM_NivelCritOleo = LeituraModbusCoil("ED_UHLM_NivelCritOleo", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_UHLM_NivelCritOleo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_NivelCritOleo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_NivelCritOleo))

        self.leitura_ED_UHLM_FluxoMcDianteiro = LeituraModbusCoil("ED_UHLM_FluxoMcDianteiro", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_UHLM_FluxoMcDiant"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FluxoMcDianteiro.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_FluxoMcDianteiro))

        self.leitura_ED_UHLM_Filt1PresSujo100Sujo = LeituraModbusCoil("ED_UHLM_Filt1PresSujo100Sujo", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_UHLMFilt1PresSujoSujo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_Filt1PresSujo100Sujo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_Filt1PresSujo100Sujo))

        self.leitura_ED_UHLM_Filt2PresSujo100Sujo = LeituraModbusCoil("ED_UHLM_Filt2PresSujo100Sujo", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_UHLMFilt2PresSujoSujo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_Filt2PresSujo100Sujo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_Filt2PresSujo100Sujo))

        # Controle Freios
        self.leitura_ED_FreioSemEnergia = LeituraModbusCoil("ED_FreioSemEnergia", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_FreioSemEnergia"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FreioSemEnergia.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_FreioSemEnergia))

        self.leitura_ED_FreioFiltroSaturado = LeituraModbusCoil("ED_FreioFiltroSaturado", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_FreioFiltroSaturado"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FreioFiltroSaturado.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_FreioFiltroSaturado))

        # Controle Filtros
        self.leitura_ED_FiltroRetSujo100Sujo = LeituraModbusCoil("ED_FiltroRetSujo100Sujo", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_FiltroRetSujoSujo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FiltroRetSujo100Sujo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_FiltroRetSujo100Sujo))

        self.leitura_ED_FiltroPresSujo100Sujo = LeituraModbusCoil("ED_FiltroPresSujo100Sujo", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_FiltroPresSujoSujo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FiltroPresSujo100Sujo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_FiltroPresSujo100Sujo))

        self.leitura_ED_FiltroPressaoBbaMecSj100 = LeituraModbusCoil("ED_FiltroPressaoBbaMecSj100", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_Filt1PresBbaMecSjSujo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FiltroPressaoBbaMecSj100.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_FiltroPressaoBbaMecSj100))

        # Outros
        self.leitura_ED_PalhetasDesal = LeituraModbusCoil("ED_PalhetasDesal", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_PalhetasDesal"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_PalhetasDesal.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_PalhetasDesal))

        self.leitura_ED_ValvBorbTravada = LeituraModbusCoil("ED_ValvBorbTravada", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_ValvBorbTravadaFechada"],)
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_ValvBorbTravada.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_ValvBorbTravada))

        self.leitura_ED_SobreVeloMecPos18 = LeituraModbusCoil("ED_SobreVeloMecPos18", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_SobreVeloMecPos18"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SobreVeloMecPos18.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SobreVeloMecPos18))

        self.leitura_ED_NivelMAltoPocoDren = LeituraModbusCoil("ED_NivelMAltoPocoDren", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_ED_NivelMAltoPocoDren"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_NivelMAltoPocoDren.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_NivelMAltoPocoDren))


        ## Retornos Digitais
        # TRIPS
        self.leitura_RD_TripVibr1 = LeituraModbusCoil("RD_TripVibr1", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_TripVibr1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripVibr1.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripVibr1))

        self.leitura_RD_TripVibr2 = LeituraModbusCoil("RD_TripVibr2", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_TripVibr2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripVibr2.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripVibr2))

        self.leitura_RD_TripTempUHRV = LeituraModbusCoil("RD_TripTempUHRV", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_TripTempUHRV"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempUHRV.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripTempUHRV))

        self.leitura_RD_TripTempUHLM = LeituraModbusCoil("RD_TripTempUHLM", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_TripTempUHLM"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempUHLM.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripTempUHLM))

        self.leitura_RD_TripTempGaxeteiro = LeituraModbusCoil("RD_TripTempGaxeteiro", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_TripTempGaxeteiro"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempGaxeteiro.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripTempGaxeteiro))

        self.leitura_RD_TripTempMcGuiaRadial = LeituraModbusCoil("RD_TripTempMcGuiaRadial", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_TripTempMcGuiaRadial"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempMcGuiaRadial.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripTempMcGuiaRadial))

        self.leitura_RD_TripTempMcGuiaEscora = LeituraModbusCoil("RD_TripTempMcGuiaEscora", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_TripTempMcGuiaEscora"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempMcGuiaEscora.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripTempMcGuiaEscora))

        self.leitura_RD_TripTempMcGuiaContraEscora = LeituraModbusCoil("RD_TripTempMcGuiaContraEscora", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_TripTempMcGuiaContraEscora"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempMcGuiaContraEscora.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripTempMcGuiaContraEscora))

        # Retornos Digitais - FALHAS
        self.leitura_RD_CLP_Falha = LeituraModbusCoil("RD_CLP_Falha", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_FalhaComuCLP"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_CLP_Falha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_CLP_Falha))

        self.leitura_RD_Q_Negativa = LeituraModbusCoil("RD_Q_Negativa", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_IHM_Q_Negativa"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_Q_Negativa.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_Q_Negativa))

        self.leitura_RD_Remota_Falha = LeituraModbusCoil("RD_Remota_Falha", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_FalhaComuRemota"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_Remota_Falha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_Remota_Falha))

        self.leitura_RD_FalhaIbntDisjGer = LeituraModbusCoil("RD_FalhaIbntDisjGer", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_FalhaIbntDisjGer"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_FalhaIbntDisjGer.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_FalhaIbntDisjGer))

        self.leitura_RD_UHRV_FalhaAcionBbaM1 = LeituraModbusCoil("RD_UHRV_FalhaAcionBbaM1", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_UHRV_FalhaAcionBbaM1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHRV_FalhaAcionBbaM1.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_UHRV_FalhaAcionBbaM1))

        self.leitura_RD_UHRV_FalhaAcionBbaM2 = LeituraModbusCoil("RD_UHRV_FalhaAcionBbaM2", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_UHRV_FalhaAcionBbaM2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHRV_FalhaAcionBbaM2.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_UHRV_FalhaAcionBbaM2))

        self.leitura_RD_UHLM_FalhaAcionBbaM1 = LeituraModbusCoil("RD_UHLM_FalhaAcionBbaM1", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_UHLM_FalhaAcionBbaM1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHLM_FalhaAcionBbaM1.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_UHLM_FalhaAcionBbaM1))

        self.leitura_RD_UHLM_FalhaAcionBbaM2 = LeituraModbusCoil("RD_UHLM_FalhaAcionBbaM2", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_UHLM_FalhaAcionBbaM2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHLM_FalhaAcionBbaM2.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_UHLM_FalhaAcionBbaM2))

        self.leitura_RD_FalhaAcionFechaValvBorb = LeituraModbusCoil("RD_FalhaAcionFechaValvBorb", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_FalhaAcionFechaValvBorb"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_FalhaAcionFechaValvBorb.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_FalhaAcionFechaValvBorb))

        self.leitura_RD_FalhaAcionFechaValvBorb = LeituraModbusCoil("RD_FalhaAcionFechaValvBorb", self.__clp[f"UG{self.__ug_id}"], REG[f"UG{self.__ug_id}_RD_FalhaAcionFechaValvBorb"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_FalhaAcionFechaValvBorb.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_FalhaAcionFechaValvBorb))
