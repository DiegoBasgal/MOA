from calendar import prmonth
import numpy as np

from time import  time
from threading import Thread
from pyModbusTCP.server import DataBank as DB

from dicts.reg import *
from dicts.const import *
from dicts.dict import compartilhado
from funcs.leitura import Leitura as LEI
from funcs.escrita import Escrita as ESC
from funcs.temporizador import Temporizador

class Unidade:
    def __init__(self, id: 'int'=None, dict_comp: 'dict'=None, tempo: 'Temporizador'=None) -> 'None':

        self.id = id
        self.dict = dict_comp

        self.escala_ruido = tempo.escala_ruido
        self.segundos_por_passo = tempo.segundos_por_passo

        self.potencia = 0
        self.setpoint = 0
        self.etapa_alvo = 0
        self.etapa_atual = 0
        self.horimetro_hora = 0
        self.tempo_transicao = 0

    def passo(self) -> 'None':

        if self.dict[f'UG{self.id}'][f'debug_setpoint'] >= 0:
            self.dict[f'UG{self.id}'][f'setpoint'] = self.dict[f'UG{self.id}'][f'debug_setpoint']
            self.dict[f'UG{self.id}'][f'debug_setpoint'] = -1

        if LEI.ler_bit(REG_UG[f'UG{self.id}']['CMD_REARME_FALHAS']):
            ESC.escrever_bit(REG_UG[f'UG{self.id}']['CMD_REARME_FALHAS'], valor=0)
            self.dict[f'UG{self.id}']['condic'] = False
            print(f"[UG{self.id}] Entrei no reset de passos")

        if LEI.ler_bit(REG_UG[f'UG{self.id}']['CMD_SINCRONISMO']) or self.dict[f'UG{self.id}'][f'debug_partir']:
            ESC.escrever_bit(REG_UG[f'UG{self.id}']['CMD_SINCRONISMO'], valor=0)
            self.dict[f'UG{self.id}'][f'debug_partir'] = False
            self.partir()

        if LEI.ler_bit(REG_UG[f'UG{self.id}']['CMD_PARADA_TOTAL']) or self.dict[f'UG{self.id}'][f'debug_parar']:
            ESC.escrever_bit(REG_UG[f'UG{self.id}']['CMD_PARADA_TOTAL'], valor=0)
            self.dict[f'UG{self.id}'][f'debug_parar'] = False
            self.parar()

        self.setpoint = DB.get_words(REG_RTV[f'UG{self.id}']['SETPOINT_POT_ATIVA_PU'])[0]
        self.dict[f'UG{self.id}'][f'setpoint'] = self.setpoint

        self.dict[f'UG{self.id}'][f'q'] = self.calcular_q_ug(self.potencia)

        self.controlar_etapas()
        self.controlar_reservatorio()
        self.controlar_limites()
        self.controlar_horimetro()


    def partir(self) -> 'None':
        if self.dict[f'UG{self.id}']['trip_condic']:
            print(f'[UG{self.id}] Máquina sem condição de partida. Normalizar antes de partir a Unidade.')
        else:
            self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo = ETAPA_US
            print(f'[UG{self.id}] Comando de Partida')


    def parar(self) -> 'None':
        if ETAPA_UP not in (self.etapa_alvo, self.etapa_atual):
            self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo = ETAPA_UP
            print(f'[UG{self.id}] Comando de Parada')


    def tripar(self) -> 'None':
        print(f'[UG{self.id}] TRIP!')
        self.potencia = 0
        self.etapa_alvo = 0
        self.dict[f'UG{self.id}'][f"etapa_alvo"] = 0


    def calcular_q_ug(self, potencia_kW) -> 'float':
        return 0.0106 * potencia_kW if potencia_kW > 200 else 0


    def controlar_horimetro(self) -> 'None':
        if self.etapa_atual > ETAPA_UP:
            self.horimetro_hora += self.segundos_por_passo / 3600


    def controlar_reservatorio(self) -> 'None':
        if self.etapa_atual > ETAPA_UP and self.dict['TDA']['nv_montante'] < USINA_NV_MINIMO_OPERACAO:
            self.potencia = 0
            self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual = ETAPA_UPGM
            self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo = ETAPA_UPGM


    def controlar_limites(self) -> 'None':
        self.dict[f"UG{self.id}"][f"temp_fase_r"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"][f"temp_fase_s"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"][f"temp_fase_t"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"][f"temp_nucleo_gerador_1"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"][f"temp_nucleo_gerador_2"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"][f"temp_nucleo_gerador_3"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"][f"temp_mancal_guia_casq"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"][f"temp_mancal_casq_comb"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"][f"temp_mancal_esc_comb"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"][f"temp_mancal_contra_esc_comb"] = np.random.normal(25, 1 * self.escala_ruido)
        # self.dict["UG"]["pressao_caixa_espiral_ug{}"] = np.random.normal(20, 1 * self.escala_ruido)



    def controlar_etapas(self) -> 'None':
        # Unidade Parada
        if self.etapa_atual == ETAPA_UP:
            self.potencia = 0

            if self.etapa_alvo == self.etapa_atual:
                self.tempo_transicao = 0
                self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_transicao += self.segundos_por_passo

                if self.tempo_transicao >= TEMPO_TRANS_US_UPS:
                    self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual = ETAPA_UPGM
                    self.tempo_transicao = 0

        # Unidade Pronta para Giro Mecânico
        if self.etapa_atual == ETAPA_UPGM:
            self.potencia = 0

            if self.etapa_alvo == self.etapa_atual:
                self.tempo_transicao = 0
                self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_transicao += self.segundos_por_passo

                if self.tempo_transicao >= TEMPO_TRANS_UPGM_UVD:
                    self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual = ETAPA_UVD
                    self.tempo_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_transicao -= self.segundos_por_passo

                if self.tempo_transicao <= -TEMPO_TRANS_UPGM_UP:
                    self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual = ETAPA_UP
                    self.tempo_transicao = 0

        # Unidade Vazio Desescitado
        if self.etapa_atual == ETAPA_UVD:
            self.potencia = 0

            if self.etapa_alvo == self.etapa_atual:
                self.tempo_transicao = 0
                self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_transicao += self.segundos_por_passo

                if self.tempo_transicao >= TEMPO_TRANS_UVD_UPS:
                    self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual = ETAPA_UPS
                    self.tempo_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_transicao -= self.segundos_por_passo

                if self.tempo_transicao <= -TEMPO_TRANS_UVD_UPGM:
                    self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual = ETAPA_UPGM
                    self.tempo_transicao = 0

        # Unidade Pronta para Sincronismo
        if self.etapa_atual == ETAPA_UPS:
            self.potencia = 0

            if self.etapa_alvo == self.etapa_atual:
                self.tempo_transicao = 0
                self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_transicao += self.segundos_por_passo

                if self.tempo_transicao >= TEMPO_TRANS_UPS_US and self.dict['SE']['dj_fechado']:
                    self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual = ETAPA_US
                    self.tempo_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_transicao -= self.segundos_por_passo

                if self.tempo_transicao <= -TEMPO_TRANS_UPS_UVD:
                    self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual = ETAPA_UVD
                    self.tempo_transicao = 0

        # Unidade Sincronizada
        if self.etapa_atual == ETAPA_US:
            if self.etapa_alvo == self.etapa_atual:
                self.tempo_transicao = 0
                self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo

                if self.dict['SE']['dj_fechado']:
                    self.dict['SE']['tensao_vs'] = self.dict['SE']['tensao_vab']
                    self.dict[f'UG{self.id}']['potencia'] = self.potencia = min(max(self.potencia, POT_MIN), POT_MAX)

                    if self.setpoint > self.potencia:
                        self.potencia += 10.4167 * self.segundos_por_passo

                    else:
                        self.potencia -= 10.4167 * self.segundos_por_passo

                    self.potencia = np.random.normal(self.potencia, 2 * self.escala_ruido)

                if self.dict['SE']['dj_aberto'] or self.dict['SE']['dj_trip']:
                    self.dict['SE']['tensao_vs'] = 0
                    self.dict[f'UG{self.id}']['potencia'] = self.potencia = 0
                    self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual = ETAPA_UVD
                    self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo = ETAPA_US
                    self.tempo_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_transicao -= self.segundos_por_passo
                self.potencia -= 10.4167 * self.segundos_por_passo
                self.dict[f'UG{self.id}']['potencia'] = self.potencia

                if self.tempo_transicao <= -TEMPO_TRANS_US_UPS and self.potencia <= 0:
                    self.potencia = 0
                    self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual = ETAPA_UPS
                    self.tempo_transicao = 0


    def atualizar_modbus(self) -> 'None':
        DB.set_words(REG_RELE[f'UG{self.id}']['P'], [round(self.dict[f'UG{self.id}']['potencia'])])
        DB.set_words(REG_RTV[f'UG{self.id}']['SETPOINT_POT_ATIVA_PU'], [self.setpoint])
        # DB.set_words(REG_UG[f'UG{self.id}']['HORIMETRO'], [np.floor(self.horimetro_hora)])
        DB.set_words(REG_UG[f'UG{self.id}']['STT_PASSO_ATUAL'], [int(self.dict[f'UG{self.id}'][f'etapa_atual'])])
        DB.set_words(REG_UG[f'UG{self.id}']['SST_PASSO_SELECIONADO'], [int(self.dict[f'UG{self.id}'][f'etapa_alvo'])])

        DB.set_words(REG_UG[f'UG{self.id}']['TEMP_GERADOR_FASE_A'], [round(self.dict[f'UG{self.id}'][f'temp_fase_r'])])
        DB.set_words(REG_UG[f'UG{self.id}']['TEMP_GERADOR_FASE_B'], [round(self.dict[f'UG{self.id}'][f'temp_fase_s'])])
        DB.set_words(REG_UG[f'UG{self.id}']['TEMP_GERADOR_FASE_C'], [round(self.dict[f'UG{self.id}'][f'temp_fase_t'])])
        DB.set_words(REG_UG[f'UG{self.id}']['TEMP_GERADOR_NUCLEO_1'], [round(self.dict[f'UG{self.id}'][f'temp_nucleo_gerador_1'])])
        DB.set_words(REG_UG[f'UG{self.id}']['TEMP_GERADOR_NUCLEO_2'], [round(self.dict[f'UG{self.id}'][f'temp_nucleo_gerador_2'])])
        DB.set_words(REG_UG[f'UG{self.id}']['TEMP_GERADOR_NUCLEO_3'], [round(self.dict[f'UG{self.id}'][f'temp_nucleo_gerador_3'])])
        DB.set_words(REG_UG[f'UG{self.id}']['TEMP_MANCAL_GUIA_CASQUILHO'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_guia_casq'])])
        DB.set_words(REG_UG[f'UG{self.id}']['TEMP_MANCAL_COMBINADO_CASQUILHO'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_casq_comb'])])
        DB.set_words(REG_UG[f'UG{self.id}']['TEMP_MANCAL_COMBINADO_ESCORA'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_esc_comb'])])
        DB.set_words(REG_UG[f'UG{self.id}']['TEMP_MANCAL_COMBINADO_CONTRA_ESCORA'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_contra_esc_comb'])])
