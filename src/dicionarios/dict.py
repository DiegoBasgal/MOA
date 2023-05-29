ips: "dict[str, any]" = {
    "UG1_ip": "0.0.0.0",
    "UG1_porta": 5003,
    "UG2_ip": "0.0.0.0",
    "UG2_porta": 5003,
    "USN_ip": "0.0.0.0",
    "USN_porta": 5003
    # "MOA_ip": "172.21.15.95",
    # "MOA_porta": 502
}

# TODO adicionar registradores após sair o mapa modbus e criar mensagens de aviso
voip: "dict[str, list[bool | str]]" = {
    "EMERGENCIA": [False, "Atenção! Houve um acionamento de emergência na PCH Pampeana, por favor analisar a situação. Atenção! Houve um acionamento de emergência na PCH Pampeana, por favor analisar a situação."],

    "": [False, ""],
}
