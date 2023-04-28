from src.UnidadeDeGeracao import *

logger = logging.getLogger("__main__")

class UnidadeDeGeracao1(UnidadeDeGeracao):
    def __init__(self, id, cfg, clp, db, con):
        super().__init__(id, cfg, clp, db, con)

        ### CONDICIONADORES NORMAIS
        self.leitura_ED_SA_FalhaDisjTPsSincrG1 = LeituraModbusCoil("ED_SA_FalhaDisjTPsSincrG1",self.clp["SA"],REG_SA_ED_SA_FalhaDisjTPsSincrG1,)
        x = self.leitura_ED_SA_FalhaDisjTPsSincrG1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SA_DisjDJ1_BloqPressBaixa = LeituraModbusCoil("ED_SA_DisjDJ1_BloqPressBaixa",self.clp["SA"],REG_SA_ED_SA_DisjDJ1_BloqPressBaixa,)
        x = self.leitura_ED_SA_DisjDJ1_BloqPressBaixa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SA_DisjDJ1_AlPressBaixa = LeituraModbusCoil("ED_SA_DisjDJ1_AlPressBaixa",self.clp["SA"],REG_SA_ED_SA_DisjDJ1_AlPressBaixa,)
        x = self.leitura_ED_SA_DisjDJ1_AlPressBaixa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_ValvBorbTravada = LeituraModbusCoil( "ED_ValvBorbTravada", self.clp["UG1"], REG_UG1_ED_ValvBorbTravada )
        x = self.leitura_ED_ValvBorbTravada
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_UHRV_TripBomba2 = LeituraModbusCoil( "ED_UHRV_TripBomba2", self.clp["UG1"], REG_UG1_ED_UHRV_TripBomba2 )
        x = self.leitura_ED_UHRV_TripBomba2
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_UHRV_TripBomba1 = LeituraModbusCoil( "ED_UHRV_TripBomba1", self.clp["UG1"], REG_UG1_ED_UHRV_TripBomba1 )
        x = self.leitura_ED_UHRV_TripBomba1
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_UHRV_NivOleominimoPos36 = LeituraModbusCoil( "ED_UHRV_NivOleominimoPos36", self.clp["UG1"], REG_UG1_ED_UHRV_NivOleominimoPos36 )
        x = self.leitura_ED_UHRV_NivOleominimoPos36
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_UHRV_NivOleoCriticoPos35 = LeituraModbusCoil( "ED_UHRV_NivOleoCriticoPos35", self.clp["UG1"], REG_UG1_ED_UHRV_NivOleoCriticoPos35 )
        x = self.leitura_ED_UHRV_NivOleoCriticoPos35
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_UHLM_Filt2PresSujo100Sujo = LeituraModbusCoil( "ED_UHLM_Filt2PresSujo100Sujo", self.clp["UG1"], REG_UG1_ED_UHLM_Filt2PresSujo100Sujo )
        x = self.leitura_ED_UHLM_Filt2PresSujo100Sujo
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_UHLM_Filt1PresSujo100Sujo = LeituraModbusCoil( "ED_UHLM_Filt1PresSujo100Sujo", self.clp["UG1"], REG_UG1_ED_UHLM_Filt1PresSujo100Sujo )
        x = self.leitura_ED_UHLM_Filt1PresSujo100Sujo
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_UHLM_TripBomba2 = LeituraModbusCoil( "ED_UHLM_TripBomba2", self.clp["UG1"], REG_UG1_ED_UHLM_TripBomba2 )
        x = self.leitura_ED_UHLM_TripBomba2
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_UHLM_TripBomba1 = LeituraModbusCoil( "ED_UHLM_TripBomba1", self.clp["UG1"], REG_UG1_ED_UHLM_TripBomba1 )
        x = self.leitura_ED_UHLM_TripBomba1
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_UHLM_NivelminOleo = LeituraModbusCoil( "ED_UHLM_NivelminOleo", self.clp["UG1"], REG_UG1_ED_UHLM_NivelminOleo )
        x = self.leitura_ED_UHLM_NivelminOleo
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_UHLM_NivelCritOleo = LeituraModbusCoil( "ED_UHLM_NivelCritOleo", self.clp["UG1"], REG_UG1_ED_UHLM_NivelCritOleo )
        x = self.leitura_ED_UHLM_NivelCritOleo
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_UHLM_FluxoMcTras = LeituraModbusCoil( "ED_UHLM_FluxoMcTras", self.clp["UG1"], REG_UG1_ED_UHLM_FluxoMcTras )
        x = self.leitura_ED_UHLM_FluxoMcTras
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_UHLM_FluxoMcDianteiro = LeituraModbusCoil( "ED_UHLM_FluxoMcDianteiro", self.clp["UG1"], REG_UG1_ED_UHLM_FluxoMcDianteiro )
        x = self.leitura_ED_UHLM_FluxoMcDianteiro
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_UHLM_FaltaPressTroc = LeituraModbusCoil( "ED_UHLM_FaltaPressTroc", self.clp["UG1"], REG_UG1_ED_UHLM_FaltaPressTroc )
        x = self.leitura_ED_UHLM_FaltaPressTroc
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_UHLM_FaltaFluxTroc = LeituraModbusCoil( "ED_UHLM_FaltaFluxTroc", self.clp["UG1"], REG_UG1_ED_UHLM_FaltaFluxTroc )
        x = self.leitura_ED_UHLM_FaltaFluxTroc
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_TripAlimPainelFreio = LeituraModbusCoil( "ED_TripAlimPainelFreio", self.clp["UG1"], REG_UG1_ED_TripAlimPainelFreio )
        x = self.leitura_ED_TripAlimPainelFreio
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SobreVeloMecPos18 = LeituraModbusCoil( "ED_SobreVeloMecPos18", self.clp["UG1"], REG_UG1_ED_SobreVeloMecPos18 )
        x = self.leitura_ED_SobreVeloMecPos18
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SEL700G_FalhaInterna = LeituraModbusCoil( "ED_SEL700G_FalhaInterna", self.clp["UG1"], REG_UG1_ED_SEL700G_FalhaInterna )
        x = self.leitura_ED_SEL700G_FalhaInterna
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_UHRV_FalhaAcionBbaM2 = LeituraModbusCoil( "RD_UHRV_FalhaAcionBbaM2", self.clp["UG1"], REG_UG1_RD_UHRV_FalhaAcionBbaM2, )
        x = self.leitura_RD_UHRV_FalhaAcionBbaM2
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_UHRV_FalhaAcionBbaM1 = LeituraModbusCoil( "RD_UHRV_FalhaAcionBbaM1", self.clp["UG1"], REG_UG1_RD_UHRV_FalhaAcionBbaM1, )
        x = self.leitura_RD_UHRV_FalhaAcionBbaM1
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_UHLM_FalhaAcionBbaM2 = LeituraModbusCoil( "RD_UHLM_FalhaAcionBbaM2", self.clp["UG1"], REG_UG1_RD_UHLM_FalhaAcionBbaM2, )
        x = self.leitura_RD_UHLM_FalhaAcionBbaM2
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_UHLM_FalhaAcionBbaM1 = LeituraModbusCoil( "RD_UHLM_FalhaAcionBbaM1", self.clp["UG1"], REG_UG1_RD_UHLM_FalhaAcionBbaM1, )
        x = self.leitura_RD_UHLM_FalhaAcionBbaM1
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_TripVibr2 = LeituraModbusCoil( "RD_TripVibr2", self.clp["UG1"], REG_UG1_RD_TripVibr2, )
        x = self.leitura_RD_TripVibr2
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_TripVibr1 = LeituraModbusCoil( "RD_TripVibr1", self.clp["UG1"], REG_UG1_RD_TripVibr1, )
        x = self.leitura_RD_TripVibr1
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_TripTempUHRV = LeituraModbusCoil( "RD_TripTempUHRV", self.clp["UG1"], REG_UG1_RD_TripTempUHRV, )
        x = self.leitura_RD_TripTempUHRV
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_TripTempUHLM = LeituraModbusCoil( "RD_TripTempUHLM", self.clp["UG1"], REG_UG1_RD_TripTempUHLM, )
        x = self.leitura_RD_TripTempUHLM
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_TripTempMcGuiaRadial = LeituraModbusCoil( "RD_TripTempMcGuiaRadial", self.clp["UG1"], REG_UG1_RD_TripTempMcGuiaRadial, )
        x = self.leitura_RD_TripTempMcGuiaRadial
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_TripTempMcGuiaEscora = LeituraModbusCoil( "RD_TripTempMcGuiaEscora", self.clp["UG1"], REG_UG1_RD_TripTempMcGuiaEscora, )
        x = self.leitura_RD_TripTempMcGuiaEscora
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_TripTempMcGuiaContraEscora = ( LeituraModbusCoil( "RD_TripTempMcGuiaContraEscora", self.clp["UG1"], REG_UG1_RD_TripTempMcGuiaContraEscora, ) )
        x = self.leitura_RD_TripTempMcGuiaContraEscora
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_TripTempGaxeteiro = LeituraModbusCoil( "RD_TripTempGaxeteiro", self.clp["UG1"], REG_UG1_RD_TripTempGaxeteiro, )
        x = self.leitura_RD_TripTempGaxeteiro
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_Q_Negativa = LeituraModbusCoil( "RD_Q_Negativa", self.clp["UG1"], REG_UG1_RD_Q_Negativa, )
        x = self.leitura_RD_Q_Negativa
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_FalhaIbntDisjGer = LeituraModbusCoil( "RD_FalhaIbntDisjGer", self.clp["UG1"], REG_UG1_RD_FalhaIbntDisjGer, )
        x = self.leitura_RD_FalhaIbntDisjGer
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_FalhaAcionFechaValvBorb = LeituraModbusCoil( "RD_FalhaAcionFechaValvBorb", self.clp["UG1"], REG_UG1_RD_FalhaAcionFechaValvBorb, )
        x = self.leitura_RD_FalhaAcionFechaValvBorb
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_CLP_Falha = LeituraModbusCoil( "RD_CLP_Falha", self.clp["UG1"], REG_UG1_RD_CLP_Falha, )
        x = self.leitura_RD_CLP_Falha
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_Remota_Falha = LeituraModbusCoil( "RD_Remota_Falha", self.clp["UG1"], REG_UG1_RD_Remota_Falha, )
        x = self.leitura_RD_Remota_Falha
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_QCAUG_TripDisjAgrup = LeituraModbusCoil( "ED_QCAUG_TripDisjAgrup", self.clp["UG1"], REG_UG1_ED_QCAUG_TripDisjAgrup )
        x = self.leitura_ED_QCAUG_TripDisjAgrup
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_QCAUG_TripDisj52A1 = LeituraModbusCoil( "ED_QCAUG_TripDisj52A1", self.clp["UG1"], REG_UG1_ED_QCAUG_TripDisj52A1 )
        x = self.leitura_ED_QCAUG_TripDisj52A1
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_QCAUG_Falha380VcaPainel = LeituraModbusCoil( "ED_QCAUG_Falha380VcaPainel", self.clp["UG1"], REG_UG1_ED_QCAUG_Falha380VcaPainel )
        x = self.leitura_ED_QCAUG_Falha380VcaPainel
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_NORMALIZAR, x) )

        self.leitura_ED_PalhetasDesal = LeituraModbusCoil( "ED_PalhetasDesal", self.clp["UG1"], REG_UG1_ED_PalhetasDesal )
        x = self.leitura_ED_PalhetasDesal
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_NivelMAltoPocoDren = LeituraModbusCoil( "ED_NivelMAltoPocoDren", self.clp["UG1"], REG_UG1_ED_NivelMAltoPocoDren )
        x = self.leitura_ED_NivelMAltoPocoDren
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_FreioSemEnergia = LeituraModbusCoil( "ED_FreioSemEnergia", self.clp["UG1"], REG_UG1_ED_FreioSemEnergia )
        x = self.leitura_ED_FreioSemEnergia
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_FreioFiltroSaturado = LeituraModbusCoil( "ED_FreioFiltroSaturado", self.clp["UG1"], REG_UG1_ED_FreioFiltroSaturado )
        x = self.leitura_ED_FreioFiltroSaturado
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_FiltroRetSujo100Sujo = LeituraModbusCoil( "ED_FiltroRetSujo100Sujo", self.clp["UG1"], REG_UG1_ED_FiltroRetSujo100Sujo )
        x = self.leitura_ED_FiltroRetSujo100Sujo
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_FiltroPresSujo100Sujo = LeituraModbusCoil( "ED_FiltroPresSujo100Sujo", self.clp["UG1"], REG_UG1_ED_FiltroPresSujo100Sujo )
        x = self.leitura_ED_FiltroPresSujo100Sujo
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_FiltroPressaoBbaMecSj100 = LeituraModbusCoil( "ED_FiltroPressaoBbaMecSj100", self.clp["UG1"], REG_UG1_ED_FiltroPressaoBbaMecSj100 )
        x = self.leitura_ED_FiltroPressaoBbaMecSj100
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_FaltaFluxoOleoMc = LeituraModbusCoil( "ED_FaltaFluxoOleoMc", self.clp["UG1"], REG_UG1_ED_FaltaFluxoOleoMc )
        x = self.leitura_ED_FaltaFluxoOleoMc
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_Falta125VccCom = LeituraModbusCoil( "ED_Falta125VccCom", self.clp["UG1"], REG_UG1_ED_Falta125VccCom )
        x = self.leitura_ED_Falta125VccCom
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_Falta125VccAlimVal = LeituraModbusCoil( "ED_Falta125VccAlimVal", self.clp["UG1"], REG_UG1_ED_Falta125VccAlimVal )
        x = self.leitura_ED_Falta125VccAlimVal
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_Falta125Vcc = LeituraModbusCoil( "ED_Falta125Vcc", self.clp["UG1"], REG_UG1_ED_Falta125Vcc )
        x = self.leitura_ED_Falta125Vcc
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_FalhaDisjTpsProt = LeituraModbusCoil( "ED_FalhaDisjTpsProt", self.clp["UG1"], REG_UG1_ED_FalhaDisjTpsProt )
        x = self.leitura_ED_FalhaDisjTpsProt
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_AVR_ED_FalhaInterna = LeituraModbusCoil( "ED_AVR_FalhaInterna", self.clp["UG1"], REG_UG1_ED_AVR_FalhaInterna )
        x = self.leitura_AVR_ED_FalhaInterna
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )