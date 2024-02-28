dct_usn = {
    # INSTÂNCIAS
    "BD": None,
    "AGN": None,
    "CFG": None,

    # PRIVADAS
    "__split1": False,
    "__split2": False,
    "__split3": False,
    "__split4": False,
    
    # PROTEGIDAS
    "_pid_inicial": -1,
    "_pot_alvo_anterior": -1,
    "_tentativas_normalizar": 0,

    "_modo_autonomo": False,

    # PÚBLICAS
    "pot_disp": 0,
    "estado_moa": 0,
    "ug_operando": 0,
    "modo_prioridade_ugs": 0,

    "controle_p": 0.0,
    "controle_i": 0.0,
    "controle_d": 0.0,
    "controle_ie": 0.0,

    "bd_emergencia": False,
    "clp_emergencia": False,
    "borda_emergencia": False,
    "normalizar_forcado": False,
}

dct_tda = {
    "nivel_montante": 0.0,

    "erro_nivel": 0.0,
    "erro_nivel_anterior": 0.0,
    "nivel_montante_anterior": 0.0,

    "aguardando_nv": False,

    "condicionadores": [],
    "condicionadores_essenciais": [],
    "condicionadores_ativos": [],
}