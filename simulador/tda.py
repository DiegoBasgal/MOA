from pickletools import read_uint1
import numpy as np

from time import time
from threading import Thread
from pyModbusTCP.server import DataBank as DB

from dicts.reg import *
from dicts.const import *
from funcs.escrita import Escrita as ESC
from funcs.temporizador import Temporizador

class Tda:
    def __init__(self, dict_comp: 'dict'=None, tempo: 'Temporizador'=None) -> 'None':
        self.dict = dict_comp

        self.escala_ruido = tempo.escala_ruido
        self.passo_simulacao = tempo.passo_simulacao
        self.segundos_por_passo = tempo.segundos_por_passo

        self.volume = self.calcular_montante_volume(self.dict['TDA']['nv_montante'])


    def passo(self) -> 'None':
        self.calcular_vazao()
        self.calcular_enchimento_reservatorio()


    def calcular_volume_montante(self, volume) -> 'float':
        return min(max(820.50, 820.50 + volume / 11301.84), 821)


    def calcular_montante_volume(self, nv_montante) -> 'float':
        return 11301.84 * (min(max(820.50, nv_montante), 820.50) - 820.50)


    def calcular_q_sanitaria(self) -> 'float':
        return 0.22


    def calcular_vazao(self) -> 'None':
        self.dict['TDA']['q_liquida'] = 0
        self.dict['TDA']['q_liquida'] += self.dict['TDA']['q_alfuente']
        self.dict['TDA']['q_liquida'] -= self.dict['TDA']['q_sanitaria']
        self.dict['TDA']['q_sanitaria'] = self.calcular_q_sanitaria()
        self.dict['TDA']['q_vertimento'] = 0

        for ug in range(2):
            self.dict['TDA']['q_liquida'] -= self.dict[f'UG{ug + 1}'][f'q']


    def calcular_enchimento_reservatorio(self) -> 'None':
        self.dict['TDA']['nv_montante'] = self.calcular_volume_montante(self.volume + self.dict['TDA']['q_liquida'] * self.segundos_por_passo)
        self.dict['TDA']['nv_jusante_grade'] = self.dict['TDA']['nv_montante'] - max(0, np.random.normal(0.1, 0.1 * self.escala_ruido))

        if self.dict["USN"]["nv_montante"] >= USINA_NV_VERTEDOURO:
            self.dict["USN"]["q_vertimento"] = self.dict["USN"]["q_liquida"]
            self.dict["USN"]["q_liquida"] = 0
            self.dict["USN"]["nv_montante"] = (
                0.000000027849 * self.dict["USN"]["q_vertimento"] ** 3
                - 0.00002181 * self.dict["USN"]["q_vertimento"] ** 2
                + 0.0080744 * self.dict["USN"]["q_vertimento"]
                + 821
            )

        self.volume += self.dict['TDA']['q_liquida'] * self.segundos_por_passo


    def atualizar_modbus(self) -> 'None':
        DB.set_words(REG_TDA['NV_MONTANTE'], [int((self.dict['TDA']['nv_montante'] - 400) * 100)])
        DB.set_words(REG_TDA['NV_JUSANTE_GRADE'], [round((self.dict['TDA']['nv_jusante_grade']) * 10000)])