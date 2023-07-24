import pytz
import logging
import threading

from sys import stdout
from time import sleep
from datetime import datetime
from mysql.connector import pooling

lock = threading.Lock()

logger = logging.getLogger("__main__")

class Controlador:
    def __init__(self, shared_dict):
        self.dict = shared_dict

        i = 0

        self.timed_afluente = []

        with open("simulation_input_data.csv", "r") as fp:
            rawlines = fp.readlines()

        for line in rawlines:
            line = line.split(",")
            self.timed_afluente.append([i, float(line[0]) * 60, float(line[1])])
            i += 1

        self.connection_pool = pooling.MySQLConnectionPool(
            pool_name="my_pool",
            pool_size=10,
            pool_reset_session=True,
            host="172.21.15.110",
            user="moa",
            password="&264H3$M@&z$",
            database="django_db",
        )

        self.conn = self.connection_pool.get_connection()
        self.cursor = self.conn.cursor()

    def get_time(self) -> object:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def run(self):
        q_ant = 0
        last_log_time = -1
        counter_timed_afluente = 0

        while not self.dict.GLB["stop_sim"]:
            w = 0.5
            qmed = 7
            qdelta = 3

            self.dict.GLB["stop_sim"] = self.dict.GLB["stop_gui"]

            try:
                t_inicio_passo = self.get_time()
                lock.acquire()

                if (self.timed_afluente[counter_timed_afluente + 1][1] <= self.dict.GLB["tempo_simul"]):
                    counter_timed_afluente += 1

                if self.timed_afluente[counter_timed_afluente][2] == -1:
                    self.dict.GLB["stop_sim"] = True
                    self.dict.GLB["stop_gui"] = True
                    exit()

                self.dict.USN["q_alfuente"] = self.timed_afluente[counter_timed_afluente][2]

                duty = (((self.dict.GLB["tempo_simul"] *  w) % 3600) / 3600)
                self.dict.USN["q_alfuente"] = qmed - (qdelta/2) + qdelta * (2 * duty) if duty <= 0.5 else qmed + (qdelta/2) + qdelta * (2 * (0.5-duty))

                lock.release()

                if not int(self.dict.GLB["tempo_simul"] / 60) == int(last_log_time / 60):
                    last_log_time = self.dict.GLB["tempo_simul"]
                    self.cursor.execute(
                        f"INSERT INTO debug.simul_data VALUES({self.get_time().timestamp()}, \
                        {self.dict['q_alfuente']}, \
                        {self.dict['nv_montante']}, \
                        {self.dict['potencia_kw_ug1']}, \
                        {self.dict['setpoint_kw_ug1']}, \
                        {self.dict['potencia_kw_ug2']}, \
                        {self.dict['setpoint_kw_ug2']});"
                    )
                    self.conn.commit()

                tempo_restante = (self.get_time() - t_inicio_passo).microseconds * 10e-6

                if tempo_restante > 0:
                    sleep(tempo_restante)

            except KeyboardInterrupt:
                self.dict.GLB["stop_gui"] = True
                continue
