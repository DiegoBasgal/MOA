from time import sleep
from datetime import datetime
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from comandos_manual.models import ComandosManual
from parametros_moa.models import ParametrosUsina

# Create your views here.

@login_required
def comandos_manual_view(request, *args, **kwargs):
   
   comandos_manual = ComandosManual.objects.get(id=1)
   usina = ParametrosUsina.objects.get(id=1)

   if request.POST.get("ativar_ma"):
      usina.modo_autonomo = 1
   elif request.POST.get("desativar_ma"):
      usina.modo_autonomo = 0

   context = {"comandos_manual": comandos_manual, "usina": usina}
   return render(request, "comandos_manual.html", context=context)




@login_required
def comando_dj52l(request, *args, **kwargs):
   
   comando_dj = ComandosManual.objects.get(id=1)

   if request.method == "POST":
      if request.POST.get("fechar_dj"):
         comando_dj.comando_dj52l = True
      elif request.POST.get("abrir_dj"):
         comando_dj.comando_dj52l = False

   comando_dj.save()
   context = {"comando_dj": comando_dj}
   render(request, "comandos_manual.html", context=context)
   return HttpResponseRedirect(reverse('comandos_manual'))

@login_required
def comando_ug1(request, *args, **kwargs):
   
   comando_ug1 = ComandosManual.objects.get(id=1)

   if request.method == "POST":
      if request.POST.get("manual"):
         comando_ug1.modo_ug1 = 0
      elif request.POST.get("disponivel"):
         comando_ug1.modo_ug1 = 1
      elif request.POST.get("restrito"):
         comando_ug1.modo_ug1 = 2
      elif request.POST.get("indisponivel"):
         comando_ug1.modo_ug1 = 3

      if request.POST.get("partir_ug1"):
         comando_ug1.partida_ug1 = True
         comando_ug1.parada_ug1 = False
      elif request.POST.get("parar_ug1"):
         comando_ug1.parada_ug1 = True
         comando_ug1.partida_ug1 = False

   comando_ug1.save()
   context = {"comando_ug1": comando_ug1}
   render(request, "comandos_manual.html", context=context)
   return HttpResponseRedirect(reverse("comandos_manual"))

@login_required
def comando_ug2(request, *args, **kwargs):
   
   comando_ug2 = ComandosManual.objects.get(id=1)

   if request.method == "POST":
      if request.POST.get("manual"):
         comando_ug2.modo_ug2 = 0
      elif request.POST.get("disponivel"):
         comando_ug2.modo_ug2 = 1
      elif request.POST.get("restrito"):
         comando_ug2.modo_ug2 = 2
      elif request.POST.get("indisponivel"):
         comando_ug2.modo_ug2 = 3

      if request.POST.get("partir_ug1"):
         comando_ug2.partida_ug2 = True
         comando_ug2.parada_ug2 = False
      elif request.POST.get("parar_ug1"):
         comando_ug2.parada_ug2 = True
         comando_ug2.partida_ug2 = False

   comando_ug2.save()
   context = {"comando_ug2": comando_ug2}
   render(request, "comandos_manual.html", context=context)
   return HttpResponseRedirect(reverse("comandos_manual"))





"""setpoint_ug1 = float(request.POST.get("setpoint_ug1"))
      usina.ug1_setpot = setpoint_ug1 if isinstance(setpoint_ug1, float) else usina.ug1_setpot
      
      setpoint_ug2 = float(request.POST.get("setpoint_ug2"))
      usina.ug2_setpot = setpoint_ug2 if isinstance(setpoint_ug2, float) else usina.ug2_setpot
      
      if request.method == "POST":
      if request.POST.get("ativar_ma") == "True":
         usina.modo_autonomo = 1
      elif request.POST.get("desativar_ma") == "False":
         usina.modo_autonomo = 0

      

      
      
      if request.POST.get("partir_ug2") == "True":
         comandos_manual.partida_ug2 = True
         sleep(2)
         comandos_manual.partida_ug2 = False
      
      if request.POST.get("parar_ug2") == "True":
         comandos_manual.parada_ug2 = True
         sleep(2)
         comandos_manual.parada_ug2 = False

      if request.POST.get("forcar_manual_ug2") == "True":
         comandos_manual.forcar_manual_ug2 = True
         
      elif request.POST.get("forcar_manual_ug2") == "False":
         comandos_manual.forcar_manual_ug2 = False
      
      
      if request.POST.get("abrir_comporta1") == "True":
         comandos_manual.abrir_comporta1 = True
         comandos_manual.fechar_comporta1 = False
         comandos_manual.cracking_comporta1 = False
      
      if request.POST.get("fechar_comporta1") == "True":
         comandos_manual.fechar_comporta1 = True
         comandos_manual.abrir_comporta1 = False
         comandos_manual.cracking_comporta1 = False

      if request.POST.get("cracking_comporta1") == "True":
         comandos_manual.cracking_comporta1 = True
         comandos_manual.abrir_comporta1 = False
         comandos_manual.fechar_comporta1 = False
      
      if request.POST.get("abrir_comporta2") == "True":
         comandos_manual.abrir_comporta2 = True
         comandos_manual.fechar_comporta2 = False
         comandos_manual.cracking_comporta2 = False
      
      if request.POST.get("fechar_comporta2") == "True":
         comandos_manual.fechar_comporta2 = True
         comandos_manual.abrir_comporta2 = False
         comandos_manual.cracking_comporta2 = False

      if request.POST.get("cracking_comporta2") == "True":
         comandos_manual.cracking_comporta2 = True
         comandos_manual.abrir_comporta2 = False
         comandos_manual.fechar_comporta2 = False"""