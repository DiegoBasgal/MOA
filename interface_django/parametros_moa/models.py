from django.db import models


# Create your models here.

class ParametrosUsina(models.Model):

    timestamp = models.DateTimeField(default=0)

    # Params Usina
    modo_autonomo = models.IntegerField(default=1)
    emergencia_acionada = models.IntegerField(default=0)
    aguardando_reservatorio = models.IntegerField(default=0)
    modo_de_escolha_das_ugs = models.IntegerField(default=2)
    tda_offline = models.IntegerField(default=0)

    # Servidores
    clp_online = models.IntegerField(default=1)
    clp_ug1_ip = models.CharField(max_length=15, default="192.168.0.54")
    clp_ug1_porta = models.IntegerField(default=502)
    clp_ug2_ip = models.CharField(max_length=15, default="192.168.0.54")
    clp_ug2_porta = models.IntegerField(default=502)
    clp_ug3_ip = models.CharField(max_length=15, default="192.168.0.54")
    clp_ug3_porta = models.IntegerField(default=502)
    clp_sa_ip = models.CharField(max_length=15, default="192.168.0.54")
    clp_sa_porta = models.IntegerField(default=502)
    clp_tda_ip = models.CharField(max_length=15, default="192.168.0.54")
    clp_tda_porta = models.IntegerField(default=502)
    clp_moa_ip = models.CharField(max_length=15, default="192.168.0.116")
    clp_moa_porta = models.IntegerField(default=502)

    # Nível
    nv_alvo = models.DecimalField(max_digits=10, decimal_places=3, default=405)
    nv_maximo = models.DecimalField(max_digits=10, decimal_places=3, default=405.25)
    nv_minimo = models.DecimalField(max_digits=10, decimal_places=3, default=404.65)
    nv_montante = models.DecimalField(max_digits=10, decimal_places=3, default=405)
    nv_religamento = models.DecimalField(max_digits=10, decimal_places=3, default=404.9)

    # PID IE 
    kp = models.DecimalField(max_digits=15, decimal_places=3, default=2)
    ki = models.DecimalField(max_digits=15, decimal_places=3, default=0.1)
    kd = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    kie = models.DecimalField(max_digits=15, decimal_places=3, default=0.1)
    cx_kp = models.DecimalField(max_digits=5, decimal_places=2, default=2)
    cx_ki = models.DecimalField(max_digits=5, decimal_places=2, default=0.1)
    cx_kie = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    press_cx_alvo = models.DecimalField(max_digits=10, decimal_places=2, default=16.3)
    valor_ie_inicial = models.DecimalField(max_digits=10, decimal_places=1, default=0.5)

    # Potência
    pot_minima = models.DecimalField(max_digits=10, decimal_places=0, default=1360)
    pot_nominal = models.DecimalField(max_digits=10, decimal_places=0, default=9900)
    pot_nominal_ug = models.DecimalField(max_digits=10, decimal_places=0, default=3600)
    margem_pot_critica = models.DecimalField(max_digits=10, decimal_places=5, default=0.037)


    # UG1
    ug1_pot = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    ug1_setpot = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    ug1_prioridade = models.IntegerField(default=0)

    alerta_caixa_espiral_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    limite_caixa_espiral_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    alerta_temperatura_fase_r_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_s_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_t_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_nucleo_estator_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_rad_dia_1_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_rad_dia_2_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_rad_tra_1_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_rad_tra_2_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_saida_de_ar_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_escora_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_radial_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_contra_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)

    limite_temperatura_fase_r_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_fase_s_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_fase_t_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_nucleo_estator_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_rad_dia_1_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_rad_dia_2_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_rad_tra_1_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_rad_tra_2_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_saida_de_ar_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_escora_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_radial_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_contra_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)

    # UG2
    ug2_pot = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    ug2_setpot = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    ug2_prioridade = models.IntegerField(default=0)

    alerta_caixa_espiral_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    limite_caixa_espiral_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    alerta_temperatura_fase_r_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_s_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_t_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_nucleo_estator_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_rad_dia_1_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_rad_dia_2_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_rad_tra_1_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_rad_tra_2_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_saida_de_ar_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_escora_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_radial_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_contra_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)

    limite_temperatura_fase_r_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_fase_s_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_fase_t_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_nucleo_estator_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_rad_dia_1_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_rad_dia_2_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_rad_tra_1_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_rad_tra_2_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_saida_de_ar_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_escora_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_radial_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_contra_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)

    # UG 3
    ug3_pot = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    ug3_setpot = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    ug3_prioridade = models.IntegerField(default=0)

    alerta_caixa_espiral_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    limite_caixa_espiral_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    alerta_temperatura_fase_r_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_s_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_t_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_nucleo_estator_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_rad_dia_1_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_rad_dia_2_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_rad_tra_1_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_rad_tra_2_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_saida_de_ar_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_escora_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_radial_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_mancal_guia_contra_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    limite_temperatura_fase_r_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_fase_s_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_fase_t_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_nucleo_estator_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_rad_dia_1_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_rad_dia_2_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_rad_tra_1_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_rad_tra_2_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_saida_de_ar_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_escora_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_radial_ug3 = models.DecimalField( max_digits=10, decimal_places=2, default=200)
    limite_temperatura_mancal_guia_contra_ug3 = models.DecimalField(max_digits=10, decimal_places=2, default=200)


class Comando(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    executavel_em_manual = models.BooleanField(default=False)
    executavel_em_autmoatico = models.BooleanField(default=True)

class Contato(models.Model):
    nome = models.CharField(max_length=250, default="")
    numero = models.CharField(max_length=20, default="")
    data_inicio = models.DateField(default=0)
    ts_inicio = models.TimeField(default=0)
    data_fim = models.DateField(default=0)
    ts_fim = models.TimeField(default=0)