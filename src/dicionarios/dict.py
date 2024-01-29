ips: "dict[str, any]" = {
    "MP_ip": "10.101.2.215",
    "MP_porta": 502,
    "MR_ip": "10.101.2.215",
    "MR_porta": 502,

    "SA_ip": "10.1",
    "SA_porta": 502,
    "TDA_ip": "10.101.2.215",
    "TDA_porta": 502,
    "UG1_ip": "10.101.2.215",
    "UG1_porta": 502,
    "UG2_ip": "10.101.2.215",
    "UG2_porta": 502,
    "MOA_ip": "10.101.2.215",
    "MOA_porta": 502,

    "RV_UG1_ip": "10.101.2.215",
    "RV_UG1_porta": 502,
    "RV_UG2_ip": "10.101.2.215",
    "RV_UG2_porta": 502,

    "RT_UG1_ip": "10.101.2.215",
    "RT_UG1_porta": 502,
    "RT_UG2_ip": "10.101.2.215",
    "RT_UG2_porta": 502,

    "RELE_SE_ip": "10.101.2.215",
    "RELE_SE_porta": 502,
    "RELE_TE_ip": "10.101.2.215",
    "RELE_TE_porta": 502,
    "RELE_BAY_ip": "10.101.2.215",
    "RELE_BAY_porta": 502,
    "RELE_UG1_ip": "10.101.2.215",
    "RELE_UG1_porta": 502,
    "RELE_UG2_ip": "10.101.2.215",
    "RELE_UG2_porta": 502,
}

voip: "dict[str, list[bool | str]]" = {
    "EMERGENCIA" : [False, 0, "Atenção! Houve um acionamento de emergência na PCH Xavantina, por favor analisar a situação. Atenção! Houve um acionamento de emergência na PCH Xavantina, por favor analisar a situação."],

    "LG_FALHA_ATUADA": [False, 0, "Atenção! Houve uma falha com o Limpa Grades na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com o Limpa Grades na PCH Xavantina, favor analisar a situação."],
    "FALHA_NIVEL_MONTANTE": [False, 0, "Atenção! Houve uma falha na leitura de nível montante na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha na leitura de nível montante na PCH Xavantina, favor analisar a situação."],
    "FILTRAGEM_BOMBA_FALHA": [False, 0, "Atenção! Houve uma falha com a bomba de filtragem na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com a bomba de filtragem na PCH Xavantina, favor analisar a situação."],
    "DRENAGEM_UNIDADES_BOMBA_FALHA": [False, 0, "Atenção! Houve uma falha com a bomba de drenagem na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com a bomba de drenagem na PCH Xavantina, favor analisar a situação."],
    "BOMBA_RECALQUE_TUBO_SUCCAO_FALHA": [False, 0, "Atenção! Houve uma falha com o tubo de succção da bomba de recalque, favor analisar a situação. Atenção! Houve uma falha com o tubo de succção da bomba de recalque, favor analisar a situação."],
    "POCO_DRENAGEM_NIVEL_MUITO_ALTO": [False, 0, "Atenção! O nível do poço de drenagem na PCH Xavantina está muito alto, favor analisar a situação. Atenção! O nível do poço de drenagem na PCH Xavantina está muito alto, favor analisar a situação."],
    "POCO_DRENAGEM_NIVEL_ALTO": [False, 0, "Atenção! O nível do poço de drenagem na PCH Xavantina está alto, favor monitorar. Atenção! O nível do poço de drenagem na PCH Xavantina está alto, favor monitorar."],
    "52SA1_SEM_FALHA": [False, 0, "Atenção! Houve uma falha com o disjuntor 52SA1 do transformador do serviço auxiliar na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com o disjuntor 52SA1 do transformador do serviço auxiliarna PCH Xavantina, favor analisar a situação."],
    "52SA2_SEM_FALHA": [False, 0, "Atenção! Houve uma falha com o disjuntor 52SA2 do gerador dieselna PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com o disjuntor 52SA2 do gerador dieselna PCH Xavantina, favor analisar a situação."],
    "52SA3_SEM_FALHA": [False, 0, "Atenção! Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciais na PCH Xavantina, favor analisar a situação . Atenção! Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciaisna PCH Xavantina, favor analisar a situação."],
    "SISTEMA_INCENDIO_ALARME_ATUADO": [False, 0, "Atenção! O alarme de incêndio da PCH Xavantina foi acionado, favor analisar a situação. Atenção! O alarme de incêndio da PCH Xavantina foi acionado, favor analisar a situação."],
    "SISTEMA_SEGURANCA_ALARME_ATUADO": [False, 0, "Atenção! O alarme do sistema de segurança da PCH Xavantina foi acionado, favor verificar a situração. Atenção! O alarme do sistema de segurança da PCH Xavantina foi acionado, favor verificar a situração."],
    "GMG_FALHA_PARTIR": [False, 0, "Atenção! Houve uma falha ao partir o gerador diesel na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha ao partir o gerador diesel na PCH Xavantina, favor analisar a situação."],
    "GMG_FALHA_PARAR": [False, 0, "Atenção! Houve uma falha ao parar o gerador diesel na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha ao parar o gerador diesel na PCH Xavantina, favor analisar a situação."],
    "GMG_OPERACAO_MANUAL": [False, 0, "Atenção! O gerador diesel saiu do modo remoto, favor analisar a situação. Atenção! O gerador diesel saiu do modo remoto, favor analisar a situação."],
    "TE_ALARME_TEMPERATURA_ENROLAMENTO": [False, 0, "Atenção! A temperatura do enrolamento do transformador elevador na PCH Xavantina está alto, favor monitorar. Atenção! A temperatura do enrolamento do transformador elevador na PCH Xavantina está alto, favor monitorar."],
    "TE_ALARME_TEMPERATURA_OLEO": [False, 0, "Atenção! A temperatura do óleo do transformador elevador na PCH Xavantina está alto, favor monitorar. Atenção! A temperatura do óleo do transformador elevador na PCH Xavantina está alto, favor monitorar."],
    "TE_ALM_TEMPERATURA_OLEO": [False, 0, "Atenção! A temperatura do óleo do transformador elevador na PCH Xavantina está alto, favor monitorar. Atenção! A temperatura do óleo do transformador elevador na PCH Xavantina está alto, favor monitorar."],
    "TE_NIVEL_OLEO_MUITO_ALTO": [False, 0, "Atenção! O nível do óleo do transformador elevador na PCH Xavantina está muito alto, favor analisar a situação. Atenção! O nível do óleo do transformador elevador na PCH Xavantina está muito alto, favor analisar a situação."],
    "TE_NIVEL_OLEO_MUITO_BAIXO": [False, 0, "Atenção! O nível do óleo do transformador elevador a PCH Xavantina está muito baixo, favor analisar a situação. Atenção! O nível do óleo do transformador elevador a PCH Xavantina está muito baixo, favor analisar a situação."]
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