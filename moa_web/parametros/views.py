from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from parametros.models import ParametrosUsina

# Create your views here.

@login_required
def parametros_moa_view(request, *args, **kwargs):

    usina = ParametrosUsina.objects.get(id=1)

    if request.method == "POST":
        if request.POST.get("ativar_ma"):
            usina.modo_autonomo = 1
            usina.save()

        if request.POST.get("desativar_ma"):
            usina.modo_autonomo = 0
            usina.save()

        if request.POST.get("bnv_alvo"):
            nv_alvo = float(request.POST.get("nv_alvo").replace(",", "."))
            usina.nv_alvo = nv_alvo if isinstance(nv_alvo, float) else usina.nv_alvo
            usina.save()

        if request.POST.get("bcx_alvo"):
            press_cx_alvo = float(request.POST.get("press_cx_alvo").replace(",", "."))
            usina.press_cx_alvo = press_cx_alvo if isinstance(press_cx_alvo, float) else usina.press_cx_alvo
            usina.save()

        if request.POST.get("salvar_params"):

            aux = float(request.POST.get("alerta_caixa_espiral_ug1").replace(",", "."))
            usina.alerta_caixa_espiral_ug1 = aux if isinstance(aux, float) else usina.alerta_caixa_espiral_ug1

            aux = float(request.POST.get("limite_caixa_espiral_ug1").replace(",", "."))
            usina.limite_caixa_espiral_ug1 = aux if isinstance(aux, float) else usina.limite_caixa_espiral_ug1

            usina.timestamp = datetime.now()
            usina.save()

    context = {"usina": usina}
    return render(request, "parametros_moa.html", context=context)


@login_required
def emergencia_view(request, *args, **kwargs):

    usina = ParametrosUsina.objects.get(id=1)
    codigo_emergencia = usina.emergencia_acionada

    if request.method == "POST":
        codigo_emergencia = int(request.POST.get("codigo_emergencia"))
        usina.emergencia_acionada = codigo_emergencia
        usina.timestamp = datetime.now()
        usina.save()

    context = {
        "estado": codigo_emergencia,
        "descr": "Emergência acionada. (cód.:{})".format(codigo_emergencia)
        if codigo_emergencia
        else "Ok",
        "timestamp": usina.timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
    }

    return render(request, "emergencia.html", context=context)
