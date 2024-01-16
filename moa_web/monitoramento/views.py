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

    clp_sa = ModbusClient("192.168.20.130", 502, unit_id=1, timeout=0.5)
    clp_tda = ModbusClient("192.168.20.140", 503, unit_id=1, timeout=0.5)
    clp_ug1 = ModbusClient("192.168.20.110", 502, unit_id=1, timeout=0.5)
    clp_ug2 = ModbusClient("192.168.20.120", 502, unit_id=1, timeout=0.5)
    clp_moa = ModbusClient("192.168.20.210", 502, unit_id=1, timeout=0.5)

    rele_se = ModbusClient("192.168.20.135", 502, unit_id=1, timeout=0.5)
    rele_bay = ModbusClient("192.168.20.170", 502, unit_id=1, timeout=0.5)
    rele_ug1 = ModbusClient("192.168.20.115", 502, unit_id=1, timeout=0.5)
    rele_ug2 = ModbusClient("192.168.20.125", 502, unit_id=1, timeout=0.5)

    rv_ug1 = ModbusClient("192.168.20.150", 502, unit_id=11, timeout=0.5)
    rv_ug2 = ModbusClient("192.168.20.150", 502, unit_id=21, timeout=0.5)

    if rele_bay.open():
        context["bay_lt_a"] = f"{((rele_bay.read_holding_registers(11)[0]) / 1000):0.1f}"
        context["bay_lt_b"] = f"{((rele_bay.read_holding_registers(14)[0]) / 1000):0.1f}"
        context["bay_lt_c"] = f"{((rele_bay.read_holding_registers(17)[0]) / 1000):0.1f}"
        bay_l_status_dj = rele_bay.read_holding_registers(44, 2)
        rele_bay.close()

        bay_dec_1 = BPD.fromRegisters(bay_l_status_dj, byteorder=Endian.LITTLE)
        bay_dec_2 = BPD.fromRegisters(bay_l_status_dj, byteorder=Endian.LITTLE)

        lbit = [int(bit) for bits in [reversed(bay_dec_1.decode_bits(1)), reversed(bay_dec_2.decode_bits(2))] for bit in bits]
        lbit_r = [b for b in reversed(lbit)]
        for i in range(len(lbit_r)):
            if i == 0:
                context["bay_status_dj"] = int(lbit_r[i])
                break

    else:
        context["bay_lt_a"] = 99
        context["bay_lt_b"] = 99
        context["bay_lt_c"] = 99
        context["bay_status_dj"] = 99


    if rele_se.open():
        se_l_status_dj = rele_se.read_holding_registers(43, 2)
        rele_se.close()

        se_dec_1 = BPD.fromRegisters(se_l_status_dj, byteorder=Endian.LITTLE)
        se_dec_2 = BPD.fromRegisters(se_l_status_dj, byteorder=Endian.LITTLE)

        lbit = [int(bit) for bits in [reversed(se_dec_1.decode_bits(1)), reversed(se_dec_2.decode_bits(2))] for bit in bits]
        lbit_r = [b for b in reversed(lbit)]
        for i in range(len(lbit_r)):
            if i == 0:
                context["se_status_dj"] = int(lbit_r[i])
                break

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


    # if clp_tda.open():
    #     l_nv = clp_tda.read_holding_registers(31, 2)
    #     l_cp1_b0 = clp_tda.read_holding_registers(0, 2)
    #     l_cp2_b0 = clp_tda.read_holding_registers(0, 2)
    #     l_cp1_b1 = clp_tda.read_holding_registers(1, 2)
    #     clp_tda.close()

    #     dec_l_nv = BPD.fromRegisters(l_nv, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    #     val_l_nv = dec_l_nv.decode_32bit_float()

    #     context["nv_montante"] = f"{val_l_nv:0.3f}"

    #     if 462 <= val_l_nv <= 462.37:
    #         context["tag"] = 0
    #     elif 461.85 < val_l_nv < 462:
    #         context["tag"] = 1
    #     elif val_l_nv <= 461.37 or val_l_nv > 462.37:
    #         context["tag"] = 2

    #     dec1_cp1_b0 = BPD.fromRegisters(l_cp1_b0, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    #     dec2_cp1_b0 = BPD.fromRegisters(l_cp1_b0, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    #     lbit = [int(bit) for bits in [reversed(dec1_cp1_b0.decode_bits(1)), reversed(dec2_cp1_b0.decode_bits(2))] for bit in bits]
    #     lbit_r = [b for b in reversed(lbit)]

    #     if lbit_r[0]:
    #         context["cp1_etapa"] = 2
    #     if lbit_r[6]:
    #         context["cp1_etapa"] = 5

    #     dec1_cp1_b1 = BPD.fromRegisters(l_cp1_b1, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    #     dec2_cp1_b1 = BPD.fromRegisters(l_cp1_b1, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    #     lbit = [int(bit) for bits in [reversed(dec1_cp1_b1.decode_bits(1)), reversed(dec2_cp1_b1.decode_bits(2))] for bit in bits]
    #     lbit_r = [b for b in reversed(lbit)]

    #     if lbit_r[14]:
    #         context["cp1_etapa"] = 1
    #     elif lbit_r[15]:
    #         context["cp1_etapa"] = 0

    #     dec1_cp2_b0 = BPD.fromRegisters(l_cp2_b0, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    #     dec2_cp2_b0 = BPD.fromRegisters(l_cp2_b0, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    #     lbit = [int(bit) for bits in [reversed(dec1_cp2_b0.decode_bits(1)), reversed(dec2_cp2_b0.decode_bits(2))] for bit in bits]
    #     lbit_r = [b for b in reversed(lbit)]
    #     if lbit_r[1]:
    #         context["cp2_etapa"] = 1
    #     elif lbit_r[2]:
    #         context["cp2_etapa"] = 0
    #     elif lbit_r[3]:
    #         context["cp2_etapa"] = 2
    #     if lbit_r[9]:
    #         context["cp2_remoto"] = 5

    # else:
    if usina.modo_autonomo:
        context["cp1_etapa"] = usina.ug1_pos_comporta
        context["cp2_etapa"] = usina.ug2_pos_comporta
        context["nv_montante"] = usina.nv_montante

        if 462 <= usina.nv_montante <= 462.37:
            context["tag"] = 0
        elif 461.85 < usina.nv_montante < 462:
            context["tag"] = 1
        elif usina.nv_montante <= 461.37 or usina.nv_montante > 462.37:
            context["tag"] = 2
    else:
        context["cp1_etapa"] = 99
        context["cp2_etapa"] = 99


    if rv_ug1.open():
        l_etapa_ug1 = rv_ug1.read_holding_registers(21)[0]
        rv_ug1.close()

        if l_etapa_ug1 == 1 or l_etapa_ug1 == 17:
            context["ug1_etapa"] = UNIDADE_PARADA
        elif 7 < l_etapa_ug1 < 17:
            context["ug1_etapa"] = UNIDADE_PARANDO
        elif 1 < l_etapa_ug1 < 7:
            context["ug1_etapa"] = UNIDADE_SINCRONIZANDO
        elif l_etapa_ug1 == 7:
            context["ug1_etapa"] = UNIDADE_SINCRONIZADA
        else:
            context["ug1_etapa"] = UNIDADE_INCONSISTENTE

    else:
        context["ug1_etapa"] = 999


    if rv_ug2.open():
        l_etapa_ug2 = rv_ug2.read_holding_registers(21)[0]
        rv_ug2.close()

        if l_etapa_ug2 == 1 or l_etapa_ug2 == 17:
            context["ug2_etapa"] = UNIDADE_PARADA
        elif 7 < l_etapa_ug2 < 17:
            context["ug2_etapa"] = UNIDADE_PARANDO
        elif 1 < l_etapa_ug2 < 7:
            context["ug2_etapa"] = UNIDADE_SINCRONIZANDO
        elif l_etapa_ug2 == 7:
            context["ug2_etapa"] = UNIDADE_SINCRONIZADA
        else:
            context["ug2_etapa"] = UNIDADE_INCONSISTENTE

    else:
        context["ug2_etapa"] = 999


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

    if context["pot_ug1"] in (usina.ug1_pot, 99) or context["pot_ug2"] in (usina.ug2_pot, 99):
        context["pot_usina"] = f"{usina.ug1_pot + usina.ug2_pot:0.1f}"
    else:
        context["pot_usina"] = f"{pot_ug1 + pot_ug2:0.1f}"

    return render(request, "monitoramento.html", context=context)
