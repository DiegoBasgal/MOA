import numpy as np

from pyModbusTCP.server import DataBank as DB

from funcs.escrita import Escrita as ESC
from funcs.temporizador import Temporizador

from dicts.reg import *
from dicts.const import *
from dicts.dict import compartilhado

class Se:
    def __init__(self, tempo: Temporizador) -> None:
        self.dict = compartilhado

        self.escala_ruido = tempo.escala_ruido
        self.passo_simulacao = tempo.passo_simulacao
        self.segundos_por_passo = tempo.segundos_por_passo

        self.mola = 0
        self.tempo_carregamento_mola = 2
        self.avisou_trip = False

        self.b_sel = False
        self.b_mola = False

    def verificar_mola_dj(self) -> "None":
        if not self.dict['SE']['dj_mola_carregada']:
            self.mola += self.segundos_por_passo

            if self.mola >= self.tempo_carregamento_mola:
                self.mola = 0
                self.dict['SE']['dj_mola_carregada'] = True

    def passo(self) -> "None":
        self.verificar_mola_dj()
        self.verificar_tensao_dj()
        self.verificar_condicao_dj()

        if self.dict['SE']['debug_dj_fechar'] and self.dict['SE']['debug_dj_abrir']:
            self.dict['SE']['dj_aberto'] = True
            self.dict['SE']['dj_fechado'] = True
            self.dict['SE']['debug_dj_abrir'] = False
            self.dict['SE']['debug_dj_fechar'] = False
            self.tripar_dj()

        elif self.dict['SE']['debug_dj_fechar']:
            self.dict['SE']['debug_dj_fechar'] = False
            self.fechar_dj()

        elif self.dict['SE']['debug_dj_abrir']:
            self.dict['SE']['debug_dj_abrir'] = False
            self.abrir_dj()

        if self.dict['SE']['debug_dj_reset']:
            self.resetar_se()

    def atualizar_modbus(self) -> "None":
        if self.dict['SE']['dj_mola_carregada'] and not self.b_mola:
            self.b_mola = True
            ESC.escrever_bit(MB['SE']['DJL_MOLA_CARREGADA'], valor=1)

        elif not self.dict['SE']['dj_mola_carregada'] and self.b_mola:
            self.b_mola = False
            ESC.escrever_bit(MB['SE']['DJL_MOLA_CARREGADA'], valor=0)

        if not self.b_sel:
            ESC.escrever_bit(MB['SE']['DJL_SELETORA_REMOTO'], 1)
            ESC.escrever_bit(MB['SE']['TE_RELE_BUCHHOLZ_ALM'], 0)
            self.b_sel = True

    def verificar_tensao_dj(self) -> "None":
        if not (USINA_TENSAO_MINIMA < self.dict['BAY']['tensao_linha'] < USINA_TENSAO_MAXIMA):
            self.dict['SE']['dj_falta_vcc'] = True
            self.tripar_dj(descr='Tensão fora dos limites.')

        else:
            self.dict['SE']['dj_falta_vcc'] = False

    def abrir_dj(self) -> "None":
        print('[SE] Comando de Abertura do Disjuntor da Subestação acionado')

        if self.dict['SE']['dj_mola_carregada']:
            self.dict['SE']['dj_aberto'] = True
            self.dict['SE']['dj_fechado'] = False

        else:
            self.tripar_dj(descr='Fechou antes de carregar a mola.')

        self.dict['SE']['dj_mola_carregada'] = False

    def fechar_dj(self) -> "None":
        if self.dict['SE']['dj_trip']:
            self.dict['SE']['dj_falha'] = True
            self.tripar_dj(descr='Picou.')

        else:
            if not self.dict['BAY']['dj_fechado']:
                print('[SE] Não foi possível Fechar o Disjuntor da Subestação, pois o Disjuntor do Bay está Aberto!')

            elif not self.dict['SE']['dj_fechado']:
                print('[SE] Comando de Fechamento do Disjuntor da Subestação acionado')

                if self.dict['SE']['dj_condicao']:
                    self.dict['SE']['dj_aberto'] = False
                    self.dict['SE']['dj_fechado'] = True
                    self.dict['SE']['dj_mola_carregada'] = False
                    self.dict['SE']['tensao_linha'] = 23100

                else:
                    self.dict['SE']['dj_falha'] = True
                    self.tripar_dj(descr='Fechou antes de ter a condição de fechamento.')

    def tripar_dj(self, descr=None) -> "None":
        if not self.avisou_trip:
            self.avisou_trip = True
            self.dict['SE']['dj_trip'] = True
            self.dict['SE']['dj_aberto'] = True
            self.dict['SE']['dj_fechado'] = False
            self.dict['SE']['dj_mola_carregada'] = False
            self.dict['SE']['dj_falha'] = True
            print(f'[SE]  TRIP Disjuntor da Subestação! | Descrição: {descr}')

    def resetar_se(self) -> "None":
        if self.dict['BAY']['dj_aberto']:
            print('[SE]  Não é possível acionar o Comando de Reset Geral, pois o Disjuntor do Bay está Aberto!')
            self.dict['SE']['dj_trip'] = True
            self.dict['SE']['dj_aberto'] = False
            self.dict['SE']['dj_fechado'] = False
            self.dict['SE']['dj_falha'] = True
            self.dict['SE']['debug_dj_abrir'] = True
            self.dict['SE']['debug_dj_fechar'] = False
            self.dict['SE']['debug_dj_reset'] = False
        else:
            print('[SE]  Comando de Reset Geral acionado')
            self.dict['SE']['dj_trip'] = False
            self.dict['SE']['dj_falha'] = False
            self.dict['SE']['debug_dj_abrir'] = False
            self.dict['SE']['debug_dj_fechar'] = False
            self.dict['SE']['debug_dj_reset'] = False
            self.avisou_trip = False

    def verificar_condicao_dj(self) -> "None":
        if self.dict['SE']['dj_trip'] \
        or self.dict['SE']['dj_fechado'] \
        or self.dict['SE']['dj_falta_vcc'] \
        or not self.dict['SE']['dj_aberto'] \
        or not self.dict['SE']['dj_mola_carregada'] \
        or not self.dict['BAY']['dj_fechado']:
            self.dict['SE']['dj_condicao'] = False

        else:
            self.dict['SE']['dj_condicao'] = True
