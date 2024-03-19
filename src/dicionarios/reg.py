REG_MOA = {
    "MOA_OUT_MODE":                                 11,
    "MOA_OUT_STATUS":                               409,

    "SM_STATE":                                     10,
    "PAINEL_LIDO":                                  12,

    # ENTRADAS
    "IN_EMERG":                                     13,
    "IN_HABILITA_AUTO":                             14,
    "IN_DESABILITA_AUTO":                           15,
    "IN_EMERG_UG1":                                 20,
    "IN_EMERG_UG2":                                 25,
    "IN_EMERG_UG3":                                 30,
    "IN_EMERG_UG4":                                 35,

    # SAÍDAS
    "OUT_EMERG":                                    16,
    "OUT_TARGET_LEVEL":                             417,
    "OUT_SETPOINT":                                 418,

    "OUT_BLOCK_UG1":                                21,
    "OUT_ETAPA_UG1":                                422,
    "OUT_STATE_UG1":                                423,

    "OUT_BLOCK_UG2":                                26,
    "OUT_STATE_UG2":                                427,
    "OUT_ETAPA_UG2":                                428,

    "OUT_BLOCK_UG3":                                31,
    "OUT_STATE_UG3":                                432,
    "OUT_ETAPA_UG3":                                433,

    "OUT_BLOCK_UG4":                                36,
    "OUT_STATE_UG4":                                437,
    "OUT_ETAPA_UG4":                                438,
}


                                                                                # NOME REGISTRADORES ELIPSE:
REG_SA = {
    ## COMANDOS
    # Gerais
    "CMD_RESET_ALARMES":                        0 + 12288,                      # Comandos.ResetAlarmes
    "CMD_RECONHECE_ALARMES":                    0 + 12289,                      # Comandos.ReconheceAlarmes
    "CMD_EMERGENCIA_LIGAR":                     1 + 12289,                      # Comandos.EmergenciaLigar
    "CMD_EMERGENCIA_DESLIGAR":                  2 + 12289,                      # Comandos.EmergenciaDesligar
    "CMD_SEL_MODO_LOCAL":                       5 + 12289,                      # Comandos.ServAuxiliar_SelecionaModoLocal
    "CMD_SEL_MODO_REMOTO":                      6 + 12289,                      # Comandos.ServAuxiliar_SelecionaModoRemoto
    "CMD_SEL_MODO_MANUAL":                      7 + 12289,                      # Comandos.ServAuxiliar_SelecionaModoManual
    "CMD_SEL_MODO_AUTOMATICO":                  8 + 12289,                      # Comandos.ServAuxiliar_SelecionaModoAutomatico

    # Disjuntor
    "CMD_DJ_FONTE_01_LIGAR":                    9 + 12289,                     # Comandos.ServAuxiliar_DisjFonte01Ligar
    "CMD_DJ_FONTE_01_DESLIGAR":                 10 + 12289,                     # Comandos.ServAuxiliar_DisjFonte01Desligar
    "CMD_DJ_FONTE_02_LIGAR":                    11 + 12289,                     # Comandos.ServAuxiliar_DisjFonte02Ligar
    "CMD_DJ_FONTE_02_DESLIGAR":                 12 + 12289,                     # Comandos.ServAuxiliar_DisjFonte02Desligar
    "CMD_DJ_FONTE_04_LIGAR":                    13 + 12289,                     # Comandos.ServAuxiliar_DisjFonte04Ligar
    "CMD_DJ_FONTE_04_DESLIGAR":                 14 + 12289,                     # Comandos.ServAuxiliar_DisjFonte04Desligar
    "CMD_DJ_FONTE_05_LIGAR":                    96 + 12289,                     # Comandos.ServAuxiliar_DisjFonte05Ligar
    "CMD_DJ_FONTE_05_DESLIGAR":                 97 + 12289,                     # Comandos.ServAuxiliar_DisjFonte05Desligar

    # Gerador Diesel
    "CMD_GD_PARTIR":                            15 + 12289,                     # Comandos.GrupoDiesel_Partir
    "CMD_GD_PARAR":                             16 + 12289,                     # Comandos.GrupoDiesel_Parar

    # Carregador de Baterias
    "CMD_CB_MODO_FLUTUACAO_LIGAR":              17 + 12289,                     # Comandos.CarregadorBateria_ModoFlutuacaoLigar
    "CMD_CB_MODO_EQUALIZACAO_LIGAR":            18 + 12289,                     # Comandos.CarregadorBateria_ModoEqualizacaoLigar

    # Poço
    "CMD_POCO_BOMBA_01_LIGAR":                  19 + 12289,                     # Comandos.Poco_Bomba01Ligar
    "CMD_POCO_BOMBA_01_DESLIGAR":               20 + 12289,                     # Comandos.Poco_Bomba01Desligar
    "CMD_POCO_BOMBA_01_PRINCIPAL":              21 + 12289,                     # Comandos.Poco_Bomba01Principal
    "CMD_POCO_BOMBA_02_LIGAR":                  22 + 12289,                     # Comandos.Poco_Bomba02Ligar
    "CMD_POCO_BOMBA_02_DESLIGAR":               23 + 12289,                     # Comandos.Poco_Bomba02Desligar
    "CMD_POCO_BOMBA_02_PRINCIPAL":              24 + 12289,                     # Comandos.Poco_Bomba02Principal
    "CMD_POCO_BOMBA_03_LIGAR":                  25 + 12289,                     # Comandos.Poco_Bomba03ligar
    "CMD_POCO_BOMBA_03_DESLIGAR":               26 + 12289,                     # Comandos.Poco_Bomba03Desligar
    "CMD_POCO_BOMBA_04_LIGAR":                  27 + 12289,                     # Comandos.Poco_Bomba04ligar
    "CMD_POCO_BOMBA_04_DESLIGAR":               28 + 12289,                     # Comandos.Poco_Bomba04Desligar
    "CMD_POCO_SEL_MODO_MANUAL":                 29 + 12289,                     # Comandos.Poco_SelecionaModoManual
    "CMD_POCO_SEL_MODO_AUTOMATICO":             30 + 12289,                     # Comandos.Poco_SelecionaModoAutomatico

    # Sensores
    "CMD_SENSOR_PRESEN_HABILITAR":              31 + 12289,                     # Comandos.SensorPresenca_Habilitar
    "CMD_SENSOR_PRESEN_DESABILITAR":            32 + 12289,                     # Comandos.SensorPresenca_Desabilitar
    "CMD_SENSOR_FUMACA_RESET":                  33 + 12289,                     # Comandos.[SensorFumaça_Reset]

    # Injeção Água Selo
    "CMD_IA_SELO_RODIZIO_AUTO":                 76 + 12289,                     # Comandos.InjecaoAguaSelo_RodizioAutomatico
    "CMD_IA_SELO_RODIZIO_MANUAL":               77 + 12289,                     # Comandos.InjecaoAguaSelo_RodizioManual
    "CMD_IA_SELO_BOMBA_01_LIGAR":               78 + 12289,                     # Comandos.InjecaoAguaSelo_Bomba01_Ligar
    "CMD_IA_SELO_BOMBA_01_DESLIGAR":            79 + 12289,                     # Comandos.InjecaoAguaSelo_Bomba01_Desligar
    "CMD_IA_SELO_BOMBA_01_PRINCIPAL":           80 + 12289,                     # Comandos.InjecaoAguaSelo_Bomba01_Principal
    "CMD_IA_SELO_BOMBA_02_LIGAR":               81 + 12289,                     # Comandos.InjecaoAguaSelo_Bomba02_Ligar
    "CMD_IA_SELO_BOMBA_02_DESLIGAR":            82 + 12289,                     # Comandos.InjecaoAguaSelo_Bomba02_Desligar
    "CMD_IA_SELO_BOMBA_02_PRINCIPAL":           83 + 12289,                     # Comandos.InjecaoAguaSelo_Bomba02_Principal

    # Água Serviço
    "CMD_AS_RODIZIO_AUTO":                      84 + 12289,                     # Comandos.AguaServico_RodizioAutomatico
    "CMD_AS_RODIZIO_MANUAL":                    85 + 12289,                     # Comandos.AguaServico_RodizioManual
    "CMD_AS_BOMBA_01_LIGAR":                    86 + 12289,                     # Comandos.AguaServico_Bomba01_Ligar
    "CMD_AS_BOMBA_01_DESLIGAR":                 87 + 12289,                     # Comandos.AguaServico_Bomba01_Desligar
    "CMD_AS_BOMBA_01_PRINCIPAL":                88 + 12289,                     # Comandos.AguaServico_Bomba01_Principal
    "CMD_AS_BOMBA_02_LIGAR":                    89 + 12289,                     # Comandos.AguaServico_Bomba02_Ligar
    "CMD_AS_BOMBA_02_DESLIGAR":                 90 + 12289,                     # Comandos.AguaServico_Bomba02_Desligar
    "CMD_AS_BOMBA_02_PRINCIPAL":                91 + 12289,                     # Comandos.AguaServico_Bomba02_Principal
    "CMD_AS_CIRCUITO_ABARTO_SEL":               92 + 12289,                     # Comandos.AguaServico_CircuitoAberto_Selecionar
    "CMD_AS_CIRCUITO_FECHADO_SEL":              93 + 12289,                     # Comandos.AguaServico_CircuitoFechado_Selecionar
    "CMD_AS_FILTRO_01_SEL":                     94 + 12289,                     # Comandos.AguaServico_Filtro01_Selecionar
    "CMD_AS_FILTRO_02_SEL":                     95 + 12289,                     # Comandos.AguaServico_Filtro02_Selecionar


    ## SETPOINTS
    # Poço
    "POCO_TEMPO_RODIZIO_LIDER":                 7 + 13569,                      # Setpoints.Poco_TempoRodizioLider
    "POCO_TEMPO_RODIZIO_RETAGUARDA":            8 + 13569,                      # Setpoints.Poco_TempoRodizioRetaguarda

    # Injeção Selo
    "IS_TEMPO_BOMBA_LIDER":                     17 + 13569,                     # Setpoints.InjecaoSelo_TempoBombaLider
    "IS_TEMPO_BOMBA_RETAGUARDA":                18 + 13569,                     # Setpoints.InjecaoSelo_TempoBombaRetaguarda

    # Agua Serviço
    "AS_TEMPO_BOMBA_LIDER":                     19 + 13569,                     # Setpoints.AguaServico_TempoBombaLider
    "AS_TEMPO_BOMBA_RETAGUARDA":                20 + 13569,                     # Setpoints.AguaServico_TempoBombaRetaguarda


    ## LEITURAS
    "RESET_ALARMES":                            5 + 12764,                      # Leituras.PainelResetAlarmes
    "RECONHECE_ALARMES":                        6 + 12764,                      # Leituras.PainelReconheceAlarmes

    "EMERGENCIA_USINA":                         7 + 12764,                      # Leituras.Usina_Emergencia_Info
    "EMERGENCIA_ACIONADA":                      [7 + 12764, 0],                 # Usina.Emergencia.Acionada
    "EMERGENCIA_SIRENE_LIG":                    [7 + 12764, 1],                 # Usina.Emergencia.Sireneligada
    "EMERGENCIA_MODO_REMOTO":                   [7 + 12764, 2],                 # Usina.Emergencia.Usina_OpercaoModoRemoto
    "EMERGENCIA_MODO_LOCAL":                    [7 + 12764, 3],                 # Usina.Emergencia.Usina_OpercaoModoLocal

    # Carregador de Baterias
    "CB_INFO":                                  9 + 12764,                     # Leituras.CarregadorBateria_Info
    "CB_EQUALIZACAO":                           [9 + 12764, 0],                # CarregadorBaterias.Info.Equalizacao
    "CB_ALARME":                                [9 + 12764, 1],                # CarregadorBaterias.Info.Alarme
    "CB_LIGADO":                                [9 + 12764, 2],                # CarregadorBaterias.Info.Ligado

    "CB_UENTRADA":                              10 + 12764,                     # Leituras.CarregadorBateria_UEntrada
    "CB_USAIDA":                                11 + 12764,                     # Leituras.CarregadorBateria_USaida
    "CB_IENTRADA":                              12 + 12764,                     # Leituras.CarregadorBateria_IEntrada
    "CB_ISAIDA":                                13 + 12764,                     # Leituras.CarregadorBateria_ISaida

    "CB2_INFO":                                 196 + 12764,                    # Leituras.CB2_Info
    "CB2_EQUALIZACAO":                          [196 + 12764, 0],               # CarregadorBaterias2.Info.Equalizacao
    "CB2_ALARME":                               [196 + 12764, 1],               # CarregadorBaterias2.Info.Alarme
    "CB2_LIGADO":                               [196 + 12764, 2],               # CarregadorBaterias2.Info.Ligado

    "CB2_UENTRADA":                             197 + 12764,                    # Leituras.CB2_UEntrada
    "CB2_USAIDA":                               198 + 12764,                    # Leituras.CB2_USaida
    "CB2_IENTRADA":                             199 + 12764,                    # Leituras.CB2_IEntrada
    "CB2_ISAIDA":                               200 + 12764,                    # Leituras.CB2_ISaida

    # Gerador Diesel
    "GD_INFO":                                  14 + 12764,                     # Leituras.GrupoDiesel_Info
    "GD_LIGADO":                                [14 + 12764, 0],                # GrupoDiesel.Info.Ligado
    "GD_DESLIGADO":                             [14 + 12764, 1],                # GrupoDiesel.Info.Desligado
    "GD_MANUAL":                                [14 + 12764, 2],                # GrupoDiesel.Info.Manual
    "GD_AUTOMATICO":                            [14 + 12764, 3],                # GrupoDiesel.Info.Automatico
    "GD_TESTE":                                 [14 + 12764, 4],                # GrupoDiesel.Info.Teste
    "GD_COMB_MENOR30":                          [14 + 12764, 5],                # GrupoDiesel.Info.[Comb<30]

    "GD_NIVEL_COMBUS":                          15 + 12764,                     # Leituras.GrupoDiesel_NivelCombustivel
    "GD_ROTACAO":                               16 + 12764,                     # Leituras.GrupoDiesel_RotacaoMotor
    "GD_TENSAO_BATERIA":                        17 + 12764,                     # Leituras.GrupoDiesel_TensaoBateria
    "GD_TENSAO_ALTERNADOR":                     18 + 12764,                     # Leituras.GrupoDiesel_TensaoAlternador
    "GD_TENSAO_L1":                             188 + 12764,                    # Leituras.GD_TensaoL1
    "GD_TENSAO_L2":                             189 + 12764,                    # Leituras.GD_TensaoL2
    "GD_TENSAO_L3":                             190 + 12764,                    # Leituras.GD_TensaoL3
    "GD_TENSAO_L1L2":                           191 + 12764,                    # Leituras.GD_TensaoL1L2
    "GD_TENSAO_L2L3":                           192 + 12764,                    # Leituras.GD_TensaoL2L3
    "GD_TENSAO_L3L1":                           193 + 12764,                    # Leituras.GD_TensaoL3L1
    "GD_FREQUANCIA":                            194 + 12764,                    # Leituras.GD_Frequencia
    "GD_TEMPAGUA":                              195 + 12764,                    # Leituras.GD_TempAgua

    # SA
    "SA_INFO":                                  65 + 12764,                     # Leituras.ServAuxiliar_Info
    "SA_MODO_LOCAL":                            [65 + 12764, 0],                # ServAuxiliar.Info.Local
    "SA_MODO_REMOTO":                           [65 + 12764, 1],                # ServAuxiliar.Info.Remoto
    "SA_MODO_AUTO":                             [65 + 12764, 2],                # ServAuxiliar.Info.Automatico
    "SA_MODO_MANUAL":                           [65 + 12764, 3],                # ServAuxiliar.Info.Manual
    "SA_ALIM_FONTE01_ATIVA":                    [65 + 12764, 4],                # ServAuxiliar.Info.Alimentacao_Fonte01Ativa
    "SA_ALIM_FONTE02_ATIVA":                    [65 + 12764, 5],                # ServAuxiliar.Info.Alimentacao_Fonte02Ativa
    "SA_ALIM_FONTE03_ATIVA":                    [65 + 12764, 6],                # ServAuxiliar.Info.Alimentacao_Fonte03Ativa
    "SA_TENSAO_PRES_FONTE01":                   [65 + 12764, 7],                # ServAuxiliar.Info.TensaoPresente_Fonte01
    "SA_TENSAO_PRES_FONTE02":                   [65 + 12764, 8],                # ServAuxiliar.Info.TensaoPresente_Fonte02
    "SA_TENSAO_PRES_FONTE03":                   [65 + 12764, 9],                # ServAuxiliar.Info.TensaoPresente_Fonte03
    "SA_SECC_CSA01_ABERTA":                     [65 + 12764, 10],               # ServAuxiliar.Info.SeccionadoraCSA01_Aberta
    "SA_SECC_CSA01_FECHADA":                    [65 + 12764, 11],               # ServAuxiliar.Info.SeccionadoraCSA01_Fechada
    "SA_SECC_CSA02_ABERTA":                     [65 + 12764, 12],               # ServAuxiliar.Info.SeccionadoraCSA02_Aberta
    "SA_SECC_CSA02_FECHADA":                    [65 + 12764, 13],               # ServAuxiliar.Info.SeccionadoraCSA02_Fechada
    "SA_CARGAS_NAO_ESSEN":                      [65 + 12764, 14],               # ServAuxiliar.Info.CargasNaoEssenciais

    # Tensão
    "TENSAO_RN":                                66 + 12764,                     # Leituras.ServAuxiliar_TensaoRN
    "TENSAO_SN":                                67 + 12764,                     # Leituras.ServAuxiliar_TensaoSN
    "TENSAO_TN":                                68 + 12764,                     # Leituras.ServAuxiliar_TensaoTN
    "TENSAO_RS":                                69 + 12764,                     # Leituras.ServAuxiliar_TensaoRS
    "TENSAO_ST":                                70 + 12764,                     # Leituras.ServAuxiliar_TensaoST
    "TENSAO_TR":                                71 + 12764,                     # Leituras.ServAuxiliar_TensaoTR

    # Corrente
    "CORRENTE_R":                               72 + 12764,                     # Leituras.ServAuxiliar_CorrenteR
    "CORRENTE_S":                               73 + 12764,                     # Leituras.ServAuxiliar_CorrenteS
    "CORRENTE_T":                               74 + 12764,                     # Leituras.ServAuxiliar_CorrenteT
    "CORRENTE_MEDIA":                           75 + 12764,                     # Leituras.ServAuxiliar_CorrenteMedia

    # Potência
    "POTENCIA_ATIVA_1":                         76 + 12764,                     # Leituras.ServAuxiliar_PotenciaAtiva1
    "POTENCIA_ATIVA_2":                         77 + 12764,                     # Leituras.ServAuxiliar_PotenciaAtiva2
    "POTENCIA_ATIVA_3":                         78 + 12764,                     # Leituras.ServAuxiliar_PotenciaAtiva3
    "POTENCIA_ATIVA_MEDIA":                     79 + 12764,                     # Leituras.ServAuxiliar_PotenciaAtivaMedia
    "POTENCIA_REATIVA_1":                       80 + 12764,                     # Leituras.ServAuxiliar_PotenciaReativa1
    "POTENCIA_REATIVA_2":                       81 + 12764,                     # Leituras.ServAuxiliar_PotenciaReativa2
    "POTENCIA_REATIVA_3":                       82 + 12764,                     # Leituras.ServAuxiliar_PotenciaReativa3
    "POTENCIA_REATIVA_MEDIA":                   83 + 12764,                     # Leituras.ServAuxiliar_PotenciaReativaMedia
    "POTENCIA_APARENTE_1":                      84 + 12764,                     # Leituras.ServAuxiliar_PotenciaAparente1
    "POTENCIA_APARENTE_2":                      85 + 12764,                     # Leituras.ServAuxiliar_PotenciaAparente2
    "POTENCIA_APARENTE_3":                      86 + 12764,                     # Leituras.ServAuxiliar_PotenciaAparente3
    "POTENCIA_APARENTE_MEDIA":                  87 + 12764,                     # Leituras.ServAuxiliar_PotenciaAparenteMedia

    # Fator Potência
    "FATOR_POTENCIA_1":                         88 + 12764,                     # Leituras.ServAuxiliar_FatorPotencia1
    "FATOR_POTENCIA_2":                         89 + 12764,                     # Leituras.ServAuxiliar_FatorPotencia2
    "FATOR_POTENCIA_3":                         90 + 12764,                     # Leituras.ServAuxiliar_FatorPotencia3
    "FATOR_POTENCIA_MEDIA":                     91 + 12764,                     # Leituras.ServAuxiliar_FatorPotenciaMedia

    # Frequência
    "FREQUENCIA":                               92 + 12764,                     # Leituras.ServAuxiliar_Frequencia

    # Energia Consumida
    "ENERGIA_CONSUMIDA_GWh":                    93 + 12764,                     # Leituras.ServAuxiliar_EnergiaConsumidaGWh
    "ENERGIA_CONSUMIDA_MWh":                    94 + 12764,                     # Leituras.ServAuxiliar_EnergiaConsumidaMWh
    "ENERGIA_CONSUMIDA_KWh":                    95 + 12764,                     # Leituras.ServAuxiliar_EnergiaConsumidaKWh
    "ENERGIA_CONSUMIDA_Wh":                     96 + 12764,                     # Leituras.ServAuxiliar_EnergiaConsumidaWh
    "ENERGIA_CONSUMIDA_GVArh":                  97 + 12764,                     # Leituras.ServAuxiliar_EnergiaConsumidaGVArh
    "ENERGIA_CONSUMIDA_MVArh":                  98 + 12764,                     # Leituras.ServAuxiliar_EnergiaConsumidaMVArh
    "ENERGIA_CONSUMIDA_KVArh":                  99 + 12764,                    # Leituras.ServAuxiliar_EnergiaConsumidaKVArh
    "ENERGIA_CONSUMIDA_WVArh":                  100 + 12764,                    # Leituras.ServAuxiliar_EnergiaConsumidaWVArh
    "ENERGIA_FORNECIDA_GVArh":                  101 + 12764,                    # Leituras.ServAuxiliar_EnergiaFornecidaGVArh
    "ENERGIA_FORNECIDA_MVArh":                  102 + 12764,                    # Leituras.ServAuxiliar_EnergiaFornecidaMVArh
    "ENERGIA_FORNECIDA_KVArh":                  103 + 12764,                    # Leituras.ServAuxiliar_EnergiaFornecidaKVArh
    "ENERGIA_FORNECIDA_VArh":                   104 + 12764,                    # Leituras.ServAuxiliar_EnergiaFornecidaVArh

    # Fuga Terra
    "FUGA_TERRA_TENSAO_POSITIVA":               104 + 12764,                    # Leituras.ServAux_FugaTerra_TensaoPositiva
    "FUGA_TERRA_TENSAO_NEGATIVA":               105 + 12764,                    # Leituras.ServAux_FugaTerra_TensaoNegativa
    "FUGA_TERRA_TENSAO":                        106 + 12764,                    # Leituras.ServAux_FugaTerra_Tensao

    "FUGA_TERRA_INFO":                          109 + 12764,                    # Leituras.ServAux_FugaTerra_Info
    "FUGA_TERRA_POSITIVO":                      [109 + 12764, 0],               # ReleFugaTerra.Info.FugaTerraPositivo
    "FUGA_TERRA_NEGATIVO":                      [109 + 12764, 1],               # ReleFugaTerra.Info.FugaTerraNegativo
    "FUGA_TERRA_SUBTENSAO":                     [109 + 12764, 2],               # ReleFugaTerra.Info.Subtensao
    "FUGA_TERRA_SOBRETENSAO":                   [109 + 12764, 3],               # ReleFugaTerra.Info.Sobretensao
    "FUGA_TERRA_ALARME":                        [109 + 12764, 4],               # ReleFugaTerra.Info.Alarme
    "FUGA_TERRA_TRIP":                          [109 + 12764, 5],               # ReleFugaTerra.Info.TRIP

    # Poço
    "POCO_INFO":                                110 + 12764,                    # Leituras.Poco_Info
    "POCO_MODO_LOCAL":                          [110 + 12764, 0],               # Poco.Info.ModoLocal
    "POCO_MODO_MANUAL":                         [110 + 12764, 1],               # Poco.Info.ModoManual
    "POCO_MODO_AUTO":                           [110 + 12764, 2],               # Poco.Info.ModoAuto
    "POCO_BOMBA01_PRINCI":                      [110 + 12764, 3],               # Poco.Info.Bomba01Principal
    "POCO_BOMBA02_PRINCI":                      [110 + 12764, 4],               # Poco.Info.Bomba02Principal
    "POCO_RODIZ_BOMBA02_ATIVA":                 [110 + 12764, 5],               # Poco.Info.RodizioBomba02Ativa
    "POCO_FLUXOSTATO_BOMBA01":                  [110 + 12764, 6],               # Poco.Info.FluxostatoBomba01
    "POCO_FLUXOSTATO_BOMBA02":                  [110 + 12764, 7],               # Poco.Info.FluxostatoBomba02
    "POCO_FLUXOSTATO_BOMBA03":                  [110 + 12764, 8],               # Poco.Info.FluxostatoBomba03

    "POCO_BOMBAS":                              111 + 12764,                    # Leituras.Poco_Bombas
    "POCO_BOMBA01":                             [111 + 12764, 0],               # Poco.Bombas.Bomba01
    "POCO_BOMBA02":                             [111 + 12764, 1],               # Poco.Bombas.Bomba02
    "POCO_BOMBA03":                             [111 + 12764, 2],               # Poco.Bombas.Bomba03
    "POCO_BOMBA04":                             [111 + 12764, 3],               # Poco.Bombas.Bomba04
    "POCO_INJ_SELO_BOMBA01":                    [111 + 12764, 4],               # Poco.Bombas.InjecaoSelo_Bomba01
    "POCO_INJ_SELO_BOMBA02":                    [111 + 12764, 5],               # Poco.Bombas.InjecaoSelo_Bomba02
    "POCO_AGUA_SERV_BOMBA01":                   [111 + 12764, 6],               # Poco.Bombas.AguaServico_Bomba01
    "POCO_AGUA_SERV_BOMBA02":                   [111 + 12764, 7],               # Poco.Bombas.AguaServico_Bomba02

    "POCO_NIVEL":                               112 + 12764,                    # Leituras.Poco_Nivel
    "POCO_NIVEL_LL":                            [112 + 12764, 0],               # Poco.Niveis.NivelLL
    "POCO_NIVEL_L":                             [112 + 12764, 1],               # Poco.Niveis.NivelL
    "POCO_NIVEL_H":                             [112 + 12764, 2],               # Poco.Niveis.NivelH
    "POCO_NIVEL_HH":                            [112 + 12764, 3],               # Poco.Niveis.NivelHH

    "POCO_HORIMETRO_PRINCIPAL":                 113 + 12764,                    # Leituras.Poco_HorimetroPrincipal
    "POCO_HORIMETRO_RETAGUARDA":                114 + 12764,                    # Leituras.Poco_HorimetroRetaguarda

    # Sensores
    "SENSOR_FUMACA_INFO":                       115 + 12764,                    # Leituras.SensorFumaca_Info

    "SENSOR_PRESENCA_INFO":                     116 + 12764,                    # Leituras.SensorPresenca_Info
    "SENSOR_PRESENCA_HABILITADO":               [116 + 12764, 0],               # SensorPresenca.Habilitado
    "SENSOR_PRESENCA_SALA_SUP":                 [116 + 12764, 1],               # SensorPresenca.SalaSupervisorio
    "SENSOR_PRESENCA_SALA_COZI_BANH":           [116 + 12764, 2],               # SensorPresenca.SalaCozinhaBanheiro
    "SENSOR_PRESENCA_ALMOXARI":                 [116 + 12764, 3],               # SensorPresenca.Almoxarifado
    "SENSOR_PRESENCA_AREA_MONT":                [116 + 12764, 4],               # SensorPresenca.AreaMontagem
    "SENSOR_PRESENCA_SALA_CUBI":                [116 + 12764, 5],               # SensorPresenca.SalaCubiculos

    # Temperaturas
    "USINA_TEMPERATURA_01":                     118 + 12764,                    # Leituras.Usina_Temperatura_01
    "USINA_TEMPERATURA_02":                     119 + 12764,                    # Leituras.Usina_Temperatura_02
    "USINA_TEMPERATURA_03":                     120 + 12764,                    # Leituras.Usina_Temperatura_03
    "USINA_TEMPERATURA_04":                     121 + 12764,                    # Leituras.Usina_Temperatura_04
    "USINA_TEMPERATURA_05":                     122 + 12764,                    # Leituras.Usina_Temperatura_05
    "USINA_TEMPERATURA_06":                     123 + 12764,                    # Leituras.Usina_Temperatura_06
    "USINA_TEMPERATURA_07":                     124 + 12764,                    # Leituras.Usina_Temperatura_07
    "USINA_TEMPERATURA_08":                     125 + 12764,                    # Leituras.Usina_Temperatura_08

    # Sistema de Água
    "SIS_AGUA_INFO":                            180 + 12764,                    # Leituras.SistemaAgua_Info
    "SIS_AGUA_CAIXA_AGUA01_NV100":              [180 + 12764, 0],               # SistemaAgua.Info.CaixaDAgua01_Nivel100
    "SIS_AGUA_CIRQUITO_FECHADO":                [180 + 12764, 1],               # SistemaAgua.Info.CircuitoFechado
    "SIS_AGUA_CIRQUITO_ABERTO":                 [180 + 12764, 2],               # SistemaAgua.Info.CircuitoAberto
    "SIS_AGUA_FILTRO01":                        [180 + 12764, 3],               # SistemaAgua.Info.Filtro01
    "SIS_AGUA_FILTRO02":                        [180 + 12764, 4],               # SistemaAgua.Info.Filtro02
    "SIS_AGUA_AGUA_SERV_BOMBA01_FLUXOS":        [180 + 12764, 5],               # SistemaAgua.Info.AguaServico_Bomba01_Fluxostato
    "SIS_AGUA_AGUA_SERV_BOMBA02_FLUXOS":        [180 + 12764, 6],               # SistemaAgua.Info.AguaServico_Bomba02_Fluxostato
    "SIS_AGUA_INJ_SELO_BOMBA01_FLUXOS":         [180 + 12764, 7],               # SistemaAgua.Info.InjecaoSelo_Bomba01_Fluxostato
    "SIS_AGUA_INJ_SELO_BOMBA02_FLUXOS":         [180 + 12764, 8],               # SistemaAgua.Info.InjecaoSelo_Bomba02_Fluxostato
    "SIS_AGUA_CAIXA_AGUA01_NV75":               [180 + 12764, 9],               # SistemaAgua.Info.CaixaDAgua01_Nivel75
    "SIS_AGUA_CAIXA_AGUA01_NV50":               [180 + 12764, 10],              # SistemaAgua.Info.CaixaDAgua01_Nivel50
    "SIS_AGUA_CAIXA_AGUA02_NV100":              [180 + 12764, 11],              # SistemaAgua.Info.CaixaDAgua02_Nivel100
    "SIS_AGUA_CAIXA_AGUA02_NV75":               [180 + 12764, 12],              # SistemaAgua.Info.CaixaDAgua02_Nivel75
    "SIS_AGUA_CAIXA_AGUA02_NV50":               [180 + 12764, 13],              # SistemaAgua.Info.CaixaDAgua02_Nivel50

    "SIS_AGUA_BOMBA":                           181 + 12764,                    # Leituras.SistemaAgua_Bombas
    "SIS_AGUA_BOM_INJ_SELO_BOMBA01":            [181 + 12764, 0],               # SistemaAgua.Bombas.InjecaoSelo_Bomba01
    "SIS_AGUA_BOM_INJ_SELO_BOMBA02":            [181 + 12764, 1],               # SistemaAgua.Bombas.InjecaoSelo_Bomba02
    "SIS_AGUA_BOM_AGUA_SERV_BOMBA01":           [181 + 12764, 2],               # SistemaAgua.Bombas.AguaServico_Bomba01
    "SIS_AGUA_BOM_AGUA_SERV_BOMBA02":           [181 + 12764, 3],               # SistemaAgua.Bombas.AguaServico_Bomba02
    "SIS_AGUA_BOM_INJ_SELO_RODIZ_BOMBA01":      [181 + 12764, 4],               # SistemaAgua.Bombas.InjecaoSelo_RodizioBomba01
    "SIS_AGUA_BOM_INJ_SELO_RODIZ_BOMBA02":      [181 + 12764, 5],               # SistemaAgua.Bombas.InjecaoSelo_RodizioBomba02
    "SIS_AGUA_BOM_INJ_SELO_RODIZ_HABILI":       [181 + 12764, 6],               # SistemaAgua.Bombas.InjecaoSelo_RodizioHabilitado
    "SIS_AGUA_BOM_AGUA_SERV_RODIZ_BOMBA01":     [181 + 12764, 7],               # SistemaAgua.Bombas.AguaServico_RodizioBomba01
    "SIS_AGUA_BOM_AGUA_SERV_RODIZ_BOMBA02":     [181 + 12764, 8],               # SistemaAgua.Bombas.AguaServico_RodizioBomba02
    "SIS_AGUA_BOM_AGUA_SERV_RODIZ_HABILI":      [181 + 12764, 9],               # SistemaAgua.Bombas.AguaServico_RodizioHabilitado

    "SIS_AGUA_VALVULAS":                        182 + 12764,                    # Leituras.SistemaAgua_Valvulas
    "SIS_AGUA_VAL_ENTRADA_FILTRO01_ABERTA":     [182 + 12764, 0],               # SistemaAgua.Valvulas.EntradaFiltro01_Aberta
    "SIS_AGUA_VAL_ENTRADA_FILTRO01_FECHADA":    [182 + 12764, 1],               # SistemaAgua.Valvulas.EntradaFiltro01_Fechada
    "SIS_AGUA_VAL_ENTRADA_FILTRO02_ABERTA":     [182 + 12764, 2],               # SistemaAgua.Valvulas.EntradaFiltro02_Aberta
    "SIS_AGUA_VAL_ENTRADA_FILTRO02_FECHADA":    [182 + 12764, 3],               # SistemaAgua.Valvulas.EntradaFiltro02_Fechada
    "SIS_AGUA_VAL_ENTRADA_TORRE_ABERTA":        [182 + 12764, 4],               # SistemaAgua.Valvulas.EntradaTorre_Aberta
    "SIS_AGUA_VAL_ENTRADA_TORRE_FECHADA":       [182 + 12764, 5],               # SistemaAgua.Valvulas.EntradaTorre_Fechada
    "SIS_AGUA_VAL_SAIDA_TORRE_ABERTA":          [182 + 12764, 6],               # SistemaAgua.Valvulas.SaidaTorre_Aberta
    "SIS_AGUA_VAL_SAIDA_TORRE_FECHADA":         [182 + 12764, 7],               # SistemaAgua.Valvulas.SaidaTorre_Fechada
    "SIS_AGUA_VAL_DESCARGA_01_ABERTA":          [182 + 12764, 8],               # SistemaAgua.Valvulas.Descarga01Aberta
    "SIS_AGUA_VAL_DESCARGA_01_FECHADA":         [182 + 12764, 9],               # SistemaAgua.Valvulas.Descarga01Fechada
    "SIS_AGUA_VAL_DESCARGA_02_ABERTA":          [182 + 12764, 10],              # SistemaAgua.Valvulas.Descarga02Aberta
    "SIS_AGUA_VAL_DESCARGA_02_FECHADA":         [182 + 12764, 11],              # SistemaAgua.Valvulas.Descarga02Fechada
    "SIS_AGUA_VAL_DESCARGA_03_ABERTA":          [182 + 12764, 12],              # SistemaAgua.Valvulas.Descarga03Aberta
    "SIS_AGUA_VAL_DESCARGA_03_FECHADA":         [182 + 12764, 13],              # SistemaAgua.Valvulas.Descarga03Fechada
    "SIS_AGUA_VAL_DESCARGA_04_ABERTA":          [182 + 12764, 14],              # SistemaAgua.Valvulas.Descarga04Aberta
    "SIS_AGUA_VAL_DESCARGA_04_FECHADA":         [182 + 12764, 15],              # SistemaAgua.Valvulas.Descarga04Fechada

    "SIS_AGUA_VALVULAS2":                       187 + 12764,                    # Leituras.SistemaAgua_Valvulas2
    "SIS_AGUA_VAL2_ENTRA_UG01_ABERTA":          [187 + 12764, 0],               # SistemaAgua.Valvulas2.EntradaUG01_Aberta
    "SIS_AGUA_VAL2_ENTRA_UG01_FECHADA":         [187 + 12764, 1],               # SistemaAgua.Valvulas2.EntradaUG01_Fechada
    "SIS_AGUA_VAL2_ENTRA_UG02_ABERTA":          [187 + 12764, 2],               # SistemaAgua.Valvulas2.EntradaUG02_Aberta
    "SIS_AGUA_VAL2_ENTRA_UG02_FECHADA":         [187 + 12764, 3],               # SistemaAgua.Valvulas2.EntradaUG02_Fechada
    "SIS_AGUA_VAL2_ENTRA_UG03_ABERTA":          [187 + 12764, 4],               # SistemaAgua.Valvulas2.EntradaUG03_Aberta
    "SIS_AGUA_VAL2_ENTRA_UG03_FECHADA":         [187 + 12764, 5],               # SistemaAgua.Valvulas2.EntradaUG03_Fechada
    "SIS_AGUA_VAL2_ENTRA_UG04_ABERTA":          [187 + 12764, 6],               # SistemaAgua.Valvulas2.EntradaUG04_Aberta
    "SIS_AGUA_VAL2_ENTRA_UG04_FECHADA":         [187 + 12764, 7],               # SistemaAgua.Valvulas2.EntradaUG04_Fechada

    # Injeção Selo
    "IS_ACUMULADOR_LIDER":                      183 + 12764,                    # Leituras.InjecaoSelo_AcumuladorLider
    "IS_ACUMULADOR_RETAGUARDA":                 184 + 12764,                    # Leituras.InjecaoSelo_AcumuladorRetaguarda

    # Água Serviço
    "AS_ACUMULADOR_LIDER":                      185 + 12764,                    # Leituras.AguaServico_AcumuladorLider
    "AS_ACUMULADOR_RETAGUARDA":                 186 + 12764,                    # Leituras.AguaServico_AcumuladorRetaguarda

    # Rendimento
    "RENDIMENTO_UG01":                          202 + 12764,                    # Leituras.Rendimento_UG01
    "RENDIMENTO_UG02":                          203 + 12764,                    # Leituras.Rendimento_UG02
    "RENDIMENTO_UG03":                          204 + 12764,                    # Leituras.Rendimento_UG03
    "RENDIMENTO_UG04":                          205 + 12764,                    # Leituras.Rendimento_UG04
    "RENDIMENTO_GERAL":                         206 + 12764,                    # Leituras.Rendimento_Geral

    "RENDIMENTO_INFO":                          217 + 12764,                    # Leituras.Rendimento_Info
    "RENDIMEN_RESERV_ESVAZIANDO":               [217 + 12764, 0],               # RendimentoVazao.ReservEsvaziando
    "RENDIMEN_RESERV_ENCHENDO":                 [217 + 12764, 1],               # RendimentoVazao.ReservEnchendo
    "RENDIMEN_RESERV_ESTAVEL":                  [217 + 12764, 2],               # RendimentoVazao.ReservEstavel


    "RENDIMENTO_TURBINA_UG01":                  218 + 12764,                    # Leituras.RendimentoTurbina_UG01
    "RENDIMENTO_TURBINA_UG02":                  219 + 12764,                    # Leituras.RendimentoTurbina_UG02
    "RENDIMENTO_TURBINA_UG03":                  220 + 12764,                    # Leituras.RendimentoTurbina_UG03
    "RENDIMENTO_TURBINA_UG04":                  221 + 12764,                    # Leituras.RendimentoTurbina_UG04
    "RENDIMENTO_GERADOR_UG01":                  222 + 12764,                    # Leituras.RendimentoGerador_UG01
    "RENDIMENTO_GERADOR_UG02":                  223 + 12764,                    # Leituras.RendimentoGerador_UG02
    "RENDIMENTO_GERADOR_UG03":                  224 + 12764,                    # Leituras.RendimentoGerador_UG03
    "RENDIMENTO_GERADOR_UG04":                  225 + 12764,                    # Leituras.RendimentoGerador_UG04

    # Vazão
    "VAZAO_TURBINADA_UG01":                     207 + 12764,                    # Leituras.VazaoTurbinada_UG01
    "VAZAO_TURBINADA_UG02":                     208 + 12764,                    # Leituras.VazaoTurbinada_UG02
    "VAZAO_TURBINADA_UG03":                     209 + 12764,                    # Leituras.VazaoTurbinada_UG03
    "VAZAO_TURBINADA_UG04":                     210 + 12764,                    # Leituras.VazaoTurbinada_UG04
    "VAZAO_TURBINADA":                          211 + 12764,                    # Leituras.VazaoTurbinada
    "VAZAO_RIO":                                212 + 12764,                    # Leituras.VazaoRio
    "VAZAO_VERTEDOR":                           213 + 12764,                    # Leituras.VazaoVertedor
    "VAZAO_ADUFA_01":                           214 + 12764,                    # Leituras.VazaoAdufa01
    "VAZAO_ADUFA_02":                           215 + 12764,                    # Leituras.VazaoAdufa02
    "VAZAO_EFLUENTE":                           216 + 12764,                    # Leituras.VazaoEfluente


    ## ALARMES
    "Alarme01_02":                              [0 + 14089, 2],
    "Alarme01_03":                              [0 + 14089, 3],
    "Alarme01_07":                              [0 + 14089, 7],
    "Alarme01_08":                              [0 + 14089, 8],
    "Alarme01_09":                              [0 + 14089, 9],
    "Alarme01_10":                              [0 + 14089, 10],
    "Alarme01_11":                              [0 + 14089, 11],
    "Alarme01_15":                              [0 + 14089, 15],

    "Alarme02_03":                              [1 + 14089, 3],
    "Alarme02_06":                              [1 + 14089, 6],
    "Alarme02_09":                              [1 + 14089, 9],
    "Alarme02_10":                              [1 + 14089, 10],
    "Alarme02_14":                              [1 + 14089, 14],
    "Alarme02_15":                              [1 + 14089, 15],

    "Alarme03_09":                              [2 + 14089, 9],
    "Alarme03_10":                              [2 + 14089, 10],
    "Alarme03_11":                              [2 + 14089, 11],
    "Alarme03_12":                              [2 + 14089, 12],
    "Alarme03_13":                              [2 + 14089, 13],
    "Alarme03_14":                              [2 + 14089, 14],
    "Alarme03_15":                              [2 + 14089, 15],

    "Alarme04_00":                              [3 + 14089, 0],
    "Alarme04_01":                              [3 + 14089, 1],
    "Alarme04_02":                              [3 + 14089, 2],
    "Alarme04_03":                              [3 + 14089, 3],
    "Alarme04_04":                              [3 + 14089, 4],
    "Alarme04_05":                              [3 + 14089, 5],
    "Alarme04_06":                              [3 + 14089, 6],
    "Alarme04_07":                              [3 + 14089, 7],
    "Alarme04_08":                              [3 + 14089, 8],
    "Alarme04_09":                              [3 + 14089, 9],

    "Alarme05_00":                              [4 + 14089, 0],
    "Alarme05_01":                              [4 + 14089, 1],
    "Alarme05_15":                              [4 + 14089, 15],

    "Alarme06_00":                              [5 + 14089, 0],
    "Alarme06_01":                              [5 + 14089, 1],
    "Alarme06_02":                              [5 + 14089, 2],
    "Alarme06_03":                              [5 + 14089, 3],
    "Alarme06_04":                              [5 + 14089, 4],
    "Alarme06_05":                              [5 + 14089, 5],
    "Alarme06_06":                              [5 + 14089, 6],
    "Alarme06_07":                              [5 + 14089, 7],
    "Alarme06_08":                              [5 + 14089, 8],
    "Alarme06_09":                              [5 + 14089, 9],
    "Alarme06_11":                              [5 + 14089, 11],
    "Alarme06_12":                              [5 + 14089, 12],
    "Alarme06_13":                              [5 + 14089, 13],
    "Alarme06_14":                              [5 + 14089, 14],

    "Alarme07_01":                              [6 + 14089, 1],
    "Alarme07_02":                              [6 + 14089, 2],
    "Alarme07_03":                              [6 + 14089, 3],
    "Alarme07_04":                              [6 + 14089, 4],
    "Alarme07_05":                              [6 + 14089, 5],
    "Alarme07_06":                              [6 + 14089, 6],
    "Alarme07_07":                              [6 + 14089, 7],
    "Alarme07_11":                              [6 + 14089, 11],
    "Alarme07_12":                              [6 + 14089, 12],
    "Alarme07_13":                              [6 + 14089, 13],
    "Alarme07_14":                              [6 + 14089, 14],
    "Alarme07_15":                              [6 + 14089, 15],

    "Alarme08_00":                              [7 + 14089, 0],
    "Alarme08_01":                              [7 + 14089, 1],
    "Alarme08_02":                              [7 + 14089, 2],
    "Alarme08_03":                              [7 + 14089, 3],
    "Alarme08_04":                              [7 + 14089, 4],
    "Alarme08_05":                              [7 + 14089, 5],
    "Alarme08_06":                              [7 + 14089, 6],
    "Alarme08_07":                              [7 + 14089, 7],
    "Alarme08_08":                              [7 + 14089, 8],
    "Alarme08_09":                              [7 + 14089, 9],
    "Alarme08_10":                              [7 + 14089, 10],
    "Alarme08_11":                              [7 + 14089, 11],
    "Alarme08_12":                              [7 + 14089, 12],
    "Alarme08_13":                              [7 + 14089, 13],
    "Alarme08_14":                              [7 + 14089, 14],

    "Alarme09_00":                              [8 + 14089, 0],
    "Alarme09_01":                              [8 + 14089, 1],
    "Alarme09_02":                              [8 + 14089, 2],
    "Alarme09_03":                              [8 + 14089, 3],
    "Alarme09_04":                              [8 + 14089, 4],
    "Alarme09_09":                              [8 + 14089, 9],
    "Alarme09_10":                              [8 + 14089, 10],
    "Alarme09_11":                              [8 + 14089, 11],
    "Alarme09_12":                              [8 + 14089, 12],

    "Alarme10_00":                              [9 + 14089, 0],
    "Alarme10_01":                              [9 + 14089, 1],
    "Alarme10_02":                              [9 + 14089, 2],
    "Alarme10_03":                              [9 + 14089, 3],
    "Alarme10_04":                              [9 + 14089, 4],
    "Alarme10_05":                              [9 + 14089, 5],
    "Alarme10_06":                              [9 + 14089, 6],
    "Alarme10_07":                              [9 + 14089, 7],

    "Alarme11_00":                              [10 + 14089, 0],
    "Alarme11_01":                              [10 + 14089, 1],
    "Alarme11_02":                              [10 + 14089, 2],
    "Alarme11_03":                              [10 + 14089, 3],
    "Alarme11_04":                              [10 + 14089, 4],
    "Alarme11_05":                              [10 + 14089, 5],
    "Alarme11_06":                              [10 + 14089, 6],
    "Alarme11_07":                              [10 + 14089, 7],
    "Alarme11_08":                              [10 + 14089, 8],
    "Alarme11_09":                              [10 + 14089, 9],
    "Alarme11_10":                              [10 + 14089, 10],
    "Alarme11_11":                              [10 + 14089, 11],
    "Alarme11_12":                              [10 + 14089, 12],
    "Alarme11_13":                              [10 + 14089, 13],
    "Alarme11_14":                              [10 + 14089, 14],
    "Alarme11_15":                              [10 + 14089, 15],

    "Alarme12_00":                              [11 + 14089, 0],
    "Alarme12_04":                              [11 + 14089, 4],
    "Alarme12_05":                              [11 + 14089, 5],
    "Alarme12_06":                              [11 + 14089, 6],

    "Alarme14_03":                              [13 + 14089, 3],
    "Alarme14_04":                              [13 + 14089, 4],
    "Alarme14_05":                              [13 + 14089, 5],
    "Alarme14_06":                              [13 + 14089, 6],
    "Alarme14_08":                              [13 + 14089, 8],
    "Alarme14_09":                              [13 + 14089, 9],
    "Alarme14_10":                              [13 + 14089, 10],
    "Alarme14_11":                              [13 + 14089, 11],
    "Alarme14_12":                              [13 + 14089, 12],
    "Alarme14_13":                              [13 + 14089, 13],
    "Alarme14_14":                              [13 + 14089, 14],
    "Alarme14_15":                              [13 + 14089, 15],

    "Alarme15_00":                              [14 + 14089, 0],
    "Alarme15_01":                              [14 + 14089, 1],
    "Alarme15_02":                              [14 + 14089, 2],
    "Alarme15_03":                              [14 + 14089, 3],
    "Alarme15_04":                              [14 + 14089, 4],
    "Alarme15_05":                              [14 + 14089, 5],
    "Alarme15_06":                              [14 + 14089, 6],
    "Alarme15_07":                              [14 + 14089, 7],
    "Alarme15_08":                              [14 + 14089, 8],
    "Alarme15_09":                              [14 + 14089, 9],
    "Alarme15_10":                              [14 + 14089, 10],
    "Alarme15_11":                              [14 + 14089, 11],

    "Alarme16_10":                              [15 + 14089, 10],
    "Alarme16_11":                              [15 + 14089, 11],
    "Alarme16_12":                              [15 + 14089, 12],
    "Alarme16_13":                              [15 + 14089, 13],
    "Alarme16_14":                              [15 + 14089, 14],
    "Alarme16_15":                              [15 + 14089, 15],

    "Alarme17_00":                              [16 + 14089, 0],
    "Alarme17_01":                              [16 + 14089, 1],
    "Alarme17_02":                              [16 + 14089, 2],
    "Alarme17_03":                              [16 + 14089, 3],
    "Alarme17_04":                              [16 + 14089, 4],
    "Alarme17_05":                              [16 + 14089, 5],
    "Alarme17_06":                              [16 + 14089, 6],
    "Alarme17_07":                              [16 + 14089, 7],
    "Alarme17_09":                              [16 + 14089, 9],
    "Alarme17_10":                              [16 + 14089, 10],
    "Alarme17_11":                              [16 + 14089, 11],
    "Alarme17_12":                              [16 + 14089, 12],
    "Alarme17_13":                              [16 + 14089, 13],
    "Alarme17_14":                              [16 + 14089, 14],

    "Alarme18_00":                              [17 + 14089, 0],
    "Alarme18_01":                              [17 + 14089, 1],
    "Alarme18_03":                              [17 + 14089, 3],
    "Alarme18_06":                              [17 + 14089, 6],
    "Alarme18_07":                              [17 + 14089, 7],
    "Alarme18_08":                              [17 + 14089, 8],
    "Alarme18_09":                              [17 + 14089, 9],
    "Alarme18_10":                              [17 + 14089, 10],
    "Alarme18_11":                              [17 + 14089, 11],
    "Alarme18_12":                              [17 + 14089, 12],

    "Alarme19_06":                              [18 + 14089, 6],
    "Alarme19_07":                              [18 + 14089, 7],
    "Alarme19_08":                              [18 + 14089, 8],
    "Alarme19_09":                              [18 + 14089, 9],
    "Alarme19_10":                              [18 + 14089, 10],
    "Alarme19_11":                              [18 + 14089, 11],
    "Alarme19_12":                              [18 + 14089, 12],
    "Alarme19_13":                              [18 + 14089, 13],
    "Alarme19_14":                              [18 + 14089, 14],

    "Alarme20_06":                              [19 + 14089, 6],
    "Alarme20_07":                              [19 + 14089, 7],
    "Alarme20_08":                              [19 + 14089, 8],
    "Alarme20_09":                              [19 + 14089, 9],
    "Alarme20_10":                              [19 + 14089, 10],
    "Alarme20_11":                              [19 + 14089, 11],
    "Alarme20_12":                              [19 + 14089, 12],
    "Alarme20_13":                              [19 + 14089, 13],
    "Alarme20_14":                              [19 + 14089, 14],

    "Alarme21_02":                              [20 + 14089, 2],
    "Alarme21_03":                              [20 + 14089, 3],
    "Alarme21_06":                              [20 + 14089, 6],
    "Alarme21_07":                              [20 + 14089, 7],
    "Alarme21_08":                              [20 + 14089, 8],
    "Alarme21_09":                              [20 + 14089, 9],
    "Alarme21_10":                              [20 + 14089, 10],
    "Alarme21_11":                              [20 + 14089, 11],
    "Alarme21_12":                              [20 + 14089, 12],
}


REG_SE = {
    ## COMANDOS
    # Dj52L
    "CMD_ABRIR_DJ52L":                          3 + 12289,                      # Comandos.Disj52LAbrir
    "CMD_FECHAR_DJ52L":                         4 + 12289,                      # Comandos.Disj52LFechar

    # Secc89L
    "CMD_SECC89L_ABRIR":                        34 + 12289,                     # Comandos.Secc89L_Abrir
    "CMD_SECC89L_FECHAR":                       35 + 12289,                     # Comandos.Secc89L_Fechar

    # Cargas Não Essenciais
    "CMD_CARGANAOESSEN_FECHAR":                 36 + 12289,                     # Comandos.CargaNaoEssencial_Fechar
    "CMD_CARGANAOESSEN_ABRIR":                  37 + 12289,                     # Comandos.CargaNaoEssencial_Abrir


    ## LEITURAS
    # Disjuntores
    "STATUS_DJ52L":                             20 + 12764,                     # Leituras.Subestacao_Disj52L
    "DJ52L_ABERTO":                             [20 + 12764, 0],                # Disj52L.Info.Aberto
    "DJ52L_FECHADO":                            [20 + 12764, 1],                # Disj52L.Info.Fechado
    "DJ52L_INCONSISTENTE":                      [20 + 12764, 2],                # Disj52L.Info.Inconsistente
    "DJ52L_TRIP":                               [20 + 12764, 3],                # Disj52L.Info.Trip
    "DJ52L_MODO_LOCAL":                         [20 + 12764, 4],                # Disj52L.Info.ModoLocal
    "DJ52L_MODO_REMOTO":                        [20 + 12764, 5],                # Disj52L.Info.ModoRemoto
    "DJ52L_MOLA_CARREGADA":                     [20 + 12764, 6],                # Disj52L.Info.MolaCarregada
    "DJ52L_ALIM125VCC_MOTOR":                   [20 + 12764, 7],                # Disj52L.Info.Alim125Vcc_motor
    "DJ52L_FALTA_VCC":                          [20 + 12764, 8],                # Disj52L.Info.FaltaVcc
    "DJ52L_COND_FECHAMENTO":                    [20 + 12764, 9],                # Disj52L.Info.CondFechamento
    "DJ52L_GAS_SF6_1":                          [20 + 12764, 10],               # Disj52L.Info.GasSF6_1
    "DJ52L_GAS_SF6_2":                          [20 + 12764, 11],               # Disj52L.Info.GasSF6_2
    "DJ52L_FALHA_ABERTURA":                     [20 + 12764, 12],               # Disj52L.Info.FalhaAbertura
    "DJ52L_FALHA_FECHAMENTO":                   [20 + 12764, 13],               # Disj52L.Info.FalhaFechamento

    "STATUS_SECCIONADORAS":                     21 + 12764,                     # Leituras.Subestacao_Seccionadoras
    "SECC_89L_ABERTA":                          [21 + 12764, 0],                # Seccionadoras.Info.[89L_Aberta]
    "SECC_89L_FECHADA":                         [21 + 12764, 1],                # Seccionadoras.Info.[89L_Fechada]
    "SECC_89L_CONDICAO":                        [21 + 12764, 2],                # Seccionadoras.Info.[89L_CondicaoFechamento]
    "SECC_MODO_LOCAL":                          [21 + 12764, 3],                # Seccionadoras.Info.Local
    "SECC_LAMINA_FECHADA":                      [21 + 12764, 4],                # Seccionadoras.Info.LaminaFechada
    "SECC_ALIM_VCC_CMD":                        [21 + 12764, 5],                # Seccionadoras.Info.AlimVccComando
    "SECC_ALIM_VCC_BLOQ":                       [21 + 12764, 6],                # Seccionadoras.Info.AlimVccBloqueio

    # Tensão
    "TENSAO_RN":                                22 + 12764,                     # Leituras.Subestacao_TensaoRN
    "TENSAO_SN":                                23 + 12764,                     # Leituras.Subestacao_TensaoSN
    "TENSAO_TN":                                24 + 12764,                     # Leituras.Subestacao_TensaoTN
    "TENSAO_RS":                                25 + 12764,                     # Leituras.Subestacao_TensaoRS
    "TENSAO_ST":                                26 + 12764,                     # Leituras.Subestacao_TensaoST
    "TENSAO_TR":                                27 + 12764,                     # Leituras.Subestacao_TensaoTR
    "TENSAO_SINCRONISMO":                       62 + 12764,                     # Leituras.Subestacao_TensaoSincronismo
    "TENSAO_VCC":                               63 + 12764,                     # Leituras.Subestacao_TensaoVCC

    "FP_INFO":                                  64 + 12764,                     # Leituras.ServAux_FPInfo
    "FP_INDUTIVO_FASE1":                        [64 + 12764, 0],                # MedidorSubestacao.FP_Info.IndutivoFase1
    "FP_CAPACITIVO_FASE1":                      [64 + 12764, 1],                # MedidorSubestacao.FP_Info.CapacitivoFase1
    "FP_INDUTIVO_FASE2":                        [64 + 12764, 2],                # MedidorSubestacao.FP_Info.IndutivoFase2
    "FP_CAPACITIVO_FASE2":                      [64 + 12764, 3],                # MedidorSubestacao.FP_Info.CapacitivoFase2
    "FP_INDUTIVO_FASE3":                        [64 + 12764, 4],                # MedidorSubestacao.FP_Info.IndutivoFase3
    "FP_CAPACITIVO_FASE3":                      [64 + 12764, 5],                # MedidorSubestacao.FP_Info.CapacitivoFase3
    "FP_INDUTIVO_TOTAL":                        [64 + 12764, 6],                # MedidorSubestacao.FP_Info.IndutivoTotal
    "FP_CAPACITIVO_TOTAL":                      [64 + 12764, 7],                # MedidorSubestacao.FP_Info.CapacitivoTotal

    # Corrente
    "CORRENTE_R":                               28 + 12764,                     # Leituras.Subestacao_CorrenteR
    "CORRENTE_S":                               29 + 12764,                     # Leituras.Subestacao_CorrenteS
    "CORRENTE_T":                               30 + 12764,                     # Leituras.Subestacao_CorrenteT
    "CORRENTE_MEDIA":                           31 + 12764,                     # Leituras.Subestacao_CorrenteMedia
    "CORRENTE_NEUTRO":                          61 + 12764,                     # Leituras.Subestacao_CorrenteNeutro

    # Potência
    "POTENCIA_ATIVA_1":                         32 + 12764,                     # Leituras.Subestacao_PotenciaAtiva1
    "POTENCIA_ATIVA_2":                         33 + 12764,                     # Leituras.Subestacao_PotenciaAtiva2
    "POTENCIA_ATIVA_3":                         34 + 12764,                     # Leituras.Subestacao_PotenciaAtiva3
    "POTENCIA_ATIVA_MEDIA":                     35 + 12764,                     # Leituras.Subestacao_PotenciaAtivaMedia
    "POTENCIA_REATIVA_1":                       36 + 12764,                     # Leituras.Subestacao_PotenciaReativa1
    "POTENCIA_REATIVA_2":                       37 + 12764,                     # Leituras.Subestacao_PotenciaReativa2
    "POTENCIA_REATIVA_3":                       38 + 12764,                     # Leituras.Subestacao_PotenciaReativa3
    "POTENCIA_REATIVA_MEDIA":                   39 + 12764,                     # Leituras.Subestacao_PotenciaReativaMedia
    "POTENCIA_APARENTE_1":                      40 + 12764,                     # Leituras.Subestacao_PotenciaAparente1
    "POTENCIA_APARENTE_2":                      41 + 12764,                     # Leituras.Subestacao_PotenciaAparente2
    "POTENCIA_APARENTE_3":                      42 + 12764,                     # Leituras.Subestacao_PotenciaAparente3
    "POTENCIA_APARENTE_MEDIA":                  43 + 12764,                     # Leituras.Subestacao_PotenciaAparenteMedia

    # Fator Potência
    "FATOR_POTENCIA_1":                         44 + 12764,                     # Leituras.Subestacao_FatorPotencia1
    "FATOR_POTENCIA_2":                         45 + 12764,                     # Leituras.Subestacao_FatorPotencia2
    "FATOR_POTENCIA_3":                         46 + 12764,                     # Leituras.Subestacao_FatorPotencia3
    "FATOR_POTENCIA_MEDIA":                     47 + 12764,                     # Leituras.Subestacao_FatorPotenciaMedia

    # Frequência
    "FREQUENCIA":                               48 + 12764,                     # Leituras.Subestacao_Frequencia

    # Energia Forncida
    "ENERGIA_FORNECIDA_TWh":                    49 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaTWh
    "ENERGIA_FORNECIDA_GWh":                    50 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaGWh
    "ENERGIA_FORNECIDA_MWh":                    51 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaMWh
    "ENERGIA_FORNECIDA_KWh":                    52 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaKWh
    "ENERGIA_FORNECIDA_TVArh":                  53 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaTVArh
    "ENERGIA_FORNECIDA_GVArh":                  54 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaGVArh
    "ENERGIA_FORNECIDA_MVArh":                  55 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaMVArh
    "ENERGIA_FORNECIDA_KVArh":                  56 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaKVArh
    "ENERGIA_FORNECIDA_TVArh":                  57 + 12764,                     # Leituras.Subestacao_EnergiaConsumidaTVArh
    "ENERGIA_FORNECIDA_GVArh":                  58 + 12764,                     # Leituras.Subestacao_EnergiaConsumidaGVArh
    "ENERGIA_FORNECIDA_MVArh":                  59 + 12764,                     # Leituras.Subestacao_EnergiaConsumidaMVArh
    "ENERGIA_FORNECIDA_KVArh":                  60 + 12764,                     # Leituras.Subestacao_EnergiaConsumidaKVArh

    ## DISJUNTORES
    "DJ_01":                                    0 + 12564,                      # PACP-SE - Alimentação Relés de Nível do Poço de Drenagem - Disj. Q220.1
    "DJ_02":                                    1 + 12564,                      # PACP-SE - Alimentação Circuitos de Comando - Disj. Q125.0
    "DJ_03":                                    2 + 12564,                      # PACP-SE - Alimentação Relé de Proteção 59N - Disj. Q125.1
    "DJ_04":                                    3 + 12564,                      # PACP-SE - Alimentação Relés de Proteção SEL311C e SEL787 -  Disj. Q125.2
    "DJ_05":                                    4 + 12564,                      # PACP-SE - Alimentação Circuitos de Comando Seccionadora 89L -  Disj. Q125.4
    "DJ_06":                                    5 + 12564,                      # PACP-SE - Alimentação Circuito de Bloqueio Lâmina de Terra -  Disj. Q125.5
    "DJ_07":                                    6 + 12564,                      # PACP-SE - Alimentação Circuito de Comando Disjuntor 52L -  Disj. Q125.6
    "DJ_08":                                    7 + 12564,                      # PACP-SE - Alimentação Motor Carregamento da Mola do Disjuntor 52L -  Disj. Q125.7
    "DJ_09":                                    8 + 12564,                      # PCP-U1 - Alimentação Fonte 125/24Vcc -  Disj. Q125.3
    "DJ_10":                                    9 + 12564,                      # PCP-U1 - Alimentação Circuitos de Comando -  Disj. Q24.1
    "DJ_11":                                    10 + 12564,                     # PCP-U2 - Alimentação Fonte 125/24Vcc -  Disj. Q125.3
    "DJ_12":                                    11 + 12564,                     # PCP-U2 - Alimentação Circuitos de Comando -  Disj. Q24.1
    "DJ_13":                                    12 + 12564,                     # PCP-U3 - Alimentação Fonte 125/24Vcc -  Disj. Q125.3
    "DJ_14":                                    13 + 12564,                     # PCP-U3 - Alimentação Circuitos de Comando -  Disj. Q24.1
    "DJ_15":                                    14 + 12564,                     # PCP-U4 - Alimentação Fonte 125/24Vcc -  Disj. Q125.3
    "DJ_16":                                    15 + 12564,                     # PCP-U4 - Alimentação Circuitos de Comando -  Disj. Q24.1
    "DJ_17":                                    16 + 12564,                     # CSA-U1 - Alimentação Circuitos de Sinalização - Disj. Q125.0
    "DJ_18":                                    17 + 12564,                     # CSA-U2 - Alimentação Circuitos de Sinalização - Disj. Q125.0
    "DJ_19":                                    18 + 12564,                     # CB01 - Carregador de Baterias 01 -  Disj. Q1/Q2/Q3
    "DJ_20":                                    19 + 12564,                     # CB02 - Carregador de Baterias 02 -  Disj. Q1/Q2/Q3
    "DJ_21":                                    20 + 12564,                     # PDSA-CC - Alimentação Principal CB01 -  Disj. Q125.E1
    "DJ_22":                                    21 + 12564,                     # PDSA-CC - Alimentação Principal CB02 -  Disj. Q125.E2
    "DJ_23":                                    22 + 12564,                     # PDSA-CC - Alimentação Inversor 125Vcc/220Vca -  Disj. Q125.1
    "DJ_24":                                    23 + 12564,                     # PDSA-CC - Alimentação do Painel PDSA-CA -  Disj. Q125.3
    "DJ_25":                                    24 + 12564,                     # PDSA-CC - Alimentação do Rack de Comunicação -  Disj. Q125.4
    "DJ_26":                                    25 + 12564,                     # PDSA-CC - Alimentação do Cubículo CSA-U1 -  Disj. Q125.5
    "DJ_27":                                    26 + 12564,                     # PDSA-CC - Alimentação do Cubículo CSA-U2 -  Disj. Q125.6
    "DJ_28":                                    27 + 12564,                     # PDSA-CC - Alimentação Painel do Trafo Elevador -  Disj. Q125.7
    "DJ_29":                                    28 + 12564,                     # PDSA-CC - Alimentação Monitor de Temperatura do TSA-01 -  Disj. Q125.8
    "DJ_30":                                    29 + 12564,                     # PDSA-CC - Alimentação Monitor de Temperatura do TSA-02 -  Disj. Q125.9
    "DJ_31":                                    30 + 12564,                     # PDSA-CC - Alimentação Reserva -  Disj. Q125.10
    "DJ_32":                                    31 + 12564,                     # PDSA-CC - Alimentação das Cargas da UG01 -  Disj. 1Q125.0
    "DJ_33":                                    32 + 12564,                     # PDSA-CC - Alimentação do Painel PCP-U1 -  Disj. 1Q125.1
    "DJ_34":                                    33 + 12564,                     # PDSA-CC - Alimentação do Quadro Q49-U1 -  Disj. 1Q125.2
    "DJ_35":                                    34 + 12564,                     # PDSA-CC - Alimentação do Cubículo CSG-U1 -  Disj. 1Q125.3
    "DJ_36":                                    35 + 12564,                     # PDSA-CC - Alimentação Painel do Regulador de Tensão UG01 -  Disj. 1Q125.4
    "DJ_37":                                    36 + 12564,                     # PDSA-CC - Alimentação do Filtro Duplo UG01 -  Disj. 1Q125.5
    "DJ_38":                                    37 + 12564,                     # PDSA-CC - Alimentação Reserva -  Disj. 1Q125.6
    "DJ_39":                                    38 + 12564,                     # PDSA-CC - Alimentação das Cargas da UG02 -  Disj. 2Q125.0
    "DJ_40":                                    39 + 12564,                     # PDSA-CC - Alimentação do Painel PCP-U2 -  Disj. 2Q125.1
    "DJ_41":                                    40 + 12564,                     # PDSA-CC - Alimentação do Quadro Q49-U2 -  Disj. 2Q125.2
    "DJ_42":                                    41 + 12564,                     # PDSA-CC - Alimentação do Cubículo CSG-U2 -  Disj. 2Q125.3
    "DJ_43":                                    42 + 12564,                     # PDSA-CC - Alimentação Painel do Regulador de Tensão UG02 -  Disj. 2Q125.4
    "DJ_44":                                    43 + 12564,                     # PDSA-CC - Alimentação do Filtro Duplo UG02 -  Disj. 2Q125.5
    "DJ_45":                                    44 + 12564,                     # PDSA-CC - Alimentação Reserva -  Disj. 2Q125.6
    "DJ_46":                                    45 + 12564,                     # PDSA-CC - Alimentação das Cargas da UG03 -  Disj. 3Q125.0
    "DJ_47":                                    46 + 12564,                     # PDSA-CC - Alimentação do Painel PCP-U3 -  Disj. 3Q125.1
    "DJ_48":                                    47 + 12564,                     # PDSA-CC - Alimentação do Quadro Q49-U3 -  Disj. 3Q125.2
    "DJ_49":                                    48 + 12564,                     # PDSA-CC - Alimentação do Cubículo CSG-U3 -  Disj. 3Q125.3
    "DJ_50":                                    49 + 12564,                     # PDSA-CC - Alimentação Painel do Regulador de Tensão UG03 -  Disj. 3Q125.4
    "DJ_51":                                    50 + 12564,                     # PDSA-CC - Alimentação do Filtro Duplo UG03 -  Disj. 3Q125.5
    "DJ_52":                                    51 + 12564,                     # PDSA-CC - Alimentação Reserva -  Disj. 3Q125.6
    "DJ_53":                                    52 + 12564,                     # PDSA-CC - Alimentação das Cargas da UG04 -  Disj. 4Q125.0
    "DJ_54":                                    53 + 12564,                     # PDSA-CC - Alimentação do Painel PCP-U4 -  Disj. 4Q125.1
    "DJ_55":                                    54 + 12564,                     # PDSA-CC - Alimentação do Quadro Q49-U4 -  Disj. 4Q125.2
    "DJ_56":                                    55 + 12564,                     # PDSA-CC - Alimentação do Cubículo CSG-U4 -  Disj. 4Q125.3
    "DJ_57":                                    56 + 12564,                     # PDSA-CC - Alimentação Painel do Regulador de Tensão UG04 -  Disj. 4Q125.4
    "DJ_58":                                    57 + 12564,                     # PDSA-CC - Alimentação do Filtro Duplo UG04 -  Disj. 4Q125.5
    "DJ_59":                                    58 + 12564,                     # PDSA-CC - Alimentação Reserva -  Disj. 4Q125.6
    "DJ_60":                                    59 + 12564,                     # PDSA-CA - Alimentação Bomba Drenagem 01 -  Disj. QM1
    "DJ_61":                                    60 + 12564,                     # PDSA-CA - Alimentação Bomba Drenagem 02 -  Disj. QM2
    "DJ_62":                                    61 + 12564,                     # PDSA-CA - Alimentação Bomba Drenagem 03 -  Disj. QM3
    "DJ_63":                                    62 + 12564,                     # PDSA-CA - Alimentação do Compressor de AR -  Disj. QM4
    "DJ_64":                                    63 + 12564,                     # PDSA-CA - Alimentação do Painel PACP-SE -  Disj. Q220.6
    "DJ_65":                                    64 + 12564,                     # PDSA-CA - Alimentação 125Vcc Principal -  Disj. Q125.0
    "DJ_66":                                    65 + 12564,                     # PDSA-CA - Alimentação 380Vca Principal -  Disj. Q380.0
    "DJ_67":                                    66 + 12564,                     # PDSA-CA - Alimentação do Painel PCTA -  Disj. Q380.1
    "DJ_68":                                    67 + 12564,                     # PDSA-CA - Alimentação da Ponte Rolante -  Disj. Q380.2
    "DJ_69":                                    68 + 12564,                     # PDSA-CA - Alimentação Monovia de Jusante -  Disj. Q380.3
    "DJ_70":                                    69 + 12564,                     # PDSA-CA - Alimentação do Quadro QDLCF -  Disj. Q380.4
    "DJ_71":                                    70 + 12564,                     # PDSA-CA - Alimentação do Elevador da Casa de Força -  Disj. Q380.5
    "DJ_72":                                    71 + 12564,                     # PDSA-CA - Alimentação do Painel PCAD -  Disj. Q380.6
    "DJ_73":                                    72 + 12564,                     # PDSA-CA - Alimentação Sistema de Retrolavagem do Filtro 01 -  Disj. Q380.7
    "DJ_74":                                    73 + 12564,                     # PDSA-CA - Alimentação Sistema de Retrolavagem do Filtro 02 -  Disj. Q380.8
    "DJ_75":                                    74 + 12564,                     # PDSA-CA - Alimentação do Carregador de Baterias 01 -  Disj. Q380.9
    "DJ_76":                                    75 + 12564,                     # PDSA-CA - Alimentação do Carregador de Baterias 02 -  Disj. Q380.10
    "DJ_77":                                    76 + 12564,                     # PDSA-CA - Alimentação das Cargas Essenciais da UG01 -  Disj. 1Q380.0
    "DJ_78":                                    77 + 12564,                     # PDSA-CA - Alimentação das Cargas Não Essenciais da UG01 -  Disj. 1Q380.1
    "DJ_79":                                    78 + 12564,                     # PDSA-CA - Alimentação das Cargas Essenciais da UG02 -  Disj. 2Q380.0
    "DJ_80":                                    79 + 12564,                     # PDSA-CA - Alimentação das Cargas Não Essenciais da UG02 -  Disj. 2Q380.1
    "DJ_81":                                    80 + 12564,                     # PDSA-CA - Alimentação das Cargas Essenciais da UG03 -  Disj. 3Q380.0
    "DJ_82":                                    81 + 12564,                     # PDSA-CA - Alimentação das Cargas Não Essenciais da UG03 -  Disj. 3Q380.1
    "DJ_83":                                    82 + 12564,                     # PDSA-CA - Alimentação das Cargas Essenciais da UG04 -  Disj. 4Q380.0
    "DJ_84":                                    83 + 12564,                     # PDSA-CA - Alimentação das Cargas Não Essenciais da UG04 -  Disj. 4Q380.1
    "DJ_85":                                    84 + 12564,                     # Disjuntor 52L - Alimentação Motor de Carregamento da Mola -  Disj. F1
    "DJ_86":                                    85 + 12564,                     # Disjuntor 52L - Alimentação Circuito de Aquecimento -  Disj. F2
    "DJ_87":                                    86 + 12564,                     # Seccionadora 89L - Alimentação Circuito de Comando -  Disj. F1
    "DJ_88":                                    87 + 12564,                     # Seccionadora 89L - Alimentação Motor de Carregamento da Mola -  Disj. F3
    "DJ_89":                                    88 + 12564,                     # PDSA-CA - Alimentação Bomba 01 Injeção Água Selo Mecânico - Disj. QM5
    "DJ_90":                                    89 + 12564,                     # PDSA-CA - Alimentação Bomba 02 Injeção Água Selo Mecânico - Disj. QM6
    "DJ_91":                                    90 + 12564,                     # PDSA-CA - Alimentação Bomba 01 Água Serviço - Disj. QM7
    "DJ_92":                                    91 + 12564,                     # PDSA-CA - Alimentação Bomba 02 Água Serviço - Disj. QM8
    "DJ_93":                                    92 + 12564,                     # PDSA-CA - Alimentação UCP Bombas de Drenagem - Disj. Q220.11
    "DJ_94":                                    93 + 12564,                     # PDSA-CA - Alimentação Torre de Resfriamento - Disj. Q380.11
    "DJ_95":                                    94 + 12564,                     # PDSA-CA - Alimentação Compressor de Ar - Disj. Q380.12
    "DJ_96":                                    95 + 12564,                     # PDSA-CA - Alimentação do Guincho da Bomba de Esgotamento - Disj. Q380.13
    "DJ_97":                                    96 + 12564,                     # PDSA-CA - Alimentação do Quadro QDLSE - Disj. Q380.14
    "DJ_98":                                    97 + 12564,                     # PACP-SE - Alimentação Válvulas Sistema de Água de Refrigeração -  Disj. Q125.8
    "DJ_99":                                    98 + 12564,                     # PDSA-CC - Alimentação do Painel PINV -  Disj. Q125.11
    "DJ_100":                                   99 + 12564,                     # PINV - Alimentação Boost 01 -  Disj. Q125.0
    "DJ_101":                                   100 + 12564,                    # PINV - Alimentação Boost 02 -  Disj. Q125.1
    "DJ_102":                                   101 + 12564,                    # PINV - Alimentação Fonte 125/24Vcc (Ventilação Forçada e Switch) -  Disj. Q125.2


    ## ALARMES

    "Alarme01_00":                              [0 + 14089, 0],
    "Alarme01_01":                              [0 + 14089, 1],
    "Alarme01_12":                              [0 + 14089, 12],
    "Alarme01_13":                              [0 + 14089, 13],
    "Alarme01_14":                              [0 + 14089, 14],

    "Alarme02_00":                              [1 + 14089, 0],
    "Alarme02_01":                              [1 + 14089, 1],
    "Alarme02_02":                              [1 + 14089, 2],
    "Alarme02_04":                              [1 + 14089, 4],
    "Alarme02_05":                              [1 + 14089, 5],
    "Alarme02_07":                              [1 + 14089, 7],
    "Alarme02_08":                              [1 + 14089, 8],
    "Alarme02_11":                              [1 + 14089, 11],
    "Alarme02_12":                              [1 + 14089, 12],
    "Alarme02_13":                              [1 + 14089, 13],

    "Alarme03_00":                              [2 + 14089, 0],
    "Alarme03_01":                              [2 + 14089, 1],
    "Alarme03_02":                              [2 + 14089, 2],
    "Alarme03_03":                              [2 + 14089, 3],
    "Alarme03_04":                              [2 + 14089, 4],
    "Alarme03_05":                              [2 + 14089, 5],
    "Alarme03_06":                              [2 + 14089, 6],
    "Alarme03_07":                              [2 + 14089, 7],
    "Alarme03_08":                              [2 + 14089, 8],

    "Alarme05_02":                              [4 + 14089, 2],
    "Alarme05_03":                              [4 + 14089, 3],
    "Alarme05_04":                              [4 + 14089, 4],
    "Alarme05_05":                              [4 + 14089, 5],
    "Alarme05_06":                              [4 + 14089, 6],
    "Alarme05_07":                              [4 + 14089, 7],
    "Alarme05_08":                              [4 + 14089, 8],
    "Alarme05_09":                              [4 + 14089, 9],
    "Alarme05_10":                              [4 + 14089, 10],
    "Alarme05_11":                              [4 + 14089, 11],
    "Alarme05_12":                              [4 + 14089, 12],
    "Alarme05_13":                              [4 + 14089, 13],
    "Alarme05_14":                              [4 + 14089, 14],

    "Alarme09_07":                              [8 + 14089, 7],
    "Alarme09_08":                              [8 + 14089, 8],

    "Alarme12_03":                              [11 + 14089, 3],

    "Alarme14_07":                              [13 + 14089, 7],

    "Alarme16_04":                              [15 + 14089, 4],
    "Alarme16_05":                              [15 + 14089, 5],
    "Alarme16_06":                              [15 + 14089, 6],
    "Alarme16_07":                              [15 + 14089, 7],
    "Alarme16_08":                              [15 + 14089, 8],
    "Alarme16_09":                              [15 + 14089, 9],

    "Alarme18_04":                              [17 + 14089, 4],
    "Alarme18_05":                              [17 + 14089, 5],
    "Alarme18_13":                              [17 + 14089, 13],
    "Alarme18_14":                              [17 + 14089, 14],
    "Alarme18_15":                              [17 + 14089, 15],

    "Alarme19_00":                              [18 + 14089, 0],
    "Alarme19_01":                              [18 + 14089, 1],
    "Alarme19_02":                              [18 + 14089, 2],
    "Alarme19_03":                              [18 + 14089, 3],
    "Alarme19_04":                              [18 + 14089, 4],
    "Alarme19_05":                              [18 + 14089, 5],
    "Alarme19_15":                              [18 + 14089, 15],

    "Alarme20_00":                              [19 + 14089, 0],
    "Alarme20_01":                              [19 + 14089, 1],
    "Alarme20_02":                              [19 + 14089, 2],
    "Alarme20_03":                              [19 + 14089, 3],
    "Alarme20_04":                              [19 + 14089, 4],
    "Alarme20_05":                              [19 + 14089, 5],
    "Alarme20_15":                              [19 + 14089, 15],

    "Alarme21_00":                              [20 + 14089, 0],
    "Alarme21_01":                              [20 + 14089, 1],
}


REG_TDA = {
    ## COMANDOS
    # UHTA
    "CMD_UHTA01_RODIZIO_AUTOMATICO":            38 + 12289,                     # Comandos.PCTA_UHTA01_RodizioAutomatico
    "CMD_UHTA01_RODIZIO_MANUAL":                39 + 12289,                     # Comandos.PCTA_UHTA01_RodizioManual
    "CMD_UHTA02_RODIZIO_AUTOMATICO":            40 + 12289,                     # Comandos.PCTA_UHTA02_RodizioAutomatico
    "CMD_UHTA02_RODIZIO_MANUAL":                41 + 12289,                     # Comandos.PCTA_UHTA02_RodizioManual
    "CMD_UHTA01_BOMBA_01_LIGAR":                42 + 12289,                     # Comandos.PCTA_UHTA01_Bomba01Ligar
    "CMD_UHTA01_BOMBA_01_DESLIGAR":             43 + 12289,                     # Comandos.PCTA_UHTA01_Bomba01Desligar
    "CMD_UHTA01_BOMBA_01_PRINCIPAL":            44 + 12289,                     # Comandos.PCTA_UHTA01_Bomba01Principal
    "CMD_UHTA01_BOMBA_02_LIGAR":                45 + 12289,                     # Comandos.PCTA_UHTA01_Bomba02Ligar
    "CMD_UHTA01_BOMBA_02_DESLIGAR":             46 + 12289,                     # Comandos.PCTA_UHTA01_Bomba02Desligar
    "CMD_UHTA01_BOMBA_02_PRINCIPAL":            47 + 12289,                     # Comandos.PCTA_UHTA01_Bomba02Principal
    "CMD_UHTA02_BOMBA_01_LIGAR":                48 + 12289,                     # Comandos.PCTA_UHTA02_Bomba01Ligar
    "CMD_UHTA02_BOMBA_01_DESLIGAR":             49 + 12289,                     # Comandos.PCTA_UHTA02_Bomba01Desligar
    "CMD_UHTA02_BOMBA_01_PRINCIPAL":            50 + 12289,                     # Comandos.PCTA_UHTA02_Bomba01Principal
    "CMD_UHTA02_BOMBA_02_LIGAR":                51 + 12289,                     # Comandos.PCTA_UHTA02_Bomba02Ligar
    "CMD_UHTA02_BOMBA_02_DESLIGAR":             52 + 12289,                     # Comandos.PCTA_UHTA02_Bomba02Desligar
    "CMD_UHTA02_BOMBA_02_PRINCIPAL":            53 + 12289,                     # Comandos.PCTA_UHTA02_Bomba02Principal

    # Sensores
    "CMD_SENSOR_PRESEN_INIBIR":                 54 + 12289,                     # Comandos.PCTA_SensorPresencaInibir
    "CMD_SENSOR_PRESEN_DESINIBIR":              55 + 12289,                     # Comandos.PCTA_SensorPresencaDesinibir


    ## SETPOINTS
    # Níveis
    "NV_BARRAGEM_HH":                           0 + 13569,                      # Setpoints.Usina_NivelBarragem_HH
    "NV_BARRAGEM_LL":                           0 + 13569,                      # Setpoints.Usina_NivelBarragem_LL
    "NV_BARRAGEM_TOLERANCIA":                   1 + 13569,                      # Setpoints.Usina_NivelBarragem_Tolerancia
    "NV_CAMARA_CARGA_HH":                       2 + 13569,                      # Setpoints.Usina_NiveCamaraCarga_HH
    "NV_CAMARA_CARGA_LL":                       3 + 13569,                      # Setpoints.Usina_NiveCamaraCarga_LL
    "NV_CAMARA_CARGA_TOLERANCIA":               4 + 13569,                      # Setpoints.Usina_NiveCamaraCarga_Tolerancia

    # Grade
    "GRADE_SUJA_DIF_ALARME":                    5 + 13569,                      # Setpoints.Usina_GradeSujaDiferencial_Alarme
    "GRADE_SUJA_DIF_TRIP":                      6 + 13569,                      # Setpoints.Usina_GradeSujaDiferencial_TRIP

    # Manobras UHTA
    "UHTA01_MANO_RODIZIO_LIDER":                9 + 13569,                     # Setpoints.PCTA_UHTA01_ManobrasRodizioLider
    "UHTA01_MANO_RODIZIO_RETAGUARDA":           10 + 13569,                     # Setpoints.PCTA_UHTA01_ManobrasRodizioRetaguarda
    "UHTA02_MANO_RODIZIO_LIDER":                11 + 13569,                     # Setpoints.PCTA_UHTA02_ManobrasRodizioLider
    "UHTA02_MANO_RODIZIO_RETAGUARDA":           12 + 13569,                     # Setpoints.PCTA_UHTA02_ManobrasRodizioRetaguarda

    # Diferencial de Grade
    "DIFERENCIAL_GRADE_01":                     21 + 13569,                     # Setpoints.DiferenciaGrade01
    "DIFERENCIAL_GRADE_02":                     24 + 13569,                     # Setpoints.DiferenciaGrade02
    "DIFERENCIAL_GRADE_03":                     25 + 13569,                     # Setpoints.DiferenciaGrade03
    "DIFERENCIAL_GRADE_04":                     26 + 13569,                     # Setpoints.DiferenciaGrade04


    ## LEITURAS
    # Níveis
    "NV_JUSANTE":                               1 + 12764,                      # Leituras.NivelJusante
    "NV_BARRAGEM":                              2 + 12764,                      # Leituras.NivelBarragem
    "NV_CANALADUCAO":                           3 + 12764,                      # Leituras.NivelCanalAducao
    "NV_CAMARACARGA":                           4 + 12764,                      # Leituras.NivelCamaraCarga
    "NV_POS_GRADE_01":                          226 + 12764,                    # Leituras.NivelPosGrade01
    "NV_POS_GRADE_02":                          227 + 12764,                    # Leituras.NivelPosGrade02
    "NV_POS_GRADE_03":                          228 + 12764,                    # Leituras.NivelPosGrade03
    "NV_POS_GRADE_04":                          229 + 12764,                    # Leituras.NivelPosGrade04

    # Pluviometro
    "PLUVIOMETRO":                              8 + 12764,                      # Leituras.Pluviometro

    # PCTA
    "COMPORTA_01_INFO":                         126 + 12764,                    # Leituras.PCTA_Comporta01_Info
    "COMPORTA_01_TEMPO_EFETIVO_EQUAL":          127 + 12764,                    # Leituras.PCTA_Comporta01TempoEfetivoEqualizacao
    "COMPORTA_01_POSICAO":                      128 + 12764,                    # Leituras.PCTA_Comporta01Posicao
    "COMPORTA_02_INFO":                         129 + 12764,                    # Leituras.PCTA_Comporta02_Info
    "COMPORTA_02_TEMPO_EFETIVO_EQUAL":          130 + 12764,                    # Leituras.PCTA_Comporta02TempoEfetivoEqualizacao
    "COMPORTA_02_POSICAO":                      131 + 12764,                    # Leituras.PCTA_Comporta02Posicao
    "COMPORTA_03_INFO":                         132 + 12764,                    # Leituras.PCTA_Comporta03_Info
    "COMPORTA_03_TEMPO_EFETIVO_EQUAL":          133 + 12764,                    # Leituras.PCTA_Comporta03TempoEfetivoEqualizacao
    "COMPORTA_03_POSICAO":                      134 + 12764,                    # Leituras.PCTA_Comporta03Posicao
    "COMPORTA_04_INFO":                         135 + 12764,                    # Leituras.PCTA_Comporta04_Info
    "COMPORTA_04_TEMPO_EFETIVO_EQUAL":          136 + 12764,                    # Leituras.PCTA_Comporta04TempoEfetivoEqualizacao
    "COMPORTA_04_POSICAO":                      137 + 12764,                    # Leituras.PCTA_Comporta04Posicao

    # UHTA
    "UHTA01_INFO":                              139 + 12764,                    # Leituras.PCTA_UHTA01_Info
    "UHTA01_OPERACIONAL":                       [139 + 12764, 0],               # PCTA.UHTA01.Info.Operacional
    "UHTA01_LIGADA":                            [139 + 12764, 1],               # PCTA.UHTA01.Info.Ligada

    "UHTA01_BOMBAS":                            139 + 12764,                    # Leituras.PCTA_UHTA01_Bombas
    "UHTA01_BOMBAS01":                          [139 + 12764, 0],               # PCTA.UHTA01.Bombas.[01]
    "UHTA01_BOMBAS02":                          [139 + 12764, 1],               # PCTA.UHTA01.Bombas.[02]

    "UHTA01_RODIZIO":                           140 + 12764,                    # Leituras.PCTA_UHTA01_Rodizio
    "UHTA01_RODIZ_BOMBA01":                     [140 + 12764, 0],               # PCTA.UHTA01.Rodizio.Bomba01
    "UHTA01_RODIZ_BOMBA02":                     [140 + 12764, 1],               # PCTA.UHTA01.Rodizio.Bomba02
    "UHTA01_RODIZ_HABILITADO":                  [140 + 12764, 2],               # PCTA.UHTA01.Rodizio.Habilitado

    "UHTA01_ACUMULADOR":                        141 + 12764,                    # Leituras.PCTA_UHTA01_Acumulador
    "UHTA01_ACUM_BOMBA_LIDER":                  [141 + 12764, 0],               # PCTA.UHTA01.AcumuladorBombaLider
    "UHTA01_ACUM_BOMBA_RETAGUARDA":             [141 + 12764, 1],               # PCTA.UHTA01.AcumuladorBombaRetaguarda

    "UHTA01_FILTROS":                           143 + 12764,                    # Leituras.PCTA_UHTA01_Filtros
    "UHTA01_FILTROS01":                         [143 + 12764, 0],               # PCTA.UHTA01.Filtros.[01]

    "UHTA01_NIVEL_OLEO_INFO":                   144 + 12764,                    # Leituras.PCTA_UHTA01_NivelOleo_Info
    "UHTA01_NIVEL_OLEO_LL":                     [144 + 12764, 0],               # PCTA.UHTA01.NivelOleo_Info.LL
    "UHTA01_NIVEL_OLEO_HH":                     [144 + 12764, 1],               # PCTA.UHTA01.NivelOleo_Info.HH

    "UHTA01_TEMPERATURA_OLEO_INFO":             145 + 12764,                    # Leituras.PCTA_UHTA01_TemperaturaOleo_info
    "UHTA01_TEMP_OLEO_H":                       [145 + 12764, 0],               # PCTA.UHTA01.TemperaturaOleo_Info.H
    "UHTA01_TEMP_OLEO_HH":                      [145 + 12764, 1],               # PCTA.UHTA01.TemperaturaOleo_Info.HH

    "UHTA01_VALVULAS":                          146 + 12764,                    # Leituras.PCTA_UHTA01_Valvulas
    "UHTA01_VALVULAS01":                        [146 + 12764, 0],               # PCTA.UHTA01.Valvulas.[01]

    "UHTA01_PRESSOSTATOS":                      147 + 12764,                    # Leituras.PCTA_UHTA01_Pressostatos
    "UHTA01_PRESSOSTATOS01":                    [147 + 12764, 0],               # PCTA.UHTA01.Pressostatos.[01]
    "UHTA01_PRESSOSTATOS02":                    [147 + 12764, 1],               # PCTA.UHTA01.Pressostatos.[02]
    "UHTA01_PRESSOSTATOS03":                    [147 + 12764, 2],               # PCTA.UHTA01.Pressostatos.[03]

    "UHTA01_TEMPERATURA_OLEO":                  148 + 12764,                    # Leituras.PCTA_UHTA01_TemperaturaOleo
    "UHTA01_NIVEL_OLEO":                        149 + 12764,                    # Leituras.PCTA_UHTA01_NivelOleo

    "UHTA02_INFO":                              149 + 12764,                    # Leituras.PCTA_UHTA02_Info
    "UHTA02_OPERACIONAL":                       [149 + 12764, 0],               # PCTA.UHTA02.Info.Operacional
    "UHTA02_LIGADA":                            [149 + 12764, 1],               # PCTA.UHTA02.Info.Ligada

    "UHTA02_BOMBAS":                            151 + 12764,                    # Leituras.PCTA_UHTA02_Bombas
    "UHTA02_BOMBAS01":                          [151 + 12764, 0],               # PCTA.UHTA02.Bombas.[01]
    "UHTA02_BOMBAS02":                          [151 + 12764, 1],               # PCTA.UHTA02.Bombas.[02]

    "UHTA02_RODIZIO":                           152 + 12764,                    # Leituras.PCTA_UHTA02_Rodizio
    "UHTA02_RODIZ_BOMBA01":                     [152 + 12764, 0],               # PCTA.UHTA02.Rodizio.Bomba01
    "UHTA02_RODIZ_BOMBA02":                     [152 + 12764, 1],               # PCTA.UHTA02.Rodizio.Bomba02
    "UHTA02_RODIZ_HABILITADO":                  [152 + 12764, 2],               # PCTA.UHTA02.Rodizio.Habilitado

    "UHTA02_ACUMULADOR":                        153 + 12764,                    # Leituras.PCTA_UHTA02_AcumuladorBombaLider
    "UHTA02_ACUM_BOMBA_LIDER":                  [153 + 12764, 0],               # PCTA.UHTA02.AcumuladorBombaLider
    "UHTA02_ACUM_BOMBA_RETAGUARDA":             [153 + 12764, 1],               # PCTA.UHTA02.AcumuladorBombaRetaguarda

    "UHTA02_FILTROS":                           155 + 12764,                    # Leituras.PCTA_UHTA02_Filtros
    "UHTA02_FILTROS01":                         [155 + 12764, 0],               # PCTA.UHTA02.Filtros.[01]

    "UHTA02_NIVEL_OLEO_INFO":                   156 + 12764,                    # Leituras.PCTA_UHTA02_NivelOleo_Info
    "UHTA02_NIVEL_OLEO_LL":                     [156 + 12764, 0],               # PCTA.UHTA02.NivelOleo_Info.LL
    "UHTA02_NIVEL_OLEO_HH":                     [156 + 12764, 1],               # PCTA.UHTA02.NivelOleo_Info.HH

    "UHTA02_TEMPERATURA_OLEO_INFO":             157 + 12764,                    # Leituras.PCTA_UHTA02_TemperaturaOleo_info
    "UHTA02_TEMP_OLEO_H":                       [157 + 12764, 0],               # PCTA.UHTA02.TemperaturaOleo_Info.H
    "UHTA02_TEMP_OLEO_HH":                      [157 + 12764, 1],               # PCTA.UHTA02.TemperaturaOleo_Info.HH

    "UHTA02_VALVULAS":                          158 + 12764,                    # Leituras.PCTA_UHTA02_Valvulas
    "UHTA02_VALVULAS01":                        [158 + 12764, 0],               # PCTA.UHTA02.Valvulas.[01]

    "UHTA02_PRESSOSTATOS":                      159 + 12764,                    # Leituras.PCTA_UHTA02_Pressostatos
    "UHTA02_PRESSOSTATOS01":                    [159 + 12764, 0],               # PCTA.UHTA02.Pressostatos.[01]
    "UHTA02_PRESSOSTATOS02":                    [159 + 12764, 1],               # PCTA.UHTA02.Pressostatos.[02]
    "UHTA02_PRESSOSTATOS03":                    [159 + 12764, 2],               # PCTA.UHTA02.Pressostatos.[03]

    "UHTA02_TEMPERATURA_OLEO":                  160 + 12764,                    # Leituras.PCTA_UHTA02_TemperaturaOleo
    "UHTA02_NIVEL_OLEO":                        161 + 12764,                    # Leituras.PCTA_UHTA02_NivelOleo

    "PCTA_INFO":                                162 + 12764,                    # Leituras.PCTA_Info
    "PCTA_FALTA_FASE":                          [162 + 12764, 0],               # PCTA.Info.FaltaFase
    "PCTA_SENS_PRESEN_ATUADO":                  [162 + 12764, 1],               # PCTA.Info.SensorPresencaAtuado
    "PCTA_SENS_PRESEN_INIBIDO":                 [162 + 12764, 2],               # PCTA.Info.SensorPresencaInibido
    "PCTA_SENS_FUMA_ATUADO":                    [162 + 12764, 3],               # PCTA.Info.SensorFumacaAtuado
    "PCTA_SENS_FUMA_DESCONEC":                  [162 + 12764, 4],               # PCTA.Info.SensorFumacaDesconectado
    "PCTA_MODO_REMOTO":                         [162 + 12764, 5],               # PCTA.Info.ModoRemoto


    ## ALARMES

    "Alarme01_04":                              [0 + 14089, 4],
    "Alarme01_05":                              [0 + 14089, 5],
    "Alarme01_06":                              [0 + 14089, 6],

    "Alarme22_00":                              [21 + 14089, 0],
    "Alarme22_03":                              [21 + 14089, 3],
    "Alarme22_04":                              [21 + 14089, 4],
    "Alarme22_05":                              [21 + 14089, 5],
    "Alarme22_06":                              [21 + 14089, 6],
    "Alarme22_07":                              [21 + 14089, 7],
    "Alarme22_08":                              [21 + 14089, 8],
    "Alarme22_09":                              [21 + 14089, 9],
    "Alarme22_10":                              [21 + 14089, 10],
    "Alarme22_11":                              [21 + 14089, 11],
    "Alarme22_14":                              [21 + 14089, 14],
    "Alarme22_15":                              [21 + 14089, 15],

    "Alarme23_01":                              [22 + 14089, 1],
    "Alarme23_02":                              [22 + 14089, 2],
    "Alarme23_04":                              [22 + 14089, 4],
    "Alarme23_05":                              [22 + 14089, 5],
    "Alarme23_06":                              [22 + 14089, 6],
    "Alarme23_07":                              [22 + 14089, 7],
    "Alarme23_08":                              [22 + 14089, 8],
    "Alarme23_11":                              [22 + 14089, 11],
    "Alarme23_12":                              [22 + 14089, 12],
    "Alarme23_13":                              [22 + 14089, 13],
    "Alarme23_14":                              [22 + 14089, 14],
    "Alarme23_15":                              [22 + 14089, 15],

    "Alarme24_02":                              [23 + 14089, 2],
    "Alarme24_03":                              [23 + 14089, 3],
    "Alarme24_04":                              [23 + 14089, 4],
    "Alarme24_05":                              [23 + 14089, 5],
    "Alarme24_06":                              [23 + 14089, 6],
    "Alarme24_07":                              [23 + 14089, 7],
    "Alarme24_08":                              [23 + 14089, 8],
    "Alarme24_09":                              [23 + 14089, 9],
    "Alarme24_10":                              [23 + 14089, 10],
    "Alarme24_13":                              [23 + 14089, 13],
    "Alarme24_14":                              [23 + 14089, 14],

    "Alarme25_00":                              [24 + 14089, 0],
    "Alarme25_01":                              [24 + 14089, 1],
    "Alarme25_03":                              [24 + 14089, 3],
    "Alarme25_04":                              [24 + 14089, 4],
    "Alarme25_05":                              [24 + 14089, 5],
    "Alarme25_06":                              [24 + 14089, 6],
    "Alarme25_07":                              [24 + 14089, 7],
    "Alarme25_10":                              [24 + 14089, 10],
    "Alarme25_11":                              [24 + 14089, 11],
    "Alarme25_12":                              [24 + 14089, 12],
    "Alarme25_13":                              [24 + 14089, 13],
    "Alarme25_14":                              [24 + 14089, 14],

    "Alarme26_01":                              [25 + 14089, 1],
    "Alarme26_02":                              [25 + 14089, 2],
    "Alarme26_04":                              [25 + 14089, 4],
    "Alarme26_05":                              [25 + 14089, 5],
    "Alarme26_07":                              [25 + 14089, 7],
    "Alarme26_08":                              [25 + 14089, 8],
    "Alarme26_09":                              [25 + 14089, 9],
    "Alarme26_10":                              [25 + 14089, 10],
    "Alarme26_11":                              [25 + 14089, 11],
    "Alarme26_12":                              [25 + 14089, 12],
    "Alarme26_13":                              [25 + 14089, 13],
    "Alarme26_14":                              [25 + 14089, 14],

    "Alarme27_00":                              [26 + 14089, 0],
    "Alarme27_01":                              [26 + 14089, 1],
    "Alarme27_02":                              [26 + 14089, 2],
    "Alarme27_03":                              [26 + 14089, 3],
}


REG_AD = {
    ## COMANDOS
    # Comportas
    "CMD_CP_01_ABRIR":                          56 + 12289,                     # Comandos.PCAD_Comporta01Abrir
    "CMD_CP_01_PARAR":                          57 + 12289,                     # Comandos.PCAD_Comporta01Parar
    "CMD_CP_01_FECHAR":                         58 + 12289,                     # Comandos.PCAD_Comporta01Fechar
    "CMD_CP_01_BUSCAR":                         59 + 12289,                     # Comandos.PCAD_Comporta01Buscar
    "CMD_CP_02_ABRIR":                          60 + 12289,                     # Comandos.PCAD_Comporta02Abrir
    "CMD_CP_02_PARAR":                          61 + 12289,                     # Comandos.PCAD_Comporta02Parar
    "CMD_CP_02_FECHAR":                         62 + 12289,                     # Comandos.PCAD_Comporta02Fechar
    "CMD_CP_02_BUSCAR":                         63 + 12289,                     # Comandos.PCAD_Comporta02Buscar

    # Modo Setpoint
    "CMD_MODO_SP_HABILITAR":                    64 + 12289,                     # Comandos.PCAD_ModoSetpointDesabilitar
    "CMD_MODO_SP_DESABILITAR":                  65 + 12289,                     # Comandos.PCAD_ModoSetpointHabilitar

    # UHCD
    "CMD_UHCD_RODIZIO_AUTO":                    66 + 12289,                     # Comandos.PCAD_UHCD_RodizioAutomatico
    "CMD_UHCD_RODIZIO_MANUAL":                  67 + 12289,                     # Comandos.PCAD_UHCD_RodizioManual

    # Bombas
    "CMD_BOMBA_01_LIGAR":                       68 + 12289,                     # Comandos.PCAD_Bomba01Ligar
    "CMD_BOMBA_01_DESLIGAR":                    69 + 12289,                     # Comandos.PCAD_Bomba01Desligar
    "CMD_BOMBA_01_PRINCIPAL":                   70 + 12289,                     # Comandos.PCAD_Bomba01Principal
    "CMD_BOMBA_02_LIGAR":                       71 + 12289,                     # Comandos.PCAD_Bomba02Ligar
    "CMD_BOMBA_02_DESLIGAR":                    72 + 12289,                     # Comandos.PCAD_Bomba02Desligar
    "CMD_BOMBA_02_PRINCIPAL":                   73 + 12289,                     # Comandos.PCAD_Bomba02Principal

    # Sensores
    "CMD_SENSOR_PRESEN_INIBIR":                 74 + 12289,                     # Comandos.PCAD_SensorPresencaInibir
    "CMD_SENSOR_PRESEN_DESINIBIR":              75 + 12289,                     # Comandos.PCAD_SensorPresencaDesinibir


    ## SETPOINTS
    # Comportas
    "CP_01_SP_POS":                             13 + 13569,                     # Setpoints.PCAD_Comporta01_SetpointPosicao
    "CP_02_SP_POS":                             14 + 13569,                     # Setpoints.PCAD_Comporta02_SetpointPosicao

    # Manobras UHCD
    "UHCD_MANO_RODIZIO_LIDER":                  15 + 13569,                     # Setpoints.PCAD_UHCD_ManobrasRodizioLider
    "UHCD_MANO_RODIZIO_RETAGUARDA":             16 + 13569,                     # Setpoints.PCAD_UHCD_ManobrasRodizioRetaguarda


    ## LEITURAS
    # Comportas
    "CP_01_INFO":                               163 + 12764,                    # Leituras.PCAD_Comporta01_Info
    "CP_01_ABRINDO":                            [163 + 12764, 0],               # PCAD.Comporta01.Info.Abrindo
    "CP_01_FECHANDO":                           [163 + 12764, 1],               # PCAD.Comporta01.Info.Fechando
    "CP_01_ABERTA":                             [163 + 12764, 2],               # PCAD.Comporta01.Info.Aberta
    "CP_01_FECHADA":                            [163 + 12764, 3],               # PCAD.Comporta01.Info.Fechada
    "CP_01_PARADA":                             [163 + 12764, 4],               # PCAD.Comporta01.Info.Parada
    "CP_01_ACION_LOCAL":                        [163 + 12764, 5],               # PCAD.Comporta01.Info.AcionamentoLocal

    "CP_01_POSICAO":                            164 + 12764,                    # Leituras.PCAD_Comporta01_Posicao

    "CP_02_INFO":                               165 + 12764,                    # Leituras.PCAD_Comporta02_Info
    "CP_02_ABRINDO":                            [165 + 12764, 0],               # PCAD.Comporta02.Info.Abrindo
    "CP_02_FECHANDO":                           [165 + 12764, 1],               # PCAD.Comporta02.Info.Fechando
    "CP_02_ABERTA":                             [165 + 12764, 2],               # PCAD.Comporta02.Info.Aberta
    "CP_02_FECHADA":                            [165 + 12764, 3],               # PCAD.Comporta02.Info.Fechada
    "CP_02_PARADA":                             [165 + 12764, 4],               # PCAD.Comporta02.Info.Parada
    "CP_02_ACION_LOCAL":                        [165 + 12764, 5],               # PCAD.Comporta02.Info.AcionamentoLocal

    "CP_02_POSICAO":                            166 + 12764,                    # Leituras.PCAD_Comporta02_Posicao

    # UHCD,
    "UHCD_INFO":                                167 + 12764,                    # Leituras.PCAD_UHCD_Info
    "UHCD_OPERACIONAL":                         [167 + 12764, 0],               # PCAD.UHCD.Info.Operacional
    "UHCD_LIGADA":                              [167 + 12764, 1],               # PCAD.UHCD.Info.Ligada

    "UHCD_BOMBAS":                              168 + 12764,                    # Leituras.PCAD_UHCD_Bombas
    "UHCD_BOMBAS01":                            [168 + 12764, 0],               # PCAD.UHCD.Bombas.[01]
    "UHCD_BOMBAS02":                            [168 + 12764, 1],               # PCAD.UHCD.Bombas.[02]

    "UHCD_RODIZIO":                             169 + 12764,                    # Leituras.PCAD_UHCD_Rodizio
    "UHCD_RODIZ_BOMBA01":                       [169 + 12764, 0],               # PCAD.UHCD.Rodizio.Bomba01
    "UHCD_RODIZ_BOMBA02":                       [169 + 12764, 1],               # PCAD.UHCD.Rodizio.Bomba02
    "UHCD_RODIZ_HABILITADO":                    [169 + 12764, 2],               # PCAD.UHCD.Rodizio.RodizioHabilitado

    "UHCD_ACUMULADOR":                          170 + 12764,                    # Leituras.PCAD_UHCD_AcumuladorBombaLider
    "UHCD_ACUM_BOMBA_LIDER":                    [170 + 12764, 0],               # PCAD.UHCD.Acumulador.BombaLider
    "UHCD_ACUM_BOMBA_RETAGUARDA":               [170 + 12764, 1],               # PCAD.UHCD.Acumulador.BombaRetaguarda

    "UHCD_FILTROS":                             172 + 12764,                    # Leituras.PCAD_UHCD_Filtros
    "UHCD_FILTRO01":                            [172 + 12764, 0],               # PCAD.UHCD.Filtros.[01]

    "UHCD_NIVEL_OLEO_INFO":                     173 + 12764,                    # Leituras.PCAD_UHCD_NivelOleo_Info
    "UHCD_NIVEL_OLEO_LL":                       [173 + 12764, 0],               # PCAD.UHCD.NivelOleo_info.LL
    "UHCD_NIVEL_OLEO_HH":                       [173 + 12764, 1],               # PCAD.UHCD.NivelOleo_info.HH

    "UHCD_TEMPERATURA_OLEO_INFO":               174 + 12764,                    # Leituras.PCAD_UHCD_TemperaturaOleo_Info
    "UHCD_TEMPE_OLEO_H":                        [174 + 12764, 0],               # PCAD.UHCD.TemperaturaOleo_Info.H
    "UHCD_TEMPE_OLEO_HH":                       [174 + 12764, 1],               # PCAD.UHCD.TemperaturaOleo_Info.HH

    "UHCD_VALVULAS":                            175 + 12764,                    # Leituras.PCAD_UHCD_Valvulas
    "UHCD_VALVULAS01":                          [175 + 12764, 0],               # PCAD.UHCD.Valvulas.[01]

    "UHCD_PRESSOSTATOS":                        176 + 12764,                    # Leituras.PCAD_UHCD_Pressostatos
    "UHCD_PRESSOSTATOS01":                      [176 + 12764, 0],               # PCAD.UHCD.Pressostatos.[01]
    "UHCD_PRESSOSTATOS02":                      [176 + 12764, 1],               # PCAD.UHCD.Pressostatos.[02]
    "UHCD_PRESSOSTATOS03":                      [176 + 12764, 2],               # PCAD.UHCD.Pressostatos.[03]

    "UHCD_TEMPERATURA_OLEO":                    177 + 12764,                    # Leituras.PCAD_UHCD_TemperaturaOleo
    "UHCD_NIVEL_OLEO":                          178 + 12764,                    # Leituras.PCAD_UHCD_NivelOleo

    "PCAD_INFO":                                179 + 12764,                    # Leituras.PCAD_Info
    "PCAD_FALTA_FASE":                          [179 + 12764, 0],               # PCAD.UHCD.PCAD_Info.FaltaFase
    "PCAD_SENS_PRESEN_ATUADO":                  [179 + 12764, 1],               # PCAD.UHCD.PCAD_Info.SensorPresencaAtuado
    "PCAD_SENS_PRESEN_INIBIDO":                 [179 + 12764, 2],               # PCAD.UHCD.PCAD_Info.SensorPresencaInibido
    "PCAD_SENS_FUMA_ATUADO":                    [179 + 12764, 3],               # PCAD.UHCD.PCAD_Info.SensorFumacaAtuado
    "PCAD_SENS_FUMA_DESCONECTADO":              [179 + 12764, 4],               # PCAD.UHCD.PCAD_Info.SensorFumacaDesconectado
    "PCAD_MODO_REMOTO":                         [179 + 12764, 5],               # PCAD.UHCD.PCAD_Info.ModoRemoto
    "PCAD_MODO_SETPOT_HAB":                     [179 + 12764, 6],               # PCAD.UHCD.PCAD_Info.ModoSetpointHabilitado


    ## ALARMES
    "Alarme28_00":                              [27 + 14089, 0],
    "Alarme28_01":                              [27 + 14089, 1],
    "Alarme28_04":                              [27 + 14089, 4],
    "Alarme28_05":                              [27 + 14089, 5],
    "Alarme28_06":                              [27 + 14089, 6],
    "Alarme28_07":                              [27 + 14089, 7],
    "Alarme28_08":                              [27 + 14089, 8],
    "Alarme28_09":                              [27 + 14089, 9],
    "Alarme28_10":                              [27 + 14089, 10],
    "Alarme28_11":                              [27 + 14089, 11],
    "Alarme28_12":                              [27 + 14089, 12],

    "Alarme29_00":                              [28 + 14089, 0],
    "Alarme29_01":                              [28 + 14089, 1],
    "Alarme29_02":                              [28 + 14089, 2],
    "Alarme29_03":                              [28 + 14089, 3],
    "Alarme29_05":                              [28 + 14089, 5],
    "Alarme29_06":                              [28 + 14089, 6],
    "Alarme29_07":                              [28 + 14089, 7],
    "Alarme29_09":                              [28 + 14089, 9],
    "Alarme29_10":                              [28 + 14089, 10],
    "Alarme29_11":                              [28 + 14089, 11],
    "Alarme29_13":                              [28 + 14089, 13],

    "Alarme30_00":                              [29 + 14089, 0],
    "Alarme30_01":                              [29 + 14089, 1],
    "Alarme30_04":                              [29 + 14089, 4],
    "Alarme30_05":                              [29 + 14089, 5],
    "Alarme30_08":                              [29 + 14089, 8],
    "Alarme30_09":                              [29 + 14089, 9],
    "Alarme30_10":                              [29 + 14089, 10],
    "Alarme30_11":                              [29 + 14089, 11],

    "Alarme31_00":                              [30 + 14089, 0],
    "Alarme31_01":                              [30 + 14089, 1],
    "Alarme31_02":                              [30 + 14089, 2],
    "Alarme31_03":                              [30 + 14089, 3],
    "Alarme31_04":                              [30 + 14089, 4],
    "Alarme31_05":                              [30 + 14089, 5],
    "Alarme31_06":                              [30 + 14089, 6],
}


REG_UG = {
    "UG1": {
        ## COMANDOS
        # Gerais
        "CMD_RESET_ALARMES":                    12288,                      # Comandos.Operacao_PCH_AdoPopinhakResetAlarmes
        "CMD_RECONHECE_ALARMES":                0 + 12289,                      # Comandos.Operacao_PCH_AdoPopinhakReconheceAlarmes

        # Operação
        "CMD_OPER_UP":                          1 + 12289,                      # Comandos.Operacao_UP
        "CMD_OPER_UPGM":                        2 + 12289,                      # Comandos.Operacao_UPGM
        "CMD_OPER_UVD":                         3 + 12289,                      # Comandos.Operacao_UVD
        "CMD_OPER_UPS":                         4 + 12289,                      # Comandos.Operacao_UPS
        "CMD_OPER_US":                          5 + 12289,                      # Comandos.Operacao_US
        "CMD_OPER_EMERGENCIA_LIGAR":            6 + 12289,                      # Comandos.Operacao_EmergenciaLigar
        "CMD_OPER_EMERGENCIA_DESLIGAR":         7 + 12289,                      # Comandos.Operacao_EmergenciaDesligar
        "CMD_OPER_PARADA_RESET":                71 + 12289,                     # Comandos.Operacao_ParadaReset

        # Turbina
        "CMD_TURB_BYPASS_ABRIR":                8 + 12289,                      # Comandos.Turb_ByPassAbrir
        "CMD_TURB_BYPASS_FECHAR":               9 + 12289,                     # Comandos.Turb_ByPassFechar
        "CMD_TURB_BORBOLETA_ABRIR":             10 + 12289,                     # Comandos.Turb_BorboletaAbrir
        "CMD_TURB_BORBOLETA_FECHAR":            11 + 12289,                     # Comandos.Turb_BorboletaFechar
        "CMD_TURB_FRENAGEM_APLICAR":            12 + 12289,                     # Comandos.Turb_FrenagemAplicar
        "CMD_TURB_FRENAGEM_DESAPLICAR":         13 + 12289,                     # Comandos.Turb_FrenagemDesaplicar
        "CMD_TURB_FRENAGEM_MANUAL":             14 + 12289,                     # Comandos.Turb_FrenagemManual
        "CMD_TURB_FRENAGEM_AUTO":               15 + 12289,                     # Comandos.Turb_FrenagemAuto
        "CMD_TURB_SENSOR_ATIVAR":               16 + 12289,                     # Comandos.Turb_SensorAtivar
        "CMD_TURB_SENSOR_DESATIVAR":            17 + 12289,                     # Comandos.Turb_SensorDesativar

        # Reg V
        "CMD_REG_V_PARTIR":                     18 + 12289,                     # Comandos.RegV_Partir
        "CMD_REG_V_PARAR":                      19 + 12289,                     # Comandos.RegV_Parar
        "CMD_REG_V_COLOCAR_CARGA":              20 + 12289,                     # Comandos.RegV_ColocarCarga
        "CMD_REG_V_RETIRAR_CARGA":              21 + 12289,                     # Comandos.RegV_RetirarCarga
        "CMD_REG_V_INCREMENTA_VELOCIDADE":      22 + 12289,                     # Comandos.RegV_IncrementaVelocidade
        "CMD_REG_V_DECREMENTA_VELOCIDADE":      23 + 12289,                     # Comandos.RegV_DecrementaVelocidade
        "CMD_REG_V_SEL_MODO_ESTATISMO":         24 + 12289,                     # Comandos.RegV_SelecionaModoEstatismo
        "CMD_REG_V_SEL_MODO_BASECARGA":         25 + 12289,                     # Comandos.RegV_SelecionaModoBaseCarga

        # Reg T
        "CMD_REG_T_LIGAR":                      26 + 12289,                     # Comandos.RegT_Ligar
        "CMD_REG_T_DESLIGAR":                   27 + 12289,                     # Comandos.RegT_Desligar
        "CMD_REG_T_INCREMENTA_TENSAO":          28 + 12289,                     # Comandos.RegT_IncrementaTensao
        "CMD_REG_T_DECREMENTA_TENSAO":          29 + 12289,                     # Comandos.RegT_DecrementaTensao
        "CMD_REG_T_PRE_EXCITACAO":              30 + 12289,                     # Comandos.RegT_PreExcitacao

        # Sinc
        "CMD_SINC_LIGAR":                       31 + 12289,                     # Comandos.Sinc_Ligar
        "CMD_SINC_DESLIGAR":                    32 + 12289,                     # Comandos.Sinc_Desligar
        "CMD_SINC_MODO_AUTO_LIGAR":             33 + 12289,                     # Comandos.Sinc_ModoAutoLigar
        "CMD_SINC_MODO_MANUAL_LIGAR":           34 + 12289,                     # Comandos.Sinc_ModoManualLigar
        "CMD_SINC_MODO_BMORTA_LIGAR":           35 + 12289,                     # Comandos.Sinc_ModoBMortaLigar

        # DJ52G
        "CMD_DJ52G_ABRIR":                      36 + 12289,                     # Comandos.Disj52G_Abrir

        # Controle Reativo
        "CMD_CTRL_REATIVO_MODO_FPLIGAR":        37 + 12289,                     # Comandos.CtrlReativo_ModoFPLigar
        "CMD_CTRL_REATIVO_MODO_FPDESLIGAR":     38 + 12289,                     # Comandos.CtrlReativo_ModoFPDesligar
        "CMD_CTRL_REATIVO_MODO_VArLIGAR":       39 + 12289,                     # Comandos.CtrlReativo_ModoVArLigar
        "CMD_CTRL_REATIVO_MODO_VArDESLIGAR":    40 + 12289,                     # Comandos.CtrlReativo_ModoVArDesligar

        # Controle Potência
        "CMD_CTRL_POT_MODO_POT_LIGAR":          41 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaLigar
        "CMD_CTRL_POT_MODO_POT_DESLIGAR":       42 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaDesligar
        "CMD_CTRL_POT_MODO_NIVEL_LIGAR":        43 + 12289,                     # Comandos.CtrlPotencia_ModoNivelLigar
        "CMD_CTRL_POT_MODO_NIVEL_DESLIGAR":     44 + 12289,                     # Comandos.CtrlPotencia_ModoNivelDesligar
        "CMD_CTRL_POT_RELI_AUTO_LIGAR":         45 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoLigar
        "CMD_CTRL_POT_RELI_AUTO_DESLIGAR":      46 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoDesligar

        # UHCT
        "CMD_UHCT_BOMBA_01_LIGAR":              47 + 12289,                     # Comandos.UHCT_Bomba01Ligar
        "CMD_UHCT_BOMBA_01_DESLIGAR":           48 + 12289,                     # Comandos.UHCT_Bomba01Desligar
        "CMD_UHCT_BOMBA_01_PRINCIPAL":          49 + 12289,                     # Comandos.UHCT_Bomba01Principal
        "CMD_UHCT_BOMBA_02_LIGAR":              50 + 12289,                     # Comandos.UHCT_Bomba02Ligar
        "CMD_UHCT_BOMBA_02_DESLIGAR":           51 + 12289,                     # Comandos.UHCT_Bomba02Desligar
        "CMD_UHCT_BOMBA_02_PRINCIPAL":          52 + 12289,                     # Comandos.UHCT_Bomba02Principal
        "CMD_UHCT_BOMBA_AGUA_LIGAR":            53 + 12289,                     # Comandos.UHCT_BombaAguaLigar
        "CMD_UHCT_BOMBA_AGUA_DESLIGAR":         54 + 12289,                     # Comandos.UHCT_BombaAguaDesligar
        "CMD_UHCT_SENSOR_ATIVAR":               55 + 12289,                     # Comandos.UHCT_SensorAtivar
        "CMD_UHCT_SENSOR_DESATIVAR":            56 + 12289,                     # Comandos.UHCT_SensorDesativar
        "CMD_UHCT_RODIZIO_HABILITAR":           57 + 12289,                     # Comandos.UHCT_RodizioHabilitar
        "CMD_UHCT_RODIZIO_DESABILITAR":         58 + 12289,                     # Comandos.UHCT_RodizioDesabilitar

        # UHLM
        "CMD_UHLM_BOMBA_01_LIGAR":              59 + 12289,                     # Comandos.UHLM_Bomba01Ligar
        "CMD_UHLM_BOMBA_01_DESLIGAR":           60 + 12289,                     # Comandos.UHLM_Bomba01Desligar
        "CMD_UHLM_BOMBA_01_PRINCIPAL":          61 + 12289,                     # Comandos.UHLM_Bomba01Principal
        "CMD_UHLM_BOMBA_02_LIGAR":              62 + 12289,                     # Comandos.UHLM_Bomba02Ligar
        "CMD_UHLM_BOMBA_02_DESLIGAR":           63 + 12289,                     # Comandos.UHLM_Bomba02Desligar
        "CMD_UHLM_BOMBA_02_PRINCIPAL":          64 + 12289,                     # Comandos.UHLM_Bomba02Principal
        "CMD_UHLM_BOMBA_JACKING_LIGA":          65 + 12289,                     # Comandos.UHLM_BombaJackingLiga
        "CMD_UHLM_BOMBA_JACKING_DESLIGA":       66 + 12289,                     # Comandos.UHLM_BombaJackingDesliga
        "CMD_UHLM_BOMBA_AGUA_LIGA":             67 + 12289,                     # Comandos.UHLM_BombaAguaLiga
        "CMD_UHLM_BOMBA_AGUA_DESLIGA":          68 + 12289,                     # Comandos.UHLM_BombaAguaDesliga
        "CMD_UHLM_RODIZIO_HABILITAR":           69 + 12289,                     # Comandos.UHLM_RodizioHabilitar
        "CMD_UHLM_RODIZIO_DESABILITAR":         70 + 12289,                     # Comandos.UHLM_RodizioDesabilitar

        # RT
        "CMD_RT_MTVC_HABILITAR":                71 + 12289,                     # Comandos.RT_MTVC_Habilitar
        "CMD_RT_MECC_HABILITAR":                72 + 12289,                     # Comandos.RT_MECC_Habilitar
        "CMD_RT_ONLINE_HABILITAR":              73 + 12289,                     # Comandos.RT_Online_habilitar
        "CMD_RT_ONLINE_DESABILITAR":            74 + 12289,                     # Comandos.RT_Online_Desabiltar
        "CMD_RT_PARALELO_HABILITAR":            75 + 12289,                     # Comandos.RT_Paralelo_habilitar
        "CMD_RT_PARALELO_DESABILITAR":          76 + 12289,                     # Comandos.RT_Paralelo_Desabilitar

        # RV
        "CMD_RV_CONJUGADO_AUTO_HABILITAR":      77 + 12289,                     # Comandos.RV_ConjugadoAuto_habilitar
        "CMD_RV_CONJUGADO_MANUAL_HABILITAR":    78 + 12289,                     # Comandos.RV_ConjugadoManual_habilitar
        "CMD_RV_CONJUGADO_01_HABILITAR":        79 + 12289,                     # Comandos.RV_Conjugado01_habilitar
        "CMD_RV_CONJUGADO_02_HABILITAR":        80 + 12289,                     # Comandos.RV_Conjugado02_habilitar
        "CMD_RV_CONJUGADO_03_HABILITAR":        81 + 12289,                     # Comandos.RV_Conjugado03_habilitar
        "CMD_RV_CONJUGADO_04_HABILITAR":        82 + 12289,                     # Comandos.RV_Conjugado04_habilitar
        "CMD_RV_CONJUGADO_05_HABILITAR":        83 + 12289,                     # Comandos.RV_Conjugado05_habilitar


        ## SETPOINTS

        # UHCT
        "UHCT_PRESSAO_MAX":                     0 + 13569,                      # Setpoints.UHCT_PressaoMaxima
        "UHCT_PRESSAO_MIN":                     0 + 13569,                      # Setpoints.UHCT_PressaoMinima
        "UHCT_PRESSAO_DESLIGAMENTO":            1 + 13569,                      # Setpoints.UHCT_PressaoDesligamento
        "UHCT_PRESSAO_CRITICA":                 2 + 13569,                      # Setpoints.UHCT_PressaoCritica

        # Controle Potência
        "CRTL_POT_NIVEL_LL1":                   3 + 13569,                      # Setpoints.CtrlPotencia_NivelLL1
        "CRTL_POT_NIVEL_LL2":                   4 + 13569,                      # Setpoints.CtrlPotencia_NivelLL2
        "CRTL_POT_NIVEL_LL3":                   5 + 13569,                      # Setpoints.CtrlPotencia_NivelLL3
        "CRTL_POT_NIVEL_LL4":                   6 + 13569,                      # Setpoints.CtrlPotencia_NivelLL4
        "CRTL_POT_NIVEL_LL5":                   7 + 13569,                      # Setpoints.CtrlPotencia_NivelLL5
        "CRTL_POT_POT_1":                       8 + 13569,                      # Setpoints.CtrlPotencia_Potencia1
        "CRTL_POT_POT_2":                       9 + 13569,                     # Setpoints.CtrlPotencia_Potencia2
        "CRTL_POT_POT_3":                       10 + 13569,                     # Setpoints.CtrlPotencia_Potencia3
        "CRTL_POT_POT_4":                       11 + 13569,                     # Setpoints.CtrlPotencia_Potencia4
        "CRTL_POT_POT_5":                       12 + 13569,                     # Setpoints.CtrlPotencia_Potencia5
        "CRTL_POT_POT_MIN":                     13 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinima
        "CRTL_POT_POT_MIN_TEMPO":               14 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinimaTempo
        "CRTL_POT_NIVEL_RELIGAMENTO":           15 + 13569,                     # Setpoints.CtrlPotencia_NivelReligamento
        "CRTL_POT_ALVO":                        16 + 13569,                     # Setpoints.CtrlPotencia_Alvo
        "CRTL_POT_TOLERANCIA":                  17 + 13569,                     # Setpoints.CtrlPotencia_Tolerancia
        "CRTL_POT_PULSO_TEMPO":                 18 + 13569,                     # Setpoints.CtrlPotencia_PulsoTempo
        "CRTL_POT_PULSO_INTERVALO":             19 + 13569,                     # Setpoints.CtrlPotencia_PulsoIntervalo
        "CRTL_POT_SP_NIVEL":                    20 + 13569,                     # Setpoints.CtrlPotencia_SetpointNivel
        "CRTL_POT_NIVEL_MIN_ALARME":            21 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoAlarme
        "CRTL_POT_NIVEL_MIN_TRIP":              22 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoTRIP
        "CTRL_POT_POT_MAX":                     88 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMaxima

        # Controle Reativo
        "CRTL_REATIVO_SP_FP":                   23 + 13569,                     # Setpoints.CtrlReativo_SetpointFP
        "CRTL_REATIVO_SP_REATIVO":              24 + 13569,                     # Setpoints.CtrlReativo_SetpointReativo

        # Turbina
        "TURB_VIBRA_01_ALARME":                 25 + 13569,                     # Setpoints.Turb_Vibracao01Alarme
        "TURB_VIBRA_01_TRIP":                   26 + 13569,                     # Setpoints.Turb_Vibracao01TRIP
        "TURB_VIBRA_02_ALARME":                 27 + 13569,                     # Setpoints.Turb_Vibracao02Alarme
        "TURB_VIBRA_02_TRIP":                   28 + 13569,                     # Setpoints.Turb_Vibracao02TRIP
        "TURB_VIBRA_03_ALARME":                 29 + 13569,                     # Setpoints.Turb_Vibracao03Alarme
        "TURB_VIBRA_03_TRIP":                   30 + 13569,                     # Setpoints.Turb_Vibracao03TRIP
        "TURB_VIBRA_04_ALARME":                 31 + 13569,                     # Setpoints.Turb_Vibracao04Alarme
        "TURB_VIBRA_04_TRIP":                   32 + 13569,                     # Setpoints.Turb_Vibracao04TRIP
        "TURB_TEMPO_EQUALI_SP":                 33 + 13569,                     # Setpoints.Turb_TempoEqualizacaoSetpoint
        "TURB_VIBRA_05_ALARME":                 89 + 13569,                     # Setpoints.Turb_Vibracao05Alarme
        "TURB_VIBRA_05_TRIP":                   90 + 13569,                     # Setpoints.Turb_Vibracao05TRIP

        # Freio
        "FREIO_PULSO_INTERVALO":                34 + 13569,                     # Setpoints.Freio_PulsoIntervalo
        "FREIO_PULSO_TEMPO":                    35 + 13569,                     # Setpoints.Freio_PulsoTempo

        # UHCT
        "UHCT_RODIZIO_PRINCIPAL":               36 + 13569,                     # Setpoints.UHCT_RodizioPrincipal
        "UHCT_RODIZIO_RETAGUARDA":              37 + 13569,                     # Setpoints.UHCT_RodizioRetaguarda

        # UHLM
        "UHLM_RODIZIO_PRINCIPAL":               38 + 13569,                     # Setpoints.UHLM_RodizioPrincipal
        "UHLM_RODIZIO_RETAGUARDA":              39 + 13569,                     # Setpoints.UHLM_RodizioRetaguarda
        "UHLM_SP_VAZAO_01":                     91 + 13569,                     # Setpoints.UHLM_SetpointVazao01
        "UHLM_SP_VAZAO_02":                     92 + 13569,                     # Setpoints.UHLM_SetpointVazao02
        "UHLM_SP_VAZAO_03":                     93 + 13569,                     # Setpoints.UHLM_SetpointVazao03
        "UHLM_SP_VAZAO_04":                     94 + 13569,                     # Setpoints.UHLM_SetpointVazao04

        # Temperaturas
        "TEMPERATURA_01_ALARME":                40 + 13569,                     # Setpoints.Temperatura01_Alarme
        "TEMPERATURA_02_ALARME":                41 + 13569,                     # Setpoints.Temperatura02_Alarme
        "TEMPERATURA_03_ALARME":                42 + 13569,                     # Setpoints.Temperatura03_Alarme
        "TEMPERATURA_04_ALARME":                43 + 13569,                     # Setpoints.Temperatura04_Alarme
        "TEMPERATURA_05_ALARME":                44 + 13569,                     # Setpoints.Temperatura05_Alarme
        "TEMPERATURA_06_ALARME":                45 + 13569,                     # Setpoints.Temperatura06_Alarme
        "TEMPERATURA_07_ALARME":                46 + 13569,                     # Setpoints.Temperatura07_Alarme
        "TEMPERATURA_08_ALARME":                47 + 13569,                     # Setpoints.Temperatura08_Alarme
        "TEMPERATURA_09_ALARME":                48 + 13569,                     # Setpoints.Temperatura09_Alarme
        "TEMPERATURA_10_ALARME":                49 + 13569,                     # Setpoints.Temperatura10_Alarme
        "TEMPERATURA_11_ALARME":                50 + 13569,                     # Setpoints.Temperatura11_Alarme
        "TEMPERATURA_12_ALARME":                51 + 13569,                     # Setpoints.Temperatura12_Alarme
        "TEMPERATURA_13_ALARME":                52 + 13569,                     # Setpoints.Temperatura13_Alarme
        "TEMPERATURA_14_ALARME":                53 + 13569,                     # Setpoints.Temperatura14_Alarme
        "TEMPERATURA_15_ALARME":                54 + 13569,                     # Setpoints.Temperatura15_Alarme
        "TEMPERATURA_16_ALARME":                55 + 13569,                     # Setpoints.Temperatura16_Alarme
        "TEMPERATURA_01_TRIP01":                56 + 13569,                     # Setpoints.Temperatura01_TRIP01
        "TEMPERATURA_02_TRIP01":                57 + 13569,                     # Setpoints.Temperatura02_TRIP01
        "TEMPERATURA_03_TRIP01":                58 + 13569,                     # Setpoints.Temperatura03_TRIP01
        "TEMPERATURA_04_TRIP01":                59 + 13569,                     # Setpoints.Temperatura04_TRIP01
        "TEMPERATURA_05_TRIP01":                60 + 13569,                     # Setpoints.Temperatura05_TRIP01
        "TEMPERATURA_06_TRIP01":                61 + 13569,                     # Setpoints.Temperatura06_TRIP01
        "TEMPERATURA_07_TRIP01":                62 + 13569,                     # Setpoints.Temperatura07_TRIP01
        "TEMPERATURA_08_TRIP01":                63 + 13569,                     # Setpoints.Temperatura08_TRIP01
        "TEMPERATURA_09_TRIP01":                64 + 13569,                     # Setpoints.Temperatura09_TRIP01
        "TEMPERATURA_10_TRIP01":                65 + 13569,                     # Setpoints.Temperatura10_TRIP01
        "TEMPERATURA_11_TRIP01":                66 + 13569,                     # Setpoints.Temperatura11_TRIP01
        "TEMPERATURA_12_TRIP01":                67 + 13569,                     # Setpoints.Temperatura12_TRIP01
        "TEMPERATURA_13_TRIP01":                68 + 13569,                     # Setpoints.Temperatura13_TRIP01
        "TEMPERATURA_14_TRIP01":                69 + 13569,                     # Setpoints.Temperatura14_TRIP01
        "TEMPERATURA_15_TRIP01":                70 + 13569,                     # Setpoints.Temperatura15_TRIP01
        "TEMPERATURA_16_TRIP01":                71 + 13569,                     # Setpoints.Temperatura16_TRIP01
        "TEMPERATURA_01_TRIP02":                72 + 13569,                     # Setpoints.Temperatura01_TRIP02
        "TEMPERATURA_02_TRIP02":                73 + 13569,                     # Setpoints.Temperatura02_TRIP02
        "TEMPERATURA_03_TRIP02":                74 + 13569,                     # Setpoints.Temperatura03_TRIP02
        "TEMPERATURA_04_TRIP02":                75 + 13569,                     # Setpoints.Temperatura04_TRIP02
        "TEMPERATURA_05_TRIP02":                76 + 13569,                     # Setpoints.Temperatura05_TRIP02
        "TEMPERATURA_06_TRIP02":                77 + 13569,                     # Setpoints.Temperatura06_TRIP02
        "TEMPERATURA_07_TRIP02":                78 + 13569,                     # Setpoints.Temperatura07_TRIP02
        "TEMPERATURA_08_TRIP02":                79 + 13569,                     # Setpoints.Temperatura08_TRIP02
        "TEMPERATURA_09_TRIP02":                80 + 13569,                     # Setpoints.Temperatura09_TRIP02
        "TEMPERATURA_10_TRIP02":                81 + 13569,                     # Setpoints.Temperatura10_TRIP02
        "TEMPERATURA_11_TRIP02":                82 + 13569,                     # Setpoints.Temperatura11_TRIP02
        "TEMPERATURA_12_TRIP02":                83 + 13569,                     # Setpoints.Temperatura12_TRIP02
        "TEMPERATURA_13_TRIP02":                84 + 13569,                     # Setpoints.Temperatura13_TRIP02
        "TEMPERATURA_14_TRIP02":                85 + 13569,                     # Setpoints.Temperatura14_TRIP02
        "TEMPERATURA_15_TRIP02":                86 + 13569,                     # Setpoints.Temperatura15_TRIP02
        "TEMPERATURA_16_TRIP02":                87 + 13569,                     # Setpoints.Temperatura16_TRIP02

        # Grade Suja
        "GradeSuja_TRIP":                       95 + 13569,                     # Setpoints.GradeSuja_TRIP

        # Curva
        "CURVA_01_DISTRIB_P1":                  96 + 13569,                     # Setpoints.Curva01_DistribuidorP1
        "CURVA_01_DISTRIB_P2":                  97 + 13569,                     # Setpoints.Curva01_DistribuidorP2
        "CURVA_01_DISTRIB_P3":                  98 + 13569,                     # Setpoints.Curva01_DistribuidorP3
        "CURVA_01_DISTRIB_P4":                  99 + 13569,                    # Setpoints.Curva01_DistribuidorP4
        "CURVA_01_DISTRIB_P5":                  100 + 13569,                    # Setpoints.Curva01_DistribuidorP5
        "CURVA_01_DISTRIB_P6":                  101 + 13569,                    # Setpoints.Curva01_DistribuidorP6
        "CURVA_01_DISTRIB_P7":                  102 + 13569,                    # Setpoints.Curva01_DistribuidorP7
        "CURVA_01_DISTRIB_P8":                  103 + 13569,                    # Setpoints.Curva01_DistribuidorP8
        "CURVA_01_DISTRIB_P9":                  104 + 13569,                    # Setpoints.Curva01_DistribuidorP9
        "CURVA_01_DISTRIB_P10":                 105 + 13569,                    # Setpoints.Curva01_DistribuidorP10
        "CURVA_01_ROTOR_P1":                    106 + 13569,                    # Setpoints.Curva01_RotorP1
        "CURVA_01_ROTOR_P2":                    107 + 13569,                    # Setpoints.Curva01_RotorP2
        "CURVA_01_ROTOR_P3":                    108 + 13569,                    # Setpoints.Curva01_RotorP3
        "CURVA_01_ROTOR_P4":                    109 + 13569,                    # Setpoints.Curva01_RotorP4
        "CURVA_01_ROTOR_P5":                    110 + 13569,                    # Setpoints.Curva01_RotorP5
        "CURVA_01_ROTOR_P6":                    111 + 13569,                    # Setpoints.Curva01_RotorP6
        "CURVA_01_ROTOR_P7":                    112 + 13569,                    # Setpoints.Curva01_RotorP7
        "CURVA_01_ROTOR_P8":                    113 + 13569,                    # Setpoints.Curva01_RotorP8
        "CURVA_01_ROTOR_P9":                    114 + 13569,                    # Setpoints.Curva01_RotorP9
        "CURVA_01_ROTOR_P10":                   115 + 13569,                    # Setpoints.Curva01_RotorP10
        "CURVA_02_DISTRIB_P1":                  116 + 13569,                    # Setpoints.Curva02_DistribuidorP1
        "CURVA_02_DISTRIB_P2":                  117 + 13569,                    # Setpoints.Curva02_DistribuidorP2
        "CURVA_02_DISTRIB_P3":                  118 + 13569,                    # Setpoints.Curva02_DistribuidorP3
        "CURVA_02_DISTRIB_P4":                  119 + 13569,                    # Setpoints.Curva02_DistribuidorP4
        "CURVA_02_DISTRIB_P5":                  120 + 13569,                    # Setpoints.Curva02_DistribuidorP5
        "CURVA_02_DISTRIB_P6":                  121 + 13569,                    # Setpoints.Curva02_DistribuidorP6
        "CURVA_02_DISTRIB_P7":                  122 + 13569,                    # Setpoints.Curva02_DistribuidorP7
        "CURVA_02_DISTRIB_P8":                  123 + 13569,                    # Setpoints.Curva02_DistribuidorP8
        "CURVA_02_DISTRIB_P9":                  124 + 13569,                    # Setpoints.Curva02_DistribuidorP9
        "CURVA_02_DISTRIB_P10":                 125 + 13569,                    # Setpoints.Curva02_DistribuidorP10
        "CURVA_02_ROTOR_P1":                    126 + 13569,                    # Setpoints.Curva02_RotorP1
        "CURVA_02_ROTOR_P2":                    127 + 13569,                    # Setpoints.Curva02_RotorP2
        "CURVA_02_ROTOR_P3":                    128 + 13569,                    # Setpoints.Curva02_RotorP3
        "CURVA_02_ROTOR_P4":                    129 + 13569,                    # Setpoints.Curva02_RotorP4
        "CURVA_02_ROTOR_P5":                    130 + 13569,                    # Setpoints.Curva02_RotorP5
        "CURVA_02_ROTOR_P6":                    131 + 13569,                    # Setpoints.Curva02_RotorP6
        "CURVA_02_ROTOR_P7":                    132 + 13569,                    # Setpoints.Curva02_RotorP7
        "CURVA_02_ROTOR_P8":                    133 + 13569,                    # Setpoints.Curva02_RotorP8
        "CURVA_02_ROTOR_P9":                    134 + 13569,                    # Setpoints.Curva02_RotorP9
        "CURVA_02_ROTOR_P10":                   135 + 13569,                    # Setpoints.Curva02_RotorP10
        "CURVA_03_DISTRIB_P1":                  136 + 13569,                    # Setpoints.Curva03_DistribuidorP1
        "CURVA_03_DISTRIB_P2":                  137 + 13569,                    # Setpoints.Curva03_DistribuidorP2
        "CURVA_03_DISTRIB_P3":                  138 + 13569,                    # Setpoints.Curva03_DistribuidorP3
        "CURVA_03_DISTRIB_P4":                  139 + 13569,                    # Setpoints.Curva03_DistribuidorP4
        "CURVA_03_DISTRIB_P5":                  140 + 13569,                    # Setpoints.Curva03_DistribuidorP5
        "CURVA_03_DISTRIB_P6":                  141 + 13569,                    # Setpoints.Curva03_DistribuidorP6
        "CURVA_03_DISTRIB_P7":                  142 + 13569,                    # Setpoints.Curva03_DistribuidorP7
        "CURVA_03_DISTRIB_P8":                  143 + 13569,                    # Setpoints.Curva03_DistribuidorP8
        "CURVA_03_DISTRIB_P9":                  144 + 13569,                    # Setpoints.Curva03_DistribuidorP9
        "CURVA_03_DISTRIB_P10":                 145 + 13569,                    # Setpoints.Curva03_DistribuidorP10
        "CURVA_03_ROTOR_P1":                    146 + 13569,                    # Setpoints.Curva03_RotorP1
        "CURVA_03_ROTOR_P2":                    147 + 13569,                    # Setpoints.Curva03_RotorP2
        "CURVA_03_ROTOR_P3":                    148 + 13569,                    # Setpoints.Curva03_RotorP3
        "CURVA_03_ROTOR_P4":                    149 + 13569,                    # Setpoints.Curva03_RotorP4
        "CURVA_03_ROTOR_P5":                    150 + 13569,                    # Setpoints.Curva03_RotorP5
        "CURVA_03_ROTOR_P6":                    151 + 13569,                    # Setpoints.Curva03_RotorP6
        "CURVA_03_ROTOR_P7":                    152 + 13569,                    # Setpoints.Curva03_RotorP7
        "CURVA_03_ROTOR_P8":                    153 + 13569,                    # Setpoints.Curva03_RotorP8
        "CURVA_03_ROTOR_P9":                    154 + 13569,                    # Setpoints.Curva03_RotorP9
        "CURVA_03_ROTOR_P10":                   155 + 13569,                    # Setpoints.Curva03_RotorP10
        "CURVA_04_DISTRIB_P1":                  156 + 13569,                    # Setpoints.Curva04_DistribuidorP1
        "CURVA_04_DISTRIB_P2":                  157 + 13569,                    # Setpoints.Curva04_DistribuidorP2
        "CURVA_04_DISTRIB_P3":                  158 + 13569,                    # Setpoints.Curva04_DistribuidorP3
        "CURVA_04_DISTRIB_P4":                  159 + 13569,                    # Setpoints.Curva04_DistribuidorP4
        "CURVA_04_DISTRIB_P5":                  160 + 13569,                    # Setpoints.Curva04_DistribuidorP5
        "CURVA_04_DISTRIB_P6":                  161 + 13569,                    # Setpoints.Curva04_DistribuidorP6
        "CURVA_04_DISTRIB_P7":                  162 + 13569,                    # Setpoints.Curva04_DistribuidorP7
        "CURVA_04_DISTRIB_P8":                  163 + 13569,                    # Setpoints.Curva04_DistribuidorP8
        "CURVA_04_DISTRIB_P9":                  164 + 13569,                    # Setpoints.Curva04_DistribuidorP9
        "CURVA_04_DISTRIB_P10":                 165 + 13569,                    # Setpoints.Curva04_DistribuidorP10
        "CURVA_04_ROTOR_P1":                    166 + 13569,                    # Setpoints.Curva04_RotorP1
        "CURVA_04_ROTOR_P2":                    167 + 13569,                    # Setpoints.Curva04_RotorP2
        "CURVA_04_ROTOR_P3":                    168 + 13569,                    # Setpoints.Curva04_RotorP3
        "CURVA_04_ROTOR_P4":                    169 + 13569,                    # Setpoints.Curva04_RotorP4
        "CURVA_04_ROTOR_P5":                    170 + 13569,                    # Setpoints.Curva04_RotorP5
        "CURVA_04_ROTOR_P6":                    171 + 13569,                    # Setpoints.Curva04_RotorP6
        "CURVA_04_ROTOR_P7":                    172 + 13569,                    # Setpoints.Curva04_RotorP7
        "CURVA_04_ROTOR_P8":                    173 + 13569,                    # Setpoints.Curva04_RotorP8
        "CURVA_04_ROTOR_P9":                    174 + 13569,                    # Setpoints.Curva04_RotorP9
        "CURVA_04_ROTOR_P10":                   175 + 13569,                    # Setpoints.Curva04_RotorP10
        "CURVA_05_DISTRIB_P1":                  176 + 13569,                    # Setpoints.Curva05_DistribuidorP1
        "CURVA_05_DISTRIB_P2":                  177 + 13569,                    # Setpoints.Curva05_DistribuidorP2
        "CURVA_05_DISTRIB_P3":                  178 + 13569,                    # Setpoints.Curva05_DistribuidorP3
        "CURVA_05_DISTRIB_P4":                  179 + 13569,                    # Setpoints.Curva05_DistribuidorP4
        "CURVA_05_DISTRIB_P5":                  180 + 13569,                    # Setpoints.Curva05_DistribuidorP5
        "CURVA_05_DISTRIB_P6":                  181 + 13569,                    # Setpoints.Curva05_DistribuidorP6
        "CURVA_05_DISTRIB_P7":                  182 + 13569,                    # Setpoints.Curva05_DistribuidorP7
        "CURVA_05_DISTRIB_P8":                  183 + 13569,                    # Setpoints.Curva05_DistribuidorP8
        "CURVA_05_DISTRIB_P9":                  184 + 13569,                    # Setpoints.Curva05_DistribuidorP9
        "CURVA_05_DISTRIB_P10":                 185 + 13569,                    # Setpoints.Curva05_DistribuidorP10
        "CURVA_05_ROTOR_P1":                    186 + 13569,                    # Setpoints.Curva05_RotorP1
        "CURVA_05_ROTOR_P2":                    187 + 13569,                    # Setpoints.Curva05_RotorP2
        "CURVA_05_ROTOR_P3":                    188 + 13569,                    # Setpoints.Curva05_RotorP3
        "CURVA_05_ROTOR_P4":                    189 + 13569,                    # Setpoints.Curva05_RotorP4
        "CURVA_05_ROTOR_P5":                    190 + 13569,                    # Setpoints.Curva05_RotorP5
        "CURVA_05_ROTOR_P6":                    191 + 13569,                    # Setpoints.Curva05_RotorP6
        "CURVA_05_ROTOR_P7":                    192 + 13569,                    # Setpoints.Curva05_RotorP7
        "CURVA_05_ROTOR_P8":                    193 + 13569,                    # Setpoints.Curva05_RotorP8
        "CURVA_05_ROTOR_P9":                    194 + 13569,                    # Setpoints.Curva05_RotorP9
        "CURVA_05_ROTOR_P10":                   195 + 13569,                    # Setpoints.Curva05_RotorP10

        # Referencia Curva
        "REFER_CURVA_01":                       196 + 13569,                    # Setpoints.ReferenciaCurva01
        "REFER_CURVA_02":                       197 + 13569,                    # Setpoints.ReferenciaCurva02
        "REFER_CURVA_03":                       198 + 13569,                    # Setpoints.ReferenciaCurva03
        "REFER_CURVA_04":                       199 + 13569,                    # Setpoints.ReferenciaCurva04
        "REFER_CURVA_05":                       200 + 13569,                    # Setpoints.ReferenciaCurva05

        # Outros
        "TEMPO_ATUALIZACAO":                    201 + 13569,                    # Setpoints.TempoAtualizacao
        "MODO_OPERACAO_RETENTIVO":              202 + 13569,                    # Setpoints.ModoOperacao_Retentivo
        "CURVA_SEL_RETENTIVO":                  203 + 13569,                    # Setpoints.CurvaSelecionada_Retentivo


        ## LEITURAS

        # Nível
        "NV_JUSANTE":                           1 + 12764,                      # Leituras.NivelJusante
        "NV_BARRAGEM":                          2 + 12764,                      # Leituras.NivelBarragem
        "NV_CANAL":                             3 + 12764,                      # Leituras.NivelCanal
        "NV_CAMARA_CARGA":                      4 + 12764,                      # Leituras.NivelCamaraCarga
        "QUEDA_BRUTA":                          130 + 12764,                    # Leituras.QuedaBruta

        # Operação
        "OPER_PAINEL_RESET_ALARMES":            [5 + 12764, 0],                 # Leituras.Operacao_PainelResetAlarmes
        "OPER_PAINEL_RECONHECE_ALARMES":        [6 + 12764, 1],                 # Leituras.Operacao_PainelReconheceAlarmes

        "OPER_INFO":                            8 + 12764,                      # Leituras.Operacao_Info
        "OPER_EMERGENCIA":                      [8 + 12764, 0],                 # Operacao.Info.Emergencia
        "OPER_SIRENE_LIGADA":                   [8 + 12764, 1],                 # Operacao.Info.SireneLigada
        "OPER_MODO_REMOTO":                     [8 + 12764, 2],                 # Operacao.Info.OperacaoModoRemoto
        "OPER_MODO_LOCAL":                      [8 + 12764, 3],                 # Operacao.Info.OperacaoModoLocal

        "OPER_ETAPA_ALVO":                      9 + 12764,                      # Leituras.Operacao_EtapaAlvo
        "OPER_ETAPA_ALVO_UP":                   [9 + 12764, 0],                 # Operacao.EtapaAlvo.UP
        "OPER_ETAPA_ALVO_UPGM":                 [9 + 12764, 1],                 # Operacao.EtapaAlvo.UPGM
        "OPER_ETAPA_ALVO_UMD":                  [9 + 12764, 2],                 # Operacao.EtapaAlvo.UMD
        "OPER_ETAPA_ALVO_UPS":                  [9 + 12764, 3],                 # Operacao.EtapaAlvo.UPS
        "OPER_ETAPA_ALVO_US":                   [9 + 12764, 4],                 # Operacao.EtapaAlvo.US

        "OPER_ETAPA_ATUAL":                     10 + 12764,                     # Leituras.Operacao_EtapaAtual
        "OPER_ETAPA_ATUAL_UP":                  [10 + 12764, 0],                # Operacao.EtapaAtual.UP
        "OPER_ETAPA_ATUAL_UPGM":                [10 + 12764, 1],                # Operacao.EtapaAtual.UPGM
        "OPER_ETAPA_ATUAL_UMD":                 [10 + 12764, 2],                # Operacao.EtapaAtual.UMD
        "OPER_ETAPA_ATUAL_UPS":                 [10 + 12764, 3],                # Operacao.EtapaAtual.UPS
        "OPER_ETAPA_ATUAL_US":                  [10 + 12764, 4],                # Operacao.EtapaAtual.US

        "OPER_ETAPA_TRANSICAO":                 11 + 12764,                     # Leituras.Operacao_EtapaTransicao
        "OPER_ETAPA_TRANS_UP_UPGM":             [11 + 12764, 0],                # Operacao.EtapaTransicao.UPtoUPGM
        "OPER_ETAPA_TRANS_UPGM_UMD":            [11 + 12764, 1],                # Operacao.EtapaTransicao.UPGMtoUMD
        "OPER_ETAPA_TRANS_UMD_UPS":             [11 + 12764, 2],                # Operacao.EtapaTransicao.UMDtoUPS
        "OPER_ETAPA_TRANS_UPS_US":              [11 + 12764, 3],                # Operacao.EtapaTransicao.UPStoUS
        "OPER_ETAPA_TRANS_US_UPS":              [11 + 12764, 4],                # Operacao.EtapaTransicao.UStoUPS
        "OPER_ETAPA_TRANS_UPS_UMD":             [11 + 12764, 5],                # Operacao.EtapaTransicao.UPStoUMD
        "OPER_ETAPA_TRANS_UMD_UPGM":            [11 + 12764, 6],                # Operacao.EtapaTransicao.UMDtoUPGM
        "OPER_ETAPA_TRANS_UPGM_UP":             [11 + 12764, 7],                # Operacao.EtapaTransicao.UPGMtoUP

        "OPER_INFO_PARADA":                     11 + 12764,                     # Leituras.Operacao_InfoParada
        "OPER_INFO_PARADA_NORMAL":              [11 + 12764, 0],                # Operacao.InfoParada.Normal
        "OPER_INFO_PARADA_EMERG":               [11 + 12764, 1],                # Operacao.InfoParada.Emergencia
        "OPER_INFO_PARADA_TRIP_AGUA":           [11 + 12764, 2],                # Operacao.InfoParada.TRIPAgua
        "OPER_INFO_PARADA_TRIP_M":              [11 + 12764, 3],                # Operacao.InfoParada.TRIPMecanico
        "OPER_INFO_PARADA_TRIP_E":              [11 + 12764, 4],                # Operacao.InfoParada.TRIPEletrico
        "OPER_INFO_PARADA_TRIP_H":              [11 + 12764, 5],                # Operacao.InfoParada.TRIPHidraulico
        "OPER_INFO_PARADA_RELIG_AUTO":          [11 + 12764, 6],                # Operacao.InfoParada.ReligamentoAutomatico
        "OPER_INFO_PARADA_PARTIDA_MANU":        [11 + 12764, 7],                # Operacao.InfoParada.PartidaManual
        "OPER_INFO_PARADA_INFO_INVAL":          [11 + 12764, 15],               # Operacao.InfoParada.ParadaInfoValida

        # UHCT
        "UHCT_INFO":                            12 + 12764,                     # Leituras.UHCT_Info
        "UHCT_OPERACIONAL":                     [12 + 12764, 0],                # UHCT.Info.Operacional
        "UHCT_LIGADA":                          [12 + 12764, 1],                # UHCT.Info.Ligada
        "UHCT_SENS_DESATIVADO":                 [12 + 12764, 2],                # UHCT.Info.SensorDesativado
        "UHCT_MODO_LOCAL":                      [12 + 12764, 3],                # UHCT.Info.ModoLocal

        "UHCT_BOMBAS":                          13 + 12764,                     # Leituras.UHCT_Bombas
        "UHCT_BOMBAS01":                        [13 + 12764, 0],                # UHCT.Bombas.Bomba01
        "UHCT_BOMBAS02":                        [13 + 12764, 1],                # UHCT.Bombas.Bomba02
        "UHCT_BOMBAS03":                        [13 + 12764, 2],                # UHCT.Bombas.Bomba03

        "UHCT_RODIZIO":                         14 + 12764,                     # Leituras.UHCT_Rodizio
        "UHCT_RODIZ_HABILITADO":                [14 + 12764, 0],                # UHCT.Rodizio.RodizioHabilitado
        "UHCT_RODIZ_BOMBA01":                   [14 + 12764, 1],                # UHCT.Rodizio.Bomba01
        "UHCT_RODIZ_BOMBA02":                   [14 + 12764, 2],                # UHCT.Rodizio.Bomba02

        "UHCT_VALVULAS":                        15 + 12764,                     # Leituras.UHCT_Valvulas
        "UHCT_VALVULAS01":                      [15 + 12764, 0],                # UHCT.Valvulas.Valvulas01
        "UHCT_VALVULAS02":                      [15 + 12764, 1],                # UHCT.Valvulas.Valvulas02
        "UHCT_VALVULAS03":                      [15 + 12764, 2],                # UHCT.Valvulas.Valvulas03
        "UHCT_VALVULAS04":                      [15 + 12764, 3],                # UHCT.Valvulas.Valvulas04

        "UHCT_FILTROS":                         16 + 12764,                     # Leituras.UHCT_Filtros
        "UHCT_FILTROS01":                       [16 + 12764, 0],                # UHCT.Filtros.Filtro01
        "UHCT_FILTROS02":                       [16 + 12764, 1],                # UHCT.Filtros.Filtro02
        "UHCT_FILTROS03":                       [16 + 12764, 2],                # UHCT.Filtros.Filtro03
        "UHCT_FILTROS04":                       [16 + 12764, 3],                # UHCT.Filtros.Filtro04
        "UHCT_FILTROS05":                       [16 + 12764, 4],                # UHCT.Filtros.Filtro05

        "UHCT_PRESSOSTATOS":                    17 + 12764,                     # Leituras.UHCT_Pressostatos
        "UHCT_PRESSOSTATO01":                   [17 + 12764, 0],                # UHCT.Pressostatos.Pressostato01
        "UHCT_PRESSOSTATO02":                   [17 + 12764, 1],                # UHCT.Pressostatos.Pressostato02
        "UHCT_PRESSOSTATO03":                   [17 + 12764, 2],                # UHCT.Pressostatos.Pressostato03

        "UHCT_NIVEL_OLEO":                      18 + 12764,                     # Leituras.UHCT_NivelOleo
        "UHCT_NIVEL_OLEO_LL":                   [18 + 12764, 0],                # UHCT.NivelOleo.LL
        "UHCT_NIVEL_OLEO_L":                    [18 + 12764, 1],                # UHCT.NivelOleo.L
        "UHCT_NIVEL_OLEO_H":                    [18 + 12764, 2],                # UHCT.NivelOleo.H
        "UHCT_NIVEL_OLEO_HH":                   [18 + 12764, 3],                # UHCT.NivelOleo.HH

        "UHCT_PRESSAO_OLEO":                    19 + 12764,                     # Leituras.UHCT_PressaoOleo
        "UHCT_ACUM_RODIZIO_PRINCIPAL":          20 + 12764,                     # Leituras.UHCT_AcumuladorRodizioPrincipal
        "UHCT_ACUM_RODIZIO_RETAGUARDA":         21 + 12764,                     # Leituras.UHCT_AcumuladorRodizioRetaguarda

        # UHLM
        "UHLM_INFO":                            22 + 12764,                     # Leituras.UHLM_Info
        "UHLM_OPERACIONAL":                     [22 + 12764, 0],                # UHLM.Info.Operacional
        "UHLM_LIGADA":                          [22 + 12764, 1],                # UHLM.Info.Ligada
        "UHLM_MODO_LOCAL":                      [22 + 12764, 2],                # UHLM.Info.ModoLocal
        "UHLM_VALV_BOMBA_MECAN":                [22 + 12764, 3],                # UHLM.Info.UHLM_ValvulaBombaMecanica
        "UHLM_VALV_ENTRA_TRO_CALO_ABER":        [22 + 12764, 4],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Aberta
        "UHLM_VALV_ENTRA_TRO_CALO_FECH":        [22 + 12764, 5],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Fechada
        "UHLM_VALV_SAI_TRO_CALO_ABER":          [22 + 12764, 6],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Aberta
        "UHLM_VALV_SAI_TRO_CALO_FECH":          [22 + 12764, 7],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Fechada
        "UHLM_BOMBA_RETAG_OPERAC":              [22 + 12764, 8],                # UHLM.Info.UHLM_BombaRetaguarda_Operacional

        "UHLM_BOMBAS":                          23 + 12764,                     # Leituras.UHLM_Bombas
        "UHLM_BOMBA01":                         [23 + 12764, 0],                # UHLM.Bombas.Bomba01
        "UHLM_BOMBA02":                         [23 + 12764, 1],                # UHLM.Bombas.Bomba02
        "UHLM_BOMBA03":                         [23 + 12764, 2],                # UHLM.Bombas.Bomba03
        "UHLM_BOMBA04":                         [23 + 12764, 3],                # UHLM.Bombas.Bomba04

        "UHLM_RODIZIO":                         24 + 12764,                     # Leituras.UHLM_Rodizio
        "UHLM_RODIZ_HABILITADO":                [24 + 12764, 0],                # UHLM.Rodizio.RodizioHabilitado
        "UHLM_RODIZ_BOMBA01":                   [24 + 12764, 1],                # UHLM.Rodizio.Bomba01
        "UHLM_RODIZ_BOMBA02":                   [24 + 12764, 2],                # UHLM.Rodizio.Bomba02

        "UHLM_FILTROS":                         25 + 12764,                     # Leituras.UHLM_Filtros
        "UHLM_FILTRO01":                        [25 + 12764, 0],                # UHLM.Filtros.Filtro01
        "UHLM_FILTRO02":                        [25 + 12764, 1],                # UHLM.Filtros.Filtro02
        "UHLM_FILTRO03":                        [25 + 12764, 2],                # UHLM.Filtros.Filtro03
        "UHLM_FILTRO04":                        [25 + 12764, 3],                # UHLM.Filtros.Filtro04
        "UHLM_FILTRO05":                        [25 + 12764, 4],                # UHLM.Filtros.Filtro05

        "UHLM_PRESSOSTATOS":                    26 + 12764,                     # Leituras.UHLM_Pressostatos
        "UHLM_PRESSOSTATO01":                   [26 + 12764, 0],                # UHLM.Pressostatos.Pressostato01
        "UHLM_PRESSOSTATO02":                   [26 + 12764, 1],                # UHLM.Pressostatos.Pressostato02
        "UHLM_PRESSOSTATO03":                   [26 + 12764, 2],                # UHLM.Pressostatos.Pressostato03
        "UHLM_PRESSOSTATO04":                   [26 + 12764, 3],                # UHLM.Pressostatos.Pressostato04

        "UHLM_FLUXOSTATOS":                     27 + 12764,                     # Leituras.UHLM_Fluxostatos
        "UHLM_FLUXOSTATO01":                    [27 + 12764, 0],                # UHLM.Fluxostatos.Fluxostato01
        "UHLM_FLUXOSTATO02":                    [27 + 12764, 1],                # UHLM.Fluxostatos.Fluxostato02
        "UHLM_FLUXOSTATO03":                    [27 + 12764, 2],                # UHLM.Fluxostatos.Fluxostato03
        "UHLM_FLUXOSTATO04":                    [27 + 12764, 3],                # UHLM.Fluxostatos.Fluxostato04
        "UHLM_FLUXOSTATO05":                    [27 + 12764, 4],                # UHLM.Fluxostatos.Fluxostato05
        "UHLM_FLUXOSTATO06":                    [27 + 12764, 5],                # UHLM.Fluxostatos.Fluxostato06
        "UHLM_FLUXOSTATO07":                    [27 + 12764, 6],                # UHLM.Fluxostatos.Fluxostato07

        "UHLM_NIVEL_OLEO":                      28 + 12764,                     # Leituras.UHLM_NivelOleo
        "UHLM_NIVEL_OLEO_LL":                   [28 + 12764, 0],                # UHLM.NivelOleo.LL
        "UHLM_NIVEL_OLEO_L":                    [28 + 12764, 1],                # UHLM.NivelOleo.L
        "UHLM_NIVEL_OLEO_H":                    [28 + 12764, 2],                # UHLM.NivelOleo.H
        "UHLM_NIVEL_OLEO_HH":                   [28 + 12764, 3],                # UHLM.NivelOleo.HH

        "UHLM_ACUM_RODIZIO_PRINCIPAL":          29 + 12764,                     # Leituras.UHLM_AcumuladorRodizioPrincipal
        "UHLM_ACUM_RODIZIO_RETAGUARDA":         30 + 12764,                     # Leituras.UHLM_AcumuladorRodizioRetaguarda

        "UHLM_FLUXOSTATO_OLEO_01":              122 + 12764,                    # Leituras.UHLM_FluxostatoOleo01
        "UHLM_FLUXOSTATO_OLEO_02":              123 + 12764,                    # Leituras.UHLM_FluxostatoOleo02
        "UHLM_FLUXOSTATO_OLEO_03":              124 + 12764,                    # Leituras.UHLM_FluxostatoOleo03
        "UHLM_FLUXOSTATO_OLEO_04":              125 + 12764,                    # Leituras.UHLM_FluxostatoOleo04

        # Turbina
        "TURB_INFO":                            31 + 12764,                     # Leituras.Turb_Info
        "TURB_EQUALIZADA":                      [31 + 12764, 0],                # Turbina.Info.Equalizada
        "TURB_PRONTA":                          [31 + 12764, 1],                # Turbina.Info.Pronta
        "TURB_FECHADA":                         [31 + 12764, 2],                # Turbina.Info.Fechada
        "TURB_TRAVADA":                         [31 + 12764, 3],                # Turbina.Info.Travada
        "TURB_PARADA":                          [31 + 12764, 4],                # Turbina.Info.Parada
        "TURB_EQUALIZANDO":                     [31 + 12764, 5],                # Turbina.Info.Equalizando
        "TURB_FECHANDO":                        [31 + 12764, 6],                # Turbina.Info.Fechando
        "TURB_SENS_DESATIVADO":                 [31 + 12764, 7],                # Turbina.Info.SensorDesativado
        "TURB_DISTRI_FECHADO":                  [31 + 12764, 8],                # Turbina.Info.DistribuidorFechado

        "TURB_VALVULA_BYPASS":                  32 + 12764,                     # Leituras.Turb_ValvulaByPass
        "TURB_VALV_BY_ACIONA":                  [32 + 12764, 0],                # Turbina.Bypass.Acionamento
        "TURB_VALV_BY_FECHADO":                 [32 + 12764, 1],                # Turbina.Bypass.Fechado
        "TURB_VALV_BY_ABERTO":                  [32 + 12764, 2],                # Turbina.Bypass.Aberto

        "TURB_VALVULA_BORBOLETA":               33 + 12764,                     # Leituras.Turb_ValvulaBorboleta
        "TURB_VALV_BORB_ACIONA":                [33 + 12764, 0],                # Turbina.Borboleta.Acionamento
        "TURB_VALV_BORB_FECHADA":               [33 + 12764, 1],                # Turbina.Borboleta.Fechada
        "TURB_VALV_BORB_ABERTA":                [33 + 12764, 2],                # Turbina.Borboleta.Aberta
        "TURB_VALV_BORB_DERIVA":                [33 + 12764, 3],                # Turbina.Borboleta.Deriva
        "TURB_VALV_BORB_TRAVADA":               [33 + 12764, 4],                # Turbina.Borboleta.Travada
        "TURB_VALV_BORB_MANTEM":                [33 + 12764, 5],                # Turbina.Borboleta.Mantem

        "TURB_TEMPO_CRACK_EFETIVO":             34 + 12764,                     # Leituras.Turb_TempoCrackEfetivo
        "TURB_TEMPO_EQUAL_EFETIVO":             35 + 12764,                     # Leituras.Turb_TempoEqualizacaoEfetivo
        "TURB_PRESSAO_CONDUTO":                 36 + 12764,                     # Leituras.Turb_PressaoConduto
        "TURB_PRESSAO_CAIXA_ESPIRAL":           37 + 12764,                     # Leituras.Turb_PressaoCaixaEspiral
        "TURB_VAZAO_TURBINADA":                 38 + 12764,                     # Leituras.Turb_VazaoTurbinada
        "TURB_VIBRACAO_01":                     39 + 12764,                     # Leituras.Turb_Vibracao01
        "TURB_VIBRACAO_02":                     40 + 12764,                     # Leituras.Turb_Vibracao02
        "TURB_VIBRACAO_03":                     41 + 12764,                     # Leituras.Turb_Vibracao03
        "TURB_VIBRACAO_04":                     42 + 12764,                     # Leituras.Turb_Vibracao04

        "TURB_FRENAGEM":                        43 + 12764,                     # Leituras.Turb_Frenagem
        "TURB_FRENA_APLICADO":                  [43 + 12764, 0],                # Turbina.Frenagem.Info.Aplicado
        "TURB_FRENA_MANUAL":                    [43 + 12764, 1],                # Turbina.Frenagem.Info.Manual
        "TURB_FRENA_PRESSOS":                   [43 + 12764, 2],                # Turbina.Frenagem.Info.Pressostato
        "TURB_FRENA_1ZE":                       [43 + 12764, 3],                # Turbina.Frenagem.Info.[1ZE]
        "TURB_FRENA_2ZE":                       [43 + 12764, 4],                # Turbina.Frenagem.Info.[2ZE]

        "TURB_VIBRACAO_05":                     128 + 12764,                    # Leituras.Turb_Vibracao05

        # Reg V
        "REG_V_INFO":                           44 + 12764,                     # Leituras.RegV_Info
        "REG_V_HABILITADO":                     [44 + 12764, 0],                # RegV.Info.Habilitado
        "REG_V_BASE_CARGA":                     [44 + 12764, 1],                # RegV.Info.BaseCarga
        "REG_V_RPM30":                          [44 + 12764, 2],                # RegV.Info.RPM30
        "REG_V_RPM90":                          [44 + 12764, 3],                # RegV.Info.RPM90
        "REG_V_CARGA_ZERADA":                   [44 + 12764, 4],                # RegV.Info.CargaZerada
        "REG_V_MODO_ESTATISMO":                 [44 + 12764, 5],                # RegV.Info.ModoEstatismo
        "REG_V_MODO_BASE_CARGA":                [44 + 12764, 6],                # RegV.Info.ModoBaseCarga
        "REG_V_DISTRI_FECHADO":                 [44 + 12764, 7],                # RegV.Info.DistribuidorFechado

        "REG_V_ESTADO":                         45 + 12764,                     # Leituras.RegV_Estado
        "REG_V_FALHA":                          [45 + 12764, 0],                # RegV.Estado.Falha
        "REG_V_PARADO":                         [45 + 12764, 1],                # RegV.Estado.Parado
        "REG_V_CTRL_MANUAL_DISTRI":             [45 + 12764, 2],                # RegV.Estado.ControleManualDistribuidor
        "REG_V_CTRL_MANUAL_VALV":               [45 + 12764, 3],                # RegV.Estado.ControleManualValvula
        "REG_V_CTRL_VELOC":                     [45 + 12764, 4],                # RegV.Estado.ControleVelocidade
        "REG_V_COMPENSA_POT_ATIVA":             [45 + 12764, 5],                # RegV.Estado.CompensacaoPotenciaAtiva
        "REG_V_CTRL_POT_ATIVA":                 [45 + 12764, 6],                # RegV.Estado.ControlePotenciaAtiva

        "REG_V_VELOCIDADE":                     46 + 12764,                     # Leituras.RegV_Velocidade
        "REG_V_DISTRIBUIDOR":                   47 + 12764,                     # Leituras.RegV_Distribuidor
        "REG_V_ROTOR":                          48 + 12764,                     # Leituras.RegV_Rotor
        "REG_V_POT_ALVO":                       49 + 12764,                     # Leituras.RegV_PotenciaAlvo

        "REG_V_CONJUGADO_INFO":                 127 + 12764,                    # Leituras.RegV_CurvaConjugacao_Info
        "REG_V_CONJ_AUTOMATICO":                [127 + 12764, 0],               # RegV.Conjugado.Automatico
        "REG_V_CONJ_MANUAL":                    [127 + 12764, 1],               # RegV.Conjugado.Manual
        "REG_V_CONJUGADO1":                     [127 + 12764, 2],               # RegV.Conjugado.Conjugado1
        "REG_V_CONJUGADO2":                     [127 + 12764, 3],               # RegV.Conjugado.Conjugado2
        "REG_V_CONJUGADO3":                     [127 + 12764, 4],               # RegV.Conjugado.Conjugado3

        # Reg T
        "REG_T_INFO":                           50 + 12764,                     # Leituras.RegT_Info
        "REG_T_HABILITACAO":                    [50 + 12764, 0],                # RegT.Info.Habilitacao
        "REG_T_TENSAO_ESTAB":                   [50 + 12764, 1],                # RegT.Info.TensaoEstabilizada
        "REG_T_CONTATOR_ABERTO":                [50 + 12764, 2],                # RegT.Info.ContatorAberto
        "REG_T_CONTATOR_FECHADO":               [50 + 12764, 3],                # RegT.Info.ContatorFechado
        "REG_T_PRE_EXCITACAO":                  [50 + 12764, 4],                # RegT.Info.PreExcitacao
        "REG_T_MTVC":                           [50 + 12764, 5],                # RegT.Info.MTVC
        "REG_T_MECC":                           [50 + 12764, 6],                # RegT.Info.MECC
        "REG_T_OPER_ONLINE":                    [50 + 12764, 7],                # RegT.Info.OperacaoOnline
        "REG_T_OPER_PARALELA":                  [50 + 12764, 9],                # RegT.Info.OperacaoParalela

        "REG_T_UEXCITACAO":                     51 + 12764,                     # Leituras.RegT_UExcitacao
        "REG_T_IEXCITACAO":                     52 + 12764,                     # Leituras.RegT_IExcitacao
        "REG_T_FPALVO":                         128 + 12764,                    # Leituras.RegT_FPAlvo
        "REG_T_REATIVO_ALVO":                   129 + 12764,                    # Leituras.RegT_ReativoAlvo

        # Sinc
        "SINC_INFO":                            53 + 12764,                     # Leituras.Sinc_Info
        "SINC_HABILITADO":                      [53 + 12764, 0],                # Sincronoscopio.Info.Habilitado
        "SINC_MODO_AUTO":                       [53 + 12764, 1],                # Sincronoscopio.Info.ModoAutomatico
        "SINC_MODO_MANUAL":                     [53 + 12764, 2],                # Sincronoscopio.Info.ModoManual
        "SINC_BARRA_MORTA":                     [53 + 12764, 3],                # Sincronoscopio.Info.BarraMorta

        "SINC_FREQ_GERADOR":                    54 + 12764,                     # Leituras.Sinc_FrequenciaGerador
        "SINC_FREQ_BARRA":                      55 + 12764,                     # Leituras.Sinc_FrequenciaBarra
        "SINC_TENSAO_GERADOR":                  56 + 12764,                     # Leituras.Sinc_TensaoGerador
        "SINC_TENSAO_BARRA":                    57 + 12764,                     # Leituras.Sinc_TensaoBarra

        # DJ
        "Dj52G_INFO":                           58 + 12764,                     # Leituras.Disj52G_Info
        "Dj52G_ABERTO":                         [58 + 12764, 0],                # Disjuntor52G.Info.Aberto
        "Dj52G_FECHADO":                        [58 + 12764, 1],                # Disjuntor52G.Info.Fechado
        "Dj52G_INCONSISTENTE":                  [58 + 12764, 2],                # Disjuntor52G.Info.Inconsistente
        "Dj52G_TRIP":                           [58 + 12764, 3],                # Disjuntor52G.Info.TRIP
        "Dj52G_TESTE":                          [58 + 12764, 4],                # Disjuntor52G.Info.Teste
        "Dj52G_INSERIDO":                       [58 + 12764, 5],                # Disjuntor52G.Info.Inserido
        "Dj52G_EXTRAIVEL":                      [58 + 12764, 6],                # Disjuntor52G.Info.Extraivel
        "Dj52G_MOLA_CARRE":                     [58 + 12764, 7],                # Disjuntor52G.Info.MolaCarregada
        "Dj52G_CONDICAO":                       [58 + 12764, 8],                # Disjuntor52G.Info.CondicaoFechamento
        "Dj52G_FALTA_VCC":                      [58 + 12764, 9],                # Disjuntor52G.Info.FaltaVCC

        # Tensão
        "TENSAO_RN":                            59 + 12764,                     # Leituras.Gerador_TensaoRN
        "TENSAO_SN":                            60 + 12764,                     # Leituras.Gerador_TensaoSN
        "TENSAO_TN":                            61 + 12764,                     # Leituras.Gerador_TensaoTN
        "TENSAO_RS":                            62 + 12764,                     # Leituras.Gerador_TensaoRS
        "TENSAO_ST":                            63 + 12764,                     # Leituras.Gerador_TensaoST
        "TENSAO_TR":                            64 + 12764,                     # Leituras.Gerador_TensaoTR

        # Corrente
        "CORRENTE_R":                           65 + 12764,                     # Leituras.Gerador_CorrenteR
        "CORRENTE_S":                           66 + 12764,                     # Leituras.Gerador_CorrenteS
        "CORRENTE_T":                           67 + 12764,                     # Leituras.Gerador_CorrenteT
        "CORRENTE_MEDIA":                       68 + 12764,                     # Leituras.Gerador_CorrenteMedia

        # Potência Ativa
        "POT_ATIVA_1":                          69 + 12764,                     # Leituras.Gerador_PotenciaAtiva1
        "POT_ATIVA_2":                          70 + 12764,                     # Leituras.Gerador_PotenciaAtiva2
        "POT_ATIVA_3":                          71 + 12764,                     # Leituras.Gerador_PotenciaAtiva3
        "POT_ATIVA_MEDIA":                      72 + 12764,                     # Leituras.Gerador_PotenciaAtivaMedia

        # Potência Reativa
        "POT_REATIVA_1":                        73 + 12764,                     # Leituras.Gerador_PotenciaReativa1
        "POT_REATIVA_2":                        74 + 12764,                     # Leituras.Gerador_PotenciaReativa2
        "POT_REATIVA_3":                        75 + 12764,                     # Leituras.Gerador_PotenciaReativa3
        "POT_REATIVA_MEDIA":                    76 + 12764,                     # Leituras.Gerador_PotenciaReativaMedia

        # Potência Aparente
        "POT_APARENTE_1":                       77 + 12764,                     # Leituras.Gerador_PotenciaAparente1
        "POT_APARENTE_2":                       78 + 12764,                     # Leituras.Gerador_PotenciaAparente2
        "POT_APARENTE_3":                       79 + 12764,                     # Leituras.Gerador_PotenciaAparente3
        "POT_APARENTE_MEDIA":                   80 + 12764,                     # Leituras.Gerador_PotenciaAparenteMedia

        # Fator Potência
        "FATOR_POT_1":                          81 + 12764,                     # Leituras.Gerador_FatorPotencia1
        "FATOR_POT_2":                          82 + 12764,                     # Leituras.Gerador_FatorPotencia2
        "FATOR_POT_3":                          83 + 12764,                     # Leituras.Gerador_FatorPotencia3
        "FATOR_POT_MEDIA":                      84 + 12764,                     # Leituras.Gerador_FatorPotenciaMedia

        # Frequencia
        "FREQUENCIA":                           85 + 12764,                     # Leituras.Gerador_Frequencia

        # Energia Fornecida
        "ENERGIA_FORNECIDA_TWh":                86 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTWh
        "ENERGIA_FORNECIDA_GWh":                87 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGWh
        "ENERGIA_FORNECIDA_MWh":                88 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMWh
        "ENERGIA_FORNECIDA_kWh":                89 + 12764,                     # Leituras.Gerador_EnergiaFornecidakWh
        "ENERGIA_FORNECIDA_TVarh":              90 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTVarh
        "ENERGIA_FORNECIDA_GVarh":              91 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGVarh
        "ENERGIA_FORNECIDA_MVarh":              92 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMVarh
        "ENERGIA_FORNECIDA_kVarh":              93 + 12764,                     # Leituras.Gerador_EnergiaFornecidakVarh
        "ENERGIA_CORNECIDA_TVarh":              94 + 12764,                     # Leituras.Gerador_EnergiaConsumidaTVarh
        "ENERGIA_CORNECIDA_GVarh":              95 + 12764,                     # Leituras.Gerador_EnergiaConsumidaGVarh
        "ENERGIA_CORNECIDA_MVarh":              96 + 12764,                     # Leituras.Gerador_EnergiaConsumidaMVarh
        "ENERGIA_CORNECIDA_kVarh":              97 + 12764,                     # Leituras.Gerador_EnergiaConsumidakVarh

        "GERADOR_FP_INFO":                      98 + 12764,                     # Leituras.Gerador_FPInfo
        "GERADOR_FP_FASE1_IND":                 [98 + 12764, 0],                # Gerador.FP_Info.Fase1_Ind
        "GERADOR_FP_FASE1_CAP":                 [98 + 12764, 1],                # Gerador.FP_Info.Fase1_Cap
        "GERADOR_FP_FASE2_IND":                 [98 + 12764, 2],                # Gerador.FP_Info.Fase2_Ind
        "GERADOR_FP_FASE2_CAP":                 [98 + 12764, 3],                # Gerador.FP_Info.Fase2_Cap
        "GERADOR_FP_FASE3_IND":                 [98 + 12764, 4],                # Gerador.FP_Info.Fase3_Ind
        "GERADOR_FP_FASE3_CAP":                 [98 + 12764, 5],                # Gerador.FP_Info.Fase3_Cap
        "GERADOR_FP_FASE4_IND":                 [98 + 12764, 6],                # Gerador.FP_Info.Total_Ind
        "GERADOR_FP_FASE4_CAP":                 [98 + 12764, 7],                # Gerador.FP_Info.Total_Cap

        # Controles
        "CTRL_REATIVO_INFO":                    99 + 12764,                    # Leituras.CtrlReativo_Info
        "CTRL_REAT_MODO_FP":                    [99 + 12764, 0],               # CtrlReativo.Info.ModoFP
        "CTRL_REAT_MODO_VAR":                   [99 + 12764, 1],               # CtrlReativo.Info.ModoVar

        "CTRL_POTENCIA_INFO":                   100 + 12764,                    # Leituras.CtrlPotencia_Info
        "CTRL_POT_MODO_NIVEL":                  [100 + 12764, 0],               # CtrlPotencia.Info.ModoNivel
        "CTRL_POT_MODO_POT":                    [100 + 12764, 1],               # CtrlPotencia.Info.ModoPotencia
        "CTRL_POT_MODO_RELIGA_AUTO":            [100 + 12764, 2],               # CtrlPotencia.Info.ModoReligamentoAutomatico

        # Horimetros
        "HORIM_ELETR_LOW":                      101 + 12764,                    # Leituras.HorimetroEletrico_Low
        "HORIM_ELETR_HIGH":                     102 + 12764,                    # Leituras.HorimetroEletrico_High
        "HORIM_MECAN_LOW":                      103 + 12764,                    # Leituras.HorimetroMecanico_Low
        "HORIM_MECAN_HIGH":                     104 + 12764,                    # Leituras.HorimetroMecanico_High

        # Temperatura
        "TEMPERATURA_01":                       106 + 12764,                    # Leituras.Temperatura_01
        "TEMPERATURA_02":                       107 + 12764,                    # Leituras.Temperatura_02
        "TEMPERATURA_03":                       108 + 12764,                    # Leituras.Temperatura_03
        "TEMPERATURA_04":                       109 + 12764,                    # Leituras.Temperatura_04
        "TEMPERATURA_05":                       110 + 12764,                    # Leituras.Temperatura_05
        "TEMPERATURA_06":                       111 + 12764,                    # Leituras.Temperatura_06
        "TEMPERATURA_07":                       112 + 12764,                    # Leituras.Temperatura_07
        "TEMPERATURA_08":                       113 + 12764,                    # Leituras.Temperatura_08
        "TEMPERATURA_09":                       114 + 12764,                    # Leituras.Temperatura_09
        "TEMPERATURA_10":                       115 + 12764,                    # Leituras.Temperatura_10
        "TEMPERATURA_11":                       116 + 12764,                    # Leituras.Temperatura_11
        "TEMPERATURA_12":                       117 + 12764,                    # Leituras.Temperatura_12
        "TEMPERATURA_13":                       118 + 12764,                    # Leituras.Temperatura_13
        "TEMPERATURA_14":                       119 + 12764,                    # Leituras.Temperatura_14
        "TEMPERATURA_15":                       120 + 12764,                    # Leituras.Temperatura_15
        "TEMPERATURA_16":                       121 + 12764,                    # Leituras.Temperatura_16


        ## DISJUNTORES

        "DJ_01":                                0 + 12564,                      # Disjuntor Q125.0 - Alimentação Circuitos de Comando                                  -> condic_indisponibiliza UG1
        "DJ_02":                                0 + 12564,                      # Disjuntor Q125.1 - Alimentação GRTD2000                                              -> condic_indisponibiliza UG1
        "DJ_03":                                1 + 12564,                      # Disjuntor Q125.2 - Alimentação Relés de Proteção                                     -> condic_indisponibiliza UG1
        "DJ_04":                                2 + 12564,                      # Disjuntor Q24.0 - Alimentação Válvula Proporcional e Transdutor de Posição           -> condic_indisponibiliza UG1
        "DJ_05":                                3 + 12564,                      # CSG - Disjuntor Q220.1 - Alimentação Carregamento de Mola                            -> condic_indisponibiliza UG1
        "DJ_06":                                4 + 12564,                      # CSG - Disjuntor Q125.0 - Alimentação Circuito de Comando 52G                         -> condic_indisponibiliza UG1
        "DJ_07":                                5 + 12564,                      # Q49 - Disjuntor Q125.0 UG1 - Alimentação SEL2600
        "DJ_08":                                6 + 12564,                      # Disjuntor Motor QM1 - Bomba de Óleo 01 da UHCT                                       -> condic_indisponibiliza UG1
        "DJ_09":                                7 + 12564,                      # Disjuntor Motor QM2 - Bomba de Óleo 02 da UHCT                                       -> condic_indisponibiliza UG1
        "DJ_10":                                8 + 12564,                      # Disjuntor Motor QM3 - Bomba de Óleo 01 da UHLM                                       -> condic_indisponibiliza UG1
        "DJ_11":                                9 + 12564,                     #
        "DJ_12":                                10 + 12564,                     #
        "DJ_13":                                11 + 12564,                     #
        "DJ_14":                                12 + 12564,                     #
        "DJ_15":                                13 + 12564,                     #
        "DJ_16":                                14 + 12564,                     #
        "DJ_17":                                15 + 12564,                     #
        "DJ_18":                                16 + 12564,                     #
        "DJ_19":                                17 + 12564,                     #
        "DJ_20":                                18 + 12564,                     #
        "DJ_21":                                19 + 12564,                     #
        "DJ_22":                                20 + 12564,                     #
        "DJ_23":                                21 + 12564,                     #
        "DJ_24":                                22 + 12564,                     #
        "DJ_25":                                23 + 12564,                     #
        "DJ_26":                                24 + 12564,                     #
        "DJ_27":                                25 + 12564,                     #
        "DJ_28":                                26 + 12564,                     #
        "DJ_29":                                27 + 12564,                     #
        "DJ_30":                                28 + 12564,                     #
        "DJ_31":                                29 + 12564,                     #
        "DJ_32":                                30 + 12564,                     #


        ## ALARMES

        # Específicos UG1
        "Alarme04_10":                          [5 + 14199, 10],
        "Alarme04_11":                          [5 + 14199, 11],
        "Alarme04_12":                          [5 + 14199, 12],

        "Alarme10_08":                          [9 + 14199, 8],
        "Alarme10_09":                          [9 + 14199, 9],

        "Alarme12_01":                          [11 + 14199, 1],
        "Alarme12_07":                          [11 + 14199, 7],
        "Alarme12_08":                          [11 + 14199, 8],
        "Alarme12_09":                          [11 + 14199, 9],
        "Alarme12_10":                          [11 + 14199, 10],
        "Alarme12_11":                          [11 + 14199, 11],
        "Alarme12_12":                          [11 + 14199, 12],
        "Alarme12_13":                          [11 + 14199, 13],

        "Alarme15_13":                          [14 + 14199, 13],
        "Alarme15_12":                          [14 + 14199, 12],

        # Gerais
        "Alarme01_00":                          [0 + 14199, 0],
        "Alarme01_01":                          [0 + 14199, 1],
        "Alarme01_02":                          [0 + 14199, 2],
        "Alarme01_03":                          [0 + 14199, 3],
        "Alarme01_06":                          [0 + 14199, 6],
        "Alarme01_07":                          [0 + 14199, 7],
        "Alarme01_08":                          [0 + 14199, 8],
        "Alarme01_09":                          [0 + 14199, 9],
        "Alarme01_10":                          [0 + 14199, 10],
        "Alarme01_11":                          [0 + 14199, 11],
        "Alarme01_12":                          [0 + 14199, 12],
        "Alarme01_13":                          [0 + 14199, 13],
        "Alarme01_14":                          [0 + 14199, 14],
        "Alarme01_15":                          [0 + 14199, 15],

        "Alarme02_00":                          [1 + 14199, 0],
        "Alarme02_01":                          [1 + 14199, 1],
        "Alarme02_02":                          [1 + 14199, 2],
        "Alarme02_03":                          [1 + 14199, 3],
        "Alarme02_04":                          [1 + 14199, 4],
        "Alarme02_05":                          [1 + 14199, 5],
        "Alarme02_06":                          [1 + 14199, 6],
        "Alarme02_07":                          [1 + 14199, 7],
        "Alarme02_08":                          [1 + 14199, 8],
        "Alarme02_09":                          [1 + 14199, 9],
        "Alarme02_10":                          [1 + 14199, 10],
        "Alarme02_11":                          [1 + 14199, 11],
        "Alarme02_12":                          [1 + 14199, 12],
        "Alarme02_13":                          [1 + 14199, 13],
        "Alarme02_14":                          [1 + 14199, 14],
        "Alarme02_15":                          [1 + 14199, 15],

        "Alarme03_00":                          [2 + 14199, 0],
        "Alarme03_01":                          [2 + 14199, 1],
        "Alarme03_02":                          [2 + 14199, 2],
        "Alarme03_03":                          [2 + 14199, 3],
        "Alarme03_04":                          [2 + 14199, 4],
        "Alarme03_05":                          [2 + 14199, 5],
        "Alarme03_06":                          [2 + 14199, 6],
        "Alarme03_07":                          [2 + 14199, 7],
        "Alarme03_08":                          [2 + 14199, 8],
        "Alarme03_09":                          [2 + 14199, 9],
        "Alarme03_10":                          [2 + 14199, 10],
        "Alarme03_11":                          [2 + 14199, 11],
        "Alarme03_12":                          [2 + 14199, 12],
        "Alarme03_13":                          [2 + 14199, 13],
        "Alarme03_14":                          [2 + 14199, 14],
        "Alarme03_15":                          [2 + 14199, 15],

        "Alarme04_00":                          [3 + 14199, 0],
        "Alarme04_01":                          [3 + 14199, 1],
        "Alarme04_02":                          [3 + 14199, 2],
        "Alarme04_04":                          [3 + 14199, 4],
        "Alarme04_05":                          [3 + 14199, 5],
        "Alarme04_06":                          [3 + 14199, 6],
        "Alarme04_07":                          [3 + 14199, 7],
        "Alarme04_09":                          [3 + 14199, 9],
        "Alarme04_10":                          [3 + 14199, 10],
        "Alarme04_11":                          [3 + 14199, 11],
        "Alarme04_12":                          [3 + 14199, 12],
        "Alarme04_13":                          [3 + 14199, 13],
        "Alarme04_14":                          [3 + 14199, 14],
        "Alarme04_15":                          [3 + 14199, 15],

        "Alarme05_00":                          [4 + 14199, 0],
        "Alarme05_02":                          [4 + 14199, 2],
        "Alarme05_03":                          [4 + 14199, 3],
        "Alarme05_04":                          [4 + 14199, 4],
        "Alarme05_05":                          [4 + 14199, 5],
        "Alarme05_06":                          [4 + 14199, 6],
        "Alarme05_07":                          [4 + 14199, 7],
        "Alarme05_09":                          [4 + 14199, 9],
        "Alarme05_10":                          [4 + 14199, 10],
        "Alarme05_11":                          [4 + 14199, 11],
        "Alarme05_12":                          [4 + 14199, 12],
        "Alarme05_13":                          [4 + 14199, 13],
        "Alarme05_14":                          [4 + 14199, 14],
        "Alarme05_15":                          [4 + 14199, 15],

        "Alarme06_00":                          [5 + 14199, 0],
        "Alarme06_03":                          [5 + 14199, 3],
        "Alarme06_04":                          [5 + 14199, 4],
        "Alarme06_05":                          [5 + 14199, 5],
        "Alarme06_08":                          [5 + 14199, 8],
        "Alarme06_09":                          [5 + 14199, 9],
        "Alarme06_10":                          [5 + 14199, 10],
        "Alarme06_11":                          [5 + 14199, 11],
        "Alarme06_12":                          [5 + 14199, 12],
        "Alarme06_13":                          [5 + 14199, 13],
        "Alarme06_14":                          [5 + 14199, 14],
        "Alarme06_15":                          [5 + 14199, 15],

        "Alarme07_00":                          [6 + 14199, 0],
        "Alarme07_01":                          [6 + 14199, 1],
        "Alarme07_02":                          [6 + 14199, 2],
        "Alarme07_03":                          [6 + 14199, 3],
        "Alarme07_06":                          [6 + 14199, 6],
        "Alarme07_07":                          [6 + 14199, 7],
        "Alarme07_08":                          [6 + 14199, 8],
        "Alarme07_09":                          [6 + 14199, 9],
        "Alarme07_10":                          [6 + 14199, 10],
        "Alarme07_11":                          [6 + 14199, 11],
        "Alarme07_12":                          [6 + 14199, 12],
        "Alarme07_13":                          [6 + 14199, 13],
        "Alarme07_14":                          [6 + 14199, 14],
        "Alarme07_15":                          [6 + 14199, 15],

        "Alarme08_00":                          [7 + 14199, 0],
        "Alarme08_01":                          [7 + 14199, 1],
        "Alarme08_02":                          [7 + 14199, 2],
        "Alarme08_03":                          [7 + 14199, 3],
        "Alarme08_07":                          [7 + 14199, 7],
        "Alarme08_08":                          [7 + 14199, 8],
        "Alarme08_09":                          [7 + 14199, 9],
        "Alarme08_10":                          [7 + 14199, 10],
        "Alarme08_11":                          [7 + 14199, 11],
        "Alarme08_12":                          [7 + 14199, 12],
        "Alarme08_13":                          [7 + 14199, 13],
        "Alarme08_14":                          [7 + 14199, 14],
        "Alarme08_15":                          [7 + 14199, 15],

        "Alarme09_00":                          [8 + 14199, 0],
        "Alarme09_01":                          [8 + 14199, 1],
        "Alarme09_02":                          [8 + 14199, 2],
        "Alarme09_03":                          [8 + 14199, 3],
        "Alarme09_04":                          [8 + 14199, 4],
        "Alarme09_06":                          [8 + 14199, 6],
        "Alarme09_07":                          [8 + 14199, 7],
        "Alarme09_08":                          [8 + 14199, 8],
        "Alarme09_09":                          [8 + 14199, 9],
        "Alarme09_10":                          [8 + 14199, 10],
        "Alarme09_11":                          [8 + 14199, 11],
        "Alarme09_12":                          [8 + 14199, 12],
        "Alarme09_13":                          [8 + 14199, 13],
        "Alarme09_14":                          [8 + 14199, 14],
        "Alarme09_15":                          [8 + 14199, 15],

        "Alarme10_00":                          [9 + 14199, 0],
        "Alarme10_01":                          [9 + 14199, 1],
        "Alarme10_02":                          [9 + 14199, 2],
        "Alarme10_03":                          [9 + 14199, 3],
        "Alarme10_05":                          [9 + 14199, 5],
        "Alarme10_06":                          [9 + 14199, 6],
        "Alarme10_07":                          [9 + 14199, 7],
        "Alarme10_08":                          [9 + 14199, 8],
        "Alarme10_09":                          [9 + 14199, 9],
        "Alarme10_10":                          [9 + 14199, 10],
        "Alarme10_11":                          [9 + 14199, 11],
        "Alarme10_12":                          [9 + 14199, 12],
        "Alarme10_13":                          [9 + 14199, 13],
        "Alarme10_14":                          [9 + 14199, 14],
        "Alarme10_15":                          [9 + 14199, 15],

        "Alarme11_00":                          [10 + 14199, 0],
        "Alarme11_01":                          [10 + 14199, 1],
        "Alarme11_02":                          [10 + 14199, 2],
        "Alarme11_06":                          [10 + 14199, 6],
        "Alarme11_07":                          [10 + 14199, 7],
        "Alarme11_08":                          [10 + 14199, 8],
        "Alarme11_09":                          [10 + 14199, 9],
        "Alarme11_10":                          [10 + 14199, 10],
        "Alarme11_11":                          [10 + 14199, 11],
        "Alarme11_12":                          [10 + 14199, 12],
        "Alarme11_13":                          [10 + 14199, 13],
        "Alarme11_14":                          [10 + 14199, 14],
        "Alarme11_15":                          [10 + 14199, 15],

        "Alarme12_01":                          [11 + 14199, 1],
        "Alarme12_02":                          [11 + 14199, 2],
        "Alarme12_03":                          [11 + 14199, 3],
        "Alarme12_04":                          [11 + 14199, 4],
        "Alarme12_05":                          [11 + 14199, 5],
        "Alarme12_06":                          [11 + 14199, 6],
        "Alarme12_07":                          [11 + 14199, 7],
        "Alarme12_09":                          [11 + 14199, 9],
        "Alarme12_10":                          [11 + 14199, 10],
        "Alarme12_11":                          [11 + 14199, 11],
        "Alarme12_12":                          [11 + 14199, 12],
        "Alarme12_13":                          [11 + 14199, 13],
        "Alarme12_14":                          [11 + 14199, 14],
        "Alarme12_15":                          [11 + 14199, 15],

        "Alarme13_00":                          [12 + 14199, 0],
        "Alarme13_01":                          [12 + 14199, 1],
        "Alarme13_02":                          [12 + 14199, 2],
        "Alarme13_03":                          [12 + 14199, 3],
        "Alarme13_09":                          [12 + 14199, 9],
        "Alarme13_10":                          [12 + 14199, 10],
        "Alarme13_11":                          [12 + 14199, 11],
        "Alarme13_12":                          [12 + 14199, 12],
        "Alarme13_13":                          [12 + 14199, 13],
        "Alarme13_14":                          [12 + 14199, 14],
        "Alarme13_15":                          [12 + 14199, 15],

        "Alarme14_00":                          [13 + 14199, 0],
        "Alarme14_01":                          [13 + 14199, 1],
        "Alarme14_02":                          [13 + 14199, 2],
        "Alarme14_03":                          [13 + 14199, 3],
        "Alarme14_04":                          [13 + 14199, 4],
        "Alarme14_05":                          [13 + 14199, 5],
        "Alarme14_10":                          [13 + 14199, 10],
        "Alarme14_11":                          [13 + 14199, 11],
        "Alarme14_12":                          [13 + 14199, 12],
        "Alarme14_13":                          [13 + 14199, 13],
        "Alarme14_14":                          [13 + 14199, 14],
        "Alarme14_15":                          [13 + 14199, 15],

        "Alarme15_00":                          [14 + 14199, 0],
        "Alarme15_01":                          [14 + 14199, 1],
        "Alarme15_02":                          [14 + 14199, 2],
        "Alarme15_03":                          [14 + 14199, 3],
        "Alarme15_04":                          [14 + 14199, 4],
        "Alarme15_05":                          [14 + 14199, 5],
        "Alarme15_06":                          [14 + 14199, 6],
        "Alarme15_07":                          [14 + 14199, 7],
        "Alarme15_08":                          [14 + 14199, 8],
        "Alarme15_09":                          [14 + 14199, 9],
        "Alarme15_10":                          [14 + 14199, 10],
        "Alarme15_12":                          [14 + 14199, 12],
        "Alarme15_13":                          [14 + 14199, 13],
        "Alarme15_14":                          [14 + 14199, 14],
        "Alarme15_15":                          [14 + 14199, 15],

        "Alarme16_00":                          [15 + 14199, 0],
        "Alarme16_01":                          [15 + 14199, 1],
        "Alarme16_02":                          [15 + 14199, 2],
        "Alarme16_03":                          [15 + 14199, 3],
        "Alarme16_04":                          [15 + 14199, 4],
        "Alarme16_05":                          [15 + 14199, 5],
        "Alarme16_06":                          [15 + 14199, 6],
        "Alarme16_07":                          [15 + 14199, 7],
        "Alarme16_08":                          [15 + 14199, 8],
        "Alarme16_09":                          [15 + 14199, 9],
        "Alarme16_10":                          [15 + 14199, 10],
        "Alarme16_11":                          [15 + 14199, 11],
        "Alarme16_12":                          [15 + 14199, 12],
    },
    "UG2": {
        ## COMANDOS
        # Gerais
        "CMD_RESET_ALARMES":                    0 + 12288,                      # Comandos.Operacao_PCH_AdoPopinhakResetAlarmes
        "CMD_RECONHECE_ALARMES":                0 + 12289,                      # Comandos.Operacao_PCH_AdoPopinhakReconheceAlarmes

        # Operação
        "CMD_OPER_UP":                          1 + 12289,                      # Comandos.Operacao_UP
        "CMD_OPER_UPGM":                        2 + 12289,                      # Comandos.Operacao_UPGM
        "CMD_OPER_UVD":                         3 + 12289,                      # Comandos.Operacao_UVD
        "CMD_OPER_UPS":                         4 + 12289,                      # Comandos.Operacao_UPS
        "CMD_OPER_US":                          5 + 12289,                      # Comandos.Operacao_US
        "CMD_OPER_EMERGENCIA_LIGAR":            6 + 12289,                      # Comandos.Operacao_EmergenciaLigar
        "CMD_OPER_EMERGENCIA_DESLIGAR":         7 + 12289,                      # Comandos.Operacao_EmergenciaDesligar
        "CMD_OPER_PARADA_RESET":                71 + 12289,                     # Comandos.Operacao_ParadaReset

        # Turbina
        "CMD_TURB_BYPASS_ABRIR":                8 + 12289,                      # Comandos.Turb_ByPassAbrir
        "CMD_TURB_BYPASS_FECHAR":               9 + 12289,                     # Comandos.Turb_ByPassFechar
        "CMD_TURB_BORBOLETA_ABRIR":             10 + 12289,                     # Comandos.Turb_BorboletaAbrir
        "CMD_TURB_BORBOLETA_FECHAR":            11 + 12289,                     # Comandos.Turb_BorboletaFechar
        "CMD_TURB_FRENAGEM_APLICAR":            12 + 12289,                     # Comandos.Turb_FrenagemAplicar
        "CMD_TURB_FRENAGEM_DESAPLICAR":         13 + 12289,                     # Comandos.Turb_FrenagemDesaplicar
        "CMD_TURB_FRENAGEM_MANUAL":             14 + 12289,                     # Comandos.Turb_FrenagemManual
        "CMD_TURB_FRENAGEM_AUTO":               15 + 12289,                     # Comandos.Turb_FrenagemAuto
        "CMD_TURB_SENSOR_ATIVAR":               16 + 12289,                     # Comandos.Turb_SensorAtivar
        "CMD_TURB_SENSOR_DESATIVAR":            17 + 12289,                     # Comandos.Turb_SensorDesativar

        # Reg V
        "CMD_REG_V_PARTIR":                     18 + 12289,                     # Comandos.RegV_Partir
        "CMD_REG_V_PARAR":                      19 + 12289,                     # Comandos.RegV_Parar
        "CMD_REG_V_COLOCAR_CARGA":              20 + 12289,                     # Comandos.RegV_ColocarCarga
        "CMD_REG_V_RETIRAR_CARGA":              21 + 12289,                     # Comandos.RegV_RetirarCarga
        "CMD_REG_V_INCREMENTA_VELOCIDADE":      22 + 12289,                     # Comandos.RegV_IncrementaVelocidade
        "CMD_REG_V_DECREMENTA_VELOCIDADE":      23 + 12289,                     # Comandos.RegV_DecrementaVelocidade
        "CMD_REG_V_SEL_MODO_ESTATISMO":         24 + 12289,                     # Comandos.RegV_SelecionaModoEstatismo
        "CMD_REG_V_SEL_MODO_BASECARGA":         25 + 12289,                     # Comandos.RegV_SelecionaModoBaseCarga

        # Reg T
        "CMD_REG_T_LIGAR":                      26 + 12289,                     # Comandos.RegT_Ligar
        "CMD_REG_T_DESLIGAR":                   27 + 12289,                     # Comandos.RegT_Desligar
        "CMD_REG_T_INCREMENTA_TENSAO":          28 + 12289,                     # Comandos.RegT_IncrementaTensao
        "CMD_REG_T_DECREMENTA_TENSAO":          29 + 12289,                     # Comandos.RegT_DecrementaTensao
        "CMD_REG_T_PRE_EXCITACAO":              30 + 12289,                     # Comandos.RegT_PreExcitacao

        # Sinc
        "CMD_SINC_LIGAR":                       31 + 12289,                     # Comandos.Sinc_Ligar
        "CMD_SINC_DESLIGAR":                    32 + 12289,                     # Comandos.Sinc_Desligar
        "CMD_SINC_MODO_AUTO_LIGAR":             33 + 12289,                     # Comandos.Sinc_ModoAutoLigar
        "CMD_SINC_MODO_MANUAL_LIGAR":           34 + 12289,                     # Comandos.Sinc_ModoManualLigar
        "CMD_SINC_MODO_BMORTA_LIGAR":           35 + 12289,                     # Comandos.Sinc_ModoBMortaLigar

        # DJ52G
        "CMD_DJ52G_ABRIR":                      36 + 12289,                     # Comandos.Disj52G_Abrir

        # Controle Reativo
        "CMD_CTRL_REATIVO_MODO_FPLIGAR":        37 + 12289,                     # Comandos.CtrlReativo_ModoFPLigar
        "CMD_CTRL_REATIVO_MODO_FPDESLIGAR":     38 + 12289,                     # Comandos.CtrlReativo_ModoFPDesligar
        "CMD_CTRL_REATIVO_MODO_VArLIGAR":       39 + 12289,                     # Comandos.CtrlReativo_ModoVArLigar
        "CMD_CTRL_REATIVO_MODO_VArDESLIGAR":    40 + 12289,                     # Comandos.CtrlReativo_ModoVArDesligar

        # Controle Potência
        "CMD_CTRL_POT_MODO_POT_LIGAR":          41 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaLigar
        "CMD_CTRL_POT_MODO_POT_DESLIGAR":       42 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaDesligar
        "CMD_CTRL_POT_MODO_NIVEL_LIGAR":        43 + 12289,                     # Comandos.CtrlPotencia_ModoNivelLigar
        "CMD_CTRL_POT_MODO_NIVEL_DESLIGAR":     44 + 12289,                     # Comandos.CtrlPotencia_ModoNivelDesligar
        "CMD_CTRL_POT_RELI_AUTO_LIGAR":         45 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoLigar
        "CMD_CTRL_POT_RELI_AUTO_DESLIGAR":      46 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoDesligar

        # UHCT
        "CMD_UHCT_BOMBA_01_LIGAR":              47 + 12289,                     # Comandos.UHCT_Bomba01Ligar
        "CMD_UHCT_BOMBA_01_DESLIGAR":           48 + 12289,                     # Comandos.UHCT_Bomba01Desligar
        "CMD_UHCT_BOMBA_01_PRINCIPAL":          49 + 12289,                     # Comandos.UHCT_Bomba01Principal
        "CMD_UHCT_BOMBA_02_LIGAR":              50 + 12289,                     # Comandos.UHCT_Bomba02Ligar
        "CMD_UHCT_BOMBA_02_DESLIGAR":           51 + 12289,                     # Comandos.UHCT_Bomba02Desligar
        "CMD_UHCT_BOMBA_02_PRINCIPAL":          52 + 12289,                     # Comandos.UHCT_Bomba02Principal
        "CMD_UHCT_BOMBA_AGUA_LIGAR":            53 + 12289,                     # Comandos.UHCT_BombaAguaLigar
        "CMD_UHCT_BOMBA_AGUA_DESLIGAR":         54 + 12289,                     # Comandos.UHCT_BombaAguaDesligar
        "CMD_UHCT_SENSOR_ATIVAR":               55 + 12289,                     # Comandos.UHCT_SensorAtivar
        "CMD_UHCT_SENSOR_DESATIVAR":            56 + 12289,                     # Comandos.UHCT_SensorDesativar
        "CMD_UHCT_RODIZIO_HABILITAR":           57 + 12289,                     # Comandos.UHCT_RodizioHabilitar
        "CMD_UHCT_RODIZIO_DESABILITAR":         58 + 12289,                     # Comandos.UHCT_RodizioDesabilitar

        # UHLM
        "CMD_UHLM_BOMBA_01_LIGAR":              59 + 12289,                     # Comandos.UHLM_Bomba01Ligar
        "CMD_UHLM_BOMBA_01_DESLIGAR":           60 + 12289,                     # Comandos.UHLM_Bomba01Desligar
        "CMD_UHLM_BOMBA_01_PRINCIPAL":          61 + 12289,                     # Comandos.UHLM_Bomba01Principal
        "CMD_UHLM_BOMBA_02_LIGAR":              62 + 12289,                     # Comandos.UHLM_Bomba02Ligar
        "CMD_UHLM_BOMBA_02_DESLIGAR":           63 + 12289,                     # Comandos.UHLM_Bomba02Desligar
        "CMD_UHLM_BOMBA_02_PRINCIPAL":          64 + 12289,                     # Comandos.UHLM_Bomba02Principal
        "CMD_UHLM_BOMBA_JACKING_LIGA":          65 + 12289,                     # Comandos.UHLM_BombaJackingLiga
        "CMD_UHLM_BOMBA_JACKING_DESLIGA":       66 + 12289,                     # Comandos.UHLM_BombaJackingDesliga
        "CMD_UHLM_BOMBA_AGUA_LIGA":             67 + 12289,                     # Comandos.UHLM_BombaAguaLiga
        "CMD_UHLM_BOMBA_AGUA_DESLIGA":          68 + 12289,                     # Comandos.UHLM_BombaAguaDesliga
        "CMD_UHLM_RODIZIO_HABILITAR":           69 + 12289,                     # Comandos.UHLM_RodizioHabilitar
        "CMD_UHLM_RODIZIO_DESABILITAR":         70 + 12289,                     # Comandos.UHLM_RodizioDesabilitar

        # RT
        "CMD_RT_MTVC_HABILITAR":                71 + 12289,                     # Comandos.RT_MTVC_Habilitar
        "CMD_RT_MECC_HABILITAR":                72 + 12289,                     # Comandos.RT_MECC_Habilitar
        "CMD_RT_ONLINE_HABILITAR":              73 + 12289,                     # Comandos.RT_Online_habilitar
        "CMD_RT_ONLINE_DESABILITAR":            74 + 12289,                     # Comandos.RT_Online_Desabiltar
        "CMD_RT_PARALELO_HABILITAR":            75 + 12289,                     # Comandos.RT_Paralelo_habilitar
        "CMD_RT_PARALELO_DESABILITAR":          76 + 12289,                     # Comandos.RT_Paralelo_Desabilitar

        # RV
        "CMD_RV_CONJUGADO_AUTO_HABILITAR":      77 + 12289,                     # Comandos.RV_ConjugadoAuto_habilitar
        "CMD_RV_CONJUGADO_MANUAL_HABILITAR":    78 + 12289,                     # Comandos.RV_ConjugadoManual_habilitar
        "CMD_RV_CONJUGADO_01_HABILITAR":        79 + 12289,                     # Comandos.RV_Conjugado01_habilitar
        "CMD_RV_CONJUGADO_02_HABILITAR":        80 + 12289,                     # Comandos.RV_Conjugado02_habilitar
        "CMD_RV_CONJUGADO_03_HABILITAR":        81 + 12289,                     # Comandos.RV_Conjugado03_habilitar
        "CMD_RV_CONJUGADO_04_HABILITAR":        82 + 12289,                     # Comandos.RV_Conjugado04_habilitar
        "CMD_RV_CONJUGADO_05_HABILITAR":        83 + 12289,                     # Comandos.RV_Conjugado05_habilitar


        ## SETPOINTS

        # UHCT
        "UHCT_PRESSAO_MAX":                     0 + 13569,                      # Setpoints.UHCT_PressaoMaxima
        "UHCT_PRESSAO_MIN":                     0 + 13569,                      # Setpoints.UHCT_PressaoMinima
        "UHCT_PRESSAO_DESLIGAMENTO":            1 + 13569,                      # Setpoints.UHCT_PressaoDesligamento
        "UHCT_PRESSAO_CRITICA":                 2 + 13569,                      # Setpoints.UHCT_PressaoCritica

        # Controle Potência
        "CRTL_POT_NIVEL_LL1":                   3 + 13569,                      # Setpoints.CtrlPotencia_NivelLL1
        "CRTL_POT_NIVEL_LL2":                   4 + 13569,                      # Setpoints.CtrlPotencia_NivelLL2
        "CRTL_POT_NIVEL_LL3":                   5 + 13569,                      # Setpoints.CtrlPotencia_NivelLL3
        "CRTL_POT_NIVEL_LL4":                   6 + 13569,                      # Setpoints.CtrlPotencia_NivelLL4
        "CRTL_POT_NIVEL_LL5":                   7 + 13569,                      # Setpoints.CtrlPotencia_NivelLL5
        "CRTL_POT_POT_1":                       8 + 13569,                      # Setpoints.CtrlPotencia_Potencia1
        "CRTL_POT_POT_2":                       9 + 13569,                     # Setpoints.CtrlPotencia_Potencia2
        "CRTL_POT_POT_3":                       10 + 13569,                     # Setpoints.CtrlPotencia_Potencia3
        "CRTL_POT_POT_4":                       11 + 13569,                     # Setpoints.CtrlPotencia_Potencia4
        "CRTL_POT_POT_5":                       12 + 13569,                     # Setpoints.CtrlPotencia_Potencia5
        "CRTL_POT_POT_MIN":                     13 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinima
        "CRTL_POT_POT_MIN_TEMPO":               14 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinimaTempo
        "CRTL_POT_NIVEL_RELIGAMENTO":           15 + 13569,                     # Setpoints.CtrlPotencia_NivelReligamento
        "CRTL_POT_ALVO":                        16 + 13569,                     # Setpoints.CtrlPotencia_Alvo
        "CRTL_POT_TOLERANCIA":                  17 + 13569,                     # Setpoints.CtrlPotencia_Tolerancia
        "CRTL_POT_PULSO_TEMPO":                 18 + 13569,                     # Setpoints.CtrlPotencia_PulsoTempo
        "CRTL_POT_PULSO_INTERVALO":             19 + 13569,                     # Setpoints.CtrlPotencia_PulsoIntervalo
        "CRTL_POT_SP_NIVEL":                    20 + 13569,                     # Setpoints.CtrlPotencia_SetpointNivel
        "CRTL_POT_NIVEL_MIN_ALARME":            21 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoAlarme
        "CRTL_POT_NIVEL_MIN_TRIP":              22 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoTRIP
        "CTRL_POT_POT_MAX":                     88 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMaxima

        # Controle Reativo
        "CRTL_REATIVO_SP_FP":                   23 + 13569,                     # Setpoints.CtrlReativo_SetpointFP
        "CRTL_REATIVO_SP_REATIVO":              24 + 13569,                     # Setpoints.CtrlReativo_SetpointReativo

        # Turbina
        "TURB_VIBRA_01_ALARME":                 25 + 13569,                     # Setpoints.Turb_Vibracao01Alarme
        "TURB_VIBRA_01_TRIP":                   26 + 13569,                     # Setpoints.Turb_Vibracao01TRIP
        "TURB_VIBRA_02_ALARME":                 27 + 13569,                     # Setpoints.Turb_Vibracao02Alarme
        "TURB_VIBRA_02_TRIP":                   28 + 13569,                     # Setpoints.Turb_Vibracao02TRIP
        "TURB_VIBRA_03_ALARME":                 29 + 13569,                     # Setpoints.Turb_Vibracao03Alarme
        "TURB_VIBRA_03_TRIP":                   30 + 13569,                     # Setpoints.Turb_Vibracao03TRIP
        "TURB_VIBRA_04_ALARME":                 31 + 13569,                     # Setpoints.Turb_Vibracao04Alarme
        "TURB_VIBRA_04_TRIP":                   32 + 13569,                     # Setpoints.Turb_Vibracao04TRIP
        "TURB_TEMPO_EQUALI_SP":                 33 + 13569,                     # Setpoints.Turb_TempoEqualizacaoSetpoint
        "TURB_VIBRA_05_ALARME":                 89 + 13569,                     # Setpoints.Turb_Vibracao05Alarme
        "TURB_VIBRA_05_TRIP":                   90 + 13569,                     # Setpoints.Turb_Vibracao05TRIP

        # Freio
        "FREIO_PULSO_INTERVALO":                34 + 13569,                     # Setpoints.Freio_PulsoIntervalo
        "FREIO_PULSO_TEMPO":                    35 + 13569,                     # Setpoints.Freio_PulsoTempo

        # UHCT
        "UHCT_RODIZIO_PRINCIPAL":               36 + 13569,                     # Setpoints.UHCT_RodizioPrincipal
        "UHCT_RODIZIO_RETAGUARDA":              37 + 13569,                     # Setpoints.UHCT_RodizioRetaguarda

        # UHLM
        "UHLM_RODIZIO_PRINCIPAL":               38 + 13569,                     # Setpoints.UHLM_RodizioPrincipal
        "UHLM_RODIZIO_RETAGUARDA":              39 + 13569,                     # Setpoints.UHLM_RodizioRetaguarda
        "UHLM_SP_VAZAO_01":                     91 + 13569,                     # Setpoints.UHLM_SetpointVazao01
        "UHLM_SP_VAZAO_02":                     92 + 13569,                     # Setpoints.UHLM_SetpointVazao02
        "UHLM_SP_VAZAO_03":                     93 + 13569,                     # Setpoints.UHLM_SetpointVazao03
        "UHLM_SP_VAZAO_04":                     94 + 13569,                     # Setpoints.UHLM_SetpointVazao04

        # Temperaturas
        "TEMPERATURA_01_ALARME":                40 + 13569,                     # Setpoints.Temperatura01_Alarme
        "TEMPERATURA_02_ALARME":                41 + 13569,                     # Setpoints.Temperatura02_Alarme
        "TEMPERATURA_03_ALARME":                42 + 13569,                     # Setpoints.Temperatura03_Alarme
        "TEMPERATURA_04_ALARME":                43 + 13569,                     # Setpoints.Temperatura04_Alarme
        "TEMPERATURA_05_ALARME":                44 + 13569,                     # Setpoints.Temperatura05_Alarme
        "TEMPERATURA_06_ALARME":                45 + 13569,                     # Setpoints.Temperatura06_Alarme
        "TEMPERATURA_07_ALARME":                46 + 13569,                     # Setpoints.Temperatura07_Alarme
        "TEMPERATURA_08_ALARME":                47 + 13569,                     # Setpoints.Temperatura08_Alarme
        "TEMPERATURA_09_ALARME":                48 + 13569,                     # Setpoints.Temperatura09_Alarme
        "TEMPERATURA_10_ALARME":                49 + 13569,                     # Setpoints.Temperatura10_Alarme
        "TEMPERATURA_11_ALARME":                50 + 13569,                     # Setpoints.Temperatura11_Alarme
        "TEMPERATURA_12_ALARME":                51 + 13569,                     # Setpoints.Temperatura12_Alarme
        "TEMPERATURA_13_ALARME":                52 + 13569,                     # Setpoints.Temperatura13_Alarme
        "TEMPERATURA_14_ALARME":                53 + 13569,                     # Setpoints.Temperatura14_Alarme
        "TEMPERATURA_15_ALARME":                54 + 13569,                     # Setpoints.Temperatura15_Alarme
        "TEMPERATURA_16_ALARME":                55 + 13569,                     # Setpoints.Temperatura16_Alarme
        "TEMPERATURA_01_TRIP01":                56 + 13569,                     # Setpoints.Temperatura01_TRIP01
        "TEMPERATURA_02_TRIP01":                57 + 13569,                     # Setpoints.Temperatura02_TRIP01
        "TEMPERATURA_03_TRIP01":                58 + 13569,                     # Setpoints.Temperatura03_TRIP01
        "TEMPERATURA_04_TRIP01":                59 + 13569,                     # Setpoints.Temperatura04_TRIP01
        "TEMPERATURA_05_TRIP01":                60 + 13569,                     # Setpoints.Temperatura05_TRIP01
        "TEMPERATURA_06_TRIP01":                61 + 13569,                     # Setpoints.Temperatura06_TRIP01
        "TEMPERATURA_07_TRIP01":                62 + 13569,                     # Setpoints.Temperatura07_TRIP01
        "TEMPERATURA_08_TRIP01":                63 + 13569,                     # Setpoints.Temperatura08_TRIP01
        "TEMPERATURA_09_TRIP01":                64 + 13569,                     # Setpoints.Temperatura09_TRIP01
        "TEMPERATURA_10_TRIP01":                65 + 13569,                     # Setpoints.Temperatura10_TRIP01
        "TEMPERATURA_11_TRIP01":                66 + 13569,                     # Setpoints.Temperatura11_TRIP01
        "TEMPERATURA_12_TRIP01":                67 + 13569,                     # Setpoints.Temperatura12_TRIP01
        "TEMPERATURA_13_TRIP01":                68 + 13569,                     # Setpoints.Temperatura13_TRIP01
        "TEMPERATURA_14_TRIP01":                69 + 13569,                     # Setpoints.Temperatura14_TRIP01
        "TEMPERATURA_15_TRIP01":                70 + 13569,                     # Setpoints.Temperatura15_TRIP01
        "TEMPERATURA_16_TRIP01":                71 + 13569,                     # Setpoints.Temperatura16_TRIP01
        "TEMPERATURA_01_TRIP02":                72 + 13569,                     # Setpoints.Temperatura01_TRIP02
        "TEMPERATURA_02_TRIP02":                73 + 13569,                     # Setpoints.Temperatura02_TRIP02
        "TEMPERATURA_03_TRIP02":                74 + 13569,                     # Setpoints.Temperatura03_TRIP02
        "TEMPERATURA_04_TRIP02":                75 + 13569,                     # Setpoints.Temperatura04_TRIP02
        "TEMPERATURA_05_TRIP02":                76 + 13569,                     # Setpoints.Temperatura05_TRIP02
        "TEMPERATURA_06_TRIP02":                77 + 13569,                     # Setpoints.Temperatura06_TRIP02
        "TEMPERATURA_07_TRIP02":                78 + 13569,                     # Setpoints.Temperatura07_TRIP02
        "TEMPERATURA_08_TRIP02":                79 + 13569,                     # Setpoints.Temperatura08_TRIP02
        "TEMPERATURA_09_TRIP02":                80 + 13569,                     # Setpoints.Temperatura09_TRIP02
        "TEMPERATURA_10_TRIP02":                81 + 13569,                     # Setpoints.Temperatura10_TRIP02
        "TEMPERATURA_11_TRIP02":                82 + 13569,                     # Setpoints.Temperatura11_TRIP02
        "TEMPERATURA_12_TRIP02":                83 + 13569,                     # Setpoints.Temperatura12_TRIP02
        "TEMPERATURA_13_TRIP02":                84 + 13569,                     # Setpoints.Temperatura13_TRIP02
        "TEMPERATURA_14_TRIP02":                85 + 13569,                     # Setpoints.Temperatura14_TRIP02
        "TEMPERATURA_15_TRIP02":                86 + 13569,                     # Setpoints.Temperatura15_TRIP02
        "TEMPERATURA_16_TRIP02":                87 + 13569,                     # Setpoints.Temperatura16_TRIP02

        # Grade Suja
        "GradeSuja_TRIP":                       95 + 13569,                     # Setpoints.GradeSuja_TRIP

        # Curva
        "CURVA_01_DISTRIB_P1":                  96 + 13569,                     # Setpoints.Curva01_DistribuidorP1
        "CURVA_01_DISTRIB_P2":                  97 + 13569,                     # Setpoints.Curva01_DistribuidorP2
        "CURVA_01_DISTRIB_P3":                  98 + 13569,                     # Setpoints.Curva01_DistribuidorP3
        "CURVA_01_DISTRIB_P4":                  99 + 13569,                    # Setpoints.Curva01_DistribuidorP4
        "CURVA_01_DISTRIB_P5":                  100 + 13569,                    # Setpoints.Curva01_DistribuidorP5
        "CURVA_01_DISTRIB_P6":                  101 + 13569,                    # Setpoints.Curva01_DistribuidorP6
        "CURVA_01_DISTRIB_P7":                  102 + 13569,                    # Setpoints.Curva01_DistribuidorP7
        "CURVA_01_DISTRIB_P8":                  103 + 13569,                    # Setpoints.Curva01_DistribuidorP8
        "CURVA_01_DISTRIB_P9":                  104 + 13569,                    # Setpoints.Curva01_DistribuidorP9
        "CURVA_01_DISTRIB_P10":                 105 + 13569,                    # Setpoints.Curva01_DistribuidorP10
        "CURVA_01_ROTOR_P1":                    106 + 13569,                    # Setpoints.Curva01_RotorP1
        "CURVA_01_ROTOR_P2":                    107 + 13569,                    # Setpoints.Curva01_RotorP2
        "CURVA_01_ROTOR_P3":                    108 + 13569,                    # Setpoints.Curva01_RotorP3
        "CURVA_01_ROTOR_P4":                    109 + 13569,                    # Setpoints.Curva01_RotorP4
        "CURVA_01_ROTOR_P5":                    110 + 13569,                    # Setpoints.Curva01_RotorP5
        "CURVA_01_ROTOR_P6":                    111 + 13569,                    # Setpoints.Curva01_RotorP6
        "CURVA_01_ROTOR_P7":                    112 + 13569,                    # Setpoints.Curva01_RotorP7
        "CURVA_01_ROTOR_P8":                    113 + 13569,                    # Setpoints.Curva01_RotorP8
        "CURVA_01_ROTOR_P9":                    114 + 13569,                    # Setpoints.Curva01_RotorP9
        "CURVA_01_ROTOR_P10":                   115 + 13569,                    # Setpoints.Curva01_RotorP10
        "CURVA_02_DISTRIB_P1":                  116 + 13569,                    # Setpoints.Curva02_DistribuidorP1
        "CURVA_02_DISTRIB_P2":                  117 + 13569,                    # Setpoints.Curva02_DistribuidorP2
        "CURVA_02_DISTRIB_P3":                  118 + 13569,                    # Setpoints.Curva02_DistribuidorP3
        "CURVA_02_DISTRIB_P4":                  119 + 13569,                    # Setpoints.Curva02_DistribuidorP4
        "CURVA_02_DISTRIB_P5":                  120 + 13569,                    # Setpoints.Curva02_DistribuidorP5
        "CURVA_02_DISTRIB_P6":                  121 + 13569,                    # Setpoints.Curva02_DistribuidorP6
        "CURVA_02_DISTRIB_P7":                  122 + 13569,                    # Setpoints.Curva02_DistribuidorP7
        "CURVA_02_DISTRIB_P8":                  123 + 13569,                    # Setpoints.Curva02_DistribuidorP8
        "CURVA_02_DISTRIB_P9":                  124 + 13569,                    # Setpoints.Curva02_DistribuidorP9
        "CURVA_02_DISTRIB_P10":                 125 + 13569,                    # Setpoints.Curva02_DistribuidorP10
        "CURVA_02_ROTOR_P1":                    126 + 13569,                    # Setpoints.Curva02_RotorP1
        "CURVA_02_ROTOR_P2":                    127 + 13569,                    # Setpoints.Curva02_RotorP2
        "CURVA_02_ROTOR_P3":                    128 + 13569,                    # Setpoints.Curva02_RotorP3
        "CURVA_02_ROTOR_P4":                    129 + 13569,                    # Setpoints.Curva02_RotorP4
        "CURVA_02_ROTOR_P5":                    130 + 13569,                    # Setpoints.Curva02_RotorP5
        "CURVA_02_ROTOR_P6":                    131 + 13569,                    # Setpoints.Curva02_RotorP6
        "CURVA_02_ROTOR_P7":                    132 + 13569,                    # Setpoints.Curva02_RotorP7
        "CURVA_02_ROTOR_P8":                    133 + 13569,                    # Setpoints.Curva02_RotorP8
        "CURVA_02_ROTOR_P9":                    134 + 13569,                    # Setpoints.Curva02_RotorP9
        "CURVA_02_ROTOR_P10":                   135 + 13569,                    # Setpoints.Curva02_RotorP10
        "CURVA_03_DISTRIB_P1":                  136 + 13569,                    # Setpoints.Curva03_DistribuidorP1
        "CURVA_03_DISTRIB_P2":                  137 + 13569,                    # Setpoints.Curva03_DistribuidorP2
        "CURVA_03_DISTRIB_P3":                  138 + 13569,                    # Setpoints.Curva03_DistribuidorP3
        "CURVA_03_DISTRIB_P4":                  139 + 13569,                    # Setpoints.Curva03_DistribuidorP4
        "CURVA_03_DISTRIB_P5":                  140 + 13569,                    # Setpoints.Curva03_DistribuidorP5
        "CURVA_03_DISTRIB_P6":                  141 + 13569,                    # Setpoints.Curva03_DistribuidorP6
        "CURVA_03_DISTRIB_P7":                  142 + 13569,                    # Setpoints.Curva03_DistribuidorP7
        "CURVA_03_DISTRIB_P8":                  143 + 13569,                    # Setpoints.Curva03_DistribuidorP8
        "CURVA_03_DISTRIB_P9":                  144 + 13569,                    # Setpoints.Curva03_DistribuidorP9
        "CURVA_03_DISTRIB_P10":                 145 + 13569,                    # Setpoints.Curva03_DistribuidorP10
        "CURVA_03_ROTOR_P1":                    146 + 13569,                    # Setpoints.Curva03_RotorP1
        "CURVA_03_ROTOR_P2":                    147 + 13569,                    # Setpoints.Curva03_RotorP2
        "CURVA_03_ROTOR_P3":                    148 + 13569,                    # Setpoints.Curva03_RotorP3
        "CURVA_03_ROTOR_P4":                    149 + 13569,                    # Setpoints.Curva03_RotorP4
        "CURVA_03_ROTOR_P5":                    150 + 13569,                    # Setpoints.Curva03_RotorP5
        "CURVA_03_ROTOR_P6":                    151 + 13569,                    # Setpoints.Curva03_RotorP6
        "CURVA_03_ROTOR_P7":                    152 + 13569,                    # Setpoints.Curva03_RotorP7
        "CURVA_03_ROTOR_P8":                    153 + 13569,                    # Setpoints.Curva03_RotorP8
        "CURVA_03_ROTOR_P9":                    154 + 13569,                    # Setpoints.Curva03_RotorP9
        "CURVA_03_ROTOR_P10":                   155 + 13569,                    # Setpoints.Curva03_RotorP10
        "CURVA_04_DISTRIB_P1":                  156 + 13569,                    # Setpoints.Curva04_DistribuidorP1
        "CURVA_04_DISTRIB_P2":                  157 + 13569,                    # Setpoints.Curva04_DistribuidorP2
        "CURVA_04_DISTRIB_P3":                  158 + 13569,                    # Setpoints.Curva04_DistribuidorP3
        "CURVA_04_DISTRIB_P4":                  159 + 13569,                    # Setpoints.Curva04_DistribuidorP4
        "CURVA_04_DISTRIB_P5":                  160 + 13569,                    # Setpoints.Curva04_DistribuidorP5
        "CURVA_04_DISTRIB_P6":                  161 + 13569,                    # Setpoints.Curva04_DistribuidorP6
        "CURVA_04_DISTRIB_P7":                  162 + 13569,                    # Setpoints.Curva04_DistribuidorP7
        "CURVA_04_DISTRIB_P8":                  163 + 13569,                    # Setpoints.Curva04_DistribuidorP8
        "CURVA_04_DISTRIB_P9":                  164 + 13569,                    # Setpoints.Curva04_DistribuidorP9
        "CURVA_04_DISTRIB_P10":                 165 + 13569,                    # Setpoints.Curva04_DistribuidorP10
        "CURVA_04_ROTOR_P1":                    166 + 13569,                    # Setpoints.Curva04_RotorP1
        "CURVA_04_ROTOR_P2":                    167 + 13569,                    # Setpoints.Curva04_RotorP2
        "CURVA_04_ROTOR_P3":                    168 + 13569,                    # Setpoints.Curva04_RotorP3
        "CURVA_04_ROTOR_P4":                    169 + 13569,                    # Setpoints.Curva04_RotorP4
        "CURVA_04_ROTOR_P5":                    170 + 13569,                    # Setpoints.Curva04_RotorP5
        "CURVA_04_ROTOR_P6":                    171 + 13569,                    # Setpoints.Curva04_RotorP6
        "CURVA_04_ROTOR_P7":                    172 + 13569,                    # Setpoints.Curva04_RotorP7
        "CURVA_04_ROTOR_P8":                    173 + 13569,                    # Setpoints.Curva04_RotorP8
        "CURVA_04_ROTOR_P9":                    174 + 13569,                    # Setpoints.Curva04_RotorP9
        "CURVA_04_ROTOR_P10":                   175 + 13569,                    # Setpoints.Curva04_RotorP10
        "CURVA_05_DISTRIB_P1":                  176 + 13569,                    # Setpoints.Curva05_DistribuidorP1
        "CURVA_05_DISTRIB_P2":                  177 + 13569,                    # Setpoints.Curva05_DistribuidorP2
        "CURVA_05_DISTRIB_P3":                  178 + 13569,                    # Setpoints.Curva05_DistribuidorP3
        "CURVA_05_DISTRIB_P4":                  179 + 13569,                    # Setpoints.Curva05_DistribuidorP4
        "CURVA_05_DISTRIB_P5":                  180 + 13569,                    # Setpoints.Curva05_DistribuidorP5
        "CURVA_05_DISTRIB_P6":                  181 + 13569,                    # Setpoints.Curva05_DistribuidorP6
        "CURVA_05_DISTRIB_P7":                  182 + 13569,                    # Setpoints.Curva05_DistribuidorP7
        "CURVA_05_DISTRIB_P8":                  183 + 13569,                    # Setpoints.Curva05_DistribuidorP8
        "CURVA_05_DISTRIB_P9":                  184 + 13569,                    # Setpoints.Curva05_DistribuidorP9
        "CURVA_05_DISTRIB_P10":                 185 + 13569,                    # Setpoints.Curva05_DistribuidorP10
        "CURVA_05_ROTOR_P1":                    186 + 13569,                    # Setpoints.Curva05_RotorP1
        "CURVA_05_ROTOR_P2":                    187 + 13569,                    # Setpoints.Curva05_RotorP2
        "CURVA_05_ROTOR_P3":                    188 + 13569,                    # Setpoints.Curva05_RotorP3
        "CURVA_05_ROTOR_P4":                    189 + 13569,                    # Setpoints.Curva05_RotorP4
        "CURVA_05_ROTOR_P5":                    190 + 13569,                    # Setpoints.Curva05_RotorP5
        "CURVA_05_ROTOR_P6":                    191 + 13569,                    # Setpoints.Curva05_RotorP6
        "CURVA_05_ROTOR_P7":                    192 + 13569,                    # Setpoints.Curva05_RotorP7
        "CURVA_05_ROTOR_P8":                    193 + 13569,                    # Setpoints.Curva05_RotorP8
        "CURVA_05_ROTOR_P9":                    194 + 13569,                    # Setpoints.Curva05_RotorP9
        "CURVA_05_ROTOR_P10":                   195 + 13569,                    # Setpoints.Curva05_RotorP10

        # Referencia Curva
        "REFER_CURVA_01":                       196 + 13569,                    # Setpoints.ReferenciaCurva01
        "REFER_CURVA_02":                       197 + 13569,                    # Setpoints.ReferenciaCurva02
        "REFER_CURVA_03":                       198 + 13569,                    # Setpoints.ReferenciaCurva03
        "REFER_CURVA_04":                       199 + 13569,                    # Setpoints.ReferenciaCurva04
        "REFER_CURVA_05":                       200 + 13569,                    # Setpoints.ReferenciaCurva05

        # Outros
        "TEMPO_ATUALIZACAO":                    201 + 13569,                    # Setpoints.TempoAtualizacao
        "MODO_OPERACAO_RETENTIVO":              202 + 13569,                    # Setpoints.ModoOperacao_Retentivo
        "CURVA_SEL_RETENTIVO":                  203 + 13569,                    # Setpoints.CurvaSelecionada_Retentivo


        ## LEITURAS

        # Nível
        "NV_JUSANTE":                           1 + 12764,                      # Leituras.NivelJusante
        "NV_BARRAGEM":                          2 + 12764,                      # Leituras.NivelBarragem
        "NV_CANAL":                             3 + 12764,                      # Leituras.NivelCanal
        "NV_CAMARA_CARGA":                      4 + 12764,                      # Leituras.NivelCamaraCarga
        "QUEDA_BRUTA":                          130 + 12764,                    # Leituras.QuedaBruta

        # Operação
        "OPER_PAINEL_RESET_ALARMES":            [5 + 12764, 0],                 # Leituras.Operacao_PainelResetAlarmes
        "OPER_PAINEL_RECONHECE_ALARMES":        [6 + 12764, 1],                 # Leituras.Operacao_PainelReconheceAlarmes

        "OPER_INFO":                            8 + 12764,                      # Leituras.Operacao_Info
        "OPER_EMERGENCIA":                      [8 + 12764, 0],                 # Operacao.Info.Emergencia
        "OPER_SIRENE_LIGADA":                   [8 + 12764, 1],                 # Operacao.Info.SireneLigada
        "OPER_MODO_REMOTO":                     [8 + 12764, 2],                 # Operacao.Info.OperacaoModoRemoto
        "OPER_MODO_LOCAL":                      [8 + 12764, 3],                 # Operacao.Info.OperacaoModoLocal

        "OPER_ETAPA_ALVO":                      9 + 12764,                      # Leituras.Operacao_EtapaAlvo
        "OPER_ETAPA_ALVO_UP":                   [9 + 12764, 0],                 # Operacao.EtapaAlvo.UP
        "OPER_ETAPA_ALVO_UPGM":                 [9 + 12764, 1],                 # Operacao.EtapaAlvo.UPGM
        "OPER_ETAPA_ALVO_UMD":                  [9 + 12764, 2],                 # Operacao.EtapaAlvo.UMD
        "OPER_ETAPA_ALVO_UPS":                  [9 + 12764, 3],                 # Operacao.EtapaAlvo.UPS
        "OPER_ETAPA_ALVO_US":                   [9 + 12764, 4],                 # Operacao.EtapaAlvo.US

        "OPER_ETAPA_ATUAL":                     10 + 12764,                     # Leituras.Operacao_EtapaAtual
        "OPER_ETAPA_ATUAL_UP":                  [10 + 12764, 0],                # Operacao.EtapaAtual.UP
        "OPER_ETAPA_ATUAL_UPGM":                [10 + 12764, 1],                # Operacao.EtapaAtual.UPGM
        "OPER_ETAPA_ATUAL_UMD":                 [10 + 12764, 2],                # Operacao.EtapaAtual.UMD
        "OPER_ETAPA_ATUAL_UPS":                 [10 + 12764, 3],                # Operacao.EtapaAtual.UPS
        "OPER_ETAPA_ATUAL_US":                  [10 + 12764, 4],                # Operacao.EtapaAtual.US

        "OPER_ETAPA_TRANSICAO":                 11 + 12764,                     # Leituras.Operacao_EtapaTransicao
        "OPER_ETAPA_TRANS_UP_UPGM":             [11 + 12764, 0],                # Operacao.EtapaTransicao.UPtoUPGM
        "OPER_ETAPA_TRANS_UPGM_UMD":            [11 + 12764, 1],                # Operacao.EtapaTransicao.UPGMtoUMD
        "OPER_ETAPA_TRANS_UMD_UPS":             [11 + 12764, 2],                # Operacao.EtapaTransicao.UMDtoUPS
        "OPER_ETAPA_TRANS_UPS_US":              [11 + 12764, 3],                # Operacao.EtapaTransicao.UPStoUS
        "OPER_ETAPA_TRANS_US_UPS":              [11 + 12764, 4],                # Operacao.EtapaTransicao.UStoUPS
        "OPER_ETAPA_TRANS_UPS_UMD":             [11 + 12764, 5],                # Operacao.EtapaTransicao.UPStoUMD
        "OPER_ETAPA_TRANS_UMD_UPGM":            [11 + 12764, 6],                # Operacao.EtapaTransicao.UMDtoUPGM
        "OPER_ETAPA_TRANS_UPGM_UP":             [11 + 12764, 7],                # Operacao.EtapaTransicao.UPGMtoUP

        "OPER_INFO_PARADA":                     11 + 12764,                     # Leituras.Operacao_InfoParada
        "OPER_INFO_PARADA_NORMAL":              [11 + 12764, 0],                # Operacao.InfoParada.Normal
        "OPER_INFO_PARADA_EMERG":               [11 + 12764, 1],                # Operacao.InfoParada.Emergencia
        "OPER_INFO_PARADA_TRIP_AGUA":           [11 + 12764, 2],                # Operacao.InfoParada.TRIPAgua
        "OPER_INFO_PARADA_TRIP_M":              [11 + 12764, 3],                # Operacao.InfoParada.TRIPMecanico
        "OPER_INFO_PARADA_TRIP_E":              [11 + 12764, 4],                # Operacao.InfoParada.TRIPEletrico
        "OPER_INFO_PARADA_TRIP_H":              [11 + 12764, 5],                # Operacao.InfoParada.TRIPHidraulico
        "OPER_INFO_PARADA_RELIG_AUTO":          [11 + 12764, 6],                # Operacao.InfoParada.ReligamentoAutomatico
        "OPER_INFO_PARADA_PARTIDA_MANU":        [11 + 12764, 7],                # Operacao.InfoParada.PartidaManual
        "OPER_INFO_PARADA_INFO_INVAL":          [11 + 12764, 15],               # Operacao.InfoParada.ParadaInfoValida

        # UHCT
        "UHCT_INFO":                            12 + 12764,                     # Leituras.UHCT_Info
        "UHCT_OPERACIONAL":                     [12 + 12764, 0],                # UHCT.Info.Operacional
        "UHCT_LIGADA":                          [12 + 12764, 1],                # UHCT.Info.Ligada
        "UHCT_SENS_DESATIVADO":                 [12 + 12764, 2],                # UHCT.Info.SensorDesativado
        "UHCT_MODO_LOCAL":                      [12 + 12764, 3],                # UHCT.Info.ModoLocal

        "UHCT_BOMBAS":                          13 + 12764,                     # Leituras.UHCT_Bombas
        "UHCT_BOMBAS01":                        [13 + 12764, 0],                # UHCT.Bombas.Bomba01
        "UHCT_BOMBAS02":                        [13 + 12764, 1],                # UHCT.Bombas.Bomba02
        "UHCT_BOMBAS03":                        [13 + 12764, 2],                # UHCT.Bombas.Bomba03

        "UHCT_RODIZIO":                         14 + 12764,                     # Leituras.UHCT_Rodizio
        "UHCT_RODIZ_HABILITADO":                [14 + 12764, 0],                # UHCT.Rodizio.RodizioHabilitado
        "UHCT_RODIZ_BOMBA01":                   [14 + 12764, 1],                # UHCT.Rodizio.Bomba01
        "UHCT_RODIZ_BOMBA02":                   [14 + 12764, 2],                # UHCT.Rodizio.Bomba02

        "UHCT_VALVULAS":                        15 + 12764,                     # Leituras.UHCT_Valvulas
        "UHCT_VALVULAS01":                      [15 + 12764, 0],                # UHCT.Valvulas.Valvulas01
        "UHCT_VALVULAS02":                      [15 + 12764, 1],                # UHCT.Valvulas.Valvulas02
        "UHCT_VALVULAS03":                      [15 + 12764, 2],                # UHCT.Valvulas.Valvulas03
        "UHCT_VALVULAS04":                      [15 + 12764, 3],                # UHCT.Valvulas.Valvulas04

        "UHCT_FILTROS":                         16 + 12764,                     # Leituras.UHCT_Filtros
        "UHCT_FILTROS01":                       [16 + 12764, 0],                # UHCT.Filtros.Filtro01
        "UHCT_FILTROS02":                       [16 + 12764, 1],                # UHCT.Filtros.Filtro02
        "UHCT_FILTROS03":                       [16 + 12764, 2],                # UHCT.Filtros.Filtro03
        "UHCT_FILTROS04":                       [16 + 12764, 3],                # UHCT.Filtros.Filtro04
        "UHCT_FILTROS05":                       [16 + 12764, 4],                # UHCT.Filtros.Filtro05

        "UHCT_PRESSOSTATOS":                    17 + 12764,                     # Leituras.UHCT_Pressostatos
        "UHCT_PRESSOSTATO01":                   [17 + 12764, 0],                # UHCT.Pressostatos.Pressostato01
        "UHCT_PRESSOSTATO02":                   [17 + 12764, 1],                # UHCT.Pressostatos.Pressostato02
        "UHCT_PRESSOSTATO03":                   [17 + 12764, 2],                # UHCT.Pressostatos.Pressostato03

        "UHCT_NIVEL_OLEO":                      18 + 12764,                     # Leituras.UHCT_NivelOleo
        "UHCT_NIVEL_OLEO_LL":                   [18 + 12764, 0],                # UHCT.NivelOleo.LL
        "UHCT_NIVEL_OLEO_L":                    [18 + 12764, 1],                # UHCT.NivelOleo.L
        "UHCT_NIVEL_OLEO_H":                    [18 + 12764, 2],                # UHCT.NivelOleo.H
        "UHCT_NIVEL_OLEO_HH":                   [18 + 12764, 3],                # UHCT.NivelOleo.HH

        "UHCT_PRESSAO_OLEO":                    19 + 12764,                     # Leituras.UHCT_PressaoOleo
        "UHCT_ACUM_RODIZIO_PRINCIPAL":          20 + 12764,                     # Leituras.UHCT_AcumuladorRodizioPrincipal
        "UHCT_ACUM_RODIZIO_RETAGUARDA":         21 + 12764,                     # Leituras.UHCT_AcumuladorRodizioRetaguarda

        # UHLM
        "UHLM_INFO":                            22 + 12764,                     # Leituras.UHLM_Info
        "UHLM_OPERACIONAL":                     [22 + 12764, 0],                # UHLM.Info.Operacional
        "UHLM_LIGADA":                          [22 + 12764, 1],                # UHLM.Info.Ligada
        "UHLM_MODO_LOCAL":                      [22 + 12764, 2],                # UHLM.Info.ModoLocal
        "UHLM_VALV_BOMBA_MECAN":                [22 + 12764, 3],                # UHLM.Info.UHLM_ValvulaBombaMecanica
        "UHLM_VALV_ENTRA_TRO_CALO_ABER":        [22 + 12764, 4],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Aberta
        "UHLM_VALV_ENTRA_TRO_CALO_FECH":        [22 + 12764, 5],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Fechada
        "UHLM_VALV_SAI_TRO_CALO_ABER":          [22 + 12764, 6],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Aberta
        "UHLM_VALV_SAI_TRO_CALO_FECH":          [22 + 12764, 7],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Fechada
        "UHLM_BOMBA_RETAG_OPERAC":              [22 + 12764, 8],                # UHLM.Info.UHLM_BombaRetaguarda_Operacional

        "UHLM_BOMBAS":                          23 + 12764,                     # Leituras.UHLM_Bombas
        "UHLM_BOMBA01":                         [23 + 12764, 0],                # UHLM.Bombas.Bomba01
        "UHLM_BOMBA02":                         [23 + 12764, 1],                # UHLM.Bombas.Bomba02
        "UHLM_BOMBA03":                         [23 + 12764, 2],                # UHLM.Bombas.Bomba03
        "UHLM_BOMBA04":                         [23 + 12764, 3],                # UHLM.Bombas.Bomba04

        "UHLM_RODIZIO":                         24 + 12764,                     # Leituras.UHLM_Rodizio
        "UHLM_RODIZ_HABILITADO":                [24 + 12764, 0],                # UHLM.Rodizio.RodizioHabilitado
        "UHLM_RODIZ_BOMBA01":                   [24 + 12764, 1],                # UHLM.Rodizio.Bomba01
        "UHLM_RODIZ_BOMBA02":                   [24 + 12764, 2],                # UHLM.Rodizio.Bomba02

        "UHLM_FILTROS":                         25 + 12764,                     # Leituras.UHLM_Filtros
        "UHLM_FILTRO01":                        [25 + 12764, 0],                # UHLM.Filtros.Filtro01
        "UHLM_FILTRO02":                        [25 + 12764, 1],                # UHLM.Filtros.Filtro02
        "UHLM_FILTRO03":                        [25 + 12764, 2],                # UHLM.Filtros.Filtro03
        "UHLM_FILTRO04":                        [25 + 12764, 3],                # UHLM.Filtros.Filtro04
        "UHLM_FILTRO05":                        [25 + 12764, 4],                # UHLM.Filtros.Filtro05

        "UHLM_PRESSOSTATOS":                    26 + 12764,                     # Leituras.UHLM_Pressostatos
        "UHLM_PRESSOSTATO01":                   [26 + 12764, 0],                # UHLM.Pressostatos.Pressostato01
        "UHLM_PRESSOSTATO02":                   [26 + 12764, 1],                # UHLM.Pressostatos.Pressostato02
        "UHLM_PRESSOSTATO03":                   [26 + 12764, 2],                # UHLM.Pressostatos.Pressostato03
        "UHLM_PRESSOSTATO04":                   [26 + 12764, 3],                # UHLM.Pressostatos.Pressostato04

        "UHLM_FLUXOSTATOS":                     27 + 12764,                     # Leituras.UHLM_Fluxostatos
        "UHLM_FLUXOSTATO01":                    [27 + 12764, 0],                # UHLM.Fluxostatos.Fluxostato01
        "UHLM_FLUXOSTATO02":                    [27 + 12764, 1],                # UHLM.Fluxostatos.Fluxostato02
        "UHLM_FLUXOSTATO03":                    [27 + 12764, 2],                # UHLM.Fluxostatos.Fluxostato03
        "UHLM_FLUXOSTATO04":                    [27 + 12764, 3],                # UHLM.Fluxostatos.Fluxostato04
        "UHLM_FLUXOSTATO05":                    [27 + 12764, 4],                # UHLM.Fluxostatos.Fluxostato05
        "UHLM_FLUXOSTATO06":                    [27 + 12764, 5],                # UHLM.Fluxostatos.Fluxostato06
        "UHLM_FLUXOSTATO07":                    [27 + 12764, 6],                # UHLM.Fluxostatos.Fluxostato07

        "UHLM_NIVEL_OLEO":                      28 + 12764,                     # Leituras.UHLM_NivelOleo
        "UHLM_NIVEL_OLEO_LL":                   [28 + 12764, 0],                # UHLM.NivelOleo.LL
        "UHLM_NIVEL_OLEO_L":                    [28 + 12764, 1],                # UHLM.NivelOleo.L
        "UHLM_NIVEL_OLEO_H":                    [28 + 12764, 2],                # UHLM.NivelOleo.H
        "UHLM_NIVEL_OLEO_HH":                   [28 + 12764, 3],                # UHLM.NivelOleo.HH

        "UHLM_ACUM_RODIZIO_PRINCIPAL":          29 + 12764,                     # Leituras.UHLM_AcumuladorRodizioPrincipal
        "UHLM_ACUM_RODIZIO_RETAGUARDA":         30 + 12764,                     # Leituras.UHLM_AcumuladorRodizioRetaguarda

        "UHLM_FLUXOSTATO_OLEO_01":              122 + 12764,                    # Leituras.UHLM_FluxostatoOleo01
        "UHLM_FLUXOSTATO_OLEO_02":              123 + 12764,                    # Leituras.UHLM_FluxostatoOleo02
        "UHLM_FLUXOSTATO_OLEO_03":              124 + 12764,                    # Leituras.UHLM_FluxostatoOleo03
        "UHLM_FLUXOSTATO_OLEO_04":              125 + 12764,                    # Leituras.UHLM_FluxostatoOleo04

        # Turbina
        "TURB_INFO":                            31 + 12764,                     # Leituras.Turb_Info
        "TURB_EQUALIZADA":                      [31 + 12764, 0],                # Turbina.Info.Equalizada
        "TURB_PRONTA":                          [31 + 12764, 1],                # Turbina.Info.Pronta
        "TURB_FECHADA":                         [31 + 12764, 2],                # Turbina.Info.Fechada
        "TURB_TRAVADA":                         [31 + 12764, 3],                # Turbina.Info.Travada
        "TURB_PARADA":                          [31 + 12764, 4],                # Turbina.Info.Parada
        "TURB_EQUALIZANDO":                     [31 + 12764, 5],                # Turbina.Info.Equalizando
        "TURB_FECHANDO":                        [31 + 12764, 6],                # Turbina.Info.Fechando
        "TURB_SENS_DESATIVADO":                 [31 + 12764, 7],                # Turbina.Info.SensorDesativado
        "TURB_DISTRI_FECHADO":                  [31 + 12764, 8],                # Turbina.Info.DistribuidorFechado

        "TURB_VALVULA_BYPASS":                  32 + 12764,                     # Leituras.Turb_ValvulaByPass
        "TURB_VALV_BY_ACIONA":                  [32 + 12764, 0],                # Turbina.Bypass.Acionamento
        "TURB_VALV_BY_FECHADO":                 [32 + 12764, 1],                # Turbina.Bypass.Fechado
        "TURB_VALV_BY_ABERTO":                  [32 + 12764, 2],                # Turbina.Bypass.Aberto

        "TURB_VALVULA_BORBOLETA":               33 + 12764,                     # Leituras.Turb_ValvulaBorboleta
        "TURB_VALV_BORB_ACIONA":                [33 + 12764, 0],                # Turbina.Borboleta.Acionamento
        "TURB_VALV_BORB_FECHADA":               [33 + 12764, 1],                # Turbina.Borboleta.Fechada
        "TURB_VALV_BORB_ABERTA":                [33 + 12764, 2],                # Turbina.Borboleta.Aberta
        "TURB_VALV_BORB_DERIVA":                [33 + 12764, 3],                # Turbina.Borboleta.Deriva
        "TURB_VALV_BORB_TRAVADA":               [33 + 12764, 4],                # Turbina.Borboleta.Travada
        "TURB_VALV_BORB_MANTEM":                [33 + 12764, 5],                # Turbina.Borboleta.Mantem

        "TURB_TEMPO_CRACK_EFETIVO":             34 + 12764,                     # Leituras.Turb_TempoCrackEfetivo
        "TURB_TEMPO_EQUAL_EFETIVO":             35 + 12764,                     # Leituras.Turb_TempoEqualizacaoEfetivo
        "TURB_PRESSAO_CONDUTO":                 36 + 12764,                     # Leituras.Turb_PressaoConduto
        "TURB_PRESSAO_CAIXA_ESPIRAL":           37 + 12764,                     # Leituras.Turb_PressaoCaixaEspiral
        "TURB_VAZAO_TURBINADA":                 38 + 12764,                     # Leituras.Turb_VazaoTurbinada
        "TURB_VIBRACAO_01":                     39 + 12764,                     # Leituras.Turb_Vibracao01
        "TURB_VIBRACAO_02":                     40 + 12764,                     # Leituras.Turb_Vibracao02
        "TURB_VIBRACAO_03":                     41 + 12764,                     # Leituras.Turb_Vibracao03
        "TURB_VIBRACAO_04":                     42 + 12764,                     # Leituras.Turb_Vibracao04

        "TURB_FRENAGEM":                        43 + 12764,                     # Leituras.Turb_Frenagem
        "TURB_FRENA_APLICADO":                  [43 + 12764, 0],                # Turbina.Frenagem.Info.Aplicado
        "TURB_FRENA_MANUAL":                    [43 + 12764, 1],                # Turbina.Frenagem.Info.Manual
        "TURB_FRENA_PRESSOS":                   [43 + 12764, 2],                # Turbina.Frenagem.Info.Pressostato
        "TURB_FRENA_1ZE":                       [43 + 12764, 3],                # Turbina.Frenagem.Info.[1ZE]
        "TURB_FRENA_2ZE":                       [43 + 12764, 4],                # Turbina.Frenagem.Info.[2ZE]

        "TURB_VIBRACAO_05":                     128 + 12764,                    # Leituras.Turb_Vibracao05

        # Reg V
        "REG_V_INFO":                           44 + 12764,                     # Leituras.RegV_Info
        "REG_V_HABILITADO":                     [44 + 12764, 0],                # RegV.Info.Habilitado
        "REG_V_BASE_CARGA":                     [44 + 12764, 1],                # RegV.Info.BaseCarga
        "REG_V_RPM30":                          [44 + 12764, 2],                # RegV.Info.RPM30
        "REG_V_RPM90":                          [44 + 12764, 3],                # RegV.Info.RPM90
        "REG_V_CARGA_ZERADA":                   [44 + 12764, 4],                # RegV.Info.CargaZerada
        "REG_V_MODO_ESTATISMO":                 [44 + 12764, 5],                # RegV.Info.ModoEstatismo
        "REG_V_MODO_BASE_CARGA":                [44 + 12764, 6],                # RegV.Info.ModoBaseCarga
        "REG_V_DISTRI_FECHADO":                 [44 + 12764, 7],                # RegV.Info.DistribuidorFechado

        "REG_V_ESTADO":                         45 + 12764,                     # Leituras.RegV_Estado
        "REG_V_FALHA":                          [45 + 12764, 0],                # RegV.Estado.Falha
        "REG_V_PARADO":                         [45 + 12764, 1],                # RegV.Estado.Parado
        "REG_V_CTRL_MANUAL_DISTRI":             [45 + 12764, 2],                # RegV.Estado.ControleManualDistribuidor
        "REG_V_CTRL_MANUAL_VALV":               [45 + 12764, 3],                # RegV.Estado.ControleManualValvula
        "REG_V_CTRL_VELOC":                     [45 + 12764, 4],                # RegV.Estado.ControleVelocidade
        "REG_V_COMPENSA_POT_ATIVA":             [45 + 12764, 5],                # RegV.Estado.CompensacaoPotenciaAtiva
        "REG_V_CTRL_POT_ATIVA":                 [45 + 12764, 6],                # RegV.Estado.ControlePotenciaAtiva

        "REG_V_VELOCIDADE":                     46 + 12764,                     # Leituras.RegV_Velocidade
        "REG_V_DISTRIBUIDOR":                   47 + 12764,                     # Leituras.RegV_Distribuidor
        "REG_V_ROTOR":                          48 + 12764,                     # Leituras.RegV_Rotor
        "REG_V_POT_ALVO":                       49 + 12764,                     # Leituras.RegV_PotenciaAlvo

        "REG_V_CONJUGADO_INFO":                 127 + 12764,                    # Leituras.RegV_CurvaConjugacao_Info
        "REG_V_CONJ_AUTOMATICO":                [127 + 12764, 0],               # RegV.Conjugado.Automatico
        "REG_V_CONJ_MANUAL":                    [127 + 12764, 1],               # RegV.Conjugado.Manual
        "REG_V_CONJUGADO1":                     [127 + 12764, 2],               # RegV.Conjugado.Conjugado1
        "REG_V_CONJUGADO2":                     [127 + 12764, 3],               # RegV.Conjugado.Conjugado2
        "REG_V_CONJUGADO3":                     [127 + 12764, 4],               # RegV.Conjugado.Conjugado3

        # Reg T
        "REG_T_INFO":                           50 + 12764,                     # Leituras.RegT_Info
        "REG_T_HABILITACAO":                    [50 + 12764, 0],                # RegT.Info.Habilitacao
        "REG_T_TENSAO_ESTAB":                   [50 + 12764, 1],                # RegT.Info.TensaoEstabilizada
        "REG_T_CONTATOR_ABERTO":                [50 + 12764, 2],                # RegT.Info.ContatorAberto
        "REG_T_CONTATOR_FECHADO":               [50 + 12764, 3],                # RegT.Info.ContatorFechado
        "REG_T_PRE_EXCITACAO":                  [50 + 12764, 4],                # RegT.Info.PreExcitacao
        "REG_T_MTVC":                           [50 + 12764, 5],                # RegT.Info.MTVC
        "REG_T_MECC":                           [50 + 12764, 6],                # RegT.Info.MECC
        "REG_T_OPER_ONLINE":                    [50 + 12764, 7],                # RegT.Info.OperacaoOnline
        "REG_T_OPER_PARALELA":                  [50 + 12764, 9],                # RegT.Info.OperacaoParalela

        "REG_T_UEXCITACAO":                     51 + 12764,                     # Leituras.RegT_UExcitacao
        "REG_T_IEXCITACAO":                     52 + 12764,                     # Leituras.RegT_IExcitacao
        "REG_T_FPALVO":                         128 + 12764,                    # Leituras.RegT_FPAlvo
        "REG_T_REATIVO_ALVO":                   129 + 12764,                    # Leituras.RegT_ReativoAlvo

        # Sinc
        "SINC_INFO":                            53 + 12764,                     # Leituras.Sinc_Info
        "SINC_HABILITADO":                      [53 + 12764, 0],                # Sincronoscopio.Info.Habilitado
        "SINC_MODO_AUTO":                       [53 + 12764, 1],                # Sincronoscopio.Info.ModoAutomatico
        "SINC_MODO_MANUAL":                     [53 + 12764, 2],                # Sincronoscopio.Info.ModoManual
        "SINC_BARRA_MORTA":                     [53 + 12764, 3],                # Sincronoscopio.Info.BarraMorta

        "SINC_FREQ_GERADOR":                    54 + 12764,                     # Leituras.Sinc_FrequenciaGerador
        "SINC_FREQ_BARRA":                      55 + 12764,                     # Leituras.Sinc_FrequenciaBarra
        "SINC_TENSAO_GERADOR":                  56 + 12764,                     # Leituras.Sinc_TensaoGerador
        "SINC_TENSAO_BARRA":                    57 + 12764,                     # Leituras.Sinc_TensaoBarra

        # DJ
        "Dj52G_INFO":                           58 + 12764,                     # Leituras.Disj52G_Info
        "Dj52G_ABERTO":                         [58 + 12764, 0],                # Disjuntor52G.Info.Aberto
        "Dj52G_FECHADO":                        [58 + 12764, 1],                # Disjuntor52G.Info.Fechado
        "Dj52G_INCONSISTENTE":                  [58 + 12764, 2],                # Disjuntor52G.Info.Inconsistente
        "Dj52G_TRIP":                           [58 + 12764, 3],                # Disjuntor52G.Info.TRIP
        "Dj52G_TESTE":                          [58 + 12764, 4],                # Disjuntor52G.Info.Teste
        "Dj52G_INSERIDO":                       [58 + 12764, 5],                # Disjuntor52G.Info.Inserido
        "Dj52G_EXTRAIVEL":                      [58 + 12764, 6],                # Disjuntor52G.Info.Extraivel
        "Dj52G_MOLA_CARRE":                     [58 + 12764, 7],                # Disjuntor52G.Info.MolaCarregada
        "Dj52G_CONDICAO":                       [58 + 12764, 8],                # Disjuntor52G.Info.CondicaoFechamento
        "Dj52G_FALTA_VCC":                      [58 + 12764, 9],                # Disjuntor52G.Info.FaltaVCC

        # Tensão
        "TENSAO_RN":                            59 + 12764,                     # Leituras.Gerador_TensaoRN
        "TENSAO_SN":                            60 + 12764,                     # Leituras.Gerador_TensaoSN
        "TENSAO_TN":                            61 + 12764,                     # Leituras.Gerador_TensaoTN
        "TENSAO_RS":                            62 + 12764,                     # Leituras.Gerador_TensaoRS
        "TENSAO_ST":                            63 + 12764,                     # Leituras.Gerador_TensaoST
        "TENSAO_TR":                            64 + 12764,                     # Leituras.Gerador_TensaoTR

        # Corrente
        "CORRENTE_R":                           65 + 12764,                     # Leituras.Gerador_CorrenteR
        "CORRENTE_S":                           66 + 12764,                     # Leituras.Gerador_CorrenteS
        "CORRENTE_T":                           67 + 12764,                     # Leituras.Gerador_CorrenteT
        "CORRENTE_MEDIA":                       68 + 12764,                     # Leituras.Gerador_CorrenteMedia

        # Potência Ativa
        "POT_ATIVA_1":                          69 + 12764,                     # Leituras.Gerador_PotenciaAtiva1
        "POT_ATIVA_2":                          70 + 12764,                     # Leituras.Gerador_PotenciaAtiva2
        "POT_ATIVA_3":                          71 + 12764,                     # Leituras.Gerador_PotenciaAtiva3
        "POT_ATIVA_MEDIA":                      72 + 12764,                     # Leituras.Gerador_PotenciaAtivaMedia

        # Potência Reativa
        "POT_REATIVA_1":                        73 + 12764,                     # Leituras.Gerador_PotenciaReativa1
        "POT_REATIVA_2":                        74 + 12764,                     # Leituras.Gerador_PotenciaReativa2
        "POT_REATIVA_3":                        75 + 12764,                     # Leituras.Gerador_PotenciaReativa3
        "POT_REATIVA_MEDIA":                    76 + 12764,                     # Leituras.Gerador_PotenciaReativaMedia

        # Potência Aparente
        "POT_APARENTE_1":                       77 + 12764,                     # Leituras.Gerador_PotenciaAparente1
        "POT_APARENTE_2":                       78 + 12764,                     # Leituras.Gerador_PotenciaAparente2
        "POT_APARENTE_3":                       79 + 12764,                     # Leituras.Gerador_PotenciaAparente3
        "POT_APARENTE_MEDIA":                   80 + 12764,                     # Leituras.Gerador_PotenciaAparenteMedia

        # Fator Potência
        "FATOR_POT_1":                          81 + 12764,                     # Leituras.Gerador_FatorPotencia1
        "FATOR_POT_2":                          82 + 12764,                     # Leituras.Gerador_FatorPotencia2
        "FATOR_POT_3":                          83 + 12764,                     # Leituras.Gerador_FatorPotencia3
        "FATOR_POT_MEDIA":                      84 + 12764,                     # Leituras.Gerador_FatorPotenciaMedia

        # Frequencia
        "FREQUENCIA":                           85 + 12764,                     # Leituras.Gerador_Frequencia

        # Energia Fornecida
        "ENERGIA_FORNECIDA_TWh":                86 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTWh
        "ENERGIA_FORNECIDA_GWh":                87 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGWh
        "ENERGIA_FORNECIDA_MWh":                88 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMWh
        "ENERGIA_FORNECIDA_kWh":                89 + 12764,                     # Leituras.Gerador_EnergiaFornecidakWh
        "ENERGIA_FORNECIDA_TVarh":              90 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTVarh
        "ENERGIA_FORNECIDA_GVarh":              91 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGVarh
        "ENERGIA_FORNECIDA_MVarh":              92 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMVarh
        "ENERGIA_FORNECIDA_kVarh":              93 + 12764,                     # Leituras.Gerador_EnergiaFornecidakVarh
        "ENERGIA_CORNECIDA_TVarh":              94 + 12764,                     # Leituras.Gerador_EnergiaConsumidaTVarh
        "ENERGIA_CORNECIDA_GVarh":              95 + 12764,                     # Leituras.Gerador_EnergiaConsumidaGVarh
        "ENERGIA_CORNECIDA_MVarh":              96 + 12764,                     # Leituras.Gerador_EnergiaConsumidaMVarh
        "ENERGIA_CORNECIDA_kVarh":              97 + 12764,                     # Leituras.Gerador_EnergiaConsumidakVarh

        "GERADOR_FP_INFO":                      98 + 12764,                     # Leituras.Gerador_FPInfo
        "GERADOR_FP_FASE1_IND":                 [98 + 12764, 0],                # Gerador.FP_Info.Fase1_Ind
        "GERADOR_FP_FASE1_CAP":                 [98 + 12764, 1],                # Gerador.FP_Info.Fase1_Cap
        "GERADOR_FP_FASE2_IND":                 [98 + 12764, 2],                # Gerador.FP_Info.Fase2_Ind
        "GERADOR_FP_FASE2_CAP":                 [98 + 12764, 3],                # Gerador.FP_Info.Fase2_Cap
        "GERADOR_FP_FASE3_IND":                 [98 + 12764, 4],                # Gerador.FP_Info.Fase3_Ind
        "GERADOR_FP_FASE3_CAP":                 [98 + 12764, 5],                # Gerador.FP_Info.Fase3_Cap
        "GERADOR_FP_FASE4_IND":                 [98 + 12764, 6],                # Gerador.FP_Info.Total_Ind
        "GERADOR_FP_FASE4_CAP":                 [98 + 12764, 7],                # Gerador.FP_Info.Total_Cap

        # Controles
        "CTRL_REATIVO_INFO":                    99 + 12764,                    # Leituras.CtrlReativo_Info
        "CTRL_REAT_MODO_FP":                    [99 + 12764, 0],               # CtrlReativo.Info.ModoFP
        "CTRL_REAT_MODO_VAR":                   [99 + 12764, 1],               # CtrlReativo.Info.ModoVar

        "CTRL_POTENCIA_INFO":                   100 + 12764,                    # Leituras.CtrlPotencia_Info
        "CTRL_POT_MODO_NIVEL":                  [100 + 12764, 0],               # CtrlPotencia.Info.ModoNivel
        "CTRL_POT_MODO_POT":                    [100 + 12764, 1],               # CtrlPotencia.Info.ModoPotencia
        "CTRL_POT_MODO_RELIGA_AUTO":            [100 + 12764, 2],               # CtrlPotencia.Info.ModoReligamentoAutomatico

        # Horimetros
        "HORIM_ELETR_LOW":                      101 + 12764,                    # Leituras.HorimetroEletrico_Low
        "HORIM_ELETR_HIGH":                     102 + 12764,                    # Leituras.HorimetroEletrico_High
        "HORIM_MECAN_LOW":                      103 + 12764,                    # Leituras.HorimetroMecanico_Low
        "HORIM_MECAN_HIGH":                     104 + 12764,                    # Leituras.HorimetroMecanico_High

        # Temperatura
        "TEMPERATURA_01":                       106 + 12764,                    # Leituras.Temperatura_01
        "TEMPERATURA_02":                       107 + 12764,                    # Leituras.Temperatura_02
        "TEMPERATURA_03":                       108 + 12764,                    # Leituras.Temperatura_03
        "TEMPERATURA_04":                       109 + 12764,                    # Leituras.Temperatura_04
        "TEMPERATURA_05":                       110 + 12764,                    # Leituras.Temperatura_05
        "TEMPERATURA_06":                       111 + 12764,                    # Leituras.Temperatura_06
        "TEMPERATURA_07":                       112 + 12764,                    # Leituras.Temperatura_07
        "TEMPERATURA_08":                       113 + 12764,                    # Leituras.Temperatura_08
        "TEMPERATURA_09":                       114 + 12764,                    # Leituras.Temperatura_09
        "TEMPERATURA_10":                       115 + 12764,                    # Leituras.Temperatura_10
        "TEMPERATURA_11":                       116 + 12764,                    # Leituras.Temperatura_11
        "TEMPERATURA_12":                       117 + 12764,                    # Leituras.Temperatura_12
        "TEMPERATURA_13":                       118 + 12764,                    # Leituras.Temperatura_13
        "TEMPERATURA_14":                       119 + 12764,                    # Leituras.Temperatura_14
        "TEMPERATURA_15":                       120 + 12764,                    # Leituras.Temperatura_15
        "TEMPERATURA_16":                       121 + 12764,                    # Leituras.Temperatura_16


        ## DISJUNTORES

        "DJ_01":                                0 + 12564,                      # Disjuntor Q125.0 - Alimentação Circuitos de Comando                                  -> condic_indisponibiliza UG1
        "DJ_02":                                0 + 12564,                      # Disjuntor Q125.1 - Alimentação GRTD2000                                              -> condic_indisponibiliza UG1
        "DJ_03":                                1 + 12564,                      # Disjuntor Q125.2 - Alimentação Relés de Proteção                                     -> condic_indisponibiliza UG1
        "DJ_04":                                2 + 12564,                      # Disjuntor Q24.0 - Alimentação Válvula Proporcional e Transdutor de Posição           -> condic_indisponibiliza UG1
        "DJ_05":                                3 + 12564,                      # CSG - Disjuntor Q220.1 - Alimentação Carregamento de Mola                            -> condic_indisponibiliza UG1
        "DJ_06":                                4 + 12564,                      # CSG - Disjuntor Q125.0 - Alimentação Circuito de Comando 52G                         -> condic_indisponibiliza UG1
        "DJ_07":                                5 + 12564,                      # Q49 - Disjuntor Q125.0 UG1 - Alimentação SEL2600
        "DJ_08":                                6 + 12564,                      # Disjuntor Motor QM1 - Bomba de Óleo 01 da UHCT                                       -> condic_indisponibiliza UG1
        "DJ_09":                                7 + 12564,                      # Disjuntor Motor QM2 - Bomba de Óleo 02 da UHCT                                       -> condic_indisponibiliza UG1
        "DJ_10":                                8 + 12564,                      # Disjuntor Motor QM3 - Bomba de Óleo 01 da UHLM                                       -> condic_indisponibiliza UG1
        "DJ_11":                                9 + 12564,                     #
        "DJ_12":                                10 + 12564,                     #
        "DJ_13":                                11 + 12564,                     #
        "DJ_14":                                12 + 12564,                     #
        "DJ_15":                                13 + 12564,                     #
        "DJ_16":                                14 + 12564,                     #
        "DJ_17":                                15 + 12564,                     #
        "DJ_18":                                16 + 12564,                     #
        "DJ_19":                                17 + 12564,                     #
        "DJ_20":                                18 + 12564,                     #
        "DJ_21":                                19 + 12564,                     #
        "DJ_22":                                20 + 12564,                     #
        "DJ_23":                                21 + 12564,                     #
        "DJ_24":                                22 + 12564,                     #
        "DJ_25":                                23 + 12564,                     #
        "DJ_26":                                24 + 12564,                     #
        "DJ_27":                                25 + 12564,                     #
        "DJ_28":                                26 + 12564,                     #
        "DJ_29":                                27 + 12564,                     #
        "DJ_30":                                28 + 12564,                     #
        "DJ_31":                                29 + 12564,                     #
        "DJ_32":                                30 + 12564,                     #


        ## ALARMES

        # Específicos UG2
        "Alarme04_13":                          [3 + 14199, 13],
        "Alarme04_14":                          [3 + 14199, 14],
        "Alarme04_15":                          [3 + 14199, 15],

        "Alarme10_10":                          [9 + 14199, 10],
        "Alarme10_11":                          [9 + 14199, 11],

        "Alarme12_02":                          [11 + 14199, 2],
        "Alarme12_14":                          [11 + 14199, 14],
        "Alarme12_15":                          [11 + 14199, 15],

        "Alarme13_00":                          [12 + 14199, 0],
        "Alarme13_01":                          [12 + 14199, 1],
        "Alarme13_02":                          [12 + 14199, 2],
        "Alarme13_03":                          [12 + 14199, 3],
        "Alarme13_04":                          [12 + 14199, 4],

        "Alarme15_14":                          [14 + 14199, 14],
        "Alarme15_15":                          [14 + 14199, 15],

        # Gerais
        "Alarme01_00":                          [0 + 14199, 0],
        "Alarme01_01":                          [0 + 14199, 1],
        "Alarme01_02":                          [0 + 14199, 2],
        "Alarme01_03":                          [0 + 14199, 3],
        "Alarme01_06":                          [0 + 14199, 6],
        "Alarme01_07":                          [0 + 14199, 7],
        "Alarme01_08":                          [0 + 14199, 8],
        "Alarme01_09":                          [0 + 14199, 9],
        "Alarme01_10":                          [0 + 14199, 10],
        "Alarme01_11":                          [0 + 14199, 11],
        "Alarme01_12":                          [0 + 14199, 12],
        "Alarme01_13":                          [0 + 14199, 13],
        "Alarme01_14":                          [0 + 14199, 14],
        "Alarme01_15":                          [0 + 14199, 15],

        "Alarme02_00":                          [1 + 14199, 0],
        "Alarme02_01":                          [1 + 14199, 1],
        "Alarme02_02":                          [1 + 14199, 2],
        "Alarme02_03":                          [1 + 14199, 3],
        "Alarme02_04":                          [1 + 14199, 4],
        "Alarme02_05":                          [1 + 14199, 5],
        "Alarme02_06":                          [1 + 14199, 6],
        "Alarme02_07":                          [1 + 14199, 7],
        "Alarme02_08":                          [1 + 14199, 8],
        "Alarme02_09":                          [1 + 14199, 9],
        "Alarme02_10":                          [1 + 14199, 10],
        "Alarme02_11":                          [1 + 14199, 11],
        "Alarme02_12":                          [1 + 14199, 12],
        "Alarme02_13":                          [1 + 14199, 13],
        "Alarme02_14":                          [1 + 14199, 14],
        "Alarme02_15":                          [1 + 14199, 15],

        "Alarme03_00":                          [2 + 14199, 0],
        "Alarme03_01":                          [2 + 14199, 1],
        "Alarme03_02":                          [2 + 14199, 2],
        "Alarme03_03":                          [2 + 14199, 3],
        "Alarme03_04":                          [2 + 14199, 4],
        "Alarme03_05":                          [2 + 14199, 5],
        "Alarme03_06":                          [2 + 14199, 6],
        "Alarme03_07":                          [2 + 14199, 7],
        "Alarme03_08":                          [2 + 14199, 8],
        "Alarme03_09":                          [2 + 14199, 9],
        "Alarme03_10":                          [2 + 14199, 10],
        "Alarme03_11":                          [2 + 14199, 11],
        "Alarme03_12":                          [2 + 14199, 12],
        "Alarme03_13":                          [2 + 14199, 13],
        "Alarme03_14":                          [2 + 14199, 14],
        "Alarme03_15":                          [2 + 14199, 15],

        "Alarme04_00":                          [3 + 14199, 0],
        "Alarme04_01":                          [3 + 14199, 1],
        "Alarme04_02":                          [3 + 14199, 2],
        "Alarme04_04":                          [3 + 14199, 4],
        "Alarme04_05":                          [3 + 14199, 5],
        "Alarme04_06":                          [3 + 14199, 6],
        "Alarme04_07":                          [3 + 14199, 7],
        "Alarme04_09":                          [3 + 14199, 9],
        "Alarme04_10":                          [3 + 14199, 10],
        "Alarme04_11":                          [3 + 14199, 11],
        "Alarme04_12":                          [3 + 14199, 12],
        "Alarme04_13":                          [3 + 14199, 13],
        "Alarme04_14":                          [3 + 14199, 14],
        "Alarme04_15":                          [3 + 14199, 15],

        "Alarme05_00":                          [4 + 14199, 0],
        "Alarme05_02":                          [4 + 14199, 2],
        "Alarme05_03":                          [4 + 14199, 3],
        "Alarme05_04":                          [4 + 14199, 4],
        "Alarme05_05":                          [4 + 14199, 5],
        "Alarme05_06":                          [4 + 14199, 6],
        "Alarme05_07":                          [4 + 14199, 7],
        "Alarme05_09":                          [4 + 14199, 9],
        "Alarme05_10":                          [4 + 14199, 10],
        "Alarme05_11":                          [4 + 14199, 11],
        "Alarme05_12":                          [4 + 14199, 12],
        "Alarme05_13":                          [4 + 14199, 13],
        "Alarme05_14":                          [4 + 14199, 14],
        "Alarme05_15":                          [4 + 14199, 15],

        "Alarme06_00":                          [5 + 14199, 0],
        "Alarme06_03":                          [5 + 14199, 3],
        "Alarme06_04":                          [5 + 14199, 4],
        "Alarme06_05":                          [5 + 14199, 5],
        "Alarme06_08":                          [5 + 14199, 8],
        "Alarme06_09":                          [5 + 14199, 9],
        "Alarme06_10":                          [5 + 14199, 10],
        "Alarme06_11":                          [5 + 14199, 11],
        "Alarme06_12":                          [5 + 14199, 12],
        "Alarme06_13":                          [5 + 14199, 13],
        "Alarme06_14":                          [5 + 14199, 14],
        "Alarme06_15":                          [5 + 14199, 15],

        "Alarme07_00":                          [6 + 14199, 0],
        "Alarme07_01":                          [6 + 14199, 1],
        "Alarme07_02":                          [6 + 14199, 2],
        "Alarme07_03":                          [6 + 14199, 3],
        "Alarme07_06":                          [6 + 14199, 6],
        "Alarme07_07":                          [6 + 14199, 7],
        "Alarme07_08":                          [6 + 14199, 8],
        "Alarme07_09":                          [6 + 14199, 9],
        "Alarme07_10":                          [6 + 14199, 10],
        "Alarme07_11":                          [6 + 14199, 11],
        "Alarme07_12":                          [6 + 14199, 12],
        "Alarme07_13":                          [6 + 14199, 13],
        "Alarme07_14":                          [6 + 14199, 14],
        "Alarme07_15":                          [6 + 14199, 15],

        "Alarme08_00":                          [7 + 14199, 0],
        "Alarme08_01":                          [7 + 14199, 1],
        "Alarme08_02":                          [7 + 14199, 2],
        "Alarme08_03":                          [7 + 14199, 3],
        "Alarme08_07":                          [7 + 14199, 7],
        "Alarme08_08":                          [7 + 14199, 8],
        "Alarme08_09":                          [7 + 14199, 9],
        "Alarme08_10":                          [7 + 14199, 10],
        "Alarme08_11":                          [7 + 14199, 11],
        "Alarme08_12":                          [7 + 14199, 12],
        "Alarme08_13":                          [7 + 14199, 13],
        "Alarme08_14":                          [7 + 14199, 14],
        "Alarme08_15":                          [7 + 14199, 15],

        "Alarme09_00":                          [8 + 14199, 0],
        "Alarme09_01":                          [8 + 14199, 1],
        "Alarme09_02":                          [8 + 14199, 2],
        "Alarme09_03":                          [8 + 14199, 3],
        "Alarme09_04":                          [8 + 14199, 4],
        "Alarme09_06":                          [8 + 14199, 6],
        "Alarme09_07":                          [8 + 14199, 7],
        "Alarme09_08":                          [8 + 14199, 8],
        "Alarme09_09":                          [8 + 14199, 9],
        "Alarme09_10":                          [8 + 14199, 10],
        "Alarme09_11":                          [8 + 14199, 11],
        "Alarme09_12":                          [8 + 14199, 12],
        "Alarme09_13":                          [8 + 14199, 13],
        "Alarme09_14":                          [8 + 14199, 14],
        "Alarme09_15":                          [8 + 14199, 15],

        "Alarme10_00":                          [9 + 14199, 0],
        "Alarme10_01":                          [9 + 14199, 1],
        "Alarme10_02":                          [9 + 14199, 2],
        "Alarme10_03":                          [9 + 14199, 3],
        "Alarme10_05":                          [9 + 14199, 5],
        "Alarme10_06":                          [9 + 14199, 6],
        "Alarme10_07":                          [9 + 14199, 7],
        "Alarme10_08":                          [9 + 14199, 8],
        "Alarme10_09":                          [9 + 14199, 9],
        "Alarme10_10":                          [9 + 14199, 10],
        "Alarme10_11":                          [9 + 14199, 11],
        "Alarme10_12":                          [9 + 14199, 12],
        "Alarme10_13":                          [9 + 14199, 13],
        "Alarme10_14":                          [9 + 14199, 14],
        "Alarme10_15":                          [9 + 14199, 15],

        "Alarme11_00":                          [10 + 14199, 0],
        "Alarme11_01":                          [10 + 14199, 1],
        "Alarme11_02":                          [10 + 14199, 2],
        "Alarme11_06":                          [10 + 14199, 6],
        "Alarme11_07":                          [10 + 14199, 7],
        "Alarme11_08":                          [10 + 14199, 8],
        "Alarme11_09":                          [10 + 14199, 9],
        "Alarme11_10":                          [10 + 14199, 10],
        "Alarme11_11":                          [10 + 14199, 11],
        "Alarme11_12":                          [10 + 14199, 12],
        "Alarme11_13":                          [10 + 14199, 13],
        "Alarme11_14":                          [10 + 14199, 14],
        "Alarme11_15":                          [10 + 14199, 15],

        "Alarme12_01":                          [11 + 14199, 1],
        "Alarme12_02":                          [11 + 14199, 2],
        "Alarme12_03":                          [11 + 14199, 3],
        "Alarme12_04":                          [11 + 14199, 4],
        "Alarme12_05":                          [11 + 14199, 5],
        "Alarme12_06":                          [11 + 14199, 6],
        "Alarme12_07":                          [11 + 14199, 7],
        "Alarme12_09":                          [11 + 14199, 9],
        "Alarme12_10":                          [11 + 14199, 10],
        "Alarme12_11":                          [11 + 14199, 11],
        "Alarme12_12":                          [11 + 14199, 12],
        "Alarme12_13":                          [11 + 14199, 13],
        "Alarme12_14":                          [11 + 14199, 14],
        "Alarme12_15":                          [11 + 14199, 15],

        "Alarme13_00":                          [12 + 14199, 0],
        "Alarme13_01":                          [12 + 14199, 1],
        "Alarme13_02":                          [12 + 14199, 2],
        "Alarme13_03":                          [12 + 14199, 3],
        "Alarme13_09":                          [12 + 14199, 9],
        "Alarme13_10":                          [12 + 14199, 10],
        "Alarme13_11":                          [12 + 14199, 11],
        "Alarme13_12":                          [12 + 14199, 12],
        "Alarme13_13":                          [12 + 14199, 13],
        "Alarme13_14":                          [12 + 14199, 14],
        "Alarme13_15":                          [12 + 14199, 15],

        "Alarme14_00":                          [13 + 14199, 0],
        "Alarme14_01":                          [13 + 14199, 1],
        "Alarme14_02":                          [13 + 14199, 2],
        "Alarme14_03":                          [13 + 14199, 3],
        "Alarme14_04":                          [13 + 14199, 4],
        "Alarme14_05":                          [13 + 14199, 5],
        "Alarme14_10":                          [13 + 14199, 10],
        "Alarme14_11":                          [13 + 14199, 11],
        "Alarme14_12":                          [13 + 14199, 12],
        "Alarme14_13":                          [13 + 14199, 13],
        "Alarme14_14":                          [13 + 14199, 14],
        "Alarme14_15":                          [13 + 14199, 15],

        "Alarme15_00":                          [14 + 14199, 0],
        "Alarme15_01":                          [14 + 14199, 1],
        "Alarme15_02":                          [14 + 14199, 2],
        "Alarme15_03":                          [14 + 14199, 3],
        "Alarme15_04":                          [14 + 14199, 4],
        "Alarme15_05":                          [14 + 14199, 5],
        "Alarme15_06":                          [14 + 14199, 6],
        "Alarme15_07":                          [14 + 14199, 7],
        "Alarme15_08":                          [14 + 14199, 8],
        "Alarme15_09":                          [14 + 14199, 9],
        "Alarme15_10":                          [14 + 14199, 10],
        "Alarme15_12":                          [14 + 14199, 12],
        "Alarme15_13":                          [14 + 14199, 13],
        "Alarme15_14":                          [14 + 14199, 14],
        "Alarme15_15":                          [14 + 14199, 15],

        "Alarme16_00":                          [15 + 14199, 0],
        "Alarme16_01":                          [15 + 14199, 1],
        "Alarme16_02":                          [15 + 14199, 2],
        "Alarme16_03":                          [15 + 14199, 3],
        "Alarme16_04":                          [15 + 14199, 4],
        "Alarme16_05":                          [15 + 14199, 5],
        "Alarme16_06":                          [15 + 14199, 6],
        "Alarme16_07":                          [15 + 14199, 7],
        "Alarme16_08":                          [15 + 14199, 8],
        "Alarme16_09":                          [15 + 14199, 9],
        "Alarme16_10":                          [15 + 14199, 10],
        "Alarme16_11":                          [15 + 14199, 11],
        "Alarme16_12":                          [15 + 14199, 12],
    },
    "UG3": {
        ## COMANDOS
        # Gerais
        "CMD_RESET_ALARMES":                    0 + 12288,                      # Comandos.Operacao_PCH_AdoPopinhakResetAlarmes
        "CMD_RECONHECE_ALARMES":                0 + 12289,                      # Comandos.Operacao_PCH_AdoPopinhakReconheceAlarmes

        # Operação
        "CMD_OPER_UP":                          1 + 12289,                      # Comandos.Operacao_UP
        "CMD_OPER_UPGM":                        2 + 12289,                      # Comandos.Operacao_UPGM
        "CMD_OPER_UVD":                         3 + 12289,                      # Comandos.Operacao_UVD
        "CMD_OPER_UPS":                         4 + 12289,                      # Comandos.Operacao_UPS
        "CMD_OPER_US":                          5 + 12289,                      # Comandos.Operacao_US
        "CMD_OPER_EMERGENCIA_LIGAR":            6 + 12289,                      # Comandos.Operacao_EmergenciaLigar
        "CMD_OPER_EMERGENCIA_DESLIGAR":         7 + 12289,                      # Comandos.Operacao_EmergenciaDesligar
        "CMD_OPER_PARADA_RESET":                71 + 12289,                     # Comandos.Operacao_ParadaReset

        # Turbina
        "CMD_TURB_BYPASS_ABRIR":                8 + 12289,                      # Comandos.Turb_ByPassAbrir
        "CMD_TURB_BYPASS_FECHAR":               9 + 12289,                     # Comandos.Turb_ByPassFechar
        "CMD_TURB_BORBOLETA_ABRIR":             10 + 12289,                     # Comandos.Turb_BorboletaAbrir
        "CMD_TURB_BORBOLETA_FECHAR":            11 + 12289,                     # Comandos.Turb_BorboletaFechar
        "CMD_TURB_FRENAGEM_APLICAR":            12 + 12289,                     # Comandos.Turb_FrenagemAplicar
        "CMD_TURB_FRENAGEM_DESAPLICAR":         13 + 12289,                     # Comandos.Turb_FrenagemDesaplicar
        "CMD_TURB_FRENAGEM_MANUAL":             14 + 12289,                     # Comandos.Turb_FrenagemManual
        "CMD_TURB_FRENAGEM_AUTO":               15 + 12289,                     # Comandos.Turb_FrenagemAuto
        "CMD_TURB_SENSOR_ATIVAR":               16 + 12289,                     # Comandos.Turb_SensorAtivar
        "CMD_TURB_SENSOR_DESATIVAR":            17 + 12289,                     # Comandos.Turb_SensorDesativar

        # Reg V
        "CMD_REG_V_PARTIR":                     18 + 12289,                     # Comandos.RegV_Partir
        "CMD_REG_V_PARAR":                      19 + 12289,                     # Comandos.RegV_Parar
        "CMD_REG_V_COLOCAR_CARGA":              20 + 12289,                     # Comandos.RegV_ColocarCarga
        "CMD_REG_V_RETIRAR_CARGA":              21 + 12289,                     # Comandos.RegV_RetirarCarga
        "CMD_REG_V_INCREMENTA_VELOCIDADE":      22 + 12289,                     # Comandos.RegV_IncrementaVelocidade
        "CMD_REG_V_DECREMENTA_VELOCIDADE":      23 + 12289,                     # Comandos.RegV_DecrementaVelocidade
        "CMD_REG_V_SEL_MODO_ESTATISMO":         24 + 12289,                     # Comandos.RegV_SelecionaModoEstatismo
        "CMD_REG_V_SEL_MODO_BASECARGA":         25 + 12289,                     # Comandos.RegV_SelecionaModoBaseCarga

        # Reg T
        "CMD_REG_T_LIGAR":                      26 + 12289,                     # Comandos.RegT_Ligar
        "CMD_REG_T_DESLIGAR":                   27 + 12289,                     # Comandos.RegT_Desligar
        "CMD_REG_T_INCREMENTA_TENSAO":          28 + 12289,                     # Comandos.RegT_IncrementaTensao
        "CMD_REG_T_DECREMENTA_TENSAO":          29 + 12289,                     # Comandos.RegT_DecrementaTensao
        "CMD_REG_T_PRE_EXCITACAO":              30 + 12289,                     # Comandos.RegT_PreExcitacao

        # Sinc
        "CMD_SINC_LIGAR":                       31 + 12289,                     # Comandos.Sinc_Ligar
        "CMD_SINC_DESLIGAR":                    32 + 12289,                     # Comandos.Sinc_Desligar
        "CMD_SINC_MODO_AUTO_LIGAR":             33 + 12289,                     # Comandos.Sinc_ModoAutoLigar
        "CMD_SINC_MODO_MANUAL_LIGAR":           34 + 12289,                     # Comandos.Sinc_ModoManualLigar
        "CMD_SINC_MODO_BMORTA_LIGAR":           35 + 12289,                     # Comandos.Sinc_ModoBMortaLigar

        # DJ52G
        "CMD_DJ52G_ABRIR":                      36 + 12289,                     # Comandos.Disj52G_Abrir

        # Controle Reativo
        "CMD_CTRL_REATIVO_MODO_FPLIGAR":        37 + 12289,                     # Comandos.CtrlReativo_ModoFPLigar
        "CMD_CTRL_REATIVO_MODO_FPDESLIGAR":     38 + 12289,                     # Comandos.CtrlReativo_ModoFPDesligar
        "CMD_CTRL_REATIVO_MODO_VArLIGAR":       39 + 12289,                     # Comandos.CtrlReativo_ModoVArLigar
        "CMD_CTRL_REATIVO_MODO_VArDESLIGAR":    40 + 12289,                     # Comandos.CtrlReativo_ModoVArDesligar

        # Controle Potência
        "CMD_CTRL_POT_MODO_POT_LIGAR":          41 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaLigar
        "CMD_CTRL_POT_MODO_POT_DESLIGAR":       42 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaDesligar
        "CMD_CTRL_POT_MODO_NIVEL_LIGAR":        43 + 12289,                     # Comandos.CtrlPotencia_ModoNivelLigar
        "CMD_CTRL_POT_MODO_NIVEL_DESLIGAR":     44 + 12289,                     # Comandos.CtrlPotencia_ModoNivelDesligar
        "CMD_CTRL_POT_RELI_AUTO_LIGAR":         45 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoLigar
        "CMD_CTRL_POT_RELI_AUTO_DESLIGAR":      46 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoDesligar

        # UHCT
        "CMD_UHCT_BOMBA_01_LIGAR":              47 + 12289,                     # Comandos.UHCT_Bomba01Ligar
        "CMD_UHCT_BOMBA_01_DESLIGAR":           48 + 12289,                     # Comandos.UHCT_Bomba01Desligar
        "CMD_UHCT_BOMBA_01_PRINCIPAL":          49 + 12289,                     # Comandos.UHCT_Bomba01Principal
        "CMD_UHCT_BOMBA_02_LIGAR":              50 + 12289,                     # Comandos.UHCT_Bomba02Ligar
        "CMD_UHCT_BOMBA_02_DESLIGAR":           51 + 12289,                     # Comandos.UHCT_Bomba02Desligar
        "CMD_UHCT_BOMBA_02_PRINCIPAL":          52 + 12289,                     # Comandos.UHCT_Bomba02Principal
        "CMD_UHCT_BOMBA_AGUA_LIGAR":            53 + 12289,                     # Comandos.UHCT_BombaAguaLigar
        "CMD_UHCT_BOMBA_AGUA_DESLIGAR":         54 + 12289,                     # Comandos.UHCT_BombaAguaDesligar
        "CMD_UHCT_SENSOR_ATIVAR":               55 + 12289,                     # Comandos.UHCT_SensorAtivar
        "CMD_UHCT_SENSOR_DESATIVAR":            56 + 12289,                     # Comandos.UHCT_SensorDesativar
        "CMD_UHCT_RODIZIO_HABILITAR":           57 + 12289,                     # Comandos.UHCT_RodizioHabilitar
        "CMD_UHCT_RODIZIO_DESABILITAR":         58 + 12289,                     # Comandos.UHCT_RodizioDesabilitar

        # UHLM
        "CMD_UHLM_BOMBA_01_LIGAR":              59 + 12289,                     # Comandos.UHLM_Bomba01Ligar
        "CMD_UHLM_BOMBA_01_DESLIGAR":           60 + 12289,                     # Comandos.UHLM_Bomba01Desligar
        "CMD_UHLM_BOMBA_01_PRINCIPAL":          61 + 12289,                     # Comandos.UHLM_Bomba01Principal
        "CMD_UHLM_BOMBA_02_LIGAR":              62 + 12289,                     # Comandos.UHLM_Bomba02Ligar
        "CMD_UHLM_BOMBA_02_DESLIGAR":           63 + 12289,                     # Comandos.UHLM_Bomba02Desligar
        "CMD_UHLM_BOMBA_02_PRINCIPAL":          64 + 12289,                     # Comandos.UHLM_Bomba02Principal
        "CMD_UHLM_BOMBA_JACKING_LIGA":          65 + 12289,                     # Comandos.UHLM_BombaJackingLiga
        "CMD_UHLM_BOMBA_JACKING_DESLIGA":       66 + 12289,                     # Comandos.UHLM_BombaJackingDesliga
        "CMD_UHLM_BOMBA_AGUA_LIGA":             67 + 12289,                     # Comandos.UHLM_BombaAguaLiga
        "CMD_UHLM_BOMBA_AGUA_DESLIGA":          68 + 12289,                     # Comandos.UHLM_BombaAguaDesliga
        "CMD_UHLM_RODIZIO_HABILITAR":           69 + 12289,                     # Comandos.UHLM_RodizioHabilitar
        "CMD_UHLM_RODIZIO_DESABILITAR":         70 + 12289,                     # Comandos.UHLM_RodizioDesabilitar

        # RT
        "CMD_RT_MTVC_HABILITAR":                71 + 12289,                     # Comandos.RT_MTVC_Habilitar
        "CMD_RT_MECC_HABILITAR":                72 + 12289,                     # Comandos.RT_MECC_Habilitar
        "CMD_RT_ONLINE_HABILITAR":              73 + 12289,                     # Comandos.RT_Online_habilitar
        "CMD_RT_ONLINE_DESABILITAR":            74 + 12289,                     # Comandos.RT_Online_Desabiltar
        "CMD_RT_PARALELO_HABILITAR":            75 + 12289,                     # Comandos.RT_Paralelo_habilitar
        "CMD_RT_PARALELO_DESABILITAR":          76 + 12289,                     # Comandos.RT_Paralelo_Desabilitar

        # RV
        "CMD_RV_CONJUGADO_AUTO_HABILITAR":      77 + 12289,                     # Comandos.RV_ConjugadoAuto_habilitar
        "CMD_RV_CONJUGADO_MANUAL_HABILITAR":    78 + 12289,                     # Comandos.RV_ConjugadoManual_habilitar
        "CMD_RV_CONJUGADO_01_HABILITAR":        79 + 12289,                     # Comandos.RV_Conjugado01_habilitar
        "CMD_RV_CONJUGADO_02_HABILITAR":        80 + 12289,                     # Comandos.RV_Conjugado02_habilitar
        "CMD_RV_CONJUGADO_03_HABILITAR":        81 + 12289,                     # Comandos.RV_Conjugado03_habilitar
        "CMD_RV_CONJUGADO_04_HABILITAR":        82 + 12289,                     # Comandos.RV_Conjugado04_habilitar
        "CMD_RV_CONJUGADO_05_HABILITAR":        83 + 12289,                     # Comandos.RV_Conjugado05_habilitar


        ## SETPOINTS

        # UHCT
        "UHCT_PRESSAO_MAX":                     0 + 13569,                      # Setpoints.UHCT_PressaoMaxima
        "UHCT_PRESSAO_MIN":                     0 + 13569,                      # Setpoints.UHCT_PressaoMinima
        "UHCT_PRESSAO_DESLIGAMENTO":            1 + 13569,                      # Setpoints.UHCT_PressaoDesligamento
        "UHCT_PRESSAO_CRITICA":                 2 + 13569,                      # Setpoints.UHCT_PressaoCritica

        # Controle Potência
        "CRTL_POT_NIVEL_LL1":                   3 + 13569,                      # Setpoints.CtrlPotencia_NivelLL1
        "CRTL_POT_NIVEL_LL2":                   4 + 13569,                      # Setpoints.CtrlPotencia_NivelLL2
        "CRTL_POT_NIVEL_LL3":                   5 + 13569,                      # Setpoints.CtrlPotencia_NivelLL3
        "CRTL_POT_NIVEL_LL4":                   6 + 13569,                      # Setpoints.CtrlPotencia_NivelLL4
        "CRTL_POT_NIVEL_LL5":                   7 + 13569,                      # Setpoints.CtrlPotencia_NivelLL5
        "CRTL_POT_POT_1":                       8 + 13569,                      # Setpoints.CtrlPotencia_Potencia1
        "CRTL_POT_POT_2":                       9 + 13569,                     # Setpoints.CtrlPotencia_Potencia2
        "CRTL_POT_POT_3":                       10 + 13569,                     # Setpoints.CtrlPotencia_Potencia3
        "CRTL_POT_POT_4":                       11 + 13569,                     # Setpoints.CtrlPotencia_Potencia4
        "CRTL_POT_POT_5":                       12 + 13569,                     # Setpoints.CtrlPotencia_Potencia5
        "CRTL_POT_POT_MIN":                     13 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinima
        "CRTL_POT_POT_MIN_TEMPO":               14 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinimaTempo
        "CRTL_POT_NIVEL_RELIGAMENTO":           15 + 13569,                     # Setpoints.CtrlPotencia_NivelReligamento
        "CRTL_POT_ALVO":                        16 + 13569,                     # Setpoints.CtrlPotencia_Alvo
        "CRTL_POT_TOLERANCIA":                  17 + 13569,                     # Setpoints.CtrlPotencia_Tolerancia
        "CRTL_POT_PULSO_TEMPO":                 18 + 13569,                     # Setpoints.CtrlPotencia_PulsoTempo
        "CRTL_POT_PULSO_INTERVALO":             19 + 13569,                     # Setpoints.CtrlPotencia_PulsoIntervalo
        "CRTL_POT_SP_NIVEL":                    20 + 13569,                     # Setpoints.CtrlPotencia_SetpointNivel
        "CRTL_POT_NIVEL_MIN_ALARME":            21 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoAlarme
        "CRTL_POT_NIVEL_MIN_TRIP":              22 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoTRIP
        "CTRL_POT_POT_MAX":                     88 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMaxima

        # Controle Reativo
        "CRTL_REATIVO_SP_FP":                   23 + 13569,                     # Setpoints.CtrlReativo_SetpointFP
        "CRTL_REATIVO_SP_REATIVO":              24 + 13569,                     # Setpoints.CtrlReativo_SetpointReativo

        # Turbina
        "TURB_VIBRA_01_ALARME":                 25 + 13569,                     # Setpoints.Turb_Vibracao01Alarme
        "TURB_VIBRA_01_TRIP":                   26 + 13569,                     # Setpoints.Turb_Vibracao01TRIP
        "TURB_VIBRA_02_ALARME":                 27 + 13569,                     # Setpoints.Turb_Vibracao02Alarme
        "TURB_VIBRA_02_TRIP":                   28 + 13569,                     # Setpoints.Turb_Vibracao02TRIP
        "TURB_VIBRA_03_ALARME":                 29 + 13569,                     # Setpoints.Turb_Vibracao03Alarme
        "TURB_VIBRA_03_TRIP":                   30 + 13569,                     # Setpoints.Turb_Vibracao03TRIP
        "TURB_VIBRA_04_ALARME":                 31 + 13569,                     # Setpoints.Turb_Vibracao04Alarme
        "TURB_VIBRA_04_TRIP":                   32 + 13569,                     # Setpoints.Turb_Vibracao04TRIP
        "TURB_TEMPO_EQUALI_SP":                 33 + 13569,                     # Setpoints.Turb_TempoEqualizacaoSetpoint
        "TURB_VIBRA_05_ALARME":                 89 + 13569,                     # Setpoints.Turb_Vibracao05Alarme
        "TURB_VIBRA_05_TRIP":                   90 + 13569,                     # Setpoints.Turb_Vibracao05TRIP

        # Freio
        "FREIO_PULSO_INTERVALO":                34 + 13569,                     # Setpoints.Freio_PulsoIntervalo
        "FREIO_PULSO_TEMPO":                    35 + 13569,                     # Setpoints.Freio_PulsoTempo

        # UHCT
        "UHCT_RODIZIO_PRINCIPAL":               36 + 13569,                     # Setpoints.UHCT_RodizioPrincipal
        "UHCT_RODIZIO_RETAGUARDA":              37 + 13569,                     # Setpoints.UHCT_RodizioRetaguarda

        # UHLM
        "UHLM_RODIZIO_PRINCIPAL":               38 + 13569,                     # Setpoints.UHLM_RodizioPrincipal
        "UHLM_RODIZIO_RETAGUARDA":              39 + 13569,                     # Setpoints.UHLM_RodizioRetaguarda
        "UHLM_SP_VAZAO_01":                     91 + 13569,                     # Setpoints.UHLM_SetpointVazao01
        "UHLM_SP_VAZAO_02":                     92 + 13569,                     # Setpoints.UHLM_SetpointVazao02
        "UHLM_SP_VAZAO_03":                     93 + 13569,                     # Setpoints.UHLM_SetpointVazao03
        "UHLM_SP_VAZAO_04":                     94 + 13569,                     # Setpoints.UHLM_SetpointVazao04

        # Temperaturas
        "TEMPERATURA_01_ALARME":                40 + 13569,                     # Setpoints.Temperatura01_Alarme
        "TEMPERATURA_02_ALARME":                41 + 13569,                     # Setpoints.Temperatura02_Alarme
        "TEMPERATURA_03_ALARME":                42 + 13569,                     # Setpoints.Temperatura03_Alarme
        "TEMPERATURA_04_ALARME":                43 + 13569,                     # Setpoints.Temperatura04_Alarme
        "TEMPERATURA_05_ALARME":                44 + 13569,                     # Setpoints.Temperatura05_Alarme
        "TEMPERATURA_06_ALARME":                45 + 13569,                     # Setpoints.Temperatura06_Alarme
        "TEMPERATURA_07_ALARME":                46 + 13569,                     # Setpoints.Temperatura07_Alarme
        "TEMPERATURA_08_ALARME":                47 + 13569,                     # Setpoints.Temperatura08_Alarme
        "TEMPERATURA_09_ALARME":                48 + 13569,                     # Setpoints.Temperatura09_Alarme
        "TEMPERATURA_10_ALARME":                49 + 13569,                     # Setpoints.Temperatura10_Alarme
        "TEMPERATURA_11_ALARME":                50 + 13569,                     # Setpoints.Temperatura11_Alarme
        "TEMPERATURA_12_ALARME":                51 + 13569,                     # Setpoints.Temperatura12_Alarme
        "TEMPERATURA_13_ALARME":                52 + 13569,                     # Setpoints.Temperatura13_Alarme
        "TEMPERATURA_14_ALARME":                53 + 13569,                     # Setpoints.Temperatura14_Alarme
        "TEMPERATURA_15_ALARME":                54 + 13569,                     # Setpoints.Temperatura15_Alarme
        "TEMPERATURA_16_ALARME":                55 + 13569,                     # Setpoints.Temperatura16_Alarme
        "TEMPERATURA_01_TRIP01":                56 + 13569,                     # Setpoints.Temperatura01_TRIP01
        "TEMPERATURA_02_TRIP01":                57 + 13569,                     # Setpoints.Temperatura02_TRIP01
        "TEMPERATURA_03_TRIP01":                58 + 13569,                     # Setpoints.Temperatura03_TRIP01
        "TEMPERATURA_04_TRIP01":                59 + 13569,                     # Setpoints.Temperatura04_TRIP01
        "TEMPERATURA_05_TRIP01":                60 + 13569,                     # Setpoints.Temperatura05_TRIP01
        "TEMPERATURA_06_TRIP01":                61 + 13569,                     # Setpoints.Temperatura06_TRIP01
        "TEMPERATURA_07_TRIP01":                62 + 13569,                     # Setpoints.Temperatura07_TRIP01
        "TEMPERATURA_08_TRIP01":                63 + 13569,                     # Setpoints.Temperatura08_TRIP01
        "TEMPERATURA_09_TRIP01":                64 + 13569,                     # Setpoints.Temperatura09_TRIP01
        "TEMPERATURA_10_TRIP01":                65 + 13569,                     # Setpoints.Temperatura10_TRIP01
        "TEMPERATURA_11_TRIP01":                66 + 13569,                     # Setpoints.Temperatura11_TRIP01
        "TEMPERATURA_12_TRIP01":                67 + 13569,                     # Setpoints.Temperatura12_TRIP01
        "TEMPERATURA_13_TRIP01":                68 + 13569,                     # Setpoints.Temperatura13_TRIP01
        "TEMPERATURA_14_TRIP01":                69 + 13569,                     # Setpoints.Temperatura14_TRIP01
        "TEMPERATURA_15_TRIP01":                70 + 13569,                     # Setpoints.Temperatura15_TRIP01
        "TEMPERATURA_16_TRIP01":                71 + 13569,                     # Setpoints.Temperatura16_TRIP01
        "TEMPERATURA_01_TRIP02":                72 + 13569,                     # Setpoints.Temperatura01_TRIP02
        "TEMPERATURA_02_TRIP02":                73 + 13569,                     # Setpoints.Temperatura02_TRIP02
        "TEMPERATURA_03_TRIP02":                74 + 13569,                     # Setpoints.Temperatura03_TRIP02
        "TEMPERATURA_04_TRIP02":                75 + 13569,                     # Setpoints.Temperatura04_TRIP02
        "TEMPERATURA_05_TRIP02":                76 + 13569,                     # Setpoints.Temperatura05_TRIP02
        "TEMPERATURA_06_TRIP02":                77 + 13569,                     # Setpoints.Temperatura06_TRIP02
        "TEMPERATURA_07_TRIP02":                78 + 13569,                     # Setpoints.Temperatura07_TRIP02
        "TEMPERATURA_08_TRIP02":                79 + 13569,                     # Setpoints.Temperatura08_TRIP02
        "TEMPERATURA_09_TRIP02":                80 + 13569,                     # Setpoints.Temperatura09_TRIP02
        "TEMPERATURA_10_TRIP02":                81 + 13569,                     # Setpoints.Temperatura10_TRIP02
        "TEMPERATURA_11_TRIP02":                82 + 13569,                     # Setpoints.Temperatura11_TRIP02
        "TEMPERATURA_12_TRIP02":                83 + 13569,                     # Setpoints.Temperatura12_TRIP02
        "TEMPERATURA_13_TRIP02":                84 + 13569,                     # Setpoints.Temperatura13_TRIP02
        "TEMPERATURA_14_TRIP02":                85 + 13569,                     # Setpoints.Temperatura14_TRIP02
        "TEMPERATURA_15_TRIP02":                86 + 13569,                     # Setpoints.Temperatura15_TRIP02
        "TEMPERATURA_16_TRIP02":                87 + 13569,                     # Setpoints.Temperatura16_TRIP02

        # Grade Suja
        "GradeSuja_TRIP":                       95 + 13569,                     # Setpoints.GradeSuja_TRIP

        # Curva
        "CURVA_01_DISTRIB_P1":                  96 + 13569,                     # Setpoints.Curva01_DistribuidorP1
        "CURVA_01_DISTRIB_P2":                  97 + 13569,                     # Setpoints.Curva01_DistribuidorP2
        "CURVA_01_DISTRIB_P3":                  98 + 13569,                     # Setpoints.Curva01_DistribuidorP3
        "CURVA_01_DISTRIB_P4":                  99 + 13569,                    # Setpoints.Curva01_DistribuidorP4
        "CURVA_01_DISTRIB_P5":                  100 + 13569,                    # Setpoints.Curva01_DistribuidorP5
        "CURVA_01_DISTRIB_P6":                  101 + 13569,                    # Setpoints.Curva01_DistribuidorP6
        "CURVA_01_DISTRIB_P7":                  102 + 13569,                    # Setpoints.Curva01_DistribuidorP7
        "CURVA_01_DISTRIB_P8":                  103 + 13569,                    # Setpoints.Curva01_DistribuidorP8
        "CURVA_01_DISTRIB_P9":                  104 + 13569,                    # Setpoints.Curva01_DistribuidorP9
        "CURVA_01_DISTRIB_P10":                 105 + 13569,                    # Setpoints.Curva01_DistribuidorP10
        "CURVA_01_ROTOR_P1":                    106 + 13569,                    # Setpoints.Curva01_RotorP1
        "CURVA_01_ROTOR_P2":                    107 + 13569,                    # Setpoints.Curva01_RotorP2
        "CURVA_01_ROTOR_P3":                    108 + 13569,                    # Setpoints.Curva01_RotorP3
        "CURVA_01_ROTOR_P4":                    109 + 13569,                    # Setpoints.Curva01_RotorP4
        "CURVA_01_ROTOR_P5":                    110 + 13569,                    # Setpoints.Curva01_RotorP5
        "CURVA_01_ROTOR_P6":                    111 + 13569,                    # Setpoints.Curva01_RotorP6
        "CURVA_01_ROTOR_P7":                    112 + 13569,                    # Setpoints.Curva01_RotorP7
        "CURVA_01_ROTOR_P8":                    113 + 13569,                    # Setpoints.Curva01_RotorP8
        "CURVA_01_ROTOR_P9":                    114 + 13569,                    # Setpoints.Curva01_RotorP9
        "CURVA_01_ROTOR_P10":                   115 + 13569,                    # Setpoints.Curva01_RotorP10
        "CURVA_02_DISTRIB_P1":                  116 + 13569,                    # Setpoints.Curva02_DistribuidorP1
        "CURVA_02_DISTRIB_P2":                  117 + 13569,                    # Setpoints.Curva02_DistribuidorP2
        "CURVA_02_DISTRIB_P3":                  118 + 13569,                    # Setpoints.Curva02_DistribuidorP3
        "CURVA_02_DISTRIB_P4":                  119 + 13569,                    # Setpoints.Curva02_DistribuidorP4
        "CURVA_02_DISTRIB_P5":                  120 + 13569,                    # Setpoints.Curva02_DistribuidorP5
        "CURVA_02_DISTRIB_P6":                  121 + 13569,                    # Setpoints.Curva02_DistribuidorP6
        "CURVA_02_DISTRIB_P7":                  122 + 13569,                    # Setpoints.Curva02_DistribuidorP7
        "CURVA_02_DISTRIB_P8":                  123 + 13569,                    # Setpoints.Curva02_DistribuidorP8
        "CURVA_02_DISTRIB_P9":                  124 + 13569,                    # Setpoints.Curva02_DistribuidorP9
        "CURVA_02_DISTRIB_P10":                 125 + 13569,                    # Setpoints.Curva02_DistribuidorP10
        "CURVA_02_ROTOR_P1":                    126 + 13569,                    # Setpoints.Curva02_RotorP1
        "CURVA_02_ROTOR_P2":                    127 + 13569,                    # Setpoints.Curva02_RotorP2
        "CURVA_02_ROTOR_P3":                    128 + 13569,                    # Setpoints.Curva02_RotorP3
        "CURVA_02_ROTOR_P4":                    129 + 13569,                    # Setpoints.Curva02_RotorP4
        "CURVA_02_ROTOR_P5":                    130 + 13569,                    # Setpoints.Curva02_RotorP5
        "CURVA_02_ROTOR_P6":                    131 + 13569,                    # Setpoints.Curva02_RotorP6
        "CURVA_02_ROTOR_P7":                    132 + 13569,                    # Setpoints.Curva02_RotorP7
        "CURVA_02_ROTOR_P8":                    133 + 13569,                    # Setpoints.Curva02_RotorP8
        "CURVA_02_ROTOR_P9":                    134 + 13569,                    # Setpoints.Curva02_RotorP9
        "CURVA_02_ROTOR_P10":                   135 + 13569,                    # Setpoints.Curva02_RotorP10
        "CURVA_03_DISTRIB_P1":                  136 + 13569,                    # Setpoints.Curva03_DistribuidorP1
        "CURVA_03_DISTRIB_P2":                  137 + 13569,                    # Setpoints.Curva03_DistribuidorP2
        "CURVA_03_DISTRIB_P3":                  138 + 13569,                    # Setpoints.Curva03_DistribuidorP3
        "CURVA_03_DISTRIB_P4":                  139 + 13569,                    # Setpoints.Curva03_DistribuidorP4
        "CURVA_03_DISTRIB_P5":                  140 + 13569,                    # Setpoints.Curva03_DistribuidorP5
        "CURVA_03_DISTRIB_P6":                  141 + 13569,                    # Setpoints.Curva03_DistribuidorP6
        "CURVA_03_DISTRIB_P7":                  142 + 13569,                    # Setpoints.Curva03_DistribuidorP7
        "CURVA_03_DISTRIB_P8":                  143 + 13569,                    # Setpoints.Curva03_DistribuidorP8
        "CURVA_03_DISTRIB_P9":                  144 + 13569,                    # Setpoints.Curva03_DistribuidorP9
        "CURVA_03_DISTRIB_P10":                 145 + 13569,                    # Setpoints.Curva03_DistribuidorP10
        "CURVA_03_ROTOR_P1":                    146 + 13569,                    # Setpoints.Curva03_RotorP1
        "CURVA_03_ROTOR_P2":                    147 + 13569,                    # Setpoints.Curva03_RotorP2
        "CURVA_03_ROTOR_P3":                    148 + 13569,                    # Setpoints.Curva03_RotorP3
        "CURVA_03_ROTOR_P4":                    149 + 13569,                    # Setpoints.Curva03_RotorP4
        "CURVA_03_ROTOR_P5":                    150 + 13569,                    # Setpoints.Curva03_RotorP5
        "CURVA_03_ROTOR_P6":                    151 + 13569,                    # Setpoints.Curva03_RotorP6
        "CURVA_03_ROTOR_P7":                    152 + 13569,                    # Setpoints.Curva03_RotorP7
        "CURVA_03_ROTOR_P8":                    153 + 13569,                    # Setpoints.Curva03_RotorP8
        "CURVA_03_ROTOR_P9":                    154 + 13569,                    # Setpoints.Curva03_RotorP9
        "CURVA_03_ROTOR_P10":                   155 + 13569,                    # Setpoints.Curva03_RotorP10
        "CURVA_04_DISTRIB_P1":                  156 + 13569,                    # Setpoints.Curva04_DistribuidorP1
        "CURVA_04_DISTRIB_P2":                  157 + 13569,                    # Setpoints.Curva04_DistribuidorP2
        "CURVA_04_DISTRIB_P3":                  158 + 13569,                    # Setpoints.Curva04_DistribuidorP3
        "CURVA_04_DISTRIB_P4":                  159 + 13569,                    # Setpoints.Curva04_DistribuidorP4
        "CURVA_04_DISTRIB_P5":                  160 + 13569,                    # Setpoints.Curva04_DistribuidorP5
        "CURVA_04_DISTRIB_P6":                  161 + 13569,                    # Setpoints.Curva04_DistribuidorP6
        "CURVA_04_DISTRIB_P7":                  162 + 13569,                    # Setpoints.Curva04_DistribuidorP7
        "CURVA_04_DISTRIB_P8":                  163 + 13569,                    # Setpoints.Curva04_DistribuidorP8
        "CURVA_04_DISTRIB_P9":                  164 + 13569,                    # Setpoints.Curva04_DistribuidorP9
        "CURVA_04_DISTRIB_P10":                 165 + 13569,                    # Setpoints.Curva04_DistribuidorP10
        "CURVA_04_ROTOR_P1":                    166 + 13569,                    # Setpoints.Curva04_RotorP1
        "CURVA_04_ROTOR_P2":                    167 + 13569,                    # Setpoints.Curva04_RotorP2
        "CURVA_04_ROTOR_P3":                    168 + 13569,                    # Setpoints.Curva04_RotorP3
        "CURVA_04_ROTOR_P4":                    169 + 13569,                    # Setpoints.Curva04_RotorP4
        "CURVA_04_ROTOR_P5":                    170 + 13569,                    # Setpoints.Curva04_RotorP5
        "CURVA_04_ROTOR_P6":                    171 + 13569,                    # Setpoints.Curva04_RotorP6
        "CURVA_04_ROTOR_P7":                    172 + 13569,                    # Setpoints.Curva04_RotorP7
        "CURVA_04_ROTOR_P8":                    173 + 13569,                    # Setpoints.Curva04_RotorP8
        "CURVA_04_ROTOR_P9":                    174 + 13569,                    # Setpoints.Curva04_RotorP9
        "CURVA_04_ROTOR_P10":                   175 + 13569,                    # Setpoints.Curva04_RotorP10
        "CURVA_05_DISTRIB_P1":                  176 + 13569,                    # Setpoints.Curva05_DistribuidorP1
        "CURVA_05_DISTRIB_P2":                  177 + 13569,                    # Setpoints.Curva05_DistribuidorP2
        "CURVA_05_DISTRIB_P3":                  178 + 13569,                    # Setpoints.Curva05_DistribuidorP3
        "CURVA_05_DISTRIB_P4":                  179 + 13569,                    # Setpoints.Curva05_DistribuidorP4
        "CURVA_05_DISTRIB_P5":                  180 + 13569,                    # Setpoints.Curva05_DistribuidorP5
        "CURVA_05_DISTRIB_P6":                  181 + 13569,                    # Setpoints.Curva05_DistribuidorP6
        "CURVA_05_DISTRIB_P7":                  182 + 13569,                    # Setpoints.Curva05_DistribuidorP7
        "CURVA_05_DISTRIB_P8":                  183 + 13569,                    # Setpoints.Curva05_DistribuidorP8
        "CURVA_05_DISTRIB_P9":                  184 + 13569,                    # Setpoints.Curva05_DistribuidorP9
        "CURVA_05_DISTRIB_P10":                 185 + 13569,                    # Setpoints.Curva05_DistribuidorP10
        "CURVA_05_ROTOR_P1":                    186 + 13569,                    # Setpoints.Curva05_RotorP1
        "CURVA_05_ROTOR_P2":                    187 + 13569,                    # Setpoints.Curva05_RotorP2
        "CURVA_05_ROTOR_P3":                    188 + 13569,                    # Setpoints.Curva05_RotorP3
        "CURVA_05_ROTOR_P4":                    189 + 13569,                    # Setpoints.Curva05_RotorP4
        "CURVA_05_ROTOR_P5":                    190 + 13569,                    # Setpoints.Curva05_RotorP5
        "CURVA_05_ROTOR_P6":                    191 + 13569,                    # Setpoints.Curva05_RotorP6
        "CURVA_05_ROTOR_P7":                    192 + 13569,                    # Setpoints.Curva05_RotorP7
        "CURVA_05_ROTOR_P8":                    193 + 13569,                    # Setpoints.Curva05_RotorP8
        "CURVA_05_ROTOR_P9":                    194 + 13569,                    # Setpoints.Curva05_RotorP9
        "CURVA_05_ROTOR_P10":                   195 + 13569,                    # Setpoints.Curva05_RotorP10

        # Referencia Curva
        "REFER_CURVA_01":                       196 + 13569,                    # Setpoints.ReferenciaCurva01
        "REFER_CURVA_02":                       197 + 13569,                    # Setpoints.ReferenciaCurva02
        "REFER_CURVA_03":                       198 + 13569,                    # Setpoints.ReferenciaCurva03
        "REFER_CURVA_04":                       199 + 13569,                    # Setpoints.ReferenciaCurva04
        "REFER_CURVA_05":                       200 + 13569,                    # Setpoints.ReferenciaCurva05

        # Outros
        "TEMPO_ATUALIZACAO":                    201 + 13569,                    # Setpoints.TempoAtualizacao
        "MODO_OPERACAO_RETENTIVO":              202 + 13569,                    # Setpoints.ModoOperacao_Retentivo
        "CURVA_SEL_RETENTIVO":                  203 + 13569,                    # Setpoints.CurvaSelecionada_Retentivo


        ## LEITURAS

        # Nível
        "NV_JUSANTE":                           1 + 12764,                      # Leituras.NivelJusante
        "NV_BARRAGEM":                          2 + 12764,                      # Leituras.NivelBarragem
        "NV_CANAL":                             3 + 12764,                      # Leituras.NivelCanal
        "NV_CAMARA_CARGA":                      4 + 12764,                      # Leituras.NivelCamaraCarga
        "QUEDA_BRUTA":                          130 + 12764,                    # Leituras.QuedaBruta

        # Operação
        "OPER_PAINEL_RESET_ALARMES":            [5 + 12764, 0],                 # Leituras.Operacao_PainelResetAlarmes
        "OPER_PAINEL_RECONHECE_ALARMES":        [6 + 12764, 1],                 # Leituras.Operacao_PainelReconheceAlarmes

        "OPER_INFO":                            8 + 12764,                      # Leituras.Operacao_Info
        "OPER_EMERGENCIA":                      [8 + 12764, 0],                 # Operacao.Info.Emergencia
        "OPER_SIRENE_LIGADA":                   [8 + 12764, 1],                 # Operacao.Info.SireneLigada
        "OPER_MODO_REMOTO":                     [8 + 12764, 2],                 # Operacao.Info.OperacaoModoRemoto
        "OPER_MODO_LOCAL":                      [8 + 12764, 3],                 # Operacao.Info.OperacaoModoLocal

        "OPER_ETAPA_ALVO":                      9 + 12764,                      # Leituras.Operacao_EtapaAlvo
        "OPER_ETAPA_ALVO_UP":                   [9 + 12764, 0],                 # Operacao.EtapaAlvo.UP
        "OPER_ETAPA_ALVO_UPGM":                 [9 + 12764, 1],                 # Operacao.EtapaAlvo.UPGM
        "OPER_ETAPA_ALVO_UMD":                  [9 + 12764, 2],                 # Operacao.EtapaAlvo.UMD
        "OPER_ETAPA_ALVO_UPS":                  [9 + 12764, 3],                 # Operacao.EtapaAlvo.UPS
        "OPER_ETAPA_ALVO_US":                   [9 + 12764, 4],                 # Operacao.EtapaAlvo.US

        "OPER_ETAPA_ATUAL":                     10 + 12764,                     # Leituras.Operacao_EtapaAtual
        "OPER_ETAPA_ATUAL_UP":                  [10 + 12764, 0],                # Operacao.EtapaAtual.UP
        "OPER_ETAPA_ATUAL_UPGM":                [10 + 12764, 1],                # Operacao.EtapaAtual.UPGM
        "OPER_ETAPA_ATUAL_UMD":                 [10 + 12764, 2],                # Operacao.EtapaAtual.UMD
        "OPER_ETAPA_ATUAL_UPS":                 [10 + 12764, 3],                # Operacao.EtapaAtual.UPS
        "OPER_ETAPA_ATUAL_US":                  [10 + 12764, 4],                # Operacao.EtapaAtual.US

        "OPER_ETAPA_TRANSICAO":                 11 + 12764,                     # Leituras.Operacao_EtapaTransicao
        "OPER_ETAPA_TRANS_UP_UPGM":             [11 + 12764, 0],                # Operacao.EtapaTransicao.UPtoUPGM
        "OPER_ETAPA_TRANS_UPGM_UMD":            [11 + 12764, 1],                # Operacao.EtapaTransicao.UPGMtoUMD
        "OPER_ETAPA_TRANS_UMD_UPS":             [11 + 12764, 2],                # Operacao.EtapaTransicao.UMDtoUPS
        "OPER_ETAPA_TRANS_UPS_US":              [11 + 12764, 3],                # Operacao.EtapaTransicao.UPStoUS
        "OPER_ETAPA_TRANS_US_UPS":              [11 + 12764, 4],                # Operacao.EtapaTransicao.UStoUPS
        "OPER_ETAPA_TRANS_UPS_UMD":             [11 + 12764, 5],                # Operacao.EtapaTransicao.UPStoUMD
        "OPER_ETAPA_TRANS_UMD_UPGM":            [11 + 12764, 6],                # Operacao.EtapaTransicao.UMDtoUPGM
        "OPER_ETAPA_TRANS_UPGM_UP":             [11 + 12764, 7],                # Operacao.EtapaTransicao.UPGMtoUP

        "OPER_INFO_PARADA":                     11 + 12764,                     # Leituras.Operacao_InfoParada
        "OPER_INFO_PARADA_NORMAL":              [11 + 12764, 0],                # Operacao.InfoParada.Normal
        "OPER_INFO_PARADA_EMERG":               [11 + 12764, 1],                # Operacao.InfoParada.Emergencia
        "OPER_INFO_PARADA_TRIP_AGUA":           [11 + 12764, 2],                # Operacao.InfoParada.TRIPAgua
        "OPER_INFO_PARADA_TRIP_M":              [11 + 12764, 3],                # Operacao.InfoParada.TRIPMecanico
        "OPER_INFO_PARADA_TRIP_E":              [11 + 12764, 4],                # Operacao.InfoParada.TRIPEletrico
        "OPER_INFO_PARADA_TRIP_H":              [11 + 12764, 5],                # Operacao.InfoParada.TRIPHidraulico
        "OPER_INFO_PARADA_RELIG_AUTO":          [11 + 12764, 6],                # Operacao.InfoParada.ReligamentoAutomatico
        "OPER_INFO_PARADA_PARTIDA_MANU":        [11 + 12764, 7],                # Operacao.InfoParada.PartidaManual
        "OPER_INFO_PARADA_INFO_INVAL":          [11 + 12764, 15],               # Operacao.InfoParada.ParadaInfoValida

        # UHCT
        "UHCT_INFO":                            12 + 12764,                     # Leituras.UHCT_Info
        "UHCT_OPERACIONAL":                     [12 + 12764, 0],                # UHCT.Info.Operacional
        "UHCT_LIGADA":                          [12 + 12764, 1],                # UHCT.Info.Ligada
        "UHCT_SENS_DESATIVADO":                 [12 + 12764, 2],                # UHCT.Info.SensorDesativado
        "UHCT_MODO_LOCAL":                      [12 + 12764, 3],                # UHCT.Info.ModoLocal

        "UHCT_BOMBAS":                          13 + 12764,                     # Leituras.UHCT_Bombas
        "UHCT_BOMBAS01":                        [13 + 12764, 0],                # UHCT.Bombas.Bomba01
        "UHCT_BOMBAS02":                        [13 + 12764, 1],                # UHCT.Bombas.Bomba02
        "UHCT_BOMBAS03":                        [13 + 12764, 2],                # UHCT.Bombas.Bomba03

        "UHCT_RODIZIO":                         14 + 12764,                     # Leituras.UHCT_Rodizio
        "UHCT_RODIZ_HABILITADO":                [14 + 12764, 0],                # UHCT.Rodizio.RodizioHabilitado
        "UHCT_RODIZ_BOMBA01":                   [14 + 12764, 1],                # UHCT.Rodizio.Bomba01
        "UHCT_RODIZ_BOMBA02":                   [14 + 12764, 2],                # UHCT.Rodizio.Bomba02

        "UHCT_VALVULAS":                        15 + 12764,                     # Leituras.UHCT_Valvulas
        "UHCT_VALVULAS01":                      [15 + 12764, 0],                # UHCT.Valvulas.Valvulas01
        "UHCT_VALVULAS02":                      [15 + 12764, 1],                # UHCT.Valvulas.Valvulas02
        "UHCT_VALVULAS03":                      [15 + 12764, 2],                # UHCT.Valvulas.Valvulas03
        "UHCT_VALVULAS04":                      [15 + 12764, 3],                # UHCT.Valvulas.Valvulas04

        "UHCT_FILTROS":                         16 + 12764,                     # Leituras.UHCT_Filtros
        "UHCT_FILTROS01":                       [16 + 12764, 0],                # UHCT.Filtros.Filtro01
        "UHCT_FILTROS02":                       [16 + 12764, 1],                # UHCT.Filtros.Filtro02
        "UHCT_FILTROS03":                       [16 + 12764, 2],                # UHCT.Filtros.Filtro03
        "UHCT_FILTROS04":                       [16 + 12764, 3],                # UHCT.Filtros.Filtro04
        "UHCT_FILTROS05":                       [16 + 12764, 4],                # UHCT.Filtros.Filtro05

        "UHCT_PRESSOSTATOS":                    17 + 12764,                     # Leituras.UHCT_Pressostatos
        "UHCT_PRESSOSTATO01":                   [17 + 12764, 0],                # UHCT.Pressostatos.Pressostato01
        "UHCT_PRESSOSTATO02":                   [17 + 12764, 1],                # UHCT.Pressostatos.Pressostato02
        "UHCT_PRESSOSTATO03":                   [17 + 12764, 2],                # UHCT.Pressostatos.Pressostato03

        "UHCT_NIVEL_OLEO":                      18 + 12764,                     # Leituras.UHCT_NivelOleo
        "UHCT_NIVEL_OLEO_LL":                   [18 + 12764, 0],                # UHCT.NivelOleo.LL
        "UHCT_NIVEL_OLEO_L":                    [18 + 12764, 1],                # UHCT.NivelOleo.L
        "UHCT_NIVEL_OLEO_H":                    [18 + 12764, 2],                # UHCT.NivelOleo.H
        "UHCT_NIVEL_OLEO_HH":                   [18 + 12764, 3],                # UHCT.NivelOleo.HH

        "UHCT_PRESSAO_OLEO":                    19 + 12764,                     # Leituras.UHCT_PressaoOleo
        "UHCT_ACUM_RODIZIO_PRINCIPAL":          20 + 12764,                     # Leituras.UHCT_AcumuladorRodizioPrincipal
        "UHCT_ACUM_RODIZIO_RETAGUARDA":         21 + 12764,                     # Leituras.UHCT_AcumuladorRodizioRetaguarda

        # UHLM
        "UHLM_INFO":                            22 + 12764,                     # Leituras.UHLM_Info
        "UHLM_OPERACIONAL":                     [22 + 12764, 0],                # UHLM.Info.Operacional
        "UHLM_LIGADA":                          [22 + 12764, 1],                # UHLM.Info.Ligada
        "UHLM_MODO_LOCAL":                      [22 + 12764, 2],                # UHLM.Info.ModoLocal
        "UHLM_VALV_BOMBA_MECAN":                [22 + 12764, 3],                # UHLM.Info.UHLM_ValvulaBombaMecanica
        "UHLM_VALV_ENTRA_TRO_CALO_ABER":        [22 + 12764, 4],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Aberta
        "UHLM_VALV_ENTRA_TRO_CALO_FECH":        [22 + 12764, 5],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Fechada
        "UHLM_VALV_SAI_TRO_CALO_ABER":          [22 + 12764, 6],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Aberta
        "UHLM_VALV_SAI_TRO_CALO_FECH":          [22 + 12764, 7],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Fechada
        "UHLM_BOMBA_RETAG_OPERAC":              [22 + 12764, 8],                # UHLM.Info.UHLM_BombaRetaguarda_Operacional

        "UHLM_BOMBAS":                          23 + 12764,                     # Leituras.UHLM_Bombas
        "UHLM_BOMBA01":                         [23 + 12764, 0],                # UHLM.Bombas.Bomba01
        "UHLM_BOMBA02":                         [23 + 12764, 1],                # UHLM.Bombas.Bomba02
        "UHLM_BOMBA03":                         [23 + 12764, 2],                # UHLM.Bombas.Bomba03
        "UHLM_BOMBA04":                         [23 + 12764, 3],                # UHLM.Bombas.Bomba04

        "UHLM_RODIZIO":                         24 + 12764,                     # Leituras.UHLM_Rodizio
        "UHLM_RODIZ_HABILITADO":                [24 + 12764, 0],                # UHLM.Rodizio.RodizioHabilitado
        "UHLM_RODIZ_BOMBA01":                   [24 + 12764, 1],                # UHLM.Rodizio.Bomba01
        "UHLM_RODIZ_BOMBA02":                   [24 + 12764, 2],                # UHLM.Rodizio.Bomba02

        "UHLM_FILTROS":                         25 + 12764,                     # Leituras.UHLM_Filtros
        "UHLM_FILTRO01":                        [25 + 12764, 0],                # UHLM.Filtros.Filtro01
        "UHLM_FILTRO02":                        [25 + 12764, 1],                # UHLM.Filtros.Filtro02
        "UHLM_FILTRO03":                        [25 + 12764, 2],                # UHLM.Filtros.Filtro03
        "UHLM_FILTRO04":                        [25 + 12764, 3],                # UHLM.Filtros.Filtro04
        "UHLM_FILTRO05":                        [25 + 12764, 4],                # UHLM.Filtros.Filtro05

        "UHLM_PRESSOSTATOS":                    26 + 12764,                     # Leituras.UHLM_Pressostatos
        "UHLM_PRESSOSTATO01":                   [26 + 12764, 0],                # UHLM.Pressostatos.Pressostato01
        "UHLM_PRESSOSTATO02":                   [26 + 12764, 1],                # UHLM.Pressostatos.Pressostato02
        "UHLM_PRESSOSTATO03":                   [26 + 12764, 2],                # UHLM.Pressostatos.Pressostato03
        "UHLM_PRESSOSTATO04":                   [26 + 12764, 3],                # UHLM.Pressostatos.Pressostato04

        "UHLM_FLUXOSTATOS":                     27 + 12764,                     # Leituras.UHLM_Fluxostatos
        "UHLM_FLUXOSTATO01":                    [27 + 12764, 0],                # UHLM.Fluxostatos.Fluxostato01
        "UHLM_FLUXOSTATO02":                    [27 + 12764, 1],                # UHLM.Fluxostatos.Fluxostato02
        "UHLM_FLUXOSTATO03":                    [27 + 12764, 2],                # UHLM.Fluxostatos.Fluxostato03
        "UHLM_FLUXOSTATO04":                    [27 + 12764, 3],                # UHLM.Fluxostatos.Fluxostato04
        "UHLM_FLUXOSTATO05":                    [27 + 12764, 4],                # UHLM.Fluxostatos.Fluxostato05
        "UHLM_FLUXOSTATO06":                    [27 + 12764, 5],                # UHLM.Fluxostatos.Fluxostato06
        "UHLM_FLUXOSTATO07":                    [27 + 12764, 6],                # UHLM.Fluxostatos.Fluxostato07

        "UHLM_NIVEL_OLEO":                      28 + 12764,                     # Leituras.UHLM_NivelOleo
        "UHLM_NIVEL_OLEO_LL":                   [28 + 12764, 0],                # UHLM.NivelOleo.LL
        "UHLM_NIVEL_OLEO_L":                    [28 + 12764, 1],                # UHLM.NivelOleo.L
        "UHLM_NIVEL_OLEO_H":                    [28 + 12764, 2],                # UHLM.NivelOleo.H
        "UHLM_NIVEL_OLEO_HH":                   [28 + 12764, 3],                # UHLM.NivelOleo.HH

        "UHLM_ACUM_RODIZIO_PRINCIPAL":          29 + 12764,                     # Leituras.UHLM_AcumuladorRodizioPrincipal
        "UHLM_ACUM_RODIZIO_RETAGUARDA":         30 + 12764,                     # Leituras.UHLM_AcumuladorRodizioRetaguarda

        "UHLM_FLUXOSTATO_OLEO_01":              122 + 12764,                    # Leituras.UHLM_FluxostatoOleo01
        "UHLM_FLUXOSTATO_OLEO_02":              123 + 12764,                    # Leituras.UHLM_FluxostatoOleo02
        "UHLM_FLUXOSTATO_OLEO_03":              124 + 12764,                    # Leituras.UHLM_FluxostatoOleo03
        "UHLM_FLUXOSTATO_OLEO_04":              125 + 12764,                    # Leituras.UHLM_FluxostatoOleo04

        # Turbina
        "TURB_INFO":                            31 + 12764,                     # Leituras.Turb_Info
        "TURB_EQUALIZADA":                      [31 + 12764, 0],                # Turbina.Info.Equalizada
        "TURB_PRONTA":                          [31 + 12764, 1],                # Turbina.Info.Pronta
        "TURB_FECHADA":                         [31 + 12764, 2],                # Turbina.Info.Fechada
        "TURB_TRAVADA":                         [31 + 12764, 3],                # Turbina.Info.Travada
        "TURB_PARADA":                          [31 + 12764, 4],                # Turbina.Info.Parada
        "TURB_EQUALIZANDO":                     [31 + 12764, 5],                # Turbina.Info.Equalizando
        "TURB_FECHANDO":                        [31 + 12764, 6],                # Turbina.Info.Fechando
        "TURB_SENS_DESATIVADO":                 [31 + 12764, 7],                # Turbina.Info.SensorDesativado
        "TURB_DISTRI_FECHADO":                  [31 + 12764, 8],                # Turbina.Info.DistribuidorFechado

        "TURB_VALVULA_BYPASS":                  32 + 12764,                     # Leituras.Turb_ValvulaByPass
        "TURB_VALV_BY_ACIONA":                  [32 + 12764, 0],                # Turbina.Bypass.Acionamento
        "TURB_VALV_BY_FECHADO":                 [32 + 12764, 1],                # Turbina.Bypass.Fechado
        "TURB_VALV_BY_ABERTO":                  [32 + 12764, 2],                # Turbina.Bypass.Aberto

        "TURB_VALVULA_BORBOLETA":               33 + 12764,                     # Leituras.Turb_ValvulaBorboleta
        "TURB_VALV_BORB_ACIONA":                [33 + 12764, 0],                # Turbina.Borboleta.Acionamento
        "TURB_VALV_BORB_FECHADA":               [33 + 12764, 1],                # Turbina.Borboleta.Fechada
        "TURB_VALV_BORB_ABERTA":                [33 + 12764, 2],                # Turbina.Borboleta.Aberta
        "TURB_VALV_BORB_DERIVA":                [33 + 12764, 3],                # Turbina.Borboleta.Deriva
        "TURB_VALV_BORB_TRAVADA":               [33 + 12764, 4],                # Turbina.Borboleta.Travada
        "TURB_VALV_BORB_MANTEM":                [33 + 12764, 5],                # Turbina.Borboleta.Mantem

        "TURB_TEMPO_CRACK_EFETIVO":             34 + 12764,                     # Leituras.Turb_TempoCrackEfetivo
        "TURB_TEMPO_EQUAL_EFETIVO":             35 + 12764,                     # Leituras.Turb_TempoEqualizacaoEfetivo
        "TURB_PRESSAO_CONDUTO":                 36 + 12764,                     # Leituras.Turb_PressaoConduto
        "TURB_PRESSAO_CAIXA_ESPIRAL":           37 + 12764,                     # Leituras.Turb_PressaoCaixaEspiral
        "TURB_VAZAO_TURBINADA":                 38 + 12764,                     # Leituras.Turb_VazaoTurbinada
        "TURB_VIBRACAO_01":                     39 + 12764,                     # Leituras.Turb_Vibracao01
        "TURB_VIBRACAO_02":                     40 + 12764,                     # Leituras.Turb_Vibracao02
        "TURB_VIBRACAO_03":                     41 + 12764,                     # Leituras.Turb_Vibracao03
        "TURB_VIBRACAO_04":                     42 + 12764,                     # Leituras.Turb_Vibracao04

        "TURB_FRENAGEM":                        43 + 12764,                     # Leituras.Turb_Frenagem
        "TURB_FRENA_APLICADO":                  [43 + 12764, 0],                # Turbina.Frenagem.Info.Aplicado
        "TURB_FRENA_MANUAL":                    [43 + 12764, 1],                # Turbina.Frenagem.Info.Manual
        "TURB_FRENA_PRESSOS":                   [43 + 12764, 2],                # Turbina.Frenagem.Info.Pressostato
        "TURB_FRENA_1ZE":                       [43 + 12764, 3],                # Turbina.Frenagem.Info.[1ZE]
        "TURB_FRENA_2ZE":                       [43 + 12764, 4],                # Turbina.Frenagem.Info.[2ZE]

        "TURB_VIBRACAO_05":                     128 + 12764,                    # Leituras.Turb_Vibracao05

        # Reg V
        "REG_V_INFO":                           44 + 12764,                     # Leituras.RegV_Info
        "REG_V_HABILITADO":                     [44 + 12764, 0],                # RegV.Info.Habilitado
        "REG_V_BASE_CARGA":                     [44 + 12764, 1],                # RegV.Info.BaseCarga
        "REG_V_RPM30":                          [44 + 12764, 2],                # RegV.Info.RPM30
        "REG_V_RPM90":                          [44 + 12764, 3],                # RegV.Info.RPM90
        "REG_V_CARGA_ZERADA":                   [44 + 12764, 4],                # RegV.Info.CargaZerada
        "REG_V_MODO_ESTATISMO":                 [44 + 12764, 5],                # RegV.Info.ModoEstatismo
        "REG_V_MODO_BASE_CARGA":                [44 + 12764, 6],                # RegV.Info.ModoBaseCarga
        "REG_V_DISTRI_FECHADO":                 [44 + 12764, 7],                # RegV.Info.DistribuidorFechado

        "REG_V_ESTADO":                         45 + 12764,                     # Leituras.RegV_Estado
        "REG_V_FALHA":                          [45 + 12764, 0],                # RegV.Estado.Falha
        "REG_V_PARADO":                         [45 + 12764, 1],                # RegV.Estado.Parado
        "REG_V_CTRL_MANUAL_DISTRI":             [45 + 12764, 2],                # RegV.Estado.ControleManualDistribuidor
        "REG_V_CTRL_MANUAL_VALV":               [45 + 12764, 3],                # RegV.Estado.ControleManualValvula
        "REG_V_CTRL_VELOC":                     [45 + 12764, 4],                # RegV.Estado.ControleVelocidade
        "REG_V_COMPENSA_POT_ATIVA":             [45 + 12764, 5],                # RegV.Estado.CompensacaoPotenciaAtiva
        "REG_V_CTRL_POT_ATIVA":                 [45 + 12764, 6],                # RegV.Estado.ControlePotenciaAtiva

        "REG_V_VELOCIDADE":                     46 + 12764,                     # Leituras.RegV_Velocidade
        "REG_V_DISTRIBUIDOR":                   47 + 12764,                     # Leituras.RegV_Distribuidor
        "REG_V_ROTOR":                          48 + 12764,                     # Leituras.RegV_Rotor
        "REG_V_POT_ALVO":                       49 + 12764,                     # Leituras.RegV_PotenciaAlvo

        "REG_V_CONJUGADO_INFO":                 127 + 12764,                    # Leituras.RegV_CurvaConjugacao_Info
        "REG_V_CONJ_AUTOMATICO":                [127 + 12764, 0],               # RegV.Conjugado.Automatico
        "REG_V_CONJ_MANUAL":                    [127 + 12764, 1],               # RegV.Conjugado.Manual
        "REG_V_CONJUGADO1":                     [127 + 12764, 2],               # RegV.Conjugado.Conjugado1
        "REG_V_CONJUGADO2":                     [127 + 12764, 3],               # RegV.Conjugado.Conjugado2
        "REG_V_CONJUGADO3":                     [127 + 12764, 4],               # RegV.Conjugado.Conjugado3

        # Reg T
        "REG_T_INFO":                           50 + 12764,                     # Leituras.RegT_Info
        "REG_T_HABILITACAO":                    [50 + 12764, 0],                # RegT.Info.Habilitacao
        "REG_T_TENSAO_ESTAB":                   [50 + 12764, 1],                # RegT.Info.TensaoEstabilizada
        "REG_T_CONTATOR_ABERTO":                [50 + 12764, 2],                # RegT.Info.ContatorAberto
        "REG_T_CONTATOR_FECHADO":               [50 + 12764, 3],                # RegT.Info.ContatorFechado
        "REG_T_PRE_EXCITACAO":                  [50 + 12764, 4],                # RegT.Info.PreExcitacao
        "REG_T_MTVC":                           [50 + 12764, 5],                # RegT.Info.MTVC
        "REG_T_MECC":                           [50 + 12764, 6],                # RegT.Info.MECC
        "REG_T_OPER_ONLINE":                    [50 + 12764, 7],                # RegT.Info.OperacaoOnline
        "REG_T_OPER_PARALELA":                  [50 + 12764, 9],                # RegT.Info.OperacaoParalela

        "REG_T_UEXCITACAO":                     51 + 12764,                     # Leituras.RegT_UExcitacao
        "REG_T_IEXCITACAO":                     52 + 12764,                     # Leituras.RegT_IExcitacao
        "REG_T_FPALVO":                         128 + 12764,                    # Leituras.RegT_FPAlvo
        "REG_T_REATIVO_ALVO":                   129 + 12764,                    # Leituras.RegT_ReativoAlvo

        # Sinc
        "SINC_INFO":                            53 + 12764,                     # Leituras.Sinc_Info
        "SINC_HABILITADO":                      [53 + 12764, 0],                # Sincronoscopio.Info.Habilitado
        "SINC_MODO_AUTO":                       [53 + 12764, 1],                # Sincronoscopio.Info.ModoAutomatico
        "SINC_MODO_MANUAL":                     [53 + 12764, 2],                # Sincronoscopio.Info.ModoManual
        "SINC_BARRA_MORTA":                     [53 + 12764, 3],                # Sincronoscopio.Info.BarraMorta

        "SINC_FREQ_GERADOR":                    54 + 12764,                     # Leituras.Sinc_FrequenciaGerador
        "SINC_FREQ_BARRA":                      55 + 12764,                     # Leituras.Sinc_FrequenciaBarra
        "SINC_TENSAO_GERADOR":                  56 + 12764,                     # Leituras.Sinc_TensaoGerador
        "SINC_TENSAO_BARRA":                    57 + 12764,                     # Leituras.Sinc_TensaoBarra

        # DJ
        "Dj52G_INFO":                           58 + 12764,                     # Leituras.Disj52G_Info
        "Dj52G_ABERTO":                         [58 + 12764, 0],                # Disjuntor52G.Info.Aberto
        "Dj52G_FECHADO":                        [58 + 12764, 1],                # Disjuntor52G.Info.Fechado
        "Dj52G_INCONSISTENTE":                  [58 + 12764, 2],                # Disjuntor52G.Info.Inconsistente
        "Dj52G_TRIP":                           [58 + 12764, 3],                # Disjuntor52G.Info.TRIP
        "Dj52G_TESTE":                          [58 + 12764, 4],                # Disjuntor52G.Info.Teste
        "Dj52G_INSERIDO":                       [58 + 12764, 5],                # Disjuntor52G.Info.Inserido
        "Dj52G_EXTRAIVEL":                      [58 + 12764, 6],                # Disjuntor52G.Info.Extraivel
        "Dj52G_MOLA_CARRE":                     [58 + 12764, 7],                # Disjuntor52G.Info.MolaCarregada
        "Dj52G_CONDICAO":                       [58 + 12764, 8],                # Disjuntor52G.Info.CondicaoFechamento
        "Dj52G_FALTA_VCC":                      [58 + 12764, 9],                # Disjuntor52G.Info.FaltaVCC

        # Tensão
        "TENSAO_RN":                            59 + 12764,                     # Leituras.Gerador_TensaoRN
        "TENSAO_SN":                            60 + 12764,                     # Leituras.Gerador_TensaoSN
        "TENSAO_TN":                            61 + 12764,                     # Leituras.Gerador_TensaoTN
        "TENSAO_RS":                            62 + 12764,                     # Leituras.Gerador_TensaoRS
        "TENSAO_ST":                            63 + 12764,                     # Leituras.Gerador_TensaoST
        "TENSAO_TR":                            64 + 12764,                     # Leituras.Gerador_TensaoTR

        # Corrente
        "CORRENTE_R":                           65 + 12764,                     # Leituras.Gerador_CorrenteR
        "CORRENTE_S":                           66 + 12764,                     # Leituras.Gerador_CorrenteS
        "CORRENTE_T":                           67 + 12764,                     # Leituras.Gerador_CorrenteT
        "CORRENTE_MEDIA":                       68 + 12764,                     # Leituras.Gerador_CorrenteMedia

        # Potência Ativa
        "POT_ATIVA_1":                          69 + 12764,                     # Leituras.Gerador_PotenciaAtiva1
        "POT_ATIVA_2":                          70 + 12764,                     # Leituras.Gerador_PotenciaAtiva2
        "POT_ATIVA_3":                          71 + 12764,                     # Leituras.Gerador_PotenciaAtiva3
        "POT_ATIVA_MEDIA":                      72 + 12764,                     # Leituras.Gerador_PotenciaAtivaMedia

        # Potência Reativa
        "POT_REATIVA_1":                        73 + 12764,                     # Leituras.Gerador_PotenciaReativa1
        "POT_REATIVA_2":                        74 + 12764,                     # Leituras.Gerador_PotenciaReativa2
        "POT_REATIVA_3":                        75 + 12764,                     # Leituras.Gerador_PotenciaReativa3
        "POT_REATIVA_MEDIA":                    76 + 12764,                     # Leituras.Gerador_PotenciaReativaMedia

        # Potência Aparente
        "POT_APARENTE_1":                       77 + 12764,                     # Leituras.Gerador_PotenciaAparente1
        "POT_APARENTE_2":                       78 + 12764,                     # Leituras.Gerador_PotenciaAparente2
        "POT_APARENTE_3":                       79 + 12764,                     # Leituras.Gerador_PotenciaAparente3
        "POT_APARENTE_MEDIA":                   80 + 12764,                     # Leituras.Gerador_PotenciaAparenteMedia

        # Fator Potência
        "FATOR_POT_1":                          81 + 12764,                     # Leituras.Gerador_FatorPotencia1
        "FATOR_POT_2":                          82 + 12764,                     # Leituras.Gerador_FatorPotencia2
        "FATOR_POT_3":                          83 + 12764,                     # Leituras.Gerador_FatorPotencia3
        "FATOR_POT_MEDIA":                      84 + 12764,                     # Leituras.Gerador_FatorPotenciaMedia

        # Frequencia
        "FREQUENCIA":                           85 + 12764,                     # Leituras.Gerador_Frequencia

        # Energia Fornecida
        "ENERGIA_FORNECIDA_TWh":                86 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTWh
        "ENERGIA_FORNECIDA_GWh":                87 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGWh
        "ENERGIA_FORNECIDA_MWh":                88 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMWh
        "ENERGIA_FORNECIDA_kWh":                89 + 12764,                     # Leituras.Gerador_EnergiaFornecidakWh
        "ENERGIA_FORNECIDA_TVarh":              90 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTVarh
        "ENERGIA_FORNECIDA_GVarh":              91 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGVarh
        "ENERGIA_FORNECIDA_MVarh":              92 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMVarh
        "ENERGIA_FORNECIDA_kVarh":              93 + 12764,                     # Leituras.Gerador_EnergiaFornecidakVarh
        "ENERGIA_CORNECIDA_TVarh":              94 + 12764,                     # Leituras.Gerador_EnergiaConsumidaTVarh
        "ENERGIA_CORNECIDA_GVarh":              95 + 12764,                     # Leituras.Gerador_EnergiaConsumidaGVarh
        "ENERGIA_CORNECIDA_MVarh":              96 + 12764,                     # Leituras.Gerador_EnergiaConsumidaMVarh
        "ENERGIA_CORNECIDA_kVarh":              97 + 12764,                     # Leituras.Gerador_EnergiaConsumidakVarh

        "GERADOR_FP_INFO":                      98 + 12764,                     # Leituras.Gerador_FPInfo
        "GERADOR_FP_FASE1_IND":                 [98 + 12764, 0],                # Gerador.FP_Info.Fase1_Ind
        "GERADOR_FP_FASE1_CAP":                 [98 + 12764, 1],                # Gerador.FP_Info.Fase1_Cap
        "GERADOR_FP_FASE2_IND":                 [98 + 12764, 2],                # Gerador.FP_Info.Fase2_Ind
        "GERADOR_FP_FASE2_CAP":                 [98 + 12764, 3],                # Gerador.FP_Info.Fase2_Cap
        "GERADOR_FP_FASE3_IND":                 [98 + 12764, 4],                # Gerador.FP_Info.Fase3_Ind
        "GERADOR_FP_FASE3_CAP":                 [98 + 12764, 5],                # Gerador.FP_Info.Fase3_Cap
        "GERADOR_FP_FASE4_IND":                 [98 + 12764, 6],                # Gerador.FP_Info.Total_Ind
        "GERADOR_FP_FASE4_CAP":                 [98 + 12764, 7],                # Gerador.FP_Info.Total_Cap

        # Controles
        "CTRL_REATIVO_INFO":                    99 + 12764,                    # Leituras.CtrlReativo_Info
        "CTRL_REAT_MODO_FP":                    [99 + 12764, 0],               # CtrlReativo.Info.ModoFP
        "CTRL_REAT_MODO_VAR":                   [99 + 12764, 1],               # CtrlReativo.Info.ModoVar

        "CTRL_POTENCIA_INFO":                   100 + 12764,                    # Leituras.CtrlPotencia_Info
        "CTRL_POT_MODO_NIVEL":                  [100 + 12764, 0],               # CtrlPotencia.Info.ModoNivel
        "CTRL_POT_MODO_POT":                    [100 + 12764, 1],               # CtrlPotencia.Info.ModoPotencia
        "CTRL_POT_MODO_RELIGA_AUTO":            [100 + 12764, 2],               # CtrlPotencia.Info.ModoReligamentoAutomatico

        # Horimetros
        "HORIM_ELETR_LOW":                      101 + 12764,                    # Leituras.HorimetroEletrico_Low
        "HORIM_ELETR_HIGH":                     102 + 12764,                    # Leituras.HorimetroEletrico_High
        "HORIM_MECAN_LOW":                      103 + 12764,                    # Leituras.HorimetroMecanico_Low
        "HORIM_MECAN_HIGH":                     104 + 12764,                    # Leituras.HorimetroMecanico_High

        # Temperatura
        "TEMPERATURA_01":                       106 + 12764,                    # Leituras.Temperatura_01
        "TEMPERATURA_02":                       107 + 12764,                    # Leituras.Temperatura_02
        "TEMPERATURA_03":                       108 + 12764,                    # Leituras.Temperatura_03
        "TEMPERATURA_04":                       109 + 12764,                    # Leituras.Temperatura_04
        "TEMPERATURA_05":                       110 + 12764,                    # Leituras.Temperatura_05
        "TEMPERATURA_06":                       111 + 12764,                    # Leituras.Temperatura_06
        "TEMPERATURA_07":                       112 + 12764,                    # Leituras.Temperatura_07
        "TEMPERATURA_08":                       113 + 12764,                    # Leituras.Temperatura_08
        "TEMPERATURA_09":                       114 + 12764,                    # Leituras.Temperatura_09
        "TEMPERATURA_10":                       115 + 12764,                    # Leituras.Temperatura_10
        "TEMPERATURA_11":                       116 + 12764,                    # Leituras.Temperatura_11
        "TEMPERATURA_12":                       117 + 12764,                    # Leituras.Temperatura_12
        "TEMPERATURA_13":                       118 + 12764,                    # Leituras.Temperatura_13
        "TEMPERATURA_14":                       119 + 12764,                    # Leituras.Temperatura_14
        "TEMPERATURA_15":                       120 + 12764,                    # Leituras.Temperatura_15
        "TEMPERATURA_16":                       121 + 12764,                    # Leituras.Temperatura_16


        ## DISJUNTORES

        "DJ_01":                                0 + 12564,                      # Disjuntor Q125.0 - Alimentação Circuitos de Comando                                  -> condic_indisponibiliza UG1
        "DJ_02":                                0 + 12564,                      # Disjuntor Q125.1 - Alimentação GRTD2000                                              -> condic_indisponibiliza UG1
        "DJ_03":                                1 + 12564,                      # Disjuntor Q125.2 - Alimentação Relés de Proteção                                     -> condic_indisponibiliza UG1
        "DJ_04":                                2 + 12564,                      # Disjuntor Q24.0 - Alimentação Válvula Proporcional e Transdutor de Posição           -> condic_indisponibiliza UG1
        "DJ_05":                                3 + 12564,                      # CSG - Disjuntor Q220.1 - Alimentação Carregamento de Mola                            -> condic_indisponibiliza UG1
        "DJ_06":                                4 + 12564,                      # CSG - Disjuntor Q125.0 - Alimentação Circuito de Comando 52G                         -> condic_indisponibiliza UG1
        "DJ_07":                                5 + 12564,                      # Q49 - Disjuntor Q125.0 UG1 - Alimentação SEL2600
        "DJ_08":                                6 + 12564,                      # Disjuntor Motor QM1 - Bomba de Óleo 01 da UHCT                                       -> condic_indisponibiliza UG1
        "DJ_09":                                7 + 12564,                      # Disjuntor Motor QM2 - Bomba de Óleo 02 da UHCT                                       -> condic_indisponibiliza UG1
        "DJ_10":                                8 + 12564,                      # Disjuntor Motor QM3 - Bomba de Óleo 01 da UHLM                                       -> condic_indisponibiliza UG1
        "DJ_11":                                9 + 12564,                     #
        "DJ_12":                                10 + 12564,                     #
        "DJ_13":                                11 + 12564,                     #
        "DJ_14":                                12 + 12564,                     #
        "DJ_15":                                13 + 12564,                     #
        "DJ_16":                                14 + 12564,                     #
        "DJ_17":                                15 + 12564,                     #
        "DJ_18":                                16 + 12564,                     #
        "DJ_19":                                17 + 12564,                     #
        "DJ_20":                                18 + 12564,                     #
        "DJ_21":                                19 + 12564,                     #
        "DJ_22":                                20 + 12564,                     #
        "DJ_23":                                21 + 12564,                     #
        "DJ_24":                                22 + 12564,                     #
        "DJ_25":                                23 + 12564,                     #
        "DJ_26":                                24 + 12564,                     #
        "DJ_27":                                25 + 12564,                     #
        "DJ_28":                                26 + 12564,                     #
        "DJ_29":                                27 + 12564,                     #
        "DJ_30":                                28 + 12564,                     #
        "DJ_31":                                29 + 12564,                     #
        "DJ_32":                                30 + 12564,                     #


        ## ALARMES

        
        # Específicos UG3
        "Alarme10_12":                          [9 + 14199, 12],
        "Alarme10_13":                          [9 + 14199, 13],

        "Alarme13_05":                          [12 + 14199, 5],
        "Alarme13_06":                          [12 + 14199, 6],
        "Alarme13_07":                          [12 + 14199, 7],
        "Alarme13_08":                          [12 + 14199, 8],
        "Alarme13_09":                          [12 + 14199, 9],
        "Alarme13_10":                          [12 + 14199, 10],
        "Alarme13_11":                          [12 + 14199, 11],

        "Alarme16_00":                          [15 + 14199, 0],
        "Alarme16_01":                          [15 + 14199, 1],

        # Gerais
        "Alarme01_00":                          [0 + 14199, 0],
        "Alarme01_01":                          [0 + 14199, 1],
        "Alarme01_02":                          [0 + 14199, 2],
        "Alarme01_03":                          [0 + 14199, 3],
        "Alarme01_06":                          [0 + 14199, 6],
        "Alarme01_07":                          [0 + 14199, 7],
        "Alarme01_08":                          [0 + 14199, 8],
        "Alarme01_09":                          [0 + 14199, 9],
        "Alarme01_10":                          [0 + 14199, 10],
        "Alarme01_11":                          [0 + 14199, 11],
        "Alarme01_12":                          [0 + 14199, 12],
        "Alarme01_13":                          [0 + 14199, 13],
        "Alarme01_14":                          [0 + 14199, 14],
        "Alarme01_15":                          [0 + 14199, 15],

        "Alarme02_00":                          [1 + 14199, 0],
        "Alarme02_01":                          [1 + 14199, 1],
        "Alarme02_02":                          [1 + 14199, 2],
        "Alarme02_03":                          [1 + 14199, 3],
        "Alarme02_04":                          [1 + 14199, 4],
        "Alarme02_05":                          [1 + 14199, 5],
        "Alarme02_06":                          [1 + 14199, 6],
        "Alarme02_07":                          [1 + 14199, 7],
        "Alarme02_08":                          [1 + 14199, 8],
        "Alarme02_09":                          [1 + 14199, 9],
        "Alarme02_10":                          [1 + 14199, 10],
        "Alarme02_11":                          [1 + 14199, 11],
        "Alarme02_12":                          [1 + 14199, 12],
        "Alarme02_13":                          [1 + 14199, 13],
        "Alarme02_14":                          [1 + 14199, 14],
        "Alarme02_15":                          [1 + 14199, 15],

        "Alarme03_00":                          [2 + 14199, 0],
        "Alarme03_01":                          [2 + 14199, 1],
        "Alarme03_02":                          [2 + 14199, 2],
        "Alarme03_03":                          [2 + 14199, 3],
        "Alarme03_04":                          [2 + 14199, 4],
        "Alarme03_05":                          [2 + 14199, 5],
        "Alarme03_06":                          [2 + 14199, 6],
        "Alarme03_07":                          [2 + 14199, 7],
        "Alarme03_08":                          [2 + 14199, 8],
        "Alarme03_09":                          [2 + 14199, 9],
        "Alarme03_10":                          [2 + 14199, 10],
        "Alarme03_11":                          [2 + 14199, 11],
        "Alarme03_12":                          [2 + 14199, 12],
        "Alarme03_13":                          [2 + 14199, 13],
        "Alarme03_14":                          [2 + 14199, 14],
        "Alarme03_15":                          [2 + 14199, 15],

        "Alarme04_00":                          [3 + 14199, 0],
        "Alarme04_01":                          [3 + 14199, 1],
        "Alarme04_02":                          [3 + 14199, 2],
        "Alarme04_04":                          [3 + 14199, 4],
        "Alarme04_05":                          [3 + 14199, 5],
        "Alarme04_06":                          [3 + 14199, 6],
        "Alarme04_07":                          [3 + 14199, 7],
        "Alarme04_09":                          [3 + 14199, 9],
        "Alarme04_10":                          [3 + 14199, 10],
        "Alarme04_11":                          [3 + 14199, 11],
        "Alarme04_12":                          [3 + 14199, 12],
        "Alarme04_13":                          [3 + 14199, 13],
        "Alarme04_14":                          [3 + 14199, 14],
        "Alarme04_15":                          [3 + 14199, 15],

        "Alarme05_00":                          [4 + 14199, 0],
        "Alarme05_02":                          [4 + 14199, 2],
        "Alarme05_03":                          [4 + 14199, 3],
        "Alarme05_04":                          [4 + 14199, 4],
        "Alarme05_05":                          [4 + 14199, 5],
        "Alarme05_06":                          [4 + 14199, 6],
        "Alarme05_07":                          [4 + 14199, 7],
        "Alarme05_09":                          [4 + 14199, 9],
        "Alarme05_10":                          [4 + 14199, 10],
        "Alarme05_11":                          [4 + 14199, 11],
        "Alarme05_12":                          [4 + 14199, 12],
        "Alarme05_13":                          [4 + 14199, 13],
        "Alarme05_14":                          [4 + 14199, 14],
        "Alarme05_15":                          [4 + 14199, 15],

        "Alarme06_00":                          [5 + 14199, 0],
        "Alarme06_03":                          [5 + 14199, 3],
        "Alarme06_04":                          [5 + 14199, 4],
        "Alarme06_05":                          [5 + 14199, 5],
        "Alarme06_08":                          [5 + 14199, 8],
        "Alarme06_09":                          [5 + 14199, 9],
        "Alarme06_10":                          [5 + 14199, 10],
        "Alarme06_11":                          [5 + 14199, 11],
        "Alarme06_12":                          [5 + 14199, 12],
        "Alarme06_13":                          [5 + 14199, 13],
        "Alarme06_14":                          [5 + 14199, 14],
        "Alarme06_15":                          [5 + 14199, 15],

        "Alarme07_00":                          [6 + 14199, 0],
        "Alarme07_01":                          [6 + 14199, 1],
        "Alarme07_02":                          [6 + 14199, 2],
        "Alarme07_03":                          [6 + 14199, 3],
        "Alarme07_06":                          [6 + 14199, 6],
        "Alarme07_07":                          [6 + 14199, 7],
        "Alarme07_08":                          [6 + 14199, 8],
        "Alarme07_09":                          [6 + 14199, 9],
        "Alarme07_10":                          [6 + 14199, 10],
        "Alarme07_11":                          [6 + 14199, 11],
        "Alarme07_12":                          [6 + 14199, 12],
        "Alarme07_13":                          [6 + 14199, 13],
        "Alarme07_14":                          [6 + 14199, 14],
        "Alarme07_15":                          [6 + 14199, 15],

        "Alarme08_00":                          [7 + 14199, 0],
        "Alarme08_01":                          [7 + 14199, 1],
        "Alarme08_02":                          [7 + 14199, 2],
        "Alarme08_03":                          [7 + 14199, 3],
        "Alarme08_07":                          [7 + 14199, 7],
        "Alarme08_08":                          [7 + 14199, 8],
        "Alarme08_09":                          [7 + 14199, 9],
        "Alarme08_10":                          [7 + 14199, 10],
        "Alarme08_11":                          [7 + 14199, 11],
        "Alarme08_12":                          [7 + 14199, 12],
        "Alarme08_13":                          [7 + 14199, 13],
        "Alarme08_14":                          [7 + 14199, 14],
        "Alarme08_15":                          [7 + 14199, 15],

        "Alarme09_00":                          [8 + 14199, 0],
        "Alarme09_01":                          [8 + 14199, 1],
        "Alarme09_02":                          [8 + 14199, 2],
        "Alarme09_03":                          [8 + 14199, 3],
        "Alarme09_04":                          [8 + 14199, 4],
        "Alarme09_06":                          [8 + 14199, 6],
        "Alarme09_07":                          [8 + 14199, 7],
        "Alarme09_08":                          [8 + 14199, 8],
        "Alarme09_09":                          [8 + 14199, 9],
        "Alarme09_10":                          [8 + 14199, 10],
        "Alarme09_11":                          [8 + 14199, 11],
        "Alarme09_12":                          [8 + 14199, 12],
        "Alarme09_13":                          [8 + 14199, 13],
        "Alarme09_14":                          [8 + 14199, 14],
        "Alarme09_15":                          [8 + 14199, 15],

        "Alarme10_00":                          [9 + 14199, 0],
        "Alarme10_01":                          [9 + 14199, 1],
        "Alarme10_02":                          [9 + 14199, 2],
        "Alarme10_03":                          [9 + 14199, 3],
        "Alarme10_05":                          [9 + 14199, 5],
        "Alarme10_06":                          [9 + 14199, 6],
        "Alarme10_07":                          [9 + 14199, 7],
        "Alarme10_08":                          [9 + 14199, 8],
        "Alarme10_09":                          [9 + 14199, 9],
        "Alarme10_10":                          [9 + 14199, 10],
        "Alarme10_11":                          [9 + 14199, 11],
        "Alarme10_12":                          [9 + 14199, 12],
        "Alarme10_13":                          [9 + 14199, 13],
        "Alarme10_14":                          [9 + 14199, 14],
        "Alarme10_15":                          [9 + 14199, 15],

        "Alarme11_00":                          [10 + 14199, 0],
        "Alarme11_01":                          [10 + 14199, 1],
        "Alarme11_02":                          [10 + 14199, 2],
        "Alarme11_06":                          [10 + 14199, 6],
        "Alarme11_07":                          [10 + 14199, 7],
        "Alarme11_08":                          [10 + 14199, 8],
        "Alarme11_09":                          [10 + 14199, 9],
        "Alarme11_10":                          [10 + 14199, 10],
        "Alarme11_11":                          [10 + 14199, 11],
        "Alarme11_12":                          [10 + 14199, 12],
        "Alarme11_13":                          [10 + 14199, 13],
        "Alarme11_14":                          [10 + 14199, 14],
        "Alarme11_15":                          [10 + 14199, 15],

        "Alarme12_01":                          [11 + 14199, 1],
        "Alarme12_02":                          [11 + 14199, 2],
        "Alarme12_03":                          [11 + 14199, 3],
        "Alarme12_04":                          [11 + 14199, 4],
        "Alarme12_05":                          [11 + 14199, 5],
        "Alarme12_06":                          [11 + 14199, 6],
        "Alarme12_07":                          [11 + 14199, 7],
        "Alarme12_09":                          [11 + 14199, 9],
        "Alarme12_10":                          [11 + 14199, 10],
        "Alarme12_11":                          [11 + 14199, 11],
        "Alarme12_12":                          [11 + 14199, 12],
        "Alarme12_13":                          [11 + 14199, 13],
        "Alarme12_14":                          [11 + 14199, 14],
        "Alarme12_15":                          [11 + 14199, 15],

        "Alarme13_00":                          [12 + 14199, 0],
        "Alarme13_01":                          [12 + 14199, 1],
        "Alarme13_02":                          [12 + 14199, 2],
        "Alarme13_03":                          [12 + 14199, 3],
        "Alarme13_09":                          [12 + 14199, 9],
        "Alarme13_10":                          [12 + 14199, 10],
        "Alarme13_11":                          [12 + 14199, 11],
        "Alarme13_12":                          [12 + 14199, 12],
        "Alarme13_13":                          [12 + 14199, 13],
        "Alarme13_14":                          [12 + 14199, 14],
        "Alarme13_15":                          [12 + 14199, 15],

        "Alarme14_00":                          [13 + 14199, 0],
        "Alarme14_01":                          [13 + 14199, 1],
        "Alarme14_02":                          [13 + 14199, 2],
        "Alarme14_03":                          [13 + 14199, 3],
        "Alarme14_04":                          [13 + 14199, 4],
        "Alarme14_05":                          [13 + 14199, 5],
        "Alarme14_10":                          [13 + 14199, 10],
        "Alarme14_11":                          [13 + 14199, 11],
        "Alarme14_12":                          [13 + 14199, 12],
        "Alarme14_13":                          [13 + 14199, 13],
        "Alarme14_14":                          [13 + 14199, 14],
        "Alarme14_15":                          [13 + 14199, 15],

        "Alarme15_00":                          [14 + 14199, 0],
        "Alarme15_01":                          [14 + 14199, 1],
        "Alarme15_02":                          [14 + 14199, 2],
        "Alarme15_03":                          [14 + 14199, 3],
        "Alarme15_04":                          [14 + 14199, 4],
        "Alarme15_05":                          [14 + 14199, 5],
        "Alarme15_06":                          [14 + 14199, 6],
        "Alarme15_07":                          [14 + 14199, 7],
        "Alarme15_08":                          [14 + 14199, 8],
        "Alarme15_09":                          [14 + 14199, 9],
        "Alarme15_10":                          [14 + 14199, 10],
        "Alarme15_12":                          [14 + 14199, 12],
        "Alarme15_13":                          [14 + 14199, 13],
        "Alarme15_14":                          [14 + 14199, 14],
        "Alarme15_15":                          [14 + 14199, 15],

        "Alarme16_00":                          [15 + 14199, 0],
        "Alarme16_01":                          [15 + 14199, 1],
        "Alarme16_02":                          [15 + 14199, 2],
        "Alarme16_03":                          [15 + 14199, 3],
        "Alarme16_04":                          [15 + 14199, 4],
        "Alarme16_05":                          [15 + 14199, 5],
        "Alarme16_06":                          [15 + 14199, 6],
        "Alarme16_07":                          [15 + 14199, 7],
        "Alarme16_08":                          [15 + 14199, 8],
        "Alarme16_09":                          [15 + 14199, 9],
        "Alarme16_10":                          [15 + 14199, 10],
        "Alarme16_11":                          [15 + 14199, 11],
        "Alarme16_12":                          [15 + 14199, 12],
    },
    "UG4": {
        ## COMANDOS
        # Gerais
        "CMD_RESET_ALARMES":                    0 + 12288,                      # Comandos.Operacao_PCH_AdoPopinhakResetAlarmes
        "CMD_RECONHECE_ALARMES":                0 + 12289,                      # Comandos.Operacao_PCH_AdoPopinhakReconheceAlarmes

        # Operação
        "CMD_OPER_UP":                          1 + 12289,                      # Comandos.Operacao_UP
        "CMD_OPER_UPGM":                        2 + 12289,                      # Comandos.Operacao_UPGM
        "CMD_OPER_UVD":                         3 + 12289,                      # Comandos.Operacao_UVD
        "CMD_OPER_UPS":                         4 + 12289,                      # Comandos.Operacao_UPS
        "CMD_OPER_US":                          5 + 12289,                      # Comandos.Operacao_US
        "CMD_OPER_EMERGENCIA_LIGAR":            6 + 12289,                      # Comandos.Operacao_EmergenciaLigar
        "CMD_OPER_EMERGENCIA_DESLIGAR":         7 + 12289,                      # Comandos.Operacao_EmergenciaDesligar
        "CMD_OPER_PARADA_RESET":                71 + 12289,                     # Comandos.Operacao_ParadaReset

        # Turbina
        "CMD_TURB_BYPASS_ABRIR":                8 + 12289,                      # Comandos.Turb_ByPassAbrir
        "CMD_TURB_BYPASS_FECHAR":               9 + 12289,                     # Comandos.Turb_ByPassFechar
        "CMD_TURB_BORBOLETA_ABRIR":             10 + 12289,                     # Comandos.Turb_BorboletaAbrir
        "CMD_TURB_BORBOLETA_FECHAR":            11 + 12289,                     # Comandos.Turb_BorboletaFechar
        "CMD_TURB_FRENAGEM_APLICAR":            12 + 12289,                     # Comandos.Turb_FrenagemAplicar
        "CMD_TURB_FRENAGEM_DESAPLICAR":         13 + 12289,                     # Comandos.Turb_FrenagemDesaplicar
        "CMD_TURB_FRENAGEM_MANUAL":             14 + 12289,                     # Comandos.Turb_FrenagemManual
        "CMD_TURB_FRENAGEM_AUTO":               15 + 12289,                     # Comandos.Turb_FrenagemAuto
        "CMD_TURB_SENSOR_ATIVAR":               16 + 12289,                     # Comandos.Turb_SensorAtivar
        "CMD_TURB_SENSOR_DESATIVAR":            17 + 12289,                     # Comandos.Turb_SensorDesativar

        # Reg V
        "CMD_REG_V_PARTIR":                     18 + 12289,                     # Comandos.RegV_Partir
        "CMD_REG_V_PARAR":                      19 + 12289,                     # Comandos.RegV_Parar
        "CMD_REG_V_COLOCAR_CARGA":              20 + 12289,                     # Comandos.RegV_ColocarCarga
        "CMD_REG_V_RETIRAR_CARGA":              21 + 12289,                     # Comandos.RegV_RetirarCarga
        "CMD_REG_V_INCREMENTA_VELOCIDADE":      22 + 12289,                     # Comandos.RegV_IncrementaVelocidade
        "CMD_REG_V_DECREMENTA_VELOCIDADE":      23 + 12289,                     # Comandos.RegV_DecrementaVelocidade
        "CMD_REG_V_SEL_MODO_ESTATISMO":         24 + 12289,                     # Comandos.RegV_SelecionaModoEstatismo
        "CMD_REG_V_SEL_MODO_BASECARGA":         25 + 12289,                     # Comandos.RegV_SelecionaModoBaseCarga

        # Reg T
        "CMD_REG_T_LIGAR":                      26 + 12289,                     # Comandos.RegT_Ligar
        "CMD_REG_T_DESLIGAR":                   27 + 12289,                     # Comandos.RegT_Desligar
        "CMD_REG_T_INCREMENTA_TENSAO":          28 + 12289,                     # Comandos.RegT_IncrementaTensao
        "CMD_REG_T_DECREMENTA_TENSAO":          29 + 12289,                     # Comandos.RegT_DecrementaTensao
        "CMD_REG_T_PRE_EXCITACAO":              30 + 12289,                     # Comandos.RegT_PreExcitacao

        # Sinc
        "CMD_SINC_LIGAR":                       31 + 12289,                     # Comandos.Sinc_Ligar
        "CMD_SINC_DESLIGAR":                    32 + 12289,                     # Comandos.Sinc_Desligar
        "CMD_SINC_MODO_AUTO_LIGAR":             33 + 12289,                     # Comandos.Sinc_ModoAutoLigar
        "CMD_SINC_MODO_MANUAL_LIGAR":           34 + 12289,                     # Comandos.Sinc_ModoManualLigar
        "CMD_SINC_MODO_BMORTA_LIGAR":           35 + 12289,                     # Comandos.Sinc_ModoBMortaLigar

        # DJ52G
        "CMD_DJ52G_ABRIR":                      36 + 12289,                     # Comandos.Disj52G_Abrir

        # Controle Reativo
        "CMD_CTRL_REATIVO_MODO_FPLIGAR":        37 + 12289,                     # Comandos.CtrlReativo_ModoFPLigar
        "CMD_CTRL_REATIVO_MODO_FPDESLIGAR":     38 + 12289,                     # Comandos.CtrlReativo_ModoFPDesligar
        "CMD_CTRL_REATIVO_MODO_VArLIGAR":       39 + 12289,                     # Comandos.CtrlReativo_ModoVArLigar
        "CMD_CTRL_REATIVO_MODO_VArDESLIGAR":    40 + 12289,                     # Comandos.CtrlReativo_ModoVArDesligar

        # Controle Potência
        "CMD_CTRL_POT_MODO_POT_LIGAR":          41 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaLigar
        "CMD_CTRL_POT_MODO_POT_DESLIGAR":       42 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaDesligar
        "CMD_CTRL_POT_MODO_NIVEL_LIGAR":        43 + 12289,                     # Comandos.CtrlPotencia_ModoNivelLigar
        "CMD_CTRL_POT_MODO_NIVEL_DESLIGAR":     44 + 12289,                     # Comandos.CtrlPotencia_ModoNivelDesligar
        "CMD_CTRL_POT_RELI_AUTO_LIGAR":         45 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoLigar
        "CMD_CTRL_POT_RELI_AUTO_DESLIGAR":      46 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoDesligar

        # UHCT
        "CMD_UHCT_BOMBA_01_LIGAR":              47 + 12289,                     # Comandos.UHCT_Bomba01Ligar
        "CMD_UHCT_BOMBA_01_DESLIGAR":           48 + 12289,                     # Comandos.UHCT_Bomba01Desligar
        "CMD_UHCT_BOMBA_01_PRINCIPAL":          49 + 12289,                     # Comandos.UHCT_Bomba01Principal
        "CMD_UHCT_BOMBA_02_LIGAR":              50 + 12289,                     # Comandos.UHCT_Bomba02Ligar
        "CMD_UHCT_BOMBA_02_DESLIGAR":           51 + 12289,                     # Comandos.UHCT_Bomba02Desligar
        "CMD_UHCT_BOMBA_02_PRINCIPAL":          52 + 12289,                     # Comandos.UHCT_Bomba02Principal
        "CMD_UHCT_BOMBA_AGUA_LIGAR":            53 + 12289,                     # Comandos.UHCT_BombaAguaLigar
        "CMD_UHCT_BOMBA_AGUA_DESLIGAR":         54 + 12289,                     # Comandos.UHCT_BombaAguaDesligar
        "CMD_UHCT_SENSOR_ATIVAR":               55 + 12289,                     # Comandos.UHCT_SensorAtivar
        "CMD_UHCT_SENSOR_DESATIVAR":            56 + 12289,                     # Comandos.UHCT_SensorDesativar
        "CMD_UHCT_RODIZIO_HABILITAR":           57 + 12289,                     # Comandos.UHCT_RodizioHabilitar
        "CMD_UHCT_RODIZIO_DESABILITAR":         58 + 12289,                     # Comandos.UHCT_RodizioDesabilitar

        # UHLM
        "CMD_UHLM_BOMBA_01_LIGAR":              59 + 12289,                     # Comandos.UHLM_Bomba01Ligar
        "CMD_UHLM_BOMBA_01_DESLIGAR":           60 + 12289,                     # Comandos.UHLM_Bomba01Desligar
        "CMD_UHLM_BOMBA_01_PRINCIPAL":          61 + 12289,                     # Comandos.UHLM_Bomba01Principal
        "CMD_UHLM_BOMBA_02_LIGAR":              62 + 12289,                     # Comandos.UHLM_Bomba02Ligar
        "CMD_UHLM_BOMBA_02_DESLIGAR":           63 + 12289,                     # Comandos.UHLM_Bomba02Desligar
        "CMD_UHLM_BOMBA_02_PRINCIPAL":          64 + 12289,                     # Comandos.UHLM_Bomba02Principal
        "CMD_UHLM_BOMBA_JACKING_LIGA":          65 + 12289,                     # Comandos.UHLM_BombaJackingLiga
        "CMD_UHLM_BOMBA_JACKING_DESLIGA":       66 + 12289,                     # Comandos.UHLM_BombaJackingDesliga
        "CMD_UHLM_BOMBA_AGUA_LIGA":             67 + 12289,                     # Comandos.UHLM_BombaAguaLiga
        "CMD_UHLM_BOMBA_AGUA_DESLIGA":          68 + 12289,                     # Comandos.UHLM_BombaAguaDesliga
        "CMD_UHLM_RODIZIO_HABILITAR":           69 + 12289,                     # Comandos.UHLM_RodizioHabilitar
        "CMD_UHLM_RODIZIO_DESABILITAR":         70 + 12289,                     # Comandos.UHLM_RodizioDesabilitar

        # RT
        "CMD_RT_MTVC_HABILITAR":                71 + 12289,                     # Comandos.RT_MTVC_Habilitar
        "CMD_RT_MECC_HABILITAR":                72 + 12289,                     # Comandos.RT_MECC_Habilitar
        "CMD_RT_ONLINE_HABILITAR":              73 + 12289,                     # Comandos.RT_Online_habilitar
        "CMD_RT_ONLINE_DESABILITAR":            74 + 12289,                     # Comandos.RT_Online_Desabiltar
        "CMD_RT_PARALELO_HABILITAR":            75 + 12289,                     # Comandos.RT_Paralelo_habilitar
        "CMD_RT_PARALELO_DESABILITAR":          76 + 12289,                     # Comandos.RT_Paralelo_Desabilitar

        # RV
        "CMD_RV_CONJUGADO_AUTO_HABILITAR":      77 + 12289,                     # Comandos.RV_ConjugadoAuto_habilitar
        "CMD_RV_CONJUGADO_MANUAL_HABILITAR":    78 + 12289,                     # Comandos.RV_ConjugadoManual_habilitar
        "CMD_RV_CONJUGADO_01_HABILITAR":        79 + 12289,                     # Comandos.RV_Conjugado01_habilitar
        "CMD_RV_CONJUGADO_02_HABILITAR":        80 + 12289,                     # Comandos.RV_Conjugado02_habilitar
        "CMD_RV_CONJUGADO_03_HABILITAR":        81 + 12289,                     # Comandos.RV_Conjugado03_habilitar
        "CMD_RV_CONJUGADO_04_HABILITAR":        82 + 12289,                     # Comandos.RV_Conjugado04_habilitar
        "CMD_RV_CONJUGADO_05_HABILITAR":        83 + 12289,                     # Comandos.RV_Conjugado05_habilitar


        ## SETPOINTS

        # UHCT
        "UHCT_PRESSAO_MAX":                     0 + 13569,                      # Setpoints.UHCT_PressaoMaxima
        "UHCT_PRESSAO_MIN":                     0 + 13569,                      # Setpoints.UHCT_PressaoMinima
        "UHCT_PRESSAO_DESLIGAMENTO":            1 + 13569,                      # Setpoints.UHCT_PressaoDesligamento
        "UHCT_PRESSAO_CRITICA":                 2 + 13569,                      # Setpoints.UHCT_PressaoCritica

        # Controle Potência
        "CRTL_POT_NIVEL_LL1":                   3 + 13569,                      # Setpoints.CtrlPotencia_NivelLL1
        "CRTL_POT_NIVEL_LL2":                   4 + 13569,                      # Setpoints.CtrlPotencia_NivelLL2
        "CRTL_POT_NIVEL_LL3":                   5 + 13569,                      # Setpoints.CtrlPotencia_NivelLL3
        "CRTL_POT_NIVEL_LL4":                   6 + 13569,                      # Setpoints.CtrlPotencia_NivelLL4
        "CRTL_POT_NIVEL_LL5":                   7 + 13569,                      # Setpoints.CtrlPotencia_NivelLL5
        "CRTL_POT_POT_1":                       8 + 13569,                      # Setpoints.CtrlPotencia_Potencia1
        "CRTL_POT_POT_2":                       9 + 13569,                     # Setpoints.CtrlPotencia_Potencia2
        "CRTL_POT_POT_3":                       10 + 13569,                     # Setpoints.CtrlPotencia_Potencia3
        "CRTL_POT_POT_4":                       11 + 13569,                     # Setpoints.CtrlPotencia_Potencia4
        "CRTL_POT_POT_5":                       12 + 13569,                     # Setpoints.CtrlPotencia_Potencia5
        "CRTL_POT_POT_MIN":                     13 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinima
        "CRTL_POT_POT_MIN_TEMPO":               14 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinimaTempo
        "CRTL_POT_NIVEL_RELIGAMENTO":           15 + 13569,                     # Setpoints.CtrlPotencia_NivelReligamento
        "CRTL_POT_ALVO":                        16 + 13569,                     # Setpoints.CtrlPotencia_Alvo
        "CRTL_POT_TOLERANCIA":                  17 + 13569,                     # Setpoints.CtrlPotencia_Tolerancia
        "CRTL_POT_PULSO_TEMPO":                 18 + 13569,                     # Setpoints.CtrlPotencia_PulsoTempo
        "CRTL_POT_PULSO_INTERVALO":             19 + 13569,                     # Setpoints.CtrlPotencia_PulsoIntervalo
        "CRTL_POT_SP_NIVEL":                    20 + 13569,                     # Setpoints.CtrlPotencia_SetpointNivel
        "CRTL_POT_NIVEL_MIN_ALARME":            21 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoAlarme
        "CRTL_POT_NIVEL_MIN_TRIP":              22 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoTRIP
        "CTRL_POT_POT_MAX":                     88 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMaxima

        # Controle Reativo
        "CRTL_REATIVO_SP_FP":                   23 + 13569,                     # Setpoints.CtrlReativo_SetpointFP
        "CRTL_REATIVO_SP_REATIVO":              24 + 13569,                     # Setpoints.CtrlReativo_SetpointReativo

        # Turbina
        "TURB_VIBRA_01_ALARME":                 25 + 13569,                     # Setpoints.Turb_Vibracao01Alarme
        "TURB_VIBRA_01_TRIP":                   26 + 13569,                     # Setpoints.Turb_Vibracao01TRIP
        "TURB_VIBRA_02_ALARME":                 27 + 13569,                     # Setpoints.Turb_Vibracao02Alarme
        "TURB_VIBRA_02_TRIP":                   28 + 13569,                     # Setpoints.Turb_Vibracao02TRIP
        "TURB_VIBRA_03_ALARME":                 29 + 13569,                     # Setpoints.Turb_Vibracao03Alarme
        "TURB_VIBRA_03_TRIP":                   30 + 13569,                     # Setpoints.Turb_Vibracao03TRIP
        "TURB_VIBRA_04_ALARME":                 31 + 13569,                     # Setpoints.Turb_Vibracao04Alarme
        "TURB_VIBRA_04_TRIP":                   32 + 13569,                     # Setpoints.Turb_Vibracao04TRIP
        "TURB_TEMPO_EQUALI_SP":                 33 + 13569,                     # Setpoints.Turb_TempoEqualizacaoSetpoint
        "TURB_VIBRA_05_ALARME":                 89 + 13569,                     # Setpoints.Turb_Vibracao05Alarme
        "TURB_VIBRA_05_TRIP":                   90 + 13569,                     # Setpoints.Turb_Vibracao05TRIP

        # Freio
        "FREIO_PULSO_INTERVALO":                34 + 13569,                     # Setpoints.Freio_PulsoIntervalo
        "FREIO_PULSO_TEMPO":                    35 + 13569,                     # Setpoints.Freio_PulsoTempo

        # UHCT
        "UHCT_RODIZIO_PRINCIPAL":               36 + 13569,                     # Setpoints.UHCT_RodizioPrincipal
        "UHCT_RODIZIO_RETAGUARDA":              37 + 13569,                     # Setpoints.UHCT_RodizioRetaguarda

        # UHLM
        "UHLM_RODIZIO_PRINCIPAL":               38 + 13569,                     # Setpoints.UHLM_RodizioPrincipal
        "UHLM_RODIZIO_RETAGUARDA":              39 + 13569,                     # Setpoints.UHLM_RodizioRetaguarda
        "UHLM_SP_VAZAO_01":                     91 + 13569,                     # Setpoints.UHLM_SetpointVazao01
        "UHLM_SP_VAZAO_02":                     92 + 13569,                     # Setpoints.UHLM_SetpointVazao02
        "UHLM_SP_VAZAO_03":                     93 + 13569,                     # Setpoints.UHLM_SetpointVazao03
        "UHLM_SP_VAZAO_04":                     94 + 13569,                     # Setpoints.UHLM_SetpointVazao04

        # Temperaturas
        "TEMPERATURA_01_ALARME":                40 + 13569,                     # Setpoints.Temperatura01_Alarme
        "TEMPERATURA_02_ALARME":                41 + 13569,                     # Setpoints.Temperatura02_Alarme
        "TEMPERATURA_03_ALARME":                42 + 13569,                     # Setpoints.Temperatura03_Alarme
        "TEMPERATURA_04_ALARME":                43 + 13569,                     # Setpoints.Temperatura04_Alarme
        "TEMPERATURA_05_ALARME":                44 + 13569,                     # Setpoints.Temperatura05_Alarme
        "TEMPERATURA_06_ALARME":                45 + 13569,                     # Setpoints.Temperatura06_Alarme
        "TEMPERATURA_07_ALARME":                46 + 13569,                     # Setpoints.Temperatura07_Alarme
        "TEMPERATURA_08_ALARME":                47 + 13569,                     # Setpoints.Temperatura08_Alarme
        "TEMPERATURA_09_ALARME":                48 + 13569,                     # Setpoints.Temperatura09_Alarme
        "TEMPERATURA_10_ALARME":                49 + 13569,                     # Setpoints.Temperatura10_Alarme
        "TEMPERATURA_11_ALARME":                50 + 13569,                     # Setpoints.Temperatura11_Alarme
        "TEMPERATURA_12_ALARME":                51 + 13569,                     # Setpoints.Temperatura12_Alarme
        "TEMPERATURA_13_ALARME":                52 + 13569,                     # Setpoints.Temperatura13_Alarme
        "TEMPERATURA_14_ALARME":                53 + 13569,                     # Setpoints.Temperatura14_Alarme
        "TEMPERATURA_15_ALARME":                54 + 13569,                     # Setpoints.Temperatura15_Alarme
        "TEMPERATURA_16_ALARME":                55 + 13569,                     # Setpoints.Temperatura16_Alarme
        "TEMPERATURA_01_TRIP01":                56 + 13569,                     # Setpoints.Temperatura01_TRIP01
        "TEMPERATURA_02_TRIP01":                57 + 13569,                     # Setpoints.Temperatura02_TRIP01
        "TEMPERATURA_03_TRIP01":                58 + 13569,                     # Setpoints.Temperatura03_TRIP01
        "TEMPERATURA_04_TRIP01":                59 + 13569,                     # Setpoints.Temperatura04_TRIP01
        "TEMPERATURA_05_TRIP01":                60 + 13569,                     # Setpoints.Temperatura05_TRIP01
        "TEMPERATURA_06_TRIP01":                61 + 13569,                     # Setpoints.Temperatura06_TRIP01
        "TEMPERATURA_07_TRIP01":                62 + 13569,                     # Setpoints.Temperatura07_TRIP01
        "TEMPERATURA_08_TRIP01":                63 + 13569,                     # Setpoints.Temperatura08_TRIP01
        "TEMPERATURA_09_TRIP01":                64 + 13569,                     # Setpoints.Temperatura09_TRIP01
        "TEMPERATURA_10_TRIP01":                65 + 13569,                     # Setpoints.Temperatura10_TRIP01
        "TEMPERATURA_11_TRIP01":                66 + 13569,                     # Setpoints.Temperatura11_TRIP01
        "TEMPERATURA_12_TRIP01":                67 + 13569,                     # Setpoints.Temperatura12_TRIP01
        "TEMPERATURA_13_TRIP01":                68 + 13569,                     # Setpoints.Temperatura13_TRIP01
        "TEMPERATURA_14_TRIP01":                69 + 13569,                     # Setpoints.Temperatura14_TRIP01
        "TEMPERATURA_15_TRIP01":                70 + 13569,                     # Setpoints.Temperatura15_TRIP01
        "TEMPERATURA_16_TRIP01":                71 + 13569,                     # Setpoints.Temperatura16_TRIP01
        "TEMPERATURA_01_TRIP02":                72 + 13569,                     # Setpoints.Temperatura01_TRIP02
        "TEMPERATURA_02_TRIP02":                73 + 13569,                     # Setpoints.Temperatura02_TRIP02
        "TEMPERATURA_03_TRIP02":                74 + 13569,                     # Setpoints.Temperatura03_TRIP02
        "TEMPERATURA_04_TRIP02":                75 + 13569,                     # Setpoints.Temperatura04_TRIP02
        "TEMPERATURA_05_TRIP02":                76 + 13569,                     # Setpoints.Temperatura05_TRIP02
        "TEMPERATURA_06_TRIP02":                77 + 13569,                     # Setpoints.Temperatura06_TRIP02
        "TEMPERATURA_07_TRIP02":                78 + 13569,                     # Setpoints.Temperatura07_TRIP02
        "TEMPERATURA_08_TRIP02":                79 + 13569,                     # Setpoints.Temperatura08_TRIP02
        "TEMPERATURA_09_TRIP02":                80 + 13569,                     # Setpoints.Temperatura09_TRIP02
        "TEMPERATURA_10_TRIP02":                81 + 13569,                     # Setpoints.Temperatura10_TRIP02
        "TEMPERATURA_11_TRIP02":                82 + 13569,                     # Setpoints.Temperatura11_TRIP02
        "TEMPERATURA_12_TRIP02":                83 + 13569,                     # Setpoints.Temperatura12_TRIP02
        "TEMPERATURA_13_TRIP02":                84 + 13569,                     # Setpoints.Temperatura13_TRIP02
        "TEMPERATURA_14_TRIP02":                85 + 13569,                     # Setpoints.Temperatura14_TRIP02
        "TEMPERATURA_15_TRIP02":                86 + 13569,                     # Setpoints.Temperatura15_TRIP02
        "TEMPERATURA_16_TRIP02":                87 + 13569,                     # Setpoints.Temperatura16_TRIP02

        # Grade Suja
        "GradeSuja_TRIP":                       95 + 13569,                     # Setpoints.GradeSuja_TRIP

        # Curva
        "CURVA_01_DISTRIB_P1":                  96 + 13569,                     # Setpoints.Curva01_DistribuidorP1
        "CURVA_01_DISTRIB_P2":                  97 + 13569,                     # Setpoints.Curva01_DistribuidorP2
        "CURVA_01_DISTRIB_P3":                  98 + 13569,                     # Setpoints.Curva01_DistribuidorP3
        "CURVA_01_DISTRIB_P4":                  99 + 13569,                    # Setpoints.Curva01_DistribuidorP4
        "CURVA_01_DISTRIB_P5":                  100 + 13569,                    # Setpoints.Curva01_DistribuidorP5
        "CURVA_01_DISTRIB_P6":                  101 + 13569,                    # Setpoints.Curva01_DistribuidorP6
        "CURVA_01_DISTRIB_P7":                  102 + 13569,                    # Setpoints.Curva01_DistribuidorP7
        "CURVA_01_DISTRIB_P8":                  103 + 13569,                    # Setpoints.Curva01_DistribuidorP8
        "CURVA_01_DISTRIB_P9":                  104 + 13569,                    # Setpoints.Curva01_DistribuidorP9
        "CURVA_01_DISTRIB_P10":                 105 + 13569,                    # Setpoints.Curva01_DistribuidorP10
        "CURVA_01_ROTOR_P1":                    106 + 13569,                    # Setpoints.Curva01_RotorP1
        "CURVA_01_ROTOR_P2":                    107 + 13569,                    # Setpoints.Curva01_RotorP2
        "CURVA_01_ROTOR_P3":                    108 + 13569,                    # Setpoints.Curva01_RotorP3
        "CURVA_01_ROTOR_P4":                    109 + 13569,                    # Setpoints.Curva01_RotorP4
        "CURVA_01_ROTOR_P5":                    110 + 13569,                    # Setpoints.Curva01_RotorP5
        "CURVA_01_ROTOR_P6":                    111 + 13569,                    # Setpoints.Curva01_RotorP6
        "CURVA_01_ROTOR_P7":                    112 + 13569,                    # Setpoints.Curva01_RotorP7
        "CURVA_01_ROTOR_P8":                    113 + 13569,                    # Setpoints.Curva01_RotorP8
        "CURVA_01_ROTOR_P9":                    114 + 13569,                    # Setpoints.Curva01_RotorP9
        "CURVA_01_ROTOR_P10":                   115 + 13569,                    # Setpoints.Curva01_RotorP10
        "CURVA_02_DISTRIB_P1":                  116 + 13569,                    # Setpoints.Curva02_DistribuidorP1
        "CURVA_02_DISTRIB_P2":                  117 + 13569,                    # Setpoints.Curva02_DistribuidorP2
        "CURVA_02_DISTRIB_P3":                  118 + 13569,                    # Setpoints.Curva02_DistribuidorP3
        "CURVA_02_DISTRIB_P4":                  119 + 13569,                    # Setpoints.Curva02_DistribuidorP4
        "CURVA_02_DISTRIB_P5":                  120 + 13569,                    # Setpoints.Curva02_DistribuidorP5
        "CURVA_02_DISTRIB_P6":                  121 + 13569,                    # Setpoints.Curva02_DistribuidorP6
        "CURVA_02_DISTRIB_P7":                  122 + 13569,                    # Setpoints.Curva02_DistribuidorP7
        "CURVA_02_DISTRIB_P8":                  123 + 13569,                    # Setpoints.Curva02_DistribuidorP8
        "CURVA_02_DISTRIB_P9":                  124 + 13569,                    # Setpoints.Curva02_DistribuidorP9
        "CURVA_02_DISTRIB_P10":                 125 + 13569,                    # Setpoints.Curva02_DistribuidorP10
        "CURVA_02_ROTOR_P1":                    126 + 13569,                    # Setpoints.Curva02_RotorP1
        "CURVA_02_ROTOR_P2":                    127 + 13569,                    # Setpoints.Curva02_RotorP2
        "CURVA_02_ROTOR_P3":                    128 + 13569,                    # Setpoints.Curva02_RotorP3
        "CURVA_02_ROTOR_P4":                    129 + 13569,                    # Setpoints.Curva02_RotorP4
        "CURVA_02_ROTOR_P5":                    130 + 13569,                    # Setpoints.Curva02_RotorP5
        "CURVA_02_ROTOR_P6":                    131 + 13569,                    # Setpoints.Curva02_RotorP6
        "CURVA_02_ROTOR_P7":                    132 + 13569,                    # Setpoints.Curva02_RotorP7
        "CURVA_02_ROTOR_P8":                    133 + 13569,                    # Setpoints.Curva02_RotorP8
        "CURVA_02_ROTOR_P9":                    134 + 13569,                    # Setpoints.Curva02_RotorP9
        "CURVA_02_ROTOR_P10":                   135 + 13569,                    # Setpoints.Curva02_RotorP10
        "CURVA_03_DISTRIB_P1":                  136 + 13569,                    # Setpoints.Curva03_DistribuidorP1
        "CURVA_03_DISTRIB_P2":                  137 + 13569,                    # Setpoints.Curva03_DistribuidorP2
        "CURVA_03_DISTRIB_P3":                  138 + 13569,                    # Setpoints.Curva03_DistribuidorP3
        "CURVA_03_DISTRIB_P4":                  139 + 13569,                    # Setpoints.Curva03_DistribuidorP4
        "CURVA_03_DISTRIB_P5":                  140 + 13569,                    # Setpoints.Curva03_DistribuidorP5
        "CURVA_03_DISTRIB_P6":                  141 + 13569,                    # Setpoints.Curva03_DistribuidorP6
        "CURVA_03_DISTRIB_P7":                  142 + 13569,                    # Setpoints.Curva03_DistribuidorP7
        "CURVA_03_DISTRIB_P8":                  143 + 13569,                    # Setpoints.Curva03_DistribuidorP8
        "CURVA_03_DISTRIB_P9":                  144 + 13569,                    # Setpoints.Curva03_DistribuidorP9
        "CURVA_03_DISTRIB_P10":                 145 + 13569,                    # Setpoints.Curva03_DistribuidorP10
        "CURVA_03_ROTOR_P1":                    146 + 13569,                    # Setpoints.Curva03_RotorP1
        "CURVA_03_ROTOR_P2":                    147 + 13569,                    # Setpoints.Curva03_RotorP2
        "CURVA_03_ROTOR_P3":                    148 + 13569,                    # Setpoints.Curva03_RotorP3
        "CURVA_03_ROTOR_P4":                    149 + 13569,                    # Setpoints.Curva03_RotorP4
        "CURVA_03_ROTOR_P5":                    150 + 13569,                    # Setpoints.Curva03_RotorP5
        "CURVA_03_ROTOR_P6":                    151 + 13569,                    # Setpoints.Curva03_RotorP6
        "CURVA_03_ROTOR_P7":                    152 + 13569,                    # Setpoints.Curva03_RotorP7
        "CURVA_03_ROTOR_P8":                    153 + 13569,                    # Setpoints.Curva03_RotorP8
        "CURVA_03_ROTOR_P9":                    154 + 13569,                    # Setpoints.Curva03_RotorP9
        "CURVA_03_ROTOR_P10":                   155 + 13569,                    # Setpoints.Curva03_RotorP10
        "CURVA_04_DISTRIB_P1":                  156 + 13569,                    # Setpoints.Curva04_DistribuidorP1
        "CURVA_04_DISTRIB_P2":                  157 + 13569,                    # Setpoints.Curva04_DistribuidorP2
        "CURVA_04_DISTRIB_P3":                  158 + 13569,                    # Setpoints.Curva04_DistribuidorP3
        "CURVA_04_DISTRIB_P4":                  159 + 13569,                    # Setpoints.Curva04_DistribuidorP4
        "CURVA_04_DISTRIB_P5":                  160 + 13569,                    # Setpoints.Curva04_DistribuidorP5
        "CURVA_04_DISTRIB_P6":                  161 + 13569,                    # Setpoints.Curva04_DistribuidorP6
        "CURVA_04_DISTRIB_P7":                  162 + 13569,                    # Setpoints.Curva04_DistribuidorP7
        "CURVA_04_DISTRIB_P8":                  163 + 13569,                    # Setpoints.Curva04_DistribuidorP8
        "CURVA_04_DISTRIB_P9":                  164 + 13569,                    # Setpoints.Curva04_DistribuidorP9
        "CURVA_04_DISTRIB_P10":                 165 + 13569,                    # Setpoints.Curva04_DistribuidorP10
        "CURVA_04_ROTOR_P1":                    166 + 13569,                    # Setpoints.Curva04_RotorP1
        "CURVA_04_ROTOR_P2":                    167 + 13569,                    # Setpoints.Curva04_RotorP2
        "CURVA_04_ROTOR_P3":                    168 + 13569,                    # Setpoints.Curva04_RotorP3
        "CURVA_04_ROTOR_P4":                    169 + 13569,                    # Setpoints.Curva04_RotorP4
        "CURVA_04_ROTOR_P5":                    170 + 13569,                    # Setpoints.Curva04_RotorP5
        "CURVA_04_ROTOR_P6":                    171 + 13569,                    # Setpoints.Curva04_RotorP6
        "CURVA_04_ROTOR_P7":                    172 + 13569,                    # Setpoints.Curva04_RotorP7
        "CURVA_04_ROTOR_P8":                    173 + 13569,                    # Setpoints.Curva04_RotorP8
        "CURVA_04_ROTOR_P9":                    174 + 13569,                    # Setpoints.Curva04_RotorP9
        "CURVA_04_ROTOR_P10":                   175 + 13569,                    # Setpoints.Curva04_RotorP10
        "CURVA_05_DISTRIB_P1":                  176 + 13569,                    # Setpoints.Curva05_DistribuidorP1
        "CURVA_05_DISTRIB_P2":                  177 + 13569,                    # Setpoints.Curva05_DistribuidorP2
        "CURVA_05_DISTRIB_P3":                  178 + 13569,                    # Setpoints.Curva05_DistribuidorP3
        "CURVA_05_DISTRIB_P4":                  179 + 13569,                    # Setpoints.Curva05_DistribuidorP4
        "CURVA_05_DISTRIB_P5":                  180 + 13569,                    # Setpoints.Curva05_DistribuidorP5
        "CURVA_05_DISTRIB_P6":                  181 + 13569,                    # Setpoints.Curva05_DistribuidorP6
        "CURVA_05_DISTRIB_P7":                  182 + 13569,                    # Setpoints.Curva05_DistribuidorP7
        "CURVA_05_DISTRIB_P8":                  183 + 13569,                    # Setpoints.Curva05_DistribuidorP8
        "CURVA_05_DISTRIB_P9":                  184 + 13569,                    # Setpoints.Curva05_DistribuidorP9
        "CURVA_05_DISTRIB_P10":                 185 + 13569,                    # Setpoints.Curva05_DistribuidorP10
        "CURVA_05_ROTOR_P1":                    186 + 13569,                    # Setpoints.Curva05_RotorP1
        "CURVA_05_ROTOR_P2":                    187 + 13569,                    # Setpoints.Curva05_RotorP2
        "CURVA_05_ROTOR_P3":                    188 + 13569,                    # Setpoints.Curva05_RotorP3
        "CURVA_05_ROTOR_P4":                    189 + 13569,                    # Setpoints.Curva05_RotorP4
        "CURVA_05_ROTOR_P5":                    190 + 13569,                    # Setpoints.Curva05_RotorP5
        "CURVA_05_ROTOR_P6":                    191 + 13569,                    # Setpoints.Curva05_RotorP6
        "CURVA_05_ROTOR_P7":                    192 + 13569,                    # Setpoints.Curva05_RotorP7
        "CURVA_05_ROTOR_P8":                    193 + 13569,                    # Setpoints.Curva05_RotorP8
        "CURVA_05_ROTOR_P9":                    194 + 13569,                    # Setpoints.Curva05_RotorP9
        "CURVA_05_ROTOR_P10":                   195 + 13569,                    # Setpoints.Curva05_RotorP10

        # Referencia Curva
        "REFER_CURVA_01":                       196 + 13569,                    # Setpoints.ReferenciaCurva01
        "REFER_CURVA_02":                       197 + 13569,                    # Setpoints.ReferenciaCurva02
        "REFER_CURVA_03":                       198 + 13569,                    # Setpoints.ReferenciaCurva03
        "REFER_CURVA_04":                       199 + 13569,                    # Setpoints.ReferenciaCurva04
        "REFER_CURVA_05":                       200 + 13569,                    # Setpoints.ReferenciaCurva05

        # Outros
        "TEMPO_ATUALIZACAO":                    201 + 13569,                    # Setpoints.TempoAtualizacao
        "MODO_OPERACAO_RETENTIVO":              202 + 13569,                    # Setpoints.ModoOperacao_Retentivo
        "CURVA_SEL_RETENTIVO":                  203 + 13569,                    # Setpoints.CurvaSelecionada_Retentivo


        ## LEITURAS

        # Nível
        "NV_JUSANTE":                           1 + 12764,                      # Leituras.NivelJusante
        "NV_BARRAGEM":                          2 + 12764,                      # Leituras.NivelBarragem
        "NV_CANAL":                             3 + 12764,                      # Leituras.NivelCanal
        "NV_CAMARA_CARGA":                      4 + 12764,                      # Leituras.NivelCamaraCarga
        "QUEDA_BRUTA":                          130 + 12764,                    # Leituras.QuedaBruta

        # Operação
        "OPER_PAINEL_RESET_ALARMES":            [5 + 12764, 0],                 # Leituras.Operacao_PainelResetAlarmes
        "OPER_PAINEL_RECONHECE_ALARMES":        [6 + 12764, 1],                 # Leituras.Operacao_PainelReconheceAlarmes

        "OPER_INFO":                            8 + 12764,                      # Leituras.Operacao_Info
        "OPER_EMERGENCIA":                      [8 + 12764, 0],                 # Operacao.Info.Emergencia
        "OPER_SIRENE_LIGADA":                   [8 + 12764, 1],                 # Operacao.Info.SireneLigada
        "OPER_MODO_REMOTO":                     [8 + 12764, 2],                 # Operacao.Info.OperacaoModoRemoto
        "OPER_MODO_LOCAL":                      [8 + 12764, 3],                 # Operacao.Info.OperacaoModoLocal

        "OPER_ETAPA_ALVO":                      9 + 12764,                      # Leituras.Operacao_EtapaAlvo
        "OPER_ETAPA_ALVO_UP":                   [9 + 12764, 0],                 # Operacao.EtapaAlvo.UP
        "OPER_ETAPA_ALVO_UPGM":                 [9 + 12764, 1],                 # Operacao.EtapaAlvo.UPGM
        "OPER_ETAPA_ALVO_UMD":                  [9 + 12764, 2],                 # Operacao.EtapaAlvo.UMD
        "OPER_ETAPA_ALVO_UPS":                  [9 + 12764, 3],                 # Operacao.EtapaAlvo.UPS
        "OPER_ETAPA_ALVO_US":                   [9 + 12764, 4],                 # Operacao.EtapaAlvo.US

        "OPER_ETAPA_ATUAL":                     10 + 12764,                     # Leituras.Operacao_EtapaAtual
        "OPER_ETAPA_ATUAL_UP":                  [10 + 12764, 0],                # Operacao.EtapaAtual.UP
        "OPER_ETAPA_ATUAL_UPGM":                [10 + 12764, 1],                # Operacao.EtapaAtual.UPGM
        "OPER_ETAPA_ATUAL_UMD":                 [10 + 12764, 2],                # Operacao.EtapaAtual.UMD
        "OPER_ETAPA_ATUAL_UPS":                 [10 + 12764, 3],                # Operacao.EtapaAtual.UPS
        "OPER_ETAPA_ATUAL_US":                  [10 + 12764, 4],                # Operacao.EtapaAtual.US

        "OPER_ETAPA_TRANSICAO":                 11 + 12764,                     # Leituras.Operacao_EtapaTransicao
        "OPER_ETAPA_TRANS_UP_UPGM":             [11 + 12764, 0],                # Operacao.EtapaTransicao.UPtoUPGM
        "OPER_ETAPA_TRANS_UPGM_UMD":            [11 + 12764, 1],                # Operacao.EtapaTransicao.UPGMtoUMD
        "OPER_ETAPA_TRANS_UMD_UPS":             [11 + 12764, 2],                # Operacao.EtapaTransicao.UMDtoUPS
        "OPER_ETAPA_TRANS_UPS_US":              [11 + 12764, 3],                # Operacao.EtapaTransicao.UPStoUS
        "OPER_ETAPA_TRANS_US_UPS":              [11 + 12764, 4],                # Operacao.EtapaTransicao.UStoUPS
        "OPER_ETAPA_TRANS_UPS_UMD":             [11 + 12764, 5],                # Operacao.EtapaTransicao.UPStoUMD
        "OPER_ETAPA_TRANS_UMD_UPGM":            [11 + 12764, 6],                # Operacao.EtapaTransicao.UMDtoUPGM
        "OPER_ETAPA_TRANS_UPGM_UP":             [11 + 12764, 7],                # Operacao.EtapaTransicao.UPGMtoUP

        "OPER_INFO_PARADA":                     11 + 12764,                     # Leituras.Operacao_InfoParada
        "OPER_INFO_PARADA_NORMAL":              [11 + 12764, 0],                # Operacao.InfoParada.Normal
        "OPER_INFO_PARADA_EMERG":               [11 + 12764, 1],                # Operacao.InfoParada.Emergencia
        "OPER_INFO_PARADA_TRIP_AGUA":           [11 + 12764, 2],                # Operacao.InfoParada.TRIPAgua
        "OPER_INFO_PARADA_TRIP_M":              [11 + 12764, 3],                # Operacao.InfoParada.TRIPMecanico
        "OPER_INFO_PARADA_TRIP_E":              [11 + 12764, 4],                # Operacao.InfoParada.TRIPEletrico
        "OPER_INFO_PARADA_TRIP_H":              [11 + 12764, 5],                # Operacao.InfoParada.TRIPHidraulico
        "OPER_INFO_PARADA_RELIG_AUTO":          [11 + 12764, 6],                # Operacao.InfoParada.ReligamentoAutomatico
        "OPER_INFO_PARADA_PARTIDA_MANU":        [11 + 12764, 7],                # Operacao.InfoParada.PartidaManual
        "OPER_INFO_PARADA_INFO_INVAL":          [11 + 12764, 15],               # Operacao.InfoParada.ParadaInfoValida

        # UHCT
        "UHCT_INFO":                            12 + 12764,                     # Leituras.UHCT_Info
        "UHCT_OPERACIONAL":                     [12 + 12764, 0],                # UHCT.Info.Operacional
        "UHCT_LIGADA":                          [12 + 12764, 1],                # UHCT.Info.Ligada
        "UHCT_SENS_DESATIVADO":                 [12 + 12764, 2],                # UHCT.Info.SensorDesativado
        "UHCT_MODO_LOCAL":                      [12 + 12764, 3],                # UHCT.Info.ModoLocal

        "UHCT_BOMBAS":                          13 + 12764,                     # Leituras.UHCT_Bombas
        "UHCT_BOMBAS01":                        [13 + 12764, 0],                # UHCT.Bombas.Bomba01
        "UHCT_BOMBAS02":                        [13 + 12764, 1],                # UHCT.Bombas.Bomba02
        "UHCT_BOMBAS03":                        [13 + 12764, 2],                # UHCT.Bombas.Bomba03

        "UHCT_RODIZIO":                         14 + 12764,                     # Leituras.UHCT_Rodizio
        "UHCT_RODIZ_HABILITADO":                [14 + 12764, 0],                # UHCT.Rodizio.RodizioHabilitado
        "UHCT_RODIZ_BOMBA01":                   [14 + 12764, 1],                # UHCT.Rodizio.Bomba01
        "UHCT_RODIZ_BOMBA02":                   [14 + 12764, 2],                # UHCT.Rodizio.Bomba02

        "UHCT_VALVULAS":                        15 + 12764,                     # Leituras.UHCT_Valvulas
        "UHCT_VALVULAS01":                      [15 + 12764, 0],                # UHCT.Valvulas.Valvulas01
        "UHCT_VALVULAS02":                      [15 + 12764, 1],                # UHCT.Valvulas.Valvulas02
        "UHCT_VALVULAS03":                      [15 + 12764, 2],                # UHCT.Valvulas.Valvulas03
        "UHCT_VALVULAS04":                      [15 + 12764, 3],                # UHCT.Valvulas.Valvulas04

        "UHCT_FILTROS":                         16 + 12764,                     # Leituras.UHCT_Filtros
        "UHCT_FILTROS01":                       [16 + 12764, 0],                # UHCT.Filtros.Filtro01
        "UHCT_FILTROS02":                       [16 + 12764, 1],                # UHCT.Filtros.Filtro02
        "UHCT_FILTROS03":                       [16 + 12764, 2],                # UHCT.Filtros.Filtro03
        "UHCT_FILTROS04":                       [16 + 12764, 3],                # UHCT.Filtros.Filtro04
        "UHCT_FILTROS05":                       [16 + 12764, 4],                # UHCT.Filtros.Filtro05

        "UHCT_PRESSOSTATOS":                    17 + 12764,                     # Leituras.UHCT_Pressostatos
        "UHCT_PRESSOSTATO01":                   [17 + 12764, 0],                # UHCT.Pressostatos.Pressostato01
        "UHCT_PRESSOSTATO02":                   [17 + 12764, 1],                # UHCT.Pressostatos.Pressostato02
        "UHCT_PRESSOSTATO03":                   [17 + 12764, 2],                # UHCT.Pressostatos.Pressostato03

        "UHCT_NIVEL_OLEO":                      18 + 12764,                     # Leituras.UHCT_NivelOleo
        "UHCT_NIVEL_OLEO_LL":                   [18 + 12764, 0],                # UHCT.NivelOleo.LL
        "UHCT_NIVEL_OLEO_L":                    [18 + 12764, 1],                # UHCT.NivelOleo.L
        "UHCT_NIVEL_OLEO_H":                    [18 + 12764, 2],                # UHCT.NivelOleo.H
        "UHCT_NIVEL_OLEO_HH":                   [18 + 12764, 3],                # UHCT.NivelOleo.HH

        "UHCT_PRESSAO_OLEO":                    19 + 12764,                     # Leituras.UHCT_PressaoOleo
        "UHCT_ACUM_RODIZIO_PRINCIPAL":          20 + 12764,                     # Leituras.UHCT_AcumuladorRodizioPrincipal
        "UHCT_ACUM_RODIZIO_RETAGUARDA":         21 + 12764,                     # Leituras.UHCT_AcumuladorRodizioRetaguarda

        # UHLM
        "UHLM_INFO":                            22 + 12764,                     # Leituras.UHLM_Info
        "UHLM_OPERACIONAL":                     [22 + 12764, 0],                # UHLM.Info.Operacional
        "UHLM_LIGADA":                          [22 + 12764, 1],                # UHLM.Info.Ligada
        "UHLM_MODO_LOCAL":                      [22 + 12764, 2],                # UHLM.Info.ModoLocal
        "UHLM_VALV_BOMBA_MECAN":                [22 + 12764, 3],                # UHLM.Info.UHLM_ValvulaBombaMecanica
        "UHLM_VALV_ENTRA_TRO_CALO_ABER":        [22 + 12764, 4],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Aberta
        "UHLM_VALV_ENTRA_TRO_CALO_FECH":        [22 + 12764, 5],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Fechada
        "UHLM_VALV_SAI_TRO_CALO_ABER":          [22 + 12764, 6],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Aberta
        "UHLM_VALV_SAI_TRO_CALO_FECH":          [22 + 12764, 7],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Fechada
        "UHLM_BOMBA_RETAG_OPERAC":              [22 + 12764, 8],                # UHLM.Info.UHLM_BombaRetaguarda_Operacional

        "UHLM_BOMBAS":                          23 + 12764,                     # Leituras.UHLM_Bombas
        "UHLM_BOMBA01":                         [23 + 12764, 0],                # UHLM.Bombas.Bomba01
        "UHLM_BOMBA02":                         [23 + 12764, 1],                # UHLM.Bombas.Bomba02
        "UHLM_BOMBA03":                         [23 + 12764, 2],                # UHLM.Bombas.Bomba03
        "UHLM_BOMBA04":                         [23 + 12764, 3],                # UHLM.Bombas.Bomba04

        "UHLM_RODIZIO":                         24 + 12764,                     # Leituras.UHLM_Rodizio
        "UHLM_RODIZ_HABILITADO":                [24 + 12764, 0],                # UHLM.Rodizio.RodizioHabilitado
        "UHLM_RODIZ_BOMBA01":                   [24 + 12764, 1],                # UHLM.Rodizio.Bomba01
        "UHLM_RODIZ_BOMBA02":                   [24 + 12764, 2],                # UHLM.Rodizio.Bomba02

        "UHLM_FILTROS":                         25 + 12764,                     # Leituras.UHLM_Filtros
        "UHLM_FILTRO01":                        [25 + 12764, 0],                # UHLM.Filtros.Filtro01
        "UHLM_FILTRO02":                        [25 + 12764, 1],                # UHLM.Filtros.Filtro02
        "UHLM_FILTRO03":                        [25 + 12764, 2],                # UHLM.Filtros.Filtro03
        "UHLM_FILTRO04":                        [25 + 12764, 3],                # UHLM.Filtros.Filtro04
        "UHLM_FILTRO05":                        [25 + 12764, 4],                # UHLM.Filtros.Filtro05

        "UHLM_PRESSOSTATOS":                    26 + 12764,                     # Leituras.UHLM_Pressostatos
        "UHLM_PRESSOSTATO01":                   [26 + 12764, 0],                # UHLM.Pressostatos.Pressostato01
        "UHLM_PRESSOSTATO02":                   [26 + 12764, 1],                # UHLM.Pressostatos.Pressostato02
        "UHLM_PRESSOSTATO03":                   [26 + 12764, 2],                # UHLM.Pressostatos.Pressostato03
        "UHLM_PRESSOSTATO04":                   [26 + 12764, 3],                # UHLM.Pressostatos.Pressostato04

        "UHLM_FLUXOSTATOS":                     27 + 12764,                     # Leituras.UHLM_Fluxostatos
        "UHLM_FLUXOSTATO01":                    [27 + 12764, 0],                # UHLM.Fluxostatos.Fluxostato01
        "UHLM_FLUXOSTATO02":                    [27 + 12764, 1],                # UHLM.Fluxostatos.Fluxostato02
        "UHLM_FLUXOSTATO03":                    [27 + 12764, 2],                # UHLM.Fluxostatos.Fluxostato03
        "UHLM_FLUXOSTATO04":                    [27 + 12764, 3],                # UHLM.Fluxostatos.Fluxostato04
        "UHLM_FLUXOSTATO05":                    [27 + 12764, 4],                # UHLM.Fluxostatos.Fluxostato05
        "UHLM_FLUXOSTATO06":                    [27 + 12764, 5],                # UHLM.Fluxostatos.Fluxostato06
        "UHLM_FLUXOSTATO07":                    [27 + 12764, 6],                # UHLM.Fluxostatos.Fluxostato07

        "UHLM_NIVEL_OLEO":                      28 + 12764,                     # Leituras.UHLM_NivelOleo
        "UHLM_NIVEL_OLEO_LL":                   [28 + 12764, 0],                # UHLM.NivelOleo.LL
        "UHLM_NIVEL_OLEO_L":                    [28 + 12764, 1],                # UHLM.NivelOleo.L
        "UHLM_NIVEL_OLEO_H":                    [28 + 12764, 2],                # UHLM.NivelOleo.H
        "UHLM_NIVEL_OLEO_HH":                   [28 + 12764, 3],                # UHLM.NivelOleo.HH

        "UHLM_ACUM_RODIZIO_PRINCIPAL":          29 + 12764,                     # Leituras.UHLM_AcumuladorRodizioPrincipal
        "UHLM_ACUM_RODIZIO_RETAGUARDA":         30 + 12764,                     # Leituras.UHLM_AcumuladorRodizioRetaguarda

        "UHLM_FLUXOSTATO_OLEO_01":              122 + 12764,                    # Leituras.UHLM_FluxostatoOleo01
        "UHLM_FLUXOSTATO_OLEO_02":              123 + 12764,                    # Leituras.UHLM_FluxostatoOleo02
        "UHLM_FLUXOSTATO_OLEO_03":              124 + 12764,                    # Leituras.UHLM_FluxostatoOleo03
        "UHLM_FLUXOSTATO_OLEO_04":              125 + 12764,                    # Leituras.UHLM_FluxostatoOleo04

        # Turbina
        "TURB_INFO":                            31 + 12764,                     # Leituras.Turb_Info
        "TURB_EQUALIZADA":                      [31 + 12764, 0],                # Turbina.Info.Equalizada
        "TURB_PRONTA":                          [31 + 12764, 1],                # Turbina.Info.Pronta
        "TURB_FECHADA":                         [31 + 12764, 2],                # Turbina.Info.Fechada
        "TURB_TRAVADA":                         [31 + 12764, 3],                # Turbina.Info.Travada
        "TURB_PARADA":                          [31 + 12764, 4],                # Turbina.Info.Parada
        "TURB_EQUALIZANDO":                     [31 + 12764, 5],                # Turbina.Info.Equalizando
        "TURB_FECHANDO":                        [31 + 12764, 6],                # Turbina.Info.Fechando
        "TURB_SENS_DESATIVADO":                 [31 + 12764, 7],                # Turbina.Info.SensorDesativado
        "TURB_DISTRI_FECHADO":                  [31 + 12764, 8],                # Turbina.Info.DistribuidorFechado

        "TURB_VALVULA_BYPASS":                  32 + 12764,                     # Leituras.Turb_ValvulaByPass
        "TURB_VALV_BY_ACIONA":                  [32 + 12764, 0],                # Turbina.Bypass.Acionamento
        "TURB_VALV_BY_FECHADO":                 [32 + 12764, 1],                # Turbina.Bypass.Fechado
        "TURB_VALV_BY_ABERTO":                  [32 + 12764, 2],                # Turbina.Bypass.Aberto

        "TURB_VALVULA_BORBOLETA":               33 + 12764,                     # Leituras.Turb_ValvulaBorboleta
        "TURB_VALV_BORB_ACIONA":                [33 + 12764, 0],                # Turbina.Borboleta.Acionamento
        "TURB_VALV_BORB_FECHADA":               [33 + 12764, 1],                # Turbina.Borboleta.Fechada
        "TURB_VALV_BORB_ABERTA":                [33 + 12764, 2],                # Turbina.Borboleta.Aberta
        "TURB_VALV_BORB_DERIVA":                [33 + 12764, 3],                # Turbina.Borboleta.Deriva
        "TURB_VALV_BORB_TRAVADA":               [33 + 12764, 4],                # Turbina.Borboleta.Travada
        "TURB_VALV_BORB_MANTEM":                [33 + 12764, 5],                # Turbina.Borboleta.Mantem

        "TURB_TEMPO_CRACK_EFETIVO":             34 + 12764,                     # Leituras.Turb_TempoCrackEfetivo
        "TURB_TEMPO_EQUAL_EFETIVO":             35 + 12764,                     # Leituras.Turb_TempoEqualizacaoEfetivo
        "TURB_PRESSAO_CONDUTO":                 36 + 12764,                     # Leituras.Turb_PressaoConduto
        "TURB_PRESSAO_CAIXA_ESPIRAL":           37 + 12764,                     # Leituras.Turb_PressaoCaixaEspiral
        "TURB_VAZAO_TURBINADA":                 38 + 12764,                     # Leituras.Turb_VazaoTurbinada
        "TURB_VIBRACAO_01":                     39 + 12764,                     # Leituras.Turb_Vibracao01
        "TURB_VIBRACAO_02":                     40 + 12764,                     # Leituras.Turb_Vibracao02
        "TURB_VIBRACAO_03":                     41 + 12764,                     # Leituras.Turb_Vibracao03
        "TURB_VIBRACAO_04":                     42 + 12764,                     # Leituras.Turb_Vibracao04

        "TURB_FRENAGEM":                        43 + 12764,                     # Leituras.Turb_Frenagem
        "TURB_FRENA_APLICADO":                  [43 + 12764, 0],                # Turbina.Frenagem.Info.Aplicado
        "TURB_FRENA_MANUAL":                    [43 + 12764, 1],                # Turbina.Frenagem.Info.Manual
        "TURB_FRENA_PRESSOS":                   [43 + 12764, 2],                # Turbina.Frenagem.Info.Pressostato
        "TURB_FRENA_1ZE":                       [43 + 12764, 3],                # Turbina.Frenagem.Info.[1ZE]
        "TURB_FRENA_2ZE":                       [43 + 12764, 4],                # Turbina.Frenagem.Info.[2ZE]

        "TURB_VIBRACAO_05":                     128 + 12764,                    # Leituras.Turb_Vibracao05

        # Reg V
        "REG_V_INFO":                           44 + 12764,                     # Leituras.RegV_Info
        "REG_V_HABILITADO":                     [44 + 12764, 0],                # RegV.Info.Habilitado
        "REG_V_BASE_CARGA":                     [44 + 12764, 1],                # RegV.Info.BaseCarga
        "REG_V_RPM30":                          [44 + 12764, 2],                # RegV.Info.RPM30
        "REG_V_RPM90":                          [44 + 12764, 3],                # RegV.Info.RPM90
        "REG_V_CARGA_ZERADA":                   [44 + 12764, 4],                # RegV.Info.CargaZerada
        "REG_V_MODO_ESTATISMO":                 [44 + 12764, 5],                # RegV.Info.ModoEstatismo
        "REG_V_MODO_BASE_CARGA":                [44 + 12764, 6],                # RegV.Info.ModoBaseCarga
        "REG_V_DISTRI_FECHADO":                 [44 + 12764, 7],                # RegV.Info.DistribuidorFechado

        "REG_V_ESTADO":                         45 + 12764,                     # Leituras.RegV_Estado
        "REG_V_FALHA":                          [45 + 12764, 0],                # RegV.Estado.Falha
        "REG_V_PARADO":                         [45 + 12764, 1],                # RegV.Estado.Parado
        "REG_V_CTRL_MANUAL_DISTRI":             [45 + 12764, 2],                # RegV.Estado.ControleManualDistribuidor
        "REG_V_CTRL_MANUAL_VALV":               [45 + 12764, 3],                # RegV.Estado.ControleManualValvula
        "REG_V_CTRL_VELOC":                     [45 + 12764, 4],                # RegV.Estado.ControleVelocidade
        "REG_V_COMPENSA_POT_ATIVA":             [45 + 12764, 5],                # RegV.Estado.CompensacaoPotenciaAtiva
        "REG_V_CTRL_POT_ATIVA":                 [45 + 12764, 6],                # RegV.Estado.ControlePotenciaAtiva

        "REG_V_VELOCIDADE":                     46 + 12764,                     # Leituras.RegV_Velocidade
        "REG_V_DISTRIBUIDOR":                   47 + 12764,                     # Leituras.RegV_Distribuidor
        "REG_V_ROTOR":                          48 + 12764,                     # Leituras.RegV_Rotor
        "REG_V_POT_ALVO":                       49 + 12764,                     # Leituras.RegV_PotenciaAlvo

        "REG_V_CONJUGADO_INFO":                 127 + 12764,                    # Leituras.RegV_CurvaConjugacao_Info
        "REG_V_CONJ_AUTOMATICO":                [127 + 12764, 0],               # RegV.Conjugado.Automatico
        "REG_V_CONJ_MANUAL":                    [127 + 12764, 1],               # RegV.Conjugado.Manual
        "REG_V_CONJUGADO1":                     [127 + 12764, 2],               # RegV.Conjugado.Conjugado1
        "REG_V_CONJUGADO2":                     [127 + 12764, 3],               # RegV.Conjugado.Conjugado2
        "REG_V_CONJUGADO3":                     [127 + 12764, 4],               # RegV.Conjugado.Conjugado3

        # Reg T
        "REG_T_INFO":                           50 + 12764,                     # Leituras.RegT_Info
        "REG_T_HABILITACAO":                    [50 + 12764, 0],                # RegT.Info.Habilitacao
        "REG_T_TENSAO_ESTAB":                   [50 + 12764, 1],                # RegT.Info.TensaoEstabilizada
        "REG_T_CONTATOR_ABERTO":                [50 + 12764, 2],                # RegT.Info.ContatorAberto
        "REG_T_CONTATOR_FECHADO":               [50 + 12764, 3],                # RegT.Info.ContatorFechado
        "REG_T_PRE_EXCITACAO":                  [50 + 12764, 4],                # RegT.Info.PreExcitacao
        "REG_T_MTVC":                           [50 + 12764, 5],                # RegT.Info.MTVC
        "REG_T_MECC":                           [50 + 12764, 6],                # RegT.Info.MECC
        "REG_T_OPER_ONLINE":                    [50 + 12764, 7],                # RegT.Info.OperacaoOnline
        "REG_T_OPER_PARALELA":                  [50 + 12764, 9],                # RegT.Info.OperacaoParalela

        "REG_T_UEXCITACAO":                     51 + 12764,                     # Leituras.RegT_UExcitacao
        "REG_T_IEXCITACAO":                     52 + 12764,                     # Leituras.RegT_IExcitacao
        "REG_T_FPALVO":                         128 + 12764,                    # Leituras.RegT_FPAlvo
        "REG_T_REATIVO_ALVO":                   129 + 12764,                    # Leituras.RegT_ReativoAlvo

        # Sinc
        "SINC_INFO":                            53 + 12764,                     # Leituras.Sinc_Info
        "SINC_HABILITADO":                      [53 + 12764, 0],                # Sincronoscopio.Info.Habilitado
        "SINC_MODO_AUTO":                       [53 + 12764, 1],                # Sincronoscopio.Info.ModoAutomatico
        "SINC_MODO_MANUAL":                     [53 + 12764, 2],                # Sincronoscopio.Info.ModoManual
        "SINC_BARRA_MORTA":                     [53 + 12764, 3],                # Sincronoscopio.Info.BarraMorta

        "SINC_FREQ_GERADOR":                    54 + 12764,                     # Leituras.Sinc_FrequenciaGerador
        "SINC_FREQ_BARRA":                      55 + 12764,                     # Leituras.Sinc_FrequenciaBarra
        "SINC_TENSAO_GERADOR":                  56 + 12764,                     # Leituras.Sinc_TensaoGerador
        "SINC_TENSAO_BARRA":                    57 + 12764,                     # Leituras.Sinc_TensaoBarra

        # DJ
        "Dj52G_INFO":                           58 + 12764,                     # Leituras.Disj52G_Info
        "Dj52G_ABERTO":                         [58 + 12764, 0],                # Disjuntor52G.Info.Aberto
        "Dj52G_FECHADO":                        [58 + 12764, 1],                # Disjuntor52G.Info.Fechado
        "Dj52G_INCONSISTENTE":                  [58 + 12764, 2],                # Disjuntor52G.Info.Inconsistente
        "Dj52G_TRIP":                           [58 + 12764, 3],                # Disjuntor52G.Info.TRIP
        "Dj52G_TESTE":                          [58 + 12764, 4],                # Disjuntor52G.Info.Teste
        "Dj52G_INSERIDO":                       [58 + 12764, 5],                # Disjuntor52G.Info.Inserido
        "Dj52G_EXTRAIVEL":                      [58 + 12764, 6],                # Disjuntor52G.Info.Extraivel
        "Dj52G_MOLA_CARRE":                     [58 + 12764, 7],                # Disjuntor52G.Info.MolaCarregada
        "Dj52G_CONDICAO":                       [58 + 12764, 8],                # Disjuntor52G.Info.CondicaoFechamento
        "Dj52G_FALTA_VCC":                      [58 + 12764, 9],                # Disjuntor52G.Info.FaltaVCC

        # Tensão
        "TENSAO_RN":                            59 + 12764,                     # Leituras.Gerador_TensaoRN
        "TENSAO_SN":                            60 + 12764,                     # Leituras.Gerador_TensaoSN
        "TENSAO_TN":                            61 + 12764,                     # Leituras.Gerador_TensaoTN
        "TENSAO_RS":                            62 + 12764,                     # Leituras.Gerador_TensaoRS
        "TENSAO_ST":                            63 + 12764,                     # Leituras.Gerador_TensaoST
        "TENSAO_TR":                            64 + 12764,                     # Leituras.Gerador_TensaoTR

        # Corrente
        "CORRENTE_R":                           65 + 12764,                     # Leituras.Gerador_CorrenteR
        "CORRENTE_S":                           66 + 12764,                     # Leituras.Gerador_CorrenteS
        "CORRENTE_T":                           67 + 12764,                     # Leituras.Gerador_CorrenteT
        "CORRENTE_MEDIA":                       68 + 12764,                     # Leituras.Gerador_CorrenteMedia

        # Potência Ativa
        "POT_ATIVA_1":                          69 + 12764,                     # Leituras.Gerador_PotenciaAtiva1
        "POT_ATIVA_2":                          70 + 12764,                     # Leituras.Gerador_PotenciaAtiva2
        "POT_ATIVA_3":                          71 + 12764,                     # Leituras.Gerador_PotenciaAtiva3
        "POT_ATIVA_MEDIA":                      72 + 12764,                     # Leituras.Gerador_PotenciaAtivaMedia

        # Potência Reativa
        "POT_REATIVA_1":                        73 + 12764,                     # Leituras.Gerador_PotenciaReativa1
        "POT_REATIVA_2":                        74 + 12764,                     # Leituras.Gerador_PotenciaReativa2
        "POT_REATIVA_3":                        75 + 12764,                     # Leituras.Gerador_PotenciaReativa3
        "POT_REATIVA_MEDIA":                    76 + 12764,                     # Leituras.Gerador_PotenciaReativaMedia

        # Potência Aparente
        "POT_APARENTE_1":                       77 + 12764,                     # Leituras.Gerador_PotenciaAparente1
        "POT_APARENTE_2":                       78 + 12764,                     # Leituras.Gerador_PotenciaAparente2
        "POT_APARENTE_3":                       79 + 12764,                     # Leituras.Gerador_PotenciaAparente3
        "POT_APARENTE_MEDIA":                   80 + 12764,                     # Leituras.Gerador_PotenciaAparenteMedia

        # Fator Potência
        "FATOR_POT_1":                          81 + 12764,                     # Leituras.Gerador_FatorPotencia1
        "FATOR_POT_2":                          82 + 12764,                     # Leituras.Gerador_FatorPotencia2
        "FATOR_POT_3":                          83 + 12764,                     # Leituras.Gerador_FatorPotencia3
        "FATOR_POT_MEDIA":                      84 + 12764,                     # Leituras.Gerador_FatorPotenciaMedia

        # Frequencia
        "FREQUENCIA":                           85 + 12764,                     # Leituras.Gerador_Frequencia

        # Energia Fornecida
        "ENERGIA_FORNECIDA_TWh":                86 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTWh
        "ENERGIA_FORNECIDA_GWh":                87 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGWh
        "ENERGIA_FORNECIDA_MWh":                88 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMWh
        "ENERGIA_FORNECIDA_kWh":                89 + 12764,                     # Leituras.Gerador_EnergiaFornecidakWh
        "ENERGIA_FORNECIDA_TVarh":              90 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTVarh
        "ENERGIA_FORNECIDA_GVarh":              91 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGVarh
        "ENERGIA_FORNECIDA_MVarh":              92 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMVarh
        "ENERGIA_FORNECIDA_kVarh":              93 + 12764,                     # Leituras.Gerador_EnergiaFornecidakVarh
        "ENERGIA_CORNECIDA_TVarh":              94 + 12764,                     # Leituras.Gerador_EnergiaConsumidaTVarh
        "ENERGIA_CORNECIDA_GVarh":              95 + 12764,                     # Leituras.Gerador_EnergiaConsumidaGVarh
        "ENERGIA_CORNECIDA_MVarh":              96 + 12764,                     # Leituras.Gerador_EnergiaConsumidaMVarh
        "ENERGIA_CORNECIDA_kVarh":              97 + 12764,                     # Leituras.Gerador_EnergiaConsumidakVarh

        "GERADOR_FP_INFO":                      98 + 12764,                     # Leituras.Gerador_FPInfo
        "GERADOR_FP_FASE1_IND":                 [98 + 12764, 0],                # Gerador.FP_Info.Fase1_Ind
        "GERADOR_FP_FASE1_CAP":                 [98 + 12764, 1],                # Gerador.FP_Info.Fase1_Cap
        "GERADOR_FP_FASE2_IND":                 [98 + 12764, 2],                # Gerador.FP_Info.Fase2_Ind
        "GERADOR_FP_FASE2_CAP":                 [98 + 12764, 3],                # Gerador.FP_Info.Fase2_Cap
        "GERADOR_FP_FASE3_IND":                 [98 + 12764, 4],                # Gerador.FP_Info.Fase3_Ind
        "GERADOR_FP_FASE3_CAP":                 [98 + 12764, 5],                # Gerador.FP_Info.Fase3_Cap
        "GERADOR_FP_FASE4_IND":                 [98 + 12764, 6],                # Gerador.FP_Info.Total_Ind
        "GERADOR_FP_FASE4_CAP":                 [98 + 12764, 7],                # Gerador.FP_Info.Total_Cap

        # Controles
        "CTRL_REATIVO_INFO":                    99 + 12764,                    # Leituras.CtrlReativo_Info
        "CTRL_REAT_MODO_FP":                    [99 + 12764, 0],               # CtrlReativo.Info.ModoFP
        "CTRL_REAT_MODO_VAR":                   [99 + 12764, 1],               # CtrlReativo.Info.ModoVar

        "CTRL_POTENCIA_INFO":                   100 + 12764,                    # Leituras.CtrlPotencia_Info
        "CTRL_POT_MODO_NIVEL":                  [100 + 12764, 0],               # CtrlPotencia.Info.ModoNivel
        "CTRL_POT_MODO_POT":                    [100 + 12764, 1],               # CtrlPotencia.Info.ModoPotencia
        "CTRL_POT_MODO_RELIGA_AUTO":            [100 + 12764, 2],               # CtrlPotencia.Info.ModoReligamentoAutomatico

        # Horimetros
        "HORIM_ELETR_LOW":                      101 + 12764,                    # Leituras.HorimetroEletrico_Low
        "HORIM_ELETR_HIGH":                     102 + 12764,                    # Leituras.HorimetroEletrico_High
        "HORIM_MECAN_LOW":                      103 + 12764,                    # Leituras.HorimetroMecanico_Low
        "HORIM_MECAN_HIGH":                     104 + 12764,                    # Leituras.HorimetroMecanico_High

        # Temperatura
        "TEMPERATURA_01":                       106 + 12764,                    # Leituras.Temperatura_01
        "TEMPERATURA_02":                       107 + 12764,                    # Leituras.Temperatura_02
        "TEMPERATURA_03":                       108 + 12764,                    # Leituras.Temperatura_03
        "TEMPERATURA_04":                       109 + 12764,                    # Leituras.Temperatura_04
        "TEMPERATURA_05":                       110 + 12764,                    # Leituras.Temperatura_05
        "TEMPERATURA_06":                       111 + 12764,                    # Leituras.Temperatura_06
        "TEMPERATURA_07":                       112 + 12764,                    # Leituras.Temperatura_07
        "TEMPERATURA_08":                       113 + 12764,                    # Leituras.Temperatura_08
        "TEMPERATURA_09":                       114 + 12764,                    # Leituras.Temperatura_09
        "TEMPERATURA_10":                       115 + 12764,                    # Leituras.Temperatura_10
        "TEMPERATURA_11":                       116 + 12764,                    # Leituras.Temperatura_11
        "TEMPERATURA_12":                       117 + 12764,                    # Leituras.Temperatura_12
        "TEMPERATURA_13":                       118 + 12764,                    # Leituras.Temperatura_13
        "TEMPERATURA_14":                       119 + 12764,                    # Leituras.Temperatura_14
        "TEMPERATURA_15":                       120 + 12764,                    # Leituras.Temperatura_15
        "TEMPERATURA_16":                       121 + 12764,                    # Leituras.Temperatura_16


        ## DISJUNTORES

        "DJ_01":                                0 + 12564,                      # Disjuntor Q125.0 - Alimentação Circuitos de Comando                                  -> condic_indisponibiliza UG1
        "DJ_02":                                0 + 12564,                      # Disjuntor Q125.1 - Alimentação GRTD2000                                              -> condic_indisponibiliza UG1
        "DJ_03":                                1 + 12564,                      # Disjuntor Q125.2 - Alimentação Relés de Proteção                                     -> condic_indisponibiliza UG1
        "DJ_04":                                2 + 12564,                      # Disjuntor Q24.0 - Alimentação Válvula Proporcional e Transdutor de Posição           -> condic_indisponibiliza UG1
        "DJ_05":                                3 + 12564,                      # CSG - Disjuntor Q220.1 - Alimentação Carregamento de Mola                            -> condic_indisponibiliza UG1
        "DJ_06":                                4 + 12564,                      # CSG - Disjuntor Q125.0 - Alimentação Circuito de Comando 52G                         -> condic_indisponibiliza UG1
        "DJ_07":                                5 + 12564,                      # Q49 - Disjuntor Q125.0 UG1 - Alimentação SEL2600
        "DJ_08":                                6 + 12564,                      # Disjuntor Motor QM1 - Bomba de Óleo 01 da UHCT                                       -> condic_indisponibiliza UG1
        "DJ_09":                                7 + 12564,                      # Disjuntor Motor QM2 - Bomba de Óleo 02 da UHCT                                       -> condic_indisponibiliza UG1
        "DJ_10":                                8 + 12564,                      # Disjuntor Motor QM3 - Bomba de Óleo 01 da UHLM                                       -> condic_indisponibiliza UG1
        "DJ_11":                                9 + 12564,                     #
        "DJ_12":                                10 + 12564,                     #
        "DJ_13":                                11 + 12564,                     #
        "DJ_14":                                12 + 12564,                     #
        "DJ_15":                                13 + 12564,                     #
        "DJ_16":                                14 + 12564,                     #
        "DJ_17":                                15 + 12564,                     #
        "DJ_18":                                16 + 12564,                     #
        "DJ_19":                                17 + 12564,                     #
        "DJ_20":                                18 + 12564,                     #
        "DJ_21":                                19 + 12564,                     #
        "DJ_22":                                20 + 12564,                     #
        "DJ_23":                                21 + 12564,                     #
        "DJ_24":                                22 + 12564,                     #
        "DJ_25":                                23 + 12564,                     #
        "DJ_26":                                24 + 12564,                     #
        "DJ_27":                                25 + 12564,                     #
        "DJ_28":                                26 + 12564,                     #
        "DJ_29":                                27 + 12564,                     #
        "DJ_30":                                28 + 12564,                     #
        "DJ_31":                                29 + 12564,                     #
        "DJ_32":                                30 + 12564,                     #


        ## ALARMES

        # Específicos UG4
        "Alarme10_14":                          [9 + 14199, 14],
        "Alarme10_15":                          [9 + 14199, 15],

        "Alarme13_12":                          [12 + 14199, 12],
        "Alarme13_13":                          [12 + 14199, 13],
        "Alarme13_14":                          [12 + 14199, 14],
        "Alarme13_15":                          [12 + 14199, 15],

        "Alarme14_00":                          [13 + 14199, 0],
        "Alarme14_01":                          [13 + 14199, 1],
        "Alarme14_02":                          [13 + 14199, 2],

        "Alarme16_02":                          [15 + 14199, 2],
        "Alarme16_03":                          [15 + 14199, 3],

        # Gerais
        "Alarme01_00":                          [0 + 14199, 0],
        "Alarme01_01":                          [0 + 14199, 1],
        "Alarme01_02":                          [0 + 14199, 2],
        "Alarme01_03":                          [0 + 14199, 3],
        "Alarme01_06":                          [0 + 14199, 6],
        "Alarme01_07":                          [0 + 14199, 7],
        "Alarme01_08":                          [0 + 14199, 8],
        "Alarme01_09":                          [0 + 14199, 9],
        "Alarme01_10":                          [0 + 14199, 10],
        "Alarme01_11":                          [0 + 14199, 11],
        "Alarme01_12":                          [0 + 14199, 12],
        "Alarme01_13":                          [0 + 14199, 13],
        "Alarme01_14":                          [0 + 14199, 14],
        "Alarme01_15":                          [0 + 14199, 15],

        "Alarme02_00":                          [1 + 14199, 0],
        "Alarme02_01":                          [1 + 14199, 1],
        "Alarme02_02":                          [1 + 14199, 2],
        "Alarme02_03":                          [1 + 14199, 3],
        "Alarme02_04":                          [1 + 14199, 4],
        "Alarme02_05":                          [1 + 14199, 5],
        "Alarme02_06":                          [1 + 14199, 6],
        "Alarme02_07":                          [1 + 14199, 7],
        "Alarme02_08":                          [1 + 14199, 8],
        "Alarme02_09":                          [1 + 14199, 9],
        "Alarme02_10":                          [1 + 14199, 10],
        "Alarme02_11":                          [1 + 14199, 11],
        "Alarme02_12":                          [1 + 14199, 12],
        "Alarme02_13":                          [1 + 14199, 13],
        "Alarme02_14":                          [1 + 14199, 14],
        "Alarme02_15":                          [1 + 14199, 15],

        "Alarme03_00":                          [2 + 14199, 0],
        "Alarme03_01":                          [2 + 14199, 1],
        "Alarme03_02":                          [2 + 14199, 2],
        "Alarme03_03":                          [2 + 14199, 3],
        "Alarme03_04":                          [2 + 14199, 4],
        "Alarme03_05":                          [2 + 14199, 5],
        "Alarme03_06":                          [2 + 14199, 6],
        "Alarme03_07":                          [2 + 14199, 7],
        "Alarme03_08":                          [2 + 14199, 8],
        "Alarme03_09":                          [2 + 14199, 9],
        "Alarme03_10":                          [2 + 14199, 10],
        "Alarme03_11":                          [2 + 14199, 11],
        "Alarme03_12":                          [2 + 14199, 12],
        "Alarme03_13":                          [2 + 14199, 13],
        "Alarme03_14":                          [2 + 14199, 14],
        "Alarme03_15":                          [2 + 14199, 15],

        "Alarme04_00":                          [3 + 14199, 0],
        "Alarme04_01":                          [3 + 14199, 1],
        "Alarme04_02":                          [3 + 14199, 2],
        "Alarme04_04":                          [3 + 14199, 4],
        "Alarme04_05":                          [3 + 14199, 5],
        "Alarme04_06":                          [3 + 14199, 6],
        "Alarme04_07":                          [3 + 14199, 7],
        "Alarme04_09":                          [3 + 14199, 9],
        "Alarme04_10":                          [3 + 14199, 10],
        "Alarme04_11":                          [3 + 14199, 11],
        "Alarme04_12":                          [3 + 14199, 12],
        "Alarme04_13":                          [3 + 14199, 13],
        "Alarme04_14":                          [3 + 14199, 14],
        "Alarme04_15":                          [3 + 14199, 15],

        "Alarme05_00":                          [4 + 14199, 0],
        "Alarme05_02":                          [4 + 14199, 2],
        "Alarme05_03":                          [4 + 14199, 3],
        "Alarme05_04":                          [4 + 14199, 4],
        "Alarme05_05":                          [4 + 14199, 5],
        "Alarme05_06":                          [4 + 14199, 6],
        "Alarme05_07":                          [4 + 14199, 7],
        "Alarme05_09":                          [4 + 14199, 9],
        "Alarme05_10":                          [4 + 14199, 10],
        "Alarme05_11":                          [4 + 14199, 11],
        "Alarme05_12":                          [4 + 14199, 12],
        "Alarme05_13":                          [4 + 14199, 13],
        "Alarme05_14":                          [4 + 14199, 14],
        "Alarme05_15":                          [4 + 14199, 15],

        "Alarme06_00":                          [5 + 14199, 0],
        "Alarme06_03":                          [5 + 14199, 3],
        "Alarme06_04":                          [5 + 14199, 4],
        "Alarme06_05":                          [5 + 14199, 5],
        "Alarme06_08":                          [5 + 14199, 8],
        "Alarme06_09":                          [5 + 14199, 9],
        "Alarme06_10":                          [5 + 14199, 10],
        "Alarme06_11":                          [5 + 14199, 11],
        "Alarme06_12":                          [5 + 14199, 12],
        "Alarme06_13":                          [5 + 14199, 13],
        "Alarme06_14":                          [5 + 14199, 14],
        "Alarme06_15":                          [5 + 14199, 15],

        "Alarme07_00":                          [6 + 14199, 0],
        "Alarme07_01":                          [6 + 14199, 1],
        "Alarme07_02":                          [6 + 14199, 2],
        "Alarme07_03":                          [6 + 14199, 3],
        "Alarme07_06":                          [6 + 14199, 6],
        "Alarme07_07":                          [6 + 14199, 7],
        "Alarme07_08":                          [6 + 14199, 8],
        "Alarme07_09":                          [6 + 14199, 9],
        "Alarme07_10":                          [6 + 14199, 10],
        "Alarme07_11":                          [6 + 14199, 11],
        "Alarme07_12":                          [6 + 14199, 12],
        "Alarme07_13":                          [6 + 14199, 13],
        "Alarme07_14":                          [6 + 14199, 14],
        "Alarme07_15":                          [6 + 14199, 15],

        "Alarme08_00":                          [7 + 14199, 0],
        "Alarme08_01":                          [7 + 14199, 1],
        "Alarme08_02":                          [7 + 14199, 2],
        "Alarme08_03":                          [7 + 14199, 3],
        "Alarme08_07":                          [7 + 14199, 7],
        "Alarme08_08":                          [7 + 14199, 8],
        "Alarme08_09":                          [7 + 14199, 9],
        "Alarme08_10":                          [7 + 14199, 10],
        "Alarme08_11":                          [7 + 14199, 11],
        "Alarme08_12":                          [7 + 14199, 12],
        "Alarme08_13":                          [7 + 14199, 13],
        "Alarme08_14":                          [7 + 14199, 14],
        "Alarme08_15":                          [7 + 14199, 15],

        "Alarme09_00":                          [8 + 14199, 0],
        "Alarme09_01":                          [8 + 14199, 1],
        "Alarme09_02":                          [8 + 14199, 2],
        "Alarme09_03":                          [8 + 14199, 3],
        "Alarme09_04":                          [8 + 14199, 4],
        "Alarme09_06":                          [8 + 14199, 6],
        "Alarme09_07":                          [8 + 14199, 7],
        "Alarme09_08":                          [8 + 14199, 8],
        "Alarme09_09":                          [8 + 14199, 9],
        "Alarme09_10":                          [8 + 14199, 10],
        "Alarme09_11":                          [8 + 14199, 11],
        "Alarme09_12":                          [8 + 14199, 12],
        "Alarme09_13":                          [8 + 14199, 13],
        "Alarme09_14":                          [8 + 14199, 14],
        "Alarme09_15":                          [8 + 14199, 15],

        "Alarme10_00":                          [9 + 14199, 0],
        "Alarme10_01":                          [9 + 14199, 1],
        "Alarme10_02":                          [9 + 14199, 2],
        "Alarme10_03":                          [9 + 14199, 3],
        "Alarme10_05":                          [9 + 14199, 5],
        "Alarme10_06":                          [9 + 14199, 6],
        "Alarme10_07":                          [9 + 14199, 7],
        "Alarme10_08":                          [9 + 14199, 8],
        "Alarme10_09":                          [9 + 14199, 9],
        "Alarme10_10":                          [9 + 14199, 10],
        "Alarme10_11":                          [9 + 14199, 11],
        "Alarme10_12":                          [9 + 14199, 12],
        "Alarme10_13":                          [9 + 14199, 13],
        "Alarme10_14":                          [9 + 14199, 14],
        "Alarme10_15":                          [9 + 14199, 15],

        "Alarme11_00":                          [10 + 14199, 0],
        "Alarme11_01":                          [10 + 14199, 1],
        "Alarme11_02":                          [10 + 14199, 2],
        "Alarme11_06":                          [10 + 14199, 6],
        "Alarme11_07":                          [10 + 14199, 7],
        "Alarme11_08":                          [10 + 14199, 8],
        "Alarme11_09":                          [10 + 14199, 9],
        "Alarme11_10":                          [10 + 14199, 10],
        "Alarme11_11":                          [10 + 14199, 11],
        "Alarme11_12":                          [10 + 14199, 12],
        "Alarme11_13":                          [10 + 14199, 13],
        "Alarme11_14":                          [10 + 14199, 14],
        "Alarme11_15":                          [10 + 14199, 15],

        "Alarme12_01":                          [11 + 14199, 1],
        "Alarme12_02":                          [11 + 14199, 2],
        "Alarme12_03":                          [11 + 14199, 3],
        "Alarme12_04":                          [11 + 14199, 4],
        "Alarme12_05":                          [11 + 14199, 5],
        "Alarme12_06":                          [11 + 14199, 6],
        "Alarme12_07":                          [11 + 14199, 7],
        "Alarme12_09":                          [11 + 14199, 9],
        "Alarme12_10":                          [11 + 14199, 10],
        "Alarme12_11":                          [11 + 14199, 11],
        "Alarme12_12":                          [11 + 14199, 12],
        "Alarme12_13":                          [11 + 14199, 13],
        "Alarme12_14":                          [11 + 14199, 14],
        "Alarme12_15":                          [11 + 14199, 15],

        "Alarme13_00":                          [12 + 14199, 0],
        "Alarme13_01":                          [12 + 14199, 1],
        "Alarme13_02":                          [12 + 14199, 2],
        "Alarme13_03":                          [12 + 14199, 3],
        "Alarme13_09":                          [12 + 14199, 9],
        "Alarme13_10":                          [12 + 14199, 10],
        "Alarme13_11":                          [12 + 14199, 11],
        "Alarme13_12":                          [12 + 14199, 12],
        "Alarme13_13":                          [12 + 14199, 13],
        "Alarme13_14":                          [12 + 14199, 14],
        "Alarme13_15":                          [12 + 14199, 15],

        "Alarme14_00":                          [13 + 14199, 0],
        "Alarme14_01":                          [13 + 14199, 1],
        "Alarme14_02":                          [13 + 14199, 2],
        "Alarme14_03":                          [13 + 14199, 3],
        "Alarme14_04":                          [13 + 14199, 4],
        "Alarme14_05":                          [13 + 14199, 5],
        "Alarme14_10":                          [13 + 14199, 10],
        "Alarme14_11":                          [13 + 14199, 11],
        "Alarme14_12":                          [13 + 14199, 12],
        "Alarme14_13":                          [13 + 14199, 13],
        "Alarme14_14":                          [13 + 14199, 14],
        "Alarme14_15":                          [13 + 14199, 15],

        "Alarme15_00":                          [14 + 14199, 0],
        "Alarme15_01":                          [14 + 14199, 1],
        "Alarme15_02":                          [14 + 14199, 2],
        "Alarme15_03":                          [14 + 14199, 3],
        "Alarme15_04":                          [14 + 14199, 4],
        "Alarme15_05":                          [14 + 14199, 5],
        "Alarme15_06":                          [14 + 14199, 6],
        "Alarme15_07":                          [14 + 14199, 7],
        "Alarme15_08":                          [14 + 14199, 8],
        "Alarme15_09":                          [14 + 14199, 9],
        "Alarme15_10":                          [14 + 14199, 10],
        "Alarme15_12":                          [14 + 14199, 12],
        "Alarme15_13":                          [14 + 14199, 13],
        "Alarme15_14":                          [14 + 14199, 14],
        "Alarme15_15":                          [14 + 14199, 15],

        "Alarme16_00":                          [15 + 14199, 0],
        "Alarme16_01":                          [15 + 14199, 1],
        "Alarme16_02":                          [15 + 14199, 2],
        "Alarme16_03":                          [15 + 14199, 3],
        "Alarme16_04":                          [15 + 14199, 4],
        "Alarme16_05":                          [15 + 14199, 5],
        "Alarme16_06":                          [15 + 14199, 6],
        "Alarme16_07":                          [15 + 14199, 7],
        "Alarme16_08":                          [15 + 14199, 8],
        "Alarme16_09":                          [15 + 14199, 9],
        "Alarme16_10":                          [15 + 14199, 10],
        "Alarme16_11":                          [15 + 14199, 11],
        "Alarme16_12":                          [15 + 14199, 12],
    },
}