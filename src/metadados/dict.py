dict_compartilhado: dict[str, dict[str, any]] = {
    "CFG": {
        "UG1_slave_ip": "10.101.2.215",
        "UG1_slave_porta": 5003,
        "UG2_slave_ip": "10.101.2.215",
        "UG2_slave_porta": 5003,
        "MOA_slave_ip": "0.0.0.0",
        "MOA_slave_porta": 5002,
        "opc_server": "opc.tcp://localhost:4840",
    },

    "GLB": {
        "avisado_eletrica": False
    }
}

dict_voip: dict[str, list[bool | str]] = {
    "LG_FALHA_ATUADA": [False, "Atenção! Houve uma falha com o Limpa Grades na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com o Limpa Grades na PCH Xavantina, favor analisar a situação."],
    "FALHA_NIVEL_MONTANTE": [False, "Atenção! Houve uma falha na leitura de nível montante na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha na leitura de nível montante na PCH Xavantina, favor analisar a situação."],
    "FILTRAGEM_BOMBA_FALHA": [False, "Atenção! Houve uma falha com a bomba de filtragem na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com a bomba de filtragem na PCH Xavantina, favor analisar a situação."],
    "DRENAGEM_UNIDADES_BOMBA_FALHA": [False, "Atenção! Houve uma falha com a bomba de drenagem na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com a bomba de drenagem na PCH Xavantina, favor analisar a situação."],
    "BOMBA_RECALQUE_TUBO_SUCCAO_FALHA": [False, "Atenção! Houve uma falha com o tubo de succção da bomba de recalque, favor analisar a situação. Atenção! Houve uma falha com o tubo de succção da bomba de recalque, favor analisar a situação."],
    "POCO_DRENAGEM_NIVEL_MUITO_ALTO": [False, "Atenção! O nível do poço de drenagem na PCH Xavantina está muito alto, favor analisar a situação. Atenção! O nível do poço de drenagem na PCH Xavantina está muito alto, favor analisar a situação."],
    "POCO_DRENAGEM_NIVEL_ALTO": [False, "Atenção! O nível do poço de drenagem na PCH Xavantina está alto, favor monitorar. Atenção! O nível do poço de drenagem na PCH Xavantina está alto, favor monitorar."],
    "52SA1_SEM_FALHA": [False, "Atenção! Houve uma falha com o disjuntor 52SA1 do transformador do serviço auxiliar na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com o disjuntor 52SA1 do transformador do serviço auxiliarna PCH Xavantina, favor analisar a situação."],
    "52SA2_SEM_FALHA": [False, "Atenção! Houve uma falha com o disjuntor 52SA2 do gerador dieselna PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com o disjuntor 52SA2 do gerador dieselna PCH Xavantina, favor analisar a situação."],
    "52SA3_SEM_FALHA": [False, "Atenção! Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciais na PCH Xavantina, favor analisar a situação . Atenção! Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciaisna PCH Xavantina, favor analisar a situação."],
    "SISTEMA_INCENDIO_ALARME_ATUADO": [False, "Atenção! O alarme de incêndio da PCH Xavantina foi acionado, favor analisar a situação. Atenção! O alarme de incêndio da PCH Xavantina foi acionado, favor analisar a situação."],
    "SISTEMA_SEGURANCA_ALARME_ATUADO": [False, "Atenção! O alarme do sistema de segurança da PCH Xavantina foi acionado, favor verificar a situração. Atenção! O alarme do sistema de segurança da PCH Xavantina foi acionado, favor verificar a situração."],
    "GMG_FALHA_PARTIR": [False, "Atenção! Houve uma falha ao partir o gerador diesel na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha ao partir o gerador diesel na PCH Xavantina, favor analisar a situação."],
    "GMG_FALHA_PARAR": [False, "Atenção! Houve uma falha ao parar o gerador diesel na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha ao parar o gerador diesel na PCH Xavantina, favor analisar a situação."],
    "GMG_OPERACAO_MANUAL": [False, "Atenção! O gerador diesel saiu do modo remoto, favor analisar a situação. Atenção! O gerador diesel saiu do modo remoto, favor analisar a situação."],
    "TE_ALARME_TEMPERATURA_ENROLAMENTO": [False, "Atenção! A temperatura do enrolamento do transformador elevador na PCH Xavantina está alto, favor monitorar. Atenção! A temperatura do enrolamento do transformador elevador na PCH Xavantina está alto, favor monitorar."],
    "TE_ALM_TEMPERATURA_ENROLAMENTO": [False, "Atenção! A temperatura do enrolamento do transformador elevador na PCH Xavantina está alto, favor monitorar. Atenção! A temperatura do enrolamento do transformador elevador na PCH Xavantina está alto, favor monitorar."],
    "TE_ALARME_TEMPERATURA_OLEO": [False, "Atenção! A temperatura do óleo do transformador elevador na PCH Xavantina está alto, favor monitorar. Atenção! A temperatura do óleo do transformador elevador na PCH Xavantina está alto, favor monitorar."],
    "TE_ALM_TEMPERATURA_OLEO": [False, "Atenção! A temperatura do óleo do transformador elevador na PCH Xavantina está alto, favor monitorar. Atenção! A temperatura do óleo do transformador elevador na PCH Xavantina está alto, favor monitorar."],
    "TE_NIVEL_OLEO_MUITO_ALTO": [False, "Atenção! O nível do óleo do transformador elevador na PCH Xavantina está muito alto, favor analisar a situação. Atenção! O nível do óleo do transformador elevador na PCH Xavantina está muito alto, favor analisar a situação."],
    "TE_NIVEL_OLEO_MUITO_BAIXO": [False, "Atenção! O nível do óleo do transformador elevador a PCH Xavantina está muito baixo, favor analisar a situação. Atenção! O nível do óleo do transformador elevador a PCH Xavantina está muito baixo, favor analisar a situação."]
}

dict_telegram = {

}

dict_watchdog: dict[str, any] = {
    "unit_id": 1,
    "ip_slave": "172.21.15.12",
    "port_slave": 5002,
    "timeout_modbus": 5,
    "timeout_moa": 30,
    "nome_usina": "Simul",
    "nome_local": "NOME DO LOCAL QUE ESTA CONECTANDO"
}