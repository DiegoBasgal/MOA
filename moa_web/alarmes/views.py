from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Alarmes

# Create your views here.

@login_required
def alarmes_view(request, *args, **kwargs):

    alarmes = Alarmes.objects.all()

    nlinhas = 15
    if int(request.GET.get("nlinhas", 0)) > 15:
        nlinhas = int(request.GET.get("nlinhas", 0))

    if len(alarmes) < nlinhas:
        context = {"alarmes": reversed(alarmes)}
    else:
        log = {}
        x = len(alarmes) - 1

        for i in range(nlinhas):
            log[alarmes[x-i]] = alarmes[i]

        context = {"alarmes": log}

    return render(request, "alarmes.html", context=context)
