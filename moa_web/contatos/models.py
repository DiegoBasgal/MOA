from django.db import models

# Create your models here.

class Contato(models.Model):

    nome = models.CharField(max_length=250, default="")
    numero = models.CharField(max_length=20, default="")

    data_inicio = models.DateField(default=0)
    ts_inicio = models.TimeField(default=0)

    data_fim = models.DateField(default=0)
    ts_fim = models.TimeField(default=0)