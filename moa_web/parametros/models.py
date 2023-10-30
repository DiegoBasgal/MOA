from django.db import models

# Create your models here.

class ParametrosUsina(models.Model):

    timestamp = models.DateTimeField(default=0)

    # Params Usina
    modo_autonomo = models.IntegerField(default=1)
    emergencia_acionada = models.IntegerField(default=0)
    aguardando_reservatorio = models.IntegerField(default=0)
    modo_de_escolha_das_ugs = models.IntegerField(default=2)

    # Servidores
    clp_online = models.IntegerField(default=1)
    clp_ug1_ip = models.CharField(max_length=15, default="192.168.20.110")
    clp_ug1_porta = models.IntegerField(default=502)
    clp_ug2_ip = models.CharField(max_length=15, default="192.168.20.120")
    clp_ug2_porta = models.IntegerField(default=502)
    clp_sa_ip = models.CharField(max_length=15, default="192.168.20.130")
    clp_sa_porta = models.IntegerField(default=502)
    clp_tda_ip = models.CharField(max_length=15, default="192.168.20.140")
    clp_tda_porta = models.IntegerField(default=502)
    clp_moa_ip = models.CharField(max_length=15, default="0.0.0.0")
    clp_moa_porta = models.IntegerField(default=502)

    # Nível
    nv_alvo = models.DecimalField(max_digits=10, decimal_places=3, default=462)
    nv_maximo = models.DecimalField(max_digits=10, decimal_places=3, default=462.37)
    nv_minimo = models.DecimalField(max_digits=10, decimal_places=3, default=460)
    nv_montante = models.DecimalField(max_digits=10, decimal_places=3, default=460)
    nv_religamento = models.DecimalField(max_digits=10, decimal_places=3, default=461.5)

    # PID IE
    kp = models.DecimalField(max_digits=15, decimal_places=3, default=2)
    ki = models.DecimalField(max_digits=15, decimal_places=3, default=0.1)
    kd = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    kie = models.DecimalField(max_digits=15, decimal_places=3, default=0.1)
    valor_ie_inicial = models.DecimalField(max_digits=10, decimal_places=3, default=0.5)

    # Potência
    pot_minima = models.DecimalField(max_digits=10, decimal_places=0, default=911)
    pot_nominal = models.DecimalField(max_digits=10, decimal_places=1, default=3037.5)
    pot_nominal_ug = models.DecimalField(max_digits=10, decimal_places=1, default=3037.5)
    margem_pot_critica = models.DecimalField(max_digits=10, decimal_places=5, default=0.037)

    # Transformador Elevador
    alerta_temperatura_oleo_trafo = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_oleo_trafo = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    alerta_temperatura_enrolamento_trafo = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_enrolamento_trafo = models.DecimalField(max_digits=10, decimal_places=2, default=200)

    # UG1
    ug1_pot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug1_disp = models.DecimalField(max_digits=10, decimal_places=5, default=1)
    ug1_setpot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug1_prioridade = models.IntegerField(default=0)
    ug1_ultima_etapa = models.IntegerField(default=0)
    ug1_ultimo_estado = models.IntegerField(default=0)
    ug1_pos_comporta = models.IntegerField(default=0)
    ug1_nv_pos_grade = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ug1_perda_grade_maxima = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    alerta_perda_grade_ug1 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    alerta_pressao_turbina_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=1.4)
    alerta_temperatura_fase_r_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_s_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_t_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_nucleo_gerador_1_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_interno_1_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_interno_2_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_patins_mancal_comb_1_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_patins_mancal_comb_2_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_casq_comb_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_contra_esc_comb_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)

    limite_perda_grade_ug1 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    limite_pressao_turbina_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    limite_temperatura_fase_r_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_fase_s_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_fase_t_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_nucleo_gerador_1_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_interno_1_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_interno_2_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_patins_mancal_comb_1_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_patins_mancal_comb_2_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_casq_comb_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_contra_esc_comb_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)

    # UG2
    ug2_pot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug2_disp = models.DecimalField(max_digits=10, decimal_places=5, default=1)
    ug2_setpot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug2_prioridade = models.IntegerField(default=0)
    ug2_ultima_etapa = models.IntegerField(default=0)
    ug2_ultimo_estado = models.IntegerField(default=0)
    ug2_pos_comporta = models.IntegerField(default=0)
    ug2_nv_pos_grade = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ug2_perda_grade_maxima = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    alerta_perda_grade_ug2 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    alerta_pressao_turbina_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=1.4)
    alerta_temperatura_fase_r_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_s_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_t_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_nucleo_gerador_1_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_interno_1_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_interno_2_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_patins_mancal_comb_1_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_patins_mancal_comb_2_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_casq_comb_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_contra_esc_comb_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)

    limite_perda_grade_ug2 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    limite_pressao_turbina_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    limite_temperatura_fase_r_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_fase_s_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_fase_t_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_nucleo_gerador_1_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_interno_1_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_interno_2_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_patins_mancal_comb_1_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_patins_mancal_comb_2_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_casq_comb_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_contra_esc_comb_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)


class Comando(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    executavel_em_manual = models.BooleanField(default=False)
    executavel_em_automatico = models.BooleanField(default=True)


class ControleEstados(models.Model):

    ts = models.DateTimeField(primary_key=True, default=0)

    ultimo_estado_ug1 = models.IntegerField(default=0)
    ultimo_estado_ug2 = models.IntegerField(default=0)
