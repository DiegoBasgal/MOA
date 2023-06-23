"""
URL configuration for moa_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from alarmes.views import alarmes_view
from ocorrencias.views import ocorrencias_view
from monitoramento.views import monitoramento_view
from parametros.views import parametros_moa_view, emergencia_view
from contatos.views import contatos_view, adicionar, deletar, retornar
from agendamentos.views import agendamentos_view, novo_agendamento_view, novo_agendamento_rapido_view, agendamento_detalhado_view
from modo_manual.views import comandos_manual_view, comando_dj52l , confirma_comando_dj, comando_ug1, comando_ug2, comando_ug3, comando_impedido

urlpatterns = [
    path("", RedirectView.as_view(url="monitoramento/")),
    path("admin/", admin.site.urls),
    path("alarmes/", alarmes_view, name="alarmes"),
    path("ocorrencias/", ocorrencias_view, name="ocorrencias"),
    path("monitoramento/", monitoramento_view, name="monitoramento"),

    path("agendamentos/", agendamentos_view, name="agendamentos"),
    path("agendamentos/<int:ag_id>/",agendamento_detalhado_view,name="agendamento_detalhado",),
    path("agendamentos/novo_agendamento/", novo_agendamento_view, name="novo_agendamento"),
    path("agendamentos/novo_agendamento_rapido/",novo_agendamento_rapido_view,name="novo_agendamento_rapido",),

    path("parametros_moa/", parametros_moa_view, name="parametros_moa"),
    path("parametros_moa/emergencia/", emergencia_view, name="emergencia"),

    path("contatos/", contatos_view, name="contatos"),
    path("contatos/adicionar/", adicionar, name="adicionar"),
    path("contatos/deletar/<int:id>", deletar, name="deletar"),
    path("contatos/adicionar/retornar/", retornar, name="retornar"),

    path("modo_manual/", comandos_manual_view, name="comandos_manual"),
    path("modo_manual/disjuntor/", comando_dj52l, name="comandos_disjuntor"),
    path("modo_manual/disjuntor/confirmar/", confirma_comando_dj, name="confirma_comando_dj"),
    path("modo_manual/ug1/", comando_ug1, name="comandos_ug1"),
    path("modo_manual/ug2/", comando_ug2, name="comandos_ug2"),
    path("modo_manual/ug3/", comando_ug3, name="comandos_ug3"),
    path("modo_manual/impedido/", comando_impedido, name="comando_impedido"),
]

# Add Django site authentication urls (for login, logout, password management)

urlpatterns += [
    path("accounts/", include("django.contrib.auth.urls")),
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)