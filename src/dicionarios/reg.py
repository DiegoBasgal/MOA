REG_RELE = {
    "UG": {
        # UG1
        "UG1_SOBREFREQ_ELEMENTO_2":                         1,    # Bit: 4                              81X4T (MOD 001)
        "UG1_SOBREFREQ_ELEMENTO_1":                         1,    # Bit: 5                              81X3T (MOD 001)
        "UG1_SUBFREQ_ELEMENTO_2":                           1,    # Bit: 6                              81X2T (MOD 001)
        "UG1_SUBFREQ_ELEMENTO_1":                           1,    # Bit: 7                              81X1T (MOD 001)

        "UG1_WATCHDOG_OP_NORMAL":                           313,  #                                     OUT305

        "UG1_SOBRECORR_INSTANTANEA":                        901,  # Bit: 0                              50PX1T
        "UG1_SOBRECORR_INSTANTANEA_NEUTRO":                 901,  # Bit: 1                              67N1T
        "UG1_SOBRECORR_SEQUENCIA_NEG":                      901,  # Bit: 2                              46Q2T
        "UG1_SOBRECORR_TEMPORIZADA_NEUTRO":                 901,  # Bit: 4                              51NT
        "UG1_DIFERENCIAL_COM_RESTRICAO":                    901,  # Bit: 14                             87R
        "UG1_DIFERENCIAL_SEM_RESTRICAO":                    901,  # Bit: 15                             87U

        "UG1_SUBTENSAO_GERAL":                              902,  # Bit: 0                              27PX1T, 27PX2T, 27PPX1T, 27PPX2T
        "UG1_SOBRETENSAO_GERAL":                            902,  # Bit: 1                              59PX1T, 59PX2T, 59PPX1T, 59PPX2T, 59GX1T, 59QX1T
        "UG1_POTENCIA_REVERSA":                             902,  # Bit: 3                              3PWRX1T
        "UG1_TRIP_RELACIONADO_FREQ":                        902,  # Bit: 4                              81
        "UG1_VOLTZ_HERTZ":                                  902,  # Bit: 5                              24C2T
        "UG1_SOBRECORR_RESTRICAO_TENSAO":                   902,  # Bit: 6                              51VT
        "UG1_ATUA_RELE_86BF":                               902,  # Bit: 8                              OUT101
        "UG1_FALHA_ABERTURA_DJ_MAQUINA":                    902,  # Bit: 8                              50BFT
        "UG1_RECIBO_TRANSFER_DISPARO":                      902,  # Bit: 9                              OUT306
        "UG1_PERDA_CAMPO_GERAL":                            902,  # Bit: 11                             40Z1T, 40Z2T
        "UG1_FUGA_SOBRECORR_GERAL":                         902,  # Bit: 12                             64G1T, 64G2T, 64GX1T, 64F1T
        "UG1_UNIDADE_FORA_PASSO":                           902,  # Bit: 14                             OOST
        "UG1_RELE_ESTADO_TRIP":                             902,  # Bit: 15                             TRIP STATUS HI  ### PODE SER REG: 2100 BIT 00

        "UG1_RESET_TRIP_RELE":                              2100, # Bit: 0                              RESET COMMAND  ### PODE SER REG: 261 BIT 00
        "UG1_FALHA_PARTIDA_DJ_MAQUINA":                     2100, # Bit: 6                              IN403
        "UG1_DJ_MAQUINA_FECHADO":                           2100, # Bit: 10                             IN401
        "UG1_TRASFER_DISPARO_RELE_LINHA_TRAFO":             2100, # Bit: 11                             IN402

        "UG1_PERMISSAO_SINCRONISMO":                        2110, # Bit: 4                              OUT301
        "UG1_TRIP_RELE_PROTECAO":                           2110, # Bit: 5                              OUT302
        "UG1_TRIP_RELE_PROTECAO":                           2110, # Bit: 6                              OUT303
        "UG1_FALHA_ABERTURA_DJ_MAQUINA":                    2110, # Bit: 7                              OUT304


        # UG2
        "UG2_SOBREFREQ_ELEMENTO_2":                         1,    # Bit: 4                              81X4T (MOD 001)
        "UG2_SOBREFREQ_ELEMENTO_1":                         1,    # Bit: 5                              81X3T (MOD 001)
        "UG2_SUBFREQ_ELEMENTO_2":                           1,    # Bit: 6                              81X2T (MOD 001)
        "UG2_SUBFREQ_ELEMENTO_1":                           1,    # Bit: 7                              81X1T (MOD 001)

        "UG2_WATCHDOG_OP_NORMAL":                           313,  #                                     OUT305

        "UG2_SOBRECORR_INSTANTANEA":                        901,  # Bit: 0                              50PX1T
        "UG2_SOBRECORR_INSTANTANEA_NEUTRO":                 901,  # Bit: 1                              67N1T
        "UG2_SOBRECORR_SEQUENCIA_NEG":                      901,  # Bit: 2                              46Q2T
        "UG2_SOBRECORR_TEMPORIZADA_NEUTRO":                 901,  # Bit: 4                              51NT
        "UG2_DIFERENCIAL_COM_RESTRICAO":                    901,  # Bit: 14                             87R
        "UG2_DIFERENCIAL_SEM_RESTRICAO":                    901,  # Bit: 15                             87U

        "UG2_SUBTENSAO_GERAL":                              902,  # Bit: 0                              27PX1T, 27PX2T, 27PPX1T, 27PPX2T
        "UG2_SOBRETENSAO_GERAL":                            902,  # Bit: 1                              59PX1T, 59PX2T, 59PPX1T, 59PPX2T, 59GX1T, 59QX1T
        "UG2_POTENCIA_REVERSA":                             902,  # Bit: 3                              3PWRX1T
        "UG2_TRIP_RELACIONADO_FREQ":                        902,  # Bit: 4                              81
        "UG2_VOLTZ_HERTZ":                                  902,  # Bit: 5                              24C2T
        "UG2_SOBRECORR_RESTRICAO_TENSAO":                   902,  # Bit: 6                              51VT
        "UG2_ATUA_RELE_86BF":                               902,  # Bit: 8                              OUT101
        "UG2_FALHA_ABERTURA_DJ_MAQUINA":                    902,  # Bit: 8                              50BFT
        "UG2_RECIBO_TRANSFER_DISPARO":                      902,  # Bit: 9                              OUT306
        "UG2_PERDA_CAMPO_GERAL":                            902,  # Bit: 11                             40Z1T, 40Z2T
        "UG2_FUGA_SOBRECORR_GERAL":                         902,  # Bit: 12                             64G1T, 64G2T, 64GX1T, 64F1T
        "UG2_UNIDADE_FORA_PASSO":                           902,  # Bit: 14                             OOST
        "UG2_RELE_ESTADO_TRIP":                             902,  # Bit: 15                             TRIP STATUS HI  ### PODE SER REG: 2100 BIT 00

        "UG2_RESET_TRIP_RELE":                              2100, # Bit: 0                              RESET COMMAND  ### PODE SER REG: 261 BIT 00
        "UG2_FALHA_PARTIDA_DJ_MAQUINA":                     2100, # Bit: 6                              IN403
        "UG2_DJ_MAQUINA_FECHADO":                           2100, # Bit: 10                             IN401
        "UG2_TRASFER_DISPARO_RELE_LINHA_TRAFO":             2100, # Bit: 11                             IN402

        "UG2_PERMISSAO_SINCRONISMO":                        2110, # Bit: 4                              OUT301
        "UG2_TRIP_RELE_PROTECAO":                           2110, # Bit: 5                              OUT302
        "UG2_TRIP_RELE_PROTECAO":                           2110, # Bit: 6                              OUT303
        "UG2_FALHA_ABETRUA_DJ_MAQUINA":                     2110, # Bit: 7                              OUT304
    },

    "SE": {
        "RELE_ESTADO_TRIP":                                 39,   # Bit: 6                              TRIP STATUS HI (MOD 40)
        "RELE_FUNCIONAMENTO":                               39,   # Bit: 7                              ENABLED (MOD 40)

        "RESET_TRIP_RELE":                                  40,   # Bit: 2                              RESET COMMAND (MOD 41)

        "DJ_LINHA_FECHADO":                                 43,   # Bit: 0                              IN101 (MOD 44)
        "SECCION_LINHA_FECHADA":                            43,   # Bit: 1                              IN 102 (MOD 44)
        "FALHA_PARTIDA_RECE_RELE_TE":                       43,   # Bit: 2                              IN 103 (MOD 44)

        "TRIP_RELE_PROTECAO":                               44,   # Bit: 0                              OUT101 (MOD 45)
        "TRIP_RELE_PROTECAO":                               44,   # Bit: 1                              OUT102 (MOD 45)
        "WATCHDOG_OP_NORMAL":                               44,   # Bit: 2                              OUT103 (MOD 45)
        "FALHA_ABERTURA_DJ_LINHA":                          44,   # Bit: 3                              OUT104 (MOD 45)
        "FALHA_ABERTURA_DJ_LINHA":                          44,   # Bit: 4                              OUT105 (MOD 45)
        "ABRE_DJ_LINHA":                                    44,   # Bit: 5                              OUT106 (MOD 45)

        "SOBRECORR_INST_FASE_Z4":                           45,   # Bit: 5                              67P3T (MOD 46)
        "SOBRECORR_INST_FASE_Z3":                           45,   # Bit: 6                              67P2T (MOD 46)
        "SOBRECORR_INST_FASE_Z1":                           45,   # Bit: 7                              67P1T (MOD 46)

        "SOBRECORR_INST_SEQUEN_NEG_Z3":                     46,   # Bit: 1                              67Q3T (MOD 47)
        "SOBRECORR_INST_SEQUEN_NEG_Z2":                     46,   # Bit: 2                              67Q2T (MOD 47)
        "SOBRECORR_INST_SEQUEN_NEG_Z1":                     46,   # Bit: 3                              67Q1T (MOD 47)

        "SOBRECORR_TEMP_FASE":                              47,   # Bit: 2                              51PT (MOD 48)

        "FALHA_ABERTURA_DJ_LINHA":                          48,   # Bit: 1                              BFT (MOD 49)

        "ID_BARRA_VIVA":                                    49,   # Bit: 1                              (MOD 50)
        "ID_BARRA_MORTA":                                   49,   # Bit: 7                              (MOD 50)

        "ID_LINHA_VIVA":                                    50,   # Bit: 0                              (MOD 51)
        "ID_LINHA_MORTA":                                   50,   # Bit: 1                              (MOD 51)

        "SOBRETENSAO_NEUTRO":                               51,   # Bit: 4                              59N1T (MOD 52)
        "SOBRETENSAO_FASE_ELEMENTO_2":                      51,   # Bit: 5                              59P2T (MOD 52)
        "SUBTENSAO_FASE_ELEMETO_2":                         51,   # Bit: 6                              27P2T (MOD 52)
        "SUBTENSAO_FASE_ELEMETO_1":                         51,   # Bit: 7                              27P1T (MOD 52)

        "SOBREFREQ_ELEMENTO_6":                             52,   # Bit: 2                              81D6T (MOD 53)
        "SOBREFREQ_ELEMENTO_2":                             52,   # Bit: 3                              81D5T (MOD 53)
        "SOBREFREQ_ELEMENTO_1":                             52,   # Bit: 4                              81D4T (MOD 53)
        "SUBFREQ_ELEMENTO_3":                               52,   # Bit: 5                              81D3T (MOD 53)
        "SUBFREQ_ELEMENTO_2":                               52,   # Bit: 6                              81D2T (MOD 53)
        "SUBFREQ_ELEMENTO_1":                               52,   # Bit: 7                              81D1T (MOD 53)

        "ENVIO_TRANS_TRIP_RELE_BAY":                        53,   # Bit: 0                              SV8T (MOD 54)
        "RECEB_TRANSF_TRIP_RELE_BAY":                       53,   # Bit: 2                              SV6T (MOD 54)

        "RECEB_TRANSF_TRIP_RELE_BAY":                       54,   # Bit: 2                              SV10T (MOD 55)
        "RECEB_TRANSF_TRIP_RELE_BAY":                       54,   # Bit: 3                              SV9T (MOD 55)
    },

    "TE": {
        "DJ_LINHA_FECHADO":                                 35,   # Bit: 7                              IN301 (MOD 35)

        "TRANSFER_DISPARO_UG2":                             36,   # Bit: 1                              OUT303 (MOD 36)
        "TRANSFER_DISPARO_SE":                              36,   # Bit: 2                              OUT302 (MOD 36)
        "WATCHDOG_OP_NORMAL":                               36,   # Bit: 3                              OUT301 (MOD 36)
        "ATUA_86T":                                         36,   # Bit: 4                              OUT103 (MOD 36)
        "TRIP_RELE_PROTECAO":                               36,   # Bit: 5                              OUT102 (MOD 36)
        "FALHA_PARTIDA_RELE_LINHA":                         36,   # Bit: 6                              OUT101 (MOD 36)

        "SOBRECORR_TEMP_RESIDUAL_ENROL_SEC":                37,   # Bit: 1                              51N1T (MOD 37)
        "SOBRECORR_TEMP_FASE_ENROL_SEC":                    37,   # Bit: 6                              51P2T (MOD 37)

        "RESET_TRIP_RELE":                                  625,  # Bit: 0                              RESET COMMAND

        "RELE_FUNCIONAMENTO":                               675,  #                                     ENABLED

        "SOBRECORR_INSTAN_FASE":                            1117, # Bit: 0                              50P11T
        "SOBRECORR_INSTAN_RESIDUAL":                        1117, # Bit: 1                              50G11T
        "SOBRECORR_TEMP_FASE_ENROL_PRIM":                   1117, # Bit: 3                              51P1T
        "SOBRECORR_TEMP_RESIDUAL_ENROL_PRIM":               1117, # Bit: 4                              51G1T
        "DIFERENCIAL_COM_RESTRICAO":                        1117, # Bit: 14                             87R
        "DIFERENCIAL_SEM_RESTRICAO":                        1117, # Bit: 15                             87U

        "RELE_ESTADO_TRIP":                                 1118, # Bit: 15                             TRIP STATUS HI
    },

    "BAY": {
        "TENSAO_FASE_A":                                    10,   # VA                                  (MOD 11)
        "TENSAO_FASE_B":                                    13,   # VB                                  (MOD 14)
        "TENSAO_FASE_C":                                    16,   # VC                                  (MOD 17)
        "TENSAO_VS":                                        19,   # VS                                  (MOD 20)

        "RELE_ESTADO_TRIP":                                 39,   # Bit: 6                              TRIP STATUS HI (MOD 40)
        "RELE_FUNCIONAMENTO":                               39,   # Bit: 7                              ENABLED (MOD 40)

        "RESET_TRIP_RELE":                                  40,   # Bit: 2                              RESET COMMAND (MOD 41)

        "CMD_FECHA_DJ":                                     43,   # Bit: 2                              CC (MOD 44)
        "CMD_ABRE_DJ":                                      43,   # Bit: 3                              OC (MOD 44)

        "DJ_LINHA_FECHADO":                                 44,   # Bit: 0                              IN101 (MOD 045)
        "DJ_MOLA_CARREGADA":                                44,   # Bit: 1                              IN102 (MOD 045)
        "BT_ABRE_DJ":                                       44,   # Bit: 2                              IN103 (MOD 045)
        "BT_FECHA_DJ":                                      44,   # Bit: 3                              IN104 (MOD 045)
        "SECC_FECHADA":                                     44,   # Bit: 4                              IN105 (MOD 045)

        "FECHA_DJ":                                         45,   # Bit: 0                              OUT101 (MOD 46)
        "ABRE_DJ":                                          45,   # Bit: 1                              OUT102 (MOD 46)

        "SOBRECORR_INST_FASE_Z3":                           46,   # Bit: 5                              67P3T (MOD 47)
        "SOBRECORR_INST_FASE_Z2":                           46,   # Bit: 6                              67P2T (MOD 47)
        "SOBRECORR_INST_FASE_Z1":                           46,   # Bit: 7                              67P1T (MOD 47)

        "FALHA_ABERTURA_DJL":                               47,   # Bit: 1                              50BFX (MOD 48)

        "SOBRECORR_INST_SEQ_NEGATIVA_Z3":                   48,   # Bit: 1                              67Q3T (MOD 49)
        "SOBRECORR_INST_SEQ_NEGATIVA_Z2":                   48,   # Bit: 2                              67Q2T (MOD 49)
        "SOBRECORR_INST_SEQ_NEGATIVA_Z1":                   48,   # Bit: 3                              67Q1T (MOD 49)
        "SOBRECORR_RESID_INST":                             48,   # Bit: 7                              67G1T (MOD 49)

        "SOBRECORR_TEMP_FASE":                              49,   # Bit: 2                              51PT (MOD 50)

        "SOBRECORR_RESID_TEMP":                             50,   # Bit: 4                              51GT (MOD 51)

        "ENVIO_TRANSFER_TRIP_RELE_SE":                      51,   # Bit: 0                              50P1 OU 50Q1 (MOD 52)
        "RECEB_TRANSFER_TRIP_RELE_SE":                      51,   # Bit: 2                              - BF DISJUNTOR (MOD 52)

        "RECEB_TRANSFER_TRIP_RELE_SE":                      52,   # Bit: 3                              + 67P2 LOCAL (MOD 53)
        "RECEB_TRANSFER_TRIP_RELE_BAY":                     52,   # Bit: 7                              + 67Q2 LOCAL (MOD 53)

        "ID_BARRA_VIVA":                                    53,   # Bit: 1                              59A1 (MOD 54)
        "ID_BARRA_MORTA":                                   53,   # Bit: 7                              27A1 (MOD 54)

        "ID_LINHA_VIVA":                                    54,   # Bit: 0                              59S1P (MOD 55)
        "ID_LINHA_MORTA":                                   54,   # Bit: 1                              27SP (MOD 55)
    }
}

REG_CLP = {
    
}