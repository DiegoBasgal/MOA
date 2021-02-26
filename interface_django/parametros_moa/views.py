from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from parametros_moa.models import ParametrosUsina


# Create your views here.


@login_required
def parametros_moa_view(request, *args, **kwargs):

    usina = ParametrosUsina.objects.get(id=1)
    modo_autonomo_ativado = True if usina.modo_autonomo else False

    if request.method == "POST":
        if request.POST['modo_autonomo_ativado'] == "True":
            modo_autonomo_ativado = True
        if request.POST['modo_autonomo_ativado'] == "False":
            modo_autonomo_ativado = False

        usina.modo_autonomo = 1 if modo_autonomo_ativado else 0

        if int(request.POST['escolha_ugs']) == 0:
            usina.modo_de_escolha_das_ugs = 1
            usina.ug1_prioridade = 0
            usina.ug2_prioridade = 0

        if int(request.POST['escolha_ugs']) == 1:
            usina.modo_de_escolha_das_ugs = 2
            usina.ug1_prioridade = 100
            usina.ug2_prioridade = 0

        if int(request.POST['escolha_ugs']) == 2:
            usina.modo_de_escolha_das_ugs = 2
            usina.ug1_prioridade = 0
            usina.ug2_prioridade = 100


    usina.timestamp = datetime.now()
    usina.save()

    escolha_ugs = 0
    if (usina.modo_de_escolha_das_ugs == 2) and (usina.ug1_prioridade > usina.ug2_prioridade):
        escolha_ugs = 1

    if (usina.modo_de_escolha_das_ugs == 2) and (usina.ug1_prioridade < usina.ug2_prioridade):
        escolha_ugs = 2

    context = {
        'escolha_ugs': escolha_ugs,
        'modo_autonomo_ativado': usina.modo_autonomo,
    }
    return render(request, 'parametros_moa.html', context=context)


def emergencia_view(request, *args, **kwargs):

    usina = ParametrosUsina.objects.get(id=1)
    codigo_emergencia = usina.emergencia_acionada

    if request.method == "POST":
        codigo_emergencia = int(request.POST['codigo_emergencia'])
        usina.emergencia_acionada = codigo_emergencia
        usina.timestamp = datetime.now()
        usina.save()

    context = {
        'estado': codigo_emergencia,
        'descr': "Emergência acionada. (cód.:{})".format(codigo_emergencia) if codigo_emergencia else "Ok",
        'timestamp': usina.timestamp.strftime("%d/%m/%Y, %H:%M:%S")}

    return render(request, 'emergencia.html', context=context)
