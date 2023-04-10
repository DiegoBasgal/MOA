from src.UnidadeDeGeracao import *

logger = logging.getLogger("__main__")

class UnidadeDeGeracao3(UnidadeDeGeracao):
    def __init__(self, id, cfg, db, con):
        super().__init__(id, cfg, db, con)

        self.modo_autonomo = 1
        self.__last_EtapaAtual = 0
        self.pot_alvo_anterior = -1

        self.QCAUGRemoto = True
        self.acionar_voip = False
        self.release_timer = False
        self.FreioCmdRemoto = True
        self.avisou_emerg_voip = False
        self.enviar_trip_eletrico = False

        self.setpoint_minimo = self.cfg["pot_minima"]
        self.setpoint_maximo = self.cfg[f"pot_maxima_ug{self.id}"]

        self.leitura_potencia = LeituraModbus(
            f"ug{self.id}_Gerador_PotenciaAtivaMedia",
            self.clp_ug3,
            REG_UG3_RA_PM_710_Potencia_Ativa,
            op=4,
        )
        self.leitura_potencia_ug1 = LeituraModbus(
            "ug1_Gerador_PotenciaAtivaMedia",
            self.clp_ug1,
            REG_UG1_RA_PM_710_Potencia_Ativa,
            op=4,
        )
        self.leitura_setpoint_ug1 = LeituraModbus(
            "ug1_Setpoint",
            self.clp_ug1,
            UG["REG_UG1_SA_SPPotAtiva"],
            op=4
        )
        self.leitura_potencia_ug2 = LeituraModbus(
            "ug2_Gerador_PotenciaAtivaMedia",
            self.clp_ug2,
            REG_UG2_RA_PM_710_Potencia_Ativa,
            op=4,
        )
        self.leitura_setpoint_ug2 = LeituraModbus(
            "ug2_Setpoint",
            self.clp_ug2,
            UG["REG_UG2_SA_SPPotAtiva"],
            op=4
        )
        self.leitura_horimetro_hora = LeituraModbus(
            f"ug{self.id} RA_Horimetro_Gerador",
            self.clp_ug3,
            REG_UG3_RA_Horimetro_Gerador,
            op=4,
        )
        self.leitura_horimetro_frac = LeituraModbus(
            f"ug{self.id} RA_Horimetro_Gerador_min",
            self.clp_ug3,
            REG_UG3_RA_Horimetro_Gerador_min,
            op=4,
            escala=1/60
        )
        self.leitura_horimetro = LeituraSoma(
            f"ug{self.id} horímetro",
            self.leitura_horimetro_hora,
            self.leitura_horimetro_frac
        )
        C1 = LeituraModbusCoil(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.clp_ug3,
            registrador=REG_UG3_ED_DisjGeradorFechado,
        )
        C2 = LeituraModbusCoil(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.clp_ug3,
            registrador=REG_UG3_RD_ParandoEmAuto,
        )
        C3 = LeituraModbusCoil(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.clp_ug3,
            registrador=REG_UG3_ED_RV_MaquinaParada,
        )
        C4 = LeituraModbusCoil(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.clp_ug3,
            registrador=REG_UG3_RD_PartindoEmAuto,
        )
        self.leitura_Operacao_EtapaAtual = LeituraComposta(
            f"ug{self.id}_Operacao_EtapaAtual",
            leitura1=C1,
            leitura2=C2,
            leitura3=C3,
            leitura4=C4,
        )

        #Lista de condicionadores essenciais que devem ser lidos a todo momento
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        # R
        self.leitura_temperatura_fase_R = LeituraModbus("Temperatura fase R",self.clp_ug3,REG_UG3_RA_Temperatura_01,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_R
        self.condicionador_temperatura_fase_r_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_r_ug)

        # S
        self.leitura_temperatura_fase_S = LeituraModbus("Temperatura fase s",self.clp_ug3,REG_UG3_RA_Temperatura_02,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_S
        self.condicionador_temperatura_fase_s_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_s_ug)

        # T
        self.leitura_temperatura_fase_T = LeituraModbus("Temperatura fase T",self.clp_ug3,REG_UG3_RA_Temperatura_03,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_T
        self.condicionador_temperatura_fase_t_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_t_ug)

        # Nucleo estator
        self.leitura_temperatura_nucleo = LeituraModbus("Temperatura núcelo do estator",self.clp_ug3,REG_UG3_RA_Temperatura_04,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_nucleo
        self.condicionador_temperatura_nucleo_estator_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_nucleo_estator_ug)

        # MRD 1
        self.leitura_temperatura_mrd1 = LeituraModbus("Temperatura mancal radial dianteiro",self.clp_ug3,REG_UG3_RA_Temperatura_05,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_mrd1
        self.condicionador_temperatura_mancal_rad_dia_1_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_dia_1_ug)

        # MRT 1
        self.leitura_temperatura_mrt1 = LeituraModbus("Temperatura mancal radial traseiro",self.clp_ug3,REG_UG3_RA_Temperatura_06,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_mrt1
        self.condicionador_temperatura_mancal_rad_tra_1_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_tra_1_ug)

        # MRD 2
        self.leitura_temperatura_mrd2 = LeituraModbus("Temperatura mancal radial dianteiro 2",self.clp_ug3,REG_UG3_RA_Temperatura_07,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_mrd2
        self.condicionador_temperatura_mancal_rad_dia_2_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_dia_2_ug)

        # MRT 2
        self.leitura_temperatura_mrt2 = LeituraModbus("Temperatura mancal radial traseiro 2",self.clp_ug3,REG_UG3_RA_Temperatura_08,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_mrt2
        self.condicionador_temperatura_mancal_rad_tra_2_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_tra_2_ug)

        # Saída de ar
        self.leitura_temperatura_saida_de_ar = LeituraModbus("Saída de ar",self.clp_ug3,REG_UG3_RA_Temperatura_10,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_saida_de_ar
        self.condicionador_temperatura_saida_de_ar_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_saida_de_ar_ug)

        # Mancal Guia Radial
        self.leitura_temperatura_guia_radial = LeituraModbus("Mancal Guia Radial",self.clp_ug3,REG_UG3_EA_TempMcGuiaRadial,)
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_radial
        self.condicionador_temperatura_mancal_guia_radial_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_radial_ug)

        # Mancal Guia escora
        self.leitura_temperatura_guia_escora = LeituraModbus("Mancal Guia escora",self.clp_ug3,REG_UG3_EA_TempMcGuiaEscora,)
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_escora
        self.condicionador_temperatura_mancal_guia_escora_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_escora_ug)

        # Mancal Guia contra_escora
        self.leitura_temperatura_guia_contra_escora = LeituraModbus("Mancal Guia contra_escora",self.clp_ug3,REG_UG3_EA_TempMcGuiaContraEscora,)
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_contra_escora
        self.condicionador_temperatura_mancal_guia_contra_ug = (CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite))
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_contra_ug)

        # Óleo do Transformador Elevador
        self.leitura_temperatura_oleo_trafo = LeituraModbus("Óleo do Transformador Elevador",self.clp_sa,REG_SA_EA_SA_TE_TempOleo, escala = 0.1 , op = 4)
        base = 100
        limite = 200
        escala = 0.1
        x = self.leitura_temperatura_oleo_trafo
        self.condicionador_leitura_temperatura_oleo_trafo = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite, escala)
        self.condicionadores_essenciais.append(self.condicionador_leitura_temperatura_oleo_trafo)

        # CX Espiral
        self.leitura_caixa_espiral = LeituraModbus("Caixa espiral",self.clp_ug3,REG_UG3_EA_PressK1CaixaExpiral_MaisCasas,escala=0.01,op = 4)
        base = 16.1
        limite = 15.5
        x = self.leitura_caixa_espiral
        self.condicionador_caixa_espiral_ug = CondicionadorExponencialReverso(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_atenuadores.append(self.condicionador_caixa_espiral_ug)

        self.leitura_CD_EmergenciaViaSuper = LeituraModbusCoil("CD_EmergenciaViaSuper", self.clp_ug3, REG_UG3_CD_EmergenciaViaSuper,)
        x = self.leitura_CD_EmergenciaViaSuper
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_RD_TripEletrico = LeituraModbusCoil("RD_TripEletrico",self.clp_ug3,REG_UG3_RD_TripEletrico,)
        x = self.leitura_RD_TripEletrico
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_ED_ReleBloqA86HAtuado = LeituraModbusCoil("ED_ReleBloqA86HAtuado", self.clp_ug3, REG_UG3_ED_ReleBloqA86HAtuado)
        x = self.leitura_ED_ReleBloqA86HAtuado
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x, self.id, [UNIDADE_SINCRONIZADA]))

        self.leitura_ED_ReleBloqA86MAtuado = LeituraModbusCoil("ED_ReleBloqA86MAtuado", self.clp_ug3, REG_UG3_ED_ReleBloqA86MAtuado)
        x = self.leitura_ED_ReleBloqA86MAtuado
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SEL700G_Atuado = LeituraModbusCoil("ED_SEL700G_Atuado",self.clp_ug3,REG_UG3_ED_SEL700G_Atuado,)
        x = self.leitura_ED_SEL700G_Atuado
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_RV_Trip = LeituraModbusCoil("ED_RV_Trip",self.clp_ug3,REG_UG3_ED_RV_Trip,)
        x = self.leitura_ED_RV_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripMecanico = LeituraModbusCoil("RD_TripMecanico",self.clp_ug3,REG_UG3_RD_TripMecanico,)
        x = self.leitura_RD_TripMecanico
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_700G_Trip = LeituraModbusCoil("RD_700G_Trip",self.clp_ug3,REG_UG3_RD_700G_Trip,)
        x = self.leitura_RD_700G_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_ED_AVR_Trip = LeituraModbusCoil("ED_AVR_Trip",self.clp_ug3,REG_UG3_ED_AVR_Trip,)
        x = self.leitura_ED_AVR_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        #Lista de condiconadores que deverão ser lidos apenas quando houver uma chamada de leitura
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        self.leitura_ED_SA_FalhaDisjTPsSincrG3 = LeituraModbusCoil("ED_SA_FalhaDisjTPsSincrG3",self.clp_sa,REG_SA_ED_SA_FalhaDisjTPsSincrG3,)
        x = self.leitura_ED_SA_FalhaDisjTPsSincrG3
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SA_DisjDJ1_BloqPressBaixa = LeituraModbusCoil("ED_SA_DisjDJ1_BloqPressBaixa",self.clp_sa,REG_SA_ED_SA_DisjDJ1_BloqPressBaixa,)
        x = self.leitura_ED_SA_DisjDJ1_BloqPressBaixa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SA_DisjDJ1_AlPressBaixa = LeituraModbusCoil("ED_SA_DisjDJ1_AlPressBaixa",self.clp_sa,REG_SA_ED_SA_DisjDJ1_AlPressBaixa,)
        x = self.leitura_ED_SA_DisjDJ1_AlPressBaixa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_AVR_FalhaInterna = LeituraModbusCoil("ED_AVR_FalhaInterna",self.clp_ug3,REG_UG3_ED_AVR_FalhaInterna,)
        x = self.leitura_ED_AVR_FalhaInterna
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_Falta125Vcc = LeituraModbusCoil("ED_Falta125Vcc",self.clp_ug3,REG_UG3_ED_Falta125Vcc,)
        x = self.leitura_ED_Falta125Vcc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_Falta125VccCom = LeituraModbusCoil("ED_Falta125VccCom",self.clp_ug3,REG_UG3_ED_Falta125VccCom,)
        x = self.leitura_ED_Falta125VccCom
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_Falta125VccAlimVal = LeituraModbusCoil("ED_Falta125VccAlimVal",self.clp_ug3,REG_UG3_ED_Falta125VccAlimVal,)
        x = self.leitura_ED_Falta125VccAlimVal
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FalhaDisjTpsProt = LeituraModbusCoil("ED_FalhaDisjTpsProt",self.clp_ug3,REG_UG3_ED_FalhaDisjTpsProt,)
        x = self.leitura_ED_FalhaDisjTpsProt
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SEL700G_FalhaInterna = LeituraModbusCoil("ED_SEL700G_FalhaInterna",self.clp_ug3,REG_UG3_ED_SEL700G_FalhaInterna,)
        x = self.leitura_ED_SEL700G_FalhaInterna
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_NivelMAltoPocoDren = LeituraModbusCoil("ED_NivelMAltoPocoDren",self.clp_ug3,REG_UG3_ED_NivelMAltoPocoDren,)
        x = self.leitura_ED_NivelMAltoPocoDren
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FreioFiltroSaturado = LeituraModbusCoil("ED_FreioFiltroSaturado",self.clp_ug3,REG_UG3_ED_FreioFiltroSaturado,)
        x = self.leitura_ED_FreioFiltroSaturado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FreioSemEnergia = LeituraModbusCoil("ED_FreioSemEnergia",self.clp_ug3,REG_UG3_ED_FreioSemEnergia,)
        x = self.leitura_ED_FreioSemEnergia
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FiltroPresSujo100Sujo = LeituraModbusCoil("ED_FiltroPresSujo100Sujo",self.clp_ug3,REG_UG3_ED_FiltroPresSujo100Sujo,)
        x = self.leitura_ED_FiltroPresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FiltroRetSujo100Sujo = LeituraModbusCoil("ED_FiltroRetSujo100Sujo",self.clp_ug3,REG_UG3_ED_FiltroRetSujo100Sujo,)
        x = self.leitura_ED_FiltroRetSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHRV_NivOleoCriticoPos35 = LeituraModbusCoil("ED_UHRV_NivOleoCriticoPos35",self.clp_ug3,REG_UG3_ED_UHRV_NivOleoCriticoPos35,)
        x = self.leitura_ED_UHRV_NivOleoCriticoPos35
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHRV_NivOleominimoPos36 = LeituraModbusCoil("ED_UHRV_NivOleominimoPos36",self.clp_ug3,REG_UG3_ED_UHRV_NivOleominimoPos36,)
        x = self.leitura_ED_UHRV_NivOleominimoPos36
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_ValvBorbTravada = LeituraModbusCoil("ED_ValvBorbTravada",self.clp_ug3,REG_UG3_ED_ValvBorbTravada,)
        x = self.leitura_ED_ValvBorbTravada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SobreVeloMecPos18 = LeituraModbusCoil("ED_SobreVeloMecPos18",self.clp_ug3,REG_UG3_ED_SobreVeloMecPos18,)
        x = self.leitura_ED_SobreVeloMecPos18
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FaltaFluxoOleoMc = LeituraModbusCoil("ED_FaltaFluxoOleoMc",self.clp_ug3,REG_UG3_ED_FaltaFluxoOleoMc,)
        x = self.leitura_ED_FaltaFluxoOleoMc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_PalhetasDesal = LeituraModbusCoil("ED_PalhetasDesal",self.clp_ug3,REG_UG3_ED_PalhetasDesal,)
        x = self.leitura_ED_PalhetasDesal
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_FaltaFluxTroc = LeituraModbusCoil("ED_UHLM_FaltaFluxTroc",self.clp_ug3,REG_UG3_ED_UHLM_FaltaFluxTroc,)
        x = self.leitura_ED_UHLM_FaltaFluxTroc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_FaltaPressTroc = LeituraModbusCoil("ED_UHLM_FaltaPressTroc",self.clp_ug3,REG_UG3_ED_UHLM_FaltaPressTroc,)
        x = self.leitura_ED_UHLM_FaltaPressTroc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_Filt1PresSujo100Sujo = LeituraModbusCoil("ED_UHLM_Filt1PresSujo100Sujo",self.clp_ug3,REG_UG3_ED_UHLM_Filt1PresSujo100Sujo,)
        x = self.leitura_ED_UHLM_Filt1PresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_Filt2PresSujo100Sujo = LeituraModbusCoil("ED_UHLM_Filt2PresSujo100Sujo",self.clp_ug3,REG_UG3_ED_UHLM_Filt2PresSujo100Sujo,)
        x = self.leitura_ED_UHLM_Filt2PresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_NivelCritOleo = LeituraModbusCoil("ED_UHLM_NivelCritOleo",self.clp_ug3,REG_UG3_ED_UHLM_NivelCritOleo,)
        x = self.leitura_ED_UHLM_NivelCritOleo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_NivelminOleo = LeituraModbusCoil("ED_UHLM_NivelminOleo",self.clp_ug3,REG_UG3_ED_UHLM_NivelminOleo,)
        x = self.leitura_ED_UHLM_NivelminOleo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FiltroPressaoBbaMecSj100 = LeituraModbusCoil("ED_FiltroPressaoBbaMecSj100",self.clp_ug3,REG_UG3_ED_FiltroPressaoBbaMecSj100,)
        x = self.leitura_ED_FiltroPressaoBbaMecSj100
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_FluxoMcDianteiro = LeituraModbusCoil("ED_UHLM_FluxoMcDianteiro",self.clp_ug3,REG_UG3_ED_UHLM_FluxoMcDianteiro,)
        x = self.leitura_ED_UHLM_FluxoMcDianteiro
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_FluxoMcTras = LeituraModbusCoil("ED_UHLM_FluxoMcTras",self.clp_ug3,REG_UG3_ED_UHLM_FluxoMcTras,)
        x = self.leitura_ED_UHLM_FluxoMcTras
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_QCAUG_Falha380VcaPainel = LeituraModbusCoil("ED_QCAUG_Falha380VcaPainel",self.clp_ug3,REG_UG3_ED_QCAUG_Falha380VcaPainel,)
        x = self.leitura_ED_QCAUG_Falha380VcaPainel
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_ED_QCAUG_TripDisj52A1 = LeituraModbusCoil("ED_QCAUG_TripDisj52A1",self.clp_ug3,REG_UG3_ED_QCAUG_TripDisj52A1,)
        x = self.leitura_ED_QCAUG_TripDisj52A1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_TripBomba1 = LeituraModbusCoil("ED_UHLM_TripBomba1",self.clp_ug3,REG_UG3_ED_UHLM_TripBomba1,)
        x = self.leitura_ED_UHLM_TripBomba1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHLM_TripBomba2 = LeituraModbusCoil("ED_UHLM_TripBomba2",self.clp_ug3,REG_UG3_ED_UHLM_TripBomba2,)
        x = self.leitura_ED_UHLM_TripBomba2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHRV_TripBomba1 = LeituraModbusCoil("ED_UHRV_TripBomba1",self.clp_ug3,REG_UG3_ED_UHRV_TripBomba1,)
        x = self.leitura_ED_UHRV_TripBomba1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_UHRV_TripBomba2 = LeituraModbusCoil("ED_UHRV_TripBomba2",self.clp_ug3,REG_UG3_ED_UHRV_TripBomba2,)
        x = self.leitura_ED_UHRV_TripBomba2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_TripAlimPainelFreio = LeituraModbusCoil("ED_TripAlimPainelFreio",self.clp_ug3,REG_UG3_ED_TripAlimPainelFreio,)
        x = self.leitura_ED_TripAlimPainelFreio
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_QCAUG_TripDisjAgrup = LeituraModbusCoil("ED_QCAUG_TripDisjAgrup",self.clp_ug3,REG_UG3_ED_QCAUG_TripDisjAgrup,)
        x = self.leitura_ED_QCAUG_TripDisjAgrup
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_FalhaAcionFechaValvBorb = LeituraModbusCoil("RD_FalhaAcionFechaValvBorb",self.clp_ug3,REG_UG3_RD_FalhaAcionFechaValvBorb,)
        x = self.leitura_RD_FalhaAcionFechaValvBorb
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_UHRV_FalhaAcionBbaM1 = LeituraModbusCoil("RD_UHRV_FalhaAcionBbaM1",self.clp_ug3,REG_UG3_RD_UHRV_FalhaAcionBbaM1,)
        x = self.leitura_RD_UHRV_FalhaAcionBbaM1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_UHRV_FalhaAcionBbaM2 = LeituraModbusCoil("RD_UHRV_FalhaAcionBbaM2",self.clp_ug3,REG_UG3_RD_UHRV_FalhaAcionBbaM2,)
        x = self.leitura_RD_UHRV_FalhaAcionBbaM2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_UHLM_FalhaAcionBbaM1 = LeituraModbusCoil("RD_UHLM_FalhaAcionBbaM1",self.clp_ug3,REG_UG3_RD_UHLM_FalhaAcionBbaM1,)
        x = self.leitura_RD_UHLM_FalhaAcionBbaM1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_UHLM_FalhaAcionBbaM2 = LeituraModbusCoil("RD_UHLM_FalhaAcionBbaM2",self.clp_ug3,REG_UG3_RD_UHLM_FalhaAcionBbaM2,)
        x = self.leitura_RD_UHLM_FalhaAcionBbaM2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripTempGaxeteiro = LeituraModbusCoil("RD_TripTempGaxeteiro",self.clp_ug3,REG_UG3_RD_TripTempGaxeteiro,)
        x = self.leitura_RD_TripTempGaxeteiro
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripTempMcGuiaRadial = LeituraModbusCoil("RD_TripTempMcGuiaRadial",self.clp_ug3,REG_UG3_RD_TripTempMcGuiaRadial,)
        x = self.leitura_RD_TripTempMcGuiaRadial
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripTempMcGuiaEscora = LeituraModbusCoil("RD_TripTempMcGuiaEscora",self.clp_ug3,REG_UG3_RD_TripTempMcGuiaEscora,)
        x = self.leitura_RD_TripTempMcGuiaEscora
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripTempMcGuiaContraEscora = (LeituraModbusCoil("RD_TripTempMcGuiaContraEscora",self.clp_ug3,REG_UG3_RD_TripTempMcGuiaContraEscora,))
        x = self.leitura_RD_TripTempMcGuiaContraEscora
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripTempUHRV = LeituraModbusCoil("RD_TripTempUHRV",self.clp_ug3,REG_UG3_RD_TripTempUHRV,)
        x = self.leitura_RD_TripTempUHRV
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripTempUHLM = LeituraModbusCoil("RD_TripTempUHLM",self.clp_ug3,REG_UG3_RD_TripTempUHLM,)
        x = self.leitura_RD_TripTempUHLM
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripVibr1 = LeituraModbusCoil("RD_TripVibr1",self.clp_ug3,REG_UG3_RD_TripVibr1,)
        x = self.leitura_RD_TripVibr1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_TripVibr2 = LeituraModbusCoil("RD_TripVibr2",self.clp_ug3,REG_UG3_RD_TripVibr2,)
        x = self.leitura_RD_TripVibr2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_FalhaIbntDisjGer = LeituraModbusCoil("RD_FalhaIbntDisjGer",self.clp_ug3,REG_UG3_RD_FalhaIbntDisjGer,)
        x = self.leitura_RD_FalhaIbntDisjGer
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_CLP_Falha = LeituraModbusCoil("RD_CLP_Falha",self.clp_ug3,REG_UG3_RD_CLP_Falha,)
        x = self.leitura_RD_CLP_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RD_Q_Negativa = LeituraModbusCoil("RD_Q_Negativa",self.clp_ug3,REG_UG3_RD_Q_Negativa,)
        x = self.leitura_RD_Q_Negativa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_FreioPastilhaGasta = LeituraModbusCoil( "ED_FreioPastilhaGasta", self.clp_ug3, REG_UG3_ED_FreioPastilhaGasta )
        self.leitura_ED_FiltroPresSujo75Troc = LeituraModbusCoil( "ED_FiltroPresSujo75Troc", self.clp_ug3, REG_UG3_ED_FiltroPresSujo75Troc )
        self.leitura_ED_FiltroRetSujo75Troc = LeituraModbusCoil( "ED_FiltroRetSujo75Troc", self.clp_ug3, REG_UG3_ED_FiltroRetSujo75Troc )
        self.leitura_ED_UHLMFilt1PresSujo75Troc = LeituraModbusCoil( "ED_UHLMFilt1PresSujo75Troc", self.clp_ug3, REG_UG3_ED_UHLM_Filt1PresSujo75Troc )
        self.leitura_ED_UHLMFilt2PresSujo75Troc = LeituraModbusCoil( "ED_UHLMFilt2PresSujo75Troc", self.clp_ug3, REG_UG3_ED_UHLM_Filt2PresSujo75Troc )
        self.leitura_ED_FiltroPressaoBbaMecSj75 = LeituraModbusCoil( "ED_FiltroPressaoBbaMecSj75", self.clp_ug3, REG_UG3_ED_FiltroPressaoBbaMecSj75 )
        self.leitura_ED_TripPartRes = LeituraModbusCoil( "ED_TripPartRes", self.clp_ug3, REG_UG3_ED_TripPartRes )
        self.leitura_ED_FreioCmdRemoto = LeituraModbusCoil( "ED_FreioCmdRemoto", self.clp_ug3, REG_UG3_ED_FreioCmdRemoto )
        self.leitura_ED_QCAUG3_Remoto = LeituraModbusCoil( "ED_QCAUG3_Remoto", self.clp_ug3, REG_UG3_ED_QCAUG3_Remoto )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        # Inicializa as variáveis de controle PI para operação TDA Offline
        self.cx_controle_p = (self.leitura_caixa_espiral.valor - self.cfg["press_cx_alvo"]) * self.cfg["cx_kp"]
        self.cx_ajuste_ie = (self.leitura_potencia.valor + self.leitura_potencia_ug2.valor + self.leitura_potencia_ug1.valor) / self.cfg["pot_maxima_alvo"]
        self.cx_controle_i = self.cx_ajuste_ie - self.cx_controle_p

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
        pot_alvo = max(min(round(self.cfg["pot_maxima_ug3"] * self.cx_controle_ie, 5), self.cfg["pot_maxima_ug3"],),self.cfg["pot_minima"],)

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

    def acionar_trip_logico(self) -> bool:
        """
        Envia o comando de acionamento do TRIP para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            logger.debug(
                f"[UG{self.id}] Acionando sinal (via rede) de TRIP."
            )
            response = self.clp_ug3.write_single_coil(
                REG_UG3_CD_EmergenciaViaSuper, 1
            )
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    def remover_trip_logico(self) -> bool:
        """
        Envia o comando de remoção do TRIP para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            logger.debug(
                f"[UG{self.id}] Removendo sinal (via rede) de TRIP.")
            response = self.clp_ug3.write_single_coil(UG[f"REG_UG{self.id}_CD_ResetGeral"], 1)
            response = self.clp_ug3.write_single_coil(REG_UG3_CD_ResetReleBloq86H, 1)
            response = self.clp_ug3.write_single_coil(REG_UG3_CD_ResetReleBloq86M, 1)
            response = self.clp_ug3.write_single_coil(REG_UG3_CD_ResetRele700G, 1)
            response = self.clp_sa.write_single_coil(REG_SA_CD_ResetRele59N, 1)
            response = self.clp_sa.write_single_coil(REG_SA_CD_ResetRele787, 1)
            response = self.clp_ug3.write_single_coil(REG_UG3_ED_ReleBloqA86HAtuado, 0)
            response = self.clp_ug3.write_single_coil(REG_UG3_ED_ReleBloqA86MAtuado, 0)
            response = self.clp_ug3.write_single_coil(REG_UG3_RD_700G_Trip, 0)
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    def acionar_trip_eletrico(self) -> bool:
        """
        Aciona o TRIP elétricamente via painel

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.enviar_trip_eletrico = True
            logger.debug(f"[UG{self.id}] Acionando sinal elétrico de TRIP.")
            self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG3"],[1],)
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return True

    def remover_trip_eletrico(self) -> bool:
        """
        Remove o TRIP elétricamente via painel

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.enviar_trip_eletrico = False
            logger.debug(f"[UG{self.id}] Removendo sinal elétrico de TRIP.")
            self.clp_moa.write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG3"],[0],)
            self.clp_moa.write_single_coil(self.cfg["REG_PAINEL_LIDO"],[0],)
            response = self.clp_ug3.write_single_coil(REG_UG3_CD_Cala_Sirene, 1)
            if self.clp_sa.read_coils(REG_SA_CD_Liga_DJ1)[0] == 0:
                logger.debug("Comando recebido da UG3 - Fechando Dj52L")
                self.con.fechaDj52L()
        except Exception as e:
            logger.debug(f"Exception! Traceback: {traceback.format_exc()}")
            return False
        else:
            return True

    def partir(self) -> bool:
        """
        Envia o comando de parida da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            # na simulação, a condição a seguir, impede a partida das ugs. Retirar comentário quando for aplicar em campo
            if not self.clp_ug3.read_discrete_inputs(REG_UG3_COND_PART, 1)[0]:
                logger.debug(f"[UG{self.id}] Máquina sem condição de partida. Irá partir quando as condições forem reestabelecidas.")
                return True
            elif self.clp_sa.read_coils(REG_SA_ED_SA_QCAP_Disj52A1Fechado)[0] != 0:
                logger.info(f"[UG{self.id}] O Disjuntor 52A1 está aberto. Para partir a máquina, o mesmo deverá ser fechado.")
                return True
            elif not self.etapa_atual == UNIDADE_SINCRONIZADA:
                logger.info(f"[UG{self.id}] Enviando comando de partida.")
                response = self.clp_ug3.write_single_coil(UG[f"REG_UG{self.id}_CD_ResetGeral"], 1)
                response = self.clp_ug3.write_single_coil(REG_UG3_CD_ResetRele700G, 1)
                response = self.clp_ug3.write_single_coil(REG_UG3_CD_ResetReleBloq86H, 1)
                response = self.clp_ug3.write_single_coil(REG_UG3_CD_ResetReleBloq86M, 1)
                response = self.clp_ug3.write_single_coil(REG_UG3_CD_ResetReleRT, 1)
                response = self.clp_ug3.write_single_coil(REG_UG3_CD_ResetRV, 1)
                response = self.clp_ug3.write_single_coil(REG_UG3_CD_IniciaPartida, 1)
                response = self.clp_ug3.write_single_coil(REG_UG3_CD_Cala_Sirene, 1)
            else:
                logger.debug(f"[UG{self.id}] A unidade já está sincronizada.")
                response = self.clp_ug3.write_single_coil(REG_UG3_CD_Cala_Sirene, 1)
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    def parar(self) -> bool:
        """
        Envia o comando de parada da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            if not self.etapa_atual == UNIDADE_PARADA:
                logger.info(f"[UG{self.id}] Enviando comando de parada.")
                response = self.clp_ug3.write_single_coil(REG_UG3_CD_AbortaPartida, 1)
                response = self.clp_ug3.write_single_coil(REG_UG3_CD_AbortaSincronismo, 1)
                response = self.clp_ug3.write_single_coil(REG_UG3_CD_IniciaParada, 1)
                response = self.clp_ug3.write_single_coil(REG_UG3_CD_Cala_Sirene, 1)
                self.enviar_setpoint(self.setpoint)
            else:
                logger.debug(f"[UG{self.id}] A unidade já está parada.")
                response = self.clp_ug3.write_single_coil(REG_UG3_CD_Cala_Sirene, 1)
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    def reconhece_reset_alarmes(self) -> bool:
        """
        Envia o comando de reconhece e reset dos alarmes da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            logger.debug(f"[UG{self.id}] Enviando comando de reconhece e reset alarmes. (Aproximadamente 10s)")

            for _ in range(3):
                self.clp_moa.write_single_coil(self.cfg["REG_PAINEL_LIDO"], [0])
                self.remover_trip_eletrico()
                self.clp_moa.write_single_coil(self.cfg["REG_PAINEL_LIDO"], [0])
                sleep(1)
                self.remover_trip_logico()
                response = self.clp_ug3.write_single_coil(UG[f"REG_UG{self.id}_CD_ResetGeral"], 1)
                response = self.clp_ug3.write_single_coil(REG_UG3_CD_Cala_Sirene, 1)
                self.clp_moa.write_single_coil(self.cfg["REG_PAINEL_LIDO"], [0])
                sleep(1)

        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    @property
    def etapa_atual(self) -> int:
        try:
            response = self.leitura_Operacao_EtapaAtual.valor
            """
            0 Inválido
            1 Em operação
            2-3 Parando
            4-7 Quina Parada
            8-15 Partindo
            """
            if response == 1:
                return UNIDADE_SINCRONIZADA
            elif 2 <= response <= 3:
                return UNIDADE_PARANDO
            elif 4 <= response <= 7:
                return UNIDADE_PARADA
            elif 8 <= response <= 15:
                return UNIDADE_SINCRONIZANDO
            else:
                return self.__last_EtapaAtual
        except:
            #! TODO Tratar exceptions
            return self.__last_EtapaAtual
        else:
            return response

    def modbus_update_state_register(self):
        self.clp_moa.write_single_coil(
            self.cfg[f"REG_MOA_OUT_STATE_UG{self.id}"],
            [self.codigo_state],
        )
        self.clp_moa.write_single_coil(
            self.cfg[f"REG_MOA_OUT_ETAPA_UG{self.id}"],
            [self.etapa_atual],
        )

    def interstep(self) -> None:
        if (not self.avisou_emerg_voip) and (self.condicionador_caixa_espiral_ug.valor > 0.1):
            self.avisou_emerg_voip = True

        elif self.condicionador_caixa_espiral_ug.valor < 0.05:
            self.avisou_emerg_voip = False

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

    def leituras_por_hora(self):

        if self.leitura_ED_FreioPastilhaGasta.valor != 0:
            logger.warning(f"[UG{self.id}] O sensor de Freio da UG retornou que a Pastilha está gasta, favor considerar troca.")

        if self.leitura_ED_FiltroPresSujo75Troc.valor != 0:
            logger.warning(f"[UG{self.id}] O sensor do Filtro de Pressão UHRV retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.leitura_ED_FiltroRetSujo75Troc.valor != 0:
            logger.warning(f"[UG{self.id}] O sensor do Filtro de Retorno UHRV retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.leitura_ED_UHLMFilt1PresSujo75Troc.valor != 0:
            logger.warning(f"[UG{self.id}] O sensor do Filtro 1 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.leitura_ED_UHLMFilt2PresSujo75Troc.valor != 0:
            logger.warning(f"[UG{self.id}] O sensor do Filtro 2 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.leitura_ED_FiltroPressaoBbaMecSj75.valor != 0:
            logger.warning(f"[UG{self.id}] O sensor do Filtro de Pressão da Bomba Mecânica retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.leitura_ED_TripPartRes.valor != 0:
            logger.warning(f"[UG{self.id}] O sensor TripPartRes retornou valor 1.")

        # deve enviar aviso por voip

        if self.leitura_ED_FreioCmdRemoto.valor == 0 and self.FreioCmdRemoto == True:
            logger.debug(f"[UG{self.id}] O freio da UG saiu do modo remoto, favor analisar a situação.")
            self.FreioCmdRemoto = False
        elif self.leitura_ED_FreioCmdRemoto.valor == 1 and self.FreioCmdRemoto == False:
            self.FreioCmdRemoto = True

        if self.leitura_ED_QCAUG3_Remoto.valor == 0 and self.QCAUGRemoto == True:
            logger.debug(f"[UG{self.id}] O compressor da UG saiu do modo remoto, favor analisar a situação.")
            self.QCAUGRemoto = False
        elif self.leitura_ED_QCAUG3_Remoto.valor == 1 and self.QCAUGRemoto == False:
            self.QCAUGRemoto = True

        return True