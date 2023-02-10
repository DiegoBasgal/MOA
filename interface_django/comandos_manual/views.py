from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from comandos_manual.models import ComandosManual
from parametros_moa.models import ParametrosUsina

from pyModbusTCP.server import DataBank
from pyModbusTCP.client import ModbusClient 

# Create your views here.

MOA_DICT_DE_STATES = {}
MOA_DICT_DE_STATES[0] = 0
MOA_DICT_DE_STATES[1] = 1
MOA_DICT_DE_STATES[2] = 2
MOA_DICT_DE_STATES[3] = 3

UNIDADE_DICT_DE_ETAPAS = {}
UNIDADE_DICT_DE_ETAPAS[1] = 1
UNIDADE_DICT_DE_ETAPAS[2] = 2
UNIDADE_DICT_DE_ETAPAS[3] = 3
UNIDADE_DICT_DE_ETAPAS[4] = 4

teste_ugs = True

flag_dj = True

@login_required
def comandos_manual_view(request, *args, **kwargs):
   
   comandos_manual = ComandosManual.objects.get(id=1)
   usina = ParametrosUsina.objects.get(id=1)

   if request.POST.get("ativar_ma"):
      usina.modo_autonomo = 1
   elif request.POST.get("desativar_ma"):
      usina.modo_autonomo = 0

   usina.save()

   context = {
      "setpot_ug1": "{:1.3f}".format(usina.ug1_setpot),
      "pot_ug1": "{:1.3f}".format(usina.ug1_pot),
      "tempo_ug1": "{:.2f}".format(usina.ug1_tempo),
      "setpot_ug2": "{:1.3f}".format(usina.ug2_setpot),
      "pot_ug2": "{:1.3f}".format(usina.ug2_pot),
      "tempo_ug2": "{:.2f}".format(usina.ug2_tempo),
      "comandos_manual": comandos_manual,
      "usina": usina
   }

   client = ModbusClient(host=usina.modbus_server_ip, port=usina.modbus_server_porta,timeout=0.5, unit_id=1,)
   client_sa = ModbusClient("10.101.2.215", 5003, unit_id=1, timeout=0.5)

   if client_sa.open():
      reg_dj = client_sa.read_holding_registers(99)[0]
      if reg_dj == 1:
          context["status_dj52l"] = True
      elif reg_dj == 0:
          context["status_dj52l"] = False
      else:
          context["status_dj52l"] = None
      client_sa.close()

   if client.open():
      regs = client.read_holding_registers(0, 120)
      client.close()
      
      if regs is None or regs[0] < 2000:
         context["ug1_state", "ug2_state", "ug1_etapa", "ug2_etapa"] = 99
      else:
         context["ug1_state"] = MOA_DICT_DE_STATES[regs[61]] if regs[61] in MOA_DICT_DE_STATES else 4
         context["ug2_state"] = MOA_DICT_DE_STATES[regs[71]] if regs[71] in MOA_DICT_DE_STATES else 4
         context["ug1_etapa"] = UNIDADE_DICT_DE_ETAPAS[regs[62]] if regs[62] in UNIDADE_DICT_DE_ETAPAS else 99
         context["ug2_etapa"] = UNIDADE_DICT_DE_ETAPAS[regs[72]] if regs[72] in UNIDADE_DICT_DE_ETAPAS else 99

   return render(request, "comandos_manual.html", context=context)

@login_required
def comando_dj52l(request, *args, **kwargs):
   global flag_dj
   usina = ParametrosUsina.objects.get(id=1)
   client = ModbusClient("10.101.2.215", 5003, unit_id=1, timeout=0.5)
   context = {"usina": usina}
   client.open()

   if request.method == "POST":
      if usina.modo_autonomo == 0:
         if request.POST.get("fechar_dj"):
            try:
               if client.read_holding_registers(99)[0] == 0:
                  flag_dj = True
                  return render(request, "confirma_dj.html")
            except Exception:
               context["impedido_dj"] = True
               context["mensagem_dj"] = 0
               return render(request, "comando_impedido.html", context=context)
            else:
               return HttpResponseRedirect(reverse("comandos_manual"))

         elif request.POST.get("abrir_dj"):
            try:
               if client.read_holding_registers(99)[0] == 1:
                  flag_dj = False
                  return render(request, "confirma_dj.html")
            except Exception:
               context["impedido_dj"] = True
               context["mensagem_dj"] = 0
               return render(request, "comando_impedido.html", context=context)
            else:
               return HttpResponseRedirect(reverse("comandos_manual"))

      elif usina.modo_autonomo == 1:
         context["impedido_dj"] = True
         if request.POST.get("fechar_dj"):
            try:
               if client.read_holding_registers(99)[0] == 1:
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               return render(request, "comando_impedido.html", context=context)
            else:
               return render(request, "comando_impedido.html", context=context)

         elif request.POST.get("abrir_dj"):
            try:
               if client.read_holding_registers(99)[0] == 0:
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               return render(request, "comando_impedido.html", context=context)
            else:
               return render(request, "comando_impedido.html", context=context)

@login_required
def confirma_comando_dj(request, *args, **kwargs):
   global flag_dj
   client = ModbusClient("10.101.2.215", 5003, unit_id=1, timeout=0.5)
   client.open()

   if request.method == "POST":
      if request.POST.get("confirmar") and not flag_dj:
         client.write_single_register(99, 0)
         return HttpResponseRedirect(reverse("comandos_manual"))
      elif request.POST.get("confirmar") and flag_dj:
         client.write_single_register(99, 1)
         return HttpResponseRedirect(reverse("comandos_manual"))
      elif request.POST.get("voltar"):
         return HttpResponseRedirect(reverse("comandos_manual"))

@login_required
def comando_ug1(request, *args, **kwargs):
   global teste_ugs
   usina = ParametrosUsina.objects.get(id=1)
   client = ModbusClient("10.101.2.215", 5003, unit_id=1, timeout=0.5)
   client_sa = ModbusClient("10.101.2.215", 5003, unit_id=1, timeout=0.5)
   client.open()
   client_sa.open()
   context = {"usina": usina}

   if request.method == "POST":
      if usina.modo_autonomo == 0:

         if request.POST.get("enviar_setpoint_ug1"):
            if 200 < float(request.POST.get("setpoint_ug1").replace(",", ".")) <= 500:
               sp = float(request.POST.get("setpoint_ug1").replace(",", "."))
               usina.ug1_setpot = sp if isinstance(sp, float) else usina.ug1_setpot
               usina.save()
               return HttpResponseRedirect(reverse("comandos_manual"))

            elif float(request.POST.get("setpoint_ug1").replace(",", ".")) < 200:
               context["impedido_ug1"] = True
               context["mensagem_ug1"] = 1
               return render(request, "comando_impedido.html", context=context)

            elif float(request.POST.get("setpoint_ug1").replace(",", ".")) > 500:
               context["impedido_ug1"] = True
               context["mensagem_ug1"] = 2
               return render(request, "comando_impedido.html", context=context)

         if request.POST.get("manual"):
            try:
               if DataBank.get_words(61)[0] != 0:
                  DataBank.set_words(61, [0])
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               context["impedido_ug1"] = True
               context["mensagem_ug1"] = 3
               return render(request, "comando_impedido.html", context=context)
            else:
               return HttpResponseRedirect(reverse("comandos_manual"))

         elif request.POST.get("disponivel"):
            try:
               if DataBank.get_words(61)[0] != 1:
                  DataBank.set_words(61, [1])
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               context["impedido_ug1"] = True
               context["mensagem_ug1"] = 3
               return render(request, "comando_impedido.html", context=context)
            else:
               return HttpResponseRedirect(reverse("comandos_manual"))

         elif request.POST.get("restrito"):
            try:
               if DataBank.get_words(61)[0] != 2:
                  DataBank.set_words(61, [2])
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               context["impedido_ug1"] = True
               context["mensagem_ug1"] = 3
               return render(request, "comando_impedido.html", context=context)
            else:
               return HttpResponseRedirect(reverse("comandos_manual"))

         elif request.POST.get("indisponivel"):
            try:
               if DataBank.get_words(61)[0] != 3:
                  DataBank.set_words(61, [3])
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               context["impedido_ug1"] = True
               context["mensagem_ug1"] = 3
               return render(request, "comando_impedido.html", context=context)
            else:
               return HttpResponseRedirect(reverse("comandos_manual"))

         if request.POST.get("partir_ug1"):
            try:
               if client_sa.read_holding_registers(99)[0] == 0:
                  context["impedido_ug2"] = True
                  context["mensagem_ug2"] = 1
                  return render(request, "comando_impedido.html", context=context)
               elif client.read_holding_registers(0)[0] == 1:
                  # TODO -> Colocar Regs para partida de acordo com cada usina
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception as e:
               context["impedido_ug1"] = True
               context["mensagem_ug1"] = 3
               return render(request, "comando_impedido.html", context=context)
            else:
               return HttpResponseRedirect(reverse("comandos_manual"))

         elif request.POST.get("parar_ug1"):
            try:
               if not client.read_holding_registers(0)[0] == 0:
                  # TODO -> Colocar Regs para parada de acordo com cada usina
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception as e:
               context["impedido_ug1"] = True
               context["mensagem_ug1"] = 3
               return render(request, "comando_impedido.html", context=context)
            else:
               return HttpResponseRedirect(reverse("comandos_manual"))

      elif usina.modo_autonomo == 1:
         context["impedido_ug1"] = True

         if request.POST.get("enviar_setpoint_ug1"):
            return render(request, "comando_impedido.html", context=context)

         if request.POST.get("manual"):
            try:
               if DataBank.get_words(61)[0] == 0:
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               return render(request, "comando_impedido.html", context=context)
            else:
               return render(request, "comando_impedido.html", context=context)

         elif request.POST.get("disponivel"):
            try:
               if DataBank.get_words(61)[0] == 1:
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               return render(request, "comando_impedido.html", context=context)
            else:
               return render(request, "comando_impedido.html", context=context)

         elif request.POST.get("restrito"):
            try:
               if DataBank.get_words(61)[0] == 2:
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               return render(request, "comando_impedido.html", context=context)
            else:
               return render(request, "comando_impedido.html", context=context)

         elif request.POST.get("indisponivel"):
            try:
               if DataBank.get_words(61)[0] == 3:
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
                return render(request, "comando_impedido.html", context=context)
            else:
               return render(request, "comando_impedido.html", context=context)
         
         if request.POST.get("parar_ug1"):
            try:
               if client.read_holding_registers(0)[0] == 0:
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               return render(request, "comando_impedido.html", context=context)
            else:
               return render(request, "comando_impedido.html", context=context)

         elif request.POST.get("partir_ug1"):
            try:
               if client.read_holding_registers(0)[0] == 5:
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               return render(request, "comando_impedido.html", context=context)
            else:
               return render(request, "comando_impedido.html", context=context)

@login_required
def comando_ug2(request, *args, **kwargs):
   global teste_ugs
   usina = ParametrosUsina.objects.get(id=1)
   client = ModbusClient("10.101.2.215", 5003, unit_id=1, timeout=0.5)
   client_sa = ModbusClient("10.101.2.215", 5003, unit_id=1, timeout=0.5)
   client.open()
   client_sa.open()
   context = {"usina": usina}

   if request.method == "POST":
      if usina.modo_autonomo == 0:

         if request.POST.get("enviar_setpoint_ug2"):
            if 200 < float(request.POST.get("setpoint_ug2").replace(",", ".")) <= 500:
               sp = float(request.POST.get("setpoint_ug2").replace(",", "."))
               usina.ug2_setpot = sp if isinstance(sp, float) else usina.ug2_setpot
               usina.save()
               return HttpResponseRedirect(reverse("comandos_manual"))

            elif float(request.POST.get("setpoint_ug2").replace(",", ".")) < 200:
               context["impedido_ug2"] = True
               context["mensagem_ug2"] = 1
               return render(request, "comando_impedido.html", context=context)

            elif float(request.POST.get("setpoint_ug2").replace(",", ".")) > 500:
               context["impedido_ug2"] = True
               context["mensagem_ug2"] = 2
               return render(request, "comando_impedido.html", context=context)

         if request.POST.get("manual"):
            try:
               if DataBank.get_words(61)[0] != 0:
                  DataBank.set_words(61, [0])
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               context["impedido_ug2"] = True
               context["mensagem_ug2"] = 3
               return render(request, "comando_impedido.html", context=context)
            else:
               return HttpResponseRedirect(reverse("comandos_manual"))

         elif request.POST.get("disponivel"):
            try:
               if DataBank.get_words(61)[0] != 1:
                  DataBank.set_words(61, [1])
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               context["impedido_ug2"] = True
               context["mensagem_ug2"] = 3
               return render(request, "comando_impedido.html", context=context)
            else:
               return HttpResponseRedirect(reverse("comandos_manual"))

         elif request.POST.get("restrito"):
            try:
               if DataBank.get_words(61)[0] != 2:
                  DataBank.set_words(61, [2])
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               context["impedido_ug2"] = True
               context["mensagem_ug2"] = 3
               return render(request, "comando_impedido.html", context=context)
            else:
               return HttpResponseRedirect(reverse("comandos_manual"))

         elif request.POST.get("indisponivel"):
            try:
               if DataBank.get_words(61)[0] != 3:
                  DataBank.set_words(61, [3])
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               context["impedido_ug2"] = True
               context["mensagem_ug2"] = 3
               return render(request, "comando_impedido.html", context=context)
            else:
               return HttpResponseRedirect(reverse("comandos_manual"))

         if request.POST.get("partir_ug2"):
            try:
               if client_sa.read_holding_registers(99)[0] == 0:
                  context["impedido_ug2"] = True
                  context["mensagem_ug2"] = 1
                  return render(request, "comando_impedido.html", context=context)
               elif client.read_holding_registers(0)[0] == 1:
                  # TODO -> Colocar Regs para partida de acordo com cada usina
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception as e:
               context["impedido_ug2"] = True
               context["mensagem_ug2"] = 3
               return render(request, "comando_impedido.html", context=context)
            else:
               return HttpResponseRedirect(reverse("comandos_manual"))

         elif request.POST.get("parar_ug2"):
            try:
               if not client.read_holding_registers(0)[0] == 0:
                  # TODO -> Colocar Regs para parada de acordo com cada usina
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception as e:
               context["impedido_ug2"] = True
               context["mensagem_ug2"] = 3
               return render(request, "comando_impedido.html", context=context)
            else:
               return HttpResponseRedirect(reverse("comandos_manual"))

      elif usina.modo_autonomo == 1:
         context["impedido_ug2"] = True

         if request.POST.get("enviar_setpoint_ug2"):
            return render(request, "comando_impedido.html", context=context)

         if request.POST.get("manual"):
            try:
               if DataBank.get_words(61)[0] == 0:
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               return render(request, "comando_impedido.html", context=context)
            else:
               return render(request, "comando_impedido.html", context=context)

         elif request.POST.get("disponivel"):
            try:
               if DataBank.get_words(61)[0] == 1:
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               return render(request, "comando_impedido.html", context=context)
            else:
               return render(request, "comando_impedido.html", context=context)

         elif request.POST.get("restrito"):
            try:
               if DataBank.get_words(61)[0] == 2:
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               return render(request, "comando_impedido.html", context=context)
            else:
               return render(request, "comando_impedido.html", context=context)

         elif request.POST.get("indisponivel"):
            try:
               if DataBank.get_words(61)[0] == 3:
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
                return render(request, "comando_impedido.html", context=context)
            else:
               return render(request, "comando_impedido.html", context=context)
         
         if request.POST.get("parar_ug2"):
            try:
               if client.read_holding_registers(0)[0] == 0:
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               return render(request, "comando_impedido.html", context=context)
            else:
               return render(request, "comando_impedido.html", context=context)

         elif request.POST.get("partir_ug2"):
            try:
               if client.read_holding_registers(0)[0] == 5:
                  return HttpResponseRedirect(reverse("comandos_manual"))
            except Exception:
               return render(request, "comando_impedido.html", context=context)
            else:
               return render(request, "comando_impedido.html", context=context)

@login_required
def comando_impedido():
   return HttpResponseRedirect(reverse("comandos_manual"))