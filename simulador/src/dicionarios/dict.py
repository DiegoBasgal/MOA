shared_dict = {
    "GLB": {
        "tempo_simul": 0,

        "stop_sim": False,
        "stop_gui": False
    },

    "USN": {
        "q_liquida": 0,
        "q_alfuente": 0,
        "q_sanitaria": 0,
        "q_vertimento": 0,
        "nv_montante": 821,
        "nv_jusante_grade": 0,

        "potencia_kw_se": 0,
        "potencia_kw_mp": 0,
        "potencia_kw_mr": 0,
        "tensao_na_linha": 34500,

        "trip_condic_usina": False,
        "reset_geral_condic": False
    },

    "DJ": {
        "dj52L_trip": False,
        "dj52L_aberto": False,
        "dj52L_fechado": True,
        "dj52L_falta_vcc": False,
        "dj52L_inconsistente": False,
        "dj52L_mola_carregada": True,
        "dj52L_falha_fechamento": False,
        "dj52L_condicao_de_fechamento": False,

        "debug_dj52L_abrir": False,
        "debug_dj52L_fechar": False,
        "debug_dj52L_reconhece_reset": False
    },

    "UG": {
        "q_ug1": 0,
        "flags_ug1": 0,
        "etapa_aux_ug1": 5,
        "etapa_alvo_ug1": 0,
        "etapa_atual_ug1": 0,
        "potencia_kw_ug1": 0,
        "setpoint_kw_ug1": 0,
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

        "q_ug2": 0,
        "flags_ug2": 0,
        "etapa_aux_ug2": 5,
        "etapa_alvo_ug2": 0,
        "etapa_atual_ug2": 0,
        "potencia_kw_ug2": 0,
        "setpoint_kw_ug2": 0,
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

        "trip_ug1": False,
        "trip_ug2": False,
        "trip_condic_ug1": False,
        "trip_condic_ug2": False,
        "reconhece_reset_ug1": False,
        "reconhece_reset_ug2": False,
        "set_press_cx_espiral_ug1": False,
        "set_press_cx_espiral_ug2": False,

        "debug_setpoint_kw_ug1": 0,
        "debug_setpoint_kw_ug2": 0,

        "debug_parar_ug1": False,
        "debug_partir_ug1": False,
        "debug_parar_ug2": False,
        "debug_partir_ug2": False
    },

    "BORDA": {
        "usn_condic": False,
        "ug1_condic": False,
        "ug2_condic": False
    }
}