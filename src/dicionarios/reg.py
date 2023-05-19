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

    ## ENTRADAS ANALÓGICAS
    # ALARMES\NÍVEIS
    "SA_EA_STT_ALARMES_HH_ANALOGICAS":                  12340,       # Input Register                       (OP -> 0x04 Read Input Registers)
    "SA_EA_STT_ALARMES_H_ANALOGICAS":                   12342,       # Input Register                       (OP -> 0x04 Read Input Registers)
    "SA_EA_STT_ALARMES_L_ANALOGICAS":                   12344,       # Input Register                       (OP -> 0x04 Read Input Registers)
    "SA_EA_STT_ALARMES_LL_ANALOGICAS":                  12346,       # Input Register                       (OP -> 0x04 Read Input Registers)

    # FALHAS\NÍVEIS
    "SA_EA_STT_FALHAS_ANALOGICAS":                      12338,      # Input Register                        (OP -> 0x04 Read input Registers)

    # LEITURAS\NÍVEIS
    "SA_EA_NIVEL_JUSANTE_CASA_FORCA":                   12448,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "SA_EA_NIVEL_MONTANTE_TA":                          12448,      # Input Register                        (OP -> 0x04 Read Input Registers)

    # LEITURAS\PRESSÃO
    "SA_EA_SFA_LADO_LIMPO":                             12500,      # Input Register                        (OP -> 0X04 Read Input Registers)
    "SA_EA_SFA_LADO_SUJO":                              12502,      # Input Register                        (OP -> 0X04 Read Input Registers)
    "SA_EA_SFB_LADO_LIMPO":                             12504,      # Input Register                        (OP -> 0X04 Read Input Registers)
    "SA_EA_SFB_LADO_SUJO":                              12506,      # Input Register                        (OP -> 0X04 Read Input Registers)

    ## ENTRADAS DIGITAIS
    # BLOQUEIOS
    "SA_ED_STT_BLOQUEIO_50BF":                          12350,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "SA_ED_STT_BLOQUEIO_86BTLSA":                       12352,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # ENTRADAS CLP
    "SA_ED_STT_ENTRADAS_DIGITAIS_0":                    12308,      # Holding Register                      (OP -> 0x03 Read holding Registers)
    "SA_ED_STT_ENTRADAS_DIGITAIS_1":                    12310,      # Holding Register                      (OP -> 0x03 Read holding Registers)
    "SA_ED_STT_ENTRADAS_DIGITAIS_2":                    12312,      # Holding Register                      (OP -> 0x03 Read holding Registers)

    # SA_SE
    "SA_ED_STT_SA_SE":                                  12348,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

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
    "UG1_CD_CMD_UHRV":                                  12290,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_UHLM":                                  12292,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG1_CD_CMD_PARTIDA_PARADA":                        12294,      # Coil                                  (OP -> 0x15 Write Multiple Coils)

    ## ENTRADAS ANALÓGICAS
    # ALARMES\PRESSÃO
    "UG1_EA_STT_ALARMES_HH_ANALOGICAS":                 12340,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_STT_ALARMES_H_ANALOGICAS":                  12342,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_STT_ALARMES_L_ANALOGICAS":                  12344,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_STT_ALARMES_LL_ANALOGICAS":                 12346,      # Input Register                        (OP -> 0x04 Read Input Registers)

    # ALARMES\TEMPERATURA
    "UG1_EA_STT_ALARMES_HH_TEMPERATURA":                12330,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG1_EA_STT_ALARMES_H_TEMPERATURA":                 12332,      # Input Register                        (OP -> 0x04 Read Input Registers)

    # FALHAS\PRESSÃO
    "UG1_EA_STT_FALHAS_ANALOGICAS":                     12338,      # Input Register                        (OP -> 0x04 Read Input Registers)

    # FALHAS\TEMPERATURA
    "UG1_EA_STT_FALHAS_TEMPERATURA":                    12328,      # Input Register                        (OP -> 0x04 Read Input Registers)

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
    "UG1_ED_STT_BLOQUEIO_86E":                          12430,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_STT_BLOQUEIO_86H":                          12432,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # BORBOLETA
    "UG1_ED_REAL_ESTADO_BORBOLETA":                     12614,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_STT_BORBOLETA":                             12414,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # ENTRADAS CLP
    "UG1_ED_STT_ENTRADAS_DIGITAIS_0":                   12308,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_STT_ENTRADAS_DIGITAIS_1":                   12310,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_STT_ENTRADAS_DIGITAIS_2":                   12312,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_STT_ENTRADAS_DIGITAIS_3":                   12314,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_STT_ENTRADAS_DIGITAIS_4":                   12316,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # PARTIDA E PARADA
    "UG1_ED_STT_PASSO_ATUAL":                           12366,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_STT_PASSO_CONCLUIDO":                       12368,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_STT_PASSO_FALHA":                           12370,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_STT_PASSO_SELECIONADO":                     12372,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_STT_REAL_ESTADO_UNIDADE":                   12374,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG1_ED_STT_REAL_PASSO_ATUAL":                      12376,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # PERMISSIVOS
    "UG1_ED_STT_PRE_CONDICOES_PARTIDA":                 12408,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # RT
    "UG1_ED_STT_RT":                                    12362,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # RV
    "UG1_ED_STT_RV":                                    12360,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # UNIDADE GERADORA
    "UG1_ED_STT_UNIDADE_GERADORA":                      12348,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # UHLM
    "UG1_ED_STT_UHLM":                                  12354,      # Holding Reggister                     (OP -> 0x03 Read Holding Registers)

    # UHRV
    "UG1_ED_STT_UHRV":                                  12350,      # Holding Reggister                     (OP -> 0x03 Read Holding Registers)

    ## DRIVER RV
    "UG1_RV_ROTACAO":                                   16,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ESTADO_OPERACAO":                           21,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONTROLE_SINCRONIZADO_SELECIONADO":         22,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_CONTROLE_VAZIO_SELECIONADO":                23,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_COMANDO_MODBUS":                            24,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ENTRADAS_DIGITAIS":                         25,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SAIDAS_DIGIAIS":                            26,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_LIMITES_OPERACAO":                          27,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SETPOINT_ABERTURA_PU":                      28,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SETPOINT_VELOCIDADE":                       29,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SETPOINT_POTENCIA_ATIVA_PU":                30,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SAIDA_CONTROLE_DISTRIBUIDOR":               32,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SAIDA_CONTROLE_DISTRIBUIDOR_PU":            32,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SAIDA_CONTROLE_ROTOR":                      33,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_SAIDA_CONTROLE_ROTOR_PU":                   33,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_REFERENCIA_DISTRIBUIDOR_PU":                36,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FEEDBACK_DISTRIBUIDOR_PU":                  37,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_REFERENCIA_ROTOR_PU":                       42,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FEEDBACK_ROTOR_PU":                         43,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_REFERENCIA_VELOCIDADE_PU":                  48,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FEEDBACK_VELOCIDADE_PU":                    49,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_REFERENCIA_POTENCIA_ATIVA_PU":              54,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FEEDBACK_POTENCIA_ATIVA_PU":                55,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_ALARME":                                    66,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_1":                                   67,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RV_FALHA_2":                                   68,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
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
    "UG1_RT_CONTROLE_SINCRONIZADO_SELECIONADO":         27,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ENTRADAS_DIGITAIS":                         30,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_SAIDAS_DIGITAIS":                           31,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_LIMITES_OPERACAO":                          32,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
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
    "UG1_RT_ALARMES_1":                                 70,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_ALARMES_2":                                 71,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_1":                                  72,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_2":                                  73,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG1_RT_FALHAS_3":                                  74,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
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
    "UG2_CD_CMD_UHRV":                                  12290,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_UHLM":                                  12292,      # Coil                                  (OP -> 0x15 Write Multiple Coils)
    "UG2_CD_CMD_PARTIDA_PARADA":                        12294,      # Coil                                  (OP -> 0x15 Write Multiple Coils)

    ## ENTRADAS ANALÓGICAS
    # ALARMES\PRESSÃO
    "UG2_EA_STT_ALARMES_HH_ANALOGICAS":                 12340,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_STT_ALARMES_H_ANALOGICAS":                  12342,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_STT_ALARMES_L_ANALOGICAS":                  12344,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_STT_ALARMES_LL_ANALOGICAS":                 12346,      # Input Register                        (OP -> 0x04 Read Input Registers)

    # ALARMES\TEMPERATURA
    "UG2_EA_STT_ALARMES_HH_TEMPERATURA":                12330,      # Input Register                        (OP -> 0x04 Read Input Registers)
    "UG2_EA_STT_ALARMES_H_TEMPERATURA":                 12332,      # Input Register                        (OP -> 0x04 Read Input Registers)

    # FALHAS\PRESSÃO
    "UG2_EA_STT_FALHAS_ANALOGICAS":                     12338,      # Input Register                        (OP -> 0x04 Read Input Registers)

    # FALHAS\TEMPERATURA
    "UG2_EA_STT_FALHAS_TEMPERATURA":                    12328,      # Input Register                        (OP -> 0x04 Read Input Registers)

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
    "UG2_ED_STT_BLOQUEIO_86E":                          12430,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_STT_BLOQUEIO_86H":                          12432,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # BORBOLETA
    "UG2_ED_REAL_ESTADO_BORBOLETA":                     12614,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_STT_BORBOLETA":                             12414,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # ENTRADAS CLP
    "UG2_ED_STT_ENTRADAS_DIGITAIS_0":                   12308,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_STT_ENTRADAS_DIGITAIS_1":                   12310,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_STT_ENTRADAS_DIGITAIS_2":                   12312,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_STT_ENTRADAS_DIGITAIS_3":                   12314,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_STT_ENTRADAS_DIGITAIS_4":                   12316,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # PARTIDA E PARADA
    "UG2_ED_STT_PASSO_ATUAL":                           12366,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_STT_PASSO_CONCLUIDO":                       12368,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_STT_PASSO_FALHA":                           12370,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_STT_PASSO_SELECIONADO":                     12372,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_STT_REAL_ESTADO_UNIDADE":                   12374,      # Holding Register                      (OP -> 0x03 Read Holding Registers)
    "UG2_ED_STT_REAL_PASSO_ATUAL":                      12376,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # PERMISSIVOS
    "UG2_ED_STT_PRE_CONDICOES_PARTIDA":                 12408,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # RT
    "UG2_ED_STT_RT":                                    12362,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # RV
    "UG2_ED_STT_RV":                                    12360,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # UNIDADE GERADORA
    "UG2_ED_STT_UNIDADE_GERADORA":                      12348,      # Holding Register                      (OP -> 0x03 Read Holding Registers)

    # UHLM
    "UG2_ED_STT_UHLM":                                  12354,      # Holding Reggister                     (OP -> 0x03 Read Holding Registers)

    # UHRV
    "UG2_ED_STT_UHRV":                                  12350,      # Holding Reggister                     (OP -> 0x03 Read Holding Registers)

    ## DRIVER RV
    "UG2_RV_ROTACAO":                                   16,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ESTADO_OPERACAO":                           21,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONTROLE_SINCRONIZADO_SELECIONADO":         22,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_CONTROLE_VAZIO_SELECIONADO":                23,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_COMANDO_MODBUS":                            24,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ENTRADAS_DIGITAIS":                         25,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SAIDAS_DIGIAIS":                            26,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_LIMITES_OPERACAO":                          27,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SETPOINT_ABERTURA_PU":                      28,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SETPOINT_VELOCIDADE":                       29,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SETPOINT_POTENCIA_ATIVA_PU":                30,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SAIDA_CONTROLE_DISTRIBUIDOR":               32,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SAIDA_CONTROLE_DISTRIBUIDOR_PU":            32,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SAIDA_CONTROLE_ROTOR":                      33,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_SAIDA_CONTROLE_ROTOR_PU":                   33,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_REFERENCIA_DISTRIBUIDOR_PU":                36,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FEEDBACK_DISTRIBUIDOR_PU":                  37,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_REFERENCIA_ROTOR_PU":                       42,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FEEDBACK_ROTOR_PU":                         43,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_REFERENCIA_VELOCIDADE_PU":                  48,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FEEDBACK_VELOCIDADE_PU":                    49,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_REFERENCIA_POTENCIA_ATIVA_PU":              54,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FEEDBACK_POTENCIA_ATIVA_PU":                55,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_ALARME":                                    66,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_1":                                   67,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RV_FALHA_2":                                   68,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
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
    "UG2_RT_CONTROLE_SINCRONIZADO_SELECIONADO":         27,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ENTRADAS_DIGITAIS":                         30,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_SAIDAS_DIGITAIS":                           31,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_LIMITES_OPERACAO":                          32,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_SETPOINT_TENSAO_PU":                        40,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_SETPOINT_POTENCIA_REATIVA_PU":              41,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_SETPOINT_FATOR_POTENCIA_PU":                42,         # Input Register -1                     (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ABERTURA_PONTE":                            43,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_REFERENCIA_CORRENTE_CAMPO_PU":              46,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FEEDBACK_CORRENTE_CAMPO_PU":                47,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_REFERENCIA_TENSAO_PU":                      52,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FEEDBACK_TENSAO_PU":                        53,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_REFERENCIA_POTENCIA_REATIVA_PU":            58,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FEEDBACK_POTENCIA_REATIVA_PU":              59,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_REFERENCIA_FATOR_POTENCIA_PU":              64,         # Input Register Scale 0.01             (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FEEDBACK_FATOR_POTENCIA_PU":                65,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_1":                                 70,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_ALARMES_2":                                 71,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_1":                                  72,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_2":                                  73,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
    "UG2_RT_FALHAS_3":                                  74,         # Input Register                        (OP -> 0x04 Read Input Registers - 3x)
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

REG_RELES = {
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


### Registradores mantidos do mapa antigo por não saber qual o equivalente do mapa novo

# Não sei se tem e se tem, não sei qual é:
REG_UG["UG1_EA_PressK1CaixaExpiral_MaisCasas"] = 157 # Scale 0.01 - Op04 (Read Input Registers)
REG_UG["UG2_EA_PressK1CaixaExpiral_MaisCasas"] = 157 # Scale 0.01 - Op04 (Read Input Registers)


### Registradores utilizados na simulação, para voltar aos valores antigos, deletar os comentarios de linha "#antigo->" e manter o número.

UG = {
    "REG_UG1_RetrornosAnalogicos_AUX_Condicionadores": 34902,

    "UG1_CD_EmergenciaViaSuper": 34902, #antigo -> 4  # Op15 (Write multiple coils)
    "UG1_CD_IniciaPartida": 32294, #antigo -> 45  # Op15 (Write multiple coils)
    "UG1_CD_IniciaParada": 32290, #antigo -> 46  # Op15 (Write multiple coils)
    "UG1_RD_TripEletrico": 34904, #antigo -> 134  # Op02 (Read Input Status)
    "UG1_RD_TripMecanico": 34198, #antigo -> 135  # Op02 (Read Input Status)
    "UG1_RA_Temperatura_01": 32871, #antigo -> 24  # Op04 (Read Input Registers - 3x)
    "UG1_RA_Temperatura_02": 32872, #antigo -> 25  # Op04 (Read Input Registers - 3x)
    "UG1_RA_Temperatura_03": 32873, #antigo -> 26  # Op04 (Read Input Registers - 3x)
    "UG1_RA_Temperatura_04": 32874, #antigo -> 27  # Op04 (Read Input Registers - 3x)
    "UG1_RA_Temperatura_05": 32875, #antigo -> 28  # Op04 (Read Input Registers - 3x)
    "UG1_RA_Temperatura_06": 32876, #antigo -> 29  # Op04 (Read Input Registers - 3x)
    "UG1_RA_Temperatura_07": 32877, #antigo -> 30  # Op04 (Read Input Registers - 3x)
    "UG1_RA_Temperatura_08": 32878, #antigo -> 31  # Op04 (Read Input Registers - 3x)
    "UG1_RA_Temperatura_09": 32879, #antigo -> 32  # Op04 (Read Input Registers - 3x)
    "UG1_RA_PM_710_Potencia_Ativa": 32836, #antigo->45  # Op04 (Read Input Registers - 3x)
    "UG1_SD_SPPotAtiva": 33585, #antigo -> 1  # Scale - Op16 (Preset Multiple Registers - 4x)
    "UG1_EA_PressK1CaixaExpiral": 34903,  # Scale 0.1 - Op04 (Read Input Registers - 3x)
    "UG1_ED_FreioPastilhaGasta": 30000, # antigo -> 24  # Op02 (Read Input Status)
    "UG1_ED_FiltroPresSujo75Troc": 30001, # antigo -> 37  # Op02 (Read Input Status)
    "UG1_ED_FiltroRetSujo75Troc": 30002, # antigo -> 39  # Op02 (Read Input Status)
    "UG1_ED_UHLM_Filt1PresSujo75Troc": 30003, # antigo -> 59  # Op02 (Read Input Status)
    "UG1_ED_UHLM_Filt2PresSujo75Troc": 30004, # antigo -> 61  # Op02 (Read Input Status)
    "UG1_ED_FiltroPressaoBbaMecSj75": 30005, # antigo -> 65  # Op02 (Read Input Status)
    "UG1_ED_TripPartRes": 30006, # antigo -> 82  # Op02 (Read Input Status)
    "UG1_RD_FalhaComunG1TDA": 30007, # antigo -> 212  # Op02 (Read Input Status)



    "REG_UG2_RetrornosAnalogicos_AUX_Condicionadores": 44902,
    "UG2_CD_EmergenciaViaSuper": 42295, #antigo -> 4  # Op15 (Write multiple coils)
    "UG2_CD_IniciaPartida": 42294, #antigo -> 45  # Op15 (Write multiple coils)
    "UG2_CD_IniciaParada": 42290, #antigo -> 46  # Op15 (Write multiple coils)
    "UG2_RD_TripEletrico": 44904,  #antigo -> 134# Op02 (Read Input Status)
    "UG2_RD_TripMecanico": 44198,  #antigo -> 135 # Op02 (Read Input Status)
    "UG2_RA_Temperatura_01": 42871, #antigo -> 24  # Op04 (Read Input Registers - 3x)
    "UG2_RA_Temperatura_02": 42872, #antigo -> 25  # Op04 (Read Input Registers - 3x)
    "UG2_RA_Temperatura_03": 42873, #antigo -> 26  # Op04 (Read Input Registers - 3x)
    "UG2_RA_Temperatura_04": 42874, #antigo -> 27  # Op04 (Read Input Registers - 3x)
    "UG2_RA_Temperatura_05": 42875, #antigo -> 28  # Op04 (Read Input Registers - 3x)
    "UG2_RA_Temperatura_06": 42876, #antigo -> 29  # Op04 (Read Input Registers - 3x)
    "UG2_RA_Temperatura_07": 42877, #antigo -> 30  # Op04 (Read Input Registers - 3x)
    "UG2_RA_Temperatura_08": 42878, #antigo -> 31  # Op04 (Read Input Registers - 3x)
    "UG2_RA_Temperatura_09": 42879, #antigo -> 32  # Op04 (Read Input Registers - 3x)
    "UG2_RA_PM_710_Potencia_Ativa": 42836, #antigo ->45  # Op04 (Read Input Registers - 3x)
    "UG2_SD_SPPotAtiva": 43585, #antigo -> 1  # Scale - Op16 (Preset Multiple Registers - 4x)
    "UG2_EA_PressK1CaixaExpiral": 44903,  # Scale 0.1 - Op04 (Read Input Registers - 3x)

    "UG2_ED_FreioPastilhaGasta": 40000, # antigo -> 24  # Op02 (Read Input Status)
    "UG2_ED_FiltroPresSujo75Troc": 40001, # antigo -> 37  # Op02 (Read Input Status)
    "UG2_ED_FiltroRetSujo75Troc": 40002, # antigo -> 39  # Op02 (Read Input Status)
    "UG2_ED_UHLM_Filt1PresSujo75Troc": 40003, # antigo -> 59  # Op02 (Read Input Status)
    "UG2_ED_UHLM_Filt2PresSujo75Troc": 40004, # antigo -> 61  # Op02 (Read Input Status)
    "UG2_ED_FiltroPressaoBbaMecSj75": 40005, # antigo -> 65  # Op02 (Read Input Status)
    "UG2_ED_TripPartRes": 40006, # antigo -> 82  # Op02 (Read Input Status)
    "UG2_RD_FalhaComunG2TDA": 40007, # antigo -> 210  # Op02 (Read Input Status)
}

SA = {
    "SA_CD_ResetGeral": 22288, #antigo -> 0  # Scale - Op15 (Write multiple coils)
    "SA_CD_Liga_DJ1": 22293, #antigo -> 17  # Scale - Op15 (Write multiple coils)
    "SA_RA_Medidor_potencia_kw_mp": 24900, # Op04 (Read Input Registers - 3x)
    "SA_RA_PM_810_Tensao_AB": 22789, #antigo -> 16  # Scale 0.1 - Op04 (Read Input Registers - 3x)
    "SA_RA_PM_810_Tensao_BC": 22790, #antigo -> 17  # Scale 0.1 - Op04 (Read Input Registers - 3x)
    "SA_RA_PM_810_Tensao_CA": 22791, #antigo -> 18  # Scale 0.1 - Op04 (Read Input Registers - 3x)
    "SA_RA_PM_810_Potencia_Ativa": 22799,  # Op04 (Read Input Registers - 3x)
    "SA_ED_QLCF_Disj52EFechado": 20000, # antigo -> 84  # Op02 (Read Discrete Inputs)
    "SA_ED_QLCF_Disj52ETrip": 20001, # antigo -> 85  # Op02 (Read Discrete Inputs)
    "SA_ED_QLCF_TripDisjAgrup": 20002, # antigo -> 86  # Op02 (Read Discrete Inputs)
    "SA_ED_QCAP_Disj52EFechado": 20003, # antigo -> 101  # Op02 (Read Discrete Inputs)
    "SA_ED_QCAP_SubtensaoBarraGeral": 20004, # antigo -> 106  # Op02 (Read Discrete Inputs)
    "SA_ED_GMG_Alarme": 20005, # antigo -> 112  # Op02 (Read Discrete Inputs)
    "SA_ED_GMG_Trip": 20006, # antigo -> 113  # Op02 (Read Discrete Inputs)
    "SA_ED_GMG_Operacao": 20007, # antigo -> 114  # Op02 (Read Discrete Inputs)
    "SA_ED_GMG_BaixoComb": 20008, # antigo -> 115  # Op02 (Read Discrete Inputs)
    "SA_RD_BbaDren1_FalhaAcion": 20009, # antigo -> 168  # Op02 (Read Input Status - 1x)
    "SA_RD_BbaDren2_FalhaAcion": 20010, # antigo -> 169  # Op02 (Read Input Status - 1x)
    "SA_RD_BbaDren3_FalhaAcion": 20011, # antigo -> 170  # Op02 (Read Input Status - 1x)
    "SA_RD_GMG_FalhaAcion": 20012, # antigo -> 175  # Op02 (Read Input Status - 1x)
    "SA_RD_FalhaComunSETDA": 20013, # antigo -> 177  # Op02 (Read Input Status - 1x)
}

TDA = {
    "REG_TDA_NivelMaisCasasAntes": 22766, #antigo -> 12  # Scale 400 + 0.0001 X - Op04 (Read Input Registers - 3x)
    "TDA_EA_NivelDepoisGrade": 22767, # antgo -> 1  # Scale 0.01 - Op04 (Read Input Registers - 3x)
}