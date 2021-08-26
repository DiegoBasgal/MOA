import math
from numpy import random

from pyModbusTCP.server import ModbusServer, DataBank
import signal
import threading
from datetime import datetime
from time import sleep
import logging
from sys import stdout
from src.mensageiro.mensageiro_log_handler import MensageiroHandler

string_date = datetime.now().strftime("%Y-%m-%d_%H-%M")

# SILENCIANDO O LOOGER ROOT
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.CRITICAL)
# Inicializando o logger principal
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("logs/{}-test.log".format(string_date))  # log para arquivo
ch = logging.StreamHandler(stdout)  # log para linha de comando
mh = MensageiroHandler()  # log para telegram e voip
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logFormatterSimples = logging.Formatter("[%(levelname)-5.5s]  %(message)s")
fh.setFormatter(logFormatter)
ch.setFormatter(logFormatter)
mh.setFormatter(logFormatterSimples)
fh.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)
mh.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(mh)

USINA_CAP_RESERVATORIO = 43000.0
USINA_NV_MAX = 643.5
USINA_NV_MIN = 643.0
USINA_VAZAO_SANITARIA_COTA = 641


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
        resultado = 3 * h * math.sqrt(19.62*(montante-636.5))
    else:
        resultado = 0

    return resultado


def q_sanitaria(nv):

        temp = (nv-USINA_VAZAO_SANITARIA_COTA) if nv > USINA_VAZAO_SANITARIA_COTA else 0
        return 0.07474 * math.sqrt(19.62*temp)      # vazao


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


class world_abstraction(threading.Thread):

    def __init__(self, simulation_speed=1):
        super().__init__()   
        self.REGS = []
        self.comp_aberta = 0
        self.comp_fechada = 0
        self.comp_flags = 0
        self.comp_p1 = 0
        self.comp_p2 = 0
        self.comp_p3 = 0
        self.comp_p4 = 0
        self.flags_usina = 0
        self.volume = 175000
        self.nv_montante = - 0.0000000002 * ((self.volume / 1000) ** 4) + 0.0000002 * ((self.volume / 1000) ** 3) - 0.0001 * (
                    (self.volume / 1000) ** 2) + 0.0331 * (self.volume / 1000) + 639.43
        self.pot_no_medidor = 0
        self.simulation_speed = simulation_speed
        self.simulation_time = 0
        self.ug1_sinc = 0
        self.ug2_sinc = 0
        self.ug1_flags = 0
        self.ug1_minutos = 0
        self.ug1_perda_grade = 0
        self.ug1_pot = 0
        self.ug1_setpoint = 0
        self.ug1_temp_mancal = 25
        self.ug2_flags = 0
        self.ug2_minutos = 0
        self.ug2_perda_grade = 0
        self.ug2_pot = 0
        self.ug2_setpoint = 0
        self.ug2_temp_mancal = 25
        self.lock = threading.Lock()
        self.stop_signal = False
        self.simulation_speed = max(self.simulation_speed, 1)
        self.simulation_speed = min(self.simulation_speed, 240)
        self.step_time = 0.1
        self.seconds_per_step = self.step_time * self.simulation_speed

    def step_ug1(self):
        # Variaveis do ambiente
        self.ug1_temp_mancal = max(self.ug1_temp_mancal, 25) + random.normal(0, 0.01)
        self.ug1_perda_grade = max(self.ug1_perda_grade + random.exponential(scale=0.001) - 0.001, 0)

        # Tratar flag da UG
        if not (self.ug1_flags == 0):
            self.ug1_setpoint = 0
            self.ug1_sinc = 0
            self.ug1_pot = 0

        # Tratar Sincronismo
        if self.ug1_setpoint >= 1:
            # Sincronizar com a rede
            self.ug1_sinc += (self.seconds_per_step / 60) / 5  # 5 minutos 
        else:
            # Remover da rede
            self.ug1_sinc -= (self.seconds_per_step / 60) / 1  # 1 minuto 

        # Limitar o sincronismo de 0% a 100%
        self.ug1_sinc = max(min(self.ug1_sinc, 1), 0)

        # Acertar tempo de operação da UG
        if self.ug1_sinc > 0.5:
            self.ug1_minutos += self.seconds_per_step / 60

        # Acertar potência na UG
        if self.ug1_sinc >= 1:
            # Se estiver sincronizada subir/ajustar potencia
            var_ug1_por_minuto = (self.ug1_setpoint - self.ug1_pot) / (self.seconds_per_step / 60)
            var_ug1_por_minuto = math.copysign(min(0.625, abs(var_ug1_por_minuto)), var_ug1_por_minuto)
            self.ug1_pot += (var_ug1_por_minuto / 60) * self.seconds_per_step
            self.ug1_pot = min(max(1, self.ug1_pot), 2.6) + random.normal(scale=0.001)
        else:
            # Se estiver desincronizada descer potencia
            self.ug1_pot -= (0.625 / 60) * self.seconds_per_step
            self.ug1_pot = max(0, self.ug1_pot)
            
    def step_ug2(self):
        # Variaveis do ambiente
        self.ug2_temp_mancal = max(self.ug2_temp_mancal, 25) + random.normal(0, 0.01)
        self.ug2_perda_grade = max(self.ug2_perda_grade + random.exponential(scale=0.001) - 0.001, 0)

        # Tratar flag da UG
        if not (self.ug2_flags == 0):
            self.ug2_setpoint = 0
            self.ug2_sinc = 0
            self.ug2_pot = 0

        # Tratar Sincronismo
        if self.ug2_setpoint >= 1:
            # Sincronizar com a rede
            self.ug2_sinc += (self.seconds_per_step / 60) / 5  # 5 minutos 
        else:
            # Remover da rede
            self.ug2_sinc -= (self.seconds_per_step / 60) / 1  # 1 minuto 

        # Limitar o sincronismo de 0% a 100%
        self.ug2_sinc = max(min(self.ug2_sinc, 1), 0)

        # Acertar tempo de operação da UG
        if self.ug2_sinc > 0.5:
            self.ug2_minutos += self.seconds_per_step / 60

        # Acertar potência na UG
        if self.ug2_sinc >= 1:
            # Se estiver sincronizada subir/ajustar potencia
            var_ug2_por_minuto = (self.ug2_setpoint - self.ug2_pot) / (self.seconds_per_step / 60)
            var_ug2_por_minuto = math.copysign(min(0.625, abs(var_ug2_por_minuto)), var_ug2_por_minuto)
            self.ug2_pot += (var_ug2_por_minuto / 60) * self.seconds_per_step
            self.ug2_pot = min(max(1, self.ug2_pot), 2.6) + random.normal(scale=0.001)
        else:
            # Se estiver desincronizada descer potencia
            self.ug2_pot -= (0.625 / 60) * self.seconds_per_step
            self.ug2_pot = max(0, self.ug2_pot)

    def stop(self):
        self.stop_signal = True
    
    def run(self):

        while not self.stop_signal:

            remaining_step_time = 0

            step_start_time = datetime.now()
            self.lock.acquire()

            # Comportamento do modelo

            # Lê registradores internos conforme mapa
            """
            Detalhamento dos conteúdos dos registradores

            REGS    Descrição 
                        
            0       nivel_montante  [620 + X mm]
            1       medidor         [kW]
            
            10      comporta flags  [raw]
            11      comporta pos    [0:fechada, 1:pos1: 2:pos2, 3:pos3, 4:pos4, 5:aberta]
            
            20      UG 1 Flags      [raw]
            21      UG 1 Potência   [kW]
            22      UG 1 Setpoint   [kW]
            23      UG 1 Tempo      [min]
            24      UG 1 T Mancal   [C*100]
            25      UG 1 Perda grd  [m*100]
            
            30      UG 2 Flags      [raw]
            31      UG 2 Potência   [kW]
            32      UG 2 Setpoint   [kW]
            33      UG 2 Tempo      [min]
            34      UG 2 T Mancal   [C*10]
            35      UG 2 Perda grd  [m*100]
            
            99      Minutos simul   [minutos]   
            100     Usina Flags     [raw]   
            """

            self.REGS = DataBank.get_words(0, 101)
            self.ug1_flags = (int(self.REGS[20]))
            self.ug1_setpoint = (int(self.REGS[22]) / 1000)
            self.ug2_flags = (int(self.REGS[30]))
            self.ug2_setpoint = (int(self.REGS[32]) / 1000)
            self.comp_flags = self.REGS[10]
            self.comp_fechada = self.REGS[11] & 0b00000001
            self.comp_p1 = self.REGS[11] & 0b00000010
            self.comp_p2 = self.REGS[11] & 0b00000100
            self.comp_p3 = self.REGS[11] & 0b00001000
            self.comp_p4 = self.REGS[11] & 0b00010000
            self.comp_aberta = self.REGS[11] & 0b00100000
            self.flags_usina = int(self.REGS[100])

            # Comportamento fisico

            # Acerto de tempo
            self.simulation_time += self.seconds_per_step

            # Verifica flags da Usina
            if not (self.flags_usina == 0):
                self.ug1_flags = 1
                self.ug2_flags = 1

            # Comportamento das UGs
            self.step_ug1()  # UG1
            self.step_ug2()  # UG2

            # Acerta o medidor
            self.pot_no_medidor = (self.ug1_pot + self.ug2_pot) * max(min(random.normal(0.985, 0.002), 1.005), 0.95)

            # Acerta as Vazoes e o nivel
            q_aflu = 10 # Todo Adicionar de onde vem esse valor conforme o tempo passa
            q_vert = q_vertimento(self.nv_montante)
            q_comp = q_comporta(self.comp_fechada, self.comp_p1, self.comp_p2, self.comp_p3, self.comp_p4, self.comp_aberta, self.nv_montante)
            q_sani = q_sanitaria(self.nv_montante)
            q_turb = q_turbinada(self.ug1_pot, self.ug2_pot)
            q_eflu = q_vert + q_comp + q_sani + q_turb
            q_liquida = q_aflu - q_eflu
            self.volume += q_liquida * self.seconds_per_step
            if self.volume < 0:
                self.volume = 0
                self.stop()
            self.nv_montante = 0.0000000002 * ((self.volume / 1000) ** 4) + 0.0000002 * ((self.volume / 1000) ** 3) - 0.0001 * ( (self.volume / 1000) ** 2) + 0.0331 * (self.volume / 1000) + 639.43

            if (self.nv_montante < 642.5) or (self.nv_montante > 644.3):
                logger.error("Algo deu errado e o nv foi apara fora dos limites.")
                logger.error("q_aflu:{}, q_vert:{}, q_comp:{}, q_sani:{}, q_turb:{}, q_eflu:{}, q_liq:{},".format(
                    self.q_aflu, q_vert, q_comp, q_sani, q_turb, q_eflu, q_liquida
                ))
                self.stop()

            # Atualiza registradores internos
            DataBank.set_words(0, [int(((self.nv_montante - 620) * 100 + random.normal(scale=0.5)))*10])
            DataBank.set_words(1, [int(self.pot_no_medidor*1000)])
            DataBank.set_words(21, [int(self.ug1_pot * 1000)])
            DataBank.set_words(23, [int(self.ug1_minutos)])
            DataBank.set_words(24, [int(self.ug1_temp_mancal*10)])
            DataBank.set_words(25, [int(self.ug1_perda_grade*100)])
            DataBank.set_words(31, [int(self.ug2_pot * 1000)])
            DataBank.set_words(33, [int(self.ug2_minutos)])
            DataBank.set_words(34, [int(self.ug2_temp_mancal*10)])
            DataBank.set_words(35, [int(self.ug2_perda_grade*100)])
            DataBank.set_words(99, [int(self.simulation_time/60)])
            # Final do comportamento modelado

            remaining_step_time = (datetime.now()-step_start_time).microseconds/1000
            # print("Remaining time on step {:}s".format(remaining_step_time))
            self.lock.release()

            if remaining_step_time > 0:
                sleep(remaining_step_time)

