from datetime import datetime
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from parametros_moa.models import ParametrosUsina, Contato

# Create your views here.

@login_required
def parametros_moa_view(request, *args, **kwargs):
    contato = Contato.objects.all()
    usina = ParametrosUsina.objects.get(id=1)
    
    if request.method == "POST":
        if request.POST.get("ativar_ma"):
            usina.modo_autonomo = 1
            usina.save()
        if request.POST.get("desativar_ma"):
            usina.modo_autonomo = 0
            usina.save()

        if request.POST.get("escolha_ugs0"):
            usina.modo_de_escolha_das_ugs = 1
            usina.ug1_prioridade = 0
            usina.ug2_prioridade = 0
            usina.save()

        if request.POST.get("escolha_ugs1"):
            usina.modo_de_escolha_das_ugs = 2
            usina.ug1_prioridade = 100
            usina.ug2_prioridade = 0
            usina.save()

        if request.POST.get("escolha_ugs2"):
            usina.modo_de_escolha_das_ugs = 2
            usina.ug1_prioridade = 0
            usina.ug2_prioridade = 100
            usina.save()

        if request.POST.get("bnv_alvo"):
            nv_alvo = float(request.POST.get("nv_alvo").replace(',', '.'))
            usina.nv_alvo = nv_alvo if isinstance(nv_alvo, float) else usina.nv_alvo
            usina.save()

        if request.POST.get("bcx_alvo"):
            press_cx_alvo = float(request.POST.get("press_cx_alvo").replace(',', '.'))
            usina.press_cx_alvo = press_cx_alvo if isinstance(press_cx_alvo, float) else usina.press_cx_alvo
            usina.save()

        if request.POST.get("salvar_params"):
            aux = request.POST.get("alerta_temperatura_fase_r_ug1")
            usina.alerta_temperatura_fase_r_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_fase_r_ug1)

            aux = request.POST.get("alerta_temperatura_fase_s_ug1")
            usina.alerta_temperatura_fase_s_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_fase_s_ug1)

            aux = request.POST.get("alerta_temperatura_fase_t_ug1")
            usina.alerta_temperatura_fase_t_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_fase_t_ug1)

            aux = request.POST.get("alerta_temperatura_nucleo_gerador_1_ug1")
            usina.alerta_temperatura_nucleo_gerador_1_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_nucleo_gerador_1_ug1)

            aux = request.POST.get("alerta_temperatura_nucleo_gerador_2_ug1")
            usina.alerta_temperatura_nucleo_gerador_2_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_nucleo_gerador_2_ug1)

            aux = request.POST.get("alerta_temperatura_nucleo_gerador_3_ug1")
            usina.alerta_temperatura_nucleo_gerador_3_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_nucleo_gerador_3_ug1)

            aux = request.POST.get("alerta_temperatura_mancal_casq_rad_ug1")
            usina.alerta_temperatura_mancal_casq_rad_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_casq_rad_ug1)

            aux = request.POST.get("alerta_temperatura_mancal_casq_comb_ug1")
            usina.alerta_temperatura_mancal_casq_comb_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_casq_comb_ug1)

            aux = request.POST.get("alerta_temperatura_mancal_escora_comb_ug1")
            usina.alerta_temperatura_mancal_escora_comb_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_escora_comb_ug1)

            aux = request.POST.get("limite_temperatura_fase_r_ug1")
            usina.limite_temperatura_fase_r_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_r_ug1)

            aux = request.POST.get("limite_temperatura_fase_s_ug1")
            usina.limite_temperatura_fase_s_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_s_ug1)

            aux = request.POST.get("limite_temperatura_fase_t_ug1")
            usina.limite_temperatura_fase_t_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_t_ug1)

            aux = request.POST.get("limite_temperatura_nucleo_gerador_1_ug1")
            usina.limite_temperatura_nucleo_gerador_1_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_nucleo_gerador_1_ug1)

            aux = request.POST.get("limite_temperatura_nucleo_gerador_2_ug1")
            usina.limite_temperatura_nucleo_gerador_2_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_nucleo_gerador_2_ug1)

            aux = request.POST.get("limite_temperatura_nucleo_gerador_3_ug1")
            usina.limite_temperatura_nucleo_gerador_3_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_nucleo_gerador_3_ug1)

            aux = request.POST.get("limite_temperatura_mancal_casq_rad_ug1")
            usina.limite_temperatura_mancal_casq_rad_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_casq_rad_ug1)

            aux = request.POST.get("limite_temperatura_mancal_casq_comb_ug1")
            usina.limite_temperatura_mancal_casq_comb_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_casq_comb_ug1)

            aux = request.POST.get("limite_temperatura_mancal_escora_comb_ug1")
            usina.limite_temperatura_mancal_escora_comb_ug1 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_escora_comb_ug1)

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

            aux = request.POST.get("alerta_temperatura_nucleo_gerador_1_ug2")
            usina.alerta_temperatura_nucleo_gerador_1_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_nucleo_gerador_1_ug2)

            aux = request.POST.get("alerta_temperatura_nucleo_gerador_2_ug2")
            usina.alerta_temperatura_nucleo_gerador_2_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_nucleo_gerador_2_ug2)

            aux = request.POST.get("alerta_temperatura_nucleo_gerador_3_ug2")
            usina.alerta_temperatura_nucleo_gerador_3_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_nucleo_gerador_3_ug2)

            aux = request.POST.get("alerta_temperatura_mancal_casq_rad_ug2")
            usina.alerta_temperatura_mancal_casq_rad_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_casq_rad_ug2)

            aux = request.POST.get("alerta_temperatura_mancal_casq_comb_ug2")
            usina.alerta_temperatura_mancal_casq_comb_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_casq_comb_ug2)

            aux = request.POST.get("alerta_temperatura_mancal_escora_comb_ug2")
            usina.alerta_temperatura_mancal_escora_comb_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.alerta_temperatura_mancal_escora_comb_ug2)

            aux = request.POST.get("limite_temperatura_fase_r_ug2")
            usina.limite_temperatura_fase_r_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_r_ug2)

            aux = request.POST.get("limite_temperatura_fase_s_ug2")
            usina.limite_temperatura_fase_s_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_s_ug2)

            aux = request.POST.get("limite_temperatura_fase_t_ug2")
            usina.limite_temperatura_fase_t_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_fase_t_ug2)

            aux = request.POST.get("limite_temperatura_nucleo_gerador_1_ug2")
            usina.limite_temperatura_nucleo_gerador_1_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_nucleo_gerador_1_ug2)

            aux = request.POST.get("limite_temperatura_nucleo_gerador_2_ug2")
            usina.limite_temperatura_nucleo_gerador_2_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_nucleo_gerador_2_ug2)

            aux = request.POST.get("limite_temperatura_nucleo_gerador_3_ug2")
            usina.limite_temperatura_nucleo_gerador_3_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_nucleo_gerador_3_ug2)

            aux = request.POST.get("limite_temperatura_mancal_casq_rad_ug2")
            usina.limite_temperatura_mancal_casq_rad_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_casq_rad_ug2)

            aux = request.POST.get("limite_temperatura_mancal_casq_comb_ug2")
            usina.limite_temperatura_mancal_casq_comb_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_casq_comb_ug2)

            aux = request.POST.get("limite_temperatura_mancal_escora_comb_ug2")
            usina.limite_temperatura_mancal_escora_comb_ug2 = (float(aux.replace(",", ".")) if aux is not None and float(aux.replace(",", ".")) > 0 else usina.limite_temperatura_mancal_escora_comb_ug2)

            aux = float(request.POST.get("alerta_caixa_espiral_ug2").replace(",", "."))
            usina.alerta_caixa_espiral_ug2 = aux if isinstance(aux, float) else usina.alerta_caixa_espiral_ug2

            aux = float(request.POST.get("limite_caixa_espiral_ug2").replace(",", "."))
            usina.limite_caixa_espiral_ug2 = aux if isinstance(aux, float) else usina.limite_caixa_espiral_ug2

            usina.timestamp = datetime.now()
            usina.save()

    escolha_ugs = 0
    if ((usina.modo_de_escolha_das_ugs == 2) and (usina.ug1_prioridade > usina.ug2_prioridade)):
        escolha_ugs = 1

    if ((usina.modo_de_escolha_das_ugs == 2) and (usina.ug2_prioridade > usina.ug1_prioridade)):
        escolha_ugs = 2

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

@login_required
def contatos_view(request, *args, **kwargs):
    contato = Contato.objects.all()
    context = {"contato": contato}
    return render(request, "contatos.html", context=context)

@login_required
def adicionar(request, *args, **kwargs):

    if request.method=='POST':
        try:
            if request.POST.get("nome") == "" and request.POST.get("numero") == "" and request.POST.get("data_inicio") == "" and \
            request.POST.get("ts_inicio") == "" and request.POST.get("daata_fim") == "" and request.POST.get("ts_inicio") == "":
                messages.error(request, "Não foi possível adicionar o contato!", extra_tags="Nenhum campo foi preenchido")
                return HttpResponseRedirect(reverse("contatos"))
                
            if request.POST.get("nome") == "":
                messages.error(request, "Não foi possível adicionar o contato!", extra_tags="Favor preencher o campo: Nome")
                return HttpResponseRedirect(reverse('contatos'))
            else:
                ctt_nome = request.POST.get("nome")

            if request.POST.get('numero') == "":
                messages.error(request, "Não foi possível adicionar o contato!", extra_tags="Favor preencher o campo: Número")
                return HttpResponseRedirect(reverse("contatos"))
            else:
                ctt_numero = request.POST.get("numero").replace("(", "").replace(")", "")
            
            if request.POST.get("data_inicio") == "":
                messages.error(request, "Não foi possível adicionar o contato!", extra_tags="Favor preencher o campo: Data início")
                return HttpResponseRedirect(reverse("contatos"))
            else:
                ctt_dt_inicio = request.POST.get("data_inicio")
            
            if request.POST.get("ts_inicio") == "":
                messages.error(request, "Não foi possível adicionar o contato!", extra_tags="Favor preencher o campo: Horário início")
                return HttpResponseRedirect(reverse("contatos"))
            else:
                ctt_ts_inicio = request.POST.get("ts_inicio")
            
            if request.POST.get("data_fim") == "":
                messages.error(request, "Não foi possível adicionar o contato!", extra_tags="Favor preencher o campo: Data fim")
                return HttpResponseRedirect(reverse("contatos"))
            else:
                ctt_dt_fim = request.POST.get("data_fim")
            
            if request.POST.get("ts_fim") == "":
                messages.error(request, "Não foi possível adicionar o contato!", extra_tags="Favor preencher o campo: Horário fim")
                return HttpResponseRedirect(reverse("contatos"))
            else:
                ctt_ts_fim = request.POST.get("ts_fim")

            Contato.objects.create(nome=ctt_nome, numero=ctt_numero, data_inicio=ctt_dt_inicio, ts_inicio=ctt_ts_inicio, data_fim=ctt_dt_fim, ts_fim=ctt_ts_fim)

        except Exception as e:
            messages.error(request, 'Erro!', extra_tags=f"Motivo: {e}")
            return HttpResponseRedirect(reverse('contatos'))

    return HttpResponseRedirect(reverse('contatos'))

@login_required
def deletar(request, id,*args, **kwargs):
    contato = Contato.objects.filter(id=id)
    contato.delete()
    return HttpResponseRedirect(reverse('contatos'))