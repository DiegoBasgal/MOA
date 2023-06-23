from django.db import models

# Create your models here.


class Alarmes(models.Model):

    data = models.DateTimeField(primary_key=True)

    gravidade = models.IntegerField(default=0)

    descricao = models.TextField(default="")