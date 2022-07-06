import json
import os
from src.Leituras import *


class LeiturasUSN:

    def __init__(self, cfg):
        self.clp_usina = ModbusClient(
            host=cfg["USN_slave_ip"],
            port=cfg["USN_slave_porta"],
            timeout=5,
            unit_id=1,
            auto_open=True,
            auto_close=False,
        )

        self.nv_montante = LeituraModbus(
            "REG_TDA_EntradasAnalogicas_MRR_NivelMaisCasasAntes",
            self.clp_usina,
            REG_TDA_EntradasAnalogicas_MRR_NivelMaisCasasAntes,
            1 / 10000,
            400
        )
        self.potencia_ativa_kW = LeituraModbus(
            "REG_SA_RetornosAnalogicos_MWR_PM_810_Potencia_Ativa",
            self.clp_usina,
            REG_SA_RetornosAnalogicos_MWR_PM_810_Potencia_Ativa,
        )
        self.tensao_rs = LeituraModbus(
            "REG_SA_RetornosAnalogicos_MWR_PM1_710_Tensao_AB",
            self.clp_usina,
            REG_SA_RetornosAnalogicos_MWR_PM1_710_Tensao_AB,
            10,
        )
        self.tensao_st = LeituraModbus(
            "REG_SA_RetornosAnalogicos_MWR_PM1_710_Tensao_BC",
            self.clp_usina,
            REG_SA_RetornosAnalogicos_MWR_PM1_710_Tensao_BC,
            10,
        )
        self.tensao_tr = LeituraModbus(
            "REG_SA_RetornosAnalogicos_MWR_PM1_710_Tensao_CA",
            self.clp_usina,
            REG_SA_RetornosAnalogicos_MWR_PM1_710_Tensao_CA,
            10,
        )
