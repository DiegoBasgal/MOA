"""interface_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from agendamentos.views import agendamentos_view
from agendamentos.views import agendamento_detalhado_view
from agendamentos.views import novo_agendamento_view
from agendamentos.views import novo_agendamento_rapido_view
from monitoramento.views import monitoramento_view
from ocorrencias.views import ocorrencias_view
from parametros_moa.views import parametros_moa_view, emergencia_view, contatos_view, deletar, adicionar, retornar

urlpatterns = [
    path("", RedirectView.as_view(url="parametros_moa/")),
    path("admin/", admin.site.urls),
    path("agendamentos/", agendamentos_view, name="agendamentos"),
    path("agendamentos/<int:ag_id>/",agendamento_detalhado_view,name="agendamento_detalhado",),
    path("agendamentos/novo_agendamento/", novo_agendamento_view, name="novo_agendamento"),
    path("agendamentos/novo_agendamento_rapido/",novo_agendamento_rapido_view,name="novo_agendamento_rapido",),
    path("monitoramento/", monitoramento_view, name="monitoramento"),
    path("ocorrencias/", ocorrencias_view, name="ocorrencias"),
    path("parametros_moa/", parametros_moa_view, name="parametros_moa"),
    path("parametros_moa/emergencia/", emergencia_view, name="emergencia"),
    path("parametros_moa/contatos/", contatos_view, name="contatos"),
    path("parametros_moa/contatos/adicionar/", adicionar, name="adicionar"),
    path("parametros_moa/contatos/deletar/<int:id>", deletar, name="deletar"),
    path("parametros_moa/contatos/adicionar/retornar/", retornar, name="retornar"),
]

# Add Django site authentication urls (for login, logout, password management)

urlpatterns += [
    path("accounts/", include("django.contrib.auth.urls")),
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)