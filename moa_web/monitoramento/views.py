import datetime

from django.shortcuts import render
from parametros.models import ParametrosUsina

# Create your views here.
from pyModbusTCP.client import ModbusClient


def monitoramento_view(request, *args, **kwargs):

    usina = ParametrosUsina.objects.get(id=1)
    context = {
        "usina": usina,
        "nv_alvo": f"{usina.nv_alvo:3.2f}",
        "timestamp": usina.timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
        "emergencia": "Sim" if usina.emergencia_acionada else "Não",
        "aguardando_reservatorio": "Sim" if usina.aguardando_reservatorio > 0 else "Não",
    }

    clp_sa = ModbusClient("192.168.68.22", 502, unit_id=1, timeout=0.5, auto_open=True, auto_close=True)
    clp_ug1 = ModbusClient("192.168.68.10", 502, unit_id=1, timeout=0.5, auto_open=True, auto_close=True)
    clp_ug2 = ModbusClient("192.168.68.13", 502, unit_id=1, timeout=0.5, auto_open=True, auto_close=True)
    clp_ug3 = ModbusClient("192.168.68.16", 502, unit_id=1, timeout=0.5, auto_open=True, auto_close=True)
    clp_ug4 = ModbusClient("192.168.68.19", 502, unit_id=1, timeout=0.5, auto_open=True, auto_close=True)
    clp_moa = ModbusClient("192.168.68.220", 502, unit_id=1, timeout=0.5)

    context["tensao_rs"] = f"{(clp_sa.read_holding_registers(25 + 12764)[0] * 0.01):0.1f}"
    context["tensao_st"] = f"{(clp_sa.read_holding_registers(26 + 12764)[0] * 0.01):0.1f}"
    context["tensao_tr"] = f"{(clp_sa.read_holding_registers(27 + 12764)[0] * 0.01):0.1f}"



    nv_montante = (clp_sa.read_holding_registers(2 + 12764)[0] * 0.01) + 800
    context['nv_montante'] = nv_montante

    if nv_montante < 816.50:
        context['tag'] = 2
    elif 816.50 <= nv_montante < 817:
        context['tag'] = 1
    elif 817 <= nv_montante < 817.50:
        context['tag'] = 0
    elif 817.50 <= nv_montante < 818:
        context['tag'] = 1
    elif 818 <= nv_montante:
        context['tag'] = 2



    moa_ultima_comunicacao = (
        datetime.datetime.now(usina.timestamp.tzinfo)
        - usina.timestamp
        - datetime.timedelta(hours=3)
    )

    hours = int(moa_ultima_comunicacao.seconds // 3600)
    remainder = int(moa_ultima_comunicacao.seconds - hours * 3600)
    mins = int(remainder // 60)
    secs = int(remainder - mins * 60)

    context ["moa_ultima_comunicacao"] = f"{moa_ultima_comunicacao.days} dias, {hours:02d}:{mins:02d}:{secs:02d}"

    return render(request, "monitoramento.html", context=context)
