from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from contatos.models import Contato

# Create your views here.

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