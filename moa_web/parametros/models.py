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

    clp_sa_ip = models.CharField(max_length=15, default="0.0.0.0")
    clp_sa_porta = models.IntegerField(default=502)

    clp_tda_ip = models.CharField(max_length=15, default="0.0.0.0")
    clp_tda_porta = models.IntegerField(default=502)

    clp_ug1_ip = models.CharField(max_length=15, default="0.0.0.0")
    clp_ug1_porta = models.IntegerField(default=502)

    clp_ug2_ip = models.CharField(max_length=15, default="0.0.0.0")
    clp_ug2_porta = models.IntegerField(default=502)

    clp_moa_ip = models.CharField(max_length=15, default="0.0.0.0")
    clp_moa_porta = models.IntegerField(default=502)

    rele_se_ip = models.CharField(max_length=15, default="0.0.0.0")
    rele_se_porta = models.IntegerField(default=502)

    # Nível
    nv_alvo = models.DecimalField(max_digits=10, decimal_places=3, default=85.40)
    nv_maximo = models.DecimalField(max_digits=10, decimal_places=3, default=85.50)
    nv_minimo = models.DecimalField(max_digits=10, decimal_places=3, default=85.00)
    nv_montante = models.DecimalField(max_digits=10, decimal_places=3, default=85.40)
    nv_religamento = models.DecimalField(max_digits=10, decimal_places=3, default=85.10)
    alerta_perda_grade = models.DecimalField(max_digits=10, decimal_places=3, default=0.3)
    limite_perda_grade = models.DecimalField(max_digits=10, decimal_places=3, default=0.4)

    # PID IE
    kp = models.DecimalField(max_digits=15, decimal_places=3, default=2)
    ki = models.DecimalField(max_digits=15, decimal_places=3, default=0.1)
    kd = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    kie = models.DecimalField(max_digits=15, decimal_places=3, default=0.1)
    valor_ie_inicial = models.DecimalField(max_digits=10, decimal_places=1, default=0.5)

    # Potência
    pot_minima = models.DecimalField(max_digits=10, decimal_places=2, default=480)
    pot_nominal = models.DecimalField(max_digits=10, decimal_places=2, default=1200)
    pot_nominal_ug = models.DecimalField(max_digits=10, decimal_places=2, default=600)
    margem_pot_critica = models.DecimalField(max_digits=10, decimal_places=5, default=0.0)

    # UG1
    ug1_pot = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    ug1_setpot = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    ug1_prioridade = models.IntegerField(default=0)
    ug1_ultimo_estado = models.IntegerField(default=0)

    alerta_temperatura_fase_a_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_b_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_c_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_rolamento_dianteiro_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_rolamento_traseiro_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_gaxeteiro_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=100)

    limite_temperatura_fase_a_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_fase_b_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_fase_c_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_rolamento_dianteiro_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_rolamento_traseiro_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_gaxeteiro_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=200)

    # UG2
    ug2_pot = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    ug2_setpot = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    ug2_prioridade = models.IntegerField(default=0)
    ug2_ultimo_estado = models.IntegerField(default=0)

    alerta_temperatura_fase_a_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_b_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_fase_c_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_rolamento_dianteiro_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_rolamento_traseiro_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    alerta_temperatura_gaxeteiro_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=100)

    limite_temperatura_fase_a_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_fase_b_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_fase_c_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_rolamento_dianteiro_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_rolamento_traseiro_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    limite_temperatura_gaxeteiro_ug2 = models.DecimalField(max_digits=10, decimal_places=2, default=200)


class Comando(models.Model):

    id = models.IntegerField(primary_key=True)

    nome = models.CharField(max_length=255)
    descricao = models.TextField()

    executavel_em_manual = models.BooleanField(default=False)
    executavel_em_automatico = models.BooleanField(default=True)

class ControleEstados(models.Model):

    ts = models.DateTimeField(default=0)

    ultimo_estado_ug1 = models.IntegerField(default=0)
    ultimo_estado_ug2 = models.IntegerField(default=0)