# MAPA NOVO

REG_MOA = {
    "SM_STATE":                                         10,         # Coil                                  (OP -> 0x05 Write Single Coil)
    "PAINEL_LIDO":                                      12,         # Coil                                  (OP -> 0x05 Write Single Coil)

    "MOA_IN_EMERG":                                     13,         # Coil                                  (OP -> 0x02 Read Input Status)
    "MOA_IN_HABILITA_AUTO":                             14,         # Coil                                  (OP -> 0x02 Read Input Status)
    "MOA_IN_DESABILITA_AUTO":                           15,         # Coil                                  (OP -> 0x02 Read Input Status)

    "MOA_OUT_MODE":                                     11,         # Coil                                  (OP -> 0x05 Write Single Coil)
    "MOA_OUT_EMERG":                                    16,         # Coil                                  (OP -> 0x05 Write Single Coil)
    "MOA_OUT_STATUS":                                   409,        # Holding Register                      (OP -> 0x06 Write Single Register)
    "MOA_OUT_TARGET_LEVEL":                             417,        # Holding Register                      (OP -> 0x06 Write Single Register)
    "MOA_OUT_SETPOINT":                                 418,        # Holding Register                      (OP -> 0x06 Write Single Register)

    "MOA_IN_EMERG_UG1":                                 20,         # Coil                                  (OP -> 0x02 Read Input Status)
    "MOA_OUT_BLOCK_UG1":                                21,         # Coil                                  (OP -> 0x05 Write Single Coil)
    "MOA_OUT_ETAPA_UG1":                                422,        # Holding Register                      (OP -> 0x06 Write Single Register)
    "MOA_OUT_STATE_UG1":                                423,        # Holding Register                      (OP -> 0x06 Write Single Register)

    "MOA_IN_EMERG_UG2":                                 25,         # Coil                                  (OP -> 0x02 Read Input Status)
    "MOA_OUT_BLOCK_UG2":                                26,         # Coil                                  (OP -> 0x05 Write Single Coil)
    "MOA_OUT_ETAPA_UG2":                                427,        # Holding Register                      (OP -> 0x06 Write Single Register)
    "MOA_OUT_STATE_UG2":                                428,        # Holding Register                      (OP -> 0x06 Write Single Register)
}


REG_GERAL= {
    ## COMANDOS DIGITAIS
    "GERAL_CD_CMD_QCTA":                                12288,      # Coil                                  (OP -> 0x05 Write Single Coil)
    "GERAL_CD_RESET_GERAL":                             [12288, 0], # Coil -> Bit 00                        (OP -> 0x05 Write Single Coil)

    ## ENTRADAS ANALÓGICAS
    # STATUS-FALHAS\NÍVEIS
    "GERAL_EA_STT_ANALOGICAS":                          12328,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "GERAL_EA_QCTA_NIVEL_JUSANTE_GRADE_FALHA_LEITURA":  [12328, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "GERAL_EA_QCTA_NIVEL_MONTANTE_GRADE_FALHA_LEITURA": [12328, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)
    "GERAL_EA_QCTA_NIVEL_JUSANTE_GRADE_MUITO_ALTO":     [12328, 2], # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers)
    "GERAL_EA_QCTA_NIVEL_MONTANTE_GRADE_MUITO_ALTO":    [12328, 3], # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers)
    "GERAL_EA_QCTA_NIVEL_JUSANTE_GRADE_ALTO":           [12328, 4], # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers)
    "GERAL_EA_QCTA_NIVEL_MONTANTE_GRADE_ALTO":          [12328, 5], # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers)
    "GERAL_EA_QCTA_NIVEL_JUSANTE_GRADE_BAIXO":          [12328, 6], # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers)
    "GERAL_EA_QCTA_NIVEL_MONTANTE_GRADE_BAIXO":         [12328, 7], # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers)
    "GERAL_EA_QCTA_NIVEL_JUSANTE_GRADE_MUITO_BAIXO":    [12328, 8], # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers)
    "GERAL_EA_QCTA_NIVEL_MONTANTE_GRADE_MUITO_BAIXO":   [12328, 9], # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers)

    # LEITURAS\NÍVEIS
    "GERAL_EA_NIVEL_JUSANTE_GRADE":                     12348,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "GERAL_EA_NIVEL_MONTANTE_GRADE":                    12350,      # Input Register                        (OP -> 0x04 Read Input Registers)

    ## ENTRADAS DIGITAIS
    # ENTRADAS CLP
    "GERAL_ED_STT_ENTRADAS_DIGITAIS":                   12308,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "GERAL_ED_QCTA_DISPO_PROTETOR_SURTO":               [12308, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "GERAL_ED_QCTA_UHLG_BOMBA_1_LIGADA":                [12308, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "GERAL_ED_QCTA_UHLG_BOMBA_1_DEFEITO":               [12308, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "GERAL_ED_QCTA_UHLG_BOMBA_2_LIGADA":                [12308, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "GERAL_ED_QCTA_UHLG_BOMBA_2_DEFEITO":               [12308, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "GERAL_ED_QCTA_MONOVIA_MOTOR_1_LIGADA":             [12308, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "GERAL_ED_QCTA_MONOVIA_MOTOR_1_DEFEITO":            [12308, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "GERAL_ED_QCTA_MONOVIA_MOTOR_2_LIGADA":             [12308, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "GERAL_ED_QCTA_MONOVIA_MOTOR_2_DEFEITO":            [12308, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)
    "GERAL_ED_QCTA_CONVERSOR_FIBRA_FALHA":              [12308, 9], # Holding Register -> Bit 09            (OP -> 0x03 Read Holding Registers)
}

REG_RELE = {
    "SE": {
        "RELE_SE_IA":                                   320,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_SE_IB":                                   322,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_SE_IC":                                   324,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_SE_VAB":                                  330,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_SE_VBC":                                  332,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_SE_VCA":                                  334,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_SE_P":                                    353,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_SE_Q":                                    361,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_SE_S":                                    369,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_SE_F":                                    374,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_SE_FP":                                   373,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_SE_EA_GERADA":                            423,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
        "RELE_SE_CONSUMIDA":                            429,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
        "RELE_SE_GERADA":                               427,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
    },

    "UG": {
        "RELE_UG1_IA":                                   320,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_UG1_IB":                                   322,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_UG1_IC":                                   324,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_UG1_VAB":                                  330,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_UG1_VBC":                                  332,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_UG1_VCA":                                  334,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_UG1_P":                                    353,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_UG1_Q":                                    361,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_UG1_S":                                    369,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_UG1_F":                                    374,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_UG1_FP":                                   373,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_UG1_EA_GERADA":                            423,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
        "RELE_UG1_CONSUMIDA":                            429,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
        "RELE_UG1_GERADA":                               427,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)

        "RELE_UG2_IA":                                   320,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_UG2_IB":                                   322,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_UG2_IC":                                   324,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_UG2_VAB":                                  330,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_UG2_VBC":                                  332,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_UG2_VCA":                                  334,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_UG2_P":                                    353,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_UG2_Q":                                    361,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_UG2_S":                                    369,        # Input Register                        (OP -> Read Input Registers - 3x)
        "RELE_UG2_F":                                    374,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_UG2_FP":                                   373,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "RELE_UG2_EA_GERADA":                            423,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
        "RELE_UG2_CONSUMIDA":                            429,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
        "RELE_UG2_GERADA":                               427,        # Input Register Scale 1                (OP -> Read Input Registers - 3x)
    },
}


REG = {
    "SA": {
        # Comandos
        "SA_CD_REARME_FALHAS":                                      [12288, 0],     # OK
        "SA_CD_DISJ_LINHA_FECHA":                                   [12288, 17],    # OK

        # Retornos
        "SA_ED_PSA_DIJS_TSA_FECHADO":                               [12308, 26],    # OK
        "SA_ED_PSA_DIJS_GMG_FECHADO":                               [12308, 27],    # OK
        "SA_ED_PSA_SE_DISJ_LINHA_FECHADO":                          [12308, 31],    # OK
    },

    "UG": {
        ## UG1
        # Comandos
        "UG1_CD_CMD_REARME_FALHAS":                                 [12288, 0],     # OK
        "UG1_CD_CMD_PARADA_EMERGENCIA":                             [12288, 1],     # OK
        "UG1_CD_CMD_CONTROLE_POTENCIA_MANUAL":                      [12288, 3],
        "UG1_CD_CMD_RV_MANUTENCAO":                                 [12288, 10],    # OK
        "UG1_CD_CMD_RV_AUTOMATICO":                                 [12288, 11],    # OK
        "UG1_CD_CMD_UHLM_MODO_AUTOMATICO":                          [12294, 0],     # OK
        "UG1_CD_CMD_UHLM_MODO_MANUTENCAO":                          [12294, 1],     # OK
        "UG1_CD_CMD_PARADA_TOTAL":                                  [12290, 0],     # OK
        "UG1_CD_CMD_SINCRONISMO":                                   [12290, 9],     # OK
        "UG1_RV_SETPOINT_POTENCIA_ATIVA_PU":                        30,
        "UG1_RT_SETPOINT_POTENCIA_REATIVA_PU":                      41,             # OK

        # Retornos
        "UG1_ED_UHRV_UNIDADE_HABILITADA":                           [12362, 1],     # OK

        "UG1_ED_STT_PASSO_SELECIONADO_BIT":                         12390,
        "UG1_ED_STT_PASSO_ATUAL_BIT":                               12392,

        ## UG2
        # Comandos
        "UG2_CD_CMD_REARME_FALHAS":                                 [12288, 0],     # OK
        "UG2_CD_CMD_PARADA_EMERGENCIA":                             [12288, 1],     # OK
        "UG2_CD_CMD_CONTROLE_POTENCIA_MANUAL":                      [12288, 3],
        "UG2_CD_CMD_RV_MANUTENCAO":                                 [12288, 10],    # OK
        "UG2_CD_CMD_RV_AUTOMATICO":                                 [12288, 11],    # OK
        "UG2_CD_CMD_UHLM_MODO_AUTOMATICO":                          [12294, 0],     # OK
        "UG2_CD_CMD_UHLM_MODO_MANUTENCAO":                          [12294, 1],     # OK
        "UG2_CD_CMD_PARADA_TOTAL":                                  [12290, 0],     # OK
        "UG2_CD_CMD_SINCRONISMO":                                   [12290, 9],     # OK
        "UG2_RV_SETPOINT_POTENCIA_ATIVA_PU":                        30,
        "UG2_RT_SETPOINT_POTENCIA_REATIVA_PU":                      41,             # OK

        # Retornos
        "UG2_ED_UHRV_UNIDADE_HABILITADA":                           [12362, 1],     # OK

        "UG2_ED_STT_PASSO_SELECIONADO_BIT":                         12390,
        "UG2_ED_STT_PASSO_ATUAL_BIT":                               12392,
    },

    "GERAL": {
        # Comandos
        "GERAL_CD_RESET_GERAL":                                     [12288, 0],     # OK

        # Retornos
        "GERAL_EA_NIVEL_MONTANTE_GRADE":                            12350,          # OK
    },

    "RELE": {
        # Retornos
        "RELE_SE_VAB":                                              330,            # OK
        "RELE_SE_VBC":                                              332,            # OK
        "RELE_SE_VCA":                                              334,            # OK
        "RELE_SE_P":                                                353,            # OK

        "RELE_UG1_P":                                               353,            # OK
        "RELE_UG1_ED_DJ_MAQUINA_FECHADO":                           [8464, 0],      # OK

        "RELE_UG2_P":                                               353,            # OK
        "RELE_UG2_ED_DJ_MAQUINA_FECHADO":                           [8464, 0],      # OK
    },

    "CONDIC_SA": {
        ## ENTRADAS DIGITAIS
        # STATUS
        "SA_ED_STT_BLOQUEIO_50BF":                                  12350,
        "SA_ED_STT_BLOQUEIO_86BTLSA":                               12352,

        # SA_ED_STT_ENTRADAS_DIGITAIS
        "SA_ED_PSA_BOTAO_BLOQUEIO_86BTBF":                          [12308, 1],
        "SA_ED_PSA_DISJUNTORES_MODO_REMOTO":                        [12308, 4],
        "SA_ED_PSA_DISJ_TSA_TRIP":                                  [12308, 5],
        "SA_ED_PSA_DISJ_GMG_TRIP":                                  [12308, 6],
        "SA_ED_PSA_RELE_BLOQUEIO_86BTBF":                           [12308, 7],
        "SA_ED_PSA_CARREGADOR_BATERIAS_FALHA":                      [12308, 8],
        # "SA_ED_PSA_CONVERSOR_FIBRA_FALHA":                          [12308, 9],
        "SA_ED_PSA_SUPERVISOR_TENSAO_FALHA":                        [12308, 10],
        "SA_ED_PSA_DPS_TSA":                                        [12308, 11],
        "SA_ED_PSA_DPS_GMG":                                        [12308, 12],
        "SA_ED_PSA_POCO_DRENAGEM_BOMBA_1_DEFEITO":                  [12308, 13],
        "SA_ED_PSA_POCO_DRENAGEM_BOMBA_2_DEFEITO":                  [12308, 15],
        "SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_BAIXO":         [12308, 21],
        "SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_ALTO":                [12308, 24],
        "SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_ALTO":          [12308, 25],
        "SA_ED_PSA_DIJS_GMG_FECHADO":                               [12308, 27],
        "SA_ED_PSA_SUPERVISOR_TENSAO_TSA_FALHA":                    [12308, 28],
        "SA_ED_PSA_SUPERVISOR_TENSAO_GMG_FALHA":                    [12308, 29],
        "SA_ED_PSA_TE_TEMPERATURA_MUITO_ALTA":                      [12308, 30],
        "SA_ED_PSA_TE_TEMPERATURA_ALTA":                            [12308, 31],

        "SA_ED_PSA_SE_DISJ_LINHA_ABERTO":                           [12310, 0],
        "SA_ED_PSA_TE_PRESSAO_MUITO_ALTA":                          [12310, 2],
        "SA_ED_PSA_NIVEL_OLEO_MUITO_BAIXO":                         [12310, 3],
        "SA_ED_PSA_PRTVA1_50BF":                                    [12310, 4],
        "SA_ED_PSA_PRTVA2_50BF":                                    [12310, 6],
        "SA_ED_PSA_SFA_ENTRADA_ELEMENTO_1_ABERTA":                  [12310, 8],
        "SA_ED_PSA_SFA_ENTRADA_ELEMENTO_2_ABERTA":                  [12310, 9],
        "SA_ED_PSA_SFA_LIMPEZA_ELEMENTO_1_ABERTA":                  [12310, 10],
        "SA_ED_PSA_SFA_LIMPEZA_ELEMENTO_2_ABERTA":                  [12310, 11],
        "SA_ED_PSA_SFB_ENTRADA_ELEMENTO_1_ABERTA":                  [12310, 13],
        "SA_ED_PSA_SFB_ENTRADA_ELEMENTO_2_ABERTA":                  [12310, 14],
        "SA_ED_PSA_SFB_LIMPEZA_ELEMENTO_1_ABERTA":                  [12310, 15],
        "SA_ED_PSA_SFB_LIMPEZA_ELEMENTO_2_ABERTA":                  [12310, 16],

        "SA_ED_PSA_GMG_DISJ_FALHA_FECHAR":                          [12348, 9],
        "SA_ED_PSA_GMG_DISJ_FALHA_ABRIR":                           [12348, 10],
        "SA_ED_PSA_TSA_DISJ_FALHA_FECHAR":                          [12348, 11],
        "SA_ED_PSA_TSA_DISJ_FALHA_ABRIR":                           [12348, 12],
        "SA_ED_PSA_SE_DISJ_FALHA_FECHAR":                           [12348, 13],
        "SA_ED_PSA_SE_DISJ_FALHA_ABRIR":                            [12348, 14],

        "SA_ED_PSA_DREANGEM_BOMBA_1_INDISP":                        [12348, 0],
        "SA_ED_PSA_DREANGEM_BOMBA_2_INDISP":                        [12348, 1],
        "SA_ED_PSA_DREANGEM_BOIAS_DISCREPANCIA":                    [12348, 4],
        "SA_ED_PSA_ESGOTAMENTO_BOMBA_1_INDISP":                     [12348, 5],
        "SA_ED_PSA_ESGOTAMENTO_BOMBA_2_INDISP":                     [12348, 6],
        "SA_ED_PSA_ESGOTAMENTO_BOMBA_1_FALHA":                      [12348, 7],
        "SA_ED_PSA_ESGOTAMENTO_BOMBA_2_FALHA":                      [12348, 8],

        "SA_ED_PSA_SFA_FALHA_ABRIR_ENTRADA_ELEM_1":                 [12354, 7],
        "SA_ED_PSA_SFA_FALHA_FECHAR_ENTRADA_ELEM_1":                [12354, 8],
        "SA_ED_PSA_SFA_FALHA_ABRIR_ENTRADA_ELEM_2":                 [12354, 9],
        "SA_ED_PSA_SFA_FALHA_FECHAR_ENTRADA_ELEM_2":                [12354, 10],
        "SA_ED_PSA_SFA_FALHA_ABRIR_LIMPEZA_ELEM_1":                 [12354, 11],
        "SA_ED_PSA_SFA_FALHA_FECHAR_LIMPEZA_ELEM_1":                [12354, 12],
        "SA_ED_PSA_SFA_FALHA_ABRIR_LIMPEZA_ELEM_2":                 [12354, 13],
        "SA_ED_PSA_SFA_FALHA_FECHAR_LIMPEZA_ELEM_2":                [12354, 14],
        "SA_ED_PSA_SFB_FALHA_ABRIR_ENTRADA_ELEM_1":                 [12354, 19],
        "SA_ED_PSA_SFB_FALHA_FECHAR_ENTRADA_ELEM_1":                [12354, 20],
        "SA_ED_PSA_SFB_FALHA_ABRIR_ENTRADA_ELEM_2":                 [12354, 21],
        "SA_ED_PSA_SFB_FALHA_FECHAR_ENTRADA_ELEM_2":                [12354, 22],
        "SA_ED_PSA_SFB_FALHA_ABRIR_LIMPEZA_ELEM_1":                 [12354, 23],
        "SA_ED_PSA_SFB_FALHA_FECHAR_LIMPEZA_ELEM_1":                [12354, 24],
        "SA_ED_PSA_SFB_FALHA_ABRIR_LIMPEZA_ELEM_2":                 [12354, 25],
        "SA_ED_PSA_SFB_FALHA_FECHAR_LIMPEZA_ELEM_2":                [12354, 26],

        "SA_ED_BLOQUEIO_50BF_ATUADO":                               [12350, 31],
        "SA_ED_BLOQUEIO_86BTLSA_ATUADO":                            [12350, 31],

        ## ENTRADAS ANALÓGICAS
        # NÍVEIS
        "SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO":                     [12328, 7],
        "SA_EA_PSA_NIVEL_MONTANTE_BAIXO":                           [12328, 9],

        "SA_EA_PSA_NIVEL_JUSANTE_MUITO_ALTO":                       [12340, 0],
        "SA_EA_PSA_NIVEL_JUSANTE_ALTO":                             [12342, 0],
        "SA_EA_PSA_NIVEL_JUSANTE_MUITO_BAIXO":                      [12344, 0],

        # SFA / SFB
        # FALHAS
        "SA_EA_PSA_NIVEL_JUSANTE_FALHA_LEITURA":                    [12338, 0],
        "SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_FALHA_LEITURA":           [12338, 2],
        "SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_FALHA_LEITURA":            [12338, 3],
        "SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_FALHA_LEITURA":           [12338, 4],
        "SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_FALHA_LEITURA":            [12338, 5],
        
        # ALARMES
        "SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO":              [12340, 3],
        "SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO":               [12340, 4],
        "SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO":              [12340, 5],
        "SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO":               [12340, 6],
        "SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO":                    [12342, 3],
        "SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO":                     [12342, 4],
        "SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO":                    [12342, 5],
        "SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO":                     [12342, 6],
        "SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_BAIXO":                   [12344, 3],
        "SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_BAIXO":                    [12344, 4],
        "SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_BAIXO":                   [12344, 5],
        "SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_BAIXO":                    [12344, 6],
        "SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_BAIXO":             [12346, 3],
        "SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_BAIXO":              [12346, 4],
        "SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_BAIXO":             [12346, 5],
        "SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_BAIXO":              [12346, 6],
    },

    "CONDIC_UG": {
        ### UG1
        ## COMANDOS DIGITAIS
        # UHRV
        "UG1_CD_CMD_UHRV_MODO_MANUTENCAO":                          [12292, 1],

        # UHLM
        "UG1_CD_CMD_UHLM_MODO_MANUTENCAO":                          [12294, 1],

        ## ENTRADAS DIGITAIS
        # STATUS
        "UG1_ED_STT_RV":                                            12372,
        "UG1_ED_STT_BLOQUEIO_86M":                                  12428,
        "UG1_ED_STT_BLOQUEIO_86E":                                  12430,
        "UG1_ED_STT_BLOQUEIO_86H":                                  12432,

        # UG1_STT_UNIDADE_GERADORA
        "UG1_ED_CONTROLE_ALARME_DIFERENCIAL_GRADE":                 [12360, 6],
        "UG1_ED_CONTROLE_TRIP_DIFERENCIAL_GRADE":                   [12360, 7],
        "UG1_ED_RESISTENCIA_AQUEC_GERADOR_INDISPONIVEL":            [12360, 8],
        "UG1_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR":             [12360, 9],
        "UG1_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_DESLIGAR":          [12360, 10],

        # UG1_ED_STT_BORBOLETA
        "UG1_ED_BROBOLETA_FALHA_ABRIR":                             [12366, 0],
        "UG1_ED_BORBOLETA_FALHA_FECHAR":                            [12366, 1],
        "UG1_ED_BYPASS_FALHA_ABRIR":                                [12366, 6],
        "UG1_ED_BYPASS_FALHA_FECHAR":                               [12366, 7],
        "UG1_ED_BORBOLETA_DISCREPANCIA_SENSORES":                   [12366, 10],
        "UG1_ED_BYPASS_DISCREPANCIA_SENSORES":                      [12366, 11],

        # UG1_ED_STT_ENTRADAS_DIGITAIS_1
        "UG1_ED_PRTVA_BOTAO_BLOQUEIO_86EH":                         [12310, 0],
        "UG1_ED_PRTVA_RELE_PROT_GERADOR_TRIP":                      [12310, 8],
        "UG1_ED_PRTVA_RELE_PROT_GERADOR_50BF":                      [12310, 10],
        "UG1_ED_PRTVA_RV_TRIP":                                     [12310, 11],
        "UG1_ED_PRTVA_RV_ALARME":                                   [12310, 12],
        "UG1_ED_PRTVA_RV_POTENCIA_NULA":                            [12310, 15],
        "UG1_ED_PRTVA_RELE_BLOQUEIO_86EH":                          [12310, 26],
        "UG1_ED_PRTVA_RT_TRIP":                                     [12310, 20],
        "UG1_ED_PRTVA_RT_ALARME":                                   [12310, 21],
        "UG1_ED_PRTVA_DISPOSITIVO_PROTECAO_SURTO":                  [12310, 28],
        "UG1_ED_PRTVA_UHRV_BOMBA_DEFEITO":                          [12310, 29],
        "UG1_ED_PRTVA_UHLM_BOMBA_DEFEITO":                          [12310, 31],

        # UG1_ED_STT_ENTRADAS_DIGITAIS_2
        "UG1_ED_PRTVA_RESISTENCIA_AQUEC_GERADOR_DEFEITO":           [12312, 3],
        "UG1_ED_PRTVA_DISJUNTOR_TPS_PROTECAO":                      [12312, 5],
        "UG1_ED_PRTVA_UHRV_OLEO_NIVEL_MUITO_BAIXO":                 [12312, 6],
        "UG1_ED_PRTVA_UHRV_FILTRO_OLEO_SUJO":                       [12312, 7],
        "UG1_ED_PRTVA_UHRV_PRESSAO_CRITICA":                        [12312, 8],
        "UG1_ED_PRTVA_UHRV_PRESSAO_FREIO":                          [12312, 10],
        "UG1_ED_PRTVA_UHLM_OLEO_NIVEL_MUITO_ALTO":                  [12312, 11],
        "UG1_ED_PRTVA_UHLM_OLEO_NIVEL_MUITO_BAIXO":                 [12312, 12],
        "UG1_ED_PRTVA_UHLM_PRESSAO_LINHA_LUBRIFICACAO":             [12312, 14],
        "UG1_ED_PRTVA_UHLM_FLUXO_TROCADOR_CALOR":                   [12312, 16],
        "UG1_ED_PRTVA_QBAG_ESCOVA_POLO_POSITIVO_DESGASTADA":        [12312, 18],
        "UG1_ED_PRTVA_QBAG_ESCOVA_POLO_NEGATIVO_DESGASTADA":        [12312, 19],

        # RV
        "UG1_ED_RV_FALHA_AO_HABILITAR":                             [12372, 0],
        "UG1_ED_RV_FALHA_AO_PARTIR":                                [12372, 1],
        "UG1_ED_RV_FALHA_AO_DESABILITAR":                           [12372, 2],
        "UG1_ED_RV_FALHA_AO_PARAR_MAQUINA":                         [12372, 3],
        "UG1_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR":                   [12372, 4],
        "UG1_ED_RV_MODO_MANUTENCAO":                                [12372, 5],

        # RT
        "UG1_ED_RT_FALHA_AO_HABILITAR":                             [12374, 0],
        "UG1_ED_RT_FALHA_AO_PARTIR":                                [12374, 1],
        "UG1_ED_RT_FALHA_AO_DESABILITAR":                           [12374, 2],

        # UHRV
        "UG1_ED_UHRV_BOMBA_1_INDISPONIVEL":                         [12362, 2],
        "UG1_ED_UHRV_BOMBA_1_FALHA_AO_LIGAR":                       [12362, 6],
        "UG1_ED_UHRV_BOMBA_1_FALHA_AO_DESLIGAR":                    [12362, 7],
        "UG1_ED_UHRV_BOMBA_2_FALHA_AO_LIGAR":                       [12362, 8],
        "UG1_ED_UHRV_BOMBA_2_FALHA_AO_DESLIGAR":                    [12362, 9],
        "UG1_ED_UHRV_BOMBA_1_FALHA_AO_PRESSURIZAR":                 [12362, 10],
        "UG1_ED_UHRV_BOMBA_2_FALHA_AO_PRESSURIZAR":                 [12362, 11],
        "UG1_ED_UHRV_FILTRO_OLEO_SUJO":                             [12362, 13],

        # UHLM
        "UG1_ED_UHLM_UNIDADE_MANUTENCAO":                           [12364, 0],
        "UG1_ED_UHLM_BOMBA_1_INDISPONIVEL":                         [12364, 2],
        "UG1_ED_UHLM_BOMBA_2_INDISPONIVEL":                         [12364, 3],
        "UG1_ED_UHLM_BOMBA_1_FALHA_LIGAR":                          [12364, 6],
        "UG1_ED_UHLM_BOMBA_1_FALHA_DESLIGAR":                       [12364, 7],
        "UG1_ED_UHLM_BOMBA_2_FALHA_LIGAR":                          [12364, 8],
        "UG1_ED_UHLM_BOMBA_2_FALHA_DESLIGAR":                       [12364, 9],
        "UG1_ED_UHLM_BOMBA_1_FALHA_PRESSURIZAR":                    [12364, 10],
        "UG1_ED_UHLM_BOMBA_2_FALHA_PRESSURIZAR":                    [12364, 11],
        "UG1_ED_UHLM_FILTRO_SUJO":                                  [12364, 13],
        "UG1_ED_UHLM_FALHA_PRESSOSTATO":                            [12364, 14],

        ## ENTRADAS ANALÓGICAS
        # ALARME TEMPERATURA MUITO ALTA
        "UG1_EA_TRISTORES_TEMP_MUITO_ALTA":                         [12330, 0],
        "UG1_EA_CROWBAR_TEMP_MUITO_ALTA":                           [12330, 1],
        "UG1_EA_TRAFO_EXCITACAO_TEMP_MUITO_ALTA":                   [12330, 2],
        "UG1_EA_UHRV_OLEO_TEMP_MUITO_ALTA":                         [12330, 3],
        "UG1_EA_UHLM_OLEO_TEMP_MUITO_ALTA":                         [12330, 4],
        "UG1_EA_GERADOR_FASE_A_TEMP_MUITO_ALTA":                    [12330, 7],
        "UG1_EA_GERADOR_FASE_B_TEMP_MUITO_ALTA":                    [12330, 8],
        "UG1_EA_GERADOR_FASE_C_TEMP_MUITO_ALTA":                    [12330, 9],
        "UG1_EA_GERADOR_NUCLEO_1_TEMP_MUITO_ALTA":                  [12330, 10],
        "UG1_EA_GERADOR_NUCLEO_2_TEMP_MUITO_ALTA":                  [12330, 11],
        "UG1_EA_GERADOR_NUCLEO_3_TEMP_MUITO_ALTA":                  [12330, 12],
        "UG1_EA_MANCAL_GUIA_CASQUILHO_TEMP_MUITO_ALTA":             [12330, 13],
        "UG1_EA_MANCAL_COMBINADO_CASQUILHO_TEMP_MUITO_ALTA":        [12330, 14],
        "UG1_EA_MANCAL_COMBINADO_ESCORA_TEMP_MUITO_ALTA":           [12330, 15],

        # ALARME TEMPERATURA ALTA
        "UG1_EA_TRISTORES_TEMP_ALTA":                               [12332, 0],
        "UG1_EA_CROWBAR_TEMP_ALTA":                                 [12332, 1],
        "UG1_EA_TRAFO_EXCITACAO_TEMP_ALTA":                         [12332, 2],
        "UG1_EA_UHRV_OLEO_TEMP_ALTA":                               [12332, 3],
        "UG1_EA_UHLM_OLEO_TEMP_ALTA":                               [12332, 4],
        "UG1_EA_GERADOR_FASE_A_TEMP_ALTA":                          [12332, 7],
        "UG1_EA_GERADOR_FASE_B_TEMP_ALTA":                          [12332, 8],
        "UG1_EA_GERADOR_FASE_C_TEMP_ALTA":                          [12332, 9],
        "UG1_EA_GERADOR_NUCLEO_1_TEMP_ALTA":                        [12332, 10],
        "UG1_EA_GERADOR_NUCLEO_2_TEMP_ALTA":                        [12332, 11],
        "UG1_EA_GERADOR_NUCLEO_3_TEMP_ALTA":                        [12332, 12],
        "UG1_EA_MANCAL_GUIA_CASQUILHO_TEMP_ALTA":                   [12332, 13],
        "UG1_EA_MANCAL_COMBINADO_CASQUILHO_TEMP_ALTA":              [12332, 14],
        "UG1_EA_MANCAL_COMBINADO_ESCORA_TEMP_ALTA":                 [12332, 15],

        # FALHA LEITURA TEMPERATURAS
        "UG1_EA_TRISTORES_TEMP_FALHA_LEITURA":                      [12328, 0],
        "UG1_EA_CROWBAR_TEMP_FALHA_LEITURA":                        [12328, 1],
        "UG1_EA_TRAFO_EXCITACAO_FALHA_LEITURA":                     [12328, 2],
        "UG1_EA_UHRV_TEMP_OLEO_FALHA_LEITURA":                      [12328, 3],
        "UG1_EA_UHLM_TEMP_OLEO_FALHA_LEITURA":                      [12328, 4],
        "UG1_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA":                 [12328, 7],
        "UG1_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA":                 [12328, 8],
        "UG1_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA":                 [12328, 9],
        "UG1_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA":               [12328, 10],
        "UG1_EA_GERADOR_NUCLEO_2_TEMP_FALHA_LEITURA":               [12328, 11],
        "UG1_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA":               [12328, 12],
        "UG1_EA_MANCAL_GUIA_CASQUILHO_TEMP_FALHA_LEITURA":          [12328, 13],
        "UG1_EA_MANCAL_COMBINADO_CASQUILHO_TEMP_FALHA_LEITURA":     [12328, 14],
        "UG1_EA_MANCAL_COMBINADO_ESCORA_TEMP_FALHA_LEITURA":        [12328, 15],

        # FALHA LEITURA ANALOGICAS
        "UG1_EA_UHRV_PRESSAO_OLEO_FALHA_LEITURA":                   [12340, 0], # Duplicado
        "UG1_EA_SINAL_NIVEL_JUSANTE_FALHA_LEITURA":                 [12340, 0], # Duplicado

        # ALARME PRESSÃO
        "UG1_EA_UHRV_PRESSAO_OLEO_MUITO_ALTO":                      [12342, 0],
        "UG1_EA_UHRV_PRESSAO_OLEO_ALTO":                            [12344, 0],
        "UG1_EA_UHRV_PRESSAO_OLEO_BAIXA":                           [12346, 0],
        "UG1_EA_UHRV_PRESSAO_OLEO_MUITO_BAIXA":                     [12348, 0],

        # ALARME NÍVEL JUSANTE
        "UG1_EA_SINAL_NIVEL_JUSANTE_MUITO_ALTO":                    [12342, 1],
        "UG1_EA_SINAL_NIVEL_JUSANTE_ALTO":                          [12344, 1],
        "UG1_EA_SINAL_NIVEL_JUSANTE_BAIXA":                         [12346, 1],
        "UG1_EA_SINAL_NIVEL_JUSANTE_MUITO_BAIXA":                   [12348, 1],

        ## DRIVER RV
        # ALARMES
        "UG1_RV_ALARME_SOBREFREQUENCIA":                            [66, 0],
        "UG1_RV_ALARME_SUBFREQUENCIA":                              [66, 1],

        # FALHAS 1
        "UG1_RV_FALHA_1":                                           67,
        "UG1_RV_FALHA_1_SOBREFREQ_INSTANT":                         [67, 0],
        "UG1_RV_FALHA_1_SOBREFREQ_TEMPOR":                          [67, 1],
        "UG1_RV_FALHA_1_SUBFREQ_TEMPORIZADA":                       [67, 2],
        "UG1_RV_FALHA_1_GIRANDO_SEM_REG_GIRO_INDEV":                [67, 3],
        "UG1_RV_FALHA_1_LEIT_POS_DISTRIBUIDOR":                     [67, 4],
        "UG1_RV_FALHA_1_LEIT_POTENCIA_ATIVA":                       [67, 6],
        "UG1_RV_FALHA_1_LEIT_REFERENCIA_POTENCIA":                  [67, 7],
        "UG1_RV_FALHA_1_NV_MONTANTE_MUITO_BAIXO":                   [67, 10],
        "UG1_RV_FALHA_1_CONTROLE_POS_DISTRIBUIDOR":                 [67, 11],
        "UG1_RV_FALHA_1_RUIDO_MED_VELOC_PRINCIPAL":                 [67, 13],
        "UG1_RV_FALHA_1_RUIDO_MED_VELOC_RETAGUARDA":                [67, 14],
        "UG1_RV_FALHA_1_PERDA_MED_VELOC_PRINCIPAL":                 [67, 15],

        # FALHAS 2
        "UG1_RV_FALHA_2_PERDA_MED_VELOC_RETAGUARDA":                [68, 0],
        "UG1_RV_FALHA_2_TEMPO_EXCESSIVO_PARTIDA":                   [68, 1],
        "UG1_RV_FALHA_2_TEMPO_EXCESSIVO_PARADA":                    [68, 2],
        "UG1_RV_FALHA_2_DIF_MED_VELO_PRINCIPAL_RETAGUARDA":         [68, 4],

        ## DRIVER RT
        # ENTRADAS DIGITAIS
        "UG1_RT_ED_CROWBAR_INATIVO":                                [30, 9],
        "UG1_RT_ED_SELEC_MODO_CONTROLE_ISOLADO":                    [30, 2],

        # SAÍDAS DIGITAIS
        "UG1_RT_SD_RELE_ALARME":                                    [31, 1],

        # ALARMES 1
        "UG1_RT_ALARMES_1_SOBRETENSAO":                             [70, 0],
        "UG1_RT_ALARMES_1_SUBTENSAO":                               [70, 1],
        "UG1_RT_ALARMES_1_SOBREFREQUENCIA":                         [70, 2],
        "UG1_RT_ALARMES_1_SUBFREQUENCIA":                           [70, 3],
        "UG1_RT_ALARMES_1_LIMITE_SUP_POT_REATIVA":                  [70, 4],
        "UG1_RT_ALARMES_1_LIMITE_INF_POT_REATIVA":                  [70, 5],
        "UG1_RT_ALARMES_1_LIMITE_SUP_FATOR_POTENCIA":               [70, 6],
        "UG1_RT_ALARMES_1_LIMITE_INF_FATOR_POTENCIA":               [70, 7],
        "UG1_RT_ALARMES_1_VARIACAO_TENSAO":                         [70, 8],
        "UG1_RT_ALARMES_1_POTENCIA_ATIVA_REVERSA":                  [70, 9],
        "UG1_RT_ALARMES_1_SOBRECORRENTE_TERMINAL":                  [70, 10],
        "UG1_RT_ALARMES_1_LIMITE_SUP_CORRENTE_EXCITACAO":           [70, 11],
        "UG1_RT_ALARMES_1_LIMITE_INF_CORRENTE_EXCITACAO":           [70, 12],
        "UG1_RT_ALARMES_1_TEMP_MUITO_ALTA_ROTOR":                   [70, 13],
        "UG1_RT_ALARMES_1_PRES_TENS_TERM_AUSEN_CORR_EXCI":          [70, 14],
        "UG1_RT_ALARMES_1_PRES_CORR_EXCI_AUSEN_TENS_TERM":          [70, 15],

        # ALARMES 2
        "UG1_RT_ALARMES_2_FALHA_CONTROLE_CORRENTE_EXCI":            [71, 0],
        "UG1_RT_ALARMES_2_FALHA_CONTROLE_TENSAO_TERM":              [71, 1],
        "UG1_RT_ALARMES_2_CROWBAR_ATUADO_REGUL_HABIL":              [71, 2],
        "UG1_RT_ALARMES_2_FALHA_HABIL_DRIVE_EXCI":                  [71, 3],
        "UG1_RT_ALARMES_2_FALHA_FECHAR_CONTATOR_CAMPO":             [71, 4],
        "UG1_RT_ALARMES_2_FALHA_CORR_EXCI_PRE_EXCI_ATIVA":          [71, 5],
        "UG1_RT_ALARMES_2_PERDA_MEDICAO_POTENCIA_REATIVA":          [71, 6],
        "UG1_RT_ALARMES_2_PERDA_MEDICAO_TENSAO_TERMINAL":           [71, 7],
        "UG1_RT_ALARMES_2_PERDA_MEDICAO_CORRENTE_EXCI":             [71, 8],
        "UG1_RT_ALARMES_2_RUIDO_INSTRUMEN_REATIVO":                 [71, 9],
        "UG1_RT_ALARMES_2_RUIDO_INSTRUMEN_TENSAO":                  [71, 10],
        "UG1_RT_ALARMES_2_RUIDO_INSTRUMEN_EXCI_PRINCI":             [71, 11],
        "UG1_RT_ALARMES_2_RUIDO_INSTRUMEN_EXCI_RETAG":              [71, 12],

        # FALHAS 1
        "UG1_RT_FALHAS_1_SOBRETENSAO":                              [72, 0],
        "UG1_RT_FALHAS_1_SUBTENSAO":                                [72, 1],
        "UG1_RT_FALHAS_1_SOBREFREQUENCIA":                          [72, 2],
        "UG1_RT_FALHAS_1_SUBFREQUENCIA":                            [72, 3],
        "UG1_RT_FALHAS_1_LIMITE_SUP_POT_REATIVA":                   [72, 4],
        "UG1_RT_FALHAS_1_LIMITE_INF_POT_REATIVA":                   [72, 5],
        "UG1_RT_FALHAS_1_LIMITE_SUP_FATOR_POT":                     [72, 6],
        "UG1_RT_FALHAS_1_LIMITE_INF_FATOR_POT":                     [72, 7],
        "UG1_RT_FALHAS_1_SOBRETENSAO_INST":                         [72, 8],
        "UG1_RT_FALHAS_1_VARIACAO_TENSAO":                          [72, 9],
        "UG1_RT_FALHAS_1_POT_ATIVA_REVERSA":                        [72, 10],
        "UG1_RT_FALHAS_1_SOBRECORRENTE_TERMINAL":                   [72, 11],
        "UG1_RT_FALHAS_1_LIMITE_SUP_CORRENTE_EXCITACAO":            [72, 12],
        "UG1_RT_FALHAS_1_LIMITE_INF_CORRENTE_EXCITACAO":            [72, 13],
        "UG1_RT_FALHAS_1_LIMITE_SUP_TENSAO_EXCITACAO":              [72, 14],
        "UG1_RT_FALHAS_1_LIMITE_INF_TENSAO_EXCITACAO":              [72, 15],

        # FALHAS 2
        "UG1_RT_FALHAS_2_TEMP_MUITO_ALTA_ROTOR":                    [73, 0],
        "UG1_RT_FALHAS_2_PRES_TENS_TERM_AUSEN_CORR_EXCI":           [73, 1],
        "UG1_RT_FALHAS_2_PRES_CORR_EXCI_AUSEN_TENS_TERM":           [73, 2],
        "UG1_RT_FALHAS_2_CONTROLE_CORR_EXCI":                       [73, 3],
        "UG1_RT_FALHAS_2_TENSAO_TERMINAL":                          [73, 4],
        "UG1_RT_FALHAS_2_CROWBAR_ATUADO_REGULADOR_HABI":            [73, 5],
        "UG1_RT_FALHAS_2_HABI_DRIVE_EXCITACAO":                     [73, 6],
        "UG1_RT_FALHAS_2_FECHAR_CONTATOR_CAMPO":                    [73, 7],
        "UG1_RT_FALHAS_2_CORR_EXCITA_PRE_EXCXITA_ATIVA":            [73, 8],
        "UG1_RT_FALHAS_2_EXCESSIVO_PRE_EXCITACAO":                  [73, 9],
        "UG1_RT_FALHAS_2_EXCESSIVO_PARADA":                         [73, 10],
        "UG1_RT_FALHAS_2_EXCESSIVO_PARTIDA":                        [73, 11],
        "UG1_RT_FALHAS_2_BLOQ_EXTERNO":                             [73, 12],

        # FALHAS 3
        "UG1_RT_FALHAS_3_PERDA_MED_POT_REATIVA":                    [74, 0],
        "UG1_RT_FALHAS_3_PERDA_MED_TENSAO_TERM":                    [74, 1],
        "UG1_RT_FALHAS_3_PERDA_MED_CORR_EXCI_PRINCI":               [74, 2],
        "UG1_RT_FALHAS_3_PERDA_MED_CORR_EXCI_RETAG":                [74, 3],
        "UG1_RT_FALHAS_3_RUIDO_INSTRUM_REATIVO":                    [74, 4],
        "UG1_RT_FALHAS_3_RUIDO_INSTRUM_TENSAO":                     [74, 5],
        "UG1_RT_FALHAS_3_RUIDO_INSTRUM_EXCI_PRINCI":                [74, 6],
        "UG1_RT_FALHAS_3_RUIDO_INSTRUM_EXCI_RETAG":                 [74, 7],

        ### UG2
        ## COMANDOS DIGITAIS
        # UHRV
        "UG2_CD_CMD_UHRV_MODO_MANUTENCAO":                          [12292, 1],

        # UHLM
        "UG2_CD_CMD_UHLM_MODO_MANUTENCAO":                          [12294, 1],

        ## ENTRADAS DIGITAIS
        # STATUS
        "UG2_ED_STT_RV":                                            12372,
        "UG2_ED_STT_BLOQUEIO_86M":                                  12428,
        "UG2_ED_STT_BLOQUEIO_86E":                                  12430,
        "UG2_ED_STT_BLOQUEIO_86H":                                  12432,

        # UG2_STT_UNIDADE_GERADORA
        "UG2_ED_CONTROLE_ALARME_DIFERENCIAL_GRADE":                 [12360, 6],
        "UG2_ED_CONTROLE_TRIP_DIFERENCIAL_GRADE":                   [12360, 7],
        "UG2_ED_RESISTENCIA_AQUEC_GERADOR_INDISPONIVEL":            [12360, 8],
        "UG2_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR":             [12360, 9],
        "UG2_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_DESLIGAR":          [12360, 10],

        # UG2_ED_STT_BORBOLETA
        "UG2_ED_BROBOLETA_FALHA_ABRIR":                             [12366, 0],
        "UG2_ED_BORBOLETA_FALHA_FECHAR":                            [12366, 1],
        "UG2_ED_BYPASS_FALHA_ABRIR":                                [12366, 6],
        "UG2_ED_BYPASS_FALHA_FECHAR":                               [12366, 7],
        "UG2_ED_BORBOLETA_DISCREPANCIA_SENSORES":                   [12366, 10],
        "UG2_ED_BYPASS_DISCREPANCIA_SENSORES":                      [12366, 11],

        # UG2_ED_STT_ENTRADAS_DIGITAIS_1
        "UG2_ED_PRTVA_BOTAO_BLOQUEIO_86EH":                         [12310, 0],
        "UG2_ED_PRTVA_RELE_PROT_GERADOR_TRIP":                      [12310, 8],
        "UG2_ED_PRTVA_RELE_PROT_GERADOR_50BF":                      [12310, 10],
        "UG2_ED_PRTVA_RV_TRIP":                                     [12310, 11],
        "UG2_ED_PRTVA_RV_ALARME":                                   [12310, 12],
        "UG2_ED_PRTVA_RV_POTENCIA_NULA":                            [12310, 15],
        "UG2_ED_PRTVA_RELE_BLOQUEIO_86EH":                          [12310, 26],
        "UG2_ED_PRTVA_RT_TRIP":                                     [12310, 20],
        "UG2_ED_PRTVA_RT_ALARME":                                   [12310, 21],
        "UG2_ED_PRTVA_DISPOSITIVO_PROTECAO_SURTO":                  [12310, 28],
        "UG2_ED_PRTVA_UHRV_BOMBA_DEFEITO":                          [12310, 29],
        "UG2_ED_PRTVA_UHLM_BOMBA_DEFEITO":                          [12310, 31],

        # UG2_ED_STT_ENTRADAS_DIGITAIS_2
        "UG2_ED_PRTVA_RESISTENCIA_AQUEC_GERADOR_DEFEITO":           [12312, 3],
        "UG2_ED_PRTVA_DISJUNTOR_TPS_PROTECAO":                      [12312, 5],
        "UG2_ED_PRTVA_UHRV_OLEO_NIVEL_MUITO_BAIXO":                 [12312, 6],
        "UG2_ED_PRTVA_UHRV_FILTRO_OLEO_SUJO":                       [12312, 7],
        "UG2_ED_PRTVA_UHRV_PRESSAO_CRITICA":                        [12312, 8],
        "UG2_ED_PRTVA_UHRV_PRESSAO_FREIO":                          [12312, 10],
        "UG2_ED_PRTVA_UHLM_OLEO_NIVEL_MUITO_ALTO":                  [12312, 11],
        "UG2_ED_PRTVA_UHLM_OLEO_NIVEL_MUITO_BAIXO":                 [12312, 12],
        "UG2_ED_PRTVA_UHLM_PRESSAO_LINHA_LUBRIFICACAO":             [12312, 14],
        "UG2_ED_PRTVA_UHLM_FLUXO_TROCADOR_CALOR":                   [12312, 16],
        "UG2_ED_PRTVA_QBAG_ESCOVA_POLO_POSITIVO_DESGASTADA":        [12312, 18],
        "UG2_ED_PRTVA_QBAG_ESCOVA_POLO_NEGATIVO_DESGASTADA":        [12312, 19],

        # RV
        "UG2_ED_RV_FALHA_AO_HABILITAR":                             [12372, 0],
        "UG2_ED_RV_FALHA_AO_PARTIR":                                [12372, 1],
        "UG2_ED_RV_FALHA_AO_DESABILITAR":                           [12372, 2],
        "UG2_ED_RV_FALHA_AO_PARAR_MAQUINA":                         [12372, 3],
        "UG2_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR":                   [12372, 4],
        "UG2_ED_RV_MODO_MANUTENCAO":                                [12372, 5],

        # RT
        "UG2_ED_RT_FALHA_AO_HABILITAR":                             [12374, 0],
        "UG2_ED_RT_FALHA_AO_PARTIR":                                [12374, 1],
        "UG2_ED_RT_FALHA_AO_DESABILITAR":                           [12374, 2],

        # UHRV
        "UG2_ED_UHRV_BOMBA_1_INDISPONIVEL":                         [12362, 2],
        "UG2_ED_UHRV_BOMBA_1_FALHA_AO_LIGAR":                       [12362, 6],
        "UG2_ED_UHRV_BOMBA_1_FALHA_AO_DESLIGAR":                    [12362, 7],
        "UG2_ED_UHRV_BOMBA_2_FALHA_AO_LIGAR":                       [12362, 8],
        "UG2_ED_UHRV_BOMBA_2_FALHA_AO_DESLIGAR":                    [12362, 9],
        "UG2_ED_UHRV_BOMBA_1_FALHA_AO_PRESSURIZAR":                 [12362, 10],
        "UG2_ED_UHRV_BOMBA_2_FALHA_AO_PRESSURIZAR":                 [12362, 11],
        "UG2_ED_UHRV_FILTRO_OLEO_SUJO":                             [12362, 13],

        # UHLM
        "UG2_ED_UHLM_UNIDADE_MANUTENCAO":                           [12364, 0],
        "UG2_ED_UHLM_BOMBA_1_INDISPONIVEL":                         [12364, 2],
        "UG2_ED_UHLM_BOMBA_2_INDISPONIVEL":                         [12364, 3],
        "UG2_ED_UHLM_BOMBA_1_FALHA_LIGAR":                          [12364, 6],
        "UG2_ED_UHLM_BOMBA_1_FALHA_DESLIGAR":                       [12364, 7],
        "UG2_ED_UHLM_BOMBA_2_FALHA_LIGAR":                          [12364, 8],
        "UG2_ED_UHLM_BOMBA_2_FALHA_DESLIGAR":                       [12364, 9],
        "UG2_ED_UHLM_BOMBA_1_FALHA_PRESSURIZAR":                    [12364, 10],
        "UG2_ED_UHLM_BOMBA_2_FALHA_PRESSURIZAR":                    [12364, 11],
        "UG2_ED_UHLM_FILTRO_SUJO":                                  [12364, 13],
        "UG2_ED_UHLM_FALHA_PRESSOSTATO":                            [12364, 14],

        ## ENTRADAS ANALÓGICAS
        # ALARME TEMPERATURA MUITO ALTA
        "UG2_EA_TRISTORES_TEMP_MUITO_ALTA":                         [12330, 0],
        "UG2_EA_CROWBAR_TEMP_MUITO_ALTA":                           [12330, 1],
        "UG2_EA_TRAFO_EXCITACAO_TEMP_MUITO_ALTA":                   [12330, 2],
        "UG2_EA_UHRV_OLEO_TEMP_MUITO_ALTA":                         [12330, 3],
        "UG2_EA_UHLM_OLEO_TEMP_MUITO_ALTA":                         [12330, 4],
        "UG2_EA_GERADOR_FASE_A_TEMP_MUITO_ALTA":                    [12330, 7],
        "UG2_EA_GERADOR_FASE_B_TEMP_MUITO_ALTA":                    [12330, 8],
        "UG2_EA_GERADOR_FASE_C_TEMP_MUITO_ALTA":                    [12330, 9],
        "UG2_EA_GERADOR_NUCLEO_1_TEMP_MUITO_ALTA":                  [12330, 10],
        "UG2_EA_GERADOR_NUCLEO_2_TEMP_MUITO_ALTA":                  [12330, 11],
        "UG2_EA_GERADOR_NUCLEO_3_TEMP_MUITO_ALTA":                  [12330, 12],
        "UG2_EA_MANCAL_GUIA_CASQUILHO_TEMP_MUITO_ALTA":             [12330, 13],
        "UG2_EA_MANCAL_COMBINADO_CASQUILHO_TEMP_MUITO_ALTA":        [12330, 14],
        "UG2_EA_MANCAL_COMBINADO_ESCORA_TEMP_MUITO_ALTA":           [12330, 15],

        # ALARME TEMPERATURA ALTA
        "UG2_EA_TRISTORES_TEMP_ALTA":                               [12332, 0],
        "UG2_EA_CROWBAR_TEMP_ALTA":                                 [12332, 1],
        "UG2_EA_TRAFO_EXCITACAO_TEMP_ALTA":                         [12332, 2],
        "UG2_EA_UHRV_OLEO_TEMP_ALTA":                               [12332, 3],
        "UG2_EA_UHLM_OLEO_TEMP_ALTA":                               [12332, 4],
        "UG2_EA_GERADOR_FASE_A_TEMP_ALTA":                          [12332, 7],
        "UG2_EA_GERADOR_FASE_B_TEMP_ALTA":                          [12332, 8],
        "UG2_EA_GERADOR_FASE_C_TEMP_ALTA":                          [12332, 9],
        "UG2_EA_GERADOR_NUCLEO_1_TEMP_ALTA":                        [12332, 10],
        "UG2_EA_GERADOR_NUCLEO_2_TEMP_ALTA":                        [12332, 11],
        "UG2_EA_GERADOR_NUCLEO_3_TEMP_ALTA":                        [12332, 12],
        "UG2_EA_MANCAL_GUIA_CASQUILHO_TEMP_ALTA":                   [12332, 13],
        "UG2_EA_MANCAL_COMBINADO_CASQUILHO_TEMP_ALTA":              [12332, 14],
        "UG2_EA_MANCAL_COMBINADO_ESCORA_TEMP_ALTA":                 [12332, 15],

        # FALHA LEITURA TEMPERATURAS
        "UG2_EA_TRISTORES_TEMP_FALHA_LEITURA":                      [12328, 0],
        "UG2_EA_CROWBAR_TEMP_FALHA_LEITURA":                        [12328, 1],
        "UG2_EA_TRAFO_EXCITACAO_FALHA_LEITURA":                     [12328, 2],
        "UG2_EA_UHRV_TEMP_OLEO_FALHA_LEITURA":                      [12328, 3],
        "UG2_EA_UHLM_TEMP_OLEO_FALHA_LEITURA":                      [12328, 4],
        "UG2_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA":                 [12328, 7],
        "UG2_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA":                 [12328, 8],
        "UG2_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA":                 [12328, 9],
        "UG2_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA":               [12328, 10],
        "UG2_EA_GERADOR_NUCLEO_2_TEMP_FALHA_LEITURA":               [12328, 11],
        "UG2_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA":               [12328, 12],
        "UG2_EA_MANCAL_GUIA_CASQUILHO_TEMP_FALHA_LEITURA":          [12328, 13],
        "UG2_EA_MANCAL_COMBINADO_CASQUILHO_TEMP_FALHA_LEITURA":     [12328, 14],
        "UG2_EA_MANCAL_COMBINADO_ESCORA_TEMP_FALHA_LEITURA":        [12328, 15],

        # FALHA LEITURA ANALOGICAS
        "UG2_EA_UHRV_PRESSAO_OLEO_FALHA_LEITURA":                   [12340, 0], # Duplicado
        "UG2_EA_SINAL_NIVEL_JUSANTE_FALHA_LEITURA":                 [12340, 0], # Duplicado

        # ALARME PRESSÃO
        "UG2_EA_UHRV_PRESSAO_OLEO_MUITO_ALTO":                      [12342, 0],
        "UG2_EA_UHRV_PRESSAO_OLEO_ALTO":                            [12344, 0],
        "UG2_EA_UHRV_PRESSAO_OLEO_BAIXA":                           [12346, 0],
        "UG2_EA_UHRV_PRESSAO_OLEO_MUITO_BAIXA":                     [12348, 0],

        # ALARME NÍVEL JUSANTE
        "UG2_EA_SINAL_NIVEL_JUSANTE_MUITO_ALTO":                    [12342, 1],
        "UG2_EA_SINAL_NIVEL_JUSANTE_ALTO":                          [12344, 1],
        "UG2_EA_SINAL_NIVEL_JUSANTE_BAIXA":                         [12346, 1],
        "UG2_EA_SINAL_NIVEL_JUSANTE_MUITO_BAIXA":                   [12348, 1],

        ## DRIVER RV
        # ALARMES
        "UG2_RV_ALARME_SOBREFREQUENCIA":                            [66, 0],
        "UG2_RV_ALARME_SUBFREQUENCIA":                              [66, 1],

        # FALHAS 1
        "UG2_RV_FALHA_1":                                           67,
        "UG2_RV_FALHA_1_SOBREFREQ_INSTANT":                         [67, 0],
        "UG2_RV_FALHA_1_SOBREFREQ_TEMPOR":                          [67, 1],
        "UG2_RV_FALHA_1_SUBFREQ_TEMPORIZADA":                       [67, 2],
        "UG2_RV_FALHA_1_GIRANDO_SEM_REG_GIRO_INDEV":                [67, 3],
        "UG2_RV_FALHA_1_LEIT_POS_DISTRIBUIDOR":                     [67, 4],
        "UG2_RV_FALHA_1_LEIT_POTENCIA_ATIVA":                       [67, 6],
        "UG2_RV_FALHA_1_LEIT_REFERENCIA_POTENCIA":                  [67, 7],
        "UG2_RV_FALHA_1_NV_MONTANTE_MUITO_BAIXO":                   [67, 10],
        "UG2_RV_FALHA_1_CONTROLE_POS_DISTRIBUIDOR":                 [67, 11],
        "UG2_RV_FALHA_1_RUIDO_MED_VELOC_PRINCIPAL":                 [67, 13],
        "UG2_RV_FALHA_1_RUIDO_MED_VELOC_RETAGUARDA":                [67, 14],
        "UG2_RV_FALHA_1_PERDA_MED_VELOC_PRINCIPAL":                 [67, 15],

        # FALHAS 2
        "UG2_RV_FALHA_2_PERDA_MED_VELOC_RETAGUARDA":                [68, 0],
        "UG2_RV_FALHA_2_TEMPO_EXCESSIVO_PARTIDA":                   [68, 1],
        "UG2_RV_FALHA_2_TEMPO_EXCESSIVO_PARADA":                    [68, 2],
        "UG2_RV_FALHA_2_DIF_MED_VELO_PRINCIPAL_RETAGUARDA":         [68, 4],

        ## DRIVER RT
        # ENTRADAS DIGITAIS
        "UG2_RT_ED_CROWBAR_INATIVO":                                [30, 9],
        "UG2_RT_ED_SELEC_MODO_CONTROLE_ISOLADO":                    [30, 2],

        # SAÍDAS DIGITAIS
        "UG2_RT_SD_RELE_ALARME":                                    [31, 1],

        # ALARMES 1
        "UG2_RT_ALARMES_1_SOBRETENSAO":                             [70, 0],
        "UG2_RT_ALARMES_1_SUBTENSAO":                               [70, 1],
        "UG2_RT_ALARMES_1_SOBREFREQUENCIA":                         [70, 2],
        "UG2_RT_ALARMES_1_SUBFREQUENCIA":                           [70, 3],
        "UG2_RT_ALARMES_1_LIMITE_SUP_POT_REATIVA":                  [70, 4],
        "UG2_RT_ALARMES_1_LIMITE_INF_POT_REATIVA":                  [70, 5],
        "UG2_RT_ALARMES_1_LIMITE_SUP_FATOR_POTENCIA":               [70, 6],
        "UG2_RT_ALARMES_1_LIMITE_INF_FATOR_POTENCIA":               [70, 7],
        "UG2_RT_ALARMES_1_VARIACAO_TENSAO":                         [70, 8],
        "UG2_RT_ALARMES_1_POTENCIA_ATIVA_REVERSA":                  [70, 9],
        "UG2_RT_ALARMES_1_SOBRECORRENTE_TERMINAL":                  [70, 10],
        "UG2_RT_ALARMES_1_LIMITE_SUP_CORRENTE_EXCITACAO":           [70, 11],
        "UG2_RT_ALARMES_1_LIMITE_INF_CORRENTE_EXCITACAO":           [70, 12],
        "UG2_RT_ALARMES_1_TEMP_MUITO_ALTA_ROTOR":                   [70, 13],
        "UG2_RT_ALARMES_1_PRES_TENS_TERM_AUSEN_CORR_EXCI":          [70, 14],
        "UG2_RT_ALARMES_1_PRES_CORR_EXCI_AUSEN_TENS_TERM":          [70, 15],

        # ALARMES 2
        "UG2_RT_ALARMES_2_FALHA_CONTROLE_CORRENTE_EXCI":            [71, 0],
        "UG2_RT_ALARMES_2_FALHA_CONTROLE_TENSAO_TERM":              [71, 1],
        "UG2_RT_ALARMES_2_CROWBAR_ATUADO_REGUL_HABIL":              [71, 2],
        "UG2_RT_ALARMES_2_FALHA_HABIL_DRIVE_EXCI":                  [71, 3],
        "UG2_RT_ALARMES_2_FALHA_FECHAR_CONTATOR_CAMPO":             [71, 4],
        "UG2_RT_ALARMES_2_FALHA_CORR_EXCI_PRE_EXCI_ATIVA":          [71, 5],
        "UG2_RT_ALARMES_2_PERDA_MEDICAO_POTENCIA_REATIVA":          [71, 6],
        "UG2_RT_ALARMES_2_PERDA_MEDICAO_TENSAO_TERMINAL":           [71, 7],
        "UG2_RT_ALARMES_2_PERDA_MEDICAO_CORRENTE_EXCI":             [71, 8],
        "UG2_RT_ALARMES_2_RUIDO_INSTRUMEN_REATIVO":                 [71, 9],
        "UG2_RT_ALARMES_2_RUIDO_INSTRUMEN_TENSAO":                  [71, 10],
        "UG2_RT_ALARMES_2_RUIDO_INSTRUMEN_EXCI_PRINCI":             [71, 11],
        "UG2_RT_ALARMES_2_RUIDO_INSTRUMEN_EXCI_RETAG":              [71, 12],

        # FALHAS 1
        "UG2_RT_FALHAS_1_SOBRETENSAO":                              [72, 0],
        "UG2_RT_FALHAS_1_SUBTENSAO":                                [72, 1],
        "UG2_RT_FALHAS_1_SOBREFREQUENCIA":                          [72, 2],
        "UG2_RT_FALHAS_1_SUBFREQUENCIA":                            [72, 3],
        "UG2_RT_FALHAS_1_LIMITE_SUP_POT_REATIVA":                   [72, 4],
        "UG2_RT_FALHAS_1_LIMITE_INF_POT_REATIVA":                   [72, 5],
        "UG2_RT_FALHAS_1_LIMITE_SUP_FATOR_POT":                     [72, 6],
        "UG2_RT_FALHAS_1_LIMITE_INF_FATOR_POT":                     [72, 7],
        "UG2_RT_FALHAS_1_SOBRETENSAO_INST":                         [72, 8],
        "UG2_RT_FALHAS_1_VARIACAO_TENSAO":                          [72, 9],
        "UG2_RT_FALHAS_1_POT_ATIVA_REVERSA":                        [72, 10],
        "UG2_RT_FALHAS_1_SOBRECORRENTE_TERMINAL":                   [72, 11],
        "UG2_RT_FALHAS_1_LIMITE_SUP_CORRENTE_EXCITACAO":            [72, 12],
        "UG2_RT_FALHAS_1_LIMITE_INF_CORRENTE_EXCITACAO":            [72, 13],
        "UG2_RT_FALHAS_1_LIMITE_SUP_TENSAO_EXCITACAO":              [72, 14],
        "UG2_RT_FALHAS_1_LIMITE_INF_TENSAO_EXCITACAO":              [72, 15],

        # FALHAS 2
        "UG2_RT_FALHAS_2_TEMP_MUITO_ALTA_ROTOR":                    [73, 0],
        "UG2_RT_FALHAS_2_PRES_TENS_TERM_AUSEN_CORR_EXCI":           [73, 1],
        "UG2_RT_FALHAS_2_PRES_CORR_EXCI_AUSEN_TENS_TERM":           [73, 2],
        "UG2_RT_FALHAS_2_CONTROLE_CORR_EXCI":                       [73, 3],
        "UG2_RT_FALHAS_2_TENSAO_TERMINAL":                          [73, 4],
        "UG2_RT_FALHAS_2_CROWBAR_ATUADO_REGULADOR_HABI":            [73, 5],
        "UG2_RT_FALHAS_2_HABI_DRIVE_EXCITACAO":                     [73, 6],
        "UG2_RT_FALHAS_2_FECHAR_CONTATOR_CAMPO":                    [73, 7],
        "UG2_RT_FALHAS_2_CORR_EXCITA_PRE_EXCXITA_ATIVA":            [73, 8],
        "UG2_RT_FALHAS_2_EXCESSIVO_PRE_EXCITACAO":                  [73, 9],
        "UG2_RT_FALHAS_2_EXCESSIVO_PARADA":                         [73, 10],
        "UG2_RT_FALHAS_2_EXCESSIVO_PARTIDA":                        [73, 11],
        "UG2_RT_FALHAS_2_BLOQ_EXTERNO":                             [73, 12],

        # FALHAS 3
        "UG2_RT_FALHAS_3_PERDA_MED_POT_REATIVA":                    [74, 0],
        "UG2_RT_FALHAS_3_PERDA_MED_TENSAO_TERM":                    [74, 1],
        "UG2_RT_FALHAS_3_PERDA_MED_CORR_EXCI_PRINCI":               [74, 2],
        "UG2_RT_FALHAS_3_PERDA_MED_CORR_EXCI_RETAG":                [74, 3],
        "UG2_RT_FALHAS_3_RUIDO_INSTRUM_REATIVO":                    [74, 4],
        "UG2_RT_FALHAS_3_RUIDO_INSTRUM_TENSAO":                     [74, 5],
        "UG2_RT_FALHAS_3_RUIDO_INSTRUM_EXCI_PRINCI":                [74, 6],
        "UG2_RT_FALHAS_3_RUIDO_INSTRUM_EXCI_RETAG":                 [74, 7],
    },
}