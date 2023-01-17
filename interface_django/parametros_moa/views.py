from datetime import datetime
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from parametros_moa.models import ParametrosUsina, Contato


# Create your views here.


@login_required
def parametros_moa_view(request, *args, **kwargs):

    usina = ParametrosUsina.objects.get(id=1)
    modo_autonomo_ativado = True if usina.modo_autonomo else False

    if request.method == "POST":
        if request.POST.get('modo_autonomo_ativado') == "True":
            modo_autonomo_ativado = True
        if request.POST.get('modo_autonomo_ativado') == "False":
            modo_autonomo_ativado = False

        usina.modo_autonomo = 1 if modo_autonomo_ativado else 0

        if int(request.POST.get('escolha_ugs')) == 0:
            usina.modo_de_escolha_das_ugs = 1
            usina.ug1_prioridade = 0
            usina.ug2_prioridade = 0

        if int(request.POST.get('escolha_ugs')) == 1:
            usina.modo_de_escolha_das_ugs = 2
            usina.ug1_prioridade = 100
            usina.ug2_prioridade = 0

        if int(request.POST.get('escolha_ugs')) == 2:
            usina.modo_de_escolha_das_ugs = 2
            usina.ug1_prioridade = 0
            usina.ug2_prioridade = 100

        nv_alvo = float(request.POST.get('nv_alvo').replace(",", "."))
        usina.nv_alvo = nv_alvo if isinstance(nv_alvo, float) else usina.nv_alvo
        
        nv_p1_ant = float(request.POST.get('nv_p1_ant').replace(",", "."))
        nv_p2_ant = float(request.POST.get('nv_p2_ant').replace(",", "."))
        nv_p3_ant = float(request.POST.get('nv_p3_ant').replace(",", "."))
        nv_p4_ant = float(request.POST.get('nv_p4_ant').replace(",", "."))
        nv_p5_ant = float(request.POST.get('nv_p5_ant').replace(",", "."))
        usina.nv_comporta_pos_1_ant = nv_p1_ant if isinstance(nv_p1_ant, float) and nv_p1_ant > 0 else usina.nv_comporta_pos_1_ant
        usina.nv_comporta_pos_2_ant = nv_p2_ant if isinstance(nv_p2_ant, float) and nv_p2_ant > 0 else usina.nv_comporta_pos_2_ant
        usina.nv_comporta_pos_3_ant = nv_p3_ant if isinstance(nv_p3_ant, float) and nv_p3_ant > 0 else usina.nv_comporta_pos_3_ant
        usina.nv_comporta_pos_4_ant = nv_p4_ant if isinstance(nv_p4_ant, float) and nv_p4_ant > 0 else usina.nv_comporta_pos_4_ant
        usina.nv_comporta_pos_5_ant = nv_p5_ant if isinstance(nv_p5_ant, float) and nv_p5_ant > 0 else usina.nv_comporta_pos_5_ant

        nv_p0_prox = float(request.POST.get('nv_p0_prox').replace(",", "."))
        nv_p1_prox = float(request.POST.get('nv_p1_prox').replace(",", "."))
        nv_p2_prox = float(request.POST.get('nv_p2_prox').replace(",", "."))
        nv_p3_prox = float(request.POST.get('nv_p3_prox').replace(",", "."))
        nv_p4_prox = float(request.POST.get('nv_p4_prox').replace(",", "."))
        usina.nv_comporta_pos_0_prox = nv_p0_prox if isinstance(nv_p0_prox, float) and nv_p0_prox > 0 else usina.nv_comporta_pos_0_prox
        usina.nv_comporta_pos_1_prox = nv_p1_prox if isinstance(nv_p1_prox, float) and nv_p1_prox > 0 else usina.nv_comporta_pos_1_prox
        usina.nv_comporta_pos_2_prox = nv_p2_prox if isinstance(nv_p2_prox, float) and nv_p2_prox > 0 else usina.nv_comporta_pos_2_prox
        usina.nv_comporta_pos_3_prox = nv_p3_prox if isinstance(nv_p3_prox, float) and nv_p3_prox > 0 else usina.nv_comporta_pos_3_prox
        usina.nv_comporta_pos_4_prox = nv_p4_prox if isinstance(nv_p4_prox, float) and nv_p4_prox > 0 else usina.nv_comporta_pos_4_prox


        aux = float(request.POST.get('temperatura_alerta_enrolamento_fase_r_ug1').replace(",", "."))
        usina.temperatura_alerta_enrolamento_fase_r_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_enrolamento_fase_r_ug1
        
        aux = float(request.POST.get('temperatura_alerta_enrolamento_fase_s_ug1').replace(",", "."))
        usina.temperatura_alerta_enrolamento_fase_s_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_enrolamento_fase_s_ug1
        
        aux = float(request.POST.get('temperatura_alerta_enrolamento_fase_t_ug1').replace(",", "."))
        usina.temperatura_alerta_enrolamento_fase_t_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_enrolamento_fase_t_ug1
        
        aux = float(request.POST.get('temperatura_alerta_mancal_la_casquilho_ug1').replace(",", "."))
        usina.temperatura_alerta_mancal_la_casquilho_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_mancal_la_casquilho_ug1
        
        aux = float(request.POST.get('temperatura_alerta_mancal_la_contra_escora_1_ug1').replace(",", "."))
        usina.temperatura_alerta_mancal_la_contra_escora_1_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_mancal_la_contra_escora_1_ug1
        
        aux = float(request.POST.get('temperatura_alerta_mancal_la_contra_escora_2_ug1').replace(",", "."))
        usina.temperatura_alerta_mancal_la_contra_escora_2_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_mancal_la_contra_escora_2_ug1
        
        aux = float(request.POST.get('temperatura_alerta_mancal_la_escora_1_ug1').replace(",", "."))
        usina.temperatura_alerta_mancal_la_escora_1_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_mancal_la_escora_1_ug1
        
        aux = float(request.POST.get('temperatura_alerta_mancal_la_escora_2_ug1').replace(",", "."))
        usina.temperatura_alerta_mancal_la_escora_2_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_mancal_la_escora_2_ug1
        
        aux = float(request.POST.get('temperatura_alerta_mancal_lna_casquilho_ug1').replace(",", "."))
        usina.temperatura_alerta_mancal_lna_casquilho_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_mancal_lna_casquilho_ug1
        
        aux = float(request.POST.get('temperatura_limite_enrolamento_fase_r_ug1').replace(",", "."))
        usina.temperatura_limite_enrolamento_fase_r_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_enrolamento_fase_r_ug1
        
        aux = float(request.POST.get('temperatura_limite_enrolamento_fase_s_ug1').replace(",", "."))
        usina.temperatura_limite_enrolamento_fase_s_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_enrolamento_fase_s_ug1
        
        aux = float(request.POST.get('temperatura_limite_enrolamento_fase_t_ug1').replace(",", "."))
        usina.temperatura_limite_enrolamento_fase_t_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_enrolamento_fase_t_ug1
        
        aux = float(request.POST.get('temperatura_limite_mancal_la_casquilho_ug1').replace(",", "."))
        usina.temperatura_limite_mancal_la_casquilho_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_mancal_la_casquilho_ug1
        
        aux = float(request.POST.get('temperatura_limite_mancal_la_contra_escora_1_ug1').replace(",", "."))
        usina.temperatura_limite_mancal_la_contra_escora_1_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_mancal_la_contra_escora_1_ug1
        
        aux = float(request.POST.get('temperatura_limite_mancal_la_contra_escora_2_ug1').replace(",", "."))
        usina.temperatura_limite_mancal_la_contra_escora_2_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_mancal_la_contra_escora_2_ug1
        
        aux = float(request.POST.get('temperatura_limite_mancal_la_escora_1_ug1').replace(",", "."))
        usina.temperatura_limite_mancal_la_escora_1_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_mancal_la_escora_1_ug1
        
        aux = float(request.POST.get('temperatura_limite_mancal_la_escora_2_ug1').replace(",", "."))
        usina.temperatura_limite_mancal_la_escora_2_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_mancal_la_escora_2_ug1
        
        aux = float(request.POST.get('temperatura_limite_mancal_lna_casquilho_ug1').replace(",", "."))
        usina.temperatura_limite_mancal_lna_casquilho_ug1 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_mancal_lna_casquilho_ug1
 
        aux = float(request.POST.get('temperatura_alerta_enrolamento_fase_r_ug2').replace(",", "."))
        usina.temperatura_alerta_enrolamento_fase_r_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_enrolamento_fase_r_ug2
        
        aux = float(request.POST.get('temperatura_alerta_enrolamento_fase_s_ug2').replace(",", "."))
        usina.temperatura_alerta_enrolamento_fase_s_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_enrolamento_fase_s_ug2
        
        aux = float(request.POST.get('temperatura_alerta_enrolamento_fase_t_ug2').replace(",", "."))
        usina.temperatura_alerta_enrolamento_fase_t_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_enrolamento_fase_t_ug2
        
        aux = float(request.POST.get('temperatura_alerta_mancal_la_casquilho_ug2').replace(",", "."))
        usina.temperatura_alerta_mancal_la_casquilho_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_mancal_la_casquilho_ug2
        
        aux = float(request.POST.get('temperatura_alerta_mancal_la_contra_escora_1_ug2').replace(",", "."))
        usina.temperatura_alerta_mancal_la_contra_escora_1_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_mancal_la_contra_escora_1_ug2
        
        aux = float(request.POST.get('temperatura_alerta_mancal_la_contra_escora_2_ug2').replace(",", "."))
        usina.temperatura_alerta_mancal_la_contra_escora_2_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_mancal_la_contra_escora_2_ug2
        
        aux = float(request.POST.get('temperatura_alerta_mancal_la_escora_1_ug2').replace(",", "."))
        usina.temperatura_alerta_mancal_la_escora_1_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_mancal_la_escora_1_ug2
        
        aux = float(request.POST.get('temperatura_alerta_mancal_la_escora_2_ug2').replace(",", "."))
        usina.temperatura_alerta_mancal_la_escora_2_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_mancal_la_escora_2_ug2
        
        aux = float(request.POST.get('temperatura_alerta_mancal_lna_casquilho_ug2').replace(",", "."))
        usina.temperatura_alerta_mancal_lna_casquilho_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_alerta_mancal_lna_casquilho_ug2
        
        aux = float(request.POST.get('temperatura_limite_enrolamento_fase_r_ug2').replace(",", "."))
        usina.temperatura_limite_enrolamento_fase_r_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_enrolamento_fase_r_ug2
        
        aux = float(request.POST.get('temperatura_limite_enrolamento_fase_s_ug2').replace(",", "."))
        usina.temperatura_limite_enrolamento_fase_s_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_enrolamento_fase_s_ug2
        
        aux = float(request.POST.get('temperatura_limite_enrolamento_fase_t_ug2').replace(",", "."))
        usina.temperatura_limite_enrolamento_fase_t_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_enrolamento_fase_t_ug2
        
        aux = float(request.POST.get('temperatura_limite_mancal_la_casquilho_ug2').replace(",", "."))
        usina.temperatura_limite_mancal_la_casquilho_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_mancal_la_casquilho_ug2
        
        aux = float(request.POST.get('temperatura_limite_mancal_la_contra_escora_1_ug2').replace(",", "."))
        usina.temperatura_limite_mancal_la_contra_escora_1_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_mancal_la_contra_escora_1_ug2
        
        aux = float(request.POST.get('temperatura_limite_mancal_la_contra_escora_2_ug2').replace(",", "."))
        usina.temperatura_limite_mancal_la_contra_escora_2_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_mancal_la_contra_escora_2_ug2
        
        aux = float(request.POST.get('temperatura_limite_mancal_la_escora_1_ug2').replace(",", "."))
        usina.temperatura_limite_mancal_la_escora_1_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_mancal_la_escora_1_ug2
        
        aux = float(request.POST.get('temperatura_limite_mancal_la_escora_2_ug2').replace(",", "."))
        usina.temperatura_limite_mancal_la_escora_2_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_mancal_la_escora_2_ug2
        
        aux = float(request.POST.get('temperatura_limite_mancal_lna_casquilho_ug2').replace(",", "."))
        usina.temperatura_limite_mancal_lna_casquilho_ug2 = aux if isinstance(aux, float) and aux > 0 else usina.temperatura_limite_mancal_lna_casquilho_ug2
 
 
        ug1_perda_grade_maxima = float(request.POST.get('ug1_perda_grade_maxima').replace(",", "."))
        ug1_perda_grade_alerta = float(request.POST.get('ug1_perda_grade_alerta').replace(",", "."))
        usina.ug1_perda_grade_alerta = ug1_perda_grade_alerta if isinstance(ug1_perda_grade_alerta, float) and ug1_perda_grade_alerta > 0 else usina.ug1_perda_grade_alerta
        usina.ug1_perda_grade_maxima = ug1_perda_grade_maxima if isinstance(ug1_perda_grade_maxima, float) and ug1_perda_grade_maxima > 0 else usina.ug1_perda_grade_maxima

        ug2_perda_grade_maxima = float(request.POST.get('ug2_perda_grade_maxima').replace(",", "."))
        ug2_perda_grade_alerta = float(request.POST.get('ug2_perda_grade_alerta').replace(",", "."))
        usina.ug2_perda_grade_alerta = ug2_perda_grade_alerta if isinstance(ug2_perda_grade_alerta, float) and ug2_perda_grade_alerta > 0 else usina.ug2_perda_grade_alerta
        usina.ug2_perda_grade_maxima = ug2_perda_grade_maxima if isinstance(ug2_perda_grade_maxima, float) and ug2_perda_grade_maxima > 0 else usina.ug2_perda_grade_maxima

        usina.timestamp = datetime.now()
        usina.save()

    escolha_ugs = 0
    if (usina.modo_de_escolha_das_ugs == 2) and (usina.ug1_prioridade > usina.ug2_prioridade):
        escolha_ugs = 1

    if (usina.modo_de_escolha_das_ugs == 2) and (usina.ug1_prioridade < usina.ug2_prioridade):
        escolha_ugs = 2

    context = {
        'escolha_ugs': escolha_ugs,
        'usina': usina

    }
    return render(request, 'parametros_moa.html', context=context)

@login_required
def emergencia_view(request, *args, **kwargs):

    usina = ParametrosUsina.objects.get(id=1)
    codigo_emergencia = usina.emergencia_acionada

    if request.method == "POST":
        codigo_emergencia = int(request.POST.get('codigo_emergencia'))
        usina.emergencia_acionada = codigo_emergencia
        usina.timestamp = datetime.now()
        usina.save()

    context = {
        'estado': codigo_emergencia,
        'descr': "Emergência acionada. (cód.:{})".format(codigo_emergencia) if codigo_emergencia else "Ok",
        'timestamp': usina.timestamp.strftime("%d/%m/%Y, %H:%M:%S")}

    return render(request, 'emergencia.html', context=context)

@login_required
def contatos_view(request, *args, **kwargs):
    contato = Contato.objects.all()
    context = {"contato": contato}
    return render(request, "contatos.html", context=context)

@login_required
def retornar(request, *args, **kwargs):
    return HttpResponseRedirect(reverse('contatos'))

@login_required
def adicionar(request, *args, **kwargs):

    if request.method=='POST':
        try:
            ctt_nome = request.POST.get("nome") 
            ctt_numero = request.POST.get("numero").replace("(", "").replace(")", "")
            ctt_dt_inicio = request.POST.get("data_inicio")
            ctt_ts_inicio = request.POST.get("ts_inicio")
            ctt_dt_fim = request.POST.get("data_fim")
            ctt_ts_fim = request.POST.get("ts_fim")

            contato = Contato.objects.create(nome=ctt_nome, numero=ctt_numero, data_inicio=ctt_dt_inicio, ts_inicio=ctt_ts_inicio, data_fim=ctt_dt_fim, ts_fim=ctt_ts_fim)

        except Exception as e:
            return render(request, 'erro.html', {'mensagem': e})

    return HttpResponseRedirect(reverse('contatos'))

@login_required
def deletar(request, id,*args, **kwargs):
    contato = Contato.objects.filter(id=id)
    contato.delete()
    return HttpResponseRedirect(reverse('contatos'))
