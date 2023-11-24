import os
import json
import datetime

from django.shortcuts import render
from parametros.models import ParametrosUsina

# Create your views here.
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder as BPD
from pyModbusTCP.client import ModbusClient


MOA_DICT_DE_STATES = {}
MOA_DICT_DE_STATES[0] = 0
MOA_DICT_DE_STATES[1] = 1
MOA_DICT_DE_STATES[2] = 2
MOA_DICT_DE_STATES[3] = 3

UNIDADE_PARADA = 1
UNIDADE_PARANDO = 2
UNIDADE_SINCRONIZANDO = 3
UNIDADE_SINCRONIZADA = 4
UNIDADE_INCONSISTENTE = 99


def monitoramento_view(request, *args, **kwargs):

    usina = ParametrosUsina.objects.get(id=1)
    context = {
        "usina": usina,
        "nv_alvo": f"{usina.nv_alvo:3.2f}",
        "timestamp": usina.timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
        "emergencia": "Sim" if usina.emergencia_acionada else "Não",
        "aguardando_reservatorio": "Sim" if usina.aguardando_reservatorio > 0 else "Não",
    }

    clp_sa = ModbusClient("192.168.68.22", 502, unit_id=1, timeout=0.5)
    clp_tda = ModbusClient("192.168.68.29", 502, unit_id=1, timeout=0.5)
    clp_ad = ModbusClient("192.168.68.30", 502, unit_id=1, timeout=0.5)
    clp_ug1 = ModbusClient("192.168.68.10", 502, unit_id=1, timeout=0.5)
    clp_ug2 = ModbusClient("192.168.68.13", 502, unit_id=1, timeout=0.5)
    clp_ug3 = ModbusClient("192.168.68.16", 502, unit_id=1, timeout=0.5)
    clp_ug4 = ModbusClient("192.168.68.19", 502, unit_id=1, timeout=0.5)
    clp_moa = ModbusClient("0.0.0.0", 502, unit_id=1, timeout=0.5)


    if clp_sa.open():
        se_lt_a = clp_sa.read_holding_registers(49, 2)
        se_lt_b = clp_sa.read_holding_registers(51, 2)
        se_lt_c = clp_sa.read_holding_registers(53, 2)
        clp_sa.close()

        dec_lt_a = BPD.fromRegisters(se_lt_a, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        dec_lt_b = BPD.fromRegisters(se_lt_b, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        dec_lt_c = BPD.fromRegisters(se_lt_c, byteorder=Endian.BIG, wordorder=Endian.LITTLE)

        context["se_lt_a"] = f"{dec_lt_a.decode_32bit_float():0.1f}"
        context["se_lt_b"] = f"{dec_lt_b.decode_32bit_float():0.1f}"
        context["se_lt_c"] = f"{dec_lt_c.decode_32bit_float():0.1f}"

    else:
        context["se_lt_a"] = "???"
        context["se_lt_b"] = "???"
        context["se_lt_c"] = "???"


    if clp_tda.open():
        l_nv = clp_tda.read_holding_registers(31, 2)
        clp_tda.close()

        dec_l_nv = BPD.fromRegisters(l_nv, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        val_l_nv = dec_l_nv.decode_32bit_float()

        context["nv_montante"] = f"{val_l_nv:0.3f}"

        if 817 <= val_l_nv <= 818.40:
            context["tag"] = 0
        elif 817 < val_l_nv < 817.6:
            context["tag"] = 1
        elif val_l_nv <= 816 or val_l_nv > 818.4:
            context["tag"] = 2

    else:
        if usina.modo_autonomo:
            context["nv_montante"] = usina.nv_montante

            if 817 <= usina.nv_montante <= 818.40:
                context["tag"] = 0
            elif 817 < usina.nv_montante < 817.6:
                context["tag"] = 1
            elif usina.nv_montante <= 816 or usina.nv_montante > 818.4:
                context["tag"] = 2


    if clp_ug1.open():
        l_pot_ug1 = clp_ug1.read_holding_registers(133, 2)
        clp_ug1.close()

        dec_pot_ug1 = BPD.fromRegisters(l_pot_ug1, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        pot_ug1 = dec_pot_ug1.decode_32bit_float()

        context["pot_ug1"] = pot_ug1
        context["setpot_ug1"] = usina.ug1_setpot
        context["tempo_ug1"] = 0

    else:
        if usina.modo_autonomo:
            context["pot_ug1"] = usina.ug1_pot
            context["setpot_ug1"] = usina.ug1_setpot
            context["tempo_ug1"] = 0

        else:
            context["pot_ug1"] = 99
            context["setpot_ug1"] = usina.ug1_setpot
            context["tempo_ug1"] = 0


    if clp_ug2.open():
        l_pot_ug2 = clp_ug2.read_holding_registers(133, 2)
        clp_ug2.close()

        dec_pot_ug2 = BPD.fromRegisters(l_pot_ug2, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        pot_ug2 = dec_pot_ug2.decode_32bit_float()

        context["pot_ug2"] = pot_ug2
        context["setpot_ug2"] = usina.ug2_setpot
        context["tempo_ug2"] = 0

    else:
        if usina.modo_autonomo:
            context["pot_ug2"] = usina.ug2_pot
            context["setpot_ug2"] = usina.ug2_setpot
            context["tempo_ug2"] = 0

        else:
            context["pot_ug2"] = 99
            context["setpot_ug2"] = usina.ug2_setpot
            context["tempo_ug2"] = 0


    if clp_ug3.open():
        l_pot_ug3 = clp_ug3.read_holding_registers(133, 2)
        clp_ug3.close()

        dec_pot_ug3 = BPD.fromRegisters(l_pot_ug3, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        pot_ug3 = dec_pot_ug3.decode_32bit_float()

        context["pot_ug3"] = pot_ug3
        context["setpot_ug3"] = usina.ug3_setpot
        context["tempo_ug3"] = 0

    else:
        if usina.modo_autonomo:
            context["pot_ug3"] = usina.ug3_pot
            context["setpot_ug3"] = usina.ug3_setpot
            context["tempo_ug3"] = 0

        else:
            context["pot_ug3"] = 99
            context["setpot_ug3"] = usina.ug3_setpot
            context["tempo_ug3"] = 0


    if clp_ug4.open():
        l_pot_ug4 = clp_ug4.read_holding_registers(133, 2)
        clp_ug4.close()

        dec_pot_ug4 = BPD.fromRegisters(l_pot_ug4, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        pot_ug4 = dec_pot_ug4.decode_32bit_float()

        context["pot_ug4"] = pot_ug4
        context["setpot_ug4"] = usina.ug4_setpot
        context["tempo_ug4"] = 0

    else:
        if usina.modo_autonomo:
            context["pot_ug4"] = usina.ug4_pot
            context["setpot_ug4"] = usina.ug4_setpot
            context["tempo_ug4"] = 0

        else:
            context["pot_ug4"] = 99
            context["setpot_ug4"] = usina.ug4_setpot
            context["tempo_ug4"] = 0


    # if clp_moa.open():
    #     context["CLP_Status"] = True
    #     clp_moa.close()

    # else:
    #     context["CLP_Status"] = False


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


    if context["pot_ug1"] in (usina.ug1_pot, 99) \
    or context["pot_ug2"] in (usina.ug2_pot, 99) \
    or context["pot_ug3"] in (usina.ug3_pot, 99) \
    or context["pot_ug4"] in (usina.ug4_pot, 99):
        context["pot_usina"] = f"{usina.ug1_pot + usina.ug2_pot + usina.ug3_pot + usina.ug4_pot:0.1f}"

    else:
        context["pot_usina"] = f"{pot_ug1 + pot_ug2 + usina.ug3_pot + usina.ug4_pot:0.1f}"


    return render(request, "monitoramento.html", context=context)
