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
        "LED1_50_51":                                                                   [220, 0],   # Holding Register                      (OP -> 0x03 Read Holding Registers)
        "LED2_67N":                                                                     [220, 1],   # Holding Register                      (OP -> 0x03 Read Holding Registers)
        "LED3":                                                                         [220, 2],   # Holding Register                      (OP -> 0x03 Read Holding Registers)
        "LED4_78":                                                                      [220, 3],   # Holding Register                      (OP -> 0x03 Read Holding Registers)
        "LED5":                                                                         [220, 4],   # Holding Register                      (OP -> 0x03 Read Holding Registers)
        "LED6_50BF":                                                                    [220, 5],   # Holding Register                      (OP -> 0x03 Read Holding Registers)
        "LED7_81":                                                                      [220, 6],   # Holding Register                      (OP -> 0x03 Read Holding Registers)
        "LED8_27":                                                                      [220, 7],   # Holding Register                      (OP -> 0x03 Read Holding Registers)
        "LED9_59":                                                                      [220, 8],   # Holding Register                      (OP -> 0x03 Read Holding Registers)
        "LED10_59N":                                                                    [220, 9],   # Holding Register                      (OP -> 0x03 Read Holding Registers)

        "VAB":                                                                          154,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "VBC":                                                                          155,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "VCA":                                                                          156,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "IA":                                                                           320,        # Input Register                        (OP -> Read Input Registers - 3x)
        "IB":                                                                           322,        # Input Register                        (OP -> Read Input Registers - 3x)
        "IC":                                                                           324,        # Input Register                        (OP -> Read Input Registers - 3x)
        "P":                                                                            160,        # Input Register                        (OP -> Read Input Registers - 3x)
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
    "CMD_PD_BOMBA_1_PRINCIPAL":                                                         [12288, 2],
    "CMD_PD_BOMBA_2_PRINCIPAL":                                                         [12288, 3],
    "CMD_PE_BOMBA_1_LIGA":                                                              [12288, 5],
    "CMD_PE_BOMBA_2_LIGA":                                                              [12288, 6],
    "CMD_PE_BOMBA_1_DESLIGA":                                                           [12288, 5],
    "CMD_PE_BOMBA_2_DESLIGA":                                                           [12288, 6],
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
    "BOTAO_BLOQUEIO_86BTBF":                                                            [12308, 1], # HIGH
    "POCO_DRANAGEM_BOMBA_1_AUTOMATICO":                                                 [12308, 2],
    "POCO_DRENAGEM_BOMBA_2_AUTOMATICO":                                                 [12308, 3],
    "DISJUNTORES_MODO_REMOTO":                                                          [12308, 4], # HIGH
    "DISJUNTOR_TSA_TRIP":                                                               [12308, 5],
    "DISJUNTOR_GMG_TRIP":                                                               [12308, 6],
    "RELE_BLOQUEIO_86BTBF":                                                             [12308, 7], # HIGH
    "CARREGADOR_BATERIAS_FALHA":                                                        [12308, 8], # HIGH
    # "CONVERSOR_FIBRA_FALHA":                                                            [12308, 9], ?
    "SUPERVISOR_TENSAO_FALHA":                                                          [12308, 10], # HIGH
    "DPS_TSA":                                                                          [12308, 11], # HIGH
    "DPS_GMG":                                                                          [12308, 12], # HIGH
    "POCO_DRENAGEM_BOMBA_1_DEFEITO":                                                    [12308, 13],
    "POCO_DRENAGEM_BOMBA_1_LIGADA":                                                     [12308, 14],
    "POCO_DRENAGEM_BOMBA_2_DEFEITO":                                                    [12308, 15],

    "POCO_DRENAGEM_BOMBA_2_LIGADA":                                                     [12309, 0],
    "SF_BOMBA_1_DEFEITO":                                                               [12309, 1],
    "SF_BOMBA_1_LIGADA":                                                                [12309, 2],
    "SF_BOMBA_2_DEFEITO":                                                               [12309, 3],
    "SF_BOMBA_2_LIGADA":                                                                [12309, 4],
    "POCO_DRENAGEM_SENSOR_NIVEL_MUITO_BAIXO":                                           [12309, 5],
    "POCO_DRENAGEM_SENSOR_NIVEL_DESLIGA_BOMBAS":                                        [12309, 6],
    "POCO_DRENAGEM_SENSOR_NIVEL_LIGA_BOMBA":                                            [12309, 7],
    "POCO_DRENAGEM_SENSOR_NIVEL_ALTO":                                                  [12309, 8],
    "POCO_DRENAGEM_SENSOR_NIVEL_MUITO_ALTO":                                            [12309, 9], # HIGH
    "DISJUNTOR_TSA_FECHADO":                                                            [12309, 10],
    "DISJUNTOR_GMG_FECHADO":                                                            [12309, 11],
    "SUPERVISOR_TENSAO_TSA_FALHA":                                                      [12309, 12], # HIGH
    "SUPERVISOR_TENSAO_GMG_FALHA":                                                      [12309, 13], # HIGH
    "TE_TEMPERATURA_MUITO_ALTA":                                                        [12309, 14],
    "SE_DISJUNTOR_LINHA_FECHADO":                                                       [12309, 15],

    ## SST_ENTRADAS_DIGITAIS_1
    "SE_DISJUNTOR_LINHA_ABERTO":                                                        [12310, 0],
    "TE_TEMPERATURA_ALARME":                                                            [12310, 1],
    "TE_PRESSAO_MUITO_ALTA":                                                            [12310, 2],
    "TE_NIVEL_OLEO_MUITO_BAIXO":                                                        [12310, 3],
    "PRTVA1_50_BF":                                                                     [12310, 4], # HIGH
    "PRTVA1_FILTRAGEM_ACIONA":                                                          [12310, 5],
    "PRTVA2_50BF":                                                                      [12310, 6], # HIGH
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
    "PSA_RELE_LINHA_SEM_TRIP_OU_FALHA":                                                 [12311, 2], # HIGH
    "PSA_CONVERSOR_FIBRA_FALHA":                                                        [12311, 3], # HIGH
    "PSA_CONVERSOR_2_FIBRA_FALHA":                                                      [12311, 4], # HIGH

    ## STT_FALHAS_ANALOGICAS
    "NIVEL_MONTANTE_FALHA_LEITURA":                                                     [12338, 0],
    "NIVEL_JUSANTE_FALHA_LEITURA":                                                      [12338, 1],
    "SFA_PRESSAO_LADO_LIMPO_FALHA_LEITURA":                                             [12338, 2],
    "SFA_PRESSAO_LADO_SUJO_FALHA_LEITURA":                                              [12338, 3],
    "SFB_PRESSAO_LADO_LIMPO_FALHA_LEITURA":                                             [12338, 4],
    "SFB_PRESSAO_LADO_SUJO_FALHA_LEITURA":                                              [12338, 5],

    ## STT_ALARMES_HH_ANALOGICAS
    "NIVEL_JUSANTE_MUITO_ALTO":                                                         [12340, 0],
    "NIVEL_MONTANTE_MUITO_ALTO":                                                        [12340, 1],
    "NIVEL_JUSANTE_2_MUITO_ALTO":                                                       [12340, 2],
    "SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO":                                                [12340, 3],
    "SFA_PRESSAO_LADO_SUJO_MUITO_ALTO":                                                 [12340, 4],
    "SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO":                                                [12340, 5],
    "SFB_PRESSAO_LADO_SUJO_MUITO_ALTO":                                                 [12340, 6],

    ## STT_ALARMES_H_ANALOGICAS
    "PSA_NIVEL_JUSANTE_ALTO":                                                           [12342, 0],
    "PSA_NIVEL_MONTANTE_ALTO":                                                          [12342, 1],
    "PSA_NIVEL_JUSANTE_2_ALTO":                                                         [12342, 2],
    "PSA_SFA_PRESSAO_LADO_LIMPO_ALTO":                                                  [12342, 3],
    "PSA_SFA_PRESSAO_LADO_SUJO_ALTO":                                                   [12342, 4],
    "PSA_SFB_PRESSAO_LADO_LIMPO_ALTO":                                                  [12342, 5],
    "PSA_SFB_PRESSAO_LADO_SUJO_ALTO":                                                   [12342, 6],

    ## STT_ALARMES_L_ANALOGICAS
    "NIVEL_JUSANTE_BAIXO":                                                              [12344, 0],
    "NIVEL_MONTANTE_BAIXO":                                                             [12344, 1],
    "NIVEL_JUSANTE_2_BAIXO":                                                            [12344, 2],
    "SFA_PRESSAO_LADO_LIMPO_BAIXO":                                                     [12344, 3],
    "SFA_PRESSAO_LADO_SUJO_BAIXO":                                                      [12344, 4],
    "SFB_PRESSAO_LADO_LIMPO_BAIXO":                                                     [12344, 5],
    "SFB_PRESSAO_LADO_SUJO_BAIXO":                                                      [12344, 6],

    ## STT_ALARMES_LL_ANALOGICAS
    "NIVEL_JUSANTE_MUITO_BAIXO":                                                        [12346, 0],
    "NIVEL_MONTANTE_MUITO_BAIXO":                                                       [12346, 1],
    "NIVEL_JUSANTE_2_MUITO_BAIXO":                                                      [12346, 2],
    "SFA_PRESSAO_LADO_LIMPO_MUITO_BAIXO":                                               [12346, 3],
    "SFA_PRESSAO_LADO_SUJO_MUITO_BAIXO":                                                [12346, 4],
    "SFB_PRESSAO_LADO_LIMPO_MUITO_BAIXO":                                               [12346, 5],
    "SFB_PRESSAO_LADO_SUJO_MUITO_BAIXO":                                                [12346, 6],

    ## STT_SA_SE
    "DRENAGEM_BOMBA_1_INDISPONIVEL":                                                    [12348, 0], # HIGH
    "DRENAGEM_BOMBA_2_INDISPONIVEL":                                                    [12348, 1], # HIGH
    "DRENAGEM_BOMBA_1_PRINCIPAL":                                                       [12348, 2],
    "DRENAGEM_BOMBA_2_PRINCIPAL":                                                       [12348, 3],
    "DRENAGEM_BOIAS_DISCREPANCIA":                                                      [12348, 4],
    "ESGOTAMENTO_BOMBA_1_INDISPONIVEL":                                                 [12348, 5], # HIGH
    "ESGOTAMENTO_BOMBA_2_INDISPONIVEL":                                                 [12348, 6], # HIGH
    "ESGOTAMENTO_BOMBA_1_FALHA":                                                        [12348, 7],
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
    "DISPOSITIVO_PROTETOR_DE_SURTO":                                                    [12308, 0], # HIGH
    "UHLG_BOMBA_1_LIGADA":                                                              [12308, 1],
    "UHLG_BOMBA_1_DEFEITO":                                                             [12308, 2],
    "UHLG_BOMBA_2_LIGADA":                                                              [12308, 3],
    "UHLG_BOMBA_2_DEFEITO":                                                             [12308, 4],
    "MONOVIA_MOTOR_1_LIGADA":                                                           [12308, 5],
    "MONOVIA_MOTOR_1_DEFEITO":                                                          [12308, 6],
    "MONOVIA_MOTOR_2_LIGADA":                                                           [12308, 7],
    "MONOVIA_MOTOR_2_DEFEITO":                                                          [12308, 8],
    "CONVERSOR_FIBRA_FALHA":                                                            [12308, 9], # HIGH

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
        "CMD_UHRV_BOMBA_1_PRINCIPAL":                                                   [12292, 4],
        "CMD_UHRV_BOMBA_2_PRINCIPAL":                                                   [12292, 5],
        "CMD_UHRV_BOMBA_2_LIGA":                                                        [12292, 6],
        "CMD_UHRV_BOMBA_2_DESLIGA":                                                     [12292, 7],

        ## CMD_UHLM
        "CMD_UHLM_MODO_AUTOMATICO":                                                     [12294, 0],
        "CMD_UHLM_MODO_MANUTENCAO":                                                     [12294, 1],
        "CMD_UHLM_BOMBA_1_LIGA":                                                        [12294, 2],
        "CMD_UHLM_BOMBA_1_DESLIGA":                                                     [12294, 3],
        "CMD_UHLM_BOMBA_1_PRINCIPAL":                                                   [12294, 4],
        "CMD_UHLM_BOMBA_2_PRINCIPAL":                                                   [12294, 5],
        "CMD_UHLM_BOMBA_2_LIGA":                                                        [12294, 6],
        "CMD_UHLM_BOMBA_2_DESLIGA":                                                     [12294, 7],

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
        ## SST_ENTRADAS_DIGITAIS_1
        "BOTAO_BLOQUEIO_86EH":                                                          [12310, 0], # HIGH
        "REARME_FALHAS":                                                                [12310, 1],
        "BOTAO_PARA_UG":                                                                [12310, 2],
        "BOTAO_PARTE_UG":                                                               [12310, 3],
        "BOTAO_DIMINUI_REFERENCIA_RV":                                                  [12310, 4],
        "BOTAO_AUMENTA_REFERENCIA_RV":                                                  [12310, 5],
        "BOTAO_DIMINUI_REFERENCIA_RT":                                                  [12310, 6],
        "BOTAO_AUMENTA_REFERENCIA_RT":                                                  [12310, 7],
        "RELE_PROT_GERADOR_TRIP":                                                       [12310, 9], # HIGH
        "RELE_PROT_GERADOR_50BF":                                                       [12310, 10], # HIGH
        "RV_TRIP":                                                                      [12310, 11], # HIGH
        "RV_ALARME":                                                                    [12310, 12],
        "RV_HABILITADO":                                                                [12310, 13],
        "RV_REGULANDO":                                                                 [12310, 14],
        "RV_POTENCIA_NULA":                                                             [12310, 15],

        "PRTVA_RV_MAQUINA_PARADA":                                                      [12311, 0],
        "PRTVA_RV_VELOCIDADE_MENOR":                                                    [12311, 1],
        "PRTVA_RV_VELOCIDADE_MAIOR":                                                    [12311, 2],
        "PRTVA_RV_DISTRIBUIDOR_ABERTO":                                                 [12311, 3],
        "PRTVA_RT_TRIP":                                                                [12311, 4], # HIGH
        "PRTVA_RT_ALARME":                                                              [12311, 5],
        "PRTVA_RT_HABILITADO":                                                          [12311, 6],
        "PRTVA_RT_REGULANDO":                                                           [12311, 7],
        "PRTVA_CONTATOR_DE_CAMPO_FECHADO":                                              [12311, 8],
        "PRTVA_DISJUNTOR_DE_MAQUINA_FECHADO":                                           [12311, 9],
        "PRTVA_RELE_BLOQUEIO_86EH":                                                     [12311, 10], # HIGH
        "PRTVA_SUPERVISAO_DE_TENSAO_ENTRADA_CA":                                        [12311, 11],
        "PRTVA_DISPOSITIVO_PROTECAO_DE_SURTO":                                          [12311, 12], # HIGH
        "PRTVA_UHRV_BOMBA_DEFEITO":                                                     [12311, 13],
        "PRTVA_UHRV_BOMBA_LIGADA":                                                      [12311, 14],
        "PRTVA_UHLM_BOMBA_DEFEITO":                                                     [12311, 15],

        ## SST_ENTRADAS_DIGITAIS_2
        "UHLM_BOMBA_LIGADA":                                                            [12312, 0],
        "UG_RESISTENCIA_AQUEC_GERADOR_DEFEITO":                                         [12312, 3],
        "UG_RESISTENCIA_AQUEC_GERADOR_LIGADA":                                          [12312, 4],
        "DISJUNTOR_TPS_PROTECAO":                                                       [12312, 5], # HIGH
        "DISJUNTOR_TPS_SINCRONIZACAO":                                                  [12312, 6], # HIGH
        "UHRV_OLEO_NIVEL_MUITO_BAIXO":                                                  [12312, 7], # HIGH
        "UHRV_FILTRO_OLEO_SUJO":                                                        [12312, 8], # HIGH
        "UHRV_PRESSAO_CRITICA":                                                         [12312, 9],
        "UHRV_PRESSAO_FREIO":                                                           [12312, 10],
        "UHLM_OLEO_NIVEL_MUITO_ALTO":                                                   [12312, 12], # HIGH
        "UHLM_OLEO_NIVEL_MUITO_BAIXO":                                                  [12312, 13], # HIGH
        "UHLM_PRESSAO_LINHA_LUBRIFICACAO":                                              [12312, 14],
        "UHLM_FILTRO_OLEO_SUJO":                                                        [12312, 15], # HIGH

        "UHLM_FLUXO_TROCADOR_DE_CALOR":                                                 [12312, 0],
        "QBAG_ESCOVA_POLO_POSITIVO_DESGASTADA":                                         [12313, 2],
        "QBAG_ESCOVA_POLO_NEGATICO_DESGASTADA":                                         [12313, 3],
        "PSA_BLOQUEIO_86BTBF":                                                          [12313, 4], # HIGH
        "PSA_POCO_DRENAGEM_NIVEL_MUITO_ALTO":                                           [12313, 5], # HIGH
        "PSA_FILTRAGEM_PRESSAO_SAIDA":                                                  [12313, 6],
        "PSA_DISJUNTOR_LINHA_FECHADO":                                                  [12313, 7],
        "VB_VALVULA_BORBOLETA_ABERTA":                                                  [12313, 12],
        "VB_VALVULA_BORBOLETA_FECHADA":                                                 [12313, 13],
        "VB_VALVULA_BYPASS_ABERTA":                                                     [12313, 14],
        "VB_VALVULA_BYPASS_FECHADA":                                                    [12313, 15],

        ## STT_FALHAS_TEMPERATURA
        "TIRISTORES_TEMPERATURA_FALHA_LEITURA":                                         [12328, 0],
        "CROWBAR_TEMPERATURA_FALHA_LEITURA":                                            [12328, 1],
        # "TRAFO_EXCITACAO_TEMPERATURA_FALHA_LEITURA":                                    [12328, 2], ?
        "GERADOR_FASE_A_TEMPERATURA_FALHA_LEITURA":                                     [12328, 3],
        "GERADOR_FASE_B_TEMPERATURA_FALHA_LEITURA":                                     [12328, 4],
        "GERADOR_FASE_C_TEMPERATURA_FALHA_LEITURA":                                     [12328, 5],
        "GERADOR_NUCLEO_1_TEMPERATURA_FALHA_LEITURA":                                   [12328, 6],
        "GERADOR_NUCLEO_2_TEMPERATURA_FALHA_LEITURA":                                   [12328, 7],
        "GERADOR_NUCLEO_3_TEMPERATURA_FALHA_LEITURA":                                   [12328, 8],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_FALHA_LEITURA":                              [12328, 9],
        "MANCAL_COMBINADO_CASQUILHO_1_TEMPERATURA_FALHA_LEITURA":                       [12328, 10],
        "MANCAL_COMBINADO_CASQUILHO_2_TEMPERATURA_FALHA_LEITURA":                       [12328, 11],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_FALHA_LEITURA":                            [12328, 12],
        "UHLM_TEMPERATURA_OLEO_FALHA_LEITURA":                                          [12328, 13],
        "UHRV_TEMPERATURA_OLEO_FALHA_LEITURA":                                          [12328, 14],


        ## STT_ALARMES_HH_TEMPERATURA
        "TIRISTORES_TEMPERATURA_MUITO_ALTA":                                            [12330, 0],
        "CROWBAR_TEMPERATURA_MUITO_ALTA":                                               [12330, 1],
        # "TRAFO_EXCITACAO_TEMPERATURA_MUITO_ALTA":                                       [12330, 2], ?
        "GERADOR_FASE_A_TEMPERATURA_MUITO_ALTA":                                        [12330, 3],
        "GERADOR_FASE_B_TEMPERATURA_MUITO_ALTA":                                        [12330, 4],
        "GERADOR_FASE_C_TEMPERATURA_MUITO_ALTA":                                        [12330, 5],
        "GERADOR_NUCLEO_1_TEMPERATURA_MUITO_ALTA":                                      [12330, 6],
        "GERADOR_NUCLEO_2_TEMPERATURA_MUITO_ALTA":                                      [12330, 7],
        "GERADOR_NUCLEO_3_TEMPERATURA_MUITO_ALTA":                                      [12330, 8],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_MUITO_ALTA":                                 [12330, 9],
        "MANCAL_COMBINADO_CASQUILHO_1_TEMPERATURA_MUITO_ALTA":                          [12330, 10],
        "MANCAL_COMBINADO_CASQUILHO_2_TEMPERATURA_MUITO_ALTA":                          [12330, 11],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_MUITO_ALTA":                               [12330, 12],
        "UHLM_TEMPERATURA_OLEO_MUITO_ALTA":                                             [12330, 13],
        "UHRV_TEMPERATURA_OLEO_MUITO_ALTA":                                             [12330, 14],


        ## STT_ALARMES_H_TEMPERATURA
        "TIRISTORES_TEMPERATURA_ALTA":                                                  [12332, 0],
        "CROWBAR_TEMPERATURA_ALTA":                                                     [12332, 1],
        # "TRAFO_EXCITACAO_TEMPERATURA_ALTA":                                             [12332, 2], ?
        "GERADOR_FASE_A_TEMPERATURA_ALTA":                                              [12332, 3],
        "GERADOR_FASE_B_TEMPERATURA_ALTA":                                              [12332, 4],
        "GERADOR_FASE_C_TEMPERATURA_ALTA":                                              [12332, 5],
        "GERADOR_NUCLEO_1_TEMPERATURA_ALTA":                                            [12332, 6],
        "GERADOR_NUCLEO_2_TEMPERATURA_ALTA":                                            [12332, 7],
        "GERADOR_NUCLEO_3_TEMPERATURA_ALTA":                                            [12332, 8],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_ALTA":                                       [12332, 9],
        "MANCAL_COMBINADO_CASQUILHO_1_TEMPERATURA_ALTA":                                [12332, 10],
        "MANCAL_COMBINADO_CASQUILHO_2_TEMPERATURA_ALTA":                                [12332, 11],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_ALTA":                                     [12332, 12],
        "UHLM_TEMPERATURA_OLEO_ALTA":                                                   [12332, 13],
        "UHRV_TEMPERATURA_OLEO_ALTA":                                                   [12332, 14],

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
        "UG_FALHA_ACOPLAMENTO_DE_CARGA":                                                [12360, 12],
        "UG_FALHA_DESCARGA_POTENCIA":                                                   [12360, 13],
        "UG_FALHA_ABRIR_DISJUNTOR":                                                     [12360, 14],

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
        # "UHLM_FALHA_PRESSOSTATO":                                                       [12364, 14],

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
        
        # STT_FILTRAGEM
        "SF_FALHA_FLUXO_TROCADOR_CALOR":                                                [12368, 0],
        "SF_FALHA_HABILITAR":                                                           [12368, 1],

        ## STT_RV
        "RV_FALHA_AO_HABILITAR":                                                        [12372, 0],
        "RV_FALHA_AO_PARTIR":                                                           [12372, 1],
        "RV_FALHA_AO_DESABILITAR":                                                      [12372, 2],
        "RV_FALHA_AO_PARAR_MAQUINA":                                                    [12372, 3],
        "RV_FALHA_AO_FECHAR_DISTRIBUIDOR":                                              [12372, 4],
        "RV_MODO_MANUTENCAO":                                                           [12372, 5],

        ## STT_RT
        "RT_FALHA_AO_HABILITAR":                                                        [12374, 0],
        "RT_FALHA_AO_PARTIR":                                                           [12374, 1],
        "RT_FALHA_AO_DESABILITAR":                                                      [12374, 2],

        ## BLOQUEIO_86M
        "BLOQUEIO_86M_ATUADO":                                                          [12428, 15],

        ## BLOQUEIO_86E
        "BLOQUEIO_86E_ATUADO":                                                          [12430, 15],

        ## BLOQUEIO_86H
        "BLOQUEIO_86H_ATUADO":                                                          [12432, 15],

        ## PARTIDA_PARADA
        "STT_PARTIDA_PARADA":                                                           12388,
        "SST_PASSO_SELECIONADO":                                                        12390,
        "STT_PASSO_ATUAL":                                                              12392,

        ## PERMISSIVOS
        "STT_PRE_CONDICOES_GIRO_MECANICO":                                              12408,
        "STT_PRE_CONDICOES_EXCITCAO":                                                   12410,
        "STT_PRE_CONDICOES_SINCRONISMO":                                                12412,

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
        "CMD_UHRV_BOMBA_1_PRINCIPAL":                                                   [12292, 4],
        "CMD_UHRV_BOMBA_2_PRINCIPAL":                                                   [12292, 5],
        "CMD_UHRV_BOMBA_2_LIGA":                                                        [12292, 6],
        "CMD_UHRV_BOMBA_2_DESLIGA":                                                     [12292, 7],

        ## CMD_UHLM
        "CMD_UHLM_MODO_AUTOMATICO":                                                     [12294, 0],
        "CMD_UHLM_MODO_MANUTENCAO":                                                     [12294, 1],
        "CMD_UHLM_BOMBA_1_LIGA":                                                        [12294, 2],
        "CMD_UHLM_BOMBA_1_DESLIGA":                                                     [12294, 3],
        "CMD_UHLM_BOMBA_1_PRINCIPAL":                                                   [12294, 4],
        "CMD_UHLM_BOMBA_2_PRINCIPAL":                                                   [12294, 5],
        "CMD_UHLM_BOMBA_2_LIGA":                                                        [12294, 6],
        "CMD_UHLM_BOMBA_2_DESLIGA":                                                     [12294, 7],

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
        ## SST_ENTRADAS_DIGITAIS_1
        "BOTAO_BLOQUEIO_86EH":                                                          [12310, 0], # HIGH
        "REARME_FALHAS":                                                                [12310, 1],
        "BOTAO_PARA_UG":                                                                [12310, 2],
        "BOTAO_PARTE_UG":                                                               [12310, 3],
        "BOTAO_DIMINUI_REFERENCIA_RV":                                                  [12310, 4],
        "BOTAO_AUMENTA_REFERENCIA_RV":                                                  [12310, 5],
        "BOTAO_DIMINUI_REFERENCIA_RT":                                                  [12310, 6],
        "BOTAO_AUMENTA_REFERENCIA_RT":                                                  [12310, 7],
        "RELE_PROT_GERADOR_TRIP":                                                       [12310, 9], # HIGH
        "RELE_PROT_GERADOR_50BF":                                                       [12310, 10], # HIGH
        "RV_TRIP":                                                                      [12310, 11], # HIGH
        "RV_ALARME":                                                                    [12310, 12],
        "RV_HABILITADO":                                                                [12310, 13],
        "RV_REGULANDO":                                                                 [12310, 14],
        "RV_POTENCIA_NULA":                                                             [12310, 15],

        "PRTVA_RV_MAQUINA_PARADA":                                                      [12311, 0],
        "PRTVA_RV_VELOCIDADE_MENOR":                                                    [12311, 1],
        "PRTVA_RV_VELOCIDADE_MAIOR":                                                    [12311, 2],
        "PRTVA_RV_DISTRIBUIDOR_ABERTO":                                                 [12311, 3],
        "PRTVA_RT_TRIP":                                                                [12311, 4], # HIGH
        "PRTVA_RT_ALARME":                                                              [12311, 5],
        "PRTVA_RT_HABILITADO":                                                          [12311, 6],
        "PRTVA_RT_REGULANDO":                                                           [12311, 7],
        "PRTVA_CONTATOR_DE_CAMPO_FECHADO":                                              [12311, 8],
        "PRTVA_DISJUNTOR_DE_MAQUINA_FECHADO":                                           [12311, 9],
        "PRTVA_RELE_BLOQUEIO_86EH":                                                     [12311, 10], # HIGH
        "PRTVA_SUPERVISAO_DE_TENSAO_ENTRADA_CA":                                        [12311, 11],
        "PRTVA_DISPOSITIVO_PROTECAO_DE_SURTO":                                          [12311, 12], # HIGH
        "PRTVA_UHRV_BOMBA_DEFEITO":                                                     [12311, 13],
        "PRTVA_UHRV_BOMBA_LIGADA":                                                      [12311, 14],
        "PRTVA_UHLM_BOMBA_DEFEITO":                                                     [12311, 15],

        ## SST_ENTRADAS_DIGITAIS_2
        "UHLM_BOMBA_LIGADA":                                                            [12312, 0],
        "UG_RESISTENCIA_AQUEC_GERADOR_DEFEITO":                                         [12312, 3],
        "UG_RESISTENCIA_AQUEC_GERADOR_LIGADA":                                          [12312, 4],
        "DISJUNTOR_TPS_PROTECAO":                                                       [12312, 5], # HIGH
        "UHRV_OLEO_NIVEL_MUITO_BAIXO":                                                  [12312, 6], # HIGH
        "UHRV_FILTRO_OLEO_SUJO":                                                        [12312, 7], # HIGH
        "UHRV_PRESSAO_CRITICA":                                                         [12312, 8],
        "UHRV_PRESSAO_FREIO":                                                           [12312, 9],
        "UHLM_OLEO_NIVEL_MUITO_ALTO":                                                   [12312, 11], # HIGH
        "UHLM_OLEO_NIVEL_MUITO_BAIXO":                                                  [12312, 12], # HIGH
        "UHLM_PRESSAO_LINHA_LUBRIFICACAO":                                              [12312, 13],
        "UHLM_FILTRO_OLEO_SUJO":                                                        [12312, 14], # HIGH
        "UHLM_FLUXO_TROCADOR_DE_CALOR":                                                 [12312, 15],

        "QBAG_ESCOVA_POLO_POSITIVO_DESGASTADA":                                         [12313, 1],
        "QBAG_ESCOVA_POLO_NEGATICO_DESGASTADA":                                         [12313, 2],
        "PSA_BLOQUEIO_86BTBF":                                                          [12313, 3], # HIGH
        "PSA_POCO_DRENAGEM_NIVEL_MUITO_ALTO":                                           [12313, 4], # HIGH
        "PSA_FILTRAGEM_PRESSAO_SAIDA":                                                  [12313, 5],
        "PSA_DISJUNTOR_LINHA_FECHADO":                                                  [12313, 6],
        "TPs_PROTECAO_59N_ABERTO":                                                      [12313, 9], # HIGH
        "VB_VALVULA_BORBOLETA_ABERTA":                                                  [12313, 12],
        "VB_VALVULA_BORBOLETA_FECHADA":                                                 [12313, 13],
        "VB_VALVULA_BYPASS_ABERTA":                                                     [12313, 14],
        "VB_VALVULA_BYPASS_FECHADA":                                                    [12313, 15],

        ## STT_FALHAS_TEMPERATURA
        "TIRISTORES_TEMPERATURA_FALHA_LEITURA":                                         [12328, 0],
        "CROWBAR_TEMPERATURA_FALHA_LEITURA":                                            [12328, 1],
        # "TRAFO_EXCITACAO_TEMPERATURA_FALHA_LEITURA":                                    [12328, 2],
        "GERADOR_FASE_A_TEMPERATURA_FALHA_LEITURA":                                     [12328, 3],
        "GERADOR_FASE_B_TEMPERATURA_FALHA_LEITURA":                                     [12328, 4],
        "GERADOR_FASE_C_TEMPERATURA_FALHA_LEITURA":                                     [12328, 5],
        "GERADOR_NUCLEO_1_TEMPERATURA_FALHA_LEITURA":                                   [12328, 6],
        "GERADOR_NUCLEO_2_TEMPERATURA_FALHA_LEITURA":                                   [12328, 7],
        "GERADOR_NUCLEO_3_TEMPERATURA_FALHA_LEITURA":                                   [12328, 8],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_FALHA_LEITURA":                              [12328, 9],
        "MANCAL_COMBINADO_CASQUILHO_1_TEMPERATURA_FALHA_LEITURA":                       [12328, 10],
        "MANCAL_COMBINADO_CASQUILHO_2_TEMPERATURA_FALHA_LEITURA":                       [12328, 11],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_FALHA_LEITURA":                            [12328, 12],
        "UHLM_TEMPERATURA_OLEO_FALHA_LEITURA":                                          [12328, 13],
        "UHRV_TEMPERATURA_OLEO_FALHA_LEITURA":                                          [12328, 14],


        ## STT_ALARMES_HH_TEMPERATURA
        "TIRISTORES_TEMPERATURA_MUITO_ALTA":                                            [12330, 0],
        "CROWBAR_TEMPERATURA_MUITO_ALTA":                                               [12330, 1],
        # "TRAFO_EXCITACAO_TEMPERATURA_MUITO_ALTA":                                       [12330, 2],
        "GERADOR_FASE_A_TEMPERATURA_MUITO_ALTA":                                        [12330, 3],
        "GERADOR_FASE_B_TEMPERATURA_MUITO_ALTA":                                        [12330, 4],
        "GERADOR_FASE_C_TEMPERATURA_MUITO_ALTA":                                        [12330, 5],
        "GERADOR_NUCLEO_1_TEMPERATURA_MUITO_ALTA":                                      [12330, 6],
        "GERADOR_NUCLEO_2_TEMPERATURA_MUITO_ALTA":                                      [12330, 7],
        "GERADOR_NUCLEO_3_TEMPERATURA_MUITO_ALTA":                                      [12330, 8],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_MUITO_ALTA":                                 [12330, 9],
        "MANCAL_COMBINADO_CASQUILHO_1_TEMPERATURA_MUITO_ALTA":                          [12330, 10],
        "MANCAL_COMBINADO_CASQUILHO_2_TEMPERATURA_MUITO_ALTA":                          [12330, 11],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_MUITO_ALTA":                               [12330, 12],
        "UHLM_TEMPERATURA_OLEO_MUITO_ALTA":                                             [12330, 13],
        "UHRV_TEMPERATURA_OLEO_MUITO_ALTA":                                             [12330, 14],


        ## STT_ALARMES_H_TEMPERATURA
        "TIRISTORES_TEMPERATURA_ALTA":                                                  [12332, 0],
        "CROWBAR_TEMPERATURA_ALTA":                                                     [12332, 1],
        # "TRAFO_EXCITACAO_TEMPERATURA_ALTA":                                             [12332, 2],
        "GERADOR_FASE_A_TEMPERATURA_ALTA":                                              [12332, 3],
        "GERADOR_FASE_B_TEMPERATURA_ALTA":                                              [12332, 4],
        "GERADOR_FASE_C_TEMPERATURA_ALTA":                                              [12332, 5],
        "GERADOR_NUCLEO_1_TEMPERATURA_ALTA":                                            [12332, 6],
        "GERADOR_NUCLEO_2_TEMPERATURA_ALTA":                                            [12332, 7],
        "GERADOR_NUCLEO_3_TEMPERATURA_ALTA":                                            [12332, 8],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_ALTA":                                       [12332, 9],
        "MANCAL_COMBINADO_CASQUILHO_1_TEMPERATURA_ALTA":                                [12332, 10],
        "MANCAL_COMBINADO_CASQUILHO_2_TEMPERATURA_ALTA":                                [12332, 11],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_ALTA":                                     [12332, 12],
        "UHLM_TEMPERATURA_OLEO_ALTA":                                                   [12332, 13],
        "UHRV_TEMPERATURA_OLEO_ALTA":                                                   [12332, 14],

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
        "FREIO_FALHA_AO_APLICAR_OU_DESAPLICAR":                                         [12360, 12],
        "FALHA_ACOPLAMENTO_DE_CARGA":                                                   [12360, 13],
        "FALHA_DESCARGA_POTENCIA":                                                      [12360, 14],
        "FALHA_ABRIR_DISJUNTOR":                                                        [12360, 15],

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
        # "UHLM_FALHA_PRESSOSTATO":                                                       [12364, 14], ?

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

        ## STT_RV
        "RV_FALHA_AO_HABILITAR":                                                        [12372, 0],
        "RV_FALHA_AO_PARTIR":                                                           [12372, 1],
        "RV_FALHA_AO_DESABILITAR":                                                      [12372, 2],
        "RV_FALHA_AO_PARAR_MAQUINA":                                                    [12372, 3],
        "RV_FALHA_AO_FECHAR_DISTRIBUIDOR":                                              [12372, 4],
        "RV_MODO_MANUTENCAO":                                                           [12372, 5],

        ## STT_RT
        "RT_FALHA_AO_HABILITAR":                                                        [12374, 0],
        "RT_FALHA_AO_PARTIR":                                                           [12374, 1],
        "RT_FALHA_AO_DESABILITAR":                                                      [12374, 2],

        ## BLOQUEIO_86M
        "BLOQUEIO_86M_ATUADO":                                                          [12428, 15],

        ## BLOQUEIO_86E
        "BLOQUEIO_86E_ATUADO":                                                          [12430, 15],

        ## BLOQUEIO_86H
        "BLOQUEIO_86H_ATUADO":                                                          [12432, 15],

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

        ## PARTIDA_PARADA
        "STT_PARTIDA_PARADA":                                                           12388,
        "SST_PASSO_SELECIONADO":                                                        12390,
        "STT_PASSO_ATUAL":                                                              12392,

        ## PERMISSIVOS
        "STT_PRE_CONDICOES_GIRO_MECANICO":                                              12408,
        "STT_PRE_CONDICOES_EXCITCAO":                                                   12410,
        "STT_PRE_CONDICOES_SINCRONISMO":                                                12412,
    },
}

REG_RTV = {
    "UG1":{
        ### RV
        ## LEITURAS_1
        "RV_POSICAO_DISTRIBUIDOR_PU":                                                       7,
        "RV_POSICAO_ROTOR_PU":                                                              8,
        "RV_VELOCIDADE_PU":                                                                 9,
        "RV_POTENCIA_ATIVA_PU":                                                             10,
        "RV_NIVEL_PU":                                                                      11,
        "RV_REFERENCIA_POTENCIA_PU":                                                        12,
        "RV_POSICAO_DISTRIBUIDOR":                                                          14,
        "RV_POSICAO_ROTOR":                                                                 15,
        "RV_ROTACAO":                                                                       16,
        "RV_FREQUENCIA":                                                                    17,
        "RV_POTENCIA_ATIVA":                                                                18,
        "RV_NIVEL":                                                                         19,

        "RV_ESTADO_OPERACAO":                                                               21,
        "RV_ESTADO_OPERACAO_PROCESSANDO":                                                   21, # Valor -> 0
        "RV_ESTADO_OPERACAO_DESLIGADO":                                                     21, # Valor -> 1
        "RV_ESTADO_OPERACAO_INI_START":                                                     21, # Valor -> 2
        "RV_ESTADO_OPERACAO_PARTINDO_1":                                                    21, # Valor -> 3
        "RV_ESTADO_OPERACAO_PARTINDO_2":                                                    21, # Valor -> 4
        "RV_ESTADO_OPERACAO_ABERTURA":                                                      21, # Valor -> 5
        "RV_ESTADO_OPERACAO_VELOCIDADE":                                                    21, # Valor -> 6
        "RV_ESTADO_OPERACAO_DROOP":                                                         21, # Valor -> 7
        "RV_ESTADO_OPERACAO_DROOP_EXT":                                                     21, # Valor -> 8
        "RV_ESTADO_OPERACAO_POTENCIA":                                                      21, # Valor -> 9
        "RV_ESTADO_OPERACAO_REF_POT":                                                       21, # Valor -> 10
        "RV_ESTADO_OPERACAO_NIVEL":                                                         21, # Valor -> 11
        "RV_ESTADO_OPERACAO_TIRA_CARGA":                                                    21, # Valor -> 12
        "RV_ESTADO_OPERACAO_PARADA":                                                        21, # Valor -> 13
        "RV_ESTADO_OPERACAO_POS_M_DISTR":                                                   21, # Valor -> 14
        "RV_ESTADO_OPERACAO_POS_M_ROTOR":                                                   21, # Valor -> 15
        "RV_ESTADO_OPERACAO_POS_DIGITAIS":                                                  21, # Valor -> 16
        "RV_ESTADO_OPERACAO_EMERGENCIA":                                                    21, # Valor -> 17

        "RV_CONTROLE_SINCRONIZADO_SELECIONADO":                                             22,
        "RV_CONTROLE_VAZIO_SELECIONADO":                                                    23,

        "RV_COMANDO_MODBUS":                                                                24,
        "RV_COMANDO_SEM_COMANDO":                                                           24, # Valor -> 0
        "RV_COMANDO_EMERGENCIA":                                                            24, # Valor -> 1
        "RV_COMANDO_RESET":                                                                 24, # Valor -> 2
        "RV_COMANDO_START":                                                                 24, # Valor -> 3
        "RV_COMANDO_STOP":                                                                  24, # Valor -> 4
        "RV_COMANDO_INCREMENTA":                                                            24, # Valor -> 5
        "RV_COMANDO_DECREMENTA":                                                            24, # Valor -> 6
        "RV_COMANDO_HAB_DEGRAU":                                                            24, # Valor -> 7
        "RV_COMANDO_DES_DEGRAU":                                                            24, # Valor -> 8
        "RV_COMANDO_CONTROLE_1":                                                            24, # Valor -> 9
        "RV_COMANDO_CONTROLE_2":                                                            24, # Valor -> 10
        "RV_COMANDO_AUTO":                                                                  24, # Valor -> 11
        "RV_COMANDO_MANUAL":                                                                24, # Valor -> 12
        "RV_COMANDO_HAB_POS_DISTR":                                                         24, # Valor -> 13
        "RV_COMANDO_DES_POS_DISTR":                                                         24, # Valor -> 14
        "RV_COMANDO_HAB_POS_DISTR":                                                         24, # Valor -> 15
        "RV_COMANDO_DES_POS_DISTR":                                                         24, # Valor -> 16
        "RV_COMANDO_TIRA_CARGA":                                                            24, # Valor -> 17


        ## ENTRADAS_DIGITAIS
        "RV_BLOQUEIO_EXTERNO":                                                              [25, 0],
        "RV_HABILITA_REGULADOR":                                                            [25, 1],
        "RV_SELECIONA_MODO_CONTROLE_ISOLADO":                                               [25, 2],
        "RV_ZERA_CARGA":                                                                    [25, 3],
        "RV_RESET_FALHAS":                                                                  [25, 4],
        "RV_INCREMENTA_REFERENCIA_CONTROLE":                                                [25, 5],
        "RV_DECREMENTA_REFERENCIA_CONTROLE":                                                [25, 6],
        "RV_DISJUNTOR_MAQUINA_FECHADO":                                                     [25, 7],
        "RV_PROGRAMAVEL_1":                                                                 [25, 8],
        "RV_PROGRAMAVEL_2":                                                                 [25, 9],
        "RV_PROGRAMAVEL_3":                                                                 [25, 10],
        "RV_PROGRAMAVEL_4":                                                                 [25, 11],


        ## SAÍDAS_DIGITAIS
        "RV_RELE_TRIP_ATUADO":                                                              [26, 0],
        "RV_RELE_ALARME":                                                                   [26, 1],
        "RV_RELE_REGULADOR_HABILITADO":                                                     [26, 2],
        "RV_RELE_REGULADOR_REGULANDO":                                                      [26, 3],
        "RV_RELE_POTENCIA_NULA":                                                            [26, 4],
        "RV_RELE_MAQUINA_PARADA":                                                           [26, 5],
        "RV_RELE_VELOCIDADE_MENOR_30_PU":                                                   [26, 6],
        "RV_RELE_VELOCIDADE_MAIOR_90_PU":                                                   [26, 7],
        "RV_RELE_DISTRIBUIDOR_ABERTO":                                                      [26, 8],
        "RV_PROGRAMAVEL_2":                                                                 [26, 9],
        "RV_SEGUIDOR_1":                                                                    [26, 10],
        "RV_SEGUIDOR_2":                                                                    [26, 11],


        ## LIMITES_OPERAÇÃO
        "RV_LIMITADOR_SUPERIOR_DISTRIBUIDOR_ATUADO":                                        [27, 0],
        "RV_LIMITADOR_INFERIOR_DISTRIBUIDOR_ATUADO":                                        [27, 1],
        "RV_LIMITADOR_SUPERIOR_ROTOR_ATUADO":                                               [27, 2],
        "RV_LIMITADOR_INFERIOR_ROTOR_ATUADO":                                               [27, 3],
        "RV_LIMITADOR_SUPERIOR_VELOCIDADE_ATUADO":                                          [27, 4],
        "RV_LIMITADOR_INFERIOR_VELOCIDADE_ATUADO":                                          [27, 5],
        "RV_LIMITADOR_SUPERIOR_POTENCIA_ATUADO":                                            [27, 6],
        "RV_LIMITADOR_INFERIOR_POTENCIA_ATUADO":                                            [27, 7],
        "RV_LIMITADOR_INFERIOR_NIVEL":                                                      [27, 8],
        "DEGRAU_ATUADO":                                                                    [27, 15],


        ## LEITURAS_2
        "RV_SETPOINT_ABERTURA_PU":                                                          28,
        "RV_SETPOINT_VELOCIDADE_PU":                                                        29,
        "RV_SETPOINT_POTENCIA_ATIVA_PU":                                                    30,
        "RV_REFERENCIA_NIVEL_PU":                                                           31,
        "RV_SAIDA_CONTROLE_DISTRIBUIDOR_PU":                                                32,
        "RV_SAIDA_CONTROLE_ROTOR_PU":                                                       33,
        "RV_CONTAGENS_DA_SAIDA_DISTRIBUIDOR_PU":                                            34,
        "RV_CONTAGENS_DA_SAIDA_ROTOR_PU":                                                   35,
        "RV_REFERENCIA_DISTRIBUIDOR_PU":                                                    36,
        "RV_FEEDBACK_DISTRIBUIDOR_PU":                                                      37,
        "RV_SAIDA_CONTROLE_DISTRIBUIDOR_PU":                                                38,
        "RV_ERRO_DISTRIBUIDOR_PU":                                                          39,
        "RV_INTEGRADOR_1_DISTRIBUIDOR":                                                     40,
        "RV_INTEGRADOR_2_DISTRIBUIDOR":                                                     41,
        "RV_REFERENCIA_ROTOR_PU":                                                           42,
        "RV_FEEDBACK_ROTOR_PU":                                                             43,
        "RV_SAIDA_CONTROLE_ROTOR_PU":                                                       44,
        "RV_ERRO_ROTOR_PU":                                                                 45,
        "RV_INTEGRADOR_1_ROTOR":                                                            46,
        "RV_INTEGRADOR_2_ROTOR":                                                            47,
        "RV_REFERENCIA_VELOCIDADE_PU":                                                      48,
        "RV_FEEDBACK_VELOCIDADE_PU":                                                        49,
        "RV_SAIDA_CONTROLE_VELOCIDADE_PU":                                                  50,
        "RV_ERRO_VELOCIDADE_PU":                                                            51,
        "RV_INTEGRADOR_1_POTENCIA":                                                         52,
        "RV_INTEGRADOR_2_POTENCIA":                                                         53,
        "RV_REFERENCIA_POTENCIA_ATIVA_PU":                                                  54,
        "RV_FEEDBACK_POTENCIA_ATIVA_PU":                                                    55,
        "RV_SAIDA_CONTROLE_POTENCIA_PU":                                                    56,
        "RV_ERRO_POTENCIA_PU":                                                              56,
        "RV_ERRO_POTENCIA_PU":                                                              57,
        "RV_INTEGRADOR_1_POTENCIA":                                                         58,
        "RV_INTEGRADOR_2_POTENCIA":                                                         59,
        "RV_SETPOINT_NIVEL_PU":                                                             60,
        "RV_FEEDBACK_NIVEL_PU":                                                             61,
        "RV_SAIDA_CONTROLE_NIVEL":                                                          62,
        "RV_ERRO_NIVEL_PU":                                                                 63,
        "RV_INTEGRADOR_1_NIVEL":                                                            64,
        "RV_INTEGRADOR_2_NIVEL":                                                            65,


        ## ALARME
        "RV_ALARME_SOBREFREQUENCIA":                                                        [66, 0],
        "RV_ALARME_SUBFREQUENCIA":                                                          [66, 1],
        "RV_ALARME_LEITURA_POSICAO_DISTRIBUIDOR":                                           [66, 2],
        "RV_ALARME_LEITURA_POSICAO_ROTOR":                                                  [66, 3],
        "RV_ALARME_LEITURA_POTENCIA_ATIVA":                                                 [66, 4],
        "RV_ALARME_LEITURA_REFERENCIA_POTENCIA":                                            [66, 5],
        "RV_ALARME_LEITURA_NIVEL_MONTANTE":                                                 [66, 6],
        "RV_ALARME_NIVEL_MONTANTE_MUITO_BAIXO":                                             [66, 7],
        "RV_ALARME_LEITURA_POSICAO_DISTRIBUIDOR":                                           [66, 8],
        "RV_ALARME_LEITURA_POSICAO_ROTOR":                                                  [66, 9],
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
        "RV_FALHA_SEM_PERMISSIVOS":                                                         [67, 9],
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
        "RV_BAUD_RATE":                                                                     71,
        "RV_VERSAO":                                                                        72,
        "RV_NUMERO_SERIAL":                                                                 73,
        "RV_ENDERECEO_REDE_MODBUS":                                                         74,
        "RV_NUMERO_PULSOS_ENCODER":                                                         75,
        "RV_NUMERO_DENTES_PICKUP":                                                          76,
        "RV_ROTACAO_NOMINAL":                                                               77,
        "RV_FREQUENCIA_NOMINAL":                                                            78,
        "RV_POTENCIA_REATIVA_NOMINAL":                                                      79,
        "RV_POTENCIA_ATIVA_NOMINAL":                                                        80,
        "RV_UNIDADE_PROGRAMADA":                                                            81,
        "RV_COTA_MONTANTE_MAXIMA":                                                          82,
        "RV_COTA_MONTANTE_DESLIGAMENTO":                                                    83,
        "RV_COTA_MONTANTE_CRITICA":                                                         84,

        "RV_CONTROLE_1":                                                                    85,
        "RV_CONTROLE_1_ABERTURA":                                                           85, # Valor -> 0
        "RV_CONTROLE_1_VELOCIDADE":                                                         85, # Valor -> 1
        "RV_CONTROLE_1_DROOP":                                                              85, # Valor -> 2
        "RV_CONTROLE_1_REFERENCIA_DROOP":                                                   85, # Valor -> 3
        "RV_CONTROLE_1_POTENCIA":                                                           85, # Valor -> 4
        "RV_CONTROLE_1_REFERENCIA_POTENCIA":                                                85, # Valor -> 5
        "RV_CONTROLE_1_NIVEL":                                                              85, # Valor -> 6

        "RV_CONTROLE_2":                                                                    86,
        "RV_CONTROLE_2_ABERTURA":                                                           86, # Valor -> 0
        "RV_CONTROLE_2_VELOCIDADE":                                                         86, # Valor -> 1
        "RV_CONTROLE_2_DROOP":                                                              86, # Valor -> 2
        "RV_CONTROLE_2_REFERENCIA_DROOP":                                                   86, # Valor -> 3
        "RV_CONTROLE_2_POTENCIA":                                                           86, # Valor -> 4
        "RV_CONTROLE_2_REFERENCIA_POTENCIA":                                                86, # Valor -> 5
        "RV_CONTROLE_2_NIVEL":                                                              86, # Valor -> 6

        "RV_CONFIGURACAO_CANAL_ANALOG_DISTRIBUIDOR":                                        87,
        "RV_CONFIGURACAO_CANAL_ANALOG_ROTOR":                                               88,
        "RV_CONFIGURACAO_CANAL_ANALOG_POTENCIA":                                            89,
        "RV_CONFIGURACAO_CANAL_ANALOG_REFERENCIA_POTENCIA":                                 90,
        "RV_CONFIGURACAO_CANAL_ANALOG_NIVEL":                                               91,
        "RV_CONFIGURACAO_ENTRADA_DIGITAL_PRINCIPAL":                                        92,
        "RV_CONFIGURACAO_ENTRADA_DIGITAL_RETAGUARDA":                                       93,
        "RV_PRESET_ABERTURA_PU":                                                            94,
        "RV_PRESET_VELOCIDADE_PU":                                                          95,
        "RV_PRESET_POTENCIA_PU":                                                            96,
        "RV_PRESET_NIVEL_PU":                                                               97,
        "RV_FATOR_DROOP_CONTROLE_1_PU":                                                     98,
        "RV_FATOR_DROOP_CONTROLE_2_PU":                                                     99,
        "RV_RAMPA_PID_ROTOR_PU":                                                            100,
        "RV_RAMPA_PID_DISTRIBUIDOR_PU":                                                     101,
        "RV_RAMPA_PID_VELOCIDADE_PU":                                                       102,
        "RV_RAMPA_PID_POTENCIA_PU":                                                         103,
        "RV_RAMPA_PID_NIVEL_PU":                                                            104,
        "RV_TAMANHO_DEGRAU_PU":                                                             105,
        "RV_PERCENTUAL_DESLOCAMENTO_MANUAL":                                                106,
        "RV_RAMPA_DISTIBUIDOR_CARGA_MODO_MANUAL":                                           107,
        "RV_RETRIGER_ENTRADAS_DIGITAIS":                                                    108,
        "RV_RELE_VELOCIDADE_MENOR_QUE_PU":                                                  109,
        "RV_RELE_VELOCIDADE_MAIOR_QUE_PU":                                                  110,
        "RV_RELE_PROGRAMAVEL_1":                                                            111,
        "RV_LIMITE_RELE_PROGRAMAVEL_1_PU":                                                  112,
        "RV_RELE_PROGRAMAVEL_2":                                                            113,
        "RV_LIMITE_RELE_PROGRAMAVEL_2_PU":                                                  114,
        "RV_RELE_SEGUIDOR_1":                                                               115,
        "RV_RELE_SEGUIDOR_2":                                                               116,
        "RV_ENTRADA_SEGUIDORA_1":                                                           117,
        "RV_ENTRADA_SEGUIDORA_2":                                                           118,
        "RV_ENTRADA_SEGUIDORA_3":                                                           119,
        "RV_ENTRADA_SEGUIDORA_4":                                                           120,
        "RV_CONJUGADO_DISTRIBUIDOR_1":                                                      121,
        "RV_CONJUGADO_ROTOR_1":                                                             122,
        "RV_CONJUGADO_DISTRIBUIDOR_2":                                                      123,
        "RV_CONJUGADO_ROTOR_2":                                                             124,
        "RV_CONJUGADO_DISTRIBUIDOR_3":                                                      125,
        "RV_CONJUGADO_ROTOR_3":                                                             126,
        "RV_CONJUGADO_DISTRIBUIDOR_4":                                                      127,
        "RV_CONJUGADO_ROTOR_4":                                                             128,
        "RV_CONJUGADO_DISTRIBUIDOR_5":                                                      129,
        "RV_CONJUGADO_ROTOR_5":                                                             130,
        "RV_CONJUGADO_DISTRIBUIDOR_6":                                                      131,
        "RV_CONJUGADO_ROTOR_6":                                                             132,
        "RV_CONJUGADO_DISTRIBUIDOR_7":                                                      133,
        "RV_CONJUGADO_ROTOR_7":                                                             134,
        "RV_CONJUGADO_DISTRIBUIDOR_8":                                                      135,
        "RV_CONJUGADO_ROTOR_8":                                                             136,
        "RV_CONJUGADO_DISTRIBUIDOR_9":                                                      137,
        "RV_CONJUGADO_ROTOR_9":                                                             138,
        "RV_CONJUGADO_DISTRIBUIDOR_10":                                                     139,
        "RV_CONJUGADO_ROTOR_10":                                                            140,
        "RV_CONSTANTE_PROPORCIONAL_DISTRIBUIDOR":                                           141,
        "RV_CONSTANTE_INTEGRAL_DISTRIBUIDOR":                                               142,
        "RV_CONSTANTE_DERIVATIVA_DISTRIBUIDOR":                                             143,
        "RV_CONSTANTE_PROPORCIONAL_ROTOR":                                                  144,
        "RV_CONSTANTE_INTEGRAL_ROTOR":                                                      145,
        "RV_CONSTANTE_DERIVATIVA_ROTOR":                                                    146,
        "RV_CONSTANTE_PROPORCIONAL_VELOCIDADE_VAZIO":                                       147,
        "RV_CONSTANTE_INTEGRAL_VELOCIDADE_VAZIO":                                           148,
        "RV_CONSTANTE_DERIVATIVA_VELOCIDADE_VAZIO":                                         149,
        "RV_CONSTANTE_PROPORCIONAL_VELOCIDADE_CARGA_1":                                     150,
        "RV_CONSTANTE_INTEGRAL_VELOCIDADE_CARGA_1":                                         151,
        "RV_CONSTANTE_DERIVATIVA_VELOCIDADE_CARGA_1":                                       152,
        "RV_CONSTANTE_PROPORCIONAL_VELOCIDADE_CARGA_2":                                     153,
        "RV_CONSTANTE_INTEGRAL_VELOCIDADE_CARGA_2":                                         154,
        "RV_CONSTANTE_DERIVATIVA_VELOCIDADE_CARGA_2":                                       155,
        "RV_CONSTANTE_PROPORCIONAL_POTENCIA":                                               156,
        "RV_CONSTANTE_INTEGRAL_POTENCIA":                                                   157,
        "RV_CONSTANTE_DERIVATIVA_POTENCIA":                                                 158,
        "RV_CONSTANTE_PROPORCIONAL_NIVEL":                                                  159,
        "RV_CONSTANTE_INTEGRAL_NIVEL":                                                      160,
        "RV_CONSTANTE_DERIVATIVA_NIVEL":                                                    161,
        "RV_AJUSTE_OFFSET_CANAL_1":                                                         162,
        "RV_AJUSTE_GANHO_CANAL_1":                                                          163,
        "RV_AJUSTE_OFFSET_CANAL_2":                                                         164,
        "RV_AJUSTE_GANHO_CANAL_2":                                                          165,
        "RV_AJUSTE_OFFSET_CANAL_3":                                                         166,
        "RV_AJUSTE_GANHO_CANAL_3":                                                          167,
        "RV_AJUSTE_OFFSET_CANAL_4":                                                         168,
        "RV_AJUSTE_GANHO_CANAL_4":                                                          169,
        "RV_AJUSTE_OFFSET_CANAL_4":                                                         170,
        "RV_AJUSTE_GANHO_CANAL_4":                                                          171,
        "RV_MAXIMA_SAIDA_DISTRIBUIDOR_PU":                                                  172,
        "RV_MINIMA_SAIDA_DISTRIBUIDOR_PU":                                                  173,
        "RV_ZONA_MORTA_SUP_SAIDA_DISTRIBUIDOR_PU":                                          174,
        "RV_ZONA_MORTA_INF_SAIDA_DISTRIBUIDOR_PU":                                          175,
        "RV_POLARIDADE_SAIDA_DISTRIBUIDOR":                                                 176,
        "RV_MAXIMA_SAIDA_ROTOR":                                                            177,
        "RV_MINIMA_SAIDA_ROTOR":                                                            178,
        "RV_ZONA_MORTA_SUP_SAIDA_ROTOR_PU":                                                 179,
        "RV_ZONA_MORTA_INF_SAIDA_ROTOR_PU":                                                 180,
        "RV_PALARIDADE_SAIDA_ROTOR":                                                        181,
        "RV_ABERTURA_MAXIMA_DISTRIBUIDOR":                                                  182,
        "RV_ABERTURA_MAXIMA_DISTRIBUIDOR_A_VAZIO":                                          184,
        "RV_ABERTURA_MINIMA_DISTRIBUIDOR":                                                  183,
        "RV_ABERTURA_MAXIMA_ROTOR":                                                         185,
        "RV_ABERTURA_MINIMA_ROTOR":                                                         186,
        "RV_VELOCIDADE_MAXIMA":                                                             187,
        "RV_VELOCIDADE_MINIMA":                                                             188,
        "RV_POTENCIA_MAXIMA":                                                               189,
        "RV_POTENCIA_MINIMA":                                                               190,
        "RV_TEMPORIZACAO_POTENCIA_MINIMA":                                                  191,
        "RV_LIMITE_OPERACIONAL_NIVEL_MINIMO":                                               192,
        "RV_LIMITE_ALARME_FREQUENCIA_MAXIMA":                                               193,
        "RV_LIMITE_ALARME_FREQUENCIA_MINIMA":                                               194,
        "RV_LIMITE_FALHA_FREQUENCIA_MAXIMA":                                                195,
        "RV_LIMITE_FALHA_FREQUENCIA_MINIMA":                                                196,
        "RV_LIMITE_FALHA_FREQUENCIA_INSTANTANEA":                                           197,
        "RV_LIMITE_FALHA_DIFERENCA_VELOCIDADE":                                             198,
        "RV_TEMPO_FALHA_FREQUENCIA":                                                        199,
        "RV_TEMPO_FALHA_PARTIDA":                                                           200,
        "RV_TEMPO_FALHA_ENTRADA_ANALOGICA":                                                 201,
        "RV_TEMPO_FALHA_NIVEL":                                                             202,
        "RV_TEMPO_FALHA_DISTRIBUIDOR":                                                      203,
        "RV_TEMPO_FALHA_ROTOR":                                                             204,
        "RV_TEMPO_FALHA_DIFERENCA_VELOCIDADE":                                              205,

        "RV_HABILITA_ALARME":                                                               206,
        "RV_HABILITA_ALARME_SOBREFREQUENCIA":                                               [206, 0],
        "RV_HABILITA_ALARME_SUBFREQUENCIA":                                                 [206, 1],
        "RV_HABILITA_ALARME_LEITURA_POSICAO_DISTRIBUIDOR":                                  [206, 2],
        "RV_HABILITA_ALARME_LEITURA_POSICAO_ROTOR":                                         [206, 3],
        "RV_HABILITA_ALARME_LEITURA_POTENCIA_ATIVA":                                        [206, 4],
        "RV_HABILITA_ALARME_LEITURA_REFERENCIA_POTENCIA":                                   [206, 5],
        "RV_HABILITA_ALARME_LEITURA_NIVEL_MONTANTE":                                        [206, 6],
        "RV_HABILITA_ALARME_NIVEL_MONTANTE_MUITO_BAIXO":                                    [206, 7],
        "RV_HABILITA_ALARME_POSICAO_DISTRIBUIDOR":                                          [206, 8],
        "RV_HABILITA_ALARME_POSICAO_ROTOR":                                                 [206, 9],
        "RV_HABILITA_ALARME_RUIDO_VELOCIDADE_PRINCIPAL":                                    [206, 10],
        "RV_HABILITA_ALARME_RUIDO_VELOCIDADE_RETAGUARDA":                                   [206, 11],
        
        "RV_HABILITA_FALHA_SOBREFREQUENCIA_INSTANTANEA":                                    [207, 0],
        "RV_HABILITA_FALHA_SOBREFREQUENCIA":                                                [207, 1],
        "RV_HABILITA_FALHA_SUBFREQUENCIA":                                                  [207, 2],
        "RV_HABILITA_FALHA_GIRANDO_SEM_REGULACAO":                                          [207, 3],
        "RV_HABILITA_FALHA_LEITURA_POSICAO_DISTRIBUIDOR":                                   [207, 4],
        "RV_HABILITA_FALHA_LEITURA_POSICAO_ROTOR":                                          [207, 5],
        "RV_HABILITA_FALHA_LEITURA_POTENCIA_ATIVA":                                         [207, 6],
        "RV_HABILITA_FALHA_LEITURA_REFERENCIA_POTENCIA":                                    [207, 7],
        "RV_HABILITA_FALHA_LEITURA_NIVEL_MONTANTE":                                         [207, 8],
        "RV_HABILITA_FALHA_SEM_PERMISSIVOS":                                                [207, 9],
        "RV_HABILITA_FALHA_NIVEL_MONTANTE_MUITO_BAIXO":                                     [207, 10],
        "RV_HABILITA_FALHA_POSICAO_DISTRIBUIDOR":                                           [207, 11],
        "RV_HABILITA_FALHA_POSICAO_ROTOR":                                                  [207, 12],
        "RV_HABILITA_FALHA_RUIDO_VELOCIDADE_PRINCIPAL":                                     [207, 13],
        "RV_HABILITA_FALHA_RUIDO_VELOCIDADE_RETAGUARDA":                                    [207, 14],
        "RV_HABILITA_FALHA_LEITURA_VELOCIDADE_PRINCIPAL":                                   [207, 15],

        "RV_HABILITA_FALHA_LEITURA_VELOCIDADE_RETAGUARDA":                                  [208, 0],
        "RV_HABILITA_FALHA_PARTIDA":                                                        [208, 1],
        "RV_HABILITA_FALHA_PARADA":                                                         [208, 2],
        "RV_HABILITA_FALHA_BLOQUEIO_EXTERNO":                                               [208, 3],
        "RV_HABILITA_FALHA_DIFERENCA_VELOCIDADE":                                           [208, 4],

        "RV_RAMPA_ABERTURA_INICIAL_PU":                                                     209,
        "RV_ABERTURA_INICIAL_PARTIDA_PU":                                                   210,
        "RV_VELOCIDADE_FINAL_ABERTURA_INICIAL_PU":                                          211,
        "RV_RAMPA_PARTIDA":                                                                 212,
        "RV_RAMPA_PARADA":                                                                  213,
        "RV_ROTACAO_MAQUINA_PARADA":                                                        214,
        "RV_POTENCIA_NULA":                                                                 215,
        "RV_FORCA_DISTRIBUIDOR_PARADO":                                                     216,
        "RV_FORCA_ROTOR_PARADO":                                                            217,


        ### RT
        ## LEITURAS_1
        "RT_MEDIDA_CORRENTE_EXCITACAO_PU":                                                  7,
        "RT_MEDIDA_TENSAO_EXCITACAO_PU":                                                    8,
        "RT_MEDIDA_TENSAO_MAQUINA_PU":                                                      9,
        "RT_MEDIDA_CORRENTE_MAQUINA_PU":                                                    10,
        "RT_MEDIDA_FATOR_POTENCIA_PU":                                                      11,
        "RT_MEDIDA_FREQUENCIA_PU":                                                          12,
        "RT_MEDIDA_POTENCIA_APARENTE_PU":                                                   13,
        "RT_MEDIDA_POTENCIA_ATIVA_PU":                                                      14,
        "RT_MEDIDA_POTENCIA_REATIVA_PU":                                                    15,
        "RT_CORRENTE_EXCITACAO":                                                            16,
        "RT_TENSAO_EXCITACAO":                                                              17,
        "RT_TENSAO_MAQUINA":                                                                18,
        "RT_CORRENTE_MAQUINA":                                                              19,
        "RT_FATOR_POTENCIA":                                                                20,
        "RT_FREQUENCIA":                                                                    21,
        "RT_POTENCIA_APARENTE":                                                             22,
        "RT_POTENCIA_ATIVA":                                                                23,
        "RT_POTENCIA_REATIVA":                                                              24,
        "RT_TEMPERATURA_ROTOR":                                                             25,

        "RT_ESTADO_OPERACAO":                                                               26,
        "RT_ESTADO_OPERACAO_PROCESSANDO":                                                   26, # Valor -> 0
        "RT_ESTADO_OPERACAO_DESLIGADO":                                                     26, # Valor -> 1
        "RT_ESTADO_OPERACAO_ESCORVANDO":                                                    26, # Valor -> 2
        "RT_ESTADO_OPERACAO_EXCITANDO":                                                     26, # Valor -> 3
        "RT_ESTADO_OPERACAO_ESTABILIZANDO":                                                 26, # Valor -> 4
        "RT_ESTADO_OPERACAO_FCR":                                                           26, # Valor -> 5
        "RT_ESTADO_OPERACAO_AVR":                                                           26, # Valor -> 6
        "RT_ESTADO_OPERACAO_DROOP_RT":                                                      26, # Valor -> 7
        "RT_ESTADO_OPERACAO_DROOP_FP":                                                      26, # Valor -> 8
        "RT_ESTADO_OPERACAO_QVAR":                                                          26, # Valor -> 9
        "RT_ESTADO_OPERACAO_FAT_POT":                                                       26, # Valor -> 10
        "RT_ESTADO_OPERACAO_TIRA_CARGA":                                                    26, # Valor -> 11
        "RT_ESTADO_OPERACAO_PARADA":                                                        26, # Valor -> 12
        "RT_ESTADO_OPERACAO_POS_MAN":                                                       26, # Valor -> 13
        "RT_ESTADO_OPERACAO_EMERGENCIA":                                                    26, # Valor -> 14

        "RT_CONTROLE_SINCRONIZADO_SELECIONADO":                                             27,
        "RT_CONTROLE_VAZIO_SELECIONADO":                                                    28,

        "RT_COMANDO_MODBUS":                                                                29,
        "RT_COMANDO_MODBUS_SEM_COMANDO":                                                    29, # Valor -> 0
        "RT_COMANDO_MODBUS_EMERGENCIA":                                                     29, # Valor -> 1
        "RT_COMANDO_MODBUS_RESET":                                                          29, # Valor -> 2
        "RT_COMANDO_MODBUS_START":                                                          29, # Valor -> 3
        "RT_COMANDO_MODBUS_STOP":                                                           29, # Valor -> 4
        "RT_COMANDO_MODBUS_INCREMENTA":                                                     29, # Valor -> 5
        "RT_COMANDO_MODBUS_DECREMENTA":                                                     29, # Valor -> 6
        "RT_COMANDO_MODBUS_HAB_DEGRAU":                                                     29, # Valor -> 7
        "RT_COMANDO_MODBUS_DES_DEGRAU":                                                     29, # Valor -> 8
        "RT_COMANDO_MODBUS_CONTROLE_1":                                                     29, # Valor -> 9
        "RT_COMANDO_MODBUS_CONTROLE_2":                                                     29, # Valor -> 10
        "RT_COMANDO_MODBUS_AUTO":                                                           29, # Valor -> 11
        "RT_COMANDO_MODBUS_MANUAL":                                                         29, # Valor -> 12
        "RT_COMANDO_MODBUS_HAB_POS":                                                        29, # Valor -> 13
        "RT_COMANDO_MODBUS_DES_POS":                                                        29, # Valor -> 14


        ## ENTRADAS_DIGITAIS
        "RT_BLOQUEIO_EXTERNO":                                                              [30, 0],
        "RT_HABILITA_REGULADOR":                                                            [30, 1],
        "RT_SELECIONA_MODO_CONTROLE_ISOLADO":                                               [30, 2],
        "RT_DRIVE_EXCITACAO_HABILITADO_LOGICA_DE_DISPARO":                                  [30, 3],
        "RT_RESET_FALHAS":                                                                  [30, 4],
        "RT_INCREMENTA_REFERENCIA_CONTROLE":                                                [30, 5],
        "RT_DECREMENTA_REFERENCIA_CONTROLE":                                                [30, 6],
        "RT_DISJUNTOR_MAQUINA_FECHADO":                                                     [30, 7],
        "RT_CONTATOR_CAMPO_FECHADO":                                                        [30, 8],
        "RT_CROWBAR_INATIVO":                                                               [30, 9],
        "RT_PROGRAMAVEL_1":                                                                 [30, 10],


        ## SAIDAS_DIGITAIS
        "RT_RELE_TRIP_ATUADO":                                                              [31, 0],
        "RT_RELE_ALARME":                                                                   [31, 1],
        "RT_RELE_REGULADOR_HABILITADO":                                                     [31, 2],
        "RT_RELE_REGULADOR_REGULANDO":                                                      [31, 3],
        "RT_RELE_HABILITA_DRIVE_EXCITACAO_LOGICA_DISPARO":                                  [31, 4],
        "RT_RELE_HABILITA_CONTATOR_CAMPO":                                                  [31, 5],
        "RT_RELE_HABILITA_PRE_EXCITACAO":                                                   [31, 6],
        "RT_RELE_HABILITA_CROWBAR":                                                         [31, 7],
        "RT_RELE_SAIDA_PROGRAMAVEL_1":                                                      [31, 8],
        "RT_RELE_SAIDA_PROGRAMAVEL_2":                                                      [31, 9],
        "RT_SEGUIDOR_1":                                                                    [31, 10],
        "RT_SEGUIDOR_2":                                                                    [31, 11],


        ## LIMITES_OPERAÇÃO
        "RT_LIMITADOR_SUPERIOR_CORRENTE_EXCITACAO":                                         [32, 0],
        "RT_LIMITADOR_INFERIOR_CORRENTE_EXCITACAO":                                         [32, 1],
        "RT_LIMITADOR_SUPERIOR_TENSAO_TERMINAL":                                            [32, 2],
        "RT_LIMITADOR_INFERIOR_TENSAO_TERMINAL":                                            [32, 3],
        "RT_LIMITADOR_SUPERIOR_POTENCIA_REATIVA":                                           [32, 4],
        "RT_LIMITADOR_INFERIOR_POTENCIA_REATIVA":                                           [32, 5],
        "RT_LIMITADOR_SUPERIOR_FATOR_DE_POTENCIA":                                          [32, 6],
        "RT_LIMITADOR_INFERIOR_FATOR_DE_POTENCIA":                                          [32, 7],
        "RT_LIMITADOR_MAXIMO_POTENCIA_REATIVA":                                             [32, 8],
        "RT_LIMITADOR_MINIMO_POTENCIA_REATIVA":                                             [32, 9],
        "RT_LIMITADOR_MAXIMO_FATOR_POTENCIA":                                               [32, 10],
        "RT_LIMITADOR_MINIMO_FATOR_POTENCIA":                                               [32, 11],
        "RT_LIMITADOR_VOLTZ_HERTZ":                                                         [32, 12],
        "RT_LIMITADOR_ABERTURA_PONTE":                                                      [32, 13],
        "RT_LIMITADOR_PQ_RELACAO_POTENCIA_ATIVA_X_POTENCIA_REATIVA":                        [32, 14],
        "RT_DEGRAU_ATUADO":                                                                 [32, 15],

        "RT_CONTINGENCIA_INSTUMENTACAO_REATIVO":                                            [33, 0],
        "RT_CONTINGENCIA_INSTUMENTACAO_TENSAO":                                             [33, 1],
        "RT_CONTINGENCIA_INSTUMENTACAO_EXCITACAO":                                          [33, 2],


        ## LEITURAS_2
        "RT_VALOR_LIMITE_PQ_PU":                                                            34,
        "RT_VALOR_LIMITE_ABERTURA_PU":                                                      35,
        "RT_VALOR_LIMITE_VOLTZ_HERTZ_PU":                                                   36,
        "RT_DERIVADA_POTENCIA_ATIVA_PU":                                                    37,
        "RT_EXCITACAO_SINCRONISMO_PU":                                                      38,
        "RT_REFERENCIA_EXCITACAO_PU":                                                       39,
        "RT_SETPOINT_TENSAO_PU":                                                            40,
        "RT_SETPOINT_POTENCIA_REATIVA_PU":                                                  41,
        "RT_SETPOINT_FATOR_POTENCIA_PU":                                                    42,
        "RT_ABERTURA_PONTE":                                                                43,
        "RT_CONTAGENS_DA_SAIDA_CONTROLE":                                                   44,
        "RT_CONTAGENS_DA_SAIDA_POTENCIA":                                                   45,
        "RT_REFERENCIA_CORRENTE_CAMPO_PU":                                                  46,
        "RT_FEEDBACK_CORRENTE_CAMPO_PU":                                                    47,
        "RT_SAIDA_CONTROLE_CORRENTE_CAMPO_PU":                                              48,
        "RT_ERRO_CONTROLE_CORRENTE_CAMPO_PU":                                               49,
        "RT_INTEGRADOR_1_CORRENTE_CAMPO_PU":                                                50,
        "RT_INTEGRADOR_2_CORRENTE_CAMPO_PU":                                                51,
        "RT_REFERENCIA_TENSAO_PU":                                                          52,
        "RT_FEEDBACK_TENSAO_PU":                                                            53,
        "RT_SAIDA_CONTROLE_TENSAO_PU":                                                      54,
        "RT_ERRO_TENSAO_PU":                                                                55,
        "RT_INTEGRADOR_1_TENSAO":                                                           56,
        "RT_INTEGRADOR_2_TENSAO":                                                           57,
        "RT_REFERENCIA_POTENCIA_REATIVA_PU":                                                58,
        "RT_FEEDBACK_POTENCIA_REATIVA_PU":                                                  59,
        "RT_SAIDA_CONTROLE_POTENCIA_REATIVA_PU":                                            60,
        "RT_ERRO_POTENCIA_REATIVA_PU":                                                      61,
        "RT_INTEGRADOR_1_POTENCIA_REATIVA":                                                 62,
        "RT_INTEGRADOR_2_POTENCIA_REATIVA":                                                 63,
        "RT_REFERENCIA_FATOR_POTENCIA_PU":                                                  64,
        "RT_FEEDBACK_FATOR_POTENCIA_PU":                                                    65,
        "RT_SAIDA_CONTROLE_FATOR_POTENCIA_PU":                                              66,
        "RT_ERRO_FATOR_POTENCIA_PU":                                                        67,
        "RT_INTEGRADOR_1_FATOR_POTENCIA":                                                   68,
        "RT_INTEGRADOR_2_FATOR_POTENCIA":                                                   69,


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
        "RT_FALHA_SOBRETENSAO":                                                             [72, 0],
        "RT_FALHA_SUBTENSAO":                                                               [72, 1],
        "RT_FALHA_SOBREFREQUENCIA":                                                         [72, 2],
        "RT_FALHA_SUBFREQUENCIA":                                                           [72, 3],
        "RT_FALHA_LIMITE_SUPERIOR_POTENCIA_REATIVA":                                        [72, 4],
        "RT_FALHA_LIMITE_INFERIOR_POTENCIA_REATIVA":                                        [72, 5],
        "RT_FALHA_LIMITE_SUPERIOR_FATOR_DE_POTENCIA":                                       [72, 6],
        "RT_FALHA_LIMITE_INFERIOR_FATOR_DE_POTENCIA":                                       [72, 7],
        "RT_FALHA_SOBRETENSAO_INSTANTANEA":                                                 [72, 8],
        "RT_FALHA_VARIACAO_DE_TENSAO":                                                      [72, 9],
        "RT_FALHA_POTENCIA_ATIVA_REVERSA":                                                  [72, 10],
        "RT_FALHA_SOBRECORRENTE_TERMINAL":                                                  [72, 11],
        "RT_FALHA_LIMITE_SUPERIOR_CORRENTE_EXCITACAO":                                      [72, 12],
        "RT_FALHA_LIMITE_INFERIOR_CORRENTE_EXCITACAO":                                      [72, 13],
        "RT_FALHA_LIMITE_SUPERIOR_TENSAO_EXCITACAO":                                        [72, 14],
        "RT_FALHA_LIMITE_INFERIOR_TENSAO_EXCITACAO":                                        [72, 15],


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
        "RT_BAUD_RATE":                                                                     81,
        "RT_ENDERECO_REDE_MODBUS":                                                          84,
        "RT_TENSAO_NOMINAL":                                                                85,
        "RT_POTENCIA_APARENTE_NOMINAL":                                                     86,
        "RT_FRQUENCIA_NOMINAL":                                                             87,
        "RT_CORRENTE_NOMINAL_EXCITACAO":                                                    88,
        "RT_TENSAO_NOMINAL_EXCITACAO":                                                      89,

        "RT_CONTROLE_1":                                                                    90,
        "RT_CONTROLE_1_FCR":                                                                90, # Valor -> 0
        "RT_CONTROLE_1_AVR":                                                                90, # Valor -> 1
        "RT_CONTROLE_1_DROOP_REATIVO":                                                      90, # Valor -> 2
        "RT_CONTROLE_1_DROOP_FATOR_POTENCIA":                                               90, # Valor -> 3
        "RT_CONTROLE_1_REATIVO":                                                            90, # Valor -> 4
        "RT_CONTROLE_1_FATOR_POTENCIA":                                                     90, # Valor -> 5

        "RT_CONTROLE_2":                                                                    91,
        "RT_CONTROLE_2_FCR":                                                                91, # Valor -> 0
        "RT_CONTROLE_2_AVR":                                                                91, # Valor -> 1
        "RT_CONTROLE_2_DROOP_REATIVO":                                                      91, # Valor -> 2
        "RT_CONTROLE_2_DROOP_FATOR_POTENCIA":                                               91, # Valor -> 3
        "RT_CONTROLE_2_REATIVO":                                                            91, # Valor -> 4
        "RT_CONTROLE_2_FATOR_POTENCIA":                                                     91, # Valor -> 5

        "RT_CANAL_ANALOGICO_CORRENTE_EXCITACAO_PRINCIPAL":                                  92,
        "RT_CANAL_ANALOGICO_CORRENTE_EXCITACAO_RETAGUARDA":                                 93,
        "RT_CANAL_ANALOGICO_TENSAO_EXCITACAO":                                              94,
        "RT_CANAL_ANALOGICO_TENSAO_MAQUINA":                                                95,
        "RT_CANAL_ANALOGICO_REATIVO":                                                       96,
        "RT_PRESET_CORRENTE_EXCITACAO_PU":                                                  97,
        "RT_PRESET_TENSAO_PU":                                                              98,
        "RT_PRESET_REATIVO_PU":                                                             99,
        "RT_PRESET_FATOR_POTENCIA_PU":                                                      100,
        "RT_FATOR_DROOP_CONTROLE_1_PU":                                                     101,
        "RT_FATOR_DROOP_CONTROLE_2_PU":                                                     102,
        "RT_RAMPA_PID_FCR_PUS":                                                             103,
        "RT_RAMPA_PID_AVR_PUS":                                                             104,
        "RT_RAMPA_PID_QVAR_PUS":                                                            105,
        "RT_RAMPA_PID_FATOR_POTENCIA_PUS":                                                  106,
        "RT_TAMANHO_DEGRAU_PU":                                                             107,
        "RT_PERCENTUAL_DESLOCAMENTO_MANUAL":                                                108,
        
        "RT_CONFIG_ANALOGICA":                                                              109,
        "RT_CONFIG_ANALOGICA_DESABILITA":                                                   109, # Valor -> 0
        "RT_CONFIG_ANALOGICA_SAIDA_CONTROLE_PONTE":                                         109, # Valor -> 1
        "RT_CONFIG_ANALOGICA_SAIDA_REFERENCIA_POTENCIA":                                    109, # Valor -> 2
        "RT_CONFIG_ANALOGICA_EXTERNA_IEX":                                                  109, # Valor -> 3
        "RT_CONFIG_ANALOGICA_EXTERNA_VM":                                                   109, # Valor -> 4
        "RT_CONFIG_ANALOGICA_EXTERNA_IM":                                                   109, # Valor -> 5
        "RT_CONFIG_ANALOGICA_EXTERNA_EA1":                                                  109, # Valor -> 6
        "RT_CONFIG_ANALOGICA_EXTERNA_EA2":                                                  109, # Valor -> 7
        "RT_CONFIG_ANALOGICA_EXTERNA_EA3":                                                  109, # Valor -> 8
        "RT_CONFIG_ANALOGICA_EXTERNA_EA4":                                                  109, # Valor -> 9
        "RT_CONFIG_ANALOGICA_EXTERNA_IEX_F1":                                               109, # Valor -> 10
        "RT_CONFIG_ANALOGICA_EXTERNA_VM_F1":                                                109, # Valor -> 11
        "RT_CONFIG_ANALOGICA_EXTERNA_IM_F1":                                                109, # Valor -> 12
        "RT_CONFIG_ANALOGICA_EXTERNA_EA1_F1":                                               109, # Valor -> 13
        "RT_CONFIG_ANALOGICA_EXTERNA_EA2_F1":                                               109, # Valor -> 14
        "RT_CONFIG_ANALOGICA_EXTERNA_EA3_F1":                                               109, # Valor -> 15
        "RT_CONFIG_ANALOGICA_EXTERNA_EA4_F1":                                               109, # Valor -> 16
        "RT_CONFIG_ANALOGICA_EXTERNA_FATOR_POTENCIA":                                       109, # Valor -> 17
        "RT_CONFIG_ANALOGICA_EXTERNA_FREQUENCIA":                                           109, # Valor -> 18
        "RT_CONFIG_ANALOGICA_EXTERNA_POTENCIA_APARENTE":                                    109, # Valor -> 19
        "RT_CONFIG_ANALOGICA_EXTERNA_POTENCIA_ATIVA":                                       109, # Valor -> 20
        "RT_CONFIG_ANALOGICA_EXTERNA_POTENCIA_REATIVA":                                     109, # Valor -> 21

        "RT_RETRIGGER_ENTRADAS_DIGITAIS":                                                   110,
        "RT_CONSTANTE_PROPORCIONAL_FCR_PARTIDA":                                            111,
        "RT_CONSTANTE_INTEGRAL_FCR_PARTIDA":                                                112,
        "RT_CONSTANTE_DERIVATIVA_FCR_PARTIDA":                                              113,
        "RT_CONSTANTE_PROPORCIONAL_FCR_VAZIO":                                              114,
        "RT_CONSTANTE_INTEGRAL_FCR_VAZIO":                                                  115,
        "RT_CONSTANTE_DERIVATIVA_FCR_VAZIO":                                                116,
        "RT_CONSTANTE_PROPORCIONAL_FCR_CARGA":                                              117,
        "RT_CONSTANTE_INTEGRAL_FCR_CARGA":                                                  118,
        "RT_CONSTANTE_DERIVATIVA_FCR_CARGA":                                                119,
        "RT_CONSTANTE_PROPORCIONAL_AVR_VAZIO":                                              120,
        "RT_CONSTANTE_INTEGRAL_AVR_VAZIO":                                                  121,
        "RT_CONSTANTE_DERIVATIVA_AVR_VAZIO":                                                122,
        "RT_CONSTANTE_PROPORCIONAL_AVR_CARGA_1":                                            123,
        "RT_CONSTANTE_INTEGRAL_AVR_CARGA_1":                                                124,
        "RT_CONSTANTE_DERIVATIVA_AVR_CARGA_1":                                              125,
        "RT_CONSTANTE_PROPORCIONAL_AVR_CARGA_2":                                            126,
        "RT_CONSTANTE_INTEGRAL_AVR_CARGA_2":                                                127,
        "RT_CONSTANTE_DERIVATIVA_AVR_CARGA_2":                                              128,
        "RT_CONSTANTE_PROPORCIONAL_QVAR":                                                   129,
        "RT_CONSTANTE_INTEGRAL_QVAR":                                                       130,
        "RT_CONSTANTE_DERIVATIVA_QVAR":                                                     131,
        "RT_CONSTANTE_PROPORCIONAL_FATOR_POTENCIA":                                         132,
        "RT_CONSTANTE_INTEGRAL_FATOR_POTENCIA":                                             133,
        "RT_CONSTANTE_DERIVATIVA_FATOR_POTENCIA":                                           134,
        "RT_AJUSTE_OFFSET_CANAL_SHUNT":                                                     135,
        "RT_AJUSTE_GANHO_CANAL_SHUNT":                                                      136,
        "RT_AJUSTE_OFFSET_CANAL_TP":                                                        137,
        "RT_AJUSTE_GANHO_CANAL_TP":                                                         138,
        "RT_AJUSTE_OFFSET_CANAL_TC":                                                        139,
        "RT_AJUSTE_GANHO_CANAL_TC":                                                         140,
        "RT_AJUSTE_OFFSET_CANAL_1":                                                         141,
        "RT_AJUSTE_GANHO_CANAL_1":                                                          142,
        "RT_AJUSTE_OFFSET_CANAL_2":                                                         143,
        "RT_AJUSTE_GANHO_CANAL_2":                                                          144,
        "RT_AJUSTE_OFFSET_CANAL_3":                                                         145,
        "RT_AJUSTE_GANHO_CANAL_3":                                                          146,
        "RT_AJUSTE_OFFSET_CANAL_4":                                                         147,
        "RT_AJUSTE_GANHO_CANAL_4":                                                          148,
        "RT_AJUSTE_OFFSET_FASE_TC_TP":                                                      149,
        "RT_RESERVADO":                                                                     150,
        "RT_RELE_PROGRAMAVEL_1":                                                            151,
        "RT_LIMITE_RELE_PROGRAMAVAL_1_PU":                                                  152,
        "RT_RELE_PROGRAMAVEL_2":                                                            153,
        "RT_LIMITE_RELE_PROGRAMAVAL_2_PU":                                                  154,
        "RT_RELE_SEGUIDOR_1":                                                               155,
        "RT_RELE_SEGUIDOR_2":                                                               156,
        "RT_ENTRADA_SEGUIDORA":                                                             157,
        "RT_LIMITE_PONTE_TENSAO_NULA_PU":                                                   158,
        "RT_LIMITE_PONTE_TENSAO_NOMINAL_PU":                                                159,
        "RT_LIMITE_PONTE_POTENCIA_NOMINAL_PU":                                              160,
        "RT_LIMITE_OPERACIONAL_EXCITACAO_MAX_PU":                                           161,
        "RT_LIMITE_OPERACIONAL_EXCITACAO_MIN_PU":                                           162,
        "RT_TEMPORIZACAO_EXCITACAO_MIN":                                                    163,
        "RT_LIMITE_OPERACIONAL_TENSAO_MAX_PU":                                              164,
        "RT_LIMITE_OPERACIONAL_TENSAO_MIN_PU":                                              165,
        "RT_LIMITE_OPERACIONAL_REATIVO_MAX_PU":                                             166,
        "RT_LIMITE_OPERACIONAL_REATIVO_MIN_PU":                                             167,
        "RT_LIMITE_OPERACIONAL_FATOR_POTENCIA_MAX_PU":                                      168,
        "RT_LIMITE_OPERACIONAL_FATOR_POTENCIA_MIN_PU":                                      169,
        "RT_LIMITE_OPERACIONAL_VOLTZ_HERTZ_PU":                                             170,
        "RT_TABELA PQ_20%":                                                                 171,
        "RT_TABELA PQ_40%":                                                                 172,
        "RT_TABELA PQ_60%":                                                                 173,
        "RT_TABELA PQ_80%":                                                                 174,
        "RT_TABELA PQ_100%":                                                                175,
        "RT_COMPENSACAO_POTENCIA_LIMITE_INICIAL_PU":                                        176,
        "RT_COMPENSACAO_POTENCIA_GANHO_PU":                                                 177,
        "RT_LIMITE_ALARME_TENSAO_MAX_PU":                                                   178,
        "RT_LIMITE_ALARME_TENSAO_MIN_PU":                                                   179,
        "RT_LIMITE_FALHA_INSTRU_EXCITACAO_MAX_PU":                                          180,
        "RT_LIMITE_FALHA_INSTRU_EXCITACAO_MAX_CARGA_PU":                                    181,
        "RT_LIMITE_FALHA_INSTRU_EXCITACAO_MIN_CARGA_PU":                                    182,
        "RT_LIMITE_FALHA_VELOCIDADE_EXCITACAO_MAX_PU":                                      183,
        "RT_LIMITE_FALHA_VELOCIDADE_EXCITACAO_MIN_PU":                                      184,
        "RT_LIMITE_FALHA_TENSAO_MAX_INSTANTANEA_PU":                                        185,
        "RT_LIMITE_FALHA_TENSAO_MAX_PU":                                                    186,
        "RT_LIMITE_FALHA_TENSAO_MIN_PU":                                                    187,
        "RT_LIMITE_FALHA_CORRENTE_MAQUINA_PU":                                              188,
        "RT_LIMITE_FALHA_REATIVO_MAX_PU":                                                   189,
        "RT_LIMITE_FALHA_REATIVO_MIN_PU":                                                   190,
        "RT_LIMITE_FALHA_FATOR_POTENCIA_MAX_PU":                                            191,
        "RT_LIMITE_FALHA_FATOR_POTENCIA_MIN_PU":                                            192,
        "RT_LIMITE_FALHA_FREQUENCIA_MAX_PU":                                                193,
        "RT_LIMITE_FALHA_FREQUENCIA_MIN_PU":                                                194,
        "RT_LIMITE_FALHA_CONTROLE_EXCITACAO_PU":                                            195,
        "RT_LIMITE_FALHA_CONTROLE_TENSAO_PU":                                               196,
        "RT_LIMITE_FALHA_MAX_TENSAO_SEM_EXCITACAO_PU":                                      197,
        "RT_LIMITE_FALHA_MAX_EXCITACAO_SEM_TENSAO_PU":                                      198,
        "RT_LIMITE_FALHA_DVDT_PU":                                                          199,
        "RT_LIMITE_FALHA_TEMPERATURA_MAX_PU":                                               200,
        "RT_LIMITE_POTENCIA_NEGATIVA_PU":                                                   201,
        "RT_TEMPO_FALHA_INSTRUM_EXCITCAO":                                                  202,
        "RT_TEMPO_FALHA_VELOCIDADE_EXCITCAO":                                               203,
        "RT_TEMPO_FALHA_TENSAO":                                                            204,
        "RT_TEMPO_FALHA_MAX_CORRENTE_MAQUINA":                                              205,
        "RT_TEMPO_FALHA_REATIVO":                                                           206,
        "RT_TEMPO_FALHA_FATOR_POTENCIA":                                                    207,
        "RT_TEMPO_FALHA_FREQUENCIA":                                                        208,
        "RT_TEMPO_FALHA_POTENCIA_REVERSA":                                                  209,
        "RT_TEMPO_FALHA_CONTROLE_EXCITACAO":                                                210,
        "RT_TEMPO_FALHA_CONTROLE_TENSAO":                                                   211,
        "RT_TEMPO_FALHA_PARTIDA":                                                           212,
        "RT_TEMPO_FALHA_PARADA":                                                            213,
        "RT_TEMPO_FALHA_PRE_EXCITACAO":                                                     214,
        "RT_TEMPO_FALHA_EXCITACAO":                                                         215,

        "RT_HABILITA_ALARME_1":                                                             216,
        "RT_HABILITA_ALARME_1_SOBRETENSAO":                                                 [216, 0],
        "RT_HABILITA_ALARME_1_SUBTENSAO":                                                   [216, 1],
        "RT_HABILITA_ALARME_1_SOBREFREQUENCIA":                                             [216, 2],
        "RT_HABILITA_ALARME_1_SUBFREQUENCIA":                                               [216, 3],
        "RT_HABILITA_ALARME_1_MAX_REATIVO":                                                 [216, 4],
        "RT_HABILITA_ALARME_1_MIN_REATIVO":                                                 [216, 5],
        "RT_HABILITA_ALARME_1_MAX_FATOR_POTENCIA":                                          [216, 6],
        "RT_HABILITA_ALARME_1_MIN_FATOR_POTENCIA":                                          [216, 7],
        "RT_HABILITA_ALARME_1_DVDT":                                                        [216, 8],
        "RT_HABILITA_ALARME_1_POTENCIA_REVERSA":                                            [216, 9],
        "RT_HABILITA_ALARME_1_MAX_CORRENTE_MAQUINA":                                        [216, 10],
        "RT_HABILITA_ALARME_1_MAX_CORRENTE_EXCITACAO":                                      [216, 11],
        "RT_HABILITA_ALARME_1_MIN_CORRENTE_EXCITACAO":                                      [216, 12],
        "RT_HABILITA_ALARME_1_MAX_TEMPERATURA":                                             [216, 13],
        "RT_HABILITA_ALARME_1_MAX_TENSAO_SEM_EXCITACAO":                                    [216, 14],
        "RT_HABILITA_ALARME_1_MAX_EXCITACAO_SEM_TENSAO":                                    [216, 15],

        "RT_HABILITA_ALARME_2":                                                             217,
        "RT_HABILITA_ALARME_2_CONTROLE_EXCITACAO":                                          [217, 0],
        "RT_HABILITA_ALARME_2_CONTROLE_TENSAO":                                             [217, 1],
        "RT_HABILITA_ALARME_2_CROWBAR":                                                     [217, 2],
        "RT_HABILITA_ALARME_2_DRIVE_EXCITACAO":                                             [217, 3],
        "RT_HABILITA_ALARME_2_CONTATORA_CAMPO":                                             [217, 4],
        "RT_HABILITA_ALARME_2_INSTR_REATIVO":                                               [217, 5],
        "RT_HABILITA_ALARME_2_INSTR_TENSAO":                                                [217, 6],
        "RT_HABILITA_ALARME_2_INSTR_EXCITACAO_PRINCIPAL":                                   [217, 7],
        "RT_HABILITA_ALARME_2_INSTR_EXCITACAO_RETAGUARDA":                                  [217, 8],
        "RT_HABILITA_ALARME_2_RUIDO_INSTR_REATIVO":                                         [217, 9],
        "RT_HABILITA_ALARME_2_RUIDO_INSTR_TENSAO":                                          [217, 10],
        "RT_HABILITA_ALARME_2_RUIDO_INSTR_EXCITACAO_PRINCIPAL":                             [217, 11],
        "RT_HABILITA_ALARME_2_RUIDO_INSTR_EXCITACAO_RETAGUARDA":                            [217, 12],

        "RT_HABILITA_FALHA_1":                                                              218,
        "RT_HABILITA_FALHA_1_SOBRETENSAO":                                                  [218, 0],
        "RT_HABILITA_FALHA_1_SUBTENSAO":                                                    [218, 1],
        "RT_HABILITA_FALHA_1_SOBREFREQUENCIA":                                              [218, 2],
        "RT_HABILITA_FALHA_1_SUBFREQUENCIA":                                                [218, 3],
        "RT_HABILITA_FALHA_1_MAX_REATIVO":                                                  [218, 4],
        "RT_HABILITA_FALHA_1_MIN_RETAIVO":                                                  [218, 5],
        "RT_HABILITA_FALHA_1_MAX_FATOR_POTENCIA":                                           [218, 6],
        "RT_HABILITA_FALHA_1_MIN_FATOR_POTENCIA":                                           [218, 7],
        "RT_HABILITA_FALHA_1_MAX_TENSAO_INSTANTANEA":                                       [218, 8],
        "RT_HABILITA_FALHA_1_DVDT":                                                         [218, 9],
        "RT_HABILITA_FALHA_1_POTENCIA_REVERSA":                                             [218, 10],
        "RT_HABILITA_FALHA_1_MAX_CORRENTE_MAQUINA":                                         [218, 11],
        "RT_HABILITA_FALHA_1_MAX_CORRENTE_EXCITACAO":                                       [218, 12],

        "RT_HABILITA_FALHA_2":                                                              219,
        "RT_HABILITA_FALHA_2_MAX_TEMPERATURA":                                              [219, 0],
        "RT_HABILITA_FALHA_2_TENSAO_SEM_EXCITACAO":                                         [219, 1],
        "RT_HABILITA_FALHA_2_EXCITACAO_SEM_TENSAO":                                         [219, 2],
        "RT_HABILITA_FALHA_2_CONTROLE_EXCITACAO":                                           [219, 3],
        "RT_HABILITA_FALHA_2_CONTROLE_TENSAO":                                              [219, 4],
        "RT_HABILITA_FALHA_2_CROWBAR":                                                      [219, 5],
        "RT_HABILITA_FALHA_2_DRIVE_EXCITACAO":                                              [219, 6],
        "RT_HABILITA_FALHA_2_CONTATORA_CAMPO":                                              [219, 7],
        "RT_HABILITA_FALHA_2_PRE_EXCITACAO":                                                [219, 8],
        "RT_HABILITA_FALHA_2_TIMEOUT_PRE_EXCITACAO":                                        [219, 9],
        "RT_HABILITA_FALHA_2_PARADA":                                                       [219, 10],
        "RT_HABILITA_FALHA_2_PARTIDA":                                                      [219, 11],
        "RT_HABILITA_FALHA_2_TRIP_EXTERNO":                                                 [219, 12],

        "RT_HABILITA_FALHAS_3":                                                             220,
        "RT_HABILITA_FALHAS_3_INSTRU_REATIVO":                                              [220, 0],
        "RT_HABILITA_FALHAS_3_INSTRU_TENSAO":                                               [220, 1],
        "RT_HABILITA_FALHAS_3_INSTRU_EXCITACAO_PRINCIPAL":                                  [220, 2],
        "RT_HABILITA_FALHAS_3_INSTRU_EXCITACAO_RETAGUARDA":                                 [220, 3],
        "RT_HABILITA_FALHAS_3_RUIDO_INSTRU_REATIVO":                                        [220, 4],
        "RT_HABILITA_FALHAS_3_RUIDO_INSTRU_TENSAO":                                         [220, 5],
        "RT_HABILITA_FALHAS_3_RUIDO_INSTRU_EXCITACAO_PRINCIPAL":                            [220, 6],
        "RT_HABILITA_FALHAS_3_RUIDO_INSTRU_EXCITACAO_RETAGUARDA":                           [220, 7],

        "RT_TENSAO_LIMITE_PRE_EXCITCAO_PU":                                                 221,
        "RT_CORRENTE_EXCITACAO_LIMITE_PRE_EXCITADO_PU":                                     222,
        "RT_ANGULO_ABERTURA_ESCORVAMENTO_PU":                                               223,
        "RT_CORRENTE_EXCITACAO_LIMITE_ESTABILIZADO_PU":                                     224,
        "RT_RAMPA_PARTIDA":                                                                 225,
        "RT_RAMPA_PARADA":                                                                  226,
    },

    "UG2":{
        ### RV
        ## LEITURAS_1
        "RV_POSICAO_DISTRIBUIDOR_PU":                                                       7,
        "RV_POSICAO_ROTOR_PU":                                                              8,
        "RV_VELOCIDADE_PU":                                                                 9,
        "RV_POTENCIA_ATIVA_PU":                                                             10,
        "RV_NIVEL_PU":                                                                      11,
        "RV_REFERENCIA_POTENCIA_PU":                                                        12,
        "RV_POSICAO_DISTRIBUIDOR":                                                          14,
        "RV_POSICAO_ROTOR":                                                                 15,
        "RV_ROTACAO":                                                                       16,
        "RV_FREQUENCIA":                                                                    17,
        "RV_POTENCIA_ATIVA":                                                                18,
        "RV_NIVEL":                                                                         19,

        "RV_ESTADO_OPERACAO":                                                               21,
        "RV_ESTADO_OPERACAO_PROCESSANDO":                                                   21, # Valor -> 0
        "RV_ESTADO_OPERACAO_DESLIGADO":                                                     21, # Valor -> 1
        "RV_ESTADO_OPERACAO_INI_START":                                                     21, # Valor -> 2
        "RV_ESTADO_OPERACAO_PARTINDO_1":                                                    21, # Valor -> 3
        "RV_ESTADO_OPERACAO_PARTINDO_2":                                                    21, # Valor -> 4
        "RV_ESTADO_OPERACAO_ABERTURA":                                                      21, # Valor -> 5
        "RV_ESTADO_OPERACAO_VELOCIDADE":                                                    21, # Valor -> 6
        "RV_ESTADO_OPERACAO_DROOP":                                                         21, # Valor -> 7
        "RV_ESTADO_OPERACAO_DROOP_EXT":                                                     21, # Valor -> 8
        "RV_ESTADO_OPERACAO_POTENCIA":                                                      21, # Valor -> 9
        "RV_ESTADO_OPERACAO_REF_POT":                                                       21, # Valor -> 10
        "RV_ESTADO_OPERACAO_NIVEL":                                                         21, # Valor -> 11
        "RV_ESTADO_OPERACAO_TIRA_CARGA":                                                    21, # Valor -> 12
        "RV_ESTADO_OPERACAO_PARADA":                                                        21, # Valor -> 13
        "RV_ESTADO_OPERACAO_POS_M_DISTR":                                                   21, # Valor -> 14
        "RV_ESTADO_OPERACAO_POS_M_ROTOR":                                                   21, # Valor -> 15
        "RV_ESTADO_OPERACAO_POS_DIGITAIS":                                                  21, # Valor -> 16
        "RV_ESTADO_OPERACAO_EMERGENCIA":                                                    21, # Valor -> 17

        "RV_CONTROLE_SINCRONIZADO_SELECIONADO":                                             22,
        "RV_CONTROLE_VAZIO_SELECIONADO":                                                    23,

        "RV_COMANDO_MODBUS":                                                                24,
        "RV_COMANDO_SEM_COMANDO":                                                           24, # Valor -> 0
        "RV_COMANDO_EMERGENCIA":                                                            24, # Valor -> 1
        "RV_COMANDO_RESET":                                                                 24, # Valor -> 2
        "RV_COMANDO_START":                                                                 24, # Valor -> 3
        "RV_COMANDO_STOP":                                                                  24, # Valor -> 4
        "RV_COMANDO_INCREMENTA":                                                            24, # Valor -> 5
        "RV_COMANDO_DECREMENTA":                                                            24, # Valor -> 6
        "RV_COMANDO_HAB_DEGRAU":                                                            24, # Valor -> 7
        "RV_COMANDO_DES_DEGRAU":                                                            24, # Valor -> 8
        "RV_COMANDO_CONTROLE_1":                                                            24, # Valor -> 9
        "RV_COMANDO_CONTROLE_2":                                                            24, # Valor -> 10
        "RV_COMANDO_AUTO":                                                                  24, # Valor -> 11
        "RV_COMANDO_MANUAL":                                                                24, # Valor -> 12
        "RV_COMANDO_HAB_POS_DISTR":                                                         24, # Valor -> 13
        "RV_COMANDO_DES_POS_DISTR":                                                         24, # Valor -> 14
        "RV_COMANDO_HAB_POS_DISTR":                                                         24, # Valor -> 15
        "RV_COMANDO_DES_POS_DISTR":                                                         24, # Valor -> 16
        "RV_COMANDO_TIRA_CARGA":                                                            24, # Valor -> 17


        ## ENTRADAS_DIGITAIS
        "RV_BLOQUEIO_EXTERNO":                                                              [25, 0],
        "RV_HABILITA_REGULADOR":                                                            [25, 1],
        "RV_SELECIONA_MODO_CONTROLE_ISOLADO":                                               [25, 2],
        "RV_ZERA_CARGA":                                                                    [25, 3],
        "RV_RESET_FALHAS":                                                                  [25, 4],
        "RV_INCREMENTA_REFERENCIA_CONTROLE":                                                [25, 5],
        "RV_DECREMENTA_REFERENCIA_CONTROLE":                                                [25, 6],
        "RV_DISJUNTOR_MAQUINA_FECHADO":                                                     [25, 7],
        "RV_PROGRAMAVEL_1":                                                                 [25, 8],
        "RV_PROGRAMAVEL_2":                                                                 [25, 9],
        "RV_PROGRAMAVEL_3":                                                                 [25, 10],
        "RV_PROGRAMAVEL_4":                                                                 [25, 11],


        ## SAÍDAS_DIGITAIS
        "RV_RELE_TRIP_ATUADO":                                                              [26, 0],
        "RV_RELE_ALARME":                                                                   [26, 1],
        "RV_RELE_REGULADOR_HABILITADO":                                                     [26, 2],
        "RV_RELE_REGULADOR_REGULANDO":                                                      [26, 3],
        "RV_RELE_POTENCIA_NULA":                                                            [26, 4],
        "RV_RELE_MAQUINA_PARADA":                                                           [26, 5],
        "RV_RELE_VELOCIDADE_MENOR_30_PU":                                                   [26, 6],
        "RV_RELE_VELOCIDADE_MAIOR_90_PU":                                                   [26, 7],
        "RV_RELE_DISTRIBUIDOR_ABERTO":                                                      [26, 8],
        "RV_PROGRAMAVEL_2":                                                                 [26, 9],
        "RV_SEGUIDOR_1":                                                                    [26, 10],
        "RV_SEGUIDOR_2":                                                                    [26, 11],


        ## LIMITES_OPERAÇÃO
        "RV_LIMITADOR_SUPERIOR_DISTRIBUIDOR_ATUADO":                                        [27, 0],
        "RV_LIMITADOR_INFERIOR_DISTRIBUIDOR_ATUADO":                                        [27, 1],
        "RV_LIMITADOR_SUPERIOR_ROTOR_ATUADO":                                               [27, 2],
        "RV_LIMITADOR_INFERIOR_ROTOR_ATUADO":                                               [27, 3],
        "RV_LIMITADOR_SUPERIOR_VELOCIDADE_ATUADO":                                          [27, 4],
        "RV_LIMITADOR_INFERIOR_VELOCIDADE_ATUADO":                                          [27, 5],
        "RV_LIMITADOR_SUPERIOR_POTENCIA_ATUADO":                                            [27, 6],
        "RV_LIMITADOR_INFERIOR_POTENCIA_ATUADO":                                            [27, 7],
        "RV_LIMITADOR_INFERIOR_NIVEL":                                                      [27, 8],
        "DEGRAU_ATUADO":                                                                    [27, 15],


        ## LEITURAS_2
        "RV_SETPOINT_ABERTURA_PU":                                                          28,
        "RV_SETPOINT_VELOCIDADE_PU":                                                        29,
        "RV_SETPOINT_POTENCIA_ATIVA_PU":                                                    30,
        "RV_REFERENCIA_NIVEL_PU":                                                           31,
        "RV_SAIDA_CONTROLE_DISTRIBUIDOR_PU":                                                32,
        "RV_SAIDA_CONTROLE_ROTOR_PU":                                                       33,
        "RV_CONTAGENS_DA_SAIDA_DISTRIBUIDOR_PU":                                            34,
        "RV_CONTAGENS_DA_SAIDA_ROTOR_PU":                                                   35,
        "RV_REFERENCIA_DISTRIBUIDOR_PU":                                                    36,
        "RV_FEEDBACK_DISTRIBUIDOR_PU":                                                      37,
        "RV_SAIDA_CONTROLE_DISTRIBUIDOR_PU":                                                38,
        "RV_ERRO_DISTRIBUIDOR_PU":                                                          39,
        "RV_INTEGRADOR_1_DISTRIBUIDOR":                                                     40,
        "RV_INTEGRADOR_2_DISTRIBUIDOR":                                                     41,
        "RV_REFERENCIA_ROTOR_PU":                                                           42,
        "RV_FEEDBACK_ROTOR_PU":                                                             43,
        "RV_SAIDA_CONTROLE_ROTOR_PU":                                                       44,
        "RV_ERRO_ROTOR_PU":                                                                 45,
        "RV_INTEGRADOR_1_ROTOR":                                                            46,
        "RV_INTEGRADOR_2_ROTOR":                                                            47,
        "RV_REFERENCIA_VELOCIDADE_PU":                                                      48,
        "RV_FEEDBACK_VELOCIDADE_PU":                                                        49,
        "RV_SAIDA_CONTROLE_VELOCIDADE_PU":                                                  50,
        "RV_ERRO_VELOCIDADE_PU":                                                            51,
        "RV_INTEGRADOR_1_POTENCIA":                                                         52,
        "RV_INTEGRADOR_2_POTENCIA":                                                         53,
        "RV_REFERENCIA_POTENCIA_ATIVA_PU":                                                  54,
        "RV_FEEDBACK_POTENCIA_ATIVA_PU":                                                    55,
        "RV_SAIDA_CONTROLE_POTENCIA_PU":                                                    56,
        "RV_ERRO_POTENCIA_PU":                                                              56,
        "RV_ERRO_POTENCIA_PU":                                                              57,
        "RV_INTEGRADOR_1_POTENCIA":                                                         58,
        "RV_INTEGRADOR_2_POTENCIA":                                                         59,
        "RV_SETPOINT_NIVEL_PU":                                                             60,
        "RV_FEEDBACK_NIVEL_PU":                                                             61,
        "RV_SAIDA_CONTROLE_NIVEL":                                                          62,
        "RV_ERRO_NIVEL_PU":                                                                 63,
        "RV_INTEGRADOR_1_NIVEL":                                                            64,
        "RV_INTEGRADOR_2_NIVEL":                                                            65,


        ## ALARME
        "RV_ALARME_SOBREFREQUENCIA":                                                        [66, 0],
        "RV_ALARME_SUBFREQUENCIA":                                                          [66, 1],
        "RV_ALARME_LEITURA_POSICAO_DISTRIBUIDOR":                                           [66, 2],
        "RV_ALARME_LEITURA_POSICAO_ROTOR":                                                  [66, 3],
        "RV_ALARME_LEITURA_POTENCIA_ATIVA":                                                 [66, 4],
        "RV_ALARME_LEITURA_REFERENCIA_POTENCIA":                                            [66, 5],
        "RV_ALARME_LEITURA_NIVEL_MONTANTE":                                                 [66, 6],
        "RV_ALARME_NIVEL_MONTANTE_MUITO_BAIXO":                                             [66, 7],
        "RV_ALARME_LEITURA_POSICAO_DISTRIBUIDOR":                                           [66, 8],
        "RV_ALARME_LEITURA_POSICAO_ROTOR":                                                  [66, 9],
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
        "RV_FALHA_SEM_PERMISSIVOS":                                                         [67, 9],
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
        "RV_BAUD_RATE":                                                                     71,
        "RV_VERSAO":                                                                        72,
        "RV_NUMERO_SERIAL":                                                                 73,
        "RV_ENDERECEO_REDE_MODBUS":                                                         74,
        "RV_NUMERO_PULSOS_ENCODER":                                                         75,
        "RV_NUMERO_DENTES_PICKUP":                                                          76,
        "RV_ROTACAO_NOMINAL":                                                               77,
        "RV_FREQUENCIA_NOMINAL":                                                            78,
        "RV_POTENCIA_REATIVA_NOMINAL":                                                      79,
        "RV_POTENCIA_ATIVA_NOMINAL":                                                        80,
        "RV_UNIDADE_PROGRAMADA":                                                            81,
        "RV_COTA_MONTANTE_MAXIMA":                                                          82,
        "RV_COTA_MONTANTE_DESLIGAMENTO":                                                    83,
        "RV_COTA_MONTANTE_CRITICA":                                                         84,

        "RV_CONTROLE_1":                                                                    85,
        "RV_CONTROLE_1_ABERTURA":                                                           85, # Valor -> 0
        "RV_CONTROLE_1_VELOCIDADE":                                                         85, # Valor -> 1
        "RV_CONTROLE_1_DROOP":                                                              85, # Valor -> 2
        "RV_CONTROLE_1_REFERENCIA_DROOP":                                                   85, # Valor -> 3
        "RV_CONTROLE_1_POTENCIA":                                                           85, # Valor -> 4
        "RV_CONTROLE_1_REFERENCIA_POTENCIA":                                                85, # Valor -> 5
        "RV_CONTROLE_1_NIVEL":                                                              85, # Valor -> 6

        "RV_CONTROLE_2":                                                                    86,
        "RV_CONTROLE_2_ABERTURA":                                                           86, # Valor -> 0
        "RV_CONTROLE_2_VELOCIDADE":                                                         86, # Valor -> 1
        "RV_CONTROLE_2_DROOP":                                                              86, # Valor -> 2
        "RV_CONTROLE_2_REFERENCIA_DROOP":                                                   86, # Valor -> 3
        "RV_CONTROLE_2_POTENCIA":                                                           86, # Valor -> 4
        "RV_CONTROLE_2_REFERENCIA_POTENCIA":                                                86, # Valor -> 5
        "RV_CONTROLE_2_NIVEL":                                                              86, # Valor -> 6

        "RV_CONFIGURACAO_CANAL_ANALOG_DISTRIBUIDOR":                                        87,
        "RV_CONFIGURACAO_CANAL_ANALOG_ROTOR":                                               88,
        "RV_CONFIGURACAO_CANAL_ANALOG_POTENCIA":                                            89,
        "RV_CONFIGURACAO_CANAL_ANALOG_REFERENCIA_POTENCIA":                                 90,
        "RV_CONFIGURACAO_CANAL_ANALOG_NIVEL":                                               91,
        "RV_CONFIGURACAO_ENTRADA_DIGITAL_PRINCIPAL":                                        92,
        "RV_CONFIGURACAO_ENTRADA_DIGITAL_RETAGUARDA":                                       93,
        "RV_PRESET_ABERTURA_PU":                                                            94,
        "RV_PRESET_VELOCIDADE_PU":                                                          95,
        "RV_PRESET_POTENCIA_PU":                                                            96,
        "RV_PRESET_NIVEL_PU":                                                               97,
        "RV_FATOR_DROOP_CONTROLE_1_PU":                                                     98,
        "RV_FATOR_DROOP_CONTROLE_2_PU":                                                     99,
        "RV_RAMPA_PID_ROTOR_PU":                                                            100,
        "RV_RAMPA_PID_DISTRIBUIDOR_PU":                                                     101,
        "RV_RAMPA_PID_VELOCIDADE_PU":                                                       102,
        "RV_RAMPA_PID_POTENCIA_PU":                                                         103,
        "RV_RAMPA_PID_NIVEL_PU":                                                            104,
        "RV_TAMANHO_DEGRAU_PU":                                                             105,
        "RV_PERCENTUAL_DESLOCAMENTO_MANUAL":                                                106,
        "RV_RAMPA_DISTIBUIDOR_CARGA_MODO_MANUAL":                                           107,
        "RV_RETRIGER_ENTRADAS_DIGITAIS":                                                    108,
        "RV_RELE_VELOCIDADE_MENOR_QUE_PU":                                                  109,
        "RV_RELE_VELOCIDADE_MAIOR_QUE_PU":                                                  110,
        "RV_RELE_PROGRAMAVEL_1":                                                            111,
        "RV_LIMITE_RELE_PROGRAMAVEL_1_PU":                                                  112,
        "RV_RELE_PROGRAMAVEL_2":                                                            113,
        "RV_LIMITE_RELE_PROGRAMAVEL_2_PU":                                                  114,
        "RV_RELE_SEGUIDOR_1":                                                               115,
        "RV_RELE_SEGUIDOR_2":                                                               116,
        "RV_ENTRADA_SEGUIDORA_1":                                                           117,
        "RV_ENTRADA_SEGUIDORA_2":                                                           118,
        "RV_ENTRADA_SEGUIDORA_3":                                                           119,
        "RV_ENTRADA_SEGUIDORA_4":                                                           120,
        "RV_CONJUGADO_DISTRIBUIDOR_1":                                                      121,
        "RV_CONJUGADO_ROTOR_1":                                                             122,
        "RV_CONJUGADO_DISTRIBUIDOR_2":                                                      123,
        "RV_CONJUGADO_ROTOR_2":                                                             124,
        "RV_CONJUGADO_DISTRIBUIDOR_3":                                                      125,
        "RV_CONJUGADO_ROTOR_3":                                                             126,
        "RV_CONJUGADO_DISTRIBUIDOR_4":                                                      127,
        "RV_CONJUGADO_ROTOR_4":                                                             128,
        "RV_CONJUGADO_DISTRIBUIDOR_5":                                                      129,
        "RV_CONJUGADO_ROTOR_5":                                                             130,
        "RV_CONJUGADO_DISTRIBUIDOR_6":                                                      131,
        "RV_CONJUGADO_ROTOR_6":                                                             132,
        "RV_CONJUGADO_DISTRIBUIDOR_7":                                                      133,
        "RV_CONJUGADO_ROTOR_7":                                                             134,
        "RV_CONJUGADO_DISTRIBUIDOR_8":                                                      135,
        "RV_CONJUGADO_ROTOR_8":                                                             136,
        "RV_CONJUGADO_DISTRIBUIDOR_9":                                                      137,
        "RV_CONJUGADO_ROTOR_9":                                                             138,
        "RV_CONJUGADO_DISTRIBUIDOR_10":                                                     139,
        "RV_CONJUGADO_ROTOR_10":                                                            140,
        "RV_CONSTANTE_PROPORCIONAL_DISTRIBUIDOR":                                           141,
        "RV_CONSTANTE_INTEGRAL_DISTRIBUIDOR":                                               142,
        "RV_CONSTANTE_DERIVATIVA_DISTRIBUIDOR":                                             143,
        "RV_CONSTANTE_PROPORCIONAL_ROTOR":                                                  144,
        "RV_CONSTANTE_INTEGRAL_ROTOR":                                                      145,
        "RV_CONSTANTE_DERIVATIVA_ROTOR":                                                    146,
        "RV_CONSTANTE_PROPORCIONAL_VELOCIDADE_VAZIO":                                       147,
        "RV_CONSTANTE_INTEGRAL_VELOCIDADE_VAZIO":                                           148,
        "RV_CONSTANTE_DERIVATIVA_VELOCIDADE_VAZIO":                                         149,
        "RV_CONSTANTE_PROPORCIONAL_VELOCIDADE_CARGA_1":                                     150,
        "RV_CONSTANTE_INTEGRAL_VELOCIDADE_CARGA_1":                                         151,
        "RV_CONSTANTE_DERIVATIVA_VELOCIDADE_CARGA_1":                                       152,
        "RV_CONSTANTE_PROPORCIONAL_VELOCIDADE_CARGA_2":                                     153,
        "RV_CONSTANTE_INTEGRAL_VELOCIDADE_CARGA_2":                                         154,
        "RV_CONSTANTE_DERIVATIVA_VELOCIDADE_CARGA_2":                                       155,
        "RV_CONSTANTE_PROPORCIONAL_POTENCIA":                                               156,
        "RV_CONSTANTE_INTEGRAL_POTENCIA":                                                   157,
        "RV_CONSTANTE_DERIVATIVA_POTENCIA":                                                 158,
        "RV_CONSTANTE_PROPORCIONAL_NIVEL":                                                  159,
        "RV_CONSTANTE_INTEGRAL_NIVEL":                                                      160,
        "RV_CONSTANTE_DERIVATIVA_NIVEL":                                                    161,
        "RV_AJUSTE_OFFSET_CANAL_1":                                                         162,
        "RV_AJUSTE_GANHO_CANAL_1":                                                          163,
        "RV_AJUSTE_OFFSET_CANAL_2":                                                         164,
        "RV_AJUSTE_GANHO_CANAL_2":                                                          165,
        "RV_AJUSTE_OFFSET_CANAL_3":                                                         166,
        "RV_AJUSTE_GANHO_CANAL_3":                                                          167,
        "RV_AJUSTE_OFFSET_CANAL_4":                                                         168,
        "RV_AJUSTE_GANHO_CANAL_4":                                                          169,
        "RV_AJUSTE_OFFSET_CANAL_4":                                                         170,
        "RV_AJUSTE_GANHO_CANAL_4":                                                          171,
        "RV_MAXIMA_SAIDA_DISTRIBUIDOR_PU":                                                  172,
        "RV_MINIMA_SAIDA_DISTRIBUIDOR_PU":                                                  173,
        "RV_ZONA_MORTA_SUP_SAIDA_DISTRIBUIDOR_PU":                                          174,
        "RV_ZONA_MORTA_INF_SAIDA_DISTRIBUIDOR_PU":                                          175,
        "RV_POLARIDADE_SAIDA_DISTRIBUIDOR":                                                 176,
        "RV_MAXIMA_SAIDA_ROTOR":                                                            177,
        "RV_MINIMA_SAIDA_ROTOR":                                                            178,
        "RV_ZONA_MORTA_SUP_SAIDA_ROTOR_PU":                                                 179,
        "RV_ZONA_MORTA_INF_SAIDA_ROTOR_PU":                                                 180,
        "RV_PALARIDADE_SAIDA_ROTOR":                                                        181,
        "RV_ABERTURA_MAXIMA_DISTRIBUIDOR":                                                  182,
        "RV_ABERTURA_MAXIMA_DISTRIBUIDOR_A_VAZIO":                                          184,
        "RV_ABERTURA_MINIMA_DISTRIBUIDOR":                                                  183,
        "RV_ABERTURA_MAXIMA_ROTOR":                                                         185,
        "RV_ABERTURA_MINIMA_ROTOR":                                                         186,
        "RV_VELOCIDADE_MAXIMA":                                                             187,
        "RV_VELOCIDADE_MINIMA":                                                             188,
        "RV_POTENCIA_MAXIMA":                                                               189,
        "RV_POTENCIA_MINIMA":                                                               190,
        "RV_TEMPORIZACAO_POTENCIA_MINIMA":                                                  191,
        "RV_LIMITE_OPERACIONAL_NIVEL_MINIMO":                                               192,
        "RV_LIMITE_ALARME_FREQUENCIA_MAXIMA":                                               193,
        "RV_LIMITE_ALARME_FREQUENCIA_MINIMA":                                               194,
        "RV_LIMITE_FALHA_FREQUENCIA_MAXIMA":                                                195,
        "RV_LIMITE_FALHA_FREQUENCIA_MINIMA":                                                196,
        "RV_LIMITE_FALHA_FREQUENCIA_INSTANTANEA":                                           197,
        "RV_LIMITE_FALHA_DIFERENCA_VELOCIDADE":                                             198,
        "RV_TEMPO_FALHA_FREQUENCIA":                                                        199,
        "RV_TEMPO_FALHA_PARTIDA":                                                           200,
        "RV_TEMPO_FALHA_ENTRADA_ANALOGICA":                                                 201,
        "RV_TEMPO_FALHA_NIVEL":                                                             202,
        "RV_TEMPO_FALHA_DISTRIBUIDOR":                                                      203,
        "RV_TEMPO_FALHA_ROTOR":                                                             204,
        "RV_TEMPO_FALHA_DIFERENCA_VELOCIDADE":                                              205,

        "RV_HABILITA_ALARME":                                                               206,
        "RV_HABILITA_ALARME_SOBREFREQUENCIA":                                               [206, 0],
        "RV_HABILITA_ALARME_SUBFREQUENCIA":                                                 [206, 1],
        "RV_HABILITA_ALARME_LEITURA_POSICAO_DISTRIBUIDOR":                                  [206, 2],
        "RV_HABILITA_ALARME_LEITURA_POSICAO_ROTOR":                                         [206, 3],
        "RV_HABILITA_ALARME_LEITURA_POTENCIA_ATIVA":                                        [206, 4],
        "RV_HABILITA_ALARME_LEITURA_REFERENCIA_POTENCIA":                                   [206, 5],
        "RV_HABILITA_ALARME_LEITURA_NIVEL_MONTANTE":                                        [206, 6],
        "RV_HABILITA_ALARME_NIVEL_MONTANTE_MUITO_BAIXO":                                    [206, 7],
        "RV_HABILITA_ALARME_POSICAO_DISTRIBUIDOR":                                          [206, 8],
        "RV_HABILITA_ALARME_POSICAO_ROTOR":                                                 [206, 9],
        "RV_HABILITA_ALARME_RUIDO_VELOCIDADE_PRINCIPAL":                                    [206, 10],
        "RV_HABILITA_ALARME_RUIDO_VELOCIDADE_RETAGUARDA":                                   [206, 11],
        
        "RV_HABILITA_FALHA_SOBREFREQUENCIA_INSTANTANEA":                                    [207, 0],
        "RV_HABILITA_FALHA_SOBREFREQUENCIA":                                                [207, 1],
        "RV_HABILITA_FALHA_SUBFREQUENCIA":                                                  [207, 2],
        "RV_HABILITA_FALHA_GIRANDO_SEM_REGULACAO":                                          [207, 3],
        "RV_HABILITA_FALHA_LEITURA_POSICAO_DISTRIBUIDOR":                                   [207, 4],
        "RV_HABILITA_FALHA_LEITURA_POSICAO_ROTOR":                                          [207, 5],
        "RV_HABILITA_FALHA_LEITURA_POTENCIA_ATIVA":                                         [207, 6],
        "RV_HABILITA_FALHA_LEITURA_REFERENCIA_POTENCIA":                                    [207, 7],
        "RV_HABILITA_FALHA_LEITURA_NIVEL_MONTANTE":                                         [207, 8],
        "RV_HABILITA_FALHA_SEM_PERMISSIVOS":                                                [207, 9],
        "RV_HABILITA_FALHA_NIVEL_MONTANTE_MUITO_BAIXO":                                     [207, 10],
        "RV_HABILITA_FALHA_POSICAO_DISTRIBUIDOR":                                           [207, 11],
        "RV_HABILITA_FALHA_POSICAO_ROTOR":                                                  [207, 12],
        "RV_HABILITA_FALHA_RUIDO_VELOCIDADE_PRINCIPAL":                                     [207, 13],
        "RV_HABILITA_FALHA_RUIDO_VELOCIDADE_RETAGUARDA":                                    [207, 14],
        "RV_HABILITA_FALHA_LEITURA_VELOCIDADE_PRINCIPAL":                                   [207, 15],

        "RV_HABILITA_FALHA_LEITURA_VELOCIDADE_RETAGUARDA":                                  [208, 0],
        "RV_HABILITA_FALHA_PARTIDA":                                                        [208, 1],
        "RV_HABILITA_FALHA_PARADA":                                                         [208, 2],
        "RV_HABILITA_FALHA_BLOQUEIO_EXTERNO":                                               [208, 3],
        "RV_HABILITA_FALHA_DIFERENCA_VELOCIDADE":                                           [208, 4],

        "RV_RAMPA_ABERTURA_INICIAL_PU":                                                     209,
        "RV_ABERTURA_INICIAL_PARTIDA_PU":                                                   210,
        "RV_VELOCIDADE_FINAL_ABERTURA_INICIAL_PU":                                          211,
        "RV_RAMPA_PARTIDA":                                                                 212,
        "RV_RAMPA_PARADA":                                                                  213,
        "RV_ROTACAO_MAQUINA_PARADA":                                                        214,
        "RV_POTENCIA_NULA":                                                                 215,
        "RV_FORCA_DISTRIBUIDOR_PARADO":                                                     216,
        "RV_FORCA_ROTOR_PARADO":                                                            217,


        ### RT
        ## LEITURAS_1
        "RT_MEDIDA_CORRENTE_EXCITACAO_PU":                                                  7,
        "RT_MEDIDA_TENSAO_EXCITACAO_PU":                                                    8,
        "RT_MEDIDA_TENSAO_MAQUINA_PU":                                                      9,
        "RT_MEDIDA_CORRENTE_MAQUINA_PU":                                                    10,
        "RT_MEDIDA_FATOR_POTENCIA_PU":                                                      11,
        "RT_MEDIDA_FREQUENCIA_PU":                                                          12,
        "RT_MEDIDA_POTENCIA_APARENTE_PU":                                                   13,
        "RT_MEDIDA_POTENCIA_ATIVA_PU":                                                      14,
        "RT_MEDIDA_POTENCIA_REATIVA_PU":                                                    15,
        "RT_CORRENTE_EXCITACAO":                                                            16,
        "RT_TENSAO_EXCITACAO":                                                              17,
        "RT_TENSAO_MAQUINA":                                                                18,
        "RT_CORRENTE_MAQUINA":                                                              19,
        "RT_FATOR_POTENCIA":                                                                20,
        "RT_FREQUENCIA":                                                                    21,
        "RT_POTENCIA_APARENTE":                                                             22,
        "RT_POTENCIA_ATIVA":                                                                23,
        "RT_POTENCIA_REATIVA":                                                              24,
        "RT_TEMPERATURA_ROTOR":                                                             25,

        "RT_ESTADO_OPERACAO":                                                               26,
        "RT_ESTADO_OPERACAO_PROCESSANDO":                                                   26, # Valor -> 0
        "RT_ESTADO_OPERACAO_DESLIGADO":                                                     26, # Valor -> 1
        "RT_ESTADO_OPERACAO_ESCORVANDO":                                                    26, # Valor -> 2
        "RT_ESTADO_OPERACAO_EXCITANDO":                                                     26, # Valor -> 3
        "RT_ESTADO_OPERACAO_ESTABILIZANDO":                                                 26, # Valor -> 4
        "RT_ESTADO_OPERACAO_FCR":                                                           26, # Valor -> 5
        "RT_ESTADO_OPERACAO_AVR":                                                           26, # Valor -> 6
        "RT_ESTADO_OPERACAO_DROOP_RT":                                                      26, # Valor -> 7
        "RT_ESTADO_OPERACAO_DROOP_FP":                                                      26, # Valor -> 8
        "RT_ESTADO_OPERACAO_QVAR":                                                          26, # Valor -> 9
        "RT_ESTADO_OPERACAO_FAT_POT":                                                       26, # Valor -> 10
        "RT_ESTADO_OPERACAO_TIRA_CARGA":                                                    26, # Valor -> 11
        "RT_ESTADO_OPERACAO_PARADA":                                                        26, # Valor -> 12
        "RT_ESTADO_OPERACAO_POS_MAN":                                                       26, # Valor -> 13
        "RT_ESTADO_OPERACAO_EMERGENCIA":                                                    26, # Valor -> 14

        "RT_CONTROLE_SINCRONIZADO_SELECIONADO":                                             27,
        "RT_CONTROLE_VAZIO_SELECIONADO":                                                    28,

        "RT_COMANDO_MODBUS":                                                                29,
        "RT_COMANDO_MODBUS_SEM_COMANDO":                                                    29, # Valor -> 0
        "RT_COMANDO_MODBUS_EMERGENCIA":                                                     29, # Valor -> 1
        "RT_COMANDO_MODBUS_RESET":                                                          29, # Valor -> 2
        "RT_COMANDO_MODBUS_START":                                                          29, # Valor -> 3
        "RT_COMANDO_MODBUS_STOP":                                                           29, # Valor -> 4
        "RT_COMANDO_MODBUS_INCREMENTA":                                                     29, # Valor -> 5
        "RT_COMANDO_MODBUS_DECREMENTA":                                                     29, # Valor -> 6
        "RT_COMANDO_MODBUS_HAB_DEGRAU":                                                     29, # Valor -> 7
        "RT_COMANDO_MODBUS_DES_DEGRAU":                                                     29, # Valor -> 8
        "RT_COMANDO_MODBUS_CONTROLE_1":                                                     29, # Valor -> 9
        "RT_COMANDO_MODBUS_CONTROLE_2":                                                     29, # Valor -> 10
        "RT_COMANDO_MODBUS_AUTO":                                                           29, # Valor -> 11
        "RT_COMANDO_MODBUS_MANUAL":                                                         29, # Valor -> 12
        "RT_COMANDO_MODBUS_HAB_POS":                                                        29, # Valor -> 13
        "RT_COMANDO_MODBUS_DES_POS":                                                        29, # Valor -> 14


        ## ENTRADAS_DIGITAIS
        "RT_BLOQUEIO_EXTERNO":                                                              [30, 0],
        "RT_HABILITA_REGULADOR":                                                            [30, 1],
        "RT_SELECIONA_MODO_CONTROLE_ISOLADO":                                               [30, 2],
        "RT_DRIVE_EXCITACAO_HABILITADO_LOGICA_DE_DISPARO":                                  [30, 3],
        "RT_RESET_FALHAS":                                                                  [30, 4],
        "RT_INCREMENTA_REFERENCIA_CONTROLE":                                                [30, 5],
        "RT_DECREMENTA_REFERENCIA_CONTROLE":                                                [30, 6],
        "RT_DISJUNTOR_MAQUINA_FECHADO":                                                     [30, 7],
        "RT_CONTATOR_CAMPO_FECHADO":                                                        [30, 8],
        "RT_CROWBAR_INATIVO":                                                               [30, 9],
        "RT_PROGRAMAVEL_1":                                                                 [30, 10],


        ## SAIDAS_DIGITAIS
        "RT_RELE_TRIP_ATUADO":                                                              [31, 0],
        "RT_RELE_ALARME":                                                                   [31, 1],
        "RT_RELE_REGULADOR_HABILITADO":                                                     [31, 2],
        "RT_RELE_REGULADOR_REGULANDO":                                                      [31, 3],
        "RT_RELE_HABILITA_DRIVE_EXCITACAO_LOGICA_DISPARO":                                  [31, 4],
        "RT_RELE_HABILITA_CONTATOR_CAMPO":                                                  [31, 5],
        "RT_RELE_HABILITA_PRE_EXCITACAO":                                                   [31, 6],
        "RT_RELE_HABILITA_CROWBAR":                                                         [31, 7],
        "RT_RELE_SAIDA_PROGRAMAVEL_1":                                                      [31, 8],
        "RT_RELE_SAIDA_PROGRAMAVEL_2":                                                      [31, 9],
        "RT_SEGUIDOR_1":                                                                    [31, 10],
        "RT_SEGUIDOR_2":                                                                    [31, 11],


        ## LIMITES_OPERAÇÃO
        "RT_LIMITADOR_SUPERIOR_CORRENTE_EXCITACAO":                                         [32, 0],
        "RT_LIMITADOR_INFERIOR_CORRENTE_EXCITACAO":                                         [32, 1],
        "RT_LIMITADOR_SUPERIOR_TENSAO_TERMINAL":                                            [32, 2],
        "RT_LIMITADOR_INFERIOR_TENSAO_TERMINAL":                                            [32, 3],
        "RT_LIMITADOR_SUPERIOR_POTENCIA_REATIVA":                                           [32, 4],
        "RT_LIMITADOR_INFERIOR_POTENCIA_REATIVA":                                           [32, 5],
        "RT_LIMITADOR_SUPERIOR_FATOR_DE_POTENCIA":                                          [32, 6],
        "RT_LIMITADOR_INFERIOR_FATOR_DE_POTENCIA":                                          [32, 7],
        "RT_LIMITADOR_MAXIMO_POTENCIA_REATIVA":                                             [32, 8],
        "RT_LIMITADOR_MINIMO_POTENCIA_REATIVA":                                             [32, 9],
        "RT_LIMITADOR_MAXIMO_FATOR_POTENCIA":                                               [32, 10],
        "RT_LIMITADOR_MINIMO_FATOR_POTENCIA":                                               [32, 11],
        "RT_LIMITADOR_VOLTZ_HERTZ":                                                         [32, 12],
        "RT_LIMITADOR_ABERTURA_PONTE":                                                      [32, 13],
        "RT_LIMITADOR_PQ_RELACAO_POTENCIA_ATIVA_X_POTENCIA_REATIVA":                        [32, 14],
        "RT_DEGRAU_ATUADO":                                                                 [32, 15],

        "RT_CONTINGENCIA_INSTUMENTACAO_REATIVO":                                            [33, 0],
        "RT_CONTINGENCIA_INSTUMENTACAO_TENSAO":                                             [33, 1],
        "RT_CONTINGENCIA_INSTUMENTACAO_EXCITACAO":                                          [33, 2],


        ## LEITURAS_2
        "RT_VALOR_LIMITE_PQ_PU":                                                            34,
        "RT_VALOR_LIMITE_ABERTURA_PU":                                                      35,
        "RT_VALOR_LIMITE_VOLTZ_HERTZ_PU":                                                   36,
        "RT_DERIVADA_POTENCIA_ATIVA_PU":                                                    37,
        "RT_EXCITACAO_SINCRONISMO_PU":                                                      38,
        "RT_REFERENCIA_EXCITACAO_PU":                                                       39,
        "RT_SETPOINT_TENSAO_PU":                                                            40,
        "RT_SETPOINT_POTENCIA_REATIVA_PU":                                                  41,
        "RT_SETPOINT_FATOR_POTENCIA_PU":                                                    42,
        "RT_ABERTURA_PONTE":                                                                43,
        "RT_CONTAGENS_DA_SAIDA_CONTROLE":                                                   44,
        "RT_CONTAGENS_DA_SAIDA_POTENCIA":                                                   45,
        "RT_REFERENCIA_CORRENTE_CAMPO_PU":                                                  46,
        "RT_FEEDBACK_CORRENTE_CAMPO_PU":                                                    47,
        "RT_SAIDA_CONTROLE_CORRENTE_CAMPO_PU":                                              48,
        "RT_ERRO_CONTROLE_CORRENTE_CAMPO_PU":                                               49,
        "RT_INTEGRADOR_1_CORRENTE_CAMPO_PU":                                                50,
        "RT_INTEGRADOR_2_CORRENTE_CAMPO_PU":                                                51,
        "RT_REFERENCIA_TENSAO_PU":                                                          52,
        "RT_FEEDBACK_TENSAO_PU":                                                            53,
        "RT_SAIDA_CONTROLE_TENSAO_PU":                                                      54,
        "RT_ERRO_TENSAO_PU":                                                                55,
        "RT_INTEGRADOR_1_TENSAO":                                                           56,
        "RT_INTEGRADOR_2_TENSAO":                                                           57,
        "RT_REFERENCIA_POTENCIA_REATIVA_PU":                                                58,
        "RT_FEEDBACK_POTENCIA_REATIVA_PU":                                                  59,
        "RT_SAIDA_CONTROLE_POTENCIA_REATIVA_PU":                                            60,
        "RT_ERRO_POTENCIA_REATIVA_PU":                                                      61,
        "RT_INTEGRADOR_1_POTENCIA_REATIVA":                                                 62,
        "RT_INTEGRADOR_2_POTENCIA_REATIVA":                                                 63,
        "RT_REFERENCIA_FATOR_POTENCIA_PU":                                                  64,
        "RT_FEEDBACK_FATOR_POTENCIA_PU":                                                    65,
        "RT_SAIDA_CONTROLE_FATOR_POTENCIA_PU":                                              66,
        "RT_ERRO_FATOR_POTENCIA_PU":                                                        67,
        "RT_INTEGRADOR_1_FATOR_POTENCIA":                                                   68,
        "RT_INTEGRADOR_2_FATOR_POTENCIA":                                                   69,


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
        "RT_FALHA_SOBRETENSAO":                                                             [72, 0],
        "RT_FALHA_SUBTENSAO":                                                               [72, 1],
        "RT_FALHA_SOBREFREQUENCIA":                                                         [72, 2],
        "RT_FALHA_SUBFREQUENCIA":                                                           [72, 3],
        "RT_FALHA_LIMITE_SUPERIOR_POTENCIA_REATIVA":                                        [72, 4],
        "RT_FALHA_LIMITE_INFERIOR_POTENCIA_REATIVA":                                        [72, 5],
        "RT_FALHA_LIMITE_SUPERIOR_FATOR_DE_POTENCIA":                                       [72, 6],
        "RT_FALHA_LIMITE_INFERIOR_FATOR_DE_POTENCIA":                                       [72, 7],
        "RT_FALHA_SOBRETENSAO_INSTANTANEA":                                                 [72, 8],
        "RT_FALHA_VARIACAO_DE_TENSAO":                                                      [72, 9],
        "RT_FALHA_POTENCIA_ATIVA_REVERSA":                                                  [72, 10],
        "RT_FALHA_SOBRECORRENTE_TERMINAL":                                                  [72, 11],
        "RT_FALHA_LIMITE_SUPERIOR_CORRENTE_EXCITACAO":                                      [72, 12],
        "RT_FALHA_LIMITE_INFERIOR_CORRENTE_EXCITACAO":                                      [72, 13],
        "RT_FALHA_LIMITE_SUPERIOR_TENSAO_EXCITACAO":                                        [72, 14],
        "RT_FALHA_LIMITE_INFERIOR_TENSAO_EXCITACAO":                                        [72, 15],


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
        "RT_BAUD_RATE":                                                                     81,
        "RT_ENDERECO_REDE_MODBUS":                                                          84,
        "RT_TENSAO_NOMINAL":                                                                85,
        "RT_POTENCIA_APARENTE_NOMINAL":                                                     86,
        "RT_FRQUENCIA_NOMINAL":                                                             87,
        "RT_CORRENTE_NOMINAL_EXCITACAO":                                                    88,
        "RT_TENSAO_NOMINAL_EXCITACAO":                                                      89,

        "RT_CONTROLE_1":                                                                    90,
        "RT_CONTROLE_1_FCR":                                                                90, # Valor -> 0
        "RT_CONTROLE_1_AVR":                                                                90, # Valor -> 1
        "RT_CONTROLE_1_DROOP_REATIVO":                                                      90, # Valor -> 2
        "RT_CONTROLE_1_DROOP_FATOR_POTENCIA":                                               90, # Valor -> 3
        "RT_CONTROLE_1_REATIVO":                                                            90, # Valor -> 4
        "RT_CONTROLE_1_FATOR_POTENCIA":                                                     90, # Valor -> 5

        "RT_CONTROLE_2":                                                                    91,
        "RT_CONTROLE_2_FCR":                                                                91, # Valor -> 0
        "RT_CONTROLE_2_AVR":                                                                91, # Valor -> 1
        "RT_CONTROLE_2_DROOP_REATIVO":                                                      91, # Valor -> 2
        "RT_CONTROLE_2_DROOP_FATOR_POTENCIA":                                               91, # Valor -> 3
        "RT_CONTROLE_2_REATIVO":                                                            91, # Valor -> 4
        "RT_CONTROLE_2_FATOR_POTENCIA":                                                     91, # Valor -> 5

        "RT_CANAL_ANALOGICO_CORRENTE_EXCITACAO_PRINCIPAL":                                  92,
        "RT_CANAL_ANALOGICO_CORRENTE_EXCITACAO_RETAGUARDA":                                 93,
        "RT_CANAL_ANALOGICO_TENSAO_EXCITACAO":                                              94,
        "RT_CANAL_ANALOGICO_TENSAO_MAQUINA":                                                95,
        "RT_CANAL_ANALOGICO_REATIVO":                                                       96,
        "RT_PRESET_CORRENTE_EXCITACAO_PU":                                                  97,
        "RT_PRESET_TENSAO_PU":                                                              98,
        "RT_PRESET_REATIVO_PU":                                                             99,
        "RT_PRESET_FATOR_POTENCIA_PU":                                                      100,
        "RT_FATOR_DROOP_CONTROLE_1_PU":                                                     101,
        "RT_FATOR_DROOP_CONTROLE_2_PU":                                                     102,
        "RT_RAMPA_PID_FCR_PUS":                                                             103,
        "RT_RAMPA_PID_AVR_PUS":                                                             104,
        "RT_RAMPA_PID_QVAR_PUS":                                                            105,
        "RT_RAMPA_PID_FATOR_POTENCIA_PUS":                                                  106,
        "RT_TAMANHO_DEGRAU_PU":                                                             107,
        "RT_PERCENTUAL_DESLOCAMENTO_MANUAL":                                                108,
        
        "RT_CONFIG_ANALOGICA":                                                              109,
        "RT_CONFIG_ANALOGICA_DESABILITA":                                                   109, # Valor -> 0
        "RT_CONFIG_ANALOGICA_SAIDA_CONTROLE_PONTE":                                         109, # Valor -> 1
        "RT_CONFIG_ANALOGICA_SAIDA_REFERENCIA_POTENCIA":                                    109, # Valor -> 2
        "RT_CONFIG_ANALOGICA_EXTERNA_IEX":                                                  109, # Valor -> 3
        "RT_CONFIG_ANALOGICA_EXTERNA_VM":                                                   109, # Valor -> 4
        "RT_CONFIG_ANALOGICA_EXTERNA_IM":                                                   109, # Valor -> 5
        "RT_CONFIG_ANALOGICA_EXTERNA_EA1":                                                  109, # Valor -> 6
        "RT_CONFIG_ANALOGICA_EXTERNA_EA2":                                                  109, # Valor -> 7
        "RT_CONFIG_ANALOGICA_EXTERNA_EA3":                                                  109, # Valor -> 8
        "RT_CONFIG_ANALOGICA_EXTERNA_EA4":                                                  109, # Valor -> 9
        "RT_CONFIG_ANALOGICA_EXTERNA_IEX_F1":                                               109, # Valor -> 10
        "RT_CONFIG_ANALOGICA_EXTERNA_VM_F1":                                                109, # Valor -> 11
        "RT_CONFIG_ANALOGICA_EXTERNA_IM_F1":                                                109, # Valor -> 12
        "RT_CONFIG_ANALOGICA_EXTERNA_EA1_F1":                                               109, # Valor -> 13
        "RT_CONFIG_ANALOGICA_EXTERNA_EA2_F1":                                               109, # Valor -> 14
        "RT_CONFIG_ANALOGICA_EXTERNA_EA3_F1":                                               109, # Valor -> 15
        "RT_CONFIG_ANALOGICA_EXTERNA_EA4_F1":                                               109, # Valor -> 16
        "RT_CONFIG_ANALOGICA_EXTERNA_FATOR_POTENCIA":                                       109, # Valor -> 17
        "RT_CONFIG_ANALOGICA_EXTERNA_FREQUENCIA":                                           109, # Valor -> 18
        "RT_CONFIG_ANALOGICA_EXTERNA_POTENCIA_APARENTE":                                    109, # Valor -> 19
        "RT_CONFIG_ANALOGICA_EXTERNA_POTENCIA_ATIVA":                                       109, # Valor -> 20
        "RT_CONFIG_ANALOGICA_EXTERNA_POTENCIA_REATIVA":                                     109, # Valor -> 21

        "RT_RETRIGGER_ENTRADAS_DIGITAIS":                                                   110,
        "RT_CONSTANTE_PROPORCIONAL_FCR_PARTIDA":                                            111,
        "RT_CONSTANTE_INTEGRAL_FCR_PARTIDA":                                                112,
        "RT_CONSTANTE_DERIVATIVA_FCR_PARTIDA":                                              113,
        "RT_CONSTANTE_PROPORCIONAL_FCR_VAZIO":                                              114,
        "RT_CONSTANTE_INTEGRAL_FCR_VAZIO":                                                  115,
        "RT_CONSTANTE_DERIVATIVA_FCR_VAZIO":                                                116,
        "RT_CONSTANTE_PROPORCIONAL_FCR_CARGA":                                              117,
        "RT_CONSTANTE_INTEGRAL_FCR_CARGA":                                                  118,
        "RT_CONSTANTE_DERIVATIVA_FCR_CARGA":                                                119,
        "RT_CONSTANTE_PROPORCIONAL_AVR_VAZIO":                                              120,
        "RT_CONSTANTE_INTEGRAL_AVR_VAZIO":                                                  121,
        "RT_CONSTANTE_DERIVATIVA_AVR_VAZIO":                                                122,
        "RT_CONSTANTE_PROPORCIONAL_AVR_CARGA_1":                                            123,
        "RT_CONSTANTE_INTEGRAL_AVR_CARGA_1":                                                124,
        "RT_CONSTANTE_DERIVATIVA_AVR_CARGA_1":                                              125,
        "RT_CONSTANTE_PROPORCIONAL_AVR_CARGA_2":                                            126,
        "RT_CONSTANTE_INTEGRAL_AVR_CARGA_2":                                                127,
        "RT_CONSTANTE_DERIVATIVA_AVR_CARGA_2":                                              128,
        "RT_CONSTANTE_PROPORCIONAL_QVAR":                                                   129,
        "RT_CONSTANTE_INTEGRAL_QVAR":                                                       130,
        "RT_CONSTANTE_DERIVATIVA_QVAR":                                                     131,
        "RT_CONSTANTE_PROPORCIONAL_FATOR_POTENCIA":                                         132,
        "RT_CONSTANTE_INTEGRAL_FATOR_POTENCIA":                                             133,
        "RT_CONSTANTE_DERIVATIVA_FATOR_POTENCIA":                                           134,
        "RT_AJUSTE_OFFSET_CANAL_SHUNT":                                                     135,
        "RT_AJUSTE_GANHO_CANAL_SHUNT":                                                      136,
        "RT_AJUSTE_OFFSET_CANAL_TP":                                                        137,
        "RT_AJUSTE_GANHO_CANAL_TP":                                                         138,
        "RT_AJUSTE_OFFSET_CANAL_TC":                                                        139,
        "RT_AJUSTE_GANHO_CANAL_TC":                                                         140,
        "RT_AJUSTE_OFFSET_CANAL_1":                                                         141,
        "RT_AJUSTE_GANHO_CANAL_1":                                                          142,
        "RT_AJUSTE_OFFSET_CANAL_2":                                                         143,
        "RT_AJUSTE_GANHO_CANAL_2":                                                          144,
        "RT_AJUSTE_OFFSET_CANAL_3":                                                         145,
        "RT_AJUSTE_GANHO_CANAL_3":                                                          146,
        "RT_AJUSTE_OFFSET_CANAL_4":                                                         147,
        "RT_AJUSTE_GANHO_CANAL_4":                                                          148,
        "RT_AJUSTE_OFFSET_FASE_TC_TP":                                                      149,
        "RT_RESERVADO":                                                                     150,
        "RT_RELE_PROGRAMAVEL_1":                                                            151,
        "RT_LIMITE_RELE_PROGRAMAVAL_1_PU":                                                  152,
        "RT_RELE_PROGRAMAVEL_2":                                                            153,
        "RT_LIMITE_RELE_PROGRAMAVAL_2_PU":                                                  154,
        "RT_RELE_SEGUIDOR_1":                                                               155,
        "RT_RELE_SEGUIDOR_2":                                                               156,
        "RT_ENTRADA_SEGUIDORA":                                                             157,
        "RT_LIMITE_PONTE_TENSAO_NULA_PU":                                                   158,
        "RT_LIMITE_PONTE_TENSAO_NOMINAL_PU":                                                159,
        "RT_LIMITE_PONTE_POTENCIA_NOMINAL_PU":                                              160,
        "RT_LIMITE_OPERACIONAL_EXCITACAO_MAX_PU":                                           161,
        "RT_LIMITE_OPERACIONAL_EXCITACAO_MIN_PU":                                           162,
        "RT_TEMPORIZACAO_EXCITACAO_MIN":                                                    163,
        "RT_LIMITE_OPERACIONAL_TENSAO_MAX_PU":                                              164,
        "RT_LIMITE_OPERACIONAL_TENSAO_MIN_PU":                                              165,
        "RT_LIMITE_OPERACIONAL_REATIVO_MAX_PU":                                             166,
        "RT_LIMITE_OPERACIONAL_REATIVO_MIN_PU":                                             167,
        "RT_LIMITE_OPERACIONAL_FATOR_POTENCIA_MAX_PU":                                      168,
        "RT_LIMITE_OPERACIONAL_FATOR_POTENCIA_MIN_PU":                                      169,
        "RT_LIMITE_OPERACIONAL_VOLTZ_HERTZ_PU":                                             170,
        "RT_TABELA PQ_20%":                                                                 171,
        "RT_TABELA PQ_40%":                                                                 172,
        "RT_TABELA PQ_60%":                                                                 173,
        "RT_TABELA PQ_80%":                                                                 174,
        "RT_TABELA PQ_100%":                                                                175,
        "RT_COMPENSACAO_POTENCIA_LIMITE_INICIAL_PU":                                        176,
        "RT_COMPENSACAO_POTENCIA_GANHO_PU":                                                 177,
        "RT_LIMITE_ALARME_TENSAO_MAX_PU":                                                   178,
        "RT_LIMITE_ALARME_TENSAO_MIN_PU":                                                   179,
        "RT_LIMITE_FALHA_INSTRU_EXCITACAO_MAX_PU":                                          180,
        "RT_LIMITE_FALHA_INSTRU_EXCITACAO_MAX_CARGA_PU":                                    181,
        "RT_LIMITE_FALHA_INSTRU_EXCITACAO_MIN_CARGA_PU":                                    182,
        "RT_LIMITE_FALHA_VELOCIDADE_EXCITACAO_MAX_PU":                                      183,
        "RT_LIMITE_FALHA_VELOCIDADE_EXCITACAO_MIN_PU":                                      184,
        "RT_LIMITE_FALHA_TENSAO_MAX_INSTANTANEA_PU":                                        185,
        "RT_LIMITE_FALHA_TENSAO_MAX_PU":                                                    186,
        "RT_LIMITE_FALHA_TENSAO_MIN_PU":                                                    187,
        "RT_LIMITE_FALHA_CORRENTE_MAQUINA_PU":                                              188,
        "RT_LIMITE_FALHA_REATIVO_MAX_PU":                                                   189,
        "RT_LIMITE_FALHA_REATIVO_MIN_PU":                                                   190,
        "RT_LIMITE_FALHA_FATOR_POTENCIA_MAX_PU":                                            191,
        "RT_LIMITE_FALHA_FATOR_POTENCIA_MIN_PU":                                            192,
        "RT_LIMITE_FALHA_FREQUENCIA_MAX_PU":                                                193,
        "RT_LIMITE_FALHA_FREQUENCIA_MIN_PU":                                                194,
        "RT_LIMITE_FALHA_CONTROLE_EXCITACAO_PU":                                            195,
        "RT_LIMITE_FALHA_CONTROLE_TENSAO_PU":                                               196,
        "RT_LIMITE_FALHA_MAX_TENSAO_SEM_EXCITACAO_PU":                                      197,
        "RT_LIMITE_FALHA_MAX_EXCITACAO_SEM_TENSAO_PU":                                      198,
        "RT_LIMITE_FALHA_DVDT_PU":                                                          199,
        "RT_LIMITE_FALHA_TEMPERATURA_MAX_PU":                                               200,
        "RT_LIMITE_POTENCIA_NEGATIVA_PU":                                                   201,
        "RT_TEMPO_FALHA_INSTRUM_EXCITCAO":                                                  202,
        "RT_TEMPO_FALHA_VELOCIDADE_EXCITCAO":                                               203,
        "RT_TEMPO_FALHA_TENSAO":                                                            204,
        "RT_TEMPO_FALHA_MAX_CORRENTE_MAQUINA":                                              205,
        "RT_TEMPO_FALHA_REATIVO":                                                           206,
        "RT_TEMPO_FALHA_FATOR_POTENCIA":                                                    207,
        "RT_TEMPO_FALHA_FREQUENCIA":                                                        208,
        "RT_TEMPO_FALHA_POTENCIA_REVERSA":                                                  209,
        "RT_TEMPO_FALHA_CONTROLE_EXCITACAO":                                                210,
        "RT_TEMPO_FALHA_CONTROLE_TENSAO":                                                   211,
        "RT_TEMPO_FALHA_PARTIDA":                                                           212,
        "RT_TEMPO_FALHA_PARADA":                                                            213,
        "RT_TEMPO_FALHA_PRE_EXCITACAO":                                                     214,
        "RT_TEMPO_FALHA_EXCITACAO":                                                         215,

        "RT_HABILITA_ALARME_1":                                                             216,
        "RT_HABILITA_ALARME_1_SOBRETENSAO":                                                 [216, 0],
        "RT_HABILITA_ALARME_1_SUBTENSAO":                                                   [216, 1],
        "RT_HABILITA_ALARME_1_SOBREFREQUENCIA":                                             [216, 2],
        "RT_HABILITA_ALARME_1_SUBFREQUENCIA":                                               [216, 3],
        "RT_HABILITA_ALARME_1_MAX_REATIVO":                                                 [216, 4],
        "RT_HABILITA_ALARME_1_MIN_REATIVO":                                                 [216, 5],
        "RT_HABILITA_ALARME_1_MAX_FATOR_POTENCIA":                                          [216, 6],
        "RT_HABILITA_ALARME_1_MIN_FATOR_POTENCIA":                                          [216, 7],
        "RT_HABILITA_ALARME_1_DVDT":                                                        [216, 8],
        "RT_HABILITA_ALARME_1_POTENCIA_REVERSA":                                            [216, 9],
        "RT_HABILITA_ALARME_1_MAX_CORRENTE_MAQUINA":                                        [216, 10],
        "RT_HABILITA_ALARME_1_MAX_CORRENTE_EXCITACAO":                                      [216, 11],
        "RT_HABILITA_ALARME_1_MIN_CORRENTE_EXCITACAO":                                      [216, 12],
        "RT_HABILITA_ALARME_1_MAX_TEMPERATURA":                                             [216, 13],
        "RT_HABILITA_ALARME_1_MAX_TENSAO_SEM_EXCITACAO":                                    [216, 14],
        "RT_HABILITA_ALARME_1_MAX_EXCITACAO_SEM_TENSAO":                                    [216, 15],

        "RT_HABILITA_ALARME_2":                                                             217,
        "RT_HABILITA_ALARME_2_CONTROLE_EXCITACAO":                                          [217, 0],
        "RT_HABILITA_ALARME_2_CONTROLE_TENSAO":                                             [217, 1],
        "RT_HABILITA_ALARME_2_CROWBAR":                                                     [217, 2],
        "RT_HABILITA_ALARME_2_DRIVE_EXCITACAO":                                             [217, 3],
        "RT_HABILITA_ALARME_2_CONTATORA_CAMPO":                                             [217, 4],
        "RT_HABILITA_ALARME_2_INSTR_REATIVO":                                               [217, 5],
        "RT_HABILITA_ALARME_2_INSTR_TENSAO":                                                [217, 6],
        "RT_HABILITA_ALARME_2_INSTR_EXCITACAO_PRINCIPAL":                                   [217, 7],
        "RT_HABILITA_ALARME_2_INSTR_EXCITACAO_RETAGUARDA":                                  [217, 8],
        "RT_HABILITA_ALARME_2_RUIDO_INSTR_REATIVO":                                         [217, 9],
        "RT_HABILITA_ALARME_2_RUIDO_INSTR_TENSAO":                                          [217, 10],
        "RT_HABILITA_ALARME_2_RUIDO_INSTR_EXCITACAO_PRINCIPAL":                             [217, 11],
        "RT_HABILITA_ALARME_2_RUIDO_INSTR_EXCITACAO_RETAGUARDA":                            [217, 12],

        "RT_HABILITA_FALHA_1":                                                              218,
        "RT_HABILITA_FALHA_1_SOBRETENSAO":                                                  [218, 0],
        "RT_HABILITA_FALHA_1_SUBTENSAO":                                                    [218, 1],
        "RT_HABILITA_FALHA_1_SOBREFREQUENCIA":                                              [218, 2],
        "RT_HABILITA_FALHA_1_SUBFREQUENCIA":                                                [218, 3],
        "RT_HABILITA_FALHA_1_MAX_REATIVO":                                                  [218, 4],
        "RT_HABILITA_FALHA_1_MIN_RETAIVO":                                                  [218, 5],
        "RT_HABILITA_FALHA_1_MAX_FATOR_POTENCIA":                                           [218, 6],
        "RT_HABILITA_FALHA_1_MIN_FATOR_POTENCIA":                                           [218, 7],
        "RT_HABILITA_FALHA_1_MAX_TENSAO_INSTANTANEA":                                       [218, 8],
        "RT_HABILITA_FALHA_1_DVDT":                                                         [218, 9],
        "RT_HABILITA_FALHA_1_POTENCIA_REVERSA":                                             [218, 10],
        "RT_HABILITA_FALHA_1_MAX_CORRENTE_MAQUINA":                                         [218, 11],
        "RT_HABILITA_FALHA_1_MAX_CORRENTE_EXCITACAO":                                       [218, 12],

        "RT_HABILITA_FALHA_2":                                                              219,
        "RT_HABILITA_FALHA_2_MAX_TEMPERATURA":                                              [219, 0],
        "RT_HABILITA_FALHA_2_TENSAO_SEM_EXCITACAO":                                         [219, 1],
        "RT_HABILITA_FALHA_2_EXCITACAO_SEM_TENSAO":                                         [219, 2],
        "RT_HABILITA_FALHA_2_CONTROLE_EXCITACAO":                                           [219, 3],
        "RT_HABILITA_FALHA_2_CONTROLE_TENSAO":                                              [219, 4],
        "RT_HABILITA_FALHA_2_CROWBAR":                                                      [219, 5],
        "RT_HABILITA_FALHA_2_DRIVE_EXCITACAO":                                              [219, 6],
        "RT_HABILITA_FALHA_2_CONTATORA_CAMPO":                                              [219, 7],
        "RT_HABILITA_FALHA_2_PRE_EXCITACAO":                                                [219, 8],
        "RT_HABILITA_FALHA_2_TIMEOUT_PRE_EXCITACAO":                                        [219, 9],
        "RT_HABILITA_FALHA_2_PARADA":                                                       [219, 10],
        "RT_HABILITA_FALHA_2_PARTIDA":                                                      [219, 11],
        "RT_HABILITA_FALHA_2_TRIP_EXTERNO":                                                 [219, 12],

        "RT_HABILITA_FALHAS_3":                                                             220,
        "RT_HABILITA_FALHAS_3_INSTRU_REATIVO":                                              [220, 0],
        "RT_HABILITA_FALHAS_3_INSTRU_TENSAO":                                               [220, 1],
        "RT_HABILITA_FALHAS_3_INSTRU_EXCITACAO_PRINCIPAL":                                  [220, 2],
        "RT_HABILITA_FALHAS_3_INSTRU_EXCITACAO_RETAGUARDA":                                 [220, 3],
        "RT_HABILITA_FALHAS_3_RUIDO_INSTRU_REATIVO":                                        [220, 4],
        "RT_HABILITA_FALHAS_3_RUIDO_INSTRU_TENSAO":                                         [220, 5],
        "RT_HABILITA_FALHAS_3_RUIDO_INSTRU_EXCITACAO_PRINCIPAL":                            [220, 6],
        "RT_HABILITA_FALHAS_3_RUIDO_INSTRU_EXCITACAO_RETAGUARDA":                           [220, 7],

        "RT_TENSAO_LIMITE_PRE_EXCITCAO_PU":                                                 221,
        "RT_CORRENTE_EXCITACAO_LIMITE_PRE_EXCITADO_PU":                                     222,
        "RT_ANGULO_ABERTURA_ESCORVAMENTO_PU":                                               223,
        "RT_CORRENTE_EXCITACAO_LIMITE_ESTABILIZADO_PU":                                     224,
        "RT_RAMPA_PARTIDA":                                                                 225,
        "RT_RAMPA_PARADA":                                                                  226,
    }
}