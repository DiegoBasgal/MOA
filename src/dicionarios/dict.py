ips: "dict[str, any]" = {
    "UG1_ip": "192.168.10.110",
    "UG1_porta": 502,

    "RELE_UG1_ip": "192.168.10.111",
    "RELE_UG1_porta": 502,

    "RV_UG1_ip": "192.168.10.112",
    "RV_UG1_porta": 502,

    "UG2_ip": "192.168.10.120",
    "UG2_porta": 502,

    "RELE_UG2_ip": "192.168.10.121",
    "RELE_UG2_porta": 502,

    "RV_UG2_ip": "192.168.10.122",
    "RV_UG2_porta": 502,

    "SA_ip": "192.168.10.109",
    "SA_porta": 502,

    "RELE_SE_ip": "192.168.10.32",
    "RELE_SE_porta": 502,

    "TDA_ip": "192.168.10.105",
    "TDA_porta": 502

    # "UG1_ip": "localhost",
    # "UG1_porta": 502,
    # "UG2_ip": "192.168.10.120",
    # "UG2_porta": 502,
    # "SA_ip": "192.168.10.109",
    # "SA_porta": 502,
    # "TDA_ip": "192.168.10.105",
    # "TDA_porta": 502

    "UG1_ip": "localhost",
    "UG1_porta": 502,
    "UG2_ip": "localhost",
    "UG2_porta": 502,
    "SA_ip": "localhost",
    "SA_porta": 502,
    "TDA_ip": "localhost",
    "TDA_porta": 502
    # "MOA_ip": "172.21.15.95",
    # "MOA_porta": 502
}

# TODO adicionar registradores após sair o mapa modbus e criar mensagens de aviso
voip: "dict[str, list[bool | str]]" = {
    "EMERGENCIA": [False, "Atenção! Houve um acionamento de emergência na PCH Pampeana, por favor analisar a situação. Atenção! Houve um acionamento de emergência na PCH Pampeana, por favor analisar a situação."],

    "": [False, ""],
}
