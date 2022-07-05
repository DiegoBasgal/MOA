import logging
import subprocess
from cmath import sqrt
from datetime import date, datetime, timedelta
from time import sleep

from pyModbusTCP.server import DataBank
from scipy.signal import butter, filtfilt
import src.mensageiro.voip as voip
from src.field_connector import FieldConnector
from src.codes import *
from src.Condicionadores import *

logger = logging.getLogger("__main__")


class Usina:
    def __init__(self, cfg=None, db=None, con=None, leituras=None):

        if not cfg or not db:
            raise ValueError
        else:
            self.cfg = cfg
            self.db = db

        if con:
            self.con = con
        else:  
            from src.field_connector import FieldConnector
            self.con = FieldConnector(self.cfg)

        if leituras:
            self.leituras = leituras
        else:
            from src.LeiturasUSN import LeiturasUSN
            from src.Leituras import LeituraModbus
            from src.Leituras import LeituraModbusBit
            self.leituras = LeiturasUSN(self.cfg)

        self.state_moa = 1

        # Inicializa Objs da usina
        from src.UG1 import UnidadeDeGeracao1
        from src.UG2 import UnidadeDeGeracao2
        from src.UG3 import UnidadeDeGeracao3
        self.ug1 = UnidadeDeGeracao1(1, cfg=self.cfg, leituras_usina=self.leituras)
        self.ug2 = UnidadeDeGeracao2(2, cfg=self.cfg, leituras_usina=self.leituras)
        self.ug3 = UnidadeDeGeracao3(3, cfg=self.cfg, leituras_usina=self.leituras)
        self.ugs = [self.ug1, self.ug2, self.ug3]

        self.avisado_em_eletrica = False

        # Define as vars inciais
        self.ts_ultima_tesntativa_de_normalizacao = datetime.now()
        self.state_moa = 0
        self.controle_p = 0
        self.controle_i = 0
        self.controle_d = 0
        self.clp_emergencia_acionada = 0
        self.db_emergencia_acionada = 0
        self.modo_autonomo = 1
        self.modo_de_escolha_das_ugs = 0
        self.nv_montante_recente = 0
        self.nv_montante_recentes = []
        self.nv_montante_anterior = 0
        self.nv_montante_anteriores = []
        self.erro_nv = 0
        self.erro_nv_anterior = 0
        self.aguardando_reservatorio = 0
        self.pot_disp = 0
        self.agendamentos_atrasados = 0
        self.deve_tentar_normalizar = True
        self.tentativas_de_normalizar = 0
        self.ts_nv = []
        self.condicionadores = []
        self.__split1 = False
        self.__split2 = False
        self.__split3 = False
        clp = ModbusClient(
            host=self.cfg["USN_slave_ip"],
            port=self.cfg["USN_slave_porta"],
            timeout=5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )

        self.leitura_EntradasDigitais_MXI_SA_SEL787_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_SEL787_Trip",
                                                                             self.clp,
                                                                             REG_SA_EntradasDigitais_MXI_SA_SEL787_Trip)
        x = self.leitura_EntradasDigitais_MXI_SA_SEL787_Trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_SEL787_FalhaInterna = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_SEL787_FalhaInterna", self.clp, REG_SA_EntradasDigitais_MXI_SA_SEL787_FalhaInterna)
        x = self.leitura_EntradasDigitais_MXI_SA_SEL787_FalhaInterna
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_SEL311_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_SEL311_Trip",
                                                                             self.clp,
                                                                             REG_SA_EntradasDigitais_MXI_SA_SEL311_Trip)
        x = self.leitura_EntradasDigitais_MXI_SA_SEL311_Trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_SEL311_Falha = LeituraModbusCoil("EntradasDigitais_MXI_SA_SEL311_Falha",
                                                                              self.clp,
                                                                              REG_SA_EntradasDigitais_MXI_SA_SEL311_Falha)
        x = self.leitura_EntradasDigitais_MXI_SA_SEL311_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_MRU3_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRU3_Trip",
                                                                           self.clp,
                                                                           REG_SA_EntradasDigitais_MXI_SA_MRU3_Trip)
        x = self.leitura_EntradasDigitais_MXI_SA_MRU3_Trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_MRU3_Falha = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRU3_Falha",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_MRU3_Falha)
        x = self.leitura_EntradasDigitais_MXI_SA_MRU3_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_MRL1_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_MRL1_Trip",
                                                                           self.clp,
                                                                           REG_SA_EntradasDigitais_MXI_SA_MRL1_Trip)
        x = self.leitura_EntradasDigitais_MXI_SA_MRL1_Trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_CTE_Falta125Vcc = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_CTE_Falta125Vcc", self.clp, REG_SA_EntradasDigitais_MXI_SA_CTE_Falta125Vcc)
        x = self.leitura_EntradasDigitais_MXI_SA_CTE_Falta125Vcc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Fechada = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_CTE_Secc89TE_Fechada", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_CTE_Secc89TE_Fechada)
        x = self.leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Fechada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta", self.clp, REG_SA_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta)
        x = self.leitura_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Disj52G1_Aberto = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_Disj52G1_Aberto", self.clp, REG_SA_EntradasDigitais_MXI_SA_Disj52G1_Aberto)
        x = self.leitura_EntradasDigitais_MXI_SA_Disj52G1_Aberto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Disj52G2_Aberto = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_Disj52G2_Aberto", self.clp, REG_SA_EntradasDigitais_MXI_SA_Disj52G2_Aberto)
        x = self.leitura_EntradasDigitais_MXI_SA_Disj52G2_Aberto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Disj52G3_Aberto = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_Disj52G3_Aberto", self.clp, REG_SA_EntradasDigitais_MXI_SA_Disj52G3_Aberto)
        x = self.leitura_EntradasDigitais_MXI_SA_Disj52G3_Aberto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_Fechado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_DisjDJ1_Fechado", self.clp, REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Fechado)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_Fechado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_Aberto = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_DisjDJ1_Aberto", self.clp, REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Aberto)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_Aberto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_Local = LeituraModbusCoil("EntradasDigitais_MXI_SA_DisjDJ1_Local",
                                                                               self.clp,
                                                                               REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Local)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_Local
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_MolaDescarregada = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_DisjDJ1_MolaDescarregada", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_MolaDescarregada)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_MolaDescarregada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiCom = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiCom", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiCom)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiCom
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiMot = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiMot", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiMot)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiMot
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobFecham = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_DisjDJ1_SuperBobFecham", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobFecham)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobFecham
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert1 = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert1", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert1)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert2 = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert2", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert2)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb1 = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb1", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb1)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb2 = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb2", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb2)
        x = self.leitura_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Secc1_Fechada = LeituraModbusCoil("EntradasDigitais_MXI_SA_Secc1_Fechada",
                                                                               self.clp,
                                                                               REG_SA_EntradasDigitais_MXI_SA_Secc1_Fechada)
        x = self.leitura_EntradasDigitais_MXI_SA_Secc1_Fechada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Secc1_Aberta = LeituraModbusCoil("EntradasDigitais_MXI_SA_Secc1_Aberta",
                                                                              self.clp,
                                                                              REG_SA_EntradasDigitais_MXI_SA_Secc1_Aberta)
        x = self.leitura_EntradasDigitais_MXI_SA_Secc1_Aberta
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Secc2_Fechada = LeituraModbusCoil("EntradasDigitais_MXI_SA_Secc2_Fechada",
                                                                               self.clp,
                                                                               REG_SA_EntradasDigitais_MXI_SA_Secc2_Fechada)
        x = self.leitura_EntradasDigitais_MXI_SA_Secc2_Fechada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Secc2_Aberta = LeituraModbusCoil("EntradasDigitais_MXI_SA_Secc2_Aberta",
                                                                              self.clp,
                                                                              REG_SA_EntradasDigitais_MXI_SA_Secc2_Aberta)
        x = self.leitura_EntradasDigitais_MXI_SA_Secc2_Aberta
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Secc3_Fechada = LeituraModbusCoil("EntradasDigitais_MXI_SA_Secc3_Fechada",
                                                                               self.clp,
                                                                               REG_SA_EntradasDigitais_MXI_SA_Secc3_Fechada)
        x = self.leitura_EntradasDigitais_MXI_SA_Secc3_Fechada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Secc3_Aberta = LeituraModbusCoil("EntradasDigitais_MXI_SA_Secc3_Aberta",
                                                                              self.clp,
                                                                              REG_SA_EntradasDigitais_MXI_SA_Secc3_Aberta)
        x = self.leitura_EntradasDigitais_MXI_SA_Secc3_Aberta
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Secc1_Remoto = LeituraModbusCoil("EntradasDigitais_MXI_SA_Secc1_Remoto",
                                                                              self.clp,
                                                                              REG_SA_EntradasDigitais_MXI_SA_Secc1_Remoto)
        x = self.leitura_EntradasDigitais_MXI_SA_Secc1_Remoto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Secc2_Remoto = LeituraModbusCoil("EntradasDigitais_MXI_SA_Secc2_Remoto",
                                                                              self.clp,
                                                                              REG_SA_EntradasDigitais_MXI_SA_Secc2_Remoto)
        x = self.leitura_EntradasDigitais_MXI_SA_Secc2_Remoto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Secc3_Remoto = LeituraModbusCoil("EntradasDigitais_MXI_SA_Secc3_Remoto",
                                                                              self.clp,
                                                                              REG_SA_EntradasDigitais_MXI_SA_Secc3_Remoto)
        x = self.leitura_EntradasDigitais_MXI_SA_Secc3_Remoto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas)
        x = self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo)
        x = self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao)
        x = self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_TE_AlarmeTempOleo", self.clp, REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo)
        x = self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento)
        x = self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_TE_AlarmeDesligamento", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento)
        x = self.leitura_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_TE_Falha = LeituraModbusCoil("EntradasDigitais_MXI_SA_TE_Falha", self.clp,
                                                                          REG_SA_EntradasDigitais_MXI_SA_TE_Falha)
        x = self.leitura_EntradasDigitais_MXI_SA_TE_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_TE_VentilacaoLig = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_TE_VentilacaoLig", self.clp, REG_SA_EntradasDigitais_MXI_SA_TE_VentilacaoLig)
        x = self.leitura_EntradasDigitais_MXI_SA_TE_VentilacaoLig
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_TE_VentilacaoDeslig = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_TE_VentilacaoDeslig", self.clp, REG_SA_EntradasDigitais_MXI_SA_TE_VentilacaoDeslig)
        x = self.leitura_EntradasDigitais_MXI_SA_TE_VentilacaoDeslig
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_TE_VentilacaoDef = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_TE_VentilacaoDef", self.clp, REG_SA_EntradasDigitais_MXI_SA_TE_VentilacaoDef)
        x = self.leitura_EntradasDigitais_MXI_SA_TE_VentilacaoDef
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsProt = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_FalhaDisjTPsProt", self.clp, REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsProt)
        x = self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsProt
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_FalhaDisjTPsSincr", self.clp, REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr)
        x = self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG1 = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG1", self.clp, REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG1)
        x = self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG2 = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG2", self.clp, REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG2)
        x = self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG3 = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG3", self.clp, REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG3)
        x = self.leitura_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG3
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Disj52G1Selecionado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_Disj52G1Selecionado", self.clp, REG_SA_EntradasDigitais_MXI_SA_Disj52G1Selecionado)
        x = self.leitura_EntradasDigitais_MXI_SA_Disj52G1Selecionado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Disj52G2Selecionado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_Disj52G2Selecionado", self.clp, REG_SA_EntradasDigitais_MXI_SA_Disj52G2Selecionado)
        x = self.leitura_EntradasDigitais_MXI_SA_Disj52G2Selecionado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Disj52G3Selecionado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_Disj52G3Selecionado", self.clp, REG_SA_EntradasDigitais_MXI_SA_Disj52G3Selecionado)
        x = self.leitura_EntradasDigitais_MXI_SA_Disj52G3Selecionado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Disj52G1Sincronizado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_Disj52G1Sincronizado", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_Disj52G1Sincronizado)
        x = self.leitura_EntradasDigitais_MXI_SA_Disj52G1Sincronizado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Disj52G2Sincronizado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_Disj52G2Sincronizado", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_Disj52G2Sincronizado)
        x = self.leitura_EntradasDigitais_MXI_SA_Disj52G2Sincronizado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Disj52G3Sincronizado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_Disj52G3Sincronizado", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_Disj52G3Sincronizado)
        x = self.leitura_EntradasDigitais_MXI_SA_Disj52G3Sincronizado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Reserva252 = LeituraModbusCoil("EntradasDigitais_MXI_SA_Reserva252",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_Reserva252)
        x = self.leitura_EntradasDigitais_MXI_SA_Reserva252
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Reserva253 = LeituraModbusCoil("EntradasDigitais_MXI_SA_Reserva253",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_Reserva253)
        x = self.leitura_EntradasDigitais_MXI_SA_Reserva253
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Reserva254 = LeituraModbusCoil("EntradasDigitais_MXI_SA_Reserva254",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_Reserva254)
        x = self.leitura_EntradasDigitais_MXI_SA_Reserva254
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Reserva255 = LeituraModbusCoil("EntradasDigitais_MXI_SA_Reserva255",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_Reserva255)
        x = self.leitura_EntradasDigitais_MXI_SA_Reserva255
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Reserva256 = LeituraModbusCoil("EntradasDigitais_MXI_SA_Reserva256",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_Reserva256)
        x = self.leitura_EntradasDigitais_MXI_SA_Reserva256
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Reserva257 = LeituraModbusCoil("EntradasDigitais_MXI_SA_Reserva257",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_Reserva257)
        x = self.leitura_EntradasDigitais_MXI_SA_Reserva257
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Fechada = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_CSA1_Secc_Fechada", self.clp, REG_SA_EntradasDigitais_MXI_SA_CSA1_Secc_Fechada)
        x = self.leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Fechada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_CSA1_Secc_Aberta", self.clp, REG_SA_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta)
        x = self.leitura_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_CSA1_FusivelQueimado", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado)
        x = self.leitura_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc)
        x = self.leitura_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_BombasDng_Desliga = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCADE_BombasDng_Desliga", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_QCADE_BombasDng_Desliga)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_BombasDng_Desliga
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_Nivel2 = LeituraModbusCoil("EntradasDigitais_MXI_SA_QCADE_Nivel2",
                                                                              self.clp,
                                                                              REG_SA_EntradasDigitais_MXI_SA_QCADE_Nivel2)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_Nivel2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_Nivel3 = LeituraModbusCoil("EntradasDigitais_MXI_SA_QCADE_Nivel3",
                                                                              self.clp,
                                                                              REG_SA_EntradasDigitais_MXI_SA_QCADE_Nivel3)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_Nivel3
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_Nivel4 = LeituraModbusCoil("EntradasDigitais_MXI_SA_QCADE_Nivel4",
                                                                              self.clp,
                                                                              REG_SA_EntradasDigitais_MXI_SA_QCADE_Nivel4)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_Nivel4
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Fechado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCADE_Disj52E1Fechado", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_QCADE_Disj52E1Fechado)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Fechado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_Falha220VCA = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCADE_Falha220VCA", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCADE_Falha220VCA)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_Falha220VCA
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_BombaDng1_Falha = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCADE_BombaDng1_Falha", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_QCADE_BombaDng1_Falha)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_BombaDng1_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_BombaDng2_Falha = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCADE_BombaDng2_Falha", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_QCADE_BombaDng2_Falha)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_BombaDng2_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_BombaDng3_Falha = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCADE_BombaDng3_Falha", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_QCADE_BombaDng3_Falha)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_BombaDng3_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_BombaDng1_Ligada = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCADE_BombaDng1_Ligada", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_QCADE_BombaDng1_Ligada)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_BombaDng1_Ligada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_BombaDng2_Ligada = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCADE_BombaDng2_Ligada", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_QCADE_BombaDng2_Ligada)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_BombaDng2_Ligada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_BombaDng3_Ligada = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCADE_BombaDng3_Ligada", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_QCADE_BombaDng3_Ligada)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_BombaDng3_Ligada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCADE_BombasDng_Auto = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCADE_BombasDng_Auto", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_QCADE_BombasDng_Auto)
        x = self.leitura_EntradasDigitais_MXI_SA_QCADE_BombasDng_Auto
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Reserva283 = LeituraModbusCoil("EntradasDigitais_MXI_SA_Reserva283",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_Reserva283)
        x = self.leitura_EntradasDigitais_MXI_SA_Reserva283
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QLCF_Disj52EFechado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QLCF_Disj52EFechado", self.clp, REG_SA_EntradasDigitais_MXI_SA_QLCF_Disj52EFechado)
        x = self.leitura_EntradasDigitais_MXI_SA_QLCF_Disj52EFechado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QLCF_Disj52ETrip = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QLCF_Disj52ETrip", self.clp, REG_SA_EntradasDigitais_MXI_SA_QLCF_Disj52ETrip)
        x = self.leitura_EntradasDigitais_MXI_SA_QLCF_Disj52ETrip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QLCF_TripDisjAgrup = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QLCF_TripDisjAgrup", self.clp, REG_SA_EntradasDigitais_MXI_SA_QLCF_TripDisjAgrup)
        x = self.leitura_EntradasDigitais_MXI_SA_QLCF_TripDisjAgrup
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Reserva287 = LeituraModbusCoil("EntradasDigitais_MXI_SA_Reserva287",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_Reserva287)
        x = self.leitura_EntradasDigitais_MXI_SA_Reserva287
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCCP_Disj72EFechado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCCP_Disj72EFechado", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCCP_Disj72EFechado)
        x = self.leitura_EntradasDigitais_MXI_SA_QCCP_Disj72EFechado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCCP_Disj72ETrip", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip)
        x = self.leitura_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCCP_Falta125Vcc", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc)
        x = self.leitura_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup)
        x = self.leitura_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_MSS_EmergAtuada = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_MSS_EmergAtuada", self.clp, REG_SA_EntradasDigitais_MXI_SA_MSS_EmergAtuada)
        x = self.leitura_EntradasDigitais_MXI_SA_MSS_EmergAtuada
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_MSS_FalhaSwitch = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_MSS_FalhaSwitch", self.clp, REG_SA_EntradasDigitais_MXI_SA_MSS_FalhaSwitch)
        x = self.leitura_EntradasDigitais_MXI_SA_MSS_FalhaSwitch
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_MSS_FalhaConvCACCEntr = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_MSS_FalhaConvCACCEntr", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_MSS_FalhaConvCACCEntr)
        x = self.leitura_EntradasDigitais_MXI_SA_MSS_FalhaConvCACCEntr
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_MSS_FalhaConvCACCRedeCA = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_MSS_FalhaConvCACCRedeCA", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_MSS_FalhaConvCACCRedeCA)
        x = self.leitura_EntradasDigitais_MXI_SA_MSS_FalhaConvCACCRedeCA
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_MSS_FalhaConvCACCSaidaCA = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_MSS_FalhaConvCACCSaidaCA", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_MSS_FalhaConvCACCSaidaCA)
        x = self.leitura_EntradasDigitais_MXI_SA_MSS_FalhaConvCACCSaidaCA
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCAP_Falta125Vcc", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc)
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup)
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Fechado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCAP_Disj52A1Fechado", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52A1Fechado)
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Fechado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha)
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFechado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCAP_Disj52EFechado", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52EFechado)
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFechado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCAP_Disj52EFalha", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha)
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteGE = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCAP_TensaoPresenteGE", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteGE)
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteGE
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA)
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCAP_Automatico = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCAP_Automatico", self.clp, REG_SA_EntradasDigitais_MXI_SA_QCAP_Automatico)
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_Automatico
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_QCAP_SubtensaoBarraGeral = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_QCAP_SubtensaoBarraGeral", self.clp,
            REG_SA_EntradasDigitais_MXI_SA_QCAP_SubtensaoBarraGeral)
        x = self.leitura_EntradasDigitais_MXI_SA_QCAP_SubtensaoBarraGeral
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Reserva313 = LeituraModbusCoil("EntradasDigitais_MXI_SA_Reserva313",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_Reserva313)
        x = self.leitura_EntradasDigitais_MXI_SA_Reserva313
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Reserva314 = LeituraModbusCoil("EntradasDigitais_MXI_SA_Reserva314",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_Reserva314)
        x = self.leitura_EntradasDigitais_MXI_SA_Reserva314
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Reserva315 = LeituraModbusCoil("EntradasDigitais_MXI_SA_Reserva315",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_Reserva315)
        x = self.leitura_EntradasDigitais_MXI_SA_Reserva315
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Reserva316 = LeituraModbusCoil("EntradasDigitais_MXI_SA_Reserva316",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_Reserva316)
        x = self.leitura_EntradasDigitais_MXI_SA_Reserva316
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_Reserva317 = LeituraModbusCoil("EntradasDigitais_MXI_SA_Reserva317",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_Reserva317)
        x = self.leitura_EntradasDigitais_MXI_SA_Reserva317
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_GMG_Alarme = LeituraModbusCoil("EntradasDigitais_MXI_SA_GMG_Alarme",
                                                                            self.clp,
                                                                            REG_SA_EntradasDigitais_MXI_SA_GMG_Alarme)
        x = self.leitura_EntradasDigitais_MXI_SA_GMG_Alarme
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_GMG_Trip = LeituraModbusCoil("EntradasDigitais_MXI_SA_GMG_Trip", self.clp,
                                                                          REG_SA_EntradasDigitais_MXI_SA_GMG_Trip)
        x = self.leitura_EntradasDigitais_MXI_SA_GMG_Trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_GMG_Operacao = LeituraModbusCoil("EntradasDigitais_MXI_SA_GMG_Operacao",
                                                                              self.clp,
                                                                              REG_SA_EntradasDigitais_MXI_SA_GMG_Operacao)
        x = self.leitura_EntradasDigitais_MXI_SA_GMG_Operacao
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_GMG_BaixoComb = LeituraModbusCoil("EntradasDigitais_MXI_SA_GMG_BaixoComb",
                                                                               self.clp,
                                                                               REG_SA_EntradasDigitais_MXI_SA_GMG_BaixoComb)
        x = self.leitura_EntradasDigitais_MXI_SA_GMG_BaixoComb
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_GMG_Automatico = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_GMG_Automatico", self.clp, REG_SA_EntradasDigitais_MXI_SA_GMG_Automatico)
        x = self.leitura_EntradasDigitais_MXI_SA_GMG_Automatico
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_SA_GMG_DisjFechado = LeituraModbusCoil(
            "EntradasDigitais_MXI_SA_GMG_DisjFechado", self.clp, REG_SA_EntradasDigitais_MXI_SA_GMG_DisjFechado)
        x = self.leitura_EntradasDigitais_MXI_SA_GMG_DisjFechado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_ResetGeral = LeituraModbusCoil("ComandosDigitais_MXW_ResetGeral", self.clp,
                                                                         REG_SA_ComandosDigitais_MXW_ResetGeral)
        x = self.leitura_ComandosDigitais_MXW_ResetGeral
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Liga_Secc1 = LeituraModbusCoil("ComandosDigitais_MXW_Liga_Secc1", self.clp,
                                                                         REG_SA_ComandosDigitais_MXW_Liga_Secc1)
        x = self.leitura_ComandosDigitais_MXW_Liga_Secc1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Desliga_Secc1 = LeituraModbusCoil("ComandosDigitais_MXW_Desliga_Secc1",
                                                                            self.clp,
                                                                            REG_SA_ComandosDigitais_MXW_Desliga_Secc1)
        x = self.leitura_ComandosDigitais_MXW_Desliga_Secc1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Liga_Secc2 = LeituraModbusCoil("ComandosDigitais_MXW_Liga_Secc2", self.clp,
                                                                         REG_SA_ComandosDigitais_MXW_Liga_Secc2)
        x = self.leitura_ComandosDigitais_MXW_Liga_Secc2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Desliga_Secc2 = LeituraModbusCoil("ComandosDigitais_MXW_Desliga_Secc2",
                                                                            self.clp,
                                                                            REG_SA_ComandosDigitais_MXW_Desliga_Secc2)
        x = self.leitura_ComandosDigitais_MXW_Desliga_Secc2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Liga_Secc3 = LeituraModbusCoil("ComandosDigitais_MXW_Liga_Secc3", self.clp,
                                                                         REG_SA_ComandosDigitais_MXW_Liga_Secc3)
        x = self.leitura_ComandosDigitais_MXW_Liga_Secc3
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Desliga_Secc3 = LeituraModbusCoil("ComandosDigitais_MXW_Desliga_Secc3",
                                                                            self.clp,
                                                                            REG_SA_ComandosDigitais_MXW_Desliga_Secc3)
        x = self.leitura_ComandosDigitais_MXW_Desliga_Secc3
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Liga_BbaDren1 = LeituraModbusCoil("ComandosDigitais_MXW_Liga_BbaDren1",
                                                                            self.clp,
                                                                            REG_SA_ComandosDigitais_MXW_Liga_BbaDren1)
        x = self.leitura_ComandosDigitais_MXW_Liga_BbaDren1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Desliga_BbaDren1 = LeituraModbusCoil("ComandosDigitais_MXW_Desliga_BbaDren1",
                                                                               self.clp,
                                                                               REG_SA_ComandosDigitais_MXW_Desliga_BbaDren1)
        x = self.leitura_ComandosDigitais_MXW_Desliga_BbaDren1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Liga_BbaDren2 = LeituraModbusCoil("ComandosDigitais_MXW_Liga_BbaDren2",
                                                                            self.clp,
                                                                            REG_SA_ComandosDigitais_MXW_Liga_BbaDren2)
        x = self.leitura_ComandosDigitais_MXW_Liga_BbaDren2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Desliga_BbaDren2 = LeituraModbusCoil("ComandosDigitais_MXW_Desliga_BbaDren2",
                                                                               self.clp,
                                                                               REG_SA_ComandosDigitais_MXW_Desliga_BbaDren2)
        x = self.leitura_ComandosDigitais_MXW_Desliga_BbaDren2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Liga_BbaDren3 = LeituraModbusCoil("ComandosDigitais_MXW_Liga_BbaDren3",
                                                                            self.clp,
                                                                            REG_SA_ComandosDigitais_MXW_Liga_BbaDren3)
        x = self.leitura_ComandosDigitais_MXW_Liga_BbaDren3
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Desliga_BbaDren3 = LeituraModbusCoil("ComandosDigitais_MXW_Desliga_BbaDren3",
                                                                               self.clp,
                                                                               REG_SA_ComandosDigitais_MXW_Desliga_BbaDren3)
        x = self.leitura_ComandosDigitais_MXW_Desliga_BbaDren3
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_ResetRele787 = LeituraModbusCoil("ComandosDigitais_MXW_ResetRele787",
                                                                           self.clp,
                                                                           REG_SA_ComandosDigitais_MXW_ResetRele787)
        x = self.leitura_ComandosDigitais_MXW_ResetRele787
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_ResetRele59N = LeituraModbusCoil("ComandosDigitais_MXW_ResetRele59N",
                                                                           self.clp,
                                                                           REG_SA_ComandosDigitais_MXW_ResetRele59N)
        x = self.leitura_ComandosDigitais_MXW_ResetRele59N
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_ResetRele311 = LeituraModbusCoil("ComandosDigitais_MXW_ResetRele311",
                                                                           self.clp,
                                                                           REG_SA_ComandosDigitais_MXW_ResetRele311)
        x = self.leitura_ComandosDigitais_MXW_ResetRele311
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_ResetReleMRL1 = LeituraModbusCoil("ComandosDigitais_MXW_ResetReleMRL1",
                                                                            self.clp,
                                                                            REG_SA_ComandosDigitais_MXW_ResetReleMRL1)
        x = self.leitura_ComandosDigitais_MXW_ResetReleMRL1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Liga_DJ1 = LeituraModbusCoil("ComandosDigitais_MXW_Liga_DJ1", self.clp,
                                                                       REG_SA_ComandosDigitais_MXW_Liga_DJ1)
        x = self.leitura_ComandosDigitais_MXW_Liga_DJ1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Desliga_DJ1 = LeituraModbusCoil("ComandosDigitais_MXW_Desliga_DJ1", self.clp,
                                                                          REG_SA_ComandosDigitais_MXW_Desliga_DJ1)
        x = self.leitura_ComandosDigitais_MXW_Desliga_DJ1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Liga_Disj52A1 = LeituraModbusCoil("ComandosDigitais_MXW_Liga_Disj52A1",
                                                                            self.clp,
                                                                            REG_SA_ComandosDigitais_MXW_Liga_Disj52A1)
        x = self.leitura_ComandosDigitais_MXW_Liga_Disj52A1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Desliga_Disj52A1 = LeituraModbusCoil("ComandosDigitais_MXW_Desliga_Disj52A1",
                                                                               self.clp,
                                                                               REG_SA_ComandosDigitais_MXW_Desliga_Disj52A1)
        x = self.leitura_ComandosDigitais_MXW_Desliga_Disj52A1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Liga_Disj52E = LeituraModbusCoil("ComandosDigitais_MXW_Liga_Disj52E",
                                                                           self.clp,
                                                                           REG_SA_ComandosDigitais_MXW_Liga_Disj52E)
        x = self.leitura_ComandosDigitais_MXW_Liga_Disj52E
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Desliga_Disj52E = LeituraModbusCoil("ComandosDigitais_MXW_Desliga_Disj52E",
                                                                              self.clp,
                                                                              REG_SA_ComandosDigitais_MXW_Desliga_Disj52E)
        x = self.leitura_ComandosDigitais_MXW_Desliga_Disj52E
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_GMG_Liga = LeituraModbusCoil("ComandosDigitais_MXW_GMG_Liga", self.clp,
                                                                       REG_SA_ComandosDigitais_MXW_GMG_Liga)
        x = self.leitura_ComandosDigitais_MXW_GMG_Liga
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_GMG_Desl = LeituraModbusCoil("ComandosDigitais_MXW_GMG_Desl", self.clp,
                                                                       REG_SA_ComandosDigitais_MXW_GMG_Desl)
        x = self.leitura_ComandosDigitais_MXW_GMG_Desl
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_QCAP_Autom = LeituraModbusCoil("ComandosDigitais_MXW_QCAP_Autom", self.clp,
                                                                         REG_SA_ComandosDigitais_MXW_QCAP_Autom)
        x = self.leitura_ComandosDigitais_MXW_QCAP_Autom
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_QCAP_Manual = LeituraModbusCoil("ComandosDigitais_MXW_QCAP_Manual", self.clp,
                                                                          REG_SA_ComandosDigitais_MXW_QCAP_Manual)
        x = self.leitura_ComandosDigitais_MXW_QCAP_Manual
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ComandosDigitais_MXW_Cala_Sirene = LeituraModbusCoil("ComandosDigitais_MXW_Cala_Sirene", self.clp,
                                                                          REG_SA_ComandosDigitais_MXW_Cala_Sirene)
        x = self.leitura_ComandosDigitais_MXW_Cala_Sirene
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM_810_Tensao_AB = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM_810_Tensao_AB", self.clp, REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_AB)
        x = self.leitura_RetornosAnalogicos_MWR_PM_810_Tensao_AB
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM_810_Tensao_BC = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM_810_Tensao_BC", self.clp, REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_BC)
        x = self.leitura_RetornosAnalogicos_MWR_PM_810_Tensao_BC
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM_810_Tensao_CA = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM_810_Tensao_CA", self.clp, REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_CA)
        x = self.leitura_RetornosAnalogicos_MWR_PM_810_Tensao_CA
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM_810_Corrente_A = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM_810_Corrente_A", self.clp, REG_SA_RetornosAnalogicos_MWR_PM_810_Corrente_A)
        x = self.leitura_RetornosAnalogicos_MWR_PM_810_Corrente_A
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM_810_Corrente_B = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM_810_Corrente_B", self.clp, REG_SA_RetornosAnalogicos_MWR_PM_810_Corrente_B)
        x = self.leitura_RetornosAnalogicos_MWR_PM_810_Corrente_B
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM_810_Corrente_C = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM_810_Corrente_C", self.clp, REG_SA_RetornosAnalogicos_MWR_PM_810_Corrente_C)
        x = self.leitura_RetornosAnalogicos_MWR_PM_810_Corrente_C
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM_810_Frequencia = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM_810_Frequencia", self.clp, REG_SA_RetornosAnalogicos_MWR_PM_810_Frequencia)
        x = self.leitura_RetornosAnalogicos_MWR_PM_810_Frequencia
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM_810_Fator_Potencia = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM_810_Fator_Potencia", self.clp,
            REG_SA_RetornosAnalogicos_MWR_PM_810_Fator_Potencia)
        x = self.leitura_RetornosAnalogicos_MWR_PM_810_Fator_Potencia
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM_810_Potencia_Aparente = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM_810_Potencia_Aparente", self.clp,
            REG_SA_RetornosAnalogicos_MWR_PM_810_Potencia_Aparente)
        x = self.leitura_RetornosAnalogicos_MWR_PM_810_Potencia_Aparente
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM_810_Potencia_Reativa = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM_810_Potencia_Reativa", self.clp,
            REG_SA_RetornosAnalogicos_MWR_PM_810_Potencia_Reativa)
        x = self.leitura_RetornosAnalogicos_MWR_PM_810_Potencia_Reativa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM_810_Potencia_Ativa = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM_810_Potencia_Ativa", self.clp,
            REG_SA_RetornosAnalogicos_MWR_PM_810_Potencia_Ativa)
        x = self.leitura_RetornosAnalogicos_MWR_PM_810_Potencia_Ativa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM1_710_Tensao_AB = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM1_710_Tensao_AB", self.clp, REG_SA_RetornosAnalogicos_MWR_PM1_710_Tensao_AB)
        x = self.leitura_RetornosAnalogicos_MWR_PM1_710_Tensao_AB
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM1_710_Tensao_BC = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM1_710_Tensao_BC", self.clp, REG_SA_RetornosAnalogicos_MWR_PM1_710_Tensao_BC)
        x = self.leitura_RetornosAnalogicos_MWR_PM1_710_Tensao_BC
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM1_710_Tensao_CA = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM1_710_Tensao_CA", self.clp, REG_SA_RetornosAnalogicos_MWR_PM1_710_Tensao_CA)
        x = self.leitura_RetornosAnalogicos_MWR_PM1_710_Tensao_CA
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM1_710_Corrente_A = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM1_710_Corrente_A", self.clp, REG_SA_RetornosAnalogicos_MWR_PM1_710_Corrente_A)
        x = self.leitura_RetornosAnalogicos_MWR_PM1_710_Corrente_A
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM1_710_Corrente_B = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM1_710_Corrente_B", self.clp, REG_SA_RetornosAnalogicos_MWR_PM1_710_Corrente_B)
        x = self.leitura_RetornosAnalogicos_MWR_PM1_710_Corrente_B
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM1_710_Corrente_C = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM1_710_Corrente_C", self.clp, REG_SA_RetornosAnalogicos_MWR_PM1_710_Corrente_C)
        x = self.leitura_RetornosAnalogicos_MWR_PM1_710_Corrente_C
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM1_710_Frequencia = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM1_710_Frequencia", self.clp, REG_SA_RetornosAnalogicos_MWR_PM1_710_Frequencia)
        x = self.leitura_RetornosAnalogicos_MWR_PM1_710_Frequencia
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM1_710_Fator_Potencia = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM1_710_Fator_Potencia", self.clp,
            REG_SA_RetornosAnalogicos_MWR_PM1_710_Fator_Potencia)
        x = self.leitura_RetornosAnalogicos_MWR_PM1_710_Fator_Potencia
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM1_710_Potencia_Aparente = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM1_710_Potencia_Aparente", self.clp,
            REG_SA_RetornosAnalogicos_MWR_PM1_710_Potencia_Aparente)
        x = self.leitura_RetornosAnalogicos_MWR_PM1_710_Potencia_Aparente
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM1_710_Potencia_Reativa = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM1_710_Potencia_Reativa", self.clp,
            REG_SA_RetornosAnalogicos_MWR_PM1_710_Potencia_Reativa)
        x = self.leitura_RetornosAnalogicos_MWR_PM1_710_Potencia_Reativa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM1_710_Potencia_Ativa = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM1_710_Potencia_Ativa", self.clp,
            REG_SA_RetornosAnalogicos_MWR_PM1_710_Potencia_Ativa)
        x = self.leitura_RetornosAnalogicos_MWR_PM1_710_Potencia_Ativa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_Reserva43 = LeituraModbusCoil("RetornosAnalogicos_MWR_Reserva43", self.clp,
                                                                          REG_SA_RetornosAnalogicos_MWR_Reserva43)
        x = self.leitura_RetornosAnalogicos_MWR_Reserva43
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_Reserva44 = LeituraModbusCoil("RetornosAnalogicos_MWR_Reserva44", self.clp,
                                                                          REG_SA_RetornosAnalogicos_MWR_Reserva44)
        x = self.leitura_RetornosAnalogicos_MWR_Reserva44
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_Reserva45 = LeituraModbusCoil("RetornosAnalogicos_MWR_Reserva45", self.clp,
                                                                          REG_SA_RetornosAnalogicos_MWR_Reserva45)
        x = self.leitura_RetornosAnalogicos_MWR_Reserva45
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM2_710_Tensao_AB = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM2_710_Tensao_AB", self.clp, REG_SA_RetornosAnalogicos_MWR_PM2_710_Tensao_AB)
        x = self.leitura_RetornosAnalogicos_MWR_PM2_710_Tensao_AB
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM2_710_Tensao_BC = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM2_710_Tensao_BC", self.clp, REG_SA_RetornosAnalogicos_MWR_PM2_710_Tensao_BC)
        x = self.leitura_RetornosAnalogicos_MWR_PM2_710_Tensao_BC
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM2_710_Tensao_CA = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM2_710_Tensao_CA", self.clp, REG_SA_RetornosAnalogicos_MWR_PM2_710_Tensao_CA)
        x = self.leitura_RetornosAnalogicos_MWR_PM2_710_Tensao_CA
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM2_710_Corrente_A = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM2_710_Corrente_A", self.clp, REG_SA_RetornosAnalogicos_MWR_PM2_710_Corrente_A)
        x = self.leitura_RetornosAnalogicos_MWR_PM2_710_Corrente_A
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM2_710_Corrente_B = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM2_710_Corrente_B", self.clp, REG_SA_RetornosAnalogicos_MWR_PM2_710_Corrente_B)
        x = self.leitura_RetornosAnalogicos_MWR_PM2_710_Corrente_B
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM2_710_Corrente_C = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM2_710_Corrente_C", self.clp, REG_SA_RetornosAnalogicos_MWR_PM2_710_Corrente_C)
        x = self.leitura_RetornosAnalogicos_MWR_PM2_710_Corrente_C
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM2_710_Frequencia = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM2_710_Frequencia", self.clp, REG_SA_RetornosAnalogicos_MWR_PM2_710_Frequencia)
        x = self.leitura_RetornosAnalogicos_MWR_PM2_710_Frequencia
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM2_710_Fator_Potencia = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM2_710_Fator_Potencia", self.clp,
            REG_SA_RetornosAnalogicos_MWR_PM2_710_Fator_Potencia)
        x = self.leitura_RetornosAnalogicos_MWR_PM2_710_Fator_Potencia
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM2_710_Potencia_Aparente = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM2_710_Potencia_Aparente", self.clp,
            REG_SA_RetornosAnalogicos_MWR_PM2_710_Potencia_Aparente)
        x = self.leitura_RetornosAnalogicos_MWR_PM2_710_Potencia_Aparente
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM2_710_Potencia_Reativa = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM2_710_Potencia_Reativa", self.clp,
            REG_SA_RetornosAnalogicos_MWR_PM2_710_Potencia_Reativa)
        x = self.leitura_RetornosAnalogicos_MWR_PM2_710_Potencia_Reativa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_PM2_710_Potencia_Ativa = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_PM2_710_Potencia_Ativa", self.clp,
            REG_SA_RetornosAnalogicos_MWR_PM2_710_Potencia_Ativa)
        x = self.leitura_RetornosAnalogicos_MWR_PM2_710_Potencia_Ativa
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_Reserva61 = LeituraModbusCoil("RetornosAnalogicos_MWR_Reserva61", self.clp,
                                                                          REG_SA_RetornosAnalogicos_MWR_Reserva61)
        x = self.leitura_RetornosAnalogicos_MWR_Reserva61
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_Reserva62 = LeituraModbusCoil("RetornosAnalogicos_MWR_Reserva62", self.clp,
                                                                          REG_SA_RetornosAnalogicos_MWR_Reserva62)
        x = self.leitura_RetornosAnalogicos_MWR_Reserva62
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_Reserva63 = LeituraModbusCoil("RetornosAnalogicos_MWR_Reserva63", self.clp,
                                                                          REG_SA_RetornosAnalogicos_MWR_Reserva63)
        x = self.leitura_RetornosAnalogicos_MWR_Reserva63
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_CorrenteBaixa1 = LeituraModbusCoil("RetornosAnalogicos_MWR_CorrenteBaixa1",
                                                                               self.clp,
                                                                               REG_SA_RetornosAnalogicos_MWR_CorrenteBaixa1)
        x = self.leitura_RetornosAnalogicos_MWR_CorrenteBaixa1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_CorrenteBaixa2 = LeituraModbusCoil("RetornosAnalogicos_MWR_CorrenteBaixa2",
                                                                               self.clp,
                                                                               REG_SA_RetornosAnalogicos_MWR_CorrenteBaixa2)
        x = self.leitura_RetornosAnalogicos_MWR_CorrenteBaixa2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_CorrenteBaixa3 = LeituraModbusCoil("RetornosAnalogicos_MWR_CorrenteBaixa3",
                                                                               self.clp,
                                                                               REG_SA_RetornosAnalogicos_MWR_CorrenteBaixa3)
        x = self.leitura_RetornosAnalogicos_MWR_CorrenteBaixa3
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_CorrenteAlta1 = LeituraModbusCoil("RetornosAnalogicos_MWR_CorrenteAlta1",
                                                                              self.clp,
                                                                              REG_SA_RetornosAnalogicos_MWR_CorrenteAlta1)
        x = self.leitura_RetornosAnalogicos_MWR_CorrenteAlta1
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_CorrenteAlta2 = LeituraModbusCoil("RetornosAnalogicos_MWR_CorrenteAlta2",
                                                                              self.clp,
                                                                              REG_SA_RetornosAnalogicos_MWR_CorrenteAlta2)
        x = self.leitura_RetornosAnalogicos_MWR_CorrenteAlta2
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_CorrenteAlta3 = LeituraModbusCoil("RetornosAnalogicos_MWR_CorrenteAlta3",
                                                                              self.clp,
                                                                              REG_SA_RetornosAnalogicos_MWR_CorrenteAlta3)
        x = self.leitura_RetornosAnalogicos_MWR_CorrenteAlta3
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_CorrenteNeutro = LeituraModbusCoil("RetornosAnalogicos_MWR_CorrenteNeutro",
                                                                               self.clp,
                                                                               REG_SA_RetornosAnalogicos_MWR_CorrenteNeutro)
        x = self.leitura_RetornosAnalogicos_MWR_CorrenteNeutro
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets = LeituraModbusCoil("RetornosAnalogicos_MWR_SEL787_Targets",
                                                                               self.clp,
                                                                               REG_SA_RetornosAnalogicos_MWR_SEL787_Targets)
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00 = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00", self.clp,
            REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00)
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01 = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01", self.clp,
            REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01)
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02 = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02", self.clp,
            REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02)
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03 = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03", self.clp,
            REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03)
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04 = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04", self.clp,
            REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04)
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05 = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05", self.clp,
            REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05)
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06 = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06", self.clp,
            REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06)
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07 = LeituraModbusCoil(
            "RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07", self.clp,
            REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07)
        x = self.leitura_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_BbaDren1_FalhaAcion = LeituraModbusCoil(
            "RetornosDigitais_MXR_BbaDren1_FalhaAcion", self.clp, REG_SA_RetornosDigitais_MXR_BbaDren1_FalhaAcion)
        x = self.leitura_RetornosDigitais_MXR_BbaDren1_FalhaAcion
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_BbaDren2_FalhaAcion = LeituraModbusCoil(
            "RetornosDigitais_MXR_BbaDren2_FalhaAcion", self.clp, REG_SA_RetornosDigitais_MXR_BbaDren2_FalhaAcion)
        x = self.leitura_RetornosDigitais_MXR_BbaDren2_FalhaAcion
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_BbaDren3_FalhaAcion = LeituraModbusCoil(
            "RetornosDigitais_MXR_BbaDren3_FalhaAcion", self.clp, REG_SA_RetornosDigitais_MXR_BbaDren3_FalhaAcion)
        x = self.leitura_RetornosDigitais_MXR_BbaDren3_FalhaAcion
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_Timeout_Sincronismo = LeituraModbusCoil(
            "RetornosDigitais_MXR_Timeout_Sincronismo", self.clp, REG_SA_RetornosDigitais_MXR_Timeout_Sincronismo)
        x = self.leitura_RetornosDigitais_MXR_Timeout_Sincronismo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_DJ1_FalhaInt = LeituraModbusCoil("RetornosDigitais_MXR_DJ1_FalhaInt",
                                                                           self.clp,
                                                                           REG_SA_RetornosDigitais_MXR_DJ1_FalhaInt)
        x = self.leitura_RetornosDigitais_MXR_DJ1_FalhaInt
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_RetornosDigitais_MXR_CLP_Falha = LeituraModbusCoil("RetornosDigitais_MXR_CLP_Falha", self.clp,
                                                                        REG_SA_RetornosDigitais_MXR_CLP_Falha)
        x = self.leitura_RetornosDigitais_MXR_CLP_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_QcataDisj52ETrip = LeituraModbusCoil("EntradasDigitais_MXI_QcataDisj52ETrip",
                                                                               self.clp,
                                                                               REG_TDA_EntradasDigitais_MXI_QcataDisj52ETrip)
        x = self.leitura_EntradasDigitais_MXI_QcataDisj52ETrip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_QcataDisj52ETripDisjSai = LeituraModbusCoil(
            "EntradasDigitais_MXI_QcataDisj52ETripDisjSai", self.clp,
            REG_TDA_EntradasDigitais_MXI_QcataDisj52ETripDisjSai)
        x = self.leitura_EntradasDigitais_MXI_QcataDisj52ETripDisjSai
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_EntradasDigitais_MXI_QcataDisj52EFalha380VCA = LeituraModbusCoil(
            "EntradasDigitais_MXI_QcataDisj52EFalha380VCA", self.clp,
            REG_TDA_EntradasDigitais_MXI_QcataDisj52EFalha380VCA)
        x = self.leitura_EntradasDigitais_MXI_QcataDisj52EFalha380VCA
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        pars = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            self.cfg["kp"],
            self.cfg["ki"],
            self.cfg["kd"],
            self.cfg["kie"],
            0, #self.n_movel_l,
            0, #self.n_movel_r,
            self.cfg["nv_alvo"],
        ]
        self.con.open()
        self.db.update_parametros_usina(pars)

        # ajuste inicial ie
        if self.cfg["saida_ie_inicial"] == "auto":
            self.controle_ie = (
                self.ug1.leitura_potencia.valor + self.ug2.leitura_potencia.valor + self.ug3.leitura_potencia.valor
            ) / self.cfg["pot_maxima_alvo"]
        else:
            self.controle_ie = self.cfg["saida_ie_inicial"]

        self.controle_i = self.controle_ie

        # ajuste inicial SP
        logger.debug("self.ug1.leitura_potencia.valor -> {}".format(self.ug1.leitura_potencia.valor))
        logger.debug("self.ug2.leitura_potencia.valor -> {}".format(self.ug2.leitura_potencia.valor))
        logger.debug("self.ug3.leitura_potencia.valor -> {}".format(self.ug3.leitura_potencia.valor))
        self.ug1.setpoint = self.ug1.leitura_potencia.valor
        self.ug2.setpoint = self.ug2.leitura_potencia.valor
        self.ug3.setpoint = self.ug3.leitura_potencia.valor

    @property
    def nv_montante(self):
        return self.leituras.nv_montante.valor

    def ler_valores(self):

        # CLP
        # regs = [0]*40000
        # aux = self.clp.read_sequential(40000, 101)
        # regs += aux
        # USN
        # self.clp_emergencia_acionada = regs[self.cfg['ENDERECO_CLP_USINA_FLAGS']]
        # self.nv_montante = round((regs[self.cfg['ENDERECO_CLP_NV_MONATNTE']] * 0.001) + 620, 2)
        # self.pot_medidor = round((regs[self.cfg['ENDERECO_CLP_MEDIDOR']] * 0.001), 3)
        
        # -> Verifica conexão com CLP Tomada d'água
        #   -> Se não estiver ok, acionar emergencia CLP
        if not ping(self.cfg["TDA_slave_ip"]):
            logger.warning("CLP TDA não respondeu a tentativa de comunicação!")
            # self.acionar_emergencia()

        # -> Verifica conexão com CLP Sub
        #   -> Se não estiver ok, avisa por logger.warning
        if not ping(self.cfg["USN_slave_ip"]):
            logger.warning("CLP 'USN' (PACP) não respondeu a tentativa de comunicação!")

        # -> Verifica conexão com CLP UG#
        #    -> Se não estiver ok, acionar indisponibiliza UG# e avisa por logger.warning
        if not ping(self.cfg["UG1_slave_ip"]):
            logger.warning("CLP UG1 não respondeu a tentativa de comunicação!")
            self.ug1.forcar_estado_restrito()

        if not ping(self.cfg["UG2_slave_ip"]):
            logger.warning("CLP UG2 não respondeu a tentativa de comunicação!")
            self.ug2.forcar_estado_restrito()

        if not ping(self.cfg["UG3_slave_ip"]):
            logger.warning("CLP UG3 não respondeu a tentativa de comunicação!")
            self.ug3.forcar_estado_restrito()

        self.clp_online = True
        self.clp_emergencia_acionada = 0

        if self.nv_montante_recente < 1:
            self.nv_montante_recentes = [self.leituras.nv_montante.valor] * 240
        self.nv_montante_recentes.append(
            round(self.leituras.nv_montante.valor, 2)
        )
        self.nv_montante_recentes = self.nv_montante_recentes[1:]

        """
        # Filtro butterworth
        b, a = butter(8, 4, fs=120)
        self.nv_montante_recente = float(
            filtfilt(b, a, self.nv_montante_recentes)[-1]
        )
        """

        smoothing = 5
        ema = [sum(self.nv_montante_recentes) / len(self.nv_montante_recentes)]
        for nv in self.nv_montante_recentes:
            ema.append((nv * (smoothing / (1 + len(self.nv_montante_recentes)))) + ema[-1] * (1 - (smoothing / (1 + len(self.nv_montante_recentes)))))
        self.nv_montante_recente = ema[-1]

        self.erro_nv_anterior = self.erro_nv
        self.erro_nv = self.nv_montante_recente - self.cfg["nv_alvo"]

        # DB
        #
        # Ler apenas os parametros que estao disponiveis no django
        #  - Botão de emergência
        #  - Limites de operação das UGS
        #  - Modo autonomo
        #  - Modo de prioridade UGS

        parametros = self.db.get_parametros_usina()

        # Botão de emergência
        self.db_emergencia_acionada = int(parametros["emergencia_acionada"])

        # Limites de operação das UGS
        # for ug in self.ugs:
        for ug in self.ugs:
            try:
                ug.prioridade = int(parametros["ug{}_prioridade".format(ug.id)])
                """
                ug.condicionador_perda_na_grade.valor_base = float(
                    parametros["ug{}_perda_grade_alerta".format(ug.id)]
                )
                ug.condicionador_perda_na_grade.valor_limite = float(
                    parametros["ug{}_perda_grade_maxima".format(ug.id)]
                )
                ug.condicionador_temperatura_enrolamento_fase_r.valor_base = float(
                    parametros["temperatura_alerta_enrolamento_fase_r_ug{}".format(ug.id)]
                )
                ug.condicionador_temperatura_enrolamento_fase_s.valor_base = float(
                    parametros["temperatura_alerta_enrolamento_fase_s_ug{}".format(ug.id)]
                )
                ug.condicionador_temperatura_enrolamento_fase_t.valor_base = float(
                    parametros["temperatura_alerta_enrolamento_fase_t_ug{}".format(ug.id)]
                )
                ug.condicionador_temperatura_mancal_la_casquilho.valor_base = float(
                    parametros["temperatura_alerta_mancal_la_casquilho_ug{}".format(ug.id)]
                )
                ug.condicionador_temperatura_mancal_la_contra_escora_1.valor_base = float(
                    parametros[
                        "temperatura_alerta_mancal_la_contra_escora_1_ug{}".format(ug.id)
                    ]
                )
                ug.condicionador_temperatura_mancal_la_contra_escora_2.valor_base = float(
                    parametros[
                        "temperatura_alerta_mancal_la_contra_escora_2_ug{}".format(ug.id)
                    ]
                )
                ug.condicionador_temperatura_mancal_la_escora_1.valor_base = float(
                    parametros["temperatura_alerta_mancal_la_escora_1_ug{}".format(ug.id)]
                )
                ug.condicionador_temperatura_mancal_la_escora_2.valor_base = float(
                    parametros["temperatura_alerta_mancal_la_escora_2_ug{}".format(ug.id)]
                )
                ug.condicionador_temperatura_mancal_lna_casquilho.valor_base = float(
                    parametros["temperatura_alerta_mancal_lna_casquilho_ug{}".format(ug.id)]
                )
                ug.condicionador_temperatura_enrolamento_fase_r.valor_limite = float(
                    parametros["temperatura_limite_enrolamento_fase_r_ug{}".format(ug.id)]
                )
                ug.condicionador_temperatura_enrolamento_fase_s.valor_limite = float(
                    parametros["temperatura_limite_enrolamento_fase_s_ug{}".format(ug.id)]
                )
                ug.condicionador_temperatura_enrolamento_fase_t.valor_limite = float(
                    parametros["temperatura_limite_enrolamento_fase_t_ug{}".format(ug.id)]
                )
                ug.condicionador_temperatura_mancal_la_casquilho.valor_limite = float(
                    parametros["temperatura_limite_mancal_la_casquilho_ug{}".format(ug.id)]
                )
                ug.condicionador_temperatura_mancal_la_contra_escora_1.valor_limite = float(
                    parametros[
                        "temperatura_limite_mancal_la_contra_escora_1_ug{}".format(ug.id)
                    ]
                )
                ug.condicionador_temperatura_mancal_la_contra_escora_2.valor_limite = float(
                    parametros[
                        "temperatura_limite_mancal_la_contra_escora_2_ug{}".format(ug.id)
                    ]
                )
                ug.condicionador_temperatura_mancal_la_escora_1.valor_limite = float(
                    parametros["temperatura_limite_mancal_la_escora_1_ug{}".format(ug.id)]
                )
                ug.condicionador_temperatura_mancal_la_escora_2.valor_limite = float(
                    parametros["temperatura_limite_mancal_la_escora_2_ug{}".format(ug.id)]
                )
                ug.condicionador_temperatura_mancal_lna_casquilho.valor_limite = float(
                    parametros["temperatura_limite_mancal_lna_casquilho_ug{}".format(ug.id)]
                )
                """
            except KeyError as e:
                logger.exception(e)

        # nv_minimo
        self.cfg["nv_minimo"] = float(parametros["nv_minimo"])

        # Modo autonomo
        logger.debug(
            "Modo autonomo que o banco respondeu: {}".format(
                int(parametros["modo_autonomo"])
            )
        )
        self.modo_autonomo = int(parametros["modo_autonomo"])
        # Modo de prioridade UGS
        if not self.modo_de_escolha_das_ugs == int(
            parametros["modo_de_escolha_das_ugs"]
        ):
            self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
            logger.info(
                "O modo de prioridade das ugs foi alterado (#{}).".format(
                    self.modo_de_escolha_das_ugs
                )
            )

        
        # Parametros banco
        self.cfg["nv_alvo"] = float(parametros["nv_alvo"])
        self.cfg["kp"] = float(parametros["kp"])
        self.cfg["ki"] = float(parametros["ki"])
        self.cfg["kd"] = float(parametros["kd"])
        self.cfg["kie"] = float(parametros["kie"])

        # Le o databank interno

        if DataBank.get_words(self.cfg["REG_MOA_IN_EMERG"])[0] != 0:
            self.avisado_em_eletrica = True
        else:
            self.avisado_em_eletrica = False

        if DataBank.get_words(self.cfg["REG_MOA_IN_HABILITA_AUTO"])[0] == 1:
            DataBank.set_words(self.cfg["REG_MOA_IN_HABILITA_AUTO"], [0])
            DataBank.set_words(self.cfg["REG_MOA_IN_DESABILITA_AUTO"], [0])
            self.modo_autonomo = 1

        if (
            DataBank.get_words(self.cfg["REG_MOA_IN_DESABILITA_AUTO"])[0] == 1
            or self.modo_autonomo == 0
        ):
            DataBank.set_words(self.cfg["REG_MOA_IN_HABILITA_AUTO"], [0])
            DataBank.set_words(self.cfg["REG_MOA_IN_DESABILITA_AUTO"], [0])
            self.modo_autonomo = 0
            self.entrar_em_modo_manual()

        self.heartbeat()

    def escrever_valores(self):

        if self.modo_autonomo:
            self.con.desliga_controles_locais()

        # DB
        # Escreve no banco
        # Paulo: mover lógica de escrever no banco para um método em DBService
        valores = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            1 if self.aguardando_reservatorio else 0,
            1 if self.clp_online else 0,
            self.nv_montante,
            self.pot_disp,
            1 if self.ug1.disponivel else 0,
            self.ug1.leitura_potencia.valor,
            self.ug1.setpoint,
            self.ug1.etapa_atual,
            self.ug1.leitura_horimetro.valor,
            1 if self.ug2.disponivel else 0,
            self.ug2.leitura_potencia.valor,
            self.ug2.setpoint,
            self.ug2.etapa_atual,
            self.ug2.leitura_horimetro.valor,
            0,
            self.ug1.leitura_perda_na_grade.valor,
            self.ug2.leitura_perda_na_grade.valor 
        ]

        self.db.update_valores_usina(valores)

    def acionar_emergencia(self):
        self.con.acionar_emergencia()
        self.clp_emergencia_acionada = 1

    def normalizar_emergencia(self):

        logger.info("Normalizando (e verificaçẽos)")

        logger.debug(
            "Ultima tentativa: {}. Tensão na linha: RS {:2.1f}kV ST{:2.1f}kV TR{:2.1f}kV.".format(
                self.ts_ultima_tesntativa_de_normalizacao,
                self.leituras.tensao_rs.valor / 1000,
                self.leituras.tensao_st.valor / 1000,
                self.leituras.tensao_tr.valor / 1000,
            )
        )

        if not (
            self.cfg["TENSAO_LINHA_BAIXA"]
            < self.leituras.tensao_rs.valor
            < self.cfg["TENSAO_LINHA_ALTA"]
            and self.cfg["TENSAO_LINHA_BAIXA"]
            < self.leituras.tensao_st.valor
            < self.cfg["TENSAO_LINHA_ALTA"]
            and self.cfg["TENSAO_LINHA_BAIXA"]
            < self.leituras.tensao_tr.valor
            < self.cfg["TENSAO_LINHA_ALTA"]
        ):
            logger.warn("Tensão na linha fora do limite.")
        elif (
            self.deve_tentar_normalizar
            and (datetime.now() - self.ts_ultima_tesntativa_de_normalizacao).seconds
            >= 60 * self.tentativas_de_normalizar
        ):
            self.tentativas_de_normalizar += 1
            self.ts_ultima_tesntativa_de_normalizacao = datetime.now()
            logger.info("Normalizando a Usina")
            self.con.normalizar_emergencia()
            self.clp_emergencia_acionada = 0
            logger.info("Normalizando no banco")
            self.db.update_remove_emergencia()
            self.db_emergencia_acionada = 0
            return True
        else:
            return False

    def heartbeat(self):

        ts = datetime.now().timestamp()
        try:
            logger.debug("Inserting in db")
            ma = 1 if self.modo_autonomo else 0
            self.db.insert_debug(
                ts,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
                self.ug1.setpoint,
                self.ug1.leitura_potencia.valor,
                self.ug2.setpoint,
                self.ug2.leitura_potencia.valor,
                self.nv_montante_recente,
                self.erro_nv,
                ma,
            )
        except Exception as e:
            pass

        agora = datetime.now()
        ano = int(agora.year)
        mes = int(agora.month)
        dia = int(agora.day)
        hor = int(agora.hour)
        mnt = int(agora.minute)
        seg = int(agora.second)
        mil = int(agora.microsecond / 1000)
        DataBank.set_words(0, [ano, mes, dia, hor, mnt, seg, mil])
        DataBank.set_words(self.cfg["REG_MOA_OUT_STATUS"], [self.state_moa])
        DataBank.set_words(self.cfg["REG_MOA_OUT_MODE"], [self.modo_autonomo])
        if self.modo_autonomo:
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_EMERG"],
                [1 if self.clp_emergencia_acionada else 0],
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_TARGET_LEVEL"], [self.cfg["nv_alvo"] - 620] * 1000
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_SETPOINT"],
                [self.ug1.setpoint + self.ug2.setpoint + self.ug3.setpoint],
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_BLOCK_UG1"],
                [1 if self.ug1.enviar_trip_eletrico else 0]
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_BLOCK_UG2"],
                [1 if self.ug2.enviar_trip_eletrico else 0]
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_BLOCK_UG3"],
                [1 if self.ug3.enviar_trip_eletrico else 0]
            )

        else:
            DataBank.set_words(self.cfg["REG_MOA_OUT_EMERG"], [0])
            DataBank.set_words(self.cfg["REG_MOA_OUT_TARGET_LEVEL"], [0])
            DataBank.set_words(self.cfg["REG_MOA_OUT_SETPOINT"], [0])
            DataBank.set_words(self.cfg["REG_MOA_OUT_BLOCK_UG1"], [0])
            DataBank.set_words(self.cfg["REG_MOA_OUT_BLOCK_UG2"], [0])
            DataBank.set_words(self.cfg["REG_MOA_OUT_BLOCK_UG3"], [0])

    def get_agendamentos_pendentes(self):
        """
        Retorna os agendamentos pendentes para a usina.
        :return: list[] agendamentos

        agora = datetime.now()
        agora = agora - timedelta(seconds=agora.second, microseconds=agora.microsecond)
        """
        agendamentos_pendentes = []
        agendamentos = self.db.get_agendamentos_pendentes()
        for agendamento in agendamentos:
            ag = list(agendamento)
            # ag -> [id, data, observacao, comando_id, executado, campo_auxiliar, criado_por, modificado_por, ts_criado, ts_modificado]
            ag[1] = ag[1] - timedelta(0, 60 * 60 * 3)
            agendamentos_pendentes.append(ag)
        return agendamentos_pendentes

    def verificar_agendamentos(self):
        """
        Verifica os agendamentos feitos pelo django no banco de dados e lida com eles, executando, etc...
        """
        agora = datetime.now()
        agendamentos = self.get_agendamentos_pendentes()

        logger.debug(agendamentos)

        if len(agendamentos) == 0:
            return True


        self.agendamentos_atrasados = 0
        for agendamento in agendamentos:
            # ag -> [id, data, observacao, comando_id, executado, campo_auxiliar, criado_por, modificado_por, ts_criado, ts_modificado]
            if agora > agendamento[1]:
                segundos_adiantados = 0
                segundos_passados = (agora - agendamento[1]).seconds
                logger.debug(segundos_passados)
            else:
                segundos_adiantados = (agendamento[1] - agora).seconds
                segundos_passados = 0
            
            if segundos_passados > 60:
                logger.warning(
                    "Agendamento #{} Atrasado! ({}).".format(
                        agendamento[0], agendamento[3]
                    )
                )
                self.agendamentos_atrasados += 1

            if segundos_passados > 300 or self.agendamentos_atrasados > 3:
                logger.info(
                    "Os agendamentos estão muito atrasados! Acionando emergência."
                )
                self.acionar_emergencia()
                return False

            if segundos_adiantados <= 60 and not bool(agendamento[4]):
                # Está na hora e ainda não foi executado. Executar!
                logger.info(
                    "Executando gendamento #{} - {}.".format(
                        agendamento[0], agendamento
                    )
                )

                # se o MOA estiver em autonomo e o agendamento não for executavel em autonomo
                #   marca como executado e altera a descricao
                #   proximo
                if self.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_autmoatico"]:
                    obs = "Este agendamento não tem efeito com o módulo em modo autônomo. Executado sem realizar nenhuma ação"
                    logger.warning(obs)
                    self.db.update_agendamento(agendamento[0], True, obs)
                    return True
            
                # se o MOA estiver em manual e o agendamento não for executavel em manual
                #   marca como executado e altera a descricao
                #   proximo
                if not self.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_manual"]:
                    obs = "Este agendamento não tem efeito com o módulo em modo manual. Executado sem realizar nenhuma ação"
                    logger.warning(obs)
                    self.db.update_agendamento(agendamento[0], True, obs)
                    return True
            

                # Exemplo Case agendamento:
                if agendamento[3] == AGENDAMENTO_DISPARAR_MENSAGEM_TESTE:
                    # Coloca em emergência
                    logger.info("Disparando mensagem teste (comando via agendamento).")
                    self.disparar_mensagem_teste()

                if agendamento[3] == AGENDAMENTO_INDISPONIBILIZAR:
                    # Coloca em emergência
                    logger.info("Indisponibilizando a usina (comando via agendamento).")
                    for ug in self.ugs:
                        ug.forcar_estado_indisponivel()
                    while (
                        not self.ugs[0].etapa_atual == UNIDADE_PARADA
                        and not self.ugs[1].etapa_atual == UNIDADE_PARADA
                    ):
                        self.ler_valores()
                        logger.debug(
                            "Indisponibilizando Usina... \n(freezing for 10 seconds)"
                        )
                        sleep(10)
                    self.acionar_emergencia()
                    logger.info(
                        "Emergência pressionada após indizponibilização agendada mudando para modo manual para evitar normalização automática."
                    )
                    self.entrar_em_modo_manual()

                if agendamento[3] == AGENDAMENTO_ALTERAR_NV_ALVO:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                    except Exception as e:
                        logger.info(
                            "Valor inválido no comando #{} ({} é inválido).".format(
                                agendamento[0], agendamento[3]
                            )
                        )
                    self.cfg["nv_alvo"] = novo
                    pars = [
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        self.cfg["kp"],
                        self.cfg["ki"],
                        self.cfg["kd"],
                        self.cfg["kie"],
                        0, #self.n_movel_l,
                        0, #self.n_movel_r,
                        self.cfg["nv_alvo"],
                    ]
                    self.db.update_parametros_usina(pars)
                    self.escrever_valores()

                if agendamento[3] == AGENDAMENTO_UG1_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg['pot_maxima_ug1'] = novo
                        self.ug1.pot_disponivel = novo
                    except Exception as e:
                        logger.info(
                            "Valor inválido no comando #{} ({} é inválido).".format(
                                agendamento[0], agendamento[3]
                            )
                        )

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_MANUAL:
                    self.ug1.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_DISPONIVEL:
                    self.ug1.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug1.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_RESTRITO:
                    self.ug1.forcar_estado_restrito()

                if agendamento[3] == AGENDAMENTO_UG2_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg['pot_maxima_ug2'] = novo
                        self.ug2.pot_disponivel = novo
                    except Exception as e:
                        logger.info(
                            "Valor inválido no comando #{} ({} é inválido).".format(
                                agendamento[0], agendamento[3]
                            )
                        )

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_MANUAL:
                    self.ug2.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_DISPONIVEL:
                    self.ug2.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug2.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_RESTRITO:
                    self.ug2.forcar_estado_restrito()

                if agendamento[3] == AGENDAMENTO_UG3_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg['pot_maxima_ug3'] = novo
                        self.ug3.pot_disponivel = novo
                    except Exception as e:
                        logger.info(
                            "Valor inválido no comando #{} ({} é inválido).".format(
                                agendamento[0], agendamento[3]
                            )
                        )

                if agendamento[3] == AGENDAMENTO_UG3_FORCAR_ESTADO_MANUAL:
                    self.ug3.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG3_FORCAR_ESTADO_DISPONIVEL:
                    self.ug3.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG3_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug3.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG3_FORCAR_ESTADO_RESTRITO:
                    self.ug3.forcar_estado_restrito()


                # Após executar, indicar no banco de dados
                self.db.update_agendamento(int(agendamento[0]), 1)
                logger.info(
                    "O comando #{} - {} foi executado.".format(
                        agendamento[0], agendamento[5]
                    )
                )
                self.con.somente_reconhecer_emergencia()
                self.escrever_valores()

    def distribuir_potencia(self, pot_alvo):

        if pot_alvo < 0.1:
            for ug in self.ugs:
                ug.setpoint = 0
            return 0

        if self.leituras.potencia_ativa_kW.valor > self.cfg["pot_maxima_alvo"] * 0.95:
            pot_alvo = pot_alvo / (self.leituras.potencia_ativa_kW.valor/self.cfg["pot_maxima_alvo"])

        ugs = self.lista_de_ugs_disponiveis()
        self.pot_disp = 0
        logger.debug("lista_de_ugs_disponiveis:")
        for ug in ugs:
            logger.debug("UG{}".format(ug.id))
            self.pot_disp += ug.cfg['pot_maxima_ug{}'.format(ugs[0].id)]

        if ugs is None:
            return False
        elif len(ugs) == 0:
            return False
        else:
            
            logger.debug("Distribuindo {}".format(pot_alvo))

            sp = pot_alvo/self.cfg["pot_maxima_usina"] 

            self.__split1 = True if sp > (0.133 + self.cfg["margem_pot_critica"]) else self.__split1
            self.__split2 = True if sp > (0.333 + self.cfg["margem_pot_critica"]) and ugs[0].etapa_atual == UNIDADE_SINCRONIZADA else self.__split2
            self.__split3 = True if sp > (0.666 + self.cfg["margem_pot_critica"]) and ugs[0].etapa_atual == UNIDADE_SINCRONIZADA and ugs[1].etapa_atual == UNIDADE_SINCRONIZADA else self.__split3
            
            self.__split3 = False if sp < (0.666) else self.__split3
            self.__split2 = False if sp < (0.333) else self.__split2       
            self.__split1 = False if sp < (0.133) else self.__split1

            logger.debug(f"Sp {sp}")

            if self.__split3:
                logger.debug("Split 3")
                ugs[0].setpoint = (
                    sp * ugs[0].setpoint_maximo
                )
                ugs[1].setpoint = (
                    sp * ugs[1].setpoint_maximo
                )
                ugs[2].setpoint = (
                    sp * ugs[2].setpoint_maximo
                )

            elif self.__split2:
                logger.debug("Split 2")
                sp = sp * 3 / 2
                ugs[0].setpoint = (
                    sp * ugs[0].setpoint_maximo
                )
                ugs[1].setpoint = (
                    sp * ugs[1].setpoint_maximo
                )
                ugs[2].setpoint = 0

            elif self.__split1:
                logger.debug("Split 1")
                sp = sp * 3 / 1
                ugs[0].setpoint = (
                    sp * ugs[0].setpoint_maximo
                )
                ugs[1].setpoint = 0
                ugs[2].setpoint = 0
            else:
                ugs[0].setpoint = 0
                ugs[1].setpoint = 0
                ugs[2].setpoint = 0

            """
            

            if 0.1 < pot_alvo < self.cfg["pot_minima"]:
                logger.debug("0.1 < {} < self.cfg['pot_minima']".format(pot_alvo))
                if len(ugs) > 0:
                    ugs[0].setpoint = self.cfg["pot_minima"]
                    for ug in ugs[1:]:
                        ug.setpoint = 0
            else:
                pot_alvo = min(pot_alvo, self.pot_disp)

                if len(ugs) == 0:
                    return False                    

                if (self.ug1.etapa_atual == UNIDADE_SINCRONIZADA
                    and self.ug2.etapa_atual == UNIDADE_SINCRONIZADA
                    and pot_alvo > (self.cfg["pot_maxima_ug"] - self.cfg["margem_pot_critica"])):
                    logger.debug("Dividindo igualmente entre as UGs")
                    logger.debug("self.cfg[margem_pot_critica] = {}".format( self.cfg["margem_pot_critica"]))
                    for ug in ugs:
                        ug.setpoint = max(self.cfg["pot_minima"], pot_alvo / len(ugs))

                elif(pot_alvo > (self.cfg["pot_maxima_ug"] + self.cfg["margem_pot_critica"])):
                    #logger.debug("Dividindo desigualmente entre UGs pois está partindo uma ou mais UGs")
                    #ugs[0].setpoint = self.cfg["pot_maxima_ug"]
                    logger.debug("Dividindo igualmente entre UGs pois está partindo uma ou mais UGs")
                    for ug in ugs[0:]:
                        ug.setpoint = max(self.cfg["pot_minima"], pot_alvo / len(ugs))

                else:
                    logger.debug("Apenas uma UG deve estar sincronizada")
                    pot_alvo = min(pot_alvo, self.cfg["pot_maxima_ug"])
                    ugs[0].setpoint = max(self.cfg["pot_minima"], pot_alvo)
                    for ug in ugs[1:]:
                        ug.setpoint = 0
            """

            for ug in self.ugs:
                logger.debug("UG{} SP:{}".format(ug.id, ug.setpoint))
    
        return pot_alvo

    def lista_de_ugs_disponiveis(self):
        """
        Retorn uma lista de ugs disponiveis conforme a ordenação selecionada
        """
        ls = []
        for ug in self.ugs:
            if ug.disponivel:
                ls.append(ug)

        if self.modo_de_escolha_das_ugs == MODO_ESCOLHA_MANUAL:
            # escolher por maior prioridade primeiro
            ls = sorted(
                ls,
                key=lambda y: (
                    -1 * y.etapa_atual,
                    -1 * y.etapa_alvo,
                    -1 * y.leitura_potencia.valor,
                    y.prioridade,
                ),
            )
        else:
            # escolher por menor horas_maquina primeiro
            ls = sorted(
                ls,
                key=lambda y: (
                    -1 * y.etapa_atual,
                    -1 * y.etapa_alvo,
                    -1 * y.leitura_potencia.valor,
                    y.leitura_horimetro.valor,
                ),
            )
        return ls

    def controle_normal(self):
        """
        Controle PID
        https://en.wikipedia.org/wiki/PID_controller#Proportional
        """
        logger.debug("-------------------------------------------------")

        # Calcula PID
        logger.debug(
            "Alvo: {:0.3f}, Recente: {:0.3f}".format(
                self.cfg["nv_alvo"], self.nv_montante_recente
            )
        )
        self.controle_p = self.cfg["kp"] * self.erro_nv
        self.controle_i = max(min((self.cfg["ki"] * self.erro_nv) + self.controle_i, 0.8), 0)
        self.controle_d = self.cfg["kd"] * (self.erro_nv - self.erro_nv_anterior)
        saida_pid = (
            self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3)
        )
        logger.debug(
            "PID: {:0.3f} <-- P:{:0.3f} + I:{:0.3f} + D:{:0.3f}; ERRO={}".format(
                saida_pid,
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.erro_nv,
            )
        )

        # Calcula o integrador de estabilidade e limita
        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)

        if self.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if self.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        logger.debug("IE: {:0.3f}".format(self.controle_ie))

        # Arredondamento e limitação
        pot_alvo = max(
            min(
                round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5),
                self.cfg["pot_maxima_usina"],
            ),
            self.cfg["pot_minima"],
        )

        logger.debug("Pot alvo: {:0.3f}".format(pot_alvo))
        logger.debug("Nv alvo: {:0.3f}".format(self.cfg["nv_alvo"]))
        ts = datetime.now().timestamp()
        try:
            logger.debug("Inserting in db")
            ma = 1 if self.modo_autonomo else 0
            self.db.insert_debug(
                ts,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
                self.ug1.setpoint,
                self.ug1.leitura_potencia.valor,
                self.ug2.setpoint,
                self.ug2.leitura_potencia.valor,
                self.nv_montante_recente,
                self.erro_nv,
                ma,
            )
        except Exception as e:
            logger.debug(
                "Exception Banco-------------------------------------------------"
            )

        pot_alvo = self.distribuir_potencia(pot_alvo)

    def disparar_mensagem_teste(self):
        logger.debug("Este e um teste!")
        logger.info("Este e um teste!")
        logger.warning("Este e um teste!")
        voip.enviar_voz_teste()

    def entrar_em_modo_manual(self):
        self.modo_autonomo = 0
        self.db.update_modo_manual()


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    https://stackoverflow.com/questions/2953462/pinging-servers-in-python
    """
    ping = False
    for i in range(5):
        ping = ping or (subprocess.call(["ping", "-c", "1", host], stdout=subprocess.PIPE) == 0)
        if not ping:
            sleep(1)
    return ping
