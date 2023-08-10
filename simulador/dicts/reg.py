MB = {
    "GERAL": {
        "USN_CONDICIONADOR":                                     [0, 15],
    },

    "SE": {
        "LT_P":                                                  5,
        "POTENCIA_KW_MP":                                        10,
        "POTENCIA_KW_MR":                                        11,
        "LT_VAB":                                                50,
        "LT_VBC":                                                52,
        "LT_VCA":                                                53,

        "DJL_CMD_FECHAR":                                        [131, 4],
        "BARRA_CA_RST_FLH":                                      [129, 0],

        "DJL_MOLA_CARREGADA":                                    [43, 1], # Ficticio
        "DJL_SELETORA_REMOTO":                                   [999, 0], # Ficticio
        "TE_RELE_BUCHHOLZ_ALM":                                  [999, 1], # Ficticio
    },

    "BAY": {
        "LT_VAB":                                               30010,
        "LT_VBC":                                               30013,
        "LT_VCA":                                               30016,
        "RELE_RST_TRP":                                         [30040, 2],
        "DJL_CMD_FECHAR":                                       [30043, 2],
        "DJL_MOLA_CARREGADA":                                   [30044, 1],
        "SECC_FECHADA":                                         [30044, 4],
        "ID_BARRA_VIVA":                                        [30053, 1],
        "ID_BARRA_MORTA":                                       [30053, 7],
        "ID_LINHA_VIVA":                                        [30054, 0],
        "ID_LINHA_MORTA":                                       [30054, 1],
    },

    "TDA": {
        "NV_MONTANTE":                                              3,
        "NV_JUSANTE_CP1":                                           7,
        "NV_JUSANTE_CP2":                                           8,

        "CP1_OPERANDO":                                             [2 + 1000, 0],
        "CP1_PERMISSIVOS_OK":                                       [6 + 1000, 15],
        "CP1_CMD_ABERTURA_CRACKING":                                [6 + 1000, 1],
        "CP1_CMD_ABERTURA_TOTAL":                                   [6 + 1000, 2],
        "CP1_CMD_FECHAMENTO":                                       [6 + 1000, 3],

        "CP2_OPERANDO":                                             [2 + 2000, 0],
        "CP2_PERMISSIVOS_OK":                                       [6 + 2000, 15],
        "CP2_CMD_ABERTURA_CRACKING":                                [6 + 2000, 1],
        "CP2_CMD_ABERTURA_TOTAL":                                   [6 + 2000, 2],
        "CP2_CMD_FECHAMENTO":                                       [6 + 2000, 3],
    },

    "UG1": {
        "PASSOS_CMD_RST_FLH":                                   [148 + 10000, 0],

        "PARTIDA_CMD_SINCRONISMO":                              [148 + 10000, 10],

        "PARADA_CMD_EMERGENCIA":                                [148 + 10000, 4],
        "PARADA_CMD_DESABILITA_UHLM":                           [148 + 10000, 15],

        "P":                                                    130 + 10000,
        "HORIMETRO":                                            108 + 10000,
        "SETPONIT":                                             40 + 10000,
        "RV_ESTADO_OPERACAO":                                   38 + 10000,
        "GERADOR_FASE_A_TMP":                                   26 + 10000,
        "GERADOR_FASE_B_TMP":                                   27 + 10000,
        "GERADOR_FASE_C_TMP":                                   28 + 10000,
        "GERADOR_NUCL_ESTAT_TMP":                               29 + 10000,
        "MANCAL_GUIA_TMP":                                      30 + 10000,
        "MANCAL_GUIA_INTE_1_TMP":                               31 + 10000,
        "MANCAL_GUIA_INTE_2_TMP":                               32 + 10000,
        "MANCAL_COMB_PATINS_1_TMP":                             33 + 10000,
        "MANCAL_COMB_PATINS_2_TMP":                             34 + 10000,
        "MANCAL_CASQ_COMB_TMP":                                 35 + 10000,
        "MANCAL_CONT_ESCO_COMB_TMP":                            36 + 10000,
        "ENTRADA_TURBINA_PRESSAO":                              37 + 10000,
    },

    "UG2": {
        "PASSOS_CMD_RST_FLH":                                   [148 + 20000, 0],

        "PARTIDA_CMD_SINCRONISMO":                              [148 + 20000, 10],

        "PARADA_CMD_EMERGENCIA":                                [148 + 20000, 4],
        "PARADA_CMD_DESABILITA_UHLM":                           [148 + 20000, 15],

        "P":                                                    130 + 20000,
        "HORIMETRO":                                            108 + 20000,
        "SETPONIT":                                             40 + 20000,
        "RV_ESTADO_OPERACAO":                                   38 + 20000,
        "GERADOR_FASE_A_TMP":                                   26 + 20000,
        "GERADOR_FASE_B_TMP":                                   27 + 20000,
        "GERADOR_FASE_C_TMP":                                   28 + 20000,
        "GERADOR_NUCL_ESTAT_TMP":                               29 + 20000,
        "MANCAL_GUIA_TMP":                                      30 + 20000,
        "MANCAL_GUIA_INTE_1_TMP":                               31 + 20000,
        "MANCAL_GUIA_INTE_2_TMP":                               32 + 20000,
        "MANCAL_COMB_PATINS_1_TMP":                             33 + 20000,
        "MANCAL_COMB_PATINS_2_TMP":                             34 + 20000,
        "MANCAL_CASQ_COMB_TMP":                                 35 + 20000,
        "MANCAL_CONT_ESCO_COMB_TMP":                            36 + 20000,
        "ENTRADA_TURBINA_PRESSAO":                              37 + 20000,
    }
}
