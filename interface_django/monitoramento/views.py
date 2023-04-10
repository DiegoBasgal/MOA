import datetime

from django.shortcuts import render
from parametros_moa.models import ParametrosUsina

# Create your views here.
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
UNIDADE_DICT_DE_ETAPAS = {}
UNIDADE_DICT_DE_ETAPAS[UNIDADE_PARADA] = 1
UNIDADE_DICT_DE_ETAPAS[UNIDADE_PARANDO] = 2
UNIDADE_DICT_DE_ETAPAS[UNIDADE_SINCRONIZANDO] = 3
UNIDADE_DICT_DE_ETAPAS[UNIDADE_SINCRONIZADA] = 4


def monitoramento_view(request, *args, **kwargs):

    clp_sa = ModbusClient("192.168.0.50", 5002, unit_id=1, timeout=0.5, auto_close=True)
    clp_tda = ModbusClient("192.168.0.54", 5002, unit_id=1, timeout=0.5, auto_close=True)
    clp_ug1 = ModbusClient("192.168.0.51", 5002, unit_id=1, timeout=0.5, auto_close=True)
    clp_ug2 = ModbusClient("192.168.0.52", 5002, unit_id=1, timeout=0.5, auto_close=True)
    clp_ug3 = ModbusClient("192.168.0.53", 503, unit_id=1, timeout=0.5, auto_close=True)
    clp_moa = ModbusClient("192.168.0.116", 502, timeout=0.5, unit_id=1, auto_close=True)

    usina = ParametrosUsina.objects.get(id=1)

    context = {
        "usina": usina,
        "em_acionada": "Sim" if usina.emergencia_acionada else "Não",
        "timestamp": usina.timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
        "nv_alvo": f"{usina.nv_alvo:3.2f}",
        "aguardo": "Sim" if usina.aguardando_reservatorio > 0 else "Não",
        "CLP_MOA": usina.clp_moa_ip,
    }

    for key in context:
        if context[key] == "" or context[key] == " ":
            context[key] = "-"

    if clp_sa.open():
        reg_dj = clp_sa.read_coils(17)[0]
        setpot_usina = clp_sa.read_input_registers(26)[0]
        context["setpot_usina"] = setpot_usina
        if reg_dj == 0:
            context["status_dj52l"] = True
        elif reg_dj == 1:
            context["status_dj52l"] = False
        else:
            context["status_dj52l"] = None

    if clp_tda.open():
        reg_nv = clp_tda.read_input_registers(12)[0]
        context["nv_montante"] = f"{(reg_nv * 1/10000) + 400:0.2f}"
        if 405 <= reg_nv <= 405.15:
            context["tag"] = 0
        elif 404.85 < reg_nv < 405:
            context["tag"] = 1
        elif reg_nv <= 404.85 or reg_nv > 405.15:
            context["tag"] = 2

    if clp_ug1.open():
        setpoint_ug1 = clp_ug1.read_input_registers(44)[0]
        potencia_ug1 = clp_ug1.read_input_registers(45)[0]
        hora = clp_ug1.read_input_registers(51)[0]
        minuto = (clp_ug1.read_input_registers(52)[0] * (1/60))
        
        res_ug1 = 0
        if clp_ug1.read_coils(0) is not None:
            res_ug1 += 2**0
        elif clp_ug1.read_coils(11) is not None:
            res_ug1 += 2**1
        elif clp_ug1.read_coils(132) is not None:
            res_ug1 += 2**2
        elif clp_ug1.read_coils(133) is not None:
            res_ug1 += 2**3
        
        if res_ug1 == 1:
            context["ug1_etapa"] = UNIDADE_SINCRONIZADA
        elif 2 <= res_ug1 <= 3:
            context["ug1_etapa"] =  UNIDADE_PARANDO
        elif 4 <= res_ug1 <= 7:
            context["ug1_etapa"] =  UNIDADE_PARADA
        elif 8 <= res_ug1 <= 15:
            context["ug1_etapa"] =  UNIDADE_SINCRONIZANDO
        else:
            context["ug1_etapa"] = 99

        context["setpot_ug1"] = setpoint_ug1
        context["pot_ug1"] = potencia_ug1
        context["tempo_ug1"] = f"{float((hora + 45657.39) + minuto):.2f}"

    if clp_ug2.open():
        setpoint_ug2 = clp_ug2.read_input_registers(44)[0]
        potencia_ug2 = clp_ug2.read_input_registers(45)[0]
        hora = clp_ug2.read_input_registers(51)[0]
        minuto = (clp_ug2.read_input_registers(52)[0] * (1/60))

        res_ug2 = 0
        if clp_ug2.read_coils(0) is not None:
            res_ug2 += 2**0
        elif clp_ug2.read_coils(11) is not None:
            res_ug2 += 2**1
        elif clp_ug2.read_coils(132) is not None:
            res_ug2 += 2**2
        elif clp_ug2.read_coils(133) is not None:
            res_ug2 += 2**3
        
        if res_ug2 == 1:
            context["ug2_etapa"] = UNIDADE_SINCRONIZADA
        elif 2 <= res_ug2 <= 3:
            context["ug2_etapa"] =  UNIDADE_PARANDO
        elif 4 <= res_ug2 <= 7:
            context["ug2_etapa"] =  UNIDADE_PARADA
        elif 8 <= res_ug2 <= 15:
            context["ug2_etapa"] =  UNIDADE_SINCRONIZANDO
        else:
            context["ug2_etapa"] = 99

        context["setpot_ug2"] = setpoint_ug2
        context["pot_ug2"] = potencia_ug2
        context["tempo_ug2"] = f"{float((hora + 49376.14) + minuto):.2f}"

    if clp_ug3.open():
        setpoint_ug3 = clp_ug3.read_input_registers(44)[0]
        potencia_ug3 = clp_ug3.read_input_registers(45)[0]
        hora = clp_ug3.read_input_registers(51)[0]
        minuto = (clp_ug3.read_input_registers(52)[0] * (1/60))

        res_ug3 = 0
        if clp_ug3.read_coils(0) is not None:
            res_ug3 += 2**0
        elif clp_ug3.read_coils(11) is not None:
            res_ug3 += 2**1
        elif clp_ug3.read_coils(132) is not None:
            res_ug3 += 2**2
        elif clp_ug3.read_coils(133) is not None:
            res_ug3 += 2**3
        
        if res_ug3 == 1:
            context["ug3_etapa"] = UNIDADE_SINCRONIZADA
        elif 2 <= res_ug3 <= 3:
            context["ug3_etapa"] =  UNIDADE_PARANDO
        elif 4 <= res_ug3 <= 7:
            context["ug3_etapa"] =  UNIDADE_PARADA
        elif 8 <= res_ug3 <= 15:
            context["ug3_etapa"] =  UNIDADE_SINCRONIZANDO
        else:
            context["ug3_etapa"] = 99

        context["setpot_ug3"] = setpoint_ug3
        context["pot_ug3"] = potencia_ug3
        context["tempo_ug3"] = f"{float((hora + 49001.22) + minuto):.2f}"

    if clp_moa.open():
        context["CLP_Status"] = True
        regs = clp_moa.read_holding_registers(0, 120)

        context["ug1_state"] = MOA_DICT_DE_STATES[regs[23]] if regs[23] in MOA_DICT_DE_STATES else 4
        context["ug2_state"] = MOA_DICT_DE_STATES[regs[28]] if regs[28] in MOA_DICT_DE_STATES else 4
        context["ug3_state"] = MOA_DICT_DE_STATES[regs[33]] if regs[33] in MOA_DICT_DE_STATES else 4

        #hb_datetime = datetime.datetime(regs[0], regs[1], regs[2], regs[3], regs[4], regs[5], regs[6] * 1000)
        #context["hb_datestring"] = hb_datetime.strftime("%d/%m/%Y, %H:%M:%S")
    else:
        context["CLP_Status"] = False

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