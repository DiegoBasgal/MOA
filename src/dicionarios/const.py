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
TENSAO_LINHA_BAIXA = 0
TENSAO_LINHA_ALTA = 0

TENSAO_VERIFICAR = 0
TENSAO_AGUARDO = 1
TENSAO_REESTABELECIDA = 2
TENSAO_FORA = 3

# Nível Montante
NIVEL_MAXIMORUM = 0
NIVEL_VERTIMENTO = 0
NIVEL_FUNDO_RESERVATORIO = 0

NV_FLAG_NORMAL = 0
NV_FLAG_EMERGENCIA = 1


CONDIC_IGNORAR = 0
CONDIC_NORMALIZAR = 1
CONDIC_AGUARDAR = 2
CONDIC_INDISPONIBILIZAR = 3

CONDIC_STR_DCT = {}
CONDIC_STR_DCT[CONDIC_IGNORAR] = "Ignorar"
CONDIC_STR_DCT[CONDIC_NORMALIZAR] = "Aguardar"
CONDIC_STR_DCT[CONDIC_AGUARDAR] = "Normalizar"
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
AGN_ALTERAR_POT_LIMITE_DA_UG = 3
AGN_AGUARDAR_RESERVATORIO = 6
AGN_NORMALIZAR_ESPERA_RESERVATORIO = 7

AGN_UG_ALTERAR_POT_LIMITE = 102
AGN_UG_FORCAR_ESTADO_DISPONIVEL = 103
AGN_UG_FORCAR_ESTADO_INDISPONIVEL = 104
AGN_UG_FORCAR_ESTADO_MANUAL = 105
AGN_UG_FORCAR_ESTADO_RESTRITO = 106
AGN_UG_TEMPO_ESPERA_RESTRITO = 107

AGN_LST_BLOQUEIO_UG = [
    AGN_UG_ALTERAR_POT_LIMITE,
    AGN_UG_FORCAR_ESTADO_DISPONIVEL,
    AGN_UG_FORCAR_ESTADO_INDISPONIVEL,
    AGN_UG_FORCAR_ESTADO_MANUAL,
    AGN_UG_FORCAR_ESTADO_RESTRITO,
    AGN_UG_TEMPO_ESPERA_RESTRITO,
]

AGN_STR_DICT = {}
AGN_STR_DICT[AGN_INDISPONIBILIZAR] = "Indisponibilizar Usina"
AGN_STR_DICT[AGN_ALTERAR_NV_ALVO] = "Alterar nível alvo"
AGN_STR_DICT[AGN_ALTERAR_POT_LIMITE_DA_UG] = "Baixar Potênica Limite da Usina"
AGN_STR_DICT[AGN_AGUARDAR_RESERVATORIO] = "Aguardar reservatório"
AGN_STR_DICT[AGN_NORMALIZAR_ESPERA_RESERVATORIO] = "Normalizar espera do reservatório"
AGN_STR_DICT[AGN_UG_ALTERAR_POT_LIMITE] = "UG1 - Alterar potência limite"
AGN_STR_DICT[AGN_UG_FORCAR_ESTADO_DISPONIVEL] = "UG1 - Forçar estado Disponível"
AGN_STR_DICT[AGN_UG_FORCAR_ESTADO_INDISPONIVEL] = "UG1 - Forçar estado Indisponível"
AGN_STR_DICT[AGN_UG_FORCAR_ESTADO_MANUAL] = "UG1 - Forçar estado Manual"
AGN_STR_DICT[AGN_UG_FORCAR_ESTADO_RESTRITO] = "UG1 - Forçar estado Restrito"
AGN_STR_DICT[AGN_UG_TEMPO_ESPERA_RESTRITO] = "UG1 - Aguardar temporizador para normalização Restrito"