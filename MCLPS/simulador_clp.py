# Import site é necessário para funcionar fora da IDE devido a necessidade de adicionar o diretório ao PATH
import site
from numpy import random
site.addsitedir('..')

from datetime import datetime
from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
import curses
import math
import MCLPS.CLP_config as CLPconfig
import MCLPS.connector_db as db
import logging
import matplotlib.pyplot as plt
import threading
import os

'''
    Simulador de CLP com comunicação Modbus
'''

# Constantes
ESCALA_DE_TEMPO = 6

PLOTAR_GRAFICO_DEBBUG = True

USINA_CAP_RESERVATORIO = 43000.0
USINA_NV_MAX = 643.5
USINA_NV_MIN = 643.0
USINA_VAZAO_SANITARIA_COTA = 641


# +-------------------------------------------------------------------------------------------------------------------+
# | Comportamento do reservatório                                                                                     |
# +-------------------------------------------------------------------------------------------------------------------+
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


def plotar_debug():
    fp = open('debug.out', 'w')
    fp.write("")
    fp.close()
    sleep(0.5)

    limite_t = 24

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Tempo decorrido na simulação (h)')
    ax1.set_ylabel('Nível montante (m)', color='blue')
    ax1.axis([0, limite_t, 642.95, 643.75])

    ax3 = ax1.twinx()
    ax3.set_ylabel('Vazão Afluente (m³/s)', color='Green')
    ax3.axis([0, limite_t, 0, 30])
    ax3.spines['right'].set_position(('outward', 60))
    ax3.xaxis.set_ticks([])

    ax2 = ax1.twinx()
    ax2.set_ylabel('Potências (MW)', color='Red')
    ax2.axis([0, limite_t, 0, 5])

    ax1.axhline(y=643.50, color="black", linestyle="--")
    ax1.axhline(y=643.25, color="gray", linestyle=":")
    ax1.axhline(y=643.00, color="black", linestyle="--")

    plt.title("MOA - Simulação do comportamento")
    plt.xticks(range(0, limite_t+1, 1))

    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    # segundos_simulados, q_afluente, nv_montante, ug1_pot, ug2_pot

    t_sim = [0]
    nv_m = [0]
    q_aflu = [0]
    pot1 = [0]
    pot2 = [0]
    pott = [0]
    setpoint = [0]

    primeira_vez = True

    while True:
        aux = False
        while not aux:
            fp = open('debug.out', 'r')
            aux = fp.readline()
            fp.close()
            sleep(0.1)
        if aux:
            aux = aux.split()[:]
            for a in range(len(aux)):
                aux[a] = float(aux[a])
            t_sim.append(int(aux[0])/3600)
            q_aflu.append(aux[1])
            nv_m.append(round(aux[2], 3))
            pot1.append(aux[3])
            pot2.append(aux[4])
            pott.append(aux[3] + aux[4])
            setpoint.append(aux[5])

        if t_sim[-1] >= limite_t:
            ax1.axis([t_sim[-1] - limite_t, t_sim[-1], 642.95, 643.75])
            ax2.axis([t_sim[-1] - limite_t, t_sim[-1], 0, 5])
            ax3.axis([t_sim[-1] - limite_t, t_sim[-1], 0, 30])

        linha1, = ax1.plot(t_sim, nv_m, label='Nível montante', color='blue')
        linha5, = ax3.plot(t_sim, q_aflu, label='Afluente', color='green')

        linha4, = ax2.plot(t_sim, pott, label='Potência total', color='red', linestyle=":")

        linha2, = ax2.plot(t_sim, pot1, label='Potência UG1', color='orange', linestyle="--")
        linha3, = ax2.plot(t_sim, pot2, label='Potência UG2', color='yellow', linestyle="--")

        linha6, = ax2.plot(t_sim, setpoint, label='SetPoint', color='purple', linestyle=":")
        if primeira_vez:
            #plt.legend(handles=[linha1, linha5, linha2, linha3, linha4, linha6], loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)
            plt.legend(handles=[linha1, linha5, linha2, linha3, linha4], loc='upper center',  bbox_to_anchor=(0.5, -0.075), ncol=5)

        # print(t_sim)
        # print("running...")

        plt.pause(0.5)
        primeira_vez = False

        if t_sim[-1] >= limite_t:
            figtitle = "resultados/plot_{}_{}.png".format(int(t_sim[-1]), datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
            plt.savefig(figtitle)
            exit()


class ComportamentoReal:
    
    run_cr = True
    flags_usina = 0
    q_aflu = 5.8623152  # 1UG@1,5MW + SANI@1/2NVMAX
    ug1_flags = 0
    ug1_minutos = 0
    ug1_perda_grade = 0
    ug1_pot = 0
    ug1_setpoint = 0
    ug1_sinc = 0
    ug1_temp_mancal = 0
    ug2_flags = 0
    ug2_flags = 0
    ug2_minutos = 0
    ug2_perda_grade = 0
    ug2_pot = 0
    ug2_setpoint = 0
    ug2_sinc = 0
    ug2_temp_mancal = 0
    volume = 192300
    segundos_simulados = 0
    comp_flags = 0
    comp_fechada = 0
    comp_p1 = 0
    comp_p2 = 0
    comp_p3 = 0
    comp_p4 = 0
    comp_aberta = 0
    rodando = 0
    tick = 0
    pot_no_medidor = 0

    def __init__(self):

        self.run_cr = True
        self.flags_usina = 0
        self.q_aflu = 5.8623152  # 1UG@1,5MW + SANI@1/2NVMAX
        self.ug1_flags = 0
        self.ug1_minutos = 0
        self.ug1_perda_grade = 0
        self.ug1_pot = 0
        self.ug1_setpoint = 0
        self.ug1_sinc = 0
        self.ug1_temp_mancal = 0
        self.ug2_flags = 0
        self.ug2_flags = 0
        self.ug2_minutos = 0
        self.ug2_perda_grade = 0
        self.ug2_pot = 0
        self.ug2_setpoint = 0
        self.ug2_sinc = 0
        self.ug2_temp_mancal = 0
        self.volume = 192300
        self.segundos_simulados = 0
        self.atualiza_nv_montante()

    def atualiza_nv_montante(self):
        nv = - 0.0000000002 * ((self.volume / 1000) ** 4) + 0.0000002 * ((self.volume / 1000) ** 3) - 0.0001 * (
                    (self.volume / 1000) ** 2) + 0.0331 * (self.volume / 1000) + 639.43
        self.nv_montante = nv
        return nv


    def comportamento_real(self):

        logger.info("Comportamento rodando")
        try:
            amostras = db.get_amostras_afluente()
        except Exception as e:
            logger.critical(e)
            exit(-1)

        while self.run_cr:

            t0 = datetime.now()
            t1 = datetime.now()
            self.segundos_simulados = 0
            segundos_simulados_ant = 0

            a = 0
            while a in range(len(amostras) - 1) and self.run_cr:

                '''
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
                        
                        100     Usina Flags     [raw]   

                    '''


                ###################
                # Entradas da CLP #
                ###################

                REGS = DataBank.get_words(0, 101)
                self.ug1_flags = (int(REGS[20]))
                self.ug1_setpoint = (int(REGS[22]) / 1000)
                self.ug2_flags = (int(REGS[30]))
                self.ug2_setpoint = (int(REGS[32]) / 1000)
                self.comp_flags = REGS[10]
                self.comp_fechada = REGS[11] & 0b00000001
                self.comp_p1 = REGS[11] & 0b00000010
                self.comp_p2 = REGS[11] & 0b00000100
                self.comp_p3 = REGS[11] & 0b00001000
                self.comp_p4 = REGS[11] & 0b00010000
                self.comp_aberta = REGS[11] & 0b00100000
                self.flags_usina = int(REGS[100])

                #################
                # Saidas da CLP #
                #################

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

                # acerto de tempo


                segundos_reais = (datetime.now()-t0).total_seconds()
                segundos_simulados_ant = self.segundos_simulados
                self.segundos_simulados = segundos_reais * ESCALA_DE_TEMPO
                delta_t_sim = self.segundos_simulados - segundos_simulados_ant
                sleep(0.001)  # tick

                if self.rodando <= 2:
                    self.rodando += 1
                else:
                    self.rodando = 1

                self.tick += 1

                if (amostras[a][0] - amostras[0][0]).total_seconds() < self.segundos_simulados:
                    a += 1
                    t_c = (datetime.now() - t1).total_seconds()
                    t_a = (amostras[a + 1][0] - amostras[a][0]).total_seconds()
                    if t_c > 0:
                        logger.debug("Escala da simulação: {:2.3f}".format(t_a / t_c))
                    t1 = datetime.now()

                else:

                    # Ciclo da simulação
                    self.ug1_temp_mancal = max(self.ug1_temp_mancal, 25) + random.normal(0, 0.01)
                    self.ug2_temp_mancal = max(self.ug2_temp_mancal, 25) + random.normal(0, 0.01)

                    self.ug1_perda_grade = max(self.ug1_perda_grade + random.exponential(scale=0.001) - 0.001, 0)
                    self.ug2_perda_grade = max(self.ug2_perda_grade + random.exponential(scale=0.001) - 0.001, 0)

                    # Acerta as UGS
                    if self.flags_usina >= 1:
                        self.ug1_setpoint = 0
                        self.ug1_sinc = 0
                        self.ug2_setpoint = 0
                        self.ug2_sinc = 0
                        # print("ALERTOU NA CLP! {}".format(self.flags_usina))

                    if self.ug1_flags > 0:
                        self.ug1_setpoint = 0
                        self.ug1_sinc = 0
                        # print("ALERTOU NA CLP! UG1 {}".format(self.ug1_flags))

                    if self.ug2_flags > 0:
                        self.ug2_setpoint = 0
                        self.ug2_sinc = 0
                        # print("ALERTOU NA CLP! UG2 {}".format(self.ug2_flags))

                    #ug1

                    if self.ug1_setpoint >= 1:
                        self.ug1_sinc += 0.2 * (delta_t_sim / 60)
                        if self.ug1_sinc >= 1:
                            self.ug1_sinc = 1
                            var_ug1_por_minuto = (self.ug1_setpoint - self.ug1_pot) / (delta_t_sim / 60)
                            var_ug1_por_minuto = math.copysign(min(0.625, abs(var_ug1_por_minuto)), var_ug1_por_minuto)
                            self.ug1_pot += (var_ug1_por_minuto / 60) * delta_t_sim
                            self.ug1_pot = min(max(1, self.ug1_pot), 2.6) + random.normal(scale=0.001)
                        else:
                            pass

                    else:
                        self.ug1_sinc -= 0.5 * (delta_t_sim / 60)
                        self.ug1_sinc = max(self.ug1_sinc, 0)
                        self.ug1_pot -= (0.625 / 60) * delta_t_sim
                        self.ug1_pot = max(0, self.ug1_pot)

                    if self.ug1_sinc > 0.5:
                        self.ug1_minutos += delta_t_sim/60

                    #ug2
                    if self.ug2_setpoint >= 1:
                        self.ug2_sinc += 0.2 * (delta_t_sim / 60)
                        if self.ug2_sinc >= 1:
                            self.ug2_sinc = 1
                            var_ug2_por_minuto = (self.ug2_setpoint - self.ug2_pot) / (delta_t_sim / 60)
                            var_ug2_por_minuto = math.copysign(min(0.625, abs(var_ug2_por_minuto)), var_ug2_por_minuto)
                            self.ug2_pot += (var_ug2_por_minuto / 60) * delta_t_sim
                            self.ug2_pot = min(max(1, self.ug2_pot), 2.6) + random.normal(scale=0.001)
                        else:
                            pass
                    else:
                        self.ug2_sinc -= 0.5 * (delta_t_sim / 60)
                        self.ug2_sinc = max(self.ug2_sinc, 0)
                        self.ug2_pot -= (0.625 / 60) * delta_t_sim
                        self.ug2_pot = max(0, self.ug2_pot)

                    if self.ug2_sinc > 0.5:
                        self.ug2_minutos += delta_t_sim/60

                    # Acerta o medidor
                    self.pot_no_medidor = (self.ug1_pot + self.ug2_pot)*max(min(random.normal(0.985, 0.002), 1.005), 0.95)

                    # TODO Acerta as Vazoes
                    self.q_aflu = amostras[a][1]
                    q_vert = q_vertimento(self.nv_montante)
                    q_comp = q_comporta(self.comp_fechada, self.comp_p1, self.comp_p2, self.comp_p3, self.comp_p4,
                                              self.comp_aberta, self.nv_montante)
                    q_sani = q_sanitaria(self.nv_montante)
                    q_turb = q_turbinada(self.ug1_pot, self.ug2_pot)
                    q_eflu = q_vert + q_comp + q_sani + q_turb
                    q_liquida = self.q_aflu - q_eflu

                    # Acerta o NV
                    self.volume += q_liquida * delta_t_sim
                    if self.volume < 0:
                        self.volume = 0
                    self.atualiza_nv_montante()

                    if (self.nv_montante < 642.5) or (self.nv_montante > 644.3) :
                        logger.error("Algo deu errado e o nv foi apra fora dos limites.")
                        logger.error("q_aflu:{}, q_vert:{}, q_comp:{}, q_sani:{}, q_turb:{}, q_eflu:{}, q_liq:{},".format(
                            self.q_aflu, q_vert, q_comp, q_sani, q_turb, q_eflu, q_liquida
                        ))
                        raise Exception

                    # print("Simulando...")

                    # para grafico de debbug
                    if PLOTAR_GRAFICO_DEBBUG:
                        fp = open('debug.out', 'w+')
                        fp.write("{:15.0f} {:5.5f} {:5.5f} {:5.5f} {:5.5f} {:5.5f}\n".format(self.segundos_simulados,  self.q_aflu, self.nv_montante, self.ug1_pot,
                                                                                     self.ug2_pot, self.ug1_setpoint+self.ug2_setpoint))
                        fp.close()

                    logger.debug(("{:15.0f};{:5.5f};{:5.5f};{:5.5f};{:5.5f};{:5.5f}\n".format(self.segundos_simulados,  self.q_aflu, self.nv_montante, self.ug1_pot,
                                                                                     self.ug2_pot, self.ug1_setpoint+self.ug2_setpoint)))
            logger.info("Final das amostras")

    def kill(self):
        self.run_cr = False
        print("RUN = ", self.run_cr)



# +-------------------------------------------------------------------------------------------------------------------+
# | MAIN                                                                                                              |
# +-------------------------------------------------------------------------------------------------------------------+
if __name__ == "__main__":

    os.remove('debug.out')

    i = 0
    tempo_inicio = datetime.now()

    cmd = 'mode 120,40'
    os.system(cmd)

    # Inicializando o logging
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # LOG to file
    fileHandler = logging.FileHandler("simulador_clp.log", mode='w+')
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)
    # LOG to console
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    if PLOTAR_GRAFICO_DEBBUG:
        t_plotar_debug = threading.Thread(target=plotar_debug)
        t_plotar_debug.daemon = False
        t_plotar_debug.start()
        sleep(2)

    # Inicialização dos comportamentos
    logger.info("Simulador iniciado. Iniciando Threads")

    cr = ComportamentoReal()
    t_cr = threading.Thread(target=cr.comportamento_real)
    t_cr.daemon = False
    t_cr.start()


    # CLI
    # create a curses object
    stdscr = curses.initscr()
    height, width = stdscr.getmaxyx()  # get the window size

    # define two color pairs, 1- header/footer , 2 - dynamic text, 3 - background, 4- erro
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)

    # Write a header and footer, first write colored strip, then write text
    stdscr.bkgd(curses.color_pair(3))
    stdscr.addstr(0, 0, " " * width, curses.color_pair(1))
    stdscr.addstr(height - 2, 0, " " * (width - 1), curses.color_pair(1))
    stdscr.addstr(height - 1, 0, " " * (width - 1), curses.color_pair(1))
    stdscr.addstr(0, 0, "MCPLS - Módulo controlador lógico programavél simulado - Ritmo Energia 2021", curses.color_pair(1))
    stdscr.addstr(height - 2, 0, " Key Commands :", curses.color_pair(1))
    stdscr.addstr(height - 1, 0, " q - Sair; a - Alterar Q_afluente; d - Alterar Databank; m - Temp. do mancal; g - Perda na grade", curses.color_pair(1))
    stdscr.refresh()


    ########################
    # Interface #
    ########################

    logger.info("Iniciando Comportamento do clp")

    logger.info("Iniciando Servidor/Slave Modbus ")
    ip = CLPconfig.SLAVE_IP
    porta = CLPconfig.SLAVE_PORT
    temporizador = CLPconfig.CLP_REFRESH_RATE

    server = ModbusServer(host=ip, port=porta, no_block=True)
    try:
        server.start()
        while True:

            k = 0
            stdscr.nodelay(True)
            k = stdscr.getch()
            if k == ord('q') or k == ord('Q'):
                curses.endwin()
                raise KeyboardInterrupt

            elif k == ord('a') or k == ord('A'):
                try:
                    valor = 0
                    for k in range(26, height-2):
                        stdscr.addstr(k, 0, " "*width, curses.color_pair(3))
                    stdscr.addstr(26, 0, "Insira o novo valor da vazão afluente (q_aflu) (entre 0 e 1000 m³/s):", curses.color_pair(3))
                    valor = stdscr.getstr()
                    valor = float(valor)
                    valor = min(max(valor, 0), 1000)
                    cr.q_aflu = valor
                    stdscr.addstr(26, 0, " "*width, curses.color_pair(3))
                except Exception as e:
                    stdscr.addstr(26, 0, " "*width, curses.color_pair(4))
                    stdscr.addstr(26, 0, "Erro! {} ".format(e), curses.color_pair(4))

            elif k == ord('d') or k == ord('D'):
                try:
                    valor = 0
                    for k in range(26, height-2):
                        stdscr.addstr(k, 0, " "*width, curses.color_pair(3))
                    stdscr.addstr(26, 0, "Alterar o valor de qual endereço (endereço entre 0 - 65535)? ", curses.color_pair(3))
                    end = stdscr.getstr()
                    end = int(end)
                    if not (0 <= valor <= 65535):
                        stdscr.addstr(26, 0, " " * width, curses.color_pair(4))
                        stdscr.addstr(26, 0, "Operação abortada: Endereço inválido", curses.color_pair(4))
                    stdscr.addstr(27, 0, "Insira o valor a ser escrito no endereço {} (valor entre 0 - 65535): ".format(end), curses.color_pair(3))
                    valor = stdscr.getstr()
                    valor = int(valor)
                    valor = min(max(valor, 0), 65535)
                    DataBank.set_words(end, [valor])
                    stdscr.addstr(26, 0, " "*width, curses.color_pair(3))
                    stdscr.addstr(27, 0, " "*width, curses.color_pair(3))
                except Exception as e:
                    stdscr.addstr(26, 0, " "*width, curses.color_pair(4))
                    stdscr.addstr(26, 0, "Erro! {} ".format(e), curses.color_pair(4))

            elif k == ord('m') or k == ord('M'):
                try:
                    valor = 0
                    for k in range(26, height - 2):
                        stdscr.addstr(k, 0, " " * width, curses.color_pair(3))
                    stdscr.addstr(26, 0, "Inserir a nova temperatura do mancal da UG1 (pressione enter para não alterar): ", curses.color_pair(3))
                    valor = stdscr.getstr()
                    if valor:
                        valor = float(valor)
                        cr.ug1_temp_mancal = valor
                    stdscr.addstr(26, 0, " "*width, curses.color_pair(3))
                    stdscr.addstr(26, 0, "Inserir a nova temperatura do mancal da UG2 (pressione enter para não alterar): ", curses.color_pair(3))
                    valor = stdscr.getstr()
                    if valor:
                        valor = float(valor)
                        cr.ug2_temp_mancal = valor
                    stdscr.addstr(26, 0, " " * width, curses.color_pair(3))
                    stdscr.addstr(27, 0, " " * width, curses.color_pair(3))

                except Exception as e:
                    stdscr.addstr(26, 0, " " * width, curses.color_pair(4))
                    stdscr.addstr(26, 0, "Erro! {} ".format(e), curses.color_pair(4))

            elif k == ord('g') or k == ord('G'):
                try:
                    valor = 0
                    for k in range(26, height - 2):
                        stdscr.addstr(k, 0, " " * width, curses.color_pair(3))
                    stdscr.addstr(26, 0, "Inserir a nova perda da grade da UG1 (pressione enter para não alterar): ", curses.color_pair(3))
                    valor = stdscr.getstr()
                    if valor:
                        valor = float(valor)
                        cr.ug1_perda_grade = valor
                    stdscr.addstr(26, 0, " "*width, curses.color_pair(3))
                    stdscr.addstr(26, 0,  "Inserir a nova perda da grade da UG2 (pressione enter para não alterar): ", curses.color_pair(3))
                    valor = stdscr.getstr()
                    if valor:
                        valor = float(valor)
                        cr.ug2_perda_grade = valor
                    stdscr.addstr(26, 0, " " * width, curses.color_pair(3))
                    stdscr.addstr(27, 0, " " * width, curses.color_pair(3))

                except Exception as e:
                    stdscr.addstr(26, 0, " " * width, curses.color_pair(4))
                    stdscr.addstr(26, 0, "Erro! {} ".format(e), curses.color_pair(4))

            else:
                tempo_real = datetime.now() - tempo_inicio

                texto_rodando = str("  Tempo decorrido: {:.1f} minutos  |  Horas simulas: {:.1f}  |  Tick: {:10d}  |  ".format(tempo_real.seconds/60, cr.segundos_simulados/3600, cr.tick) + "Rodando" + "." * cr.rodando)
                stdscr.addstr(2, 0, " "*width, curses.color_pair(3))
                stdscr.addstr(2, 0, texto_rodando, curses.color_pair(3))
                stdscr.addstr(3, 0, "-"*width, curses.color_pair(3))
                sensor_nv = 620 + (DataBank.get_words(0, 1)[0]/1000)
                stdscr.addstr(4, 0, "  Nível montante: Real:{:3.2f}m Sensor:{:3.2f}m  |  Pot no Medidor: {:5.3f}MW  |  Flags Usina {:^5d}  |  Aflu: {:2.3f}m³/s ".format(cr.nv_montante, sensor_nv, cr.pot_no_medidor, cr.flags_usina, cr.q_aflu), curses.color_pair(3))
                stdscr.addstr(5, 0, "-"*width, curses.color_pair(3))

                estado_comporta_string = "None"
                if bool(cr.comp_fechada):
                    estado_comporta_string = "P0/Fechada"
                elif bool(cr.comp_p1):
                    estado_comporta_string = "P1"
                elif bool(cr.comp_p2):
                    estado_comporta_string = "P2"
                elif bool(cr.comp_p3):
                    estado_comporta_string = "P3"
                elif bool(cr.comp_p4):
                    estado_comporta_string = "P4"
                elif bool(cr.comp_aberta):
                    estado_comporta_string = "P5/Aberta"

                stdscr.addstr(6, 0, "  Comporta: {:10s}  |  Flags:{}".format(estado_comporta_string,cr.comp_flags), curses.color_pair(3))
                stdscr.addstr(7, 0, "-"*width, curses.color_pair(3))
                stdscr.addstr(8, 0, "  UG  |  Potencia  |  Setpoint  |  Flags  |  Sinc  |   T mancal   |  Perda grade  |  Horas-máquina".format(cr.nv_montante, cr.flags_usina), curses.color_pair(3))
                stdscr.addstr(9, 0,
                              "   1  |   {:5.3f}MW  |   {:5.3f}MW  |  {:^5d}  |  {:3.0f}%  |   {:6.1f}°C   |     {:4.2f}m     |      {:.3f}h"
                              .format(cr.ug1_pot, cr.ug1_setpoint, cr.ug1_flags, cr.ug1_sinc * 100, cr.ug1_temp_mancal, cr.ug1_perda_grade,
                                      cr.ug1_minutos/60), curses.color_pair(3))
                stdscr.addstr(10, 0,
                              "   2  |   {:5.3f}MW  |   {:5.3f}MW  |  {:^5d}  |  {:3.0f}%  |   {:6.1f}°C   |     {:4.2f}m     |      {:.3f}h"
                              .format(cr.ug2_pot, cr.ug2_setpoint, cr.ug2_flags, cr.ug2_sinc * 100,  cr.ug2_temp_mancal, cr.ug2_perda_grade,
                                      cr.ug2_minutos/60), curses.color_pair(3))

                stdscr.addstr(11, 0, "-" * width, curses.color_pair(3))
                stdscr.addstr(12, 0, "  Data bank ", curses.color_pair(3))
                stdscr.addstr(13, 0, "-" * width, curses.color_pair(3))
                stdscr.addstr(14, 0, "      :   0     1     2     3     4     5     6     7     8     9   :    "

                              , curses.color_pair(3))

                for j in range(11):
                    stdscr.addstr(15+j, 0, "  {:3d} : {:^5d} {:^5d} {:^5d} {:^5d} {:^5d} {:^5d} {:^5d} {:^5d} {:^5d} {:^5d} : {:<3d}".format(*([j*10]+DataBank.get_words(0+(10*j), 10)+[9+(10*j)])), curses.color_pair(3))
                stdscr.addstr(25, 0, "-"*width, curses.color_pair(3))
                stdscr.addstr(height-3, 0, "DEBUG: Valor entrado: {}".format(k), curses.color_pair(2))

                if not t_cr.is_alive():
                    raise Exception("Erro tread morreu");

                sleep(temporizador)

    except Exception as e:
        logger.error("Erro na execução do CLP: {}".format(e))

    except KeyboardInterrupt as e:
        logger.info("Finalizando por interrupção de teclado ({})".format(e))

    finally:
        curses.endwin()
        logger.info("Finalizando t_cr")
        while t_cr.is_alive():
            cr.kill()
            sleep(2)
        logger.info("Finalizado t_cr")

    input("Pressione enter para sair...")
    logger.info("Final da Main")
