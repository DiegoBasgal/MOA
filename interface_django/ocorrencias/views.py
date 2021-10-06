from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def ocorrencias_view(request, *args, **kwargs):
    context = {}
    return render(request, 'ocorrencias.html', context=context)