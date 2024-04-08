REG_MOA = {
    "SM_STATE":                                                                         10,         # Coil                                  (OP -> 0x05 Write Single Coil)
    "PAINEL_LIDO":                                                                      12,         # Coil                                  (OP -> 0x05 Write Single Coil)

    "MOA_IN_EMERG":                                                                     13,         # Coil                                  (OP -> 0x02 Read Input Status)
    "MOA_IN_HABILITA_AUTO":                                                             14,         # Coil                                  (OP -> 0x02 Read Input Status)
    "MOA_IN_DESABILITA_AUTO":                                                           15,         # Coil                                  (OP -> 0x02 Read Input Status)

    "MOA_OUT_MODE":                                                                     11,         # Coil                                  (OP -> 0x05 Write Single Coil)
    "MOA_OUT_EMERG":                                                                    16,         # Coil                                  (OP -> 0x05 Write Single Coil)
    "MOA_OUT_STATUS":                                                                   409,        # Holding Register                      (OP -> 0x06 Write Single Register)
    "MOA_OUT_TARGET_LEVEL":                                                             417,        # Holding Register                      (OP -> 0x06 Write Single Register)
    "MOA_OUT_SETPOINT":                                                                 418,        # Holding Register                      (OP -> 0x06 Write Single Register)

    "MOA_IN_EMERG_UG1":                                                                 20,         # Coil                                  (OP -> 0x02 Read Input Status)
    "MOA_OUT_BLOCK_UG1":                                                                21,         # Coil                                  (OP -> 0x05 Write Single Coil)
    "MOA_OUT_ETAPA_UG1":                                                                422,        # Holding Register                      (OP -> 0x06 Write Single Register)
    "MOA_OUT_STATE_UG1":                                                                423,        # Holding Register                      (OP -> 0x06 Write Single Register)

    "MOA_IN_EMERG_UG2":                                                                 25,         # Coil                                  (OP -> 0x02 Read Input Status)
    "MOA_OUT_BLOCK_UG2":                                                                26,         # Coil                                  (OP -> 0x05 Write Single Coil)
    "MOA_OUT_ETAPA_UG2":                                                                427,        # Holding Register                      (OP -> 0x06 Write Single Register)
    "MOA_OUT_STATE_UG2":                                                                428,        # Holding Register                      (OP -> 0x06 Write Single Register)
}

REG_RELE = {
    "SE": {
        "VAB":                                                                          154,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "VBC":                                                                          155,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "VCA":                                                                          156,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "IA":                                                                           320,        # Input Register                        (OP -> Read Input Registers - 3x)
        "IB":                                                                           322,        # Input Register                        (OP -> Read Input Registers - 3x)
        "IC":                                                                           324,        # Input Register                        (OP -> Read Input Registers - 3x)
        "P":                                                                            353,        # Input Register                        (OP -> Read Input Registers - 3x)
        "Q":                                                                            361,        # Input Register                        (OP -> Read Input Registers - 3x)
        "S":                                                                            369,        # Input Register                        (OP -> Read Input Registers - 3x)
        "F":                                                                            374,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "FP":                                                                           373,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "EA_GERADA":                                                                    423,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
        "CONSUMIDA":                                                                    429,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
        "GERADA":                                                                       427,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
    },

    "UG1": {
        "IA":                                                                           320,        # Input Register                        (OP -> Read Input Registers - 3x)
        "IB":                                                                           322,        # Input Register                        (OP -> Read Input Registers - 3x)
        "IC":                                                                           324,        # Input Register                        (OP -> Read Input Registers - 3x)
        "VAB":                                                                          330,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "VBC":                                                                          332,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "VCA":                                                                          334,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "P":                                                                            353,        # Input Register                        (OP -> Read Input Registers - 3x)
        "Q":                                                                            361,        # Input Register                        (OP -> Read Input Registers - 3x)
        "S":                                                                            369,        # Input Register                        (OP -> Read Input Registers - 3x)
        "F":                                                                            374,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "FP":                                                                           373,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "EA_GERADA":                                                                    423,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
        "CONSUMIDA":                                                                    429,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
        "GERADA":                                                                       427,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
    },

    "UG2": {
        "IA":                                                                           320,        # Input Register                        (OP -> Read Input Registers - 3x)
        "IB":                                                                           322,        # Input Register                        (OP -> Read Input Registers - 3x)
        "IC":                                                                           324,        # Input Register                        (OP -> Read Input Registers - 3x)
        "VAB":                                                                          330,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "VBC":                                                                          332,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "VCA":                                                                          334,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "P":                                                                            353,        # Input Register                        (OP -> Read Input Registers - 3x)
        "Q":                                                                            361,        # Input Register                        (OP -> Read Input Registers - 3x)
        "S":                                                                            369,        # Input Register                        (OP -> Read Input Registers - 3x)
        "F":                                                                            374,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "FP":                                                                           373,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "EA_GERADA":                                                                    423,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
        "CONSUMIDA":                                                                    429,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
        "GERADA":                                                                       427,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
    },
}

REG_SASE = {
    ### COMANDOS
    ## CMD_SA_SE
    "CMD_REARME_FALHAS":                                                                [12288, 0],
    "CMD_PD_BOMBA_1_PRINCIPAL":                                                         [12288, 1],
    "CMD_PD_BOMBA_2_PRINCIPAL":                                                         [12288, 2],
    "CMD_DISJ_TSA_ABRE":                                                                [12288, 13],
    "CMD_DISJ_TSA_FECHA":                                                               [12288, 14],
    "CMD_DISJ_GMG_ABRE":                                                                [12288, 15],

    "CMD_DISJ_GMG_FECHA":                                                               [12289, 0],
    "CMD_DISJ_LINHA_FECHA":                                                             [12289, 1],
    "CMD_DISJ_LINHA_ABRE":                                                              [12289, 2],
    "CMD_SFA_COMUTA_ELEMENTO":                                                          [12289, 3],
    "CMD_SFA_AUTOMATICO":                                                               [12289, 4],
    "CMD_SFA_MANUAL":                                                                   [12289, 5],
    "CMD_SFB_MANUAL":                                                                   [12289, 8],
    "CMD_SFB_AUTOMATICO":                                                               [12289, 9],
    "CMD_SFB_COMUTA_ELEMENTO":                                                          [12289, 10],

    ### STATUS
    ## SST_ENTRADAS_DIGITAIS_0
    "BOTAO_REARME_FALHAS_PAINEL":                                                       [12308, 0],
    "BOTAO_BLOQUEIO_86BTBF":                                                            [12308, 1],
    "POCO_DRANAGEM_BOMBA_1_AUTOMATICO":                                                 [12308, 2],
    "POCO_DRENAGEM_BOMBA_2_ATUTOMATICO":                                                [12308, 3],
    "DISJUNTORES_MODO_REMOTO":                                                          [12308, 4],
    "DISJUNTOR_TSA_TRIP":                                                               [12308, 5],
    "DISJUNTOR_GMG_TRIP":                                                               [12308, 6],
    "RELE_BLOQUEIO_86BTBF":                                                             [12308, 7],
    "CARREGADOR_BATERIAS_FALHA":                                                        [12308, 8],
    "CONVERSOR_FIBRA_FALHA":                                                            [12308, 9],
    "SUPERVISOR_TENSAO_FALHA":                                                          [12308, 10],
    "DPS_TSA":                                                                          [12308, 11],
    "DPS_GMG":                                                                          [12308, 12],
    "POCO_DRENAGEM_BOMBA_1_DEFEITO":                                                    [12308, 13],
    "POCO_DRENAGEM_BOMBA_1_LIGADA":                                                     [12308, 14],
    "POCO_DRENAGEM_BOMBA_2_DEFEITO":                                                    [12308, 15],

    "POCO_DRENAGEM_BOMBA_2_LIGADA":                                                     [12309, 0],
    "SF_BOMBA_1_DEFEITO":                                                               [12309, 1],
    "SF_BOMBA_1_LIGADA":                                                                [12309, 2],
    "POCO_DRENAGEM_SENSOR_NIVEL_MUITO_BAIXO":                                           [12309, 5],
    "POCO_DRENAGEM_SENSOR_NIVEL_DESLIGA_BOMBAS":                                        [12309, 6],
    "POCO_DRENAGEM_SENSOR_NIVEL_LIGA_BOMBA":                                            [12309, 7],
    "POCO_DRENAGEM_SENSOR_NIVEL_ALTO":                                                  [12309, 8],
    "POCO_DRENAGEM_SENSOR_NIVEL_MUITO_ALTO":                                            [12309, 9],
    "DISJUNTOR_TSA_FECHADO":                                                            [12309, 10],
    "DISJUNTOR_GMG_FECHADO":                                                            [12309, 11],
    "SUPERVISOR_TENSAO_TSA_FALHA":                                                      [12309, 12],
    "SUPERVISOR_TENSAO_GMG_FALHA":                                                      [12309, 13],
    "TE_TEMPERATURA_MUITO_ALTA":                                                        [12309, 14],
    "SE_DISJUNTOR_LINHA_FECHADO":                                                       [12309, 15],

    ## SST_ENTRADAS_DIGITAIS_1
    "SE_DISJUNTOR_LINHA_ABERTO":                                                        [12310, 0],
    "TE_TEMPERATURA_ALARME":                                                            [12310, 1],
    "TE_PRESSAO_MUITO_ALTA":                                                            [12310, 2],
    "TE_NIVEL_OLEO_MUITO_BAIXO":                                                        [12310, 3],
    "PRTVA1_50_BF":                                                                     [12310, 4],
    "PRTVA1_FILTRAGEM_ACIONA":                                                          [12310, 5],
    "PRTVA2_50BF":                                                                      [12310, 6],
    "PRTVA2_FILTRAGEM_ACIONA":                                                          [12310, 7],
    "SFA_ENTRADA_ELEMENTO_1_ABERTA":                                                    [12310, 8],
    "SFA_ENTRADA_ELEMENTO_2_ABERTA":                                                    [12310, 9],
    "SFA_LIMPEZA_ELEMENTO_1_ABERTA":                                                    [12310, 10],
    "SFA_LIMPEZA_ELEMENTO_2_ABERTA":                                                    [12310, 11],
    "SFB_PRESSAO_SAIDA":                                                                [12310, 12],
    "SFB_ENTRADA_ELEMENTO_1_ABERTA":                                                    [12310, 13],
    "SFB_ENTRADA_ELEMENTO_2_ABERTA":                                                    [12310, 14],
    "SFB_LIMPEZA_ELEMENTO_1_ABERTA":                                                    [12310, 15],

    "PSA_SFB_LIMPEZA_ELEMENTO_2_ABERTO":                                                [12311, 0],
    "PSA_CONVERSOR_FIBRA_FALHA":                                                        [12311, 1],
    "PSA_RELE_LINHA_SEM_TRIP_OU_FALHA":                                                 [12311, 2],

    ## STT_FALHAS_ANALOGICAS
    "NIVEL_JUSANTE_FALHA_LEITURA":                                                      [12338, 1],
    "SFA_PRESSAO_LADO_LIMPO_FALHA_LEITURA":                                             [12338, 2],
    "SFA_PRESSAO_LADO_SUJO_FALHA_LEITURA":                                              [12338, 3],
    "SFB_PRESSAO_LADO_LIMPO_FALHA_LEITURA":                                             [12338, 4],
    "SFB_PRESSAO_LADO_SUJO_FALHA_LEITURA":                                              [12338, 5],

    ## STT_ALARMES_HH_ANALOGICAS
    "NIVEL_JUSANTE_MUITO_ALTO":                                                         [12340, 0],
    "SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO":                                                [12340, 3],
    "SFA_PRESSAO_LADO_SUJO_MUITO_ALTO":                                                 [12340, 4],
    "SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO":                                                [12340, 5],
    "SFB_PRESSAO_LADO_SUJO_MUITO_ALTO":                                                 [12340, 6],

    ## STT_ALARMES_H_ANALOGICAS
    "PSA_NIVEL_JUSANTE_ALTO":                                                           [12342, 0],
    "PSA_SFA_PRESSAO_LADO_LIMPO_ALTO":                                                  [12342, 3],
    "PSA_SFA_PRESSAO_LADO_SUJO_ALTO":                                                   [12342, 4],
    "PSA_SFB_PRESSAO_LADO_LIMPO_ALTO":                                                  [12342, 5],
    "PSA_SFB_PRESSAO_LADO_SUJO_ALTO":                                                   [12342, 6],

    ## STT_ALARMES_L_ANALOGICAS
    "NIVEL_JUSANTE_BAIXO":                                                              [12344, 0],
    "SFA_PRESSAO_LADO_LIMPO_BAIXO":                                                     [12344, 3],
    "SFA_PRESSAO_LADO_SUJO_BAIXO":                                                      [12344, 4],
    "SFB_PRESSAO_LADO_LIMPO_BAIXO":                                                     [12344, 5],
    "SFB_PRESSAO_LADO_SUJO_BAIXO":                                                      [12344, 6],

    ## STT_ALARMES_LL_ANALOGICAS
    "NIVEL_JUSANTE_MUITO_BAIXO":                                                        [12346, 0],
    "SFA_PRESSAO_LADO_LIMPO_MUITO_BAIXO":                                               [12346, 3],
    "SFA_PRESSAO_LADO_SUJO_MUITO_BAIXO":                                                [12346, 4],
    "SFB_PRESSAO_LADO_LIMPO_MUITO_BAIXO":                                               [12346, 5],
    "SFB_PRESSAO_LADO_SUJO_MUITO_BAIXO":                                                [12346, 6],

    ## STT_SA_SE
    "DRENAGEM_BOMBA_1_INDISPONIVEL":                                                    [12348, 0],
    "DRENAGEM_BOMBA_2_INDISPONIVEL":                                                    [12348, 1],
    "DRENAGEM_BOMBA_1_PRINCIPAL":                                                       [12348, 2],
    "DRENAGEM_BOMBA_2_PRINCIPAL":                                                       [12348, 3],
    "DRENAGEM_BOIAS_DISCREPANCIA":                                                      [12348, 4],
    "SF_BOMBA_1_INDISPONIVEL":                                                          [12348, 5],
    "ESGOTAMENTO_BOMBA_2_INDISPONIVEL":                                                 [12348, 6],
    "SF_BOMBA_1_FALHA":                                                                 [12348, 7],
    "ESGOTAMENTO_BOMBA_2_FALHA":                                                        [12348, 8],
    "GMG_DISJUNTOR_FALHA_FECHAR":                                                       [12348, 9],
    "GMG_DISJUNTOR_FALHA_ABRIR":                                                        [12348, 10],
    "TSA_DISJUNTOR_FALHA_ABRIR":                                                        [12348, 11],
    "TSA_DISJUNTOR_FALHA_FECHAR":                                                       [12348, 12],
    "SE_DISJUNTOR_FALHA_ABRIR":                                                         [12348, 13],
    "SE_DISJUNTOR_FALHA_FECHAR":                                                        [12348, 14],

    ## STT_BLOQUEIO_50BF
    "BLOQUEIO_50BF_ATUADO":                                                             [12351, 15],

    ## STT_BLOQUEIO_86BTLSA
    "BLOQUEIO_86BTLSA_ATUADO":                                                          [12353, 15],

    ## STT_SF
    "SISTEMA_DE_FILTRAGEM_OPERANDO":                                                    [12354, 0],
    "SFA_COMUTACAO_MANUAL":                                                             [12354, 1],
    "SFA_COMUTACAO_BLOQUEADA":                                                          [12354, 2],
    "SFA_ELEMENTO_1_OPERANDO":                                                          [12354, 3],
    "SFA_ELEMENTO_1_LIMPEZA":                                                           [12354, 4],
    "SFA_ELEMENTO_2_LIMPEZA":                                                           [12354, 5],
    "SFA_ELEMENTO_2_OPERANDO":                                                          [12354, 6],
    "SFA_ELEMENTO_1_FALHA_ABRIR_ENTRADA":                                               [12354, 7],
    "SFA_ELEMENTO_1_FALHA_FECHAR_ENTRADA":                                              [12354, 8],
    "SFA_ELEMENTO_2_FALHA_ABRIR_ENTRADA":                                               [12354, 9],
    "SFA_ELEMENTO_2_FALHA_FECHAR_ENTRADA":                                              [12354, 10],
    "SFA_ELEMENTO_1_FALHA_ABRIR_LIMPEZA":                                               [12354, 11],
    "SFA_ELEMENTO_1_FALHA_FECHAR_LIMPEZA":                                              [12354, 12],
    "SFA_ELEMENTO_2_FALHA_ABRIR_LIMPEZA":                                               [12354, 13],
    "SFA_ELEMENTO_2_FALHA_FECHAR_LIMPEZA":                                              [12354, 14],
    "SFB_ELEMENTO_1_OPERANDO":                                                          [12354, 15],

    "SFB_ELEMENTO_1_LIMPEZA":                                                           [12355, 0],
    "SFB_ELEMENTO_2_LIMPEZA":                                                           [12355, 1],
    "SFB_ELEMENTO_2_OPERANDO":                                                          [12355, 2],
    "SFB_ELEMENTO_1_FALHA_ABRIR_ENTRADA":                                               [12355, 3],
    "SFB_ELEMENTO_1_FALHA_FECHAR_ENTRADA":                                              [12355, 4],
    "SFB_ELEMENTO_2_FALHA_ABRIR_ENTRADA":                                               [12355, 5],
    "SFB_ELEMENTO_2_FALHA_FECHAR_ENTRADA":                                              [12355, 6],
    "SFB_ELEMENTO_1_FALHA_ABRIR_LIMPEZA":                                               [12355, 7],
    "SFB_ELEMENTO_1_FALHA_FECHAR_LIMPEZA":                                              [12355, 8],
    "SFB_ELEMENTO_2_FALHA_ABRIR_LIMPEZA":                                               [12355, 9],
    "SFB_ELEMENTO_2_FALHA_FECHAR_LIMPEZA":                                              [12355, 10],
    "SFB_COMUTACAO_MANUAL":                                                             [12355, 11],
    "SFB_COMUTACAO_BLOQUEADA":                                                          [12355, 12],

    ## LEITURAS_ANALÓGICAS
    "NIVEL_JUSANTE_CASA_FORCA":                                                         12488,
    "NIVEL_MONTANTE_TA":                                                                12490,
    "SFA_LADO_LIMPO":                                                                   12500,
    "SFA_LADO_SUJO":                                                                    12502,
    "SFB_LADO_LIMPO":                                                                   12504,
    "SFB_LADO_SUJO":                                                                    12506,

    ## LEITURAS_DIGITAIS
    "REAL_STT_SFA":                                                                     12508,
    "REAL_STT_SFB":                                                                     12510,
}

REG_TDA = {
    ### COMANDOS
    ## CMD_QCTA
    "CMD_RESET_GERAL":                                                                  [12288, 0],

    ### STATUS
    ## STT_ENTRADAS_DIGITAIS_0
    "DISPOSITIVO_PROTETOR_DE_SURTO":                                                    [12308, 0],
    "UHLG_BOMBA_1_LIGADA":                                                              [12308, 1],
    "UHLG_BOMBA_1_DEFEITO":                                                             [12308, 2],
    "UHLG_BOMBA_2_LIGADA":                                                              [12308, 3],
    "UHLG_BOMBA_2_DEFEITO":                                                             [12308, 4],
    "MONOVIA_MOTOR_1_LIGADA":                                                           [12308, 5],
    "MONOVIA_MOTOR_1_DEFEITO":                                                          [12308, 6],
    "MONOVIA_MOTOR_2_LIGADA":                                                           [12308, 7],
    "MONOVIA_MOTOR_2_DEFEITO":                                                          [12308, 8],
    "CONVERSOR_FIBRA_FALHA":                                                            [12308, 9],

    ## STT_ANALÓGICAS
    "NIVEL_JUSANTE_GRADE_FALHA_LEITURA":                                                [12328, 0],
    "NIVEL_MONTANTE_GRADE_FALHA_LEITURA":                                               [12328, 1],
    "NIVEL_JUSANTE_GRADE_MUITO_ALTO":                                                   [12328, 2],
    "NIVEL_MONTANTE_GRADE_MUITO_ALTO":                                                  [12328, 3],
    "NIVEL_JUSANTE_GRADE_ALTO":                                                         [12328, 4],
    "NIVEL_MONTANTE_GRADE_ALTO":                                                        [12328, 5],
    "NIVEL_JUSANTE_GRADE_BAIXO":                                                        [12328, 6],
    "NIVEL_MONTANTE_GRADE_BAIXO":                                                       [12328, 7],
    "NIVEL_JUSANTE_GRADE_MUITO_BAIXO":                                                  [12328, 8],
    "NIVEL_MONTANTE_GRADE_MUITO_BAIXO":                                                 [12328, 9],

    ## LEITURAS_ANALÓGICAS
    "NIVEL_JUSANTE_GRADE":                                                              12348,
    "NIVEL_MONTANTE_GRADE":                                                             12350,
}

REG_UG = {
    "UG1": {
        ### COMANDOS
        ## CMD_UG1
        "CMD_REARME_FALHAS":                                                            [12288, 0],
        "CMD_COMANDO_PARADA_DE_EMERGENCIA":                                             [12288, 1],
        "CMD_CONTROLE_NIVEL":                                                           [12288, 2],
        "CMD_CONTROLE_POTENCIA_MANUAL":                                                 [12288, 3],
        "CMD_CONTROLE_POTENCIA_POR_NIVEL":                                              [12288, 4],
        "CMD_PARADA_NIVEL_HABILITA":                                                    [12288, 5],
        "CMD_PARADA_NIVEL_DESABILITA":                                                  [12288, 6],
        "CMD_RV_MANUTENCAO":                                                            [12288, 10],
        "CMD_RV_AUTOMATICO":                                                            [12288, 11],

        # CMD_PARTIDA_PARADA
        "CMD_PARADA_TOTAL":                                                             [12290, 0],
        "CMD_SINCRONISMO":                                                              [12290, 9],

        ## CMD_UHRV
        "CMD_UHRV_MODO_AUTOMATICO":                                                     [12292, 0],
        "CMD_UHRV_MODO_MANUTENCAO":                                                     [12292, 1],
        "CMD_UHRV_BOMBA_1_LIGA":                                                        [12292, 2],
        "CMD_UHRV_BOMBA_1_DESLIGA":                                                     [12292, 3],
        "CMD_UHRV_BOMBA_2_LIGA":                                                        [12292, 4],
        "CMD_UHRV_BOMBA_2_DESLIGA":                                                     [12292, 5],
        "CMD_UHRV_BOMBA_1_PRINCIPAL":                                                   [12292, 6],
        "CMD_UHRV_BOMBA_2_PRINCIPAL":                                                   [12292, 7],

        ## CMD_UHLM
        "CMD_UHLM_MODO_AUTOMATICO":                                                     [12294, 0],
        "CMD_UHLM_MODO_MANUTENCAO":                                                     [12294, 1],
        "CMD_UHLM_BOMBA_1_LIGA":                                                        [12294, 2],
        "CMD_UHLM_BOMBA_1_DESLIGA":                                                     [12294, 3],

        ## COMANDOS_ANALÓGICOS
        # CONTROLE_NÍVEL
        "SETPOINT_NIVEL_5":                                                             12588,
        "SETPOINT_NIVEL_4":                                                             12590,
        "SETPOINT_NIVEL_3":                                                             12592,
        "SETPOINT_NIVEL_2":                                                             12594,
        "SETPOINT_NIVEL_1":                                                             12596,
        "SETPOINT_NIVEL_PARADA":                                                        12598,
        "SETPOINT_POTENCIA_5":                                                          12600,
        "SETPOINT_POTENCIA_4":                                                          12602,
        "SETPOINT_POTENCIA_3":                                                          12604,
        "SETPOINT_POTENCIA_2":                                                          12606,
        "SETPOINT_POTENCIA_1":                                                          12608,
        "SETPOINT_MINIMO_POTENCIA":                                                     12610,
        "SETPOINT_MAXIMO_POTENCIA":                                                     12612,
        "SETPOINT_NIVEL":                                                               12616,


        ### STATUS
        ## STT_FALHAS_TEMPERATURA
        "TIRISTORES_TEMPERATURA_FALHA_LEITURA":                                         [12328, 0],
        "CROWBAR_TEMPERATURA_FALHA_LEITURA":                                            [12328, 1],
        "TRAFO_EXCITACAO_TEMPERATURA_FALHA_LEITURA":                                    [12328, 2],
        "UHRV_TEMPERATURA_OLEO_FALHA_LEITURA":                                          [12328, 3],
        "UHLM_TEMPERATURA_OLEO_FALHA_LEITURA":                                          [12328, 4],
        "GERADOR_FASE_A_TEMPERATURA_FALHA_LEITURA":                                     [12328, 7],
        "GERADOR_FASE_B_TEMPERATURA_FALHA_LEITURA":                                     [12328, 8],
        "GERADOR_FASE_C_TEMPERATURA_FALHA_LEITURA":                                     [12328, 9],
        "GERADOR_NUCLEO_1_TEMPERATURA_FALHA_LEITURA":                                   [12328, 10],
        "GERADOR_NUCLEO_2_TEMPERATURA_FALHA_LEITURA":                                   [12328, 11],
        "GERADOR_NUCLEO_3_TEMPERATURA_FALHA_LEITURA":                                   [12328, 12],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_FALHA_LEITURA":                              [12328, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMPERATURA_FALHA_LEITURA":                         [12328, 14],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_FALHA_LEITURA":                            [12328, 15],


        ## STT_ALARMES_HH_TEMPERATURA
        "TIRISTORES_TEMPERATURA_MUITO_ALTA":                                            [12330, 0],
        "CROWBAR_TEMPERATURA_MUITO_ALTA":                                               [12330, 1],
        "TRAFO_EXCITACAO_TEMPERATURA_MUITO_ALTA":                                       [12330, 2],
        "UHRV_TEMPERATURA_OLEO_MUITO_ALTA":                                             [12330, 3],
        "UHLM_TEMPERATURA_OLEO_MUITO_ALTA":                                             [12330, 4],
        "GERADOR_FASE_A_TEMPERATURA_MUITO_ALTA":                                        [12330, 7],
        "GERADOR_FASE_B_TEMPERATURA_MUITO_ALTA":                                        [12330, 8],
        "GERADOR_FASE_C_TEMPERATURA_MUITO_ALTA":                                        [12330, 9],
        "GERADOR_NUCLEO_1_TEMPERATURA_MUITO_ALTA":                                      [12330, 10],
        "GERADOR_NUCLEO_2_TEMPERATURA_MUITO_ALTA":                                      [12330, 11],
        "GERADOR_NUCLEO_3_TEMPERATURA_MUITO_ALTA":                                      [12330, 12],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_MUITO_ALTA":                                 [12330, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMPERATURA_MUITO_ALTA":                            [12330, 14],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_MUITO_ALTA":                               [12330, 15],


        ## STT_ALARMES_H_TEMPERATURA
        "TIRISTORES_TEMPERATURA_ALTA":                                                  [12332, 0],
        "CROWBAR_TEMPERATURA_ALTA":                                                     [12332, 1],
        "TRAFO_EXCITACAO_TEMPERATURA_ALTA":                                             [12332, 2],
        "UHRV_TEMPERATURA_OLEO_ALTA":                                                   [12332, 3],
        "UHLM_TEMPERATURA_OLEO_ALTA":                                                   [12332, 4],
        "GERADOR_FASE_A_TEMPERATURA_ALTA":                                              [12332, 7],
        "GERADOR_FASE_B_TEMPERATURA_ALTA":                                              [12332, 8],
        "GERADOR_FASE_C_TEMPERATURA_ALTA":                                              [12332, 9],
        "GERADOR_NUCLEO_1_TEMPERATURA_ALTA":                                            [12332, 10],
        "GERADOR_NUCLEO_2_TEMPERATURA_ALTA":                                            [12332, 11],
        "GERADOR_NUCLEO_3_TEMPERATURA_ALTA":                                            [12332, 12],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_ALTA":                                       [12332, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMPERATURA_ALTA":                                  [12332, 14],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_ALTA":                                     [12332, 15],

        ## STT_FALHAS_ANALOGICAS
        "UHRV_PRESSAO_OLEO_FALHA_LEITURA":                                              [12340, 0],
        "SINAL_NIVEL_JUSANTE_FALHA_LEITURA":                                            [12340, 1],

        ## STT_ALARMES_HH_ANALOGICAS
        "UHRV_PRESSAO_OLEO_MUITO_ALTA":                                                 [12342, 0],
        "SINAL_NIVEL_JUSANTE_MUITO_ALTA":                                               [12342, 1],

        ## STT_ALARMES_H_ANALOGICAS
        "UHRV_PRESSAO_OLEO_ALTA":                                                       [12344, 0],
        "SINAL_NIVEL_JUSANTE_ALTA":                                                     [12344, 1],

        ## STT_ALARMES_L_ANALOGICAS
        "UHRV_PRESSAO_OLEO_BAIXA":                                                      [12346, 0],
        "SINAL_NIVEL_JUSANTE_BAIXA":                                                    [12346, 1],

        ## STT_ALARMES_LL_ANALOGICAS
        "UHRV_PRESSAO_OLEO_MUITO_BAIXA":                                                [12348, 0],
        "SINAL_NIVEL_JUSANTE_MUITO_BAIXA":                                              [12348, 1],

        ## LEITURAS_ANALÓGICAS
        "TEMPERATURA_PONTE_TIRISTORES":                                                 12488,
        "TEMPERATURA_CROWBAR":                                                          12490,
        "TEMPERATURA_GERADOR_FASE_A":                                                   12494,
        "TEMPERATURA_GERADOR_FASE_B":                                                   12496,
        "TEMPERATURA_GERADOR_FASE_C":                                                   12498,
        "TEMPERATURA_GERADOR_NUCLEO_1":                                                 12500,
        "TEMPERATURA_GERADOR_NUCLEO_2":                                                 12502,
        "TEMPERATURA_GERADOR_NUCLEO_3":                                                 12504,
        "TEMPERATURA_MANCAL_GUIA_CASQUILHO":                                            12506,
        "TEMPERATURA_MANCAL_COMBINADO_CASQUILHO":                                       12508,
        "TEMPERATURA_MANCAL_COMBINADO_CONTRA_ESCORA":                                   12510,
        "TEMPERATURA_MANCAL_COMBINADO_ESCORA":                                          12512,
        "TEMPERATURA_OLEO_UHLM":                                                        12514,
        "TEMPERATURA_OLEO_UHRV":                                                        12516,
        "PRESSAO_OLEO_UHRV":                                                            12520,
        "NIVEL_JUSANTE":                                                                12522,
        "VIBRACAO_EIXO_X_GUIA":                                                         12524,
        "VIBRACAO_EIXO_X_COMBINADO":                                                    12526,
        "VIBRACAO_EIXO_Y_COMBINADO":                                                    12528,
        "VIBRACAO_EIXO_Z_COMBINADO":                                                    12530,
        "VIBRACAO_EIXO_Y_GUIA":                                                         12532,

        ## BLOQUEIO_86M
        "BLOQUEIO_86M_ATUADO":                                                          [12428, 15],

        ## BLOQUEIO_86E
        "BLOQUEIO_86E_ATUADO":                                                          [12430, 15],

        ## BLOQUEIO_86H
        "BLOQUEIO_86H_ATUADO":                                                          [12432, 15],

        ## STT_BORBOLETA
        "BORBOLETA_FALHA_ABRIR":                                                        [12366, 0],
        "BORBOLETA_FALHA_FECHAR":                                                       [12366, 1],
        "BORBOLETA_ABRINDO":                                                            [12366, 2],
        "BORBOLETA_FECHANDO":                                                           [12366, 3],
        "BYPASS_ABRINDO":                                                               [12366, 4],
        "BYPASS_FECHANDO":                                                              [12366, 5],
        "BYPASS_FALHA_ABRIR":                                                           [12366, 6],
        "BYPASS_FALHA_FECHAR":                                                          [12366, 7],
        "BORBOLETA_DISCREPANCIA_SENSORES":                                              [12366, 10],
        "BYPASS_DISCREPANCIA_SENSORES":                                                 [12366, 11],

        ## SST_ENTRADAS_DIGITAIS_1
        "BOTAO_BLOQUEIO_86EH":                                                          [12310, 0],
        "REARME_FALHAS":                                                                [12310, 1],
        "BOTAO_PARA_UG":                                                                [12310, 2],
        "BOTAO_PARTE_UG":                                                               [12310, 3],
        "BOTAO_DIMINUI_REFERENCIA_RV":                                                  [12310, 4],
        "BOTAO_AUMENTA_REFERENCIA_RV":                                                  [12310, 5],
        "BOTAO_DIMINUI_REFERENCIA_RT":                                                  [12310, 6],
        "BOTAO_AUMENTA_REFERENCIA_RT":                                                  [12310, 7],
        "RELE_PROT_GERADOR_TRIP":                                                       [12310, 8],
        "RELE_PROT_GERADOR_50BF":                                                       [12310, 10],
        "RV_TRIP":                                                                      [12310, 11],
        "RV_ALARME":                                                                    [12310, 12],
        "RV_HABILITADO":                                                                [12310, 13],
        "RV_REGULANDO":                                                                 [12310, 14],
        "RV_POTENCIA_NULA":                                                             [12310, 15],

        "PRTVA_RV_MAQUINA_PARADA":                                                      [12311, 0],
        "PRTVA_RV_VELOCIDADE_MENOR":                                                    [12311, 1],
        "PRTVA_RV_VELOCIDADE_MAIOR":                                                    [12311, 2],
        "PRTVA_RV_DISTRIBUIDOR_ABERTO":                                                 [12311, 3],
        "PRTVA_RT_TRIP":                                                                [12311, 4],
        "PRTVA_RT_ALARME":                                                              [12311, 5],
        "PRTVA_RT_HABILITADO":                                                          [12311, 6],
        "PRTVA_RT_REGULANDO":                                                           [12311, 7],
        "PRTVA_CONTATOR_DE_COMPO_FECHADO":                                              [12311, 8],
        "PRTVA_DISJUNTOR_DE_MAQUINA_FECHADO":                                           [12311, 9],
        "PRTVA_RELE_BLOQUEIO_86EH":                                                     [12311, 10],
        "PRTVA_SUPERVISAO_DE_TENSAO_ENTRADA_CA":                                        [12311, 11],
        "PRTVA_DISPOSITIVO_PROTECAO_DE_SURTO":                                          [12311, 12],
        "PRTVA_UHRV_BOMBA_DEFEITO":                                                     [12311, 13],
        "PRTVA_UHRV_BOMBA_LIGADA":                                                      [12311, 14],
        "PRTVA_UHLM_BOMBA_DEFEITO":                                                     [12311, 15],

        ## SST_ENTRADAS_DIGITAIS_2
        "UHLM_BOMBA_LIGADA":                                                            [12312, 0],
        "UG_RESISTENCIA_AQUEC_GERADOR_DEFEITO":                                         [12312, 3],
        "UG_RESISTENCIA_AQUEC_GERADOR_LIGADA":                                          [12312, 4],
        "DISJUNTOR_TPS_PROTECAO":                                                       [12312, 5],
        "UHRV_OLEO_NIVEL_MUITO_BAIXO":                                                  [12312, 6],
        "UHRV_FILTRO_OLEO_SUJO":                                                        [12312, 7],
        "UHRV_PRESSAO_CRITICA":                                                         [12312, 8],
        "UHRV_PRESSAO_FREIO":                                                           [12312, 9],
        "UHLM_OLEO_NIVEL_MUITO_ALTO":                                                   [12312, 11],
        "UHLM_OLEO_NIVEL_MUITO_BAIXO":                                                  [12312, 12],
        "UHLM_PRESSAO_LINHA_LUBRIFICACAO":                                              [12312, 13],
        "UHLM_FILTRO_OLEO_SUJO":                                                        [12312, 14],
        "UHLM_FLUXO_TROCADOR_DE_CALOR":                                                 [12312, 15],

        "QBAG_ESCOVA_POLO_POSITIVO_DESGASTADA":                                         [12313, 1],
        "QBAG_ESCOVA_POLO_NEGATICO_DESGASTADA":                                         [12313, 2],
        "PSA_BLOQUEIO_86BTBF":                                                          [12313, 3],
        "PSA_POCO_DRENAGEM_NIVEL_MUITO_ALTO":                                           [12313, 4],
        "PSA_FILTRAGEM_PRESSAO_SAIDA":                                                  [12313, 5],
        "PSA_DISJUNTOR_LINHA_FECHADO":                                                  [12313, 6],
        "TPs_PROTECAO_59N_ABERTO":                                                      [12313, 9],
        "VB_VALVULA_BORBOLETA_ABERTA":                                                  [12313, 12],
        "VB_VALVULA_BORBOLETA_FECHADA":                                                 [12313, 13],
        "VB_VALVULA_BYPASS_ABERTA":                                                     [12313, 14],
        "VB_VALVULA_BYPASS_FECHADA":                                                    [12313, 15],

        ## PARTIDA_PARADA
        "STT_PARTIDA_PARADA":                                                           12388,
        "SST_PASSO_SELECIONADO":                                                        12390,
        "STT_PASSO_ATUAL":                                                              12392,

        ## PERMISSIVOS
        "STT_PRE_CONDICOES_GIRO_MECANICO":                                              12408,
        "STT_PRE_CONDICOES_EXCITCAO":                                                   12410,
        "STT_PRE_CONDICOES_SINCRONISMO":                                                12412,

        ## STT_RT
        "RT_FALHA_AO_HABILITAR":                                                        [12374, 0],
        "RT_FALHA_AO_PARTIR":                                                           [12374, 1],
        "RT_FALHA_AO_DESABILITAR":                                                      [12374, 2],

        ## STT_RV
        "RV_FALHA_AO_HABILITAR":                                                        [12372, 0],
        "RV_FALHA_AO_PARTIR":                                                           [12372, 1],
        "RV_FALHA_AO_DESABILITAR":                                                      [12372, 2],
        "RV_FALHA_AO_PARAR_MAQUINA":                                                    [12372, 3],
        "RV_FALHA_AO_FECHAR_DISTRIBUIDOR":                                              [12372, 4],
        "RV_MODO_MANUTENCAO":                                                           [12372, 5],

        ## STT_UNIDADE_GERADORA
        "CONTROLE_POTENCIA_POR_NIVEL_HABILITADO":                                       [12360, 0],
        "CONTROLE_DE_NIVEL_HABILITADO":                                                 [12360, 1],
        "CONTROLE_POTENCIA_MANUAL_HABILITADO":                                          [12360, 2],
        "CONTROLE_PARADA_POR_NIVEL_HABILITADO":                                         [12360, 3],
        "CONTROLE_PARADA_NIVEL_BAIXO":                                                  [12360, 4],
        "CONTROLE_FALHA_SENSOR_NIVEL":                                                  [12360, 5],
        "CONTROLE_ALARME_DIFERENCIAL_DE_GRADE":                                         [12360, 6],
        "CONTROLE_TRIP_DIFERENCIAL_DE_GRADE":                                           [12360, 7],
        "RESISTENCIA_AQUECIMENTO_GERADOR_INDISPONIVEL":                                 [12360, 8],
        "RESISTENCIA_AQUECIMENTO_GERADOR_FALHA_LIGAR":                                  [12360, 9],
        "RESISTENCIA_AQUECIMENTO_GERADOR_FALHA_DESLIGAR":                               [12360, 10],
        "FREIO_FALHA_AO_APLICAR_OU_DESAPLICAR":                                         [12360, 11],

        ## STT_UHLM
        "UHLM_UNIDADE_MANUTENCAO":                                                      [12364, 0],
        "UHLM_BOMBA_1_INDISPONIVEL":                                                    [12364, 2],
        "UHLM_BOMBA_2_INDISPONIVEL":                                                    [12364, 3],
        "UHLM_BOMBA_1_PRINCIPAL":                                                       [12364, 4],
        "UHLM_BOMBA_2_PRINCIPAL":                                                       [12364, 5],
        "UHLM_BOMBA_1_FALHA_AO_LIGAR":                                                  [12364, 6],
        "UHLM_BOMBA_1_FALHA_AO_DESLIGAR":                                               [12364, 7],
        "UHLM_BOMBA_2_FALHA_AO_LIGAR":                                                  [12364, 8],
        "UHLM_BOMBA_2_FALHA_AO_DESLIGAR":                                               [12364, 9],
        "UHLM_BOMBA_1_FALHA_AO_PRESSURIZAR":                                            [12364, 10],
        "UHLM_BOMBA_2_FALHA_AO_PRESSURIZAR":                                            [12364, 11],
        "UHLM_FILTRO_OLEO_SUJO":                                                        [12364, 13],
        "UHLM_FALHA_PRESSOSTATO":                                                       [12364, 14],

        ## STT_UHRV
        "UHRV_UNIDADE_MANUTENCAO":                                                      [12362, 0],
        "UHRV_UNIDADE_HABILITADA":                                                      [12362, 1],
        "UHRV_BOMBA_1_INDISPONIVEL":                                                    [12362, 2],
        "UHRV_BOMBA_2_INDISPONIVEL":                                                    [12362, 3],
        "UHRV_BOMBA_1_PRINCIPAL":                                                       [12362, 4],
        "UHRV_BOMBA_2_PRINCIPAL":                                                       [12362, 5],
        "UHRV_BOMBA_1_FALHA_AO_LIGAR":                                                  [12362, 6],
        "UHRV_BOMBA_1_FALHA_AO_DESLIGAR":                                               [12362, 7],
        "UHRV_BOMBA_2_FALHA_AO_LIGAR":                                                  [12362, 8],
        "UHRV_BOMBA_2_FALHA_AO_DESLIGAR":                                               [12362, 9],
        "UHRV_BOMBA_1_FALHA_AO_PRESSURIZAR":                                            [12362, 10],
        "UHRV_BOMBA_2_FALHA_AO_PRESSURIZAR":                                            [12362, 11],
        "UHRV_FILTRO_OLEO_SUJO":                                                        [12362, 13],
    },

    "UG2": {
        ### COMANDOS
        ## CMD_UG2
        "CMD_REARME_FALHAS":                                                            [12288, 0],
        "CMD_COMANDO_PARADA_DE_EMERGENCIA":                                             [12288, 1],
        "CMD_CONTROLE_NIVEL":                                                           [12288, 2],
        "CMD_CONTROLE_POTENCIA_MANUAL":                                                 [12288, 3],
        "CMD_CONTROLE_POTENCIA_POR_NIVEL":                                              [12288, 4],
        "CMD_PARADA_NIVEL_HABILITA":                                                    [12288, 5],
        "CMD_PARADA_NIVEL_DESABILITA":                                                  [12288, 6],
        "CMD_RV_MANUTENCAO":                                                            [12288, 10],
        "CMD_RV_AUTOMATICO":                                                            [12288, 11],

        # CMD_PARTIDA_PARADA
        "CMD_PARADA_TOTAL":                                                             [12290, 0],
        "CMD_SINCRONISMO":                                                              [12290, 9],

        ## CMD_UHRV
        "CMD_UHRV_MODO_AUTOMATICO":                                                     [12292, 0],
        "CMD_UHRV_MODO_MANUTENCAO":                                                     [12292, 1],
        "CMD_UHRV_BOMBA_1_LIGA":                                                        [12292, 2],
        "CMD_UHRV_BOMBA_1_DESLIGA":                                                     [12292, 3],
        "CMD_UHRV_BOMBA_2_LIGA":                                                        [12292, 4],
        "CMD_UHRV_BOMBA_2_DESLIGA":                                                     [12292, 5],
        "CMD_UHRV_BOMBA_1_PRINCIPAL":                                                   [12292, 6],
        "CMD_UHRV_BOMBA_2_PRINCIPAL":                                                   [12292, 7],

        ## CMD_UHLM
        "CMD_UHLM_MODO_AUTOMATICO":                                                     [12294, 0],
        "CMD_UHLM_MODO_MANUTENCAO":                                                     [12294, 1],
        "CMD_UHLM_BOMBA_1_LIGA":                                                        [12294, 2],
        "CMD_UHLM_BOMBA_1_DESLIGA":                                                     [12294, 3],

        ## COMANDOS_ANALÓGICOS
        # CONTROLE_NÍVEL
        "SETPOINT_NIVEL_5":                                                             12588,
        "SETPOINT_NIVEL_4":                                                             12590,
        "SETPOINT_NIVEL_3":                                                             12592,
        "SETPOINT_NIVEL_2":                                                             12594,
        "SETPOINT_NIVEL_1":                                                             12596,
        "SETPOINT_NIVEL_PARADA":                                                        12598,
        "SETPOINT_POTENCIA_5":                                                          12600,
        "SETPOINT_POTENCIA_4":                                                          12602,
        "SETPOINT_POTENCIA_3":                                                          12604,
        "SETPOINT_POTENCIA_2":                                                          12606,
        "SETPOINT_POTENCIA_1":                                                          12608,
        "SETPOINT_MINIMO_POTENCIA":                                                     12610,
        "SETPOINT_MAXIMO_POTENCIA":                                                     12612,
        "SETPOINT_NIVEL":                                                               12616,


        ### STATUS
        ## STT_FALHAS_TEMPERATURA
        "TIRISTORES_TEMPERATURA_FALHA_LEITURA":                                         [12328, 0],
        "CROWBAR_TEMPERATURA_FALHA_LEITURA":                                            [12328, 1],
        "TRAFO_EXCITACAO_TEMPERATURA_FALHA_LEITURA":                                    [12328, 2],
        "UHRV_TEMPERATURA_OLEO_FALHA_LEITURA":                                          [12328, 3],
        "UHLM_TEMPERATURA_OLEO_FALHA_LEITURA":                                          [12328, 4],
        "GERADOR_FASE_A_TEMPERATURA_FALHA_LEITURA":                                     [12328, 7],
        "GERADOR_FASE_B_TEMPERATURA_FALHA_LEITURA":                                     [12328, 8],
        "GERADOR_FASE_C_TEMPERATURA_FALHA_LEITURA":                                     [12328, 9],
        "GERADOR_NUCLEO_1_TEMPERATURA_FALHA_LEITURA":                                   [12328, 10],
        "GERADOR_NUCLEO_2_TEMPERATURA_FALHA_LEITURA":                                   [12328, 11],
        "GERADOR_NUCLEO_3_TEMPERATURA_FALHA_LEITURA":                                   [12328, 12],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_FALHA_LEITURA":                              [12328, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMPERATURA_FALHA_LEITURA":                         [12328, 14],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_FALHA_LEITURA":                            [12328, 15],


        ## STT_ALARMES_HH_TEMPERATURA
        "TIRISTORES_TEMPERATURA_MUITO_ALTA":                                            [12330, 0],
        "CROWBAR_TEMPERATURA_MUITO_ALTA":                                               [12330, 1],
        "TRAFO_EXCITACAO_TEMPERATURA_MUITO_ALTA":                                       [12330, 2],
        "UHRV_TEMPERATURA_OLEO_MUITO_ALTA":                                             [12330, 3],
        "UHLM_TEMPERATURA_OLEO_MUITO_ALTA":                                             [12330, 4],
        "GERADOR_FASE_A_TEMPERATURA_MUITO_ALTA":                                        [12330, 7],
        "GERADOR_FASE_B_TEMPERATURA_MUITO_ALTA":                                        [12330, 8],
        "GERADOR_FASE_C_TEMPERATURA_MUITO_ALTA":                                        [12330, 9],
        "GERADOR_NUCLEO_1_TEMPERATURA_MUITO_ALTA":                                      [12330, 10],
        "GERADOR_NUCLEO_2_TEMPERATURA_MUITO_ALTA":                                      [12330, 11],
        "GERADOR_NUCLEO_3_TEMPERATURA_MUITO_ALTA":                                      [12330, 12],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_MUITO_ALTA":                                 [12330, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMPERATURA_MUITO_ALTA":                            [12330, 14],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_MUITO_ALTA":                               [12330, 15],


        ## STT_ALARMES_H_TEMPERATURA
        "TIRISTORES_TEMPERATURA_ALTA":                                                  [12332, 0],
        "CROWBAR_TEMPERATURA_ALTA":                                                     [12332, 1],
        "TRAFO_EXCITACAO_TEMPERATURA_ALTA":                                             [12332, 2],
        "UHRV_TEMPERATURA_OLEO_ALTA":                                                   [12332, 3],
        "UHLM_TEMPERATURA_OLEO_ALTA":                                                   [12332, 4],
        "GERADOR_FASE_A_TEMPERATURA_ALTA":                                              [12332, 7],
        "GERADOR_FASE_B_TEMPERATURA_ALTA":                                              [12332, 8],
        "GERADOR_FASE_C_TEMPERATURA_ALTA":                                              [12332, 9],
        "GERADOR_NUCLEO_1_TEMPERATURA_ALTA":                                            [12332, 10],
        "GERADOR_NUCLEO_2_TEMPERATURA_ALTA":                                            [12332, 11],
        "GERADOR_NUCLEO_3_TEMPERATURA_ALTA":                                            [12332, 12],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_ALTA":                                       [12332, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMPERATURA_ALTA":                                  [12332, 14],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_ALTA":                                     [12332, 15],

        ## STT_FALHAS_ANALOGICAS
        "UHRV_PRESSAO_OLEO_FALHA_LEITURA":                                              [12340, 0],
        "SINAL_NIVEL_JUSANTE_FALHA_LEITURA":                                            [12340, 1],

        ## STT_ALARMES_HH_ANALOGICAS
        "UHRV_PRESSAO_OLEO_MUITO_ALTA":                                                 [12342, 0],
        "SINAL_NIVEL_JUSANTE_MUITO_ALTA":                                               [12342, 1],

        ## STT_ALARMES_H_ANALOGICAS
        "UHRV_PRESSAO_OLEO_ALTA":                                                       [12344, 0],
        "SINAL_NIVEL_JUSANTE_ALTA":                                                     [12344, 1],

        ## STT_ALARMES_L_ANALOGICAS
        "UHRV_PRESSAO_OLEO_BAIXA":                                                      [12346, 0],
        "SINAL_NIVEL_JUSANTE_BAIXA":                                                    [12346, 1],

        ## STT_ALARMES_LL_ANALOGICAS
        "UHRV_PRESSAO_OLEO_MUITO_BAIXA":                                                [12348, 0],
        "SINAL_NIVEL_JUSANTE_MUITO_BAIXA":                                              [12348, 1],

        ## LEITURAS_ANALÓGICAS
        "TEMPERATURA_PONTE_TIRISTORES":                                                 12488,
        "TEMPERATURA_CROWBAR":                                                          12490,
        "TEMPERATURA_GERADOR_FASE_A":                                                   12494,
        "TEMPERATURA_GERADOR_FASE_B":                                                   12496,
        "TEMPERATURA_GERADOR_FASE_C":                                                   12498,
        "TEMPERATURA_GERADOR_NUCLEO_1":                                                 12500,
        "TEMPERATURA_GERADOR_NUCLEO_2":                                                 12502,
        "TEMPERATURA_GERADOR_NUCLEO_3":                                                 12504,
        "TEMPERATURA_MANCAL_GUIA_CASQUILHO":                                            12506,
        "TEMPERATURA_MANCAL_COMBINADO_CASQUILHO":                                       12508,
        "TEMPERATURA_MANCAL_COMBINADO_CONTRA_ESCORA":                                   12510,
        "TEMPERATURA_MANCAL_COMBINADO_ESCORA":                                          12512,
        "TEMPERATURA_OLEO_UHLM":                                                        12514,
        "TEMPERATURA_OLEO_UHRV":                                                        12516,
        "PRESSAO_OLEO_UHRV":                                                            12520,
        "NIVEL_JUSANTE":                                                                12522,
        "VIBRACAO_EIXO_X_GUIA":                                                         12524,
        "VIBRACAO_EIXO_X_COMBINADO":                                                    12526,
        "VIBRACAO_EIXO_Y_COMBINADO":                                                    12528,
        "VIBRACAO_EIXO_Z_COMBINADO":                                                    12530,
        "VIBRACAO_EIXO_Y_GUIA":                                                         12532,

        ## BLOQUEIO_86M
        "BLOQUEIO_86M_ATUADO":                                                          [12428, 15],

        ## BLOQUEIO_86E
        "BLOQUEIO_86E_ATUADO":                                                          [12430, 15],

        ## BLOQUEIO_86H
        "BLOQUEIO_86H_ATUADO":                                                          [12432, 15],

        ## STT_BORBOLETA
        "BORBOLETA_FALHA_ABRIR":                                                        [12366, 0],
        "BORBOLETA_FALHA_FECHAR":                                                       [12366, 1],
        "BORBOLETA_ABRINDO":                                                            [12366, 2],
        "BORBOLETA_FECHANDO":                                                           [12366, 3],
        "BYPASS_ABRINDO":                                                               [12366, 4],
        "BYPASS_FECHANDO":                                                              [12366, 5],
        "BYPASS_FALHA_ABRIR":                                                           [12366, 6],
        "BYPASS_FALHA_FECHAR":                                                          [12366, 7],
        "BORBOLETA_DISCREPANCIA_SENSORES":                                              [12366, 10],
        "BYPASS_DISCREPANCIA_SENSORES":                                                 [12366, 11],

        ## SST_ENTRADAS_DIGITAIS_1
        "BOTAO_BLOQUEIO_86EH":                                                          [12310, 0],
        "REARME_FALHAS":                                                                [12310, 1],
        "BOTAO_PARA_UG":                                                                [12310, 2],
        "BOTAO_PARTE_UG":                                                               [12310, 3],
        "BOTAO_DIMINUI_REFERENCIA_RV":                                                  [12310, 4],
        "BOTAO_AUMENTA_REFERENCIA_RV":                                                  [12310, 5],
        "BOTAO_DIMINUI_REFERENCIA_RT":                                                  [12310, 6],
        "BOTAO_AUMENTA_REFERENCIA_RT":                                                  [12310, 7],
        "RELE_PROT_GERADOR_TRIP":                                                       [12310, 8],
        "RELE_PROT_GERADOR_50BF":                                                       [12310, 10],
        "RV_TRIP":                                                                      [12310, 11],
        "RV_ALARME":                                                                    [12310, 12],
        "RV_HABILITADO":                                                                [12310, 13],
        "RV_REGULANDO":                                                                 [12310, 14],
        "RV_POTENCIA_NULA":                                                             [12310, 15],

        "PRTVA_RV_MAQUINA_PARADA":                                                      [12311, 0],
        "PRTVA_RV_VELOCIDADE_MENOR":                                                    [12311, 1],
        "PRTVA_RV_VELOCIDADE_MAIOR":                                                    [12311, 2],
        "PRTVA_RV_DISTRIBUIDOR_ABERTO":                                                 [12311, 3],
        "PRTVA_RT_TRIP":                                                                [12311, 4],
        "PRTVA_RT_ALARME":                                                              [12311, 5],
        "PRTVA_RT_HABILITADO":                                                          [12311, 6],
        "PRTVA_RT_REGULANDO":                                                           [12311, 7],
        "PRTVA_CONTATOR_DE_COMPO_FECHADO":                                              [12311, 8],
        "PRTVA_DISJUNTOR_DE_MAQUINA_FECHADO":                                           [12311, 9],
        "PRTVA_RELE_BLOQUEIO_86EH":                                                     [12311, 10],
        "PRTVA_SUPERVISAO_DE_TENSAO_ENTRADA_CA":                                        [12311, 11],
        "PRTVA_DISPOSITIVO_PROTECAO_DE_SURTO":                                          [12311, 12],
        "PRTVA_UHRV_BOMBA_DEFEITO":                                                     [12311, 13],
        "PRTVA_UHRV_BOMBA_LIGADA":                                                      [12311, 14],
        "PRTVA_UHLM_BOMBA_DEFEITO":                                                     [12311, 15],

        ## SST_ENTRADAS_DIGITAIS_2
        "UHLM_BOMBA_LIGADA":                                                            [12312, 0],
        "UG_RESISTENCIA_AQUEC_GERADOR_DEFEITO":                                         [12312, 3],
        "UG_RESISTENCIA_AQUEC_GERADOR_LIGADA":                                          [12312, 4],
        "DISJUNTOR_TPS_PROTECAO":                                                       [12312, 5],
        "UHRV_OLEO_NIVEL_MUITO_BAIXO":                                                  [12312, 6],
        "UHRV_FILTRO_OLEO_SUJO":                                                        [12312, 7],
        "UHRV_PRESSAO_CRITICA":                                                         [12312, 8],
        "UHRV_PRESSAO_FREIO":                                                           [12312, 9],
        "UHLM_OLEO_NIVEL_MUITO_ALTO":                                                   [12312, 11],
        "UHLM_OLEO_NIVEL_MUITO_BAIXO":                                                  [12312, 12],
        "UHLM_PRESSAO_LINHA_LUBRIFICACAO":                                              [12312, 13],
        "UHLM_FILTRO_OLEO_SUJO":                                                        [12312, 14],
        "UHLM_FLUXO_TROCADOR_DE_CALOR":                                                 [12312, 15],

        "QBAG_ESCOVA_POLO_POSITIVO_DESGASTADA":                                         [12313, 1],
        "QBAG_ESCOVA_POLO_NEGATICO_DESGASTADA":                                         [12313, 2],
        "PSA_BLOQUEIO_86BTBF":                                                          [12313, 3],
        "PSA_POCO_DRENAGEM_NIVEL_MUITO_ALTO":                                           [12313, 4],
        "PSA_FILTRAGEM_PRESSAO_SAIDA":                                                  [12313, 5],
        "PSA_DISJUNTOR_LINHA_FECHADO":                                                  [12313, 6],
        "TPs_PROTECAO_59N_ABERTO":                                                      [12313, 9],
        "VB_VALVULA_BORBOLETA_ABERTA":                                                  [12313, 12],
        "VB_VALVULA_BORBOLETA_FECHADA":                                                 [12313, 13],
        "VB_VALVULA_BYPASS_ABERTA":                                                     [12313, 14],
        "VB_VALVULA_BYPASS_FECHADA":                                                    [12313, 15],

        ## PARTIDA_PARADA
        "STT_PARTIDA_PARADA":                                                           12388,
        "SST_PASSO_SELECIONADO":                                                        12390,
        "STT_PASSO_ATUAL":                                                              12392,

        ## PERMISSIVOS
        "STT_PRE_CONDICOES_GIRO_MECANICO":                                              12408,
        "STT_PRE_CONDICOES_EXCITCAO":                                                   12410,
        "STT_PRE_CONDICOES_SINCRONISMO":                                                12412,

        ## STT_RT
        "RT_FALHA_AO_HABILITAR":                                                        [12374, 0],
        "RT_FALHA_AO_PARTIR":                                                           [12374, 1],
        "RT_FALHA_AO_DESABILITAR":                                                      [12374, 2],

        ## STT_RV
        "RV_FALHA_AO_HABILITAR":                                                        [12372, 0],
        "RV_FALHA_AO_PARTIR":                                                           [12372, 1],
        "RV_FALHA_AO_DESABILITAR":                                                      [12372, 2],
        "RV_FALHA_AO_PARAR_MAQUINA":                                                    [12372, 3],
        "RV_FALHA_AO_FECHAR_DISTRIBUIDOR":                                              [12372, 4],
        "RV_MODO_MANUTENCAO":                                                           [12372, 5],

        ## STT_UNIDADE_GERADORA
        "CONTROLE_POTENCIA_POR_NIVEL_HABILITADO":                                       [12360, 0],
        "CONTROLE_DE_NIVEL_HABILITADO":                                                 [12360, 1],
        "CONTROLE_POTENCIA_MANUAL_HABILITADO":                                          [12360, 2],
        "CONTROLE_PARADA_POR_NIVEL_HABILITADO":                                         [12360, 3],
        "CONTROLE_PARADA_NIVEL_BAIXO":                                                  [12360, 4],
        "CONTROLE_FALHA_SENSOR_NIVEL":                                                  [12360, 5],
        "CONTROLE_ALARME_DIFERENCIAL_DE_GRADE":                                         [12360, 6],
        "CONTROLE_TRIP_DIFERENCIAL_DE_GRADE":                                           [12360, 7],
        "RESISTENCIA_AQUECIMENTO_GERADOR_INDISPONIVEL":                                 [12360, 8],
        "RESISTENCIA_AQUECIMENTO_GERADOR_FALHA_LIGAR":                                  [12360, 9],
        "RESISTENCIA_AQUECIMENTO_GERADOR_FALHA_DESLIGAR":                               [12360, 10],
        "FREIO_FALHA_AO_APLICAR_OU_DESAPLICAR":                                         [12360, 11],

        ## STT_UHLM
        "UHLM_UNIDADE_MANUTENCAO":                                                      [12364, 0],
        "UHLM_BOMBA_1_INDISPONIVEL":                                                    [12364, 2],
        "UHLM_BOMBA_2_INDISPONIVEL":                                                    [12364, 3],
        "UHLM_BOMBA_1_PRINCIPAL":                                                       [12364, 4],
        "UHLM_BOMBA_2_PRINCIPAL":                                                       [12364, 5],
        "UHLM_BOMBA_1_FALHA_AO_LIGAR":                                                  [12364, 6],
        "UHLM_BOMBA_1_FALHA_AO_DESLIGAR":                                               [12364, 7],
        "UHLM_BOMBA_2_FALHA_AO_LIGAR":                                                  [12364, 8],
        "UHLM_BOMBA_2_FALHA_AO_DESLIGAR":                                               [12364, 9],
        "UHLM_BOMBA_1_FALHA_AO_PRESSURIZAR":                                            [12364, 10],
        "UHLM_BOMBA_2_FALHA_AO_PRESSURIZAR":                                            [12364, 11],
        "UHLM_FILTRO_OLEO_SUJO":                                                        [12364, 13],
        "UHLM_FALHA_PRESSOSTATO":                                                       [12364, 14],

        ## STT_UHRV
        "UHRV_UNIDADE_MANUTENCAO":                                                      [12362, 0],
        "UHRV_UNIDADE_HABILITADA":                                                      [12362, 1],
        "UHRV_BOMBA_1_INDISPONIVEL":                                                    [12362, 2],
        "UHRV_BOMBA_2_INDISPONIVEL":                                                    [12362, 3],
        "UHRV_BOMBA_1_PRINCIPAL":                                                       [12362, 4],
        "UHRV_BOMBA_2_PRINCIPAL":                                                       [12362, 5],
        "UHRV_BOMBA_1_FALHA_AO_LIGAR":                                                  [12362, 6],
        "UHRV_BOMBA_1_FALHA_AO_DESLIGAR":                                               [12362, 7],
        "UHRV_BOMBA_2_FALHA_AO_LIGAR":                                                  [12362, 8],
        "UHRV_BOMBA_2_FALHA_AO_DESLIGAR":                                               [12362, 9],
        "UHRV_BOMBA_1_FALHA_AO_PRESSURIZAR":                                            [12362, 10],
        "UHRV_BOMBA_2_FALHA_AO_PRESSURIZAR":                                            [12362, 11],
        "UHRV_FILTRO_OLEO_SUJO":                                                        [12362, 13],
    },
}

REG_RTV = {
    "UG1":{
        ### RV
        ## LEITURAS_1
        "RV_ROTACAO":                                                                          16,
        "RV_ESTADO_OPERACAO":                                                                  21,
        "RV_CONTROLE_SINCRONIZADO_SELECIONADO":                                                22,
        "RV_CONTROLE_VAZIO_SELECIONADO":                                                       23,
        "RV_COMANDO_MODBUS":                                                                   24,

        ## ENTRADAS_DIGITAIS
        "RV_ED_SEM_BLOQUEIO_EXTERNO":                                                       [25, 0],
        "RV_ED_HABILITA_REGULADOR":                                                         [25, 1],
        "RV_ED_SELECIONA_MODO_CONTROLE_ISOLADO":                                            [25, 2],
        "RV_ED_ZERA_CARGA":                                                                 [25, 3],
        "RV_ED_RESET_FALHAS":                                                               [25, 4],
        "RV_ED_INCREMENTA_REFERENCIA_CONTROLE":                                             [25, 5],
        "RV_ED_DECREMENTA_REFERENCIA_CONTROLE":                                             [25, 6],
        "RV_ED_DISJUNTOR_MAQUINA_FECHADO":                                                  [25, 7],
        "RV_ED_PROGRAMAVEL_1":                                                              [25, 8],
        "RV_ED_PROGRAMAVEL_2":                                                              [25, 9],
        "RV_ED_PROGRAMAVEL_3":                                                              [25, 10],
        "RV_ED_PROGRAMAVEL_4":                                                              [25, 11],

        ## SAÍDAS_DIGITAIS
        "RV_SD_RELE_TRIP_NAO_ATUADO":                                                       [26, 0],
        "RV_SD_RELE_ALARME":                                                                [26, 1],
        "RV_SD_RELE_REGULADOR_HABILITADO":                                                  [26, 2],
        "RV_SD_RELE_REGULADOR_REGULANDO":                                                   [26, 3],
        "RV_SD_RELE_POTENCIA_NULA":                                                         [26, 4],
        "RV_SD_RELE_MAQUINA_PARADA":                                                        [26, 5],
        "RV_SD_RELE_VELOCIDADE_MENOR_30_POR_CENTO":                                         [26, 6],
        "RV_SD_RELE_VELOCIDADE_MAIOR_90_POR_CENTO":                                         [26, 7],
        "RV_SD_RELE_DISTRIBUIDOR_ABERTO":                                                   [26, 8],
        "RV_SD_RELE_SAIDA_PROGRAMAVEL_":                                                    [26, 9],
        "RV_SD_SEGUIDOR_1":                                                                 [26, 10],
        "RV_SD_SEGUIDOR_2":                                                                 [26, 11],

        ## LIMITES_OPERAÇÃO
        "RV_LIMITADOR_SUPERIOR_DISTRIBUIDOR_ATUADO":                                        [27, 0],
        "RV_LIMITADOR_INFERIOR_DISTRIBUIDOR_ATUADO":                                        [27, 1],
        "RV_LIMITADOR_SUPERIOR_ROTOR_ATUADO":                                               [27, 2],
        "RV_LIMITADOR_INFERIOR_ROTOR_ATUADO":                                               [27, 3],
        "RV_LIMITADOR_SUPERIOR_VELOCIDADE_ATUADO":                                          [27, 4],
        "RV_LIMITADOR_INFERIOR_VELOCIDADE_ATUADO":                                          [27, 5],
        "RV_LIMITADOR_SUPERIOR_POTENCIA_ATUADO":                                            [27, 6],
        "RV_LIMITADOR_INFERIOR_POTENCIA_ATUADO":                                            [27, 7],

        ## LEITURAS_2
        "RV_SETPOINT_ABERTURA_PU":                                                             28,
        "RV_SETPOINT_VELOCIDADE":                                                              29,
        "RV_SETPOINT_POTENCIA_ATIVA_KW":                                                       30,
        "RV_SETPOINT_POTENCIA_ATIVA_PU":                                                       30,
        "RV_SAIDA_CONTROLE_DISTRIBUIDOR":                                                      32,
        "RV_SAIDA_CONTROLE_ROTOR":                                                             33,
        "RV_REFERENCIA_DISTRIBUIDOR_PU":                                                       36,
        "RV_FEEDBACK_DISTRIBUIDOR_PU":                                                         37,
        "RV_SAIDA_CONTROLE_DISTRIBUIDOR_PU":                                                   32,
        "RV_REFERENCIA_ROTOR_PU":                                                              42,
        "RV_FEEDBACK_ROTOR_PU":                                                                43,
        "RV_SAIDA_CONTROLE_ROTOR_PU":                                                          33,
        "RV_REFERENCIA_VELOCIDADE_PU":                                                         48,
        "RV_FEEDBACK_VELOCIDADE_PU":                                                           49,
        "RV_REFERENCIA_POTENCIA_ATIVA_PU":                                                     54,
        "RV_FEEDBACK_POTENCIA_ATIVA_PU":                                                       55,

        ## ALARME
        "RV_ALARME_SOBREFREQUENCIA":                                                        [66, 0],
        "RV_ALARME_SUBFREQUENCIA":                                                          [66, 1],
        "RV_ALARME_LEITURA_POSICAO_DISTRIBUIDOR":                                           [66, 2],
        "RV_ALARME_LEITURA_POSICAO_ROTOR":                                                  [66, 3],
        "RV_ALARME_LEITURA_POTENCIA_ATIVA":                                                 [66, 4],
        "RV_ALARME_LEITURA_REFERENCIA_POTENCIA":                                            [66, 5],
        "RV_ALARME_LEITURA_NIVEL_MONTANTE":                                                 [66, 6],
        "RV_ALARME_NIVEL_MONTANTE_MUITO_BAIXO":                                             [66, 7],
        "RV_ALARME_CONTROLE_POSICAO_DISTRIBUIDOR":                                          [66, 8],
        "RV_ALARME_CONTROLE_POSICAO_ROTOR":                                                 [66, 9],
        "RV_ALARME_RUIDO_MEDICAO_VELOCIDADE_PRINCIPAL":                                     [66, 10],
        "RV_ALARME_RUIDO_MEDICAO_VELOCIDADE_RETAGUARDA":                                    [66, 11],
        "RV_ALARME_PERDA_MEDICAO_VELOCIDADE_PRINCIPAL":                                     [66, 12],
        "RV_ALARME_PERDA_MEDICAO_VELOCIDADE_RETAGUARDA":                                    [66, 13],
        "RV_ALARME_DIFERENCA_MEDICAO_VELOCIDADE_PRINCIPAL_RETAGUARDA":                      [66, 14],

        ## FALHA_1
        "RV_FALHA_SOBREFREQUENCIA_INSTANTANEA":                                             [67, 0],
        "RV_FALHA_SOBREFREQUENCIA_TEMPORIZADA":                                             [67, 1],
        "RV_FALHA_SUBFREQUENCIA_TEMPORIZADA":                                               [67, 2],
        "RV_FALHA_GIRANDO_SEM_REGULACAO_OU_GIRO_INDEVIDO":                                  [67, 3],
        "RV_FALHA_LEITURA_POSICAO_DISTRIBUIDOR":                                            [67, 4],
        "RV_FALHA_LEITURA_POSICAO_ROTOR":                                                   [67, 5],
        "RV_FALHA_LEITURA_POTENCIA_ATIVA":                                                  [67, 6],
        "RV_FALHA_LEITURA_REFERENCIA_POTENCIA":                                             [67, 7],
        "RV_FALHA_LEITURA_NIVEL_MONTANTE":                                                  [67, 8],
        "RV_FALHA_NIVEL_MONTANTE_MUITO_BAIXO":                                              [67, 10],
        "RV_FALHA_CONTROLE_POSICAO_DISTRIBUIDOR":                                           [67, 11],
        "RV_FALHA_CONTROLE_POSICAO_ROTOR":                                                  [67, 12],
        "RV_FALHA_RUIDO_MEDICAO_VELOCIDADE_PRINCIPAL":                                      [67, 13],
        "RV_FALHA_RUIDO_MEDICAO_VELOCIDADE_RETAGUARDA":                                     [67, 14],
        "RV_FALHA_PERDA_MEDICAO_VELOCIDADE_PRINCIPAL":                                      [67, 15],

        ## FALHA_2
        "RV_FALHA_PERDA_MEDICAO_VELOCIDADE_RETAGUARDA":                                     [68, 0],
        "RV_FALHA_TEMPO_EXCESSIVO_PARTIDA":                                                 [68, 1],
        "RV_FALHA_TEMPO_EXCESSIVO_PARADA":                                                  [68, 2],
        "RV_FALHA_BLOQUEIO_EXTERNO":                                                        [68, 3],
        "RV_FALHA_DIFERENCA_MEDICAO_VELOCIDADE_PRINCIPAL_E_RETAGUARDA":                     [68, 4],

        ## LEITURAS_3
        "RV_POTENCIA_APARENTE_NOMINAL":                                                        79,
        "RV_POTENCIA_ATIVA_NOMINAL":                                                           80,
        "RV_CONTROLE_1":                                                                       85,
        "RV_CONTROLE_2":                                                                       86,
        "RV_CONJUGADO_DISTRIBUIDOR_1":                                                         121,
        "RV_CONJUGADO_ROTOR_1":                                                                122,
        "RV_CONJUGADO_DISTRIBUIDOR_2":                                                         123,
        "RV_CONJUGADO_ROTOR_2":                                                                124,
        "RV_CONJUGADO_DISTRIBUIDOR_3":                                                         125,
        "RV_CONJUGADO_ROTOR_3":                                                                126,
        "RV_CONJUGADO_DISTRIBUIDOR_4":                                                         127,
        "RV_CONJUGADO_ROTOR_4":                                                                128,
        "RV_CONJUGADO_DISTRIBUIDOR_5":                                                         129,
        "RV_CONJUGADO_ROTOR_5":                                                                130,
        "RV_CONJUGADO_DISTRIBUIDOR_6":                                                         131,
        "RV_CONJUGADO_ROTOR_6":                                                                132,
        "RV_CONJUGADO_DISTRIBUIDOR_7":                                                         133,
        "RV_CONJUGADO_ROTOR_7":                                                                134,
        "RV_CONJUGADO_DISTRIBUIDOR_8":                                                         135,
        "RV_CONJUGADO_ROTOR_8":                                                                136,
        "RV_CONJUGADO_DISTRIBUIDOR_9":                                                         137,
        "RV_CONJUGADO_ROTOR_9":                                                                138,
        "RV_CONJUGADO_DISTRIBUIDOR_10":                                                        139,
        "RV_CONJUGADO_ROTOR_10":                                                               140,
        "RV_ABERTURA_MAXIMA_DISTRIBUIDOR":                                                     182,
        "RV_ABERTURA_MAXIMA_DISTRIBUIDOR_A_VAZIO":                                             184,
        "RV_ABERTURA_MINIMA_DISTRIBUIDOR":                                                     183,
        "RV_ABERTURA_MAXIMA_ROTOR":                                                            185,
        "RV_ABERTURA_MINIMA_ROTOR":                                                            186,
        "RV_POTENCIA_MAXIMA":                                                                  189,
        "RV_POTENCIA_MINIMA":                                                                  190,


        ### RT
        ## LEITURAS_1
        "RT_CORRENTE_EXCITACAO":                                                               16,
        "RT_TENSAO_EXCITACAO":                                                                 17,
        "RT_TEMPERATURA_ROTOR":                                                                25,
        "RT_ESTADO_OPERACAO":                                                                  26,
        "RT_CONTROLE_SINCRONIZADO_SELECIONADO":                                                27,

        ## ENTRADAS_DIGITAIS
        "RT_ED_SEM_BLOQUEIO_EXTERNO":                                                       [30, 0],
        "RT_ED_HABILITA_REGULADOR":                                                         [30, 1],
        "RT_ED_SELECIONA_MODO_CONTROLE_ISOLADO":                                            [30, 2],
        "RV_ED_DRIVE_EXCITACAO_HABILITADO_LOGICA_DE_DISPARO":                               [30, 3],
        "RV_ED_RESET_FALHAS":                                                               [30, 4],
        "RT_ED_INCREMENTA_REFERENCIA_CONTROLE":                                             [30, 5],
        "RT_ED_DECREMENTA_REFERENCIA_CONTROLE":                                             [30, 6],
        "RT_ED_DISJUNTOR_MAQUINA_FECHADO":                                                  [30, 7],
        "RT_ED_CONTATOR_CAMPO_FECHADO":                                                     [30, 8],
        "RT_ED_CROWBAR_INATIVO":                                                            [30, 9],
        "RT_ED_PROGRAMAVEL_1":                                                              [30, 10],
        "RT_ED_PROGRAMAVEL_2":                                                              [30, 11],

        ## SAIDAS_DIGITAIS
        "RT_SD_RELE_TRIP_NAO_ATUADO":                                                       [31, 0],
        "RT_SD_RELE_ALARME":                                                                [31, 1],
        "RT_SD_RELE_REGULADOR_HABILITADO":                                                  [31, 2],
        "RT_SD_RELE_REGULADOR_REGULANDO":                                                   [31, 3],
        "RT_SD_RELE_HABILITA_DRIVE_EXCITACAO_LOGICA_DISPARO":                               [31, 4],
        "RT_SD_RELE_HABILITA_CONTATOR_CAMPO":                                               [31, 5],
        "RT_SD_RELE_HABILITA_PRE_EXCITACAO":                                                [31, 6],
        "RT_SD_RELE_HABILITA_CROWBAR":                                                      [31, 7],
        "RT_SD_RELE_SAIDA_PROGRAMAVEL_1":                                                   [31, 8],
        "RT_SD_RELE_SAIDA_PROGRAMAVEL_2":                                                   [31, 9],
        "RT_SD_SEGUIDOR_1":                                                                 [31, 10],
        "RT_SD_SEGUIDOR_2":                                                                 [31, 11],

        ## LIMITES_OPERAÇÃO
        "RT_LIMITADOR_SUPERIOR_CORRENTE_EXCITACAO":                                         [31, 0],
        "RT_LIMITADOR_INFERIOR_CORRENTE_EXCITACAO":                                         [31, 1],
        "RT_LIMITADOR_SUPERIOR_TENSAO_TERMINAL":                                            [31, 2],
        "RT_LIMITADOR_INFERIOR_TENSAO_TERMINAL":                                            [31, 3],
        "RT_LIMITADOR_SUPERIOR_POTENCIA_REATIVA":                                           [31, 4],
        "RT_LIMITADOR_INFERIOR_POTENCIA_REATIVA":                                           [31, 5],
        "RT_LIMITADOR_SUPERIOR_FATOR_DE_POTENCIA":                                          [31, 10],
        "RT_LIMITADOR_INFERIOR_FATOR_DE_POTENCIA":                                          [31, 11],
        "RT_LIMITADOR_VOLTZ_HERTZ":                                                         [31, 12],
        "RT_LIMITADOR_ABERTURA_PONTE":                                                      [31, 13],
        "RT_LIMITADOR_PQ_RELACAO_POTENCIA_ATIVA_X_POTENCIA_REATIVA":                        [31, 14],

        ## LEITURAS_2
        "RT_SETPOINT_TENSAO_PU":                                                               40,
        "RT_SETPOINT_POTENCIA_REATIVA_KVAR":                                                   41,
        "RT_SETPOINT_POTENCIA_REATIVA_PU":                                                     41,
        "RT_SETPOINT_FATOR_POTENCIA_PU":                                                       42,
        "RT_ABERTURA_PONTE":                                                                   43,
        "RT_REFERENCIA_CORRENTE_CAMPO_PU":                                                     46,
        "RT_FEEDBACK_CORRENTE_CAMPO_PU":                                                       47,
        "RT_REFERENCIA_TENSAO_PU":                                                             52,
        "RT_FEEDBACK_TENSAO_PU":                                                               53,
        "RT_REFERENCIA_POTENCIA_REATIVA_PU":                                                   58,
        "RT_FEEDBACK_POTENCIA_REATIVA_PU":                                                     59,
        "RT_REFERENCIA_FATOR_POTENCIA_PU":                                                     64,
        "RT_FEEDBACK_FATOR_POTENCIA_PU":                                                       65,

        ## ALARMES_1
        "RT_ALARME_SOBRETENSAO":                                                            [70, 0],
        "RT_ALARME_SUBTENSAO":                                                              [70, 1],
        "RT_ALARME_SOBREFREQUENCIA":                                                        [70, 2],
        "RT_ALARME_SUBFREQUENCIA":                                                          [70, 3],
        "RT_ALARME_LIMITE_SUPERIOR_POTENCIA_REATIVA":                                       [70, 4],
        "RT_ALARME_LIMITE_INFERIOR_POTENCIA_REATIVA":                                       [70, 5],
        "RT_ALARME_LIMITE_SUPERIOR_FATOR_DE_POTENCIA":                                      [70, 6],
        "RT_ALARME_LIMITE_INFERIOR_FATOR_DE_POTENCIA":                                      [70, 7],
        "RT_ALARME_VARIACAO_DE_TENSAO":                                                     [70, 8],
        "RT_ALARME_POTENCIA_ATIVA_REVERSA":                                                 [70, 9],
        "RT_ALARME_SOBRECORRENTE_TERMINAL":                                                 [70, 10],
        "RT_ALARME_LIMITE_SUPERIOR_CORRENTE_EXCITACAO":                                     [70, 11],
        "RT_ALARME_LIMITE_INFERIOR_CORRENTE_EXCITACAO":                                     [70, 12],
        "RT_ALARME_TEMPERATURA_MUITO_ALTA_ROTOR":                                           [70, 13],
        "RT_ALARME_PRESENCA_DE_TENSAO_TERMINAL_COM_AUSENCIA_DE_CORRENTE_DE_EXCITACAO":      [70, 14],
        "RT_ALARME_PRESENCA_DE_CORRENTE_DE_EXCITACAO_COM_AUXENCIA_DE_TENSAO_TERMINAL":      [70, 15],

        ## ALARMES_2
        "RT_ALARME_FALHA_CONTROLE_CORRENTE_EXCITACAO":                                      [71, 0],
        "RT_ALARME_FALHA_CONTROLE_TENSAO_TERMINAL":                                         [71, 1],
        "RT_ALARME_CROWBAR_ATUADO_COM_REGULADOR_HABILITADO":                                [71, 2],
        "RT_ALARME_FALHA_HABILITAR_DRIVE_DE_EXCITACAO":                                     [71, 3],
        "RT_ALARME_FALHA_FECHAR_CONTATOR_DE_CAMPO":                                         [71, 4],
        "RT_ALARME_FALHA_DE_CORRENTE_DE_EXCITACAO_COM_PRE_EXCITACAO_ATIVA":                 [71, 5],
        "RT_ALARME_PERDA_MEDICAO_POTENCIA_REATIVA":                                         [71, 6],
        "RT_ALARME_PERDA_MEDICAO_TENSAO_TERMINAL":                                          [71, 7],
        "RT_ALARME_PERDA_MEDICAO_CORRENTE_EXCITACAO":                                       [71, 8],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_REATIVO":                                        [71, 9],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_TENSAO":                                         [71, 10],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_PRINCIPAL":                            [71, 11],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_RETAGUARDA":                           [71, 12],

        ## FALHAS_1
        "RT_FALHA_SOBRETENSAO":                                                             [71, 0],
        "RT_FALHA_SUBTENSAO":                                                               [71, 1],
        "RT_FALHA_SOBREFREQUENCIA":                                                         [71, 2],
        "RT_FALHA_SUBFREQUENCIA":                                                           [71, 3],
        "RT_FALHA_LIMITE_SUPERIOR_POTENCIA_REATIVA":                                        [71, 4],
        "RT_FALHA_LIMITE_INFERIOR_POTENCIA_REATIVA":                                        [71, 5],
        "RT_FALHA_LIMITE_SUPERIOR_FATOR_DE_POTENCIA":                                       [71, 6],
        "RT_FALHA_LIMITE_INFERIOR_FATOR_DE_POTENCIA":                                       [71, 7],
        "RT_FALHA_SOBRETENSAO_INSTANTANEA":                                                 [71, 8],
        "RT_FALHA_VARIACAO_DE_TENSAO":                                                      [71, 9],
        "RT_FALHA_POTENCIA_ATIVA_REVERSA":                                                  [71, 10],
        "RT_FALHA_SOBRECORRENTE_TERMINAL":                                                  [71, 11],
        "RT_FALHA_LIMITE_SUPERIOR_CORRENTE_EXCITACAO":                                      [71, 12],
        "RT_FALHA_LIMITE_INFERIOR_CORRENTE_EXCITACAO":                                      [71, 13],
        "RT_FALHA_LIMITE_SUPERIOR_TENSAO_EXCITACAO":                                        [71, 14],
        "RT_FALHA_LIMITE_INFERIOR_TENSAO_EXCITACAO":                                        [71, 15],

        ## FALHAS_2
        "RT_FALHA_TEMPERATURA_MUITO_ALTA_ROTOR":                                            [73, 0],
        "RT_FALHA_PRESENCA_DE_TENSAO_TERMINAL_COM_AUSENCIA_DE_CORRENTE_DE_EXCITACAO":       [73, 1],
        "RT_FALHA_PRESENCA_DE_CORRENTE_DE_EXCITACAO_COM_AUXENCIA_DE_TENSAO_TERMINAL":       [73, 2],
        "RT_FALHA_FALHA_CONTROLE_CORRENTE_EXCITACAO":                                       [73, 3],
        "RT_FALHA_FALHA_CONTROLE_TENSAO_TERMINAL":                                          [73, 4],
        "RT_FALHA_CROWBAR_ATUADO_COM_REGULADOR_HABILITADO":                                 [73, 5],
        "RT_FALHA_FALHA_HABILITAR_DRIVE_DE_EXCITACAO_LOGICA_DE_DISPARO":                    [73, 6],
        "RT_ALAME_FALHA_FECHAR_CONTATOR_DE_CAMPO":                                          [73, 7],
        "RT_FALHA_FALHA_DE_CORRENTE_DE_EXCITACAO_COM_PRE_EXCITACAO_ATIVA":                  [73, 8],
        "RT_FALHA_TEMPO_EXCESSIVO_DE_PRE_EXCITACAO":                                        [73, 9],
        "RT_FALHA_TEMPO_EXCESSIVO_DE_PARADA":                                               [73, 10],
        "RT_FALHA_TEMPO_EXCESSIVO_DE_PARTIDA":                                              [73, 11],
        "RT_FALHA_BLOQUEIO_EXTERNO":                                                        [73, 12],

        ## FALHAS_3
        "RT_FALHA_PERDA_MEDICAO_POTENCIA_REATIVA":                                          [74, 0],
        "RT_FALHA_PERDA_MEDICAO_TENSAO_TERMINAL":                                           [74, 1],
        "RT_FALHA_PERDA_MEDICAO_CORRENTE_EXCITACAO_PRINCIPAL":                              [74, 2],
        "RT_FALHA_PERDA_MEDICAO_CORRENTE_EXCITACAO_RETAGUARDA":                             [74, 3],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_REATIVO":                                         [74, 4],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_TENSAO":                                          [74, 5],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_PRINCIPAL":                             [74, 6],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_RETAGUARDA":                            [74, 7],

        ## LEITURAS_3
        "RT_TENSAO_NOMINAL":                                                                   85,
        "RT_POTENCIA_APARENTE_NOMINAL":                                                        86,
        "RT_CONTROLE_1":                                                                       90,
        "RT_CONTROLE_2":                                                                       91,
    },

    "UG2":{
        ### RV
        ## LEITURAS_1
        "RV_ROTACAO":                                                                          16,
        "RV_ESTADO_OPERACAO":                                                                  21,
        "RV_CONTROLE_SINCRONIZADO_SELECIONADO":                                                22,
        "RV_CONTROLE_VAZIO_SELECIONADO":                                                       23,
        "RV_COMANDO_MODBUS":                                                                   24,

        ## ENTRADAS_DIGITAIS
        "RV_ED_SEM_BLOQUEIO_EXTERNO":                                                       [25, 0],
        "RV_ED_HABILITA_REGULADOR":                                                         [25, 1],
        "RV_ED_SELECIONA_MODO_CONTROLE_ISOLADO":                                            [25, 2],
        "RV_ED_ZERA_CARGA":                                                                 [25, 3],
        "RV_ED_RESET_FALHAS":                                                               [25, 4],
        "RV_ED_INCREMENTA_REFERENCIA_CONTROLE":                                             [25, 5],
        "RV_ED_DECREMENTA_REFERENCIA_CONTROLE":                                             [25, 6],
        "RV_ED_DISJUNTOR_MAQUINA_FECHADO":                                                  [25, 7],
        "RV_ED_PROGRAMAVEL_1":                                                              [25, 8],
        "RV_ED_PROGRAMAVEL_2":                                                              [25, 9],
        "RV_ED_PROGRAMAVEL_3":                                                              [25, 10],
        "RV_ED_PROGRAMAVEL_4":                                                              [25, 11],

        ## SAÍDAS_DIGITAIS
        "RV_SD_RELE_TRIP_NAO_ATUADO":                                                       [26, 0],
        "RV_SD_RELE_ALARME":                                                                [26, 1],
        "RV_SD_RELE_REGULADOR_HABILITADO":                                                  [26, 2],
        "RV_SD_RELE_REGULADOR_REGULANDO":                                                   [26, 3],
        "RV_SD_RELE_POTENCIA_NULA":                                                         [26, 4],
        "RV_SD_RELE_MAQUINA_PARADA":                                                        [26, 5],
        "RV_SD_RELE_VELOCIDADE_MENOR_30_POR_CENTO":                                         [26, 6],
        "RV_SD_RELE_VELOCIDADE_MAIOR_90_POR_CENTO":                                         [26, 7],
        "RV_SD_RELE_DISTRIBUIDOR_ABERTO":                                                   [26, 8],
        "RV_SD_RELE_SAIDA_PROGRAMAVEL_":                                                    [26, 9],
        "RV_SD_SEGUIDOR_1":                                                                 [26, 10],
        "RV_SD_SEGUIDOR_2":                                                                 [26, 11],

        ## LIMITES_OPERAÇÃO
        "RV_LIMITADOR_SUPERIOR_DISTRIBUIDOR_ATUADO":                                        [27, 0],
        "RV_LIMITADOR_INFERIOR_DISTRIBUIDOR_ATUADO":                                        [27, 1],
        "RV_LIMITADOR_SUPERIOR_ROTOR_ATUADO":                                               [27, 2],
        "RV_LIMITADOR_INFERIOR_ROTOR_ATUADO":                                               [27, 3],
        "RV_LIMITADOR_SUPERIOR_VELOCIDADE_ATUADO":                                          [27, 4],
        "RV_LIMITADOR_INFERIOR_VELOCIDADE_ATUADO":                                          [27, 5],
        "RV_LIMITADOR_SUPERIOR_POTENCIA_ATUADO":                                            [27, 6],
        "RV_LIMITADOR_INFERIOR_POTENCIA_ATUADO":                                            [27, 7],

        ## LEITURAS_2
        "RV_SETPOINT_ABERTURA_PU":                                                             28,
        "RV_SETPOINT_VELOCIDADE":                                                              29,
        "RV_SETPOINT_POTENCIA_ATIVA_KW":                                                       30,
        "RV_SETPOINT_POTENCIA_ATIVA_PU":                                                       30,
        "RV_SAIDA_CONTROLE_DISTRIBUIDOR":                                                      32,
        "RV_SAIDA_CONTROLE_ROTOR":                                                             33,
        "RV_REFERENCIA_DISTRIBUIDOR_PU":                                                       36,
        "RV_FEEDBACK_DISTRIBUIDOR_PU":                                                         37,
        "RV_SAIDA_CONTROLE_DISTRIBUIDOR_PU":                                                   32,
        "RV_REFERENCIA_ROTOR_PU":                                                              42,
        "RV_FEEDBACK_ROTOR_PU":                                                                43,
        "RV_SAIDA_CONTROLE_ROTOR_PU":                                                          33,
        "RV_REFERENCIA_VELOCIDADE_PU":                                                         48,
        "RV_FEEDBACK_VELOCIDADE_PU":                                                           49,
        "RV_REFERENCIA_POTENCIA_ATIVA_PU":                                                     54,
        "RV_FEEDBACK_POTENCIA_ATIVA_PU":                                                       55,

        ## ALARME
        "RV_ALARME_SOBREFREQUENCIA":                                                        [66, 0],
        "RV_ALARME_SUBFREQUENCIA":                                                          [66, 1],
        "RV_ALARME_LEITURA_POSICAO_DISTRIBUIDOR":                                           [66, 2],
        "RV_ALARME_LEITURA_POSICAO_ROTOR":                                                  [66, 3],
        "RV_ALARME_LEITURA_POTENCIA_ATIVA":                                                 [66, 4],
        "RV_ALARME_LEITURA_REFERENCIA_POTENCIA":                                            [66, 5],
        "RV_ALARME_LEITURA_NIVEL_MONTANTE":                                                 [66, 6],
        "RV_ALARME_NIVEL_MONTANTE_MUITO_BAIXO":                                             [66, 7],
        "RV_ALARME_CONTROLE_POSICAO_DISTRIBUIDOR":                                          [66, 8],
        "RV_ALARME_CONTROLE_POSICAO_ROTOR":                                                 [66, 9],
        "RV_ALARME_RUIDO_MEDICAO_VELOCIDADE_PRINCIPAL":                                     [66, 10],
        "RV_ALARME_RUIDO_MEDICAO_VELOCIDADE_RETAGUARDA":                                    [66, 11],
        "RV_ALARME_PERDA_MEDICAO_VELOCIDADE_PRINCIPAL":                                     [66, 12],
        "RV_ALARME_PERDA_MEDICAO_VELOCIDADE_RETAGUARDA":                                    [66, 13],
        "RV_ALARME_DIFERENCA_MEDICAO_VELOCIDADE_PRINCIPAL_RETAGUARDA":                      [66, 14],

        ## FALHA_1
        "RV_FALHA_SOBREFREQUENCIA_INSTANTANEA":                                             [67, 0],
        "RV_FALHA_SOBREFREQUENCIA_TEMPORIZADA":                                             [67, 1],
        "RV_FALHA_SUBFREQUENCIA_TEMPORIZADA":                                               [67, 2],
        "RV_FALHA_GIRANDO_SEM_REGULACAO_OU_GIRO_INDEVIDO":                                  [67, 3],
        "RV_FALHA_LEITURA_POSICAO_DISTRIBUIDOR":                                            [67, 4],
        "RV_FALHA_LEITURA_POSICAO_ROTOR":                                                   [67, 5],
        "RV_FALHA_LEITURA_POTENCIA_ATIVA":                                                  [67, 6],
        "RV_FALHA_LEITURA_REFERENCIA_POTENCIA":                                             [67, 7],
        "RV_FALHA_LEITURA_NIVEL_MONTANTE":                                                  [67, 8],
        "RV_FALHA_NIVEL_MONTANTE_MUITO_BAIXO":                                              [67, 10],
        "RV_FALHA_CONTROLE_POSICAO_DISTRIBUIDOR":                                           [67, 11],
        "RV_FALHA_CONTROLE_POSICAO_ROTOR":                                                  [67, 12],
        "RV_FALHA_RUIDO_MEDICAO_VELOCIDADE_PRINCIPAL":                                      [67, 13],
        "RV_FALHA_RUIDO_MEDICAO_VELOCIDADE_RETAGUARDA":                                     [67, 14],
        "RV_FALHA_PERDA_MEDICAO_VELOCIDADE_PRINCIPAL":                                      [67, 15],

        ## FALHA_2
        "RV_FALHA_PERDA_MEDICAO_VELOCIDADE_RETAGUARDA":                                     [68, 0],
        "RV_FALHA_TEMPO_EXCESSIVO_PARTIDA":                                                 [68, 1],
        "RV_FALHA_TEMPO_EXCESSIVO_PARADA":                                                  [68, 2],
        "RV_FALHA_BLOQUEIO_EXTERNO":                                                        [68, 3],
        "RV_FALHA_DIFERENCA_MEDICAO_VELOCIDADE_PRINCIPAL_E_RETAGUARDA":                     [68, 4],

        ## LEITURAS_3
        "RV_POTENCIA_APARENTE_NOMINAL":                                                        79,
        "RV_POTENCIA_ATIVA_NOMINAL":                                                           80,
        "RV_CONTROLE_1":                                                                       85,
        "RV_CONTROLE_2":                                                                       86,
        "RV_CONJUGADO_DISTRIBUIDOR_1":                                                         121,
        "RV_CONJUGADO_ROTOR_1":                                                                122,
        "RV_CONJUGADO_DISTRIBUIDOR_2":                                                         123,
        "RV_CONJUGADO_ROTOR_2":                                                                124,
        "RV_CONJUGADO_DISTRIBUIDOR_3":                                                         125,
        "RV_CONJUGADO_ROTOR_3":                                                                126,
        "RV_CONJUGADO_DISTRIBUIDOR_4":                                                         127,
        "RV_CONJUGADO_ROTOR_4":                                                                128,
        "RV_CONJUGADO_DISTRIBUIDOR_5":                                                         129,
        "RV_CONJUGADO_ROTOR_5":                                                                130,
        "RV_CONJUGADO_DISTRIBUIDOR_6":                                                         131,
        "RV_CONJUGADO_ROTOR_6":                                                                132,
        "RV_CONJUGADO_DISTRIBUIDOR_7":                                                         133,
        "RV_CONJUGADO_ROTOR_7":                                                                134,
        "RV_CONJUGADO_DISTRIBUIDOR_8":                                                         135,
        "RV_CONJUGADO_ROTOR_8":                                                                136,
        "RV_CONJUGADO_DISTRIBUIDOR_9":                                                         137,
        "RV_CONJUGADO_ROTOR_9":                                                                138,
        "RV_CONJUGADO_DISTRIBUIDOR_10":                                                        139,
        "RV_CONJUGADO_ROTOR_10":                                                               140,
        "RV_ABERTURA_MAXIMA_DISTRIBUIDOR":                                                     182,
        "RV_ABERTURA_MAXIMA_DISTRIBUIDOR_A_VAZIO":                                             184,
        "RV_ABERTURA_MINIMA_DISTRIBUIDOR":                                                     183,
        "RV_ABERTURA_MAXIMA_ROTOR":                                                            185,
        "RV_ABERTURA_MINIMA_ROTOR":                                                            186,
        "RV_POTENCIA_MAXIMA":                                                                  189,
        "RV_POTENCIA_MINIMA":                                                                  190,


        ### RT
        ## LEITURAS_1
        "RT_CORRENTE_EXCITACAO":                                                               16,
        "RT_TENSAO_EXCITACAO":                                                                 17,
        "RT_TEMPERATURA_ROTOR":                                                                25,
        "RT_ESTADO_OPERACAO":                                                                  26,
        "RT_CONTROLE_SINCRONIZADO_SELECIONADO":                                                27,

        ## ENTRADAS_DIGITAIS
        "RT_ED_SEM_BLOQUEIO_EXTERNO":                                                       [30, 0],
        "RT_ED_HABILITA_REGULADOR":                                                         [30, 1],
        "RT_ED_SELECIONA_MODO_CONTROLE_ISOLADO":                                            [30, 2],
        "RV_ED_DRIVE_EXCITACAO_HABILITADO_LOGICA_DE_DISPARO":                               [30, 3],
        "RV_ED_RESET_FALHAS":                                                               [30, 4],
        "RT_ED_INCREMENTA_REFERENCIA_CONTROLE":                                             [30, 5],
        "RT_ED_DECREMENTA_REFERENCIA_CONTROLE":                                             [30, 6],
        "RT_ED_DISJUNTOR_MAQUINA_FECHADO":                                                  [30, 7],
        "RT_ED_CONTATOR_CAMPO_FECHADO":                                                     [30, 8],
        "RT_ED_CROWBAR_INATIVO":                                                            [30, 9],
        "RT_ED_PROGRAMAVEL_1":                                                              [30, 10],
        "RT_ED_PROGRAMAVEL_2":                                                              [30, 11],

        ## SAIDAS_DIGITAIS
        "RT_SD_RELE_TRIP_NAO_ATUADO":                                                       [31, 0],
        "RT_SD_RELE_ALARME":                                                                [31, 1],
        "RT_SD_RELE_REGULADOR_HABILITADO":                                                  [31, 2],
        "RT_SD_RELE_REGULADOR_REGULANDO":                                                   [31, 3],
        "RT_SD_RELE_HABILITA_DRIVE_EXCITACAO_LOGICA_DISPARO":                               [31, 4],
        "RT_SD_RELE_HABILITA_CONTATOR_CAMPO":                                               [31, 5],
        "RT_SD_RELE_HABILITA_PRE_EXCITACAO":                                                [31, 6],
        "RT_SD_RELE_HABILITA_CROWBAR":                                                      [31, 7],
        "RT_SD_RELE_SAIDA_PROGRAMAVEL_1":                                                   [31, 8],
        "RT_SD_RELE_SAIDA_PROGRAMAVEL_2":                                                   [31, 9],
        "RT_SD_SEGUIDOR_1":                                                                 [31, 10],
        "RT_SD_SEGUIDOR_2":                                                                 [31, 11],

        ## LIMITES_OPERAÇÃO
        "RT_LIMITADOR_SUPERIOR_CORRENTE_EXCITACAO":                                         [31, 0],
        "RT_LIMITADOR_INFERIOR_CORRENTE_EXCITACAO":                                         [31, 1],
        "RT_LIMITADOR_SUPERIOR_TENSAO_TERMINAL":                                            [31, 2],
        "RT_LIMITADOR_INFERIOR_TENSAO_TERMINAL":                                            [31, 3],
        "RT_LIMITADOR_SUPERIOR_POTENCIA_REATIVA":                                           [31, 4],
        "RT_LIMITADOR_INFERIOR_POTENCIA_REATIVA":                                           [31, 5],
        "RT_LIMITADOR_SUPERIOR_FATOR_DE_POTENCIA":                                          [31, 10],
        "RT_LIMITADOR_INFERIOR_FATOR_DE_POTENCIA":                                          [31, 11],
        "RT_LIMITADOR_VOLTZ_HERTZ":                                                         [31, 12],
        "RT_LIMITADOR_ABERTURA_PONTE":                                                      [31, 13],
        "RT_LIMITADOR_PQ_RELACAO_POTENCIA_ATIVA_X_POTENCIA_REATIVA":                        [31, 14],

        ## LEITURAS_2
        "RT_SETPOINT_TENSAO_PU":                                                               40,
        "RT_SETPOINT_POTENCIA_REATIVA_KVAR":                                                   41,
        "RT_SETPOINT_POTENCIA_REATIVA_PU":                                                     41,
        "RT_SETPOINT_FATOR_POTENCIA_PU":                                                       42,
        "RT_ABERTURA_PONTE":                                                                   43,
        "RT_REFERENCIA_CORRENTE_CAMPO_PU":                                                     46,
        "RT_FEEDBACK_CORRENTE_CAMPO_PU":                                                       47,
        "RT_REFERENCIA_TENSAO_PU":                                                             52,
        "RT_FEEDBACK_TENSAO_PU":                                                               53,
        "RT_REFERENCIA_POTENCIA_REATIVA_PU":                                                   58,
        "RT_FEEDBACK_POTENCIA_REATIVA_PU":                                                     59,
        "RT_REFERENCIA_FATOR_POTENCIA_PU":                                                     64,
        "RT_FEEDBACK_FATOR_POTENCIA_PU":                                                       65,

        ## ALARMES_1
        "RT_ALARME_SOBRETENSAO":                                                            [70, 0],
        "RT_ALARME_SUBTENSAO":                                                              [70, 1],
        "RT_ALARME_SOBREFREQUENCIA":                                                        [70, 2],
        "RT_ALARME_SUBFREQUENCIA":                                                          [70, 3],
        "RT_ALARME_LIMITE_SUPERIOR_POTENCIA_REATIVA":                                       [70, 4],
        "RT_ALARME_LIMITE_INFERIOR_POTENCIA_REATIVA":                                       [70, 5],
        "RT_ALARME_LIMITE_SUPERIOR_FATOR_DE_POTENCIA":                                      [70, 6],
        "RT_ALARME_LIMITE_INFERIOR_FATOR_DE_POTENCIA":                                      [70, 7],
        "RT_ALARME_VARIACAO_DE_TENSAO":                                                     [70, 8],
        "RT_ALARME_POTENCIA_ATIVA_REVERSA":                                                 [70, 9],
        "RT_ALARME_SOBRECORRENTE_TERMINAL":                                                 [70, 10],
        "RT_ALARME_LIMITE_SUPERIOR_CORRENTE_EXCITACAO":                                     [70, 11],
        "RT_ALARME_LIMITE_INFERIOR_CORRENTE_EXCITACAO":                                     [70, 12],
        "RT_ALARME_TEMPERATURA_MUITO_ALTA_ROTOR":                                           [70, 13],
        "RT_ALARME_PRESENCA_DE_TENSAO_TERMINAL_COM_AUSENCIA_DE_CORRENTE_DE_EXCITACAO":      [70, 14],
        "RT_ALARME_PRESENCA_DE_CORRENTE_DE_EXCITACAO_COM_AUXENCIA_DE_TENSAO_TERMINAL":      [70, 15],

        ## ALARMES_2
        "RT_ALARME_FALHA_CONTROLE_CORRENTE_EXCITACAO":                                      [71, 0],
        "RT_ALARME_FALHA_CONTROLE_TENSAO_TERMINAL":                                         [71, 1],
        "RT_ALARME_CROWBAR_ATUADO_COM_REGULADOR_HABILITADO":                                [71, 2],
        "RT_ALARME_FALHA_HABILITAR_DRIVE_DE_EXCITACAO":                                     [71, 3],
        "RT_ALARME_FALHA_FECHAR_CONTATOR_DE_CAMPO":                                         [71, 4],
        "RT_ALARME_FALHA_DE_CORRENTE_DE_EXCITACAO_COM_PRE_EXCITACAO_ATIVA":                 [71, 5],
        "RT_ALARME_PERDA_MEDICAO_POTENCIA_REATIVA":                                         [71, 6],
        "RT_ALARME_PERDA_MEDICAO_TENSAO_TERMINAL":                                          [71, 7],
        "RT_ALARME_PERDA_MEDICAO_CORRENTE_EXCITACAO":                                       [71, 8],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_REATIVO":                                        [71, 9],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_TENSAO":                                         [71, 10],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_PRINCIPAL":                            [71, 11],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_RETAGUARDA":                           [71, 12],

        ## FALHAS_1
        "RT_FALHA_SOBRETENSAO":                                                             [71, 0],
        "RT_FALHA_SUBTENSAO":                                                               [71, 1],
        "RT_FALHA_SOBREFREQUENCIA":                                                         [71, 2],
        "RT_FALHA_SUBFREQUENCIA":                                                           [71, 3],
        "RT_FALHA_LIMITE_SUPERIOR_POTENCIA_REATIVA":                                        [71, 4],
        "RT_FALHA_LIMITE_INFERIOR_POTENCIA_REATIVA":                                        [71, 5],
        "RT_FALHA_LIMITE_SUPERIOR_FATOR_DE_POTENCIA":                                       [71, 6],
        "RT_FALHA_LIMITE_INFERIOR_FATOR_DE_POTENCIA":                                       [71, 7],
        "RT_FALHA_SOBRETENSAO_INSTANTANEA":                                                 [71, 8],
        "RT_FALHA_VARIACAO_DE_TENSAO":                                                      [71, 9],
        "RT_FALHA_POTENCIA_ATIVA_REVERSA":                                                  [71, 10],
        "RT_FALHA_SOBRECORRENTE_TERMINAL":                                                  [71, 11],
        "RT_FALHA_LIMITE_SUPERIOR_CORRENTE_EXCITACAO":                                      [71, 12],
        "RT_FALHA_LIMITE_INFERIOR_CORRENTE_EXCITACAO":                                      [71, 13],
        "RT_FALHA_LIMITE_SUPERIOR_TENSAO_EXCITACAO":                                        [71, 14],
        "RT_FALHA_LIMITE_INFERIOR_TENSAO_EXCITACAO":                                        [71, 15],

        ## FALHAS_2
        "RT_FALHA_TEMPERATURA_MUITO_ALTA_ROTOR":                                            [73, 0],
        "RT_FALHA_PRESENCA_DE_TENSAO_TERMINAL_COM_AUSENCIA_DE_CORRENTE_DE_EXCITACAO":       [73, 1],
        "RT_FALHA_PRESENCA_DE_CORRENTE_DE_EXCITACAO_COM_AUXENCIA_DE_TENSAO_TERMINAL":       [73, 2],
        "RT_FALHA_FALHA_CONTROLE_CORRENTE_EXCITACAO":                                       [73, 3],
        "RT_FALHA_FALHA_CONTROLE_TENSAO_TERMINAL":                                          [73, 4],
        "RT_FALHA_CROWBAR_ATUADO_COM_REGULADOR_HABILITADO":                                 [73, 5],
        "RT_FALHA_FALHA_HABILITAR_DRIVE_DE_EXCITACAO_LOGICA_DE_DISPARO":                    [73, 6],
        "RT_ALAME_FALHA_FECHAR_CONTATOR_DE_CAMPO":                                          [73, 7],
        "RT_FALHA_FALHA_DE_CORRENTE_DE_EXCITACAO_COM_PRE_EXCITACAO_ATIVA":                  [73, 8],
        "RT_FALHA_TEMPO_EXCESSIVO_DE_PRE_EXCITACAO":                                        [73, 9],
        "RT_FALHA_TEMPO_EXCESSIVO_DE_PARADA":                                               [73, 10],
        "RT_FALHA_TEMPO_EXCESSIVO_DE_PARTIDA":                                              [73, 11],
        "RT_FALHA_BLOQUEIO_EXTERNO":                                                        [73, 12],

        ## FALHAS_3
        "RT_FALHA_PERDA_MEDICAO_POTENCIA_REATIVA":                                          [74, 0],
        "RT_FALHA_PERDA_MEDICAO_TENSAO_TERMINAL":                                           [74, 1],
        "RT_FALHA_PERDA_MEDICAO_CORRENTE_EXCITACAO_PRINCIPAL":                              [74, 2],
        "RT_FALHA_PERDA_MEDICAO_CORRENTE_EXCITACAO_RETAGUARDA":                             [74, 3],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_REATIVO":                                         [74, 4],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_TENSAO":                                          [74, 5],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_PRINCIPAL":                             [74, 6],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_RETAGUARDA":                            [74, 7],

        ## LEITURAS_3
        "RT_TENSAO_NOMINAL":                                                                   85,
        "RT_POTENCIA_APARENTE_NOMINAL":                                                        86,
        "RT_CONTROLE_1":                                                                       90,
        "RT_CONTROLE_2":                                                                       91,
    },
}