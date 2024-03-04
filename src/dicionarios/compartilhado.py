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