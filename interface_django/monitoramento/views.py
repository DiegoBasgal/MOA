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
    usina = ParametrosUsina.objects.get(id=1)

    context = {
        "usina": usina,
        "em_acionada": "Sim" if usina.emergencia_acionada else "Não",
        "timestamp": usina.timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
        "setpot_usina": "{:1.3f}".format(usina.ug1_setpot + usina.ug2_setpot + usina.ug3_setpot),
        "setpot_ug1": "{:1.3f}".format(usina.ug1_setpot),
        "pot_ug1": "{:1.3f}".format(usina.ug1_pot),
        "setpot_ug2": "{:1.3f}".format(usina.ug2_setpot),
        "pot_ug2": "{:1.3f}".format(usina.ug2_pot),
        "setpot_ug3": "{:1.3f}".format(usina.ug3_setpot),
        "pot_ug3": "{:1.3f}".format(usina.ug3_pot),
        "nv_alvo": "{:3.2f}".format(usina.nv_alvo),
        "aguardo": "Sim" if usina.aguardando_reservatorio > 0 else "Não",
        "nv_montante": "{:3.2f}".format(usina.nv_montante),
        "CLP_MOA": usina.clp_moa_ip,
        "CLP_Status": "ONLINE" if usina.clp_online else "ERRO/OFFLINE",
    }

    if 405 <= usina.nv_montante <= 405.15:
        context["tag"] = 0
    elif 404.85 < usina.nv_montante < 405:
        context["tag"] = 1
    elif usina.nv_montante <= 404.85 or usina.nv_montante > 405.15:
        context["tag"] = 2

    for key in context:
        if context[key] == "" or context[key] == " ":
            context[key] = "-"

    # Comunicação modbus para verificar se servidor está on
    client = ModbusClient(
        host=usina.modbus_server_ip,
        port=usina.modbus_server_porta,
        timeout=0.5,
        unit_id=1,
        auto_close=True
    )

    client_sa = ModbusClient("192.168.0.50", 502, unit_id=1, timeout=0.5, auto_close=True)
    client_ug1 = ModbusClient("192.168.0.51", 5002, unit_id=1, timeout=0.5, auto_close=True)
    client_ug2 = ModbusClient("192.168.0.52", 5002, unit_id=1, timeout=0.5, auto_close=True)
    client_ug3 = ModbusClient("192.168.0.53", 503, unit_id=1, timeout=0.5, auto_close=True)

    if client_sa.open():
        reg_dj = client_sa.read_coils(17)[0]
        if reg_dj == 0:
            context["status_dj52l"] = True
        elif reg_dj == 1:
            context["status_dj52l"] = False
        else:
            context["status_dj52l"] = None

    if client.open():
        regs = client.read_holding_registers(0, 120)
        if regs is None or regs[0] < 2000:
            context["ug1_state", "ug2_state", "ug3_state", "ug1_etapa", "ug2_etapa", "ug3_etapa"] = 99

        else:
            context["ug1_state"] = MOA_DICT_DE_STATES[regs[61]] if regs[61] in MOA_DICT_DE_STATES else 4
            context["ug2_state"] = MOA_DICT_DE_STATES[regs[71]] if regs[71] in MOA_DICT_DE_STATES else 4
            context["ug3_state"] = MOA_DICT_DE_STATES[regs[81]] if regs[81] in MOA_DICT_DE_STATES else 4
            context["ug1_etapa"] = UNIDADE_DICT_DE_ETAPAS[regs[62]] if regs[62] in UNIDADE_DICT_DE_ETAPAS else 99
            context["ug2_etapa"] = UNIDADE_DICT_DE_ETAPAS[regs[72]] if regs[72] in UNIDADE_DICT_DE_ETAPAS else 99
            context["ug3_etapa"] = UNIDADE_DICT_DE_ETAPAS[regs[82]] if regs[82] in UNIDADE_DICT_DE_ETAPAS else 99
            hb_detetime = datetime.datetime(
                regs[0], regs[1], regs[2], regs[3], regs[4], regs[5], regs[6] * 1000
            )
            context["hb_datestring"] = hb_detetime.strftime("%d/%m/%Y, %H:%M:%S")

        if context["ug1_etapa"] == 99:
            context["ug1_state"] = 4

        if context["ug2_etapa"] == 99:
            context["ug2_state"] = 4

        if context["ug3_etapa"] == 99:
            context["ug3_state"] = 4

    else:
        context["modbus_status"] = "Sem comunicação"

    if client_ug1.open():
        hora = client_ug1.read_input_registers(51)[0]
        minuto = (client_ug1.read_input_registers(52)[0] * (1/60))
        context["tempo_ug1"] = f"{float((hora + 45657.39) + minuto):.2f}"

    if client_ug2.open():
        hora = client_ug2.read_input_registers(51)[0]
        minuto = (client_ug2.read_input_registers(52)[0] * (1/60))
        context["tempo_ug2"] = f"{float((hora + 49376.14) + minuto):.2f}"

    if client_ug3.open():
        hora = client_ug3.read_input_registers(51)[0]
        minuto = (client_ug3.read_input_registers(52)[0] * (1/60))
        context["tempo_ug3"] = f"{float((hora + 49001.22) + minuto):.2f}"


    tempo_desde_moa_comunicando = (
        datetime.datetime.now(usina.timestamp.tzinfo)
        - usina.timestamp
        - datetime.timedelta(hours=3)
    )

    hours = int(tempo_desde_moa_comunicando.seconds // 3600)
    remainder = int(tempo_desde_moa_comunicando.seconds - hours * 3600)
    mins = int(remainder // 60)
    secs = int(remainder - mins * 60)

    context["tempo_desde_moa_comunicando"] = "{} dias, {:02d}:{:02d}:{:02d}".format(
        tempo_desde_moa_comunicando.days, hours, mins, secs
    )

    return render(request, "monitoramento.html", context=context)