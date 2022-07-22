import json
import os
from unittest.mock import MagicMock
from src.Condicionadores import *
from src.Leituras import *
from src.LeiturasUSN import *
from src.UnidadeDeGeracao import *
from pyModbusTCP.server import DataBank, ModbusServer
from src.mensageiro import voip

class UnidadeDeGeracao3(UnidadeDeGeracao):
    def __init__(self, id, cfg=None, leituras_usina=None):
        super().__init__(id)

        if not cfg or not leituras_usina:
            raise ValueError
        else:
            self.cfg = cfg
            self.leituras_usina = leituras_usina

        self.setpoint_minimo = self.cfg["pot_minima"]
        self.setpoint_maximo = self.cfg["pot_maxima_ug{}".format(self.id)]

        self.clp_ip = self.cfg["UG3_slave_ip"]
        self.clp_port = self.cfg["UG3_slave_porta"]
        self.clp = ModbusClient(
            host=self.clp_ip,
            port=self.clp_port,
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )
        self.clp_sa_ip = self.cfg["USN_slave_ip"]
        self.clp_sa_port = self.cfg["USN_slave_porta"]
        self.clp_sa = ModbusClient(
            host=self.clp_ip,
            port=self.clp_port,
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )
        self.clp_tda_ip = self.cfg["TDA_slave_ip"]
        self.clp_tda_port = self.cfg["TDA_slave_porta"]
        self.clp_tda = ModbusClient(
            host=self.clp_ip,
            port=self.clp_port,
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )
        self.__last_EtapaAtual = 0
        self.enviar_trip_eletrico = False
        self.avisou_emerg_voip = False

        self.leitura_potencia = LeituraModbus(
            "ug{}_Gerador_PotenciaAtivaMedia".format(self.id),
            self.clp,
            REG_UG3_RetornosAnalogicos_MWR_PM_710_Potencia_Ativa,
            op=4,
        )
        
        self.leitura_horimetro_hora = LeituraModbus(
            "ug{} RetornosAnalogicos_MWR_Horimetro_Gerador".format(self.id),
            self.clp,
            REG_UG3_RetornosAnalogicos_MWR_Horimetro_Gerador,
            op=4,
        )
        self.leitura_horimetro_frac = LeituraModbus(
            "ug{} RetornosAnalogicos_MWR_Horimetro_Gerador_min".format(self.id),
            self.clp,
            REG_UG3_RetornosAnalogicos_MWR_Horimetro_Gerador_min,
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
            registrador=REG_UG3_EntradasDigitais_MXI_DisjGeradorFechado,
        )
        C2 = LeituraModbusCoil(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.clp,
            registrador=REG_UG3_RetornosDigitais_MXR_ParandoEmAuto,
        )
        C3 = LeituraModbusCoil(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.clp,
            registrador=REG_UG3_EntradasDigitais_MXI_RV_MaquinaParada,
        )
        C4 = LeituraModbusCoil(
            descr="MXR_PartindoEmAuto",
            modbus_client=self.clp,
            registrador=REG_UG3_RetornosDigitais_MXR_PartindoEmAuto,
        )
        self.leitura_Operacao_EtapaAtual = LeituraComposta(
            "ug{}_Operacao_EtapaAtual".format(self.id),
            leitura1=C1,
            leitura2=C2,
            leitura3=C3,
            leitura4=C4,
        )

        self.leitura_EntradasDigitais_MXI_RV_Trip = LeituraModbusCoil(
            "EntradasDigitais_MXI_RV_Trip",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_RV_Trip,
        )
        x = self.leitura_EntradasDigitais_MXI_RV_Trip
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_AVR_Trip = LeituraModbusCoil(
            "EntradasDigitais_MXI_AVR_Trip",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_AVR_Trip,
        )
        x = self.leitura_EntradasDigitais_MXI_AVR_Trip
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_AVR_FalhaInterna = LeituraModbusCoil(
            "EntradasDigitais_MXI_AVR_FalhaInterna",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_AVR_FalhaInterna,
        )
        x = self.leitura_EntradasDigitais_MXI_AVR_FalhaInterna
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_Falta125Vcc = LeituraModbusCoil(
            "EntradasDigitais_MXI_Falta125Vcc",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_Falta125Vcc,
        )
        x = self.leitura_EntradasDigitais_MXI_Falta125Vcc
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_Falta125VccCom = LeituraModbusCoil(
            "EntradasDigitais_MXI_Falta125VccCom",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_Falta125VccCom,
        )
        x = self.leitura_EntradasDigitais_MXI_Falta125VccCom
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_Falta125VccAlimVal = LeituraModbusCoil(
            "EntradasDigitais_MXI_Falta125VccAlimVal",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_Falta125VccAlimVal,
        )
        x = self.leitura_EntradasDigitais_MXI_Falta125VccAlimVal
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_FalhaDisjTpsProt = LeituraModbusCoil(
            "EntradasDigitais_MXI_FalhaDisjTpsProt",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_FalhaDisjTpsProt,
        )
        x = self.leitura_EntradasDigitais_MXI_FalhaDisjTpsProt
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_SEL700G_Atuado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SEL700G_Atuado",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_SEL700G_Atuado,
        )
        x = self.leitura_EntradasDigitais_MXI_SEL700G_Atuado
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_SEL700G_FalhaInterna = LeituraModbusCoil(
            "EntradasDigitais_MXI_SEL700G_FalhaInterna",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_SEL700G_FalhaInterna,
        )
        x = self.leitura_EntradasDigitais_MXI_SEL700G_FalhaInterna
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_NivelMAltoPocoDren = LeituraModbusCoil(
            "EntradasDigitais_MXI_NivelMAltoPocoDren",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_NivelMAltoPocoDren,
        )
        x = self.leitura_EntradasDigitais_MXI_NivelMAltoPocoDren
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_FreioFiltroSaturado = LeituraModbusCoil(
            "EntradasDigitais_MXI_FreioFiltroSaturado",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_FreioFiltroSaturado,
        )
        x = self.leitura_EntradasDigitais_MXI_FreioFiltroSaturado
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_FreioSemEnergia = LeituraModbusCoil(
            "EntradasDigitais_MXI_FreioSemEnergia",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_FreioSemEnergia,
        )
        x = self.leitura_EntradasDigitais_MXI_FreioSemEnergia
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHRV_PressCriticaPos321 = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHRV_PressCriticaPos321",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHRV_PressCriticaPos321,
        )
        x = self.leitura_EntradasDigitais_MXI_UHRV_PressCriticaPos321
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_FiltroPresSujo100Sujo = LeituraModbusCoil(
            "EntradasDigitais_MXI_FiltroPresSujo100Sujo",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_FiltroPresSujo100Sujo,
        )
        x = self.leitura_EntradasDigitais_MXI_FiltroPresSujo100Sujo
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_FiltroRetSujo100Sujo = LeituraModbusCoil(
            "EntradasDigitais_MXI_FiltroRetSujo100Sujo",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_FiltroRetSujo100Sujo,
        )
        x = self.leitura_EntradasDigitais_MXI_FiltroRetSujo100Sujo
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35 = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35,
        )
        x = self.leitura_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHRV_NivOleominimoPos36 = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHRV_NivOleominimoPos36",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHRV_NivOleominimoPos36,
        )
        x = self.leitura_EntradasDigitais_MXI_UHRV_NivOleominimoPos36
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_ValvBorbTravada = LeituraModbusCoil(
            "EntradasDigitais_MXI_ValvBorbTravada",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_ValvBorbTravada,
        )
        x = self.leitura_EntradasDigitais_MXI_ValvBorbTravada
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_SobreVeloMecPos18 = LeituraModbusCoil(
            "EntradasDigitais_MXI_SobreVeloMecPos18",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_SobreVeloMecPos18,
        )
        x = self.leitura_EntradasDigitais_MXI_SobreVeloMecPos18
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_FaltaFluxoOleoMc = LeituraModbusCoil(
            "EntradasDigitais_MXI_FaltaFluxoOleoMc",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_FaltaFluxoOleoMc,
        )
        x = self.leitura_EntradasDigitais_MXI_FaltaFluxoOleoMc
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_PalhetasDesal = LeituraModbusCoil(
            "EntradasDigitais_MXI_PalhetasDesal",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_PalhetasDesal,
        )
        x = self.leitura_EntradasDigitais_MXI_PalhetasDesal
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHLM_FaltaFluxTroc = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHLM_FaltaFluxTroc",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHLM_FaltaFluxTroc,
        )
        x = self.leitura_EntradasDigitais_MXI_UHLM_FaltaFluxTroc
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHLM_FaltaPressTroc = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHLM_FaltaPressTroc",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHLM_FaltaPressTroc,
        )
        x = self.leitura_EntradasDigitais_MXI_UHLM_FaltaPressTroc
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHLMFilt1PresSujo100Sujo = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHLMFilt1PresSujo100Sujo",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHLMFilt1PresSujo100Sujo,
        )
        x = self.leitura_EntradasDigitais_MXI_UHLMFilt1PresSujo100Sujo
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHLMFilt2PresSujo100Sujo = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHLMFilt2PresSujo100Sujo",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHLMFilt2PresSujo100Sujo,
        )
        x = self.leitura_EntradasDigitais_MXI_UHLMFilt2PresSujo100Sujo
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHLM_NivelCritOleo = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHLM_NivelCritOleo",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHLM_NivelCritOleo,
        )
        x = self.leitura_EntradasDigitais_MXI_UHLM_NivelCritOleo
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHLM_NivelminOleo = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHLM_NivelminOleo",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHLM_NivelminOleo,
        )
        x = self.leitura_EntradasDigitais_MXI_UHLM_NivelminOleo
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100 = LeituraModbusCoil(
            "EntradasDigitais_MXI_FiltroPressaoBbaMecSj100",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100,
        )
        x = self.leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHLM_FluxoMcDianteiro",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro,
        )
        x = self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcTras = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHLM_FluxoMcTras",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHLM_FluxoMcTras,
        )
        x = self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcTras
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel = LeituraModbusCoil(
            "EntradasDigitais_MXI_QCAUG_Falha380VcaPainel",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel,
        )
        x = self.leitura_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_QCAUG_TripDisj52A1 = LeituraModbusCoil(
            "EntradasDigitais_MXI_QCAUG_TripDisj52A1",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_QCAUG_TripDisj52A1,
        )
        x = self.leitura_EntradasDigitais_MXI_QCAUG_TripDisj52A1
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHLM_TripBomba1 = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHLM_TripBomba1",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHLM_TripBomba1,
        )
        x = self.leitura_EntradasDigitais_MXI_UHLM_TripBomba1
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHLM_TripBomba2 = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHLM_TripBomba2",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHLM_TripBomba2,
        )
        x = self.leitura_EntradasDigitais_MXI_UHLM_TripBomba2
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHRV_TripBomba1 = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHRV_TripBomba1",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHRV_TripBomba1,
        )
        x = self.leitura_EntradasDigitais_MXI_UHRV_TripBomba1
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_UHRV_TripBomba2 = LeituraModbusCoil(
            "EntradasDigitais_MXI_UHRV_TripBomba2",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_UHRV_TripBomba2,
        )
        x = self.leitura_EntradasDigitais_MXI_UHRV_TripBomba2
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_TripAlimPainelFreio = LeituraModbusCoil(
            "EntradasDigitais_MXI_TripAlimPainelFreio",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_TripAlimPainelFreio,
        )
        x = self.leitura_EntradasDigitais_MXI_TripAlimPainelFreio
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_EntradasDigitais_MXI_QCAUG_TripDisjAgrup = LeituraModbusCoil(
            "EntradasDigitais_MXI_QCAUG_TripDisjAgrup",
            self.clp,
            REG_UG3_EntradasDigitais_MXI_QCAUG_TripDisjAgrup,
        )
        x = self.leitura_EntradasDigitais_MXI_QCAUG_TripDisjAgrup
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_TripEletrico = LeituraModbusCoil(
            "RetornosDigitais_MXR_TripEletrico",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_TripEletrico,
        )
        x = self.leitura_RetornosDigitais_MXR_TripEletrico
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_TripMecanico = LeituraModbusCoil(
            "RetornosDigitais_MXR_TripMecanico",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_TripMecanico,
        )
        x = self.leitura_RetornosDigitais_MXR_TripMecanico
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_FalhaAcionFechaValvBorb = LeituraModbusCoil(
            "RetornosDigitais_MXR_FalhaAcionFechaValvBorb",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_FalhaAcionFechaValvBorb,
        )
        x = self.leitura_RetornosDigitais_MXR_FalhaAcionFechaValvBorb
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1 = LeituraModbusCoil(
            "RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1,
        )
        x = self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2 = LeituraModbusCoil(
            "RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2,
        )
        x = self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1 = LeituraModbusCoil(
            "RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1,
        )
        x = self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2 = LeituraModbusCoil(
            "RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2,
        )
        x = self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_TripTempGaxeteiro = LeituraModbusCoil(
            "RetornosDigitais_MXR_TripTempGaxeteiro",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_TripTempGaxeteiro,
        )
        x = self.leitura_RetornosDigitais_MXR_TripTempGaxeteiro
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_TripTempMcGuiaRadial = LeituraModbusCoil(
            "RetornosDigitais_MXR_TripTempMcGuiaRadial",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_TripTempMcGuiaRadial,
        )
        x = self.leitura_RetornosDigitais_MXR_TripTempMcGuiaRadial
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_TripTempMcGuiaEscora = LeituraModbusCoil(
            "RetornosDigitais_MXR_TripTempMcGuiaEscora",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_TripTempMcGuiaEscora,
        )
        x = self.leitura_RetornosDigitais_MXR_TripTempMcGuiaEscora
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_TripTempMcGuiaContraEscora = (
            LeituraModbusCoil(
                "RetornosDigitais_MXR_TripTempMcGuiaContraEscora",
                self.clp,
                REG_UG3_RetornosDigitais_MXR_TripTempMcGuiaContraEscora,
            )
        )
        x = self.leitura_RetornosDigitais_MXR_TripTempMcGuiaContraEscora
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_TripTempUHRV = LeituraModbusCoil(
            "RetornosDigitais_MXR_TripTempUHRV",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_TripTempUHRV,
        )
        x = self.leitura_RetornosDigitais_MXR_TripTempUHRV
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_TripTempUHLM = LeituraModbusCoil(
            "RetornosDigitais_MXR_TripTempUHLM",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_TripTempUHLM,
        )
        x = self.leitura_RetornosDigitais_MXR_TripTempUHLM
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_TripVibr1 = LeituraModbusCoil(
            "RetornosDigitais_MXR_TripVibr1",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_TripVibr1,
        )
        x = self.leitura_RetornosDigitais_MXR_TripVibr1
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_TripVibr2 = LeituraModbusCoil(
            "RetornosDigitais_MXR_TripVibr2",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_TripVibr2,
        )
        x = self.leitura_RetornosDigitais_MXR_TripVibr2
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_FalhaIbntDisjGer = LeituraModbusCoil(
            "RetornosDigitais_MXR_FalhaIbntDisjGer",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_FalhaIbntDisjGer,
        )
        x = self.leitura_RetornosDigitais_MXR_FalhaIbntDisjGer
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_700G_Trip = LeituraModbusCoil(
            "RetornosDigitais_MXR_700G_Trip",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_700G_Trip,
        )
        x = self.leitura_RetornosDigitais_MXR_700G_Trip
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_CLP_Falha = LeituraModbusCoil(
            "RetornosDigitais_MXR_CLP_Falha",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_CLP_Falha,
        )
        x = self.leitura_RetornosDigitais_MXR_CLP_Falha
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_RetornosDigitais_MXR_Q_Negativa = LeituraModbusCoil(
            "RetornosDigitais_MXR_Q_Negativa",
            self.clp,
            REG_UG3_RetornosDigitais_MXR_Q_Negativa,
        )
        x = self.leitura_RetornosDigitais_MXR_Q_Negativa
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )
        # Lista

        # R
        self.leitura_temperatura_fase_R = LeituraModbus(
            "Gerador {} - temperatura fase R".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_01,
            op=4,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_R
        self.condicionador_temperatura_fase_r_ug = CondicionadorExponencial(
            x.descr, DEVE_INDISPONIBILIZAR, x, base, limite
        )
        self.condicionadores.append(self.condicionador_temperatura_fase_r_ug)

        # S
        self.leitura_temperatura_fase_S = LeituraModbus(
            "Gerador {} - temperatura fase s".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_02,
            op=4,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_S
        self.condicionador_temperatura_fase_s_ug = CondicionadorExponencial(
            x.descr, DEVE_INDISPONIBILIZAR, x, base, limite
        )
        self.condicionadores.append(self.condicionador_temperatura_fase_s_ug)

        # T
        self.leitura_temperatura_fase_T = LeituraModbus(
            "Gerador {} - temperatura fase T".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_03,
            op=4,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_T
        self.condicionador_temperatura_fase_t_ug = CondicionadorExponencial(
            x.descr, DEVE_INDISPONIBILIZAR, x, base, limite
        )
        self.condicionadores.append(self.condicionador_temperatura_fase_t_ug)

        # Nucleo estator
        self.leitura_temperatura_nucleo = LeituraModbus(
            "Gerador {} - temperatura núcelo do estator".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_04,
            op=4,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_nucleo
        self.condicionador_temperatura_nucleo_estator_ug = CondicionadorExponencial(
            x.descr, DEVE_INDISPONIBILIZAR, x, base, limite
        )
        self.condicionadores.append(self.condicionador_temperatura_nucleo_estator_ug)

        # MRD 1
        self.leitura_temperatura_mrd1 = LeituraModbus(
            "Gerador {} - temperatura mancal radial dianteiro".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_05,
            op=4,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mrd1
        self.condicionador_temperatura_mancal_rad_dia_1_ug = CondicionadorExponencial(
            x.descr, DEVE_INDISPONIBILIZAR, x, base, limite
        )
        self.condicionadores.append(self.condicionador_temperatura_mancal_rad_dia_1_ug)

        # MRT 1
        self.leitura_temperatura_mrt1 = LeituraModbus(
            "Gerador {} - temperatura mancal radial traseiro".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_06,
            op=4,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mrt1
        self.condicionador_temperatura_mancal_rad_tra_1_ug = CondicionadorExponencial(
            x.descr, DEVE_INDISPONIBILIZAR, x, base, limite
        )
        self.condicionadores.append(self.condicionador_temperatura_mancal_rad_tra_1_ug)

        # MRD 2
        self.leitura_temperatura_mrd2 = LeituraModbus(
            "Gerador {} - temperatura mancal radial dianteiro 2".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_07,
            op=4,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mrd2
        self.condicionador_temperatura_mancal_rad_dia_2_ug = CondicionadorExponencial(
            x.descr, DEVE_INDISPONIBILIZAR, x, base, limite
        )
        self.condicionadores.append(self.condicionador_temperatura_mancal_rad_dia_2_ug)

        # MRT 2
        self.leitura_temperatura_mrt2 = LeituraModbus(
            "Gerador {} - temperatura mancal radial traseiro 2".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_08,
            op=4,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mrt2
        self.condicionador_temperatura_mancal_rad_tra_2_ug = CondicionadorExponencial(
            x.descr, DEVE_INDISPONIBILIZAR, x, base, limite
        )
        self.condicionadores.append(self.condicionador_temperatura_mancal_rad_tra_2_ug)

        # Saída de ar
        self.leitura_temperatura_saida_de_ar = LeituraModbus(
            "Gerador {} - saída de ar".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_10,
            op=4,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_saida_de_ar
        self.condicionador_temperatura_saida_de_ar_ug = CondicionadorExponencial(
            x.descr, DEVE_INDISPONIBILIZAR, x, base, limite
        )
        self.condicionadores.append(self.condicionador_temperatura_saida_de_ar_ug)

        """
        # Perda na grade
        self.leitura_NivelAntesGrade = LeituraModbus(
            "TDA {} - Nivel Antes Grade".format(self.id),
            self.clp_tda,
            REG_TDA_NivelMaisCasasAntes,
            escala=0.0001,
            fundo_de_escala=400,
            op=4,
        )
        self.leitura_NivelDepoisGrade = LeituraModbus(
            "TDA {} - Nivel Depois Grade".format(self.id),
            self.clp_tda,
            REG_TDA_NivelMaisCasasDepois,
            escala=0.0001,
            fundo_de_escala=400,
            op=4,
        )
        base, limite = 100, 200
        self.leitura_perda_na_grade = LeituraDelta(
            "Perda na grade",
            self.leitura_NivelAntesGrade,
            self.leitura_NivelDepoisGrade,
        )
        x = self.leitura_perda_na_grade
        self.condicionadorleitura_perda_na_grade = CondicionadorExponencial(
            x.descr, DEVE_INDISPONIBILIZAR, x, base, limite
        )
        self.condicionadores.append(self.condicionadorleitura_perda_na_grade)
        """
        
        # Mancal Guia Radial
        self.leitura_temperatura_guia_radial = LeituraModbus(
            "Gerador {} - Mancal Guia Radial".format(self.id),
            self.clp,
            REG_UG2_EntradasAnalogicas_MRR_TempMcGuiaRadial,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_radial
        self.condicionador_temperatura_mancal_guia_radial_ug = CondicionadorExponencial(
            x.descr, DEVE_INDISPONIBILIZAR, x, base, limite
        )
        self.condicionadores.append(self.condicionador_temperatura_mancal_guia_radial_ug)

        # Mancal Guia escora
        self.leitura_temperatura_guia_escora = LeituraModbus(
            "Gerador {} - Mancal Guia escora".format(self.id),
            self.clp,
            REG_UG2_EntradasAnalogicas_MRR_TempMcGuiaEscora,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_escora
        self.condicionador_temperatura_mancal_guia_escora_ug = CondicionadorExponencial(
            x.descr, DEVE_INDISPONIBILIZAR, x, base, limite
        )
        self.condicionadores.append(self.condicionador_temperatura_mancal_guia_escora_ug)

        # Mancal Guia contra_escora
        self.leitura_temperatura_guia_contra_escora = LeituraModbus(
            "Gerador {} - Mancal Guia contra_escora".format(self.id),
            self.clp,
            REG_UG2_EntradasAnalogicas_MRR_TempMcGuiaContraEscora,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_contra_escora
        self.condicionador_temperatura_mancal_guia_contra_ug = (
            CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        )
        self.condicionadores.append(
            self.condicionador_temperatura_mancal_guia_contra_ug
        )

        # Óleo do Transformador Elevador
        self.leitura_temperatura_oleo_trafo = LeituraModbus(
            "Gerador {} - Óleo do Transformador Elevador".format(self.id),
            self.clp_sa,
            REG_SA_EntradasAnalogicas_MRR_SA_TE_TempOleo,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_oleo_trafo
        self.condicionador_leitura_temperatura_oleo_trafo = CondicionadorExponencial(
            x.descr, DEVE_INDISPONIBILIZAR, x, base, limite
        )
        self.condicionadores.append(self.condicionador_leitura_temperatura_oleo_trafo)

        # CX Espiral
        self.leitura_caixa_espiral = LeituraModbus(
            "Gerador {} - Caixa espiral".format(self.id),
            self.clp,
            REG_UG2_EntradasAnalogicas_MRR_PressK1CaixaExpiral,
            escala=0.1,
            op = 4
        )
        base, limite = 16.5, 15.5
        x = self.leitura_caixa_espiral
        self.condicionador_caixa_espiral_ug = CondicionadorExponencialReverso(
            x.descr, DEVE_INDISPONIBILIZAR, x, base, limite
        )
        self.condicionadores_atenuadores.append(
            self.condicionador_caixa_espiral_ug
        )

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
                REG_UG3_ComandosDigitais_MXW_EmergenciaViaSuper, 1
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
            self.logger.debug(
                "[UG{}] Removendo sinal (via rede) de TRIP.".format(self.id)
            )
            response = self.clp.write_single_coil(
                REG_UG3_ComandosDigitais_MXW_ResetGeral, 1
            )
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
            self.logger.debug(
                "[UG{}] Acionando sinal (elétrico) de TRIP.".format(self.id)
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_BLOCK_UG{}".format(self.id)],
                [1],
            )
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
            self.logger.debug(
                "[UG{}] Removendo sinal (elétrico) de TRIP.".format(self.id)
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_BLOCK_UG{}".format(self.id)],
                [0],
            )
            DataBank.set_words(
                self.cfg["REG_PAINEL_LIDO"],
                [0],
            )
        except Exception as e:
            self.logger.warning(
                "Exception! Traceback: {}".format(traceback.format_exc())
            )
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
            if not self.clp.read_coils(REG_UG3_COND_PART,1)[0]:
                self.logger.debug(
                    "[UG{}] Sem cond. de partida. Vai partir quando tiver.".format(self.id)
                )
                return True

            if not self.etapa_atual == UNIDADE_SINCRONIZADA:
                self.logger.info(
                    "[UG{}] Enviando comando (via rede) de partida.".format(self.id)
                )
            else:
                self.logger.debug(
                    "[UG{}] Enviando comando (via rede) de partida.".format(self.id)
                )
            response = self.clp.write_single_coil(
                REG_UG3_ComandosDigitais_MXW_ResetGeral, 1
            )
            response = self.clp.write_single_coil(
                REG_UG3_ComandosDigitais_MXW_ResetRele700G, 1
            )
            response = self.clp.write_single_coil(
                REG_UG3_ComandosDigitais_MXW_ResetReleBloq86H, 1
            )
            response = self.clp.write_single_coil(
                REG_UG3_ComandosDigitais_MXW_ResetReleBloq86M, 1
            )
            response = self.clp.write_single_coil(
                REG_UG3_ComandosDigitais_MXW_ResetReleRT, 1
            )
            response = self.clp.write_single_coil(
                REG_UG3_ComandosDigitais_MXW_ResetRV, 1
            )
            response = self.clp.write_single_coil(
                REG_UG3_ComandosDigitais_MXW_IniciaPartida, 1
            )
            self.enviar_setpoint(self.setpoint)
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
                self.logger.info(
                    "[UG{}] Enviando comando (via rede) de parada.".format(self.id)
                )
            else:
                self.logger.debug(
                    "[UG{}] Enviando comando (via rede) de parada.".format(self.id)
                )
            self.enviar_setpoint(0)
            response = False
            response = self.clp.write_single_coil(
                REG_UG3_ComandosDigitais_MXW_AbortaPartida, 1
            )
            response = self.clp.write_single_coil(
                REG_UG3_ComandosDigitais_MXW_AbortaSincronismo, 1
            )
            response = self.clp.write_single_coil(
                REG_UG3_ComandosDigitais_MXW_IniciaParada, 1
            )

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
            self.logger.info(
                "[UG{}] Enviando comando de reconhece e reset alarmes. (Vai tomar aprox 10s)".format(
                    self.id
                )
            )

            for _ in range(3):
                DataBank.set_words(self.cfg["REG_PAINEL_LIDO"], [0])
                self.remover_trip_eletrico()
                DataBank.set_words(self.cfg["REG_PAINEL_LIDO"], [0])
                sleep(1)
                self.remover_trip_logico()
                response = self.clp.write_single_coil(
                    REG_UG3_ComandosDigitais_MXW_ResetGeral, 1
                )
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
            self.logger.debug(
                "[UG{}] Enviando setpoint {} kW.".format(self.id, int(self.setpoint))
            )
            response = False
            if self.setpoint > 1:
                response = self.clp.write_single_coil(
                    REG_UG3_ComandosDigitais_MXW_ResetGeral, 1
                )
                response = self.clp.write_single_coil(
                    REG_UG3_ComandosDigitais_MXW_RV_RefRemHabilita, 1
                )
                response = self.clp.write_single_register(
                    REG_UG3_SaidasAnalogicas_MWW_SPPotAtiva, self.setpoint
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
            voip.enviar_voz_emergencia()
        elif self.condicionador_caixa_espiral_ug.valor < 0.05:
            self.avisou_emerg_voip = False
