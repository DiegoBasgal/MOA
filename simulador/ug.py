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

        if LEI.ler_bit(MB[f'UG{self.id}']['PARTIDA_CMD_SINCRONISMO']) or self.dict[f'UG{self.id}'][f'debug_partir']:
            ESC.escrever_bit(MB[f'UG{self.id}']['PARTIDA_CMD_SINCRONISMO'], valor=0)
            self.dict[f'UG{self.id}'][f'debug_partir'] = False
            self.partir()

        if LEI.ler_bit(MB[f'UG{self.id}']['PARADA_CMD_DESABILITA_UHLM']) or self.dict[f'UG{self.id}'][f'debug_parar']:
            ESC.escrever_bit(MB[f'UG{self.id}']['PARADA_CMD_DESABILITA_UHLM'], valor=0)
            self.dict[f'UG{self.id}'][f'debug_parar'] = False
            self.parar()

        if LEI.ler_bit(MB['TDA'][f'CP{self.id}_CMD_FECHAMENTO']) or self.dict[f'CP{self.id}'][f'thread_fechada']:
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_CMD_FECHAMENTO'], valor=0)
            self.dict[f'CP{self.id}'][f'thread_fechada'] = False
            Thread(target=lambda: self.controlar_fechamento_comporta()).start()

        if LEI.ler_bit(MB['TDA'][f'CP{self.id}_CMD_ABERTURA_TOTAL']) or self.dict[f'CP{self.id}'][f'thread_aberta']:
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_CMD_ABERTURA_TOTAL'], valor=0)
            self.dict[f'CP{self.id}'][f'thread_aberta'] = False
            Thread(target=lambda: self.controlar_abertura_comporta()).start()

        if LEI.ler_bit(MB['TDA'][f'CP{self.id}_CMD_ABERTURA_CRACKING']) or self.dict[f'CP{self.id}'][f'thread_cracking']:
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_CMD_ABERTURA_CRACKING'], valor=0)
            self.dict[f'CP{self.id}'][f'thread_cracking'] = False
            Thread(target=lambda: self.controlar_cracking_comporta()).start()

        self.setpoint = DB.get_words(MB[f'UG{self.id}']['SETPONIT'])[0]
        self.dict[f'UG{self.id}'][f'setpoint'] = self.setpoint

        self.dict[f'UG{self.id}'][f'q'] = self.calcular_q_ug(self.potencia)

        self.controlar_etapas()
        self.controlar_reservatorio()
        self.controlar_limites()
        self.controlar_horimetro()


    def partir(self) -> 'None':
        if self.dict[f'CP{self.id}'][f'aberta']:
            self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo = ETAPA_US
            print(f'[UG{self.id}] Comando de Partida')
        else:
            print(f'[UG{self.id}-CP{self.id}] Para partir a Unidade é necessário Abrir a Comporta primeiro!')


    def parar(self) -> 'None':
        if ETAPA_UP not in (self.etapa_alvo, self.etapa_atual):
            self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo = ETAPA_UP
            print(f'[UG{self.id}] Comando de Parada')


    def calcular_q_ug(self, potencia_kW) -> 'float':
        return 0.005610675 * potencia_kW if potencia_kW > 911 else 0


    def controlar_horimetro(self) -> 'None':
        if self.etapa_atual > ETAPA_UP:
            self.horimetro_hora += self.segundos_por_passo / 3600


    def controlar_reservatorio(self) -> 'None':
        if self.etapa_atual > ETAPA_UP and self.dict['TDA']['nv_montante'] < USINA_NV_MINIMO_OPERACAO:
            self.potencia = 0
            self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual = ETAPA_UPGM
            self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo = ETAPA_UPGM


    def controlar_limites(self) -> 'None':
        self.dict[f'UG{self.id}'][f'temp_fase_r'] = 110
        self.dict[f'UG{self.id}'][f'temp_fase_s'] = 110
        self.dict[f'UG{self.id}'][f'temp_fase_t'] = 110
        self.dict[f'UG{self.id}'][f'temp_mancal_guia'] = 110
        self.dict[f'UG{self.id}'][f'temp_mancal_casq_comb'] = 110
        self.dict[f'UG{self.id}'][f'temp_nucleo_gerador_1'] = 110
        self.dict[f'UG{self.id}'][f'temp_patins_mancal_comb_1'] = 110
        self.dict[f'UG{self.id}'][f'temp_patins_mancal_comb_2'] = 110
        self.dict[f'UG{self.id}'][f'temp_mancal_guia_interno_1'] = 110
        self.dict[f'UG{self.id}'][f'temp_mancal_guia_interno_2'] = 110
        self.dict[f'UG{self.id}'][f'temp_mancal_contra_esc_comb'] = 110
        self.dict[f'UG{self.id}'][f'temp_mancal_contra_esc_comb'] = 110
        self.dict[f'UG{self.id}'][f'pressao_turbina'] = np.random.normal(1.6, 1 * self.escala_ruido)


    def controlar_fechamento_comporta(self) -> 'None':
        if self.dict[f'UG{self.id}'][f'etapa_atual'] != ETAPA_UP:
            print(f'[UG{self.id}-CP{self.id}] A Unidade deve estar completamente Parada para realizar o Fechamento da Comporta!')

        elif self.dict[f'CP{self.id}'][f'aberta'] or self.dict[f'CP{self.id}'][f'cracking']:

            while self.dict[f'CP{self.id}'][f'progresso'] >= 0:
                self.dict[f'CP{self.id}'][f'progresso'] -= 0.0001

            self.dict[f'CP{self.id}'][f'cracking'] = False
            self.dict[f'CP{self.id}'][f'aberta'] = False
            self.dict[f'CP{self.id}'][f'fechada'] = True


    def controlar_abertura_comporta(self) -> 'None':
        if  self.dict['TDA']['lg_operando'] \
            or self.dict[f'CP{self.id}'][f'fechada'] \
            or not self.dict[f'CP{self.id}'][f'permissao'] \
            or self.dict[f'CP{2 if self.id == 1 else 1}'][f'operando']:
            print(f'[UG{self.id}-CP{self.id}] Não é possível realizar a Abertura da Comporta.')
            print(f'[UG{self.id}-CP{self.id}] Limpa Grades em operação.') if self.dict['TDA']['lg_operando'] else None
            print(f'[UG{self.id}-CP{self.id}] Comporta {self.id} sem Permissão de Abertura.') if not self.dict[f'CP{self.id}'][f'permissao'] else None
            print(f'[UG{self.id}-CP{self.id}] Comporta Fechada. Executar operação de Cracking primeiro!') if self.dict[f'CP{self.id}'][f'fechada'] else None
            print(f'[UG{self.id}-CP{self.id}] Comporta {2 if self.id == 1 else 1} em operação.') if self.dict[f'CP{2 if self.id == 1 else 1}'][f'operando'] else None

        elif self.dict[f'CP{self.id}'][f'cracking'] and not self.dict[f'CP{self.id}'][f'fechada']:
            self.dict[f'CP{self.id}'][f'aguardando'] = False
            self.dict[f'CP{self.id}'][f'operando'] = True

            while self.dict[f'CP{self.id}'][f'progresso'] <= 100:
                self.dict['TDA'][f'uh_disponivel'] = False
                self.dict[f'CP{self.id}'][f'progresso'] += 0.0001

            self.dict['TDA'][f'uh_disponivel'] = True
            self.dict[f'CP{self.id}'][f'operando'] = False
            self.dict[f'CP{self.id}'][f'fechada'] = False
            self.dict[f'CP{self.id}'][f'cracking'] = False
            self.dict[f'CP{self.id}'][f'aberta'] = True


    def controlar_cracking_comporta(self) -> 'None':
        if  self.dict['TDA']['lg_operando'] \
            or self.dict[f'CP{self.id}'][f'aberta'] \
            or self.dict[f'CP{2 if self.id == 1 else 1}'][f'operando']:
            print(f'[UG{self.id}-CP{self.id}] Não é possível realizar o Cracking da Comporta.')
            print(f'[UG{self.id}-CP{self.id}] Limpa Grades em operação.') if self.dict['TDA']['lg_operando'] else None
            print(f'[UG{self.id}-CP{self.id}] A Comporta ja está Aberta.') if self.dict[f'CP{self.id}'][f'aberta'] else None
            print(f'[UG{self.id}-CP{self.id}] Comporta {2 if self.id == 1 else 1} em operação.') if self.dict[f'CP{2 if self.id == 1 else 1}'][f'operando'] else None

        elif self.dict[f'CP{self.id}'][f'fechada'] and not self.dict[f'CP{self.id}'][f'aberta']:
            self.dict[f'CP{self.id}'][f'operando'] = True

            while self.dict[f'CP{self.id}'][f'progresso'] <= 30:
                self.dict['TDA'][f'uh_disponivel'] = False
                self.dict[f'CP{self.id}'][f'progresso'] += 0.00001

            self.dict['TDA'][f'uh_disponivel'] = True
            self.dict[f'CP{self.id}'][f'operando'] = False
            self.dict[f'CP{self.id}'][f'fechada'] = False
            self.dict[f'CP{self.id}'][f'aberta'] = False
            self.dict[f'CP{self.id}'][f'cracking'] = True

            Thread(target=lambda: self.equalizar_unidade_hidraulica()).start()


    def equalizar_unidade_hidraulica(self) -> 'None':
        print(f'[UG{self.id}-CP{self.id}] Equalizando pressao.')

        delay = time() + 5
        self.dict['TDA']['uh_disponivel'] = True
        self.dict[f'CP{self.id}']['equalizada'] = True

        while time() < delay:
            self.dict['TDA']['uh_disponivel'] = False
            self.dict[f'CP{self.id}']['equalizada'] = False

            if self.dict[f'CP{self.id}']['trip']:
                print(f'[UG{self.id}-CP{self.id}] Não foi possível Equalizar a Unidade Hidráulica! Fechando Comporta...')

                self.dict[f'CP{self.id}']['trip'] = False
                self.dict[f'CP{self.id}']['thread_fechada'] = True
                self.dict['TDA']['uh_disponivel'] = True
                return

        print(f'[UG{self.id}-CP{self.id}] A Unidade foi Equalizada, Permissão para Abrir comporta ativada!')
        self.dict['TDA']['uh_disponivel'] = True
        self.dict[f'CP{self.id}']['equalizada'] = True
        self.dict[f'CP{self.id}']['permissao'] = True
        self.dict[f'CP{self.id}']['aguardando'] = True


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
                    self.dict[f'UG{self.id}']['potencia'] = self.potencia = min(max(self.potencia, POT_MIN), POT_MAX)

                    if self.setpoint > self.potencia:
                        self.potencia += 20 * self.segundos_por_passo

                    else:
                        self.potencia -= 20 * self.segundos_por_passo

                    self.potencia = np.random.normal(self.potencia, 2 * self.escala_ruido)

                if self.dict['SE']['dj_aberto'] or self.dict['SE']['dj_trip']:
                    self.dict[f'UG{self.id}']['potencia'] = self.potencia = 0
                    self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual = ETAPA_UVD
                    self.dict[f'UG{self.id}'][f'etapa_alvo'] = self.etapa_alvo = ETAPA_US
                    self.tempo_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_transicao -= self.segundos_por_passo
                self.potencia -= 20.4167 * self.segundos_por_passo
                self.dict[f'UG{self.id}']['potencia'] = self.potencia

                if self.tempo_transicao <= -TEMPO_TRANS_US_UPS and self.potencia <= 0:
                    self.potencia = 0
                    self.dict[f'UG{self.id}'][f'etapa_atual'] = self.etapa_atual = ETAPA_UPS
                    self.tempo_transicao = 0


    def atualizar_modbus(self) -> 'None':
        DB.set_words(MB[f'UG{self.id}']['P'], [round(self.potencia)])
        DB.set_words(MB[f'UG{self.id}']['SETPONIT'], [self.setpoint])
        DB.set_words(MB[f'UG{self.id}']['HORIMETRO'], [np.floor(self.horimetro_hora)])
        DB.set_words(MB[f'UG{self.id}']['RV_ESTADO_OPERACAO'], [int(self.dict[f'UG{self.id}'][f'etapa_atual'])])
        DB.set_words(MB[f'UG{self.id}']['RV_ESTADO_OPERACAO_2'], [int(self.dict[f'UG{self.id}'][f'etapa_alvo'])])
        DB.set_words(MB[f'UG{self.id}']['ENTRADA_TURBINA_PRESSAO'], [round(self.dict[f'UG{self.id}'][f'pressao_turbina'] * 10)])
        DB.set_words(MB[f'UG{self.id}']['GERADOR_FASE_A_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_fase_r'])])
        DB.set_words(MB[f'UG{self.id}']['GERADOR_FASE_B_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_fase_s'])])
        DB.set_words(MB[f'UG{self.id}']['GERADOR_FASE_C_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_fase_t'])])
        DB.set_words(MB[f'UG{self.id}']['GERADOR_NUCL_ESTAT_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_nucleo_gerador_1'])])
        DB.set_words(MB[f'UG{self.id}']['MANCAL_GUIA_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_guia'])])
        DB.set_words(MB[f'UG{self.id}']['MANCAL_GUIA_INTE_1_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_guia_interno_1'])])
        DB.set_words(MB[f'UG{self.id}']['MANCAL_GUIA_INTE_2_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_guia_interno_2'])])
        DB.set_words(MB[f'UG{self.id}']['MANCAL_COMB_PATINS_1_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_patins_mancal_comb_1'])])
        DB.set_words(MB[f'UG{self.id}']['MANCAL_COMB_PATINS_2_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_patins_mancal_comb_2'])])
        DB.set_words(MB[f'UG{self.id}']['MANCAL_CASQ_COMB_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_casq_comb'])])
        DB.set_words(MB[f'UG{self.id}']['MANCAL_CONT_ESCO_COMB_TMP'], [round(self.dict[f'UG{self.id}'][f'temp_mancal_contra_esc_comb'])])

        # CP Fechada
        if self.dict[f'CP{self.id}']['fechada'] and not self.dict['BRD'][f'cp{self.id}_fechada']:
            self.dict['BRD'][f'cp{self.id}_fechada'] = True
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_FECHADA'], valor=1)

        elif not self.dict[f'CP{self.id}']['fechada'] and self.dict['BRD'][f'cp{self.id}_fechada']:
            self.dict['BRD'][f'cp{self.id}_fechada'] = False
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_FECHADA'], valor=0)

        # CP Aberta
        if self.dict[f'CP{self.id}']['aberta'] and not self.dict['BRD'][f'cp{self.id}_aberta']:
            self.dict['BRD'][f'cp{self.id}_aberta'] = True
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_ABERTA'], valor=1)

        elif not self.dict[f'CP{self.id}']['aberta'] and self.dict['BRD'][f'cp{self.id}_aberta']:
            self.dict['BRD'][f'cp{self.id}_aberta'] = False
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_ABERTA'], valor=0)

        # CP Cracking
        if self.dict[f'CP{self.id}']['cracking'] and not self.dict['BRD'][f'cp{self.id}_cracking']:
            self.dict['BRD'][f'cp{self.id}_cracking'] = True
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_CRACKING'], valor=1)

        elif not self.dict[f'CP{self.id}']['cracking'] and self.dict['BRD'][f'cp{self.id}_cracking']:
            self.dict['BRD'][f'cp{self.id}_cracking'] = False
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_CRACKING'], valor=0)

        # CP Operando
        if self.dict[f'CP{self.id}'][f'operando'] and not self.dict['BRD'][f'cp{self.id}_operando']:
            self.dict['BRD'][f'cp{self.id}_operando'] = True
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_OPERANDO'], valor=1)

        elif not self.dict[f'CP{self.id}'][f'operando'] and self.dict['BRD'][f'cp{self.id}_operando']:
            self.dict['BRD'][f'cp{self.id}_operando'] = False
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_OPERANDO'], valor=0)

        # CP Permissão
        if self.dict[f'CP{self.id}']['permissao'] and not self.dict['BRD'][f'cp{self.id}_permissao']:
            self.dict['BRD'][f'cp{self.id}_permissao'] = True
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_PERMISSIVOS_OK'], valor=0)

        elif not self.dict[f'CP{self.id}']['permissao'] and self.dict['BRD'][f'cp{self.id}_permissao']:
            self.dict['BRD'][f'cp{self.id}_permissao'] = False
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_PERMISSIVOS_OK'], valor=1)

        # CP Bloqueio
        if self.dict[f'CP{self.id}']['trip'] and not self.dict['BRD'][f'cp{self.id}_bloqueio']:
            self.dict['BRD'][f'cp{self.id}_bloqueio'] = True
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_BLQ_ATUADO'], valor=1)

        elif not self.dict[f'CP{self.id}']['trip'] and self.dict['BRD'][f'cp{self.id}_bloqueio']:
            self.dict['BRD'][f'cp{self.id}_bloqueio'] = False
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_BLQ_ATUADO'], valor=0)

        # CP Pressao Equalizada
        if self.dict[f'CP{self.id}']['equalizada'] and not self.dict['BRD'][f'cp{self.id}_equalizada']:
            self.dict['BRD'][f'cp{self.id}_equalizada'] = True
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_PRESSAO_EQUALIZADA'], valor=1)

        elif not self.dict[f'CP{self.id}']['equalizada'] and self.dict['BRD'][f'cp{self.id}_equalizada']:
            self.dict['BRD'][f'cp{self.id}_equalizada'] = False
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_PRESSAO_EQUALIZADA'], valor=0)

        # CP Aguardando Abertura
        if self.dict[f'CP{self.id}']['aguardando'] and not self.dict['BRD'][f'cp{self.id}_aguardando']:
            self.dict['BRD'][f'cp{self.id}_aguardando'] = True
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_AGUARDANDO_CMD_ABERTURA'], valor=1)

        elif not self.dict[f'CP{self.id}']['aguardando'] and self.dict['BRD'][f'cp{self.id}_aguardando']:
            self.dict['BRD'][f'cp{self.id}_aguardando'] = False
            ESC.escrever_bit(MB['TDA'][f'CP{self.id}_AGUARDANDO_CMD_ABERTURA'], valor=0)
