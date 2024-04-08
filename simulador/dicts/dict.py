compartilhado = {
    "GLB": {
        "tempo_real": 0,
        "tempo_simul": 0,

        "passo_afluente": 0,

        "stop_sim": False,
        "stop_gui": False
    },

    "BRD": {
        # GERAL
        "condic": False,
        "sa_condic": False,
        "se_condic": False,
        "ad_condic": False,
        "tda_condic": False,
        "ug1_condic": False,
        "ug2_condic": False,
        "ug3_condic": False,
        "ug4_condic": False,

        # SE
        "djse_trip": False,
        "djse_mola": False,
        "djse_fechado": False,
        "djse_condicao": False,

        # TDA
        "uh1_disponivel": False,
        "uh2_disponivel": False,

        # AD
        "uhcd_disponivel": True,
        "cp1ad_manual": False,
        "cp2ad_manual": False,
    },

    "USN": {
        "trip_condic": False,
    },

    "TDA": {
        "condic": False,

        "q_liquida": 0,
        "q_alfuente": 0,
        "q_sanitaria": 0,
        "q_vertimento": 0,
        "q_atual_vert": 0,
        "q_liq_vert": 0,

        "nv_montante": 818.9,
        "nv_jusante_grade": 0,

        "cp1_posicao": 0,
        "cp2_posicao": 0,
        "cp3_posicao": 0,
        "cp4_posicao": 0,

        "uh1_disponivel": True,
        "uh2_disponivel": True,

        "cp1_aberta": False,
        "cp1_fechada": True,

        "cp2_aberta": False,
        "cp2_fechada": True,

        "cp3_aberta": False,
        "cp3_fechada": True,

        "cp4_aberta": False,
        "cp4_fechada": True,
    },

    "AD": {
        "condic": False,

        "cp1_q": 0,
        "cp1_setpoint": 0,

        "cp1_manual": False,
        "cp1_buscar": False,

        "cp2_q": 0,
        "cp2_setpoint": 0,

        "cp2_manual": False,
        "cp2_buscar": False,

        "uhcd_disponivel": True,

    },

    "SE": {
        "condic": False,

        "potencia_se": 0,

        "tensao_rs": 138000,
        "tensao_st": 138000,
        "tensao_tr": 138000,

        "dj_trip": False,
        "dj_falha": False,
        "dj_aberto": True,
        "dj_fechado": False,
        "dj_condicao": False,
        "dj_falta_vcc": False,
        "dj_inconsistente": False,
        "dj_mola_carregada": True,

        "debug_dj_reset": False,
        "debug_dj_abrir": False,
        "debug_dj_fechar": False,
    },

    "UG1": {
        "condic": False,

        "q": 1,
        "potencia": 0,
        "setpoint": 0,
        "etapa_alvo": 0,
        "etapa_atual": 0,
        "debug_setpoint": 0,
        "posicao_distribuidor": 0,

        "pressao_turbina": 1.5,
        "temp_fase_r": 25,
        "temp_fase_s": 25,
        "temp_fase_t": 25,
        "temp_mancal_gerador_la_1": 25,
        "temp_mancal_gerador_la_2": 25,
        "temp_mancal_gerador_lna_1": 25,
        "temp_mancal_gerador_lna_2": 25,
        "temp_mancal_turbina_radial": 25,
        "temp_mancal_turbina_escora": 25,
        "temp_mancal_turbina_contra_escora": 25,

        "set_pressao": False,

        "debug_parar": False,
        "debug_partir": False,
    },

    "UG2": {
        "condic": False,

        "q": 1,
        "potencia": 0,
        "setpoint": 0,
        "etapa_alvo": 0,
        "etapa_atual": 0,
        "debug_setpoint": 0,
        "posicao_distribuidor": 0,

        "pressao_turbina": 1.5,
        "temp_fase_r": 25,
        "temp_fase_s": 25,
        "temp_fase_t": 25,
        "temp_mancal_gerador_la_1": 25,
        "temp_mancal_gerador_la_2": 25,
        "temp_mancal_gerador_lna_1": 25,
        "temp_mancal_gerador_lna_2": 25,
        "temp_mancal_turbina_radial": 25,
        "temp_mancal_turbina_escora": 25,
        "temp_mancal_turbina_contra_escora": 25,

        "set_pressao": False,

        "debug_parar": False,
        "debug_partir": False,
    },

    "UG3": {
        "condic": False,

        "q": 1,
        "potencia": 0,
        "setpoint": 0,
        "etapa_alvo": 0,
        "etapa_atual": 0,
        "debug_setpoint": 0,
        "posicao_distribuidor": 0,

        "pressao_turbina": 1.5,
        "temp_fase_r": 25,
        "temp_fase_s": 25,
        "temp_fase_t": 25,
        "temp_mancal_gerador_la_1": 25,
        "temp_mancal_gerador_la_2": 25,
        "temp_mancal_gerador_lna_1": 25,
        "temp_mancal_gerador_lna_2": 25,
        "temp_mancal_turbina_radial": 25,
        "temp_mancal_turbina_escora": 25,
        "temp_mancal_turbina_contra_escora": 25,

        "set_pressao": False,

        "debug_parar": False,
        "debug_partir": False,
    },

    "UG4": {
        "condic": False,

        "q": 1,
        "potencia": 0,
        "setpoint": 0,
        "etapa_alvo": 0,
        "etapa_atual": 0,
        "debug_setpoint": 0,
        "posicao_distribuidor": 0,

        "pressao_turbina": 1.5,
        "temp_fase_r": 25,
        "temp_fase_s": 25,
        "temp_fase_t": 25,
        "temp_mancal_gerador_la_1": 25,
        "temp_mancal_gerador_la_2": 25,
        "temp_mancal_gerador_lna_1": 25,
        "temp_mancal_gerador_lna_2": 25,
        "temp_mancal_turbina_radial": 25,
        "temp_mancal_turbina_escora": 25,
        "temp_mancal_turbina_contra_escora": 25,

        "set_pressao": False,

        "debug_parar": False,
        "debug_partir": False,
    },
}