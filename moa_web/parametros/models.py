from django.db import models

# Create your models here.

class ParametrosUsina(models.Model):

    timestamp = models.DateTimeField(default=0)

    # Params Usina
    modo_autonomo = models.IntegerField(default=1)
    emergencia_acionada = models.IntegerField(default=0)
    aguardando_reservatorio = models.IntegerField(default=0)
    tda_offline = models.IntegerField(default=0)

    # Servidores
    clp_online = models.IntegerField(default=1)
    clp_ug1_ip = models.CharField(max_length=15, default="0.0.0.0")
    clp_ug1_porta = models.IntegerField(default=502)
    clp_sa_ip = models.CharField(max_length=15, default="0.0.0.0")
    clp_sa_porta = models.IntegerField(default=502)
    clp_tda_ip = models.CharField(max_length=15, default="0.0.0.0")
    clp_tda_porta = models.IntegerField(default=502)
    clp_moa_ip = models.CharField(max_length=15, default="0.0.0.0")
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
    pot_minima = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    pot_nominal = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    pot_nominal_ug = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    margem_pot_critica = models.DecimalField(max_digits=10, decimal_places=5, default=0.037)

    # UG1
    ug1_pot = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    ug1_setpot = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    ug1_ultimo_estado = models.IntegerField(default=0)

    alerta_caixa_espiral_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    limite_caixa_espiral_ug1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Comando(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    executavel_em_manual = models.BooleanField(default=False)
    executavel_em_automatico = models.BooleanField(default=True)


class ControleEstados(models.Model):

    ts = models.DateTimeField(primary_key=True, default=0)

    ultimo_estado_ug1 = models.IntegerField(default=0)