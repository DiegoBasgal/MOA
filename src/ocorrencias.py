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


        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.condicionadores_ativos: "list[CondicionadorBase]" = []


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

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condicionadores_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if self.condicionadores_ativos == []:
                logger.warning(f"[OCO-USN] Foram detectados condicionadores ativos na Usina!")
            else:
                logger.info(f"[OCO-USN] Ainda há condicionadores ativos na Usina!")

            for condic in condicionadores_ativos:
                if condic in self.condicionadores_ativos:
                    logger.debug(f"[OCO-USN] Descrição: \"{condic.descr}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    flag = condic.gravidade
                    continue

                elif condic.gravidade == CONDIC_NORMALIZAR:
                    logger.warning(f"[OCO-USN] Descrição: \"{condic.descr}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    flag = CONDIC_NORMALIZAR
                    self.__db.update_alarmes([datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descr])

                elif condic.gravidade == CONDIC_INDISPONIBILIZAR:
                    logger.warning(f"[OCO-USN] Descrição: \"{condic.descr}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    flag = CONDIC_INDISPONIBILIZAR
                    self.__db.update_alarmes([datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descr])

            logger.debug("")
            return flag

        else:
            self.condicionadores_ativos = []
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
        self.leitura_ED_SA_GMG_Trip = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_GMG_Trip"], descr="[USN] Grupo Motor Gerador Trip")
        self.leitura_ED_SA_GMG_Alarme = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_GMG_Alarme"], descr="[USN] Grupo Motor Gerador Alarme")
        self.leitura_ED_SA_GMG_Operacao = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_GMG_Operacao"], descr="[USN] Grupo Motor Gerador Operação")
        self.leitura_RD_FalhaComunSETDA = LeituraModbusCoil(self.__clp["SA"], REG["SA_RD_FalhaComunSETDA"], descr="[USN] CLP TDA Falha")
        self.leitura_ED_SA_GMG_BaixoComb = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_GMG_BaixoComb"], descr="[USN] ED_SA_GMG_BaixoComb")
        self.leitura_RD_SA_GMG_FalhaAcion = LeituraModbusCoil(self.__clp["SA"], REG["SA_RD_GMG_FalhaAcion"], descr="[USN] Grupo Motor Gerador Falha Acionamento")
        self.leitura_ED_SA_QLCF_Disj52ETrip = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QLCF_Disj52ETrip"], descr="[USN] Disjuntor 52E Trip")
        self.leitura_RD_BbaDren1_FalhaAcion = LeituraModbusCoil(self.__clp["SA"], REG["SA_RD_BbaDren1_FalhaAcion"], descr="[USN] Bomba Drenagem 1 Falha Acionamento")
        self.leitura_RD_BbaDren2_FalhaAcion = LeituraModbusCoil(self.__clp["SA"], REG["SA_RD_BbaDren2_FalhaAcion"], descr="[USN] Bomba Drenagem 2 Falha Acionamento")
        self.leitura_RD_BbaDren3_FalhaAcion = LeituraModbusCoil(self.__clp["SA"], REG["SA_RD_BbaDren3_FalhaAcion"], descr="[USN] Bomba Drenagem 3 Falha Acionamento")
        self.leitura_ED_SA_QLCF_TripDisjAgrup = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QLCF_TripDisjAgrup"], descr="[USN] Disjuntor Agrupamento Trip")
        self.leitura_ED_SA_QCAP_Disj52EFechado = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCAP_Disj52EFechado"], descr="[USN] Disjuntor 52E Fechado")
        self.leitura_ED_SA_QCADE_BombasDng_Auto = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCADE_BombasDng_Auto"], descr="[USN] Bombas Drenagem Automático")
        self.leitura_ED_SA_QCAP_SubtensaoBarraGeral = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCAP_SubtensaoBarraGeral"], descr="[USN] Subtensão Barramento Geral")

        ### CONDICIONADORES ESSENCIAIS
        # self.leitura_ED_SA_QCAP_TensaoPresenteTSA = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCAP_TensaoPresenteTSA"], descr="[SA] TSA Tensão Presente")
        # self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_QCAP_TensaoPresenteTSA, CONDIC_NORMALIZAR))

        self.leitura_ED_SA_SEL787_Trip = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_SEL787_Trip"], descr="[SA] SEL 787 Trip")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_SEL787_Trip, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_SEL311_Trip = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_SEL311_Trip"], descr="[SA] SEL 311 Trip")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_SEL311_Trip, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_MRU3_Trip = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_MRU3_Trip"], descr="[SA] MRU3 Trip")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_MRU3_Trip, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_MRL1_Trip = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_MRL1_Trip"], descr="[SA] MRL1 Trip")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_MRL1_Trip, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_QCADE_Disj52E1Trip = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCADE_Disj52E1Trip"], descr="[SA] Dijuntor 52E1 Trip")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Disj52E1Trip, CONDIC_INDISPONIBILIZAR))

        ### CONDICIONADORES NORMAIS
        if not d.glb["TDA_Offline"]:
            self.leitura_ED_TDA_QcataDisj52ETrip = LeituraModbusCoil(self.__clp["TDA"], REG["TDA_ED_QcataDisj52ETrip"], descr="[TDA] Disjuntor 52E Trip")
            self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52ETrip, CONDIC_INDISPONIBILIZAR))

            self.leitura_ED_TDA_QcataDisj52ETripDisjSai = LeituraModbusCoil(self.__clp["TDA"], REG["TDA_ED_QcataDisj52ETripDisjSai"], descr="[TDA] Disjuntor 52E Saída Trip")
            self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52ETripDisjSai, CONDIC_INDISPONIBILIZAR))

            # self.leitura_ED_TDA_QcataDisj52EFalha380VCA = LeituraModbusCoil(self.__clp["TDA"], REG["TDA_ED_QcataDisj52EFalha380VCA"], descr="[TDA] Disjuntor 52E Falha 380 VCA")
            # self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52EFalha380VCA, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_MRU3_Falha = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_MRU3_Falha"], descr="[SA] MRU3 Falha")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_MRU3_Falha, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_SEL787_FalhaInterna = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_SEL787_FalhaInterna"], descr="[SA] SEL 787 Falha")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_SEL787_FalhaInterna, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_SEL311_Falha = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_SEL311_Falha"], descr="[SA] SEL 311 Falha")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_SEL311_Falha, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_CTE_Falta125Vcc = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_CTE_Falta125Vcc"], descr="[SA] CTE Falta 125 Vcc")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CTE_Falta125Vcc, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_CTE_Secc89TE_Aberta = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_CTE_Secc89TE_Aberta"], descr="[SA] CTE Seccionadora 89TE Aberta")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CTE_Secc89TE_Aberta, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_TE_AlarmeDetectorGas = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_TE_AlarmeDetectorGas"], descr="[SA] Detector de Gás Alarme")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeDetectorGas, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_TE_AlarmeNivelMaxOleo = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_TE_AlarmeNivelMaxOleo"], descr="[SA] Transformador Elevador Alarme Nível Máximo Óleo")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeNivelMaxOleo, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_TE_AlarmeAlivioPressao = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_TE_AlarmeAlivioPressao"], descr="[SA] Transformador Elevador Alarme Alívio Pressão")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeAlivioPressao, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_TE_AlarmeTempOleo = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_TE_AlarmeTempOleo"], descr="[SA] Transformador Elevador Alarme Temperatura Óleo")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeTempOleo, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_TE_AlarmeTempEnrolamento = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_TE_AlarmeTempEnrolamento"], descr="[SA] Transformador Elevador Alarme Temperatura Enrolamento")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeTempEnrolamento, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_TE_AlarmeDesligamento = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_TE_AlarmeDesligamento"], descr="[SA] Transformador Elevador Alarme Desligamento")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeDesligamento, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_TE_Falha = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_TE_Falha"], descr="[SA] Transformador Elevador Falha")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_Falha, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_FalhaDisjTPsProt = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_FalhaDisjTPsProt"], descr="[SA] Disjuntor Transformador Potencial Falha")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_FalhaDisjTPsProt, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_FalhaDisjTPsSincr = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_FalhaDisjTPsSincr"], descr="[SA] Disjuntor Transformador Potencial Falha Sincronização")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_FalhaDisjTPsSincr, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_CSA1_Secc_Aberta = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_CSA1_Secc_Aberta"], descr="[SA] CSA1 Seccionadora Aberta")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_Secc_Aberta, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_CSA1_FusivelQueimado = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_CSA1_FusivelQueimado"], descr="[SA] CSA1 Fusível Queimado")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_FusivelQueimado, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_CSA1_FaltaTensao125Vcc = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_CSA1_FaltaTensao125Vcc"], descr="[SA] CSA1 Falta Tensão 125 Vcc")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_FaltaTensao125Vcc, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_QCADE_Nivel4 = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCADE_Nivel4"], descr="[SA] CA Drenagem Nível 4")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Nivel4, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_QCADE_NivelMuitoAlto = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCADE_NivelMuitoAlto"], descr="[SA] CA Drenagem Nível Muito Alto")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_NivelMuitoAlto, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_QCADE_Falha220VCA = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCADE_Falha220VCA"], descr="[SA] CA Drenagem Falha 220 VCA")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Falha220VCA, CONDIC_INDISPONIBILIZAR))

        # Verificar
        self.leitura_ED_SA_QCCP_Disj72ETrip = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCCP_Disj72ETrip"], descr="[SA] QCCP Disjuntor 72E Trip")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_Disj72ETrip, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_QCCP_Falta125Vcc = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCCP_Falta125Vcc"], descr="[SA] QCCP Falta 125 Vcc")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_Falta125Vcc, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_QCCP_TripDisjAgrup = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCCP_TripDisjAgrup"], descr="[SA] QCCP Disjuntor Agrupamento Trip")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_TripDisjAgrup, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_QCAP_Falta125Vcc = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCAP_Falta125Vcc"], descr="[SA] CA Principal Falta 125 Vcc")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Falta125Vcc, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_QCAP_TripDisjAgrup = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCAP_TripDisjAgrup"], descr="[SA] CA Principal Disjuntor Agrupamento Trip")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_TripDisjAgrup, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_QCAP_Disj52A1Falha = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCAP_Disj52A1Falha"], descr="[SA] CA Principal Disjuntor 52A1 Falha")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Disj52A1Falha, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_QCAP_Disj52EFalha = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_QCAP_Disj52EFalha"], descr="[SA] CA Principal Disjuntor 52E Falha")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Disj52EFalha, CONDIC_INDISPONIBILIZAR))

        # self.leitura_ED_SA_GMG_DisjFechado = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_GMG_DisjFechado"], descr="[SA] Disjuntor Grupo Motor Gerador Fechado")
        # self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_GMG_DisjFechado, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_DJ1_FalhaInt = LeituraModbusCoil(self.__clp["SA"], REG["SA_RD_DJ1_FalhaInt"], descr="[SA] Disjuntor 1 Falha Interna")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_DJ1_FalhaInt, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_CLP_Falha = LeituraModbusCoil(self.__clp["SA"], REG["SA_RD_FalhaComuCLP"], descr="[SA] CLP SA Falha")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_CLP_Falha, CONDIC_INDISPONIBILIZAR))

        self.leitura_RA_SEL787_Targets = LeituraModbusCoil(self.__clp["SA"], REG["SA_RA_SEL787_Targets"], descr="[SA] SEL 787 Targets")
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets, CONDIC_INDISPONIBILIZAR))

        self.leitura_RA_SEL787_Targets_Links_Bit00 = LeituraModbusCoil(self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit00"], descr="[SA] SEL 787 Targets Bit 0")
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit00, CONDIC_INDISPONIBILIZAR))

        # self.leitura_RA_SEL787_Targets_Links_Bit01 = LeituraModbusCoil(self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit01"], descr="[SA] SEL 787 Targets Bit 1")
        # self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit01, CONDIC_INDISPONIBILIZAR))

        self.leitura_RA_SEL787_Targets_Links_Bit02 = LeituraModbusCoil(self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit02"], descr="[SA] SEL 787 Targets Bit 2")
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit02, CONDIC_INDISPONIBILIZAR))

        self.leitura_RA_SEL787_Targets_Links_Bit03 = LeituraModbusCoil(self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit03"], descr="[SA] SEL 787 Targets Bit 3")
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit03, CONDIC_INDISPONIBILIZAR))

        self.leitura_RA_SEL787_Targets_Links_Bit04 = LeituraModbusCoil(self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit04"], descr="[SA] SEL 787 Targets Bit 4")
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit04, CONDIC_INDISPONIBILIZAR))

        # self.leitura_RA_SEL787_Targets_Links_Bit05 = LeituraModbusCoil(self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit05"], descr="[SA] SEL 787 Targets Bit 5")
        # self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit05, CONDIC_INDISPONIBILIZAR))

        # self.leitura_RA_SEL787_Targets_Links_Bit06 = LeituraModbusCoil(self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit06"], descr="[SA] SEL 787 Targets Bit 6")
        # self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit06, CONDIC_INDISPONIBILIZAR))

        self.leitura_RA_SEL787_Targets_Links_Bit07 = LeituraModbusCoil(self.__clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit07"], descr="[SA] SEL 787 Targets Bit 7")
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit07, CONDIC_INDISPONIBILIZAR))

        return


class OcorrenciasUnidades:
    def __init__(self, ug, clp: "dict[str, ModbusClient]"=None, db: BancoDados=None):

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

        self.condicionadores_ativos: "list[CondicionadorBase]" = []


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

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condicionadores_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if self.condicionadores_ativos == []:
                logger.warning(f"[OCO-UG{self.__ug.id}] Foram detectados condicionadores ativos na Usina!")
            else:
                logger.info(f"[OCO-UG{self.__ug.id}] Ainda há condicionadores ativos na Usina!")

            for condic in condicionadores_ativos:
                if condic in self.condicionadores_ativos:
                    logger.debug(f"[OCO-UG{self.__ug.id}] Descrição: \"{condic.descr}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    flag = condic.gravidade
                    continue

                elif condic.gravidade == CONDIC_NORMALIZAR:
                    logger.warning(f"[OCO-UG{self.__ug.id}] Descrição: \"{condic.descr}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    flag = CONDIC_NORMALIZAR
                    self.__db.update_alarmes([datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descr])

                elif condic.gravidade == CONDIC_AGUARDAR:
                    logger.warning(f"[OCO-UG{self.__ug.id}] Descrição: \"{condic.descr}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    flag = CONDIC_NORMALIZAR
                    self.__db.update_alarmes([datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descr])

                elif condic.gravidade == CONDIC_INDISPONIBILIZAR:
                    logger.warning(f"[OCO-UG{self.__ug.id}] Descrição: \"{condic.descr}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    flag = CONDIC_INDISPONIBILIZAR
                    self.__db.update_alarmes([datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descr])

            logger.debug("")
            return flag

        else:
            self.condicionadores_ativos = []
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

        if ld[f"pressao_cx_espiral_ug{self.__ug.id}"].valor <= cd[f"pressao_cx_espiral_ug{self.__ug.id}"].valor_base and ld[f"pressao_cx_espiral_ug{self.__ug.id}"].valor != 0 and self.__ug.id == UG_SINCRONIZADA:
            logger.debug(f"[OCO-UG{self.__ug.id}] A pressão Caixa Espiral da UG passou do valor base! ({cd[f'pressao_cx_espiral_ug{self.__ug.id}'].valor_base:03.2f} KGf/m2) | Leitura: {ld[f'pressao_cx_espiral_ug{self.__ug.id}'].valor:03.2f}")

        if ld[f"pressao_cx_espiral_ug{self.__ug.id}"].valor <= cd[f"pressao_cx_espiral_ug{self.__ug.id}"].valor_limite and ld[f"pressao_cx_espiral_ug{self.__ug.id}"].valor != 0 and self.__ug.id == UG_SINCRONIZADA:
            logger.debug(f"[OCO-UG{self.__ug.id}] A pressão Caixa Espiral da UG está muito próxima do limite! ({cd[f'pressao_cx_espiral_ug{self.__ug.id}'].valor_limite:03.2f} KGf/m2) | Leitura: {ld[f'pressao_cx_espiral_ug{self.__ug.id}'].valor:03.2f} KGf/m2")


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
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_FreioPastilhaGasta"],
            descr=f"[UG{self.__ug.id}] Pastilha Freio Gasta"
        )
        self.leitura_voip["leitura_ED_FiltroPresSujo75Troc"] = LeituraModbusCoil(
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_FiltroPresSujo75Troc"],
            descr=f"[UG{self}] UHRV Filtro Pressão 75% Sujo"
        )
        self.leitura_voip["leitura_ED_FiltroRetSujo75Troc"] = LeituraModbusCoil(
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_FiltroRetSujo75Troc"],
            descr=f"[UG{self.__ug.id}] UHRV Filtro Pressão Retorno 75% Sujo"
        )
        self.leitura_voip["leitura_ED_UHLMFilt1PresSujo75Troc"] = LeituraModbusCoil(
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_UHLMFilt1PresSujo75Troc"],
            descr=f"[UG{self.__ug.id}] UHLM Filtro Pressão 1 75% Sujo"
        )
        self.leitura_voip["leitura_ED_UHLMFilt2PresSujo75Troc"] = LeituraModbusCoil(
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_UHLMFilt2PresSujo75Troc"],
            descr=f"[UG{self.__ug.id}] UHLM Filtro Pressão 2 75% Sujo"
        )
        self.leitura_voip["leitura_ED_FiltroPressaoBbaMecSj75"] = LeituraModbusCoil(
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_Filt1PresBbaMecSj75Troc"],
            descr=f"[UG{self.__ug.id}] Filtro Pressão Bomba Mecância 75% Sujo"
        )
        self.leitura_voip["leitura_ED_TripPartRes"] = LeituraModbusCoil(
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_TripPartRes"],
            descr=f"[UG{self.__ug.id}] Trip Part Res"
        )
        self.leitura_voip["leitura_ED_FreioCmdRemoto"] = LeituraModbusCoil(
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_FreioCmdRemoto"],
            descr=f"[UG{self.__ug.id}] Freio Modo Remoto"
        )
        self.leitura_voip[f"leitura_ED_QCAUG{self.__ug.id}_Remoto"] = LeituraModbusCoil(
            self.__clp[f"UG{self.__ug.id}"],
            REG[f"UG{self.__ug.id}_ED_QCAUG{self.__ug.id}_Remoto"],
            descr=f"[UG{self.__ug.id}] Compressor Modo Remoto"
        )

        ### CONDICIONADORES ESSENCIAIS
        # R
        self.leitura_dict[f"tmp_fase_r_ug{self.__ug.id}"] = LeituraModbus(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_01"], op=4, descr=f"[UG{self.__ug.id}] Temperatura Fase R")
        self.condic_dict[f"tmp_fase_r_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_fase_r_ug{self.__ug.id}"], CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_r_ug{self.__ug.id}"])

        # S
        self.leitura_dict[f"tmp_fase_s_ug{self.__ug.id}"] = LeituraModbus(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_02"], op=4, descr=f"[UG{self.__ug.id}] Temperatura Fase S")
        self.condic_dict[f"tmp_fase_s_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_fase_s_ug{self.__ug.id}"], CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_s_ug{self.__ug.id}"])

        # T
        self.leitura_dict[f"tmp_fase_t_ug{self.__ug.id}"] = LeituraModbus(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_03"], op=4, descr=f"[UG{self.__ug.id}] Temperatura Fase T")
        self.condic_dict[f"tmp_fase_t_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_fase_t_ug{self.__ug.id}"], CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_fase_t_ug{self.__ug.id}"])

        # Nucleo estator
        self.leitura_dict[f"tmp_nucleo_estator_ug{self.__ug.id}"] = LeituraModbus(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_04"], op=4, descr=f"[UG{self.__ug.id}] Temperatura Núcelo do Estator",)
        self.condic_dict[f"tmp_nucleo_estator_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_nucleo_estator_ug{self.__ug.id}"], CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_nucleo_estator_ug{self.__ug.id}"])

        # MRD 1
        self.leitura_dict[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"] = LeituraModbus(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_05"], op=4, descr=f"[UG{self.__ug.id}] Temperatura Mancal Radial Dianteiro")
        self.condic_dict[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"], CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_rad_dia_1_ug{self.__ug.id}"])

        # MRT 1
        self.leitura_dict[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"] = LeituraModbus(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_06"], op=4, descr=f"[UG{self.__ug.id}] Temperatura Mancal Radial Traseiro",)
        self.condic_dict[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"], CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_rad_tra_1_ug{self.__ug.id}"])

        # MRD 2
        self.leitura_dict[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"] = LeituraModbus(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_07"], op=4, descr=f"[UG{self.__ug.id}] Temperatura Mancal Radial Dianteiro 2")
        self.condic_dict[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"], CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_rad_dia_2_ug{self.__ug.id}"])

        # MRT 2
        self.leitura_dict[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"] = LeituraModbus(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_08"], op=4, descr=f"[UG{self.__ug.id}] Temperatura Mancal Radial Traseiro 2")
        self.condic_dict[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"], CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_rad_tra_2_ug{self.__ug.id}"])

        # Saída de ar
        self.leitura_dict[f"tmp_saida_de_ar_ug{self.__ug.id}"] = LeituraModbus(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_Temperatura_10"], op=4, descr=f"[UG{self.__ug.id}] Saída de Ar")
        self.condic_dict[f"tmp_saida_de_ar_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_saida_de_ar_ug{self.__ug.id}"], CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_saida_de_ar_ug{self.__ug.id}"])

        # Mancal Guia Radial
        self.leitura_dict[f"tmp_mancal_guia_radial_ug{self.__ug.id}"] = LeituraModbus(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_TempMcGuiaRadial"], descr=f"[UG{self.__ug.id}] Mancal Guia Radial",)
        self.condic_dict[f"tmp_mancal_guia_radial_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_mancal_guia_radial_ug{self.__ug.id}"], CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_guia_radial_ug{self.__ug.id}"])

        # Mancal Guia escora
        self.leitura_dict[f"tmp_mancal_guia_escora_ug{self.__ug.id}"] = LeituraModbus(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_TempMcGuiaEscora"], descr=f"[UG{self.__ug.id}] Mancal Guia Escora")
        self.condic_dict[f"tmp_mancal_guia_escora_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_mancal_guia_escora_ug{self.__ug.id}"], CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_guia_escora_ug{self.__ug.id}"])

        # Mancal Guia contra_escora
        self.leitura_dict[f"tmp_mancal_guia_contra_ug{self.__ug.id}"] = LeituraModbus(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RA_TempMcGuiaContraEscora"], descr=f"[UG{self.__ug.id}] Mancal Guia Contra Escora")
        self.condic_dict[f"tmp_mancal_guia_contra_ug{self.__ug.id}"] = CondicionadorExponencial(self.leitura_dict[f"tmp_mancal_guia_contra_ug{self.__ug.id}"], CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condic_dict[f"tmp_mancal_guia_contra_ug{self.__ug.id}"])

        self.leitura_dict[f"pressao_cx_espiral_ug{self.__ug.id}"] = LeituraModbus(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_EA_PressK1CaixaExpiral_MaisCasas"], escala=0.01, op=4, descr=f"[UG{self.__ug.id}] Caixa Espiral")
        self.condic_dict[f"pressao_cx_espiral_ug{self.__ug.id}"] = CondicionadorExponencialReverso(self.leitura_dict[f"pressao_cx_espiral_ug{self.__ug.id}"], CONDIC_INDISPONIBILIZAR, valor_base=16.5, valor_limite=14)


        # Óleo do Transformador Elevador
        self.leitura_temperatura_oleo_trafo = LeituraModbus(self.__clp["SA"], REG["SA_EA_TE_TempOleo"], escala=0.1, op=4, descr=f"[UG{self.__ug.id}] Óleo do Transformador Elevador")
        self.condicionador_leitura_temperatura_oleo_trafo = CondicionadorExponencial(self.leitura_temperatura_oleo_trafo, CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_leitura_temperatura_oleo_trafo)

        ## Comandos self. Digitais
        # GERAL
        self.leitura_CD_EmergenciaViaSuper = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_CD_EmergenciaViaSuper"], descr=f"[UG{self.__ug.id}] Emergência Via Supervisório")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_CD_EmergenciaViaSuper, CONDIC_NORMALIZAR))

        ## Retornos Digitais
        # TRIPS
        self.leitura_RD_TripEletrico = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripEletrico"], descr=f"[UG{self.__ug.id}] Trip Elétrico")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_RD_TripEletrico, CONDIC_NORMALIZAR, [UG_SINCRONIZADA], self.__ug.id))

        self.leitura_RD_700G_Trip = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_700G_Trip"], descr=f"[UG{self.__ug.id}] SEL 700G Trip")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_RD_700G_Trip, CONDIC_NORMALIZAR, [UG_SINCRONIZADA], self.__ug.id))

        self.leitura_RD_TripMecanico = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripMecanico"], descr=f"[UG{self.__ug.id}] Trip Mecâncio")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_RD_TripMecanico, CONDIC_INDISPONIBILIZAR))

        ## Entradas Digitais
        # TRIPS
        self.leitura_ED_RV_Trip = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_RV_Trip"], descr=f"[UG{self.__ug.id}] RV Trip")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_RV_Trip, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_AVR_Trip = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_AVR_Trip"], descr=f"[UG{self.__ug.id}] AVR Trip")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_AVR_Trip, CONDIC_INDISPONIBILIZAR))

        # RELÉS
        self.leitura_ED_SEL700G_Atuado = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_SEL700G_Atuado"], descr=f"[UG{self.__ug.id}] SEL 700G Atuado")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SEL700G_Atuado, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_ReleBloqA86MAtuado = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_ReleBloqA86MAtuado"], descr=f"[UG{self.__ug.id}] Bloqueio 86M Atuado")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_ReleBloqA86MAtuado, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_ReleBloqA86HAtuado = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_ReleBloqA86HAtuado"], descr=f"[UG{self.__ug.id}] Bloqueio 86H Atuado")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_ReleBloqA86HAtuado, CONDIC_NORMALIZAR, [UG_SINCRONIZADA], self.__ug.id))


        ### CONDICIONADORES NORMAIS
        # Entradas Digitais
        # SA -> UG
        self.leitura_ED_SA_FalhaDisjTPsSincrG2 = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_FalhaDisjTPsSincrG2"], descr=f"[SA-UG{self.__ug.id}] Trasformador Potencial Disjuntor Sincronização Falha")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_FalhaDisjTPsSincrG2, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_DisjDJ1_AlPressBaixa = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_DisjDJ1_AlPressBaixa"], descr=f"[SA-UG{self.__ug.id}] Disjutor 1 Alarme Pressão Baixa")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_DisjDJ1_AlPressBaixa, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SA_DisjDJ1_BloqPressBaixa = LeituraModbusCoil(self.__clp["SA"], REG["SA_ED_DisjDJ1_BloqPressBaixa"], descr=f"[SA-UG{self.__ug.id}] Disjuntor 1 Bloqueio Pressão Baixa")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_DisjDJ1_BloqPressBaixa, CONDIC_INDISPONIBILIZAR))

        # TRIPS
        self.leitura_ED_UHRV_TripBomba1 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHRV_TripBomba1"], descr=f"[UG{self.__ug.id}] UHRV Bomba 1 Trip")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_TripBomba1, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_UHRV_TripBomba2 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHRV_TripBomba2"], descr=f"[UG{self.__ug.id}] UHRV Bomba 2 Trip")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_TripBomba2, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_UHLM_TripBomba1 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_TripBomba1"], descr=f"[UG{self.__ug.id}] UHLM Bomba 1 Trip")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_TripBomba1, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_UHLM_TripBomba2 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_TripBomba2"], descr=f"[UG{self.__ug.id}] UHLM Bomba 2 Trip")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_TripBomba2, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_QCAUG_TripDisj52A1 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_QCAUG_TripDisj52A1"], descr=f"[UG{self.__ug.id}] QCAUG Disjuntor 52A1 Trip")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_QCAUG_TripDisj52A1, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_TripAlimPainelFreio = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_TripAlimPainelFreio"], descr=f"[UG{self.__ug.id}] Alimentação Painel Freio Trip")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_TripAlimPainelFreio, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_QCAUG_TripDisjAgrup = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_QCAUG_TripDisjAgrup"], descr=f"[UG{self.__ug.id}] QCAUG Disjuntor Agrupamento Trip")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_QCAUG_TripDisjAgrup, CONDIC_INDISPONIBILIZAR))

        # FALHAS
        self.leitura_ED_AVR_FalhaInterna = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_AVR_FalhaInterna"], descr=f"[UG{self.__ug.id}] AVR Falha Interna")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_AVR_FalhaInterna, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SEL700G_FalhaInterna = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_SEL700G_FalhaInterna"], descr=f"[UG{self.__ug.id}] SEL 700G Falha Interna")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SEL700G_FalhaInterna, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_QCAUG_Falha380VcaPainel = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_QCAUG_Falha380VcaPainel"], descr=f"[UG{self.__ug.id}] QCAUG Falha 380 VCA Painel")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_QCAUG_Falha380VcaPainel, CONDIC_NORMALIZAR))

        # FALTAS
        self.leitura_ED_Falta125Vcc = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_Falta125Vcc"], descr=f"[UG{self.__ug.id}] Falta 125 Vcc")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_Falta125Vcc, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_Falta125VccCom = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_Falta125VccCom"], descr=f"[UG{self.__ug.id}] Falta 125 Vcc Com")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_Falta125VccCom, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_FaltaFluxoOleoMc = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_FaltaFluxoOleoMc"], descr=f"[UG{self.__ug.id}] Falta Fluxo Óleo MC")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FaltaFluxoOleoMc, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_Falta125VccAlimVal = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_Falta125VccAlimVal"], descr=f"[UG{self.__ug.id}] Falta 125 Vcc Alimentação")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_Falta125VccAlimVal, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_UHLM_FaltaFluxTroc = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_FaltaFluxTroc"], descr=f"[UG{self.__ug.id}] UHLM Falta Fluxo")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FaltaFluxTroc, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_UHLM_FaltaPressTroc = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_FaltaPressTroc"], descr=f"[UG{self.__ug.id}] UHLM Falta Pressão") # TODO retornar para DEVE_INDISPONIBILZIA, descr=R
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FaltaPressTroc, CONDIC_NORMALIZAR))

        # Controle UHRV
        self.leitura_ED_UHRV_NivOleominimoPos36 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHRV_NivOleominimoPos36"], descr=f"[UG{self.__ug.id}] UHRV Óleo Nível Mínimo Posição 36")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_NivOleominimoPos36, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_UHRV_NivOleoCriticoPos35 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHRV_NivOleoCriticoPos35"], descr=f"[UG{self.__ug.id}] UHRV Óleo Nível Crítico Posição 35")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_NivOleoCriticoPos35, CONDIC_INDISPONIBILIZAR))

        # Controle UHLM
        self.leitura_ED_UHLM_FluxoMcTras = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_FluxoMcTras"], descr=f"[UG{self.__ug.id}] UHLM Fluxo Traseiro MC")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FluxoMcTras, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_UHLM_NivelminOleo = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_NivelminOleo"], descr=f"[UG{self.__ug.id}] UHLM Óleo Nível Mínimo")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_NivelminOleo, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_UHLM_NivelCritOleo = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_NivelCritOleo"], descr=f"[UG{self.__ug.id}] UHLM Óleo Nível Crítico")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_NivelCritOleo, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_UHLM_FluxoMcDianteiro = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLM_FluxoMcDiant"], descr=f"[UG{self.__ug.id}] UHLM Fluxo Dianteiro")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FluxoMcDianteiro, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_UHLM_Filt1PresSujo100Sujo = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLMFilt1PresSujoSujo"], descr=f"[UG{self.__ug.id}] UHLM Filtro 1 Pressão 100% Sujo")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_Filt1PresSujo100Sujo, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_UHLM_Filt2PresSujo100Sujo = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_UHLMFilt2PresSujoSujo"], descr=f"[UG{self.__ug.id}] UHLM Filtro 2 Pressão 100% Sujo")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_Filt2PresSujo100Sujo, CONDIC_INDISPONIBILIZAR))

        # Controle Freios
        self.leitura_ED_FreioSemEnergia = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_FreioSemEnergia"], descr=f"[UG{self.__ug.id}] Freio Sem Energia")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FreioSemEnergia, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_FreioFiltroSaturado = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_FreioFiltroSaturado"], descr=f"[UG{self.__ug.id}] Freio Filtro Saturado")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FreioFiltroSaturado, CONDIC_INDISPONIBILIZAR))

        # Controle Filtros
        self.leitura_ED_FiltroRetSujo100Sujo = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_FiltroRetSujoSujo"], descr=f"[UG{self.__ug.id}] UHRV Filtro Retorno 100% Sujo")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FiltroRetSujo100Sujo, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_FiltroPresSujo100Sujo = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_FiltroPresSujoSujo"], descr=f"[UG{self.__ug.id}] UHRV Filtro Pressão 100% Sujo")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FiltroPresSujo100Sujo, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_FiltroPressaoBbaMecSj100 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_Filt1PresBbaMecSjSujo"], descr=f"[UG{self.__ug.id}] UHRV Bomba Filtro Pressão 100% Sujo")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FiltroPressaoBbaMecSj100, CONDIC_INDISPONIBILIZAR))

        # Outros
        self.leitura_ED_PalhetasDesal = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_PalhetasDesal"], descr=f"[UG{self.__ug.id}] Pás Desalinhadas")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_PalhetasDesal, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_ValvBorbTravada = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_ValvBorbTravadaFechada"], descr=f"[UG{self.__ug.id}] Válvula Borboleta Travada")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_ValvBorbTravada, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_SobreVeloMecPos18 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_SobreVeloMecPos18"], descr=f"[UG{self.__ug.id}] Sobre Velocidade Posição 18")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SobreVeloMecPos18, CONDIC_INDISPONIBILIZAR))

        self.leitura_ED_NivelMAltoPocoDren = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_ED_NivelMAltoPocoDren"], descr=f"[UG{self.__ug.id}] Poço Drenagem Nível Alto")
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_NivelMAltoPocoDren, CONDIC_INDISPONIBILIZAR))


        ## Retornos Digitais
        # TRIPS
        self.leitura_RD_TripVibr1 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripVibr1"], descr=f"[UG{self.__ug.id}] Vibração 1 Trip")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripVibr1, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_TripVibr2 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripVibr2"], descr=f"[UG{self.__ug.id}] Vibração 2 Trip")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripVibr2, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_TripTempUHRV = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripTempUHRV"], descr=f"[UG{self.__ug.id}] UHRV Trip Temperatura")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempUHRV, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_TripTempUHLM = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripTempUHLM"], descr=f"[UG{self.__ug.id}] UHLM Trip Temperatura")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempUHLM, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_TripTempGaxeteiro = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripTempGaxeteiro"], descr=f"[UG{self.__ug.id}] Gaxeteiro Trip Temperatura")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempGaxeteiro, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_TripTempMcGuiaRadial = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripTempMcGuiaRadial"], descr=f"[UG{self.__ug.id}] Mancal Guia Radial Trip Temperatura")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempMcGuiaRadial, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_TripTempMcGuiaEscora = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripTempMcGuiaEscora"], descr=f"[UG{self.__ug.id}] Mancal Guia Escora Trip Temperatura")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempMcGuiaEscora, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_TripTempMcGuiaContraEscora = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_TripTempMcGuiaContraEscora"], descr=f"[UG{self.__ug.id}] Mancal Guia Contra Escora Trip Temperatura")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempMcGuiaContraEscora, CONDIC_INDISPONIBILIZAR))

        # Retornos Digitais - FALHAS
        self.leitura_RD_CLP_Falha = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_FalhaComuCLP"], descr=f"[UG{self.__ug.id}] CLP Falha")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_CLP_Falha, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_Q_Negativa = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_IHM_Q_Negativa"], descr=f"[UG{self.__ug.id}] Q Negativa")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_Q_Negativa, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_Remota_Falha = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_FalhaComuRemota"], descr=f"[UG{self.__ug.id}] Falha Remota")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_Remota_Falha, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_FalhaIbntDisjGer = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_FalhaIbntDisjGer"], descr=f"[UG{self.__ug.id}] Dijuntor Gerador Falha")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_FalhaIbntDisjGer, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_UHRV_FalhaAcionBbaM1 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_UHRV_FalhaAcionBbaM1"], descr=f"[UG{self.__ug.id}] UHRV Bomba 1 Falha Acionamento")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHRV_FalhaAcionBbaM1, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_UHRV_FalhaAcionBbaM2 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_UHRV_FalhaAcionBbaM2"], descr=f"[UG{self.__ug.id}] UHRV Bomba 2 Falha Acionamento")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHRV_FalhaAcionBbaM2, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_UHLM_FalhaAcionBbaM1 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_UHLM_FalhaAcionBbaM1"], descr=f"[UG{self.__ug.id}] UHLM Bomba 1 Falha Acionamento")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHLM_FalhaAcionBbaM1, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_UHLM_FalhaAcionBbaM2 = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_UHLM_FalhaAcionBbaM2"], descr=f"[UG{self.__ug.id}] UHLM Bomba 2 Falha Acionamento")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHLM_FalhaAcionBbaM2, CONDIC_INDISPONIBILIZAR))

        self.leitura_RD_FalhaAcionFechaValvBorb = LeituraModbusCoil(self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_RD_FalhaAcionFechaValvBorb"], descr=f"[UG{self.__ug.id}] Válvula Borboleta Falha Acionamento Fechamento")
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_FalhaAcionFechaValvBorb, CONDIC_INDISPONIBILIZAR))
