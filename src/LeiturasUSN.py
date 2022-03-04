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

        self.dj52L_aberto = LeituraModbusBit(
            "Subestacao_Disj52L",
            self.clp_usina,
            REG_USINA_Subestacao_Disj52L,
            0,
        )
        self.dj52L_fechado = LeituraModbusBit(
            "REG_USINA_Subestacao_Disj52L",
            self.clp_usina,
            REG_USINA_Subestacao_Disj52L,
            1,
        )
        self.dj52L_inconsistente = LeituraModbusBit(
            "REG_USINA_Subestacao_Disj52L",
            self.clp_usina,
            REG_USINA_Subestacao_Disj52L,
            2,
        )
        self.dj52L_trip = LeituraModbusBit(
            "REG_USINA_Subestacao_Disj52L",
            self.clp_usina,
            REG_USINA_Subestacao_Disj52L,
            3,
        )
        self.dj52L_mola_carregada = LeituraModbusBit(
            "REG_USINA_Subestacao_Disj52L",
            self.clp_usina,
            REG_USINA_Subestacao_Disj52L,
            6,
        )
        self.dj52L_falta_vcc = LeituraModbusBit(
            "REG_USINA_Subestacao_Disj52L",
            self.clp_usina,
            REG_USINA_Subestacao_Disj52L,
            8,
        )
        self.dj52L_condicao_de_fechamento = LeituraModbusBit(
            "REG_USINA_Subestacao_Disj52L",
            self.clp_usina,
            REG_USINA_Subestacao_Disj52L,
            9,
        )
        self.dj52L_falha_fechamento = LeituraModbusBit(
            "REG_USINA_Subestacao_Disj52L",
            self.clp_usina,
            REG_USINA_Subestacao_Disj52L,
            13,
        )
        self.nv_montante = LeituraModbus(
            "REG_USINA_NivelBarragem",
            self.clp_usina,
            REG_USINA_NivelBarragem,
            1 / 100,
        )
        self.potencia_ativa_kW = LeituraModbus(
            "REG_USINA_Subestacao_PotenciaAtivaMedia",
            self.clp_usina,
            REG_USINA_Subestacao_PotenciaAtivaMedia,
        )
        self.tensao_rs = LeituraModbus(
            "REG_USINA_Subestacao_TensaoRS",
            self.clp_usina,
            REG_USINA_Subestacao_TensaoRS,
            10,
        )
        self.tensao_st = LeituraModbus(
            "REG_USINA_Subestacao_TensaoST",
            self.clp_usina,
            REG_USINA_Subestacao_TensaoST,
            10,
        )
        self.tensao_tr = LeituraModbus(
            "REG_USINA_Subestacao_TensaoTR",
            self.clp_usina,
            REG_USINA_Subestacao_TensaoTR,
            10,
        )
        self.nv_canal_aducao = LeituraModbus(
            "REG_USINA_NivelCanalAducao",
            self.clp_usina,
            REG_USINA_NivelCanalAducao,
            1 / 100,
        )

    