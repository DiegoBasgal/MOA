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
        self.voip_ug: bool = None
        self.voip_usn: bool = None

        self.voip_dict: dict = voip.vars_dict

    # Property/Setter Protegidos
    @property
    def ugs(self) -> list([UnidadeDeGeracao]):
        return self._ugs

    @ugs.setter
    def ugs(self, var: list([UnidadeDeGeracao])) -> None:
        self._ugs = var

    def leitura_periodica(self, delay: int) -> None:
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

        self._condicionadores: list(CondicionadorBase)
        self._condicionadores_essenciais: list(CondicionadorBase)

        self.flag: int = CONDIC_IGNORAR

        self.leitura_condicionadores()

    @property
    def condicionadores(self) -> list(CondicionadorBase):
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: list(CondicionadorBase)) -> None:
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> list(CondicionadorBase):
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: list(CondicionadorBase)) -> None:
        self._condicionadores_essenciais = var

    def verificar_condicionadores(self) -> int:
        if [condic.ativo for condic in self.condicionadores_essenciais]:
            condicionadores_ativos = [x for y in [self.condicionadores_essenciais, self.condicionadores] for x in y if x.ativo]

            self.flag = [CONDIC_NORMALIZAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_NORMALIZAR]
            self.flag = [CONDIC_INDISPONIBILIZAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_INDISPONIBILIZAR]

            logger.warning(f"[OCO-USN] Foram detectados condicionadores ativos na Usina:")
            [logger.warning(f"[OCO-USN] Descrição: \"{condic.descr}\", Gravidade: {CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}") for condic in condicionadores_ativos]

        return self.flag

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
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA.descr, CONDIC_NORMALIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA))

        leitura_EntradasDigitais_MXI_SA_SEL787_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_SEL787_Trip", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_SEL787_Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_SEL787_Trip.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_SEL787_Trip))

        leitura_EntradasDigitais_MXI_SA_SEL311_Trip = LeituraModbusCoil( "EntradasDigitais_MXI_SA_SEL311_Trip", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_SEL311_Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_SEL311_Trip.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_SEL311_Trip))

        leitura_EntradasDigitais_MXI_SA_MRU3_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRU3_Trip", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_MRU3_Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_MRU3_Trip.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_MRU3_Trip))

        leitura_EntradasDigitais_MXI_SA_MRL1_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRL1_Trip", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_MRL1_Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_MRL1_Trip.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_MRL1_Trip))

        leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip"], )
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip) )

        if not self.dict["GLB"]["tda_offline"]:
            leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETrip = LeituraModbusCoil("EntradasDigitais_MXI_TDA_QcataDisj52ETrip", self.clp_tda, TDA["REG_TDA_EntradasDigitais_MXI_QcataDisj52ETrip"], )
            self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETrip.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETrip))

            leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai = LeituraModbusCoil("EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai", self.clp_tda, TDA["REG_TDA_EntradasDigitais_MXI_QcataDisj52ETripDisjSai"], )
            self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_TDA_QcataDisj52ETripDisjSai))

            leitura_EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA = LeituraModbusCoil("EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA", self.clp_tda, TDA["REG_TDA_EntradasDigitais_MXI_QcataDisj52EFalha380VCA"], )
            self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_TDA_QcataDisj52EFalha380VCA))

        leitura_EntradasDigitais_MXI_SA_MRU3_Falha = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRU3_Falha", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_MRU3_Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_MRU3_Falha.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_MRU3_Falha))

        leitura_EntradasDigitais_MXI_SA_SEL787_FalhaInterna = LeituraModbusCoil( "EntradasDigitais_MXI_SA_SEL787_FalhaInterna", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_SEL787_FalhaInterna"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_SEL787_FalhaInterna.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_SEL787_FalhaInterna) )

        leitura_EntradasDigitais_MXI_SA_SEL311_Falha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_SEL311_Falha", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_SEL311_Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_SEL311_Falha.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_SEL311_Falha) )

        leitura_EntradasDigitais_MXI_SA_CTE_Falta125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CTE_Falta125Vcc", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_CTE_Falta125Vcc"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CTE_Falta125Vcc.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CTE_Falta125Vcc) )

        leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeTempOleo", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento = ( LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento) )

        leitura_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_AlarmeDesligamento", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento) )

        leitura_EntradasDigitais_MXI_SA_TE_Falha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_TE_Falha", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_TE_Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_TE_Falha.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_TE_Falha) )

        leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsProt = LeituraModbusCoil( "EntradasDigitais_MXI_SA_FalhaDisjTPsProt", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsProt"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsProt.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsProt) )

        leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr = LeituraModbusCoil( "EntradasDigitais_MXI_SA_FalhaDisjTPsSincr", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr) )

        leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CSA1_Secc_Aberta", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta) )

        leitura_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CSA1_FusivelQueimado", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado) )

        leitura_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc) )

        leitura_EntradasDigitais_MXI_SA_QCADE_Nivel4 = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_Nivel4", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_Nivel4"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCADE_Nivel4.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCADE_Nivel4) )

        leitura_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto) )

        leitura_EntradasDigitais_MXI_SA_QCADE_Falha220VCA = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCADE_Falha220VCA", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCADE_Falha220VCA"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCADE_Falha220VCA.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCADE_Falha220VCA) )

        leitura_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCCP_Disj72ETrip", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip) )

        leitura_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCCP_Falta125Vcc", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc) )

        leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup) )

        leitura_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_Falta125Vcc", self.clclp_sap, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc) )

        leitura_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup) )

        leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha) )

        leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha = LeituraModbusCoil( "EntradasDigitais_MXI_SA_QCAP_Disj52EFalha", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha) )

        leitura_EntradasDigitais_MXI_SA_GMG_DisjFechado = LeituraModbusCoil( "EntradasDigitais_MXI_SA_GMG_DisjFechado", self.clp_usn, SA["REG_SA_EntradasDigitais_MXI_SA_GMG_DisjFechado"], )
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_GMG_DisjFechado.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_GMG_DisjFechado) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets = LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets"], )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06) )

        leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07 = ( LeituraModbusCoil( "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07", self.clp_usn, SA["REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07"], ) )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07) )

        leitura_RetornosDigitais_MXR_DJ1_FalhaInt = LeituraModbusCoil( "RetornosDigitais_MXR_DJ1_FalhaInt", self.clp_usn, SA["REG_SA_RetornosDigitais_MXR_DJ1_FalhaInt"], )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosDigitais_MXR_DJ1_FalhaInt.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_DJ1_FalhaInt) )

        leitura_RetornosDigitais_MXR_CLP_Falha = LeituraModbusCoil("RetornosDigitais_MXR_CLP_Falha", self.clp_usn, SA["REG_SA_RetornosDigitais_MXR_CLP_Falha"], )
        self.condicionadores.append(CondicionadorBase(leitura_RetornosDigitais_MXR_CLP_Falha.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_CLP_Falha) )


class OcorrenciasUg(Ocorrencias):
    def __init__(self, sd, ugs):
        super().__init__(sd, ugs)

        self._temperatura_base: int = 100
        self._temperatura_limite: int = 200
        self._pressao_caixa_base: float = 16
        self._pressao_caixa_limite: float = 15.5

        self._condicionadores: list(CondicionadorBase)
        self._condicionadores_essenciais: list(CondicionadorBase)
        self._condicionadores_atenuadores: list(CondicionadorBase)

        self._condic_dict: dict
        self._leitura_dict: dict

        self.flag: int = CONDIC_IGNORAR

        for ug in self.ugs: self.leitura_condicionadores(ug)

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
    def pressao_caixa_base(self) -> float:
        return self._pressao_caixa_base

    @pressao_caixa_base.setter
    def pressao_caixa_base(self, var: float):
        self._pressao_caixa_base = var

    @property
    def pressao_caixa_limite(self) -> float:
        return self._pressao_caixa_limite

    @pressao_caixa_limite.setter
    def pressao_caixa_limite(self, var: float):
        self._pressao_caixa_limite = var

    @property
    def condic_dict(self) -> dict({CondicionadorExponencial}):
        return self._condic_dict

    @condic_dict.setter
    def condic_dict(self, var: dict({CondicionadorExponencial})) -> None:
        self._condic_dict = var
    
    @property
    def leitura_dict(self) -> dict({LeituraBase}):
        return self._leitura_dict

    @leitura_dict.setter
    def leitura_dict(self, var: dict({LeituraBase})) -> None:
        self._leitura_dict = var

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

    @property
    def condicionadores_atenuadores(self) -> list([CondicionadorBase]):
        return self._condicionadores_atenuadores

    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: list([CondicionadorBase])) -> None:
        self._condicionadores_atenuadores = var

    def verificar_condicionadores(self, ug: UnidadeDeGeracao) -> int:
        if [condic.ativo for condic in self.condicionadores_essenciais]:
            condicionadores_ativos = [x for y in [self.condicionadores_essenciais, self.condicionadores] for x in y if x.ativo]

            self.flag = [CONDIC_AGUARDAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_AGUARDAR]
            self.flag = [CONDIC_NORMALIZAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_NORMALIZAR]
            self.flag = [CONDIC_INDISPONIBILIZAR for condic in condicionadores_ativos if condic.gravidade == CONDIC_INDISPONIBILIZAR]

            logger.warning(f"[OCO-UG{ug.id}] Foram detectados condicionadores ativos na UG:")
            [logger.warning(f"[OCO-UG{ug.id}] Descrição: \"{condic.descr}\", Gravidade: {CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}") for condic in condicionadores_ativos]

        return self.flag

    def atualizar_limites_condicionadores(self, parametros, ug: UnidadeDeGeracao) -> None:
        try:
            ug.prioridade = int(parametros[f"ug{ug.id}_prioridade"])
            self.condic_dict[f"temperatura_fase_r_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{ug.id}"])
            self.condic_dict[f"temperatura_fase_r_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{ug.id}"])
            self.condic_dict[f"temperatura_fase_s_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{ug.id}"])
            self.condic_dict[f"temperatura_fase_s_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{ug.id}"])
            self.condic_dict[f"temperatura_fase_t_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{ug.id}"])
            self.condic_dict[f"temperatura_fase_t_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{ug.id}"])
            self.condic_dict[f"temperatura_nucleo_gerador_1_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_1_ug{ug.id}"])
            self.condic_dict[f"temperatura_nucleo_gerador_1_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_1_ug{ug.id}"])
            self.condic_dict[f"temperatura_nucleo_gerador_2_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_2_ug{ug.id}"])
            self.condic_dict[f"temperatura_nucleo_gerador_2_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_2_ug{ug.id}"])
            self.condic_dict[f"temperatura_nucleo_gerador_3_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_3_ug{ug.id}"])
            self.condic_dict[f"temperatura_nucleo_gerador_3_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_3_ug{ug.id}"])
            self.condic_dict[f"temperatura_mancal_casq_rad_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_casq_rad_ug{ug.id}"])
            self.condic_dict[f"temperatura_mancal_casq_rad_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_casq_rad_ug{ug.id}"])
            self.condic_dict[f"temperatura_mancal_casq_comb_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_casq_comb_ug{ug.id}"])
            self.condic_dict[f"temperatura_mancal_casq_comb_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_casq_comb_ug{ug.id}"])
            self.condic_dict[f"temperatura_mancal_escora_comb_ug{ug.id}"].valor_base = float(parametros[f"alerta_temperatura_mancal_escora_comb_ug{ug.id}"])
            self.condic_dict[f"temperatura_mancal_escora_comb_ug{ug.id}"].valor_limite = float(parametros[f"limite_temperatura_mancal_escora_comb_ug{ug.id}"])
            self.condic_dict[f"caixa_espiral_ug{ug.id}"].valor_base = float(parametros[f"alerta_caixa_espiral_ug{ug.id}"])
            self.condic_dict[f"caixa_espiral_ug{ug.id}"].valor_limite = float(parametros[f"limite_caixa_espiral_ug{ug.id}"])

        except Exception as e:
            logger.exception(f"[OCO-UG{ug.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores. Exception: \"{repr(e)}\"")
            logger.exception(f"[OCO-UG{ug.id}] Traceback: {traceback.print_stack}")

    def controle_limites_operacao(self, ug: UnidadeDeGeracao) -> None:
        fase_r = [self.leitura_dict[f"temperatura_fase_r_ug{ug.id}"], self.condic_dict[f"temperatura_fase_r_ug{ug.id}"]]
        fase_s = [self.leitura_dict[f"temperatura_fase_s_ug{ug.id}"], self.condic_dict[f"temperatura_fase_s_ug{ug.id}"]]
        fase_t = [self.leitura_dict[f"temperatura_fase_t_ug{ug.id}"], self.condic_dict[f"temperatura_fase_t_ug{ug.id}"]]
        nucleo_1 = [self.leitura_dict[f"temperatura_nucleo_gerador_1_ug{ug.id}"], self.condic_dict[f"temperatura_nucleo_gerador_1_ug{ug.id}"]]
        nucleo_2 = [self.leitura_dict[f"temperatura_nucleo_gerador_2_ug{ug.id}"], self.condic_dict[f"temperatura_nucleo_gerador_2_ug{ug.id}"]]
        nucleo_3 = [self.leitura_dict[f"temperatura_nucleo_gerador_3_ug{ug.id}"], self.condic_dict[f"temperatura_nucleo_gerador_3_ug{ug.id}"]]
        mancal_CR = [self.leitura_dict[f"temperatura_mancal_casq_rad_ug{ug.id}"], self.condic_dict[f"temperatura_mancal_casq_rad_ug{ug.id}"]]
        mancal_CC = [self.leitura_dict[f"temperatura_mancal_casq_comb_ug{ug.id}"], self.condic_dict[f"temperatura_mancal_casq_comb_ug{ug.id}"]]
        mancal_EC = [self.leitura_dict[f"temperatura_mancal_escora_comb_ug{ug.id}"], self.condic_dict[f"temperatura_mancal_escora_comb_ug{ug.id}"]]
        caixa_espiral = [self.leitura_dict[f"caixa_espiral_ug{ug.id}"], self.condic_dict[f"caixa_espiral_ug{ug.id}"]]

        if fase_r[0].valor >= fase_r[1].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura de Fase R da UG passou do valor base! ({fase_r[1].valor_base}C) | Leitura: {fase_r[0].valor}C")
        if fase_r[0].valor >= 0.9*(fase_r[1].valor_limite - fase_r[1].valor_base) + fase_r[1].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura de Fase R da UG está muito próxima do limite! ({fase_r[1].valor_limite}C) | Leitura: {fase_r[0].valor}C")

        if fase_s[0].valor >= fase_s[1].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura de Fase S da UG passou do valor base! ({fase_s[1].valor_base}C) | Leitura: {fase_s[0].valor}C")
        if fase_s[0].valor >= 0.9*(fase_s[1].valor_limite - fase_s[1].valor_base) + fase_s[1].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura de Fase S da UG está muito próxima do limite! ({fase_s[1].valor_limite}C) | Leitura: {fase_s[0].valor}C")

        if fase_t[0].valor >= fase_t[1].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura de Fase T da UG passou do valor base! ({fase_t[1].valor_base}C) | Leitura: {fase_t[0].valor}C")
        if fase_t[0].valor >= 0.9*(fase_t[1].valor_limite - fase_t[1].valor_base) + fase_t[1].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura de Fase T da UG está muito próxima do limite! ({fase_t[1].valor_limite}C) | Leitura: {fase_t[0].valor}C")

        if nucleo_1[0].valor >= nucleo_1[1].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura do Núcleo Gerador 1 da UG passou do valor base! ({nucleo_1[1].valor_base}C) | Leitura: {nucleo_1[0].valor}C")
        if nucleo_1[0].valor >= 0.9*(nucleo_1[1].valor_limite - nucleo_1[1].valor_base) + nucleo_1[1].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura do Núcleo Gerador 1 da UG está muito próxima do limite! ({nucleo_1[1].valor_limite}C) | Leitura: {nucleo_1[0].valor}C")

        if nucleo_2[0].valor >= nucleo_2[1].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura do Núcleo Gerador 2 da UG passou do valor base! ({nucleo_2[1].valor_base}C) | Leitura: {nucleo_2[0].valor}C")
        if nucleo_2[0].valor >= 0.9*(nucleo_2[1].valor_limite - nucleo_2[1].valor_base) + nucleo_2[1].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura do Núcleo Gerador 2 da UG está muito próxima do limite! ({nucleo_2[1].valor_limite}C) | Leitura: {nucleo_2[0].valor}C")

        if nucleo_3[0].valor >= nucleo_3[1].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura do Núcleo Gerador 3 da UG passou do valor base! ({nucleo_3[1].valor_base}C) | Leitura: {nucleo_3[0].valor}C")
        if nucleo_3[0].valor >= 0.9*(nucleo_3[1].valor_limite - nucleo_3[1].valor_base) + nucleo_3[1].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura do Núcleo Gerador 3 da UG está muito próxima do limite! ({nucleo_3[1].valor_limite}C) | Leitura: {nucleo_3[0].valor}C")

        if mancal_CR[0].valor >= mancal_CR[1].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura do Mancal Casquilho Radial da UG passou do valor base! ({mancal_CR[1].valor_base}C) | Leitura: {mancal_CR[0].valor}C")
        if mancal_CR[0].valor >= 0.9*(mancal_CR[1].valor_limite - mancal_CR[1].valor_base) + mancal_CR[1].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura do Mancal Casquilho Radial da UG está muito próxima do limite! ({mancal_CR[1].valor_limite}C) | Leitura: {mancal_CR[0].valor}C")

        if mancal_CC[0].valor >= mancal_CC[1].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura do Mancal Casquilho Combinado da UG passou do valor base! ({mancal_CC[1].valor_base}C) | Leitura: {mancal_CC[0].valor}C")
        if mancal_CC[0].valor >= 0.9*(mancal_CC[1].valor_limite - mancal_CC[1].valor_base) + mancal_CC[1].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura do Mancal Casquilho Combinado da UG está muito próxima do limite! ({mancal_CC[1].valor_limite}C) | Leitura: {mancal_CC[0].valor}C")

        if mancal_EC[0].valor >= mancal_EC[1].valor_base:
            logger.warning(f"[UG{ug.id}] A temperatura do Mancal Escora Combinado da UG passou do valor base! ({mancal_EC[1].valor_base}C) | Leitura: {mancal_EC[0].valor}C")
        if mancal_EC[0].valor >= 0.9*(mancal_EC[1].valor_limite - mancal_EC[1].valor_base) + mancal_EC[1].valor_base:
            logger.critical(f"[UG{ug.id}] A temperatura do Mancal Escora Combinado da UG está muito próxima do limite! ({mancal_EC[1].valor_limite}C) | Leitura: {mancal_EC[0].valor}C")

        if caixa_espiral[0].valor <= caixa_espiral[1].valor_base and caixa_espiral[0].valor != 0 and self.etapa_atual == UG_SINCRONIZADA:
            logger.warning(f"[UG{ug.id}] A pressão Caixa Espiral da UG passou do valor base! ({caixa_espiral[1].valor_base:03.2f} KGf/m2) | Leitura: {caixa_espiral[0].valor:03.2f}")
        if caixa_espiral[0].valor <= caixa_espiral[1].valor_limite+0.9*(caixa_espiral[1].valor_base - caixa_espiral[1].valor_limite) and caixa_espiral[0].valor != 0 and self.etapa_atual == UG_SINCRONIZADA:
            logger.critical(f"[UG{ug.id}] A pressão Caixa Espiral da UG está muito próxima do limite! ({caixa_espiral[1].valor_limite:03.2f} KGf/m2) | Leitura: {caixa_espiral[0].valor:03.2f} KGf/m2")


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

            leitura_EntradasDigitais_MXI_QCAUG_Remoto = LeituraModbusCoil("QCAUG_Remoto", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_QCAUG{ug.id}_Remoto"] )
            if leitura_EntradasDigitais_MXI_QCAUG_Remoto.valor == 0 and not self.dict["VOIP"][f"UG{ug.id}_QCAUGRemoto"]:
                logger.warning(f"[OCO-UG{ug.id}] O compressor da UG saiu do modo remoto, favor analisar a situação.")
                self.dict["VOIP"][f"UG{ug.id}_QCAUGRemoto"] = True
                self.voip_ug = True
            elif leitura_EntradasDigitais_MXI_QCAUG_Remoto.valor == 1 and self.dict["VOIP"][f"UG{ug.id}_QCAUGRemoto"]:
                self.dict["VOIP"][f"UG{ug.id}_QCAUGRemoto"] = False

            return True if self.voip_ug else False

        except Exception as e:
            logger.exception(f"[OCO-UG{ug.id}] Houve um erro ao executar a leitura temporizada da UG{ug.id}. Exception: \"{repr(e)}\"")
            logger.exception(f"[OCO-UG{ug.id}] Traceback: {traceback.print_stack}")
            return False

    def leitura_condicionadores(self, ug: UnidadeDeGeracao) -> None:
        # Leituras -> Condicionadores
        # Fase R
        self.leitura_dict[f"temperatura_fase_r_ug{ug.id}"] = LeituraModbus(
            f"[UG{ug.id}] Temperatura Fase R",
            self.clp_ug,
            UG[f"REG_UG{ug.id}_RetornosAnalogicos_MWR_Temperatura_01"],
            op=4
        )
        self.condic_dict[f"temperatura_fase_r_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"temperatura_fase_r_ug{ug.id}"].descr, 
            CONDIC_INDISPONIBILIZAR,
            self.leitura_dict[f"temperatura_fase_r_ug{ug.id}"],
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"temperatura_fase_r_ug{ug.id}"])

        # Fase S
        self.leitura_dict[f"temperatura_fase_s_ug{ug.id}"] = LeituraModbus(
            f"[UG{ug.id}] Temperatura Fase S",
            self.clp_ug,
            UG[f"REG_UG{ug.id}_RetornosAnalogicos_MWR_Temperatura_02"],
            op=4
        )
        self.condic_dict[f"temperatura_fase_s_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"temperatura_fase_s_ug{ug.id}"].descr,
            CONDIC_INDISPONIBILIZAR,
            self.leitura_dict[f"temperatura_fase_s_ug{ug.id}"],
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"temperatura_fase_s_ug{ug.id}"])

        # Fase T
        self.leitura_dict[f"temperatura_fase_t_ug{ug.id}"] = LeituraModbus(
            f"[UG{ug.id}] Temperatura Fase T",
            self.clp_ug,
            UG[f"REG_UG{ug.id}_RetornosAnalogicos_MWR_Temperatura_03"],
            op=4
        )
        self.condic_dict[f"temperatura_fase_t_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"temperatura_fase_t_ug{ug.id}"].descr,
            CONDIC_INDISPONIBILIZAR,
            self.leitura_dict[f"temperatura_fase_t_ug{ug.id}"],
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"temperatura_fase_t_ug{ug.id}"])

        # Nucleo Gerador 1
        self.leitura_dict[f"temperatura_nucleo_gerador_1_ug{ug.id}"] = LeituraModbus(
            f"[UG{ug.id}] Temperatura Núcleo Gerador 1",
            self.clp_ug,
            UG[f"REG_UG{ug.id}_RetornosAnalogicos_MWR_Temperatura_04"],
            op=4
        )
        self.condic_dict[f"temperatura_nucleo_gerador_1_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"temperatura_nucleo_gerador_1_ug{ug.id}"].descr,
            CONDIC_INDISPONIBILIZAR,
            self.leitura_dict[f"temperatura_nucleo_gerador_1_ug{ug.id}"],
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"temperatura_nucleo_gerador_1_ug{ug.id}"])

        # Nucleo Gerador 2
        self.leitura_dict[f"temperatura_nucleo_gerador_2_ug{ug.id}"] = LeituraModbus(
            f"[UG{ug.id}] Temperatura Núcleo Gerador 2",
            self.clp_ug,
            UG[f"REG_UG{ug.id}_RetornosAnalogicos_MWR_Temperatura_04"],
            op=4
        )
        self.condic_dict[f"temperatura_nucleo_gerador_2_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"temperatura_nucleo_gerador_2_ug{ug.id}"].descr,
            CONDIC_INDISPONIBILIZAR,
            self.leitura_dict[f"temperatura_nucleo_gerador_2_ug{ug.id}"],
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"temperatura_nucleo_gerador_2_ug{ug.id}"])

        # Nucleo Gerador 3
        self.leitura_dict[f"temperatura_nucleo_gerador_3_ug{ug.id}"] = LeituraModbus(
            f"[UG{ug.id}] Temperatura Núcleo Gerador 3",
            self.clp_ug,
            UG[f"REG_UG{ug.id}_RetornosAnalogicos_MWR_Temperatura_04"],
            op=4
        )
        self.condic_dict[f"temperatura_nucleo_gerador_3_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"temperatura_nucleo_gerador_3_ug{ug.id}"].descr,
            CONDIC_INDISPONIBILIZAR,
            self.leitura_dict[f"temperatura_nucleo_gerador_3_ug{ug.id}"],
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"temperatura_nucleo_gerador_3_ug{ug.id}"])

        # Mancal Casquilho Radial
        self.leitura_dict[f"temperatura_mancal_casq_rad_ug{ug.id}"] = LeituraModbus(
            f"[UG{ug.id}] Temperatura Mancal Casquilho Radial",
            self.clp_ug,
            UG[f"REG_UG{ug.id}_RetornosAnalogicos_MWR_Temperatura_08"],
            op=4
        )
        self.condic_dict[f"temperatura_mancal_casq_rad_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"temperatura_mancal_casq_rad_ug{ug.id}"].descr,
            CONDIC_INDISPONIBILIZAR,
            self.leitura_dict[f"temperatura_mancal_casq_rad_ug{ug.id}"],
            self._temperatura_base,
            self._temperatura_limite,
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"temperatura_mancal_casq_rad_ug{ug.id}"])

        # Mancal Casquilho Combinado
        self.leitura_dict[f"temperatura_mancal_casq_comb_ug{ug.id}"] = LeituraModbus(
            f"[UG{ug.id}] Temperatura Mancal Casquilho Combinado",
            self.clp_ug,
            UG[f"REG_UG{ug.id}_RetornosAnalogicos_MWR_Temperatura_10"],
            op=4
        )
        self.condic_dict[f"temperatura_mancal_casq_comb_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"temperatura_mancal_casq_comb_ug{ug.id}"].descr,
            CONDIC_INDISPONIBILIZAR,
            self.leitura_dict[f"temperatura_mancal_casq_comb_ug{ug.id}"],
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"temperatura_mancal_casq_comb_ug{ug.id}"])

        # Mancal Escora Combinado
        self.leitura_dict[f"temperatura_mancal_escora_comb_ug{ug.id}"] = LeituraModbus(
            f"[UG{ug.id}] Temperatura Mancal Escora Combinado",
            self.clp_ug,
            UG[f"REG_UG{ug.id}_RetornosAnalogicos_MWR_Temperatura_07"],
            op=4
        )
        self.condic_dict[f"temperatura_mancal_escora_comb_ug{ug.id}"] = CondicionadorExponencial(
            self.leitura_dict[f"temperatura_mancal_escora_comb_ug{ug.id}"].descr,
            CONDIC_INDISPONIBILIZAR,
            self.leitura_dict[f"temperatura_mancal_escora_comb_ug{ug.id}"],
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"temperatura_mancal_escora_comb_ug{ug.id}"])

        # CX Espiral
        self.leitura_dict[f"caixa_espiral_ug{ug.id}"] = LeituraModbus(
            f"[UG{ug.id}] Pressão Caixa espiral",
            self.clp_ug[f"ug{ug.id}"],
            UG[f"REG_UG{ug.id}_EntradasAnalogicas_MRR_PressK1CaixaExpiral_MaisCasas"],
            escala=0.1,
            op=4
        )
        self.condic_dict[f"caixa_espiral_ug{ug.id}"] = CondicionadorExponencialReverso(
            self.leitura_dict[f"caixa_espiral_ug{ug.id}"].descr,
            CONDIC_INDISPONIBILIZAR,
            self.leitura_dict[f"caixa_espiral_ug{ug.id}"],
            self._pressao_caixa_base,
            self._pressao_caixa_limite
        )
        self.condicionadores_essenciais.append(self.condic_dict[f"caixa_espiral_ug{ug.id}"])
        self.condicionadores_atenuadores.append(self.condic_dict[f"caixa_espiral_ug{ug.id}"])

        leitura_ComandosDigitais_MXW_EmergenciaViaSuper = LeituraModbusCoil("ComandosDigitais_MXW_EmergenciaViaSuper", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_ComandosDigitais_MXW_EmergenciaViaSuper"],)
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ComandosDigitais_MXW_EmergenciaViaSuper.descr, CONDIC_NORMALIZAR, leitura_ComandosDigitais_MXW_EmergenciaViaSuper, ug.id, [UG_SINCRONIZADA, UG_SINCRONIZANDO]))

        leitura_RetornosDigitais_MXR_TripEletrico = LeituraModbusCoil("RetornosDigitais_MXR_TripEletrico", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripEletrico"],)
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_RetornosDigitais_MXR_TripEletrico.descr, CONDIC_NORMALIZAR, leitura_RetornosDigitais_MXR_TripEletrico, ug.id, [UG_SINCRONIZADA, UG_SINCRONIZANDO]))

        leitura_ReleBloqA86MAtuado = LeituraModbusCoil("ReleBloqA86MAtuado", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_ReleBloqA86MAtuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ReleBloqA86MAtuado.descr, CONDIC_INDISPONIBILIZAR, leitura_ReleBloqA86MAtuado))

        leitura_ReleBloqA86HAtuado = LeituraModbusCoil("ReleBloqA86HAtuado", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_ReleBloqA86HAtuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_ReleBloqA86HAtuado.descr, CONDIC_NORMALIZAR, leitura_ReleBloqA86HAtuado, ug.id, [UG_SINCRONIZADA, UG_SINCRONIZANDO]))

        leitura_SEL700G_Atuado = LeituraModbusCoil("SEL700G_Atuado", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_SEL700G_Atuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_SEL700G_Atuado.descr, CONDIC_INDISPONIBILIZAR, leitura_SEL700G_Atuado))

        leitura_RV_Trip = LeituraModbusCoil("RV_Trip", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_RV_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_RV_Trip.descr, CONDIC_INDISPONIBILIZAR, leitura_RV_Trip))

        leitura_RetornosDigitais_MXR_TripMecanico = LeituraModbusCoil("RetornosDigitais_MXR_TripMecanico", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripMecanico"],)
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_RetornosDigitais_MXR_TripMecanico.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripMecanico))

        leitura_RetornosDigitais_MXR_700G_Trip = LeituraModbusCoil("RetornosDigitais_MXR_700G_Trip", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_700G_Trip"],) 
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_RetornosDigitais_MXR_700G_Trip.descr, CONDIC_NORMALIZAR, leitura_RetornosDigitais_MXR_700G_Trip, ug.id, [UG_SINCRONIZADA, UG_SINCRONIZANDO]))

        leitura_AVR_Trip = LeituraModbusCoil("AVR_Trip", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_AVR_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(leitura_AVR_Trip.descr, CONDIC_INDISPONIBILIZAR, leitura_AVR_Trip))

        leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG1 = LeituraModbusCoil("SA_FalhaDisjTPsSincrG1",self.clp_usn,SA["REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG1"],)
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG1.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG1))

        leitura_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa = LeituraModbusCoil("SA_DisjDJ1_BloqPressBaixa",self.clp_usn,SA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa"],)
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa))

        leitura_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa = LeituraModbusCoil("SA_DisjDJ1_AlPressBaixa",self.clp_usn,SA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa"],)
        self.condicionadores.append(CondicionadorBase(leitura_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa))

        leitura_EntradasDigitais_MXI_ValvBorbTravada = LeituraModbusCoil("MXI_ValvBorbTravada", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_ValvBorbTravada"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_ValvBorbTravada.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_ValvBorbTravada) )

        leitura_EntradasDigitais_MXI_UHRV_TripBomba2 = LeituraModbusCoil("UHRV_TripBomba2", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHRV_TripBomba2"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHRV_TripBomba2.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHRV_TripBomba2) )

        leitura_EntradasDigitais_MXI_UHRV_TripBomba1 = LeituraModbusCoil("UHRV_TripBomba1", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHRV_TripBomba1"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHRV_TripBomba1.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHRV_TripBomba1) )

        leitura_EntradasDigitais_MXI_UHRV_NivOleominimoPos36 = LeituraModbusCoil("UHRV_NivOleominimoPos36", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHRV_NivOleominimoPos36"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHRV_NivOleominimoPos36.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHRV_NivOleominimoPos36) )

        leitura_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35 = LeituraModbusCoil("UHRV_NivOleoCriticoPos35", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35) )

        leitura_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo = LeituraModbusCoil("UHLM_Filt2PresSujo100Sujo", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo) )

        leitura_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo = LeituraModbusCoil("UHLM_Filt1PresSujo100Sujo", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo) )

        leitura_EntradasDigitais_MXI_UHLM_TripBomba2 = LeituraModbusCoil("UHLM_TripBomba2", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_TripBomba2"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_TripBomba2.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_TripBomba2) )

        leitura_EntradasDigitais_MXI_UHLM_TripBomba1 = LeituraModbusCoil("UHLM_TripBomba1", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_TripBomba1"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_TripBomba1.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_TripBomba1) )

        leitura_EntradasDigitais_MXI_UHLM_NivelminOleo = LeituraModbusCoil("UHLM_NivelminOleo", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_NivelminOleo"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_NivelminOleo.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_NivelminOleo) )

        leitura_EntradasDigitais_MXI_UHLM_NivelCritOleo = LeituraModbusCoil("UHLM_NivelCritOleo", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_NivelCritOleo"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_NivelCritOleo.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_NivelCritOleo) )

        leitura_EntradasDigitais_MXI_UHLM_FluxoMcTras = LeituraModbusCoil("UHLM_FluxoMcTras", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_FluxoMcTras"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_FluxoMcTras.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_FluxoMcTras) )

        leitura_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro = LeituraModbusCoil("UHLM_FluxoMcDianteiro", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro) )

        leitura_EntradasDigitais_MXI_UHLM_FaltaPressTroc = LeituraModbusCoil("UHLM_FaltaPressTroc", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_FaltaPressTroc"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_FaltaPressTroc.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_FaltaPressTroc) )

        leitura_EntradasDigitais_MXI_UHLM_FaltaFluxTroc = LeituraModbusCoil("UHLM_FaltaFluxTroc", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_UHLM_FaltaFluxTroc"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_UHLM_FaltaFluxTroc.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_UHLM_FaltaFluxTroc) )

        leitura_EntradasDigitais_MXI_TripAlimPainelFreio = LeituraModbusCoil("TripAlimPainelFreio", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_TripAlimPainelFreio"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_TripAlimPainelFreio.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_TripAlimPainelFreio) )

        leitura_EntradasDigitais_MXI_SobreVeloMecPos18 = LeituraModbusCoil("SobreVeloMecPos18", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_SobreVeloMecPos18"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_SobreVeloMecPos18.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SobreVeloMecPos18) )

        leitura_EntradasDigitais_MXI_SEL700G_FalhaInterna = LeituraModbusCoil("SEL700G_FalhaInterna", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_SEL700G_FalhaInterna"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_SEL700G_FalhaInterna.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_SEL700G_FalhaInterna) )

        leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2 = LeituraModbusCoil("UHRV_FalhaAcionBbaM2", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2) )

        leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1 = LeituraModbusCoil("UHRV_FalhaAcionBbaM1", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1) )

        leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2 = LeituraModbusCoil("UHLM_FalhaAcionBbaM2", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2) )

        leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1 = LeituraModbusCoil("UHLM_FalhaAcionBbaM1", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1) )

        leitura_RetornosDigitais_MXR_TripVibr2 = LeituraModbusCoil("TripVibr2", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripVibr2"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripVibr2.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripVibr2) )

        leitura_RetornosDigitais_MXR_TripVibr1 = LeituraModbusCoil("TripVibr1", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripVibr1"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripVibr1.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripVibr1) )

        leitura_RetornosDigitais_MXR_TripTempUHRV = LeituraModbusCoil("TripTempUHRV", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripTempUHRV"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripTempUHRV.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripTempUHRV) )

        leitura_RetornosDigitais_MXR_TripTempUHLM = LeituraModbusCoil("TripTempUHLM", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripTempUHLM"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripTempUHLM.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripTempUHLM) )

        leitura_RetornosDigitais_MXR_TripTempMcGuiaRadial = LeituraModbusCoil("TripTempMcGuiaRadial", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripTempMcGuiaRadial"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripTempMcGuiaRadial.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripTempMcGuiaRadial) )

        leitura_RetornosDigitais_MXR_TripTempMcGuiaEscora = LeituraModbusCoil("TripTempMcGuiaEscora", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripTempMcGuiaEscora"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripTempMcGuiaEscora.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripTempMcGuiaEscora) )

        leitura_RetornosDigitais_MXR_TripTempMcGuiaContraEscora = LeituraModbusCoil("TripTempMcGuiaContraEscora", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripTempMcGuiaContraEscora"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripTempMcGuiaContraEscora.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripTempMcGuiaContraEscora) )

        leitura_RetornosDigitais_MXR_TripTempGaxeteiro = LeituraModbusCoil("TripTempGaxeteiro", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_TripTempGaxeteiro"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_TripTempGaxeteiro.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_TripTempGaxeteiro) )

        leitura_RetornosDigitais_MXR_Q_Negativa = LeituraModbusCoil("Q_Negativa", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_Q_Negativa"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_Q_Negativa.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_Q_Negativa) )

        leitura_RetornosDigitais_MXR_FalhaIbntDisjGer = LeituraModbusCoil("FalhaIbntDisjGer", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_FalhaIbntDisjGer"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_FalhaIbntDisjGer.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_FalhaIbntDisjGer) )

        leitura_RetornosDigitais_MXR_FalhaAcionFechaValvBorb = LeituraModbusCoil("FalhaAcionFechaValvBorb", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_FalhaAcionFechaValvBorb"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_FalhaAcionFechaValvBorb.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_FalhaAcionFechaValvBorb) )

        leitura_RetornosDigitais_MXR_CLP_Falha = LeituraModbusCoil("CLP_Falha", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_CLP_Falha"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_CLP_Falha.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_CLP_Falha) )

        leitura_RetornosDigitais_MXR_Remota_Falha = LeituraModbusCoil("Remota_Falha", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_RetornosDigitais_MXR_Remota_Falha"], )
        self.condicionadores.append( CondicionadorBase(leitura_RetornosDigitais_MXR_Remota_Falha.descr, CONDIC_INDISPONIBILIZAR, leitura_RetornosDigitais_MXR_Remota_Falha) )

        leitura_EntradasDigitais_MXI_QCAUG_TripDisjAgrup = LeituraModbusCoil("QCAUG_TripDisjAgrup", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_QCAUG_TripDisjAgrup"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_QCAUG_TripDisjAgrup.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_QCAUG_TripDisjAgrup) )

        leitura_EntradasDigitais_MXI_QCAUG_TripDisj52A1 = LeituraModbusCoil("QCAUG_TripDisj52A1", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_QCAUG_TripDisj52A1"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_QCAUG_TripDisj52A1.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_QCAUG_TripDisj52A1) )

        leitura_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel = LeituraModbusCoil("QCAUG_Falha380VcaPainel", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel.descr, CONDIC_NORMALIZAR, leitura_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel) )

        leitura_EntradasDigitais_MXI_PalhetasDesal = LeituraModbusCoil("PalhetasDesal", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_PalhetasDesal"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_PalhetasDesal.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_PalhetasDesal) )

        leitura_EntradasDigitais_MXI_NivelMAltoPocoDren = LeituraModbusCoil("NivelMAltoPocoDren", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_NivelMAltoPocoDren"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_NivelMAltoPocoDren.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_NivelMAltoPocoDren) )

        leitura_EntradasDigitais_MXI_FreioSemEnergia = LeituraModbusCoil("FreioSemEnergia", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FreioSemEnergia"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_FreioSemEnergia.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_FreioSemEnergia) )

        leitura_EntradasDigitais_MXI_FreioFiltroSaturado = LeituraModbusCoil("FreioFiltroSaturado", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FreioFiltroSaturado"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_FreioFiltroSaturado.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_FreioFiltroSaturado) )

        leitura_EntradasDigitais_MXI_FiltroRetSujo100Sujo = LeituraModbusCoil("FiltroRetSujo100Sujo", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FiltroRetSujo100Sujo"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_FiltroRetSujo100Sujo.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_FiltroRetSujo100Sujo) )

        leitura_EntradasDigitais_MXI_FiltroPresSujo100Sujo = LeituraModbusCoil("FiltroPresSujo100Sujo", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FiltroPresSujo100Sujo"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_FiltroPresSujo100Sujo.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_FiltroPresSujo100Sujo) )

        leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100 = LeituraModbusCoil("FiltroPressaoBbaMecSj100", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100) )

        leitura_EntradasDigitais_MXI_FaltaFluxoOleoMc = LeituraModbusCoil("FaltaFluxoOleoMc", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FaltaFluxoOleoMc"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_FaltaFluxoOleoMc.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_FaltaFluxoOleoMc) )

        leitura_EntradasDigitais_MXI_Falta125VccCom = LeituraModbusCoil("Falta125VccCom", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_Falta125VccCom"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_Falta125VccCom.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_Falta125VccCom) )

        leitura_EntradasDigitais_MXI_Falta125VccAlimVal = LeituraModbusCoil("Falta125VccAlimVal", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_Falta125VccAlimVal"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_Falta125VccAlimVal.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_Falta125VccAlimVal) )

        leitura_EntradasDigitais_MXI_Falta125Vcc = LeituraModbusCoil("Falta125Vcc", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_Falta125Vcc"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_Falta125Vcc.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_Falta125Vcc) )

        leitura_EntradasDigitais_MXI_FalhaDisjTpsProt = LeituraModbusCoil("FalhaDisjTpsProt", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_FalhaDisjTpsProt"] )
        self.condicionadores.append( CondicionadorBase(leitura_EntradasDigitais_MXI_FalhaDisjTpsProt.descr, CONDIC_INDISPONIBILIZAR, leitura_EntradasDigitais_MXI_FalhaDisjTpsProt) )

        leitura_AVR_EntradasDigitais_MXI_FalhaInterna = LeituraModbusCoil("AVR_FalhaInterna", self.clp_ug[f"ug{ug.id}"], UG[f"REG_UG{ug.id}_EntradasDigitais_MXI_AVR_FalhaInterna"] )
        self.condicionadores.append( CondicionadorBase(leitura_AVR_EntradasDigitais_MXI_FalhaInterna.descr, CONDIC_INDISPONIBILIZAR, leitura_AVR_EntradasDigitais_MXI_FalhaInterna) )