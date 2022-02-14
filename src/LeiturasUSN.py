import json
import os
from Leituras import *

# carrega as configurações
config_file = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_file, "r") as file:
    cfg = json.load(file)

clp_usina_ip = cfg["UG2_slave_ip"]
clp_usina_port = cfg["UG2_slave_porta"]

clp_usina = ModbusClient(
    host=clp_usina_ip,
    port=clp_usina_port,
    timeout=5,
    unit_id=1,
    auto_open=True,
    auto_close=False,
)

leitura_dj52L_aberto = LeituraModbusBit(
    "Subestacao_Disj52L",
    clp_usina,
    REG_USINA_Subestacao_Disj52L,
    0,
)
leitura_dj52L_fechado = LeituraModbusBit(
    "REG_USINA_Subestacao_Disj52L",
    clp_usina,
    REG_USINA_Subestacao_Disj52L,
    1,
)
leitura_dj52L_inconsistente = LeituraModbusBit(
    "REG_USINA_Subestacao_Disj52L",
    clp_usina,
    REG_USINA_Subestacao_Disj52L,
    2,
)
leitura_dj52L_trip = LeituraModbusBit(
    "REG_USINA_Subestacao_Disj52L",
    clp_usina,
    REG_USINA_Subestacao_Disj52L,
    3,
)
leitura_dj52L_mola_carregada = LeituraModbusBit(
    "REG_USINA_Subestacao_Disj52L",
    clp_usina,
    REG_USINA_Subestacao_Disj52L,
    6,
)
leitura_dj52L_falta_vcc = LeituraModbusBit(
    "REG_USINA_Subestacao_Disj52L",
    clp_usina,
    REG_USINA_Subestacao_Disj52L,
    8,
)
leitura_dj52L_condicao_de_fechamento = LeituraModbusBit(
    "REG_USINA_Subestacao_Disj52L",
    clp_usina,
    REG_USINA_Subestacao_Disj52L,
    9,
)
leitura_dj52L_falha_fechamento = LeituraModbusBit(
    "REG_USINA_Subestacao_Disj52L",
    clp_usina,
    REG_USINA_Subestacao_Disj52L,
    13,
)

leitura_nv_montante = LeituraModbus(
    "REG_USINA_NivelBarragem",
    clp_usina,
    REG_USINA_NivelBarragem,
    1 / 100,
)

leitura_potencia_ativa_kW = LeituraModbus(
    "REG_USINA_Subestacao_PotenciaAtivaMedia",
    clp_usina,
    REG_USINA_Subestacao_PotenciaAtivaMedia,
)

leitura_tensao_rs = LeituraModbus(
    "REG_USINA_Subestacao_TensaoRS",
    clp_usina,
    REG_USINA_Subestacao_TensaoRS,
    10,
)
leitura_tensao_st = LeituraModbus(
    "REG_USINA_Subestacao_TensaoST",
    clp_usina,
    REG_USINA_Subestacao_TensaoST,
    10,
)
leitura_tensao_tr = LeituraModbus(
    "REG_USINA_Subestacao_TensaoTR",
    clp_usina,
    REG_USINA_Subestacao_TensaoTR,
    10,
)

leitura_nv_canal_aducao = LeituraModbus(
    "REG_USINA_NivelCanalAducao",
    clp_usina,
    REG_USINA_NivelCanalAducao,
    1 / 100,
)

leitura_pot_medidor = LeituraModbus(
    "REG_USINA_Subestacao_PotenciaAtivaMedia",
    clp_usina,
    REG_USINA_Subestacao_PotenciaAtivaMedia,
)