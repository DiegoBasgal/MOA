import logging
import numpy as np

from logging.config import fileConfig
from pyModbusTCP.server import DataBank

from dicts.const import *
from dicts.regs import REG
from funcs.temporizador import Temporizador


fileConfig("C:/opt/operacao-autonoma/logger_config.ini")
logger = logging.getLogger("sim")


class Tda:
    def __init__(self, dict_comp: "dict", tempo: "Temporizador", data_bank: "DataBank") -> "None":

        self.dict = dict_comp
        self.sim_db = data_bank

        self.escala_ruido = tempo.escala_ruido
        self.segundos_por_passo = tempo.segundos_por_passo

        self.volume = self.montate_volume(self.dict["TDA"]["nv_montante"])


    def passo(self) -> "None":
        self.calcular_vazao()
        self.calcular_enchimento_reservatorio()
        self.atualizar_modbus()


    def calcular_q_sanitaria(self) -> "float":
        return 0.35


    def volume_montate(self, volume) -> "float":
        return min(max(404.75, 404.75 + volume / 3887.18), 405.15)


    def montate_volume(self, nv_montante) -> "float":
        return 3887.18 * (min(max(404.75, nv_montante), 405.15) - 404.75)


    def calcular_vazao(self) -> "None":
        self.dict["TDA"]["q_liquida"] = 0
        self.dict["TDA"]["q_liquida"] += self.dict["TDA"]["q_afluente"]
        self.dict["TDA"]["q_liquida"] -= self.dict["TDA"]["q_sanitaria"]
        self.dict["TDA"]["q_sanitaria"] = self.calcular_q_sanitaria()
        self.dict["TDA"]["q_vertimento"] = 0

        for ug in range(2):
            self.dict["TDA"]["q_liquida"] -= self.dict[f"UG{ug+1}"][f"q"]


    def calcular_enchimento_reservatorio(self) -> "None":
        self.dict["TDA"]["nv_montante"] = self.volume_montate(self.volume + self.dict["TDA"]["q_liquida"] * self.segundos_por_passo)
        self.dict["TDA"]["nv_jusante_grade"] = self.dict["TDA"]["nv_montante"] - max(0, np.random.normal(0.1, 0.1 * self.escala_ruido))

        if self.dict["TDA"]["nv_montante"] >= USINA_NV_VERTEDOURO:
            self.dict["TDA"]["q_vertimento"] = self.dict["TDA"]["q_liquida"]
            self.dict["TDA"]["q_liquida"] = 0
            self.dict["TDA"]["nv_montante"] = (0.00004 * self.dict["TDA"]["q_vertimento"] ** 3
                                               - 0.0021 * self.dict["TDA"]["q_vertimento"] ** 2
                                               + 0.0475 * self.dict["TDA"]["q_vertimento"]
                                               + 405.15)

        self.volume += self.dict["TDA"]["q_liquida"] * self.segundos_por_passo


    def atualizar_modbus(self) -> "None":
        self.sim_db.set_words(REG["TDA_NivelMontante"], [int((self.dict["TDA"]["nv_montante"] - 400) * 10000)])
