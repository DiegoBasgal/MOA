ips: "dict[str, any]" = {
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

    "UG1_ip": "0.0.0.0",
    "UG1_porta": 502,

    "RELE_UG1_ip": "0.0.0.0",
    "RELE_UG1_porta": 502,

    "RV_UG1_ip": "0.0.0.0",
    "RV_UG1_porta": 502,

    "UG2_ip": "0.0.0.0",
    "UG2_porta": 502,

    "RELE_UG2_ip": "0.0.0.0",
    "RELE_UG2_porta": 502,

    "RV_UG2_ip": "0.0.0.0",
    "RV_UG2_porta": 502,

    "SA_ip": "0.0.0.0",
    "SA_porta": 502,

    "RELE_SE_ip": "0.0.0.0",
    "RELE_SE_porta": 502,

    "TDA_ip": "0.0.0.0",
    "TDA_porta": 502

    # "MOA_ip": "172.21.15.95",
    # "MOA_porta": 502
}

# TODO adicionar registradores após sair o mapa modbus e criar mensagens de aviso
voip: "dict[str, list[bool | str]]" = {
    "EMERGENCIA": [False, "Atenção! Houve um acionamento de emergência na PCH Pampeana, por favor analisar a situação. Atenção! Houve um acionamento de emergência na PCH Pampeana, por favor analisar a situação."],

    "SA_ED_PSA_DISJ_GMG_TRIP": [False, "Atenção! Foi identificado um sinal de TRIP do Disjuntor do Grupo Motor Gerador na CGH Pampeana, favor verificar."],

    "SA_ED_PSA_DPS_GMG": [False, "Atenção! Houve uma falha com o Grupo Motor Gerador na CGH Pampeana, favor verificar."],
    "SA_ED_PSA_CONVERSOR_FIBRA_FALHA": [False, "Atenção! Houve uma falha com o Conversor de Fibra na CGH Pampeana, favor verificar."],
    "SA_ED_PSA_CARREGADOR_BATERIAS_FALHA": [False, "Atenção! Houve uma falha com o Carregador de Baterias na CGH Pampeana, favor verificar."],
    "SA_ED_PSA_GMG_DISJ_FALHA_FECHAR": [False, "Atenção! Houve uma falha com o Disjuntor do Grupo Motor Gerador na CGH Pampeana, favor verificar."],

    "SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO": [False, "Atenção! Foi identificado que o Nível Montante está muito baixo na CGH Pampeana, favor verificar."],

    "SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO": [False, "Atenção! Foi identificado que a pressão do lado sujo do Sistema de Filtragem A está alto na CGH Pampeana, favor verificar."],
    "SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO": [False, "Atenção! Foi identificado que a pressão do lado limpo do Sistema de Filtragem A está alto na CGH Pampeana, favor verificar."],
    "SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO": [False, "Atenção! Foi identificado que a pressão do lado sujo do Sistema de Filtragem A está muito alto na CGH Pampeana, favor verificar."],
    "SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO": [False, "Atenção! Foi identificado que a pressão do lado limpo do Sistema de Filtragem A está muito alto na CGH Pampeana, favor verificar."],

    "SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO": [False, "Atenção! Foi identificado que a pressão do lado sujo do Sistema de Filtragem B está alto na CGH Pampeana, favor verificar."],
    "SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO": [False, "Atenção! Foi identificado que a pressão do lado limpo do Sistema de Filtragem B está alto na CGH Pampeana, favor verificar."],
    "SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO": [False, "Atenção! Foi identificado que a pressão do lado sujo do Sistema de Filtragem B está muito alto na CGH Pampeana, favor verificar."],
    "SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO": [False, "Atenção! Foi identificado que a pressão do lado limpo do Sistema de Filtragem B está muito alto na CGH Pampeana, favor verificar."],
}