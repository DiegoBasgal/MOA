import numpy as np

import dicts.dict as dct

from time import  time
from threading import Thread
from pyModbusTCP.server import DataBank as DB

from dicts.reg import *
from dicts.const import *

from funcs.temporizador import Temporizador

class Unidade:
    def __init__(self, id, tempo: "Temporizador") -> "None":
        self.id = id
        self.dict = dct.compartilhado

        self.tempo = tempo

        # COPIA DE INFORMACOES DA CLASSE SITE
        self.escala_ruido = self.tempo.escala_ruido
        self.segundos_por_passo = self.tempo.segundos_por_passo

        self.potencia = 0
        self.setpoint = 0
        self.etapa_alvo = 1
        self.etapa_atual = 1
        self.horimetro_hora = 0
        self.tempo_na_transicao = 0

        self.avisou_trip = False

    def passo(self) -> "None":
        # DEBUG VIA GUI
        self.setpoint = self.dict[f'UG{self.id}'][f'setpoint']

        if self.dict[f'UG{self.id}'][f'debug_partir']:
            self.dict[f'UG{self.id}'][f'debug_partir'] = False
            self.partir()

        if self.dict[f'UG{self.id}'][f'debug_parar']:
            self.dict[f'UG{self.id}'][f'debug_parar'] = False
            self.parar()

        self.controle_horimetro()
        self.controle_reservatorio()
        self.controle_etapas()
        self.controle_temperaturas()

        self.dict[f'UG{self.id}'][f'q'] = self.q_ug(self.potencia)

        self.dict[f'UG{self.id}'][f'potencia'] = self.potencia
        self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual

        self.atualizar_modbus()

    def q_ug(self, potencia_kW) -> "float":
        return 0.005610675 * potencia_kW if potencia_kW > 911 else 0

    def partir(self) -> "None":
        if self.dict['TDA'][f'cp{self.id}_aberta']:
            self.etapa_alvo = ETAPA_US
            self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo
            print(f'[UG{self.id}] Comando de Partida')
        
        elif ETAPA_US in (self.etapa_alvo, self.etapa_atual):
            print(f'[UG{self.id}] A Unidade já recebeu o comando de Partida!')

        else:
            print(f'[UG{self.id}-CP{self.id}] Para partir a Unidade é necessário Abrir a Comporta primeiro!')

    def parar(self) -> "None":
        if ETAPA_UP not in (self.etapa_alvo, self.etapa_atual):
            self.etapa_alvo = ETAPA_UP
            self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo
            print(f'[UG{self.id}] Comando de Parada')
        else:
            print(f"[UG{self.id}] A Unidade já está Parada!")

    def controle_horimetro(self) -> "None":
        if self.etapa_atual > ETAPA_UP:
            self.horimetro_hora += self.segundos_por_passo / 3600

    def controle_reservatorio(self) -> "None":
        if (self.etapa_atual > ETAPA_UP and self.dict['TDA']['nv_montante'] < USINA_NV_MINIMO_OPERACAO):
            self.potencia = 0
            self.etapa_atual = ETAPA_UPGM
            self.etapa_alvo = ETAPA_UPGM

    def controle_temperaturas(self) -> "None":
        self.dict[f'UG{self.id}'][f'temp_fase_r'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f'UG{self.id}'][f'temp_fase_s'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f'UG{self.id}'][f'temp_fase_t'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f'UG{self.id}'][f'temp_mancal_guia'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f'UG{self.id}'][f'temp_mancal_casq_comb'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f'UG{self.id}'][f'temp_nucleo_gerador_1'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f'UG{self.id}'][f'temp_patins_mancal_comb_1'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f'UG{self.id}'][f'temp_patins_mancal_comb_2'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f'UG{self.id}'][f'temp_mancal_guia_interno_1'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f'UG{self.id}'][f'temp_mancal_guia_interno_2'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f'UG{self.id}'][f'temp_mancal_contra_esc_comb'] = np.random.normal(25, 1 * self.escala_ruido)


    def atualizar_modbus(self) -> "None":
        DB.set_words(MB[f'UG{self.id}_RV_ESTADO_OPERACAO'], [int(self.etapa_atual)])
        DB.set_words(MB[f'UG{self.id}_P'], [round(self.potencia)])
        DB.set_words(MB[f'UG{self.id}_HORIMETRO'], [np.floor(self.horimetro_hora)])
        DB.set_words(MB[f'UG{self.id}_GERADOR_FASE_A_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_fase_r'])])
        DB.set_words(MB[f'UG{self.id}_GERADOR_FASE_B_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_fase_s'])])
        DB.set_words(MB[f'UG{self.id}_GERADOR_FASE_C_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_fase_t'])])
        DB.set_words(MB[f'UG{self.id}_GERADOR_NUCL_ESTAT_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_nucleo_gerador_1'])])
        DB.set_words(MB[f'UG{self.id}_MANCAL_GUIA_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_guia'])])
        DB.set_words(MB[f'UG{self.id}_MANCAL_GUIA_INTE_1_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_guia_interno_1'])])
        DB.set_words(MB[f'UG{self.id}_MANCAL_GUIA_INTE_2_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_guia_interno_2'])])
        DB.set_words(MB[f'UG{self.id}_MANCAL_COMB_PATINS_1_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_patins_mancal_comb_1'])])
        DB.set_words(MB[f'UG{self.id}_MANCAL_COMB_PATINS_2_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_patins_mancal_comb_2'])])
        DB.set_words(MB[f'UG{self.id}_MANCAL_CASQ_COMB_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_casq_comb'])])
        DB.set_words(MB[f'UG{self.id}_MANCAL_CONT_ESCO_COMB_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_contra_esc_comb'])])
        DB.set_words(MB[f'UG{self.id}_ENTRADA_TURBINA_PRESSAO'], [round(10 * self.dict[f'UG{self.id}'][f'pressao_turbina'])])

    def controle_etapas(self) -> None:
        # COMPORTAMENTO self.ETAPAS
        self.etapa_alvo = self.dict[f'UG{self.id}'][f'etapa_alvo']

        # self.ETAPA UP
        if self.etapa_atual == ETAPA_UP:
            self.potencia = 0

            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo

                if self.tempo_na_transicao >= TEMPO_TRANS_US_UPS:
                    self.etapa_atual = ETAPA_UPGM
                    self.tempo_na_transicao = 0

        # self.ETAPA UPGM
        if self.etapa_atual == ETAPA_UPGM:
            self.potencia = 0

            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo

                if self.tempo_na_transicao >= TEMPO_TRANS_UPGM_UVD:
                    self.etapa_atual = ETAPA_UVD
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo

                if self.tempo_na_transicao <= -TEMPO_TRANS_UPGM_UP:
                    self.etapa_atual = ETAPA_UP
                    self.tempo_na_transicao = 0

        # self.ETAPA UVD
        if self.etapa_atual == ETAPA_UVD:
            self.potencia = 0

            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo

                if self.tempo_na_transicao >= TEMPO_TRANS_UVD_UPS:
                    self.etapa_atual = ETAPA_UPS
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo

                if self.tempo_na_transicao <= -TEMPO_TRANS_UVD_UPGM:
                    self.etapa_atual = ETAPA_UPGM
                    self.tempo_na_transicao = 0

        # self.ETAPA UPS
        if self.etapa_atual == ETAPA_UPS:
            self.potencia = 0

            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo

                if (self.tempo_na_transicao >= TEMPO_TRANS_UPS_US and self.dict['SE']['dj_fechado']):
                    self.etapa_atual = ETAPA_US
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo

                if self.tempo_na_transicao <= -TEMPO_TRANS_UPS_UVD:
                    self.etapa_atual = ETAPA_UVD
                    self.tempo_na_transicao = 0

        # self.ETAPA US
        if self.etapa_atual == ETAPA_US:
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo

                if (self.dict['SE']['dj_fechado'] and not self.dict['SE']['dj_trip']):
                    self.potencia = min(self.potencia, POT_MAX)
                    self.potencia = max(self.potencia, POT_MIN)

                    if self.setpoint > self.potencia:
                        self.potencia += 10.4167 * self.segundos_por_passo

                    else:
                        self.potencia -= 10.4167 * self.segundos_por_passo

                    self.potencia = np.random.normal(self.potencia, 1 * self.escala_ruido)

                if self.dict['SE']['dj_aberto'] or self.dict['SE']['dj_trip']:
                    self.potencia = 0
                    self.etapa_atual = ETAPA_UVD
                    self.etapa_alvo = ETAPA_US
                    self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.potencia -= 10.4167 * self.segundos_por_passo

                if (self.tempo_na_transicao <= -TEMPO_TRANS_US_UPS and self.potencia <= 0):
                    self.potencia = 0
                    self.etapa_atual = ETAPA_UPS
                    self.tempo_na_transicao = 0

        self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual
        # FIM COMPORTAMENTO self.ETAPAS

        if self.dict['TDA'][f'cp{self.id}_thread_aberta']:
            Thread(target=lambda: self.set_abertura_cp_ug()).start()
            self.dict['TDA'][f'cp{self.id}_thread_aberta'] = False

        if self.dict['TDA'][f'cp{self.id}_thread_fechada']:
            Thread(target=lambda: self.set_fechamento_cp_ug()).start()
            self.dict['TDA'][f'cp{self.id}_thread_fechada'] = False

        if self.dict['TDA'][f'cp{self.id}_thread_cracking']:
            Thread(target=lambda: self.set_cracking_cp_ug()).start()
            self.dict['TDA'][f'cp{self.id}_thread_cracking'] = False

    def set_abertura_cp_ug(self) -> "None":
        if self.dict['TDA'][f'cp{2 if self.id == 1 else 1}_operando']:
            print(f'[UG{self.id}-CP{self.id}] Não é possível realizar a Abertura da Comporta {1 if self.id == 1 else 2}, pois a Comporta {2 if self.id == 1 else 1} está em operação!')

        elif self.dict['TDA']['lg_operando']:
            print(f'[UG{self.id}-CP{self.id}] Não é possível realizar a Abertura da Comporta {self.id} pois o Limpa Grades se encontra em operação!')

        elif not self.dict['TDA'][f'cp{self.id}_permissao_abertura']:
            print(f'[UG{self.id}-CP{self.id}] As Permissões de Abertura da Comporta {self.id} ainda não foram ativadas!')

        elif self.dict['TDA'][f'cp{self.id}_cracking'] and not self.dict['TDA'][f'cp{self.id}_fechada']:
            self.dict['TDA'][f'cp{self.id}_operando'] = True

            while self.dict['TDA'][f'cp{self.id}_progresso'] <= 100:
                self.dict['TDA'][f'cp{self.id}_progresso'] += 0.00001

            self.dict['TDA'][f'cp{self.id}_operando'] = False
            self.dict['TDA'][f'cp{self.id}_fechada'] = False
            self.dict['TDA'][f'cp{self.id}_aberta'] = True
            self.dict['TDA'][f'cp{self.id}_cracking'] = False
            self.dict['TDA'][f'cp{self.id}_equalizar'] = False

        elif not self.dict['TDA'][f'cp{self.id}_cracking'] and self.dict['TDA'][f'cp{self.id}_fechada']:
            print(f'[UG{self.id}-CP{self.id}] A Comporta está Fechada, execute a operação de Cracking primeiro!')

        else:
            print(f'[UG{self.id}-CP{self.id}] A Comporta já está aberta.')

    def set_fechamento_cp_ug(self) -> "None":
        if self.dict[f'UG{self.id}'][f'etapa_atual'] != ETAPA_UP:
            print(f'[UG{self.id}-CP{self.id}] A Unidade deve estar completamente Parada para realizar o Fechamento da Comporta!')

        elif (self.dict['TDA'][f'cp{self.id}_aberta'] and not self.dict['TDA'][f'cp{self.id}_cracking']) \
            or (self.dict['TDA'][f'cp{self.id}_cracking'] and not self.dict['TDA'][f'cp{self.id}_aberta']):

            while self.dict['TDA'][f'cp{self.id}_progresso'] >= 0:
                self.dict['TDA'][f'cp{self.id}_progresso'] -= 0.00001

            self.dict['TDA'][f'cp{self.id}_fechada'] = True
            self.dict['TDA'][f'cp{self.id}_aberta'] = False
            self.dict['TDA'][f'cp{self.id}_cracking'] = False

        else:
            print(f'[UG{self.id}-CP{self.id}] A comporta já está Fechada!')

    def set_cracking_cp_ug(self) -> "None":
        if self.dict['TDA'][f'cp{2 if self.id == 1 else 1}_operando']:
            print(f'[UG{self.id}-CP{self.id}] Não é possível realizar a Abertura da Comporta {1 if self.id == 1 else 2}, pois a Comporta {2 if self.id == 1 else 1} está em operaçã!')

        elif self.dict['TDA']['lg_operando']:
            print(f'[UG{self.id}-CP{self.id}] Não é possível realizar o Cracking da Comporta {self.id} pois o Limpa Grades se encontra em operação!')

        elif self.dict['TDA'][f'cp{self.id}_fechada'] and not self.dict['TDA'][f'cp{self.id}_aberta']:
            self.dict['TDA'][f'cp{self.id}_operando'] = True

            while self.dict['TDA'][f'cp{self.id}_progresso'] <= 20:
                self.dict['TDA'][f'cp{self.id}_progresso'] += 0.00001

            self.dict['TDA'][f'cp{self.id}_operando'] = False
            self.dict['TDA'][f'cp{self.id}_fechada'] = False
            self.dict['TDA'][f'cp{self.id}_aberta'] = False
            self.dict['TDA'][f'cp{self.id}_cracking'] = True
            Thread(target=lambda: self.equalizar_uh_cp()).start()

        elif self.dict['TDA'][f'cp{self.id}_aberta'] and not self.dict['TDA'][f'cp{self.id}_fechada']:
            print(f'[UG{self.id}-CP{self.id}] A Comporta já está Aberta!')

        else:
            print(f'[UG{self.id}-CP{self.id}] A Comporta já está na posição de Cracking!')

    def equalizar_uh_cp(self) -> "None":
        print(f'[UG{self.id}-CP{self.id}] Aguardando Equalização de Pressão da Unidade Hidráulica da Comporta...')

        tempo_equalizacao = time() + 5
        while time() <= tempo_equalizacao:
            if self.dict['TDA'][f'cp{self.id}_trip']:
                print(f'[UG{self.id}-CP{self.id}] Não foi possível Equalizar a Unidade Hidráulica! Fechando Comporta...')
                self.dict['TDA'][f'cp{self.id}_thread_fechada'] = True
                self.dict['TDA'][f'cp{self.id}_trip'] = False
                return

        print(f'[UG{self.id}-CP{self.id}] A Unidade foi Equalizada, Permissão para Abrir comporta ativada!')
        self.dict['TDA'][f'cp{self.id}_permissao_abertura'] = True
