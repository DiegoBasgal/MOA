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

# Posição das comportas
COMPORTA_FECHADA = 0
COMPORTA_ABERTA = 1
COMPORTA_CRACKING = 2

# Unidades de Geração
UNIDADE_SINCRONIZADA = 5
UNIDADE_PARANDO = 2
UNIDADE_PARADA = 1
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
DEVE_INDISPONIBILIZAR = 2
DEVE_NORMALIZAR = 1
DEVE_IGNORAR = 0
MOA_UNIDADE_MANUAL = 0
MOA_UNIDADE_DISPONIVEL = 1
MOA_UNIDADE_RESTRITA = 2
MOA_UNIDADE_INDISPONIVEL = 3

# Agendamentos
AGENDAMENTO_INDISPONIBILIZAR = 1
AGENDAMENTO_ALTERAR_NV_ALVO = 2
AGENDAMENTO_ALTERAR_POT_LIMITE_TODAS_AS_UGS = 3
AGENDAMENTO_BAIXAR_POT_UGS_MINIMO = 4
AGENDAMENTO_NORMALIZAR_POT_UGS_MINIMO = 5

AGENDAMENTO_UG1_ALTERAR_POT_LIMITE = 102
AGENDAMENTO_UG1_FORCAR_ESTADO_DISPONIVEL = 103
AGENDAMENTO_UG1_FORCAR_ESTADO_INDISPONIVEL = 104
AGENDAMENTO_UG1_FORCAR_ESTADO_MANUAL = 105
AGENDAMENTO_UG1_FORCAR_ESTADO_RESTRITO = 106

AGENDAMENTO_UG2_ALTERAR_POT_LIMITE = 202
AGENDAMENTO_UG2_FORCAR_ESTADO_DISPONIVEL = 203
AGENDAMENTO_UG2_FORCAR_ESTADO_INDISPONIVEL = 204
AGENDAMENTO_UG2_FORCAR_ESTADO_MANUAL = 205
AGENDAMENTO_UG2_FORCAR_ESTADO_RESTRITO = 206

AGENDAMENTO_DISPARAR_MENSAGEM_TESTE = 777
MODO_ESCOLHA_MANUAL = 2

AGENDAMENTO_LISTA_BLOQUEIO_UG1 = [
    AGENDAMENTO_UG1_ALTERAR_POT_LIMITE,
    AGENDAMENTO_UG1_FORCAR_ESTADO_DISPONIVEL,
    AGENDAMENTO_UG1_FORCAR_ESTADO_INDISPONIVEL,
    AGENDAMENTO_UG1_FORCAR_ESTADO_MANUAL,
    AGENDAMENTO_UG1_FORCAR_ESTADO_RESTRITO
]

AGENDAMENTO_LISTA_BLOQUEIO_UG2 = [
    AGENDAMENTO_UG2_ALTERAR_POT_LIMITE,
    AGENDAMENTO_UG2_FORCAR_ESTADO_DISPONIVEL,
    AGENDAMENTO_UG2_FORCAR_ESTADO_INDISPONIVEL,
    AGENDAMENTO_UG2_FORCAR_ESTADO_MANUAL,
    AGENDAMENTO_UG2_FORCAR_ESTADO_RESTRITO
]


REG_UG1_EntradasDigitais_MXI_RV_MaquinaParada = 0  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_RV_VeloMenor30 = 1  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_RV_VeloMaior90 = 2  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_RV_Trip = 3  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_AVR_Trip = 4  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_AVR_FalhaInterna = 5  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_AVR_Ligado = 6  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_PotenciaNula = 7  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_Falta125Vcc = 8  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_DisjGeradorInserido = 9  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_DisjGeradorAberto = 10  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_DisjGeradorFechado = 11  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_EmergPainelAtuada = 12  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_Falta125VccCom = 13  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_Falta125VccAlimVal = 14  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FalhaDisjTpsProt = 15  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_ReleBloqA86HAtuado = 16  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_ReleBloqA86MAtuado = 17  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_SEL700G_Atuado = 18  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_SEL700G_FalhaInterna = 19  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_Falta125VccQPCUG2 = 20  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_Falta125VccQPCUG3 = 21  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_NivelMAltoPocoDren = 22  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_DijAlimAVRLig = 23  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FreioPastilhaGasta = 24  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FreioPressNormal = 25  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FreioDesaplicado = 26  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FreioAplicado = 27  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_Reserva254 = 28  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FreioCmdRemoto = 29  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FreioFiltroSaturado = 30  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FreioSemEnergia = 31  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHRV_PressCriticaPos321 = 32  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHRV_PressMinimaPos322 = 33  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHRV_PressNominalPos323 = 34  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHRV_Reserva263 = 35  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHRV_Reserva264 = 36  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FiltroPresSujo75Troc = 37  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FiltroPresSujo100Sujo = 38  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FiltroRetSujo75Troc = 39  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FiltroRetSujo100Sujo = 40  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35 = 41  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHRV_NivOleominimoPos36 = 42  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHRV_PressaoEqual = 43  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_ValvBorbTravada = 44  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_ValvBorbDestravada = 45  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_ValvBorbFechada = 46  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_ValvBorbAberta = 47  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_ValvBorbADeriva = 48  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_ValvByPassFechada = 49  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_ValvByPassAberta = 50  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_DistribuidorFechado = 51  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FluxInjAguaPos14 = 52  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_PresInjAguaPos15 = 53  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_SobreVeloMecPos18 = 54  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FaltaFluxoOleoMc = 55  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_PalhetasDesal = 56  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_FaltaFluxTroc = 57  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_FaltaPressTroc = 58  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_Filt1PresSujo75Troc = 59  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo = 60  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_Filt2PresSujo75Troc = 61  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo = 62  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_NivelCritOleo = 63  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_NivelminOleo = 64  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FiltroPressaoBbaMecSj75 = 65  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100 = 66  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_FaltaFluxoBbaMec = 67  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro = 68  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_FluxoMcTras = 69  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_PressPos37 = 70  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_Reserva307 = 71  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_Bomba1Ligada = 72  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_Bomba2Ligada = 73  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_CompressorLigado = 74  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHRV_Bomba1Ligada = 75  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHRV_Bomba2Ligada = 76  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel = 77  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_QCAUG_Disj52A1Lig = 78  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_QCAUG_TripDisj52A1 = 79  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_TripBomba1 = 80  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHLM_TripBomba2 = 81  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_TripPartRes = 82  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHRV_TripBomba1 = 83  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_UHRV_TripBomba2 = 84  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_TripAlimPainelFreio = 85  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_PainelFreioStatus = 86  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_QCAUG_TripDisjAgrup = 87  # Op02 (Read Input Status)
REG_UG1_EntradasDigitais_MXI_QCAUG1_Remoto = 88  # Op02 (Read Input Status)

REG_UG1_RetornosDigitais_MXR_TensaoEstabilizada = 128  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_EmergenciaViaSuper = 129  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_SeqManual = 130  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_SeqAutomatica = 131  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PartindoEmAuto = 132  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_ParandoEmAuto = 133  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_TripEletrico = 134  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_TripMecanico = 135  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_ValvSeg_Energizadas = 136  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_FalhaAcionAbertValvBorb = 137  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_FalhaAcionFechaValvBorb = 138  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_FalhaAcionAbertValvByPass = 139  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_FalhaAcionFechaValvByPass = 140  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_UHRV_CondOK_M1 = 141  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_UHRV_CondOK_M2 = 142  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_UHLM_CondOK_M1 = 143  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_UHLM_CondOK_M2 = 144  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_Bombas_UHRV_Ligada = 145  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1 = 146  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2 = 147  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1 = 148  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2 = 149  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_UHRV_PressaoOK = 150  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_UHRV_BbaM1Princ = 151  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_UHLM_BbaM1Princ = 152  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_Filtros_Manual = 153  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_FalhaAcionRT = 154  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_RV_CondOK = 155  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_RT_CondOK = 156  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_AVR_HabRefExterna = 157  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_AVR_ControleFP = 158  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_UHLM_Ligada = 159  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_Filtro1Sel = 160  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_Filtro2Sel = 161  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_FalhaAcionCompressor = 162  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_FalhaAcionFreio = 163  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_TripTempGaxeteiro = 164  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_TripTempMcGuiaRadial = 165  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_TripTempMcGuiaEscora = 166  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_TripTempMcGuiaContraEscora = (
    167  # Op02 (Read Input Status)
)
REG_UG1_RetornosDigitais_MXR_TripTempUHRV = 168  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_TripTempUHLM = 169  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_TripVibr1 = 170  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_TripVibr2 = 171  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_FalhaIbntDisjGer = 172  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_AbortaPartida = 173  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_TempoPartidaExc = 174  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_ValvInjArRotorLig = 175  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_ValvInjArRotorAuto = 176  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PreCondPartidaOK = 177  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoLigaValvSeg = 178  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoDeslValvSeg = 179  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoAbreValvBorb = 180  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoFechaValvBorb = 181  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoLigaUHRV = 182  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoDesligaUHRV = 183  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoLigaRT = 184  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoDesligaRT = 185  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoLigaRV = 186  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoDesligaRV = 187  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoAbreValvByPass = 188  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoFechaValvByPass = 189  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoLigaUHLM = 190  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoDesligaUHLM = 191  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoAbreDisjuntor = 192  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoLigaFreioPara = 193  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoDeslFreioPart = 194  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoSincroniza = 195  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_700G_EN = 196  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_700G_Trip = 197  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_700G_TLED_01 = 198  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_700G_TLED_02 = 199  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_700G_TLED_03 = 200  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_700G_TLED_04 = 201  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_700G_TLED_05 = 202  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_700G_TLED_06 = 203  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_SincronismoHab = 204  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_CLP_Falha = 205  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_Remota_Falha = 206  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoLigaFreioPart = 207  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_ArComprimPressBaixa = 208  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_ArComprimPressAlta = 209  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_PassoRetiraCarga = 210  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_RV_RefRemHabilitada = 211  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_FalhaComunG1TDA = 212  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_Q_Negativa = 213  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_UG1_StsBloqueio = 214  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_TripPressaoCaixaEspiral = 215  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_Trip_PBCE_Habilitado = 216  # Op02 (Read Input Status)
REG_UG1_ComandosDigitais_MXW_ResetGeral = 0  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_ResetReleBloq86H = 1  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_ResetReleBloq86M = 2  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_ResetRele700G = 3  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_EmergenciaViaSuper = 4  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_ResetReleRT = 5  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_ResetRV = 6  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_AumentaTensaoRT = 7  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_DiminuiTensaoRT = 8  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_HabControleFP = 9  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_DesabControleFP = 10  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_HabRefExterna = 11  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_DesHabRefExterna = 12  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_AumentaFreq = 13  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_DiminuiFreq = 14  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_HabFiltro1 = 15  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_DesabFiltro1 = 16  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_HabFiltro2 = 17  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_DesabFiltro2 = 18  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_Filtros_Manual = 19  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_Filtros_Auto = 20  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_RV_Liga = 21  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_RV_Desliga = 22  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_RT_Liga = 23  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_RT_Desliga = 24  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_AbreValvBorb = 25  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_FechaValvBorb = 26  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_AbreValvByPass = 27  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_FechaValvByPass = 28  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_UHRV_LigaBbaM1 = 29  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_UHRV_DesligaBbaM1 = 30  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_UHRV_LigaBbaM2 = 31  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_UHRV_DesligaBbaM2 = 32  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_UHRV_SelM1Princ = 33  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_UHRV_SelM2Princ = 34  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_UHLM_LigaBbaM1 = 35  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_UHLM_DesligaBbaM1 = 36  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_UHLM_LigaBbaM2 = 37  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_UHLM_DesligaBbaM2 = 38  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_UHLM_SelM1Princ = 39  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_UHLM_SelM2Princ = 40  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_HabSeqAuto = 41  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_HabSeqManual = 42  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_Freio_Aplica = 43  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_Freio_Desaplica = 44  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_IniciaPartida = 45  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_IniciaParada = 46  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_AbortaPartida = 47  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_ValvSeg_Liga = 48  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_ValvSeg_Desliga = 49  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_DeslDisj52G = 50  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_LigaCompressor = 51  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_DeslCompressor = 52  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_AbreDisj = 53  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_SelValvInjRotorAuto = 54  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_SelValvInjRotorManu = 55  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_LigaValvInjArRotor = 56  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_DeslValvInjArRotor = 57  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_Sincroniza = 58  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_AbortaSincronismo = 59  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_Reset_Hori_Gerador = 60  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_Cala_Sirene = 61  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_RV_RetiraCarga = 62  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_RV_RefRemHabilita = 63  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_RV_RefRemDesabilita = 64  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_Trip_PBCE_Habilita = 65  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_Trip_PBCE_Desabilita = 66  # Op15 (Write multiple coils)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_01 = 24  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_02 = 25  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_03 = 26  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_04 = 27  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_05 = 28  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_06 = 29  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_07 = 30  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_08 = 31  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_09 = 32  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_10 = 33  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_11 = 34  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_12 = 35  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_PM_710_Tensao_AB = 36  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_PM_710_Tensao_BC = 37  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_PM_710_Tensao_CA = 38  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_PM_710_Corrente_A = 39  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_PM_710_Corrente_B = 40  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_PM_710_Corrente_C = 41  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_PM_710_Frequencia = 42  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_PM_710_Fator_Potencia = 43  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_PM_710_Potencia_Aparente = (
    44  # Op04 (Read Input Regs - 3x)
)
REG_UG1_RetornosAnalogicos_MWR_PM_710_Potencia_Ativa = 45  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_PM_710_Potencia_Reativa = (
    46  # Op04 (Read Input Regs - 3x)
)
REG_UG1_RetornosAnalogicos_MWR_Horimetro_Gerador = 51  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Horimetro_Gerador_min = 52  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Estabiliz_Tensao = 49  # Op04 (Read Input Regs - 3x)
REG_UG1_EntradasAnalogicas_MRR_PosicaoDistribuidor = (
    0  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_Velocidade = 1  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG1_EntradasAnalogicas_MRR_Reserva01 = 2  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG1_EntradasAnalogicas_MRR_Reserva02 = 3  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG1_EntradasAnalogicas_MRR_PressAguaVedEixo = (
    4  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_PressDifCaixaExpiral = (
    5  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_PressK1CaixaExpiral = (
    6  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_PressK1Succao = (
    7  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_TempGaxetas = (
    8  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_TempMcGuiaRadial = (
    9  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_TempMcGuiaEscora = (
    10  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_TempMcGuiaContraEscora = (
    11  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_VibMcGuiaRadial = (
    12  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_VibMcGuiaAxial = (
    13  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_UHRV_TempOleo = (
    14  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_UHRV_Pressao = (
    15  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_UHLM_TempOleo = (
    16  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_PressaoArComp = (
    17  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_VazEntrOleoMcDiant = (
    18  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_VazEntrOleoMcTras = (
    19  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_EntradasAnalogicas_MRR_Reserva04 = 20  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG1_EntradasAnalogicas_MRR_Reserva05 = 21  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG1_EntradasAnalogicas_MRR_Reserva06 = 22  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG1_EntradasAnalogicas_MRR_Reserva07 = 23  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG1_SaidasAnalogicas_MWW_Reserva01 = 0  # Scale - Op16 (Preset Multiple Regs - 4x)
REG_UG1_SaidasAnalogicas_MWW_SPPotAtiva = 1  # Scale - Op16 (Preset Multiple Regs - 4x)
REG_UG1_SaidasAnalogicas_MWW_Reserva03 = 2  # Scale - Op16 (Preset Multiple Regs - 4x)
REG_UG1_SaidasAnalogicas_MWW_Reserva04 = 3  # Scale - Op16 (Preset Multiple Regs - 4x)
REG_UG1_RetornosAnalogicos_Float_MWR_PM_710_Energia_Reativa_Consumida = (
    149  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_RetornosAnalogicos_Float_MWR_PM_710_Energia_Ativa_Consumida = (
    151  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_RetornosAnalogicos_Float_MWR_PM_710_Energia_Reativa_Fornecida = (
    153  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG1_RetornosAnalogicos_Float_MWR_PM_710_Energia_Ativa_Fornecida = (
    155  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)

REG_UG2_EntradasDigitais_MXI_RV_MaquinaParada = 0  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_RV_VeloMenor30 = 1  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_RV_VeloMaior90 = 2  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_RV_Trip = 3  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_AVR_Trip = 4  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_AVR_FalhaInterna = 5  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_AVR_Ligado = 6  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_PotenciaNula = 7  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_Falta125Vcc = 8  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_DisjGeradorInserido = 9  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_DisjGeradorAberto = 10  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_DisjGeradorFechado = 11  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_EmergPainelAtuada = 12  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_Falta125VccQPCUG1 = 13  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_Falta125VccQPCUG3 = 00000  # Op02 (Read Input Status) # verificar
REG_UG2_EntradasDigitais_MXI_Falta125VccAlimVal = 14  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FalhaDisjTpsProt = 15  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_ReleBloqA86HAtuado = 16  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_ReleBloqA86MAtuado = 17  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_SEL700G_Atuado = 18  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_SEL700G_FalhaInterna = 19  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_Reserva244 = 20  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_Reserva245 = 21  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_NivelMAltoPocoDren = 22  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_DijAlimAVRLig = 23  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FreioPastilhaGasta = 24  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FreioPressNormal = 25  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FreioDesaplicado = 26  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FreioAplicado = 27  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_Reserva254 = 28  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FreioCmdRemoto = 29  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FreioFiltroSaturado = 30  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FreioSemEnergia = 31  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHRV_PressCriticaPos321 = 32  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHRV_PressMinimaPos322 = 33  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHRV_PressNominalPos323 = 34  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHRV_Reserva263 = 35  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHRV_Reserva264 = 36  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FiltroPresSujo75Troc = 37  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FiltroPresSujo100Sujo = 38  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FiltroRetSujo75Troc = 39  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FiltroRetSujo100Sujo = 40  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHRV_NivOleoCriticoPos35 = 41  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHRV_NivOleominimoPos36 = 42  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHRV_PressaoEqual = 43  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_ValvBorbTravada = 44  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_ValvBorbDestravada = 45  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_ValvBorbFechada = 46  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_ValvBorbAberta = 47  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_ValvBorbADeriva = 48  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_ValvByPassFechada = 49  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_ValvByPassAberta = 50  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_DistribuidorFechado = 51  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FluxInjAguaPos14 = 52  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_PresInjAguaPos15 = 53  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_SobreVeloMecPos18 = 54  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FaltaFluxoOleoMc = 55  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_PalhetasDesal = 56  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_FaltaFluxTroc = 57  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_FaltaPressTroc = 58  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_Filt1PresSujo75Troc = 59  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_Filt1PresSujo100Sujo = 60  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_Filt2PresSujo75Troc = 61  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_Filt2PresSujo100Sujo = 62  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_NivelCritOleo = 63  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_NivelminOleo = 64  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FiltroPressaoBbaMecSj75 = 65  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FiltroPressaoBbaMecSj100 = 66  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FaltaFluxoBbaMec = 67  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_FluxoMcDianteiro = 68  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_FluxoMcTras = 69  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_PressPos37 = 70  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_Reserva307 = 71  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_Bomba1Ligada = 72  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_Bomba2Ligada = 73  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_PartResLigada = 74  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHRV_Bomba1Ligada = 75  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHRV_Bomba2Ligada = 76  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_QCAUG_Falha380VcaPainel = 77  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_QCAUG_Disj52A1Lig = 78  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_QCAUG_TripDisj52A1 = 79  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_TripBomba1 = 80  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_TripBomba2 = 81  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_TripPartRes = 82  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHRV_TripBomba1 = 83  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHRV_TripBomba2 = 84  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_TripAlimPainelFreio = 85  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_PainelFreioStatus = 86  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_QCAUG_TripDisjAgrup = 87  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_QCAUG2_Remoto = 88  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_TensaoEstabilizada = 128  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_EmergenciaViaSuper = 129  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_SeqManual = 130  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_SeqAutomatica = 131  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PartindoEmAuto = 132  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_ParandoEmAuto = 133  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_TripEletrico = 134  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_TripMecanico = 135  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_ValvSeg_Energizadas = 136  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_FalhaAcionAbertValvBorb = 137  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_FalhaAcionFechaValvBorb = 138  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_FalhaAcionAbertValvByPass = 139  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_FalhaAcionFechaValvByPass = 140  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_UHRV_CondOK_M1 = 141  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_UHRV_CondOK_M2 = 142  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_UHLM_CondOK_M1 = 143  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_UHLM_CondOK_M2 = 144  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_Bombas_UHRV_Ligada = 145  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM1 = 146  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_UHRV_FalhaAcionBbaM2 = 147  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM1 = 148  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_UHLM_FalhaAcionBbaM2 = 149  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_UHRV_PressaoOK = 150  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_UHRV_BbaM1Princ = 151  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_UHLM_BbaM1Princ = 152  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_Filtros_Manual = 153  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_FalhaAcionRT = 154  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_RV_CondOK = 155  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_RT_CondOK = 156  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_AVR_HabRefExterna = 157  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_AVR_ControleFP = 158  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_UHLM_Ligada = 159  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_Filtro1Sel = 160  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_Filtro2Sel = 161  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_QCAUGFalhaAcionPartRes = 162  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_FalhaAcionFreio = 163  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_TripTempGaxeteiro = 164  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_TripTempMcGuiaRadial = 165  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_TripTempMcGuiaEscora = 166  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_TripTempMcGuiaContraEscora = (
    167  # Op02 (Read Input Status)
)
REG_UG2_RetornosDigitais_MXR_TripTempUHRV = 168  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_TripTempUHLM = 169  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_TripVibr1 = 170  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_TripVibr2 = 171  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_FalhaIbntDisjGer = 172  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_AbortaPartida = 173  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_TempoPartidaExc = 174  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_ValvInjArRotorLig = 175  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_ValvInjArRotorAuto = 176  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PreCondPartidaOK = 177  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoLigaValvSeg = 178  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoDeslValvSeg = 179  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoAbreValvBorb = 180  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoFechaValvBorb = 181  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoLigaUHRV = 182  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoDesligaUHRV = 183  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoLigaRT = 184  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoDesligaRT = 185  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoLigaRV = 186  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoDesligaRV = 187  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoAbreValvByPass = 188  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoFechaValvByPass = 189  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoLigaUHLM = 190  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoDesligaUHLM = 191  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoAbreDisjuntor = 192  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoLigaFreioPara = 193  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoDeslFreioPart = 194  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoSincroniza = 195  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_700G_EN = 196  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_700G_Trip = 197  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_700G_TLED_01 = 198  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_700G_TLED_02 = 199  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_700G_TLED_03 = 200  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_700G_TLED_04 = 201  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_700G_TLED_05 = 202  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_700G_TLED_06 = 203  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_SincronismoHab = 204  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_CLP_Falha = 205  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_Remota_Falha = 206  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_PassoLigaFreioPart = 207  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_RV_RetiraCarga = 208  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_RV_RefRemHabilitada = 209  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_FalhaComunG2TDA = 210  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_Q_Negativa = 211  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_UG2_StsBloqueio = 212  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_TripPressaoCaixaEspiral = 213  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_Trip_PBCE_Habilitado = 214  # Op02 (Read Input Status)
REG_UG2_ComandosDigitais_MXW_ResetGeral = 0  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_ResetReleBloq86H = 1  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_ResetReleBloq86M = 2  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_ResetRele700G = 3  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_EmergenciaViaSuper = 4  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_ResetReleRT = 5  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_ResetRV = 6  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_AumentaTensaoRT = 7  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_DiminuiTensaoRT = 8  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_HabControleFP = 9  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_DesabControleFP = 10  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_HabRefExterna = 11  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_DesHabRefExterna = 12  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_AumentaFreq = 13  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_DiminuiFreq = 14  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_HabFiltro1 = 15  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_DesabFiltro1 = 16  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_HabFiltro2 = 17  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_DesabFiltro2 = 18  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_Filtros_Manual = 19  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_Filtros_Auto = 20  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_RV_Liga = 21  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_RV_Desliga = 22  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_RT_Liga = 23  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_RT_Desliga = 24  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_AbreValvBorb = 25  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_FechaValvBorb = 26  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_AbreValvByPass = 27  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_FechaValvByPass = 28  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_UHRV_LigaBbaM1 = 29  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_UHRV_DesligaBbaM1 = 30  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_UHRV_LigaBbaM2 = 31  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_UHRV_DesligaBbaM2 = 32  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_UHRV_SelM1Princ = 33  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_UHRV_SelM2Princ = 34  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_UHLM_LigaBbaM1 = 35  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_UHLM_DesligaBbaM1 = 36  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_UHLM_LigaBbaM2 = 37  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_UHLM_DesligaBbaM2 = 38  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_UHLM_SelM1Princ = 39  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_UHLM_SelM2Princ = 40  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_HabSeqAuto = 41  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_HabSeqManual = 42  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_Freio_Aplica = 43  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_Freio_Desaplica = 44  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_IniciaPartida = 45  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_IniciaParada = 46  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_AbortaPartida = 47  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_ValvSeg_Liga = 48  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_ValvSeg_Desliga = 49  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_DeslDisj52G = 50  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_QCAUG_LigaPartRes = 51  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_QCAUG_DeslPartRes = 52  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_AbreDisj = 53  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_SelValvInjRotorAuto = 54  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_SelValvInjRotorManu = 55  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_LigaValvInjArRotor = 56  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_DeslValvInjArRotor = 57  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_Sincroniza = 58  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_AbortaSincronismo = 59  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_Reset_Hori_Gerador = 60  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_Cala_Sirene = 61  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_RetiraCarga = 62  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_RV_RetiraCarga = 63  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_RV_RefRemHabilita = 64  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_RV_RefRemDesabilita = 65  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_Trip_PBCE_Habilita = 66  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_Trip_PBCE_Desabilita = 67  # Op15 (Write multiple coils)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_01 = 24  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_02 = 25  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_03 = 26  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_04 = 27  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_05 = 28  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_06 = 29  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_07 = 30  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_08 = 31  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_09 = 32  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_10 = 33  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_11 = 34  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_12 = 35  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_PM_710_Tensao_AB = 36  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_PM_710_Tensao_BC = 37  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_PM_710_Tensao_CA = 38  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_PM_710_Corrente_A = 39  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_PM_710_Corrente_B = 40  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_PM_710_Corrente_C = 41  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_PM_710_Frequencia = 42  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_PM_710_Fator_Potencia = 43  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_PM_710_Potencia_Aparente = (
    44  # Op04 (Read Input Regs - 3x)
)
REG_UG2_RetornosAnalogicos_MWR_PM_710_Potencia_Ativa = 45  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_PM_710_Potencia_Reativa = (
    46  # Op04 (Read Input Regs - 3x)
)
REG_UG2_RetornosAnalogicos_MWR_Horimetro_Gerador = 51  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Horimetro_Gerador_min = 52  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Estabiliz_Tensao = 49  # Op04 (Read Input Regs - 3x)
REG_UG2_EntradasAnalogicas_MRR_PosicaoDistribuidor = (
    0  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_Velocidade = 1  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG2_EntradasAnalogicas_MRR_Reserva01 = 2  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG2_EntradasAnalogicas_MRR_Reserva02 = 3  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG2_EntradasAnalogicas_MRR_PressAguaVedEixo = (
    4  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_PressDifCaixaExpiral = (
    5  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_PressK1CaixaExpiral = (
    6  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_PressK1Succao = (
    7  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_TempGaxetas = (
    8  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_TempMcGuiaRadial = (
    9  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_TempMcGuiaEscora = (
    10  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_TempMcGuiaContraEscora = (
    11  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_VibMcGuiaRadial = (
    12  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_VibMcGuiaAxial = (
    13  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_UHRV_TempOleo = (
    14  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_UHRV_Pressao = (
    15  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_UHLM_TempOleo = (
    16  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_Reserva03 = 17  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG2_EntradasAnalogicas_MRR_VazEntrOleoMcDiant = (
    18  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_VazEntrOleoMcTras = (
    19  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_EntradasAnalogicas_MRR_Reserva04 = 20  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG2_EntradasAnalogicas_MRR_Reserva05 = 21  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG2_EntradasAnalogicas_MRR_Reserva06 = 22  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG2_EntradasAnalogicas_MRR_Reserva07 = 23  # Scale 0.1 - Op04 (Read Input Regs - 3x)
REG_UG2_SaidasAnalogicas_MWW_Reserva01 = 0  # Scale - Op16 (Preset Multiple Regs - 4x)
REG_UG2_SaidasAnalogicas_MWW_SPPotAtiva = 1  # Scale - Op16 (Preset Multiple Regs - 4x)
REG_UG2_SaidasAnalogicas_MWW_Reserva03 = 2  # Scale - Op16 (Preset Multiple Regs - 4x)
REG_UG2_SaidasAnalogicas_MWW_Reserva04 = 3  # Scale - Op16 (Preset Multiple Regs - 4x)
REG_UG2_RetornosAnalogicos_Float_MWR_PM_710_Energia_Reativa_Consumida = (
    149  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_RetornosAnalogicos_Float_MWR_PM_710_Energia_Ativa_Consumida = (
    151  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_RetornosAnalogicos_Float_MWR_PM_710_Energia_Reativa_Fornecida = (
    153  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_UG2_RetornosAnalogicos_Float_MWR_PM_710_Energia_Ativa_Fornecida = (
    155  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)


REG_SA_EntradasAnalogicas_MRR_SA_Reserva07 = 15  # Scale - Op04 (Read Input Regs - 3x)
REG_SA_EntradasAnalogicas_MRR_SA_QCAP_TensaoT = (
    14  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_EntradasAnalogicas_MRR_SA_QCAP_TensaoS = (
    13  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_EntradasAnalogicas_MRR_SA_QCAP_TensaoR = (
    12  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_EntradasAnalogicas_MRR_SA_CBU01_TensaoBarra = (
    11  # Scale - Op04 (Read Input Regs - 3x)
)
REG_SA_EntradasAnalogicas_MRR_SA_CBU01_CorrenteBarra = (
    10  # Scale - Op04 (Read Input Regs - 3x)
)
REG_SA_EntradasAnalogicas_MRR_SA_QCCP_Tensao = 9  # Scale - Op04 (Read Input Regs - 3x)
REG_SA_EntradasAnalogicas_MRR_SA_QCCP_Corrente = (
    8  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_EntradasAnalogicas_MRR_SA_Reserva06 = 7  # Scale - Op04 (Read Input Regs - 3x)
REG_SA_EntradasAnalogicas_MRR_SA_Reserva05 = 6  # Scale - Op04 (Read Input Regs - 3x)
REG_SA_EntradasAnalogicas_MRR_SA_Reserva04 = 5  # Scale - Op04 (Read Input Regs - 3x)
REG_SA_EntradasAnalogicas_MRR_SA_Reserva03 = 4  # Scale - Op04 (Read Input Regs - 3x)
REG_SA_EntradasAnalogicas_MRR_SA_NivelSuccao = (
    3  # Scale 0.01 - Op04 (Read Input Regs - 3x)
)
REG_SA_EntradasAnalogicas_MRR_HoraLigaGerador = 2  # Op04 (Read Input Regs - 3x)
REG_SA_EntradasAnalogicas_MRR_SA_TE_TempEnrolamento = (
    1  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_EntradasAnalogicas_MRR_SA_TE_TempOleo = (
    0  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_EntradasDigitais_MXI_SA_Reserva180 = 0  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Reserva181 = 1  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_SEL787_Trip = 2  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_SEL787_FalhaInterna = 3  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_SEL311_Trip = 4  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_SEL311_Falha = 5  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_MRU3_Trip = 6  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_MRU3_Falha = 7  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_MRL1_Trip = 8  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_CTE_Falta125Vcc = 9  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_CTE_Secc89TE_Fechada = 10  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_CTE_Secc89TE_Aberta = 11  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Disj52G1_Aberto = 12  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Disj52G2_Aberto = 13  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Disj52G3_Aberto = 14  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Fechado = 15  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Aberto = 16  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa = 17  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa = (
    18  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Local = 19  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_MolaDescarregada = (
    20  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiCom = (
    21  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiMot = (
    22  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobFecham = (
    23  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert1 = (
    24  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert2 = (
    25  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb1 = (
    26  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb2 = (
    27  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_Secc1_Fechada = 28  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Secc1_Aberta = 29  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Secc2_Fechada = 30  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Secc2_Aberta = 31  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Secc3_Fechada = 32  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Secc3_Aberta = 33  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Secc1_Remoto = 34  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Secc2_Remoto = 35  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Secc3_Remoto = 36  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeDetectorGas = 37  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeNivelMaxOleo = 38  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeAlivioPressao = (
    39  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeTempOleo = 40  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeTempEnrolamento = (
    41  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_TE_AlarmeDesligamento = 42  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_TE_Falha = 43  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_TE_VentilacaoLig = 44  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_TE_VentilacaoDeslig = 45  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_TE_VentilacaoDef = 46  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsProt = 47  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincr = 48  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG1 = 49  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG2 = 50  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_FalhaDisjTPsSincrG3 = 51  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Disj52G1Selecionado = 52  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Disj52G2Selecionado = 53  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Disj52G3Selecionado = 54  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Disj52G1Sincronizado = 55  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Disj52G2Sincronizado = 56  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Disj52G3Sincronizado = 57  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Reserva252 = 58  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Reserva253 = 59  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Reserva254 = 60  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Reserva255 = 61  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Reserva256 = 62  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Reserva257 = 63  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_CSA1_Secc_Fechada = 64  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_CSA1_Secc_Aberta = 65  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_CSA1_FusivelQueimado = 66  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_CSA1_FaltaTensao125Vcc = (
    67  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_QCADE_BombasDng_Desliga = (
    68  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_QCADE_Nivel2 = 69  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCADE_Nivel3 = 70  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCADE_Nivel4 = 71  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCADE_NivelMuitoAlto = 72  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCADE_Disj52E1Fechado = 73  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCADE_Disj52E1Trip = 74  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCADE_Falha220VCA = 75  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCADE_BombaDng1_Falha = 76  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCADE_BombaDng2_Falha = 77  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCADE_BombaDng3_Falha = 78  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCADE_BombaDng1_Ligada = (
    79  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_QCADE_BombaDng2_Ligada = (
    80  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_QCADE_BombaDng3_Ligada = (
    81  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_QCADE_BombasDng_Auto = 82  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Reserva283 = 83  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QLCF_Disj52EFechado = 84  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QLCF_Disj52ETrip = 85  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QLCF_TripDisjAgrup = 86  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Reserva287 = 87  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCCP_Disj72EFechado = 88  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCCP_Disj72ETrip = 89  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCCP_Falta125Vcc = 90  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCCP_TripDisjAgrup = 91  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_MSS_EmergAtuada = 92  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_MSS_FalhaSwitch = 93  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_MSS_FalhaConvCACCEntr = 94  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_MSS_FalhaConvCACCRedeCA = (
    95  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_MSS_FalhaConvCACCSaidaCA = (
    96  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_QCAP_Falta125Vcc = 97  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCAP_TripDisjAgrup = 98  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52A1Fechado = 99  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52A1Falha = 100  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52EFechado = 101  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52EFalha = 102  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteGE = (
    103  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_QCAP_TensaoPresenteTSA = (
    104  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_QCAP_Automatico = 105  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCAP_SubtensaoBarraGeral = (
    106  # Op02 (Read Discrete Inputs)
)
REG_SA_EntradasDigitais_MXI_SA_Reserva313 = 107  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Reserva314 = 108  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Reserva315 = 109  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Reserva316 = 110  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_Reserva317 = 111  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_GMG_Alarme = 112  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_GMG_Trip = 113  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_GMG_Operacao = 114  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_GMG_BaixoComb = 115  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_GMG_Automatico = 116  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_GMG_DisjFechado = 117  # Op02 (Read Discrete Inputs)
REG_SA_ComandosDigitais_MXW_ResetGeral = 0  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Liga_Secc1 = 1  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Desliga_Secc1 = 2  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Liga_Secc2 = 3  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Desliga_Secc2 = 4  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Liga_Secc3 = 5  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Desliga_Secc3 = 6  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Liga_BbaDren1 = 7  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Desliga_BbaDren1 = 8  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Liga_BbaDren2 = 9  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Desliga_BbaDren2 = 10  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Liga_BbaDren3 = 11  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Desliga_BbaDren3 = 12  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_ResetRele787 = 13  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_ResetRele59N = 14  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_ResetRele311 = 15  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_ResetReleMRL1 = 16  # Scale - Op15 (Write multiple coils)
#REG_SA_ComandosDigitais_MXW_Liga_DJ1 = 17  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Desliga_DJ1 = 18  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Liga_Disj52A1 = 19  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Desliga_Disj52A1 = 20  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Liga_Disj52E = 21  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Desliga_Disj52E = 22  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_GMG_Liga = 23  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_GMG_Desl = 24  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_QCAP_Autom = 25  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_QCAP_Manual = 26  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Cala_Sirene = 27  # Scale - Op15 (Write multiple coils)
REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_AB = (
    16  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_BC = (
    17  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_CA = (
    18  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM_810_Corrente_A = (
    19  # Scale 0.01 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM_810_Corrente_B = (
    20  # Scale 0.01 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM_810_Corrente_C = (
    21  # Scale 0.01 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM_810_Frequencia = (
    22  # Scale 0.001 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM_810_Fator_Potencia = (
    23  # Scale 0.001 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM_810_Potencia_Aparente = (
    24  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM_810_Potencia_Reativa = (
    25  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM_810_Potencia_Ativa = 26  # Op04 (Read Input Regs - 3x)
REG_SA_RetornosAnalogicos_MWR_PM1_710_Tensao_AB = (
    27  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM1_710_Tensao_BC = (
    28  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM1_710_Tensao_CA = (
    29  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM1_710_Corrente_A = (
    30  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM1_710_Corrente_B = (
    31  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM1_710_Corrente_C = (
    32  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM1_710_Frequencia = (
    33  # Scale 0.001 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM1_710_Fator_Potencia = (
    34  # Scale 0.001 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM1_710_Potencia_Aparente = (
    35  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM1_710_Potencia_Reativa = (
    36  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM1_710_Potencia_Ativa = (
    37  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_Reserva43 = 38  # Op04 (Read Input Regs - 3x)
REG_SA_RetornosAnalogicos_MWR_Reserva44 = 39  # Op04 (Read Input Regs - 3x)
REG_SA_RetornosAnalogicos_MWR_Reserva45 = 40  # Op04 (Read Input Regs - 3x)
REG_SA_RetornosAnalogicos_MWR_PM2_710_Tensao_AB = (
    41  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM2_710_Tensao_BC = (
    42  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM2_710_Tensao_CA = (
    43  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM2_710_Corrente_A = (
    44  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM2_710_Corrente_B = (
    45  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM2_710_Corrente_C = (
    46  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM2_710_Frequencia = (
    47  # Scale 0.001 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM2_710_Fator_Potencia = 48  # Op04 (Read Input Regs - 3x)
REG_SA_RetornosAnalogicos_MWR_PM2_710_Potencia_Aparente = (
    49  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM2_710_Potencia_Reativa = (
    50  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM2_710_Potencia_Ativa = 51  # Op04 (Read Input Regs - 3x)
REG_SA_RetornosAnalogicos_MWR_Reserva61 = 52  # Op04 (Read Input Regs - 3x)
REG_SA_RetornosAnalogicos_MWR_Reserva62 = 53  # Op04 (Read Input Regs - 3x)
REG_SA_RetornosAnalogicos_MWR_Reserva63 = 54  # Op04 (Read Input Regs - 3x)
REG_SA_RetornosAnalogicos_MWR_CorrenteBaixa1 = (
    55  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_CorrenteBaixa2 = (
    56  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_CorrenteBaixa3 = (
    57  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_CorrenteAlta1 = (
    58  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_CorrenteAlta2 = (
    59  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_CorrenteAlta3 = (
    60  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_CorrenteNeutro = (
    61  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_SEL787_Targets = 62  # Op04 (Read Input Regs - 3x)
REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit00 = (
    63  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit01 = (
    64  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit02 = (
    65  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit03 = (
    66  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit04 = (
    67  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit05 = (
    68  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit06 = (
    69  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_SEL787_Targets_Links_Bit07 = (
    70  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosDigitais_MXR_BbaDren1_FalhaAcion = 168  # Op02 (Read Input Status - 1x)
REG_SA_RetornosDigitais_MXR_BbaDren2_FalhaAcion = 169  # Op02 (Read Input Status - 1x)
REG_SA_RetornosDigitais_MXR_BbaDren3_FalhaAcion = 170  # Op02 (Read Input Status - 1x)
REG_SA_RetornosDigitais_MXR_Timeout_Sincronismo = 171  # Op02 (Read Input Status - 1x)
REG_SA_RetornosDigitais_MXR_DJ1_FalhaInt = 172  # Op02 (Read Input Status - 1x)
REG_SA_RetornosDigitais_MXR_CLP_Falha = 173  # Op02 (Read Input Status - 1x)
REG_SA_RetornosDigitais_MXR_Remota_Falha = 174  # Op02 (Read Input Status - 1x)
REG_SA_RetornosDigitais_MXR_SA_GMG_FalhaAcion = 175  # Op02 (Read Input Status - 1x)
REG_SA_RetornosDigitais_MXR_SA_QCAP_Autom = 176  # Op02 (Read Input Status - 1x)
REG_SA_RetornosDigitais_MXR_FalhaComunSETDA = 177  # Op02 (Read Input Status - 1x)
REG_SA_SaidasAnalogicas_MWW_TempoLigar = 0  # Op03 Read Holding Regs - 4x
REG_SA_RetornosAnalogicos_Float_MWR_PM_810_Energia_Reativa_Consumida = (
    149  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_Float_MWR_PM_810_Energia_Ativa_Consumida = (
    151  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_Float_MWR_PM_810_Energia_Reativa_Fornecida = (
    153  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_Float_MWR_PM_810_Energia_Ativa_Fornecida = (
    155  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_Float_MWR_PM1_710_Energia_Reativa_Consumida = (
    157  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_Float_MWR_PM1_710_Energia_Ativa_Consumida = (
    159  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_Float_MWR_PM1_710_Energia_Reativa_Fornecida = (
    161  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_Float_MWR_PM1_710_Energia_Ativa_Fornecida = (
    163  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_Float_MWR_PM2_710_Energia_Reativa_Consumida = (
    165  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_Float_MWR_PM2_710_Energia_Ativa_Consumida = (
    167  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_Float_MWR_PM2_710_Energia_Reativa_Fornecida = (
    169  # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_Float_MWR_PM2_710_Energia_Ativa_Fornecida = (
    171  # Op04 (Read Input Regs - 3x)
)
REG_TDA_EntradasDigitais_MXI_QcataDisj52EAberto = 0  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_QcataDisj52ETrip = 1  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_QcataDisj52ETripDisjSai = 2  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_QcataDisj52EFalha380VCA = 3  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_DefeitoLimpaGrades = 4  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva65 = 5  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva66 = 6  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva67 = 7  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva70 = 8  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva71 = 9  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva72 = 10  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva73 = 11  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva74 = 12  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva75 = 13  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva76 = 14  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva77 = 15  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva80 = 16  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva81 = 17  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva82 = 18  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva83 = 19  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva84 = 20  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva85 = 21  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva86 = 22  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva87 = 23  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva90 = 24  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva91 = 25  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva92 = 26  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva93 = 27  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva94 = 28  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva95 = 29  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva96 = 30  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXI_Reserva97 = 31  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXR_1_AlmNivelBaixo = 32  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXR_1_TripNivelBaixo = 33  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXR_1_TripNivelCritico = 34  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXR_2_AlmNivelBaixo = 35  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXR_2_TripNivelBaixo = 36  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXR_2_TripNivelCritico = 37  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXR_3_AlmNivelBaixo = 38  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXR_3_TripNivelBaixo = 39  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXR_3_TripNivelCritico = 40  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasDigitais_MXR_VertendoAlm = 41  # Op02 (Read Discrete Inputs)
REG_TDA_EntradasAnalogicas_MRR_NivelAntesGrade = (
    0  # Scale 0.01 - Op04 (Read Input Regs - 3x)
)
REG_TDA_EntradasAnalogicas_MRR_NivelDepoisGrade = (
    1  # Scale 0.01 - Op04 (Read Input Regs - 3x)
)
REG_TDA_EntradasAnalogicas_MRR_Reserva01 = 2  # Op04 (Read Input Regs - 3x)
REG_TDA_EntradasAnalogicas_MRR_Reserva02 = 3  # Op04 (Read Input Regs - 3x)
REG_TDA_EntradasAnalogicas_MRR_Reserva03 = 4  # Op04 (Read Input Regs - 3x)
REG_TDA_EntradasAnalogicas_MRR_Reserva04 = 5  # Op04 (Read Input Regs - 3x)
REG_TDA_EntradasAnalogicas_MRR_Reserva05 = 6  # Op04 (Read Input Regs - 3x)
REG_TDA_EntradasAnalogicas_MRR_Reserva06 = 7  # Op04 (Read Input Regs - 3x)
REG_TDA_EntradasAnalogicas_MRR_NivelAntesGradeFiltrado = (
    8  # Scale 0.01 - Op04 (Read Input Regs - 3x)
)
REG_TDA_EntradasAnalogicas_MWR_NumUGTabela1 = 9  # Op04 (Read Input Regs - 3x)
REG_TDA_EntradasAnalogicas_MWR_NumUGTabela2 = 10  # Op04 (Read Input Regs - 3x)
REG_TDA_EntradasAnalogicas_MWR_NumUGTabela3 = 11  # Op04 (Read Input Regs - 3x)
REG_TDA_RetornosDigitais_MXR_FalhaParametroNivel = 42  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_UG1_ContNivelHabilitado = 43  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_UG1_CmdResetAutoNivel = 44  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_UG1_CmdPartidaAutoNivel = 45  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_UG2_ContNivelHabilitado = 46  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_UG2_CmdResetAutoNivel = 47  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_UG2_CmdPartidaAutoNivel = 48  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_UG3_ContNivelHabilitado = 49  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_UG3_CmdResetAutoNivel = 50  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_UG3_CmdPartidaAutoNivel = 51  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_ExcedidoReligUG1 = 52  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_ExcedidoReligUG2 = 53  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_ExcedidoReligUG3 = 54  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_ExcedidoReligSE = 55  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_StatusControleNivel = 56  # Op02 (Read Discrete Inputs)
REG_TDA_RetornosDigitais_MXR_StatusRelig52L = 57  # Op02 (Read Discrete Inputs)
REG_TDA_ComandosDigitais_MXW_ResetGeral = (
    0  # Escrita de Word Simples (Preset Single Register - 4x)
)
REG_TDA_ComandosDigitais_MXW_Hab_Nivel = (
    1  # Escrita de Word Simples (Preset Single Register - 4x)
)
REG_TDA_ComandosDigitais_MXW_Desab_Nivel = (
    2  # Escrita de Word Simples (Preset Single Register - 4x)
)
REG_TDA_ComandosDigitais_MXW_Hab_Religamento52L = (
    3  # Escrita de Word Simples (Preset Single Register - 4x)
)
REG_TDA_ComandosDigitais_MXW_Desab_Religamento52L = (
    4  # Escrita de Word Simples (Preset Single Register - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Nivel_1_Religamento = (
    0  # Scale 0.01 - OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Nivel_1_Alto = (
    1  # Scale 0.01 - OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Nivel_1_Medio = (
    2  # Scale 0.01 - OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Nivel_1_Baixo = (
    3  # Scale 0.01 - OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Nivel_2_Religamento = (
    4  # Scale 0.01 - OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Nivel_2_Alto = (
    5  # Scale 0.01 - OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Nivel_2_Medio = (
    6  # Scale 0.01 - OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Nivel_2_Baixo = (
    7  # Scale 0.01 - OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Nivel_3_Religamento = (
    8  # Scale 0.01 - OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Nivel_3_Alto = (
    9  # Scale 0.01 - OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Nivel_3_Medio = (
    10  # Scale 0.01 - OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Nivel_3_Baixo = (
    11  # Scale 0.01 - OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Potencia_1_Alta = (
    12  # OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Potencia_1_Media = (
    13  # OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Potencia_1_Baixa = (
    14  # OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Potencia_2_Alta = (
    15  # OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Potencia_2_Media = (
    16  # OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Potencia_2_Baixa = (
    17  # OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Potencia_3_Alta = (
    18  # OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Potencia_3_Media = (
    19  # OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_SaidasAnalogicas_MRW_Potencia_3_Baixa = (
    20  # OpLeitura de Words (Read Holding Regs - 4x)
)
REG_TDA_NivelMaisCasasAntes = 12  # Scale 400 + 0.0001 X - Op04 (Read Input Regs - 3x)
REG_TDA_NivelMaisCasasDepois = 13  # Scale 400 + 0.0001 X - Op04 (Read Input Regs - 3x)
REG_UG1_COND_PART = 222
REG_UG2_COND_PART = 222



#--------------------------------------------------------------------------------------------------------------------------------------#
#Registradores utilizados na simulação, para voltar aos valores antigos, deletar os comentarios de linha "#antigo->" e manter o número.
REG_UG1_RetornosDigitais_EtapaAux_Sim = 32773
REG_UG1_RetornosDigitais_EtapaAlvo_Sim = 32772

REG_UG1_EntradasAnalogicas_MRR_PressK1CaixaExpiral_MaisCasas = (
    34903 # Scale 0.01 - Op04 (Read Input Regs)
)

REG_UG1_RetornosDigitais_StatusComporta = 34905

REG_UG1_RetrornosAnalogicos_AUX_Condicionadores = 34902
REG_UG1_ComandosDigitais_MXW_EmergenciaViaSuper = 32295 #antigo -> 4  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_IniciaPartida = 32294 #antigo -> 45  # Op15 (Write multiple coils)
REG_UG1_ComandosDigitais_MXW_IniciaParada = 32290 #antigo -> 46  # Op15 (Write multiple coils)
REG_UG1_RetornosDigitais_MXR_TripEletrico = 34904 #antigo -> 134  # Op02 (Read Input Status)
REG_UG1_RetornosDigitais_MXR_TripMecanico = 34198 #antigo -> 135  # Op02 (Read Input Status)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_01 = 32871 #antigo -> 24  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_02 = 32872 #antigo -> 25  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_03 = 32873 #antigo -> 26  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_04 = 32874 #antigo -> 27  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_05 = 32875 #antigo -> 28  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_06 = 32876 #antigo -> 29  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_07 = 32877 #antigo -> 30  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_08 = 32878 #antigo -> 31  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_Temperatura_09 = 32879 #antigo -> 32  # Op04 (Read Input Regs - 3x)
REG_UG1_RetornosAnalogicos_MWR_PM_710_Potencia_Ativa = 32836 #antigo->45  # Op04 (Read Input Regs - 3x)
REG_UG1_SaidasAnalogicas_MWW_SPPotAtiva = 33585 #antigo -> 1  # Scale - Op16 (Preset Multiple Regs - 4x)
REG_UG1_EntradasAnalogicas_MRR_PressK1CaixaExpiral = (
    34903  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)

REG_UG2_RetornosDigitais_EtapaAux_Sim = 42773
REG_UG2_RetornosDigitais_EtapaAlvo_Sim = 42772
REG_UG2_RetornosDigitais_StatusComporta = 44905

REG_UG2_RetrornosAnalogicos_AUX_Condicionadores = 44902
REG_UG2_ComandosDigitais_MXW_EmergenciaViaSuper = 42295 #antigo -> 4  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_IniciaPartida = 42294 #antigo -> 45  # Op15 (Write multiple coils)
REG_UG2_ComandosDigitais_MXW_IniciaParada = 42290 #antigo -> 46  # Op15 (Write multiple coils)
REG_UG2_RetornosDigitais_MXR_TripEletrico = 44904  #antigo -> 134# Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_TripMecanico = 44198  #antigo -> 135 # Op02 (Read Input Status)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_01 = 42871 #antigo -> 24  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_02 = 42872 #antigo -> 25  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_03 = 42873 #antigo -> 26  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_04 = 42874 #antigo -> 27  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_05 = 42875 #antigo -> 28  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_06 = 42876 #antigo -> 29  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_07 = 42877 #antigo -> 30  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_08 = 42878 #antigo -> 31  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_Temperatura_09 = 42879 #antigo -> 32  # Op04 (Read Input Regs - 3x)
REG_UG2_RetornosAnalogicos_MWR_PM_710_Potencia_Ativa = 42836 #antigo ->45  # Op04 (Read Input Regs - 3x)
REG_UG2_SaidasAnalogicas_MWW_SPPotAtiva = 43585 #antigo -> 1  # Scale - Op16 (Preset Multiple Regs - 4x)
REG_UG2_EntradasAnalogicas_MRR_PressK1CaixaExpiral = (
    44903  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)

REG_UG2_EntradasAnalogicas_MRR_PressK1CaixaExpiral_MaisCasas = (
    44903 # Scale 0.01 - Op04 (Read Input Regs)
)

REG_SA_ComandosDigitais_MXW_ResetGeral = 22288 #antigo -> 0  # Scale - Op15 (Write multiple coils)
REG_SA_ComandosDigitais_MXW_Liga_DJ1 = 22293 #antigo -> 17  # Scale - Op15 (Write multiple coils)
REG_SA_RetornosAnalogicos_Medidor_potencia_kw_mp = (
    24900 # Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_AB = (
    22789 #antigo -> 16  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_BC = (
    22790 #antigo -> 17  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)
REG_SA_RetornosAnalogicos_MWR_PM_810_Tensao_CA = (
    22791 #antigo -> 18  # Scale 0.1 - Op04 (Read Input Regs - 3x)
)

REG_SA_RetornosAnalogicos_MWR_PM_810_Potencia_Ativa = 22799  # Op04 (Read Input Regs - 3x)

REG_TDA_NivelMaisCasasAntes = 22766 #antigo -> 12  # Scale 400 + 0.0001 X - Op04 (Read Input Regs - 3x)
REG_TDA_EntradasAnalogicas_MRR_NivelDepoisGrade = (
    22767 # antgo -> 1  # Scale 0.01 - Op04 (Read Input Regs - 3x)
)


REG_UG1_EntradasDigitais_MXI_FreioPastilhaGasta = 30000 # antigo -> 24  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FreioPastilhaGasta = 40000 # antigo -> 24  # Op02 (Read Input Status)

REG_UG1_EntradasDigitais_MXI_FiltroPresSujo75Troc = 30001 # antigo -> 37  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FiltroPresSujo75Troc = 40001 # antigo -> 37  # Op02 (Read Input Status)

REG_UG1_EntradasDigitais_MXI_FiltroRetSujo75Troc = 30002 # antigo -> 39  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FiltroRetSujo75Troc = 40002 # antigo -> 39  # Op02 (Read Input Status)

REG_UG1_EntradasDigitais_MXI_UHLM_Filt1PresSujo75Troc = 30003 # antigo -> 59  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_Filt1PresSujo75Troc = 40003 # antigo -> 59  # Op02 (Read Input Status)

REG_UG1_EntradasDigitais_MXI_UHLM_Filt2PresSujo75Troc = 30004 # antigo -> 61  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_UHLM_Filt2PresSujo75Troc = 40004 # antigo -> 61  # Op02 (Read Input Status)

REG_UG1_EntradasDigitais_MXI_FiltroPressaoBbaMecSj75 = 30005 # antigo -> 65  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_FiltroPressaoBbaMecSj75 = 40005 # antigo -> 65  # Op02 (Read Input Status)

REG_UG1_EntradasDigitais_MXI_TripPartRes = 30006 # antigo -> 82  # Op02 (Read Input Status)
REG_UG2_EntradasDigitais_MXI_TripPartRes = 40006 # antigo -> 82  # Op02 (Read Input Status)

REG_UG1_RetornosDigitais_MXR_FalhaComunG1TDA = 30007 # antigo -> 212  # Op02 (Read Input Status)
REG_UG2_RetornosDigitais_MXR_FalhaComunG2TDA = 40007 # antigo -> 210  # Op02 (Read Input Status)

REG_SA_EntradasDigitais_MXI_SA_QLCF_Disj52EFechado = 20000 # antigo -> 84  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QLCF_Disj52ETrip = 20001 # antigo -> 85  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QLCF_TripDisjAgrup = 20002 # antigo -> 86  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52EFechado = 20003 # antigo -> 101  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_QCAP_SubtensaoBarraGeral = 20004 # antigo -> 106  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_GMG_Alarme = 20005 # antigo -> 112  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_GMG_Trip = 20006 # antigo -> 113  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_GMG_Operacao = 20007 # antigo -> 114  # Op02 (Read Discrete Inputs)
REG_SA_EntradasDigitais_MXI_SA_GMG_BaixoComb = 20008 # antigo -> 115  # Op02 (Read Discrete Inputs)
REG_SA_RetornosDigitais_MXR_BbaDren1_FalhaAcion = 20009 # antigo -> 168  # Op02 (Read Input Status - 1x)
REG_SA_RetornosDigitais_MXR_BbaDren2_FalhaAcion = 20010 # antigo -> 169  # Op02 (Read Input Status - 1x)
REG_SA_RetornosDigitais_MXR_BbaDren3_FalhaAcion = 20011 # antigo -> 170  # Op02 (Read Input Status - 1x)
REG_SA_RetornosDigitais_MXR_SA_GMG_FalhaAcion = 20012 # antigo -> 175  # Op02 (Read Input Status - 1x)
REG_SA_RetornosDigitais_MXR_FalhaComunSETDA = 20013 # antigo -> 177  # Op02 (Read Input Status - 1x)

REG_UG1_UHRV_BOMBA_1_FALHA = 0
REG_UG1_UHRV_BOMBA_1_LIGADA = 0
REG_UG1_UHRV_BOMBA_2_FALHA = 0
REG_UG1_UHRV_BOMBA_2_LIGADA = 0
REG_UG1_UHLM_BOMBA_1_FALHA = 0
REG_UG1_UHLM_BOMBA_1_LIGADA = 0
REG_UG1_UHLM_BOMBA_2_FALHA = 0
REG_UG1_UHLM_BOMBA_2_LIGADA = 0
REG_UG1_52G_MOLHA_CARREGADA = 0
REG_UG1_52G_FECHADO = 0
REG_UG1_CPG_DJ_TPS_MULTIMEDIDOR_REGULADORES_FECHADO = 0
REG_UG1_CPG_DJ_TPS_RELE_PROTECAO_FECHADO = 0
REG_UG1_CPG_UG_PORTA_INTERNA_FECHADA = 0
REG_UG1_CPG_UG_PORTA_TRASEIRA_FECHADA = 0
REG_UG1_UHLM_SEM_NIV_MUITO_BAIXO = 0
REG_UG1_UHLM_SEM_NIV_MUITO_ALTO = 0
REG_UG1_ENTRADA_DIGITAL_RESERVA_4 = 0
REG_UG1_UHLM_PRESSAO_LINHA_OLEO = 0
REG_UG1_UG_ENTRADA_DIGITAL_RESERVA_1 = 0
REG_UG1_UG_ENTRADA_DIGITAL_RESERVA_2 = 0
REG_UG1_UG_ENTRADA_DIGITAL_RESERVA_3 = 0
REG_UG1_UHLM_FILTRO_LIMPO = 0
REG_UG1_UHRV_SEM_NIV_MUITO_BAIXO = 0
REG_UG1_UHRV_FREIO_PRESSURIZADO = 0
REG_UG1_UHRV_FILTRO_LIMPO = 0
REG_UG1_ENTRADA_DIGITAL_RESERVA_3 = 0
REG_UG1_ENTRADA_DIGITAL_RESERVA_1 = 0
REG_UG1_ENTRADA_DIGITAL_RESERVA_2 = 0
REG_UG1_RESISTENCIA_SEM_FALHA = 0
REG_UG1_RESISTENCIA_LIGADA = 0
REG_UG1_CONTATOR_CAMPO_FECHADO = 0
REG_UG1_RELE_700G_TRIP_ATUADO = 0
REG_UG1_RELE_700G_BF_ATUADO = 0
REG_UG1_RELE_700G_WATCHDOG = 0
REG_UG1_RELE_700G_TRANSFERENCIA_DISPARO = 0
REG_UG1_BT_RV_AUMENTA_REFERENCIA = 0
REG_UG1_BT_RV_DIMINUI_REFERENCIA = 0
REG_UG1_BT_RT_AUMENTA_REFERENCIA = 0
REG_UG1_BT_RT_DIMINUI_REFERENCIA = 0
REG_UG1_SINCRONIZADOR_SINCRONIZADO = 0
REG_UG1_BT_PARA_UG = 0
REG_UG1_BT_PARTE_UG = 0
REG_UG1_BT_REARME_FALHAS = 0
REG_UG1_BT_EMERGENCIA_NAO_ATUADO = 0
REG_UG1_SUPERVISAO_BOBINA_52G = 0
REG_UG1_SUPERVISAO_BOBINA_86EH = 0
REG_UG1_RV_RELE_TRIP_NAO_ATUADO = 0
REG_UG1_RV_RELE_ALARME_ATUADO = 0
REG_UG1_RV_RELE_ESTADO_HABILITADO = 0
REG_UG1_RV_RELE_ESTADO_REGULANDO = 0
REG_UG1_RV_RELE_POTENCIA_NULA = 0
REG_UG1_RV_RELE_MAQUINA_PARADA = 0
REG_UG1_RV_RELE_VEL_MENOR_30 = 0
REG_UG1_RV_RELE_VEL_MAIOR_90 = 0
REG_UG1_RV_RELE_DISTRIBUIDOR_ABERTO = 0
REG_UG1_RT_RELE_TRIP_NAO_ATUADO = 0
REG_UG1_RT_RELE_ALARME_ATUADO = 0
REG_UG1_RT_RELE_ESTADO_HABILITADO = 0
REG_UG1_RT_RELE_ESTADO_REGULANDO = 0
REG_UG1_UG_ENTRADA_DIGITAL_RESERVA = 0
REG_UG1_RELE_BLOQUEIO_86EH_DESATUADO = 0
REG_UG1_SUPERVISAO_TENSAO_125VCC = 0
REG_UG1_SUPERVISAO_TENSAO_24VCC = 0
REG_UG1_DISJUNTORES_125VCC_FECHADOS = 0
REG_UG1_DISJUNTORES_24VCC_FECHADOS = 0
REG_UG1_CLP_GERAL_SEM_BLOQUEIO_EXTERNO = 0
REG_UG1_CLP_GERAL_SISTEMA_AGUA_OK = 0
REG_UG1_CLP_GERAL_COM_TENSAO_BARRA_ESSENCIAIS = 0
REG_UG1_COMPORTA_PERMISSIVO_ABERTURA_OK = 0
REG_UG1_ESCOVAS_GASTAS_POLO_POSITIVO = 0
REG_UG1_ESCOVAS_GASTAS_POLO_NEGATIVO = 0
REG_UG1_ENTRADA_DIGITAL_RESERVA_5 = 0
REG_UG1_DISPARO_MECANICO_DESATUADO = 0
REG_UG1_DISPARO_MECANICO_ATUADO = 0
REG_UG1_ENTRADA_DIGITAL_RESERVA_6 = 0
REG_UG1_ENTRADA_DIGITAL_RESERVA_7 = 0
REG_UG1_ENTRADA_DIGITAL_RESERVA_8 = 0
REG_UG1_ENTRADA_DIGITAL_RESERVA_9 = 0
REG_UG1_ENTRADA_DIGITAL_RESERVA_10 = 0
REG_UG1_ENTRADA_DIGITAL_RESERVA_11 = 0
REG_UG1_ACN_52G_PERMITE_FECHAMENTO = 0
REG_UG1_ACN_52G_ABRE = 0
REG_UG1_ACN_REARME_BLOQUEIO_86EH = 0
REG_UG1_ACN_SINCRO_SELECIONA_BARRA_MORTA = 0
REG_UG1_ACN_RESISTENCIA_DESLIGA = 0
REG_UG1_ACN_PERMISSIVO_COMPORTA = 0
REG_UG1_ACN_UHRV_BOMBA_1_LIGA = 0
REG_UG1_ACN_UHRV_BOMBA_2_LIGA = 0
REG_UG1_ACN_UHLM_BOMBA_1_LIGA = 0
REG_UG1_ACN_UHLM_BOMBA_2_LIGA = 0
REG_UG1_ACN_RV_ACIONA_SEM_BLOQUEIO_EXTERNO = 0
REG_UG1_ACN_RV_HABILITA = 0
REG_UG1_ACN_RV_SELECIONA_CONTROLE_ISOLADO = 0
REG_UG1_ACN_RV_ACIONA_ZERA_CARGA = 0
REG_UG1_ACN_RV_RESET_FALHAS = 0
REG_UG1_ACN_RV_AUMENTA_REFERENCIA = 0
REG_UG1_ACN_RV_DIMINUI_REFERENCIA = 0
REG_UG1_ACN_RV_PROGRAMAVEL_1 = 0
REG_UG1_ACN_RT_ACIONA_SEM_BLOQUEIO_EXTERNO = 0
REG_UG1_ACN_RT_HABILITA = 0
REG_UG1_ACN_RT_SELECIONA_CONTROLE_ISOLADO = 0
REG_UG1_ACN_RT_RESET_FALHAS = 0
REG_UG1_ACN_RT_AUMENTA_REFERENCIA = 0
REG_UG1_ACN_RT_DIMINUI_REFERENCIA = 0
REG_UG1_ACN_RT_PROGRAMAVEL_1 = 0
REG_UG1_ACN_SINCRO_HABILITA = 0
REG_UG1_ACN_SAIDA_RESERVA_1 = 0
REG_UG1_ACN_SAIDA_RESERVA_2 = 0
REG_UG1_ACN_APLICA_FREIO = 0
REG_UG1_ACN_ACIONA_VALV_SEG_DISTRIBUIDOR = 0
REG_UG1_ACN_ACIONA_VALV_SEG_ROTOR = 0
REG_UG1_ACN_UHRV_VALVULA_RETORNA_TANQUE = 0
REG_UG1_ACN_SINALIZA_UG_OPERACAO = 0
REG_UG1_ACN_SINALIZA_UG_FALHA = 0
REG_UG1_ACN_SINALIZA_UG_PERMISSIVO = 0
REG_UG1_ACN_SEM_BLOQUEIO_86EH = 0
REG_UG1_ACN_ATUA_BLOQUEIO_86EH_RESERVA_1 = 0
REG_UG1_ACN_ATUA_BLOQUEIO_86EH_RESERVA_2 = 0
REG_UG1_ACN_CLP_GERAL_HABILITA_SISTEMA_AGUA = 0
REG_UG1_ACN_CLP_GERAL_RESERVA_2 = 0
REG_UG1_ACN_CLP_GERAL_RESERVA_3 = 0
REG_UG1_ACN_SAIDA_RESERVA_RESERVA_3 = 0
REG_UG1_ACN_SAIDA_RESERVA_RESERVA_4 = 0
REG_UG1_ACN_SAIDA_RESERVA_RESERVA_5 = 0
REG_UG1_ACN_SAIDA_RESERVA_RESERVA_6 = 0
REG_UG1_ACN_SAIDA_RESERVA_RESERVA_7 = 0
REG_UG1_ACN_SAIDA_RESERVA_RESERVA_8 = 0
REG_UG1_ACN_SAIDA_RESERVA_RESERVA_9 = 0
REG_UG1_TEMP_PONTE_TIRISTORES_FASE_A = 0
REG_UG1_TEMP_PONTE_TIRISTORES_FASE_B = 0
REG_UG1_TEMP_PONTE_TIRISTORES_FASE_C = 0
REG_UG1_TEMP_RESERVA_3 = 0
REG_UG1_TEMP_TRAFO_EXCITACAO = 0
REG_UG1_TEMP_MANCAL_GUIA_GERADOR = 0
REG_UG1_TEMP_UHRV_OLEO = 0
REG_UG1_TEMP_UHLM_OLEO = 0
REG_UG1_TEMP_CASQ_MANCAL_COMBINADO = 0
REG_UG1_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO = 0
REG_UG1_TEMP_1_PATIN_MANCAL_COMBINADO = 0
REG_UG1_TEMP_2_PATIN_MANCAL_COMBINADO = 0
REG_UG1_TEMP_1_MANCAL_GUIA_INTERNO = 0
REG_UG1_TEMP_2_MANCAL_GUIA_INTERNO = 0
REG_UG1_TEMP_GERADOR_NUCLEO = 0
REG_UG1_TEMP_GERADOR_FASE_A = 0
REG_UG1_TEMP_GERADOR_FASE_B = 0
REG_UG1_TEMP_GERADOR_FASE_C = 0
REG_UG1_TEMP_RESERVA_2 = 0
REG_UG1_TEMP_RESERVA = 0
REG_UG1_PRESSAO_ENTRADA_TURBINA = 0
REG_UG1_PRESSAO_REGULAGEM_1_TURBINA = 0
REG_UG1_PRESSAO_VACUOSTATO_SAIDA_RODA = 0
REG_UG1_PRESSAO_VACUOSTATO_SAIDA_SUCCAO = 0
REG_UG1_VIBRACAO_EIXO_X_MANCAL_COMBINADO = 0
REG_UG1_VIBRACAO_EIXO_Y_MANCAL_COMBINADO = 0
REG_UG1_VIBRACAO_EIXO_Z_MANCAL_COMBINADO = 0
REG_UG1_PRESSAO_UHRV_ACUMULADOR = 0
REG_UG1_VIBRACAO_DETECCAO_HORIZONTAL = 0
REG_UG1_VIBRACAO_DETECCAO_VERTICAL = 0
REG_UG1_PRESSAO_REGULAGEM_2_TURBINA = 0
REG_UG1_PRESSAO_DIFERENCIAL_REGULAGEM_TURBINA = 0
REG_UG1_ALM_TEMP_PONTE_FASE_A = 0
REG_UG1_ALM_TEMP_PONTE_FASE_B = 0
REG_UG1_ALM_TEMP_PONTE_FASE_C = 0
REG_UG1_ALM_TEMP_RESERVA_3 = 0
REG_UG1_ALM_TEMP_TRAFO_EXCITACAO = 0
REG_UG1_ALM_TEMP_MANCAL_GUIA = 0
REG_UG1_ALM_TEMP_OLEO_UHRV = 0
REG_UG1_ALM_TEMP_OLEO_UHLM = 0
REG_UG1_ALM_TEMP_CASQ_MANCAL_COMBINADO = 0
REG_UG1_ALM_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO = 0
REG_UG1_ALM_TEMP_1_PATINS_MANCAL_COMBINADO = 0
REG_UG1_ALM_TEMP_2_PATINS_MANCAL_COMBINADO = 0
REG_UG1_ALM_TEMP_1_MANCAL_GUIA_INTERNO = 0
REG_UG1_ALM_TEMP_2_MANCAL_GUIA_INTERNO = 0
REG_UG1_ALM_TEMP_GERADOR_NUCLEO_ESTATORICO = 0
REG_UG1_ALM_TEMP_GERADOR_FASE_A = 0
REG_UG1_ALM_TEMP_GERADOR_FASE_B = 0
REG_UG1_ALM_TEMP_GERADOR_FASE_C = 0
REG_UG1_ALM_TEMP_RESERVA_2 = 0
REG_UG1_ALM_TEMP_RESERVA = 0
REG_UG1_ALM_PRESSAO_ENTRADA_TURBINA = 0
REG_UG1_ALM_PRESSAO_REGULAGEM_1_TURBINA = 0
REG_UG1_ALM_PRESSAO_SAIDA_RODA = 0
REG_UG1_ALM_PRESSAO_SAIDA_SUCCAO = 0
REG_UG1_ALM_VIBRACAO_EIXO_X_MANCAL_COMBINADO = 0
REG_UG1_ALM_VIBRACAO_EIXO_Y_MANCAL_COMBINADO = 0
REG_UG1_ALM_VIBRACAO_EIXO_Z_MANCAL_COMBINADO = 0
REG_UG1_ALM_PRESSAO_ACUMULADOR_UHRV = 0
REG_UG1_ALM_VIBRACAO_DETECCAO_HORIZONTAL = 0
REG_UG1_ALM_VIBRACAO_DETECACAO_VERTICAL = 0
REG_UG1_ALM_PRESSAO_REGULAGEM_2_TURBINA = 0
REG_UG1_ALM_PRESSAO_DIFERENCIAL_REGULAGEM_TURBINA = 0
REG_UG1_TRIP_TEMP_PONTE_FASE_A = 0
REG_UG1_TRIP_TEMP_PONTE_FASE_B = 0
REG_UG1_TRIP_TEMP_PONTE_FASE_C = 0
REG_UG1_TRIP_TEMP_TRAFO_ATERRAMENTO = 0
REG_UG1_TRIP_TEMP_TRAFO_EXCITACAO = 0
REG_UG1_TRIP_TEMP_MANCAL_GUIA = 0
REG_UG1_TRIP_TEMP_OLEO_UHRV = 0
REG_UG1_TRIP_TEMP_OLEO_UHLM = 0
REG_UG1_TRIP_TEMP_CASQ_MANCAL_COMBINADO = 0
REG_UG1_TRIP_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO = 0
REG_UG1_TRIP_TEMP_1_PATINS_MANCAL_COMBINADO = 0
REG_UG1_TRIP_TEMP_2_PATINS_MANCAL_COMBINADO = 0
REG_UG1_TRIP_TEMP_1_MANCAL_GUIA_INTERNO = 0
REG_UG1_TRIP_TEMP_2_MANCAL_GUIA_INTERNO = 0
REG_UG1_TRIP_TEMP_GERADOR_NUCLEO_ESTATORICO = 0
REG_UG1_TRIP_TEMP_GERADOR_FASE_A = 0
REG_UG1_TRIP_TEMP_GERADOR_FASE_B = 0
REG_UG1_TRIP_TEMP_GERADOR_FASE_C = 0
REG_UG1_TRIP_TEMP_GERADOR_SAIDA_AR = 0
REG_UG1_TRIP_TEMP_RESERVA = 0
REG_UG1_TRIP_PRESSAO_ENTRADA_TURBINA = 0
REG_UG1_TRIP_PRESSAO_REGULAGEM_1_TURBINA = 0
REG_UG1_TRIP_PRESSAO_SAIDA_RODA = 0
REG_UG1_TRIP_PRESSAO_SAIDA_SUCCAO = 0
REG_UG1_TRIP_VIBRACAO_EIXO_X_MANCAL_COMBINADO = 0
REG_UG1_TRIP_VIBRACAO_EIXO_Y_MANCAL_COMBINADO = 0
REG_UG1_TRIP_VIBRACAO_EIXO_Z_MANCAL_COMBINADO = 0
REG_UG1_TRIP_PRESSAO_ACUMULADOR_UHRV = 0
REG_UG1_TRIP_VIBRACAO_DETECCAO_HORIZONTAL = 0
REG_UG1_TRIP_VIBRACAO_DETECACAO_VERTICAL = 0
REG_UG1_TRIP_PRESSAO_REGULAGEM_2_TURBINA = 0
REG_UG1_TRIP_PRESSAO_DIFERENCIAL_REGULAGEM_TURBINA = 0
REG_UG1_FALHA_TEMP_PONTE_FASE_A = 0
REG_UG1_FALHA_TEMP_PONTE_FASE_B = 0
REG_UG1_FALHA_TEMP_PONTE_FASE_C = 0
REG_UG1_FALHA_TEMP_RESERVA_3 = 0
REG_UG1_FALHA_TEMP_TRAFO_EXCITACAO = 0
REG_UG1_FALHA_TEMP_MANCAL_GUIA = 0
REG_UG1_FALHA_TEMP_OLEO_UHRV = 0
REG_UG1_FALHA_TEMP_OLEO_UHLM = 0
REG_UG1_FALHA_TEMP_CASQ_MANCAL_COMBINADO = 0
REG_UG1_FALHA_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO = 0
REG_UG1_FALHA_TEMP_1_PATINS_MANCAL_COMBINADO = 0
REG_UG1_FALHA_TEMP_2_PATINS_MANCAL_COMBINADO = 0
REG_UG1_FALHA_TEMP_1_MANCAL_GUIA_INTERNO = 0
REG_UG1_FALHA_TEMP_2_MANCAL_GUIA_INTERNO = 0
REG_UG1_FALHA_TEMP_GERADOR_NUCLEO_ESTATORICO = 0
REG_UG1_FALHA_TEMP_GERADOR_FASE_A = 0
REG_UG1_FALHA_TEMP_GERADOR_FASE_B = 0
REG_UG1_FALHA_TEMP_GERADOR_FASE_C = 0
REG_UG1_FALHA_TEMP_RESERVA_2 = 0
REG_UG1_FALHA_TEMP_RESERVA = 0
REG_UG1_FALHA_PRESSAO_ENTRADA_TURBINA = 0
REG_UG1_FALHA_PRESSAO_REGULAGEM_1_TURBINA = 0
REG_UG1_FALHA_PRESSAO_SAIDA_RODA = 0
REG_UG1_FALHA_PRESSAO_SAIDA_SUCCAO = 0
REG_UG1_FALHA_VIBRACAO_EIXO_X_MANCAL_COMBINADO = 0
REG_UG1_FALHA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO = 0
REG_UG1_FALHA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO = 0
REG_UG1_FALHA_PRESSAO_ACUMULADOR_UHRV = 0
REG_UG1_FALHA_VIBRACAO_DETECCAO_HORIZONTAL = 0
REG_UG1_FALHA_VIBRACAO_DETECACAO_VERTICAL = 0
REG_UG1_FALHA_PRESSAO_REGULAGEM_2_TURBINA = 0
REG_UG1_FALHA_PRESSAO_DIFERENCIAL_REGULAGEM_TURBINA = 0
REG_UG1_CMD_RESET_FALHAS_PASSOS = 0
REG_UG1_CMD_REARME_BLOQUEIO_86M = 0
REG_UG1_CMD_REARME_BLOQUEIO_86E = 0
REG_UG1_CMD_REARME_BLOQUEIO_86H = 0
REG_UG1_CMD_PARTIDA_CMD_DESAPLICA_FREIO = 0
REG_UG1_CMD_PARTIDA_CMD_HAB_UHLM = 0
REG_UG1_CMD_PARTIDA_CMD_HABILITA_SISTEMA_AGUA = 0
REG_UG1_CMD_PARTIDA_CMD_PARTE_RV = 0
REG_UG1_CMD_PARTIDA_CMD_PARTE_RT = 0
REG_UG1_CMD_PARTIDA_CMD_SINCRONISMO = 0
REG_UG1_CMD_PARADA_CMD_ABERTURA_DISJ_MAQUINA = 0
REG_UG1_CMD_PARADA_CMD_PARA_RT = 0
REG_UG1_CMD_PARADA_CMD_PARA_RV_APLICA_FREIO = 0
REG_UG1_CMD_PARADA_CMD_DESABILITA_SISTEMA_AGUA = 0
REG_UG1_CMD_PARADA_CMD_DESABILITA_UHLM = 0
REG_UG1_CMD_PARADA_EMERGENCIA = 0
REG_UG1_CMD_HABILITA_CONTROLE_NIVEL = 0
REG_UG1_CMD_DESABILITA_CONTROLE_NIVEL = 0
REG_UG1_CMD_HABILITA_CONTROLE_NIVEL_ESCALONADO = 0
REG_UG1_CMD_DESABILITA_CONTROLE_NIVEL_ESCALONADO = 0
REG_UG1_CMD_HABILITA_PARADA_POR_NIVEL = 0
REG_UG1_CMD_DESABILITA_PARADA_POR_NIVEL = 0
REG_UG1_CMD_UHRV_SEL_OPERACAO_AUTOMATICA = 0
REG_UG1_CMD_UHRV_SEL_OPERACAO_MANUTENCAO = 0
REG_UG1_CMD_UHRV_LIGA_BOMBA_1 = 0
REG_UG1_CMD_UHRV_DESL_BOMBA_1 = 0
REG_UG1_CMD_UHRV_LIGA_BOMBA_2 = 0
REG_UG1_CMD_UHRV_DESL_BOMBA_2 = 0
REG_UG1_CMD_UHRV_REARME_FALHAS = 0
REG_UG1_CMD_UHRV_SEL_BOMBA_1_PRINCIPAL = 0
REG_UG1_CMD_UHRV_SEL_BOMBA_2_PRINCIPAL = 0
REG_UG1_CMD_UHRV_RESET_HORIMETRO_BOMBA_1 = 0
REG_UG1_CMD_UHRV_RESET_HORIMETRO_BOMBA_2 = 0
REG_UG1_CMD_UHRV_RESERVA_1 = 0
REG_UG1_CMD_UHRV_RESERVA_2 = 0
REG_UG1_CMD_UHRV_RESERVA_3 = 0
REG_UG1_CMD_UHRV_RESERVA_4 = 0
REG_UG1_CMD_UHRV_RESERVA_5 = 0
REG_UG1_CMD_UHLM_REARME_FALHAS = 0
REG_UG1_CMD_UHLM_SEL_OPERACAO_AUTOMATICA = 0
REG_UG1_CMD_UHLM_SEL_OPERACAO_MANUTENCAO = 0
REG_UG1_CMD_UHLM_LIGA_BOMBA_1 = 0
REG_UG1_CMD_UHLM_DESL_BOMBA_1 = 0
REG_UG1_CMD_UHLM_LIGA_BOMBA_2 = 0
REG_UG1_CMD_UHLM_DESL_BOMBA_2 = 0
REG_UG1_CMD_UHLM_SEL_BOMBA_1_PRINCIPAL = 0
REG_UG1_CMD_UHLM_SEL_BOMBA_2_PRINCIPAL = 0
REG_UG1_CMD_UHLM_RESET_HORIMETRO_BOMBA_1 = 0
REG_UG1_CMD_UHLM_RESET_HORIMETRO_BOMBA_2 = 0
REG_UG1_CMD_UHLM_RESERVA_1 = 0
REG_UG1_CMD_UHLM_RESERVA_2 = 0
REG_UG1_CMD_UHLM_RESERVA_3 = 0
REG_UG1_CMD_UHLM_RESERVA_4 = 0
REG_UG1_CMD_UHLM_RESERVA_5 = 0
REG_UG1_CMD_RESET_HORIMETRO_UG = 0
REG_UG1_CMD_UG_RESERVA_1 = 0
REG_UG1_CMD_UG_RESERVA_2 = 0
REG_UG1_CMD_UG_RESERVA_3 = 0
REG_UG1_CMD_UG_RESERVA_4 = 0
REG_UG1_CMD_UG_RESERVA_5 = 0
REG_UG1_CMD_UG_RESERVA_6 = 0
REG_UG1_CMD_UG_RESERVA_7 = 0
REG_UG1_CMD_UG_RESERVA_8 = 0
REG_UG1_CMD_UG_RESERVA_9 = 0
REG_UG1_PRE_CONDICOES_PARTIDA_OK = 0
REG_UG1_PERMISSIVOS_UHLM_OK = 0
REG_UG1_PERMISSIVOS_SISTEMA_AGUA_OK = 0
REG_UG1_PERMISSIVOS_RV_OK = 0
REG_UG1_PERMISSIVOS_RT_OK = 0
REG_UG1_PERMISSIVOS_SINCRONISMO_OK = 0
REG_UG1_BLOQUEIO_86M_ATUADO = 0
REG_UG1_BLOQUEIO_86E_ATUADO = 0
REG_UG1_BLOQUEIO_86H_ATUADO = 0
REG_UG1_HABILITA_FREIO = 0
REG_UG1_HABILITA_UHLM = 0
REG_UG1_HABILITA_RV = 0
REG_UG1_HABILITA_RT = 0
REG_UG1_PARTIDA_BLOQUEIO_FREIO_PASSO_A_FRENTE = 0
REG_UG1_PART_ATUAL_DESAPLICANDO_FREIO = 0
REG_UG1_PART_ATUAL_HABILITANDO_UHLM = 0
REG_UG1_PART_ATUAL_HABILITANDO_SISTEMA_AGUA = 0
REG_UG1_PART_ATUAL_PARTINDO_RV = 0
REG_UG1_PART_ATUAL_PARTINDO_RT = 0
REG_UG1_PART_ATUAL_SINCRONIZANDO = 0
REG_UG1_PART_ATUAL_RESERVA_01 = 0
REG_UG1_PART_ATUAL_RESERVA_02 = 0
REG_UG1_PART_ATUAL_RESERVA_03 = 0
REG_UG1_PART_ATUAL_RESERVA_04 = 0
REG_UG1_PART_ATUAL_RESERVA_05 = 0
REG_UG1_PART_ATUAL_RESERVA_06 = 0
REG_UG1_PART_ATUAL_RESERVA_07 = 0
REG_UG1_PART_ATUAL_RESERVA_08 = 0
REG_UG1_PART_ATUAL_RESERVA_09 = 0
REG_UG1_PART_ATUAL_RESERVA_10 = 0
REG_UG1_PARA_ATUAL_DESCARGA_POT = 0
REG_UG1_PARA_ATUAL_PARANDO_RT = 0
REG_UG1_PARA_ATUAL_PARANDO_RV_APLICANDO_FREIO = 0
REG_UG1_PARA_ATUAL_DESABILITANDO_SISTEMA_AGUA = 0
REG_UG1_PARA_ATUAL_DESABILITANDO_UHLM = 0
REG_UG1_PARA_ATUAL_RESERVA_01 = 0
REG_UG1_PARA_ATUAL_RESERVA_02 = 0
REG_UG1_PARA_ATUAL_RESERVA_03 = 0
REG_UG1_PARA_ATUAL_RESERVA_04 = 0
REG_UG1_PARA_ATUAL_RESERVA_05 = 0
REG_UG1_PARA_ATUAL_RESERVA_06 = 0
REG_UG1_PARA_ATUAL_RESERVA_07 = 0
REG_UG1_PARA_ATUAL_RESERVA_08 = 0
REG_UG1_PARA_ATUAL_RESERVA_09 = 0
REG_UG1_PARA_ATUAL_RESERVA_10 = 0
REG_UG1_PART_CONCLUIDA_DESPLICA_FREIO = 0
REG_UG1_PART_CONCLUIDA_HABILITA_UHLM = 0
REG_UG1_PART_CONCLUIDA_HABILITA_SISTEMA_AGUA = 0
REG_UG1_PART_CONCLUIDA_PARTE_RV = 0
REG_UG1_PART_CONCLUIDA_PARTE_RT = 0
REG_UG1_PART_CONCLUIDA_SINCRONIZADO = 0
REG_UG1_PART_CONCLUIDA_RESERVA_01 = 0
REG_UG1_PART_CONCLUIDA_RESERVA_02 = 0
REG_UG1_PART_CONCLUIDA_RESERVA_03 = 0
REG_UG1_PART_CONCLUIDA_RESERVA_04 = 0
REG_UG1_PART_CONCLUIDA_RESERVA_05 = 0
REG_UG1_PART_CONCLUIDA_RESERVA_06 = 0
REG_UG1_PART_CONCLUIDA_RESERVA_07 = 0
REG_UG1_PART_CONCLUIDA_RESERVA_08 = 0
REG_UG1_PART_CONCLUIDA_RESERVA_09 = 0
REG_UG1_PART_CONCLUIDA_RESERVA_10 = 0
REG_UG1_PARA_CONCLUIDA_DESCARGA_POT = 0
REG_UG1_PARA_CONCLUIDA_PARA_RT = 0
REG_UG1_PARA_CONCLUIDA_PARA_RV_APLICA_FREIO = 0
REG_UG1_PARA_CONCLUIDA_DESABILITA_SISTEMA_AGUA = 0
REG_UG1_PARA_CONCLUIDA_DESABILITA_UHLM = 0
REG_UG1_PARA_CONCLUIDA_RESERVA_01 = 0
REG_UG1_PARA_CONCLUIDA_RESERVA_02 = 0
REG_UG1_PARA_CONCLUIDA_RESERVA_03 = 0
REG_UG1_PARA_CONCLUIDA_RESERVA_04 = 0
REG_UG1_PARA_CONCLUIDA_RESERVA_05 = 0
REG_UG1_PARA_CONCLUIDA_RESERVA_06 = 0
REG_UG1_PARA_CONCLUIDA_RESERVA_07 = 0
REG_UG1_PARA_CONCLUIDA_RESERVA_08 = 0
REG_UG1_PARA_CONCLUIDA_RESERVA_09 = 0
REG_UG1_PARA_CONCLUIDA_RESERVA_10 = 0
REG_UG1_FALHA_PARTIDA_DESAPLICA_FREIO = 0
REG_UG1_FALHA_PARTIDA_HABILITA_UHLM = 0
REG_UG1_FALHA_PARTIDA_HABILITA_SISTEMA_AGUA = 0
REG_UG1_FALHA_PARTIDA_PARTE_RV = 0
REG_UG1_FALHA_PARTIDA_PARTE_RT = 0
REG_UG1_FALHA_PARTIDA_SINCRONISMO = 0
REG_UG1_FALHA_PARTIDA_RESERVA_1 = 0
REG_UG1_FALHA_PARTIDA_RESERVA_2 = 0
REG_UG1_FALHA_PARTIDA_RESERVA_3 = 0
REG_UG1_FALHA_PARTIDA_RESERVA_4 = 0
REG_UG1_FALHA_PARTIDA_RESERVA_5 = 0
REG_UG1_FALHA_PARTIDA_RESERVA_6 = 0
REG_UG1_FALHA_PARTIDA_RESERVA_7 = 0
REG_UG1_FALHA_PARTIDA_RESERVA_8 = 0
REG_UG1_FALHA_PARTIDA_RESERVA_9 = 0
REG_UG1_FALHA_PARTIDA_RESERVA_10 = 0
REG_UG1_RV_FALHA_HABILITAR_RV = 0
REG_UG1_RV_FALHA_PARTIR_RV = 0
REG_UG1_RV_FALHA_DESABILITAR_RV = 0
REG_UG1_RV_FALHA_PARAR_MAQUINA = 0
REG_UG1_RV_FALHA_FECHAR_DISTRIBUIDOR = 0
REG_UG1_STT_RV_RESERVA_1 = 0
REG_UG1_STT_RV_RESERVA_2 = 0
REG_UG1_STT_RV_RESERVA_3 = 0
REG_UG1_STT_RV_RESERVA_4 = 0
REG_UG1_STT_RV_RESERVA_5 = 0
REG_UG1_STT_RV_RESERVA_6 = 0
REG_UG1_STT_RV_RESERVA_7 = 0
REG_UG1_STT_RV_RESERVA_8 = 0
REG_UG1_STT_RV_RESERVA_9 = 0
REG_UG1_STT_RV_RESERVA_10 = 0
REG_UG1_STT_RV_RESERVA_11 = 0
REG_UG1_RT_FALHA_HABILITAR = 0
REG_UG1_RT_FALHA_PARTIR = 0
REG_UG1_RT_FALHA_DESABILITAR = 0
REG_UG1_STT_RT_RESERVA_1 = 0
REG_UG1_STT_RT_RESERVA_2 = 0
REG_UG1_STT_RT_RESERVA_3 = 0
REG_UG1_STT_RT_RESERVA_4 = 0
REG_UG1_STT_RT_RESERVA_5 = 0
REG_UG1_STT_RT_RESERVA_6 = 0
REG_UG1_STT_RT_RESERVA_7 = 0
REG_UG1_STT_RT_RESERVA_8 = 0
REG_UG1_STT_RT_RESERVA_9 = 0
REG_UG1_STT_RT_RESERVA_10 = 0
REG_UG1_STT_RT_RESERVA_11 = 0
REG_UG1_STT_RT_RESERVA_12 = 0
REG_UG1_STT_RT_RESERVA_13 = 0
REG_UG1_PARTIDA_BLOQUEIO_UHL_PASSO_A_FRENTE = 0
REG_UG1_PARTIDA_BLOQUEIO_SISTEMA_AGUA_PASSO_A_FRENTE = 0
REG_UG1_PARADA_BLOQUEIO_DESCARGA_POTENCIA = 0
REG_UG1_PARADA_BLOQUEIO_ABERTURA_DISJUNTOR = 0
REG_UG1_PARADA_FINALIZADA = 0
REG_UG1_MAQUINA_PARTINDO = 0
REG_UG1_GIRANDO_DESEXCITADA = 0
REG_UG1_PRONTA_PARA_SINCRONIZAR = 0
REG_UG1_OPERANDO_SINCRONIZADA = 0
REG_UG1_MAQUINA_PARANDO_PASSO = 0
REG_UG1_PARANDO_SEM_REJEICAO = 0
REG_UG1_PARANDO_EMERGENCIA = 0
REG_UG1_CONTROLE_NIVEL_HABILITADO = 0
REG_UG1_CONTROLE_ESCALONADO_HABILITADO = 0
REG_UG1_PARADA_POR_NIVEL_HABILITADA = 0
REG_UG1_UHLM_BOMBA_1_PRINCIPAL = 0
REG_UG1_UHLM_BOMBA_2_PRINCIPAL = 0
REG_UG1_UHLM_BOMBA_1_DISPONIVEL = 0
REG_UG1_UHLM_BOMBA_2_DISPONIVEL = 0
REG_UG1_UHLM_UNIDADE_EM_MANUTENCAO = 0
REG_UG1_UHLM_TIME_OUT_LIGA_BOMBA_1 = 0
REG_UG1_UHLM_TIME_OUT_DESL_BOMBA_1 = 0
REG_UG1_UHLM_TIME_OUT_LIGA_BOMBA_2 = 0
REG_UG1_UHLM_TIME_OUT_DESL_BOMBA_2 = 0
REG_UG1_UHLM_FALHA_PRESSAO_LINHA_B1 = 0
REG_UG1_UHLM_FALHA_PRESSAO_LINHA_B2 = 0
REG_UG1_UHLM_FALHA_PRESSOSTATO_LINHA = 0
REG_UG1_UHLM_STT_RESERVA_02 = 0
REG_UG1_UHLM_STT_RESERVA_01 = 0
REG_UG1_UHLM_STT_RESERVA_0 = 0
REG_UG1_UHLM_STT_RESERVA_1 = 0
REG_UG1_UHLM_STT_RESERVA_2 = 0
REG_UG1_UHLM_STT_RESERVA_3 = 0
REG_UG1_UHLM_STT_RESERVA_4 = 0
REG_UG1_UHLM_STT_RESERVA_5 = 0
REG_UG1_UHLM_STT_RESERVA_6 = 0
REG_UG1_UHLM_STT_RESERVA_7 = 0
REG_UG1_UHLM_STT_RESERVA_8 = 0
REG_UG1_UHLM_STT_RESERVA_9 = 0
REG_UG1_UHLM_STT_RESERVA_10 = 0
REG_UG1_UHLM_STT_RESERVA_11 = 0
REG_UG1_UHLM_STT_RESERVA_12 = 0
REG_UG1_UHLM_STT_RESERVA_13 = 0
REG_UG1_UHLM_STT_RESERVA_14 = 0
REG_UG1_UHLM_STT_RESERVA_15 = 0
REG_UG1_UHLM_STT_RESERVA_16 = 0
REG_UG1_UHLM_STT_RESERVA_17 = 0
REG_UG1_UHRV_UNIDADE_EM_MANUTENCAO = 0
REG_UG1_UHRV_BOMBA_1_PRINCIPAL = 0
REG_UG1_UHRV_BOMBA_2_PRINCIPAL = 0
REG_UG1_UHRV_BOMBA_1_DISPONIVEL = 0
REG_UG1_UHRV_BOMBA_2_DISPONIVEL = 0
REG_UG1_UHRV_TIME_OUT_LIGA_BOMBA_1 = 0
REG_UG1_UHRV_TIME_OUT_DESL_BOMBA_1 = 0
REG_UG1_UHRV_TIME_OUT_LIGA_BOMBA_2 = 0
REG_UG1_UHRV_TIME_OUT_DESL_BOMBA_2 = 0
REG_UG1_UHRV_FALHA_PRESSURIZA_BOMBA_1 = 0
REG_UG1_UHRV_FALHA_PRESSURIZA_BOMBA_2 = 0
REG_UG1_UHRV_FREIO_APLICANDO_FREIO = 0
REG_UG1_UHRV_FALHA_PRESSURIZAR_FREIO = 0
REG_UG1_UHRV_FALHA_DESPRESSURIZAR_FREIO = 0
REG_UG1_UHRV_STT_RESERVA_1 = 0
REG_UG1_UHRV_STT_RESERVA_2 = 0
REG_UG1_UHRV_STT_RESERVA_3 = 0
REG_UG1_UHRV_STT_RESERVA_4 = 0
REG_UG1_UHRV_STT_RESERVA_5 = 0
REG_UG1_UHRV_STT_RESERVA_6 = 0
REG_UG1_UHRV_STT_RESERVA_7 = 0
REG_UG1_UHRV_STT_RESERVA_8 = 0
REG_UG1_UHRV_STT_RESERVA_9 = 0
REG_UG1_UHRV_STT_RESERVA_10 = 0
REG_UG1_UHRV_STT_RESERVA_11 = 0
REG_UG1_UHRV_STT_RESERVA_12 = 0
REG_UG1_UHRV_STT_RESERVA_13 = 0
REG_UG1_UHRV_STT_RESERVA_14 = 0
REG_UG1_UHRV_STT_RESERVA_15 = 0
REG_UG1_UHRV_STT_RESERVA_16 = 0
REG_UG1_UHRV_STT_RESERVA_17 = 0
REG_UG1_UHRV_STT_RESERVA_18 = 0
REG_UG1_UHLM_OK = 0
REG_UG1_SISTEMA_AGUA_OK = 0
REG_UG1_RV_OK = 0
REG_UG1_RT_OK = 0
REG_UG1_FALHA_HABILITAR_SISTEMA_AGUA = 0
REG_UG1_UHLM_STT_RESERVA_33 = 0
REG_UG1_CP_STT_HEARTBEAT = 0
REG_UG1_CP_STT_COMPORTA_OPERANDO = 0
REG_UG1_CP_STT_FECHAMENTO_FINALIZADO = 0
REG_UG1_CP_STT_FALHA_GRAVE = 0
REG_UG1_CP_STT_FALHA_NIVEL_MONTATE = 0
REG_UG1_CP_STT_FALHA_NIVEL_JUSANTE_GRADE = 0
REG_UG1_CP_STT_06 = 0
REG_UG1_CP_STT_07 = 0
REG_UG1_CP_STT_08 = 0
REG_UG1_CP_STT_09 = 0
REG_UG1_CP_STT_10 = 0
REG_UG1_CP_STT_11 = 0
REG_UG1_CP_STT_12 = 0
REG_UG1_CP_STT_13 = 0
REG_UG1_CP_STT_14 = 0
REG_UG1_CP_STT_15 = 0
REG_UG1_CP_STT_16 = 0
REG_UG1_CP_STT_17 = 0
REG_UG1_CP_STT_18 = 0
REG_UG1_CP_STT_19 = 0
REG_UG1_CP_STT_20 = 0
REG_UG1_CP_STT_21 = 0
REG_UG1_CP_STT_22 = 0
REG_UG1_CP_STT_23 = 0
REG_UG1_CP_STT_24 = 0
REG_UG1_CP_STT_25 = 0
REG_UG1_CP_STT_26 = 0
REG_UG1_CP_STT_27 = 0
REG_UG1_CP_STT_28 = 0
REG_UG1_CP_STT_29 = 0
REG_UG1_CP_STT_30 = 0
REG_UG1_CP_STT_31 = 0
REG_UG1_HABILITA_SISTEMA_AGUA = 0
REG_UG1_CP_FALHA_CONTROLE_VIDA = 0
REG_UG1_FALSE = 0
REG_UG1_TRUE = 0
REG_UG1_PARANDO_PARCIAL = 0
REG_UG1_STT_UG_RESERVA_13 = 0
REG_UG1_STT_UG_RESERVA_14 = 0
REG_UG1_STT_UG_RESERVA_15 = 0
REG_UG1_STT_UG_RESERVA_16 = 0
REG_UG1_STT_UG_RESERVA_17 = 0
REG_UG1_STT_UG_RESERVA_18 = 0
REG_UG1_STT_UG_RESERVA_19 = 0
REG_UG1_STT_UG_RESERVA_20 = 0
REG_UG1_STT_UG_RESERVA_21 = 0
REG_UG1_STT_UG_RESERVA_22 = 0
REG_UG1_STT_UG_RESERVA_23 = 0
REG_UG1_STT_UG_RESERVA_24 = 0
REG_UG1_STT_UG_RESERVA_25 = 0
REG_UG1_STT_UG_RESERVA_26 = 0
REG_UG1_STT_UG_RESERVA_27 = 0
REG_UG1_STT_UG_RESERVA_28 = 0
REG_UG1_STT_UG_RESERVA_29 = 0
REG_UG1_STT_UG_RESERVA_30 = 0
REG_UG1_STT_UG_RESERVA_31 = 0
REG_UG1_PARA_ATUAL_RESERVA_11 = 0
REG_UG1_PARA_CONCLUIDA_RESERVA_11 = 0
REG_UG1_PARADA_NIVEL = 0
REG_UG1_PARADA_FALHA_MEDICAO_NIVEL = 0
REG_UG1_UG_VAB = 0
REG_UG1_UG_VBC = 0
REG_UG1_UG_VCA = 0
REG_UG1_UG_IA = 0
REG_UG1_UG_IB = 0
REG_UG1_UG_IC = 0
REG_UG1_UG_P = 0
REG_UG1_UG_Q = 0
REG_UG1_UG_S = 0
REG_UG1_UG_F = 0
REG_UG1_UG_FP = 0
REG_UG1_UG_EAP = 0
REG_UG1_UG_EAN = 0
REG_UG1_UG_ERP = 0
REG_UG1_UG_ERN = 0
REG_UG1_BLOQUEIO_CMD_EMERGENCIA = 0
REG_UG1_BLOQUEIO_GIRO_INDEVIDO = 0
REG_UG1_BLOQUEIO_BLOQUEIO_EXTERNO = 0

REG_UG2_CMD_RESET_FALHAS_PASSOS = 0
REG_UG2_CMD_REARME_BLOQUEIO_86M = 0
REG_UG2_CMD_REARME_BLOQUEIO_86E = 0
REG_UG2_CMD_REARME_BLOQUEIO_86H = 0
REG_UG2_CMD_PARTIDA_CMD_DESAPLICA_FREIO = 0
REG_UG2_CMD_PARTIDA_CMD_HAB_UHLM = 0
REG_UG2_CMD_PARTIDA_CMD_HABILITA_SISTEMA_AGUA = 0
REG_UG2_CMD_PARTIDA_CMD_PARTE_RV = 0
REG_UG2_CMD_PARTIDA_CMD_PARTE_RT = 0
REG_UG2_CMD_PARTIDA_CMD_SINCRONISMO = 0
REG_UG2_CMD_PARADA_CMD_ABERTURA_DISJ_MAQUINA = 0
REG_UG2_CMD_PARADA_CMD_PARA_RT = 0
REG_UG2_CMD_PARADA_CMD_PARA_RV_APLICA_FREIO = 0
REG_UG2_CMD_PARADA_CMD_DESABILITA_SISTEMA_AGUA = 0
REG_UG2_CMD_PARADA_CMD_DESABILITA_UHLM = 0
REG_UG2_CMD_PARADA_EMERGENCIA = 0
REG_UG2_CMD_HABILITA_CONTROLE_NIVEL = 0
REG_UG2_CMD_DESABILITA_CONTROLE_NIVEL = 0
REG_UG2_CMD_HABILITA_CONTROLE_NIVEL_ESCALONADO = 0
REG_UG2_CMD_DESABILITA_CONTROLE_NIVEL_ESCALONADO = 0
REG_UG2_CMD_HABILITA_PARADA_POR_NIVEL = 0
REG_UG2_CMD_DESABILITA_PARADA_POR_NIVEL = 0
REG_UG2_CMD_RESET_HORIMETRO_UG = 0
REG_UG2_CMD_UG_RESERVA_1 = 0
REG_UG2_CMD_UG_RESERVA_2 = 0
REG_UG2_CMD_UG_RESERVA_3 = 0
REG_UG2_CMD_UG_RESERVA_4 = 0
REG_UG2_CMD_UG_RESERVA_5 = 0
REG_UG2_CMD_UG_RESERVA_6 = 0
REG_UG2_CMD_UG_RESERVA_7 = 0
REG_UG2_CMD_UG_RESERVA_8 = 0
REG_UG2_CMD_UG_RESERVA_9 = 0
REG_UG2_CMD_UHRV_SEL_OPERACAO_AUTOMATICA = 0
REG_UG2_CMD_UHRV_SEL_OPERACAO_MANUTENCAO = 0
REG_UG2_CMD_UHRV_LIGA_BOMBA_1 = 0
REG_UG2_CMD_UHRV_DESL_BOMBA_1 = 0
REG_UG2_CMD_UHRV_LIGA_BOMBA_2 = 0
REG_UG2_CMD_UHRV_DESL_BOMBA_2 = 0
REG_UG2_CMD_UHRV_REARME_FALHAS = 0
REG_UG2_CMD_UHRV_SEL_BOMBA_1_PRINCIPAL = 0
REG_UG2_CMD_UHRV_SEL_BOMBA_2_PRINCIPAL = 0
REG_UG2_CMD_UHRV_RESET_HORIMETRO_BOMBA_1 = 0
REG_UG2_CMD_UHRV_RESET_HORIMETRO_BOMBA_2 = 0
REG_UG2_CMD_UHRV_RESERVA_1 = 0
REG_UG2_CMD_UHRV_RESERVA_2 = 0
REG_UG2_CMD_UHRV_RESERVA_3 = 0
REG_UG2_CMD_UHRV_RESERVA_4 = 0
REG_UG2_CMD_UHRV_RESERVA_5 = 0
REG_UG2_CMD_UHLM_REARME_FALHAS = 0
REG_UG2_CMD_UHLM_SEL_OPERACAO_AUTOMATICA = 0
REG_UG2_CMD_UHLM_SEL_OPERACAO_MANUTENCAO = 0
REG_UG2_CMD_UHLM_LIGA_BOMBA_1 = 0
REG_UG2_CMD_UHLM_DESL_BOMBA_1 = 0
REG_UG2_CMD_UHLM_LIGA_BOMBA_2 = 0
REG_UG2_CMD_UHLM_DESL_BOMBA_2 = 0
REG_UG2_CMD_UHLM_SEL_BOMBA_1_PRINCIPAL = 0
REG_UG2_CMD_UHLM_SEL_BOMBA_2_PRINCIPAL = 0
REG_UG2_CMD_UHLM_RESET_HORIMETRO_BOMBA_1 = 0
REG_UG2_CMD_UHLM_RESET_HORIMETRO_BOMBA_2 = 0
REG_UG2_CMD_UHLM_RESERVA_1 = 0
REG_UG2_CMD_UHLM_RESERVA_2 = 0
REG_UG2_CMD_UHLM_RESERVA_3 = 0
REG_UG2_CMD_UHLM_RESERVA_4 = 0
REG_UG2_CMD_UHLM_RESERVA_5 = 0
REG_UG2_UHRV_BOMBA_1_FALHA = 0
REG_UG2_UHRV_BOMBA_1_LIGADA = 0
REG_UG2_UHRV_BOMBA_2_FALHA = 0
REG_UG2_UHRV_BOMBA_2_LIGADA = 0
REG_UG2_UHLM_BOMBA_1_FALHA = 0
REG_UG2_UHLM_BOMBA_1_LIGADA = 0
REG_UG2_UHLM_BOMBA_2_FALHA = 0
REG_UG2_UHLM_BOMBA_2_LIGADA = 0
REG_UG2_52G_MOLHA_CARREGADA = 0
REG_UG2_52G_FECHADO = 0
REG_UG2_CPG_DJ_TPS_MULTIMEDIDOR_REGULADORES_FECHADO = 0
REG_UG2_CPG_DJ_TPS_RELE_PROTECAO_FECHADO = 0
REG_UG2_CPG_UG_PORTA_INTERNA_FECHADA = 0
REG_UG2_CPG_UG_PORTA_TRASEIRA_FECHADA = 0
REG_UG2_UHLM_SEM_NIV_MUITO_BAIXO = 0
REG_UG2_UHLM_SEM_NIV_MUITO_ALTO = 0
REG_UG2_ENTRADA_DIGITAL_RESERVA_4 = 0
REG_UG2_UHLM_PRESSAO_LINHA_OLEO = 0
REG_UG2_UG_ENTRADA_DIGITAL_RESERVA_1 = 0
REG_UG2_UG_ENTRADA_DIGITAL_RESERVA_2 = 0
REG_UG2_UG_ENTRADA_DIGITAL_RESERVA_3 = 0
REG_UG2_UHLM_FILTRO_LIMPO = 0
REG_UG2_UHRV_SEM_NIV_MUITO_BAIXO = 0
REG_UG2_UHRV_FREIO_PRESSURIZADO = 0
REG_UG2_UHRV_FILTRO_LIMPO = 0
REG_UG2_ENTRADA_DIGITAL_RESERVA_3 = 0
REG_UG2_ENTRADA_DIGITAL_RESERVA_1 = 0
REG_UG2_ENTRADA_DIGITAL_RESERVA_2 = 0
REG_UG2_RESISTENCIA_SEM_FALHA = 0
REG_UG2_RESISTENCIA_LIGADA = 0
REG_UG2_CONTATOR_CAMPO_FECHADO = 0
REG_UG2_RELE_700G_TRIP_ATUADO = 0
REG_UG2_RELE_700G_BF_ATUADO = 0
REG_UG2_RELE_700G_WATCHDOG = 0
REG_UG2_RELE_700G_TRANSFERENCIA_DISPARO = 0
REG_UG2_BT_RV_AUMENTA_REFERENCIA = 0
REG_UG2_BT_RV_DIMINUI_REFERENCIA = 0
REG_UG2_BT_RT_AUMENTA_REFERENCIA = 0
REG_UG2_BT_RT_DIMINUI_REFERENCIA = 0
REG_UG2_SINCRONIZADOR_SINCRONIZADO = 0
REG_UG2_BT_PARA_UG = 0
REG_UG2_BT_PARTE_UG = 0
REG_UG2_BT_REARME_FALHAS = 0
REG_UG2_BT_EMERGENCIA_NAO_ATUADO = 0
REG_UG2_SUPERVISAO_BOBINA_52G = 0
REG_UG2_SUPERVISAO_BOBINA_86EH = 0
REG_UG2_RV_RELE_TRIP_NAO_ATUADO = 0
REG_UG2_RV_RELE_ALARME_ATUADO = 0
REG_UG2_RV_RELE_ESTADO_HABILITADO = 0
REG_UG2_RV_RELE_ESTADO_REGULANDO = 0
REG_UG2_RV_RELE_POTENCIA_NULA = 0
REG_UG2_RV_RELE_MAQUINA_PARADA = 0
REG_UG2_RV_RELE_VEL_MENOR_30 = 0
REG_UG2_RV_RELE_VEL_MAIOR_90 = 0
REG_UG2_RV_RELE_DISTRIBUIDOR_ABERTO = 0
REG_UG2_RT_RELE_TRIP_NAO_ATUADO = 0
REG_UG2_RT_RELE_ALARME_ATUADO = 0
REG_UG2_RT_RELE_ESTADO_HABILITADO = 0
REG_UG2_RT_RELE_ESTADO_REGULANDO = 0
REG_UG2_UG_ENTRADA_DIGITAL_RESERVA = 0
REG_UG2_RELE_BLOQUEIO_86EH_DESATUADO = 0
REG_UG2_SUPERVISAO_TENSAO_125VCC = 0
REG_UG2_SUPERVISAO_TENSAO_24VCC = 0
REG_UG2_DISJUNTORES_125VCC_FECHADOS = 0
REG_UG2_DISJUNTORES_24VCC_FECHADOS = 0
REG_UG2_CLP_GERAL_SEM_BLOQUEIO_EXTERNO = 0
REG_UG2_CLP_GERAL_SISTEMA_AGUA_OK = 0
REG_UG2_CLP_GERAL_COM_TENSAO_BARRA_ESSENCIAIS = 0
REG_UG2_COMPORTA_PERMISSIVO_ABERTURA_OK = 0
REG_UG2_ESCOVAS_GASTAS_POLO_POSITIVO = 0
REG_UG2_ESCOVAS_GASTAS_POLO_NEGATIVO = 0
REG_UG2_ENTRADA_DIGITAL_RESERVA_5 = 0
REG_UG2_DISPARO_MECANICO_DESATUADO = 0
REG_UG2_DISPARO_MECANICO_ATUADO = 0
REG_UG2_ENTRADA_DIGITAL_RESERVA_6 = 0
REG_UG2_ENTRADA_DIGITAL_RESERVA_7 = 0
REG_UG2_ENTRADA_DIGITAL_RESERVA_8 = 0
REG_UG2_ENTRADA_DIGITAL_RESERVA_9 = 0
REG_UG2_ENTRADA_DIGITAL_RESERVA_10 = 0
REG_UG2_ENTRADA_DIGITAL_RESERVA_11 = 0
REG_UG2_ACN_52G_PERMITE_FECHAMENTO = 0
REG_UG2_ACN_52G_ABRE = 0
REG_UG2_ACN_REARME_BLOQUEIO_86EH = 0
REG_UG2_ACN_SINCRO_SELECIONA_BARRA_MORTA = 0
REG_UG2_ACN_RESISTENCIA_DESLIGA = 0
REG_UG2_ACN_PERMISSIVO_COMPORTA = 0
REG_UG2_ACN_UHRV_BOMBA_1_LIGA = 0
REG_UG2_ACN_UHRV_BOMBA_2_LIGA = 0
REG_UG2_ACN_UHLM_BOMBA_1_LIGA = 0
REG_UG2_ACN_UHLM_BOMBA_2_LIGA = 0
REG_UG2_ACN_RV_ACIONA_SEM_BLOQUEIO_EXTERNO = 0
REG_UG2_ACN_RV_HABILITA = 0
REG_UG2_ACN_RV_SELECIONA_CONTROLE_ISOLADO = 0
REG_UG2_ACN_RV_ACIONA_ZERA_CARGA = 0
REG_UG2_ACN_RV_RESET_FALHAS = 0
REG_UG2_ACN_RV_AUMENTA_REFERENCIA = 0
REG_UG2_ACN_RV_DIMINUI_REFERENCIA = 0
REG_UG2_ACN_RV_PROGRAMAVEL_1 = 0
REG_UG2_ACN_RT_ACIONA_SEM_BLOQUEIO_EXTERNO = 0
REG_UG2_ACN_RT_HABILITA = 0
REG_UG2_ACN_RT_SELECIONA_CONTROLE_ISOLADO = 0
REG_UG2_ACN_RT_RESET_FALHAS = 0
REG_UG2_ACN_RT_AUMENTA_REFERENCIA = 0
REG_UG2_ACN_RT_DIMINUI_REFERENCIA = 0
REG_UG2_ACN_RT_PROGRAMAVEL_1 = 0
REG_UG2_ACN_SINCRO_HABILITA = 0
REG_UG2_ACN_SAIDA_RESERVA_1 = 0
REG_UG2_ACN_SAIDA_RESERVA_2 = 0
REG_UG2_ACN_APLICA_FREIO = 0
REG_UG2_ACN_ACIONA_VALV_SEG_DISTRIBUIDOR = 0
REG_UG2_ACN_ACIONA_VALV_SEG_ROTOR = 0
REG_UG2_ACN_UHRV_VALVULA_RETORNA_TANQUE = 0
REG_UG2_ACN_SINALIZA_UG_OPERACAO = 0
REG_UG2_ACN_SINALIZA_UG_FALHA = 0
REG_UG2_ACN_SINALIZA_UG_PERMISSIVO = 0
REG_UG2_ACN_SEM_BLOQUEIO_86EH = 0
REG_UG2_ACN_ATUA_BLOQUEIO_86EH_RESERVA_1 = 0
REG_UG2_ACN_ATUA_BLOQUEIO_86EH_RESERVA_2 = 0
REG_UG2_ACN_CLP_GERAL_HABILITA_SISTEMA_AGUA = 0
REG_UG2_ACN_CLP_GERAL_RESERVA_2 = 0
REG_UG2_ACN_CLP_GERAL_RESERVA_3 = 0
REG_UG2_ACN_SAIDA_RESERVA_RESERVA_3 = 0
REG_UG2_ACN_SAIDA_RESERVA_RESERVA_4 = 0
REG_UG2_ACN_SAIDA_RESERVA_RESERVA_5 = 0
REG_UG2_ACN_SAIDA_RESERVA_RESERVA_6 = 0
REG_UG2_ACN_SAIDA_RESERVA_RESERVA_7 = 0
REG_UG2_ACN_SAIDA_RESERVA_RESERVA_8 = 0
REG_UG2_ACN_SAIDA_RESERVA_RESERVA_9 = 0
REG_UG2_TEMP_PONTE_TIRISTORES_FASE_A = 0
REG_UG2_TEMP_PONTE_TIRISTORES_FASE_B = 0
REG_UG2_TEMP_PONTE_TIRISTORES_FASE_C = 0
REG_UG2_TEMP_RESERVA_3 = 0
REG_UG2_TEMP_TRAFO_EXCITACAO = 0
REG_UG2_TEMP_MANCAL_GUIA_GERADOR = 0
REG_UG2_TEMP_UHRV_OLEO = 0
REG_UG2_TEMP_UHLM_OLEO = 0
REG_UG2_TEMP_CASQ_MANCAL_COMBINADO = 0
REG_UG2_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO = 0
REG_UG2_TEMP_1_PATIN_MANCAL_COMBINADO = 0
REG_UG2_TEMP_2_PATIN_MANCAL_COMBINADO = 0
REG_UG2_TEMP_1_MANCAL_GUIA_INTERNO = 0
REG_UG2_TEMP_2_MANCAL_GUIA_INTERNO = 0
REG_UG2_TEMP_GERADOR_NUCLEO = 0
REG_UG2_TEMP_GERADOR_FASE_A = 0
REG_UG2_TEMP_GERADOR_FASE_B = 0
REG_UG2_TEMP_GERADOR_FASE_C = 0
REG_UG2_TEMP_RESERVA_2 = 0
REG_UG2_TEMP_RESERVA = 0
REG_UG2_PRESSAO_ENTRADA_TURBINA = 0
REG_UG2_PRESSAO_REGULAGEM_1_TURBINA = 0
REG_UG2_PRESSAO_VACUOSTATO_SAIDA_RODA = 0
REG_UG2_PRESSAO_VACUOSTATO_SAIDA_SUCCAO = 0
REG_UG2_VIBRACAO_EIXO_X_MANCAL_COMBINADO = 0
REG_UG2_VIBRACAO_EIXO_Y_MANCAL_COMBINADO = 0
REG_UG2_VIBRACAO_EIXO_Z_MANCAL_COMBINADO = 0
REG_UG2_PRESSAO_UHRV_ACUMULADOR = 0
REG_UG2_VIBRACAO_DETECCAO_HORIZONTAL = 0
REG_UG2_VIBRACAO_DETECCAO_VERTICAL = 0
REG_UG2_PRESSAO_REGULAGEM_2_TURBINA = 0
REG_UG2_PRESSAO_DIFERENCIAL_REGULAGEM_TURBINA = 0
REG_UG2_UG_VAB = 0
REG_UG2_UG_VBC = 0
REG_UG2_UG_VCA = 0
REG_UG2_UG_IA = 0
REG_UG2_UG_IB = 0
REG_UG2_UG_IC = 0
REG_UG2_UG_P = 0
REG_UG2_UG_Q = 0
REG_UG2_UG_S = 0
REG_UG2_UG_F = 0
REG_UG2_UG_FP = 0
REG_UG2_UG_EAP = 0
REG_UG2_UG_EAN = 0
REG_UG2_UG_ERP = 0
REG_UG2_UG_ERN = 0
REG_UG2_PARADA_FINALIZADA = 0
REG_UG2_MAQUINA_PARTINDO = 0
REG_UG2_GIRANDO_DESEXCITADA = 0
REG_UG2_PRONTA_PARA_SINCRONIZAR = 0
REG_UG2_OPERANDO_SINCRONIZADA = 0
REG_UG2_MAQUINA_PARANDO_PASSO = 0
REG_UG2_PARANDO_SEM_REJEICAO = 0
REG_UG2_PARANDO_EMERGENCIA = 0
REG_UG2_CONTROLE_NIVEL_HABILITADO = 0
REG_UG2_CONTROLE_ESCALONADO_HABILITADO = 0
REG_UG2_PARADA_POR_NIVEL_HABILITADA = 0
REG_UG2_FALHA_HABILITAR_SISTEMA_AGUA = 0
REG_UG2_PARANDO_PARCIAL = 0
REG_UG2_STT_UG_RESERVA_13 = 0
REG_UG2_STT_UG_RESERVA_14 = 0
REG_UG2_STT_UG_RESERVA_15 = 0
REG_UG2_STT_UG_RESERVA_16 = 0
REG_UG2_STT_UG_RESERVA_17 = 0
REG_UG2_STT_UG_RESERVA_18 = 0
REG_UG2_STT_UG_RESERVA_19 = 0
REG_UG2_STT_UG_RESERVA_20 = 0
REG_UG2_STT_UG_RESERVA_21 = 0
REG_UG2_STT_UG_RESERVA_22 = 0
REG_UG2_STT_UG_RESERVA_23 = 0
REG_UG2_STT_UG_RESERVA_24 = 0
REG_UG2_STT_UG_RESERVA_25 = 0
REG_UG2_STT_UG_RESERVA_26 = 0
REG_UG2_STT_UG_RESERVA_27 = 0
REG_UG2_STT_UG_RESERVA_28 = 0
REG_UG2_STT_UG_RESERVA_29 = 0
REG_UG2_STT_UG_RESERVA_30 = 0
REG_UG2_STT_UG_RESERVA_31 = 0
REG_UG2_ALM_TEMP_PONTE_FASE_A = 0
REG_UG2_ALM_TEMP_PONTE_FASE_B = 0
REG_UG2_ALM_TEMP_PONTE_FASE_C = 0
REG_UG2_ALM_TEMP_RESERVA_3 = 0
REG_UG2_ALM_TEMP_TRAFO_EXCITACAO = 0
REG_UG2_ALM_TEMP_MANCAL_GUIA = 0
REG_UG2_ALM_TEMP_OLEO_UHRV = 0
REG_UG2_ALM_TEMP_OLEO_UHLM = 0
REG_UG2_ALM_TEMP_CASQ_MANCAL_COMBINADO = 0
REG_UG2_ALM_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO = 0
REG_UG2_ALM_TEMP_1_PATINS_MANCAL_COMBINADO = 0
REG_UG2_ALM_TEMP_2_PATINS_MANCAL_COMBINADO = 0
REG_UG2_ALM_TEMP_1_MANCAL_GUIA_INTERNO = 0
REG_UG2_ALM_TEMP_2_MANCAL_GUIA_INTERNO = 0
REG_UG2_ALM_TEMP_GERADOR_NUCLEO_ESTATORICO = 0
REG_UG2_ALM_TEMP_GERADOR_FASE_A = 0
REG_UG2_ALM_TEMP_GERADOR_FASE_B = 0
REG_UG2_ALM_TEMP_GERADOR_FASE_C = 0
REG_UG2_ALM_TEMP_RESERVA_2 = 0
REG_UG2_ALM_TEMP_RESERVA = 0
REG_UG2_ALM_PRESSAO_ENTRADA_TURBINA = 0
REG_UG2_ALM_PRESSAO_REGULAGEM_TURBINA = 0
REG_UG2_ALM_PRESSAO_SAIDA_RODA = 0
REG_UG2_ALM_PRESSAO_SAIDA_SUCCAO = 0
REG_UG2_ALM_VIBRACAO_EIXO_X_MANCAL_COMBINADO = 0
REG_UG2_ALM_VIBRACAO_EIXO_Y_MANCAL_COMBINADO = 0
REG_UG2_ALM_VIBRACAO_EIXO_Z_MANCAL_COMBINADO = 0
REG_UG2_ALM_PRESSAO_ACUMULADOR_UHRV = 0
REG_UG2_ALM_VIBRACAO_DETECCAO_HORIZONTAL = 0
REG_UG2_ALM_VIBRACAO_DETECACAO_VERTICAL = 0
REG_UG2_ALM_PRESSAO_REGULAGEM_2_TURBINA = 0
REG_UG2_ALM_PRESSAO_DIFERENCIAL_REGULAGEM_TURBINA = 0
REG_UG2_TRIP_TEMP_PONTE_FASE_A = 0
REG_UG2_TRIP_TEMP_PONTE_FASE_B = 0
REG_UG2_TRIP_TEMP_PONTE_FASE_C = 0
REG_UG2_TRIP_TEMP_TRAFO_ATERRAMENTO = 0
REG_UG2_TRIP_TEMP_TRAFO_EXCITACAO = 0
REG_UG2_TRIP_TEMP_MANCAL_GUIA = 0
REG_UG2_TRIP_TEMP_OLEO_UHRV = 0
REG_UG2_TRIP_TEMP_OLEO_UHLM = 0
REG_UG2_TRIP_TEMP_CASQ_MANCAL_COMBINADO = 0
REG_UG2_TRIP_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO = 0
REG_UG2_TRIP_TEMP_1_PATINS_MANCAL_COMBINADO = 0
REG_UG2_TRIP_TEMP_2_PATINS_MANCAL_COMBINADO = 0
REG_UG2_TRIP_TEMP_1_MANCAL_GUIA_INTERNO = 0
REG_UG2_TRIP_TEMP_2_MANCAL_GUIA_INTERNO = 0
REG_UG2_TRIP_TEMP_GERADOR_NUCLEO_ESTATORICO = 0
REG_UG2_TRIP_TEMP_GERADOR_FASE_A = 0
REG_UG2_TRIP_TEMP_GERADOR_FASE_B = 0
REG_UG2_TRIP_TEMP_GERADOR_FASE_C = 0
REG_UG2_TRIP_TEMP_GERADOR_SAIDA_AR = 0
REG_UG2_TRIP_TEMP_RESERVA = 0
REG_UG2_TRIP_PRESSAO_ENTRADA_TURBINA = 0
REG_UG2_TRIP_PRESSAO_REGULAGEM_TURBINA = 0
REG_UG2_TRIP_PRESSAO_SAIDA_RODA = 0
REG_UG2_TRIP_PRESSAO_SAIDA_SUCCAO = 0
REG_UG2_TRIP_VIBRACAO_EIXO_X_MANCAL_COMBINADO = 0
REG_UG2_TRIP_VIBRACAO_EIXO_Y_MANCAL_COMBINADO = 0
REG_UG2_TRIP_VIBRACAO_EIXO_Z_MANCAL_COMBINADO = 0
REG_UG2_TRIP_PRESSAO_ACUMULADOR_UHRV = 0
REG_UG2_TRIP_VIBRACAO_DETECCAO_HORIZONTAL = 0
REG_UG2_TRIP_VIBRACAO_DETECACAO_VERTICAL = 0
REG_UG2_TRIP_PRESSAO_REGULAGEM_2_TURBINA = 0
REG_UG2_TRIP_PRESSAO_DIFERENCIAL_REGULAGEM_TURBINA = 0
REG_UG2_UHRV_UNIDADE_EM_MANUTENCAO = 0
REG_UG2_UHRV_BOMBA_1_PRINCIPAL = 0
REG_UG2_UHRV_BOMBA_2_PRINCIPAL = 0
REG_UG2_UHRV_BOMBA_1_DISPONIVEL = 0
REG_UG2_UHRV_BOMBA_2_DISPONIVEL = 0
REG_UG2_UHRV_TIME_OUT_LIGA_BOMBA_1 = 0
REG_UG2_UHRV_TIME_OUT_DESL_BOMBA_1 = 0
REG_UG2_UHRV_TIME_OUT_LIGA_BOMBA_2 = 0
REG_UG2_UHRV_TIME_OUT_DESL_BOMBA_2 = 0
REG_UG2_UHRV_FALHA_PRESSURIZA_BOMBA_1 = 0
REG_UG2_UHRV_FALHA_PRESSURIZA_BOMBA_2 = 0
REG_UG2_UHRV_FREIO_APLICANDO_FREIO = 0
REG_UG2_UHRV_FALHA_PRESSURIZAR_FREIO = 0
REG_UG2_UHRV_FALHA_DESPRESSURIZAR_FREIO = 0
REG_UG2_UHRV_STT_RESERVA_1 = 0
REG_UG2_UHRV_STT_RESERVA_2 = 0
REG_UG2_UHRV_STT_RESERVA_3 = 0
REG_UG2_UHRV_STT_RESERVA_4 = 0
REG_UG2_UHRV_STT_RESERVA_5 = 0
REG_UG2_UHRV_STT_RESERVA_6 = 0
REG_UG2_UHRV_STT_RESERVA_7 = 0
REG_UG2_UHRV_STT_RESERVA_8 = 0
REG_UG2_UHRV_STT_RESERVA_9 = 0
REG_UG2_UHRV_STT_RESERVA_10 = 0
REG_UG2_UHRV_STT_RESERVA_11 = 0
REG_UG2_UHRV_STT_RESERVA_12 = 0
REG_UG2_UHRV_STT_RESERVA_13 = 0
REG_UG2_UHRV_STT_RESERVA_14 = 0
REG_UG2_UHRV_STT_RESERVA_15 = 0
REG_UG2_UHRV_STT_RESERVA_16 = 0
REG_UG2_UHRV_STT_RESERVA_17 = 0
REG_UG2_UHRV_STT_RESERVA_18 = 0
REG_UG2_UHLM_BOMBA_1_PRINCIPAL = 0
REG_UG2_UHLM_BOMBA_2_PRINCIPAL = 0
REG_UG2_UHLM_BOMBA_1_DISPONIVEL = 0
REG_UG2_UHLM_BOMBA_2_DISPONIVEL = 0
REG_UG2_UHLM_UNIDADE_EM_MANUTENCAO = 0
REG_UG2_UHLM_TIME_OUT_LIGA_BOMBA_1 = 0
REG_UG2_UHLM_TIME_OUT_DESL_BOMBA_1 = 0
REG_UG2_UHLM_TIME_OUT_LIGA_BOMBA_2 = 0
REG_UG2_UHLM_TIME_OUT_DESL_BOMBA_2 = 0
REG_UG2_UHLM_FALHA_PRESSAO_LINHA_B1 = 0
REG_UG2_UHLM_FALHA_PRESSAO_LINHA_B2 = 0
REG_UG2_UHLM_FALHA_PRESSOSTATO_LINHA = 0
REG_UG2_UHLM_STT_RESERVA_02 = 0
REG_UG2_UHLM_STT_RESERVA_01 = 0
REG_UG2_UHLM_STT_RESERVA_0 = 0
REG_UG2_UHLM_STT_RESERVA_1 = 0
REG_UG2_UHLM_STT_RESERVA_2 = 0
REG_UG2_UHLM_STT_RESERVA_3 = 0
REG_UG2_UHLM_STT_RESERVA_4 = 0
REG_UG2_UHLM_STT_RESERVA_5 = 0
REG_UG2_UHLM_STT_RESERVA_6 = 0
REG_UG2_UHLM_STT_RESERVA_7 = 0
REG_UG2_UHLM_STT_RESERVA_8 = 0
REG_UG2_UHLM_STT_RESERVA_9 = 0
REG_UG2_UHLM_STT_RESERVA_10 = 0
REG_UG2_UHLM_STT_RESERVA_11 = 0
REG_UG2_UHLM_STT_RESERVA_12 = 0
REG_UG2_UHLM_STT_RESERVA_13 = 0
REG_UG2_UHLM_STT_RESERVA_14 = 0
REG_UG2_UHLM_STT_RESERVA_15 = 0
REG_UG2_UHLM_STT_RESERVA_16 = 0
REG_UG2_UHLM_STT_RESERVA_17 = 0
REG_UG2_UHLM_STT_RESERVA_33 = 0
REG_UG2_RV_FALHA_HABILITAR_RV = 0
REG_UG2_RV_FALHA_PARTIR_RV = 0
REG_UG2_RV_FALHA_DESABILITAR_RV = 0
REG_UG2_RV_FALHA_PARAR_MAQUINA = 0
REG_UG2_RV_FALHA_FECHAR_DISTRIBUIDOR = 0
REG_UG2_STT_RV_RESERVA_1 = 0
REG_UG2_STT_RV_RESERVA_2 = 0
REG_UG2_STT_RV_RESERVA_3 = 0
REG_UG2_STT_RV_RESERVA_4 = 0
REG_UG2_STT_RV_RESERVA_5 = 0
REG_UG2_STT_RV_RESERVA_6 = 0
REG_UG2_STT_RV_RESERVA_7 = 0
REG_UG2_STT_RV_RESERVA_8 = 0
REG_UG2_STT_RV_RESERVA_9 = 0
REG_UG2_STT_RV_RESERVA_10 = 0
REG_UG2_STT_RV_RESERVA_11 = 0
REG_UG2_RT_FALHA_HABILITAR = 0
REG_UG2_RT_FALHA_PARTIR = 0
REG_UG2_RT_FALHA_DESABILITAR = 0
REG_UG2_STT_RT_RESERVA_1 = 0
REG_UG2_STT_RT_RESERVA_2 = 0
REG_UG2_STT_RT_RESERVA_3 = 0
REG_UG2_STT_RT_RESERVA_4 = 0
REG_UG2_STT_RT_RESERVA_5 = 0
REG_UG2_STT_RT_RESERVA_6 = 0
REG_UG2_STT_RT_RESERVA_7 = 0
REG_UG2_STT_RT_RESERVA_8 = 0
REG_UG2_STT_RT_RESERVA_9 = 0
REG_UG2_STT_RT_RESERVA_10 = 0
REG_UG2_STT_RT_RESERVA_11 = 0
REG_UG2_STT_RT_RESERVA_12 = 0
REG_UG2_STT_RT_RESERVA_13 = 0
REG_UG2_PART_ATUAL_DESAPLICANDO_FREIO = 0
REG_UG2_PART_ATUAL_HABILITANDO_UHLM = 0
REG_UG2_PART_ATUAL_HABILITANDO_SISTEMA_AGUA = 0
REG_UG2_PART_ATUAL_PARTINDO_RV = 0
REG_UG2_PART_ATUAL_PARTINDO_RT = 0
REG_UG2_PART_ATUAL_SINCRONIZANDO = 0
REG_UG2_PART_ATUAL_RESERVA_01 = 0
REG_UG2_PART_ATUAL_RESERVA_02 = 0
REG_UG2_PART_ATUAL_RESERVA_03 = 0
REG_UG2_PART_ATUAL_RESERVA_04 = 0
REG_UG2_PART_ATUAL_RESERVA_05 = 0
REG_UG2_PART_ATUAL_RESERVA_06 = 0
REG_UG2_PART_ATUAL_RESERVA_07 = 0
REG_UG2_PART_ATUAL_RESERVA_08 = 0
REG_UG2_PART_ATUAL_RESERVA_09 = 0
REG_UG2_PART_ATUAL_RESERVA_10 = 0
REG_UG2_PARA_ATUAL_DESCARGA_POT = 0
REG_UG2_PARA_ATUAL_PARANDO_RT = 0
REG_UG2_PARA_ATUAL_PARANDO_RV_APLICANDO_FREIO = 0
REG_UG2_PARA_ATUAL_DESABILITANDO_SISTEMA_AGUA = 0
REG_UG2_PARA_ATUAL_DESABILITANDO_UHLM = 0
REG_UG2_PARA_ATUAL_RESERVA_01 = 0
REG_UG2_PARA_ATUAL_RESERVA_02 = 0
REG_UG2_PARA_ATUAL_RESERVA_03 = 0
REG_UG2_PARA_ATUAL_RESERVA_04 = 0
REG_UG2_PARA_ATUAL_RESERVA_05 = 0
REG_UG2_PARA_ATUAL_RESERVA_06 = 0
REG_UG2_PARA_ATUAL_RESERVA_07 = 0
REG_UG2_PARA_ATUAL_RESERVA_08 = 0
REG_UG2_PARA_ATUAL_RESERVA_09 = 0
REG_UG2_PARA_ATUAL_RESERVA_10 = 0
REG_UG2_PARA_ATUAL_RESERVA_11 = 0
REG_UG2_PART_CONCLUIDA_DESPLICA_FREIO = 0
REG_UG2_PART_CONCLUIDA_HABILITA_UHLM = 0
REG_UG2_PART_CONCLUIDA_HABILITA_SISTEMA_AGUA = 0
REG_UG2_PART_CONCLUIDA_PARTE_RV = 0
REG_UG2_PART_CONCLUIDA_PARTE_RT = 0
REG_UG2_PART_CONCLUIDA_SINCRONIZADO = 0
REG_UG2_PART_CONCLUIDA_RESERVA_01 = 0
REG_UG2_PART_CONCLUIDA_RESERVA_02 = 0
REG_UG2_PART_CONCLUIDA_RESERVA_03 = 0
REG_UG2_PART_CONCLUIDA_RESERVA_04 = 0
REG_UG2_PART_CONCLUIDA_RESERVA_05 = 0
REG_UG2_PART_CONCLUIDA_RESERVA_06 = 0
REG_UG2_PART_CONCLUIDA_RESERVA_07 = 0
REG_UG2_PART_CONCLUIDA_RESERVA_08 = 0
REG_UG2_PART_CONCLUIDA_RESERVA_09 = 0
REG_UG2_PART_CONCLUIDA_RESERVA_10 = 0
REG_UG2_PARA_CONCLUIDA_DESCARGA_POT = 0
REG_UG2_PARA_CONCLUIDA_PARA_RT = 0
REG_UG2_PARA_CONCLUIDA_PARA_RV_APLICA_FREIO = 0
REG_UG2_PARA_CONCLUIDA_DESABILITA_SISTEMA_AGUA = 0
REG_UG2_PARA_CONCLUIDA_DESABILITA_UHLM = 0
REG_UG2_PARA_CONCLUIDA_RESERVA_01 = 0
REG_UG2_PARA_CONCLUIDA_RESERVA_02 = 0
REG_UG2_PARA_CONCLUIDA_RESERVA_03 = 0
REG_UG2_PARA_CONCLUIDA_RESERVA_04 = 0
REG_UG2_PARA_CONCLUIDA_RESERVA_05 = 0
REG_UG2_PARA_CONCLUIDA_RESERVA_06 = 0
REG_UG2_PARA_CONCLUIDA_RESERVA_07 = 0
REG_UG2_PARA_CONCLUIDA_RESERVA_08 = 0
REG_UG2_PARA_CONCLUIDA_RESERVA_09 = 0
REG_UG2_PARA_CONCLUIDA_RESERVA_10 = 0
REG_UG2_PARA_CONCLUIDA_RESERVA_11 = 0
REG_UG2_FALHA_PARTIDA_DESAPLICA_FREIO = 0
REG_UG2_FALHA_PARTIDA_HABILITA_UHLM = 0
REG_UG2_FALHA_PARTIDA_HABILITA_SISTEMA_AGUA = 0
REG_UG2_FALHA_PARTIDA_PARTE_RV = 0
REG_UG2_FALHA_PARTIDA_PARTE_RT = 0
REG_UG2_FALHA_PARTIDA_SINCRONISMO = 0
REG_UG2_FALHA_PARTIDA_RESERVA_1 = 0
REG_UG2_FALHA_PARTIDA_RESERVA_2 = 0
REG_UG2_FALHA_PARTIDA_RESERVA_3 = 0
REG_UG2_FALHA_PARTIDA_RESERVA_4 = 0
REG_UG2_FALHA_PARTIDA_RESERVA_5 = 0
REG_UG2_FALHA_PARTIDA_RESERVA_6 = 0
REG_UG2_FALHA_PARTIDA_RESERVA_7 = 0
REG_UG2_FALHA_PARTIDA_RESERVA_8 = 0
REG_UG2_FALHA_PARTIDA_RESERVA_9 = 0
REG_UG2_FALHA_PARTIDA_RESERVA_10 = 0
REG_UG2_FALHA_TEMP_PONTE_FASE_A = 0
REG_UG2_FALHA_TEMP_PONTE_FASE_B = 0
REG_UG2_FALHA_TEMP_PONTE_FASE_C = 0
REG_UG2_FALHA_TEMP_RESERVA_3 = 0
REG_UG2_FALHA_TEMP_TRAFO_EXCITACAO = 0
REG_UG2_FALHA_TEMP_MANCAL_GUIA = 0
REG_UG2_FALHA_TEMP_OLEO_UHRV = 0
REG_UG2_FALHA_TEMP_OLEO_UHLM = 0
REG_UG2_FALHA_TEMP_CASQ_MANCAL_COMBINADO = 0
REG_UG2_FALHA_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO = 0
REG_UG2_FALHA_TEMP_1_PATINS_MANCAL_COMBINADO = 0
REG_UG2_FALHA_TEMP_2_PATINS_MANCAL_COMBINADO = 0
REG_UG2_FALHA_TEMP_1_MANCAL_GUIA_INTERNO = 0
REG_UG2_FALHA_TEMP_2_MANCAL_GUIA_INTERNO = 0
REG_UG2_FALHA_TEMP_GERADOR_NUCLEO_ESTATORICO = 0
REG_UG2_FALHA_TEMP_GERADOR_FASE_A = 0
REG_UG2_FALHA_TEMP_GERADOR_FASE_B = 0
REG_UG2_FALHA_TEMP_GERADOR_FASE_C = 0
REG_UG2_FALHA_TEMP_RESERVA_2 = 0
REG_UG2_FALHA_TEMP_RESERVA = 0
REG_UG2_FALHA_PRESSAO_ENTRADA_TURBINA = 0
REG_UG2_FALHA_PRESSAO_REGULAGEM_TURBINA = 0
REG_UG2_FALHA_PRESSAO_SAIDA_RODA = 0
REG_UG2_FALHA_PRESSAO_SAIDA_SUCCAO = 0
REG_UG2_FALHA_VIBRACAO_EIXO_X_MANCAL_COMBINADO = 0
REG_UG2_FALHA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO = 0
REG_UG2_FALHA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO = 0
REG_UG2_FALHA_PRESSAO_ACUMULADOR_UHRV = 0
REG_UG2_FALHA_VIBRACAO_DETECCAO_HORIZONTAL = 0
REG_UG2_FALHA_VIBRACAO_DETECACAO_VERTICAL = 0
REG_UG2_FALHA_PRESSAO_REGULAGEM_2_TURBINA = 0
REG_UG2_FALHA_PRESSAO_DIFERENCIAL_REGULAGEM_TURBINA = 0
REG_UG2_CP_STT_HEARTBEAT = 0
REG_UG2_CP_STT_COMPORTA_OPERANDO = 0
REG_UG2_CP_STT_FECHAMENTO_FINALIZADO = 0
REG_UG2_CP_STT_FALHA_GRAVE = 0
REG_UG2_CP_STT_FALHA_NIVEL_MONTATE = 0
REG_UG2_CP_STT_FALHA_NIVEL_JUSANTE_GRADE = 0
REG_UG2_CP_STT_06 = 0
REG_UG2_CP_STT_07 = 0
REG_UG2_CP_STT_08 = 0
REG_UG2_CP_STT_09 = 0
REG_UG2_CP_STT_10 = 0
REG_UG2_CP_STT_11 = 0
REG_UG2_CP_STT_12 = 0
REG_UG2_CP_STT_13 = 0
REG_UG2_CP_STT_14 = 0
REG_UG2_CP_STT_15 = 0
REG_UG2_CP_STT_16 = 0
REG_UG2_CP_STT_17 = 0
REG_UG2_CP_STT_18 = 0
REG_UG2_CP_STT_19 = 0
REG_UG2_CP_STT_20 = 0
REG_UG2_CP_STT_21 = 0
REG_UG2_CP_STT_22 = 0
REG_UG2_CP_STT_23 = 0
REG_UG2_CP_STT_24 = 0
REG_UG2_CP_STT_25 = 0
REG_UG2_CP_STT_26 = 0
REG_UG2_CP_STT_27 = 0
REG_UG2_CP_STT_28 = 0
REG_UG2_CP_STT_29 = 0
REG_UG2_CP_STT_30 = 0
REG_UG2_CP_STT_31 = 0
REG_UG2_PRE_CONDICOES_PARTIDA_OK = 0
REG_UG2_PERMISSIVOS_UHLM_OK = 0
REG_UG2_PERMISSIVOS_SISTEMA_AGUA_OK = 0
REG_UG2_PERMISSIVOS_RV_OK = 0
REG_UG2_PERMISSIVOS_RT_OK = 0
REG_UG2_PERMISSIVOS_SINCRONISMO_OK = 0
REG_UG2_BLOQUEIO_86M_ATUADO = 0
REG_UG2_BLOQUEIO_86E_ATUADO = 0
REG_UG2_BLOQUEIO_86H_ATUADO = 0
REG_UG2_HABILITA_FREIO = 0
REG_UG2_HABILITA_UHLM = 0
REG_UG2_HABILITA_RV = 0
REG_UG2_HABILITA_RT = 0
REG_UG2_PARTIDA_BLOQUEIO_FREIO_PASSO_A_FRENTE = 0
REG_UG2_PARTIDA_BLOQUEIO_UHL_PASSO_A_FRENTE = 0
REG_UG2_PARTIDA_BLOQUEIO_SISTEMA_AGUA_PASSO_A_FRENTE = 0
REG_UG2_PARADA_BLOQUEIO_DESCARGA_POTENCIA = 0
REG_UG2_PARADA_BLOQUEIO_ABERTURA_DISJUNTOR = 0
REG_UG2_UHLM_OK = 0
REG_UG2_SISTEMA_AGUA_OK = 0
REG_UG2_RV_OK = 0
REG_UG2_RT_OK = 0
REG_UG2_HABILITA_SISTEMA_AGUA = 0
REG_UG2_CP_FALHA_CONTROLE_VIDA = 0
REG_UG2_FALSE = 0
REG_UG2_TRUE = 0
REG_UG2_PARADA_NIVEL = 0
REG_UG2_PARADA_FALHA_MEDICAO_NIVEL = 0
REG_UG2_BLOQUEIO_CMD_EMERGENCIA = 0
REG_UG2_BLOQUEIO_GIRO_INDEVIDO = 0
REG_UG2_BLOQUEIO_BLOQUEIO_EXTERNO = 0

REG_TDA_LG_RASTELO_RECOLHIDO = 0
REG_TDA_LG_POSICAO_INICIAL_ESQUERDA = 0
REG_TDA_LG_INCREMENTA_POSICAO_LIMPEZA = 0
REG_TDA_LG_SELETORA_AUTOMATICO = 0
REG_TDA_LG_BT_AFASTA_RASTELO = 0
REG_TDA_LG_BT_DESCE_RASTELO = 0
REG_TDA_LG_BT_SOBE_RASTELO = 0
REG_TDA_LG_BT_MOVIMENTO_ESQUERDA = 0
REG_TDA_LG_BT_MOVIMENTO_DIREITA = 0
REG_TDA_LG_BT_INICIAL_CICLO_LIMPEZA = 0
REG_TDA_UH_BOMBA_LIGADA = 0
REG_TDA_COM_TENSAO_CA = 0
REG_TDA_UH_SEM_NIVEL_MUITO_BAIXO = 0
REG_TDA_UH_FILTRO_LIMPO = 0
REG_TDA_CP_COMPORTA_1_ABERTA = 0
REG_TDA_CP_COMPORTA_1_FECHADA = 0
REG_TDA_CP_COMPORTA_1_CRACKING = 0
REG_TDA_CP_COMPORTA_2_ABERTA = 0
REG_TDA_CP_COMPORTA_2_FECHADA = 0
REG_TDA_CP_COMPORTA_2_CRACKING = 0
REG_TDA_VB_VALVULA_BORBOLETA_ABERTA = 0
REG_TDA_VB_VALVULA_BORBOLETA_FECHADA = 0
REG_TDA_CP_COMPORTA_1_REMOTO = 0
REG_TDA_LG_RESET_FALHAS = 0
REG_TDA_SEM_EMERGENCIA = 0
REG_TDA_CP_COMPORTA_2_REMOTO = 0
REG_TDA_CP_COMPORTA_1_PERMISSIVO_ABERTURA = 0
REG_TDA_CP_COMPORTA_2_PERMISSIVO_ABERTURA = 0
REG_TDA_ENTRADA_DIGITAL_RESERVA_1 = 0
REG_TDA_ENTRADA_DIGITAL_RESERVA_2 = 0
REG_TDA_ACN_LG_MOVIMENTA_ESQUERDA = 0
REG_TDA_ACN_LG_MOVIMENTA_DIREITA = 0
REG_TDA_ACN_UH_LIGA_BOMBA = 0
REG_TDA_ACN_LG_LIGA_ESTEIRA_1 = 0
REG_TDA_ACN_LG_LIGA_ESTEIRA_2 = 0
REG_TDA_ACN_LG_AFASTA_RASTELO = 0
REG_TDA_ACN_LG_DESCE_RASTELO = 0
REG_TDA_ACN_LG_BLOQUEIA_RASTELO = 0
REG_TDA_ACN_LG_SINALEIRO_LIMPA_GRADES_OPERANDO = 0
REG_TDA_ACN_LG_SINALEIRO_LIMPA_GRADES_FALHA = 0
REG_TDA_ACN_SAIDA_DIGITAL_RESERVA = 0
REG_TDA_ACN_CP_COMPORTA_1_VALVULA_CONTROLE = 0
REG_TDA_ACN_CP_COMPORTA_1_VALVULA_ABERTURA = 0
REG_TDA_ACN_CP_COMPORTA_2_VALVULA_CONTROLE = 0
REG_TDA_ACN_CP_COMPORTA_2_VALVULA_ABERTURA = 0
REG_TDA_ACN_VB_VALVULA_CONTROLE_BORBOLETA = 0
REG_TDA_ACN_VB_VALVULA_FECHAMENTO_BORBOLETA = 0
REG_TDA_ACN_CONTATOR_GERAL = 0
REG_TDA_NIVEL_MONTANTE = 0
REG_TDA_NIVEL_JUSANTE_GRADE_COMPORTA_1 = 0
REG_TDA_NIVEL_JUSANTE_GRADE_COMPORTA_2 = 0
REG_TDA_NIVEL_JUSANTE_COMPORTA_1 = 0
REG_TDA_NIVEL_JUSANTE_COMPORTA_2 = 0
REG_TDA_ENTRADA_ANALOGICA_RESERVA_1 = 0
REG_TDA_ENTRADA_ANALOGICA_RESERVA_2 = 0
REG_TDA_ENTRADA_ANALOGICA_RESERVA_3 = 0
REG_TDA_CP1_CMD_REARME_FALHAS = 0
REG_TDA_CP1_CMD_ABERTURA_CRACKING = 0
REG_TDA_CP1_CMD_ABERTURA_TOTAL = 0
REG_TDA_CP1_CMD_FECHAMENTO = 0
REG_TDA_CP1_CMD_RESERVA_04 = 0
REG_TDA_CP1_CMD_RESERVA_05 = 0
REG_TDA_CP1_CMD_RESERVA_06 = 0
REG_TDA_CP1_CMD_RESERVA_07 = 0
REG_TDA_CP1_CMD_RESERVA_08 = 0
REG_TDA_CP1_CMD_RESERVA_09 = 0
REG_TDA_CP1_CMD_RESERVA_10 = 0
REG_TDA_CP1_CMD_RESERVA_11 = 0
REG_TDA_CP1_CMD_RESERVA_12 = 0
REG_TDA_CP1_CMD_RESERVA_13 = 0
REG_TDA_CP1_CMD_RESERVA_14 = 0
REG_TDA_CP1_CMD_RESERVA_15 = 0
REG_TDA_CP1_CMD_RESERVA_16 = 0
REG_TDA_CP1_CMD_RESERVA_17 = 0
REG_TDA_CP1_CMD_RESERVA_18 = 0
REG_TDA_CP1_CMD_RESERVA_19 = 0
REG_TDA_CP1_CMD_RESERVA_20 = 0
REG_TDA_CP1_CMD_RESERVA_21 = 0
REG_TDA_CP1_CMD_RESERVA_22 = 0
REG_TDA_CP1_CMD_RESERVA_23 = 0
REG_TDA_CP1_CMD_RESERVA_24 = 0
REG_TDA_CP1_CMD_RESERVA_25 = 0
REG_TDA_CP1_CMD_RESERVA_26 = 0
REG_TDA_CP1_CMD_RESERVA_27 = 0
REG_TDA_CP1_CMD_RESERVA_28 = 0
REG_TDA_CP1_CMD_RESERVA_29 = 0
REG_TDA_CP1_CMD_RESERVA_30 = 0
REG_TDA_CP1_CMD_RESERVA_31 = 0
REG_TDA_CP2_CMD_REARME_FALHAS = 0
REG_TDA_CP2_CMD_ABERTURA_CRACKING = 0
REG_TDA_CP2_CMD_ABERTURA_TOTAL = 0
REG_TDA_CP2_CMD_FECHAMENTO = 0
REG_TDA_CP2_CMD_RESERVA_04 = 0
REG_TDA_CP2_CMD_RESERVA_05 = 0
REG_TDA_CP2_CMD_RESERVA_06 = 0
REG_TDA_CP2_CMD_RESERVA_07 = 0
REG_TDA_CP2_CMD_RESERVA_08 = 0
REG_TDA_CP2_CMD_RESERVA_09 = 0
REG_TDA_CP2_CMD_RESERVA_10 = 0
REG_TDA_CP2_CMD_RESERVA_11 = 0
REG_TDA_CP2_CMD_RESERVA_12 = 0
REG_TDA_CP2_CMD_RESERVA_13 = 0
REG_TDA_CP2_CMD_RESERVA_14 = 0
REG_TDA_CP2_CMD_RESERVA_15 = 0
REG_TDA_CP2_CMD_RESERVA_16 = 0
REG_TDA_CP2_CMD_RESERVA_17 = 0
REG_TDA_CP2_CMD_RESERVA_18 = 0
REG_TDA_CP2_CMD_RESERVA_19 = 0
REG_TDA_CP2_CMD_RESERVA_20 = 0
REG_TDA_CP2_CMD_RESERVA_21 = 0
REG_TDA_CP2_CMD_RESERVA_22 = 0
REG_TDA_CP2_CMD_RESERVA_23 = 0
REG_TDA_CP2_CMD_RESERVA_24 = 0
REG_TDA_CP2_CMD_RESERVA_25 = 0
REG_TDA_CP2_CMD_RESERVA_26 = 0
REG_TDA_CP2_CMD_RESERVA_27 = 0
REG_TDA_CP2_CMD_RESERVA_28 = 0
REG_TDA_CP2_CMD_RESERVA_29 = 0
REG_TDA_CP2_CMD_RESERVA_30 = 0
REG_TDA_CP2_CMD_RESERVA_31 = 0
REG_TDA_CP1_HABILITA_UNIDADE_HIDRAULICA = 0
REG_TDA_CP2_HABILITA_UNIDADE_HIDRAULICA = 0
REG_TDA_LG_HABILITA_UNIDADE_HIDRAULICA = 0
REG_TDA_CP1_COMPORTA_OPERANDO = 0
REG_TDA_CP1_REPONDO_COMPORTA = 0
REG_TDA_CP1_ABRINDO_COMPORTA = 0
REG_TDA_CP1_AGUARDANDO_COMANDO_ABERTURA = 0
REG_TDA_CP1_PRESSAO_EQUALIZADA = 0
REG_TDA_CP1_EQUALIZANDO_PRESSAO = 0
REG_TDA_CP1_ABRINDO_CRACKING = 0
REG_TDA_CP1_FECHANDO_COMPORTA = 0
REG_TDA_CP1_FECHAMENTO_FINALIZADO = 0
REG_TDA_CP1_FALHA_COMUNICACAO_CLP_UG = 0
REG_TDA_CP1_ALARME_DIFERENCIAL_GRADE = 0
REG_TDA_CP1_STT_RESERVA_11 = 0
REG_TDA_CP1_STT_RESERVA_12 = 0
REG_TDA_CP1_STT_RESERVA_13 = 0
REG_TDA_CP1_STT_RESERVA_14 = 0
REG_TDA_CP1_STT_RESERVA_15 = 0
REG_TDA_CP1_STT_RESERVA_16 = 0
REG_TDA_CP1_STT_RESERVA_17 = 0
REG_TDA_CP1_STT_RESERVA_18 = 0
REG_TDA_CP1_STT_RESERVA_19 = 0
REG_TDA_CP1_STT_RESERVA_20 = 0
REG_TDA_CP1_STT_RESERVA_21 = 0
REG_TDA_CP1_STT_RESERVA_22 = 0
REG_TDA_CP1_STT_RESERVA_23 = 0
REG_TDA_CP1_STT_RESERVA_24 = 0
REG_TDA_CP1_STT_RESERVA_25 = 0
REG_TDA_CP1_STT_RESERVA_26 = 0
REG_TDA_CP1_STT_RESERVA_27 = 0
REG_TDA_CP1_STT_RESERVA_28 = 0
REG_TDA_CP1_STT_RESERVA_29 = 0
REG_TDA_CP1_STT_RESERVA_30 = 0
REG_TDA_CP1_STT_RESERVA_31 = 0
REG_TDA_CP2_COMPORTA_OPERANDO = 0
REG_TDA_CP2_REPONDO_COMPORTA = 0
REG_TDA_CP2_ABRINDO_COMPORTA = 0
REG_TDA_CP2_AGUARDANDO_COMANDO_ABERTURA = 0
REG_TDA_CP2_PRESSAO_EQUALIZADA = 0
REG_TDA_CP2_EQUALIZANDO_PRESSAO = 0
REG_TDA_CP2_ABRINDO_CRACKING = 0
REG_TDA_CP2_FECHANDO_COMPORTA = 0
REG_TDA_CP2_FECHAMENTO_FINALIZADO = 0
REG_TDA_CP2_FALHA_COMUNICACAO_CLP_UG = 0
REG_TDA_CP2_ALARME_DIFERENCIAL_GRADE = 0
REG_TDA_CP2_STT_RESERVA_11 = 0
REG_TDA_CP2_STT_RESERVA_12 = 0
REG_TDA_CP2_STT_RESERVA_13 = 0
REG_TDA_CP2_STT_RESERVA_14 = 0
REG_TDA_CP2_STT_RESERVA_15 = 0
REG_TDA_CP2_STT_RESERVA_16 = 0
REG_TDA_CP2_STT_RESERVA_17 = 0
REG_TDA_CP2_STT_RESERVA_18 = 0
REG_TDA_CP2_STT_RESERVA_19 = 0
REG_TDA_CP2_STT_RESERVA_20 = 0
REG_TDA_CP2_STT_RESERVA_21 = 0
REG_TDA_CP2_STT_RESERVA_22 = 0
REG_TDA_CP2_STT_RESERVA_23 = 0
REG_TDA_CP2_STT_RESERVA_24 = 0
REG_TDA_CP2_STT_RESERVA_25 = 0
REG_TDA_CP2_STT_RESERVA_26 = 0
REG_TDA_CP2_STT_RESERVA_27 = 0
REG_TDA_CP2_STT_RESERVA_28 = 0
REG_TDA_CP2_STT_RESERVA_29 = 0
REG_TDA_CP2_STT_RESERVA_30 = 0
REG_TDA_CP2_STT_RESERVA_31 = 0
REG_TDA_FALHA_NIVEL_MONTANTE = 0
REG_TDA_FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_1 = 0
REG_TDA_FALHA_NIVEL_JUSANTE_COMPORTA_1 = 0
REG_TDA_FALHA_NIVEL_JUSANTE_GRADE_COMPORTA_2 = 0
REG_TDA_FALHA_NIVEL_JUSANTE_COMPORTA_2 = 0
REG_TDA_FALHA_ENTRADA_ANALOGICA_RESERVA_1 = 0
REG_TDA_FALHA_ENTRADA_ANALOGICA_RESERVA_2 = 0
REG_TDA_FALHA_ENTRADA_ANALOGICA_RESERVA_3 = 0
REG_TDA_FALSE = 0
REG_TDA_TRUE = 0
REG_TDA_UH_UNIDADE_HIDRAULICA_OK = 0
REG_TDA_UH_UNIDADE_HIDRAULICA_DISPONIVEL = 0
REG_TDA_UH_FALHA_LIGAR_BOMBA = 0
REG_TDA_UH_FALHA_DESLIGAR_BOMBA = 0
REG_TDA_UH_STT_RESERVA_04 = 0
REG_TDA_UH_STT_RESERVA_05 = 0
REG_TDA_UH_STT_RESERVA_06 = 0
REG_TDA_UH_STT_RESERVA_07 = 0
REG_TDA_UH_STT_RESERVA_08 = 0
REG_TDA_UH_STT_RESERVA_09 = 0
REG_TDA_UH_STT_RESERVA_10 = 0
REG_TDA_UH_STT_RESERVA_11 = 0
REG_TDA_UH_STT_RESERVA_12 = 0
REG_TDA_UH_STT_RESERVA_13 = 0
REG_TDA_UH_STT_RESERVA_14 = 0
REG_TDA_UH_STT_RESERVA_15 = 0
REG_TDA_UH_STT_RESERVA_16 = 0
REG_TDA_UH_STT_RESERVA_17 = 0
REG_TDA_UH_STT_RESERVA_18 = 0
REG_TDA_UH_STT_RESERVA_19 = 0
REG_TDA_UH_STT_RESERVA_20 = 0
REG_TDA_UH_STT_RESERVA_21 = 0
REG_TDA_UH_STT_RESERVA_22 = 0
REG_TDA_UH_STT_RESERVA_23 = 0
REG_TDA_UH_STT_RESERVA_24 = 0
REG_TDA_UH_STT_RESERVA_25 = 0
REG_TDA_UH_STT_RESERVA_26 = 0
REG_TDA_UH_STT_RESERVA_27 = 0
REG_TDA_UH_STT_RESERVA_28 = 0
REG_TDA_UH_STT_RESERVA_29 = 0
REG_TDA_UH_STT_RESERVA_30 = 0
REG_TDA_UH_STT_RESERVA_31 = 0
REG_TDA_HEARTBEAT = 0
REG_TDA_CP1_BLOQUEIO_ATUADO = 0
REG_TDA_CP2_BLOQUEIO_ATUADO = 0
REG_TDA_ACN_SAIDA_DIGITAL_RESERVA_2 = 0
REG_TDA_ACN_SAIDA_DIGITAL_RESERVA_3 = 0
REG_TDA_ACN_SAIDA_DIGITAL_RESERVA_4 = 0
REG_TDA_ACN_SAIDA_DIGITAL_RESERVA_5 = 0
REG_TDA_ACN_SAIDA_DIGITAL_RESERVA_6 = 0
REG_TDA_ACN_SAIDA_DIGITAL_RESERVA_7 = 0
REG_TDA_ACN_SAIDA_DIGITAL_RESERVA_8 = 0
REG_TDA_ACN_SAIDA_DIGITAL_RESERVA_9 = 0
REG_TDA_STT_UG1_HEARTBEAT = 0
REG_TDA_STT_UG1_PERMISSIVO_ABERTURA = 0
REG_TDA_STT_UG1_OPERANDO_SINCRONIZADA = 0
REG_TDA_STT_UG1_RESERVA_3 = 0
REG_TDA_STT_UG1_RESERVA_4 = 0
REG_TDA_STT_UG1_RESERVA_5 = 0
REG_TDA_STT_UG1_RESERVA_6 = 0
REG_TDA_STT_UG1_RESERVA_7 = 0
REG_TDA_STT_UG1_RESERVA_8 = 0
REG_TDA_STT_UG1_RESERVA_9 = 0
REG_TDA_STT_UG1_RESERVA_10 = 0
REG_TDA_STT_UG1_RESERVA_11 = 0
REG_TDA_STT_UG1_RESERVA_12 = 0
REG_TDA_STT_UG1_RESERVA_13 = 0
REG_TDA_STT_UG1_RESERVA_14 = 0
REG_TDA_STT_UG1_RESERVA_15 = 0
REG_TDA_STT_UG1_RESERVA_16 = 0
REG_TDA_STT_UG1_RESERVA_17 = 0
REG_TDA_STT_UG1_RESERVA_18 = 0
REG_TDA_STT_UG1_RESERVA_19 = 0
REG_TDA_STT_UG1_RESERVA_20 = 0
REG_TDA_STT_UG1_RESERVA_21 = 0
REG_TDA_STT_UG1_RESERVA_22 = 0
REG_TDA_STT_UG1_RESERVA_23 = 0
REG_TDA_STT_UG1_RESERVA_24 = 0
REG_TDA_STT_UG1_RESERVA_25 = 0
REG_TDA_STT_UG1_RESERVA_26 = 0
REG_TDA_STT_UG1_RESERVA_27 = 0
REG_TDA_STT_UG1_RESERVA_28 = 0
REG_TDA_STT_UG1_RESERVA_29 = 0
REG_TDA_STT_UG1_RESERVA_30 = 0
REG_TDA_STT_UG1_RESERVA_31 = 0
REG_TDA_STT_UG2_HEARTBEAT = 0
REG_TDA_STT_UG2_PERMISSIVO_ABERTURA = 0
REG_TDA_STT_UG2_OPERANDO_SINCRONIZADA = 0
REG_TDA_STT_UG2_RESERVA_3 = 0
REG_TDA_STT_UG2_RESERVA_4 = 0
REG_TDA_STT_UG2_RESERVA_5 = 0
REG_TDA_STT_UG2_RESERVA_6 = 0
REG_TDA_STT_UG2_RESERVA_7 = 0
REG_TDA_STT_UG2_RESERVA_8 = 0
REG_TDA_STT_UG2_RESERVA_9 = 0
REG_TDA_STT_UG2_RESERVA_10 = 0
REG_TDA_STT_UG2_RESERVA_11 = 0
REG_TDA_STT_UG2_RESERVA_12 = 0
REG_TDA_STT_UG2_RESERVA_13 = 0
REG_TDA_STT_UG2_RESERVA_14 = 0
REG_TDA_STT_UG2_RESERVA_15 = 0
REG_TDA_STT_UG2_RESERVA_16 = 0
REG_TDA_STT_UG2_RESERVA_17 = 0
REG_TDA_STT_UG2_RESERVA_18 = 0
REG_TDA_STT_UG2_RESERVA_19 = 0
REG_TDA_STT_UG2_RESERVA_20 = 0
REG_TDA_STT_UG2_RESERVA_21 = 0
REG_TDA_STT_UG2_RESERVA_22 = 0
REG_TDA_STT_UG2_RESERVA_23 = 0
REG_TDA_STT_UG2_RESERVA_24 = 0
REG_TDA_STT_UG2_RESERVA_25 = 0
REG_TDA_STT_UG2_RESERVA_26 = 0
REG_TDA_STT_UG2_RESERVA_27 = 0
REG_TDA_STT_UG2_RESERVA_28 = 0
REG_TDA_STT_UG2_RESERVA_29 = 0
REG_TDA_STT_UG2_RESERVA_30 = 0
REG_TDA_STT_UG2_RESERVA_31 = 0
REG_TDA_CP1_PERMISSIVOS_OK = 0
REG_TDA_CP2_PERMISSIVOS_OK = 0
REG_TDA_STT_BORBOLETA_REPONDO = 0
REG_TDA_STT_BORBOLETA_FECHANDO = 0
REG_TDA_STT_BORBOLETA_ABRINDO = 0
REG_TDA_STT_BORBOLETA_ABERTURA_FINALIZADA = 0
REG_TDA_BORBOLETA_CMD_RESET_FALHAS = 0
REG_TDA_BORBOLETA_CMD_MANUTENCAO = 0
REG_TDA_BORBOLETA_CMD_AUTOMATICO = 0
REG_TDA_BORBOLETA_CMD_FECHA = 0
REG_TDA_BORBOLETA_CMD_ABRE = 0
REG_TDA_BORBOLETA_CMD_RESERVA_05 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_06 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_07 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_08 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_09 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_10 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_11 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_12 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_13 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_14 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_15 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_16 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_17 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_18 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_19 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_20 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_21 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_22 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_23 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_24 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_25 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_26 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_27 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_28 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_29 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_30 = 0
REG_TDA_BORBOLETA_CMD_RESERVA_31 = 0
REG_TDA_VB_HABILITA_UNIDADE_HIDRAULICA = 0
REG_TDA_VB_PERMISSIVOS_OK = 0
REG_TDA_VB_BLOQUEIO_ATUADO = 0
REG_TDA_VB_EM_MANUTENCAO = 0
REG_TDA_LG_PERMISSIVOS_OK = 0
REG_TDA_LG_FALHA_ATUADA = 0
REG_TDA_LG_OPERACAO_MANUAL = 0
REG_TDA_LG_AVANCANDO_PORTICO = 0
REG_TDA_LG_AFASTANDO_RASTELO = 0
REG_TDA_LG_DESCENDO_RASTELO = 0
REG_TDA_LG_APROXIMANDO_RASTELO = 0
REG_TDA_LG_SUBINDO_RASTELO = 0
REG_TDA_LG_RETORNANDO_PORTICO = 0
REG_TDA_LG_CMD_REARME_FALHAS = 0
REG_TDA_LG_CMD_RECOLHE_POSICAO_INICIAL = 0
REG_TDA_LG_CMD_INICIA_CICLO_LIMPEZA = 0
REG_TDA_LG_CMD_PULA_CICLO = 0
REG_TDA_LG_CMD_LIMPEZA_DIF_GRADE_HABILITA = 0
REG_TDA_LG_CMD_LIMPEZA_DIF_GRADE_DESABILITA = 0
REG_TDA_LG_CMD_RESERVA_06 = 0
REG_TDA_LG_CMD_RESERVA_07 = 0
REG_TDA_LG_CMD_RESERVA_08 = 0
REG_TDA_LG_CMD_RESERVA_09 = 0
REG_TDA_LG_CMD_RESERVA_10 = 0
REG_TDA_LG_CMD_RESERVA_11 = 0
REG_TDA_LG_CMD_RESERVA_12 = 0
REG_TDA_LG_CMD_RESERVA_13 = 0
REG_TDA_LG_CMD_RESERVA_14 = 0
REG_TDA_LG_CMD_RESERVA_15 = 0
REG_TDA_LG_CMD_RESERVA_16 = 0
REG_TDA_LG_CMD_RESERVA_17 = 0
REG_TDA_LG_CMD_RESERVA_18 = 0
REG_TDA_LG_CMD_RESERVA_19 = 0
REG_TDA_LG_CMD_RESERVA_20 = 0
REG_TDA_LG_CMD_RESERVA_21 = 0
REG_TDA_LG_CMD_RESERVA_22 = 0
REG_TDA_LG_CMD_RESERVA_23 = 0
REG_TDA_LG_CMD_RESERVA_24 = 0
REG_TDA_LG_CMD_RESERVA_25 = 0
REG_TDA_LG_CMD_RESERVA_26 = 0
REG_TDA_LG_CMD_RESERVA_27 = 0
REG_TDA_LG_CMD_RESERVA_28 = 0
REG_TDA_LG_CMD_RESERVA_29 = 0
REG_TDA_LG_CMD_RESERVA_30 = 0
REG_TDA_LG_CMD_RESERVA_31 = 0
REG_TDA_LG_PRIMEIRO_CICLO = 0
REG_TDA_LG_SEGUNDO_CICLO = 0
REG_TDA_LG_TERCEIRO_CICLO = 0
REG_TDA_LG_QUARTO_CICLO = 0
REG_TDA_LG_LIMPEZA_DIF_GRADE_HABILITADA = 0
REG_TDA_LG_PULSO_DIF_GRADE = 0

REG_SA_SA_DRENAGEM_BOMBA_1_FALHA = 0
REG_SA_SA_DRENAGEM_BOMBA_1_LIGADA = 0
REG_SA_SA_DRENAGEM_BOMBA_2_FALHA = 0
REG_SA_SA_DRENAGEM_BOMBA_2_LIGADA = 0
REG_SA_SA_DRENAGEM_BOMBA_3_FALHA = 0
REG_SA_SA_DRENAGEM_BOMBA_3_LIGADA = 0
REG_SA_SA_FILTRAGEM_BOMBA_FALHA = 0
REG_SA_SA_FILTRAGEM_BOMBA_LIGADA = 0
REG_SA_SA_ACION_RESERVA_1_FALHA = 0
REG_SA_SA_ACION_RESERVA_1_LIGADO = 0
REG_SA_SA_ACION_RESERVA_2_FALHA = 0
REG_SA_SA_ACION_RESERVA_2_LIGADO = 0
REG_SA_SA_DRENAGEM_UNIDADES_BOMBA_FALHA = 0
REG_SA_SA_DRENAGEM_UNIDADES_BOMBA_LIGADA = 0
REG_SA_SA_BOMBA_RECALQUE_TUBO_SUCCAO_FALHA = 0
REG_SA_SA_BOMBA_RECALQUE_TUBO_SUCCAO_LIGADA = 0
REG_SA_SA_ACION_RESERVA_3_FALHA = 0
REG_SA_SA_ACION_RESERVA_3_LIGADO = 0
REG_SA_SA_FILTRO_B_ELEM_1_ENTRADA_ABERTA = 0
REG_SA_SA_FILTRO_B_ELEM_2_ENTRADA_ABERTA = 0
REG_SA_SA_FILTRO_B_ELEM_1_RETROLAVAGEM_ABERTA = 0
REG_SA_SA_FILTRO_B_ELEM_2_RETROLAVAGEM_ABERTA = 0
REG_SA_SA_FILTRO_B_PRESSAO_SAIDA = 0
REG_SA_SA_COM_TENSAO_LINHA_EXTERNA = 0
REG_SA_SA_ENTRADA_DIGITAL_RESERVA_2 = 0
REG_SA_SA_POCO_DRENAGEM_NIVEL_MUITO_ALTO = 0
REG_SA_SA_POCO_DRENAGEM_NIVEL_ALTO = 0
REG_SA_SA_POCO_DRENAGEM_NIVEL_LIGA_BOMBAS = 0
REG_SA_SA_POCO_DRENAGEM_NIVEL_DESL_BOMBAS = 0
REG_SA_SA_POCO_DRENAGEM_NIVEL_BLOQ_BOMBAS = 0
REG_SA_SA_RETIFICADOR_SOBRETENSAO = 0
REG_SA_SA_RETIFICADOR_SUBTENSAO = 0
REG_SA_SA_RETIFICADOR_SOBRECORRENTE_SAIDA = 0
REG_SA_SA_RETIFICADOR_SOBRECORRENTE_BATERIAS = 0
REG_SA_SA_RETIFICADOR_FUSIVEL_QUEIMADO = 0
REG_SA_SA_RETIFICADOR_FALTA_CA = 0
REG_SA_SA_RETIFICADOR_FALHA_GERAL = 0
REG_SA_SA_RETIFICADOR_FUGA_TERRA_POSITIVO = 0
REG_SA_SA_RETIFICADOR_FUGA_TERRA_NEGATIVO = 0
REG_SA_SE_CFB_52G101_FECHADO = 0
REG_SA_SE_CFB_52G101_SOBRECORRENTE = 0
REG_SA_SE_CFB_PORTA_INTERNA_FECHADA = 0
REG_SA_SE_CFB_PORTA_TRASEIRA_FECHADA = 0
REG_SA_ENTRADA_DIGITAL_RESERVA_12 = 0
REG_SA_SE_89L_FECHADA = 0
REG_SA_ENTRADA_DIGITAL_RESERVA_1 = 0
REG_SA_SE_52L_FECHADO = 0
REG_SA_ENTRADA_DIGITAL_RESERVA_2 = 0
REG_SA_SE_52L_MOLA_CARREGADA = 0
REG_SA_SE_52L_PORTA_INTERNA_FECHADA = 0
REG_SA_SE_TE_ALARME_TEMPERATURA_OLEO = 0
REG_SA_SE_TE_TRIP_TEMPERATURA_OLEO = 0
REG_SA_SE_TE_ALARME_TEMPERATURA_ENROLAMENTO = 0
REG_SA_SE_TE_TRIP_TEMPERATURA_ENROLAMENTO = 0
REG_SA_SE_TE_ALARME_RELE_BUCHHOLZ = 0
REG_SA_SE_TE_TRIP_RELE_BUCHHOLZ = 0
REG_SA_SE_TE_ALARME_ALIVIO_PRESSAO = 0
REG_SA_SE_TE_TRIP_ALIVIO_PRESSAO = 0
REG_SA_SE_TE_NIVEL_OLEO_MUITO_ALTO = 0
REG_SA_SE_TE_NIVEL_OLEO_MUITO_BAIXO = 0
REG_SA_SA_ENTRADA_DIGITAL_RESERVA_13 = 0
REG_SA_SA_ENTRADA_DIGITAL_RESERVA_14 = 0
REG_SA_SE_86BF_ATUACAO_RESERVA = 0
REG_SA_SA_52SA1_SEM_FALHA = 0
REG_SA_SA_52SA1_FECHADO = 0
REG_SA_SA_52SA2_SEM_FALHA = 0
REG_SA_SA_52SA2_FECHADO = 0
REG_SA_SA_52SA3_SEM_FALHA = 0
REG_SA_SA_52SA3_FECHADO = 0
REG_SA_SA_COM_TENSAO_ENTRADA_52SA1 = 0
REG_SA_SA_COM_TENSAO_ENTRADA_52SA2 = 0
REG_SA_SA_COM_TENSAO_BARRA_ESSENCIAIS = 0
REG_SA_SA_COM_TENSAO_BARRA_NAO_ESSENCIAIS = 0
REG_SA_SA_DISJUNTORES_BARRA_SELETORA_REMOTO = 0
REG_SA_SE_52L_SELETORA_REMOTO = 0
REG_SA_SA_CONVERSOR_FIBRA_BAY_SEM_FALHA = 0
REG_SA_SA_CONVERSOR_FIBRA_TA_SEM_FALHA = 0
REG_SA_SA_SEM_EMERGENCIA = 0
REG_SA_SE_RELE_LINHA_ATUADO = 0
REG_SA_SE_RELE_LINHA_WATHDOG = 0
REG_SA_SE_RELE_LINHA_ATUACAO_BF = 0
REG_SA_SE_TE_RELE_ATUADO = 0
REG_SA_SE_TE_RELE_WATCHDOG = 0
REG_SA_SE_86BF_ATUADO = 0
REG_SA_SE_86T_ATUADO = 0
REG_SA_SE_SUPERVISAO_BOBINAS_RELES_BLOQUEIOS = 0
REG_SA_SE_REARME_86BF_86T = 0
REG_SA_SA_REARME_BLOQUEIO_GERAL_E_FALHAS_SA = 0
REG_SA_SE_86T_ATUACAO_RESERVA_1 = 0
REG_SA_SE_86T_ATUACAO_RESERVA_2 = 0
REG_SA_UG1_CMD_HABILITA_SISTEMA_AGUA = 0
REG_SA_UG1_CMD_RESERVA_2 = 0
REG_SA_UG1_CMD_RESERVA_3 = 0
REG_SA_UG2_CMD_HABILITA_SISTEMA_AGUA = 0
REG_SA_UG2_CMD_RESERVA_2 = 0
REG_SA_UG2_CMD_RESERVA_3 = 0
REG_SA_SE_TE_FALHA_CONTROLADOR_LOCAL = 0
REG_SA_SA_FILTRO_A_ELEM_1_ENTRADA_ABERTA = 0
REG_SA_SA_FILTRO_A_ELEM_2_ENTRADA_ABERTA = 0
REG_SA_SA_FILTRO_A_ELEM_1_RETROLAVAGEM_ABERTA = 0
REG_SA_SA_FILTRO_A_ELEM_2_RETROLAVAGEM_ABERTA = 0
REG_SA_SA_FILTRO_A_PRESSAO_SAIDA = 0
REG_SA_SISTEMA_INCENDIO_ALARME_ATUADO = 0
REG_SA_SISTEMA_SEGURANCA_ALARME_ATUADO = 0
REG_SA_ENTRADA_DIGITAL_RESERVA_8 = 0
REG_SA_ENTRADA_DIGITAL_RESERVA_10 = 0
REG_SA_SA_72SA1_FECHADO = 0
REG_SA_SA_DISJUNTORES_125VCC_FECHADOS = 0
REG_SA_SA_DISJUNTORES_24VCC_FECHADOS = 0
REG_SA_SA_COM_TENSAO_ALIMENTACAO_125VCC = 0
REG_SA_SA_COM_TENSAO_COMANDO_125VCC = 0
REG_SA_SA_COM_TENSAO_COMANDO_24VCC = 0
REG_SA_ACN_SE_CMD_FECHA_52L = 0
REG_SA_ACN_SE_CMD_ABRE_52L = 0
REG_SA_ACN_SA_CMD_FECHA_52SA1 = 0
REG_SA_ACN_SA_CMD_ABRE_52SA1 = 0
REG_SA_ACN_SA_CMD_FECHA_52SA2 = 0
REG_SA_ACN_SA_CMD_ABRE_52SA2 = 0
REG_SA_ACN_SA_CMD_FECHA_52SA3 = 0
REG_SA_ACN_SA_CMD_ABRE_52SA3 = 0
REG_SA_ACN_SA_CMD_DRENAGEM_SELECIONA_SEQ_123 = 0
REG_SA_ACN_SA_CMD_DRENAGEM_SELECIONA_SEQ_231 = 0
REG_SA_ACN_SA_CMD_DRENAGEM_SELECIONA_SEQ_312 = 0
REG_SA_ACN_SA_CMD_WHATCHDOG_PARA_DRENAGEM = 0
REG_SA_ACN_SA_CMD_LIGA_BOMBA_SISTEMA_FILTRAGEM = 0
REG_SA_ACN_SA_CMD_LIGA_ACIONAMENTO_RESERVA_1 = 0
REG_SA_ACN_SA_CMD_LIGA_ACIONAMENTO_RESERVA_2 = 0
REG_SA_ACN_SA_DESLIGA_GMG = 0
REG_SA_ACN_SA_CMD_LIGA_BOMBA_RECALQUE_SUCCAO = 0
REG_SA_ACN_SA_CMD_LIGA_ACIONAMENTO_RESERVA_4 = 0
REG_SA_ACN_SE_CMD_REARME_86BF = 0
REG_SA_ACN_SE_CMD_REARME_86T = 0
REG_SA_ACN_SE_CMD_ATUA_86T = 0
REG_SA_ACN_SA_UG1_UG2_SEM_BLOQUEIO_EXTERNO = 0
REG_SA_ACN_SA_UG1_UG2_SISTEMA_AGUA_OK = 0
REG_SA_ACN_SA_UG1_UG2_COM_TENSAO_BARRA_ESSENCIAIS = 0
REG_SA_ACN_SA_FILTRO_B_ABRE_ENTRADA_ELEMENTO_1 = 0
REG_SA_ACN_SA_FILTRO_B_ABRE_ENTRADA_ELEMENTO_2 = 0
REG_SA_ACN_SA_FILTRO_B_ABRE_RETROLAVAGEM_ELEMENTO_1 = 0
REG_SA_ACN_SA_FILTRO_B_ABRE_RETROLAVAGEM_ELEMENTO_2 = 0
REG_SA_ACN_SA_FILTRO_A_ABRE_ENTRADA_ELEMENTO_1 = 0
REG_SA_ACN_SA_FILTRO_A_ABRE_ENTRADA_ELEMENTO_2 = 0
REG_SA_ACN_SA_FILTRO_A_ABRE_RETROLAVAGEM_ELEMENTO_1 = 0
REG_SA_ACN_SA_FILTRO_A_ABRE_RETROLAVAGEM_ELEMENTO_2 = 0
REG_SA_SA_NIVEL_CANAL_DE_FUGA = 0
REG_SA_SE_TE_TEMPERATURA_OLEO = 0
REG_SA_SE_TE_TEMPERATURA_ENROLAMENTO = 0
REG_SA_SA_FILTRO_B_PRESSAO_DIFERENCIAL_ELEMENTO_1 = 0
REG_SA_SA_FILTRO_B_PRESSAO_DIFERENCIAL_ELEMENTO_2 = 0
REG_SA_SA_FILTRO_A_PRESSAO_DIFERENCIAL_ELEMENTO_1 = 0
REG_SA_SA_FILTRO_A_PRESSAO_DIFERENCIAL_ELEMENTO_2 = 0
REG_SA_ENTRADA_ANALOGICA_RESERVA_5 = 0
REG_SA_CMD_SA_RESET_FALHAS_BARRA_CA = 0
REG_SA_CMD_SA_RESET_FALHAS_SISTEMA_AGUA = 0
REG_SA_CMD_SA_RESET_FALHAS_RESERVA_1 = 0
REG_SA_CMD_SA_RESET_FALHAS_RESERVA_2 = 0
REG_SA_SA_FALHA_ABRIR_52SA1 = 0
REG_SA_SA_FALHA_FECHAR_52SA1 = 0
REG_SA_SA_FALHA_ABRIR_52SA2 = 0
REG_SA_SA_FALHA_FECHAR_52SA2 = 0
REG_SA_SA_FALHA_ABRIR_52SA3 = 0
REG_SA_SA_FALHA_FECHAR_52SA3 = 0
REG_SA_CMD_SE_REARME_BLOQUEIO_GERAL = 0
REG_SA_CMD_SE_REARME_86T = 0
REG_SA_CMD_SE_REARME_86BF = 0
REG_SA_CMD_SE_ABRE_52L = 0
REG_SA_CMD_SE_FECHA_52L = 0
REG_SA_SE_BLOQUEIO_86T_ATUADO = 0
REG_SA_SE_REGISTRO_ATUACAO_RELE_LINHA = 0
REG_SA_SE_FALHA_COMANDO_ABERTURA_52L = 0
REG_SA_SA_SISTEMA_AGUA_BOMBA_DISPONIVEL = 0
REG_SA_SA_SISTEMA_AGUA_FALHA_LIGA_BOMBA = 0
REG_SA_SA_SISTEMA_AGUA_FALHA_DESL_BOMBA = 0
REG_SA_SA_SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_A = 0
REG_SA_SA_SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_A = 0
REG_SA_SA_FILTRO_B_INDICACAO_OPERACAO_ELEMENTO_1 = 0
REG_SA_SA_FILTRO_B_INDICACAO_LIMPEZA_ELEMENTO_2 = 0
REG_SA_SA_FILTRO_B_INDICACAO_OPERACAO_ELEMENTO_2 = 0
REG_SA_SA_FILTRO_B_INDICACAO_LIMPEZA_ELEMENTO_1 = 0
REG_SA_SA_FILTRO_B_FALHA_ABRIR_ENTRADA_ELEMENTO_1 = 0
REG_SA_SA_FILTRO_B_FALHA_FECHAR_ENTRADA_ELEMENTO_1 = 0
REG_SA_SA_FILTRO_B_FALHA_ABRIR_ENTRADA_ELEMENTO_2 = 0
REG_SA_SA_FILTRO_B_FALHA_FECHAR_ENTRADA_ELEMENTO_2 = 0
REG_SA_SA_FILTRO_B_FALHA_ABRIR_RETROLAVAGEM_ELEMENTO_1 = 0
REG_SA_SA_FILTRO_B_FALHA_FECHAR_RETROLAVAGEM_ELEMENTO_1 = 0
REG_SA_SA_FILTRO_B_FALHA_ABRIR_RETROLAVAGEM_ELEMENTO_2 = 0
REG_SA_SA_FILTRO_B_FALHA_FECHAR_RETROLAVAGEM_ELEMENTO_2 = 0
REG_SA_SA_FILTRO_B_REVEZAMENTO_EM_MANUAL = 0
REG_SA_SA_STT_RESERVA_02 = 0
REG_SA_SA_STT_RESERVA_03 = 0
REG_SA_SA_STT_RESERVA_04 = 0
REG_SA_SA_FILTRO_A_INDICACAO_OPERACAO_ELEMENTO_1 = 0
REG_SA_SA_FILTRO_A_INDICACAO_LIMPEZA_ELEMENTO_2 = 0
REG_SA_SA_FILTRO_A_INDICACAO_OPERACAO_ELEMENTO_2 = 0
REG_SA_SA_FILTRO_A_INDICACAO_LIMPEZA_ELEMENTO_1 = 0
REG_SA_SA_FILTRO_A_FALHA_ABRIR_ENTRADA_ELEMENTO_1 = 0
REG_SA_SA_FILTRO_A_FALHA_FECHAR_ENTRADA_ELEMENTO_1 = 0
REG_SA_SA_FILTRO_A_FALHA_ABRIR_ENTRADA_ELEMENTO_2 = 0
REG_SA_SA_FILTRO_A_FALHA_FECHAR_ENTRADA_ELEMENTO_2 = 0
REG_SA_SA_FILTRO_A_FALHA_ABRIR_RETROLAVAGEM_ELEMENTO_1 = 0
REG_SA_SA_FILTRO_A_FALHA_FECHAR_RETROLAVAGEM_ELEMENTO_1 = 0
REG_SA_SA_FILTRO_A_FALHA_ABRIR_RETROLAVAGEM_ELEMENTO_2 = 0
REG_SA_SA_FILTRO_A_FALHA_FECHAR_RETROLAVAGEM_ELEMENTO_2 = 0
REG_SA_SA_FILTRO_A_REVEZAMENTO_EM_MANUAL = 0
REG_SA_SA_STT_RESERVA_18 = 0
REG_SA_SA_STT_RESERVA_19 = 0
REG_SA_SA_STT_RESERVA_20 = 0
REG_SA_SA_SISTEMA_AGUA_FALHA_PRESSURIZAR_FILTRO_B = 0
REG_SA_SA_SISTEMA_AGUA_FALHA_PRESSOSTATO_FILTRO_B = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_03 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_04 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_05 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_06 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_07 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_08 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_09 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_10 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_11 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_12 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_13 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_14 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_15 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_16 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_17 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_18 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_19 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_20 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_21 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_22 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_23 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_24 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_25 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_26 = 0
REG_SA_SA_SISTEMA_AGUA_STT_RESERVA_27 = 0
REG_SA_CMD_SA_RESERVA_1 = 0
REG_SA_CMD_SA_DRENAGEM_SELECIONA_SEQ_123 = 0
REG_SA_CMD_SA_DRENAGEM_SELECIONA_SEQ_231 = 0
REG_SA_CMD_SA_DRENAGEM_SELECIONA_SEQ_312 = 0
REG_SA_SA_GMG_FALHA_PARTIR = 0
REG_SA_SA_GMG_FALHA_PARAR = 0
REG_SA_SA_GMG_PARTIDA_PERIODICA = 0
REG_SA_SA_DRENAGEM_DISCREPANCIA_BOIAS_POCO = 0
REG_SA_CMD_SA_GMG_SELECIONA_OPERACAO_MANUAL = 0
REG_SA_CMD_SA_GMG_SELECIONA_OPERACAO_AUTOMATICA = 0
REG_SA_CMD_SA_GMG_PARTE_MANUAL = 0
REG_SA_CMD_SA_GMG_PARA_MANUAL = 0
REG_SA_SA_GMG_OPERACAO_MANUAL = 0
REG_SA_CMD_SA_RESET_HORIMETRO_BOMBA_1_DRENAGEM = 0
REG_SA_CMD_SA_RESET_HORIMETRO_BOMBA_2_DRENAGEM = 0
REG_SA_CMD_SA_RESET_HORIMETRO_BOMBA_3_DRENAGEM = 0
REG_SA_CMD_SA_RESET_HORIMETRO_BOMBA_DRENAGEM_UNIDADES = 0
REG_SA_CMD_SA_RESET_HORIMETRO_BOMBA_RECALQUE = 0
REG_SA_CMD_SA_RESET_HORIMETRO_BOMBA_SISTEMA_AGUA = 0
REG_SA_CMD_SA_COMUTA_FILTRO_A = 0
REG_SA_CMD_SA_SEL_REVEZAMENTO_AUTO_FILTRO_A = 0
REG_SA_CMD_SA_SEL_REVEZAMENTO_MANUAL_FILTRO_A = 0
REG_SA_CMD_SA_COMUTA_FILTRO_B = 0
REG_SA_CMD_SA_SEL_REVEZAMENTO_AUTO_FILTRO_B = 0
REG_SA_CMD_SA_SEL_REVEZAMENTO_MANUAL_FILTRO_B = 0
REG_SA_CMD_SA_RESERVA_24 = 0
REG_SA_CMD_SA_RESERVA_25 = 0
REG_SA_CMD_SA_RESERVA_26 = 0
REG_SA_CMD_SA_RESERVA_27 = 0
REG_SA_CMD_SA_RESERVA_28 = 0
REG_SA_CMD_SA_RESERVA_29 = 0
REG_SA_CMD_SA_RESERVA_30 = 0
REG_SA_CMD_SA_RESERVA_31 = 0
REG_SA_CMD_SE_RESET_REGISTROS = 0
REG_SA_CMD_SE_RESERVA_06 = 0
REG_SA_CMD_SE_RESERVA_07 = 0
REG_SA_CMD_SE_RESERVA_08 = 0
REG_SA_CMD_SE_RESERVA_09 = 0
REG_SA_CMD_SE_RESERVA_10 = 0
REG_SA_CMD_SE_RESERVA_11 = 0
REG_SA_CMD_SE_RESERVA_12 = 0
REG_SA_CMD_SE_RESERVA_13 = 0
REG_SA_CMD_SE_RESERVA_14 = 0
REG_SA_CMD_SE_RESERVA_15 = 0
REG_SA_CMD_SE_RESERVA_16 = 0
REG_SA_CMD_SE_RESERVA_17 = 0
REG_SA_CMD_SE_RESERVA_18 = 0
REG_SA_CMD_SE_RESERVA_19 = 0
REG_SA_CMD_SE_RESERVA_20 = 0
REG_SA_CMD_SE_RESERVA_21 = 0
REG_SA_CMD_SE_RESERVA_22 = 0
REG_SA_CMD_SE_RESERVA_23 = 0
REG_SA_CMD_SE_RESERVA_24 = 0
REG_SA_CMD_SE_RESERVA_25 = 0
REG_SA_CMD_SE_RESERVA_26 = 0
REG_SA_CMD_SE_RESERVA_27 = 0
REG_SA_CMD_SE_RESERVA_28 = 0
REG_SA_CMD_SE_RESERVA_29 = 0
REG_SA_CMD_SE_RESERVA_30 = 0
REG_SA_CMD_SE_RESERVA_31 = 0
REG_SA_SE_BLOQUEIO_GERAL_ATUADO = 0
REG_SA_SE_FALHA_COMANDO_FECHAMENTO_52L = 0
REG_SA_SE_STT_RESERVA_03 = 0
REG_SA_SE_STT_RESERVA_04 = 0
REG_SA_SE_STT_RESERVA_05 = 0
REG_SA_SE_STT_RESERVA_06 = 0
REG_SA_SE_STT_RESERVA_07 = 0
REG_SA_SE_STT_RESERVA_08 = 0
REG_SA_SE_STT_RESERVA_09 = 0
REG_SA_SE_STT_RESERVA_10 = 0
REG_SA_SE_STT_RESERVA_11 = 0
REG_SA_SE_STT_RESERVA_12 = 0
REG_SA_SE_STT_RESERVA_13 = 0
REG_SA_SE_STT_RESERVA_14 = 0
REG_SA_SE_STT_RESERVA_15 = 0
REG_SA_SE_STT_RESERVA_16 = 0
REG_SA_SE_STT_RESERVA_17 = 0
REG_SA_SE_STT_RESERVA_18 = 0
REG_SA_SE_STT_RESERVA_19 = 0
REG_SA_SE_STT_RESERVA_20 = 0
REG_SA_SE_STT_RESERVA_21 = 0
REG_SA_SE_STT_RESERVA_22 = 0
REG_SA_SE_STT_RESERVA_23 = 0
REG_SA_SE_STT_RESERVA_24 = 0
REG_SA_SE_STT_RESERVA_25 = 0
REG_SA_SE_STT_RESERVA_26 = 0
REG_SA_SE_STT_RESERVA_27 = 0
REG_SA_SE_STT_RESERVA_28 = 0
REG_SA_SE_STT_RESERVA_29 = 0
REG_SA_SE_STT_RESERVA_30 = 0
REG_SA_SA_FALHA_NIVEL_CANAL_FUGA = 0
REG_SA_SE_TE_FALHA_TEMPERATURA_OLEO = 0
REG_SA_SE_TE_FALHA_TEMPERATURA_ENROLAMENTO = 0
REG_SA_SA_FALHA_FILTRO_A_PRESSAO_DIFERENCIAL_ELEMENTO_1 = 0
REG_SA_SA_FALHA_FILTRO_A_PRESSAO_DIFERENCIAL_ELEMENTO_2 = 0
REG_SA_SA_FALHA_FILTRO_B_PRESSAO_DIFERENCIAL_ELEMENTO_1 = 0
REG_SA_SA_FALHA_FILTRO_B_PRESSAO_DIFERENCIAL_ELEMENTO_2 = 0
REG_SA_SA_SE_FALHA_ENTRADA_ANALOGICA_RESERVA_05 = 0
REG_SA_SA_ALM_NIVEL_CANAL_FUGA = 0
REG_SA_SE_TE_ALM_TEMPERATURA_OLEO = 0
REG_SA_SE_TE_ALM_TEMPERATURA_ENROLAMENTO = 0
REG_SA_SA_ALM_FILTRO_A_PRESSAO_DIFERENCIAL_ELEMENTO_1 = 0
REG_SA_SA_ALM_FILTRO_A_PRESSAO_DIFERENCIAL_ELEMENTO_2 = 0
REG_SA_SA_ALM_FILTRO_B_PRESSAO_DIFERENCIAL_ELEMENTO_1 = 0
REG_SA_SA_ALM_FILTRO_B_PRESSAO_DIFERENCIAL_ELEMENTO_2 = 0
REG_SA_SA_SE_ALM_ENTRADA_ANALOGICA_RESERVA_05 = 0
REG_SA_SA_SST_RESERVA_11 = 0
REG_SA_SA_SST_RESERVA_12 = 0
REG_SA_SA_SST_RESERVA_13 = 0
REG_SA_SA_SST_RESERVA_14 = 0
REG_SA_SA_SST_RESERVA_15 = 0
REG_SA_SA_SST_RESERVA_16 = 0
REG_SA_SA_SST_RESERVA_17 = 0
REG_SA_SA_SST_RESERVA_18 = 0
REG_SA_SA_SST_RESERVA_19 = 0
REG_SA_SA_SST_RESERVA_20 = 0
REG_SA_SA_SST_RESERVA_21 = 0
REG_SA_SA_SST_RESERVA_22 = 0
REG_SA_SA_SST_RESERVA_23 = 0
REG_SA_SA_SST_RESERVA_24 = 0
REG_SA_SA_SST_RESERVA_25 = 0
REG_SA_SA_SST_RESERVA_26 = 0
REG_SA_SA_SST_RESERVA_27 = 0
REG_SA_SA_SST_RESERVA_28 = 0
REG_SA_SA_SST_RESERVA_29 = 0
REG_SA_SA_SST_RESERVA_30 = 0
REG_SA_SA_SST_RESERVA_31 = 0
REG_SA_SE_STT_RESERVA_31 = 0
REG_SA_FALSE = 0
REG_SA_TRUE = 0
REG_SA_LT_VAB = 0
REG_SA_LT_VBC = 0
REG_SA_LT_VCA = 0
REG_SA_LT_IA = 0
REG_SA_LT_IB = 0
REG_SA_LT_IC = 0
REG_SA_LT_P = 0
REG_SA_LT_Q = 0
REG_SA_LT_S = 0
REG_SA_LT_F = 0
REG_SA_LT_FP = 0
REG_SA_LT_EAP = 0
REG_SA_LT_EAN = 0
REG_SA_LT_ERP = 0
REG_SA_LT_ERN = 0
REG_SA_TSA_VAB = 0
REG_SA_TSA_VBC = 0
REG_SA_TSA_VCA = 0
REG_SA_TSA_IA = 0
REG_SA_TSA_IB = 0
REG_SA_TSA_IC = 0
REG_SA_TSA_P = 0
REG_SA_TSA_Q = 0
REG_SA_TSA_S = 0
REG_SA_TSA_F = 0
REG_SA_TSA_FP = 0
REG_SA_TSA_EAP = 0
REG_SA_GMG_VAB = 0
REG_SA_GMG_VBC = 0
REG_SA_GMG_VCA = 0
REG_SA_GMG_IA = 0
REG_SA_GMG_IB = 0
REG_SA_GMG_IC = 0
REG_SA_GMG_P = 0
REG_SA_GMG_Q = 0
REG_SA_GMG_S = 0
REG_SA_GMG_F = 0
REG_SA_GMG_FP = 0
REG_SA_GMG_EAP = 0