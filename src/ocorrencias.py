import pytz
import logging
import traceback

import src.mensageiro.dict as vd
import src.dicionarios.dict as d

from time import time
from datetime import datetime

from src.funcoes.leitura import *
from src.Condicionadores import *
from src.dicionarios.reg import *
from src.dicionarios.const import *

from src.banco_dados import BancoDados


logger = logging.getLogger("__main__")

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
    def condicionadores(self, var: "list[CondicionadorBase]") -> None:
        # SETTER -> Atrubui a nova lista de condicionadores da Usina.

        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[CondicionadorBase]":
        # PROPRIEDADE -> Retrona a lista de condicionadores essenciais da Usina.

        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[CondicionadorBase]") -> None:
        # SETTER -> Atrubui a nova lista de condicionadores essenciais da Usina.

        self._condicionadores_essenciais = var

    def verificar_condicionadores(self) -> int:
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

            for condic in condicionadores_ativos:
                v = [datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descr]
                self.__db.update_alarmes(v)

            return flag
        return flag

    def leitura_temporizada(self) -> None:
        """
        Função para consulta de acionamentos da usina e avisos através do mecanismo
        de acionamento temporizado.
        """

        if self.leitura_ED_SA_QLCF_Disj52ETrip.valor != 0:
            logger.warning("[OCO-USN] O Disjuntor do Gerador Diesel de Emergência QLCF identificou um sinal de TRIP, favor verificar.")

        if self.leitura_ED_SA_QLCF_TripDisjAgrup.valor != 0:
            logger.warning("[OCO-USN] O sensor do Disjuntor de Agrupamento QLCF identificou um sinal de trip, favor verificar.")

        if self.leitura_ED_SA_QCAP_SubtensaoBarraGeral.valor != 0:
            logger.warning("[OCO-USN] O sensor de Subtensão do Barramento Geral QCAP foi acionado, favor verificar.")

        if self.leitura_ED_SA_GMG_Alarme.valor != 0:
            logger.warning("[OCO-USN] O alarme do Grupo Motor Gerador foi acionado, favor verificar.")

        if self.leitura_ED_SA_GMG_Trip.valor != 0:
            logger.warning("[OCO-USN] O sensor de TRIP do Grupo Motor Gerador foi acionado, favor verificar.")

        if self.leitura_ED_SA_GMG_Operacao.valor != 0:
            logger.warning("[OCO-USN] O sensor de operação do Grupo Motor Gerador foi acionado, favor verificar.")

        if self.leitura_ED_SA_GMG_BaixoComb.valor != 0:
            logger.warning("[OCO-USN] O sensor de de combustível do Grupo Motor Gerador retornou que o nível está baixo, favor reabastercer o gerador.")

        if self.leitura_RD_BbaDren1_FalhaAcion.valor != 0:
            logger.warning("[OCO-USN] O sensor da Bomba de Drenagem 1 identificou uma falha no acionamento, favor verificar.")

        if self.leitura_RD_BbaDren2_FalhaAcion.valor != 0:
            logger.warning("[OCO-USN] O sensor da Bomba de Drenagem 2 identificou uma falha no acionamento, favor verificar.")

        if self.leitura_RD_BbaDren3_FalhaAcion.valor != 0:
            logger.warning("[OCO-USN] O sensor da Bomba de Drenagem 3 identificou uma falha no acionamento, favor verificar.")

        if self.leitura_RD_SA_GMG_FalhaAcion.valor != 0:
            logger.warning("[OCO-USN] O sensor do Grupo Motor Gerador identificou uma falha no acionamento, favor verificar.")

        if self.leitura_RD_FalhaComunSETDA.valor != 0 and not vd.voip_dict["FALHA_COMUM_SETDA"][0]:
            logger.warning("[OCO-USN] Houve uma falha de comunicação com o CLP da Subestação e o CLP da Tomada da Água, favor verificar")
            vd.voip_dict["FALHA_COMUM_SETDA"][0] = True
        elif self.leitura_RD_FalhaComunSETDA.valor == 0 and vd.voip_dict["FALHA_COMUM_SETDA"][0]:
            vd.voip_dict["FALHA_COMUM_SETDA"][0] = False
            vd.voip_dict["FALHA_COMUM_SETDA"][1] = 0

        if self.leitura_ED_SA_QCAP_Disj52EFechado.valor != 0 and not vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0]:
            logger.warning("[OCO-USN] O Disjuntor do Gerador Diesel de Emergência QLCF foi fechado.")
            vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0] = True
        elif self.leitura_ED_SA_QCAP_Disj52EFechado.valor == 0 and vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0]:
            vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0] = False
            vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][1] = 0

        if self.leitura_ED_SA_QCADE_BombasDng_Auto.valor != 1 and not vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0]:
            logger.warning("[OCO-USN] O poço de drenagem da Usina entrou em modo remoto, favor verificar.")
            vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0] = True
        elif self.leitura_ED_SA_QCADE_BombasDng_Auto.valor == 1 and vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0]:
            vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0] = False
            vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][1] = 0

        return

    def carregar_leituras(self) -> None:
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """

        ### Leituras para acionamento temporizado por chamada Voip
        ## CONDICIONADORES ESSENCIAIS
                # Leituras para acionamento periódico
        self.leitura_ED_SA_GMG_Trip = LeituraModbusCoil("[USN] Grupo Motor Gerador Trip", self.__clp["SA"], REG["SA_ED_GMG_Trip"])
        self.leitura_ED_SA_GMG_Alarme = LeituraModbusCoil("[USN] Grupo Motor Gerador Alarme", self.__clp["SA"], REG["SA_ED_GMG_Alarme"])
        self.leitura_ED_SA_GMG_Operacao = LeituraModbusCoil("[USN] Grupo Motor Gerador Operação", self.__clp["SA"], REG["SA_ED_GMG_Operacao"])
        self.leitura_RD_FalhaComunSETDA = LeituraModbusCoil("[USN] CLP TDA Falha", self.__clp["SA"], REG["SA_RD_FalhaComunSETDA"])
        self.leitura_ED_SA_GMG_BaixoComb = LeituraModbusCoil("[USN] ED_SA_GMG_BaixoComb", self.__clp["SA"], REG["SA_ED_GMG_BaixoComb"])
        self.leitura_RD_SA_GMG_FalhaAcion = LeituraModbusCoil("[USN] Grupo Motor Gerador Falha Acionamento", self.__clp["SA"], REG["SA_RD_GMG_FalhaAcion"])
        self.leitura_ED_SA_QLCF_Disj52ETrip = LeituraModbusCoil("[USN] Disjuntor 52E Trip", self.__clp["SA"], REG["SA_ED_QLCF_Disj52ETrip"])
        self.leitura_RD_BbaDren1_FalhaAcion = LeituraModbusCoil("[USN] Bomba Drenagem 1 Falha Acionamento", self.__clp["SA"], REG["SA_RD_BbaDren1_FalhaAcion"])
        self.leitura_RD_BbaDren2_FalhaAcion = LeituraModbusCoil("[USN] Bomba Drenagem 2 Falha Acionamento", self.__clp["SA"], REG["SA_RD_BbaDren2_FalhaAcion"])
        self.leitura_RD_BbaDren3_FalhaAcion = LeituraModbusCoil("[USN] Bomba Drenagem 3 Falha Acionamento", self.__clp["SA"], REG["SA_RD_BbaDren3_FalhaAcion"])
        self.leitura_ED_SA_QLCF_TripDisjAgrup = LeituraModbusCoil("[USN] Disjuntor Agrupamento Trip", self.__clp["SA"], REG["SA_ED_QLCF_TripDisjAgrup"])
        self.leitura_ED_SA_QCAP_Disj52EFechado = LeituraModbusCoil("[USN] Disjuntor 52E Fechado", self.__clp["SA"], REG["SA_ED_QCAP_Disj52EFechado"])
        self.leitura_ED_SA_QCADE_BombasDng_Auto = LeituraModbusCoil("[USN] Bombas Drenagem Automático", self.__clp["SA"], REG["SA_ED_QCADE_BombasDng_Auto"])
        self.leitura_ED_SA_QCAP_SubtensaoBarraGeral = LeituraModbusCoil("[USN] Subtensão Barramento Geral", self.__clp["SA"], REG["SA_ED_QCAP_SubtensaoBarraGeral"])

        ### CONDICIONADORES ESSENCIAIS
        # self.leitura_ED_SA_QCAP_TensaoPresenteTSA = LeituraModbusCoil("[SA] TSA Tensão Presente", self.__clp["SA"], REG["SA_ED_QCAP_TensaoPresenteTSA"])
        # self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_QCAP_TensaoPresenteTSA.descr, CONDIC_NORMALIZAR, self.leitura_ED_SA_QCAP_TensaoPresenteTSA))

        self.leitura_ED_SA_SEL787_Trip = LeituraModbusCoil("[SA] SEL 787 Trip", self.__clp["SA"], REG["SA_ED_SEL787_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_SEL787_Trip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_SEL787_Trip))

        self.leitura_ED_SA_SEL311_Trip = LeituraModbusCoil("[SA] SEL 311 Trip", self.__clp["SA"], REG["SA_ED_SEL311_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_SEL311_Trip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_SEL311_Trip))

        self.leitura_ED_SA_MRU3_Trip = LeituraModbusCoil("[SA] MRU3 Trip", self.__clp["SA"], REG["SA_ED_MRU3_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_MRU3_Trip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_MRU3_Trip))

        self.leitura_ED_SA_MRL1_Trip = LeituraModbusCoil("[SA] MRL1 Trip", self.__clp["SA"], REG["SA_ED_MRL1_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_MRL1_Trip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_MRL1_Trip))

        self.leitura_ED_SA_QCADE_Disj52E1Trip = LeituraModbusCoil("[SA] Dijuntor 52E1 Trip", self.__clp["SA"], REG["SA_ED_QCADE_Disj52E1Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Disj52E1Trip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCADE_Disj52E1Trip))

        ### CONDICIONADORES NORMAIS
        if not d.glb["TDA_Offline"]:
            self.leitura_ED_TDA_QcataDisj52ETrip = LeituraModbusCoil("[TDA] Disjuntor 52E Trip", self.__clp["TDA"], REG["TDA_ED_QcataDisj52ETrip"])
            self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52ETrip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_TDA_QcataDisj52ETrip))

            self.leitura_ED_TDA_QcataDisj52ETripDisjSai = LeituraModbusCoil("[TDA] Disjuntor 52E Saída Trip", self.__clp["TDA"], REG["TDA_ED_QcataDisj52ETripDisjSai"])
            self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52ETripDisjSai.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_TDA_QcataDisj52ETripDisjSai))

            # self.leitura_ED_TDA_QcataDisj52EFalha380VCA = LeituraModbusCoil("[TDA] Disjuntor 52E Falha 380 VCA", self.__clp["TDA"], REG["TDA_ED_QcataDisj52EFalha380VCA"])
            # self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52EFalha380VCA.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_TDA_QcataDisj52EFalha380VCA))

        self.leitura_ED_SA_MRU3_Falha = LeituraModbusCoil("[SA] MRU3 Falha", self.__clp["SA"], REG["SA_ED_MRU3_Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_MRU3_Falha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_MRU3_Falha))

        self.leitura_ED_SA_SEL787_FalhaInterna = LeituraModbusCoil("[SA] SEL 787 Falha", self.__clp["SA"], REG["SA_ED_SEL787_FalhaInterna"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_SEL787_FalhaInterna.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_SEL787_FalhaInterna))

        self.leitura_ED_SA_SEL311_Falha = LeituraModbusCoil("[SA] SEL 311 Falha", self.__clp["SA"], REG["SA_ED_SEL311_Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_SEL311_Falha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_SEL311_Falha))

        self.leitura_ED_SA_CTE_Falta125Vcc = LeituraModbusCoil("[SA] CTE Falta 125 Vcc", self.__clp["SA"], REG["SA_ED_CTE_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CTE_Falta125Vcc.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_CTE_Falta125Vcc))

        self.leitura_ED_SA_CTE_Secc89TE_Aberta = LeituraModbusCoil("[SA] CTE Seccionadora 89TE Aberta", self.__clp["SA"], REG["SA_ED_CTE_Secc89TE_Aberta"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CTE_Secc89TE_Aberta.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_CTE_Secc89TE_Aberta))

        self.leitura_ED_SA_TE_AlarmeDetectorGas = LeituraModbusCoil("[SA] Detector de Gás Alarme", self.__clp["SA"], REG["SA_ED_TE_AlarmeDetectorGas"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeDetectorGas.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeDetectorGas))

        self.leitura_ED_SA_TE_AlarmeNivelMaxOleo = LeituraModbusCoil("[SA] Transformador Elevador Alarme Nível Máximo Óleo", self.__clp["SA"], REG["SA_ED_TE_AlarmeNivelMaxOleo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeNivelMaxOleo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeNivelMaxOleo))

        self.leitura_ED_SA_TE_AlarmeAlivioPressao = LeituraModbusCoil("[SA] Transformador Elevador Alarme Alívio Pressão", self.__clp["SA"], REG["SA_ED_TE_AlarmeAlivioPressao"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeAlivioPressao.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeAlivioPressao))

        self.leitura_ED_SA_TE_AlarmeTempOleo = LeituraModbusCoil("[SA] Transformador Elevador Alarme Temperatura Óleo", self.__clp["SA"], REG["SA_ED_TE_AlarmeTempOleo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeTempOleo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeTempOleo))

        self.leitura_ED_SA_TE_AlarmeTempEnrolamento = LeituraModbusCoil("[SA] Transformador Elevador Alarme Temperatura Enrolamento", self.__clp["SA"], REG["SA_ED_TE_AlarmeTempEnrolamento"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeTempEnrolamento.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeTempEnrolamento))

        self.leitura_ED_SA_TE_AlarmeDesligamento = LeituraModbusCoil("[SA] Transformador Elevador Alarme Desligamento", self.__clp["SA"], REG["SA_ED_TE_AlarmeDesligamento"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeDesligamento.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeDesligamento))

        self.leitura_ED_SA_TE_Falha = LeituraModbusCoil("[SA] Transformador Elevador Falha", self.__clp["SA"], REG["SA_ED_TE_Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_Falha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_TE_Falha))

        self.leitura_ED_SA_FalhaDisjTPsProt = LeituraModbusCoil("[SA] Disjuntor Transformador Potencial Falha", self.__clp["SA"], REG["SA_ED_FalhaDisjTPsProt"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_FalhaDisjTPsProt.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_FalhaDisjTPsProt))

        self.leitura_ED_SA_FalhaDisjTPsSincr = LeituraModbusCoil("[SA] Disjuntor Transformador Potencial Falha Sincronização", self.__clp["SA"], REG["SA_ED_FalhaDisjTPsSincr"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_FalhaDisjTPsSincr.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_FalhaDisjTPsSincr))

        self.leitura_ED_SA_CSA1_Secc_Aberta = LeituraModbusCoil("[SA] CSA1 Seccionadora Aberta", self.__clp["SA"], REG["SA_ED_CSA1_Secc_Aberta"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_Secc_Aberta.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_CSA1_Secc_Aberta))

        self.leitura_ED_SA_CSA1_FusivelQueimado = LeituraModbusCoil("[SA] CSA1 Fusível Queimado", self.__clp["SA"], REG["SA_ED_CSA1_FusivelQueimado"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_FusivelQueimado.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_CSA1_FusivelQueimado))

        self.leitura_ED_SA_CSA1_FaltaTensao125Vcc = LeituraModbusCoil("[SA] CSA1 Falta Tensão 125 Vcc", self.__clp["SA"], REG["SA_ED_CSA1_FaltaTensao125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_FaltaTensao125Vcc.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_CSA1_FaltaTensao125Vcc))

        self.leitura_ED_SA_QCADE_Nivel4 = LeituraModbusCoil("[SA] CA Drenagem Nível 4", self.__clp["SA"], REG["SA_ED_QCADE_Nivel4"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Nivel4.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCADE_Nivel4))

        self.leitura_ED_SA_QCADE_NivelMuitoAlto = LeituraModbusCoil("[SA] CA Drenagem Nível Muito Alto", self.__clp["SA"], REG["SA_ED_QCADE_NivelMuitoAlto"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_NivelMuitoAlto.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCADE_NivelMuitoAlto))

        self.leitura_ED_SA_QCADE_Falha220VCA = LeituraModbusCoil("[SA] CA Drenagem Falha 220 VCA", self.__clp["SA"], REG["SA_ED_QCADE_Falha220VCA"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Falha220VCA.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCADE_Falha220VCA))

        # Verificar
        self.leitura_ED_SA_QCCP_Disj72ETrip = LeituraModbusCoil("[SA] QCCP Disjuntor 72E Trip", self.__clp["SA"], REG["SA_ED_QCCP_Disj72ETrip"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_Disj72ETrip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCCP_Disj72ETrip))

        self.leitura_ED_SA_QCCP_Falta125Vcc = LeituraModbusCoil("[SA] QCCP Falta 125 Vcc", self.__clp["SA"], REG["SA_ED_QCCP_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_Falta125Vcc.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCCP_Falta125Vcc))

        self.leitura_ED_SA_QCCP_TripDisjAgrup = LeituraModbusCoil("[SA] QCCP Disjuntor Agrupamento Trip", self.__clp["SA"], REG["SA_ED_QCCP_TripDisjAgrup"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_TripDisjAgrup.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCCP_TripDisjAgrup))

        self.leitura_ED_SA_QCAP_Falta125Vcc = LeituraModbusCoil("[SA] CA Principal Falta 125 Vcc", self.__clp["SA"], REG["SA_ED_QCAP_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Falta125Vcc.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCAP_Falta125Vcc))

        self.leitura_ED_SA_QCAP_TripDisjAgrup = LeituraModbusCoil("[SA] CA Principal Disjuntor Agrupamento Trip", self.__clp["SA"], REG["SA_ED_QCAP_TripDisjAgrup"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_TripDisjAgrup.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCAP_TripDisjAgrup))

        self.leitura_ED_SA_QCAP_Disj52A1Falha = LeituraModbusCoil("[SA] CA Principal Disjuntor 52A1 Falha", self.__clp["SA"], REG["SA_ED_QCAP_Disj52A1Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Disj52A1Falha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCAP_Disj52A1Falha))

        self.leitura_ED_SA_QCAP_Disj52EFalha = LeituraModbusCoil("[SA] CA Principal Disjuntor 52E Falha", self.__clp["SA"], REG["SA_ED_QCAP_Disj52EFalha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Disj52EFalha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_QCAP_Disj52EFalha))

        # self.leitura_ED_SA_GMG_DisjFechado = LeituraModbusCoil("[SA] Disjuntor Grupo Motor Gerador Fechado", self.__clp["SA"], REG["SA_ED_GMG_DisjFechado"])
        # self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_GMG_DisjFechado.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_GMG_DisjFechado))

        self.leitura_RD_DJ1_FalhaInt = LeituraModbusCoil("[SA] Disjuntor 1 Falha Interna", self.__clp["SA"], REG["SA_RD_DJ1_FalhaInt"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_DJ1_FalhaInt.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_DJ1_FalhaInt))

        self.leitura_RD_CLP_Falha = LeituraModbusCoil("[SA] CLP SA Falha", self.__clp["SA"], REG["SA_RD_FalhaComuCLP"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_CLP_Falha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_CLP_Falha))

        self.leitura_RA_SEL787_Targets = LeituraModbusCoil("[SA] SEL 787 Targets", self.__clp["SA"], REG["SA_RA_SEL787_Targets"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets))

        self.leitura_RA_SEL787_Targets_Links_Bit00 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 0", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit00"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit00.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit00))

        # self.leitura_RA_SEL787_Targets_Links_Bit01 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 1", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit01"])
        # self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit01.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit01))

        self.leitura_RA_SEL787_Targets_Links_Bit02 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 2", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit02"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit02.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit02))

        self.leitura_RA_SEL787_Targets_Links_Bit03 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 3", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit03"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit03.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit03))

        self.leitura_RA_SEL787_Targets_Links_Bit04 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 4", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit04"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit04.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit04))

        # self.leitura_RA_SEL787_Targets_Links_Bit05 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 5", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit05"])
        # self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit05.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit05))

        # self.leitura_RA_SEL787_Targets_Links_Bit06 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 6", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit06"])
        # self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit06.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit06))

        self.leitura_RA_SEL787_Targets_Links_Bit07 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 7", self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit07"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit07.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit07))

        return


class OcorrenciasUg:
    def __init__(self, ug, clp: "dict[str, ModbusClient]"=None, db: BancoDados=None):

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

            for condic in condicionadores_ativos:
                v = [datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descr]
                self.__db.update_alarmes(v)

            return flag
        return flag

    def atualizar_limites_condicionadores(self, parametros) -> "None":
        """
        Função para extração de valores do Banco de Dados da Interface WEB e atribuição
        de novos limites de operação de condicionadores.
        """

        try:
            self.__ug.prioridade = int(parametros[f"ug{self.__ug.id}_prioridade"])
            self.condic_dict[f"tmp_fase_r_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_fase_s_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_fase_t_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_nucleo_estator_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_nucleo_estator_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_rad_dia_1_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_rad_dia_2_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_rad_tra_1_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_rad_tra_2_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_saida_de_ar_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_saida_de_ar_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_guia_escora_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_guia_escora_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_guia_radial_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_guia_radial_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_guia_contra_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_guia_contra_ug{self.__ug.id}"])
            self.condic_dict[f"pressao_cx_espiral_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_caixa_espiral_ug{self.__ug.id}"])

            self.condic_dict[f"tmp_fase_r_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_fase_s_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_fase_t_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_nucleo_estator_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_nucleo_estator_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_rad_dia_1_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_rad_dia_2_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_rad_tra_1_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_rad_tra_2_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_saida_de_ar_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_saida_de_ar_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_guia_escora_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_guia_escora_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_guia_radial_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_guia_radial_ug{self.__ug.id}"])
            self.condic_dict[f"tmp_mancal_guia_contra_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_guia_contra_ug{self.__ug.id}"])
            self.condic_dict[f"pressao_cx_espiral_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_caixa_espiral_ug{self.__ug.id}"])

        except Exception:
            logger.error(f"[OCO-UG{self.__ug.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores.")
            logger.debug(f"[OCO-UG{self.__ug.id}] Traceback: {traceback.format_exc()}")

    def controle_limites_operacao(self) -> "None":
        """
        Função para verificação de limites de operação da Unidade.

        Verifica os valores base e limite da Unidade, pré-determinados na interface
        WEB, e avisa o operador caso algum valor ultrapasse o estipulado.
        """

        ld = self.leitura_dict
        cd = self.condic_dict

        if ld[f"tmp_fase_r_ug{self.__ug.id}"].valor >= cd[f"tmp_fase_r_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura de Fase R da UG passou do valor base! ({cd[f'tmp_fase_r_ug{self.__ug.id}'].valor_base} C) | Leitura: {ld[f'tmp_fase_r_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_fase_r_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_fase_r_ug{self.__ug.id}"].valor_limite - cd[f"tmp_fase_r_ug{self.__ug.id}"].valor_base) + cd[f"tmp_fase_r_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura de Fase R da UG está muito próxima do limite! ({cd[f'tmp_fase_r_ug{self.__ug.id}'].valor_limite} C) | Leitura: {ld[f'tmp_fase_r_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_fase_s_ug{self.__ug.id}"].valor >= cd[f"tmp_fase_s_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura de Fase S da UG passou do valor base! ({cd[f'tmp_fase_s_ug{self.__ug.id}'].valor_base} C) | Leitura: {ld[f'tmp_fase_s_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_fase_s_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_fase_s_ug{self.__ug.id}"].valor_limite - cd[f"tmp_fase_s_ug{self.__ug.id}"].valor_base) + cd[f"tmp_fase_s_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura de Fase S da UG está muito próxima do limite! ({cd[f'tmp_fase_s_ug{self.__ug.id}'].valor_limite} C) | Leitura: {ld[f'tmp_fase_s_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_fase_t_ug{self.__ug.id}"].valor >= cd[f"tmp_fase_t_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura de Fase T da UG passou do valor base! ({cd[f'tmp_fase_t_ug{self.__ug.id}'].valor_base} C) | Leitura: {ld[f'tmp_fase_t_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_fase_t_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_fase_t_ug{self.__ug.id}"].valor_limite - cd[f"tmp_fase_t_ug{self.__ug.id}"].valor_base) + cd[f"tmp_fase_t_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura de Fase T da UG está muito próxima do limite! ({cd[f'tmp_fase_t_ug{self.__ug.id}'].valor_limite} C) | Leitura: {ld[f'tmp_fase_t_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_nucleo_estator_ug{self.__ug.id}"].valor >= cd[f"tmp_nucleo_estator_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Núcleo Gerador Estator da UG passou do valor base! ({cd[f'tmp_nucleo_estator_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_nucleo_estator_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_nucleo_estator_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_nucleo_estator_ug{self.__ug.id}"].valor_limite - cd[f"tmp_nucleo_estator_ug{self.__ug.id}"].valor_base) + cd[f"tmp_nucleo_estator_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Núcleo Gerador Estator da UG está muito próxima do limite! ({cd[f'tmp_nucleo_estator_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_nucleo_estator_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"].valor >= cd[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Dianteiro 1 da UG passou do valor base! ({cd[f'tmp_mancal_rad_dia_1_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_mancal_rad_dia_1_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"].valor_limite - cd[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"].valor_base) + cd[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Dianteiro 1 da UG está muito próxima do limite! ({cd[f'tmp_mancal_rad_dia_1_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_mancal_rad_dia_1_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"].valor >= cd[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Dianteiro 2 da UG passou do valor base! ({cd[f'tmp_mancal_rad_dia_2_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_mancal_rad_dia_2_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"].valor_limite - cd[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"].valor_base) + cd[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Dianteiro 2 da UG está muito próxima do limite! ({cd[f'tmp_mancal_rad_dia_2_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_mancal_rad_dia_2_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"].valor >= cd[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Traseiro 1 da UG passou do valor base! ({cd[f'tmp_mancal_rad_tra_1_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_mancal_rad_tra_1_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"].valor_limite - cd[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"].valor_base) + cd[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Traseiro 1 da UG está muito próxima do limite! ({cd[f'tmp_mancal_rad_tra_1_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_mancal_rad_tra_1_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"].valor >= cd[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Traseiro 2 da UG passou do valor base! ({cd[f'tmp_mancal_rad_tra_2_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_mancal_rad_tra_2_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"].valor_limite - cd[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"].valor_base) + cd[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Traseiro 2 da UG está muito próxima do limite! ({cd[f'tmp_mancal_rad_tra_2_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_mancal_rad_tra_2_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_saida_de_ar_ug{self.__ug.id}"].valor >= cd[f"tmp_saida_de_ar_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura da Saída de Ar da UG passou do valor base! ({cd[f'tmp_saida_de_ar_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_saida_de_ar_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_saida_de_ar_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_saida_de_ar_ug{self.__ug.id}"].valor_limite - cd[f"tmp_saida_de_ar_ug{self.__ug.id}"].valor_base) + cd[f"tmp_saida_de_ar_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura da Saída de Ar da UG está muito próxima do limite! ({cd[f'tmp_saida_de_ar_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_saida_de_ar_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_guia_escora_ug{self.__ug.id}"].valor >= cd[f"tmp_mancal_guia_escora_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Guia Escora da UG passou do valor base! ({cd[f'tmp_mancal_guia_escora_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_mancal_guia_escora_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_guia_escora_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_mancal_guia_escora_ug{self.__ug.id}"].valor_limite - cd[f"tmp_mancal_guia_escora_ug{self.__ug.id}"].valor_base) + cd[f"tmp_mancal_guia_escora_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Guia Escora da UG está muito próxima do limite! ({cd[f'tmp_mancal_guia_escora_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_mancal_guia_escora_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_guia_radial_ug{self.__ug.id}"].valor >= cd[f"tmp_mancal_guia_radial_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Guia Radial da UG passou do valor base! ({cd[f'tmp_mancal_guia_radial_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_mancal_guia_radial_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_guia_radial_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_mancal_guia_radial_ug{self.__ug.id}"].valor_limite - cd[f"tmp_mancal_guia_radial_ug{self.__ug.id}"].valor_base) + cd[f"tmp_mancal_guia_radial_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Guia Radial da UG está muito próxima do limite! ({cd[f'tmp_mancal_guia_radial_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_mancal_guia_radial_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_guia_contra_ug{self.__ug.id}"].valor >= cd[f"tmp_mancal_guia_contra_ug{self.__ug.id}"].valor_base:
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Guia Contra Escora da UG passou do valor base! ({cd[f'tmp_mancal_guia_contra_ug{self.__ug.id}'].valor_base} C) | Leitura: {cd[f'tmp_mancal_guia_contra_ug{self.__ug.id}'].valor} C")

        if ld[f"tmp_mancal_guia_contra_ug{self.__ug.id}"].valor >= 0.9*(cd[f"tmp_mancal_guia_contra_ug{self.__ug.id}"].valor_limite - cd[f"tmp_mancal_guia_contra_ug{self.__ug.id}"].valor_base) + cd[f"tmp_mancal_guia_contra_ug{self.__ug.id}"].valor_base:
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Guia Contra Escora da UG está muito próxima do limite! ({cd[f'tmp_mancal_guia_contra_ug{self.__ug.id}'].valor_limite} C) | Leitura: {cd[f'tmp_mancal_guia_contra_ug{self.__ug.id}'].valor} C")

        if ld[f"pressao_cx_espiral_ug{self.__ug.id}"].valor <= cd[f"pressao_cx_espiral_ug{self.__ug.id}"].valor_base and ld[f"pressao_cx_espiral_ug{self.__ug.id}"].valor != 0 and self.__ug.etapa_atual == UG_SINCRONIZADA:
            logger.warning(f"[OCO-UG{self.__ug.id}] A pressão Caixa Espiral da UG passou do valor base! ({cd[f'pressao_cx_espiral_ug{self.__ug.id}'].valor_base:03.2f} KGf/m2) | Leitura: {ld[f'pressao_cx_espiral_ug{self.__ug.id}'].valor:03.2f}")

        if ld[f"pressao_cx_espiral_ug{self.__ug.id}"].valor <= 16.1 and ld[f"pressao_cx_espiral_ug{self.__ug.id}"].valor != 0 and self.__ug.etapa_atual == UG_SINCRONIZADA:
            logger.critical(f"[OCO-UG{self.__ug.id}] A pressão Caixa Espiral da UG está muito próxima do limite! ({cd[f'pressao_cx_espiral_ug{self.__ug.id}'].valor_limite:03.2f} KGf/m2) | Leitura: {ld[f'pressao_cx_espiral_ug{self.__ug.id}'].valor:03.2f} KGf/m2")


    def leitura_temporizada(self) -> "None":
        """
        Função para consulta de acionamentos da Unidade e avisos através do mecanismo
        de acionamento temporizado.
        """

        if self.leitura_voip["leitura_ED_FreioPastilhaGasta"].valor != 0:
            logger.warning(f"[OCO-UG{self.__ug.id}] O sensor de Freio da UG retornou que a Pastilha está gasta, favor considerar troca.")

        if self.leitura_voip["leitura_ED_FiltroPresSujo75Troc"].valor != 0:
            logger.warning(f"[OCO-UG{self.__ug.id}] O sensor do Filtro de Pressão UHRV retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.leitura_voip["leitura_ED_FiltroRetSujo75Troc"].valor != 0:
            logger.warning(f"[OCO-UG{self.__ug.id}] O sensor do Filtro de Retorno UHRV retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.leitura_voip["leitura_ED_UHLMFilt1PresSujo75Troc"].valor != 0:
            logger.warning(f"[OCO-UG{self.__ug.id}] O sensor do Filtro 1 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.leitura_voip["leitura_ED_UHLMFilt2PresSujo75Troc"].valor != 0:
            logger.warning(f"[OCO-UG{self.__ug.id}] O sensor do Filtro 2 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.leitura_voip["leitura_ED_FiltroPressaoBbaMecSj75"].valor != 0:
            logger.warning(f"[OCO-UG{self.__ug.id}] O sensor do Filtro de Pressão da Bomba Mecânica retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.leitura_voip["leitura_ED_FreioCmdRemoto"].valor != 1:
            logger.debug(f"[OCO-UG{self.__ug.id}] O freio da UG saiu do modo remoto, favor analisar a situação.")

        if self.leitura_voip[f"leitura_ED_QCAUG{self.__ug.id}_Remoto"].valor != 1:
            logger.debug(f"[OCO-UG{self.__ug.id}] O compressor da UG saiu do modo remoto, favor analisar a situação.")

        return

    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Unidade.
        """

        # Leituras de condicionadores com limites de operção checados a cada ciclo
        self.leitura_voip["leitura_ED_FreioPastilhaGasta"] = LeituraModbusCoil(
            f"[UG{self.__ug.id}] Pastilha Freio Gasta",
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_FreioPastilhaGasta"]
        )
        self.leitura_voip["leitura_ED_FiltroPresSujo75Troc"] = LeituraModbusCoil(
            f"[UG{self}] UHRV Filtro Pressão 75% Sujo",
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_FiltroPresSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_FiltroRetSujo75Troc"] = LeituraModbusCoil(
            f"[UG{self.__ug.id}] UHRV Filtro Pressão Retorno 75% Sujo",
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_FiltroRetSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_UHLMFilt1PresSujo75Troc"] = LeituraModbusCoil(
            f"[UG{self.__ug.id}] UHLM Filtro Pressão 1 75% Sujo",
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_UHLMFilt1PresSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_UHLMFilt2PresSujo75Troc"] = LeituraModbusCoil(
            f"[UG{self.__ug.id}] UHLM Filtro Pressão 2 75% Sujo",
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_UHLMFilt2PresSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_FiltroPressaoBbaMecSj75"] = LeituraModbusCoil(
            f"[UG{self.__ug.id}] Filtro Pressão Bomba Mecância 75% Sujo",
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_Filt1PresBbaMecSj75Troc"]
        )
        self.leitura_voip["leitura_ED_TripPartRes"] = LeituraModbusCoil(
            f"[UG{self.__ug.id}] Trip Part Res",
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_TripPartRes"]
        )
        self.leitura_voip["leitura_ED_FreioCmdRemoto"] = LeituraModbusCoil(
            f"[UG{self.__ug.id}] Freio Modo Remoto",
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_FreioCmdRemoto"]
        )
        self.leitura_voip[f"leitura_ED_QCAUG{self.__ug.id}_Remoto"] = LeituraModbusCoil(
            f"[UG{self.__ug.id}] Compressor Modo Remoto",
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_QCAUG{self.__ug.id}_Remoto"]
        )

        ### CONDICIONADORES ESSENCIAIS
        # R
        self.leitura_dict[f"tmp_fase_r_ug{self.__ug.id}"] = LeituraModbus(f"[UG{self.__ug.id}] Temperatura Fase R", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_01"], op=4)
        self.condic_dict[f"tmp_fase_r_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_fase_r_ug{self.__ug.id}"].descr, CONDIC_INDISPONIBILIZAR, self.leitura_dict[f"tmp_fase_r_ug{self.__ug.id}"], 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_r_ug{self.__ug.id}"])

        # S
        self.leitura_dict[f"tmp_fase_s_ug{self.__ug.id}"] = LeituraModbus(f"[UG{self.__ug.id}] Temperatura Fase S", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_02"], op=4)
        self.condic_dict[f"tmp_fase_s_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_fase_s_ug{self.__ug.id}"].descr, CONDIC_INDISPONIBILIZAR, self.leitura_dict[f"tmp_fase_s_ug{self.__ug.id}"], 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_s_ug{self.__ug.id}"])

        # T
        self.leitura_dict[f"tmp_fase_t_ug{self.__ug.id}"] = LeituraModbus(f"[UG{self.__ug.id}] Temperatura Fase T", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_03"], op=4)
        self.condic_dict[f"tmp_fase_t_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_fase_t_ug{self.__ug.id}"].descr, CONDIC_INDISPONIBILIZAR, self.leitura_dict[f"tmp_fase_t_ug{self.__ug.id}"], 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_t_ug{self.__ug.id}"])

        # Nucleo estator
        self.leitura_dict[f"tmp_nucleo_estator_ug{self.__ug.id}"] = LeituraModbus(f"[UG{self.__ug.id}] Temperatura Núcelo do Estator", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_04"], op=4)
        self.condic_dict[f"tmp_nucleo_estator_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_nucleo_estator_ug{self.__ug.id}"].descr, CONDIC_INDISPONIBILIZAR, self.leitura_dict[f"tmp_nucleo_estator_ug{self.__ug.id}"], 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_nucleo_estator_ug{self.__ug.id}"])

        # MRD 1
        self.leitura_dict[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"] = LeituraModbus(f"[UG{self.__ug.id}] Temperatura Mancal Radial Dianteiro", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_05"], op=4)
        self.condic_dict[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"].descr, CONDIC_INDISPONIBILIZAR, self.leitura_dict[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"], 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"])

        # MRT 1
        self.leitura_dict[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"] = LeituraModbus(f"[UG{self.__ug.id}] Temperatura Mancal Radial Traseiro", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_06"], op=4)
        self.condic_dict[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"].descr, CONDIC_INDISPONIBILIZAR, self.leitura_dict[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"], 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"])

        # MRD 2
        self.leitura_dict[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"] = LeituraModbus(f"[UG{self.__ug.id}] Temperatura Mancal Radial Dianteiro 2", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_07"], op=4)
        self.condic_dict[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"].descr, CONDIC_INDISPONIBILIZAR, self.leitura_dict[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"], 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"])

        # MRT 2
        self.leitura_dict[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"] = LeituraModbus(f"[UG{self.__ug.id}] Temperatura Mancal Radial Traseiro 2", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_08"], op=4)
        self.condic_dict[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"].descr, CONDIC_INDISPONIBILIZAR, self.leitura_dict[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"], 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"])

        # Saída de ar
        self.leitura_dict[f"tmp_saida_de_ar_ug{self.__ug.id}"] = LeituraModbus(f"[UG{self.__ug.id}] Saída de Ar", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_10"], op=4)
        self.condic_dict[f"tmp_saida_de_ar_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_saida_de_ar_ug{self.__ug.id}"].descr, CONDIC_INDISPONIBILIZAR, self.leitura_dict[f"tmp_saida_de_ar_ug{self.__ug.id}"], 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_saida_de_ar_ug{self.__ug.id}"])

        # Mancal Guia Radial
        self.leitura_dict[f"tmp_mancal_guia_radial_ug{self.__ug.id}"] = LeituraModbus(f"[UG{self.__ug.id}] Mancal Guia Radial", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_TempMcGuiaRadial"])
        self.condic_dict[f"tmp_mancal_guia_radial_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_mancal_guia_radial_ug{self.__ug.id}"].descr, CONDIC_INDISPONIBILIZAR, self.leitura_dict[f"tmp_mancal_guia_radial_ug{self.__ug.id}"], 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_guia_radial_ug{self.__ug.id}"])

        # Mancal Guia escora
        self.leitura_dict[f"tmp_mancal_guia_escora_ug{self.__ug.id}"] = LeituraModbus(f"[UG{self.__ug.id}] Mancal Guia Escora", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_TempMcGuiaEscora"])
        self.condic_dict[f"tmp_mancal_guia_escora_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_mancal_guia_escora_ug{self.__ug.id}"].descr, CONDIC_INDISPONIBILIZAR, self.leitura_dict[f"tmp_mancal_guia_escora_ug{self.__ug.id}"], 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_guia_escora_ug{self.__ug.id}"])

        # Mancal Guia contra_escora
        self.leitura_dict[f"tmp_mancal_guia_contra_ug{self.__ug.id}"] = LeituraModbus(f"[UG{self.__ug.id}] Mancal Guia Contra Escora", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_TempMcGuiaContraEscora"])
        self.condic_dict[f"tmp_mancal_guia_contra_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_mancal_guia_contra_ug{self.__ug.id}"].descr, CONDIC_INDISPONIBILIZAR, self.leitura_dict[f"tmp_mancal_guia_contra_ug{self.__ug.id}"], 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_guia_contra_ug{self.__ug.id}"])

        self.leitura_dict[f"pressao_cx_espiral_ug{self.__ug.id}"] = LeituraModbus(f"[UG{self.__ug.id}] Pressão Caixa Espiral", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_EA_PressK1CaixaExpiral_MaisCasas"], escala=0.1, op=4)
        self.condic_dict[f"pressao_cx_espiral_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"pressao_cx_espiral_ug{self.__ug.id}"].descr, CONDIC_INDISPONIBILIZAR, self.leitura_dict[f"pressao_cx_espiral_ug{self.__ug.id}"], 15.5, 18)
        self.condicionadores_essenciais.append(self.condic_dict[f"pressao_cx_espiral_ug{self.__ug.id}"])


        # Óleo do Transformador Elevador
        self.leitura_temperatura_oleo_trafo = LeituraModbus(f"[UG{self.__ug.id}] Óleo do Transformador Elevador", self.__clp["SA"], REG["SA_EA_TE_TempOleo"], escala=0.1, op=4)
        self.condicionador_leitura_temperatura_oleo_trafo = CondicionadorExponencial(self.leitura_temperatura_oleo_trafo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_temperatura_oleo_trafo, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_leitura_temperatura_oleo_trafo)

        ## Comandos Digitais
        # GERAL
        self.leitura_CD_EmergenciaViaSuper = LeituraModbusCoil(f"[UG{self.__ug.id}] Emergência Via Supervisório", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_CD_EmergenciaViaSuper"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_CD_EmergenciaViaSuper.descr, CONDIC_NORMALIZAR, self.leitura_CD_EmergenciaViaSuper))

        ## Retornos Digitais
        # TRIPS
        self.leitura_RD_TripEletrico = LeituraModbusCoil(f"[UG{self.__ug.id}] Trip Elétrico", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripEletrico"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_RD_TripEletrico.descr, CONDIC_NORMALIZAR, self.leitura_RD_TripEletrico, self.__ug.id, [UG_PARANDO, UG_PARADA]))

        self.leitura_RD_700G_Trip = LeituraModbusCoil(f"[UG{self.__ug.id}] SEL 700G Trip", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_700G_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_RD_700G_Trip.descr, CONDIC_NORMALIZAR, self.leitura_RD_700G_Trip, self.__ug.id, [UG_PARANDO, UG_PARADA]))

        self.leitura_RD_TripMecanico = LeituraModbusCoil(f"[UG{self.__ug.id}] Trip Mecâncio", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripMecanico"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_RD_TripMecanico.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripMecanico))

        ## Entradas Digitais
        # TRIPS
        self.leitura_ED_RV_Trip = LeituraModbusCoil(f"[UG{self.__ug.id}] RV Trip", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_RV_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_RV_Trip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_RV_Trip))

        self.leitura_ED_AVR_Trip = LeituraModbusCoil(f"[UG{self.__ug.id}] AVR Trip", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_AVR_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_AVR_Trip.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_AVR_Trip))

        # RELÉS
        self.leitura_ED_SEL700G_Atuado = LeituraModbusCoil(f"[UG{self.__ug.id}] SEL 700G Atuado", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_SEL700G_Atuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SEL700G_Atuado.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SEL700G_Atuado))

        self.leitura_ED_ReleBloqA86MAtuado = LeituraModbusCoil(f"[UG{self.__ug.id}] Bloqueio 86M Atuado", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_ReleBloqA86MAtuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_ReleBloqA86MAtuado.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_ReleBloqA86MAtuado))

        self.leitura_ED_ReleBloqA86HAtuado = LeituraModbusCoil(f"[UG{self.__ug.id}] Bloqueio 86H Atuado", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_ReleBloqA86HAtuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_ReleBloqA86HAtuado.descr, CONDIC_NORMALIZAR, self.leitura_ED_ReleBloqA86HAtuado, self.__ug.id, [UG_SINCRONIZADA]))


        ### CONDICIONADORES NORMAIS
        # Entradas Digitais
        # SA -> UG
        self.leitura_ED_SA_FalhaDisjTPsSincrG2 = LeituraModbusCoil(f"[SA-UG{self.__ug.id}] Trasformador Potencial Disjuntor Sincronização Falha", self.__clp["SA"], REG["SA_ED_FalhaDisjTPsSincrG2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_FalhaDisjTPsSincrG2.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_FalhaDisjTPsSincrG2))

        self.leitura_ED_SA_DisjDJ1_AlPressBaixa = LeituraModbusCoil(f"[SA-UG{self.__ug.id}] Disjutor 1 Alarme Pressão Baixa", self.__clp["SA"], REG["SA_ED_DisjDJ1_AlPressBaixa"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_DisjDJ1_AlPressBaixa.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_DisjDJ1_AlPressBaixa))

        self.leitura_ED_SA_DisjDJ1_BloqPressBaixa = LeituraModbusCoil(f"[SA-UG{self.__ug.id}] Disjuntor 1 Bloqueio Pressão Baixa", self.__clp["SA"], REG["SA_ED_DisjDJ1_BloqPressBaixa"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_DisjDJ1_BloqPressBaixa.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SA_DisjDJ1_BloqPressBaixa))

        # TRIPS
        self.leitura_ED_UHRV_TripBomba1 = LeituraModbusCoil(f"[UG{self.__ug.id}] UHRV Bomba 1 Trip", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHRV_TripBomba1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_TripBomba1.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHRV_TripBomba1))

        self.leitura_ED_UHRV_TripBomba2 = LeituraModbusCoil(f"[UG{self.__ug.id}] UHRV Bomba 2 Trip", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHRV_TripBomba2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_TripBomba2.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHRV_TripBomba2))

        self.leitura_ED_UHLM_TripBomba1 = LeituraModbusCoil(f"[UG{self.__ug.id}] UHLM Bomba 1 Trip", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_TripBomba1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_TripBomba1.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_TripBomba1))

        self.leitura_ED_UHLM_TripBomba2 = LeituraModbusCoil(f"[UG{self.__ug.id}] UHLM Bomba 2 Trip", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_TripBomba2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_TripBomba2.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_TripBomba2))

        self.leitura_ED_QCAUG_TripDisj52A1 = LeituraModbusCoil(f"[UG{self.__ug.id}] QCAUG Disjuntor 52A1 Trip", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_QCAUG_TripDisj52A1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_QCAUG_TripDisj52A1.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_QCAUG_TripDisj52A1))

        self.leitura_ED_TripAlimPainelFreio = LeituraModbusCoil(f"[UG{self.__ug.id}] Alimentação Painel Freio Trip", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_TripAlimPainelFreio"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_TripAlimPainelFreio.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_TripAlimPainelFreio))

        self.leitura_ED_QCAUG_TripDisjAgrup = LeituraModbusCoil(f"[UG{self.__ug.id}] QCAUG Disjuntor Agrupamento Trip", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_QCAUG_TripDisjAgrup"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_QCAUG_TripDisjAgrup.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_QCAUG_TripDisjAgrup))

        # FALHAS
        self.leitura_ED_AVR_FalhaInterna = LeituraModbusCoil(f"[UG{self.__ug.id}] AVR Falha Interna", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_AVR_FalhaInterna"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_AVR_FalhaInterna.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_AVR_FalhaInterna))

        self.leitura_ED_SEL700G_FalhaInterna = LeituraModbusCoil(f"[UG{self.__ug.id}] SEL 700G Falha Interna", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_SEL700G_FalhaInterna"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SEL700G_FalhaInterna.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SEL700G_FalhaInterna))

        self.leitura_ED_QCAUG_Falha380VcaPainel = LeituraModbusCoil(f"[UG{self.__ug.id}] QCAUG Falha 380 VCA Painel", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_QCAUG_Falha380VcaPainel"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_QCAUG_Falha380VcaPainel.descr, CONDIC_NORMALIZAR, self.leitura_ED_QCAUG_Falha380VcaPainel))

        # FALTAS
        self.leitura_ED_Falta125Vcc = LeituraModbusCoil(f"[UG{self.__ug.id}] Falta 125 Vcc", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_Falta125Vcc.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_Falta125Vcc))

        self.leitura_ED_Falta125VccCom = LeituraModbusCoil(f"[UG{self.__ug.id}] Falta 125 Vcc Com", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_Falta125VccCom"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_Falta125VccCom.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_Falta125VccCom))

        self.leitura_ED_FaltaFluxoOleoMc = LeituraModbusCoil(f"[UG{self.__ug.id}] Falta Fluxo Óleo MC", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_FaltaFluxoOleoMc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FaltaFluxoOleoMc.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_FaltaFluxoOleoMc))

        self.leitura_ED_Falta125VccAlimVal = LeituraModbusCoil(f"[UG{self.__ug.id}] Falta 125 Vcc Alimentação", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_Falta125VccAlimVal"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_Falta125VccAlimVal.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_Falta125VccAlimVal))

        self.leitura_ED_UHLM_FaltaFluxTroc = LeituraModbusCoil(f"[UG{self.__ug.id}] UHLM Falta Fluxo", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_FaltaFluxTroc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FaltaFluxTroc.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_FaltaFluxTroc))

        self.leitura_ED_UHLM_FaltaPressTroc = LeituraModbusCoil(f"[UG{self.__ug.id}] UHLM Falta Pressão", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_FaltaPressTroc"]) # TODO retornar para DEVE_INDISPONIBILZIAR
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FaltaPressTroc.descr, CONDIC_NORMALIZAR, self.leitura_ED_UHLM_FaltaPressTroc))

        # Controle UHRV
        self.leitura_ED_UHRV_NivOleominimoPos36 = LeituraModbusCoil(f"[UG{self.__ug.id}] UHRV Óleo Nível Mínimo Posição 36", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHRV_NivOleominimoPos36"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_NivOleominimoPos36.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHRV_NivOleominimoPos36))

        self.leitura_ED_UHRV_NivOleoCriticoPos35 = LeituraModbusCoil(f"[UG{self.__ug.id}] UHRV Óleo Nível Crítico Posição 35", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHRV_NivOleoCriticoPos35"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_NivOleoCriticoPos35.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHRV_NivOleoCriticoPos35))

        # Controle UHLM
        self.leitura_ED_UHLM_FluxoMcTras = LeituraModbusCoil(f"[UG{self.__ug.id}] UHLM Fluxo Traseiro MC", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_FluxoMcTras"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FluxoMcTras.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_FluxoMcTras))

        self.leitura_ED_UHLM_NivelminOleo = LeituraModbusCoil(f"[UG{self.__ug.id}] UHLM Óleo Nível Mínimo", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_NivelminOleo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_NivelminOleo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_NivelminOleo))

        self.leitura_ED_UHLM_NivelCritOleo = LeituraModbusCoil(f"[UG{self.__ug.id}] UHLM Óleo Nível Crítico", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_NivelCritOleo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_NivelCritOleo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_NivelCritOleo))

        self.leitura_ED_UHLM_FluxoMcDianteiro = LeituraModbusCoil(f"[UG{self.__ug.id}] UHLM Fluxo Dianteiro", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_FluxoMcDiant"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FluxoMcDianteiro.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_FluxoMcDianteiro))

        self.leitura_ED_UHLM_Filt1PresSujo100Sujo = LeituraModbusCoil(f"[UG{self.__ug.id}] UHLM Filtro 1 Pressão 100% Sujo", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLMFilt1PresSujoSujo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_Filt1PresSujo100Sujo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_Filt1PresSujo100Sujo))

        self.leitura_ED_UHLM_Filt2PresSujo100Sujo = LeituraModbusCoil(f"[UG{self.__ug.id}] UHLM Filtro 2 Pressão 100% Sujo", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLMFilt2PresSujoSujo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_Filt2PresSujo100Sujo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_UHLM_Filt2PresSujo100Sujo))

        # Controle Freios
        self.leitura_ED_FreioSemEnergia = LeituraModbusCoil(f"[UG{self.__ug.id}] Freio Sem Energia", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_FreioSemEnergia"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FreioSemEnergia.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_FreioSemEnergia))

        self.leitura_ED_FreioFiltroSaturado = LeituraModbusCoil(f"[UG{self.__ug.id}] Freio Filtro Saturado", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_FreioFiltroSaturado"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FreioFiltroSaturado.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_FreioFiltroSaturado))

        # Controle Filtros
        self.leitura_ED_FiltroRetSujo100Sujo = LeituraModbusCoil(f"[UG{self.__ug.id}] UHRV Filtro Retorno 100% Sujo", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_FiltroRetSujoSujo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FiltroRetSujo100Sujo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_FiltroRetSujo100Sujo))

        self.leitura_ED_FiltroPresSujo100Sujo = LeituraModbusCoil(f"[UG{self.__ug.id}] UHRV Filtro Pressão 100% Sujo", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_FiltroPresSujoSujo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FiltroPresSujo100Sujo.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_FiltroPresSujo100Sujo))

        self.leitura_ED_FiltroPressaoBbaMecSj100 = LeituraModbusCoil(f"[UG{self.__ug.id}] UHRV Bomba Filtro Pressão 100% Sujo", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_Filt1PresBbaMecSjSujo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FiltroPressaoBbaMecSj100.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_FiltroPressaoBbaMecSj100))

        # Outros
        self.leitura_ED_PalhetasDesal = LeituraModbusCoil(f"[UG{self.__ug.id}] Pás Desalinhadas", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_PalhetasDesal"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_PalhetasDesal.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_PalhetasDesal))

        self.leitura_ED_ValvBorbTravada = LeituraModbusCoil(f"[UG{self.__ug.id}] Válvula Borboleta Travada", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_ValvBorbTravadaFechada"],)
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_ValvBorbTravada.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_ValvBorbTravada))

        self.leitura_ED_SobreVeloMecPos18 = LeituraModbusCoil(f"[UG{self.__ug.id}] Sobre Velocidade Posição 18", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_SobreVeloMecPos18"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SobreVeloMecPos18.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_SobreVeloMecPos18))

        self.leitura_ED_NivelMAltoPocoDren = LeituraModbusCoil(f"[UG{self.__ug.id}] Poço Drenagem Nível Alto", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_NivelMAltoPocoDren"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_NivelMAltoPocoDren.descr, CONDIC_INDISPONIBILIZAR, self.leitura_ED_NivelMAltoPocoDren))


        ## Retornos Digitais
        # TRIPS
        self.leitura_RD_TripVibr1 = LeituraModbusCoil(f"[UG{self.__ug.id}] Vibração 1 Trip", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripVibr1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripVibr1.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripVibr1))

        self.leitura_RD_TripVibr2 = LeituraModbusCoil(f"[UG{self.__ug.id}] Vibração 2 Trip", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripVibr2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripVibr2.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripVibr2))

        self.leitura_RD_TripTempUHRV = LeituraModbusCoil(f"[UG{self.__ug.id}] UHRV Trip Temperatura", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripTempUHRV"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempUHRV.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripTempUHRV))

        self.leitura_RD_TripTempUHLM = LeituraModbusCoil(f"[UG{self.__ug.id}] UHLM Trip Temperatura", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripTempUHLM"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempUHLM.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripTempUHLM))

        self.leitura_RD_TripTempGaxeteiro = LeituraModbusCoil(f"[UG{self.__ug.id}] Gaxeteiro Trip Temperatura", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripTempGaxeteiro"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempGaxeteiro.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripTempGaxeteiro))

        self.leitura_RD_TripTempMcGuiaRadial = LeituraModbusCoil(f"[UG{self.__ug.id}] Mancal Guia Radial Trip Temperatura", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripTempMcGuiaRadial"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempMcGuiaRadial.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripTempMcGuiaRadial))

        self.leitura_RD_TripTempMcGuiaEscora = LeituraModbusCoil(f"[UG{self.__ug.id}] Mancal Guia Escora Trip Temperatura", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripTempMcGuiaEscora"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempMcGuiaEscora.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripTempMcGuiaEscora))

        self.leitura_RD_TripTempMcGuiaContraEscora = LeituraModbusCoil(f"[UG{self.__ug.id}] Mancal Guia Contra Escora Trip Temperatura", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripTempMcGuiaContraEscora"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempMcGuiaContraEscora.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_TripTempMcGuiaContraEscora))

        # Retornos Digitais - FALHAS
        self.leitura_RD_CLP_Falha = LeituraModbusCoil(f"[UG{self.__ug.id}] CLP Falha", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_FalhaComuCLP"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_CLP_Falha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_CLP_Falha))

        self.leitura_RD_Q_Negativa = LeituraModbusCoil(f"[UG{self.__ug.id}] Q Negativa", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_IHM_Q_Negativa"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_Q_Negativa.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_Q_Negativa))

        self.leitura_RD_Remota_Falha = LeituraModbusCoil(f"[UG{self.__ug.id}] Falha Remota", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_FalhaComuRemota"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_Remota_Falha.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_Remota_Falha))

        self.leitura_RD_FalhaIbntDisjGer = LeituraModbusCoil(f"[UG{self.__ug.id}] Dijuntor Gerador Falha", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_FalhaIbntDisjGer"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_FalhaIbntDisjGer.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_FalhaIbntDisjGer))

        self.leitura_RD_UHRV_FalhaAcionBbaM1 = LeituraModbusCoil(f"[UG{self.__ug.id}] UHRV Bomba 1 Falha Acionamento", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_UHRV_FalhaAcionBbaM1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHRV_FalhaAcionBbaM1.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_UHRV_FalhaAcionBbaM1))

        self.leitura_RD_UHRV_FalhaAcionBbaM2 = LeituraModbusCoil(f"[UG{self.__ug.id}] UHRV Bomba 2 Falha Acionamento", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_UHRV_FalhaAcionBbaM2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHRV_FalhaAcionBbaM2.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_UHRV_FalhaAcionBbaM2))

        self.leitura_RD_UHLM_FalhaAcionBbaM1 = LeituraModbusCoil(f"[UG{self.__ug.id}] UHLM Bomba 1 Falha Acionamento", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_UHLM_FalhaAcionBbaM1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHLM_FalhaAcionBbaM1.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_UHLM_FalhaAcionBbaM1))

        self.leitura_RD_UHLM_FalhaAcionBbaM2 = LeituraModbusCoil(f"[UG{self.__ug.id}] UHLM Bomba 2 Falha Acionamento", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_UHLM_FalhaAcionBbaM2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHLM_FalhaAcionBbaM2.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_UHLM_FalhaAcionBbaM2))

        self.leitura_RD_FalhaAcionFechaValvBorb = LeituraModbusCoil(f"[UG{self.__ug.id}] Válvula Borboleta Falha Acionamento Fechamento", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_FalhaAcionFechaValvBorb"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_FalhaAcionFechaValvBorb.descr, CONDIC_INDISPONIBILIZAR, self.leitura_RD_FalhaAcionFechaValvBorb))
