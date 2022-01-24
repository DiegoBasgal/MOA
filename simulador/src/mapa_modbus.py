REG = {
    "REG_UG1_Alarme01" : 1001,  # & (2**0)
    "REG_UG1_CtrlPotencia_Alvo" : 1002,  # setpoint
    "REG_UG1_Gerador_PotenciaAtivaMedia" : 1004,  # * 0.001
    "REG_UG1_HorimetroEletrico_Low" : 1005,  #
    "REG_UG1_Operacao_EmergenciaDesligar" : 1006,  # 1 => True
    "REG_UG1_Operacao_EmergenciaLigar" : 1007,  # 1 => True
    "REG_UG1_Operacao_EtapaAlvo" : 1008, # >> 0 & 1
    "REG_UG1_Operacao_EtapaAtual" : 1009,  #
    "REG_UG1_Operacao_PCH_CovoReconheceAlarmes" : 1010,  # 1 => True
    "REG_UG1_Operacao_PCH_CovoResetAlarmes" : 1011,  # 1 => True
    "REG_UG1_Operacao_UP" : 1012,  # 1 => True
    "REG_UG1_Operacao_US" : 1013,  # 1 => True
    "REG_UG1_Temperatura_01" : 1014,  # Gerador 1 - Enrolamento Fase R
    "REG_UG1_Temperatura_02" : 1015,  # Gerador 1 - Enrolamento Fase S
    "REG_UG1_Temperatura_03" : 1016,  # Gerador 1 - Enrolamento fase T
    "REG_UG1_Temperatura_04" : 1017,  # Gerador 1 - Mancal L.A. Escora 01 
    "REG_UG1_Temperatura_05" : 1018,  # Gerador 1 - Mancal L.A. Escora 02
    "REG_UG1_Temperatura_06" : 1019,  # Gerador 1 - Mancal L. A. Casquilho
    "REG_UG1_Temperatura_07" : 1020,  # Gerador 1 - Mancal L. A. Contra Escora 01
    "REG_UG1_Temperatura_08" : 1021,  # Gerador 1 - Mancal L.N.A. Casquilho
    "REG_UG1_Temperatura_09" : 1022,  # Gerador 1 - Mancal L. A. Contra Escora 02
    "REG_UG1_Turb_Info" : 1023,  # ???

    "REG_UG2_Alarme01" : 2001,  # & (2**0)
    "REG_UG2_CtrlPotencia_Alvo" : 2002,  # setpoint
    "REG_UG2_Gerador_PotenciaAtivaMedia" : 2004,  # * 0.001
    "REG_UG2_HorimetroEletrico_Low" : 2005,  #
    "REG_UG2_Operacao_EmergenciaDesligar" : 2006,  # 1 => True
    "REG_UG2_Operacao_EmergenciaLigar" : 2007,  # 1 => True
    "REG_UG2_Operacao_EtapaAlvo" : 2008,  # >> 0 & 1
    "REG_UG2_Operacao_EtapaAtual" : 2009,  #
    "REG_UG2_Operacao_PCH_CovoReconheceAlarmes" : 2010,  # 1 => True
    "REG_UG2_Operacao_PCH_CovoResetAlarmes" : 2011,  # 1 => True
    "REG_UG2_Operacao_UP" : 2012,  # 1 => True
    "REG_UG2_Operacao_US" : 2013,  # 1 => True
    "REG_UG2_Temperatura_01" : 2014,  # Gerador 2 - Enrolamento Fase R
    "REG_UG2_Temperatura_02" : 2015,  # Gerador 2 - Enrolamento Fase S
    "REG_UG2_Temperatura_03" : 2016,  # Gerador 2 - Enrolamento fase T
    "REG_UG2_Temperatura_04" : 2017,  # Gerador 2 - Mancal L.A. Escora 01 
    "REG_UG2_Temperatura_05" : 2018,  # Gerador 2 - Mancal L.A. Escora 02
    "REG_UG2_Temperatura_06" : 2019,  # Gerador 2 - Mancal L. A. Casquilho
    "REG_UG2_Temperatura_07" : 2020,  # Gerador 2 - Mancal L. A. Contra Escora 01
    "REG_UG2_Temperatura_08" : 2021,  # Gerador 2 - Mancal L.N.A. Casquilho
    "REG_UG2_Temperatura_09" : 2022,  # Gerador 2 - Mancal L. A. Contra Escora 02
    "REG_UG2_Turb_Info" : 2023,  # ???

    "REG_USINA_Disj52LFechar" : 3001,  # 1 => True
    "REG_USINA_EmergenciaDesligar" : 3002,  # 1 => True
    "REG_USINA_EmergenciaLigar" : 3003,  # 1 => True
    "REG_USINA_NivelBarragem" : 3004,  # / 100
    "REG_USINA_NivelCanalAducao" : 3005,  # / 100
    "REG_USINA_ReconheceAlarmes" : 3006,  # 1 => True 
    "REG_USINA_ResetAlarmes" : 3007,  # 1 => True
    "REG_USINA_Subestacao_Disj52L" : 3008,  # ???
    "REG_USINA_Subestacao_PotenciaAtivaMedia" : 3009,  # * 0.001
    "REG_USINA_Subestacao_TensaoRS" : 3010,  # * 10
    "REG_USINA_Subestacao_TensaoST" : 3011,  # * 10
    "REG_USINA_Subestacao_TensaoTR" : 3012,  # * 10
}