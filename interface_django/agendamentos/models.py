from django.db import models
from parametros_moa.models import Comando

# Create your models here.


class Agendamento(models.Model):

    ts_criado = models.DateTimeField()
    criado_por = models.CharField(max_length=255)
    ts_modificado = models.DateTimeField()
    modificado_por = models.CharField(max_length=255)
    data = models.DateTimeField()
    comando = models.ForeignKey(Comando, on_delete=models.CASCADE)
    campo_auxiliar = models.TextField()
    observacao = models.TextField()
    executado = models.IntegerField(default=0)
