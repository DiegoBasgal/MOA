import logging
import threading
import numpy as np

from time import sleep
from datetime import datetime
from logging.config import fileConfig
from pyModbusTCP.server import DataBank

from ug import Ug
from se import Se
from tda import Tda
from dicts.regs import REG
from funcs.temporizador import Temporizador


fileConfig("C:/opt/operacao-autonoma/logger_config.ini")
logger = logging.getLogger("sim")

lock = threading.Lock()


class Usn:
    def __init__(self, dict_comp: "dict", data_bank: "DataBank", tempo: "Temporizador") -> "None":

        self.dict = dict_comp
        self.sim_db = data_bank

        self.speed = tempo.velocidade
        self.escala_ruido = tempo.escala_ruido
        self.passo_simulacao = tempo.passo_simulacao
        self.segundos_por_passo = self.passo_simulacao * self.speed

        self.se = Se(dict_comp, tempo, data_bank)
        self.tda = Tda(dict_comp, tempo, data_bank)

        ug1 = Ug(1, dict_comp, tempo, data_bank)
        ug2 = Ug(2, dict_comp, tempo, data_bank)
        ug3 = Ug(3, dict_comp, tempo, data_bank)
        self.ugs = [ug1, ug2, ug3]


        self.b_condic = False


    def run(self) -> "None":
        while not self.dict["GLB"]["stop_sim"]:
            self.dict["GLB"]["stop_sim"] = self.dict["GLB"]["stop_gui"]

            try:
                t_inicio_passo = datetime.now()

                lock.acquire()

                self.dict["GLB"]["tempo_simul"] += self.segundos_por_passo

                if self.dict["SA"]["condicionador"] and not self.b_condic:
                    self.b_condic = True
                    self.sim_db.set_words(REG["SA_Condicionador"], [1])

                elif not self.dict["SA"]["condicionador"] and self.b_condic:
                    self.b_condic = False
                    self.sim_db.set_words(REG["SA_Condicionador"], [0])
                    self.se.reconhece_reset_dj()

                if self.dict["GLB"]["reset_condicionadores"]:
                    self.sim_db.set_words(REG["SA_Condicionador"], [0])
                    self.sim_db.set_words(REG["UG1_Condicionador"], [0])
                    self.sim_db.set_words(REG["UG2_Condicionador"], [0])
                    self.sim_db.set_words(REG["UG3_Condicionador"], [0])

                if self.sim_db.get_words(REG["SA_CMD_ResetGeral"])[0] == 1:
                    self.sim_db.set_words(REG["SA_CMD_ResetGeral"], [0])
                    self.sim_db.set_words(REG["SA_CMD_CalaSirene"], [0])
                    logger.info("[USN] Comando de Reconhece e Reset Geral")
                    self.se.reconhece_reset_dj()
                    for ug in self.ugs: ug.reconhece_reset()

                self.se.passo()
                self.tda.passo()
                for ug in self.ugs: ug.passo()

                lock.release()

                tempo_restante = (self.passo_simulacao - (datetime.now() - t_inicio_passo).seconds)
                sleep(tempo_restante) if tempo_restante > 0 else logger.warning("A simulação está demorando mais do que o permitido.")

            except KeyboardInterrupt:
                self.dict["GLB"]["stop_gui"] = True
                continue
