from django.db import models


# Create your models here.
class Contato(models.Model):
    nome = models.CharField(max_length=250)
    numero = models.CharField(max_length=20)


class ParametrosUsina(models.Model):

    modo_autonomo = models.IntegerField(default=0)
    status_moa = models.IntegerField(default=0)
    emergencia_acionada = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=0)
    aguardando_reservatorio = models.IntegerField(default=1)
    clp_online = models.IntegerField(default=0)
    clp_ip = models.CharField(max_length=15, default="")
    clp_porta = models.IntegerField(default=502)
    modbus_server_ip = models.CharField(max_length=15, default="0.0.0.0")
    modbus_server_porta = models.IntegerField(default=5003)
    kp = models.DecimalField(max_digits=15, decimal_places=10, default=1)
    ki = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    kd = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    kie = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    margem_pot_critica = models.DecimalField(
        max_digits=10, decimal_places=5, default=0.2
    )
    nv_alvo = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    nv_maximo = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    nv_minimo = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    nv_montante = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    nv_religamento = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    pot_minima = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    pot_nominal = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    pot_nominal_ug = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    pot_disp = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    timer_erro = models.IntegerField(default=30)
    valor_ie_inicial = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    modo_de_escolha_das_ugs = models.IntegerField(default=1)
    # modo 1 = hora depois prioridade
    # modo 2 = prioridade depois hora

    # ug1
    ug1_disp = models.DecimalField(max_digits=10, decimal_places=5, default=1)
    ug1_pot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug1_setpot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug1_sinc = models.IntegerField(default=0)
    ug1_tempo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ug1_prioridade = models.IntegerField(default=0)
    alerta_temperatura_fase_r_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_fase_s_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_fase_t_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_nucleo_estator_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_rad_dia_1_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_rad_dia_2_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_rad_tra_1_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_rad_tra_2_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_saida_de_ar_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_guia_escora_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_guia_radial_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_guia_contra_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    limite_temperatura_fase_r_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_fase_s_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_fase_t_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_nucleo_estator_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_rad_dia_1_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_rad_dia_2_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_rad_tra_1_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_rad_tra_2_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_saida_de_ar_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_guia_escora_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_guia_radial_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_guia_contra_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )

    alerta_caixa_espiral_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=10
    )
    limite_caixa_espiral_ug1 = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    # ug2
    ug2_disp = models.DecimalField(max_digits=10, decimal_places=5, default=1)
    ug2_pot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug2_setpot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug2_sinc = models.IntegerField(default=0)
    ug2_tempo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ug2_prioridade = models.IntegerField(default=0)
    alerta_temperatura_fase_r_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_fase_s_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_fase_t_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_nucleo_estator_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_rad_dia_1_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_rad_dia_2_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_rad_tra_1_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_rad_tra_2_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_saida_de_ar_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_guia_escora_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_guia_radial_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_guia_contra_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    limite_temperatura_fase_r_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_fase_s_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_fase_t_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_nucleo_estator_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_rad_dia_1_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_rad_dia_2_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_rad_tra_1_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_rad_tra_2_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_saida_de_ar_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_guia_escora_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_guia_radial_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_guia_contra_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    alerta_caixa_espiral_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=10
    )
    limite_caixa_espiral_ug2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    # ug3
    ug3_disp = models.DecimalField(max_digits=10, decimal_places=5, default=1)
    ug3_pot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug3_setpot = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    ug3_sinc = models.IntegerField(default=0)
    ug3_tempo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ug3_prioridade = models.IntegerField(default=0)
    alerta_temperatura_fase_r_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_fase_s_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_fase_t_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_nucleo_estator_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_rad_dia_1_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_rad_dia_2_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_rad_tra_1_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_rad_tra_2_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_saida_de_ar_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_guia_escora_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_guia_radial_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    alerta_temperatura_mancal_guia_contra_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=100
    )
    limite_temperatura_fase_r_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_fase_s_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_fase_t_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_nucleo_estator_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_rad_dia_1_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_rad_dia_2_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_rad_tra_1_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_rad_tra_2_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_saida_de_ar_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_guia_escora_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_guia_radial_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )
    limite_temperatura_mancal_guia_contra_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=200
    )

    alerta_caixa_espiral_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=10
    )
    limite_caixa_espiral_ug3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )


class Comando(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    executavel_em_manual = models.BooleanField(default=False)
    executavel_em_autmoatico = models.BooleanField(default=True)
