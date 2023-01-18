from src.Escrita import *
from src.Leituras import *
from src.Condicionadores import *
from src.Unidade_Geracao import *
from src.Conector import Database, FieldConnector

from opcua import Client
from pyModbusTCP.server import DataBank

class UnidadeDeGeracao2(UnidadeDeGeracao):
    def __init__(self, id, cfg=None, leituras_usina=None):
        super().__init__(id)

        if not cfg or not leituras_usina:
            raise ValueError
        else:
            self.cfg = cfg
            self.leituras_usina = leituras_usina
        
        self.db = Database()

        self.con = FieldConnector(self.cfg)
        
        self.modo_autonomo = 1
        self.__last_EtapaAtual = 0
        self.__last_EtapaAlvo = -1

        self.QCAUGRemoto = True
        self.acionar_voip = False
        self.limpeza_grade = False
        self.TDA_FalhaComum = False
        self.FreioCmdRemoto = True
        self.avisou_emerg_voip = False
        self.enviar_trip_eletrico = False

        self.setpoint_minimo = self.cfg["pot_minima"]
        self.setpoint_maximo = self.cfg["pot_maxima_ug{}".format(self.id)]

        self.opc_server = Client(self.cfg["opc_server"])

        self.leitura_potencia = LeituraOPC(
            "UG{} Gerador Potência Ativa Média".format(self.id),
            self.opc_server,
            "REG_UG2_RetornosAnalogicos_MWR_PM_710_Potencia_Ativa"
        )

        self.leitura_potencia_ug1 = LeituraOPC(
            "UG1 Gerador Potência Ativa Média",
            self.opc_server,
            "REG_UG1_RetornosAnalogicos_MWR_PM_710_Potencia_Ativa"
        )

        self.leitura_setpoint_ug1 = LeituraOPC(
            "UG1 Setpoint",
            self.opc_server,
            "REG_UG1_SaidasAnalogicas_MWW_SPPotAtiva"
        )

        self.leitura_horimetro_hora = LeituraOPC(
            "UG{} Horímetro Gerador".format(self.id),
            self.opc_server,
            "REG_UG2_RetornosAnalogicos_MWR_Horimetro_Gerador"
        )

        self.leitura_horimetro_frac = LeituraOPC(
            "UG{} Horímetro Gerador min".format(self.id),
            self.opc_server,
            "REG_UG2_RetornosAnalogicos_MWR_Horimetro_Gerador_min"
        )

        self.leitura_horimetro = LeituraSoma(
            "UG{} Horímetro".format(self.id),
            self.leitura_horimetro_hora,
            self.leitura_horimetro_frac
        )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        # utilizar essa forma de leitura de etapa apenas quando for usar o simulador, 
        # utilizar a forma comentada anterior quando for em produção
        self.leitura_Operacao_EtapaAtual = LeituraOPC(
            "REG_UG2_RetornosDigitais_EtapaAux_Sim",
            self.opc_server,
            "REG_UG2_RetornosDigitais_EtapaAux_Sim"
        )
        self.leitura_Operacao_EtapaAlvo = LeituraOPC(
            "REG_UG2_RetornosDigitais_Operacao_EtapaAlvo",
            self.opc_server, 
            "REG_UG2_RetornosDigitais_EtapaAlvo_Sim"
        )
        self.condic_ativos_sim_ug2 = LeituraOPC(
            "REG_UG2_RetrornosAnalogicos_AUX_Condicionadores",
            self.opc_server,
            "REG_UG2_RetrornosAnalogicos_AUX_Condicionadores",
        )
        self.leitura_Status_Comporta = LeituraOPC(
            "REG_UG2_RetornosDigitais_StatusComporta",
            self.opc_server,
            "REG_UG2_RetornosDigitais_StatusComporta"
        )
        """
        C1 = LeituraOPC(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.opc_server,
            registrador=REG_UG2_EntradasDigitais_MXI_DisjGeradorFechado,
        )
        C2 = LeituraOPC(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.opc_server,
            registrador=REG_UG2_RetornosDigitais_MXR_ParandoEmAuto,
        )
        C3 = LeituraOPC(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.opc_server,
            registrador=REG_UG2_EntradasDigitais_MXI_RV_MaquinaParada,
        )
        C4 = LeituraOPC(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.opc_server,
            registrador=REG_UG2_RetornosDigitais_MXR_PartindoEmAuto,
        )
        self.leitura_Operacao_EtapaAtual = LeituraComposta(
            "ug{}_Operacao_EtapaAtual".format(self.id),
            leitura1=C1,
            leitura2=C2,
            leitura3=C3,
            leitura4=C4,
        )
        """

        #Lista de condicionadores essenciais que devem ser lidos a todo momento
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        # R
        self.leitura_temperatura_fase_R = LeituraOPC("Gerador {} - Temperatura Fase R".format(self.id), self.opc_server, REG_OPC["UG2_TEMP_GERADOR_FASE_A"])
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_R
        self.condicionador_temperatura_fase_r_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_r_ug)

        # S
        self.leitura_temperatura_fase_S = LeituraOPC("Gerador {} - Temperatura Fase s".format(self.id), self.opc_server, REG_OPC["UG2_TEMP_GERADOR_FASE_B"])
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_S
        self.condicionador_temperatura_fase_s_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_s_ug)
        
        # T
        self.leitura_temperatura_fase_T = LeituraOPC("Gerador {} - Temperatura Fase T".format(self.id), self.opc_server, REG_OPC["UG2_TEMP_GERADOR_FASE_C"])
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_T
        self.condicionador_temperatura_fase_t_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_t_ug)
        
        # Nucleo Gerador 1
        self.leitura_temperatura_nucleo_gerador_1 = LeituraOPC("Gerador {} - Temperatura Núcelo do Gerador 1".format(self.id),self.opc_server, REG_OPC["UG2_TEMP_GERADOR_NUCLEO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_nucleo_gerador_1
        self.condicionador_temperatura_nucleo_gerador_1_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_nucleo_gerador_1_ug)

        # Mancal Guia
        self.leitura_temperatura_mancal_guia = LeituraOPC("Gerador {} - Temperatura Mancal Guia".format(self.id), self.opc_server, REG_OPC["UG2_TEMP_MANCAL_GUIA_GERADOR"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_guia
        self.condicionador_temperatura_mancal_guia_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_ug)

        # Mancal Guia Interno 1
        self.leitura_temperatura_mancal_guia_interno_1 = LeituraOPC("Gerador {} - Temperatura Mancal Guia Interno 1".format(self.id),self.opc_server, REG_OPC["UG2_TEMP_1_MANCAL_GUIA_INTERNO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_guia_interno_1
        self.condicionador_temperatura_mancal_guia_interno_1_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_interno_1_ug)
        
        # Mancal Guia Interno 2
        self.leitura_temperatura_mancal_guia_interno_2 = LeituraOPC("Gerador {} - Temperatura Mancal Guia Interno 2".format(self.id),self.opc_server, REG_OPC["UG2_TEMP_2_MANCAL_GUIA_INTERNO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_guia_interno_2
        self.condicionador_temperatura_mancal_guia_interno_2_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_interno_2_ug)
        
        # Patins Mancal Combinado 1
        self.leitura_temperatura_patins_mancal_comb_1 = LeituraOPC("Gerador {} - Temperatura Patins Mancal Combinado 1".format(self.id), self.opc_server, REG_OPC["UG2_TEMP_1_PATINS_MANCAL_COMBINADO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_patins_mancal_comb_1
        self.condicionador_temperatura_patins_mancal_comb_1_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_patins_mancal_comb_1_ug)
        
        # Patins Mancal Combinado 2
        self.leitura_temperatura_patins_mancal_comb_2 = LeituraOPC("Gerador {} - Temperatura Patins Mancal Combinado 2".format(self.id),self.opc_server, REG_OPC["UG2_TEMP_2_PATINS_MANCAL_COMBINADO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_patins_mancal_comb_2
        self.condicionador_temperatura_patins_mancal_comb_2_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_patins_mancal_comb_2_ug)
        
        # Mancal Casquilho Combinado
        self.leitura_temperatura_mancal_casq_comb = LeituraOPC("Gerador {} - Temperatura Mancal Casquilho Combinado".format(self.id), self.opc_server, REG_OPC["UG2_TEMP_CASQ_MANCAL_COMBINADO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_casq_comb
        self.condicionador_temperatura_mancal_casq_comb_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_casq_comb_ug)

        # Mancal Contra Escora Combinado
        self.leitura_temperatura_mancal_contra_esc_comb = LeituraOPC("Gerador {} - Temperatura Mancal Contra Escora Combinado".format(self.id),self.opc_server, REG_OPC["UG2_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_contra_esc_comb
        self.condicionador_temperatura_mancal_contra_esc_comb_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_contra_esc_comb_ug)
        
        # Pressão Entrada Turbina
        self.leitura_pressao_turbina = LeituraOPC("Gerador {} - Pressão Turbina".format(self.id), self.opc_server, REG_OPC["UG2_PRESSAO_ENTRADA_TURBINA"],escala=0.1 ,op = 4)
        base = 16.1
        limite = 15.5
        x = self.leitura_pressao_turbina
        self.condicionador_pressao_turbina_ug = CondicionadorExponencialReverso(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        if self.leitura_pressao_turbina.valor != 0.0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            self.condicionadores_atenuadores.append(self.condicionador_pressao_turbina_ug)

        """
        self.leitura_ComandosDigitais_MXW_EmergenciaViaSuper = LeituraOPC("ComandosDigitais_MXW_EmergenciaViaSuper", self.opc_server, REG_UG2_ComandosDigitais_MXW_EmergenciaViaSuper,)
        x = self.leitura_ComandosDigitais_MXW_EmergenciaViaSuper
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripEletrico = LeituraOPC("RetornosDigitais_MXR_TripEletrico",self.opc_server,REG_UG2_RetornosDigitais_MXR_TripEletrico,)
        x = self.leitura_RetornosDigitais_MXR_TripEletrico
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_EntradasDigitais_MXI_ReleBloqA86HAtuado = LeituraOPC("EntradasDigitais_MXI_ReleBloqA86HAtuado", self.opc_server, REG_UG2_EntradasDigitais_MXI_ReleBloqA86HAtuado)
        x = self.leitura_EntradasDigitais_MXI_ReleBloqA86HAtuado
        if not (self.etapa_atual==UNIDADE_PARADA or self.etapa_atual==UNIDADE_PARANDO):
            self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_EntradasDigitais_MXI_ReleBloqA86MAtuado = LeituraOPC("EntradasDigitais_MXI_ReleBloqA86MAtuado", self.opc_server, REG_UG2_EntradasDigitais_MXI_ReleBloqA86MAtuado)
        x = self.leitura_EntradasDigitais_MXI_ReleBloqA86MAtuado
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SEL700G_Atuado = LeituraOPC("EntradasDigitais_MXI_SEL700G_Atuado",self.opc_server,REG_UG2_EntradasDigitais_MXI_SEL700G_Atuado,)
        x = self.leitura_EntradasDigitais_MXI_SEL700G_Atuado
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_RV_Trip = LeituraOPC("EntradasDigitais_MXI_RV_Trip",self.opc_server,REG_UG2_EntradasDigitais_MXI_RV_Trip,)
        x = self.leitura_EntradasDigitais_MXI_RV_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripMecanico = LeituraOPC("RetornosDigitais_MXR_TripMecanico",self.opc_server,REG_UG2_RetornosDigitais_MXR_TripMecanico,)
        x = self.leitura_RetornosDigitais_MXR_TripMecanico
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_700G_Trip = LeituraOPC("RetornosDigitais_MXR_700G_Trip",self.opc_server,REG_UG2_RetornosDigitais_MXR_700G_Trip,)
        x = self.leitura_RetornosDigitais_MXR_700G_Trip
        if not (self.etapa_atual==UNIDADE_PARADA or self.etapa_atual==UNIDADE_PARANDO):
            self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_EntradasDigitais_MXI_AVR_Trip = LeituraOPC("EntradasDigitais_MXI_AVR_Trip",self.opc_server,REG_UG2_EntradasDigitais_MXI_AVR_Trip,)
        x = self.leitura_EntradasDigitais_MXI_AVR_Trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        #Lista de condiconadores que deverão ser lidaos apenas quando houver uma chamada de leitura
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG2 = LeituraOPC("EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG2",self.opc_server_sa,REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG2,)
        x = self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa = LeituraOPC("EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa",self.opc_server_sa,REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa,)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa = LeituraOPC("EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa",self.opc_server_sa,REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa,)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        if self.etapa_atual==UNIDADE_SINCRONIZADA:
            self.leitura_EntradasDigitais_MXI_SA_Disj52G2_Aberto = LeituraOPC("EntradasDigitais_MXI_SA_Disj52G2_Aberto",self.opc_server_sa,REG_SA_EntradasDigitais_MXI_SA_Disj52G2_Aberto,)
            x = self.leitura_EntradasDigitais_MXI_SA_Disj52G2_Aberto
            self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_EntradasDigitais_MXI_AVR_FalhaInterna = LeituraOPC("EntradasDigitais_MXI_AVR_FalhaInterna",self.opc_server,REG_UG2_EntradasDigitais_MXI_AVR_FalhaInterna,)
        x = self.leitura_EntradasDigitais_MXI_AVR_FalhaInterna
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_Falta125Vcc = LeituraOPC("EntradasDigitais_MXI_Falta125Vcc",self.opc_server,REG_UG2_EntradasDigitais_MXI_Falta125Vcc,)
        x = self.leitura_EntradasDigitais_MXI_Falta125Vcc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_Falta125VccAlimVal = LeituraOPC("EntradasDigitais_MXI_Falta125VccAlimVal",self.opc_server,REG_UG2_EntradasDigitais_MXI_Falta125VccAlimVal,)
        x = self.leitura_EntradasDigitais_MXI_Falta125VccAlimVal
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_FalhaDisjTpsProt = LeituraOPC("EntradasDigitais_MXI_FalhaDisjTpsProt",self.opc_server,REG_UG2_EntradasDigitais_MXI_FalhaDisjTpsProt,)
        x = self.leitura_EntradasDigitais_MXI_FalhaDisjTpsProt
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SEL700G_FalhaInterna = LeituraOPC("EntradasDigitais_MXI_SEL700G_FalhaInterna",self.opc_server,REG_UG2_EntradasDigitais_MXI_SEL700G_FalhaInterna,)
        x = self.leitura_EntradasDigitais_MXI_SEL700G_FalhaInterna
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_NivelMAltoPocoDren = LeituraOPC("EntradasDigitais_MXI_NivelMAltoPocoDren",self.opc_server,REG_UG2_EntradasDigitais_MXI_NivelMAltoPocoDren,)
        x = self.leitura_EntradasDigitais_MXI_NivelMAltoPocoDren
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_FreioFiltroSaturado = LeituraOPC("EntradasDigitais_MXI_FreioFiltroSaturado",self.opc_server,REG_UG2_EntradasDigitais_MXI_FreioFiltroSaturado,)
        x = self.leitura_EntradasDigitais_MXI_FreioFiltroSaturado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_FreioSemEnergia = LeituraOPC("EntradasDigitais_MXI_FreioSemEnergia",self.opc_server,REG_UG2_EntradasDigitais_MXI_FreioSemEnergia,)
        x = self.leitura_EntradasDigitais_MXI_FreioSemEnergia
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_FiltroPresSujo100Sujo = LeituraOPC("EntradasDigitais_MXI_FiltroPresSujo100Sujo",self.opc_server,REG_UG2_EntradasDigitais_MXI_FiltroPresSujo100Sujo,)
        x = self.leitura_EntradasDigitais_MXI_FiltroPresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_FiltroRetSujo100Sujo = LeituraOPC("EntradasDigitais_MXI_FiltroRetSujo100Sujo",self.opc_server,REG_UG2_EntradasDigitais_MXI_FiltroRetSujo100Sujo,)
        x = self.leitura_EntradasDigitais_MXI_FiltroRetSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35 = LeituraOPC("EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35",self.opc_server,REG_UG2_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35,)
        x = self.leitura_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHRV_NivOleominimoPos36 = LeituraOPC("EntradasDigitais_MXI_UHRV_NivOleominimoPos36",self.opc_server,REG_UG2_EntradasDigitais_MXI_UHRV_NivOleominimoPos36,)
        x = self.leitura_EntradasDigitais_MXI_UHRV_NivOleominimoPos36
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_ValvBorbTravada = LeituraOPC("EntradasDigitais_MXI_ValvBorbTravada",self.opc_server,REG_UG2_EntradasDigitais_MXI_ValvBorbTravada,)
        x = self.leitura_EntradasDigitais_MXI_ValvBorbTravada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SobreVeloMecPos18 = LeituraOPC("EntradasDigitais_MXI_SobreVeloMecPos18",self.opc_server,REG_UG2_EntradasDigitais_MXI_SobreVeloMecPos18,)
        x = self.leitura_EntradasDigitais_MXI_SobreVeloMecPos18
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_FaltaFluxoOleoMc = LeituraOPC("EntradasDigitais_MXI_FaltaFluxoOleoMc",self.opc_server,REG_UG2_EntradasDigitais_MXI_FaltaFluxoOleoMc,)
        x = self.leitura_EntradasDigitais_MXI_FaltaFluxoOleoMc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_PalhetasDesal = LeituraOPC("EntradasDigitais_MXI_PalhetasDesal",self.opc_server,REG_UG2_EntradasDigitais_MXI_PalhetasDesal,)
        x = self.leitura_EntradasDigitais_MXI_PalhetasDesal
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_FaltaFluxTroc = LeituraOPC("EntradasDigitais_MXI_UHLM_FaltaFluxTroc",self.opc_server,REG_UG2_EntradasDigitais_MXI_UHLM_FaltaFluxTroc,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_FaltaFluxTroc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_FaltaPressTroc = LeituraOPC("EntradasDigitais_MXI_UHLM_FaltaPressTroc",self.opc_server,REG_UG2_EntradasDigitais_MXI_UHLM_FaltaPressTroc,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_FaltaPressTroc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo = LeituraOPC("EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo",self.opc_server,REG_UG2_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo = LeituraOPC("EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo",self.opc_server,REG_UG2_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_NivelCritOleo = LeituraOPC("EntradasDigitais_MXI_UHLM_NivelCritOleo",self.opc_server,REG_UG2_EntradasDigitais_MXI_UHLM_NivelCritOleo,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_NivelCritOleo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_NivelminOleo = LeituraOPC("EntradasDigitais_MXI_UHLM_NivelminOleo",self.opc_server,REG_UG2_EntradasDigitais_MXI_UHLM_NivelminOleo,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_NivelminOleo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100 = LeituraOPC("EntradasDigitais_MXI_FiltroPressaoBbaMecSj100",self.opc_server,REG_UG2_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100,)
        x = self.leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro = LeituraOPC("EntradasDigitais_MXI_UHLM_FluxoMcDianteiro",self.opc_server,REG_UG2_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcTras = LeituraOPC("EntradasDigitais_MXI_UHLM_FluxoMcTras",self.opc_server,REG_UG2_EntradasDigitais_MXI_UHLM_FluxoMcTras,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcTras
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel = LeituraOPC("EntradasDigitais_MXI_QCAUG_Falha380VcaPainel",self.opc_server,REG_UG2_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel,)
        x = self.leitura_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_EntradasDigitais_MXI_QCAUG_TripDisj52A1 = LeituraOPC("EntradasDigitais_MXI_QCAUG_TripDisj52A1",self.opc_server,REG_UG2_EntradasDigitais_MXI_QCAUG_TripDisj52A1,)
        x = self.leitura_EntradasDigitais_MXI_QCAUG_TripDisj52A1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_TripBomba1 = LeituraOPC("EntradasDigitais_MXI_UHLM_TripBomba1",self.opc_server,REG_UG2_EntradasDigitais_MXI_UHLM_TripBomba1,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_TripBomba1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_TripBomba2 = LeituraOPC("EntradasDigitais_MXI_UHLM_TripBomba2",self.opc_server,REG_UG2_EntradasDigitais_MXI_UHLM_TripBomba2,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_TripBomba2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHRV_TripBomba1 = LeituraOPC("EntradasDigitais_MXI_UHRV_TripBomba1",self.opc_server,REG_UG2_EntradasDigitais_MXI_UHRV_TripBomba1,)
        x = self.leitura_EntradasDigitais_MXI_UHRV_TripBomba1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHRV_TripBomba2 = LeituraOPC("EntradasDigitais_MXI_UHRV_TripBomba2",self.opc_server,REG_UG2_EntradasDigitais_MXI_UHRV_TripBomba2,)
        x = self.leitura_EntradasDigitais_MXI_UHRV_TripBomba2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_TripAlimPainelFreio = LeituraOPC("EntradasDigitais_MXI_TripAlimPainelFreio",self.opc_server,REG_UG2_EntradasDigitais_MXI_TripAlimPainelFreio,)
        x = self.leitura_EntradasDigitais_MXI_TripAlimPainelFreio
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_QCAUG_TripDisjAgrup = LeituraOPC("EntradasDigitais_MXI_QCAUG_TripDisjAgrup",self.opc_server,REG_UG2_EntradasDigitais_MXI_QCAUG_TripDisjAgrup,)
        x = self.leitura_EntradasDigitais_MXI_QCAUG_TripDisjAgrup
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_FalhaAcionFechaValvBorb = LeituraOPC("RetornosDigitais_MXR_FalhaAcionFechaValvBorb",self.opc_server,REG_UG2_RetornosDigitais_MXR_FalhaAcionFechaValvBorb,)
        x = self.leitura_RetornosDigitais_MXR_FalhaAcionFechaValvBorb
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1 = LeituraOPC("RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1",self.opc_server,REG_UG2_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1,)
        x = self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2 = LeituraOPC("RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2",self.opc_server,REG_UG2_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2,)
        x = self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1 = LeituraOPC("RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1",self.opc_server,REG_UG2_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1,)
        x = self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2 = LeituraOPC("RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2",self.opc_server,REG_UG2_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2,)
        x = self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripTempGaxeteiro = LeituraOPC("RetornosDigitais_MXR_TripTempGaxeteiro",self.opc_server,REG_UG2_RetornosDigitais_MXR_TripTempGaxeteiro,)
        x = self.leitura_RetornosDigitais_MXR_TripTempGaxeteiro
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripTempMcGuiaRadial = LeituraOPC("RetornosDigitais_MXR_TripTempMcGuiaRadial",self.opc_server,REG_UG2_RetornosDigitais_MXR_TripTempMcGuiaRadial,)
        x = self.leitura_RetornosDigitais_MXR_TripTempMcGuiaRadial
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripTempMcGuiaEscora = LeituraOPC("RetornosDigitais_MXR_TripTempMcGuiaEscora",self.opc_server,REG_UG2_RetornosDigitais_MXR_TripTempMcGuiaEscora,)
        x = self.leitura_RetornosDigitais_MXR_TripTempMcGuiaEscora
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripTempMcGuiaContraEscora = (LeituraOPC("RetornosDigitais_MXR_TripTempMcGuiaContraEscora",self.opc_server,REG_UG2_RetornosDigitais_MXR_TripTempMcGuiaContraEscora,))
        x = self.leitura_RetornosDigitais_MXR_TripTempMcGuiaContraEscora
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripTempUHRV = LeituraOPC("RetornosDigitais_MXR_TripTempUHRV",self.opc_server,REG_UG2_RetornosDigitais_MXR_TripTempUHRV,)
        x = self.leitura_RetornosDigitais_MXR_TripTempUHRV
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripTempUHLM = LeituraOPC("RetornosDigitais_MXR_TripTempUHLM",self.opc_server,REG_UG2_RetornosDigitais_MXR_TripTempUHLM,)
        x = self.leitura_RetornosDigitais_MXR_TripTempUHLM
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripVibr1 = LeituraOPC("RetornosDigitais_MXR_TripVibr1",self.opc_server,REG_UG2_RetornosDigitais_MXR_TripVibr1,)
        x = self.leitura_RetornosDigitais_MXR_TripVibr1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripVibr2 = LeituraOPC("RetornosDigitais_MXR_TripVibr2",self.opc_server,REG_UG2_RetornosDigitais_MXR_TripVibr2,)
        x = self.leitura_RetornosDigitais_MXR_TripVibr2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_FalhaIbntDisjGer = LeituraOPC("RetornosDigitais_MXR_FalhaIbntDisjGer",self.opc_server,REG_UG2_RetornosDigitais_MXR_FalhaIbntDisjGer,)
        x = self.leitura_RetornosDigitais_MXR_FalhaIbntDisjGer
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_CLP_Falha = LeituraOPC("RetornosDigitais_MXR_CLP_Falha",self.opc_server,REG_UG2_RetornosDigitais_MXR_CLP_Falha,)
        x = self.leitura_RetornosDigitais_MXR_CLP_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_Q_Negativa = LeituraOPC("RetornosDigitais_MXR_Q_Negativa",self.opc_server,REG_UG2_RetornosDigitais_MXR_Q_Negativa,)
        x = self.leitura_RetornosDigitais_MXR_Q_Negativa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.RetornosDigitais_MXR_TripPressaoCaixaEspiral = LeituraOPC( "RetornosDigitais_MXR_TripPressaoCaixaEspiral", self.opc_server, REG_UG2_RetornosDigitais_MXR_TripPressaoCaixaEspiral, )
        x = self.RetornosDigitais_MXR_TripPressaoCaixaEspiral
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )
        """
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # Inicializa as variáveis de controle PI para operação TDA Offline
        self.pt_controle_p = (self.leitura_pressao_turbina.valor - self.cfg["press_turbina_alvo"]) * self.cfg["pt_kp"]
        self.pt_ajuste_ie = (self.leitura_potencia.valor + self.leitura_potencia_UG2.valor) / self.cfg["pot_maxima_alvo"]
        self.pt_controle_i = self.pt_ajuste_ie - self.pt_controle_p

    def controle_cx_espiral(self):
        # Calcula PI
        self.erro_press_turbina = 0
        self.erro_press_turbina = self.leitura_pressao_turbina.valor - self.cfg["press_turbina_alvo"]

        self.logger.debug("[UG{}] Pressão Alvo: {:0.3f}, Recente: {:0.3f}".format(self.id, self.cfg["press_turbina_alvo"], self.leitura_pressao_turbina.valor))

        self.pt_controle_p = self.cfg["pt_kp"] * self.erro_press_turbina
        self.pt_controle_i = max(min((self.cfg["cx_ki"] * self.erro_press_turbina) + self.pt_controle_i, 1), 0)
        saida_pi = self.pt_controle_p + self.pt_controle_i
        
        self.logger.debug("[UG{}] PI: {:0.3f} <-- P:{:0.3f} + I:{:0.3f}; ERRO={}".format(self.id, saida_pi, self.pt_controle_p, self.pt_controle_i, self.erro_press_turbina))

        # Calcula o integrador de estabilidade e limita
        self.pt_controle_ie = max(min(saida_pi + self.pt_ajuste_ie * self.cfg["pt_kie"], 1), 0)

        # Arredondamento e limitação
        pot_alvo = max(min(round(self.cfg["pot_maxima_ug2"] * self.pt_controle_ie, 5), self.cfg["pot_maxima_ug2"],),self.cfg["pot_minima"],)

        self.logger.debug("[UG{}] Pot alvo: {:0.3f}".format(self.id, pot_alvo))

        ts = datetime.now(pytz.timezone("Brazil/East")).timestamp()
        try:
            self.db.insert_debug(
                ts,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
                0,
                0,
                0,
                0,
                self.leitura_setpoint_UG2.valor,
                self.leitura_potencia_UG2.valor,
                self.setpoint,
                self.leitura_potencia.valor,
                0,
                0,
                1,
                self.cfg["pt_kp"],
                self.cfg["pt_ki"],
                self.cfg["pt_kie"],
                self.pt_controle_ie,
            )
        except Exception as e:
            logger.exception(e)

        if self.leitura_pressao_turbina.valor >= 15.5:
            self.enviar_setpoint(pot_alvo)
        else:
            self.enviar_setpoint(0)
        print("")
        
    def acionar_trip_logico(self) -> bool:
        """
        Envia o comando de acionamento do TRIP para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.debug("[UG{}] Acionando sinal de TRIP.".format(self.id))
            response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_EmergenciaViaSuper", True)
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
            self.logger.debug("[UG{}] Removendo sinal de TRIP.".format(self.id))
            response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_ResetGeral", True)
            response = Escrita.write_value_bool(self.opc_server, "REG_UG2_EntradasDigitais_MXI_ReleBloqA86HAtuado", False)
            response = Escrita.write_value_bool(self.opc_server, "REG_UG2_RetornosDigitais_MXR_700G_Trip", False)
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
            self.logger.debug("[UG{}] Acionando sinal elétrico de TRIP.".format(self.id))
            DataBank.set_words(self.cfg["REG_MOA_OUT_BLOCK_UG2"],[1],)
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
            self.logger.debug("[UG{}] Removendo sinal elétrico de TRIP.".format(self.id))
            DataBank.set_words(self.cfg["REG_MOA_OUT_BLOCK_UG2"],[0],)
            DataBank.set_words(self.cfg["REG_PAINEL_LIDO"],[0],)
            response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_Cala_Sirene", True)
            if read_input_value(self.opc_server, "REG_SA_ComandosDigitais_MXW_Liga_DJ1") == 0:
                self.logger.debug("Comando recebido da UG2 - Fechando Dj52L")
                self.con.fechaDj52L()
        except Exception as e:
            self.logger.debug("Exception! Traceback: {}".format(traceback.format_exc()))
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
            """
            # na simulação, a condição a seguir, impede a partida das ugs. Retirar comentário quando for aplicar em campo
            if not self.opc_server.read_discrete_inputs(REG_UG2_COND_PART,1)[0]:
                self.logger.debug("[UG{}] Máquina sem condição de partida. Irá partir quando as condições forem reestabelecidas.".format(self.id))
                return True
            elif self.opc_server_sa.read_coils(REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52A1Fechado)[0] != 0:
                self.logger.debug("[UG{}] O Disjuntor 52A1 está aberto. Para partir a máquina, o mesmo deverá ser fechado.")
                return True
            """
            if not self.etapa_alvo == UNIDADE_SINCRONIZADA:
                self.logger.info("[UG{}] Enviando comando de partida.".format(self.id))
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_ResetGeral", True)
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_ResetRele700G", True)
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_ResetReleBloq86H", True)
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_ResetReleBloq86M", True)
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_ResetReleRT", True)
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_ResetRV", True)
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_IniciaPartida", True)
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_Cala_Sirene", True)
                self.enviar_setpoint(self.setpoint)
            else:
                self.logger.debug("[UG{}] A unidade já está sincronizada.".format(self.id))
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_Cala_Sirene", True)

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
                self.logger.info("[UG{}] Enviando comando de parada.".format(self.id))
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_AbortaPartida", True)
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_AbortaSincronismo", True)
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_IniciaParada", True)
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_Cala_Sirene", True)
                self.enviar_setpoint(self.setpoint)
            else:
                self.logger.debug("[UG{}] A unidade já está parada.".format(self.id))
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_Cala_Sirene", True)

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
            self.logger.info("[UG{}] Enviando comando de reconhece e reset alarmes. (Aproximadamente 10s)".format(self.id))

            for _ in range(3):
                DataBank.set_words(self.cfg["REG_PAINEL_LIDO"], [0])
                self.remover_trip_eletrico()
                DataBank.set_words(self.cfg["REG_PAINEL_LIDO"], [0])
                sleep(1)
                self.remover_trip_logico()
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_ResetGeral", True)
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_Cala_Sirene", True)
                DataBank.set_words(self.cfg["REG_PAINEL_LIDO"], [0])
                sleep(1)

        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    def enviar_setpoint(self, setpoint_kw: int) -> bool:
        """
        Envia o setpoint desejado para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:

            self.setpoint_minimo = self.cfg["pot_minima"]
            self.setpoint_maximo = self.cfg["pot_maxima_ug{}".format(self.id)]

            self.setpoint = int(setpoint_kw)
            self.logger.debug("[UG{}] Enviando setpoint {} kW.".format(self.id, int(self.setpoint)))
            response = False
            if self.setpoint > 1:
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_ResetGeral", True)
                response = Escrita.write_value_bool(self.opc_server, "REG_UG2_ComandosDigitais_MXW_RV_RefRemHabilita", True)
                response = Escrita.write_value_int(self.opc_server, "REG_UG2_SaidasAnalogicas_MWW_SPPotAtiva", self.setpoint)

        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    
    @property
    def etapa_alvo(self) -> int:
        try:
            response = self.leitura_Operacao_EtapaAlvo.valor
            
            if response > 0 and response < 255:
                self.__last_EtapaAlvo = response
            else:
                self.__last_EtapaAlvo = self.etapa_atual

            return self.__last_EtapaAlvo
            
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    @property
    def etapa_atual(self) -> int:
        try:
            response = self.leitura_Operacao_EtapaAtual.valor
            if response > 0:
                self.__last_EtapaAtual = response
                return response
            else:
                return self.__last_EtapaAtual
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    @property
    def status_comporta(self) -> int:
        try:
            response = self.leitura_Status_Comporta.valor
        except Exception as e:
            raise(e)
            return False
        else:
            return response

    def abrir_comporta(self) -> bool:
        try:
            response = Escrita.write_value_int(self.opc_server, "REG_UG2_RetornosDigitais_StatusComporta", 1)
        except Exception as e:
            raise(e)
            return False
        else:
            return response
    
    def fechar_comporta(self) -> bool:
        try:
            response = Escrita.write_value_int(self.opc_server, "REG_UG2_RetornosDigitais_StatusComporta", 0)
        except Exception as e:
            raise(e)
            return False
        else:
            return response

    def cracking_comporta(self) -> bool:
        try:
            response = Escrita.write_value_int(self.opc_server, "REG_UG2_RetornosDigitais_StatusComporta", 2)
        except Exception as e:
            raise(e)
            return False
        else:
            return response

    def modbus_update_state_register(self):
        DataBank.set_words(self.cfg["REG_MOA_OUT_STATE_UG{}".format(self.id)],[self.codigo_state],)
        DataBank.set_words(self.cfg["REG_MOA_OUT_ETAPA_UG{}".format(self.id)],[self.etapa_atual],)
        
    def interstep(self) -> None:
        if (not self.avisou_emerg_voip) and (self.condicionador_pressao_turbina_ug.valor > 0.1):
            self.avisou_emerg_voip = True

        elif self.condicionador_pressao_turbina_ug.valor < 0.05:
            self.avisou_emerg_voip = False

    def controle_limites_operacao(self):

        if self.leitura_temperatura_fase_R.valor >= self.condicionador_temperatura_fase_r_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura de Fase R da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_r_ug.valor_base, self.leitura_temperatura_fase_R.valor))
        if self.leitura_temperatura_fase_R.valor >= 0.9*(self.condicionador_temperatura_fase_r_ug.valor_limite - self.condicionador_temperatura_fase_r_ug.valor_base) + self.condicionador_temperatura_fase_r_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura de Fase R da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_r_ug.valor_limite, self.leitura_temperatura_fase_R.valor))
        
        if self.leitura_temperatura_fase_S.valor >= self.condicionador_temperatura_fase_s_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura de Fase S da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_s_ug.valor_base, self.leitura_temperatura_fase_S.valor))
        if self.leitura_temperatura_fase_S.valor >= 0.9*(self.condicionador_temperatura_fase_s_ug.valor_limite - self.condicionador_temperatura_fase_s_ug.valor_base) + self.condicionador_temperatura_fase_s_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura de Fase S da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_s_ug.valor_limite, self.leitura_temperatura_fase_S.valor))

        if self.leitura_temperatura_fase_T.valor >= self.condicionador_temperatura_fase_t_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura de Fase T da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_t_ug.valor_base, self.leitura_temperatura_fase_T.valor))
        if self.leitura_temperatura_fase_T.valor >= 0.9*(self.condicionador_temperatura_fase_t_ug.valor_limite - self.condicionador_temperatura_fase_t_ug.valor_base) + self.condicionador_temperatura_fase_t_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura de Fase T da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_t_ug.valor_limite, self.leitura_temperatura_fase_T.valor))

        if self.leitura_temperatura_nucleo_gerador_1.valor >= self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Núcleo Gerador 1 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base, self.leitura_temperatura_nucleo_gerador_1.valor))
        if self.leitura_temperatura_nucleo_gerador_1.valor >= 0.9*(self.condicionador_temperatura_nucleo_gerador_1_ug.valor_limite - self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base) + self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Núcleo Gerador 1 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_nucleo_gerador_1_ug.valor_limite, self.leitura_temperatura_nucleo_gerador_1.valor))
        
        if self.leitura_temperatura_mancal_guia.valor >= self.condicionador_temperatura_mancal_guia_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Guia da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_ug.valor_base, self.leitura_temperatura_mancal_guia.valor))
        if self.leitura_temperatura_mancal_guia.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_ug.valor_limite - self.condicionador_temperatura_mancal_guia_ug.valor_base) + self.condicionador_temperatura_mancal_guia_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Guia da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_ug.valor_limite, self.leitura_temperatura_mancal_guia.valor))
        
        if self.leitura_temperatura_mancal_guia_interno_1.valor >= self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Guia Interno 1 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base, self.leitura_temperatura_mancal_guia_interno_1.valor))
        if self.leitura_temperatura_mancal_guia_interno_1.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_limite - self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base) + self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Guia Interno 1 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_limite, self.leitura_temperatura_mancal_guia_interno_1.valor))
        
        if self.leitura_temperatura_mancal_guia_interno_2.valor >= self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Guia Interno 2 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base, self.leitura_temperatura_mancal_guia_interno_2.valor))
        if self.leitura_temperatura_mancal_guia_interno_2.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_limite - self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base) + self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Guia Interno 2 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_limite, self.leitura_temperatura_mancal_guia_interno_2.valor))

        if self.leitura_temperatura_patins_mancal_comb_1.valor >= self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura dos Patins do Mancal Combinado 1 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base, self.leitura_temperatura_patins_mancal_comb_1.valor))
        if self.leitura_temperatura_patins_mancal_comb_1.valor >= 0.9*(self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_limite - self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base) + self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura dos Patins do Mancal Combinado 1 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_limite, self.leitura_temperatura_patins_mancal_comb_1.valor))
        
        if self.leitura_temperatura_patins_mancal_comb_2.valor >= self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura dos Patins do Mancal Combinado 2 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base, self.leitura_temperatura_patins_mancal_comb_2.valor))
        if self.leitura_temperatura_patins_mancal_comb_2.valor >= 0.9*(self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_limite - self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base) + self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura dos Patins do Mancal Combinado 2 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_limite, self.leitura_temperatura_patins_mancal_comb_2.valor))

        if self.leitura_temperatura_mancal_casq_comb.valor >= self.condicionador_temperatura_mancal_casq_comb_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Casquilho Combinado da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_casq_comb_ug.valor_base, self.leitura_temperatura_mancal_casq_comb.valor))
        if self.leitura_temperatura_mancal_casq_comb.valor >= 0.9*(self.condicionador_temperatura_mancal_casq_comb_ug.valor_limite - self.condicionador_temperatura_mancal_casq_comb_ug.valor_base) + self.condicionador_temperatura_mancal_casq_comb_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Casquilho Combinado da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_casq_comb_ug.valor_limite, self.leitura_temperatura_mancal_casq_comb.valor))

        if self.leitura_temperatura_mancal_contra_esc_comb.valor >= self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Contra Escora Combinado da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base, self.leitura_temperatura_mancal_contra_esc_comb.valor))
        if self.leitura_temperatura_mancal_contra_esc_comb.valor >= 0.9*(self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_limite - self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base) + self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Contra Escora Combinado da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_limite, self.leitura_temperatura_mancal_contra_esc_comb.valor))

        if self.leitura_pressao_turbina.valor <= self.condicionador_pressao_turbina_ug.valor_base and self.leitura_pressao_turbina.valor != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            self.logger.warning("[UG{}] A pressão na entrada da turbina da UG passou do valor base! ({:03.2f} KGf/m2) | Leitura: {:03.2f}".format(self.id, self.condicionador_pressao_turbina_ug.valor_base, self.leitura_pressao_turbina.valor))
        if self.leitura_pressao_turbina.valor <= self.condicionador_pressao_turbina_ug.valor_limite+0.9*(self.condicionador_pressao_turbina_ug.valor_base - self.condicionador_pressao_turbina_ug.valor_limite) and self.leitura_pressao_turbina.valor != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            self.logger.critical("[UG{}] A pressão na entrada da turbina da UG está muito próxima do limite! ({:03.2f} KGf/m2) | Leitura: {:03.2f} KGf/m2".format(self.id, self.condicionador_pressao_turbina_ug.valor_limite, self.leitura_pressao_turbina.valor))

    def leituras_por_hora(self):
        """
        self.leitura_EntradasDigitais_MXI_FreioPastilhaGasta = LeituraOPC( "EntradasDigitais_MXI_FreioPastilhaGasta", self.opc_server, REG_UG2_EntradasDigitais_MXI_FreioPastilhaGasta )
        if self.leitura_EntradasDigitais_MXI_FreioPastilhaGasta.valor != 0:
            self.logger.warning("[UG{}] O sensor de Freio da UG retornou que a Pastilha está gasta, favor considerar troca.".format(self.id))

        self.leitura_EntradasDigitais_MXI_FiltroPresSujo75Troc = LeituraOPC( "EntradasDigitais_MXI_FiltroPresSujo75Troc", self.opc_server, REG_UG2_EntradasDigitais_MXI_FiltroPresSujo75Troc )
        if self.leitura_EntradasDigitais_MXI_FiltroPresSujo75Troc.valor != 0:
            self.logger.warning("[UG{}] O sensor do Filtro de Pressão UHRV retornou que o filtro está 75% sujo, favor considerar troca.".format(self.id))

        self.leitura_EntradasDigitais_MXI_FiltroRetSujo75Troc = LeituraOPC( "EntradasDigitais_MXI_FiltroRetSujo75Troc", self.opc_server, REG_UG2_EntradasDigitais_MXI_FiltroRetSujo75Troc )
        if self.leitura_EntradasDigitais_MXI_FiltroRetSujo75Troc.valor != 0:
            self.logger.warning("[UG{}] O sensor do Filtro de Retorno UHRV retornou que o filtro está 75% sujo, favor considerar troca.".format(self.id))

        self.leitura_EntradasDigitais_MXI_UHLMFilt1PresSujo75Troc = LeituraOPC( "EntradasDigitais_MXI_UHLMFilt1PresSujo75Troc", self.opc_server, REG_UG2_EntradasDigitais_MXI_UHLM_Filt1PresSujo75Troc )
        if self.leitura_EntradasDigitais_MXI_UHLMFilt1PresSujo75Troc.valor != 0:
            self.logger.warning("[UG{}] O sensor do Filtro 1 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.".format(self.id))

        self.leitura_EntradasDigitais_MXI_UHLMFilt2PresSujo75Troc = LeituraOPC( "EntradasDigitais_MXI_UHLMFilt2PresSujo75Troc", self.opc_server, REG_UG2_EntradasDigitais_MXI_UHLM_Filt2PresSujo75Troc )
        if self.leitura_EntradasDigitais_MXI_UHLMFilt2PresSujo75Troc.valor != 0:
            self.logger.warning("[UG{}] O sensor do Filtro 2 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.".format(self.id))

        self.leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj75 = LeituraOPC( "EntradasDigitais_MXI_FiltroPressaoBbaMecSj75", self.opc_server, REG_UG2_EntradasDigitais_MXI_FiltroPressaoBbaMecSj75 )
        if self.leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj75.valor != 0:
            self.logger.warning("[UG{}] O sensor do Filtro de Pressão da Bomba Mecânica retornou que o filtro está 75% sujo, favor considerar troca.".format(self.id))

        self.leitura_EntradasDigitais_MXI_TripPartRes = LeituraOPC( "EntradasDigitais_MXI_TripPartRes", self.opc_server, REG_UG2_EntradasDigitais_MXI_TripPartRes )
        if self.leitura_EntradasDigitais_MXI_TripPartRes.valor != 0:
            self.logger.warning("[UG{}] O sensor TripPartRes retornou valor 1.".format(self.id))

        # deve enviar aviso por voip

        self.leitura_EntradasDigitais_MXI_FreioCmdRemoto = LeituraOPC( "EntradasDigitais_MXI_FreioCmdRemoto", self.opc_server, REG_UG2_EntradasDigitais_MXI_FreioCmdRemoto )
        if self.leitura_EntradasDigitais_MXI_FreioCmdRemoto.valor == 0 and self.FreioCmdRemoto == True:
            self.logger.warning("[UG{}] O sensor de freio da UG saiu do modo remoto, favor analisar a situação.".format(self.id))
            self.FreioCmdRemoto = False
            self.acionar_voip = True
        elif self.leitura_EntradasDigitais_MXI_FreioCmdRemoto.valor == 1 and self.FreioCmdRemoto == False:
            self.FreioCmdRemoto = True

        self.leitura_EntradasDigitais_MXI_QCAUG2_Remoto = LeituraOPC( "EntradasDigitais_MXI_QCAUG2_Remoto", self.opc_server, REG_UG2_EntradasDigitais_MXI_QCAUG2_Remoto )
        if self.leitura_EntradasDigitais_MXI_QCAUG2_Remoto.valor == 0 and self.QCAUGRemoto == True:
            self.logger.warning("[UG{}] O compressor da UG saiu do modo remoto, favor analisar a situação.".format(self.id))
            self.QCAUGRemoto = False
            self.acionar_voip = True
        elif self.leitura_EntradasDigitais_MXI_QCAUG2_Remoto.valor == 1 and self.QCAUGRemoto == False:
            self.QCAUGRemoto = True
        
        return True
        """