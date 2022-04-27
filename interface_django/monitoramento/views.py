import datetime

from django.shortcuts import render
from parametros_moa.models import ParametrosUsina


# Create your views here.
from pyModbusTCP.client import ModbusClient

UNIDADE_PARADA = 1
UNIDADE_PRONTA_PARA_GIRO_MECANICO = 2
UNIDADE_EM_VAZIO_DESEXITADA = 4
UNIDADE_PRONTA_PARA_SINCRONISMO = 8
UNIDADE_SINCRONIZADA = 16
DICT_LISTA_DE_ETAPAS = {}
DICT_LISTA_DE_ETAPAS[UNIDADE_PARADA] = "UNIDADE_PARADA"
DICT_LISTA_DE_ETAPAS[UNIDADE_PRONTA_PARA_GIRO_MECANICO] = "UNIDADE_PARADA"
DICT_LISTA_DE_ETAPAS[UNIDADE_EM_VAZIO_DESEXITADA] = "UNIDADE_EM_VAZIO_DESEXITADA"
DICT_LISTA_DE_ETAPAS[UNIDADE_PRONTA_PARA_SINCRONISMO] = "UNIDADE_PRONTA_PARA_SINCRONISMO"
DICT_LISTA_DE_ETAPAS[UNIDADE_SINCRONIZADA] = "UNIDADE_SINCRONIZADA"

def monitoramento_view(request, *args, **kwargs):
    usina = ParametrosUsina.objects.get(id=1)

    context = {
        'usina': usina,
        'estado': "{}".format(usina.status_moa),
        'em_acionada': "{}".format(usina.emergencia_acionada),
        'timestamp': usina.timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
        'setpot_usina': "{:1.3f}".format(usina.ug1_setpot + usina.ug2_setpot),
        'setpot_ug1': "{:1.3f}".format(usina.ug1_setpot),
        'pot_ug1': "{:1.3f}".format(usina.ug1_pot),
        'tempo_ug1': "{:d}".format(usina.ug1_tempo),
        'setpot_ug2': "{:1.3f}".format(usina.ug2_setpot),
        'pot_ug2': "{:1.3f}".format(usina.ug2_pot),
        'tempo_ug2': "{:d}".format(usina.ug2_tempo),
        'nv_alvo': "{:3.2f}".format(usina.nv_alvo),
        'aguardo': "Sim" if usina.aguardando_reservatorio > 0 else "Não",
        'nv_montante': "{:3.2f}".format(usina.nv_montante),
        'LOCAL_MODBUS_PORT': usina.modbus_server_porta,
        'CLP_IP': usina.clp_ip,
        'CLP_ON': "ONLINE" if usina.clp_online else "ERRO/OFFLINE",}

    # Comunicação modbus para verificar se servidor está on
    client = ModbusClient(host='127.0.0.1', port=usina.modbus_server_porta, timeout=5, unit_id=1)
    if client.open():
        regs = client.read_holding_registers(0, 120)
        client.close()
        if regs is None or regs[0] < 2000:
            context['modbus_status'] = "Sem comunicação (regs is None)"
        else:
            context['modbus_status'] = 'Ok!'
            context['ug1_state'] = str(DICT_LISTA_DE_ETAPAS[regs[61]] if regs[61] in DICT_LISTA_DE_ETAPAS else "INCONSISTENTE")
            context['ug2_state'] = str(DICT_LISTA_DE_ETAPAS[regs[71]] if regs[71] in DICT_LISTA_DE_ETAPAS else "INCONSISTENTE")
            hb_detetime = datetime.datetime(regs[0], regs[1], regs[2], regs[3], regs[4], regs[5], regs[6]*1000)
            context['hb_datestring'] = hb_detetime.strftime("%d/%m/%Y, %H:%M:%S")
    else:
        context['modbus_status'] = "Sem comunicação (client.open() falhou)"

    tempo_desde_moa_comunicando = datetime.datetime.now(usina.timestamp.tzinfo) - usina.timestamp - datetime.timedelta(hours=3)

    hours = int(tempo_desde_moa_comunicando.seconds // 3600)
    remainder = int(tempo_desde_moa_comunicando.seconds - hours * 3600)
    mins = int(remainder // 60)
    secs = int(remainder - mins * 60)

    context['tempo_desde_moa_comunicando'] = "{} dias, {:02d}:{:02d}:{:02d}".format(tempo_desde_moa_comunicando.days,
                                                                         hours, mins, secs)

    return render(request, 'monitoramento.html', context=context)