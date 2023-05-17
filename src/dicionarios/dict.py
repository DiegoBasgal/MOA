ips: "dict[str, any]" = {
    "UG1_slave_ip": "10.101.2.215",
    "UG1_slave_porta": 5003,
    "UG2_slave_ip": "10.101.2.215",
    "UG2_slave_porta": 5003,
    "USN_slave_ip": "10.101.2.215",
    "USN_slave_porta": 5003,
    "TDA_slave_ip": "10.101.2.215",
    "TDA_slave_porta": 5003,
    "MOA_slave_ip": "172.21.15.95",
    "MOA_slave_porta": 502
}

# TODO adicionar registradores após sair o mapa modbus e criar mensagens de aviso
voip: "dict[str, list[bool | str]]" = {
    "EMERGENCIA": [False, "Atenção! Houve um acionamento de emergência na PCH Pampeana, por favor analisar a situação. Atenção! Houve um acionamento de emergência na PCH Pampeana, por favor analisar a situação."],

    "UG1_QCAUGRemoto": [False, "mensagem"],
    "UG1_FreioCmdRemoto": [False, "mensagem"],
    "UG2_QCAUGRemoto": [False, "mensagem"],
    "UG2_FreioCmdRemoto": [False, "mensagem"],

    "TDA_FalhaComum": [False, "mensagem"],
    "BombasDngRemoto": [False, "mensagem"],
    "Disj_GDE_QCAP_Fechado": [False, "mensagem"]
}
