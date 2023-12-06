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

REG_MEDIDOR = {
    "LT_P_MP":                                          33,
    "LT_P_MR":                                          33,
}

REG_RELE = {
    "BAY": {
        # Leituras Analógicas
        "LT_FASE_A":                                    11,
        "LT_FASE_B":                                    14,
        "LT_FASE_C":                                    17,
        "LT_VS":                                        19,


        # Relé
        "RELE_RST_TRP":                                 88,


        # DJ
        "DJL_CMD_ABRIR":                                84,
        "DJL_CMD_FECHAR":                               85,
        "DJL_FECHADO":                                  [44, 0],


        # DJ
        "DJL_MOLA_CARREGADA":                           [44, 1],
        # Seccionadora
        "SECC_FECHADA":                                 [44, 4],


        # DJ
        "DJL_FLH_ABERTURA":                             [47, 1],


        # Barra
        "ID_BARRA_VIVA":                                [53, 1],
        "ID_BARRA_MORTA":                               [53, 7],


        # Linha
        "ID_LINHA_VIVA":                                [54, 0],
        "ID_LINHA_MORTA":                               [54, 1],

    },

    "SE": {
        # DJ
        "DJL_FECHADO":                                  [43, 0],
        "DJL_MOLA_CARREGADA":                           [43, 1],
        # Relé
        "RELE_TE_FLH_PARTIDA":                          [43, 2],

        # Seccionadora
        "SECC_FECHADA":                                 [43, 1],


        # DJ
        "DJL_FLH_ABERTURA_B3":                          [44, 3],
        "DJL_FLH_ABERTURA_B4":                          [44, 4],


        # Zonas
        "Z3_SOBRECO_INST_SEQU_NEG":                     [46, 1],
        "Z2_SOBRECO_INST_SEQU_NEG":                     [46, 2],
        "Z1_SOBRECO_INST_SEQU_NEG":                     [46, 3],


        # DJ
        "DJL_FLH_ABERTURA_B1":                          [48, 1],


        # Barra
        "ID_BARRA_VIVA":                                [49, 1],
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
        # Leituras Analógicas
        "LT_VAB":                                       48,
        "LT_VBC":                                       50,
        "LT_VCA":                                       52,
        "P":                                            64,


        ## ENTRADAS_DIGITAIS_2 -> REGS: 3, 2

        # DJ 52L
        "DJL_FECHADO":                                  [3, 7],

        # Secc 89L
        "89L_FECHADA":                                  [3, 11],

        "TE_ALM_TMP_OLEO":                              [2, 2],
        "TE_TRP_TMP_OLEO":                              [2, 3],
        "TE_ALM_TMP_ENROL":                             [2, 4],
        "TE_TRP_TMP_ENROL":                             [2, 5],
        "TE_RELE_BUCHHOLZ_ALM":                         [2, 6],
        "TE_RELE_BUCHHOLZ_TRP":                         [2, 7],
        "TE_TRP_ALIVIO_PRESSAO":                        [2, 9],
        "TE_NV_OLEO_MUITO_BAIXO":                       [44, 6],


        ## ENTRADAS_DIGITAIS_3 -> REGS: 5, 4

        # Relé Linha
        "RELE_LINHA_ATUACAO_BF":                        [4, 0],
        "86BF_ATUADO":                                  [4, 3],

        # Relé TE
        "86T_ATUADO":                                   [5, 4],

        # DJ52l
        "DJL_SELETORA_REMOTO":                          [5, 10],
        "DJL_FLH_CMD_ABERTURA":                         [40, 1],
        "DJL_FLH_CMD_FECHAMENTO":                       [40, 2],


        ## FALHAS_ANALOGICAS

        # Transformador Elevador
        "TE_FLH_LER_TMP_ENROL":                         [11, 1],
        "TE_FLH_LER_TMP_OLEO":                          [11, 2],


        # STATUS SE

        # Relé Linha
        "RELE_LINHA_ATUADO":                            [44, 1],


        # COMANDOS

        # Rearme
        "BLQ_GERAL_FLH_SA_REARME":                      [130, 0],

        # Rearmes
        "BLQ_GERAL_CMD_REARME":                         [131, 0],
        "86T_CMD_REARME":                               [131, 1],
        "86BF_CMD_REARME":                              [131, 2],

        # DJs
        "DJL_CMD_ABRIR":                                [131, 3],
        "DJL_CMD_FECHAR":                               [131, 4],

        # Registros
        "REGISTROS_CMD_RST":                            [131, 5],

    },

    "SA": {

        ## ENTRADAS_DIGITAIS_1 -> REGS: 1, 0

        # Poço Drenagem
        "POCO_DREN_NV_MUITO_ALTO":                      [0, 9],
        "POCO_DREN_NV_ALTO":                            [0, 10],

        # Retificador
        "RETI_SOBRETEN":                                [0, 14],
        "RETI_SUBTEN":                                  [0, 15],

        # Bomba Drenagem/Filtragem
        "BOMBA_FILT_FLH":                               [1, 6],
        "BOMBA_DREN_1_FLH":                             [1, 0],
        "BOMBA_DREN_2_FLH":                             [1, 2],
        "BOMBA_DREN_3_FLH":                             [1, 4],
        "BOMBA_DREN_UNIDADES_FLH":                      [1, 12],
        "BOMBA_RECALQUE_TUBO_SUCCAO_FALHA":             [1, 12],


        ## ENTRADAS_DIGITAIS_2 -> REGS: 3, 2

        # DJs
        "DJ52SA1_SEM_FLH":                              [2, 15],

        # Retificador
        # Poço Drenagem
        "RETI_SOBRECO_SAIDA":                           [3, 0],
        "RETI_SOBRECO_BATERIAS":                        [3, 1],
        "RETI_FUSIVEL_QUEIMADO":                        [3, 2],
        "RETI_FUGA_TERRA_POSITIVO":                     [3, 5],
        "RETI_FUGA_TERRA_NEGATIVO":                     [3, 6],


        ## ENTRADAS_DIGITAIS_3 -> REGS: 5, 4

        # DJs
        "DJ52SA2_SEM_FLH":                              [5, 1],
        "DJ52SA3_SEM_FLH":                              [5, 3],
        "DJS_BARRA_SELETORA_REMOTO":                    [5, 9],

        "SUBTENSAO_CMD_SA_125VCC":                      [6, 14],


        ## ENTRADAS_DIGITAIS_4 -> REGS: 7, 6

        # Sistemas
        "SIS_INCENDIO_ALM_ATUADO":                      [7, 6],
        "SIS_SEGURANCA_ALM_ATUADO":                     [7, 7],

        # DJs
        "DJ72SA1_FECHADO":                              [7, 10],
        "DJS_125VCC_FECHADOS":                          [7, 11],
        "DJS_24VCC_FECHADOS":                           [7, 12],

        # 24/125VCC
        "ALIM_125VCC_COM_TENSAO":                       [7, 13],
        "CMD_125VCC_COM_TENSAO":                        [7, 14],
        "CMD_24VCC_COM_TENSAO":                         [7, 15],


        ## STATUS SA

        # DJs
        "DJ52SA1_FLH_ABRIR":                            [13, 0],
        "DJ52SA1_FLH_FECHAR":                           [13, 1],
        "DJ52SA2_FLH_ABRIR":                            [13, 2],
        "DJ52SA2_FLH_FECHAR":                           [13, 3],
        "DJ52SA3_FLH_ABRIR":                            [13, 4],
        "DJ52SA3_FLH_FECHAR":                           [13, 5],

        # GMG
        "GMG_FLH_PARTIR":                               [13, 6],
        "GMG_FLH_PARAR":                                [13, 7],
        "GMG_OPERACAO_MANUAL":                          [13, 10],

        "POCO_DREN_DISCRE_BOIAS":                       [13, 9],


        ## STATUS SISTEMA ÁGUA

        # Sistema Água
        "SIS_AGUA_BOMBA_DISPONIVEL":                    [17, 0],
        "SIS_AGUA_FLH_LIGA_BOMBA":                      [17, 1],
        "SIS_AGUA_FLH_PRESSURIZAR_FILTRO_A":            [17, 3],
        "SIS_AGUA_FLH_PRESSOSTATO_FILTRO_A":            [17, 4],
        "SIS_AGUA_FLH_PRESSURIZAR_FILTRO_B":            [17, 5],
        "SIS_AGUA_FLH_PRESSOSTATO_FILTRO_B":            [17, 6],

        "BLQ_GERAL":                                    [23, 15],




        ## COMANDOS

        # Barra CA
        "BARRA_CA_RST_FLH":                             [129, 0],

        # Sistema Água
        "SIS_AGUA_RST_FLH":                             [129, 1],
    },

    "TDA": {
        ## LEITURAS_ANALOGICAS

        "NV_MONTANTE":                                  30,
        "NV_JUSANTE_GRADE_CP2":                         32,
        "NV_JUSANTE_GRADE_CP1":                         34,
        "NV_JUSANTE_CP1":                               36,
        "NV_JUSANTE_CP2":                               38,


        ## ENTRADAS_DIGITAIS

        # Nível Montante
        "NV_MONTANTE_LER_FLH":                          [3, 0],
        "NV_JUSANTE_CP1_LER_FLH":                       [3, 2],
        "NV_JUSANTE_CP2_LER_FLH":                       [3, 4],
        "NV_JUSANTE_GRADE_CP1_LER_FLH":                 [3, 1],
        "NV_JUSANTE_GRADE_CP2_LER_FLH":                 [3, 3],

        # Botão Emergência
        "SEM_EMERGENCIA":                               [0, 8],

        # Tensão CA
        "CA_COM_TENSAO":                                [1, 11],

        # Unidade Hidráulica
        "UH_FILTRO_LIMPO":                              [1, 13],

        ## COMANDOS LIMPA GRADES

        "LG_CMD_RST_FLH":                               [7, 0],
        "LG_CMD_LIMPEZA":                               [7, 2],

        ## LIMPA_GRADES_PERMISSAO

        "LG_PERMISSAO":                                 [24, 15],
        "LG_PARADO":                                    [25, 3],

        ## LIMPA_GRADES_FALHAS

        "LG_FLH_ATUADA":                                [26, 15],

        ## LIMPA_GRADES_STATUS

        "LG_OPE_MANUAL":                                [29, 0],


        ## BORBOLETA_STATUS

        "VB_FECHANDO":                                  [23, 0],


        ## COMANDOS BORBOLETA

        "VB_CMD_RST_FLH":                               [55, 0],


        ## UNIDADE_HIDRAULICA

        "UH_DISPONIVEL":                                [5, 1],
        "UH_FLH_LIGAR_BOMBA":                           [5, 2],


        ### COMPORTA 1

        ## COMPORTA_1_STATUS

        "CP1_OPERANDO":                                 [11, 0],
        "CP1_AGUARDANDO_CMD_ABERTURA":                  [11, 3],
        "CP1_PRESSAO_EQUALIZADA":                       [11, 4],


        ## COMPORTA_1_BLOQUEIOS

        "CP1_BLQ_ATUADO":                               [8, 15],


        ## ENTRADAS_DIGITAIS -> REGS: 1, 0

        "CP1_CRACKING":                                 [0, 0],
        "CP1_REMOTO":                                   [0, 6],
        "CP1_ABERTA":                                   [1, 14],
        "CP1_FECHADA":                                  [1, 15],


        ## COMPORTA_1_PERMISSIVOS

        "CP1_PERMISSIVOS_OK":                           [7, 10],


        ## COMPORTA_1_COMANDOS

        "CP1_CMD_REARME_FLH":                           [51, 0],
        "CP1_CMD_ABERTURA_CRACKING":                    [51, 1],
        "CP1_CMD_ABERTURA_TOTAL":                       [51, 2],
        "CP1_CMD_FECHAMENTO":                           [51, 3],


        ### COMPORTA 2

        ## COMPORTA_2_STATUS

        "CP2_OPERANDO":                                 [17, 0],
        "CP2_AGUARDANDO_CMD_ABERTURA":                  [17, 3],
        "CP2_PRESSAO_EQUALIZADA":                       [17, 4],


        ## COMPORTA_2_PERMISSIVOS

        "CP2_PERMISSIVOS_OK":                           [12, 15],


        ## COMPORTA_2_BLOQUEIOS

        "CP2_BLQ_ATUADO":                               [15, 15],


        ## ENTRADAS_DIGITAIS -> REGS: 1, 0

        "CP2_ABERTA":                                   [0, 1],
        "CP2_FECHADA":                                  [0, 2],
        "CP2_CRACKING":                                 [0, 3],
        "CP2_REMOTO":                                   [0, 9],


        ## COMPORTA_2_COMANDOS

        "CP2_CMD_REARME_FLH":                           [53, 0],
        "CP2_CMD_ABERTURA_CRACKING":                    [53, 1],
        "CP2_CMD_ABERTURA_TOTAL":                       [53, 2],
        "CP2_CMD_FECHAMENTO":                           [53, 3],

    },

    "UG1": {

        ## LEITURAS_ANALOGICAS

        "GERADOR_FASE_A_TMP":                           44,
        "GERADOR_FASE_B_TMP":                           46,
        "GERADOR_FASE_C_TMP":                           48,
        "MANCAL_GUIA_TMP":                              54,
        "MANCAL_CASQ_COMB_TMP":                         60,
        "MANCAL_CONT_ESCO_COMB_TMP":                    62,
        "MANCAL_COMB_PATINS_1_TMP":                     64,
        "MANCAL_COMB_PATINS_2_TMP":                     66,
        "MANCAL_GUIA_INTE_1_TMP":                       68,
        "MANCAL_GUIA_INTE_2_TMP":                       70,
        "GERADOR_NUCL_ESTAT_TMP":                       72,
        "ENTRADA_TURBINA_PRESSAO":                      84,
        "GERADOR_SAIDA_AR_TRP_TMP":                     90,
        "HORIMETRO":                                    108,
        "P":                                            132,


        ## ENTRADAS_DIGITAIS_1 -> REGS 1, 0

        # UHLM
        "UHLM_FILTRO_SUJO":                             [0, 5],

        # UHRV
        "UHRV_FILTRO_SUJO":                             [0, 8],

        # Resistência
        "RESISTENCIA_FALHA":                            [0, 12],


        ## ENTRADAS_DIGITAIS_2 -> REGS 3, 2

        # Botão Emergência
        "BT_EMERGENCIA_ATUADO":                         [3, 11],

        # Supervisão
        "SUP_BOBINA_52G":                               [3, 12],
        "SUP_BOBINA_86EH":                              [3, 13],

        # Relé
        "RELE_BLQ_86EH_DESATUADO":                      [2, 12],
        "SUP_TENSAO_125VCC":                            [2, 13],
        "SUP_TENSAO_24VCC":                             [2, 14],

        # DJ
        "DJS_125VCC_FECHADOS":                          [2, 15],


        ## ENTRADAS_DIGITAIS_3 -> REGS 5, 4

        # DJ
        "DJS_24VCC_FECHADOS":                           [5, 0],

        # CLPs
        "CLP_GERAL_SEM_BLQ_EXTERNO":                    [5, 1],
        "CLP_GERAL_SIS_AGUA_OK":                        [5, 2],

        # Escovas Polo
        "ESCOVAS_POLO_POS_GASTAS":                      [5, 5],
        "ESCOVAS_POLO_NEG_GASTAS":                      [5, 6],

        # Disparo Mecânico
        "DISP_MECANICO_DESATUADO":                      [5, 8],
        "DISP_MECANICO_ATUADO":                         [5, 9],


        ## ALARMES_ANALOGICAS

        # Alarmes de Temperatura/Vibração
        "PONTE_FASE_A_ALM_TMP":                         [7, 0],
        "PONTE_FASE_B_ALM_TMP":                         [7, 1],
        "PONTE_FASE_C_ALM_TMP":                         [7, 2],
        "TRAFO_EXCITACAO_ALM_TMP":                      [7, 4],
        "MANCAL_GUIA_ALM_TMP":                          [7, 5],
        "UHRV_ALM_TMP_OLEO":                            [7, 6],
        "UHLM_ALM_TMP_OLEO":                            [7, 7],
        "MANCAL_CASQ_COMB_ALM_TMP":                     [7, 8],
        "MANCAL_CONT_ESCO_COMB_ALM_TMP":                [7, 9],
        "MANCAL_COMB_PATINS_1_ALM_TMP":                 [7, 10],
        "MANCAL_COMB_PATINS_2_ALM_TMP":                 [7, 11],
        "MANCAL_GUIA_INTE_1_ALM_TMP":                   [7, 12],
        "MANCAL_GUIA_INTE_2_ALM_TMP":                   [7, 13],
        "GERADOR_NUCL_ESTAT_ALM_TMP":                   [7, 14],
        "GERADOR_FASE_A_ALM_TMP":                       [7, 15],
        "GERADOR_FASE_B_ALM_TMP":                       [6, 0],
        "GERADOR_FASE_C_ALM_TMP":                       [6, 1],
        "MANCAL_COMB_EIXO_X_ALM_VIBR":                  [6, 8],
        "MANCAL_COMB_EIXO_Y_ALM_VIBR":                  [6, 9],
        "MANCAL_COMB_EIXO_Z_ALM_VIBR":                  [6, 10],
        "DETECCAO_HORIZONTAL_ALM_VIBRA":                [6, 12],
        "DETECCAO_VERTICAL_ALM_VIBRA":                  [6, 13],


        ## FALHAS_ANALOGICAS

        # Falhas de Leitura de Pressão/Vibração
        "ENTRADA_TURBINA_FLH_LER_PRESSAO":              [8, 4],
        "MANCAL_COMB_EIXO_X_FLH_LER_VIBR":              [8, 8],
        "MANCAL_COMB_EIXO_Y_FLH_LER_VIBR":              [8, 9],
        "MANCAL_COMB_EIXO_Z_FLH_LER_VIBR":              [8, 10],
        "DETECCAO_HORIZONTAL_FLH_LER_VIBRA":            [8, 12],
        "DETECCAO_VERTICAL_FLH_LER_VIBRA":              [8, 13],


        ## STATUS UG

        # Sistema de Água
        "SIS_AGUA_FLH_HAB":                             [11, 11],


        ## BLOQUEIO 86M

        # Trip Temperatura
        "UHLM_TRP_TMP_OLEO":                            [25, 4],
        "UHRV_TRP_TMP_OLEO":                            [25, 5],

        # Falhas de Leitura de Temperaturas
        "UHLM_FLH_LER_TMP_OLEO":                        [25, 6],
        "UHRV_FLH_LER_TMP_OLEO":                        [25, 7],
        "MANCAL_CASQ_COMB_FLH_LER_TMP":                 [25, 8],
        "MANCAL_CONT_ESCO_COMB_FLH_LER_TMP":            [25, 9],
        "MANCAL_COMB_PATINS_1_FLH_LER_TMP":             [25, 10],
        "MANCAL_COMB_PATINS_2_FLH_LER_TMP":             [25, 11],
        "MANCAL_GUIA_INTE_1_FLH_LER_TMP":               [25, 12],
        "MANCAL_GUIA_INTE_2_FLH_LER_TMP":               [25, 13],
        "PONTE_FASE_A_FLH_LER_TMP":                     [25, 14],
        "PONTE_FASE_B_FLH_LER_TMP":                     [25, 15],
        "PONTE_FASE_C_FLH_LER_TMP":                     [24, 0],
        "GERADOR_FASE_A_FLH_LER_TMP":                   [24, 1],
        "GERADOR_FASE_B_FLH_LER_TMP":                   [24, 2],
        "GERADOR_FASE_C_FLH_LER_TMP":                   [24, 3],
        "GERADOR_NUCL_ESTAT_FLH_LER_TMP":               [24, 4],

        # Trips Vibração
        "DETECCAO_HORIZONTAL_TRP_VIBRA":                [24, 10],
        "DETECCAO_VERTICAL_TRP_VIBRA":                  [24, 11],
        "MANCAL_COMB_EIXO_X_TRP_VIBR":                  [24, 12],
        "MANCAL_COMB_EIXO_Y_TRP_VIBR":                  [24, 13],
        "MANCAL_COMB_EIXO_Z_TRP_VIBR":                  [24, 14],

        # Bloqueio Atuado
        "86M_BLQ_ATUADO":                               [24, 15],

        "MANCAL_GUIA_1_FLH_LER_TMP":                    [25, 12],
        "MANCAL_GUIA_2_FLH_LER_TMP":                    [25, 13],

        ## BLOQUEIO_86E

        # Cubiculo Proteção Gerador
        "CPG_PORTA_INTERNA_FECHADA":                    [27, 2],
        "CPG_PORTA_TRASEIRA_FECHADA":                   [27, 3],

        # Relés
        "RELE_700G_TRP_ATUADO":                         [27, 4],
        "RELE_700G_BF_ATUADO":                          [27, 6],

        # Trips por Temperatura
        "PONTE_FASE_A_TRP_TMP":                         [26, 0],
        "PONTE_FASE_B_TRP_TMP":                         [26, 1],
        "PONTE_FASE_C_TRP_TMP":                         [26, 2],
        "GERADOR_FASE_A_TRP_TMP":                       [26, 3],
        "GERADOR_FASE_B_TRP_TMP":                       [26, 4],
        "GERADOR_FASE_C_TRP_TMP":                       [26, 5],
        "GERADOR_NUCL_ESTAT_TRP_TMP":                   [26, 6],

        # Trafo Excitação/Aterramento
        "TRAFO_ATERRAMENTO_TRP_TMP":                    [26, 8],
        "TRAFO_EXCITACAO_TRP_TMP":                      [26, 9],
        "TRAFO_EXCITACAO_FLH_LER_TMP":                  [26, 10],

        # Bloqueio Atuado
        "86E_BLQ_ATUADO":                               [26, 15],


        ## BLOQUEIO_86H

        # Trips Temperatura/Vibração/Pressão
        "UHRV_ACUMULADOR_PRESSAO_TRP":                  [29, 5],
        "MANCAL_CASQ_COMB_TRP_TMP":                     [28, 2],
        "MANCAL_CONT_ESCO_COMB_TRP_TMP":                [28, 3],
        "MANCAL_COMB_PATINS_1_TRP_TMP":                 [28, 4],
        "MANCAL_COMB_PATINS_2_TRP_TMP":                 [28, 5],
        "MANCAL_GUIA_INTE_1_TRP_TMP":                   [28, 6],
        "MANCAL_GUIA_INTE_2_TRP_TMP":                   [28, 7],
        "86H_BLQ_ATUADO":                               [28, 15],


        ## UHRV

        "UHRV_MANUTENCAO":                              [37, 0],
        "UHRV_BOMBA_1_FLH":                             [37, 5],
        "UHRV_BOMBA_2_FLH":                             [37, 7],


        ## UHLM

        "UHLM_MANUTENCAO":                              [39, 4],
        "UHLM_BOMBA_1_FLH":                             [39, 5],
        "UHLM_BOMBA_2_FLH":                             [39, 7],
        "UHLM_FLH_PRESSAO_LINHA_B1":                    [39, 9],
        "UHLM_FLH_PRESSAO_LINHA_B2":                    [39, 10],
        "UHLM_FLH_PRESSOSTATO_LINHA":                   [39, 11],


        ## RV

        "RV_FLH_HABILITAR":                             [43, 0],
        "RV_FLH_PARTIR":                                [43, 1],
        "RV_FLH_DESABILITAR":                           [43, 2],
        "RV_FLH_FECHAR_DISTRIBUIDOR":                   [43, 4],


        ## RT

        "RT_FLH_HABILITAR":                             [43, 8],
        "RT_FLH_PARTIR":                                [43, 9],
        "RT_FLH_DESABILITAR":                           [43, 10],



        ## COMANDOS_UG

        # Rearme Bloqueio
        "PASSOS_CMD_RST_FLH":                           [149, 0],
        "86M_CMD_REARME_BLQ":                           [149, 1],
        "86E_CMD_REARME_BLQ":                           [149, 2],
        "86H_CMD_REARME_BLQ":                           [149, 3],

        # Parada
        "PARADA_CMD_EMERGENCIA":                        [149, 4],
        "PARADA_BLQ_ABERTURA_DJ":                       [149, 11],
        "PARADA_CMD_DESABILITA_UHLM":                   [149, 15],

        # Partida
        "PARTIDA_CMD_SINCRONISMO":                      [149, 10],


        ## COMANDOS_UH

        # UHRV
        "UHRV_CMD_REARME_FLH":                          [151, 0],
        "UHLM_CMD_REARME_FLH":                          [150, 0],


        # --------------------------------------------------------------------- #
        ## Comunicação RTV

        # RV
        "RV_ESTADO_OPERACAO":                           21,

        "RV_SAIDAS_DIGITAIS":                           26,
        "RV_RELE_TRP_NAO_ATUADO":                       [26, 0],
        "RV_RELE_ALM_ATUADO":                           [26, 1],

        "RV_SETPOT_POT_ATIVA_PU":                       29,

        "RT_RELE_TRP_NAO_ATUADO":                       [31, 0],

        "RV_FLH_1_B0":                                  [67, 0],
        "RV_FLH_1_B1":                                  [67, 1],
        "RV_FLH_1_B2":                                  [67, 2],
        "RV_FLH_1_B3":                                  [67, 3],
        "RV_FLH_1_B4":                                  [67, 4],
        "RV_FLH_1_B5":                                  [67, 5],
        "RV_FLH_1_B6":                                  [67, 6],
        "RV_FLH_1_B7":                                  [67, 7],
        "RV_FLH_1_B8":                                  [67, 8],
        "RV_FLH_1_B10":                                 [67, 10],
        "RV_FLH_1_B11":                                 [67, 11],
        "RV_FLH_1_B12":                                 [67, 12],
        "RV_FLH_1_B13":                                 [67, 13],
        "RV_FLH_1_B14":                                 [67, 14],
        "RV_FLH_1_B15":                                 [67, 15],

        "RV_FLH_2_B0":                                  [68, 0],
        "RV_FLH_2_B1":                                  [68, 1],
        "RV_FLH_2_B2":                                  [68, 2],
        "RV_FLH_2_B3":                                  [68, 3],
        "RV_FLH_2_B4":                                  [68, 4],


        # RT
        "RT_SAIDAS_DIGITAIS":                           31,

        "RT_ALM_1_B0":                                  [70, 0],
        "RT_ALM_1_B4":                                  [70, 4],
        "RT_ALM_1_B5":                                  [70, 5],
        "RT_ALM_1_B8":                                  [70, 8],

        "RT_FLH_1_B0":                                  [72, 0],
        "RT_FLH_1_B1":                                  [72, 1],
        "RT_FLH_1_B2":                                  [72, 2],
        "RT_FLH_1_B3":                                  [72, 3],
        "RT_FLH_1_B4":                                  [72, 4],
        "RT_FLH_1_B5":                                  [72, 5],
        "RT_FLH_1_B6":                                  [72, 6],
        "RT_FLH_1_B7":                                  [72, 7],
        "RT_FLH_1_B8":                                  [72, 8],
        "RT_FLH_1_B9":                                  [72, 9],
        "RT_FLH_1_B10":                                 [72, 10],
        "RT_FLH_1_B11":                                 [72, 11],
        "RT_FLH_1_B12":                                 [72, 12],
        "RT_FLH_1_B13":                                 [72, 13],
        "RT_FLH_1_B14":                                 [72, 14],
        "RT_FLH_1_B15":                                 [72, 15],

        "RT_FLH_2_B0":                                  [73, 0],
        "RT_FLH_2_B1":                                  [73, 1],
        "RT_FLH_2_B2":                                  [73, 2],
        "RT_FLH_2_B3":                                  [73, 3],
        "RT_FLH_2_B4":                                  [73, 4],
        "RT_FLH_2_B5":                                  [73, 5],
        "RT_FLH_2_B6":                                  [73, 6],
        "RT_FLH_2_B7":                                  [73, 7],
        "RT_FLH_2_B8":                                  [73, 8],
        "RT_FLH_2_B9":                                  [73, 9],
        "RT_FLH_2_B10":                                 [73, 10],
        "RT_FLH_2_B11":                                 [73, 11],
        "RT_FLH_2_B12":                                 [73, 12],

        "RT_FLH_3_B0":                                  [74, 0],
        "RT_FLH_3_B1":                                  [74, 1],
        "RT_FLH_3_B2":                                  [74, 2],
        "RT_FLH_3_B3":                                  [74, 3],
        "RT_FLH_3_B4":                                  [74, 4],
        "RT_FLH_3_B5":                                  [74, 5],
        "RT_FLH_3_B6":                                  [74, 6],
        "RT_FLH_3_B7":                                  [74, 7],
    },

    "UG2": {

        ## LEITURAS_ANALOGICAS

        "GERADOR_FASE_A_TMP":                           44,
        "GERADOR_FASE_B_TMP":                           46,
        "GERADOR_FASE_C_TMP":                           48,
        "MANCAL_GUIA_TMP":                              54,
        "MANCAL_CASQ_COMB_TMP":                         60,
        "MANCAL_CONT_ESCO_COMB_TMP":                    62,
        "MANCAL_COMB_PATINS_1_TMP":                     64,
        "MANCAL_COMB_PATINS_2_TMP":                     66,
        "MANCAL_GUIA_INTE_1_TMP":                       68,
        "MANCAL_GUIA_INTE_2_TMP":                       70,
        "GERADOR_NUCL_ESTAT_TMP":                       72,
        "ENTRADA_TURBINA_PRESSAO":                      84,
        "GERADOR_SAIDA_AR_TRP_TMP":                     90,
        "HORIMETRO":                                    108,
        "P":                                            132,


        ## ENTRADAS_DIGITAIS_1 -> REGS 1, 0

        # UHLM
        "UHLM_FILTRO_SUJO":                             [0, 5],

        # UHRV
        "UHRV_FILTRO_SUJO":                             [0, 8],

        # Resistência
        "RESISTENCIA_FALHA":                            [0, 12],


        ## ENTRADAS_DIGITAIS_2 -> REGS 3, 2

        # Botão Emergência
        "BT_EMERGENCIA_ATUADO":                         [3, 11],

        # Supervisão
        "SUP_BOBINA_52G":                               [3, 12],
        "SUP_BOBINA_86EH":                              [3, 13],

        # Relé
        "RELE_BLQ_86EH_DESATUADO":                      [2, 12],
        "SUP_TENSAO_125VCC":                            [2, 13],
        "SUP_TENSAO_24VCC":                             [2, 14],

        # DJ
        "DJS_125VCC_FECHADOS":                          [2, 15],


        ## ENTRADAS_DIGITAIS_3 -> REGS 5, 4

        # DJ
        "DJS_24VCC_FECHADOS":                           [5, 0],

        # CLPs
        "CLP_GERAL_SEM_BLQ_EXTERNO":                    [5, 1],
        "CLP_GERAL_SIS_AGUA_OK":                        [5, 2],

        # Escovas Polo
        "ESCOVAS_POLO_POS_GASTAS":                      [5, 5],
        "ESCOVAS_POLO_NEG_GASTAS":                      [5, 6],

        # Disparo Mecânico
        "DISP_MECANICO_DESATUADO":                      [5, 8],
        "DISP_MECANICO_ATUADO":                         [5, 9],


        ## ALARMES_ANALOGICAS

        # Alarmes de Temperatura/Vibração
        "PONTE_FASE_A_ALM_TMP":                         [7, 0],
        "PONTE_FASE_B_ALM_TMP":                         [7, 1],
        "PONTE_FASE_C_ALM_TMP":                         [7, 2],
        "TRAFO_EXCITACAO_ALM_TMP":                      [7, 4],
        "MANCAL_GUIA_ALM_TMP":                          [7, 5],
        "UHRV_ALM_TMP_OLEO":                            [7, 6],
        "UHLM_ALM_TMP_OLEO":                            [7, 7],
        "MANCAL_CASQ_COMB_ALM_TMP":                     [7, 8],
        "MANCAL_CONT_ESCO_COMB_ALM_TMP":                [7, 9],
        "MANCAL_COMB_PATINS_1_ALM_TMP":                 [7, 10],
        "MANCAL_COMB_PATINS_2_ALM_TMP":                 [7, 11],
        "MANCAL_GUIA_INTE_1_ALM_TMP":                   [7, 12],
        "MANCAL_GUIA_INTE_2_ALM_TMP":                   [7, 13],
        "GERADOR_NUCL_ESTAT_ALM_TMP":                   [7, 14],
        "GERADOR_FASE_A_ALM_TMP":                       [7, 15],
        "GERADOR_FASE_B_ALM_TMP":                       [6, 0],
        "GERADOR_FASE_C_ALM_TMP":                       [6, 1],
        "MANCAL_COMB_EIXO_X_ALM_VIBR":                  [6, 8],
        "MANCAL_COMB_EIXO_Y_ALM_VIBR":                  [6, 9],
        "MANCAL_COMB_EIXO_Z_ALM_VIBR":                  [6, 10],
        "DETECCAO_HORIZONTAL_ALM_VIBRA":                [6, 12],
        "DETECCAO_VERTICAL_ALM_VIBRA":                  [6, 13],


        ## FALHAS_ANALOGICAS

        # Falhas de Leitura de Pressão/Vibração
        "ENTRADA_TURBINA_FLH_LER_PRESSAO":              [8, 4],
        "MANCAL_COMB_EIXO_X_FLH_LER_VIBR":              [8, 8],
        "MANCAL_COMB_EIXO_Y_FLH_LER_VIBR":              [8, 9],
        "MANCAL_COMB_EIXO_Z_FLH_LER_VIBR":              [8, 10],
        "DETECCAO_HORIZONTAL_FLH_LER_VIBRA":            [8, 12],
        "DETECCAO_VERTICAL_FLH_LER_VIBRA":              [8, 13],


        ## STATUS UG

        # Sistema de Água
        "SIS_AGUA_FLH_HAB":                             [11, 11],


        ## BLOQUEIO 86M

        # Trip Temperatura
        "UHLM_TRP_TMP_OLEO":                            [25, 4],
        "UHRV_TRP_TMP_OLEO":                            [25, 5],

        # Falhas de Leitura de Temperaturas
        "UHLM_FLH_LER_TMP_OLEO":                        [25, 6],
        "UHRV_FLH_LER_TMP_OLEO":                        [25, 7],
        "MANCAL_CASQ_COMB_FLH_LER_TMP":                 [25, 8],
        "MANCAL_CONT_ESCO_COMB_FLH_LER_TMP":            [25, 9],
        "MANCAL_COMB_PATINS_1_FLH_LER_TMP":             [25, 10],
        "MANCAL_COMB_PATINS_2_FLH_LER_TMP":             [25, 11],
        "MANCAL_GUIA_INTE_1_FLH_LER_TMP":               [25, 12],
        "MANCAL_GUIA_INTE_2_FLH_LER_TMP":               [25, 13],
        "PONTE_FASE_A_FLH_LER_TMP":                     [25, 14],
        "PONTE_FASE_B_FLH_LER_TMP":                     [25, 15],
        "PONTE_FASE_C_FLH_LER_TMP":                     [24, 0],
        "GERADOR_FASE_A_FLH_LER_TMP":                   [24, 1],
        "GERADOR_FASE_B_FLH_LER_TMP":                   [24, 2],
        "GERADOR_FASE_C_FLH_LER_TMP":                   [24, 3],
        "GERADOR_NUCL_ESTAT_FLH_LER_TMP":               [24, 4],

        # Trips Vibração
        "DETECCAO_HORIZONTAL_TRP_VIBRA":                [24, 10],
        "DETECCAO_VERTICAL_TRP_VIBRA":                  [24, 11],
        "MANCAL_COMB_EIXO_X_TRP_VIBR":                  [24, 12],
        "MANCAL_COMB_EIXO_Y_TRP_VIBR":                  [24, 13],
        "MANCAL_COMB_EIXO_Z_TRP_VIBR":                  [24, 14],

        # Bloqueio Atuado
        "86M_BLQ_ATUADO":                               [24, 15],


        ## BLOQUEIO_86E

        # Cubiculo Proteção Gerador
        "CPG_PORTA_INTERNA_FECHADA":                    [27, 2],
        "CPG_PORTA_TRASEIRA_FECHADA":                   [27, 3],

        # Relés
        "RELE_700G_TRP_ATUADO":                         [27, 4],
        "RELE_700G_BF_ATUADO":                          [27, 6],

        # Trips por Temperatura
        "PONTE_FASE_A_TRP_TMP":                         [26, 0],
        "PONTE_FASE_B_TRP_TMP":                         [26, 1],
        "PONTE_FASE_C_TRP_TMP":                         [26, 2],
        "GERADOR_FASE_A_TRP_TMP":                       [26, 3],
        "GERADOR_FASE_B_TRP_TMP":                       [26, 4],
        "GERADOR_FASE_C_TRP_TMP":                       [26, 5],
        "GERADOR_NUCL_ESTAT_TRP_TMP":                   [26, 6],

        # Trafo Excitação/Aterramento
        "TRAFO_ATERRAMENTO_TRP_TMP":                    [26, 8],
        "TRAFO_EXCITACAO_TRP_TMP":                      [26, 9],
        "TRAFO_EXCITACAO_FLH_LER_TMP":                  [26, 10],

        # Bloqueio Atuado
        "86E_BLQ_ATUADO":                               [26, 15],


        ## BLOQUEIO_86H

        # Trips Temperatura/Vibração/Pressão
        "UHRV_ACUMULADOR_PRESSAO_TRP":                  [29, 5],
        "MANCAL_CASQ_COMB_TRP_TMP":                     [28, 2],
        "MANCAL_CONT_ESCO_COMB_TRP_TMP":                [28, 3],
        "MANCAL_COMB_PATINS_1_TRP_TMP":                 [28, 4],
        "MANCAL_COMB_PATINS_2_TRP_TMP":                 [28, 5],
        "MANCAL_GUIA_INTE_1_TRP_TMP":                   [28, 6],
        "MANCAL_GUIA_INTE_2_TRP_TMP":                   [28, 7],
        "86H_BLQ_ATUADO":                               [28, 15],


        ## UHRV

        "UHRV_MANUTENCAO":                              [37, 0],
        "UHRV_BOMBA_1_FLH":                             [37, 5],
        "UHRV_BOMBA_2_FLH":                             [37, 7],


        ## UHLM

        "UHLM_MANUTENCAO":                              [39, 4],
        "UHLM_BOMBA_1_FLH":                             [39, 5],
        "UHLM_BOMBA_2_FLH":                             [39, 7],
        "UHLM_FLH_PRESSAO_LINHA_B1":                    [39, 9],
        "UHLM_FLH_PRESSAO_LINHA_B2":                    [39, 10],
        "UHLM_FLH_PRESSOSTATO_LINHA":                   [39, 11],


        ## RV

        "RV_FLH_HABILITAR":                             [43, 0],
        "RV_FLH_PARTIR":                                [43, 1],
        "RV_FLH_DESABILITAR":                           [43, 2],
        "RV_FLH_FECHAR_DISTRIBUIDOR":                   [43, 4],


        ## RT

        "RT_FLH_HABILITAR":                             [43, 8],
        "RT_FLH_PARTIR":                                [43, 9],
        "RT_FLH_DESABILITAR":                           [43, 10],


        ## COMANDOS_UG

        # Rearme Bloqueio
        "PASSOS_CMD_RST_FLH":                           [149, 0],
        "86M_CMD_REARME_BLQ":                           [149, 1],
        "86E_CMD_REARME_BLQ":                           [149, 2],
        "86H_CMD_REARME_BLQ":                           [149, 3],

        # Parada
        "PARADA_CMD_EMERGENCIA":                        [149, 4],
        "PARADA_BLQ_ABERTURA_DJ":                       [149, 11],
        "PARADA_CMD_DESABILITA_UHLM":                   [149, 15],

        # Partida
        "PARTIDA_CMD_SINCRONISMO":                      [149, 10],


        ## COMANDOS_UH

        # UHRV
        "UHRV_CMD_REARME_FLH":                          [151, 0],
        "UHLM_CMD_REARME_FLH":                          [150, 0],


        # --------------------------------------------------------------------- #
        ## Comunicação RTV

        # RV
        "RV_ESTADO_OPERACAO":                           21,

        "RV_SAIDAS_DIGITAIS":                           26,
        "RV_RELE_TRP_NAO_ATUADO":                       [26, 0],
        "RV_RELE_ALM_ATUADO":                           [26, 1],

        "RV_SETPOT_POT_ATIVA_PU":                       30,

        "RT_RELE_TRP_NAO_ATUADO":                       [31, 0],

        "RV_FLH_1_B0":                                  [67, 0],
        "RV_FLH_1_B1":                                  [67, 1],
        "RV_FLH_1_B2":                                  [67, 2],
        "RV_FLH_1_B3":                                  [67, 3],
        "RV_FLH_1_B4":                                  [67, 4],
        "RV_FLH_1_B5":                                  [67, 5],
        "RV_FLH_1_B6":                                  [67, 6],
        "RV_FLH_1_B7":                                  [67, 7],
        "RV_FLH_1_B8":                                  [67, 8],
        "RV_FLH_1_B10":                                 [67, 10],
        "RV_FLH_1_B11":                                 [67, 11],
        "RV_FLH_1_B12":                                 [67, 12],
        "RV_FLH_1_B13":                                 [67, 13],
        "RV_FLH_1_B14":                                 [67, 14],
        "RV_FLH_1_B15":                                 [67, 15],

        "RV_FLH_2_B0":                                  [68, 0],
        "RV_FLH_2_B1":                                  [68, 1],
        "RV_FLH_2_B2":                                  [68, 2],
        "RV_FLH_2_B3":                                  [68, 3],
        "RV_FLH_2_B4":                                  [68, 4],


        # RT
        "RT_SAIDAS_DIGITAIS":                           31,

        "RT_ALM_1_B0":                                  [70, 0],
        "RT_ALM_1_B4":                                  [70, 4],
        "RT_ALM_1_B5":                                  [70, 5],
        "RT_ALM_1_B8":                                  [70, 8],

        "RT_FLH_1_B0":                                  [72, 0],
        "RT_FLH_1_B1":                                  [72, 1],
        "RT_FLH_1_B2":                                  [72, 2],
        "RT_FLH_1_B3":                                  [72, 3],
        "RT_FLH_1_B4":                                  [72, 4],
        "RT_FLH_1_B5":                                  [72, 5],
        "RT_FLH_1_B6":                                  [72, 6],
        "RT_FLH_1_B7":                                  [72, 7],
        "RT_FLH_1_B8":                                  [72, 8],
        "RT_FLH_1_B9":                                  [72, 9],
        "RT_FLH_1_B10":                                 [72, 10],
        "RT_FLH_1_B11":                                 [72, 11],
        "RT_FLH_1_B12":                                 [72, 12],
        "RT_FLH_1_B13":                                 [72, 13],
        "RT_FLH_1_B14":                                 [72, 14],
        "RT_FLH_1_B15":                                 [72, 15],

        "RT_FLH_2_B0":                                  [73, 0],
        "RT_FLH_2_B1":                                  [73, 1],
        "RT_FLH_2_B2":                                  [73, 2],
        "RT_FLH_2_B3":                                  [73, 3],
        "RT_FLH_2_B4":                                  [73, 4],
        "RT_FLH_2_B5":                                  [73, 5],
        "RT_FLH_2_B6":                                  [73, 6],
        "RT_FLH_2_B7":                                  [73, 7],
        "RT_FLH_2_B8":                                  [73, 8],
        "RT_FLH_2_B9":                                  [73, 9],
        "RT_FLH_2_B10":                                 [73, 10],
        "RT_FLH_2_B11":                                 [73, 11],
        "RT_FLH_2_B12":                                 [73, 12],

        "RT_FLH_3_B0":                                  [74, 0],
        "RT_FLH_3_B1":                                  [74, 1],
        "RT_FLH_3_B2":                                  [74, 2],
        "RT_FLH_3_B3":                                  [74, 3],
        "RT_FLH_3_B4":                                  [74, 4],
        "RT_FLH_3_B5":                                  [74, 5],
        "RT_FLH_3_B6":                                  [74, 6],
        "RT_FLH_3_B7":                                  [74, 7],
    },
}


"""
Registradores que não achei:
CLP:
    SE:
        "RELE_LINHA_ATUADO"
        "RELE_SUP_BLQ_BOBINAS"

        "TE_NV_OLEO_MUITO_ALTO"



    UGs:
        "CLP_GERAL_COM_TENSAO_BARRA_ESSEN"
"""

REG_CLP["SE"]["CONDIC"] = [995, 4]
REG_CLP["UG1"]["CONDIC"] = [9950, 4]
REG_CLP["UG2"]["CONDIC"] = [995, 4]
REG_RELE["BAY"]["CONDIC"] = [999, 4]