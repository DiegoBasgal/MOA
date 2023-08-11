MB = {
    "GERAL": {
        "USN_CONDICIONADOR":                                        [0, 15],
    },

    "SE": {
        "LT_P":                                                     5,
        "POTENCIA_KW_MP":                                           10,
        "POTENCIA_KW_MR":                                           11,
        "LT_VAB":                                                   50,
        "LT_VBC":                                                   52,
        "LT_VCA":                                                   53,

        "DJL_CMD_FECHAR":                                           [131, 4],
        "BARRA_CA_RST_FLH":                                         [129, 0],

        "DJL_MOLA_CARREGADA":                                       [43, 1], # Ficticio
        "DJL_SELETORA_REMOTO":                                      [999, 0], # Ficticio
        "TE_RELE_BUCHHOLZ_ALM":                                     [999, 1], # Ficticio
    },

    "BAY": {
        "LT_VAB":                                                   10 + 30000,
        "LT_VBC":                                                   13 + 30000,
        "LT_VCA":                                                   16 + 30000,
        "RELE_RST_TRP":                                             [40 + 30000, 2],
        "DJL_CMD_FECHAR":                                           [43 + 30000, 2],
        "DJL_MOLA_CARREGADA":                                       [44 + 30000, 1],
        "SECC_FECHADA":                                             [44 + 30000, 4],
        "ID_BARRA_VIVA":                                            [53 + 30000, 1],
        "ID_BARRA_MORTA":                                           [53 + 30000, 7],
        "ID_LINHA_VIVA":                                            [54 + 30000, 0],
        "ID_LINHA_MORTA":                                           [54 + 30000, 1],
    },

    "TDA": {
        "NV_MONTANTE":                                              30,
        "NV_JUSANTE_CP1":                                           36,
        "NV_JUSANTE_CP2":                                           38,

        "UH_DISPONIVEL":                                            [5 + 500, 1],
        "VB_FECHANDO":                                              [23 + 500, 0],
        "LG_OPE_MANUAL":                                            [28 + 500, 0],

        "CP1_OPERANDO":                                             [2 + 1000, 0],
        "CP1_AGUARDANDO_CMD_ABERTURA":                              [2 + 1000, 3],
        "CP1_PRESSAO_EQUALIZADA":                                   [2 + 1000, 4],
        "CP1_BLQ_ATUADO":                                           [8 + 1000, 15],
        "CP1_PERMISSIVOS_OK":                                       [6 + 1000, 15],
        "CP1_CMD_ABERTURA_CRACKING":                                [6 + 1000, 1],
        "CP1_CMD_ABERTURA_TOTAL":                                   [6 + 1000, 2],
        "CP1_CMD_FECHAMENTO":                                       [6 + 1000, 3],
        "CP1_CRACKING":                                             [16 + 1000, 0],
        "CP1_REMOTO":                                               [16 + 1000, 6],
        "CP1_ABERTA":                                               [17 + 1000, 14],
        "CP1_FECHADA":                                              [17 + 1000, 15],

        "CP2_OPERANDO":                                             [2 + 2000, 0],
        "CP2_AGUARDANDO_CMD_ABERTURA":                              [2 + 2000, 3],
        "CP2_PRESSAO_EQUALIZADA":                                   [2 + 2000, 4],
        "CP2_BLQ_ATUADO":                                           [8 + 2000, 15],
        "CP2_PERMISSIVOS_OK":                                       [6 + 2000, 15],
        "CP2_CMD_ABERTURA_CRACKING":                                [6 + 2000, 1],
        "CP2_CMD_ABERTURA_TOTAL":                                   [6 + 2000, 2],
        "CP2_CMD_FECHAMENTO":                                       [6 + 2000, 3],
        "CP2_CRACKING":                                             [16 + 2000, 0],
        "CP2_REMOTO":                                               [16 + 2000, 6],
        "CP2_ABERTA":                                               [17 + 2000, 14],
        "CP2_FECHADA":                                              [17 + 2000, 15],

    },

    "UG1": {
        "GERADOR_FASE_A_TMP":                                       44 + 10000,
        "GERADOR_FASE_B_TMP":                                       46 + 10000,
        "GERADOR_FASE_C_TMP":                                       48 + 10000,
        "GERADOR_NUCL_ESTAT_TMP":                                   72 + 10000,
        "MANCAL_GUIA_TMP":                                          54 + 10000,
        "MANCAL_GUIA_INTE_1_TMP":                                   68 + 10000,
        "MANCAL_GUIA_INTE_2_TMP":                                   70 + 10000,
        "MANCAL_COMB_PATINS_1_TMP":                                 64 + 10000,
        "MANCAL_COMB_PATINS_2_TMP":                                 66 + 10000,
        "MANCAL_CASQ_COMB_TMP":                                     60 + 10000,
        "MANCAL_CONT_ESCO_COMB_TMP":                                62 + 10000,
        "ENTRADA_TURBINA_PRESSAO":                                  84 + 10000,
        "RV_ESTADO_OPERACAO":                                       21 + 10000,
        "SETPONIT":                                                 30 + 10000,
        "HORIMETRO":                                                108 + 10000,
        "P":                                                        130 + 10000,

        "RV_ESTADO_OPERACAO_2":                                     999 + 10000,

        "PASSOS_CMD_RST_FLH":                                       [148 + 10000, 0],
        "PARTIDA_CMD_SINCRONISMO":                                  [148 + 10000, 10],
        "PARADA_CMD_EMERGENCIA":                                    [148 + 10000, 4],
        "PARADA_CMD_DESABILITA_UHLM":                               [148 + 10000, 15],
    },

    "UG2": {
        "GERADOR_FASE_A_TMP":                                       44 + 20000,
        "GERADOR_FASE_B_TMP":                                       46 + 20000,
        "GERADOR_FASE_C_TMP":                                       48 + 20000,
        "GERADOR_NUCL_ESTAT_TMP":                                   72 + 20000,
        "MANCAL_GUIA_TMP":                                          54 + 20000,
        "MANCAL_GUIA_INTE_1_TMP":                                   68 + 20000,
        "MANCAL_GUIA_INTE_2_TMP":                                   70 + 20000,
        "MANCAL_COMB_PATINS_1_TMP":                                 64 + 20000,
        "MANCAL_COMB_PATINS_2_TMP":                                 66 + 20000,
        "MANCAL_CASQ_COMB_TMP":                                     60 + 20000,
        "MANCAL_CONT_ESCO_COMB_TMP":                                62 + 20000,
        "ENTRADA_TURBINA_PRESSAO":                                  84 + 20000,
        "RV_ESTADO_OPERACAO":                                       21 + 20000,
        "SETPONIT":                                                 30 + 20000,
        "HORIMETRO":                                                108 + 20000,
        "P":                                                        130 + 20000,

        "RV_ESTADO_OPERACAO_2":                                     999 + 20000,

        "PASSOS_CMD_RST_FLH":                                       [148 + 20000, 0],
        "PARTIDA_CMD_SINCRONISMO":                                  [148 + 20000, 10],
        "PARADA_CMD_EMERGENCIA":                                    [148 + 20000, 4],
        "PARADA_CMD_DESABILITA_UHLM":                               [148 + 20000, 15],
    },
}
