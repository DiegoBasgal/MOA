MB = {
    "GERAL": {
        "USN_CONDICIONADOR":                                        [0, 15],
    },

    "TDA": {
        "NV_MONTANTE":                                              30 + 500,
        "NV_JUSANTE_CP1":                                           36 + 500,
        "NV_JUSANTE_CP2":                                           38 + 500,

        "UH_DISPONIVEL":                                            [5 + 500, 1],
        "VB_FECHANDO":                                              [23 + 500, 0],
        "LG_OPE_MANUAL":                                            [29 + 500, 0],

        "CP1_CRACKING":                                             [0 + 1000, 0],
        "CP1_REMOTO":                                               [0 + 1000, 6],
        "CP1_ABERTA":                                               [1 + 1000, 14],
        "CP1_FECHADA":                                              [1 + 1000, 15],
        "CP1_PERMISSIVOS_OK":                                       [7 + 1000, 10],
        "CP1_BLQ_ATUADO":                                           [8 + 1000, 15],
        "CP1_OPERANDO":                                             [11 + 1000, 0],
        "CP1_AGUARDANDO_CMD_ABERTURA":                              [11 + 1000, 3],
        "CP1_PRESSAO_EQUALIZADA":                                   [11 + 1000, 4],
        "CP1_CMD_ABERTURA_CRACKING":                                [51 + 1000, 1],
        "CP1_CMD_ABERTURA_TOTAL":                                   [51 + 1000, 2],
        "CP1_CMD_FECHAMENTO":                                       [51 + 1000, 3],

        "CP2_CRACKING":                                             [0 + 2000, 1],
        "CP2_REMOTO":                                               [0 + 2000, 2],
        "CP2_ABERTA":                                               [0 + 2000, 3],
        "CP2_FECHADA":                                              [0 + 2000, 9],
        "CP2_PERMISSIVOS_OK":                                       [12 + 2000, 15],
        "CP2_BLQ_ATUADO":                                           [15 + 2000, 15],
        "CP2_OPERANDO":                                             [17 + 2000, 0],
        "CP2_AGUARDANDO_CMD_ABERTURA":                              [17 + 2000, 3],
        "CP2_PRESSAO_EQUALIZADA":                                   [17 + 2000, 4],
        "CP2_CMD_ABERTURA_CRACKING":                                [53 + 2000, 1],
        "CP2_CMD_ABERTURA_TOTAL":                                   [53 + 2000, 2],
        "CP2_CMD_FECHAMENTO":                                       [53 + 2000, 3],
    },

    "BAY": {
        "LT_VAB":                                                   11 + 3000,
        "LT_VBC":                                                   14 + 3000,
        "LT_VCA":                                                   17 + 3000,
        "LT_VS":                                                    19 + 3000,
        "LT_P_MP":                                                  33 + 3000,
        "LT_P_MR":                                                  33 + 3000,

        "DJL_CMD_FECHAR":                                           85 + 3000,
        "RELE_RST_TRP":                                             88 + 3000,

        "DJL_FECHADO":                                              [44 + 3000, 0],
        "DJL_MOLA_CARREGADA":                                       [44 + 3000, 1],
        "SECC_FECHADA":                                             [44 + 3000, 4],
        "ID_BARRA_VIVA":                                            [53 + 3000, 1],
        "ID_BARRA_MORTA":                                           [53 + 3000, 7],
        "ID_LINHA_VIVA":                                            [54 + 3000, 0],
        "ID_LINHA_MORTA":                                           [54 + 3000, 1],
    },

    "SE": {
        "LT_VAB":                                                   48 + 4000,
        "LT_VBC":                                                   50 + 4000,
        "LT_VCA":                                                   52 + 4000,
        "LT_P":                                                     64 + 4000,

        "DJL_CMD_ABRIR":                                            [131 + 4000, 3],
        "DJL_CMD_FECHAR":                                           [131 + 4000, 4],
        "REGISTROS_CMD_RST":                                        [131 + 4000, 5],

        "TE_RELE_BUCHHOLZ_ALM":                                     [2 + 4000, 6],
        "DJL_SELETORA_REMOTO":                                      [5 + 4000, 10],
        "DJL_FECHADO":                                              [43 + 4000, 0],
        "DJL_MOLA_CARREGADA":                                       [43 + 4000, 1],
        "RELE_LINHA_ATUADO":                                        [44 + 4000, 1],
    },

    "UG1": {
        "RV_ESTADO_OPERACAO":                                       21 + 10000,
        "SETPONIT":                                                 30 + 10000,

        "GERADOR_FASE_A_TMP":                                       42 + 10000,
        "GERADOR_FASE_B_TMP":                                       44 + 10000,
        "GERADOR_FASE_C_TMP":                                       46 + 10000,
        "MANCAL_GUIA_TMP":                                          52 + 10000,
        "MANCAL_CASQ_COMB_TMP":                                     58 + 10000,
        "MANCAL_CONT_ESCO_COMB_TMP":                                60 + 10000,
        "MANCAL_COMB_PATINS_1_TMP":                                 62 + 10000,
        "MANCAL_COMB_PATINS_2_TMP":                                 64 + 10000,
        "MANCAL_GUIA_INTE_1_TMP":                                   66 + 10000,
        "MANCAL_GUIA_INTE_2_TMP":                                   68 + 10000,
        "GERADOR_NUCL_ESTAT_TMP":                                   70 + 10000,
        "ENTRADA_TURBINA_PRESSAO":                                  82 + 10000,
        "HORIMETRO":                                                108 + 10000,
        "P":                                                        132 + 10000,

        "PASSOS_CMD_RST_FLH":                                       [149 + 10000, 0],
        "PARTIDA_CMD_SINCRONISMO":                                  [149 + 10000, 10],
        "PARADA_CMD_EMERGENCIA":                                    [149 + 10000, 4],
        "PARADA_CMD_DESABILITA_UHLM":                               [149 + 10000, 15],
    },

    "UG2": {
        "RV_ESTADO_OPERACAO":                                       21 + 20000,
        "SETPONIT":                                                 30 + 20000,

        "GERADOR_FASE_A_TMP":                                       44 + 20000,
        "GERADOR_FASE_B_TMP":                                       46 + 20000,
        "GERADOR_FASE_C_TMP":                                       48 + 20000,
        "MANCAL_GUIA_TMP":                                          54 + 20000,
        "MANCAL_CASQ_COMB_TMP":                                     60 + 20000,
        "MANCAL_CONT_ESCO_COMB_TMP":                                62 + 20000,
        "MANCAL_COMB_PATINS_1_TMP":                                 64 + 20000,
        "MANCAL_COMB_PATINS_2_TMP":                                 66 + 20000,
        "MANCAL_GUIA_INTE_1_TMP":                                   68 + 20000,
        "MANCAL_GUIA_INTE_2_TMP":                                   70 + 20000,
        "GERADOR_NUCL_ESTAT_TMP":                                   72 + 20000,
        "ENTRADA_TURBINA_PRESSAO":                                  84 + 20000,
        "HORIMETRO":                                                108 + 20000,
        "P":                                                        132 + 20000,

        "PASSOS_CMD_RST_FLH":                                       [149 + 20000, 0],
        "PARTIDA_CMD_SINCRONISMO":                                  [149 + 20000, 10],
        "PARADA_CMD_EMERGENCIA":                                    [149 + 20000, 4],
        "PARADA_CMD_DESABILITA_UHLM":                               [149 + 20000, 15],
    },
}



MB["SE"]["CONDIC"] = [995, 4]
MB["UG1"]["CONDIC"] = [10995, 4]
MB["UG2"]["CONDIC"] = [20995, 4]
MB["BAY"]["CONDIC"] = [30999, 4]