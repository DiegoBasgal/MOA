from django.db import models

# Create your models here.

class ComandosManual(models.Model):
   id = models.IntegerField(primary_key=True)
   
   partida_ug1 = models.BooleanField(default=False)
   parada_ug1 = models.BooleanField(default=False)
   modo_ug1 = models.IntegerField(default=1)

   partida_ug2 = models.BooleanField(default=False)
   parada_ug2 = models.BooleanField(default=False)
   modo_ug2 = models.IntegerField(default=1)

   comando_dj52l = models.BooleanField(default=True)

   modo_comporta_1 = models.IntegerField(default=0)
   
   modo_comporta_2 = models.IntegerField(default=0)