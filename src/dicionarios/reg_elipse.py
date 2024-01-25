

REG_SASE = {
    ### COMANDOS
    ## CMD_SA_SE
    "REARME_FALHAS":                                                                    [12289, 0],
    "PD_BOMBA_1_PRINCIPAL":                                                             [12289, 1],
    "PD_BOMBA_2_PRINCIPAL":                                                             [12289, 2],
    "DISJ_TSA_ABRE":                                                                    [12289, 13],
    "DISJ_TSA_FECHA":                                                                   [12289, 14],
    "DISJ_GMG_ABRE":                                                                    [12289, 15],

    "DISJ_GMG_FECHA":                                                                   [12288, 0],
    "DISJ_LINHA_FECHA":                                                                 [12288, 1],
    "DISJ_LINHA_ABRE":                                                                  [12288, 2],
    "SFA_COMUTA_ELEMENTO":                                                              [12288, 3],
    "SFA_AUTOMATICO":                                                                   [12288, 4],
    "SFA_MANUAL":                                                                       [12288, 5],
    "SFB_MANUAL":                                                                       [12288, 8],
    "SFB_AUTOMATICO":                                                                   [12288, 9],
    "SFB_COMUTA_ELEMENTO":                                                              [12288, 10],

    ### STATUS
    ## SST_ENTRADAS_DIGITAIS_0
    "BOTAO_REARME_FALHAS_PAINEL":                                                       [12309, 0],
    "BOTAO_BLOQUEIO_86BTBF":                                                            [12309, 1],
    "POCO_DRANAGEM_BOMBA_1_AUTOMATICO":                                                 [12309, 2],
    "POCO_DRENAGEM_BOMBA_2_ATUTOMATICO":                                                [12309, 3],
    "DISJUNTORES_MODO_REMOTO":                                                          [12309, 4],
    "DISJUNTOR_TSA_TRIP":                                                               [12309, 5],
    "DISJUNTOR_GMG_TRIP":                                                               [12309, 6],
    "RELE_BLOQUEIO_86BTBF":                                                             [12309, 7],
    "CARREGADOR_BATERIAS_FALHA":                                                        [12309, 8],
    "CONVERSOR_FIBRA_FALHA":                                                            [12309, 9],
    "SUPERVISOR_TENSAO_FALHA":                                                          [12309, 10],
    "DPS_TSA":                                                                          [12309, 11],
    "DPS_GMG":                                                                          [12309, 12],
    "POCO_DRENAGEM_BOMBA_1_DEFEITO":                                                    [12309, 13],
    "POCO_DRENAGEM_BOMBA_1_LIGADA":                                                     [12309, 14],
    "POCO_DRENAGEM_BOMBA_2_DEFEITO":                                                    [12309, 15],

    "POCO_DRENAGEM_BOMBA_2_LIGADA":                                                     [12308, 0],
    "SF_BOMBA_1_DEFEITO":                                                               [12308, 1],
    "SF_BOMBA_1_LIGADA":                                                                [12308, 2],
    "POCO_DRENAGEM_SENSOR_NIVEL_MUITO_BAIXO":                                           [12308, 5],
    "POCO_DRENAGEM_SENSOR_NIVEL_DESLIGA_BOMBAS":                                        [12308, 6],
    "POCO_DRENAGEM_SENSOR_NIVEL_LIGA_BOMBA":                                            [12308, 7],
    "POCO_DRENAGEM_SENSOR_NIVEL_ALTO":                                                  [12308, 8],
    "POCO_DRENAGEM_SENSOR_NIVEL_MUITO_ALTO":                                            [12308, 9],
    "DISJUNTOR_TSA_FECHADO":                                                            [12308, 10],
    "DISJUNTOR_GMG_FECHADO":                                                            [12308, 11],
    "SUPERVISOR_TENSAO_TSA_FALHA":                                                      [12308, 12],
    "SUPERVISOR_TENSAO_GMG_FALHA":                                                      [12308, 13],
    "TRAFO_ELEVADOR_TEMPERATURA_MUITO_ALTA":                                            [12308, 14],
    "SE_DISJUNTOR_LINHA_FECHADO":                                                       [12308, 15],

    ## SST_ENTRADAS_DIGITAIS_1
    "SE_DISJUNTOR_LINHA_ABERTO":                                                        [12311, 0],
    "TE_TEMPERATURA_ALARME":                                                            [12311, 1],
    "TE_PRESSAO_MUITO_ALTA":                                                            [12311, 2],
    "TE_NIVEL_OLEO_MUITO_BAIXO":                                                        [12311, 3],
    "PRTVA1_50_BF_":                                                                    [12311, 4],
    "PRTVA1_FILTRAGEM_ACIONA":                                                          [12311, 5],
    "PRTVA2_50BF":                                                                      [12311, 6],
    "PRTVA2_FILTRAGEM_ACIONA":                                                          [12311, 7],
    "SFA_ENTRADA_ELEMENTO_1_ABERTA":                                                    [12311, 8],
    "SFA_ENTRADA_ELEMENTO_2_ABERTA":                                                    [12311, 9],
    "SFA_LIMPEZA_ELEMENTO_1_ABERTA":                                                    [12311, 10],
    "SFA_LIMPEZA_ELEMENTO_2_ABERTA":                                                    [12311, 11],
    "SFB_PRESSAO_SAIDA":                                                                [12311, 12],
    "SFB_ENTRADA_ELEMENTO_1_ABERTA":                                                    [12311, 13],
    "SFB_ENTRADA_ELEMENTO_2_ABERTA":                                                    [12311, 14],
    "SFB_LIMPEZA_ELEMENTO_1_ABERTA":                                                    [12311, 15],

    "PSA_SFB_LIMPEZA_ELEMENTO_2_ABERTO":                                                [12310, 0],
    "PSA_CONVERSOR_FIBRA_FALHA":                                                        [12310, 1],
    "PSA_RELE_LINHA_SEM_TRIP_OU_FALHA":                                                 [12310, 2],

    ## STT_FALHAS_ANALOGICAS
    "NIVEL_JUSANTE_FALHA_LEITURA":                                                      [12339, 1],
    "SFA_PRESSAO_LADO_LIMPO_FALHA_LEITURA":                                             [12339, 2],
    "SFA_PRESSAO_LADO_SUJO_FALHA_LEITURA":                                              [12339, 3],
    "SFB_PRESSAO_LADO_LIMPO_FALHA_LEITURA":                                             [12339, 4],
    "SFB_PRESSAO_LADO_SUJO_FALHA_LEITURA":                                              [12339, 5],

    ## STT_ALARMES_HH_ANALOGICAS
    "NIVEL_JUSANTE_MUITO_ALTO":                                                         [12341, 0],
    "SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO":                                                [12341, 3],
    "SFA_PRESSAO_LADO_SUJO_MUITO_ALTO":                                                 [12341, 4],
    "SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO":                                                [12341, 5],
    "SFB_PRESSAO_LADO_SUJO_MUITO_ALTO":                                                 [12341, 6],

    ## STT_ALARMES_H_ANALOGICAS
    "PSA_NIVEL_JUSANTE_ALTO":                                                           [12343, 0],
    "PSA_SFA_PRESSAO_LADO_LIMPO_ALTO":                                                  [12343, 3],
    "PSA_SFA_PRESSAO_LADO_SUJO_ALTO":                                                   [12343, 4],
    "PSA_SFB_PRESSAO_LADO_LIMPO_ALTO":                                                  [12343, 5],
    "PSA_SFB_PRESSAO_LADO_SUJO_ALTO":                                                   [12343, 6],

    ## STT_ALARMES_L_ANALOGICAS
    "NIVEL_JUSANTE_BAIXO":                                                              [12345, 0],
    "SFA_PRESSAO_LADO_LIMPO_BAIXO":                                                     [12345, 3],
    "SFA_PRESSAO_LADO_SUJO_BAIXO":                                                      [12345, 4],
    "SFB_PRESSAO_LADO_LIMPO_BAIXO":                                                     [12345, 5],
    "SFB_PRESSAO_LADO_SUJO_BAIXO":                                                      [12345, 6],

    ## STT_ALARMES_LL_ANALOGICAS
    "NIVEL_JUSANTE_MUITO_BAIXO":                                                        [12347, 0],
    "SFA_PRESSAO_LADO_LIMPO_MUITO_BAIXO":                                               [12347, 3],
    "SFA_PRESSAO_LADO_SUJO_MUITO_BAIXO":                                                [12347, 4],
    "SFB_PRESSAO_LADO_LIMPO_MUITO_BAIXO":                                               [12347, 5],
    "SFB_PRESSAO_LADO_SUJO_MUITO_BAIXO":                                                [12347, 6],

    ## STT_SA_SE
    "DRENAGEM_BOMBA_1_INDISPONIVEL":                                                    [12349, 0],
    "DRENAGEM_BOMBA_2_INDISPONIVEL":                                                    [12349, 1],
    "DRENAGEM_BOMBA_1_PRINCIPAL":                                                       [12349, 2],
    "DRENAGEM_BOMBA_2_PRINCIPAL":                                                       [12349, 3],
    "DRENAGEM_BOIAS_DISCREPANCIA":                                                      [12349, 4],
    "SF_BOMBA_1_INDISPONIVEL":                                                          [12349, 5],
    "ESGOTAMENTO_BOMBA_2_INDISPONIVEL":                                                 [12349, 6],
    "SF_BOMBA_1_FALHA":                                                                 [12349, 7],
    "ESGOTAMENTO_BOMBA_2_FALHA":                                                        [12349, 8],
    "GMG_DISJUNTOR_FALHA_FECHAR":                                                       [12349, 9],
    "GMG_DISJUNTOR_FALHA_ABRIR":                                                        [12349, 10],
    "TSA_DISJUNTOR_FALHA_ABRIR":                                                        [12349, 11],
    "TSA_DISJUNTOR_FALHA_FECHAR":                                                       [12349, 12],
    "SE_DISJUNTOR_FALHA_ABRIR":                                                         [12349, 13],
    "SE_DISJUNTOR_FALHA_FECHAR":                                                        [12349, 14],

    ## STT_BLOQUEIO_50BF
    "BLOQUEIO_50BF_ATUADO":                                                             [12350, 15],

    ## STT_BLOQUEIO_86BTLSA
    "BLOQUEIO_86BTLSA_ATUADO":                                                          [12352, 15],

    ## STT_SF
    "SISTEMA_DE_FILTRAGEM_OPERANDO":                                                    [12355, 0],
    "SFA_COMUTACAO_MANUAL":                                                             [12355, 1],
    "SFA_COMUTACAO_BLOQUEADA":                                                          [12355, 2],
    "SFA_ELEMENTO_1_OPERANDO":                                                          [12355, 3],
    "SFA_ELEMENTO_1_LIMPEZA":                                                           [12355, 4],
    "SFA_ELEMENTO_2_LIMPEZA":                                                           [12355, 5],
    "SFA_ELEMENTO_2_OPERANDO":                                                          [12355, 6],
    "SFA_ELEMENTO_1_FALHA_ABRIR_ENTRADA":                                               [12355, 7],
    "SFA_ELEMENTO_1_FALHA_FECHAR_ENTRADA":                                              [12355, 8],
    "SFA_ELEMENTO_2_FALHA_ABRIR_ENTRADA":                                               [12355, 9],
    "SFA_ELEMENTO_2_FALHA_FECHAR_ENTRADA":                                              [12355, 10],
    "SFA_ELEMENTO_1_FALHA_ABRIR_LIMPEZA":                                               [12355, 11],
    "SFA_ELEMENTO_1_FALHA_FECHAR_LIMPEZA":                                              [12355, 12],
    "SFA_ELEMENTO_2_FALHA_ABRIR_LIMPEZA":                                               [12355, 13],
    "SFA_ELEMENTO_2_FALHA_FECHAR_LIMPEZA":                                              [12355, 14],
    "SFB_ELEMENTO_1_OPERANDO":                                                          [12355, 15],

    "SFB_ELEMENTO_1_LIMPEZA":                                                           [12354, 0],
    "SFB_ELEMENTO_2_LIMPEZA":                                                           [12354, 1],
    "SFB_ELEMENTO_2_OPERANDO":                                                          [12354, 2],
    "SFB_ELEMENTO_1_FALHA_ABRIR_ENTRADA":                                               [12354, 3],
    "SFB_ELEMENTO_1_FALHA_FECHAR_ENTRADA":                                              [12354, 4],
    "SFB_ELEMENTO_2_FALHA_ABRIR_ENTRADA":                                               [12354, 5],
    "SFB_ELEMENTO_2_FALHA_FECHAR_ENTRADA":                                              [12354, 6],
    "SFB_ELEMENTO_1_FALHA_ABRIR_LIMPEZA":                                               [12354, 7],
    "SFB_ELEMENTO_1_FALHA_FECHAR_LIMPEZA":                                              [12354, 8],
    "SFB_ELEMENTO_2_FALHA_ABRIR_LIMPEZA":                                               [12354, 9],
    "SFB_ELEMENTO_2_FALHA_FECHAR_LIMPEZA":                                              [12354, 10],
    "SFB_COMUTACAO_MANUAL":                                                             [12354, 11],
    "SFB_COMUTACAO_BLOQUEADA":                                                          [12354, 12],

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
    "RESET_GERAL":                                                                      [12289, 0],

    ### STATUS
    ## STT_ENTRADAS_DIGITAIS_0
    "DISPOSITIVO_PROTETOR_DE_SURTO":                                                    [12309, 0],
    "UHLG_BOMBA_1_LIGADA":                                                              [12309, 1],
    "UHLG_BOMBA_1_DEFEITO":                                                             [12309, 2],
    "UHLG_BOMBA_2_LIGADA":                                                              [12309, 3],
    "UHLG_BOMBA_2_DEFEITO":                                                             [12309, 4],
    "MONOVIA_MOTOR_1_LIGADA":                                                           [12309, 5],
    "MONOVIA_MOTOR_1_DEFEITO":                                                          [12309, 6],
    "MONOVIA_MOTOR_2_LIGADA":                                                           [12309, 7],
    "MONOVIA_MOTOR_2_DEFEITO":                                                          [12309, 8],
    "CONVERSOR_FIBRA_FALHA":                                                            [12309, 9],

    ## STT_ANALÓGICAS
    "NIVEL_JUSANTE_GRADE_FALHA_LEITURA":                                                [12329, 0],
    "NIVEL_MONTANTE_GRADE_FALHA_LEITURA":                                               [12329, 1],
    "NIVEL_JUSANTE_GRADE_MUITO_ALTO":                                                   [12329, 2],
    "NIVEL_MONTANTE_GRADE_MUITO_ALTO":                                                  [12329, 3],
    "NIVEL_JUSANTE_GRADE_ALTO":                                                         [12329, 4],
    "NIVEL_MONTANTE_GRADE_ALTO":                                                        [12329, 5],
    "NIVEL_JUSANTE_GRADE_BAIXO":                                                        [12329, 6],
    "NIVEL_MONTANTE_GRADE_BAIXO":                                                       [12329, 7],
    "NIVEL_JUSANTE_GRADE_MUITO_BAIXO":                                                  [12329, 8],
    "NIVEL_MONTANTE_GRADE_MUITO_BAIXO":                                                 [12329, 9],

    ## LEITURAS_ANALÓGICAS
    "NIVEL_JUSANTE_GRADE":                                                              12348,
    "NIVEL_MONTANTE_GRADE":                                                             12350,
}

REG_UG = {
    "UG1": {
        ### COMANDOS
        ## CMD_UG1
        "REARME_FALHAS":                                                                [12289, 0],
        "COMANDO_PARADA_DE_EMERGENCIA":                                                 [12289, 1],
        "CONTROLE_NIVEL":                                                               [12289, 2],
        "CONTROLE_POTENCIA_MANUAL":                                                     [12289, 3],
        "CONTROLE_POTENCIA_POR_NIVEL":                                                  [12289, 4],
        "PARADA_NIVEL_HABILITA":                                                        [12289, 5],
        "PARADA_NIVEL_DESABILITA":                                                      [12289, 6],
        "RV_MANUTENCAO":                                                                [12289, 10],
        "RV_AUTOMATICO":                                                                [12289, 11],

        ## CMD_UHRV
        "MODO_AUTOMATICO":                                                              [12291, 0],
        "MODO_MANUTENCAO":                                                              [12291, 1],
        "BOMBA_1_LIGA":                                                                 [12291, 2],
        "BOMBA_1_DESLIGA":                                                              [12291, 3],
        "BOMBA_2_LIGA":                                                                 [12291, 4],
        "BOMBA_2_DESLIGA":                                                              [12291, 5],
        "BOMBA_1_PRINCIPAL":                                                            [12291, 6],
        "BOMBA_2_PRINCIPAL":                                                            [12291, 7],

        ## CMD_UHLM
        "MODO_AUTOMATICO":                                                              [12293, 0],
        "MODO_MANUTENCAO":                                                              [12293, 1],
        "BOMBA_1_LIGA":                                                                 [12293, 2],
        "BOMBA_1_DESLIGA":                                                              [12293, 3],

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
        "TIRISTORES_TEMPERATURA_FALHA_LEITURA":                                         [12329, 0],
        "CROWBAR_TEMPERATURA_FALHA_LEITURA":                                            [12329, 1],
        "TRAFO_EXCITACAO_TEMPERATURA_FALHA_LEITURA":                                    [12329, 2],
        "UHRV_TEMPERATURA_OLEO_FALHA_LEITURA":                                          [12329, 3],
        "UHLM_TEMPERATURA_OLEO_FALHA_LEITURA":                                          [12329, 4],
        "GERADOR_FASE_A_TEMPERATURA_FALHA_LEITURA":                                     [12329, 7],
        "GERADOR_FASE_B_TEMPERATURA_FALHA_LEITURA":                                     [12329, 8],
        "GERADOR_FASE_C_TEMPERATURA_FALHA_LEITURA":                                     [12329, 9],
        "GERADOR_NUCLEO_1_TEMPERATURA_FALHA_LEITURA":                                   [12329, 10],
        "GERADOR_NUCLEO_2_TEMPERATURA_FALHA_LEITURA":                                   [12329, 11],
        "GERADOR_NUCLEO_3_TEMPERATURA_FALHA_LEITURA":                                   [12329, 12],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_FALHA_LEITURA":                              [12329, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMPERATURA_FALHA_LEITURA":                         [12329, 14],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_FALHA_LEITURA":                            [12329, 15],


        ## STT_ALARMES_HH_TEMPERATURA
        "TIRISTORES_TEMPERATURA_MUITO_ALTA":                                            [12331, 0],
        "CROWBAR_TEMPERATURA_MUITO_ALTA":                                               [12331, 1],
        "TRAFO_EXCITACAO_TEMPERATURA_MUITO_ALTA":                                       [12331, 2],
        "UHRV_TEMPERATURA_OLEO_MUITO_ALTA":                                             [12331, 3],
        "UHLM_TEMPERATURA_OLEO_MUITO_ALTA":                                             [12331, 4],
        "GERADOR_FASE_A_TEMPERATURA_MUITO_ALTA":                                        [12331, 7],
        "GERADOR_FASE_B_TEMPERATURA_MUITO_ALTA":                                        [12331, 8],
        "GERADOR_FASE_C_TEMPERATURA_MUITO_ALTA":                                        [12331, 9],
        "GERADOR_NUCLEO_1_TEMPERATURA_MUITO_ALTA":                                      [12331, 10],
        "GERADOR_NUCLEO_2_TEMPERATURA_MUITO_ALTA":                                      [12331, 11],
        "GERADOR_NUCLEO_3_TEMPERATURA_MUITO_ALTA":                                      [12331, 12],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_MUITO_ALTA":                                 [12331, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMPERATURA_MUITO_ALTA":                            [12331, 14],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_MUITO_ALTA":                               [12331, 15],


        ## STT_ALARMES_H_TEMPERATURA
        "TIRISTORES_TEMPERATURA_ALTA":                                                  [12333, 0],
        "CROWBAR_TEMPERATURA_ALTA":                                                     [12333, 1],
        "TRAFO_EXCITACAO_TEMPERATURA_ALTA":                                             [12333, 2],
        "UHRV_TEMPERATURA_OLEO_ALTA":                                                   [12333, 3],
        "UHLM_TEMPERATURA_OLEO_ALTA":                                                   [12333, 4],
        "GERADOR_FASE_A_TEMPERATURA_ALTA":                                              [12333, 7],
        "GERADOR_FASE_B_TEMPERATURA_ALTA":                                              [12333, 8],
        "GERADOR_FASE_C_TEMPERATURA_ALTA":                                              [12333, 9],
        "GERADOR_NUCLEO_1_TEMPERATURA_ALTA":                                            [12333, 10],
        "GERADOR_NUCLEO_2_TEMPERATURA_ALTA":                                            [12333, 11],
        "GERADOR_NUCLEO_3_TEMPERATURA_ALTA":                                            [12333, 12],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_ALTA":                                       [12333, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMPERATURA_ALTA":                                  [12333, 14],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_ALTA":                                     [12333, 15],

        ## STT_FALHAS_ANALOGICAS
        "UHRV_PRESSAO_OLEO_FALHA_LEITURA":                                              [12341, 0],
        "SINAL_NIVEL_JUSANTE_FALHA_LEITURA":                                            [12341, 1],

        ## STT_ALARMES_HH_ANALOGICAS
        "UHRV_PRESSAO_OLEO_MUITO_ALTA":                                                 [12343, 0],
        "SINAL_NIVEL_JUSANTE_MUITO_ALTA":                                               [12343, 1],

        ## STT_ALARMES_H_ANALOGICAS
        "UHRV_PRESSAO_OLEO_ALTA":                                                       [12345, 0],
        "SINAL_NIVEL_JUSANTE_ALTA":                                                     [12345, 1],

        ## STT_ALARMES_L_ANALOGICAS
        "UHRV_PRESSAO_OLEO_BAIXA":                                                      [12347, 0],
        "SINAL_NIVEL_JUSANTE_BAIXA":                                                    [12347, 1],

        ## STT_ALARMES_LL_ANALOGICAS
        "UHRV_PRESSAO_OLEO_MUITO_BAIXA":                                                [12349, 0],
        "SINAL_NIVEL_JUSANTE_MUITO_BAIXA":                                              [12349, 1],

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
        "BLOQUEIO_86E_ATUADO":                                                          [12340, 15],

        ## BLOQUEIO_86H
        "BLOQUEIO_86H_ATUADO":                                                          [12342, 15],

        ## STT_BORBOLETA
        "BORBOLETA_FALHA_ABRIR":                                                        [12365, 0],
        "BORBOLETA_FALHA_FECHAR":                                                       [12365, 1],
        "BORBOLETA_ABRINDO":                                                            [12365, 2],
        "BORBOLETA_FECHANDO":                                                           [12365, 3],
        "BYPASS_ABRINDO":                                                               [12365, 4],
        "BYPASS_FECHANDO":                                                              [12365, 5],
        "BYPASS_FALHA_ABRIR":                                                           [12365, 6],
        "BYPASS_FALHA_FECHAR":                                                          [12365, 7],
        "BORBOLETA_DISCREPANCIA_SENSORES":                                              [12365, 10],
        "BYPASS_DISCREPANCIA_SENSORES":                                                 [12365, 11],

        ## SST_ENTRADAS_DIGITAIS_1
        "BOTAO_BLOQUEIO_86EH":                                                          [12309, 0],
        "REARME_FALHAS":                                                                [12309, 1],
        "BOTAO_PARA_UG":                                                                [12309, 2],
        "BOTAO_PARTE_UG":                                                               [12309, 3],
        "BOTAO_DIMINUI_REFERENCIA_RV":                                                  [12309, 4],
        "BOTAO_AUMENTA_REFERENCIA_RV":                                                  [12309, 5],
        "BOTAO_DIMINUI_REFERENCIA_RT":                                                  [12309, 6],
        "BOTAO_AUMENTA_REFERENCIA_RT":                                                  [12309, 7],
        "RELE_PROT_GERADOR_TRIP":                                                       [12309, 8],
        "RELE_PROT_GERADOR_50BF":                                                       [12309, 10],
        "RV_TRIP":                                                                      [12309, 11],
        "RV_ALARME":                                                                    [12309, 12],
        "RV_HABILITADO":                                                                [12309, 13],
        "RV_REGULANDO":                                                                 [12309, 14],
        "RV_POTENCIA_NULA":                                                             [12309, 15],

        "PRTVA_RV_MAQUINA_PARADA":                                                      [12310, 0],
        "PRTVA_RV_VELOCIDADE_MENOR":                                                    [12310, 1],
        "PRTVA_RV_VELOCIDADE_MAIOR":                                                    [12310, 2],
        "PRTVA_RV_DISTRIBUIDOR_ABERTO":                                                 [12310, 3],
        "PRTVA_RT_TRIP":                                                                [12310, 4],
        "PRTVA_RT_ALARME":                                                              [12310, 5],
        "PRTVA_RT_HABILITADO":                                                          [12310, 6],
        "PRTVA_RT_REGULANDO":                                                           [12310, 7],
        "PRTVA_CONTATOR_DE_COMPO_FECHADO":                                              [12310, 8],
        "PRTVA_DISJUNTOR_DE_MAQUINA_FECHADO":                                           [12310, 9],
        "PRTVA_RELE_BLOQUEIO_86EH":                                                     [12310, 10],
        "PRTVA_SUPERVISAO_DE_TENSAO_ENTRADA_CA":                                        [12310, 11],
        "PRTVA_DISPOSITIVO_PROTECAO_DE_SURTO":                                          [12310, 12],
        "PRTVA_UHRV_BOMBA_DEFEITO":                                                     [12310, 13],
        "PRTVA_UHRV_BOMBA_LIGADA":                                                      [12310, 14],
        "PRTVA_UHLM_BOMBA_DEFEITO":                                                     [12310, 15],

        ## SST_ENTRADAS_DIGITAIS_2
        "UHLM_BOMBA_LIGADA":                                                            [12311, 0],
        "UG_RESISTENCIA_AQUEC_GERADOR_DEFEITO":                                         [12311, 3],
        "UG_RESISTENCIA_AQUEC_GERADOR_LIGADA":                                          [12311, 4],
        "DISJUNTOR_TPS_PROTECAO":                                                       [12311, 5],
        "UHRV_OLEO_NIVEL_MUITO_BAIXO":                                                  [12311, 6],
        "UHRV_FILTRO_OLEO_SUJO":                                                        [12311, 7],
        "UHRV_PRESSAO_CRITICA":                                                         [12311, 8],
        "UHRV_PRESSAO_FREIO":                                                           [12311, 9],
        "UHLM_OLEO_NIVEL_MUITO_ALTO":                                                   [12311, 11],
        "UHLM_OLEO_NIVEL_MUITO_BAIXO":                                                  [12311, 12],
        "UHLM_PRESSAO_LINHA_LUBRIFICACAO":                                              [12311, 13],
        "UHLM_FILTRO_OLEO_SUJO":                                                        [12311, 14],
        "UHLM_FLUXO_TROCADOR_DE_CALOR":                                                 [12311, 15],

        "QBAG_ESCOVA_POLO_POSITIVO_DESGASTADA":                                         [12312, 1],
        "QBAG_ESCOVA_POLO_NEGATICO_DESGASTADA":                                         [12312, 2],
        "PSA_BLOQUEIO_86BTBF":                                                          [12312, 3],
        "PSA_POCO_DRENAGEM_NIVEL_MUITO_ALTO":                                           [12312, 4],
        "PSA_FILTRAGEM_PRESSAO_SAIDA":                                                  [12312, 5],
        "PSA_DISJUNTOR_LINHA_FECHADO":                                                  [12312, 6],
        "TPs_PROTECAO_59N_ABERTO":                                                      [12312, 9],
        "VB_VALVULA_BORBOLETA_ABERTA":                                                  [12312, 12],
        "VB_VALVULA_BORBOLETA_FECHADA":                                                 [12312, 13],
        "VB_VALVULA_BYPASS_ABERTA":                                                     [12312, 14],
        "VB_VALVULA_BYPASS_FECHADA":                                                    [12312, 15],

        ## PARTIDA_PARADA
        "STT_PARTIDA_PARADA":                                                           12388,
        "SST_PASSO_SELECIONADO":                                                        12390,
        "STT_PASSO_ATUAL":                                                              12392,

        ## PERMISSIVOS
        "STT_PRE_CONDICOES_GIRO_MECANICO":                                              12408,
        "STT_PRE_CONDICOES_EXCITCAO":                                                   12410,
        "STT_PRE_CONDICOES_SINCRONISMO":                                                12412,

        ## STT_RT
        "RT_FALHA_AO_HABILITAR":                                                        [12375, 0],
        "RT_FALHA_AO_PARTIR":                                                           [12375, 1],
        "RT_FALHA_AO_DESABILITAR":                                                      [12375, 2],

        ## STT_RV
        "RV_FALHA_AO_HABILITAR":                                                        [12371, 0],
        "RV_FALHA_AO_PARTIR":                                                           [12371, 1],
        "RV_FALHA_AO_DESABILITAR":                                                      [12371, 2],
        "RV_FALHA_AO_PARAR_MAQUINA":                                                    [12371, 3],
        "RV_FALHA_AO_FECHAR_DISTRIBUIDOR":                                              [12371, 4],
        "RV_MODO_MANUTENCAO":                                                           [12371, 5],

        ## STT_UNIDADE_GERADORA
        "CONTROLE_POTENCIA_POR_NIVEL_HABILITADO":                                       [12361, 0],
        "CONTROLE_DE_NIVEL_HABILITADO":                                                 [12361, 1],
        "CONTROLE_POTENCIA_MANUAL_HABILITADO":                                          [12361, 2],
        "CONTROLE_PARADA_POR_NIVEL_HABILITADO":                                         [12361, 3],
        "CONTROLE_PARADA_NIVEL_BAIXO":                                                  [12361, 4],
        "CONTROLE_FALHA_SENSOR_NIVEL":                                                  [12361, 5],
        "CONTROLE_ALARME_DIFERENCIAL_DE_GRADE":                                         [12361, 6],
        "CONTROLE_TRIP_DIFERENCIAL_DE_GRADE":                                           [12361, 7],
        "RESISTENCIA_AQUECIMENTO_GERADOR_INDISPONIVEL":                                 [12361, 8],
        "RESISTENCIA_AQUECIMENTO_GERADOR_FALHA_LIGAR":                                  [12361, 9],
        "RESISTENCIA_AQUECIMENTO_GERADOR_FALHA_DESLIGAR":                               [12361, 10],
        "FREIO_FALHA_AO_APLICAR_OU_DESAPLICAR":                                         [12361, 11],

        ## STT_UHLM
        "UNIDADE_MANUTENCAO":                                                           [12365, 0],
        "BOMBA_1_INDISPONIVEL":                                                         [12365, 2],
        "BOMBA_2_INDISPONIVEL":                                                         [12365, 3],
        "BOMBA_1_PRINCIPAL":                                                            [12365, 4],
        "BOMBA_2_PRINCIPAL":                                                            [12365, 5],
        "BOMBA_1_FALHA_AO_LIGAR":                                                       [12365, 6],
        "BOMBA_1_FALHA_AO_DESLIGAR":                                                    [12365, 7],
        "BOMBA_2_FALHA_AO_LIGAR":                                                       [12365, 8],
        "BOMBA_2_FALHA_AO_DESLIGAR":                                                    [12365, 9],
        "BOMBA_1_FALHA_AO_PRESSURIZAR":                                                 [12365, 10],
        "BOMBA_2_FALHA_AO_PRESSURIZAR":                                                 [12365, 11],
        "FILTRO_OLEO_SUJO":                                                             [12365, 13],
        "FALHA_PRESSOSTATO":                                                            [12365, 14],

        ## STT_UHRV
        "UNIDADE_MANUTENCAO":                                                           [12361, 0],
        "UNIDADE_HABILITADA":                                                           [12361, 1],
        "BOMBA_1_INDISPONIVEL":                                                         [12361, 2],
        "BOMBA_2_INDISPONIVEL":                                                         [12361, 3],
        "BOMBA_1_PRINCIPAL":                                                            [12361, 4],
        "BOMBA_2_PRINCIPAL":                                                            [12361, 5],
        "BOMBA_1_FALHA_AO_LIGAR":                                                       [12361, 6],
        "BOMBA_1_FALHA_AO_DESLIGAR":                                                    [12361, 7],
        "BOMBA_2_FALHA_AO_LIGAR":                                                       [12361, 8],
        "BOMBA_2_FALHA_AO_DESLIGAR":                                                    [12361, 9],
        "BOMBA_1_FALHA_AO_PRESSURIZAR":                                                 [12361, 10],
        "BOMBA_2_FALHA_AO_PRESSURIZAR":                                                 [12361, 11],
        "FILTRO_OLEO_SUJO":                                                             [12361, 13],
    },

    "UG2": {
        ### COMANDOS
        ## CMD_UG2
        "REARME_FALHAS":                                                                [12289, 0],
        "COMANDO_PARADA_DE_EMERGENCIA":                                                 [12289, 1],
        "CONTROLE_NIVEL":                                                               [12289, 2],
        "CONTROLE_POTENCIA_MANUAL":                                                     [12289, 3],
        "CONTROLE_POTENCIA_POR_NIVEL":                                                  [12289, 4],
        "PARADA_NIVEL_HABILITA":                                                        [12289, 5],
        "PARADA_NIVEL_DESABILITA":                                                      [12289, 6],
        "RV_MANUTENCAO":                                                                [12289, 10],
        "RV_AUTOMATICO":                                                                [12289, 11],

        ## CMD_UHRV
        "MODO_AUTOMATICO":                                                              [12291, 0],
        "MODO_MANUTENCAO":                                                              [12291, 1],
        "BOMBA_1_LIGA":                                                                 [12291, 2],
        "BOMBA_1_DESLIGA":                                                              [12291, 3],
        "BOMBA_2_LIGA":                                                                 [12291, 4],
        "BOMBA_2_DESLIGA":                                                              [12291, 5],
        "BOMBA_1_PRINCIPAL":                                                            [12291, 6],
        "BOMBA_2_PRINCIPAL":                                                            [12291, 7],

        ## CMD_UHLM
        "MODO_AUTOMATICO":                                                              [12293, 0],
        "MODO_MANUTENCAO":                                                              [12293, 1],
        "BOMBA_1_LIGA":                                                                 [12293, 2],
        "BOMBA_1_DESLIGA":                                                              [12293, 3],

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
        "TIRISTORES_TEMPERATURA_FALHA_LEITURA":                                         [12329, 0],
        "CROWBAR_TEMPERATURA_FALHA_LEITURA":                                            [12329, 1],
        "TRAFO_EXCITACAO_TEMPERATURA_FALHA_LEITURA":                                    [12329, 2],
        "UHRV_TEMPERATURA_OLEO_FALHA_LEITURA":                                          [12329, 3],
        "UHLM_TEMPERATURA_OLEO_FALHA_LEITURA":                                          [12329, 4],
        "GERADOR_FASE_A_TEMPERATURA_FALHA_LEITURA":                                     [12329, 7],
        "GERADOR_FASE_B_TEMPERATURA_FALHA_LEITURA":                                     [12329, 8],
        "GERADOR_FASE_C_TEMPERATURA_FALHA_LEITURA":                                     [12329, 9],
        "GERADOR_NUCLEO_1_TEMPERATURA_FALHA_LEITURA":                                   [12329, 10],
        "GERADOR_NUCLEO_2_TEMPERATURA_FALHA_LEITURA":                                   [12329, 11],
        "GERADOR_NUCLEO_3_TEMPERATURA_FALHA_LEITURA":                                   [12329, 12],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_FALHA_LEITURA":                              [12329, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMPERATURA_FALHA_LEITURA":                         [12329, 14],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_FALHA_LEITURA":                            [12329, 15],

        ## STT_ALARMES_HH_TEMPERATURA
        "TIRISTORES_TEMPERATURA_MUITO_ALTA":                                            [12331, 0],
        "CROWBAR_TEMPERATURA_MUITO_ALTA":                                               [12331, 1],
        "TRAFO_EXCITACAO_TEMPERATURA_MUITO_ALTA":                                       [12331, 2],
        "UHRV_TEMPERATURA_OLEO_MUITO_ALTA":                                             [12331, 3],
        "UHLM_TEMPERATURA_OLEO_MUITO_ALTA":                                             [12331, 4],
        "GERADOR_FASE_A_TEMPERATURA_MUITO_ALTA":                                        [12331, 7],
        "GERADOR_FASE_B_TEMPERATURA_MUITO_ALTA":                                        [12331, 8],
        "GERADOR_FASE_C_TEMPERATURA_MUITO_ALTA":                                        [12331, 9],
        "GERADOR_NUCLEO_1_TEMPERATURA_MUITO_ALTA":                                      [12331, 10],
        "GERADOR_NUCLEO_2_TEMPERATURA_MUITO_ALTA":                                      [12331, 11],
        "GERADOR_NUCLEO_3_TEMPERATURA_MUITO_ALTA":                                      [12331, 12],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_MUITO_ALTA":                                 [12331, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMPERATURA_MUITO_ALTA":                            [12331, 14],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_MUITO_ALTA":                               [12331, 15],

        ## STT_ALARMES_H_TEMPERATURA
        "TIRISTORES_TEMPERATURA_ALTA":                                                  [12333, 0],
        "CROWBAR_TEMPERATURA_ALTA":                                                     [12333, 1],
        "TRAFO_EXCITACAO_TEMPERATURA_ALTA":                                             [12333, 2],
        "UHRV_TEMPERATURA_OLEO_ALTA":                                                   [12333, 3],
        "UHLM_TEMPERATURA_OLEO_ALTA":                                                   [12333, 4],
        "GERADOR_FASE_A_TEMPERATURA_ALTA":                                              [12333, 7],
        "GERADOR_FASE_B_TEMPERATURA_ALTA":                                              [12333, 8],
        "GERADOR_FASE_C_TEMPERATURA_ALTA":                                              [12333, 9],
        "GERADOR_NUCLEO_1_TEMPERATURA_ALTA":                                            [12333, 10],
        "GERADOR_NUCLEO_2_TEMPERATURA_ALTA":                                            [12333, 11],
        "GERADOR_NUCLEO_3_TEMPERATURA_ALTA":                                            [12333, 12],
        "MANCAL_GUIA_CASQUILHO_TEMPERATURA_ALTA":                                       [12333, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMPERATURA_ALTA":                                  [12333, 14],
        "MANCAL_COMBINADO_ESCORA_TEMPERATURA_ALTA":                                     [12333, 15],

        ## STT_FALHAS_ANALOGICAS
        "UHRV_PRESSAO_OLEO_FALHA_LEITURA":                                              [12341, 0],
        "SINAL_NIVEL_JUSANTE_FALHA_LEITURA":                                            [12341, 1],

        ## STT_ALARMES_HH_ANALOGICAS
        "UHRV_PRESSAO_OLEO_MUITO_ALTA":                                                 [12343, 0],
        "SINAL_NIVEL_JUSANTE_MUITO_ALTA":                                               [12343, 1],

        ## STT_ALARMES_H_ANALOGICAS
        "UHRV_PRESSAO_OLEO_ALTA":                                                       [12345, 0],
        "SINAL_NIVEL_JUSANTE_ALTA":                                                     [12345, 1],

        ## STT_ALARMES_L_ANALOGICAS
        "UHRV_PRESSAO_OLEO_BAIXA":                                                      [12347, 0],
        "SINAL_NIVEL_JUSANTE_BAIXA":                                                    [12347, 1],

        ## STT_ALARMES_LL_ANALOGICAS
        "UHRV_PRESSAO_OLEO_MUITO_BAIXA":                                                [12349, 0],
        "SINAL_NIVEL_JUSANTE_MUITO_BAIXA":                                              [12349, 1],

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
        "BLOQUEIO_86E_ATUADO":                                                          [12340, 15],

        ## BLOQUEIO_86H
        "BLOQUEIO_86H_ATUADO":                                                          [12342, 15],

        ## STT_BORBOLETA
        "BORBOLETA_FALHA_ABRIR":                                                        [12365, 0],
        "BORBOLETA_FALHA_FECHAR":                                                       [12365, 1],
        "BORBOLETA_ABRINDO":                                                            [12365, 2],
        "BORBOLETA_FECHANDO":                                                           [12365, 3],
        "BYPASS_ABRINDO":                                                               [12365, 4],
        "BYPASS_FECHANDO":                                                              [12365, 5],
        "BYPASS_FALHA_ABRIR":                                                           [12365, 6],
        "BYPASS_FALHA_FECHAR":                                                          [12365, 7],
        "BORBOLETA_DISCREPANCIA_SENSORES":                                              [12365, 10],
        "BYPASS_DISCREPANCIA_SENSORES":                                                 [12365, 11],

        ## SST_ENTRADAS_DIGITAIS_1
        "BOTAO_BLOQUEIO_86EH":                                                          [12309, 0],
        "REARME_FALHAS":                                                                [12309, 1],
        "BOTAO_PARA_UG":                                                                [12309, 2],
        "BOTAO_PARTE_UG":                                                               [12309, 3],
        "BOTAO_DIMINUI_REFERENCIA_RV":                                                  [12309, 4],
        "BOTAO_AUMENTA_REFERENCIA_RV":                                                  [12309, 5],
        "BOTAO_DIMINUI_REFERENCIA_RT":                                                  [12309, 6],
        "BOTAO_AUMENTA_REFERENCIA_RT":                                                  [12309, 7],
        "RELE_PROT_GERADOR_TRIP":                                                       [12309, 8],
        "RELE_PROT_GERADOR_50BF":                                                       [12309, 10],
        "RV_TRIP":                                                                      [12309, 11],
        "RV_ALARME":                                                                    [12309, 12],
        "RV_HABILITADO":                                                                [12309, 13],
        "RV_REGULANDO":                                                                 [12309, 14],
        "RV_POTENCIA_NULA":                                                             [12309, 15],

        "PRTVA_RV_MAQUINA_PARADA":                                                      [12310, 0],
        "PRTVA_RV_VELOCIDADE_MENOR":                                                    [12310, 1],
        "PRTVA_RV_VELOCIDADE_MAIOR":                                                    [12310, 2],
        "PRTVA_RV_DISTRIBUIDOR_ABERTO":                                                 [12310, 3],
        "PRTVA_RT_TRIP":                                                                [12310, 4],
        "PRTVA_RT_ALARME":                                                              [12310, 5],
        "PRTVA_RT_HABILITADO":                                                          [12310, 6],
        "PRTVA_RT_REGULANDO":                                                           [12310, 7],
        "PRTVA_CONTATOR_DE_COMPO_FECHADO":                                              [12310, 8],
        "PRTVA_DISJUNTOR_DE_MAQUINA_FECHADO":                                           [12310, 9],
        "PRTVA_RELE_BLOQUEIO_86EH":                                                     [12310, 10],
        "PRTVA_SUPERVISAO_DE_TENSAO_ENTRADA_CA":                                        [12310, 11],
        "PRTVA_DISPOSITIVO_PROTECAO_DE_SURTO":                                          [12310, 12],
        "PRTVA_UHRV_BOMBA_DEFEITO":                                                     [12310, 13],
        "PRTVA_UHRV_BOMBA_LIGADA":                                                      [12310, 14],
        "PRTVA_UHLM_BOMBA_DEFEITO":                                                     [12310, 15],

        ## SST_ENTRADAS_DIGITAIS_2
        "UHLM_BOMBA_LIGADA":                                                            [12311, 0],
        "UG_RESISTENCIA_AQUEC_GERADOR_DEFEITO":                                         [12311, 3],
        "UG_RESISTENCIA_AQUEC_GERADOR_LIGADA":                                          [12311, 4],
        "DISJUNTOR_TPS_PROTECAO":                                                       [12311, 5],
        "UHRV_OLEO_NIVEL_MUITO_BAIXO":                                                  [12311, 6],
        "UHRV_FILTRO_OLEO_SUJO":                                                        [12311, 7],
        "UHRV_PRESSAO_CRITICA":                                                         [12311, 8],
        "UHRV_PRESSAO_FREIO":                                                           [12311, 9],
        "UHLM_OLEO_NIVEL_MUITO_ALTO":                                                   [12311, 11],
        "UHLM_OLEO_NIVEL_MUITO_BAIXO":                                                  [12311, 12],
        "UHLM_PRESSAO_LINHA_LUBRIFICACAO":                                              [12311, 13],
        "UHLM_FILTRO_OLEO_SUJO":                                                        [12311, 14],
        "UHLM_FLUXO_TROCADOR_DE_CALOR":                                                 [12311, 15],

        "QBAG_ESCOVA_POLO_POSITIVO_DESGASTADA":                                         [12312, 1],
        "QBAG_ESCOVA_POLO_NEGATICO_DESGASTADA":                                         [12312, 2],
        "PSA_BLOQUEIO_86BTBF":                                                          [12312, 3],
        "PSA_POCO_DRENAGEM_NIVEL_MUITO_ALTO":                                           [12312, 4],
        "PSA_FILTRAGEM_PRESSAO_SAIDA":                                                  [12312, 5],
        "PSA_DISJUNTOR_LINHA_FECHADO":                                                  [12312, 6],
        "TPs_PROTECAO_59N_ABERTO":                                                      [12312, 9],
        "VB_VALVULA_BORBOLETA_ABERTA":                                                  [12312, 12],
        "VB_VALVULA_BORBOLETA_FECHADA":                                                 [12312, 13],
        "VB_VALVULA_BYPASS_ABERTA":                                                     [12312, 14],
        "VB_VALVULA_BYPASS_FECHADA":                                                    [12312, 15],

        ## PARTIDA_PARADA
        "STT_PARTIDA_PARADA":                                                           12388,
        "SST_PASSO_SELECIONADO":                                                        12390,
        "STT_PASSO_ATUAL":                                                              12392,

        ## PERMISSIVOS
        "STT_PRE_CONDICOES_GIRO_MECANICO":                                              12408,
        "STT_PRE_CONDICOES_EXCITCAO":                                                   12410,
        "STT_PRE_CONDICOES_SINCRONISMO":                                                12412,

        ## STT_RT
        "RT_FALHA_AO_HABILITAR":                                                        [12375, 0],
        "RT_FALHA_AO_PARTIR":                                                           [12375, 1],
        "RT_FALHA_AO_DESABILITAR":                                                      [12375, 2],

        ## STT_RV
        "RV_FALHA_AO_HABILITAR":                                                        [12371, 0],
        "RV_FALHA_AO_PARTIR":                                                           [12371, 1],
        "RV_FALHA_AO_DESABILITAR":                                                      [12371, 2],
        "RV_FALHA_AO_PARAR_MAQUINA":                                                    [12371, 3],
        "RV_FALHA_AO_FECHAR_DISTRIBUIDOR":                                              [12371, 4],
        "RV_MODO_MANUTENCAO":                                                           [12371, 5],

        ## STT_UNIDADE_GERADORA
        "CONTROLE_POTENCIA_POR_NIVEL_HABILITADO":                                       [12361, 0],
        "CONTROLE_DE_NIVEL_HABILITADO":                                                 [12361, 1],
        "CONTROLE_POTENCIA_MANUAL_HABILITADO":                                          [12361, 2],
        "CONTROLE_PARADA_POR_NIVEL_HABILITADO":                                         [12361, 3],
        "CONTROLE_PARADA_NIVEL_BAIXO":                                                  [12361, 4],
        "CONTROLE_FALHA_SENSOR_NIVEL":                                                  [12361, 5],
        "CONTROLE_ALARME_DIFERENCIAL_DE_GRADE":                                         [12361, 6],
        "CONTROLE_TRIP_DIFERENCIAL_DE_GRADE":                                           [12361, 7],
        "RESISTENCIA_AQUECIMENTO_GERADOR_INDISPONIVEL":                                 [12361, 8],
        "RESISTENCIA_AQUECIMENTO_GERADOR_FALHA_LIGAR":                                  [12361, 9],
        "RESISTENCIA_AQUECIMENTO_GERADOR_FALHA_DESLIGAR":                               [12361, 10],
        "FREIO_FALHA_AO_APLICAR_OU_DESAPLICAR":                                         [12361, 11],

        ## STT_UHLM
        "UNIDADE_MANUTENCAO":                                                           [12365, 0],
        "BOMBA_1_INDISPONIVEL":                                                         [12365, 2],
        "BOMBA_2_INDISPONIVEL":                                                         [12365, 3],
        "BOMBA_1_PRINCIPAL":                                                            [12365, 4],
        "BOMBA_2_PRINCIPAL":                                                            [12365, 5],
        "BOMBA_1_FALHA_AO_LIGAR":                                                       [12365, 6],
        "BOMBA_1_FALHA_AO_DESLIGAR":                                                    [12365, 7],
        "BOMBA_2_FALHA_AO_LIGAR":                                                       [12365, 8],
        "BOMBA_2_FALHA_AO_DESLIGAR":                                                    [12365, 9],
        "BOMBA_1_FALHA_AO_PRESSURIZAR":                                                 [12365, 10],
        "BOMBA_2_FALHA_AO_PRESSURIZAR":                                                 [12365, 11],
        "FILTRO_OLEO_SUJO":                                                             [12365, 13],
        "FALHA_PRESSOSTATO":                                                            [12365, 14],

        ## STT_UHRV
        "UNIDADE_MANUTENCAO":                                                           [12361, 0],
        "UNIDADE_HABILITADA":                                                           [12361, 1],
        "BOMBA_1_INDISPONIVEL":                                                         [12361, 2],
        "BOMBA_2_INDISPONIVEL":                                                         [12361, 3],
        "BOMBA_1_PRINCIPAL":                                                            [12361, 4],
        "BOMBA_2_PRINCIPAL":                                                            [12361, 5],
        "BOMBA_1_FALHA_AO_LIGAR":                                                       [12361, 6],
        "BOMBA_1_FALHA_AO_DESLIGAR":                                                    [12361, 7],
        "BOMBA_2_FALHA_AO_LIGAR":                                                       [12361, 8],
        "BOMBA_2_FALHA_AO_DESLIGAR":                                                    [12361, 9],
        "BOMBA_1_FALHA_AO_PRESSURIZAR":                                                 [12361, 10],
        "BOMBA_2_FALHA_AO_PRESSURIZAR":                                                 [12361, 11],
        "FILTRO_OLEO_SUJO":                                                             [12361, 13],
    }
}

REG_RTV = {
    ### RV
    ## LEITURAS_1
    "ROTACAO":                                                                          16,
    "ESTADO_OPERACAO":                                                                  21,
    "CONTROLE_SINCRONIZADO_SELECIONADO":                                                22,
    "CONTROLE_VAZIO_SELECIONADO":                                                       23,
    "COMANDO_MODBUS":                                                                   24,

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
    "SETPOINT_ABERTURA_PU":                                                             28,
    "SETPOINT_VELOCIDADE":                                                              29,
    "SETPOINT_POTENCIA_ATIVA_KW":                                                       30,
    "SETPOINT_POTENCIA_ATIVA_PU":                                                       30,
    "SAIDA_CONTROLE_DISTRIBUIDOR":                                                      32,
    "SAIDA_CONTROLE_ROTOR":                                                             33,
    "REFERENCIA_DISTRIBUIDOR_PU":                                                       36,
    "FEEDBACK_DISTRIBUIDOR_PU":                                                         37,
    "SAIDA_CONTROLE_DISTRIBUIDOR_PU":                                                   32,
    "REFERENCIA_ROTOR_PU":                                                              42,
    "FEEDBACK_ROTOR_PU":                                                                43,
    "SAIDA_CONTROLE_ROTOR_PU":                                                          33,
    "REFERENCIA_VELOCIDADE_PU":                                                         48,
    "FEEDBACK_VELOCIDADE_PU":                                                           49,
    "REFERENCIA_POTENCIA_ATIVA_PU":                                                     54,
    "FEEDBACK_POTENCIA_ATIVA_PU":                                                       55,

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
    "POTENCIA_APARENTE_NOMINAL":                                                        79,
    "POTENCIA_ATIVA_NOMINAL":                                                           80,
    "CONTROLE_1":                                                                       85,
    "CONTROLE_2":                                                                       86,
    "CONJUGADO_DISTRIBUIDOR_1":                                                         121,
    "CONJUGADO_ROTOR_1":                                                                122,
    "CONJUGADO_DISTRIBUIDOR_2":                                                         123,
    "CONJUGADO_ROTOR_2":                                                                124,
    "CONJUGADO_DISTRIBUIDOR_3":                                                         125,
    "CONJUGADO_ROTOR_3":                                                                126,
    "CONJUGADO_DISTRIBUIDOR_4":                                                         127,
    "CONJUGADO_ROTOR_4":                                                                128,
    "CONJUGADO_DISTRIBUIDOR_5":                                                         129,
    "CONJUGADO_ROTOR_5":                                                                130,
    "CONJUGADO_DISTRIBUIDOR_6":                                                         131,
    "CONJUGADO_ROTOR_6":                                                                132,
    "CONJUGADO_DISTRIBUIDOR_7":                                                         133,
    "CONJUGADO_ROTOR_7":                                                                134,
    "CONJUGADO_DISTRIBUIDOR_8":                                                         135,
    "CONJUGADO_ROTOR_8":                                                                136,
    "CONJUGADO_DISTRIBUIDOR_9":                                                         137,
    "CONJUGADO_ROTOR_9":                                                                138,
    "CONJUGADO_DISTRIBUIDOR_10":                                                        139,
    "CONJUGADO_ROTOR_10":                                                               140,
    "ABERTURA_MAXIMA_DISTRIBUIDOR":                                                     182,
    "ABERTURA_MAXIMA_DISTRIBUIDOR_A_VAZIO":                                             184,
    "ABERTURA_MINIMA_DISTRIBUIDOR":                                                     183,
    "ABERTURA_MAXIMA_ROTOR":                                                            185,
    "ABERTURA_MINIMA_ROTOR":                                                            186,
    "POTENCIA_MAXIMA":                                                                  189,
    "POTENCIA_MINIMA":                                                                  190,


    ### RT
    ## LEITURAS_1
    "CORRENTE_EXCITACAO":                                                               16,
    "TENSAO_EXCITACAO":                                                                 17,
    "TEMPERATURA_ROTOR":                                                                25,
    "ESTADO_OPERACAO":                                                                  26,
    "CONTROLE_SINCRONIZADO_SELECIONADO":                                                27,

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
    "SETPOINT_TENSAO_PU":                                                               40,
    "SETPOINT_POTENCIA_REATIVA_KVAR":                                                   41,
    "SETPOINT_POTENCIA_REATIVA_PU":                                                     41,
    "SETPOINT_FATOR_POTENCIA_PU":                                                       42,
    "ABERTURA_PONTE":                                                                   43,
    "REFERENCIA_CORRENTE_CAMPO_PU":                                                     46,
    "FEEDBACK_CORRENTE_CAMPO_PU":                                                       47,
    "REFERENCIA_TENSAO_PU":                                                             52,
    "FEEDBACK_TENSAO_PU":                                                               53,
    "REFERENCIA_POTENCIA_REATIVA_PU":                                                   58,
    "FEEDBACK_POTENCIA_REATIVA_PU":                                                     59,
    "REFERENCIA_FATOR_POTENCIA_PU":                                                     64,
    "FEEDBACK_FATOR_POTENCIA_PU":                                                       65,

    ## ALARMES_1
    "RT_ALARME_SOBRETENSAO":                                                            [70, 0],
    "RT_ALARME_SUBTENSAO":                                                              [70, 1],
    "RT_ALARME_SOBREFREQUENCIA":                                                        [70, 2],
    "RT_ALARME_SUBFREQUENCIA":                                                          [70, 3],
    "RT_ALARME_LIMITE_SUPERIOR_POTENCIA_REATIVA_":                                      [70, 4],
    "RT_ALARME_LIMITE_INFERIOR_POTENCIA_REATIVA_":                                      [70, 5],
    "RT_ALARME_LIMITE_SUPERIOR_FATOR_DE_POTENCIA_":                                     [70, 6],
    "RT_ALARME_LIMITE_INFERIOR_FATOR_DE_POTENCIA_":                                     [70, 7],
    "RT_ALARME_VARIACAO_DE_TENSAO":                                                     [70, 8],
    "RT_ALARME_POTENCIA_ATIVA_REVERSA":                                                 [70, 9],
    "RT_ALARME_SOBRECORRENTE_TERMINAL":                                                 [70, 10],
    "RT_ALARME_LIMITE_SUPERIOR_CORRENTE_EXCITACAO_":                                    [70, 11],
    "RT_ALARME_LIMITE_INFERIOR_CORRENTE_EXCITACAO_":                                    [70, 12],
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
    "TENSAO_NOMINAL":                                                                   85,
    "POTENCIA_APARENTE_NOMINAL":                                                        86,
    "CONTROLE_1":                                                                       90,
    "CONTROLE_2":                                                                       91,

}