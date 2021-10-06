from django.db import models
from parametros_moa.models import Comando
# Create your models here.


class Agendamento(models.Model):

    executado = models.IntegerField(default=0)
    data = models.DateTimeField()
    observacao = models.TextField()
    comando = models.ForeignKey(Comando, on_delete=models.CASCADE)

