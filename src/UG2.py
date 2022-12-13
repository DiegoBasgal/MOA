from src.Leituras import *
from src.Condicionadores import *
from src.UnidadeDeGeracao import *
from pyModbusTCP.server import DataBank
from src.database_connector import Database

class UnidadeDeGeracao2(UnidadeDeGeracao):
    def __init__(self, id, cfg=None, leituras_usina=None):
        super().__init__(id)

        if not cfg or not leituras_usina:
            raise ValueError
        else:
            self.cfg = cfg
            self.leituras_usina = leituras_usina
        
        self.db = Database()

        from src.field_connector import FieldConnector
        self.con = FieldConnector(self.cfg)

        from src.LeiturasUSN import LeiturasUSN
        self.leituras = LeiturasUSN(self.cfg)
        
        self.modo_autonomo = 1
        self.__last_EtapaAtual = 0
        self.pot_alvo_anterior = -1

        self.QCAUGRemoto = True
        self.acionar_voip = False
        self.limpeza_grade = False
        self.FreioCmdRemoto = True
        self.avisou_emerg_voip = False
        self.enviar_trip_eletrico = False

        self.setpoint_minimo = self.cfg["pot_minima"]
        self.setpoint_maximo = self.cfg["pot_maxima_ug{}".format(self.id)]

        self.clp_ip = self.cfg["UG2_slave_ip"]
        self.clp_port = self.cfg["UG2_slave_porta"]
        self.clp = ModbusClient(
            host=self.clp_ip,
            port=self.clp_port,
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )
        self.clp_ug1_ip = self.cfg["UG1_slave_ip"]
        self.clp_ug1_port = self.cfg["UG1_slave_porta"]
        self.clp_ug1 = ModbusClient(
            host=self.clp_ug1_ip,
            port=self.clp_ug1_port,
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )
        self.clp_ug3_ip = self.cfg["UG3_slave_ip"]
        self.clp_ug3_port = self.cfg["UG3_slave_porta"]
        self.clp_ug3 = ModbusClient(
            host=self.clp_ug3_ip,
            port=self.clp_ug3_port,
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )
        self.clp_sa_ip = self.cfg["USN_slave_ip"]
        self.clp_sa_port = self.cfg["USN_slave_porta"]
        self.clp_sa = ModbusClient(
            host=self.clp_sa_ip,
            port=self.clp_sa_port,
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )
        self.leitura_potencia = LeituraModbus(
            "ug{}_Gerador_PotenciaAtivaMedia".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_PM_710_Potencia_Ativa,
            op=4,
        )
        self.leitura_potencia_ug1 = LeituraModbus(
            "ug1_Gerador_PotenciaAtivaMedia",
            self.clp_ug1,
            REG_UG1_RetornosAnalogicos_MWR_PM_710_Potencia_Ativa,
            op=4,
        )
        self.leitura_setpoint_ug1 = LeituraModbus(
            "ug1_Setpoint",
            self.clp_ug1,
            REG_UG1_SaidasAnalogicas_MWW_SPPotAtiva,
            op=4
        )
        self.leitura_potencia_ug3 = LeituraModbus(
            "ug3_Gerador_PotenciaAtivaMedia",
            self.clp_ug3,
            REG_UG3_RetornosAnalogicos_MWR_PM_710_Potencia_Ativa,
            op=4,
        )
        self.leitura_setpoint_ug3 = LeituraModbus(
            "ug3_Setpoint",
            self.clp_ug3,
            REG_UG3_SaidasAnalogicas_MWW_SPPotAtiva,
            op=4
        )
        self.leitura_horimetro_hora = LeituraModbus(
            "ug{} RetornosAnalogicos_MWR_Horimetro_Gerador".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Horimetro_Gerador,
            op=4,
        )
        self.leitura_horimetro_frac = LeituraModbus(
            "ug{} RetornosAnalogicos_MWR_Horimetro_Gerador_min".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Horimetro_Gerador_min,
            op=4,
            escala=1/60
        )
        self.leitura_horimetro = LeituraSoma(
            "ug{} horímetro".format(self.id),
            self.leitura_horimetro_hora,
            self.leitura_horimetro_frac
        )
        C1 = LeituraModbusCoil(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.clp,
            registrador=REG_UG2_EntradasDigitais_MXI_DisjGeradorFechado,
        )
        C2 = LeituraModbusCoil(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.clp,
            registrador=REG_UG2_RetornosDigitais_MXR_ParandoEmAuto,
        )
        C3 = LeituraModbusCoil(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.clp,
            registrador=REG_UG2_EntradasDigitais_MXI_RV_MaquinaParada,
        )
        C4 = LeituraModbusCoil(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.clp,
            registrador=REG_UG2_RetornosDigitais_MXR_PartindoEmAuto,
        )
        self.leitura_Operacao_EtapaAtual = LeituraComposta(
            "ug{}_Operacao_EtapaAtual".format(self.id),
            leitura1=C1,
            leitura2=C2,
            leitura3=C3,
            leitura4=C4,
        )

        #Lista de condicionadores essenciais que devem ser lidos a todo momento
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        # R
        self.leitura_temperatura_fase_R = LeituraModbus("Gerador {} - temperatura fase R".format(self.id),self.clp,REG_UG2_RetornosAnalogicos_MWR_Temperatura_01,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_R
        self.condicionador_temperatura_fase_r_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_r_ug)
        
        # S
        self.leitura_temperatura_fase_S = LeituraModbus("Gerador {} - temperatura fase s".format(self.id),self.clp,REG_UG2_RetornosAnalogicos_MWR_Temperatura_02,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_S
        self.condicionador_temperatura_fase_s_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_s_ug)
        
        # T
        self.leitura_temperatura_fase_T = LeituraModbus("Gerador {} - temperatura fase T".format(self.id),self.clp,REG_UG2_RetornosAnalogicos_MWR_Temperatura_03,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_T
        self.condicionador_temperatura_fase_t_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_t_ug)
        
        # Nucleo estator
        self.leitura_temperatura_nucleo = LeituraModbus("Gerador {} - temperatura núcelo do estator".format(self.id),self.clp,REG_UG2_RetornosAnalogicos_MWR_Temperatura_04,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_nucleo
        self.condicionador_temperatura_nucleo_estator_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_nucleo_estator_ug)
        
        # MRD 1
        self.leitura_temperatura_mrd1 = LeituraModbus("Gerador {} - temperatura mancal radial dianteiro".format(self.id),self.clp,REG_UG2_RetornosAnalogicos_MWR_Temperatura_05,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_mrd1
        self.condicionador_temperatura_mancal_rad_dia_1_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_dia_1_ug)
        
        # MRT 1
        self.leitura_temperatura_mrt1 = LeituraModbus("Gerador {} - temperatura mancal radial traseiro".format(self.id),self.clp,REG_UG2_RetornosAnalogicos_MWR_Temperatura_06,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_mrt1
        self.condicionador_temperatura_mancal_rad_tra_1_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_tra_1_ug)
        
        # MRD 2
        self.leitura_temperatura_mrd2 = LeituraModbus("Gerador {} - temperatura mancal radial dianteiro 2".format(self.id),self.clp,REG_UG2_RetornosAnalogicos_MWR_Temperatura_07,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_mrd2
        self.condicionador_temperatura_mancal_rad_dia_2_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_dia_2_ug)
        
        # MRT 2
        self.leitura_temperatura_mrt2 = LeituraModbus("Gerador {} - temperatura mancal radial traseiro 2".format(self.id),self.clp,REG_UG2_RetornosAnalogicos_MWR_Temperatura_08,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_mrt2
        self.condicionador_temperatura_mancal_rad_tra_2_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_tra_2_ug)
        
        # Saída de ar
        self.leitura_temperatura_saida_de_ar = LeituraModbus("Gerador {} - saída de ar".format(self.id),self.clp,REG_UG2_RetornosAnalogicos_MWR_Temperatura_10,op=4,)
        base, limite = 100, 200
        x = self.leitura_temperatura_saida_de_ar
        self.condicionador_temperatura_saida_de_ar_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_saida_de_ar_ug)
        
        # Mancal Guia Radial
        self.leitura_temperatura_guia_radial = LeituraModbus("Gerador {} - Mancal Guia Radial".format(self.id),self.clp,REG_UG2_EntradasAnalogicas_MRR_TempMcGuiaRadial,)
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_radial
        self.condicionador_temperatura_mancal_guia_radial_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_radial_ug)
        
        # Mancal Guia escora
        self.leitura_temperatura_guia_escora = LeituraModbus("Gerador {} - Mancal Guia escora".format(self.id),self.clp,REG_UG2_EntradasAnalogicas_MRR_TempMcGuiaEscora,)
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_escora
        self.condicionador_temperatura_mancal_guia_escora_ug = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_escora_ug)
        
        # Mancal Guia contra_escora
        self.leitura_temperatura_guia_contra_escora = LeituraModbus("Gerador {} - Mancal Guia contra_escora".format(self.id),self.clp,REG_UG2_EntradasAnalogicas_MRR_TempMcGuiaContraEscora,)
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_contra_escora
        self.condicionador_temperatura_mancal_guia_contra_ug = (CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite))
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_contra_ug)
        
        # Óleo do Transformador Elevador
        self.leitura_temperatura_oleo_trafo = LeituraModbus("Gerador {} - Óleo do Transformador Elevador".format(self.id),self.clp_sa,REG_SA_EntradasAnalogicas_MRR_SA_TE_TempOleo, escala=0.1, op=4)
        base = 100
        limite = 200
        escala = 0.1
        x = self.leitura_temperatura_oleo_trafo
        self.condicionador_leitura_temperatura_oleo_trafo = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_leitura_temperatura_oleo_trafo)
        
        # CX Espiral
        self.leitura_caixa_espiral = LeituraModbus("Gerador {} - Caixa espiral".format(self.id),self.clp,REG_UG2_EntradasAnalogicas_MRR_PressK1CaixaExpiral_MaisCasas,escala=0.01,op = 4)
        base = 16.1
        limite = 15.5
        x = self.leitura_caixa_espiral
        self.condicionador_caixa_espiral_ug = CondicionadorExponencialReverso(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        if self.leitura_caixa_espiral.valor != 0.0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            self.condicionadores_atenuadores.append(self.condicionador_caixa_espiral_ug)
        
        self.leitura_ComandosDigitais_MXW_EmergenciaViaSuper = LeituraModbusCoil("ComandosDigitais_MXW_EmergenciaViaSuper", self.clp, REG_UG2_ComandosDigitais_MXW_EmergenciaViaSuper,)
        x = self.leitura_ComandosDigitais_MXW_EmergenciaViaSuper
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripEletrico = LeituraModbusCoil("RetornosDigitais_MXR_TripEletrico",self.clp,REG_UG2_RetornosDigitais_MXR_TripEletrico,)
        x = self.leitura_RetornosDigitais_MXR_TripEletrico
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_EntradasDigitais_MXI_ReleBloqA86HAtuado = LeituraModbusCoil("EntradasDigitais_MXI_ReleBloqA86HAtuado", self.clp, REG_UG2_EntradasDigitais_MXI_ReleBloqA86HAtuado)
        x = self.leitura_EntradasDigitais_MXI_ReleBloqA86HAtuado
        if not (self.etapa_atual==UNIDADE_PARADA or self.etapa_atual==UNIDADE_PARANDO):
            self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_EntradasDigitais_MXI_ReleBloqA86MAtuado = LeituraModbusCoil("EntradasDigitais_MXI_ReleBloqA86MAtuado", self.clp, REG_UG2_EntradasDigitais_MXI_ReleBloqA86MAtuado)
        x = self.leitura_EntradasDigitais_MXI_ReleBloqA86MAtuado
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SEL700G_Atuado = LeituraModbusCoil("EntradasDigitais_MXI_SEL700G_Atuado",self.clp,REG_UG2_EntradasDigitais_MXI_SEL700G_Atuado,)
        x = self.leitura_EntradasDigitais_MXI_SEL700G_Atuado
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_RV_Trip = LeituraModbusCoil("EntradasDigitais_MXI_RV_Trip",self.clp,REG_UG2_EntradasDigitais_MXI_RV_Trip,)
        x = self.leitura_EntradasDigitais_MXI_RV_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripMecanico = LeituraModbusCoil("RetornosDigitais_MXR_TripMecanico",self.clp,REG_UG2_RetornosDigitais_MXR_TripMecanico,)
        x = self.leitura_RetornosDigitais_MXR_TripMecanico
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_700G_Trip = LeituraModbusCoil("RetornosDigitais_MXR_700G_Trip",self.clp,REG_UG2_RetornosDigitais_MXR_700G_Trip,)
        x = self.leitura_RetornosDigitais_MXR_700G_Trip
        if not (self.etapa_atual==UNIDADE_PARADA or self.etapa_atual==UNIDADE_PARANDO):
            self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_EntradasDigitais_MXI_AVR_Trip = LeituraModbusCoil("EntradasDigitais_MXI_AVR_Trip",self.clp,REG_UG2_EntradasDigitais_MXI_AVR_Trip,)
        x = self.leitura_EntradasDigitais_MXI_AVR_Trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        #Lista de condiconadores que deverão ser lidaos apenas quando houver uma chamada de leitura
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG2 = LeituraModbusCoil("EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG2",self.clp_sa,REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG2,)
        x = self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa = LeituraModbusCoil("EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa",self.clp_sa,REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa,)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa = LeituraModbusCoil("EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa",self.clp_sa,REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa,)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        if self.etapa_atual==UNIDADE_SINCRONIZADA:
            self.leitura_EntradasDigitais_MXI_SA_Disj52G2_Aberto = LeituraModbusCoil("EntradasDigitais_MXI_SA_Disj52G2_Aberto",self.clp_sa,REG_SA_EntradasDigitais_MXI_SA_Disj52G2_Aberto,)
            x = self.leitura_EntradasDigitais_MXI_SA_Disj52G2_Aberto
            self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_EntradasDigitais_MXI_AVR_FalhaInterna = LeituraModbusCoil("EntradasDigitais_MXI_AVR_FalhaInterna",self.clp,REG_UG2_EntradasDigitais_MXI_AVR_FalhaInterna,)
        x = self.leitura_EntradasDigitais_MXI_AVR_FalhaInterna
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_Falta125Vcc = LeituraModbusCoil("EntradasDigitais_MXI_Falta125Vcc",self.clp,REG_UG2_EntradasDigitais_MXI_Falta125Vcc,)
        x = self.leitura_EntradasDigitais_MXI_Falta125Vcc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_Falta125VccAlimVal = LeituraModbusCoil("EntradasDigitais_MXI_Falta125VccAlimVal",self.clp,REG_UG2_EntradasDigitais_MXI_Falta125VccAlimVal,)
        x = self.leitura_EntradasDigitais_MXI_Falta125VccAlimVal
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_FalhaDisjTpsProt = LeituraModbusCoil("EntradasDigitais_MXI_FalhaDisjTpsProt",self.clp,REG_UG2_EntradasDigitais_MXI_FalhaDisjTpsProt,)
        x = self.leitura_EntradasDigitais_MXI_FalhaDisjTpsProt
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SEL700G_FalhaInterna = LeituraModbusCoil("EntradasDigitais_MXI_SEL700G_FalhaInterna",self.clp,REG_UG2_EntradasDigitais_MXI_SEL700G_FalhaInterna,)
        x = self.leitura_EntradasDigitais_MXI_SEL700G_FalhaInterna
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_NivelMAltoPocoDren = LeituraModbusCoil("EntradasDigitais_MXI_NivelMAltoPocoDren",self.clp,REG_UG2_EntradasDigitais_MXI_NivelMAltoPocoDren,)
        x = self.leitura_EntradasDigitais_MXI_NivelMAltoPocoDren
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_FreioFiltroSaturado = LeituraModbusCoil("EntradasDigitais_MXI_FreioFiltroSaturado",self.clp,REG_UG2_EntradasDigitais_MXI_FreioFiltroSaturado,)
        x = self.leitura_EntradasDigitais_MXI_FreioFiltroSaturado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_FreioSemEnergia = LeituraModbusCoil("EntradasDigitais_MXI_FreioSemEnergia",self.clp,REG_UG2_EntradasDigitais_MXI_FreioSemEnergia,)
        x = self.leitura_EntradasDigitais_MXI_FreioSemEnergia
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_FiltroPresSujo100Sujo = LeituraModbusCoil("EntradasDigitais_MXI_FiltroPresSujo100Sujo",self.clp,REG_UG2_EntradasDigitais_MXI_FiltroPresSujo100Sujo,)
        x = self.leitura_EntradasDigitais_MXI_FiltroPresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_FiltroRetSujo100Sujo = LeituraModbusCoil("EntradasDigitais_MXI_FiltroRetSujo100Sujo",self.clp,REG_UG2_EntradasDigitais_MXI_FiltroRetSujo100Sujo,)
        x = self.leitura_EntradasDigitais_MXI_FiltroRetSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35 = LeituraModbusCoil("EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35",self.clp,REG_UG2_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35,)
        x = self.leitura_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHRV_NivOleominimoPos36 = LeituraModbusCoil("EntradasDigitais_MXI_UHRV_NivOleominimoPos36",self.clp,REG_UG2_EntradasDigitais_MXI_UHRV_NivOleominimoPos36,)
        x = self.leitura_EntradasDigitais_MXI_UHRV_NivOleominimoPos36
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_ValvBorbTravada = LeituraModbusCoil("EntradasDigitais_MXI_ValvBorbTravada",self.clp,REG_UG2_EntradasDigitais_MXI_ValvBorbTravada,)
        x = self.leitura_EntradasDigitais_MXI_ValvBorbTravada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SobreVeloMecPos18 = LeituraModbusCoil("EntradasDigitais_MXI_SobreVeloMecPos18",self.clp,REG_UG2_EntradasDigitais_MXI_SobreVeloMecPos18,)
        x = self.leitura_EntradasDigitais_MXI_SobreVeloMecPos18
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_FaltaFluxoOleoMc = LeituraModbusCoil("EntradasDigitais_MXI_FaltaFluxoOleoMc",self.clp,REG_UG2_EntradasDigitais_MXI_FaltaFluxoOleoMc,)
        x = self.leitura_EntradasDigitais_MXI_FaltaFluxoOleoMc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_PalhetasDesal = LeituraModbusCoil("EntradasDigitais_MXI_PalhetasDesal",self.clp,REG_UG2_EntradasDigitais_MXI_PalhetasDesal,)
        x = self.leitura_EntradasDigitais_MXI_PalhetasDesal
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_FaltaFluxTroc = LeituraModbusCoil("EntradasDigitais_MXI_UHLM_FaltaFluxTroc",self.clp,REG_UG2_EntradasDigitais_MXI_UHLM_FaltaFluxTroc,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_FaltaFluxTroc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_FaltaPressTroc = LeituraModbusCoil("EntradasDigitais_MXI_UHLM_FaltaPressTroc",self.clp,REG_UG2_EntradasDigitais_MXI_UHLM_FaltaPressTroc,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_FaltaPressTroc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo = LeituraModbusCoil("EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo",self.clp,REG_UG2_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo = LeituraModbusCoil("EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo",self.clp,REG_UG2_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_NivelCritOleo = LeituraModbusCoil("EntradasDigitais_MXI_UHLM_NivelCritOleo",self.clp,REG_UG2_EntradasDigitais_MXI_UHLM_NivelCritOleo,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_NivelCritOleo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_NivelminOleo = LeituraModbusCoil("EntradasDigitais_MXI_UHLM_NivelminOleo",self.clp,REG_UG2_EntradasDigitais_MXI_UHLM_NivelminOleo,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_NivelminOleo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100 = LeituraModbusCoil("EntradasDigitais_MXI_FiltroPressaoBbaMecSj100",self.clp,REG_UG2_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100,)
        x = self.leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro = LeituraModbusCoil("EntradasDigitais_MXI_UHLM_FluxoMcDianteiro",self.clp,REG_UG2_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcTras = LeituraModbusCoil("EntradasDigitais_MXI_UHLM_FluxoMcTras",self.clp,REG_UG2_EntradasDigitais_MXI_UHLM_FluxoMcTras,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcTras
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel = LeituraModbusCoil("EntradasDigitais_MXI_QCAUG_Falha380VcaPainel",self.clp,REG_UG2_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel,)
        x = self.leitura_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_EntradasDigitais_MXI_QCAUG_TripDisj52A1 = LeituraModbusCoil("EntradasDigitais_MXI_QCAUG_TripDisj52A1",self.clp,REG_UG2_EntradasDigitais_MXI_QCAUG_TripDisj52A1,)
        x = self.leitura_EntradasDigitais_MXI_QCAUG_TripDisj52A1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_TripBomba1 = LeituraModbusCoil("EntradasDigitais_MXI_UHLM_TripBomba1",self.clp,REG_UG2_EntradasDigitais_MXI_UHLM_TripBomba1,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_TripBomba1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHLM_TripBomba2 = LeituraModbusCoil("EntradasDigitais_MXI_UHLM_TripBomba2",self.clp,REG_UG2_EntradasDigitais_MXI_UHLM_TripBomba2,)
        x = self.leitura_EntradasDigitais_MXI_UHLM_TripBomba2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHRV_TripBomba1 = LeituraModbusCoil("EntradasDigitais_MXI_UHRV_TripBomba1",self.clp,REG_UG2_EntradasDigitais_MXI_UHRV_TripBomba1,)
        x = self.leitura_EntradasDigitais_MXI_UHRV_TripBomba1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_UHRV_TripBomba2 = LeituraModbusCoil("EntradasDigitais_MXI_UHRV_TripBomba2",self.clp,REG_UG2_EntradasDigitais_MXI_UHRV_TripBomba2,)
        x = self.leitura_EntradasDigitais_MXI_UHRV_TripBomba2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_TripAlimPainelFreio = LeituraModbusCoil("EntradasDigitais_MXI_TripAlimPainelFreio",self.clp,REG_UG2_EntradasDigitais_MXI_TripAlimPainelFreio,)
        x = self.leitura_EntradasDigitais_MXI_TripAlimPainelFreio
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_QCAUG_TripDisjAgrup = LeituraModbusCoil("EntradasDigitais_MXI_QCAUG_TripDisjAgrup",self.clp,REG_UG2_EntradasDigitais_MXI_QCAUG_TripDisjAgrup,)
        x = self.leitura_EntradasDigitais_MXI_QCAUG_TripDisjAgrup
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_FalhaAcionFechaValvBorb = LeituraModbusCoil("RetornosDigitais_MXR_FalhaAcionFechaValvBorb",self.clp,REG_UG2_RetornosDigitais_MXR_FalhaAcionFechaValvBorb,)
        x = self.leitura_RetornosDigitais_MXR_FalhaAcionFechaValvBorb
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1 = LeituraModbusCoil("RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1",self.clp,REG_UG2_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1,)
        x = self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2 = LeituraModbusCoil("RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2",self.clp,REG_UG2_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2,)
        x = self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1 = LeituraModbusCoil("RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1",self.clp,REG_UG2_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1,)
        x = self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2 = LeituraModbusCoil("RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2",self.clp,REG_UG2_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2,)
        x = self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripTempGaxeteiro = LeituraModbusCoil("RetornosDigitais_MXR_TripTempGaxeteiro",self.clp,REG_UG2_RetornosDigitais_MXR_TripTempGaxeteiro,)
        x = self.leitura_RetornosDigitais_MXR_TripTempGaxeteiro
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripTempMcGuiaRadial = LeituraModbusCoil("RetornosDigitais_MXR_TripTempMcGuiaRadial",self.clp,REG_UG2_RetornosDigitais_MXR_TripTempMcGuiaRadial,)
        x = self.leitura_RetornosDigitais_MXR_TripTempMcGuiaRadial
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripTempMcGuiaEscora = LeituraModbusCoil("RetornosDigitais_MXR_TripTempMcGuiaEscora",self.clp,REG_UG2_RetornosDigitais_MXR_TripTempMcGuiaEscora,)
        x = self.leitura_RetornosDigitais_MXR_TripTempMcGuiaEscora
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripTempMcGuiaContraEscora = (LeituraModbusCoil("RetornosDigitais_MXR_TripTempMcGuiaContraEscora",self.clp,REG_UG2_RetornosDigitais_MXR_TripTempMcGuiaContraEscora,))
        x = self.leitura_RetornosDigitais_MXR_TripTempMcGuiaContraEscora
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripTempUHRV = LeituraModbusCoil("RetornosDigitais_MXR_TripTempUHRV",self.clp,REG_UG2_RetornosDigitais_MXR_TripTempUHRV,)
        x = self.leitura_RetornosDigitais_MXR_TripTempUHRV
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripTempUHLM = LeituraModbusCoil("RetornosDigitais_MXR_TripTempUHLM",self.clp,REG_UG2_RetornosDigitais_MXR_TripTempUHLM,)
        x = self.leitura_RetornosDigitais_MXR_TripTempUHLM
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripVibr1 = LeituraModbusCoil("RetornosDigitais_MXR_TripVibr1",self.clp,REG_UG2_RetornosDigitais_MXR_TripVibr1,)
        x = self.leitura_RetornosDigitais_MXR_TripVibr1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_TripVibr2 = LeituraModbusCoil("RetornosDigitais_MXR_TripVibr2",self.clp,REG_UG2_RetornosDigitais_MXR_TripVibr2,)
        x = self.leitura_RetornosDigitais_MXR_TripVibr2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_FalhaIbntDisjGer = LeituraModbusCoil("RetornosDigitais_MXR_FalhaIbntDisjGer",self.clp,REG_UG2_RetornosDigitais_MXR_FalhaIbntDisjGer,)
        x = self.leitura_RetornosDigitais_MXR_FalhaIbntDisjGer
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_CLP_Falha = LeituraModbusCoil("RetornosDigitais_MXR_CLP_Falha",self.clp,REG_UG2_RetornosDigitais_MXR_CLP_Falha,)
        x = self.leitura_RetornosDigitais_MXR_CLP_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_Q_Negativa = LeituraModbusCoil("RetornosDigitais_MXR_Q_Negativa",self.clp,REG_UG2_RetornosDigitais_MXR_Q_Negativa,)
        x = self.leitura_RetornosDigitais_MXR_Q_Negativa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.RetornosDigitais_MXR_TripPressaoCaixaEspiral = LeituraModbusCoil( "RetornosDigitais_MXR_TripPressaoCaixaEspiral", self.clp, REG_UG2_RetornosDigitais_MXR_TripPressaoCaixaEspiral, )
        x = self.RetornosDigitais_MXR_TripPressaoCaixaEspiral
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        # Inicializa as variáveis de controle PI para operação TDA Offline
        self.cx_controle_p = (self.leitura_caixa_espiral.valor - self.cfg["press_cx_alvo"]) * self.cfg["cx_kp"]
        self.cx_ajuste_ie = (self.leitura_potencia.valor + self.leitura_potencia_ug1.valor + self.leitura_potencia_ug3.valor) / self.cfg["pot_maxima_alvo"]
        self.cx_controle_i = self.cx_ajuste_ie - self.cx_controle_p

    def controle_cx_espiral(self):
        # Calcula PI
        self.erro_press_cx = 0
        self.erro_press_cx = self.leitura_caixa_espiral.valor - self.cfg["press_cx_alvo"]

        self.logger.debug("[UG{}] Pressão Alvo: {:0.3f}, Recente: {:0.3f}".format(self.id, self.cfg["press_cx_alvo"], self.leitura_caixa_espiral.valor))

        self.cx_controle_p = self.cfg["cx_kp"] * self.erro_press_cx
        self.cx_controle_i = max(min((self.cfg["cx_ki"] * self.erro_press_cx) + self.cx_controle_i, 1), 0)
        saida_pi = self.cx_controle_p + self.cx_controle_i
        
        self.logger.debug("[UG{}] PI: {:0.3f} <-- P:{:0.3f} + I:{:0.3f}; ERRO={}".format(self.id, saida_pi, self.cx_controle_p, self.cx_controle_i, self.erro_press_cx))

        # Calcula o integrador de estabilidade e limita
        self.cx_controle_ie = max(min(saida_pi + self.cx_ajuste_ie * self.cfg["cx_kie"], 1), 0)

        # Arredondamento e limitação
        pot_alvo = max(min(round(self.cfg["pot_maxima_ug2"] * self.cx_controle_ie, 5), self.cfg["pot_maxima_ug2"],),self.cfg["pot_minima"],)

        self.logger.debug("[UG{}] Pot alvo: {:0.3f}".format(self.id, pot_alvo))

        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = pot_alvo

        self.logger.debug("Pot alvo = {}".format(pot_alvo))

        pot_medidor = self.leituras.potencia_ativa_kW.valor

        self.logger.debug("Pot no medidor = {}".format(pot_medidor))

        print("\nPotência medidor antes: ", pot_medidor)

        # implementação nova
        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])

        pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

        print("\nPotência medidor depois: ", pot_medidor, "\n")

        try:
            if pot_medidor > self.cfg["pot_maxima_alvo"] * 0.97:
                pot_alvo = self.pot_alvo_anterior * (1 - 0.5 * ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))
                
                print("\nPotência alvo: ", pot_alvo, "\n")
        except TypeError as e:
            logger.info(repr(e))

        self.pot_alvo_anterior = pot_alvo

        if self.leitura_caixa_espiral.valor >= 15.5:
            self.enviar_setpoint(pot_alvo)
        else:
            self.enviar_setpoint(0)
        
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
                self.leitura_setpoint_ug1.valor,
                self.leitura_potencia_ug1.valor,
                self.setpoint,
                self.leitura_potencia.valor,
                0,
                0,
                1,
                self.leitura_setpoint_ug3.valor,
                self.leitura_potencia_ug3.valor,
                self.cfg["cx_kp"],
                self.cfg["cx_ki"],
                self.cfg["cx_kie"],
                self.cx_controle_ie,
            )
        except Exception as e:
            logger.exception(e)

        print("")

    def acionar_trip_logico(self) -> bool:
        """
        Envia o comando de acionamento do TRIP para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.debug(
                "[UG{}] Acionando sinal (via rede) de TRIP.".format(self.id)
            )
            response = self.clp.write_single_coil(
                REG_UG2_ComandosDigitais_MXW_EmergenciaViaSuper, 1
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
            self.logger.debug("[UG{}] Removendo sinal (via rede) de TRIP.".format(self.id))
            response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_ResetGeral, 1)
            response = self.clp.write_single_coil(REG_UG2_EntradasDigitais_MXI_ReleBloqA86HAtuado, 0)
            response = self.clp.write_single_coil(REG_UG2_EntradasDigitais_MXI_ReleBloqA86MAtuado, 0)
            response = self.clp.write_single_coil(REG_UG2_RetornosDigitais_MXR_700G_Trip, 0)
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
            response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_Cala_Sirene, 1)
            if self.clp_sa.read_coils(REG_SA_ComandosDigitais_MXW_Liga_DJ1)[0] == 0:
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
            
            # na simulação, a condição a seguir, impede a partida das ugs. Retirar comentário quando for aplicar em campo
            if not self.clp.read_discrete_inputs(REG_UG2_COND_PART,1)[0]:
                self.logger.debug("[UG{}] Máquina sem condição de partida. Irá partir quando as condições forem reestabelecidas.".format(self.id))
                return True
            elif self.clp_sa.read_coils(REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52A1Fechado)[0] != 0:
                self.logger.debug("[UG{}] O Disjuntor 52A1 está aberto. Para partir a máquina, o mesmo deverá ser fechado.")
                return True
            elif not self.etapa_atual == UNIDADE_SINCRONIZADA:
                self.logger.info("[UG{}] Enviando comando de partida.".format(self.id))
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_ResetGeral, 1)
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_ResetRele700G, 1)
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_ResetReleBloq86H, 1)
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_ResetReleBloq86M, 1)
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_ResetReleRT, 1)
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_ResetRV, 1)
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_IniciaPartida, 1)
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_Cala_Sirene, 1)
                self.enviar_setpoint(self.setpoint)
            else:
                self.logger.debug("[UG{}] A unidade já está sincronizada.".format(self.id))
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_Cala_Sirene, 1)

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
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_AbortaPartida, 1)
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_AbortaSincronismo, 1)
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_IniciaParada, 1)
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_Cala_Sirene, 1)
                self.enviar_setpoint(self.setpoint)
            else:
                self.logger.debug("[UG{}] A unidade já está parada.".format(self.id))
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_Cala_Sirene, 1)

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
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_ResetGeral, 1)
                response = self.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_Cala_Sirene, 1)
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

            if self.limpeza_grade:
                self.setpoint_minimo = self.cfg["pot_limpeza_grade"]
            else:
                self.setpoint_minimo = self.cfg["pot_minima"]
            self.setpoint_maximo = self.cfg["pot_maxima_ug{}".format(self.id)]

            self.setpoint = int(setpoint_kw)
            self.logger.debug("[UG{}] Enviando setpoint {} kW.".format(self.id, int(self.setpoint)))
            response = False
            if self.setpoint > 1:
                response = self.clp.write_single_coil(
                    REG_UG2_ComandosDigitais_MXW_ResetGeral, 1
                )
                response = self.clp.write_single_coil(
                    REG_UG2_ComandosDigitais_MXW_RV_RefRemHabilita, 1
                )
                response = self.clp.write_single_register(
                    REG_UG2_SaidasAnalogicas_MWW_SPPotAtiva, self.setpoint
                )

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
        DataBank.set_words(
            self.cfg["REG_MOA_OUT_STATE_UG{}".format(self.id)],
            [self.codigo_state],
        )
        DataBank.set_words(
            self.cfg["REG_MOA_OUT_ETAPA_UG{}".format(self.id)],
            [self.etapa_atual],
        )
        
    def interstep(self) -> None:
        if (not self.avisou_emerg_voip) and (self.condicionador_caixa_espiral_ug.valor > 0.1):
            self.avisou_emerg_voip = True

        elif self.condicionador_caixa_espiral_ug.valor < 0.05:
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

        if self.leitura_temperatura_nucleo.valor >= self.condicionador_temperatura_nucleo_estator_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Núcleo Estator da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_nucleo_estator_ug.valor_base, self.leitura_temperatura_nucleo.valor))
        if self.leitura_temperatura_nucleo.valor >= 0.9*(self.condicionador_temperatura_nucleo_estator_ug.valor_limite - self.condicionador_temperatura_nucleo_estator_ug.valor_base) + self.condicionador_temperatura_nucleo_estator_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Núcleo Estator da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_nucleo_estator_ug.valor_limite, self.leitura_temperatura_nucleo.valor))

        if self.leitura_temperatura_mrd1.valor >= self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Radial Dianteiro 1 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_base, self.leitura_temperatura_mrd1.valor))
        if self.leitura_temperatura_mrd1.valor >= 0.9*(self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_limite - self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_base) + self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Radial Dianteiro 1 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_rad_dia_1_ug.valor_limite, self.leitura_temperatura_mrd1.valor))

        if self.leitura_temperatura_mrt1.valor >= self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Radial Traseiro 1 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_base, self.leitura_temperatura_mrt1.valor))
        if self.leitura_temperatura_mrt1.valor >= 0.9*(self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_limite - self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_base) + self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Radial Traseiro 1 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_rad_tra_1_ug.valor_limite, self.leitura_temperatura_mrt1.valor))

        if self.leitura_temperatura_mrd2.valor >= self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Radial Dianteiro 2 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_base, self.leitura_temperatura_mrd2.valor))
        if self.leitura_temperatura_mrd2.valor >= 0.9*(self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_limite - self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_base) + self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Radial Dianteiro 2 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_rad_dia_2_ug.valor_limite, self.leitura_temperatura_mrd2.valor))

        if self.leitura_temperatura_mrt2.valor >= self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Radial Traseiro 2 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_base, self.leitura_temperatura_mrt2.valor))
        if self.leitura_temperatura_mrt2.valor >= 0.9*(self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_limite - self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_base) + self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Radial Traseiro 2 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_rad_tra_2_ug.valor_limite, self.leitura_temperatura_mrt2.valor))

        if self.leitura_temperatura_saida_de_ar.valor >= self.condicionador_temperatura_saida_de_ar_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura da Saída de Ar da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.leitura_temperatura_saida_de_ar.valor, self.condicionador_temperatura_saida_de_ar_ug.valor_base))
        if self.leitura_temperatura_saida_de_ar.valor >= 0.9*(self.condicionador_temperatura_saida_de_ar_ug.valor_limite - self.condicionador_temperatura_saida_de_ar_ug.valor_base) + self.condicionador_temperatura_saida_de_ar_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura da Saída de Ar da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_saida_de_ar_ug.valor_limite, self.leitura_temperatura_saida_de_ar.valor))

        if self.leitura_temperatura_guia_radial.valor >= self.condicionador_temperatura_mancal_guia_radial_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Guia Radial da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_radial_ug.valor_base, self.leitura_temperatura_guia_radial.valor))
        if self.leitura_temperatura_guia_radial.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_radial_ug.valor_limite - self.condicionador_temperatura_mancal_guia_radial_ug.valor_base) + self.condicionador_temperatura_mancal_guia_radial_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Guia Radial da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_radial_ug.valor_limite, self.leitura_temperatura_guia_radial.valor))

        if self.leitura_temperatura_guia_escora.valor >= self.condicionador_temperatura_mancal_guia_escora_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Guia Escora da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_escora_ug.valor_base, self.leitura_temperatura_guia_escora.valor))
        if self.leitura_temperatura_guia_escora.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_escora_ug.valor_limite - self.condicionador_temperatura_mancal_guia_escora_ug.valor_base) + self.condicionador_temperatura_mancal_guia_escora_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Guia Escora da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_escora_ug.valor_limite, self.leitura_temperatura_guia_escora.valor))

        if self.leitura_temperatura_guia_contra_escora.valor >= self.condicionador_temperatura_mancal_guia_contra_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Guia Contra Escora da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_contra_ug.valor_base, self.leitura_temperatura_guia_contra_escora.valor))
        if self.leitura_temperatura_guia_contra_escora.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_contra_ug.valor_limite - self.condicionador_temperatura_mancal_guia_contra_ug.valor_base) + self.condicionador_temperatura_mancal_guia_contra_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Guia Contra Escora da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_contra_ug.valor_limite, self.leitura_temperatura_guia_contra_escora.valor))

        if self.leitura_temperatura_oleo_trafo.valor >= self.condicionador_leitura_temperatura_oleo_trafo.valor_base:
            self.logger.warning("[UG{}] A temperatura do Óleo do Transformador Elevador da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_leitura_temperatura_oleo_trafo.valor_base, self.leitura_temperatura_oleo_trafo.valor))
        if self.leitura_temperatura_oleo_trafo.valor >= 0.9*(self.condicionador_leitura_temperatura_oleo_trafo.valor_limite - self.condicionador_leitura_temperatura_oleo_trafo.valor_base) + self.condicionador_leitura_temperatura_oleo_trafo.valor_base:
            self.logger.critical("[UG{}] A temperatura do Óleo do Transformador Elevador da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_leitura_temperatura_oleo_trafo.valor_limite, self.leitura_temperatura_oleo_trafo.valor))

        if self.leitura_caixa_espiral.valor <= self.condicionador_caixa_espiral_ug.valor_base and self.leitura_caixa_espiral.valor != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            self.logger.warning("[UG{}] A pressão Caixa Espiral da UG passou do valor base! ({:03.2f} KGf/m2) | Leitura: {:03.2f}".format(self.id, self.condicionador_caixa_espiral_ug.valor_base, self.leitura_caixa_espiral.valor))
        if self.leitura_caixa_espiral.valor <= 16.1 and self.leitura_caixa_espiral.valor != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            self.logger.critical("[UG{}] A pressão Caixa Espiral da UG está muito próxima do limite! ({:03.2f} KGf/m2) | Leitura: {:03.2f} KGf/m2".format(self.id, self.condicionador_caixa_espiral_ug.valor_limite, self.leitura_caixa_espiral.valor))

    def leituras_por_hora(self):
        self.leitura_EntradasDigitais_MXI_FreioPastilhaGasta = LeituraModbusCoil( "EntradasDigitais_MXI_FreioPastilhaGasta", self.clp, REG_UG2_EntradasDigitais_MXI_FreioPastilhaGasta )
        if self.leitura_EntradasDigitais_MXI_FreioPastilhaGasta.valor != 0:
            self.logger.warning("[UG{}] O sensor de Freio da UG retornou que a Pastilha está gasta, favor considerar troca.".format(self.id))

        self.leitura_EntradasDigitais_MXI_FiltroPresSujo75Troc = LeituraModbusCoil( "EntradasDigitais_MXI_FiltroPresSujo75Troc", self.clp, REG_UG2_EntradasDigitais_MXI_FiltroPresSujo75Troc )
        if self.leitura_EntradasDigitais_MXI_FiltroPresSujo75Troc.valor != 0:
            self.logger.warning("[UG{}] O sensor do Filtro de Pressão UHRV retornou que o filtro está 75% sujo, favor considerar troca.".format(self.id))

        self.leitura_EntradasDigitais_MXI_FiltroRetSujo75Troc = LeituraModbusCoil( "EntradasDigitais_MXI_FiltroRetSujo75Troc", self.clp, REG_UG2_EntradasDigitais_MXI_FiltroRetSujo75Troc )
        if self.leitura_EntradasDigitais_MXI_FiltroRetSujo75Troc.valor != 0:
            self.logger.warning("[UG{}] O sensor do Filtro de Retorno UHRV retornou que o filtro está 75% sujo, favor considerar troca.".format(self.id))

        self.leitura_EntradasDigitais_MXI_UHLMFilt1PresSujo75Troc = LeituraModbusCoil( "EntradasDigitais_MXI_UHLMFilt1PresSujo75Troc", self.clp, REG_UG2_EntradasDigitais_MXI_UHLM_Filt1PresSujo75Troc )
        if self.leitura_EntradasDigitais_MXI_UHLMFilt1PresSujo75Troc.valor != 0:
            self.logger.warning("[UG{}] O sensor do Filtro 1 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.".format(self.id))

        self.leitura_EntradasDigitais_MXI_UHLMFilt2PresSujo75Troc = LeituraModbusCoil( "EntradasDigitais_MXI_UHLMFilt2PresSujo75Troc", self.clp, REG_UG2_EntradasDigitais_MXI_UHLM_Filt2PresSujo75Troc )
        if self.leitura_EntradasDigitais_MXI_UHLMFilt2PresSujo75Troc.valor != 0:
            self.logger.warning("[UG{}] O sensor do Filtro 2 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.".format(self.id))

        self.leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj75 = LeituraModbusCoil( "EntradasDigitais_MXI_FiltroPressaoBbaMecSj75", self.clp, REG_UG2_EntradasDigitais_MXI_FiltroPressaoBbaMecSj75 )
        if self.leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj75.valor != 0:
            self.logger.warning("[UG{}] O sensor do Filtro de Pressão da Bomba Mecânica retornou que o filtro está 75% sujo, favor considerar troca.".format(self.id))

        self.leitura_EntradasDigitais_MXI_TripPartRes = LeituraModbusCoil( "EntradasDigitais_MXI_TripPartRes", self.clp, REG_UG2_EntradasDigitais_MXI_TripPartRes )
        if self.leitura_EntradasDigitais_MXI_TripPartRes.valor != 0:
            self.logger.warning("[UG{}] O sensor TripPartRes retornou valor 1.".format(self.id))

        # deve enviar aviso por voip
        self.leitura_EntradasDigitais_MXI_FreioCmdRemoto = LeituraModbusCoil( "EntradasDigitais_MXI_FreioCmdRemoto", self.clp, REG_UG2_EntradasDigitais_MXI_FreioCmdRemoto )
        if self.leitura_EntradasDigitais_MXI_FreioCmdRemoto.valor == 0 and self.FreioCmdRemoto == True:
            self.logger.warning("[UG{}] O sensor de freio da UG saiu do modo remoto, favor analisar a situação.".format(self.id))
            self.FreioCmdRemoto = False
            self.acionar_voip = True
        elif self.leitura_EntradasDigitais_MXI_FreioCmdRemoto.valor == 1 and self.FreioCmdRemoto == False:
            self.FreioCmdRemoto = True

        self.leitura_EntradasDigitais_MXI_QCAUG2_Remoto = LeituraModbusCoil( "EntradasDigitais_MXI_QCAUG2_Remoto", self.clp, REG_UG2_EntradasDigitais_MXI_QCAUG2_Remoto )
        if self.leitura_EntradasDigitais_MXI_QCAUG2_Remoto.valor == 0 and self.QCAUGRemoto == True:
            self.logger.warning("[UG{}] O compressor da UG saiu do modo remoto, favor analisar a situação.".format(self.id))
            self.QCAUGRemoto = False
            self.acionar_voip = True
        elif self.leitura_EntradasDigitais_MXI_QCAUG2_Remoto.valor == 1 and self.QCAUGRemoto == False:
            self.QCAUGRemoto = True
        
        return True