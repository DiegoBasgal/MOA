"""
Unidade de geração.

Esse módulo corresponde a implementação das unidades de geração e
da máquina de estado que rege a mesma.
"""
__version__ = "0.1"
__author__ = "Lucas Lavratti"

import pytz
import logging
import traceback

import src.mensageiro.dict as vd

from threading import Thread
from time import sleep, time
from datetime import datetime
from abc import abstractmethod
from pyModbusTCP.client import ModbusClient

from src.codes import *
from src.Leituras import *
from src.Condicionadores import *
from src.abstracao_usina import *
from src.maquinas_estado.ug import *
from src.database_connector import Database
from src.field_connector import FieldConnector

logger = logging.getLogger("__main__")


class UnidadeDeGeracao:
    def __init__(self, id: int = None, cfg: dict = None, clp: "dict[str, ModbusClient]" = None, db: Database = None, con: FieldConnector = None):
        
        if not id or id < 1:
            logger.error(f"[UG{self.id}] O id não pode ser Nulo ou menor que 1")
            raise ValueError
        else:
            self.__id = id

        if not clp:
            logger.error(f"[UG{self.id}] Erro ao carregar conexões com CLPs Modbus")
            raise ValueError
        else:
            self.clp = clp

        self.db = db
        self.con = con
        self.cfg = cfg


        self.__prioridade = 0
        self.__codigo_state = 0
        self.__last_EtapaAtual = 0

        self.__tempo_entre_tentativas = 0
        self.__limite_tentativas_de_normalizacao = 3

        self.__setpoint = 0
        self.__setpoint_minimo = 0
        self.__setpoint_maximo = 0
        self.__tentativas_de_normalizacao = 0

        self.__condicionadores = []
        self.__condicionadores_essenciais = []
        self.__condicionadores_atenuadores = []

        self.__next_state = StateDisponivel(self)

        self.pot_alvo_anterior = -1
        self.ajuste_inicial_cx_esp = -1

        self.release_timer = False
        self.limpeza_grade = False
        self.enviar_trip_eletrico = False
        self.aux_tempo_sincronizada = None
        self.deve_ler_condicionadores = False

        self.setpoint_minimo = self.cfg["pot_minima"]
        self.setpoint_maximo = self.cfg[f"pot_maxima_ug{self.id}"]

        self.ts_auxiliar = self.get_time()

        self.potencia_ativa_kW = LeituraModbus(
            "Potência Usina",
            self.clp["SA"],
            REG_SA_RA_PM_810_Potencia_Ativa,
            1,
            op=4
        )

        # Leituras de operação das UGS
        self.leituras_ug: dict[str, LeituraBase] = {}

        self.leituras_ug[f"leitura_potencia"] = LeituraModbus(
            f"ug{self.id}_Gerador_PotenciaAtivaMedia",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_RA_PM_710_Potencia_Ativa"],
            op=4,
        )
        self.leituras_ug[f"leitura_setpoint"] = LeituraModbus(
            f"UG{self.id}_Setpoint",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_SA_SPPotAtiva"],
            op=4
        )
        self.leituras_ug[f"leitura_horimetro_hora"] = LeituraModbus(
            f"UG{self.id}_Horimetro",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_RA_Horimetro_Gerador"],
            op=4,
        )
        self.leituras_ug[f"leitura_horimetro_frac"] = LeituraModbus(
            f"ug{self.id}_Horimetro_min",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_RA_Horimetro_Gerador_min"],
            op=4,
            escala=1/60
        )
        self.leituras_ug[f"leitura_horimetro"] = LeituraSoma(
            f"ug{self.id} horímetro",
            self.leituras_ug[f"leitura_horimetro_hora"],
            self.leituras_ug[f"leitura_horimetro_frac"]
        )
        C1 = LeituraModbusCoil(
            descr=f"UG{self.id}_Sincronizada",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=UG[f"REG_UG{self.id}_ED_DisjGeradorFechado"],
        )
        C2 = LeituraModbusCoil(
            descr=f"UG{self.id}_Parando",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=UG[f"REG_UG{self.id}_RD_ParandoEmAuto"],
        )
        C3 = LeituraModbusCoil(
            descr=f"UG{self.id}_Parada",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=UG[f"REG_UG{self.id}_ED_RV_MaquinaParada"],
        )
        C4 = LeituraModbusCoil(
            descr=f"UG{self.id}_Sincronizando",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=UG[f"REG_UG{self.id}_RD_PartindoEmAuto"],
        )
        self.leituras_ug[f"leitura_Operacao_EtapaAtual"] = LeituraComposta(
            f"ug{self.id}_Operacao_EtapaAtual",
            leitura1=C1,
            leitura2=C2,
            leitura3=C3,
            leitura4=C4,
        )

        # Leituras para envio de torpedo voip
        self.leitura_voip: dict[str, LeituraBase] = {}

        self.leitura_voip["leitura_ED_FreioPastilhaGasta"] = LeituraModbusCoil(
            "ED_FreioPastilhaGasta",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_FreioPastilhaGasta"]
        )
        self.leitura_voip["leitura_ED_FiltroPresSujo75Troc"] = LeituraModbusCoil(
            "ED_FiltroPresSujo75Troc",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_FiltroPresSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_FiltroRetSujo75Troc"] = LeituraModbusCoil(
            "ED_FiltroRetSujo75Troc",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_FiltroRetSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_UHLMFilt1PresSujo75Troc"] = LeituraModbusCoil(
            "ED_UHLMFilt1PresSujo75Troc",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_UHLM_Filt1PresSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_UHLMFilt2PresSujo75Troc"] = LeituraModbusCoil(
            "ED_UHLMFilt2PresSujo75Troc",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_UHLM_Filt2PresSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_FiltroPressaoBbaMecSj75"] = LeituraModbusCoil(
            "ED_FiltroPressaoBbaMecSj75",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_FiltroPressaoBbaMecSj75"]
        )
        self.leitura_voip["leitura_ED_TripPartRes"] = LeituraModbusCoil(
            "ED_TripPartRes",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_TripPartRes"]
        )
        self.leitura_voip["leitura_ED_FreioCmdRemoto"] = LeituraModbusCoil(
            "ED_FreioCmdRemoto",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_FreioCmdRemoto"]
        )
        self.leitura_voip[f"leitura_ED_QCAUG{self.id}_Remoto"] = LeituraModbusCoil(
            f"ED_QCAUG{self.id}_Remoto",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_QCAUG{self.id}_Remoto"]
        )

        ### CONDICIONADORES ESSENCIAIS
        # R
        self.leitura_temperatura_fase_R = LeituraModbus("Temperatura fase R", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RA_Temperatura_01"], op=4)
        self.condicionador_temperatura_fase_r_ug = CondicionadorExponencial(self.leitura_temperatura_fase_R.descr, DEVE_INDISPONIBILIZAR, self.leitura_temperatura_fase_R, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_r_ug)

        # S
        self.leitura_temperatura_fase_S = LeituraModbus("Temperatura fase S", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RA_Temperatura_02"], op=4)
        self.condicionador_temperatura_fase_s_ug = CondicionadorExponencial(self.leitura_temperatura_fase_S.descr, DEVE_INDISPONIBILIZAR, self.leitura_temperatura_fase_S, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_s_ug)

        # T
        self.leitura_temperatura_fase_T = LeituraModbus("Temperatura fase T", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RA_Temperatura_03"], op=4)
        self.condicionador_temperatura_fase_t_ug = CondicionadorExponencial(self.leitura_temperatura_fase_T.descr, DEVE_INDISPONIBILIZAR, self.leitura_temperatura_fase_T, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_t_ug)

        # Nucleo estator
        self.leitura_temperatura_nucleo = LeituraModbus("Temperatura núcelo do estator", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RA_Temperatura_04"], op=4)
        self.condicionador_temperatura_nucleo_estator_ug = CondicionadorExponencial(self.leitura_temperatura_nucleo.descr, DEVE_INDISPONIBILIZAR, self.leitura_temperatura_nucleo, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_nucleo_estator_ug)

        # MRD 1
        self.leitura_temperatura_mrd1 = LeituraModbus("Temperatura mancal radial dianteiro", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RA_Temperatura_05"], op=4)
        self.condicionador_temperatura_mancal_rad_dia_1_ug = CondicionadorExponencial(self.leitura_temperatura_mrd1.descr, DEVE_INDISPONIBILIZAR, self.leitura_temperatura_mrd1, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_dia_1_ug)

        # MRT 1
        self.leitura_temperatura_mrt1 = LeituraModbus("Temperatura mancal radial traseiro", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RA_Temperatura_06"], op=4)
        self.condicionador_temperatura_mancal_rad_tra_1_ug = CondicionadorExponencial(self.leitura_temperatura_mrt1.descr, DEVE_INDISPONIBILIZAR, self.leitura_temperatura_mrt1, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_tra_1_ug)

        # MRD 2
        self.leitura_temperatura_mrd2 = LeituraModbus("Temperatura mancal radial dianteiro 2", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RA_Temperatura_07"], op=4)
        self.condicionador_temperatura_mancal_rad_dia_2_ug = CondicionadorExponencial(self.leitura_temperatura_mrd2.descr, DEVE_INDISPONIBILIZAR, self.leitura_temperatura_mrd2, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_dia_2_ug)

        # MRT 2
        self.leitura_temperatura_mrt2 = LeituraModbus("Temperatura mancal radial traseiro 2", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RA_Temperatura_08"], op=4)
        self.condicionador_temperatura_mancal_rad_tra_2_ug = CondicionadorExponencial(self.leitura_temperatura_mrt2.descr, DEVE_INDISPONIBILIZAR, self.leitura_temperatura_mrt2, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_rad_tra_2_ug)

        # Saída de ar
        self.leitura_temperatura_saida_de_ar = LeituraModbus("Saída de ar", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RA_Temperatura_10"], op=4)
        self.condicionador_temperatura_saida_de_ar_ug = CondicionadorExponencial(self.leitura_temperatura_saida_de_ar.descr, DEVE_INDISPONIBILIZAR, self.leitura_temperatura_saida_de_ar, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_saida_de_ar_ug)

        # Mancal Guia Radial
        self.leitura_temperatura_guia_radial = LeituraModbus("Mancal Guia Radial", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_EA_TempMcGuiaRadial"])
        self.condicionador_temperatura_mancal_guia_radial_ug = CondicionadorExponencial(self.leitura_temperatura_guia_radial.descr, DEVE_INDISPONIBILIZAR, self.leitura_temperatura_guia_radial, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_radial_ug)

        # Mancal Guia escora
        self.leitura_temperatura_guia_escora = LeituraModbus("Mancal Guia escora", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_EA_TempMcGuiaEscora"])
        self.condicionador_temperatura_mancal_guia_escora_ug = CondicionadorExponencial(self.leitura_temperatura_guia_escora.descr, DEVE_INDISPONIBILIZAR, self.leitura_temperatura_guia_escora, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_escora_ug)

        # Mancal Guia contra_escora
        self.leitura_temperatura_guia_contra_escora = LeituraModbus("Mancal Guia contra_escora", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_EA_TempMcGuiaContraEscora"])
        self.condicionador_temperatura_mancal_guia_contra_ug = (CondicionadorExponencial(self.leitura_temperatura_guia_contra_escora.descr, DEVE_INDISPONIBILIZAR, self.leitura_temperatura_guia_contra_escora, 100, 200))
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_contra_ug)

        # Óleo do Transformador Elevador
        self.leitura_temperatura_oleo_trafo = LeituraModbus("Óleo do Transformador Elevador", self.clp["SA"], REG_SA_EA_SA_TE_TempOleo, escala=0.1, op=4)
        self.condicionador_leitura_temperatura_oleo_trafo = CondicionadorExponencial(self.leitura_temperatura_oleo_trafo.descr, DEVE_INDISPONIBILIZAR, self.leitura_temperatura_oleo_trafo, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_leitura_temperatura_oleo_trafo)

        # CX Espiral
        self.leitura_caixa_espiral = LeituraModbus("Caixa espiral", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_EA_PressK1CaixaExpiral_MaisCasas"], escala=0.01, op=4)
        self.condicionador_caixa_espiral_ug = CondicionadorExponencialReverso(self.leitura_caixa_espiral.descr, DEVE_INDISPONIBILIZAR, self.leitura_caixa_espiral, 16.5, 15.5)
        self.condicionadores_atenuadores.append(self.condicionador_caixa_espiral_ug)

        ## Comandos Digitais
        # GERAL
        self.leitura_CD_EmergenciaViaSuper = LeituraModbusCoil("CD_EmergenciaViaSuper", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_CD_EmergenciaViaSuper"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_CD_EmergenciaViaSuper.descr, DEVE_NORMALIZAR, self.leitura_CD_EmergenciaViaSuper))

        ## Retornos Digitais
        # TRIPS
        self.leitura_RD_TripEletrico = LeituraModbusCoil("RD_TripEletrico", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_TripEletrico"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_RD_TripEletrico.descr, DEVE_NORMALIZAR, self.leitura_RD_TripEletrico))

        self.leitura_RD_700G_Trip = LeituraModbusCoil("RD_700G_Trip", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_700G_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_RD_700G_Trip.descr, DEVE_NORMALIZAR, self.leitura_RD_700G_Trip, self.id))

        self.leitura_RD_TripMecanico = LeituraModbusCoil("RD_TripMecanico", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_TripMecanico"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_RD_TripMecanico.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_TripMecanico))

        ## Entradas Digitais
        # TRIPS
        self.leitura_ED_RV_Trip = LeituraModbusCoil("ED_RV_Trip", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_RV_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_RV_Trip.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_RV_Trip))

        self.leitura_ED_AVR_Trip = LeituraModbusCoil("ED_AVR_Trip", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_AVR_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_AVR_Trip.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_AVR_Trip))

        # RELÉS
        self.leitura_ED_SEL700G_Atuado = LeituraModbusCoil("ED_SEL700G_Atuado", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_SEL700G_Atuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SEL700G_Atuado.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SEL700G_Atuado))

        self.leitura_ED_ReleBloqA86MAtuado = LeituraModbusCoil("ED_ReleBloqA86MAtuado", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_ReleBloqA86MAtuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_ReleBloqA86MAtuado.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_ReleBloqA86MAtuado))

        self.leitura_ED_ReleBloqA86HAtuado = LeituraModbusCoil("ED_ReleBloqA86HAtuado", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_ReleBloqA86HAtuado"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_ReleBloqA86HAtuado.descr, DEVE_NORMALIZAR, self.leitura_ED_ReleBloqA86HAtuado, self.id, [UNIDADE_SINCRONIZADA]))


        ### CONDICIONADORES NORMAIS
        # Entradas Digitais
        # SA -> UG
        self.leitura_ED_SA_FalhaDisjTPsSincrG2 = LeituraModbusCoil(f"ED_SA_FalhaDisjTPsSincrG{self.id}", self.clp["SA"], REG_SA_ED_SA_FalhaDisjTPsSincrG2)
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_FalhaDisjTPsSincrG2.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_FalhaDisjTPsSincrG2))

        self.leitura_ED_SA_DisjDJ1_AlPressBaixa = LeituraModbusCoil("ED_SA_DisjDJ1_AlPressBaixa", self.clp["SA"], REG_SA_ED_SA_DisjDJ1_AlPressBaixa)
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_DisjDJ1_AlPressBaixa.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_DisjDJ1_AlPressBaixa))

        self.leitura_ED_SA_DisjDJ1_BloqPressBaixa = LeituraModbusCoil("ED_SA_DisjDJ1_BloqPressBaixa", self.clp["SA"], REG_SA_ED_SA_DisjDJ1_BloqPressBaixa)
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_DisjDJ1_BloqPressBaixa.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_DisjDJ1_BloqPressBaixa))

        # TRIPS
        self.leitura_ED_UHRV_TripBomba1 = LeituraModbusCoil("ED_UHRV_TripBomba1", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_UHRV_TripBomba1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_TripBomba1.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_UHRV_TripBomba1))

        self.leitura_ED_UHRV_TripBomba2 = LeituraModbusCoil("ED_UHRV_TripBomba2", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_UHRV_TripBomba2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_TripBomba2.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_UHRV_TripBomba2))

        self.leitura_ED_UHLM_TripBomba1 = LeituraModbusCoil("ED_UHLM_TripBomba1", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_UHLM_TripBomba1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_TripBomba1.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_UHLM_TripBomba1))

        self.leitura_ED_UHLM_TripBomba2 = LeituraModbusCoil("ED_UHLM_TripBomba2", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_UHLM_TripBomba2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_TripBomba2.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_UHLM_TripBomba2))

        self.leitura_ED_QCAUG_TripDisj52A1 = LeituraModbusCoil("ED_QCAUG_TripDisj52A1", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_QCAUG_TripDisj52A1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_QCAUG_TripDisj52A1.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_QCAUG_TripDisj52A1))

        self.leitura_ED_TripAlimPainelFreio = LeituraModbusCoil("ED_TripAlimPainelFreio", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_TripAlimPainelFreio"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_TripAlimPainelFreio.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_TripAlimPainelFreio))

        self.leitura_ED_QCAUG_TripDisjAgrup = LeituraModbusCoil("ED_QCAUG_TripDisjAgrup", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_QCAUG_TripDisjAgrup"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_QCAUG_TripDisjAgrup.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_QCAUG_TripDisjAgrup))

        # FALHAS
        self.leitura_ED_AVR_FalhaInterna = LeituraModbusCoil("ED_AVR_FalhaInterna", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_AVR_FalhaInterna"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_AVR_FalhaInterna.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_AVR_FalhaInterna))

        self.leitura_ED_SEL700G_FalhaInterna = LeituraModbusCoil("ED_SEL700G_FalhaInterna", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_SEL700G_FalhaInterna"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SEL700G_FalhaInterna.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SEL700G_FalhaInterna))

        self.leitura_ED_QCAUG_Falha380VcaPainel = LeituraModbusCoil("ED_QCAUG_Falha380VcaPainel", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_QCAUG_Falha380VcaPainel"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_QCAUG_Falha380VcaPainel.descr, DEVE_NORMALIZAR, self.leitura_ED_QCAUG_Falha380VcaPainel))

        # FALTAS
        self.leitura_ED_Falta125Vcc = LeituraModbusCoil("ED_Falta125Vcc", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_Falta125Vcc.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_Falta125Vcc))

        self.leitura_ED_Falta125VccCom = LeituraModbusCoil("ED_Falta125VccCom", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_Falta125VccCom"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_Falta125VccCom.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_Falta125VccCom))

        self.leitura_ED_FaltaFluxoOleoMc = LeituraModbusCoil("ED_FaltaFluxoOleoMc", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_FaltaFluxoOleoMc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FaltaFluxoOleoMc.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_FaltaFluxoOleoMc))

        self.leitura_ED_Falta125VccAlimVal = LeituraModbusCoil("ED_Falta125VccAlimVal", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_Falta125VccAlimVal"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_Falta125VccAlimVal.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_Falta125VccAlimVal))

        self.leitura_ED_UHLM_FaltaFluxTroc = LeituraModbusCoil("ED_UHLM_FaltaFluxTroc", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_UHLM_FaltaFluxTroc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FaltaFluxTroc.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_UHLM_FaltaFluxTroc))

        self.leitura_ED_UHLM_FaltaPressTroc = LeituraModbusCoil("ED_UHLM_FaltaPressTroc", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_UHLM_FaltaPressTroc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FaltaPressTroc.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_UHLM_FaltaPressTroc))

        # Controle UHRV
        self.leitura_ED_UHRV_NivOleominimoPos36 = LeituraModbusCoil("ED_UHRV_NivOleominimoPos36", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_UHRV_NivOleominimoPos36"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_NivOleominimoPos36.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_UHRV_NivOleominimoPos36))

        self.leitura_ED_UHRV_NivOleoCriticoPos35 = LeituraModbusCoil("ED_UHRV_NivOleoCriticoPos35", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_UHRV_NivOleoCriticoPos35"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHRV_NivOleoCriticoPos35.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_UHRV_NivOleoCriticoPos35))

        # Controle UHLM
        self.leitura_ED_UHLM_FluxoMcTras = LeituraModbusCoil("ED_UHLM_FluxoMcTras", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_UHLM_FluxoMcTras"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FluxoMcTras.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_UHLM_FluxoMcTras))

        self.leitura_ED_UHLM_NivelminOleo = LeituraModbusCoil("ED_UHLM_NivelminOleo", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_UHLM_NivelminOleo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_NivelminOleo.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_UHLM_NivelminOleo))

        self.leitura_ED_UHLM_NivelCritOleo = LeituraModbusCoil("ED_UHLM_NivelCritOleo", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_UHLM_NivelCritOleo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_NivelCritOleo.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_UHLM_NivelCritOleo))

        self.leitura_ED_UHLM_FluxoMcDianteiro = LeituraModbusCoil("ED_UHLM_FluxoMcDianteiro", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_UHLM_FluxoMcDianteiro"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_FluxoMcDianteiro.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_UHLM_FluxoMcDianteiro))

        self.leitura_ED_UHLM_Filt1PresSujo100Sujo = LeituraModbusCoil("ED_UHLM_Filt1PresSujo100Sujo", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_UHLM_Filt1PresSujo100Sujo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_Filt1PresSujo100Sujo.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_UHLM_Filt1PresSujo100Sujo))

        self.leitura_ED_UHLM_Filt2PresSujo100Sujo = LeituraModbusCoil("ED_UHLM_Filt2PresSujo100Sujo", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_UHLM_Filt2PresSujo100Sujo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_UHLM_Filt2PresSujo100Sujo.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_UHLM_Filt2PresSujo100Sujo))

        # Controle Freios
        self.leitura_ED_FreioSemEnergia = LeituraModbusCoil("ED_FreioSemEnergia", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_FreioSemEnergia"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FreioSemEnergia.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_FreioSemEnergia))

        self.leitura_ED_FreioFiltroSaturado = LeituraModbusCoil("ED_FreioFiltroSaturado", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_FreioFiltroSaturado"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FreioFiltroSaturado.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_FreioFiltroSaturado))

        # Controle Filtros
        self.leitura_ED_FiltroRetSujo100Sujo = LeituraModbusCoil("ED_FiltroRetSujo100Sujo", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_FiltroRetSujo100Sujo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FiltroRetSujo100Sujo.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_FiltroRetSujo100Sujo))

        self.leitura_ED_FiltroPresSujo100Sujo = LeituraModbusCoil("ED_FiltroPresSujo100Sujo", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_FiltroPresSujo100Sujo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FiltroPresSujo100Sujo.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_FiltroPresSujo100Sujo))

        self.leitura_ED_FiltroPressaoBbaMecSj100 = LeituraModbusCoil("ED_FiltroPressaoBbaMecSj100", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_FiltroPressaoBbaMecSj100"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_FiltroPressaoBbaMecSj100.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_FiltroPressaoBbaMecSj100))

        # Outros
        self.leitura_ED_PalhetasDesal = LeituraModbusCoil("ED_PalhetasDesal", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_PalhetasDesal"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_PalhetasDesal.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_PalhetasDesal))

        self.leitura_ED_ValvBorbTravada = LeituraModbusCoil("ED_ValvBorbTravada", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_ValvBorbTravada"],)
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_ValvBorbTravada.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_ValvBorbTravada))

        self.leitura_ED_SobreVeloMecPos18 = LeituraModbusCoil("ED_SobreVeloMecPos18", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_SobreVeloMecPos18"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SobreVeloMecPos18.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SobreVeloMecPos18))

        self.leitura_ED_NivelMAltoPocoDren = LeituraModbusCoil("ED_NivelMAltoPocoDren", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_ED_NivelMAltoPocoDren"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_NivelMAltoPocoDren.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_NivelMAltoPocoDren))


        ## Retornos Digitais
        # TRIPS
        self.leitura_RD_TripVibr1 = LeituraModbusCoil("RD_TripVibr1", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_TripVibr1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripVibr1.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_TripVibr1))

        self.leitura_RD_TripVibr2 = LeituraModbusCoil("RD_TripVibr2", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_TripVibr2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripVibr2.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_TripVibr2))

        self.leitura_RD_TripTempUHRV = LeituraModbusCoil("RD_TripTempUHRV", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_TripTempUHRV"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempUHRV.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_TripTempUHRV))

        self.leitura_RD_TripTempUHLM = LeituraModbusCoil("RD_TripTempUHLM", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_TripTempUHLM"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempUHLM.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_TripTempUHLM))

        self.leitura_RD_TripTempGaxeteiro = LeituraModbusCoil("RD_TripTempGaxeteiro", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_TripTempGaxeteiro"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempGaxeteiro.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_TripTempGaxeteiro))

        self.leitura_RD_TripTempMcGuiaRadial = LeituraModbusCoil("RD_TripTempMcGuiaRadial", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_TripTempMcGuiaRadial"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempMcGuiaRadial.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_TripTempMcGuiaRadial))

        self.leitura_RD_TripTempMcGuiaEscora = LeituraModbusCoil("RD_TripTempMcGuiaEscora", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_TripTempMcGuiaEscora"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempMcGuiaEscora.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_TripTempMcGuiaEscora))

        self.leitura_RD_TripTempMcGuiaContraEscora = LeituraModbusCoil("RD_TripTempMcGuiaContraEscora", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_TripTempMcGuiaContraEscora"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_TripTempMcGuiaContraEscora.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_TripTempMcGuiaContraEscora))

        # Retornos Digitais - FALHAS
        self.leitura_RD_CLP_Falha = LeituraModbusCoil("RD_CLP_Falha", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_CLP_Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_CLP_Falha.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_CLP_Falha))

        self.leitura_RD_Q_Negativa = LeituraModbusCoil("RD_Q_Negativa", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_Q_Negativa"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_Q_Negativa.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_Q_Negativa))

        self.leitura_RD_Remota_Falha = LeituraModbusCoil("RD_Remota_Falha", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_Remota_Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_Remota_Falha.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_Remota_Falha))

        self.leitura_RD_FalhaIbntDisjGer = LeituraModbusCoil("RD_FalhaIbntDisjGer", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_FalhaIbntDisjGer"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_FalhaIbntDisjGer.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_FalhaIbntDisjGer))

        self.leitura_RD_UHRV_FalhaAcionBbaM1 = LeituraModbusCoil("RD_UHRV_FalhaAcionBbaM1", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_UHRV_FalhaAcionBbaM1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHRV_FalhaAcionBbaM1.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_UHRV_FalhaAcionBbaM1))

        self.leitura_RD_UHRV_FalhaAcionBbaM2 = LeituraModbusCoil("RD_UHRV_FalhaAcionBbaM2", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_UHRV_FalhaAcionBbaM2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHRV_FalhaAcionBbaM2.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_UHRV_FalhaAcionBbaM2))

        self.leitura_RD_UHLM_FalhaAcionBbaM1 = LeituraModbusCoil("RD_UHLM_FalhaAcionBbaM1", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_UHLM_FalhaAcionBbaM1"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHLM_FalhaAcionBbaM1.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_UHLM_FalhaAcionBbaM1))

        self.leitura_RD_UHLM_FalhaAcionBbaM2 = LeituraModbusCoil("RD_UHLM_FalhaAcionBbaM2", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_UHLM_FalhaAcionBbaM2"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_UHLM_FalhaAcionBbaM2.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_UHLM_FalhaAcionBbaM2))

        self.leitura_RD_FalhaAcionFechaValvBorb = LeituraModbusCoil("RD_FalhaAcionFechaValvBorb", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_FalhaAcionFechaValvBorb"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_FalhaAcionFechaValvBorb.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_FalhaAcionFechaValvBorb))

        self.leitura_RD_FalhaAcionFechaValvBorb = LeituraModbusCoil("RD_FalhaAcionFechaValvBorb", self.clp[f"UG{self.id}"], UG[f"REG_UG{self.id}_RD_FalhaAcionFechaValvBorb"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_FalhaAcionFechaValvBorb.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_FalhaAcionFechaValvBorb))

    @property
    def id(self) -> int:
        return self.__id

    @property
    def manual(self) -> bool:
        return isinstance(self.__next_state, StateManual)

    @property
    def disponivel(self) -> bool:
        return isinstance(self.__next_state, StateDisponivel)

    @property
    def etapa_atual(self) -> int:
        try:
            response = self.leituras_ug[f"leitura_Operacao_EtapaAtual"].valor
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

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível realizar a leitura de Etapa Atual.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return self.__last_EtapaAtual

    @property
    def tempo_entre_tentativas(self) -> int:
        return self.__tempo_entre_tentativas

    @property
    def limite_tentativas_de_normalizacao(self) -> int:
        return self.__limite_tentativas_de_normalizacao

    @property
    def prioridade(self) -> int:
        return self.__prioridade

    @prioridade.setter
    def prioridade(self, var) -> None:
        self.__prioridade = var

    @property
    def codigo_state(self) -> int:
        return self.__codigo_state

    @codigo_state.setter
    def codigo_state(self, var) -> None:
        self.__codigo_state = var

    @property
    def setpoint(self) -> int:
        return self.__setpoint

    @setpoint.setter
    def setpoint(self, var: int):
        if var < self.setpoint_minimo:
            self.__setpoint = 0
        elif var > self.setpoint_maximo:
            self.__setpoint = self.setpoint_maximo
        else:
            self.__setpoint = int(var)
        logger.debug(f"[UG{self.id}] SP<-{var}")

    @property
    def setpoint_minimo(self) -> int:
        return self.__setpoint_minimo

    @setpoint_minimo.setter
    def setpoint_minimo(self, var: int):
        self.__setpoint_minimo = var

    @property
    def setpoint_maximo(self) -> int:
        return self.__setpoint_maximo

    @setpoint_maximo.setter
    def setpoint_maximo(self, var: int):
        self.__setpoint_maximo = var

    @property
    def tentativas_de_normalizacao(self) -> int:
        return self.__tentativas_de_normalizacao

    @tentativas_de_normalizacao.setter
    def tentativas_de_normalizacao(self, var: int):
        self.__tentativas_de_normalizacao = var

    @property
    def condicionadores(self) -> "list[CondicionadorBase]":
        return self.__condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[CondicionadorBase]") -> None:
        self.__condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[CondicionadorBase]":
        return self.__condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[CondicionadorBase]") -> None:
        self.__condicionadores_essenciais = var

    @property
    def condicionadores_atenuadores(self) -> "list[CondicionadorBase]":
        return self.__condicionadores_atenuadores

    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: "list[CondicionadorBase]") -> None:
        self.__condicionadores_atenuadores = var

    @property
    def lista_ugs(self) -> "list[UnidadeDeGeracao]":
        return self._lista_ugs

    @lista_ugs.setter
    def lista_ugs(self, var: "list[UnidadeDeGeracao]") -> None:
        self._lista_ugs = var


    @staticmethod
    def get_time() -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def modbus_update_state_register(self) -> None:
        self.clp["MOA"].write_single_register(self.cfg[f"REG_MOA_OUT_STATE_UG{self.id}"], self.codigo_state)
        self.clp["MOA"].write_single_register(self.cfg[f"REG_MOA_OUT_ETAPA_UG{self.id}"], self.etapa_atual)

    def forcar_estado_disponivel(self) -> None:
        try:
            self.reconhece_reset_alarmes()
            sleep(1)
            self.__next_state = StateDisponivel(self)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível forçar o estado \"Disponível\".")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def forcar_estado_indisponivel(self) -> None:
        try:
            self.__next_state = StateIndisponivel(self)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível forçar o estado \"Indisponível\".")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def forcar_estado_manual(self) -> None:
        try:
            self.__next_state = StateManual(self)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível forçar o estado \"Manual\".")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def forcar_estado_restrito(self) -> None:
        try:
            self.__next_state = StateRestrito(self)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível forçar o estado \"Restrito\".")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def step(self) -> None:
        try:
            logger.debug("")
            logger.debug(f"[UG{self.id}] Step. (Tentativas de normalização: {self.tentativas_de_normalizacao}/{self.limite_tentativas_de_normalizacao})")
            self.__next_state = self.__next_state.step()
            self.modbus_update_state_register()

        except Exception:
            logger.error(f"[UG{self.id}] Erro na execução da Máquina de estados da UG.")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def partir(self) -> bool:
        try:
            if not self.clp[f"UG{self.id}"].read_discrete_inputs(UG[f"REG_UG{self.id}_COND_PART"], 1)[0]:
                logger.debug(f"[UG{self.id}] Máquina sem condição de partida. Irá partir quando as condições forem reestabelecidas.")
                return True

            elif self.clp["SA"].read_coils(REG_SA_ED_SA_QCAP_Disj52A1Fechado)[0] != 0:
                logger.info(f"[UG{self.id}] O Disjuntor 52A1 está aberto. Para partir a máquina, o mesmo deverá ser fechado.")
                return True

            elif not self.etapa_atual == UNIDADE_SINCRONIZADA:
                logger.info(f"[UG{self.id}] Enviando comando de partida.")
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetGeral"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetRele700G"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetReleBloq86H"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetReleBloq86M"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetReleRT"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetRV"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_IniciaPartida"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_Cala_Sirene"], 1)

            else:
                logger.debug(f"[UG{self.id}] A unidade já está sincronizada.")
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_Cala_Sirene"], 1)
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o comando de partida.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def parar(self) -> bool:
        try:
            if not self.etapa_atual == UNIDADE_PARADA:
                logger.info(f"[UG{self.id}] Enviando comando de parada.")
                response = False
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_AbortaPartida"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_AbortaSincronismo"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_IniciaParada"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_Cala_Sirene"], 1)
                self.enviar_setpoint(self.setpoint)
            else:
                logger.debug(f"[UG{self.id}] A unidade já está parada.")
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_Cala_Sirene"], 1)
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o comando de parada.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def enviar_setpoint(self, setpoint_kw: int) -> bool:
        try:
            response = False
            if self.limpeza_grade:
                self.setpoint_minimo = self.cfg["pot_limpeza_grade"]
            else:
                self.setpoint_minimo = self.cfg["pot_minima"]
            self.setpoint_maximo = self.cfg[f"pot_maxima_ug{self.id}"]

            logger.debug(f"[UG{self.id}] Enviando setpoint {int(self.setpoint)} kW.")

            if self.setpoint > 1:
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetGeral"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_RV_RefRemHabilita"], 1)
                response = self.clp[f"UG{self.id}"].write_single_register(UG[f"REG_UG{self.id}_SA_SPPotAtiva"], self.setpoint)
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o setpoint.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def acionar_trip_eletrico(self) -> bool:
        try:
            self.enviar_trip_eletrico = True
            logger.debug(f"[UG{self.id}] Acionando sinal de TRIP -> Elétrico.")

            self.clp["MOA"].write_single_coil(self.cfg[f"REG_MOA_OUT_BLOCK_UG{self.id}"], [1])
            return True

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível acionar o TRIP -> Elétrico.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def remover_trip_eletrico(self) -> bool:
        try:
            self.enviar_trip_eletrico = False
            logger.debug(f"[UG{self.id}] Removendo sinal de TRIP -> Elétrico.")

            self.clp["MOA"].write_single_coil(self.cfg["REG_PAINEL_LIDO"], [0])
            self.clp["MOA"].write_single_coil(self.cfg[f"REG_MOA_OUT_BLOCK_UG{self.id}"], [0])
            self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_Cala_Sirene"], [1])

            if self.clp["SA"].read_coils(REG_SA_CD_Liga_DJ1)[0] == 0:
                logger.debug(f"[UG{self.id}] Comando recebido -> Fechar Dj52L")
                self.con.fechaDj52L()
            return True

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível remover o TRIP -> Elétrico.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def acionar_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Acionando sinal de TRIP -> Lógico.")
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_EmergenciaViaSuper"], [1])
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível acionar o TRIP -> Lógico.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def remover_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Removendo sinal de TRIP -> Lógico.")
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetGeral"], 1)
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetReleBloq86H"], 1)
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetReleBloq86M"], 1)
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetRele700G"], 1)
            response = self.clp["SA"].write_single_coil(REG_SA_CD_ResetRele59N, 1)
            response = self.clp["SA"].write_single_coil(REG_SA_CD_ResetRele787, 1)
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_ED_ReleBloqA86HAtuado"], 0)
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_ED_ReleBloqA86MAtuado"], 0)
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_RD_700G_Trip"], 0)
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível remover o TRIP -> Lógico.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def reconhece_reset_alarmes(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Enviando comando de reconhece alarmes e reset.")
            self.clp["MOA"].write_single_coil(self.cfg["REG_PAINEL_LIDO"], [0])

            for _ in range(3):
                self.remover_trip_eletrico()
                sleep(1)
                self.remover_trip_logico()
                sleep(1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetGeral"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_Cala_Sirene"], 1)
                sleep(1)
                return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o comando de reconhese alarmes e reset.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def ajuste_inicial_cx(self):
        if self.ajuste_inicial_cx_esp == -1:
            # Inicializa as variáveis de controle PI para operação TDA Offline
            self.cx_controle_p = (self.leitura_caixa_espiral.valor - self.cfg["press_cx_alvo"]) * self.cfg["cx_kp"]
            self.cx_ajuste_ie = sum(ug.leituras_ug["leitura_potencia"] for ug in self.lista_ugs) / self.cfg["pot_maxima_alvo"]
            self.cx_controle_i = self.cx_ajuste_ie - self.cx_controle_p
            self.ajuste_inicial_cx_esp = 0

    def controle_cx_espiral(self):
        self.ajuste_inicial_cx()

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
        pot_alvo = max(min(round(self.cfg[f"pot_maxima_ug{self.id}"] * self.cx_controle_ie, 5), self.cfg[f"pot_maxima_ug{self.id}"],),self.cfg["pot_minima"],)

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
            logger.error(f"[UG{self.id}] Erro de tipo controle CX Espiral.")
            logger.debug(f"Traceback: {traceback.format_exc()}")

        self.pot_alvo_anterior = pot_alvo

        if self.leitura_caixa_espiral.valor >= 15.5:
            self.enviar_setpoint(pot_alvo)
        else:
            self.enviar_setpoint(0)

    def leituras_temporizadas(self) -> None:
        if self.leitura_voip["leitura_ED_FreioPastilhaGasta"].valor != 0 and not vd.voip_dict[f"FREIO_PASTILHA_GASTA_UG{self.id}"]:
            logger.warning(f"[UG{self.id}] O sensor de Freio da UG retornou que a Pastilha está gasta, favor considerar troca.")
            vd.voip_dict[f"FREIO_PASTILHA_GASTA_UG{self.id}"] = True
        elif self.leitura_voip["leitura_ED_FreioPastilhaGasta"].valor == 0 and vd.voip_dict[f"FREIO_PASTILHA_GASTA_UG{self.id}"]:
            vd.voip_dict[f"FREIO_PASTILHA_GASTA_UG{self.id}"] = False

        if self.leitura_voip["leitura_ED_FiltroPresSujo75Troc"].valor != 0 and not vd.voip_dict[f"FILTRO_PRES_SUJO_75_TROC_UG{self.id}"]:
            logger.warning(f"[UG{self.id}] O sensor do Filtro de Pressão UHRV retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"FILTRO_PRES_SUJO_75_TROC_UG{self.id}"] = True
        elif self.leitura_voip["leitura_ED_FiltroPresSujo75Troc"].valor == 0 and vd.voip_dict[f"FILTRO_PRES_SUJO_75_TROC_UG{self.id}"]:
            vd.voip_dict[f"FILTRO_PRES_SUJO_75_TROC_UG{self.id}"] = False

        if self.leitura_voip["leitura_ED_FiltroRetSujo75Troc"].valor != 0 and not vd.voip_dict[f"FILTRO_RET_SUJO_75_TROC_UG{self.id}"]:
            logger.warning(f"[UG{self.id}] O sensor do Filtro de Retorno UHRV retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"FILTRO_RET_SUJO_75_TROC_UG{self.id}"] = True
        elif self.leitura_voip["leitura_ED_FiltroRetSujo75Troc"].valor == 0 and vd.voip_dict[f"FILTRO_RET_SUJO_75_TROC_UG{self.id}"]:
            vd.voip_dict[f"FILTRO_RET_SUJO_75_TROC_UG{self.id}"] = False

        if self.leitura_voip["leitura_ED_UHLMFilt1PresSujo75Troc"].valor != 0 and not vd.voip_dict[f"UHLM_FILTR_1_PRES_SUJO_75_TROC_UG{self.id}"]:
            logger.warning(f"[UG{self.id}] O sensor do Filtro 1 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"UHLM_FILTR_1_PRES_SUJO_75_TROC_UG{self.id}"] = True
        elif self.leitura_voip["leitura_ED_UHLMFilt1PresSujo75Troc"].valor == 0 and vd.voip_dict[f"UHLM_FILTR_1_PRES_SUJO_75_TROC_UG{self.id}"]:
            vd.voip_dict[f"UHLM_FILTR_1_PRES_SUJO_75_TROC_UG{self.id}"] = False

        if self.leitura_voip["leitura_ED_UHLMFilt2PresSujo75Troc"].valor != 0 and not vd.voip_dict[f"UHLM_FILTR_2_PRES_SUJO_75_TROC_UG{self.id}"]:
            logger.warning(f"[UG{self.id}] O sensor do Filtro 2 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"UHLM_FILTR_2_PRES_SUJO_75_TROC_UG{self.id}"] = True
        elif self.leitura_voip["leitura_ED_UHLMFilt2PresSujo75Troc"].valor == 0 and vd.voip_dict[f"UHLM_FILTR_2_PRES_SUJO_75_TROC_UG{self.id}"]:
            vd.voip_dict[f"UHLM_FILTR_2_PRES_SUJO_75_TROC_UG{self.id}"] = False

        if self.leitura_voip["leitura_ED_FiltroPressaoBbaMecSj75"].valor != 0 and not vd.voip_dict[f"FILTRO_PRESSAO_BBA_MEC_SJ_75_UG{self.id}"]:
            logger.warning(f"[UG{self.id}] O sensor do Filtro de Pressão da Bomba Mecânica retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"FILTRO_PRESSAO_BBA_MEC_SJ_75_UG{self.id}"] = True
        elif self.leitura_voip["leitura_ED_FiltroPressaoBbaMecSj75"].valor == 0 and vd.voip_dict[f"FILTRO_PRESSAO_BBA_MEC_SJ_75_UG{self.id}"]:
            vd.voip_dict[f"FILTRO_PRESSAO_BBA_MEC_SJ_75_UG{self.id}"] = False

        if self.leitura_voip["leitura_ED_TripPartRes"].valor != 0 and not vd.voip_dict[f"TRIP_PART_RES_UG{self.id}"]:
            logger.warning(f"[UG{self.id}] O sensor TripPartRes retornou valor 1.")
            vd.voip_dict[f"TRIP_PART_RES_UG{self.id}"] = True
        elif self.leitura_voip["leitura_ED_TripPartRes"].valor == 0 and vd.voip_dict[f"TRIP_PART_RES_UG{self.id}"]:
            vd.voip_dict[f"TRIP_PART_RES_UG{self.id}"] = False

        if self.leitura_voip["leitura_ED_FreioCmdRemoto"].valor != 1:
            logger.debug(f"[UG{self.id}] O freio da UG saiu do modo remoto, favor analisar a situação.")

        if self.leitura_voip[f"leitura_ED_QCAUG{self.id}_Remoto"].valor != 1:
            logger.debug(f"[UG{self.id}] O compressor da UG saiu do modo remoto, favor analisar a situação.")

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