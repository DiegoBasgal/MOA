"""
Documentação do Mapa de Registradores:

## NOMES / NOMES CHAVE:

- Bay: BAY
- Subestação: SE
- Tomada da Água: TDA
- Comporta: CP1 - CP2
- Serviço Auxiliar: SA
- Unidade Geração: UG1 - UG2

- Limpa Grades: LG
- Seccionadora: SECC
- Válvula Borboleta: VB
- Grupo Motor Gerador: GMG
- Transformador Elevador: TE
- Disjuntor: DJ - DJL - DJA - DJ1 ...
- Unidade Hidráulica: UH - UHL - UHRV - UHLM ...

- Nível: NV
- Tensão: LT
- Potência: POT
- Elemento: ELE
- Alimentação: ALIM
- Enrolamento: ENRO
- Retificador: RETI
- Subtensão: SUBTEN
- Subfrequência: SUBFRE
- Sobretensão: SOBRETEN
- Sobrecorrente: SOBRECO
- Sobrefrequência: SOBREFRE

- Sistema: SIS
- Leitura: LER
- Positiva: POS
- Negativa: NEG
- Primário: PRI
- Disparo: DISP
- Dreangem: DREN
- Filtragem: FILT
- Supervisão: SUP
- Secundário: SEC
- Sequência: SEQU
- Diferencial: DIF
- Instantânea: INST
- Temporizada: TEMPO
- Discrepância: DICRE
- Transferência: TRANS

## FLAGS:
- Trip: TRP
- Falha: FLH
- Reset: RST
- Alarme: ALM
- Comando: CMD
- Operação: OPE
- Bloqueio: BLQ
- Temperatura: TMP
- Identificação: ID


-> O Padrão para nomear os registradores segue da seguinte forma (Dependendo do sentido do nome do Registrador, a ordem pode mudar):
    "Nome / Nome Chave"_"Flag"_"Descrição"

-> Exemplos:
  - LG_FLH_ATUADA
  - CP1_NV_JUSANTE
  - NV_MONTANTE_FLH
  - DJL_FLH_ABERTURA
  - DJL_FLH_CMD_ABERTURA

-> Caso o Registrador possua o mesmo nome que outro, porém seu diferencial é o BIT que é acessado,
será adicionado a letra "B" + o número do BIT no final do nome:
    "Nome / Nome Chave"_"Flag"_"Descrição"_"BitN"

-> Exemplos:
    - RELE_PROTECAO_TRP_B5
    - RELE_PROTECAO_TRP_B6
"""



REG_RELE = {
    "BAY": {
        "LT_FASE_A":                                    10,
        "LT_FASE_B":                                    13,
        "LT_FASE_C":                                    16,
        "LT_VS":                                        19,

        "RELE_RST_TRP":                                 [40, 2],

        "DJL_CMD_FECHAR":                               [43, 2],
        "DJL_MOLA_CARREGADA":                           [44, 1],
        "DJL_FLH_ABERTURA":                             [47, 1],

        "SECC_FECHADA":                                 [44, 4],

        "ID_BARRA_VIVA":                                [53, 1],
        "ID_BARRA_MORTA":                               [53, 7],
        "ID_LINHA_VIVA":                                [54, 0],
        "ID_LINHA_MORTA":                               [54, 1],
    },

    "SE": {
        "RELE_TE_FLH_PARTIDA":                          [43, 2],

        "DJL_FECHADO":                                  [43, 0],
        "DJL_FLH_ABERTURA_B3":                          [44, 3],
        "DJL_FLH_ABERTURA_B4":                          [44, 4],
        "DJL_FLH_ABERTURA_B1":                          [48, 1],

        "Z3_SOBRECO_INST_SEQU_NEG":                     [46, 1],
        "Z2_SOBRECO_INST_SEQU_NEG":                     [46, 2],
        "Z1_SOBRECO_INST_SEQU_NEG":                     [46, 3],

    },

    "TE": {
        "86T_ATUADO":                                   [36, 4],

        "ENROL_SEC_SOBRECO_TEMPO_RES":                  [37, 1],
        "ENROL_SEC_SOBRECO_TEMPO_FASE":                 [37, 6],
        "ENROL_PRI_SOBRECO_TEMPO_FASE":                 [1117, 3],
        "ENROL_PRI_SOBRECO_TEMPO_RES":                  [1117, 4],

        "DIF_COM_RESTRICAO":                            [1117, 14],
        "DIF_SEM_RESTRICAO":                            [1117, 15],

        "RELE_ESTADO_TRP":                              [1118, 15],
    },

    "UG1": {
        "ELE_2_SOBREFRE":                               [1, 4],
        "ELE_1_SOBREFRE":                               [1, 5],
        "ELE_2_SUBFRE":                                 [1, 6],
        "ELE_1_SUBFRE":                                 [1, 7],

        "RELE_PROTECAO_TRP_B5":                         [2110, 5],
        "RELE_PROTECAO_TRP_B6":                         [2110, 6],

        "SOBRECO_INST":                                 [901, 0],
        "SOBRECO_INST_NEUTRO":                          [901, 1],
        "SOBRECO_SEQU_NEG":                             [901, 2],
        "SOBRECO_TEMPO_NEUTRO":                         [901, 4],

        "DIF_COM_RESTRICAO":                            [901, 14],
        "DIF_SEM_RESTRICAO":                            [901, 15],

        "SUBTEN_GERAL":                                 [902, 0],
        "SOBRETEN_GERAL":                               [902, 1],

        "POT_REVERSA":                                  [902, 3],
        "VOLTZ_HERTZ":                                  [902, 5],

        "LT_SOBRECO_RESTRICAO":                         [902, 6],
        "RECIBO_TRANS_DISP":                            [902, 9],
        "PERDA_CAMPO_GERAL":                            [902, 11],
        "FUGA_SOBRECO_GERAL":                           [902, 12],
        "UNIDADE_FORA_PASSO":                           [902, 14],

        "DJ_MAQUINA_FLH_ABERTURA_B8":                   [902, 8],
        "DJ_MAQUINA_FLH_ABERTURA_B7":                   [2100, 7],
        "DJ_MAQUINA_FLH_PARTIDA":                       [2100, 6],

        "TE_RELE_LINHA_TRANS_DISP":                     [2100, 11],
    },

    "UG2": {
        "ELE_2_SOBREFRE":                               [1, 4],
        "ELE_1_SOBREFRE":                               [1, 5],
        "ELE_2_SUBFRE":                                 [1, 6],
        "ELE_1_SUBFRE":                                 [1, 7],

        "RELE_PROTECAO_TRP_B5":                         [2110, 5],
        "RELE_PROTECAO_TRP_B6":                         [2110, 6],

        "SOBRECO_INST":                                 [901, 0],
        "SOBRECO_INST_NEUTRO":                          [901, 1],
        "SOBRECO_SEQU_NEG":                             [901, 2],
        "SOBRECO_TEMPO_NEUTRO":                         [901, 4],

        "DIF_COM_RESTRICAO":                            [901, 14],
        "DIF_SEM_RESTRICAO":                            [901, 15],

        "SUBTEN_GERAL":                                 [902, 0],
        "SOBRETEN_GERAL":                               [902, 1],

        "POT_REVERSA":                                  [902, 3],
        "VOLTZ_HERTZ":                                  [902, 5],

        "LT_SOBRECO_RESTRICAO":                         [902, 6],
        "RECIBO_TRANS_DISP":                            [902, 9],
        "PERDA_CAMPO_GERAL":                            [902, 11],
        "FUGA_SOBRECO_GERAL":                           [902, 12],
        "UNIDADE_FORA_PASSO":                           [902, 14],

        "DJ_MAQUINA_FLH_ABERTURA_B8":                   [902, 8],
        "DJ_MAQUINA_FLH_ABERTURA_B7":                   [2100, 7],
        "DJ_MAQUINA_FLH_PARTIDA":                       [2100, 6],

        "TE_RELE_LINHA_TRANS_DISP":                     [2100, 11],
    },
}

REG_CLP = {
    "MOA": {
        "MOA_OUT_STATUS":                               409,

        "MOA_OUT_MODE":                                 11,
        "SM_STATE":                                     10,
        "PAINEL_LIDO":                                  12,
        "IN_EMERG":                                     13,
        "IN_HABILITA_AUTO":                             14,
        "IN_DESABILITA_AUTO":                           15,
        "OUT_EMERG":                                    16,

        "OUT_TARGET_LEVEL":                             417,
        "OUT_SETPOINT":                                 418,

        "IN_EMERG_UG1":                                 20,
        "OUT_BLOCK_UG1":                                21,
        "OUT_ETAPA_UG1":                                422,
        "OUT_STATE_UG1":                                423,

        "IN_EMERG_UG2":                                 25,
        "OUT_BLOCK_UG2":                                26,
        "OUT_STATE_UG2":                                427,
        "OUT_ETAPA_UG2":                                428,
    },

    "SE": {
        "LT_VAB":                                       50,
        "LT_VBC":                                       52,
        "LT_VCA":                                       53,

        "89L_FECHADA":                                  [, ],
        "86T_ATUADO":                                   [, ],
        "86BF_ATUADO":                                  [, ],
        "86T_CMD_REARME":                               [131, 1],
        "86BF_CMD_REARME":                              [131, 2],
        "86BF_86T_CMD_REARME":                          [, ],

        "REGISTROS_CMD_RST":                            [131, 5],
        "BLQ_GERAL_CMD_REARME":                         [131, 0],

        "DJL_CMD_ABRIR":                                [131, 3],
        "DJL_CMD_FECHAR":                               [131, 4],
        "DJL_MOLA_CARREGADA":                           [, ],
        "DJL_SELETORA_REMOTO":                          [, ],
        "DJL_FLH_CMD_ABERTURA":                         [, ],
        "DJL_FLH_CMD_FECHAMENTO":                       [, ],

        "RELE_LINHA_ATUADO":                            [, ],
        "RELE_LINHA_ATUACAO_BF":                        [, ],
        "RELE_SUP_BLQ_BOBINAS":                         [, ],

        "TE_RELE_ATUADO":                               [, ],
        "TE_RELE_BUCHHOLZ_TRP":                         [, ],
        "TE_RELE_BUCHHOLZ_ALM":                         [, ],

        "TE_TRP_TMP_OLEO":                              [, ],
        "TE_TRP_TMP_ENROL":                             [, ],
        "TE_TRP_ALIVIO_PRESSAO":                        [, ],

        "TE_ALM_TMP_OLEO":                              [, ],
        "TE_ALM_TMP_OLEO":                              [, ],
        "TE_ALM_TMP_ENROL":                             [, ],
        "TE_ALM_TMP_ENROL":                             [, ],

        "TE_FLH_LER_TMP_ENROL":                         [, ],
        "TE_FLH_LER_TMP_OLEO":                          [, ],

        "TE_NV_OLEO_MUITO_ALTO":                        [, ],
        "TE_NV_OLEO_MUITO_BAIXO":                       [, ],
    },

    "SA": {
        "POCO_DREN_NV_ALTO":                            [9, 0],
        "POCO_DREN_NV_MUITO_ALTO":                      [0, 9],
        "POCO_DREN_DISCRE_BOIAS":                       [13, 9],

        "RETI_SOBRETEN":                                [0, 14],
        "RETI_SUBTEN":                                  [0, 15],
        "RETI_SOBRECO_SAIDA":                           [3, 0],
        "RETI_FUSIVEL_QUEIMADO":                        [3, 2],
        "RETI_SOBRECO_BATERIAS":                        [3, 1],
        "RETI_FUGA_TERRA_POSITIVO":                     [3, 5],
        "RETI_FUGA_TERRA_NEGATIVO":                     [3, 6],

        "BOMBA_FILT_FLH":                               [1, 6],
        "BOMBA_DREN_1_FLH":                             [1, 0],
        "BOMBA_DREN_2_FLH":                             [1, 2],
        "BOMBA_DREN_3_FLH":                             [1, 4],
        "BOMBA_DREN_UNIDADES_FLH":                      [1, 12],

        "DJ52SA1_SEM_FLH":                              [2, 15],
        "DJ52SA1_FLH_ABRIR":                            [13, 0],
        "DJ52SA1_FLH_FECHAR":                           [13, 1],
        "DJ52SA2_SEM_FLH":                              [5, 1],
        "DJ52SA2_FLH_ABRIR":                            [13, 2],
        "DJ52SA2_FLH_FECHAR":                           [13, 3],
        "DJ52SA3_SEM_FLH":                              [5, 3],
        "DJ52SA3_FLH_ABRIR":                            [13, 4],
        "DJ52SA3_FLH_FECHAR":                           [13, 5],
        "DJ72SA1_FECHADO":                              [7, 10],
        "DJS_125VCC_FECHADOS":                          [7, 11],
        "DJS_24VCC_FECHADOS":                           [7, 12],
        "DJS_BARRA_SELETORA_REMOTO.":                   [5, 9],

        "SIS_INCENDIO_ALM_ATUADO":                      [7, 6],
        "SIS_SEGURANCA_ALM_ATUADO":                     [7, 7],

        "ALIM_125VCC_COM_TENSAO":                       [7, 13],
        "CMD_125VCC_COM_TENSAO":                        [7, 14],
        "CMD_24VCC_COM_TENSAO":                         [7, 15],

        "GMG_FLH_PARTIR":                               [13, 6],
        "GMG_FLH_PARAR":                                [13, 7],
        "GMG_OPERACAO_MANUAL":                          [13, 10],

        "SIS_AGUA_BOMBA_DISPONIVEL":                    [17, 0],
        "SIS_AGUA_FLH_LIGA_BOMBA":                      [17, 1],
        "SIS_AGUA_FLH_PRESSURIZAR_FILTRO_A":            [17, 3],
        "SIS_AGUA_FLH_PRESSOSTATO_FILTRO_A":            [17, 4],
        "SIS_AGUA_FLH_PRESSURIZAR_FILTRO_B":            [17, 5],
        "SIS_AGUA_FLH_PRESSOSTATO_FILTRO_B":            [17, 6],
        "SIS_AGUA_RST_FLH":                             [129, 1],

        "BARRA_CA_RST_FLH":                             [129, 0],

        "BLQ_GERAL_FLH_SA_REARME":                      [130, 0],

        # "BOMBA_RECALQUE_TUBO_SUCCAO_FALHA":             [, ],
        # "SEM_EMERGENCIA":                               [, ],
    },

    "TDA": {
        "NV_MONTANTE":                                  3,
        "NV_JUSANTE_CP1":                               36,
        "NV_JUSANTE_CP2":                               38,
        "NV_JUSANTE_GRADE_CP2_LER_FLH":                 32,
        "NV_JUSANTE_GRADE_CP1_LER_FLH":                 34,
        "NV_MONTANTE_LER_FLH":                          [3, 0],

        "SEM_EMERGENCIA":                               [16, 8],

        "CA_COM_TENSAO":                                [17, 11],

        "LG_FLH_ATUADA":                                [26, 15],
        "LG_OPE_MANUAL":                                [28, 0],

        "VB_FECHANDO":                                  [23, 0],
        "VB_CMD_RST_FLH":                               [55, 0],

        "UH_DISPONIVEL":                                [5, 1],
        "UH_FLH_LIGAR_BOMBA":                           [5, 2],
        "UH_FILTRO_LIMPO":                              [17, 13],

        "CP1_OPERANDO":                                 [2, 0],
        "CP1_AGUARDANDO_CMD_ABERTURA":                  [2, 3],
        "CP1_PRESSAO_EQUALIZADA":                       [2, 4],

        "CP1_CMD_REARME_FLH":                           [6, 0],
        "CP1_CMD_ABERTURA_CRACKING":                    [6, 1],
        "CP1_CMD_ABERTURA_TOTAL":                       [6, 2],
        "CP1_CMD_FECHAMENTO":                           [6, 3],
        "CP1_PERMISSIVOS_OK":                           [6, 15],

        "CP1_BLQ_ATUADO":                               [8, 15],

        "CP1_CRACKING":                                 [16, 0],
        "CP1_REMOTO":                                   [16, 6],

        "CP1_ABERTA":                                   [17, 14],
        "CP1_FECHADA":                                  [17, 15],

        "CP2_OPERANDO":                                 [2, 0],
        "CP2_AGUARDANDO_CMD_ABERTURA":                  [2, 3],
        "CP2_PRESSAO_EQUALIZADA":                       [2, 4],

        "CP2_CMD_REARME_FLH":                           [6, 0],
        "CP2_CMD_ABERTURA_CRACKING":                    [6, 1],
        "CP2_CMD_ABERTURA_TOTAL":                       [6, 2],
        "CP2_CMD_FECHAMENTO":                           [6, 3],
        "CP2_PERMISSIVOS_OK":                           [6, 15],

        "CP2_BLQ_ATUADO":                               [8, 15],

        "CP2_CRACKING":                                 [16, 0],
        "CP2_REMOTO":                                   [16, 6],

        "CP2_ABERTA":                                   [17, 14],
        "CP2_FECHADA":                                  [17, 15],
    },

    "UG1": {
        "P":                                            130,
        "HORIMETRO":                                    108,

        "SIS_AGUA_FLH_HAB":                             [, ],

        "RESISTENCIA_SEM_FALHA":                        [, ],

        "BT_EMERGENCIA_NAO_ATUADO":                     [, ],

        "DJS_125VCC_FECHADOS":                          [, ],
        "DJS_24VCC_FECHADOS":                           [, ],

        "CPG_PORTA_INTERNA_FECHADA":                    [, ],
        "CPG_PORTA_TRASEIRA_FECHADA":                   [, ],

        "CLP_GERAL_SIS_AGUA_OK":                        [, ],
        "CLP_GERAL_SEM_BLQ_EXTERNO":                    [, ],
        "CLP_GERAL_COM_TENSAO_BARRA_ESSEN":             [, ],

        "RELE_700G_BF_ATUADO":                          [, ],
        "RELE_700G_TRP_ATUADO":                         [, ],
        "RELE_BLQ_86EH_DESATUADO":                      [, ],

        "TRAFO_ATERRAMENTO_TRP_TMP":                    [, ],

        "TRAFO_EXCITACAO_ALM_TMP":                      [, ],
        "TRAFO_EXCITACAO_TRP_TMP":                      [, ],
        "TRAFO_EXCITACAO_FLH_LER_TMP":                  [, ],

        "UHRV_MANUTENCAO":                              [, ],
        "UHRV_BOMBA_1_FLH":                             [, ],
        "UHRV_BOMBA_2_FLH":                             [, ],
        "UHRV_FILTRO_LIMPO":                            [, ],
        "UHRV_ALM_TMP_OLEO":                            [, ],
        "UHRV_TRP_TMP_OLEO":                            [, ],
        "UHRV_FLH_LER_TMP_OLEO":                        [, ],
        "UHRV_ACUMULADOR_PRESSAO_TRP":                  [, ],
        "UHRV_CMD_REARME_FLH":                          [, ],

        "UHLM_MANUTENCAO":                              [, ],
        "UHLM_BOMBA_1_FLH":                             [, ],
        "UHLM_BOMBA_2_FLH":                             [, ],
        "UHLM_FILTRO_LIMPO":                            [, ],
        "UHLM_ALM_TMP_OLEO":                            [, ],
        "UHLM_TRP_TMP_OLEO":                            [, ],
        "UHLM_FLH_LER_TMP_OLEO":                        [, ],
        "UHLM_FLH_PRESSAO_LINHA_B1":                    [, ],
        "UHLM_FLH_PRESSAO_LINHA_B2":                    [, ],
        "UHLM_FLH_PRESSOSTATO_LINHA":                   [, ],
        "UHLM_CMD_REARME_FLH":                          [, ],

        "PARTIDA_CMD_SINCRONISMO":                      [, ],

        "PARADA_BLQ_ABERTURA_DJ":                       [, ],
        "PARADA_BLQ_DESCARGA_POT":                      [, ],
        "PARADA_CMD_EMERGENCIA":                        [, ],
        "PARADA_CMD_DESABILITA_UHLM":                   [, ],

        "86M_BLQ_ATUADO":                               [, ],
        "86M_CMD_REARME_BLQ":                           [, ],

        "86E_BLQ_ATUADO":                               [, ],
        "86E_CMD_REARME_BLQ":                           [, ],

        "86H_BLQ_ATUADO":                               [, ],
        "86H_CMD_REARME_BLQ":                           [, ],

        "SUP_TENSAO_24VCC":                             [, ],
        "SUP_TENSAO_125VCC":                            [, ],
        "SUP_BOBINA_86EH":                              [, ],
        "SUP_BOBINA_52G":                               [, ],

        "PASSOS_CMD_RST_FLH":                           [, ],

        "DISP_MECANICO_ATUADO":                         [, ],
        "DISP_MECANICO_DESATUADO":                      [, ],

        "ESCOVAS_POLO_POS_GASTAS":                      [, ],
        "ESCOVAS_POLO_NEG_GASTAS":                      [, ],

        "ENTRADA_TURBINA_PRESSAO":                      [, ],
        "ENTRADA_TURBINA_FLH_LER_PRESSAO":              [, ],

        "GERADOR_SAIDA_AR_TRP_TMP":                     [, ],

        "GERADOR_FASE_A_TMP":                           [, ],
        "GERADOR_FASE_A_ALM_TMP":                       [, ],
        "GERADOR_FASE_A_TRP_TMP":                       [, ],
        "GERADOR_FASE_A_FLH_LER_TMP":                   [, ],

        "GERADOR_FASE_B_TMP":                           [, ],
        "GERADOR_FASE_B_TRP_TMP":                       [, ],
        "GERADOR_FASE_B_ALM_TMP":                       [, ],
        "GERADOR_FASE_B_FLH_LER_TMP":                   [, ],

        "GERADOR_FASE_C_TMP":                           [, ],
        "GERADOR_FASE_C_ALM_TMP":                       [, ],
        "GERADOR_FASE_C_TRP_TMP":                       [, ],
        "GERADOR_FASE_C_FLH_LER_TMP":                   [, ],

        "GERADOR_NUCL_ESTAT_TMP":                       [, ],
        "GERADOR_NUCL_ESTAT_ALM_TMP":                   [, ],
        "GERADOR_NUCL_ESTAT_TRP_TMP":                   [, ],
        "GERADOR_NUCL_ESTAT_FLH_LER_TMP":               [, ],

        "PONTE_FASE_A_ALM_TMP":                         [, ],
        "PONTE_FASE_A_TRP_TMP":                         [, ],
        "PONTE_FASE_A_FLH_LER_TMP":                     [, ],

        "PONTE_FASE_B_ALM_TMP":                         [, ],
        "PONTE_FASE_B_TRP_TMP":                         [, ],
        "PONTE_FASE_B_FLH_LER_TMP":                     [, ],

        "PONTE_FASE_C_ALM_TMP":                         [, ],
        "PONTE_FASE_C_TRP_TMP":                         [, ],
        "PONTE_FASE_C_FLH_LER_TMP":                     [, ],

        "MANCAL_GUIA_TMP":                              [, ],
        "MANCAL_GUIA_ALM_TMP":                          [, ],
        "MANCAL_GUIA_FLH_LER_TMP":                      [, ],

        "MANCAL_CASQ_COMB_TMP":                         [, ],
        "MANCAL_CASQ_COMB_ALM_TMP":                     [, ],
        "MANCAL_CASQ_COMB_TRP_TMP":                     [, ],
        "MANCAL_CASQ_COMB_FLH_LER_TMP":                 [, ],

        "MANCAL_GUIA_INTE_1_TMP":                       [, ],
        "MANCAL_GUIA_INTE_1_ALM_TMP":                   [, ],
        "MANCAL_GUIA_INTE_1_TRP_TMP":                   [, ],
        "MANCAL_GUIA_INTE_1_FLH_LER_TMP":               [, ],

        "MANCAL_GUIA_INTE_2_TMP":                       [, ],
        "MANCAL_GUIA_INTE_2_ALM_TMP":                   [, ],
        "MANCAL_GUIA_INTE_2_TRP_TMP":                   [, ],
        "MANCAL_GUIA_INTE_2_FLH_LER_TMP":               [, ],

        "MANCAL_COMB_PATINS_1_TMP":                     [, ],
        "MANCAL_COMB_PATINS_1_ALM_TMP":                 [, ],
        "MANCAL_COMB_PATINS_1_TRP_TMP":                 [, ],
        "MANCAL_COMB_PATINS_1_FLH_LER_TMP":             [, ],

        "MANCAL_COMB_PATINS_2_TMP":                     [, ],
        "MANCAL_COMB_PATINS_2_ALM_TMP":                 [, ],
        "MANCAL_COMB_PATINS_2_TRP_TMP":                 [, ],
        "MANCAL_COMB_PATINS_2_FLH_LER_TMP":             [, ],

        "MANCAL_CONT_ESCO_COMB_TMP":                    [, ],
        "MANCAL_CONT_ESCO_COMB_ALM_TMP":                [, ],
        "MANCAL_CONT_ESCO_COMB_TRP_TMP":                [, ],
        "MANCAL_CONT_ESCO_COMB_FLH_LER_TMP":            [, ],

        "MANCAL_COMB_EIXO_X_ALM_VIBR":                  [, ],
        "MANCAL_COMB_EIXO_X_TRP_VIBR":                  [, ],
        "MANCAL_COMB_EIXO_X_FLH_LER_VIBR":              [, ],

        "MANCAL_COMB_EIXO_Y_ALM_VIBR":                  [, ],
        "MANCAL_COMB_EIXO_Y_TRP_VIBR":                  [, ],
        "MANCAL_COMB_EIXO_Y_FLH_LER_VIBR":              [, ],

        "MANCAL_COMB_EIXO_Z_ALM_VIBR":                  [, ],
        "MANCAL_COMB_EIXO_Z_TRP_VIBR":                  [, ],
        "MANCAL_COMB_EIXO_Z_FLH_LER_VIBR":              [, ],

        "DETECCAO_VERTICAL_ALM_VIBRA":                  [, ],
        "DETECCAO_VERTICAL_TRP_VIBRA":                  [, ],
        "DETECCAO_VERTICAL_FLH_LER_VIBRA":              [, ],

        "DETECCAO_HORIZONTAL_ALM_VIBRA":                [, ],
        "DETECCAO_HORIZONTAL_TRP_VIBRA":                [, ],
        "DETECCAO_HORIZONTAL_FLH_LER_VIBRA":            [, ],

        # RV
        "RV_SAIDAS_DIGITAIS":                           [, ],
        "RV_ESTADO_OPERACAO":                           [, ],
        "RV_FLH_PARTIR":                                [, ],
        "RV_FLH_HABILITAR":                             [, ],
        "RV_FLH_DESABILITAR":                           [, ],
        "RV_FLH_FECHAR_DISTRIBUIDOR":                   [, ],
        "RV_RELE_TRP_NAO_ATUADO":                       [, ],
        "RV_RELE_ALM_ATUADO":                           [, ],
        "RV_SETPOT_POT_ATIVA_PU":                       [, ],

        # RT
        "RT_SAIDAS_DIGITAIS":                           [, ],
        "RT_FLH_PARTIR":                                [, ],
        "RT_FLH_HABILITAR":                             [, ],
        "RT_FLH_DESABILITAR":                           [, ],
        "RT_RELE_TRP_NAO_ATUADO":                       [, ],

        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],
        "RV_FLH_1":                                     [, ],

        "RV_FLH_2":                                     [, ],
        "RV_FLH_2":                                     [, ],
        "RV_FLH_2":                                     [, ],
        "RV_FLH_2":                                     [, ],
        "RV_FLH_2":                                     [, ],
        "RV_FLH_2":                                     [, ],
        "RV_FLH_2":                                     [, ],
        "RV_FLH_2":                                     [, ],
        "RV_FLH_2":                                     [, ],
        "RV_FLH_2":                                     [, ],
        "RV_FLH_2":                                     [, ],

        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],
        "RT_FLH_1":                                     [, ],

        "RT_FLH_2":                                     [, ],
        "RT_FLH_2":                                     [, ],
        "RT_FLH_2":                                     [, ],
        "RT_FLH_2":                                     [, ],
        "RT_FLH_2":                                     [, ],
        "RT_FLH_2":                                     [, ],
        "RT_FLH_2":                                     [, ],

        "RT_FLH_3":                                     [, ],
        "RT_FLH_3":                                     [, ],
        "RT_FLH_3":                                     [, ],
        "RT_FLH_3":                                     [, ],
        "RT_FLH_3":                                     [, ],
        "RT_FLH_3":                                     [, ],
        "RT_FLH_3":                                     [, ],
        "RT_FLH_3":                                     [, ],

        "RT_ALM_1":                                     [, ],
        "RT_ALM_1":                                     [, ],
        "RT_ALM_1":                                     [, ],
        "RT_ALM_1":                                     [, ],
    },
}