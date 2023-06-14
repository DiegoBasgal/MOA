from datetime import datetime
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Contato

# Create your views here.


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