dct_sa = {
    # VARIÁVEIS
    "condicionadores": [],
    "condicionadores_essenciais": [],
    "condicionadores_ativos": [],
}

dct_se = {
    # LEITURAS MB
    "tensao_r": None,
    "tensao_s": None,
    "tensao_t": None,
    "medidor_usina": None,

    "dj_linha": None,

    # VARIÁVEIS
    "status_tensao": 0,

    "condicionadores": [],
    "condicionadores_essenciais": [],
    "condicionadores_ativos": [],
}

dct_tda = {
    # LEITURAS MB
    "nivel_montante": None,

    # VARIÁVEIS
    "erro_nivel": 0.0,
    "erro_nivel_anterior": 0.0,
    "nivel_montante_anterior": 0.0,

    "aguardando_nv": False,

    "condicionadores": [],
    "condicionadores_essenciais": [],
    "condicionadores_ativos": [],
}

dct_usn = {
    # INSTÂNCIAS
    "BD": None,
    "AGN": None,
    "CFG": None,

    # VARIÁVEIS
    "pid_inicial": -1,
    "pot_alvo_anterior": -1,

    "tentativas_normalizar": 0,

    "pot_disp": 0,
    "estado_moa": 0,
    "ug_operando": 0,
    "modo_prioridade_ugs": 0,

    "controle_p": 0.0,
    "controle_i": 0.0,
    "controle_d": 0.0,
    "controle_ie": 0.0,

    "split1": False,
    "split2": False,
    "split3": False,
    "split4": False,

    "modo_autonomo": False,

    "bd_emergencia": False,
    "clp_emergencia": False,
    "borda_emergencia": False,

    "normalizar_forcado": False,
}

dct_ad = {
    # INSTÂNCIAS
    "Comporta1": None,
    "Comporta2": None,

    # VARIÁVEIS
    "condicionadores": [],
    "condicionadores_essenciais": [],
    "condicionadores_ativos": [],

    # COMPORTAS
    "CP1": {
        # LEITURAS MB
        "manual": None,
        "posicao": None,

        # VARIÁVEIS
        "k": 1000,
        "estado": 0,
        "setpoint": 0,
        "setpoint_maximo": 0,
        "setpoint_anterior": 0,

        "controle_p": 0.0,
        "controle_i": 0.0,
    },
    "CP2": {
        # LEITURAS MB
        "manual": None,
        "posicao": None,

        # VARIÁVEIS
        "k": 1000,
        "estado": 0,
        "setpoint": 0,
        "setpoint_maximo": 0,
        "setpoint_anterior": 0,

        "controle_p": 0.0,
        "controle_i": 0.0,
    },
}

dct_ug = {
    "UG1": {
        # LEITURAS MB
        "potencia": None,
        "horimetro": None,
        "etapa_alvo": None,
        "etapa_atual": None,
        "posicao_distribuidor": None,

        "uhta": {
            "UHTA01": None,
            "UHTA02": None,
        },

        # VARIÁVEIS
        "next_state": None,
        "ts_auxiliar": None,
        "aux_tempo_sincronizada": 0,

        "setpoint": 0,
        "setpoint_maximo": 0,
        "setpoint_minimo": 0,
        "amostras_sp_mppt": 2,
        "amostras_pot_mppt": 5,

        "prioridade": 0,
        "codigo_state": 0,

        "tempo_normalizar": 0,
        "tempo_entre_tentativas": 0,
        "tentativas_normalizacao": 0,
        "limite_tentativas_normalizacao": 3,

        "pot_alvo_usina": 0.0,
        "pos_dist_anterior": 0.0,

        "manter_unidade": False,
        "operar_comporta": False,
        "borda_cp_fechar": False,
        "temporizar_partida": False,
        "aguardar_pressao_cp": False,
        "normalizacao_agendada": False,
        "temporizar_normalizacao": False,

        "potencias_anteriores": [],
        "setpoints_anteriores": [],

        "condicionadores": [],
        "condicionadores_essenciais": [],
        "condicionadores_atenuadores": [],
        "condicionadores_ativos": [],
    },
    "UG2": {
        # LEITURAS MB
        "potencia": None,
        "horimetro": None,
        "etapa_alvo": None,
        "etapa_atual": None,
        "posicao_distribuidor": None,

        "uhta": {
            "UHTA01": None,
            "UHTA02": None,
        },

        # VARIÁVEIS
        "next_state": None,
        "ts_auxiliar": None,
        "aux_tempo_sincronizada": 0,

        "setpoint": 0,
        "setpoint_maximo": 0,
        "setpoint_minimo": 0,
        "amostras_sp_mppt": 2,
        "amostras_pot_mppt": 5,

        "prioridade": 0,
        "codigo_state": 0,

        "tempo_normalizar": 0,
        "tempo_entre_tentativas": 0,
        "tentativas_normalizacao": 0,
        "limite_tentativas_normalizacao": 3,

        "pot_alvo_usina": 0.0,
        "pos_dist_anterior": 0.0,

        "manter_unidade": False,
        "operar_comporta": False,
        "borda_cp_fechar": False,
        "temporizar_partida": False,
        "aguardar_pressao_cp": False,
        "normalizacao_agendada": False,
        "temporizar_normalizacao": False,

        "potencias_anteriores": [],
        "setpoints_anteriores": [],

        "condicionadores": [],
        "condicionadores_essenciais": [],
        "condicionadores_atenuadores": [],
        "condicionadores_ativos": [],
    },
    "UG3": {
        # LEITURAS MB
        "potencia": None,
        "horimetro": None,
        "etapa_alvo": None,
        "etapa_atual": None,
        "posicao_distribuidor": None,

        "uhta": {
            "UHTA01": None,
            "UHTA02": None,
        },

        # VARIÁVEIS
        "next_state": None,
        "ts_auxiliar": None,
        "aux_tempo_sincronizada": 0,

        "setpoint": 0,
        "setpoint_maximo": 0,
        "setpoint_minimo": 0,
        "amostras_sp_mppt": 2,
        "amostras_pot_mppt": 5,

        "prioridade": 0,
        "codigo_state": 0,

        "tempo_normalizar": 0,
        "tempo_entre_tentativas": 0,
        "tentativas_normalizacao": 0,
        "limite_tentativas_normalizacao": 3,

        "pot_alvo_usina": 0.0,
        "pos_dist_anterior": 0.0,

        "manter_unidade": False,
        "operar_comporta": False,
        "borda_cp_fechar": False,
        "temporizar_partida": False,
        "aguardar_pressao_cp": False,
        "normalizacao_agendada": False,
        "temporizar_normalizacao": False,

        "potencias_anteriores": [],
        "setpoints_anteriores": [],

        "condicionadores": [],
        "condicionadores_essenciais": [],
        "condicionadores_atenuadores": [],
        "condicionadores_ativos": [],
    },
    "UG4": {
        # LEITURAS MB
        "potencia": None,
        "horimetro": None,
        "etapa_alvo": None,
        "etapa_atual": None,
        "posicao_distribuidor": None,

        "uhta": {
            "UHTA01": None,
            "UHTA02": None,
        },

        # VARIÁVEIS
        "next_state": None,
        "ts_auxiliar": None,
        "aux_tempo_sincronizada": 0,

        "setpoint": 0,
        "setpoint_maximo": 0,
        "setpoint_minimo": 0,
        "amostras_sp_mppt": 2,
        "amostras_pot_mppt": 5,

        "prioridade": 0,
        "codigo_state": 0,

        "tempo_normalizar": 0,
        "tempo_entre_tentativas": 0,
        "tentativas_normalizacao": 0,
        "limite_tentativas_normalizacao": 3,

        "pot_alvo_usina": 0.0,
        "pos_dist_anterior": 0.0,

        "manter_unidade": False,
        "operar_comporta": False,
        "borda_cp_fechar": False,
        "temporizar_partida": False,
        "aguardar_pressao_cp": False,
        "normalizacao_agendada": False,
        "temporizar_normalizacao": False,

        "potencias_anteriores": [],
        "setpoints_anteriores": [],

        "condicionadores": [],
        "condicionadores_essenciais": [],
        "condicionadores_atenuadores": [],
        "condicionadores_ativos": [],
    },

}