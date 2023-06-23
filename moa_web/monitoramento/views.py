import os
import sys
import datetime

from django.shortcuts import render
from parametros.models import ParametrosUsina

# Create your views here.
from pyModbusTCP.utils import *
from pyModbusTCP.client import ModbusClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("/opt/operacao-autonoma/"))))

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


def monitoramento_view(request, *args, **kwargs):
    usina = ParametrosUsina.objects.get(id=1)

    context = {
        "usina": usina,
        "em_acionada": f"{usina.emergencia_acionada}",
        "timestamp": usina.timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
        "setpot_ug1": f"{usina.ug1_setpot:1.3f}",
        "ug1_state": usina.ug1_ultimo_estado,
        "setpot_ug2": f"{usina.ug2_setpot:1.3f}",
        "ug2_state": usina.ug2_ultimo_estado,
        "nv_alvo": f"{usina.nv_alvo:3.2f}",
        "aguardo": "Sim" if usina.aguardando_reservatorio > 0 else "Não",
        "nv_montante": f"{usina.nv_montante:3.2f}",
    }

    clp_sa = ModbusClient(
        host="192.168.10.109",
        port=502,
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )
    clp_ug1 = ModbusClient(
        host="192.168.10.110",
        port=502,
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )
    clp_ug2 = ModbusClient(
        host="192.168.10.120",
        port=502,
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )
    rele_ug1 = ModbusClient(
        host="192.168.10.111",
        port=502,
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )
    rele_ug2 = ModbusClient(
        host="192.168.10.121",
        port=502,
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )

    raw_djl = clp_sa.read_holding_registers(12309)[0]
    raw_djl_aux = clp_sa.read_holding_registers(12308)[0]
    conv = get_bits_from_int(raw_djl)
    conv_aux = get_bits_from_int(raw_djl_aux)
    lista_bits = conv_aux + conv
    for i in range(len(lista_bits)):
        if i == 31:
            leitura_djl = lista_bits[i]

    if 820.9 <= usina.nv_montante < 821:
        context["tag"] = 0
    elif 820.75 <= usina.nv_montante < 820.9:
        context["tag"] = 1
    elif usina.nv_montante < 820.75 or usina.nv_montante > 821:
        context["tag"] = 2

    if leitura_djl == 0:
        context["status_dj_linha"] = True
    elif leitura_djl == 1:
        context["status_dj_linha"] = False
    else:
        context["status_dj_linha"] = None

    for key in context:
        if context[key] == "" or context[key] == " ":
            context[key] = "-"

    context["setpot_usina"] = clp_sa.read_holding_registers(353)[0]
    context["ug1_etapa"] = clp_ug1.read_holding_registers(12390)[0]
    context["ug2_etapa"] = clp_ug2.read_holding_registers(12390)[0]
    context["pot_ug1"] = rele_ug1.read_holding_registers(353)[0]
    context["pot_ug2"] = rele_ug2.read_holding_registers(353)[0]

    tempo_desde_moa_comunicando = (
        datetime.datetime.now(usina.timestamp.tzinfo)
        - usina.timestamp
        - datetime.timedelta(hours=3)
    )

    hours = int(tempo_desde_moa_comunicando.seconds // 3600)
    remainder = int(tempo_desde_moa_comunicando.seconds - hours * 3600)
    mins = int(remainder // 60)
    secs = int(remainder - mins * 60)

    context["tempo_desde_moa_comunicando"] = f"{tempo_desde_moa_comunicando.days} dias, {hours:02d}:{mins:02d}:{secs:02d}"

    return render(request, "monitoramento.html", context=context)
