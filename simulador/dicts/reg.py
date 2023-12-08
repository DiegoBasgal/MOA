MB = {
    "SA": {
        "CONDICIONADOR":                        [1, 2],
    },

    "SE": {
        "CONDICIONADOR":                        [1, 0],

        "CMD_RESET_ALARMES":                    0 + 12764 + 1000,
        "CMD_ABRIR_DJ52L":                      4 + 12764 + 1000,
        "CMD_FECHAR_DJ52L":                     5 + 12764 + 1000,

        "DJ52L_ABERTO":                         [21 + 12764 + 1000, 0],
        "DJ52L_FECHADO":                        [21 + 12764 + 1000, 1],
        "DJ52L_INCONSISTENTE":                  [21 + 12764 + 1000, 2],
        "DJ52L_TRIP":                           [21 + 12764 + 1000, 3],
        "DJ52L_MOLA_CARREGADA":                 [21 + 12764 + 1000, 6],
        "DJ52L_FALTA_VCC":                      [21 + 12764 + 1000, 8],
        "DJ52L_CONDICAO":                       [21 + 12764 + 1000, 9],
        "DJ52L_FALHA_FECHAMENTO":               [21 + 12764 + 1000, 13],

        "SECC_89L_ABERTA":                      [22 + 12764 + 1000, 0],
        "SECC_89L_FECHADA":                     [22 + 12764 + 1000, 1],

        "TENSAO_RS":                            26 + 12764 + 1000,
        "TENSAO_ST":                            27 + 12764 + 1000,
        "TENSAO_TR":                            28 + 12764 + 1000,

        "POTENCIA_ATIVA_MEDIA":                 36 + 12764 + 1000,
    },

    "TDA": {
        "CONDICIONADOR":                        [1, 4],

        "NV_BARRAGEM":                          3 + 12764 + 2000,
    },

    "AD": {
        "CMD_CP_01_BUSCAR":                     60 + 12289 + 3000,
        "CMD_CP_02_BUSCAR":                     64 + 12289 + 3000,

        "CP_01_INFO":                           164 + 12764 + 3000,
        "CP_01_ABRINDO":                        [164 + 12764 + 3000, 0],
        "CP_01_FECHANDO":                       [164 + 12764 + 3000, 1],
        "CP_01_ABERTA":                         [164 + 12764 + 3000, 2],
        "CP_01_FECHADA":                        [164 + 12764 + 3000, 3],
        "CP_01_PARADA":                         [164 + 12764 + 3000, 4],
        "CP_01_ACION_LOCAL":                    [164 + 12764 + 3000, 5],

        "CP_01_POSICAO":                        163 + 12764 + 3000,

        "CP_02_INFO":                           166 + 12764 + 3000,
        "CP_02_ABRINDO":                        [166 + 12764 + 3000, 0],
        "CP_02_FECHANDO":                       [166 + 12764 + 3000, 1],
        "CP_02_ABERTA":                         [166 + 12764 + 3000, 2],
        "CP_02_FECHADA":                        [166 + 12764 + 3000, 3],
        "CP_02_PARADA":                         [166 + 12764 + 3000, 4],
        "CP_02_ACION_LOCAL":                    [166 + 12764 + 3000, 5],

        "CP_02_POSICAO":                        167 + 12764 + 3000,

        "Alarme28_00":                          [28 + 14089 + 3000, 0],
    },

    "UG1": {
        "CONDICIONADOR":                        [4, 1],

        "CMD_RESET_ALARMES":                    0 + 10000,
        "CMD_OPER_UP":                          2 + 10000,
        "CMD_OPER_US":                          6 + 10000,
        "CMD_OPER_EMER":                        7 + 10000,

        "CRTL_POT_ALVO":                        17 + 10000,

        "OPER_ETAPA_ALVO":                      9 + 12764 + 10000,
        "OPER_ETAPA_ALVO_UP":                   [9 + 12764 + 10000, 0],
        "OPER_ETAPA_ALVO_UPGM":                 [9 + 12764 + 10000, 1],
        "OPER_ETAPA_ALVO_UMD":                  [9 + 12764 + 10000, 2],
        "OPER_ETAPA_ALVO_UPS":                  [9 + 12764 + 10000, 3],
        "OPER_ETAPA_ALVO_US":                   [9 + 12764 + 10000, 4],

        "OPER_ETAPA_ATUAL":                     10 + 12764 + 10000,
        "OPER_ETAPA_ATUAL_UP":                  [10 + 12764 + 10000, 0],
        "OPER_ETAPA_ATUAL_UMD":                 [10 + 12764 + 10000, 2],
        "OPER_ETAPA_ATUAL_UPGM":                [10 + 12764 + 10000, 1],
        "OPER_ETAPA_ATUAL_US":                  [10 + 12764 + 10000, 4],
        "OPER_ETAPA_ATUAL_UPS":                 [10 + 12764 + 10000, 3],

        "POT_ATIVA_MEDIA":                      73 + 10000,

        "ENTRADA_TURBINA_PRESSAO":              37 + 10000,
        "GERADOR_FASE_R_TMP":                   107 + 10000,
        "GERADOR_FASE_S_TMP":                   108 + 10000,
        "GERADOR_FASE_T_TMP":                   109 + 10000,
        "MANCAL_GERADOR_LA_1_TMP":              110 + 10000,
        "MANCAL_GERADOR_LA_2_TMP":              111 + 10000,
        "MANCAL_GERADOR_LNA_2_TMP":             112 + 10000,
        "MANCAL_GERADOR_LNA_1_TMP":             113 + 10000,
        "MANCAL_TURBINA_RADIAL":                114 + 10000,
        "MANCAL_TURBINA_ESCORA":                115 + 10000,
        "MANCAL_TURBINA_CONTRA_ESCORA":         116 + 10000,
    },

    "UG2": {
        "CONDICIONADOR":                        [4, 1],

        "CMD_RESET_ALARMES":                    0 + 20000,
        "CMD_OPER_UP":                          2 + 20000,
        "CMD_OPER_US":                          6 + 20000,
        "CMD_OPER_EMERGENCIA_LIGAR":            7 + 20000,

        "CRTL_POT_ALVO":                        17 + 20000,

        "OPER_ETAPA_ALVO":                      9 + 12764 + 20000,
        "OPER_ETAPA_ALVO_UP":                   [9 + 12764 + 20000, 0],
        "OPER_ETAPA_ALVO_UPGM":                 [9 + 12764 + 20000, 1],
        "OPER_ETAPA_ALVO_UMD":                  [9 + 12764 + 20000, 2],
        "OPER_ETAPA_ALVO_UPS":                  [9 + 12764 + 20000, 3],
        "OPER_ETAPA_ALVO_US":                   [9 + 12764 + 20000, 4],

        "OPER_ETAPA_ATUAL":                     10 + 12764 + 20000,
        "OPER_ETAPA_ATUAL_UP":                  [10 + 12764 + 20000, 0],
        "OPER_ETAPA_ATUAL_UMD":                 [10 + 12764 + 20000, 2],
        "OPER_ETAPA_ATUAL_UPGM":                [10 + 12764 + 20000, 1],
        "OPER_ETAPA_ATUAL_UPS":                 [10 + 12764 + 20000, 3],
        "OPER_ETAPA_ATUAL_US":                  [10 + 12764 + 20000, 4],

        "POT_ATIVA_MEDIA":                      73 + 20000,

        "ENTRADA_TURBINA_PRESSAO":              37 + 20000,
        "GERADOR_FASE_R_TMP":                   107 + 20000,
        "GERADOR_FASE_S_TMP":                   108 + 20000,
        "GERADOR_FASE_T_TMP":                   109 + 20000,
        "MANCAL_GERADOR_LA_1_TMP":              110 + 20000,
        "MANCAL_GERADOR_LA_2_TMP":              111 + 20000,
        "MANCAL_GERADOR_LNA_2_TMP":             112 + 20000,
        "MANCAL_GERADOR_LNA_1_TMP":             113 + 20000,
        "MANCAL_TURBINA_RADIAL":                114 + 20000,
        "MANCAL_TURBINA_ESCORA":                115 + 20000,
        "MANCAL_TURBINA_CONTRA_ESCORA":         116 + 20000,
    },

    "UG3": {
        "CONDICIONADOR":                        [4, 1],

        "CMD_RESET_ALARMES":                    0 + 30000,
        "CMD_OPER_UP":                          2 + 30000,
        "CMD_OPER_US":                          6 + 30000,
        "CMD_OPER_EMERGENCIA_LIGAR":            7 + 30000,

        "CRTL_POT_ALVO":                        17 + 30000,

        "OPER_ETAPA_ALVO":                      9 + 12764 + 30000,
        "OPER_ETAPA_ALVO_UP":                   [9 + 12764 + 30000, 0],
        "OPER_ETAPA_ALVO_UPGM":                 [9 + 12764 + 30000, 1],
        "OPER_ETAPA_ALVO_UMD":                  [9 + 12764 + 30000, 2],
        "OPER_ETAPA_ALVO_UPS":                  [9 + 12764 + 30000, 3],
        "OPER_ETAPA_ALVO_US":                   [9 + 12764 + 30000, 4],

        "OPER_ETAPA_ATUAL":                     10 + 12764 + 30000,
        "OPER_ETAPA_ATUAL_UP":                  [10 + 12764 + 30000, 0],
        "OPER_ETAPA_ATUAL_UMD":                 [10 + 12764 + 30000, 2],
        "OPER_ETAPA_ATUAL_UPGM":                [10 + 12764 + 30000, 1],
        "OPER_ETAPA_ATUAL_US":                  [10 + 12764 + 30000, 4],
        "OPER_ETAPA_ATUAL_UPS":                 [10 + 12764 + 30000, 3],

        "POT_ATIVA_MEDIA":                      73 + 30000,

        "ENTRADA_TURBINA_PRESSAO":              37 + 30000,
        "GERADOR_FASE_R_TMP":                   107 + 30000,
        "GERADOR_FASE_S_TMP":                   108 + 30000,
        "GERADOR_FASE_T_TMP":                   109 + 30000,
        "MANCAL_GERADOR_LA_1_TMP":              110 + 30000,
        "MANCAL_GERADOR_LA_2_TMP":              111 + 30000,
        "MANCAL_GERADOR_LNA_2_TMP":             112 + 30000,
        "MANCAL_GERADOR_LNA_1_TMP":             113 + 30000,
        "MANCAL_TURBINA_RADIAL":                114 + 30000,
        "MANCAL_TURBINA_ESCORA":                115 + 30000,
        "MANCAL_TURBINA_CONTRA_ESCORA":         116 + 30000,
    },

    "UG4": {
        "CONDICIONADOR":                        [4, 1],

        "CMD_RESET_ALARMES":                    0 + 40000,
        "CMD_OPER_UP":                          2 + 40000,
        "CMD_OPER_US":                          6 + 40000,
        "CMD_OPER_EMERGENCIA_LIGAR":            7 + 40000,

        "CRTL_POT_ALVO":                        17 + 40000,

        "OPER_ETAPA_ALVO":                      9 + 12764 + 40000,
        "OPER_ETAPA_ALVO_UP":                   [9 + 12764 + 40000, 0],
        "OPER_ETAPA_ALVO_UPGM":                 [9 + 12764 + 40000, 1],
        "OPER_ETAPA_ALVO_UMD":                  [9 + 12764 + 40000, 2],
        "OPER_ETAPA_ALVO_UPS":                  [9 + 12764 + 40000, 3],
        "OPER_ETAPA_ALVO_US":                   [9 + 12764 + 40000, 4],

        "OPER_ETAPA_ATUAL":                     10 + 12764 + 40000,
        "OPER_ETAPA_ATUAL_UP":                  [10 + 12764 + 40000, 0],
        "OPER_ETAPA_ATUAL_UMD":                 [10 + 12764 + 40000, 2],
        "OPER_ETAPA_ATUAL_UPGM":                [10 + 12764 + 40000, 1],
        "OPER_ETAPA_ATUAL_UPS":                 [10 + 12764 + 40000, 3],
        "OPER_ETAPA_ATUAL_US":                  [10 + 12764 + 40000, 4],

        "POT_ATIVA_MEDIA":                      73 + 40000,

        "ENTRADA_TURBINA_PRESSAO":              37 + 40000,
        "GERADOR_FASE_R_TMP":                   107 + 40000,
        "GERADOR_FASE_S_TMP":                   108 + 40000,
        "GERADOR_FASE_T_TMP":                   109 + 40000,
        "MANCAL_GERADOR_LA_1_TMP":              110 + 40000,
        "MANCAL_GERADOR_LA_2_TMP":              111 + 40000,
        "MANCAL_GERADOR_LNA_2_TMP":             112 + 40000,
        "MANCAL_GERADOR_LNA_1_TMP":             113 + 40000,
        "MANCAL_TURBINA_RADIAL":                114 + 40000,
        "MANCAL_TURBINA_ESCORA":                115 + 40000,
        "MANCAL_TURBINA_CONTRA_ESCORA":         116 + 40000,
    },
}