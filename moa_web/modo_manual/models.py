from django.db import models

# Create your models here.

class ModoManual(models.Model):
   id = models.IntegerField(primary_key=True)
   
   partida_ug1 = models.BooleanField(default=False)
   parada_ug1 = models.BooleanField(default=False)
   modo_ug1 = models.IntegerField(default=1)

   comando_dj52l = models.BooleanField(default=True)