import numpy as np

from pyModbusTCP.server import DataBank as DB

from se import Se
from funcs.escrita import Escrita as ESC
from funcs.temporizador import Temporizador

from dicts.reg import *
from dicts.const import *
from dicts.dict import compartilhado

class Bay:
    def __init__(self, tempo: Temporizador) -> "None":
        self.dict = compartilhado

        self.escala_ruido = tempo.escala_ruido
        self.passo_simulacao = tempo.passo_simulacao
        self.segundos_por_passo = tempo.segundos_por_passo

        self.mola = 0
        self.tempo_carregamento_mola = 2
        self.avisou_trip = False

        self.b_mola = False
        self.b_secc = False


    def passo(self) -> "None":
        self.verificar_mola_dj()
        self.verificar_tensao_dj()
        self.verificar_condicao_dj()

        if self.dict['BAY']['debug_dj_fechar'] and self.dict['BAY']['debug_dj_abrir']:
            self.dict['BAY']['dj_aberto'] = True
            self.dict['BAY']['dj_fechado'] = True
            self.dict['BAY']['debug_dj_abrir'] = False
            self.dict['BAY']['debug_dj_fechar'] = False
            self.tripar_dj()

        elif self.dict['BAY']['debug_dj_fechar']:
            self.dict['BAY']['debug_dj_fechar'] = False
            self.fechar_dj()

        elif self.dict['BAY']['debug_dj_abrir']:
            self.dict['BAY']['debug_dj_abrir'] = False
            self.abrir_dj()

        if self.dict['BAY']['debug_dj_reset']:
            self.resetar_bay()


    def atualizar_mp_mr(self) -> "None":
        self.dict['BAY']['potencia_mp'] = (np.random.normal(self.dict['SE']['potencia_se'] * 0.98,10 * self.escala_ruido) - 20)
        self.dict['BAY']['potencia_mr'] = (np.random.normal(self.dict['SE']['potencia_se'] * 0.98,10 * self.escala_ruido) - 20)


    def verificar_tensao_dj(self) -> "None":
        if not (USINA_TENSAO_MINIMA < self.dict['BAY']['tensao_linha'] < USINA_TENSAO_MAXIMA):
            self.dict['BAY']['dj_falta_vcc'] = True
            self.tripar_dj(descr='Tensão fora dos limites.')

        else:
            self.dict['BAY']['dj_falta_vcc'] = False


    def verificar_mola_dj(self) -> "None":
        if not self.dict['BAY']['dj_mola_carregada']:
            self.mola += self.segundos_por_passo

            if self.mola >= self.tempo_carregamento_mola:
                self.mola = 0
                self.dict['BAY']['dj_mola_carregada'] = True


    def abrir_dj(self) -> "None":
        print('[BAY] Comando de Abertura do Disjuntor do Bay acionado')

        if self.dict['BAY']['dj_mola_carregada']:
            self.dict['BAY']['dj_aberto'] = True
            self.dict['BAY']['dj_fechado'] = False

            if self.dict['SE']['dj_fechado']:
                self.dict['SE']['dj_trip'] = True
                self.dict['SE']['dj_aberto'] = True
                self.dict['SE']['dj_fechado'] = False
                self.dict['SE']['debug_dj_aberto'] = True
                self.dict['SE']['debug_dj_fechado'] = False

        else:
            self.tripar_dj(descr='Fechou antes de carregar a mola.')

        self.dict['BAY']['dj_mola_carregada'] = False


    def fechar_dj(self) -> "None":
        if self.dict['BAY']['dj_trip']:
            self.dict['BAY']['dj_falha'] = True
            self.tripar_dj(descr='Picou.')

        else:
            if self.dict['SE']['dj_fechado']:
                print('[BAY] Realizando Abertura do Disjuntor da Subestação antes de fechar o Disjuntor do BAY')
                self.dict['SE']['dj_aberto'] = True
                self.dict['SE']['dj_fechado'] = False
                self.dict['SE']['debug_dj_aberto'] = True
                self.dict['SE']['debug_dj_fechado'] = False

            if not self.dict['BAY']['dj_fechado']:
                print('[BAY] Comando de Fechamento do Disjuntor do Bay acionado')

                if self.dict['BAY']['dj_condicao']:
                    self.dict['BAY']['dj_aberto'] = False
                    self.dict['BAY']['dj_fechado'] = True
                    self.dict['BAY']['dj_mola_carregada'] = False

                else:
                    self.dict['BAY']['dj_falha'] = True
                    self.tripar_dj(descr='Fechou antes de ter a condição de fechamento.')


    def tripar_dj(self, descr=None) -> "None":
        if not self.avisou_trip:
            self.avisou_trip = True
            self.dict['BAY']['dj_trip'] = True
            self.dict['BAY']['dj_aberto'] = True
            self.dict['BAY']['dj_fechado'] = False
            self.dict['BAY']['dj_mola_carregada'] = False
            self.dict['BAY']['dj_falha'] = True
            print(f'[BAY] TRIP Disjuntor do Bay! | Descrição: {descr}')


    def resetar_bay(self) -> "None":
        print('[BAY] Comando de Reset Geral acionado')
        self.dict['BAY']['dj_trip'] = False
        self.dict['BAY']['dj_falha'] = False
        self.dict['BAY']['debug_dj_abrir'] = False
        self.dict['BAY']['debug_dj_fechar'] = False
        self.dict['BAY']['debug_dj_reset'] = False
        self.avisou_trip = False


    def verificar_condicao_dj(self) -> "None":
        if self.dict['BAY']['dj_trip'] \
        or self.dict['BAY']['dj_fechado'] \
        or self.dict['BAY']['dj_falta_vcc'] \
        or not self.dict['BAY']['dj_aberto'] \
        or not self.dict['BAY']['dj_mola_carregada']:
            self.dict['BAY']['dj_condicao'] = False

        else:
            self.dict['BAY']['dj_condicao'] = True


    def atualizar_modbus(self) -> "None":
        # DB.set_words(MB['BAY']['POTENCIA_KW_MP'], [round(max(0, self.dict['BAY']['potencia_mp']))])
        # DB.set_words(MB['BAY']['POTENCIA_KW_MR'], [round(max(0, self.dict['BAY']['potencia_mr']))])

        if self.dict['BAY']['dj_secc'] and not self.b_secc:
            self.b_secc = True
            ESC.escrever_bit(MB['BAY']['SECC_FECHADA'], valor=1)

        elif not self.dict['BAY']['dj_secc'] and self.b_secc:
            self.b_secc = False
            ESC.escrever_bit(MB['BAY']['SECC_FECHADA'], valor=0)

        if self.dict['BAY']['dj_mola_carregada'] and not self.b_mola:
            self.b_mola = True
            ESC.escrever_bit(MB['BAY']['DJL_MOLA_CARREGADA'], valor=1)

        elif not self.dict['BAY']['dj_mola_carregada'] and self.b_mola:
            self.b_mola = False
            ESC.escrever_bit(MB['BAY']['DJL_MOLA_CARREGADA'], valor=0)