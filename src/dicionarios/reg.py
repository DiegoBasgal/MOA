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

    # Carregador de Baterias
    "CB_INFO":                                  10 + 12764,                     # Leituras.CarregadorBateria_Info
    "CB_UENTRADA":                              11 + 12764,                     # Leituras.CarregadorBateria_UEntrada
    "CB_USAIDA":                                12 + 12764,                     # Leituras.CarregadorBateria_USaida
    "CB_IENTRADA":                              13 + 12764,                     # Leituras.CarregadorBateria_IEntrada
    "CB_ISAIDA":                                14 + 12764,                     # Leituras.CarregadorBateria_ISaida
    "CB2_INFO":                                 197 + 12764,                    # Leituras.CB2_Info
    "CB2_UENTRADA":                             198 + 12764,                    # Leituras.CB2_UEntrada
    "CB2_USAIDA":                               199 + 12764,                    # Leituras.CB2_USaida
    "CB2_IENTRADA":                             200 + 12764,                    # Leituras.CB2_IEntrada
    "CB2_ISAIDA":                               201 + 12764,                    # Leituras.CB2_ISaida

    # Gerador Diesel
    "GD_INFO":                                  15 + 12764,                     # Leituras.GrupoDiesel_Info
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

    # Poço
    "POCO_INFO":                                111 + 12764,                    # Leituras.Poco_Info
    "POCO_BOMBAS":                              112 + 12764,                    # Leituras.Poco_Bombas
    "POCO_NIVEL":                               113 + 12764,                    # Leituras.Poco_Nivel
    "POCO_HORIMETRO_PRINCIPAL":                 114 + 12764,                    # Leituras.Poco_HorimetroPrincipal
    "POCO_HORIMETRO_RETAGUARDA":                115 + 12764,                    # Leituras.Poco_HorimetroRetaguarda

    # Sensores
    "SENSOR_FUMACA_INFO":                       116 + 12764,                    # Leituras.SensorFumaca_Info
    "SENSOR_PRESENCA_INFO":                     117 + 12764,                    # Leituras.SensorPresenca_Info

    # Temperaturas
    "USINA_TEMPERATURA_01":                     119 + 12764,                    # Leituras.Usina_Temperatura_01
    "USINA_TEMPERATURA_02":                     120 + 12764,                    # Leituras.Usina_Temperatura_02
    "USINA_TEMPERATURA_03":                     121 + 12764,                    # Leituras.Usina_Temperatura_03
    "USINA_TEMPERATURA_04":                     122 + 12764,                    # Leituras.Usina_Temperatura_04
    "USINA_TEMPERATURA_05":                     123 + 12764,                    # Leituras.Usina_Temperatura_05
    "USINA_TEMPERATURA_06":                     124 + 12764,                    # Leituras.Usina_Temperatura_06
    "USINA_TEMPERATURA_07":                     125 + 12764,                    # Leituras.Usina_Temperatura_07
    "USINA_TEMPERATURA_08":                     126 + 12764,                    # Leituras.Usina_Temperatura_08

    # Rendimento
    "RENDIMENTO_UG01":                          203 + 12764,                    # Leituras.Rendimento_UG01
    "RENDIMENTO_UG02":                          204 + 12764,                    # Leituras.Rendimento_UG02
    "RENDIMENTO_UG03":                          205 + 12764,                    # Leituras.Rendimento_UG03
    "RENDIMENTO_UG04":                          206 + 12764,                    # Leituras.Rendimento_UG04
    "RENDIMENTO_GERAL":                         207 + 12764,                    # Leituras.Rendimento_Geral
    "RENDIMENTO_INFO":                          218 + 12764,                    # Leituras.Rendimento_Info
    "RENDIMENTO_TURBINA_UG01":                  219 + 12764,                    # Leituras.RendimentoTurbina_UG01
    "RENDIMENTO_TURBINA_UG02":                  220 + 12764,                    # Leituras.RendimentoTurbina_UG02
    "RENDIMENTO_TURBINA_UG03":                  221 + 12764,                    # Leituras.RendimentoTurbina_UG03
    "RENDIMENTO_TURBINA_UG04":                  222 + 12764,                    # Leituras.RendimentoTurbina_UG04
    "RENDIMENTO_GERADOR_UG01":                  223 + 12764,                    # Leituras.RendimentoGerador_UG01
    "RENDIMENTO_GERADOR_UG02":                  224 + 12764,                    # Leituras.RendimentoGerador_UG02
    "RENDIMENTO_GERADOR_UG03":                  225 + 12764,                    # Leituras.RendimentoGerador_UG03
    "RENDIMENTO_GERADOR_UG04":                  226 + 12764,                    # Leituras.RendimentoGerador_UG04

    # Sistema de Água
    "SA_INFO":                                  181 + 12764,                    # Leituras.SistemaAgua_Info
    "SA_BOMBA":                                 182 + 12764,                    # Leituras.SistemaAgua_Bombas
    "SA_VALVULAS":                              183 + 12764,                    # Leituras.SistemaAgua_Valvulas
    "SA_VALVULAS2":                             188 + 12764,                    # Leituras.SistemaAgua_Valvulas2

    # Injeção Selo
    "IS_ACUMULADOR_LIDER":                      184 + 12764,                    # Leituras.InjecaoSelo_AcumuladorLider
    "IS_ACUMULADOR_RETAGUARDA":                 185 + 12764,                    # Leituras.InjecaoSelo_AcumuladorRetaguarda

    # Água Serviço
    "AS_ACUMULADOR_LIDER":                      186 + 12764,                    # Leituras.AguaServico_AcumuladorLider
    "AS_ACUMULADOR_RETAGUARDA":                 187 + 12764,                    # Leituras.AguaServico_AcumuladorRetaguarda


    ## ALARMES
    "Alarme01_02":                              [1, 2],
    "Alarme01_03":                              [1, 3],
    "Alarme01_07":                              [1, 7],
    "Alarme01_08":                              [1, 8],
    "Alarme01_09":                              [1, 9],
    "Alarme01_10":                              [1, 10],
    "Alarme01_11":                              [1, 11],
    "Alarme01_15":                              [1, 15],

    "Alarme02_03":                              [2, 3],
    "Alarme02_06":                              [2, 6],
    "Alarme02_09":                              [2, 9],
    "Alarme02_10":                              [2, 10],
    "Alarme02_14":                              [2, 14],
    "Alarme02_15":                              [2, 15],

    "Alarme03_09":                              [3, 9],
    "Alarme03_10":                              [3, 10],
    "Alarme03_11":                              [3, 11],
    "Alarme03_12":                              [3, 12],
    "Alarme03_13":                              [3, 13],
    "Alarme03_14":                              [3, 14],
    "Alarme03_15":                              [3, 15],

    "Alarme04_00":                              [4, 0],
    "Alarme04_01":                              [4, 1],
    "Alarme04_02":                              [4, 2],
    "Alarme04_03":                              [4, 3],
    "Alarme04_04":                              [4, 4],
    "Alarme04_05":                              [4, 5],
    "Alarme04_06":                              [4, 6],
    "Alarme04_07":                              [4, 7],
    "Alarme04_08":                              [4, 8],
    "Alarme04_09":                              [4, 9],

    "Alarme05_00":                              [5, 0],
    "Alarme05_01":                              [5, 1],
    "Alarme05_15":                              [5, 15],

    "Alarme06_00":                              [6, 0],
    "Alarme06_01":                              [6, 1],
    "Alarme06_02":                              [6, 2],
    "Alarme06_03":                              [6, 3],
    "Alarme06_04":                              [6, 4],
    "Alarme06_05":                              [6, 5],
    "Alarme06_06":                              [6, 6],
    "Alarme06_07":                              [6, 7],
    "Alarme06_08":                              [6, 8],
    "Alarme06_09":                              [6, 9],
    "Alarme06_11":                              [6, 11],
    "Alarme06_12":                              [6, 12],
    "Alarme06_13":                              [6, 13],
    "Alarme06_14":                              [6, 14],

    "Alarme07_01":                              [7, 1],
    "Alarme07_02":                              [7, 2],
    "Alarme07_03":                              [7, 3],
    "Alarme07_04":                              [7, 4],
    "Alarme07_05":                              [7, 5],
    "Alarme07_06":                              [7, 6],
    "Alarme07_07":                              [7, 7],
    "Alarme07_11":                              [7, 11],
    "Alarme07_12":                              [7, 12],
    "Alarme07_13":                              [7, 13],
    "Alarme07_14":                              [7, 14],
    "Alarme07_15":                              [7, 15],

    "Alarme08_00":                              [8, 0],
    "Alarme08_01":                              [8, 1],
    "Alarme08_02":                              [8, 2],
    "Alarme08_03":                              [8, 3],
    "Alarme08_04":                              [8, 4],
    "Alarme08_05":                              [8, 5],
    "Alarme08_06":                              [8, 6],
    "Alarme08_07":                              [8, 7],
    "Alarme08_08":                              [8, 8],
    "Alarme08_09":                              [8, 9],
    "Alarme08_10":                              [8, 10],
    "Alarme08_11":                              [8, 11],
    "Alarme08_12":                              [8, 12],
    "Alarme08_13":                              [8, 13],
    "Alarme08_14":                              [8, 14],

    "Alarme09_00":                              [9, 0],
    "Alarme09_01":                              [9, 1],
    "Alarme09_02":                              [9, 2],
    "Alarme09_03":                              [9, 3],
    "Alarme09_04":                              [9, 4],
    "Alarme09_09":                              [9, 9],
    "Alarme09_10":                              [9, 10],
    "Alarme09_11":                              [9, 11],
    "Alarme09_12":                              [9, 12],

    "Alarme10_00":                              [10, 0],
    "Alarme10_01":                              [10, 1],
    "Alarme10_02":                              [10, 2],
    "Alarme10_03":                              [10, 3],
    "Alarme10_04":                              [10, 4],
    "Alarme10_05":                              [10, 5],
    "Alarme10_06":                              [10, 6],
    "Alarme10_07":                              [10, 7],

    "Alarme11_00":                              [11, 0],
    "Alarme11_01":                              [11, 1],
    "Alarme11_02":                              [11, 2],
    "Alarme11_03":                              [11, 3],
    "Alarme11_04":                              [11, 4],
    "Alarme11_05":                              [11, 5],
    "Alarme11_06":                              [11, 6],
    "Alarme11_07":                              [11, 7],
    "Alarme11_08":                              [11, 8],
    "Alarme11_09":                              [11, 9],
    "Alarme11_10":                              [11, 10],
    "Alarme11_11":                              [11, 11],
    "Alarme11_12":                              [11, 12],
    "Alarme11_13":                              [11, 13],
    "Alarme11_14":                              [11, 14],
    "Alarme11_15":                              [11, 15],

    "Alarme12_00":                              [12, 0],
    "Alarme12_04":                              [12, 4],
    "Alarme12_05":                              [12, 5],
    "Alarme12_06":                              [12, 6],

    "Alarme14_03":                              [14, 3],
    "Alarme14_04":                              [14, 4],
    "Alarme14_05":                              [14, 5],
    "Alarme14_06":                              [14, 6],
    "Alarme14_08":                              [14, 8],
    "Alarme14_09":                              [14, 9],
    "Alarme14_10":                              [14, 10],
    "Alarme14_11":                              [14, 11],
    "Alarme14_12":                              [14, 12],
    "Alarme14_13":                              [14, 13],
    "Alarme14_14":                              [14, 14],
    "Alarme14_15":                              [14, 15],

    "Alarme15_00":                              [15, 0],
    "Alarme15_01":                              [15, 1],
    "Alarme15_02":                              [15, 2],
    "Alarme15_03":                              [15, 3],
    "Alarme15_04":                              [15, 4],
    "Alarme15_05":                              [15, 5],
    "Alarme15_06":                              [15, 6],
    "Alarme15_07":                              [15, 7],
    "Alarme15_08":                              [15, 8],
    "Alarme15_09":                              [15, 9],
    "Alarme15_10":                              [15, 10],
    "Alarme15_11":                              [15, 11],

    "Alarme16_10":                              [16, 10],
    "Alarme16_11":                              [16, 11],
    "Alarme16_12":                              [16, 12],
    "Alarme16_13":                              [16, 13],
    "Alarme16_14":                              [16, 14],
    "Alarme16_15":                              [16, 15],

    "Alarme17_00":                              [17, 0],
    "Alarme17_01":                              [17, 1],
    "Alarme17_02":                              [17, 2],
    "Alarme17_03":                              [17, 3],
    "Alarme17_04":                              [17, 4],
    "Alarme17_05":                              [17, 5],
    "Alarme17_06":                              [17, 6],
    "Alarme17_07":                              [17, 7],
    "Alarme17_09":                              [17, 9],
    "Alarme17_10":                              [17, 10],
    "Alarme17_11":                              [17, 11],
    "Alarme17_12":                              [17, 12],
    "Alarme17_13":                              [17, 13],
    "Alarme17_14":                              [17, 14],

    "Alarme18_00":                              [18, 0],
    "Alarme18_01":                              [18, 1],
    "Alarme18_03":                              [18, 3],
    "Alarme18_06":                              [18, 6],
    "Alarme18_07":                              [18, 7],
    "Alarme18_08":                              [18, 8],
    "Alarme18_09":                              [18, 9],
    "Alarme18_10":                              [18, 10],
    "Alarme18_11":                              [18, 11],
    "Alarme18_12":                              [18, 12],

    "Alarme19_06":                              [19, 6],
    "Alarme19_07":                              [19, 7],
    "Alarme19_08":                              [19, 8],
    "Alarme19_09":                              [19, 9],
    "Alarme19_10":                              [19, 10],
    "Alarme19_11":                              [19, 11],
    "Alarme19_12":                              [19, 12],
    "Alarme19_13":                              [19, 13],
    "Alarme19_14":                              [19, 14],

    "Alarme20_06":                              [20, 6],
    "Alarme20_07":                              [20, 7],
    "Alarme20_08":                              [20, 8],
    "Alarme20_09":                              [20, 9],
    "Alarme20_10":                              [20, 10],
    "Alarme20_11":                              [20, 11],
    "Alarme20_12":                              [20, 12],
    "Alarme20_13":                              [20, 13],
    "Alarme20_14":                              [20, 14],

    "Alarme21_02":                              [21, 2],
    "Alarme21_03":                              [21, 3],
    "Alarme21_06":                              [21, 6],
    "Alarme21_07":                              [21, 7],
    "Alarme21_08":                              [21, 8],
    "Alarme21_09":                              [21, 9],
    "Alarme21_10":                              [21, 10],
    "Alarme21_11":                              [21, 11],
    "Alarme21_12":                              [21, 12],
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
    "STATUS_SECCIONADORAS":                     22 + 12764,                     # Leituras.Subestacao_Seccionadoras

    # Tensão
    "TENSAO_RN":                                23 + 12764,                     # Leituras.Subestacao_TensaoRN
    "TENSAO_SN":                                24 + 12764,                     # Leituras.Subestacao_TensaoSN
    "TENSAO_TN":                                25 + 12764,                     # Leituras.Subestacao_TensaoTN
    "TENSAO_RS":                                26 + 12764,                     # Leituras.Subestacao_TensaoRS
    "TENSAO_ST":                                27 + 12764,                     # Leituras.Subestacao_TensaoST
    "TENSAO_TR":                                28 + 12764,                     # Leituras.Subestacao_TensaoTR
    "TENSAO_SINCRONISMO":                       63 + 12764,                     # Leituras.Subestacao_TensaoSincronismo
    "TENSAO_VCC":                               64 + 12764,                     # Leituras.Subestacao_TensaoVCC

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

    "Alarme01_00":                              [1, 0],
    "Alarme01_01":                              [1, 1],
    "Alarme01_12":                              [1, 12],
    "Alarme01_13":                              [1, 13],
    "Alarme01_14":                              [1, 14],

    "Alarme02_00":                              [2, 0],
    "Alarme02_01":                              [2, 1],
    "Alarme02_02":                              [2, 2],
    "Alarme02_04":                              [2, 4],
    "Alarme02_05":                              [2, 5],
    "Alarme02_07":                              [2, 7],
    "Alarme02_08":                              [2, 8],
    "Alarme02_11":                              [2, 11],
    "Alarme02_12":                              [2, 12],
    "Alarme02_13":                              [2, 13],

    "Alarme03_00":                              [3, 0],
    "Alarme03_01":                              [3, 1],
    "Alarme03_02":                              [3, 2],
    "Alarme03_03":                              [3, 3],
    "Alarme03_04":                              [3, 4],
    "Alarme03_05":                              [3, 5],
    "Alarme03_06":                              [3, 6],
    "Alarme03_07":                              [3, 7],
    "Alarme03_08":                              [3, 8],

    "Alarme05_02":                              [5, 2],
    "Alarme05_03":                              [5, 3],
    "Alarme05_04":                              [5, 4],
    "Alarme05_05":                              [5, 5],
    "Alarme05_06":                              [5, 6],
    "Alarme05_07":                              [5, 7],
    "Alarme05_08":                              [5, 8],
    "Alarme05_09":                              [5, 9],
    "Alarme05_10":                              [5, 10],
    "Alarme05_11":                              [5, 11],
    "Alarme05_12":                              [5, 12],
    "Alarme05_13":                              [5, 13],
    "Alarme05_14":                              [5, 14],

    "Alarme09_07":                              [9, 7],
    "Alarme09_08":                              [9, 8],

    "Alarme12_03":                              [12, 3],

    "Alarme14_07":                              [14, 7],

    "Alarme16_04":                              [16, 4],
    "Alarme16_05":                              [16, 5],
    "Alarme16_06":                              [16, 6],
    "Alarme16_07":                              [16, 7],
    "Alarme16_08":                              [16, 8],
    "Alarme16_09":                              [16, 9],

    "Alarme18_04":                              [18, 4],
    "Alarme18_05":                              [18, 5],
    "Alarme18_13":                              [18, 13],
    "Alarme18_14":                              [18, 14],
    "Alarme18_15":                              [18, 15],

    "Alarme19_00":                              [19, 0],
    "Alarme19_01":                              [19, 1],
    "Alarme19_02":                              [19, 2],
    "Alarme19_03":                              [19, 3],
    "Alarme19_04":                              [19, 4],
    "Alarme19_05":                              [19, 5],
    "Alarme19_15":                              [19, 15],

    "Alarme20_00":                              [20, 0],
    "Alarme20_01":                              [20, 1],
    "Alarme20_02":                              [20, 2],
    "Alarme20_03":                              [20, 3],
    "Alarme20_04":                              [20, 4],
    "Alarme20_05":                              [20, 5],
    "Alarme20_15":                              [20, 15],

    "Alarme21_00":                              [21, 0],
    "Alarme21_01":                              [21, 1],
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
    "UHTA01_BOMBAS":                            140 + 12764,                    # Leituras.PCTA_UHTA01_Bombas
    "UHTA01_RODIZIO":                           141 + 12764,                    # Leituras.PCTA_UHTA01_Rodizio
    "UHTA01_ACUMULADOR_BOMBA_LIDER":            142 + 12764,                    # Leituras.PCTA_UHTA01_AcumuladorBombaLider
    "UHTA01_ACUMULADOR_BOMBA_RETAGUARDA":       143 + 12764,                    # Leituras.PCTA_UHTA01_AcumuladorBombaRetaguarda
    "UHTA01_FILTROS":                           144 + 12764,                    # Leituras.PCTA_UHTA01_Filtros
    "UHTA01_NIVEL_OLEO_INFO":                   145 + 12764,                    # Leituras.PCTA_UHTA01_NivelOleo_Info
    "UHTA01_TEMPERATURA_OLEO_INFO":             146 + 12764,                    # Leituras.PCTA_UHTA01_TemperaturaOleo_info
    "UHTA01_VALVULAS":                          147 + 12764,                    # Leituras.PCTA_UHTA01_Valvulas
    "UHTA01_PRESSOSTATOS":                      148 + 12764,                    # Leituras.PCTA_UHTA01_Pressostatos
    "UHTA01_TEMPERATURA_OLEO":                  149 + 12764,                    # Leituras.PCTA_UHTA01_TemperaturaOleo
    "UHTA01_NIVEL_OLEO":                        150 + 12764,                    # Leituras.PCTA_UHTA01_NivelOleo
    "UHTA02_INFO":                              151 + 12764,                    # Leituras.PCTA_UHTA02_Info
    "UHTA02_BOMBAS":                            152 + 12764,                    # Leituras.PCTA_UHTA02_Bombas
    "UHTA02_RODIZIO":                           153 + 12764,                    # Leituras.PCTA_UHTA02_Rodizio
    "UHTA02_ACUMULADOR_BOMBA_LIDER":            154 + 12764,                    # Leituras.PCTA_UHTA02_AcumuladorBombaLider
    "UHTA02_ACUMULADOR_BOMBA_RETAGUARDA":       155 + 12764,                    # Leituras.PCTA_UHTA02_AcumuladorBombaRetaguarda
    "UHTA02_FILTROS":                           156 + 12764,                    # Leituras.PCTA_UHTA02_Filtros
    "UHTA02_NIVEL_OLEO_INFO":                   157 + 12764,                    # Leituras.PCTA_UHTA02_NivelOleo_Info
    "UHTA02_TEMPERATURA_OLEO_INFO":             158 + 12764,                    # Leituras.PCTA_UHTA02_TemperaturaOleo_info
    "UHTA02_VALVULAS":                          159 + 12764,                    # Leituras.PCTA_UHTA02_Valvulas
    "UHTA02_PRESSOSTATOS":                      160 + 12764,                    # Leituras.PCTA_UHTA02_Pressostatos
    "UHTA02_TEMPERATURA_OLEO":                  161 + 12764,                    # Leituras.PCTA_UHTA02_TemperaturaOleo
    "UHTA02_NIVEL_OLEO":                        162 + 12764,                    # Leituras.PCTA_UHTA02_NivelOleo


    ## ALARMES

    "Alarme01_04":                              [1, 4],
    "Alarme01_05":                              [1, 5],
    "Alarme01_06":                              [1, 6],

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
    "CP_01_POSICAO":                            165 + 12764,                    # Leituras.PCAD_Comporta01_Posicao
    "CP_02_INFO":                               166 + 12764,                    # Leituras.PCAD_Comporta02_Info
    "CP_02_POSICAO":                            167 + 12764,                    # Leituras.PCAD_Comporta02_Posicao

    # UHCD,
    "UHCD_INFO":                                168 + 12764,                    # Leituras.PCAD_UHCD_Info
    "UHCD_BOMBAS":                              169 + 12764,                    # Leituras.PCAD_UHCD_Bombas
    "UHCD_RODIZIO":                             170 + 12764,                    # Leituras.PCAD_UHCD_Rodizio
    "UHCD_ACUMULADOR_BOMBA_LIDER":              171 + 12764,                    # Leituras.PCAD_UHCD_AcumuladorBombaLider
    "UHCD_ACUMULADOR_BOMBA_RETAGUARDA":         172 + 12764,                    # Leituras.PCAD_UHCD_AcumuladorBombaRetaguarda
    "UHCD_FILTROS":                             173 + 12764,                    # Leituras.PCAD_UHCD_Filtros
    "UHCD_NIVEL_OLEO_INFO":                     174 + 12764,                    # Leituras.PCAD_UHCD_NivelOleo_Info
    "UHCD_TEMPERATURA_OLEO_INFO":               175 + 12764,                    # Leituras.PCAD_UHCD_TemperaturaOleo_Info
    "UHCD_VALVULAS":                            176 + 12764,                    # Leituras.PCAD_UHCD_Valvulas
    "UHCD_PRESSOSTATOS":                        177 + 12764,                    # Leituras.PCAD_UHCD_Pressostatos
    "UHCD_TEMPERATURA_OLEO":                    178 + 12764,                    # Leituras.PCAD_UHCD_TemperaturaOleo
    "UHCD_NIVEL_OLEO":                          179 + 12764,                    # Leituras.PCAD_UHCD_NivelOleo


    ## ALARMES
    "Alarme28_00":                              [28, 0],
    "Alarme28_01":                              [28, 1],
    "Alarme28_04":                              [28, 4],
    "Alarme28_05":                              [28, 5],
    "Alarme28_06":                              [28, 6],
    "Alarme28_07":                              [28, 7],
    "Alarme28_08":                              [28, 8],
    "Alarme28_09":                              [28, 9],
    "Alarme28_10":                              [28, 10],
    "Alarme28_11":                              [28, 11],
    "Alarme28_12":                              [28, 12],

    "Alarme29_00":                              [29, 0],
    "Alarme29_01":                              [29, 1],
    "Alarme29_02":                              [29, 2],
    "Alarme29_03":                              [29, 3],
    "Alarme29_05":                              [29, 5],
    "Alarme29_06":                              [29, 6],
    "Alarme29_07":                              [29, 7],
    "Alarme29_09":                              [29, 9],
    "Alarme29_10":                              [29, 10],
    "Alarme29_11":                              [29, 11],
    "Alarme29_13":                              [29, 13],

    "Alarme30_00":                              [30, 0],
    "Alarme30_01":                              [30, 1],
    "Alarme30_04":                              [30, 4],
    "Alarme30_05":                              [30, 5],
    "Alarme30_08":                              [30, 8],
    "Alarme30_09":                              [30, 9],
    "Alarme30_10":                              [30, 10],
    "Alarme30_11":                              [30, 11],

    "Alarme31_00":                              [31, 0],
    "Alarme31_01":                              [31, 1],
    "Alarme31_02":                              [31, 2],
    "Alarme31_03":                              [31, 3],
    "Alarme31_04":                              [31, 4],
    "Alarme31_05":                              [31, 5],
    "Alarme31_06":                              [31, 6],
}

REG_UG = {
    "UG1": {
        ## COMANDOS
        # Gerais
        "CMD_RESET_ALARMES":                    0,                              # Comandos.Operacao_PCH_AdoPopinhakResetAlarmes
        "CMD_RECONHECE_ALARMES":                1,                              # Comandos.Operacao_PCH_AdoPopinhakReconheceAlarmes

        # Operação
        "CMD_OPER_UP":                          2,                              # Comandos.Operacao_UP
        "CMD_OPER_UPGM":                        3,                              # Comandos.Operacao_UPGM
        "CMD_OPER_UVD":                         4,                              # Comandos.Operacao_UVD
        "CMD_OPER_UPS":                         5,                              # Comandos.Operacao_UPS
        "CMD_OPER_US":                          6,                              # Comandos.Operacao_US
        "CMD_OPER_EMERGENCIA_LIGAR":            7,                              # Comandos.Operacao_EmergenciaLigar
        "CMD_OPER_EMERGENCIA_DESLIGAR":         8,                              # Comandos.Operacao_EmergenciaDesligar
        "CMD_OPER_PARADA_RESET":                72,                             # Comandos.Operacao_ParadaReset

        # Turbina
        "CMD_TURB_BYPASS_ABRIR":                9,                              # Comandos.Turb_ByPassAbrir
        "CMD_TURB_BYPASS_FECHAR":               10,                             # Comandos.Turb_ByPassFechar
        "CMD_TURB_BORBOLETA_ABRIR":             11,                             # Comandos.Turb_BorboletaAbrir
        "CMD_TURB_BORBOLETA_FECHAR":            12,                             # Comandos.Turb_BorboletaFechar
        "CMD_TURB_FRENAGEM_APLICAR":            13,                             # Comandos.Turb_FrenagemAplicar
        "CMD_TURB_FRENAGEM_DESAPLICAR":         14,                             # Comandos.Turb_FrenagemDesaplicar
        "CMD_TURB_FRENAGEM_MANUAL":             15,                             # Comandos.Turb_FrenagemManual
        "CMD_TURB_FRENAGEM_AUTO":               16,                             # Comandos.Turb_FrenagemAuto
        "CMD_TURB_SENSOR_ATIVAR":               17,                             # Comandos.Turb_SensorAtivar
        "CMD_TURB_SENSOR_DESATIVAR":            18,                             # Comandos.Turb_SensorDesativar

        # Reg V
        "CMD_REG_V_PARTIR":                     19,                             # Comandos.RegV_Partir
        "CMD_REG_V_PARAR":                      20,                             # Comandos.RegV_Parar
        "CMD_REG_V_COLOCAR_CARGA":              21,                             # Comandos.RegV_ColocarCarga
        "CMD_REG_V_RETIRAR_CARGA":              22,                             # Comandos.RegV_RetirarCarga
        "CMD_REG_V_INCREMENTA_VELOCIDADE":      23,                             # Comandos.RegV_IncrementaVelocidade
        "CMD_REG_V_DECREMENTA_VELOCIDADE":      24,                             # Comandos.RegV_DecrementaVelocidade
        "CMD_REG_V_SEL_MODO_ESTATISMO":         25,                             # Comandos.RegV_SelecionaModoEstatismo
        "CMD_REG_V_SEL_MODO_BASECARGA":         26,                             # Comandos.RegV_SelecionaModoBaseCarga

        # Reg T
        "CMD_REG_T_LIGAR":                      27,                             # Comandos.RegT_Ligar
        "CMD_REG_T_DESLIGAR":                   28,                             # Comandos.RegT_Desligar
        "CMD_REG_T_INCREMENTA_TENSAO":          29,                             # Comandos.RegT_IncrementaTensao
        "CMD_REG_T_DECREMENTA_TENSAO":          30,                             # Comandos.RegT_DecrementaTensao
        "CMD_REG_T_PRE_EXCITACAO":              31,                             # Comandos.RegT_PreExcitacao

        # Sinc
        "CMD_SINC_LIGAR":                       32,                             # Comandos.Sinc_Ligar
        "CMD_SINC_DESLIGAR":                    33,                             # Comandos.Sinc_Desligar
        "CMD_SINC_MODO_AUTO_LIGAR":             34,                             # Comandos.Sinc_ModoAutoLigar
        "CMD_SINC_MODO_MANUAL_LIGAR":           35,                             # Comandos.Sinc_ModoManualLigar
        "CMD_SINC_MODO_BMORTA_LIGAR":           36,                             # Comandos.Sinc_ModoBMortaLigar

        # DJ52G
        "CMD_DJ52G_ABRIR":                      37,                             # Comandos.Disj52G_Abrir

        # Controle Reativo
        "CMD_CTRL_REATIVO_MODO_FPLIGAR":        38,                             # Comandos.CtrlReativo_ModoFPLigar
        "CMD_CTRL_REATIVO_MODO_FPDESLIGAR":     39,                             # Comandos.CtrlReativo_ModoFPDesligar
        "CMD_CTRL_REATIVO_MODO_VArLIGAR":       40,                             # Comandos.CtrlReativo_ModoVArLigar
        "CMD_CTRL_REATIVO_MODO_VArDESLIGAR":    41,                             # Comandos.CtrlReativo_ModoVArDesligar

        # Controle Potência
        "CMD_CTRL_POT_MODO_POT_LIGAR":          42,                             # Comandos.CtrlPotencia_ModoPotenciaLigar
        "CMD_CTRL_POT_MODO_POT_DESLIGAR":       43,                             # Comandos.CtrlPotencia_ModoPotenciaDesligar
        "CMD_CTRL_POT_MODO_NIVEL_LIGAR":        44,                             # Comandos.CtrlPotencia_ModoNivelLigar
        "CMD_CTRL_POT_MODO_NIVEL_DESLIGAR":     45,                             # Comandos.CtrlPotencia_ModoNivelDesligar
        "CMD_CTRL_POT_RELI_AUTO_LIGAR":         46,                             # Comandos.CtrlPotencia_ReligamentoAutomaticoLigar
        "CMD_CTRL_POT_RELI_AUTO_DESLIGAR":      47,                             # Comandos.CtrlPotencia_ReligamentoAutomaticoDesligar

        # UHCT
        "CMD_UHCT_BOMBA_01_LIGAR":              48,                             # Comandos.UHCT_Bomba01Ligar
        "CMD_UHCT_BOMBA_01_DESLIGAR":           49,                             # Comandos.UHCT_Bomba01Desligar
        "CMD_UHCT_BOMBA_01_PRINCIPAL":          50,                             # Comandos.UHCT_Bomba01Principal
        "CMD_UHCT_BOMBA_02_LIGAR":              51,                             # Comandos.UHCT_Bomba02Ligar
        "CMD_UHCT_BOMBA_02_DESLIGAR":           52,                             # Comandos.UHCT_Bomba02Desligar
        "CMD_UHCT_BOMBA_02_PRINCIPAL":          53,                             # Comandos.UHCT_Bomba02Principal
        "CMD_UHCT_BOMBA_AGUA_LIGAR":            54,                             # Comandos.UHCT_BombaAguaLigar
        "CMD_UHCT_BOMBA_AGUA_DESLIGAR":         55,                             # Comandos.UHCT_BombaAguaDesligar
        "CMD_UHCT_SENSOR_ATIVAR":               56,                             # Comandos.UHCT_SensorAtivar
        "CMD_UHCT_SENSOR_DESATIVAR":            57,                             # Comandos.UHCT_SensorDesativar
        "CMD_UHCT_RODIZIO_HABILITAR":           58,                             # Comandos.UHCT_RodizioHabilitar
        "CMD_UHCT_RODIZIO_DESABILITAR":         59,                             # Comandos.UHCT_RodizioDesabilitar

        # UHLM
        "CMD_UHLM_BOMBA_01_LIGAR":              60,                             # Comandos.UHLM_Bomba01Ligar
        "CMD_UHLM_BOMBA_01_DESLIGAR":           61,                             # Comandos.UHLM_Bomba01Desligar
        "CMD_UHLM_BOMBA_01_PRINCIPAL":          62,                             # Comandos.UHLM_Bomba01Principal
        "CMD_UHLM_BOMBA_02_LIGAR":              63,                             # Comandos.UHLM_Bomba02Ligar
        "CMD_UHLM_BOMBA_02_DESLIGAR":           64,                             # Comandos.UHLM_Bomba02Desligar
        "CMD_UHLM_BOMBA_02_PRINCIPAL":          65,                             # Comandos.UHLM_Bomba02Principal
        "CMD_UHLM_BOMBA_JACKING_LIGA":          66,                             # Comandos.UHLM_BombaJackingLiga
        "CMD_UHLM_BOMBA_JACKING_DESLIGA":       67,                             # Comandos.UHLM_BombaJackingDesliga
        "CMD_UHLM_BOMBA_AGUA_LIGA":             68,                             # Comandos.UHLM_BombaAguaLiga
        "CMD_UHLM_BOMBA_AGUA_DESLIGA":          69,                             # Comandos.UHLM_BombaAguaDesliga
        "CMD_UHLM_RODIZIO_HABILITAR":           70,                             # Comandos.UHLM_RodizioHabilitar
        "CMD_UHLM_RODIZIO_DESABILITAR":         71,                             # Comandos.UHLM_RodizioDesabilitar

        # RT
        "CMD_RT_MTVC_HABILITAR":                73,                             # Comandos.RT_MTVC_Habilitar
        "CMD_RT_MECC_HABILITAR":                74,                             # Comandos.RT_MECC_Habilitar
        "CMD_RT_ONLINE_HABILITAR":              75,                             # Comandos.RT_Online_habilitar
        "CMD_RT_ONLINE_DESABILITAR":            76,                             # Comandos.RT_Online_Desabiltar
        "CMD_RT_PARALELO_HABILITAR":            77,                             # Comandos.RT_Paralelo_habilitar
        "CMD_RT_PARALELO_DESABILITAR":          78,                             # Comandos.RT_Paralelo_Desabilitar

        # RV
        "CMD_RV_CONJUGADO_AUTO_HABILITAR":      79,                             # Comandos.RV_ConjugadoAuto_habilitar
        "CMD_RV_CONJUGADO_MANUAL_HABILITAR":    80,                             # Comandos.RV_ConjugadoManual_habilitar
        "CMD_RV_CONJUGADO_01_HABILITAR":        81,                             # Comandos.RV_Conjugado01_habilitar
        "CMD_RV_CONJUGADO_02_HABILITAR":        82,                             # Comandos.RV_Conjugado02_habilitar
        "CMD_RV_CONJUGADO_03_HABILITAR":        83,                             # Comandos.RV_Conjugado03_habilitar
        "CMD_RV_CONJUGADO_04_HABILITAR":        84,                             # Comandos.RV_Conjugado04_habilitar
        "CMD_RV_CONJUGADO_05_HABILITAR":        85,                             # Comandos.RV_Conjugado05_habilitar


        ## SETPOINTS

        # UHCT
        "UHCT_PRESSAO_MAX":                     0,                              # Setpoints.UHCT_PressaoMaxima
        "UHCT_PRESSAO_MIN":                     1,                              # Setpoints.UHCT_PressaoMinima
        "UHCT_PRESSAO_DESLIGAMENTO":            2,                              # Setpoints.UHCT_PressaoDesligamento
        "UHCT_PRESSAO_CRITICA":                 3,                              # Setpoints.UHCT_PressaoCritica

        # Controle Potência
        "CRTL_POT_NIVEL_LL1":                   4,                              # Setpoints.CtrlPotencia_NivelLL1
        "CRTL_POT_NIVEL_LL2":                   5,                              # Setpoints.CtrlPotencia_NivelLL2
        "CRTL_POT_NIVEL_LL3":                   6,                              # Setpoints.CtrlPotencia_NivelLL3
        "CRTL_POT_NIVEL_LL4":                   7,                              # Setpoints.CtrlPotencia_NivelLL4
        "CRTL_POT_NIVEL_LL5":                   8,                              # Setpoints.CtrlPotencia_NivelLL5
        "CRTL_POT_POT_1":                       9,                              # Setpoints.CtrlPotencia_Potencia1
        "CRTL_POT_POT_2":                       10,                             # Setpoints.CtrlPotencia_Potencia2
        "CRTL_POT_POT_3":                       11,                             # Setpoints.CtrlPotencia_Potencia3
        "CRTL_POT_POT_4":                       12,                             # Setpoints.CtrlPotencia_Potencia4
        "CRTL_POT_POT_5":                       13,                             # Setpoints.CtrlPotencia_Potencia5
        "CRTL_POT_POT_MIN":                     14,                             # Setpoints.CtrlPotencia_PotenciaMinima
        "CRTL_POT_POT_MIN_TEMPO":               15,                             # Setpoints.CtrlPotencia_PotenciaMinimaTempo
        "CRTL_POT_NIVEL_RELIGAMENTO":           16,                             # Setpoints.CtrlPotencia_NivelReligamento
        "CRTL_POT_ALVO":                        17,                             # Setpoints.CtrlPotencia_Alvo
        "CRTL_POT_TOLERANCIA":                  18,                             # Setpoints.CtrlPotencia_Tolerancia
        "CRTL_POT_PULSO_TEMPO":                 19,                             # Setpoints.CtrlPotencia_PulsoTempo
        "CRTL_POT_PULSO_INTERVALO":             20,                             # Setpoints.CtrlPotencia_PulsoIntervalo
        "CRTL_POT_SP_NIVEL":                    21,                             # Setpoints.CtrlPotencia_SetpointNivel
        "CRTL_POT_NIVEL_MIN_ALARME":            22,                             # Setpoints.CtrlPotencia_NivelMinimoAlarme
        "CRTL_POT_NIVEL_MIN_TRIP":              23,                             # Setpoints.CtrlPotencia_NivelMinimoTRIP
        "CTRL_POT_POT_MAX":                     89,                             # Setpoints.CtrlPotencia_PotenciaMaxima

        # Controle Reativo
        "CRTL_REATIVO_SP_FP":                   24,                             # Setpoints.CtrlReativo_SetpointFP
        "CRTL_REATIVO_SP_REATIVO":              25,                             # Setpoints.CtrlReativo_SetpointReativo

        # Turbina
        "TURB_VIBRA_01_ALARME":                 26,                             # Setpoints.Turb_Vibracao01Alarme
        "TURB_VIBRA_01_TRIP":                   27,                             # Setpoints.Turb_Vibracao01TRIP
        "TURB_VIBRA_02_ALARME":                 28,                             # Setpoints.Turb_Vibracao02Alarme
        "TURB_VIBRA_02_TRIP":                   29,                             # Setpoints.Turb_Vibracao02TRIP
        "TURB_VIBRA_03_ALARME":                 30,                             # Setpoints.Turb_Vibracao03Alarme
        "TURB_VIBRA_03_TRIP":                   31,                             # Setpoints.Turb_Vibracao03TRIP
        "TURB_VIBRA_04_ALARME":                 32,                             # Setpoints.Turb_Vibracao04Alarme
        "TURB_VIBRA_04_TRIP":                   33,                             # Setpoints.Turb_Vibracao04TRIP
        "TURB_TEMPO_EQUALI_SP":                 34,                             # Setpoints.Turb_TempoEqualizacaoSetpoint
        "TURB_VIBRA_05_ALARME":                 90,                             # Setpoints.Turb_Vibracao05Alarme
        "TURB_VIBRA_05_TRIP":                   91,                             # Setpoints.Turb_Vibracao05TRIP

        # Freio
        "FREIO_PULSO_INTERVALO":                35,                             # Setpoints.Freio_PulsoIntervalo
        "FREIO_PULSO_TEMPO":                    36,                             # Setpoints.Freio_PulsoTempo

        # UHCT
        "UHCT_RODIZIO_PRINCIPAL":               37,                             # Setpoints.UHCT_RodizioPrincipal
        "UHCT_RODIZIO_RETAGUARDA":              38,                             # Setpoints.UHCT_RodizioRetaguarda

        # UHLM
        "UHLM_RODIZIO_PRINCIPAL":               39,                             # Setpoints.UHLM_RodizioPrincipal
        "UHLM_RODIZIO_RETAGUARDA":              40,                             # Setpoints.UHLM_RodizioRetaguarda
        "UHLM_SP_VAZAO_01":                     92,                             # Setpoints.UHLM_SetpointVazao01
        "UHLM_SP_VAZAO_02":                     93,                             # Setpoints.UHLM_SetpointVazao02
        "UHLM_SP_VAZAO_03":                     94,                             # Setpoints.UHLM_SetpointVazao03
        "UHLM_SP_VAZAO_04":                     95,                             # Setpoints.UHLM_SetpointVazao04

        # Temperaturas
        "TEMPERATURA_01_ALARME":                41,                             # Setpoints.Temperatura01_Alarme
        "TEMPERATURA_02_ALARME":                42,                             # Setpoints.Temperatura02_Alarme
        "TEMPERATURA_03_ALARME":                43,                             # Setpoints.Temperatura03_Alarme
        "TEMPERATURA_04_ALARME":                44,                             # Setpoints.Temperatura04_Alarme
        "TEMPERATURA_05_ALARME":                45,                             # Setpoints.Temperatura05_Alarme
        "TEMPERATURA_06_ALARME":                46,                             # Setpoints.Temperatura06_Alarme
        "TEMPERATURA_07_ALARME":                47,                             # Setpoints.Temperatura07_Alarme
        "TEMPERATURA_08_ALARME":                48,                             # Setpoints.Temperatura08_Alarme
        "TEMPERATURA_09_ALARME":                49,                             # Setpoints.Temperatura09_Alarme
        "TEMPERATURA_10_ALARME":                50,                             # Setpoints.Temperatura10_Alarme
        "TEMPERATURA_11_ALARME":                51,                             # Setpoints.Temperatura11_Alarme
        "TEMPERATURA_12_ALARME":                52,                             # Setpoints.Temperatura12_Alarme
        "TEMPERATURA_13_ALARME":                53,                             # Setpoints.Temperatura13_Alarme
        "TEMPERATURA_14_ALARME":                54,                             # Setpoints.Temperatura14_Alarme
        "TEMPERATURA_15_ALARME":                55,                             # Setpoints.Temperatura15_Alarme
        "TEMPERATURA_16_ALARME":                56,                             # Setpoints.Temperatura16_Alarme
        "TEMPERATURA_01_TRIP01":                57,                             # Setpoints.Temperatura01_TRIP01
        "TEMPERATURA_02_TRIP01":                58,                             # Setpoints.Temperatura02_TRIP01
        "TEMPERATURA_03_TRIP01":                59,                             # Setpoints.Temperatura03_TRIP01
        "TEMPERATURA_04_TRIP01":                60,                             # Setpoints.Temperatura04_TRIP01
        "TEMPERATURA_05_TRIP01":                61,                             # Setpoints.Temperatura05_TRIP01
        "TEMPERATURA_06_TRIP01":                62,                             # Setpoints.Temperatura06_TRIP01
        "TEMPERATURA_07_TRIP01":                63,                             # Setpoints.Temperatura07_TRIP01
        "TEMPERATURA_08_TRIP01":                64,                             # Setpoints.Temperatura08_TRIP01
        "TEMPERATURA_09_TRIP01":                65,                             # Setpoints.Temperatura09_TRIP01
        "TEMPERATURA_10_TRIP01":                66,                             # Setpoints.Temperatura10_TRIP01
        "TEMPERATURA_11_TRIP01":                67,                             # Setpoints.Temperatura11_TRIP01
        "TEMPERATURA_12_TRIP01":                68,                             # Setpoints.Temperatura12_TRIP01
        "TEMPERATURA_13_TRIP01":                69,                             # Setpoints.Temperatura13_TRIP01
        "TEMPERATURA_14_TRIP01":                70,                             # Setpoints.Temperatura14_TRIP01
        "TEMPERATURA_15_TRIP01":                71,                             # Setpoints.Temperatura15_TRIP01
        "TEMPERATURA_16_TRIP01":                72,                             # Setpoints.Temperatura16_TRIP01
        "TEMPERATURA_01_TRIP02":                73,                             # Setpoints.Temperatura01_TRIP02
        "TEMPERATURA_02_TRIP02":                74,                             # Setpoints.Temperatura02_TRIP02
        "TEMPERATURA_03_TRIP02":                75,                             # Setpoints.Temperatura03_TRIP02
        "TEMPERATURA_04_TRIP02":                76,                             # Setpoints.Temperatura04_TRIP02
        "TEMPERATURA_05_TRIP02":                77,                             # Setpoints.Temperatura05_TRIP02
        "TEMPERATURA_06_TRIP02":                78,                             # Setpoints.Temperatura06_TRIP02
        "TEMPERATURA_07_TRIP02":                79,                             # Setpoints.Temperatura07_TRIP02
        "TEMPERATURA_08_TRIP02":                80,                             # Setpoints.Temperatura08_TRIP02
        "TEMPERATURA_09_TRIP02":                81,                             # Setpoints.Temperatura09_TRIP02
        "TEMPERATURA_10_TRIP02":                82,                             # Setpoints.Temperatura10_TRIP02
        "TEMPERATURA_11_TRIP02":                83,                             # Setpoints.Temperatura11_TRIP02
        "TEMPERATURA_12_TRIP02":                84,                             # Setpoints.Temperatura12_TRIP02
        "TEMPERATURA_13_TRIP02":                85,                             # Setpoints.Temperatura13_TRIP02
        "TEMPERATURA_14_TRIP02":                86,                             # Setpoints.Temperatura14_TRIP02
        "TEMPERATURA_15_TRIP02":                87,                             # Setpoints.Temperatura15_TRIP02
        "TEMPERATURA_16_TRIP02":                88,                             # Setpoints.Temperatura16_TRIP02

        # Grade Suja
        "GradeSuja_TRIP":                       96,                             # Setpoints.GradeSuja_TRIP

        # Curva
        "CURVA_01_DISTRIB_P1":                  97,                             # Setpoints.Curva01_DistribuidorP1
        "CURVA_01_DISTRIB_P2":                  98,                             # Setpoints.Curva01_DistribuidorP2
        "CURVA_01_DISTRIB_P3":                  99,                             # Setpoints.Curva01_DistribuidorP3
        "CURVA_01_DISTRIB_P4":                  100,                            # Setpoints.Curva01_DistribuidorP4
        "CURVA_01_DISTRIB_P5":                  101,                            # Setpoints.Curva01_DistribuidorP5
        "CURVA_01_DISTRIB_P6":                  102,                            # Setpoints.Curva01_DistribuidorP6
        "CURVA_01_DISTRIB_P7":                  103,                            # Setpoints.Curva01_DistribuidorP7
        "CURVA_01_DISTRIB_P8":                  104,                            # Setpoints.Curva01_DistribuidorP8
        "CURVA_01_DISTRIB_P9":                  105,                            # Setpoints.Curva01_DistribuidorP9
        "CURVA_01_DISTRIB_P10":                 106,                            # Setpoints.Curva01_DistribuidorP10
        "CURVA_01_ROTOR_P1":                    107,                            # Setpoints.Curva01_RotorP1
        "CURVA_01_ROTOR_P2":                    108,                            # Setpoints.Curva01_RotorP2
        "CURVA_01_ROTOR_P3":                    109,                            # Setpoints.Curva01_RotorP3
        "CURVA_01_ROTOR_P4":                    110,                            # Setpoints.Curva01_RotorP4
        "CURVA_01_ROTOR_P5":                    111,                            # Setpoints.Curva01_RotorP5
        "CURVA_01_ROTOR_P6":                    112,                            # Setpoints.Curva01_RotorP6
        "CURVA_01_ROTOR_P7":                    113,                            # Setpoints.Curva01_RotorP7
        "CURVA_01_ROTOR_P8":                    114,                            # Setpoints.Curva01_RotorP8
        "CURVA_01_ROTOR_P9":                    115,                            # Setpoints.Curva01_RotorP9
        "CURVA_01_ROTOR_P10":                   116,                            # Setpoints.Curva01_RotorP10
        "CURVA_02_DISTRIB_P1":                  117,                            # Setpoints.Curva02_DistribuidorP1
        "CURVA_02_DISTRIB_P2":                  118,                            # Setpoints.Curva02_DistribuidorP2
        "CURVA_02_DISTRIB_P3":                  119,                            # Setpoints.Curva02_DistribuidorP3
        "CURVA_02_DISTRIB_P4":                  120,                            # Setpoints.Curva02_DistribuidorP4
        "CURVA_02_DISTRIB_P5":                  121,                            # Setpoints.Curva02_DistribuidorP5
        "CURVA_02_DISTRIB_P6":                  122,                            # Setpoints.Curva02_DistribuidorP6
        "CURVA_02_DISTRIB_P7":                  123,                            # Setpoints.Curva02_DistribuidorP7
        "CURVA_02_DISTRIB_P8":                  124,                            # Setpoints.Curva02_DistribuidorP8
        "CURVA_02_DISTRIB_P9":                  125,                            # Setpoints.Curva02_DistribuidorP9
        "CURVA_02_DISTRIB_P10":                 126,                            # Setpoints.Curva02_DistribuidorP10
        "CURVA_02_ROTOR_P1":                    127,                            # Setpoints.Curva02_RotorP1
        "CURVA_02_ROTOR_P2":                    128,                            # Setpoints.Curva02_RotorP2
        "CURVA_02_ROTOR_P3":                    129,                            # Setpoints.Curva02_RotorP3
        "CURVA_02_ROTOR_P4":                    130,                            # Setpoints.Curva02_RotorP4
        "CURVA_02_ROTOR_P5":                    131,                            # Setpoints.Curva02_RotorP5
        "CURVA_02_ROTOR_P6":                    132,                            # Setpoints.Curva02_RotorP6
        "CURVA_02_ROTOR_P7":                    133,                            # Setpoints.Curva02_RotorP7
        "CURVA_02_ROTOR_P8":                    134,                            # Setpoints.Curva02_RotorP8
        "CURVA_02_ROTOR_P9":                    135,                            # Setpoints.Curva02_RotorP9
        "CURVA_02_ROTOR_P10":                   136,                            # Setpoints.Curva02_RotorP10
        "CURVA_03_DISTRIB_P1":                  137,                            # Setpoints.Curva03_DistribuidorP1
        "CURVA_03_DISTRIB_P2":                  138,                            # Setpoints.Curva03_DistribuidorP2
        "CURVA_03_DISTRIB_P3":                  139,                            # Setpoints.Curva03_DistribuidorP3
        "CURVA_03_DISTRIB_P4":                  140,                            # Setpoints.Curva03_DistribuidorP4
        "CURVA_03_DISTRIB_P5":                  141,                            # Setpoints.Curva03_DistribuidorP5
        "CURVA_03_DISTRIB_P6":                  142,                            # Setpoints.Curva03_DistribuidorP6
        "CURVA_03_DISTRIB_P7":                  143,                            # Setpoints.Curva03_DistribuidorP7
        "CURVA_03_DISTRIB_P8":                  144,                            # Setpoints.Curva03_DistribuidorP8
        "CURVA_03_DISTRIB_P9":                  145,                            # Setpoints.Curva03_DistribuidorP9
        "CURVA_03_DISTRIB_P10":                 146,                            # Setpoints.Curva03_DistribuidorP10
        "CURVA_03_ROTOR_P1":                    147,                            # Setpoints.Curva03_RotorP1
        "CURVA_03_ROTOR_P2":                    148,                            # Setpoints.Curva03_RotorP2
        "CURVA_03_ROTOR_P3":                    149,                            # Setpoints.Curva03_RotorP3
        "CURVA_03_ROTOR_P4":                    150,                            # Setpoints.Curva03_RotorP4
        "CURVA_03_ROTOR_P5":                    151,                            # Setpoints.Curva03_RotorP5
        "CURVA_03_ROTOR_P6":                    152,                            # Setpoints.Curva03_RotorP6
        "CURVA_03_ROTOR_P7":                    153,                            # Setpoints.Curva03_RotorP7
        "CURVA_03_ROTOR_P8":                    154,                            # Setpoints.Curva03_RotorP8
        "CURVA_03_ROTOR_P9":                    155,                            # Setpoints.Curva03_RotorP9
        "CURVA_03_ROTOR_P10":                   156,                            # Setpoints.Curva03_RotorP10
        "CURVA_04_DISTRIB_P1":                  157,                            # Setpoints.Curva04_DistribuidorP1
        "CURVA_04_DISTRIB_P2":                  158,                            # Setpoints.Curva04_DistribuidorP2
        "CURVA_04_DISTRIB_P3":                  159,                            # Setpoints.Curva04_DistribuidorP3
        "CURVA_04_DISTRIB_P4":                  160,                            # Setpoints.Curva04_DistribuidorP4
        "CURVA_04_DISTRIB_P5":                  161,                            # Setpoints.Curva04_DistribuidorP5
        "CURVA_04_DISTRIB_P6":                  162,                            # Setpoints.Curva04_DistribuidorP6
        "CURVA_04_DISTRIB_P7":                  163,                            # Setpoints.Curva04_DistribuidorP7
        "CURVA_04_DISTRIB_P8":                  164,                            # Setpoints.Curva04_DistribuidorP8
        "CURVA_04_DISTRIB_P9":                  165,                            # Setpoints.Curva04_DistribuidorP9
        "CURVA_04_DISTRIB_P10":                 166,                            # Setpoints.Curva04_DistribuidorP10
        "CURVA_04_ROTOR_P1":                    167,                            # Setpoints.Curva04_RotorP1
        "CURVA_04_ROTOR_P2":                    168,                            # Setpoints.Curva04_RotorP2
        "CURVA_04_ROTOR_P3":                    169,                            # Setpoints.Curva04_RotorP3
        "CURVA_04_ROTOR_P4":                    170,                            # Setpoints.Curva04_RotorP4
        "CURVA_04_ROTOR_P5":                    171,                            # Setpoints.Curva04_RotorP5
        "CURVA_04_ROTOR_P6":                    172,                            # Setpoints.Curva04_RotorP6
        "CURVA_04_ROTOR_P7":                    173,                            # Setpoints.Curva04_RotorP7
        "CURVA_04_ROTOR_P8":                    174,                            # Setpoints.Curva04_RotorP8
        "CURVA_04_ROTOR_P9":                    175,                            # Setpoints.Curva04_RotorP9
        "CURVA_04_ROTOR_P10":                   176,                            # Setpoints.Curva04_RotorP10
        "CURVA_05_DISTRIB_P1":                  177,                            # Setpoints.Curva05_DistribuidorP1
        "CURVA_05_DISTRIB_P2":                  178,                            # Setpoints.Curva05_DistribuidorP2
        "CURVA_05_DISTRIB_P3":                  179,                            # Setpoints.Curva05_DistribuidorP3
        "CURVA_05_DISTRIB_P4":                  180,                            # Setpoints.Curva05_DistribuidorP4
        "CURVA_05_DISTRIB_P5":                  181,                            # Setpoints.Curva05_DistribuidorP5
        "CURVA_05_DISTRIB_P6":                  182,                            # Setpoints.Curva05_DistribuidorP6
        "CURVA_05_DISTRIB_P7":                  183,                            # Setpoints.Curva05_DistribuidorP7
        "CURVA_05_DISTRIB_P8":                  184,                            # Setpoints.Curva05_DistribuidorP8
        "CURVA_05_DISTRIB_P9":                  185,                            # Setpoints.Curva05_DistribuidorP9
        "CURVA_05_DISTRIB_P10":                 186,                            # Setpoints.Curva05_DistribuidorP10
        "CURVA_05_ROTOR_P1":                    187,                            # Setpoints.Curva05_RotorP1
        "CURVA_05_ROTOR_P2":                    188,                            # Setpoints.Curva05_RotorP2
        "CURVA_05_ROTOR_P3":                    189,                            # Setpoints.Curva05_RotorP3
        "CURVA_05_ROTOR_P4":                    190,                            # Setpoints.Curva05_RotorP4
        "CURVA_05_ROTOR_P5":                    191,                            # Setpoints.Curva05_RotorP5
        "CURVA_05_ROTOR_P6":                    192,                            # Setpoints.Curva05_RotorP6
        "CURVA_05_ROTOR_P7":                    193,                            # Setpoints.Curva05_RotorP7
        "CURVA_05_ROTOR_P8":                    194,                            # Setpoints.Curva05_RotorP8
        "CURVA_05_ROTOR_P9":                    195,                            # Setpoints.Curva05_RotorP9
        "CURVA_05_ROTOR_P10":                   196,                            # Setpoints.Curva05_RotorP10

        # Referencia Curva
        "REFER_CURVA_01":                       197,                            # Setpoints.ReferenciaCurva01
        "REFER_CURVA_02":                       198,                            # Setpoints.ReferenciaCurva02
        "REFER_CURVA_03":                       199,                            # Setpoints.ReferenciaCurva03
        "REFER_CURVA_04":                       200,                            # Setpoints.ReferenciaCurva04
        "REFER_CURVA_05":                       201,                            # Setpoints.ReferenciaCurva05

        # Outros
        "TEMPO_ATUALIZACAO":                    202,                            # Setpoints.TempoAtualizacao
        "MODO_OPERACAO_RETENTIVO":              203,                            # Setpoints.ModoOperacao_Retentivo
        "CURVA_SEL_RETENTIVO":                  204,                            # Setpoints.CurvaSelecionada_Retentivo


        ## LEITURAS

        # Nível
        "NV_JUSANTE":                           2,                              # Leituras.NivelJusante
        "NV_BARRAGEM":                          3,                              # Leituras.NivelBarragem
        "NV_CANAL":                             4,                              # Leituras.NivelCanal
        "NV_CAMARA_CARGA":                      5,                              # Leituras.NivelCamaraCarga
        "QUEDA_BRUTA":                          131,                            # Leituras.QuedaBruta

        # Operação
        "OPER_PAINEL_RESET_ALARMES":            6,                              # Leituras.Operacao_PainelResetAlarmes
        "OPER_PAINEL_RECONHECE_ALARMES":        7,                              # Leituras.Operacao_PainelReconheceAlarmes
        "OPER_INFO":                            8,                              # Leituras.Operacao_Info
        "OPER_ETAPA_ALVO":                      9,                              # Leituras.Operacao_EtapaAlvo
        "OPER_ETAPA_ATUAL":                     10,                             # Leituras.Operacao_EtapaAtual
        "OPER_ETAPA_TRANSICAO":                 11,                             # Leituras.Operacao_EtapaTransicao
        "OPER_INFO_PARADA":                     12,                             # Leituras.Operacao_InfoParada

        # UHCT
        "UHCT_INFO":                            13,                             # Leituras.UHCT_Info
        "UHCT_BOMBAS":                          14,                             # Leituras.UHCT_Bombas
        "UHCT_RODIZIO":                         15,                             # Leituras.UHCT_Rodizio
        "UHCT_VALVULAS":                        16,                             # Leituras.UHCT_Valvulas
        "UHCT_FILTROS":                         17,                             # Leituras.UHCT_Filtros
        "UHCT_PRESSOSTATOS":                    18,                             # Leituras.UHCT_Pressostatos
        "UHCT_NIVEL":                           19,                             # Leituras.UHCT_Nivel
        "UHCT_PRESSAO_OLEO":                    20,                             # Leituras.UHCT_PressaoOleo
        "UHCT_ACUM_RODIZIO_PRINCIPAL":          21,                             # Leituras.UHCT_AcumuladorRodizioPrincipal
        "UHCT_ACUM_RODIZIO_RETAGUARDA":         22,                             # Leituras.UHCT_AcumuladorRodizioRetaguarda

        # UHLM
        "UHLM_INFO":                            23,                             # Leituras.UHLM_Info
        "UHLM_BOMBAS":                          24,                             # Leituras.UHLM_Bombas
        "UHLM_RODIZIO":                         25,                             # Leituras.UHLM_Rodizio
        "UHLM_FILTROS":                         26,                             # Leituras.UHLM_Filtros
        "UHLM_PRESSOSTATOS":                    27,                             # Leituras.UHLM_Pressostatos
        "UHLM_FLUXOSTATOS":                     28,                             # Leituras.UHLM_Fluxostatos
        "UHLM_NIVEL":                           29,                             # Leituras.UHLM_Nivel
        "UHLM_ACUM_RODIZIO_PRINCIPAL":          30,                             # Leituras.UHLM_AcumuladorRodizioPrincipal
        "UHLM_ACUM_RODIZIO_RETAGUARDA":         31,                             # Leituras.UHLM_AcumuladorRodizioRetaguarda
        "UHLM_FLUXOSTATO_OLEO_01":              123,                            # Leituras.UHLM_FluxostatoOleo01
        "UHLM_FLUXOSTATO_OLEO_02":              124,                            # Leituras.UHLM_FluxostatoOleo02
        "UHLM_FLUXOSTATO_OLEO_03":              125,                            # Leituras.UHLM_FluxostatoOleo03
        "UHLM_FLUXOSTATO_OLEO_04":              126,                            # Leituras.UHLM_FluxostatoOleo04

        # Turbina
        "TURB_INFO":                            32,                             # 
        "TURB_VALVULA_BYPASS":                  33,                             # 
        "TURB_VALVULA_BORBOLETA":               34,                             # 
        "TURB_TEMPO_CRACK_EFETIVO":             35,                             # 
        "TURB_TEMPO_EQUAL_EFETIVO":             36,                             # 
        "TURB_PRESSAO_CONDUTO":                 37,                             # 
        "TURB_PRESSAO_CAIXA_ESPIRAL":           38,                             # 
        "TURB_VAZAO_TURBINADA":                 39,                             # 
        "TURB_VIBRACAO_01":                     40,                             # 
        "TURB_VIBRACAO_02":                     41,                             # 
        "TURB_VIBRACAO_03":                     42,                             # 
        "TURB_VIBRACAO_04":                     43,                             # 
        "TURB_FRENAGEM":                        44,                             # 
        "TURB_VIBRACAO_05":                     127,                            # 

        # Reg V
        "REG_V_INFO":                           45,                             # 
        "REG_V_ESTADO":                         46,                             # 
        "REG_V_VELOCIDADE":                     47,                             # 
        "REG_V_DISTRIBUIDOR":                   48,                             # 
        "REG_V_ROTOR":                          49,                             # 
        "REG_V_POT_ALVO":                       50,                             # 
        "REG_V_CURVA_CONJUG_INFO":              128,                            # 

        # Reg T
        "REG_T_INFO":                           51,                             # 
        "REG_T_UEXCITACAO":                     52,                             # 
        "REG_T_IEXCITACAO":                     53,                             # 
        "REG_T_FPALVO":                         129,                                # 
        "REG_T_REATIVO_ALVO":                   130,                                # 

        # Sinc
        "SINC_INFO":                            54,                             # 
        "SINC_FREQ_GERADOR":                    55,                             # 
        "SINC_FREQ_BARRA":                      56,                             # 
        "SINC_TENSAO_GERADOR":                  57,                             # 
        "SINC_TENSAO_BARRA":                    58,                             # 

        # DJ
        "Dj52G_INFO":                           59,                             # 

        # Tensão
        "TENSAO_RN":                            60,                             # 
        "TENSAO_SN":                            61,                             # 
        "TENSAO_TN":                            62,                             # 
        "TENSAO_RS":                            63,                             # 
        "TENSAO_ST":                            64,                             # 
        "TENSAO_TR":                            65,                             # 

        # Corrente
        "CORRENTE_R":                           66,                             # 
        "CORRENTE_S":                           67,                             # 
        "CORRENTE_T":                           68,                             # 
        "CORRENTE_MEDIA":                       69,                             # 

        # Potência Ativa
        "POT_ATIVA_1":                          70,                             # 
        "POT_ATIVA_2":                          71,                             # 
        "POT_ATIVA_3":                          72,                             # 
        "POT_ATIVA_MEDIA":                      73,                             # 

        # Potência Reativa
        "POT_REATIVA_1":                        74,                             # 
        "POT_REATIVA_2":                        75,                             # 
        "POT_REATIVA_3":                        76,                             # 
        "POT_REATIVA_MEDIA":                    77,                             # 

        # Potência Aparente
        "POT_APARENTE_1":                       78,                             # 
        "POT_APARENTE_2":                       79,                             # 
        "POT_APARENTE_3":                       80,                             # 
        "POT_APARENTE_MEDIA":                   81,                             # 

        # Fator Potência
        "FATOR_POT_1":                          82,                             # 
        "FATOR_POT_2":                          83,                             # 
        "FATOR_POT_3":                          84,                             # 
        "FATOR_POT_MEDIA":                      85,                             # 

        # Frequencia
        "FREQUENCIA":                           86,                             # 

        # Energia Fornecida
        "ENERGIA_FORNECIDA_TWh":                87,                             # 
        "ENERGIA_FORNECIDA_GWh":                88,                             # 
        "ENERGIA_FORNECIDA_MWh":                89,                             # 
        "ENERGIA_FORNECIDA_kWh":                90,                             # 
        "ENERGIA_FORNECIDA_TVarh":              91,                             # 
        "ENERGIA_FORNECIDA_GVarh":              92,                             # 
        "ENERGIA_FORNECIDA_MVarh":              93,                             # 
        "ENERGIA_FORNECIDA_kVarh":              94,                             # 
        "ENERGIA_CORNECIDA_TVarh":              95,                             # 
        "ENERGIA_CORNECIDA_GVarh":              96,                             # 
        "ENERGIA_CORNECIDA_MVarh":              97,                             # 
        "ENERGIA_CORNECIDA_kVarh":              98,                             # 

        # Controles
        "CTRL_REATIVO_INFO":                    100,                                # 
        "CTRL_POTENCIA_INFO":                   101,                                # 

        # Horimetros
        "HORIM_ELETR_LOW":                      102,                                # 
        "HORIM_ELETR_HIGH":                     103,                                # 
        "HORIM_MECAN_LOW":                      104,                                # 
        "HORIM_MECAN_HIGH":                     105,                                # 

        # Temperatura
        "TEMPERATURA_01":                       107,                                # 
        "TEMPERATURA_02":                       108,                                # 
        "TEMPERATURA_03":                       109,                                # 
        "TEMPERATURA_04":                       110,                                # 
        "TEMPERATURA_05":                       111,                                # 
        "TEMPERATURA_06":                       112,                                # 
        "TEMPERATURA_07":                       113,                                # 
        "TEMPERATURA_08":                       114,                                # 
        "TEMPERATURA_09":                       115,                                # 
        "TEMPERATURA_10":                       116,                                # 
        "TEMPERATURA_11":                       117,                                # 
        "TEMPERATURA_12":                       118,                                # 
        "TEMPERATURA_13":                       119,                                # 
        "TEMPERATURA_14":                       120,                                # 
        "TEMPERATURA_15":                       121,                                # 
        "TEMPERATURA_16":                       122,                                # 


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
        "Alarme04_10":                          [4, 10],
        "Alarme04_11":                          [4, 11],
        "Alarme04_12":                          [4, 12],

        "Alarme10_08":                          [10, 8],
        "Alarme10_09":                          [10, 9],

        "Alarme12_01":                          [12, 1],
        "Alarme12_07":                          [12, 7],
        "Alarme12_08":                          [12, 8],
        "Alarme12_09":                          [12, 9],
        "Alarme12_10":                          [12, 10],
        "Alarme12_11":                          [12, 11],
        "Alarme12_12":                          [12, 12],
        "Alarme12_13":                          [12, 13],

        "Alarme15_12":                          [15, 12],
        "Alarme15_13":                          [15, 13],

        # Gerais
        "Alarme01_01":                          [1, 1],
        "Alarme01_02":                          [1, 2],
        "Alarme01_00":                          [1, 0],
        "Alarme01_03":                          [1, 3],
        "Alarme01_06":                          [1, 6],
        "Alarme01_07":                          [1, 7],
        "Alarme01_08":                          [1, 8],
        "Alarme01_09":                          [1, 9],
        "Alarme01_10":                          [1, 10],
        "Alarme01_11":                          [1, 11],
        "Alarme01_12":                          [1, 12],
        "Alarme01_13":                          [1, 13],
        "Alarme01_14":                          [1, 14],
        "Alarme01_15":                          [1, 15],

        "Alarme02_00":                          [2, 0],
        "Alarme02_01":                          [2, 1],
        "Alarme02_02":                          [2, 2],
        "Alarme02_03":                          [2, 3],
        "Alarme02_04":                          [2, 4],
        "Alarme02_05":                          [2, 5],
        "Alarme02_06":                          [2, 6],
        "Alarme02_07":                          [2, 7],
        "Alarme02_08":                          [2, 8],
        "Alarme02_09":                          [2, 9],
        "Alarme02_10":                          [2, 10],
        "Alarme02_11":                          [2, 11],
        "Alarme02_12":                          [2, 12],
        "Alarme02_13":                          [2, 13],
        "Alarme02_14":                          [2, 14],
        "Alarme02_15":                          [2, 15],

        "Alarme03_00":                          [3, 0],
        "Alarme03_01":                          [3, 1],
        "Alarme03_02":                          [3, 2],
        "Alarme03_03":                          [3, 3],
        "Alarme03_04":                          [3, 4],
        "Alarme03_05":                          [3, 5],
        "Alarme03_06":                          [3, 6],
        "Alarme03_07":                          [3, 7],
        "Alarme03_08":                          [3, 8],
        "Alarme03_09":                          [3, 9],
        "Alarme03_10":                          [3, 10],
        "Alarme03_11":                          [3, 11],
        "Alarme03_12":                          [3, 12],
        "Alarme03_13":                          [3, 13],
        "Alarme03_14":                          [3, 14],
        "Alarme03_15":                          [3, 15],

        "Alarme04_00":                          [4, 0],
        "Alarme04_01":                          [4, 1],
        "Alarme04_02":                          [4, 2],
        "Alarme04_04":                          [4, 4],
        "Alarme04_05":                          [4, 5],
        "Alarme04_06":                          [4, 6],
        "Alarme04_07":                          [4, 7],
        "Alarme04_09":                          [4, 9],
        "Alarme04_10":                          [4, 10],
        "Alarme04_11":                          [4, 11],
        "Alarme04_12":                          [4, 12],
        "Alarme04_13":                          [4, 13],
        "Alarme04_14":                          [4, 14],
        "Alarme04_15":                          [4, 15],

        "Alarme05_00":                          [5, 0],
        "Alarme05_02":                          [5, 2],
        "Alarme05_03":                          [5, 3],
        "Alarme05_04":                          [5, 4],
        "Alarme05_05":                          [5, 5],
        "Alarme05_06":                          [5, 6],
        "Alarme05_07":                          [5, 7],
        "Alarme05_09":                          [5, 9],
        "Alarme05_10":                          [5, 10],
        "Alarme05_11":                          [5, 11],
        "Alarme05_12":                          [5, 12],
        "Alarme05_13":                          [5, 13],
        "Alarme05_14":                          [5, 14],
        "Alarme05_15":                          [5, 15],

        "Alarme06_00":                          [6, 0],
        "Alarme06_03":                          [6, 3],
        "Alarme06_04":                          [6, 4],
        "Alarme06_05":                          [6, 5],
        "Alarme06_08":                          [6, 8],
        "Alarme06_09":                          [6, 9],
        "Alarme06_10":                          [6, 10],
        "Alarme06_11":                          [6, 11],
        "Alarme06_12":                          [6, 12],
        "Alarme06_13":                          [6, 13],
        "Alarme06_14":                          [6, 14],
        "Alarme06_15":                          [6, 15],

        "Alarme07_00":                          [7, 0],
        "Alarme07_01":                          [7, 1],
        "Alarme07_02":                          [7, 2],
        "Alarme07_03":                          [7, 3],
        "Alarme07_06":                          [7, 6],
        "Alarme07_07":                          [7, 7],
        "Alarme07_08":                          [7, 8],
        "Alarme07_09":                          [7, 9],
        "Alarme07_10":                          [7, 10],
        "Alarme07_11":                          [7, 11],
        "Alarme07_12":                          [7, 12],
        "Alarme07_13":                          [7, 13],
        "Alarme07_14":                          [7, 14],
        "Alarme07_15":                          [7, 15],

        "Alarme08_00":                          [8, 0],
        "Alarme08_01":                          [8, 1],
        "Alarme08_02":                          [8, 2],
        "Alarme08_03":                          [8, 3],
        "Alarme08_07":                          [8, 7],
        "Alarme08_08":                          [8, 8],
        "Alarme08_09":                          [8, 9],
        "Alarme08_10":                          [8, 10],
        "Alarme08_11":                          [8, 11],
        "Alarme08_12":                          [8, 12],
        "Alarme08_13":                          [8, 13],
        "Alarme08_14":                          [8, 14],
        "Alarme08_15":                          [8, 15],

        "Alarme09_00":                          [9, 0],
        "Alarme09_01":                          [9, 1],
        "Alarme09_02":                          [9, 2],
        "Alarme09_03":                          [9, 3],
        "Alarme09_04":                          [9, 4],
        "Alarme09_06":                          [9, 6],
        "Alarme09_07":                          [9, 7],
        "Alarme09_08":                          [9, 8],
        "Alarme09_09":                          [9, 9],
        "Alarme09_10":                          [9, 10],
        "Alarme09_11":                          [9, 11],
        "Alarme09_12":                          [9, 12],
        "Alarme09_13":                          [9, 13],
        "Alarme09_14":                          [9, 14],
        "Alarme09_15":                          [9, 15],

        "Alarme10_00":                          [10, 0],
        "Alarme10_01":                          [10, 1],
        "Alarme10_02":                          [10, 2],
        "Alarme10_03":                          [10, 3],
        "Alarme10_05":                          [10, 5],
        "Alarme10_06":                          [10, 6],
        "Alarme10_07":                          [10, 7],
        "Alarme10_08":                          [10, 8],
        "Alarme10_09":                          [10, 9],
        "Alarme10_10":                          [10, 10],
        "Alarme10_11":                          [10, 11],
        "Alarme10_12":                          [10, 12],
        "Alarme10_13":                          [10, 13],
        "Alarme10_14":                          [10, 14],
        "Alarme10_15":                          [10, 15],

        "Alarme11_00":                          [11, 0],
        "Alarme11_01":                          [11, 1],
        "Alarme11_02":                          [11, 2],
        "Alarme11_06":                          [11, 6],
        "Alarme11_07":                          [11, 7],
        "Alarme11_08":                          [11, 8],
        "Alarme11_09":                          [11, 9],
        "Alarme11_10":                          [11, 10],
        "Alarme11_11":                          [11, 11],
        "Alarme11_12":                          [11, 12],
        "Alarme11_13":                          [11, 13],
        "Alarme11_14":                          [11, 14],
        "Alarme11_15":                          [11, 15],

        "Alarme12_01":                          [12, 1],
        "Alarme12_02":                          [12, 2],
        "Alarme12_03":                          [12, 3],
        "Alarme12_04":                          [12, 4],
        "Alarme12_05":                          [12, 5],
        "Alarme12_06":                          [12, 6],
        "Alarme12_07":                          [12, 7],
        "Alarme12_09":                          [12, 9],
        "Alarme12_10":                          [12, 10],
        "Alarme12_11":                          [12, 11],
        "Alarme12_12":                          [12, 12],
        "Alarme12_13":                          [12, 13],
        "Alarme12_14":                          [12, 14],
        "Alarme12_15":                          [12, 15],

        "Alarme13_00":                          [13, 0],
        "Alarme13_01":                          [13, 1],
        "Alarme13_02":                          [13, 2],
        "Alarme13_03":                          [13, 3],
        "Alarme13_09":                          [13, 9],
        "Alarme13_10":                          [13, 10],
        "Alarme13_11":                          [13, 11],
        "Alarme13_12":                          [13, 12],
        "Alarme13_13":                          [13, 13],
        "Alarme13_14":                          [13, 14],
        "Alarme13_15":                          [13, 15],

        "Alarme14_00":                          [14, 0],
        "Alarme14_01":                          [14, 1],
        "Alarme14_02":                          [14, 2],
        "Alarme14_03":                          [14, 3],
        "Alarme14_04":                          [14, 4],
        "Alarme14_05":                          [14, 5],
        "Alarme14_10":                          [14, 10],
        "Alarme14_11":                          [14, 11],
        "Alarme14_12":                          [14, 12],
        "Alarme14_13":                          [14, 13],
        "Alarme14_14":                          [14, 14],
        "Alarme14_15":                          [14, 15],

        "Alarme15_00":                          [15, 0],
        "Alarme15_01":                          [15, 1],
        "Alarme15_02":                          [15, 2],
        "Alarme15_03":                          [15, 3],
        "Alarme15_04":                          [15, 4],
        "Alarme15_05":                          [15, 5],
        "Alarme15_06":                          [15, 6],
        "Alarme15_07":                          [15, 7],
        "Alarme15_08":                          [15, 8],
        "Alarme15_09":                          [15, 9],
        "Alarme15_10":                          [15, 10],
        "Alarme15_12":                          [15, 12],
        "Alarme15_13":                          [15, 13],
        "Alarme15_14":                          [15, 14],
        "Alarme15_15":                          [15, 15],

        "Alarme16_00":                          [16, 0],
        "Alarme16_01":                          [16, 1],
        "Alarme16_02":                          [16, 2],
        "Alarme16_03":                          [16, 3],
        "Alarme16_04":                          [16, 4],
        "Alarme16_05":                          [16, 5],
        "Alarme16_06":                          [16, 6],
        "Alarme16_07":                          [16, 7],
        "Alarme16_08":                          [16, 8],
        "Alarme16_09":                          [16, 9],
        "Alarme16_10":                          [16, 10],
        "Alarme16_11":                          [16, 11],
        "Alarme16_12":                          [16, 12],
    },
}