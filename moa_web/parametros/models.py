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
    clp_ug1_ip = models.CharField(max_length=15, default="192.168.68.10")
    clp_ug1_porta = models.IntegerField(default=502)
    clp_ug2_ip = models.CharField(max_length=15, default="192.168.68.13")
    clp_ug2_porta = models.IntegerField(default=502)
    clp_ug3_ip = models.CharField(max_length=15, default="192.168.68.16")
    clp_ug3_porta = models.IntegerField(default=502)
    clp_ug4_ip = models.CharField(max_length=15, default="192.168.68.19")
    clp_ug4_porta = models.IntegerField(default=502)
    clp_se_ip = models.CharField(max_length=15, default="192.168.68.22")
    clp_se_porta = models.IntegerField(default=502)
    clp_tda_ip = models.CharField(max_length=15, default="192.168.68.29")
    clp_tda_porta = models.IntegerField(default=502)
    clp_adufas_ip = models.CharField(max_length=15, default="192.168.68.30")
    clp_adufas_porta = models.IntegerField(default=502)
    clp_moa_ip = models.CharField(max_length=15, default="0.0.0.0")
    clp_moa_porta = models.IntegerField(default=502)


    # Nível
    nv_alvo = models.DecimalField(max_digits=10, decimal_places=3, default=817)
    nv_maximo = models.DecimalField(max_digits=10, decimal_places=3, default=818)
    nv_minimo = models.DecimalField(max_digits=10, decimal_places=3, default=816)
    nv_montante = models.DecimalField(max_digits=10, decimal_places=3, default=817)
    nv_religamento = models.DecimalField(max_digits=10, decimal_places=3, default=816.3)
    
    ad_nv_alvo = models.DecimalField(max_digits=15, decimal_places=3, default=818.1)

    # PID IE
    kp = models.DecimalField(max_digits=15, decimal_places=3, default=2)
    ki = models.DecimalField(max_digits=15, decimal_places=3, default=0.1)
    kd = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    kie = models.DecimalField(max_digits=15, decimal_places=3, default=0.1)
    ie_inicial = models.DecimalField(max_digits=10, decimal_places=3, default=0.5)


    # PI Adufas
    ad_kp = models.DecimalField(max_digits=15, decimal_places=3, default=1)
    ad_ki = models.DecimalField(max_digits=15, decimal_places=3, default=0.5)


    # Potência
    pot_minima_ugs = models.DecimalField(max_digits=10, decimal_places=0, default=1700)
    pot_maxima_ugs = models.DecimalField(max_digits=10, decimal_places=1, default=5650)
    pot_maxima_usina = models.DecimalField(max_digits=10, decimal_places=1, default=22600)
    margem_pot_critica = models.DecimalField(max_digits=10, decimal_places=5, default=0.05)


    # UG1
    ug1_pot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug1_disp = models.DecimalField(max_digits=10, decimal_places=5, default=1)
    ug1_setpot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug1_prioridade = models.IntegerField(default=0)
    ug1_ultimo_estado = models.IntegerField(default=0)
    ug1_nv_pos_grade = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ug1_perda_grade_maxima = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    alerta_perda_grade_ug1 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    alerta_pressao_turbina_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=1.4)
    alerta_temperatura_oleo_uhrv_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_oleo_uhlm_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_r_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_s_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_t_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_la_1_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_la_2_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_lna_1_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_lna_2_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_turbina_radial_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_turbina_escora_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_turbina_contra_escora_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)

    limite_perda_grade_ug1 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    limite_pressao_turbina_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=1.4)
    limite_temperatura_oleo_uhrv_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_oleo_uhlm_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_fase_r_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_fase_s_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_fase_t_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_la_1_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_la_2_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_lna_1_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_lna_2_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_turbina_radial_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_turbina_escora_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_turbina_contra_escora_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)


    # UG2
    ug2_pot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug2_disp = models.DecimalField(max_digits=10, decimal_places=5, default=1)
    ug2_setpot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug2_prioridade = models.IntegerField(default=0)
    ug2_ultimo_estado = models.IntegerField(default=0)
    ug2_nv_pos_grade = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ug2_perda_grade_maxima = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    alerta_perda_grade_ug2 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    alerta_pressao_turbina_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=1.4)
    alerta_temperatura_oleo_uhrv_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_oleo_uhlm_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_r_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_s_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_t_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_la_1_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_la_2_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_lna_1_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_lna_2_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_turbina_radial_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_turbina_escora_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_turbina_contra_escora_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)

    limite_perda_grade_ug2 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    limite_pressao_turbina_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=1.4)
    limite_temperatura_oleo_uhrv_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_oleo_uhlm_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_fase_r_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_fase_s_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_fase_t_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_la_1_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_la_2_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_lna_1_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_lna_2_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_turbina_radial_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_turbina_escora_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_turbina_contra_escora_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)


    # UG3
    ug3_pot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug3_disp = models.DecimalField(max_digits=10, decimal_places=5, default=1)
    ug3_setpot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug3_prioridade = models.IntegerField(default=0)
    ug3_ultimo_estado = models.IntegerField(default=0)
    ug3_nv_pos_grade = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ug3_perda_grade_maxima = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    alerta_perda_grade_ug3 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    alerta_pressao_turbina_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=1.4)
    alerta_temperatura_oleo_uhrv_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_oleo_uhlm_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_r_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_s_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_t_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_la_1_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_la_2_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_lna_1_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_lna_2_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_turbina_radial_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_turbina_escora_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_turbina_contra_escora_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)

    limite_perda_grade_ug3 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    limite_pressao_turbina_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=1.4)
    limite_temperatura_oleo_uhrv_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_oleo_uhlm_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_fase_r_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_fase_s_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_fase_t_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_la_1_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_la_2_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_lna_1_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_lna_2_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_turbina_radial_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_turbina_escora_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_turbina_contra_escora_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)


    # UG4
    ug4_pot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug4_disp = models.DecimalField(max_digits=10, decimal_places=5, default=1)
    ug4_setpot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug4_prioridade = models.IntegerField(default=0)
    ug4_ultimo_estado = models.IntegerField(default=0)
    ug4_nv_pos_grade = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ug4_perda_grade_maxima = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    
    alerta_perda_grade_ug4 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    alerta_pressao_turbina_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=1.4)
    alerta_temperatura_oleo_uhrv_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_oleo_uhlm_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_r_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_s_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_t_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_la_1_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_la_2_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_lna_1_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_gerador_lna_2_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_turbina_radial_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_turbina_escora_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_turbina_contra_escora_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)

    limite_perda_grade_ug4 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    limite_pressao_turbina_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=1.4)
    limite_temperatura_oleo_uhrv_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_oleo_uhlm_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_fase_r_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_fase_s_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_fase_t_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_la_1_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_la_2_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_lna_1_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_gerador_lna_2_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_turbina_radial_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_turbina_escora_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_mancal_turbina_contra_escora_ug4 = models.DecimalField(max_digits=10, decimal_places=2, default=100)


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
    ultimo_estado_ug3 = models.IntegerField(default=0)
    ultimo_estado_ug4 = models.IntegerField(default=0)