from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from agendamentos.models import Agendamento
from parametros_moa.models import Comando


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

    context = {'agendamentos': sorted(agendamentos, key=lambda y: y.data),
               'agendamentos_executados': sorted(agendamentos_executados, key=lambda y: y.data),
               'comandos': comandos,
               }

    return render(request, 'agendamentos.html', context=context)


@login_required
def agendamento_detalhado_view(request, *args, **kwargs):

    if kwargs['ag_id'] is None:
        return HttpResponseRedirect('../')

    ag = Agendamento.objects.get(id=kwargs['ag_id'])
    context = {'ag': ag}

    if request.method == "POST":
        if request.POST['acao'] == "remover":
            ag.delete()
            return HttpResponseRedirect('../')

    return render(request, 'agendamento_detalhado.html', context=context)


@login_required
def novo_agendamento_view(request, *args, **kwargs):
    if request.method == "POST":

        now = datetime.now()
        
        ano = int(request.POST['ano'])
        mes = int(request.POST['mes'])
        dia = int(request.POST['dia'])
        hora = int(request.POST['hora'])
        minuto = int(request.POST['minuto'])
        data_hora = datetime(ano, mes, dia, hora, minuto, 0)
        if data_hora <= now:
            return HttpResponseRedirect('../')

        observacao = request.POST['observacao']
        comando_id = request.POST['comando']
        ag = Agendamento(data=data_hora, observacao=observacao, comando=Comando.objects.get(id=comando_id))
        ag.save()
        return HttpResponseRedirect('../')

    now = datetime.now()
    context = {'agora': now,
                'dia': now.day,
                'mes': now.month,
                'ano': now.year,
                'hora': now.hour,
                'minuto': now.minute,
                'prox_minuto': now.minute + 1,
                'range_dias': range(1, 32),
                'range_mes': range(1, 13),
                'range_ano': range(2021, 2026),
                'range_hora': range(24),
                'range_minuto': range(60),
                'range_segundo': range(60),
                'comandos': Comando.objects.all()
                }

    return render(request, 'novo_agendamento.html', context=context)
