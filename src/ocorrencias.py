import logging
import traceback

from time import sleep, time

from leituras import *
from mensageiro import voip
from condicionadores import *
from dicionarios.reg import *
from dicionarios.const import *

from clients import ClpClients
from unidade_geracao import UnidadeDeGeracao

logger = logging.getLogger("__main__")

class Ocorrencias:
    def __init__(self, sd=None, clp: ClpClients=None, ugs: list([UnidadeDeGeracao])=None):

        if not sd:
            logger.warning("[OCO] Houve um erro ao carregar arquivos de configuração (\"shared_dict\").")
            raise ValueError
        else:
            self.dict = sd

        if not clp:
            logger.warning("[OCO-USN] Não foi possível carregar classes de conexão com clps | campo | banco de dados.")
            raise ConnectionError
        else:
            self.clp_usn = clp.clp_dict[1]
            self.clp_tda = clp.clp_dict[2]
            self.clp_ug = {
                "ug1": clp.clp_dict[3],
                "ug2": clp.clp_dict[4]
            }

        if not ugs:
            logger.error("[OCO] A lista de ugs é necessária para realizar a leitura de ocorrências.")
            raise ValueError
        else:
            self._ugs = ugs
            self._ug1 = ugs[0]
            self._ug2 = ugs[1]

        # Variáveis Públicas
        self.voip_ug = None
        self.voip_usn = None

        self.voip_dict = voip.vars_dict

    # Property/Setter Protegidos
    @property
    def ugs(self) -> list([UnidadeDeGeracao]):
        return self._ugs

    @ugs.setter
    def ugs(self, var: list([UnidadeDeGeracao])) -> None:
        self._ugs = var

    def leitura_periodica(self, delay) -> None:
        logger.debug("[OCO] Iniciando o timer de leitura por hora.")
        try:
            proxima_leitura = time() + delay
            while True:
                if OcorrenciasUsn.leitura_temporizada() or (OcorrenciasUg.leitura_temporizada(ug) for ug in self.ugs):
                    self.acionar_voip()
                sleep(max(0, proxima_leitura - time()))
                proxima_leitura += (time() - proxima_leitura) // delay * delay + delay

        except Exception as e:
            logger.exception(f"[OCO] Houve um problema ao executar a leitura por hora. Exception: \"{repr(e)}\"")
            logger.exception(f"[OCO] Traceback: {traceback.print_stack}")

    def acionar_voip(self) -> None:
        try:
            if self.voip_usn or self.voip_ug:
                for i, j in zip(self.dict["VOIP"], self.voip_dict):
                    if i == j and self.dict["VOIP"][i]:
                        self.voip_dict[j][0] = self.dict["VOIP"][i]
                voip.enviar_voz_auxiliar()
                self.voip_ug = False
                self.voip_usn = False

            if self.dict["GLB"]["avisado_em_eletrica"]:
                voip.enviar_voz_emergencia()
                self.dict["GLB"]["avisado_em_eletrica"] = False

        except Exception as e:
            logger.exception(f"[OCO] Houve um problema ao ligar por Voip. Exception: \"{repr(e)}\"")
            logger.exception(f"[OCO] Traceback: {traceback.print_stack}")


class OcorrenciasUsn(Ocorrencias):
    def __init__(self, sd, ugs):
        super().__init__(sd, ugs)

        self._condicionadores = []
        self._condicionadores_essenciais = []

        self.normalizar= False
        self.indisponibilizar = False

        self.leitura_condicionadores()

    @property
    def condicionadores(self) -> list([CondicionadorBase]):
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: list([CondicionadorBase])) -> None:
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> list([CondicionadorBase]):
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: list([CondicionadorBase])) -> None:
        self._condicionadores_essenciais = var

    def verificar_condicionadores(self) -> bool:
        if [condic.ativo for condic in self.condicionadores_essenciais]:
            condicionadores_ativos = [x for y in [self.condicionadores_essenciais, self.condicionadores] for x in y if x.ativo]

            self.normalizar = [True for condic in condicionadores_ativos if condic.gravidade == DEVE_NORMALIZAR]
            self.indisponibilizar = [True for condic in condicionadores_ativos if condic.gravidade == DEVE_INDISPONIBILIZAR]

            logger.warning(f"[OCO-USN] Foram detectados condicionadores ativos na Usina:")
            [logger.warning(f"[OCO-USN] Descrição: \"{condic.descr}\", Gravidade: {STR_CONDIC[condic.gravidade] if condic.gravidade in STR_CONDIC else 'Desconhecida'}") for condic in condicionadores_ativos]

            return True if self.normalizar or self.indisponibilizar else False
        else:
            return False

    def leitura_temporizada(self) -> bool:
        try:
            if LeituraModbusCoil("TRIP GMG", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_GMG_Trip"]).valor != 0:
                logger.warning("[OCO-USN] O sensor de TRIP do Grupo Motor Gerador foi acionado, favor verificar.")

            if LeituraModbusCoil("Alarme GMG", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_GMG_Alarme"]).valor != 0:
                logger.warning("[OCO-USN] O alarme do Grupo Motor Gerador foi acionado, favor verificar.")

            if LeituraModbusCoil("Sensor Operação GMG", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_GMG_Operacao"]).valor != 0:
                logger.warning("[OCO-USN] O sensor de operação do Grupo Motor Gerador foi acionado, favor verificar.")

            if LeituraModbusCoil("Baixo Combustível GMG", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_GMG_BaixoComb"]).valor != 0:
                logger.warning("[OCO-USN] O sensor de de combustível baixo do Grupo Motor Gerador foi acionado, favor reabastercer.")

            if LeituraModbusCoil("Falha Acionamento GMG", self.clp_usn, SA["REG_SA_RetornosDigitais_MXR_SA_GMG_FalhaAcion"]).valor != 0:
                logger.warning("[OCO-USN] O sensor do Grupo Motor Gerador identificou uma falha no acionamento, favor verificar.")

            if LeituraModbusCoil("TRIP Disjuntor 52E QLCF", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QLCF_Disj52ETrip"]).valor != 0:
                logger.warning("[OCO-USN] O Disjuntor do Gerador Diesel de Emergência QLCF identificou um sinal de TRIP, favor verificar.")

            if LeituraModbusCoil("TRIP Agrupamento QLCF", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QLCF_TripDisjAgrup"]).valor != 0:
                logger.warning("[OCO-USN] O sensor do Disjuntor de Agrupamento QLCF identificou um sinal de trip, favor verificar.")

            if LeituraModbusCoil("Falha Acionamento Bomba 1", self.clp_usn, SA["REG_SA_RetornosDigitais_MXR_BbaDren1_FalhaAcion"]).valor != 0:
                logger.warning("[OCO-USN] O sensor da Bomba de Drenagem 1 identificou uma falha no acionamento, favor verificar.")

            if LeituraModbusCoil("Falha Acionamento Bomba 2", self.clp_usn, SA["REG_SA_RetornosDigitais_MXR_BbaDren2_FalhaAcion"]).valor != 0:
                logger.warning("[OCO-USN] O sensor da Bomba de Drenagem 2 identificou uma falha no acionamento, favor verificar.")

            if LeituraModbusCoil("Falha Acionamento Bomba 3", self.clp_usn, SA["REG_SA_RetornosDigitais_MXR_BbaDren3_FalhaAcion"]).valor != 0:
                logger.warning("[OCO-USN] O sensor da Bomba de Drenagem 3 identificou uma falha no acionamento, favor verificar.")

            if LeituraModbusCoil("Sensor Barramento Geral QCAP", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_SubtensaoBarraGeral"]).valor != 0:
                logger.warning("[OCO-USN] O sensor de Subtensão do Barramento Geral QCAP foi acionado, favor verificar.")

            leitura_FalhaComunSETDA = LeituraModbusCoil("Falha Comunicação CLPs SA e TDA", self.clp_usn, SA["REG_SA_RetornosDigitais_MXR_FalhaComunSETDA"])
            if leitura_FalhaComunSETDA.valor != 0 and not self.dict["VOIP"]["TDA_FalhaComum"]:
                logger.warning("[OCO-USN] Houve uma falha de comunicação com o CLP da Subestação e o CLP da Tomada da Água, favor verificar")
                self.dict["VOIP"]["TDA_FalhaComum"] = True
                self.voip_usn = True
            elif leitura_FalhaComunSETDA.valor == 0 and self.dict["VOIP"]["TDA_FalhaComum"]:
                self.dict["VOIP"]["TDA_FalhaComum"] = False

            leitura_QCAP_Disj52EFechado = LeituraModbusCoil("Disjuntor 52E QLCF Fechado", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52EFechado"])
            if leitura_QCAP_Disj52EFechado.valor == 1 and not self.dict["VOIP"]["Disj_GDE_QCAP_Fechado"]:
                logger.warning("[OCO-USN] O Disjuntor do Gerador Diesel de Emergência QLCF foi fechado.")
                self.dict["VOIP"]["Disj_GDE_QCAP_Fechado"] = True
                self.voip_usn = True
            elif leitura_QCAP_Disj52EFechado.valor == 0 and self.dict["VOIP"]["Disj_GDE_QCAP_Fechado"]:
                self.dict["VOIP"]["Disj_GDE_QCAP_Fechado"] = False

            leitura_QCADE_BombasDng_Auto = LeituraModbusCoil("Bombas Modo Remoto", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_BombasDng_Auto"])
            if leitura_QCADE_BombasDng_Auto.valor == 0 and not self.dict["VOIP"]["BombasDngRemoto"]:
                logger.warning("[OCO-USN] O poço de drenagem da Usina saiu do modo remoto, favor verificar.")
                self.dict["VOIP"]["BombasDngRemoto"] = True
                self.voip_usn = True
            elif leitura_QCADE_BombasDng_Auto.valor == 1 and self.dict["VOIP"]["BombasDngRemoto"]:
                self.dict["VOIP"]["BombasDngRemoto"] = False

            return True if self.voip_usn else False

        except Exception as e:
            logger.exception(f"[OCO-USN] Houve um erro ao realizar a leitura temporizada da Usina. Exception: \"{repr(e)}\"")
            logger.exception(f"[OCO-USN] Traceback: {traceback.print_stack}")
            return False

    def leitura_condicionadores(self) -> None:
        leitura_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA = LeituraModbusCoil("EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA.descr, DEVE_NORMALIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA))

        leitura_EntradasDigitais_MXI_SA_SEL787_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_SEL787_Trip", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_SEL787_Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_SEL787_Trip.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_SEL787_Trip))

        leitura_EntradasDigitais_MXI_SA_SEL311_Trip = LeituraModbusCoil( "EntradasDigitais_MXI_SA_SEL311_Trip", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_SEL311_Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_SEL311_Trip.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_SEL311_Trip))

        leitura_EntradasDigitais_MXI_SA_MRU3_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRU3_Trip", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_MRU3_Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_MRU3_Trip.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_MRU3_Trip))

        leitura_EntradasDigitais_MXI_SA_MRL1_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRL1_Trip", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_MRL1_Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_MRL1_Trip.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_MRL1_Trip))

        leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip) )

        if not self.dict["GLB"]["tda_offline"]:
            leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETrip = LeituraModbusCoil("EntradasDigitais_MXI_TDA_QcataDisj52ETrip", self.clp_tda, TDA["REG_TDA_EntradasDigitais_MXI_QcataDisj52ETrip"], )
            self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETrip.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETrip))

            leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai = LeituraModbusCoil("EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai", self.clp_tda, TDA["REG_TDA_EntradasDigitais_MXI_QcataDisj52ETripDisjSai"], )
            self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai))

            leitura_EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA = LeituraModbusCoil("EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA", self.clp_tda, TDA["REG_TDA_EntradasDigitais_MXI_QcataDisj52EFalha380VCA"], )
            self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA))

        leitura_EntradasDigitais_MXI_SA_MRU3_Falha = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRU3_Falha", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_MRU3_Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_MRU3_Falha.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_MRU3_Falha))

        leitura_EntradasDigitais_MXI_SA_SEL787_FalhaInterna = LeituraModbusCoil( "EntradasDigitais_MXI_SA_SEL787_FalhaInterna", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_SEL787_FalhaInterna"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_SEL787_FalhaInterna.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_SEL787_FalhaInterna) )

        leitura_EntradasDigitais_MXI_SA_SEL311_Falha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_SEL311_Falha", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_SEL311_Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_SEL311_Falha.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_SEL311_Falha) )

        leitura_EntradasDigitais_MXI_SA_CTE_Falta125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CTE_Falta125Vcc", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_CTE_Falta125Vcc"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CTE_Falta125Vcc.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CTE_Falta125Vcc) )

        leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeTempOleo", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento = ( LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeDesligamento", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento) )

        leitura_EntradasDigitais_MXI_SA_TE_Falha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_Falha", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_TE_Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_Falha.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_Falha) )

        leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsProt = LeituraModbusCoil( "EntradasDigitais_MXI_SA_FalhaDisjTPsProt", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsProt"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsProt.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsProt) )

        leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr = LeituraModbusCoil( "EntradasDigitais_MXI_SA_FalhaDisjTPsSincr", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr) )

        leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CSA1_Secc_Aberta", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta) )

        leitura_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CSA1_FusivelQueimado", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado) )

        leitura_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc) )

        leitura_EntradasDigitais_MXI_SA_QCADE_Nivel4 = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_Nivel4", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_Nivel4"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCADE_Nivel4.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCADE_Nivel4) )

        leitura_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto) )

        leitura_EntradasDigitais_MXI_SA_QCADE_Falha220VCA = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_Falha220VCA", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_Falha220VCA"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCADE_Falha220VCA.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCADE_Falha220VCA) )

        leitura_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCCP_Disj72ETrip", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip) )

        leitura_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCCP_Falta125Vcc", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc) )

        leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup) )

        leitura_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_Falta125Vcc", self.clclp_sap, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc) )

        leitura_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup) )

        leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha) )

        leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_Disj52EFalha", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha) )

        leitura_EntradasDigitais_MXI_SA_GMG_DisjFechado = LeituraModbusCoil( "EntradasDigitais_MXI_SA_GMG_DisjFechado", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_GMG_DisjFechado"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_GMG_DisjFechado.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_GMG_DisjFechado) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets = LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets"], )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07) )

        leitura_RetornosDigitais_MXR_DJ1_FalhaInt = LeituraModbusCoil( "RetornosDigitais_MXR_DJ1_FalhaInt", self.clp_usn, SA["REG_SA_RetornosDigitais_MXR_DJ1_FalhaInt"], )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosDigitais_MXR_DJ1_FalhaInt.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_DJ1_FalhaInt) )

        leitura_RetornosDigitais_MXR_CLP_Falha = LeituraModbusCoil("RetornosDigitais_MXR_CLP_Falha", self.clp_usn, SA["REG_SA_RetornosDigitais_MXR_CLP_Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosDigitais_MXR_CLP_Falha.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_CLP_Falha) )


class OcorrenciasUg(Ocorrencias):
    def __init__(self, sd, ugs):
        super().__init__(sd, ugs)

        self._condicionadores = []
        self._condicionadores_essenciais = []

        self.aguardar = False
        self.normalizar = False
        self.indisponibilizar = False

        for ug in self.ugs: self.leitura_condicionadores(ug)

    @property
    def condicionadores(self) -> list([CondicionadorBase]):
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: list([CondicionadorBase])) -> None:
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> list([CondicionadorBase]):
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: list([CondicionadorBase])) -> None:
        self._condicionadores_essenciais = var

    def verificar_condicionadores(self, ug: UnidadeDeGeracao) -> bool:
        if [condic.ativo for condic in self.condicionadores_essenciais]:
            condicionadores_ativos = [x for y in [self.condicionadores_essenciais, self.condicionadores] for x in y if x.ativo]

            self.aguardar = [True for condic in condicionadores_ativos if condic.gravidade == DEVE_AGUARDAR]
            self.normalizar = [True for condic in condicionadores_ativos if condic.gravidade == DEVE_NORMALIZAR]
            self.indisponibilizar = [True for condic in condicionadores_ativos if condic.gravidade == DEVE_INDISPONIBILIZAR]

            logger.warning(f"[OCO-UG{ug.id}] Foram detectados condicionadores ativos na UG:")
            [logger.warning(f"[OCO-UG{ug.id}] Descrição: \"{condic.descr}\", Gravidade: {STR_CONDIC[condic.gravidade] if condic.gravidade in STR_CONDIC else 'Desconhecida'}") for condic in condicionadores_ativos]

            return True if self.normalizar or self.indisponibilizar or self.aguardar else False
        else:
            return False

    def atualizar_limites_condicionadores(self, parametros, ug: UnidadeDeGeracao) -> None:
        try:
            ug.prioridade = int(parametros[f"ug{ug.id}_prioridade"])
            ug.condicionador_temperatura_fase_r_ug.valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{ug.id}"])
            ug.condicionador_temperatura_fase_r_ug.valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{ug.id}"])
            ug.condicionador_temperatura_fase_s_ug.valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{ug.id}"])
            ug.condicionador_temperatura_fase_s_ug.valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{ug.id}"])
            ug.condicionador_temperatura_fase_t_ug.valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{ug.id}"])
            ug.condicionador_temperatura_fase_t_ug.valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{ug.id}"])
            ug.condicionador_temperatura_nucleo_gerador_1_ug.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_1_ug{ug.id}"])
            ug.condicionador_temperatura_nucleo_gerador_1_ug.valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_1_ug{ug.id}"])
            ug.condicionador_temperatura_nucleo_gerador_2_ug.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_2_ug{ug.id}"])
            ug.condicionador_temperatura_nucleo_gerador_2_ug.valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_2_ug{ug.id}"])
            ug.condicionador_temperatura_nucleo_gerador_3_ug.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_3_ug{ug.id}"])
            ug.condicionador_temperatura_nucleo_gerador_3_ug.valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_3_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_casq_rad_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_casq_rad_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_casq_rad_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_casq_rad_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_casq_comb_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_casq_comb_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_casq_comb_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_casq_comb_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_escora_comb_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_escora_comb_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_escora_comb_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_escora_comb_ug{ug.id}"])
            ug.condicionador_caixa_espiral_ug.valor_base = float(parametros[f"alerta_caixa_espiral_ug{ug.id}"])
            ug.condicionador_caixa_espiral_ug.valor_limite = float(parametros[f"limite_caixa_espiral_ug{ug.id}"])

        except Exception as e:
            logger.exception(f"[OCO-UG{ug.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores. Exception: \"{repr(e)}\"")
            logger.exception(f"[OCO-UG{ug.id}] Traceback: {traceback.print_stack}")

    def leitura_temporizada(self, ug: UnidadeDeGeracao) -> bool:
        try:
            if LeituraModbusCoil("FreioPastilhaGasta", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FreioPastilhaGasta"] ).valor != 0:
                logger.warning(f"[OCO-UG{ug.id}] O sensor de Freio da UG retornou que a Pastilha está gasta, favor considerar troca.")

            if LeituraModbusCoil("FiltroPresSujo75Troc", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FiltroPresSujo75Troc"] ).valor != 0:
                logger.warning(f"[OCO-UG{ug.id}] O sensor do Filtro de Pressão UHRV retornou que o filtro está 75% sujo, favor considerar troca.")

            if LeituraModbusCoil("FiltroRetSujo75Troc", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FiltroRetSujo75Troc"] ).valor != 0:
                logger.warning(f"[OCO-UG{ug.id}] O sensor do Filtro de Retorno UHRV retornou que o filtro está 75% sujo, favor considerar troca.")

            if LeituraModbusCoil("UHLMFilt1PresSujo75Troc", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_Filt1PresSujo75Troc"] ).valor != 0:
                logger.warning(f"[OCO-UG{ug.id}] O sensor do Filtro 1 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")

            if LeituraModbusCoil("UHLMFilt2PresSujo75Troc", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_Filt2PresSujo75Troc"] ).valor != 0:
                logger.warning(f"[OCO-UG{ug.id}] O sensor do Filtro 2 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")

            if LeituraModbusCoil("FiltroPressaoBbaMecSj75", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FiltroPressaoBbaMecSj75"] ).valor != 0:
                logger.warning(f"[OCO-UG{ug.id}] O sensor do Filtro de Pressão da Bomba Mecânica retornou que o filtro está 75% sujo, favor considerar troca.")

            if LeituraModbusCoil("TripPartRes", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_TripPartRes"] ).valor != 0:
                logger.warning(f"[OCO-UG{ug.id}] O sensor TripPartRes retornou valor 1.")

            leitura_EntradasDigitais_MXI_FreioCmdRemoto = LeituraModbusCoil("FreioCmdRemoto", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FreioCmdRemoto"] )
            if leitura_EntradasDigitais_MXI_FreioCmdRemoto.valor == 0 and not self.dict["VOIP"][f"UG{ug.id}_FreioCmdRemoto"]:
                logger.warning(f"[OCO-UG{ug.id}] O freio da UG saiu do modo remoto, favor analisar a situação.")
                self.dict["VOIP"][f"UG{ug.id}_FreioCmdRemoto"] = True
                self.voip_ug = True
            elif leitura_EntradasDigitais_MXI_FreioCmdRemoto.valor == 1 and self.dict["VOIP"][f"UG{ug.id}_FreioCmdRemoto"]:
                self.dict["VOIP"][f"UG{ug.id}_FreioCmdRemoto"] = False

            leitura_EntradasDigitais_MXI_QCAUG1_Remoto = LeituraModbusCoil("QCAUG1_Remoto", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_QCAUG1_Remoto"] )
            if leitura_EntradasDigitais_MXI_QCAUG1_Remoto.valor == 0 and not self.dict["VOIP"][f"UG{ug.id}_QCAUGRemoto"]:
                logger.warning(f"[OCO-UG{ug.id}] O compressor da UG saiu do modo remoto, favor analisar a situação.")
                self.dict["VOIP"][f"UG{ug.id}_QCAUGRemoto"] = True
                self.voip_ug = True
            elif leitura_EntradasDigitais_MXI_QCAUG1_Remoto.valor == 1 and self.dict["VOIP"][f"UG{ug.id}_QCAUGRemoto"]:
                self.dict["VOIP"][f"UG{ug.id}_QCAUGRemoto"] = False

            return True if self.voip_ug else False

        except Exception as e:
            logger.exception(f"[OCO-UG{ug.id}] Houve um erro ao executar a leitura temporizada da UG{ug.id}. Exception: \"{repr(e)}\"")
            logger.exception(f"[OCO-UG{ug.id}] Traceback: {traceback.print_stack}")
            return False

    def leitura_condicionadores(self, ug: UnidadeDeGeracao) -> None:
        self.condicionadores_essenciais.append(ug.condicionador_temperatura_fase_r_ug)
        self.condicionadores_essenciais.append(ug.condicionador_temperatura_fase_s_ug)
        self.condicionadores_essenciais.append(ug.condicionador_temperatura_fase_t_ug)
        self.condicionadores_essenciais.append(ug.condicionador_temperatura_nucleo_gerador_1_ug)
        self.condicionadores_essenciais.append(ug.condicionador_temperatura_nucleo_gerador_2_ug)
        self.condicionadores_essenciais.append(ug.condicionador_temperatura_nucleo_gerador_3_ug)
        self.condicionadores_essenciais.append(ug.condicionador_temperatura_mancal_casq_rad_ug)
        self.condicionadores_essenciais.append(ug.condicionador_temperatura_mancal_casq_comb_ug)
        self.condicionadores_essenciais.append(ug.condicionador_temperatura_mancal_escora_comb_ug)

        leitura_ComandosDigitais_MXW_EmergenciaViaSuper = LeituraModbusCoil("ComandosDigitais_MXW_EmergenciaViaSuper", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_ComandosDigitais_MXW_EmergenciaViaSuper"],)
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ComandosDigitais_MXW_EmergenciaViaSuper.descr, DEVE_NORMALIZAR, leitura_ComandosDigitais_MXW_EmergenciaViaSuper, ug.id, [UNIDADE_SINCRONIZADA, UNIDADE_SINCRONIZANDO]))

        leitura_RetornosDigitais_MXR_TripEletrico = LeituraModbusCoil("RetornosDigitais_MXR_TripEletrico", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripEletrico"],)
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_RetornosDigitais_MXR_TripEletrico.descr, DEVE_NORMALIZAR, leitura_RetornosDigitais_MXR_TripEletrico, ug.id, [UNIDADE_SINCRONIZADA, UNIDADE_SINCRONIZANDO]))

        leitura_ReleBloqA86MAtuado = LeituraModbusCoil("ReleBloqA86MAtuado", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_ReleBloqA86MAtuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ReleBloqA86MAtuado.descr, DEVE_INDISPONIBILIZAR, leitura_ReleBloqA86MAtuado))

        leitura_ReleBloqA86HAtuado = LeituraModbusCoil("ReleBloqA86HAtuado", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_ReleBloqA86HAtuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ReleBloqA86HAtuado.descr, DEVE_NORMALIZAR, leitura_ReleBloqA86HAtuado, ug.id, [UNIDADE_SINCRONIZADA, UNIDADE_SINCRONIZANDO]))

        leitura_SEL700G_Atuado = LeituraModbusCoil("SEL700G_Atuado", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_SEL700G_Atuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_SEL700G_Atuado.descr, DEVE_INDISPONIBILIZAR, leitura_SEL700G_Atuado))

        leitura_RV_Trip = LeituraModbusCoil("RV_Trip", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_RV_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_RV_Trip.descr, DEVE_INDISPONIBILIZAR, leitura_RV_Trip))

        leitura_RetornosDigitais_MXR_TripMecanico = LeituraModbusCoil("RetornosDigitais_MXR_TripMecanico", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripMecanico"],)
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_RetornosDigitais_MXR_TripMecanico.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripMecanico))

        leitura_RetornosDigitais_MXR_700G_Trip = LeituraModbusCoil("RetornosDigitais_MXR_700G_Trip", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_700G_Trip"],) 
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_RetornosDigitais_MXR_700G_Trip.descr, DEVE_NORMALIZAR, leitura_RetornosDigitais_MXR_700G_Trip, ug.id, [UNIDADE_SINCRONIZADA, UNIDADE_SINCRONIZANDO]))

        leitura_AVR_Trip = LeituraModbusCoil("AVR_Trip", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_AVR_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_AVR_Trip.descr, DEVE_INDISPONIBILIZAR, leitura_AVR_Trip))

        leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG1 = LeituraModbusCoil("SA_FalhaDisjTPsSincrG1",self.clp_usn,SA["REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG1"],)
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG1.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG1))

        leitura_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa = LeituraModbusCoil("SA_DisjDJ1_BloqPressBaixa",self.clp_usn,SA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa"],)
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa))

        leitura_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa = LeituraModbusCoil("SA_DisjDJ1_AlPressBaixa",self.clp_usn,SA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa"],)
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa))

        leitura_EntradasDigitais_MXI_ValvBorbTravada = LeituraModbusCoil("MXI_ValvBorbTravada", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_ValvBorbTravada"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_ValvBorbTravada.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_ValvBorbTravada) )

        leitura_EntradasDigitais_MXI_UHRV_TripBomba2 = LeituraModbusCoil("UHRV_TripBomba2", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHRV_TripBomba2"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHRV_TripBomba2.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHRV_TripBomba2) )

        leitura_EntradasDigitais_MXI_UHRV_TripBomba1 = LeituraModbusCoil("UHRV_TripBomba1", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHRV_TripBomba1"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHRV_TripBomba1.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHRV_TripBomba1) )

        leitura_EntradasDigitais_MXI_UHRV_NivOleominimoPos36 = LeituraModbusCoil("UHRV_NivOleominimoPos36", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHRV_NivOleominimoPos36"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHRV_NivOleominimoPos36.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHRV_NivOleominimoPos36) )

        leitura_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35 = LeituraModbusCoil("UHRV_NivOleoCriticoPos35", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35) )

        leitura_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo = LeituraModbusCoil("UHLM_Filt2PresSujo100Sujo", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo) )

        leitura_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo = LeituraModbusCoil("UHLM_Filt1PresSujo100Sujo", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo) )

        leitura_EntradasDigitais_MXI_UHLM_TripBomba2 = LeituraModbusCoil("UHLM_TripBomba2", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_TripBomba2"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_TripBomba2.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_TripBomba2) )

        leitura_EntradasDigitais_MXI_UHLM_TripBomba1 = LeituraModbusCoil("UHLM_TripBomba1", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_TripBomba1"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_TripBomba1.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_TripBomba1) )

        leitura_EntradasDigitais_MXI_UHLM_NivelminOleo = LeituraModbusCoil("UHLM_NivelminOleo", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_NivelminOleo"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_NivelminOleo.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_NivelminOleo) )

        leitura_EntradasDigitais_MXI_UHLM_NivelCritOleo = LeituraModbusCoil("UHLM_NivelCritOleo", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_NivelCritOleo"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_NivelCritOleo.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_NivelCritOleo) )

        leitura_EntradasDigitais_MXI_UHLM_FluxoMcTras = LeituraModbusCoil("UHLM_FluxoMcTras", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_FluxoMcTras"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_FluxoMcTras.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_FluxoMcTras) )

        leitura_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro = LeituraModbusCoil("UHLM_FluxoMcDianteiro", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro) )

        leitura_EntradasDigitais_MXI_UHLM_FaltaPressTroc = LeituraModbusCoil("UHLM_FaltaPressTroc", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_FaltaPressTroc"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_FaltaPressTroc.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_FaltaPressTroc) )

        leitura_EntradasDigitais_MXI_UHLM_FaltaFluxTroc = LeituraModbusCoil("UHLM_FaltaFluxTroc", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_FaltaFluxTroc"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_FaltaFluxTroc.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_FaltaFluxTroc) )

        leitura_EntradasDigitais_MXI_TripAlimPainelFreio = LeituraModbusCoil("TripAlimPainelFreio", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_TripAlimPainelFreio"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_TripAlimPainelFreio.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_TripAlimPainelFreio) )

        leitura_EntradasDigitais_MXI_SobreVeloMecPos18 = LeituraModbusCoil("SobreVeloMecPos18", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_SobreVeloMecPos18"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_SobreVeloMecPos18.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SobreVeloMecPos18) )

        leitura_EntradasDigitais_MXI_SEL700G_FalhaInterna = LeituraModbusCoil("SEL700G_FalhaInterna", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_SEL700G_FalhaInterna"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_SEL700G_FalhaInterna.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SEL700G_FalhaInterna) )

        leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2 = LeituraModbusCoil("UHRV_FalhaAcionBbaM2", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2) )

        leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1 = LeituraModbusCoil("UHRV_FalhaAcionBbaM1", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1) )

        leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2 = LeituraModbusCoil("UHLM_FalhaAcionBbaM2", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2) )

        leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1 = LeituraModbusCoil("UHLM_FalhaAcionBbaM1", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1) )

        leitura_RetornosDigitais_MXR_TripVibr2 = LeituraModbusCoil("TripVibr2", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripVibr2"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripVibr2.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripVibr2) )

        leitura_RetornosDigitais_MXR_TripVibr1 = LeituraModbusCoil("TripVibr1", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripVibr1"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripVibr1.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripVibr1) )

        leitura_RetornosDigitais_MXR_TripTempUHRV = LeituraModbusCoil("TripTempUHRV", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripTempUHRV"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripTempUHRV.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripTempUHRV) )

        leitura_RetornosDigitais_MXR_TripTempUHLM = LeituraModbusCoil("TripTempUHLM", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripTempUHLM"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripTempUHLM.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripTempUHLM) )

        leitura_RetornosDigitais_MXR_TripTempMcGuiaRadial = LeituraModbusCoil("TripTempMcGuiaRadial", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripTempMcGuiaRadial"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripTempMcGuiaRadial.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripTempMcGuiaRadial) )

        leitura_RetornosDigitais_MXR_TripTempMcGuiaEscora = LeituraModbusCoil("TripTempMcGuiaEscora", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripTempMcGuiaEscora"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripTempMcGuiaEscora.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripTempMcGuiaEscora) )

        leitura_RetornosDigitais_MXR_TripTempMcGuiaContraEscora = LeituraModbusCoil("TripTempMcGuiaContraEscora", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripTempMcGuiaContraEscora"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripTempMcGuiaContraEscora.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripTempMcGuiaContraEscora) )

        leitura_RetornosDigitais_MXR_TripTempGaxeteiro = LeituraModbusCoil("TripTempGaxeteiro", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripTempGaxeteiro"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripTempGaxeteiro.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripTempGaxeteiro) )

        leitura_RetornosDigitais_MXR_Q_Negativa = LeituraModbusCoil("Q_Negativa", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_Q_Negativa"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_Q_Negativa.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_Q_Negativa) )

        leitura_RetornosDigitais_MXR_FalhaIbntDisjGer = LeituraModbusCoil("FalhaIbntDisjGer", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_FalhaIbntDisjGer"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_FalhaIbntDisjGer.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_FalhaIbntDisjGer) )

        leitura_RetornosDigitais_MXR_FalhaAcionFechaValvBorb = LeituraModbusCoil("FalhaAcionFechaValvBorb", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_FalhaAcionFechaValvBorb"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_FalhaAcionFechaValvBorb.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_FalhaAcionFechaValvBorb) )

        leitura_RetornosDigitais_MXR_CLP_Falha = LeituraModbusCoil("CLP_Falha", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_CLP_Falha"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_CLP_Falha.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_CLP_Falha) )

        leitura_RetornosDigitais_MXR_Remota_Falha = LeituraModbusCoil("Remota_Falha", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_Remota_Falha"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_Remota_Falha.descr, DEVE_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_Remota_Falha) )

        leitura_EntradasDigitais_MXI_QCAUG_TripDisjAgrup = LeituraModbusCoil("QCAUG_TripDisjAgrup", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_QCAUG_TripDisjAgrup"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_QCAUG_TripDisjAgrup.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_QCAUG_TripDisjAgrup) )

        leitura_EntradasDigitais_MXI_QCAUG_TripDisj52A1 = LeituraModbusCoil("QCAUG_TripDisj52A1", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_QCAUG_TripDisj52A1"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_QCAUG_TripDisj52A1.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_QCAUG_TripDisj52A1) )

        leitura_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel = LeituraModbusCoil("QCAUG_Falha380VcaPainel", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel.descr, DEVE_NORMALIZAR, leitura_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel) )

        leitura_EntradasDigitais_MXI_PalhetasDesal = LeituraModbusCoil("PalhetasDesal", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_PalhetasDesal"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_PalhetasDesal.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_PalhetasDesal) )

        leitura_EntradasDigitais_MXI_NivelMAltoPocoDren = LeituraModbusCoil("NivelMAltoPocoDren", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_NivelMAltoPocoDren"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_NivelMAltoPocoDren.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_NivelMAltoPocoDren) )

        leitura_EntradasDigitais_MXI_FreioSemEnergia = LeituraModbusCoil("FreioSemEnergia", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FreioSemEnergia"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_FreioSemEnergia.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_FreioSemEnergia) )

        leitura_EntradasDigitais_MXI_FreioFiltroSaturado = LeituraModbusCoil("FreioFiltroSaturado", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FreioFiltroSaturado"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_FreioFiltroSaturado.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_FreioFiltroSaturado) )

        leitura_EntradasDigitais_MXI_FiltroRetSujo100Sujo = LeituraModbusCoil("FiltroRetSujo100Sujo", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FiltroRetSujo100Sujo"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_FiltroRetSujo100Sujo.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_FiltroRetSujo100Sujo) )

        leitura_EntradasDigitais_MXI_FiltroPresSujo100Sujo = LeituraModbusCoil("FiltroPresSujo100Sujo", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FiltroPresSujo100Sujo"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_FiltroPresSujo100Sujo.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_FiltroPresSujo100Sujo) )

        leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100 = LeituraModbusCoil("FiltroPressaoBbaMecSj100", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100) )

        leitura_EntradasDigitais_MXI_FaltaFluxoOleoMc = LeituraModbusCoil("FaltaFluxoOleoMc", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FaltaFluxoOleoMc"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_FaltaFluxoOleoMc.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_FaltaFluxoOleoMc) )

        leitura_EntradasDigitais_MXI_Falta125VccCom = LeituraModbusCoil("Falta125VccCom", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_Falta125VccCom"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_Falta125VccCom.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_Falta125VccCom) )

        leitura_EntradasDigitais_MXI_Falta125VccAlimVal = LeituraModbusCoil("Falta125VccAlimVal", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_Falta125VccAlimVal"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_Falta125VccAlimVal.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_Falta125VccAlimVal) )

        leitura_EntradasDigitais_MXI_Falta125Vcc = LeituraModbusCoil("Falta125Vcc", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_Falta125Vcc"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_Falta125Vcc.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_Falta125Vcc) )

        leitura_EntradasDigitais_MXI_FalhaDisjTpsProt = LeituraModbusCoil("FalhaDisjTpsProt", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FalhaDisjTpsProt"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_FalhaDisjTpsProt.descr, DEVE_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_FalhaDisjTpsProt) )

        leitura_AVR_EntradasDigitais_MXI_FalhaInterna = LeituraModbusCoil("AVR_FalhaInterna", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_AVR_FalhaInterna"] )
        self.condicionadores.append( CondicionadorBase(leitura_AVR_EntradasDigitais_MXI_FalhaInterna.descr, DEVE_INDISPONIBILIZAR, leitura_AVR_EntradasDigitais_MXI_FalhaInterna) )