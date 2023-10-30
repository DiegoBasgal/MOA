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

        if request.POST.get("escolha_ugs0"):
            usina.modo_de_escolha_das_ugs = 0
            usina.ug1_prioridade = 0
            usina.ug2_prioridade = 0
            usina.ug3_prioridade = 0
            usina.save()

        if request.POST.get("escolha_ugs1"):
            usina.modo_de_escolha_das_ugs = 1
            usina.ug1_prioridade = 100
            usina.ug2_prioridade = 0
            usina.ug3_prioridade = 0
            usina.save()

        if request.POST.get("escolha_ugs2"):
            usina.modo_de_escolha_das_ugs = 2
            usina.ug1_prioridade = 0
            usina.ug2_prioridade = 100
            usina.ug3_prioridade = 0
            usina.save()

        if request.POST.get("escolha_ugs3"):
            usina.modo_de_escolha_das_ugs = 3
            usina.ug1_prioridade = 0
            usina.ug2_prioridade = 0
            usina.ug3_prioridade = 100
            usina.save()

        if request.POST.get("bnv_alvo"):
            nv_alvo = float(request.POST.get("nv_alvo").replace(",", "."))
            usina.nv_alvo = nv_alvo if isinstance(nv_alvo, float) else usina.nv_alvo
            usina.save()

        if request.POST.get("ug1_cx_alvo"):
            ug1_press_cx_alvo = float(request.POST.get("ug1_press_cx_alvo").replace(",", "."))
            usina.ug1_press_cx_alvo = ug1_press_cx_alvo if isinstance(ug1_press_cx_alvo, float) else usina.ug1_press_cx_alvo
            usina.save()

        if request.POST.get("ug2_cx_alvo"):
            ug2_press_cx_alvo = float(request.POST.get("ug2_press_cx_alvo").replace(",", "."))
            usina.ug2_press_cx_alvo = ug2_press_cx_alvo if isinstance(ug2_press_cx_alvo, float) else usina.ug2_press_cx_alvo
            usina.save()

        if request.POST.get("ug3_cx_alvo"):
            ug3_press_cx_alvo = float(request.POST.get("ug3_press_cx_alvo").replace(",", "."))
            usina.ug3_press_cx_alvo = ug3_press_cx_alvo if isinstance(ug3_press_cx_alvo, float) else usina.ug3_press_cx_alvo
            usina.save()


        if request.POST.get("salvar_params"):
            aux = request.POST.get("alerta_temperatura_fase_r_ug1")
            usina.alerta_temperatura_fase_r_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_fase_r_ug1)

            aux = request.POST.get("alerta_temperatura_fase_s_ug1")
            usina.alerta_temperatura_fase_s_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_fase_s_ug1)

            aux = request.POST.get("alerta_temperatura_fase_t_ug1")
            usina.alerta_temperatura_fase_t_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_fase_t_ug1)

            aux = request.POST.get("alerta_temperatura_nucleo_estator_ug1")
            usina.alerta_temperatura_nucleo_estator_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_nucleo_estator_ug1)

            aux = request.POST.get("alerta_temperatura_mancal_rad_dia_1_ug1")
            usina.alerta_temperatura_mancal_rad_dia_1_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_rad_dia_1_ug1)

            aux = request.POST.get("alerta_temperatura_mancal_rad_dia_2_ug1")
            usina.alerta_temperatura_mancal_rad_dia_2_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_rad_dia_2_ug1)

            aux = request.POST.get("alerta_temperatura_mancal_rad_tra_1_ug1")
            usina.alerta_temperatura_mancal_rad_tra_1_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_rad_tra_1_ug1)

            aux = request.POST.get("alerta_temperatura_mancal_rad_tra_2_ug1")
            usina.alerta_temperatura_mancal_rad_tra_2_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_rad_tra_2_ug1)

            aux = request.POST.get("alerta_temperatura_saida_de_ar_ug1")
            usina.alerta_temperatura_saida_de_ar_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_saida_de_ar_ug1)

            aux = request.POST.get("alerta_temperatura_mancal_guia_escora_ug1")
            usina.alerta_temperatura_mancal_guia_escora_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_guia_escora_ug1)

            aux = request.POST.get("alerta_temperatura_mancal_guia_radial_ug1")
            usina.alerta_temperatura_mancal_guia_radial_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_guia_radial_ug1)

            aux = request.POST.get("alerta_temperatura_mancal_guia_contra_ug1")
            usina.alerta_temperatura_mancal_guia_contra_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_guia_contra_ug1)

            aux = request.POST.get("limite_temperatura_fase_r_ug1")
            usina.limite_temperatura_fase_r_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_r_ug1)

            aux = request.POST.get("limite_temperatura_fase_s_ug1")
            usina.limite_temperatura_fase_s_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_s_ug1)

            aux = request.POST.get("limite_temperatura_fase_t_ug1")
            usina.limite_temperatura_fase_t_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_t_ug1)

            aux = request.POST.get("limite_temperatura_nucleo_estator_ug1")
            usina.limite_temperatura_nucleo_estator_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_nucleo_estator_ug1)

            aux = request.POST.get("limite_temperatura_mancal_rad_dia_1_ug1")
            usina.limite_temperatura_mancal_rad_dia_1_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_rad_dia_1_ug1)

            aux = request.POST.get("limite_temperatura_mancal_rad_dia_2_ug1")
            usina.limite_temperatura_mancal_rad_dia_2_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_rad_dia_2_ug1)

            aux = request.POST.get("limite_temperatura_mancal_rad_tra_1_ug1")
            usina.limite_temperatura_mancal_rad_tra_1_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_rad_tra_1_ug1)

            aux = request.POST.get("limite_temperatura_mancal_rad_tra_2_ug1")
            usina.limite_temperatura_mancal_rad_tra_2_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_rad_tra_2_ug1)

            aux = request.POST.get("limite_temperatura_saida_de_ar_ug1")
            usina.limite_temperatura_saida_de_ar_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_saida_de_ar_ug1)

            aux = request.POST.get("limite_temperatura_mancal_guia_escora_ug1")
            usina.limite_temperatura_mancal_guia_escora_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_guia_escora_ug1)

            aux = request.POST.get("limite_temperatura_mancal_guia_radial_ug1")
            usina.limite_temperatura_mancal_guia_radial_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_guia_radial_ug1)

            aux = request.POST.get("limite_temperatura_mancal_guia_contra_ug1")
            usina.limite_temperatura_mancal_guia_contra_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_guia_contra_ug1)

            aux = float(request.POST.get("alerta_caixa_espiral_ug1").replace(",", "."))
            usina.alerta_caixa_espiral_ug1 = aux if isinstance(aux, float) else usina.alerta_caixa_espiral_ug1

            aux = float(request.POST.get("limite_caixa_espiral_ug1").replace(",", "."))
            usina.limite_caixa_espiral_ug1 = aux if isinstance(aux, float) else usina.limite_caixa_espiral_ug1

            aux = request.POST.get("alerta_temperatura_fase_r_ug2")
            usina.alerta_temperatura_fase_r_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_fase_r_ug2)

            aux = request.POST.get("alerta_temperatura_fase_s_ug2")
            usina.alerta_temperatura_fase_s_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_fase_s_ug2)

            aux = request.POST.get("alerta_temperatura_fase_t_ug2")
            usina.alerta_temperatura_fase_t_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_fase_t_ug2)

            aux = request.POST.get("alerta_temperatura_nucleo_estator_ug2")
            usina.alerta_temperatura_nucleo_estator_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_nucleo_estator_ug2)

            aux = request.POST.get("alerta_temperatura_mancal_rad_dia_1_ug2")
            usina.alerta_temperatura_mancal_rad_dia_1_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_rad_dia_1_ug2)

            aux = request.POST.get("alerta_temperatura_mancal_rad_dia_2_ug2")
            usina.alerta_temperatura_mancal_rad_dia_2_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_rad_dia_2_ug2)

            aux = request.POST.get("alerta_temperatura_mancal_rad_tra_1_ug2")
            usina.alerta_temperatura_mancal_rad_tra_1_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_rad_tra_1_ug2)

            aux = request.POST.get("alerta_temperatura_mancal_rad_tra_2_ug2")
            usina.alerta_temperatura_mancal_rad_tra_2_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_rad_tra_2_ug2)

            aux = request.POST.get("alerta_temperatura_saida_de_ar_ug2")
            usina.alerta_temperatura_saida_de_ar_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_saida_de_ar_ug2)

            aux = request.POST.get("alerta_temperatura_mancal_guia_escora_ug2")
            usina.alerta_temperatura_mancal_guia_escora_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_guia_escora_ug2)

            aux = request.POST.get("alerta_temperatura_mancal_guia_radial_ug2")
            usina.alerta_temperatura_mancal_guia_radial_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_guia_radial_ug2)

            aux = request.POST.get("alerta_temperatura_mancal_guia_contra_ug2")
            usina.alerta_temperatura_mancal_guia_contra_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_guia_contra_ug2)

            aux = request.POST.get("limite_temperatura_fase_r_ug2")
            usina.limite_temperatura_fase_r_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_r_ug2)

            aux = request.POST.get("limite_temperatura_fase_s_ug2")
            usina.limite_temperatura_fase_s_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_s_ug2)

            aux = request.POST.get("limite_temperatura_fase_t_ug2")
            usina.limite_temperatura_fase_t_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_t_ug2)

            aux = request.POST.get("limite_temperatura_nucleo_estator_ug2")
            usina.limite_temperatura_nucleo_estator_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_nucleo_estator_ug2)

            aux = request.POST.get("limite_temperatura_mancal_rad_dia_1_ug2")
            usina.limite_temperatura_mancal_rad_dia_1_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_rad_dia_1_ug2)

            aux = request.POST.get("limite_temperatura_mancal_rad_dia_2_ug2")
            usina.limite_temperatura_mancal_rad_dia_2_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_rad_dia_2_ug2)

            aux = request.POST.get("limite_temperatura_mancal_rad_tra_1_ug2")
            usina.limite_temperatura_mancal_rad_tra_1_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_rad_tra_1_ug2)

            aux = request.POST.get("limite_temperatura_mancal_rad_tra_2_ug2")
            usina.limite_temperatura_mancal_rad_tra_2_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_rad_tra_2_ug2)

            aux = request.POST.get("limite_temperatura_saida_de_ar_ug2")
            usina.limite_temperatura_saida_de_ar_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_saida_de_ar_ug2)

            aux = request.POST.get("limite_temperatura_mancal_guia_escora_ug2")
            usina.limite_temperatura_mancal_guia_escora_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_guia_escora_ug2)

            aux = request.POST.get("limite_temperatura_mancal_guia_radial_ug2")
            usina.limite_temperatura_mancal_guia_radial_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_guia_radial_ug2)

            aux = request.POST.get("limite_temperatura_mancal_guia_contra_ug2")
            usina.limite_temperatura_mancal_guia_contra_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_guia_contra_ug2)

            aux = float(request.POST.get("alerta_caixa_espiral_ug2").replace(",", "."))
            usina.alerta_caixa_espiral_ug2 = aux if isinstance(aux, float) else usina.alerta_caixa_espiral_ug2

            aux = float(request.POST.get("limite_caixa_espiral_ug2").replace(",", "."))
            usina.limite_caixa_espiral_ug2 = aux if isinstance(aux, float) else usina.limite_caixa_espiral_ug2

            aux = request.POST.get("alerta_temperatura_fase_r_ug3")
            usina.alerta_temperatura_fase_r_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_fase_r_ug3)

            aux = request.POST.get("alerta_temperatura_fase_s_ug3")
            usina.alerta_temperatura_fase_s_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_fase_s_ug3)

            aux = request.POST.get("alerta_temperatura_fase_t_ug3")
            usina.alerta_temperatura_fase_t_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_fase_t_ug3)

            aux = request.POST.get("alerta_temperatura_nucleo_estator_ug3")
            usina.alerta_temperatura_nucleo_estator_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_nucleo_estator_ug3)

            aux = request.POST.get("alerta_temperatura_mancal_rad_dia_1_ug3")
            usina.alerta_temperatura_mancal_rad_dia_1_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_rad_dia_1_ug3)

            aux = request.POST.get("alerta_temperatura_mancal_rad_dia_2_ug3")
            usina.alerta_temperatura_mancal_rad_dia_2_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_rad_dia_2_ug3)

            aux = request.POST.get("alerta_temperatura_mancal_rad_tra_1_ug3")
            usina.alerta_temperatura_mancal_rad_tra_1_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_rad_tra_1_ug3)

            aux = request.POST.get("alerta_temperatura_mancal_rad_tra_2_ug3")
            usina.alerta_temperatura_mancal_rad_tra_2_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_rad_tra_2_ug3)

            aux = request.POST.get("alerta_temperatura_saida_de_ar_ug3")
            usina.alerta_temperatura_saida_de_ar_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_saida_de_ar_ug3)

            aux = request.POST.get("alerta_temperatura_mancal_guia_escora_ug3")
            usina.alerta_temperatura_mancal_guia_escora_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_guia_escora_ug3)

            aux = request.POST.get("alerta_temperatura_mancal_guia_radial_ug3")
            usina.alerta_temperatura_mancal_guia_radial_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_guia_radial_ug3)

            aux = request.POST.get("alerta_temperatura_mancal_guia_contra_ug3")
            usina.alerta_temperatura_mancal_guia_contra_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_guia_contra_ug3)

            aux = request.POST.get("limite_temperatura_fase_r_ug3")
            usina.limite_temperatura_fase_r_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_r_ug3)

            aux = request.POST.get("limite_temperatura_fase_s_ug3")
            usina.limite_temperatura_fase_s_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_s_ug3)

            aux = request.POST.get("limite_temperatura_fase_t_ug3")
            usina.limite_temperatura_fase_t_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_t_ug3)

            aux = request.POST.get("limite_temperatura_nucleo_estator_ug3")
            usina.limite_temperatura_nucleo_estator_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_nucleo_estator_ug3)

            aux = request.POST.get("limite_temperatura_mancal_rad_dia_1_ug3")
            usina.limite_temperatura_mancal_rad_dia_1_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_rad_dia_1_ug3)

            aux = request.POST.get("limite_temperatura_mancal_rad_dia_2_ug3")
            usina.limite_temperatura_mancal_rad_dia_2_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_rad_dia_2_ug3)

            aux = request.POST.get("limite_temperatura_mancal_rad_tra_1_ug3")
            usina.limite_temperatura_mancal_rad_tra_1_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_rad_tra_1_ug3)

            aux = request.POST.get("limite_temperatura_mancal_rad_tra_2_ug3")
            usina.limite_temperatura_mancal_rad_tra_2_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_rad_tra_2_ug3)

            aux = request.POST.get("limite_temperatura_saida_de_ar_ug3")
            usina.limite_temperatura_saida_de_ar_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_saida_de_ar_ug3)

            aux = request.POST.get("limite_temperatura_mancal_guia_escora_ug3")
            usina.limite_temperatura_mancal_guia_escora_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_guia_escora_ug3)

            aux = request.POST.get("limite_temperatura_mancal_guia_radial_ug3")
            usina.limite_temperatura_mancal_guia_radial_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_guia_radial_ug3)

            aux = request.POST.get("limite_temperatura_mancal_guia_contra_ug3")
            usina.limite_temperatura_mancal_guia_contra_ug3 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_guia_contra_ug3)

            aux = float(request.POST.get("alerta_caixa_espiral_ug3").replace(",", "."))
            usina.alerta_caixa_espiral_ug3 = aux if isinstance(aux, float) else usina.alerta_caixa_espiral_ug3

            aux = float(request.POST.get("limite_caixa_espiral_ug3").replace(",", "."))
            usina.limite_caixa_espiral_ug3 = aux if isinstance(aux, float) else usina.limite_caixa_espiral_ug3

            usina.timestamp = datetime.now()
            usina.save()

    escolha_ugs = 0
    if ((usina.modo_de_escolha_das_ugs == 2)
        and (usina.ug1_prioridade > usina.ug2_prioridade)
        and (usina.ug1_prioridade > usina.ug3_prioridade)):
        escolha_ugs = 1

    if ((usina.modo_de_escolha_das_ugs == 2)
        and (usina.ug2_prioridade > usina.ug1_prioridade)
        and (usina.ug2_prioridade > usina.ug3_prioridade)):
        escolha_ugs = 2

    if ((usina.modo_de_escolha_das_ugs == 2)
        and (usina.ug3_prioridade > usina.ug2_prioridade)
        and (usina.ug3_prioridade > usina.ug1_prioridade)):
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
