import os
import json
from src.Leituras import *

class LeiturasUSN:
    def __init__(self, cfg):
        self.clp_usina = ModbusClient(host=cfg["USN_slave_ip"], port=cfg["USN_slave_porta"], timeout=0.5, unit_id=1, auto_open=True, auto_close=True,)
        self.clp_tda = ModbusClient(host=cfg["TDA_slave_ip"], port=cfg["TDA_slave_porta"], timeout=0.5, unit_id=1, auto_open=True, auto_close=True,)

        self.nv_montante = LeituraModbus(
            "REG_TDA_EntradasAnalogicas_MRR_NivelMaisCasasAntes",
            self.clp_tda,
            REG_TDA_NivelMaisCasasAntes,
            1 / 10000,
            400,
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

        # usar essa forma de leitura de potencia ativa quando for executar o moa de campo
        
        self.potencia_ativa_kW = LeituraNBRPower(
            "LeituraNBRPower potencia_ativa_kW",
            ip_1=cfg["MP_ip"],
            port_1=cfg["MP_port"],
            ip_2=cfg["MR_ip"],
            port_2=cfg["MR_port"],
            escala=cfg["MPMR_scale"],
        )
        """
        # essa forma de leitura de potencia ativa, deve ser utilizada apenas com o simulador
        self.potencia_ativa_kW = LeituraModbus(
            "REG_SA_RetornosAnalogicos_Medidor_potencia_kw_mp",
            self.clp_usina,
            REG_SA_RetornosAnalogicos_Medidor_potencia_kw_mp,
            1,
            op=4,
        )
        """