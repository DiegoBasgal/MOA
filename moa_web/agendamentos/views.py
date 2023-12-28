import pytz
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from agendamentos.models import Agendamento
from parametros.models import Comando

# Create your views here.

def agendamentos_view(request, *args, **kwargs):

    agendamentos = []
    agendamentos_executados = []

    res = Agendamento.objects.all()
    for row in res:
        if row.executado:
            agendamentos_executados.append(row)
        else:
            agendamentos.append(row)

    comandos = Comando.objects.all()

    context = {
        "agendamentos": sorted(agendamentos, key=lambda y: y.data),
        "agendamentos_executados": sorted(
            agendamentos_executados, key=lambda y: y.data, reverse=True
        ),
        "comandos": comandos,
    }

    return render(request, "agendamentos.html", context=context)


@login_required
def agendamento_detalhado_view(request, *args, **kwargs):

    if kwargs["ag_id"] is None:
        return HttpResponseRedirect("../")

    ag = Agendamento.objects.get(id=kwargs["ag_id"])
    context = {"ag": ag}

    if request.method == "POST":
        if request.POST.get("acao") == "alterar":
            ag.ts_modificado = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
            ag.modificado_por = str(request.user)
            ag.executado = True
            ag.observacao = (
                ag.observacao + " - MARCADO COMO EXECUTADO PELA INTERFACE WEB"
            )
            ag.save()
            return HttpResponseRedirect("../")

    return render(request, "agendamento_detalhado.html", context=context)


@login_required
def novo_agendamento_view(request, *args, **kwargs):

    now = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    if request.method == "POST":

        ano = int(request.POST.get("ano"))
        mes = int(request.POST.get("mes"))
        dia = int(request.POST.get("dia"))
        hora = int(request.POST.get("hora"))
        minuto = int(request.POST.get("minuto"))
        observacao = request.POST.get("observacao")
        campo_auxiliar = request.POST.get("campo_auxiliar")
        comando_id = request.POST.get("comando")

        data_hora = datetime(ano, mes, dia, hora, minuto, 0)
        if data_hora <= now:
            if (now - data_hora).seconds < 60:
                data_hora = now
            else:
                return HttpResponseRedirect('../')

        ag = Agendamento(
            ts_criado=now,
            criado_por=request.user,
            ts_modificado=now,
            modificado_por=request.user,
            data=data_hora,
            comando=Comando.objects.get(id=comando_id),
            campo_auxiliar=campo_auxiliar,
            observacao=campo_auxiliar if observacao == "" else observacao,
            executado=False,
        )

        ag.save()

        return HttpResponseRedirect("../")

    context = {
        "agora": now,
        "dia": now.day,
        "mes": now.month,
        "ano": now.year,
        "hora": now.hour,
        "minuto": now.minute,
        "prox_minuto": now.minute + 1,
        "range_dias": range(1, 32),
        "range_mes": range(1, 13),
        "range_ano": range(2021, 2026),
        "range_hora": range(24),
        "range_minuto": range(60),
        "range_segundo": range(60),
        "comandos": Comando.objects.all(),
    }

    return render(request, "novo_agendamento.html", context=context)


@login_required
def novo_agendamento_rapido_view(request, *args, **kwargs):

    now = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
    context = {"comandos": Comando.objects.all()}

    if request.method == "POST":

        comando_id = request.POST.get("comando")
        ag = Agendamento(
            ts_criado=now,
            criado_por=request.user,
            ts_modificado=now,
            modificado_por=request.user,
            data=now,
            comando=Comando.objects.get(id=comando_id),
            campo_auxiliar="",
            observacao="Criado pela tela de comando rápido",
            executado=False,
        )
        ag.save()
        return HttpResponseRedirect("../")

    return render(request, "novo_agendamento_rapido.html", context=context)
