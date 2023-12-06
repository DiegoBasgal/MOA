# Temporizador interno
ESCALA_DE_TEMPO = 1
TIMEOUT_PADRAO = 5
TIMEOUT_MAIN = 10
TIMEOUT_NORMALIZACAO = 10
TEMPO_CICLO_TOTAL = 30

# Valores fixos de nível
NIVEL_MAXIMORUM = 466.37
NIVEL_VERTIMENTO = 462.37
NIVEL_FUNDO_RESERVATORIO = 460

# Valores fixos de tensão na linha
TENSAO_LINHA_BAIXA = 21945
TENSAO_LINHA_ALTA = 24255

TENSAO_FASE_BAY_BAIXA = 12682
TENSAO_FASE_BAY_ALTA = 14350

# Sinais da funcção de retomada após queda de tensão
TENSAO_VERIFICAR = 0
TENSAO_AGUARDO = 1
TENSAO_REESTABELECIDA = 2
TENSAO_FORA = 3

# Sinais da função de verificação do Bay e Subestação
DJS_OK = 0
DJS_FALHA = 1
DJS_FALTA_TENSAO = 2

# Sinais da função de controle de reservatório
NV_NORMAL = 0
NV_EMERGENCIA = 1

# Status Limpa Grades
LG_INDISPONIVEL = 0
LG_DISPONIVEL = 1

# Valor de Disparo do Limpa Grades por Perda na Grade

LG_PERDA_UG1 = 0.3
LG_PERDA_UG2 = 0.3

# Posição das comportas
CP_FECHADA = 0
CP_ABERTA = 1
CP_CRACKING = 2
CP_MANUAL = 3
CP_OPERANDO = 4
CP_INCONSISTENTE = 99

CP_STR_DCT = {}
CP_STR_DCT[CP_FECHADA] = "Fechada"
CP_STR_DCT[CP_ABERTA] = "Aberta"
CP_STR_DCT[CP_CRACKING] = "Cracking"
CP_STR_DCT[CP_MANUAL] = "Manual"
CP_STR_DCT[CP_OPERANDO] = "Operando"
CP_STR_DCT[CP_INCONSISTENTE] = "Inconsistente"

# Prioridade das UGs
UG_PRIORIDADE_HORAS = 0
UG_PRIORIDADE_1 = 1
UG_PRIORIDADE_2 = 2

UG_STR_DCT_PRIORIDADE = {}
UG_STR_DCT_PRIORIDADE[UG_PRIORIDADE_HORAS] = "Priorizar Horas-Máquina"
UG_STR_DCT_PRIORIDADE[UG_PRIORIDADE_1] = "Priorizar Unidade de Geração 1"
UG_STR_DCT_PRIORIDADE[UG_PRIORIDADE_2] = "Priorizar Unidade de Geração 2"

# Gravidade dos Condicionadores
CONDIC_IGNORAR = 0
CONDIC_NORMALIZAR = 1
CONDIC_AGUARDAR = 2
CONDIC_INDISPONIBILIZAR = 3

CONDIC_STR_DCT = {}
CONDIC_STR_DCT[CONDIC_IGNORAR] = "Ignorar"
CONDIC_STR_DCT[CONDIC_NORMALIZAR] = "Normalizar"
CONDIC_STR_DCT[CONDIC_AGUARDAR] = "Aguardar"
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
UG_PARADA = 1
UG_PARANDO = 3
UG_SINCRONIZADA = 7
UG_SINCRONIZANDO = 4
# UG_VAZIO_DESESCITADO = 9
# UG_PRONTA_SINCRONISMO = 8
# UG_PRONTA_GIRO_MECANICO = 7
UG_INCONSISTENTE = None

UG_LST_ETAPAS = [
    UG_SINCRONIZADA,
    UG_PARANDO,
    UG_PARADA,
    UG_SINCRONIZANDO,
    # UG_PRONTA_SINCRONISMO,
    # UG_VAZIO_DESESCITADO,
    # UG_PRONTA_GIRO_MECANICO,
    UG_INCONSISTENTE,
]

UG_STR_DCT_ETAPAS = {}
UG_STR_DCT_ETAPAS[UG_PARADA] = "Parada"
UG_STR_DCT_ETAPAS[UG_PARANDO] = "Parando"
UG_STR_DCT_ETAPAS[UG_SINCRONIZADA] = "Sincronizada"
UG_STR_DCT_ETAPAS[UG_SINCRONIZANDO] = "Sincronizando"
# UG_STR_DCT_ETAPAS[UG_VAZIO_DESESCITADO] = "Vazio Desescitado"
# UG_STR_DCT_ETAPAS[UG_PRONTA_SINCRONISMO] = "Pronta Sincronismo"
# UG_STR_DCT_ETAPAS[UG_PRONTA_GIRO_MECANICO] = "Pronta Giro Mecâncico"
UG_STR_DCT_ETAPAS[UG_INCONSISTENTE] = "Inconsistente"

# Estados Moa
MOA_SM_INVALIDO = 0
MOA_SM_NAO_INICIALIZADO = 1
MOA_SM_FALHA_CRITICA = 2
MOA_SM_PRONTO = 3
MOA_SM_EMERGENCIA = 4
MOA_SM_MODO_MANUAL = 5
MOA_SM_CONTROLE_ESTADOS = 6
MOA_SM_CONTROLE_COMPORTAS = 7
MOA_SM_CONTROLE_RESERVATORIO = 8
MOA_SM_CONTROLE_DADOS = 9
MOA_SM_CONTROLE_AGENDAMENTOS = 10

MOA_SM_STR_DCT = {}
MOA_SM_STR_DCT[MOA_SM_INVALIDO] = "Inválido"
MOA_SM_STR_DCT[MOA_SM_NAO_INICIALIZADO] = "Não Incializado"
MOA_SM_STR_DCT[MOA_SM_FALHA_CRITICA] = "Falha Crítica"
MOA_SM_STR_DCT[MOA_SM_PRONTO] = "Pronto"
MOA_SM_STR_DCT[MOA_SM_EMERGENCIA] = "Emergência"
MOA_SM_STR_DCT[MOA_SM_MODO_MANUAL] = "Modo Manual"
MOA_SM_STR_DCT[MOA_SM_CONTROLE_ESTADOS] = "Controle Estados"
MOA_SM_STR_DCT[MOA_SM_CONTROLE_COMPORTAS] = "Controle Comportas"
MOA_SM_STR_DCT[MOA_SM_CONTROLE_RESERVATORIO] = "Controle Reservatório"
MOA_SM_STR_DCT[MOA_SM_CONTROLE_DADOS] = "Controle Dados"
MOA_SM_STR_DCT[MOA_SM_CONTROLE_AGENDAMENTOS] = "Controle Agendamentos"

# Agendamentos
AGN_INDISPONIBILIZAR = 1
AGN_ALTERAR_NV_ALVO = 2
AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS = 3
AGN_AGUARDAR_RESERVATORIO = 6
AGN_NORMALIZAR_ESPERA_RESERVATORIO = 7
AGN_LG_FORCAR_ESTADO_DISPONIVEL = 8
AGN_LG_FORCAR_ESTADO_INDISPONIVEL = 9

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
AGN_STR_DICT[AGN_ALTERAR_NV_ALVO] = "Alterar Nível Alvo"
AGN_STR_DICT[AGN_ALTERAR_POT_LIMITE_TODAS_AS_UGS] = "Alterar Potênica Limite da Usina"
AGN_STR_DICT[AGN_AGUARDAR_RESERVATORIO] = "Aguardar Reservatório"
AGN_STR_DICT[AGN_NORMALIZAR_ESPERA_RESERVATORIO] = "Normalizar Espera do Reservatório"
AGN_STR_DICT[AGN_LG_FORCAR_ESTADO_DISPONIVEL] = "LG - Forçar Estado Disponível"
AGN_STR_DICT[AGN_LG_FORCAR_ESTADO_INDISPONIVEL] = "LG - Forçar Estado Indisponível"
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


# Antigos (TODO VERIFICAR)
INVALID = 0
CRITICAL_FAILURE = 2
MODO_ESCOLHA_MANUAL = 2

MOA_DEACTIVATED_AUTONOMOUS_MODE = 0
MOA_ACTIVATED_AUTONOMOUS_MODE = 1