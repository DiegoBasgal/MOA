import pytz
import mariadb
import logging
import threading

from logging.config import fileConfig

from time import sleep
from datetime import datetime


fileConfig("C:/opt/operacao-autonoma/logger_config.ini")
logger = logging.getLogger("sim")


lock = threading.Lock()


class Controlador:
    def __init__(self, compartilhado):
        self.dict = compartilhado

        self.cnx = mariadb.ConnectionPool(
            host='172.21.15.999',
            user='moa',
            password='&264H3$M@&z$',
            database='django_db',
            pool_name='sim_control',
            pool_size=10,
            pool_validation_interval=250,
        )

        self.conn = self.cnx.get_connection()
        self.cursor = self.conn.cursor()

        self.b_se = False
        self.b_ug1 = False
        self.b_ug2 = False
        self.b_ug3 = False

        self.tempo_afluente = []

        with open('C:/Users/diego.garcia/Desktop/operacao-autonoma/simulador/dicts/entrada_afluente.csv', 'r') as fp:
            rawlines = fp.readlines()

        i = 0
        for line in rawlines:
            s = line.split(',')
            self.tempo_afluente.append([i, float(s[0]) * 60, float(s[1])])
            i += 1


    @staticmethod
    def get_time() -> 'datetime':
        return datetime.now(pytz.timezone('Brazil/East')).replace(tzinfo=None)


    def run(self):
        q_ant = 0
        ultimo_log = -1
        contador_afluente = 0

        while not self.dict['GLB']['stop_sim']:

            self.dict['GLB']['stop_sim'] = self.dict['GLB']['stop_gui']

            try:
                t_inicio_passo = self.get_time()
                lock.acquire()

                if self.tempo_afluente[contador_afluente + 1][1] <= self.dict['GLB']['tempo_simul']:
                    contador_afluente += 1
                    print(contador_afluente)


                if self.tempo_afluente[contador_afluente][2] == -1:
                    self.dict['GLB']['stop_sim'] = self.dict['GLB']['stop_gui'] = True
                    exit()

                if self.tempo_afluente[contador_afluente][2] in (9910, 9920, 9930, 9940):
                    pass

                else:
                    self.dict['TDA']['q_afluente'] = self.tempo_afluente[contador_afluente][2]


                if self.tempo_afluente[contador_afluente][2] == 9910 and not self.b_ug1:
                    self.b_ug1 = True
                    self.dict['UG1']['condicionador'] = True

                elif self.tempo_afluente[contador_afluente][2] != 9910 and self.b_ug1:
                    self.b_ug1 = False

                if self.tempo_afluente[contador_afluente][2] == 9920 and not self.b_ug2:
                    self.b_ug2 = True
                    self.dict['UG2']['condicionador'] = True

                elif self.tempo_afluente[contador_afluente][2] != 9920 and self.b_ug2:
                    self.b_ug2 = False

                if self.tempo_afluente[contador_afluente][2] == 9930 and not self.b_ug3:
                    self.b_ug3 = True
                    self.dict['UG3']['condicionador'] = True

                elif self.tempo_afluente[contador_afluente][2] != 9930 and self.b_ug3:
                    self.b_ug3 = False

                if self.tempo_afluente[contador_afluente][2] == 9940 and not self.b_se:
                    self.b_se = True
                    self.dict['SE']['condicionador'] = True

                elif self.tempo_afluente[contador_afluente][2] != 9940 and self.b_se:
                    self.b_se = False

                lock.release()

                if not int(self.dict['GLB']['tempo_simul'] / 60) == int(ultimo_log / 60):
                    ultimo_log = self.dict['GLB']['tempo_simul']
                    self.cursor.execute(
                        f'INSERT INTO debug.simul_data VALUES( \
                        {self.get_time().timestamp()}, \
                        {self.dict["TDA"]["q_afluente"]}, \
                        {self.dict["TDA"]["nv_montante"]}, \
                        {self.dict["UG1"]["potencia"]}, \
                        {self.dict["UG1"]["setpoint"]}, \
                        {self.dict["UG2"]["potencia"]}, \
                        {self.dict["UG2"]["setpoint"]}, \
                        {self.dict["UG3"]["potencia"]}, \
                        {self.dict["UG3"]["setpoint"]} );'
                    )
                    self.conn.commit()

                tempo_restante = (self.get_time() - t_inicio_passo).microseconds * 10e-6

                if tempo_restante > 0:
                    sleep(tempo_restante)

            except KeyboardInterrupt:
                self.dict['GLB']['stop_gui'] = True
                continue
