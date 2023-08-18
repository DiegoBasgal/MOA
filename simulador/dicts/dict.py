compartilhado = {
    "GLB": {
        "tempo_real": 0,
        "tempo_simul": 0,

        "stop_sim": False,
        "stop_gui": False
    },

    "BRD": {
        # GERAL
        "condic" : False,

        # TDA
        "lg_operando": False,
        "vb_operando": False,
        "vb_calculo_q": False,
        "uh_disponivel": False,

        # SE
        "djse_trip": False,
        "djse_mola": False,
        "djse_fechado": False,

        # BAY
        "djbay_secc": False,
        "djbay_mola": False,
        "djbay_fechado": False,

        # Comportas
        "cp1_aberta": False,
        "cp1_fechada": False,
        "cp1_cracking": False,
        "cp1_bloqueio": False,
        "cp1_operando": False,
        "cp1_permissao": False,
        "cp1_equalizada": False,
        "cp1_aguardando": False,

        "cp2_aberta": False,
        "cp2_fechada": False,
        "cp2_cracking": False,
        "cp2_bloqueio": False,
        "cp2_operando": False,
        "cp2_permissao": False,
        "cp2_equalizada": False,
        "cp2_aguardando": False,

    },

    "USN": {
        "trip_condic": False,
    },

    "TDA": {
        "q_liquida": 0,
        "q_alfuente": 0,
        "q_sanitaria": 0,
        "q_vertimento": 0,

        "nv_montante": 462.100,
        "nv_jusante_grade": 0,

        "lg_operando": False,
        "vb_operando": False,
        "uh_disponivel": True,
    },

    "SE": {
        "potencia_se": 0,

        "tensao_vab": 22800,
        "tensao_vbc": 22800,
        "tensao_vca": 22800,

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

    "BAY": {
        "potencia_mp": 0,
        "potencia_mr": 0,

        "tensao_vs": 0,
        "tensao_vab": 22800,
        "tensao_vbc": 22800,
        "tensao_vca": 22800,

        "dj_secc": True,
        "dj_trip": False,
        "dj_falha": False,
        "dj_aberto": True,
        "dj_fechado": False,
        "dj_condicao": False,
        "dj_inconsistente": False,
        "dj_mola_carregada": True,

        "debug_dj_reset": False,
        "debug_dj_abrir": False,
        "debug_dj_fechar": False,
    },

    "CP1": {
        "progresso": 0,

        "trip": False,
        "aberta": False,
        "fechada": True,
        "cracking": False,
        "operando": False,
        "permissao": False,
        "equalizada": True,
        "aguardando": False,

        "thread_aberta": False,
        "thread_fechada": False,
        "thread_cracking": False,
        "falha_cracking": False,
    },

    "CP2": {
        "progresso": 0,

        "trip": False,
        "aberta": False,
        "fechada": True,
        "cracking": False,
        "operando": False,
        "permissao": False,
        "equalizada": True,
        "aguardando": False,

        "thread_aberta": False,
        "thread_fechada": False,
        "thread_cracking": False,
        "falha_cracking": False,
    },

    "UG1": {
        "q": 1,
        "potencia": 0,
        "setpoint": 0,
        "etapa_alvo": 0,
        "etapa_atual": 0,
        "debug_setpoint": 0,

        "pressao_turbina": 1.5,
        "temp_fase_r": 25,
        "temp_fase_s": 25,
        "temp_fase_t": 25,
        "temp_mancal_guia": 25,
        "temp_mancal_casq_comb": 25,
        "temp_nucleo_gerador_1": 25,
        "temp_patins_mancal_comb_1": 25,
        "temp_patins_mancal_comb_2": 25,
        "temp_mancal_guia_interno_1": 25,
        "temp_mancal_guia_interno_2": 25,
        "temp_mancal_contra_esc_comb": 25,

        "debug_parar": False,
        "debug_partir": False,
    },

    "UG2": {
        "q": 1,
        "potencia": 0,
        "setpoint": 0,
        "etapa_alvo": 0,
        "etapa_atual": 0,
        "debug_setpoint": 0,

        "pressao_turbina": 1.5,
        "temp_fase_r": 25,
        "temp_fase_s": 25,
        "temp_fase_t": 25,
        "temp_mancal_guia": 25,
        "temp_mancal_casq_comb": 25,
        "temp_nucleo_gerador_1": 25,
        "temp_patins_mancal_comb_1": 25,
        "temp_patins_mancal_comb_2": 25,
        "temp_mancal_guia_interno_1": 25,
        "temp_mancal_guia_interno_2": 25,
        "temp_mancal_contra_esc_comb": 25,

        "debug_parar": False,
        "debug_partir": False,
    },
}