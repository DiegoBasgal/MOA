from django.db import models

# Create your models here.


class Alarmes(models.Model):

    id = models.IntegerField(primary_key=True, default=0)

    data = models.DateTimeField(default="")

    gravidade = models.IntegerField(default=0)

    descricao = models.TextField(default="")

    autor = models.TextField(default="")