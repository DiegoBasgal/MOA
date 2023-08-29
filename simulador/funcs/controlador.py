import pytz
import mariadb
import threading

from sys import stdout
from time import sleep
from datetime import datetime

lock = threading.Lock()

class Controlador:
    def __init__(self, compartilhado):
        self.dict = compartilhado

        self.cnx = mariadb.ConnectionPool(
            host="localhost",
            user="moa",
            password="&264H3$M@&z$",
            pool_name="controlador_sim",
            database="debug",
            pool_size=10,
            pool_reset_session=True,
        )

        self.conn = self.cnx.get_connection()
        self.cursor = self.conn.cursor()

        self.tempo_afluente = []

        with open("C:/Users/diego.garcia/Desktop/operacao-autonoma/simulador/entrada_afluente.csv", "r") as fp:
            rawlines = fp.readlines()

        i = 0
        for line in rawlines:
            line = line.split(",")
            self.tempo_afluente.append([i, float(line[0]) * 60, float(line[1])])
            i += 1


    @staticmethod
    def get_time() -> "datetime":
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    def run(self):
        q_ant = 0
        ultimo_log = -1
        contador_afluente = 0

        while not self.dict["GLB"]["stop_sim"]:

            self.dict["GLB"]["stop_sim"] = self.dict["GLB"]["stop_gui"]

            try:
                t_inicio_passo = self.get_time()
                lock.acquire()

                if self.tempo_afluente[contador_afluente + 1][1] <= self.dict["GLB"]["tempo_simul"]:
                    contador_afluente += 1

                if self.tempo_afluente[contador_afluente][2] == 9910:
                    self.dict['UG1']['condic'] = True

                if self.tempo_afluente[contador_afluente][2] == 9920:
                    self.dict['UG2']['condic'] = True

                if self.tempo_afluente[contador_afluente][2] == 9930:
                    self.dict['BAY']['condic'] = True

                if self.tempo_afluente[contador_afluente][2] == 9940:
                    self.dict['SE']['condic'] = True

                if self.tempo_afluente[contador_afluente][2] == -1:
                    self.dict["GLB"]["stop_sim"] = self.dict["GLB"]["stop_gui"] = True
                    exit()

                lock.release()

                if not int(self.dict["GLB"]["tempo_simul"] / 60) == int(ultimo_log / 60):
                    ultimo_log = self.dict["GLB"]["tempo_simul"]
                    self.cursor.execute(
                        f"INSERT INTO debug.simul_data VALUES( \
                        {self.get_time().timestamp()}, \
                        {self.dict['TDA']['q_alfuente']}, \
                        {self.dict['TDA']['nv_montante']}, \
                        {self.dict['UG1']['potencia']}, \
                        {self.dict['UG1']['setpoint']}, \
                        {self.dict['UG2']['potencia']}, \
                        {self.dict['UG2']['setpoint']});"
                    )
                    self.conn.commit()

                tempo_restante = (self.get_time() - t_inicio_passo).microseconds * 10e-6

                if tempo_restante > 0:
                    sleep(tempo_restante)

            except KeyboardInterrupt:
                self.dict["GLB"]["stop_gui"] = True
                continue
