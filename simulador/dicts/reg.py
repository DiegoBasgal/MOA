# MAPA NOVO

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
        "IA":                                                                           320,        # Input Register                        (OP -> Read Input Registers - 3x)
        "IB":                                                                           322,        # Input Register                        (OP -> Read Input Registers - 3x)
        "IC":                                                                           324,        # Input Register                        (OP -> Read Input Registers - 3x)
        "VAB":                                                                          330 + 1000,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "VBC":                                                                          332 + 1000,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "VCA":                                                                          334 + 1000,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "P":                                                                            353 + 1000,        # Input Register                        (OP -> Read Input Registers - 3x)
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
        "VBC":                                                                          332 + 10000,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "VCA":                                                                          334 + 10000,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "P":                                                                            353 + 10000,        # Input Register                        (OP -> Read Input Registers - 3x)
        "Q":                                                                            361 + 10000,        # Input Register                        (OP -> Read Input Registers - 3x)
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
        "VAB":                                                                          330 + 20000,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "VBC":                                                                          332 + 20000,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "VCA":                                                                          334 + 20000,        # Input Register Scale 0.1              (OP -> Read Input Registers - 3x)
        "P":                                                                            353 + 20000,        # Input Register                        (OP -> Read Input Registers - 3x)
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
    # Rearme
    "CMD_REARME_FALHAS":                                                                [12289 + 1000, 0],

    # Poço Drenagem
    "CMD_PD_BOMBA_1_PRINC":                                                             [12289, 1],
    "CMD_PD_BOMBA_2_PRINC":                                                             [12289, 2],

    # Disjuntores
    "CMD_DJ_TSA_ABRE":                                                                  [12289, 13],
    "CMD_DJ_TSA_FECHA":                                                                 [12289, 14],
    "CMD_DJ_GMG_ABRE":                                                                  [12289, 15],
    "CMD_DJ_GMG_FECHA":                                                                 [12288, 0],
    "CMD_DJ_LINHA_FECHA":                                                               [12288 + 1000, 1],
    "CMD_DJ_LINHA_ABRE":                                                                [12288 + 1000, 2],

    # Sistema Filtragem
    "CMD_SFA_COMUTA_ELEM":                                                              [12288, 3],
    "CMD_SFA_AUTOMATICO":                                                               [12288, 4],
    "CMD_SFA_MANUAL":                                                                   [12288, 5],
    "CMD_SFB_MANUAL":                                                                   [12288, 8],
    "CMD_SFB_AUTOMATICO":                                                               [12288, 9],
    "CMD_SFB_COMUTA_ELEM":                                                              [12288, 10],



    ### STATUS
    ## SST_ENTRAS_DIGITAIS_0
    # Botão
    "BT_REARME_FALHAS_PSA":                                                             [12309, 0],
    "BT_BLOQ_86BTBF":                                                                   [12309, 1],

    # Poço Drenagem
    "PD_BOMBA_1_AUTOMATICO":                                                            [12309, 2],
    "PD_BOMBA_2_ATUTOMATICO":                                                           [12309, 3],
    "PD_BOMBA_1_DEFEITO":                                                               [12309, 13],
    "PD_BOMBA_1_LIGADA":                                                                [12309, 14],
    "PD_BOMBA_2_DEFEITO":                                                               [12309, 15],
    "PD_BOMBA_2_LIGADA":                                                                [12308, 0],
    "PD_SENS_NV_MUITO_BAIXO":                                                           [12308, 5],
    "PD_SENS_NV_DESLIGA_BOMBAS":                                                        [12308, 6],
    "PD_SENS_NV_LIGA_BOMBA":                                                            [12308, 7],
    "PD_SENS_NV_ALTO":                                                                  [12308, 8],
    "PD_SENS_NV_MUITO_ALTO":                                                            [12308, 9],

    # Disjuntores
    "DJS_MODO_REMOTO":                                                                  [12309, 4],
    "DJ_TSA_TRIP":                                                                      [12309, 5],
    "DJ_GMG_TRIP":                                                                      [12309, 6],
    "DJ_TSA_FECHADO":                                                                   [12308, 10],
    "DJ_GMG_FECHADO":                                                                   [12308, 11],
    "DJ_LINHA_FECHADO":                                                                 [12308 + 1000, 15],

    # Relé
    "RELE_BLOQ_86BTBF":                                                                 [12309, 7],

    # Carregador de Baterias
    "CB_FALHA":                                                                         [12309, 8],

    # Conversor de Fibra
    "CONV_FIBRA_FALHA":                                                                 [12309, 9],

    # Supervisor Tensão
    "SUPER_TENSAO_FALHA":                                                               [12309, 10],
    "SUPER_TENSAO_TSA_FALHA":                                                           [12308, 12],
    "SUPER_TENSAO_GMG_FALHA":                                                           [12308, 13],

    # Dispositivo de Proteção de Surto
    "DPS_TSA":                                                                          [12309, 11],
    "DPS_GMG":                                                                          [12309, 12],

    # Sistem de Filtragem
    "SF_BOMBA_1_DEFEITO":                                                               [12308, 1],
    "SF_BOMBA_1_LIGADA":                                                                [12308, 2],

    # Transformador Elevador
    "TE_TEMP_MUITO_ALTA":                                                               [12308, 14],


    ## SST_ENTRAS_DIGITAIS_1
    # Disjuntores
    "DJ_LINHA_ABERTO":                                                                  [12311, 0],

    # Transformador Elevador
    "TE_TEMP_ALARME":                                                                   [12311, 1],
    "TE_PRESSAO_MUITO_ALTA":                                                            [12311, 2],
    "TE_NV_OLEO_MUITO_BAIXO":                                                           [12311, 3],

    # Paineis das Unidades de Geração
    "PRTVA1_50_BF":                                                                     [12311, 4],
    "PRTVA1_FILTRA_ACIONA":                                                             [12311, 5],
    "PRTVA2_50BF":                                                                      [12311, 6],
    "PRTVA2_FILTRA_ACIONA":                                                             [12311, 7],

    # Sistema de Filtragem
    "SFA_ENTRA_ELEM_1_ABERTA":                                                          [12311, 8],
    "SFA_ENTRA_ELEM_2_ABERTA":                                                          [12311, 9],
    "SFA_LIMP_ELEM_1_ABERTA":                                                           [12311, 10],
    "SFA_LIMP_ELEM_2_ABERTA":                                                           [12311, 11],
    "SFB_PRESSAO_SAIDA":                                                                [12311, 12],
    "SFB_ENTRA_ELEM_1_ABERTA":                                                          [12311, 13],
    "SFB_ENTRA_ELEM_2_ABERTA":                                                          [12311, 14],
    "SFB_LIMP_ELEM_1_ABERTA":                                                           [12311, 15],
    "SFB_LIMP_ELEM_2_ABERTA":                                                           [12310, 0],

    # Conversor de Fibra
    "CONVE_FIBRA_FALHA":                                                                [12310, 1],

    # Relé
    "RELE_LINHA_SEM_TRIP_FALHA":                                                        [12310, 2],


    ## STT_FALHAS_ANALOGICAS
    # Nível
    "NV_JUSANTE_FALHA_LEITURA":                                                         [12339, 1],

    # Sistema de Filtragem
    "SFA_PRESSAO_LADO_LIMPO_FALHA_LEITURA":                                             [12339, 2],
    "SFA_PRESSAO_LADO_SUJO_FALHA_LEITURA":                                              [12339, 3],
    "SFB_PRESSAO_LADO_LIMPO_FALHA_LEITURA":                                             [12339, 4],
    "SFB_PRESSAO_LADO_SUJO_FALHA_LEITURA":                                              [12339, 5],


    ## STT_ALARMES_HH_ANALOGICAS
    # Nível
    "NV_JUSANTE_MUITO_ALTO":                                                            [12341, 0],

    # Sistema de Filtragem
    "SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO":                                                [12341, 3],
    "SFA_PRESSAO_LADO_SUJO_MUITO_ALTO":                                                 [12341, 4],
    "SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO":                                                [12341, 5],
    "SFB_PRESSAO_LADO_SUJO_MUITO_ALTO":                                                 [12341, 6],


    ## STT_ALARMES_H_ANALOGICAS
    # Nível
    "NV_JUSANTE_ALTO":                                                                  [12343, 0],

    # Sistema de Filtragem
    "PSA_SFA_PRESSAO_LADO_LIMPO_ALTO":                                                  [12343, 3],
    "PSA_SFA_PRESSAO_LADO_SUJO_ALTO":                                                   [12343, 4],
    "PSA_SFB_PRESSAO_LADO_LIMPO_ALTO":                                                  [12343, 5],
    "PSA_SFB_PRESSAO_LADO_SUJO_ALTO":                                                   [12343, 6],


    ## STT_ALARMES_L_ANALOGICAS
    # Nível
    "NV_JUSANTE_BAIXO":                                                                 [12345, 0],

    # Sistema de Filtragem
    "SFA_PRESSAO_LADO_LIMPO_BAIXO":                                                     [12345, 3],
    "SFA_PRESSAO_LADO_SUJO_BAIXO":                                                      [12345, 4],
    "SFB_PRESSAO_LADO_LIMPO_BAIXO":                                                     [12345, 5],
    "SFB_PRESSAO_LADO_SUJO_BAIXO":                                                      [12345, 6],

    ## STT_ALARMES_LL_ANALOGICAS
    # Nível
    "NV_JUSANTE_MUITO_BAIXO":                                                           [12347, 0],

    # Sistema de Filtragem
    "SFA_PRESSAO_LADO_LIMPO_MUITO_BAIXO":                                               [12347, 3],
    "SFA_PRESSAO_LADO_SUJO_MUITO_BAIXO":                                                [12347, 4],
    "SFB_PRESSAO_LADO_LIMPO_MUITO_BAIXO":                                               [12347, 5],
    "SFB_PRESSAO_LADO_SUJO_MUITO_BAIXO":                                                [12347, 6],

    ## STT_SA_SE
    # Sistema  de Drenagem
    "DREN_BOMBA_1_INDISPONV":                                                           [12349, 0],
    "DREN_BOMBA_2_INDISPONV":                                                           [12349, 1],
    "DREN_BOMBA_1_PRINC":                                                               [12349, 2],
    "DREN_BOMBA_2_PRINC":                                                               [12349, 3],
    "DREN_BOIAS_DISCREPANCIA":                                                          [12349, 4],

    # Sistema de Filtragem
    "SF_BOMBA_1_INDISPONV":                                                             [12349, 5],
    "SF_BOMBA_1_FALHA":                                                                 [12349, 7],

    # Sistema de Esgotamento
    "ESGOTA_BOMBA_2_INDISPONV":                                                         [12349, 6],
    "ESGOTA_BOMBA_2_FALHA":                                                             [12349, 8],

    # Disjuntores
    "DJ_GMG_FALHA_FECHAR":                                                              [12349, 9],
    "DJ_GMG_FALHA_ABRIR":                                                               [12349, 10],
    "DJ_TSA_FALHA_ABRIR":                                                               [12349, 11],
    "DJ_TSA_FALHA_FECHAR":                                                              [12349, 12],
    "DJ_SE_FALHA_ABRIR":                                                                [12349, 13],
    "DJ_SE_FALHA_FECHAR":                                                               [12349, 14],


    ## STT_BLOQUEIO_50BF
    # 50BF
    "BLOQ_50BF_ATUADO":                                                                 [12350, 15],


    ## STT_BLOQUEIO_86BTLSA
    # 86BTLSA
    "BLOQ_86BTLSA_ATUADO":                                                              [12352, 15],


    ## STT_SF
    # Geral
    "SF_OPERANDO":                                                                      [12355, 0],

    # Sistema Filtragem A
    "SFA_COMUTACAO_MANUAL":                                                             [12355, 1],
    "SFA_COMUTACAO_BLOQUEADA":                                                          [12355, 2],
    "SFA_ELEM_1_OPERANDO":                                                              [12355, 3],
    "SFA_ELEM_1_LIMP":                                                                  [12355, 4],
    "SFA_ELEM_2_LIMP":                                                                  [12355, 5],
    "SFA_ELEM_2_OPERANDO":                                                              [12355, 6],
    "SFA_ELEM_1_FALHA_ABRIR_ENTRA":                                                     [12355, 7],
    "SFA_ELEM_1_FALHA_FECHAR_ENTRA":                                                    [12355, 8],
    "SFA_ELEM_2_FALHA_ABRIR_ENTRA":                                                     [12355, 9],
    "SFA_ELEM_2_FALHA_FECHAR_ENTRA":                                                    [12355, 10],
    "SFA_ELEM_1_FALHA_ABRIR_LIMP":                                                      [12355, 11],
    "SFA_ELEM_1_FALHA_FECHAR_LIMP":                                                     [12355, 12],
    "SFA_ELEM_2_FALHA_ABRIR_LIMP":                                                      [12355, 13],
    "SFA_ELEM_2_FALHA_FECHAR_LIMP":                                                     [12355, 14],

    # Sistema Filtragem B
    "SFB_ELEM_1_OPERANDO":                                                              [12355, 15],
    "SFB_ELEM_1_LIMP":                                                                  [12354, 0],
    "SFB_ELEM_2_LIMP":                                                                  [12354, 1],
    "SFB_ELEM_2_OPERANDO":                                                              [12354, 2],
    "SFB_ELEM_1_FALHA_ABRIR_ENTRA":                                                     [12354, 3],
    "SFB_ELEM_1_FALHA_FECHAR_ENTRA":                                                    [12354, 4],
    "SFB_ELEM_2_FALHA_ABRIR_ENTRA":                                                     [12354, 5],
    "SFB_ELEM_2_FALHA_FECHAR_ENTRA":                                                    [12354, 6],
    "SFB_ELEM_1_FALHA_ABRIR_LIMP":                                                      [12354, 7],
    "SFB_ELEM_1_FALHA_FECHAR_LIMP":                                                     [12354, 8],
    "SFB_ELEM_2_FALHA_ABRIR_LIMP":                                                      [12354, 9],
    "SFB_ELEM_2_FALHA_FECHAR_LIMP":                                                     [12354, 10],
    "SFB_COMUTACAO_MANUAL":                                                             [12354, 11],
    "SFB_COMUTACAO_BLOQUEADA":                                                          [12354, 12],


    ## LEITURAS_ANALÓGICAS
    # Níveis
    "NV_JUSANTE_CASA_FORCA":                                                            12488,
    "NV_MONTANTE_TA":                                                                   12490,

    # Sistema de Filtragem
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
    # Geral
    "CMD_RESET_GERAL":                                                                  [12289, 0],

    ### STATUS
    ## STT_ENTRAS_DIGITAIS_0
    # Dispositivo de Proteção de Surto
    "DPS":                                                                              [12309, 0],

    # Conversor de Fibra
    "CONVE_FIBRA_FALHA":                                                                [12309, 9],


    ## STT_ANALÓGICAS
    # Níveis
    "NV_JUSANTE_GRADE_FALHA_LEITURA":                                                   [12329, 0],
    "NV_MONTANTE_GRADE_FALHA_LEITURA":                                                  [12329, 1],
    "NV_JUSANTE_GRADE_MUITO_ALTO":                                                      [12329, 2],
    "NV_MONTANTE_GRADE_MUITO_ALTO":                                                     [12329, 3],
    "NV_JUSANTE_GRADE_ALTO":                                                            [12329, 4],
    "NV_MONTANTE_GRADE_ALTO":                                                           [12329, 5],
    "NV_JUSANTE_GRADE_BAIXO":                                                           [12329, 6],
    "NV_MONTANTE_GRADE_BAIXO":                                                          [12329, 7],
    "NV_JUSANTE_GRADE_MUITO_BAIXO":                                                     [12329, 8],
    "NV_MONTANTE_GRADE_MUITO_BAIXO":                                                    [12329, 9],


    ## LEITURAS_ANALÓGICAS
    # Níveis
    "NV_JUSANTE_GRADE":                                                                 12348 + 2000,
    "NV_MONTANTE_GRADE":                                                                12350 + 2000,
    "DIFERENCIAL_GRADE":                                                                999 + 2000,
    "NV_MONTANTE_TESTE":                                                                950 + 2000,
}

REG_UG = {
    "UG1": {
        ### COMANDOS
        ## CMD_UG1
        # Rearme
        "CMD_REARME_FALHAS":                                                            [12289 + 10000, 0],

        # Partida/Parada
        "CMD_PARADA_EMERG":                                                             [12289, 1],
        "CMD_PARADA_NV_HABILITA":                                                       [12289, 5],
        "CMD_PARADA_NV_DESABILITA":                                                     [12289, 6],
        "CMD_PARADA_TOTAL":                                                             [12290 + 10000, 0],
        "CMD_SINCRONISMO":                                                              [12290 + 10000, 9],

        # Controle de Nível
        "CMD_CONTROLE_NV":                                                              [12289, 2],
        "CMD_CONTROLE_POT_MANUAL":                                                      [12289, 3],
        "CMD_CONTROLE_POT_NV":                                                          [12289, 4],

        # RV e RT
        "CMD_RV_MANUTENCAO":                                                            [12289, 10],
        "CMD_RV_AUTOMATICO":                                                            [12289, 11],


        ## CMD_UHRV
        "CMD_UHRV_MODO_AUTOMATICO":                                                     [12291, 0],
        "CMD_UHRV_MODO_MANUTENCAO":                                                     [12291, 1],
        "CMD_UHRV_BOMBA_1_LIGA":                                                        [12291, 2],
        "CMD_UHRV_BOMBA_1_DESLIGA":                                                     [12291, 3],
        "CMD_UHRV_BOMBA_2_LIGA":                                                        [12291, 4],
        "CMD_UHRV_BOMBA_2_DESLIGA":                                                     [12291, 5],
        "CMD_UHRV_BOMBA_1_PRINC":                                                       [12291, 6],
        "CMD_UHRV_BOMBA_2_PRINC":                                                       [12291, 7],


        ## CMD_UHLM
        "CMD_UHLM_MODO_AUTOMATICO":                                                     [12293, 0],
        "CMD_UHLM_MODO_MANUTENCAO":                                                     [12293, 1],
        "CMD_UHLM_BOMBA_1_LIGA":                                                        [12293, 2],
        "CMD_UHLM_BOMBA_1_DESLIGA":                                                     [12293, 3],


        ## COMANDOS_ANALÓGICOS
        # Controle de Nível
        "SETPOINT_NV_5":                                                                12588,
        "SETPOINT_NV_4":                                                                12590,
        "SETPOINT_NV_3":                                                                12592,
        "SETPOINT_NV_2":                                                                12594,
        "SETPOINT_NV_1":                                                                12596,
        "SETPOINT_NV_PARADA":                                                           12598,
        "SETPOINT_POTENCIA_5":                                                          12600,
        "SETPOINT_POTENCIA_4":                                                          12602,
        "SETPOINT_POTENCIA_3":                                                          12604,
        "SETPOINT_POTENCIA_2":                                                          12606,
        "SETPOINT_POTENCIA_1":                                                          12608,
        "SETPOINT_MINIMO_POT":                                                          12610,
        "SETPOINT_MAXIMO_POT":                                                          12612,
        "SETPOINT_NV":                                                                  12616,



        ### STATUS
        ## STT_FALHAS_TEMP
        "TIRISTORES_TEMP_FALHA_LEITURA":                                                [12329, 0],
        "CROWBAR_TEMP_FALHA_LEITURA":                                                   [12329, 1],
        "TRAFO_EXCITACAO_TEMP_FALHA_LEITURA":                                           [12329, 2],
        "UHRV_TEMP_OLEO_FALHA_LEITURA":                                                 [12329, 3],
        "UHLM_TEMP_OLEO_FALHA_LEITURA":                                                 [12329, 4],
        "GERADOR_FASE_A_TEMP_FALHA_LEITURA":                                            [12329, 7],
        "GERADOR_FASE_B_TEMP_FALHA_LEITURA":                                            [12329, 8],
        "GERADOR_FASE_C_TEMP_FALHA_LEITURA":                                            [12329, 9],
        "GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA":                                          [12329, 10],
        "GERADOR_NUCLEO_2_TEMP_FALHA_LEITURA":                                          [12329, 11],
        "GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA":                                          [12329, 12],
        "MANCAL_GUIA_CASQUILHO_TEMP_FALHA_LEITURA":                                     [12329, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMP_FALHA_LEITURA":                                [12329, 14],
        "MANCAL_COMBINADO_ESCORA_TEMP_FALHA_LEITURA":                                   [12329, 15],


        ## STT_ALARMES_HH_TEMP
        "TIRISTORES_TEMP_MUITO_ALTA":                                                   [12331, 0],
        "CROWBAR_TEMP_MUITO_ALTA":                                                      [12331, 1],
        "TRAFO_EXCITACAO_TEMP_MUITO_ALTA":                                              [12331, 2],
        "UHRV_TEMP_OLEO_MUITO_ALTA":                                                    [12331, 3],
        "UHLM_TEMP_OLEO_MUITO_ALTA":                                                    [12331, 4],
        "GERADOR_FASE_A_TEMP_MUITO_ALTA":                                               [12331, 7],
        "GERADOR_FASE_B_TEMP_MUITO_ALTA":                                               [12331, 8],
        "GERADOR_FASE_C_TEMP_MUITO_ALTA":                                               [12331, 9],
        "GERADOR_NUCLEO_1_TEMP_MUITO_ALTA":                                             [12331, 10],
        "GERADOR_NUCLEO_2_TEMP_MUITO_ALTA":                                             [12331, 11],
        "GERADOR_NUCLEO_3_TEMP_MUITO_ALTA":                                             [12331, 12],
        "MANCAL_GUIA_CASQUILHO_TEMP_MUITO_ALTA":                                        [12331, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMP_MUITO_ALTA":                                   [12331, 14],
        "MANCAL_COMBINADO_ESCORA_TEMP_MUITO_ALTA":                                      [12331, 15],


        ## STT_ALARMES_H_TEMP
        "TIRISTORES_TEMP_ALTA":                                                         [12333, 0],
        "CROWBAR_TEMP_ALTA":                                                            [12333, 1],
        "TRAFO_EXCITACAO_TEMP_ALTA":                                                    [12333, 2],
        "UHRV_TEMP_OLEO_ALTA":                                                          [12333, 3],
        "UHLM_TEMP_OLEO_ALTA":                                                          [12333, 4],
        "GERADOR_FASE_A_TEMP_ALTA":                                                     [12333, 7],
        "GERADOR_FASE_B_TEMP_ALTA":                                                     [12333, 8],
        "GERADOR_FASE_C_TEMP_ALTA":                                                     [12333, 9],
        "GERADOR_NUCLEO_1_TEMP_ALTA":                                                   [12333, 10],
        "GERADOR_NUCLEO_2_TEMP_ALTA":                                                   [12333, 11],
        "GERADOR_NUCLEO_3_TEMP_ALTA":                                                   [12333, 12],
        "MANCAL_GUIA_CASQUILHO_TEMP_ALTA":                                              [12333, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMP_ALTA":                                         [12333, 14],
        "MANCAL_COMBINADO_ESCORA_TEMP_ALTA":                                            [12333, 15],


        ## STT_FALHAS_ANALOGICAS
        "UHRV_PRESSAO_OLEO_FALHA_LEITURA":                                              [12341, 0],
        "NV_JUSANTE_FALHA_LEITURA":                                                     [12341, 1],


        ## STT_ALARMES_HH_ANALOGICAS
        "UHRV_PRESSAO_OLEO_MUITO_ALTA":                                                 [12343, 0],
        "NV_JUSANTE_MUITO_ALTO":                                                        [12343, 1],


        ## STT_ALARMES_H_ANALOGICAS
        "UHRV_PRESSAO_OLEO_ALTA":                                                       [12345, 0],
        "NV_JUSANTE_ALTO":                                                              [12345, 1],


        ## STT_ALARMES_L_ANALOGICAS
        "UHRV_PRESSAO_OLEO_BAIXA":                                                      [12347, 0],
        "NV_JUSANTE_BAIXO":                                                             [12347, 1],


        ## STT_ALARMES_LL_ANALOGICAS
        "UHRV_PRESSAO_OLEO_MUITO_BAIXA":                                                [12349, 0],
        "NV_JUSANTE_MUITO_BAIXO":                                                       [12349, 1],


        ## LEITURAS_ANALÓGICAS
        # Temperaturas
        "TEMP_PONTE_TIRISTORES":                                                        12488,
        "TEMP_CROWBAR":                                                                 12490,
        "TEMP_GERADOR_FASE_A":                                                          12494 + 20000,
        "TEMP_GERADOR_FASE_B":                                                          12496 + 20000,
        "TEMP_GERADOR_FASE_C":                                                          12498 + 20000,
        "TEMP_GERADOR_NUCLEO_1":                                                        12500 + 20000,
        "TEMP_GERADOR_NUCLEO_2":                                                        12502 + 20000,
        "TEMP_GERADOR_NUCLEO_3":                                                        12504 + 20000,
        "TEMP_MANCAL_GUIA_CASQUILHO":                                                   12506 + 20000,
        "TEMP_MANCAL_COMBINADO_CASQUILHO":                                              12508 + 20000,
        "TEMP_MANCAL_COMBINADO_CONTRA_ESCORA":                                          12510 + 20000,
        "TEMP_MANCAL_COMBINADO_ESCORA":                                                 12512 + 20000,
        "TEMP_OLEO_UHLM":                                                               12514,
        "TEMP_OLEO_UHRV":                                                               12516,

        # Pressão
        "PRESSAO_OLEO_UHRV":                                                            12520,

        # Níveis
        "NV_JUSANTE":                                                                   12522,

        # Vibração
        "VIBRA_EIXO_X_GUIA":                                                            12524,
        "VIBRA_EIXO_X_COMBINADO":                                                       12526,
        "VIBRA_EIXO_Y_COMBINADO":                                                       12528,
        "VIBRA_EIXO_Z_COMBINADO":                                                       12530,
        "VIBRA_EIXO_Y_GUIA":                                                            12532,


        ## BLOQUEIO_86M
        "BLOQ_86M_ATUADO":                                                              [12428, 15],


        ## BLOQUEIO_86E
        "BLOQ_86E_ATUADO":                                                              [12340, 15],


        ## BLOQUEIO_86H
        "BLOQ_86H_ATUADO":                                                              [12342, 15],


        ## STT_BORBOLETA
        # Borboleta
        "BORB_FALHA_ABRIR":                                                             [12365, 0],
        "BORB_FALHA_FECHAR":                                                            [12365, 1],
        "BORB_ABRINDO":                                                                 [12365, 2],
        "BORB_FECHANDO":                                                                [12365, 3],
        "BORB_DISCRE_SENSES":                                                           [12365, 10],

        # Bypass
        "BYPASS_ABRINDO":                                                               [12365, 4],
        "BYPASS_FECHANDO":                                                              [12365, 5],
        "BYPASS_FALHA_ABRIR":                                                           [12365, 6],
        "BYPASS_FALHA_FECHAR":                                                          [12365, 7],
        "BYPASS_DISCRE_SENSES":                                                         [12365, 11],


        ## SST_ENTRAS_DIGITAIS_1
        # Botão Painel PRTVA
        "BT_BLOQ_86EH":                                                                 [12309, 0],
        "BT_PARA_UG":                                                                   [12309, 2],
        "BT_PARTE_UG":                                                                  [12309, 3],
        "BT_DIMINUI_REF_RV":                                                            [12309, 4],
        "BT_AUMENTA_REF_RV":                                                            [12309, 5],
        "BT_DIMINUI_REF_RT":                                                            [12309, 6],
        "BT_AUMENTA_REF_RT":                                                            [12309, 7],

        # Rearme
        "REARME_FALHAS":                                                                [12309, 1],

        # Relé
        "RELE_PROT_GERADOR_TRIP":                                                       [12309, 8],
        "RELE_PROT_GERADOR_50BF":                                                       [12309, 10],
        "RELE_BLOQ_86EH":                                                               [12310, 10],

        # RV
        "RV_TRIP":                                                                      [12309, 11],
        "RV_ALARME":                                                                    [12309, 12],
        "RV_HABILITADO":                                                                [12309, 13],
        "RV_REGULANDO":                                                                 [12309, 14],
        "RV_POTENCIA_NULA":                                                             [12309, 15],
        "RV_MAQUINA_PARADA":                                                            [12310, 0],
        "RV_VELOCIDADE_MENOR":                                                          [12310, 1],
        "RV_VELOCIDADE_MAIOR":                                                          [12310, 2],
        "RV_DISTRIBUIDOR_ABERTO":                                                       [12310, 3],

        # RT
        "RT_TRIP":                                                                      [12310, 4],
        "RT_ALARME":                                                                    [12310, 5],
        "RT_HABILITADO":                                                                [12310, 6],
        "RT_REGULANDO":                                                                 [12310, 7],

        # Contator Campo
        "CONTATOR_CAMPO_FECHADO":                                                       [12310, 8],

        # Disjuntores
        "DJ_MAQUINA_FECHADO":                                                           [12310, 9],

        # Supervisor Tensão
        "SUPER_TENSAO_ENTRA_CA":                                                        [12310, 11],

        # Dispositivo de Proteção de Surto
        "DPS":                                                                          [12310, 12],

        # UHRV
        "UHRV_BOMBA_DEFEITO":                                                           [12310, 13],
        "UHRV_BOMBA_LIGADA":                                                            [12310, 14],

        # UHLM
        "UHLM_BOMBA_DEFEITO":                                                           [12310, 15],


        ## SST_ENTRAS_DIGITAIS_2
        # UHLM
        "UHLM_BOMBA_LIGADA":                                                            [12311, 0],

        # Resistência Aquecedor
        "RESIS_AQUEC_GERA_DEFEITO":                                                     [12311, 3],
        "RESIS_AQUEC_GERA_LIGADA":                                                      [12311, 4],

        # Disjuntores
        "DJ_TPS_PROTECAO":                                                              [12311, 5],
        "DJ_TPS_PROTECAO_59N_ABERTO":                                                   [12312, 9],
        "DJ_LINHA_FECHADO":                                                             [12312, 6],

        # UHRV
        "UHRV_OLEO_NV_MUITO_BAIXO":                                                     [12311, 6],
        "UHRV_FILTRO_OLEO_SUJO":                                                        [12311, 7],
        "UHRV_PRESSAO_CRITICA":                                                         [12311, 8],
        "UHRV_PRESSAO_FREIO":                                                           [12311, 9],
        "UHLM_OLEO_NV_MUITO_ALTO":                                                      [12311, 11],
        "UHLM_OLEO_NV_MUITO_BAIXO":                                                     [12311, 12],
        "UHLM_PRESSAO_LINHA_LUBRIF":                                                    [12311, 13],
        "UHLM_FILTRO_OLEO_SUJO":                                                        [12311, 14],
        "UHLM_FLUXO_TROCADOR_CALOR":                                                    [12311, 15],

        # QBAG
        "QBAG_ESCOVA_POLO_POS_DESGASTADA":                                              [12312, 1],
        "QBAG_ESCOVA_POLO_NEG_DESGASTADA":                                              [12312, 2],

        # Bloqueio
        "BLOQUEIO_86BTBF":                                                              [12312, 3],

        # Poço de Drenagem
        "PD_NV_MUITO_ALTO":                                                             [12312, 4],

        # Sistema de Filtragem
        "SF_PRESSAO_SAIDA":                                                             [12312, 5],

        # Válvula Borboleta
        "VB_VALV_BORB_ABERTA":                                                          [12312, 12],
        "VB_VALV_BORB_FECHADA":                                                         [12312, 13],
        "VB_VALV_BYPASS_ABERTA":                                                        [12312, 14],
        "VB_VALV_BYPASS_FECHADA":                                                       [12312, 15],


        ## PARTIDA_PARADA
        "STT_PARTIDA_PARADA":                                                           12388,
        "SST_PASSO_SELECIONADO":                                                        12390 + 10000,
        "STT_PASSO_ATUAL":                                                              12392 + 10000,


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
        # Controle
        "CTRL_POTENCIA_POR_NV_HABILITADO":                                              [12361, 0],
        "CTRL_NV_HABILITADO":                                                           [12361, 1],
        "CTRL_POTENCIA_MANUAL_HABILITADO":                                              [12361, 2],
        "CTRL_PARADA_POR_NV_HABILITADO":                                                [12361, 3],
        "CTRL_PARADA_NV_BAIXO":                                                         [12361, 4],
        "CTRL_FALHA_SENS_NV":                                                           [12361, 5],
        "CTRL_ALARME_DIFERENCIAL_DE_GRADE":                                             [12361, 6],
        "CTRL_TRIP_DIFERENCIAL_DE_GRADE":                                               [12361, 7],

        # Resistencia Aquecedor
        "RESIS_AQUEC_GERA_INDISPONV":                                                   [12361, 8],
        "RESIS_AQUEC_GERA_FALHA_LIGAR":                                                 [12361, 9],
        "RESIS_AQUEC_GERA_FALHA_DESLIGAR":                                              [12361, 10],
        "FREIO_FALHA_APLICAR_DESAPLICAR":                                               [12361, 11],


        ## STT_UHLM
        "UHLM_UNIDADE_MANUTENCAO":                                                      [12365, 0],
        "UHLM_BOMBA_1_INDISPONV":                                                       [12365, 2],
        "UHLM_BOMBA_2_INDISPONV":                                                       [12365, 3],
        "UHLM_BOMBA_1_PRINC":                                                           [12365, 4],
        "UHLM_BOMBA_2_PRINC":                                                           [12365, 5],
        "UHLM_BOMBA_1_FALHA_AO_LIGAR":                                                  [12365, 6],
        "UHLM_BOMBA_1_FALHA_AO_DESLIGAR":                                               [12365, 7],
        "UHLM_BOMBA_2_FALHA_AO_LIGAR":                                                  [12365, 8],
        "UHLM_BOMBA_2_FALHA_AO_DESLIGAR":                                               [12365, 9],
        "UHLM_BOMBA_1_FALHA_AO_PRESSURIZAR":                                            [12365, 10],
        "UHLM_BOMBA_2_FALHA_AO_PRESSURIZAR":                                            [12365, 11],
        "UHLM_FILTRO_OLEO_SUJO":                                                        [12365, 13],
        "UHLM_FALHA_PRESSOSTATO":                                                       [12365, 14],


        ## STT_UHRV
        "UHRV_UNIDADE_MANUTENCAO":                                                      [12361, 0],
        "UHRV_UNIDADE_HABILITADA":                                                      [12361, 1],
        "UHRV_BOMBA_1_INDISPONV":                                                       [12361, 2],
        "UHRV_BOMBA_2_INDISPONV":                                                       [12361, 3],
        "UHRV_BOMBA_1_PRINC":                                                           [12361, 4],
        "UHRV_BOMBA_2_PRINC":                                                           [12361, 5],
        "UHRV_BOMBA_1_FALHA_AO_LIGAR":                                                  [12361, 6],
        "UHRV_BOMBA_1_FALHA_AO_DESLIGAR":                                               [12361, 7],
        "UHRV_BOMBA_2_FALHA_AO_LIGAR":                                                  [12361, 8],
        "UHRV_BOMBA_2_FALHA_AO_DESLIGAR":                                               [12361, 9],
        "UHRV_BOMBA_1_FALHA_AO_PRESSURIZAR":                                            [12361, 10],
        "UHRV_BOMBA_2_FALHA_AO_PRESSURIZAR":                                            [12361, 11],
        "UHRV_FILTRO_OLEO_SUJO":                                                        [12361, 13],
    },

    "UG2": {
        ### COMANDOS
        ## CMD_UG1
        # Rearme
        "CMD_REARME_FALHAS":                                                            [12289 + 20000, 0],

        # Partida/Parada
        "CMD_PARADA_EMERG":                                                             [12289, 1],
        "CMD_PARADA_NV_HABILITA":                                                       [12289, 5],
        "CMD_PARADA_NV_DESABILITA":                                                     [12289, 6],
        "CMD_PARADA_TOTAL":                                                             [12290 + 20000, 0],
        "CMD_SINCRONISMO":                                                              [12290 + 20000, 9],

        # Controle de Nível
        "CMD_CONTROLE_NV":                                                              [12289, 2],
        "CMD_CONTROLE_POT_MANUAL":                                                      [12289, 3],
        "CMD_CONTROLE_POT_NV":                                                          [12289, 4],

        # RV e RT
        "CMD_RV_MANUTENCAO":                                                            [12289, 10],
        "CMD_RV_AUTOMATICO":                                                            [12289, 11],


        ## CMD_UHRV
        "CMD_UHRV_MODO_AUTOMATICO":                                                     [12291, 0],
        "CMD_UHRV_MODO_MANUTENCAO":                                                     [12291, 1],
        "CMD_UHRV_BOMBA_1_LIGA":                                                        [12291, 2],
        "CMD_UHRV_BOMBA_1_DESLIGA":                                                     [12291, 3],
        "CMD_UHRV_BOMBA_2_LIGA":                                                        [12291, 4],
        "CMD_UHRV_BOMBA_2_DESLIGA":                                                     [12291, 5],
        "CMD_UHRV_BOMBA_1_PRINC":                                                       [12291, 6],
        "CMD_UHRV_BOMBA_2_PRINC":                                                       [12291, 7],


        ## CMD_UHLM
        "CMD_UHLM_MODO_AUTOMATICO":                                                     [12293, 0],
        "CMD_UHLM_MODO_MANUTENCAO":                                                     [12293, 1],
        "CMD_UHLM_BOMBA_1_LIGA":                                                        [12293, 2],
        "CMD_UHLM_BOMBA_1_DESLIGA":                                                     [12293, 3],


        ## COMANDOS_ANALÓGICOS
        # Controle de Nível
        "SETPOINT_NV_5":                                                                12588,
        "SETPOINT_NV_4":                                                                12590,
        "SETPOINT_NV_3":                                                                12592,
        "SETPOINT_NV_2":                                                                12594,
        "SETPOINT_NV_1":                                                                12596,
        "SETPOINT_NV_PARADA":                                                           12598,
        "SETPOINT_POTENCIA_5":                                                          12600,
        "SETPOINT_POTENCIA_4":                                                          12602,
        "SETPOINT_POTENCIA_3":                                                          12604,
        "SETPOINT_POTENCIA_2":                                                          12606,
        "SETPOINT_POTENCIA_1":                                                          12608,
        "SETPOINT_MINIMO_POT":                                                          12610,
        "SETPOINT_MAXIMO_POT":                                                          12612,
        "SETPOINT_NV":                                                                  12616,



        ### STATUS
        ## STT_FALHAS_TEMP
        "TIRISTORES_TEMP_FALHA_LEITURA":                                                [12329, 0],
        "CROWBAR_TEMP_FALHA_LEITURA":                                                   [12329, 1],
        "TRAFO_EXCITACAO_TEMP_FALHA_LEITURA":                                           [12329, 2],
        "UHRV_TEMP_OLEO_FALHA_LEITURA":                                                 [12329, 3],
        "UHLM_TEMP_OLEO_FALHA_LEITURA":                                                 [12329, 4],
        "GERADOR_FASE_A_TEMP_FALHA_LEITURA":                                            [12329, 7],
        "GERADOR_FASE_B_TEMP_FALHA_LEITURA":                                            [12329, 8],
        "GERADOR_FASE_C_TEMP_FALHA_LEITURA":                                            [12329, 9],
        "GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA":                                          [12329, 10],
        "GERADOR_NUCLEO_2_TEMP_FALHA_LEITURA":                                          [12329, 11],
        "GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA":                                          [12329, 12],
        "MANCAL_GUIA_CASQUILHO_TEMP_FALHA_LEITURA":                                     [12329, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMP_FALHA_LEITURA":                                [12329, 14],
        "MANCAL_COMBINADO_ESCORA_TEMP_FALHA_LEITURA":                                   [12329, 15],


        ## STT_ALARMES_HH_TEMP
        "TIRISTORES_TEMP_MUITO_ALTA":                                                   [12331, 0],
        "CROWBAR_TEMP_MUITO_ALTA":                                                      [12331, 1],
        "TRAFO_EXCITACAO_TEMP_MUITO_ALTA":                                              [12331, 2],
        "UHRV_TEMP_OLEO_MUITO_ALTA":                                                    [12331, 3],
        "UHLM_TEMP_OLEO_MUITO_ALTA":                                                    [12331, 4],
        "GERADOR_FASE_A_TEMP_MUITO_ALTA":                                               [12331, 7],
        "GERADOR_FASE_B_TEMP_MUITO_ALTA":                                               [12331, 8],
        "GERADOR_FASE_C_TEMP_MUITO_ALTA":                                               [12331, 9],
        "GERADOR_NUCLEO_1_TEMP_MUITO_ALTA":                                             [12331, 10],
        "GERADOR_NUCLEO_2_TEMP_MUITO_ALTA":                                             [12331, 11],
        "GERADOR_NUCLEO_3_TEMP_MUITO_ALTA":                                             [12331, 12],
        "MANCAL_GUIA_CASQUILHO_TEMP_MUITO_ALTA":                                        [12331, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMP_MUITO_ALTA":                                   [12331, 14],
        "MANCAL_COMBINADO_ESCORA_TEMP_MUITO_ALTA":                                      [12331, 15],


        ## STT_ALARMES_H_TEMP
        "TIRISTORES_TEMP_ALTA":                                                         [12333, 0],
        "CROWBAR_TEMP_ALTA":                                                            [12333, 1],
        "TRAFO_EXCITACAO_TEMP_ALTA":                                                    [12333, 2],
        "UHRV_TEMP_OLEO_ALTA":                                                          [12333, 3],
        "UHLM_TEMP_OLEO_ALTA":                                                          [12333, 4],
        "GERADOR_FASE_A_TEMP_ALTA":                                                     [12333, 7],
        "GERADOR_FASE_B_TEMP_ALTA":                                                     [12333, 8],
        "GERADOR_FASE_C_TEMP_ALTA":                                                     [12333, 9],
        "GERADOR_NUCLEO_1_TEMP_ALTA":                                                   [12333, 10],
        "GERADOR_NUCLEO_2_TEMP_ALTA":                                                   [12333, 11],
        "GERADOR_NUCLEO_3_TEMP_ALTA":                                                   [12333, 12],
        "MANCAL_GUIA_CASQUILHO_TEMP_ALTA":                                              [12333, 13],
        "MANCAL_COMBINADO_CASQUILHO_TEMP_ALTA":                                         [12333, 14],
        "MANCAL_COMBINADO_ESCORA_TEMP_ALTA":                                            [12333, 15],


        ## STT_FALHAS_ANALOGICAS
        "UHRV_PRESSAO_OLEO_FALHA_LEITURA":                                              [12341, 0],
        "NV_JUSANTE_FALHA_LEITURA":                                                     [12341, 1],


        ## STT_ALARMES_HH_ANALOGICAS
        "UHRV_PRESSAO_OLEO_MUITO_ALTA":                                                 [12343, 0],
        "NV_JUSANTE_MUITO_ALTO":                                                        [12343, 1],


        ## STT_ALARMES_H_ANALOGICAS
        "UHRV_PRESSAO_OLEO_ALTA":                                                       [12345, 0],
        "NV_JUSANTE_ALTO":                                                              [12345, 1],


        ## STT_ALARMES_L_ANALOGICAS
        "UHRV_PRESSAO_OLEO_BAIXA":                                                      [12347, 0],
        "NV_JUSANTE_BAIXo":                                                             [12347, 1],


        ## STT_ALARMES_LL_ANALOGICAS
        "UHRV_PRESSAO_OLEO_MUITO_BAIXA":                                                [12349, 0],
        "NV_JUSANTE_MUITO_BAIXO":                                                       [12349, 1],


        ## LEITURAS_ANALÓGICAS
        # Temperaturas
        "TEMP_PONTE_TIRISTORES":                                                        12488,
        "TEMP_CROWBAR":                                                                 12490,
        "TEMP_GERADOR_FASE_A":                                                          12494 + 10000,
        "TEMP_GERADOR_FASE_B":                                                          12496 + 10000,
        "TEMP_GERADOR_FASE_C":                                                          12498 + 10000,
        "TEMP_GERADOR_NUCLEO_1":                                                        12500 + 10000,
        "TEMP_GERADOR_NUCLEO_2":                                                        12502 + 10000,
        "TEMP_GERADOR_NUCLEO_3":                                                        12504 + 10000,
        "TEMP_MANCAL_GUIA_CASQUILHO":                                                   12506 + 10000,
        "TEMP_MANCAL_COMBINADO_CASQUILHO":                                              12508 + 10000,
        "TEMP_MANCAL_COMBINADO_CONTRA_ESCORA":                                          12510 + 10000,
        "TEMP_MANCAL_COMBINADO_ESCORA":                                                 12512 + 10000,
        "TEMP_OLEO_UHLM":                                                               12514,
        "TEMP_OLEO_UHRV":                                                               12516,

        # Pressão
        "PRESSAO_OLEO_UHRV":                                                            12520,

        # Níveis
        "NV_JUSANTE":                                                                   12522,

        # Vibração
        "VIBRA_EIXO_X_GUIA":                                                            12524,
        "VIBRA_EIXO_X_COMBINADO":                                                       12526,
        "VIBRA_EIXO_Y_COMBINADO":                                                       12528,
        "VIBRA_EIXO_Z_COMBINADO":                                                       12530,
        "VIBRA_EIXO_Y_GUIA":                                                            12532,


        ## BLOQUEIO_86M
        "BLOQ_86M_ATUADO":                                                              [12428, 15],


        ## BLOQUEIO_86E
        "BLOQ_86E_ATUADO":                                                              [12340, 15],


        ## BLOQUEIO_86H
        "BLOQ_86H_ATUADO":                                                              [12342, 15],


        ## STT_BORBOLETA
        # Borboleta
        "BORB_FALHA_ABRIR":                                                             [12365, 0],
        "BORB_FALHA_FECHAR":                                                            [12365, 1],
        "BORB_ABRINDO":                                                                 [12365, 2],
        "BORB_FECHANDO":                                                                [12365, 3],
        "BORB_DISCRE_SENSES":                                                           [12365, 10],

        # Bypass
        "BYPASS_ABRINDO":                                                               [12365, 4],
        "BYPASS_FECHANDO":                                                              [12365, 5],
        "BYPASS_FALHA_ABRIR":                                                           [12365, 6],
        "BYPASS_FALHA_FECHAR":                                                          [12365, 7],
        "BYPASS_DISCRE_SENSES":                                                         [12365, 11],


        ## SST_ENTRAS_DIGITAIS_1
        # Botão Painel PRTVA
        "BT_BLOQ_86EH":                                                                 [12309, 0],
        "BT_PARA_UG":                                                                   [12309, 2],
        "BT_PARTE_UG":                                                                  [12309, 3],
        "BT_DIMINUI_REF_RV":                                                            [12309, 4],
        "BT_AUMENTA_REF_RV":                                                            [12309, 5],
        "BT_DIMINUI_REF_RT":                                                            [12309, 6],
        "BT_AUMENTA_REF_RT":                                                            [12309, 7],

        # Rearme
        "REARME_FALHAS":                                                                [12309, 1],

        # Relé
        "RELE_PROT_GERADOR_TRIP":                                                       [12309, 8],
        "RELE_PROT_GERADOR_50BF":                                                       [12309, 10],
        "RELE_BLOQ_86EH":                                                               [12310, 10],

        # RV
        "RV_TRIP":                                                                      [12309, 11],
        "RV_ALARME":                                                                    [12309, 12],
        "RV_HABILITADO":                                                                [12309, 13],
        "RV_REGULANDO":                                                                 [12309, 14],
        "RV_POTENCIA_NULA":                                                             [12309, 15],
        "RV_MAQUINA_PARADA":                                                            [12310, 0],
        "RV_VELOCIDADE_MENOR":                                                          [12310, 1],
        "RV_VELOCIDADE_MAIOR":                                                          [12310, 2],
        "RV_DISTRIBUIDOR_ABERTO":                                                       [12310, 3],

        # RT
        "RT_TRIP":                                                                      [12310, 4],
        "RT_ALARME":                                                                    [12310, 5],
        "RT_HABILITADO":                                                                [12310, 6],
        "RT_REGULANDO":                                                                 [12310, 7],

        # Contator Campo
        "CONTATOR_CAMPO_FECHADO":                                                       [12310, 8],

        # Disjuntores
        "DJ_MAQUINA_FECHADO":                                                           [12310, 9],

        # Supervisor Tensão
        "SUPER_TENSAO_ENTRA_CA":                                                        [12310, 11],

        # Dispositivo de Proteção de Surto
        "DPS":                                                                          [12310, 12],

        # UHRV
        "UHRV_BOMBA_DEFEITO":                                                           [12310, 13],
        "UHRV_BOMBA_LIGADA":                                                            [12310, 14],

        # UHLM
        "UHLM_BOMBA_DEFEITO":                                                           [12310, 15],


        ## SST_ENTRAS_DIGITAIS_2
        # UHLM
        "UHLM_BOMBA_LIGADA":                                                            [12311, 0],

        # Resistência Aquecedor
        "RESIS_AQUEC_GERA_DEFEITO":                                                     [12311, 3],
        "RESIS_AQUEC_GERA_LIGADA":                                                      [12311, 4],

        # Disjuntores
        "DJ_TPS_PROTECAO":                                                              [12311, 5],
        "DJ_TPS_PROTECAO_59N_ABERTO":                                                   [12312, 9],
        "DJ_LINHA_FECHADO":                                                             [12312, 6],

        # UHRV
        "UHRV_OLEO_NV_MUITO_BAIXO":                                                     [12311, 6],
        "UHRV_FILTRO_OLEO_SUJO":                                                        [12311, 7],
        "UHRV_PRESSAO_CRITICA":                                                         [12311, 8],
        "UHRV_PRESSAO_FREIO":                                                           [12311, 9],
        "UHLM_OLEO_NV_MUITO_ALTO":                                                      [12311, 11],
        "UHLM_OLEO_NV_MUITO_BAIXO":                                                     [12311, 12],
        "UHLM_PRESSAO_LINHA_LUBRIF":                                                    [12311, 13],
        "UHLM_FILTRO_OLEO_SUJO":                                                        [12311, 14],
        "UHLM_FLUXO_TROCADOR_CALOR":                                                    [12311, 15],

        # QBAG
        "QBAG_ESCOVA_POLO_POS_DESGASTADA":                                              [12312, 1],
        "QBAG_ESCOVA_POLO_NEG_DESGASTADA":                                              [12312, 2],

        # Bloqueio
        "BLOQUEIO_86BTBF":                                                              [12312, 3],

        # Poço de Drenagem
        "PD_NV_MUITO_ALTO":                                                             [12312, 4],

        # Sistema de Filtragem
        "SF_PRESSAO_SAIDA":                                                             [12312, 5],

        # Válvula Borboleta
        "VB_VALV_BORB_ABERTA":                                                          [12312, 12],
        "VB_VALV_BORB_FECHADA":                                                         [12312, 13],
        "VB_VALV_BYPASS_ABERTA":                                                        [12312, 14],
        "VB_VALV_BYPASS_FECHADA":                                                       [12312, 15],


        ## PARTIDA_PARADA
        "STT_PARTIDA_PARADA":                                                           12388,
        "SST_PASSO_SELECIONADO":                                                        12390 + 20000,
        "STT_PASSO_ATUAL":                                                              12392 + 20000,


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
        # Controle
        "CTRL_POTENCIA_POR_NV_HABILITADO":                                              [12361, 0],
        "CTRL_NV_HABILITADO":                                                           [12361, 1],
        "CTRL_POTENCIA_MANUAL_HABILITADO":                                              [12361, 2],
        "CTRL_PARADA_POR_NV_HABILITADO":                                                [12361, 3],
        "CTRL_PARADA_NV_BAIXO":                                                         [12361, 4],
        "CTRL_FALHA_SENS_NV":                                                           [12361, 5],
        "CTRL_ALARME_DIFERENCIAL_DE_GRADE":                                             [12361, 6],
        "CTRL_TRIP_DIFERENCIAL_DE_GRADE":                                               [12361, 7],

        # Resistencia Aquecedor
        "RESIS_AQUEC_GERA_INDISPONV":                                                   [12361, 8],
        "RESIS_AQUEC_GERA_FALHA_LIGAR":                                                 [12361, 9],
        "RESIS_AQUEC_GERA_FALHA_DESLIGAR":                                              [12361, 10],
        "FREIO_FALHA_APLICAR_DESAPLICAR":                                               [12361, 11],


        ## STT_UHLM
        "UHLM_UNIDADE_MANUTENCAO":                                                      [12365, 0],
        "UHLM_BOMBA_1_INDISPONV":                                                       [12365, 2],
        "UHLM_BOMBA_2_INDISPONV":                                                       [12365, 3],
        "UHLM_BOMBA_1_PRINC":                                                           [12365, 4],
        "UHLM_BOMBA_2_PRINC":                                                           [12365, 5],
        "UHLM_BOMBA_1_FALHA_AO_LIGAR":                                                  [12365, 6],
        "UHLM_BOMBA_1_FALHA_AO_DESLIGAR":                                               [12365, 7],
        "UHLM_BOMBA_2_FALHA_AO_LIGAR":                                                  [12365, 8],
        "UHLM_BOMBA_2_FALHA_AO_DESLIGAR":                                               [12365, 9],
        "UHLM_BOMBA_1_FALHA_AO_PRESSURIZAR":                                            [12365, 10],
        "UHLM_BOMBA_2_FALHA_AO_PRESSURIZAR":                                            [12365, 11],
        "UHLM_FILTRO_OLEO_SUJO":                                                        [12365, 13],
        "UHLM_FALHA_PRESSOSTATO":                                                       [12365, 14],


        ## STT_UHRV
        "UHRV_UNIDADE_MANUTENCAO":                                                      [12361, 0],
        "UHRV_UNIDADE_HABILITADA":                                                      [12361, 1],
        "UHRV_BOMBA_1_INDISPONV":                                                       [12361, 2],
        "UHRV_BOMBA_2_INDISPONV":                                                       [12361, 3],
        "UHRV_BOMBA_1_PRINC":                                                           [12361, 4],
        "UHRV_BOMBA_2_PRINC":                                                           [12361, 5],
        "UHRV_BOMBA_1_FALHA_AO_LIGAR":                                                  [12361, 6],
        "UHRV_BOMBA_1_FALHA_AO_DESLIGAR":                                               [12361, 7],
        "UHRV_BOMBA_2_FALHA_AO_LIGAR":                                                  [12361, 8],
        "UHRV_BOMBA_2_FALHA_AO_DESLIGAR":                                               [12361, 9],
        "UHRV_BOMBA_1_FALHA_AO_PRESSURIZAR":                                            [12361, 10],
        "UHRV_BOMBA_2_FALHA_AO_PRESSURIZAR":                                            [12361, 11],
        "UHRV_FILTRO_OLEO_SUJO":                                                        [12361, 13],
    },
}

REG_RTV = {
    "UG1":{
        ### RV
        ## LEITURAS_1
        "ROTACAO":                                                                          16,
        "ESTADO_OPERACAO":                                                                  21,
        "CRTL_SINCRONIZADO_SELEC":                                                          22,
        "CRTL_VAZIO_SELEC":                                                                 23,
        "CMD_MODBUS":                                                                       24,


        ## ENTRAS_DIGITAIS
        "RV_SEM_BLOQ_EXTERNO":                                                              [25, 0],
        "RV_HAB_REGULADOR":                                                                 [25, 1],
        "RV_SELEC_MODO_CTRL_ISOLADO":                                                       [25, 2],
        "RV_ZERA_CARGA":                                                                    [25, 3],
        "RV_RESET_FALHAS":                                                                  [25, 4],
        "RV_INCRE_REF_CTRL":                                                                [25, 5],
        "RV_DECRE_REF_CTRL":                                                                [25, 6],
        "RV_DJ_MAQUINA_FECHADO":                                                            [25, 7],


        ## SAÍDAS_DIGITAIS
        "RV_RELE_TRIP_NAO_ATUADO":                                                          [26, 0],
        "RV_RELE_ALARME":                                                                   [26, 1],
        "RV_RELE_REGULADOR_HAB":                                                            [26, 2],
        "RV_RELE_REGULADOR_REGULANDO":                                                      [26, 3],
        "RV_RELE_POT_NULA":                                                                 [26, 4],
        "RV_RELE_MAQUINA_PARADA":                                                           [26, 5],
        "RV_RELE_VELO_MENOR_30%":                                                           [26, 6],
        "RV_RELE_VELO_MAIOR_90%":                                                           [26, 7],
        "RV_RELE_DISTRI_ABERTO":                                                            [26, 8],


        ## LIMITES_OPERAÇÃO
        "RV_LIM_SUP_DISTRI_ATUADO":                                                         [27, 0],
        "RV_LIM_INF_DISTRI_ATUADO":                                                         [27, 1],
        "RV_LIM_SUP_ROTOR_ATUADO":                                                          [27, 2],
        "RV_LIM_INF_ROTOR_ATUADO":                                                          [27, 3],
        "RV_LIM_SUP_VELO_ATUADO":                                                           [27, 4],
        "RV_LIM_INF_VELO_ATUADO":                                                           [27, 5],
        "RV_LIM_SUP_POT_ATUADO":                                                            [27, 6],
        "RV_LIM_INF_POT_ATUADO":                                                            [27, 7],


        ## LEITURAS_2
        "SETPOINT_ABERTURA_PU":                                                             28,
        "SETPOINT_VELO":                                                                    29,
        "SETPOINT_POT_ATIVA_KW":                                                            30,
        "SETPOINT_POT_ATIVA_PU":                                                            30 + 3100,
        "SAIDA_CTRL_DISTRI":                                                                32,
        "SAIDA_CTRL_ROTOR":                                                                 33,
        "REF_DISTRI_PU":                                                                    36,
        "FEEDBACK_DISTRI_PU":                                                               37,
        "SAIDA_CTRL_DISTRI_PU":                                                             32,
        "REF_ROTOR_PU":                                                                     42,
        "FEEDBACK_ROTOR_PU":                                                                43,
        "SAIDA_CTRL_ROTOR_PU":                                                              33,
        "REF_VELO_PU":                                                                      48,
        "FEEDBACK_VELO_PU":                                                                 49,
        "REF_POT_ATIVA_PU":                                                                 54,
        "FEEDBACK_POT_ATIVA_PU":                                                            55,


        ## ALARME
        "RV_ALARME_SOBREFREQUENCIA":                                                        [66, 0],
        "RV_ALARME_SUBFREQUENCIA":                                                          [66, 1],
        "RV_ALARME_LEITURA_POS_DISTRI":                                                     [66, 2],
        "RV_ALARME_LEITURA_POS_ROTOR":                                                      [66, 3],
        "RV_ALARME_LEITURA_POT_ATIVA":                                                      [66, 4],
        "RV_ALARME_LEITURA_REF_POT":                                                        [66, 5],
        "RV_ALARME_LEITURA_NV_MONTANTE":                                                    [66, 6],
        "RV_ALARME_NV_MONTANTE_MUITO_BAIXO":                                                [66, 7],
        "RV_ALARME_CTRL_POS_DISTRI":                                                        [66, 8],
        "RV_ALARME_CTRL_POS_ROTOR":                                                         [66, 9],
        "RV_ALARME_RUIDO_MED_VELO_PRINC":                                                   [66, 10],
        "RV_ALARME_RUIDO_MED_VELO_RETAG":                                                   [66, 11],
        "RV_ALARME_PERDA_MED_VELO_PRINC":                                                   [66, 12],
        "RV_ALARME_PERDA_MED_VELO_RETAG":                                                   [66, 13],
        "RV_ALARME_DIF_MED_VELO_PRINC_RETAG":                                               [66, 14],


        ## FALHA_1
        "RV_FALHA_SOBREFREQUENCIA_INSTAN":                                                  [67, 0],
        "RV_FALHA_SOBREFREQUENCIA_TEMPO":                                                   [67, 1],
        "RV_FALHA_SUBFREQUENCIA_TEMPO":                                                     [67, 2],
        "RV_FALHA_GIRANDO_SEM_REG_GIRO_INDEVIDO":                                           [67, 3],
        "RV_FALHA_LEITURA_POS_DISTRI":                                                      [67, 4],
        "RV_FALHA_LEITURA_POS_ROTOR":                                                       [67, 5],
        "RV_FALHA_LEITURA_POT_ATIVA":                                                       [67, 6],
        "RV_FALHA_LEITURA_REF_POT":                                                         [67, 7],
        "RV_FALHA_LEITURA_NV_MONTANTE":                                                     [67, 8],
        "RV_FALHA_NV_MONTANTE_MUITO_BAIXO":                                                 [67, 10],
        "RV_FALHA_CTRL_POS_DISTRI":                                                         [67, 11],
        "RV_FALHA_CTRL_POS_ROTOR":                                                          [67, 12],
        "RV_FALHA_RUIDO_MED_VELO_PRINC":                                                    [67, 13],
        "RV_FALHA_RUIDO_MED_VELO_RETAG":                                                    [67, 14],
        "RV_FALHA_PERDA_MED_VELO_PRINC":                                                    [67, 15],


        ## FALHA_2
        "RV_FALHA_RUIDO_MED_VELO_RETAG":                                                    [68, 0],
        "RV_FALHA_TEMPO_EXCESSIVO_PARTIDA":                                                 [68, 1],
        "RV_FALHA_TEMPO_EXCESSIVO_PARADA":                                                  [68, 2],
        "RV_FALHA_BLOQ_EXTERNO":                                                            [68, 3],
        "RV_FALHA_DIF_MED_VELO_PRINC_RETAG":                                                [68, 4],


        ## LEITURAS_3
        "POT_APARENTE_NOMINAL":                                                             79,
        "POT_ATIVA_NOMINAL":                                                                80,
        "CTRL_1":                                                                           85,
        "CTRL_2":                                                                           86,
        "CONJ_DISTRI_1":                                                                    121,
        "CONJ_ROTOR_1":                                                                     122,
        "CONJ_DISTRI_2":                                                                    123,
        "CONJ_ROTOR_2":                                                                     124,
        "CONJ_DISTRI_3":                                                                    125,
        "CONJ_ROTOR_3":                                                                     126,
        "CONJ_DISTRI_4":                                                                    127,
        "CONJ_ROTOR_4":                                                                     128,
        "CONJ_DISTRI_5":                                                                    129,
        "CONJ_ROTOR_5":                                                                     130,
        "CONJ_DISTRI_6":                                                                    131,
        "CONJ_ROTOR_6":                                                                     132,
        "CONJ_DISTRI_7":                                                                    133,
        "CONJ_ROTOR_7":                                                                     134,
        "CONJ_DISTRI_8":                                                                    135,
        "CONJ_ROTOR_8":                                                                     136,
        "CONJ_DISTRI_9":                                                                    137,
        "CONJ_ROTOR_9":                                                                     138,
        "CONJ_DISTRI_10":                                                                   139,
        "CONJ_ROTOR_10":                                                                    140,
        "ABERTURA_MAX_DISTRI":                                                              182,
        "ABERTURA_MAX_DISTRI_VAZIO":                                                        184,
        "ABERTURA_MIN_DISTRI":                                                              183,
        "ABERTURA_MAX_ROTOR":                                                               185,
        "ABERTURA_MIN_ROTOR":                                                               186,
        "POTENCIA_MAX":                                                                     189,
        "POTENCIA_MIN":                                                                     190,



        ### RT
        ## LEITURAS_1
        "CORRENTE_EXCITACAO":                                                               16,
        "TENSAO_EXCITACAO":                                                                 17,
        "TEMP_ROTOR":                                                                       25,
        "ESTADO_OPERACAO":                                                                  26,
        "CTRL_SINCRONIZADO_SELEC":                                                          27,


        ## ENTRAS_DIGITAIS
        "RT_SEM_BLOQ_EXTERNO":                                                              [30, 0],
        "RT_HAB_REGULADOR":                                                                 [30, 1],
        "RT_SELEC_MODO_CTRL_ISOLADO":                                                       [30, 2],
        "RV_DRIVE_EXCITACAO_HAB_LOGICA_DISPARO":                                            [30, 3],
        "RV_RESET_FALHAS":                                                                  [30, 4],
        "RT_INCRE_REF_CTRL":                                                                [30, 5],
        "RT_DECRE_REF_CTRL":                                                                [30, 6],
        "RT_DJ_MAQUINA_FECHADO":                                                            [30, 7],
        "RT_CONTATOR_CAMPO_FECHADO":                                                        [30, 8],
        "RT_CROWBAR_INATIVO":                                                               [30, 9],


        ## SAIDAS_DIGITAIS
        "RT_RELE_TRIP_NAO_ATUADO":                                                          [31, 0],
        "RT_RELE_ALARME":                                                                   [31, 1],
        "RT_RELE_REGULADOR_HAB":                                                            [31, 2],
        "RT_RELE_REGULADOR_REGULANDO":                                                      [31, 3],
        "RT_RELE_HAB_DRIVE_EXCITACAO_LOGICA_DISPARO":                                       [31, 4],
        "RT_RELE_HAB_CONTATOR_CAMPO":                                                       [31, 5],
        "RT_RELE_HAB_PRE_EXCITACAO":                                                        [31, 6],
        "RT_RELE_HAB_CROWBAR":                                                              [31, 7],


        ## LIMITES_OPERAÇÃO
        "RT_LIM_SUP_CORRENTE_EXCITACAO":                                                    [32, 0],
        "RT_LIM_INF_CORRENTE_EXCITACAO":                                                    [32, 1],
        "RT_LIM_SUP_TENSAO_TERMINAL":                                                       [32, 2],
        "RT_LIM_INF_TENSAO_TERMINAL":                                                       [32, 3],
        "RT_LIM_SUP_POT_REATIVA":                                                           [32, 4],
        "RT_LIM_INF_POT_REATIVA":                                                           [32, 5],
        "RT_LIM_SUP_FATOR_DE_POT":                                                          [32, 10],
        "RT_LIM_INF_FATOR_DE_POT":                                                          [32, 11],
        "RT_LIM_VOLTZ_HERTZ":                                                               [32, 12],
        "RT_LIM_ABERTURA_PONTE":                                                            [32, 13],
        "RT_LIM_PQ_RELACAO_POT_ATIVA_POT_REATIVA":                                          [32, 14],


        ## LEITURAS_2
        "SETPOINT_TENSAO_PU":                                                               40,
        "SETPOINT_POT_REATIVA_KVAR":                                                        41,
        "SETPOINT_POT_REATIVA_PU":                                                          41,
        "SETPOINT_FATOR_POT_PU":                                                            42,
        "ABERTURA_PONTE":                                                                   43,
        "REF_CORRENTE_CAMPO_PU":                                                            46,
        "FEEDBACK_CORRENTE_CAMPO_PU":                                                       47,
        "REF_TENSAO_PU":                                                                    52,
        "FEEDBACK_TENSAO_PU":                                                               53,
        "REF_POT_REATIVA_PU":                                                               58,
        "FEEDBACK_POT_REATIVA_PU":                                                          59,
        "REF_FATOR_POT_PU":                                                                 64,
        "FEEDBACK_FATOR_POT_PU":                                                            65,


        ## ALARMES_1
        "RT_ALARME_SOBRETENSAO":                                                            [70, 0],
        "RT_ALARME_SUBTENSAO":                                                              [70, 1],
        "RT_ALARME_SOBREFREQUENCIA":                                                        [70, 2],
        "RT_ALARME_SUBFREQUENCIA":                                                          [70, 3],
        "RT_ALARME_LIM_SUP_POT_REATIVA":                                                    [70, 4],
        "RT_ALARME_LIM_INF_POT_REATIVA":                                                    [70, 5],
        "RT_ALARME_LIM_SUP_FATOR_DE_POT":                                                   [70, 6],
        "RT_ALARME_LIM_INF_FATOR_DE_POT":                                                   [70, 7],
        "RT_ALARME_VARIACAO_TENSAO":                                                        [70, 8],
        "RT_ALARME_POT_ATIVA_REVERSA":                                                      [70, 9],
        "RT_ALARME_SOBRECORRENTE_TERMINAL":                                                 [70, 10],
        "RT_ALARME_LIM_SUP_CORRENTE_EXCITACAO":                                             [70, 11],
        "RT_ALARME_LIM_INF_CORRENTE_EXCITACAO":                                             [70, 12],
        "RT_ALARME_TEMP_MUITO_ALTA_ROTOR":                                                  [70, 13],
        "RT_ALARME_PRES_TENSAO_TERMINAL_AUSENCIA_CORRENTE_EXCITACAO":                       [70, 14],
        "RT_ALARME_PRES_CORRENTE_EXCITACAO_AUXENCIA_TENSAO_TERMINAL":                       [70, 15],


        ## ALARMES_2
        "RT_ALARME_FALHA_CONTROLE_CORRENTE_EXCITACAO":                                      [71, 0],
        "RT_ALARME_FALHA_CONTROLE_TENSAO_TERMINAL":                                         [71, 1],
        "RT_ALARME_CROWBAR_ATUADO_REGULADOR_HABILITADO":                                    [71, 2],
        "RT_ALARME_FALHA_HAB_DRIVE_EXCITACAO":                                              [71, 3],
        "RT_ALARME_FALHA_FECHAR_CONTATOR_CAMPO":                                            [71, 4],
        "RT_ALARME_FALHA_CORRENTE_EXCITACAO_PRE_EXCITACAO_ATIVA":                           [71, 5],
        "RT_ALARME_PERDA_MED_POT_REATIVA":                                                  [71, 6],
        "RT_ALARME_PERDA_MED_TENSAO_TERMINAL":                                              [71, 7],
        "RT_ALARME_PERDA_MED_CORRENTE_EXCITACAO":                                           [71, 8],
        "RT_ALARME_RUIDO_INSTRU_REATIVO":                                                   [71, 9],
        "RT_ALARME_RUIDO_INSTRU_TENSAO":                                                    [71, 10],
        "RT_ALARME_RUIDO_INSTRU_EXCITACAO_PRINC":                                           [71, 11],
        "RT_ALARME_RUIDO_INSTRU_EXCITACAO_RETAG":                                           [71, 12],


        ## FALHAS_1
        "RT_FALHA_SOBRETENSAO":                                                             [72, 0],
        "RT_FALHA_SUBTENSAO":                                                               [72, 1],
        "RT_FALHA_SOBREFREQUENCIA":                                                         [72, 2],
        "RT_FALHA_SUBFREQUENCIA":                                                           [72, 3],
        "RT_FALHA_LIM_SUP_POT_REATIVA":                                                     [72, 4],
        "RT_FALHA_LIM_INF_POT_REATIVA":                                                     [72, 5],
        "RT_FALHA_LIM_SUP_FATOR_POT":                                                       [72, 6],
        "RT_FALHA_LIM_INF_FATOR_POT":                                                       [72, 7],
        "RT_FALHA_SOBRETENSAO_INSTAN":                                                      [72, 8],
        "RT_FALHA_VARIACAO_TENSAO":                                                         [72, 9],
        "RT_FALHA_POT_ATIVA_REVERSA":                                                       [72, 10],
        "RT_FALHA_SOBRECORRENTE_TERM":                                                      [72, 11],
        "RT_FALHA_LIM_SUP_CORRENTE_EXCITACAO":                                              [72, 12],
        "RT_FALHA_LIM_INF_CORRENTE_EXCITACAO":                                              [72, 13],
        "RT_FALHA_LIM_SUP_TENSAO_EXCITACAO":                                                [72, 14],
        "RT_FALHA_LIM_INF_TENSAO_EXCITACAO":                                                [72, 15],


        ## FALHAS_2
        "RT_FALHA_TEMP_MUITO_ALTA_ROTOR":                                                   [73, 0],
        "RT_FALHA_PRESENCA_TENSAO_TERMINAL_AUSENCIA_CORRENTE_EXCITACAO":                    [73, 1],
        "RT_FALHA_PRESENCA_CORRENTE_EXCITACAO_AUSENCIA_TENSAO_TERM":                        [73, 2],
        "RT_FALHA_CTRL_CORRENTE_EXCITACAO":                                                 [73, 3],
        "RT_FALHA_CTRL_TENSAO_TERMINAL":                                                    [73, 4],
        "RT_FALHA_CROWBAR_ATUADO_REGULADOR_HAB":                                            [73, 5],
        "RT_FALHA_HAB_DRIVE_EXCITACAO_LOGICA_DISPARO":                                      [73, 6],
        "RT_FALHA_FECHAR_CONTATOR_CAMPO":                                                   [73, 7],
        "RT_FALHA_CORRENTE_EXCITACAO_PRE_EXCITACAO_ATIVA":                                  [73, 8],
        "RT_FALHA_TEMPO_EXCESSIVO_PRE_EXCITACAO":                                           [73, 9],
        "RT_FALHA_TEMPO_EXCESSIVO_PARADA":                                                  [73, 10],
        "RT_FALHA_TEMPO_EXCESSIVO_PARTIDA":                                                 [73, 11],
        "RT_FALHA_BLOQ_EXTERNO":                                                            [73, 12],


        ## FALHAS_3
        "RT_FALHA_PERDA_MED_POT_REATIVA":                                                   [74, 0],
        "RT_FALHA_PERDA_MED_TENSAO_TERMINAL":                                               [74, 1],
        "RT_FALHA_PERDA_MED_CORRENTE_EXCITACAO_PRINC":                                      [74, 2],
        "RT_FALHA_PERDA_MED_CORRENTE_EXCITACAO_RETAG":                                      [74, 3],
        "RT_FALHA_RUIDO_INSTRU_REATIVO":                                                    [74, 4],
        "RT_FALHA_RUIDO_INSTRU_TENSAO":                                                     [74, 5],
        "RT_FALHA_RUIDO_INSTRU_EXCITACAO_PRINC":                                            [74, 6],
        "RT_FALHA_RUIDO_INSTRU_EXCITACAO_RETAG":                                            [74, 7],


        ## LEITURAS_3
        "TENSAO_NOMINAL":                                                                   85,
        "POT_APARENTE_NOMINAL":                                                             86,
        "CONTROLE_1":                                                                       90,
        "CONTROLE_2":                                                                       91,
    },

    "UG2":{
        ### RV
        ## LEITURAS_1
        "ROTACAO":                                                                          16,
        "ESTADO_OPERACAO":                                                                  21,
        "CRTL_SINCRONIZADO_SELEC":                                                          22,
        "CRTL_VAZIO_SELEC":                                                                 23,
        "CMD_MODBUS":                                                                       24,


        ## ENTRAS_DIGITAIS
        "RV_SEM_BLOQ_EXTERNO":                                                              [25, 0],
        "RV_HAB_REGULADOR":                                                                 [25, 1],
        "RV_SELEC_MODO_CTRL_ISOLADO":                                                       [25, 2],
        "RV_ZERA_CARGA":                                                                    [25, 3],
        "RV_RESET_FALHAS":                                                                  [25, 4],
        "RV_INCRE_REF_CTRL":                                                                [25, 5],
        "RV_DECRE_REF_CTRL":                                                                [25, 6],
        "RV_DJ_MAQUINA_FECHADO":                                                            [25, 7],


        ## SAÍDAS_DIGITAIS
        "RV_RELE_TRIP_NAO_ATUADO":                                                          [26, 0],
        "RV_RELE_ALARME":                                                                   [26, 1],
        "RV_RELE_REGULADOR_HAB":                                                            [26, 2],
        "RV_RELE_REGULADOR_REGULANDO":                                                      [26, 3],
        "RV_RELE_POT_NULA":                                                                 [26, 4],
        "RV_RELE_MAQUINA_PARADA":                                                           [26, 5],
        "RV_RELE_VELO_MENOR_30%":                                                           [26, 6],
        "RV_RELE_VELO_MAIOR_90%":                                                           [26, 7],
        "RV_RELE_DISTRI_ABERTO":                                                            [26, 8],


        ## LIMITES_OPERAÇÃO
        "RV_LIM_SUP_DISTRI_ATUADO":                                                         [27, 0],
        "RV_LIM_INF_DISTRI_ATUADO":                                                         [27, 1],
        "RV_LIM_SUP_ROTOR_ATUADO":                                                          [27, 2],
        "RV_LIM_INF_ROTOR_ATUADO":                                                          [27, 3],
        "RV_LIM_SUP_VELO_ATUADO":                                                           [27, 4],
        "RV_LIM_INF_VELO_ATUADO":                                                           [27, 5],
        "RV_LIM_SUP_POT_ATUADO":                                                            [27, 6],
        "RV_LIM_INF_POT_ATUADO":                                                            [27, 7],


        ## LEITURAS_2
        "SETPOINT_ABERTURA_PU":                                                             28,
        "SETPOINT_VELO":                                                                    29,
        "SETPOINT_POT_ATIVA_KW":                                                            30,
        "SETPOINT_POT_ATIVA_PU":                                                            30 + 3200,
        "SAIDA_CTRL_DISTRI":                                                                32,
        "SAIDA_CTRL_ROTOR":                                                                 33,
        "REF_DISTRI_PU":                                                                    36,
        "FEEDBACK_DISTRI_PU":                                                               37,
        "SAIDA_CTRL_DISTRI_PU":                                                             32,
        "REF_ROTOR_PU":                                                                     42,
        "FEEDBACK_ROTOR_PU":                                                                43,
        "SAIDA_CTRL_ROTOR_PU":                                                              33,
        "REF_VELO_PU":                                                                      48,
        "FEEDBACK_VELO_PU":                                                                 49,
        "REF_POT_ATIVA_PU":                                                                 54,
        "FEEDBACK_POT_ATIVA_PU":                                                            55,


        ## ALARME
        "RV_ALARME_SOBREFREQUENCIA":                                                        [66, 0],
        "RV_ALARME_SUBFREQUENCIA":                                                          [66, 1],
        "RV_ALARME_LEITURA_POS_DISTRI":                                                     [66, 2],
        "RV_ALARME_LEITURA_POS_ROTOR":                                                      [66, 3],
        "RV_ALARME_LEITURA_POT_ATIVA":                                                      [66, 4],
        "RV_ALARME_LEITURA_REF_POT":                                                        [66, 5],
        "RV_ALARME_LEITURA_NV_MONTANTE":                                                    [66, 6],
        "RV_ALARME_NV_MONTANTE_MUITO_BAIXO":                                                [66, 7],
        "RV_ALARME_CTRL_POS_DISTRI":                                                        [66, 8],
        "RV_ALARME_CTRL_POS_ROTOR":                                                         [66, 9],
        "RV_ALARME_RUIDO_MED_VELO_PRINC":                                                   [66, 10],
        "RV_ALARME_RUIDO_MED_VELO_RETAG":                                                   [66, 11],
        "RV_ALARME_PERDA_MED_VELO_PRINC":                                                   [66, 12],
        "RV_ALARME_PERDA_MED_VELO_RETAG":                                                   [66, 13],
        "RV_ALARME_DIF_MED_VELO_PRINC_RETAG":                                               [66, 14],


        ## FALHA_1
        "RV_FALHA_SOBREFREQUENCIA_INSTAN":                                                  [67, 0],
        "RV_FALHA_SOBREFREQUENCIA_TEMPO":                                                   [67, 1],
        "RV_FALHA_SUBFREQUENCIA_TEMPO":                                                     [67, 2],
        "RV_FALHA_GIRANDO_SEM_REG_GIRO_INDEVIDO":                                           [67, 3],
        "RV_FALHA_LEITURA_POS_DISTRI":                                                      [67, 4],
        "RV_FALHA_LEITURA_POS_ROTOR":                                                       [67, 5],
        "RV_FALHA_LEITURA_POT_ATIVA":                                                       [67, 6],
        "RV_FALHA_LEITURA_REF_POT":                                                         [67, 7],
        "RV_FALHA_LEITURA_NV_MONTANTE":                                                     [67, 8],
        "RV_FALHA_NV_MONTANTE_MUITO_BAIXO":                                                 [67, 10],
        "RV_FALHA_CTRL_POS_DISTRI":                                                         [67, 11],
        "RV_FALHA_CTRL_POS_ROTOR":                                                          [67, 12],
        "RV_FALHA_RUIDO_MED_VELO_PRINC":                                                    [67, 13],
        "RV_FALHA_RUIDO_MED_VELO_RETAG":                                                    [67, 14],
        "RV_FALHA_PERDA_MED_VELO_PRINC":                                                    [67, 15],


        ## FALHA_2
        "RV_FALHA_RUIDO_MED_VELO_RETAG":                                                    [68, 0],
        "RV_FALHA_TEMPO_EXCESSIVO_PARTIDA":                                                 [68, 1],
        "RV_FALHA_TEMPO_EXCESSIVO_PARADA":                                                  [68, 2],
        "RV_FALHA_BLOQ_EXTERNO":                                                            [68, 3],
        "RV_FALHA_DIF_MED_VELO_PRINC_RETAG":                                                [68, 4],


        ## LEITURAS_3
        "POT_APARENTE_NOMINAL":                                                             79,
        "POT_ATIVA_NOMINAL":                                                                80,
        "CTRL_1":                                                                           85,
        "CTRL_2":                                                                           86,
        "CONJ_DISTRI_1":                                                                    121,
        "CONJ_ROTOR_1":                                                                     122,
        "CONJ_DISTRI_2":                                                                    123,
        "CONJ_ROTOR_2":                                                                     124,
        "CONJ_DISTRI_3":                                                                    125,
        "CONJ_ROTOR_3":                                                                     126,
        "CONJ_DISTRI_4":                                                                    127,
        "CONJ_ROTOR_4":                                                                     128,
        "CONJ_DISTRI_5":                                                                    129,
        "CONJ_ROTOR_5":                                                                     130,
        "CONJ_DISTRI_6":                                                                    131,
        "CONJ_ROTOR_6":                                                                     132,
        "CONJ_DISTRI_7":                                                                    133,
        "CONJ_ROTOR_7":                                                                     134,
        "CONJ_DISTRI_8":                                                                    135,
        "CONJ_ROTOR_8":                                                                     136,
        "CONJ_DISTRI_9":                                                                    137,
        "CONJ_ROTOR_9":                                                                     138,
        "CONJ_DISTRI_10":                                                                   139,
        "CONJ_ROTOR_10":                                                                    140,
        "ABERTURA_MAX_DISTRI":                                                              182,
        "ABERTURA_MAX_DISTRI_VAZIO":                                                        184,
        "ABERTURA_MIN_DISTRI":                                                              183,
        "ABERTURA_MAX_ROTOR":                                                               185,
        "ABERTURA_MIN_ROTOR":                                                               186,
        "POTENCIA_MAX":                                                                     189,
        "POTENCIA_MIN":                                                                     190,



        ### RT
        ## LEITURAS_1
        "CORRENTE_EXCITACAO":                                                               16,
        "TENSAO_EXCITACAO":                                                                 17,
        "TEMP_ROTOR":                                                                       25,
        "ESTADO_OPERACAO":                                                                  26,
        "CTRL_SINCRONIZADO_SELEC":                                                          27,


        ## ENTRAS_DIGITAIS
        "RT_SEM_BLOQ_EXTERNO":                                                              [30, 0],
        "RT_HAB_REGULADOR":                                                                 [30, 1],
        "RT_SELEC_MODO_CTRL_ISOLADO":                                                       [30, 2],
        "RV_DRIVE_EXCITACAO_HAB_LOGICA_DISPARO":                                            [30, 3],
        "RV_RESET_FALHAS":                                                                  [30, 4],
        "RT_INCRE_REF_CTRL":                                                                [30, 5],
        "RT_DECRE_REF_CTRL":                                                                [30, 6],
        "RT_DJ_MAQUINA_FECHADO":                                                            [30, 7],
        "RT_CONTATOR_CAMPO_FECHADO":                                                        [30, 8],
        "RT_CROWBAR_INATIVO":                                                               [30, 9],


        ## SAIDAS_DIGITAIS
        "RT_RELE_TRIP_NAO_ATUADO":                                                          [31, 0],
        "RT_RELE_ALARME":                                                                   [31, 1],
        "RT_RELE_REGULADOR_HAB":                                                            [31, 2],
        "RT_RELE_REGULADOR_REGULANDO":                                                      [31, 3],
        "RT_RELE_HAB_DRIVE_EXCITACAO_LOGICA_DISPARO":                                       [31, 4],
        "RT_RELE_HAB_CONTATOR_CAMPO":                                                       [31, 5],
        "RT_RELE_HAB_PRE_EXCITACAO":                                                        [31, 6],
        "RT_RELE_HAB_CROWBAR":                                                              [31, 7],


        ## LIMITES_OPERAÇÃO
        "RT_LIM_SUP_CORRENTE_EXCITACAO":                                                    [32, 0],
        "RT_LIM_INF_CORRENTE_EXCITACAO":                                                    [32, 1],
        "RT_LIM_SUP_TENSAO_TERMINAL":                                                       [32, 2],
        "RT_LIM_INF_TENSAO_TERMINAL":                                                       [32, 3],
        "RT_LIM_SUP_POT_REATIVA":                                                           [32, 4],
        "RT_LIM_INF_POT_REATIVA":                                                           [32, 5],
        "RT_LIM_SUP_FATOR_DE_POT":                                                          [32, 10],
        "RT_LIM_INF_FATOR_DE_POT":                                                          [32, 11],
        "RT_LIM_VOLTZ_HERTZ":                                                               [32, 12],
        "RT_LIM_ABERTURA_PONTE":                                                            [32, 13],
        "RT_LIM_PQ_RELACAO_POT_ATIVA_POT_REATIVA":                                          [32, 14],


        ## LEITURAS_2
        "SETPOINT_TENSAO_PU":                                                               40,
        "SETPOINT_POT_REATIVA_KVAR":                                                        41,
        "SETPOINT_POT_REATIVA_PU":                                                          41,
        "SETPOINT_FATOR_POT_PU":                                                            42,
        "ABERTURA_PONTE":                                                                   43,
        "REF_CORRENTE_CAMPO_PU":                                                            46,
        "FEEDBACK_CORRENTE_CAMPO_PU":                                                       47,
        "REF_TENSAO_PU":                                                                    52,
        "FEEDBACK_TENSAO_PU":                                                               53,
        "REF_POT_REATIVA_PU":                                                               58,
        "FEEDBACK_POT_REATIVA_PU":                                                          59,
        "REF_FATOR_POT_PU":                                                                 64,
        "FEEDBACK_FATOR_POT_PU":                                                            65,


        ## ALARMES_1
        "RT_ALARME_SOBRETENSAO":                                                            [70, 0],
        "RT_ALARME_SUBTENSAO":                                                              [70, 1],
        "RT_ALARME_SOBREFREQUENCIA":                                                        [70, 2],
        "RT_ALARME_SUBFREQUENCIA":                                                          [70, 3],
        "RT_ALARME_LIM_SUP_POT_REATIVA":                                                    [70, 4],
        "RT_ALARME_LIM_INF_POT_REATIVA":                                                    [70, 5],
        "RT_ALARME_LIM_SUP_FATOR_DE_POT":                                                   [70, 6],
        "RT_ALARME_LIM_INF_FATOR_DE_POT":                                                   [70, 7],
        "RT_ALARME_VARIACAO_TENSAO":                                                        [70, 8],
        "RT_ALARME_POT_ATIVA_REVERSA":                                                      [70, 9],
        "RT_ALARME_SOBRECORRENTE_TERMINAL":                                                 [70, 10],
        "RT_ALARME_LIM_SUP_CORRENTE_EXCITACAO":                                             [70, 11],
        "RT_ALARME_LIM_INF_CORRENTE_EXCITACAO":                                             [70, 12],
        "RT_ALARME_TEMP_MUITO_ALTA_ROTOR":                                                  [70, 13],
        "RT_ALARME_PRES_TENSAO_TERMINAL_AUSENCIA_CORRENTE_EXCITACAO":                       [70, 14],
        "RT_ALARME_PRES_CORRENTE_EXCITACAO_AUXENCIA_TENSAO_TERMINAL":                       [70, 15],


        ## ALARMES_2
        "RT_ALARME_FALHA_CONTROLE_CORRENTE_EXCITACAO":                                      [71, 0],
        "RT_ALARME_FALHA_CONTROLE_TENSAO_TERMINAL":                                         [71, 1],
        "RT_ALARME_CROWBAR_ATUADO_REGULADOR_HABILITADO":                                    [71, 2],
        "RT_ALARME_FALHA_HAB_DRIVE_EXCITACAO":                                              [71, 3],
        "RT_ALARME_FALHA_FECHAR_CONTATOR_CAMPO":                                            [71, 4],
        "RT_ALARME_FALHA_CORRENTE_EXCITACAO_PRE_EXCITACAO_ATIVA":                           [71, 5],
        "RT_ALARME_PERDA_MED_POT_REATIVA":                                                  [71, 6],
        "RT_ALARME_PERDA_MED_TENSAO_TERMINAL":                                              [71, 7],
        "RT_ALARME_PERDA_MED_CORRENTE_EXCITACAO":                                           [71, 8],
        "RT_ALARME_RUIDO_INSTRU_REATIVO":                                                   [71, 9],
        "RT_ALARME_RUIDO_INSTRU_TENSAO":                                                    [71, 10],
        "RT_ALARME_RUIDO_INSTRU_EXCITACAO_PRINC":                                           [71, 11],
        "RT_ALARME_RUIDO_INSTRU_EXCITACAO_RETAG":                                           [71, 12],


        ## FALHAS_1
        "RT_FALHA_SOBRETENSAO":                                                             [72, 0],
        "RT_FALHA_SUBTENSAO":                                                               [72, 1],
        "RT_FALHA_SOBREFREQUENCIA":                                                         [72, 2],
        "RT_FALHA_SUBFREQUENCIA":                                                           [72, 3],
        "RT_FALHA_LIM_SUP_POT_REATIVA":                                                     [72, 4],
        "RT_FALHA_LIM_INF_POT_REATIVA":                                                     [72, 5],
        "RT_FALHA_LIM_SUP_FATOR_POT":                                                       [72, 6],
        "RT_FALHA_LIM_INF_FATOR_POT":                                                       [72, 7],
        "RT_FALHA_SOBRETENSAO_INSTAN":                                                      [72, 8],
        "RT_FALHA_VARIACAO_TENSAO":                                                         [72, 9],
        "RT_FALHA_POT_ATIVA_REVERSA":                                                       [72, 10],
        "RT_FALHA_SOBRECORRENTE_TERM":                                                      [72, 11],
        "RT_FALHA_LIM_SUP_CORRENTE_EXCITACAO":                                              [72, 12],
        "RT_FALHA_LIM_INF_CORRENTE_EXCITACAO":                                              [72, 13],
        "RT_FALHA_LIM_SUP_TENSAO_EXCITACAO":                                                [72, 14],
        "RT_FALHA_LIM_INF_TENSAO_EXCITACAO":                                                [72, 15],


        ## FALHAS_2
        "RT_FALHA_TEMP_MUITO_ALTA_ROTOR":                                                   [73, 0],
        "RT_FALHA_PRESENCA_TENSAO_TERMINAL_AUSENCIA_CORRENTE_EXCITACAO":                    [73, 1],
        "RT_FALHA_PRESENCA_CORRENTE_EXCITACAO_AUSENCIA_TENSAO_TERM":                        [73, 2],
        "RT_FALHA_CTRL_CORRENTE_EXCITACAO":                                                 [73, 3],
        "RT_FALHA_CTRL_TENSAO_TERMINAL":                                                    [73, 4],
        "RT_FALHA_CROWBAR_ATUADO_REGULADOR_HAB":                                            [73, 5],
        "RT_FALHA_HAB_DRIVE_EXCITACAO_LOGICA_DISPARO":                                      [73, 6],
        "RT_FALHA_FECHAR_CONTATOR_CAMPO":                                                   [73, 7],
        "RT_FALHA_CORRENTE_EXCITACAO_PRE_EXCITACAO_ATIVA":                                  [73, 8],
        "RT_FALHA_TEMPO_EXCESSIVO_PRE_EXCITACAO":                                           [73, 9],
        "RT_FALHA_TEMPO_EXCESSIVO_PARADA":                                                  [73, 10],
        "RT_FALHA_TEMPO_EXCESSIVO_PARTIDA":                                                 [73, 11],
        "RT_FALHA_BLOQ_EXTERNO":                                                            [73, 12],


        ## FALHAS_3
        "RT_FALHA_PERDA_MED_POT_REATIVA":                                                   [74, 0],
        "RT_FALHA_PERDA_MED_TENSAO_TERMINAL":                                               [74, 1],
        "RT_FALHA_PERDA_MED_CORRENTE_EXCITACAO_PRINC":                                      [74, 2],
        "RT_FALHA_PERDA_MED_CORRENTE_EXCITACAO_RETAG":                                      [74, 3],
        "RT_FALHA_RUIDO_INSTRU_REATIVO":                                                    [74, 4],
        "RT_FALHA_RUIDO_INSTRU_TENSAO":                                                     [74, 5],
        "RT_FALHA_RUIDO_INSTRU_EXCITACAO_PRINC":                                            [74, 6],
        "RT_FALHA_RUIDO_INSTRU_EXCITACAO_RETAG":                                            [74, 7],


        ## LEITURAS_3
        "TENSAO_NOMINAL":                                                                   85,
        "POT_APARENTE_NOMINAL":                                                             86,
        "CONTROLE_1":                                                                       90,
        "CONTROLE_2":                                                                       91,
    },
}