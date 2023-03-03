USINA_NV_VERTEDOURO = 821
USINA_VAZAO_SANITARIA_COTA = 820.80
USINA_NV_MINIMO_OPERACAO = 820.80
USINA_TENSAO_MINIMA = 34500 * 0.95
USINA_TENSAO_MAXIMA = 34500 * 1.05

POT_MAX = 500
POT_MIN = 0.4 * POT_MAX
ETAPA_UP = 0
ETAPA_UPGM = 1
ETAPA_UVD = 3
ETAPA_UPS = 4
ETAPA_US = 5

UNIDADE_SINCRONIZADA = 1
UNIDADE_PARANDO = 2
UNIDADE_PARADA = 5
UNIDADE_SINCRONIZANDO = 9

TEMPO_TRANS_UP_UPGM = 20
TEMPO_TRANS_UPGM_UVD = 20
TEMPO_TRANS_UVD_UPS = 20
TEMPO_TRANS_UPS_US = 20
TEMPO_TRANS_US_UPS = 20
TEMPO_TRANS_UPS_UVD = 20
TEMPO_TRANS_UVD_UPGM = 20
TEMPO_TRANS_UPGM_UP = 20

DJ = {
      "debug_dj52L_abrir": False,
      "debug_dj52L_reconhece_reset": False,
      "dj52L_fechado": True,
      "debug_dj52L_fechar": False,
      "dj52L_trip": False,
      "dj52L_aberto": False,
      "dj52L_falta_vcc": False,
      "dj52L_inconsistente": False,
      "dj52L_falha_fechamento": False,
      "dj52L_mola_carregada": True,
      "dj52L_condicao_de_fechamento": False,
}

USN = {
   "nv_montante": 821,
   "potencia_kw_se": 0,
   "q_alfuente": 0,
   "q_liquida": 0,
   "q_sanitaria": 0,
   "q_vertimento": 0,
   "tempo_simul": 0,
   "tensao_na_linha": 34500,
   "potencia_kw_mp": 0,
   "potencia_kw_mr": 0,
   "nv_jusante_grade": 0,
   "stop_sim": False,
   "stop_gui": False,
   "trip_condic_ug1": False,
   "trip_condic_ug2": False,
   "trip_condic_usina": False,
   "reset_geral_condic": False,
}

UG = {
      "debug_parar_ug1": False,
      "debug_partir_ug1": False,
      "etapa_alvo_ug1": 0,
      "etapa_atual_ug1": 0,
      "etapa_aux_ug1": 5,
      "flags_ug1": 0,
      "potencia_kw_ug1": 0,
      "q_ug1": 0,
      "reconhece_reset_ug1": False,
      "setpoint_kw_ug1": 0,
      "debug_setpoint_kw_ug1": 0,
      "trip_ug1": False,
      "temperatura_ug1_fase_r": 25,
      "temperatura_ug1_fase_s": 25,
      "temperatura_ug1_fase_t": 25,
      "temperatura_ug1_nucleo_gerador_1": 25,
      "temperatura_ug1_nucleo_gerador_2": 25,
      "temperatura_ug1_nucleo_gerador_3": 25,
      "temperatura_ug1_mancal_casq_rad": 25,
      "temperatura_ug1_mancal_casq_comb": 25,
      "temperatura_ug1_mancal_escora_comb": 25,
      "pressao_caixa_espiral_ug1": 16.2,

      "debug_parar_ug2": False,
      "debug_partir_ug2": False,
      "etapa_alvo_ug2": 0,
      "etapa_atual_ug2": 0,
      "etapa_aux_ug2": 5,
      "flags_ug2": 0,
      "potencia_kw_ug2": 0,
      "q_ug2": 0,
      "reconhece_reset_ug2": False,
      "setpoint_kw_ug2": 0,
      "debug_setpoint_kw_ug2": 0,
      "trip_ug2": False,
      "temperatura_ug2_fase_r": 25,
      "temperatura_ug2_fase_s": 25,
      "temperatura_ug2_fase_t": 25,
      "temperatura_ug2_nucleo_gerador_1": 25,
      "temperatura_ug2_nucleo_gerador_2": 25,
      "temperatura_ug2_nucleo_gerador_3": 25,
      "temperatura_ug2_mancal_casq_rad": 25,
      "temperatura_ug2_mancal_casq_comb": 25,
      "temperatura_ug2_mancal_escora_comb": 25,
      "pressao_caixa_espiral_ug2": 16.2,
}

GUI = {
    "trip_condic_usina": False,
    "trip_condic_ug1": False,
    "trip_condic_ug2": False,
    "set_press_cx_espiral_ug1": False,
    "set_press_cx_espiral_ug2": False,
}

BORDA = {
    "db_condic": False,
    "usn_condic": False,
    "ug1_condic": False,
    "ug2_condic": False,
}