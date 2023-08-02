## Dicionário de siglas

# ED -> Entradas Digitais
# RD -> Retornos Digitais
# CD -> Comandos Digitais
# EA -> Entradas Analógicas
# RA -> Retornos Analógicos
# SA -> Saídas Analógicas

REG = {
    ### MOA

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
}