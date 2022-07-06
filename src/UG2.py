import json
import os
from unittest.mock import MagicMock
from src.Condicionadores import *
from src.Leituras import *
from src.LeiturasUSN import *
from src.UnidadeDeGeracao import *
from pyModbusTCP.server import DataBank, ModbusServer


class UnidadeDeGeracao2(UnidadeDeGeracao):
    def __init__(
        self,
        id,
        cfg=None,
        leituras_usina=None
    ):
        super().__init__(id)

        if not cfg or not leituras_usina:
            raise ValueError
        else:
            self.cfg = cfg
            self.leituras_usina = leituras_usina

        self.setpoint_minimo = self.cfg["pot_minima"]
        self.setpoint_maximo = self.cfg["pot_maxima_ug{}".format(self.id)]

        self.clp_ip = self.cfg["UG2_slave_ip"]
        self.clp_port = self.cfg["UG2_slave_porta"]
        self.clp = ModbusClient(
            host=self.clp_ip,
            port=self.clp_port,
            timeout=5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )

        self.__last_EtapaAtual = 0
        self.enviar_trip_eletrico = False

        self.leitura_potencia = LeituraModbus(
            "ug{}_Gerador_PotenciaAtivaMedia".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_PM_710_Potencia_Ativa,
        )

        self.leitura_horimetro = LeituraModbus(
            "ug{}_HorimetroEletrico_Low".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Horimetro_Gerador,
        )

        C1 = LeituraModbusCoil(descr="MXR_PartindoEmAuto",modbus_client=self.clp, registrador=REG_UG2_EntradasDigitais_MXI_DisjGeradorFechado)
        C2 = LeituraModbusCoil(descr="MXR_PartindoEmAuto",modbus_client=self.clp, registrador=REG_UG2_RetornosDigitais_MXR_ParandoEmAuto)
        C3 = LeituraModbusCoil(descr="MXR_PartindoEmAuto",modbus_client=self.clp, registrador=REG_UG2_EntradasDigitais_MXI_RV_MaquinaParada)
        C4 = LeituraModbusCoil(descr="MXR_PartindoEmAuto",modbus_client=self.clp, registrador=REG_UG2_RetornosDigitais_MXR_PartindoEmAuto)
        self.leitura_Operacao_EtapaAtual = LeituraComposta(
                                    "ug{}_Operacao_EtapaAtual".format(self.id),
                                    leitura1=C1,
                                    leitura2=C2,
                                    leitura3=C3,
                                    leitura4=C4)

        self.leitura_EntradasDigitais_MXI_RV_Trip = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_RV_Trip".format(self.id), self.clp, REG_UG2_EntradasDigitais_MXI_RV_Trip)
        x = self.leitura_EntradasDigitais_MXI_RV_Trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_AVR_Trip = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_AVR_Trip".format(self.id), self.clp, REG_UG2_EntradasDigitais_MXI_AVR_Trip)
        x = self.leitura_EntradasDigitais_MXI_AVR_Trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_AVR_FalhaInterna = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_AVR_FalhaInterna".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_AVR_FalhaInterna)
        x = self.leitura_EntradasDigitais_MXI_AVR_FalhaInterna
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_AVR_Ligado = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_AVR_Ligado".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_AVR_Ligado)
        x = self.leitura_EntradasDigitais_MXI_AVR_Ligado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_PotenciaNula = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_PotenciaNula".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_PotenciaNula)
        x = self.leitura_EntradasDigitais_MXI_PotenciaNula
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_Falta125Vcc = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_Falta125Vcc".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_Falta125Vcc)
        x = self.leitura_EntradasDigitais_MXI_Falta125Vcc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_DisjGeradorInserido = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_DisjGeradorInserido".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_DisjGeradorInserido)
        x = self.leitura_EntradasDigitais_MXI_DisjGeradorInserido
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_DisjGeradorAberto = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_DisjGeradorAberto".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_DisjGeradorAberto)
        x = self.leitura_EntradasDigitais_MXI_DisjGeradorAberto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_DisjGeradorFechado = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_DisjGeradorFechado".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_DisjGeradorFechado)
        x = self.leitura_EntradasDigitais_MXI_DisjGeradorFechado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_EmergPainelAtuada = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_EmergPainelAtuada".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_EmergPainelAtuada)
        x = self.leitura_EntradasDigitais_MXI_EmergPainelAtuada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_Falta125VccQPCUG2 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_Falta125VccQPCUG2".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_Falta125Vcc)
        x = self.leitura_EntradasDigitais_MXI_Falta125VccQPCUG2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_Falta125VccAlimVal = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_Falta125VccAlimVal".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_Falta125VccAlimVal)
        x = self.leitura_EntradasDigitais_MXI_Falta125VccAlimVal
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FalhaDisjTpsProt = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FalhaDisjTpsProt".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FalhaDisjTpsProt)
        x = self.leitura_EntradasDigitais_MXI_FalhaDisjTpsProt
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_ReleBloqA86HAtuado = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_ReleBloqA86HAtuado".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_ReleBloqA86HAtuado)
        x = self.leitura_EntradasDigitais_MXI_ReleBloqA86HAtuado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_ReleBloqA86MAtuado = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_ReleBloqA86MAtuado".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_ReleBloqA86MAtuado)
        x = self.leitura_EntradasDigitais_MXI_ReleBloqA86MAtuado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_SEL700G_Atuado = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_SEL700G_Atuado".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_SEL700G_Atuado)
        x = self.leitura_EntradasDigitais_MXI_SEL700G_Atuado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_SEL700G_FalhaInterna = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_SEL700G_FalhaInterna".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_SEL700G_FalhaInterna)
        x = self.leitura_EntradasDigitais_MXI_SEL700G_FalhaInterna
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_Reserva244 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_Reserva244".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_Reserva244)
        x = self.leitura_EntradasDigitais_MXI_Reserva244
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_Reserva245 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_Reserva245".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_Reserva245)
        x = self.leitura_EntradasDigitais_MXI_Reserva245
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_NivelMAltoPocoDren = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_NivelMAltoPocoDren".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_NivelMAltoPocoDren)
        x = self.leitura_EntradasDigitais_MXI_NivelMAltoPocoDren
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_DijAlimAVRLig = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_DijAlimAVRLig".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_DijAlimAVRLig)
        x = self.leitura_EntradasDigitais_MXI_DijAlimAVRLig
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FreioPastilhaGasta = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FreioPastilhaGasta".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FreioPastilhaGasta)
        x = self.leitura_EntradasDigitais_MXI_FreioPastilhaGasta
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FreioPressNormal = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FreioPressNormal".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FreioPressNormal)
        x = self.leitura_EntradasDigitais_MXI_FreioPressNormal
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FreioDesaplicado = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FreioDesaplicado".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FreioDesaplicado)
        x = self.leitura_EntradasDigitais_MXI_FreioDesaplicado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FreioAplicado = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FreioAplicado".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FreioAplicado)
        x = self.leitura_EntradasDigitais_MXI_FreioAplicado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_Reserva254 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_Reserva254".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_Reserva254)
        x = self.leitura_EntradasDigitais_MXI_Reserva254
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FreioCmdRemoto = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FreioCmdRemoto".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FreioCmdRemoto)
        x = self.leitura_EntradasDigitais_MXI_FreioCmdRemoto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FreioFiltroSaturado = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FreioFiltroSaturado".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FreioFiltroSaturado)
        x = self.leitura_EntradasDigitais_MXI_FreioFiltroSaturado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FreioSemEnergia = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FreioSemEnergia".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FreioSemEnergia)
        x = self.leitura_EntradasDigitais_MXI_FreioSemEnergia
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHRV_PressCriticaPos321 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHRV_PressCriticaPos321".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHRV_PressCriticaPos321)
        x = self.leitura_EntradasDigitais_MXI_UHRV_PressCriticaPos321
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHRV_PressMinimaPos322 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHRV_PressMinimaPos322".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHRV_PressMinimaPos322)
        x = self.leitura_EntradasDigitais_MXI_UHRV_PressMinimaPos322
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHRV_PressNominalPos323 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHRV_PressNominalPos323".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHRV_PressNominalPos323)
        x = self.leitura_EntradasDigitais_MXI_UHRV_PressNominalPos323
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHRV_Reserva263 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHRV_Reserva263".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHRV_Reserva263)
        x = self.leitura_EntradasDigitais_MXI_UHRV_Reserva263
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHRV_Reserva264 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHRV_Reserva264".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHRV_Reserva264)
        x = self.leitura_EntradasDigitais_MXI_UHRV_Reserva264
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FiltroPresSujo75Troc = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FiltroPresSujo75Troc".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FiltroPresSujo75Troc)
        x = self.leitura_EntradasDigitais_MXI_FiltroPresSujo75Troc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FiltroPresSujo100Sujo = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FiltroPresSujo100Sujo".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FiltroPresSujo100Sujo)
        x = self.leitura_EntradasDigitais_MXI_FiltroPresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FiltroRetSujo75Troc = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FiltroRetSujo75Troc".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FiltroRetSujo75Troc)
        x = self.leitura_EntradasDigitais_MXI_FiltroRetSujo75Troc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FiltroRetSujo100Sujo = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FiltroRetSujo100Sujo".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FiltroRetSujo100Sujo)
        x = self.leitura_EntradasDigitais_MXI_FiltroRetSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35)
        x = self.leitura_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHRV_NivOleominimoPos36 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHRV_NivOleominimoPos36".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHRV_NivOleominimoPos36)
        x = self.leitura_EntradasDigitais_MXI_UHRV_NivOleominimoPos36
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHRV_PressaoEqual = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHRV_PressaoEqual".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHRV_PressaoEqual)
        x = self.leitura_EntradasDigitais_MXI_UHRV_PressaoEqual
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_ValvBorbTravada = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_ValvBorbTravada".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_ValvBorbTravada)
        x = self.leitura_EntradasDigitais_MXI_ValvBorbTravada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_ValvBorbDestravada = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_ValvBorbDestravada".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_ValvBorbDestravada)
        x = self.leitura_EntradasDigitais_MXI_ValvBorbDestravada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_ValvBorbFechada = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_ValvBorbFechada".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_ValvBorbFechada)
        x = self.leitura_EntradasDigitais_MXI_ValvBorbFechada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_ValvBorbAberta = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_ValvBorbAberta".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_ValvBorbAberta)
        x = self.leitura_EntradasDigitais_MXI_ValvBorbAberta
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_ValvBorbADeriva = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_ValvBorbADeriva".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_ValvBorbADeriva)
        x = self.leitura_EntradasDigitais_MXI_ValvBorbADeriva
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_ValvByPassFechada = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_ValvByPassFechada".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_ValvByPassFechada)
        x = self.leitura_EntradasDigitais_MXI_ValvByPassFechada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_ValvByPassAberta = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_ValvByPassAberta".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_ValvByPassAberta)
        x = self.leitura_EntradasDigitais_MXI_ValvByPassAberta
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_DistribuidorFechado = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_DistribuidorFechado".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_DistribuidorFechado)
        x = self.leitura_EntradasDigitais_MXI_DistribuidorFechado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FluxInjAguaPos14 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FluxInjAguaPos14".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FluxInjAguaPos14)
        x = self.leitura_EntradasDigitais_MXI_FluxInjAguaPos14
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_PresInjAguaPos15 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_PresInjAguaPos15".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_PresInjAguaPos15)
        x = self.leitura_EntradasDigitais_MXI_PresInjAguaPos15
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_SobreVeloMecPos18 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_SobreVeloMecPos18".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_SobreVeloMecPos18)
        x = self.leitura_EntradasDigitais_MXI_SobreVeloMecPos18
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FaltaFluxoOleoMc = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FaltaFluxoOleoMc".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FaltaFluxoOleoMc)
        x = self.leitura_EntradasDigitais_MXI_FaltaFluxoOleoMc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_PalhetasDesal = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_PalhetasDesal".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_PalhetasDesal)
        x = self.leitura_EntradasDigitais_MXI_PalhetasDesal
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLM_FaltaFluxTroc = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLM_FaltaFluxTroc".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLM_FaltaFluxTroc)
        x = self.leitura_EntradasDigitais_MXI_UHLM_FaltaFluxTroc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLM_FaltaPressTroc = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLM_FaltaPressTroc".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLM_FaltaPressTroc)
        x = self.leitura_EntradasDigitais_MXI_UHLM_FaltaPressTroc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLMFilt1PresSujo75Troc = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLMFilt1PresSujo75Troc".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLMFilt1PresSujo75Troc)
        x = self.leitura_EntradasDigitais_MXI_UHLMFilt1PresSujo75Troc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLMFilt1PresSujo100Sujo = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLMFilt1PresSujo100Sujo".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLMFilt1PresSujo100Sujo)
        x = self.leitura_EntradasDigitais_MXI_UHLMFilt1PresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLMFilt2PresSujo75Troc = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLMFilt2PresSujo75Troc".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLMFilt2PresSujo75Troc)
        x = self.leitura_EntradasDigitais_MXI_UHLMFilt2PresSujo75Troc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLMFilt2PresSujo100Sujo = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLMFilt2PresSujo100Sujo".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLMFilt2PresSujo100Sujo)
        x = self.leitura_EntradasDigitais_MXI_UHLMFilt2PresSujo100Sujo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLM_NivelCritOleo = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLM_NivelCritOleo".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLM_NivelCritOleo)
        x = self.leitura_EntradasDigitais_MXI_UHLM_NivelCritOleo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLM_NivelminOleo = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLM_NivelminOleo".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLM_NivelminOleo)
        x = self.leitura_EntradasDigitais_MXI_UHLM_NivelminOleo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj75 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FiltroPressaoBbaMecSj75".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FiltroPressaoBbaMecSj75)
        x = self.leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj75
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FiltroPressaoBbaMecSj100".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100)
        x = self.leitura_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_FaltaFluxoBbaMec = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_FaltaFluxoBbaMec".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_FaltaFluxoBbaMec)
        x = self.leitura_EntradasDigitais_MXI_FaltaFluxoBbaMec
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLM_FluxoMcDianteiro".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro)
        x = self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcTras = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLM_FluxoMcTras".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLM_FluxoMcTras)
        x = self.leitura_EntradasDigitais_MXI_UHLM_FluxoMcTras
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLM_PressPos37 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLM_PressPos37".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLM_PressPos37)
        x = self.leitura_EntradasDigitais_MXI_UHLM_PressPos37
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_Reserva307 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_Reserva307".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_Reserva307)
        x = self.leitura_EntradasDigitais_MXI_Reserva307
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLM_Bomba1Ligada = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLM_Bomba1Ligada".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLM_Bomba1Ligada)
        x = self.leitura_EntradasDigitais_MXI_UHLM_Bomba1Ligada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLM_Bomba2Ligada = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLM_Bomba2Ligada".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLM_Bomba2Ligada)
        x = self.leitura_EntradasDigitais_MXI_UHLM_Bomba2Ligada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_PartResLigada = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_PartResLigada".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_PartResLigada)
        x = self.leitura_EntradasDigitais_MXI_PartResLigada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHRV_Bomba1Ligada = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHRV_Bomba1Ligada".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHRV_Bomba1Ligada)
        x = self.leitura_EntradasDigitais_MXI_UHRV_Bomba1Ligada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHRV_Bomba2Ligada = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHRV_Bomba2Ligada".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHRV_Bomba2Ligada)
        x = self.leitura_EntradasDigitais_MXI_UHRV_Bomba2Ligada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_QCAUG_Falha380VcaPainel".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel)
        x = self.leitura_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_QCAUG_Disj52A1Lig = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_QCAUG_Disj52A1Lig".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_QCAUG_Disj52A1Lig)
        x = self.leitura_EntradasDigitais_MXI_QCAUG_Disj52A1Lig
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_QCAUG_TripDisj52A1 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_QCAUG_TripDisj52A1".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_QCAUG_TripDisj52A1)
        x = self.leitura_EntradasDigitais_MXI_QCAUG_TripDisj52A1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLM_TripBomba1 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLM_TripBomba1".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLM_TripBomba1)
        x = self.leitura_EntradasDigitais_MXI_UHLM_TripBomba1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHLM_TripBomba2 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHLM_TripBomba2".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHLM_TripBomba2)
        x = self.leitura_EntradasDigitais_MXI_UHLM_TripBomba2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_TripPartRes = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_TripPartRes".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_TripPartRes)
        x = self.leitura_EntradasDigitais_MXI_TripPartRes
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHRV_TripBomba1 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHRV_TripBomba1".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHRV_TripBomba1)
        x = self.leitura_EntradasDigitais_MXI_UHRV_TripBomba1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_UHRV_TripBomba2 = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_UHRV_TripBomba2".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_UHRV_TripBomba2)
        x = self.leitura_EntradasDigitais_MXI_UHRV_TripBomba2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_TripAlimPainelFreio = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_TripAlimPainelFreio".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_TripAlimPainelFreio)
        x = self.leitura_EntradasDigitais_MXI_TripAlimPainelFreio
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_PainelFreioStatus = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_PainelFreioStatus".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_PainelFreioStatus)
        x = self.leitura_EntradasDigitais_MXI_PainelFreioStatus
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_QCAUG_TripDisjAgrup = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_QCAUG_TripDisjAgrup".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_QCAUG_TripDisjAgrup)
        x = self.leitura_EntradasDigitais_MXI_QCAUG_TripDisjAgrup
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_EntradasDigitais_MXI_QCAUG2_Remoto = LeituraModbusCoil(
            "Gerador {} - EntradasDigitais_MXI_QCAUG2_Remoto".format(self.id), self.clp,
            REG_UG2_EntradasDigitais_MXI_QCAUG2_Remoto)
        x = self.leitura_EntradasDigitais_MXI_QCAUG2_Remoto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_TensaoEstabilizada = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_TensaoEstabilizada".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_TensaoEstabilizada)
        x = self.leitura_RetornosDigitais_MXR_TensaoEstabilizada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_EmergenciaViaSuper = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_EmergenciaViaSuper".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_EmergenciaViaSuper)
        x = self.leitura_RetornosDigitais_MXR_EmergenciaViaSuper
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_SeqManual = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_SeqManual".format(self.id), self.clp, REG_UG2_RetornosDigitais_MXR_SeqManual)
        x = self.leitura_RetornosDigitais_MXR_SeqManual
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_SeqAutomatica = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_SeqAutomatica".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_SeqAutomatica)
        x = self.leitura_RetornosDigitais_MXR_SeqAutomatica
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PartindoEmAuto = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PartindoEmAuto".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PartindoEmAuto)
        x = self.leitura_RetornosDigitais_MXR_PartindoEmAuto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_ParandoEmAuto = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_ParandoEmAuto".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_ParandoEmAuto)
        x = self.leitura_RetornosDigitais_MXR_ParandoEmAuto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_TripEletrico = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_TripEletrico".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_TripEletrico)
        x = self.leitura_RetornosDigitais_MXR_TripEletrico
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_TripMecanico = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_TripMecanico".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_TripMecanico)
        x = self.leitura_RetornosDigitais_MXR_TripMecanico
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_ValvSeg_Energizadas = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_ValvSeg_Energizadas".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_ValvSeg_Energizadas)
        x = self.leitura_RetornosDigitais_MXR_ValvSeg_Energizadas
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_FalhaAcionAbertValvBorb = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_FalhaAcionAbertValvBorb".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_FalhaAcionAbertValvBorb)
        x = self.leitura_RetornosDigitais_MXR_FalhaAcionAbertValvBorb
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_FalhaAcionFechaValvBorb = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_FalhaAcionFechaValvBorb".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_FalhaAcionFechaValvBorb)
        x = self.leitura_RetornosDigitais_MXR_FalhaAcionFechaValvBorb
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_FalhaAcionAbertValvByPass = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_FalhaAcionAbertValvByPass".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_FalhaAcionAbertValvByPass)
        x = self.leitura_RetornosDigitais_MXR_FalhaAcionAbertValvByPass
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_FalhaAcionFechaValvByPass = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_FalhaAcionFechaValvByPass".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_FalhaAcionFechaValvByPass)
        x = self.leitura_RetornosDigitais_MXR_FalhaAcionFechaValvByPass
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_UHRV_CondOK_M1 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_UHRV_CondOK_M1".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_UHRV_CondOK_M1)
        x = self.leitura_RetornosDigitais_MXR_UHRV_CondOK_M1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_UHRV_CondOK_M2 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_UHRV_CondOK_M2".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_UHRV_CondOK_M2)
        x = self.leitura_RetornosDigitais_MXR_UHRV_CondOK_M2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_UHLM_CondOK_M1 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_UHLM_CondOK_M1".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_UHLM_CondOK_M1)
        x = self.leitura_RetornosDigitais_MXR_UHLM_CondOK_M1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_UHLM_CondOK_M2 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_UHLM_CondOK_M2".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_UHLM_CondOK_M2)
        x = self.leitura_RetornosDigitais_MXR_UHLM_CondOK_M2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_Bombas_UHRV_Ligada = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_Bombas_UHRV_Ligada".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_Bombas_UHRV_Ligada)
        x = self.leitura_RetornosDigitais_MXR_Bombas_UHRV_Ligada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1)
        x = self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2)
        x = self.leitura_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1)
        x = self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2)
        x = self.leitura_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_UHRV_PressaoOK = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_UHRV_PressaoOK".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_UHRV_PressaoOK)
        x = self.leitura_RetornosDigitais_MXR_UHRV_PressaoOK
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_UHRV_BbaM1Princ = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_UHRV_BbaM1Princ".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_UHRV_BbaM1Princ)
        x = self.leitura_RetornosDigitais_MXR_UHRV_BbaM1Princ
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_UHLM_BbaM1Princ = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_UHLM_BbaM1Princ".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_UHLM_BbaM1Princ)
        x = self.leitura_RetornosDigitais_MXR_UHLM_BbaM1Princ
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_Filtros_Manual = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_Filtros_Manual".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_Filtros_Manual)
        x = self.leitura_RetornosDigitais_MXR_Filtros_Manual
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_FalhaAcionRT = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_FalhaAcionRT".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_FalhaAcionRT)
        x = self.leitura_RetornosDigitais_MXR_FalhaAcionRT
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_RV_CondOK = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_RV_CondOK".format(self.id), self.clp, REG_UG2_RetornosDigitais_MXR_RV_CondOK)
        x = self.leitura_RetornosDigitais_MXR_RV_CondOK
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_RT_CondOK = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_RT_CondOK".format(self.id), self.clp, REG_UG2_RetornosDigitais_MXR_RT_CondOK)
        x = self.leitura_RetornosDigitais_MXR_RT_CondOK
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_AVR_HabRefExterna = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_AVR_HabRefExterna".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_AVR_HabRefExterna)
        x = self.leitura_RetornosDigitais_MXR_AVR_HabRefExterna
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_AVR_ControleFP = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_AVR_ControleFP".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_AVR_ControleFP)
        x = self.leitura_RetornosDigitais_MXR_AVR_ControleFP
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_UHLM_Ligada = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_UHLM_Ligada".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_UHLM_Ligada)
        x = self.leitura_RetornosDigitais_MXR_UHLM_Ligada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_Filtro1Sel = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_Filtro1Sel".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_Filtro1Sel)
        x = self.leitura_RetornosDigitais_MXR_Filtro1Sel
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_Filtro2Sel = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_Filtro2Sel".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_Filtro2Sel)
        x = self.leitura_RetornosDigitais_MXR_Filtro2Sel
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_QCAUGFalhaAcionPartRes = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_QCAUGFalhaAcionPartRes".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_QCAUGFalhaAcionPartRes)
        x = self.leitura_RetornosDigitais_MXR_QCAUGFalhaAcionPartRes
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_FalhaAcionFreio = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_FalhaAcionFreio".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_FalhaAcionFreio)
        x = self.leitura_RetornosDigitais_MXR_FalhaAcionFreio
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_TripTempGaxeteiro = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_TripTempGaxeteiro".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_TripTempGaxeteiro)
        x = self.leitura_RetornosDigitais_MXR_TripTempGaxeteiro
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_TripTempMcGuiaRadial = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_TripTempMcGuiaRadial".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_TripTempMcGuiaRadial)
        x = self.leitura_RetornosDigitais_MXR_TripTempMcGuiaRadial
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_TripTempMcGuiaEscora = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_TripTempMcGuiaEscora".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_TripTempMcGuiaEscora)
        x = self.leitura_RetornosDigitais_MXR_TripTempMcGuiaEscora
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_TripTempMcGuiaContraEscora = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_TripTempMcGuiaContraEscora".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_TripTempMcGuiaContraEscora)
        x = self.leitura_RetornosDigitais_MXR_TripTempMcGuiaContraEscora
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_TripTempUHRV = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_TripTempUHRV".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_TripTempUHRV)
        x = self.leitura_RetornosDigitais_MXR_TripTempUHRV
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_TripTempUHLM = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_TripTempUHLM".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_TripTempUHLM)
        x = self.leitura_RetornosDigitais_MXR_TripTempUHLM
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_TripVibr1 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_TripVibr1".format(self.id), self.clp, REG_UG2_RetornosDigitais_MXR_TripVibr1)
        x = self.leitura_RetornosDigitais_MXR_TripVibr1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_TripVibr2 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_TripVibr2".format(self.id), self.clp, REG_UG2_RetornosDigitais_MXR_TripVibr2)
        x = self.leitura_RetornosDigitais_MXR_TripVibr2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_FalhaIbntDisjGer = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_FalhaIbntDisjGer".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_FalhaIbntDisjGer)
        x = self.leitura_RetornosDigitais_MXR_FalhaIbntDisjGer
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_AbortaPartida = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_AbortaPartida".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_AbortaPartida)
        x = self.leitura_RetornosDigitais_MXR_AbortaPartida
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_TempoPartidaExc = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_TempoPartidaExc".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_TempoPartidaExc)
        x = self.leitura_RetornosDigitais_MXR_TempoPartidaExc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_ValvInjArRotorLig = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_ValvInjArRotorLig".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_ValvInjArRotorLig)
        x = self.leitura_RetornosDigitais_MXR_ValvInjArRotorLig
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_ValvInjArRotorAuto = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_ValvInjArRotorAuto".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_ValvInjArRotorAuto)
        x = self.leitura_RetornosDigitais_MXR_ValvInjArRotorAuto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PreCondPartidaOK = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PreCondPartidaOK".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PreCondPartidaOK)
        x = self.leitura_RetornosDigitais_MXR_PreCondPartidaOK
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoLigaValvSeg = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoLigaValvSeg".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoLigaValvSeg)
        x = self.leitura_RetornosDigitais_MXR_PassoLigaValvSeg
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoDeslValvSeg = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoDeslValvSeg".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoDeslValvSeg)
        x = self.leitura_RetornosDigitais_MXR_PassoDeslValvSeg
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoAbreValvBorb = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoAbreValvBorb".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoAbreValvBorb)
        x = self.leitura_RetornosDigitais_MXR_PassoAbreValvBorb
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoFechaValvBorb = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoFechaValvBorb".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoFechaValvBorb)
        x = self.leitura_RetornosDigitais_MXR_PassoFechaValvBorb
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoLigaUHRV = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoLigaUHRV".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoLigaUHRV)
        x = self.leitura_RetornosDigitais_MXR_PassoLigaUHRV
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoDesligaUHRV = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoDesligaUHRV".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoDesligaUHRV)
        x = self.leitura_RetornosDigitais_MXR_PassoDesligaUHRV
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoLigaRT = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoLigaRT".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoLigaRT)
        x = self.leitura_RetornosDigitais_MXR_PassoLigaRT
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoDesligaRT = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoDesligaRT".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoDesligaRT)
        x = self.leitura_RetornosDigitais_MXR_PassoDesligaRT
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoLigaRV = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoLigaRV".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoLigaRV)
        x = self.leitura_RetornosDigitais_MXR_PassoLigaRV
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoDesligaRV = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoDesligaRV".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoDesligaRV)
        x = self.leitura_RetornosDigitais_MXR_PassoDesligaRV
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoAbreValvByPass = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoAbreValvByPass".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoAbreValvByPass)
        x = self.leitura_RetornosDigitais_MXR_PassoAbreValvByPass
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoFechaValvByPass = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoFechaValvByPass".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoFechaValvByPass)
        x = self.leitura_RetornosDigitais_MXR_PassoFechaValvByPass
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoLigaUHLM = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoLigaUHLM".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoLigaUHLM)
        x = self.leitura_RetornosDigitais_MXR_PassoLigaUHLM
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoDesligaUHLM = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoDesligaUHLM".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoDesligaUHLM)
        x = self.leitura_RetornosDigitais_MXR_PassoDesligaUHLM
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoAbreDisjuntor = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoAbreDisjuntor".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoAbreDisjuntor)
        x = self.leitura_RetornosDigitais_MXR_PassoAbreDisjuntor
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoLigaFreioPara = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoLigaFreioPara".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoLigaFreioPara)
        x = self.leitura_RetornosDigitais_MXR_PassoLigaFreioPara
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoDeslFreioPart = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoDeslFreioPart".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoDeslFreioPart)
        x = self.leitura_RetornosDigitais_MXR_PassoDeslFreioPart
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoSincroniza = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoSincroniza".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoSincroniza)
        x = self.leitura_RetornosDigitais_MXR_PassoSincroniza
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_700G_EN = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_700G_EN".format(self.id), self.clp, REG_UG2_RetornosDigitais_MXR_700G_EN)
        x = self.leitura_RetornosDigitais_MXR_700G_EN
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_700G_Trip = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_700G_Trip".format(self.id), self.clp, REG_UG2_RetornosDigitais_MXR_700G_Trip)
        x = self.leitura_RetornosDigitais_MXR_700G_Trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_700G_TLED_01 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_700G_TLED_01".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_700G_TLED_01)
        x = self.leitura_RetornosDigitais_MXR_700G_TLED_01
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_700G_TLED_02 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_700G_TLED_02".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_700G_TLED_02)
        x = self.leitura_RetornosDigitais_MXR_700G_TLED_02
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_700G_TLED_03 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_700G_TLED_03".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_700G_TLED_03)
        x = self.leitura_RetornosDigitais_MXR_700G_TLED_03
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_700G_TLED_04 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_700G_TLED_04".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_700G_TLED_04)
        x = self.leitura_RetornosDigitais_MXR_700G_TLED_04
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_700G_TLED_05 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_700G_TLED_05".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_700G_TLED_05)
        x = self.leitura_RetornosDigitais_MXR_700G_TLED_05
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_700G_TLED_06 = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_700G_TLED_06".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_700G_TLED_06)
        x = self.leitura_RetornosDigitais_MXR_700G_TLED_06
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_SincronismoHab = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_SincronismoHab".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_SincronismoHab)
        x = self.leitura_RetornosDigitais_MXR_SincronismoHab
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_CLP_Falha = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_CLP_Falha".format(self.id), self.clp, REG_UG2_RetornosDigitais_MXR_CLP_Falha)
        x = self.leitura_RetornosDigitais_MXR_CLP_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_Remota_Falha = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_Remota_Falha".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_Remota_Falha)
        x = self.leitura_RetornosDigitais_MXR_Remota_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_PassoLigaFreioPart = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_PassoLigaFreioPart".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_PassoLigaFreioPart)
        x = self.leitura_RetornosDigitais_MXR_PassoLigaFreioPart
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_RV_RetiraCarga = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_RV_RetiraCarga".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_RV_RetiraCarga)
        x = self.leitura_RetornosDigitais_MXR_RV_RetiraCarga
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_RV_RefRemHabilitada = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_RV_RefRemHabilitada".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_RV_RefRemHabilitada)
        x = self.leitura_RetornosDigitais_MXR_RV_RefRemHabilitada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_FalhaComunG2TDA = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_FalhaComunG2TDA".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_FalhaComunG2TDA)
        x = self.leitura_RetornosDigitais_MXR_FalhaComunG2TDA
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_Q_Negativa = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_Q_Negativa".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_Q_Negativa)
        x = self.leitura_RetornosDigitais_MXR_Q_Negativa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
    
        self.leitura_RetornosDigitais_MXR_UG2_StsBloqueio = LeituraModbusCoil(
            "Gerador {} - RetornosDigitais_MXR_UG2_StsBloqueio".format(self.id), self.clp,
            REG_UG2_RetornosDigitais_MXR_UG2_StsBloqueio)
        x = self.leitura_RetornosDigitais_MXR_UG2_StsBloqueio
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        # R
        self.leitura_temperatura_fase_R = LeituraModbus(
            "Gerador {} - temperatura fase R".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_01,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_R
        self.condicionador_leitura_temperatura_fase_R = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_leitura_temperatura_fase_R)
        
        # S
        self.leitura_temperatura_fase_S = LeituraModbus(
            "Gerador {} - temperatura fase s".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_02,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_S
        self.condicionador_leitura_temperatura_fase_S = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_leitura_temperatura_fase_S)
        
        # T
        self.leitura_temperatura_fase_T = LeituraModbus(
            "Gerador {} - temperatura fase T".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_03,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_T
        self.condicionador_leitura_temperatura_fase_T = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_leitura_temperatura_fase_T)

        # Nucleo estator
        self.leitura_temperatura_nucleo = LeituraModbus(
            "Gerador {} - temperatura núcelo do estator".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_04,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_nucleo
        self.condicionador_leitura_temperatura_nucleo = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_leitura_temperatura_nucleo)
        
        # MRD 1
        self.leitura_temperatura_mrd1 = LeituraModbus(
            "Gerador {} - temperatura mancal radial dianteiro".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_05,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mrd1
        self.condicionador_leitura_temperatura_mrd1 = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_leitura_temperatura_mrd1)
        
        # MRT 1
        self.leitura_temperatura_mrt1 = LeituraModbus(
            "Gerador {} - temperatura mancal radial traseiro".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_06,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mrt1
        self.condicionador_leitura_temperatura_mrt1 = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_leitura_temperatura_mrt1)
        
        # MRD 2
        self.leitura_temperatura_mrd2 = LeituraModbus(
            "Gerador {} - temperatura mancal radial dianteiro 2".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_07,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mrd2
        self.condicionador_leitura_temperatura_mrd2 = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_leitura_temperatura_mrd2)
        
        # MRT 2
        self.leitura_temperatura_mrt2 = LeituraModbus(
            "Gerador {} - temperatura mancal radial traseiro 2".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_08,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mrt2
        self.condicionador_leitura_temperatura_mrt2 = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_leitura_temperatura_mrt2)
                
        # Saída de ar
        self.leitura_temperatura_saida_de_ar = LeituraModbus(
            "Gerador {} - saída de ar".format(self.id),
            self.clp,
            REG_UG2_RetornosAnalogicos_MWR_Temperatura_10,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_saida_de_ar
        self.condicionador_leitura_temperatura_saida_de_ar = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_leitura_temperatura_saida_de_ar)
                
        # Perda na grade
        self.leitura_NivelAntesGrade = LeituraModbus(
            "TDA {} - Nivel Antes Grade".format(self.id),
            self.clp,
            REG_TDA_EntradasAnalogicas_MRR_NivelMaisCasasAntes,
            escala=0.0001,
            fundo_de_escala=400
        )
        self.leitura_NivelDepoisGrade = LeituraModbus(
            "TDA {} - Nivel Depois Grade".format(self.id),
            self.clp,
            REG_TDA_EntradasAnalogicas_MRR_NivelMaisCasasDepois,
            escala=0.0001,
            fundo_de_escala=400
        )
        base, limite = 100, 200
        self.leitura_perda_na_grade = LeituraDelta("Perda na grade", self.leitura_NivelAntesGrade, self.leitura_NivelDepoisGrade)
        x = self.leitura_perda_na_grade
        self.condicionadorleitura_perda_na_grade = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionadorleitura_perda_na_grade)
        
         # Mancal Guia Radial
        self.leitura_temperatura_guia_radial = LeituraModbus(
            "Gerador {} - Mancal Guia Radial".format(self.id),
            self.clp,
            REG_UG2_EntradasAnalogicas_MRR_TempMcGuiaRadial,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_radial
        self.condicionador_leitura_temperatura_guia_radial = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_leitura_temperatura_guia_radial)
         
        # Mancal Guia escora
        self.leitura_temperatura_guia_escora = LeituraModbus(
            "Gerador {} - Mancal Guia escora".format(self.id),
            self.clp,
            REG_UG2_EntradasAnalogicas_MRR_TempMcGuiaEscora,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_escora
        self.condicionador_leitura_temperatura_guia_escora = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_leitura_temperatura_guia_escora)

        # Mancal Guia contra_escora
        self.leitura_temperatura_guia_contra_escora = LeituraModbus(
            "Gerador {} - Mancal Guia contra_escora".format(self.id),
            self.clp,
            REG_UG2_EntradasAnalogicas_MRR_TempMcGuiaContraEscora,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_guia_contra_escora
        self.condicionador_leitura_temperatura_guia_contra_escora = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_leitura_temperatura_guia_contra_escora)

        # Óleo do Transformador Elevador
        self.leitura_temperatura_oleo_trafo = LeituraModbus(
            "Gerador {} - Óleo do Transformador Elevador".format(self.id),
            self.clp,
            REG_SA_EntradasAnalogicas_MRR_SA_TE_TempOleo,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_oleo_trafo
        self.condicionador_leitura_temperatura_oleo_trafo = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_leitura_temperatura_oleo_trafo)

        # Enrolamento do Transformador Elevador
        self.leitura_temperatura_enrolamento_trafo = LeituraModbus(
            "Gerador {} - Enrolamento do Transformador Elevador".format(self.id),
            self.clp,
            REG_SA_EntradasAnalogicas_MRR_SA_TE_TempEnrolamento,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_enrolamento_trafo
        self.condicionador_leitura_temperatura_enrolamento_trafo = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_leitura_temperatura_enrolamento_trafo)


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
            response = self.clp.write_multiple_coils(
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
            self.logger.debug(
                "[UG{}] Removendo sinal (via rede) de TRIP.".format(self.id)
            )
            response = self.clp.write_single_register(
                REG_UG2_ComandosDigitais_MXW_ResetGeral, 1
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
                self.cfg['REG_PAINEL_LIDO'],
                [0],
            )
        except Exception as e:
            self.logger.warning("Exception! Traceback: {}".format(traceback.format_exc()))
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
            if not self.etapa_atual == UNIDADE_SINCRONIZADA:
                self.logger.info(
                    "[UG{}] Enviando comando (via rede) de partida.".format(self.id)
                )
            else:
                self.logger.debug(
                    "[UG{}] Enviando comando (via rede) de partida.".format(self.id)
                ) 
            response = self.clp.write_single_register(REG_UG2_ComandosDigitais_MXW_IniciaPartida, 1)
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
            response = self.clp.write_single_register(REG_UG2_ComandosDigitais_MXW_AbortaPartida, 1)
            response = self.clp.write_single_register(REG_UG2_ComandosDigitais_MXW_AbortaSincronismo, 1)
            response = self.clp.write_single_register(REG_UG2_ComandosDigitais_MXW_IniciaParada, 1)

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
                "[UG{}] Enviando comando de reconhece e reset alarmes. (Vai tomar aprox 10s)".format(self.id)
            )

            for _ in range(3):
                DataBank.set_words(self.cfg['REG_PAINEL_LIDO'],[0])
                self.remover_trip_eletrico()
                DataBank.set_words(self.cfg['REG_PAINEL_LIDO'],[0])
                sleep(1)
                self.remover_trip_logico()
                response = self.clp.write_single_register(
                    REG_UG2_ComandosDigitais_MXW_ResetGeral, 1
                )
                DataBank.set_words(self.cfg['REG_PAINEL_LIDO'],[0])
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
            if self.setpoint > 1:
                response = self.clp.write_single_register(REG_UG2_SaidasAnalogicas_MWW_SPPotAtiva, self.setpoint)

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

    def modbus_update_state_register(self):
        DataBank.set_words(
                    self.cfg["REG_MOA_OUT_STATE_UG{}".format(self.id)],
                    [self.codigo_state],
                )