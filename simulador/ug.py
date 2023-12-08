import numpy as np

from time import  time
from threading import Thread
from pyModbusTCP.server import DataBank as DB

from dicts.reg import *
from dicts.const import *
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
        if self.dict[f'UG{self.id}']['debug_setpoint'] >= 0:
            self.dict[f'UG{self.id}']['setpoint'] = self.dict[f'UG{self.id}']['debug_setpoint']
            self.dict[f'UG{self.id}']['debug_setpoint'] = -1

        if DB.get_words(MB[f'UG{self.id}']['CMD_RESET_ALARMES'])[0]:
            DB.set_words(MB[f'UG{self.id}']['CMD_RESET_ALARMES'], [0])
            self.dict[f'UG{self.id}']['condic'] = False
            print(f"[UG{self.id}] Entrei no reset de passos")

        if DB.get_words(MB[f'UG{self.id}']['CMD_OPER_US']) or self.dict[f'UG{self.id}']['debug_partir']:
            DB.set_words(MB[f'UG{self.id}']['CMD_OPER_US'], [0])
            self.dict[f'UG{self.id}']['debug_partir'] = False
            if self.dict['TDA'][f'cp{self.id}_fechada'] and not self.dict['TDA'][f'cp{self.id}_aberta']:
                Thread(target=lambda: self.abrir_comporta()).start()
            elif self.dict['TDA'][f'cp{self.id}_aberta'] and not self.dict['TDA'][f'cp{self.id}_fechada']:
                self.partir()

        if DB.get_words(MB[f'UG{self.id}']['CMD_OPER_UP']) or self.dict[f'UG{self.id}']['debug_parar']:
            DB.set_words(MB[f'UG{self.id}']['CMD_OPER_UP'], [0])
            self.dict[f'UG{self.id}']['debug_parar'] = False
            self.parar()

        self.setpoint = DB.get_words(MB[f'UG{self.id}']['CRTL_POT_ALVO'])[0]
        self.dict[f'UG{self.id}']['setpoint'] = self.setpoint
        self.dict[f'UG{self.id}']['q'] = self.calcular_q_ug(self.potencia)

        # Lógica Exclusiva para acionamento de condicionadores TESTE:
        if self.dict[f'UG{self.id}']['condic'] and not self.dict['BRD'][f'ug{self.id}_condic']:
            self.dict['BRD'][f'ug{self.id}_condic'] = True
            self.tripar()
            ESC.escrever_bit(MB[f'UG{self.id}']['CONDICIONADOR'], valor=1)

        elif not self.dict[f'UG{self.id}']['condic'] and self.dict['BRD'][f'ug{self.id}_condic']:
            self.dict['BRD'][f'ug{self.id}_condic'] = False
            ESC.escrever_bit(MB[f'UG{self.id}']['CONDICIONADOR'], valor=0)

        self.controlar_etapas()
        self.controlar_reservatorio()
        self.controlar_limites()
        self.controlar_horimetro()


    def partir(self) -> 'None':
        if ETAPA_UP in (self.etapa_alvo, self.etapa_atual) and not self.dict[f'UG{self.id}']['condic']:
            self.dict[f'UG{self.id}']['etapa_alvo'] = self.etapa_alvo = ETAPA_US
            print(f'[UG{self.id}] Comando de Partida')

        elif self.dict[f'UG{self.id}']['condic']:
            print(f'[UG{self.id}] Máquina sem condição de partida.')


    def parar(self) -> 'None':
        if ETAPA_UP not in (self.etapa_alvo, self.etapa_atual):
            self.dict[f'UG{self.id}']['etapa_alvo'] = self.etapa_alvo = ETAPA_UP
            print(f'[UG{self.id}] Comando de Parada')


    def tripar(self) -> 'None':
        print(f'[UG{self.id}] TRIP!')
        self.potencia = 0
        self.etapa_alvo = 0
        self.dict[f'UG{self.id}']['etapa_alvo'] = 0


    def calcular_q_ug(self, potencia_kW) -> 'float':
        return 0.005610675 * potencia_kW if potencia_kW > 911 else 0


    def controlar_horimetro(self) -> 'None':
        if self.etapa_atual > ETAPA_UP:
            self.horimetro_hora += self.segundos_por_passo / 3600


    def controlar_reservatorio(self) -> 'None':
        if self.etapa_atual > ETAPA_UP and self.dict['TDA']['nv_montante'] < USINA_NV_MINIMO_OPERACAO:
            self.potencia = 0
            self.dict[f'UG{self.id}']['etapa_atual'] = self.etapa_atual = ETAPA_UPGM
            self.dict[f'UG{self.id}']['etapa_alvo'] = self.etapa_alvo = ETAPA_UPGM


    def controlar_limites(self) -> 'None':
        self.dict[f'UG{self.id}']['temp_fase_r'] = 60
        self.dict[f'UG{self.id}']['temp_fase_s'] = 60
        self.dict[f'UG{self.id}']['temp_fase_t'] = 60
        self.dict[f'UG{self.id}']['temp_mancal_gerador_la_1'] = 60
        self.dict[f'UG{self.id}']['temp_mancal_gerador_la_2'] = 60
        self.dict[f'UG{self.id}']['temp_mancal_gerador_lna_1'] = 60
        self.dict[f'UG{self.id}']['temp_mancal_gerador_lna_2'] = 60
        self.dict[f'UG{self.id}']['temp_mancal_turbina_radial'] = 60
        self.dict[f'UG{self.id}']['temp_mancal_turbina_escora'] = 60
        self.dict[f'UG{self.id}']['temp_mancal_turbina_contra_escora'] = 60


    def abrir_comporta(self) -> 'None':
        self.dict['TDA'][f'cp{self.id}_fechada'] = False

        # Temporizador para cracking da comporta
        tc = time() + TEMPO_CRACKING_CP_UGS
        t1 = t2 = time()

        while time() < tc:
            self.dict['TDA'][f'uh{1 if self.id in (1,3) else 2}_disponivel'] = False
            if t2 - t1 >= 1:
                t1 = t2
                t2 = time()
                self.dict['TDA'][f'cp{self.id}_setpoint'] += (1/TEMPO_CRACKING_CP_UGS)*20
            else:
                t2 = time()

        # Temporizador para enchimento do conduto das unidades
        ta = time() + TEMPO_ENCH_CONDU_CP_UGS
        t1 = t2 = time()

        while time() < ta:
            if t2 - t1 >= 1:
                t1 = t2
                t2 = time()
            else:
                t2 = time()

        # Temporizador para abertura da comporta
        ta = time() + TEMPO_ABERTURA_CP_UGS
        t1 = t2 = time()

        while time() < ta:
            self.dict['TDA'][f'uh{1 if self.id in (1,3) else 2}_disponivel'] = False
            if t2 - t1 >= 1:
                t1 = t2
                t2 = time()
                self.dict['TDA'][f'cp{self.id}_setpoint'] += (1/TEMPO_ABERTURA_CP_UGS)*80
            else:
                t2 = time()

        self.dict['TDA'][f'cp{self.id}_aberta'] = True


    def fechar_comporta(self) -> 'None':
        if self.dict[f'UG{self.id}']['etapa_atual'] == ETAPA_UP and self.dict['TDA'][f'cp{self.id}_aberta']:
            self.dict['TDA'][f'cp{self.id}_aberta'] = False

            while self.dict[f'TDA'][f'cp{self.id}_setpoint'] >= 0:
                self.dict[f'TDA'][f'cp{self.id}_setpoint'] -= 1000

            self.dict['TDA'][f'cp{self.id}_fechada'] = True


    def controlar_etapas(self) -> 'None':
        # Unidade Parada
        if self.etapa_atual == ETAPA_UP:
            self.potencia = 0

            if self.etapa_alvo == self.etapa_atual:
                self.tempo_transicao = 0
                self.dict[f'UG{self.id}']['etapa_alvo'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_transicao += self.segundos_por_passo

                if self.tempo_transicao >= TEMPO_TRANS_US_UPS:
                    self.dict[f'UG{self.id}']['etapa_atual'] = self.etapa_atual = ETAPA_UPGM
                    self.tempo_transicao = 0

        # Unidade Pronta para Giro Mecânico
        if self.etapa_atual == ETAPA_UPGM:
            self.potencia = 0

            if self.etapa_alvo == self.etapa_atual:
                self.tempo_transicao = 0
                self.dict[f'UG{self.id}']['etapa_alvo'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_transicao += self.segundos_por_passo

                if self.tempo_transicao >= TEMPO_TRANS_UPGM_UVD:
                    self.dict[f'UG{self.id}']['etapa_atual'] = self.etapa_atual = ETAPA_UVD
                    self.tempo_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_transicao -= self.segundos_por_passo

                if self.tempo_transicao <= -TEMPO_TRANS_UPGM_UP:
                    self.dict[f'UG{self.id}']['etapa_atual'] = self.etapa_atual = ETAPA_UP
                    self.tempo_transicao = 0

        # Unidade Vazio Desescitado
        if self.etapa_atual == ETAPA_UVD:
            self.potencia = 0

            if self.etapa_alvo == self.etapa_atual:
                self.tempo_transicao = 0
                self.dict[f'UG{self.id}']['etapa_alvo'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_transicao += self.segundos_por_passo

                if self.tempo_transicao >= TEMPO_TRANS_UVD_UPS:
                    self.dict[f'UG{self.id}']['etapa_atual'] = self.etapa_atual = ETAPA_UPS
                    self.tempo_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_transicao -= self.segundos_por_passo

                if self.tempo_transicao <= -TEMPO_TRANS_UVD_UPGM:
                    self.dict[f'UG{self.id}']['etapa_atual'] = self.etapa_atual = ETAPA_UPGM
                    self.tempo_transicao = 0

        # Unidade Pronta para Sincronismo
        if self.etapa_atual == ETAPA_UPS:
            self.potencia = 0

            if self.etapa_alvo == self.etapa_atual:
                self.tempo_transicao = 0
                self.dict[f'UG{self.id}']['etapa_alvo'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_transicao += self.segundos_por_passo

                if self.tempo_transicao >= TEMPO_TRANS_UPS_US and self.dict['SE']['dj_fechado']:
                    self.dict[f'UG{self.id}']['etapa_atual'] = self.etapa_atual = ETAPA_US
                    self.tempo_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_transicao -= self.segundos_por_passo

                if self.tempo_transicao <= -TEMPO_TRANS_UPS_UVD:
                    self.dict[f'UG{self.id}']['etapa_atual'] = self.etapa_atual = ETAPA_UVD
                    self.tempo_transicao = 0

        # Unidade Sincronizada
        if self.etapa_atual == ETAPA_US:
            if self.etapa_alvo == self.etapa_atual:
                self.tempo_transicao = 0
                self.dict[f'UG{self.id}']['etapa_alvo'] = self.etapa_alvo

                if self.dict['SE']['dj_fechado']:
                    self.dict[f'UG{self.id}']['potencia'] = self.potencia = min(max(self.potencia, POT_MIN), POT_MAX)

                    if self.setpoint > self.potencia:
                        self.potencia += 10.4167 * self.segundos_por_passo

                    else:
                        self.potencia -= 10.4167 * self.segundos_por_passo

                    self.potencia = np.random.normal(self.potencia, 2 * self.escala_ruido)

                if self.dict['SE']['dj_aberto'] or self.dict['SE']['dj_trip']:
                    self.dict[f'UG{self.id}']['potencia'] = self.potencia = 0
                    self.dict[f'UG{self.id}']['etapa_atual'] = self.etapa_atual = ETAPA_UVD
                    self.dict[f'UG{self.id}']['etapa_alvo'] = self.etapa_alvo = ETAPA_US
                    self.tempo_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_transicao -= self.segundos_por_passo
                self.potencia -= 10.4167 * self.segundos_por_passo
                self.dict[f'UG{self.id}']['potencia'] = self.potencia

                if self.tempo_transicao <= -TEMPO_TRANS_US_UPS and self.potencia <= 0:
                    self.potencia = 0
                    self.dict[f'UG{self.id}']['etapa_atual'] = self.etapa_atual = ETAPA_UPS
                    self.tempo_transicao = 0


    def atualizar_modbus(self) -> 'None':
        DB.set_words(MB[f'UG{self.id}']['POT_ATIVA_MEDIA'], [round(self.potencia)])
        DB.set_words(MB[f'UG{self.id}']['CRTL_POT_ALVO'], [self.setpoint])
        DB.set_words(MB[f'UG{self.id}']['OPER_ETAPA_ATUAL'], [int(self.dict[f'UG{self.id}']['etapa_atual'])])
        DB.set_words(MB[f'UG{self.id}']['OPER_ETAPA_ALVO'], [int(self.dict[f'UG{self.id}']['etapa_alvo'])])
        DB.set_words(MB[f'UG{self.id}']['ENTRADA_TURBINA_PRESSAO'], [round(self.dict[f'UG{self.id}'][f'pressao_turbina'] * 10)])
        DB.set_words(MB[f'UG{self.id}']['GERADOR_FASE_R_TMP'], [round(self.dict[f'UG{self.id}']['temp_fase_r'])])
        DB.set_words(MB[f'UG{self.id}']['GERADOR_FASE_S_TMP'], [round(self.dict[f'UG{self.id}']['temp_fase_s'])])
        DB.set_words(MB[f'UG{self.id}']['GERADOR_FASE_T_TMP'], [round(self.dict[f'UG{self.id}']['temp_fase_t'])])
        DB.set_words(MB[f'UG{self.id}']['MANCAL_GERADOR_LA_1_TMP'], [round(self.dict[f'UG{self.id}']['temp_mancal_gerador_la_1'])])
        DB.set_words(MB[f'UG{self.id}']['MANCAL_GERADOR_LA_2_TMP'], [round(self.dict[f'UG{self.id}']['temp_mancal_gerador_la_2'])])
        DB.set_words(MB[f'UG{self.id}']['MANCAL_GERADOR_LNA_2_TMP'], [round(self.dict[f'UG{self.id}']['temp_mancal_gerador_lna_1'])])
        DB.set_words(MB[f'UG{self.id}']['MANCAL_GERADOR_LNA_1_TMP'], [round(self.dict[f'UG{self.id}']['temp_mancal_gerador_lna_2'])])
        DB.set_words(MB[f'UG{self.id}']['MANCAL_TURBINA_RADIAL'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_turbina_radial'])])
        DB.set_words(MB[f'UG{self.id}']['MANCAL_TURBINA_ESCORA'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_turbina_escora'])])
        DB.set_words(MB[f'UG{self.id}']['MANCAL_TURBINA_CONTRA_ESCORA'], [round(self.dict[f'UG{self.id}']['temp_mancal_turbina_contra_escora'])])