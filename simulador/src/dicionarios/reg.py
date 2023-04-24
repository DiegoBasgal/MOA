MB = {
    # SE
    # Comandos
    "CMD_SE_FECHA_52L": 0,# Bit 04 # "REG_USINA_Disj52LFechar": False,

    # SA
    # Comandos
    "RESET_FALHAS_BARRA_CA": 1, #  Bit 00 # "REG_USINA_ResetAlarmes": 0,

    # Status M
    "LT_VAB": 2, # .Value # "REG_USINA_Subestacao_TensaoRS": 23100,
    "LT_VBC": 3, # .Value # "REG_USINA_Subestacao_TensaoST": 23100,
    "LT_VCA": 4, # .Value # "REG_USINA_Subestacao_TensaoTR": 23100,
    "LT_P": 5, # .Value # "REG_USINA_Subestacao_PotenciaAtivaMedia": 0,

    # TA
    # Comandos
    "CP1_CMD_ABERTURA_CRACKING": 6, # Bit 01  (%M200.1)
    "CP1_CMD_ABERTURA_TOTAL": 7, # Bit 02  (%M200.2)
    "CP1_CMD_FECHAMENTO": 8, # Bit 03  (%M200.3)

    "CP2_CMD_ABERTURA_CRACKING": 9, # Bit 01  (%M200.1)
    "CP2_CMD_ABERTURA_TOTAL": 10, # Bit 02  (%M200.2)
    "CP2_CMD_FECHAMENTO": 11, # Bit 03  (%M200.3)

    # Status A
    "NIVEL_MONTANTE": 12, # .Value # "REG_USINA_NivelBarragem": 461.80,
    "NIVEL_JUSANTE_GRADE_COMPORTA_1": 13, # .Value # "REG_USINA_NivelCanalAducao1": 0,
    "NIVEL_JUSANTE_GRADE_COMPORTA_2": 14, # .Value # "REG_USINA_NivelCanalAducao2": 0,
    
    # Status D 
    "CP1_COMPORTA_OPERANDO": 15, # Bit 00 # "REG_UG1_Status_Comporta": 14906 - 1 + 20000,
    "CP1_PERMISSIVOS_OK": 16, # Bit 31 # "REG_UG1_Permissao_Comporta": 14907 - 1 + 20000,
    "CP2_COMPORTA_OPERANDO": 17, # Bit 00 # "REG_UG2_Status_Comporta": 14906 - 1 + 30000,
    "CP2_PERMISSIVOS_OK": 18, # Bit 31 # "REG_UG2_Permissao_Comporta": 14907 - 1 + 30000,


    # UG1
    # Comandos
    "UG1_CMD_RESET_FALHAS_PASSOS": 19, # Bit 00 # "REG_UG1_Operacao_ResetAlarmes": 12289 - 1 + 20000,
    "UG1_CMD_PARADA_CMD_PARA_RV_APLICA_FREIO": 20, # Bit 13 # "REG_UG1_Operacao_UP": 12291 - 1 + 20000,
    "UG1_CMD_PARTIDA_CMD_SINCRONISMO": 21, # Bit 10 # "REG_UG1_Operacao_UPS": 12294 - 1 + 20000,
    "UG1_CMD_PARADA_EMERGENCIA": 22, # Bit 04 # "REG_UG1_Operacao_EmergenciaLigar": 12296 - 1 + 20000,
    
    # Status M H
    "UG1_UG_P": 23, # .Value # "REG_UG1_Gerador_PotenciaAtivaMedia": 12837 - 1 + 20000,
    "UG1_UG_HORIMETRO": 24, # Bit 22 # "REG_UG1_HorimetroEletrico_Hora": 12866 - 1 + 20000,
    
    # Status A
    "UG1_TEMP_GERADOR_FASE_A": 25, # .Value # "REG_UG1_Temperatura_01": 12871 - 1 + 20000,
    "UG1_TEMP_GERADOR_FASE_B": 26, # .Value # "REG_UG1_Temperatura_02": 12872 - 1 + 20000,
    "UG1_TEMP_GERADOR_FASE_C": 27, # .Value # "REG_UG1_Temperatura_03": 12873 - 1 + 20000,
    "UG1_TEMP_GERADOR_NUCLEO": 28, # .Value # "REG_UG1_Temperatura_04": 12874 - 1 + 20000,
    "UG1_TEMP_MANCAL_GUIA_GERADOR": 29, # .Value # "REG_UG1_Temperatura_05": 12875 - 1 + 20000,
    "UG1_TEMP_1_MANCAL_GUIA_INTERNO": 30, # .Value # "REG_UG1_Temperatura_06": 12876 - 1 + 20000,
    "UG1_TEMP_2_MANCAL_GUIA_INTERNO": 31, # .Value # "REG_UG1_Temperatura_07": 12877 - 1 + 20000,
    "UG1_TEMP_1_PATINS_MANCAL_COMBINADO": 32, # .Value # "REG_UG1_Temperatura_08": 12878 - 1 + 20000,
    "UG1_TEMP_2_PATINS_MANCAL_COMBINADO": 33, # .Value # "REG_UG1_Temperatura_09": 12879 - 1 + 20000,
    "UG1_TEMP_CASQ_MANCAL_COMBINADO": 34, # .Value # "REG_UG1_Temperatura_10": 12880 - 1 + 20000,
    "UG1_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO": 35, # .Value # "REG_UG1_Temperatura_11": 12881 - 1 + 20000,
    "UG1_PRESSAO_ENTRADA_TURBINA": 36, # .Value # "REG_UG1_Pressao_Turbina": 14904 - 1 + 20000,
    
    
    # UG2
    # Comandos
    "UG2_CMD_RESET_FALHAS_PASSOS": 37, # Bit 00 # "REG_UG2_Operacao_ResetAlarmes": 12289 - 1 + 30000,
    "UG2_CMD_PARADA_CMD_PARA_RV_APLICA_FREIO": 38, # Bit 13 # "REG_UG2_Operacao_UP": 12291 - 1 + 30000,
    "UG2_CMD_PARTIDA_CMD_SINCRONISMO": 39, # Bit 10 # "REG_UG2_Operacao_UPS": 12294 - 1 + 30000,
    "UG2_CMD_PARADA_EMERGENCIA": 40, # Bit 04 # "REG_UG2_Operacao_EmergenciaLigar": 12296 - 1 + 30000,
    
    # Status M H
    "UG2_UG_P": 41, # .Value # "REG_UG2_Gerador_PotenciaAtivaMedia": 12837 - 1 + 30000,
    "UG2_UG_HORIMETRO": 42, # Bit 22 # "REG_UG2_HorimetroEletrico_Hora": 12866 - 1 + 30000,
    
    # Status A
    "UG2_TEMP_GERADOR_FASE_A": 43, # .Value # "REG_UG2_Temperatura_01": 12871 - 1 + 30000,
    "UG2_TEMP_GERADOR_FASE_B": 44, # .Value # "REG_UG2_Temperatura_02": 12872 - 1 + 30000,
    "UG2_TEMP_GERADOR_FASE_C": 45, # .Value # "REG_UG2_Temperatura_03": 12873 - 1 + 30000,
    "UG2_TEMP_GERADOR_NUCLEO": 46, # .Value # "REG_UG2_Temperatura_04": 12874 - 1 + 30000,
    "UG2_TEMP_MANCAL_GUIA_GERADOR": 47, # .Value # "REG_UG2_Temperatura_05": 12875 - 1 + 30000,
    "UG2_TEMP_1_MANCAL_GUIA_INTERNO": 48, # .Value # "REG_UG2_Temperatura_06": 12876 - 1 + 30000,
    "UG2_TEMP_2_MANCAL_GUIA_INTERNO": 49, # .Value # "REG_UG2_Temperatura_07": 12877 - 1 + 30000,
    "UG2_TEMP_1_PATINS_MANCAL_COMBINADO": 50, # .Value # "REG_UG2_Temperatura_08": 12878 - 1 + 30000,
    "UG2_TEMP_2_PATINS_MANCAL_COMBINADO": 51, # .Value # "REG_UG2_Temperatura_09": 12879 - 1 + 30000,
    "UG2_TEMP_CASQ_MANCAL_COMBINADO": 52, # .Value # "REG_UG2_Temperatura_10": 12880 - 1 + 30000,
    "UG2_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO": 53, # .Value # "REG_UG2_Temperatura_11": 12881 - 1 + 30000,
    "UG2_PRESSAO_ENTRADA_TURBINA": 54, # .Value # "REG_UG2_Pressao_Turbina": 14904 - 1 + 30000,

    "REG_USINA_Condicionadores": 14903 - 1 + 20000,
    "REG_USINA_potencia_kw_mp": 14900 - 1 + 10000,
    "REG_USINA_potencia_kw_mr": 14901 - 1 + 10000,
    
    "UG1_RV_ESTADO_OPERACAO": 55, # "REG_UG1_Operacao_EtapaAtual": 12774 - 1 + 20000,
    
    "REG_UG1_Condicionadores": 14903 - 1 + 20000,
    "REG_UG1_CtrlPotencia_Alvo": 13569 - 1 + 17 + 20000,
    
    "UG2_RV_ESTADO_OPERACAO": 55, # "REG_UG2_Operacao_EtapaAtual": 12774 - 1 + 30000,

    "REG_UG2_Condicionadores": 14903 - 1 + 30000,
    "REG_UG2_CtrlPotencia_Alvo": 13569 + 17 - 1 + 30000,

}
