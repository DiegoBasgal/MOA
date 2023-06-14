from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.sessions import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from modo_manual.models import ModoManual
from parametros.models import ParametrosUsina

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

@login_required
def comandos_manual_view(request, *args, **kwargs):
   usina = ParametrosUsina.objects.get(id=1)
   comando = ModoManual.objects.get(id=1)
   client = ModbusClient(host="10.101.2.215", port=5003,timeout=0.5, unit_id=1,)
   client_sa = ModbusClient("10.101.2.215", 5003, unit_id=1, timeout=0.5)

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
      "comandos_manual": comando,
      "usina": usina,
   }

   """if client_sa.open():
      reg_dj = client_sa.read_holding_registers(99)[0]
      if reg_dj == 1:
         comando.comando_dj52l = 1
      elif reg_dj == 0:
         comando.comando_dj52l = 0
      else:
         comando.comando_dj52l = 2
         client_sa.close()"""

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
def comando_abrir_dj(request, *args, **kwargs):
   usina = ParametrosUsina.objects.get(id=1)
   comando = ModoManual.objects.get(id=1)
   #client = ModbusClient("10.101.2.215", 5003, unit_id=1, timeout=0.5)
   #client.open()

   if request.method == "POST":
      if usina.modo_autonomo == 0:
         try:
            if request.POST.get('abrir_dj', 'Abrir'):
               if comando.comando_dj52l == 1: #client.read_holding_registers(99)[0] == 1:
                  comando.comando_dj52l = 0
                  comando.save()
                  return HttpResponseRedirect(reverse("comandos_manual"))
               else:
                  messages.info(request, "Comando ignorado!", extra_tags="O disjuntor já está aberto")
                  return HttpResponseRedirect(reverse("comandos_manual"))

         except Exception as e:
            messages.error(request, "ERRO!", extra_tags=e.with_traceback)
            return HttpResponseRedirect(reverse("comandos_manual"))

      elif usina.modo_autonomo == 1:
         try:
            if request.POST.get('abrir_dj', 'Abrir'):
               messages.warning(request, "Não foi possível executar o comando!", extra_tags="MOA - Modo autônomo ativado")
               return HttpResponseRedirect(reverse("comandos_manual"))

         except Exception:
            messages.error(request, "ERRO!", extra_tags="Comunicação ModBus Falhou")
            return HttpResponseRedirect(reverse("comandos_manual"))

@login_required
def comando_fechar_dj(request, *args, **kwargs):
   usina = ParametrosUsina.objects.get(id=1)
   comando = ModoManual.objects.get(id=1)
   #client = ModbusClient("10.101.2.215", 5003, unit_id=1, timeout=0.5)
   #client.open()

   if request.method == "POST":
      if usina.modo_autonomo == 0:
         try:
            if request.POST.get('fechar_dj', 'Fechar'):
               if comando.comando_dj52l == 0: #client.read_holding_registers(99)[0] == 0:
                  comando.comando_dj52l = 1
                  comando.save()
                  return HttpResponseRedirect(reverse("comandos_manual"))
               else:
                  messages.info(request, "Comando ignorado!", extra_tags="O disjuntor já está fechado")
                  return HttpResponseRedirect(reverse("comandos_manual"))

         except Exception as e:
            messages.error(request, "ERRO!", extra_tags=e.with_traceback)
            return HttpResponseRedirect(reverse("comandos_manual"))

      elif usina.modo_autonomo == 1:
         try:
            if request.POST.get('fechar_dj', 'Fechar'):
               messages.warning(request, "Não foi possível executar o comando!", extra_tags="MOA - Modo autônomo ativado")
               return HttpResponseRedirect(reverse("comandos_manual"))

         except Exception:
            messages.error(request, "ERRO!", extra_tags="Comunicação ModBus Falhou")
            return HttpResponseRedirect(reverse("comandos_manual"))


@login_required
def comando_ug1(request, *args, **kwargs):
   global teste_ugs
   teste = False
   usina = ParametrosUsina.objects.get(id=1)
   client = ModbusClient("10.101.2.215", 5003, unit_id=1, timeout=0.5)
   client_sa = ModbusClient("10.101.2.215", 5003, unit_id=1, timeout=0.5)
   client.open()
   client_sa.open()

   if request.method == "POST":
      if usina.modo_autonomo == 0:
         try:
            if request.POST.get("enviar_setpoint_ug1"):
               setpoint = int(request.POST.get("setpoint_ug1"))
               if 200 < setpoint <= 500:
                  usina.ug1_setpot = setpoint
                  usina.save()
                  return HttpResponseRedirect(reverse("comandos_manual"))

               elif setpoint < 200:
                  messages.warning(request, "Não foi possível executar o comando!", extra_tags="Setpoint abaixo do mínimo")
                  return HttpResponseRedirect(reverse("comandos_manual"))

               elif setpoint > 500:
                  messages.warning(request, "Não foi possível executar o comando!", extra_tags="Setpoint acima do máximo")
                  return HttpResponseRedirect(reverse("comandos_manual"))
         except Exception as e:
            messages.error(request, "ERRO!", extra_tags=e)
            return HttpResponseRedirect(reverse("comandos_manual"))

         try:
            if request.POST.get("manual"):
               if client.read_coils(61)[0] != 0:
                  client.write_single_coil(61, [0])
                  return HttpResponseRedirect(reverse("comandos_manual"))
               else:
                  messages.info(request, "Comando ignorado!", extra_tags="A unidade já está no modo manual")
                  return HttpResponseRedirect(reverse("comandos_manual"))

            elif request.POST.get("disponivel"):
               if client.read_coils(61)[0] != 1:
                  client.write_single_coil(61, [1])
                  return HttpResponseRedirect(reverse("comandos_manual"))
               else:
                  messages.info(request, "Comando ignorado!", extra_tags="A unidade já está no modo disponível")
                  return HttpResponseRedirect(reverse("comandos_manual"))

            elif request.POST.get("restrito"):
               if client.read_coils(61)[0] != 2:
                  client.write_single_coil(61, [2])
                  return HttpResponseRedirect(reverse("comandos_manual"))
               else:
                  messages.info(request, "Comando ignorado!", extra_tags="A unidade já está no modo restrito")
                  return HttpResponseRedirect(reverse("comandos_manual"))

            elif request.POST.get("indisponivel"):
               if client.read_coils(61)[0] != 3:
                  client.write_single_coil(61, [3])
                  return HttpResponseRedirect(reverse("comandos_manual"))
               else:
                  messages.info(request, "Comando ignorado!", extra_tags="A unidade já está no modo indisponivel")
                  return HttpResponseRedirect(reverse("comandos_manual"))

            if request.POST.get("partir_ug1"):
               if teste: #client_sa.read_holding_registers(99)[0] == 0:
                  messages.warning(request, "Não foi possível executar o comando!", extra_tags="Disjuntor 52L - Aberto")
                  return HttpResponseRedirect(reverse("comandos_manual"))
               if teste: #client.read_holding_registers(0)[0] == 1:
                  # TODO -> Colocar Regs para partida de acordo com cada usina
                  return HttpResponseRedirect(reverse("comandos_manual"))
               else:
                  messages.info(request, "Comando ignorado!", extra_tags="A unidade ja está operando")
                  return HttpResponseRedirect(reverse("comandos_manual"))

            elif request.POST.get("parar_ug1"):
               if teste:#not client.read_holding_registers(0)[0] == 0:
                  # TODO -> Colocar Regs para parada de acordo com cada usina
                  return HttpResponseRedirect(reverse("comandos_manual"))
               else:
                  messages.info(request, "Comando ignorado!", extra_tags="A unidade ja está parada")
                  return HttpResponseRedirect(reverse("comandos_manual"))
         
         except Exception as e:
            messages.error(request, "ERRO!", extra_tags="Comunicação ModBus Falhou")
            return HttpResponseRedirect(reverse("comandos_manual"))

      elif usina.modo_autonomo == 1:
         if request.POST.get("enviar_setpoint_ug1") or request.POST.get("parar_ug1") or request.POST.get("partir_ug1")\
            or request.POST.get("manual") or request.POST.get("disponivel") or request.POST.get("restrito") or request.POST.get("indisponivel"):
            messages.warning(request, "Não foi possível executar o comando!", extra_tags="MOA - Modo autônomo ativado")
            return HttpResponseRedirect(reverse("comandos_manual"))

@login_required
def comando_ug2(request, *args, **kwargs):
   global teste_ugs
   usina = ParametrosUsina.objects.get(id=1)
   client = ModbusClient("10.101.2.215", 5003, unit_id=1, timeout=0.5)
   client_sa = ModbusClient("10.101.2.215", 5003, unit_id=1, timeout=0.5)
   client.open()
   client_sa.open()

   if request.method == "POST":
      if usina.modo_autonomo == 0:
         try:
            if request.POST.get("enviar_setpoint_ug2"):
               setpoint = int(request.POST.get("setpoint_ug2"))
               if 200 < setpoint <= 500:
                  usina.ug2_setpot = setpoint
                  usina.save()
                  return HttpResponseRedirect(reverse("comandos_manual"))

               elif setpoint < 200:
                  messages.warning(request, "Não foi possível executar o comando!", extra_tags="Setpoint abaixo do mínimo")
                  return HttpResponseRedirect(reverse("comandos_manual"))

               elif setpoint > 500:
                  messages.warning(request, "Não foi possível executar o comando!", extra_tags="Setpoint acima do máximo")
                  return HttpResponseRedirect(reverse("comandos_manual"))
         except Exception as e:
            messages.error(request, "ERRO!", extra_tags=e)
            return HttpResponseRedirect(reverse("comandos_manual"))

         try:
            if request.POST.get("manual"):
               if client.read_coils(71)[0] != 0:
                  client.write_single_coil(71, [0])
                  return HttpResponseRedirect(reverse("comandos_manual"))
               else:
                  messages.info(request, "Comando ignorado!", extra_tags="A unidade já está no modo manual")
                  return HttpResponseRedirect(reverse("comandos_manual"))

            elif request.POST.get("disponivel"):
               if client.read_coils(71)[0] != 1:
                  client.write_single_coil(71, [1])
                  return HttpResponseRedirect(reverse("comandos_manual"))
               else:
                  messages.info(request, "Comando ignorado!", extra_tags="A unidade já está no modo disponivel")
                  return HttpResponseRedirect(reverse("comandos_manual"))

            elif request.POST.get("restrito"):
               if client.read_coils(71)[0] != 2:
                  client.write_single_coil(71, [2])
                  return HttpResponseRedirect(reverse("comandos_manual"))
               else:
                  messages.info(request, "Comando ignorado!", extra_tags="A unidade já está no modo restrito")
                  return HttpResponseRedirect(reverse("comandos_manual"))

            elif request.POST.get("indisponivel"):
               if client.read_coils(71)[0] != 3:
                  client.write_single_coil(71, [3])
                  return HttpResponseRedirect(reverse("comandos_manual"))
               else:
                  messages.info(request, "Comando ignorado!", extra_tags="A unidade já está no modo indisponivel")
                  return HttpResponseRedirect(reverse("comandos_manual"))

            if request.POST.get("partir_ug2"):
               if client_sa.read_holding_registers(99)[0] == 0:
                  messages.warning(request, "Não foi possível executar o comando!", extra_tags="Disjuntor 52L - Aberto")
                  return HttpResponseRedirect(reverse("comandos_manual"))
               if client.read_holding_registers(0)[0] == 1:
                  # TODO -> Colocar Regs para partida de acordo com cada usina
                  return HttpResponseRedirect(reverse("comandos_manual"))
               else:
                  messages.info(request, "Comando ignorado!", extra_tags="A unidade já está operando")
                  return HttpResponseRedirect(reverse("comandos_manual"))

            elif request.POST.get("parar_ug2"):
               if not client.read_holding_registers(0)[0] == 0:
                  # TODO -> Colocar Regs para parada de acordo com cada usina
                  return HttpResponseRedirect(reverse("comandos_manual"))
               else:
                  messages.info(request, "Comando ignorado!", extra_tags="A unidade já está parada")
                  return HttpResponseRedirect(reverse("comandos_manual"))
         
         except Exception as e:
            messages.error(request, "ERRO!", extra_tags="Comunicação ModBus Falhou")
            return HttpResponseRedirect(reverse("comandos_manual"))

      elif usina.modo_autonomo == 1:
         if request.POST.get("enviar_setpoint_ug2") or request.POST.get("parar_ug2") or request.POST.get("partir_ug2")\
            or request.POST.get("manual") or request.POST.get("disponivel") or request.POST.get("restrito") or request.POST.get("indisponivel"):
            messages.warning(request, "Não foi possível executar o comando!", extra_tags="MOA - Modo autônomo ativado")
            return HttpResponseRedirect(reverse("comandos_manual"))