MB = {
    "SA": {
        "Alarme01_02":                          [1 + 14089 + 1000, 2],
    },

    "SE": {
        "CMD_RESET_ALARMES":                    0 + 12289 + 1000,
        "CMD_ABRIR_DJ52L":                      4 + 12289 + 1000,
        "CMD_FECHAR_DJ52L":                     5 + 12289 + 1000,

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

        "Alarme01_13":                          [1 + 14089 + 1000, 4],
    },

    "TDA": {
        "NV_BARRAGEM":                          3 + 12764 + 2000,

        "UHTA01_OPERACIONAL":                   [139 + 12764 + 2000, 0],
        "UHTA02_OPERACIONAL":                   [151 + 12764 + 2000, 0],

        "Alarme01_04":                          [1 + 14089 + 2000, 4],
    },

    "AD": {
        "CMD_CP_01_BUSCAR":                     60 + 12289 + 3100,
        "CMD_CP_02_BUSCAR":                     64 + 12289 + 3200,

        "CP_01_SP_POS":                         14 + 13569 + 3100,
        "CP_02_SP_POS":                         15 + 13569 + 3200,

        "CP_01_INFO":                           164 + 12764 + 3100,
        "CP_01_ABRINDO":                        [164 + 12764 + 3100, 0],
        "CP_01_FECHANDO":                       [164 + 12764 + 3100, 1],
        "CP_01_ABERTA":                         [164 + 12764 + 3100, 2],
        "CP_01_FECHADA":                        [164 + 12764 + 3100, 3],
        "CP_01_PARADA":                         [164 + 12764 + 3100, 4],
        "CP_01_ACION_LOCAL":                    [164 + 12764 + 3100, 5],

        "CP_01_POSICAO":                        165 + 12764 + 3100,

        "CP_02_INFO":                           166 + 12764 + 3200,
        "CP_02_ABRINDO":                        [166 + 12764 + 3200, 0],
        "CP_02_FECHANDO":                       [166 + 12764 + 3200, 1],
        "CP_02_ABERTA":                         [166 + 12764 + 3200, 2],
        "CP_02_FECHADA":                        [166 + 12764 + 3200, 3],
        "CP_02_PARADA":                         [166 + 12764 + 3200, 4],
        "CP_02_ACION_LOCAL":                    [166 + 12764 + 3200, 5],

        "CP_02_POSICAO":                        167 + 12764 + 3200,

        "Alarme28_00":                          [28 + 14089 + 3000, 0],
    },

    "UG1": {
        "CMD_RESET_ALARMES":                    0 + 12289 + 10000,
        "CMD_OPER_UP":                          2 + 12289 + 10000,
        "CMD_OPER_US":                          6 + 12289 + 10000,
        "CMD_OPER_EMER":                        7 + 12289 + 10000,

        "CRTL_POT_ALVO":                        17 + 13569 + 10000,

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

        "POT_ATIVA_MEDIA":                      73 + 12764 + 10000,

        "ENTRADA_TURBINA_PRESSAO":              37 + 12764 + 10000,
        "GERADOR_FASE_R_TMP":                   107 + 12764 + 10000,
        "GERADOR_FASE_S_TMP":                   108 + 12764 + 10000,
        "GERADOR_FASE_T_TMP":                   109 + 12764 + 10000,
        "MANCAL_GERADOR_LA_1_TMP":              110 + 12764 + 10000,
        "MANCAL_GERADOR_LA_2_TMP":              111 + 12764 + 10000,
        "MANCAL_GERADOR_LNA_2_TMP":             112 + 12764 + 10000,
        "MANCAL_GERADOR_LNA_1_TMP":             113 + 12764 + 10000,
        "MANCAL_TURBINA_RADIAL":                114 + 12764 + 10000,
        "MANCAL_TURBINA_ESCORA":                115 + 12764 + 10000,
        "MANCAL_TURBINA_CONTRA_ESCORA":         116 + 12764 + 10000,

        "Alarme01_03":                          [1 + 14199 + 10000, 3],
    },

    "UG2": {
        "CMD_RESET_ALARMES":                    0 + 12289 + 20000,
        "CMD_OPER_UP":                          2 + 12289 + 20000,
        "CMD_OPER_US":                          6 + 12289 + 20000,
        "CMD_OPER_EMERGENCIA_LIGAR":            7 + 12289 + 20000,

        "CRTL_POT_ALVO":                        17 + 13569 + 20000,

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

        "POT_ATIVA_MEDIA":                      73 + 12764 + 20000,

        "ENTRADA_TURBINA_PRESSAO":              37 + 12764 + 20000,
        "GERADOR_FASE_R_TMP":                   107 + 12764 + 20000,
        "GERADOR_FASE_S_TMP":                   108 + 12764 + 20000,
        "GERADOR_FASE_T_TMP":                   109 + 12764 + 20000,
        "MANCAL_GERADOR_LA_1_TMP":              110 + 12764 + 20000,
        "MANCAL_GERADOR_LA_2_TMP":              111 + 12764 + 20000,
        "MANCAL_GERADOR_LNA_2_TMP":             112 + 12764 + 20000,
        "MANCAL_GERADOR_LNA_1_TMP":             113 + 12764 + 20000,
        "MANCAL_TURBINA_RADIAL":                114 + 12764 + 20000,
        "MANCAL_TURBINA_ESCORA":                115 + 12764 + 20000,
        "MANCAL_TURBINA_CONTRA_ESCORA":         116 + 12764 + 20000,

        "Alarme01_03":                          [1 + 14199 + 20000, 3],
    },

    "UG3": {
        "CMD_RESET_ALARMES":                    0 + 12289 + 30000,
        "CMD_OPER_UP":                          2 + 12289 + 30000,
        "CMD_OPER_US":                          6 + 12289 + 30000,
        "CMD_OPER_EMERGENCIA_LIGAR":            7 + 12289 + 30000,

        "CRTL_POT_ALVO":                        17 + 13569 + 30000,

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

        "POT_ATIVA_MEDIA":                      73 + 12764 + 30000,

        "ENTRADA_TURBINA_PRESSAO":              37 + 12764 + 30000,
        "GERADOR_FASE_R_TMP":                   107 + 12764 + 30000,
        "GERADOR_FASE_S_TMP":                   108 + 12764 + 30000,
        "GERADOR_FASE_T_TMP":                   109 + 12764 + 30000,
        "MANCAL_GERADOR_LA_1_TMP":              110 + 12764 + 30000,
        "MANCAL_GERADOR_LA_2_TMP":              111 + 12764 + 30000,
        "MANCAL_GERADOR_LNA_2_TMP":             112 + 12764 + 30000,
        "MANCAL_GERADOR_LNA_1_TMP":             113 + 12764 + 30000,
        "MANCAL_TURBINA_RADIAL":                114 + 12764 + 30000,
        "MANCAL_TURBINA_ESCORA":                115 + 12764 + 30000,
        "MANCAL_TURBINA_CONTRA_ESCORA":         116 + 12764 + 30000,

        "Alarme01_03":                          [1 + 14199 + 30000, 3],
    },

    "UG4": {
        "CMD_RESET_ALARMES":                    0 + 12289 + 40000,
        "CMD_OPER_UP":                          2 + 12289 + 40000,
        "CMD_OPER_US":                          6 + 12289 + 40000,
        "CMD_OPER_EMERGENCIA_LIGAR":            7 + 12289 + 40000,

        "CRTL_POT_ALVO":                        17 + 13569 + 40000,

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

        "POT_ATIVA_MEDIA":                      73 + 12764 + 40000,

        "ENTRADA_TURBINA_PRESSAO":              37 + 12764 + 40000,
        "GERADOR_FASE_R_TMP":                   107 + 12764 + 40000,
        "GERADOR_FASE_S_TMP":                   108 + 12764 + 40000,
        "GERADOR_FASE_T_TMP":                   109 + 12764 + 40000,
        "MANCAL_GERADOR_LA_1_TMP":              110 + 12764 + 40000,
        "MANCAL_GERADOR_LA_2_TMP":              111 + 12764 + 40000,
        "MANCAL_GERADOR_LNA_2_TMP":             112 + 12764 + 40000,
        "MANCAL_GERADOR_LNA_1_TMP":             113 + 12764 + 40000,
        "MANCAL_TURBINA_RADIAL":                114 + 12764 + 40000,
        "MANCAL_TURBINA_ESCORA":                115 + 12764 + 40000,
        "MANCAL_TURBINA_CONTRA_ESCORA":         116 + 12764 + 40000,

        "Alarme01_03":                          [1 + 14199 + 40000, 3],
    },
}