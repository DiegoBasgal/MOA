import os
import sys
import datetime

from django.shortcuts import render
from parametros.models import ParametrosUsina

# Create your views here.
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
    
    clp_sa = ModbusClient(
        host="192.168.10.109",
        port=502,
        unit_id=1,
        timeout=0.5
    )
    # leitura_dj_linha = LeituraModbusBit(
    #     clp_sa,
    #     REG_SA["SA_ED_PSA_SE_DISJ_LINHA_FECHADO"]
    # )

    context = {
        "usina": usina,
        "em_acionada": f"{usina.emergencia_acionada}",
        "timestamp": usina.timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
        "setpot_usina": f"{(usina.ug1_setpot + usina.ug2_setpot):1.3f}",
        "setpot_ug1": f"{usina.ug1_setpot:1.3f}",
        "ug1_state": f"{usina.ug1_ultimo_estado}",
        "pot_ug1": f"{usina.ug1_pot:1.3f}",
        "setpot_ug2": f"{usina.ug2_setpot:1.3f}",
        "ug2_state": f"{usina.ug2_ultimo_estado}",
        "pot_ug2": f"{usina.ug2_pot:1.3f}",
        "nv_alvo": f"{usina.nv_alvo:3.2f}",
        "aguardo": "Sim" if usina.aguardando_reservatorio > 0 else "Não",
        "nv_montante": f"{usina.nv_montante:3.2f}",
        "CLP_ON": "ONLINE" if usina.clp_online else "ERRO/OFFLINE",
    }

    if 820.9 <= usina.nv_montante < 821:
        context["tag"] = 0
    elif 820.75 <= usina.nv_montante < 820.9:
        context["tag"] = 1
    elif usina.nv_montante < 820.75 or usina.nv_montante > 821:
        context["tag"] = 2

    # if leitura_dj_linha.valor == 0:
    #     context["status_dj_linha"] = True
    # elif leitura_dj_linha.valor == 1:
    #     context["status_dj_linha"] = False
    # else:
    #     context["status_dj_linha"] = None


    for key in context:
        if context[key] == "" or context[key] == " ":
            context[key] = "-"

    # TODO - adicionar na interface novamente após determinação da Automatic da integração do CLP do MOA no painel

        

    """
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
            hb_detetime = datetime.datetime(
                regs[0], regs[1], regs[2], regs[3], regs[4], regs[5], regs[6] * 1000
            )
            context["hb_datestring"] = hb_detetime.strftime("%d/%m/%Y, %H:%M:%S")
    else:
        context["modbus_status"] = "Sem comunicação (client.open() falhou)"
        """

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
