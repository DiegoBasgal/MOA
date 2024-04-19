REG_RELE = {
    "BAY": {
        "LT_FASE_A":                                                11,
        "LT_FASE_B":                                                14,
        "LT_FASE_C":                                                17,
        "LT_VS":                                                    19,

        "RELE_RST_TRP":                                             88,
        "DJL_CMD_ABRIR":                                            84,
        "DJL_CMD_FECHAR":                                           85,

        "DJL_FECHADO":                                              [44, 0],
        "DJL_MOLA_CARREGADA":                                       [44, 1],
        "BT_ABRE_DJ":                                               [44, 2],
        "BT_FECHA_DJ":                                              [44, 3],
        "SECC_FECHADA":                                             [44, 4],

        "SOBRECORRENTE_INSTANTANEA_DE_FASE_ZONA_3":                 [46, 5],
        "SOBRECORRENTE_INSTANTANEA_DE_FASE_ZONA_2":                 [46, 6],
        "SOBRECORRENTE_INSTANTANEA_DE_FASE_ZONA_1":                 [46, 7],

        "FALHA_ABERTURA_DISJUNTOR_DE_LINHA":                        [47, 1],

        "SOBRECORRENTE_INSTANTANEA_DE_SEQUENCIA_NEGATIVA_ZONA_3":   [48, 1],
        "SOBRECORRENTE_INSTANTANEA_DE_SEQUENCIA_NEGATIVA_ZONA_2":   [48, 2],
        "SOBRECORRENTE_INSTANTANEA_DE_SEQUENCIA_NEGATIVA_ZONA_1":   [48, 3],
        "SOBRECORRENTE_RESIDUAL_INSTANTANEA":                       [48, 7],

        "SOBRECORRENTE_TEMPORIZADA_DE_FASE":                        [49, 2],

        "SOBRECORRENTE_RESIDUAL_TEMPORIZADA":                       [50, 4],

        "ID_BARRA_VIVA":                                            [53, 1],
        "ID_BARRA_MORTA":                                           [53, 7],

        "ID_LINHA_VIVA":                                            [54, 0],
        "ID_LINHA_MORTA":                                           [54, 1],
    },

    "SE": {
        "DJL_FECHADO":                                              [43, 0],
        "DJL_MOLA_CARREGADA":                                       [43, 1],

        "RELE_TE_FLH_PARTIDA":                                      [43, 2],

        "SECC_FECHADA":                                             [43, 1],

        "50BF_FALHA_ABERTURA_DISJUNTOR_DE_LINHA_B3":                [44, 3],
        "50BF_FALHA_ABERTURA_DISJUNTOR_DE_LINHA_B4":                [44, 4],

        "SOBRECORRENTE_INSTANTANEA_DE_FASE_ZONA_1":                 [45, 7],
        "SOBRECORRENTE_INSTANTANEA_DE_FASE_ZONA_2":                 [45, 6],
        "SOBRECORRENTE_INSTANTANEA_DE_FASE_ZONA_3":                 [45, 5],

        "SOBRECORRENTE_INSTANTANEA_DE_SEQUENCIA_NEGATIVA_ZONA_1":   [46, 3],
        "SOBRECORRENTE_INSTANTANEA_DE_SEQUENCIA_NEGATIVA_ZONA_2":   [46, 2],
        "SOBRECORRENTE_INSTANTANEA_DE_SEQUENCIA_NEGATIVA_ZONA_3":   [46, 1],

        "SOBRECORRENTE_TEMPORIZADA_DE_FASE":                        [47, 2],

        "FALHA_ABERTURA_DISJUNTOR_DE_LINHA":                        [48, 1],

        "ID_BARRA_VIVA":                                            [49, 1],
    },

    "TE": {
        # Bloqueio
        "86T_ATUADO":                                   [36, 4],


        # Enrolamento
        "ENROL_SEC_SOBRECO_TEMPO_RES":                  [36, 1],
        "ENROL_SEC_SOBRECO_TEMPO_FASE":                 [36, 6],


        # Enrolamento
        "ENROL_PRI_SOBRECO_TEMPO_FASE":                 [1117, 3],
        "ENROL_PRI_SOBRECO_TEMPO_RES":                  [1117, 4],
        # Diferencial
        "DIF_COM_RESTRICAO":                            [1117, 14],
        "DIF_SEM_RESTRICAO":                            [1117, 15],


        # Relé
        "RELE_ESTADO_TRP":                              [1118, 15],
    },

    "UG1": {
        # Elementos
        "ELE_2_SOBREFRE":                               [1, 4],
        "ELE_1_SOBREFRE":                               [1, 5],
        "ELE_2_SUBFRE":                                 [1, 6],
        "ELE_1_SUBFRE":                                 [1, 7],

        # Sobrecorrente
        "SOBRECO_INST":                                 [901, 0],
        "SOBRECO_INST_NEUTRO":                          [901, 1],
        "SOBRECO_SEQU_NEG":                             [901, 2],
        "SOBRECO_TEMPO_NEUTRO":                         [901, 4],
        # Diferencial
        "DIF_COM_RESTRICAO":                            [901, 14],
        "DIF_SEM_RESTRICAO":                            [901, 15],


        # Outros
        "SUBTEN_GERAL":                                 [902, 0],
        "SOBRETEN_GERAL":                               [902, 1],
        "POT_REVERSA":                                  [902, 3],
        "VOLTZ_HERTZ":                                  [902, 5],
        "LT_SOBRECO_RESTRICAO":                         [902, 6],
        "DJ_MAQUINA_FLH_ABERTURA_B8":                   [902, 8],
        "RECIBO_TRANS_DISP":                            [902, 9],
        "PERDA_CAMPO_GERAL":                            [902, 11],
        "FUGA_SOBRECO_GERAL":                           [902, 12],
        "UNIDADE_FORA_PASSO":                           [902, 14],


        # DJ
        "DJ_MAQUINA_FLH_ABERTURA_B7":                   [2100, 7],
        "DJ_MAQUINA_FLH_PARTIDA":                       [2100, 6],


        # Transformador Elevador
        "TE_RELE_LINHA_TRANS_DISP":                     [2100, 11],


        # Relé
        "RELE_PROTECAO_TRP_B5":                         [2110, 5],
        "RELE_PROTECAO_TRP_B6":                         [2110, 6],
    },

    "UG2": {
        # Elementos
        "ELE_2_SUBFRE":                                 [29, 6],
        "ELE_1_SUBFRE":                                 [29, 7],

        "ELE_2_SOBREFRE":                               [146, 4],
        "ELE_1_SOBREFRE":                               [146, 6],


        # Sobrecorrente
        "SOBRECO_INST":                                 [901, 0],
        "SOBRECO_INST_NEUTRO":                          [901, 1],
        "SOBRECO_SEQU_NEG":                             [901, 2],
        "SOBRECO_TEMPO_NEUTRO":                         [901, 4],
        # Diferencial
        "DIF_COM_RESTRICAO":                            [901, 14],
        "DIF_SEM_RESTRICAO":                            [901, 15],


        # Outros
        "SUBTEN_GERAL":                                 [902, 0],
        "SOBRETEN_GERAL":                               [902, 1],
        "POT_REVERSA":                                  [902, 3],
        "VOLTZ_HERTZ":                                  [902, 5],
        "LT_SOBRECO_RESTRICAO":                         [902, 6],
        "DJ_MAQUINA_FLH_ABERTURA_B8":                   [902, 8],
        "RECIBO_TRANS_DISP":                            [902, 9],
        "PERDA_CAMPO_GERAL":                            [902, 11],
        "FUGA_SOBRECO_GERAL":                           [902, 12],
        "UNIDADE_FORA_PASSO":                           [902, 14],


        # DJ
        "DJ_MAQUINA_FLH_ABERTURA_B7":                   [2100, 7],
        "DJ_MAQUINA_FLH_PARTIDA":                       [2100, 6],


        # Transformador Elevador
        "TE_RELE_LINHA_TRANS_DISP":                     [2100, 11],


        # Relé
        "RELE_PROTECAO_TRP_B5":                         [2110, 5],
        "RELE_PROTECAO_TRP_B6":                         [2110, 6],
    },
}

REG_CLP = {
    "SA_SE": {
        ### STATUS
        ## ENTRADAS_DIGITAIS_1
        "DRENAGEM_BOMBA_1_FALHA":                                                                           [1, 0],
        "DRENAGEM_BOMBA_1_LIGADA":                                                                          [1, 1],
        "DRENAGEM_BOMBA_2_FALHA":                                                                           [1, 2],
        "DRENAGEM_BOMBA_2_LIGADA":                                                                          [1, 3],
        "DRENAGEM_BOMBA_3_FALHA":                                                                           [1, 4],
        "DRENAGEM_BOMBA_3_LIGADA":                                                                          [1, 5],
        "SISTEMA_FILTRAGEM_BOMBA_FALHA":                                                                    [1, 6],
        "SISTEMA_FILTRAGEM_BOMBA_LIGADA":                                                                   [1, 7],
        "ACIONAMENTO_RESERVA_1_FALHA":                                                                      [1, 8],
        "ACIONAMENTO_RESERVA_1_LIGADO":                                                                     [1, 9],
        "ACIONAMENTO_RESERVA_2_FALHA":                                                                      [1, 10],
        "ACIONAMENTO_RESERVA_2_LIGADO":                                                                     [1, 11],
        "BOMBA_ESGOTAMENTO_UNIDADES_FALHA":                                                                 [1, 12],
        "BOMBA_ESGOTAMENTO_UNIDADES_LIGADA":                                                                [1, 13],
        "ACIONAMENTO_RESERVA_4_FALHA":                                                                      [1, 14],
        "ACIONAMENTO_RESERVA_4_LIGADO":                                                                     [1, 15],

        "ACIONAMENTO_RESERVA_3_FALHA":                                                                      [0, 0],
        "ACIONAMENTO_RESERVA_3_LIGADO":                                                                     [0, 1],
        "SISTEMA_FILTRAGEM_FILTRO_B_ELEMENTO_1_ENTRADA_ABERTA":                                             [0, 2],
        "SISTEMA_FILTRAGEM_FILTRO_B_ELEMENTO_2_ENTRADA_ABERTA":                                             [0, 3],
        "SISTEMA_FILTRAGEM_FILTRO_B_ELEMENTO_1_RETROLAVAGEM_ABERTA":                                        [0, 4],
        "SISTEMA_FILTRAGEM_FILTRO_B_ELEMENTO_2_RETROLAVAGEM_ABERTA":                                        [0, 5],
        "SISTEMA_FILTRAGEM_PRESSAO_AGUA_SAIDA_FILTRO_B":                                                    [0, 6],
        "DISJUNTOR_52SA2_ALIMENTACAO_EXTERNA_SUBTENSAO":                                                    [0, 7],
        "COM_TENSAO_LINHA_EXTERNA":                                                                         [0, 8], # HIGH
        "DRENAGEM_NIVEL_MUITO_ALTO":                                                                        [0, 9],
        "DRENAGEM_NIVEL_ALTO":                                                                              [0, 10],
        "DRENAGEM_NIVEL_LIGA_BOMBAS":                                                                       [0, 11],
        "DRENAGEM_NIVEL_DESLIGA_BOMBAS":                                                                    [0, 12],
        "DRENAGEM_NIVEL_BLOQUEIA_BOMBAS":                                                                   [0, 13],
        "RETIFICADOR_SOBRETENSAO_CC":                                                                       [0, 14], # HIGH
        "RETIFICADOR_SUBTENSAO_CC":                                                                         [0, 15], # HIGH

        ## ENTRADAS_DIGITAIS_2
        "RETIFICADOR_SOBRECORRENTE_SAIDA":                                                                  [3, 0], # HIGH
        "RETIFICADOR_SOBRECORRENTE_BATERIAS":                                                               [3, 1], # HIGH
        "RETIFICADOR_FUSIVEL_QUEIMADO":                                                                     [3, 2], # HIGH
        "RETIFICADOR_FALTA_CA":                                                                             [3, 3], # HIGH
        "RETIFICADOR_FALHA_ATIVA":                                                                          [3, 4], # HIGH
        "RETIFICADOR_FUGA_TERRA_POSITIVO":                                                                  [3, 5], # HIGH
        "RETIFICADOR_FUGA_TERRA_NEGATIVO":                                                                  [3, 6], # HIGH
        "CUBICULO_FECHAMENTO_BARRAS_DISJUNTOR_TP_SINCRONISMO_52G101_ABERTO":                                [3, 7], # HIGH
        "CUBICULO_FECHAMENTO_BARRAS_DISJUNTOR_TP_SINCRONISMO_52G101_FALHA":                                 [3, 8], # HIGH
        "CUBICULO_FECHAMENTO_BARRAS_PORTA_INTERNA_ABERTA":                                                  [3, 9], # HIGH
        "CUBICULO_FECHAMENTO_BARRAS_PORTA_TRASEIRA_ABERTA":                                                 [3, 10], # HIGH
        "SECCIONADORA_89L_FECHADA":                                                                         [3, 11],
        "DISJUTOR_52L_FECHADO":                                                                             [3, 14],

        "MOLA_52L_CARREGADA":                                                                               [2, 0],
        "CUBICULO_DISJUNTOR_DE_LINHA_PORTA_INTERNA_ABERTA":                                                 [2, 1], # HIGH
        "TRANSFORMADOR_ELEVADOR_ALARME_TEMPERATURA_OLEO":                                                   [2, 2],
        "TRANSFORMADOR_ELEVADOR_TRIP_TEMPERATURA_OLEO":                                                     [2, 3],
        "TRANSFORMADOR_ELEVADOR_ALARME_TEMPERATURA_ENROLAMENTO":                                            [2, 4],
        "TRANSFORMADOR_ELEVADOR_TRIP_TEMPERATURA_ENROLAMENTO":                                              [2, 5],
        "TRANSFORMADOR_ELEVADOR_ALARME_RELE_BUCHHOLZ":                                                      [2, 6],
        "TRANSFORMADOR_ELEVADOR_TRIP_RELE_BUCHHOLZ":                                                        [2, 7],
        "TRANSFORMADOR_ELEVADOR_ALARME_ALIVIO_DE_PRESSAO":                                                  [2, 8],
        "TRANSFORMADOR_ELEVADOR_TRIP_ALIVIO_DE_PRESSAO":                                                    [2, 9],
        "TRANSFORMADOR_ELEVADOR_ALARME_NIVEL_OLEO_ALTO":                                                    [2, 10],
        "TRANSFORMADOR_ELEVADOR_TRIP_NIVEL_OLEO_MUITO_BAIXO":                                               [2, 11],
        "BLOQUEIO_86BF_ATUACAO_RESERVA":                                                                    [2, 14],
        "DISJUNTOR_52SA1_TRANSFORMADOR_SERVICOS_AUXILIARES_FALHA":                                          [2, 15], # HIGH

        ## ENTRADAS_DIGITAIS_3
        "DISJUNTOR_52SA1_TRANSFORMADOR_SERVICOS_AUXILIARES_FECHADO":                                        [4, 0],
        "DISJUNTOR_52SA2_GERADOR_DIESEL_DE_EMERGENCIA_FALHA":                                               [4, 1], # HIGH
        "DISJUNTOR_52SA2_GERADOR_DIESEL_DE_EMERGENCIA_FECHADO":                                             [4, 2],
        "DISJUNTOR_52SA3_INTERLIGACAO_BARRAS_FALHA":                                                        [4, 3], # HIGH
        "DISJUNTOR_52SA3_INTERLIGACAO_BARRAS_FECHADO":                                                      [4, 4],
        "DISJUNTOR_52SA1_TRANSFORMADOR_SERVICOS_AUXILIARES_SUBTENSAO":                                      [4, 5], # HIGH
        "DISJUNTOR_52SA2_GERADOR_DIESEL_DE_EMERGENCIA_SUBTENSAO":                                           [4, 6], # HIGH
        "BARRA_SERVICOS_AUXILIARES_ESSENCIAIS_SUBTENSAO":                                                   [4, 7], # HIGH
        "BARRA_SERVICOS_AUXILIARES_NAO-ESSENCIAIS_SUBTENSAO":                                               [4, 8], # HIGH
        "SELETORA_DISJUNTORES_BARRA_SERVICOS_AUXILIARES_EM_REMOTO":                                         [4, 9],
        "SELETORA_DISJUNTOR_52L_EM_REMOTO":                                                                 [4, 10],
        "CONVERSOR_FIBRA_BAY_FALHA":                                                                        [4, 11], # HIGH
        "CONVERSOR_FIBRA_TOMADA_DAGUA_FALHA":                                                               [4, 12], # HIGH
        "BOTAO_EMEGENCIA_ACIONADO":                                                                         [4, 13], # HIGH
        "RELE_DE_PROTECAO_DA_LINHA_TRIP":                                                                   [4, 14],
        "RELE_DE_PROTECAO_DA_LINHA_FALHA_WATCHDOG":                                                         [4, 15],

        "RELE_DE_PROTECAO_DA_LINHA_86BF":                                                                   [5, 0],
        "RELE_DE_PROTECAO_DO_TRANSFORMADOR_ELEVADOR_TRIP":                                                  [5, 1],
        "RELE_DE_PROTECAO_DO_TRANSFORMADOR_ELEVADOR_FALHA_WATCHDOG":                                        [5, 2],
        "RELE_DE_BLOQUEIO_FALHA_ABERTURA_DISJUNTORES_86BF":                                                 [5, 3],
        "RELE_DE_BLOQUEIO_TRANSFORMADOR_ELEVADOR_86T":                                                      [5, 4],
        "SUPERVISAO_BOBINAS_RELES_DE_BLOQUEIO_INTEGRAS":                                                    [5, 5],
        "BOTAO_REARME_RELE_DE_BLOQUEIO_86BF":                                                               [5, 6],
        "BOTAO_REARME_RELE_DE_BLOQUEIO_86BT":                                                               [5, 7],
        "BLOQUEIO_86T_ATUACAO_RESERVA_1":                                                                   [5, 8],
        "BLOQUEIO_86T_ATUACAO_RESERVA_2":                                                                   [5, 9],
        "CLP_UNIDADE_GERADORA_1_COMANDO_HABILITA_SISTEMA_AGUA":                                             [5, 10],
        "CLP_UNIDADE_GERADORA_1_COMANDO_RESERVA_2":                                                         [5, 11],
        "CLP_UNIDADE_GERADORA_1_COMANDO_RESERVA_3":                                                         [5, 12],
        "CLP_UNIDADE_GERADORA_2_COMANDO_HABILITA_SISTEMA_AGUA":                                             [5, 13],
        "CLP_UNIDADE_GERADORA_2_COMANDO_RESERVA_2":                                                         [5, 14],
        "CLP_UNIDADE_GERADORA_2_COMANDO_RESERVA_3":                                                         [5, 15],

        ## ENTRADAS_DIGITAIS_4
        "TRANSFORMADOR_ELEVADOR_FALHA_CONTROLADOR_LOCAL":                                                   [6, 0],
        "SISTEMA_FILTRAGEM_FILTRO_A_ELEMENTO_1_ENTRADA_ABERTA":                                             [6, 1],
        "SISTEMA_FILTRAGEM_FILTRO_A_ELEMENTO_2_ENTRADA_ABERTA":                                             [6, 2],
        "SISTEMA_FILTRAGEM_FILTRO_A_ELEMENTO_1_RETROLAVAGEM_ABERTA":                                        [6, 3],
        "SISTEMA_FILTRAGEM_FILTRO_A_ELEMENTO_2_RETROLAVAGEM_ABERTA":                                        [6, 4],
        "SISTEMA_FILTRAGEM_PRESSAO_AGUA_SAIDA_FILTRO_A":                                                    [6, 5],
        "SINAL_DO_SISTEMA_DE_INCENDIO":                                                                     [6, 6],
        "SINAL_DO_SISTEMA_DE_SEGURANCA":                                                                    [6, 7],
        "DISJUNTOR_GERAL_CORRENTE_CONTINUA_125VCC_72SA1_FECHADO":                                           [6, 10],
        "DISJUNTORES_CORRENTE_CONTINUA_125VCC_ABERTOS":                                                     [6, 11], # HIGH
        "DISJUNTORES_CORRENTE_CONTINUA_24VCC_ABERTOS":                                                      [6, 12], # HIGH
        "SUBTENSAO_ALIMENTACAO_SERVICOS_AUXILIARES_125VCC":                                                 [6, 13], # HIGH
        "SUBTENSAO_COMANDO_SERVICOS_AUXILIARES_125VCC":                                                     [6, 14], # HIGH
        "SUBTENSAO_COMANDO_SERVICOS_AUXILIARES_24VCC":                                                      [6, 15], # HIGH

        ## ALARMES_ANALÓGICOS
        "ALARME_NIVEL_CANAL_DE_FUGA":                                                                       [8, 0],

        ## FALHAS_ANALÓGICAS
        "FALHA_LEITURA_NIVEL_CANAL_DE_FUGA":                                                                [10, 0],
        "FALHA_LEITURA_TEMPERATURA_OLEO_TRANFORMADOR_ELEVADOR":                                             [10, 1],
        "FALHA_LEITURA_TEMPERATURA_ENROLAMENTO_TRANFORMADOR_ELEVADOR":                                      [10, 2],
        "FALHA_LEITURA_FILTRO_A_PRESSAO_DIFERENCIAL_ELEMENTO_1":                                            [10, 3],
        "FALHA_LEITURA_FILTRO_A_PRESSAO_DIFERENCIAL_ELEMENTO_2":                                            [10, 4],
        "FALHA_LEITURA_FILTRO_B_PRESSAO_DIFERENCIAL_ELEMENTO_1":                                            [10, 5],
        "FALHA_LEITURA_FILTRO_B_PRESSAO_DIFERENCIAL_ELEMENTO_2":                                            [10, 6],

        ## SA
        "DISJUNTOR_SERVICOS_AUXILIARES_52SA1_FALHA_ABERTURA":                                               [12, 0],
        "DISJUNTOR_SERVICOS_AUXILIARES_52SA1_FALHA_FECHAMENTO":                                             [12, 1],
        "DISJUNTOR_GERADOR_DIESEL_52SA2_FALHA_ABERTURA":                                                    [12, 2],
        "DISJUNTOR_GERADOR_DIESEL_52SA2_FALHA_FECHAMENTO":                                                  [12, 3],
        "DISJUNTOR_INTERLIGACAO_BARRAS_52SA3_FALHA_ABERTURA":                                               [12, 4],
        "DISJUNTOR_INTERLIGACAO_BARRAS_52SA3_FALHA_FECHAMENTO":                                             [12, 5],
        "GERADOR_DIESEL_DE_EMERGENCIA_FALHA_PARTIDA":                                                       [12, 6],
        "GERADOR_DIESEL_DE_EMERGENCIA_FALHA_PARADA":                                                        [12, 7],
        "GERADOR_DIESEL_DE_EMERGENCIA_PARTIDA_PERIODICA":                                                   [12, 8],
        "DRENAGEM_DISCREPANCIA_SINAIS_NIVEL":                                                               [12, 9],
        "GERADOR_DIESEL_DE_EMERGENCIA_OPERACAO_REMOTA_MANUAL":                                              [12, 10],
        "FALHA_COMUNICACAO_COM_MULTIMEDIDOR_LT":                                                            [12, 11],
        "FALHA_COMUNICACAO_COM_MULTIMEDIDOR_TSA":                                                           [12, 12],
        "FALHA_COMUNICACAO_COM_MULTIMEDIDOR_GMG":                                                           [12, 13],

        ## BLOQUEIO_GERAL
        "BLOQUEIO_GERAL_BLOQUEIO_00_NIVEL_MUITO_ALTO_POCO_DRENAGEM":                                        [14, 0],
        "BLOQUEIO_GERAL_BLOQUEIO_01_SUBTENSAO_CC_RETIFICADOR":                                              [14, 1],
        "BLOQUEIO_GERAL_BLOQUEIO_02_CUBICULO_DE_FECHAMENTO_DE_BARRA_PORTA_TRASEIRA_ABERTA":                 [14, 2],
        "BLOQUEIO_GERAL_BLOQUEIO_03_CUBICULO_DE_FECHAMENTO_DE_BARRA_PORTA_INTERNA_ABERTA":                  [14, 3],
        "BLOQUEIO_GERAL_BLOQUEIO_04_RELE_PROTECAO_LINHA_FALHA_ABERTURA_52L_ATUADO":                         [14, 4],
        "BLOQUEIO_GERAL_BLOQUEIO_05_RELE_PROTECAO_LINHA_FALHA_WATCHDOG":                                    [14, 5],
        "BLOQUEIO_GERAL_BLOQUEIO_06_BOTAO_EMERGENCIA_GERAL":                                                [14, 6],
        "BLOQUEIO_GERAL_BLOQUEIO_07_TEMPO_EXCESSIVO_NIVEL_ALTO_POCO_DRENAGEM":                              [14, 7],
        "BLOQUEIO_GERAL_BLOQUEIO_08_TEMPO_EXCESSIVO_DISCREPANCIA_SINAIS_BOIAS_POCO_DRENAGEM":               [14, 8],
        "BLOQUEIO_GERAL_BLOQUEIO_09_RESERVA":                                                               [14, 9],

        "BLOQUEIO_GERAL":                                                                                   [15, 15],

        ## SISTEMA_AGUA
        "SISTEMA_AGUA_BOMBA_DISPONIVEL":                                                                    [16, 0],
        "SISTEMA_AGUA_FALHA_LIGAR_BOMBA":                                                                   [16, 1],
        "SISTEMA_AGUA_FALHA_DESLIGAR_BOMBA":                                                                [16, 2],
        "SISTEMA_AGUA_FALHA_PRESSURIZAR_SAIDA_FILTRO_A":                                                    [16, 3],
        "SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_A":                                                          [16, 4],
        "SISTEMA_AGUA_FALHA_PRESSURIZAR_SAIDA_FILTRO_B":                                                    [16, 5],
        "SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_B":                                                          [16, 6],

        ## FILTRO_AUTOLIMPANTE
        "FILTRO_B_OPERANDO_ELEMENTO_1":                                                                     [18, 0],
        "FILTRO_B_LIMPANDO_ELEMENTO_2":                                                                     [18, 1],
        "FILTRO_B_OPERANDO_ELEMENTO_2":                                                                     [18, 2],
        "FILTRO_B_LIMPANDO_ELEMENTO_1":                                                                     [18, 3],
        "FILTRO_B_FALHA_ABRIR_ENTRADA_ELEMENTO_1":                                                          [18, 4],
        "FILTRO_B_FALHA_FECHAR_ENTRADA_ELEMENTO_1":                                                         [18, 5],
        "FILTRO_B_FALHA_ABRIR_ENTRADA_ELEMENTO_2":                                                          [18, 6],
        "FILTRO_B_FALHA_FECHAR_ENTRADA_ELEMENTO_2":                                                         [18, 7],
        "FILTRO_B_FALHA_ABRIR_RETROLAVAGEM_ELEMENTO_1":                                                     [18, 8],
        "FILTRO_B_FALHA_FECHAR_RETROLAVAGEM_ELEMENTO_1":                                                    [18, 9],
        "FILTRO_B_FALHA_ABRIR_RETROLAVAGEM_ELEMENTO_2":                                                     [18, 10],
        "FILTRO_B_FALHA_FECHAR_RETROLAVAGEM_ELEMENTO_2":                                                    [18, 11],
        "FILTRO_B_COMUTACAO_EM_MANUAL":                                                                     [18, 12],

        "FILTRO_A_OPERANDO_ELEMENTO_1":                                                                     [19, 0],
        "FILTRO_A_LIMPANDO_ELEMENTO_2":                                                                     [19, 1],
        "FILTRO_A_OPERANDO_ELEMENTO_2":                                                                     [19, 2],
        "FILTRO_A_LIMPANDO_ELEMENTO_1":                                                                     [19, 3],
        "FILTRO_A_FALHA_ABRIR_ENTRADA_ELEMENTO_1":                                                          [19, 4],
        "FILTRO_A_FALHA_FECHAR_ENTRADA_ELEMENTO_1":                                                         [19, 5],
        "FILTRO_A_FALHA_ABRIR_ENTRADA_ELEMENTO_2":                                                          [19, 6],
        "FILTRO_A_FALHA_FECHAR_ENTRADA_ELEMENTO_2":                                                         [19, 7],
        "FILTRO_A_FALHA_ABRIR_RETROLAVAGEM_ELEMENTO_1":                                                     [19, 8],
        "FILTRO_A_FALHA_FECHAR_RETROLAVAGEM_ELEMENTO_1":                                                    [19, 9],
        "FILTRO_A_FALHA_ABRIR_RETROLAVAGEM_ELEMENTO_2":                                                     [19, 10],
        "FILTRO_A_FALHA_FECHAR_RETROLAVAGEM_ELEMENTO_2":                                                    [19, 11],
        "FILTRO_A_COMUTACAO_EM_MANUAL":                                                                     [19, 12],

        ## SE
        "REGISTRO_ATUACAO_RELE_DE_PROTECAO_DA_LINHA":                                                       [20, 0],
        "FALHA_COMANDO_ABERTURA_DISJUNTOR_52L":                                                             [20, 1],
        "FALHA_COMANDO_FECHAMENTO_DISJUNTOR_52L":                                                           [20, 2],

        ## BLOQUEIO_86T
        "BLOQUEIO_86T_BLOQUEIO_00_RELE_DE_PROTECAO_TRANSFORMADOR_ELEVADOR_ATUADO":                          [22, 0],
        "BLOQUEIO_86T_BLOQUEIO_01_RELE_DE_PROTECAO_TRANSFORMADOR_ELEVADOR_FALHA_WATCHDOG":                  [22, 1],
        "BLOQUEIO_86T_BLOQUEIO_02_TRANSFORMADOR_ELEVADOR_TEMPERATURA_MUITO_ALTA_OLEO":                      [22, 2],
        "BLOQUEIO_86T_BLOQUEIO_03_TRANSFORMADOR_ELEVADOR_TEMPERATURA_MUITO_ALTA_ENROLAMENTO":               [22, 3],
        "BLOQUEIO_86T_BLOQUEIO_04_TRANSFORMADOR_ELEVADOR_RELE_BUCHHOLZ":                                    [22, 4],
        "BLOQUEIO_86T_BLOQUEIO_05_TRANSFORMADOR_ELEVADOR_ALIVIO_DE_PRESSAO":                                [22, 5],
        "BLOQUEIO_86T_BLOQUEIO_06_TRANSFORMADOR_ELEVADOR_NIVEL_OLEO_MUITO_BAIXO":                           [22, 6],
        "BLOQUEIO_86T_BLOQUEIO_07_TRANSFORMADOR_ELEVADOR_FALHA_CONTROLADOR_LOCAL":                          [22, 7],
        "BLOQUEIO_86T_BLOQUEIO_08_TRANSFORMADOR_ELEVADOR_ATUACAO_RESERVA_1":                                [22, 8],
        "BLOQUEIO_86T_BLOQUEIO_09_TRANSFORMADOR_ELEVADOR_ATUACAO_RESERVA_2":                                [22, 9],

        "BLOQUEIO_86T":                                                                                     [23, 15],

        ## LEITURAS_ANALÓGICAS
        "NIVEL_CANAL_FUGA":                                                                                 24,
        "TE_TEMPERATURA_OLEO":                                                                              26,
        "TE_TEMPERATURA_ENROLAMENTO":                                                                       28,
        "FILTRO_A_PRESSAO_DIFERENCIAL_ELEMENTO_1":                                                          30,
        "FILTRO_A_PRESSAO_DIFERENCIAL_ELEMENTO_2":                                                          32,
        "FILTRO_B_PRESSAO_DIFERENCIAL_ELEMENTO_1":                                                          34,
        "FILTRO_B_PRESSAO_DIFERENCIAL_ELEMENTO_2":                                                          36,

        ## HORÍMETROS
        "BOMBA_1_DRENAGEM":                                                                                 38,
        "BOMBA_2_DRENAGEM":                                                                                 40,
        "BOMBA_3_DRENAGEM":                                                                                 42,
        "BOMBA_ESGOTAMENTO_UNIDADES":                                                                       44,
        "BOMBA_SISTEMA_AGUA":                                                                               48,

        ## MULTIMEDIDOR_LT
        "VAB":                                                                                              50,
        "VBC":                                                                                              52,
        "VCA":                                                                                              54,
        "IA":                                                                                               56,
        "IB":                                                                                               58,
        "IC":                                                                                               60,
        "P":                                                                                                62,
        "Q":                                                                                                64,
        "S":                                                                                                66,
        "F":                                                                                                68,
        "FP":                                                                                               70,
        "EAP":                                                                                              72,
        "EAN":                                                                                              74,
        "ERP":                                                                                              76,
        "ERN":                                                                                              78,

        ## MULTIMEDIDOR_TSA
        "VAB":                                                                                              80,
        "VBC":                                                                                              82,
        "VCA":                                                                                              84,
        "IA":                                                                                               86,
        "IB":                                                                                               88,
        "IC":                                                                                               90,
        "P":                                                                                                92,
        "Q":                                                                                                94,
        "S":                                                                                                96,
        "F":                                                                                                98,
        "FP":                                                                                               100,
        "EAP":                                                                                              102,

        ## MULTIMEDIDOR_GMG
        "VAB":                                                                                              104,
        "VBC":                                                                                              106,
        "VCA":                                                                                              108,
        "IA":                                                                                               110,
        "IB":                                                                                               112,
        "IC":                                                                                               114,
        "P":                                                                                                116,
        "Q":                                                                                                118,
        "S":                                                                                                120,
        "F":                                                                                                122,
        "FP":                                                                                               124,
        "EAP":                                                                                              262,


        ### COMANDOS
        ## SA
        "COMANDO_RESET_FALHAS_BARRA_SERVICOS_AUXILIARES":                                                   [1, 0],
        "COMANDO_RESET_FALHAS_SISTEMA_AGUA":                                                                [1, 1],
        "COMANDO_RESERVA_1":                                                                                [1, 2],
        "COMANDO_RESERVA_2":                                                                                [1, 3],
        "COMANDO_SELECIONA_SEQUENCIA_123_BOMBAS_DRENAGEM":                                                  [1, 5],
        "COMANDO_SELECIONA_SEQUENCIA_231_BOMBAS_DRENAGEM":                                                  [1, 6],
        "COMANDO_SELECIONA_SEQUENCIA_312_BOMBAS_DRENAGEM":                                                  [1, 7],
        "COMANDO_SELECIONA_OPERACAO_MANUAL_GERADOR_DIESEL_DE_EMERGENCIA":                                   [1, 8],
        "COMANDO_SELECIONA_OPERACAO_AUTOMATICA_GERADOR_DIESEL_DE_EMERGENCIA":                               [1, 9],
        "COMANDO_PARTE_MANUAL_GERADOR_DIESEL_DE_EMERGENCIA":                                                [1, 10],
        "COMANDO_PARA_MANUAL_GERADOR_DIESEL_DE_EMERGENCIA":                                                 [1, 11],

        "COMANDO_COMUTA_FILTRO_A":                                                                          [0, 2],
        "COMANDO_SELECIONA_COMUTACAO_EM_AUTOMATICO_FILTRO_A":                                               [0, 3],
        "COMANDO_SELECIONA_COMUTACAO_EM_MANUAL_FILTRO_A":                                                   [0, 4],
        "COMANDO_COMUTA_FILTRO_B":                                                                          [0, 5],
        "COMANDO_SELECIONA_COMUTACAO_EM_AUTOMATICO_FILTRO_B":                                               [0, 6],
        "COMANDO_SELECIONA_COMUTACAO_EM_MANUAL_FILTRO_B":                                                   [0, 7],

        ## SE
        "COMANDO_REARME_BLOQUEIO_EXTERNO":                                                                  [3, 0],
        "COMANDO_REARME_BLOQUEIO_86T":                                                                      [3, 1],
        "COMANDO_REARME_BLOQUEIO_86BF":                                                                     [3, 2],
        "COMANDO_ABRE_DISJUNTOR_52L":                                                                       [3, 3],
        "COMANDO_FECHA_DISJUNTOR_52L":                                                                      [3, 4],
        "COMANDO_RESET_REGISTROS":                                                                          [3, 5],
    },

    "TDA": {
        ### STATUS
        ## ENTRADAS_DIGITAIS
        "LIMPA_GRADES_RASTELO_RECOLHIDO":                                                                   [1, 0],
        "LIMPA_GRADES_POSICAO_INICIAL_ESQUERDA":                                                            [1, 1],
        "LIMPA_GRADES_INCREMENTA_POSICAO_LIMPEZA":                                                          [1, 2],
        "LIMPA_GRADES_SELETORA_EM_AUTOMATICO":                                                              [1, 3],
        "LIMPA_GRADES_BOTAO_AFASTA_RASTELO":                                                                [1, 4],
        "LIMPA_GRADES_BOTAO_DESCE_RASTELO":                                                                 [1, 5],
        "LIMPA_GRADES_BOTAO_SOBE_RASTELO":                                                                  [1, 6],
        "LIMPA_GRADES_BOTAO_MOVIMENTA_PARA_ESQUERDA":                                                       [1, 7],
        "LIMPA_GRADES_BOTAO_MOVIMENTA_PARA_DIREITA":                                                        [1, 8],
        "LIMPA_GRADES_BOTAO_INICIA_CICLO_LIMPEZA":                                                          [1, 9],
        "UNIDADE_HIDRAULICA_BOMBA_LIGADA":                                                                  [1, 10],
        "SUBTENSAO_CA":                                                                                     [1, 11], # HIGH
        "UNIDADE_HIDRAULICA_NIVEL_OLEO_MUITO_BAIXO":                                                        [1, 12], # HIGH
        "UNIDADE_HIDRAULICA_FILTRO_SUJO":                                                                   [1, 13], # HIGH
        "COMPORTA_1_ABERTA":                                                                                [1, 14],
        "COMPORTA_1_FECHADA":                                                                               [1, 15],

        "COMPORTA_1_CRACKING":                                                                              [0, 0],
        "COMPORTA_2_ABERTA":                                                                                [0, 1],
        "COMPORTA_2_FECHADA":                                                                               [0, 2],
        "COMPORTA_2_CRACKING":                                                                              [0, 3],
        "VALVULA_BORBOLETA_ABERTA":                                                                         [0, 4],
        "VALVULA_BORBOLETA_FECHADA":                                                                        [0, 5],
        "COMPORTA_1_SELETORA_EM_REMOTO":                                                                    [0, 6],
        "LIMPA_GRADES_BOTAO_RESET_FALHAS":                                                                  [0, 7],
        "BOTAO_EMERGENCIA_ACIONADO":                                                                        [0, 8],
        "COMPORTA_2_SELETORA_EM_REMOTO":                                                                    [0, 9],
        "COMPORTA_1_PERMISSIVO_ABERTURA":                                                                   [0, 10],
        "COMPORTA_2_PERMISSIVO_ABERTURA":                                                                   [0, 11],
        "ENTRADA_DIGITAL_RESERVA_1":                                                                        [0, 12],
        "ENTRADA_DIGITAL_RESERVA_2":                                                                        [0, 13],

        ## FALHAS_ANALÓGICAS
        "FALHA_LEITURA_NIVEL_MONTANTE":                                                                     [3, 0],
        "FALHA_LEITURA_NIVEL_JUSANTE_GRADE_COMPORTA_1":                                                     [3, 1],
        "FALHA_LEITURA_NIVEL_JUSANTE_COMPORTA_1":                                                           [3, 2],
        "FALHA_LEITURA_NIVEL_JUSANTE_GRADE_COMPORTA_2":                                                     [3, 3],
        "FALHA_LEITURA_NIVEL_JUSANTE_COMPORTA_2":                                                           [3, 4],

        ## UNIDADE_HIDRÁULICA
        "UNIDADE_HIDRAULICA_OPERANDO":                                                                      [5, 0],
        "UNIDADE_HIDRAULICA_DISPONIVEL":                                                                    [5, 1],
        "UNIDADE_HIDRAULICA_FALHA_LIGAR_BOMBA":                                                             [5, 2],
        "UNIDADE_HIDRAULICA_FALHA_DESLIGAR_BOMBA":                                                          [5, 3],

        ## COMPORTA_1_PERMISSIVOS
        "COMPORTA_1_PERMISSIVO_00_SEM_BLOQUEIO_ATIVO":                                                      [7, 0],
        "COMPORTA_1_PERMISSIVO_01_COM_TENSAO_CA":                                                           [7, 1],
        "COMPORTA_1_PERMISSIVO_02_COM_NIVEL_OLEO_NORMAL_UNIDADE_HIDRAULICA":                                [7, 2],
        "COMPORTA_1_PERMISSIVO_03_UNIDADE_HIDRAULICA_DISPONIVEL":                                           [7, 3],
        "COMPORTA_1_PERMISSIVO_04_FECHAMENTO_FINALIZADO":                                                   [7, 4],

        "COMPORTA_1_PERMISSIVOS_OK":                                                                        [6, 15],

        ## COMPORTA_1_BLOQUEIOS
        "COMPORTA_1_BLOQUEIO_00_SELETORA_EM_MANUTENCAO":                                                    [9, 0],
        "COMPORTA_1_BLOQUEIO_01_SEM_PERMISSIVO_ABERTURA_PELO_CLP_DA_UG":                                    [9, 1],
        "COMPORTA_1_BLOQUEIO_02_BOTAO_EMERGENCIA_DO_QUADRO_ACIONADO":                                       [9, 2],
        "COMPORTA_1_BLOQUEIO_03_FALHA_ABERTURA_CRACKING":                                                   [9, 3],
        "COMPORTA_1_BLOQUEIO_04_FALHA_EQUALIZAR_PRESSAO":                                                   [9, 4],
        "COMPORTA_1_BLOQUEIO_05_FALHA_ABERTURA_COMPORTA":                                                   [9, 5],
        "COMPORTA_1_BLOQUEIO_06_FALHA_REPOSICAO_COMPORTA":                                                  [9, 6],
        "COMPORTA_1_BLOQUEIO_07_FALHA_FECHAMENTO_COMPORTA":                                                 [9, 7],
        "COMPORTA_1_BLOQUEIO_08_DISCREPANCIA_SINAIS_COMPORTA":                                              [9, 8],
        "COMPORTA_1_BLOQUEIO_09_COMANDO_FECHAMENTO_COMPORTA":                                               [9, 9],
        "COMPORTA_1_BLOQUEIO_10_FALHA_COMUNICACAO_COM_CLP_DA_UNIDADE_GERADORA":                             [9, 10],

        "COMPORTA_1_BLOQUEIO":                                                                              [8, 15],

        ## COMPORTA_1_STATUS
        "COMPORTA_1_OPERANDO":                                                                              [11, 0],
        "COMPORTA_1_REPONDO_COMPORTA":                                                                      [11, 1],
        "COMPORTA_1_ABRINDO_COMPORTA":                                                                      [11, 2],
        "COMPORTA_1_AGUARDANDO_COMANDO_ABERTURA":                                                           [11, 3],
        "COMPORTA_1_PRESSAO_EQUALIZADA":                                                                    [11, 4],
        "COMPORTA_1_EQUALIZANDO_PRESSAO":                                                                   [11, 5],
        "COMPORTA_1_ABRINDO_CRACKING":                                                                      [11, 6],
        "COMPORTA_1_FECHANDO_COMPORTA":                                                                     [11, 7],
        "COMPORTA_1_FECHAMENTO_FINALIZADO":                                                                 [11, 8],
        "COMPORTA_1_FALHA_COMUNICACAO_CLP_TA_CLP_UG":                                                       [11, 9],
        "COMPORTA_1_ALARME_DIFERENCIAL_DE_GRADE":                                                           [11, 10],

        ## COMPORTA_2_PERMISSIVOS
        "COMPORTA_2_PERMISSIVO_00_SEM_BLOQUEIO_ATIVO":                                                      [13, 0],
        "COMPORTA_2_PERMISSIVO_01_COM_TENSAO_CA":                                                           [13, 1],
        "COMPORTA_2_PERMISSIVO_02_COM_NIVEL_OLEO_NORMAL_UNIDADE_HIDRAULICA":                                [13, 2],
        "COMPORTA_2_PERMISSIVO_03_UNIDADE_HIDRAULICA_DISPONIVEL":                                           [13, 3],
        "COMPORTA_2_PERMISSIVO_04_FECHAMENTO_FINALIZADO":                                                   [13, 4],

        "COMPORTA_2_PERMISSIVOS_OK":                                                                        [12, 15],

        ## COMPORTA_2_BLOQUEIOS
        "COMPORTA_2_BLOQUEIO_00_SELETORA_EM_MANUTENCAO":                                                    [15, 0],
        "COMPORTA_2_BLOQUEIO_01_SEM_PERMISSIVO_ABERTURA_PELO_CLP_DA_UG":                                    [15, 1],
        "COMPORTA_2_BLOQUEIO_02_BOTAO_EMERGENCIA_DO_QUADRO_ACIONADO":                                       [15, 2],
        "COMPORTA_2_BLOQUEIO_03_FALHA_ABERTURA_CRACKING":                                                   [15, 3],
        "COMPORTA_2_BLOQUEIO_04_FALHA_EQUALIZAR_PRESSAO":                                                   [15, 4],
        "COMPORTA_2_BLOQUEIO_05_FALHA_ABERTURA_COMPORTA":                                                   [15, 5],
        "COMPORTA_2_BLOQUEIO_06_FALHA_REPOSICAO_COMPORTA":                                                  [15, 6],
        "COMPORTA_2_BLOQUEIO_07_FALHA_FECHAMENTO_COMPORTA":                                                 [15, 7],
        "COMPORTA_2_BLOQUEIO_08_DISCREPANCIA_SINAIS_COMPORTA":                                              [15, 8],
        "COMPORTA_2_BLOQUEIO_09_COMANDO_FECHAMENTO_COMPORTA":                                               [15, 9],
        "COMPORTA_2_BLOQUEIO_10_FALHA_COMUNICACAO_COM_CLP_DA_UNIDADE_GERADORA":                             [15, 10],

        "COMPORTA_2_BLOQUEIO":                                                                              [14, 15],

        ## COMPORTA_2_STATUS
        "COMPORTA_2_OPERANDO":                                                                              [17, 0],
        "COMPORTA_2_REPONDO_COMPORTA":                                                                      [17, 1],
        "COMPORTA_2_ABRINDO_COMPORTA":                                                                      [17, 2],
        "COMPORTA_2_AGUARDANDO_COMANDO_ABERTURA":                                                           [17, 3],
        "COMPORTA_2_PRESSAO_EQUALIZADA":                                                                    [17, 4],
        "COMPORTA_2_EQUALIZANDO_PRESSAO":                                                                   [17, 5],
        "COMPORTA_2_ABRINDO_CRACKING":                                                                      [17, 6],
        "COMPORTA_2_FECHANDO_COMPORTA":                                                                     [17, 7],
        "COMPORTA_2_FECHAMENTO_FINALIZADO":                                                                 [17, 8],
        "COMPORTA_2_FALHA_COMUNICACAO_CLP_TA_CLP_UG":                                                       [17, 9],
        "COMPORTA_2_ALARME_DIFERENCIAL_DE_GRADE":                                                           [17, 10],

        ## BORBOLETA_PERMISSIVOS
        "BORBOLETA_PERMISSIVO_00_SEM_BLOQUEIO_ATIVO":                                                       [19, 0],
        "BORBOLETA_PERMISSIVO_01_COM_TENSAO_CA":                                                            [19, 1],
        "BORBOLETA_PERMISSIVO_02_COM_NIVEL_OLEO_NORMAL_UNIDADE_HIDRAULICA":                                 [19, 2],
        "BORBOLETA_PERMISSIVO_03_UNIDADE_HIDRAULICA_DISPONIVEL":                                            [19, 3],
        "BORBOLETA_PERMISSIVO_04_ABERTURA_BORBOLETA_FINALIZADA":                                            [19, 4],

        "BORBOLETA_PERMISSIVOS_OK":                                                                         [18, 15],

        ## BORBOLETA_BLOQUEIOS
        "BORBOLETA_BLOQUEIO_00_BOTAO_EMERGENCIA_DO_QUADRO_ACIONADO":                                        [21, 0],
        "BORBOLETA_BLOQUEIO_01_FALHA_FECHAMENTO_BORBOLETA":                                                 [21, 1],
        "BORBOLETA_BLOQUEIO_02_FALHA_REPOSICAO_BORBOLETA":                                                  [21, 2],
        "BORBOLETA_BLOQUEIO_03_FALHA_ABERTURA_BORBOLETA":                                                   [21, 3],

        "BORBOLETA_BLOQUEIO":                                                                               [20, 15],

        ## BORBOLETA_STATUS
        "BORBOLETA_FECHANDO":                                                                               [22, 0],
        "BORBOLETA_REPONDO":                                                                                [22, 1],
        "BORBOLETA_ABRINDO":                                                                                [22, 2],
        "BORBOLETA_ABERTURA_FINALIZADA":                                                                    [22, 3],
        "BORBOLETA_EM_MANUTENCAO":                                                                          [22, 4],

        ## LIMPA_GRADES_PERMISSIVOS
        "LIMPA_GRADES_PERMISSIVO_00_SEM_FALHA_ATUADA":                                                      [25, 0],
        "LIMPA_GRADES_PERMISSIVO_01_UNIDADE_HIDRAULICA_DISPONIVEL":                                         [25, 1],
        "LIMPA_GRADES_PERMISSIVO_02_SELETORA_EM_AUTOMATICO":                                                [25, 2],
        "LIMPA_GRADES_PERMISSIVO_03_ESTADO_DO_LIMPA_GRADES_EM_POSICAO_INICIAL":                             [25, 3],

        "LIMPA_GRADES_PERMISSIVOS_OK":                                                                      [24, 15],

        ## LIMPA_GRADES_FALHAS
        "LIMPA_GRADES_FALHA_00_BOTAO_EMERGENCIA_DO_QUADRO_ATUADA":                                          [27, 0],
        "LIMPA_GRADES_FALHA_01_FALHA_AVANCAR_PORTICO":                                                      [27, 1],
        "LIMPA_GRADES_FALHA_02_FALHA_DESCER_RASTELO":                                                       [27, 2],
        "LIMPA_GRADES_FALHA_03_FALHA_SUBIR_RASTELO":                                                        [27, 3],
        "LIMPA_GRADES_FALHA_04_FALHA_RETORNAR_POSICAO_INICIAL":                                             [27, 4],

        "LIMPA_GRADES_FALHA_ATUADA":                                                                        [26, 15],

        ## LIMPA_GRADES_STATUS
        "LIMPA_GRADES_OPERACAO_MANUAL":                                                                     [29, 0],
        "LIMPA_GRADES_AFASTANDO_RASTELO":                                                                   [29, 1],
        "LIMPA_GRADES_DESCENDO_RASTELO":                                                                    [29, 2],
        "LIMPA_GRADES_APROXIMANDO_RASTELO":                                                                 [29, 3],
        "LIMPA_GRADES_SUBINDO_RASTELO":                                                                     [29, 4],
        "LIMPA_GRADES_AVANCANDO_PORTICO":                                                                   [29, 5],
        "LIMPA_GRADES_RETORNANDO_PORTICO":                                                                  [29, 6],
        "LIMPA_GRADES_PRIMEIRO_CICLO":                                                                      [29, 7],
        "LIMPA_GRADES_SEGUNDO_CICLO":                                                                       [29, 8],
        "LIMPA_GRADES_TERCEIRO_CICLO":                                                                      [29, 9],
        "LIMPA_GRADES_QUARTO_CICLO":                                                                        [29, 10],
        "LIMPA_GRADES_LIMPEZA_DIFERENCIAL_GRADE_HABILITADA":                                                [29, 11],

        "LIMPA_GRADES_ESTEIRA_LIGADAS":                                                                     [28, 14],
        "LIMPA_GRADES_MOTORES_PORTICO_LIGADOS":                                                             [28, 15],

        ## LEITURAS_ANALÓGICAS
        "NIVEL_MONTANTE":                                                                                   30,
        "NIVEL_JUSANTE_GRADE_COMPORTA_2":                                                                   32,
        "NIVEL_JUSANTE_GRADE_COMPORTA_1":                                                                   34,
        "NIVEL_JUSANTE_COMPORTA_1":                                                                         36,
        "NIVEL_JUSANTE_COMPORTA_2":                                                                         38,
        "ENTRADA_ANALOGICA_RESERVA_1":                                                                      40,
        "ENTRADA_ANALOGICA_RESERVA_2":                                                                      42,
        "ENTRADA_ANALOGICA_RESERVA_3":                                                                      44,
        "DIFERENCIAL_GRADE_COMPORTA_1":                                                                     46,
        "DIFERENCIAL_GRADE_COMPORTA_2":                                                                     48,


        ### COMANDOS
        ## COMPORTA_1
        "COMPORTA_1_COMANDO_REARME_FALHAS":                                                                 [51, 0],
        "COMPORTA_1_COMANDO_ABERTURA_CRACKING":                                                             [51, 1],
        "COMPORTA_1_COMANDO_ABERTURA_TOTAL":                                                                [51, 2],
        "COMPORTA_1_COMANDO_FECHAMENTO":                                                                    [51, 3],

        ## COMPORTA_2
        "COMPORTA_2_COMANDO_REARME_FALHAS":                                                                 [53, 0],
        "COMPORTA_2_COMANDO_ABERTURA_CRACKING":                                                             [53, 1],
        "COMPORTA_2_COMANDO_ABERTURA_TOTAL":                                                                [53, 2],
        "COMPORTA_2_COMANDO_FECHAMENTO":                                                                    [53, 3],

        ## BORBOLETA
        "BORBOLETA_COMANDO_RESET_FALHAS":                                                                   [55, 0],
        "BORBOLETA_COMANDO_SELECIONA_MANUTENCAO":                                                           [55, 1],
        "BORBOLETA_COMANDO_SELECIONA_OPERACAO_AUTOMATICA":                                                  [55, 2],
        "BORBOLETA_COMANDO_FECHA_BORBOLETA_EM_MANUTENCAO":                                                  [55, 3],
        "BORBOLETA_COMANDO_ABRE_BORBOLETA_EM_MANUTENCAO":                                                   [55, 4],

        ## LIMPA_GRADES
        "LIMPA_GRADES_RESET_FALHAS":                                                                        [57, 0],
        "LIMPA_GRADES_RETORNA_POSICAO_INICIAL":                                                             [57, 1],
        "LIMPA_GRADES_INICIA_CICLO_LIMPEZA":                                                                [57, 2],
        "LIMPA_GRADES_PULA_CICLO":                                                                          [57, 3],
        "LIMPA_GRADES_HABILITA_LIMPEZA_DIFERENCIAL_GRADE":                                                  [57, 4],
        "LIMPA_GRADES_DESABILITA_LIMPEZA_DIFRENCIAL_GRADE":                                                 [57, 5],
    },

    "UG1": {
        ### STATUS
        ## ENTRADAS_DIGITAIS_1
        "UHRV_BOMBA_1_FALHA":                                                                               [1, 0],
        "UHRV_BOMBA_1_LIGADA":                                                                              [1, 1],
        "UHRV_BOMBA_2_FALHA":                                                                               [1, 2],
        "UHRV_BOMBA_2_LIGADA":                                                                              [1, 3],
        "UHL_BOMBA_1_FALHA":                                                                                [1, 4],
        "UHL_BOMBA_1_LIGADA":                                                                               [1, 5],
        "UHL_BOMBA_2_FALHA":                                                                                [1, 6],
        "UHL_BOMBA_2_LIGADA":                                                                               [1, 7],
        "UG_MOLA_CARREGADA_DISJUNTOR_DE_MAQUINA":                                                           [1, 8],
        "UG_DISJUNTOR_MAQUINA_52G_FECHADO":                                                                 [1, 9],
        "UG_CPG_DISJUNTOR_TPS_MULTIMEDIDOR_E_REGULADORES_FECHADO":                                          [1, 10],
        "UG_CPG_DISJUNTOR_TPS_RELE_DE_PROTECAO_FECHADO":                                                    [1, 11],
        "UG_CPG_PORTA_FRONTAL_FECHADA":                                                                     [1, 12],
        "UG_CPG_PORTA_TRASEIRA_FECHADA":                                                                    [1, 13],
        "UHL_NIVEL_OLEO_MUITO_BAIXO":                                                                       [1, 14], # HIGH
        "UHL_NIVEL_OLEO_MUITO_ALTO":                                                                        [1, 15], # HIGH

        "UG_ENTRADA_DIGITAL_RESERVA_2":                                                                     [0, 0],
        "UHL_PRESSAO_LINHA_OLEO":                                                                           [0, 1],
        "UG_ENTRADA_DIGITAL_RESERVA_4":                                                                     [0, 2],
        "UG_ENTRADA_DIGITAL_RESERVA_5":                                                                     [0, 3],
        "UG_ENTRADA_DIGITAL_RESERVA_6":                                                                     [0, 4],
        "UHL_FILTRO_OLEO_SUJO":                                                                             [0, 5], # HIGH
        "UHRV_NIVEL_OLEO_MUITO_BAIXO":                                                                      [0, 6], # HIGH
        "UHRV_FREIO_PRESSURIZADO":                                                                          [0, 7],
        "UHRV_FILTRO_OLEO_SUJO":                                                                            [0, 8], # HIGH
        "UG_ENTRADA_DIGITAL_RESERVA_3":                                                                     [0, 9],
        "UG_ENTRADA_DIGITAL_RESERVA_1":                                                                     [0, 10],
        "UG_ENTRADA_DIGITAL_RESERVA_7":                                                                     [0, 11],
        "UG_RESISTENCIA_AQUECIMENTO_GERADOR_FALHA":                                                         [0, 12],
        "UG_RESISTENCIA_AQUECIMENTO_GERADOR_LIGADA":                                                        [0, 13],
        "RT_CONTATOR_CAMPO_FECHADO":                                                                        [0, 14],
        "UG_RELE_PROTECAO_MAQUINA":                                                                         [0, 15],

        ## ENTRADAS_DIGITAIS_2
        "UG_RELE_PROTECAO_MAQUINA_BF":                                                                      [3, 0],
        "UG_RELE_PROTECAO_MAQUINA_WATCHDOG_NORMAL":                                                         [3, 1],
        "UG_RELE_PROTECAO_TRANSFERENCIA_DE_DISPARO":                                                        [3, 2],
        "RV_BOTAO_AUMENTA_REFERENCIA_CONTROLE":                                                             [3, 3],
        "RV_BOTAO_DIMINUI_REFERENCIA_CONTROLE":                                                             [3, 4],
        "RT_BOTAO_AUMENTA_REFERENCIA_CONTROLE":                                                             [3, 5],
        "RT_BOTAO_DIMINUI_REFERENCIA_CONTROLE":                                                             [3, 6],
        "UG_SINCRONIZADOR_ESTADO_SINCRONIZADO":                                                             [3, 7],
        "UG_BOTAO_PARA_UNIDADE_GERADORA":                                                                   [3, 8],
        "UG_BOTAO_PARTE_UNIDADE_GERADORA":                                                                  [3, 9],
        "UG_BOTAO_REARME_FALHAS_UNIDADE_GERADORA":                                                          [3, 10],
        "UG_BOTAO_EMERGENCIA_DA_UNIDADE_GERADORA":                                                          [3, 11], # HIGH
        "UG_SUPERVISAO_BOBINA_DISJUNTOR_DE_MAQUINA":                                                        [3, 12],
        "UG_SUPERVISAO_BOBINA_RELE_DE_BLOQUEIO":                                                            [3, 13],

        "UG_RELE_DE_BLOQUEIO_86EH_ATUADO":                                                                  [2, 12], # HIGH
        "UG_SUBTENSAO_TENSAO_125VCC":                                                                       [2, 13], # HIGH
        "UG_SUBTENSAO_TENSAO_24VCC":                                                                        [2, 14], # HIGH
        "UG_DISJUNTORES_125VCC_ABERTOS":                                                                    [2, 15], # HIGH

        ## ENTRADAS_DIGITAIS_3
        "UG_DISJUNTORES_24VCC_ABERTOS":                                                                     [5, 0], # HIGH
        "UG_CLP_GERAL_SINAL_DE_BLOQUEIO_EXTERNO":                                                           [5, 1], # HIGH
        "UG_CLP_GERAL_SINAL_DE_SISTEMA_DE_AGUA_OK":                                                         [5, 2],
        "UG_CLP_GERAL_SINAL_RESERVA":                                                                       [5, 3],
        "ENTRADA_DIGITAL_RESERVA_3":                                                                        [5, 4],
        "UG_ESCOVAS_GASTAS_POLO_POSITIVO":                                                                  [5, 5],
        "UG_ESCOVAS_GASTAS_POLO_NEGATIVO":                                                                  [5, 6],
        "ENTRADA_DIGITAL_RESERVA_5":                                                                        [5, 7],
        "UG_DISPARO_MECANICO_DESATUADO":                                                                    [5, 8],
        "UG_DISPARO_MECANICO_ATUADO":                                                                       [5, 9],

        ## ALARMES_ANALÓGICOS
        "ALARME_TEMPERATURA_ALTA_PONTE_RETIFICADORA_FASE_A":                                                [7, 0],
        "ALARME_TEMPERATURA_ALTA_PONTE_RETIFICADORA_FASE_B":                                                [7, 1],
        "ALARME_TEMPERATURA_ALTA_PONTE_RETIFICADORA_FASE_C":                                                [7, 2],
        "ALARME_TEMPERATURA_ALTA_ENTRADA_RESERVA_3":                                                        [7, 3],
        "ALARME_TEMPERATURA_ALTA_TRAFO_EXCITACAO":                                                          [7, 4],
        "ALARME_TEMPERATURA_ALTA_MANCAL_GUIA":                                                              [7, 5],
        "ALARME_TEMPERATURA_ALTA_OLEO_DA_UHRV":                                                             [7, 6],
        "ALARME_TEMPERATURA_ALTA_OLEO_DA_UHL":                                                              [7, 7],
        "ALARME_TEMPERATURA_ALTA_CASQUILHO_MANCAL_COMBINADO":                                               [7, 8],
        "ALARME_TEMPERATURA_ALTA_CONTRA_ESCORA_MANCAL_COMBINADO":                                           [7, 9],
        "ALARME_TEMPERATURA_ALTA_PATINS_MANCAL_COMBINADO_MEDICAO_1":                                        [7, 10],
        "ALARME_TEMPERATURA_ALTA_PATINS_MANCAL_COMBINADO_MEDICAO_2":                                        [7, 11],
        "ALARME_TEMPERATURA_ALTA_MANCAL_GUIA_INTERNO_MEDICAO_1":                                            [7, 12],
        "ALARME_TEMPERATURA_ALTA_MANCAL_GUIA_INTERNO_MEDICAO_2":                                            [7, 13],
        "ALARME_TEMPERATURA_ALTA_NUCLEO_ESTATORICO":                                                        [7, 14],
        "ALARME_TEMPERATURA_ALTA_GERADOR_FASE_A":                                                           [7, 15],

        "ALARME_TEMPERATURA_ALTA_GERADOR_FASE_B":                                                           [6, 0],
        "ALARME_TEMPERATURA_ALTA_GERADOR_FASE_C":                                                           [6, 1],
        "ALARME_TEMPERATURA_ALTA_ENTRADA_RESERVA_2":                                                        [6, 2],
        "ALARME_TEMPERATURA_ALTA_ENTRADA_RESERVA":                                                          [6, 3],
        "ALARME_PRESSAO_ENTRADA_TURBINA":                                                                   [6, 4],
        "ALARME_PRESSAO_REGULAGEM_1_TURBINA":                                                               [6, 5],
        "ALARME_PRESSAO_SAIDA_RODA":                                                                        [6, 6],
        "ALARME_PRESSAO_SAIDA_SUCCAO":                                                                      [6, 7],
        "ALARME_VIBRACAO_EIXO_X_MANCAL_COMBINADO":                                                          [6, 8],
        "ALARME_VIBRACAO_EIXO_Y_MANCAL_COMBINADO":                                                          [6, 9],
        "ALARME_VIBRACAO_EIXO_Z_MANCAL_COMBINADO":                                                          [6, 10],
        "ALARME_PRESSAO_ACUMULADOR_UHRV":                                                                   [6, 11],
        "ALARME_VIBRACAO_DETECCAO_HORIZONTAL_":                                                             [6, 12],
        "ALARME_VIBRACAO_DETECCAO_VERTICAL":                                                                [6, 13],
        "ALARME_PRESSAO_REGULAGEM_2_TURBINA":                                                               [6, 14],
        "ALARME_PRESSAO_DIFERENCIAL_REGULAGEM_TURBINA":                                                     [6, 15],

        ## FALHAS_ANALÓGICAS
        "FALHA_LEITURA_PRESSAO_ENTRADA_TURBINA":                                                            [8, 4],
        "FALHA_LEITURA_PRESSAO_REGULAGEM_1_TURBINA":                                                        [8, 5],
        "FALHA_LEITURA_PRESSAO_SAIDA_RODA":                                                                 [8, 6],
        "FALHA_LEITURA_PRESSAO_SAIDA_SUCCAO":                                                               [8, 7],
        "FALHA_LEITURA_VIBRACAO_EIXO_X_MANCAL_COMBINADO":                                                   [8, 8],
        "FALHA_LEITURA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO":                                                   [8, 9],
        "FALHA_LEITURA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO":                                                   [8, 10],
        "FALHA_LEITURA_VIBRACAO_DETECCAO_HORIZONTAL_":                                                      [8, 12],
        "FALHA_LEITURA_VIBRACAO_DETECCAO_VERTICAL":                                                         [8, 13],
        "FALHA_LEITURA_PRESSAO_REGULAGEM_2_TURBINA":                                                        [8, 14],
        "FALHA_LEITURA_PRESSAO_DIFERENCIAL_REGULAGEM_TURBINA":                                              [8, 15],

        ## UG
        "ESTADO_DE_MAQUINA_PARADA_FINALIZADA":                                                              [11, 0],
        "ESTADO_DE_MAQUINA_PARTINDO":                                                                       [11, 1],
        "ESTADO_DE_MAQUINA_GIRANDO_DESEXITADA":                                                             [11, 2],
        "ESTADO_DE_MAQUINA_PRONTA_PARA_SINCRONIZAR":                                                        [11, 3],
        "ESTADO_DE_MAQUINA_SINCRONIZADA":                                                                   [11, 4],
        "ESTADO_DE_MAQUINA_PARANDO_PASSO_A_PASSO":                                                          [11, 5],
        "ESTADO_DE_MAQUINA_PARANDO_SEM_REJEICAO":                                                           [11, 6],
        "ESTADO_DE_MAQUINA_PARANDO_EM_EMERGENCIA":                                                          [11, 7],
        "CONTROLE_DE_POTENCIA_POR_NIVEL_HABILITADO":                                                        [11, 8],
        "CONTROLE_DE_POTENCIA_POR_NIVEL_ESCALONADO_HABILITADO":                                             [11, 9],
        "PARADA_DA_UNIDADE_POR_NIVEL_HABILITADO":                                                           [11, 10],
        "FALHA_HABILITAR_SISTEMA_DE_AGUA":                                                                  [11, 11],
        "ESTADO_DE_MAQUINA_PARANDO_PARCIAL":                                                                [11, 12],
        "FALHA_COMUNICACAO_COM_CLP_DA_TOMADA_DAGUA":                                                        [11, 13],
        "COMPORTA_OPERANDO":                                                                                [11, 14],

        ## PRE_CONDICOES_PARTIDA
        "PRE_CONDICAO_00_SEM_BLOQUEIOS":                                                                    [13, 0],
        "PRE_CONDICAO_01_BOMBA_1_OU_2_DA_UHRV_DISPONÍVEL":                                                  [13, 1],
        "PRE_CONDICAO_02_COM_TENSAO_SERVICOS_AUXILIARES":                                                   [13, 2],
        "PRE_CONDICAO_03_PARADA_FINALIZADA":                                                                [13, 3],
        "PRE_CONDICAO_04_UHRV_EM_AUTOMATICO":                                                               [13, 4],
        "PRE_CONDICAO_05_COMPORTA_OPERANDO":                                                                [13, 5],

        "PRE_CONDICOES_PARTIDA_OK":                                                                         [12, 15],

        ## PERMISSIVOS_UHL
        "UHL_PERMISSIVO_00_BOMBA_1_OU_BOMBA_2_UHL_DISPONIVEL":                                              [15, 0],
        "UHL_PERMISSIVO_01_SEM_FALHA_PRESSOSTATO_LINHA_OLEO":                                               [15, 1],
        "UHL_PERMISSIVO_02_UNIDADE_EM_AUTOMATICO":                                                          [15, 2],

        "UHL_PERMISSIVOS_OK":                                                                               [14, 15],

        ## PERMISSIVOS_SISTEMA_ÁGUA
        "AGUA_SELO_PERMISSIVOS_OK":                                                                         [16, 15],

        ## PERMISSIVOS_RV
        "RV_PERMISSIVO_00_SEM_ALARME_TEMPERATURA_OLEO_UHL":                                                 [19, 0],
        "RV_PERMISSIVO_01_SEM_ALARME_TEMPERATURA_OLEO_UHRV":                                                [19, 1],
        "RV_PERMISSIVO_02_SEM_ALARME_TEMPERATURA_MANCAL_COMBINADO":                                         [19, 2],
        "RV_PERMISSIVO_03_SEM_ALARME_TEMPERATURA_MANCAL_CONTRA_ESCORA_COMBINADO":                           [19, 3],
        "RV_PERMISSIVO_04_SEM_ALARME_TEMPERATURA_1_PATINS_MANCAL_COMBINADO":                                [19, 4],
        "RV_PERMISSIVO_05_SEM_ALARME_TEMPERATURA_2_PATINS_MANCAL_COMBINADO":                                [19, 5],
        "RV_PERMISSIVO_06_SEM_ALARME_TEMPERATURA_1_MACAL_GUIA_INTERNO":                                     [19, 6],
        "RV_PERMISSIVO_07_SEM_ALARME_TEMPERATURA_2_MACAL_GUIA_INTERNO":                                     [19, 7],

        "RV_PERMISSIVOS_OK":                                                                                [18, 15],

        ## PERMISSIVOS_RT
        "RT_PERMISSIVO_00_SEM_ALARME_TEMPERATURAS_PONTE_RETIFICADORA_FASE_A":                               [21, 0],
        "RT_PERMISSIVO_01_SEM_ALARME_TEMPERATURAS_PONTE_RETIFICADORA_FASE_B":                               [21, 1],
        "RT_PERMISSIVO_02_SEM_ALARME_TEMPERATURAS_PONTE_RETIFICADORA_FASE_C":                               [21, 2],
        "RT_PERMISSIVO_03_SEM_ALARME_TEMPERATURA_GERADOR_FASE_A":                                           [21, 3],
        "RT_PERMISSIVO_04_SEM_ALARME_TEMPERATURA_GERADOR_FASE_B":                                           [21, 4],
        "RT_PERMISSIVO_05_SEM_ALARME_TEMPERATURA_GERADOR_FASE_C":                                           [21, 5],
        "RT_PERMISSIVO_06_SEM_ALARME_TEMPERATURA_GERADOR_NUCLEO_ESTATORICO":                                [21, 6],
        "RT_PERMISSIVO_07_SEM_ALARME_TEMPERATURA_TRAFO_EXCITACAO":                                          [21, 7],

        "RT_PERMISSIVOS_OK":                                                                                [20, 15],

        ## PERMISSIVOS_SINCRONISMO
        "SINCRONISMO_PERMISSIVO_00_DISJUNTOR_DE_LINHA_FECHADO":                                             [23, 0],

        "SINCRONISMO_PERMISSIVOS_OK":                                                                       [22, 15],

        ## BLOQUEIO_86M
        "86M_BLOQUEIO_00_NIVEL_MUITO_ALTO_OLEO_UHL":                                                        [25, 0],
        "86M_BLOQUEIO_01_NIVEL_MUITO_BAIXO_OLEO_UHL":                                                       [25, 1],
        "86M_BLOQUEIO_02_NIVEL_MUITO_BAIXO_OLEO_UHRV":                                                      [25, 2],
        "86M_BLOQUEIO_03_FALTA_PRESSAO_SISTEMA_DE_AGUA":                                                    [25, 3],
        "86M_BLOQUEIO_04_TEMPERATURA_MUITO_ALTA_OLEO_UHL":                                                  [25, 4],
        "86M_BLOQUEIO_05_TEMPERATURA_MUITO_ALTA_OLEO_UHRV":                                                 [25, 5],
        "86M_BLOQUEIO_06_FALHA_LEITURA_TEMPERATURA_OLEO_UHL":                                               [25, 6],
        "86M_BLOQUEIO_07_FALHA_LEITURA_TEMPERATURA_OLEO_UHRV":                                              [25, 7],
        "86M_BLOQUEIO_08_FALHA_LEITURA_TEMPERATURA_CASQUILHO_MANCAL_COMBINADO":                             [25, 8],
        "86M_BLOQUEIO_09_FALHA_LEITURA_TEMPERATURA_CONTRA_ESCORA_MANCAL_COMBINADO":                         [25, 9],
        "86M_BLOQUEIO_10_FALHA_LEITURA_TEMPERATURA_1_PATINS_MANCAL_COMBINADO":                              [25, 10],
        "86M_BLOQUEIO_11_FALHA_LEITURA_TEMPERATURA_2_PATINS_MANCAL_COMBINADO":                              [25, 11],
        "86M_BLOQUEIO_12_FALHA_LEITURA_TEMPERATURA_1_MANCAL_GUIA_INTERNO":                                  [25, 12],
        "86M_BLOQUEIO_13_FALHA_LEITURA_TEMPERATURA_2_MANCAL_GUIA_INTERNO":                                  [25, 13],
        "86M_BLOQUEIO_14_FALHA_LEITURA_TEMPERATURA_PONTE_FASE_A":                                           [25, 14],
        "86M_BLOQUEIO_15_FALHA_LEITURA_TEMPERATURA_PONTE_FASE_B":                                           [25, 15],

        "86M_BLOQUEIO_16_FALHA_LEITURA_TEMPERATURA_PONTE_FASE_C":                                           [24, 0],
        "86M_BLOQUEIO_17_FALHA_LEITURA_TEMPERATURA_GERADOR_FASE_A":                                         [24, 1],
        "86M_BLOQUEIO_18_FALHA_LEITURA_TEMPERATURA_GERADOR_FASE_B":                                         [24, 2],
        "86M_BLOQUEIO_19_FALHA_LEITURA_TEMPERATURA_GERADOR_FASE_C":                                         [24, 3],
        "86M_BLOQUEIO_20_FALHA_LEITURA_TEMPERATURA_GERADOR_NUCLEO_ESTATORICO":                              [24, 4],
        "86M_BLOQUEIO_21_FALHA_LEITURA_VIBRACAO_DETECCAO_HORIZONTAL":                                       [24, 5],
        "86M_BLOQUEIO_22_FALHA_LEITURA_VIBRACAO_DETECCAO_VERTICAL":                                         [24, 6],
        "86M_BLOQUEIO_23_FALHA_LEITURA_VIBRACAO_EIXO_X_MANCAL_COMBINADO":                                   [24, 7],
        "86M_BLOQUEIO_24_FALHA_LEITURA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO":                                   [24, 8],
        "86M_BLOQUEIO_25_FALHA_LEITURA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO":                                   [24, 9],
        "86M_BLOQUEIO_26_TRIP_VIBRACAO_DETECCAO_HORIZONTAL":                                                [24, 10],
        "86M_BLOQUEIO_27_TRIP_VIBRACAO_DETECCAO_VERTICAL":                                                  [24, 11],
        "86M_BLOQUEIO_28_TRIP_VIBRACAO_EIXO_X_MANCAL_COMBINADO":                                            [24, 12],
        "86M_BLOQUEIO_29_TRIP_VIBRACAO_EIXO_Y_MANCAL_COMBINADO":                                            [24, 13],
        "86M_BLOQUEIO_30_TRIP_VIBRACAO_EIXO_Z_MANCAL_COMBINADO":                                            [24, 14],
        "86M_BLOQUEIO":                                                                                     [24, 15],

        ## BLOQUEIO_86E
        "86E_BLOQUEIO_00_CUBICULO_PROTECAO_GERADOR_DISJUNTOR_TPS_MULTIMEDIDOR_E_REGULADORES_ABERTO":        [27, 0],
        "86E_BLOQUEIO_01_CUBICULO_PROTECAO_GERADOR_DISJUNTOR_TPS_RELE_DE_PROTECAO_DA_UNIDADE_ABERTO":       [27, 1],
        "86E_BLOQUEIO_02_CUBICULO_PROTECAO_GERADOR_PORTA_FRONTAL_ABERTA":                                   [27, 2],
        "86E_BLOQUEIO_03_CUBICULO_PROTECAO_GERADOR_PORTA_TRASEIRA_ABERTA":                                  [27, 3],
        "86E_BLOQUEIO_04_RELE_DE_PROTECAO_DA_UNIDADE":                                                      [27, 4],
        "86E_BLOQUEIO_05_RELE_DE_PROTECAO_DA_UNIDADE_FALHA_WATCHDOG":                                       [27, 5],
        "86E_BLOQUEIO_06_RELE_DE_PROTECAO_DA_UNIDADE_BF":                                                   [27, 6],
        "86E_BLOQUEIO_07_SUBTENSAO_CIRCUITO_TENSAO_24VCC":                                                  [27, 7],
        "86E_BLOQUEIO_08_SUBTENSAO_CIRCUITO_TENSAO_125VCC":                                                 [27, 8],
        "86E_BLOQUEIO_09_DISJUNTORES_CIRCUITO_TENSAO_24VCC_ABERTOS":                                        [27, 9],
        "86E_BLOQUEIO_10_DISJUNTORES_CIRCUITO_TENSAO_125VCC_ABERTOS":                                       [27, 10],
        "86E_BLOQUEIO_11_PARADA_FALHA_ABERTURA_DISJUNTOR_DE_MAQUINA":                                       [27, 11],
        "86E_BLOQUEIO_12_PARADA_FALHA_DESABILITAR_REGULADOR_DE_TENSAO":                                     [27, 12],
        "86E_BLOQUEIO_13_PARADA_RELE_TRIP_REGULADOR_DE_TENSAO":                                             [27, 13],
        "86E_BLOQUEIO_14_RELE_DE_PROTECAO_DA_UNIDADE_TRANSFERENCIA_DE_DISPARO_RELE_LINHA_OU_TRAFO":         [27, 14],
        "86E_BLOQUEIO_15_RESERVA_2":                                                                        [27, 15],

        "86E_BLOQUEIO_16_TEMPERATURA_MUITO_ALTA_PONTE_RETIFICADOR_FASE_A":                                  [26, 0],
        "86E_BLOQUEIO_17_TEMPERATURA_MUITO_ALTA_PONTE_RETIFICADOR_FASE_B":                                  [26, 1],
        "86E_BLOQUEIO_18_TEMPERATURA_MUITO_ALTA_PONTE_RETIFICADOR_FASE_C":                                  [26, 2],
        "86E_BLOQUEIO_19_TEMPERATURA_MUITO_ALTA_GERADOR_FASE_A":                                            [26, 3],
        "86E_BLOQUEIO_20_TEMPERATURA_MUITO_ALTA_GERADOR_FASE_B":                                            [26, 4],
        "86E_BLOQUEIO_21_TEMPERATURA_MUITO_ALTA_GERADOR_FASE_C":                                            [26, 5],
        "86E_BLOQUEIO_22_TEMPERATURA_MUITO_ALTA_GERADOR_NUCLEO_ESTATORICO":                                 [26, 6],
        "86E_BLOQUEIO_23_TEMPERATURA_MUITO_ALTA_GERADOR_SAIDA_DE_AR":                                       [26, 7],
        "86E_BLOQUEIO_24_TEMPERATURA_MUITO_ALTA_TRAFO_ATERRAMENTO":                                         [26, 8],
        "86E_BLOQUEIO_25_TEMPERATURA_MUITO_ALTA_TRAFO_EXCITACAO":                                           [26, 9],
        "86E_BLOQUEIO_26_FALHA_LEITURA_TEMPERATURA_TRAFO_EXCITACAO":                                        [26, 10],
        "86E_BLOQUEIO":                                                                                     [26, 15],

        ## BLOQUEIO_86H
        "86H_BLOQUEIO_00_FALHA_BOMBAS_DE_LUBRIFICACAO":                                                     [29, 0],
        "86H_BLOQUEIO_01_FALTA_PRESSAO_OLEO_LINHA_LUBRIFICACAO":                                            [29, 1],
        "86H_BLOQUEIO_02_GIRO_INDEVIDO_DA_UNIDADE_GERADORA":                                                [29, 2],
        "86H_BLOQUEIO_03_RESERVA":                                                                          [29, 3],
        "86H_BLOQUEIO_04_RESERVA":                                                                          [29, 4],
        "86H_BLOQUEIO_05_PRESSAO_MUITO_BAIXA_ACUMULADOR_UHRV_MEDICAO_ANALOGICA":                            [29, 5],
        "86H_BLOQUEIO_06_BOTAO_EMERGENCIA":                                                                 [29, 6],
        "86H_BLOQUEIO_07_RELE_TRIP_REGULADOR_DE_VELOCIDADE":                                                [29, 7],
        "86H_BLOQUEIO_08_RESERVA":                                                                          [29, 8],
        "86H_BLOQUEIO_09_BLOQUEIO_EXTERNO_CLP_GERAL":                                                       [29, 9],
        "86H_BLOQUEIO_10_PARADA_FALHA_DESCARGA_POTENCIA":                                                   [29, 10],
        "86H_BLOQUEIO_11_PARADA_FALHA_DESABILITAR_REGULADOR_DE_VELOCIDADE":                                 [29, 11],
        "86H_BLOQUEIO_12_PARADA_FALHA_FECHAR_DISTRIBUIDOR":                                                 [29, 12],
        "86H_BLOQUEIO_13_PARADA_FALHA_PARAR_UNIDADE_GERADORA":                                              [29, 13],
        "86H_BLOQUEIO_14_BLOQUEIO_COMPORTA":                                                                [29, 14],
        "86H_BLOQUEIO_15_COMPORTA_NAO_OPERANDO":                                                            [29, 15],

        "86H_BLOQUEIO_16_FALHA_COMUNICACAO_CLP_TOMADA_DAGUA":                                               [28, 0],
        "86H_BLOQUEIO_17_FALHA_LEITURA_PRESSAO_ACUMULADOR_UHRV":                                            [28, 1],
        "86H_BLOQUEIO_18_TEMPERATURA_MUITO_ALTA_MANCAL_COMBINADO":                                          [28, 2],
        "86H_BLOQUEIO_19_TEMPERATURA_MUITO_ALTA_CONTRA_ESCORA_MANCAL_COMBINADO":                            [28, 3],
        "86H_BLOQUEIO_20_TEMPERATURA_MUITO_ALTA_PATINS_MANCAL_COMBINADO_LEITURA_1":                         [28, 4],
        "86H_BLOQUEIO_21_TEMPERATURA_MUITO_ALTA_PATINS_MANCAL_COMBINADO_LEITURA_2":                         [28, 5],
        "86H_BLOQUEIO_22_TEMPERATURA_MUITO_ALTA_MANCAL_GUIA_INTERNO_LEITURA_1":                             [28, 6],
        "86H_BLOQUEIO_23_TEMPERATURA_MUITO_ALTA_MANCAL_GUIA_INTERNO_LEITURA_2":                             [28, 7],
        "86H_BLOQUEIO_24_COMANDO_PARADA_DE_EMERGENCIA":                                                     [28, 8],
        "86H_BLOQUEIO_25_DISPARO_MECANICO_ATUADO":                                                          [28, 9],
        "86H_BLOQUEIO_26_MAXIMO_DIFERENCIAL_DE_GRADE":                                                      [28, 10],
        "86H_BLOQUEIO":                                                                                     [28, 15],

        ## PARTIDA_PARADA_PASSO_ATUAL
        "PARTIDA_PASSO_ATUAL_HABILITA_DESAPLICA_FREIO":                                                     [31, 0],
        "PARTIDA_PASSO_ATUAL_HABILITA_UNIDADE_LUBRIFICACAO_MANCAIS":                                        [31, 1],
        "PARTIDA_PASSO_ATUAL_HABILITA_SISTEMA_DE_AGUA":                                                     [31, 2],
        "PARTIDA_PASSO_ATUAL_HABILITA_REGULADOR_DE_VELOCIDADE":                                             [31, 3],
        "PARTIDA_PASSO_ATUAL_HABILITA_REGULADOR_DE_TENSAO":                                                 [31, 4],
        "PARTIDA_PASSO_ATUAL_HABILITA_SINCRONISMO":                                                         [31, 5],

        "PARADA_PASSO_ATUAL_DESCARGA_POTENCIA":                                                             [30, 0],
        "PARADA_PASSO_ATUAL_DESABILITA_REGULADOR_DE_TENSAO":                                                [30, 1],
        "PARADA_PASSO_ATUAL_DESABILITA_REGULADOR_DE_VELOCIDADE_E_APLICA_FREIO":                             [30, 2],
        "PARADA_PASSO_ATUAL_DESABILITA_SISTEMA_DE_AGUA":                                                    [30, 3],
        "PARADA_PASSO_ATUAL_DESABILITA_UNIDADE_LUBRIFICACAO_MANCAIS":                                       [30, 4],

        ## PARTIDA_PARADA_PASSO_CONCLUIDO
        "PARTIDA_CONCLUIDO_PASSO_HABILITA_DESAPLICA_FREIO":                                                 [33, 0],
        "PARTIDA_CONCLUIDO_PASSO_HABILITA_UNIDADE_LUBRIFICACAO":                                            [33, 1],
        "PARTIDA_CONCLUIDO_PASSO_HABILITA_SISTEMA_DE_AGUA":                                                 [33, 2],
        "PARTIDA_CONCLUIDO_PASSO_HABILITA_REGULADOR_DE_VELOCIDADE":                                         [33, 3],
        "PARTIDA_CONCLUIDO_PASSO_HABILITA_REGULADOR_DE_TENSAO":                                             [33, 4],
        "PARTIDA_CONCLUIDO_PASSO_HABILITA_SINCRONISMO":                                                     [33, 5],

        "PARADA_CONCLUIDO_PASSO_DESCARGA_POTENCIA_E_ABERTURA_DISJUNTOR":                                    [32, 0],
        "PARADA_CONCLUIDO_PASSO_DESABILITA_REGULADOR_TENSAO":                                               [32, 1],
        "PARADA_CONCLUIDO_PASSO_DESABILITA_REGULADOR_VELOCIDADE":                                           [32, 2],
        "PARADA_CONCLUIDO_PASSO_DESABILITA_SISTEMA_DE_AGUA":                                                [32, 3],
        "PARADA_CONCLUIDO_PASSO_DESABILITA_UNIDADE_LUBRIFICACAO":                                           [32, 4],

        ## PARTIDA_PARADA_PASSO_FALHA
        "PARTIDA_FALHA_PASSO_HABILITA_DESAPLICA_FREIO":                                                     [35, 0],
        "PARTIDA_FALHA_PASSO_HABILITA_UNIDADE_DE_LUBRIFICACAO":                                             [35, 1],
        "PARTIDA_FALHA_PASSO_HABILITA_SISTEMA_DE_AGUA":                                                     [35, 2],
        "PARTIDA_FALHA_PASSO_HABILITA_REGULADOR_DE_VELOCIDADE":                                             [35, 3],
        "PARTIDA_FALHA_PASSO_HABILITA_REGULADOR_DE_TENSAO":                                                 [35, 4],
        "PARTIDA_FALHA_PASSO_HABILITA_SINCRONISMO":                                                         [35, 5],

        "PARADA_FALHA_PASSO_DESCARGA_DE_POTENCIA_E_ABERTURA_DISJUNTOR_DE_MAQUINA":                          [34, 0],
        "PARADA_FALHA_PASSO_DESABILITAR_REGULADOR_DE_TENSAO":                                               [34, 1],
        "PARADA_FALHA_PASSO_DESABILITAR_REGULADOR_DE_VELOCIDADE":                                           [34, 2],
        "PARADA_FALHA_PASSO_DESABILITAR_SISTEMA_DE_AGUA":                                                   [34, 3],
        "PARADA_FALHA_PASSO_DESABILITAR_LUBRIFICACAO_DOS_MANCAIS":                                          [34, 4],

        ## UHRV
        "UHRV_UNIDADE_EM_MANUTENCAO":                                                                       [37, 0],
        "UHRV_BOMBA_1_PRINCIPAL":                                                                           [37, 1],
        "UHRV_BOMBA_2_PRINCIPAL":                                                                           [37, 2],
        "UHRV_BOMBA_1_DISPONIVEL":                                                                          [37, 3],
        "UHRV_BOMBA_2_DISPONIVEL":                                                                          [37, 4],
        "UHRV_FALHA_LIGAR_BOMBA_1":                                                                         [37, 5],
        "UHRV_FALHA_DESLIGAR_BOMBA_1":                                                                      [37, 6],
        "UHRV_FALHA_LIGAR_BOMBA_2":                                                                         [37, 7],
        "UHRV_FALHA_DESLIGAR_BOMBA_2":                                                                      [37, 8],
        "UHRV_FALHA_PRESSURIZAR_PELA_BOMBA_1":                                                              [37, 9],
        "UHRV_FALHA_PRESSURIZAR_PELA_BOMBA_2":                                                              [37, 10],
        "UHRV_APLICANDO_FREIO":                                                                             [37, 11],
        "UHRV_FALHA_PRESSURIZAR_FREIO":                                                                     [37, 12],
        "UHRV_FALHA_DESPRESSURIZAR_FREIO":                                                                  [37, 13],

        ## UHL
        "UHL_BOMBA_1_PRINCIPAL":                                                                            [39, 0],
        "UHL_BOMBA_2_PRINCIPAL":                                                                            [39, 1],
        "UHL_BOMBA_1_DISPONIVEL":                                                                           [39, 2],
        "UHL_BOMBA_2_DISPONIVEL":                                                                           [39, 3],
        "UHL_UNIDADE_EM_MANUTENCAO":                                                                        [39, 4],
        "UHL_FALHA_LIGAR_BOMBA_1":                                                                          [39, 5],
        "UHL_FALHA_DESLIGAR_BOMBA_1":                                                                       [39, 6],
        "UHL_FALHA_LIGAR_BOMBA_2":                                                                          [39, 7],
        "UHL_FALHA_DESLIGAR_BOMBA_2":                                                                       [39, 8],
        "UHL_FALHA_PRESSAO_OLEO_LINHA_PELA_BOMBA_1":                                                        [39, 9],
        "UHL_FALHA_PRESSAO_OLEO_LINHA_PELA_BOMBA_2":                                                        [39, 10],
        "UHL_FALHA_PRESSOSTATO_LINHA_DE_OLEO":                                                              [39, 11],

        ## SISTEMA_AGUA
        "SISTEMA_AGUA":                                                                                     40,

        ## AUTOMACAO_RTV
        "RV_FALHA_HABILITAR_RV":                                                                            [43, 0],
        "RV_FALHA_PARTIR_RV":                                                                               [43, 1],
        "RV_FALHA_DESABILITAR_RV":                                                                          [43, 2],
        "RV_FALHA_PARAR_MAQUINA":                                                                           [43, 3],
        "RV_FALHA_FECHAR_DISTRIBUIDOR":                                                                     [43, 4],

        "RT_FALHA_HABILITAR":                                                                               [42, 0],
        "RT_FALHA_PARTIR":                                                                                  [42, 1],
        "RT_FALHA_DESABILITAR":                                                                             [42, 2],

        ## LEITURAS_ANALÓGICAS
        "TEMP_PONTE_FASE_A":                                                                                44,
        "TEMP_GERADOR_FASE_A":                                                                              44,
        "TEMP_PONTE_FASE_B":                                                                                46,
        "TEMP_GERADOR_FASE_B":                                                                              46,
        "TEMP_PONTE_FASE_C":                                                                                48,
        "TEMP_GERADOR_FASE_C":                                                                              48,
        "TEMP_RESERVA":                                                                                     50,
        "TEMP_TRAFO_EXCITACAO":                                                                             52,
        "TEMP_MANCAL_GUIA":                                                                                 54,
        "TEMP_OLEO_UHRV":                                                                                   56,
        "TEMP_OLEO_UHL":                                                                                    58,
        "TEMP_CASQ_MANCAL_COMBINADO":                                                                       60,
        "TEMP_CONTRA_ESCORA_MANCAL_COMBINADO":                                                              62,
        "TEMP_1_PATINS_MANCAL_COMBINADO":                                                                   64,
        "TEMP_2_PATINS_MANCAL_COMBINADO":                                                                   66,
        "TEMP_1_MANCAL_GUIA_INTERNO":                                                                       68,
        "TEMP_2_MANCAL_GUIA_INTERNO":                                                                       70,
        "TEMP_GERADOR_NUCLEO_ESTATORICO":                                                                   72,
        "PRESSAO_ENTRADA_TURBINA":                                                                          84,
        "PRESSAO_REGULAGEM_1_TURBINA":                                                                      86,
        "PRESSAO_SAIDA_RODA":                                                                               88,
        "PRESSAO_SAIDA_SUCCAO":                                                                             90,
        "VIBRACAO_EIXO_X_MANCAL_COMBINADO":                                                                 92,
        "VIBRACAO_EIXO_Y_MANCAL_COMBINADO":                                                                 94,
        "VIBRACAO_EIXO_Z_MANCAL_COMBINADO":                                                                 96,
        "PRESSAO_ACUMULADOR_UHRV":                                                                          98,
        "VIBRACAO_DETECCAO_HORIZONTAL":                                                                     100,
        "VIBRACAO_DETECACAO_VERTICAL":                                                                      102,
        "PRESSAO_REGULAGEM_2_TURBINA":                                                                      104,
        "PRESSAO_DIFERENCIAL_REGULAGEM_TURBINA":                                                            106,

        ## HORÍMETROS
        "UG":                                                                                               108,
        "UHRV_B1":                                                                                          110,
        "UHRV_B2":                                                                                          112,
        "UHL_B1":                                                                                           114,
        "UHL_B2":                                                                                           116,

        ## MULTIMEDIDOR
        "VAB":                                                                                              118,
        "VBC":                                                                                              120,
        "VCA":                                                                                              122,
        "IA":                                                                                               124,
        "IB":                                                                                               126,
        "IC":                                                                                               128,
        "P":                                                                                                130,
        "Q":                                                                                                132,
        "S":                                                                                                134,
        "F":                                                                                                136,
        "FP":                                                                                               138,
        "EAP":                                                                                              138,
        "EAN":                                                                                              140,
        "ERP":                                                                                              142,
        "ERN":                                                                                              144,


        ### COMANDOS
        ## UG
        "UG_REARME_FALHA_PASSOS":                                                                           [1, 0],
        "UG_REARME_BLOQUEIO_86M":                                                                           [1, 1],
        "UG_REARME_BLOQUEIO_86E":                                                                           [1, 2],
        "UG_REARME_BLOQUEIO_86H":                                                                           [1, 3],
        "UG_COMANDO_PARADA_DE_EMERGENCIA":                                                                  [1, 4],
        "PARTIDA_UG_HABILITA_DESAPLICAR_FREIO":                                                             [1, 5],
        "PARTIDA_UG_HABILITA_UNIDADE_DE_LUBRIFICACAO_DOS_MANCAIS":                                          [1, 6],
        "PARTIDA_UG_HABILITA_SISTEMA_DE_AGUA":                                                              [1, 7],
        "PARTIDA_UG_HABILITA_REGULADOR_DE_VELOCIDADE":                                                      [1, 8],
        "PARTIDA_UG_HABILITA_REGULADOR_DE_TENSAO":                                                          [1, 9],
        "PARTIDA_UG_HABILITA_SINCRONISMO":                                                                  [1, 10],
        "PARADA_UG_HABILITA_DESCARGA_POTENCIA_E_ABERTURA_DISJUNTOR_MAQUINA":                                [1, 11],
        "PARADA_UG_DESABILITA_REGULADOR_DE_TENSAO":                                                         [1, 12],
        "PARADA_UG_DESABILITA_REGULADOR_DE_VELOCIDADE":                                                     [1, 13],
        "PARADA_UG_DESABILITA_SISTEMA_DE_AGUA":                                                             [1, 14],
        "PARADA_UG_DESABILITA_UNIDADES_DE_LUBRIFICACAO":                                                    [1, 15],

        "UG_HABILITA_CONTROLE_DE_POTENCIA_POR_NIVEL":                                                       [0, 0],
        "UG_DESABILITA_CONTROLE_DE_POTENCIA_POR_NIVEL":                                                     [0, 1],
        "UG_HABILITA_CONTROLE_DE_POTENCIA_POR_NIVEL_ESCALONADO":                                            [0, 2],
        "UG_DESABILITA_CONTROLE_DE_POTENCIA_POR_NIVEL_ESCALONADO":                                          [0, 3],
        "UG_HABILITA_PARADA_DA_UNIDADE_POR_NIVEL":                                                          [0, 4],
        "UG_DESABILITA_PARADA_DA_UNIDADE_POR_NIVEL":                                                        [0, 5],
        "UG_RESET_HORIMETRO_DA_UNIDADE":                                                                    [0, 6],

        ## UNIDADES_HIDRAULICAS
        "UHRV_RESET_FALHAS":                                                                                [3, 0],
        "UHRV_SELECIONA_OPERACAO_AUTOMATICA":                                                               [3, 1],
        "UHRV_SELECIONA_OPERACAO_EM_MANUTENCAO":                                                            [3, 2],
        "UHRV_LIGA_BOMBA_1_MANUAL":                                                                         [3, 3],
        "UHRV_DESLIGA_BOMBA_1_MANUAL":                                                                      [3, 4],
        "UHRV_LIGA_BOMBA_2_MANUAL":                                                                         [3, 5],
        "UHRV_DESLIGA_BOMBA_2_MANUAL":                                                                      [3, 6],
        "UHRV_SELECIONA_BOMBA_1_PRINCIPAL":                                                                 [3, 7],
        "UHRV_SELECIONA_BOMBA_2_PRINCIPAL":                                                                 [3, 8],
        "UHRV_RESET_HORIMETRO_BOMBA_1":                                                                     [3, 9],
        "UHRV_RESET_HORIMETRO_BOMBA_2":                                                                     [3, 10],

        "UHL_RESET_FALHAS":                                                                                 [2, 0],
        "UHL_SELECIONA_OPERACAO_AUTOMATICA":                                                                [2, 1],
        "UHL_SELECIONA_OPERACAO_EM_MANUTENCAO":                                                             [2, 2],
        "UHL_LIGA_BOMBA_1_MANUAL":                                                                          [2, 3],
        "UHL_DESLIGA_BOMBA_1_MANUAL":                                                                       [2, 4],
        "UHL_LIGA_BOMBA_2_MANUAL":                                                                          [2, 5],
        "UHL_DESLIGA_BOMBA_2_MANUAL":                                                                       [2, 6],
        "UHL_SELECIONA_BOMBA_1_PRINCIPAL":                                                                  [2, 7],
        "UHL_SELECIONA_BOMBA_2_PRINCIPAL":                                                                  [2, 8],
        "UHL_RESET_HORIMETRO_BOMBA_1":                                                                      [2, 9],
        "UHL_RESET_HORIMETRO_BOMBA_2":                                                                      [2, 10],

        ## COMANDOS_ANALÓGICOS
        "SP_NIVEL_MAX":                                                                                     4,
        "SP_NIVEL_4":                                                                                       6,
        "SP_NIVEL_3":                                                                                       8,
        "SP_NIVEL_2":                                                                                       10,
        "SP_NIVEL_1":                                                                                       12,
        "SP_NIVEL_PARADA":                                                                                  14,
        "SP_POTENCIA_MAX":                                                                                  16,
        "SP_POTENCIA_4":                                                                                    18,
        "SP_POTENCIA_3":                                                                                    20,
        "SP_POTENCIA_2":                                                                                    22,
        "SP_POTENCIA_1":                                                                                    24,


        ### RV
        ## ROTAÇÃO
        "RV_ROTACAO":                                                                                       16,

        ## ESTADO_OPERAÇÃO
        "RV_ESTADO_OPERACAO_PROCESSANDO":                                                                   [21, 0],
        "RV_ESTADO_OPERACAO_PARADA_FINALIZADA":                                                             [21, 1],
        "RV_ESTADO_OPERACAO_INICIO_PARTIDA":                                                                [21, 2],
        "RV_ESTADO_OPERACAO_PRIMEIRO_ESTAGIO_PARTIDA":                                                      [21, 3],
        "RV_ESTADO_OPERACAO_SEGUNDO_ESTAGIO_PARTIDA":                                                       [21, 4],
        "RV_ESTADO_OPERACAO_CONTROLANDO_ABERTURA":                                                          [21, 5],
        "RV_ESTADO_OPERACAO_CONTROLANDO_VELOCIDADE":                                                        [21, 6],
        "RV_ESTADO_OPERACAO_CONTROLANDO_EM_DROOP":                                                          [21, 7],
        "RV_ESTADO_OPERACAO_CONTROLANDO_EM_DROOP_EXTERNO":                                                  [21, 8],
        "RV_ESTADO_OPERACAO_CONTROLANDO_POTENCIA":                                                          [21, 9],
        "RV_ESTADO_OPERACAO_CONTROLANDO_POTENCIA_POR_REFERENCIA_ANALOGICA":                                 [21, 10],
        "RV_ESTADO_OPERACAO_CONTROLANDO_NIVEL":                                                             [21, 11],
        "RV_ESTADO_OPERACAO_ZERANDO_CARGA":                                                                 [21, 12],
        "RV_ESTADO_OPERACAO_PARANDO":                                                                       [21, 13],
        "RV_ESTADO_OPERACAO_CONTROLE_MANUAL_DISTRIBUIDOR":                                                  [21, 14],
        "RV_ESTADO_OPERACAO_CONTROLE_MANUAL_ROTOR":                                                         [21, 15],

        "RV_ESTADO_OPERACAO_EMERGENCIA":                                                                    [22, 0],

        ## CONTROLE_SINCRONIZADO_SELECIONADO
        "RV_CONTROLE_SINCRONIZADO_SELECIONADO":                                                             23,

        ## ENTRADAS_DIGITAIS
        "RV_ENTRADA_DIGITAL_SEM_BLOQUEIO_EXTERNO":                                                          [25, 0],
        "RV_ENTRADA_DIGITAL_HABILITA_REGULADOR":                                                            [25, 1],
        "RV_ENTRADA_DIGITAL_SELECIONA_MODO_CONTROLE_ISOLADO":                                               [25, 2],
        "RV_ENTRADA_DIGITAL_ZERA_CARGA":                                                                    [25, 3],
        "RV_ENTRADA_DIGITAL_RESET_FALHAS":                                                                  [25, 4],
        "RV_ENTRADA_DIGITAL_INCREMENTA_REFERENCIA_CONTROLE":                                                [25, 5],
        "RV_ENTRADA_DIGITAL_DECREMENTA_REFERENCIA_CONTROLE":                                                [25, 6],
        "RV_ENTRADA_DIGITAL_DISJUNTOR_MAQUINA_FECHADO":                                                     [25, 7],
        "RV_ENTRADA_DIGITAL_PROGRAMAVEL_1":                                                                 [25, 8],
        "RV_ENTRADA_DIGITAL_PROGRAMAVEL_2":                                                                 [25, 9],
        "RV_ENTRADA_DIGITAL_PROGRAMAVEL_3":                                                                 [25, 10],
        "RV_ENTRADA_DIGITAL_PROGRAMAVEL_4":                                                                 [25, 11],
        
        ## SAÍDAS_DIGITAIS
        "RV_SAIDA_DIGITAL_RELE_TRIP_NAO_ATUADO":                                                            [26, 0],
        "RV_SAIDA_DIGITAL_RELE_ALARME_ATUADO":                                                              [26, 1],
        "RV_SAIDA_DIGITAL_RELE_REGULADOR_HABILITADO":                                                       [26, 2],
        "RV_SAIDA_DIGITAL_RELE_REGULADOR_REGULANDO":                                                        [26, 3],
        "RV_SAIDA_DIGITAL_RELE_POTENCIA_NULA":                                                              [26, 4],
        "RV_SAIDA_DIGITAL_RELE_MAQUINA_PARADA":                                                             [26, 5],
        "RV_SAIDA_DIGITAL_RELE_VELOCIDADE_MENOR_30_PORCENTO":                                               [26, 6],
        "RV_SAIDA_DIGITAL_RELE_VELOCIDADE_MAIOR_90_PORCENTO":                                               [26, 7],
        "RV_SAIDA_DIGITAL_RELE_DISTRIBUIDOR_ABERTO":                                                        [26, 8],
        "RV_SAIDA_DIGITAL_RELE_SAIDA_PROGRAMAVEL_2":                                                        [26, 9],
        "RV_SAIDA_DIGITAL_SEGUIDOR_1":                                                                      [26, 10],
        "RV_SAIDA_DIGITAL_SEGUIDOR_2":                                                                      [26, 11],

        ## LIMITES_OPERAÇÃO
        "RV_LIMITADOR_SUPERIOR_DISTRIBUIDOR_ATUADO":                                                        [27, 0],
        "RV_LIMITADOR_INFERIOR_DISTRIBUIDOR_ATUADO":                                                        [27, 1],
        "RV_LIMITADOR_SUPERIOR_ROTOR_ATUADO":                                                               [27, 2],
        "RV_LIMITADOR_INFERIOR_ROTOR_ATUADO":                                                               [27, 3],
        "RV_LIMITADOR_SUPERIOR_VELOCIDADE_ATUADO":                                                          [27, 4],
        "RV_LIMITADOR_INFERIOR_VELOCIDADE_ATUADO":                                                          [27, 5],
        "RV_LIMITADOR_SUPERIOR_POTENCIA_ATUADO":                                                            [27, 6],
        "RV_LIMITADOR_INFERIOR_POTENCIA_ATUADO":                                                            [27, 7],

        ## SETPOINTS/REFERENCIA/FEEDBACK
        "RV_SETPOINT_VELOCIDADE":                                                                           29,
        "RV_SETPOINT_POTENCIA_ATIVA_KW":                                                                    30,
        "RV_SETPOINT_POTENCIA_ATIVA_PU":                                                                    30,
        "RV_SAIDA_CONTROLE_DISTRIBUIDOR_PU":                                                                32,
        "RV_SAIDA_CONTROLE_ROTOR_PU":                                                                       33,
        "RV_REFERENCIA_DISTRIBUIDOR_PU":                                                                    36,
        "RV_FEEDBACK_DISTRIBUIDOR_PU":                                                                      37,
        "RV_REFERENCIA_ROTOR_PU":                                                                           42,
        "RV_FEEDBACK_ROTOR_PU":                                                                             43,
        "RV_REFERENCIA_VELOCIDADE_PU":                                                                      48,
        "RV_FEEDBACK_VELOCIDADE_PU":                                                                        49,
        "RV_REFERENCIA_POTENCIA_ATIVA_PU":                                                                  54,
        "RV_FEEDBACK_POTENCIA_ATIVA_PU":                                                                    55,

        ## ALARME
        "RV_ALARME_SOBREFREQUENCIA":                                                                        [66, 0],
        "RV_ALARME_SUBFREQUENCIA":                                                                          [66, 1],
        "RV_ALARME_LEITURA_POSICAO_DISTRIBUIDOR":                                                           [66, 2],
        "RV_ALARME_LEITURA_POSICAO_ROTOR":                                                                  [66, 3],
        "RV_ALARME_LEITURA_POTENCIA_ATIVA":                                                                 [66, 4],
        "RV_ALARME_LEITURA_REFERENCIA_POTENCIA":                                                            [66, 5],
        "RV_ALARME_LEITURA_NIVEL_MONTANTE":                                                                 [66, 6],
        "RV_ALARME_NIVEL_MONTANTE_MUITO_BAIXO":                                                             [66, 7],
        "RV_ALARME_CONTROLE_POSICAO_DISTRIBUIDOR":                                                          [66, 8],
        "RV_ALARME_CONTROLE_POSICAO_ROTOR":                                                                 [66, 9],
        "RV_ALARME_RUIDO_MEDICAO_VELOCIDADE_PRINCIPAL":                                                     [66, 10],
        "RV_ALARME_RUIDO_MEDICAO_VELOCIDADE_RETAGUARDA":                                                    [66, 11],
        "RV_ALARME_PERDA_MEDICAO_VELOCIDADE_PRINCIPAL":                                                     [66, 12],
        "RV_ALARME_PERDA_MEDICAO_VELOCIDADE_RETAGUARDA":                                                    [66, 13],
        "RV_ALARME_DIFERENCA_MEDICAO_VELOCIDADE_PRINCIPAL_E_RETAGUARDA":                                    [66, 14],

        ## FALHA_1
        "RV_FALHA_SOBREFREQUENCIA_INSTANTANEA":                                                             [67, 0],
        "RV_FALHA_SOBREFREQUENCIA_TEMPORIZADA":                                                             [67, 1],
        "RV_FALHA_SUBFREQUENCIA_TEMPORIZADA":                                                               [67, 2],
        "RV_FALHA_GIRANDO_SEM_REGULACAO_OU_GIRO_INDEVIDO":                                                  [67, 3],
        "RV_FALHA_LEITURA_POSICAO_DISTRIBUIDOR":                                                            [67, 4],
        "RV_FALHA_LEITURA_POSICAO_ROTOR":                                                                   [67, 5],
        "RV_FALHA_LEITURA_POTENCIA_ATIVA":                                                                  [67, 6],
        "RV_FALHA_LEITURA_REFERENCIA_POTENCIA":                                                             [67, 7],
        "RV_FALHA_LEITURA_NIVEL_MONTANTE":                                                                  [67, 8],
        "RV_FALHA_RESERVA":                                                                                 [67, 9],
        "RV_FALHA_NIVEL_MONTANTE_MUITO_BAIXO":                                                              [67, 10],
        "RV_FALHA_CONTROLE_POSICAO_DISTRIBUIDOR":                                                           [67, 11],
        "RV_FALHA_CONTROLE_POSICAO_ROTOR":                                                                  [67, 12],
        "RV_FALHA_RUIDO_MEDICAO_VELOCIDADE_PRINCIPAL":                                                      [67, 13],
        "RV_FALHA_RUIDO_MEDICAO_VELOCIDADE_RETAGUARDA":                                                     [67, 14],
        "RV_FALHA_PERDA_MEDICAO_VELOCIDADE_PRINCIPAL":                                                      [67, 15],

        ## FALHA_2
        "RV_FALHA_PERDA_MEDICAO_VELOCIDADE_RETAGUARDA":                                                     [68, 0],
        "RV_FALHA_TEMPO_EXCESSIVO_PARTIDA":                                                                 [68, 1],
        "RV_FALHA_TEMPO_EXCESSIVO_PARADA":                                                                  [68, 2],
        "RV_FALHA_BLOQUEIO_EXTERNO":                                                                        [68, 3],
        "RV_FALHA_DIFERENCIA_MEDICAO_VELOCIDADE_PRINCIPAL_E_RETAGUARDA":                                    [68, 4],

        ## LEITURAS_ANALÓGICAS
        "RV_POTENCIA_APARENTE_NOMINAL":                                                                     79,
        "RV_POTENCIA_ATIVA_NOMINAL":                                                                        80,
        "RV_CONTROLE_1":                                                                                    85,
        "RV_CONTROLE_2":                                                                                    86,


        ### RT
        ## LEITURAS_ANALÓGICAS
        "RT_CORRENTE_EXCITACAO":                                                                            16,
        "RT_TENSAO_EXCITACAO":                                                                              17,
        "RT_TEMPERATURA_ROTOR":                                                                             25,

        ## ESTADO_OPERAÇÃO
        "RT_ESTADO_OPERACAO_PROCESSANDO":                                                                   [26, 0],
        "RT_ESTADO_OPERACAO_PARADA_FINALIZADA":                                                             [26, 1],
        "RT_ESTADO_OPERACAO_PRE_EXCITANDO":                                                                 [26, 2],
        "RT_ESTADO_OPERACAO_EXCITANDO":                                                                     [26, 3],
        "RT_ESTADO_OPERACAO_ESTABILIZANDO":                                                                 [26, 4],
        "RT_ESTADO_OPERACAO_CONTROLANDO_CORRENTE_EXCITACAO":                                                [26, 5],
        "RT_ESTADO_OPERACAO_CONTROLANDO_TENSAO_TERMINAL":                                                   [26, 6],
        "RT_ESTADO_OPERACAO_CONTROLANDO_EM_DROOP_POTENCIA_REATIVA":                                         [26, 7],
        "RT_ESTADO_OPERACAO_CONTROLANDO_EM_DROOP_FATOR_DE_POTENCIA":                                        [26, 8],
        "RT_ESTADO_OPERACAO_CONTROLANDO_POTENCIA_REATIVA":                                                  [26, 9],
        "RT_ESTADO_OPERACAO_CONTROLANDO_FATOR_DE_POTENCIA":                                                 [26, 10],
        "RT_ESTADO_OPERACAO_ZERANDO_CARGA":                                                                 [26, 11],
        "RT_ESTADO_OPERACAO_PARANDO":                                                                       [26, 12],
        "RT_ESTADO_OPERACAO_DISPARO_MANUAL_PONTE":                                                          [26, 13],
        "RT_ESTADO_OPERACAO_EMERGENCIA":                                                                    [26, 14],

        ## CONTROLE_SINCRONIZADO_SELECIONADO
        "RT_CONTROLE_SINCRONIZADO_SELECIONADO":                                                             27,

        ## ENTRADAS_DIGITAIS
        "RT_ENTRADA_DIGITAL_SEM_BLOQUEIO_EXTERNO":                                                          [30, 0],
        "RT_ENTRADA_DIGITAL_HABILITA_REGULADOR":                                                            [30, 1],
        "RT_ENTRADA_DIGITAL_SELECIONA_MODO_CONTROLE_ISOLADO":                                               [30, 2],
        "RT_RV_ENTRADA_DIGITAL_DRIVE_EXCITACAO_HABILITADO_LOGICA_DE_DISPARO":                               [30, 3],
        "RT_RV_ENTRADA_DIGITAL_RESET_FALHAS":                                                               [30, 4],
        "RT_ENTRADA_DIGITAL_INCREMENTA_REFERENCIA_CONTROLE":                                                [30, 5],
        "RT_ENTRADA_DIGITAL_DECREMENTA_REFERENCIA_CONTROLE":                                                [30, 6],
        "RT_ENTRADA_DIGITAL_DISJUNTOR_MAQUINA_FECHADO":                                                     [30, 7],
        "RT_ENTRADA_DIGITAL_CONTATOR_CAMPO_FECHADO":                                                        [30, 8],
        "RT_ENTRADA_DIGITAL_CROWBAR_INATIVO":                                                               [30, 9],
        "RT_ENTRADA_DIGITAL_PROGRAMAVEL_1":                                                                 [30, 10],
        "RT_ENTRADA_DIGITAL_PROGRAMAVEL_2":                                                                 [30, 11],

        ## SAÍDAS_DIGITAIS
        "RT_SAIDA_DIGITAL_RELE_TRIP_NAO_ATUADO":                                                            [31, 0],
        "RT_SAIDA_DIGITAL_RELE_ALARME_ATUADO":                                                              [31, 1],
        "RT_SAIDA_DIGITAL_RELE_REGULADOR_HABILITADO":                                                       [31, 2],
        "RT_SAIDA_DIGITAL_RELE_REGULADOR_REGULANDO":                                                        [31, 3],
        "RT_SAIDA_DIGITAL_RELE_HABILITA_DRIVE_EXCITACAO_LOGICA_DISPARO":                                    [31, 4],
        "RT_SAIDA_DIGITAL_RELE_HABILITA_CONTATOR_CAMPO":                                                    [31, 5],
        "RT_SAIDA_DIGITAL_RELE_HABILITA_PRE_EXCITACAO":                                                     [31, 6],
        "RT_SAIDA_DIGITAL_RELE_HABILITA_CROWBAR":                                                           [31, 7],
        "RT_SAIDA_DIGITAL_RELE_SAIDA_PROGRAMAVEL_1":                                                        [31, 8],
        "RT_SAIDA_DIGITAL_RELE_SAIDA_PROGRAMAVEL_2":                                                        [31, 9],
        "RT_SAIDA_DIGITAL_SEGUIDOR_1":                                                                      [31, 10],
        "RT_SAIDA_DIGITAL_SEGUIDOR_2":                                                                      [31, 11],

        ## LIMITIES_OPERAÇÃO
        "RT_LIMITADOR_SUPERIOR_CORRENTE_EXCITACAO_ATUADO":                                                  [32, 0],
        "RT_LIMITADOR_INFERIOR_CORRENTE_EXCITACAO_ATUADO":                                                  [32, 1],
        "RT_LIMITADOR_SUPERIOR_TENSAO_TERMINAL_ATUADO":                                                     [32, 2],
        "RT_LIMITADOR_INFERIOR_TENSAO_TERMINAL_ATUADO":                                                     [32, 3],
        "RT_LIMITADOR_SUPERIOR_POTENCIA_REATIVA_ATUADO":                                                    [32, 4],
        "RT_LIMITADOR_INFERIOR_POTENCIA_REATIVA_ATUADO":                                                    [32, 5],
        "RT_LIMITADOR_SUPERIOR_FATOR_DE_POTENCIA_ATUADO":                                                   [32, 6],
        "RT_LIMITADOR_INFERIOR_FATOR_DE_POTENCIA_ATUADO":                                                   [32, 7],
        "RT_LIMITADOR_VOLTZ_HERZ_ATUADO":                                                                   [32, 12],
        "RT_LIMITADOR_ABERTURA_PONTE_ATUADO":                                                               [32, 13],
        "RT_LIMITADOR_PQ_ATUADO_RELACAO_POTENCIA_ATIVA_X_POTENCIA_REATIVA":                                 [32, 14],

        ## SETPOINTS/REFERENCIA/FEEDBACK
        "RT_SETPOINT_TENSAO_PU":                                                                            40,
        "RT_SETPOINT_POTENCIA_REATIVA_KVAR":                                                                41,
        "RT_SETPOINT_POTENCIA_REATIVA_PU":                                                                  41,
        "RT_SETPOINT_FATOR_POTENCIA_PU":                                                                    42,
        "RT_ABERTURA_PONTE":                                                                                43,
        "RT_REFERENCIA_CORRENTE_CAMPO_PU":                                                                  46,
        "RT_FEEDBACK_CORRENTE_CAMPO_PU":                                                                    47,
        "RT_REFERENCIA_TENSAO_PU":                                                                          52,
        "RT_FEEDBACK_TENSAO_PU":                                                                            53,
        "RT_REFERENCIA_POTENCIA_REATIVA_PU":                                                                58,
        "RT_FEEDBACK_POTENCIA_REATIVA_PU":                                                                  59,
        "RT_REFERENCIA_FATOR_POTENCIA_PU":                                                                  64,
        "RT_FEEDBACK_FATOR_POTENCIA_PU":                                                                    65,

        ## ALARMES_1
        "RT_ALARME_SOBRETENSAO":                                                                            [70, 0],
        "RT_ALARME_SUBTENSAO":                                                                              [70, 1],
        "RT_ALARME_SOBREFREQUENCIA":                                                                        [70, 2],
        "RT_ALARME_SUBFREQUENCIA":                                                                          [70, 3],
        "RT_ALARME_LIMITE_SUPERIOR_POTENCIA_REATIVA_ULTRAPASSADO":                                          [70, 4],
        "RT_ALARME_LIMITE_INFERIOR_POTENCIA_REATIVA_ULTRAPASSADO":                                          [70, 5],
        "RT_ALARME_LIMITE_SUPERIOR_FATOR_DE_POTENCIA_ULTRAPASSADO":                                         [70, 6],
        "RT_ALARME_LIMITE_INFERIOR_FATOR_DE_POTENCIA_ULTRAPASSADO":                                         [70, 7],
        "RT_ALARME_VARIACAO_DE_TENSAO":                                                                     [70, 8],
        "RT_ALARME_POTENCIA_ATIVA_REVERSA":                                                                 [70, 9],
        "RT_ALARME_SOBRECORRENTE_TERMINAL":                                                                 [70, 10],
        "RT_ALARME_LIMITE_SUPERIOR_CORRENTE_EXCITACAO_ULTRAPASSADO":                                        [70, 11],
        "RT_ALARME_LIMITE_INFERIOR_CORRENTE_EXCITACAO_ULTRAPASSADO":                                        [70, 12],
        "RT_ALARME_TEMPERATURA_MUITO_ALTA_ROTOR":                                                           [70, 13],
        "RT_ALARME_PRESENCA_DE_TENSAO_TERMINAL_COM_AUSENCIA_DE_CORRENTE_DE_EXCITACAO":                      [70, 14],
        "RT_ALARME_PRESENCA_DE_CORRENTE_DE_EXCITACAO_COM_AUXENCIA_DE_TENSAO_TERMINAL":                      [70, 15],
        
        ## ALARMES_2
        "RT_ALARME_FALHA_CONTROLE_CORRENTE_EXCITACAO":                                                      [71, 0],
        "RT_ALARME_FALHA_CONTROLE_TENSAO_TERMINAL":                                                         [71, 1],
        "RT_ALARME_CROWBAR_ATUADO_COM_REGULADOR_HABILITADO":                                                [71, 2],
        "RT_ALARME_FALHA_HABILITAR_DRIVE_DE_EXCITACAO_LOGICA_DE_DISPARO":                                   [71, 3],
        "RT_ALARME_FALHA_FECHAR_CONTATOR_DE_CAMPO":                                                         [71, 4],
        "RT_ALARME_FALHA_DE_CORRENTE_DE_EXCITACAO_COM_PRE_EXCITACAO_ATIVA":                                 [71, 5],
        "RT_ALARME_PERDA_MEDICAO_POTENCIA_REATIVA":                                                         [71, 6],
        "RT_ALARME_PERDA_MEDICAO_TENSAO_TERMINAL":                                                          [71, 7],
        "RT_ALARME_PERDA_MEDICAO_CORRENTE_EXCITACAO":                                                       [71, 8],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_REATIVO":                                                        [71, 9],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_TENSAO":                                                         [71, 10],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_PRINCIPAL":                                            [71, 11],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_RETAGUARDA":                                           [71, 12],

        ## FALHAS_1
        "RT_FALHA_SOBRETENSAO":                                                                             [72, 0],
        "RT_FALHA_SUBTENSAO":                                                                               [72, 1],
        "RT_FALHA_SOBREFREQUENCIA":                                                                         [72, 2],
        "RT_FALHA_SUBFREQUENCIA":                                                                           [72, 3],
        "RT_FALHA_LIMITE_SUPERIOR_POTENCIA_REATIVA_ULTRAPASSADO":                                           [72, 4],
        "RT_FALHA_LIMITE_INFERIOR_POTENCIA_REATIVA_ULTRAPASSADO":                                           [72, 5],
        "RT_FALHA_LIMITE_SUPERIOR_FATOR_DE_POTENCIA_ULTRAPASSADO":                                          [72, 6],
        "RT_FALHA_LIMITE_INFERIOR_FATOR_DE_POTENCIA_ULTRAPASSADO":                                          [72, 7],
        "RT_FALHA_SOBRETENSAO_INSTANTANEA":                                                                 [72, 8],
        "RT_FALHA_VARIACAO_DE_TENSAO":                                                                      [72, 9],
        "RT_FALHA_POTENCIA_ATIVA_REVERSA":                                                                  [72, 10],
        "RT_FALHA_SOBRECORRENTE_TERMINAL":                                                                  [72, 11],
        "RT_FALHA_LIMITE_SUPERIOR_CORRENTE_EXCITACAO_ULTRAPASSADO":                                         [72, 12],
        "RT_FALHA_LIMITE_INFERIOR_CORRENTE_EXCITACAO_ULTRAPASSADO":                                         [72, 13],
        "RT_FALHA_LIMITE_SUPERIOR_TENSAO_EXCITACAO_ULTRAPASSADO":                                           [72, 14],
        "RT_FALHA_LIMITE_INFERIOR_TENSAO_EXCITACAO_ULTRAPASSADO":                                           [72, 15],

        ## FALHAS_2
        "RT_FALHA_TEMPERATURA_MUITO_ALTA_ROTOR":                                                            [73, 0],
        "RT_FALHA_PRESENCA_DE_TENSAO_TERMINAL_COM_AUSENCIA_DE_CORRENTE_DE_EXCITACAO":                       [73, 1],
        "RT_FALHA_PRESENCA_DE_CORRENTE_DE_EXCITACAO_COM_AUXENCIA_DE_TENSAO_TERMINAL":                       [73, 2],
        "RT_FALHA_FALHA_CONTROLE_CORRENTE_EXCITACAO":                                                       [73, 3],
        "RT_FALHA_FALHA_CONTROLE_TENSAO_TERMINAL":                                                          [73, 4],
        "RT_FALHA_CROWBAR_ATUADO_COM_REGULADOR_HABILITADO":                                                 [73, 5],
        "RT_FALHA_FALHA_HABILITAR_DRIVE_DE_EXCITACAO_LOGICA_DE_DISPARO":                                    [73, 6],
        "RT_ALAME_FALHA_FECHAR_CONTATOR_DE_CAMPO":                                                          [73, 7],
        "RT_FALHA_FALHA_DE_CORRENTE_DE_EXCITACAO_COM_PRE_EXCITACAO_ATIVA":                                  [73, 8],
        "RT_FALHA_TEMPO_EXCESSIVO_DE_PRE_EXCITACAO":                                                        [73, 9],
        "RT_FALHA_TEMPO_EXCESSIVO_DE_PARADA":                                                               [73, 10],
        "RT_FALHA_TEMPO_EXCESSIVO_DE_PARTIDA":                                                              [73, 11],
        "RT_FALHA_BLOQUEIO_EXTERNO":                                                                        [73, 12],

        "RT_FALHA_PERDA_MEDICAO_POTENCIA_REATIVA":                                                          [74, 0],
        "RT_FALHA_PERDA_MEDICAO_TENSAO_TERMINAL":                                                           [74, 1],
        "RT_FALHA_PERDA_MEDICAO_CORRENTE_EXCITACAO_PRINCIPAL":                                              [74, 2],
        "RT_FALHA_PERDA_MEDICAO_CORRENTE_EXCITACAO_RETAGUARDA":                                             [74, 3],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_REATIVO":                                                         [74, 4],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_TENSAO":                                                          [74, 5],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_PRINCIPAL":                                             [74, 6],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_RETAGUARDA":                                            [74, 7],

        ## LEITURAS_ANALÓGICAS
        "RT_TENSAO_NOMINAL":                                                                                85,
        "RT_CONTROLE_1":                                                                                    90,
        "RT_CONTROLE_2":                                                                                    91,
    },

    "UG2": {
        ### STATUS
        ## ENTRADAS_DIGITAIS_1
        "UHRV_BOMBA_1_FALHA":                                                                               [1, 0],
        "UHRV_BOMBA_1_LIGADA":                                                                              [1, 1],
        "UHRV_BOMBA_2_FALHA":                                                                               [1, 2],
        "UHRV_BOMBA_2_LIGADA":                                                                              [1, 3],
        "UHL_BOMBA_1_FALHA":                                                                                [1, 4],
        "UHL_BOMBA_1_LIGADA":                                                                               [1, 5],
        "UHL_BOMBA_2_FALHA":                                                                                [1, 6],
        "UHL_BOMBA_2_LIGADA":                                                                               [1, 7],
        "UG_MOLA_CARREGADA_DISJUNTOR_DE_MAQUINA":                                                           [1, 8],
        "UG_DISJUNTOR_MAQUINA_52G_FECHADO":                                                                 [1, 9],
        "UG_CPG_DISJUNTOR_TPS_MULTIMEDIDOR_E_REGULADORES_FECHADO":                                          [1, 10],
        "UG_CPG_DISJUNTOR_TPS_RELE_DE_PROTECAO_FECHADO":                                                    [1, 11],
        "UG_CPG_PORTA_FRONTAL_FECHADA":                                                                     [1, 12],
        "UG_CPG_PORTA_TRASEIRA_FECHADA":                                                                    [1, 13],
        "UHL_NIVEL_OLEO_MUITO_BAIXO":                                                                       [1, 14], # HIGH
        "UHL_NIVEL_OLEO_MUITO_ALTO":                                                                        [1, 15], # HIGH

        "UG_ENTRADA_DIGITAL_RESERVA_2":                                                                     [0, 0],
        "UHL_PRESSAO_LINHA_OLEO":                                                                           [0, 1],
        "UG_ENTRADA_DIGITAL_RESERVA_4":                                                                     [0, 2],
        "UG_ENTRADA_DIGITAL_RESERVA_5":                                                                     [0, 3],
        "UG_ENTRADA_DIGITAL_RESERVA_6":                                                                     [0, 4],
        "UHL_FILTRO_OLEO_SUJO":                                                                             [0, 5], # HIGH
        "UHRV_NIVEL_OLEO_MUITO_BAIXO":                                                                      [0, 6], # HIGH
        "UHRV_FREIO_PRESSURIZADO":                                                                          [0, 7],
        "UHRV_FILTRO_OLEO_SUJO":                                                                            [0, 8], # HIGH
        "UG_ENTRADA_DIGITAL_RESERVA_3":                                                                     [0, 9],
        "UG_ENTRADA_DIGITAL_RESERVA_1":                                                                     [0, 10],
        "UG_ENTRADA_DIGITAL_RESERVA_7":                                                                     [0, 11],
        "UG_RESISTENCIA_AQUECIMENTO_GERADOR_FALHA":                                                         [0, 12],
        "UG_RESISTENCIA_AQUECIMENTO_GERADOR_LIGADA":                                                        [0, 13],
        "RT_CONTATOR_CAMPO_FECHADO":                                                                        [0, 14],
        "UG_RELE_PROTECAO_MAQUINA":                                                                         [0, 15],

        ## ENTRADAS_DIGITAIS_2
        "UG_RELE_PROTECAO_MAQUINA_BF":                                                                      [3, 0],
        "UG_RELE_PROTECAO_MAQUINA_WATCHDOG_NORMAL":                                                         [3, 1],
        "UG_RELE_PROTECAO_TRANSFERENCIA_DE_DISPARO":                                                        [3, 2],
        "RV_BOTAO_AUMENTA_REFERENCIA_CONTROLE":                                                             [3, 3],
        "RV_BOTAO_DIMINUI_REFERENCIA_CONTROLE":                                                             [3, 4],
        "RT_BOTAO_AUMENTA_REFERENCIA_CONTROLE":                                                             [3, 5],
        "RT_BOTAO_DIMINUI_REFERENCIA_CONTROLE":                                                             [3, 6],
        "UG_SINCRONIZADOR_ESTADO_SINCRONIZADO":                                                             [3, 7],
        "UG_BOTAO_PARA_UNIDADE_GERADORA":                                                                   [3, 8],
        "UG_BOTAO_PARTE_UNIDADE_GERADORA":                                                                  [3, 9],
        "UG_BOTAO_REARME_FALHAS_UNIDADE_GERADORA":                                                          [3, 10],
        "UG_BOTAO_EMERGENCIA_DA_UNIDADE_GERADORA":                                                          [3, 11], # HIGH
        "UG_SUPERVISAO_BOBINA_DISJUNTOR_DE_MAQUINA":                                                        [3, 12],
        "UG_SUPERVISAO_BOBINA_RELE_DE_BLOQUEIO":                                                            [3, 13],

        "UG_RELE_DE_BLOQUEIO_86EH_ATUADO":                                                                  [2, 12], # HIGH
        "UG_SUBTENSAO_TENSAO_125VCC":                                                                       [2, 13], # HIGH
        "UG_SUBTENSAO_TENSAO_24VCC":                                                                        [2, 14], # HIGH
        "UG_DISJUNTORES_125VCC_ABERTOS":                                                                    [2, 15], # HIGH

        ## ENTRADAS_DIGITAIS_3
        "UG_DISJUNTORES_24VCC_ABERTOS":                                                                     [5, 0], # HIGH
        "UG_CLP_GERAL_SINAL_DE_BLOQUEIO_EXTERNO":                                                           [5, 1], # HIGH
        "UG_CLP_GERAL_SINAL_DE_SISTEMA_DE_AGUA_OK":                                                         [5, 2],
        "UG_CLP_GERAL_SINAL_RESERVA":                                                                       [5, 3],
        "ENTRADA_DIGITAL_RESERVA_3":                                                                        [5, 4],
        "UG_ESCOVAS_GASTAS_POLO_POSITIVO":                                                                  [5, 5],
        "UG_ESCOVAS_GASTAS_POLO_NEGATIVO":                                                                  [5, 6],
        "ENTRADA_DIGITAL_RESERVA_5":                                                                        [5, 7],
        "UG_DISPARO_MECANICO_DESATUADO":                                                                    [5, 8],
        "UG_DISPARO_MECANICO_ATUADO":                                                                       [5, 9],

        ## ALARMES_ANALÓGICOS
        "ALARME_TEMPERATURA_ALTA_PONTE_RETIFICADORA_FASE_A":                                                [7, 0],
        "ALARME_TEMPERATURA_ALTA_PONTE_RETIFICADORA_FASE_B":                                                [7, 1],
        "ALARME_TEMPERATURA_ALTA_PONTE_RETIFICADORA_FASE_C":                                                [7, 2],
        "ALARME_TEMPERATURA_ALTA_ENTRADA_RESERVA_3":                                                        [7, 3],
        "ALARME_TEMPERATURA_ALTA_TRAFO_EXCITACAO":                                                          [7, 4],
        "ALARME_TEMPERATURA_ALTA_MANCAL_GUIA":                                                              [7, 5],
        "ALARME_TEMPERATURA_ALTA_OLEO_DA_UHRV":                                                             [7, 6],
        "ALARME_TEMPERATURA_ALTA_OLEO_DA_UHL":                                                              [7, 7],
        "ALARME_TEMPERATURA_ALTA_CASQUILHO_MANCAL_COMBINADO":                                               [7, 8],
        "ALARME_TEMPERATURA_ALTA_CONTRA_ESCORA_MANCAL_COMBINADO":                                           [7, 9],
        "ALARME_TEMPERATURA_ALTA_PATINS_MANCAL_COMBINADO_MEDICAO_1":                                        [7, 10],
        "ALARME_TEMPERATURA_ALTA_PATINS_MANCAL_COMBINADO_MEDICAO_2":                                        [7, 11],
        "ALARME_TEMPERATURA_ALTA_MANCAL_GUIA_INTERNO_MEDICAO_1":                                            [7, 12],
        "ALARME_TEMPERATURA_ALTA_MANCAL_GUIA_INTERNO_MEDICAO_2":                                            [7, 13],
        "ALARME_TEMPERATURA_ALTA_NUCLEO_ESTATORICO":                                                        [7, 14],
        "ALARME_TEMPERATURA_ALTA_GERADOR_FASE_A":                                                           [7, 15],

        "ALARME_TEMPERATURA_ALTA_GERADOR_FASE_B":                                                           [6, 0],
        "ALARME_TEMPERATURA_ALTA_GERADOR_FASE_C":                                                           [6, 1],
        "ALARME_TEMPERATURA_ALTA_ENTRADA_RESERVA_2":                                                        [6, 2],
        "ALARME_TEMPERATURA_ALTA_ENTRADA_RESERVA":                                                          [6, 3],
        "ALARME_PRESSAO_ENTRADA_TURBINA":                                                                   [6, 4],
        "ALARME_PRESSAO_REGULAGEM_1_TURBINA":                                                               [6, 5],
        "ALARME_PRESSAO_SAIDA_RODA":                                                                        [6, 6],
        "ALARME_PRESSAO_SAIDA_SUCCAO":                                                                      [6, 7],
        "ALARME_VIBRACAO_EIXO_X_MANCAL_COMBINADO":                                                          [6, 8],
        "ALARME_VIBRACAO_EIXO_Y_MANCAL_COMBINADO":                                                          [6, 9],
        "ALARME_VIBRACAO_EIXO_Z_MANCAL_COMBINADO":                                                          [6, 10],
        "ALARME_PRESSAO_ACUMULADOR_UHRV":                                                                   [6, 11],
        "ALARME_VIBRACAO_DETECCAO_HORIZONTAL_":                                                             [6, 12],
        "ALARME_VIBRACAO_DETECCAO_VERTICAL":                                                                [6, 13],
        "ALARME_PRESSAO_REGULAGEM_2_TURBINA":                                                               [6, 14],
        "ALARME_PRESSAO_DIFERENCIAL_REGULAGEM_TURBINA":                                                     [6, 15],

        ## FALHAS_ANALÓGICAS
        "FALHA_LEITURA_PRESSAO_ENTRADA_TURBINA":                                                            [8, 4],
        "FALHA_LEITURA_PRESSAO_REGULAGEM_1_TURBINA":                                                        [8, 5],
        "FALHA_LEITURA_PRESSAO_SAIDA_RODA":                                                                 [8, 6],
        "FALHA_LEITURA_PRESSAO_SAIDA_SUCCAO":                                                               [8, 7],
        "FALHA_LEITURA_VIBRACAO_EIXO_X_MANCAL_COMBINADO":                                                   [8, 8],
        "FALHA_LEITURA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO":                                                   [8, 9],
        "FALHA_LEITURA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO":                                                   [8, 10],
        "FALHA_LEITURA_VIBRACAO_DETECCAO_HORIZONTAL_":                                                      [8, 12],
        "FALHA_LEITURA_VIBRACAO_DETECCAO_VERTICAL":                                                         [8, 13],
        "FALHA_LEITURA_PRESSAO_REGULAGEM_2_TURBINA":                                                        [8, 14],
        "FALHA_LEITURA_PRESSAO_DIFERENCIAL_REGULAGEM_TURBINA":                                              [8, 15],

        ## UG
        "ESTADO_DE_MAQUINA_PARADA_FINALIZADA":                                                              [11, 0],
        "ESTADO_DE_MAQUINA_PARTINDO":                                                                       [11, 1],
        "ESTADO_DE_MAQUINA_GIRANDO_DESEXITADA":                                                             [11, 2],
        "ESTADO_DE_MAQUINA_PRONTA_PARA_SINCRONIZAR":                                                        [11, 3],
        "ESTADO_DE_MAQUINA_SINCRONIZADA":                                                                   [11, 4],
        "ESTADO_DE_MAQUINA_PARANDO_PASSO_A_PASSO":                                                          [11, 5],
        "ESTADO_DE_MAQUINA_PARANDO_SEM_REJEICAO":                                                           [11, 6],
        "ESTADO_DE_MAQUINA_PARANDO_EM_EMERGENCIA":                                                          [11, 7],
        "CONTROLE_DE_POTENCIA_POR_NIVEL_HABILITADO":                                                        [11, 8],
        "CONTROLE_DE_POTENCIA_POR_NIVEL_ESCALONADO_HABILITADO":                                             [11, 9],
        "PARADA_DA_UNIDADE_POR_NIVEL_HABILITADO":                                                           [11, 10],
        "FALHA_HABILITAR_SISTEMA_DE_AGUA":                                                                  [11, 11],
        "ESTADO_DE_MAQUINA_PARANDO_PARCIAL":                                                                [11, 12],
        "FALHA_COMUNICACAO_COM_CLP_DA_TOMADA_DAGUA":                                                        [11, 13],
        "COMPORTA_OPERANDO":                                                                                [11, 14],

        ## PRE_CONDICOES_PARTIDA
        "PRE_CONDICAO_00_SEM_BLOQUEIOS":                                                                    [13, 0],
        "PRE_CONDICAO_01_BOMBA_1_OU_2_DA_UHRV_DISPONÍVEL":                                                  [13, 1],
        "PRE_CONDICAO_02_COM_TENSAO_SERVICOS_AUXILIARES":                                                   [13, 2],
        "PRE_CONDICAO_03_PARADA_FINALIZADA":                                                                [13, 3],
        "PRE_CONDICAO_04_UHRV_EM_AUTOMATICO":                                                               [13, 4],
        "PRE_CONDICAO_05_COMPORTA_OPERANDO":                                                                [13, 5],

        "PRE_CONDICOES_PARTIDA_OK":                                                                         [12, 15],

        ## PERMISSIVOS_UHL
        "UHL_PERMISSIVO_00_BOMBA_1_OU_BOMBA_2_UHL_DISPONIVEL":                                              [15, 0],
        "UHL_PERMISSIVO_01_SEM_FALHA_PRESSOSTATO_LINHA_OLEO":                                               [15, 1],
        "UHL_PERMISSIVO_02_UNIDADE_EM_AUTOMATICO":                                                          [15, 2],

        "UHL_PERMISSIVOS_OK":                                                                               [14, 15],

        ## PERMISSIVOS_SISTEMA_ÁGUA
        "AGUA_SELO_PERMISSIVOS_OK":                                                                         [17, 15],

        ## PERMISSIVOS_RV
        "RV_PERMISSIVO_00_SEM_ALARME_TEMPERATURA_OLEO_UHL":                                                 [19, 0],
        "RV_PERMISSIVO_01_SEM_ALARME_TEMPERATURA_OLEO_UHRV":                                                [19, 1],
        "RV_PERMISSIVO_02_SEM_ALARME_TEMPERATURA_MANCAL_COMBINADO":                                         [19, 2],
        "RV_PERMISSIVO_03_SEM_ALARME_TEMPERATURA_MANCAL_CONTRA_ESCORA_COMBINADO":                           [19, 3],
        "RV_PERMISSIVO_04_SEM_ALARME_TEMPERATURA_1_PATINS_MANCAL_COMBINADO":                                [19, 4],
        "RV_PERMISSIVO_05_SEM_ALARME_TEMPERATURA_2_PATINS_MANCAL_COMBINADO":                                [19, 5],
        "RV_PERMISSIVO_06_SEM_ALARME_TEMPERATURA_1_MACAL_GUIA_INTERNO":                                     [19, 6],
        "RV_PERMISSIVO_07_SEM_ALARME_TEMPERATURA_2_MACAL_GUIA_INTERNO":                                     [19, 7],

        "RV_PERMISSIVOS_OK":                                                                                [18, 15],

        ## PERMISSIVOS_RT
        "RT_PERMISSIVO_00_SEM_ALARME_TEMPERATURAS_PONTE_RETIFICADORA_FASE_A":                               [21, 0],
        "RT_PERMISSIVO_01_SEM_ALARME_TEMPERATURAS_PONTE_RETIFICADORA_FASE_B":                               [21, 1],
        "RT_PERMISSIVO_02_SEM_ALARME_TEMPERATURAS_PONTE_RETIFICADORA_FASE_C":                               [21, 2],
        "RT_PERMISSIVO_03_SEM_ALARME_TEMPERATURA_GERADOR_FASE_A":                                           [21, 3],
        "RT_PERMISSIVO_04_SEM_ALARME_TEMPERATURA_GERADOR_FASE_B":                                           [21, 4],
        "RT_PERMISSIVO_05_SEM_ALARME_TEMPERATURA_GERADOR_FASE_C":                                           [21, 5],
        "RT_PERMISSIVO_06_SEM_ALARME_TEMPERATURA_GERADOR_NUCLEO_ESTATORICO":                                [21, 6],
        "RT_PERMISSIVO_07_SEM_ALARME_TEMPERATURA_TRAFO_EXCITACAO":                                          [21, 7],

        "RT_PERMISSIVOS_OK":                                                                                [20, 15],

        ## PERMISSIVOS_SINCRONISMO
        "SINCRONISMO_PERMISSIVO_00_DISJUNTOR_DE_LINHA_FECHADO":                                             [23, 0],

        "SINCRONISMO_PERMISSIVOS_OK":                                                                       [22, 15],

        ## BLOQUEIO_86M
        "86M_BLOQUEIO_00_NIVEL_MUITO_ALTO_OLEO_UHL":                                                        [25, 0],
        "86M_BLOQUEIO_01_NIVEL_MUITO_BAIXO_OLEO_UHL":                                                       [25, 1],
        "86M_BLOQUEIO_02_NIVEL_MUITO_BAIXO_OLEO_UHRV":                                                      [25, 2],
        "86M_BLOQUEIO_03_FALTA_PRESSAO_SISTEMA_DE_AGUA":                                                    [25, 3],
        "86M_BLOQUEIO_04_TEMPERATURA_MUITO_ALTA_OLEO_UHL":                                                  [25, 4],
        "86M_BLOQUEIO_05_TEMPERATURA_MUITO_ALTA_OLEO_UHRV":                                                 [25, 5],
        "86M_BLOQUEIO_06_FALHA_LEITURA_TEMPERATURA_OLEO_UHL":                                               [25, 6],
        "86M_BLOQUEIO_07_FALHA_LEITURA_TEMPERATURA_OLEO_UHRV":                                              [25, 7],
        "86M_BLOQUEIO_08_FALHA_LEITURA_TEMPERATURA_CASQUILHO_MANCAL_COMBINADO":                             [25, 8],
        "86M_BLOQUEIO_09_FALHA_LEITURA_TEMPERATURA_CONTRA_ESCORA_MANCAL_COMBINADO":                         [25, 9],
        "86M_BLOQUEIO_10_FALHA_LEITURA_TEMPERATURA_1_PATINS_MANCAL_COMBINADO":                              [25, 10],
        "86M_BLOQUEIO_11_FALHA_LEITURA_TEMPERATURA_2_PATINS_MANCAL_COMBINADO":                              [25, 11],
        "86M_BLOQUEIO_12_FALHA_LEITURA_TEMPERATURA_1_MANCAL_GUIA_INTERNO":                                  [25, 12],
        "86M_BLOQUEIO_13_FALHA_LEITURA_TEMPERATURA_2_MANCAL_GUIA_INTERNO":                                  [25, 13],
        "86M_BLOQUEIO_14_FALHA_LEITURA_TEMPERATURA_PONTE_FASE_A":                                           [25, 14],
        "86M_BLOQUEIO_15_FALHA_LEITURA_TEMPERATURA_PONTE_FASE_B":                                           [25, 15],

        "86M_BLOQUEIO_16_FALHA_LEITURA_TEMPERATURA_PONTE_FASE_C":                                           [24, 0],
        "86M_BLOQUEIO_17_FALHA_LEITURA_TEMPERATURA_GERADOR_FASE_A":                                         [24, 1],
        "86M_BLOQUEIO_18_FALHA_LEITURA_TEMPERATURA_GERADOR_FASE_B":                                         [24, 2],
        "86M_BLOQUEIO_19_FALHA_LEITURA_TEMPERATURA_GERADOR_FASE_C":                                         [24, 3],
        "86M_BLOQUEIO_20_FALHA_LEITURA_TEMPERATURA_GERADOR_NUCLEO_ESTATORICO":                              [24, 4],
        "86M_BLOQUEIO_21_FALHA_LEITURA_VIBRACAO_DETECCAO_HORIZONTAL":                                       [24, 5],
        "86M_BLOQUEIO_22_FALHA_LEITURA_VIBRACAO_DETECCAO_VERTICAL":                                         [24, 6],
        "86M_BLOQUEIO_23_FALHA_LEITURA_VIBRACAO_EIXO_X_MANCAL_COMBINADO":                                   [24, 7],
        "86M_BLOQUEIO_24_FALHA_LEITURA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO":                                   [24, 8],
        "86M_BLOQUEIO_25_FALHA_LEITURA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO":                                   [24, 9],
        "86M_BLOQUEIO_26_TRIP_VIBRACAO_DETECCAO_HORIZONTAL":                                                [24, 10],
        "86M_BLOQUEIO_27_TRIP_VIBRACAO_DETECCAO_VERTICAL":                                                  [24, 11],
        "86M_BLOQUEIO_28_TRIP_VIBRACAO_EIXO_X_MANCAL_COMBINADO":                                            [24, 12],
        "86M_BLOQUEIO_29_TRIP_VIBRACAO_EIXO_Y_MANCAL_COMBINADO":                                            [24, 13],
        "86M_BLOQUEIO_30_TRIP_VIBRACAO_EIXO_Z_MANCAL_COMBINADO":                                            [24, 14],
        "86M_BLOQUEIO":                                                                                     [24, 15],

        ## BLOQUEIO_86E
        "86E_BLOQUEIO_00_CUBICULO_PROTECAO_GERADOR_DISJUNTOR_TPS_MULTIMEDIDOR_E_REGULADORES_ABERTO":        [27, 0],
        "86E_BLOQUEIO_01_CUBICULO_PROTECAO_GERADOR_DISJUNTOR_TPS_RELE_DE_PROTECAO_DA_UNIDADE_ABERTO":       [27, 1],
        "86E_BLOQUEIO_02_CUBICULO_PROTECAO_GERADOR_PORTA_FRONTAL_ABERTA":                                   [27, 2],
        "86E_BLOQUEIO_03_CUBICULO_PROTECAO_GERADOR_PORTA_TRASEIRA_ABERTA":                                  [27, 3],
        "86E_BLOQUEIO_04_RELE_DE_PROTECAO_DA_UNIDADE":                                                      [27, 4],
        "86E_BLOQUEIO_05_RELE_DE_PROTECAO_DA_UNIDADE_FALHA_WATCHDOG":                                       [27, 5],
        "86E_BLOQUEIO_06_RELE_DE_PROTECAO_DA_UNIDADE_BF":                                                   [27, 6],
        "86E_BLOQUEIO_07_SUBTENSAO_CIRCUITO_TENSAO_24VCC":                                                  [27, 7],
        "86E_BLOQUEIO_08_SUBTENSAO_CIRCUITO_TENSAO_125VCC":                                                 [27, 8],
        "86E_BLOQUEIO_09_DISJUNTORES_CIRCUITO_TENSAO_24VCC_ABERTOS":                                        [27, 9],
        "86E_BLOQUEIO_10_DISJUNTORES_CIRCUITO_TENSAO_125VCC_ABERTOS":                                       [27, 10],
        "86E_BLOQUEIO_11_PARADA_FALHA_ABERTURA_DISJUNTOR_DE_MAQUINA":                                       [27, 11],
        "86E_BLOQUEIO_12_PARADA_FALHA_DESABILITAR_REGULADOR_DE_TENSAO":                                     [27, 12],
        "86E_BLOQUEIO_13_PARADA_RELE_TRIP_REGULADOR_DE_TENSAO":                                             [27, 13],
        "86E_BLOQUEIO_14_RELE_DE_PROTECAO_DA_UNIDADE_TRANSFERENCIA_DE_DISPARO_RELE_LINHA_OU_TRAFO":         [27, 14],
        "86E_BLOQUEIO_15_RESERVA_2":                                                                        [27, 15],

        "86E_BLOQUEIO_16_TEMPERATURA_MUITO_ALTA_PONTE_RETIFICADOR_FASE_A":                                  [26, 0],
        "86E_BLOQUEIO_17_TEMPERATURA_MUITO_ALTA_PONTE_RETIFICADOR_FASE_B":                                  [26, 1],
        "86E_BLOQUEIO_18_TEMPERATURA_MUITO_ALTA_PONTE_RETIFICADOR_FASE_C":                                  [26, 2],
        "86E_BLOQUEIO_19_TEMPERATURA_MUITO_ALTA_GERADOR_FASE_A":                                            [26, 3],
        "86E_BLOQUEIO_20_TEMPERATURA_MUITO_ALTA_GERADOR_FASE_B":                                            [26, 4],
        "86E_BLOQUEIO_21_TEMPERATURA_MUITO_ALTA_GERADOR_FASE_C":                                            [26, 5],
        "86E_BLOQUEIO_22_TEMPERATURA_MUITO_ALTA_GERADOR_NUCLEO_ESTATORICO":                                 [26, 6],
        "86E_BLOQUEIO_23_TEMPERATURA_MUITO_ALTA_GERADOR_SAIDA_DE_AR":                                       [26, 7],
        "86E_BLOQUEIO_24_TEMPERATURA_MUITO_ALTA_TRAFO_ATERRAMENTO":                                         [26, 8],
        "86E_BLOQUEIO_25_TEMPERATURA_MUITO_ALTA_TRAFO_EXCITACAO":                                           [26, 9],
        "86E_BLOQUEIO_26_FALHA_LEITURA_TEMPERATURA_TRAFO_EXCITACAO":                                        [26, 10],
        "86E_BLOQUEIO":                                                                                     [26, 15],

        ## BLOQUEIO_86H
        "86H_BLOQUEIO_00_FALHA_BOMBAS_DE_LUBRIFICACAO":                                                     [29, 0],
        "86H_BLOQUEIO_01_FALTA_PRESSAO_OLEO_LINHA_LUBRIFICACAO":                                            [29, 1],
        "86H_BLOQUEIO_02_GIRO_INDEVIDO_DA_UNIDADE_GERADORA":                                                [29, 2],
        "86H_BLOQUEIO_03_RESERVA":                                                                          [29, 3],
        "86H_BLOQUEIO_04_RESERVA":                                                                          [29, 4],
        "86H_BLOQUEIO_05_PRESSAO_MUITO_BAIXA_ACUMULADOR_UHRV_MEDICAO_ANALOGICA":                            [29, 5],
        "86H_BLOQUEIO_06_BOTAO_EMERGENCIA":                                                                 [29, 6],
        "86H_BLOQUEIO_07_RELE_TRIP_REGULADOR_DE_VELOCIDADE":                                                [29, 7],
        "86H_BLOQUEIO_08_RESERVA":                                                                          [29, 8],
        "86H_BLOQUEIO_09_BLOQUEIO_EXTERNO_CLP_GERAL":                                                       [29, 9],
        "86H_BLOQUEIO_10_PARADA_FALHA_DESCARGA_POTENCIA":                                                   [29, 10],
        "86H_BLOQUEIO_11_PARADA_FALHA_DESABILITAR_REGULADOR_DE_VELOCIDADE":                                 [29, 11],
        "86H_BLOQUEIO_12_PARADA_FALHA_FECHAR_DISTRIBUIDOR":                                                 [29, 12],
        "86H_BLOQUEIO_13_PARADA_FALHA_PARAR_UNIDADE_GERADORA":                                              [29, 13],
        "86H_BLOQUEIO_14_BLOQUEIO_COMPORTA":                                                                [29, 14],
        "86H_BLOQUEIO_15_COMPORTA_NAO_OPERANDO":                                                            [29, 15],

        "86H_BLOQUEIO_16_FALHA_COMUNICACAO_CLP_TOMADA_DAGUA":                                               [28, 0],
        "86H_BLOQUEIO_17_FALHA_LEITURA_PRESSAO_ACUMULADOR_UHRV":                                            [28, 1],
        "86H_BLOQUEIO_18_TEMPERATURA_MUITO_ALTA_MANCAL_COMBINADO":                                          [28, 2],
        "86H_BLOQUEIO_19_TEMPERATURA_MUITO_ALTA_CONTRA_ESCORA_MANCAL_COMBINADO":                            [28, 3],
        "86H_BLOQUEIO_20_TEMPERATURA_MUITO_ALTA_PATINS_MANCAL_COMBINADO_LEITURA_1":                         [28, 4],
        "86H_BLOQUEIO_21_TEMPERATURA_MUITO_ALTA_PATINS_MANCAL_COMBINADO_LEITURA_2":                         [28, 5],
        "86H_BLOQUEIO_22_TEMPERATURA_MUITO_ALTA_MANCAL_GUIA_INTERNO_LEITURA_1":                             [28, 6],
        "86H_BLOQUEIO_23_TEMPERATURA_MUITO_ALTA_MANCAL_GUIA_INTERNO_LEITURA_2":                             [28, 7],
        "86H_BLOQUEIO_24_COMANDO_PARADA_DE_EMERGENCIA":                                                     [28, 8],
        "86H_BLOQUEIO_25_DISPARO_MECANICO_ATUADO":                                                          [28, 9],
        "86H_BLOQUEIO_26_MAXIMO_DIFERENCIAL_DE_GRADE":                                                      [28, 10],
        "86H_BLOQUEIO":                                                                                     [28, 15],

        ## PARTIDA_PARADA_PASSO_ATUAL
        "PARTIDA_PASSO_ATUAL_HABILITA_DESAPLICA_FREIO":                                                     [31, 0],
        "PARTIDA_PASSO_ATUAL_HABILITA_UNIDADE_LUBRIFICACAO_MANCAIS":                                        [31, 1],
        "PARTIDA_PASSO_ATUAL_HABILITA_SISTEMA_DE_AGUA":                                                     [31, 2],
        "PARTIDA_PASSO_ATUAL_HABILITA_REGULADOR_DE_VELOCIDADE":                                             [31, 3],
        "PARTIDA_PASSO_ATUAL_HABILITA_REGULADOR_DE_TENSAO":                                                 [31, 4],
        "PARTIDA_PASSO_ATUAL_HABILITA_SINCRONISMO":                                                         [31, 5],

        "PARADA_PASSO_ATUAL_DESCARGA_POTENCIA":                                                             [30, 0],
        "PARADA_PASSO_ATUAL_DESABILITA_REGULADOR_DE_TENSAO":                                                [30, 1],
        "PARADA_PASSO_ATUAL_DESABILITA_REGULADOR_DE_VELOCIDADE_E_APLICA_FREIO":                             [30, 2],
        "PARADA_PASSO_ATUAL_DESABILITA_SISTEMA_DE_AGUA":                                                    [30, 3],
        "PARADA_PASSO_ATUAL_DESABILITA_UNIDADE_LUBRIFICACAO_MANCAIS":                                       [30, 4],

        ## PARTIDA_PARADA_PASSO_CONCLUIDO
        "PARTIDA_CONCLUIDO_PASSO_HABILITA_DESAPLICA_FREIO":                                                 [33, 0],
        "PARTIDA_CONCLUIDO_PASSO_HABILITA_UNIDADE_LUBRIFICACAO":                                            [33, 1],
        "PARTIDA_CONCLUIDO_PASSO_HABILITA_SISTEMA_DE_AGUA":                                                 [33, 2],
        "PARTIDA_CONCLUIDO_PASSO_HABILITA_REGULADOR_DE_VELOCIDADE":                                         [33, 3],
        "PARTIDA_CONCLUIDO_PASSO_HABILITA_REGULADOR_DE_TENSAO":                                             [33, 4],
        "PARTIDA_CONCLUIDO_PASSO_HABILITA_SINCRONISMO":                                                     [33, 5],

        "PARADA_CONCLUIDO_PASSO_DESCARGA_POTENCIA_E_ABERTURA_DISJUNTOR":                                    [32, 0],
        "PARADA_CONCLUIDO_PASSO_DESABILITA_REGULADOR_TENSAO":                                               [32, 1],
        "PARADA_CONCLUIDO_PASSO_DESABILITA_REGULADOR_VELOCIDADE":                                           [32, 2],
        "PARADA_CONCLUIDO_PASSO_DESABILITA_SISTEMA_DE_AGUA":                                                [32, 3],
        "PARADA_CONCLUIDO_PASSO_DESABILITA_UNIDADE_LUBRIFICACAO":                                           [32, 4],

        ## PARTIDA_PARADA_PASSO_FALHA
        "PARTIDA_FALHA_PASSO_HABILITA_DESAPLICA_FREIO":                                                     [35, 0],
        "PARTIDA_FALHA_PASSO_HABILITA_UNIDADE_DE_LUBRIFICACAO":                                             [35, 1],
        "PARTIDA_FALHA_PASSO_HABILITA_SISTEMA_DE_AGUA":                                                     [35, 2],
        "PARTIDA_FALHA_PASSO_HABILITA_REGULADOR_DE_VELOCIDADE":                                             [35, 3],
        "PARTIDA_FALHA_PASSO_HABILITA_REGULADOR_DE_TENSAO":                                                 [35, 4],
        "PARTIDA_FALHA_PASSO_HABILITA_SINCRONISMO":                                                         [35, 5],

        "PARADA_FALHA_PASSO_DESCARGA_DE_POTENCIA_E_ABERTURA_DISJUNTOR_DE_MAQUINA":                          [34, 0],
        "PARADA_FALHA_PASSO_DESABILITAR_REGULADOR_DE_TENSAO":                                               [34, 1],
        "PARADA_FALHA_PASSO_DESABILITAR_REGULADOR_DE_VELOCIDADE":                                           [34, 2],
        "PARADA_FALHA_PASSO_DESABILITAR_SISTEMA_DE_AGUA":                                                   [34, 3],
        "PARADA_FALHA_PASSO_DESABILITAR_LUBRIFICACAO_DOS_MANCAIS":                                          [34, 4],

        ## UHRV
        "UHRV_UNIDADE_EM_MANUTENCAO":                                                                       [37, 0],
        "UHRV_BOMBA_1_PRINCIPAL":                                                                           [37, 1],
        "UHRV_BOMBA_2_PRINCIPAL":                                                                           [37, 2],
        "UHRV_BOMBA_1_DISPONIVEL":                                                                          [37, 3],
        "UHRV_BOMBA_2_DISPONIVEL":                                                                          [37, 4],
        "UHRV_FALHA_LIGAR_BOMBA_1":                                                                         [37, 5],
        "UHRV_FALHA_DESLIGAR_BOMBA_1":                                                                      [37, 6],
        "UHRV_FALHA_LIGAR_BOMBA_2":                                                                         [37, 7],
        "UHRV_FALHA_DESLIGAR_BOMBA_2":                                                                      [37, 8],
        "UHRV_FALHA_PRESSURIZAR_PELA_BOMBA_1":                                                              [37, 9],
        "UHRV_FALHA_PRESSURIZAR_PELA_BOMBA_2":                                                              [37, 10],
        "UHRV_APLICANDO_FREIO":                                                                             [37, 11],
        "UHRV_FALHA_PRESSURIZAR_FREIO":                                                                     [37, 12],
        "UHRV_FALHA_DESPRESSURIZAR_FREIO":                                                                  [37, 13],

        ## UHL
        "UHL_BOMBA_1_PRINCIPAL":                                                                            [39, 0],
        "UHL_BOMBA_2_PRINCIPAL":                                                                            [39, 1],
        "UHL_BOMBA_1_DISPONIVEL":                                                                           [39, 2],
        "UHL_BOMBA_2_DISPONIVEL":                                                                           [39, 3],
        "UHL_UNIDADE_EM_MANUTENCAO":                                                                        [39, 4],
        "UHL_FALHA_LIGAR_BOMBA_1":                                                                          [39, 5],
        "UHL_FALHA_DESLIGAR_BOMBA_1":                                                                       [39, 6],
        "UHL_FALHA_LIGAR_BOMBA_2":                                                                          [39, 7],
        "UHL_FALHA_DESLIGAR_BOMBA_2":                                                                       [39, 8],
        "UHL_FALHA_PRESSAO_OLEO_LINHA_PELA_BOMBA_1":                                                        [39, 9],
        "UHL_FALHA_PRESSAO_OLEO_LINHA_PELA_BOMBA_2":                                                        [39, 10],
        "UHL_FALHA_PRESSOSTATO_LINHA_DE_OLEO":                                                              [39, 11],

        ## SISTEMA_AGUA
        "SISTEMA_AGUA":                                                                                     40,

        ## AUTOMACAO_RTV
        "RV_FALHA_HABILITAR_RV":                                                                            [43, 0],
        "RV_FALHA_PARTIR_RV":                                                                               [43, 1],
        "RV_FALHA_DESABILITAR_RV":                                                                          [43, 2],
        "RV_FALHA_PARAR_MAQUINA":                                                                           [43, 3],
        "RV_FALHA_FECHAR_DISTRIBUIDOR":                                                                     [43, 4],

        "RT_FALHA_HABILITAR":                                                                               [42, 0],
        "RT_FALHA_PARTIR":                                                                                  [42, 1],
        "RT_FALHA_DESABILITAR":                                                                             [42, 2],

        ## LEITURAS_ANALÓGICAS
        "TEMP_PONTE_FASE_A":                                                                                44,
        "TEMP_GERADOR_FASE_A":                                                                              44,
        "TEMP_PONTE_FASE_B":                                                                                46,
        "TEMP_GERADOR_FASE_B":                                                                              46,
        "TEMP_PONTE_FASE_C":                                                                                48,
        "TEMP_GERADOR_FASE_C":                                                                              48,
        "TEMP_RESERVA":                                                                                     50,
        "TEMP_TRAFO_EXCITACAO":                                                                             52,
        "TEMP_MANCAL_GUIA":                                                                                 54,
        "TEMP_OLEO_UHRV":                                                                                   56,
        "TEMP_OLEO_UHL":                                                                                    58,
        "TEMP_CASQ_MANCAL_COMBINADO":                                                                       60,
        "TEMP_CONTRA_ESCORA_MANCAL_COMBINADO":                                                              62,
        "TEMP_1_PATINS_MANCAL_COMBINADO":                                                                   64,
        "TEMP_2_PATINS_MANCAL_COMBINADO":                                                                   66,
        "TEMP_1_MANCAL_GUIA_INTERNO":                                                                       68,
        "TEMP_2_MANCAL_GUIA_INTERNO":                                                                       70,
        "TEMP_GERADOR_NUCLEO_ESTATORICO":                                                                   72,
        "PRESSAO_ENTRADA_TURBINA":                                                                          84,
        "PRESSAO_REGULAGEM_1_TURBINA":                                                                      86,
        "PRESSAO_SAIDA_RODA":                                                                               88,
        "PRESSAO_SAIDA_SUCCAO":                                                                             90,
        "VIBRACAO_EIXO_X_MANCAL_COMBINADO":                                                                 92,
        "VIBRACAO_EIXO_Y_MANCAL_COMBINADO":                                                                 94,
        "VIBRACAO_EIXO_Z_MANCAL_COMBINADO":                                                                 96,
        "PRESSAO_ACUMULADOR_UHRV":                                                                          98,
        "VIBRACAO_DETECCAO_HORIZONTAL":                                                                     100,
        "VIBRACAO_DETECACAO_VERTICAL":                                                                      102,
        "PRESSAO_REGULAGEM_2_TURBINA":                                                                      104,
        "PRESSAO_DIFERENCIAL_REGULAGEM_TURBINA":                                                            106,

        ## HORÍMETROS
        "UG":                                                                                               108,
        "UHRV_B1":                                                                                          110,
        "UHRV_B2":                                                                                          112,
        "UHL_B1":                                                                                           114,
        "UHL_B2":                                                                                           116,

        ## MULTIMEDIDOR
        "VAB":                                                                                              118,
        "VBC":                                                                                              120,
        "VCA":                                                                                              122,
        "IA":                                                                                               124,
        "IB":                                                                                               126,
        "IC":                                                                                               128,
        "P":                                                                                                130,
        "Q":                                                                                                132,
        "S":                                                                                                134,
        "F":                                                                                                136,
        "FP":                                                                                               138,
        "EAP":                                                                                              138,
        "EAN":                                                                                              140,
        "ERP":                                                                                              142,
        "ERN":                                                                                              144,


        ### COMANDOS
        ## UG
        "UG_REARME_FALHA_PASSOS":                                                                           [1, 0],
        "UG_REARME_BLOQUEIO_86M":                                                                           [1, 1],
        "UG_REARME_BLOQUEIO_86E":                                                                           [1, 2],
        "UG_REARME_BLOQUEIO_86H":                                                                           [1, 3],
        "UG_COMANDO_PARADA_DE_EMERGENCIA":                                                                  [1, 4],
        "PARTIDA_UG_HABILITA_DESAPLICAR_FREIO":                                                             [1, 5],
        "PARTIDA_UG_HABILITA_UNIDADE_DE_LUBRIFICACAO_DOS_MANCAIS":                                          [1, 6],
        "PARTIDA_UG_HABILITA_SISTEMA_DE_AGUA":                                                              [1, 7],
        "PARTIDA_UG_HABILITA_REGULADOR_DE_VELOCIDADE":                                                      [1, 8],
        "PARTIDA_UG_HABILITA_REGULADOR_DE_TENSAO":                                                          [1, 9],
        "PARTIDA_UG_HABILITA_SINCRONISMO":                                                                  [1, 10],
        "PARADA_UG_HABILITA_DESCARGA_POTENCIA_E_ABERTURA_DISJUNTOR_MAQUINA":                                [1, 11],
        "PARADA_UG_DESABILITA_REGULADOR_DE_TENSAO":                                                         [1, 12],
        "PARADA_UG_DESABILITA_REGULADOR_DE_VELOCIDADE":                                                     [1, 13],
        "PARADA_UG_DESABILITA_SISTEMA_DE_AGUA":                                                             [1, 14],
        "PARADA_UG_DESABILITA_UNIDADES_DE_LUBRIFICACAO":                                                    [1, 15],

        "UG_HABILITA_CONTROLE_DE_POTENCIA_POR_NIVEL":                                                       [0, 0],
        "UG_DESABILITA_CONTROLE_DE_POTENCIA_POR_NIVEL":                                                     [0, 1],
        "UG_HABILITA_CONTROLE_DE_POTENCIA_POR_NIVEL_ESCALONADO":                                            [0, 2],
        "UG_DESABILITA_CONTROLE_DE_POTENCIA_POR_NIVEL_ESCALONADO":                                          [0, 3],
        "UG_HABILITA_PARADA_DA_UNIDADE_POR_NIVEL":                                                          [0, 4],
        "UG_DESABILITA_PARADA_DA_UNIDADE_POR_NIVEL":                                                        [0, 5],
        "UG_RESET_HORIMETRO_DA_UNIDADE":                                                                    [0, 6],

        ## UNIDADES_HIDRAULICAS
        "UHRV_RESET_FALHAS":                                                                                [3, 0],
        "UHRV_SELECIONA_OPERACAO_AUTOMATICA":                                                               [3, 1],
        "UHRV_SELECIONA_OPERACAO_EM_MANUTENCAO":                                                            [3, 2],
        "UHRV_LIGA_BOMBA_1_MANUAL":                                                                         [3, 3],
        "UHRV_DESLIGA_BOMBA_1_MANUAL":                                                                      [3, 4],
        "UHRV_LIGA_BOMBA_2_MANUAL":                                                                         [3, 5],
        "UHRV_DESLIGA_BOMBA_2_MANUAL":                                                                      [3, 6],
        "UHRV_SELECIONA_BOMBA_1_PRINCIPAL":                                                                 [3, 7],
        "UHRV_SELECIONA_BOMBA_2_PRINCIPAL":                                                                 [3, 8],
        "UHRV_RESET_HORIMETRO_BOMBA_1":                                                                     [3, 9],
        "UHRV_RESET_HORIMETRO_BOMBA_2":                                                                     [3, 10],

        "UHL_RESET_FALHAS":                                                                                 [2, 0],
        "UHL_SELECIONA_OPERACAO_AUTOMATICA":                                                                [2, 1],
        "UHL_SELECIONA_OPERACAO_EM_MANUTENCAO":                                                             [2, 2],
        "UHL_LIGA_BOMBA_1_MANUAL":                                                                          [2, 3],
        "UHL_DESLIGA_BOMBA_1_MANUAL":                                                                       [2, 4],
        "UHL_LIGA_BOMBA_2_MANUAL":                                                                          [2, 5],
        "UHL_DESLIGA_BOMBA_2_MANUAL":                                                                       [2, 6],
        "UHL_SELECIONA_BOMBA_1_PRINCIPAL":                                                                  [2, 7],
        "UHL_SELECIONA_BOMBA_2_PRINCIPAL":                                                                  [2, 8],
        "UHL_RESET_HORIMETRO_BOMBA_1":                                                                      [2, 9],
        "UHL_RESET_HORIMETRO_BOMBA_2":                                                                      [2, 10],

        ## COMANDOS_ANALÓGICOS
        "SP_NIVEL_MAX":                                                                                     4,
        "SP_NIVEL_4":                                                                                       6,
        "SP_NIVEL_3":                                                                                       8,
        "SP_NIVEL_2":                                                                                       10,
        "SP_NIVEL_1":                                                                                       12,
        "SP_NIVEL_PARADA":                                                                                  14,
        "SP_POTENCIA_MAX":                                                                                  16,
        "SP_POTENCIA_4":                                                                                    18,
        "SP_POTENCIA_3":                                                                                    20,
        "SP_POTENCIA_2":                                                                                    22,
        "SP_POTENCIA_1":                                                                                    24,


        ### RV
        ## ROTAÇÃO
        "RV_ROTACAO":                                                                                       16,

        ## ESTADO_OPERAÇÃO
        "RV_ESTADO_OPERACAO_PROCESSANDO":                                                                   [21, 0],
        "RV_ESTADO_OPERACAO_PARADA_FINALIZADA":                                                             [21, 1],
        "RV_ESTADO_OPERACAO_INICIO_PARTIDA":                                                                [21, 2],
        "RV_ESTADO_OPERACAO_PRIMEIRO_ESTAGIO_PARTIDA":                                                      [21, 3],
        "RV_ESTADO_OPERACAO_SEGUNDO_ESTAGIO_PARTIDA":                                                       [21, 4],
        "RV_ESTADO_OPERACAO_CONTROLANDO_ABERTURA":                                                          [21, 5],
        "RV_ESTADO_OPERACAO_CONTROLANDO_VELOCIDADE":                                                        [21, 6],
        "RV_ESTADO_OPERACAO_CONTROLANDO_EM_DROOP":                                                          [21, 7],
        "RV_ESTADO_OPERACAO_CONTROLANDO_EM_DROOP_EXTERNO":                                                  [21, 8],
        "RV_ESTADO_OPERACAO_CONTROLANDO_POTENCIA":                                                          [21, 9],
        "RV_ESTADO_OPERACAO_CONTROLANDO_POTENCIA_POR_REFERENCIA_ANALOGICA":                                 [21, 10],
        "RV_ESTADO_OPERACAO_CONTROLANDO_NIVEL":                                                             [21, 11],
        "RV_ESTADO_OPERACAO_ZERANDO_CARGA":                                                                 [21, 12],
        "RV_ESTADO_OPERACAO_PARANDO":                                                                       [21, 13],
        "RV_ESTADO_OPERACAO_CONTROLE_MANUAL_DISTRIBUIDOR":                                                  [21, 14],
        "RV_ESTADO_OPERACAO_CONTROLE_MANUAL_ROTOR":                                                         [21, 15],

        "RV_ESTADO_OPERACAO_EMERGENCIA":                                                                    [22, 0],

        ## CONTROLE_SINCRONIZADO_SELECIONADO
        "RV_CONTROLE_SINCRONIZADO_SELECIONADO":                                                             23,

        ## ENTRADAS_DIGITAIS
        "RV_ENTRADA_DIGITAL_SEM_BLOQUEIO_EXTERNO":                                                          [25, 0],
        "RV_ENTRADA_DIGITAL_HABILITA_REGULADOR":                                                            [25, 1],
        "RV_ENTRADA_DIGITAL_SELECIONA_MODO_CONTROLE_ISOLADO":                                               [25, 2],
        "RV_ENTRADA_DIGITAL_ZERA_CARGA":                                                                    [25, 3],
        "RV_ENTRADA_DIGITAL_RESET_FALHAS":                                                                  [25, 4],
        "RV_ENTRADA_DIGITAL_INCREMENTA_REFERENCIA_CONTROLE":                                                [25, 5],
        "RV_ENTRADA_DIGITAL_DECREMENTA_REFERENCIA_CONTROLE":                                                [25, 6],
        "RV_ENTRADA_DIGITAL_DISJUNTOR_MAQUINA_FECHADO":                                                     [25, 7],
        "RV_ENTRADA_DIGITAL_PROGRAMAVEL_1":                                                                 [25, 8],
        "RV_ENTRADA_DIGITAL_PROGRAMAVEL_2":                                                                 [25, 9],
        "RV_ENTRADA_DIGITAL_PROGRAMAVEL_3":                                                                 [25, 10],
        "RV_ENTRADA_DIGITAL_PROGRAMAVEL_4":                                                                 [25, 11],
        
        ## SAÍDAS_DIGITAIS
        "RV_SAIDA_DIGITAL_RELE_TRIP_NAO_ATUADO":                                                            [26, 0],
        "RV_SAIDA_DIGITAL_RELE_ALARME_ATUADO":                                                              [26, 1],
        "RV_SAIDA_DIGITAL_RELE_REGULADOR_HABILITADO":                                                       [26, 2],
        "RV_SAIDA_DIGITAL_RELE_REGULADOR_REGULANDO":                                                        [26, 3],
        "RV_SAIDA_DIGITAL_RELE_POTENCIA_NULA":                                                              [26, 4],
        "RV_SAIDA_DIGITAL_RELE_MAQUINA_PARADA":                                                             [26, 5],
        "RV_SAIDA_DIGITAL_RELE_VELOCIDADE_MENOR_30_PORCENTO":                                               [26, 6],
        "RV_SAIDA_DIGITAL_RELE_VELOCIDADE_MAIOR_90_PORCENTO":                                               [26, 7],
        "RV_SAIDA_DIGITAL_RELE_DISTRIBUIDOR_ABERTO":                                                        [26, 8],
        "RV_SAIDA_DIGITAL_RELE_SAIDA_PROGRAMAVEL_2":                                                        [26, 9],
        "RV_SAIDA_DIGITAL_SEGUIDOR_1":                                                                      [26, 10],
        "RV_SAIDA_DIGITAL_SEGUIDOR_2":                                                                      [26, 11],

        ## LIMITES_OPERAÇÃO
        "RV_LIMITADOR_SUPERIOR_DISTRIBUIDOR_ATUADO":                                                        [27, 0],
        "RV_LIMITADOR_INFERIOR_DISTRIBUIDOR_ATUADO":                                                        [27, 1],
        "RV_LIMITADOR_SUPERIOR_ROTOR_ATUADO":                                                               [27, 2],
        "RV_LIMITADOR_INFERIOR_ROTOR_ATUADO":                                                               [27, 3],
        "RV_LIMITADOR_SUPERIOR_VELOCIDADE_ATUADO":                                                          [27, 4],
        "RV_LIMITADOR_INFERIOR_VELOCIDADE_ATUADO":                                                          [27, 5],
        "RV_LIMITADOR_SUPERIOR_POTENCIA_ATUADO":                                                            [27, 6],
        "RV_LIMITADOR_INFERIOR_POTENCIA_ATUADO":                                                            [27, 7],

        ## SETPOINTS/REFERENCIA/FEEDBACK
        "RV_SETPOINT_VELOCIDADE":                                                                           29,
        "RV_SETPOINT_POTENCIA_ATIVA_KW":                                                                    30,
        "RV_SETPOINT_POTENCIA_ATIVA_PU":                                                                    30,
        "RV_SAIDA_CONTROLE_DISTRIBUIDOR_PU":                                                                32,
        "RV_SAIDA_CONTROLE_ROTOR_PU":                                                                       33,
        "RV_REFERENCIA_DISTRIBUIDOR_PU":                                                                    36,
        "RV_FEEDBACK_DISTRIBUIDOR_PU":                                                                      37,
        "RV_REFERENCIA_ROTOR_PU":                                                                           42,
        "RV_FEEDBACK_ROTOR_PU":                                                                             43,
        "RV_REFERENCIA_VELOCIDADE_PU":                                                                      48,
        "RV_FEEDBACK_VELOCIDADE_PU":                                                                        49,
        "RV_REFERENCIA_POTENCIA_ATIVA_PU":                                                                  54,
        "RV_FEEDBACK_POTENCIA_ATIVA_PU":                                                                    55,

        ## ALARME
        "RV_ALARME_SOBREFREQUENCIA":                                                                        [66, 0],
        "RV_ALARME_SUBFREQUENCIA":                                                                          [66, 1],
        "RV_ALARME_LEITURA_POSICAO_DISTRIBUIDOR":                                                           [66, 2],
        "RV_ALARME_LEITURA_POSICAO_ROTOR":                                                                  [66, 3],
        "RV_ALARME_LEITURA_POTENCIA_ATIVA":                                                                 [66, 4],
        "RV_ALARME_LEITURA_REFERENCIA_POTENCIA":                                                            [66, 5],
        "RV_ALARME_LEITURA_NIVEL_MONTANTE":                                                                 [66, 6],
        "RV_ALARME_NIVEL_MONTANTE_MUITO_BAIXO":                                                             [66, 7],
        "RV_ALARME_CONTROLE_POSICAO_DISTRIBUIDOR":                                                          [66, 8],
        "RV_ALARME_CONTROLE_POSICAO_ROTOR":                                                                 [66, 9],
        "RV_ALARME_RUIDO_MEDICAO_VELOCIDADE_PRINCIPAL":                                                     [66, 10],
        "RV_ALARME_RUIDO_MEDICAO_VELOCIDADE_RETAGUARDA":                                                    [66, 11],
        "RV_ALARME_PERDA_MEDICAO_VELOCIDADE_PRINCIPAL":                                                     [66, 12],
        "RV_ALARME_PERDA_MEDICAO_VELOCIDADE_RETAGUARDA":                                                    [66, 13],
        "RV_ALARME_DIFERENCA_MEDICAO_VELOCIDADE_PRINCIPAL_E_RETAGUARDA":                                    [66, 14],

        ## FALHA_1
        "RV_FALHA_SOBREFREQUENCIA_INSTANTANEA":                                                             [67, 0],
        "RV_FALHA_SOBREFREQUENCIA_TEMPORIZADA":                                                             [67, 1],
        "RV_FALHA_SUBFREQUENCIA_TEMPORIZADA":                                                               [67, 2],
        "RV_FALHA_GIRANDO_SEM_REGULACAO_OU_GIRO_INDEVIDO":                                                  [67, 3],
        "RV_FALHA_LEITURA_POSICAO_DISTRIBUIDOR":                                                            [67, 4],
        "RV_FALHA_LEITURA_POSICAO_ROTOR":                                                                   [67, 5],
        "RV_FALHA_LEITURA_POTENCIA_ATIVA":                                                                  [67, 6],
        "RV_FALHA_LEITURA_REFERENCIA_POTENCIA":                                                             [67, 7],
        "RV_FALHA_LEITURA_NIVEL_MONTANTE":                                                                  [67, 8],
        "RV_FALHA_RESERVA":                                                                                 [67, 9],
        "RV_FALHA_NIVEL_MONTANTE_MUITO_BAIXO":                                                              [67, 10],
        "RV_FALHA_CONTROLE_POSICAO_DISTRIBUIDOR":                                                           [67, 11],
        "RV_FALHA_CONTROLE_POSICAO_ROTOR":                                                                  [67, 12],
        "RV_FALHA_RUIDO_MEDICAO_VELOCIDADE_PRINCIPAL":                                                      [67, 13],
        "RV_FALHA_RUIDO_MEDICAO_VELOCIDADE_RETAGUARDA":                                                     [67, 14],
        "RV_FALHA_PERDA_MEDICAO_VELOCIDADE_PRINCIPAL":                                                      [67, 15],

        ## FALHA_2
        "RV_FALHA_PERDA_MEDICAO_VELOCIDADE_RETAGUARDA":                                                     [68, 0],
        "RV_FALHA_TEMPO_EXCESSIVO_PARTIDA":                                                                 [68, 1],
        "RV_FALHA_TEMPO_EXCESSIVO_PARADA":                                                                  [68, 2],
        "RV_FALHA_BLOQUEIO_EXTERNO":                                                                        [68, 3],
        "RV_FALHA_DIFERENCIA_MEDICAO_VELOCIDADE_PRINCIPAL_E_RETAGUARDA":                                    [68, 4],

        ## LEITURAS_ANALÓGICAS
        "RV_POTENCIA_APARENTE_NOMINAL":                                                                     79,
        "RV_POTENCIA_ATIVA_NOMINAL":                                                                        80,
        "RV_CONTROLE_1":                                                                                    85,
        "RV_CONTROLE_2":                                                                                    86,


        ### RT
        ## LEITURAS_ANALÓGICAS
        "RT_CORRENTE_EXCITACAO":                                                                            16,
        "RT_TENSAO_EXCITACAO":                                                                              17,
        "RT_TEMPERATURA_ROTOR":                                                                             25,

        ## ESTADO_OPERAÇÃO
        "RT_ESTADO_OPERACAO_PROCESSANDO":                                                                   [26, 0],
        "RT_ESTADO_OPERACAO_PARADA_FINALIZADA":                                                             [26, 1],
        "RT_ESTADO_OPERACAO_PRE_EXCITANDO":                                                                 [26, 2],
        "RT_ESTADO_OPERACAO_EXCITANDO":                                                                     [26, 3],
        "RT_ESTADO_OPERACAO_ESTABILIZANDO":                                                                 [26, 4],
        "RT_ESTADO_OPERACAO_CONTROLANDO_CORRENTE_EXCITACAO":                                                [26, 5],
        "RT_ESTADO_OPERACAO_CONTROLANDO_TENSAO_TERMINAL":                                                   [26, 6],
        "RT_ESTADO_OPERACAO_CONTROLANDO_EM_DROOP_POTENCIA_REATIVA":                                         [26, 7],
        "RT_ESTADO_OPERACAO_CONTROLANDO_EM_DROOP_FATOR_DE_POTENCIA":                                        [26, 8],
        "RT_ESTADO_OPERACAO_CONTROLANDO_POTENCIA_REATIVA":                                                  [26, 9],
        "RT_ESTADO_OPERACAO_CONTROLANDO_FATOR_DE_POTENCIA":                                                 [26, 10],
        "RT_ESTADO_OPERACAO_ZERANDO_CARGA":                                                                 [26, 11],
        "RT_ESTADO_OPERACAO_PARANDO":                                                                       [26, 12],
        "RT_ESTADO_OPERACAO_DISPARO_MANUAL_PONTE":                                                          [26, 13],
        "RT_ESTADO_OPERACAO_EMERGENCIA":                                                                    [26, 14],

        ## CONTROLE_SINCRONIZADO_SELECIONADO
        "RT_CONTROLE_SINCRONIZADO_SELECIONADO":                                                             27,

        ## ENTRADAS_DIGITAIS
        "RT_ENTRADA_DIGITAL_SEM_BLOQUEIO_EXTERNO":                                                          [30, 0],
        "RT_ENTRADA_DIGITAL_HABILITA_REGULADOR":                                                            [30, 1],
        "RT_ENTRADA_DIGITAL_SELECIONA_MODO_CONTROLE_ISOLADO":                                               [30, 2],
        "RT_RV_ENTRADA_DIGITAL_DRIVE_EXCITACAO_HABILITADO_LOGICA_DE_DISPARO":                               [30, 3],
        "RT_RV_ENTRADA_DIGITAL_RESET_FALHAS":                                                               [30, 4],
        "RT_ENTRADA_DIGITAL_INCREMENTA_REFERENCIA_CONTROLE":                                                [30, 5],
        "RT_ENTRADA_DIGITAL_DECREMENTA_REFERENCIA_CONTROLE":                                                [30, 6],
        "RT_ENTRADA_DIGITAL_DISJUNTOR_MAQUINA_FECHADO":                                                     [30, 7],
        "RT_ENTRADA_DIGITAL_CONTATOR_CAMPO_FECHADO":                                                        [30, 8],
        "RT_ENTRADA_DIGITAL_CROWBAR_INATIVO":                                                               [30, 9],
        "RT_ENTRADA_DIGITAL_PROGRAMAVEL_1":                                                                 [30, 10],
        "RT_ENTRADA_DIGITAL_PROGRAMAVEL_2":                                                                 [30, 11],

        ## SAÍDAS_DIGITAIS
        "RT_SAIDA_DIGITAL_RELE_TRIP_NAO_ATUADO":                                                            [31, 0],
        "RT_SAIDA_DIGITAL_RELE_ALARME_ATUADO":                                                              [31, 1],
        "RT_SAIDA_DIGITAL_RELE_REGULADOR_HABILITADO":                                                       [31, 2],
        "RT_SAIDA_DIGITAL_RELE_REGULADOR_REGULANDO":                                                        [31, 3],
        "RT_SAIDA_DIGITAL_RELE_HABILITA_DRIVE_EXCITACAO_LOGICA_DISPARO":                                    [31, 4],
        "RT_SAIDA_DIGITAL_RELE_HABILITA_CONTATOR_CAMPO":                                                    [31, 5],
        "RT_SAIDA_DIGITAL_RELE_HABILITA_PRE_EXCITACAO":                                                     [31, 6],
        "RT_SAIDA_DIGITAL_RELE_HABILITA_CROWBAR":                                                           [31, 7],
        "RT_SAIDA_DIGITAL_RELE_SAIDA_PROGRAMAVEL_1":                                                        [31, 8],
        "RT_SAIDA_DIGITAL_RELE_SAIDA_PROGRAMAVEL_2":                                                        [31, 9],
        "RT_SAIDA_DIGITAL_SEGUIDOR_1":                                                                      [31, 10],
        "RT_SAIDA_DIGITAL_SEGUIDOR_2":                                                                      [31, 11],

        ## LIMITIES_OPERAÇÃO
        "RT_LIMITADOR_SUPERIOR_CORRENTE_EXCITACAO_ATUADO":                                                  [32, 0],
        "RT_LIMITADOR_INFERIOR_CORRENTE_EXCITACAO_ATUADO":                                                  [32, 1],
        "RT_LIMITADOR_SUPERIOR_TENSAO_TERMINAL_ATUADO":                                                     [32, 2],
        "RT_LIMITADOR_INFERIOR_TENSAO_TERMINAL_ATUADO":                                                     [32, 3],
        "RT_LIMITADOR_SUPERIOR_POTENCIA_REATIVA_ATUADO":                                                    [32, 4],
        "RT_LIMITADOR_INFERIOR_POTENCIA_REATIVA_ATUADO":                                                    [32, 5],
        "RT_LIMITADOR_SUPERIOR_FATOR_DE_POTENCIA_ATUADO":                                                   [32, 6],
        "RT_LIMITADOR_INFERIOR_FATOR_DE_POTENCIA_ATUADO":                                                   [32, 7],
        "RT_LIMITADOR_VOLTZ_HERZ_ATUADO":                                                                   [32, 12],
        "RT_LIMITADOR_ABERTURA_PONTE_ATUADO":                                                               [32, 13],
        "RT_LIMITADOR_PQ_ATUADO_RELACAO_POTENCIA_ATIVA_X_POTENCIA_REATIVA":                                 [32, 14],

        ## SETPOINTS/REFERENCIA/FEEDBACK
        "RT_SETPOINT_TENSAO_PU":                                                                            40,
        "RT_SETPOINT_POTENCIA_REATIVA_KVAR":                                                                41,
        "RT_SETPOINT_POTENCIA_REATIVA_PU":                                                                  41,
        "RT_SETPOINT_FATOR_POTENCIA_PU":                                                                    42,
        "RT_ABERTURA_PONTE":                                                                                43,
        "RT_REFERENCIA_CORRENTE_CAMPO_PU":                                                                  46,
        "RT_FEEDBACK_CORRENTE_CAMPO_PU":                                                                    47,
        "RT_REFERENCIA_TENSAO_PU":                                                                          52,
        "RT_FEEDBACK_TENSAO_PU":                                                                            53,
        "RT_REFERENCIA_POTENCIA_REATIVA_PU":                                                                58,
        "RT_FEEDBACK_POTENCIA_REATIVA_PU":                                                                  59,
        "RT_REFERENCIA_FATOR_POTENCIA_PU":                                                                  64,
        "RT_FEEDBACK_FATOR_POTENCIA_PU":                                                                    65,

        ## ALARMES_1
        "RT_ALARME_SOBRETENSAO":                                                                            [70, 0],
        "RT_ALARME_SUBTENSAO":                                                                              [70, 1],
        "RT_ALARME_SOBREFREQUENCIA":                                                                        [70, 2],
        "RT_ALARME_SUBFREQUENCIA":                                                                          [70, 3],
        "RT_ALARME_LIMITE_SUPERIOR_POTENCIA_REATIVA_ULTRAPASSADO":                                          [70, 4],
        "RT_ALARME_LIMITE_INFERIOR_POTENCIA_REATIVA_ULTRAPASSADO":                                          [70, 5],
        "RT_ALARME_LIMITE_SUPERIOR_FATOR_DE_POTENCIA_ULTRAPASSADO":                                         [70, 6],
        "RT_ALARME_LIMITE_INFERIOR_FATOR_DE_POTENCIA_ULTRAPASSADO":                                         [70, 7],
        "RT_ALARME_VARIACAO_DE_TENSAO":                                                                     [70, 8],
        "RT_ALARME_POTENCIA_ATIVA_REVERSA":                                                                 [70, 9],
        "RT_ALARME_SOBRECORRENTE_TERMINAL":                                                                 [70, 10],
        "RT_ALARME_LIMITE_SUPERIOR_CORRENTE_EXCITACAO_ULTRAPASSADO":                                        [70, 11],
        "RT_ALARME_LIMITE_INFERIOR_CORRENTE_EXCITACAO_ULTRAPASSADO":                                        [70, 12],
        "RT_ALARME_TEMPERATURA_MUITO_ALTA_ROTOR":                                                           [70, 13],
        "RT_ALARME_PRESENCA_DE_TENSAO_TERMINAL_COM_AUSENCIA_DE_CORRENTE_DE_EXCITACAO":                      [70, 14],
        "RT_ALARME_PRESENCA_DE_CORRENTE_DE_EXCITACAO_COM_AUXENCIA_DE_TENSAO_TERMINAL":                      [70, 15],
        
        ## ALARMES_2
        "RT_ALARME_FALHA_CONTROLE_CORRENTE_EXCITACAO":                                                      [71, 0],
        "RT_ALARME_FALHA_CONTROLE_TENSAO_TERMINAL":                                                         [71, 1],
        "RT_ALARME_CROWBAR_ATUADO_COM_REGULADOR_HABILITADO":                                                [71, 2],
        "RT_ALARME_FALHA_HABILITAR_DRIVE_DE_EXCITACAO_LOGICA_DE_DISPARO":                                   [71, 3],
        "RT_ALARME_FALHA_FECHAR_CONTATOR_DE_CAMPO":                                                         [71, 4],
        "RT_ALARME_FALHA_DE_CORRENTE_DE_EXCITACAO_COM_PRE_EXCITACAO_ATIVA":                                 [71, 5],
        "RT_ALARME_PERDA_MEDICAO_POTENCIA_REATIVA":                                                         [71, 6],
        "RT_ALARME_PERDA_MEDICAO_TENSAO_TERMINAL":                                                          [71, 7],
        "RT_ALARME_PERDA_MEDICAO_CORRENTE_EXCITACAO":                                                       [71, 8],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_REATIVO":                                                        [71, 9],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_TENSAO":                                                         [71, 10],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_PRINCIPAL":                                            [71, 11],
        "RT_ALARME_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_RETAGUARDA":                                           [71, 12],

        ## FALHAS_1
        "RT_FALHA_SOBRETENSAO":                                                                             [72, 0],
        "RT_FALHA_SUBTENSAO":                                                                               [72, 1],
        "RT_FALHA_SOBREFREQUENCIA":                                                                         [72, 2],
        "RT_FALHA_SUBFREQUENCIA":                                                                           [72, 3],
        "RT_FALHA_LIMITE_SUPERIOR_POTENCIA_REATIVA_ULTRAPASSADO":                                           [72, 4],
        "RT_FALHA_LIMITE_INFERIOR_POTENCIA_REATIVA_ULTRAPASSADO":                                           [72, 5],
        "RT_FALHA_LIMITE_SUPERIOR_FATOR_DE_POTENCIA_ULTRAPASSADO":                                          [72, 6],
        "RT_FALHA_LIMITE_INFERIOR_FATOR_DE_POTENCIA_ULTRAPASSADO":                                          [72, 7],
        "RT_FALHA_SOBRETENSAO_INSTANTANEA":                                                                 [72, 8],
        "RT_FALHA_VARIACAO_DE_TENSAO":                                                                      [72, 9],
        "RT_FALHA_POTENCIA_ATIVA_REVERSA":                                                                  [72, 10],
        "RT_FALHA_SOBRECORRENTE_TERMINAL":                                                                  [72, 11],
        "RT_FALHA_LIMITE_SUPERIOR_CORRENTE_EXCITACAO_ULTRAPASSADO":                                         [72, 12],
        "RT_FALHA_LIMITE_INFERIOR_CORRENTE_EXCITACAO_ULTRAPASSADO":                                         [72, 13],
        "RT_FALHA_LIMITE_SUPERIOR_TENSAO_EXCITACAO_ULTRAPASSADO":                                           [72, 14],
        "RT_FALHA_LIMITE_INFERIOR_TENSAO_EXCITACAO_ULTRAPASSADO":                                           [72, 15],

        ## FALHAS_2
        "RT_FALHA_TEMPERATURA_MUITO_ALTA_ROTOR":                                                            [73, 0],
        "RT_FALHA_PRESENCA_DE_TENSAO_TERMINAL_COM_AUSENCIA_DE_CORRENTE_DE_EXCITACAO":                       [73, 1],
        "RT_FALHA_PRESENCA_DE_CORRENTE_DE_EXCITACAO_COM_AUXENCIA_DE_TENSAO_TERMINAL":                       [73, 2],
        "RT_FALHA_FALHA_CONTROLE_CORRENTE_EXCITACAO":                                                       [73, 3],
        "RT_FALHA_FALHA_CONTROLE_TENSAO_TERMINAL":                                                          [73, 4],
        "RT_FALHA_CROWBAR_ATUADO_COM_REGULADOR_HABILITADO":                                                 [73, 5],
        "RT_FALHA_FALHA_HABILITAR_DRIVE_DE_EXCITACAO_LOGICA_DE_DISPARO":                                    [73, 6],
        "RT_ALAME_FALHA_FECHAR_CONTATOR_DE_CAMPO":                                                          [73, 7],
        "RT_FALHA_FALHA_DE_CORRENTE_DE_EXCITACAO_COM_PRE_EXCITACAO_ATIVA":                                  [73, 8],
        "RT_FALHA_TEMPO_EXCESSIVO_DE_PRE_EXCITACAO":                                                        [73, 9],
        "RT_FALHA_TEMPO_EXCESSIVO_DE_PARADA":                                                               [73, 10],
        "RT_FALHA_TEMPO_EXCESSIVO_DE_PARTIDA":                                                              [73, 11],
        "RT_FALHA_BLOQUEIO_EXTERNO":                                                                        [73, 12],

        "RT_FALHA_PERDA_MEDICAO_POTENCIA_REATIVA":                                                          [74, 0],
        "RT_FALHA_PERDA_MEDICAO_TENSAO_TERMINAL":                                                           [74, 1],
        "RT_FALHA_PERDA_MEDICAO_CORRENTE_EXCITACAO_PRINCIPAL":                                              [74, 2],
        "RT_FALHA_PERDA_MEDICAO_CORRENTE_EXCITACAO_RETAGUARDA":                                             [74, 3],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_REATIVO":                                                         [74, 4],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_TENSAO":                                                          [74, 5],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_PRINCIPAL":                                             [74, 6],
        "RT_FALHA_RUIDO_INSTRUMENTACAO_DE_EXCITACAO_RETAGUARDA":                                            [74, 7],

        ## LEITURAS_ANALÓGICAS
        "RT_TENSAO_NOMINAL":                                                                                85,
        "RT_CONTROLE_1":                                                                                    90,
        "RT_CONTROLE_2":                                                                                    91,
    },
}