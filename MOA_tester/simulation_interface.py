import csv
from time import sleep

from pyModbusTCP.server import ModbusServer, DataBank
import logging
import threading
import datetime
from sys import stdout
from src.mensageiro.mensageiro_log_handler import MensageiroHandler

string_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

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


class simulation_interface(threading.Thread):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.stop_signal = False
        self.simulation_data_log_path = "logs/simulation_data_{}.csv".format(string_date)
        with open(self.simulation_data_log_path, 'w+') as f:
            logger.info("Simulation data is being saved to {}".format(self.simulation_data_log_path))
            header = ["segundos_simulados", "nv_montante", "pot_medidor", "usina_flags", "comporta_flags", "comporta_pos",
                        "ug1_flags", "ug1_pot", "ug1_setpot", "ug1_tempo", "ug1_t_mancal", "ug1_perda_grade",
                        "ug2_flags", "ug2_pot", "ug2_setpot", "ug2_tempo", "ug2_t_mancal", "ug2_perda_grade"]
            writer = csv.writer(f, dialect='excel')
            writer.writerow(header)

        logger.debug("simulation_interface init OK")


    def stop(self):
        self.stop_signal = True

    def run(self):
        while not self.stop_signal:
            try:
                self.lock.acquire()
                REGS = DataBank.get_words(0, 101)

                nv_montante = (REGS[0] / 1000) + 620
                pot_medidor = REGS[1]
                usina_flags = REGS[100]
                comporta_flags = REGS[10]
                comporta_pos = REGS[10]
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

                row = [segundos_simulados, nv_montante, pot_medidor, usina_flags, comporta_flags, comporta_pos,
                          ug1_flags, ug1_pot, ug1_setpot, ug1_tempo, ug1_t_mancal, ug1_perda_grade,
                          ug2_flags, ug2_pot, ug2_setpot, ug2_tempo, ug2_t_mancal, ug2_perda_grade]

                with open(self.simulation_data_log_path, 'a') as f:
                    writer = csv.writer(f, dialect='excel')
                    writer.writerow(row)

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

                sleep(1)

            finally:
                self.lock.release()

