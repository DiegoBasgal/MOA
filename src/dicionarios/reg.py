REG_MOA = {

}
                                                                                # NOME REGISTRADORES ELIPSE:
REG_SA = {
    ## COMANDOS
    # Gerais
    "CMD_RESET_ALARMES":                        0 + 12289,                      # Comandos.ResetAlarmes
    "CMD_RECONHECE_ALARMES":                    1 + 12289,                      # Comandos.ReconheceAlarmes
    "CMD_EMERGENCIA_LIGAR":                     2 + 12289,                      # Comandos.EmergenciaLigar
    "CMD_EMERGENCIA_DESLIGAR":                  3 + 12289,                      # Comandos.EmergenciaDesligar
    "CMD_SEL_MODO_LOCAL":                       6 + 12289,                      # Comandos.ServAuxiliar_SelecionaModoLocal
    "CMD_SEL_MODO_REMOTO":                      7 + 12289,                      # Comandos.ServAuxiliar_SelecionaModoRemoto
    "CMD_SEL_MODO_MANUAL":                      8 + 12289,                      # Comandos.ServAuxiliar_SelecionaModoManual
    "CMD_SEL_MODO_AUTOMATICO":                  9 + 12289,                      # Comandos.ServAuxiliar_SelecionaModoAutomatico

    # Disjuntor
    "CMD_DJ_FONTE_01_LIGAR":                    10 + 12289,                     # Comandos.ServAuxiliar_DisjFonte01Ligar
    "CMD_DJ_FONTE_01_DESLIGAR":                 11 + 12289,                     # Comandos.ServAuxiliar_DisjFonte01Desligar
    "CMD_DJ_FONTE_02_LIGAR":                    12 + 12289,                     # Comandos.ServAuxiliar_DisjFonte02Ligar
    "CMD_DJ_FONTE_02_DESLIGAR":                 13 + 12289,                     # Comandos.ServAuxiliar_DisjFonte02Desligar
    "CMD_DJ_FONTE_04_LIGAR":                    14 + 12289,                     # Comandos.ServAuxiliar_DisjFonte04Ligar
    "CMD_DJ_FONTE_04_DESLIGAR":                 15 + 12289,                     # Comandos.ServAuxiliar_DisjFonte04Desligar
    "CMD_DJ_FONTE_05_LIGAR":                    97 + 12289,                     # Comandos.ServAuxiliar_DisjFonte05Ligar
    "CMD_DJ_FONTE_05_DESLIGAR":                 98 + 12289,                     # Comandos.ServAuxiliar_DisjFonte05Desligar

    # Gerador Diesel
    "CMD_GD_PARTIR":                            16 + 12289,                     # Comandos.GrupoDiesel_Partir
    "CMD_GD_PARAR":                             17 + 12289,                     # Comandos.GrupoDiesel_Parar

    # Carregador de Baterias
    "CMD_CB_MODO_FLUTUACAO_LIGAR":              18 + 12289,                     # Comandos.CarregadorBateria_ModoFlutuacaoLigar
    "CMD_CB_MODO_EQUALIZACAO_LIGAR":            19 + 12289,                     # Comandos.CarregadorBateria_ModoEqualizacaoLigar

    # Poço
    "CMD_POCO_BOMBA_01_LIGAR":                  20 + 12289,                     # Comandos.Poco_Bomba01Ligar
    "CMD_POCO_BOMBA_01_DESLIGAR":               21 + 12289,                     # Comandos.Poco_Bomba01Desligar
    "CMD_POCO_BOMBA_01_PRINCIPAL":              22 + 12289,                     # Comandos.Poco_Bomba01Principal
    "CMD_POCO_BOMBA_02_LIGAR":                  23 + 12289,                     # Comandos.Poco_Bomba02Ligar
    "CMD_POCO_BOMBA_02_DESLIGAR":               24 + 12289,                     # Comandos.Poco_Bomba02Desligar
    "CMD_POCO_BOMBA_02_PRINCIPAL":              25 + 12289,                     # Comandos.Poco_Bomba02Principal
    "CMD_POCO_BOMBA_03_LIGAR":                  26 + 12289,                     # Comandos.Poco_Bomba03ligar
    "CMD_POCO_BOMBA_03_DESLIGAR":               27 + 12289,                     # Comandos.Poco_Bomba03Desligar
    "CMD_POCO_BOMBA_04_LIGAR":                  28 + 12289,                     # Comandos.Poco_Bomba04ligar
    "CMD_POCO_BOMBA_04_DESLIGAR":               29 + 12289,                     # Comandos.Poco_Bomba04Desligar
    "CMD_POCO_SEL_MODO_MANUAL":                 30 + 12289,                     # Comandos.Poco_SelecionaModoManual
    "CMD_POCO_SEL_MODO_AUTOMATICO":             31 + 12289,                     # Comandos.Poco_SelecionaModoAutomatico

    # Sensores
    "CMD_SENSOR_PRESEN_HABILITAR":              32 + 12289,                     # Comandos.SensorPresenca_Habilitar
    "CMD_SENSOR_PRESEN_DESABILITAR":            33 + 12289,                     # Comandos.SensorPresenca_Desabilitar
    "CMD_SENSOR_FUMACA_RESET":                  34 + 12289,                     # Comandos.[SensorFumaça_Reset]

    # Injeção Água Selo
    "CMD_IA_SELO_RODIZIO_AUTO":                 77 + 12289,                     # Comandos.InjecaoAguaSelo_RodizioAutomatico
    "CMD_IA_SELO_RODIZIO_MANUAL":               78 + 12289,                     # Comandos.InjecaoAguaSelo_RodizioManual
    "CMD_IA_SELO_BOMBA_01_LIGAR":               79 + 12289,                     # Comandos.InjecaoAguaSelo_Bomba01_Ligar
    "CMD_IA_SELO_BOMBA_01_DESLIGAR":            80 + 12289,                     # Comandos.InjecaoAguaSelo_Bomba01_Desligar
    "CMD_IA_SELO_BOMBA_01_PRINCIPAL":           81 + 12289,                     # Comandos.InjecaoAguaSelo_Bomba01_Principal
    "CMD_IA_SELO_BOMBA_02_LIGAR":               82 + 12289,                     # Comandos.InjecaoAguaSelo_Bomba02_Ligar
    "CMD_IA_SELO_BOMBA_02_DESLIGAR":            83 + 12289,                     # Comandos.InjecaoAguaSelo_Bomba02_Desligar
    "CMD_IA_SELO_BOMBA_02_PRINCIPAL":           84 + 12289,                     # Comandos.InjecaoAguaSelo_Bomba02_Principal

    # Água Serviço
    "CMD_AS_RODIZIO_AUTO":                      85 + 12289,                     # Comandos.AguaServico_RodizioAutomatico
    "CMD_AS_RODIZIO_MANUAL":                    86 + 12289,                     # Comandos.AguaServico_RodizioManual
    "CMD_AS_BOMBA_01_LIGAR":                    87 + 12289,                     # Comandos.AguaServico_Bomba01_Ligar
    "CMD_AS_BOMBA_01_DESLIGAR":                 88 + 12289,                     # Comandos.AguaServico_Bomba01_Desligar
    "CMD_AS_BOMBA_01_PRINCIPAL":                89 + 12289,                     # Comandos.AguaServico_Bomba01_Principal
    "CMD_AS_BOMBA_02_LIGAR":                    90 + 12289,                     # Comandos.AguaServico_Bomba02_Ligar
    "CMD_AS_BOMBA_02_DESLIGAR":                 91 + 12289,                     # Comandos.AguaServico_Bomba02_Desligar
    "CMD_AS_BOMBA_02_PRINCIPAL":                92 + 12289,                     # Comandos.AguaServico_Bomba02_Principal
    "CMD_AS_CIRCUITO_ABARTO_SEL":               93 + 12289,                     # Comandos.AguaServico_CircuitoAberto_Selecionar
    "CMD_AS_CIRCUITO_FECHADO_SEL":              94 + 12289,                     # Comandos.AguaServico_CircuitoFechado_Selecionar
    "CMD_AS_FILTRO_01_SEL":                     95 + 12289,                     # Comandos.AguaServico_Filtro01_Selecionar
    "CMD_AS_FILTRO_02_SEL":                     96 + 12289,                     # Comandos.AguaServico_Filtro02_Selecionar


    ## SETPOINTS
    # Poço
    "POCO_TEMPO_RODIZIO_LIDER":                 8 + 13569,                      # Setpoints.Poco_TempoRodizioLider
    "POCO_TEMPO_RODIZIO_RETAGUARDA":            9 + 13569,                      # Setpoints.Poco_TempoRodizioRetaguarda

    # Injeção Selo
    "IS_TEMPO_BOMBA_LIDER":                     18 + 13569,                     # Setpoints.InjecaoSelo_TempoBombaLider
    "IS_TEMPO_BOMBA_RETAGUARDA":                19 + 13569,                     # Setpoints.InjecaoSelo_TempoBombaRetaguarda

    # Agua Serviço
    "AS_TEMPO_BOMBA_LIDER":                     20 + 13569,                     # Setpoints.AguaServico_TempoBombaLider
    "AS_TEMPO_BOMBA_RETAGUARDA":                21 + 13569,                     # Setpoints.AguaServico_TempoBombaRetaguarda


    ## LEITURAS
    "RESET_ALARMES":                            6 + 12764,                      # Leituras.PainelResetAlarmes
    "RECONHECE_ALARMES":                        7 + 12764,                      # Leituras.PainelReconheceAlarmes

    "EMERGENCIA_USINA":                         8 + 12764,                      # Leituras.Usina_Emergencia_Info
    "EMERGENCIA_ACIONADA":                      [8 + 12764, 0],                 # Usina.Emergencia.Acionada
    "EMERGENCIA_SIRENE_LIG":                    [8 + 12764, 1],                 # Usina.Emergencia.Sireneligada
    "EMERGENCIA_MODO_REMOTO":                   [8 + 12764, 2],                 # Usina.Emergencia.Usina_OpercaoModoRemoto
    "EMERGENCIA_MODO_LOCAL":                    [8 + 12764, 3],                 # Usina.Emergencia.Usina_OpercaoModoLocal

    # Carregador de Baterias
    "CB_INFO":                                  10 + 12764,                     # Leituras.CarregadorBateria_Info
    "CB_EQUALIZACAO":                           [10 + 12764, 0],                # CarregadorBaterias.Info.Equalizacao
    "CB_ALARME":                                [10 + 12764, 1],                # CarregadorBaterias.Info.Alarme
    "CB_LIGADO":                                [10 + 12764, 2],                # CarregadorBaterias.Info.Ligado

    "CB_UENTRADA":                              11 + 12764,                     # Leituras.CarregadorBateria_UEntrada
    "CB_USAIDA":                                12 + 12764,                     # Leituras.CarregadorBateria_USaida
    "CB_IENTRADA":                              13 + 12764,                     # Leituras.CarregadorBateria_IEntrada
    "CB_ISAIDA":                                14 + 12764,                     # Leituras.CarregadorBateria_ISaida

    "CB2_INFO":                                 197 + 12764,                    # Leituras.CB2_Info
    "CB2_EQUALIZACAO":                          [197 + 12764, 0],               # CarregadorBaterias2.Info.Equalizacao
    "CB2_ALARME":                               [197 + 12764, 1],               # CarregadorBaterias2.Info.Alarme
    "CB2_LIGADO":                               [197 + 12764, 2],               # CarregadorBaterias2.Info.Ligado

    "CB2_UENTRADA":                             198 + 12764,                    # Leituras.CB2_UEntrada
    "CB2_USAIDA":                               199 + 12764,                    # Leituras.CB2_USaida
    "CB2_IENTRADA":                             200 + 12764,                    # Leituras.CB2_IEntrada
    "CB2_ISAIDA":                               201 + 12764,                    # Leituras.CB2_ISaida

    # Gerador Diesel
    "GD_INFO":                                  15 + 12764,                     # Leituras.GrupoDiesel_Info
    "GD_LIGADO":                                [15 + 12764, 0],                # GrupoDiesel.Info.Ligado
    "GD_DESLIGADO":                             [15 + 12764, 1],                # GrupoDiesel.Info.Desligado
    "GD_MANUAL":                                [15 + 12764, 2],                # GrupoDiesel.Info.Manual
    "GD_AUTOMATICO":                            [15 + 12764, 3],                # GrupoDiesel.Info.Automatico
    "GD_TESTE":                                 [15 + 12764, 4],                # GrupoDiesel.Info.Teste
    "GD_COMB_MENOR30":                          [15 + 12764, 5],                # GrupoDiesel.Info.[Comb<30]

    "GD_NIVEL_COMBUS":                          16 + 12764,                     # Leituras.GrupoDiesel_NivelCombustivel
    "GD_ROTACAO":                               17 + 12764,                     # Leituras.GrupoDiesel_RotacaoMotor
    "GD_TENSAO_BATERIA":                        18 + 12764,                     # Leituras.GrupoDiesel_TensaoBateria
    "GD_TENSAO_ALTERNADOR":                     19 + 12764,                     # Leituras.GrupoDiesel_TensaoAlternador
    "GD_TENSAO_L1":                             189 + 12764,                    # Leituras.GD_TensaoL1
    "GD_TENSAO_L2":                             190 + 12764,                    # Leituras.GD_TensaoL2
    "GD_TENSAO_L3":                             191 + 12764,                    # Leituras.GD_TensaoL3
    "GD_TENSAO_L1L2":                           192 + 12764,                    # Leituras.GD_TensaoL1L2
    "GD_TENSAO_L2L3":                           193 + 12764,                    # Leituras.GD_TensaoL2L3
    "GD_TENSAO_L3L1":                           194 + 12764,                    # Leituras.GD_TensaoL3L1
    "GD_FREQUANCIA":                            195 + 12764,                    # Leituras.GD_Frequencia
    "GD_TEMPAGUA":                              196 + 12764,                    # Leituras.GD_TempAgua

    # SA
    "SA_INFO":                                  66 + 12764,                     # Leituras.ServAuxiliar_Info
    "SA_MODO_LOCAL":                            [66 + 12764, 0],                # ServAuxiliar.Info.Local
    "SA_MODO_REMOTO":                           [66 + 12764, 1],                # ServAuxiliar.Info.Remoto
    "SA_MODO_AUTO":                             [66 + 12764, 2],                # ServAuxiliar.Info.Automatico
    "SA_MODO_MANUAL":                           [66 + 12764, 3],                # ServAuxiliar.Info.Manual
    "SA_ALIM_FONTE01_ATIVA":                    [66 + 12764, 4],                # ServAuxiliar.Info.Alimentacao_Fonte01Ativa
    "SA_ALIM_FONTE02_ATIVA":                    [66 + 12764, 5],                # ServAuxiliar.Info.Alimentacao_Fonte02Ativa
    "SA_ALIM_FONTE03_ATIVA":                    [66 + 12764, 6],                # ServAuxiliar.Info.Alimentacao_Fonte03Ativa
    "SA_TENSAO_PRES_FONTE01":                   [66 + 12764, 7],                # ServAuxiliar.Info.TensaoPresente_Fonte01
    "SA_TENSAO_PRES_FONTE02":                   [66 + 12764, 8],                # ServAuxiliar.Info.TensaoPresente_Fonte02
    "SA_TENSAO_PRES_FONTE03":                   [66 + 12764, 9],                # ServAuxiliar.Info.TensaoPresente_Fonte03
    "SA_SECC_CSA01_ABERTA":                     [66 + 12764, 10],               # ServAuxiliar.Info.SeccionadoraCSA01_Aberta
    "SA_SECC_CSA01_FECHADA":                    [66 + 12764, 11],               # ServAuxiliar.Info.SeccionadoraCSA01_Fechada
    "SA_SECC_CSA02_ABERTA":                     [66 + 12764, 12],               # ServAuxiliar.Info.SeccionadoraCSA02_Aberta
    "SA_SECC_CSA02_FECHADA":                    [66 + 12764, 13],               # ServAuxiliar.Info.SeccionadoraCSA02_Fechada
    "SA_CARGAS_NAO_ESSEN":                      [66 + 12764, 14],               # ServAuxiliar.Info.CargasNaoEssenciais

    # Tensão
    "TENSAO_RN":                                67 + 12764,                     # Leituras.ServAuxiliar_TensaoRN
    "TENSAO_SN":                                68 + 12764,                     # Leituras.ServAuxiliar_TensaoSN
    "TENSAO_TN":                                69 + 12764,                     # Leituras.ServAuxiliar_TensaoTN
    "TENSAO_RS":                                70 + 12764,                     # Leituras.ServAuxiliar_TensaoRS
    "TENSAO_ST":                                71 + 12764,                     # Leituras.ServAuxiliar_TensaoST
    "TENSAO_TR":                                72 + 12764,                     # Leituras.ServAuxiliar_TensaoTR

    # Corrente
    "CORRENTE_R":                               73 + 12764,                     # Leituras.ServAuxiliar_CorrenteR
    "CORRENTE_S":                               74 + 12764,                     # Leituras.ServAuxiliar_CorrenteS
    "CORRENTE_T":                               75 + 12764,                     # Leituras.ServAuxiliar_CorrenteT
    "CORRENTE_MEDIA":                           76 + 12764,                     # Leituras.ServAuxiliar_CorrenteMedia

    # Potência
    "POTENCIA_ATIVA_1":                         77 + 12764,                     # Leituras.ServAuxiliar_PotenciaAtiva1
    "POTENCIA_ATIVA_2":                         78 + 12764,                     # Leituras.ServAuxiliar_PotenciaAtiva2
    "POTENCIA_ATIVA_3":                         79 + 12764,                     # Leituras.ServAuxiliar_PotenciaAtiva3
    "POTENCIA_ATIVA_MEDIA":                     80 + 12764,                     # Leituras.ServAuxiliar_PotenciaAtivaMedia
    "POTENCIA_REATIVA_1":                       81 + 12764,                     # Leituras.ServAuxiliar_PotenciaReativa1
    "POTENCIA_REATIVA_2":                       82 + 12764,                     # Leituras.ServAuxiliar_PotenciaReativa2
    "POTENCIA_REATIVA_3":                       83 + 12764,                     # Leituras.ServAuxiliar_PotenciaReativa3
    "POTENCIA_REATIVA_MEDIA":                   84 + 12764,                     # Leituras.ServAuxiliar_PotenciaReativaMedia
    "POTENCIA_APARENTE_1":                      85 + 12764,                     # Leituras.ServAuxiliar_PotenciaAparente1
    "POTENCIA_APARENTE_2":                      86 + 12764,                     # Leituras.ServAuxiliar_PotenciaAparente2
    "POTENCIA_APARENTE_3":                      87 + 12764,                     # Leituras.ServAuxiliar_PotenciaAparente3
    "POTENCIA_APARENTE_MEDIA":                  88 + 12764,                     # Leituras.ServAuxiliar_PotenciaAparenteMedia

    # Fator Potência
    "FATOR_POTENCIA_1":                         89 + 12764,                     # Leituras.ServAuxiliar_FatorPotencia1
    "FATOR_POTENCIA_2":                         90 + 12764,                     # Leituras.ServAuxiliar_FatorPotencia2
    "FATOR_POTENCIA_3":                         91 + 12764,                     # Leituras.ServAuxiliar_FatorPotencia3
    "FATOR_POTENCIA_MEDIA":                     92 + 12764,                     # Leituras.ServAuxiliar_FatorPotenciaMedia

    # Frequência
    "FREQUENCIA":                               93 + 12764,                     # Leituras.ServAuxiliar_Frequencia

    # Energia Consumida
    "ENERGIA_CONSUMIDA_GWh":                    94 + 12764,                     # Leituras.ServAuxiliar_EnergiaConsumidaGWh
    "ENERGIA_CONSUMIDA_MWh":                    95 + 12764,                     # Leituras.ServAuxiliar_EnergiaConsumidaMWh
    "ENERGIA_CONSUMIDA_KWh":                    96 + 12764,                     # Leituras.ServAuxiliar_EnergiaConsumidaKWh
    "ENERGIA_CONSUMIDA_Wh":                     97 + 12764,                     # Leituras.ServAuxiliar_EnergiaConsumidaWh
    "ENERGIA_CONSUMIDA_GVArh":                  98 + 12764,                     # Leituras.ServAuxiliar_EnergiaConsumidaGVArh
    "ENERGIA_CONSUMIDA_MVArh":                  99 + 12764,                     # Leituras.ServAuxiliar_EnergiaConsumidaMVArh
    "ENERGIA_CONSUMIDA_KVArh":                  100 + 12764,                    # Leituras.ServAuxiliar_EnergiaConsumidaKVArh
    "ENERGIA_CONSUMIDA_WVArh":                  101 + 12764,                    # Leituras.ServAuxiliar_EnergiaConsumidaWVArh
    "ENERGIA_FORNECIDA_GVArh":                  102 + 12764,                    # Leituras.ServAuxiliar_EnergiaFornecidaGVArh
    "ENERGIA_FORNECIDA_MVArh":                  103 + 12764,                    # Leituras.ServAuxiliar_EnergiaFornecidaMVArh
    "ENERGIA_FORNECIDA_KVArh":                  104 + 12764,                    # Leituras.ServAuxiliar_EnergiaFornecidaKVArh
    "ENERGIA_FORNECIDA_VArh":                   105 + 12764,                    # Leituras.ServAuxiliar_EnergiaFornecidaVArh

    # Fuga Terra
    "FUGA_TERRA_TENSAO_POSITIVA":               106 + 12764,                    # Leituras.ServAux_FugaTerra_TensaoPositiva
    "FUGA_TERRA_TENSAO_NEGATIVA":               107 + 12764,                    # Leituras.ServAux_FugaTerra_TensaoNegativa
    "FUGA_TERRA_TENSAO":                        108 + 12764,                    # Leituras.ServAux_FugaTerra_Tensao

    "FUGA_TERRA_INFO":                          110 + 12764,                    # Leituras.ServAux_FugaTerra_Info
    "FUGA_TERRA_POSITIVO":                      [110 + 12764, 0],               # ReleFugaTerra.Info.FugaTerraPositivo
    "FUGA_TERRA_NEGATIVO":                      [110 + 12764, 1],               # ReleFugaTerra.Info.FugaTerraNegativo
    "FUGA_TERRA_SUBTENSAO":                     [110 + 12764, 2],               # ReleFugaTerra.Info.Subtensao
    "FUGA_TERRA_SOBRETENSAO":                   [110 + 12764, 3],               # ReleFugaTerra.Info.Sobretensao
    "FUGA_TERRA_ALARME":                        [110 + 12764, 4],               # ReleFugaTerra.Info.Alarme
    "FUGA_TERRA_TRIP":                          [110 + 12764, 5],               # ReleFugaTerra.Info.TRIP

    # Poço
    "POCO_INFO":                                111 + 12764,                    # Leituras.Poco_Info
    "POCO_MODO_LOCAL":                          [111 + 12764, 0],               # Poco.Info.ModoLocal
    "POCO_MODO_MANUAL":                         [111 + 12764, 1],               # Poco.Info.ModoManual
    "POCO_MODO_AUTO":                           [111 + 12764, 2],               # Poco.Info.ModoAuto
    "POCO_BOMBA01_PRINCI":                      [111 + 12764, 3],               # Poco.Info.Bomba01Principal
    "POCO_BOMBA02_PRINCI":                      [111 + 12764, 4],               # Poco.Info.Bomba02Principal
    "POCO_RODIZ_BOMBA02_ATIVA":                 [111 + 12764, 5],               # Poco.Info.RodizioBomba02Ativa
    "POCO_FLUXOSTATO_BOMBA01":                  [111 + 12764, 6],               # Poco.Info.FluxostatoBomba01
    "POCO_FLUXOSTATO_BOMBA02":                  [111 + 12764, 7],               # Poco.Info.FluxostatoBomba02
    "POCO_FLUXOSTATO_BOMBA03":                  [111 + 12764, 8],               # Poco.Info.FluxostatoBomba03

    "POCO_BOMBAS":                              112 + 12764,                    # Leituras.Poco_Bombas
    "POCO_BOMBA01":                             [112 + 12764, 0],               # Poco.Bombas.Bomba01
    "POCO_BOMBA02":                             [112 + 12764, 1],               # Poco.Bombas.Bomba02
    "POCO_BOMBA03":                             [112 + 12764, 2],               # Poco.Bombas.Bomba03
    "POCO_BOMBA04":                             [112 + 12764, 3],               # Poco.Bombas.Bomba04
    "POCO_INJ_SELO_BOMBA01":                    [112 + 12764, 4],               # Poco.Bombas.InjecaoSelo_Bomba01
    "POCO_INJ_SELO_BOMBA02":                    [112 + 12764, 5],               # Poco.Bombas.InjecaoSelo_Bomba02
    "POCO_AGUA_SERV_BOMBA01":                   [112 + 12764, 6],               # Poco.Bombas.AguaServico_Bomba01
    "POCO_AGUA_SERV_BOMBA02":                   [112 + 12764, 7],               # Poco.Bombas.AguaServico_Bomba02

    "POCO_NIVEL":                               113 + 12764,                    # Leituras.Poco_Nivel
    "POCO_NIVEL_LL":                            [113 + 12764, 0],               # Poco.Niveis.NivelLL
    "POCO_NIVEL_L":                             [113 + 12764, 1],               # Poco.Niveis.NivelL
    "POCO_NIVEL_H":                             [113 + 12764, 2],               # Poco.Niveis.NivelH
    "POCO_NIVEL_HH":                            [113 + 12764, 3],               # Poco.Niveis.NivelHH

    "POCO_HORIMETRO_PRINCIPAL":                 114 + 12764,                    # Leituras.Poco_HorimetroPrincipal
    "POCO_HORIMETRO_RETAGUARDA":                115 + 12764,                    # Leituras.Poco_HorimetroRetaguarda

    # Sensores
    "SENSOR_FUMACA_INFO":                       116 + 12764,                    # Leituras.SensorFumaca_Info

    "SENSOR_PRESENCA_INFO":                     117 + 12764,                    # Leituras.SensorPresenca_Info
    "SENSOR_PRESENCA_HABILITADO":               [117 + 12764, 0],               # SensorPresenca.Habilitado
    "SENSOR_PRESENCA_SALA_SUP":                 [117 + 12764, 1],               # SensorPresenca.SalaSupervisorio
    "SENSOR_PRESENCA_SALA_COZI_BANH":           [117 + 12764, 2],               # SensorPresenca.SalaCozinhaBanheiro
    "SENSOR_PRESENCA_ALMOXARI":                 [117 + 12764, 3],               # SensorPresenca.Almoxarifado
    "SENSOR_PRESENCA_AREA_MONT":                [117 + 12764, 4],               # SensorPresenca.AreaMontagem
    "SENSOR_PRESENCA_SALA_CUBI":                [117 + 12764, 5],               # SensorPresenca.SalaCubiculos

    # Temperaturas
    "USINA_TEMPERATURA_01":                     119 + 12764,                    # Leituras.Usina_Temperatura_01
    "USINA_TEMPERATURA_02":                     120 + 12764,                    # Leituras.Usina_Temperatura_02
    "USINA_TEMPERATURA_03":                     121 + 12764,                    # Leituras.Usina_Temperatura_03
    "USINA_TEMPERATURA_04":                     122 + 12764,                    # Leituras.Usina_Temperatura_04
    "USINA_TEMPERATURA_05":                     123 + 12764,                    # Leituras.Usina_Temperatura_05
    "USINA_TEMPERATURA_06":                     124 + 12764,                    # Leituras.Usina_Temperatura_06
    "USINA_TEMPERATURA_07":                     125 + 12764,                    # Leituras.Usina_Temperatura_07
    "USINA_TEMPERATURA_08":                     126 + 12764,                    # Leituras.Usina_Temperatura_08

    # Sistema de Água
    "SIS_AGUA_INFO":                            181 + 12764,                    # Leituras.SistemaAgua_Info
    "SIS_AGUA_CAIXA_AGUA01_NV100":              [181 + 12764, 0],               # SistemaAgua.Info.CaixaDAgua01_Nivel100
    "SIS_AGUA_CIRQUITO_FECHADO":                [181 + 12764, 1],               # SistemaAgua.Info.CircuitoFechado
    "SIS_AGUA_CIRQUITO_ABERTO":                 [181 + 12764, 2],               # SistemaAgua.Info.CircuitoAberto
    "SIS_AGUA_FILTRO01":                        [181 + 12764, 3],               # SistemaAgua.Info.Filtro01
    "SIS_AGUA_FILTRO02":                        [181 + 12764, 4],               # SistemaAgua.Info.Filtro02
    "SIS_AGUA_AGUA_SERV_BOMBA01_FLUXOS":        [181 + 12764, 5],               # SistemaAgua.Info.AguaServico_Bomba01_Fluxostato
    "SIS_AGUA_AGUA_SERV_BOMBA02_FLUXOS":        [181 + 12764, 6],               # SistemaAgua.Info.AguaServico_Bomba02_Fluxostato
    "SIS_AGUA_INJ_SELO_BOMBA01_FLUXOS":         [181 + 12764, 7],               # SistemaAgua.Info.InjecaoSelo_Bomba01_Fluxostato
    "SIS_AGUA_INJ_SELO_BOMBA02_FLUXOS":         [181 + 12764, 8],               # SistemaAgua.Info.InjecaoSelo_Bomba02_Fluxostato
    "SIS_AGUA_CAIXA_AGUA01_NV75":               [181 + 12764, 9],               # SistemaAgua.Info.CaixaDAgua01_Nivel75
    "SIS_AGUA_CAIXA_AGUA01_NV50":               [181 + 12764, 10],              # SistemaAgua.Info.CaixaDAgua01_Nivel50
    "SIS_AGUA_CAIXA_AGUA02_NV100":              [181 + 12764, 11],              # SistemaAgua.Info.CaixaDAgua02_Nivel100
    "SIS_AGUA_CAIXA_AGUA02_NV75":               [181 + 12764, 12],              # SistemaAgua.Info.CaixaDAgua02_Nivel75
    "SIS_AGUA_CAIXA_AGUA02_NV50":               [181 + 12764, 13],              # SistemaAgua.Info.CaixaDAgua02_Nivel50

    "SIS_AGUA_BOMBA":                           182 + 12764,                    # Leituras.SistemaAgua_Bombas
    "SIS_AGUA_BOM_INJ_SELO_BOMBA01":            [182 + 12764, 0],               # SistemaAgua.Bombas.InjecaoSelo_Bomba01
    "SIS_AGUA_BOM_INJ_SELO_BOMBA02":            [182 + 12764, 1],               # SistemaAgua.Bombas.InjecaoSelo_Bomba02
    "SIS_AGUA_BOM_AGUA_SERV_BOMBA01":           [182 + 12764, 2],               # SistemaAgua.Bombas.AguaServico_Bomba01
    "SIS_AGUA_BOM_AGUA_SERV_BOMBA02":           [182 + 12764, 3],               # SistemaAgua.Bombas.AguaServico_Bomba02
    "SIS_AGUA_BOM_INJ_SELO_RODIZ_BOMBA01":      [182 + 12764, 4],               # SistemaAgua.Bombas.InjecaoSelo_RodizioBomba01
    "SIS_AGUA_BOM_INJ_SELO_RODIZ_BOMBA02":      [182 + 12764, 5],               # SistemaAgua.Bombas.InjecaoSelo_RodizioBomba02
    "SIS_AGUA_BOM_INJ_SELO_RODIZ_HABILI":       [182 + 12764, 6],               # SistemaAgua.Bombas.InjecaoSelo_RodizioHabilitado
    "SIS_AGUA_BOM_AGUA_SERV_RODIZ_BOMBA01":     [182 + 12764, 7],               # SistemaAgua.Bombas.AguaServico_RodizioBomba01
    "SIS_AGUA_BOM_AGUA_SERV_RODIZ_BOMBA02":     [182 + 12764, 8],               # SistemaAgua.Bombas.AguaServico_RodizioBomba02
    "SIS_AGUA_BOM_AGUA_SERV_RODIZ_HABILI":      [182 + 12764, 9],               # SistemaAgua.Bombas.AguaServico_RodizioHabilitado

    "SIS_AGUA_VALVULAS":                        183 + 12764,                    # Leituras.SistemaAgua_Valvulas
    "SIS_AGUA_VAL_ENTRADA_FILTRO01_ABERTA":     [183 + 12764, 0],               # SistemaAgua.Valvulas.EntradaFiltro01_Aberta
    "SIS_AGUA_VAL_ENTRADA_FILTRO01_FECHADA":    [183 + 12764, 1],               # SistemaAgua.Valvulas.EntradaFiltro01_Fechada
    "SIS_AGUA_VAL_ENTRADA_FILTRO02_ABERTA":     [183 + 12764, 2],               # SistemaAgua.Valvulas.EntradaFiltro02_Aberta
    "SIS_AGUA_VAL_ENTRADA_FILTRO02_FECHADA":    [183 + 12764, 3],               # SistemaAgua.Valvulas.EntradaFiltro02_Fechada
    "SIS_AGUA_VAL_ENTRADA_TORRE_ABERTA":        [183 + 12764, 4],               # SistemaAgua.Valvulas.EntradaTorre_Aberta
    "SIS_AGUA_VAL_ENTRADA_TORRE_FECHADA":       [183 + 12764, 5],               # SistemaAgua.Valvulas.EntradaTorre_Fechada
    "SIS_AGUA_VAL_SAIDA_TORRE_ABERTA":          [183 + 12764, 6],               # SistemaAgua.Valvulas.SaidaTorre_Aberta
    "SIS_AGUA_VAL_SAIDA_TORRE_FECHADA":         [183 + 12764, 7],               # SistemaAgua.Valvulas.SaidaTorre_Fechada
    "SIS_AGUA_VAL_DESCARGA_01_ABERTA":          [183 + 12764, 8],               # SistemaAgua.Valvulas.Descarga01Aberta
    "SIS_AGUA_VAL_DESCARGA_01_FECHADA":         [183 + 12764, 9],               # SistemaAgua.Valvulas.Descarga01Fechada
    "SIS_AGUA_VAL_DESCARGA_02_ABERTA":          [183 + 12764, 10],              # SistemaAgua.Valvulas.Descarga02Aberta
    "SIS_AGUA_VAL_DESCARGA_02_FECHADA":         [183 + 12764, 11],              # SistemaAgua.Valvulas.Descarga02Fechada
    "SIS_AGUA_VAL_DESCARGA_03_ABERTA":          [183 + 12764, 12],              # SistemaAgua.Valvulas.Descarga03Aberta
    "SIS_AGUA_VAL_DESCARGA_03_FECHADA":         [183 + 12764, 13],              # SistemaAgua.Valvulas.Descarga03Fechada
    "SIS_AGUA_VAL_DESCARGA_04_ABERTA":          [183 + 12764, 14],              # SistemaAgua.Valvulas.Descarga04Aberta
    "SIS_AGUA_VAL_DESCARGA_04_FECHADA":         [183 + 12764, 15],              # SistemaAgua.Valvulas.Descarga04Fechada

    "SIS_AGUA_VALVULAS2":                       188 + 12764,                    # Leituras.SistemaAgua_Valvulas2
    "SIS_AGUA_VAL2_ENTRA_UG01_ABERTA":          [188 + 12764, 0],               # SistemaAgua.Valvulas2.EntradaUG01_Aberta
    "SIS_AGUA_VAL2_ENTRA_UG01_FECHADA":         [188 + 12764, 1],               # SistemaAgua.Valvulas2.EntradaUG01_Fechada
    "SIS_AGUA_VAL2_ENTRA_UG02_ABERTA":          [188 + 12764, 2],               # SistemaAgua.Valvulas2.EntradaUG02_Aberta
    "SIS_AGUA_VAL2_ENTRA_UG02_FECHADA":         [188 + 12764, 3],               # SistemaAgua.Valvulas2.EntradaUG02_Fechada
    "SIS_AGUA_VAL2_ENTRA_UG03_ABERTA":          [188 + 12764, 4],               # SistemaAgua.Valvulas2.EntradaUG03_Aberta
    "SIS_AGUA_VAL2_ENTRA_UG03_FECHADA":         [188 + 12764, 5],               # SistemaAgua.Valvulas2.EntradaUG03_Fechada
    "SIS_AGUA_VAL2_ENTRA_UG04_ABERTA":          [188 + 12764, 6],               # SistemaAgua.Valvulas2.EntradaUG04_Aberta
    "SIS_AGUA_VAL2_ENTRA_UG04_FECHADA":         [188 + 12764, 7],               # SistemaAgua.Valvulas2.EntradaUG04_Fechada

    # Injeção Selo
    "IS_ACUMULADOR_LIDER":                      184 + 12764,                    # Leituras.InjecaoSelo_AcumuladorLider
    "IS_ACUMULADOR_RETAGUARDA":                 185 + 12764,                    # Leituras.InjecaoSelo_AcumuladorRetaguarda

    # Água Serviço
    "AS_ACUMULADOR_LIDER":                      186 + 12764,                    # Leituras.AguaServico_AcumuladorLider
    "AS_ACUMULADOR_RETAGUARDA":                 187 + 12764,                    # Leituras.AguaServico_AcumuladorRetaguarda

    # Rendimento
    "RENDIMENTO_UG01":                          203 + 12764,                    # Leituras.Rendimento_UG01
    "RENDIMENTO_UG02":                          204 + 12764,                    # Leituras.Rendimento_UG02
    "RENDIMENTO_UG03":                          205 + 12764,                    # Leituras.Rendimento_UG03
    "RENDIMENTO_UG04":                          206 + 12764,                    # Leituras.Rendimento_UG04
    "RENDIMENTO_GERAL":                         207 + 12764,                    # Leituras.Rendimento_Geral

    "RENDIMENTO_INFO":                          218 + 12764,                    # Leituras.Rendimento_Info
    "RENDIMEN_RESERV_ESVAZIANDO":               [218 + 12764, 0],               # RendimentoVazao.ReservEsvaziando
    "RENDIMEN_RESERV_ENCHENDO":                 [218 + 12764, 1],               # RendimentoVazao.ReservEnchendo
    "RENDIMEN_RESERV_ESTAVEL":                  [218 + 12764, 2],               # RendimentoVazao.ReservEstavel


    "RENDIMENTO_TURBINA_UG01":                  219 + 12764,                    # Leituras.RendimentoTurbina_UG01
    "RENDIMENTO_TURBINA_UG02":                  220 + 12764,                    # Leituras.RendimentoTurbina_UG02
    "RENDIMENTO_TURBINA_UG03":                  221 + 12764,                    # Leituras.RendimentoTurbina_UG03
    "RENDIMENTO_TURBINA_UG04":                  222 + 12764,                    # Leituras.RendimentoTurbina_UG04
    "RENDIMENTO_GERADOR_UG01":                  223 + 12764,                    # Leituras.RendimentoGerador_UG01
    "RENDIMENTO_GERADOR_UG02":                  224 + 12764,                    # Leituras.RendimentoGerador_UG02
    "RENDIMENTO_GERADOR_UG03":                  225 + 12764,                    # Leituras.RendimentoGerador_UG03
    "RENDIMENTO_GERADOR_UG04":                  226 + 12764,                    # Leituras.RendimentoGerador_UG04

    # Vazão
    "VAZAO_TURBINADA_UG01":                     208 + 12764,                    # Leituras.VazaoTurbinada_UG01
    "VAZAO_TURBINADA_UG02":                     209 + 12764,                    # Leituras.VazaoTurbinada_UG02
    "VAZAO_TURBINADA_UG03":                     210 + 12764,                    # Leituras.VazaoTurbinada_UG03
    "VAZAO_TURBINADA_UG04":                     211 + 12764,                    # Leituras.VazaoTurbinada_UG04
    "VAZAO_TURBINADA":                          212 + 12764,                    # Leituras.VazaoTurbinada
    "VAZAO_RIO":                                213 + 12764,                    # Leituras.VazaoRio
    "VAZAO_VERTEDOR":                           214 + 12764,                    # Leituras.VazaoVertedor
    "VAZAO_ADUFA_01":                           215 + 12764,                    # Leituras.VazaoAdufa01
    "VAZAO_ADUFA_02":                           216 + 12764,                    # Leituras.VazaoAdufa02
    "VAZAO_EFLUENTE":                           217 + 12764,                    # Leituras.VazaoEfluente


    ## ALARMES
    "Alarme01_02":                              [1 + 14089, 2],
    "Alarme01_03":                              [1 + 14089, 3],
    "Alarme01_07":                              [1 + 14089, 7],
    "Alarme01_08":                              [1 + 14089, 8],
    "Alarme01_09":                              [1 + 14089, 9],
    "Alarme01_10":                              [1 + 14089, 10],
    "Alarme01_11":                              [1 + 14089, 11],
    "Alarme01_15":                              [1 + 14089, 15],

    "Alarme02_03":                              [2 + 14089, 3],
    "Alarme02_06":                              [2 + 14089, 6],
    "Alarme02_09":                              [2 + 14089, 9],
    "Alarme02_10":                              [2 + 14089, 10],
    "Alarme02_14":                              [2 + 14089, 14],
    "Alarme02_15":                              [2 + 14089, 15],

    "Alarme03_09":                              [3 + 14089, 9],
    "Alarme03_10":                              [3 + 14089, 10],
    "Alarme03_11":                              [3 + 14089, 11],
    "Alarme03_12":                              [3 + 14089, 12],
    "Alarme03_13":                              [3 + 14089, 13],
    "Alarme03_14":                              [3 + 14089, 14],
    "Alarme03_15":                              [3 + 14089, 15],

    "Alarme04_00":                              [4 + 14089, 0],
    "Alarme04_01":                              [4 + 14089, 1],
    "Alarme04_02":                              [4 + 14089, 2],
    "Alarme04_03":                              [4 + 14089, 3],
    "Alarme04_04":                              [4 + 14089, 4],
    "Alarme04_05":                              [4 + 14089, 5],
    "Alarme04_06":                              [4 + 14089, 6],
    "Alarme04_07":                              [4 + 14089, 7],
    "Alarme04_08":                              [4 + 14089, 8],
    "Alarme04_09":                              [4 + 14089, 9],

    "Alarme05_00":                              [5 + 14089, 0],
    "Alarme05_01":                              [5 + 14089, 1],
    "Alarme05_15":                              [5 + 14089, 15],

    "Alarme06_00":                              [6 + 14089, 0],
    "Alarme06_01":                              [6 + 14089, 1],
    "Alarme06_02":                              [6 + 14089, 2],
    "Alarme06_03":                              [6 + 14089, 3],
    "Alarme06_04":                              [6 + 14089, 4],
    "Alarme06_05":                              [6 + 14089, 5],
    "Alarme06_06":                              [6 + 14089, 6],
    "Alarme06_07":                              [6 + 14089, 7],
    "Alarme06_08":                              [6 + 14089, 8],
    "Alarme06_09":                              [6 + 14089, 9],
    "Alarme06_11":                              [6 + 14089, 11],
    "Alarme06_12":                              [6 + 14089, 12],
    "Alarme06_13":                              [6 + 14089, 13],
    "Alarme06_14":                              [6 + 14089, 14],

    "Alarme07_01":                              [7 + 14089, 1],
    "Alarme07_02":                              [7 + 14089, 2],
    "Alarme07_03":                              [7 + 14089, 3],
    "Alarme07_04":                              [7 + 14089, 4],
    "Alarme07_05":                              [7 + 14089, 5],
    "Alarme07_06":                              [7 + 14089, 6],
    "Alarme07_07":                              [7 + 14089, 7],
    "Alarme07_11":                              [7 + 14089, 11],
    "Alarme07_12":                              [7 + 14089, 12],
    "Alarme07_13":                              [7 + 14089, 13],
    "Alarme07_14":                              [7 + 14089, 14],
    "Alarme07_15":                              [7 + 14089, 15],

    "Alarme08_00":                              [8 + 14089, 0],
    "Alarme08_01":                              [8 + 14089, 1],
    "Alarme08_02":                              [8 + 14089, 2],
    "Alarme08_03":                              [8 + 14089, 3],
    "Alarme08_04":                              [8 + 14089, 4],
    "Alarme08_05":                              [8 + 14089, 5],
    "Alarme08_06":                              [8 + 14089, 6],
    "Alarme08_07":                              [8 + 14089, 7],
    "Alarme08_08":                              [8 + 14089, 8],
    "Alarme08_09":                              [8 + 14089, 9],
    "Alarme08_10":                              [8 + 14089, 10],
    "Alarme08_11":                              [8 + 14089, 11],
    "Alarme08_12":                              [8 + 14089, 12],
    "Alarme08_13":                              [8 + 14089, 13],
    "Alarme08_14":                              [8 + 14089, 14],

    "Alarme09_00":                              [9 + 14089, 0],
    "Alarme09_01":                              [9 + 14089, 1],
    "Alarme09_02":                              [9 + 14089, 2],
    "Alarme09_03":                              [9 + 14089, 3],
    "Alarme09_04":                              [9 + 14089, 4],
    "Alarme09_09":                              [9 + 14089, 9],
    "Alarme09_10":                              [9 + 14089, 10],
    "Alarme09_11":                              [9 + 14089, 11],
    "Alarme09_12":                              [9 + 14089, 12],

    "Alarme10_00":                              [10 + 14089, 0],
    "Alarme10_01":                              [10 + 14089, 1],
    "Alarme10_02":                              [10 + 14089, 2],
    "Alarme10_03":                              [10 + 14089, 3],
    "Alarme10_04":                              [10 + 14089, 4],
    "Alarme10_05":                              [10 + 14089, 5],
    "Alarme10_06":                              [10 + 14089, 6],
    "Alarme10_07":                              [10 + 14089, 7],

    "Alarme11_00":                              [11 + 14089, 0],
    "Alarme11_01":                              [11 + 14089, 1],
    "Alarme11_02":                              [11 + 14089, 2],
    "Alarme11_03":                              [11 + 14089, 3],
    "Alarme11_04":                              [11 + 14089, 4],
    "Alarme11_05":                              [11 + 14089, 5],
    "Alarme11_06":                              [11 + 14089, 6],
    "Alarme11_07":                              [11 + 14089, 7],
    "Alarme11_08":                              [11 + 14089, 8],
    "Alarme11_09":                              [11 + 14089, 9],
    "Alarme11_10":                              [11 + 14089, 10],
    "Alarme11_11":                              [11 + 14089, 11],
    "Alarme11_12":                              [11 + 14089, 12],
    "Alarme11_13":                              [11 + 14089, 13],
    "Alarme11_14":                              [11 + 14089, 14],
    "Alarme11_15":                              [11 + 14089, 15],

    "Alarme12_00":                              [12 + 14089, 0],
    "Alarme12_04":                              [12 + 14089, 4],
    "Alarme12_05":                              [12 + 14089, 5],
    "Alarme12_06":                              [12 + 14089, 6],

    "Alarme14_03":                              [14 + 14089, 3],
    "Alarme14_04":                              [14 + 14089, 4],
    "Alarme14_05":                              [14 + 14089, 5],
    "Alarme14_06":                              [14 + 14089, 6],
    "Alarme14_08":                              [14 + 14089, 8],
    "Alarme14_09":                              [14 + 14089, 9],
    "Alarme14_10":                              [14 + 14089, 10],
    "Alarme14_11":                              [14 + 14089, 11],
    "Alarme14_12":                              [14 + 14089, 12],
    "Alarme14_13":                              [14 + 14089, 13],
    "Alarme14_14":                              [14 + 14089, 14],
    "Alarme14_15":                              [14 + 14089, 15],

    "Alarme15_00":                              [15 + 14089, 0],
    "Alarme15_01":                              [15 + 14089, 1],
    "Alarme15_02":                              [15 + 14089, 2],
    "Alarme15_03":                              [15 + 14089, 3],
    "Alarme15_04":                              [15 + 14089, 4],
    "Alarme15_05":                              [15 + 14089, 5],
    "Alarme15_06":                              [15 + 14089, 6],
    "Alarme15_07":                              [15 + 14089, 7],
    "Alarme15_08":                              [15 + 14089, 8],
    "Alarme15_09":                              [15 + 14089, 9],
    "Alarme15_10":                              [15 + 14089, 10],
    "Alarme15_11":                              [15 + 14089, 11],

    "Alarme16_10":                              [16 + 14089, 10],
    "Alarme16_11":                              [16 + 14089, 11],
    "Alarme16_12":                              [16 + 14089, 12],
    "Alarme16_13":                              [16 + 14089, 13],
    "Alarme16_14":                              [16 + 14089, 14],
    "Alarme16_15":                              [16 + 14089, 15],

    "Alarme17_00":                              [17 + 14089, 0],
    "Alarme17_01":                              [17 + 14089, 1],
    "Alarme17_02":                              [17 + 14089, 2],
    "Alarme17_03":                              [17 + 14089, 3],
    "Alarme17_04":                              [17 + 14089, 4],
    "Alarme17_05":                              [17 + 14089, 5],
    "Alarme17_06":                              [17 + 14089, 6],
    "Alarme17_07":                              [17 + 14089, 7],
    "Alarme17_09":                              [17 + 14089, 9],
    "Alarme17_10":                              [17 + 14089, 10],
    "Alarme17_11":                              [17 + 14089, 11],
    "Alarme17_12":                              [17 + 14089, 12],
    "Alarme17_13":                              [17 + 14089, 13],
    "Alarme17_14":                              [17 + 14089, 14],

    "Alarme18_00":                              [18 + 14089, 0],
    "Alarme18_01":                              [18 + 14089, 1],
    "Alarme18_03":                              [18 + 14089, 3],
    "Alarme18_06":                              [18 + 14089, 6],
    "Alarme18_07":                              [18 + 14089, 7],
    "Alarme18_08":                              [18 + 14089, 8],
    "Alarme18_09":                              [18 + 14089, 9],
    "Alarme18_10":                              [18 + 14089, 10],
    "Alarme18_11":                              [18 + 14089, 11],
    "Alarme18_12":                              [18 + 14089, 12],

    "Alarme19_06":                              [19 + 14089, 6],
    "Alarme19_07":                              [19 + 14089, 7],
    "Alarme19_08":                              [19 + 14089, 8],
    "Alarme19_09":                              [19 + 14089, 9],
    "Alarme19_10":                              [19 + 14089, 10],
    "Alarme19_11":                              [19 + 14089, 11],
    "Alarme19_12":                              [19 + 14089, 12],
    "Alarme19_13":                              [19 + 14089, 13],
    "Alarme19_14":                              [19 + 14089, 14],

    "Alarme20_06":                              [20 + 14089, 6],
    "Alarme20_07":                              [20 + 14089, 7],
    "Alarme20_08":                              [20 + 14089, 8],
    "Alarme20_09":                              [20 + 14089, 9],
    "Alarme20_10":                              [20 + 14089, 10],
    "Alarme20_11":                              [20 + 14089, 11],
    "Alarme20_12":                              [20 + 14089, 12],
    "Alarme20_13":                              [20 + 14089, 13],
    "Alarme20_14":                              [20 + 14089, 14],

    "Alarme21_02":                              [21 + 14089, 2],
    "Alarme21_03":                              [21 + 14089, 3],
    "Alarme21_06":                              [21 + 14089, 6],
    "Alarme21_07":                              [21 + 14089, 7],
    "Alarme21_08":                              [21 + 14089, 8],
    "Alarme21_09":                              [21 + 14089, 9],
    "Alarme21_10":                              [21 + 14089, 10],
    "Alarme21_11":                              [21 + 14089, 11],
    "Alarme21_12":                              [21 + 14089, 12],
}


REG_SE = {
    ## COMANDOS
    # Dj52L
    "CMD_ABRIR_DJ52L":                          4 + 12289,                      # Comandos.Disj52LAbrir
    "CMD_FECHAR_DJ52L":                         5 + 12289,                      # Comandos.Disj52LFechar

    # Secc89L
    "CMD_SECC89L_ABRIR":                        35 + 12289,                     # Comandos.Secc89L_Abrir
    "CMD_SECC89L_FECHAR":                       36 + 12289,                     # Comandos.Secc89L_Fechar

    # Cargas Não Essenciais
    "CMD_CARGANAOESSEN_FECHAR":                 37 + 12289,                     # Comandos.CargaNaoEssencial_Fechar
    "CMD_CARGANAOESSEN_ABRIR":                  38 + 12289,                     # Comandos.CargaNaoEssencial_Abrir


    ## LEITURAS
    # Disjuntores
    "STATUS_DJ52L":                             21 + 12764,                     # Leituras.Subestacao_Disj52L
    "DJ52L_ABERTO":                             [21 + 12764, 0],                # Disj52L.Info.Aberto
    "DJ52L_FECHADO":                            [21 + 12764, 1],                # Disj52L.Info.Fechado
    "DJ52L_INCONSISTENTE":                      [21 + 12764, 2],                # Disj52L.Info.Inconsistente
    "DJ52L_TRIP":                               [21 + 12764, 3],                # Disj52L.Info.Trip
    "DJ52L_MODO_LOCAL":                         [21 + 12764, 4],                # Disj52L.Info.ModoLocal
    "DJ52L_MODO_REMOTO":                        [21 + 12764, 5],                # Disj52L.Info.ModoRemoto
    "DJ52L_MOLA_CARREGADA":                     [21 + 12764, 6],                # Disj52L.Info.MolaCarregada
    "DJ52L_ALIM125VCC_MOTOR":                   [21 + 12764, 7],                # Disj52L.Info.Alim125Vcc_motor
    "DJ52L_FALTA_VCC":                          [21 + 12764, 8],                # Disj52L.Info.FaltaVcc
    "DJ52L_COND_FECHAMENTO":                    [21 + 12764, 9],                # Disj52L.Info.CondFechamento
    "DJ52L_GAS_SF6_1":                          [21 + 12764, 10],               # Disj52L.Info.GasSF6_1
    "DJ52L_GAS_SF6_2":                          [21 + 12764, 11],               # Disj52L.Info.GasSF6_2
    "DJ52L_FALHA_ABERTURA":                     [21 + 12764, 12],               # Disj52L.Info.FalhaAbertura
    "DJ52L_FALHA_FECHAMENTO":                   [21 + 12764, 13],               # Disj52L.Info.FalhaFechamento

    "STATUS_SECCIONADORAS":                     22 + 12764,                     # Leituras.Subestacao_Seccionadoras
    "SECC_89L_ABERTA":                          [22 + 12764, 0],                # Seccionadoras.Info.[89L_Aberta]
    "SECC_89L_FECHADA":                         [22 + 12764, 1],                # Seccionadoras.Info.[89L_Fechada]
    "SECC_89L_CONDICAO":                        [22 + 12764, 2],                # Seccionadoras.Info.[89L_CondicaoFechamento]
    "SECC_MODO_LOCAL":                          [22 + 12764, 3],                # Seccionadoras.Info.Local
    "SECC_LAMINA_FECHADA":                      [22 + 12764, 4],                # Seccionadoras.Info.LaminaFechada
    "SECC_ALIM_VCC_CMD":                        [22 + 12764, 5],                # Seccionadoras.Info.AlimVccComando
    "SECC_ALIM_VCC_BLOQ":                       [22 + 12764, 6],                # Seccionadoras.Info.AlimVccBloqueio

    # Tensão
    "TENSAO_RN":                                23 + 12764,                     # Leituras.Subestacao_TensaoRN
    "TENSAO_SN":                                24 + 12764,                     # Leituras.Subestacao_TensaoSN
    "TENSAO_TN":                                25 + 12764,                     # Leituras.Subestacao_TensaoTN
    "TENSAO_RS":                                26 + 12764,                     # Leituras.Subestacao_TensaoRS
    "TENSAO_ST":                                27 + 12764,                     # Leituras.Subestacao_TensaoST
    "TENSAO_TR":                                28 + 12764,                     # Leituras.Subestacao_TensaoTR
    "TENSAO_SINCRONISMO":                       63 + 12764,                     # Leituras.Subestacao_TensaoSincronismo
    "TENSAO_VCC":                               64 + 12764,                     # Leituras.Subestacao_TensaoVCC

    "FP_INFO":                                  65 + 12764,                     # Leituras.ServAux_FPInfo
    "FP_INDUTIVO_FASE1":                        [65 + 12764, 0],                # MedidorSubestacao.FP_Info.IndutivoFase1
    "FP_CAPACITIVO_FASE1":                      [65 + 12764, 1],                # MedidorSubestacao.FP_Info.CapacitivoFase1
    "FP_INDUTIVO_FASE2":                        [65 + 12764, 2],                # MedidorSubestacao.FP_Info.IndutivoFase2
    "FP_CAPACITIVO_FASE2":                      [65 + 12764, 3],                # MedidorSubestacao.FP_Info.CapacitivoFase2
    "FP_INDUTIVO_FASE3":                        [65 + 12764, 4],                # MedidorSubestacao.FP_Info.IndutivoFase3
    "FP_CAPACITIVO_FASE3":                      [65 + 12764, 5],                # MedidorSubestacao.FP_Info.CapacitivoFase3
    "FP_INDUTIVO_TOTAL":                        [65 + 12764, 6],                # MedidorSubestacao.FP_Info.IndutivoTotal
    "FP_CAPACITIVO_TOTAL":                      [65 + 12764, 7],                # MedidorSubestacao.FP_Info.CapacitivoTotal

    # Corrente
    "CORRENTE_R":                               29 + 12764,                     # Leituras.Subestacao_CorrenteR
    "CORRENTE_S":                               30 + 12764,                     # Leituras.Subestacao_CorrenteS
    "CORRENTE_T":                               31 + 12764,                     # Leituras.Subestacao_CorrenteT
    "CORRENTE_MEDIA":                           32 + 12764,                     # Leituras.Subestacao_CorrenteMedia
    "CORRENTE_NEUTRO":                          62 + 12764,                     # Leituras.Subestacao_CorrenteNeutro

    # Potência
    "POTENCIA_ATIVA_1":                         33 + 12764,                     # Leituras.Subestacao_PotenciaAtiva1
    "POTENCIA_ATIVA_2":                         34 + 12764,                     # Leituras.Subestacao_PotenciaAtiva2
    "POTENCIA_ATIVA_3":                         35 + 12764,                     # Leituras.Subestacao_PotenciaAtiva3
    "POTENCIA_ATIVA_MEDIA":                     36 + 12764,                     # Leituras.Subestacao_PotenciaAtivaMedia
    "POTENCIA_REATIVA_1":                       37 + 12764,                     # Leituras.Subestacao_PotenciaReativa1
    "POTENCIA_REATIVA_2":                       38 + 12764,                     # Leituras.Subestacao_PotenciaReativa2
    "POTENCIA_REATIVA_3":                       39 + 12764,                     # Leituras.Subestacao_PotenciaReativa3
    "POTENCIA_REATIVA_MEDIA":                   40 + 12764,                     # Leituras.Subestacao_PotenciaReativaMedia
    "POTENCIA_APARENTE_1":                      41 + 12764,                     # Leituras.Subestacao_PotenciaAparente1
    "POTENCIA_APARENTE_2":                      42 + 12764,                     # Leituras.Subestacao_PotenciaAparente2
    "POTENCIA_APARENTE_3":                      43 + 12764,                     # Leituras.Subestacao_PotenciaAparente3
    "POTENCIA_APARENTE_MEDIA":                  44 + 12764,                     # Leituras.Subestacao_PotenciaAparenteMedia

    # Fator Potência
    "FATOR_POTENCIA_1":                         45 + 12764,                     # Leituras.Subestacao_FatorPotencia1
    "FATOR_POTENCIA_2":                         46 + 12764,                     # Leituras.Subestacao_FatorPotencia2
    "FATOR_POTENCIA_3":                         47 + 12764,                     # Leituras.Subestacao_FatorPotencia3
    "FATOR_POTENCIA_MEDIA":                     48 + 12764,                     # Leituras.Subestacao_FatorPotenciaMedia

    # Frequência
    "FREQUENCIA":                               49 + 12764,                     # Leituras.Subestacao_Frequencia

    # Energia Forncida
    "ENERGIA_FORNECIDA_TWh":                    50 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaTWh
    "ENERGIA_FORNECIDA_GWh":                    51 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaGWh
    "ENERGIA_FORNECIDA_MWh":                    52 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaMWh
    "ENERGIA_FORNECIDA_KWh":                    53 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaKWh
    "ENERGIA_FORNECIDA_TVArh":                  54 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaTVArh
    "ENERGIA_FORNECIDA_GVArh":                  55 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaGVArh
    "ENERGIA_FORNECIDA_MVArh":                  56 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaMVArh
    "ENERGIA_FORNECIDA_KVArh":                  57 + 12764,                     # Leituras.Subestacao_EnergiaFornecidaKVArh
    "ENERGIA_FORNECIDA_TVArh":                  58 + 12764,                     # Leituras.Subestacao_EnergiaConsumidaTVArh
    "ENERGIA_FORNECIDA_GVArh":                  59 + 12764,                     # Leituras.Subestacao_EnergiaConsumidaGVArh
    "ENERGIA_FORNECIDA_MVArh":                  60 + 12764,                     # Leituras.Subestacao_EnergiaConsumidaMVArh
    "ENERGIA_FORNECIDA_KVArh":                  61 + 12764,                     # Leituras.Subestacao_EnergiaConsumidaKVArh

    ## DISJUNTORES
    "DJ_01":                                    0,
    "DJ_02":                                    1,
    "DJ_03":                                    2,
    "DJ_04":                                    3,
    "DJ_05":                                    4,
    "DJ_06":                                    5,
    "DJ_07":                                    6,
    "DJ_08":                                    7,
    "DJ_09":                                    8,
    "DJ_10":                                    9,
    "DJ_11":                                    10,
    "DJ_12":                                    11,
    "DJ_13":                                    12,
    "DJ_14":                                    13,
    "DJ_15":                                    14,
    "DJ_16":                                    15,
    "DJ_17":                                    16,
    "DJ_18":                                    17,
    "DJ_19":                                    18,
    "DJ_20":                                    19,
    "DJ_21":                                    20,
    "DJ_22":                                    21,
    "DJ_23":                                    22,
    "DJ_24":                                    23,
    "DJ_25":                                    24,
    "DJ_26":                                    25,
    "DJ_27":                                    26,
    "DJ_28":                                    27,
    "DJ_29":                                    28,
    "DJ_30":                                    29,
    "DJ_31":                                    30,
    "DJ_32":                                    31,
    "DJ_33":                                    32,
    "DJ_34":                                    33,
    "DJ_35":                                    34,
    "DJ_36":                                    35,
    "DJ_37":                                    36,
    "DJ_38":                                    37,
    "DJ_39":                                    38,
    "DJ_40":                                    39,
    "DJ_41":                                    40,
    "DJ_42":                                    41,
    "DJ_43":                                    42,
    "DJ_44":                                    43,
    "DJ_45":                                    44,
    "DJ_46":                                    45,
    "DJ_47":                                    46,
    "DJ_48":                                    47,
    "DJ_49":                                    48,
    "DJ_50":                                    49,
    "DJ_51":                                    50,
    "DJ_52":                                    51,
    "DJ_53":                                    52,
    "DJ_54":                                    53,
    "DJ_55":                                    54,
    "DJ_56":                                    55,
    "DJ_57":                                    56,
    "DJ_58":                                    57,
    "DJ_59":                                    58,
    "DJ_60":                                    59,
    "DJ_61":                                    60,
    "DJ_62":                                    61,
    "DJ_63":                                    62,
    "DJ_64":                                    63,
    "DJ_65":                                    64,
    "DJ_66":                                    65,
    "DJ_67":                                    66,
    "DJ_68":                                    67,
    "DJ_69":                                    68,
    "DJ_70":                                    69,
    "DJ_71":                                    70,
    "DJ_72":                                    71,
    "DJ_73":                                    72,
    "DJ_74":                                    73,
    "DJ_75":                                    74,
    "DJ_76":                                    75,
    "DJ_77":                                    76,
    "DJ_78":                                    77,
    "DJ_79":                                    78,
    "DJ_80":                                    79,
    "DJ_81":                                    80,
    "DJ_82":                                    81,
    "DJ_83":                                    82,
    "DJ_84":                                    83,
    "DJ_85":                                    84,
    "DJ_86":                                    85,
    "DJ_87":                                    86,
    "DJ_88":                                    87,
    "DJ_89":                                    88,
    "DJ_90":                                    89,
    "DJ_91":                                    90,
    "DJ_92":                                    91,
    "DJ_93":                                    92,
    "DJ_94":                                    93,
    "DJ_95":                                    94,
    "DJ_96":                                    95,
    "DJ_97":                                    96,


    ## ALARMES

    "Alarme01_00":                              [1 + 14089, 0],
    "Alarme01_01":                              [1 + 14089, 1],
    "Alarme01_12":                              [1 + 14089, 12],
    "Alarme01_13":                              [1 + 14089, 13],
    "Alarme01_14":                              [1 + 14089, 14],

    "Alarme02_00":                              [2 + 14089, 0],
    "Alarme02_01":                              [2 + 14089, 1],
    "Alarme02_02":                              [2 + 14089, 2],
    "Alarme02_04":                              [2 + 14089, 4],
    "Alarme02_05":                              [2 + 14089, 5],
    "Alarme02_07":                              [2 + 14089, 7],
    "Alarme02_08":                              [2 + 14089, 8],
    "Alarme02_11":                              [2 + 14089, 11],
    "Alarme02_12":                              [2 + 14089, 12],
    "Alarme02_13":                              [2 + 14089, 13],

    "Alarme03_00":                              [3 + 14089, 0],
    "Alarme03_01":                              [3 + 14089, 1],
    "Alarme03_02":                              [3 + 14089, 2],
    "Alarme03_03":                              [3 + 14089, 3],
    "Alarme03_04":                              [3 + 14089, 4],
    "Alarme03_05":                              [3 + 14089, 5],
    "Alarme03_06":                              [3 + 14089, 6],
    "Alarme03_07":                              [3 + 14089, 7],
    "Alarme03_08":                              [3 + 14089, 8],

    "Alarme05_02":                              [5 + 14089, 2],
    "Alarme05_03":                              [5 + 14089, 3],
    "Alarme05_04":                              [5 + 14089, 4],
    "Alarme05_05":                              [5 + 14089, 5],
    "Alarme05_06":                              [5 + 14089, 6],
    "Alarme05_07":                              [5 + 14089, 7],
    "Alarme05_08":                              [5 + 14089, 8],
    "Alarme05_09":                              [5 + 14089, 9],
    "Alarme05_10":                              [5 + 14089, 10],
    "Alarme05_11":                              [5 + 14089, 11],
    "Alarme05_12":                              [5 + 14089, 12],
    "Alarme05_13":                              [5 + 14089, 13],
    "Alarme05_14":                              [5 + 14089, 14],

    "Alarme09_07":                              [9 + 14089, 7],
    "Alarme09_08":                              [9 + 14089, 8],

    "Alarme12_03":                              [12 + 14089, 3],

    "Alarme14_07":                              [14 + 14089, 7],

    "Alarme16_04":                              [16 + 14089, 4],
    "Alarme16_05":                              [16 + 14089, 5],
    "Alarme16_06":                              [16 + 14089, 6],
    "Alarme16_07":                              [16 + 14089, 7],
    "Alarme16_08":                              [16 + 14089, 8],
    "Alarme16_09":                              [16 + 14089, 9],

    "Alarme18_04":                              [18 + 14089, 4],
    "Alarme18_05":                              [18 + 14089, 5],
    "Alarme18_13":                              [18 + 14089, 13],
    "Alarme18_14":                              [18 + 14089, 14],
    "Alarme18_15":                              [18 + 14089, 15],

    "Alarme19_00":                              [19 + 14089, 0],
    "Alarme19_01":                              [19 + 14089, 1],
    "Alarme19_02":                              [19 + 14089, 2],
    "Alarme19_03":                              [19 + 14089, 3],
    "Alarme19_04":                              [19 + 14089, 4],
    "Alarme19_05":                              [19 + 14089, 5],
    "Alarme19_15":                              [19 + 14089, 15],

    "Alarme20_00":                              [20 + 14089, 0],
    "Alarme20_01":                              [20 + 14089, 1],
    "Alarme20_02":                              [20 + 14089, 2],
    "Alarme20_03":                              [20 + 14089, 3],
    "Alarme20_04":                              [20 + 14089, 4],
    "Alarme20_05":                              [20 + 14089, 5],
    "Alarme20_15":                              [20 + 14089, 15],

    "Alarme21_00":                              [21 + 14089, 0],
    "Alarme21_01":                              [21 + 14089, 1],
}


REG_TDA = {
    ## COMANDOS
    # UHTA
    "CMD_UHTA01_RODIZIO_AUTOMATICO":            39 + 12289,                     # Comandos.PCTA_UHTA01_RodizioAutomatico
    "CMD_UHTA01_RODIZIO_MANUAL":                40 + 12289,                     # Comandos.PCTA_UHTA01_RodizioManual
    "CMD_UHTA02_RODIZIO_AUTOMATICO":            41 + 12289,                     # Comandos.PCTA_UHTA02_RodizioAutomatico
    "CMD_UHTA02_RODIZIO_MANUAL":                42 + 12289,                     # Comandos.PCTA_UHTA02_RodizioManual
    "CMD_UHTA01_BOMBA_01_LIGAR":                43 + 12289,                     # Comandos.PCTA_UHTA01_Bomba01Ligar
    "CMD_UHTA01_BOMBA_01_DESLIGAR":             44 + 12289,                     # Comandos.PCTA_UHTA01_Bomba01Desligar
    "CMD_UHTA01_BOMBA_01_PRINCIPAL":            45 + 12289,                     # Comandos.PCTA_UHTA01_Bomba01Principal
    "CMD_UHTA01_BOMBA_02_LIGAR":                46 + 12289,                     # Comandos.PCTA_UHTA01_Bomba02Ligar
    "CMD_UHTA01_BOMBA_02_DESLIGAR":             47 + 12289,                     # Comandos.PCTA_UHTA01_Bomba02Desligar
    "CMD_UHTA01_BOMBA_02_PRINCIPAL":            48 + 12289,                     # Comandos.PCTA_UHTA01_Bomba02Principal
    "CMD_UHTA02_BOMBA_01_LIGAR":                49 + 12289,                     # Comandos.PCTA_UHTA02_Bomba01Ligar
    "CMD_UHTA02_BOMBA_01_DESLIGAR":             50 + 12289,                     # Comandos.PCTA_UHTA02_Bomba01Desligar
    "CMD_UHTA02_BOMBA_01_PRINCIPAL":            51 + 12289,                     # Comandos.PCTA_UHTA02_Bomba01Principal
    "CMD_UHTA02_BOMBA_02_LIGAR":                52 + 12289,                     # Comandos.PCTA_UHTA02_Bomba02Ligar
    "CMD_UHTA02_BOMBA_02_DESLIGAR":             53 + 12289,                     # Comandos.PCTA_UHTA02_Bomba02Desligar
    "CMD_UHTA02_BOMBA_02_PRINCIPAL":            54 + 12289,                     # Comandos.PCTA_UHTA02_Bomba02Principal

    # Sensores
    "CMD_SENSOR_PRESEN_INIBIR":                 55 + 12289,                     # Comandos.PCTA_SensorPresencaInibir
    "CMD_SENSOR_PRESEN_DESINIBIR":              56 + 12289,                     # Comandos.PCTA_SensorPresencaDesinibir


    ## SETPOINTS
    # Níveis
    "NV_BARRAGEM_HH":                           0 + 13569,                      # Setpoints.Usina_NivelBarragem_HH
    "NV_BARRAGEM_LL":                           1 + 13569,                      # Setpoints.Usina_NivelBarragem_LL
    "NV_BARRAGEM_TOLERANCIA":                   2 + 13569,                      # Setpoints.Usina_NivelBarragem_Tolerancia
    "NV_CAMARA_CARGA_HH":                       3 + 13569,                      # Setpoints.Usina_NiveCamaraCarga_HH
    "NV_CAMARA_CARGA_LL":                       4 + 13569,                      # Setpoints.Usina_NiveCamaraCarga_LL
    "NV_CAMARA_CARGA_TOLERANCIA":               5 + 13569,                      # Setpoints.Usina_NiveCamaraCarga_Tolerancia

    # Grade
    "GRADE_SUJA_DIF_ALARME":                    6 + 13569,                      # Setpoints.Usina_GradeSujaDiferencial_Alarme
    "GRADE_SUJA_DIF_TRIP":                      7 + 13569,                      # Setpoints.Usina_GradeSujaDiferencial_TRIP

    # Manobras UHTA
    "UHTA01_MANO_RODIZIO_LIDER":                10 + 13569,                     # Setpoints.PCTA_UHTA01_ManobrasRodizioLider
    "UHTA01_MANO_RODIZIO_RETAGUARDA":           11 + 13569,                     # Setpoints.PCTA_UHTA01_ManobrasRodizioRetaguarda
    "UHTA02_MANO_RODIZIO_LIDER":                12 + 13569,                     # Setpoints.PCTA_UHTA02_ManobrasRodizioLider
    "UHTA02_MANO_RODIZIO_RETAGUARDA":           13 + 13569,                     # Setpoints.PCTA_UHTA02_ManobrasRodizioRetaguarda

    # Diferencial de Grade
    "DIFERENCIAL_GRADE_01":                     22 + 13569,                     # Setpoints.DiferenciaGrade01
    "DIFERENCIAL_GRADE_02":                     23 + 13569,                     # Setpoints.DiferenciaGrade02
    "DIFERENCIAL_GRADE_03":                     24 + 13569,                     # Setpoints.DiferenciaGrade03
    "DIFERENCIAL_GRADE_04":                     25 + 13569,                     # Setpoints.DiferenciaGrade04


    ## LEITURAS
    # Níveis
    "NV_JUSANTE":                               2 + 12764,                      # Leituras.NivelJusante
    "NV_BARRAGEM":                              3 + 12764,                      # Leituras.NivelBarragem
    "NV_CANALADUCAO":                           4 + 12764,                      # Leituras.NivelCanalAducao
    "NV_CAMARACARGA":                           5 + 12764,                      # Leituras.NivelCamaraCarga
    "NV_POS_GRADE_01":                          227 + 12764,                    # Leituras.NivelPosGrade01
    "NV_POS_GRADE_02":                          228 + 12764,                    # Leituras.NivelPosGrade02
    "NV_POS_GRADE_03":                          229 + 12764,                    # Leituras.NivelPosGrade03
    "NV_POS_GRADE_04":                          230 + 12764,                    # Leituras.NivelPosGrade04

    # Pluviometro
    "PLUVIOMETRO":                              9 + 12764,                      # Leituras.Pluviometro

    # PCTA
    "COMPORTA_01_INFO":                         127 + 12764,                    # Leituras.PCTA_Comporta01_Info
    "COMPORTA_01_TEMPO_EFETIVO_EQUAL":          128 + 12764,                    # Leituras.PCTA_Comporta01TempoEfetivoEqualizacao
    "COMPORTA_01_POSICAO":                      129 + 12764,                    # Leituras.PCTA_Comporta01Posicao
    "COMPORTA_02_INFO":                         130 + 12764,                    # Leituras.PCTA_Comporta02_Info
    "COMPORTA_02_TEMPO_EFETIVO_EQUAL":          131 + 12764,                    # Leituras.PCTA_Comporta02TempoEfetivoEqualizacao
    "COMPORTA_02_POSICAO":                      132 + 12764,                    # Leituras.PCTA_Comporta02Posicao
    "COMPORTA_03_INFO":                         133 + 12764,                    # Leituras.PCTA_Comporta03_Info
    "COMPORTA_03_TEMPO_EFETIVO_EQUAL":          134 + 12764,                    # Leituras.PCTA_Comporta03TempoEfetivoEqualizacao
    "COMPORTA_03_POSICAO":                      135 + 12764,                    # Leituras.PCTA_Comporta03Posicao
    "COMPORTA_04_INFO":                         136 + 12764,                    # Leituras.PCTA_Comporta04_Info
    "COMPORTA_04_TEMPO_EFETIVO_EQUAL":          137 + 12764,                    # Leituras.PCTA_Comporta04TempoEfetivoEqualizacao
    "COMPORTA_04_POSICAO":                      138 + 12764,                    # Leituras.PCTA_Comporta04Posicao

    # UHTA
    "UHTA01_INFO":                              139 + 12764,                    # Leituras.PCTA_UHTA01_Info
    "UHTA01_OPERACIONAL":                       [139 + 12764, 0],               # PCTA.UHTA01.Info.Operacional
    "UHTA01_LIGADA":                            [139 + 12764, 1],               # PCTA.UHTA01.Info.Ligada

    "UHTA01_BOMBAS":                            140 + 12764,                    # Leituras.PCTA_UHTA01_Bombas
    "UHTA01_BOMBAS01":                          [140 + 12764, 0],               # PCTA.UHTA01.Bombas.[01]
    "UHTA01_BOMBAS02":                          [140 + 12764, 1],               # PCTA.UHTA01.Bombas.[02]

    "UHTA01_RODIZIO":                           141 + 12764,                    # Leituras.PCTA_UHTA01_Rodizio
    "UHTA01_RODIZ_BOMBA01":                     [141 + 12764, 0],               # PCTA.UHTA01.Rodizio.Bomba01
    "UHTA01_RODIZ_BOMBA02":                     [141 + 12764, 1],               # PCTA.UHTA01.Rodizio.Bomba02
    "UHTA01_RODIZ_HABILITADO":                  [141 + 12764, 2],               # PCTA.UHTA01.Rodizio.Habilitado

    "UHTA01_ACUMULADOR":                        142 + 12764,                    # Leituras.PCTA_UHTA01_Acumulador
    "UHTA01_ACUM_BOMBA_LIDER":                  [142 + 12764, 0],               # PCTA.UHTA01.AcumuladorBombaLider
    "UHTA01_ACUM_BOMBA_RETAGUARDA":             [143 + 12764, 1],               # PCTA.UHTA01.AcumuladorBombaRetaguarda

    "UHTA01_FILTROS":                           144 + 12764,                    # Leituras.PCTA_UHTA01_Filtros
    "UHTA01_FILTROS01":                         [144 + 12764, 0],               # PCTA.UHTA01.Filtros.[01]

    "UHTA01_NIVEL_OLEO_INFO":                   145 + 12764,                    # Leituras.PCTA_UHTA01_NivelOleo_Info
    "UHTA01_NIVEL_OLEO_LL":                     [145 + 12764, 0],               # PCTA.UHTA01.NivelOleo_Info.LL
    "UHTA01_NIVEL_OLEO_HH":                     [145 + 12764, 1],               # PCTA.UHTA01.NivelOleo_Info.HH

    "UHTA01_TEMPERATURA_OLEO_INFO":             146 + 12764,                    # Leituras.PCTA_UHTA01_TemperaturaOleo_info
    "UHTA01_TEMP_OLEO_H":                       [146 + 12764, 0],               # PCTA.UHTA01.TemperaturaOleo_Info.H
    "UHTA01_TEMP_OLEO_HH":                      [146 + 12764, 1],               # PCTA.UHTA01.TemperaturaOleo_Info.HH

    "UHTA01_VALVULAS":                          147 + 12764,                    # Leituras.PCTA_UHTA01_Valvulas
    "UHTA01_VALVULAS01":                        [147 + 12764, 0],               # PCTA.UHTA01.Valvulas.[01]

    "UHTA01_PRESSOSTATOS":                      148 + 12764,                    # Leituras.PCTA_UHTA01_Pressostatos
    "UHTA01_PRESSOSTATOS01":                    [148 + 12764, 0],               # PCTA.UHTA01.Pressostatos.[01]
    "UHTA01_PRESSOSTATOS02":                    [148 + 12764, 1],               # PCTA.UHTA01.Pressostatos.[02]
    "UHTA01_PRESSOSTATOS03":                    [148 + 12764, 2],               # PCTA.UHTA01.Pressostatos.[03]

    "UHTA01_TEMPERATURA_OLEO":                  149 + 12764,                    # Leituras.PCTA_UHTA01_TemperaturaOleo
    "UHTA01_NIVEL_OLEO":                        150 + 12764,                    # Leituras.PCTA_UHTA01_NivelOleo

    "UHTA02_INFO":                              151 + 12764,                    # Leituras.PCTA_UHTA02_Info
    "UHTA02_OPERACIONAL":                       [151 + 12764, 0],               # PCTA.UHTA02.Info.Operacional
    "UHTA02_LIGADA":                            [151 + 12764, 1],               # PCTA.UHTA02.Info.Ligada

    "UHTA02_BOMBAS":                            152 + 12764,                    # Leituras.PCTA_UHTA02_Bombas
    "UHTA02_BOMBAS01":                          [152 + 12764, 0],               # PCTA.UHTA02.Bombas.[01]
    "UHTA02_BOMBAS02":                          [152 + 12764, 1],               # PCTA.UHTA02.Bombas.[02]

    "UHTA02_RODIZIO":                           153 + 12764,                    # Leituras.PCTA_UHTA02_Rodizio
    "UHTA02_RODIZ_BOMBA01":                     [153 + 12764, 0],               # PCTA.UHTA02.Rodizio.Bomba01
    "UHTA02_RODIZ_BOMBA02":                     [153 + 12764, 1],               # PCTA.UHTA02.Rodizio.Bomba02
    "UHTA02_RODIZ_HABILITADO":                  [153 + 12764, 2],               # PCTA.UHTA02.Rodizio.Habilitado

    "UHTA02_ACUMULADOR":                        154 + 12764,                    # Leituras.PCTA_UHTA02_AcumuladorBombaLider
    "UHTA02_ACUM_BOMBA_LIDER":                  [154 + 12764, 0],               # PCTA.UHTA02.AcumuladorBombaLider
    "UHTA02_ACUM_BOMBA_RETAGUARDA":             [155 + 12764, 1],               # PCTA.UHTA02.AcumuladorBombaRetaguarda

    "UHTA02_FILTROS":                           156 + 12764,                    # Leituras.PCTA_UHTA02_Filtros
    "UHTA02_FILTROS01":                         [156 + 12764, 0],               # PCTA.UHTA02.Filtros.[01]

    "UHTA02_NIVEL_OLEO_INFO":                   157 + 12764,                    # Leituras.PCTA_UHTA02_NivelOleo_Info
    "UHTA02_NIVEL_OLEO_LL":                     [157 + 12764, 0],               # PCTA.UHTA02.NivelOleo_Info.LL
    "UHTA02_NIVEL_OLEO_HH":                     [157 + 12764, 1],               # PCTA.UHTA02.NivelOleo_Info.HH

    "UHTA02_TEMPERATURA_OLEO_INFO":             158 + 12764,                    # Leituras.PCTA_UHTA02_TemperaturaOleo_info
    "UHTA02_TEMP_OLEO_H":                       [158 + 12764, 0],               # PCTA.UHTA02.TemperaturaOleo_Info.H
    "UHTA02_TEMP_OLEO_HH":                      [158 + 12764, 1],               # PCTA.UHTA02.TemperaturaOleo_Info.HH

    "UHTA02_VALVULAS":                          159 + 12764,                    # Leituras.PCTA_UHTA02_Valvulas
    "UHTA02_VALVULAS01":                        [159 + 12764, 0],               # PCTA.UHTA02.Valvulas.[01]

    "UHTA02_PRESSOSTATOS":                      160 + 12764,                    # Leituras.PCTA_UHTA02_Pressostatos
    "UHTA02_PRESSOSTATOS01":                    [160 + 12764, 0],               # PCTA.UHTA02.Pressostatos.[01]
    "UHTA02_PRESSOSTATOS02":                    [160 + 12764, 1],               # PCTA.UHTA02.Pressostatos.[02]
    "UHTA02_PRESSOSTATOS03":                    [160 + 12764, 2],               # PCTA.UHTA02.Pressostatos.[03]

    "UHTA02_TEMPERATURA_OLEO":                  161 + 12764,                    # Leituras.PCTA_UHTA02_TemperaturaOleo
    "UHTA02_NIVEL_OLEO":                        162 + 12764,                    # Leituras.PCTA_UHTA02_NivelOleo

    "PCTA_INFO":                                163 + 12764,                    # Leituras.PCTA_Info
    "PCTA_FALTA_FASE":                          [163 + 12764, 0],               # PCTA.Info.FaltaFase
    "PCTA_SENS_PRESEN_ATUADO":                  [163 + 12764, 1],               # PCTA.Info.SensorPresencaAtuado
    "PCTA_SENS_PRESEN_INIBIDO":                 [163 + 12764, 2],               # PCTA.Info.SensorPresencaInibido
    "PCTA_SENS_FUMA_ATUADO":                    [163 + 12764, 3],               # PCTA.Info.SensorFumacaAtuado
    "PCTA_SENS_FUMA_DESCONEC":                  [163 + 12764, 4],               # PCTA.Info.SensorFumacaDesconectado
    "PCTA_MODO_REMOTO":                         [163 + 12764, 5],               # PCTA.Info.ModoRemoto


    ## ALARMES

    "Alarme01_04":                              [1 + 1, 4],
    "Alarme01_05":                              [1 + 1, 5],
    "Alarme01_06":                              [1 + 1, 6],

    "Alarme22_00":                              [22, 0],
    "Alarme22_03":                              [22, 3],
    "Alarme22_04":                              [22, 4],
    "Alarme22_05":                              [22, 5],
    "Alarme22_06":                              [22, 6],
    "Alarme22_07":                              [22, 7],
    "Alarme22_08":                              [22, 8],
    "Alarme22_09":                              [22, 9],
    "Alarme22_10":                              [22, 10],
    "Alarme22_11":                              [22, 11],
    "Alarme22_14":                              [22, 14],
    "Alarme22_15":                              [22, 15],

    "Alarme23_01":                              [23, 1],
    "Alarme23_02":                              [23, 2],
    "Alarme23_04":                              [23, 4],
    "Alarme23_05":                              [23, 5],
    "Alarme23_06":                              [23, 6],
    "Alarme23_07":                              [23, 7],
    "Alarme23_08":                              [23, 8],
    "Alarme23_11":                              [23, 11],
    "Alarme23_12":                              [23, 12],
    "Alarme23_13":                              [23, 13],
    "Alarme23_14":                              [23, 14],
    "Alarme23_15":                              [23, 15],

    "Alarme24_02":                              [24, 2],
    "Alarme24_03":                              [24, 3],
    "Alarme24_04":                              [24, 4],
    "Alarme24_05":                              [24, 5],
    "Alarme24_06":                              [24, 6],
    "Alarme24_07":                              [24, 7],
    "Alarme24_08":                              [24, 8],
    "Alarme24_09":                              [24, 9],
    "Alarme24_10":                              [24, 10],
    "Alarme24_13":                              [24, 13],
    "Alarme24_14":                              [24, 14],

    "Alarme25_00":                              [25, 0],
    "Alarme25_01":                              [25, 1],
    "Alarme25_03":                              [25, 3],
    "Alarme25_04":                              [25, 4],
    "Alarme25_05":                              [25, 5],
    "Alarme25_06":                              [25, 6],
    "Alarme25_07":                              [25, 7],
    "Alarme25_10":                              [25, 10],
    "Alarme25_11":                              [25, 11],
    "Alarme25_12":                              [25, 12],
    "Alarme25_13":                              [25, 13],
    "Alarme25_14":                              [25, 14],

    "Alarme26_01":                              [26, 1],
    "Alarme26_02":                              [26, 2],
    "Alarme26_04":                              [26, 4],
    "Alarme26_05":                              [26, 5],
    "Alarme26_07":                              [26, 7],
    "Alarme26_08":                              [26, 8],
    "Alarme26_09":                              [26, 9],
    "Alarme26_10":                              [26, 10],
    "Alarme26_11":                              [26, 11],
    "Alarme26_12":                              [26, 12],
    "Alarme26_13":                              [26, 13],
    "Alarme26_14":                              [26, 14],

    "Alarme27_00":                              [27, 0],
    "Alarme27_01":                              [27, 1],
    "Alarme27_02":                              [27, 2],
    "Alarme27_03":                              [27, 3],
}


REG_AD = {
    ## COMANDOS
    # Comportas
    "CMD_CP_01_ABRIR":                          57 + 12289,                     # Comandos.PCAD_Comporta01Abrir
    "CMD_CP_01_PARAR":                          58 + 12289,                     # Comandos.PCAD_Comporta01Parar
    "CMD_CP_01_FECHAR":                         59 + 12289,                     # Comandos.PCAD_Comporta01Fechar
    "CMD_CP_01_BUSCAR":                         60 + 12289,                     # Comandos.PCAD_Comporta01Buscar
    "CMD_CP_02_ABRIR":                          61 + 12289,                     # Comandos.PCAD_Comporta02Abrir
    "CMD_CP_02_PARAR":                          62 + 12289,                     # Comandos.PCAD_Comporta02Parar
    "CMD_CP_02_FECHAR":                         63 + 12289,                     # Comandos.PCAD_Comporta02Fechar
    "CMD_CP_02_BUSCAR":                         64 + 12289,                     # Comandos.PCAD_Comporta02Buscar

    # Modo Setpoint
    "CMD_MODO_SP_DESABILITAR":                  66 + 12289,                     # Comandos.PCAD_ModoSetpointHabilitar
    "CMD_MODO_SP_HABILITAR":                    65 + 12289,                     # Comandos.PCAD_ModoSetpointDesabilitar

    # UHCD
    "CMD_UHCD_RODIZIO_AUTO":                    67 + 12289,                     # Comandos.PCAD_UHCD_RodizioAutomatico
    "CMD_UHCD_RODIZIO_MANUAL":                  68 + 12289,                     # Comandos.PCAD_UHCD_RodizioManual

    # Bombas
    "CMD_BOMBA_01_LIGAR":                       69 + 12289,                     # Comandos.PCAD_Bomba01Ligar
    "CMD_BOMBA_01_DESLIGAR":                    70 + 12289,                     # Comandos.PCAD_Bomba01Desligar
    "CMD_BOMBA_01_PRINCIPAL":                   71 + 12289,                     # Comandos.PCAD_Bomba01Principal
    "CMD_BOMBA_02_LIGAR":                       72 + 12289,                     # Comandos.PCAD_Bomba02Ligar
    "CMD_BOMBA_02_DESLIGAR":                    73 + 12289,                     # Comandos.PCAD_Bomba02Desligar
    "CMD_BOMBA_02_PRINCIPAL":                   74 + 12289,                     # Comandos.PCAD_Bomba02Principal

    # Sensores
    "CMD_SENSOR_PRESEN_INIBIR":                 75 + 12289,                     # Comandos.PCAD_SensorPresencaInibir
    "CMD_SENSOR_PRESEN_DESINIBIR":              76 + 12289,                     # Comandos.PCAD_SensorPresencaDesinibir


    ## SETPOINTS
    # Comportas
    "CP_01_SP_POS":                             14 + 13569,                     # Setpoints.PCAD_Comporta01_SetpointPosicao
    "CP_02_SP_POS":                             15 + 13569,                     # Setpoints.PCAD_Comporta02_SetpointPosicao

    # Manobras UHCD
    "UHCD_MANO_RODIZIO_LIDER":                  16 + 13569,                     # Setpoints.PCAD_UHCD_ManobrasRodizioLider
    "UHCD_MANO_RODIZIO_RETAGUARDA":             17 + 13569,                     # Setpoints.PCAD_UHCD_ManobrasRodizioRetaguarda


    ## LEITURAS
    # Comportas
    "CP_01_INFO":                               164 + 12764,                    # Leituras.PCAD_Comporta01_Info
    "CP_01_ABRINDO":                            [164 + 12764, 0],               # PCAD.Comporta01.Info.Abrindo
    "CP_01_FECHANDO":                           [164 + 12764, 1],               # PCAD.Comporta01.Info.Fechando
    "CP_01_ABERTA":                             [164 + 12764, 2],               # PCAD.Comporta01.Info.Aberta
    "CP_01_FECHADA":                            [164 + 12764, 3],               # PCAD.Comporta01.Info.Fechada
    "CP_01_PARADA":                             [164 + 12764, 4],               # PCAD.Comporta01.Info.Parada
    "CP_01_ACION_LOCAL":                        [164 + 12764, 5],               # PCAD.Comporta01.Info.AcionamentoLocal

    "CP_01_POSICAO":                            165 + 12764,                    # Leituras.PCAD_Comporta01_Posicao

    "CP_02_INFO":                               166 + 12764,                    # Leituras.PCAD_Comporta02_Info
    "CP_02_ABRINDO":                            [166 + 12764, 0],               # PCAD.Comporta02.Info.Abrindo
    "CP_02_FECHANDO":                           [166 + 12764, 1],               # PCAD.Comporta02.Info.Fechando
    "CP_02_ABERTA":                             [166 + 12764, 2],               # PCAD.Comporta02.Info.Aberta
    "CP_02_FECHADA":                            [166 + 12764, 3],               # PCAD.Comporta02.Info.Fechada
    "CP_02_PARADA":                             [166 + 12764, 4],               # PCAD.Comporta02.Info.Parada
    "CP_02_ACION_LOCAL":                        [166 + 12764, 5],               # PCAD.Comporta02.Info.AcionamentoLocal

    "CP_02_POSICAO":                            167 + 12764,                    # Leituras.PCAD_Comporta02_Posicao

    # UHCD,
    "UHCD_INFO":                                168 + 12764,                    # Leituras.PCAD_UHCD_Info
    "UHCD_OPERACIONAL":                         [168 + 12764, 0],               # PCAD.UHCD.Info.Operacional
    "UHCD_LIGADA":                              [168 + 12764, 1],               # PCAD.UHCD.Info.Ligada

    "UHCD_BOMBAS":                              169 + 12764,                    # Leituras.PCAD_UHCD_Bombas
    "UHCD_BOMBAS01":                            [169 + 12764, 0],               # PCAD.UHCD.Bombas.[01]
    "UHCD_BOMBAS02":                            [169 + 12764, 1],               # PCAD.UHCD.Bombas.[02]

    "UHCD_RODIZIO":                             170 + 12764,                    # Leituras.PCAD_UHCD_Rodizio
    "UHCD_RODIZ_BOMBA01":                       [170 + 12764, 0],               # PCAD.UHCD.Rodizio.Bomba01
    "UHCD_RODIZ_BOMBA02":                       [170 + 12764, 1],               # PCAD.UHCD.Rodizio.Bomba02
    "UHCD_RODIZ_HABILITADO":                    [170 + 12764, 2],               # PCAD.UHCD.Rodizio.RodizioHabilitado

    "UHCD_ACUMULADOR":                          171 + 12764,                    # Leituras.PCAD_UHCD_AcumuladorBombaLider
    "UHCD_ACUM_BOMBA_LIDER":                    [171 + 12764, 0],               # PCAD.UHCD.Acumulador.BombaLider
    "UHCD_ACUM_BOMBA_RETAGUARDA":               [172 + 12764, 1],               # PCAD.UHCD.Acumulador.BombaRetaguarda

    "UHCD_FILTROS":                             173 + 12764,                    # Leituras.PCAD_UHCD_Filtros
    "UHCD_FILTRO01":                            [173 + 12764, 0],               # PCAD.UHCD.Filtros.[01]

    "UHCD_NIVEL_OLEO_INFO":                     174 + 12764,                    # Leituras.PCAD_UHCD_NivelOleo_Info
    "UHCD_NIVEL_OLEO_LL":                       [174 + 12764, 0],               # PCAD.UHCD.NivelOleo_info.LL
    "UHCD_NIVEL_OLEO_HH":                       [174 + 12764, 1],               # PCAD.UHCD.NivelOleo_info.HH

    "UHCD_TEMPERATURA_OLEO_INFO":               175 + 12764,                    # Leituras.PCAD_UHCD_TemperaturaOleo_Info
    "UHCD_TEMPE_OLEO_H":                        [175 + 12764, 0],               # PCAD.UHCD.TemperaturaOleo_Info.H
    "UHCD_TEMPE_OLEO_H":                        [175 + 12764, 1],               # PCAD.UHCD.TemperaturaOleo_Info.HH

    "UHCD_VALVULAS":                            176 + 12764,                    # Leituras.PCAD_UHCD_Valvulas
    "UHCD_VALVULAS01":                          [176 + 12764, 0],               # PCAD.UHCD.Valvulas.[01]

    "UHCD_PRESSOSTATOS":                        177 + 12764,                    # Leituras.PCAD_UHCD_Pressostatos
    "UHCD_PRESSOSTATOS01":                      [177 + 12764, 0],               # PCAD.UHCD.Pressostatos.[01]
    "UHCD_PRESSOSTATOS02":                      [177 + 12764, 1],               # PCAD.UHCD.Pressostatos.[02]
    "UHCD_PRESSOSTATOS03":                      [177 + 12764, 2],               # PCAD.UHCD.Pressostatos.[03]

    "UHCD_TEMPERATURA_OLEO":                    178 + 12764,                    # Leituras.PCAD_UHCD_TemperaturaOleo
    "UHCD_NIVEL_OLEO":                          179 + 12764,                    # Leituras.PCAD_UHCD_NivelOleo

    "PCAD_INFO":                                180 + 12764,                    # Leituras.PCAD_Info
    "PCAD_FALTA_FASE":                          [180 + 12764, 0],               # PCAD.UHCD.PCAD_Info.FaltaFase
    "PCAD_SENS_PRESEN_ATUADO":                  [180 + 12764, 1],               # PCAD.UHCD.PCAD_Info.SensorPresencaAtuado
    "PCAD_SENS_PRESEN_INIBIDO":                 [180 + 12764, 2],               # PCAD.UHCD.PCAD_Info.SensorPresencaInibido
    "PCAD_SENS_FUMA_ATUADO":                    [180 + 12764, 3],               # PCAD.UHCD.PCAD_Info.SensorFumacaAtuado
    "PCAD_SENS_FUMA_DESCONECTADO":              [180 + 12764, 4],               # PCAD.UHCD.PCAD_Info.SensorFumacaDesconectado
    "PCAD_MODO_REMOTO":                         [180 + 12764, 5],               # PCAD.UHCD.PCAD_Info.ModoRemoto
    "PCAD_MODO_SETPOT_HAB":                     [180 + 12764, 6],               # PCAD.UHCD.PCAD_Info.ModoSetpointHabilitado


    ## ALARMES
    "Alarme28_00":                              [28 + 14089, 0],
    "Alarme28_01":                              [28 + 14089, 1],
    "Alarme28_04":                              [28 + 14089, 4],
    "Alarme28_05":                              [28 + 14089, 5],
    "Alarme28_06":                              [28 + 14089, 6],
    "Alarme28_07":                              [28 + 14089, 7],
    "Alarme28_08":                              [28 + 14089, 8],
    "Alarme28_09":                              [28 + 14089, 9],
    "Alarme28_10":                              [28 + 14089, 10],
    "Alarme28_11":                              [28 + 14089, 11],
    "Alarme28_12":                              [28 + 14089, 12],

    "Alarme29_00":                              [29 + 14089, 0],
    "Alarme29_01":                              [29 + 14089, 1],
    "Alarme29_02":                              [29 + 14089, 2],
    "Alarme29_03":                              [29 + 14089, 3],
    "Alarme29_05":                              [29 + 14089, 5],
    "Alarme29_06":                              [29 + 14089, 6],
    "Alarme29_07":                              [29 + 14089, 7],
    "Alarme29_09":                              [29 + 14089, 9],
    "Alarme29_10":                              [29 + 14089, 10],
    "Alarme29_11":                              [29 + 14089, 11],
    "Alarme29_13":                              [29 + 14089, 13],

    "Alarme30_00":                              [30 + 14089, 0],
    "Alarme30_01":                              [30 + 14089, 1],
    "Alarme30_04":                              [30 + 14089, 4],
    "Alarme30_05":                              [30 + 14089, 5],
    "Alarme30_08":                              [30 + 14089, 8],
    "Alarme30_09":                              [30 + 14089, 9],
    "Alarme30_10":                              [30 + 14089, 10],
    "Alarme30_11":                              [30 + 14089, 11],

    "Alarme31_00":                              [31 + 14089, 0],
    "Alarme31_01":                              [31 + 14089, 1],
    "Alarme31_02":                              [31 + 14089, 2],
    "Alarme31_03":                              [31 + 14089, 3],
    "Alarme31_04":                              [31 + 14089, 4],
    "Alarme31_05":                              [31 + 14089, 5],
    "Alarme31_06":                              [31 + 14089, 6],
}

REG_UG = {
    "UG1": {
        ## COMANDOS
        # Gerais
        "CMD_RESET_ALARMES":                    0 + 12289,                      # Comandos.Operacao_PCH_AdoPopinhakResetAlarmes
        "CMD_RECONHECE_ALARMES":                1 + 12289,                      # Comandos.Operacao_PCH_AdoPopinhakReconheceAlarmes

        # Operação
        "CMD_OPER_UP":                          2 + 12289,                      # Comandos.Operacao_UP
        "CMD_OPER_UPGM":                        3 + 12289,                      # Comandos.Operacao_UPGM
        "CMD_OPER_UVD":                         4 + 12289,                      # Comandos.Operacao_UVD
        "CMD_OPER_UPS":                         5 + 12289,                      # Comandos.Operacao_UPS
        "CMD_OPER_US":                          6 + 12289,                      # Comandos.Operacao_US
        "CMD_OPER_EMERGENCIA_LIGAR":            7 + 12289,                      # Comandos.Operacao_EmergenciaLigar
        "CMD_OPER_EMERGENCIA_DESLIGAR":         8 + 12289,                      # Comandos.Operacao_EmergenciaDesligar
        "CMD_OPER_PARADA_RESET":                72 + 12289,                     # Comandos.Operacao_ParadaReset

        # Turbina
        "CMD_TURB_BYPASS_ABRIR":                9 + 12289,                      # Comandos.Turb_ByPassAbrir
        "CMD_TURB_BYPASS_FECHAR":               10 + 12289,                     # Comandos.Turb_ByPassFechar
        "CMD_TURB_BORBOLETA_ABRIR":             11 + 12289,                     # Comandos.Turb_BorboletaAbrir
        "CMD_TURB_BORBOLETA_FECHAR":            12 + 12289,                     # Comandos.Turb_BorboletaFechar
        "CMD_TURB_FRENAGEM_APLICAR":            13 + 12289,                     # Comandos.Turb_FrenagemAplicar
        "CMD_TURB_FRENAGEM_DESAPLICAR":         14 + 12289,                     # Comandos.Turb_FrenagemDesaplicar
        "CMD_TURB_FRENAGEM_MANUAL":             15 + 12289,                     # Comandos.Turb_FrenagemManual
        "CMD_TURB_FRENAGEM_AUTO":               16 + 12289,                     # Comandos.Turb_FrenagemAuto
        "CMD_TURB_SENSOR_ATIVAR":               17 + 12289,                     # Comandos.Turb_SensorAtivar
        "CMD_TURB_SENSOR_DESATIVAR":            18 + 12289,                     # Comandos.Turb_SensorDesativar

        # Reg V
        "CMD_REG_V_PARTIR":                     19 + 12289,                     # Comandos.RegV_Partir
        "CMD_REG_V_PARAR":                      20 + 12289,                     # Comandos.RegV_Parar
        "CMD_REG_V_COLOCAR_CARGA":              21 + 12289,                     # Comandos.RegV_ColocarCarga
        "CMD_REG_V_RETIRAR_CARGA":              22 + 12289,                     # Comandos.RegV_RetirarCarga
        "CMD_REG_V_INCREMENTA_VELOCIDADE":      23 + 12289,                     # Comandos.RegV_IncrementaVelocidade
        "CMD_REG_V_DECREMENTA_VELOCIDADE":      24 + 12289,                     # Comandos.RegV_DecrementaVelocidade
        "CMD_REG_V_SEL_MODO_ESTATISMO":         25 + 12289,                     # Comandos.RegV_SelecionaModoEstatismo
        "CMD_REG_V_SEL_MODO_BASECARGA":         26 + 12289,                     # Comandos.RegV_SelecionaModoBaseCarga

        # Reg T
        "CMD_REG_T_LIGAR":                      27 + 12289,                     # Comandos.RegT_Ligar
        "CMD_REG_T_DESLIGAR":                   28 + 12289,                     # Comandos.RegT_Desligar
        "CMD_REG_T_INCREMENTA_TENSAO":          29 + 12289,                     # Comandos.RegT_IncrementaTensao
        "CMD_REG_T_DECREMENTA_TENSAO":          30 + 12289,                     # Comandos.RegT_DecrementaTensao
        "CMD_REG_T_PRE_EXCITACAO":              31 + 12289,                     # Comandos.RegT_PreExcitacao

        # Sinc
        "CMD_SINC_LIGAR":                       32 + 12289,                     # Comandos.Sinc_Ligar
        "CMD_SINC_DESLIGAR":                    33 + 12289,                     # Comandos.Sinc_Desligar
        "CMD_SINC_MODO_AUTO_LIGAR":             34 + 12289,                     # Comandos.Sinc_ModoAutoLigar
        "CMD_SINC_MODO_MANUAL_LIGAR":           35 + 12289,                     # Comandos.Sinc_ModoManualLigar
        "CMD_SINC_MODO_BMORTA_LIGAR":           36 + 12289,                     # Comandos.Sinc_ModoBMortaLigar

        # DJ52G
        "CMD_DJ52G_ABRIR":                      37 + 12289,                     # Comandos.Disj52G_Abrir

        # Controle Reativo
        "CMD_CTRL_REATIVO_MODO_FPLIGAR":        38 + 12289,                     # Comandos.CtrlReativo_ModoFPLigar
        "CMD_CTRL_REATIVO_MODO_FPDESLIGAR":     39 + 12289,                     # Comandos.CtrlReativo_ModoFPDesligar
        "CMD_CTRL_REATIVO_MODO_VArLIGAR":       40 + 12289,                     # Comandos.CtrlReativo_ModoVArLigar
        "CMD_CTRL_REATIVO_MODO_VArDESLIGAR":    41 + 12289,                     # Comandos.CtrlReativo_ModoVArDesligar

        # Controle Potência
        "CMD_CTRL_POT_MODO_POT_LIGAR":          42 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaLigar
        "CMD_CTRL_POT_MODO_POT_DESLIGAR":       43 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaDesligar
        "CMD_CTRL_POT_MODO_NIVEL_LIGAR":        44 + 12289,                     # Comandos.CtrlPotencia_ModoNivelLigar
        "CMD_CTRL_POT_MODO_NIVEL_DESLIGAR":     45 + 12289,                     # Comandos.CtrlPotencia_ModoNivelDesligar
        "CMD_CTRL_POT_RELI_AUTO_LIGAR":         46 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoLigar
        "CMD_CTRL_POT_RELI_AUTO_DESLIGAR":      47 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoDesligar

        # UHCT
        "CMD_UHCT_BOMBA_01_LIGAR":              48 + 12289,                     # Comandos.UHCT_Bomba01Ligar
        "CMD_UHCT_BOMBA_01_DESLIGAR":           49 + 12289,                     # Comandos.UHCT_Bomba01Desligar
        "CMD_UHCT_BOMBA_01_PRINCIPAL":          50 + 12289,                     # Comandos.UHCT_Bomba01Principal
        "CMD_UHCT_BOMBA_02_LIGAR":              51 + 12289,                     # Comandos.UHCT_Bomba02Ligar
        "CMD_UHCT_BOMBA_02_DESLIGAR":           52 + 12289,                     # Comandos.UHCT_Bomba02Desligar
        "CMD_UHCT_BOMBA_02_PRINCIPAL":          53 + 12289,                     # Comandos.UHCT_Bomba02Principal
        "CMD_UHCT_BOMBA_AGUA_LIGAR":            54 + 12289,                     # Comandos.UHCT_BombaAguaLigar
        "CMD_UHCT_BOMBA_AGUA_DESLIGAR":         55 + 12289,                     # Comandos.UHCT_BombaAguaDesligar
        "CMD_UHCT_SENSOR_ATIVAR":               56 + 12289,                     # Comandos.UHCT_SensorAtivar
        "CMD_UHCT_SENSOR_DESATIVAR":            57 + 12289,                     # Comandos.UHCT_SensorDesativar
        "CMD_UHCT_RODIZIO_HABILITAR":           58 + 12289,                     # Comandos.UHCT_RodizioHabilitar
        "CMD_UHCT_RODIZIO_DESABILITAR":         59 + 12289,                     # Comandos.UHCT_RodizioDesabilitar

        # UHLM
        "CMD_UHLM_BOMBA_01_LIGAR":              60 + 12289,                     # Comandos.UHLM_Bomba01Ligar
        "CMD_UHLM_BOMBA_01_DESLIGAR":           61 + 12289,                     # Comandos.UHLM_Bomba01Desligar
        "CMD_UHLM_BOMBA_01_PRINCIPAL":          62 + 12289,                     # Comandos.UHLM_Bomba01Principal
        "CMD_UHLM_BOMBA_02_LIGAR":              63 + 12289,                     # Comandos.UHLM_Bomba02Ligar
        "CMD_UHLM_BOMBA_02_DESLIGAR":           64 + 12289,                     # Comandos.UHLM_Bomba02Desligar
        "CMD_UHLM_BOMBA_02_PRINCIPAL":          65 + 12289,                     # Comandos.UHLM_Bomba02Principal
        "CMD_UHLM_BOMBA_JACKING_LIGA":          66 + 12289,                     # Comandos.UHLM_BombaJackingLiga
        "CMD_UHLM_BOMBA_JACKING_DESLIGA":       67 + 12289,                     # Comandos.UHLM_BombaJackingDesliga
        "CMD_UHLM_BOMBA_AGUA_LIGA":             68 + 12289,                     # Comandos.UHLM_BombaAguaLiga
        "CMD_UHLM_BOMBA_AGUA_DESLIGA":          69 + 12289,                     # Comandos.UHLM_BombaAguaDesliga
        "CMD_UHLM_RODIZIO_HABILITAR":           70 + 12289,                     # Comandos.UHLM_RodizioHabilitar
        "CMD_UHLM_RODIZIO_DESABILITAR":         71 + 12289,                     # Comandos.UHLM_RodizioDesabilitar

        # RT
        "CMD_RT_MTVC_HABILITAR":                73 + 12289,                     # Comandos.RT_MTVC_Habilitar
        "CMD_RT_MECC_HABILITAR":                74 + 12289,                     # Comandos.RT_MECC_Habilitar
        "CMD_RT_ONLINE_HABILITAR":              75 + 12289,                     # Comandos.RT_Online_habilitar
        "CMD_RT_ONLINE_DESABILITAR":            76 + 12289,                     # Comandos.RT_Online_Desabiltar
        "CMD_RT_PARALELO_HABILITAR":            77 + 12289,                     # Comandos.RT_Paralelo_habilitar
        "CMD_RT_PARALELO_DESABILITAR":          78 + 12289,                     # Comandos.RT_Paralelo_Desabilitar

        # RV
        "CMD_RV_CONJUGADO_AUTO_HABILITAR":      79 + 12289,                     # Comandos.RV_ConjugadoAuto_habilitar
        "CMD_RV_CONJUGADO_MANUAL_HABILITAR":    80 + 12289,                     # Comandos.RV_ConjugadoManual_habilitar
        "CMD_RV_CONJUGADO_01_HABILITAR":        81 + 12289,                     # Comandos.RV_Conjugado01_habilitar
        "CMD_RV_CONJUGADO_02_HABILITAR":        82 + 12289,                     # Comandos.RV_Conjugado02_habilitar
        "CMD_RV_CONJUGADO_03_HABILITAR":        83 + 12289,                     # Comandos.RV_Conjugado03_habilitar
        "CMD_RV_CONJUGADO_04_HABILITAR":        84 + 12289,                     # Comandos.RV_Conjugado04_habilitar
        "CMD_RV_CONJUGADO_05_HABILITAR":        85 + 12289,                     # Comandos.RV_Conjugado05_habilitar


        ## SETPOINTS

        # UHCT
        "UHCT_PRESSAO_MAX":                     0 + 13569,                      # Setpoints.UHCT_PressaoMaxima
        "UHCT_PRESSAO_MIN":                     1 + 13569,                      # Setpoints.UHCT_PressaoMinima
        "UHCT_PRESSAO_DESLIGAMENTO":            2 + 13569,                      # Setpoints.UHCT_PressaoDesligamento
        "UHCT_PRESSAO_CRITICA":                 3 + 13569,                      # Setpoints.UHCT_PressaoCritica

        # Controle Potência
        "CRTL_POT_NIVEL_LL1":                   4 + 13569,                      # Setpoints.CtrlPotencia_NivelLL1
        "CRTL_POT_NIVEL_LL2":                   5 + 13569,                      # Setpoints.CtrlPotencia_NivelLL2
        "CRTL_POT_NIVEL_LL3":                   6 + 13569,                      # Setpoints.CtrlPotencia_NivelLL3
        "CRTL_POT_NIVEL_LL4":                   7 + 13569,                      # Setpoints.CtrlPotencia_NivelLL4
        "CRTL_POT_NIVEL_LL5":                   8 + 13569,                      # Setpoints.CtrlPotencia_NivelLL5
        "CRTL_POT_POT_1":                       9 + 13569,                      # Setpoints.CtrlPotencia_Potencia1
        "CRTL_POT_POT_2":                       10 + 13569,                     # Setpoints.CtrlPotencia_Potencia2
        "CRTL_POT_POT_3":                       11 + 13569,                     # Setpoints.CtrlPotencia_Potencia3
        "CRTL_POT_POT_4":                       12 + 13569,                     # Setpoints.CtrlPotencia_Potencia4
        "CRTL_POT_POT_5":                       13 + 13569,                     # Setpoints.CtrlPotencia_Potencia5
        "CRTL_POT_POT_MIN":                     14 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinima
        "CRTL_POT_POT_MIN_TEMPO":               15 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinimaTempo
        "CRTL_POT_NIVEL_RELIGAMENTO":           16 + 13569,                     # Setpoints.CtrlPotencia_NivelReligamento
        "CRTL_POT_ALVO":                        17 + 13569,                     # Setpoints.CtrlPotencia_Alvo
        "CRTL_POT_TOLERANCIA":                  18 + 13569,                     # Setpoints.CtrlPotencia_Tolerancia
        "CRTL_POT_PULSO_TEMPO":                 19 + 13569,                     # Setpoints.CtrlPotencia_PulsoTempo
        "CRTL_POT_PULSO_INTERVALO":             20 + 13569,                     # Setpoints.CtrlPotencia_PulsoIntervalo
        "CRTL_POT_SP_NIVEL":                    21 + 13569,                     # Setpoints.CtrlPotencia_SetpointNivel
        "CRTL_POT_NIVEL_MIN_ALARME":            22 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoAlarme
        "CRTL_POT_NIVEL_MIN_TRIP":              23 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoTRIP
        "CTRL_POT_POT_MAX":                     89 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMaxima

        # Controle Reativo
        "CRTL_REATIVO_SP_FP":                   24 + 13569,                     # Setpoints.CtrlReativo_SetpointFP
        "CRTL_REATIVO_SP_REATIVO":              25 + 13569,                     # Setpoints.CtrlReativo_SetpointReativo

        # Turbina
        "TURB_VIBRA_01_ALARME":                 26 + 13569,                     # Setpoints.Turb_Vibracao01Alarme
        "TURB_VIBRA_01_TRIP":                   27 + 13569,                     # Setpoints.Turb_Vibracao01TRIP
        "TURB_VIBRA_02_ALARME":                 28 + 13569,                     # Setpoints.Turb_Vibracao02Alarme
        "TURB_VIBRA_02_TRIP":                   29 + 13569,                     # Setpoints.Turb_Vibracao02TRIP
        "TURB_VIBRA_03_ALARME":                 30 + 13569,                     # Setpoints.Turb_Vibracao03Alarme
        "TURB_VIBRA_03_TRIP":                   31 + 13569,                     # Setpoints.Turb_Vibracao03TRIP
        "TURB_VIBRA_04_ALARME":                 32 + 13569,                     # Setpoints.Turb_Vibracao04Alarme
        "TURB_VIBRA_04_TRIP":                   33 + 13569,                     # Setpoints.Turb_Vibracao04TRIP
        "TURB_TEMPO_EQUALI_SP":                 34 + 13569,                     # Setpoints.Turb_TempoEqualizacaoSetpoint
        "TURB_VIBRA_05_ALARME":                 90 + 13569,                     # Setpoints.Turb_Vibracao05Alarme
        "TURB_VIBRA_05_TRIP":                   91 + 13569,                     # Setpoints.Turb_Vibracao05TRIP

        # Freio
        "FREIO_PULSO_INTERVALO":                35 + 13569,                     # Setpoints.Freio_PulsoIntervalo
        "FREIO_PULSO_TEMPO":                    36 + 13569,                     # Setpoints.Freio_PulsoTempo

        # UHCT
        "UHCT_RODIZIO_PRINCIPAL":               37 + 13569,                     # Setpoints.UHCT_RodizioPrincipal
        "UHCT_RODIZIO_RETAGUARDA":              38 + 13569,                     # Setpoints.UHCT_RodizioRetaguarda

        # UHLM
        "UHLM_RODIZIO_PRINCIPAL":               39 + 13569,                     # Setpoints.UHLM_RodizioPrincipal
        "UHLM_RODIZIO_RETAGUARDA":              40 + 13569,                     # Setpoints.UHLM_RodizioRetaguarda
        "UHLM_SP_VAZAO_01":                     92 + 13569,                     # Setpoints.UHLM_SetpointVazao01
        "UHLM_SP_VAZAO_02":                     93 + 13569,                     # Setpoints.UHLM_SetpointVazao02
        "UHLM_SP_VAZAO_03":                     94 + 13569,                     # Setpoints.UHLM_SetpointVazao03
        "UHLM_SP_VAZAO_04":                     95 + 13569,                     # Setpoints.UHLM_SetpointVazao04

        # Temperaturas
        "TEMPERATURA_01_ALARME":                41 + 13569,                     # Setpoints.Temperatura01_Alarme
        "TEMPERATURA_02_ALARME":                42 + 13569,                     # Setpoints.Temperatura02_Alarme
        "TEMPERATURA_03_ALARME":                43 + 13569,                     # Setpoints.Temperatura03_Alarme
        "TEMPERATURA_04_ALARME":                44 + 13569,                     # Setpoints.Temperatura04_Alarme
        "TEMPERATURA_05_ALARME":                45 + 13569,                     # Setpoints.Temperatura05_Alarme
        "TEMPERATURA_06_ALARME":                46 + 13569,                     # Setpoints.Temperatura06_Alarme
        "TEMPERATURA_07_ALARME":                47 + 13569,                     # Setpoints.Temperatura07_Alarme
        "TEMPERATURA_08_ALARME":                48 + 13569,                     # Setpoints.Temperatura08_Alarme
        "TEMPERATURA_09_ALARME":                49 + 13569,                     # Setpoints.Temperatura09_Alarme
        "TEMPERATURA_10_ALARME":                50 + 13569,                     # Setpoints.Temperatura10_Alarme
        "TEMPERATURA_11_ALARME":                51 + 13569,                     # Setpoints.Temperatura11_Alarme
        "TEMPERATURA_12_ALARME":                52 + 13569,                     # Setpoints.Temperatura12_Alarme
        "TEMPERATURA_13_ALARME":                53 + 13569,                     # Setpoints.Temperatura13_Alarme
        "TEMPERATURA_14_ALARME":                54 + 13569,                     # Setpoints.Temperatura14_Alarme
        "TEMPERATURA_15_ALARME":                55 + 13569,                     # Setpoints.Temperatura15_Alarme
        "TEMPERATURA_16_ALARME":                56 + 13569,                     # Setpoints.Temperatura16_Alarme
        "TEMPERATURA_01_TRIP01":                57 + 13569,                     # Setpoints.Temperatura01_TRIP01
        "TEMPERATURA_02_TRIP01":                58 + 13569,                     # Setpoints.Temperatura02_TRIP01
        "TEMPERATURA_03_TRIP01":                59 + 13569,                     # Setpoints.Temperatura03_TRIP01
        "TEMPERATURA_04_TRIP01":                60 + 13569,                     # Setpoints.Temperatura04_TRIP01
        "TEMPERATURA_05_TRIP01":                61 + 13569,                     # Setpoints.Temperatura05_TRIP01
        "TEMPERATURA_06_TRIP01":                62 + 13569,                     # Setpoints.Temperatura06_TRIP01
        "TEMPERATURA_07_TRIP01":                63 + 13569,                     # Setpoints.Temperatura07_TRIP01
        "TEMPERATURA_08_TRIP01":                64 + 13569,                     # Setpoints.Temperatura08_TRIP01
        "TEMPERATURA_09_TRIP01":                65 + 13569,                     # Setpoints.Temperatura09_TRIP01
        "TEMPERATURA_10_TRIP01":                66 + 13569,                     # Setpoints.Temperatura10_TRIP01
        "TEMPERATURA_11_TRIP01":                67 + 13569,                     # Setpoints.Temperatura11_TRIP01
        "TEMPERATURA_12_TRIP01":                68 + 13569,                     # Setpoints.Temperatura12_TRIP01
        "TEMPERATURA_13_TRIP01":                69 + 13569,                     # Setpoints.Temperatura13_TRIP01
        "TEMPERATURA_14_TRIP01":                70 + 13569,                     # Setpoints.Temperatura14_TRIP01
        "TEMPERATURA_15_TRIP01":                71 + 13569,                     # Setpoints.Temperatura15_TRIP01
        "TEMPERATURA_16_TRIP01":                72 + 13569,                     # Setpoints.Temperatura16_TRIP01
        "TEMPERATURA_01_TRIP02":                73 + 13569,                     # Setpoints.Temperatura01_TRIP02
        "TEMPERATURA_02_TRIP02":                74 + 13569,                     # Setpoints.Temperatura02_TRIP02
        "TEMPERATURA_03_TRIP02":                75 + 13569,                     # Setpoints.Temperatura03_TRIP02
        "TEMPERATURA_04_TRIP02":                76 + 13569,                     # Setpoints.Temperatura04_TRIP02
        "TEMPERATURA_05_TRIP02":                77 + 13569,                     # Setpoints.Temperatura05_TRIP02
        "TEMPERATURA_06_TRIP02":                78 + 13569,                     # Setpoints.Temperatura06_TRIP02
        "TEMPERATURA_07_TRIP02":                79 + 13569,                     # Setpoints.Temperatura07_TRIP02
        "TEMPERATURA_08_TRIP02":                80 + 13569,                     # Setpoints.Temperatura08_TRIP02
        "TEMPERATURA_09_TRIP02":                81 + 13569,                     # Setpoints.Temperatura09_TRIP02
        "TEMPERATURA_10_TRIP02":                82 + 13569,                     # Setpoints.Temperatura10_TRIP02
        "TEMPERATURA_11_TRIP02":                83 + 13569,                     # Setpoints.Temperatura11_TRIP02
        "TEMPERATURA_12_TRIP02":                84 + 13569,                     # Setpoints.Temperatura12_TRIP02
        "TEMPERATURA_13_TRIP02":                85 + 13569,                     # Setpoints.Temperatura13_TRIP02
        "TEMPERATURA_14_TRIP02":                86 + 13569,                     # Setpoints.Temperatura14_TRIP02
        "TEMPERATURA_15_TRIP02":                87 + 13569,                     # Setpoints.Temperatura15_TRIP02
        "TEMPERATURA_16_TRIP02":                88 + 13569,                     # Setpoints.Temperatura16_TRIP02

        # Grade Suja
        "GradeSuja_TRIP":                       96 + 13569,                     # Setpoints.GradeSuja_TRIP

        # Curva
        "CURVA_01_DISTRIB_P1":                  97 + 13569,                     # Setpoints.Curva01_DistribuidorP1
        "CURVA_01_DISTRIB_P2":                  98 + 13569,                     # Setpoints.Curva01_DistribuidorP2
        "CURVA_01_DISTRIB_P3":                  99 + 13569,                     # Setpoints.Curva01_DistribuidorP3
        "CURVA_01_DISTRIB_P4":                  100 + 13569,                    # Setpoints.Curva01_DistribuidorP4
        "CURVA_01_DISTRIB_P5":                  101 + 13569,                    # Setpoints.Curva01_DistribuidorP5
        "CURVA_01_DISTRIB_P6":                  102 + 13569,                    # Setpoints.Curva01_DistribuidorP6
        "CURVA_01_DISTRIB_P7":                  103 + 13569,                    # Setpoints.Curva01_DistribuidorP7
        "CURVA_01_DISTRIB_P8":                  104 + 13569,                    # Setpoints.Curva01_DistribuidorP8
        "CURVA_01_DISTRIB_P9":                  105 + 13569,                    # Setpoints.Curva01_DistribuidorP9
        "CURVA_01_DISTRIB_P10":                 106 + 13569,                    # Setpoints.Curva01_DistribuidorP10
        "CURVA_01_ROTOR_P1":                    107 + 13569,                    # Setpoints.Curva01_RotorP1
        "CURVA_01_ROTOR_P2":                    108 + 13569,                    # Setpoints.Curva01_RotorP2
        "CURVA_01_ROTOR_P3":                    109 + 13569,                    # Setpoints.Curva01_RotorP3
        "CURVA_01_ROTOR_P4":                    110 + 13569,                    # Setpoints.Curva01_RotorP4
        "CURVA_01_ROTOR_P5":                    111 + 13569,                    # Setpoints.Curva01_RotorP5
        "CURVA_01_ROTOR_P6":                    112 + 13569,                    # Setpoints.Curva01_RotorP6
        "CURVA_01_ROTOR_P7":                    113 + 13569,                    # Setpoints.Curva01_RotorP7
        "CURVA_01_ROTOR_P8":                    114 + 13569,                    # Setpoints.Curva01_RotorP8
        "CURVA_01_ROTOR_P9":                    115 + 13569,                    # Setpoints.Curva01_RotorP9
        "CURVA_01_ROTOR_P10":                   116 + 13569,                    # Setpoints.Curva01_RotorP10
        "CURVA_02_DISTRIB_P1":                  117 + 13569,                    # Setpoints.Curva02_DistribuidorP1
        "CURVA_02_DISTRIB_P2":                  118 + 13569,                    # Setpoints.Curva02_DistribuidorP2
        "CURVA_02_DISTRIB_P3":                  119 + 13569,                    # Setpoints.Curva02_DistribuidorP3
        "CURVA_02_DISTRIB_P4":                  120 + 13569,                    # Setpoints.Curva02_DistribuidorP4
        "CURVA_02_DISTRIB_P5":                  121 + 13569,                    # Setpoints.Curva02_DistribuidorP5
        "CURVA_02_DISTRIB_P6":                  122 + 13569,                    # Setpoints.Curva02_DistribuidorP6
        "CURVA_02_DISTRIB_P7":                  123 + 13569,                    # Setpoints.Curva02_DistribuidorP7
        "CURVA_02_DISTRIB_P8":                  124 + 13569,                    # Setpoints.Curva02_DistribuidorP8
        "CURVA_02_DISTRIB_P9":                  125 + 13569,                    # Setpoints.Curva02_DistribuidorP9
        "CURVA_02_DISTRIB_P10":                 126 + 13569,                    # Setpoints.Curva02_DistribuidorP10
        "CURVA_02_ROTOR_P1":                    127 + 13569,                    # Setpoints.Curva02_RotorP1
        "CURVA_02_ROTOR_P2":                    128 + 13569,                    # Setpoints.Curva02_RotorP2
        "CURVA_02_ROTOR_P3":                    129 + 13569,                    # Setpoints.Curva02_RotorP3
        "CURVA_02_ROTOR_P4":                    130 + 13569,                    # Setpoints.Curva02_RotorP4
        "CURVA_02_ROTOR_P5":                    131 + 13569,                    # Setpoints.Curva02_RotorP5
        "CURVA_02_ROTOR_P6":                    132 + 13569,                    # Setpoints.Curva02_RotorP6
        "CURVA_02_ROTOR_P7":                    133 + 13569,                    # Setpoints.Curva02_RotorP7
        "CURVA_02_ROTOR_P8":                    134 + 13569,                    # Setpoints.Curva02_RotorP8
        "CURVA_02_ROTOR_P9":                    135 + 13569,                    # Setpoints.Curva02_RotorP9
        "CURVA_02_ROTOR_P10":                   136 + 13569,                    # Setpoints.Curva02_RotorP10
        "CURVA_03_DISTRIB_P1":                  137 + 13569,                    # Setpoints.Curva03_DistribuidorP1
        "CURVA_03_DISTRIB_P2":                  138 + 13569,                    # Setpoints.Curva03_DistribuidorP2
        "CURVA_03_DISTRIB_P3":                  139 + 13569,                    # Setpoints.Curva03_DistribuidorP3
        "CURVA_03_DISTRIB_P4":                  140 + 13569,                    # Setpoints.Curva03_DistribuidorP4
        "CURVA_03_DISTRIB_P5":                  141 + 13569,                    # Setpoints.Curva03_DistribuidorP5
        "CURVA_03_DISTRIB_P6":                  142 + 13569,                    # Setpoints.Curva03_DistribuidorP6
        "CURVA_03_DISTRIB_P7":                  143 + 13569,                    # Setpoints.Curva03_DistribuidorP7
        "CURVA_03_DISTRIB_P8":                  144 + 13569,                    # Setpoints.Curva03_DistribuidorP8
        "CURVA_03_DISTRIB_P9":                  145 + 13569,                    # Setpoints.Curva03_DistribuidorP9
        "CURVA_03_DISTRIB_P10":                 146 + 13569,                    # Setpoints.Curva03_DistribuidorP10
        "CURVA_03_ROTOR_P1":                    147 + 13569,                    # Setpoints.Curva03_RotorP1
        "CURVA_03_ROTOR_P2":                    148 + 13569,                    # Setpoints.Curva03_RotorP2
        "CURVA_03_ROTOR_P3":                    149 + 13569,                    # Setpoints.Curva03_RotorP3
        "CURVA_03_ROTOR_P4":                    150 + 13569,                    # Setpoints.Curva03_RotorP4
        "CURVA_03_ROTOR_P5":                    151 + 13569,                    # Setpoints.Curva03_RotorP5
        "CURVA_03_ROTOR_P6":                    152 + 13569,                    # Setpoints.Curva03_RotorP6
        "CURVA_03_ROTOR_P7":                    153 + 13569,                    # Setpoints.Curva03_RotorP7
        "CURVA_03_ROTOR_P8":                    154 + 13569,                    # Setpoints.Curva03_RotorP8
        "CURVA_03_ROTOR_P9":                    155 + 13569,                    # Setpoints.Curva03_RotorP9
        "CURVA_03_ROTOR_P10":                   156 + 13569,                    # Setpoints.Curva03_RotorP10
        "CURVA_04_DISTRIB_P1":                  157 + 13569,                    # Setpoints.Curva04_DistribuidorP1
        "CURVA_04_DISTRIB_P2":                  158 + 13569,                    # Setpoints.Curva04_DistribuidorP2
        "CURVA_04_DISTRIB_P3":                  159 + 13569,                    # Setpoints.Curva04_DistribuidorP3
        "CURVA_04_DISTRIB_P4":                  160 + 13569,                    # Setpoints.Curva04_DistribuidorP4
        "CURVA_04_DISTRIB_P5":                  161 + 13569,                    # Setpoints.Curva04_DistribuidorP5
        "CURVA_04_DISTRIB_P6":                  162 + 13569,                    # Setpoints.Curva04_DistribuidorP6
        "CURVA_04_DISTRIB_P7":                  163 + 13569,                    # Setpoints.Curva04_DistribuidorP7
        "CURVA_04_DISTRIB_P8":                  164 + 13569,                    # Setpoints.Curva04_DistribuidorP8
        "CURVA_04_DISTRIB_P9":                  165 + 13569,                    # Setpoints.Curva04_DistribuidorP9
        "CURVA_04_DISTRIB_P10":                 166 + 13569,                    # Setpoints.Curva04_DistribuidorP10
        "CURVA_04_ROTOR_P1":                    167 + 13569,                    # Setpoints.Curva04_RotorP1
        "CURVA_04_ROTOR_P2":                    168 + 13569,                    # Setpoints.Curva04_RotorP2
        "CURVA_04_ROTOR_P3":                    169 + 13569,                    # Setpoints.Curva04_RotorP3
        "CURVA_04_ROTOR_P4":                    170 + 13569,                    # Setpoints.Curva04_RotorP4
        "CURVA_04_ROTOR_P5":                    171 + 13569,                    # Setpoints.Curva04_RotorP5
        "CURVA_04_ROTOR_P6":                    172 + 13569,                    # Setpoints.Curva04_RotorP6
        "CURVA_04_ROTOR_P7":                    173 + 13569,                    # Setpoints.Curva04_RotorP7
        "CURVA_04_ROTOR_P8":                    174 + 13569,                    # Setpoints.Curva04_RotorP8
        "CURVA_04_ROTOR_P9":                    175 + 13569,                    # Setpoints.Curva04_RotorP9
        "CURVA_04_ROTOR_P10":                   176 + 13569,                    # Setpoints.Curva04_RotorP10
        "CURVA_05_DISTRIB_P1":                  177 + 13569,                    # Setpoints.Curva05_DistribuidorP1
        "CURVA_05_DISTRIB_P2":                  178 + 13569,                    # Setpoints.Curva05_DistribuidorP2
        "CURVA_05_DISTRIB_P3":                  179 + 13569,                    # Setpoints.Curva05_DistribuidorP3
        "CURVA_05_DISTRIB_P4":                  180 + 13569,                    # Setpoints.Curva05_DistribuidorP4
        "CURVA_05_DISTRIB_P5":                  181 + 13569,                    # Setpoints.Curva05_DistribuidorP5
        "CURVA_05_DISTRIB_P6":                  182 + 13569,                    # Setpoints.Curva05_DistribuidorP6
        "CURVA_05_DISTRIB_P7":                  183 + 13569,                    # Setpoints.Curva05_DistribuidorP7
        "CURVA_05_DISTRIB_P8":                  184 + 13569,                    # Setpoints.Curva05_DistribuidorP8
        "CURVA_05_DISTRIB_P9":                  185 + 13569,                    # Setpoints.Curva05_DistribuidorP9
        "CURVA_05_DISTRIB_P10":                 186 + 13569,                    # Setpoints.Curva05_DistribuidorP10
        "CURVA_05_ROTOR_P1":                    187 + 13569,                    # Setpoints.Curva05_RotorP1
        "CURVA_05_ROTOR_P2":                    188 + 13569,                    # Setpoints.Curva05_RotorP2
        "CURVA_05_ROTOR_P3":                    189 + 13569,                    # Setpoints.Curva05_RotorP3
        "CURVA_05_ROTOR_P4":                    190 + 13569,                    # Setpoints.Curva05_RotorP4
        "CURVA_05_ROTOR_P5":                    191 + 13569,                    # Setpoints.Curva05_RotorP5
        "CURVA_05_ROTOR_P6":                    192 + 13569,                    # Setpoints.Curva05_RotorP6
        "CURVA_05_ROTOR_P7":                    193 + 13569,                    # Setpoints.Curva05_RotorP7
        "CURVA_05_ROTOR_P8":                    194 + 13569,                    # Setpoints.Curva05_RotorP8
        "CURVA_05_ROTOR_P9":                    195 + 13569,                    # Setpoints.Curva05_RotorP9
        "CURVA_05_ROTOR_P10":                   196 + 13569,                    # Setpoints.Curva05_RotorP10

        # Referencia Curva
        "REFER_CURVA_01":                       197 + 13569,                    # Setpoints.ReferenciaCurva01
        "REFER_CURVA_02":                       198 + 13569,                    # Setpoints.ReferenciaCurva02
        "REFER_CURVA_03":                       199 + 13569,                    # Setpoints.ReferenciaCurva03
        "REFER_CURVA_04":                       200 + 13569,                    # Setpoints.ReferenciaCurva04
        "REFER_CURVA_05":                       201 + 13569,                    # Setpoints.ReferenciaCurva05

        # Outros
        "TEMPO_ATUALIZACAO":                    202 + 13569,                    # Setpoints.TempoAtualizacao
        "MODO_OPERACAO_RETENTIVO":              203 + 13569,                    # Setpoints.ModoOperacao_Retentivo
        "CURVA_SEL_RETENTIVO":                  204 + 13569,                    # Setpoints.CurvaSelecionada_Retentivo


        ## LEITURAS

        # Nível
        "NV_JUSANTE":                           2 + 12764,                      # Leituras.NivelJusante
        "NV_BARRAGEM":                          3 + 12764,                      # Leituras.NivelBarragem
        "NV_CANAL":                             4 + 12764,                      # Leituras.NivelCanal
        "NV_CAMARA_CARGA":                      5 + 12764,                      # Leituras.NivelCamaraCarga
        "QUEDA_BRUTA":                          131 + 12764,                    # Leituras.QuedaBruta

        # Operação
        "OPER_PAINEL_RESET_ALARMES":            [6 + 12764, 0],                 # Leituras.Operacao_PainelResetAlarmes
        "OPER_PAINEL_RECONHECE_ALARMES":        [7 + 12764, 1],                 # Leituras.Operacao_PainelReconheceAlarmes

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

        "OPER_INFO_PARADA":                     12 + 12764,                     # Leituras.Operacao_InfoParada
        "OPER_INFO_PARADA_NORMAL":              [12 + 12764, 0],                # Operacao.InfoParada.Normal
        "OPER_INFO_PARADA_EMERG":               [12 + 12764, 1],                # Operacao.InfoParada.Emergencia
        "OPER_INFO_PARADA_TRIP_AGUA":           [12 + 12764, 2],                # Operacao.InfoParada.TRIPAgua
        "OPER_INFO_PARADA_TRIP_M":              [12 + 12764, 3],                # Operacao.InfoParada.TRIPMecanico
        "OPER_INFO_PARADA_TRIP_E":              [12 + 12764, 4],                # Operacao.InfoParada.TRIPEletrico
        "OPER_INFO_PARADA_TRIP_H":              [12 + 12764, 5],                # Operacao.InfoParada.TRIPHidraulico
        "OPER_INFO_PARADA_RELIG_AUTO":          [12 + 12764, 6],                # Operacao.InfoParada.ReligamentoAutomatico
        "OPER_INFO_PARADA_PARTIDA_MANU":        [12 + 12764, 7],                # Operacao.InfoParada.PartidaManual
        "OPER_INFO_PARADA_INFO_INVAL":          [12 + 12764, 15],               # Operacao.InfoParada.ParadaInfoValida

        # UHCT
        "UHCT_INFO":                            13 + 12764,                     # Leituras.UHCT_Info
        "UHCT_OPERACIONAL":                     [13 + 12764, 0],                # UHCT.Info.Operacional
        "UHCT_LIGADA":                          [13 + 12764, 1],                # UHCT.Info.Ligada
        "UHCT_SENS_DESATIVADO":                 [13 + 12764, 2],                # UHCT.Info.SensorDesativado
        "UHCT_MODO_LOCAL":                      [13 + 12764, 3],                # UHCT.Info.ModoLocal

        "UHCT_BOMBAS":                          14 + 12764,                     # Leituras.UHCT_Bombas
        "UHCT_BOMBAS01":                        [14 + 12764, 0],                # UHCT.Bombas.Bomba01
        "UHCT_BOMBAS02":                        [14 + 12764, 1],                # UHCT.Bombas.Bomba02
        "UHCT_BOMBAS03":                        [14 + 12764, 2],                # UHCT.Bombas.Bomba03

        "UHCT_RODIZIO":                         15 + 12764,                     # Leituras.UHCT_Rodizio
        "UHCT_RODIZ_HABILITADO":                [15 + 12764, 0],                # UHCT.Rodizio.RodizioHabilitado
        "UHCT_RODIZ_BOMBA01":                   [15 + 12764, 1],                # UHCT.Rodizio.Bomba01
        "UHCT_RODIZ_BOMBA02":                   [15 + 12764, 2],                # UHCT.Rodizio.Bomba02

        "UHCT_VALVULAS":                        16 + 12764,                     # Leituras.UHCT_Valvulas
        "UHCT_VALVULAS01":                      [16 + 12764, 0],                # UHCT.Valvulas.Valvulas01
        "UHCT_VALVULAS02":                      [16 + 12764, 1],                # UHCT.Valvulas.Valvulas02
        "UHCT_VALVULAS03":                      [16 + 12764, 2],                # UHCT.Valvulas.Valvulas03
        "UHCT_VALVULAS04":                      [16 + 12764, 3],                # UHCT.Valvulas.Valvulas04

        "UHCT_FILTROS":                         17 + 12764,                     # Leituras.UHCT_Filtros
        "UHCT_FILTROS01":                       [17 + 12764, 0],                # UHCT.Filtros.Filtro01
        "UHCT_FILTROS02":                       [17 + 12764, 1],                # UHCT.Filtros.Filtro02
        "UHCT_FILTROS03":                       [17 + 12764, 2],                # UHCT.Filtros.Filtro03
        "UHCT_FILTROS04":                       [17 + 12764, 3],                # UHCT.Filtros.Filtro04
        "UHCT_FILTROS05":                       [17 + 12764, 4],                # UHCT.Filtros.Filtro05

        "UHCT_PRESSOSTATOS":                    18 + 12764,                     # Leituras.UHCT_Pressostatos
        "UHCT_PRESSOSTATO01":                   [18 + 12764, 0],                # UHCT.Pressostatos.Pressostato01
        "UHCT_PRESSOSTATO02":                   [18 + 12764, 1],                # UHCT.Pressostatos.Pressostato02
        "UHCT_PRESSOSTATO03":                   [18 + 12764, 2],                # UHCT.Pressostatos.Pressostato03

        "UHCT_NIVEL_OLEO":                      19 + 12764,                     # Leituras.UHCT_NivelOleo
        "UHCT_NIVEL_OLEO_LL":                   [19 + 12764, 0],                # UHCT.NivelOleo.LL
        "UHCT_NIVEL_OLEO_L":                    [19 + 12764, 1],                # UHCT.NivelOleo.L
        "UHCT_NIVEL_OLEO_H":                    [19 + 12764, 2],                # UHCT.NivelOleo.H
        "UHCT_NIVEL_OLEO_HH":                   [19 + 12764, 3],                # UHCT.NivelOleo.HH

        "UHCT_PRESSAO_OLEO":                    20 + 12764,                     # Leituras.UHCT_PressaoOleo
        "UHCT_ACUM_RODIZIO_PRINCIPAL":          21 + 12764,                     # Leituras.UHCT_AcumuladorRodizioPrincipal
        "UHCT_ACUM_RODIZIO_RETAGUARDA":         22 + 12764,                     # Leituras.UHCT_AcumuladorRodizioRetaguarda

        # UHLM
        "UHLM_INFO":                            23 + 12764,                     # Leituras.UHLM_Info
        "UHLM_OPERACIONAL":                     [23 + 12764, 0],                # UHLM.Info.Operacional
        "UHLM_LIGADA":                          [23 + 12764, 1],                # UHLM.Info.Ligada
        "UHLM_MODO_LOCAL":                      [23 + 12764, 2],                # UHLM.Info.ModoLocal
        "UHLM_VALV_BOMBA_MECAN":                [23 + 12764, 3],                # UHLM.Info.UHLM_ValvulaBombaMecanica
        "UHLM_VALV_ENTRA_TRO_CALO_ABER":        [23 + 12764, 4],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Aberta
        "UHLM_VALV_ENTRA_TRO_CALO_FECH":        [23 + 12764, 5],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Fechada
        "UHLM_VALV_SAI_TRO_CALO_ABER":          [23 + 12764, 6],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Aberta
        "UHLM_VALV_SAI_TRO_CALO_FECH":          [23 + 12764, 7],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Fechada
        "UHLM_BOMBA_RETAG_OPERAC":              [23 + 12764, 8],                # UHLM.Info.UHLM_BombaRetaguarda_Operacional

        "UHLM_BOMBAS":                          24 + 12764,                     # Leituras.UHLM_Bombas
        "UHLM_BOMBA01":                         [24 + 12764, 0],                # UHLM.Bombas.Bomba01
        "UHLM_BOMBA02":                         [24 + 12764, 1],                # UHLM.Bombas.Bomba02
        "UHLM_BOMBA03":                         [24 + 12764, 2],                # UHLM.Bombas.Bomba03
        "UHLM_BOMBA04":                         [24 + 12764, 3],                # UHLM.Bombas.Bomba04

        "UHLM_RODIZIO":                         25 + 12764,                     # Leituras.UHLM_Rodizio
        "UHLM_RODIZ_HABILITADO":                [25 + 12764, 0],                # UHLM.Rodizio.RodizioHabilitado
        "UHLM_RODIZ_BOMBA01":                   [25 + 12764, 1],                # UHLM.Rodizio.Bomba01
        "UHLM_RODIZ_BOMBA02":                   [25 + 12764, 2],                # UHLM.Rodizio.Bomba02

        "UHLM_FILTROS":                         26 + 12764,                     # Leituras.UHLM_Filtros
        "UHLM_FILTRO01":                        [26 + 12764, 0],                # UHLM.Filtros.Filtro01
        "UHLM_FILTRO02":                        [26 + 12764, 1],                # UHLM.Filtros.Filtro02
        "UHLM_FILTRO03":                        [26 + 12764, 2],                # UHLM.Filtros.Filtro03
        "UHLM_FILTRO04":                        [26 + 12764, 3],                # UHLM.Filtros.Filtro04
        "UHLM_FILTRO05":                        [26 + 12764, 4],                # UHLM.Filtros.Filtro05

        "UHLM_PRESSOSTATOS":                    27 + 12764,                     # Leituras.UHLM_Pressostatos
        "UHLM_PRESSOSTATO01":                   [27 + 12764, 0],                # UHLM.Pressostatos.Pressostato01
        "UHLM_PRESSOSTATO02":                   [27 + 12764, 1],                # UHLM.Pressostatos.Pressostato02
        "UHLM_PRESSOSTATO03":                   [27 + 12764, 2],                # UHLM.Pressostatos.Pressostato03
        "UHLM_PRESSOSTATO04":                   [27 + 12764, 3],                # UHLM.Pressostatos.Pressostato04

        "UHLM_FLUXOSTATOS":                     28 + 12764,                     # Leituras.UHLM_Fluxostatos
        "UHLM_FLUXOSTATO01":                    [28 + 12764, 0],                # UHLM.Fluxostatos.Fluxostato01
        "UHLM_FLUXOSTATO02":                    [28 + 12764, 1],                # UHLM.Fluxostatos.Fluxostato02
        "UHLM_FLUXOSTATO03":                    [28 + 12764, 2],                # UHLM.Fluxostatos.Fluxostato03
        "UHLM_FLUXOSTATO04":                    [28 + 12764, 3],                # UHLM.Fluxostatos.Fluxostato04
        "UHLM_FLUXOSTATO05":                    [28 + 12764, 4],                # UHLM.Fluxostatos.Fluxostato05
        "UHLM_FLUXOSTATO06":                    [28 + 12764, 5],                # UHLM.Fluxostatos.Fluxostato06
        "UHLM_FLUXOSTATO07":                    [28 + 12764, 6],                # UHLM.Fluxostatos.Fluxostato07

        "UHLM_NIVEL_OLEO":                      29 + 12764,                     # Leituras.UHLM_NivelOleo
        "UHLM_NIVEL_OLEO_LL":                   [29 + 12764, 0],                # UHLM.NivelOleo.LL
        "UHLM_NIVEL_OLEO_L":                    [29 + 12764, 1],                # UHLM.NivelOleo.L
        "UHLM_NIVEL_OLEO_H":                    [29 + 12764, 2],                # UHLM.NivelOleo.H
        "UHLM_NIVEL_OLEO_HH":                   [29 + 12764, 3],                # UHLM.NivelOleo.HH

        "UHLM_ACUM_RODIZIO_PRINCIPAL":          30 + 12764,                     # Leituras.UHLM_AcumuladorRodizioPrincipal
        "UHLM_ACUM_RODIZIO_RETAGUARDA":         31 + 12764,                     # Leituras.UHLM_AcumuladorRodizioRetaguarda

        "UHLM_FLUXOSTATO_OLEO_01":              123 + 12764,                    # Leituras.UHLM_FluxostatoOleo01
        "UHLM_FLUXOSTATO_OLEO_02":              124 + 12764,                    # Leituras.UHLM_FluxostatoOleo02
        "UHLM_FLUXOSTATO_OLEO_03":              125 + 12764,                    # Leituras.UHLM_FluxostatoOleo03
        "UHLM_FLUXOSTATO_OLEO_04":              126 + 12764,                    # Leituras.UHLM_FluxostatoOleo04

        # Turbina
        "TURB_INFO":                            32 + 12764,                     # Leituras.Turb_Info
        "TURB_EQUALIZADA":                      [32 + 12764, 0],                # Turbina.Info.Equalizada
        "TURB_PRONTA":                          [32 + 12764, 1],                # Turbina.Info.Pronta
        "TURB_FECHADA":                         [32 + 12764, 2],                # Turbina.Info.Fechada
        "TURB_TRAVADA":                         [32 + 12764, 3],                # Turbina.Info.Travada
        "TURB_PARADA":                          [32 + 12764, 4],                # Turbina.Info.Parada
        "TURB_EQUALIZANDO":                     [32 + 12764, 5],                # Turbina.Info.Equalizando
        "TURB_FECHANDO":                        [32 + 12764, 6],                # Turbina.Info.Fechando
        "TURB_SENS_DESATIVADO":                 [32 + 12764, 7],                # Turbina.Info.SensorDesativado
        "TURB_DISTRI_FECHADO":                  [32 + 12764, 8],                # Turbina.Info.DistribuidorFechado

        "TURB_VALVULA_BYPASS":                  33 + 12764,                     # Leituras.Turb_ValvulaByPass
        "TURB_VALV_BY_ACIONA":                  [33 + 12764, 0],                # Turbina.Bypass.Acionamento
        "TURB_VALV_BY_FECHADO":                 [33 + 12764, 1],                # Turbina.Bypass.Fechado
        "TURB_VALV_BY_ABERTO":                  [33 + 12764, 2],                # Turbina.Bypass.Aberto

        "TURB_VALVULA_BORBOLETA":               34 + 12764,                     # Leituras.Turb_ValvulaBorboleta
        "TURB_VALV_BORB_ACIONA":                [34 + 12764, 0],                # Turbina.Borboleta.Acionamento
        "TURB_VALV_BORB_FECHADA":               [34 + 12764, 1],                # Turbina.Borboleta.Fechada
        "TURB_VALV_BORB_ABERTA":                [34 + 12764, 2],                # Turbina.Borboleta.Aberta
        "TURB_VALV_BORB_DERIVA":                [34 + 12764, 3],                # Turbina.Borboleta.Deriva
        "TURB_VALV_BORB_TRAVADA":               [34 + 12764, 4],                # Turbina.Borboleta.Travada
        "TURB_VALV_BORB_MANTEM":                [34 + 12764, 5],                # Turbina.Borboleta.Mantem

        "TURB_TEMPO_CRACK_EFETIVO":             35 + 12764,                     # Leituras.Turb_TempoCrackEfetivo
        "TURB_TEMPO_EQUAL_EFETIVO":             36 + 12764,                     # Leituras.Turb_TempoEqualizacaoEfetivo
        "TURB_PRESSAO_CONDUTO":                 37 + 12764,                     # Leituras.Turb_PressaoConduto
        "TURB_PRESSAO_CAIXA_ESPIRAL":           38 + 12764,                     # Leituras.Turb_PressaoCaixaEspiral
        "TURB_VAZAO_TURBINADA":                 39 + 12764,                     # Leituras.Turb_VazaoTurbinada
        "TURB_VIBRACAO_01":                     40 + 12764,                     # Leituras.Turb_Vibracao01
        "TURB_VIBRACAO_02":                     41 + 12764,                     # Leituras.Turb_Vibracao02
        "TURB_VIBRACAO_03":                     42 + 12764,                     # Leituras.Turb_Vibracao03
        "TURB_VIBRACAO_04":                     43 + 12764,                     # Leituras.Turb_Vibracao04

        "TURB_FRENAGEM":                        44 + 12764,                     # Leituras.Turb_Frenagem
        "TURB_FRENA_APLICADO":                  [44 + 12764, 0],                # Turbina.Frenagem.Info.Aplicado
        "TURB_FRENA_MANUAL":                    [44 + 12764, 1],                # Turbina.Frenagem.Info.Manual
        "TURB_FRENA_PRESSOS":                   [44 + 12764, 2],                # Turbina.Frenagem.Info.Pressostato
        "TURB_FRENA_1ZE":                       [44 + 12764, 3],                # Turbina.Frenagem.Info.[1ZE]
        "TURB_FRENA_2ZE":                       [44 + 12764, 4],                # Turbina.Frenagem.Info.[2ZE]

        "TURB_VIBRACAO_05":                     127 + 12764,                    # Leituras.Turb_Vibracao05

        # Reg V
        "REG_V_INFO":                           45 + 12764,                     # Leituras.RegV_Info
        "REG_V_HABILITADO":                     [45 + 12764, 0],                # RegV.Info.Habilitado
        "REG_V_BASE_CARGA":                     [45 + 12764, 1],                # RegV.Info.BaseCarga
        "REG_V_RPM30":                          [45 + 12764, 2],                # RegV.Info.RPM30
        "REG_V_RPM90":                          [45 + 12764, 3],                # RegV.Info.RPM90
        "REG_V_CARGA_ZERADA":                   [45 + 12764, 4],                # RegV.Info.CargaZerada
        "REG_V_MODO_ESTATISMO":                 [45 + 12764, 5],                # RegV.Info.ModoEstatismo
        "REG_V_MODO_BASE_CARGA":                [45 + 12764, 6],                # RegV.Info.ModoBaseCarga
        "REG_V_DISTRI_FECHADO":                 [45 + 12764, 7],                # RegV.Info.DistribuidorFechado

        "REG_V_ESTADO":                         46 + 12764,                     # Leituras.RegV_Estado
        "REG_V_FALHA":                          [46 + 12764, 0],                # RegV.Estado.Falha
        "REG_V_PARADO":                         [46 + 12764, 1],                # RegV.Estado.Parado
        "REG_V_CTRL_MANUAL_DISTRI":             [46 + 12764, 2],                # RegV.Estado.ControleManualDistribuidor
        "REG_V_CTRL_MANUAL_VALV":               [46 + 12764, 3],                # RegV.Estado.ControleManualValvula
        "REG_V_CTRL_VELOC":                     [46 + 12764, 4],                # RegV.Estado.ControleVelocidade
        "REG_V_COMPENSA_POT_ATIVA":             [46 + 12764, 5],                # RegV.Estado.CompensacaoPotenciaAtiva
        "REG_V_CTRL_POT_ATIVA":                 [46 + 12764, 6],                # RegV.Estado.ControlePotenciaAtiva

        "REG_V_VELOCIDADE":                     47 + 12764,                     # Leituras.RegV_Velocidade
        "REG_V_DISTRIBUIDOR":                   48 + 12764,                     # Leituras.RegV_Distribuidor
        "REG_V_ROTOR":                          49 + 12764,                     # Leituras.RegV_Rotor
        "REG_V_POT_ALVO":                       50 + 12764,                     # Leituras.RegV_PotenciaAlvo

        "REG_V_CONJUGADO_INFO":                 128 + 12764,                    # Leituras.RegV_CurvaConjugacao_Info
        "REG_V_CONJ_AUTOMATICO":                [128 + 12764, 0],               # RegV.Conjugado.Automatico
        "REG_V_CONJ_MANUAL":                    [128 + 12764, 1],               # RegV.Conjugado.Manual
        "REG_V_CONJUGADO1":                     [128 + 12764, 2],               # RegV.Conjugado.Conjugado1
        "REG_V_CONJUGADO2":                     [128 + 12764, 3],               # RegV.Conjugado.Conjugado2
        "REG_V_CONJUGADO3":                     [128 + 12764, 4],               # RegV.Conjugado.Conjugado3

        # Reg T
        "REG_T_INFO":                           51 + 12764,                     # Leituras.RegT_Info
        "REG_T_HABILITACAO":                    [51 + 12764, 0],                # RegT.Info.Habilitacao
        "REG_T_TENSAO_ESTAB":                   [51 + 12764, 1],                # RegT.Info.TensaoEstabilizada
        "REG_T_CONTATOR_ABERTO":                [51 + 12764, 2],                # RegT.Info.ContatorAberto
        "REG_T_CONTATOR_FECHADO":               [51 + 12764, 3],                # RegT.Info.ContatorFechado
        "REG_T_PRE_EXCITACAO":                  [51 + 12764, 4],                # RegT.Info.PreExcitacao
        "REG_T_MTVC":                           [51 + 12764, 5],                # RegT.Info.MTVC
        "REG_T_MECC":                           [51 + 12764, 6],                # RegT.Info.MECC
        "REG_T_OPER_ONLINE":                    [51 + 12764, 7],                # RegT.Info.OperacaoOnline
        "REG_T_OPER_PARALELA":                  [51 + 12764, 9],                # RegT.Info.OperacaoParalela

        "REG_T_UEXCITACAO":                     52 + 12764,                     # Leituras.RegT_UExcitacao
        "REG_T_IEXCITACAO":                     53 + 12764,                     # Leituras.RegT_IExcitacao
        "REG_T_FPALVO":                         129 + 12764,                    # Leituras.RegT_FPAlvo
        "REG_T_REATIVO_ALVO":                   130 + 12764,                    # Leituras.RegT_ReativoAlvo

        # Sinc
        "SINC_INFO":                            54 + 12764,                     # Leituras.Sinc_Info
        "SINC_HABILITADO":                      [54 + 12764, 0],                # Sincronoscopio.Info.Habilitado
        "SINC_MODO_AUTO":                       [54 + 12764, 1],                # Sincronoscopio.Info.ModoAutomatico
        "SINC_MODO_MANUAL":                     [54 + 12764, 2],                # Sincronoscopio.Info.ModoManual
        "SINC_BARRA_MORTA":                     [54 + 12764, 3],                # Sincronoscopio.Info.BarraMorta

        "SINC_FREQ_GERADOR":                    55 + 12764,                     # Leituras.Sinc_FrequenciaGerador
        "SINC_FREQ_BARRA":                      56 + 12764,                     # Leituras.Sinc_FrequenciaBarra
        "SINC_TENSAO_GERADOR":                  57 + 12764,                     # Leituras.Sinc_TensaoGerador
        "SINC_TENSAO_BARRA":                    58 + 12764,                     # Leituras.Sinc_TensaoBarra

        # DJ
        "Dj52G_INFO":                           59 + 12764,                     # Leituras.Disj52G_Info
        "Dj52G_ABERTO":                         [59 + 12764, 0],                # Disjuntor52G.Info.Aberto
        "Dj52G_FECHADO":                        [59 + 12764, 1],                # Disjuntor52G.Info.Fechado
        "Dj52G_INCONSISTENTE":                  [59 + 12764, 2],                # Disjuntor52G.Info.Inconsistente
        "Dj52G_TRIP":                           [59 + 12764, 3],                # Disjuntor52G.Info.TRIP
        "Dj52G_TESTE":                          [59 + 12764, 4],                # Disjuntor52G.Info.Teste
        "Dj52G_INSERIDO":                       [59 + 12764, 5],                # Disjuntor52G.Info.Inserido
        "Dj52G_EXTRAIVEL":                      [59 + 12764, 6],                # Disjuntor52G.Info.Extraivel
        "Dj52G_MOLA_CARRE":                     [59 + 12764, 7],                # Disjuntor52G.Info.MolaCarregada
        "Dj52G_CONDICAO":                       [59 + 12764, 8],                # Disjuntor52G.Info.CondicaoFechamento
        "Dj52G_FALTA_VCC":                      [59 + 12764, 9],                # Disjuntor52G.Info.FaltaVCC

        # Tensão
        "TENSAO_RN":                            60 + 12764,                     # Leituras.Gerador_TensaoRN
        "TENSAO_SN":                            61 + 12764,                     # Leituras.Gerador_TensaoSN
        "TENSAO_TN":                            62 + 12764,                     # Leituras.Gerador_TensaoTN
        "TENSAO_RS":                            63 + 12764,                     # Leituras.Gerador_TensaoRS
        "TENSAO_ST":                            64 + 12764,                     # Leituras.Gerador_TensaoST
        "TENSAO_TR":                            65 + 12764,                     # Leituras.Gerador_TensaoTR

        # Corrente
        "CORRENTE_R":                           66 + 12764,                     # Leituras.Gerador_CorrenteR
        "CORRENTE_S":                           67 + 12764,                     # Leituras.Gerador_CorrenteS
        "CORRENTE_T":                           68 + 12764,                     # Leituras.Gerador_CorrenteT
        "CORRENTE_MEDIA":                       69 + 12764,                     # Leituras.Gerador_CorrenteMedia

        # Potência Ativa
        "POT_ATIVA_1":                          70 + 12764,                     # Leituras.Gerador_PotenciaAtiva1
        "POT_ATIVA_2":                          71 + 12764,                     # Leituras.Gerador_PotenciaAtiva2
        "POT_ATIVA_3":                          72 + 12764,                     # Leituras.Gerador_PotenciaAtiva3
        "POT_ATIVA_MEDIA":                      73 + 12764,                     # Leituras.Gerador_PotenciaAtivaMedia

        # Potência Reativa
        "POT_REATIVA_1":                        74 + 12764,                     # Leituras.Gerador_PotenciaReativa1
        "POT_REATIVA_2":                        75 + 12764,                     # Leituras.Gerador_PotenciaReativa2
        "POT_REATIVA_3":                        76 + 12764,                     # Leituras.Gerador_PotenciaReativa3
        "POT_REATIVA_MEDIA":                    77 + 12764,                     # Leituras.Gerador_PotenciaReativaMedia

        # Potência Aparente
        "POT_APARENTE_1":                       78 + 12764,                     # Leituras.Gerador_PotenciaAparente1
        "POT_APARENTE_2":                       79 + 12764,                     # Leituras.Gerador_PotenciaAparente2
        "POT_APARENTE_3":                       80 + 12764,                     # Leituras.Gerador_PotenciaAparente3
        "POT_APARENTE_MEDIA":                   81 + 12764,                     # Leituras.Gerador_PotenciaAparenteMedia

        # Fator Potência
        "FATOR_POT_1":                          82 + 12764,                     # Leituras.Gerador_FatorPotencia1
        "FATOR_POT_2":                          83 + 12764,                     # Leituras.Gerador_FatorPotencia2
        "FATOR_POT_3":                          84 + 12764,                     # Leituras.Gerador_FatorPotencia3
        "FATOR_POT_MEDIA":                      85 + 12764,                     # Leituras.Gerador_FatorPotenciaMedia

        # Frequencia
        "FREQUENCIA":                           86 + 12764,                     # Leituras.Gerador_Frequencia

        # Energia Fornecida
        "ENERGIA_FORNECIDA_TWh":                87 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTWh
        "ENERGIA_FORNECIDA_GWh":                88 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGWh
        "ENERGIA_FORNECIDA_MWh":                89 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMWh
        "ENERGIA_FORNECIDA_kWh":                90 + 12764,                     # Leituras.Gerador_EnergiaFornecidakWh
        "ENERGIA_FORNECIDA_TVarh":              91 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTVarh
        "ENERGIA_FORNECIDA_GVarh":              92 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGVarh
        "ENERGIA_FORNECIDA_MVarh":              93 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMVarh
        "ENERGIA_FORNECIDA_kVarh":              94 + 12764,                     # Leituras.Gerador_EnergiaFornecidakVarh
        "ENERGIA_CORNECIDA_TVarh":              95 + 12764,                     # Leituras.Gerador_EnergiaConsumidaTVarh
        "ENERGIA_CORNECIDA_GVarh":              96 + 12764,                     # Leituras.Gerador_EnergiaConsumidaGVarh
        "ENERGIA_CORNECIDA_MVarh":              97 + 12764,                     # Leituras.Gerador_EnergiaConsumidaMVarh
        "ENERGIA_CORNECIDA_kVarh":              98 + 12764,                     # Leituras.Gerador_EnergiaConsumidakVarh
    
        "GERADOR_FP_INFO":                      99 + 12764,                     # Leituras.Gerador_FPInfo
        "GERADOR_FP_FASE1_IND":                 [99 + 12764, 0],                # Gerador.FP_Info.Fase1_Ind
        "GERADOR_FP_FASE1_CAP":                 [99 + 12764, 1],                # Gerador.FP_Info.Fase1_Cap
        "GERADOR_FP_FASE2_IND":                 [99 + 12764, 2],                # Gerador.FP_Info.Fase2_Ind
        "GERADOR_FP_FASE2_CAP":                 [99 + 12764, 3],                # Gerador.FP_Info.Fase2_Cap
        "GERADOR_FP_FASE3_IND":                 [99 + 12764, 4],                # Gerador.FP_Info.Fase3_Ind
        "GERADOR_FP_FASE3_CAP":                 [99 + 12764, 5],                # Gerador.FP_Info.Fase3_Cap
        "GERADOR_FP_FASE4_IND":                 [99 + 12764, 6],                # Gerador.FP_Info.Total_Ind
        "GERADOR_FP_FASE4_CAP":                 [99 + 12764, 7],                # Gerador.FP_Info.Total_Cap

        # Controles
        "CTRL_REATIVO_INFO":                    100 + 12764,                    # Leituras.CtrlReativo_Info
        "CTRL_REAT_MODO_FP":                    [100 + 12764, 0],               # CtrlReativo.Info.ModoFP
        "CTRL_REAT_MODO_VAR":                   [100 + 12764, 1],               # CtrlReativo.Info.ModoVar

        "CTRL_POTENCIA_INFO":                   101 + 12764,                    # Leituras.CtrlPotencia_Info
        "CTRL_POT_MODO_NIVEL":                  [101 + 12764, 0],               # CtrlPotencia.Info.ModoNivel
        "CTRL_POT_MODO_POT":                    [101 + 12764, 1],               # CtrlPotencia.Info.ModoPotencia
        "CTRL_POT_MODO_RELIGA_AUTO":            [101 + 12764, 2],               # CtrlPotencia.Info.ModoReligamentoAutomatico

        # Horimetros
        "HORIM_ELETR_LOW":                      102 + 12764,                    # Leituras.HorimetroEletrico_Low
        "HORIM_ELETR_HIGH":                     103 + 12764,                    # Leituras.HorimetroEletrico_High
        "HORIM_MECAN_LOW":                      104 + 12764,                    # Leituras.HorimetroMecanico_Low
        "HORIM_MECAN_HIGH":                     105 + 12764,                    # Leituras.HorimetroMecanico_High

        # Temperatura
        "TEMPERATURA_01":                       107 + 12764,                    # Leituras.Temperatura_01
        "TEMPERATURA_02":                       108 + 12764,                    # Leituras.Temperatura_02
        "TEMPERATURA_03":                       109 + 12764,                    # Leituras.Temperatura_03
        "TEMPERATURA_04":                       110 + 12764,                    # Leituras.Temperatura_04
        "TEMPERATURA_05":                       111 + 12764,                    # Leituras.Temperatura_05
        "TEMPERATURA_06":                       112 + 12764,                    # Leituras.Temperatura_06
        "TEMPERATURA_07":                       113 + 12764,                    # Leituras.Temperatura_07
        "TEMPERATURA_08":                       114 + 12764,                    # Leituras.Temperatura_08
        "TEMPERATURA_09":                       115 + 12764,                    # Leituras.Temperatura_09
        "TEMPERATURA_10":                       116 + 12764,                    # Leituras.Temperatura_10
        "TEMPERATURA_11":                       117 + 12764,                    # Leituras.Temperatura_11
        "TEMPERATURA_12":                       118 + 12764,                    # Leituras.Temperatura_12
        "TEMPERATURA_13":                       119 + 12764,                    # Leituras.Temperatura_13
        "TEMPERATURA_14":                       120 + 12764,                    # Leituras.Temperatura_14
        "TEMPERATURA_15":                       121 + 12764,                    # Leituras.Temperatura_15
        "TEMPERATURA_16":                       122 + 12764,                    # Leituras.Temperatura_16


        ## DISJUNTORES

        "DJ_01":                                0,
        "DJ_02":                                1,
        "DJ_03":                                2,
        "DJ_04":                                3,
        "DJ_05":                                4,
        "DJ_06":                                5,
        "DJ_07":                                6,
        "DJ_08":                                7,
        "DJ_09":                                8,
        "DJ_10":                                9,
        "DJ_11":                                10,
        "DJ_12":                                11,
        "DJ_13":                                12,
        "DJ_14":                                13,
        "DJ_15":                                14,
        "DJ_16":                                15,
        "DJ_17":                                16,
        "DJ_18":                                17,
        "DJ_19":                                18,
        "DJ_20":                                19,
        "DJ_21":                                20,
        "DJ_22":                                21,
        "DJ_23":                                22,
        "DJ_24":                                23,
        "DJ_25":                                24,
        "DJ_26":                                25,
        "DJ_27":                                26,
        "DJ_28":                                27,
        "DJ_29":                                28,
        "DJ_30":                                29,
        "DJ_31":                                30,
        "DJ_32":                                31,


        ## ALARMES

        # Específicos UG1
        "Alarme04_10":                          [4 + 14199, 10],
        "Alarme04_11":                          [4 + 14199, 11],
        "Alarme04_12":                          [4 + 14199, 12],

        "Alarme10_08":                          [10 + 14199, 8],
        "Alarme10_09":                          [10 + 14199, 9],

        "Alarme12_01":                          [12 + 14199, 1],
        "Alarme12_07":                          [12 + 14199, 7],
        "Alarme12_08":                          [12 + 14199, 8],
        "Alarme12_09":                          [12 + 14199, 9],
        "Alarme12_10":                          [12 + 14199, 10],
        "Alarme12_11":                          [12 + 14199, 11],
        "Alarme12_12":                          [12 + 14199, 12],
        "Alarme12_13":                          [12 + 14199, 13],

        "Alarme15_12":                          [15 + 14199, 12],
        "Alarme15_13":                          [15 + 14199, 13],

        # Gerais
        "Alarme01_01":                          [1 + 14199, 1],
        "Alarme01_02":                          [1 + 14199, 2],
        "Alarme01_00":                          [1 + 14199, 0],
        "Alarme01_03":                          [1 + 14199, 3],
        "Alarme01_06":                          [1 + 14199, 6],
        "Alarme01_07":                          [1 + 14199, 7],
        "Alarme01_08":                          [1 + 14199, 8],
        "Alarme01_09":                          [1 + 14199, 9],
        "Alarme01_10":                          [1 + 14199, 10],
        "Alarme01_11":                          [1 + 14199, 11],
        "Alarme01_12":                          [1 + 14199, 12],
        "Alarme01_13":                          [1 + 14199, 13],
        "Alarme01_14":                          [1 + 14199, 14],
        "Alarme01_15":                          [1 + 14199, 15],

        "Alarme02_00":                          [2 + 14199, 0],
        "Alarme02_01":                          [2 + 14199, 1],
        "Alarme02_02":                          [2 + 14199, 2],
        "Alarme02_03":                          [2 + 14199, 3],
        "Alarme02_04":                          [2 + 14199, 4],
        "Alarme02_05":                          [2 + 14199, 5],
        "Alarme02_06":                          [2 + 14199, 6],
        "Alarme02_07":                          [2 + 14199, 7],
        "Alarme02_08":                          [2 + 14199, 8],
        "Alarme02_09":                          [2 + 14199, 9],
        "Alarme02_10":                          [2 + 14199, 10],
        "Alarme02_11":                          [2 + 14199, 11],
        "Alarme02_12":                          [2 + 14199, 12],
        "Alarme02_13":                          [2 + 14199, 13],
        "Alarme02_14":                          [2 + 14199, 14],
        "Alarme02_15":                          [2 + 14199, 15],

        "Alarme03_00":                          [3 + 14199, 0],
        "Alarme03_01":                          [3 + 14199, 1],
        "Alarme03_02":                          [3 + 14199, 2],
        "Alarme03_03":                          [3 + 14199, 3],
        "Alarme03_04":                          [3 + 14199, 4],
        "Alarme03_05":                          [3 + 14199, 5],
        "Alarme03_06":                          [3 + 14199, 6],
        "Alarme03_07":                          [3 + 14199, 7],
        "Alarme03_08":                          [3 + 14199, 8],
        "Alarme03_09":                          [3 + 14199, 9],
        "Alarme03_10":                          [3 + 14199, 10],
        "Alarme03_11":                          [3 + 14199, 11],
        "Alarme03_12":                          [3 + 14199, 12],
        "Alarme03_13":                          [3 + 14199, 13],
        "Alarme03_14":                          [3 + 14199, 14],
        "Alarme03_15":                          [3 + 14199, 15],

        "Alarme04_00":                          [4 + 14199, 0],
        "Alarme04_01":                          [4 + 14199, 1],
        "Alarme04_02":                          [4 + 14199, 2],
        "Alarme04_04":                          [4 + 14199, 4],
        "Alarme04_05":                          [4 + 14199, 5],
        "Alarme04_06":                          [4 + 14199, 6],
        "Alarme04_07":                          [4 + 14199, 7],
        "Alarme04_09":                          [4 + 14199, 9],
        "Alarme04_10":                          [4 + 14199, 10],
        "Alarme04_11":                          [4 + 14199, 11],
        "Alarme04_12":                          [4 + 14199, 12],
        "Alarme04_13":                          [4 + 14199, 13],
        "Alarme04_14":                          [4 + 14199, 14],
        "Alarme04_15":                          [4 + 14199, 15],

        "Alarme05_00":                          [5 + 14199, 0],
        "Alarme05_02":                          [5 + 14199, 2],
        "Alarme05_03":                          [5 + 14199, 3],
        "Alarme05_04":                          [5 + 14199, 4],
        "Alarme05_05":                          [5 + 14199, 5],
        "Alarme05_06":                          [5 + 14199, 6],
        "Alarme05_07":                          [5 + 14199, 7],
        "Alarme05_09":                          [5 + 14199, 9],
        "Alarme05_10":                          [5 + 14199, 10],
        "Alarme05_11":                          [5 + 14199, 11],
        "Alarme05_12":                          [5 + 14199, 12],
        "Alarme05_13":                          [5 + 14199, 13],
        "Alarme05_14":                          [5 + 14199, 14],
        "Alarme05_15":                          [5 + 14199, 15],

        "Alarme06_00":                          [6 + 14199, 0],
        "Alarme06_03":                          [6 + 14199, 3],
        "Alarme06_04":                          [6 + 14199, 4],
        "Alarme06_05":                          [6 + 14199, 5],
        "Alarme06_08":                          [6 + 14199, 8],
        "Alarme06_09":                          [6 + 14199, 9],
        "Alarme06_10":                          [6 + 14199, 10],
        "Alarme06_11":                          [6 + 14199, 11],
        "Alarme06_12":                          [6 + 14199, 12],
        "Alarme06_13":                          [6 + 14199, 13],
        "Alarme06_14":                          [6 + 14199, 14],
        "Alarme06_15":                          [6 + 14199, 15],

        "Alarme07_00":                          [7 + 14199, 0],
        "Alarme07_01":                          [7 + 14199, 1],
        "Alarme07_02":                          [7 + 14199, 2],
        "Alarme07_03":                          [7 + 14199, 3],
        "Alarme07_06":                          [7 + 14199, 6],
        "Alarme07_07":                          [7 + 14199, 7],
        "Alarme07_08":                          [7 + 14199, 8],
        "Alarme07_09":                          [7 + 14199, 9],
        "Alarme07_10":                          [7 + 14199, 10],
        "Alarme07_11":                          [7 + 14199, 11],
        "Alarme07_12":                          [7 + 14199, 12],
        "Alarme07_13":                          [7 + 14199, 13],
        "Alarme07_14":                          [7 + 14199, 14],
        "Alarme07_15":                          [7 + 14199, 15],

        "Alarme08_00":                          [8 + 14199, 0],
        "Alarme08_01":                          [8 + 14199, 1],
        "Alarme08_02":                          [8 + 14199, 2],
        "Alarme08_03":                          [8 + 14199, 3],
        "Alarme08_07":                          [8 + 14199, 7],
        "Alarme08_08":                          [8 + 14199, 8],
        "Alarme08_09":                          [8 + 14199, 9],
        "Alarme08_10":                          [8 + 14199, 10],
        "Alarme08_11":                          [8 + 14199, 11],
        "Alarme08_12":                          [8 + 14199, 12],
        "Alarme08_13":                          [8 + 14199, 13],
        "Alarme08_14":                          [8 + 14199, 14],
        "Alarme08_15":                          [8 + 14199, 15],

        "Alarme09_00":                          [9 + 14199, 0],
        "Alarme09_01":                          [9 + 14199, 1],
        "Alarme09_02":                          [9 + 14199, 2],
        "Alarme09_03":                          [9 + 14199, 3],
        "Alarme09_04":                          [9 + 14199, 4],
        "Alarme09_06":                          [9 + 14199, 6],
        "Alarme09_07":                          [9 + 14199, 7],
        "Alarme09_08":                          [9 + 14199, 8],
        "Alarme09_09":                          [9 + 14199, 9],
        "Alarme09_10":                          [9 + 14199, 10],
        "Alarme09_11":                          [9 + 14199, 11],
        "Alarme09_12":                          [9 + 14199, 12],
        "Alarme09_13":                          [9 + 14199, 13],
        "Alarme09_14":                          [9 + 14199, 14],
        "Alarme09_15":                          [9 + 14199, 15],

        "Alarme10_00":                          [10 + 14199, 0],
        "Alarme10_01":                          [10 + 14199, 1],
        "Alarme10_02":                          [10 + 14199, 2],
        "Alarme10_03":                          [10 + 14199, 3],
        "Alarme10_05":                          [10 + 14199, 5],
        "Alarme10_06":                          [10 + 14199, 6],
        "Alarme10_07":                          [10 + 14199, 7],
        "Alarme10_08":                          [10 + 14199, 8],
        "Alarme10_09":                          [10 + 14199, 9],
        "Alarme10_10":                          [10 + 14199, 10],
        "Alarme10_11":                          [10 + 14199, 11],
        "Alarme10_12":                          [10 + 14199, 12],
        "Alarme10_13":                          [10 + 14199, 13],
        "Alarme10_14":                          [10 + 14199, 14],
        "Alarme10_15":                          [10 + 14199, 15],

        "Alarme11_00":                          [11 + 14199, 0],
        "Alarme11_01":                          [11 + 14199, 1],
        "Alarme11_02":                          [11 + 14199, 2],
        "Alarme11_06":                          [11 + 14199, 6],
        "Alarme11_07":                          [11 + 14199, 7],
        "Alarme11_08":                          [11 + 14199, 8],
        "Alarme11_09":                          [11 + 14199, 9],
        "Alarme11_10":                          [11 + 14199, 10],
        "Alarme11_11":                          [11 + 14199, 11],
        "Alarme11_12":                          [11 + 14199, 12],
        "Alarme11_13":                          [11 + 14199, 13],
        "Alarme11_14":                          [11 + 14199, 14],
        "Alarme11_15":                          [11 + 14199, 15],

        "Alarme12_01":                          [12 + 14199, 1],
        "Alarme12_02":                          [12 + 14199, 2],
        "Alarme12_03":                          [12 + 14199, 3],
        "Alarme12_04":                          [12 + 14199, 4],
        "Alarme12_05":                          [12 + 14199, 5],
        "Alarme12_06":                          [12 + 14199, 6],
        "Alarme12_07":                          [12 + 14199, 7],
        "Alarme12_09":                          [12 + 14199, 9],
        "Alarme12_10":                          [12 + 14199, 10],
        "Alarme12_11":                          [12 + 14199, 11],
        "Alarme12_12":                          [12 + 14199, 12],
        "Alarme12_13":                          [12 + 14199, 13],
        "Alarme12_14":                          [12 + 14199, 14],
        "Alarme12_15":                          [12 + 14199, 15],

        "Alarme13_00":                          [13 + 14199, 0],
        "Alarme13_01":                          [13 + 14199, 1],
        "Alarme13_02":                          [13 + 14199, 2],
        "Alarme13_03":                          [13 + 14199, 3],
        "Alarme13_09":                          [13 + 14199, 9],
        "Alarme13_10":                          [13 + 14199, 10],
        "Alarme13_11":                          [13 + 14199, 11],
        "Alarme13_12":                          [13 + 14199, 12],
        "Alarme13_13":                          [13 + 14199, 13],
        "Alarme13_14":                          [13 + 14199, 14],
        "Alarme13_15":                          [13 + 14199, 15],

        "Alarme14_00":                          [14 + 14199, 0],
        "Alarme14_01":                          [14 + 14199, 1],
        "Alarme14_02":                          [14 + 14199, 2],
        "Alarme14_03":                          [14 + 14199, 3],
        "Alarme14_04":                          [14 + 14199, 4],
        "Alarme14_05":                          [14 + 14199, 5],
        "Alarme14_10":                          [14 + 14199, 10],
        "Alarme14_11":                          [14 + 14199, 11],
        "Alarme14_12":                          [14 + 14199, 12],
        "Alarme14_13":                          [14 + 14199, 13],
        "Alarme14_14":                          [14 + 14199, 14],
        "Alarme14_15":                          [14 + 14199, 15],

        "Alarme15_00":                          [15 + 14199, 0],
        "Alarme15_01":                          [15 + 14199, 1],
        "Alarme15_02":                          [15 + 14199, 2],
        "Alarme15_03":                          [15 + 14199, 3],
        "Alarme15_04":                          [15 + 14199, 4],
        "Alarme15_05":                          [15 + 14199, 5],
        "Alarme15_06":                          [15 + 14199, 6],
        "Alarme15_07":                          [15 + 14199, 7],
        "Alarme15_08":                          [15 + 14199, 8],
        "Alarme15_09":                          [15 + 14199, 9],
        "Alarme15_10":                          [15 + 14199, 10],
        "Alarme15_12":                          [15 + 14199, 12],
        "Alarme15_13":                          [15 + 14199, 13],
        "Alarme15_14":                          [15 + 14199, 14],
        "Alarme15_15":                          [15 + 14199, 15],

        "Alarme16_00":                          [16 + 14199, 0],
        "Alarme16_01":                          [16 + 14199, 1],
        "Alarme16_02":                          [16 + 14199, 2],
        "Alarme16_03":                          [16 + 14199, 3],
        "Alarme16_04":                          [16 + 14199, 4],
        "Alarme16_05":                          [16 + 14199, 5],
        "Alarme16_06":                          [16 + 14199, 6],
        "Alarme16_07":                          [16 + 14199, 7],
        "Alarme16_08":                          [16 + 14199, 8],
        "Alarme16_09":                          [16 + 14199, 9],
        "Alarme16_10":                          [16 + 14199, 10],
        "Alarme16_11":                          [16 + 14199, 11],
        "Alarme16_12":                          [16 + 14199, 12],
    },
    "UG2": {
        ## COMANDOS
        # Gerais
        "CMD_RESET_ALARMES":                    0 + 12289,                      # Comandos.Operacao_PCH_AdoPopinhakResetAlarmes
        "CMD_RECONHECE_ALARMES":                1 + 12289,                      # Comandos.Operacao_PCH_AdoPopinhakReconheceAlarmes

        # Operação
        "CMD_OPER_UP":                          2 + 12289,                      # Comandos.Operacao_UP
        "CMD_OPER_UPGM":                        3 + 12289,                      # Comandos.Operacao_UPGM
        "CMD_OPER_UVD":                         4 + 12289,                      # Comandos.Operacao_UVD
        "CMD_OPER_UPS":                         5 + 12289,                      # Comandos.Operacao_UPS
        "CMD_OPER_US":                          6 + 12289,                      # Comandos.Operacao_US
        "CMD_OPER_EMERGENCIA_LIGAR":            7 + 12289,                      # Comandos.Operacao_EmergenciaLigar
        "CMD_OPER_EMERGENCIA_DESLIGAR":         8 + 12289,                      # Comandos.Operacao_EmergenciaDesligar
        "CMD_OPER_PARADA_RESET":                72 + 12289,                     # Comandos.Operacao_ParadaReset

        # Turbina
        "CMD_TURB_BYPASS_ABRIR":                9 + 12289,                      # Comandos.Turb_ByPassAbrir
        "CMD_TURB_BYPASS_FECHAR":               10 + 12289,                     # Comandos.Turb_ByPassFechar
        "CMD_TURB_BORBOLETA_ABRIR":             11 + 12289,                     # Comandos.Turb_BorboletaAbrir
        "CMD_TURB_BORBOLETA_FECHAR":            12 + 12289,                     # Comandos.Turb_BorboletaFechar
        "CMD_TURB_FRENAGEM_APLICAR":            13 + 12289,                     # Comandos.Turb_FrenagemAplicar
        "CMD_TURB_FRENAGEM_DESAPLICAR":         14 + 12289,                     # Comandos.Turb_FrenagemDesaplicar
        "CMD_TURB_FRENAGEM_MANUAL":             15 + 12289,                     # Comandos.Turb_FrenagemManual
        "CMD_TURB_FRENAGEM_AUTO":               16 + 12289,                     # Comandos.Turb_FrenagemAuto
        "CMD_TURB_SENSOR_ATIVAR":               17 + 12289,                     # Comandos.Turb_SensorAtivar
        "CMD_TURB_SENSOR_DESATIVAR":            18 + 12289,                     # Comandos.Turb_SensorDesativar

        # Reg V
        "CMD_REG_V_PARTIR":                     19 + 12289,                     # Comandos.RegV_Partir
        "CMD_REG_V_PARAR":                      20 + 12289,                     # Comandos.RegV_Parar
        "CMD_REG_V_COLOCAR_CARGA":              21 + 12289,                     # Comandos.RegV_ColocarCarga
        "CMD_REG_V_RETIRAR_CARGA":              22 + 12289,                     # Comandos.RegV_RetirarCarga
        "CMD_REG_V_INCREMENTA_VELOCIDADE":      23 + 12289,                     # Comandos.RegV_IncrementaVelocidade
        "CMD_REG_V_DECREMENTA_VELOCIDADE":      24 + 12289,                     # Comandos.RegV_DecrementaVelocidade
        "CMD_REG_V_SEL_MODO_ESTATISMO":         25 + 12289,                     # Comandos.RegV_SelecionaModoEstatismo
        "CMD_REG_V_SEL_MODO_BASECARGA":         26 + 12289,                     # Comandos.RegV_SelecionaModoBaseCarga

        # Reg T
        "CMD_REG_T_LIGAR":                      27 + 12289,                     # Comandos.RegT_Ligar
        "CMD_REG_T_DESLIGAR":                   28 + 12289,                     # Comandos.RegT_Desligar
        "CMD_REG_T_INCREMENTA_TENSAO":          29 + 12289,                     # Comandos.RegT_IncrementaTensao
        "CMD_REG_T_DECREMENTA_TENSAO":          30 + 12289,                     # Comandos.RegT_DecrementaTensao
        "CMD_REG_T_PRE_EXCITACAO":              31 + 12289,                     # Comandos.RegT_PreExcitacao

        # Sinc
        "CMD_SINC_LIGAR":                       32 + 12289,                     # Comandos.Sinc_Ligar
        "CMD_SINC_DESLIGAR":                    33 + 12289,                     # Comandos.Sinc_Desligar
        "CMD_SINC_MODO_AUTO_LIGAR":             34 + 12289,                     # Comandos.Sinc_ModoAutoLigar
        "CMD_SINC_MODO_MANUAL_LIGAR":           35 + 12289,                     # Comandos.Sinc_ModoManualLigar
        "CMD_SINC_MODO_BMORTA_LIGAR":           36 + 12289,                     # Comandos.Sinc_ModoBMortaLigar

        # DJ52G
        "CMD_DJ52G_ABRIR":                      37 + 12289,                     # Comandos.Disj52G_Abrir

        # Controle Reativo
        "CMD_CTRL_REATIVO_MODO_FPLIGAR":        38 + 12289,                     # Comandos.CtrlReativo_ModoFPLigar
        "CMD_CTRL_REATIVO_MODO_FPDESLIGAR":     39 + 12289,                     # Comandos.CtrlReativo_ModoFPDesligar
        "CMD_CTRL_REATIVO_MODO_VArLIGAR":       40 + 12289,                     # Comandos.CtrlReativo_ModoVArLigar
        "CMD_CTRL_REATIVO_MODO_VArDESLIGAR":    41 + 12289,                     # Comandos.CtrlReativo_ModoVArDesligar

        # Controle Potência
        "CMD_CTRL_POT_MODO_POT_LIGAR":          42 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaLigar
        "CMD_CTRL_POT_MODO_POT_DESLIGAR":       43 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaDesligar
        "CMD_CTRL_POT_MODO_NIVEL_LIGAR":        44 + 12289,                     # Comandos.CtrlPotencia_ModoNivelLigar
        "CMD_CTRL_POT_MODO_NIVEL_DESLIGAR":     45 + 12289,                     # Comandos.CtrlPotencia_ModoNivelDesligar
        "CMD_CTRL_POT_RELI_AUTO_LIGAR":         46 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoLigar
        "CMD_CTRL_POT_RELI_AUTO_DESLIGAR":      47 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoDesligar

        # UHCT
        "CMD_UHCT_BOMBA_01_LIGAR":              48 + 12289,                     # Comandos.UHCT_Bomba01Ligar
        "CMD_UHCT_BOMBA_01_DESLIGAR":           49 + 12289,                     # Comandos.UHCT_Bomba01Desligar
        "CMD_UHCT_BOMBA_01_PRINCIPAL":          50 + 12289,                     # Comandos.UHCT_Bomba01Principal
        "CMD_UHCT_BOMBA_02_LIGAR":              51 + 12289,                     # Comandos.UHCT_Bomba02Ligar
        "CMD_UHCT_BOMBA_02_DESLIGAR":           52 + 12289,                     # Comandos.UHCT_Bomba02Desligar
        "CMD_UHCT_BOMBA_02_PRINCIPAL":          53 + 12289,                     # Comandos.UHCT_Bomba02Principal
        "CMD_UHCT_BOMBA_AGUA_LIGAR":            54 + 12289,                     # Comandos.UHCT_BombaAguaLigar
        "CMD_UHCT_BOMBA_AGUA_DESLIGAR":         55 + 12289,                     # Comandos.UHCT_BombaAguaDesligar
        "CMD_UHCT_SENSOR_ATIVAR":               56 + 12289,                     # Comandos.UHCT_SensorAtivar
        "CMD_UHCT_SENSOR_DESATIVAR":            57 + 12289,                     # Comandos.UHCT_SensorDesativar
        "CMD_UHCT_RODIZIO_HABILITAR":           58 + 12289,                     # Comandos.UHCT_RodizioHabilitar
        "CMD_UHCT_RODIZIO_DESABILITAR":         59 + 12289,                     # Comandos.UHCT_RodizioDesabilitar

        # UHLM
        "CMD_UHLM_BOMBA_01_LIGAR":              60 + 12289,                     # Comandos.UHLM_Bomba01Ligar
        "CMD_UHLM_BOMBA_01_DESLIGAR":           61 + 12289,                     # Comandos.UHLM_Bomba01Desligar
        "CMD_UHLM_BOMBA_01_PRINCIPAL":          62 + 12289,                     # Comandos.UHLM_Bomba01Principal
        "CMD_UHLM_BOMBA_02_LIGAR":              63 + 12289,                     # Comandos.UHLM_Bomba02Ligar
        "CMD_UHLM_BOMBA_02_DESLIGAR":           64 + 12289,                     # Comandos.UHLM_Bomba02Desligar
        "CMD_UHLM_BOMBA_02_PRINCIPAL":          65 + 12289,                     # Comandos.UHLM_Bomba02Principal
        "CMD_UHLM_BOMBA_JACKING_LIGA":          66 + 12289,                     # Comandos.UHLM_BombaJackingLiga
        "CMD_UHLM_BOMBA_JACKING_DESLIGA":       67 + 12289,                     # Comandos.UHLM_BombaJackingDesliga
        "CMD_UHLM_BOMBA_AGUA_LIGA":             68 + 12289,                     # Comandos.UHLM_BombaAguaLiga
        "CMD_UHLM_BOMBA_AGUA_DESLIGA":          69 + 12289,                     # Comandos.UHLM_BombaAguaDesliga
        "CMD_UHLM_RODIZIO_HABILITAR":           70 + 12289,                     # Comandos.UHLM_RodizioHabilitar
        "CMD_UHLM_RODIZIO_DESABILITAR":         71 + 12289,                     # Comandos.UHLM_RodizioDesabilitar

        # RT
        "CMD_RT_MTVC_HABILITAR":                73 + 12289,                     # Comandos.RT_MTVC_Habilitar
        "CMD_RT_MECC_HABILITAR":                74 + 12289,                     # Comandos.RT_MECC_Habilitar
        "CMD_RT_ONLINE_HABILITAR":              75 + 12289,                     # Comandos.RT_Online_habilitar
        "CMD_RT_ONLINE_DESABILITAR":            76 + 12289,                     # Comandos.RT_Online_Desabiltar
        "CMD_RT_PARALELO_HABILITAR":            77 + 12289,                     # Comandos.RT_Paralelo_habilitar
        "CMD_RT_PARALELO_DESABILITAR":          78 + 12289,                     # Comandos.RT_Paralelo_Desabilitar

        # RV
        "CMD_RV_CONJUGADO_AUTO_HABILITAR":      79 + 12289,                     # Comandos.RV_ConjugadoAuto_habilitar
        "CMD_RV_CONJUGADO_MANUAL_HABILITAR":    80 + 12289,                     # Comandos.RV_ConjugadoManual_habilitar
        "CMD_RV_CONJUGADO_01_HABILITAR":        81 + 12289,                     # Comandos.RV_Conjugado01_habilitar
        "CMD_RV_CONJUGADO_02_HABILITAR":        82 + 12289,                     # Comandos.RV_Conjugado02_habilitar
        "CMD_RV_CONJUGADO_03_HABILITAR":        83 + 12289,                     # Comandos.RV_Conjugado03_habilitar
        "CMD_RV_CONJUGADO_04_HABILITAR":        84 + 12289,                     # Comandos.RV_Conjugado04_habilitar
        "CMD_RV_CONJUGADO_05_HABILITAR":        85 + 12289,                     # Comandos.RV_Conjugado05_habilitar


        ## SETPOINTS

        # UHCT
        "UHCT_PRESSAO_MAX":                     0 + 13569,                      # Setpoints.UHCT_PressaoMaxima
        "UHCT_PRESSAO_MIN":                     1 + 13569,                      # Setpoints.UHCT_PressaoMinima
        "UHCT_PRESSAO_DESLIGAMENTO":            2 + 13569,                      # Setpoints.UHCT_PressaoDesligamento
        "UHCT_PRESSAO_CRITICA":                 3 + 13569,                      # Setpoints.UHCT_PressaoCritica

        # Controle Potência
        "CRTL_POT_NIVEL_LL1":                   4 + 13569,                      # Setpoints.CtrlPotencia_NivelLL1
        "CRTL_POT_NIVEL_LL2":                   5 + 13569,                      # Setpoints.CtrlPotencia_NivelLL2
        "CRTL_POT_NIVEL_LL3":                   6 + 13569,                      # Setpoints.CtrlPotencia_NivelLL3
        "CRTL_POT_NIVEL_LL4":                   7 + 13569,                      # Setpoints.CtrlPotencia_NivelLL4
        "CRTL_POT_NIVEL_LL5":                   8 + 13569,                      # Setpoints.CtrlPotencia_NivelLL5
        "CRTL_POT_POT_1":                       9 + 13569,                      # Setpoints.CtrlPotencia_Potencia1
        "CRTL_POT_POT_2":                       10 + 13569,                     # Setpoints.CtrlPotencia_Potencia2
        "CRTL_POT_POT_3":                       11 + 13569,                     # Setpoints.CtrlPotencia_Potencia3
        "CRTL_POT_POT_4":                       12 + 13569,                     # Setpoints.CtrlPotencia_Potencia4
        "CRTL_POT_POT_5":                       13 + 13569,                     # Setpoints.CtrlPotencia_Potencia5
        "CRTL_POT_POT_MIN":                     14 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinima
        "CRTL_POT_POT_MIN_TEMPO":               15 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinimaTempo
        "CRTL_POT_NIVEL_RELIGAMENTO":           16 + 13569,                     # Setpoints.CtrlPotencia_NivelReligamento
        "CRTL_POT_ALVO":                        17 + 13569,                     # Setpoints.CtrlPotencia_Alvo
        "CRTL_POT_TOLERANCIA":                  18 + 13569,                     # Setpoints.CtrlPotencia_Tolerancia
        "CRTL_POT_PULSO_TEMPO":                 19 + 13569,                     # Setpoints.CtrlPotencia_PulsoTempo
        "CRTL_POT_PULSO_INTERVALO":             20 + 13569,                     # Setpoints.CtrlPotencia_PulsoIntervalo
        "CRTL_POT_SP_NIVEL":                    21 + 13569,                     # Setpoints.CtrlPotencia_SetpointNivel
        "CRTL_POT_NIVEL_MIN_ALARME":            22 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoAlarme
        "CRTL_POT_NIVEL_MIN_TRIP":              23 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoTRIP
        "CTRL_POT_POT_MAX":                     89 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMaxima

        # Controle Reativo
        "CRTL_REATIVO_SP_FP":                   24 + 13569,                     # Setpoints.CtrlReativo_SetpointFP
        "CRTL_REATIVO_SP_REATIVO":              25 + 13569,                     # Setpoints.CtrlReativo_SetpointReativo

        # Turbina
        "TURB_VIBRA_01_ALARME":                 26 + 13569,                     # Setpoints.Turb_Vibracao01Alarme
        "TURB_VIBRA_01_TRIP":                   27 + 13569,                     # Setpoints.Turb_Vibracao01TRIP
        "TURB_VIBRA_02_ALARME":                 28 + 13569,                     # Setpoints.Turb_Vibracao02Alarme
        "TURB_VIBRA_02_TRIP":                   29 + 13569,                     # Setpoints.Turb_Vibracao02TRIP
        "TURB_VIBRA_03_ALARME":                 30 + 13569,                     # Setpoints.Turb_Vibracao03Alarme
        "TURB_VIBRA_03_TRIP":                   31 + 13569,                     # Setpoints.Turb_Vibracao03TRIP
        "TURB_VIBRA_04_ALARME":                 32 + 13569,                     # Setpoints.Turb_Vibracao04Alarme
        "TURB_VIBRA_04_TRIP":                   33 + 13569,                     # Setpoints.Turb_Vibracao04TRIP
        "TURB_TEMPO_EQUALI_SP":                 34 + 13569,                     # Setpoints.Turb_TempoEqualizacaoSetpoint
        "TURB_VIBRA_05_ALARME":                 90 + 13569,                     # Setpoints.Turb_Vibracao05Alarme
        "TURB_VIBRA_05_TRIP":                   91 + 13569,                     # Setpoints.Turb_Vibracao05TRIP

        # Freio
        "FREIO_PULSO_INTERVALO":                35 + 13569,                     # Setpoints.Freio_PulsoIntervalo
        "FREIO_PULSO_TEMPO":                    36 + 13569,                     # Setpoints.Freio_PulsoTempo

        # UHCT
        "UHCT_RODIZIO_PRINCIPAL":               37 + 13569,                     # Setpoints.UHCT_RodizioPrincipal
        "UHCT_RODIZIO_RETAGUARDA":              38 + 13569,                     # Setpoints.UHCT_RodizioRetaguarda

        # UHLM
        "UHLM_RODIZIO_PRINCIPAL":               39 + 13569,                     # Setpoints.UHLM_RodizioPrincipal
        "UHLM_RODIZIO_RETAGUARDA":              40 + 13569,                     # Setpoints.UHLM_RodizioRetaguarda
        "UHLM_SP_VAZAO_01":                     92 + 13569,                     # Setpoints.UHLM_SetpointVazao01
        "UHLM_SP_VAZAO_02":                     93 + 13569,                     # Setpoints.UHLM_SetpointVazao02
        "UHLM_SP_VAZAO_03":                     94 + 13569,                     # Setpoints.UHLM_SetpointVazao03
        "UHLM_SP_VAZAO_04":                     95 + 13569,                     # Setpoints.UHLM_SetpointVazao04

        # Temperaturas
        "TEMPERATURA_01_ALARME":                41 + 13569,                     # Setpoints.Temperatura01_Alarme
        "TEMPERATURA_02_ALARME":                42 + 13569,                     # Setpoints.Temperatura02_Alarme
        "TEMPERATURA_03_ALARME":                43 + 13569,                     # Setpoints.Temperatura03_Alarme
        "TEMPERATURA_04_ALARME":                44 + 13569,                     # Setpoints.Temperatura04_Alarme
        "TEMPERATURA_05_ALARME":                45 + 13569,                     # Setpoints.Temperatura05_Alarme
        "TEMPERATURA_06_ALARME":                46 + 13569,                     # Setpoints.Temperatura06_Alarme
        "TEMPERATURA_07_ALARME":                47 + 13569,                     # Setpoints.Temperatura07_Alarme
        "TEMPERATURA_08_ALARME":                48 + 13569,                     # Setpoints.Temperatura08_Alarme
        "TEMPERATURA_09_ALARME":                49 + 13569,                     # Setpoints.Temperatura09_Alarme
        "TEMPERATURA_10_ALARME":                50 + 13569,                     # Setpoints.Temperatura10_Alarme
        "TEMPERATURA_11_ALARME":                51 + 13569,                     # Setpoints.Temperatura11_Alarme
        "TEMPERATURA_12_ALARME":                52 + 13569,                     # Setpoints.Temperatura12_Alarme
        "TEMPERATURA_13_ALARME":                53 + 13569,                     # Setpoints.Temperatura13_Alarme
        "TEMPERATURA_14_ALARME":                54 + 13569,                     # Setpoints.Temperatura14_Alarme
        "TEMPERATURA_15_ALARME":                55 + 13569,                     # Setpoints.Temperatura15_Alarme
        "TEMPERATURA_16_ALARME":                56 + 13569,                     # Setpoints.Temperatura16_Alarme
        "TEMPERATURA_01_TRIP01":                57 + 13569,                     # Setpoints.Temperatura01_TRIP01
        "TEMPERATURA_02_TRIP01":                58 + 13569,                     # Setpoints.Temperatura02_TRIP01
        "TEMPERATURA_03_TRIP01":                59 + 13569,                     # Setpoints.Temperatura03_TRIP01
        "TEMPERATURA_04_TRIP01":                60 + 13569,                     # Setpoints.Temperatura04_TRIP01
        "TEMPERATURA_05_TRIP01":                61 + 13569,                     # Setpoints.Temperatura05_TRIP01
        "TEMPERATURA_06_TRIP01":                62 + 13569,                     # Setpoints.Temperatura06_TRIP01
        "TEMPERATURA_07_TRIP01":                63 + 13569,                     # Setpoints.Temperatura07_TRIP01
        "TEMPERATURA_08_TRIP01":                64 + 13569,                     # Setpoints.Temperatura08_TRIP01
        "TEMPERATURA_09_TRIP01":                65 + 13569,                     # Setpoints.Temperatura09_TRIP01
        "TEMPERATURA_10_TRIP01":                66 + 13569,                     # Setpoints.Temperatura10_TRIP01
        "TEMPERATURA_11_TRIP01":                67 + 13569,                     # Setpoints.Temperatura11_TRIP01
        "TEMPERATURA_12_TRIP01":                68 + 13569,                     # Setpoints.Temperatura12_TRIP01
        "TEMPERATURA_13_TRIP01":                69 + 13569,                     # Setpoints.Temperatura13_TRIP01
        "TEMPERATURA_14_TRIP01":                70 + 13569,                     # Setpoints.Temperatura14_TRIP01
        "TEMPERATURA_15_TRIP01":                71 + 13569,                     # Setpoints.Temperatura15_TRIP01
        "TEMPERATURA_16_TRIP01":                72 + 13569,                     # Setpoints.Temperatura16_TRIP01
        "TEMPERATURA_01_TRIP02":                73 + 13569,                     # Setpoints.Temperatura01_TRIP02
        "TEMPERATURA_02_TRIP02":                74 + 13569,                     # Setpoints.Temperatura02_TRIP02
        "TEMPERATURA_03_TRIP02":                75 + 13569,                     # Setpoints.Temperatura03_TRIP02
        "TEMPERATURA_04_TRIP02":                76 + 13569,                     # Setpoints.Temperatura04_TRIP02
        "TEMPERATURA_05_TRIP02":                77 + 13569,                     # Setpoints.Temperatura05_TRIP02
        "TEMPERATURA_06_TRIP02":                78 + 13569,                     # Setpoints.Temperatura06_TRIP02
        "TEMPERATURA_07_TRIP02":                79 + 13569,                     # Setpoints.Temperatura07_TRIP02
        "TEMPERATURA_08_TRIP02":                80 + 13569,                     # Setpoints.Temperatura08_TRIP02
        "TEMPERATURA_09_TRIP02":                81 + 13569,                     # Setpoints.Temperatura09_TRIP02
        "TEMPERATURA_10_TRIP02":                82 + 13569,                     # Setpoints.Temperatura10_TRIP02
        "TEMPERATURA_11_TRIP02":                83 + 13569,                     # Setpoints.Temperatura11_TRIP02
        "TEMPERATURA_12_TRIP02":                84 + 13569,                     # Setpoints.Temperatura12_TRIP02
        "TEMPERATURA_13_TRIP02":                85 + 13569,                     # Setpoints.Temperatura13_TRIP02
        "TEMPERATURA_14_TRIP02":                86 + 13569,                     # Setpoints.Temperatura14_TRIP02
        "TEMPERATURA_15_TRIP02":                87 + 13569,                     # Setpoints.Temperatura15_TRIP02
        "TEMPERATURA_16_TRIP02":                88 + 13569,                     # Setpoints.Temperatura16_TRIP02

        # Grade Suja
        "GradeSuja_TRIP":                       96 + 13569,                     # Setpoints.GradeSuja_TRIP

        # Curva
        "CURVA_01_DISTRIB_P1":                  97 + 13569,                     # Setpoints.Curva01_DistribuidorP1
        "CURVA_01_DISTRIB_P2":                  98 + 13569,                     # Setpoints.Curva01_DistribuidorP2
        "CURVA_01_DISTRIB_P3":                  99 + 13569,                     # Setpoints.Curva01_DistribuidorP3
        "CURVA_01_DISTRIB_P4":                  100 + 13569,                    # Setpoints.Curva01_DistribuidorP4
        "CURVA_01_DISTRIB_P5":                  101 + 13569,                    # Setpoints.Curva01_DistribuidorP5
        "CURVA_01_DISTRIB_P6":                  102 + 13569,                    # Setpoints.Curva01_DistribuidorP6
        "CURVA_01_DISTRIB_P7":                  103 + 13569,                    # Setpoints.Curva01_DistribuidorP7
        "CURVA_01_DISTRIB_P8":                  104 + 13569,                    # Setpoints.Curva01_DistribuidorP8
        "CURVA_01_DISTRIB_P9":                  105 + 13569,                    # Setpoints.Curva01_DistribuidorP9
        "CURVA_01_DISTRIB_P10":                 106 + 13569,                    # Setpoints.Curva01_DistribuidorP10
        "CURVA_01_ROTOR_P1":                    107 + 13569,                    # Setpoints.Curva01_RotorP1
        "CURVA_01_ROTOR_P2":                    108 + 13569,                    # Setpoints.Curva01_RotorP2
        "CURVA_01_ROTOR_P3":                    109 + 13569,                    # Setpoints.Curva01_RotorP3
        "CURVA_01_ROTOR_P4":                    110 + 13569,                    # Setpoints.Curva01_RotorP4
        "CURVA_01_ROTOR_P5":                    111 + 13569,                    # Setpoints.Curva01_RotorP5
        "CURVA_01_ROTOR_P6":                    112 + 13569,                    # Setpoints.Curva01_RotorP6
        "CURVA_01_ROTOR_P7":                    113 + 13569,                    # Setpoints.Curva01_RotorP7
        "CURVA_01_ROTOR_P8":                    114 + 13569,                    # Setpoints.Curva01_RotorP8
        "CURVA_01_ROTOR_P9":                    115 + 13569,                    # Setpoints.Curva01_RotorP9
        "CURVA_01_ROTOR_P10":                   116 + 13569,                    # Setpoints.Curva01_RotorP10
        "CURVA_02_DISTRIB_P1":                  117 + 13569,                    # Setpoints.Curva02_DistribuidorP1
        "CURVA_02_DISTRIB_P2":                  118 + 13569,                    # Setpoints.Curva02_DistribuidorP2
        "CURVA_02_DISTRIB_P3":                  119 + 13569,                    # Setpoints.Curva02_DistribuidorP3
        "CURVA_02_DISTRIB_P4":                  120 + 13569,                    # Setpoints.Curva02_DistribuidorP4
        "CURVA_02_DISTRIB_P5":                  121 + 13569,                    # Setpoints.Curva02_DistribuidorP5
        "CURVA_02_DISTRIB_P6":                  122 + 13569,                    # Setpoints.Curva02_DistribuidorP6
        "CURVA_02_DISTRIB_P7":                  123 + 13569,                    # Setpoints.Curva02_DistribuidorP7
        "CURVA_02_DISTRIB_P8":                  124 + 13569,                    # Setpoints.Curva02_DistribuidorP8
        "CURVA_02_DISTRIB_P9":                  125 + 13569,                    # Setpoints.Curva02_DistribuidorP9
        "CURVA_02_DISTRIB_P10":                 126 + 13569,                    # Setpoints.Curva02_DistribuidorP10
        "CURVA_02_ROTOR_P1":                    127 + 13569,                    # Setpoints.Curva02_RotorP1
        "CURVA_02_ROTOR_P2":                    128 + 13569,                    # Setpoints.Curva02_RotorP2
        "CURVA_02_ROTOR_P3":                    129 + 13569,                    # Setpoints.Curva02_RotorP3
        "CURVA_02_ROTOR_P4":                    130 + 13569,                    # Setpoints.Curva02_RotorP4
        "CURVA_02_ROTOR_P5":                    131 + 13569,                    # Setpoints.Curva02_RotorP5
        "CURVA_02_ROTOR_P6":                    132 + 13569,                    # Setpoints.Curva02_RotorP6
        "CURVA_02_ROTOR_P7":                    133 + 13569,                    # Setpoints.Curva02_RotorP7
        "CURVA_02_ROTOR_P8":                    134 + 13569,                    # Setpoints.Curva02_RotorP8
        "CURVA_02_ROTOR_P9":                    135 + 13569,                    # Setpoints.Curva02_RotorP9
        "CURVA_02_ROTOR_P10":                   136 + 13569,                    # Setpoints.Curva02_RotorP10
        "CURVA_03_DISTRIB_P1":                  137 + 13569,                    # Setpoints.Curva03_DistribuidorP1
        "CURVA_03_DISTRIB_P2":                  138 + 13569,                    # Setpoints.Curva03_DistribuidorP2
        "CURVA_03_DISTRIB_P3":                  139 + 13569,                    # Setpoints.Curva03_DistribuidorP3
        "CURVA_03_DISTRIB_P4":                  140 + 13569,                    # Setpoints.Curva03_DistribuidorP4
        "CURVA_03_DISTRIB_P5":                  141 + 13569,                    # Setpoints.Curva03_DistribuidorP5
        "CURVA_03_DISTRIB_P6":                  142 + 13569,                    # Setpoints.Curva03_DistribuidorP6
        "CURVA_03_DISTRIB_P7":                  143 + 13569,                    # Setpoints.Curva03_DistribuidorP7
        "CURVA_03_DISTRIB_P8":                  144 + 13569,                    # Setpoints.Curva03_DistribuidorP8
        "CURVA_03_DISTRIB_P9":                  145 + 13569,                    # Setpoints.Curva03_DistribuidorP9
        "CURVA_03_DISTRIB_P10":                 146 + 13569,                    # Setpoints.Curva03_DistribuidorP10
        "CURVA_03_ROTOR_P1":                    147 + 13569,                    # Setpoints.Curva03_RotorP1
        "CURVA_03_ROTOR_P2":                    148 + 13569,                    # Setpoints.Curva03_RotorP2
        "CURVA_03_ROTOR_P3":                    149 + 13569,                    # Setpoints.Curva03_RotorP3
        "CURVA_03_ROTOR_P4":                    150 + 13569,                    # Setpoints.Curva03_RotorP4
        "CURVA_03_ROTOR_P5":                    151 + 13569,                    # Setpoints.Curva03_RotorP5
        "CURVA_03_ROTOR_P6":                    152 + 13569,                    # Setpoints.Curva03_RotorP6
        "CURVA_03_ROTOR_P7":                    153 + 13569,                    # Setpoints.Curva03_RotorP7
        "CURVA_03_ROTOR_P8":                    154 + 13569,                    # Setpoints.Curva03_RotorP8
        "CURVA_03_ROTOR_P9":                    155 + 13569,                    # Setpoints.Curva03_RotorP9
        "CURVA_03_ROTOR_P10":                   156 + 13569,                    # Setpoints.Curva03_RotorP10
        "CURVA_04_DISTRIB_P1":                  157 + 13569,                    # Setpoints.Curva04_DistribuidorP1
        "CURVA_04_DISTRIB_P2":                  158 + 13569,                    # Setpoints.Curva04_DistribuidorP2
        "CURVA_04_DISTRIB_P3":                  159 + 13569,                    # Setpoints.Curva04_DistribuidorP3
        "CURVA_04_DISTRIB_P4":                  160 + 13569,                    # Setpoints.Curva04_DistribuidorP4
        "CURVA_04_DISTRIB_P5":                  161 + 13569,                    # Setpoints.Curva04_DistribuidorP5
        "CURVA_04_DISTRIB_P6":                  162 + 13569,                    # Setpoints.Curva04_DistribuidorP6
        "CURVA_04_DISTRIB_P7":                  163 + 13569,                    # Setpoints.Curva04_DistribuidorP7
        "CURVA_04_DISTRIB_P8":                  164 + 13569,                    # Setpoints.Curva04_DistribuidorP8
        "CURVA_04_DISTRIB_P9":                  165 + 13569,                    # Setpoints.Curva04_DistribuidorP9
        "CURVA_04_DISTRIB_P10":                 166 + 13569,                    # Setpoints.Curva04_DistribuidorP10
        "CURVA_04_ROTOR_P1":                    167 + 13569,                    # Setpoints.Curva04_RotorP1
        "CURVA_04_ROTOR_P2":                    168 + 13569,                    # Setpoints.Curva04_RotorP2
        "CURVA_04_ROTOR_P3":                    169 + 13569,                    # Setpoints.Curva04_RotorP3
        "CURVA_04_ROTOR_P4":                    170 + 13569,                    # Setpoints.Curva04_RotorP4
        "CURVA_04_ROTOR_P5":                    171 + 13569,                    # Setpoints.Curva04_RotorP5
        "CURVA_04_ROTOR_P6":                    172 + 13569,                    # Setpoints.Curva04_RotorP6
        "CURVA_04_ROTOR_P7":                    173 + 13569,                    # Setpoints.Curva04_RotorP7
        "CURVA_04_ROTOR_P8":                    174 + 13569,                    # Setpoints.Curva04_RotorP8
        "CURVA_04_ROTOR_P9":                    175 + 13569,                    # Setpoints.Curva04_RotorP9
        "CURVA_04_ROTOR_P10":                   176 + 13569,                    # Setpoints.Curva04_RotorP10
        "CURVA_05_DISTRIB_P1":                  177 + 13569,                    # Setpoints.Curva05_DistribuidorP1
        "CURVA_05_DISTRIB_P2":                  178 + 13569,                    # Setpoints.Curva05_DistribuidorP2
        "CURVA_05_DISTRIB_P3":                  179 + 13569,                    # Setpoints.Curva05_DistribuidorP3
        "CURVA_05_DISTRIB_P4":                  180 + 13569,                    # Setpoints.Curva05_DistribuidorP4
        "CURVA_05_DISTRIB_P5":                  181 + 13569,                    # Setpoints.Curva05_DistribuidorP5
        "CURVA_05_DISTRIB_P6":                  182 + 13569,                    # Setpoints.Curva05_DistribuidorP6
        "CURVA_05_DISTRIB_P7":                  183 + 13569,                    # Setpoints.Curva05_DistribuidorP7
        "CURVA_05_DISTRIB_P8":                  184 + 13569,                    # Setpoints.Curva05_DistribuidorP8
        "CURVA_05_DISTRIB_P9":                  185 + 13569,                    # Setpoints.Curva05_DistribuidorP9
        "CURVA_05_DISTRIB_P10":                 186 + 13569,                    # Setpoints.Curva05_DistribuidorP10
        "CURVA_05_ROTOR_P1":                    187 + 13569,                    # Setpoints.Curva05_RotorP1
        "CURVA_05_ROTOR_P2":                    188 + 13569,                    # Setpoints.Curva05_RotorP2
        "CURVA_05_ROTOR_P3":                    189 + 13569,                    # Setpoints.Curva05_RotorP3
        "CURVA_05_ROTOR_P4":                    190 + 13569,                    # Setpoints.Curva05_RotorP4
        "CURVA_05_ROTOR_P5":                    191 + 13569,                    # Setpoints.Curva05_RotorP5
        "CURVA_05_ROTOR_P6":                    192 + 13569,                    # Setpoints.Curva05_RotorP6
        "CURVA_05_ROTOR_P7":                    193 + 13569,                    # Setpoints.Curva05_RotorP7
        "CURVA_05_ROTOR_P8":                    194 + 13569,                    # Setpoints.Curva05_RotorP8
        "CURVA_05_ROTOR_P9":                    195 + 13569,                    # Setpoints.Curva05_RotorP9
        "CURVA_05_ROTOR_P10":                   196 + 13569,                    # Setpoints.Curva05_RotorP10

        # Referencia Curva
        "REFER_CURVA_01":                       197 + 13569,                    # Setpoints.ReferenciaCurva01
        "REFER_CURVA_02":                       198 + 13569,                    # Setpoints.ReferenciaCurva02
        "REFER_CURVA_03":                       199 + 13569,                    # Setpoints.ReferenciaCurva03
        "REFER_CURVA_04":                       200 + 13569,                    # Setpoints.ReferenciaCurva04
        "REFER_CURVA_05":                       201 + 13569,                    # Setpoints.ReferenciaCurva05

        # Outros
        "TEMPO_ATUALIZACAO":                    202 + 13569,                    # Setpoints.TempoAtualizacao
        "MODO_OPERACAO_RETENTIVO":              203 + 13569,                    # Setpoints.ModoOperacao_Retentivo
        "CURVA_SEL_RETENTIVO":                  204 + 13569,                    # Setpoints.CurvaSelecionada_Retentivo


        ## LEITURAS

        # Nível
        "NV_JUSANTE":                           2 + 12764,                      # Leituras.NivelJusante
        "NV_BARRAGEM":                          3 + 12764,                      # Leituras.NivelBarragem
        "NV_CANAL":                             4 + 12764,                      # Leituras.NivelCanal
        "NV_CAMARA_CARGA":                      5 + 12764,                      # Leituras.NivelCamaraCarga
        "QUEDA_BRUTA":                          131 + 12764,                    # Leituras.QuedaBruta

        # Operação
        "OPER_PAINEL_RESET_ALARMES":            [6 + 12764, 0],                 # Leituras.Operacao_PainelResetAlarmes
        "OPER_PAINEL_RECONHECE_ALARMES":        [7 + 12764, 1],                 # Leituras.Operacao_PainelReconheceAlarmes

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

        "OPER_INFO_PARADA":                     12 + 12764,                     # Leituras.Operacao_InfoParada
        "OPER_INFO_PARADA_NORMAL":              [12 + 12764, 0],                # Operacao.InfoParada.Normal
        "OPER_INFO_PARADA_EMERG":               [12 + 12764, 1],                # Operacao.InfoParada.Emergencia
        "OPER_INFO_PARADA_TRIP_AGUA":           [12 + 12764, 2],                # Operacao.InfoParada.TRIPAgua
        "OPER_INFO_PARADA_TRIP_M":              [12 + 12764, 3],                # Operacao.InfoParada.TRIPMecanico
        "OPER_INFO_PARADA_TRIP_E":              [12 + 12764, 4],                # Operacao.InfoParada.TRIPEletrico
        "OPER_INFO_PARADA_TRIP_H":              [12 + 12764, 5],                # Operacao.InfoParada.TRIPHidraulico
        "OPER_INFO_PARADA_RELIG_AUTO":          [12 + 12764, 6],                # Operacao.InfoParada.ReligamentoAutomatico
        "OPER_INFO_PARADA_PARTIDA_MANU":        [12 + 12764, 7],                # Operacao.InfoParada.PartidaManual
        "OPER_INFO_PARADA_INFO_INVAL":          [12 + 12764, 15],               # Operacao.InfoParada.ParadaInfoValida

        # UHCT
        "UHCT_INFO":                            13 + 12764,                     # Leituras.UHCT_Info
        "UHCT_OPERACIONAL":                     [13 + 12764, 0],                # UHCT.Info.Operacional
        "UHCT_LIGADA":                          [13 + 12764, 1],                # UHCT.Info.Ligada
        "UHCT_SENS_DESATIVADO":                 [13 + 12764, 2],                # UHCT.Info.SensorDesativado
        "UHCT_MODO_LOCAL":                      [13 + 12764, 3],                # UHCT.Info.ModoLocal

        "UHCT_BOMBAS":                          14 + 12764,                     # Leituras.UHCT_Bombas
        "UHCT_BOMBAS01":                        [14 + 12764, 0],                # UHCT.Bombas.Bomba01
        "UHCT_BOMBAS02":                        [14 + 12764, 1],                # UHCT.Bombas.Bomba02
        "UHCT_BOMBAS03":                        [14 + 12764, 2],                # UHCT.Bombas.Bomba03

        "UHCT_RODIZIO":                         15 + 12764,                     # Leituras.UHCT_Rodizio
        "UHCT_RODIZ_HABILITADO":                [15 + 12764, 0],                # UHCT.Rodizio.RodizioHabilitado
        "UHCT_RODIZ_BOMBA01":                   [15 + 12764, 1],                # UHCT.Rodizio.Bomba01
        "UHCT_RODIZ_BOMBA02":                   [15 + 12764, 2],                # UHCT.Rodizio.Bomba02

        "UHCT_VALVULAS":                        16 + 12764,                     # Leituras.UHCT_Valvulas
        "UHCT_VALVULAS01":                      [16 + 12764, 0],                # UHCT.Valvulas.Valvulas01
        "UHCT_VALVULAS02":                      [16 + 12764, 1],                # UHCT.Valvulas.Valvulas02
        "UHCT_VALVULAS03":                      [16 + 12764, 2],                # UHCT.Valvulas.Valvulas03
        "UHCT_VALVULAS04":                      [16 + 12764, 3],                # UHCT.Valvulas.Valvulas04

        "UHCT_FILTROS":                         17 + 12764,                     # Leituras.UHCT_Filtros
        "UHCT_FILTROS01":                       [17 + 12764, 0],                # UHCT.Filtros.Filtro01
        "UHCT_FILTROS02":                       [17 + 12764, 1],                # UHCT.Filtros.Filtro02
        "UHCT_FILTROS03":                       [17 + 12764, 2],                # UHCT.Filtros.Filtro03
        "UHCT_FILTROS04":                       [17 + 12764, 3],                # UHCT.Filtros.Filtro04
        "UHCT_FILTROS05":                       [17 + 12764, 4],                # UHCT.Filtros.Filtro05

        "UHCT_PRESSOSTATOS":                    18 + 12764,                     # Leituras.UHCT_Pressostatos
        "UHCT_PRESSOSTATO01":                   [18 + 12764, 0],                # UHCT.Pressostatos.Pressostato01
        "UHCT_PRESSOSTATO02":                   [18 + 12764, 1],                # UHCT.Pressostatos.Pressostato02
        "UHCT_PRESSOSTATO03":                   [18 + 12764, 2],                # UHCT.Pressostatos.Pressostato03

        "UHCT_NIVEL_OLEO":                      19 + 12764,                     # Leituras.UHCT_NivelOleo
        "UHCT_NIVEL_OLEO_LL":                   [19 + 12764, 0],                # UHCT.NivelOleo.LL
        "UHCT_NIVEL_OLEO_L":                    [19 + 12764, 1],                # UHCT.NivelOleo.L
        "UHCT_NIVEL_OLEO_H":                    [19 + 12764, 2],                # UHCT.NivelOleo.H
        "UHCT_NIVEL_OLEO_HH":                   [19 + 12764, 3],                # UHCT.NivelOleo.HH

        "UHCT_PRESSAO_OLEO":                    20 + 12764,                     # Leituras.UHCT_PressaoOleo
        "UHCT_ACUM_RODIZIO_PRINCIPAL":          21 + 12764,                     # Leituras.UHCT_AcumuladorRodizioPrincipal
        "UHCT_ACUM_RODIZIO_RETAGUARDA":         22 + 12764,                     # Leituras.UHCT_AcumuladorRodizioRetaguarda

        # UHLM
        "UHLM_INFO":                            23 + 12764,                     # Leituras.UHLM_Info
        "UHLM_OPERACIONAL":                     [23 + 12764, 0],                # UHLM.Info.Operacional
        "UHLM_LIGADA":                          [23 + 12764, 1],                # UHLM.Info.Ligada
        "UHLM_MODO_LOCAL":                      [23 + 12764, 2],                # UHLM.Info.ModoLocal
        "UHLM_VALV_BOMBA_MECAN":                [23 + 12764, 3],                # UHLM.Info.UHLM_ValvulaBombaMecanica
        "UHLM_VALV_ENTRA_TRO_CALO_ABER":        [23 + 12764, 4],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Aberta
        "UHLM_VALV_ENTRA_TRO_CALO_FECH":        [23 + 12764, 5],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Fechada
        "UHLM_VALV_SAI_TRO_CALO_ABER":          [23 + 12764, 6],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Aberta
        "UHLM_VALV_SAI_TRO_CALO_FECH":          [23 + 12764, 7],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Fechada
        "UHLM_BOMBA_RETAG_OPERAC":              [23 + 12764, 8],                # UHLM.Info.UHLM_BombaRetaguarda_Operacional

        "UHLM_BOMBAS":                          24 + 12764,                     # Leituras.UHLM_Bombas
        "UHLM_BOMBA01":                         [24 + 12764, 0],                # UHLM.Bombas.Bomba01
        "UHLM_BOMBA02":                         [24 + 12764, 1],                # UHLM.Bombas.Bomba02
        "UHLM_BOMBA03":                         [24 + 12764, 2],                # UHLM.Bombas.Bomba03
        "UHLM_BOMBA04":                         [24 + 12764, 3],                # UHLM.Bombas.Bomba04

        "UHLM_RODIZIO":                         25 + 12764,                     # Leituras.UHLM_Rodizio
        "UHLM_RODIZ_HABILITADO":                [25 + 12764, 0],                # UHLM.Rodizio.RodizioHabilitado
        "UHLM_RODIZ_BOMBA01":                   [25 + 12764, 1],                # UHLM.Rodizio.Bomba01
        "UHLM_RODIZ_BOMBA02":                   [25 + 12764, 2],                # UHLM.Rodizio.Bomba02

        "UHLM_FILTROS":                         26 + 12764,                     # Leituras.UHLM_Filtros
        "UHLM_FILTRO01":                        [26 + 12764, 0],                # UHLM.Filtros.Filtro01
        "UHLM_FILTRO02":                        [26 + 12764, 1],                # UHLM.Filtros.Filtro02
        "UHLM_FILTRO03":                        [26 + 12764, 2],                # UHLM.Filtros.Filtro03
        "UHLM_FILTRO04":                        [26 + 12764, 3],                # UHLM.Filtros.Filtro04
        "UHLM_FILTRO05":                        [26 + 12764, 4],                # UHLM.Filtros.Filtro05

        "UHLM_PRESSOSTATOS":                    27 + 12764,                     # Leituras.UHLM_Pressostatos
        "UHLM_PRESSOSTATO01":                   [27 + 12764, 0],                # UHLM.Pressostatos.Pressostato01
        "UHLM_PRESSOSTATO02":                   [27 + 12764, 1],                # UHLM.Pressostatos.Pressostato02
        "UHLM_PRESSOSTATO03":                   [27 + 12764, 2],                # UHLM.Pressostatos.Pressostato03
        "UHLM_PRESSOSTATO04":                   [27 + 12764, 3],                # UHLM.Pressostatos.Pressostato04

        "UHLM_FLUXOSTATOS":                     28 + 12764,                     # Leituras.UHLM_Fluxostatos
        "UHLM_FLUXOSTATO01":                    [28 + 12764, 0],                # UHLM.Fluxostatos.Fluxostato01
        "UHLM_FLUXOSTATO02":                    [28 + 12764, 1],                # UHLM.Fluxostatos.Fluxostato02
        "UHLM_FLUXOSTATO03":                    [28 + 12764, 2],                # UHLM.Fluxostatos.Fluxostato03
        "UHLM_FLUXOSTATO04":                    [28 + 12764, 3],                # UHLM.Fluxostatos.Fluxostato04
        "UHLM_FLUXOSTATO05":                    [28 + 12764, 4],                # UHLM.Fluxostatos.Fluxostato05
        "UHLM_FLUXOSTATO06":                    [28 + 12764, 5],                # UHLM.Fluxostatos.Fluxostato06
        "UHLM_FLUXOSTATO07":                    [28 + 12764, 6],                # UHLM.Fluxostatos.Fluxostato07

        "UHLM_NIVEL_OLEO":                      29 + 12764,                     # Leituras.UHLM_NivelOleo
        "UHLM_NIVEL_OLEO_LL":                   [29 + 12764, 0],                # UHLM.NivelOleo.LL
        "UHLM_NIVEL_OLEO_L":                    [29 + 12764, 1],                # UHLM.NivelOleo.L
        "UHLM_NIVEL_OLEO_H":                    [29 + 12764, 2],                # UHLM.NivelOleo.H
        "UHLM_NIVEL_OLEO_HH":                   [29 + 12764, 3],                # UHLM.NivelOleo.HH

        "UHLM_ACUM_RODIZIO_PRINCIPAL":          30 + 12764,                     # Leituras.UHLM_AcumuladorRodizioPrincipal
        "UHLM_ACUM_RODIZIO_RETAGUARDA":         31 + 12764,                     # Leituras.UHLM_AcumuladorRodizioRetaguarda

        "UHLM_FLUXOSTATO_OLEO_01":              123 + 12764,                    # Leituras.UHLM_FluxostatoOleo01
        "UHLM_FLUXOSTATO_OLEO_02":              124 + 12764,                    # Leituras.UHLM_FluxostatoOleo02
        "UHLM_FLUXOSTATO_OLEO_03":              125 + 12764,                    # Leituras.UHLM_FluxostatoOleo03
        "UHLM_FLUXOSTATO_OLEO_04":              126 + 12764,                    # Leituras.UHLM_FluxostatoOleo04

        # Turbina
        "TURB_INFO":                            32 + 12764,                     # Leituras.Turb_Info
        "TURB_EQUALIZADA":                      [32 + 12764, 0],                # Turbina.Info.Equalizada
        "TURB_PRONTA":                          [32 + 12764, 1],                # Turbina.Info.Pronta
        "TURB_FECHADA":                         [32 + 12764, 2],                # Turbina.Info.Fechada
        "TURB_TRAVADA":                         [32 + 12764, 3],                # Turbina.Info.Travada
        "TURB_PARADA":                          [32 + 12764, 4],                # Turbina.Info.Parada
        "TURB_EQUALIZANDO":                     [32 + 12764, 5],                # Turbina.Info.Equalizando
        "TURB_FECHANDO":                        [32 + 12764, 6],                # Turbina.Info.Fechando
        "TURB_SENS_DESATIVADO":                 [32 + 12764, 7],                # Turbina.Info.SensorDesativado
        "TURB_DISTRI_FECHADO":                  [32 + 12764, 8],                # Turbina.Info.DistribuidorFechado

        "TURB_VALVULA_BYPASS":                  33 + 12764,                     # Leituras.Turb_ValvulaByPass
        "TURB_VALV_BY_ACIONA":                  [33 + 12764, 0],                # Turbina.Bypass.Acionamento
        "TURB_VALV_BY_FECHADO":                 [33 + 12764, 1],                # Turbina.Bypass.Fechado
        "TURB_VALV_BY_ABERTO":                  [33 + 12764, 2],                # Turbina.Bypass.Aberto

        "TURB_VALVULA_BORBOLETA":               34 + 12764,                     # Leituras.Turb_ValvulaBorboleta
        "TURB_VALV_BORB_ACIONA":                [34 + 12764, 0],                # Turbina.Borboleta.Acionamento
        "TURB_VALV_BORB_FECHADA":               [34 + 12764, 1],                # Turbina.Borboleta.Fechada
        "TURB_VALV_BORB_ABERTA":                [34 + 12764, 2],                # Turbina.Borboleta.Aberta
        "TURB_VALV_BORB_DERIVA":                [34 + 12764, 3],                # Turbina.Borboleta.Deriva
        "TURB_VALV_BORB_TRAVADA":               [34 + 12764, 4],                # Turbina.Borboleta.Travada
        "TURB_VALV_BORB_MANTEM":                [34 + 12764, 5],                # Turbina.Borboleta.Mantem

        "TURB_TEMPO_CRACK_EFETIVO":             35 + 12764,                     # Leituras.Turb_TempoCrackEfetivo
        "TURB_TEMPO_EQUAL_EFETIVO":             36 + 12764,                     # Leituras.Turb_TempoEqualizacaoEfetivo
        "TURB_PRESSAO_CONDUTO":                 37 + 12764,                     # Leituras.Turb_PressaoConduto
        "TURB_PRESSAO_CAIXA_ESPIRAL":           38 + 12764,                     # Leituras.Turb_PressaoCaixaEspiral
        "TURB_VAZAO_TURBINADA":                 39 + 12764,                     # Leituras.Turb_VazaoTurbinada
        "TURB_VIBRACAO_01":                     40 + 12764,                     # Leituras.Turb_Vibracao01
        "TURB_VIBRACAO_02":                     41 + 12764,                     # Leituras.Turb_Vibracao02
        "TURB_VIBRACAO_03":                     42 + 12764,                     # Leituras.Turb_Vibracao03
        "TURB_VIBRACAO_04":                     43 + 12764,                     # Leituras.Turb_Vibracao04

        "TURB_FRENAGEM":                        44 + 12764,                     # Leituras.Turb_Frenagem
        "TURB_FRENA_APLICADO":                  [44 + 12764, 0],                # Turbina.Frenagem.Info.Aplicado
        "TURB_FRENA_MANUAL":                    [44 + 12764, 1],                # Turbina.Frenagem.Info.Manual
        "TURB_FRENA_PRESSOS":                   [44 + 12764, 2],                # Turbina.Frenagem.Info.Pressostato
        "TURB_FRENA_1ZE":                       [44 + 12764, 3],                # Turbina.Frenagem.Info.[1ZE]
        "TURB_FRENA_2ZE":                       [44 + 12764, 4],                # Turbina.Frenagem.Info.[2ZE]

        "TURB_VIBRACAO_05":                     127 + 12764,                    # Leituras.Turb_Vibracao05

        # Reg V
        "REG_V_INFO":                           45 + 12764,                     # Leituras.RegV_Info
        "REG_V_HABILITADO":                     [45 + 12764, 0],                # RegV.Info.Habilitado
        "REG_V_BASE_CARGA":                     [45 + 12764, 1],                # RegV.Info.BaseCarga
        "REG_V_RPM30":                          [45 + 12764, 2],                # RegV.Info.RPM30
        "REG_V_RPM90":                          [45 + 12764, 3],                # RegV.Info.RPM90
        "REG_V_CARGA_ZERADA":                   [45 + 12764, 4],                # RegV.Info.CargaZerada
        "REG_V_MODO_ESTATISMO":                 [45 + 12764, 5],                # RegV.Info.ModoEstatismo
        "REG_V_MODO_BASE_CARGA":                [45 + 12764, 6],                # RegV.Info.ModoBaseCarga
        "REG_V_DISTRI_FECHADO":                 [45 + 12764, 7],                # RegV.Info.DistribuidorFechado

        "REG_V_ESTADO":                         46 + 12764,                     # Leituras.RegV_Estado
        "REG_V_FALHA":                          [46 + 12764, 0],                # RegV.Estado.Falha
        "REG_V_PARADO":                         [46 + 12764, 1],                # RegV.Estado.Parado
        "REG_V_CTRL_MANUAL_DISTRI":             [46 + 12764, 2],                # RegV.Estado.ControleManualDistribuidor
        "REG_V_CTRL_MANUAL_VALV":               [46 + 12764, 3],                # RegV.Estado.ControleManualValvula
        "REG_V_CTRL_VELOC":                     [46 + 12764, 4],                # RegV.Estado.ControleVelocidade
        "REG_V_COMPENSA_POT_ATIVA":             [46 + 12764, 5],                # RegV.Estado.CompensacaoPotenciaAtiva
        "REG_V_CTRL_POT_ATIVA":                 [46 + 12764, 6],                # RegV.Estado.ControlePotenciaAtiva

        "REG_V_VELOCIDADE":                     47 + 12764,                     # Leituras.RegV_Velocidade
        "REG_V_DISTRIBUIDOR":                   48 + 12764,                     # Leituras.RegV_Distribuidor
        "REG_V_ROTOR":                          49 + 12764,                     # Leituras.RegV_Rotor
        "REG_V_POT_ALVO":                       50 + 12764,                     # Leituras.RegV_PotenciaAlvo

        "REG_V_CONJUGADO_INFO":                 128 + 12764,                    # Leituras.RegV_CurvaConjugacao_Info
        "REG_V_CONJ_AUTOMATICO":                [128 + 12764, 0],               # RegV.Conjugado.Automatico
        "REG_V_CONJ_MANUAL":                    [128 + 12764, 1],               # RegV.Conjugado.Manual
        "REG_V_CONJUGADO1":                     [128 + 12764, 2],               # RegV.Conjugado.Conjugado1
        "REG_V_CONJUGADO2":                     [128 + 12764, 3],               # RegV.Conjugado.Conjugado2
        "REG_V_CONJUGADO3":                     [128 + 12764, 4],               # RegV.Conjugado.Conjugado3

        # Reg T
        "REG_T_INFO":                           51 + 12764,                     # Leituras.RegT_Info
        "REG_T_HABILITACAO":                    [51 + 12764, 0],                # RegT.Info.Habilitacao
        "REG_T_TENSAO_ESTAB":                   [51 + 12764, 1],                # RegT.Info.TensaoEstabilizada
        "REG_T_CONTATOR_ABERTO":                [51 + 12764, 2],                # RegT.Info.ContatorAberto
        "REG_T_CONTATOR_FECHADO":               [51 + 12764, 3],                # RegT.Info.ContatorFechado
        "REG_T_PRE_EXCITACAO":                  [51 + 12764, 4],                # RegT.Info.PreExcitacao
        "REG_T_MTVC":                           [51 + 12764, 5],                # RegT.Info.MTVC
        "REG_T_MECC":                           [51 + 12764, 6],                # RegT.Info.MECC
        "REG_T_OPER_ONLINE":                    [51 + 12764, 7],                # RegT.Info.OperacaoOnline
        "REG_T_OPER_PARALELA":                  [51 + 12764, 9],                # RegT.Info.OperacaoParalela

        "REG_T_UEXCITACAO":                     52 + 12764,                     # Leituras.RegT_UExcitacao
        "REG_T_IEXCITACAO":                     53 + 12764,                     # Leituras.RegT_IExcitacao
        "REG_T_FPALVO":                         129 + 12764,                    # Leituras.RegT_FPAlvo
        "REG_T_REATIVO_ALVO":                   130 + 12764,                    # Leituras.RegT_ReativoAlvo

        # Sinc
        "SINC_INFO":                            54 + 12764,                     # Leituras.Sinc_Info
        "SINC_HABILITADO":                      [54 + 12764, 0],                # Sincronoscopio.Info.Habilitado
        "SINC_MODO_AUTO":                       [54 + 12764, 1],                # Sincronoscopio.Info.ModoAutomatico
        "SINC_MODO_MANUAL":                     [54 + 12764, 2],                # Sincronoscopio.Info.ModoManual
        "SINC_BARRA_MORTA":                     [54 + 12764, 3],                # Sincronoscopio.Info.BarraMorta

        "SINC_FREQ_GERADOR":                    55 + 12764,                     # Leituras.Sinc_FrequenciaGerador
        "SINC_FREQ_BARRA":                      56 + 12764,                     # Leituras.Sinc_FrequenciaBarra
        "SINC_TENSAO_GERADOR":                  57 + 12764,                     # Leituras.Sinc_TensaoGerador
        "SINC_TENSAO_BARRA":                    58 + 12764,                     # Leituras.Sinc_TensaoBarra

        # DJ
        "Dj52G_INFO":                           59 + 12764,                     # Leituras.Disj52G_Info
        "Dj52G_ABERTO":                         [59 + 12764, 0],                # Disjuntor52G.Info.Aberto
        "Dj52G_FECHADO":                        [59 + 12764, 1],                # Disjuntor52G.Info.Fechado
        "Dj52G_INCONSISTENTE":                  [59 + 12764, 2],                # Disjuntor52G.Info.Inconsistente
        "Dj52G_TRIP":                           [59 + 12764, 3],                # Disjuntor52G.Info.TRIP
        "Dj52G_TESTE":                          [59 + 12764, 4],                # Disjuntor52G.Info.Teste
        "Dj52G_INSERIDO":                       [59 + 12764, 5],                # Disjuntor52G.Info.Inserido
        "Dj52G_EXTRAIVEL":                      [59 + 12764, 6],                # Disjuntor52G.Info.Extraivel
        "Dj52G_MOLA_CARRE":                     [59 + 12764, 7],                # Disjuntor52G.Info.MolaCarregada
        "Dj52G_CONDICAO":                       [59 + 12764, 8],                # Disjuntor52G.Info.CondicaoFechamento
        "Dj52G_FALTA_VCC":                      [59 + 12764, 9],                # Disjuntor52G.Info.FaltaVCC

        # Tensão
        "TENSAO_RN":                            60 + 12764,                     # Leituras.Gerador_TensaoRN
        "TENSAO_SN":                            61 + 12764,                     # Leituras.Gerador_TensaoSN
        "TENSAO_TN":                            62 + 12764,                     # Leituras.Gerador_TensaoTN
        "TENSAO_RS":                            63 + 12764,                     # Leituras.Gerador_TensaoRS
        "TENSAO_ST":                            64 + 12764,                     # Leituras.Gerador_TensaoST
        "TENSAO_TR":                            65 + 12764,                     # Leituras.Gerador_TensaoTR

        # Corrente
        "CORRENTE_R":                           66 + 12764,                     # Leituras.Gerador_CorrenteR
        "CORRENTE_S":                           67 + 12764,                     # Leituras.Gerador_CorrenteS
        "CORRENTE_T":                           68 + 12764,                     # Leituras.Gerador_CorrenteT
        "CORRENTE_MEDIA":                       69 + 12764,                     # Leituras.Gerador_CorrenteMedia

        # Potência Ativa
        "POT_ATIVA_1":                          70 + 12764,                     # Leituras.Gerador_PotenciaAtiva1
        "POT_ATIVA_2":                          71 + 12764,                     # Leituras.Gerador_PotenciaAtiva2
        "POT_ATIVA_3":                          72 + 12764,                     # Leituras.Gerador_PotenciaAtiva3
        "POT_ATIVA_MEDIA":                      73 + 12764,                     # Leituras.Gerador_PotenciaAtivaMedia

        # Potência Reativa
        "POT_REATIVA_1":                        74 + 12764,                     # Leituras.Gerador_PotenciaReativa1
        "POT_REATIVA_2":                        75 + 12764,                     # Leituras.Gerador_PotenciaReativa2
        "POT_REATIVA_3":                        76 + 12764,                     # Leituras.Gerador_PotenciaReativa3
        "POT_REATIVA_MEDIA":                    77 + 12764,                     # Leituras.Gerador_PotenciaReativaMedia

        # Potência Aparente
        "POT_APARENTE_1":                       78 + 12764,                     # Leituras.Gerador_PotenciaAparente1
        "POT_APARENTE_2":                       79 + 12764,                     # Leituras.Gerador_PotenciaAparente2
        "POT_APARENTE_3":                       80 + 12764,                     # Leituras.Gerador_PotenciaAparente3
        "POT_APARENTE_MEDIA":                   81 + 12764,                     # Leituras.Gerador_PotenciaAparenteMedia

        # Fator Potência
        "FATOR_POT_1":                          82 + 12764,                     # Leituras.Gerador_FatorPotencia1
        "FATOR_POT_2":                          83 + 12764,                     # Leituras.Gerador_FatorPotencia2
        "FATOR_POT_3":                          84 + 12764,                     # Leituras.Gerador_FatorPotencia3
        "FATOR_POT_MEDIA":                      85 + 12764,                     # Leituras.Gerador_FatorPotenciaMedia

        # Frequencia
        "FREQUENCIA":                           86 + 12764,                     # Leituras.Gerador_Frequencia

        # Energia Fornecida
        "ENERGIA_FORNECIDA_TWh":                87 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTWh
        "ENERGIA_FORNECIDA_GWh":                88 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGWh
        "ENERGIA_FORNECIDA_MWh":                89 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMWh
        "ENERGIA_FORNECIDA_kWh":                90 + 12764,                     # Leituras.Gerador_EnergiaFornecidakWh
        "ENERGIA_FORNECIDA_TVarh":              91 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTVarh
        "ENERGIA_FORNECIDA_GVarh":              92 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGVarh
        "ENERGIA_FORNECIDA_MVarh":              93 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMVarh
        "ENERGIA_FORNECIDA_kVarh":              94 + 12764,                     # Leituras.Gerador_EnergiaFornecidakVarh
        "ENERGIA_CORNECIDA_TVarh":              95 + 12764,                     # Leituras.Gerador_EnergiaConsumidaTVarh
        "ENERGIA_CORNECIDA_GVarh":              96 + 12764,                     # Leituras.Gerador_EnergiaConsumidaGVarh
        "ENERGIA_CORNECIDA_MVarh":              97 + 12764,                     # Leituras.Gerador_EnergiaConsumidaMVarh
        "ENERGIA_CORNECIDA_kVarh":              98 + 12764,                     # Leituras.Gerador_EnergiaConsumidakVarh
    
        "GERADOR_FP_INFO":                      99 + 12764,                     # Leituras.Gerador_FPInfo
        "GERADOR_FP_FASE1_IND":                 [99 + 12764, 0],                # Gerador.FP_Info.Fase1_Ind
        "GERADOR_FP_FASE1_CAP":                 [99 + 12764, 1],                # Gerador.FP_Info.Fase1_Cap
        "GERADOR_FP_FASE2_IND":                 [99 + 12764, 2],                # Gerador.FP_Info.Fase2_Ind
        "GERADOR_FP_FASE2_CAP":                 [99 + 12764, 3],                # Gerador.FP_Info.Fase2_Cap
        "GERADOR_FP_FASE3_IND":                 [99 + 12764, 4],                # Gerador.FP_Info.Fase3_Ind
        "GERADOR_FP_FASE3_CAP":                 [99 + 12764, 5],                # Gerador.FP_Info.Fase3_Cap
        "GERADOR_FP_FASE4_IND":                 [99 + 12764, 6],                # Gerador.FP_Info.Total_Ind
        "GERADOR_FP_FASE4_CAP":                 [99 + 12764, 7],                # Gerador.FP_Info.Total_Cap

        # Controles
        "CTRL_REATIVO_INFO":                    100 + 12764,                    # Leituras.CtrlReativo_Info
        "CTRL_REAT_MODO_FP":                    [100 + 12764, 0],               # CtrlReativo.Info.ModoFP
        "CTRL_REAT_MODO_VAR":                   [100 + 12764, 1],               # CtrlReativo.Info.ModoVar

        "CTRL_POTENCIA_INFO":                   101 + 12764,                    # Leituras.CtrlPotencia_Info
        "CTRL_POT_MODO_NIVEL":                  [101 + 12764, 0],               # CtrlPotencia.Info.ModoNivel
        "CTRL_POT_MODO_POT":                    [101 + 12764, 1],               # CtrlPotencia.Info.ModoPotencia
        "CTRL_POT_MODO_RELIGA_AUTO":            [101 + 12764, 2],               # CtrlPotencia.Info.ModoReligamentoAutomatico

        # Horimetros
        "HORIM_ELETR_LOW":                      102 + 12764,                    # Leituras.HorimetroEletrico_Low
        "HORIM_ELETR_HIGH":                     103 + 12764,                    # Leituras.HorimetroEletrico_High
        "HORIM_MECAN_LOW":                      104 + 12764,                    # Leituras.HorimetroMecanico_Low
        "HORIM_MECAN_HIGH":                     105 + 12764,                    # Leituras.HorimetroMecanico_High

        # Temperatura
        "TEMPERATURA_01":                       107 + 12764,                    # Leituras.Temperatura_01
        "TEMPERATURA_02":                       108 + 12764,                    # Leituras.Temperatura_02
        "TEMPERATURA_03":                       109 + 12764,                    # Leituras.Temperatura_03
        "TEMPERATURA_04":                       110 + 12764,                    # Leituras.Temperatura_04
        "TEMPERATURA_05":                       111 + 12764,                    # Leituras.Temperatura_05
        "TEMPERATURA_06":                       112 + 12764,                    # Leituras.Temperatura_06
        "TEMPERATURA_07":                       113 + 12764,                    # Leituras.Temperatura_07
        "TEMPERATURA_08":                       114 + 12764,                    # Leituras.Temperatura_08
        "TEMPERATURA_09":                       115 + 12764,                    # Leituras.Temperatura_09
        "TEMPERATURA_10":                       116 + 12764,                    # Leituras.Temperatura_10
        "TEMPERATURA_11":                       117 + 12764,                    # Leituras.Temperatura_11
        "TEMPERATURA_12":                       118 + 12764,                    # Leituras.Temperatura_12
        "TEMPERATURA_13":                       119 + 12764,                    # Leituras.Temperatura_13
        "TEMPERATURA_14":                       120 + 12764,                    # Leituras.Temperatura_14
        "TEMPERATURA_15":                       121 + 12764,                    # Leituras.Temperatura_15
        "TEMPERATURA_16":                       122 + 12764,                    # Leituras.Temperatura_16


        ## DISJUNTORES

        "DJ_01":                                0,
        "DJ_02":                                1,
        "DJ_03":                                2,
        "DJ_04":                                3,
        "DJ_05":                                4,
        "DJ_06":                                5,
        "DJ_07":                                6,
        "DJ_08":                                7,
        "DJ_09":                                8,
        "DJ_10":                                9,
        "DJ_11":                                10,
        "DJ_12":                                11,
        "DJ_13":                                12,
        "DJ_14":                                13,
        "DJ_15":                                14,
        "DJ_16":                                15,
        "DJ_17":                                16,
        "DJ_18":                                17,
        "DJ_19":                                18,
        "DJ_20":                                19,
        "DJ_21":                                20,
        "DJ_22":                                21,
        "DJ_23":                                22,
        "DJ_24":                                23,
        "DJ_25":                                24,
        "DJ_26":                                25,
        "DJ_27":                                26,
        "DJ_28":                                27,
        "DJ_29":                                28,
        "DJ_30":                                29,
        "DJ_31":                                30,
        "DJ_32":                                31,


        ## ALARMES

        # Específicos UG2
        "Alarme04_13":                          [4 + 14199, 13],
        "Alarme04_14":                          [4 + 14199, 14],
        "Alarme04_15":                          [4 + 14199, 15],

        "Alarme10_10":                          [10 + 14199, 10],
        "Alarme10_11":                          [10 + 14199, 11],

        "Alarme12_02":                          [12 + 14199, 2],
        "Alarme12_14":                          [12 + 14199, 14],
        "Alarme12_15":                          [12 + 14199, 15],

        "Alarme13_00":                          [13 + 14199, 0],
        "Alarme13_01":                          [13 + 14199, 1],
        "Alarme13_02":                          [13 + 14199, 2],
        "Alarme13_03":                          [13 + 14199, 3],
        "Alarme13_04":                          [13 + 14199, 4],

        "Alarme15_14":                          [15 + 14199, 14],
        "Alarme15_15":                          [15 + 14199, 15],

        # Gerais
        "Alarme01_01":                          [1 + 14199, 1],
        "Alarme01_02":                          [1 + 14199, 2],
        "Alarme01_00":                          [1 + 14199, 0],
        "Alarme01_03":                          [1 + 14199, 3],
        "Alarme01_06":                          [1 + 14199, 6],
        "Alarme01_07":                          [1 + 14199, 7],
        "Alarme01_08":                          [1 + 14199, 8],
        "Alarme01_09":                          [1 + 14199, 9],
        "Alarme01_10":                          [1 + 14199, 10],
        "Alarme01_11":                          [1 + 14199, 11],
        "Alarme01_12":                          [1 + 14199, 12],
        "Alarme01_13":                          [1 + 14199, 13],
        "Alarme01_14":                          [1 + 14199, 14],
        "Alarme01_15":                          [1 + 14199, 15],

        "Alarme02_00":                          [2 + 14199, 0],
        "Alarme02_01":                          [2 + 14199, 1],
        "Alarme02_02":                          [2 + 14199, 2],
        "Alarme02_03":                          [2 + 14199, 3],
        "Alarme02_04":                          [2 + 14199, 4],
        "Alarme02_05":                          [2 + 14199, 5],
        "Alarme02_06":                          [2 + 14199, 6],
        "Alarme02_07":                          [2 + 14199, 7],
        "Alarme02_08":                          [2 + 14199, 8],
        "Alarme02_09":                          [2 + 14199, 9],
        "Alarme02_10":                          [2 + 14199, 10],
        "Alarme02_11":                          [2 + 14199, 11],
        "Alarme02_12":                          [2 + 14199, 12],
        "Alarme02_13":                          [2 + 14199, 13],
        "Alarme02_14":                          [2 + 14199, 14],
        "Alarme02_15":                          [2 + 14199, 15],

        "Alarme03_00":                          [3 + 14199, 0],
        "Alarme03_01":                          [3 + 14199, 1],
        "Alarme03_02":                          [3 + 14199, 2],
        "Alarme03_03":                          [3 + 14199, 3],
        "Alarme03_04":                          [3 + 14199, 4],
        "Alarme03_05":                          [3 + 14199, 5],
        "Alarme03_06":                          [3 + 14199, 6],
        "Alarme03_07":                          [3 + 14199, 7],
        "Alarme03_08":                          [3 + 14199, 8],
        "Alarme03_09":                          [3 + 14199, 9],
        "Alarme03_10":                          [3 + 14199, 10],
        "Alarme03_11":                          [3 + 14199, 11],
        "Alarme03_12":                          [3 + 14199, 12],
        "Alarme03_13":                          [3 + 14199, 13],
        "Alarme03_14":                          [3 + 14199, 14],
        "Alarme03_15":                          [3 + 14199, 15],

        "Alarme04_00":                          [4 + 14199, 0],
        "Alarme04_01":                          [4 + 14199, 1],
        "Alarme04_02":                          [4 + 14199, 2],
        "Alarme04_04":                          [4 + 14199, 4],
        "Alarme04_05":                          [4 + 14199, 5],
        "Alarme04_06":                          [4 + 14199, 6],
        "Alarme04_07":                          [4 + 14199, 7],
        "Alarme04_09":                          [4 + 14199, 9],
        "Alarme04_10":                          [4 + 14199, 10],
        "Alarme04_11":                          [4 + 14199, 11],
        "Alarme04_12":                          [4 + 14199, 12],
        "Alarme04_13":                          [4 + 14199, 13],
        "Alarme04_14":                          [4 + 14199, 14],
        "Alarme04_15":                          [4 + 14199, 15],

        "Alarme05_00":                          [5 + 14199, 0],
        "Alarme05_02":                          [5 + 14199, 2],
        "Alarme05_03":                          [5 + 14199, 3],
        "Alarme05_04":                          [5 + 14199, 4],
        "Alarme05_05":                          [5 + 14199, 5],
        "Alarme05_06":                          [5 + 14199, 6],
        "Alarme05_07":                          [5 + 14199, 7],
        "Alarme05_09":                          [5 + 14199, 9],
        "Alarme05_10":                          [5 + 14199, 10],
        "Alarme05_11":                          [5 + 14199, 11],
        "Alarme05_12":                          [5 + 14199, 12],
        "Alarme05_13":                          [5 + 14199, 13],
        "Alarme05_14":                          [5 + 14199, 14],
        "Alarme05_15":                          [5 + 14199, 15],

        "Alarme06_00":                          [6 + 14199, 0],
        "Alarme06_03":                          [6 + 14199, 3],
        "Alarme06_04":                          [6 + 14199, 4],
        "Alarme06_05":                          [6 + 14199, 5],
        "Alarme06_08":                          [6 + 14199, 8],
        "Alarme06_09":                          [6 + 14199, 9],
        "Alarme06_10":                          [6 + 14199, 10],
        "Alarme06_11":                          [6 + 14199, 11],
        "Alarme06_12":                          [6 + 14199, 12],
        "Alarme06_13":                          [6 + 14199, 13],
        "Alarme06_14":                          [6 + 14199, 14],
        "Alarme06_15":                          [6 + 14199, 15],

        "Alarme07_00":                          [7 + 14199, 0],
        "Alarme07_01":                          [7 + 14199, 1],
        "Alarme07_02":                          [7 + 14199, 2],
        "Alarme07_03":                          [7 + 14199, 3],
        "Alarme07_06":                          [7 + 14199, 6],
        "Alarme07_07":                          [7 + 14199, 7],
        "Alarme07_08":                          [7 + 14199, 8],
        "Alarme07_09":                          [7 + 14199, 9],
        "Alarme07_10":                          [7 + 14199, 10],
        "Alarme07_11":                          [7 + 14199, 11],
        "Alarme07_12":                          [7 + 14199, 12],
        "Alarme07_13":                          [7 + 14199, 13],
        "Alarme07_14":                          [7 + 14199, 14],
        "Alarme07_15":                          [7 + 14199, 15],

        "Alarme08_00":                          [8 + 14199, 0],
        "Alarme08_01":                          [8 + 14199, 1],
        "Alarme08_02":                          [8 + 14199, 2],
        "Alarme08_03":                          [8 + 14199, 3],
        "Alarme08_07":                          [8 + 14199, 7],
        "Alarme08_08":                          [8 + 14199, 8],
        "Alarme08_09":                          [8 + 14199, 9],
        "Alarme08_10":                          [8 + 14199, 10],
        "Alarme08_11":                          [8 + 14199, 11],
        "Alarme08_12":                          [8 + 14199, 12],
        "Alarme08_13":                          [8 + 14199, 13],
        "Alarme08_14":                          [8 + 14199, 14],
        "Alarme08_15":                          [8 + 14199, 15],

        "Alarme09_00":                          [9 + 14199, 0],
        "Alarme09_01":                          [9 + 14199, 1],
        "Alarme09_02":                          [9 + 14199, 2],
        "Alarme09_03":                          [9 + 14199, 3],
        "Alarme09_04":                          [9 + 14199, 4],
        "Alarme09_06":                          [9 + 14199, 6],
        "Alarme09_07":                          [9 + 14199, 7],
        "Alarme09_08":                          [9 + 14199, 8],
        "Alarme09_09":                          [9 + 14199, 9],
        "Alarme09_10":                          [9 + 14199, 10],
        "Alarme09_11":                          [9 + 14199, 11],
        "Alarme09_12":                          [9 + 14199, 12],
        "Alarme09_13":                          [9 + 14199, 13],
        "Alarme09_14":                          [9 + 14199, 14],
        "Alarme09_15":                          [9 + 14199, 15],

        "Alarme10_00":                          [10 + 14199, 0],
        "Alarme10_01":                          [10 + 14199, 1],
        "Alarme10_02":                          [10 + 14199, 2],
        "Alarme10_03":                          [10 + 14199, 3],
        "Alarme10_05":                          [10 + 14199, 5],
        "Alarme10_06":                          [10 + 14199, 6],
        "Alarme10_07":                          [10 + 14199, 7],
        "Alarme10_08":                          [10 + 14199, 8],
        "Alarme10_09":                          [10 + 14199, 9],
        "Alarme10_10":                          [10 + 14199, 10],
        "Alarme10_11":                          [10 + 14199, 11],
        "Alarme10_12":                          [10 + 14199, 12],
        "Alarme10_13":                          [10 + 14199, 13],
        "Alarme10_14":                          [10 + 14199, 14],
        "Alarme10_15":                          [10 + 14199, 15],

        "Alarme11_00":                          [11 + 14199, 0],
        "Alarme11_01":                          [11 + 14199, 1],
        "Alarme11_02":                          [11 + 14199, 2],
        "Alarme11_06":                          [11 + 14199, 6],
        "Alarme11_07":                          [11 + 14199, 7],
        "Alarme11_08":                          [11 + 14199, 8],
        "Alarme11_09":                          [11 + 14199, 9],
        "Alarme11_10":                          [11 + 14199, 10],
        "Alarme11_11":                          [11 + 14199, 11],
        "Alarme11_12":                          [11 + 14199, 12],
        "Alarme11_13":                          [11 + 14199, 13],
        "Alarme11_14":                          [11 + 14199, 14],
        "Alarme11_15":                          [11 + 14199, 15],

        "Alarme12_01":                          [12 + 14199, 1],
        "Alarme12_02":                          [12 + 14199, 2],
        "Alarme12_03":                          [12 + 14199, 3],
        "Alarme12_04":                          [12 + 14199, 4],
        "Alarme12_05":                          [12 + 14199, 5],
        "Alarme12_06":                          [12 + 14199, 6],
        "Alarme12_07":                          [12 + 14199, 7],
        "Alarme12_09":                          [12 + 14199, 9],
        "Alarme12_10":                          [12 + 14199, 10],
        "Alarme12_11":                          [12 + 14199, 11],
        "Alarme12_12":                          [12 + 14199, 12],
        "Alarme12_13":                          [12 + 14199, 13],
        "Alarme12_14":                          [12 + 14199, 14],
        "Alarme12_15":                          [12 + 14199, 15],

        "Alarme13_00":                          [13 + 14199, 0],
        "Alarme13_01":                          [13 + 14199, 1],
        "Alarme13_02":                          [13 + 14199, 2],
        "Alarme13_03":                          [13 + 14199, 3],
        "Alarme13_09":                          [13 + 14199, 9],
        "Alarme13_10":                          [13 + 14199, 10],
        "Alarme13_11":                          [13 + 14199, 11],
        "Alarme13_12":                          [13 + 14199, 12],
        "Alarme13_13":                          [13 + 14199, 13],
        "Alarme13_14":                          [13 + 14199, 14],
        "Alarme13_15":                          [13 + 14199, 15],

        "Alarme14_00":                          [14 + 14199, 0],
        "Alarme14_01":                          [14 + 14199, 1],
        "Alarme14_02":                          [14 + 14199, 2],
        "Alarme14_03":                          [14 + 14199, 3],
        "Alarme14_04":                          [14 + 14199, 4],
        "Alarme14_05":                          [14 + 14199, 5],
        "Alarme14_10":                          [14 + 14199, 10],
        "Alarme14_11":                          [14 + 14199, 11],
        "Alarme14_12":                          [14 + 14199, 12],
        "Alarme14_13":                          [14 + 14199, 13],
        "Alarme14_14":                          [14 + 14199, 14],
        "Alarme14_15":                          [14 + 14199, 15],

        "Alarme15_00":                          [15 + 14199, 0],
        "Alarme15_01":                          [15 + 14199, 1],
        "Alarme15_02":                          [15 + 14199, 2],
        "Alarme15_03":                          [15 + 14199, 3],
        "Alarme15_04":                          [15 + 14199, 4],
        "Alarme15_05":                          [15 + 14199, 5],
        "Alarme15_06":                          [15 + 14199, 6],
        "Alarme15_07":                          [15 + 14199, 7],
        "Alarme15_08":                          [15 + 14199, 8],
        "Alarme15_09":                          [15 + 14199, 9],
        "Alarme15_10":                          [15 + 14199, 10],
        "Alarme15_12":                          [15 + 14199, 12],
        "Alarme15_13":                          [15 + 14199, 13],
        "Alarme15_14":                          [15 + 14199, 14],
        "Alarme15_15":                          [15 + 14199, 15],

        "Alarme16_00":                          [16 + 14199, 0],
        "Alarme16_01":                          [16 + 14199, 1],
        "Alarme16_02":                          [16 + 14199, 2],
        "Alarme16_03":                          [16 + 14199, 3],
        "Alarme16_04":                          [16 + 14199, 4],
        "Alarme16_05":                          [16 + 14199, 5],
        "Alarme16_06":                          [16 + 14199, 6],
        "Alarme16_07":                          [16 + 14199, 7],
        "Alarme16_08":                          [16 + 14199, 8],
        "Alarme16_09":                          [16 + 14199, 9],
        "Alarme16_10":                          [16 + 14199, 10],
        "Alarme16_11":                          [16 + 14199, 11],
        "Alarme16_12":                          [16 + 14199, 12],
    },
    "UG3": {
        ## COMANDOS
        # Gerais
        "CMD_RESET_ALARMES":                    0 + 12289,                      # Comandos.Operacao_PCH_AdoPopinhakResetAlarmes
        "CMD_RECONHECE_ALARMES":                1 + 12289,                      # Comandos.Operacao_PCH_AdoPopinhakReconheceAlarmes

        # Operação
        "CMD_OPER_UP":                          2 + 12289,                      # Comandos.Operacao_UP
        "CMD_OPER_UPGM":                        3 + 12289,                      # Comandos.Operacao_UPGM
        "CMD_OPER_UVD":                         4 + 12289,                      # Comandos.Operacao_UVD
        "CMD_OPER_UPS":                         5 + 12289,                      # Comandos.Operacao_UPS
        "CMD_OPER_US":                          6 + 12289,                      # Comandos.Operacao_US
        "CMD_OPER_EMERGENCIA_LIGAR":            7 + 12289,                      # Comandos.Operacao_EmergenciaLigar
        "CMD_OPER_EMERGENCIA_DESLIGAR":         8 + 12289,                      # Comandos.Operacao_EmergenciaDesligar
        "CMD_OPER_PARADA_RESET":                72 + 12289,                     # Comandos.Operacao_ParadaReset

        # Turbina
        "CMD_TURB_BYPASS_ABRIR":                9 + 12289,                      # Comandos.Turb_ByPassAbrir
        "CMD_TURB_BYPASS_FECHAR":               10 + 12289,                     # Comandos.Turb_ByPassFechar
        "CMD_TURB_BORBOLETA_ABRIR":             11 + 12289,                     # Comandos.Turb_BorboletaAbrir
        "CMD_TURB_BORBOLETA_FECHAR":            12 + 12289,                     # Comandos.Turb_BorboletaFechar
        "CMD_TURB_FRENAGEM_APLICAR":            13 + 12289,                     # Comandos.Turb_FrenagemAplicar
        "CMD_TURB_FRENAGEM_DESAPLICAR":         14 + 12289,                     # Comandos.Turb_FrenagemDesaplicar
        "CMD_TURB_FRENAGEM_MANUAL":             15 + 12289,                     # Comandos.Turb_FrenagemManual
        "CMD_TURB_FRENAGEM_AUTO":               16 + 12289,                     # Comandos.Turb_FrenagemAuto
        "CMD_TURB_SENSOR_ATIVAR":               17 + 12289,                     # Comandos.Turb_SensorAtivar
        "CMD_TURB_SENSOR_DESATIVAR":            18 + 12289,                     # Comandos.Turb_SensorDesativar

        # Reg V
        "CMD_REG_V_PARTIR":                     19 + 12289,                     # Comandos.RegV_Partir
        "CMD_REG_V_PARAR":                      20 + 12289,                     # Comandos.RegV_Parar
        "CMD_REG_V_COLOCAR_CARGA":              21 + 12289,                     # Comandos.RegV_ColocarCarga
        "CMD_REG_V_RETIRAR_CARGA":              22 + 12289,                     # Comandos.RegV_RetirarCarga
        "CMD_REG_V_INCREMENTA_VELOCIDADE":      23 + 12289,                     # Comandos.RegV_IncrementaVelocidade
        "CMD_REG_V_DECREMENTA_VELOCIDADE":      24 + 12289,                     # Comandos.RegV_DecrementaVelocidade
        "CMD_REG_V_SEL_MODO_ESTATISMO":         25 + 12289,                     # Comandos.RegV_SelecionaModoEstatismo
        "CMD_REG_V_SEL_MODO_BASECARGA":         26 + 12289,                     # Comandos.RegV_SelecionaModoBaseCarga

        # Reg T
        "CMD_REG_T_LIGAR":                      27 + 12289,                     # Comandos.RegT_Ligar
        "CMD_REG_T_DESLIGAR":                   28 + 12289,                     # Comandos.RegT_Desligar
        "CMD_REG_T_INCREMENTA_TENSAO":          29 + 12289,                     # Comandos.RegT_IncrementaTensao
        "CMD_REG_T_DECREMENTA_TENSAO":          30 + 12289,                     # Comandos.RegT_DecrementaTensao
        "CMD_REG_T_PRE_EXCITACAO":              31 + 12289,                     # Comandos.RegT_PreExcitacao

        # Sinc
        "CMD_SINC_LIGAR":                       32 + 12289,                     # Comandos.Sinc_Ligar
        "CMD_SINC_DESLIGAR":                    33 + 12289,                     # Comandos.Sinc_Desligar
        "CMD_SINC_MODO_AUTO_LIGAR":             34 + 12289,                     # Comandos.Sinc_ModoAutoLigar
        "CMD_SINC_MODO_MANUAL_LIGAR":           35 + 12289,                     # Comandos.Sinc_ModoManualLigar
        "CMD_SINC_MODO_BMORTA_LIGAR":           36 + 12289,                     # Comandos.Sinc_ModoBMortaLigar

        # DJ52G
        "CMD_DJ52G_ABRIR":                      37 + 12289,                     # Comandos.Disj52G_Abrir

        # Controle Reativo
        "CMD_CTRL_REATIVO_MODO_FPLIGAR":        38 + 12289,                     # Comandos.CtrlReativo_ModoFPLigar
        "CMD_CTRL_REATIVO_MODO_FPDESLIGAR":     39 + 12289,                     # Comandos.CtrlReativo_ModoFPDesligar
        "CMD_CTRL_REATIVO_MODO_VArLIGAR":       40 + 12289,                     # Comandos.CtrlReativo_ModoVArLigar
        "CMD_CTRL_REATIVO_MODO_VArDESLIGAR":    41 + 12289,                     # Comandos.CtrlReativo_ModoVArDesligar

        # Controle Potência
        "CMD_CTRL_POT_MODO_POT_LIGAR":          42 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaLigar
        "CMD_CTRL_POT_MODO_POT_DESLIGAR":       43 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaDesligar
        "CMD_CTRL_POT_MODO_NIVEL_LIGAR":        44 + 12289,                     # Comandos.CtrlPotencia_ModoNivelLigar
        "CMD_CTRL_POT_MODO_NIVEL_DESLIGAR":     45 + 12289,                     # Comandos.CtrlPotencia_ModoNivelDesligar
        "CMD_CTRL_POT_RELI_AUTO_LIGAR":         46 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoLigar
        "CMD_CTRL_POT_RELI_AUTO_DESLIGAR":      47 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoDesligar

        # UHCT
        "CMD_UHCT_BOMBA_01_LIGAR":              48 + 12289,                     # Comandos.UHCT_Bomba01Ligar
        "CMD_UHCT_BOMBA_01_DESLIGAR":           49 + 12289,                     # Comandos.UHCT_Bomba01Desligar
        "CMD_UHCT_BOMBA_01_PRINCIPAL":          50 + 12289,                     # Comandos.UHCT_Bomba01Principal
        "CMD_UHCT_BOMBA_02_LIGAR":              51 + 12289,                     # Comandos.UHCT_Bomba02Ligar
        "CMD_UHCT_BOMBA_02_DESLIGAR":           52 + 12289,                     # Comandos.UHCT_Bomba02Desligar
        "CMD_UHCT_BOMBA_02_PRINCIPAL":          53 + 12289,                     # Comandos.UHCT_Bomba02Principal
        "CMD_UHCT_BOMBA_AGUA_LIGAR":            54 + 12289,                     # Comandos.UHCT_BombaAguaLigar
        "CMD_UHCT_BOMBA_AGUA_DESLIGAR":         55 + 12289,                     # Comandos.UHCT_BombaAguaDesligar
        "CMD_UHCT_SENSOR_ATIVAR":               56 + 12289,                     # Comandos.UHCT_SensorAtivar
        "CMD_UHCT_SENSOR_DESATIVAR":            57 + 12289,                     # Comandos.UHCT_SensorDesativar
        "CMD_UHCT_RODIZIO_HABILITAR":           58 + 12289,                     # Comandos.UHCT_RodizioHabilitar
        "CMD_UHCT_RODIZIO_DESABILITAR":         59 + 12289,                     # Comandos.UHCT_RodizioDesabilitar

        # UHLM
        "CMD_UHLM_BOMBA_01_LIGAR":              60 + 12289,                     # Comandos.UHLM_Bomba01Ligar
        "CMD_UHLM_BOMBA_01_DESLIGAR":           61 + 12289,                     # Comandos.UHLM_Bomba01Desligar
        "CMD_UHLM_BOMBA_01_PRINCIPAL":          62 + 12289,                     # Comandos.UHLM_Bomba01Principal
        "CMD_UHLM_BOMBA_02_LIGAR":              63 + 12289,                     # Comandos.UHLM_Bomba02Ligar
        "CMD_UHLM_BOMBA_02_DESLIGAR":           64 + 12289,                     # Comandos.UHLM_Bomba02Desligar
        "CMD_UHLM_BOMBA_02_PRINCIPAL":          65 + 12289,                     # Comandos.UHLM_Bomba02Principal
        "CMD_UHLM_BOMBA_JACKING_LIGA":          66 + 12289,                     # Comandos.UHLM_BombaJackingLiga
        "CMD_UHLM_BOMBA_JACKING_DESLIGA":       67 + 12289,                     # Comandos.UHLM_BombaJackingDesliga
        "CMD_UHLM_BOMBA_AGUA_LIGA":             68 + 12289,                     # Comandos.UHLM_BombaAguaLiga
        "CMD_UHLM_BOMBA_AGUA_DESLIGA":          69 + 12289,                     # Comandos.UHLM_BombaAguaDesliga
        "CMD_UHLM_RODIZIO_HABILITAR":           70 + 12289,                     # Comandos.UHLM_RodizioHabilitar
        "CMD_UHLM_RODIZIO_DESABILITAR":         71 + 12289,                     # Comandos.UHLM_RodizioDesabilitar

        # RT
        "CMD_RT_MTVC_HABILITAR":                73 + 12289,                     # Comandos.RT_MTVC_Habilitar
        "CMD_RT_MECC_HABILITAR":                74 + 12289,                     # Comandos.RT_MECC_Habilitar
        "CMD_RT_ONLINE_HABILITAR":              75 + 12289,                     # Comandos.RT_Online_habilitar
        "CMD_RT_ONLINE_DESABILITAR":            76 + 12289,                     # Comandos.RT_Online_Desabiltar
        "CMD_RT_PARALELO_HABILITAR":            77 + 12289,                     # Comandos.RT_Paralelo_habilitar
        "CMD_RT_PARALELO_DESABILITAR":          78 + 12289,                     # Comandos.RT_Paralelo_Desabilitar

        # RV
        "CMD_RV_CONJUGADO_AUTO_HABILITAR":      79 + 12289,                     # Comandos.RV_ConjugadoAuto_habilitar
        "CMD_RV_CONJUGADO_MANUAL_HABILITAR":    80 + 12289,                     # Comandos.RV_ConjugadoManual_habilitar
        "CMD_RV_CONJUGADO_01_HABILITAR":        81 + 12289,                     # Comandos.RV_Conjugado01_habilitar
        "CMD_RV_CONJUGADO_02_HABILITAR":        82 + 12289,                     # Comandos.RV_Conjugado02_habilitar
        "CMD_RV_CONJUGADO_03_HABILITAR":        83 + 12289,                     # Comandos.RV_Conjugado03_habilitar
        "CMD_RV_CONJUGADO_04_HABILITAR":        84 + 12289,                     # Comandos.RV_Conjugado04_habilitar
        "CMD_RV_CONJUGADO_05_HABILITAR":        85 + 12289,                     # Comandos.RV_Conjugado05_habilitar


        ## SETPOINTS

        # UHCT
        "UHCT_PRESSAO_MAX":                     0 + 13569,                      # Setpoints.UHCT_PressaoMaxima
        "UHCT_PRESSAO_MIN":                     1 + 13569,                      # Setpoints.UHCT_PressaoMinima
        "UHCT_PRESSAO_DESLIGAMENTO":            2 + 13569,                      # Setpoints.UHCT_PressaoDesligamento
        "UHCT_PRESSAO_CRITICA":                 3 + 13569,                      # Setpoints.UHCT_PressaoCritica

        # Controle Potência
        "CRTL_POT_NIVEL_LL1":                   4 + 13569,                      # Setpoints.CtrlPotencia_NivelLL1
        "CRTL_POT_NIVEL_LL2":                   5 + 13569,                      # Setpoints.CtrlPotencia_NivelLL2
        "CRTL_POT_NIVEL_LL3":                   6 + 13569,                      # Setpoints.CtrlPotencia_NivelLL3
        "CRTL_POT_NIVEL_LL4":                   7 + 13569,                      # Setpoints.CtrlPotencia_NivelLL4
        "CRTL_POT_NIVEL_LL5":                   8 + 13569,                      # Setpoints.CtrlPotencia_NivelLL5
        "CRTL_POT_POT_1":                       9 + 13569,                      # Setpoints.CtrlPotencia_Potencia1
        "CRTL_POT_POT_2":                       10 + 13569,                     # Setpoints.CtrlPotencia_Potencia2
        "CRTL_POT_POT_3":                       11 + 13569,                     # Setpoints.CtrlPotencia_Potencia3
        "CRTL_POT_POT_4":                       12 + 13569,                     # Setpoints.CtrlPotencia_Potencia4
        "CRTL_POT_POT_5":                       13 + 13569,                     # Setpoints.CtrlPotencia_Potencia5
        "CRTL_POT_POT_MIN":                     14 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinima
        "CRTL_POT_POT_MIN_TEMPO":               15 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinimaTempo
        "CRTL_POT_NIVEL_RELIGAMENTO":           16 + 13569,                     # Setpoints.CtrlPotencia_NivelReligamento
        "CRTL_POT_ALVO":                        17 + 13569,                     # Setpoints.CtrlPotencia_Alvo
        "CRTL_POT_TOLERANCIA":                  18 + 13569,                     # Setpoints.CtrlPotencia_Tolerancia
        "CRTL_POT_PULSO_TEMPO":                 19 + 13569,                     # Setpoints.CtrlPotencia_PulsoTempo
        "CRTL_POT_PULSO_INTERVALO":             20 + 13569,                     # Setpoints.CtrlPotencia_PulsoIntervalo
        "CRTL_POT_SP_NIVEL":                    21 + 13569,                     # Setpoints.CtrlPotencia_SetpointNivel
        "CRTL_POT_NIVEL_MIN_ALARME":            22 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoAlarme
        "CRTL_POT_NIVEL_MIN_TRIP":              23 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoTRIP
        "CTRL_POT_POT_MAX":                     89 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMaxima

        # Controle Reativo
        "CRTL_REATIVO_SP_FP":                   24 + 13569,                     # Setpoints.CtrlReativo_SetpointFP
        "CRTL_REATIVO_SP_REATIVO":              25 + 13569,                     # Setpoints.CtrlReativo_SetpointReativo

        # Turbina
        "TURB_VIBRA_01_ALARME":                 26 + 13569,                     # Setpoints.Turb_Vibracao01Alarme
        "TURB_VIBRA_01_TRIP":                   27 + 13569,                     # Setpoints.Turb_Vibracao01TRIP
        "TURB_VIBRA_02_ALARME":                 28 + 13569,                     # Setpoints.Turb_Vibracao02Alarme
        "TURB_VIBRA_02_TRIP":                   29 + 13569,                     # Setpoints.Turb_Vibracao02TRIP
        "TURB_VIBRA_03_ALARME":                 30 + 13569,                     # Setpoints.Turb_Vibracao03Alarme
        "TURB_VIBRA_03_TRIP":                   31 + 13569,                     # Setpoints.Turb_Vibracao03TRIP
        "TURB_VIBRA_04_ALARME":                 32 + 13569,                     # Setpoints.Turb_Vibracao04Alarme
        "TURB_VIBRA_04_TRIP":                   33 + 13569,                     # Setpoints.Turb_Vibracao04TRIP
        "TURB_TEMPO_EQUALI_SP":                 34 + 13569,                     # Setpoints.Turb_TempoEqualizacaoSetpoint
        "TURB_VIBRA_05_ALARME":                 90 + 13569,                     # Setpoints.Turb_Vibracao05Alarme
        "TURB_VIBRA_05_TRIP":                   91 + 13569,                     # Setpoints.Turb_Vibracao05TRIP

        # Freio
        "FREIO_PULSO_INTERVALO":                35 + 13569,                     # Setpoints.Freio_PulsoIntervalo
        "FREIO_PULSO_TEMPO":                    36 + 13569,                     # Setpoints.Freio_PulsoTempo

        # UHCT
        "UHCT_RODIZIO_PRINCIPAL":               37 + 13569,                     # Setpoints.UHCT_RodizioPrincipal
        "UHCT_RODIZIO_RETAGUARDA":              38 + 13569,                     # Setpoints.UHCT_RodizioRetaguarda

        # UHLM
        "UHLM_RODIZIO_PRINCIPAL":               39 + 13569,                     # Setpoints.UHLM_RodizioPrincipal
        "UHLM_RODIZIO_RETAGUARDA":              40 + 13569,                     # Setpoints.UHLM_RodizioRetaguarda
        "UHLM_SP_VAZAO_01":                     92 + 13569,                     # Setpoints.UHLM_SetpointVazao01
        "UHLM_SP_VAZAO_02":                     93 + 13569,                     # Setpoints.UHLM_SetpointVazao02
        "UHLM_SP_VAZAO_03":                     94 + 13569,                     # Setpoints.UHLM_SetpointVazao03
        "UHLM_SP_VAZAO_04":                     95 + 13569,                     # Setpoints.UHLM_SetpointVazao04

        # Temperaturas
        "TEMPERATURA_01_ALARME":                41 + 13569,                     # Setpoints.Temperatura01_Alarme
        "TEMPERATURA_02_ALARME":                42 + 13569,                     # Setpoints.Temperatura02_Alarme
        "TEMPERATURA_03_ALARME":                43 + 13569,                     # Setpoints.Temperatura03_Alarme
        "TEMPERATURA_04_ALARME":                44 + 13569,                     # Setpoints.Temperatura04_Alarme
        "TEMPERATURA_05_ALARME":                45 + 13569,                     # Setpoints.Temperatura05_Alarme
        "TEMPERATURA_06_ALARME":                46 + 13569,                     # Setpoints.Temperatura06_Alarme
        "TEMPERATURA_07_ALARME":                47 + 13569,                     # Setpoints.Temperatura07_Alarme
        "TEMPERATURA_08_ALARME":                48 + 13569,                     # Setpoints.Temperatura08_Alarme
        "TEMPERATURA_09_ALARME":                49 + 13569,                     # Setpoints.Temperatura09_Alarme
        "TEMPERATURA_10_ALARME":                50 + 13569,                     # Setpoints.Temperatura10_Alarme
        "TEMPERATURA_11_ALARME":                51 + 13569,                     # Setpoints.Temperatura11_Alarme
        "TEMPERATURA_12_ALARME":                52 + 13569,                     # Setpoints.Temperatura12_Alarme
        "TEMPERATURA_13_ALARME":                53 + 13569,                     # Setpoints.Temperatura13_Alarme
        "TEMPERATURA_14_ALARME":                54 + 13569,                     # Setpoints.Temperatura14_Alarme
        "TEMPERATURA_15_ALARME":                55 + 13569,                     # Setpoints.Temperatura15_Alarme
        "TEMPERATURA_16_ALARME":                56 + 13569,                     # Setpoints.Temperatura16_Alarme
        "TEMPERATURA_01_TRIP01":                57 + 13569,                     # Setpoints.Temperatura01_TRIP01
        "TEMPERATURA_02_TRIP01":                58 + 13569,                     # Setpoints.Temperatura02_TRIP01
        "TEMPERATURA_03_TRIP01":                59 + 13569,                     # Setpoints.Temperatura03_TRIP01
        "TEMPERATURA_04_TRIP01":                60 + 13569,                     # Setpoints.Temperatura04_TRIP01
        "TEMPERATURA_05_TRIP01":                61 + 13569,                     # Setpoints.Temperatura05_TRIP01
        "TEMPERATURA_06_TRIP01":                62 + 13569,                     # Setpoints.Temperatura06_TRIP01
        "TEMPERATURA_07_TRIP01":                63 + 13569,                     # Setpoints.Temperatura07_TRIP01
        "TEMPERATURA_08_TRIP01":                64 + 13569,                     # Setpoints.Temperatura08_TRIP01
        "TEMPERATURA_09_TRIP01":                65 + 13569,                     # Setpoints.Temperatura09_TRIP01
        "TEMPERATURA_10_TRIP01":                66 + 13569,                     # Setpoints.Temperatura10_TRIP01
        "TEMPERATURA_11_TRIP01":                67 + 13569,                     # Setpoints.Temperatura11_TRIP01
        "TEMPERATURA_12_TRIP01":                68 + 13569,                     # Setpoints.Temperatura12_TRIP01
        "TEMPERATURA_13_TRIP01":                69 + 13569,                     # Setpoints.Temperatura13_TRIP01
        "TEMPERATURA_14_TRIP01":                70 + 13569,                     # Setpoints.Temperatura14_TRIP01
        "TEMPERATURA_15_TRIP01":                71 + 13569,                     # Setpoints.Temperatura15_TRIP01
        "TEMPERATURA_16_TRIP01":                72 + 13569,                     # Setpoints.Temperatura16_TRIP01
        "TEMPERATURA_01_TRIP02":                73 + 13569,                     # Setpoints.Temperatura01_TRIP02
        "TEMPERATURA_02_TRIP02":                74 + 13569,                     # Setpoints.Temperatura02_TRIP02
        "TEMPERATURA_03_TRIP02":                75 + 13569,                     # Setpoints.Temperatura03_TRIP02
        "TEMPERATURA_04_TRIP02":                76 + 13569,                     # Setpoints.Temperatura04_TRIP02
        "TEMPERATURA_05_TRIP02":                77 + 13569,                     # Setpoints.Temperatura05_TRIP02
        "TEMPERATURA_06_TRIP02":                78 + 13569,                     # Setpoints.Temperatura06_TRIP02
        "TEMPERATURA_07_TRIP02":                79 + 13569,                     # Setpoints.Temperatura07_TRIP02
        "TEMPERATURA_08_TRIP02":                80 + 13569,                     # Setpoints.Temperatura08_TRIP02
        "TEMPERATURA_09_TRIP02":                81 + 13569,                     # Setpoints.Temperatura09_TRIP02
        "TEMPERATURA_10_TRIP02":                82 + 13569,                     # Setpoints.Temperatura10_TRIP02
        "TEMPERATURA_11_TRIP02":                83 + 13569,                     # Setpoints.Temperatura11_TRIP02
        "TEMPERATURA_12_TRIP02":                84 + 13569,                     # Setpoints.Temperatura12_TRIP02
        "TEMPERATURA_13_TRIP02":                85 + 13569,                     # Setpoints.Temperatura13_TRIP02
        "TEMPERATURA_14_TRIP02":                86 + 13569,                     # Setpoints.Temperatura14_TRIP02
        "TEMPERATURA_15_TRIP02":                87 + 13569,                     # Setpoints.Temperatura15_TRIP02
        "TEMPERATURA_16_TRIP02":                88 + 13569,                     # Setpoints.Temperatura16_TRIP02

        # Grade Suja
        "GradeSuja_TRIP":                       96 + 13569,                     # Setpoints.GradeSuja_TRIP

        # Curva
        "CURVA_01_DISTRIB_P1":                  97 + 13569,                     # Setpoints.Curva01_DistribuidorP1
        "CURVA_01_DISTRIB_P2":                  98 + 13569,                     # Setpoints.Curva01_DistribuidorP2
        "CURVA_01_DISTRIB_P3":                  99 + 13569,                     # Setpoints.Curva01_DistribuidorP3
        "CURVA_01_DISTRIB_P4":                  100 + 13569,                    # Setpoints.Curva01_DistribuidorP4
        "CURVA_01_DISTRIB_P5":                  101 + 13569,                    # Setpoints.Curva01_DistribuidorP5
        "CURVA_01_DISTRIB_P6":                  102 + 13569,                    # Setpoints.Curva01_DistribuidorP6
        "CURVA_01_DISTRIB_P7":                  103 + 13569,                    # Setpoints.Curva01_DistribuidorP7
        "CURVA_01_DISTRIB_P8":                  104 + 13569,                    # Setpoints.Curva01_DistribuidorP8
        "CURVA_01_DISTRIB_P9":                  105 + 13569,                    # Setpoints.Curva01_DistribuidorP9
        "CURVA_01_DISTRIB_P10":                 106 + 13569,                    # Setpoints.Curva01_DistribuidorP10
        "CURVA_01_ROTOR_P1":                    107 + 13569,                    # Setpoints.Curva01_RotorP1
        "CURVA_01_ROTOR_P2":                    108 + 13569,                    # Setpoints.Curva01_RotorP2
        "CURVA_01_ROTOR_P3":                    109 + 13569,                    # Setpoints.Curva01_RotorP3
        "CURVA_01_ROTOR_P4":                    110 + 13569,                    # Setpoints.Curva01_RotorP4
        "CURVA_01_ROTOR_P5":                    111 + 13569,                    # Setpoints.Curva01_RotorP5
        "CURVA_01_ROTOR_P6":                    112 + 13569,                    # Setpoints.Curva01_RotorP6
        "CURVA_01_ROTOR_P7":                    113 + 13569,                    # Setpoints.Curva01_RotorP7
        "CURVA_01_ROTOR_P8":                    114 + 13569,                    # Setpoints.Curva01_RotorP8
        "CURVA_01_ROTOR_P9":                    115 + 13569,                    # Setpoints.Curva01_RotorP9
        "CURVA_01_ROTOR_P10":                   116 + 13569,                    # Setpoints.Curva01_RotorP10
        "CURVA_02_DISTRIB_P1":                  117 + 13569,                    # Setpoints.Curva02_DistribuidorP1
        "CURVA_02_DISTRIB_P2":                  118 + 13569,                    # Setpoints.Curva02_DistribuidorP2
        "CURVA_02_DISTRIB_P3":                  119 + 13569,                    # Setpoints.Curva02_DistribuidorP3
        "CURVA_02_DISTRIB_P4":                  120 + 13569,                    # Setpoints.Curva02_DistribuidorP4
        "CURVA_02_DISTRIB_P5":                  121 + 13569,                    # Setpoints.Curva02_DistribuidorP5
        "CURVA_02_DISTRIB_P6":                  122 + 13569,                    # Setpoints.Curva02_DistribuidorP6
        "CURVA_02_DISTRIB_P7":                  123 + 13569,                    # Setpoints.Curva02_DistribuidorP7
        "CURVA_02_DISTRIB_P8":                  124 + 13569,                    # Setpoints.Curva02_DistribuidorP8
        "CURVA_02_DISTRIB_P9":                  125 + 13569,                    # Setpoints.Curva02_DistribuidorP9
        "CURVA_02_DISTRIB_P10":                 126 + 13569,                    # Setpoints.Curva02_DistribuidorP10
        "CURVA_02_ROTOR_P1":                    127 + 13569,                    # Setpoints.Curva02_RotorP1
        "CURVA_02_ROTOR_P2":                    128 + 13569,                    # Setpoints.Curva02_RotorP2
        "CURVA_02_ROTOR_P3":                    129 + 13569,                    # Setpoints.Curva02_RotorP3
        "CURVA_02_ROTOR_P4":                    130 + 13569,                    # Setpoints.Curva02_RotorP4
        "CURVA_02_ROTOR_P5":                    131 + 13569,                    # Setpoints.Curva02_RotorP5
        "CURVA_02_ROTOR_P6":                    132 + 13569,                    # Setpoints.Curva02_RotorP6
        "CURVA_02_ROTOR_P7":                    133 + 13569,                    # Setpoints.Curva02_RotorP7
        "CURVA_02_ROTOR_P8":                    134 + 13569,                    # Setpoints.Curva02_RotorP8
        "CURVA_02_ROTOR_P9":                    135 + 13569,                    # Setpoints.Curva02_RotorP9
        "CURVA_02_ROTOR_P10":                   136 + 13569,                    # Setpoints.Curva02_RotorP10
        "CURVA_03_DISTRIB_P1":                  137 + 13569,                    # Setpoints.Curva03_DistribuidorP1
        "CURVA_03_DISTRIB_P2":                  138 + 13569,                    # Setpoints.Curva03_DistribuidorP2
        "CURVA_03_DISTRIB_P3":                  139 + 13569,                    # Setpoints.Curva03_DistribuidorP3
        "CURVA_03_DISTRIB_P4":                  140 + 13569,                    # Setpoints.Curva03_DistribuidorP4
        "CURVA_03_DISTRIB_P5":                  141 + 13569,                    # Setpoints.Curva03_DistribuidorP5
        "CURVA_03_DISTRIB_P6":                  142 + 13569,                    # Setpoints.Curva03_DistribuidorP6
        "CURVA_03_DISTRIB_P7":                  143 + 13569,                    # Setpoints.Curva03_DistribuidorP7
        "CURVA_03_DISTRIB_P8":                  144 + 13569,                    # Setpoints.Curva03_DistribuidorP8
        "CURVA_03_DISTRIB_P9":                  145 + 13569,                    # Setpoints.Curva03_DistribuidorP9
        "CURVA_03_DISTRIB_P10":                 146 + 13569,                    # Setpoints.Curva03_DistribuidorP10
        "CURVA_03_ROTOR_P1":                    147 + 13569,                    # Setpoints.Curva03_RotorP1
        "CURVA_03_ROTOR_P2":                    148 + 13569,                    # Setpoints.Curva03_RotorP2
        "CURVA_03_ROTOR_P3":                    149 + 13569,                    # Setpoints.Curva03_RotorP3
        "CURVA_03_ROTOR_P4":                    150 + 13569,                    # Setpoints.Curva03_RotorP4
        "CURVA_03_ROTOR_P5":                    151 + 13569,                    # Setpoints.Curva03_RotorP5
        "CURVA_03_ROTOR_P6":                    152 + 13569,                    # Setpoints.Curva03_RotorP6
        "CURVA_03_ROTOR_P7":                    153 + 13569,                    # Setpoints.Curva03_RotorP7
        "CURVA_03_ROTOR_P8":                    154 + 13569,                    # Setpoints.Curva03_RotorP8
        "CURVA_03_ROTOR_P9":                    155 + 13569,                    # Setpoints.Curva03_RotorP9
        "CURVA_03_ROTOR_P10":                   156 + 13569,                    # Setpoints.Curva03_RotorP10
        "CURVA_04_DISTRIB_P1":                  157 + 13569,                    # Setpoints.Curva04_DistribuidorP1
        "CURVA_04_DISTRIB_P2":                  158 + 13569,                    # Setpoints.Curva04_DistribuidorP2
        "CURVA_04_DISTRIB_P3":                  159 + 13569,                    # Setpoints.Curva04_DistribuidorP3
        "CURVA_04_DISTRIB_P4":                  160 + 13569,                    # Setpoints.Curva04_DistribuidorP4
        "CURVA_04_DISTRIB_P5":                  161 + 13569,                    # Setpoints.Curva04_DistribuidorP5
        "CURVA_04_DISTRIB_P6":                  162 + 13569,                    # Setpoints.Curva04_DistribuidorP6
        "CURVA_04_DISTRIB_P7":                  163 + 13569,                    # Setpoints.Curva04_DistribuidorP7
        "CURVA_04_DISTRIB_P8":                  164 + 13569,                    # Setpoints.Curva04_DistribuidorP8
        "CURVA_04_DISTRIB_P9":                  165 + 13569,                    # Setpoints.Curva04_DistribuidorP9
        "CURVA_04_DISTRIB_P10":                 166 + 13569,                    # Setpoints.Curva04_DistribuidorP10
        "CURVA_04_ROTOR_P1":                    167 + 13569,                    # Setpoints.Curva04_RotorP1
        "CURVA_04_ROTOR_P2":                    168 + 13569,                    # Setpoints.Curva04_RotorP2
        "CURVA_04_ROTOR_P3":                    169 + 13569,                    # Setpoints.Curva04_RotorP3
        "CURVA_04_ROTOR_P4":                    170 + 13569,                    # Setpoints.Curva04_RotorP4
        "CURVA_04_ROTOR_P5":                    171 + 13569,                    # Setpoints.Curva04_RotorP5
        "CURVA_04_ROTOR_P6":                    172 + 13569,                    # Setpoints.Curva04_RotorP6
        "CURVA_04_ROTOR_P7":                    173 + 13569,                    # Setpoints.Curva04_RotorP7
        "CURVA_04_ROTOR_P8":                    174 + 13569,                    # Setpoints.Curva04_RotorP8
        "CURVA_04_ROTOR_P9":                    175 + 13569,                    # Setpoints.Curva04_RotorP9
        "CURVA_04_ROTOR_P10":                   176 + 13569,                    # Setpoints.Curva04_RotorP10
        "CURVA_05_DISTRIB_P1":                  177 + 13569,                    # Setpoints.Curva05_DistribuidorP1
        "CURVA_05_DISTRIB_P2":                  178 + 13569,                    # Setpoints.Curva05_DistribuidorP2
        "CURVA_05_DISTRIB_P3":                  179 + 13569,                    # Setpoints.Curva05_DistribuidorP3
        "CURVA_05_DISTRIB_P4":                  180 + 13569,                    # Setpoints.Curva05_DistribuidorP4
        "CURVA_05_DISTRIB_P5":                  181 + 13569,                    # Setpoints.Curva05_DistribuidorP5
        "CURVA_05_DISTRIB_P6":                  182 + 13569,                    # Setpoints.Curva05_DistribuidorP6
        "CURVA_05_DISTRIB_P7":                  183 + 13569,                    # Setpoints.Curva05_DistribuidorP7
        "CURVA_05_DISTRIB_P8":                  184 + 13569,                    # Setpoints.Curva05_DistribuidorP8
        "CURVA_05_DISTRIB_P9":                  185 + 13569,                    # Setpoints.Curva05_DistribuidorP9
        "CURVA_05_DISTRIB_P10":                 186 + 13569,                    # Setpoints.Curva05_DistribuidorP10
        "CURVA_05_ROTOR_P1":                    187 + 13569,                    # Setpoints.Curva05_RotorP1
        "CURVA_05_ROTOR_P2":                    188 + 13569,                    # Setpoints.Curva05_RotorP2
        "CURVA_05_ROTOR_P3":                    189 + 13569,                    # Setpoints.Curva05_RotorP3
        "CURVA_05_ROTOR_P4":                    190 + 13569,                    # Setpoints.Curva05_RotorP4
        "CURVA_05_ROTOR_P5":                    191 + 13569,                    # Setpoints.Curva05_RotorP5
        "CURVA_05_ROTOR_P6":                    192 + 13569,                    # Setpoints.Curva05_RotorP6
        "CURVA_05_ROTOR_P7":                    193 + 13569,                    # Setpoints.Curva05_RotorP7
        "CURVA_05_ROTOR_P8":                    194 + 13569,                    # Setpoints.Curva05_RotorP8
        "CURVA_05_ROTOR_P9":                    195 + 13569,                    # Setpoints.Curva05_RotorP9
        "CURVA_05_ROTOR_P10":                   196 + 13569,                    # Setpoints.Curva05_RotorP10

        # Referencia Curva
        "REFER_CURVA_01":                       197 + 13569,                    # Setpoints.ReferenciaCurva01
        "REFER_CURVA_02":                       198 + 13569,                    # Setpoints.ReferenciaCurva02
        "REFER_CURVA_03":                       199 + 13569,                    # Setpoints.ReferenciaCurva03
        "REFER_CURVA_04":                       200 + 13569,                    # Setpoints.ReferenciaCurva04
        "REFER_CURVA_05":                       201 + 13569,                    # Setpoints.ReferenciaCurva05

        # Outros
        "TEMPO_ATUALIZACAO":                    202 + 13569,                    # Setpoints.TempoAtualizacao
        "MODO_OPERACAO_RETENTIVO":              203 + 13569,                    # Setpoints.ModoOperacao_Retentivo
        "CURVA_SEL_RETENTIVO":                  204 + 13569,                    # Setpoints.CurvaSelecionada_Retentivo


        ## LEITURAS

        # Nível
        "NV_JUSANTE":                           2 + 12764,                      # Leituras.NivelJusante
        "NV_BARRAGEM":                          3 + 12764,                      # Leituras.NivelBarragem
        "NV_CANAL":                             4 + 12764,                      # Leituras.NivelCanal
        "NV_CAMARA_CARGA":                      5 + 12764,                      # Leituras.NivelCamaraCarga
        "QUEDA_BRUTA":                          131 + 12764,                    # Leituras.QuedaBruta

        # Operação
        "OPER_PAINEL_RESET_ALARMES":            [6 + 12764, 0],                 # Leituras.Operacao_PainelResetAlarmes
        "OPER_PAINEL_RECONHECE_ALARMES":        [7 + 12764, 1],                 # Leituras.Operacao_PainelReconheceAlarmes

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

        "OPER_INFO_PARADA":                     12 + 12764,                     # Leituras.Operacao_InfoParada
        "OPER_INFO_PARADA_NORMAL":              [12 + 12764, 0],                # Operacao.InfoParada.Normal
        "OPER_INFO_PARADA_EMERG":               [12 + 12764, 1],                # Operacao.InfoParada.Emergencia
        "OPER_INFO_PARADA_TRIP_AGUA":           [12 + 12764, 2],                # Operacao.InfoParada.TRIPAgua
        "OPER_INFO_PARADA_TRIP_M":              [12 + 12764, 3],                # Operacao.InfoParada.TRIPMecanico
        "OPER_INFO_PARADA_TRIP_E":              [12 + 12764, 4],                # Operacao.InfoParada.TRIPEletrico
        "OPER_INFO_PARADA_TRIP_H":              [12 + 12764, 5],                # Operacao.InfoParada.TRIPHidraulico
        "OPER_INFO_PARADA_RELIG_AUTO":          [12 + 12764, 6],                # Operacao.InfoParada.ReligamentoAutomatico
        "OPER_INFO_PARADA_PARTIDA_MANU":        [12 + 12764, 7],                # Operacao.InfoParada.PartidaManual
        "OPER_INFO_PARADA_INFO_INVAL":          [12 + 12764, 15],               # Operacao.InfoParada.ParadaInfoValida

        # UHCT
        "UHCT_INFO":                            13 + 12764,                     # Leituras.UHCT_Info
        "UHCT_OPERACIONAL":                     [13 + 12764, 0],                # UHCT.Info.Operacional
        "UHCT_LIGADA":                          [13 + 12764, 1],                # UHCT.Info.Ligada
        "UHCT_SENS_DESATIVADO":                 [13 + 12764, 2],                # UHCT.Info.SensorDesativado
        "UHCT_MODO_LOCAL":                      [13 + 12764, 3],                # UHCT.Info.ModoLocal

        "UHCT_BOMBAS":                          14 + 12764,                     # Leituras.UHCT_Bombas
        "UHCT_BOMBAS01":                        [14 + 12764, 0],                # UHCT.Bombas.Bomba01
        "UHCT_BOMBAS02":                        [14 + 12764, 1],                # UHCT.Bombas.Bomba02
        "UHCT_BOMBAS03":                        [14 + 12764, 2],                # UHCT.Bombas.Bomba03

        "UHCT_RODIZIO":                         15 + 12764,                     # Leituras.UHCT_Rodizio
        "UHCT_RODIZ_HABILITADO":                [15 + 12764, 0],                # UHCT.Rodizio.RodizioHabilitado
        "UHCT_RODIZ_BOMBA01":                   [15 + 12764, 1],                # UHCT.Rodizio.Bomba01
        "UHCT_RODIZ_BOMBA02":                   [15 + 12764, 2],                # UHCT.Rodizio.Bomba02

        "UHCT_VALVULAS":                        16 + 12764,                     # Leituras.UHCT_Valvulas
        "UHCT_VALVULAS01":                      [16 + 12764, 0],                # UHCT.Valvulas.Valvulas01
        "UHCT_VALVULAS02":                      [16 + 12764, 1],                # UHCT.Valvulas.Valvulas02
        "UHCT_VALVULAS03":                      [16 + 12764, 2],                # UHCT.Valvulas.Valvulas03
        "UHCT_VALVULAS04":                      [16 + 12764, 3],                # UHCT.Valvulas.Valvulas04

        "UHCT_FILTROS":                         17 + 12764,                     # Leituras.UHCT_Filtros
        "UHCT_FILTROS01":                       [17 + 12764, 0],                # UHCT.Filtros.Filtro01
        "UHCT_FILTROS02":                       [17 + 12764, 1],                # UHCT.Filtros.Filtro02
        "UHCT_FILTROS03":                       [17 + 12764, 2],                # UHCT.Filtros.Filtro03
        "UHCT_FILTROS04":                       [17 + 12764, 3],                # UHCT.Filtros.Filtro04
        "UHCT_FILTROS05":                       [17 + 12764, 4],                # UHCT.Filtros.Filtro05

        "UHCT_PRESSOSTATOS":                    18 + 12764,                     # Leituras.UHCT_Pressostatos
        "UHCT_PRESSOSTATO01":                   [18 + 12764, 0],                # UHCT.Pressostatos.Pressostato01
        "UHCT_PRESSOSTATO02":                   [18 + 12764, 1],                # UHCT.Pressostatos.Pressostato02
        "UHCT_PRESSOSTATO03":                   [18 + 12764, 2],                # UHCT.Pressostatos.Pressostato03

        "UHCT_NIVEL_OLEO":                      19 + 12764,                     # Leituras.UHCT_NivelOleo
        "UHCT_NIVEL_OLEO_LL":                   [19 + 12764, 0],                # UHCT.NivelOleo.LL
        "UHCT_NIVEL_OLEO_L":                    [19 + 12764, 1],                # UHCT.NivelOleo.L
        "UHCT_NIVEL_OLEO_H":                    [19 + 12764, 2],                # UHCT.NivelOleo.H
        "UHCT_NIVEL_OLEO_HH":                   [19 + 12764, 3],                # UHCT.NivelOleo.HH

        "UHCT_PRESSAO_OLEO":                    20 + 12764,                     # Leituras.UHCT_PressaoOleo
        "UHCT_ACUM_RODIZIO_PRINCIPAL":          21 + 12764,                     # Leituras.UHCT_AcumuladorRodizioPrincipal
        "UHCT_ACUM_RODIZIO_RETAGUARDA":         22 + 12764,                     # Leituras.UHCT_AcumuladorRodizioRetaguarda

        # UHLM
        "UHLM_INFO":                            23 + 12764,                     # Leituras.UHLM_Info
        "UHLM_OPERACIONAL":                     [23 + 12764, 0],                # UHLM.Info.Operacional
        "UHLM_LIGADA":                          [23 + 12764, 1],                # UHLM.Info.Ligada
        "UHLM_MODO_LOCAL":                      [23 + 12764, 2],                # UHLM.Info.ModoLocal
        "UHLM_VALV_BOMBA_MECAN":                [23 + 12764, 3],                # UHLM.Info.UHLM_ValvulaBombaMecanica
        "UHLM_VALV_ENTRA_TRO_CALO_ABER":        [23 + 12764, 4],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Aberta
        "UHLM_VALV_ENTRA_TRO_CALO_FECH":        [23 + 12764, 5],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Fechada
        "UHLM_VALV_SAI_TRO_CALO_ABER":          [23 + 12764, 6],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Aberta
        "UHLM_VALV_SAI_TRO_CALO_FECH":          [23 + 12764, 7],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Fechada
        "UHLM_BOMBA_RETAG_OPERAC":              [23 + 12764, 8],                # UHLM.Info.UHLM_BombaRetaguarda_Operacional

        "UHLM_BOMBAS":                          24 + 12764,                     # Leituras.UHLM_Bombas
        "UHLM_BOMBA01":                         [24 + 12764, 0],                # UHLM.Bombas.Bomba01
        "UHLM_BOMBA02":                         [24 + 12764, 1],                # UHLM.Bombas.Bomba02
        "UHLM_BOMBA03":                         [24 + 12764, 2],                # UHLM.Bombas.Bomba03
        "UHLM_BOMBA04":                         [24 + 12764, 3],                # UHLM.Bombas.Bomba04

        "UHLM_RODIZIO":                         25 + 12764,                     # Leituras.UHLM_Rodizio
        "UHLM_RODIZ_HABILITADO":                [25 + 12764, 0],                # UHLM.Rodizio.RodizioHabilitado
        "UHLM_RODIZ_BOMBA01":                   [25 + 12764, 1],                # UHLM.Rodizio.Bomba01
        "UHLM_RODIZ_BOMBA02":                   [25 + 12764, 2],                # UHLM.Rodizio.Bomba02

        "UHLM_FILTROS":                         26 + 12764,                     # Leituras.UHLM_Filtros
        "UHLM_FILTRO01":                        [26 + 12764, 0],                # UHLM.Filtros.Filtro01
        "UHLM_FILTRO02":                        [26 + 12764, 1],                # UHLM.Filtros.Filtro02
        "UHLM_FILTRO03":                        [26 + 12764, 2],                # UHLM.Filtros.Filtro03
        "UHLM_FILTRO04":                        [26 + 12764, 3],                # UHLM.Filtros.Filtro04
        "UHLM_FILTRO05":                        [26 + 12764, 4],                # UHLM.Filtros.Filtro05

        "UHLM_PRESSOSTATOS":                    27 + 12764,                     # Leituras.UHLM_Pressostatos
        "UHLM_PRESSOSTATO01":                   [27 + 12764, 0],                # UHLM.Pressostatos.Pressostato01
        "UHLM_PRESSOSTATO02":                   [27 + 12764, 1],                # UHLM.Pressostatos.Pressostato02
        "UHLM_PRESSOSTATO03":                   [27 + 12764, 2],                # UHLM.Pressostatos.Pressostato03
        "UHLM_PRESSOSTATO04":                   [27 + 12764, 3],                # UHLM.Pressostatos.Pressostato04

        "UHLM_FLUXOSTATOS":                     28 + 12764,                     # Leituras.UHLM_Fluxostatos
        "UHLM_FLUXOSTATO01":                    [28 + 12764, 0],                # UHLM.Fluxostatos.Fluxostato01
        "UHLM_FLUXOSTATO02":                    [28 + 12764, 1],                # UHLM.Fluxostatos.Fluxostato02
        "UHLM_FLUXOSTATO03":                    [28 + 12764, 2],                # UHLM.Fluxostatos.Fluxostato03
        "UHLM_FLUXOSTATO04":                    [28 + 12764, 3],                # UHLM.Fluxostatos.Fluxostato04
        "UHLM_FLUXOSTATO05":                    [28 + 12764, 4],                # UHLM.Fluxostatos.Fluxostato05
        "UHLM_FLUXOSTATO06":                    [28 + 12764, 5],                # UHLM.Fluxostatos.Fluxostato06
        "UHLM_FLUXOSTATO07":                    [28 + 12764, 6],                # UHLM.Fluxostatos.Fluxostato07

        "UHLM_NIVEL_OLEO":                      29 + 12764,                     # Leituras.UHLM_NivelOleo
        "UHLM_NIVEL_OLEO_LL":                   [29 + 12764, 0],                # UHLM.NivelOleo.LL
        "UHLM_NIVEL_OLEO_L":                    [29 + 12764, 1],                # UHLM.NivelOleo.L
        "UHLM_NIVEL_OLEO_H":                    [29 + 12764, 2],                # UHLM.NivelOleo.H
        "UHLM_NIVEL_OLEO_HH":                   [29 + 12764, 3],                # UHLM.NivelOleo.HH

        "UHLM_ACUM_RODIZIO_PRINCIPAL":          30 + 12764,                     # Leituras.UHLM_AcumuladorRodizioPrincipal
        "UHLM_ACUM_RODIZIO_RETAGUARDA":         31 + 12764,                     # Leituras.UHLM_AcumuladorRodizioRetaguarda

        "UHLM_FLUXOSTATO_OLEO_01":              123 + 12764,                    # Leituras.UHLM_FluxostatoOleo01
        "UHLM_FLUXOSTATO_OLEO_02":              124 + 12764,                    # Leituras.UHLM_FluxostatoOleo02
        "UHLM_FLUXOSTATO_OLEO_03":              125 + 12764,                    # Leituras.UHLM_FluxostatoOleo03
        "UHLM_FLUXOSTATO_OLEO_04":              126 + 12764,                    # Leituras.UHLM_FluxostatoOleo04

        # Turbina
        "TURB_INFO":                            32 + 12764,                     # Leituras.Turb_Info
        "TURB_EQUALIZADA":                      [32 + 12764, 0],                # Turbina.Info.Equalizada
        "TURB_PRONTA":                          [32 + 12764, 1],                # Turbina.Info.Pronta
        "TURB_FECHADA":                         [32 + 12764, 2],                # Turbina.Info.Fechada
        "TURB_TRAVADA":                         [32 + 12764, 3],                # Turbina.Info.Travada
        "TURB_PARADA":                          [32 + 12764, 4],                # Turbina.Info.Parada
        "TURB_EQUALIZANDO":                     [32 + 12764, 5],                # Turbina.Info.Equalizando
        "TURB_FECHANDO":                        [32 + 12764, 6],                # Turbina.Info.Fechando
        "TURB_SENS_DESATIVADO":                 [32 + 12764, 7],                # Turbina.Info.SensorDesativado
        "TURB_DISTRI_FECHADO":                  [32 + 12764, 8],                # Turbina.Info.DistribuidorFechado

        "TURB_VALVULA_BYPASS":                  33 + 12764,                     # Leituras.Turb_ValvulaByPass
        "TURB_VALV_BY_ACIONA":                  [33 + 12764, 0],                # Turbina.Bypass.Acionamento
        "TURB_VALV_BY_FECHADO":                 [33 + 12764, 1],                # Turbina.Bypass.Fechado
        "TURB_VALV_BY_ABERTO":                  [33 + 12764, 2],                # Turbina.Bypass.Aberto

        "TURB_VALVULA_BORBOLETA":               34 + 12764,                     # Leituras.Turb_ValvulaBorboleta
        "TURB_VALV_BORB_ACIONA":                [34 + 12764, 0],                # Turbina.Borboleta.Acionamento
        "TURB_VALV_BORB_FECHADA":               [34 + 12764, 1],                # Turbina.Borboleta.Fechada
        "TURB_VALV_BORB_ABERTA":                [34 + 12764, 2],                # Turbina.Borboleta.Aberta
        "TURB_VALV_BORB_DERIVA":                [34 + 12764, 3],                # Turbina.Borboleta.Deriva
        "TURB_VALV_BORB_TRAVADA":               [34 + 12764, 4],                # Turbina.Borboleta.Travada
        "TURB_VALV_BORB_MANTEM":                [34 + 12764, 5],                # Turbina.Borboleta.Mantem

        "TURB_TEMPO_CRACK_EFETIVO":             35 + 12764,                     # Leituras.Turb_TempoCrackEfetivo
        "TURB_TEMPO_EQUAL_EFETIVO":             36 + 12764,                     # Leituras.Turb_TempoEqualizacaoEfetivo
        "TURB_PRESSAO_CONDUTO":                 37 + 12764,                     # Leituras.Turb_PressaoConduto
        "TURB_PRESSAO_CAIXA_ESPIRAL":           38 + 12764,                     # Leituras.Turb_PressaoCaixaEspiral
        "TURB_VAZAO_TURBINADA":                 39 + 12764,                     # Leituras.Turb_VazaoTurbinada
        "TURB_VIBRACAO_01":                     40 + 12764,                     # Leituras.Turb_Vibracao01
        "TURB_VIBRACAO_02":                     41 + 12764,                     # Leituras.Turb_Vibracao02
        "TURB_VIBRACAO_03":                     42 + 12764,                     # Leituras.Turb_Vibracao03
        "TURB_VIBRACAO_04":                     43 + 12764,                     # Leituras.Turb_Vibracao04

        "TURB_FRENAGEM":                        44 + 12764,                     # Leituras.Turb_Frenagem
        "TURB_FRENA_APLICADO":                  [44 + 12764, 0],                # Turbina.Frenagem.Info.Aplicado
        "TURB_FRENA_MANUAL":                    [44 + 12764, 1],                # Turbina.Frenagem.Info.Manual
        "TURB_FRENA_PRESSOS":                   [44 + 12764, 2],                # Turbina.Frenagem.Info.Pressostato
        "TURB_FRENA_1ZE":                       [44 + 12764, 3],                # Turbina.Frenagem.Info.[1ZE]
        "TURB_FRENA_2ZE":                       [44 + 12764, 4],                # Turbina.Frenagem.Info.[2ZE]

        "TURB_VIBRACAO_05":                     127 + 12764,                    # Leituras.Turb_Vibracao05

        # Reg V
        "REG_V_INFO":                           45 + 12764,                     # Leituras.RegV_Info
        "REG_V_HABILITADO":                     [45 + 12764, 0],                # RegV.Info.Habilitado
        "REG_V_BASE_CARGA":                     [45 + 12764, 1],                # RegV.Info.BaseCarga
        "REG_V_RPM30":                          [45 + 12764, 2],                # RegV.Info.RPM30
        "REG_V_RPM90":                          [45 + 12764, 3],                # RegV.Info.RPM90
        "REG_V_CARGA_ZERADA":                   [45 + 12764, 4],                # RegV.Info.CargaZerada
        "REG_V_MODO_ESTATISMO":                 [45 + 12764, 5],                # RegV.Info.ModoEstatismo
        "REG_V_MODO_BASE_CARGA":                [45 + 12764, 6],                # RegV.Info.ModoBaseCarga
        "REG_V_DISTRI_FECHADO":                 [45 + 12764, 7],                # RegV.Info.DistribuidorFechado

        "REG_V_ESTADO":                         46 + 12764,                     # Leituras.RegV_Estado
        "REG_V_FALHA":                          [46 + 12764, 0],                # RegV.Estado.Falha
        "REG_V_PARADO":                         [46 + 12764, 1],                # RegV.Estado.Parado
        "REG_V_CTRL_MANUAL_DISTRI":             [46 + 12764, 2],                # RegV.Estado.ControleManualDistribuidor
        "REG_V_CTRL_MANUAL_VALV":               [46 + 12764, 3],                # RegV.Estado.ControleManualValvula
        "REG_V_CTRL_VELOC":                     [46 + 12764, 4],                # RegV.Estado.ControleVelocidade
        "REG_V_COMPENSA_POT_ATIVA":             [46 + 12764, 5],                # RegV.Estado.CompensacaoPotenciaAtiva
        "REG_V_CTRL_POT_ATIVA":                 [46 + 12764, 6],                # RegV.Estado.ControlePotenciaAtiva

        "REG_V_VELOCIDADE":                     47 + 12764,                     # Leituras.RegV_Velocidade
        "REG_V_DISTRIBUIDOR":                   48 + 12764,                     # Leituras.RegV_Distribuidor
        "REG_V_ROTOR":                          49 + 12764,                     # Leituras.RegV_Rotor
        "REG_V_POT_ALVO":                       50 + 12764,                     # Leituras.RegV_PotenciaAlvo

        "REG_V_CONJUGADO_INFO":                 128 + 12764,                    # Leituras.RegV_CurvaConjugacao_Info
        "REG_V_CONJ_AUTOMATICO":                [128 + 12764, 0],               # RegV.Conjugado.Automatico
        "REG_V_CONJ_MANUAL":                    [128 + 12764, 1],               # RegV.Conjugado.Manual
        "REG_V_CONJUGADO1":                     [128 + 12764, 2],               # RegV.Conjugado.Conjugado1
        "REG_V_CONJUGADO2":                     [128 + 12764, 3],               # RegV.Conjugado.Conjugado2
        "REG_V_CONJUGADO3":                     [128 + 12764, 4],               # RegV.Conjugado.Conjugado3

        # Reg T
        "REG_T_INFO":                           51 + 12764,                     # Leituras.RegT_Info
        "REG_T_HABILITACAO":                    [51 + 12764, 0],                # RegT.Info.Habilitacao
        "REG_T_TENSAO_ESTAB":                   [51 + 12764, 1],                # RegT.Info.TensaoEstabilizada
        "REG_T_CONTATOR_ABERTO":                [51 + 12764, 2],                # RegT.Info.ContatorAberto
        "REG_T_CONTATOR_FECHADO":               [51 + 12764, 3],                # RegT.Info.ContatorFechado
        "REG_T_PRE_EXCITACAO":                  [51 + 12764, 4],                # RegT.Info.PreExcitacao
        "REG_T_MTVC":                           [51 + 12764, 5],                # RegT.Info.MTVC
        "REG_T_MECC":                           [51 + 12764, 6],                # RegT.Info.MECC
        "REG_T_OPER_ONLINE":                    [51 + 12764, 7],                # RegT.Info.OperacaoOnline
        "REG_T_OPER_PARALELA":                  [51 + 12764, 9],                # RegT.Info.OperacaoParalela

        "REG_T_UEXCITACAO":                     52 + 12764,                     # Leituras.RegT_UExcitacao
        "REG_T_IEXCITACAO":                     53 + 12764,                     # Leituras.RegT_IExcitacao
        "REG_T_FPALVO":                         129 + 12764,                    # Leituras.RegT_FPAlvo
        "REG_T_REATIVO_ALVO":                   130 + 12764,                    # Leituras.RegT_ReativoAlvo

        # Sinc
        "SINC_INFO":                            54 + 12764,                     # Leituras.Sinc_Info
        "SINC_HABILITADO":                      [54 + 12764, 0],                # Sincronoscopio.Info.Habilitado
        "SINC_MODO_AUTO":                       [54 + 12764, 1],                # Sincronoscopio.Info.ModoAutomatico
        "SINC_MODO_MANUAL":                     [54 + 12764, 2],                # Sincronoscopio.Info.ModoManual
        "SINC_BARRA_MORTA":                     [54 + 12764, 3],                # Sincronoscopio.Info.BarraMorta

        "SINC_FREQ_GERADOR":                    55 + 12764,                     # Leituras.Sinc_FrequenciaGerador
        "SINC_FREQ_BARRA":                      56 + 12764,                     # Leituras.Sinc_FrequenciaBarra
        "SINC_TENSAO_GERADOR":                  57 + 12764,                     # Leituras.Sinc_TensaoGerador
        "SINC_TENSAO_BARRA":                    58 + 12764,                     # Leituras.Sinc_TensaoBarra

        # DJ
        "Dj52G_INFO":                           59 + 12764,                     # Leituras.Disj52G_Info
        "Dj52G_ABERTO":                         [59 + 12764, 0],                # Disjuntor52G.Info.Aberto
        "Dj52G_FECHADO":                        [59 + 12764, 1],                # Disjuntor52G.Info.Fechado
        "Dj52G_INCONSISTENTE":                  [59 + 12764, 2],                # Disjuntor52G.Info.Inconsistente
        "Dj52G_TRIP":                           [59 + 12764, 3],                # Disjuntor52G.Info.TRIP
        "Dj52G_TESTE":                          [59 + 12764, 4],                # Disjuntor52G.Info.Teste
        "Dj52G_INSERIDO":                       [59 + 12764, 5],                # Disjuntor52G.Info.Inserido
        "Dj52G_EXTRAIVEL":                      [59 + 12764, 6],                # Disjuntor52G.Info.Extraivel
        "Dj52G_MOLA_CARRE":                     [59 + 12764, 7],                # Disjuntor52G.Info.MolaCarregada
        "Dj52G_CONDICAO":                       [59 + 12764, 8],                # Disjuntor52G.Info.CondicaoFechamento
        "Dj52G_FALTA_VCC":                      [59 + 12764, 9],                # Disjuntor52G.Info.FaltaVCC

        # Tensão
        "TENSAO_RN":                            60 + 12764,                     # Leituras.Gerador_TensaoRN
        "TENSAO_SN":                            61 + 12764,                     # Leituras.Gerador_TensaoSN
        "TENSAO_TN":                            62 + 12764,                     # Leituras.Gerador_TensaoTN
        "TENSAO_RS":                            63 + 12764,                     # Leituras.Gerador_TensaoRS
        "TENSAO_ST":                            64 + 12764,                     # Leituras.Gerador_TensaoST
        "TENSAO_TR":                            65 + 12764,                     # Leituras.Gerador_TensaoTR

        # Corrente
        "CORRENTE_R":                           66 + 12764,                     # Leituras.Gerador_CorrenteR
        "CORRENTE_S":                           67 + 12764,                     # Leituras.Gerador_CorrenteS
        "CORRENTE_T":                           68 + 12764,                     # Leituras.Gerador_CorrenteT
        "CORRENTE_MEDIA":                       69 + 12764,                     # Leituras.Gerador_CorrenteMedia

        # Potência Ativa
        "POT_ATIVA_1":                          70 + 12764,                     # Leituras.Gerador_PotenciaAtiva1
        "POT_ATIVA_2":                          71 + 12764,                     # Leituras.Gerador_PotenciaAtiva2
        "POT_ATIVA_3":                          72 + 12764,                     # Leituras.Gerador_PotenciaAtiva3
        "POT_ATIVA_MEDIA":                      73 + 12764,                     # Leituras.Gerador_PotenciaAtivaMedia

        # Potência Reativa
        "POT_REATIVA_1":                        74 + 12764,                     # Leituras.Gerador_PotenciaReativa1
        "POT_REATIVA_2":                        75 + 12764,                     # Leituras.Gerador_PotenciaReativa2
        "POT_REATIVA_3":                        76 + 12764,                     # Leituras.Gerador_PotenciaReativa3
        "POT_REATIVA_MEDIA":                    77 + 12764,                     # Leituras.Gerador_PotenciaReativaMedia

        # Potência Aparente
        "POT_APARENTE_1":                       78 + 12764,                     # Leituras.Gerador_PotenciaAparente1
        "POT_APARENTE_2":                       79 + 12764,                     # Leituras.Gerador_PotenciaAparente2
        "POT_APARENTE_3":                       80 + 12764,                     # Leituras.Gerador_PotenciaAparente3
        "POT_APARENTE_MEDIA":                   81 + 12764,                     # Leituras.Gerador_PotenciaAparenteMedia

        # Fator Potência
        "FATOR_POT_1":                          82 + 12764,                     # Leituras.Gerador_FatorPotencia1
        "FATOR_POT_2":                          83 + 12764,                     # Leituras.Gerador_FatorPotencia2
        "FATOR_POT_3":                          84 + 12764,                     # Leituras.Gerador_FatorPotencia3
        "FATOR_POT_MEDIA":                      85 + 12764,                     # Leituras.Gerador_FatorPotenciaMedia

        # Frequencia
        "FREQUENCIA":                           86 + 12764,                     # Leituras.Gerador_Frequencia

        # Energia Fornecida
        "ENERGIA_FORNECIDA_TWh":                87 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTWh
        "ENERGIA_FORNECIDA_GWh":                88 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGWh
        "ENERGIA_FORNECIDA_MWh":                89 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMWh
        "ENERGIA_FORNECIDA_kWh":                90 + 12764,                     # Leituras.Gerador_EnergiaFornecidakWh
        "ENERGIA_FORNECIDA_TVarh":              91 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTVarh
        "ENERGIA_FORNECIDA_GVarh":              92 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGVarh
        "ENERGIA_FORNECIDA_MVarh":              93 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMVarh
        "ENERGIA_FORNECIDA_kVarh":              94 + 12764,                     # Leituras.Gerador_EnergiaFornecidakVarh
        "ENERGIA_CORNECIDA_TVarh":              95 + 12764,                     # Leituras.Gerador_EnergiaConsumidaTVarh
        "ENERGIA_CORNECIDA_GVarh":              96 + 12764,                     # Leituras.Gerador_EnergiaConsumidaGVarh
        "ENERGIA_CORNECIDA_MVarh":              97 + 12764,                     # Leituras.Gerador_EnergiaConsumidaMVarh
        "ENERGIA_CORNECIDA_kVarh":              98 + 12764,                     # Leituras.Gerador_EnergiaConsumidakVarh
    
        "GERADOR_FP_INFO":                      99 + 12764,                     # Leituras.Gerador_FPInfo
        "GERADOR_FP_FASE1_IND":                 [99 + 12764, 0],                # Gerador.FP_Info.Fase1_Ind
        "GERADOR_FP_FASE1_CAP":                 [99 + 12764, 1],                # Gerador.FP_Info.Fase1_Cap
        "GERADOR_FP_FASE2_IND":                 [99 + 12764, 2],                # Gerador.FP_Info.Fase2_Ind
        "GERADOR_FP_FASE2_CAP":                 [99 + 12764, 3],                # Gerador.FP_Info.Fase2_Cap
        "GERADOR_FP_FASE3_IND":                 [99 + 12764, 4],                # Gerador.FP_Info.Fase3_Ind
        "GERADOR_FP_FASE3_CAP":                 [99 + 12764, 5],                # Gerador.FP_Info.Fase3_Cap
        "GERADOR_FP_FASE4_IND":                 [99 + 12764, 6],                # Gerador.FP_Info.Total_Ind
        "GERADOR_FP_FASE4_CAP":                 [99 + 12764, 7],                # Gerador.FP_Info.Total_Cap

        # Controles
        "CTRL_REATIVO_INFO":                    100 + 12764,                    # Leituras.CtrlReativo_Info
        "CTRL_REAT_MODO_FP":                    [100 + 12764, 0],               # CtrlReativo.Info.ModoFP
        "CTRL_REAT_MODO_VAR":                   [100 + 12764, 1],               # CtrlReativo.Info.ModoVar

        "CTRL_POTENCIA_INFO":                   101 + 12764,                    # Leituras.CtrlPotencia_Info
        "CTRL_POT_MODO_NIVEL":                  [101 + 12764, 0],               # CtrlPotencia.Info.ModoNivel
        "CTRL_POT_MODO_POT":                    [101 + 12764, 1],               # CtrlPotencia.Info.ModoPotencia
        "CTRL_POT_MODO_RELIGA_AUTO":            [101 + 12764, 2],               # CtrlPotencia.Info.ModoReligamentoAutomatico

        # Horimetros
        "HORIM_ELETR_LOW":                      102 + 12764,                    # Leituras.HorimetroEletrico_Low
        "HORIM_ELETR_HIGH":                     103 + 12764,                    # Leituras.HorimetroEletrico_High
        "HORIM_MECAN_LOW":                      104 + 12764,                    # Leituras.HorimetroMecanico_Low
        "HORIM_MECAN_HIGH":                     105 + 12764,                    # Leituras.HorimetroMecanico_High

        # Temperatura
        "TEMPERATURA_01":                       107 + 12764,                    # Leituras.Temperatura_01
        "TEMPERATURA_02":                       108 + 12764,                    # Leituras.Temperatura_02
        "TEMPERATURA_03":                       109 + 12764,                    # Leituras.Temperatura_03
        "TEMPERATURA_04":                       110 + 12764,                    # Leituras.Temperatura_04
        "TEMPERATURA_05":                       111 + 12764,                    # Leituras.Temperatura_05
        "TEMPERATURA_06":                       112 + 12764,                    # Leituras.Temperatura_06
        "TEMPERATURA_07":                       113 + 12764,                    # Leituras.Temperatura_07
        "TEMPERATURA_08":                       114 + 12764,                    # Leituras.Temperatura_08
        "TEMPERATURA_09":                       115 + 12764,                    # Leituras.Temperatura_09
        "TEMPERATURA_10":                       116 + 12764,                    # Leituras.Temperatura_10
        "TEMPERATURA_11":                       117 + 12764,                    # Leituras.Temperatura_11
        "TEMPERATURA_12":                       118 + 12764,                    # Leituras.Temperatura_12
        "TEMPERATURA_13":                       119 + 12764,                    # Leituras.Temperatura_13
        "TEMPERATURA_14":                       120 + 12764,                    # Leituras.Temperatura_14
        "TEMPERATURA_15":                       121 + 12764,                    # Leituras.Temperatura_15
        "TEMPERATURA_16":                       122 + 12764,                    # Leituras.Temperatura_16


        ## DISJUNTORES

        "DJ_01":                                0,
        "DJ_02":                                1,
        "DJ_03":                                2,
        "DJ_04":                                3,
        "DJ_05":                                4,
        "DJ_06":                                5,
        "DJ_07":                                6,
        "DJ_08":                                7,
        "DJ_09":                                8,
        "DJ_10":                                9,
        "DJ_11":                                10,
        "DJ_12":                                11,
        "DJ_13":                                12,
        "DJ_14":                                13,
        "DJ_15":                                14,
        "DJ_16":                                15,
        "DJ_17":                                16,
        "DJ_18":                                17,
        "DJ_19":                                18,
        "DJ_20":                                19,
        "DJ_21":                                20,
        "DJ_22":                                21,
        "DJ_23":                                22,
        "DJ_24":                                23,
        "DJ_25":                                24,
        "DJ_26":                                25,
        "DJ_27":                                26,
        "DJ_28":                                27,
        "DJ_29":                                28,
        "DJ_30":                                29,
        "DJ_31":                                30,
        "DJ_32":                                31,


        ## ALARMES

        # Específicos UG3
        "Alarme10_12":                          [10 + 14199, 12],
        "Alarme10_13":                          [10 + 14199, 13],

        "Alarme13_05":                          [13 + 14199, 5],
        "Alarme13_06":                          [13 + 14199, 6],
        "Alarme13_07":                          [13 + 14199, 7],
        "Alarme13_08":                          [13 + 14199, 8],
        "Alarme13_09":                          [13 + 14199, 9],
        "Alarme13_10":                          [13 + 14199, 10],
        "Alarme13_11":                          [13 + 14199, 11],

        "Alarme16_00":                          [16 + 14199, 0],
        "Alarme16_01":                          [16 + 14199, 1],


        # Gerais
        "Alarme01_01":                          [1 + 14199, 1],
        "Alarme01_02":                          [1 + 14199, 2],
        "Alarme01_00":                          [1 + 14199, 0],
        "Alarme01_03":                          [1 + 14199, 3],
        "Alarme01_06":                          [1 + 14199, 6],
        "Alarme01_07":                          [1 + 14199, 7],
        "Alarme01_08":                          [1 + 14199, 8],
        "Alarme01_09":                          [1 + 14199, 9],
        "Alarme01_10":                          [1 + 14199, 10],
        "Alarme01_11":                          [1 + 14199, 11],
        "Alarme01_12":                          [1 + 14199, 12],
        "Alarme01_13":                          [1 + 14199, 13],
        "Alarme01_14":                          [1 + 14199, 14],
        "Alarme01_15":                          [1 + 14199, 15],

        "Alarme02_00":                          [2 + 14199, 0],
        "Alarme02_01":                          [2 + 14199, 1],
        "Alarme02_02":                          [2 + 14199, 2],
        "Alarme02_03":                          [2 + 14199, 3],
        "Alarme02_04":                          [2 + 14199, 4],
        "Alarme02_05":                          [2 + 14199, 5],
        "Alarme02_06":                          [2 + 14199, 6],
        "Alarme02_07":                          [2 + 14199, 7],
        "Alarme02_08":                          [2 + 14199, 8],
        "Alarme02_09":                          [2 + 14199, 9],
        "Alarme02_10":                          [2 + 14199, 10],
        "Alarme02_11":                          [2 + 14199, 11],
        "Alarme02_12":                          [2 + 14199, 12],
        "Alarme02_13":                          [2 + 14199, 13],
        "Alarme02_14":                          [2 + 14199, 14],
        "Alarme02_15":                          [2 + 14199, 15],

        "Alarme03_00":                          [3 + 14199, 0],
        "Alarme03_01":                          [3 + 14199, 1],
        "Alarme03_02":                          [3 + 14199, 2],
        "Alarme03_03":                          [3 + 14199, 3],
        "Alarme03_04":                          [3 + 14199, 4],
        "Alarme03_05":                          [3 + 14199, 5],
        "Alarme03_06":                          [3 + 14199, 6],
        "Alarme03_07":                          [3 + 14199, 7],
        "Alarme03_08":                          [3 + 14199, 8],
        "Alarme03_09":                          [3 + 14199, 9],
        "Alarme03_10":                          [3 + 14199, 10],
        "Alarme03_11":                          [3 + 14199, 11],
        "Alarme03_12":                          [3 + 14199, 12],
        "Alarme03_13":                          [3 + 14199, 13],
        "Alarme03_14":                          [3 + 14199, 14],
        "Alarme03_15":                          [3 + 14199, 15],

        "Alarme04_00":                          [4 + 14199, 0],
        "Alarme04_01":                          [4 + 14199, 1],
        "Alarme04_02":                          [4 + 14199, 2],
        "Alarme04_04":                          [4 + 14199, 4],
        "Alarme04_05":                          [4 + 14199, 5],
        "Alarme04_06":                          [4 + 14199, 6],
        "Alarme04_07":                          [4 + 14199, 7],
        "Alarme04_09":                          [4 + 14199, 9],
        "Alarme04_10":                          [4 + 14199, 10],
        "Alarme04_11":                          [4 + 14199, 11],
        "Alarme04_12":                          [4 + 14199, 12],
        "Alarme04_13":                          [4 + 14199, 13],
        "Alarme04_14":                          [4 + 14199, 14],
        "Alarme04_15":                          [4 + 14199, 15],

        "Alarme05_00":                          [5 + 14199, 0],
        "Alarme05_02":                          [5 + 14199, 2],
        "Alarme05_03":                          [5 + 14199, 3],
        "Alarme05_04":                          [5 + 14199, 4],
        "Alarme05_05":                          [5 + 14199, 5],
        "Alarme05_06":                          [5 + 14199, 6],
        "Alarme05_07":                          [5 + 14199, 7],
        "Alarme05_09":                          [5 + 14199, 9],
        "Alarme05_10":                          [5 + 14199, 10],
        "Alarme05_11":                          [5 + 14199, 11],
        "Alarme05_12":                          [5 + 14199, 12],
        "Alarme05_13":                          [5 + 14199, 13],
        "Alarme05_14":                          [5 + 14199, 14],
        "Alarme05_15":                          [5 + 14199, 15],

        "Alarme06_00":                          [6 + 14199, 0],
        "Alarme06_03":                          [6 + 14199, 3],
        "Alarme06_04":                          [6 + 14199, 4],
        "Alarme06_05":                          [6 + 14199, 5],
        "Alarme06_08":                          [6 + 14199, 8],
        "Alarme06_09":                          [6 + 14199, 9],
        "Alarme06_10":                          [6 + 14199, 10],
        "Alarme06_11":                          [6 + 14199, 11],
        "Alarme06_12":                          [6 + 14199, 12],
        "Alarme06_13":                          [6 + 14199, 13],
        "Alarme06_14":                          [6 + 14199, 14],
        "Alarme06_15":                          [6 + 14199, 15],

        "Alarme07_00":                          [7 + 14199, 0],
        "Alarme07_01":                          [7 + 14199, 1],
        "Alarme07_02":                          [7 + 14199, 2],
        "Alarme07_03":                          [7 + 14199, 3],
        "Alarme07_06":                          [7 + 14199, 6],
        "Alarme07_07":                          [7 + 14199, 7],
        "Alarme07_08":                          [7 + 14199, 8],
        "Alarme07_09":                          [7 + 14199, 9],
        "Alarme07_10":                          [7 + 14199, 10],
        "Alarme07_11":                          [7 + 14199, 11],
        "Alarme07_12":                          [7 + 14199, 12],
        "Alarme07_13":                          [7 + 14199, 13],
        "Alarme07_14":                          [7 + 14199, 14],
        "Alarme07_15":                          [7 + 14199, 15],

        "Alarme08_00":                          [8 + 14199, 0],
        "Alarme08_01":                          [8 + 14199, 1],
        "Alarme08_02":                          [8 + 14199, 2],
        "Alarme08_03":                          [8 + 14199, 3],
        "Alarme08_07":                          [8 + 14199, 7],
        "Alarme08_08":                          [8 + 14199, 8],
        "Alarme08_09":                          [8 + 14199, 9],
        "Alarme08_10":                          [8 + 14199, 10],
        "Alarme08_11":                          [8 + 14199, 11],
        "Alarme08_12":                          [8 + 14199, 12],
        "Alarme08_13":                          [8 + 14199, 13],
        "Alarme08_14":                          [8 + 14199, 14],
        "Alarme08_15":                          [8 + 14199, 15],

        "Alarme09_00":                          [9 + 14199, 0],
        "Alarme09_01":                          [9 + 14199, 1],
        "Alarme09_02":                          [9 + 14199, 2],
        "Alarme09_03":                          [9 + 14199, 3],
        "Alarme09_04":                          [9 + 14199, 4],
        "Alarme09_06":                          [9 + 14199, 6],
        "Alarme09_07":                          [9 + 14199, 7],
        "Alarme09_08":                          [9 + 14199, 8],
        "Alarme09_09":                          [9 + 14199, 9],
        "Alarme09_10":                          [9 + 14199, 10],
        "Alarme09_11":                          [9 + 14199, 11],
        "Alarme09_12":                          [9 + 14199, 12],
        "Alarme09_13":                          [9 + 14199, 13],
        "Alarme09_14":                          [9 + 14199, 14],
        "Alarme09_15":                          [9 + 14199, 15],

        "Alarme10_00":                          [10 + 14199, 0],
        "Alarme10_01":                          [10 + 14199, 1],
        "Alarme10_02":                          [10 + 14199, 2],
        "Alarme10_03":                          [10 + 14199, 3],
        "Alarme10_05":                          [10 + 14199, 5],
        "Alarme10_06":                          [10 + 14199, 6],
        "Alarme10_07":                          [10 + 14199, 7],
        "Alarme10_08":                          [10 + 14199, 8],
        "Alarme10_09":                          [10 + 14199, 9],
        "Alarme10_10":                          [10 + 14199, 10],
        "Alarme10_11":                          [10 + 14199, 11],
        "Alarme10_12":                          [10 + 14199, 12],
        "Alarme10_13":                          [10 + 14199, 13],
        "Alarme10_14":                          [10 + 14199, 14],
        "Alarme10_15":                          [10 + 14199, 15],

        "Alarme11_00":                          [11 + 14199, 0],
        "Alarme11_01":                          [11 + 14199, 1],
        "Alarme11_02":                          [11 + 14199, 2],
        "Alarme11_06":                          [11 + 14199, 6],
        "Alarme11_07":                          [11 + 14199, 7],
        "Alarme11_08":                          [11 + 14199, 8],
        "Alarme11_09":                          [11 + 14199, 9],
        "Alarme11_10":                          [11 + 14199, 10],
        "Alarme11_11":                          [11 + 14199, 11],
        "Alarme11_12":                          [11 + 14199, 12],
        "Alarme11_13":                          [11 + 14199, 13],
        "Alarme11_14":                          [11 + 14199, 14],
        "Alarme11_15":                          [11 + 14199, 15],

        "Alarme12_01":                          [12 + 14199, 1],
        "Alarme12_02":                          [12 + 14199, 2],
        "Alarme12_03":                          [12 + 14199, 3],
        "Alarme12_04":                          [12 + 14199, 4],
        "Alarme12_05":                          [12 + 14199, 5],
        "Alarme12_06":                          [12 + 14199, 6],
        "Alarme12_07":                          [12 + 14199, 7],
        "Alarme12_09":                          [12 + 14199, 9],
        "Alarme12_10":                          [12 + 14199, 10],
        "Alarme12_11":                          [12 + 14199, 11],
        "Alarme12_12":                          [12 + 14199, 12],
        "Alarme12_13":                          [12 + 14199, 13],
        "Alarme12_14":                          [12 + 14199, 14],
        "Alarme12_15":                          [12 + 14199, 15],

        "Alarme13_00":                          [13 + 14199, 0],
        "Alarme13_01":                          [13 + 14199, 1],
        "Alarme13_02":                          [13 + 14199, 2],
        "Alarme13_03":                          [13 + 14199, 3],
        "Alarme13_09":                          [13 + 14199, 9],
        "Alarme13_10":                          [13 + 14199, 10],
        "Alarme13_11":                          [13 + 14199, 11],
        "Alarme13_12":                          [13 + 14199, 12],
        "Alarme13_13":                          [13 + 14199, 13],
        "Alarme13_14":                          [13 + 14199, 14],
        "Alarme13_15":                          [13 + 14199, 15],

        "Alarme14_00":                          [14 + 14199, 0],
        "Alarme14_01":                          [14 + 14199, 1],
        "Alarme14_02":                          [14 + 14199, 2],
        "Alarme14_03":                          [14 + 14199, 3],
        "Alarme14_04":                          [14 + 14199, 4],
        "Alarme14_05":                          [14 + 14199, 5],
        "Alarme14_10":                          [14 + 14199, 10],
        "Alarme14_11":                          [14 + 14199, 11],
        "Alarme14_12":                          [14 + 14199, 12],
        "Alarme14_13":                          [14 + 14199, 13],
        "Alarme14_14":                          [14 + 14199, 14],
        "Alarme14_15":                          [14 + 14199, 15],

        "Alarme15_00":                          [15 + 14199, 0],
        "Alarme15_01":                          [15 + 14199, 1],
        "Alarme15_02":                          [15 + 14199, 2],
        "Alarme15_03":                          [15 + 14199, 3],
        "Alarme15_04":                          [15 + 14199, 4],
        "Alarme15_05":                          [15 + 14199, 5],
        "Alarme15_06":                          [15 + 14199, 6],
        "Alarme15_07":                          [15 + 14199, 7],
        "Alarme15_08":                          [15 + 14199, 8],
        "Alarme15_09":                          [15 + 14199, 9],
        "Alarme15_10":                          [15 + 14199, 10],
        "Alarme15_12":                          [15 + 14199, 12],
        "Alarme15_13":                          [15 + 14199, 13],
        "Alarme15_14":                          [15 + 14199, 14],
        "Alarme15_15":                          [15 + 14199, 15],

        "Alarme16_00":                          [16 + 14199, 0],
        "Alarme16_01":                          [16 + 14199, 1],
        "Alarme16_02":                          [16 + 14199, 2],
        "Alarme16_03":                          [16 + 14199, 3],
        "Alarme16_04":                          [16 + 14199, 4],
        "Alarme16_05":                          [16 + 14199, 5],
        "Alarme16_06":                          [16 + 14199, 6],
        "Alarme16_07":                          [16 + 14199, 7],
        "Alarme16_08":                          [16 + 14199, 8],
        "Alarme16_09":                          [16 + 14199, 9],
        "Alarme16_10":                          [16 + 14199, 10],
        "Alarme16_11":                          [16 + 14199, 11],
        "Alarme16_12":                          [16 + 14199, 12],
    },
    "UG4": {
        ## COMANDOS
        # Gerais
        "CMD_RESET_ALARMES":                    0 + 12289,                      # Comandos.Operacao_PCH_AdoPopinhakResetAlarmes
        "CMD_RECONHECE_ALARMES":                1 + 12289,                      # Comandos.Operacao_PCH_AdoPopinhakReconheceAlarmes

        # Operação
        "CMD_OPER_UP":                          2 + 12289,                      # Comandos.Operacao_UP
        "CMD_OPER_UPGM":                        3 + 12289,                      # Comandos.Operacao_UPGM
        "CMD_OPER_UVD":                         4 + 12289,                      # Comandos.Operacao_UVD
        "CMD_OPER_UPS":                         5 + 12289,                      # Comandos.Operacao_UPS
        "CMD_OPER_US":                          6 + 12289,                      # Comandos.Operacao_US
        "CMD_OPER_EMERGENCIA_LIGAR":            7 + 12289,                      # Comandos.Operacao_EmergenciaLigar
        "CMD_OPER_EMERGENCIA_DESLIGAR":         8 + 12289,                      # Comandos.Operacao_EmergenciaDesligar
        "CMD_OPER_PARADA_RESET":                72 + 12289,                     # Comandos.Operacao_ParadaReset

        # Turbina
        "CMD_TURB_BYPASS_ABRIR":                9 + 12289,                      # Comandos.Turb_ByPassAbrir
        "CMD_TURB_BYPASS_FECHAR":               10 + 12289,                     # Comandos.Turb_ByPassFechar
        "CMD_TURB_BORBOLETA_ABRIR":             11 + 12289,                     # Comandos.Turb_BorboletaAbrir
        "CMD_TURB_BORBOLETA_FECHAR":            12 + 12289,                     # Comandos.Turb_BorboletaFechar
        "CMD_TURB_FRENAGEM_APLICAR":            13 + 12289,                     # Comandos.Turb_FrenagemAplicar
        "CMD_TURB_FRENAGEM_DESAPLICAR":         14 + 12289,                     # Comandos.Turb_FrenagemDesaplicar
        "CMD_TURB_FRENAGEM_MANUAL":             15 + 12289,                     # Comandos.Turb_FrenagemManual
        "CMD_TURB_FRENAGEM_AUTO":               16 + 12289,                     # Comandos.Turb_FrenagemAuto
        "CMD_TURB_SENSOR_ATIVAR":               17 + 12289,                     # Comandos.Turb_SensorAtivar
        "CMD_TURB_SENSOR_DESATIVAR":            18 + 12289,                     # Comandos.Turb_SensorDesativar

        # Reg V
        "CMD_REG_V_PARTIR":                     19 + 12289,                     # Comandos.RegV_Partir
        "CMD_REG_V_PARAR":                      20 + 12289,                     # Comandos.RegV_Parar
        "CMD_REG_V_COLOCAR_CARGA":              21 + 12289,                     # Comandos.RegV_ColocarCarga
        "CMD_REG_V_RETIRAR_CARGA":              22 + 12289,                     # Comandos.RegV_RetirarCarga
        "CMD_REG_V_INCREMENTA_VELOCIDADE":      23 + 12289,                     # Comandos.RegV_IncrementaVelocidade
        "CMD_REG_V_DECREMENTA_VELOCIDADE":      24 + 12289,                     # Comandos.RegV_DecrementaVelocidade
        "CMD_REG_V_SEL_MODO_ESTATISMO":         25 + 12289,                     # Comandos.RegV_SelecionaModoEstatismo
        "CMD_REG_V_SEL_MODO_BASECARGA":         26 + 12289,                     # Comandos.RegV_SelecionaModoBaseCarga

        # Reg T
        "CMD_REG_T_LIGAR":                      27 + 12289,                     # Comandos.RegT_Ligar
        "CMD_REG_T_DESLIGAR":                   28 + 12289,                     # Comandos.RegT_Desligar
        "CMD_REG_T_INCREMENTA_TENSAO":          29 + 12289,                     # Comandos.RegT_IncrementaTensao
        "CMD_REG_T_DECREMENTA_TENSAO":          30 + 12289,                     # Comandos.RegT_DecrementaTensao
        "CMD_REG_T_PRE_EXCITACAO":              31 + 12289,                     # Comandos.RegT_PreExcitacao

        # Sinc
        "CMD_SINC_LIGAR":                       32 + 12289,                     # Comandos.Sinc_Ligar
        "CMD_SINC_DESLIGAR":                    33 + 12289,                     # Comandos.Sinc_Desligar
        "CMD_SINC_MODO_AUTO_LIGAR":             34 + 12289,                     # Comandos.Sinc_ModoAutoLigar
        "CMD_SINC_MODO_MANUAL_LIGAR":           35 + 12289,                     # Comandos.Sinc_ModoManualLigar
        "CMD_SINC_MODO_BMORTA_LIGAR":           36 + 12289,                     # Comandos.Sinc_ModoBMortaLigar

        # DJ52G
        "CMD_DJ52G_ABRIR":                      37 + 12289,                     # Comandos.Disj52G_Abrir

        # Controle Reativo
        "CMD_CTRL_REATIVO_MODO_FPLIGAR":        38 + 12289,                     # Comandos.CtrlReativo_ModoFPLigar
        "CMD_CTRL_REATIVO_MODO_FPDESLIGAR":     39 + 12289,                     # Comandos.CtrlReativo_ModoFPDesligar
        "CMD_CTRL_REATIVO_MODO_VArLIGAR":       40 + 12289,                     # Comandos.CtrlReativo_ModoVArLigar
        "CMD_CTRL_REATIVO_MODO_VArDESLIGAR":    41 + 12289,                     # Comandos.CtrlReativo_ModoVArDesligar

        # Controle Potência
        "CMD_CTRL_POT_MODO_POT_LIGAR":          42 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaLigar
        "CMD_CTRL_POT_MODO_POT_DESLIGAR":       43 + 12289,                     # Comandos.CtrlPotencia_ModoPotenciaDesligar
        "CMD_CTRL_POT_MODO_NIVEL_LIGAR":        44 + 12289,                     # Comandos.CtrlPotencia_ModoNivelLigar
        "CMD_CTRL_POT_MODO_NIVEL_DESLIGAR":     45 + 12289,                     # Comandos.CtrlPotencia_ModoNivelDesligar
        "CMD_CTRL_POT_RELI_AUTO_LIGAR":         46 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoLigar
        "CMD_CTRL_POT_RELI_AUTO_DESLIGAR":      47 + 12289,                     # Comandos.CtrlPotencia_ReligamentoAutomaticoDesligar

        # UHCT
        "CMD_UHCT_BOMBA_01_LIGAR":              48 + 12289,                     # Comandos.UHCT_Bomba01Ligar
        "CMD_UHCT_BOMBA_01_DESLIGAR":           49 + 12289,                     # Comandos.UHCT_Bomba01Desligar
        "CMD_UHCT_BOMBA_01_PRINCIPAL":          50 + 12289,                     # Comandos.UHCT_Bomba01Principal
        "CMD_UHCT_BOMBA_02_LIGAR":              51 + 12289,                     # Comandos.UHCT_Bomba02Ligar
        "CMD_UHCT_BOMBA_02_DESLIGAR":           52 + 12289,                     # Comandos.UHCT_Bomba02Desligar
        "CMD_UHCT_BOMBA_02_PRINCIPAL":          53 + 12289,                     # Comandos.UHCT_Bomba02Principal
        "CMD_UHCT_BOMBA_AGUA_LIGAR":            54 + 12289,                     # Comandos.UHCT_BombaAguaLigar
        "CMD_UHCT_BOMBA_AGUA_DESLIGAR":         55 + 12289,                     # Comandos.UHCT_BombaAguaDesligar
        "CMD_UHCT_SENSOR_ATIVAR":               56 + 12289,                     # Comandos.UHCT_SensorAtivar
        "CMD_UHCT_SENSOR_DESATIVAR":            57 + 12289,                     # Comandos.UHCT_SensorDesativar
        "CMD_UHCT_RODIZIO_HABILITAR":           58 + 12289,                     # Comandos.UHCT_RodizioHabilitar
        "CMD_UHCT_RODIZIO_DESABILITAR":         59 + 12289,                     # Comandos.UHCT_RodizioDesabilitar

        # UHLM
        "CMD_UHLM_BOMBA_01_LIGAR":              60 + 12289,                     # Comandos.UHLM_Bomba01Ligar
        "CMD_UHLM_BOMBA_01_DESLIGAR":           61 + 12289,                     # Comandos.UHLM_Bomba01Desligar
        "CMD_UHLM_BOMBA_01_PRINCIPAL":          62 + 12289,                     # Comandos.UHLM_Bomba01Principal
        "CMD_UHLM_BOMBA_02_LIGAR":              63 + 12289,                     # Comandos.UHLM_Bomba02Ligar
        "CMD_UHLM_BOMBA_02_DESLIGAR":           64 + 12289,                     # Comandos.UHLM_Bomba02Desligar
        "CMD_UHLM_BOMBA_02_PRINCIPAL":          65 + 12289,                     # Comandos.UHLM_Bomba02Principal
        "CMD_UHLM_BOMBA_JACKING_LIGA":          66 + 12289,                     # Comandos.UHLM_BombaJackingLiga
        "CMD_UHLM_BOMBA_JACKING_DESLIGA":       67 + 12289,                     # Comandos.UHLM_BombaJackingDesliga
        "CMD_UHLM_BOMBA_AGUA_LIGA":             68 + 12289,                     # Comandos.UHLM_BombaAguaLiga
        "CMD_UHLM_BOMBA_AGUA_DESLIGA":          69 + 12289,                     # Comandos.UHLM_BombaAguaDesliga
        "CMD_UHLM_RODIZIO_HABILITAR":           70 + 12289,                     # Comandos.UHLM_RodizioHabilitar
        "CMD_UHLM_RODIZIO_DESABILITAR":         71 + 12289,                     # Comandos.UHLM_RodizioDesabilitar

        # RT
        "CMD_RT_MTVC_HABILITAR":                73 + 12289,                     # Comandos.RT_MTVC_Habilitar
        "CMD_RT_MECC_HABILITAR":                74 + 12289,                     # Comandos.RT_MECC_Habilitar
        "CMD_RT_ONLINE_HABILITAR":              75 + 12289,                     # Comandos.RT_Online_habilitar
        "CMD_RT_ONLINE_DESABILITAR":            76 + 12289,                     # Comandos.RT_Online_Desabiltar
        "CMD_RT_PARALELO_HABILITAR":            77 + 12289,                     # Comandos.RT_Paralelo_habilitar
        "CMD_RT_PARALELO_DESABILITAR":          78 + 12289,                     # Comandos.RT_Paralelo_Desabilitar

        # RV
        "CMD_RV_CONJUGADO_AUTO_HABILITAR":      79 + 12289,                     # Comandos.RV_ConjugadoAuto_habilitar
        "CMD_RV_CONJUGADO_MANUAL_HABILITAR":    80 + 12289,                     # Comandos.RV_ConjugadoManual_habilitar
        "CMD_RV_CONJUGADO_01_HABILITAR":        81 + 12289,                     # Comandos.RV_Conjugado01_habilitar
        "CMD_RV_CONJUGADO_02_HABILITAR":        82 + 12289,                     # Comandos.RV_Conjugado02_habilitar
        "CMD_RV_CONJUGADO_03_HABILITAR":        83 + 12289,                     # Comandos.RV_Conjugado03_habilitar
        "CMD_RV_CONJUGADO_04_HABILITAR":        84 + 12289,                     # Comandos.RV_Conjugado04_habilitar
        "CMD_RV_CONJUGADO_05_HABILITAR":        85 + 12289,                     # Comandos.RV_Conjugado05_habilitar


        ## SETPOINTS

        # UHCT
        "UHCT_PRESSAO_MAX":                     0 + 13569,                      # Setpoints.UHCT_PressaoMaxima
        "UHCT_PRESSAO_MIN":                     1 + 13569,                      # Setpoints.UHCT_PressaoMinima
        "UHCT_PRESSAO_DESLIGAMENTO":            2 + 13569,                      # Setpoints.UHCT_PressaoDesligamento
        "UHCT_PRESSAO_CRITICA":                 3 + 13569,                      # Setpoints.UHCT_PressaoCritica

        # Controle Potência
        "CRTL_POT_NIVEL_LL1":                   4 + 13569,                      # Setpoints.CtrlPotencia_NivelLL1
        "CRTL_POT_NIVEL_LL2":                   5 + 13569,                      # Setpoints.CtrlPotencia_NivelLL2
        "CRTL_POT_NIVEL_LL3":                   6 + 13569,                      # Setpoints.CtrlPotencia_NivelLL3
        "CRTL_POT_NIVEL_LL4":                   7 + 13569,                      # Setpoints.CtrlPotencia_NivelLL4
        "CRTL_POT_NIVEL_LL5":                   8 + 13569,                      # Setpoints.CtrlPotencia_NivelLL5
        "CRTL_POT_POT_1":                       9 + 13569,                      # Setpoints.CtrlPotencia_Potencia1
        "CRTL_POT_POT_2":                       10 + 13569,                     # Setpoints.CtrlPotencia_Potencia2
        "CRTL_POT_POT_3":                       11 + 13569,                     # Setpoints.CtrlPotencia_Potencia3
        "CRTL_POT_POT_4":                       12 + 13569,                     # Setpoints.CtrlPotencia_Potencia4
        "CRTL_POT_POT_5":                       13 + 13569,                     # Setpoints.CtrlPotencia_Potencia5
        "CRTL_POT_POT_MIN":                     14 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinima
        "CRTL_POT_POT_MIN_TEMPO":               15 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMinimaTempo
        "CRTL_POT_NIVEL_RELIGAMENTO":           16 + 13569,                     # Setpoints.CtrlPotencia_NivelReligamento
        "CRTL_POT_ALVO":                        17 + 13569,                     # Setpoints.CtrlPotencia_Alvo
        "CRTL_POT_TOLERANCIA":                  18 + 13569,                     # Setpoints.CtrlPotencia_Tolerancia
        "CRTL_POT_PULSO_TEMPO":                 19 + 13569,                     # Setpoints.CtrlPotencia_PulsoTempo
        "CRTL_POT_PULSO_INTERVALO":             20 + 13569,                     # Setpoints.CtrlPotencia_PulsoIntervalo
        "CRTL_POT_SP_NIVEL":                    21 + 13569,                     # Setpoints.CtrlPotencia_SetpointNivel
        "CRTL_POT_NIVEL_MIN_ALARME":            22 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoAlarme
        "CRTL_POT_NIVEL_MIN_TRIP":              23 + 13569,                     # Setpoints.CtrlPotencia_NivelMinimoTRIP
        "CTRL_POT_POT_MAX":                     89 + 13569,                     # Setpoints.CtrlPotencia_PotenciaMaxima

        # Controle Reativo
        "CRTL_REATIVO_SP_FP":                   24 + 13569,                     # Setpoints.CtrlReativo_SetpointFP
        "CRTL_REATIVO_SP_REATIVO":              25 + 13569,                     # Setpoints.CtrlReativo_SetpointReativo

        # Turbina
        "TURB_VIBRA_01_ALARME":                 26 + 13569,                     # Setpoints.Turb_Vibracao01Alarme
        "TURB_VIBRA_01_TRIP":                   27 + 13569,                     # Setpoints.Turb_Vibracao01TRIP
        "TURB_VIBRA_02_ALARME":                 28 + 13569,                     # Setpoints.Turb_Vibracao02Alarme
        "TURB_VIBRA_02_TRIP":                   29 + 13569,                     # Setpoints.Turb_Vibracao02TRIP
        "TURB_VIBRA_03_ALARME":                 30 + 13569,                     # Setpoints.Turb_Vibracao03Alarme
        "TURB_VIBRA_03_TRIP":                   31 + 13569,                     # Setpoints.Turb_Vibracao03TRIP
        "TURB_VIBRA_04_ALARME":                 32 + 13569,                     # Setpoints.Turb_Vibracao04Alarme
        "TURB_VIBRA_04_TRIP":                   33 + 13569,                     # Setpoints.Turb_Vibracao04TRIP
        "TURB_TEMPO_EQUALI_SP":                 34 + 13569,                     # Setpoints.Turb_TempoEqualizacaoSetpoint
        "TURB_VIBRA_05_ALARME":                 90 + 13569,                     # Setpoints.Turb_Vibracao05Alarme
        "TURB_VIBRA_05_TRIP":                   91 + 13569,                     # Setpoints.Turb_Vibracao05TRIP

        # Freio
        "FREIO_PULSO_INTERVALO":                35 + 13569,                     # Setpoints.Freio_PulsoIntervalo
        "FREIO_PULSO_TEMPO":                    36 + 13569,                     # Setpoints.Freio_PulsoTempo

        # UHCT
        "UHCT_RODIZIO_PRINCIPAL":               37 + 13569,                     # Setpoints.UHCT_RodizioPrincipal
        "UHCT_RODIZIO_RETAGUARDA":              38 + 13569,                     # Setpoints.UHCT_RodizioRetaguarda

        # UHLM
        "UHLM_RODIZIO_PRINCIPAL":               39 + 13569,                     # Setpoints.UHLM_RodizioPrincipal
        "UHLM_RODIZIO_RETAGUARDA":              40 + 13569,                     # Setpoints.UHLM_RodizioRetaguarda
        "UHLM_SP_VAZAO_01":                     92 + 13569,                     # Setpoints.UHLM_SetpointVazao01
        "UHLM_SP_VAZAO_02":                     93 + 13569,                     # Setpoints.UHLM_SetpointVazao02
        "UHLM_SP_VAZAO_03":                     94 + 13569,                     # Setpoints.UHLM_SetpointVazao03
        "UHLM_SP_VAZAO_04":                     95 + 13569,                     # Setpoints.UHLM_SetpointVazao04

        # Temperaturas
        "TEMPERATURA_01_ALARME":                41 + 13569,                     # Setpoints.Temperatura01_Alarme
        "TEMPERATURA_02_ALARME":                42 + 13569,                     # Setpoints.Temperatura02_Alarme
        "TEMPERATURA_03_ALARME":                43 + 13569,                     # Setpoints.Temperatura03_Alarme
        "TEMPERATURA_04_ALARME":                44 + 13569,                     # Setpoints.Temperatura04_Alarme
        "TEMPERATURA_05_ALARME":                45 + 13569,                     # Setpoints.Temperatura05_Alarme
        "TEMPERATURA_06_ALARME":                46 + 13569,                     # Setpoints.Temperatura06_Alarme
        "TEMPERATURA_07_ALARME":                47 + 13569,                     # Setpoints.Temperatura07_Alarme
        "TEMPERATURA_08_ALARME":                48 + 13569,                     # Setpoints.Temperatura08_Alarme
        "TEMPERATURA_09_ALARME":                49 + 13569,                     # Setpoints.Temperatura09_Alarme
        "TEMPERATURA_10_ALARME":                50 + 13569,                     # Setpoints.Temperatura10_Alarme
        "TEMPERATURA_11_ALARME":                51 + 13569,                     # Setpoints.Temperatura11_Alarme
        "TEMPERATURA_12_ALARME":                52 + 13569,                     # Setpoints.Temperatura12_Alarme
        "TEMPERATURA_13_ALARME":                53 + 13569,                     # Setpoints.Temperatura13_Alarme
        "TEMPERATURA_14_ALARME":                54 + 13569,                     # Setpoints.Temperatura14_Alarme
        "TEMPERATURA_15_ALARME":                55 + 13569,                     # Setpoints.Temperatura15_Alarme
        "TEMPERATURA_16_ALARME":                56 + 13569,                     # Setpoints.Temperatura16_Alarme
        "TEMPERATURA_01_TRIP01":                57 + 13569,                     # Setpoints.Temperatura01_TRIP01
        "TEMPERATURA_02_TRIP01":                58 + 13569,                     # Setpoints.Temperatura02_TRIP01
        "TEMPERATURA_03_TRIP01":                59 + 13569,                     # Setpoints.Temperatura03_TRIP01
        "TEMPERATURA_04_TRIP01":                60 + 13569,                     # Setpoints.Temperatura04_TRIP01
        "TEMPERATURA_05_TRIP01":                61 + 13569,                     # Setpoints.Temperatura05_TRIP01
        "TEMPERATURA_06_TRIP01":                62 + 13569,                     # Setpoints.Temperatura06_TRIP01
        "TEMPERATURA_07_TRIP01":                63 + 13569,                     # Setpoints.Temperatura07_TRIP01
        "TEMPERATURA_08_TRIP01":                64 + 13569,                     # Setpoints.Temperatura08_TRIP01
        "TEMPERATURA_09_TRIP01":                65 + 13569,                     # Setpoints.Temperatura09_TRIP01
        "TEMPERATURA_10_TRIP01":                66 + 13569,                     # Setpoints.Temperatura10_TRIP01
        "TEMPERATURA_11_TRIP01":                67 + 13569,                     # Setpoints.Temperatura11_TRIP01
        "TEMPERATURA_12_TRIP01":                68 + 13569,                     # Setpoints.Temperatura12_TRIP01
        "TEMPERATURA_13_TRIP01":                69 + 13569,                     # Setpoints.Temperatura13_TRIP01
        "TEMPERATURA_14_TRIP01":                70 + 13569,                     # Setpoints.Temperatura14_TRIP01
        "TEMPERATURA_15_TRIP01":                71 + 13569,                     # Setpoints.Temperatura15_TRIP01
        "TEMPERATURA_16_TRIP01":                72 + 13569,                     # Setpoints.Temperatura16_TRIP01
        "TEMPERATURA_01_TRIP02":                73 + 13569,                     # Setpoints.Temperatura01_TRIP02
        "TEMPERATURA_02_TRIP02":                74 + 13569,                     # Setpoints.Temperatura02_TRIP02
        "TEMPERATURA_03_TRIP02":                75 + 13569,                     # Setpoints.Temperatura03_TRIP02
        "TEMPERATURA_04_TRIP02":                76 + 13569,                     # Setpoints.Temperatura04_TRIP02
        "TEMPERATURA_05_TRIP02":                77 + 13569,                     # Setpoints.Temperatura05_TRIP02
        "TEMPERATURA_06_TRIP02":                78 + 13569,                     # Setpoints.Temperatura06_TRIP02
        "TEMPERATURA_07_TRIP02":                79 + 13569,                     # Setpoints.Temperatura07_TRIP02
        "TEMPERATURA_08_TRIP02":                80 + 13569,                     # Setpoints.Temperatura08_TRIP02
        "TEMPERATURA_09_TRIP02":                81 + 13569,                     # Setpoints.Temperatura09_TRIP02
        "TEMPERATURA_10_TRIP02":                82 + 13569,                     # Setpoints.Temperatura10_TRIP02
        "TEMPERATURA_11_TRIP02":                83 + 13569,                     # Setpoints.Temperatura11_TRIP02
        "TEMPERATURA_12_TRIP02":                84 + 13569,                     # Setpoints.Temperatura12_TRIP02
        "TEMPERATURA_13_TRIP02":                85 + 13569,                     # Setpoints.Temperatura13_TRIP02
        "TEMPERATURA_14_TRIP02":                86 + 13569,                     # Setpoints.Temperatura14_TRIP02
        "TEMPERATURA_15_TRIP02":                87 + 13569,                     # Setpoints.Temperatura15_TRIP02
        "TEMPERATURA_16_TRIP02":                88 + 13569,                     # Setpoints.Temperatura16_TRIP02

        # Grade Suja
        "GradeSuja_TRIP":                       96 + 13569,                     # Setpoints.GradeSuja_TRIP

        # Curva
        "CURVA_01_DISTRIB_P1":                  97 + 13569,                     # Setpoints.Curva01_DistribuidorP1
        "CURVA_01_DISTRIB_P2":                  98 + 13569,                     # Setpoints.Curva01_DistribuidorP2
        "CURVA_01_DISTRIB_P3":                  99 + 13569,                     # Setpoints.Curva01_DistribuidorP3
        "CURVA_01_DISTRIB_P4":                  100 + 13569,                    # Setpoints.Curva01_DistribuidorP4
        "CURVA_01_DISTRIB_P5":                  101 + 13569,                    # Setpoints.Curva01_DistribuidorP5
        "CURVA_01_DISTRIB_P6":                  102 + 13569,                    # Setpoints.Curva01_DistribuidorP6
        "CURVA_01_DISTRIB_P7":                  103 + 13569,                    # Setpoints.Curva01_DistribuidorP7
        "CURVA_01_DISTRIB_P8":                  104 + 13569,                    # Setpoints.Curva01_DistribuidorP8
        "CURVA_01_DISTRIB_P9":                  105 + 13569,                    # Setpoints.Curva01_DistribuidorP9
        "CURVA_01_DISTRIB_P10":                 106 + 13569,                    # Setpoints.Curva01_DistribuidorP10
        "CURVA_01_ROTOR_P1":                    107 + 13569,                    # Setpoints.Curva01_RotorP1
        "CURVA_01_ROTOR_P2":                    108 + 13569,                    # Setpoints.Curva01_RotorP2
        "CURVA_01_ROTOR_P3":                    109 + 13569,                    # Setpoints.Curva01_RotorP3
        "CURVA_01_ROTOR_P4":                    110 + 13569,                    # Setpoints.Curva01_RotorP4
        "CURVA_01_ROTOR_P5":                    111 + 13569,                    # Setpoints.Curva01_RotorP5
        "CURVA_01_ROTOR_P6":                    112 + 13569,                    # Setpoints.Curva01_RotorP6
        "CURVA_01_ROTOR_P7":                    113 + 13569,                    # Setpoints.Curva01_RotorP7
        "CURVA_01_ROTOR_P8":                    114 + 13569,                    # Setpoints.Curva01_RotorP8
        "CURVA_01_ROTOR_P9":                    115 + 13569,                    # Setpoints.Curva01_RotorP9
        "CURVA_01_ROTOR_P10":                   116 + 13569,                    # Setpoints.Curva01_RotorP10
        "CURVA_02_DISTRIB_P1":                  117 + 13569,                    # Setpoints.Curva02_DistribuidorP1
        "CURVA_02_DISTRIB_P2":                  118 + 13569,                    # Setpoints.Curva02_DistribuidorP2
        "CURVA_02_DISTRIB_P3":                  119 + 13569,                    # Setpoints.Curva02_DistribuidorP3
        "CURVA_02_DISTRIB_P4":                  120 + 13569,                    # Setpoints.Curva02_DistribuidorP4
        "CURVA_02_DISTRIB_P5":                  121 + 13569,                    # Setpoints.Curva02_DistribuidorP5
        "CURVA_02_DISTRIB_P6":                  122 + 13569,                    # Setpoints.Curva02_DistribuidorP6
        "CURVA_02_DISTRIB_P7":                  123 + 13569,                    # Setpoints.Curva02_DistribuidorP7
        "CURVA_02_DISTRIB_P8":                  124 + 13569,                    # Setpoints.Curva02_DistribuidorP8
        "CURVA_02_DISTRIB_P9":                  125 + 13569,                    # Setpoints.Curva02_DistribuidorP9
        "CURVA_02_DISTRIB_P10":                 126 + 13569,                    # Setpoints.Curva02_DistribuidorP10
        "CURVA_02_ROTOR_P1":                    127 + 13569,                    # Setpoints.Curva02_RotorP1
        "CURVA_02_ROTOR_P2":                    128 + 13569,                    # Setpoints.Curva02_RotorP2
        "CURVA_02_ROTOR_P3":                    129 + 13569,                    # Setpoints.Curva02_RotorP3
        "CURVA_02_ROTOR_P4":                    130 + 13569,                    # Setpoints.Curva02_RotorP4
        "CURVA_02_ROTOR_P5":                    131 + 13569,                    # Setpoints.Curva02_RotorP5
        "CURVA_02_ROTOR_P6":                    132 + 13569,                    # Setpoints.Curva02_RotorP6
        "CURVA_02_ROTOR_P7":                    133 + 13569,                    # Setpoints.Curva02_RotorP7
        "CURVA_02_ROTOR_P8":                    134 + 13569,                    # Setpoints.Curva02_RotorP8
        "CURVA_02_ROTOR_P9":                    135 + 13569,                    # Setpoints.Curva02_RotorP9
        "CURVA_02_ROTOR_P10":                   136 + 13569,                    # Setpoints.Curva02_RotorP10
        "CURVA_03_DISTRIB_P1":                  137 + 13569,                    # Setpoints.Curva03_DistribuidorP1
        "CURVA_03_DISTRIB_P2":                  138 + 13569,                    # Setpoints.Curva03_DistribuidorP2
        "CURVA_03_DISTRIB_P3":                  139 + 13569,                    # Setpoints.Curva03_DistribuidorP3
        "CURVA_03_DISTRIB_P4":                  140 + 13569,                    # Setpoints.Curva03_DistribuidorP4
        "CURVA_03_DISTRIB_P5":                  141 + 13569,                    # Setpoints.Curva03_DistribuidorP5
        "CURVA_03_DISTRIB_P6":                  142 + 13569,                    # Setpoints.Curva03_DistribuidorP6
        "CURVA_03_DISTRIB_P7":                  143 + 13569,                    # Setpoints.Curva03_DistribuidorP7
        "CURVA_03_DISTRIB_P8":                  144 + 13569,                    # Setpoints.Curva03_DistribuidorP8
        "CURVA_03_DISTRIB_P9":                  145 + 13569,                    # Setpoints.Curva03_DistribuidorP9
        "CURVA_03_DISTRIB_P10":                 146 + 13569,                    # Setpoints.Curva03_DistribuidorP10
        "CURVA_03_ROTOR_P1":                    147 + 13569,                    # Setpoints.Curva03_RotorP1
        "CURVA_03_ROTOR_P2":                    148 + 13569,                    # Setpoints.Curva03_RotorP2
        "CURVA_03_ROTOR_P3":                    149 + 13569,                    # Setpoints.Curva03_RotorP3
        "CURVA_03_ROTOR_P4":                    150 + 13569,                    # Setpoints.Curva03_RotorP4
        "CURVA_03_ROTOR_P5":                    151 + 13569,                    # Setpoints.Curva03_RotorP5
        "CURVA_03_ROTOR_P6":                    152 + 13569,                    # Setpoints.Curva03_RotorP6
        "CURVA_03_ROTOR_P7":                    153 + 13569,                    # Setpoints.Curva03_RotorP7
        "CURVA_03_ROTOR_P8":                    154 + 13569,                    # Setpoints.Curva03_RotorP8
        "CURVA_03_ROTOR_P9":                    155 + 13569,                    # Setpoints.Curva03_RotorP9
        "CURVA_03_ROTOR_P10":                   156 + 13569,                    # Setpoints.Curva03_RotorP10
        "CURVA_04_DISTRIB_P1":                  157 + 13569,                    # Setpoints.Curva04_DistribuidorP1
        "CURVA_04_DISTRIB_P2":                  158 + 13569,                    # Setpoints.Curva04_DistribuidorP2
        "CURVA_04_DISTRIB_P3":                  159 + 13569,                    # Setpoints.Curva04_DistribuidorP3
        "CURVA_04_DISTRIB_P4":                  160 + 13569,                    # Setpoints.Curva04_DistribuidorP4
        "CURVA_04_DISTRIB_P5":                  161 + 13569,                    # Setpoints.Curva04_DistribuidorP5
        "CURVA_04_DISTRIB_P6":                  162 + 13569,                    # Setpoints.Curva04_DistribuidorP6
        "CURVA_04_DISTRIB_P7":                  163 + 13569,                    # Setpoints.Curva04_DistribuidorP7
        "CURVA_04_DISTRIB_P8":                  164 + 13569,                    # Setpoints.Curva04_DistribuidorP8
        "CURVA_04_DISTRIB_P9":                  165 + 13569,                    # Setpoints.Curva04_DistribuidorP9
        "CURVA_04_DISTRIB_P10":                 166 + 13569,                    # Setpoints.Curva04_DistribuidorP10
        "CURVA_04_ROTOR_P1":                    167 + 13569,                    # Setpoints.Curva04_RotorP1
        "CURVA_04_ROTOR_P2":                    168 + 13569,                    # Setpoints.Curva04_RotorP2
        "CURVA_04_ROTOR_P3":                    169 + 13569,                    # Setpoints.Curva04_RotorP3
        "CURVA_04_ROTOR_P4":                    170 + 13569,                    # Setpoints.Curva04_RotorP4
        "CURVA_04_ROTOR_P5":                    171 + 13569,                    # Setpoints.Curva04_RotorP5
        "CURVA_04_ROTOR_P6":                    172 + 13569,                    # Setpoints.Curva04_RotorP6
        "CURVA_04_ROTOR_P7":                    173 + 13569,                    # Setpoints.Curva04_RotorP7
        "CURVA_04_ROTOR_P8":                    174 + 13569,                    # Setpoints.Curva04_RotorP8
        "CURVA_04_ROTOR_P9":                    175 + 13569,                    # Setpoints.Curva04_RotorP9
        "CURVA_04_ROTOR_P10":                   176 + 13569,                    # Setpoints.Curva04_RotorP10
        "CURVA_05_DISTRIB_P1":                  177 + 13569,                    # Setpoints.Curva05_DistribuidorP1
        "CURVA_05_DISTRIB_P2":                  178 + 13569,                    # Setpoints.Curva05_DistribuidorP2
        "CURVA_05_DISTRIB_P3":                  179 + 13569,                    # Setpoints.Curva05_DistribuidorP3
        "CURVA_05_DISTRIB_P4":                  180 + 13569,                    # Setpoints.Curva05_DistribuidorP4
        "CURVA_05_DISTRIB_P5":                  181 + 13569,                    # Setpoints.Curva05_DistribuidorP5
        "CURVA_05_DISTRIB_P6":                  182 + 13569,                    # Setpoints.Curva05_DistribuidorP6
        "CURVA_05_DISTRIB_P7":                  183 + 13569,                    # Setpoints.Curva05_DistribuidorP7
        "CURVA_05_DISTRIB_P8":                  184 + 13569,                    # Setpoints.Curva05_DistribuidorP8
        "CURVA_05_DISTRIB_P9":                  185 + 13569,                    # Setpoints.Curva05_DistribuidorP9
        "CURVA_05_DISTRIB_P10":                 186 + 13569,                    # Setpoints.Curva05_DistribuidorP10
        "CURVA_05_ROTOR_P1":                    187 + 13569,                    # Setpoints.Curva05_RotorP1
        "CURVA_05_ROTOR_P2":                    188 + 13569,                    # Setpoints.Curva05_RotorP2
        "CURVA_05_ROTOR_P3":                    189 + 13569,                    # Setpoints.Curva05_RotorP3
        "CURVA_05_ROTOR_P4":                    190 + 13569,                    # Setpoints.Curva05_RotorP4
        "CURVA_05_ROTOR_P5":                    191 + 13569,                    # Setpoints.Curva05_RotorP5
        "CURVA_05_ROTOR_P6":                    192 + 13569,                    # Setpoints.Curva05_RotorP6
        "CURVA_05_ROTOR_P7":                    193 + 13569,                    # Setpoints.Curva05_RotorP7
        "CURVA_05_ROTOR_P8":                    194 + 13569,                    # Setpoints.Curva05_RotorP8
        "CURVA_05_ROTOR_P9":                    195 + 13569,                    # Setpoints.Curva05_RotorP9
        "CURVA_05_ROTOR_P10":                   196 + 13569,                    # Setpoints.Curva05_RotorP10

        # Referencia Curva
        "REFER_CURVA_01":                       197 + 13569,                    # Setpoints.ReferenciaCurva01
        "REFER_CURVA_02":                       198 + 13569,                    # Setpoints.ReferenciaCurva02
        "REFER_CURVA_03":                       199 + 13569,                    # Setpoints.ReferenciaCurva03
        "REFER_CURVA_04":                       200 + 13569,                    # Setpoints.ReferenciaCurva04
        "REFER_CURVA_05":                       201 + 13569,                    # Setpoints.ReferenciaCurva05

        # Outros
        "TEMPO_ATUALIZACAO":                    202 + 13569,                    # Setpoints.TempoAtualizacao
        "MODO_OPERACAO_RETENTIVO":              203 + 13569,                    # Setpoints.ModoOperacao_Retentivo
        "CURVA_SEL_RETENTIVO":                  204 + 13569,                    # Setpoints.CurvaSelecionada_Retentivo


        ## LEITURAS

        # Nível
        "NV_JUSANTE":                           2 + 12764,                      # Leituras.NivelJusante
        "NV_BARRAGEM":                          3 + 12764,                      # Leituras.NivelBarragem
        "NV_CANAL":                             4 + 12764,                      # Leituras.NivelCanal
        "NV_CAMARA_CARGA":                      5 + 12764,                      # Leituras.NivelCamaraCarga
        "QUEDA_BRUTA":                          131 + 12764,                    # Leituras.QuedaBruta

        # Operação
        "OPER_PAINEL_RESET_ALARMES":            [6 + 12764, 0],                 # Leituras.Operacao_PainelResetAlarmes
        "OPER_PAINEL_RECONHECE_ALARMES":        [7 + 12764, 1],                 # Leituras.Operacao_PainelReconheceAlarmes

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

        "OPER_INFO_PARADA":                     12 + 12764,                     # Leituras.Operacao_InfoParada
        "OPER_INFO_PARADA_NORMAL":              [12 + 12764, 0],                # Operacao.InfoParada.Normal
        "OPER_INFO_PARADA_EMERG":               [12 + 12764, 1],                # Operacao.InfoParada.Emergencia
        "OPER_INFO_PARADA_TRIP_AGUA":           [12 + 12764, 2],                # Operacao.InfoParada.TRIPAgua
        "OPER_INFO_PARADA_TRIP_M":              [12 + 12764, 3],                # Operacao.InfoParada.TRIPMecanico
        "OPER_INFO_PARADA_TRIP_E":              [12 + 12764, 4],                # Operacao.InfoParada.TRIPEletrico
        "OPER_INFO_PARADA_TRIP_H":              [12 + 12764, 5],                # Operacao.InfoParada.TRIPHidraulico
        "OPER_INFO_PARADA_RELIG_AUTO":          [12 + 12764, 6],                # Operacao.InfoParada.ReligamentoAutomatico
        "OPER_INFO_PARADA_PARTIDA_MANU":        [12 + 12764, 7],                # Operacao.InfoParada.PartidaManual
        "OPER_INFO_PARADA_INFO_INVAL":          [12 + 12764, 15],               # Operacao.InfoParada.ParadaInfoValida

        # UHCT
        "UHCT_INFO":                            13 + 12764,                     # Leituras.UHCT_Info
        "UHCT_OPERACIONAL":                     [13 + 12764, 0],                # UHCT.Info.Operacional
        "UHCT_LIGADA":                          [13 + 12764, 1],                # UHCT.Info.Ligada
        "UHCT_SENS_DESATIVADO":                 [13 + 12764, 2],                # UHCT.Info.SensorDesativado
        "UHCT_MODO_LOCAL":                      [13 + 12764, 3],                # UHCT.Info.ModoLocal

        "UHCT_BOMBAS":                          14 + 12764,                     # Leituras.UHCT_Bombas
        "UHCT_BOMBAS01":                        [14 + 12764, 0],                # UHCT.Bombas.Bomba01
        "UHCT_BOMBAS02":                        [14 + 12764, 1],                # UHCT.Bombas.Bomba02
        "UHCT_BOMBAS03":                        [14 + 12764, 2],                # UHCT.Bombas.Bomba03

        "UHCT_RODIZIO":                         15 + 12764,                     # Leituras.UHCT_Rodizio
        "UHCT_RODIZ_HABILITADO":                [15 + 12764, 0],                # UHCT.Rodizio.RodizioHabilitado
        "UHCT_RODIZ_BOMBA01":                   [15 + 12764, 1],                # UHCT.Rodizio.Bomba01
        "UHCT_RODIZ_BOMBA02":                   [15 + 12764, 2],                # UHCT.Rodizio.Bomba02

        "UHCT_VALVULAS":                        16 + 12764,                     # Leituras.UHCT_Valvulas
        "UHCT_VALVULAS01":                      [16 + 12764, 0],                # UHCT.Valvulas.Valvulas01
        "UHCT_VALVULAS02":                      [16 + 12764, 1],                # UHCT.Valvulas.Valvulas02
        "UHCT_VALVULAS03":                      [16 + 12764, 2],                # UHCT.Valvulas.Valvulas03
        "UHCT_VALVULAS04":                      [16 + 12764, 3],                # UHCT.Valvulas.Valvulas04

        "UHCT_FILTROS":                         17 + 12764,                     # Leituras.UHCT_Filtros
        "UHCT_FILTROS01":                       [17 + 12764, 0],                # UHCT.Filtros.Filtro01
        "UHCT_FILTROS02":                       [17 + 12764, 1],                # UHCT.Filtros.Filtro02
        "UHCT_FILTROS03":                       [17 + 12764, 2],                # UHCT.Filtros.Filtro03
        "UHCT_FILTROS04":                       [17 + 12764, 3],                # UHCT.Filtros.Filtro04
        "UHCT_FILTROS05":                       [17 + 12764, 4],                # UHCT.Filtros.Filtro05

        "UHCT_PRESSOSTATOS":                    18 + 12764,                     # Leituras.UHCT_Pressostatos
        "UHCT_PRESSOSTATO01":                   [18 + 12764, 0],                # UHCT.Pressostatos.Pressostato01
        "UHCT_PRESSOSTATO02":                   [18 + 12764, 1],                # UHCT.Pressostatos.Pressostato02
        "UHCT_PRESSOSTATO03":                   [18 + 12764, 2],                # UHCT.Pressostatos.Pressostato03

        "UHCT_NIVEL_OLEO":                      19 + 12764,                     # Leituras.UHCT_NivelOleo
        "UHCT_NIVEL_OLEO_LL":                   [19 + 12764, 0],                # UHCT.NivelOleo.LL
        "UHCT_NIVEL_OLEO_L":                    [19 + 12764, 1],                # UHCT.NivelOleo.L
        "UHCT_NIVEL_OLEO_H":                    [19 + 12764, 2],                # UHCT.NivelOleo.H
        "UHCT_NIVEL_OLEO_HH":                   [19 + 12764, 3],                # UHCT.NivelOleo.HH

        "UHCT_PRESSAO_OLEO":                    20 + 12764,                     # Leituras.UHCT_PressaoOleo
        "UHCT_ACUM_RODIZIO_PRINCIPAL":          21 + 12764,                     # Leituras.UHCT_AcumuladorRodizioPrincipal
        "UHCT_ACUM_RODIZIO_RETAGUARDA":         22 + 12764,                     # Leituras.UHCT_AcumuladorRodizioRetaguarda

        # UHLM
        "UHLM_INFO":                            23 + 12764,                     # Leituras.UHLM_Info
        "UHLM_OPERACIONAL":                     [23 + 12764, 0],                # UHLM.Info.Operacional
        "UHLM_LIGADA":                          [23 + 12764, 1],                # UHLM.Info.Ligada
        "UHLM_MODO_LOCAL":                      [23 + 12764, 2],                # UHLM.Info.ModoLocal
        "UHLM_VALV_BOMBA_MECAN":                [23 + 12764, 3],                # UHLM.Info.UHLM_ValvulaBombaMecanica
        "UHLM_VALV_ENTRA_TRO_CALO_ABER":        [23 + 12764, 4],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Aberta
        "UHLM_VALV_ENTRA_TRO_CALO_FECH":        [23 + 12764, 5],                # UHLM.Info.UHLM_ValvulaEntradaTrocadorCalor_Fechada
        "UHLM_VALV_SAI_TRO_CALO_ABER":          [23 + 12764, 6],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Aberta
        "UHLM_VALV_SAI_TRO_CALO_FECH":          [23 + 12764, 7],                # UHLM.Info.UHLM_ValvulaSaidaTrocadorCalor_Fechada
        "UHLM_BOMBA_RETAG_OPERAC":              [23 + 12764, 8],                # UHLM.Info.UHLM_BombaRetaguarda_Operacional

        "UHLM_BOMBAS":                          24 + 12764,                     # Leituras.UHLM_Bombas
        "UHLM_BOMBA01":                         [24 + 12764, 0],                # UHLM.Bombas.Bomba01
        "UHLM_BOMBA02":                         [24 + 12764, 1],                # UHLM.Bombas.Bomba02
        "UHLM_BOMBA03":                         [24 + 12764, 2],                # UHLM.Bombas.Bomba03
        "UHLM_BOMBA04":                         [24 + 12764, 3],                # UHLM.Bombas.Bomba04

        "UHLM_RODIZIO":                         25 + 12764,                     # Leituras.UHLM_Rodizio
        "UHLM_RODIZ_HABILITADO":                [25 + 12764, 0],                # UHLM.Rodizio.RodizioHabilitado
        "UHLM_RODIZ_BOMBA01":                   [25 + 12764, 1],                # UHLM.Rodizio.Bomba01
        "UHLM_RODIZ_BOMBA02":                   [25 + 12764, 2],                # UHLM.Rodizio.Bomba02

        "UHLM_FILTROS":                         26 + 12764,                     # Leituras.UHLM_Filtros
        "UHLM_FILTRO01":                        [26 + 12764, 0],                # UHLM.Filtros.Filtro01
        "UHLM_FILTRO02":                        [26 + 12764, 1],                # UHLM.Filtros.Filtro02
        "UHLM_FILTRO03":                        [26 + 12764, 2],                # UHLM.Filtros.Filtro03
        "UHLM_FILTRO04":                        [26 + 12764, 3],                # UHLM.Filtros.Filtro04
        "UHLM_FILTRO05":                        [26 + 12764, 4],                # UHLM.Filtros.Filtro05

        "UHLM_PRESSOSTATOS":                    27 + 12764,                     # Leituras.UHLM_Pressostatos
        "UHLM_PRESSOSTATO01":                   [27 + 12764, 0],                # UHLM.Pressostatos.Pressostato01
        "UHLM_PRESSOSTATO02":                   [27 + 12764, 1],                # UHLM.Pressostatos.Pressostato02
        "UHLM_PRESSOSTATO03":                   [27 + 12764, 2],                # UHLM.Pressostatos.Pressostato03
        "UHLM_PRESSOSTATO04":                   [27 + 12764, 3],                # UHLM.Pressostatos.Pressostato04

        "UHLM_FLUXOSTATOS":                     28 + 12764,                     # Leituras.UHLM_Fluxostatos
        "UHLM_FLUXOSTATO01":                    [28 + 12764, 0],                # UHLM.Fluxostatos.Fluxostato01
        "UHLM_FLUXOSTATO02":                    [28 + 12764, 1],                # UHLM.Fluxostatos.Fluxostato02
        "UHLM_FLUXOSTATO03":                    [28 + 12764, 2],                # UHLM.Fluxostatos.Fluxostato03
        "UHLM_FLUXOSTATO04":                    [28 + 12764, 3],                # UHLM.Fluxostatos.Fluxostato04
        "UHLM_FLUXOSTATO05":                    [28 + 12764, 4],                # UHLM.Fluxostatos.Fluxostato05
        "UHLM_FLUXOSTATO06":                    [28 + 12764, 5],                # UHLM.Fluxostatos.Fluxostato06
        "UHLM_FLUXOSTATO07":                    [28 + 12764, 6],                # UHLM.Fluxostatos.Fluxostato07

        "UHLM_NIVEL_OLEO":                      29 + 12764,                     # Leituras.UHLM_NivelOleo
        "UHLM_NIVEL_OLEO_LL":                   [29 + 12764, 0],                # UHLM.NivelOleo.LL
        "UHLM_NIVEL_OLEO_L":                    [29 + 12764, 1],                # UHLM.NivelOleo.L
        "UHLM_NIVEL_OLEO_H":                    [29 + 12764, 2],                # UHLM.NivelOleo.H
        "UHLM_NIVEL_OLEO_HH":                   [29 + 12764, 3],                # UHLM.NivelOleo.HH

        "UHLM_ACUM_RODIZIO_PRINCIPAL":          30 + 12764,                     # Leituras.UHLM_AcumuladorRodizioPrincipal
        "UHLM_ACUM_RODIZIO_RETAGUARDA":         31 + 12764,                     # Leituras.UHLM_AcumuladorRodizioRetaguarda

        "UHLM_FLUXOSTATO_OLEO_01":              123 + 12764,                    # Leituras.UHLM_FluxostatoOleo01
        "UHLM_FLUXOSTATO_OLEO_02":              124 + 12764,                    # Leituras.UHLM_FluxostatoOleo02
        "UHLM_FLUXOSTATO_OLEO_03":              125 + 12764,                    # Leituras.UHLM_FluxostatoOleo03
        "UHLM_FLUXOSTATO_OLEO_04":              126 + 12764,                    # Leituras.UHLM_FluxostatoOleo04

        # Turbina
        "TURB_INFO":                            32 + 12764,                     # Leituras.Turb_Info
        "TURB_EQUALIZADA":                      [32 + 12764, 0],                # Turbina.Info.Equalizada
        "TURB_PRONTA":                          [32 + 12764, 1],                # Turbina.Info.Pronta
        "TURB_FECHADA":                         [32 + 12764, 2],                # Turbina.Info.Fechada
        "TURB_TRAVADA":                         [32 + 12764, 3],                # Turbina.Info.Travada
        "TURB_PARADA":                          [32 + 12764, 4],                # Turbina.Info.Parada
        "TURB_EQUALIZANDO":                     [32 + 12764, 5],                # Turbina.Info.Equalizando
        "TURB_FECHANDO":                        [32 + 12764, 6],                # Turbina.Info.Fechando
        "TURB_SENS_DESATIVADO":                 [32 + 12764, 7],                # Turbina.Info.SensorDesativado
        "TURB_DISTRI_FECHADO":                  [32 + 12764, 8],                # Turbina.Info.DistribuidorFechado

        "TURB_VALVULA_BYPASS":                  33 + 12764,                     # Leituras.Turb_ValvulaByPass
        "TURB_VALV_BY_ACIONA":                  [33 + 12764, 0],                # Turbina.Bypass.Acionamento
        "TURB_VALV_BY_FECHADO":                 [33 + 12764, 1],                # Turbina.Bypass.Fechado
        "TURB_VALV_BY_ABERTO":                  [33 + 12764, 2],                # Turbina.Bypass.Aberto

        "TURB_VALVULA_BORBOLETA":               34 + 12764,                     # Leituras.Turb_ValvulaBorboleta
        "TURB_VALV_BORB_ACIONA":                [34 + 12764, 0],                # Turbina.Borboleta.Acionamento
        "TURB_VALV_BORB_FECHADA":               [34 + 12764, 1],                # Turbina.Borboleta.Fechada
        "TURB_VALV_BORB_ABERTA":                [34 + 12764, 2],                # Turbina.Borboleta.Aberta
        "TURB_VALV_BORB_DERIVA":                [34 + 12764, 3],                # Turbina.Borboleta.Deriva
        "TURB_VALV_BORB_TRAVADA":               [34 + 12764, 4],                # Turbina.Borboleta.Travada
        "TURB_VALV_BORB_MANTEM":                [34 + 12764, 5],                # Turbina.Borboleta.Mantem

        "TURB_TEMPO_CRACK_EFETIVO":             35 + 12764,                     # Leituras.Turb_TempoCrackEfetivo
        "TURB_TEMPO_EQUAL_EFETIVO":             36 + 12764,                     # Leituras.Turb_TempoEqualizacaoEfetivo
        "TURB_PRESSAO_CONDUTO":                 37 + 12764,                     # Leituras.Turb_PressaoConduto
        "TURB_PRESSAO_CAIXA_ESPIRAL":           38 + 12764,                     # Leituras.Turb_PressaoCaixaEspiral
        "TURB_VAZAO_TURBINADA":                 39 + 12764,                     # Leituras.Turb_VazaoTurbinada
        "TURB_VIBRACAO_01":                     40 + 12764,                     # Leituras.Turb_Vibracao01
        "TURB_VIBRACAO_02":                     41 + 12764,                     # Leituras.Turb_Vibracao02
        "TURB_VIBRACAO_03":                     42 + 12764,                     # Leituras.Turb_Vibracao03
        "TURB_VIBRACAO_04":                     43 + 12764,                     # Leituras.Turb_Vibracao04

        "TURB_FRENAGEM":                        44 + 12764,                     # Leituras.Turb_Frenagem
        "TURB_FRENA_APLICADO":                  [44 + 12764, 0],                # Turbina.Frenagem.Info.Aplicado
        "TURB_FRENA_MANUAL":                    [44 + 12764, 1],                # Turbina.Frenagem.Info.Manual
        "TURB_FRENA_PRESSOS":                   [44 + 12764, 2],                # Turbina.Frenagem.Info.Pressostato
        "TURB_FRENA_1ZE":                       [44 + 12764, 3],                # Turbina.Frenagem.Info.[1ZE]
        "TURB_FRENA_2ZE":                       [44 + 12764, 4],                # Turbina.Frenagem.Info.[2ZE]

        "TURB_VIBRACAO_05":                     127 + 12764,                    # Leituras.Turb_Vibracao05

        # Reg V
        "REG_V_INFO":                           45 + 12764,                     # Leituras.RegV_Info
        "REG_V_HABILITADO":                     [45 + 12764, 0],                # RegV.Info.Habilitado
        "REG_V_BASE_CARGA":                     [45 + 12764, 1],                # RegV.Info.BaseCarga
        "REG_V_RPM30":                          [45 + 12764, 2],                # RegV.Info.RPM30
        "REG_V_RPM90":                          [45 + 12764, 3],                # RegV.Info.RPM90
        "REG_V_CARGA_ZERADA":                   [45 + 12764, 4],                # RegV.Info.CargaZerada
        "REG_V_MODO_ESTATISMO":                 [45 + 12764, 5],                # RegV.Info.ModoEstatismo
        "REG_V_MODO_BASE_CARGA":                [45 + 12764, 6],                # RegV.Info.ModoBaseCarga
        "REG_V_DISTRI_FECHADO":                 [45 + 12764, 7],                # RegV.Info.DistribuidorFechado

        "REG_V_ESTADO":                         46 + 12764,                     # Leituras.RegV_Estado
        "REG_V_FALHA":                          [46 + 12764, 0],                # RegV.Estado.Falha
        "REG_V_PARADO":                         [46 + 12764, 1],                # RegV.Estado.Parado
        "REG_V_CTRL_MANUAL_DISTRI":             [46 + 12764, 2],                # RegV.Estado.ControleManualDistribuidor
        "REG_V_CTRL_MANUAL_VALV":               [46 + 12764, 3],                # RegV.Estado.ControleManualValvula
        "REG_V_CTRL_VELOC":                     [46 + 12764, 4],                # RegV.Estado.ControleVelocidade
        "REG_V_COMPENSA_POT_ATIVA":             [46 + 12764, 5],                # RegV.Estado.CompensacaoPotenciaAtiva
        "REG_V_CTRL_POT_ATIVA":                 [46 + 12764, 6],                # RegV.Estado.ControlePotenciaAtiva

        "REG_V_VELOCIDADE":                     47 + 12764,                     # Leituras.RegV_Velocidade
        "REG_V_DISTRIBUIDOR":                   48 + 12764,                     # Leituras.RegV_Distribuidor
        "REG_V_ROTOR":                          49 + 12764,                     # Leituras.RegV_Rotor
        "REG_V_POT_ALVO":                       50 + 12764,                     # Leituras.RegV_PotenciaAlvo

        "REG_V_CONJUGADO_INFO":                 128 + 12764,                    # Leituras.RegV_CurvaConjugacao_Info
        "REG_V_CONJ_AUTOMATICO":                [128 + 12764, 0],               # RegV.Conjugado.Automatico
        "REG_V_CONJ_MANUAL":                    [128 + 12764, 1],               # RegV.Conjugado.Manual
        "REG_V_CONJUGADO1":                     [128 + 12764, 2],               # RegV.Conjugado.Conjugado1
        "REG_V_CONJUGADO2":                     [128 + 12764, 3],               # RegV.Conjugado.Conjugado2
        "REG_V_CONJUGADO3":                     [128 + 12764, 4],               # RegV.Conjugado.Conjugado3

        # Reg T
        "REG_T_INFO":                           51 + 12764,                     # Leituras.RegT_Info
        "REG_T_HABILITACAO":                    [51 + 12764, 0],                # RegT.Info.Habilitacao
        "REG_T_TENSAO_ESTAB":                   [51 + 12764, 1],                # RegT.Info.TensaoEstabilizada
        "REG_T_CONTATOR_ABERTO":                [51 + 12764, 2],                # RegT.Info.ContatorAberto
        "REG_T_CONTATOR_FECHADO":               [51 + 12764, 3],                # RegT.Info.ContatorFechado
        "REG_T_PRE_EXCITACAO":                  [51 + 12764, 4],                # RegT.Info.PreExcitacao
        "REG_T_MTVC":                           [51 + 12764, 5],                # RegT.Info.MTVC
        "REG_T_MECC":                           [51 + 12764, 6],                # RegT.Info.MECC
        "REG_T_OPER_ONLINE":                    [51 + 12764, 7],                # RegT.Info.OperacaoOnline
        "REG_T_OPER_PARALELA":                  [51 + 12764, 9],                # RegT.Info.OperacaoParalela

        "REG_T_UEXCITACAO":                     52 + 12764,                     # Leituras.RegT_UExcitacao
        "REG_T_IEXCITACAO":                     53 + 12764,                     # Leituras.RegT_IExcitacao
        "REG_T_FPALVO":                         129 + 12764,                    # Leituras.RegT_FPAlvo
        "REG_T_REATIVO_ALVO":                   130 + 12764,                    # Leituras.RegT_ReativoAlvo

        # Sinc
        "SINC_INFO":                            54 + 12764,                     # Leituras.Sinc_Info
        "SINC_HABILITADO":                      [54 + 12764, 0],                # Sincronoscopio.Info.Habilitado
        "SINC_MODO_AUTO":                       [54 + 12764, 1],                # Sincronoscopio.Info.ModoAutomatico
        "SINC_MODO_MANUAL":                     [54 + 12764, 2],                # Sincronoscopio.Info.ModoManual
        "SINC_BARRA_MORTA":                     [54 + 12764, 3],                # Sincronoscopio.Info.BarraMorta

        "SINC_FREQ_GERADOR":                    55 + 12764,                     # Leituras.Sinc_FrequenciaGerador
        "SINC_FREQ_BARRA":                      56 + 12764,                     # Leituras.Sinc_FrequenciaBarra
        "SINC_TENSAO_GERADOR":                  57 + 12764,                     # Leituras.Sinc_TensaoGerador
        "SINC_TENSAO_BARRA":                    58 + 12764,                     # Leituras.Sinc_TensaoBarra

        # DJ
        "Dj52G_INFO":                           59 + 12764,                     # Leituras.Disj52G_Info
        "Dj52G_ABERTO":                         [59 + 12764, 0],                # Disjuntor52G.Info.Aberto
        "Dj52G_FECHADO":                        [59 + 12764, 1],                # Disjuntor52G.Info.Fechado
        "Dj52G_INCONSISTENTE":                  [59 + 12764, 2],                # Disjuntor52G.Info.Inconsistente
        "Dj52G_TRIP":                           [59 + 12764, 3],                # Disjuntor52G.Info.TRIP
        "Dj52G_TESTE":                          [59 + 12764, 4],                # Disjuntor52G.Info.Teste
        "Dj52G_INSERIDO":                       [59 + 12764, 5],                # Disjuntor52G.Info.Inserido
        "Dj52G_EXTRAIVEL":                      [59 + 12764, 6],                # Disjuntor52G.Info.Extraivel
        "Dj52G_MOLA_CARRE":                     [59 + 12764, 7],                # Disjuntor52G.Info.MolaCarregada
        "Dj52G_CONDICAO":                       [59 + 12764, 8],                # Disjuntor52G.Info.CondicaoFechamento
        "Dj52G_FALTA_VCC":                      [59 + 12764, 9],                # Disjuntor52G.Info.FaltaVCC

        # Tensão
        "TENSAO_RN":                            60 + 12764,                     # Leituras.Gerador_TensaoRN
        "TENSAO_SN":                            61 + 12764,                     # Leituras.Gerador_TensaoSN
        "TENSAO_TN":                            62 + 12764,                     # Leituras.Gerador_TensaoTN
        "TENSAO_RS":                            63 + 12764,                     # Leituras.Gerador_TensaoRS
        "TENSAO_ST":                            64 + 12764,                     # Leituras.Gerador_TensaoST
        "TENSAO_TR":                            65 + 12764,                     # Leituras.Gerador_TensaoTR

        # Corrente
        "CORRENTE_R":                           66 + 12764,                     # Leituras.Gerador_CorrenteR
        "CORRENTE_S":                           67 + 12764,                     # Leituras.Gerador_CorrenteS
        "CORRENTE_T":                           68 + 12764,                     # Leituras.Gerador_CorrenteT
        "CORRENTE_MEDIA":                       69 + 12764,                     # Leituras.Gerador_CorrenteMedia

        # Potência Ativa
        "POT_ATIVA_1":                          70 + 12764,                     # Leituras.Gerador_PotenciaAtiva1
        "POT_ATIVA_2":                          71 + 12764,                     # Leituras.Gerador_PotenciaAtiva2
        "POT_ATIVA_3":                          72 + 12764,                     # Leituras.Gerador_PotenciaAtiva3
        "POT_ATIVA_MEDIA":                      73 + 12764,                     # Leituras.Gerador_PotenciaAtivaMedia

        # Potência Reativa
        "POT_REATIVA_1":                        74 + 12764,                     # Leituras.Gerador_PotenciaReativa1
        "POT_REATIVA_2":                        75 + 12764,                     # Leituras.Gerador_PotenciaReativa2
        "POT_REATIVA_3":                        76 + 12764,                     # Leituras.Gerador_PotenciaReativa3
        "POT_REATIVA_MEDIA":                    77 + 12764,                     # Leituras.Gerador_PotenciaReativaMedia

        # Potência Aparente
        "POT_APARENTE_1":                       78 + 12764,                     # Leituras.Gerador_PotenciaAparente1
        "POT_APARENTE_2":                       79 + 12764,                     # Leituras.Gerador_PotenciaAparente2
        "POT_APARENTE_3":                       80 + 12764,                     # Leituras.Gerador_PotenciaAparente3
        "POT_APARENTE_MEDIA":                   81 + 12764,                     # Leituras.Gerador_PotenciaAparenteMedia

        # Fator Potência
        "FATOR_POT_1":                          82 + 12764,                     # Leituras.Gerador_FatorPotencia1
        "FATOR_POT_2":                          83 + 12764,                     # Leituras.Gerador_FatorPotencia2
        "FATOR_POT_3":                          84 + 12764,                     # Leituras.Gerador_FatorPotencia3
        "FATOR_POT_MEDIA":                      85 + 12764,                     # Leituras.Gerador_FatorPotenciaMedia

        # Frequencia
        "FREQUENCIA":                           86 + 12764,                     # Leituras.Gerador_Frequencia

        # Energia Fornecida
        "ENERGIA_FORNECIDA_TWh":                87 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTWh
        "ENERGIA_FORNECIDA_GWh":                88 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGWh
        "ENERGIA_FORNECIDA_MWh":                89 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMWh
        "ENERGIA_FORNECIDA_kWh":                90 + 12764,                     # Leituras.Gerador_EnergiaFornecidakWh
        "ENERGIA_FORNECIDA_TVarh":              91 + 12764,                     # Leituras.Gerador_EnergiaFornecidaTVarh
        "ENERGIA_FORNECIDA_GVarh":              92 + 12764,                     # Leituras.Gerador_EnergiaFornecidaGVarh
        "ENERGIA_FORNECIDA_MVarh":              93 + 12764,                     # Leituras.Gerador_EnergiaFornecidaMVarh
        "ENERGIA_FORNECIDA_kVarh":              94 + 12764,                     # Leituras.Gerador_EnergiaFornecidakVarh
        "ENERGIA_CORNECIDA_TVarh":              95 + 12764,                     # Leituras.Gerador_EnergiaConsumidaTVarh
        "ENERGIA_CORNECIDA_GVarh":              96 + 12764,                     # Leituras.Gerador_EnergiaConsumidaGVarh
        "ENERGIA_CORNECIDA_MVarh":              97 + 12764,                     # Leituras.Gerador_EnergiaConsumidaMVarh
        "ENERGIA_CORNECIDA_kVarh":              98 + 12764,                     # Leituras.Gerador_EnergiaConsumidakVarh
    
        "GERADOR_FP_INFO":                      99 + 12764,                     # Leituras.Gerador_FPInfo
        "GERADOR_FP_FASE1_IND":                 [99 + 12764, 0],                # Gerador.FP_Info.Fase1_Ind
        "GERADOR_FP_FASE1_CAP":                 [99 + 12764, 1],                # Gerador.FP_Info.Fase1_Cap
        "GERADOR_FP_FASE2_IND":                 [99 + 12764, 2],                # Gerador.FP_Info.Fase2_Ind
        "GERADOR_FP_FASE2_CAP":                 [99 + 12764, 3],                # Gerador.FP_Info.Fase2_Cap
        "GERADOR_FP_FASE3_IND":                 [99 + 12764, 4],                # Gerador.FP_Info.Fase3_Ind
        "GERADOR_FP_FASE3_CAP":                 [99 + 12764, 5],                # Gerador.FP_Info.Fase3_Cap
        "GERADOR_FP_FASE4_IND":                 [99 + 12764, 6],                # Gerador.FP_Info.Total_Ind
        "GERADOR_FP_FASE4_CAP":                 [99 + 12764, 7],                # Gerador.FP_Info.Total_Cap

        # Controles
        "CTRL_REATIVO_INFO":                    100 + 12764,                    # Leituras.CtrlReativo_Info
        "CTRL_REAT_MODO_FP":                    [100 + 12764, 0],               # CtrlReativo.Info.ModoFP
        "CTRL_REAT_MODO_VAR":                   [100 + 12764, 1],               # CtrlReativo.Info.ModoVar

        "CTRL_POTENCIA_INFO":                   101 + 12764,                    # Leituras.CtrlPotencia_Info
        "CTRL_POT_MODO_NIVEL":                  [101 + 12764, 0],               # CtrlPotencia.Info.ModoNivel
        "CTRL_POT_MODO_POT":                    [101 + 12764, 1],               # CtrlPotencia.Info.ModoPotencia
        "CTRL_POT_MODO_RELIGA_AUTO":            [101 + 12764, 2],               # CtrlPotencia.Info.ModoReligamentoAutomatico

        # Horimetros
        "HORIM_ELETR_LOW":                      102 + 12764,                    # Leituras.HorimetroEletrico_Low
        "HORIM_ELETR_HIGH":                     103 + 12764,                    # Leituras.HorimetroEletrico_High
        "HORIM_MECAN_LOW":                      104 + 12764,                    # Leituras.HorimetroMecanico_Low
        "HORIM_MECAN_HIGH":                     105 + 12764,                    # Leituras.HorimetroMecanico_High

        # Temperatura
        "TEMPERATURA_01":                       107 + 12764,                    # Leituras.Temperatura_01
        "TEMPERATURA_02":                       108 + 12764,                    # Leituras.Temperatura_02
        "TEMPERATURA_03":                       109 + 12764,                    # Leituras.Temperatura_03
        "TEMPERATURA_04":                       110 + 12764,                    # Leituras.Temperatura_04
        "TEMPERATURA_05":                       111 + 12764,                    # Leituras.Temperatura_05
        "TEMPERATURA_06":                       112 + 12764,                    # Leituras.Temperatura_06
        "TEMPERATURA_07":                       113 + 12764,                    # Leituras.Temperatura_07
        "TEMPERATURA_08":                       114 + 12764,                    # Leituras.Temperatura_08
        "TEMPERATURA_09":                       115 + 12764,                    # Leituras.Temperatura_09
        "TEMPERATURA_10":                       116 + 12764,                    # Leituras.Temperatura_10
        "TEMPERATURA_11":                       117 + 12764,                    # Leituras.Temperatura_11
        "TEMPERATURA_12":                       118 + 12764,                    # Leituras.Temperatura_12
        "TEMPERATURA_13":                       119 + 12764,                    # Leituras.Temperatura_13
        "TEMPERATURA_14":                       120 + 12764,                    # Leituras.Temperatura_14
        "TEMPERATURA_15":                       121 + 12764,                    # Leituras.Temperatura_15
        "TEMPERATURA_16":                       122 + 12764,                    # Leituras.Temperatura_16


        ## DISJUNTORES

        "DJ_01":                                0,
        "DJ_02":                                1,
        "DJ_03":                                2,
        "DJ_04":                                3,
        "DJ_05":                                4,
        "DJ_06":                                5,
        "DJ_07":                                6,
        "DJ_08":                                7,
        "DJ_09":                                8,
        "DJ_10":                                9,
        "DJ_11":                                10,
        "DJ_12":                                11,
        "DJ_13":                                12,
        "DJ_14":                                13,
        "DJ_15":                                14,
        "DJ_16":                                15,
        "DJ_17":                                16,
        "DJ_18":                                17,
        "DJ_19":                                18,
        "DJ_20":                                19,
        "DJ_21":                                20,
        "DJ_22":                                21,
        "DJ_23":                                22,
        "DJ_24":                                23,
        "DJ_25":                                24,
        "DJ_26":                                25,
        "DJ_27":                                26,
        "DJ_28":                                27,
        "DJ_29":                                28,
        "DJ_30":                                29,
        "DJ_31":                                30,
        "DJ_32":                                31,


        ## ALARMES

        # Específicos UG4
        "Alarme10_14":                          [10 + 14199, 14],
        "Alarme10_15":                          [10 + 14199, 15],

        "Alarme13_12":                          [13 + 14199, 12],
        "Alarme13_13":                          [13 + 14199, 13],
        "Alarme13_14":                          [13 + 14199, 14],
        "Alarme13_15":                          [13 + 14199, 15],

        "Alarme14_00":                          [14 + 14199, 0],
        "Alarme14_01":                          [14 + 14199, 1],
        "Alarme14_02":                          [14 + 14199, 2],

        "Alarme16_02":                          [16 + 14199, 2],
        "Alarme16_03":                          [16 + 14199, 3],


        # Gerais
        "Alarme01_01":                          [1 + 14199, 1],
        "Alarme01_02":                          [1 + 14199, 2],
        "Alarme01_00":                          [1 + 14199, 0],
        "Alarme01_03":                          [1 + 14199, 3],
        "Alarme01_06":                          [1 + 14199, 6],
        "Alarme01_07":                          [1 + 14199, 7],
        "Alarme01_08":                          [1 + 14199, 8],
        "Alarme01_09":                          [1 + 14199, 9],
        "Alarme01_10":                          [1 + 14199, 10],
        "Alarme01_11":                          [1 + 14199, 11],
        "Alarme01_12":                          [1 + 14199, 12],
        "Alarme01_13":                          [1 + 14199, 13],
        "Alarme01_14":                          [1 + 14199, 14],
        "Alarme01_15":                          [1 + 14199, 15],

        "Alarme02_00":                          [2 + 14199, 0],
        "Alarme02_01":                          [2 + 14199, 1],
        "Alarme02_02":                          [2 + 14199, 2],
        "Alarme02_03":                          [2 + 14199, 3],
        "Alarme02_04":                          [2 + 14199, 4],
        "Alarme02_05":                          [2 + 14199, 5],
        "Alarme02_06":                          [2 + 14199, 6],
        "Alarme02_07":                          [2 + 14199, 7],
        "Alarme02_08":                          [2 + 14199, 8],
        "Alarme02_09":                          [2 + 14199, 9],
        "Alarme02_10":                          [2 + 14199, 10],
        "Alarme02_11":                          [2 + 14199, 11],
        "Alarme02_12":                          [2 + 14199, 12],
        "Alarme02_13":                          [2 + 14199, 13],
        "Alarme02_14":                          [2 + 14199, 14],
        "Alarme02_15":                          [2 + 14199, 15],

        "Alarme03_00":                          [3 + 14199, 0],
        "Alarme03_01":                          [3 + 14199, 1],
        "Alarme03_02":                          [3 + 14199, 2],
        "Alarme03_03":                          [3 + 14199, 3],
        "Alarme03_04":                          [3 + 14199, 4],
        "Alarme03_05":                          [3 + 14199, 5],
        "Alarme03_06":                          [3 + 14199, 6],
        "Alarme03_07":                          [3 + 14199, 7],
        "Alarme03_08":                          [3 + 14199, 8],
        "Alarme03_09":                          [3 + 14199, 9],
        "Alarme03_10":                          [3 + 14199, 10],
        "Alarme03_11":                          [3 + 14199, 11],
        "Alarme03_12":                          [3 + 14199, 12],
        "Alarme03_13":                          [3 + 14199, 13],
        "Alarme03_14":                          [3 + 14199, 14],
        "Alarme03_15":                          [3 + 14199, 15],

        "Alarme04_00":                          [4 + 14199, 0],
        "Alarme04_01":                          [4 + 14199, 1],
        "Alarme04_02":                          [4 + 14199, 2],
        "Alarme04_04":                          [4 + 14199, 4],
        "Alarme04_05":                          [4 + 14199, 5],
        "Alarme04_06":                          [4 + 14199, 6],
        "Alarme04_07":                          [4 + 14199, 7],
        "Alarme04_09":                          [4 + 14199, 9],
        "Alarme04_10":                          [4 + 14199, 10],
        "Alarme04_11":                          [4 + 14199, 11],
        "Alarme04_12":                          [4 + 14199, 12],
        "Alarme04_13":                          [4 + 14199, 13],
        "Alarme04_14":                          [4 + 14199, 14],
        "Alarme04_15":                          [4 + 14199, 15],

        "Alarme05_00":                          [5 + 14199, 0],
        "Alarme05_02":                          [5 + 14199, 2],
        "Alarme05_03":                          [5 + 14199, 3],
        "Alarme05_04":                          [5 + 14199, 4],
        "Alarme05_05":                          [5 + 14199, 5],
        "Alarme05_06":                          [5 + 14199, 6],
        "Alarme05_07":                          [5 + 14199, 7],
        "Alarme05_09":                          [5 + 14199, 9],
        "Alarme05_10":                          [5 + 14199, 10],
        "Alarme05_11":                          [5 + 14199, 11],
        "Alarme05_12":                          [5 + 14199, 12],
        "Alarme05_13":                          [5 + 14199, 13],
        "Alarme05_14":                          [5 + 14199, 14],
        "Alarme05_15":                          [5 + 14199, 15],

        "Alarme06_00":                          [6 + 14199, 0],
        "Alarme06_03":                          [6 + 14199, 3],
        "Alarme06_04":                          [6 + 14199, 4],
        "Alarme06_05":                          [6 + 14199, 5],
        "Alarme06_08":                          [6 + 14199, 8],
        "Alarme06_09":                          [6 + 14199, 9],
        "Alarme06_10":                          [6 + 14199, 10],
        "Alarme06_11":                          [6 + 14199, 11],
        "Alarme06_12":                          [6 + 14199, 12],
        "Alarme06_13":                          [6 + 14199, 13],
        "Alarme06_14":                          [6 + 14199, 14],
        "Alarme06_15":                          [6 + 14199, 15],

        "Alarme07_00":                          [7 + 14199, 0],
        "Alarme07_01":                          [7 + 14199, 1],
        "Alarme07_02":                          [7 + 14199, 2],
        "Alarme07_03":                          [7 + 14199, 3],
        "Alarme07_06":                          [7 + 14199, 6],
        "Alarme07_07":                          [7 + 14199, 7],
        "Alarme07_08":                          [7 + 14199, 8],
        "Alarme07_09":                          [7 + 14199, 9],
        "Alarme07_10":                          [7 + 14199, 10],
        "Alarme07_11":                          [7 + 14199, 11],
        "Alarme07_12":                          [7 + 14199, 12],
        "Alarme07_13":                          [7 + 14199, 13],
        "Alarme07_14":                          [7 + 14199, 14],
        "Alarme07_15":                          [7 + 14199, 15],

        "Alarme08_00":                          [8 + 14199, 0],
        "Alarme08_01":                          [8 + 14199, 1],
        "Alarme08_02":                          [8 + 14199, 2],
        "Alarme08_03":                          [8 + 14199, 3],
        "Alarme08_07":                          [8 + 14199, 7],
        "Alarme08_08":                          [8 + 14199, 8],
        "Alarme08_09":                          [8 + 14199, 9],
        "Alarme08_10":                          [8 + 14199, 10],
        "Alarme08_11":                          [8 + 14199, 11],
        "Alarme08_12":                          [8 + 14199, 12],
        "Alarme08_13":                          [8 + 14199, 13],
        "Alarme08_14":                          [8 + 14199, 14],
        "Alarme08_15":                          [8 + 14199, 15],

        "Alarme09_00":                          [9 + 14199, 0],
        "Alarme09_01":                          [9 + 14199, 1],
        "Alarme09_02":                          [9 + 14199, 2],
        "Alarme09_03":                          [9 + 14199, 3],
        "Alarme09_04":                          [9 + 14199, 4],
        "Alarme09_06":                          [9 + 14199, 6],
        "Alarme09_07":                          [9 + 14199, 7],
        "Alarme09_08":                          [9 + 14199, 8],
        "Alarme09_09":                          [9 + 14199, 9],
        "Alarme09_10":                          [9 + 14199, 10],
        "Alarme09_11":                          [9 + 14199, 11],
        "Alarme09_12":                          [9 + 14199, 12],
        "Alarme09_13":                          [9 + 14199, 13],
        "Alarme09_14":                          [9 + 14199, 14],
        "Alarme09_15":                          [9 + 14199, 15],

        "Alarme10_00":                          [10 + 14199, 0],
        "Alarme10_01":                          [10 + 14199, 1],
        "Alarme10_02":                          [10 + 14199, 2],
        "Alarme10_03":                          [10 + 14199, 3],
        "Alarme10_05":                          [10 + 14199, 5],
        "Alarme10_06":                          [10 + 14199, 6],
        "Alarme10_07":                          [10 + 14199, 7],
        "Alarme10_08":                          [10 + 14199, 8],
        "Alarme10_09":                          [10 + 14199, 9],
        "Alarme10_10":                          [10 + 14199, 10],
        "Alarme10_11":                          [10 + 14199, 11],
        "Alarme10_12":                          [10 + 14199, 12],
        "Alarme10_13":                          [10 + 14199, 13],
        "Alarme10_14":                          [10 + 14199, 14],
        "Alarme10_15":                          [10 + 14199, 15],

        "Alarme11_00":                          [11 + 14199, 0],
        "Alarme11_01":                          [11 + 14199, 1],
        "Alarme11_02":                          [11 + 14199, 2],
        "Alarme11_06":                          [11 + 14199, 6],
        "Alarme11_07":                          [11 + 14199, 7],
        "Alarme11_08":                          [11 + 14199, 8],
        "Alarme11_09":                          [11 + 14199, 9],
        "Alarme11_10":                          [11 + 14199, 10],
        "Alarme11_11":                          [11 + 14199, 11],
        "Alarme11_12":                          [11 + 14199, 12],
        "Alarme11_13":                          [11 + 14199, 13],
        "Alarme11_14":                          [11 + 14199, 14],
        "Alarme11_15":                          [11 + 14199, 15],

        "Alarme12_01":                          [12 + 14199, 1],
        "Alarme12_02":                          [12 + 14199, 2],
        "Alarme12_03":                          [12 + 14199, 3],
        "Alarme12_04":                          [12 + 14199, 4],
        "Alarme12_05":                          [12 + 14199, 5],
        "Alarme12_06":                          [12 + 14199, 6],
        "Alarme12_07":                          [12 + 14199, 7],
        "Alarme12_09":                          [12 + 14199, 9],
        "Alarme12_10":                          [12 + 14199, 10],
        "Alarme12_11":                          [12 + 14199, 11],
        "Alarme12_12":                          [12 + 14199, 12],
        "Alarme12_13":                          [12 + 14199, 13],
        "Alarme12_14":                          [12 + 14199, 14],
        "Alarme12_15":                          [12 + 14199, 15],

        "Alarme13_00":                          [13 + 14199, 0],
        "Alarme13_01":                          [13 + 14199, 1],
        "Alarme13_02":                          [13 + 14199, 2],
        "Alarme13_03":                          [13 + 14199, 3],
        "Alarme13_09":                          [13 + 14199, 9],
        "Alarme13_10":                          [13 + 14199, 10],
        "Alarme13_11":                          [13 + 14199, 11],
        "Alarme13_12":                          [13 + 14199, 12],
        "Alarme13_13":                          [13 + 14199, 13],
        "Alarme13_14":                          [13 + 14199, 14],
        "Alarme13_15":                          [13 + 14199, 15],

        "Alarme14_00":                          [14 + 14199, 0],
        "Alarme14_01":                          [14 + 14199, 1],
        "Alarme14_02":                          [14 + 14199, 2],
        "Alarme14_03":                          [14 + 14199, 3],
        "Alarme14_04":                          [14 + 14199, 4],
        "Alarme14_05":                          [14 + 14199, 5],
        "Alarme14_10":                          [14 + 14199, 10],
        "Alarme14_11":                          [14 + 14199, 11],
        "Alarme14_12":                          [14 + 14199, 12],
        "Alarme14_13":                          [14 + 14199, 13],
        "Alarme14_14":                          [14 + 14199, 14],
        "Alarme14_15":                          [14 + 14199, 15],

        "Alarme15_00":                          [15 + 14199, 0],
        "Alarme15_01":                          [15 + 14199, 1],
        "Alarme15_02":                          [15 + 14199, 2],
        "Alarme15_03":                          [15 + 14199, 3],
        "Alarme15_04":                          [15 + 14199, 4],
        "Alarme15_05":                          [15 + 14199, 5],
        "Alarme15_06":                          [15 + 14199, 6],
        "Alarme15_07":                          [15 + 14199, 7],
        "Alarme15_08":                          [15 + 14199, 8],
        "Alarme15_09":                          [15 + 14199, 9],
        "Alarme15_10":                          [15 + 14199, 10],
        "Alarme15_12":                          [15 + 14199, 12],
        "Alarme15_13":                          [15 + 14199, 13],
        "Alarme15_14":                          [15 + 14199, 14],
        "Alarme15_15":                          [15 + 14199, 15],

        "Alarme16_00":                          [16 + 14199, 0],
        "Alarme16_01":                          [16 + 14199, 1],
        "Alarme16_02":                          [16 + 14199, 2],
        "Alarme16_03":                          [16 + 14199, 3],
        "Alarme16_04":                          [16 + 14199, 4],
        "Alarme16_05":                          [16 + 14199, 5],
        "Alarme16_06":                          [16 + 14199, 6],
        "Alarme16_07":                          [16 + 14199, 7],
        "Alarme16_08":                          [16 + 14199, 8],
        "Alarme16_09":                          [16 + 14199, 9],
        "Alarme16_10":                          [16 + 14199, 10],
        "Alarme16_11":                          [16 + 14199, 11],
        "Alarme16_12":                          [16 + 14199, 12],
    }
}