from django.contrib import admin

# Register your models here.

from .models import ParametrosUsina
from .models import Contato
from .models import Comando

admin.site.register(ParametrosUsina)
admin.site.register(Contato)
admin.site.register(Comando)
