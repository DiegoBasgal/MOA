import csv
import json
import math
import os

from numpy import random
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import ModbusServer, DataBank
import threading
from datetime import datetime
from time import sleep
import logging

logger = logging.getLogger('__main__')

USINA_CAP_RESERVATORIO = 43000.0
USINA_NV_MAX = 643.5
USINA_NV_MIN = 643.0
USINA_VAZAO_SANITARIA_COTA = 641

TRIP_NV_MIN = 643.0
TRIP_TENSAO_SUPERIOR = 36200
TRIP_TENSAO_ABAIXO = 31050

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


class world_abstraction(threading.Thread):

    def __init__(self, simulation_speed=1):
        super().__init__()

        config_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'config.json')
        with open(config_file, 'r') as file:
            self.cfg = json.load(file)
        self.moa_slave = ModbusClient(host=self.cfg['moa_slave_ip'], port=self.cfg['moa_slave_porta'])
        self.REGS = []
        self.tensao_na_linha = 34500
        self.comp_aberta = 0
        self.comp_fechada = 0
        self.comp_flags = 0
        self.comp_p1 = 0
        self.comp_p2 = 0
        self.comp_p3 = 0
        self.comp_p4 = 0
        self.flags_usina = 0
        self.volume = 0
        self.nv_montante = 643.25 # MUDAR AQUI
        for aux in range(250000):
            self.volume = aux
            aux_nv_montante = -0.0000000002 * ((self.volume / 1000) ** 4) + 0.0000002 * ((self.volume / 1000) ** 3) - 0.0001 * (
                    (self.volume / 1000) ** 2) + 0.0331 * (self.volume / 1000) + 639.43
            if round(aux_nv_montante, 3) == round(self.nv_montante, 3):
                logger.info("[SIMUL] Volume res: {}, Nv: {}".format(self.volume, self.nv_montante))
                break
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
        self.step_time = 0.001
        self.seconds_per_step = self.step_time * self.simulation_speed
        self.events = []
        with open('simulated_events.csv') as f:
            d = csv.excel
            d.delimiter = ';'
            for row in csv.reader(f, dialect=d):
                self.events.append(row)
        self.events = self.events[1:]

    def step_ug1(self):
        # Variaveis do ambiente
        self.ug1_temp_mancal = max(self.ug1_temp_mancal, 25) + random.normal(0, 0.01)
        self.ug1_perda_grade = max(self.ug1_perda_grade + random.exponential(scale=0.001) - 0.001, 0)

        if self.ug1_temp_mancal >= 100:
            self.ug1_flags = self.ug1_flags | 2

        if self.ug1_perda_grade >= 3:
            self.ug1_flags = self.ug1_flags | 4

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
            var_ug1_por_minuto = ((self.ug1_setpoint - self.ug1_pot) * 60) / (self.seconds_per_step)
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

        if self.ug2_temp_mancal >= 100:
            self.ug2_flags = self.ug2_flags | 2

        if self.ug2_perda_grade >= 3:
            self.ug2_flags = self.ug2_flags | 4

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
            var_ug2_por_minuto = ((self.ug2_setpoint - self.ug2_pot) * 60 )/ (self.seconds_per_step)
            var_ug2_por_minuto = math.copysign(min(0.625, abs(var_ug2_por_minuto)), var_ug2_por_minuto)
            self.ug2_pot += (var_ug2_por_minuto / 60) * self.seconds_per_step
            self.ug2_pot = min(max(1, self.ug2_pot), 2.6) + random.normal(scale=0.001)
        else:
            # Se estiver desincronizada descer potencia
            self.ug2_pot -= (0.625 / 60) * self.seconds_per_step
            self.ug2_pot = max(0, self.ug2_pot)

    def stop(self):
        self.stop_signal = True
        logger.info("[SIMUL] Soft Stopping thread")

    def run(self):
        server = ModbusServer(host='0.0.0.0', port=5002, no_block=True)
        server.start()
        q_aflu = 0
        q_vert = 0
        DataBank.set_words(40000, [int(((self.nv_montante - 620) * 100 + random.normal(scale=0.1))) * 10])
        logger.info("[SIMUL] Aguardando MOA")
        moa_is_alive = False
        while not moa_is_alive:
            moa_is_alive = self.moa_slave.open()
            sleep(0.01)
        self.moa_slave.close()
        logger.info("[SIMUL] Rodando")
        simul_start_time = datetime.now()

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
            2       tensao         [V]
            
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

            self.REGS = DataBank.get_words(40000, 201)
            self.ug1_flags = (int(self.REGS[20]))
            self.ug1_setpoint = (int(self.REGS[22]) / 1000)
            self.ug2_flags = (int(self.REGS[30]))
            self.ug2_setpoint = (int(self.REGS[32]) / 1000)
            self.comp_flags = self.REGS[10]
            self.comp_p1 = self.REGS[11] & 0b00000010
            self.comp_p2 = self.REGS[11] & 0b00000100
            self.comp_p3 = self.REGS[11] & 0b00001000
            self.comp_p4 = self.REGS[11] & 0b00010000
            self.comp_aberta = self.REGS[11] & 0b00100000
            self.flags_usina = int(self.REGS[100])
            self.trip_painel = int(self.REGS[200])

            # Comportamento fisico

            # Acerto de tempo
            self.simulation_time += self.seconds_per_step
            # Ler eventos
            # ['minuto', 'q_aflu', 'flag_usina', 'disp_ug1', 'temp_ug1', 'perda_ug1', 'disp_ug2', 'temp_ug2', 'perda_ug2']
            if not len(self.events) == 0:
                if self.events[0][0] == "STOP":
                    logger.info("[SIMUL] Executando evento agendado na simulação STOP")
                    DataBank.set_words(41000, [1])
                    self.stop()
                    continue

                if float(self.events[0][0])*60 <= self.simulation_time:
                    current_event = self.events[0]  # hold current
                    for i in range(10):
                        current_event[i] = float(current_event[i])
                    self.events = self.events[1:]   # remove current from list
                    q_aflu = min(max(0, current_event[1]), 100) if current_event[1] >= 0 else q_aflu
                    self.flags_usina = current_event[2] if current_event[2] >= 0 else self.flags_usina
                    self.ug1_flags = current_event[3] if current_event[3] >= 0 else self.ug1_flags
                    self.ug1_temp_mancal = current_event[4] if current_event[4] >= 0 else self.ug1_temp_mancal
                    self.ug1_perda_grade = current_event[5] if current_event[5] >= 0 else self.ug1_perda_grade
                    self.ug2_flags = current_event[6] if current_event[6] >= 0 else self.ug2_flags
                    self.ug2_temp_mancal = current_event[7] if current_event[7] >= 0 else self.ug2_temp_mancal
                    self.ug2_perda_grade = current_event[8] if current_event[8] >= 0 else self.ug2_perda_grade
                    self.tensao_na_linha = current_event[9] if current_event[9] >= 0 else self.tensao_na_linha
                    logger.debug("[SIMUL] Executando evento agendado na simulação {}".format(current_event))

            # Verifica flags da Usina
            if not self.trip_painel == 0:
                self.flags_usina = int(self.flags_usina) | 1

            if not (TRIP_TENSAO_ABAIXO < self.tensao_na_linha < TRIP_TENSAO_SUPERIOR):
                self.flags_usina = int(self.flags_usina) | 2

            if not (TRIP_NV_MIN < self.nv_montante):
                self.flags_usina = int(self.flags_usina) | 4

            if not (self.flags_usina == 0):
                old_flag_ug1 = self.ug1_flags
                old_flag_ug2 = self.ug2_flags
                self.ug1_flags = 1
                self.ug2_flags = 1
                self.step_ug1()  # UG1
                self.step_ug2()  # UG2
                self.ug1_flags = old_flag_ug1
                self.ug2_flags = old_flag_ug2

            # Comportamento das UGs
            self.step_ug1()  # UG1
            self.step_ug2()  # UG2

            # Acerta o medidor
            self.pot_no_medidor = (self.ug1_pot + self.ug2_pot) * max(min(random.normal(0.985, 0.002), 1.005), 0.95)

            # Acerta as Vazoes e o nivel
            q_comp = q_comporta(self.comp_fechada, self.comp_p1, self.comp_p2, self.comp_p3, self.comp_p4, self.comp_aberta, self.nv_montante)
            q_sani = q_sanitaria(self.nv_montante)
            q_turb = q_turbinada(self.ug1_pot, self.ug2_pot)

            q_vert = q_aflu - q_comp - q_sani - q_turb
            q_vert = max(0, q_vert)

            if self.nv_montante <= USINA_NV_MAX or q_vert == 0:
                self.volume += (q_aflu - q_comp - q_sani - q_turb) * self.seconds_per_step
                self.nv_montante = - 0.0000000002 * ((self.volume / 1000) ** 4) + 0.0000002 * (
                            (self.volume / 1000) ** 3) - 0.0001 * ((self.volume / 1000) ** 2) + 0.0331 * (
                                               self.volume / 1000) + 639.43
            else:
                self.nv_montante = USINA_NV_MAX + ((q_vert / ((1.66 + 0.0017336 * q_vert) * 110)) ** (2 / 3))

            if (self.nv_montante < 642.5) or (self.nv_montante > 644.3):
                logger.error("[SIMUL] Algo deu errado e o nv foi apara fora dos limites.")
                logger.error("[SIMUL] vol: {}, q_aflu:{}, q_comp:{}, q_sani:{}, q_turb:{}, q_vert:{},".format(
                    self.volume, q_aflu, q_comp, q_sani, q_turb, q_vert
                ))
                self.stop()

            # Atualiza registradores internos
            DataBank.set_words(40000, [int(((self.nv_montante - 620) * 100 + random.normal(scale=0.1)))*10])
            DataBank.set_words(40001, [int(self.pot_no_medidor*1000)])
            DataBank.set_words(40002, [int(self.tensao_na_linha + random.normal()*10)])
            DataBank.set_words(40020, [self.ug1_flags])
            DataBank.set_words(40021, [int(self.ug1_pot * 1000)])
            DataBank.set_words(40023, [int(self.ug1_minutos)])
            DataBank.set_words(40024, [int(self.ug1_temp_mancal*10)])
            DataBank.set_words(40025, [int(self.ug1_perda_grade*100)])
            DataBank.set_words(40030, [self.ug2_flags])
            DataBank.set_words(40031, [int(self.ug2_pot * 1000)])
            DataBank.set_words(40033, [int(self.ug2_minutos)])
            DataBank.set_words(40034, [int(self.ug2_temp_mancal*10)])
            DataBank.set_words(40035, [int(self.ug2_perda_grade*100)])
            DataBank.set_words(40099, [int(self.simulation_time/60)])
            DataBank.set_words(40100, [self.flags_usina])
            # Final do comportamento modelado

            remaining_step_time = self.step_time - (datetime.now()-step_start_time).seconds
            # print("Remaining time on step {:}s".format(remaining_step_time))

            self.lock.release()
            if remaining_step_time > 0:
                sleep(remaining_step_time)
            else:
                logger.warning("[SIMUL] Step time too low or speed too high!")

        simul_mesured_speed = self.simulation_time/(datetime.now() - simul_start_time).seconds
        logger.info("Simulated with an actual speed of: {:.3f}x".format(simul_mesured_speed))

if __name__ == '__main__':
    th = world_abstraction()
    th.run()
    th.join()