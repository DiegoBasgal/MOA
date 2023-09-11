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
        return min(max(461.37, 461.37 + volume / 190000), 462.37)


    def calcular_montante_volume(self, nv_montante) -> 'float':
        return 190000 * (min(max(461.37, nv_montante), 462.37) - 461.37)


    def calcular_q_sanitaria(self) -> 'float':
        if self.dict['UG1']['etapa_atual'] == ETAPA_UP and self.dict['UG2']['etapa_atual'] == ETAPA_UP:
            if not self.dict['BRD']['vb_calculo_q']:
                self.dict['BRD']['vb_calculo_q'] = True
                Thread(target=lambda: self.operar_vb()).start()
            return np.random.normal(2.33, 0.1 * self.escala_ruido)

        else:
            if self.dict['BRD']['vb_calculo_q']:
                self.dict['BRD']['vb_calculo_q'] = False
                Thread(target=lambda: self.operar_vb()).start()
            return 0


    def operar_vb(self) -> 'None':
        print('[TDA] Operando Válvula Borboleta de Vazão Sanitária')
        self.dict['TDA']['vb_operando'] = True
        self.dict['TDA']['uh_disponivel'] = False
        delay = time() + 10
        while time() < delay:
            None

        self.dict['TDA']['vb_operando'] = False
        self.dict['TDA']['uh_disponivel'] = True
        print('[TDA] Operação Válvula Borboleta Finalizada')


    def calcular_vazao(self) -> 'None':
        self.dict['TDA']['q_liquida'] = 0
        self.dict['TDA']['q_liquida'] += self.dict['TDA']['q_alfuente']
        self.dict['TDA']['q_liquida'] -= self.dict['TDA']['q_sanitaria']
        self.dict['TDA']['q_sanitaria'] = self.calcular_q_sanitaria()
        self.dict['TDA']['q_vertimento'] = 0

        for ug in range(1):
            self.dict['TDA']['q_liquida'] -= self.dict[f'UG{ug + 1}'][f'q']


    def calcular_enchimento_reservatorio(self) -> 'None':
        self.dict['TDA']['nv_montante'] = self.calcular_volume_montante(self.volume + self.dict['TDA']['q_liquida'] * self.segundos_por_passo)
        self.dict['TDA']['nv_jusante_grade'] = self.dict['TDA']['nv_montante'] - max(0, np.random.normal(0.1, 0.1 * self.escala_ruido))
    
        if self.dict['TDA']['nv_montante'] >= USINA_NV_VERTEDOURO:
            self.dict['TDA']['q_vertimento'] = self.dict['TDA']['q_liquida']
            self.dict['TDA']['q_liquida'] = 0
            self.dict['TDA']['nv_montante'] = (0.0000021411 * self.dict["q_vertimento"] ** 3
                                            - 0.00025189 * self.dict["q_vertimento"] ** 2
                                            + 0.014859 * self.dict["q_vertimento"]
                                            + 462.37)

        self.volume += self.dict['TDA']['q_liquida'] * self.segundos_por_passo


    def atualizar_modbus(self) -> 'None':

        DB.set_words(MB['TDA']['NV_MONTANTE'], [self.dict['TDA']['nv_montante'] * 100])
        DB.set_words(MB['TDA']['NV_JUSANTE_CP1'], [round((self.dict['TDA']['nv_jusante_grade']) * 10000)])
        DB.set_words(MB['TDA']['NV_JUSANTE_CP2'], [round((self.dict['TDA']['nv_jusante_grade']) * 10000)])

        # Limpa Grades
        if self.dict['TDA']['lg_operando'] and not self.dict['BRD']['lg_operando']:
            self.dict['BRD']['lg_operando'] = True
            ESC.escrever_bit(MB['TDA']['LG_OPE_MANUAL'], valor=1)

        elif not self.dict['TDA']['lg_operando'] and self.dict['BRD']['lg_operando']:
            self.dict['BRD']['lg_operando'] = False
            ESC.escrever_bit(MB['TDA']['LG_OPE_MANUAL'], valor=0)

        # Válvula Borboleta
        if self.dict['TDA']['vb_operando'] and not self.dict['BRD']['vb_operando']:
            self.dict['BRD']['vb_operando'] = True
            ESC.escrever_bit(MB['TDA']['VB_FECHANDO'], valor=1)

        elif not self.dict['TDA']['vb_operando'] and self.dict['BRD']['vb_operando']:
            self.dict['BRD']['vb_operando'] = False
            ESC.escrever_bit(MB['TDA']['VB_FECHANDO'], valor=0)

        # Unidade Hidráulica
        if self.dict['TDA']['uh_disponivel'] and not self.dict['BRD']['uh_disponivel']:
            self.dict['BRD']['uh_disponivel'] = True
            ESC.escrever_bit(MB['TDA']['UH_DISPONIVEL'], valor=1)

        elif not self.dict['TDA']['uh_disponivel'] and self.dict['BRD']['uh_disponivel']:
            self.dict['BRD']['uh_disponivel'] = False
            ESC.escrever_bit(MB['TDA']['UH_DISPONIVEL'], valor=0)