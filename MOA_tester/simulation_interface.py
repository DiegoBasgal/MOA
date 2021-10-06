import csv
import datetime
import logging
import matplotlib.pyplot as plt
import threading
from time import sleep

import numpy as np
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
        self.simulation_data_log_path = "logs/log_simulation_data.csv"
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

        rows = []
        while not self.stop_signal:
            try:
                self.lock.acquire()
                REGS = DataBank.get_words(40000, 1001)
            finally:
                self.lock.release()

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

            if segundos_simulados/60 == 0:
                continue

            if rows and int(segundos_simulados/60) == int(rows[-1][0]):
                sleep(0.00001)
                continue

            rows.append([segundos_simulados/60, nv_montante, pot_medidor/1000, usina_flags, comporta_flags, comporta_pos,ug1_flags, ug1_pot/1000, ug1_setpot, ug1_tempo, ug1_t_mancal, ug1_perda_grade,ug2_flags, ug2_pot/1000, ug2_setpot, ug2_tempo, ug2_t_mancal, ug2_perda_grade])

            with open(self.simulation_data_log_path, 'a+') as f:
                writer = csv.writer(f, dialect='excel')
                writer.writerow(rows[-1])

            with_clp_text = True
            if with_clp_text and not segundos_simulados % 600:
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

        # After stop sig
        data = np.array(list(map(list, zip(*rows))))
        data[0] = data[0]/60
        data[3] = data[3]/np.linalg.norm(data[3])
        data[5] = data[5]/np.linalg.norm(data[5])
        data[6] = data[6]/np.linalg.norm(data[6])
        data[10] = data[10]/np.linalg.norm(data[10])
        data[11] = data[11]/np.linalg.norm(data[11])
        data[12] = data[12]/np.linalg.norm(data[12])
        data[16] = data[16]/np.linalg.norm(data[16])
        data[17] = data[17]/np.linalg.norm(data[17])

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
        plt.gcf().set_size_inches(12, 9)
        ax1.grid(True)
        ax2.grid(True)
        ax3.grid(True)
        ax4.grid(True)

        ax1.plot([0, data[0][-1]], [643.0, 643.0], linestyle='dotted', color='red')
        ax1.plot([0, data[0][-1]], [643.5, 643.5], linestyle='dotted', color='red')
        ax1.plot([0, data[0][-1]], [643.25, 643.25], linestyle='dotted', color='gray')
        ax2.plot([0, data[0][-1]], [5, 5], linestyle='dashed', color='gray')

        ax1.plot(data[0], data[1], color='blue', label="nv_montante")
        ax2.plot(data[0], data[2], color='orange', label="pot_medidor")
        ax2.plot(data[0], data[7], color='pink', linestyle=':', label="pot_ug1")
        ax2.plot(data[0], data[13], color='khaki', linestyle=':', label="pot_ug2")
        ax3.plot(data[0], data[5], color='lightblue', label="nv_comporta")
        ax3.plot(data[0], data[10], color='maroon', label="temp_ug1")
        ax3.plot(data[0], data[11], color='indianred', label="perda_ug1")
        ax3.plot(data[0], data[16], color='yellowgreen', label="temp_ug2")
        ax3.plot(data[0], data[17], color='darkolivegreen', label="perda_ug2")
        ax4.plot(data[0], data[6], color='orange', label="trip_ug1")
        ax4.plot(data[0], data[3], color='red', label="trip_usina")
        ax4.plot(data[0], data[12], color='yellow', label="trip_ug2")

        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax1.set_xlim([0, data[0][-1]])
        ax2.set_xlim([0, data[0][-1]])
        ax3.set_xlim([0, data[0][-1]])
        ax4.set_xlim([0, data[0][-1]])
        ax1.yaxis.set_major_formatter("{x:.2f}m")
        ax2.yaxis.set_major_formatter("{x:.2f}MW")
        # ax3.yaxis.set_major_formatter("{x:d}")
        # ax4.yaxis.set_major_formatter("{x:d}")

        import src.database_connector
        db = src.database_connector.Database()
        res = db.get_parametros_usina()
        kp = float(res['kp'])
        ki = float(res['ki'])
        kd = float(res['kd'])
        kie = float(res['kie'])
        ml = float(res['n_movel_L'])
        mr = float(res['n_movel_R'])
        plt.savefig("logs/imgs/log_plot kp{} kd{} ki{} Kie{} mr{} ml{}".format(kp, kd, ki, kie, mr, ml).replace('.', '_') + ".png", dpi=100)

        total_error = 0
        for row in rows:
            total_error += abs(float(row[1])-643.25)
        logger.info("Abs error: {:.2f} Abs error/time: {:.5f}".format(total_error, total_error/len(rows)))