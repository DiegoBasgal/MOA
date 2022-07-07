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
            usina.modo_de_escolha_das_ugs = 3
            usina.ug1_prioridade = 0
            usina.ug2_prioridade = 0
            usina.ug3_prioridade = 100

        nv_alvo = float(request.POST.get("nv_alvo").replace(",", "."))
        usina.nv_alvo = nv_alvo if isinstance(nv_alvo, float) else usina.nv_alvo

        """
        aux = float(
            request.POST.get("temperatura_alerta_enrolamento_fase_r_ug1").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_enrolamento_fase_r_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_enrolamento_fase_r_ug1
        )

        aux = float(
            request.POST.get("temperatura_alerta_enrolamento_fase_s_ug1").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_enrolamento_fase_s_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_enrolamento_fase_s_ug1
        )

        aux = float(
            request.POST.get("temperatura_alerta_enrolamento_fase_t_ug1").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_enrolamento_fase_t_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_enrolamento_fase_t_ug1
        )

        aux = float(
            request.POST.get("temperatura_alerta_mancal_la_casquilho_ug1").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_mancal_la_casquilho_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_casquilho_ug1
        )

        aux = float(
            request.POST.get(
                "temperatura_alerta_mancal_la_contra_escora_1_ug1"
            ).replace(",", ".")
        )
        usina.temperatura_alerta_mancal_la_contra_escora_1_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_contra_escora_1_ug1
        )

        aux = float(
            request.POST.get(
                "temperatura_alerta_mancal_la_contra_escora_2_ug1"
            ).replace(",", ".")
        )
        usina.temperatura_alerta_mancal_la_contra_escora_2_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_contra_escora_2_ug1
        )

        aux = float(
            request.POST.get("temperatura_alerta_mancal_la_escora_1_ug1").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_mancal_la_escora_1_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_escora_1_ug1
        )

        aux = float(
            request.POST.get("temperatura_alerta_mancal_la_escora_2_ug1").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_mancal_la_escora_2_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_escora_2_ug1
        )

        aux = float(
            request.POST.get("temperatura_alerta_mancal_lna_casquilho_ug1").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_mancal_lna_casquilho_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_lna_casquilho_ug1
        )

        aux = float(
            request.POST.get("temperatura_limite_enrolamento_fase_r_ug1").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_enrolamento_fase_r_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_enrolamento_fase_r_ug1
        )

        aux = float(
            request.POST.get("temperatura_limite_enrolamento_fase_s_ug1").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_enrolamento_fase_s_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_enrolamento_fase_s_ug1
        )

        aux = float(
            request.POST.get("temperatura_limite_enrolamento_fase_t_ug1").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_enrolamento_fase_t_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_enrolamento_fase_t_ug1
        )

        aux = float(
            request.POST.get("temperatura_limite_mancal_la_casquilho_ug1").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_mancal_la_casquilho_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_casquilho_ug1
        )

        aux = float(
            request.POST.get(
                "temperatura_limite_mancal_la_contra_escora_1_ug1"
            ).replace(",", ".")
        )
        usina.temperatura_limite_mancal_la_contra_escora_1_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_contra_escora_1_ug1
        )

        aux = float(
            request.POST.get(
                "temperatura_limite_mancal_la_contra_escora_2_ug1"
            ).replace(",", ".")
        )
        usina.temperatura_limite_mancal_la_contra_escora_2_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_contra_escora_2_ug1
        )

        aux = float(
            request.POST.get("temperatura_limite_mancal_la_escora_1_ug1").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_mancal_la_escora_1_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_escora_1_ug1
        )

        aux = float(
            request.POST.get("temperatura_limite_mancal_la_escora_2_ug1").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_mancal_la_escora_2_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_escora_2_ug1
        )

        aux = float(
            request.POST.get("temperatura_limite_mancal_lna_casquilho_ug1").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_mancal_lna_casquilho_ug1 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_lna_casquilho_ug1
        )

        aux = float(
            request.POST.get("temperatura_alerta_enrolamento_fase_r_ug2").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_enrolamento_fase_r_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_enrolamento_fase_r_ug2
        )

        aux = float(
            request.POST.get("temperatura_alerta_enrolamento_fase_s_ug2").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_enrolamento_fase_s_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_enrolamento_fase_s_ug2
        )

        aux = float(
            request.POST.get("temperatura_alerta_enrolamento_fase_t_ug2").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_enrolamento_fase_t_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_enrolamento_fase_t_ug2
        )

        aux = float(
            request.POST.get("temperatura_alerta_mancal_la_casquilho_ug2").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_mancal_la_casquilho_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_casquilho_ug2
        )

        aux = float(
            request.POST.get(
                "temperatura_alerta_mancal_la_contra_escora_1_ug2"
            ).replace(",", ".")
        )
        usina.temperatura_alerta_mancal_la_contra_escora_1_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_contra_escora_1_ug2
        )

        aux = float(
            request.POST.get(
                "temperatura_alerta_mancal_la_contra_escora_2_ug2"
            ).replace(",", ".")
        )
        usina.temperatura_alerta_mancal_la_contra_escora_2_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_contra_escora_2_ug2
        )

        aux = float(
            request.POST.get("temperatura_alerta_mancal_la_escora_1_ug2").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_mancal_la_escora_1_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_escora_1_ug2
        )

        aux = float(
            request.POST.get("temperatura_alerta_mancal_la_escora_2_ug2").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_mancal_la_escora_2_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_escora_2_ug2
        )

        aux = float(
            request.POST.get("temperatura_alerta_mancal_lna_casquilho_ug2").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_mancal_lna_casquilho_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_lna_casquilho_ug2
        )

        aux = float(
            request.POST.get("temperatura_limite_enrolamento_fase_r_ug2").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_enrolamento_fase_r_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_enrolamento_fase_r_ug2
        )

        aux = float(
            request.POST.get("temperatura_limite_enrolamento_fase_s_ug2").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_enrolamento_fase_s_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_enrolamento_fase_s_ug2
        )

        aux = float(
            request.POST.get("temperatura_limite_enrolamento_fase_t_ug2").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_enrolamento_fase_t_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_enrolamento_fase_t_ug2
        )

        aux = float(
            request.POST.get("temperatura_limite_mancal_la_casquilho_ug2").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_mancal_la_casquilho_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_casquilho_ug2
        )

        aux = float(
            request.POST.get(
                "temperatura_limite_mancal_la_contra_escora_1_ug2"
            ).replace(",", ".")
        )
        usina.temperatura_limite_mancal_la_contra_escora_1_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_contra_escora_1_ug2
        )

        aux = float(
            request.POST.get(
                "temperatura_limite_mancal_la_contra_escora_2_ug2"
            ).replace(",", ".")
        )
        usina.temperatura_limite_mancal_la_contra_escora_2_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_contra_escora_2_ug2
        )

        aux = float(
            request.POST.get("temperatura_limite_mancal_la_escora_1_ug2").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_mancal_la_escora_1_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_escora_1_ug2
        )

        aux = float(
            request.POST.get("temperatura_limite_mancal_la_escora_2_ug2").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_mancal_la_escora_2_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_escora_2_ug2
        )

        aux = float(
            request.POST.get("temperatura_limite_mancal_lna_casquilho_ug2").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_mancal_lna_casquilho_ug2 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_lna_casquilho_ug2
        )

        aux = float(
            request.POST.get("temperatura_alerta_enrolamento_fase_r_ug3").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_enrolamento_fase_r_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_enrolamento_fase_r_ug3
        )

        aux = float(
            request.POST.get("temperatura_alerta_enrolamento_fase_s_ug3").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_enrolamento_fase_s_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_enrolamento_fase_s_ug3
        )

        aux = float(
            request.POST.get("temperatura_alerta_enrolamento_fase_t_ug3").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_enrolamento_fase_t_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_enrolamento_fase_t_ug3
        )

        aux = float(
            request.POST.get("temperatura_alerta_mancal_la_casquilho_ug3").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_mancal_la_casquilho_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_casquilho_ug3
        )

        aux = float(
            request.POST.get(
                "temperatura_alerta_mancal_la_contra_escora_1_ug3"
            ).replace(",", ".")
        )
        usina.temperatura_alerta_mancal_la_contra_escora_1_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_contra_escora_1_ug3
        )

        aux = float(
            request.POST.get(
                "temperatura_alerta_mancal_la_contra_escora_2_ug3"
            ).replace(",", ".")
        )
        usina.temperatura_alerta_mancal_la_contra_escora_2_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_contra_escora_2_ug3
        )

        aux = float(
            request.POST.get("temperatura_alerta_mancal_la_escora_1_ug3").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_mancal_la_escora_1_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_escora_1_ug3
        )

        aux = float(
            request.POST.get("temperatura_alerta_mancal_la_escora_2_ug3").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_mancal_la_escora_2_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_la_escora_2_ug3
        )

        aux = float(
            request.POST.get("temperatura_alerta_mancal_lna_casquilho_ug3").replace(
                ",", "."
            )
        )
        usina.temperatura_alerta_mancal_lna_casquilho_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_alerta_mancal_lna_casquilho_ug3
        )

        aux = float(
            request.POST.get("temperatura_limite_enrolamento_fase_r_ug3").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_enrolamento_fase_r_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_enrolamento_fase_r_ug3
        )

        aux = float(
            request.POST.get("temperatura_limite_enrolamento_fase_s_ug3").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_enrolamento_fase_s_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_enrolamento_fase_s_ug3
        )

        aux = float(
            request.POST.get("temperatura_limite_enrolamento_fase_t_ug3").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_enrolamento_fase_t_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_enrolamento_fase_t_ug3
        )

        aux = float(
            request.POST.get("temperatura_limite_mancal_la_casquilho_ug3").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_mancal_la_casquilho_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_casquilho_ug3
        )

        aux = float(
            request.POST.get(
                "temperatura_limite_mancal_la_contra_escora_1_ug3"
            ).replace(",", ".")
        )
        usina.temperatura_limite_mancal_la_contra_escora_1_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_contra_escora_1_ug3
        )

        aux = float(
            request.POST.get(
                "temperatura_limite_mancal_la_contra_escora_2_ug3"
            ).replace(",", ".")
        )
        usina.temperatura_limite_mancal_la_contra_escora_2_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_contra_escora_2_ug3
        )

        aux = float(
            request.POST.get("temperatura_limite_mancal_la_escora_1_ug3").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_mancal_la_escora_1_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_escora_1_ug3
        )

        aux = float(
            request.POST.get("temperatura_limite_mancal_la_escora_2_ug3").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_mancal_la_escora_2_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_la_escora_2_ug3
        )

        aux = float(
            request.POST.get("temperatura_limite_mancal_lna_casquilho_ug3").replace(
                ",", "."
            )
        )
        usina.temperatura_limite_mancal_lna_casquilho_ug3 = (
            aux
            if isinstance(aux, float) and aux > 0
            else usina.temperatura_limite_mancal_lna_casquilho_ug3
        )

        ug1_perda_grade_maxima = float(
            request.POST.get("ug1_perda_grade_maxima").replace(",", ".")
        )
        ug1_perda_grade_alerta = float(
            request.POST.get("ug1_perda_grade_alerta").replace(",", ".")
        )
        usina.ug1_perda_grade_alerta = (
            ug1_perda_grade_alerta
            if isinstance(ug1_perda_grade_alerta, float) and ug1_perda_grade_alerta > 0
            else usina.ug1_perda_grade_alerta
        )
        usina.ug1_perda_grade_maxima = (
            ug1_perda_grade_maxima
            if isinstance(ug1_perda_grade_maxima, float) and ug1_perda_grade_maxima > 0
            else usina.ug1_perda_grade_maxima
        )

        ug2_perda_grade_maxima = float(
            request.POST.get("ug2_perda_grade_maxima").replace(",", ".")
        )
        ug2_perda_grade_alerta = float(
            request.POST.get("ug2_perda_grade_alerta").replace(",", ".")
        )
        usina.ug2_perda_grade_alerta = (
            ug2_perda_grade_alerta
            if isinstance(ug2_perda_grade_alerta, float) and ug2_perda_grade_alerta > 0
            else usina.ug2_perda_grade_alerta
        )
        usina.ug2_perda_grade_maxima = (
            ug2_perda_grade_maxima
            if isinstance(ug2_perda_grade_maxima, float) and ug2_perda_grade_maxima > 0
            else usina.ug2_perda_grade_maxima
        )

        ug3_perda_grade_maxima = float(
            request.POST.get("ug3_perda_grade_maxima").replace(",", ".")
        )
        ug3_perda_grade_alerta = float(
            request.POST.get("ug3_perda_grade_alerta").replace(",", ".")
        )
        usina.ug3_perda_grade_alerta = (
            ug3_perda_grade_alerta
            if isinstance(ug3_perda_grade_alerta, float) and ug3_perda_grade_alerta > 0
            else usina.ug3_perda_grade_alerta
        )
        usina.ug3_perda_grade_maxima = (
            ug3_perda_grade_maxima
            if isinstance(ug3_perda_grade_maxima, float) and ug3_perda_grade_maxima > 0
            else usina.ug3_perda_grade_maxima
        )
"""

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
