from django.db import models
from parametros.models import Comando

# Create your models here.

class Agendamento(models.Model):
    
    id = models.IntegerField(primary_key=True)
    data = models.DateTimeField()
    observacao = models.TextField()
    comando = models.ForeignKey(Comando, on_delete=models.CASCADE)
    executado = models.IntegerField(default=0)
    campo_auxiliar = models.TextField()
    criado_por = models.CharField(max_length=255)
    modificado_por = models.CharField(max_length=255)
    ts_criado = models.DateTimeField()
    ts_modificado = models.DateTimeField()