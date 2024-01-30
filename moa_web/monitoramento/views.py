import datetime

from django.shortcuts import render
from parametros.models import ParametrosUsina

# Create your views here.
from pyModbusTCP.client import ModbusClient


def monitoramento_view(request, *args, **kwargs):

    usina = ParametrosUsina.objects.get(id=1)

    context = {
        "usina": usina,
        "em_acionada": "Sim" if usina.emergencia_acionada else "Não",
        "timestamp": usina.timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
        "nv_montante": f"{usina.nv_montante:0.2f}",
        "nv_alvo": f"{usina.nv_alvo:3.2f}",
        "pot_ug1": f"{usina.ug1_pot:0.2f}",
        "ug1_sp": f"{usina.ug1_setpot}",
        "ug1_state": usina.ug1_ultimo_estado,
        "pot_ug2": f"{usina.ug2_pot:0.2f}",
        "ug2_sp": f"{usina.ug2_setpot}",
        "ug2_state": usina.ug2_ultimo_estado,
        "aguardo": "Sim" if usina.aguardando_reservatorio > 0 else "Não",
        "CLP_MOA": usina.clp_moa_ip,
    }

    for key in context:
        if context[key] == "" or context[key] == " ":
            context[key] = "-"

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
