# Temporizador interno
ESCALA_DE_TEMPO = 3
TIMEOUT_PADRAO = 5
TIMEOUT_MAIN = 10
TIMEOUT_NORMALIZACAO = 10
TEMPO_CICLO_TOTAL = 50

# Valores fixos de nível
NIVEL_MAXIMORUM = 466.37
NIVEL_VERTIMENTO = ...
NIVEL_FUNDO_RESERVATORIO = 460

# Valores fixos de tensão na linha
TENSAO_LINHA_BAIXA = 21945
TENSAO_LINHA_ALTA = 24255

TENSAO_FASE_BAY_BAIXA = 12682
TENSAO_FASE_BAY_ALTA = 13350

# Sinais da funcção de retomada após queda de tensão
TENSAO_VERIFICAR = 0
TENSAO_AGUARDO = 1
TENSAO_REESTABELECIDA = 2
TENSAO_FORA = 3

# Sinais da função de fechamento do Disjuntor Linha
DJL_FALHA_FECHAMENTO = 0
DJL_FECHAMENTO_OK = 1
DJL_DJBAY_ABERTO = 2

# Sinais da função de normalização da Usina
NORM_USN_EXECUTADA = 0
NORM_USN_JA_EXECUTADA = 1
NORM_USN_DJBAY_ABERTO = 2
NORM_USN_DJL_ABERTO = 3
NORM_USN_FALTA_TENSAO = 4

# Sinais da função de controle de reservatório
NV_FLAG_NORMAL = 0
NV_FLAG_EMERGENCIA = 1

# Posição das comportas
CP_FECHADA = 0
CP_ABERTA = 1
CP_CRACKING = 2
CP_REMOTO = 3

CP_STR_DCT = {}
CP_STR_DCT[CP_FECHADA] = "Fechada"
CP_STR_DCT[CP_ABERTA] = "Aberta"
CP_STR_DCT[CP_CRACKING] = "Cracking"
CP_STR_DCT[CP_REMOTO] = "Remoto"

# Prioridade das UGs
UG_PRIORIDADE_HORAS = 0
UG_PRIORIDADE_1 = 1
UG_PRIORIDADE_2 = 2
UG_PRIORIDADE_3 = 3

UG_STR_DCT_PRIORIDADE = {}
UG_STR_DCT_PRIORIDADE[UG_PRIORIDADE_HORAS] = "Priorizar Horas-Máquina"
UG_STR_DCT_PRIORIDADE[UG_PRIORIDADE_1] = "Priorizar Unidade de Geração 1"
UG_STR_DCT_PRIORIDADE[UG_PRIORIDADE_2] = "Priorizar Unidade de Geração 2"
UG_STR_DCT_PRIORIDADE[UG_PRIORIDADE_3] = "Priorizar Unidade de Geração 3"

# Gravidade dos Condicionadores
CONDIC_IGNORAR = 0
CONDIC_NORMALIZAR = 1
CONDIC_AGUARDAR = 2
CONDIC_INDISPONIBILIZAR = 3

CONDIC_STR_DCT = {}
CONDIC_STR_DCT[CONDIC_IGNORAR] = "Ignorar"
CONDIC_STR_DCT[CONDIC_NORMALIZAR] = "Aguardar"
CONDIC_STR_DCT[CONDIC_AGUARDAR] = "Normalizar"
CONDIC_STR_DCT[CONDIC_INDISPONIBILIZAR] = "Indisponibilizar"

# Estados Unidade de Geração
UG_SM_MANUAL = 0
UG_SM_DISPONIVEL = 1
UG_SM_RESTRITA = 2
UG_SM_INDISPONIVEL = 3

UG_SM_STR_DCT = {}
UG_SM_STR_DCT[UG_SM_MANUAL] = "Manual"
UG_SM_STR_DCT[UG_SM_DISPONIVEL] = "Disponível"
UG_SM_STR_DCT[UG_SM_RESTRITA] = "Restrito"
UG_SM_STR_DCT[UG_SM_INDISPONIVEL] = "Indisponível"

# Etapas Unidade de Geração
UG_PARADA = 0
UG_PARANDO = 2
UG_SINCRONIZADA = 5
UG_SINCRONIZANDO = 9
UG_VAZIO_DESESCITADO = 3
UG_PRONTA_SINCRONISMO = 4
UG_PRONTA_GIRO_MECANICO = 1

UG_LST_ETAPAS = [
    UG_SINCRONIZADA,
    UG_PARANDO,
    UG_PARADA,
    UG_SINCRONIZANDO,
    UG_PRONTA_SINCRONISMO,
    UG_VAZIO_DESESCITADO,
    UG_PRONTA_GIRO_MECANICO,
]

UG_STR_DCT_ETAPAS = {}
UG_STR_DCT_ETAPAS[UG_PARADA] = "Parada"
UG_STR_DCT_ETAPAS[UG_PARANDO] = "Parando"
UG_STR_DCT_ETAPAS[UG_SINCRONIZADA] = "Sincronizada"
UG_STR_DCT_ETAPAS[UG_SINCRONIZANDO] = "Sincronizando"
UG_STR_DCT_ETAPAS[UG_VAZIO_DESESCITADO] = "Vazio Desescitado"
UG_STR_DCT_ETAPAS[UG_PRONTA_SINCRONISMO] = "Pronta Sincronismo"
UG_STR_DCT_ETAPAS[UG_PRONTA_GIRO_MECANICO] = "Pronta Giro Mecâncico"

# Estados Moa
MOA_SM_INVALIDO = 0
MOA_SM_NAO_INICIALIZADO = 1
MOA_SM_FALHA_CRITICA = 2
MOA_SM_PRONTO = 3
MOA_SM_CONTROLE_NORMAL = 4
MOA_SM_CONTROLE_RESERVATORIO = 5
MOA_SM_CONTROLE_DADOS = 6
MOA_SM_CONTROLE_AGENDAMENTOS = 7
MOA_SM_CONTROLE_MANUAL = 8
MOA_SM_CONTROLE_EMERGENCIA = 9

MOA_SM_STR_DCT = {}
MOA_SM_STR_DCT[MOA_SM_INVALIDO] = "Inválido"
MOA_SM_STR_DCT[MOA_SM_NAO_INICIALIZADO] = "Não Incializado"
MOA_SM_STR_DCT[MOA_SM_FALHA_CRITICA] = "Falha Crítica"
MOA_SM_STR_DCT[MOA_SM_PRONTO] = "Pronto"
MOA_SM_STR_DCT[MOA_SM_CONTROLE_NORMAL] = "Controle Normal"
MOA_SM_STR_DCT[MOA_SM_CONTROLE_RESERVATORIO] = "Controle Reservatório"
MOA_SM_STR_DCT[MOA_SM_CONTROLE_DADOS] = "Controle Dados"
MOA_SM_STR_DCT[MOA_SM_CONTROLE_AGENDAMENTOS] = "Controle Agendamentos"
MOA_SM_STR_DCT[MOA_SM_CONTROLE_EMERGENCIA] = "Controle Emergência"

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
    AGN_UG2_TEMPO_ESPERA_RESTRITO
]

AGN_STR_DICT = {}
AGN_STR_DICT[AGN_INDISPONIBILIZAR] = "Indisponibilizar Usina"
AGN_STR_DICT[AGN_ALTERAR_NV_ALVO] = "Alterar nível alvo"
AGN_STR_DICT[AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS] = "Baixar potênica limite da Usina"
AGN_STR_DICT[AGN_BAIXAR_POT_UGS_MINIMO] = "Baixar potência para limpeza de grades"
AGN_STR_DICT[AGN_NORMALIZAR_POT_UGS_MINIMO] = "Normalizar potência pós limpeza de grades"
AGN_STR_DICT[AGN_AGUARDAR_RESERVATORIO] = "Aguardar reservatório"
AGN_STR_DICT[AGN_NORMALIZAR_ESPERA_RESERVATORIO] = "Normalizar espera do reservatório"
AGN_STR_DICT[AGN_UG1_ALTERAR_POT_LIMITE] = "UG1 - Alterar potência limite"
AGN_STR_DICT[AGN_UG1_FORCAR_ESTADO_DISPONIVEL] = "UG1 - Forçar estado Disponível"
AGN_STR_DICT[AGN_UG1_FORCAR_ESTADO_INDISPONIVEL] = "UG1 - Forçar estado Indisponível"
AGN_STR_DICT[AGN_UG1_FORCAR_ESTADO_MANUAL] = "UG1 - Forçar estado Manual"
AGN_STR_DICT[AGN_UG1_FORCAR_ESTADO_RESTRITO] = "UG1 - Forçar estado Restrito"
AGN_STR_DICT[AGN_UG1_TEMPO_ESPERA_RESTRITO] = "UG1 - Aguardar temporizador para normalização Restrito"
AGN_STR_DICT[AGN_UG2_ALTERAR_POT_LIMITE] = "UG2 - Alterar potência limite"
AGN_STR_DICT[AGN_UG2_FORCAR_ESTADO_DISPONIVEL] = "UG2 - Forçar estado Disponível"
AGN_STR_DICT[AGN_UG2_FORCAR_ESTADO_INDISPONIVEL] = "UG2 - Forçar estado Indisponível"
AGN_STR_DICT[AGN_UG2_FORCAR_ESTADO_MANUAL] = "UG2 - Forçar estado Manual"
AGN_STR_DICT[AGN_UG2_FORCAR_ESTADO_RESTRITO] = "UG2 - Forçar estado Restrito"
AGN_STR_DICT[AGN_UG2_TEMPO_ESPERA_RESTRITO] = "UG2 - Aguardar temporizador para normalização Restrito"





# Antigos (TODO VERIFICAR)
INVALID = 0
CRITICAL_FAILURE = 2
MODO_ESCOLHA_MANUAL = 2

MOA_INVALID = 0
MOA_INITIALIZING = 1
MOA_CRITICAL_FAILURE = 2
MOA_OPERATIONAL = 3
MOA_AWAITING = 4

SM_INVALID = 0
SM_NOT_INITIALIDED = 1
SM_CRITICAL_FAILURE = 2
SM_READY = 3
SM_INTERNAL_VALUES_UPDATED = 4
SM_EMERGENCY = 5
SM_MANUAL_MODE_ACTIVE = 6
SM_SCHEDULE_PENDING = 7
SM_DAM_LEVEL_UNDER_LOW_LIMIT = 8
SM_DAM_LEVEL_OVER_HIGH_LIMIT = 9
SM_DAM_LEVEL_BETWEEN_LIMITS = 10
SM_CONTROL_ACTION_SENT = 11

MOA_DEACTIVATED_AUTONOMOUS_MODE = 0
MOA_ACTIVATED_AUTONOMOUS_MODE = 1