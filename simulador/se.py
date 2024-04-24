import numpy as np

from pyModbusTCP.server import DataBank as DB

from dicts.reg import *
from dicts.const import *
from funcs.leitura import Leitura as LEI
from funcs.escrita import Escrita as ESC
from funcs.temporizador import Temporizador

class Se:
    def __init__(self, dict_comp: 'dict'=None, tempo: 'Temporizador'=None) -> "None":
        self.dict = dict_comp

        self.escala_ruido = tempo.escala_ruido
        self.passo_simulacao = tempo.passo_simulacao
        self.segundos_por_passo = tempo.segundos_por_passo

        self.mola = 0
        self.tempo_carregamento_mola = 2

        self.aux = False
        self.avisou_trip = False


    def passo(self) -> "None":
        self.verificar_mola_dj()
        self.verificar_tensao_dj()
        self.verificar_condicao_dj()

        if LEI.ler_bit(REG_SASE['CMD_DISJ_LINHA_FECHA']):
            ESC.escrever_bit(REG_SASE['CMD_DISJ_LINHA_FECHA'], valor=0)
            self.fechar_dj()

        if LEI.ler_bit(REG_SASE['CMD_DISJ_LINHA_ABRE']):
            ESC.escrever_bit(REG_SASE['CMD_DISJ_LINHA_ABRE'], valor=0)
            self.abrir_dj()

        if LEI.ler_bit(REG_SASE['CMD_REARME_FALHAS']):
            ESC.escrever_bit(REG_SASE['CMD_REARME_FALHAS'], valor=0)
            self.dict['SE']['condic'] = False
            self.resetar_dj()

        if self.dict['SE']['debug_dj_abrir']:
            self.dict['SE']['debug_dj_abrir'] = False
            self.abrir_dj()

        if self.dict['SE']['debug_dj_fechar']:
            self.dict['SE']['debug_dj_fechar'] = False
            self.fechar_dj()

        if self.dict['SE']['debug_dj_reset']:
            self.dict['SE']['debug_dj_reset'] = False
            self.resetar_dj()

        if self.dict['SE']['debug_dj_fechar'] and self.dict['SE']['debug_dj_abrir']:
            self.dict['SE']['debug_dj_abrir'] = False
            self.dict['SE']['debug_dj_fechar'] = False
            self.tripar_dj()

        self.dict['SE']['potencia_se'] = self.dict['UG1']['potencia'] + self.dict['UG2']['potencia']


    def verificar_tensao_dj(self) -> "None":
        if not (USINA_TENSAO_MINIMA < self.dict['SE']['tensao_vab'] < USINA_TENSAO_MAXIMA):
            self.dict['SE']['dj_falta_vcc'] = True
            self.tripar_dj(descr='Tensão fora dos limites.')

        else:
            self.dict['SE']['dj_falta_vcc'] = False


    def verificar_mola_dj(self) -> "None":
        if not self.dict['SE']['dj_mola_carregada']:
            self.mola += self.segundos_por_passo

            if self.mola >= self.tempo_carregamento_mola:
                self.mola = 0
                self.dict['SE']['dj_mola_carregada'] = True


    def verificar_condicao_dj(self) -> "None":
        if self.dict['SE']['dj_trip'] \
        or self.dict['SE']['dj_fechado'] \
        or self.dict['SE']['dj_falta_vcc'] \
        or not self.dict['SE']['dj_aberto'] \
        or not self.dict['SE']['dj_mola_carregada']:
            self.dict['SE']['dj_condicao'] = False

        else:
            self.dict['SE']['dj_condicao'] = True


    def abrir_dj(self) -> "None":
        print('[SE] Comando de Abertura do Disjuntor da Subestação acionado')

        if self.dict['SE']['dj_mola_carregada']:
            self.dict['SE']['dj_trip'] = False
            self.dict['SE']['dj_aberto'] = True
            self.dict['SE']['dj_fechado'] = False

        else:
            self.tripar_dj(descr='Fechou antes de carregar a mola.')

        self.dict['SE']['dj_mola_carregada'] = False


    def fechar_dj(self) -> "None":
        if self.dict['SE']['dj_trip']:
            self.dict['SE']['dj_falha'] = True
            self.tripar_dj(descr='Picou.')

        elif self.dict['SE']['dj_aberto']:
            if self.dict['SE']['dj_condicao']:
                print('[SE] Comando de Fechamento Disjuntor SE')
                self.dict['SE']['dj_fechado'] = True
                self.dict['SE']['dj_aberto'] = False

            else:
                self.dict['SE']['dj_falha'] = True
                self.tripar_dj(descr='Fechou antes de ter a condição de fechamento.')

        self.dict['SE']['dj_mola_carregada'] = False


    def resetar_dj(self) -> "None":
        print('[SE]  Comando de Reset.')
        self.dict['SE']['dj_trip'] = False
        self.dict['SE']['dj_falha'] = False
        self.avisou_trip = False


    def tripar_dj(self, descr=None) -> "None":
        if not self.avisou_trip:
            self.avisou_trip = True
            self.dict['SE']['dj_trip'] = True
            self.dict['SE']['dj_falha'] = True
            self.dict['SE']['dj_aberto'] = True
            self.dict['SE']['dj_fechado'] = False
            self.dict['SE']['dj_mola_carregada'] = False
            print(f'[SE]  TRIP Disjuntor! | Descrição: {descr}')


    def atualizar_modbus(self) -> "None":
        DB.set_words(REG_RELE['SE']['P'], [round(self.dict['SE']['potencia_se'] / 1000)])
        DB.set_words(REG_RELE['SE']['VAB'], [round(self.dict['SE']['tensao_vab'] / 1000)])
        DB.set_words(REG_RELE['SE']['VBC'], [round(self.dict['SE']['tensao_vbc'] / 1000)])
        DB.set_words(REG_RELE['SE']['VCA'], [round(self.dict['SE']['tensao_vca'] / 1000)])

        # Disjuntor 52L Fechado
        if self.dict['SE']['dj_fechado'] and not self.dict['BRD']['djse_fechado']:
            self.dict['BRD']['djse_fechado'] = True
            ESC.escrever_bit(REG_SASE['SE_DISJUNTOR_LINHA_FECHADO'], valor=1)

        elif not self.dict['SE']['dj_fechado'] and self.dict['BRD']['djse_fechado']:
            self.dict['BRD']['djse_fechado'] = False
            ESC.escrever_bit(REG_SASE['SE_DISJUNTOR_LINHA_FECHADO'], valor=0)


