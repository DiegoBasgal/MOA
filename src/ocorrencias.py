import pytz
import logging
import traceback

import src.mensageiro.dict as vd
import src.dicionarios.dict as d

from time import time
from datetime import datetime

from src.funcoes.leitura import *
from src.dicionarios.reg import *
from src.dicionarios.const import *
from src.funcoes.condicionador import *

from src.conectores.banco_dados import BancoDados


logger = logging.getLogger("logger")

class OcorrenciasGerais:
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

        self.leitura_ED_SA_SEL787_Trip = LeituraModbusCoil("[SA] SEL 787 Trip", self.__clp["SA"], REG["SA"]["ED_SEL787_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_SEL787_Trip, CONDIC_INDISPONIBILIZAR,))
        return


        ### Leituras para acionamento temporizado por chamada Voip
        ## CONDICIONADORES ESSENCIAIS
                # Leituras para acionamento periódico
        self.leitura_ED_SA_GMG_Trip = LeituraModbusCoil("[USN] Grupo Motor Gerador Trip", self.__clp["SA"], REG["SA"]["ED_GMG_Trip"])
        self.leitura_ED_SA_GMG_Alarme = LeituraModbusCoil("[USN] Grupo Motor Gerador Alarme", self.__clp["SA"], REG["SA"]["ED_GMG_Alarme"])
        self.leitura_ED_SA_GMG_Operacao = LeituraModbusCoil("[USN] Grupo Motor Gerador Operação", self.__clp["SA"], REG["SA"]["ED_GMG_Operacao"])
        self.leitura_RD_FalhaComunSETDA = LeituraModbusCoil("[USN] CLP TDA Falha", self.__clp["SA"], REG["SA"]["RD_FalhaComunSETDA"])
        self.leitura_ED_SA_GMG_BaixoComb = LeituraModbusCoil("[USN] ED_SA_GMG_BaixoComb", self.__clp["SA"], REG["SA"]["ED_GMG_BaixoComb"])
        self.leitura_RD_SA_GMG_FalhaAcion = LeituraModbusCoil("[USN] Grupo Motor Gerador Falha Acionamento", self.__clp["SA"], REG["SA"]["RD_GMG_FalhaAcion"])
        self.leitura_ED_SA_QLCF_Disj52ETrip = LeituraModbusCoil("[USN] Disjuntor 52E Trip", self.__clp["SA"], REG["SA"]["ED_QLCF_Disj52ETrip"])
        self.leitura_RD_BbaDren1_FalhaAcion = LeituraModbusCoil("[USN] Bomba Drenagem 1 Falha Acionamento", self.__clp["SA"], REG["SA"]["RD_BbaDren1_FalhaAcion"])
        self.leitura_RD_BbaDren2_FalhaAcion = LeituraModbusCoil("[USN] Bomba Drenagem 2 Falha Acionamento", self.__clp["SA"], REG["SA"]["RD_BbaDren2_FalhaAcion"])
        self.leitura_RD_BbaDren3_FalhaAcion = LeituraModbusCoil("[USN] Bomba Drenagem 3 Falha Acionamento", self.__clp["SA"], REG["SA"]["RD_BbaDren3_FalhaAcion"])
        self.leitura_ED_SA_QLCF_TripDisjAgrup = LeituraModbusCoil("[USN] Disjuntor Agrupamento Trip", self.__clp["SA"], REG["SA"]["ED_QLCF_TripDisjAgrup"])
        self.leitura_ED_SA_QCAP_Disj52EFechado = LeituraModbusCoil("[USN] Disjuntor 52E Fechado", self.__clp["SA"], REG["SA"]["ED_QCAP_Disj52EFechado"])
        self.leitura_ED_SA_QCADE_BombasDng_Auto = LeituraModbusCoil("[USN] Bombas Drenagem Automático", self.__clp["SA"], REG["SA"]["ED_QCADE_BombasDng_Auto"])
        self.leitura_ED_SA_QCAP_SubtensaoBarraGeral = LeituraModbusCoil("[USN] Subtensão Barramento Geral", self.__clp["SA"], REG["SA"]["ED_QCAP_SubtensaoBarraGeral"])

        ### CONDICIONADORES ESSENCIAIS

        # # Óleo do Transformador Elevador
        # self.l_temp_oleo_trafo = LeituraModbus(f"[UG{self.__ug.id}] Óleo do Transformador Elevador", self.__clp["SA"], REG["SA"]["EA_TE_TempOleo"], escala=0.1, op=4)
        # self.c_temp_oleo_trafo = CondicionadorExponencial(self.l_temp_oleo_trafo, CONDIC_INDISPONIBILIZAR)
        # self.condicionadores_essenciais.append(self.c_temp_oleo_trafo)

        self.l_ED_SA_FalhaDisjTPsSincrG2 = LeituraModbusCoil("SA -> Trasformador Potencial Disjuntor Sincronização Falha", self.__clp["SA"], REG["SA"]["ED_FalhaDisjTPsSincrG2"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_SA_FalhaDisjTPsSincrG2, CONDIC_INDISPONIBILIZAR))

        self.l_ED_SA_DisjDJ1_AlPressBaixa = LeituraModbusCoil("SA -> Disjutor 1 Alarme Pressão Baixa", self.__clp["SA"], REG["SA"]["ED_DisjDJ1_AlPressBaixa"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_SA_DisjDJ1_AlPressBaixa, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_DisjDJ1_BloqPressBaixa = LeituraModbusCoil(f"[SA-UG{self.__ug.id}] Disjuntor 1 Bloqueio Pressão Baixa", self.__clp["SA"], REG["SA"]["ED_DisjDJ1_BloqPressBaixa"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_DisjDJ1_BloqPressBaixa, CONDIC_INDISPONIBILIZAR,))

        # self.leitura_ED_SA_QCAP_TensaoPresenteTSA = LeituraModbusCoil("[SA] TSA Tensão Presente", self.__clp["SA"], REG["SA"]["ED_QCAP_TensaoPresenteTSA"])
        # self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_QCAP_TensaoPresenteTSA, CONDIC_NORMALIZAR,))

        self.leitura_ED_SA_SEL787_Trip = LeituraModbusCoil("[SA] SEL 787 Trip", self.__clp["SA"], REG["SA"]["ED_SEL787_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_SEL787_Trip, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_SEL311_Trip = LeituraModbusCoil("[SA] SEL 311 Trip", self.__clp["SA"], REG["SA"]["ED_SEL311_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_SEL311_Trip, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_MRU3_Trip = LeituraModbusCoil("[SA] MRU3 Trip", self.__clp["SA"], REG["SA"]["ED_MRU3_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_MRU3_Trip, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_MRL1_Trip = LeituraModbusCoil("[SA] MRL1 Trip", self.__clp["SA"], REG["SA"]["ED_MRL1_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_MRL1_Trip, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_QCADE_Disj52E1Trip = LeituraModbusCoil("[SA] Dijuntor 52E1 Trip", self.__clp["SA"], REG["SA"]["ED_QCADE_Disj52E1Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Disj52E1Trip, CONDIC_INDISPONIBILIZAR,))

        ### CONDICIONADORES NORMAIS
        if not d.glb["TDA_Offline"]:
            self.leitura_ED_TDA_QcataDisj52ETrip = LeituraModbusCoil("[TDA] Disjuntor 52E Trip", self.__clp["TDA"], REG["TDA"]["ED_QcataDisj52ETrip"])
            self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52ETrip, CONDIC_INDISPONIBILIZAR,))

            self.leitura_ED_TDA_QcataDisj52ETripDisjSai = LeituraModbusCoil("[TDA] Disjuntor 52E Saída Trip", self.__clp["TDA"], REG["TDA"]["ED_QcataDisj52ETripDisjSai"])
            self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52ETripDisjSai, CONDIC_INDISPONIBILIZAR,))

            # self.leitura_ED_TDA_QcataDisj52EFalha380VCA = LeituraModbusCoil("[TDA] Disjuntor 52E Falha 380 VCA", self.__clp["TDA"], REG["TDA"]["ED_QcataDisj52EFalha380VCA"])
            # self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52EFalha380VCA, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_MRU3_Falha = LeituraModbusCoil("[SA] MRU3 Falha", self.__clp["SA"], REG["SA"]["ED_MRU3_Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_MRU3_Falha, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_SEL787_FalhaInterna = LeituraModbusCoil("[SA] SEL 787 Falha", self.__clp["SA"], REG["SA"]["ED_SEL787_FalhaInterna"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_SEL787_FalhaInterna, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_SEL311_Falha = LeituraModbusCoil("[SA] SEL 311 Falha", self.__clp["SA"], REG["SA"]["ED_SEL311_Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_SEL311_Falha, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_CTE_Falta125Vcc = LeituraModbusCoil("[SA] CTE Falta 125 Vcc", self.__clp["SA"], REG["SA"]["ED_CTE_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CTE_Falta125Vcc, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_CTE_Secc89TE_Aberta = LeituraModbusCoil("[SA] CTE Seccionadora 89TE Aberta", self.__clp["SA"], REG["SA"]["ED_CTE_Secc89TE_Aberta"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CTE_Secc89TE_Aberta, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_TE_AlarmeDetectorGas = LeituraModbusCoil("[SA] Detector de Gás Alarme", self.__clp["SA"], REG["SA"]["ED_TE_AlarmeDetectorGas"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeDetectorGas, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_TE_AlarmeNivelMaxOleo = LeituraModbusCoil("[SA] Transformador Elevador Alarme Nível Máximo Óleo", self.__clp["SA"], REG["SA"]["ED_TE_AlarmeNivelMaxOleo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeNivelMaxOleo, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_TE_AlarmeAlivioPressao = LeituraModbusCoil("[SA] Transformador Elevador Alarme Alívio Pressão", self.__clp["SA"], REG["SA"]["ED_TE_AlarmeAlivioPressao"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeAlivioPressao, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_TE_AlarmeTempOleo = LeituraModbusCoil("[SA] Transformador Elevador Alarme Temperatura Óleo", self.__clp["SA"], REG["SA"]["ED_TE_AlarmeTempOleo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeTempOleo, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_TE_AlarmeTempEnrolamento = LeituraModbusCoil("[SA] Transformador Elevador Alarme Temperatura Enrolamento", self.__clp["SA"], REG["SA"]["ED_TE_AlarmeTempEnrolamento"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeTempEnrolamento, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_TE_AlarmeDesligamento = LeituraModbusCoil("[SA] Transformador Elevador Alarme Desligamento", self.__clp["SA"], REG["SA"]["ED_TE_AlarmeDesligamento"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeDesligamento, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_TE_Falha = LeituraModbusCoil("[SA] Transformador Elevador Falha", self.__clp["SA"], REG["SA"]["ED_TE_Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_Falha, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_FalhaDisjTPsProt = LeituraModbusCoil("[SA] Disjuntor Transformador Potencial Falha", self.__clp["SA"], REG["SA"]["ED_FalhaDisjTPsProt"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_FalhaDisjTPsProt, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_FalhaDisjTPsSincr = LeituraModbusCoil("[SA] Disjuntor Transformador Potencial Falha Sincronização", self.__clp["SA"], REG["SA"]["ED_FalhaDisjTPsSincr"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_FalhaDisjTPsSincr, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_CSA1_Secc_Aberta = LeituraModbusCoil("[SA] CSA1 Seccionadora Aberta", self.__clp["SA"], REG["SA"]["ED_CSA1_Secc_Aberta"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_Secc_Aberta, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_CSA1_FusivelQueimado = LeituraModbusCoil("[SA] CSA1 Fusível Queimado", self.__clp["SA"], REG["SA"]["ED_CSA1_FusivelQueimado"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_FusivelQueimado, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_CSA1_FaltaTensao125Vcc = LeituraModbusCoil("[SA] CSA1 Falta Tensão 125 Vcc", self.__clp["SA"], REG["SA"]["ED_CSA1_FaltaTensao125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_FaltaTensao125Vcc, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_QCADE_Nivel4 = LeituraModbusCoil("[SA] CA Drenagem Nível 4", self.__clp["SA"], REG["SA"]["ED_QCADE_Nivel4"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Nivel4, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_QCADE_NivelMuitoAlto = LeituraModbusCoil("[SA] CA Drenagem Nível Muito Alto", self.__clp["SA"], REG["SA"]["ED_QCADE_NivelMuitoAlto"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_NivelMuitoAlto, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_QCADE_Falha220VCA = LeituraModbusCoil("[SA] CA Drenagem Falha 220 VCA", self.__clp["SA"], REG["SA"]["ED_QCADE_Falha220VCA"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Falha220VCA, CONDIC_INDISPONIBILIZAR,))

        # Verificar
        self.leitura_ED_SA_QCCP_Disj72ETrip = LeituraModbusCoil("[SA] QCCP Disjuntor 72E Trip", self.__clp["SA"], REG["SA"]["ED_QCCP_Disj72ETrip"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_Disj72ETrip, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_QCCP_Falta125Vcc = LeituraModbusCoil("[SA] QCCP Falta 125 Vcc", self.__clp["SA"], REG["SA"]["ED_QCCP_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_Falta125Vcc, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_QCCP_TripDisjAgrup = LeituraModbusCoil("[SA] QCCP Disjuntor Agrupamento Trip", self.__clp["SA"], REG["SA"]["ED_QCCP_TripDisjAgrup"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_TripDisjAgrup, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_QCAP_Falta125Vcc = LeituraModbusCoil("[SA] CA Principal Falta 125 Vcc", self.__clp["SA"], REG["SA"]["ED_QCAP_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Falta125Vcc, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_QCAP_TripDisjAgrup = LeituraModbusCoil("[SA] CA Principal Disjuntor Agrupamento Trip", self.__clp["SA"], REG["SA"]["ED_QCAP_TripDisjAgrup"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_TripDisjAgrup, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_QCAP_Disj52A1Falha = LeituraModbusCoil("[SA] CA Principal Disjuntor 52A1 Falha", self.__clp["SA"], REG["SA"]["ED_QCAP_Disj52A1Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Disj52A1Falha, CONDIC_INDISPONIBILIZAR,))

        self.leitura_ED_SA_QCAP_Disj52EFalha = LeituraModbusCoil("[SA] CA Principal Disjuntor 52E Falha", self.__clp["SA"], REG["SA"]["ED_QCAP_Disj52EFalha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Disj52EFalha, CONDIC_INDISPONIBILIZAR,))

        # self.leitura_ED_SA_GMG_DisjFechado = LeituraModbusCoil("[SA] Disjuntor Grupo Motor Gerador Fechado", self.__clp["SA"], REG["SA"]["ED_GMG_DisjFechado"])
        # self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_GMG_DisjFechado, CONDIC_INDISPONIBILIZAR,))

        self.leitura_RD_DJ1_FalhaInt = LeituraModbusCoil("[SA] Disjuntor 1 Falha Interna", self.__clp["SA"], REG["SA"]["RD_DJ1_FalhaInt"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_DJ1_FalhaInt, CONDIC_INDISPONIBILIZAR,))

        self.l_RD_CLP_Falha = LeituraModbusCoil("[SA] CLP SA Falha", self.__clp["SA"], REG["SA"]["RD_FalhaComuCLP"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_CLP_Falha, CONDIC_INDISPONIBILIZAR,))

        self.leitura_RA_SEL787_Targets = LeituraModbusCoil("[SA] SEL 787 Targets", self.__clp["SA"], REG["SA"]["RA_SEL787_Targets"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets, CONDIC_INDISPONIBILIZAR,))

        self.leitura_RA_SEL787_Targets_Links_Bit00 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 0", self.__clp["SA"], REG["SA"]["RA_SEL787_Targets_Links_Bit00"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit00, CONDIC_INDISPONIBILIZAR,))

        # self.leitura_RA_SEL787_Targets_Links_Bit01 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 1", self.__clp["SA"], REG["SA"]["RA_SEL787_Targets_Links_Bit01"])
        # self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit01, CONDIC_INDISPONIBILIZAR,))

        self.leitura_RA_SEL787_Targets_Links_Bit02 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 2", self.__clp["SA"], REG["SA"]["RA_SEL787_Targets_Links_Bit02"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit02, CONDIC_INDISPONIBILIZAR,))

        self.leitura_RA_SEL787_Targets_Links_Bit03 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 3", self.__clp["SA"], REG["SA"]["RA_SEL787_Targets_Links_Bit03"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit03, CONDIC_INDISPONIBILIZAR,))

        self.leitura_RA_SEL787_Targets_Links_Bit04 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 4", self.__clp["SA"], REG["SA"]["RA_SEL787_Targets_Links_Bit04"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit04, CONDIC_INDISPONIBILIZAR,))

        # self.leitura_RA_SEL787_Targets_Links_Bit05 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 5", self.__clp["SA"], REG["SA"]["RA_SEL787_Targets_Links_Bit05"])
        # self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit05, CONDIC_INDISPONIBILIZAR,))

        # self.leitura_RA_SEL787_Targets_Links_Bit06 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 6", self.__clp["SA"], REG["SA"]["RA_SEL787_Targets_Links_Bit06"])
        # self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit06, CONDIC_INDISPONIBILIZAR,))

        self.leitura_RA_SEL787_Targets_Links_Bit07 = LeituraModbusCoil("[SA] SEL 787 Targets Bit 7", self.__clp["SA"], REG["SA"]["RA_SEL787_Targets_Links_Bit07"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit07, CONDIC_INDISPONIBILIZAR,))

        return


class OcorrenciasUnidades:
    def __init__(self, ug, clp: "ModbusClient"=None, db: BancoDados=None):

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__ug = ug
        self.__db = db
        self.__clp = clp

        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS

        self._condicionadores: "list[CondicionadorBase]" = []
        self._condicionadores_essenciais: "list[CondicionadorBase]" = []

        self._leitura_dict: "dict[str, LeituraModbus]" = {}
        self._condic_dict: "dict[str, CondicionadorBase]" = {}


        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.leitura_voip: "dict[str, LeituraModbus]" = {}


        # FINALIZAÇÃO DO __INIT__

        self.carregar_leituras()


    @property
    def condic_dict(self) -> "dict[str, CondicionadorExponencial]":
        # PROPRIEDADE -> Retrona o dicionário de condicionadores da Unidade.

        return self._condic_dict

    @condic_dict.setter
    def condic_dict(self, var: "dict[str, CondicionadorExponencial]") -> "None":
        # SETTER -> Atrubui o novo dicionário de condicionadores da Unidade.

        self._condic_dict = var

    @property
    def leitura_dict(self) -> "dict[str, LeituraModbus]":
        # PROPRIEDADE -> Retrona o dicionário de leituras da Unidade.

        return self._leitura_dict

    @leitura_dict.setter
    def leitura_dict(self, var: "dict[str, LeituraModbus]") -> "None":
        # SETTER -> Atrubui o novo dicionário de leituras da Unidade.

        self._leitura_dict = var

    @property
    def condicionadores(self) -> "list[CondicionadorBase]":
        # PROPRIEDADE -> Retrona a lista de condicionadores da Unidade.

        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[CondicionadorBase]") -> "None":
        # SETTER -> Atrubui a nova lista de condicionadores da Unidade.

        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[CondicionadorBase]":
        # PROPRIEDADE -> Retrona a lista de condicionadores essenciais da Unidade.

        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[CondicionadorBase]") -> "None":
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
            self.c_temp_fase_r.valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{self.__ug.id}"])
            self.c_temp_fase_s.valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{self.__ug.id}"])
            self.c_temp_fase_t.valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{self.__ug.id}"])
            self.c_temp_nucleo_estator.valor_base = float(parametros[f"alerta_temperatura_nucleo_estator_ug{self.__ug.id}"])
            self.c_temp_mrd_1.valor_base = float(parametros[f"alerta_temperatura_mancal_rad_dia_1_ug{self.__ug.id}"])
            self.c_temp_mrd_2.valor_base = float(parametros[f"alerta_temperatura_mancal_rad_dia_2_ug{self.__ug.id}"])
            self.c_temp_mrt_1.valor_base = float(parametros[f"alerta_temperatura_mancal_rad_tra_1_ug{self.__ug.id}"])
            self.c_temp_mrt_2.valor_base = float(parametros[f"alerta_temperatura_mancal_rad_tra_2_ug{self.__ug.id}"])
            self.c_temp_saida_ar.valor_base = float(parametros[f"alerta_temperatura_saida_de_ar_ug{self.__ug.id}"])
            self.c_temp_mge.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_escora_ug{self.__ug.id}"])
            self.c_temp_mgr.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_radial_ug{self.__ug.id}"])
            self.c_temp_mgce.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_contra_ug{self.__ug.id}"])
            self.c_pressao_cx_espiral.valor_base = float(parametros[f"alerta_caixa_espiral_ug{self.__ug.id}"])

            self.c_temp_fase_r.valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{self.__ug.id}"])
            self.c_temp_fase_s.valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{self.__ug.id}"])
            self.c_temp_fase_t.valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{self.__ug.id}"])
            self.c_temp_nucleo_estator.valor_limite = float(parametros[f"limite_temperatura_nucleo_estator_ug{self.__ug.id}"])
            self.c_temp_mrd_1.valor_limite = float(parametros[f"limite_temperatura_mancal_rad_dia_1_ug{self.__ug.id}"])
            self.c_temp_mrd_2.valor_limite = float(parametros[f"limite_temperatura_mancal_rad_dia_2_ug{self.__ug.id}"])
            self.c_temp_mrt_1.valor_limite = float(parametros[f"limite_temperatura_mancal_rad_tra_1_ug{self.__ug.id}"])
            self.c_temp_mrt_2.valor_limite = float(parametros[f"limite_temperatura_mancal_rad_tra_2_ug{self.__ug.id}"])
            self.c_temp_saida_ar.valor_limite = float(parametros[f"limite_temperatura_saida_de_ar_ug{self.__ug.id}"])
            self.c_temp_mge.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_escora_ug{self.__ug.id}"])
            self.c_temp_mgr.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_radial_ug{self.__ug.id}"])
            self.c_temp_mgce.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_contra_ug{self.__ug.id}"])
            self.c_pressao_cx_espiral.valor_limite = float(parametros[f"limite_caixa_espiral_ug{self.__ug.id}"])

        except Exception:
            logger.error(f"[OCO-UG{self.__ug.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores.")
            logger.debug(f"[OCO-UG{self.__ug.id}] Traceback: {traceback.format_exc()}")

    def controle_limites_operacao(self) -> "None":
        """
        Função para verificação de limites de operação da Unidade.

        Verifica os valores base e limite da Unidade, pré-determinados na interface
        WEB, e avisa o operador caso algum valor ultrapasse o estipulado.
        """

        if self.l_temp_fase_r.valor >= self.c_temp_fase_r.valor_base:
            logger.debug("")
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura de Fase R da UG passou do valor base! ({self.c_temp_fase_r.valor_base} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_fase_r.valor} C")

        if self.l_temp_fase_r.valor >= 0.9 * (self.c_temp_fase_r.valor_limite - self.c_temp_fase_r.valor_base) + self.c_temp_fase_r.valor_base:
            logger.debug("")
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura de Fase R da UG está muito próxima do limite! ({self.c_temp_fase_r.valor_limite} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_fase_r.valor} C")


        if self.l_temp_fase_s.valor >= self.c_temp_fase_s.valor_base:
            logger.debug("")
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura de Fase S da UG passou do valor base! ({self.c_temp_fase_s.valor_base} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_fase_s.valor} C")

        if self.l_temp_fase_s.valor >= 0.9 * (self.c_temp_fase_s.valor_limite - self.c_temp_fase_s.valor_base) + self.c_temp_fase_s.valor_base:
            logger.debug("")
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura de Fase S da UG está muito próxima do limite! ({self.c_temp_fase_s.valor_limite} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_fase_s.valor} C")


        if self.l_temp_fase_t.valor >= self.c_temp_fase_t.valor_base:
            logger.debug("")
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura de Fase T da UG passou do valor base! ({self.c_temp_fase_t.valor_base} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_fase_t.valor} C")

        if self.l_temp_fase_t.valor >= 0.9 * (self.c_temp_fase_t.valor_limite - self.c_temp_fase_t.valor_base) + self.c_temp_fase_t.valor_base:
            logger.debug("")
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura de Fase T da UG está muito próxima do limite! ({self.c_temp_fase_t.valor_limite} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_fase_t.valor} C")


        if self.l_temp_nucleo_estator.valor >= self.c_temp_nucleo_estator.valor_base:
            logger.debug("")
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Núcleo Gerador Estator da UG passou do valor base! ({self.c_temp_nucleo_estator.valor_base} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_nucleo_estator.valor} C")

        if self.l_temp_nucleo_estator.valor >= 0.9 * (self.c_temp_nucleo_estator.valor_limite - self.c_temp_nucleo_estator.valor_base) + self.c_temp_nucleo_estator.valor_base:
            logger.debug("")
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Núcleo Gerador Estator da UG está muito próxima do limite! ({self.c_temp_nucleo_estator.valor_limite} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_nucleo_estator.valor} C")


        if self.l_temp_mrd_1.valor >= self.c_temp_mrd_1.valor_base:
            logger.debug("")
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Dianteiro 1 da UG passou do valor base! ({self.c_temp_mrd_1.valor_base} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_mrd_1.valor} C")

        if self.l_temp_mrd_1.valor >= 0.9 * (self.c_temp_mrd_1.valor_limite - self.c_temp_mrd_1.valor_base) + self.c_temp_mrd_1.valor_base:
            logger.debug("")
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Dianteiro 1 da UG está muito próxima do limite! ({self.c_temp_mrd_1.valor_limite} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_mrd_1.valor} C")


        if self.l_temp_mrd_2.valor >= self.c_temp_mrd_2.valor_base:
            logger.debug("")
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Dianteiro 2 da UG passou do valor base! ({self.c_temp_mrd_2.valor_base} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_mrd_2.valor} C")

        if self.l_temp_mrd_2.valor >= 0.9 * (self.c_temp_mrd_2.valor_limite - self.c_temp_mrd_2.valor_base) + self.c_temp_mrd_2.valor_base:
            logger.debug("")
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Dianteiro 2 da UG está muito próxima do limite! ({self.c_temp_mrd_2.valor_limite} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_mrd_2.valor} C")


        if self.l_temp_mrt_1.valor >= self.c_temp_mrt_1.valor_base:
            logger.debug("")
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Traseiro 1 da UG passou do valor base! ({self.c_temp_mrt_1.valor_base} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_mrt_1.valor} C")

        if self.l_temp_mrt_1.valor >= 0.9 * (self.c_temp_mrt_1.valor_limite - self.c_temp_mrt_1.valor_base) + self.c_temp_mrt_1.valor_base:
            logger.debug("")
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Traseiro 1 da UG está muito próxima do limite! ({self.c_temp_mrt_1.valor_limite} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_mrt_1.valor} C")


        if self.l_temp_mrt_2.valor >= self.c_temp_mrt_2.valor_base:
            logger.debug("")
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Traseiro 2 da UG passou do valor base! ({self.c_temp_mrt_2.valor_base} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_mrt_2.valor} C")

        if self.l_temp_mrt_2.valor >= 0.9 * (self.c_temp_mrt_2.valor_limite - self.c_temp_mrt_2.valor_base) + self.c_temp_mrt_2.valor_base:
            logger.debug("")
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Radial Traseiro 2 da UG está muito próxima do limite! ({self.c_temp_mrt_2.valor_limite} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_mrt_2.valor} C")


        if self.l_temp_saida_ar.valor >= self.c_temp_saida_ar.valor_base:
            logger.debug("")
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura da Saída de Ar da UG passou do valor base! ({self.c_temp_saida_ar.valor_base} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_saida_ar.valor} C")

        if self.l_temp_saida_ar.valor >= 0.9 * (self.c_temp_saida_ar.valor_limite - self.c_temp_saida_ar.valor_base) + self.c_temp_saida_ar.valor_base:
            logger.debug("")
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura da Saída de Ar da UG está muito próxima do limite! ({self.c_temp_saida_ar.valor_limite} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_saida_ar.valor} C")


        if self.l_temp_mge.valor >= self.c_temp_mge.valor_base:
            logger.debug("")
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Guia Escora da UG passou do valor base! ({self.c_temp_mge.valor_base} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_mge.valor} C")

        if self.l_temp_mge.valor >= 0.9*(self.c_temp_mge.valor_limite - self.c_temp_mge.valor_base) + self.c_temp_mge.valor_base:
            logger.debug("")
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Guia Escora da UG está muito próxima do limite! ({self.c_temp_mge.valor_limite} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_mge.valor} C")


        if self.l_temp_mgce.valor >= self.c_temp_mgce.valor_base:
            logger.debug("")
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Guia Contra Escora da UG passou do valor base! ({self.c_temp_mgce.valor_base} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_mgce.valor} C")

        if self.l_temp_mgce.valor >= 0.9*(self.c_temp_mgce.valor_limite - self.c_temp_mgce.valor_base) + self.c_temp_mgce.valor_base:
            logger.debug("")
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Guia Contra Escora da UG está muito próxima do limite! ({self.c_temp_mgce.valor_limite} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_mgce.valor} C")


        if self.l_temp_mgr.valor >= self.c_temp_mgr.valor_base:
            logger.debug("")
            logger.warning(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Guia Radial da UG passou do valor base! ({self.c_temp_mgr.valor_base} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_mgr.valor} C")

        if self.l_temp_mgr.valor >= 0.9*(self.c_temp_mgr.valor_limite - self.c_temp_mgr.valor_base) + self.c_temp_mgr.valor_base:
            logger.debug("")
            logger.critical(f"[OCO-UG{self.__ug.id}] A temperatura do Mancal Guia Radial da UG está muito próxima do limite! ({self.c_temp_mgr.valor_limite} C)")
            logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_temp_mgr.valor} C")


        # if self.l_pressao_cx_espiral.valor <= self.c_pressao_cx_espiral.valor_base and self.l_pressao_cx_espiral.valor != 0 and self.__ug.etapa_atual == UG_SINCRONIZADA:
        #     logger.debug("")
        #     logger.debug(f"[OCO-UG{self.__ug.id}] A pressão Caixa Espiral da UG passou do valor base! ({self.c_pressao_cx_espiral.valor_base:03.2f} KGf/m2)")
        #     logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_pressao_cx_espiral.valor:03.2f}")

        # if self.l_pressao_cx_espiral.valor <= self.c_pressao_cx_espiral.valor_limite and self.l_pressao_cx_espiral.valor != 0 and self.__ug.etapa_atual == UG_SINCRONIZADA:
        #     logger.debug("")
        #     logger.debug(f"[OCO-UG{self.__ug.id}] A pressão Caixa Espiral da UG está muito próxima do limite! ({self.c_pressao_cx_espiral.valor_limite:03.2f} KGf/m2)")
        #     logger.info(f"[OCO-UG{self.__ug.id}] Leitura: {self.l_pressao_cx_espiral.valor:03.2f}")


    def leitura_temporizada(self) -> "None":
        """
        Função para consulta de acionamentos da Unidade e avisos através do mecanismo
        de acionamento temporizado.
        """

        if self.lv_ED_FreioPastilhaGasta.valor != 0:
            logger.warning(f"[OCO-UG{self.__ug.id}] O sensor de Freio da UG retornou que a Pastilha está gasta, favor considerar troca.")

        if self.lv_ED_FiltroPresSujo75Troc.valor != 0:
            logger.warning(f"[OCO-UG{self.__ug.id}] O sensor do Filtro de Pressão UHRV retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.lv_ED_FiltroRetSujo75Troc.valor != 0:
            logger.warning(f"[UG{self.__ug.id}] O sensor do Filtro de Retorno UHRV retornou que filtro está 75% sujo, favor considerar troca.")

        if self.lv_ED_UHLMFilt1PresSujo75Troc.valor != 0:
            logger.warning(f"[OCO-UG{self.__ug.id}] O sensor do Filtro 1 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.lv_ED_UHLMFilt2PresSujo75Troc.valor != 0:
            logger.warning(f"[UG{self.__ug.id}] O sensor do Filtro 2 de Pressão UHLM retornou que o iltro está 75% sujo, favor considerar troca.")

        if self.lv_ED_FiltroPressaoBbaMecSj75.valor != 0:
            logger.warning(f"[OCO-UG{self.__ug.id}] O sensor do Filtro de Pressão da Bomba Mecânica retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.lv_ED_FreioCmdRemoto.valor != 1:
            logger.debug(f"[OCO-UG{self.__ug.id}] O freio da UG saiu do modo remoto, favor analisar a situação.")

        if self.lv_ED_QCAUG_Remoto.valor != 1:
            logger.debug(f"[OCO-UG{self.__ug.id}] O compressor da UG saiu do modo remoto, favor analisar a situação.")

        return

    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Unidade.
        """

        ### CONDICIONADORES ESSENCIAIS
        # R
        self.l_temp_fase_r = LeituraModbus("Temperatura Fase R", self.__clp, REG[f"UG{self.__ug.id}"]["RA_Temperatura_01"], op=4)
        self.c_temp_fase_r = CondicionadorExponencial(self.l_temp_fase_r, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_temp_fase_r)

        # S
        self.l_temp_fase_s = LeituraModbus("Temperatura Fase S", self.__clp, REG[f"UG{self.__ug.id}"]["RA_Temperatura_02"], op=4)
        self.c_temp_fase_s = CondicionadorExponencial(self.l_temp_fase_s, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_temp_fase_s)

        # T
        self.l_temp_fase_t = LeituraModbus("Temperatura Fase T", self.__clp, REG[f"UG{self.__ug.id}"]["RA_Temperatura_03"], op=4)
        self.c_temp_fase_t = CondicionadorExponencial(self.l_temp_fase_t, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_temp_fase_t)

        # Nucleo estator
        self.l_temp_nucleo_estator = LeituraModbus("Temperatura Núcleo Estator", self.__clp, REG[f"UG{self.__ug.id}"]["RA_Temperatura_04"], op=4)
        self.c_temp_nucleo_estator = CondicionadorExponencial(self.l_temp_nucleo_estator, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_temp_nucleo_estator)

        # MRD 1
        self.l_temp_mrd_1 = LeituraModbus("Temperatura Mancal Radial Dianteiro 1", self.__clp, REG[f"UG{self.__ug.id}"]["RA_Temperatura_05"], op=4)
        self.c_temp_mrd_1 = CondicionadorExponencial(self.l_temp_mrd_1, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_temp_mrd_1)

        # MRT 1
        self.l_temp_mrt_1 = LeituraModbus("Temperatura Mancal Radial Traseiro 1", self.__clp, REG[f"UG{self.__ug.id}"]["RA_Temperatura_06"], op=4)
        self.c_temp_mrt_1 = CondicionadorExponencial(self.l_temp_mrt_1, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_temp_mrt_1)

        # MRD 2
        self.l_temp_mrd_2 = LeituraModbus("Temperatura Mancal Radial Dianteiro 2", self.__clp, REG[f"UG{self.__ug.id}"]["RA_Temperatura_07"], op=4)
        self.c_temp_mrd_2 = CondicionadorExponencial(self.l_temp_mrd_2, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_temp_mrd_2)

        # MRT 2
        self.l_temp_mrt_2 = LeituraModbus("Temperatura Mancal Radial Traseiro 2", self.__clp, REG[f"UG{self.__ug.id}"]["RA_Temperatura_08"], op=4)
        self.c_temp_mrt_2 = CondicionadorExponencial(self.l_temp_mrt_2, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_temp_mrt_2)

        # Saída de ar
        self.l_temp_saida_ar = LeituraModbus("Temperatura Saída de Ar", self.__clp, REG[f"UG{self.__ug.id}"]["RA_Temperatura_10"], op=4)
        self.c_temp_saida_ar = CondicionadorExponencial(self.l_temp_saida_ar, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_temp_saida_ar)

        # Mancal Guia Radial
        self.l_temp_mgr = LeituraModbus("Temperatura Mancal Guia Radial", self.__clp, REG[f"UG{self.__ug.id}"]["RA_TempMcGuiaRadial"])
        self.c_temp_mgr = CondicionadorExponencial(self.l_temp_mgr, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_temp_mgr)

        # Mancal Guia escora
        self.l_temp_mge = LeituraModbus("Temperatura Mancal Guia Escora", self.__clp, REG[f"UG{self.__ug.id}"]["RA_TempMcGuiaEscora"])
        self.c_temp_mge = CondicionadorExponencial(self.l_temp_mge, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_temp_mge)

        # Mancal Guia contra_escora
        self.l_temp_mgce = LeituraModbus("Temperatura Mancal Guia Contra Escora", self.__clp, REG[f"UG{self.__ug.id}"]["RA_TempMcGuiaContraEscora"])
        self.c_temp_mgce = CondicionadorExponencial(self.l_temp_mgce, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_temp_mgce)

        self.l_pressao_cx_espiral = LeituraModbus("Pressão Caixa Espiral", self.__clp, REG[f"UG{self.__ug.id}"]["EA_PressK1CaixaExpiral_MaisCasas"], escala=0.01, op=4)
        self.c_pressao_cx_espiral = CondicionadorExponencialReverso(self.l_pressao_cx_espiral, CONDIC_INDISPONIBILIZAR, valor_base=16.5, valor_limite=14)

        ## Comandos Digitais
        # GERAL
        self.l_CD_EmergenciaViaSuper = LeituraModbusCoil("Emergência Via Supervisório", self.__clp, REG[f"UG{self.__ug.id}"]["CD_EmergenciaViaSuper"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.l_CD_EmergenciaViaSuper, CONDIC_NORMALIZAR))

        ## Retornos Digitais
        # TRIPS
        self.l_RD_TripEletrico = LeituraModbusCoil("Trip Elétrico", self.__clp, REG[f"UG{self.__ug.id}"]["RD_TripEletrico"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.l_RD_TripEletrico, CONDIC_NORMALIZAR, [UG_PARANDO, UG_PARADA], self.__ug))
        return

        self.l_RD_700G_Trip = LeituraModbusCoil("SEL 700G Trip", self.__clp, REG[f"UG{self.__ug.id}"]["RD_700G_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.l_RD_700G_Trip, CONDIC_NORMALIZAR, [UG_PARANDO, UG_PARADA], self.__ug))

        self.l_RD_TripMecanico = LeituraModbusCoil("Trip Mecâncio", self.__clp, REG[f"UG{self.__ug.id}"]["RD_TripMecanico"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.l_RD_TripMecanico, CONDIC_INDISPONIBILIZAR))

        ## Entradas Digitais
        # TRIPS
        self.l_ED_RV_Trip = LeituraModbusCoil("RV Trip", self.__clp, REG[f"UG{self.__ug.id}"]["ED_RV_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.l_ED_RV_Trip, CONDIC_INDISPONIBILIZAR))

        self.l_ED_AVR_Trip = LeituraModbusCoil("AVR Trip", self.__clp, REG[f"UG{self.__ug.id}"]["ED_AVR_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.l_ED_AVR_Trip, CONDIC_INDISPONIBILIZAR))

        # RELÉS
        self.l_ED_SEL700G_Atuado = LeituraModbusCoil("SEL 700G Atuado", self.__clp, REG[f"UG{self.__ug.id}"]["ED_SEL700G_Atuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.l_ED_SEL700G_Atuado, CONDIC_INDISPONIBILIZAR))

        self.l_ED_ReleBloqA86MAtuado = LeituraModbusCoil("Bloqueio 86M Atuado", self.__clp, REG[f"UG{self.__ug.id}"]["ED_ReleBloqA86MAtuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.l_ED_ReleBloqA86MAtuado, CONDIC_INDISPONIBILIZAR))

        self.l_ED_ReleBloqA86HAtuado = LeituraModbusCoil("Bloqueio 86H Atuado", self.__clp, REG[f"UG{self.__ug.id}"]["ED_ReleBloqA86HAtuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.l_ED_ReleBloqA86HAtuado, CONDIC_NORMALIZAR, [UG_SINCRONIZADA], self.__ug))


        ### CONDICIONADORES NORMAIS
        # Entradas Digitais
        # TRIPS
        self.l_ED_UHRV_TripBomba1 = LeituraModbusCoil("UHRV Bomba 1 Trip", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHRV_TripBomba1"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_UHRV_TripBomba1, CONDIC_INDISPONIBILIZAR))

        self.l_ED_UHRV_TripBomba2 = LeituraModbusCoil("UHRV Bomba 2 Trip", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHRV_TripBomba2"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_UHRV_TripBomba2, CONDIC_INDISPONIBILIZAR))

        self.l_ED_UHLM_TripBomba1 = LeituraModbusCoil("UHLM Bomba 1 Trip", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHLM_TripBomba1"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_UHLM_TripBomba1, CONDIC_INDISPONIBILIZAR))

        self.l_ED_UHLM_TripBomba2 = LeituraModbusCoil("UHLM Bomba 2 Trip", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHLM_TripBomba2"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_UHLM_TripBomba2, CONDIC_INDISPONIBILIZAR))

        self.l_ED_QCAUG_TripDisj52A1 = LeituraModbusCoil("QCAUG Disjuntor 52A1 Trip", self.__clp, REG[f"UG{self.__ug.id}"]["ED_QCAUG_TripDisj52A1"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_QCAUG_TripDisj52A1, CONDIC_INDISPONIBILIZAR))

        self.l_ED_TripAlimPainelFreio = LeituraModbusCoil("Alimentação Painel Freio Trip", self.__clp, REG[f"UG{self.__ug.id}"]["ED_TripAlimPainelFreio"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_TripAlimPainelFreio, CONDIC_INDISPONIBILIZAR))

        self.l_ED_QCAUG_TripDisjAgrup = LeituraModbusCoil("QCAUG Disjuntor Agrupamento Trip", self.__clp, REG[f"UG{self.__ug.id}"]["ED_QCAUG_TripDisjAgrup"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_QCAUG_TripDisjAgrup, CONDIC_INDISPONIBILIZAR))

        # FALHAS
        self.l_ED_AVR_FalhaInterna = LeituraModbusCoil("AVR Falha Interna", self.__clp, REG[f"UG{self.__ug.id}"]["ED_AVR_FalhaInterna"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_AVR_FalhaInterna, CONDIC_INDISPONIBILIZAR))

        self.l_ED_SEL700G_FalhaInterna = LeituraModbusCoil("SEL 700G Falha Interna", self.__clp, REG[f"UG{self.__ug.id}"]["ED_SEL700G_FalhaInterna"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_SEL700G_FalhaInterna, CONDIC_INDISPONIBILIZAR))

        self.l_ED_QCAUG_Falha380VcaPainel = LeituraModbusCoil("QCAUG Falha 380 VCA Painel", self.__clp, REG[f"UG{self.__ug.id}"]["ED_QCAUG_Falha380VcaPainel"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_QCAUG_Falha380VcaPainel, CONDIC_NORMALIZAR))

        # FALTAS
        self.l_ED_Falta125Vcc = LeituraModbusCoil("Falta 125 Vcc", self.__clp, REG[f"UG{self.__ug.id}"]["ED_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_Falta125Vcc, CONDIC_INDISPONIBILIZAR))

        self.l_ED_Falta125VccCom = LeituraModbusCoil("Falta 125 Vcc Com", self.__clp, REG[f"UG{self.__ug.id}"]["ED_Falta125VccCom"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_Falta125VccCom, CONDIC_INDISPONIBILIZAR))

        self.l_ED_FaltaFluxoOleoMc = LeituraModbusCoil("Falta Fluxo Óleo MC", self.__clp, REG[f"UG{self.__ug.id}"]["ED_FaltaFluxoOleoMc"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_FaltaFluxoOleoMc, CONDIC_INDISPONIBILIZAR))

        self.l_ED_Falta125VccAlimVal = LeituraModbusCoil("Falta 125 Vcc Alimentação", self.__clp, REG[f"UG{self.__ug.id}"]["ED_Falta125VccAlimVal"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_Falta125VccAlimVal, CONDIC_INDISPONIBILIZAR))

        self.l_ED_UHLM_FaltaFluxTroc = LeituraModbusCoil("UHLM Falta Fluxo", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHLM_FaltaFluxTroc"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_UHLM_FaltaFluxTroc, CONDIC_INDISPONIBILIZAR))

        self.l_ED_UHLM_FaltaPressTroc = LeituraModbusCoil("UHLM Falta Pressão", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHLM_FaltaPressTroc"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_UHLM_FaltaPressTroc, DEVE_INDISPONIBILZIAR))

        # Controle UHRV
        self.l_ED_UHRV_NivOleominimoPos36 = LeituraModbusCoil("UHRV Óleo Nível Mínimo Posição 36", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHRV_NivOleominimoPos36"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_UHRV_NivOleominimoPos36, CONDIC_INDISPONIBILIZAR))

        self.l_ED_UHRV_NivOleoCriticoPos35 = LeituraModbusCoil("UHRV Óleo Nível Crítico Posição 35", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHRV_NivOleoCriticoPos35"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_UHRV_NivOleoCriticoPos35, CONDIC_INDISPONIBILIZAR))

        # Controle UHLM
        self.l_ED_UHLM_FluxoMcTras = LeituraModbusCoil("UHLM Fluxo Traseiro MC", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHLM_FluxoMcTras"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_UHLM_FluxoMcTras, CONDIC_INDISPONIBILIZAR))

        self.l_ED_UHLM_NivelminOleo = LeituraModbusCoil("UHLM Óleo Nível Mínimo", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHLM_NivelminOleo"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_UHLM_NivelminOleo, CONDIC_INDISPONIBILIZAR))

        self.l_ED_UHLM_NivelCritOleo = LeituraModbusCoil("UHLM Óleo Nível Crítico", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHLM_NivelCritOleo"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_UHLM_NivelCritOleo, CONDIC_INDISPONIBILIZAR))

        self.l_ED_UHLM_FluxoMcDianteiro = LeituraModbusCoil("UHLM Fluxo Dianteiro", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHLM_FluxoMcDiant"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_UHLM_FluxoMcDianteiro, CONDIC_INDISPONIBILIZAR))

        self.l_ED_UHLM_Filt1PresSujo100Sujo = LeituraModbusCoil("UHLM Filtro 1 Pressão 100% Sujo", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHLMFilt1PresSujoSujo"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_UHLM_Filt1PresSujo100Sujo, CONDIC_INDISPONIBILIZAR))

        self.l_ED_UHLM_Filt2PresSujo100Sujo = LeituraModbusCoil("UHLM Filtro 2 Pressão 100% Sujo", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHLMFilt2PresSujoSujo"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_UHLM_Filt2PresSujo100Sujo, CONDIC_INDISPONIBILIZAR))

        # Controle Freios
        self.l_ED_FreioSemEnergia = LeituraModbusCoil("Freio Sem Energia", self.__clp, REG[f"UG{self.__ug.id}"]["ED_FreioSemEnergia"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_FreioSemEnergia, CONDIC_INDISPONIBILIZAR))

        self.l_ED_FreioFiltroSaturado = LeituraModbusCoil("Freio Filtro Saturado", self.__clp, REG[f"UG{self.__ug.id}"]["ED_FreioFiltroSaturado"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_FreioFiltroSaturado, CONDIC_INDISPONIBILIZAR))

        # Controle Filtros
        self.l_ED_FiltroRetSujo100Sujo = LeituraModbusCoil("UHRV Filtro Retorno 100% Sujo", self.__clp, REG[f"UG{self.__ug.id}"]["ED_FiltroRetSujoSujo"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_FiltroRetSujo100Sujo, CONDIC_INDISPONIBILIZAR))

        self.l_ED_FiltroPresSujo100Sujo = LeituraModbusCoil("UHRV Filtro Pressão 100% Sujo", self.__clp, REG[f"UG{self.__ug.id}"]["ED_FiltroPresSujoSujo"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_FiltroPresSujo100Sujo, CONDIC_INDISPONIBILIZAR))

        self.l_ED_FiltroPressaoBbaMecSj100 = LeituraModbusCoil("UHRV Bomba Filtro Pressão 100% Sujo", self.__clp, REG[f"UG{self.__ug.id}"]["ED_Filt1PresBbaMecSjSujo"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_FiltroPressaoBbaMecSj100, CONDIC_INDISPONIBILIZAR))

        # Outros
        self.l_ED_PalhetasDesal = LeituraModbusCoil("Pás Desalinhadas", self.__clp, REG[f"UG{self.__ug.id}"]["ED_PalhetasDesal"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_PalhetasDesal, CONDIC_INDISPONIBILIZAR))

        self.l_ED_ValvBorbTravada = LeituraModbusCoil("Válvula Borboleta Travada", self.__clp, REG[f"UG{self.__ug.id}"]["ED_ValvBorbTravadaFechada"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_ValvBorbTravada, CONDIC_INDISPONIBILIZAR))

        self.l_ED_SobreVeloMecPos18 = LeituraModbusCoil("Sobre Velocidade Posição 18", self.__clp, REG[f"UG{self.__ug.id}"]["ED_SobreVeloMecPos18"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_SobreVeloMecPos18, CONDIC_INDISPONIBILIZAR))

        self.l_ED_NivelMAltoPocoDren = LeituraModbusCoil("Poço Drenagem Nível Alto", self.__clp, REG[f"UG{self.__ug.id}"]["ED_NivelMAltoPocoDren"])
        self.condicionadores.append(CondicionadorBase(self.l_ED_NivelMAltoPocoDren, CONDIC_INDISPONIBILIZAR))


        ## Retornos Digitais
        # TRIPS
        self.l_RD_TripVibr1 = LeituraModbusCoil("Vibração 1 Trip", self.__clp, REG[f"UG{self.__ug.id}"]["RD_TripVibr1"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_TripVibr1, CONDIC_INDISPONIBILIZAR))

        self.l_RD_TripVibr2 = LeituraModbusCoil("Vibração 2 Trip", self.__clp, REG[f"UG{self.__ug.id}"]["RD_TripVibr2"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_TripVibr2, CONDIC_INDISPONIBILIZAR))

        self.l_RD_TripTempUHRV = LeituraModbusCoil("UHRV Trip Temperatura", self.__clp, REG[f"UG{self.__ug.id}"]["RD_TripTempUHRV"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_TripTempUHRV, CONDIC_INDISPONIBILIZAR))

        self.l_RD_TripTempUHLM = LeituraModbusCoil("UHLM Trip Temperatura", self.__clp, REG[f"UG{self.__ug.id}"]["RD_TripTempUHLM"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_TripTempUHLM, CONDIC_INDISPONIBILIZAR))

        self.l_RD_TripTempGaxeteiro = LeituraModbusCoil("Gaxeteiro Trip Temperatura", self.__clp, REG[f"UG{self.__ug.id}"]["RD_TripTempGaxeteiro"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_TripTempGaxeteiro, CONDIC_INDISPONIBILIZAR))

        self.l_RD_TripTempMcGuiaRadial = LeituraModbusCoil("Mancal Guia Radial Trip Temperatura", self.__clp, REG[f"UG{self.__ug.id}"]["RD_TripTempMcGuiaRadial"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_TripTempMcGuiaRadial, CONDIC_INDISPONIBILIZAR))

        self.l_RD_TripTempMcGuiaEscora = LeituraModbusCoil("Mancal Guia Escora Trip Temperatura", self.__clp, REG[f"UG{self.__ug.id}"]["RD_TripTempMcGuiaEscora"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_TripTempMcGuiaEscora, CONDIC_INDISPONIBILIZAR))

        self.l_RD_TripTempMcGuiaContraEscora = LeituraModbusCoil("Mancal Guia Contra Escora Trip Temperatura", self.__clp, REG[f"UG{self.__ug.id}"]["RD_TripTempMcGuiaContraEscora"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_TripTempMcGuiaContraEscora, CONDIC_INDISPONIBILIZAR))

        # Retornos Digitais - FALHAS
        self.l_RD_CLP_Falha = LeituraModbusCoil("CLP Falha", self.__clp, REG[f"UG{self.__ug.id}"]["RD_FalhaComuCLP"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_CLP_Falha, CONDIC_INDISPONIBILIZAR))

        self.l_RD_Q_Negativa = LeituraModbusCoil("Q Negativa", self.__clp, REG[f"UG{self.__ug.id}"]["RD_IHM_Q_Negativa"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_Q_Negativa, CONDIC_INDISPONIBILIZAR))

        self.l_RD_Remota_Falha = LeituraModbusCoil("Falha Remota", self.__clp, REG[f"UG{self.__ug.id}"]["RD_FalhaComuRemota"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_Remota_Falha, CONDIC_INDISPONIBILIZAR))

        self.l_RD_FalhaIbntDisjGer = LeituraModbusCoil("Dijuntor Gerador Falha", self.__clp, REG[f"UG{self.__ug.id}"]["RD_FalhaIbntDisjGer"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_FalhaIbntDisjGer, CONDIC_INDISPONIBILIZAR))

        self.l_RD_UHRV_FalhaAcionBbaM1 = LeituraModbusCoil("UHRV Bomba 1 Falha Acionamento", self.__clp, REG[f"UG{self.__ug.id}"]["RD_UHRV_FalhaAcionBbaM1"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_UHRV_FalhaAcionBbaM1, CONDIC_INDISPONIBILIZAR))

        self.l_RD_UHRV_FalhaAcionBbaM2 = LeituraModbusCoil("UHRV Bomba 2 Falha Acionamento", self.__clp, REG[f"UG{self.__ug.id}"]["RD_UHRV_FalhaAcionBbaM2"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_UHRV_FalhaAcionBbaM2, CONDIC_INDISPONIBILIZAR))

        self.l_RD_UHLM_FalhaAcionBbaM1 = LeituraModbusCoil("UHLM Bomba 1 Falha Acionamento", self.__clp, REG[f"UG{self.__ug.id}"]["RD_UHLM_FalhaAcionBbaM1"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_UHLM_FalhaAcionBbaM1, CONDIC_INDISPONIBILIZAR))

        self.l_RD_UHLM_FalhaAcionBbaM2 = LeituraModbusCoil("UHLM Bomba 2 Falha Acionamento", self.__clp, REG[f"UG{self.__ug.id}"]["RD_UHLM_FalhaAcionBbaM2"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_UHLM_FalhaAcionBbaM2, CONDIC_INDISPONIBILIZAR))

        self.l_RD_FalhaAcionFechaValvBorb = LeituraModbusCoil("Válvula Borboleta Falha Acionar Fechamento", self.__clp, REG[f"UG{self.__ug.id}"]["RD_FalhaAcionFechaValvBorb"])
        self.condicionadores.append(CondicionadorBase(self.l_RD_FalhaAcionFechaValvBorb, CONDIC_INDISPONIBILIZAR))


        # Leituras de condicionadores com limites de operção checados a cada ciclo
        self.lv_ED_TripPartRes = LeituraModbusCoil("Trip Part Res", self.__clp, REG[f"UG{self.__ug.id}"]["ED_TripPartRes"])
        self.lv_ED_FreioCmdRemoto = LeituraModbusCoil("Freio Modo Remoto", self.__clp, REG[f"UG{self.__ug.id}"]["ED_FreioCmdRemoto"])
        self.lv_ED_FreioPastilhaGasta = LeituraModbusCoil("Pastilha Freio Gasta", self.__clp, REG[f"UG{self.__ug.id}"]["ED_FreioPastilhaGasta"])
        self.lv_ED_QCAUG_Remoto = LeituraModbusCoil("Compressor Modo Remoto", self.__clp, REG[f"UG{self.__ug.id}"][f"ED_QCAUG{self.__ug.id}_Remoto"])
        self.lv_ED_FiltroPresSujo75Troc = LeituraModbusCoil("UHRV Filtro Pressão 75% Sujo", self.__clp, REG[f"UG{self.__ug.id}"]["ED_FiltroPresSujo75Troc"])
        self.lv_ED_FiltroRetSujo75Troc = LeituraModbusCoil("UHRV Filtro Pressão Retorno 75% Sujo", self.__clp, REG[f"UG{self.__ug.id}"]["ED_FiltroRetSujo75Troc"])
        self.lv_ED_UHLMFilt1PresSujo75Troc = LeituraModbusCoil("UHLM Filtro Pressão 1 75% Sujo", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHLMFilt1PresSujo75Troc"])
        self.lv_ED_UHLMFilt2PresSujo75Troc = LeituraModbusCoil("UHLM Filtro Pressão 2 75% Sujo", self.__clp, REG[f"UG{self.__ug.id}"]["ED_UHLMFilt2PresSujo75Troc"])
        self.lv_ED_FiltroPressaoBbaMecSj75 = LeituraModbusCoil("Filtro Pressão Bomba Mecância 75% Sujo", self.__clp, REG[f"UG{self.__ug.id}"]["ED_Filt1PresBbaMecSj75Troc"])
