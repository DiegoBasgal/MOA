REG_RELE = {
    "BAY": {
        "TENSAO_FASE_A":                                10,         # RELÉ -> BAY
        "TENSAO_FASE_B":                                13,         # RELÉ -> BAY
        "TENSAO_FASE_C":                                16,         # RELÉ -> BAY
        "TENSAO_VS":                                    19,         # RELÉ -> BAY

        "RESET_TRIP_RELE":                              [40, 2],    # RELÉ -> BAY

        "CMD_FECHA_DJ":                                 [43, 2],    # RELÉ -> BAY

        "DJ_MOLA_CARREGADA":                            [44, 1],    # RELÉ -> BAY
        "SECC_FECHADA":                                 [44, 4],    # RELÉ -> BAY

        "FALHA_ABERTURA_DJL":                           [47, 1],    # RELÉ -> BAY

        "ID_BARRA_VIVA":                                [53, 1],    # RELÉ -> BAY
        "ID_BARRA_MORTA":                               [53, 7],    # RELÉ -> BAY

        "ID_LINHA_VIVA":                                [54, 0],    # RELÉ -> BAY
        "ID_LINHA_MORTA":                               [54, 1],    # RELÉ -> BAY
    },

    "SE": {
        "DJ_LINHA_FECHADO":                             [43, 0],    # RELÉ -> SE
        "FALHA_PARTIDA_RECE_RELE_TE":                   [43, 2],    # RELÉ -> SE

        "FALHA_ABERTURA_DJ_LINHA_3":                    [44, 3],    # RELÉ -> SE
        "FALHA_ABERTURA_DJ_LINHA_4":                    [44, 4],    # RELÉ -> SE

        "SOBRECORR_INST_SEQUEN_NEG_Z3":                 [46, 1],    # RELÉ -> SE
        "SOBRECORR_INST_SEQUEN_NEG_Z2":                 [46, 2],    # RELÉ -> SE
        "SOBRECORR_INST_SEQUEN_NEG_Z1":                 [46, 3],    # RELÉ -> SE

        "FALHA_ABERTURA_DJ_LINHA_1":                    [48, 1],    # RELÉ -> SE
    },

    "TE": {
        "ATUA_86T":                                     [36, 4],

        "SOBRECORR_TEMP_RESIDUAL_ENROL_SEC":            [37, 1],
        "SOBRECORR_TEMP_FASE_ENROL_SEC":                [37, 6],

        "DIFERENCIAL_COM_RESTRICAO":                    [1117, 14],

        "SOBRECORR_TEMP_FASE_ENROL_PRIM":               [1117, 3],
        "SOBRECORR_TEMP_RESIDUAL_ENROL_PRIM":           [1117, 4],
        "DIFERENCIAL_SEM_RESTRICAO":                    [1117, 15],

        "RELE_ESTADO_TRIP":                             [1118, 15],
    },

    "UG": {
        # UG1
        "UG1_SOBREFREQ_ELEMENTO_2":                     [1, 4],
        "UG1_SOBREFREQ_ELEMENTO_1":                     [1, 5],
        "UG1_SUBFREQ_ELEMENTO_2":                       [1, 6],
        "UG1_SUBFREQ_ELEMENTO_1":                       [1, 7],

        "UG1_TRIP_RELE_PROTECAO_5":                     [2110, 5],
        "UG1_TRIP_RELE_PROTECAO_6":                     [2110, 6],

        "UG1_SOBRECORR_INSTANTANEA":                    [901, 0],
        "UG1_SOBRECORR_INSTANTANEA_NEUTRO":             [901, 1],
        "UG1_SOBRECORR_SEQUENCIA_NEG":                  [901, 2],
        "UG1_SOBRECORR_TEMPORIZADA_NEUTRO":             [901, 4],
        "UG1_DIFERENCIAL_COM_RESTRICAO":                [901, 14],
        "UG1_DIFERENCIAL_SEM_RESTRICAO":                [901, 15],

        "UG1_SUBTENSAO_GERAL":                          [902, 0],
        "UG1_SOBRETENSAO_GERAL":                        [902, 1],
        "UG1_POTENCIA_REVERSA":                         [902, 3],
        "UG1_VOLTZ_HERTZ":                              [902, 5],
        "UG1_SOBRECORR_RESTRICAO_TENSAO":               [902, 6],
        "UG1_FALHA_ABERTURA_DJ_MAQUINA":                [902, 8],
        "UG1_RECIBO_TRANSFER_DISPARO":                  [902, 9],
        "UG1_PERDA_CAMPO_GERAL":                        [902, 11],
        "UG1_FUGA_SOBRECORR_GERAL":                     [902, 12],
        "UG1_UNIDADE_FORA_PASSO":                       [902, 14],

        "UG1_FALHA_PARTIDA_DJ_MAQUINA":                 [2100, 6],
        "UG1_FALHA_ABERTURA_DJ_MAQUINA":                [2100, 7],
        "UG1_TRASFER_DISPARO_RELE_LINHA_TRAFO":         [2100, 11],

        # UG2
        "UG2_SOBREFREQ_ELEMENTO_2":                     [1, 4],
        "UG2_SOBREFREQ_ELEMENTO_1":                     [1, 5],
        "UG2_SUBFREQ_ELEMENTO_2":                       [1, 6],
        "UG2_SUBFREQ_ELEMENTO_1":                       [1, 7],

        "UG2_SOBRECORR_INSTANTANEA":                    [901, 0],
        "UG2_SOBRECORR_INSTANTANEA_NEUTRO":             [901, 1],
        "UG2_SOBRECORR_SEQUENCIA_NEG":                  [901, 2],
        "UG2_SOBRECORR_TEMPORIZADA_NEUTRO":             [901, 4],
        "UG2_DIFERENCIAL_COM_RESTRICAO":                [901, 14],
        "UG2_DIFERENCIAL_SEM_RESTRICAO":                [901, 15],

        "UG2_SUBTENSAO_GERAL":                          [902, 0],
        "UG2_SOBRETENSAO_GERAL":                        [902, 1],
        "UG2_POTENCIA_REVERSA":                         [902, 3],
        "UG2_VOLTZ_HERTZ":                              [902, 5],
        "UG2_SOBRECORR_RESTRICAO_TENSAO":               [902, 6],
        "UG2_FALHA_ABERTURA_DJ_MAQUINA":                [902, 8],
        "UG2_RECIBO_TRANSFER_DISPARO":                  [902, 9],
        "UG2_PERDA_CAMPO_GERAL":                        [902, 11],
        "UG2_FUGA_SOBRECORR_GERAL":                     [902, 12],
        "UG2_UNIDADE_FORA_PASSO":                       [902, 14],

        "UG2_FALHA_PARTIDA_DJ_MAQUINA":                 [2100, 6],
        "UG2_FALHA_ABERTURA_DJ_MAQUINA":                [2100, 7],
        "UG2_TRASFER_DISPARO_RELE_LINHA_TRAFO":         [2100, 11],


        "UG2_TRIP_RELE_PROTECAO_5":                     [2110, 5],
        "UG2_TRIP_RELE_PROTECAO_6":                     [2110, 6],
    }
}

REG_CLP = {
    "MOA": {
        "MOA_OUT_STATUS":                               409,

        "MOA_OUT_MODE":                                 11,
        "SM_STATE":                                     10,
        "PAINEL_LIDO":                                  12,
        "IN_EMERG":                                     13,
        "IN_HABILITA_AUTO":                             14,
        "IN_DESABILITA_AUTO":                           15,
        "OUT_EMERG":                                    16,

        "OUT_TARGET_LEVEL":                             417,
        "OUT_SETPOINT":                                 418,

        "IN_EMERG_UG1":                                 20,
        "OUT_BLOCK_UG1":                                21,
        "OUT_ETAPA_UG1":                                422,
        "OUT_STATE_UG1":                                423,

        "IN_EMERG_UG2":                                 25,
        "OUT_BLOCK_UG2":                                26,
        "OUT_STATE_UG2":                                427,
        "OUT_ETAPA_UG2":                                428,
    },

    "SE": {
        "LT_VAB":                                       50,
        "LT_VBC":                                       52,
        "LT_VCA":                                       53,

        "CMD_SE_REARME_BLOQUEIO_GERAL":                 [131, 0],
        "CMD_SE_REARME_86T":                            [131, 1],
        "CMD_SE_REARME_86BF":                           [131, 2],
        "CMD_SE_ABRE_52L":                              [131, 3], # CLP -> SA/SE
        "CMD_SE_FECHA_52L":                             [131, 4],
        "CMD_SE_RESET_REGISTROS":                       [131, 5],

        "REARME_86BF_86T":                              [, ],
        "52L_MOLA_CARREGADA":                           [, ],
        "52L_SELETORA_REMOTO":                          [, ],
        "52L_SELETORA_REMOTO":                          [, ],
        "RELE_LINHA_ATUADO":                            [, ],
        "RELE_LINHA_ATUACAO_BF":                        [, ],
        "89L_FECHADA":                                  [, ],
        "86T_ATUADO":                                   [, ],
        "86BF_ATUADO":                                  [, ],
        "FALHA_COMANDO_ABERTURA_52L":                   [, ],
        "FALHA_COMANDO_FECHAMENTO_52L":                 [, ],
        "SUPERVISAO_BOBINAS_RELES_BLOQUEIOS":           [, ],

        # TRANSFORMADOR ELEVADOR
        "TE_RELE_ATUADO":                               [, ],
        "TE_TRIP_RELE_BUCHHOLZ":                        [, ],
        "TE_ALARME_RELE_BUCHHOLZ":                      [, ],
        "TE_ALARME_RELE_BUCHHOLZ":                      [, ],
        "TE_TRIP_ALIVIO_PRESSAO":                       [, ],
        "TE_TRIP_TEMPERATURA_OLEO":                     [, ],
        "TE_ALM_TEMPERATURA_OLEO":                      [, ],
        "TE_NIVEL_OLEO_MUITO_ALTO":                     [, ],
        "TE_FALHA_TEMPERATURA_OLEO":                    [, ],
        "TE_NIVEL_OLEO_MUITO_BAIXO":                    [, ],
        "TE_ALARME_TEMPERATURA_OLEO":                   [, ],
        "TE_ALM_TEMPERATURA_ENROLAMENTO":               [, ],
        "TE_TRIP_TEMPERATURA_ENROLAMENTO":              [, ],
        "TE_ALARME_TEMPERATURA_ENROLAMENTO":            [, ],
        "TE_FALHA_TEMPERATURA_ENROLAMENTO":             [, ],
    },

    "SA": {
        "POCO_DRENAGEM_NIVEL_ALTO":                     [9, 0],
        "POCO_DRENAGEM_NIVEL_MUITO_ALTO":               [0, 9],
        "RETIFICADOR_SOBRETENSAO":                      [0, 14],
        "RETIFICADOR_SUBTENSAO":                        [0, 15],

        "DRENAGEM_BOMBA_1_FALHA":                       [1, 0],
        "DRENAGEM_BOMBA_2_FALHA":                       [1, 2],
        "DRENAGEM_BOMBA_3_FALHA":                       [1, 4],
        "FILTRAGEM_BOMBA_FALHA":                        [1, 6],
        "DRENAGEM_UNIDADES_BOMBA_FALHA":                [1, 12],

        "52SA1_SEM_FALHA":                              [2, 15],

        "RETIFICADOR_SOBRECORRENTE_SAIDA":              [3, 0],
        "RETIFICADOR_FUSIVEL_QUEIMADO":                 [3, 2],
        "RETIFICADOR_SOBRECORRENTE_BATERIAS":           [3, 1],
        "RETIFICADOR_FUGA_TERRA_POSITIVO":              [3, 5],
        "RETIFICADOR_FUGA_TERRA_NEGATIVO":              [3, 6],

        "52SA2_SEM_FALHA":                              [5, 1],
        "52SA3_SEM_FALHA":                              [5, 3],
        "DISJUNTORES_BARRA_SELETORA_REMOTO":            [5, 9],

        "SISTEMA_INCENDIO_ALARME_ATUADO":               [7, 6],
        "SISTEMA_SEGURANCA_ALARME_ATUADO":              [7, 7],
        "SA_72SA1_FECHADO":                             [7, 10],
        "DISJUNTORES_125VCC_FECHADOS":                  [7, 11],
        "DISJUNTORES_24VCC_FECHADOS":                   [7, 12],
        "COM_TENSAO_ALIMENTACAO_125VCC":                [7, 13],
        "COM_TENSAO_COMANDO_125VCC":                    [7, 14],
        "COM_TENSAO_COMANDO_24VCC":                     [7, 15],

        "FALHA_ABRIR_52SA1":                            [13, 0],
        "FALHA_FECHAR_52SA1":                           [13, 1],
        "FALHA_ABRIR_52SA2":                            [13, 2],
        "FALHA_FECHAR_52SA2":                           [13, 3],
        "FALHA_ABRIR_52SA3":                            [13, 4],
        "FALHA_FECHAR_52SA3":                           [13, 5],
        "GMG_FALHA_PARTIR":                             [13, 6],
        "GMG_FALHA_PARAR":                              [13, 7],
        "DRENAGEM_DISCREPANCIA_BOIAS_POCO":             [13, 9],
        "GMG_OPERACAO_MANUAL":                          [13, 10],

        "SISTEMA_AGUA_BOMBA_DISPONIVEL":                [17, 0],
        "SISTEMA_AGUA_FALHA_LIGA_BOMBA":                [17, 1],
        "SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_A":      [17, 3],
        "SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_A":      [17, 4],
        "SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_B":      [17, 5],
        "SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_B":      [17, 6],

        "RESET_FALHAS_BARRA_CA":                        [129, 0],
        "RESET_FALHAS_SISTEMA_AGUA":                    [129, 1],

        "REARME_BLOQUEIO_GERAL_E_FALHAS_SA":            [130, 0],

        # "BOMBA_RECALQUE_TUBO_SUCCAO_FALHA":             [, ],
        # "SEM_EMERGENCIA":                               [, ],
    },

    "TDA": {
        "NIVEL_MONTANTE":                               3,
        "FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_2":         32,
        "FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_1":         34,
        "NIVEL_JUSANTE_COMPORTA_1":                     36,
        "NIVEL_JUSANTE_COMPORTA_2":                     38,

        "FALHA_NIVEL_MONTANTE":                         [3, 0],

        "SEM_EMERGENCIA":                               [16, 8],

        "COM_TENSAO_CA":                                [17, 11],

        # LIMPA GRADES
        "LG_FALHA_ATUADA":                              [26, 15],

        "LG_OPERACAO_MANUAL":                           [28, 0],

        # VÁLVULA BORBOLETA
        "VB_FECHANDO":                                  [23, 0],

        "VB_CMD_RESET_FALHAS":                          [55, 0],

        # UNIADE HIDRÁULICA
        "UH_UNIDADE_HIDRAULICA_DISPONIVEL":             [5, 1],
        "UH_FALHA_LIGAR_BOMBA":                         [5, 2],

        "UH_FILTRO_LIMPO":                              [17, 13],

        # COMPORTA 1
        "CP1_COMPORTA_OPERANDO":                        [2, 0],
        "CP1_AGUARDANDO_COMANDO_ABERTURA":              [2, 3],
        "CP1_PRESSAO_EQUALIZADA":                       [2, 4],

        "CP1_CMD_REARME_FALHAS":                        [6, 0],
        "CP1_CMD_ABERTURA_CRACKING":                    [6, 1],
        "CP1_CMD_ABERTURA_TOTAL":                       [6, 2],
        "CP1_CMD_FECHAMENTO":                           [6, 3],
        "CP1_PERMISSIVOS_OK":                           [6, 15],

        "CP1_BLOQUEIO_ATUADO":                          [8, 15],

        "CP1_CRACKING":                                 [16, 0],
        "CP1_REMOTO":                                   [16, 6],

        "CP1_ABERTA":                                   [17, 14],
        "CP1_FECHADA":                                  [17, 15],

        # COMPORTA 2
        "CP2_COMPORTA_OPERANDO":                        [2, 0],
        "CP2_AGUARDANDO_COMANDO_ABERTURA":              [2, 3],
        "CP2_PRESSAO_EQUALIZADA":                       [2, 4],

        "CP2_CMD_REARME_FALHAS":                        [6, 0],
        "CP2_CMD_ABERTURA_CRACKING":                    [6, 1],
        "CP2_CMD_ABERTURA_TOTAL":                       [6, 2],
        "CP2_CMD_FECHAMENTO":                           [6, 3],
        "CP2_PERMISSIVOS_OK":                           [6, 15],

        "CP2_BLOQUEIO_ATUADO":                          [8, 15],

        "CP2_CRACKING":                                 [16, 0],
        "CP2_REMOTO":                                   [16, 6],

        "CP2_ABERTA":                                   [17, 14],
        "CP2_FECHADA":                                  [17, 15],
    },

    "UG": {
        "UG1_UG_P":                                     130,

        "UG1_RV_ESTADO_OPERACAO":                       [, ],
        "UG1_UG_HORIMETRO":                             [, ],
        "UG1_CMD_RESET_FALHAS_PASSOS":                  [, ],
        "UG1_CMD_REARME_BLOQUEIO_86M":                  [, ],
        "UG1_CMD_REARME_BLOQUEIO_86E":                  [, ],
        "UG1_CMD_REARME_BLOQUEIO_86H":                  [, ],
        "UG1_CMD_UHRV_REARME_FALHAS":                   [, ],
        "UG1_CMD_UHLM_REARME_FALHAS":                   [, ],
        "UG1_CMD_PARTIDA_CMD_SINCRONISMO":              [, ],
        "UG1_CMD_PARADA_CMD_DESABILITA_UHLM":           [, ],
        "UG1_CMD_RESET_FALHAS_PASSOS":                  [, ],
        "UG1_CMD_REARME_BLOQUEIO_86M":                  [, ],
        "UG1_CMD_REARME_BLOQUEIO_86E":                  [, ],
        "UG1_CMD_REARME_BLOQUEIO_86H":                  [, ],
        "UG1_CMD_UHRV_REARME_FALHAS":                   [, ],
        "UG1_CMD_UHLM_REARME_FALHAS":                   [, ],
        "UG1_CMD_PARADA_EMERGENCIA":                    [, ],
        "UG1_CMD_RESET_FALHAS_PASSOS":                  [, ],
        "UG1_CMD_REARME_BLOQUEIO_86M":                  [, ],
        "UG1_CMD_REARME_BLOQUEIO_86E":                  [, ],
        "UG1_CMD_REARME_BLOQUEIO_86H":                  [, ],
        "UG1_CMD_UHRV_REARME_FALHAS":                   [, ],
        "UG1_CMD_UHLM_REARME_FALHAS":                   [, ],
        "UG1_RV_SETPOINT_POTENCIA_ATIVA_PU":            [, ],
        "UG1_BLOQUEIO_86H_ATUADO":                      [, ],
        "UG1_RELE_700G_TRIP_ATUADO":                    [, ],
        "UG1_CMD_PARADA_EMERGENCIA":                    [, ],
        "UG1_UHRV_FILTRO_LIMPO":                        [, ],
        "UG1_UHLM_FILTRO_LIMPO":                        [, ],
        "UG1_RESISTENCIA_SEM_FALHA":                    [, ],
        "UG1_CPG_UG_PORTA_INTERNA_FECHADA":             [, ],
        "UG1_CPG_UG_PORTA_TRASEIRA_FECHADA":            [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_2":                               [, ],
        "UG1_RV_FALHA_2":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RT_FALHAS_3":                              [, ],
        "UG1_RT_FALHAS_3":                              [, ],
        "UG1_RT_FALHAS_3":                              [, ],
        "UG1_RT_FALHAS_3":                              [, ],
        "UG1_RT_FALHAS_3":                              [, ],
        "UG1_RT_FALHAS_3":                              [, ],
        "UG1_RT_FALHAS_3":                              [, ],
        "UG1_RT_FALHAS_3":                              [, ],
        "UG1_RV_SAIDAS_DIGITAIS":                       [, ],
        "UG1_RT_SAIDAS_DIGITAIS":                       [, ],
        "UG1_ALM_TEMP_OLEO_UHRV":                       [, ],
        "UG1_ALM_TEMP_OLEO_UHLM":                       [, ],
        "UG1_ALM_TEMP_MANCAL_GUIA":                     [, ],
        "UG1_ALM_TEMP_GERADOR_FASE_A":                  [, ],
        "UG1_ALM_TEMP_GERADOR_FASE_B":                  [, ],
        "UG1_ALM_TEMP_GERADOR_FASE_C":                  [, ],
        "UG1_ALM_TEMP_PONTE_FASE_A":                    [, ],
        "UG1_ALM_TEMP_PONTE_FASE_B":                    [, ],
        "UG1_ALM_TEMP_PONTE_FASE_C":                    [, ],
        "UG1_UHRV_UNIDADE_EM_MANUTENCAO":               [, ],
        "UG1_UHLM_UNIDADE_EM_MANUTENCAO":               [, ],
        "UG1_ALM_TEMP_TRAFO_EXCITACAO":                 [, ],
        "UG1_ESCOVAS_GASTAS_POLO_POSITIVO":             [, ],
        "UG1_ESCOVAS_GASTAS_POLO_NEGATIVO":             [, ],
        "UG1_ALM_TEMP_CASQ_MANCAL_COMBINADO":           [, ],
        "UG1_ALM_VIBRACAO_DETECCAO_VERTICAL":           [, ],
        "UG1_ALM_VIBRACAO_DETECCAO_HORIZONTAL":         [, ],
        "UG1_ALM_TEMP_1_MANCAL_GUIA_INTERNO":           [, ],
        "UG1_ALM_TEMP_2_MANCAL_GUIA_INTERNO":           [, ],
        "UG1_ALM_TEMP_1_PATINS_MANCAL_COMBINADO":       [, ],
        "UG1_ALM_TEMP_2_PATINS_MANCAL_COMBINADO":       [, ],
        "UG1_ALM_VIBRACAO_EIXO_X_MANCAL_COMBINADO":     [, ],
        "UG1_ALM_VIBRACAO_EIXO_Y_MANCAL_COMBINADO":     [, ],
        "UG1_ALM_VIBRACAO_EIXO_Z_MANCAL_COMBINADO":     [, ],
        "UG1_ALM_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO":  [, ],
        "UG1_ALM_TEMP_GERADOR_NUCLEO_ESTATORICO":       [, ],
        "UG1_TEMP_GERADOR_FASE_A":                      [, ],
        "UG1_TEMP_GERADOR_FASE_B":                      [, ],
        "UG1_TEMP_GERADOR_FASE_C":                      [, ],
        "UG1_TEMP_GERADOR_NUCLEO":                      [, ],
        "UG1_TEMP_MANCAL_GUIA_GERADOR":                 [, ],
        "UG1_TEMP_1_MANCAL_GUIA_INTERNO":               [, ],
        "UG1_TEMP_2_MANCAL_GUIA_INTERNO":               [, ],
        "UG1_TEMP_1_PATINS_MANCAL_COMBINADO":           [, ],
        "UG1_TEMP_2_PATINS_MANCAL_COMBINADO":           [, ],
        "UG1_TEMP_CASQ_MANCAL_COMBINADO":               [, ],
        "UG1_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO":      [, ],
        "UG1_PRESSAO_ENTRADA_TURBINA":                  [, ],
        "UG1_RV_SAIDAS_DIGITAIS":                       [, ],
        "UG1_RV_FALHA_2":                               [, ],
        "UG1_RT_SAIDAS_DIGITAIS":                       [, ],
        "UG1_RELE_700G_TRIP_ATUADO":                    [, ],
        "UG1_RELE_BLOQUEIO_86EH_DESATUADO":             [, ],
        "UG1_RV_RELE_TRIP_NAO_ATUADO":                  [, ],
        "UG1_RT_RELE_TRIP_NAO_ATUADO":                  [, ],
        "UG1_BT_EMERGENCIA_NAO_ATUADO":                 [, ],
        "UG1_CLP_GERAL_SEM_BLOQUEIO_EXTERNO":           [, ],
        "UG1_BLOQUEIO_86M_ATUADO":                      [, ],
        "UG1_BLOQUEIO_86E_ATUADO":                      [, ],
        "UG1_BLOQUEIO_86H_ATUADO":                      [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RV_FALHA_1":                               [, ],
        "UG1_RT_ALARMES_1":                             [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_2":                              [, ],
        "UG1_RT_FALHAS_2":                              [, ],
        "UG1_RT_FALHAS_2":                              [, ],
        "UG1_RT_FALHAS_2":                              [, ],
        "UG1_RT_FALHAS_2":                              [, ],
        "UG1_RT_FALHAS_2":                              [, ],
        "UG1_RT_FALHAS_2":                              [, ],
        "UG1_UHRV_BOMBA_1_FALHA":                       [, ],
        "UG1_UHRV_BOMBA_2_FALHA":                       [, ],
        "UG1_UHLM_BOMBA_1_FALHA":                       [, ],
        "UG1_UHLM_BOMBA_2_FALHA":                       [, ],
        "UG1_RV_RELE_ALARME_ATUADO":                    [, ],
        "UG1_CLP_GERAL_SISTEMA_AGUA_OK":                [, ],
        "UG1_CLP_GERAL_COM_TENSAO_BARRA_ESSENCIAIS":    [, ],
        "UG1_DISPARO_MECANICO_ATUADO":                  [, ],
        "UG1_DISPARO_MECANICO_DESATUADO":               [, ],
        "UG1_FALHA_HABILITAR_SISTEMA_AGUA":             [, ],
        "UG1_TRIP_TEMP_OLEO_UHLM":                      [, ],
        "UG1_TRIP_TEMP_OLEO_UHRV":                      [, ],
        "UG1_PARADA_BLOQUEIO_ABERTURA_DISJUNTOR":       [, ],
        "UG1_PARADA_BLOQUEIO_DESCARGA_POTENCIA":        [, ],
        "UG1_UHLM_FALHA_PRESSAO_LINHA_B1":              [, ],
        "UG1_UHLM_FALHA_PRESSAO_LINHA_B2":              [, ],
        "UG1_UHLM_FALHA_PRESSOSTATO_LINHA":             [, ],
        "UG1_RV_FALHA_HABILITAR_RV":                    [, ],
        "UG1_RV_FALHA_PARTIR_RV":                       [, ],
        "UG1_RV_FALHA_DESABILITAR_RV":                  [, ],
        "UG1_RT_FALHA_HABILITAR":                       [, ],
        "UG1_RT_FALHA_PARTIR":                          [, ],
        "UG1_RT_ALARMES_1":                             [, ],
        "UG1_RT_ALARMES_1":                             [, ],
        "UG1_RT_ALARMES_1":                             [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RT_FALHAS_1":                              [, ],
        "UG1_RV_FALHAS_2":                              [, ],
        "UG1_RV_FALHAS_2":                              [, ],
        "UG1_RV_FALHAS_2":                              [, ],
        "UG1_RV_FALHAS_2":                              [, ],
        "UG1_RV_FALHAS_2":                              [, ],
        "UG1_RV_FALHAS_2":                              [, ],
        "UG1_RV_FALHAS_2":                              [, ],
        "UG1_RV_FALHAS_2":                              [, ],
        "UG1_RELE_700G_BF_ATUADO":                      [, ],
        "UG1_SUPERVISAO_TENSAO_125VCC":                 [, ],
        "UG1_SUPERVISAO_TENSAO_24VCC":                  [, ],
        "UG1_SUPERVISAO_BOBINA_52G":                    [, ],
        "UG1_SUPERVISAO_BOBINA_86EH":                   [, ],
        "UG1_DISJUNTORES_125VCC_FECHADOS":              [, ],
        "UG1_DISJUNTORES_24VCC_FECHADOS":               [, ],
        "UG1_FALHA_TEMP_PONTE_FASE_A":                  [, ],
        "UG1_FALHA_TEMP_PONTE_FASE_B":                  [, ],
        "UG1_FALHA_TEMP_PONTE_FASE_C":                  [, ],
        "UG1_FALHA_TEMP_TRAFO_EXCITACAO":               [, ],
        "UG1_FALHA_TEMP_MANCAL_GUIA":                   [, ],
        "UG1_FALHA_TEMP_OLEO_UHRV":                     [, ],
        "UG1_FALHA_TEMP_OLEO_UHLM":                     [, ],
        "UG1_FALHA_TEMP_CASQ_MANCAL_COMBINADO":         [, ],
        "UG1_FALHA_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO":[, ],
        "UG1_FALHA_TEMP_1_PATINS_MANCAL_COMBINADO":     [, ],
        "UG1_FALHA_TEMP_2_PATINS_MANCAL_COMBINADO":     [, ],
        "UG1_FALHA_TEMP_1_MANCAL_GUIA_INTERNO":         [, ],
        "UG1_FALHA_TEMP_2_MANCAL_GUIA_INTERNO":         [, ],
        "UG1_FALHA_TEMP_GERADOR_NUCLEO_ESTATORICO":     [, ],
        "UG1_FALHA_TEMP_GERADOR_FASE_A":                [, ],
        "UG1_FALHA_TEMP_GERADOR_FASE_B":                [, ],
        "UG1_FALHA_TEMP_GERADOR_FASE_C":                [, ],
        "UG1_FALHA_PRESSAO_ENTRADA_TURBINA":            [, ],
        "UG1_FALHA_VIBRACAO_EIXO_X_MANCAL_COMBINADO":   [, ],
        "UG1_FALHA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO":   [, ],
        "UG1_FALHA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO":   [, ],
        "UG1_FALHA_VIBRACAO_DETECCAO_HORIZONTAL":       [, ],
        "UG1_FALHA_VIBRACAO_DETECACAO_VERTICAL":        [, ],
        "UG1_BLOQUEIO_86M_ATUADO":                      [, ],
        "UG1_TRIP_VIBRACAO_DETECCAO_HORIZONTAL":        [, ],
        "UG1_TRIP_VIBRACAO_DETECACAO_VERTICAL":         [, ],
        "UG1_TRIP_VIBRACAO_EIXO_X_MANCAL_COMBINADO":    [, ],
        "UG1_TRIP_VIBRACAO_EIXO_Y_MANCAL_COMBINADO":    [, ],
        "UG1_TRIP_VIBRACAO_EIXO_Z_MANCAL_COMBINADO":    [, ],
        "UG1_TRIP_TEMP_PONTE_FASE_A":                   [, ],
        "UG1_TRIP_TEMP_PONTE_FASE_B":                   [, ],
        "UG1_TRIP_TEMP_PONTE_FASE_C":                   [, ],
        "UG1_TRIP_TEMP_GERADOR_FASE_A":                 [, ],
        "UG1_TRIP_TEMP_GERADOR_FASE_B":                 [, ],
        "UG1_TRIP_TEMP_GERADOR_FASE_C":                 [, ],
        "UG1_TRIP_TEMP_GERADOR_NUCLEO_ESTATORICO":      [, ],
        "UG1_TRIP_TEMP_GERADOR_SAIDA_AR":               [, ],
        "UG1_TRIP_TEMP_TRAFO_ATERRAMENTO":              [, ],
        "UG1_TRIP_TEMP_TRAFO_EXCITACAO":                [, ],
        "UG1_TRIP_PRESSAO_ACUMULADOR_UHRV":             [, ],
        "UG1_TRIP_TEMP_CASQ_MANCAL_COMBINADO":          [, ],
        "UG1_TRIP_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO": [, ],
        "UG1_TRIP_TEMP_1_PATINS_MANCAL_COMBINADO":      [, ],
        "UG1_TRIP_TEMP_2_PATINS_MANCAL_COMBINADO":      [, ],
        "UG1_TRIP_TEMP_1_MANCAL_GUIA_INTERNO":          [, ],
        "UG1_TRIP_TEMP_2_MANCAL_GUIA_INTERNO":          [, ],
        "UG1_RV_FALHA_FECHAR_DISTRIBUIDOR":             [, ],
        "UG1_RT_FALHA_DESABILITAR":                     [, ],
    }
}