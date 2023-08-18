import numpy as np

from pyModbusTCP.server import DataBank as DB

from dicts.reg import *
from dicts.const import *
from funcs.leitura import Leitura as LEI
from funcs.escrita import Escrita as ESC
from funcs.temporizador import Temporizador

class Bay:
    def __init__(self, dict_comp: 'dict'=None, tempo: 'Temporizador'=None) -> "None":
        self.dict = dict_comp

        self.escala_ruido = tempo.escala_ruido
        self.passo_simulacao = tempo.passo_simulacao
        self.segundos_por_passo = tempo.segundos_por_passo

        self.mola = 0
        self.tempo_carregamento_mola = 2

        self.avisou_trip = False


    def passo(self) -> "None":
        self.verificar_mola_dj()
        self.verificar_tensao_dj()
        self.verificar_condicao_dj()

        if LEI.ler_bit(MB['BAY']['DJL_CMD_FECHAR']):
            ESC.escrever_bit(MB['BAY']['DJL_CMD_FECHAR'], valor=0)
            self.fechar_dj()

        if LEI.ler_bit(MB['BAY']['RELE_RST_TRP']):
            ESC.escrever_bit(MB['BAY']['RELE_RST_TRP'], valor=0)
            self.resetar_dj()

        if self.dict['BAY']['debug_dj_abrir']:
            self.dict['BAY']['debug_dj_abrir'] = False
            self.abrir_dj()

        if self.dict['BAY']['debug_dj_fechar']:
            self.dict['BAY']['debug_dj_fechar'] = False
            self.fechar_dj()

        if self.dict['BAY']['debug_dj_reset']:
            self.dict['BAY']['debug_dj_reset'] = False
            self.resetar_dj()

        if self.dict['BAY']['debug_dj_fechar'] and self.dict['BAY']['debug_dj_abrir']:
            self.dict['BAY']['debug_dj_abrir'] = False
            self.dict['BAY']['debug_dj_fechar'] = False
            self.tripar_dj()


        if self.dict['BAY']['dj_fechado']:
            self.dict['BAY']['tensao_vs'] = self.dict['BAY']['tensao_vab']
        
        elif self.dict['SE']['dj_aberto']:
            self.dict['BAY']['tensao_vs'] = 0


        self.dict['BAY']['tensao_vab'] = np.random.normal(self.dict['BAY']['tensao_vab'], 50 * self.escala_ruido)
        self.dict['BAY']['tensao_vbc'] = np.random.normal(self.dict['BAY']['tensao_vbc'], 50 * self.escala_ruido)
        self.dict['BAY']['tensao_vca'] = np.random.normal(self.dict['BAY']['tensao_vca'], 50 * self.escala_ruido)
        self.dict['BAY']['potencia_mp'] = max(0, (np.random.normal(self.dict['SE']['potencia_se'] * 0.98, 10 * self.escala_ruido) - 20))
        self.dict['BAY']['potencia_mr'] = max(0, (np.random.normal(self.dict['SE']['potencia_se'] * 0.98, 10 * self.escala_ruido) - 20))


    def verificar_tensao_dj(self) -> "None":
        if not (USINA_TENSAO_MINIMA < self.dict['BAY']['tensao_vab'] < USINA_TENSAO_MAXIMA):
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


    def verificar_condicao_dj(self) -> "None":
        if self.dict['BAY']['dj_trip'] \
        or self.dict['BAY']['dj_fechado'] \
        or self.dict['BAY']['dj_falta_vcc'] \
        or not self.dict['BAY']['dj_aberto'] \
        or not self.dict['BAY']['dj_mola_carregada']:
            self.dict['BAY']['dj_condicao'] = False

        else:
            self.dict['BAY']['dj_condicao'] = True


    def abrir_dj(self) -> "None":
        print('[BAY] Comando de Abertura do Disjuntor do Bay acionado')

        if self.dict['BAY']['dj_mola_carregada']:

            if self.dict['BAY']['dj_fechado']:
                self.dict['BAY']['dj_trip'] = False
                self.dict['BAY']['dj_aberto'] = True
                self.dict['BAY']['dj_fechado'] = False

        else:
            self.tripar_dj(descr='Abriu antes de carregar a mola.')

        self.dict['BAY']['dj_mola_carregada'] = False


    def fechar_dj(self) -> "None":
        if self.dict['BAY']['dj_trip']:
            self.dict['BAY']['dj_falha'] = True
            self.tripar_dj(descr='Picou.')

        elif self.dict['BAY']['tensao_vs'] != 0:
            print("[SE] Não há como fechar o Disjuntor do BAY, pois há uma leitura de corrente VS!")

        elif self.dict['BAY']['dj_aberto']:
            if self.dict['BAY']['dj_condicao']:
                print('[BAY] Comando de Fechamento Disjuntor BAY')
                self.dict['BAY']['dj_fechado'] = True
                self.dict['BAY']['dj_aberto'] = False

            else:
                self.dict['BAY']['dj_falha'] = True
                self.tripar_dj(descr='Fechou antes de ter a condição de fechamento.')

        self.dict['BAY']['dj_mola_carregada'] = False


    def resetar_dj(self) -> "None":
        print('[BAY] Comando de Reset.')
        self.dict['BAY']['dj_trip'] = False
        self.dict['BAY']['dj_falha'] = False
        self.avisou_trip = False


    def tripar_dj(self, descr=None) -> "None":
        if not self.avisou_trip:
            self.avisou_trip = True
            self.dict['BAY']['dj_trip'] = True
            self.dict['BAY']['dj_falha'] = True
            self.dict['BAY']['dj_aberto'] = True
            self.dict['BAY']['dj_fechado'] = False
            self.dict['BAY']['dj_mola_carregada'] = False
            print(f'[BAY] TRIP Disjuntor! | Descrição: {descr}')


    def atualizar_modbus(self) -> "None":
        DB.set_words(MB['BAY']['LT_VS'], [round(self.dict['BAY']['tensao_vs'] / 1000)])
        DB.set_words(MB['BAY']['LT_VAB'], [round(self.dict['BAY']['tensao_vab'] / 1000)])
        DB.set_words(MB['BAY']['LT_VBC'], [round(self.dict['BAY']['tensao_vbc'] / 1000)])
        DB.set_words(MB['BAY']['LT_VCA'], [round(self.dict['BAY']['tensao_vca'] / 1000)])
        DB.set_words(MB['BAY']['LT_P_MP'], [round(max(0, self.dict['BAY']['potencia_mp']))])
        # DB.set_words(MB['BAY']['LT_P_MR'], [round(max(0, self.dict['BAY']['potencia_mr']))])

        if self.dict['BAY']['dj_secc'] and not self.dict['BRD']['djbay_secc']:
            self.dict['BRD']['djbay_secc'] = True
            ESC.escrever_bit(MB['BAY']['SECC_FECHADA'], valor=1)

        elif not self.dict['BAY']['dj_secc'] and self.dict['BRD']['djbay_secc']:
            self.dict['BRD']['djbay_secc'] = False
            ESC.escrever_bit(MB['BAY']['SECC_FECHADA'], valor=0)

        if self.dict['BAY']['dj_fechado'] and not self.dict['BRD']['djbay_fechado']:
            self.dict['BRD']['djbay_fechado'] = True
            ESC.escrever_bit(MB['BAY']['DJL_FECHADO'], valor=1)

        elif not self.dict['BAY']['dj_fechado'] and self.dict['BRD']['djbay_fechado']:
            self.dict['BRD']['djbay_fechado'] = False
            ESC.escrever_bit(MB['BAY']['DJL_FECHADO'], valor=0)

        if self.dict['BAY']['dj_mola_carregada'] and not self.dict['BRD']['djbay_mola']:
            self.dict['BRD']['djbay_mola'] = True
            ESC.escrever_bit(MB['BAY']['DJL_MOLA_CARREGADA'], valor=1)

        elif not self.dict['BAY']['dj_mola_carregada'] and self.dict['BRD']['djbay_mola']:
            self.dict['BRD']['djbay_mola'] = False
            ESC.escrever_bit(MB['BAY']['DJL_MOLA_CARREGADA'], valor=0)