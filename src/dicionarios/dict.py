IP: "dict[str, any]" = {
    "UG1_ip": "192.168.10.110",
    "UG1_porta": 502,

    "RELE_UG1_ip": "192.168.10.111",
    "RELE_UG1_porta": 502,

    "RV_UG1_ip": "192.168.10.112",
    "RV_UG1_porta": 502,

    "RT_UG1_ip": "192.168.10.112",
    "RT_UG1_porta": 502,

    "UG2_ip": "192.168.10.120",
    "UG2_porta": 502,

    "RELE_UG2_ip": "192.168.10.121",
    "RELE_UG2_porta": 502,

    "RV_UG2_ip": "192.168.10.122",
    "RV_UG2_porta": 502,

    "RT_UG2_ip": "192.168.10.122",
    "RT_UG2_porta": 502,

    "SA_ip": "192.168.10.109",
    "SA_porta": 502,

    "RELE_SE_ip": "192.168.10.32",
    "RELE_SE_porta": 502,

    "TDA_ip": "192.168.10.105",
    "TDA_porta": 502

    # "UG1_ip": "0.0.0.0",
    # "UG1_porta": 502,
# 
    # "RELE_UG1_ip": "0.0.0.0",
    # "RELE_UG1_porta": 502,
# 
    # "RV_UG1_ip": "0.0.0.0",
    # "RV_UG1_porta": 502,
# 
    # "UG2_ip": "0.0.0.0",
    # "UG2_porta": 502,
# 
    # "RELE_UG2_ip": "0.0.0.0",
    # "RELE_UG2_porta": 502,
# 
    # "RV_UG2_ip": "0.0.0.0",
    # "RV_UG2_porta": 502,
# 
    # "SA_ip": "0.0.0.0",
    # "SA_porta": 502,
# 
    # "RELE_SE_ip": "0.0.0.0",
    # "RELE_SE_porta": 502,
# 
    # "TDA_ip": "0.0.0.0",
    # "TDA_porta": 502
# 
    # "MOA_ip": "172.21.15.95",
    # "MOA_porta": 502
}

WATCHDOG = {
    "ip": "172.21.15.12",
    "porta": 502,
    "timeout_moa": 30,
    "usina": "Pampeana (PPN)",
    "local": "Painel Serviço Auxiliar (PSA)"
}

# TODO adicionar registradores após sair o mapa modbus e criar mensagens de aviso
voip: "dict[str, list[bool | str]]" = {
    "EMERGENCIA": [False, "Atenção! Houve um acionamento de emergência na PCH Pampeana, por favor analisar a situação. Atenção! Houve um acionamento de emergência na PCH Pampeana, por favor analisar a situação."],
    "WATCHDOG": [False, "Atenção! Houve um erro com a verificação do Watchdog na PCH Pampeana! Falha na verificação por Banco de Dados e CLP do MOA, favor verificar."],

    # SA
    "SA_ED_PSA_DISJ_GMG_TRIP": [False, 0, "Atenção! Foi identificado um sinal de TRIP do Disjuntor do Grupo Motor Gerador na CGH Pampeana, favor verificar."],

    "SA_ED_PSA_DPS_GMG": [False, 0, "Atenção! Houve uma falha com o Grupo Motor Gerador na CGH Pampeana, favor verificar."],
    "SA_ED_PSA_CONVERSOR_FIBRA_FALHA": [False, 0, "Atenção! Houve uma falha com o Conversor de Fibra na CGH Pampeana, favor verificar."],
    "SA_ED_PSA_CARREGADOR_BATERIAS_FALHA": [False, 0, "Atenção! Houve uma falha com o Carregador de Baterias na CGH Pampeana, favor verificar."],
    "SA_ED_PSA_GMG_DISJ_FALHA_FECHAR": [False, 0, "Atenção! Houve uma falha com o Disjuntor do Grupo Motor Gerador na CGH Pampeana, favor verificar."],

    "SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO": [False, 0, "Atenção! Foi identificado que o Nível Montante está muito baixo na CGH Pampeana, favor verificar."],

    "SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO": [False, 0, "Atenção! Foi identificado que a pressão do lado sujo do Sistema de Filtragem A está alto na CGH Pampeana, favor verificar."],
    "SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO": [False, 0, "Atenção! Foi identificado que a pressão do lado limpo do Sistema de Filtragem A está alto na CGH Pampeana, favor verificar."],
    "SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO": [False, 0, "Atenção! Foi identificado que a pressão do lado sujo do Sistema de Filtragem A está muito alto na CGH Pampeana, favor verificar."],
    "SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO": [False, 0, "Atenção! Foi identificado que a pressão do lado limpo do Sistema de Filtragem A está muito alto na CGH Pampeana, favor verificar."],

    "SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO": [False, 0, "Atenção! Foi identificado que a pressão do lado sujo do Sistema de Filtragem B está alto na CGH Pampeana, favor verificar."],
    "SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO": [False, 0, "Atenção! Foi identificado que a pressão do lado limpo do Sistema de Filtragem B está alto na CGH Pampeana, favor verificar."],
    "SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO": [False, 0, "Atenção! Foi identificado que a pressão do lado sujo do Sistema de Filtragem B está muito alto na CGH Pampeana, favor verificar."],
    "SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO": [False, 0, "Atenção! Foi identificado que a pressão do lado limpo do Sistema de Filtragem B está muito alto na CGH Pampeana, favor verificar."],

    # UGs
    "UG1_CD_CMD_UHRV_MODO_MANUTENCAO": [False, 0, "Atenção! Foi identificado o acionamento do comando do modo de manutenção da UHRV da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_CD_CMD_UHLM_MODO_MANUTENCAO": [False, 0, "Atenção! Foi identificado o acionamento do comando do modo de manutenção da UHLM da Unidade de Geração 1 na CGH Pampeana, favor verificar."],

    "UG1_ED_BYPASS_FALHA_ABRIR": [False, 0, "Atenção! Foi identificado uma falha ao abrir a Válvula Bypass da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_ED_BYPASS_FALHA_FECHAR": [False, 0, "Atenção! Foi identificado uma falha ao fechar a Válvula Bypass da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR": [False, 0, "Atenção! Foi identificado uma falha ao fechar o Distribuidor da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR": [False, 0, "Atenção! Foi identificado uma falha ao ligar a resistência do aquecedor do gerador da Unidade de Geração 1 na CGH Pampeana, favor verificar."],

    "UG1_EA_TRISTORES_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura de Tristores da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_EA_CROWBAR_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Crowbar da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_EA_TRAFO_EXCITACAO_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Transformador de Excitação da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_EA_UHRV_TEMP_OLEO_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Óleo da UHRV da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura de Fase A do gerador da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura de Fase B do gerador da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura de Fase C do gerador da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Núcleo 1 do Gerador da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_EA_GERADOR_NUCLEO_2_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Núcleo 2 do Gerador da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Núcleo 3 do Gerador da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_EA_MANCAL_GUIA_CASQUILHO_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Mancal Guia Casquilho da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_EA_MANCAL_COMBINADO_CASQUILHO_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Mancal Combinado Casquilho da Unidade de Geração 1 na CGH Pampeana, favor verificar."],
    "UG1_EA_MANCAL_COMBINADO_ESCORA_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Mancal Combinado Escora da Unidade de Geração 1 na CGH Pampeana, favor verificar."],

    "UG2_CD_CMD_UHRV_MODO_MANUTENCAO": [False, 0, "Atenção! Foi identificado o acionamento do comando do modo de manutenção da UHRV da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_CD_CMD_UHLM_MODO_MANUTENCAO": [False, 0, "Atenção! Foi identificado o acionamento do comando do modo de manutenção da UHLM da Unidade de Geração 2 na CGH Pampeana, favor verificar."],

    "UG2_ED_BYPASS_FALHA_ABRIR": [False, 0, "Atenção! Foi identificado uma falha ao abrir a Válvula Bypass da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_ED_BYPASS_FALHA_FECHAR": [False, 0, "Atenção! Foi identificado uma falha ao fechar a Válvula Bypass da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR": [False, 0, "Atenção! Foi identificado uma falha ao fechar o Distribuidor da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR": [False, 0, "Atenção! Foi identificado uma falha ao ligar a resistência do aquecedor do gerador da Unidade de Geração 2 na CGH Pampeana, favor verificar."],

    "UG2_EA_TRISTORES_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura de Tristores da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_EA_CROWBAR_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Crowbar da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_EA_TRAFO_EXCITACAO_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Transformador de Excitação da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_EA_UHRV_TEMP_OLEO_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Óleo da UHRV da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura de Fase A do gerador da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura de Fase B do gerador da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura de Fase C do gerador da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Núcleo 1 do Gerador da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_EA_GERADOR_NUCLEO_2_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Núcleo 2 do Gerador da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Núcleo 3 do Gerador da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_EA_MANCAL_GUIA_CASQUILHO_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Mancal Guia Casquilho da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_EA_MANCAL_COMBINADO_CASQUILHO_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Mancal Combinado Casquilho da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
    "UG2_EA_MANCAL_COMBINADO_ESCORA_FALHA_LEITURA": [False, 0, "Atenção! Foi identificado uma falha na leitura de temperatura do Mancal Combinado Escora da Unidade de Geração 2 na CGH Pampeana, favor verificar."],
}