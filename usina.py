import logging
from datetime import datetime
from math import sqrt
import socket
from time import sleep

from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import DataBank, ModbusServer

# CONST
USINA_CAP_RESERVATORIO = 43000.0
USINA_DEPLECAO = 0.5
USINA_GF_MWm = 2.6
USINA_GER_ESTIMADA_MWm = [2.08, 2.25, 1.78, 1.66, 2.42, 3.06, 2.77, 2.73, 2.97, 3.52, 3.2, 2.69]
USINA_GRAVIDADE = 9.8
USINA_NV_MAX = 643.5
USINA_NV_MIN = 643.0
USINA_NV_MONTANTE_INICIAL = 0
USINA_PERMANENCIA = 0.8540
USINA_PESO_ESP_h20 = 988
USINA_POTENCIA_NOMINAL = 5
USINA_POTENCIA_MINIMA_UG = 1.0
USINA_POTENCIA_NOMINAL_UG = 2.5
USINA_QUEDA_BRUTA = 35.30
USINA_QUEDA_LIQUIDA = 34.31
USINA_VAZAO_NOMINAL_MAQ = 8.7
USINA_VAZAO_SANITARIA_COTA = 641
USINA_VAZAO_MAXIMA_TURBINAVEL = 17.4
USINA_MARGEM_POT_CRITICA = 0.5


# Constantes de ganho
Ku = -60
Tu = 600
Kp = Ku/3
Ki = Kp/Tu
Kd = Kp*Tu/13

CLP_SLAVE_IP = "172.21.15.13"
CLP_SLAVE_PORT = 502
E3_SLAVE_IP = "172.21.15.13"
E3_SLAVE_PORT = 503


def q_turbinada(UG1, UG2):

    """
    Retorna o valor da turbinada conforme conforme cálculo preestabelecido
    Cálculo retirado da planilha de excel
    """

    if UG1 > 100:
        UG1 = UG1/1000

    if UG2 > 100:
        UG2 = UG2/1000

    resultado = 0
    if UG1 >= 1.0:
        resultado += (4.50629 * (UG1 ** 10) - 76.41655 * (UG1 ** 9) + 573.2949 * (UG1 ** 8) - 2503.93565 * (
                    UG1 ** 7) + 7045.30229 * (UG1 ** 6) - 13332.41115 * (UG1 ** 5) + 17168.57033 * (
                                  UG1 ** 4) - 14840.58664 * (UG1 ** 3) + 8233.58463 * (
                                  UG1 ** 2) - 2643.3025 * UG1 + 375.46773)
    if UG2 >= 1.0:
        resultado += (4.50629 * (UG2 ** 10) - 76.41655 * (UG2 ** 9) + 573.2949 * (UG2 ** 8) - 2503.93565 * (
                    UG2 ** 7) + 7045.30229 * (UG2 ** 6) - 13332.41115 * (UG2 ** 5) + 17168.57033 * (
                                  UG2 ** 4) - 14840.58664 * (UG2 ** 3) + 8233.58463 * (
                                  UG2 ** 2) - 2643.3025 * UG2 + 375.46773)
    if resultado > 100:
        msg = "Verifique as potências: UG1={}, UG2={}".format(UG1, UG2)
        raise Exception(msg)

    return resultado


def q_vertimento(nv):

    """
    Retorna o valor do vertimento conforme cálculo preestabelecido
    Cálculo retirado da planilha de excel
    """

    resultado = 0
    if nv > USINA_NV_MAX:
        resultado = 2.11 * (0.096006 * ((nv - 643.5) / 2.78) ** 3 - 0.270618 * ((nv - 643.5) / 2.78) ** 2 + 0.386699 * (
                    (nv - 643.5) / 2.78) + 0.783742) * 46.5 * (nv - 643.5) ** 1.5
    return resultado


def q_comporta(fechado, pos1, pos2, pos3, pos4, aberto, montante):

    resultado = 0
    h = 0

    if fechado != 0:
        h = 0
    if pos1 != 0:
        h = 0.050
    if pos2 != 0:
        h = 0.100
    if pos3 != 0:
        h = 0.150
    if pos4 != 0:
        h = 1.500
    if aberto != 0:
        h = 3.000

    if montante >= 636.5:
        resultado = 3 * h * sqrt(19.62*(montante-636.5))
    else:
        resultado = 0

    return resultado


def q_sanitaria(nv):

        temp = (nv-USINA_VAZAO_SANITARIA_COTA) if nv > USINA_VAZAO_SANITARIA_COTA else 0
        return 0.07474 * sqrt(19.62*temp)      # vazao


def q_afluente(tempo, UG1, UG2, nv_mont, nv_mont_ant, pos_comporta):

    """
    Retorna o valor do afluente conforme cálculo preestabelecido
    Cálculo retirado da planilha de excel
    """

    if not isinstance(nv_mont_ant, float):
        return -1

    resultado = 0
    aux = 0

    resultado += q_turbinada(UG1, UG2)
    resultado += q_vertimento(nv_mont)
    resultado += q_sanitaria(nv_mont)
    comp_fechada = pos_comporta & 0b1
    comp_pos1 = pos_comporta & 0b10
    comp_pos2 = pos_comporta & 0b100
    comp_pos3 = pos_comporta & 0b1000
    comp_pos4 = pos_comporta & 0b10000
    comp_aberta = pos_comporta & 0b100000
    resultado += q_comporta(comp_fechada, comp_pos1, comp_pos2, comp_pos3, comp_pos4, comp_aberta, nv_mont)

    if nv_mont > USINA_NV_MAX:
        aux += USINA_NV_MAX
    else:
        aux += nv_mont

    if nv_mont_ant > USINA_NV_MAX:
        aux -= USINA_NV_MAX
    else:
        aux -= nv_mont_ant

    resultado += (aux * ((USINA_CAP_RESERVATORIO / (USINA_NV_MAX - USINA_NV_MIN)) / tempo))

    return resultado


def area_na_cota(nv):
    area = 10000*(1.06*nv - 628.55)
    return area


def q_liquida(delta_t, nv_mont, nv_mont_ant):
    nv_med = (nv_mont + nv_mont_ant)/2
    q_liquida = (nv_mont - nv_mont_ant)*area_na_cota(nv_med)/delta_t
    return q_liquida


def determina_pot(afl, nv):

    if nv <= USINA_NV_MIN:
        return 0

    if nv >= USINA_NV_MAX:
        return USINA_POTENCIA_NOMINAL

    pot_alvo = -0.0032*(afl**4) + 0.0751*(afl**3) - 0.6542*(afl**2) + 2.8849*(afl) - 4.0841

    pot_alvo = max(USINA_POTENCIA_MINIMA_UG, pot_alvo)
    pot_alvo = min(USINA_POTENCIA_NOMINAL, pot_alvo)

    pot_agora = get_pot_ug1() + get_pot_ug2()
    if pot_agora > 0:
        pot_alvo = max(pot_alvo, USINA_POTENCIA_MINIMA_UG)

    return pot_alvo


def get_nv_montante():

    nv_montante_zero = 620  # 620m
    nv_montante_escala = 0.001  # REG[0] retorna em mm

    client = ModbusClient(host=CLP_SLAVE_IP, port=CLP_SLAVE_PORT, timeout=5, unit_id=1)
    if client.open():
        regs = client.read_holding_registers(0, 1)
        client.close()

        if type(regs) != type(None):
            nv_montante = (regs[0] * nv_montante_escala) + nv_montante_zero
            nv_montante = round(nv_montante, 2)

            return nv_montante

    else:
        raise Exception("Erro de comunicação em get_nv_montante, O modbus falhou (CLP).")


def get_pot_ug1():

    client = ModbusClient(host=CLP_SLAVE_IP, port=CLP_SLAVE_PORT, timeout=5, unit_id=1)
    if client.open():
        reg = client.read_holding_registers(8, 1)[0]
        client.close()
        reg = reg/1000
        return reg
    else:
        raise Exception("Erro de comunicação em get_pot_ug1, O modbus falhou (CLP).")


def get_pot_ug2():

    client = ModbusClient(host=CLP_SLAVE_IP, port=CLP_SLAVE_PORT, timeout=5, unit_id=1)
    if client.open():
        reg = client.read_holding_registers(9, 1)[0]
        client.close()
        reg = reg/1000
        return reg
    else:
        raise Exception("Erro de comunicação em get_pot_ug2, O modbus falhou (CLP).")


def get_setpoint_ug1():

    client = ModbusClient(host=CLP_SLAVE_IP, port=CLP_SLAVE_PORT, timeout=5, unit_id=1)
    if client.open():
        reg = client.read_holding_registers(1, 1)[0]
        client.close()
        reg = reg/1000
        return reg
    else:
        raise Exception("Erro de comunicação em get_pot_ug1, O modbus falhou (CLP).")


def get_setpoint_ug2():

    client = ModbusClient(host=CLP_SLAVE_IP, port=CLP_SLAVE_PORT, timeout=5, unit_id=1)
    if client.open():
        reg = client.read_holding_registers(3, 1)[0]
        client.close()
        reg = reg/1000
        return reg
    else:
        raise Exception("Erro de comunicação em get_pot_ug2, O modbus falhou (CLP).")


def get_pos_comporta():

    # ToDo: Adcionar leitura das comportas

    return 0


def set_pot_ug1(pot_alvo):

    if pot_alvo != 0:
        pot_alvo = max(USINA_POTENCIA_MINIMA_UG, pot_alvo)
        pot_alvo = min(USINA_POTENCIA_NOMINAL_UG, pot_alvo)
    client = ModbusClient(host=CLP_SLAVE_IP, port=CLP_SLAVE_PORT, timeout=5, unit_id=1)
    if client.open():
        client.write_single_register(1, int(pot_alvo * 1000))
        client.close()
    else:
        raise Exception("Erro de comunicação em set_pot_ug1, O modbus falhou (CLP).")


def set_pot_ug2(pot_alvo):

    if pot_alvo != 0:
        pot_alvo = max(USINA_POTENCIA_MINIMA_UG, pot_alvo)
        pot_alvo = min(USINA_POTENCIA_NOMINAL_UG, pot_alvo)
    client = ModbusClient(host=CLP_SLAVE_IP, port=CLP_SLAVE_PORT, timeout=5, unit_id=1)
    if client.open():
        client.write_single_register(3, int(pot_alvo * 1000))
        client.close()
    else:
        raise Exception("Erro de comunicação em set_pot_ug2, O modbus falhou (CLP).")


def get_disp_ug1():

    client = ModbusClient(host=CLP_SLAVE_IP, port=CLP_SLAVE_PORT, timeout=5, unit_id=1)
    if client.open():
        ug1_disp = False
        if not client.read_holding_registers(2, 1)[0]:
            ug1_disp = True
        client.close()
        return ug1_disp
    else:
        raise Exception("Erro de comunicação em get_disp_ug1, O modbus falhou (CLP).")

def get_disp_ug2():

    client = ModbusClient(host=CLP_SLAVE_IP, port=CLP_SLAVE_PORT, timeout=5, unit_id=1)
    if client.open():
        ug2_disp = False
        if not client.read_holding_registers(4, 1)[0]:
            ug2_disp = True
        client.close()
        return ug2_disp
    else:
        raise Exception("Erro de comunicação em get_disp_ug2, O modbus falhou (CLP).")


def distribuir_potencia(pot_alvo, erro_nv):

    ug1_sinc = True if get_pot_ug1() >= 1 else False
    ug1_disp = get_disp_ug1()

    ug2_sinc = True if get_pot_ug2() >= 1 else False
    ug2_disp = get_disp_ug2()

    pot_disp = 0
    if ug1_disp:
        pot_disp += 2.5
    if ug2_disp:
        pot_disp += 2.5

    pot_alvo = min(pot_alvo, pot_disp)

    if pot_alvo < USINA_POTENCIA_MINIMA_UG:
        set_pot_ug1(0)
        set_pot_ug2(0)
        return 0

    if not ug1_disp:
        set_pot_ug1(0)

    if not ug2_disp:
        set_pot_ug2(0)

    if ug1_sinc and ug2_sinc:
        if pot_alvo > ((2 * USINA_POTENCIA_MINIMA_UG) + USINA_MARGEM_POT_CRITICA):
            set_pot_ug1(pot_alvo/2)
            set_pot_ug2(pot_alvo/2)
        else:
            if ug1_disp:
                set_pot_ug1(pot_alvo)
                set_pot_ug2(0)
            elif ug2_disp:
                set_pot_ug1(0)
                set_pot_ug2(pot_alvo)
    else:
        if (pot_alvo > (USINA_POTENCIA_NOMINAL_UG + USINA_MARGEM_POT_CRITICA)) and (abs(erro_nv) > 0.05):
            set_pot_ug1(pot_alvo / 2)
            set_pot_ug2(pot_alvo / 2)
        else:
            if ug1_disp:
                set_pot_ug1(pot_alvo)
                set_pot_ug2(0)
            elif ug2_disp:
                set_pot_ug1(0)
                set_pot_ug2(pot_alvo)

def get_q_afluente_debbug():
    client = ModbusClient(host=CLP_SLAVE_IP, port=CLP_SLAVE_PORT, timeout=5, unit_id=1)
    if client.open():
        q = client.read_holding_registers(7, 1)[0]/1000
        client.close()
        return q
    else:
        raise Exception("Erro de comunicação em get_q_afluente_debbug, O modbus falhou (CLP).")


def controle_proporcional(erro_nv):
        return Kp * erro_nv


def controle_integral(erro_nv, ganho_integral_anterior):
    res = (Ki * erro_nv) + ganho_integral_anterior
    res = min(res, 0.8)
    res = max(res, 0)
    return res


def controle_derivativo(erro_nv, erro_nv_anterior):
    return Kd * (erro_nv-erro_nv_anterior)


def heartbeat():

    agora = datetime.now()
    ano = int(agora.year)
    mes = int(agora.month)
    dia = int(agora.day)
    hor = int(agora.hour)
    mnt = int(agora.minute)
    seg = int(agora.second)
    mil = int(agora.microsecond/1000)
    DataBank.set_words(0, [ano, mes, dia, hor, mnt, seg, mil])

def get_nv_alvo():
    zero = 620  # 620m
    escala = 0.001  # REG[0] retorna em mm
    alvo = (DataBank.get_words(10)[0] * escala) + zero
    alvo = round(alvo, 2)
    if not USINA_NV_MIN < alvo < USINA_NV_MAX:
        alvo = (USINA_NV_MIN + USINA_NV_MAX)/2
    return alvo


def get_nv_religamento():
    zero = 620  # 620m
    escala = 0.001  # REG[0] retorna em mm
    alvo = (DataBank.get_words(11)[0] * escala) + zero
    alvo = round(alvo, 2)
    if not USINA_NV_MIN < alvo < USINA_NV_MAX:
        alvo = (USINA_NV_MIN + USINA_NV_MAX)/2
    return alvo


def inicializar():

    logging.info("Iniciando Servidor/Slave Modbus MOA")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = 'localhost'
    finally:
        s.close()
    porta = 5002
    server = ModbusServer(host=local_ip, port=porta, no_block=True)
    while not server.is_run:
        try:
            server.start()
            DataBank.set_words(0, [0] * 0x10000)
            logging.info("Servidor/Slave Modbus MOA Iniciado com sucesso. Endereço: {:}:{:}".format(local_ip, porta))
        except Exception as e:
            logging.error("Erro ao iniciar Modbus MOA: '{:}'. Aguardando 5s e tentando novamente".format(e))
            sleep(5)
            continue
