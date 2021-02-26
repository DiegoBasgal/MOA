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
    kp = models.DecimalField(max_digits=30, decimal_places=15)
    ki = models.DecimalField(max_digits=30, decimal_places=15)
    kd = models.DecimalField(max_digits=30, decimal_places=15)
    kie = models.DecimalField(max_digits=30, decimal_places=15)
    margem_pot_critica = models.DecimalField(max_digits=30, decimal_places=15)
    n_movel_L = models.IntegerField()
    n_movel_R = models.IntegerField()
    nv_alvo = models.DecimalField(max_digits=30, decimal_places=15)
    nv_maximo = models.DecimalField(max_digits=30, decimal_places=15)
    nv_minimo = models.DecimalField(max_digits=30, decimal_places=15)
    nv_montante = models.DecimalField(max_digits=30, decimal_places=15)
    nv_religamento = models.DecimalField(max_digits=30, decimal_places=15)
    posicao_comporta = models.IntegerField()
    pot_minima = models.DecimalField(max_digits=30, decimal_places=15)
    pot_nominal = models.DecimalField(max_digits=30, decimal_places=15)
    pot_nominal_ug = models.DecimalField(max_digits=30, decimal_places=15)
    pot_disp = models.DecimalField(max_digits=30, decimal_places=15)
    timer_erro = models.IntegerField()
    ug1_disp = models.DecimalField(max_digits=30, decimal_places=15)
    ug1_pot = models.DecimalField(max_digits=30, decimal_places=15)
    ug1_setpot = models.DecimalField(max_digits=30, decimal_places=15)
    ug1_sinc = models.IntegerField()
    ug1_tempo = models.IntegerField()
    ug1_prioridade = models.IntegerField()
    ug2_disp = models.DecimalField(max_digits=30, decimal_places=15)
    ug2_pot = models.DecimalField(max_digits=30, decimal_places=15)
    ug2_setpot = models.DecimalField(max_digits=30, decimal_places=15)
    ug2_sinc = models.IntegerField()
    ug2_tempo = models.IntegerField()
    ug2_prioridade = models.IntegerField()
    valor_ie_inicial = models.DecimalField(max_digits=30, decimal_places=15)
    modo_de_escolha_das_ugs = models.IntegerField()
    # modo 1 = hora depois prioridade
    # modo 2 = prioridade depois hora

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

