ESCALA_DE_TEMPO = 5
TIMEOUT_PADRAO = 5
TIMEOUT_NORMALIZACAO = 10

NIVEL_MAXIMORUM = 825
NIVEL_FUNDO_RESERVATORIO = 820.5

TENSAO_LINHA_BAIXA = 32775
TENSAO_LINHA_ALTA = 36225

MODO_ESCOLHA_MANUAL = 2

NV_FLAG_NORMAL = 0
NV_FLAG_AGUARDANDO = 1
NV_FLAG_EMERGENCIA = 2
NV_FLAG_TDAOFFLINE = 3

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
MOA_SM_CONTROLE_TDAOFFLINE = 10

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
MOA_SM_STR_DCT[MOA_SM_CONTROLE_TDAOFFLINE] = "Controle Tda-Offline"

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

AGN_LST_BLOQUEIO_UG1 = [
    AGN_UG1_ALTERAR_POT_LIMITE,
    AGN_UG1_FORCAR_ESTADO_DISPONIVEL,
    AGN_UG1_FORCAR_ESTADO_INDISPONIVEL,
    AGN_UG1_FORCAR_ESTADO_MANUAL,
    AGN_UG1_FORCAR_ESTADO_RESTRITO,
    AGN_UG1_TEMPO_ESPERA_RESTRITO
]

AGN_UG2_ALTERAR_POT_LIMITE = 202
AGN_UG2_FORCAR_ESTADO_DISPONIVEL = 203
AGN_UG2_FORCAR_ESTADO_INDISPONIVEL = 204
AGN_UG2_FORCAR_ESTADO_MANUAL = 205
AGN_UG2_FORCAR_ESTADO_RESTRITO = 206
AGN_UG2_TEMPO_ESPERA_RESTRITO = 207

AGN_LST_BLOQUEIO_UG2 = [
    AGN_UG2_ALTERAR_POT_LIMITE,
    AGN_UG2_FORCAR_ESTADO_DISPONIVEL,
    AGN_UG2_FORCAR_ESTADO_INDISPONIVEL,
    AGN_UG2_FORCAR_ESTADO_MANUAL,
    AGN_UG2_FORCAR_ESTADO_RESTRITO,
    AGN_UG2_TEMPO_ESPERA_RESTRITO
]