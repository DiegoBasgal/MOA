#### APARENTEMENTE A MAIS ATUALIZADA EM CONDICIONADORES

from src.UnidadeDeGeracao import *

logger = logging.getLogger("__main__")

class UnidadeDeGeracao2(UnidadeDeGeracao):
    def __init__(self, id, cfg, clp, db, con):
        super().__init__(id, cfg, clp, db, con)

        # CX Espiral
        self.leitura_caixa_espiral = LeituraModbus("Caixa espiral", self.clp["UG2"], REG_UG2_EA_PressK1CaixaExpiral_MaisCasas, escala=0.01, op=4)
        self.condicionador_caixa_espiral_ug = CondicionadorExponencialReverso(self.leitura_caixa_espiral.descr, DEVE_INDISPONIBILIZAR, x, 16.5, 15.5)
        self.condicionadores_atenuadores.append(self.condicionador_caixa_espiral_ug)

        # Inicializa as variáveis de controle PI para operação TDA Offline
        self.cx_controle_p = (self.leitura_caixa_espiral.valor - self.cfg["press_cx_alvo"]) * self.cfg["cx_kp"]

        self.cx_ajuste_ie = (
            self.leituras_ug["leitura_potencia_ug1"].valor \
            + self.leituras_ug["leitura_potencia_ug2"].valor \
            + self.leituras_ug["leitura_potencia_ug3"].valor) \
            / self.cfg["pot_maxima_alvo"]

        self.cx_controle_i = self.cx_ajuste_ie - self.cx_controle_p


        ### CONDICIONADORES ESSENCIAIS
        # R
        self.leitura_temperatura_fase_R = LeituraModbus("Temperatura fase R",self.clp["UG2"],REG_UG2_RA_Temperatura_01,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_R
        self.condicionador_temperatura_fase_r_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_r_ug)

        # S
        self.leitura_temperatura_fase_S = LeituraModbus("Temperatura fase s",self.clp["UG2"],REG_UG2_RA_Temperatura_02,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_S
        self.condicionador_temperatura_fase_s_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_s_ug)

        # T
        self.leitura_temperatura_fase_T = LeituraModbus("Temperatura fase T",self.clp["UG2"],REG_UG2_RA_Temperatura_03,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_T
        self.condicionador_temperatura_fase_t_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_t_ug)

        # Nucleo estator
        self.leitura_temperatura_nucleo = LeituraModbus("Temperatura núcelo do estator",self.clp["UG2"],REG_UG2_RA_Temperatura_04,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_nucleo
        self.condicionador_temperatura_nucleo_estator_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_nucleo_estator_ug)

        # MRD 1
        self.leitura_temperatura_mrd1 = LeituraModbus("Temperatura mancal radial dianteiro",self.clp["UG2"],REG_UG2_RA_Temperatura_05,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_mrd1
        self.condicionador_temperatura_mancal_rad_dia_1_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_dia_1_ug)

        # MRT 1
        self.leitura_temperatura_mrt1 = LeituraModbus("Temperatura mancal radial traseiro",self.clp["UG2"],REG_UG2_RA_Temperatura_06,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_mrt1
        self.condicionador_temperatura_mancal_rad_tra_1_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_tra_1_ug)

        # MRD 2
        self.leitura_temperatura_mrd2 = LeituraModbus("Temperatura mancal radial dianteiro 2",self.clp["UG2"],REG_UG2_RA_Temperatura_07,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_mrd2
        self.condicionador_temperatura_mancal_rad_dia_2_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_dia_2_ug)

        # MRT 2
        self.leitura_temperatura_mrt2 = LeituraModbus("Temperatura mancal radial traseiro 2",self.clp["UG2"],REG_UG2_RA_Temperatura_08,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_mrt2
        self.condicionador_temperatura_mancal_rad_tra_2_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_tra_2_ug)

        # Saída de ar
        self.leitura_temperatura_saida_de_ar = LeituraModbus("Saída de ar",self.clp["UG2"],REG_UG2_RA_Temperatura_10,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_saida_de_ar
        self.condicionador_temperatura_saida_de_ar_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_saida_de_ar_ug)

        # Mancal Guia Radial
        self.leitura_temperatura_guia_radial = LeituraModbus("Mancal Guia Radial",self.clp["UG2"],REG_UG2_EA_TempMcGuiaRadial,)
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_radial
        self.condicionador_temperatura_mancal_guia_radial_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_radial_ug)

        # Mancal Guia escora
        self.leitura_temperatura_guia_escora = LeituraModbus("Mancal Guia escora",self.clp["UG2"],REG_UG2_EA_TempMcGuiaEscora,)
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_escora
        self.condicionador_temperatura_mancal_guia_escora_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_escora_ug)

        # Mancal Guia contra_escora
        self.leitura_temperatura_guia_contra_escora = LeituraModbus("Mancal Guia contra_escora",self.clp["UG2"],REG_UG2_EA_TempMcGuiaContraEscora,)
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_contra_escora
        self.condicionador_temperatura_mancal_guia_contra_ug = (CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite))
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_contra_ug)

        # Óleo do Transformador Elevador
        self.leitura_temperatura_oleo_trafo = LeituraModbus("Óleo do Transformador Elevador",self.clp["SA"],REG_SA_EA_SA_TE_TempOleo, escala=0.1, op=4)
        base = 100
        limite = 200
        escala = 0.1
        x = self.leitura_temperatura_oleo_trafo
        self.condicionador_leitura_temperatura_oleo_trafo = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_leitura_temperatura_oleo_trafo)

        self.leitura_CD_EmergenciaViaSuper = LeituraModbusCoil("CD_EmergenciaViaSuper", self.clp["UG2"], UG["REG_UG2_CD_EmergenciaViaSuper"],)
        x = self.leitura_CD_EmergenciaViaSuper
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_RD_TripEletrico = LeituraModbusCoil("RD_TripEletrico",self.clp["UG2"],REG_UG2_RD_TripEletrico,)
        x = self.leitura_RD_TripEletrico
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_ED_ReleBloqA86HAtuado = LeituraModbusCoil("ED_ReleBloqA86HAtuado", self.clp["UG2"], UG["REG_UG2_ED_ReleBloqA86HAtuado"])
        x = self.leitura_ED_ReleBloqA86HAtuado
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x, self.id, [UNIDADE_SINCRONIZADA]))

        self.leitura_ED_ReleBloqA86MAtuado = LeituraModbusCoil("ED_ReleBloqA86MAtuado", self.clp["UG2"], UG["REG_UG2_ED_ReleBloqA86MAtuado"])
        x = self.leitura_ED_ReleBloqA86MAtuado
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SEL700G_Atuado = LeituraModbusCoil("ED_SEL700G_Atuado",self.clp["UG2"],REG_UG2_ED_SEL700G_Atuado,)
        x = self.leitura_ED_SEL700G_Atuado
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_RV_Trip = LeituraModbusCoil("ED_RV_Trip",self.clp["UG2"],REG_UG2_ED_RV_Trip,)
        x = self.leitura_ED_RV_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripMecanico = LeituraModbusCoil("RD_TripMecanico",self.clp["UG2"],REG_UG2_RD_TripMecanico,)
        x = self.leitura_RD_TripMecanico
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_700G_Trip = LeituraModbusCoil("RD_700G_Trip",self.clp["UG2"], UG["REG_UG2_RD_700G_Trip"],)
        x = self.leitura_RD_700G_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x, self.id))

        self.leitura_ED_AVR_Trip = LeituraModbusCoil("ED_AVR_Trip",self.clp["UG2"],REG_UG2_ED_AVR_Trip,)
        x = self.leitura_ED_AVR_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))


        ### CONDICIONADORES NORMAIS
        self.leitura_ED_SA_FalhaDisjTPsSincrG2 = LeituraModbusCoil("ED_SA_FalhaDisjTPsSincrG2",self.clp["SA"],REG_SA_ED_SA_FalhaDisjTPsSincrG2,)
        x = self.leitura_ED_SA_FalhaDisjTPsSincrG2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SA_DisjDJ1_BloqPressBaixa = LeituraModbusCoil("ED_SA_DisjDJ1_BloqPressBaixa",self.clp["SA"],REG_SA_ED_SA_DisjDJ1_BloqPressBaixa,)
        x = self.leitura_ED_SA_DisjDJ1_BloqPressBaixa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SA_DisjDJ1_AlPressBaixa = LeituraModbusCoil("ED_SA_DisjDJ1_AlPressBaixa",self.clp["SA"],REG_SA_ED_SA_DisjDJ1_AlPressBaixa,)
        x = self.leitura_ED_SA_DisjDJ1_AlPressBaixa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_AVR_FalhaInterna = LeituraModbusCoil("ED_AVR_FalhaInterna",self.clp["UG2"],REG_UG2_ED_AVR_FalhaInterna,)
        x = self.leitura_ED_AVR_FalhaInterna
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_Falta125Vcc = LeituraModbusCoil("ED_Falta125Vcc",self.clp["UG2"],REG_UG2_ED_Falta125Vcc,)
        x = self.leitura_ED_Falta125Vcc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_Falta125VccAlimVal = LeituraModbusCoil("ED_Falta125VccAlimVal",self.clp["UG2"],REG_UG2_ED_Falta125VccAlimVal,)
        x = self.leitura_ED_Falta125VccAlimVal
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FalhaDisjTpsProt = LeituraModbusCoil("ED_FalhaDisjTpsProt",self.clp["UG2"],REG_UG2_ED_FalhaDisjTpsProt,)
        x = self.leitura_ED_FalhaDisjTpsProt
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SEL700G_FalhaInterna = LeituraModbusCoil("ED_SEL700G_FalhaInterna",self.clp["UG2"],REG_UG2_ED_SEL700G_FalhaInterna,)
        x = self.leitura_ED_SEL700G_FalhaInterna
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_NivelMAltoPocoDren = LeituraModbusCoil("ED_NivelMAltoPocoDren",self.clp["UG2"],REG_UG2_ED_NivelMAltoPocoDren,)
        x = self.leitura_ED_NivelMAltoPocoDren
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FreioFiltroSaturado = LeituraModbusCoil("ED_FreioFiltroSaturado",self.clp["UG2"],REG_UG2_ED_FreioFiltroSaturado,)
        x = self.leitura_ED_FreioFiltroSaturado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FreioSemEnergia = LeituraModbusCoil("ED_FreioSemEnergia",self.clp["UG2"],REG_UG2_ED_FreioSemEnergia,)
        x = self.leitura_ED_FreioSemEnergia
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FiltroPresSujo100Sujo = LeituraModbusCoil("ED_FiltroPresSujo100Sujo",self.clp["UG2"],REG_UG2_ED_FiltroPresSujo100Sujo,)
        x = self.leitura_ED_FiltroPresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FiltroRetSujo100Sujo = LeituraModbusCoil("ED_FiltroRetSujo100Sujo",self.clp["UG2"],REG_UG2_ED_FiltroRetSujo100Sujo,)
        x = self.leitura_ED_FiltroRetSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHRV_NivOleoCriticoPos35 = LeituraModbusCoil("ED_UHRV_NivOleoCriticoPos35",self.clp["UG2"],REG_UG2_ED_UHRV_NivOleoCriticoPos35,)
        x = self.leitura_ED_UHRV_NivOleoCriticoPos35
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHRV_NivOleominimoPos36 = LeituraModbusCoil("ED_UHRV_NivOleominimoPos36",self.clp["UG2"],REG_UG2_ED_UHRV_NivOleominimoPos36,)
        x = self.leitura_ED_UHRV_NivOleominimoPos36
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_ValvBorbTravada = LeituraModbusCoil("ED_ValvBorbTravada",self.clp["UG2"],REG_UG2_ED_ValvBorbTravada,)
        x = self.leitura_ED_ValvBorbTravada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SobreVeloMecPos18 = LeituraModbusCoil("ED_SobreVeloMecPos18",self.clp["UG2"],REG_UG2_ED_SobreVeloMecPos18,)
        x = self.leitura_ED_SobreVeloMecPos18
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FaltaFluxoOleoMc = LeituraModbusCoil("ED_FaltaFluxoOleoMc",self.clp["UG2"],REG_UG2_ED_FaltaFluxoOleoMc,)
        x = self.leitura_ED_FaltaFluxoOleoMc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_PalhetasDesal = LeituraModbusCoil("ED_PalhetasDesal",self.clp["UG2"],REG_UG2_ED_PalhetasDesal,)
        x = self.leitura_ED_PalhetasDesal
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_FaltaFluxTroc = LeituraModbusCoil("ED_UHLM_FaltaFluxTroc",self.clp["UG2"],REG_UG2_ED_UHLM_FaltaFluxTroc,)
        x = self.leitura_ED_UHLM_FaltaFluxTroc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_FaltaPressTroc = LeituraModbusCoil("ED_UHLM_FaltaPressTroc",self.clp["UG2"],REG_UG2_ED_UHLM_FaltaPressTroc,)
        x = self.leitura_ED_UHLM_FaltaPressTroc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_Filt1PresSujo100Sujo = LeituraModbusCoil("ED_UHLM_Filt1PresSujo100Sujo",self.clp["UG2"],REG_UG2_ED_UHLM_Filt1PresSujo100Sujo,)
        x = self.leitura_ED_UHLM_Filt1PresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_Filt2PresSujo100Sujo = LeituraModbusCoil("ED_UHLM_Filt2PresSujo100Sujo",self.clp["UG2"],REG_UG2_ED_UHLM_Filt2PresSujo100Sujo,)
        x = self.leitura_ED_UHLM_Filt2PresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_NivelCritOleo = LeituraModbusCoil("ED_UHLM_NivelCritOleo",self.clp["UG2"],REG_UG2_ED_UHLM_NivelCritOleo,)
        x = self.leitura_ED_UHLM_NivelCritOleo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_NivelminOleo = LeituraModbusCoil("ED_UHLM_NivelminOleo",self.clp["UG2"],REG_UG2_ED_UHLM_NivelminOleo,)
        x = self.leitura_ED_UHLM_NivelminOleo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FiltroPressaoBbaMecSj100 = LeituraModbusCoil("ED_FiltroPressaoBbaMecSj100",self.clp["UG2"],REG_UG2_ED_FiltroPressaoBbaMecSj100,)
        x = self.leitura_ED_FiltroPressaoBbaMecSj100
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_FluxoMcDianteiro = LeituraModbusCoil("ED_UHLM_FluxoMcDianteiro",self.clp["UG2"],REG_UG2_ED_UHLM_FluxoMcDianteiro,)
        x = self.leitura_ED_UHLM_FluxoMcDianteiro
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_FluxoMcTras = LeituraModbusCoil("ED_UHLM_FluxoMcTras",self.clp["UG2"],REG_UG2_ED_UHLM_FluxoMcTras,)
        x = self.leitura_ED_UHLM_FluxoMcTras
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_QCAUG_Falha380VcaPainel = LeituraModbusCoil("ED_QCAUG_Falha380VcaPainel",self.clp["UG2"],REG_UG2_ED_QCAUG_Falha380VcaPainel,)
        x = self.leitura_ED_QCAUG_Falha380VcaPainel
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_ED_QCAUG_TripDisj52A1 = LeituraModbusCoil("ED_QCAUG_TripDisj52A1",self.clp["UG2"],REG_UG2_ED_QCAUG_TripDisj52A1,)
        x = self.leitura_ED_QCAUG_TripDisj52A1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_TripBomba1 = LeituraModbusCoil("ED_UHLM_TripBomba1",self.clp["UG2"],REG_UG2_ED_UHLM_TripBomba1,)
        x = self.leitura_ED_UHLM_TripBomba1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_TripBomba2 = LeituraModbusCoil("ED_UHLM_TripBomba2",self.clp["UG2"],REG_UG2_ED_UHLM_TripBomba2,)
        x = self.leitura_ED_UHLM_TripBomba2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHRV_TripBomba1 = LeituraModbusCoil("ED_UHRV_TripBomba1",self.clp["UG2"],REG_UG2_ED_UHRV_TripBomba1,)
        x = self.leitura_ED_UHRV_TripBomba1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHRV_TripBomba2 = LeituraModbusCoil("ED_UHRV_TripBomba2",self.clp["UG2"],REG_UG2_ED_UHRV_TripBomba2,)
        x = self.leitura_ED_UHRV_TripBomba2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_TripAlimPainelFreio = LeituraModbusCoil("ED_TripAlimPainelFreio",self.clp["UG2"],REG_UG2_ED_TripAlimPainelFreio,)
        x = self.leitura_ED_TripAlimPainelFreio
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_QCAUG_TripDisjAgrup = LeituraModbusCoil("ED_QCAUG_TripDisjAgrup",self.clp["UG2"],REG_UG2_ED_QCAUG_TripDisjAgrup,)
        x = self.leitura_ED_QCAUG_TripDisjAgrup
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_FalhaAcionFechaValvBorb = LeituraModbusCoil("RD_FalhaAcionFechaValvBorb",self.clp["UG2"],REG_UG2_RD_FalhaAcionFechaValvBorb,)
        x = self.leitura_RD_FalhaAcionFechaValvBorb
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_UHRV_FalhaAcionBbaM1 = LeituraModbusCoil("RD_UHRV_FalhaAcionBbaM1",self.clp["UG2"],REG_UG2_RD_UHRV_FalhaAcionBbaM1,)
        x = self.leitura_RD_UHRV_FalhaAcionBbaM1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_UHRV_FalhaAcionBbaM2 = LeituraModbusCoil("RD_UHRV_FalhaAcionBbaM2",self.clp["UG2"],REG_UG2_RD_UHRV_FalhaAcionBbaM2,)
        x = self.leitura_RD_UHRV_FalhaAcionBbaM2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_UHLM_FalhaAcionBbaM1 = LeituraModbusCoil("RD_UHLM_FalhaAcionBbaM1",self.clp["UG2"],REG_UG2_RD_UHLM_FalhaAcionBbaM1,)
        x = self.leitura_RD_UHLM_FalhaAcionBbaM1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_UHLM_FalhaAcionBbaM2 = LeituraModbusCoil("RD_UHLM_FalhaAcionBbaM2",self.clp["UG2"],REG_UG2_RD_UHLM_FalhaAcionBbaM2,)
        x = self.leitura_RD_UHLM_FalhaAcionBbaM2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripTempGaxeteiro = LeituraModbusCoil("RD_TripTempGaxeteiro",self.clp["UG2"],REG_UG2_RD_TripTempGaxeteiro,)
        x = self.leitura_RD_TripTempGaxeteiro
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripTempMcGuiaRadial = LeituraModbusCoil("RD_TripTempMcGuiaRadial",self.clp["UG2"],REG_UG2_RD_TripTempMcGuiaRadial,)
        x = self.leitura_RD_TripTempMcGuiaRadial
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripTempMcGuiaEscora = LeituraModbusCoil("RD_TripTempMcGuiaEscora",self.clp["UG2"],REG_UG2_RD_TripTempMcGuiaEscora,)
        x = self.leitura_RD_TripTempMcGuiaEscora
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripTempMcGuiaContraEscora = (LeituraModbusCoil("RD_TripTempMcGuiaContraEscora",self.clp["UG2"],REG_UG2_RD_TripTempMcGuiaContraEscora,))
        x = self.leitura_RD_TripTempMcGuiaContraEscora
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripTempUHRV = LeituraModbusCoil("RD_TripTempUHRV",self.clp["UG2"],REG_UG2_RD_TripTempUHRV,)
        x = self.leitura_RD_TripTempUHRV
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripTempUHLM = LeituraModbusCoil("RD_TripTempUHLM",self.clp["UG2"],REG_UG2_RD_TripTempUHLM,)
        x = self.leitura_RD_TripTempUHLM
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripVibr1 = LeituraModbusCoil("RD_TripVibr1",self.clp["UG2"],REG_UG2_RD_TripVibr1,)
        x = self.leitura_RD_TripVibr1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripVibr2 = LeituraModbusCoil("RD_TripVibr2",self.clp["UG2"],REG_UG2_RD_TripVibr2,)
        x = self.leitura_RD_TripVibr2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_FalhaIbntDisjGer = LeituraModbusCoil("RD_FalhaIbntDisjGer",self.clp["UG2"],REG_UG2_RD_FalhaIbntDisjGer,)
        x = self.leitura_RD_FalhaIbntDisjGer
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_CLP_Falha = LeituraModbusCoil("RD_CLP_Falha",self.clp["UG2"],REG_UG2_RD_CLP_Falha,)
        x = self.leitura_RD_CLP_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_Q_Negativa = LeituraModbusCoil("RD_Q_Negativa",self.clp["UG2"],REG_UG2_RD_Q_Negativa,)
        x = self.leitura_RD_Q_Negativa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def controle_cx_espiral(self):
        # Calcula PI
        self.erro_press_cx = 0
        self.erro_press_cx = self.leitura_caixa_espiral.valor - self.cfg["press_cx_alvo"]

        logger.debug(f"[UG{self.id}] Pressão Alvo: {self.cfg['press_cx_alvo']:0.3f}, Recente: {self.leitura_caixa_espiral.valor:0.3f}")

        self.cx_controle_p = self.cfg["cx_kp"] * self.erro_press_cx
        self.cx_controle_i = max(min((self.cfg["cx_ki"] * self.erro_press_cx) + self.cx_controle_i, 1), 0)
        saida_pi = self.cx_controle_p + self.cx_controle_i

        logger.debug(f"[UG{self.id}] PI: {saida_pi:0.3f} <-- P:{self.cx_controle_p:0.3f} + I:{self.cx_controle_i:0.3f}; ERRO={self.erro_press_cx}")

        # Calcula o integrador de estabilidade e limita
        self.cx_controle_ie = max(min(saida_pi + self.cx_ajuste_ie * self.cfg["cx_kie"], 1), 0)

        # Arredondamento e limitação
        pot_alvo = max(min(round(self.cfg["pot_maxima_ug2"] * self.cx_controle_ie, 5), self.cfg["pot_maxima_ug2"],),self.cfg["pot_minima"],)

        logger.debug(f"[UG{self.id}] Pot alvo: {pot_alvo:0.3f}")

        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = pot_alvo

        logger.debug(f"Pot alvo = {pot_alvo}")

        pot_medidor = self.potencia_ativa_kW.valor

        logger.debug(f"Pot no medidor = {pot_medidor}")

        # implementação nova
        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])

        pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

        try:
            if pot_medidor > self.cfg["pot_maxima_alvo"] * 0.97:
                pot_alvo = self.pot_alvo_anterior * (1 - 0.5 * ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))

        except TypeError as e:
            logger.debug(repr(e))

        self.pot_alvo_anterior = pot_alvo

        if self.leitura_caixa_espiral.valor >= 15.5:
            self.enviar_setpoint(pot_alvo)
        else:
            self.enviar_setpoint(0)

    def controle_limites_operacao(self):
        if self.leitura_temperatura_fase_R.valor >= self.condicionador_temperatura_fase_r_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase R da UG passou do valor base! ({self.condicionador_temperatura_fase_r_ug.valor_base}C) | Leitura: {self.leitura_temperatura_fase_R.valor}C")
        if self.leitura_temperatura_fase_R.valor >= 0.9*(self.condicionador_temperatura_fase_r_ug.valor_limite - self.condicionador_temperatura_fase_r_ug.valor_base) + self.condicionador_temperatura_fase_r_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase R da UG está muito próxima do limite! ({self.condicionador_temperatura_fase_r_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_fase_R.valor}C")

        if self.leitura_temperatura_fase_S.valor >= self.condicionador_temperatura_fase_s_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase S da UG passou do valor base! ({self.condicionador_temperatura_fase_s_ug.valor_base}C) | Leitura: {self.leitura_temperatura_fase_S.valor}C")
        if self.leitura_temperatura_fase_S.valor >= 0.9*(self.condicionador_temperatura_fase_s_ug.valor_limite - self.condicionador_temperatura_fase_s_ug.valor_base) + self.condicionador_temperatura_fase_s_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase S da UG está muito próxima do limite! ({self.condicionador_temperatura_fase_s_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_fase_S.valor}C")

        if self.leitura_temperatura_fase_T.valor >= self.condicionador_temperatura_fase_t_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase T da UG passou do valor base! ({self.condicionador_temperatura_fase_t_ug.valor_base}C) | Leitura: {self.leitura_temperatura_fase_T.valor}C")
        if self.leitura_temperatura_fase_T.valor >= 0.9*(self.condicionador_temperatura_fase_t_ug.valor_limite - self.condicionador_temperatura_fase_t_ug.valor_base) + self.condicionador_temperatura_fase_t_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase T da UG está muito próxima do limite! ({self.condicionador_temperatura_fase_t_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_fase_T.valor}C")

        if self.leitura_temperatura_nucleo.valor >= self.condicionador_temperatura_nucleo_estator_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Núcleo Estator da UG passou do valor base! ({self.condicionador_temperatura_nucleo_estator_ug.valor_base}C) | Leitura: {self.leitura_temperatura_nucleo.valor}C")
        if self.leitura_temperatura_nucleo.valor >= 0.9*(self.condicionador_temperatura_nucleo_estator_ug.valor_limite - self.condicionador_temperatura_nucleo_estator_ug.valor_base) + self.condicionador_temperatura_nucleo_estator_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Núcleo Estator da UG está muito próxima do limite! ({self.condicionador_temperatura_nucleo_estator_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_nucleo.valor}C")

        if self.leitura_temperatura_mrd1.valor >= self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Radial Dianteiro 1 da UG passou do valor base! ({self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mrd1.valor}C")
        if self.leitura_temperatura_mrd1.valor >= 0.9*(self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_limite - self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_base) + self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Radial Dianteiro 1 da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mrd1.valor}C")

        if self.leitura_temperatura_mrt1.valor >= self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Radial Traseiro 1 da UG passou do valor base! ({self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mrt1.valor}C")
        if self.leitura_temperatura_mrt1.valor >= 0.9*(self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_limite - self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_base) + self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Radial Traseiro 1 da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mrt1.valor}C")

        if self.leitura_temperatura_mrd2.valor >= self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Radial Dianteiro 2 da UG passou do valor base! ({self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mrd2.valor}C")
        if self.leitura_temperatura_mrd2.valor >= 0.9*(self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_limite - self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_base) + self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Radial Dianteiro 2 da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mrd2.valor}C")

        if self.leitura_temperatura_mrt2.valor >= self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Radial Traseiro 2 da UG passou do valor base! ({self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mrt2.valor}C")
        if self.leitura_temperatura_mrt2.valor >= 0.9*(self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_limite - self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_base) + self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Radial Traseiro 2 da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mrt2.valor}C")

        if self.leitura_temperatura_saida_de_ar.valor >= self.condicionador_temperatura_saida_de_ar_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura da Saída de Ar da UG passou do valor base! ({self.leitura_temperatura_saida_de_ar.valor}C) | Leitura: {self.condicionador_temperatura_saida_de_ar_ug.valor_base}C")
        if self.leitura_temperatura_saida_de_ar.valor >= 0.9*(self.condicionador_temperatura_saida_de_ar_ug.valor_limite - self.condicionador_temperatura_saida_de_ar_ug.valor_base) + self.condicionador_temperatura_saida_de_ar_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura da Saída de Ar da UG está muito próxima do limite! ({self.condicionador_temperatura_saida_de_ar_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_saida_de_ar.valor}C")

        if self.leitura_temperatura_guia_radial.valor >= self.condicionador_temperatura_mancal_guia_radial_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Guia Radial da UG passou do valor base! ({self.condicionador_temperatura_mancal_guia_radial_ug.valor_base}C) | Leitura: {self.leitura_temperatura_guia_radial.valor}C")
        if self.leitura_temperatura_guia_radial.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_radial_ug.valor_limite - self.condicionador_temperatura_mancal_guia_radial_ug.valor_base) + self.condicionador_temperatura_mancal_guia_radial_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Guia Radial da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_guia_radial_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_guia_radial.valor}C")

        if self.leitura_temperatura_guia_escora.valor >= self.condicionador_temperatura_mancal_guia_escora_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Guia Escora da UG passou do valor base! ({self.condicionador_temperatura_mancal_guia_escora_ug.valor_base}C) | Leitura: {self.leitura_temperatura_guia_escora.valor}C")
        if self.leitura_temperatura_guia_escora.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_escora_ug.valor_limite - self.condicionador_temperatura_mancal_guia_escora_ug.valor_base) + self.condicionador_temperatura_mancal_guia_escora_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Guia Escora da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_guia_escora_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_guia_escora.valor}C")

        if self.leitura_temperatura_guia_contra_escora.valor >= self.condicionador_temperatura_mancal_guia_contra_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Guia Contra Escora da UG passou do valor base! ({self.condicionador_temperatura_mancal_guia_contra_ug.valor_base}C) | Leitura: {self.leitura_temperatura_guia_contra_escora.valor}C")
        if self.leitura_temperatura_guia_contra_escora.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_contra_ug.valor_limite - self.condicionador_temperatura_mancal_guia_contra_ug.valor_base) + self.condicionador_temperatura_mancal_guia_contra_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Guia Contra Escora da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_guia_contra_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_guia_contra_escora.valor}C")

        if self.leitura_temperatura_oleo_trafo.valor >= self.condicionador_leitura_temperatura_oleo_trafo.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Óleo do Transformador Elevador da UG passou do valor base! ({self.condicionador_leitura_temperatura_oleo_trafo.valor_base}C) | Leitura: {self.leitura_temperatura_oleo_trafo.valor}C")
        if self.leitura_temperatura_oleo_trafo.valor >= 0.9*(self.condicionador_leitura_temperatura_oleo_trafo.valor_limite - self.condicionador_leitura_temperatura_oleo_trafo.valor_base) + self.condicionador_leitura_temperatura_oleo_trafo.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Óleo do Transformador Elevador da UG está muito próxima do limite! ({self.condicionador_leitura_temperatura_oleo_trafo.valor_limite}C) | Leitura: {self.leitura_temperatura_oleo_trafo.valor}C")

        if self.leitura_caixa_espiral.valor <= self.condicionador_caixa_espiral_ug.valor_base and self.leitura_caixa_espiral.valor != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            logger.warning(f"[UG{self.id}] A pressão Caixa Espiral da UG passou do valor base! ({self.condicionador_caixa_espiral_ug.valor_base:03.2f} KGf/m2) | Leitura: {self.leitura_caixa_espiral.valor:03.2f}")
        if self.leitura_caixa_espiral.valor <= 16.1 and self.leitura_caixa_espiral.valor != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            logger.critical(f"[UG{self.id}] A pressão Caixa Espiral da UG está muito próxima do limite! ({self.condicionador_caixa_espiral_ug.valor_limite:03.2f} KGf/m2) | Leitura: {self.leitura_caixa_espiral.valor:03.2f} KGf/m2")