from django.db import models


# Create your models here.
class Contato(models.Model):
    nome = models.CharField(max_length=250)
    numero = models.CharField(max_length=20)


class ParametrosUsina(models.Model):

    modo_autonomo = models.IntegerField()
    status_moa = models.IntegerField()
    emergencia_acionada = models.IntegerField()
    timestamp = models.DateTimeField()
    aguardando_reservatorio = models.IntegerField()
    clp_online = models.IntegerField()
    clp_ip = models.CharField(max_length=15)
    clp_porta = models.IntegerField()
    modbus_server_ip = models.CharField(max_length=15)
    modbus_server_porta = models.IntegerField()
    kp = models.DecimalField(max_digits=15, decimal_places=10)
    ki = models.DecimalField(max_digits=15, decimal_places=10)
    kd = models.DecimalField(max_digits=15, decimal_places=10)
    kie = models.DecimalField(max_digits=15, decimal_places=10)
    margem_pot_critica = models.DecimalField(max_digits=10, decimal_places=5)
    n_movel_L = models.IntegerField()
    n_movel_R = models.IntegerField()
    nv_alvo = models.DecimalField(max_digits=10, decimal_places=3)
    nv_maximo = models.DecimalField(max_digits=10, decimal_places=3)
    nv_minimo = models.DecimalField(max_digits=10, decimal_places=3)
    nv_montante = models.DecimalField(max_digits=10, decimal_places=3)
    nv_religamento = models.DecimalField(max_digits=10, decimal_places=3)
    pot_minima = models.DecimalField(max_digits=10, decimal_places=5)
    pot_nominal = models.DecimalField(max_digits=10, decimal_places=5)
    pot_nominal_ug = models.DecimalField(max_digits=10, decimal_places=5)
    pot_disp = models.DecimalField(max_digits=10, decimal_places=5)
    timer_erro = models.IntegerField()
    ug1_disp = models.DecimalField(max_digits=10, decimal_places=5)
    ug1_pot = models.DecimalField(max_digits=10, decimal_places=5)
    ug1_setpot = models.DecimalField(max_digits=10, decimal_places=5)
    ug1_sinc = models.IntegerField()
    ug1_tempo = models.IntegerField()
    ug1_prioridade = models.IntegerField()
    ug2_disp = models.DecimalField(max_digits=10, decimal_places=5)
    ug2_pot = models.DecimalField(max_digits=10, decimal_places=5)
    ug2_setpot = models.DecimalField(max_digits=10, decimal_places=5)
    ug2_sinc = models.IntegerField()
    ug2_tempo = models.IntegerField()
    ug2_prioridade = models.IntegerField()
    valor_ie_inicial = models.DecimalField(max_digits=10, decimal_places=5)
    modo_de_escolha_das_ugs = models.IntegerField()
    # modo 1 = hora depois prioridade
    # modo 2 = prioridade depois hora

    pos_comporta = models.IntegerField()
    nv_comporta_pos_0_ant = models.DecimalField(max_digits=10, decimal_places=2)
    nv_comporta_pos_1_ant = models.DecimalField(max_digits=10, decimal_places=2)
    nv_comporta_pos_2_ant = models.DecimalField(max_digits=10, decimal_places=2)
    nv_comporta_pos_3_ant = models.DecimalField(max_digits=10, decimal_places=2)
    nv_comporta_pos_4_ant = models.DecimalField(max_digits=10, decimal_places=2)
    nv_comporta_pos_5_ant = models.DecimalField(max_digits=10, decimal_places=2)
    nv_comporta_pos_0_prox = models.DecimalField(max_digits=10, decimal_places=2)
    nv_comporta_pos_1_prox = models.DecimalField(max_digits=10, decimal_places=2)
    nv_comporta_pos_2_prox = models.DecimalField(max_digits=10, decimal_places=2)
    nv_comporta_pos_3_prox = models.DecimalField(max_digits=10, decimal_places=2)
    nv_comporta_pos_4_prox = models.DecimalField(max_digits=10, decimal_places=2)
    nv_comporta_pos_5_prox = models.DecimalField(max_digits=10, decimal_places=2)

    tolerancia_pot_maxima = models.DecimalField(max_digits=10, decimal_places=5)

    ug1_temp_alerta = models.DecimalField(max_digits=10, decimal_places=2)
    ug2_temp_alerta = models.DecimalField(max_digits=10, decimal_places=2)
    ug1_temp_maxima = models.DecimalField(max_digits=10, decimal_places=2)
    ug2_temp_maxima = models.DecimalField(max_digits=10, decimal_places=2)
    ug1_temp_mancal = models.DecimalField(max_digits=10, decimal_places=2)
    ug2_temp_mancal = models.DecimalField(max_digits=10, decimal_places=2)

    ug1_perda_grade_alerta = models.DecimalField(max_digits=10, decimal_places=3)
    ug2_perda_grade_alerta = models.DecimalField(max_digits=10, decimal_places=3)
    ug1_perda_grade_maxima = models.DecimalField(max_digits=10, decimal_places=3)
    ug2_perda_grade_maxima = models.DecimalField(max_digits=10, decimal_places=3)
    ug1_perda_grade = models.DecimalField(max_digits=10, decimal_places=3)
    ug2_perda_grade = models.DecimalField(max_digits=10, decimal_places=3)

    pot_maxima_alvo = models.DecimalField(max_digits=10, decimal_places=5)

    temperatura_alerta_enrolamento_fase_r_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_enrolamento_fase_s_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_enrolamento_fase_t_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_mancal_la_casquilho_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_mancal_la_contra_escora_1_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_mancal_la_contra_escora_2_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_mancal_la_escora_1_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_mancal_la_escora_2_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_mancal_lna_casquilho_ug1 = models.DecimalField(max_digits=10, decimal_places=5)    
    temperatura_limite_enrolamento_fase_r_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_enrolamento_fase_s_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_enrolamento_fase_t_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_mancal_la_casquilho_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_mancal_la_contra_escora_1_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_mancal_la_contra_escora_2_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_mancal_la_escora_1_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_mancal_la_escora_2_ug1 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_mancal_lna_casquilho_ug1 = models.DecimalField(max_digits=10, decimal_places=5)

    temperatura_alerta_enrolamento_fase_r_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_enrolamento_fase_s_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_enrolamento_fase_t_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_mancal_la_casquilho_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_mancal_la_contra_escora_1_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_mancal_la_contra_escora_2_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_mancal_la_escora_1_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_mancal_la_escora_2_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_alerta_mancal_lna_casquilho_ug2 = models.DecimalField(max_digits=10, decimal_places=5)    
    temperatura_limite_enrolamento_fase_r_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_enrolamento_fase_s_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_enrolamento_fase_t_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_mancal_la_casquilho_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_mancal_la_contra_escora_1_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_mancal_la_contra_escora_2_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_mancal_la_escora_1_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_mancal_la_escora_2_ug2 = models.DecimalField(max_digits=10, decimal_places=5)
    temperatura_limite_mancal_lna_casquilho_ug2 = models.DecimalField(max_digits=10, decimal_places=5)


class Comando(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()

    """
    AGENDAMENTO_RESET_PARMAETROS = 1
    AGENDAMENTO_INDISPONIBILIZAR = 2
    AGENDAMENTO_NORMALIZAR = 3

    AGENDAMENTO_INDISPONIBILIZAR_UG_1 = 10
    AGENDAMENTO_NORMALIZAR_UG_1 = 11

    AGENDAMENTO_INDISPONIBILIZAR_UG_2 = 20
    AGENDAMENTO_NORMALIZAR_UG_2 = 21
    """

