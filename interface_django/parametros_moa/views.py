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
        if request.POST.get("modo_autonomo_ativado") == "True":
            modo_autonomo_ativado = True
        if request.POST.get("modo_autonomo_ativado") == "False":
            modo_autonomo_ativado = False

        usina.modo_autonomo = 1 if modo_autonomo_ativado else 0

        if int(request.POST.get("escolha_ugs")) == 0:
            usina.modo_de_escolha_das_ugs = 1
            usina.ug1_prioridade = 0
            usina.ug2_prioridade = 0
            usina.ug3_prioridade = 0

        if int(request.POST.get("escolha_ugs")) == 1:
            usina.modo_de_escolha_das_ugs = 2
            usina.ug1_prioridade = 100
            usina.ug2_prioridade = 0
            usina.ug3_prioridade = 0

        if int(request.POST.get("escolha_ugs")) == 2:
            usina.modo_de_escolha_das_ugs = 2
            usina.ug1_prioridade = 0
            usina.ug2_prioridade = 100
            usina.ug3_prioridade = 0

        if int(request.POST.get("escolha_ugs")) == 3:
            usina.modo_de_escolha_das_ugs = 2
            usina.ug1_prioridade = 0
            usina.ug2_prioridade = 0
            usina.ug3_prioridade = 100

        nv_alvo = float(request.POST.get("nv_alvo").replace(",", "."))
        usina.nv_alvo = nv_alvo if isinstance(nv_alvo, float) else usina.nv_alvo

        aux = request.POST.get("alerta_temperatura_fase_r_ug1")
        usina.alerta_temperatura_fase_r_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_fase_r_ug1)

        aux = request.POST.get("alerta_temperatura_fase_s_ug1")
        usina.alerta_temperatura_fase_s_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_fase_s_ug1)

        aux = request.POST.get("alerta_temperatura_fase_t_ug1")
        usina.alerta_temperatura_fase_t_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_fase_t_ug1)

        aux = request.POST.get("alerta_temperatura_nucleo_estator_ug1")
        usina.alerta_temperatura_nucleo_estator_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_nucleo_estator_ug1)

        aux = request.POST.get("alerta_temperatura_mancal_rad_dia_1_ug1")
        usina.alerta_temperatura_mancal_rad_dia_1_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_rad_dia_1_ug1)

        aux = request.POST.get("alerta_temperatura_mancal_rad_dia_2_ug1")
        usina.alerta_temperatura_mancal_rad_dia_2_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_rad_dia_2_ug1)

        aux = request.POST.get("alerta_temperatura_mancal_rad_tra_1_ug1")
        usina.alerta_temperatura_mancal_rad_tra_1_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_rad_tra_1_ug1)

        aux = request.POST.get("alerta_temperatura_mancal_rad_tra_2_ug1")
        usina.alerta_temperatura_mancal_rad_tra_2_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_rad_tra_2_ug1)

        aux = request.POST.get("alerta_temperatura_saida_de_ar_ug1")
        usina.alerta_temperatura_saida_de_ar_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_saida_de_ar_ug1)

        aux = request.POST.get("alerta_temperatura_mancal_guia_escora_ug1")
        usina.alerta_temperatura_mancal_guia_escora_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_guia_escora_ug1)

        aux = request.POST.get("alerta_temperatura_mancal_guia_radial_ug1")
        usina.alerta_temperatura_mancal_guia_radial_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_guia_radial_ug1)

        aux = request.POST.get("alerta_temperatura_mancal_guia_contra_ug1")
        usina.alerta_temperatura_mancal_guia_contra_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_guia_contra_ug1)

        aux = request.POST.get("limite_temperatura_fase_r_ug1")
        usina.limite_temperatura_fase_r_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_fase_r_ug1)

        aux = request.POST.get("limite_temperatura_fase_s_ug1")
        usina.limite_temperatura_fase_s_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_fase_s_ug1)

        aux = request.POST.get("limite_temperatura_fase_t_ug1")
        usina.limite_temperatura_fase_t_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_fase_t_ug1)

        aux = request.POST.get("limite_temperatura_nucleo_estator_ug1")
        usina.limite_temperatura_nucleo_estator_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_nucleo_estator_ug1)

        aux = request.POST.get("limite_temperatura_mancal_rad_dia_1_ug1")
        usina.limite_temperatura_mancal_rad_dia_1_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_rad_dia_1_ug1)

        aux = request.POST.get("limite_temperatura_mancal_rad_dia_2_ug1")
        usina.limite_temperatura_mancal_rad_dia_2_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_rad_dia_2_ug1)

        aux = request.POST.get("limite_temperatura_mancal_rad_tra_1_ug1")
        usina.limite_temperatura_mancal_rad_tra_1_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_rad_tra_1_ug1)

        aux = request.POST.get("limite_temperatura_mancal_rad_tra_2_ug1")
        usina.limite_temperatura_mancal_rad_tra_2_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_rad_tra_2_ug1)

        aux = request.POST.get("limite_temperatura_saida_de_ar_ug1")
        usina.limite_temperatura_saida_de_ar_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_saida_de_ar_ug1)

        aux = request.POST.get("limite_temperatura_mancal_guia_escora_ug1")
        usina.limite_temperatura_mancal_guia_escora_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_guia_escora_ug1)

        aux = request.POST.get("limite_temperatura_mancal_guia_radial_ug1")
        usina.limite_temperatura_mancal_guia_radial_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_guia_radial_ug1)

        aux = request.POST.get("limite_temperatura_mancal_guia_contra_ug1")
        usina.limite_temperatura_mancal_guia_contra_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_guia_contra_ug1)

        aux = request.POST.get("alerta_caixa_espiral_ug1")
        usina.alerta_caixa_espiral_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_caixa_espiral_ug1)

        aux = request.POST.get("limite_caixa_espiral_ug1")
        usina.limite_caixa_espiral_ug1 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_caixa_espiral_ug1)

        aux = request.POST.get("alerta_temperatura_fase_r_ug2")
        usina.alerta_temperatura_fase_r_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_fase_r_ug2)

        aux = request.POST.get("alerta_temperatura_fase_s_ug2")
        usina.alerta_temperatura_fase_s_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_fase_s_ug2)

        aux = request.POST.get("alerta_temperatura_fase_t_ug2")
        usina.alerta_temperatura_fase_t_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_fase_t_ug2)

        aux = request.POST.get("alerta_temperatura_nucleo_estator_ug2")
        usina.alerta_temperatura_nucleo_estator_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_nucleo_estator_ug2)

        aux = request.POST.get("alerta_temperatura_mancal_rad_dia_1_ug2")
        usina.alerta_temperatura_mancal_rad_dia_1_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_rad_dia_1_ug2)

        aux = request.POST.get("alerta_temperatura_mancal_rad_dia_2_ug2")
        usina.alerta_temperatura_mancal_rad_dia_2_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_rad_dia_2_ug2)

        aux = request.POST.get("alerta_temperatura_mancal_rad_tra_1_ug2")
        usina.alerta_temperatura_mancal_rad_tra_1_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_rad_tra_1_ug2)

        aux = request.POST.get("alerta_temperatura_mancal_rad_tra_2_ug2")
        usina.alerta_temperatura_mancal_rad_tra_2_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_rad_tra_2_ug2)

        aux = request.POST.get("alerta_temperatura_saida_de_ar_ug2")
        usina.alerta_temperatura_saida_de_ar_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_saida_de_ar_ug2)

        aux = request.POST.get("alerta_temperatura_mancal_guia_escora_ug2")
        usina.alerta_temperatura_mancal_guia_escora_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_guia_escora_ug2)

        aux = request.POST.get("alerta_temperatura_mancal_guia_radial_ug2")
        usina.alerta_temperatura_mancal_guia_radial_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_guia_radial_ug2)

        aux = request.POST.get("alerta_temperatura_mancal_guia_contra_ug2")
        usina.alerta_temperatura_mancal_guia_contra_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_guia_contra_ug2)

        aux = request.POST.get("limite_temperatura_fase_r_ug2")
        usina.limite_temperatura_fase_r_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_fase_r_ug2)

        aux = request.POST.get("limite_temperatura_fase_s_ug2")
        usina.limite_temperatura_fase_s_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_fase_s_ug2)

        aux = request.POST.get("limite_temperatura_fase_t_ug2")
        usina.limite_temperatura_fase_t_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_fase_t_ug2)

        aux = request.POST.get("limite_temperatura_nucleo_estator_ug2")
        usina.limite_temperatura_nucleo_estator_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_nucleo_estator_ug2)

        aux = request.POST.get("limite_temperatura_mancal_rad_dia_1_ug2")
        usina.limite_temperatura_mancal_rad_dia_1_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_rad_dia_1_ug2)

        aux = request.POST.get("limite_temperatura_mancal_rad_dia_2_ug2")
        usina.limite_temperatura_mancal_rad_dia_2_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_rad_dia_2_ug2)

        aux = request.POST.get("limite_temperatura_mancal_rad_tra_1_ug2")
        usina.limite_temperatura_mancal_rad_tra_1_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_rad_tra_1_ug2)

        aux = request.POST.get("limite_temperatura_mancal_rad_tra_2_ug2")
        usina.limite_temperatura_mancal_rad_tra_2_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_rad_tra_2_ug2)

        aux = request.POST.get("limite_temperatura_saida_de_ar_ug2")
        usina.limite_temperatura_saida_de_ar_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_saida_de_ar_ug2)

        aux = request.POST.get("limite_temperatura_mancal_guia_escora_ug2")
        usina.limite_temperatura_mancal_guia_escora_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_guia_escora_ug2)

        aux = request.POST.get("limite_temperatura_mancal_guia_radial_ug2")
        usina.limite_temperatura_mancal_guia_radial_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_guia_radial_ug2)

        aux = request.POST.get("limite_temperatura_mancal_guia_contra_ug2")
        usina.limite_temperatura_mancal_guia_contra_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_guia_contra_ug2)

        aux = request.POST.get("alerta_caixa_espiral_ug2")
        usina.alerta_caixa_espiral_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_caixa_espiral_ug2)

        aux = request.POST.get("limite_caixa_espiral_ug2")
        usina.limite_caixa_espiral_ug2 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_caixa_espiral_ug2)

        aux = request.POST.get("alerta_temperatura_fase_r_ug3")
        usina.alerta_temperatura_fase_r_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_fase_r_ug3)

        aux = request.POST.get("alerta_temperatura_fase_s_ug3")
        usina.alerta_temperatura_fase_s_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_fase_s_ug3)

        aux = request.POST.get("alerta_temperatura_fase_t_ug3")
        usina.alerta_temperatura_fase_t_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_fase_t_ug3)

        aux = request.POST.get("alerta_temperatura_nucleo_estator_ug3")
        usina.alerta_temperatura_nucleo_estator_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_nucleo_estator_ug3)

        aux = request.POST.get("alerta_temperatura_mancal_rad_dia_1_ug3")
        usina.alerta_temperatura_mancal_rad_dia_1_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_rad_dia_1_ug3)

        aux = request.POST.get("alerta_temperatura_mancal_rad_dia_2_ug3")
        usina.alerta_temperatura_mancal_rad_dia_2_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_rad_dia_2_ug3)

        aux = request.POST.get("alerta_temperatura_mancal_rad_tra_1_ug3")
        usina.alerta_temperatura_mancal_rad_tra_1_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_rad_tra_1_ug3)

        aux = request.POST.get("alerta_temperatura_mancal_rad_tra_2_ug3")
        usina.alerta_temperatura_mancal_rad_tra_2_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_rad_tra_2_ug3)

        aux = request.POST.get("alerta_temperatura_saida_de_ar_ug3")
        usina.alerta_temperatura_saida_de_ar_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_saida_de_ar_ug3)

        aux = request.POST.get("alerta_temperatura_mancal_guia_escora_ug3")
        usina.alerta_temperatura_mancal_guia_escora_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_guia_escora_ug3)

        aux = request.POST.get("alerta_temperatura_mancal_guia_radial_ug3")
        usina.alerta_temperatura_mancal_guia_radial_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_guia_radial_ug3)

        aux = request.POST.get("alerta_temperatura_mancal_guia_contra_ug3")
        usina.alerta_temperatura_mancal_guia_contra_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_temperatura_mancal_guia_contra_ug3)

        aux = request.POST.get("limite_temperatura_fase_r_ug3")
        usina.limite_temperatura_fase_r_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_fase_r_ug3)

        aux = request.POST.get("limite_temperatura_fase_s_ug3")
        usina.limite_temperatura_fase_s_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_fase_s_ug3)

        aux = request.POST.get("limite_temperatura_fase_t_ug3")
        usina.limite_temperatura_fase_t_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_fase_t_ug3)

        aux = request.POST.get("limite_temperatura_nucleo_estator_ug3")
        usina.limite_temperatura_nucleo_estator_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_nucleo_estator_ug3)

        aux = request.POST.get("limite_temperatura_mancal_rad_dia_1_ug3")
        usina.limite_temperatura_mancal_rad_dia_1_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_rad_dia_1_ug3)

        aux = request.POST.get("limite_temperatura_mancal_rad_dia_2_ug3")
        usina.limite_temperatura_mancal_rad_dia_2_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_rad_dia_2_ug3)

        aux = request.POST.get("limite_temperatura_mancal_rad_tra_1_ug3")
        usina.limite_temperatura_mancal_rad_tra_1_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_rad_tra_1_ug3)

        aux = request.POST.get("limite_temperatura_mancal_rad_tra_2_ug3")
        usina.limite_temperatura_mancal_rad_tra_2_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_rad_tra_2_ug3)

        aux = request.POST.get("limite_temperatura_saida_de_ar_ug3")
        usina.limite_temperatura_saida_de_ar_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_saida_de_ar_ug3)

        aux = request.POST.get("limite_temperatura_mancal_guia_escora_ug3")
        usina.limite_temperatura_mancal_guia_escora_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_guia_escora_ug3)

        aux = request.POST.get("limite_temperatura_mancal_guia_radial_ug3")
        usina.limite_temperatura_mancal_guia_radial_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_guia_radial_ug3)

        aux = request.POST.get("limite_temperatura_mancal_guia_contra_ug3")
        usina.limite_temperatura_mancal_guia_contra_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_temperatura_mancal_guia_contra_ug3)

        aux = request.POST.get("alerta_caixa_espiral_ug3")
        usina.alerta_caixa_espiral_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.alerta_caixa_espiral_ug3)

        aux = request.POST.get("limite_caixa_espiral_ug3")
        usina.limite_caixa_espiral_ug3 = (float(aux.replace(",", ".")) if aux is not None and aux > 0 else usina.limite_caixa_espiral_ug3)


        usina.timestamp = datetime.now()
        usina.save()

    escolha_ugs = 0
    if (
        (usina.modo_de_escolha_das_ugs == 2)
        and (usina.ug1_prioridade > usina.ug2_prioridade)
        and (usina.ug1_prioridade > usina.ug3_prioridade)
    ):
        escolha_ugs = 1

    if (
        (usina.modo_de_escolha_das_ugs == 2)
        and (usina.ug2_prioridade > usina.ug1_prioridade)
        and (usina.ug2_prioridade > usina.ug3_prioridade)
    ):
        escolha_ugs = 2

    if (
        (usina.modo_de_escolha_das_ugs == 2)
        and (usina.ug3_prioridade > usina.ug2_prioridade)
        and (usina.ug3_prioridade > usina.ug1_prioridade)
    ):
        escolha_ugs = 3

    context = {"escolha_ugs": escolha_ugs, "usina": usina}
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
