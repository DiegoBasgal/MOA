from django.db import models

# Create your models here.

class ComandosManual(models.Model):
   id = models.IntegerField(primary_key=True)
   comando_dj52l = models.BooleanField(default=True)
   modo_ug1 = models.IntegerField(default=1)
   modo_ug2 = models.IntegerField(default=1)