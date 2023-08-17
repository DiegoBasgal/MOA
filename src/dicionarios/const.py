# Genéricos
INVALID = 0
CRITICAL_FAILURE = 2

ESCALA_DE_TEMPO = 1
TEMPO_CICLO_TOTAL = 30

TIMEOUT_MAIN = 10
TIMEOUT_PADRAO = 5
TIMEOUT_EMERGENCIA = 10
TIMEOUT_NORMALIZACAO = 10

# Tensão de linha
TENSAO_LINHA_BAIXA = 65550
TENSAO_LINHA_ALTA = 72450

TENSAO_VERIFICAR = 0
TENSAO_AGUARDO = 1
TENSAO_REESTABELECIDA = 2
TENSAO_FORA = 3

# Nível Montante
NIVEL_MAXIMORUM = 407.5
NIVEL_VERTIMENTO = 405.15
NIVEL_FUNDO_RESERVATORIO = 404.6

NV_FLAG_NORMAL = 0
NV_FLAG_EMERGENCIA = 1


CONDIC_IGNORAR = 0
CONDIC_NORMALIZAR = 1
CONDIC_AGUARDAR = 2
CONDIC_INDISPONIBILIZAR = 3

CONDIC_STR_DCT = {}
CONDIC_STR_DCT[CONDIC_IGNORAR] = "Ignorar"
CONDIC_STR_DCT[CONDIC_NORMALIZAR] = "Normalizar"
CONDIC_STR_DCT[CONDIC_AGUARDAR] = "Aguardar"
CONDIC_STR_DCT[CONDIC_INDISPONIBILIZAR] = "Indisponibilizar"

UG_SM_MANUAL = 0
UG_SM_DISPONIVEL = 1
UG_SM_RESTRITA = 2
UG_SM_INDISPONIVEL = 3

UG_SM_STR_DCT = {}
UG_SM_STR_DCT[UG_SM_MANUAL] = "Manual" 
UG_SM_STR_DCT[UG_SM_DISPONIVEL] = "Disponível"
UG_SM_STR_DCT[UG_SM_RESTRITA] = "Restrito"
UG_SM_STR_DCT[UG_SM_INDISPONIVEL] = "Indisponível"

UG_INCONSISTENTE = -1
UG_PARADA = 1
UG_PARANDO = 0
UG_SINCRONIZANDO = 2
UG_SINCRONIZADA = 3

UG_LST_ETAPAS = [
    UG_INCONSISTENTE,
    UG_PARADA,
    UG_PARANDO,
    UG_SINCRONIZADA,
    UG_SINCRONIZANDO,
]

UG_STR_DCT_ETAPAS = {}
UG_STR_DCT_ETAPAS[UG_INCONSISTENTE] = "Unidade Inconsistente"
UG_STR_DCT_ETAPAS[UG_PARADA] = "Unidade Parada"
UG_STR_DCT_ETAPAS[UG_PARANDO] = "Unidade Parando"
UG_STR_DCT_ETAPAS[UG_SINCRONIZADA] = "Unidade Sincronizada"
UG_STR_DCT_ETAPAS[UG_SINCRONIZANDO] = "Unidade Sincronizando"

UG_PRIORIDADE_HORAS = 0
UG_PRIORIDADE_1 = 1
UG_PRIORIDADE_2 = 2
UG_PRIORIDADE_3 = 3

UG_STR_DCT_PRIORIDADE = {}
UG_STR_DCT_PRIORIDADE[UG_PRIORIDADE_HORAS] = "Priorizar Horas-Máquina"
UG_STR_DCT_PRIORIDADE[UG_PRIORIDADE_1] = "Priorizar Unidade de Geração 1"
UG_STR_DCT_PRIORIDADE[UG_PRIORIDADE_2] = "Priorizar Unidade de Geração 2"
UG_STR_DCT_PRIORIDADE[UG_PRIORIDADE_3] = "Priorizar Unidade de Geração 3"

MOA_SM_INVALIDO = 0
MOA_SM_NAO_INICIALIZADO = 1
MOA_SM_FALHA_CRITICA = 2
MOA_SM_PRONTO = 3
MOA_SM_EMERGENCIA = 4
MOA_SM_MODO_MANUAL = 5
MOA_SM_CONTROLE_ESTADOS = 6
MOA_SM_CONTROLE_RESERVATORIO = 7
MOA_SM_CONTROLE_DADOS = 8
MOA_SM_CONTROLE_AGENDAMENTOS = 9

MOA_SM_STR_DCT = {}
MOA_SM_STR_DCT[MOA_SM_INVALIDO] = "Inválido"
MOA_SM_STR_DCT[MOA_SM_NAO_INICIALIZADO] = "Não Incializado"
MOA_SM_STR_DCT[MOA_SM_FALHA_CRITICA] = "Falha Crítica"
MOA_SM_STR_DCT[MOA_SM_PRONTO] = "Pronto"
MOA_SM_STR_DCT[MOA_SM_EMERGENCIA] = "Emergência"
MOA_SM_STR_DCT[MOA_SM_MODO_MANUAL] = "Modo Manual"
MOA_SM_STR_DCT[MOA_SM_CONTROLE_ESTADOS] = "Controle Estados"
MOA_SM_STR_DCT[MOA_SM_CONTROLE_RESERVATORIO] = "Controle Reservatório"
MOA_SM_STR_DCT[MOA_SM_CONTROLE_DADOS] = "Controle Dados"
MOA_SM_STR_DCT[MOA_SM_CONTROLE_AGENDAMENTOS] = "Controle Agendamentos"

# Agendamentos
AGN_INDISPONIBILIZAR = 1
AGN_ALTERAR_NV_ALVO = 2
AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS = 3
AGN_BAIXAR_POT_UGS_MINIMO = 4
AGN_NORMALIZAR_POT_UGS_MINIMO = 5
AGN_AGUARDAR_RESERVATORIO = 6
AGN_NORMALIZAR_ESPERA_RESERVATORIO = 7

AGN_UG1_ALTERAR_POT_LIMITE = 102
AGN_UG1_FORCAR_ESTADO_DISPONIVEL = 103
AGN_UG1_FORCAR_ESTADO_INDISPONIVEL = 104
AGN_UG1_FORCAR_ESTADO_MANUAL = 105
AGN_UG1_FORCAR_ESTADO_RESTRITO = 106
AGN_UG1_TEMPO_ESPERA_RESTRITO = 107
AGN_UG2_ALTERAR_POT_LIMITE = 202
AGN_UG2_FORCAR_ESTADO_DISPONIVEL = 203
AGN_UG2_FORCAR_ESTADO_INDISPONIVEL = 204
AGN_UG2_FORCAR_ESTADO_MANUAL = 205
AGN_UG2_FORCAR_ESTADO_RESTRITO = 206
AGN_UG2_TEMPO_ESPERA_RESTRITO = 207
AGN_UG3_ALTERAR_POT_LIMITE = 302
AGN_UG3_FORCAR_ESTADO_DISPONIVEL = 303
AGN_UG3_FORCAR_ESTADO_INDISPONIVEL = 304
AGN_UG3_FORCAR_ESTADO_MANUAL = 305
AGN_UG3_FORCAR_ESTADO_RESTRITO = 306
AGN_UG3_TEMPO_ESPERA_RESTRITO = 307

AGN_LST_BLOQUEIO_UG = [
    AGN_UG1_ALTERAR_POT_LIMITE,
    AGN_UG1_FORCAR_ESTADO_DISPONIVEL,
    AGN_UG1_FORCAR_ESTADO_INDISPONIVEL,
    AGN_UG1_FORCAR_ESTADO_MANUAL,
    AGN_UG1_FORCAR_ESTADO_RESTRITO,
    AGN_UG1_TEMPO_ESPERA_RESTRITO,
    AGN_UG2_ALTERAR_POT_LIMITE,
    AGN_UG2_FORCAR_ESTADO_DISPONIVEL,
    AGN_UG2_FORCAR_ESTADO_INDISPONIVEL,
    AGN_UG2_FORCAR_ESTADO_MANUAL,
    AGN_UG2_FORCAR_ESTADO_RESTRITO,
    AGN_UG2_TEMPO_ESPERA_RESTRITO,
    AGN_UG3_ALTERAR_POT_LIMITE,
    AGN_UG3_FORCAR_ESTADO_DISPONIVEL,
    AGN_UG3_FORCAR_ESTADO_INDISPONIVEL,
    AGN_UG3_FORCAR_ESTADO_MANUAL,
    AGN_UG3_FORCAR_ESTADO_RESTRITO,
    AGN_UG3_TEMPO_ESPERA_RESTRITO,
]

AGN_STR_DICT = {}
AGN_STR_DICT[AGN_INDISPONIBILIZAR] = "Indisponibilizar Usina"
AGN_STR_DICT[AGN_ALTERAR_NV_ALVO] = "Alterar Nível Alvo"
AGN_STR_DICT[AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS] = "Alterar Potênica Limite da Usina"
AGN_STR_DICT[AGN_BAIXAR_POT_UGS_MINIMO] = "Baixar Potência para Limpeza de Grades"
AGN_STR_DICT[AGN_NORMALIZAR_POT_UGS_MINIMO] = "Normalizar Potência Após Limpeza de Grades"
AGN_STR_DICT[AGN_AGUARDAR_RESERVATORIO] = "Acionar Espera do Reservatório"
AGN_STR_DICT[AGN_NORMALIZAR_ESPERA_RESERVATORIO] = "Normalizar Espera do Reservatório"
AGN_STR_DICT[AGN_UG1_ALTERAR_POT_LIMITE] = "UG1 - Alterar Potência Limite"
AGN_STR_DICT[AGN_UG1_FORCAR_ESTADO_DISPONIVEL] = "UG1 - Forçar Estado Disponível"
AGN_STR_DICT[AGN_UG1_FORCAR_ESTADO_INDISPONIVEL] = "UG1 - Forçar Estado Indisponível"
AGN_STR_DICT[AGN_UG1_FORCAR_ESTADO_MANUAL] = "UG1 - Forçar Estado Manual"
AGN_STR_DICT[AGN_UG1_FORCAR_ESTADO_RESTRITO] = "UG1 - Forçar Estado Restrito"
AGN_STR_DICT[AGN_UG1_TEMPO_ESPERA_RESTRITO] = "UG1 - Aguardar Temporizador para Normalização Restrito"
AGN_STR_DICT[AGN_UG2_ALTERAR_POT_LIMITE] = "UG2 - Alterar Potência Limite"
AGN_STR_DICT[AGN_UG2_FORCAR_ESTADO_DISPONIVEL] = "UG2 - Forçar Estado Disponível"
AGN_STR_DICT[AGN_UG2_FORCAR_ESTADO_INDISPONIVEL] = "UG2 - Forçar Estado Indisponível"
AGN_STR_DICT[AGN_UG2_FORCAR_ESTADO_MANUAL] = "UG2 - Forçar Estado Manual"
AGN_STR_DICT[AGN_UG2_FORCAR_ESTADO_RESTRITO] = "UG2 - Forçar Estado Restrito"
AGN_STR_DICT[AGN_UG2_TEMPO_ESPERA_RESTRITO] = "UG2 - Aguardar Temporizador para Normalização Restrito"
AGN_STR_DICT[AGN_UG3_ALTERAR_POT_LIMITE] = "UG3 - Alterar Potência Limite"
AGN_STR_DICT[AGN_UG3_FORCAR_ESTADO_DISPONIVEL] = "UG3 - Forçar Estado Disponível"
AGN_STR_DICT[AGN_UG3_FORCAR_ESTADO_INDISPONIVEL] = "UG3 - Forçar Estado Indisponível"
AGN_STR_DICT[AGN_UG3_FORCAR_ESTADO_MANUAL] = "UG3 - Forçar Estado Manual"
AGN_STR_DICT[AGN_UG3_FORCAR_ESTADO_RESTRITO] = "UG3 - Forçar Estado Restrito"
AGN_STR_DICT[AGN_UG3_TEMPO_ESPERA_RESTRITO] = "UG3 - Aguardar Temporizador para Normalização Restrito"