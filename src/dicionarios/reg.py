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

REG_SA = {
    ## COMANDOS DIGITAIS
    "SA_CD_CMD_SA_SE":                                  12288,       # Coil                                  (OP -> 0X05 Write Single Coil)
    "SA_CD_REARME_FALHAS":                              [12288, 0],  # Coil -> Bit 00                        (OP -> 0X05 Write Single Coil)
    "SA_CD_PD_BOMBA_1_PRINCIPAL":                       [12288, 2],  # Coil -> Bit 02                        (OP -> 0X05 Write Single Coil)
    "SA_CD_PD_BOMBA_2_PRINCIPAL":                       [12288, 3],  # Coil -> Bit 03                        (OP -> 0X05 Write Single Coil)
    "SA_CD_PE_BOMBA_1_LIGA":                            [12288, 5],  # Coil -> Bit 05                        (OP -> 0X05 Write Single Coil)
    "SA_CD_PE_BOMBA_2_LIGA":                            [12288, 6],  # Coil -> Bit 06                        (OP -> 0X05 Write Single Coil)
    "SA_CD_PE_BOMBA_1_DESLIGA":                         [12288, 7],  # Coil -> Bit 07                        (OP -> 0X05 Write Single Coil)
    "SA_CD_DISJ_TSA_ABRE":                              [12288, 13], # Coil -> Bit 13                        (OP -> 0X05 Write Single Coil)
    "SA_CD_DISJ_TSA_FECHA":                             [12288, 14], # Coil -> Bit 14                        (OP -> 0X05 Write Single Coil)
    "SA_CD_DISJ_GMG_ABRE":                              [12288, 15], # Coil -> Bit 15                        (OP -> 0X05 Write Single Coil)
    "SA_CD_DISJ_GMG_FECHA":                             [12288, 16], # Coil -> Bit 16                        (OP -> 0X05 Write Single Coil)
    "SA_CD_DISJ_LINHA_ABRE":                            [12288, 18], # Coil -> Bit 18                        (OP -> 0X05 Write Single Coil)
    "SA_CD_DISJ_LINHA_FECHA":                           [12288, 17], # Coil -> Bit 17                        (OP -> 0X05 Write Single Coil)
    "SA_CD_SF_MANUAL":                                  [12288, 19], # Coil -> Bit 19                        (OP -> 0X05 Write Single Coil)
    "SA_CD_SF_AUTOMATICO":                              [12288, 20], # Coil -> Bit 20                        (OP -> 0X05 Write Single Coil)
    "SA_CD_SF_COMUTA_ELEMENTO":                         [12288, 21], # Coil -> Bit 21                        (OP -> 0X05 Write Single Coil)
    "SA_CD_SF_BLOQUEIA_COMUTACAO_ELEMENTO":             [12288, 22], # Coil -> Bit 22                        (OP -> 0X05 Write Single Coil)
    "SA_CD_SF_DESBLOQUEIA_COMUTACAO_ELEMENTO":          [12288, 23], # Coil -> Bit 22                        (OP -> 0X05 Write Single Coil)

    ## ENTRADAS ANALÓGICAS
    # ALARMES\NÍVEIS
    "SA_EA_STT_ALARMES_HH_ANALOGICAS":                  12340,       # Input Register                       (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_NIVEL_JUSANTE_MUITO_ALTO":               [12340, 0],  # Input Register -> Bit 00             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_NIVEL_MONTANTE_MUITO_ALTO":              [12340, 1],  # Input Register -> Bit 01             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_NIVEL_JUSANTE_2_MUITO_ALTO":             [12340, 2],  # Input Register -> Bit 02             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_ALTO":      [12340, 3],  # Input Register -> Bit 03             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_ALTO":       [12340, 4],  # Input Register -> Bit 04             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_ALTO":      [12340, 5],  # Input Register -> Bit 05             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_ALTO":       [12340, 6],  # Input Register -> Bit 06             (OP -> 0x04 Read Input Registers)

    "SA_EA_STT_ALARMES_H_ANALOGICAS":                   12342,       # Input Register                       (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_NIVEL_JUSANTE_ALTO":                     [12342, 0],  # Input Register -> Bit 00             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_NIVEL_MONTANTE_ALTO":                    [12342, 1],  # Input Register -> Bit 01             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_NIVEL_JUSANTE_2_ALTO":                   [12342, 2],  # Input Register -> Bit 02             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_ALTO":            [12342, 3],  # Input Register -> Bit 03             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_ALTO":             [12342, 4],  # Input Register -> Bit 04             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_ALTO":            [12342, 5],  # Input Register -> Bit 05             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_ALTO":             [12342, 6],  # Input Register -> Bit 06             (OP -> 0x04 Read Input Registers)

    "SA_EA_STT_ALARMES_L_ANALOGICAS":                   12344,       # Input Register                       (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_NIVEL_JUSANTE_BAIXO":                    [12344, 0],  # Input Register -> Bit 00             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_NIVEL_MONTANTE_BAIXO":                   [12344, 1],  # Input Register -> Bit 01             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_NIVEL_JUSANTE_2_BAIXO":                  [12344, 2],  # Input Register -> Bit 02             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_BAIXO":           [12344, 3],  # Input Register -> Bit 03             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_BAIXO":            [12344, 4],  # Input Register -> Bit 04             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_BAIXO":           [12344, 5],  # Input Register -> Bit 05             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_BAIXO":            [12344, 6],  # Input Register -> Bit 06             (OP -> 0x04 Read Input Registers)

    "SA_EA_STT_ALARMES_LL_ANALOGICAS":                  12346,       # Input Register                       (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_NIVEL_JUSANTE_MUITO_BAIXO":              [12346, 0],  # Input Register -> Bit 00             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_NIVEL_MONTANTE_MUITO_BAIXO":             [12346, 1],  # Input Register -> Bit 01             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_NIVEL_JUSANTE_2_MUITO_BAIXO":            [12346, 2],  # Input Register -> Bit 02             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_MUITO_BAIXO":     [12346, 3],  # Input Register -> Bit 03             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_MUITO_BAIXO":      [12346, 4],  # Input Register -> Bit 04             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_MUITO_BAIXO":     [12346, 5],  # Input Register -> Bit 05             (OP -> 0x04 Read Input Registers)
    "SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_MUITO_BAIXO":      [12346, 6],  # Input Register -> Bit 06             (OP -> 0x04 Read Input Registers)


    # FALHAS\NÍVEIS
    "SA_EA_STT_FALHAS_ANALOGICAS":                      12338,      # Input Register                        (OP -> 0x04 Read input Registers)
    "SA_EA_PSA_NIVEL_MONTANTE_FALHA_LEITURA":           [12338, 0], # Input Register -> Bit 00              (OP -> 0x04 Read input Registers)
    "SA_EA_PSA_NIVEL_JUSANTE_FALHA_LEITURA":            [12338, 1], # Input Register -> Bit 01              (OP -> 0x04 Read input Registers)
    "SA_EA_PSA_SFA_PRESSAO_LADO_LIMPO_FALHA_LEITURA":   [12338, 2], # Input Register -> Bit 02              (OP -> 0x04 Read input Registers)
    "SA_EA_PSA_SFA_PRESSAO_LADO_SUJO_FALHA_LEITURA":    [12338, 3], # Input Register -> Bit 03              (OP -> 0x04 Read input Registers)
    "SA_EA_PSA_SFB_PRESSAO_LADO_LIMPO_FALHA_LEITURA":   [12338, 4], # Input Register -> Bit 04              (OP -> 0x04 Read input Registers)
    "SA_EA_PSA_SFB_PRESSAO_LADO_SUJO_FALHA_LEITURA":    [12338, 5], # Input Register -> Bit 05              (OP -> 0x04 Read input Registers)
    "SA_EA_PSA_NIVEL_JUSANTE_2_FALHA_LEITURA":          [12338, 6], # Input Register -> Bit 06              (OP -> 0x04 Read input Registers)

    # LEITURAS\NÍVEIS
    "SA_EA_NIVEL_JUSANTE_CASA_FORCA":                   12448,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "SA_EA_NIVEL_MONTANTE_TA":                          12448,      # Input Register -477.23                (OP -> 0x04 Read Input Registers)

    # LEITURAS\PRESSÃO
    "SA_EA_SFA_LADO_LIMPO":                             12500,      # Input Register                        (OP -> 0X04 Read Input Registers)
    "SA_EA_SFA_LADO_SUJO":                              12502,      # Input Register                        (OP -> 0X04 Read Input Registers)
    "SA_EA_SFB_LADO_LIMPO":                             12504,      # Input Register                        (OP -> 0X04 Read Input Registers)
    "SA_EA_SFB_LADO_SUJO":                              12506,      # Input Register                        (OP -> 0X04 Read Input Registers)

    ## ENTRADAS DIGITAIS
    # BLOQUEIOS
    "SA_ED_STT_BLOQUEIO_50BF":                          12350,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "SA_ED_BLOQUEIO_50BF_ATUADO":                       [12350, 31],# Holding Register                      (OP -> 0x03 Read Holding Registers)

    "SA_ED_STT_BLOQUEIO_86BTLSA":                       12352,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "SA_ED_BLOQUEIO_86BTLSA_ATUADO":                    [12352, 31],# Holding Register                      (OP -> 0x03 Read Holding Registers)

    # ENTRADAS CLP
    "SA_ED_STT_ENTRADAS_DIGITAIS_0":                    12308,      # Holding Register                      (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_BOTAO_REARME_FALHAS_PAINEL":             [12308, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_BOTAO_BLOQUEIO_86BTBF":                  [12308, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_DRENAGEM_BOMBA_1_AUTO":             [12308, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_DRENAGEM_BOMBA_2_AUTO":             [12308, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_DISJUNTORES_MODO_REMOTO":                [12308, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_DISJ_TSA_TRIP":                          [12308, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_DISJ_GMG_TRIP":                          [12308, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_RELE_BLOQUEIO_86BTBF":                   [12308, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_CARREGADOR_BATERIAS_FALHA":              [12308, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_CONVERSOR_FIBRA_FALHA":                  [12308, 9], # Holding Register -> Bit 09            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SUPERVISOR_TENSAO_FALHA":                [12308, 10],# Holding Register -> Bit 10            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_DPS_TSA":                                [12308, 11],# Holding Register -> Bit 11            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_DPS_GMG":                                [12308, 12],# Holding Register -> Bit 12            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_DRENAGEM_BOMBA_1_DEFEITO":          [12308, 13],# Holding Register -> Bit 13            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_DRENAGEM_BOMBA_1_LIGADA":           [12308, 14],# Holding Register -> Bit 14            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_DRENAGEM_BOMBA_2_DEFEITO":          [12308, 15],# Holding Register -> Bit 15            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_DRENAGEM_BOMBA_2_LIGADA":           [12309, 16],# Holding Register -> Bit 16            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_ESGOTAMENTO_BOMBA_1_DEFEITO":       [12309, 17],# Holding Register -> Bit 17            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_ESGOTAMENTO_BOMBA_1_LIGADA":        [12309, 18],# Holding Register -> Bit 18            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_ESGOTAMENTO_BOMBA_2_DEFEITO":       [12309, 19],# Holding Register -> Bit 19            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_ESGOTAMENTO_BOMBA_2_LIGADA":        [12309, 20],# Holding Register -> Bit 20            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_BAIXO": [12309, 21],# Holding Register -> Bit 21            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_DESL_BOMBAS": [12309, 22],# Holding Register -> Bit 22            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_LIGA_BOMBA":  [12309, 23],# Holding Register -> Bit 23            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_ALTO":        [12309, 24],# Holding Register -> Bit 24            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_POCO_DRENAGEM_SENSOR_NIVEL_MUITO_ALTO":  [12309, 25],# Holding Register -> Bit 25            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_DIJS_TSA_FECHADO":                       [12309, 26],# Holding Register -> Bit 26            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_DIJS_GMG_FECHADO":                       [12309, 27],# Holding Register -> Bit 27            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SUPERVISOR_TENSAO_TSA_FALHA":            [12309, 28],# Holding Register -> Bit 28            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SUPERVISOR_TENSAO_GMG_FALHA":            [12309, 29],# Holding Register -> Bit 29            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_TRAFO_ELEVADOR_TEMP_MUITO_ALTA":         [12309, 30],# Holding Register -> Bit 30            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SE_DISJ_LINHA_FECHADO":                  [12309, 31],# Holding Register -> Bit 31            (OP -> 0x03 Read holding Registers)

    "SA_ED_STT_ENTRADAS_DIGITAIS_1":                    12310,      # Holding Register                      (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SE_DISJ_LINHA_ABERTO":                   [12310, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_TE_TEMPERATURA_MUIT_ALTA":               [12310, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_TE_PRESSAO_MUITO_ALTA":                  [12310, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_OLEO_MUITO_BAIXO":                       [12310, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_PRTVA1_50BF":                            [12310, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_PRTVA2_50BF":                            [12310, 6], # Holding Register -> Bit 04            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SFA_ENTRADA_ELEMENTO_1_ABERTA":          [12310, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SFA_ENTRADA_ELEMENTO_2_ABERTA":          [12310, 9], # Holding Register -> Bit 08            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SFA_LIMPEZA_ELEMENTO_2_ABERTA":          [12310, 10],# Holding Register -> Bit 10            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SFA_LIMPEZA_ELEMENTO_1_ABERTA":          [12310, 11],# Holding Register -> Bit 11            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SFA_SFB_PRESSAO_SAIDA":                  [12310, 12],# Holding Register -> Bit 12            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SFB_ENTRADA_ELEMENTO_1_ABERTA":          [12310, 13],# Holding Register -> Bit 13            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SFB_ENTRADA_ELEMENTO_2_ABERTA":          [12310, 14],# Holding Register -> Bit 14            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SFB_LIMPEZA_ELEMENTO_2_ABERTA":          [12310, 15],# Holding Register -> Bit 15            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SFB_LIMPEZA_ELEMENTO_1_ABERTA":          [12310, 16],# Holding Register -> Bit 16            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SE_RELE_LINHA_TRIP":                     [12310, 17],# Holding Register -> Bit 17            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SE_RELE_LINHA_FALHA":                    [12310, 18],# Holding Register -> Bit 18            (OP -> 0x03 Read holding Registers)
    "SA_ED_PSA_SE_RELE_LINHA_50BF":                     [12310, 19],# Holding Register -> Bit 19            (OP -> 0x03 Read holding Registers)


    "SA_ED_STT_ENTRADAS_DIGITAIS_2":                    12312,      # Holding Register                      (OP -> 0x03 Read holding Registers)

    # SA_SE
    "SA_ED_STT_SA_SE":                                  12348,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_DREANGEM_BOMBA_1_INDISP":                [12348, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_DREANGEM_BOMBA_2_INDISP":                [12348, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_DREANGEM_BOMBA_1_PRINCIPAL":             [12348, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_DREANGEM_BOMBA_2_PRINCIPAL":             [12348, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_DREANGEM_BOIAS_DISCREPANCIA":            [12348, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_ESGOTAMENTO_BOMBA_1_INDISP":             [12348, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_ESGOTAMENTO_BOMBA_2_INDISP":             [12348, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_ESGOTAMENTO_BOMBA_1_FALHA":              [12348, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_ESGOTAMENTO_BOMBA_2_FALHA":              [12348, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_GMG_DISJ_FALHA_FECHAR":                  [12348, 9], # Holding Register -> Bit 09            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_GMG_DISJ_FALHA_ABRIR":                   [12348, 10],# Holding Register -> Bit 10            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_TSA_DISJ_FALHA_FECHAR":                  [12348, 11],# Holding Register -> Bit 11            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_TSA_DISJ_FALHA_ABRIR":                   [12348, 12],# Holding Register -> Bit 12            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SE_DISJ_FALHA_FECHAR":                   [12348, 13],# Holding Register -> Bit 13            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SE_DISJ_FALHA_ABRIR":                    [12348, 14],# Holding Register -> Bit 14            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SFA_ELEMENTO_OPERANDO":                  [12348, 15],# Holding Register -> Bit 15            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SFA_ELEMENTO_LIMPEZA":                   [12348, 16],# Holding Register -> Bit 16            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SFB_ELEMENTO_LIMPEZA":                   [12348, 17],# Holding Register -> Bit 17            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SFB_ELEMENTO_OPERANDO":                  [12348, 18],# Holding Register -> Bit 18            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SFA_FALHA_ABRIR_ENTRADA_ELEM":           [12348, 19],# Holding Register -> Bit 19            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SFA_FALHA_FECHAR_ENTRADA_ELEM":          [12348, 20],# Holding Register -> Bit 20            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SFB_FALHA_ABRIR_ENTRADA_ELEM":           [12348, 21],# Holding Register -> Bit 21            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SFB_FALHA_FECHAR_ENTRADA_ELEM":          [12348, 22],# Holding Register -> Bit 22            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SFA_FALHA_ABRIR_RETROLAVAGEM":           [12348, 23],# Holding Register -> Bit 23            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SFA_FALHA_FECHAR_RETROLAVAGEM":          [12348, 24],# Holding Register -> Bit 24            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SFB_FALHA_ABRIR_RETROLAVAGEM":           [12348, 25],# Holding Register -> Bit 25            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SFB_FALHA_FECHAR_RETROLAVAGEM":          [12348, 26],# Holding Register -> Bit 26            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SF_COMUTACAO_ELEMENTO_MANUAL":           [12348, 27],# Holding Register -> Bit 27            (OP -> 0x03 Read Holding Registers)
    "SA_ED_PSA_SF_COMUTACAO_ELEMENTO_BLOQUEIO":         [12348, 28],# Holding Register -> Bit 28            (OP -> 0x03 Read Holding Registers)


    # SF
    "SA_ED_REAL_STT_SFA":                               12508,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

}

REG_UG ={
    ## COMANDOS ANALOGICOS
    # CONTROLE NÍVEL
    "UG1_CA_SETPOINT_NIVEL_5":                          12588,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CA_SETPOINT_NIVEL_4":                          12590,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CA_SETPOINT_NIVEL_3":                          12592,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CA_SETPOINT_NIVEL_2":                          12594,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CA_SETPOINT_NIVEL_1":                          12596,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CA_SETPOINT_NIVEL_PARADA":                     12598,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CA_POTENCIA_5":                                12600,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CA_POTENCIA_4":                                12602,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CA_POTENCIA_3":                                12604,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CA_POTENCIA_2":                                12606,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CA_POTENCIA_1":                                12608,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CA_SETPOINT_MINIMO_POTENCIA":                  12610,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CA_SETPOINT_MAXIMO_POTENCIA":                  12612,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CA_SETPOINT_NIVEL":                            12616,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CA_SETPOINT_MINIMO_OPERACAO":                  12618,      # Coil                                  (OP -> 0x15 Write Multiple Coils)

    ## COMANDOS DIGITAIS
    "UG1_CD_CMD_UG1":                                   12288,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_REARME_FALHAS":                         [12288, 0], # Coil -> Bit 00                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_PARADA_EMERGENCIA":                     [12288, 1], # Coil -> Bit 01                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_CONTROLE_NIVEL":                        [12288, 2], # Coil -> Bit 02                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_CONTROLE_POTENCIA_MANUAL":              [12288, 3], # Coil -> Bit 03                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_CONTROLE_POTENCIA_POR NIVEL":           [12288, 4], # Coil -> Bit 04                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_CONTROLE_PARADA_NIVEL_HABILITA":        [12288, 5], # Coil -> Bit 05                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_CONTROLE_PARADA_NIVEL_DESABILITA":      [12288, 6], # Coil -> Bit 06                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_RV_MANUTENCAO":                         [12288, 10],# Coil -> Bit 10                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_RV_AUTOMATICO":                         [12288, 11],# Coil -> Bit 11                        (OP -> 0x15 Write Multiple Coils)

    "UG1_CD_CMD_UHRV":                                  12292,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_UHRV_MODO_AUTOMATICO":                  [12292, 0], # Coil -> Bit 00                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_UHRV_MODO_MANUTENCAO":                  [12292, 1], # Coil -> Bit 01                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_UHRV_BOMBA_1_LIGA":                     [12292, 2], # Coil -> Bit 02                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_UHRV_BOMBA_1_DESLIGA":                  [12292, 3], # Coil -> Bit 03                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_UHRV_BOMBA_2_LIGA":                     [12292, 4], # Coil -> Bit 04                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_UHRV_BOMBA_2_DESLIGA":                  [12292, 5], # Coil -> Bit 05                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_UHRV_BOMBA_1_PRINCIPAL":                [12292, 6], # Coil -> Bit 06                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_UHRV_BOMBA_2_PRINCIPAL":                [12292, 7], # Coil -> Bit 07                        (OP -> 0x15 Write Multiple Coils)

    "UG1_CD_CMD_UHLM":                                  12294,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_UHLM_MODO_AUTOMATICO":                  [12294, 0], # Coil -> Bit 00                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_UHLM_MODO_MANUTENCAO":                  [12294, 1], # Coil -> Bit 01                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_UHLM_BOMBA_1_LIGA":                     [12294, 2], # Coil -> Bit 02                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_UHLM_BOMBA_1_DESLIGA":                  [12294, 3], # Coil -> Bit 03                        (OP -> 0x15 Write Multiple Coils)

    "UG1_CD_CMD_PARTIDA_PARADA":                        12290,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_PARADA_TOTAL":                          [12290, 0], # Coil -> Bit 00                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_ATE_UHRV":                              [12290, 1], # Coil -> Bit 01                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_ATE_UHLM":                              [12290, 2], # Coil -> Bit 02                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_ATE_BORBOLETA":                         [12290, 5], # Coil -> Bit 05                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_ATE_RV":                                [12290, 7], # Coil -> Bit 07                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_ATE_RT":                                [12290, 8], # Coil -> Bit 08                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_SINCRONISMO":                           [12290, 9], # Coil -> Bit 09                        (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_ATE_FILTRAGEM":                         [12290, 10],# Coil -> Bit 10                        (OP -> 0x15 Write Multiple Coils)

    ## ENTRADAS ANALÓGICAS
    # ALARMES\PRESSÃO
    "UG1_EA_STT_ALARMES_HH_ANALOGICAS":                 12340,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_UHRV_PRESSAO_OLEO_MUITO_ALTO":              [12340, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG1_EA_SINAL_NIVEL_JUSANTE_MUITO_ALTO":            [12340, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)

    "UG1_EA_STT_ALARMES_H_ANALOGICAS":                  12342,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_UHRV_PRESSAO_OLEO_ALTO":                    [12342, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG1_EA_SINAL_NIVEL_JUSANTE_ALTO":                  [12342, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)

    "UG1_EA_STT_ALARMES_L_ANALOGICAS":                  12344,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_UHRV_PRESSAO_OLEO_BAIXA":                   [12344, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG1_EA_SINAL_NIVEL_JUSANTE_BAIXA":                 [12344, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)

    "UG1_EA_STT_ALARMES_LL_ANALOGICAS":                 12346,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_UHRV_PRESSAO_OLEO_MUITO_BAIXA":             [12346, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG1_EA_SINAL_NIVEL_JUSANTE_MUITO_BAIXA":           [12346, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)

    # ALARMES\TEMPERATURA
    "UG1_EA_STT_ALARMES_HH_TEMPERATURA":                12330,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TRISTORES_TEMP_MUITO_ALTA":                 [12330, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG1_EA_CROWBAR_TEMP_MUITO_ALTA":                   [12330, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)
    "UG1_EA_TRAFO_EXCITACAO_MUITO_ALTA":                [12330, 2], # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers)
    "UG1_EA_UHRV_TEMP_OLEO_MUITO_ALTA":                 [12330, 3], # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_FASE_A_TEMP_MUITO_ALTA":            [12330, 4], # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_FASE_B_TEMP_MUITO_ALTA":            [12330, 7], # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_FASE_C_TEMP_MUITO_ALTA":            [12330, 8], # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_NUCLEO_1_TEMP_MUITO_ALTA":          [12330, 9], # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_NUCLEO_2_MUITO_ALTA":               [12330, 10],# Input Register -> Bit 10              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_NUCLEO_3_TEMP_MUITO_ALTA":          [12330, 11],# Input Register -> Bit 11              (OP -> 0x04 Read Input Registers)
    "UG1_EA_MANCAL_GUIA_CASQUILHO_MUITO_ALTA":          [12330, 12],# Input Register -> Bit 12              (OP -> 0x04 Read Input Registers)
    "UG1_EA_MANCAL_COMBINADO_CASQUILHO_MUITO_ALTA":     [12330, 13],# Input Register -> Bit 13              (OP -> 0x04 Read Input Registers)
    "UG1_EA_MANCAL_COMBINADO_ESCORA_MUITO_ALTA":        [12330, 14],# Input Register -> Bit 14              (OP -> 0x04 Read Input Registers)

    "UG1_EA_STT_ALARMES_H_TEMPERATURA":                 12332,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TRISTORES_TEMP_ALTA":                       [12332, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG1_EA_CROWBAR_TEMP_ALTA":                         [12332, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)
    "UG1_EA_TRAFO_EXCITACAO_ALTA":                      [12332, 2], # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers)
    "UG1_EA_UHRV_TEMP_OLEO_ALTA":                       [12332, 3], # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_FASE_A_TEMP_ALTA":                  [12332, 4], # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_FASE_B_TEMP_ALTA":                  [12332, 7], # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_FASE_C_TEMP_ALTA":                  [12332, 8], # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_NUCLEO_1_TEMP_ALTA":                [12332, 9], # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_NUCLEO_2_ALTA":                     [12332, 10],# Input Register -> Bit 10              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_NUCLEO_3_TEMP_ALTA":                [12332, 11],# Input Register -> Bit 11              (OP -> 0x04 Read Input Registers)
    "UG1_EA_MANCAL_GUIA_CASQUILHO_ALTA":                [12332, 12],# Input Register -> Bit 12              (OP -> 0x04 Read Input Registers)
    "UG1_EA_MANCAL_COMBINADO_CASQUILHO_ALTA":           [12332, 13],# Input Register -> Bit 13              (OP -> 0x04 Read Input Registers)
    "UG1_EA_MANCAL_COMBINADO_ESCORA_ALTA":              [12332, 14],# Input Register -> Bit 14              (OP -> 0x04 Read Input Registers)

    # FALHAS\PRESSÃO
    "UG1_EA_STT_FALHAS_ANALOGICAS":                     12338,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_UHRV_PRESSAO_OLEO_FALHA_LEITURA":           [12338, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG1_EA_SINAL_NIVEL_JUSANTE_FALHA_LEITURA":         [12338, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)

    # FALHAS\TEMPERATURA
    "UG1_EA_STT_FALHAS_TEMPERATURA":                    12328,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TRISTORES_TEMP_FALHA_LEITURA":              [12328, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG1_EA_CROWBAR_TEMP_FALHA_LEITURA":                [12328, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)
    "UG1_EA_TRAFO_EXCITACAO_FALHA_LEITURA":             [12328, 2], # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers)
    "UG1_EA_UHRV_TEMP_OLEO_FALHA_LEITURA":              [12328, 3], # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA":         [12328, 4], # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA":         [12328, 7], # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA":         [12328, 8], # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA":       [12328, 9], # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_NUCLEO_2_FALHA_LEITURA":            [12328, 10],# Input Register -> Bit 10              (OP -> 0x04 Read Input Registers)
    "UG1_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA":       [12328, 11],# Input Register -> Bit 11              (OP -> 0x04 Read Input Registers)
    "UG1_EA_MANCAL_GUIA_CASQUILHO_FALHA_LEITURA":       [12328, 12],# Input Register -> Bit 12              (OP -> 0x04 Read Input Registers)
    "UG1_EA_MANCAL_COMBINADO_CASQUILHO_FALHA_LEITURA":  [12328, 13],# Input Register -> Bit 13              (OP -> 0x04 Read Input Registers)
    "UG1_EA_MANCAL_COMBINADO_ESCORA_FALHA_LEITURA":     [12328, 14],# Input Register -> Bit 14              (OP -> 0x04 Read Input Registers)

    # LEITURAS\TEMPERATURAS
    "UG1_EA_TEMPERATURA_PONTE_TRISTORES":               12488,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TEMPERATURA_CROWBAR":                       12490,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TEMPERATURA_OLEO_UHRV":                     12492,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TEMPERATURA_OLEO_UHLM":                     12494,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TEMPERATURA_GERADOR_FASE_A":                12496,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TEMPERATURA_GERADOR_FASE_B":                12498,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TEMPERATURA_GERADOR_FASE_C":                12500,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TEMPERATURA_GERADOR_NUCLEO_1":              12502,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TEMPERATURA_GERADOR_NUCLEO_2":              12504,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TEMPERATURA_GERADOR_NUCLEO_3":              12506,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TEMPERATURA_MANCAL_GUIA_CASQUILHO":         12508,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TEMPERATURA_MANCAL_COMBINADO_CASQUILHO":    12510,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TEMPERATURA_MANCAL_COMBINADO_ESCORA":       12512,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TEMPERATURA_MANCAL_COMBINADO_CONTRA_ESCORA":12514,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_TEMPERATURA_TRAFO_EXCITACAO":               12518,      # Input Register                        (OP -> 0x04 Read Input Registers)

    # LEITURAS\PRESSÕES
    "UG1_EA_PRESSAO_OLEO_UHRV":                         12522,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_NIVEL_JUSANTE":                             12524,      # Input Register                        (OP -> 0x04 Read Input Registers)

    # LEITURAS\VIBRACOES
    "UG1_EA_VIBRACAO_EIXO_X_GUIA":                      12526,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_VIBRACAO_EIXO_X_COMBINADO":                 12528,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_VIBRACAO_EIXO_Y_COMBINADO":                 12530,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_VIBRACAO_EIXO_Z_COMBINADO":                 12532,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_VIBRACAO_EIXO_Y_GUIA":                      12534,      # Input Register                        (OP -> 0x04 Read Input Registers)

    ## ENTRADAS DIGITAIS
    # BLOQUEIOS
    "UG1_ED_STT_BLOQUEIO_86M":                          12428,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BLOQUEIO_86M_ATUADO":                       [12428, 31],# Holding Register -> Bit 31            (OP -> 0x03 Read Holding Registers)

    "UG1_ED_STT_BLOQUEIO_86E":                          12430,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BLOQUEIO_86E_ATUADO":                       [12430, 31],# Holding Register -> Bit 31            (OP -> 0x03 Read Holding Registers)

    "UG1_ED_STT_BLOQUEIO_86H":                          12432,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BLOQUEIO_86E_ATUADO":                       [12430, 31],# Holding Register -> Bit 31            (OP -> 0x03 Read Holding Registers)

    # BORBOLETA
    "UG1_ED_REAL_ESTADO_BORBOLETA":                     12614,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    "UG1_ED_STT_BORBOLETA":                             12414,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BROBOLETA_FALHA_ABRIR":                     [12414, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BORBOLETA_FALHA_FECHAR":                    [12414, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BORBOLETA_ABRINDO":                         [12414, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BORBOLETA_FECHANDO":                        [12414, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BYPASS_ABRINDO":                            [12414, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BYPASS_FECHANDO":                           [12414, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BYPASS_FALHA_ABRIR":                        [12414, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BYPASS_FALHA_FECHAR":                       [12414, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BORBOLETA_DISCREPANCIA_SENSORES":           [12414, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BYPASS_DISCREPANCIA_SENSORES":              [12414, 9], # Holding Register -> Bit 09            (OP -> 0x03 Read Holding Registers)

    # ENTRADAS CLP
    "UG1_ED_STT_ENTRADAS_DIGITAIS_0":                   12308,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    "UG1_ED_STT_ENTRADAS_DIGITAIS_1":                   12310,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_BOTAO_BLOQUEIO_86EH":                 [12310, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_REARME_FALHAS":                       [12310, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_BOTAO_PARA_UG":                       [12310, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_BOTAO_PARTE_UG":                      [12310, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_BOTAO_DIMINUI_REFERENCIA_RV":         [12310, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_BOTAO_AUMENTA_REFERENCIA_RV":         [12310, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_BOTAO_DIMINUI_REFERENCIA_RT":         [12310, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_BOTAO_AUMENTA_REFERENCIA_RT":         [12310, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RELE_PROT_GERADOR_FALHA":             [12310, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RELE_PROT_GERADOR_TRIP":              [12310, 9], # Holding Register -> Bit 09            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RELE_PROT_GERADOR_50BF":              [12310, 10],# Holding Register -> Bit 10            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RV_TRIP":                             [12310, 11],# Holding Register -> Bit 11            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RV_ALARME":                           [12310, 12],# Holding Register -> Bit 12            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RV_HABILITADO":                       [12310, 13],# Holding Register -> Bit 13            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RV_REGULANDO":                        [12310, 14],# Holding Register -> Bit 14            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RV_POTENCIA_NULA":                    [12310, 15],# Holding Register -> Bit 15            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RV_MAQUINA_PARADA":                   [12310, 16],# Holding Register -> Bit 16            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RV_VELOCIDADE_MENOR":                 [12310, 17],# Holding Register -> Bit 17            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RV_VELOCIDADE_MAIOR":                 [12310, 18],# Holding Register -> Bit 18            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RV_DISTRIBUIDOR_ABERTO":              [12310, 19],# Holding Register -> Bit 19            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RT_TRIP":                             [12310, 20],# Holding Register -> Bit 20            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RT_ALARME":                           [12310, 21],# Holding Register -> Bit 21            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RT_HABILITADO":                       [12310, 22],# Holding Register -> Bit 22            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RT_REGULANDO":                        [12310, 23],# Holding Register -> Bit 23            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_CONTATOR_CAMPO_FECHADO":              [12310, 24],# Holding Register -> Bit 24            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_DISJUNTOR_MAQUINA_FECHADO":           [12310, 25],# Holding Register -> Bit 25            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RELE_BLOQUEIO_86EH":                  [12310, 26],# Holding Register -> Bit 26            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_SUPERVISAO_DE_TENSAO_ENTRADA_CA":     [12310, 27],# Holding Register -> Bit 27            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_DISPOSITIVO_PROTECAO_SURTO":          [12310, 28],# Holding Register -> Bit 28            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_UHRV_BOMBA_DEFEITO":                  [12310, 29],# Holding Register -> Bit 29            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_UHRV_BOMBA_LIGADA":                   [12310, 30],# Holding Register -> Bit 30            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_UHLM_BOMBA_DEFEITO":                  [12310, 31],# Holding Register -> Bit 31            (OP -> 0x03 Read Holding Registers)

    "UG1_ED_STT_ENTRADAS_DIGITAIS_2":                   12312,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_UHLM_BOMBA_LIGADA":                   [12312, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_ACIONAMENTO_RESERVA_DEFEITO":         [12312, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_ACIONAMENTO_RESERVA_LIGADO":          [12312, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RESISTENCIA_AQUEC_GERADOR_DEFEITO":   [12312, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_RESISTENCIA_AQUEC_GERADOR_LIGADA":    [12312, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_DISJUNTOR_TPS_PROTECAO":              [12312, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_DISJUNTOR_TPS_SINCRO":                [12312, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_UHRV_OLEO_NIVEL_MUITO_BAIXO":         [12312, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_UHRV_FILTRO_OLEO_SUJO":               [12312, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_UHRV_PRESSAO_CRITICA":                [12312, 9], # Holding Register -> Bit 09            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_UHRV_PRESSAO_FREIO":                  [12312, 10],# Holding Register -> Bit 10            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_UHLM_OLEO_NIVEL_MUITO_ALTO":          [12312, 12],# Holding Register -> Bit 12            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_UHLM_OLEO_NIVEL_MUITO_BAIXO":         [12312, 13],# Holding Register -> Bit 13            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_UHLM_PRESSAO_LINHA_LUBRIFICACAO":     [12312, 14],# Holding Register -> Bit 14            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_UHLM_FILTRO_OLEO_SUJO":               [12312, 15],# Holding Register -> Bit 15            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_UHLM_FLUXO_TROCADOR_CALOR":           [12312, 16],# Holding Register -> Bit 16            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_QBAG_ESCOVA_POLO_POSITIVO_DESGASTADA":[12312, 18],# Holding Register -> Bit 18            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_QBAG_ESCOVA_POLO_NEGATICO_DESGASTADA":[12312, 19],# Holding Register -> Bit 19            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_PSA_BLOQUEIO_86BTBF":                 [12312, 20],# Holding Register -> Bit 20            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_PSA_POCO_DRENAGEM_NIVEL_MUITO_ALTO":  [12312, 21],# Holding Register -> Bit 21            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_PSA_FILTRAGEM_PRESSAO_SAIDA":         [12312, 22],# Holding Register -> Bit 22            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_PSA_DISJUNTOR_LINHA_FECHADO":         [12312, 23],# Holding Register -> Bit 23            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_VB_VALVULA_BORBOLETA_ABERTA":         [12312, 28],# Holding Register -> Bit 28            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_VB_VALVULA_BORBOLETA_FECHADA":        [12312, 29],# Holding Register -> Bit 29            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_VB_VALVULA_BYPASS_ABERTA":            [12312, 30],# Holding Register -> Bit 30            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PRTVA_VB_VALVULA_BYPASS_FECHADA":           [12312, 31],# Holding Register -> Bit 31            (OP -> 0x03 Read Holding Registers)

    "UG1_ED_STT_ENTRADAS_DIGITAIS_3":                   12314,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_STT_ENTRADAS_DIGITAIS_4":                   12316,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # PARTIDA E PARADA
    "UG1_ED_STT_PASSO_SELECIONADO_BIT":                 12390,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_STT_PASSO_ATUAL_BIT":                       12392,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    "UG1_ED_STT_PASSO_ATUAL":                           12366,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHRV_PASSO_ATUAL":                          [12366, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHLM_PASSO_ATUAL":                          [12366, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_FILTRAGEM_PASSO_ATUAL":                     [12366, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BORBOLETA_PASSO_ATUAL":                     [12366, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RV_PASSO_ATUAL":                            [12366, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RT_PASSO_ATUAL":                            [12366, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_SINCRONISMO_PASSO_ATUAL":                   [12366, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_OPERANDO_PASSO_ATUAL":                      [12366, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PARADA_EMERGENCIA_PASSO_ATUAL":             [12366, 9], # Holding Register -> Bit 09            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PARADA_PARCIAL_PASSO_ATUAL":                [12366, 10],# Holding Register -> Bit 10            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PARADA_SEM_REJEICAO_PASSO_ATUAL":           [12366, 11],# Holding Register -> Bit 11            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PARADA_PASSO_A_PASSO_PASSO_ATUAL":          [12366, 12],# Holding Register -> Bit 12            (OP -> 0x03 Read Holding Registers)

    "UG1_ED_STT_PASSO_CONCLUIDO":                       12368,      # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PARDA_TOTAL_PASSO_CONCLUIDO":               [12368, 0], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_URHV_PASSO_CONCLUIDO":                      [12368, 1], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHLM_PASSO_CONCLUIDO":                      [12368, 2], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_FILTRAGEM_PASSO_CONCLUIDO":                 [12368, 3], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BORBOLETA_PASSO_CONCLUIDO":                 [12368, 4], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RV_PASSO_CONCLUIDO":                        [12368, 5], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RT_PASSO_CONCLUIDO":                        [12368, 6], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_SINCRONISMO_PASSO_CONCLUIDO":               [12368, 7], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)

    "UG1_ED_STT_PASSO_FALHA":                           12370,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHRV_PASSO_FALHA":                          [12370, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_FRIO_PASSO_FALHA":                          [12370, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHLM_PASSO_FALHA":                          [12370, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_FILTRAGEM_PASSO_FALHA":                     [12370, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BORBOLETA_PASSO_FALHA":                     [12370, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RV_PASSO_FALHA":                            [12370, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RT_PASSO_FALHA":                            [12370, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_SINCRONIZAR_PASSO_FALHA":                   [12370, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)

    "UG1_ED_STT_PASSO_SELECIONADO":                     12372,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_PARADA_TOTAL":                              [12372, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHRV":                                      [12372, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHLM":                                      [12372, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_FILTRAGEM":                                 [12372, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_BORBOLETA":                                 [12372, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RV":                                        [12372, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RT":                                        [12372, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_SINCRONISMO":                               [12372, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)

    "UG1_ED_STT_REAL_ESTADO_UNIDADE":                   12374,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_STT_REAL_PASSO_ATUAL":                      12376,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # PERMISSIVOS
    "UG1_ED_STT_PRE_CONDICOES_PARTIDA":                 12408,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # RT
    "UG1_ED_STT_RT":                                    12350,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RT_FALHA_AO_HABILITAR":                     [12350, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RT_FALHA_AO_PARTIR":                        [12350, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RT_FALHA_AO_DESABILITAR":                   [12350, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)

    # RV
    "UG1_ED_STT_RV":                                    12360,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RV_FALHA_AO_HABILITAR":                     [12360, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RV_FALHA_AO_PARTIR":                        [12360, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RV_FALHA_AO_DESABILITAR":                   [12360, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RV_FALHA_AO_PARAR_MAQUINA":                 [12360, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR":           [12360, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RV_MODO_MANUTENCAO":                        [12360, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)

    # UNIDADE GERADORA
    "UG1_ED_STT_UNIDADE_GERADORA":                      12348,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_CONTROLE_POTENCIA_NIVEL_HABILITADO":        [12348, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_CONTROLE_NIVEL_HABILITADO":                 [12348, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_CONTROLE_POTENCIA_MANUAL_HABILITADO":       [12348, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_CONTROLE_PARADA_NIVEL_HABILITADO":          [12348, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_CONTROLE_PARADA_NIVEL_BAIXO":               [12348, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_CONTROLE_FALHA_SENSOR_NIVEL":               [12348, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_CONTROLE_ALARME_DIFERENCIAL_GRADE":         [12348, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_CONTROLE_TRIP_DIFERENCIAL_GRADE":           [12348, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RESISTENCIA_AQUEC_GERADOR_INDISPONIVEL":    [12348, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR":     [12348, 9], # Holding Register -> Bit 09            (OP -> 0x03 Read Holding Registers)
    "UG1_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_DESLIGAR":  [12348, 10],# Holding Register -> Bit 10            (OP -> 0x03 Read Holding Registers)

    # UHLM
    "UG1_ED_STT_UHLM":                                  12354,      # Holding Reggister                     (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHLM_UNIDADE_MANUTENCAO":                   [12354, 0], # Holding Reggister -> Bit 00           (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHLM_BOMBA_1_INDISPONIVEL":                 [12354, 1], # Holding Reggister -> Bit 01           (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHLM_BOMBA_1_FALHA_LIGAR":                  [12354, 5], # Holding Reggister -> Bit 05           (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHLM_BOMBA_1_FALHA_DESLIGAR":               [12354, 6], # Holding Reggister -> Bit 06           (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHLM_BOMBA_1_FALHA_PRESSURIZAR":            [12354, 9], # Holding Reggister -> Bit 09           (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHLM_FILTRO_SUJO":                          [12354, 12],# Holding Reggister -> Bit 10           (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHLM_FALHA_PRESSOSTATO":                    [12354, 13],# Holding Reggister -> Bit 13           (OP -> 0x03 Read Holding Registers)

    # UHRV
    "UG1_ED_STT_UHRV":                                  12362,      # Holding Reggister                     (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHRV_UNIDADE_MANUTENCAO":                   [12362, 0], # Holding Reggister -> Bit 00           (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHRV_UNIDADE_HABILITADA":                   [12362, 1], # Holding Reggister -> Bit 01           (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHRV_INDISPONIVEL":                         [12362, 2], # Holding Reggister -> Bit 02           (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHRV_FALHA_AO_LIGAR":                       [12362, 6], # Holding Reggister -> Bit 06           (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHRV_FALHA_AO_DESLIGAR":                    [12362, 7], # Holding Reggister -> Bit 07           (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHRV_FALHA_AO_PRESSURIZAR":                 [12362, 10],# Holding Reggister -> Bit 10           (OP -> 0x03 Read Holding Registers)
    "UG1_ED_UHRV_FILTRO_OLEO_SUJO":                     [12362, 13],# Holding Reggister -> Bit 13           (OP -> 0x03 Read Holding Registers)

    ## DRIVER RV
    "UG1_RV_ROTACAO":                                   16,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)

    "UG1_RV_ESTADO_OPERACAO":                           21,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    # "UG1_RV_ESTADO_OPERACAO" -> PROCESSANDO = 00
    # "UG1_RV_ESTADO_OPERACAO" -> PARADA FINALIZADA = 01
    # "UG1_RV_ESTADO_OPERACAO" -> INICIO PARTIDA = 02
    # "UG1_RV_ESTADO_OPERACAO" -> PRIMEIRO ESTAGIO PARTIDA = 03
    # "UG1_RV_ESTADO_OPERACAO" -> SEGUNDO ESTAGIO PARTIDA = 04
    # "UG1_RV_ESTADO_OPERACAO" -> CONTROLANDO ABERTURA = 5
    # "UG1_RV_ESTADO_OPERACAO" -> CONTROLANDO VELOCIDADE = 6
    # "UG1_RV_ESTADO_OPERACAO" -> CONTROLANDO EM DROOP = 7
    # "UG1_RV_ESTADO_OPERACAO" -> CONTROLANDO EM DROOP EXTERNO = 8
    # "UG1_RV_ESTADO_OPERACAO" -> CONTROLANDO POTENCIA = 9
    # "UG1_RV_ESTADO_OPERACAO" -> CONTROLANDO POTENCIA POR REFERENCIA ANALOGICA = 10
    # "UG1_RV_ESTADO_OPERACAO" -> CONTROLANDO NIVEL = 11
    # "UG1_RV_ESTADO_OPERACAO" -> ZERANDO CARGA = 12
    # "UG1_RV_ESTADO_OPERACAO" -> PARANDO = 13
    # "UG1_RV_ESTADO_OPERACAO" -> CONTROLE MANUAL DISTRIBUIDOR = 14
    # "UG1_RV_ESTADO_OPERACAO" -> CONTROLE MANUAL ROTOR = 15
    # "UG1_RV_ESTADO_OPERACAO" -> EMERGENCIA = 16

    "UG1_RV_CONTROLE_SINCRONIZADO_SELECIONADO":         22,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONTROLE_VAZIO_SELECIONADO":                23,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_COMANDO_MODBUS":                            24,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SETPOINT_POTENCIA_ATIVA_PU":                30,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)


    # DIGITAIS
    "UG1_RV_ENTRADAS_DIGITAIS":                         25,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ED_SEN_BLOQUEIIO_EXTERNO":                  [25, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ED_HABILITA_REGULADOR":                     [25, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ED_SELEC_MODO_CONTROLE_ISOLADO":            [25, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ED_ZERA_CARGA":                             [25, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ED_RESET_FALHAS":                           [25, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ED_INCREMENTA_REF_CONTROLE":                [25, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ED_DECREMENTA_REFERENCIA_CONTROLE":         [25, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ED_DISJ_MAQUINA_FECHADO":                   [25, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)

    # RELE
    "UG1_RV_SAIDAS_DIGIAIS":                            26,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SD_RELE_TRIP_NAO_ATUADO":                   [26, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SD_RELE_ALARME":                            [26, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SD_RELE_REGULADOR_HABILITADO":              [26, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SD_RELE_REGULADOR_REGULANDO":               [26, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SD_RELE_POTENCIA_NULA":                     [26, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SD_RELE_MAQUINA_PARADA":                    [26, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SD_RELE_VELOC_MENOR_30":                    [26, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SD_RELE_VELOC_MAIOR_90":                    [26, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SD_RELE_DISTRIBUIDOR_ABERTO":               [26, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SD_RELE_SAIDA_PROGRAMAVEL":                 [26, 9],    # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers - 3x)

    # LIMITES
    "UG1_RV_LIMITES_OPERACAO":                          27,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_LIMITADOR_SUPERIOR_DISTRI_ATUADO":          [27, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_LIMITADOR_INFERIOR_DISTRI_ATUADO":          [27, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_LIMITADOR_SUPERIOR_ROTOR_ATUADO":           [27, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_LIMITADOR_INFERIOR_ROTOR_ATUADO":           [27, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_LIMITADOR_SUPERIOR_VELOC_ATUADO":           [27, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_LIMITADOR_INFERIOR_VELOC_ATUADO":           [27, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_LIMITADOR_SUPERIOR_POTENCIA_ATUADO":        [27, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_LIMITADOR_INFERIOR_POTENCIA_ATUADO":        [27, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)

    # ALARMES
    "UG1_RV_ALARME":                                    66,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME_SOBREFREQUENCIA":                    [66, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME_SUBFREQUENCIA":                      [66, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME_LEIT_POS_DISTRIBUIDOR":              [66, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME_LEIT_POS_ROTOR":                     [66, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME_LEIT_POS_POTENCIA_ATIVA":            [66, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME_LEIT_POS_NV_MONTANTE":               [66, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME_LEIT_POS_NV_MONTANTE_MUITO_BAIXO":   [66, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME_CONTR_POS_DISTRIBUIDOR":             [66, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME_CONTR_POS_ROTOR":                    [66, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME_RUIDO_MED_VELOCIDADE_PRINCIPAL":     [66, 9],    # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME_RUIDO_MED_VELOCIDADE_RETAGUARDA":    [66, 10],   # Input Register -> Bit 10              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME_PERDA_MED_VELOC_PRINCIPAL":          [66, 11],   # Input Register -> Bit 11              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME_PERDA_MED_VELOC_RETAGUARDA":         [66, 12],   # Input Register -> Bit 12              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME_DIF_MED_VELOCIDADE_PRINCIPAL":       [66, 13],   # Input Register -> Bit 13              (OP -> 0x04 Read Input Registers - 3x)

    # FALHAS
    "UG1_RV_FALHA_1":                                   67,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_SOBREFREQ_INSTANT":                 [67, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_SOBREFREQ_TEMPOR":                  [67, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_SUBFREQ_TEMPORIZADA":               [67, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_GIRANDO_SEM_REG_GIRO_INDEV":        [67, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_LEIT_POS_DISTRIBUIDOR":             [67, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_LEIT_POS_ROTOR":                    [67, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_LEIT_POTENCIA_ATIVA":               [67, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_LEIT_REFERENCIA_POTENCIA":          [67, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_LEIT_NV_MONTANTE":                  [67, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_NV_MONTANTE_MUITO_BAIXO":           [67, 10],   # Input Register -> Bit 10              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_CONTROLE_POS_DISTRIBUIDOR":         [67, 11],   # Input Register -> Bit 11              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_CONTROLE_POS_ROTOR":                [67, 12],   # Input Register -> Bit 12              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_RUIDO_MED_VELOC_PRINCIPAL":         [67, 13],   # Input Register -> Bit 13              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_RUIDO_MED_VELOC_RETAGUARDA":        [67, 14],   # Input Register -> Bit 14              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1_PERDA_MED_VELOC_PRINCIPAL":         [67, 15],   # Input Register -> Bit 15              (OP -> 0x04 Read Input Registers - 3x)

    "UG1_RV_FALHA_2":                                   68,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_2_PERDA_MED_VELOC_RETAGUARDA":        [68, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_2_TEMPO_EXCESSIVO_PARTIDA":           [68, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_2_TEMPO_EXCESSIVO_PARADA":            [68, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_2_BLOQUEIO_EXTERNO":                  [68, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_2_DIF_MED_VELO_PRINCIPAL_RETAGUARDA": [68, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)

    "UG1_RV_POTENCIA_APARENTE_NOMINAL":                 79,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_POTENCIA_ATIVA_NOMINAL":                    80,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONTROLE_1":                                85,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONTROLE_2":                                86,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_DISTRIBUIDOR_1":                  121,        # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_ROTOR_1":                         122,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_DISTRIBUIDOR_2":                  123,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_ROTOR_2":                         124,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_DISTRIBUIDOR_3":                  125,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_ROTOR_3":                         126,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_DISTRIBUIDOR_4":                  127,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_ROTOR_4":                         128,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_DISTRIBUIDOR_5":                  129,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_ROTOR_5":                         130,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_DISTRIBUIDOR_6":                  131,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_ROTOR_6":                         132,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_DISTRIBUIDOR_7":                  133,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_ROTOR_7":                         134,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_DISTRIBUIDOR_8":                  135,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_ROTOR_8":                         136,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_DISTRIBUIDOR_9":                  137,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_ROTOR_9":                         138,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_DISTRIBUIDOR_10":                 139,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONJUGADO_ROTOR_10":                        140,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ABERTURA_MAXIMA_DISTRIBUIDOR":              182,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ABERTURA_MINIMA_DISTRIBUIDOR":              183,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ABERTURA_MAXIMA_DISTRIBUIDOR_A_VAZIO":      184,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ABERTURA_MAXIMA_ROTOR":                     185,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ABERTURA_MINIMA_ROTOR":                     186,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_POTENCIA_MAXIMA":                           189,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_POTENCIA_MINIMA":                           190,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)

    ## DRIVER RT
    "UG1_RT_CORRENTE_EXCITACAO":                        16,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_TENSAO_EXCITACAO":                          17,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_TEMPERATURA_ROTOR":                         25,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)

    "UG1_RT_ESTADO_OPERACAO":                           26,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    # "UG1_RT_ESTADO_OPERACAO" -> PROCESSANDO = 00
    # "UG1_RT_ESTADO_OPERACAO" -> PARADA FINALIZADA = 01
    # "UG1_RT_ESTADO_OPERACAO" -> INICIO PARTIDA = 02
    # "UG1_RT_ESTADO_OPERACAO" -> PRIMEIRO ESTAGIO PARTIDA = 03
    # "UG1_RT_ESTADO_OPERACAO" -> SEGUNDO ESTAGIO PARTIDA = 04
    # "UG1_RT_ESTADO_OPERACAO" -> CONTROLANDO ABERTURA = 5
    # "UG1_RT_ESTADO_OPERACAO" -> CONTROLANDO VELOCIDADE = 6
    # "UG1_RT_ESTADO_OPERACAO" -> CONTROLANDO EM DROOP = 7
    # "UG1_RT_ESTADO_OPERACAO" -> CONTROLANDO EM DROOP EXTERNO = 8
    # "UG1_RT_ESTADO_OPERACAO" -> CONTROLANDO POTENCIA = 9
    # "UG1_RT_ESTADO_OPERACAO" -> CONTROLANDO POTENCIA POR REFERENCIA ANALOGICA = 10
    # "UG1_RT_ESTADO_OPERACAO" -> CONTROLANDO NIVEL = 11
    # "UG1_RT_ESTADO_OPERACAO" -> ZERANDO CARGA = 12
    # "UG1_RT_ESTADO_OPERACAO" -> PARANDO = 13
    # "UG1_RT_ESTADO_OPERACAO" -> CONTROLE MANUAL DISTRIBUIDOR = 14
    # "UG1_RT_ESTADO_OPERACAO" -> CONTROLE MANUAL ROTOR = 15
    # "UG1_RT_ESTADO_OPERACAO" -> EMERGENCIA = 16

    "UG1_RT_CONTROLE_SINCRONIZADO_SELECIONADO":         27,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)

    "UG1_RT_ENTRADAS_DIGITAIS":                         30,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ED_SEM_BLOQUEIO_EXTERNO":                   [30, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ED_HABILITA_REGULADOR":                     [30, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ED_SELEC_MODO_CONTROLE_ISOLADO":            [30, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ED_DRIVE_EXCITACAO_HABILITADO":             [30, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ED_RESET_FALHAS":                           [30, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ED_INCREMENTA_REF_CONTROLE":                [30, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ED_DECREMENTA_REF_CONTROLE":                [30, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ED_DISJ_MAQUINA_FECHADO":                   [30, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ED_CONTATOR_CAMPO_FECHADO":                 [30, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ED_CROWBAR_INATIVO":                        [30, 9],    # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers - 3x)

    "UG1_RT_SAIDAS_DIGITAIS":                           31,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_SD_RELE_TRIP_NAO_ATUADO":                   [31, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_SD_RELE_ALARME":                            [31, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_SD_RELE_REGULADOR_HABILITADO":              [31, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_SD_RELE_REGULADOR_REGULANDO":               [31, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_SD_RELE_HABILITA_DRIVE_EXCITACAO":          [31, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_SD_RELE_HABILITA_CONTATOR_CAMPO":           [31, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_SD_RELE_HABILITA_PRE_EXCITACAO":            [31, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_SD_RELE_HABILITA_CROWBAR":                  [31, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)

    "UG1_RT_LIMITES_OPERACAO":                          32,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_LIMITADOR_SUP_CORRENTE_EXCITACAO":          [32, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_LIMITADOR_INF_CORRENTE_EXCITACAO":          [32, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_LIMITADOR_SUP_TENSAO_TERMINAL":             [32, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_LIMITADOR_INF_TENSAO_TERMINAL":             [32, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_LIMITADOR_SUP_POTENCIA_REATIVA":            [32, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_LIMITADOR_INF_POTENCIA_REATIVA":            [32, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_LIMITADOR_SUP_FATOR_POTENCIA":              [32, 10],   # Input Register -> Bit 10              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_LIMITADOR_INF_FATOR_POTENCIA":              [32, 11],   # Input Register -> Bit 11              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_LIMITADOR_VOLTZ_HERTZ":                     [32, 12],   # Input Register -> Bit 12              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_LIMITADOR_ABERTURA_PONTE":                  [32, 13],   # Input Register -> Bit 13              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_LIMITADOR_PQ":                              [32, 14],   # Input Register -> Bit 14              (OP -> 0x04 Read Input Registers - 3x)

    "UG1_RT_SETPOINT_TENSAO_PU":                        40,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_SETPOINT_POTENCIA_REATIVA_PU":              41,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_SETPOINT_FATOR_POTENCIA_PU":                42,         # Input Register Scale -1               (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ABERTURA_PONTE":                            43,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_REFERENCIA_CORRENTE_CAMPO_PU":              46,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FEEDBACK_CORRENTE_CAMPO_PU":                47,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_REFERENCIA_TENSAO_PU":                      52,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FEEDBACK_TENSAO_PU":                        53,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_REFERENCIA_POTENCIA_REATIVA_PU":            58,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FEEDBACK_POTENCIA_REATIVA_PU":              59,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_REFERENCIA_FATOR_POTENCIA_PU":              64,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FEEDBACK_FATOR_POTENCIA_PU":                65,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)

    # ALARMES
    "UG1_RT_ALARMES_1":                                 70,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_SOBRETENSAO":                     [70, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_SUBTENSAO":                       [70, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_SOBREFREQUENCIA":                 [70, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_SUBFREQUENCIA":                   [70, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_LIMITE_SUP_POT_REATICA":          [70, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_LIMITE_INF_POT_REATIAVA":         [70, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_LIMITE_SUP_FATOR_POTENCIA":       [70, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_LIMITE_INF_FATOR_POTENCIA":       [70, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_VARIACAO_TENSAO":                 [70, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_POTENCIA_ATIVA_REVERSA":          [70, 9],    # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_SOBRECORRENTE_TERMINAL":          [70, 10],   # Input Register -> Bit 10              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_LIMITE_SUP_CORRENTE_EXCITACAO":   [70, 11],   # Input Register -> Bit 11              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_LIMITE_INF_CORRENTE_EXCITACAO":   [70, 12],   # Input Register -> Bit 12              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_TEMP_MUITO_ALTA_ROTOR":           [70, 13],   # Input Register -> Bit 13              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_PRES_TENS_TERM_AUSEN_CORR_EXCI":  [70, 14],   # Input Register -> Bit 14              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_1_PRES_CORR_EXCI_AUSEN_TENS_TERM":  [70, 15],   # Input Register -> Bit 15              (OP -> 0x04 Read Input Registers - 3x)

    "UG1_RT_ALARMES_2":                                 71,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_2_FALHA_CONTROLE_CORRENTE_EXCI":    [71, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_2_FALHA_CONTROLE_TENSAO_TERM":      [71, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_2_CROWBAR_ATUADO_REGUL_HABIL":      [71, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_2_FALHA_HABIL_DRIVE_EXCI":          [71, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_2_FALHA_FECHAR_CONTATOR_CAMPO":     [71, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_2_FALHA_CORR_EXCI_PRE_EXCI_ATIVA":  [71, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_2_PERDA_MEDICAO_POTENCIA_REATIVA":  [71, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_2_PERDA_MEDICAO_TENSAO_TERMINAL":   [71, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_2_PERDA_MEDICAO_CORRENTE_EXCI":     [71, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_2_RUIDO_INSTRUMEN_REATIVO":         [71, 9],    # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_2_RUIDO_INSTRUMEN_TENSAO":          [71, 10],   # Input Register -> Bit 10              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_2_RUIDO_INSTRUMEN_EXCI_PRINCI":     [71, 11],   # Input Register -> Bit 11              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_2_RUIDO_INSTRUMEN_EXCI_RETAG":      [71, 12],   # Input Register -> Bit 12              (OP -> 0x04 Read Input Registers - 3x)

    "UG1_RT_FALHAS_1":                                  72,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_SOBRETENSAO":                      [72, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_SUBTENSAO":                        [72, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_SOBREFREQUENCIA":                  [72, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_SUBFREQUENCIA":                    [72, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_LIMITE_SUP_POT_REATIVA":           [72, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_LIMITE_INF_POT_REATIVA":           [72, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_LIMITE_SUP_FATOR_POT":             [72, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_LIMITE_INF_FATOR_POT":             [72, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_SOBRETENSAO_INST":                 [72, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_VARIACAO_TENSAO":                  [72, 9],    # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_POT_ATIVA_REVERSA":                [72, 10],   # Input Register -> Bit 10              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_SOBRECORRENTE_TERMINAL":           [72, 11],   # Input Register -> Bit 11              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_LIMITE_SUP_CORRENTE_EXCITACAO":    [72, 12],   # Input Register -> Bit 12              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_LIMITE_INF_CORRENTE_EXCITACAO":    [72, 13],   # Input Register -> Bit 13              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_LIMITE_SUP_TENSAO_EXCITACAO":      [72, 14],   # Input Register -> Bit 14              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1_LIMITE_INF_TENSAO_EXCITACAO":      [72, 15],   # Input Register -> Bit 15              (OP -> 0x04 Read Input Registers - 3x)

    "UG1_RT_FALHAS_2":                                  73,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_2_TEMP_MUITO_ALTA_ROTOR":            [73, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_2_PRES_TENS_TERM_AUSEN_CORR_EXCI":   [73, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_2_PRES_CORR_EXCI_AUSEN_TENS_TERM":   [73, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_2_CONTROLE_CORR_EXCI":               [73, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_2_TENSAO_TERMINAL":                  [73, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_2_CROWBAR_ATUADO_REGULADOR_HABI":    [73, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_2_HABI_DRIVE_EXCITACAO":             [73, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_2_FECHAR_CONTATOR_CAMPO":            [73, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_2_CORR_EXCITA_PRE_EXCXITA_ATIVA":    [73, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_2_EXCESSIVO_PRE_EXCITACAO":          [73, 9],    # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_2_EXCESSIVO_PARADA":                 [73, 10],   # Input Register -> Bit 10              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_2_EXCESSIVO_PARTIDA":                [73, 11],   # Input Register -> Bit 11              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_2_BLOQ_EXTERNO":                     [73, 12],   # Input Register -> Bit 12              (OP -> 0x04 Read Input Registers - 3x)

    "UG1_RT_FALHAS_3":                                  74,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_3_PERDA_MED_POT_REATIVA":            [74, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_3_PERDA_MED_TENSAO_TERM":            [74, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_3_PERDA_MED_CORR_EXCI_PRINCI":       [74, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_3_PERDA_MED_CORR_EXCI_RETAG":        [74, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_3_RUIDO_INSTRUM_REATIVO":            [74, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_3_RUIDO_INSTRUM_TENSAO":             [74, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_3_RUIDO_INSTRUM_PRINCI":             [74, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_3_RUIDO_INSTRUM_RETAG":              [74, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)

    "UG1_RT_TENSAO_NOMINAL":                            85,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_POTENCIA_APARENTE_NOMINAL":                 86,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_CONTROLE_1":                                90,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_CONTROLE_2":                                91,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)


    ### UG2
    ## COMANDOS ANALOGICOS
    # CONTROLE NÍVEL
    "UG2_CA_SETPOINT_NIVEL_5":                          12588,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CA_SETPOINT_NIVEL_4":                          12590,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CA_SETPOINT_NIVEL_3":                          12592,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CA_SETPOINT_NIVEL_2":                          12594,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CA_SETPOINT_NIVEL_1":                          12596,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CA_SETPOINT_NIVEL_PARADA":                     12598,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CA_POTENCIA_5":                                12600,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CA_POTENCIA_4":                                12602,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CA_POTENCIA_3":                                12604,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CA_POTENCIA_2":                                12606,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CA_POTENCIA_1":                                12608,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CA_SETPOINT_MINIMO_POTENCIA":                  12610,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CA_SETPOINT_MAXIMO_POTENCIA":                  12612,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CA_SETPOINT_NIVEL":                            12616,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CA_SETPOINT_MINIMO_OPERACAO":                  12618,      # Coil                                  (OP -> 0x15 Write Multiple Coils)

    ## COMANDOS DIGITAIS
    "UG2_CD_CMD_UG2":                                   12288,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_REARME_FALHAS":                         [12288, 0], # Coil -> Bit 00                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_PARADA_EMERGENCIA":                     [12288, 1], # Coil -> Bit 01                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_CONTROLE_NIVEL":                        [12288, 2], # Coil -> Bit 02                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_CONTROLE_POTENCIA_MANUAL":              [12288, 3], # Coil -> Bit 03                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_CONTROLE_POTENCIA_POR NIVEL":           [12288, 4], # Coil -> Bit 04                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_CONTROLE_PARADA_NIVEL_HABILITA":        [12288, 5], # Coil -> Bit 05                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_CONTROLE_PARADA_NIVEL_DESABILITA":      [12288, 6], # Coil -> Bit 06                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_RV_MANUTENCAO":                         [12288, 10],# Coil -> Bit 10                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_RV_AUTOMATICO":                         [12288, 11],# Coil -> Bit 11                        (OP -> 0x15 Write Multiple Coils)

    "UG2_CD_CMD_UHRV":                                  12292,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_UHRV_MODO_AUTOMATICO":                  [12292, 0], # Coil -> Bit 00                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_UHRV_MODO_MANUTENCAO":                  [12292, 1], # Coil -> Bit 01                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_UHRV_BOMBA_1_LIGA":                     [12292, 2], # Coil -> Bit 02                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_UHRV_BOMBA_1_DESLIGA":                  [12292, 3], # Coil -> Bit 03                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_UHRV_BOMBA_2_LIGA":                     [12292, 4], # Coil -> Bit 04                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_UHRV_BOMBA_2_DESLIGA":                  [12292, 5], # Coil -> Bit 05                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_UHRV_BOMBA_1_PRINCIPAL":                [12292, 6], # Coil -> Bit 06                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_UHRV_BOMBA_2_PRINCIPAL":                [12292, 7], # Coil -> Bit 07                        (OP -> 0x15 Write Multiple Coils)

    "UG2_CD_CMD_UHLM":                                  12294,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_UHLM_MODO_AUTOMATICO":                  [12294, 0], # Coil -> Bit 00                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_UHLM_MODO_MANUTENCAO":                  [12294, 1], # Coil -> Bit 01                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_UHLM_BOMBA_1_LIGA":                     [12294, 2], # Coil -> Bit 02                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_UHLM_BOMBA_1_DESLIGA":                  [12294, 3], # Coil -> Bit 03                        (OP -> 0x15 Write Multiple Coils)

    "UG2_CD_CMD_PARTIDA_PARADA":                        12290,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_PARADA_TOTAL":                          [12290, 0], # Coil -> Bit 00                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_ATE_UHRV":                              [12290, 1], # Coil -> Bit 01                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_ATE_UHLM":                              [12290, 2], # Coil -> Bit 02                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_ATE_BORBOLETA":                         [12290, 5], # Coil -> Bit 05                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_ATE_RV":                                [12290, 7], # Coil -> Bit 07                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_ATE_RT":                                [12290, 8], # Coil -> Bit 08                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_SINCRONISMO":                           [12290, 9], # Coil -> Bit 09                        (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_ATE_FILTRAGEM":                         [12290, 10],# Coil -> Bit 10                        (OP -> 0x15 Write Multiple Coils)

    ## ENTRADAS ANALÓGICAS
    # ALARMES\PRESSÃO
    "UG2_EA_STT_ALARMES_HH_ANALOGICAS":                 12340,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_UHRV_PRESSAO_OLEO_MUITO_ALTO":              [12340, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG2_EA_SINAL_NIVEL_JUSANTE_MUITO_ALTO":            [12340, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)

    "UG2_EA_STT_ALARMES_H_ANALOGICAS":                  12342,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_UHRV_PRESSAO_OLEO_ALTO":                    [12342, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG2_EA_SINAL_NIVEL_JUSANTE_ALTO":                  [12342, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)

    "UG2_EA_STT_ALARMES_L_ANALOGICAS":                  12344,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_UHRV_PRESSAO_OLEO_BAIXA":                   [12344, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG2_EA_SINAL_NIVEL_JUSANTE_BAIXA":                 [12344, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)

    "UG2_EA_STT_ALARMES_LL_ANALOGICAS":                 12346,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_UHRV_PRESSAO_OLEO_MUITO_BAIXA":             [12346, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG2_EA_SINAL_NIVEL_JUSANTE_MUITO_BAIXA":           [12346, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)

    # ALARMES\TEMPERATURA
    "UG2_EA_STT_ALARMES_HH_TEMPERATURA":                12330,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TRISTORES_TEMP_MUITO_ALTA":                 [12330, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG2_EA_CROWBAR_TEMP_MUITO_ALTA":                   [12330, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)
    "UG2_EA_TRAFO_EXCITACAO_MUITO_ALTA":                [12330, 2], # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers)
    "UG2_EA_UHRV_TEMP_OLEO_MUITO_ALTA":                 [12330, 3], # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_FASE_A_TEMP_MUITO_ALTA":            [12330, 4], # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_FASE_B_TEMP_MUITO_ALTA":            [12330, 7], # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_FASE_C_TEMP_MUITO_ALTA":            [12330, 8], # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_NUCLEO_1_TEMP_MUITO_ALTA":          [12330, 9], # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_NUCLEO_2_MUITO_ALTA":               [12330, 10],# Input Register -> Bit 10              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_NUCLEO_3_TEMP_MUITO_ALTA":          [12330, 11],# Input Register -> Bit 11              (OP -> 0x04 Read Input Registers)
    "UG2_EA_MANCAL_GUIA_CASQUILHO_MUITO_ALTA":          [12330, 12],# Input Register -> Bit 12              (OP -> 0x04 Read Input Registers)
    "UG2_EA_MANCAL_COMBINADO_CASQUILHO_MUITO_ALTA":     [12330, 13],# Input Register -> Bit 13              (OP -> 0x04 Read Input Registers)
    "UG2_EA_MANCAL_COMBINADO_ESCORA_MUITO_ALTA":        [12330, 14],# Input Register -> Bit 14              (OP -> 0x04 Read Input Registers)

    "UG2_EA_STT_ALARMES_H_TEMPERATURA":                 12332,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TRISTORES_TEMP_ALTA":                       [12332, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG2_EA_CROWBAR_TEMP_ALTA":                         [12332, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)
    "UG2_EA_TRAFO_EXCITACAO_ALTA":                      [12332, 2], # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers)
    "UG2_EA_UHRV_TEMP_OLEO_ALTA":                       [12332, 3], # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_FASE_A_TEMP_ALTA":                  [12332, 4], # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_FASE_B_TEMP_ALTA":                  [12332, 7], # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_FASE_C_TEMP_ALTA":                  [12332, 8], # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_NUCLEO_1_TEMP_ALTA":                [12332, 9], # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_NUCLEO_2_ALTA":                     [12332, 10],# Input Register -> Bit 10              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_NUCLEO_3_TEMP_ALTA":                [12332, 11],# Input Register -> Bit 11              (OP -> 0x04 Read Input Registers)
    "UG2_EA_MANCAL_GUIA_CASQUILHO_ALTA":                [12332, 12],# Input Register -> Bit 12              (OP -> 0x04 Read Input Registers)
    "UG2_EA_MANCAL_COMBINADO_CASQUILHO_ALTA":           [12332, 13],# Input Register -> Bit 13              (OP -> 0x04 Read Input Registers)
    "UG2_EA_MANCAL_COMBINADO_ESCORA_ALTA":              [12332, 14],# Input Register -> Bit 14              (OP -> 0x04 Read Input Registers)

    # FALHAS\PRESSÃO
    "UG2_EA_STT_FALHAS_ANALOGICAS":                     12338,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_UHRV_PRESSAO_OLEO_FALHA_LEITURA":           [12338, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG2_EA_SINAL_NIVEL_JUSANTE_FALHA_LEITURA":         [12338, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)

    # FALHAS\TEMPERATURA
    "UG2_EA_STT_FALHAS_TEMPERATURA":                    12328,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TRISTORES_TEMP_FALHA_LEITURA":              [12328, 0], # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers)
    "UG2_EA_CROWBAR_TEMP_FALHA_LEITURA":                [12328, 1], # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers)
    "UG2_EA_TRAFO_EXCITACAO_FALHA_LEITURA":             [12328, 2], # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers)
    "UG2_EA_UHRV_TEMP_OLEO_FALHA_LEITURA":              [12328, 3], # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA":         [12328, 4], # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA":         [12328, 7], # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA":         [12328, 8], # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA":       [12328, 9], # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_NUCLEO_2_FALHA_LEITURA":            [12328, 10],# Input Register -> Bit 10              (OP -> 0x04 Read Input Registers)
    "UG2_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA":       [12328, 11],# Input Register -> Bit 11              (OP -> 0x04 Read Input Registers)
    "UG2_EA_MANCAL_GUIA_CASQUILHO_FALHA_LEITURA":       [12328, 12],# Input Register -> Bit 12              (OP -> 0x04 Read Input Registers)
    "UG2_EA_MANCAL_COMBINADO_CASQUILHO_FALHA_LEITURA":  [12328, 13],# Input Register -> Bit 13              (OP -> 0x04 Read Input Registers)
    "UG2_EA_MANCAL_COMBINADO_ESCORA_FALHA_LEITURA":     [12328, 14],# Input Register -> Bit 14              (OP -> 0x04 Read Input Registers)

    # LEITURAS\TEMPERATURAS
    "UG2_EA_TEMPERATURA_PONTE_TRISTORES":               12488,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TEMPERATURA_CROWBAR":                       12490,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TEMPERATURA_OLEO_UHRV":                     12492,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TEMPERATURA_OLEO_UHLM":                     12494,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TEMPERATURA_GERADOR_FASE_A":                12496,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TEMPERATURA_GERADOR_FASE_B":                12498,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TEMPERATURA_GERADOR_FASE_C":                12500,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TEMPERATURA_GERADOR_NUCLEO_1":              12502,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TEMPERATURA_GERADOR_NUCLEO_2":              12504,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TEMPERATURA_GERADOR_NUCLEO_3":              12506,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TEMPERATURA_MANCAL_GUIA_CASQUILHO":         12508,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TEMPERATURA_MANCAL_COMBINADO_CASQUILHO":    12510,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TEMPERATURA_MANCAL_COMBINADO_ESCORA":       12512,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TEMPERATURA_MANCAL_COMBINADO_CONTRA_ESCORA":12514,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_TEMPERATURA_TRAFO_EXCITACAO":               12518,      # Input Register                        (OP -> 0x04 Read Input Registers)

    # LEITURAS\PRESSÕES
    "UG2_EA_PRESSAO_OLEO_UHRV":                         12522,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_NIVEL_JUSANTE":                             12524,      # Input Register                        (OP -> 0x04 Read Input Registers)

    # LEITURAS\VIBRACOES
    "UG2_EA_VIBRACAO_EIXO_X_GUIA":                      12526,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_VIBRACAO_EIXO_X_COMBINADO":                 12528,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_VIBRACAO_EIXO_Y_COMBINADO":                 12530,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_VIBRACAO_EIXO_Z_COMBINADO":                 12532,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_VIBRACAO_EIXO_Y_GUIA":                      12534,      # Input Register                        (OP -> 0x04 Read Input Registers)

    ## ENTRADAS DIGITAIS
    # BLOQUEIOS
    "UG2_ED_STT_BLOQUEIO_86M":                          12428,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BLOQUEIO_86M_ATUADO":                       [12428, 31],# Holding Register -> Bit 31            (OP -> 0x03 Read Holding Registers)

    "UG2_ED_STT_BLOQUEIO_86E":                          12430,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BLOQUEIO_86E_ATUADO":                       [12430, 31],# Holding Register -> Bit 31            (OP -> 0x03 Read Holding Registers)

    "UG2_ED_STT_BLOQUEIO_86H":                          12432,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BLOQUEIO_86E_ATUADO":                       [12430, 31],# Holding Register -> Bit 31            (OP -> 0x03 Read Holding Registers)

    # BORBOLETA
    "UG2_ED_REAL_ESTADO_BORBOLETA":                     12614,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    "UG2_ED_STT_BORBOLETA":                             12414,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BROBOLETA_FALHA_ABRIR":                     [12414, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BORBOLETA_FALHA_FECHAR":                    [12414, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BORBOLETA_ABRINDO":                         [12414, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BORBOLETA_FECHANDO":                        [12414, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BYPASS_ABRINDO":                            [12414, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BYPASS_FECHANDO":                           [12414, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BYPASS_FALHA_ABRIR":                        [12414, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BYPASS_FALHA_FECHAR":                       [12414, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BORBOLETA_DISCREPANCIA_SENSORES":           [12414, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BYPASS_DISCREPANCIA_SENSORES":              [12414, 9], # Holding Register -> Bit 09            (OP -> 0x03 Read Holding Registers)

    # ENTRADAS CLP
    "UG2_ED_STT_ENTRADAS_DIGITAIS_0":                   12308,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    "UG2_ED_STT_ENTRADAS_DIGITAIS_1":                   12310,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_BOTAO_BLOQUEIO_86EH":                 [12310, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_REARME_FALHAS":                       [12310, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_BOTAO_PARA_UG":                       [12310, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_BOTAO_PARTE_UG":                      [12310, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_BOTAO_DIMINUI_REFERENCIA_RV":         [12310, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_BOTAO_AUMENTA_REFERENCIA_RV":         [12310, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_BOTAO_DIMINUI_REFERENCIA_RT":         [12310, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_BOTAO_AUMENTA_REFERENCIA_RT":         [12310, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RELE_PROT_GERADOR_FALHA":             [12310, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RELE_PROT_GERADOR_TRIP":              [12310, 9], # Holding Register -> Bit 09            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RELE_PROT_GERADOR_50BF":              [12310, 10],# Holding Register -> Bit 10            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RV_TRIP":                             [12310, 11],# Holding Register -> Bit 11            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RV_ALARME":                           [12310, 12],# Holding Register -> Bit 12            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RV_HABILITADO":                       [12310, 13],# Holding Register -> Bit 13            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RV_REGULANDO":                        [12310, 14],# Holding Register -> Bit 14            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RV_POTENCIA_NULA":                    [12310, 15],# Holding Register -> Bit 15            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RV_MAQUINA_PARADA":                   [12310, 16],# Holding Register -> Bit 16            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RV_VELOCIDADE_MENOR":                 [12310, 17],# Holding Register -> Bit 17            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RV_VELOCIDADE_MAIOR":                 [12310, 18],# Holding Register -> Bit 18            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RV_DISTRIBUIDOR_ABERTO":              [12310, 19],# Holding Register -> Bit 19            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RT_TRIP":                             [12310, 20],# Holding Register -> Bit 20            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RT_ALARME":                           [12310, 21],# Holding Register -> Bit 21            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RT_HABILITADO":                       [12310, 22],# Holding Register -> Bit 22            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RT_REGULANDO":                        [12310, 23],# Holding Register -> Bit 23            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_CONTATOR_CAMPO_FECHADO":              [12310, 24],# Holding Register -> Bit 24            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_DISJUNTOR_MAQUINA_FECHADO":           [12310, 25],# Holding Register -> Bit 25            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RELE_BLOQUEIO_86EH":                  [12310, 26],# Holding Register -> Bit 26            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_SUPERVISAO_DE_TENSAO_ENTRADA_CA":     [12310, 27],# Holding Register -> Bit 27            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_DISPOSITIVO_PROTECAO_SURTO":          [12310, 28],# Holding Register -> Bit 28            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_UHRV_BOMBA_DEFEITO":                  [12310, 29],# Holding Register -> Bit 29            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_UHRV_BOMBA_LIGADA":                   [12310, 30],# Holding Register -> Bit 30            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_UHLM_BOMBA_DEFEITO":                  [12310, 31],# Holding Register -> Bit 31            (OP -> 0x03 Read Holding Registers)

    "UG2_ED_STT_ENTRADAS_DIGITAIS_2":                   12312,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_UHLM_BOMBA_LIGADA":                   [12312, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_ACIONAMENTO_RESERVA_DEFEITO":         [12312, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_ACIONAMENTO_RESERVA_LIGADO":          [12312, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RESISTENCIA_AQUEC_GERADOR_DEFEITO":   [12312, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_RESISTENCIA_AQUEC_GERADOR_LIGADA":    [12312, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_DISJUNTOR_TPS_PROTECAO":              [12312, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_UHRV_OLEO_NIVEL_MUITO_BAIXO":         [12312, 6], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_UHRV_FILTRO_OLEO_SUJO":               [12312, 7], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_UHRV_PRESSAO_CRITICA":                [12312, 8], # Holding Register -> Bit 09            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_UHRV_PRESSAO_FREIO":                  [12312, 9], # Holding Register -> Bit 10            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_UHLM_OLEO_NIVEL_MUITO_ALTO":          [12312, 11],# Holding Register -> Bit 12            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_UHLM_OLEO_NIVEL_MUITO_BAIXO":         [12312, 12],# Holding Register -> Bit 13            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_UHLM_PRESSAO_LINHA_LUBRIFICACAO":     [12312, 13],# Holding Register -> Bit 14            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_UHLM_FILTRO_OLEO_SUJO":               [12312, 14],# Holding Register -> Bit 15            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_UHLM_FLUXO_TROCADOR_CALOR":           [12312, 15],# Holding Register -> Bit 16            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_QBAG_ESCOVA_POLO_POSITIVO_DESGASTADA":[12312, 17],# Holding Register -> Bit 18            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_QBAG_ESCOVA_POLO_NEGATICO_DESGASTADA":[12312, 18],# Holding Register -> Bit 19            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_PSA_BLOQUEIO_86BTBF":                 [12312, 19],# Holding Register -> Bit 20            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_PSA_POCO_DRENAGEM_NIVEL_MUITO_ALTO":  [12312, 20],# Holding Register -> Bit 21            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_PSA_FILTRAGEM_PRESSAO_SAIDA":         [12312, 21],# Holding Register -> Bit 22            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_PSA_DISJUNTOR_LINHA_FECHADO":         [12312, 22],# Holding Register -> Bit 23            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_VB_VALVULA_BORBOLETA_ABERTA":         [12312, 28],# Holding Register -> Bit 28            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_VB_VALVULA_BORBOLETA_FECHADA":        [12312, 29],# Holding Register -> Bit 29            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_VB_VALVULA_BYPASS_ABERTA":            [12312, 30],# Holding Register -> Bit 30            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PRTVA_VB_VALVULA_BYPASS_FECHADA":           [12312, 31],# Holding Register -> Bit 31            (OP -> 0x03 Read Holding Registers)

    "UG2_ED_STT_ENTRADAS_DIGITAIS_3":                   12314,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_STT_ENTRADAS_DIGITAIS_4":                   12316,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # PARTIDA E PARADA
    "UG2_ED_STT_PASSO_SELECIONADO_BIT":                 12390,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_STT_PASSO_ATUAL_BIT":                       12392,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    "UG2_ED_STT_PASSO_ATUAL":                           12366,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHRV_PASSO_ATUAL":                          [12366, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHLM_PASSO_ATUAL":                          [12366, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_FILTRAGEM_PASSO_ATUAL":                     [12366, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BORBOLETA_PASSO_ATUAL":                     [12366, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RV_PASSO_ATUAL":                            [12366, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RT_PASSO_ATUAL":                            [12366, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_SINCRONISMO_PASSO_ATUAL":                   [12366, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_OPERANDO_PASSO_ATUAL":                      [12366, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PARADA_EMERGENCIA_PASSO_ATUAL":             [12366, 9], # Holding Register -> Bit 09            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PARADA_PARCIAL_PASSO_ATUAL":                [12366, 10],# Holding Register -> Bit 10            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PARADA_SEM_REJEICAO_PASSO_ATUAL":           [12366, 11],# Holding Register -> Bit 11            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PARADA_PASSO_A_PASSO_PASSO_ATUAL":          [12366, 12],# Holding Register -> Bit 12            (OP -> 0x03 Read Holding Registers)

    "UG2_ED_STT_PASSO_CONCLUIDO":                       12368,      # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PARDA_TOTAL_PASSO_CONCLUIDO":               [12368, 0], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_URHV_PASSO_CONCLUIDO":                      [12368, 1], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHLM_PASSO_CONCLUIDO":                      [12368, 2], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_FILTRAGEM_PASSO_CONCLUIDO":                 [12368, 3], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BORBOLETA_PASSO_CONCLUIDO":                 [12368, 4], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RV_PASSO_CONCLUIDO":                        [12368, 5], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RT_PASSO_CONCLUIDO":                        [12368, 6], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_SINCRONISMO_PASSO_CONCLUIDO":               [12368, 7], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)

    "UG2_ED_STT_PASSO_FALHA":                           12370,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHRV_PASSO_FALHA":                          [12370, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_FRIO_PASSO_FALHA":                          [12370, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHLM_PASSO_FALHA":                          [12370, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_FILTRAGEM_PASSO_FALHA":                     [12370, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BORBOLETA_PASSO_FALHA":                     [12370, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RV_PASSO_FALHA":                            [12370, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RT_PASSO_FALHA":                            [12370, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_SINCRONIZAR_PASSO_FALHA":                   [12370, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)

    "UG2_ED_STT_PASSO_SELECIONADO":                     12372,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_PARADA_TOTAL":                              [12372, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHRV":                                      [12372, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHLM":                                      [12372, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_FILTRAGEM":                                 [12372, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_BORBOLETA":                                 [12372, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RV":                                        [12372, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RT":                                        [12372, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_SINCRONISMO":                               [12372, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)

    "UG2_ED_STT_REAL_ESTADO_UNIDADE":                   12374,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_STT_REAL_PASSO_ATUAL":                      12376,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # PERMISSIVOS
    "UG2_ED_STT_PRE_CONDICOES_PARTIDA":                 12408,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # RT
    "UG2_ED_STT_RT":                                    12350,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RT_FALHA_AO_HABILITAR":                     [12350, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RT_FALHA_AO_PARTIR":                        [12350, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RT_FALHA_AO_DESABILITAR":                   [12350, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)

    # RV
    "UG2_ED_STT_RV":                                    12360,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RV_FALHA_AO_HABILITAR":                     [12360, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RV_FALHA_AO_PARTIR":                        [12360, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RV_FALHA_AO_DESABILITAR":                   [12360, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RV_FALHA_AO_PARAR_MAQUINA":                 [12360, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR":           [12360, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RV_MODO_MANUTENCAO":                        [12360, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)

    # UNIDADE GERADORA
    "UG2_ED_STT_UNIDADE_GERADORA":                      12348,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_CONTROLE_POTENCIA_NIVEL_HABILITADO":        [12348, 0], # Holding Register -> Bit 00            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_CONTROLE_NIVEL_HABILITADO":                 [12348, 1], # Holding Register -> Bit 01            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_CONTROLE_POTENCIA_MANUAL_HABILITADO":       [12348, 2], # Holding Register -> Bit 02            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_CONTROLE_PARADA_NIVEL_HABILITADO":          [12348, 3], # Holding Register -> Bit 03            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_CONTROLE_PARADA_NIVEL_BAIXO":               [12348, 4], # Holding Register -> Bit 04            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_CONTROLE_FALHA_SENSOR_NIVEL":               [12348, 5], # Holding Register -> Bit 05            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_CONTROLE_ALARME_DIFERENCIAL_GRADE":         [12348, 6], # Holding Register -> Bit 06            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_CONTROLE_TRIP_DIFERENCIAL_GRADE":           [12348, 7], # Holding Register -> Bit 07            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RESISTENCIA_AQUEC_GERADOR_INDISPONIVEL":    [12348, 8], # Holding Register -> Bit 08            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR":     [12348, 9], # Holding Register -> Bit 09            (OP -> 0x03 Read Holding Registers)
    "UG2_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_DESLIGAR":  [12348, 10],# Holding Register -> Bit 10            (OP -> 0x03 Read Holding Registers)

    # UHLM
    "UG2_ED_STT_UHLM":                                  12354,      # Holding Reggister                     (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHLM_UNIDADE_MANUTENCAO":                   [12354, 0], # Holding Reggister -> Bit 00           (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHLM_BOMBA_1_INDISPONIVEL":                 [12354, 1], # Holding Reggister -> Bit 01           (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHLM_BOMBA_1_FALHA_LIGAR":                  [12354, 5], # Holding Reggister -> Bit 05           (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHLM_BOMBA_1_FALHA_DESLIGAR":               [12354, 6], # Holding Reggister -> Bit 06           (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHLM_BOMBA_1_FALHA_PRESSURIZAR":            [12354, 9], # Holding Reggister -> Bit 09           (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHLM_FILTRO_SUJO":                          [12354, 12],# Holding Reggister -> Bit 10           (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHLM_FALHA_PRESSOSTATO":                    [12354, 13],# Holding Reggister -> Bit 13           (OP -> 0x03 Read Holding Registers)

    # UHRV
    "UG2_ED_STT_UHRV":                                  12362,      # Holding Reggister                     (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHRV_UNIDADE_MANUTENCAO":                   [12362, 0], # Holding Reggister -> Bit 00           (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHRV_UNIDADE_HABILITADA":                   [12362, 1], # Holding Reggister -> Bit 01           (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHRV_INDISPONIVEL":                         [12362, 2], # Holding Reggister -> Bit 02           (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHRV_FALHA_AO_LIGAR":                       [12362, 6], # Holding Reggister -> Bit 06           (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHRV_FALHA_AO_DESLIGAR":                    [12362, 7], # Holding Reggister -> Bit 07           (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHRV_FALHA_AO_PRESSURIZAR":                 [12362, 10],# Holding Reggister -> Bit 10           (OP -> 0x03 Read Holding Registers)
    "UG2_ED_UHRV_FILTRO_OLEO_SUJO":                     [12362, 13],# Holding Reggister -> Bit 13           (OP -> 0x03 Read Holding Registers)

    ## DRIVER RV
    "UG2_RV_ROTACAO":                                   16,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)

    "UG2_RV_ESTADO_OPERACAO":                           21,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    # "UG2_RV_ESTADO_OPERACAO" -> PROCESSANDO = 00
    # "UG2_RV_ESTADO_OPERACAO" -> PARADA FINALIZADA = 01
    # "UG2_RV_ESTADO_OPERACAO" -> INICIO PARTIDA = 02
    # "UG2_RV_ESTADO_OPERACAO" -> PRIMEIRO ESTAGIO PARTIDA = 03
    # "UG2_RV_ESTADO_OPERACAO" -> SEGUNDO ESTAGIO PARTIDA = 04
    # "UG2_RV_ESTADO_OPERACAO" -> CONTROLANDO ABERTURA = 5
    # "UG2_RV_ESTADO_OPERACAO" -> CONTROLANDO VELOCIDADE = 6
    # "UG2_RV_ESTADO_OPERACAO" -> CONTROLANDO EM DROOP = 7
    # "UG2_RV_ESTADO_OPERACAO" -> CONTROLANDO EM DROOP EXTERNO = 8
    # "UG2_RV_ESTADO_OPERACAO" -> CONTROLANDO POTENCIA = 9
    # "UG2_RV_ESTADO_OPERACAO" -> CONTROLANDO POTENCIA POR REFERENCIA ANALOGICA = 10
    # "UG2_RV_ESTADO_OPERACAO" -> CONTROLANDO NIVEL = 11
    # "UG2_RV_ESTADO_OPERACAO" -> ZERANDO CARGA = 12
    # "UG2_RV_ESTADO_OPERACAO" -> PARANDO = 13
    # "UG2_RV_ESTADO_OPERACAO" -> CONTROLE MANUAL DISTRIBUIDOR = 14
    # "UG2_RV_ESTADO_OPERACAO" -> CONTROLE MANUAL ROTOR = 15
    # "UG2_RV_ESTADO_OPERACAO" -> EMERGENCIA = 16

    "UG2_RV_CONTROLE_SINCRONIZADO_SELECIONADO":         22,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONTROLE_VAZIO_SELECIONADO":                23,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_COMANDO_MODBUS":                            24,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SETPOINT_POTENCIA_ATIVA_PU":                30,         # Input Register                        (OP -. 0x04 Read Input Registers - 3x)


    # DIGITAIS
    "UG2_RV_ENTRADAS_DIGITAIS":                         25,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ED_SEN_BLOQUEIIO_EXTERNO":                  [25, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ED_HABILITA_REGULADOR":                     [25, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ED_SELEC_MODO_CONTROLE_ISOLADO":            [25, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ED_ZERA_CARGA":                             [25, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ED_RESET_FALHAS":                           [25, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ED_INCREMENTA_REF_CONTROLE":                [25, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ED_DECREMENTA_REFERENCIA_CONTROLE":         [25, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ED_DISJ_MAQUINA_FECHADO":                   [25, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)

    # RELE
    "UG2_RV_SAIDAS_DIGIAIS":                            26,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SD_RELE_TRIP_NAO_ATUADO":                   [26, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SD_RELE_ALARME":                            [26, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SD_RELE_REGULADOR_HABILITADO":              [26, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SD_RELE_REGULADOR_REGULANDO":               [26, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SD_RELE_POTENCIA_NULA":                     [26, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SD_RELE_MAQUINA_PARADA":                    [26, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SD_RELE_VELOC_MENOR_30":                    [26, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SD_RELE_VELOC_MAIOR_90":                    [26, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SD_RELE_DISTRIBUIDOR_ABERTO":               [26, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SD_RELE_SAIDA_PROGRAMAVEL":                 [26, 9],    # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers - 3x)

    # LIMITES
    "UG2_RV_LIMITES_OPERACAO":                          27,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_LIMITADOR_SUPERIOR_DISTRI_ATUADO":          [27, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_LIMITADOR_INFERIOR_DISTRI_ATUADO":          [27, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_LIMITADOR_SUPERIOR_ROTOR_ATUADO":           [27, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_LIMITADOR_INFERIOR_ROTOR_ATUADO":           [27, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_LIMITADOR_SUPERIOR_VELOC_ATUADO":           [27, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_LIMITADOR_INFERIOR_VELOC_ATUADO":           [27, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_LIMITADOR_SUPERIOR_POTENCIA_ATUADO":        [27, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_LIMITADOR_INFERIOR_POTENCIA_ATUADO":        [27, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)

    # ALARMES
    "UG2_RV_ALARME":                                    66,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME_SOBREFREQUENCIA":                    [66, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME_SUBFREQUENCIA":                      [66, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME_LEIT_POS_DISTRIBUIDOR":              [66, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME_LEIT_POS_ROTOR":                     [66, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME_LEIT_POS_POTENCIA_ATIVA":            [66, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME_LEIT_POS_NV_MONTANTE":               [66, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME_LEIT_POS_NV_MONTANTE_MUITO_BAIXO":   [66, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME_CONTR_POS_DISTRIBUIDOR":             [66, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME_CONTR_POS_ROTOR":                    [66, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME_RUIDO_MED_VELOCIDADE_PRINCIPAL":     [66, 9],    # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME_RUIDO_MED_VELOCIDADE_RETAGUARDA":    [66, 10],   # Input Register -> Bit 10              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME_PERDA_MED_VELOC_PRINCIPAL":          [66, 11],   # Input Register -> Bit 11              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME_PERDA_MED_VELOC_RETAGUARDA":         [66, 12],   # Input Register -> Bit 12              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME_DIF_MED_VELOCIDADE_PRINCIPAL":       [66, 13],   # Input Register -> Bit 13              (OP -> 0x04 Read Input Registers - 3x)

    # FALHAS
    "UG2_RV_FALHA_1":                                   67,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_SOBREFREQ_INSTANT":                 [67, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_SOBREFREQ_TEMPOR":                  [67, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_SUBFREQ_TEMPORIZADA":               [67, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_GIRANDO_SEM_REG_GIRO_INDEV":        [67, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_LEIT_POS_DISTRIBUIDOR":             [67, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_LEIT_POS_ROTOR":                    [67, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_LEIT_POTENCIA_ATIVA":               [67, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_LEIT_REFERENCIA_POTENCIA":          [67, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_LEIT_NV_MONTANTE":                  [67, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_NV_MONTANTE_MUITO_BAIXO":           [67, 10],   # Input Register -> Bit 10              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_CONTROLE_POS_DISTRIBUIDOR":         [67, 11],   # Input Register -> Bit 11              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_CONTROLE_POS_ROTOR":                [67, 12],   # Input Register -> Bit 12              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_RUIDO_MED_VELOC_PRINCIPAL":         [67, 13],   # Input Register -> Bit 13              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_RUIDO_MED_VELOC_RETAGUARDA":        [67, 14],   # Input Register -> Bit 14              (OP -> 0x04 Read Input Registers - 3x)

    "UG2_RV_FALHA_2":                                   68,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1_PERDA_MED_VELOC_PRINCIPAL":         [68, 15],   # Input Register -> Bit 15              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_2_PERDA_MED_VELOC_RETAGUARDA":        [68, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_2_TEMPO_EXCESSIVO_PARTIDA":           [68, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_2_TEMPO_EXCESSIVO_PARADA":            [68, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_2_BLOQUEIO_EXTERNO":                  [68, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_2_DIF_MED_VELO_PRINCIPAL_RETAGUARDA": [68, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)

    "UG2_RV_POTENCIA_APARENTE_NOMINAL":                 79,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_POTENCIA_ATIVA_NOMINAL":                    80,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONTROLE_1":                                85,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONTROLE_2":                                86,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_DISTRIBUIDOR_1":                  121,        # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_ROTOR_1":                         122,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_DISTRIBUIDOR_2":                  123,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_ROTOR_2":                         124,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_DISTRIBUIDOR_3":                  125,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_ROTOR_3":                         126,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_DISTRIBUIDOR_4":                  127,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_ROTOR_4":                         128,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_DISTRIBUIDOR_5":                  129,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_ROTOR_5":                         130,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_DISTRIBUIDOR_6":                  131,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_ROTOR_6":                         132,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_DISTRIBUIDOR_7":                  133,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_ROTOR_7":                         134,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_DISTRIBUIDOR_8":                  135,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_ROTOR_8":                         136,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_DISTRIBUIDOR_9":                  137,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_ROTOR_9":                         138,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_DISTRIBUIDOR_10":                 139,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONJUGADO_ROTOR_10":                        140,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ABERTURA_MAXIMA_DISTRIBUIDOR":              182,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ABERTURA_MINIMA_DISTRIBUIDOR":              183,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ABERTURA_MAXIMA_DISTRIBUIDOR_A_VAZIO":      184,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ABERTURA_MAXIMA_ROTOR":                     185,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ABERTURA_MINIMA_ROTOR":                     186,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_POTENCIA_MAXIMA":                           189,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_POTENCIA_MINIMA":                           190,        # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)

    ## DRIVER RT
    "UG2_RT_CORRENTE_EXCITACAO":                        16,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_TENSAO_EXCITACAO":                          17,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_TEMPERATURA_ROTOR":                         25,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)

    "UG2_RT_ESTADO_OPERACAO":                           26,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    # "UG2_RT_ESTADO_OPERACAO" -> PROCESSANDO = 00
    # "UG2_RT_ESTADO_OPERACAO" -> PARADA FINALIZADA = 01
    # "UG2_RT_ESTADO_OPERACAO" -> INICIO PARTIDA = 02
    # "UG2_RT_ESTADO_OPERACAO" -> PRIMEIRO ESTAGIO PARTIDA = 03
    # "UG2_RT_ESTADO_OPERACAO" -> SEGUNDO ESTAGIO PARTIDA = 04
    # "UG2_RT_ESTADO_OPERACAO" -> CONTROLANDO ABERTURA = 5
    # "UG2_RT_ESTADO_OPERACAO" -> CONTROLANDO VELOCIDADE = 6
    # "UG2_RT_ESTADO_OPERACAO" -> CONTROLANDO EM DROOP = 7
    # "UG2_RT_ESTADO_OPERACAO" -> CONTROLANDO EM DROOP EXTERNO = 8
    # "UG2_RT_ESTADO_OPERACAO" -> CONTROLANDO POTENCIA = 9
    # "UG2_RT_ESTADO_OPERACAO" -> CONTROLANDO POTENCIA POR REFERENCIA ANALOGICA = 10
    # "UG2_RT_ESTADO_OPERACAO" -> CONTROLANDO NIVEL = 11
    # "UG2_RT_ESTADO_OPERACAO" -> ZERANDO CARGA = 12
    # "UG2_RT_ESTADO_OPERACAO" -> PARANDO = 13
    # "UG2_RT_ESTADO_OPERACAO" -> CONTROLE MANUAL DISTRIBUIDOR = 14
    # "UG2_RT_ESTADO_OPERACAO" -> CONTROLE MANUAL ROTOR = 15
    # "UG2_RT_ESTADO_OPERACAO" -> EMERGENCIA = 16

    "UG2_RT_CONTROLE_SINCRONIZADO_SELECIONADO":         27,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)

    "UG2_RT_ENTRADAS_DIGITAIS":                         30,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ED_SEM_BLOQUEIO_EXTERNO":                   [30, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ED_HABILITA_REGULADOR":                     [30, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ED_SELEC_MODO_CONTROLE_ISOLADO":            [30, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ED_DRIVE_EXCITACAO_HABILITADO":             [30, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ED_RESET_FALHAS":                           [30, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ED_INCREMENTA_REF_CONTROLE":                [30, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ED_DECREMENTA_REF_CONTROLE":                [30, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ED_DISJ_MAQUINA_FECHADO":                   [30, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ED_CONTATOR_CAMPO_FECHADO":                 [30, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ED_CROWBAR_INATIVO":                        [30, 9],    # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers - 3x)

    "UG2_RT_SAIDAS_DIGITAIS":                           31,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_SD_RELE_TRIP_NAO_ATUADO":                   [31, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_SD_RELE_ALARME":                            [31, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_SD_RELE_REGULADOR_HABILITADO":              [31, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_SD_RELE_REGULADOR_REGULANDO":               [31, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_SD_RELE_HABILITA_DRIVE_EXCITACAO":          [31, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_SD_RELE_HABILITA_CONTATOR_CAMPO":           [31, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_SD_RELE_HABILITA_PRE_EXCITACAO":            [31, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_SD_RELE_HABILITA_CROWBAR":                  [31, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)

    "UG2_RT_LIMITES_OPERACAO":                          32,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_LIMITADOR_SUP_CORRENTE_EXCITACAO":          [32, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_LIMITADOR_INF_CORRENTE_EXCITACAO":          [32, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_LIMITADOR_SUP_TENSAO_TERMINAL":             [32, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_LIMITADOR_INF_TENSAO_TERMINAL":             [32, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_LIMITADOR_SUP_POTENCIA_REATIVA":            [32, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_LIMITADOR_INF_POTENCIA_REATIVA":            [32, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_LIMITADOR_SUP_FATOR_POTENCIA":              [32, 10],   # Input Register -> Bit 10              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_LIMITADOR_INF_FATOR_POTENCIA":              [32, 11],   # Input Register -> Bit 11              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_LIMITADOR_VOLTZ_HERTZ":                     [32, 12],   # Input Register -> Bit 12              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_LIMITADOR_ABERTURA_PONTE":                  [32, 13],   # Input Register -> Bit 13              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_LIMITADOR_PQ":                              [32, 14],   # Input Register -> Bit 14              (OP -> 0x04 Read Input Registers - 3x)

    "UG2_RT_SETPOINT_TENSAO_PU":                        40,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_SETPOINT_POTENCIA_REATIVA_PU":              41,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_SETPOINT_FATOR_POTENCIA_PU":                42,         # Input Register Scale -1               (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ABERTURA_PONTE":                            43,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_REFERENCIA_CORRENTE_CAMPO_PU":              46,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FEEDBACK_CORRENTE_CAMPO_PU":                47,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_REFERENCIA_TENSAO_PU":                      52,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FEEDBACK_TENSAO_PU":                        53,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_REFERENCIA_POTENCIA_REATIVA_PU":            58,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FEEDBACK_POTENCIA_REATIVA_PU":              59,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_REFERENCIA_FATOR_POTENCIA_PU":              64,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FEEDBACK_FATOR_POTENCIA_PU":                65,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)

    # ALARMES
    "UG2_RT_ALARMES_1":                                 70,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_SOBRETENSAO":                     [70, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_SUBTENSAO":                       [70, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_SOBREFREQUENCIA":                 [70, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_SUBFREQUENCIA":                   [70, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_LIMITE_SUP_POT_REATICA":          [70, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_LIMITE_INF_POT_REATIAVA":         [70, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_LIMITE_SUP_FATOR_POTENCIA":       [70, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_LIMITE_INF_FATOR_POTENCIA":       [70, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_VARIACAO_TENSAO":                 [70, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_POTENCIA_ATIVA_REVERSA":          [70, 9],    # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_SOBRECORRENTE_TERMINAL":          [70, 10],   # Input Register -> Bit 10              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_LIMITE_SUP_CORRENTE_EXCITACAO":   [70, 11],   # Input Register -> Bit 11              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_LIMITE_INF_CORRENTE_EXCITACAO":   [70, 12],   # Input Register -> Bit 12              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_TEMP_MUITO_ALTA_ROTOR":           [70, 13],   # Input Register -> Bit 13              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_PRES_TENS_TERM_AUSEN_CORR_EXCI":  [70, 14],   # Input Register -> Bit 14              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1_PRES_CORR_EXCI_AUSEN_TENS_TERM":  [70, 15],   # Input Register -> Bit 15              (OP -> 0x04 Read Input Registers - 3x)

    "UG2_RT_ALARMES_2":                                 71,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_2_FALHA_CONTROLE_CORRENTE_EXCI":    [71, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_2_FALHA_CONTROLE_TENSAO_TERM":      [71, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_2_CROWBAR_ATUADO_REGUL_HABIL":      [71, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_2_FALHA_HABIL_DRIVE_EXCI":          [71, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_2_FALHA_FECHAR_CONTATOR_CAMPO":     [71, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_2_FALHA_CORR_EXCI_PRE_EXCI_ATIVA":  [71, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_2_PERDA_MEDICAO_POTENCIA_REATIVA":  [71, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_2_PERDA_MEDICAO_TENSAO_TERMINAL":   [71, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_2_PERDA_MEDICAO_CORRENTE_EXCI":     [71, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_2_RUIDO_INSTRUMEN_REATIVO":         [71, 9],    # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_2_RUIDO_INSTRUMEN_TENSAO":          [71, 10],   # Input Register -> Bit 10              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_2_RUIDO_INSTRUMEN_EXCI_PRINCI":     [71, 11],   # Input Register -> Bit 11              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_2_RUIDO_INSTRUMEN_EXCI_RETAG":      [71, 12],   # Input Register -> Bit 12              (OP -> 0x04 Read Input Registers - 3x)

    "UG2_RT_FALHAS_1":                                  72,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_SOBRETENSAO":                      [72, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_SUBTENSAO":                        [72, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_SOBREFREQUENCIA":                  [72, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_SUBFREQUENCIA":                    [72, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_LIMITE_SUP_POT_REATIVA":           [72, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_LIMITE_INF_POT_REATIVA":           [72, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_LIMITE_SUP_FATOR_POT":             [72, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_LIMITE_INF_FATOR_POT":             [72, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_SOBRETENSAO_INST":                 [72, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_VARIACAO_TENSAO":                  [72, 9],    # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_POT_ATIVA_REVERSA":                [72, 10],   # Input Register -> Bit 10              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_SOBRECORRENTE_TERMINAL":           [72, 11],   # Input Register -> Bit 11              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_LIMITE_SUP_CORRENTE_EXCITACAO":    [72, 12],   # Input Register -> Bit 12              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_LIMITE_INF_CORRENTE_EXCITACAO":    [72, 13],   # Input Register -> Bit 13              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_LIMITE_SUP_TENSAO_EXCITACAO":      [72, 14],   # Input Register -> Bit 14              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1_LIMITE_INF_TENSAO_EXCITACAO":      [72, 15],   # Input Register -> Bit 15              (OP -> 0x04 Read Input Registers - 3x)

    "UG2_RT_FALHAS_2":                                  73,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_2_TEMP_MUITO_ALTA_ROTOR":            [73, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_2_PRES_TENS_TERM_AUSEN_CORR_EXCI":   [73, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_2_PRES_CORR_EXCI_AUSEN_TENS_TERM":   [73, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_2_CONTROLE_CORR_EXCI":               [73, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_2_TENSAO_TERMINAL":                  [73, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_2_CROWBAR_ATUADO_REGULADOR_HABI":    [73, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_2_HABI_DRIVE_EXCITACAO":             [73, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_2_FECHAR_CONTATOR_CAMPO":            [73, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_2_CORR_EXCITA_PRE_EXCXITA_ATIVA":    [73, 8],    # Input Register -> Bit 08              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_2_EXCESSIVO_PRE_EXCITACAO":          [73, 9],    # Input Register -> Bit 09              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_2_EXCESSIVO_PARADA":                 [73, 10],   # Input Register -> Bit 10              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_2_EXCESSIVO_PARTIDA":                [73, 11],   # Input Register -> Bit 11              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_2_BLOQ_EXTERNO":                     [73, 12],   # Input Register -> Bit 12              (OP -> 0x04 Read Input Registers - 3x)

    "UG2_RT_FALHAS_3":                                  74,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_3_PERDA_MED_POT_REATIVA":            [74, 0],    # Input Register -> Bit 00              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_3_PERDA_MED_TENSAO_TERM":            [74, 1],    # Input Register -> Bit 01              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_3_PERDA_MED_CORR_EXCI_PRINCI":       [74, 2],    # Input Register -> Bit 02              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_3_PERDA_MED_CORR_EXCI_RETAG":        [74, 3],    # Input Register -> Bit 03              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_3_RUIDO_INSTRUM_REATIVO":            [74, 4],    # Input Register -> Bit 04              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_3_RUIDO_INSTRUM_TENSAO":             [74, 5],    # Input Register -> Bit 05              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_3_RUIDO_INSTRUM_PRINCI":             [74, 6],    # Input Register -> Bit 06              (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_3_RUIDO_INSTRUM_RETAG":              [74, 7],    # Input Register -> Bit 07              (OP -> 0x04 Read Input Registers - 3x)

    "UG2_RT_TENSAO_NOMINAL":                            85,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_POTENCIA_APARENTE_NOMINAL":                 86,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_CONTROLE_1":                                90,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_CONTROLE_2":                                91,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
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
        "SA_CD_REARME_FALHAS":                      [12288, 0],     # OK
        "SA_CD_DISJ_LINHA_FECHA":                   [12288, 17],    # OK

        # Retornos
        "SA_ED_PSA_DIJS_TSA_FECHADO":               [12309, 26],    # OK
        "SA_ED_PSA_DIJS_GMG_FECHADO":               [12309, 27],    # OK
        "SA_ED_PSA_SE_DISJ_LINHA_FECHADO":          [12309, 31],    # OK
    },

    "UG": {
        ## UG1
        # Comandos
        "UG1_CD_CMD_REARME_FALHAS":                 [12288, 0],     # OK
        "UG1_CD_CMD_PARADA_EMERGENCIA":             [12288, 1],     # OK
        "UG1_CD_CMD_RV_MANUTENCAO":                 [12288, 10],    # OK
        "UG1_CD_CMD_RV_AUTOMATICO":                 [12288, 11],    # OK
        "UG1_CD_CMD_UHLM_MODO_MANUTENCAO":          [12294, 0],     # OK
        "UG1_CD_CMD_UHLM_MODO_AUTOMATICO":          [12294, 1],     # OK
        "UG1_CD_CMD_PARADA_TOTAL":                  [12290, 0],     # OK
        "UG1_CD_CMD_SINCRONISMO":                   [12290, 9],     # OK
        "UG1_RV_SETPOINT_POTENCIA_ATIVA_PU":        30,             # OK

        # Retornos
        "UG1_ED_UHRV_UNIDADE_HABILITADA":           [12362, 1],     # OK



        ## UG2
        # Comandos
        "UG2_CD_CMD_REARME_FALHAS":                 [12288, 0],     # OK
        "UG2_CD_CMD_PARADA_EMERGENCIA":             [12288, 1],     # OK
        "UG2_CD_CMD_RV_MANUTENCAO":                 [12288, 10],    # OK
        "UG2_CD_CMD_RV_AUTOMATICO":                 [12288, 11],    # OK
        "UG2_CD_CMD_UHLM_MODO_MANUTENCAO":          [12294, 0],     # OK
        "UG2_CD_CMD_UHLM_MODO_AUTOMATICO":          [12294, 1],     # OK
        "UG2_CD_CMD_PARADA_TOTAL":                  [12290, 0],     # OK
        "UG2_CD_CMD_SINCRONISMO":                   [12290, 9],     # OK
        "UG2_RV_SETPOINT_POTENCIA_ATIVA_PU":        30,             # OK

        # Retornos
        "UG2_ED_UHRV_UNIDADE_HABILITADA":           [12362, 1],     # OK
    },

    "GERAL": {
        # Comandos
        "GERAL_CD_RESET_GERAL":                     [12288, 0],     # OK

        # Retornos
        "GERAL_EA_NIVEL_MONTANTE_GRADE":            12350,          # OK
    },

    "RELE": {
        # Retornos
        "RELE_SE_VAB":                              330,            # OK
        "RELE_SE_VBC":                              332,            # OK
        "RELE_SE_VCA":                              334,            # OK
        "RELE_SE_P":                                353,            # OK

        "RELE_UG1_P":                               353,            # OK
        "UG1_ED_PRTVA_DISJUNTOR_MAQUINA_FECHADO":   [8464, 0],      # OK

        "RELE_UG2_P":                               353,            # OK
        "UG2_ED_PRTVA_DISJUNTOR_MAQUINA_FECHADO":   [8464, 0],      # OK
    },
}