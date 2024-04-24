IP: "dict[str, any]" = {
    # "UG1_ip": "192.168.10.110",
    # "UG1_porta": 502,

    # "RELE_UG1_ip": "192.168.10.111",
    # "RELE_UG1_porta": 502,

    # "RV_UG1_ip": "192.168.10.112",
    # "RV_UG1_porta": 502,

    # "RT_UG1_ip": "192.168.10.112",
    # "RT_UG1_porta": 502,

    # "UG2_ip": "192.168.10.120",
    # "UG2_porta": 502,

    # "RELE_UG2_ip": "192.168.10.121",
    # "RELE_UG2_porta": 502,

    # "RV_UG2_ip": "192.168.10.122",
    # "RV_UG2_porta": 502,

    # "RT_UG2_ip": "192.168.10.122",
    # "RT_UG2_porta": 502,

    # "SA_ip": "192.168.10.109",
    # "SA_porta": 502,

    # "RELE_SE_ip": "192.168.10.32",
    # "RELE_SE_porta": 502,

    # "TDA_ip": "192.168.10.105",
    # "TDA_porta": 502

    "UG1_ip": "10.101.2.215",
    "UG1_porta": 502,

    "RELE_UG1_ip": "10.101.2.215",
    "RELE_UG1_porta": 502,

    "RV_UG1_ip": "10.101.2.215",
    "RV_UG1_porta": 502,

    "RT_UG1_ip": "10.101.2.215",
    "RT_UG1_porta": 502,

    "UG2_ip": "10.101.2.215",
    "UG2_porta": 502,

    "RELE_UG2_ip": "10.101.2.215",
    "RELE_UG2_porta": 502,

    "RV_UG2_ip": "10.101.2.215",
    "RV_UG2_porta": 502,

    "RT_UG2_ip": "10.101.2.215",
    "RT_UG2_porta": 502,

    "SA_ip": "10.101.2.215",
    "SA_porta": 502,

    "RELE_SE_ip": "10.101.2.215",
    "RELE_SE_porta": 502,

    "TDA_ip": "10.101.2.215",
    "TDA_porta": 502,

    "MOA_ip": "0.0.0.0",
    "MOA_porta": 502,
}

# TODO adicionar registradores após sair o mapa modbus e criar mensagens de aviso
voip: "dict[str, list[bool | str]]" = {
    "EMERGENCIA": [False, "Atenção! Houve um acionamento de emergência na PCH Pampeana, por favor analisar a situação. Atenção! Houve um acionamento de emergência na PCH Pampeana, por favor analisar a situação."],
    "WATCHDOG": [False, "Atenção! Houve um erro com a verificação do Watchdog na PCH Pampeana! Falha na verificação por Banco de Dados e CLP do MOA, favor verificar."],

    # SA
    "SA_L_TESTE_VOIP": [False, 0, "Leitura Teste Voip do Serviço Auxiliar Ativada"],
    "SE_L_TESTE_VOIP": [False, 0, "Leitura Teste Voip da Subestação Ativada"],
    "TDA_L_TESTE_VOIP": [False, 0, "Leitura Teste Voip da Tomada da Água Ativada"],
    "UG1_L_TESTE_VOIP": [False, 0, "Leitura Teste Voip da Unidade de Geração 1 Ativada"],
    "UG2_L_TESTE_VOIP": [False, 0, "Leitura Teste Voip da Unidade de Geração 2 Ativada"],
}