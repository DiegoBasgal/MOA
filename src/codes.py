# Genéricos
INVALID = 0
CRITICAL_FAILURE = 2

# Status MOA 'tabela 1'
MOA_INVALID = 0
MOA_INITIALIZING = 1
MOA_CRITICAL_FAILURE = 2
MOA_OPERATIONAL = 3
MOA_AWAITING = 4

# Estados SM 'tabela 2'
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

# Modo MOA 'tabela 3'
MOA_DEACTIVATED_AUTONOMOUS_MODE = 0
MOA_ACTIVATED_AUTONOMOUS_MODE = 1

# Unidades de Geração
UNIDADE_PARADA = 1
UNIDADE_PRONTA_PARA_GIRO_MECANICO = 2
UNIDADE_EM_VAZIO_DESEXITADA = 4
UNIDADE_PRONTA_PARA_SINCRONISMO = 8
UNIDADE_SINCRONIZADA = 16
UNIDADE_LISTA_DE_ETAPAS = [UNIDADE_PARADA, UNIDADE_SINCRONIZADA]
DEVE_INDISPONIBILIZAR = 2
DEVE_NORMALIZAR = 1
DEVE_IGNORAR = 0

# Agendamentos
AGENDAMENTO_INDISPONIBILIZAR = 1
AGENDAMENTO_ALETRAR_NV_ALVO = 2

AGENDAMENTO_UG1_ALETRAR_POT_LIMITE = 102
AGENDAMENTO_UG1_FORCAR_ESTADO_DISPONIVEL = 103
AGENDAMENTO_UG1_FORCAR_ESTADO_INDISPONIVEL = 104
AGENDAMENTO_UG1_FORCAR_ESTADO_MANUAL = 105
AGENDAMENTO_UG1_FORCAR_ESTADO_RESTRITO = 106

AGENDAMENTO_UG2_ALETRAR_POT_LIMITE = 202
AGENDAMENTO_UG2_FORCAR_ESTADO_DISPONIVEL = 203
AGENDAMENTO_UG2_FORCAR_ESTADO_INDISPONIVEL = 204
AGENDAMENTO_UG2_FORCAR_ESTADO_MANUAL = 205
AGENDAMENTO_UG2_FORCAR_ESTADO_RESTRITO = 206

AGENDAMENTO_DISPARAR_MENSAGEM_TESTE = 777
MODO_ESCOLHA_MANUAL = 2