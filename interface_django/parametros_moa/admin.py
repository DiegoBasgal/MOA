from django.contrib import admin

# Register your models here.

from .models import ParametrosUsina
from .models import Contato

admin.site.register(ParametrosUsina)
admin.site.register(Contato)