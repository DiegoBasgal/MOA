ips: "dict[str, any]" = {
    "SA_ip": "192.168.68.22",
    "SA_porta": 502,
    "AD_ip": "192.168.68.30",
    "AD_porta": 502,
    "TDA_ip": "192.168.68.29",
    "TDA_porta": 502,
    "UG1_ip": "192.168.68.10",
    "UG1_porta": 502,
    "UG2_ip": "192.168.68.13",
    "UG2_porta": 502,
    "UG3_ip": "192.168.68.16",
    "UG3_porta": 502,
    "UG4_ip": "192.168.68.19",
    "UG4_porta": 502,
    "MOA_ip": "0.0.0.0",
    "MOA_porta": 5000,
}

voip: "dict[str, list[bool | str]]" = {
    "EMERGENCIA" : [False, 0, "Atenção! Houve um acionamento de emergência na PCH Xavantina, por favor analisar a situação. Atenção! Houve um acionamento de emergência na PCH Xavantina, por favor analisar a situação."],
}

watchdog: "dict[str, any]" = {
    "unit_id": 1,
    "ip_slave": "172.21.15.12",
    "port_slave": 5000,
    "timeout_modbus": 5,
    "timeout_moa": 30,
    "nome_usina": "Simul",
    "nome_local": "NOME DO LOCAL QUE ESTA CONECTANDO"
}