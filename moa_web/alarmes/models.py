from django.db import models

# Create your models here.


class Alarmes(models.Model):

    ts = models.IntegerField(primary_key=True,default=0, max_length=11)

    gravidade = models.IntegerField(default=0)

    descricao = models.TextField(default="")