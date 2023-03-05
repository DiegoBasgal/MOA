INVALID = 0
CRITICAL_FAILURE = 2

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

UNIDADE_SINCRONIZADA = 5
UNIDADE_PARANDO = 2
UNIDADE_PARADA = 0
UNIDADE_SINCRONIZANDO = 9
UNIDADE_PRONTA_SINCRONISMO = 4
UNIDADE_VAZIO_DESESCITADO = 3
UNIDADE_PRONTA_GIRO_MECANICO = 1
UNIDADE_LISTA_DE_ETAPAS = [
    UNIDADE_SINCRONIZADA,
    UNIDADE_PARANDO,
    UNIDADE_PARADA,
    UNIDADE_SINCRONIZANDO,
    UNIDADE_PRONTA_SINCRONISMO,
    UNIDADE_VAZIO_DESESCITADO,
    UNIDADE_PRONTA_GIRO_MECANICO,
]

DEVE_INDISPONIBILIZAR = 3
DEVE_AGUARDAR = 2
DEVE_NORMALIZAR = 1
DEVE_IGNORAR = 0


MOA_UNIDADE_MANUAL = 0
MOA_UNIDADE_DISPONIVEL = 1
MOA_UNIDADE_RESTRITA = 2
MOA_UNIDADE_INDISPONIVEL = 3

AGENDAMENTO_INDISPONIBILIZAR = 1
AGENDAMENTO_ALTERAR_NV_ALVO = 2
AGENDAMENTO_ALTERAR_POT_LIMITE_TODAS_AS_UGS = 3
AGENDAMENTO_BAIXAR_POT_UGS_MINIMO = 4
AGENDAMENTO_NORMALIZAR_POT_UGS_MINIMO = 5
AGENDAMENTO_AGUARDAR_RESERVATORIO = 6
AGENDAMENTO_NORMALIZAR_ESPERA_RESERVATORIO = 7

AGENDAMENTO_UG1_ALTERAR_POT_LIMITE = 102
AGENDAMENTO_UG1_FORCAR_ESTADO_DISPONIVEL = 103
AGENDAMENTO_UG1_FORCAR_ESTADO_INDISPONIVEL = 104
AGENDAMENTO_UG1_FORCAR_ESTADO_MANUAL = 105
AGENDAMENTO_UG1_FORCAR_ESTADO_RESTRITO = 106
AGENDAMENTO_UG1_TEMPO_ESPERA_RESTRITO = 107

AGENDAMENTO_UG2_ALTERAR_POT_LIMITE = 202
AGENDAMENTO_UG2_FORCAR_ESTADO_DISPONIVEL = 203
AGENDAMENTO_UG2_FORCAR_ESTADO_INDISPONIVEL = 204
AGENDAMENTO_UG2_FORCAR_ESTADO_MANUAL = 205
AGENDAMENTO_UG2_FORCAR_ESTADO_RESTRITO = 206
AGENDAMENTO_UG2_TEMPO_ESPERA_RESTRITO = 207

AGENDAMENTO_DISPARAR_MENSAGEM_TESTE = 777
MODO_ESCOLHA_MANUAL = 2

AGENDAMENTO_LISTA_BLOQUEIO_UG1 = [
    AGENDAMENTO_UG1_ALTERAR_POT_LIMITE,
    AGENDAMENTO_UG1_FORCAR_ESTADO_DISPONIVEL,
    AGENDAMENTO_UG1_FORCAR_ESTADO_INDISPONIVEL,
    AGENDAMENTO_UG1_FORCAR_ESTADO_MANUAL,
    AGENDAMENTO_UG1_FORCAR_ESTADO_RESTRITO,
    AGENDAMENTO_UG1_TEMPO_ESPERA_RESTRITO
]

AGENDAMENTO_LISTA_BLOQUEIO_UG2 = [
    AGENDAMENTO_UG2_ALTERAR_POT_LIMITE,
    AGENDAMENTO_UG2_FORCAR_ESTADO_DISPONIVEL,
    AGENDAMENTO_UG2_FORCAR_ESTADO_INDISPONIVEL,
    AGENDAMENTO_UG2_FORCAR_ESTADO_MANUAL,
    AGENDAMENTO_UG2_FORCAR_ESTADO_RESTRITO,
    AGENDAMENTO_UG2_TEMPO_ESPERA_RESTRITO
]