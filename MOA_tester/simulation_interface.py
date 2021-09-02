import csv
import datetime
import logging
import matplotlib.pyplot as plt
import threading
from time import sleep
from pyModbusTCP.server import DataBank

string_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

# SILENCIANDO O LOOGER ROOT
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.CRITICAL)
# Inicializando o logger principal
logger = logging.getLogger('__main__')


class simulation_interface(threading.Thread):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.stop_signal = False
        self.simulation_data_log_path = "logs/log_simulation_data_{}.csv".format(string_date)
        with open(self.simulation_data_log_path, 'w+') as f:
            logger.info("Simulation data is being saved to {}".format(self.simulation_data_log_path))
            header = ["minutos_simulados", "nv_montante", "pot_medidor", "usina_flags", "comporta_flags", "comporta_pos",
                        "ug1_flags", "ug1_pot", "ug1_setpot", "ug1_tempo", "ug1_t_mancal", "ug1_perda_grade",
                        "ug2_flags", "ug2_pot", "ug2_setpot", "ug2_tempo", "ug2_t_mancal", "ug2_perda_grade"]
            writer = csv.writer(f, dialect='excel')
            writer.writerow(header)

        logger.debug("simulation_interface init OK")


    def stop(self):
        self.stop_signal = True

    def run(self):

        with_plot = False
        with_clp_text = True
        show_end_plot = True

        if with_plot:

            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            ax1.plot([0, 10000000], [643.0, 643.0], linestyle='dotted', color='red')
            ax1.plot([0, 10000000], [643.5, 643.5], linestyle='dotted', color='red')
            ax1.plot([0, 10000000], [643.25, 643.25], linestyle='dotted', color='gray')
            ax2.plot([0, 10000000], [5, 5], linestyle='dashed', color='gray')

        rows = []
        while not self.stop_signal:
            try:
                self.lock.acquire()
                REGS = DataBank.get_words(0, 1001)

                nv_montante = (REGS[0] / 1000) + 620
                pot_medidor = REGS[1]
                usina_flags = REGS[100]
                comporta_flags = REGS[10]
                comporta_pos = REGS[11]
                ug1_flags = REGS[20]
                ug1_pot = REGS[21]
                ug1_setpot = REGS[22]
                ug1_tempo = REGS[23]/60
                ug1_t_mancal = REGS[24]/10
                ug1_perda_grade = REGS[25]/100
                ug2_flags = REGS[30]
                ug2_pot = REGS[31]
                ug2_setpot = REGS[32]
                ug2_tempo = REGS[33]/60
                ug2_t_mancal = REGS[34]/10
                ug2_perda_grade = REGS[35]/100
                segundos_simulados = REGS[99]*60

                if REGS[1000]:
                    self.stop()
                    continue

                if len(rows) > 1:
                    if segundos_simulados/60 == rows[-1][0]:
                        sleep(0.001)
                        continue

                rows.append([segundos_simulados/60, nv_montante, pot_medidor/1000, usina_flags, comporta_flags, comporta_pos,
                          ug1_flags, ug1_pot/1000, ug1_setpot, ug1_tempo, ug1_t_mancal, ug1_perda_grade,
                          ug2_flags, ug2_pot/1000, ug2_setpot, ug2_tempo, ug2_t_mancal, ug2_perda_grade])

                with open(self.simulation_data_log_path, 'a') as f:
                    writer = csv.writer(f, dialect='excel')
                    writer.writerow(rows[-1])

                if with_plot:
                    ax1.plot(list(map(list, zip(*rows)))[0], list(map(list, zip(*rows)))[1], color='blue')
                    ax2.plot(list(map(list, zip(*rows)))[0], list(map(list, zip(*rows)))[2], color='orange')
                    ax2.plot(list(map(list, zip(*rows)))[0], list(map(list, zip(*rows)))[7], color='pink', linestyle=':')
                    ax2.plot(list(map(list, zip(*rows)))[0], list(map(list, zip(*rows)))[13], color='khaki', linestyle=':')
                    plt.xlim(0, rows[-1][0])
                    plt.pause(0.05)

                if with_clp_text:
                    print("-----------------------------------------------------------------------------------------------")
                    print("Tempo simulado: {:} | NV montante: {:3.2f}m | Pot Medidor: {:5.0f}kW"
                          .format(str(datetime.timedelta(seconds=segundos_simulados)), nv_montante, pot_medidor))
                    print("Flags Usina: {:08b} | Flags Comporta: {:8b}| Pos Cmporta: {:}"
                          .format(usina_flags, comporta_flags, comporta_pos))
                    print(
                        "UG1 | Flags: {:08b} | Potência: {:5.0f}kW | Setpoint: {:5.0f}kW | Horimetro: {:3.1f}h | Temp Mancal {:3.1f}C | Perda na grade: {:1.2f}m"
                        .format(ug1_flags, ug1_pot, ug1_setpot, ug1_tempo / 60, ug1_t_mancal, ug1_perda_grade))
                    print(
                        "UG2 | Flags: {:08b} | Potência: {:5.0f}kW | Setpoint: {:5.0f}kW | Horimetro: {:3.1f}h | Temp Mancal {:3.1f}C | Perda na grade: {:1.2f}m"
                        .format(ug2_flags, ug2_pot, ug2_setpot, ug2_tempo / 60, ug2_t_mancal, ug2_perda_grade))

            finally:
                self.lock.release()

        # After stop sig
        if show_end_plot:
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            ax1.plot([0, 10000000], [643.0, 643.0], linestyle='dotted', color='red')
            ax1.plot([0, 10000000], [643.5, 643.5], linestyle='dotted', color='red')
            ax1.plot([0, 10000000], [643.25, 643.25], linestyle='dotted', color='gray')
            ax2.plot([0, 10000000], [5, 5], linestyle='dashed', color='gray')
            ax1.plot(list(map(list, zip(*rows)))[0], list(map(list, zip(*rows)))[1], color='blue')
            ax2.plot(list(map(list, zip(*rows)))[0], list(map(list, zip(*rows)))[2], color='orange')
            ax2.plot(list(map(list, zip(*rows)))[0], list(map(list, zip(*rows)))[7], color='pink', linestyle=':')
            ax2.plot(list(map(list, zip(*rows)))[0], list(map(list, zip(*rows)))[13], color='khaki', linestyle=':')
            ax1.set_ylim(642.5, 645.5)
            plt.xlim(0, rows[-1][0])
            plt.show()

        total_error = 0
        for row in rows:
            total_error += abs(float(row[1])-643.25)
        logger.info("Abs error: {:.2f} Abs error/time: {:.5f}".format(total_error, total_error/len(rows)))