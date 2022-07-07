from time import sleep

itens_ug1 = [
    "ValvBorbTravada",
    "UHRV_TripBomba2",
    "UHRV_TripBomba1",
    "UHRV_PressCriticaPos321",
    "UHRV_NivOleominimoPos36",
    "UHRV_NivOleoCriticoPos35",
    "UHLMFilt2PresSujo100Sujo",
    "UHLMFilt1PresSujo100Sujo",
    "UHLM_TripBomba2",
    "UHLM_TripBomba1",
    "UHLM_NivelminOleo",
    "UHLM_NivelCritOleo",
    "UHLM_FluxoMcTras",
    "UHLM_FluxoMcDianteiro",
    "UHLM_FaltaPressTroc",
    "UHLM_FaltaFluxTroc",
    "TripAlimPainelFreio",
    "SobreVeloMecPos18",
    "SEL700G_FalhaInterna",
    "SEL700G_Atuado",
    "RV_Trip",
    "RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2",
    "RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1",
    "RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2",
    "RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1",
    "RetornosDigitais_MXR_UG1_StsBloqueio",
    "RetornosDigitais_MXR_TripVibr2",
    "RetornosDigitais_MXR_TripVibr1",
    "RetornosDigitais_MXR_TripTempUHRV",
    "RetornosDigitais_MXR_TripTempUHLM",
    "RetornosDigitais_MXR_TripTempMcGuiaRadial",
    "RetornosDigitais_MXR_TripTempMcGuiaEscora",
    "RetornosDigitais_MXR_TripTempMcGuiaContraEscora",
    "RetornosDigitais_MXR_TripTempGaxeteiro",
    "RetornosDigitais_MXR_TripMecanico",
    "RetornosDigitais_MXR_TripEletrico",
    "RetornosDigitais_MXR_Q_Negativa",
    "RetornosDigitais_MXR_FalhaIbntDisjGer",
    "RetornosDigitais_MXR_FalhaAcionFechaValvBorb",
    "RetornosDigitais_MXR_CLP_Falha",
    "RetornosDigitais_MXR_700G_Trip",
    "ReleBloqA86MAtuado",
    "ReleBloqA86HAtuado",
    "QCAUG_TripDisjAgrup",
    "QCAUG_TripDisj52A1",
    "QCAUG_Falha380VcaPainel",
    "PalhetasDesal",
    "NivelMAltoPocoDren",
    "FreioSemEnergia",
    "FreioFiltroSaturado",
    "FiltroRetSujo100Sujo",
    "FiltroPresSujo100Sujo",
    "FiltroPressaoBbaMecSj100",
    "FaltaFluxoOleoMc",
    "Falta125VccCom",
    "Falta125VccAlimVal",
    "Falta125Vcc",
    "FalhaDisjTpsProt",
    "AVR_Trip",
    "AVR_FalhaInterna",
]
itens_ug2 = [
    "EntradasDigitais_MXI_RV_Trip",
    "EntradasDigitais_MXI_AVR_Trip",
    "EntradasDigitais_MXI_AVR_FalhaInterna",
    "EntradasDigitais_MXI_Falta125Vcc",
    "EntradasDigitais_MXI_Falta125VccQPCUG1",
    "EntradasDigitais_MXI_Falta125VccAlimVal",
    "EntradasDigitais_MXI_FalhaDisjTpsProt",
    "EntradasDigitais_MXI_ReleBloqA86HAtuado",
    "EntradasDigitais_MXI_ReleBloqA86MAtuado",
    "EntradasDigitais_MXI_SEL700G_Atuado",
    "EntradasDigitais_MXI_SEL700G_FalhaInterna",
    "EntradasDigitais_MXI_NivelMAltoPocoDren",
    "EntradasDigitais_MXI_FreioFiltroSaturado",
    "EntradasDigitais_MXI_FreioSemEnergia",
    "EntradasDigitais_MXI_UHRV_PressCriticaPos321",
    "EntradasDigitais_MXI_FiltroPresSujo100Sujo",
    "EntradasDigitais_MXI_FiltroRetSujo100Sujo",
    "EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35",
    "EntradasDigitais_MXI_UHRV_NivOleominimoPos36",
    "EntradasDigitais_MXI_ValvBorbTravada",
    "EntradasDigitais_MXI_SobreVeloMecPos18",
    "EntradasDigitais_MXI_FaltaFluxoOleoMc",
    "EntradasDigitais_MXI_PalhetasDesal",
    "EntradasDigitais_MXI_UHLM_FaltaFluxTroc",
    "EntradasDigitais_MXI_UHLM_FaltaPressTroc",
    "EntradasDigitais_MXI_UHLMFilt1PresSujo100Sujo",
    "EntradasDigitais_MXI_UHLMFilt2PresSujo100Sujo",
    "EntradasDigitais_MXI_UHLM_NivelCritOleo",
    "EntradasDigitais_MXI_UHLM_NivelminOleo",
    "EntradasDigitais_MXI_FiltroPressaoBbaMecSj100",
    "EntradasDigitais_MXI_UHLM_FluxoMcDianteiro",
    "EntradasDigitais_MXI_UHLM_FluxoMcTras",
    "EntradasDigitais_MXI_QCAUG_Falha380VcaPainel",
    "EntradasDigitais_MXI_QCAUG_TripDisj52A1",
    "EntradasDigitais_MXI_UHLM_TripBomba1",
    "EntradasDigitais_MXI_UHLM_TripBomba2",
    "EntradasDigitais_MXI_UHRV_TripBomba1",
    "EntradasDigitais_MXI_UHRV_TripBomba2",
    "EntradasDigitais_MXI_TripAlimPainelFreio",
    "EntradasDigitais_MXI_QCAUG_TripDisjAgrup",
    "RetornosDigitais_MXR_TripEletrico",
    "RetornosDigitais_MXR_TripMecanico",
    "RetornosDigitais_MXR_FalhaAcionFechaValvBorb",
    "RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1",
    "RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2",
    "RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1",
    "RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2",
    "RetornosDigitais_MXR_TripTempGaxeteiro",
    "RetornosDigitais_MXR_TripTempMcGuiaRadial",
    "RetornosDigitais_MXR_TripTempMcGuiaEscora",
    "RetornosDigitais_MXR_TripTempMcGuiaContraEscora",
    "RetornosDigitais_MXR_TripTempUHRV",
    "RetornosDigitais_MXR_TripTempUHLM",
    "RetornosDigitais_MXR_TripVibr1",
    "RetornosDigitais_MXR_TripVibr2",
    "RetornosDigitais_MXR_FalhaIbntDisjGer",
    "RetornosDigitais_MXR_700G_Trip",
    "RetornosDigitais_MXR_CLP_Falha",
    "RetornosDigitais_MXR_Q_Negativa",
    "RetornosDigitais_MXR_UG2_StsBloqueio",
]
itens_ug3 = [
    "EntradasDigitais_MXI_RV_Trip",
    "EntradasDigitais_MXI_AVR_Trip",
    "EntradasDigitais_MXI_AVR_FalhaInterna",
    "EntradasDigitais_MXI_Falta125Vcc",
    "EntradasDigitais_MXI_Falta125VccCom",
    "EntradasDigitais_MXI_Falta125VccAlimVal",
    "EntradasDigitais_MXI_FalhaDisjTpsProt",
    "EntradasDigitais_MXI_ReleBloqA86HAtuado",
    "EntradasDigitais_MXI_ReleBloqA86MAtuado",
    "EntradasDigitais_MXI_SEL700G_Atuado",
    "EntradasDigitais_MXI_SEL700G_FalhaInterna",
    "EntradasDigitais_MXI_NivelMAltoPocoDren",
    "EntradasDigitais_MXI_FreioFiltroSaturado",
    "EntradasDigitais_MXI_FreioSemEnergia",
    "EntradasDigitais_MXI_UHRV_PressCriticaPos321",
    "EntradasDigitais_MXI_FiltroPresSujo100Sujo",
    "EntradasDigitais_MXI_FiltroRetSujo100Sujo",
    "EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35",
    "EntradasDigitais_MXI_UHRV_NivOleominimoPos36",
    "EntradasDigitais_MXI_ValvBorbTravada",
    "EntradasDigitais_MXI_SobreVeloMecPos18",
    "EntradasDigitais_MXI_FaltaFluxoOleoMc",
    "EntradasDigitais_MXI_PalhetasDesal",
    "EntradasDigitais_MXI_UHLM_FaltaFluxTroc",
    "EntradasDigitais_MXI_UHLM_FaltaPressTroc",
    "EntradasDigitais_MXI_UHLMFilt1PresSujo100Sujo",
    "EntradasDigitais_MXI_UHLMFilt2PresSujo100Sujo",
    "EntradasDigitais_MXI_UHLM_NivelCritOleo",
    "EntradasDigitais_MXI_UHLM_NivelminOleo",
    "EntradasDigitais_MXI_FiltroPressaoBbaMecSj100",
    "EntradasDigitais_MXI_UHLM_FluxoMcDianteiro",
    "EntradasDigitais_MXI_UHLM_FluxoMcTras",
    "EntradasDigitais_MXI_QCAUG_Falha380VcaPainel",
    "EntradasDigitais_MXI_QCAUG_TripDisj52A1",
    "EntradasDigitais_MXI_UHLM_TripBomba1",
    "EntradasDigitais_MXI_UHLM_TripBomba2",
    "EntradasDigitais_MXI_UHRV_TripBomba1",
    "EntradasDigitais_MXI_UHRV_TripBomba2",
    "EntradasDigitais_MXI_TripAlimPainelFreio",
    "EntradasDigitais_MXI_QCAUG_TripDisjAgrup",
    "RetornosDigitais_MXR_TripEletrico",
    "RetornosDigitais_MXR_TripMecanico",
    "RetornosDigitais_MXR_FalhaAcionFechaValvBorb",
    "RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1",
    "RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2",
    "RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1",
    "RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2",
    "RetornosDigitais_MXR_TripTempGaxeteiro",
    "RetornosDigitais_MXR_TripTempMcGuiaRadial",
    "RetornosDigitais_MXR_TripTempMcGuiaEscora",
    "RetornosDigitais_MXR_TripTempMcGuiaContraEscora",
    "RetornosDigitais_MXR_TripTempUHRV",
    "RetornosDigitais_MXR_TripTempUHLM",
    "RetornosDigitais_MXR_TripVibr1",
    "RetornosDigitais_MXR_TripVibr2",
    "RetornosDigitais_MXR_FalhaIbntDisjGer",
    "RetornosDigitais_MXR_700G_Trip",
    "RetornosDigitais_MXR_CLP_Falha",
    "RetornosDigitais_MXR_Q_Negativa",
    "RetornosDigitais_MXR_UG3_StsBloqueio",
]
itens_sa = [
    "EntradasDigitais_MXI_SA_SEL787_Trip",
    "EntradasDigitais_MXI_SA_SEL787_FalhaInterna",
    "EntradasDigitais_MXI_SA_SEL311_Trip",
    "EntradasDigitais_MXI_SA_SEL311_Falha",
    "EntradasDigitais_MXI_SA_MRU3_Trip",
    "EntradasDigitais_MXI_SA_MRU3_Falha",
    "EntradasDigitais_MXI_SA_MRL1_Trip",
    "EntradasDigitais_MXI_SA_CTE_Falta125Vcc",
    "EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta",
    "EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas",
    "EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo",
    "EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao",
    "EntradasDigitais_MXI_SA_TE_AlarmeTempOleo",
    "EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento",
    "EntradasDigitais_MXI_SA_TE_AlarmeDesligamento",
    "EntradasDigitais_MXI_SA_TE_Falha",
    "EntradasDigitais_MXI_SA_FalhaDisjTPsProt",
    "EntradasDigitais_MXI_SA_FalhaDisjTPsSincr",
    "EntradasDigitais_MXI_SA_CSA1_Secc_Aberta",
    "EntradasDigitais_MXI_SA_CSA1_FusivelQueimado",
    "EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc",
    "EntradasDigitais_MXI_SA_QCADE_Nivel4",
    "EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto",
    "EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip",
    "EntradasDigitais_MXI_SA_QCADE_Falha220VCA",
    "EntradasDigitais_MXI_SA_QCCP_Disj72ETrip",
    "EntradasDigitais_MXI_SA_QCCP_Falta125Vcc",
    "EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup",
    "EntradasDigitais_MXI_SA_QCAP_Falta125Vcc",
    "EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup",
    "EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha",
    "EntradasDigitais_MXI_SA_QCAP_Disj52EFalha",
    "EntradasDigitais_MXI_SA_GMG_DisjFechado",
    "RetornosAnalogicos_MWR_SEL787_Targets",
    "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00",
    "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01",
    "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02",
    "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03",
    "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04",
    "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05",
    "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06",
    "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07",
    "RetornosDigitais_MXR_DJ1_FalhaInt",
    "RetornosDigitais_MXR_CLP_Falha",
]


for i in itens_ug1:
    clp = "UG1"
    l = (
        """self.leitura_"""
        + i
        + """ = LeituraModbusCoil(\""""
        + i
        + """\", self.clp, REG_"""
        + clp
        + """_"""
        + i
        + """)
x = self.leitura_"""
        + i
        + """
self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
"""
    )
    # print(l)
    # sleep(0.01)

for i in itens_ug2:
    clp = "UG2"
    l = (
        """self.leitura_"""
        + i
        + """ = LeituraModbusCoil(\""""
        + i
        + """\", self.clp, REG_"""
        + clp
        + """_"""
        + i
        + """)
x = self.leitura_"""
        + i
        + """
self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
"""
    )
    # print(l)
    # sleep(0.01)

for i in itens_ug3:
    clp = "UG3"
    l = (
        """self.leitura_"""
        + i
        + """ = LeituraModbusCoil(\""""
        + i
        + """\", self.clp, REG_"""
        + clp
        + """_"""
        + i
        + """)
x = self.leitura_"""
        + i
        + """
self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
"""
    )
    # print(l)
    # sleep(0.01)

for i in itens_sa:
    clp = "SA"
    l = (
        """self.leitura_"""
        + i
        + """ = LeituraModbusCoil(\""""
        + i
        + """\", self.clp, REG_"""
        + clp
        + """_"""
        + i
        + """)
x = self.leitura_"""
        + i
        + """
self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
"""
    )
    print(l)
    sleep(0.01)
