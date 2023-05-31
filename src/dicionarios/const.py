# Temporizador interno
ESCALA_DE_TEMPO = 1
TEMPO_CICLO_TOTAL = 1

TIMEOUT_MAIN = 10
TIMEOUT_PADRAO = 5
TIMEOUT_NORMALIZACAO = 10

MODO_ESCOLHA_MANUAL = 2

NIVEL_MAXIMORUM = 825
NIVEL_VERTIMENTO = 821
NIVEL_FUNDO_RESERVATORIO = 820.5

TENSAO_LINHA_ALTA = 0 # 36225
TENSAO_LINHA_BAIXA = 0 # 32775

TENSAO_VERIFICAR = 0
TENSAO_AGUARDO = 1
TENSAO_REESTABELECIDA = 2
TENSAO_FORA = 3

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

UG_PARADA = 0
UG_PARANDO = 3
UG_SINCRONIZANDO = 5
UG_SINCRONIZADA = 7

UG_LST_ETAPAS = [
    UG_PARADA,
    UG_PARANDO,
    UG_SINCRONIZADA,
    UG_SINCRONIZANDO,
]

UG_STR_DCT_ETAPAS = {}
UG_STR_DCT_ETAPAS[UG_PARADA] = "Parada"
UG_STR_DCT_ETAPAS[UG_PARANDO] = "Parando"
UG_STR_DCT_ETAPAS[UG_SINCRONIZADA] = "Sincronizada"
UG_STR_DCT_ETAPAS[UG_SINCRONIZANDO] = "Sincronizando"

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

AGN_INDISPONIBILIZAR = 1
AGN_ALTERAR_NV_ALVO = 2
AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS = 3
AGN_BAIXAR_POT_UGS_MINIMO = 4
AGN_NORMALIZAR_POT_UGS_MINIMO = 5
AGN_AGUARDAR_RESERVATORIO = 6
AGN_NORMALIZAR_ESPERA_RESERVATORIO = 7

AGN_UG_ALTERAR_POT_LIMITE = [None, 102, 202]
AGN_UG_FORCAR_ESTADO_DISPONIVEL = [None, 103, 203]
AGN_UG_FORCAR_ESTADO_INDISPONIVEL = [None, 104, 204]
AGN_UG_FORCAR_ESTADO_MANUAL = [None, 105, 205]
AGN_UG_FORCAR_ESTADO_RESTRITO = [None, 106, 206]
AGN_UG_TEMPO_ESPERA_RESTRITO = [None, 107, 207]

AGN_LST_BLOQUEIO_UG = [
    AGN_UG_ALTERAR_POT_LIMITE[1],
    AGN_UG_FORCAR_ESTADO_DISPONIVEL[1],
    AGN_UG_FORCAR_ESTADO_INDISPONIVEL[1],
    AGN_UG_FORCAR_ESTADO_MANUAL[1],
    AGN_UG_FORCAR_ESTADO_RESTRITO[1],
    AGN_UG_TEMPO_ESPERA_RESTRITO[1],
    AGN_UG_ALTERAR_POT_LIMITE[2],
    AGN_UG_FORCAR_ESTADO_DISPONIVEL[2],
    AGN_UG_FORCAR_ESTADO_INDISPONIVEL[2],
    AGN_UG_FORCAR_ESTADO_MANUAL[2],
    AGN_UG_FORCAR_ESTADO_RESTRITO[2],
    AGN_UG_TEMPO_ESPERA_RESTRITO[2],
]

AGN_STR_DICT = {}
AGN_STR_DICT[AGN_INDISPONIBILIZAR] = "Indisponibilizar Usina"
AGN_STR_DICT[AGN_ALTERAR_NV_ALVO] = "Alterar nível alvo"
AGN_STR_DICT[AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS] = "Baixar potênica limite da Usina"
AGN_STR_DICT[AGN_BAIXAR_POT_UGS_MINIMO] = "Baixar potência para limpeza de grades"
AGN_STR_DICT[AGN_NORMALIZAR_POT_UGS_MINIMO] = "Normalizar potência pós limpeza de grades"
AGN_STR_DICT[AGN_AGUARDAR_RESERVATORIO] = "Aguardar reservatório"
AGN_STR_DICT[AGN_NORMALIZAR_ESPERA_RESERVATORIO] = "Normalizar espera do reservatório"
AGN_STR_DICT[AGN_UG_ALTERAR_POT_LIMITE[1]] = "Alterar potência limite"
AGN_STR_DICT[AGN_UG_FORCAR_ESTADO_DISPONIVEL[1]] = "Forçar estado Disponível"
AGN_STR_DICT[AGN_UG_FORCAR_ESTADO_INDISPONIVEL[1]] = "Forçar estado Indisponível"
AGN_STR_DICT[AGN_UG_FORCAR_ESTADO_MANUAL[1]] = "Forçar estado Manual"
AGN_STR_DICT[AGN_UG_FORCAR_ESTADO_RESTRITO[1]] = "Forçar estado Restrito"
AGN_STR_DICT[AGN_UG_TEMPO_ESPERA_RESTRITO[1]] = "Aguardar temporizador para normalização Restrito"