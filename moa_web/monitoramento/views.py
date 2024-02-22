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
        "emergencia": f"{usina.emergencia_acionada}",
        "timestamp": usina.timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
        "setpot_ug1": f"{usina.ug1_setpot:1.3f}",
        "ug1_state": usina.ug1_ultimo_estado,
        "setpot_ug2": f"{usina.ug2_setpot:1.3f}",
        "ug2_state": usina.ug2_ultimo_estado,
        "nv_alvo": f"{usina.nv_alvo:3.2f}",
        "aguardo": "Sim" if usina.aguardando_reservatorio > 0 else "Não",
    }

    clp_sa = ModbusClient(
        host="192.168.10.109",
        port=502,
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )
    clp_tda = ModbusClient(
        host="192.168.10.105",
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
    rele_se = ModbusClient(
        host="192.168.10.32",
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


    try:
        l_djl_raw = clp_sa.read_holding_registers(12309)

    except Exception:
        pass

    try:
        l_t_vab_raw = (rele_se.read_holding_registers(151)[0] / 1000) * 34500
        l_t_vbc_raw = (rele_se.read_holding_registers(152)[0] / 1000) * 34500
        l_t_vca_raw = (rele_se.read_holding_registers(153)[0] / 1000) * 34500

    except Exception:
        pass

    try:
        l_montante_raw = clp_tda.read_holding_registers(12350, 2)

    except Exception:
        pass

        l_ug1_pot_raw = rele_ug1.read_holding_registers(353)[0]
        l_ug2_pot_raw = rele_ug2.read_holding_registers(353)[0]
        l_ug1_etapa_raw = clp_ug1.read_holding_registers(12390)[0]
        l_ug2_etapa_raw = clp_ug2.read_holding_registers(12390)[0]


    dec_nv = BPD.fromRegisters(l_montante_raw, byteorder=Endian.Big, wordorder=Endian.Little)

    nv_montante = dec_nv.decode_32bit_float()
    context["nv_montante"] = f"{nv_montante:.3f}"

    if 820.9 <= nv_montante < 821:
        context["tag"] = 0
    elif 820.75 <= nv_montante < 820.9:
        context["tag"] = 1
    elif nv_montante < 820.75 or nv_montante > 821:
        context["tag"] = 2

    for key in context:
        if context[key] == "" or context[key] == " ":
            context[key] = "-"

    try:
        dec1 = BPD.fromRegisters(l_djl_raw, byteorder=Endian.Big, wordorder=Endian.Little)
        dec2 = BPD.fromRegisters(l_djl_raw, byteorder=Endian.Big, wordorder=Endian.Little)

        dj_lbit = [int(b) for bits in [reversed(dec1.decode_bits(1)), reversed(dec2.decode_bits(2))] for b in bits]
        dj_lbit_r = [int(b) for b in reversed(dj_lbit)]

        leitura_djl = dj_lbit_r[15]

        if leitura_djl == 1:
            context["status_dj_linha"] = 1
        elif leitura_djl == 0:
            context["status_dj_linha"] = 0
        else:
            context["status_dj_linha"] = 2

    except Exception:
        context["status_dj_linha"] = 99
        pass

    try:
        context["se_ll_t_vab_raw"] = f"{l_t_vab_raw:0.1f}"
        context["se_ll_t_vbc_raw"] = f"{l_t_vbc_raw:0.1f}"
        context["se_ll_t_vca_raw"] = f"{l_t_vca_raw:0.1f}"

    except Exception:
        context["setpot_usina"] = 99
        context["se_ll_t_vab_raw"] = 99
        context["se_ll_t_vbc_raw"] = 99
        context["se_ll_t_vca_raw"] = 99
        pass

    try:
        if l_ug1_etapa_raw in (0, 7):
            context["l_ug1_etapa_raw"] = l_ug1_etapa_raw
        elif l_ug1_etapa_raw == None:
            context["l_ug1_etapa_raw"] = 99
        else:
            context["l_ug1_etapa_raw"] = 50

    except Exception:
        context["l_ug1_etapa_raw"] = 99
        pass

    try:
        if l_ug2_etapa_raw in (0, 7):
            context["l_ug2_etapa_raw"] = l_ug2_etapa_raw
        elif l_ug2_etapa_raw == None:
            context["l_ug2_etapa_raw"] = 99
        else:
            context["l_ug2_etapa_raw"] = 50

    except Exception:
        context["l_ug2_etapa_raw"] = 99
        pass

    try:
        context["pot_ug1"] = l_ug1_pot_raw

    except Exception:
        context["pot_ug1"] = 99
        pass

    try:
        context["pot_ug2"] = l_ug2_pot_raw

    except Exception:
        context["pot_ug2"] = 99
        pass


    tempo_desde_moa_comunicando = (datetime.datetime.now(usina.timestamp.tzinfo) - usina.timestamp - datetime.timedelta(hours=3))

    hours = int(tempo_desde_moa_comunicando.seconds // 3600)
    remainder = int(tempo_desde_moa_comunicando.seconds - hours * 3600)
    mins = int(remainder // 60)
    secs = int(remainder - mins * 60)

    context["tempo_desde_moa_comunicando"] = f"{tempo_desde_moa_comunicando.days} dias, {hours:02d}:{mins:02d}:{secs:02d}"

    return render(request, "monitoramento.html", context=context)
