from tkinter import E
import numpy as np


from time import time
from pyModbusTCP.server import DataBank as DB

from funcs.escrita import Escrita as ESC
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

        self.b_lg = False
        self.b_vb = False
        self.b_cp1_f = False
        self.b_cp2_f = False
        self.b_cp1_a = False
        self.b_cp2_a = False
        self.b_cp1_c = False
        self.b_cp2_c = False

    def passo(self) -> "None":
        self.calcular_vazao()
        self.calcular_enchimento_reservatorio()

    def calcular_volume_montante(self, volume) -> "float":
        return min(max(460, 460 + volume / 40000), 462.37)

    def calcular_montante_volume(self, nv_montante) -> "float":
        return 40000 * (min(max(460, nv_montante), 462.37) - 460)

    def calcular_q_sanitaria(self, nv_montante) -> "float":
        if self.dict['UG1']['etapa_atual'] != ETAPA_UP or self.dict['UG2']['etapa_atual'] != ETAPA_UP:
            # while time() < (time() + 5):
            #     self.dict["TDA"]["vb_operando"] = True
            
            # self.dict["TDA"]["vb_operando"] = False
            return 0
        else:
            # while time() < (time() + 5):
            #     self.dict["TDA"]["vb_operando"] = True
            
            # self.dict["TDA"]["vb_operando"] = False
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
        DB.set_words(MB['TDA']['NV_MONTANTE'], [round((self.dict['TDA']['nv_montante']) * 10000)],)
        DB.set_words(MB['TDA']['NV_JUSANTE_CP1'], [round((self.dict['TDA']['nv_jusante_grade']) * 10000)],)
        DB.set_words(MB['TDA']['NV_JUSANTE_CP2'], [round((self.dict['TDA']['nv_jusante_grade']) * 10000)],)

        # CP Fechada
        if self.dict["TDA"]["cp1_fechada"] and not self.b_cp1_f:
            self.b_cp1_f = True
            ESC.escrever_bit(MB["TDA"]["CP1_FECHADA"], valor=1)

        elif not self.dict["TDA"]["cp1_fechada"] and self.b_cp1_f:
            self.b_cp1_f = False
            ESC.escrever_bit(MB["TDA"]["CP1_FECHADA"], valor=0)

        if self.dict["TDA"]["cp2_fechada"] and not self.b_cp1_f:
            self.b_cp1_f = True
            ESC.escrever_bit(MB["TDA"]["CP2_FECHADA"], valor=1)

        elif not self.dict["TDA"]["cp2_fechada"] and self.b_cp1_f:
            self.b_cp1_f = False
            ESC.escrever_bit(MB["TDA"]["CP2_FECHADA"], valor=0)

        # CP Aberta
        if self.dict["TDA"]["cp1_aberta"] and not self.b_cp1_a:
            self.b_cp1_a = True
            ESC.escrever_bit(MB["TDA"]["CP1_ABERTA"], valor=1)

        elif not self.dict["TDA"]["cp1_aberta"] and self.b_cp1_a:
            self.b_cp1_a = False
            ESC.escrever_bit(MB["TDA"]["CP1_ABERTA"], valor=0)

        if self.dict["TDA"]["cp2_aberta"] and not self.b_cp1_a:
            self.b_cp1_a = True
            ESC.escrever_bit(MB["TDA"]["CP2_ABERTA"], valor=1)

        elif not self.dict["TDA"]["cp2_aberta"] and self.b_cp1_a:
            self.b_cp1_a = False
            ESC.escrever_bit(MB["TDA"]["CP2_ABERTA"], valor=0)

        # CP Aberta
        if self.dict["TDA"]["cp1_cracking"] and not self.b_cp1_c:
            self.b_cp1_c = True
            ESC.escrever_bit(MB["TDA"]["CP1_CRACKING"], valor=1)

        elif not self.dict["TDA"]["cp1_cracking"] and self.b_cp1_c:
            self.b_cp1_c = False
            ESC.escrever_bit(MB["TDA"]["CP1_CRACKING"], valor=0)

        if self.dict["TDA"]["cp2_cracking"] and not self.b_cp2_c:
            self.b_cp2_c = True
            ESC.escrever_bit(MB["TDA"]["CP2_CRACKING"], valor=1)

        elif not self.dict["TDA"]["cp2_cracking"] and self.b_cp2_c:
            self.b_cp2_c = False
            ESC.escrever_bit(MB["TDA"]["CP2_CRACKING"], valor=0)

        # Limpa Grades
        if self.dict["TDA"]["lg_operando"] and not self.b_lg:
            self.b_lg = True
            ESC.escrever_bit(MB["TDA"]["LG_OPE_MANUAL"], valor=1)

        elif not self.dict["TDA"]["lg_operando"] and self.b_lg:
            self.b_lg = False
            ESC.escrever_bit(MB["TDA"]["LG_OPE_MANUAL"], valor=0)

        # Válvula Borboleta
        if self.dict["TDA"]["vb_operando"] and not self.b_vb:
            self.b_vb = True
            ESC.escrever_bit(MB["TDA"]["VB_FECHANDO"], valor=1)

        elif not self.dict["TDA"]["vb_operando"] and self.b_vb:
            self.b_vb = False
            ESC.escrever_bit(MB["TDA"]["VB_FECHANDO"], valor=0)