import json
import os
from src.Leituras import *


class LeiturasUSN:

    def __init__(self, cfg):
        self.clp_usina = ModbusClient(
            host=cfg["USN_slave_ip"],
            port=cfg["USN_slave_porta"],
            timeout=30,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )
        self.clp_tda = ModbusClient(
            host=cfg["TDA_slave_ip"],
            port=cfg["TDA_slave_porta"],
            timeout=30,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )

        self.nv_montante = LeituraModbus(
            "REG_TDA_EntradasAnalogicas_MRR_NivelMaisCasasAntes",
            self.clp_tda,
            REG_TDA_NivelMaisCasasAntes,
            1 / 10000,
            400,
            op=4
        )
        self.potencia_ativa_kW = LeituraModbus(
            "REG_SA_RetornosAnalogicos_MWR_PM_810_Potencia_Ativa",
            self.clp_usina,
            REG_SA_RetornosAnalogicos_MWR_PM_810_Potencia_Ativa,
            op=4,
        )
        self.tensao_rs = LeituraModbus(
            "REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_AB",
            self.clp_usina,
            REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_AB,
            100,
            op=4,
        )
        self.tensao_st = LeituraModbus(
            "REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_BC",
            self.clp_usina,
            REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_BC,
            100,
            op=4,
        )
        self.tensao_tr = LeituraModbus(
            "REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_CA",
            self.clp_usina,
            REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_CA,
            100,
            op=4,
        )
