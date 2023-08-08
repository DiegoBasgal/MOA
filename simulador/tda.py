import numpy as np

from pyModbusTCP.server import DataBank as DB

from funcs.temporizador import Temporizador

from dicts.reg import *
from dicts.const import *
from dicts.dict import compartilhado

class Tda:
    def __init__(self, tempo: Temporizador) -> "None":
        self.dict = compartilhado

        self.volume = 0

        self.escala_ruido = tempo.escala_ruido
        self.passo_simulacao = tempo.passo_simulacao
        self.segundos_por_passo = tempo.segundos_por_passo

    def passo(self) -> "None":
        self.calcular_vazao()
        self.calcular_enchimento_reservatorio()
        self.atualizar_modbus()

    def calcular_volume_montante(self, volume) -> "float":
        return min(max(460, 460 + volume / 40000), 462.37)

    def calcular_montante_volume(self, nv_montante) -> "float":
        return 40000 * (min(max(460, nv_montante), 462.37) - 460)

    def calcular_q_sanitaria(self, nv_montante) -> "float":
        if self.dict['UG1']['etapa_atual'] != ETAPA_UP or self.dict['UG2']['etapa_atual'] != ETAPA_UP:
            return 0
        else:
            return 2.33

    def calcular_vazao(self) -> "None":
        self.dict['TDA']['q_liquida'] = 0
        self.dict['TDA']['q_liquida'] += self.dict['TDA']['q_alfuente']
        self.dict['TDA']['q_liquida'] -= self.dict['TDA']['q_sanitaria']
        self.dict['TDA']['q_sanitaria'] = self.calcular_q_sanitaria(self.dict['TDA']['nv_montante'])
        self.dict['TDA']['q_vertimento'] = 0

        ug = 0
        for _ in range(2):
            ug += 1
            self.dict['TDA']['q_liquida'] -= self.dict[f'UG{ug}'][f'q']

    def calcular_enchimento_reservatorio(self) -> "None":
        self.dict['TDA']['nv_montante'] = self.calcular_volume_montante(self.volume + self.dict['TDA']['q_liquida'] * self.segundos_por_passo)
        self.dict['TDA']['nv_jusante_grade'] = self.dict['TDA']['nv_montante'] - max(0, np.random.normal(0.1, 0.1 * self.escala_ruido))

        if self.dict['TDA']['nv_montante'] >= USINA_NV_VERTEDOURO:
            self.dict['TDA']['q_vertimento'] = self.dict['TDA']['q_liquida']
            self.dict['TDA']['q_liquida'] = 0
            self.dict['TDA']['nv_montante'] = (
                0.0000021411 * self.dict['TDA']['q_vertimento'] ** 3
                - 0.00025189 * self.dict['TDA']['q_vertimento'] ** 2
                + 0.014859 * self.dict['TDA']['q_vertimento']
                + 462.37
            )

        self.volume += self.dict['TDA']['q_liquida'] * self.segundos_por_passo

    def atualizar_modbus(self) -> "None":
        DB.set_words(MB['NV_MONTANTE'], [round((self.dict['TDA']['nv_montante']) * 10000)])
        DB.set_words(MB['NV_JUSANTE_CP1'], [round((self.dict['TDA']['nv_jusante_grade']) * 10000)])
        DB.set_words(MB['NV_JUSANTE_CP2'], [round((self.dict['TDA']['nv_jusante_grade']) * 10000)])