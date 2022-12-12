from datetime import datetime
from sys import stdout
import threading
import logging
from time import sleep
from datetime import datetime
from mysql.connector import pooling

lock = threading.Lock()


class Controlador:
    def __init__(self, shared_dict):

        # Set-up logging
        rootLogger = logging.getLogger()
        if rootLogger.hasHandlers():
            rootLogger.handlers.clear()
        rootLogger.setLevel(logging.NOTSET)
        self.logger = logging.getLogger(__name__)

        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.setLevel(logging.NOTSET)
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-20.20s] [%(levelname)-5.5s] %(message)s")

        ch = logging.StreamHandler(stdout)  # log para sdtout
        ch.setFormatter(logFormatter)
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)

        fh = logging.FileHandler("simulacao.log")  # log para arquivo
        fh.setFormatter(logFormatter)
        fh.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)
        # Fim Set-up logging

        self.shared_dict = shared_dict

        self.timed_afluente = []
        with open("simulation_input_data.csv", "r") as fp:
            rawlines = fp.readlines()

        i = 0
        for line in rawlines:
            line = line.split(",")
            self.timed_afluente.append([i, float(line[0]) * 60, float(line[1])])
            i += 1

        self.connection_pool = pooling.MySQLConnectionPool(
            pool_name="my_pool",
            pool_size=10,
            pool_reset_session=True,
            host="172.21.15.171",
            user="root",
            password="&264H3$M@&z$",
            database="django_db",
        )

        self.conn = self.connection_pool.get_connection()
        self.cursor = self.conn.cursor()
        
    def run(self):

        q_ant = 0
        counter_timed_afluente = 0
        last_log_time = -1

        with open("simulation_output_data.csv", "w") as fp:
            fp.write("ts,q_aflu,nv_montante,pot_ug1,set_ug1,pot_ug2,set_ug2\n")

        while not self.shared_dict["stop_sim"]:
            self.shared_dict["stop_sim"] = self.shared_dict["stop_gui"]
            try:
                t_inicio_passo = datetime.now()
                lock.acquire()

                if (self.timed_afluente[counter_timed_afluente + 1][1]<= self.shared_dict["tempo_simul"]):
                    counter_timed_afluente += 1

                if self.timed_afluente[counter_timed_afluente][2] == -1:
                    self.shared_dict["stop_sim"] = True
                    self.shared_dict["stop_gui"] = True
                    exit()

                # lf.shared_dict["q_alfuente"] = self.timed_afluente[counter_timed_afluente][2]

                """
                qmed = 7
                qdelta = 3           
                w = 0.5

                duty = (((self.shared_dict["tempo_simul"]*w)%3600)/3600)
                if duty <= 0.5:
                    self.shared_dict["q_alfuente"] = qmed - (qdelta/2) + qdelta * (2 * duty)
                else:
                    self.shared_dict["q_alfuente"] = qmed + (qdelta/2) + qdelta * (2 * (0.5-duty))
                """

                # FIM COMPORTAMENTO USINA
                lock.release()

                if not int(self.shared_dict["tempo_simul"] / 60) == int(last_log_time / 60):
                    last_log_time = self.shared_dict["tempo_simul"]
                    # "ts,q_aflu,nv_montante,pot_ug1,set_ug1,pot_ug2,set_ug2"
                    ts = int(datetime.timestamp(datetime.now()))

                    self.cursor.execute(
                        "INSERT INTO debug.simul_data VALUES({}, {}, {}, {}, {}, {}, {});".format(
                            ts,
                            self.shared_dict["q_alfuente"],
                            self.shared_dict["nv_montante"],
                            self.shared_dict["potencia_kw_ug1"],
                            self.shared_dict["setpoint_kw_ug1"],
                            self.shared_dict["potencia_kw_ug2"],
                            self.shared_dict["setpoint_kw_ug2"],
                        )
                    )
                    self.conn.commit()

                tempo_restante = (datetime.now() - t_inicio_passo).microseconds * 10e-6
                if tempo_restante > 0:
                    sleep(tempo_restante)

            except KeyboardInterrupt:
                self.shared_dict["stop_gui"] = True
                continue
