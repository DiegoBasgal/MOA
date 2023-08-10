import os
import sys
import datetime

from django.shortcuts import render
from parametros.models import ParametrosUsina

# Create your views here.
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder as BPD
from pyModbusTCP.utils import *
from pyModbusTCP.client import ModbusClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("/opt/operacao-autonoma/"))))


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

    if 820.9 <= usina.nv_montante < 821:
        context["tag"] = 0
    elif 820.75 <= usina.nv_montante < 820.9:
        context["tag"] = 1
    elif usina.nv_montante < 820.75 or usina.nv_montante > 821:
        context["tag"] = 2

    for key in context:
        if context[key] == "" or context[key] == " ":
            context[key] = "-"

    try:
        raw_djl = clp_sa.read_holding_registers(12309)

        dec1 = BPD.fromRegisters(raw_djl, byteorder=Endian.Big, wordorder=Endian.Little)
        dec2 = BPD.fromRegisters(raw_djl, byteorder=Endian.Big, wordorder=Endian.Little)

        dj_lbit = [int(b) for bits in [reversed(dec1.decode_bits(1)), reversed(dec2.decode_bits(2))] for b in bits]
        dj_lbit_r = [int(b) for b in reversed(dj_lbit)]

        leitura_djl = dj_lbit_r[15]

        if leitura_djl == 1:
            context["status_dj_linha"] = True
        elif leitura_djl == 0:
            context["status_dj_linha"] = False
        else:
            context["status_dj_linha"] = None

    except Exception:
        context["status_dj_linha"] = None
        pass

    try:
        setpot_usina = clp_sa.read_holding_registers(353)[0]
        context["setpot_usina"] = setpot_usina

    except Exception:
        context["setpot_usina"] = 0
        pass

    try:
        ug1_etapa = clp_ug1.read_holding_registers(12390)[0]
        context["ug1_etapa"] = ug1_etapa

    except Exception:
        context["ug1_etapa"] = 0
        pass

    try:
        ug2_etapa = clp_ug2.read_holding_registers(12390)[0]
        context["ug2_etapa"] = ug2_etapa

    except Exception:
        context["ug2_etapa"] = 0
        pass

    try:
        ug1_pot = rele_ug1.read_holding_registers(353)[0]
        context["pot_ug1"] = ug1_pot

    except Exception:
        context["pot_ug1"] = 0
        pass

    try:
        ug2_pot = rele_ug2.read_holding_registers(353)[0]
        context["pot_ug2"] = ug2_pot

    except Exception:
        context["pot_ug2"] = 0
        pass


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
