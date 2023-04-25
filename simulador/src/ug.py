import logging
import numpy as np

from time import  time
from threading import Thread
from time_handler import TimeHandler

from dicionarios.const import *

logger = logging.getLogger('__main__')

class Ug:
    def __init__(self, id, shared_dict, time_handler: TimeHandler) -> None:
        self.id = id
        self.dict = shared_dict

        # COPIA DE INFORMACOES DA CLASSE SITE
        self.escala_ruido = time_handler.escala_ruido
        self.segundos_por_passo = time_handler.segundos_por_passo

        self.potencia = 0
        self.setpoint = 0
        self.etapa_alvo = 1
        self.etapa_atual = 1
        self.horimetro_hora = 0
        self.tempo_na_transicao = 0

        self.avisou_trip = False

    def passo(self):
        # DEBUG VIA GUI
        self.setpoint = self.dict['UG'][f'setpoint_kw_ug{self.id}']

        if self.dict['UG'][f'debug_partir_ug{self.id}']:
            self.dict['UG'][f'debug_partir_ug{self.id}'] = False
            self.partir()

        if self.dict['UG'][f'debug_parar_ug{self.id}']:
            self.dict['UG'][f'debug_parar_ug{self.id}'] = False
            self.parar()

        if self.dict['UG'][f'trip_ug{self.id}']:
            self.tripar(1, 'Trip Elétrico.')
            self.dict['UG'][f'trip_ug{self.id}'] = False

        if self.dict['UG'][f'reconhece_reset_ug{self.id}']:
            self.dict['UG'][f'reconhece_reset_ug{self.id}'] = False
            self.reconhece_reset()

        self.controle_horimetro()
        self.controle_reservatorio()
        self.controle_etapas()
        self.controle_temperaturas()

        self.dict['UG'][f'q_ug{self.id}'] = self.q_ug(self.potencia)

        self.dict['UG'][f'potencia_kw_ug{self.id}'] = self.potencia
        self.dict['UG'][f'etapa_atual_ug{self.id}'] = self.etapa_atual

        # FIM DEBUG VIA GUI

    def q_ug(self, potencia_kW):
        return 0.005610675 * potencia_kW if potencia_kW > 911 else 0

    def partir(self):
        if self.dict['UG'][f'comporta_aberta_ug{self.id}']:
            self.etapa_alvo = ETAPA_US
            self.dict['UG'][f'etapa_alvo_ug{self.id}'] = self.etapa_alvo
            logger.info(f'[UG{self.id}] Comando de partida')
        else:
            logger.warning(f'[UG{self.id}] Para partir a ug é necessário abrir a comporta primeiro!')

    def parar(self):
        self.etapa_alvo = ETAPA_UP
        self.dict['UG'][f'etapa_alvo_ug{self.id}'] = self.etapa_alvo
        logger.info(f'[UG{self.id}] Comando de parada')

    def tripar(self, flag, desc=None):
        self.potencia = 0
        self.etapa_alvo = ETAPA_UPGM
        self.etapa_atual = ETAPA_UPGM
        self.dict['UG'][f'flags_ug{self.id}'] = flag
        if not self.avisou_trip:
            self.avisou_trip = True
            logger.warning(F'[UG{self.id}] Trip!. {desc}')
        self.dict['UG'][f'etapa_alvo_ug{self.id}'] = self.etapa_alvo

    def reconhece_reset(self) -> None:
        self.avisou_trip = False
        self.dict['UG'][f'flags_ug{self.id}'] = 0
        logger.info(f'[UG{self.id}] Reconhece Reset.')

    def controle_horimetro(self) -> None:
        if self.etapa_atual > ETAPA_UP:
            self.horimetro_hora += self.segundos_por_passo / 3600
        
    def controle_reservatorio(self) -> None:
        if (self.etapa_atual > ETAPA_UP and self.dict['USN']['nv_montante'] < USINA_NV_MINIMO_OPERACAO):
            self.potencia = 0
            self.etapa_atual = ETAPA_UPGM
            self.etapa_alvo = ETAPA_UPGM
    
    def controle_temperaturas(self) -> None:
        self.dict['UG'][f'temperatura_ug{self.id}_fase_r'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict['UG'][f'temperatura_ug{self.id}_fase_s'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict['UG'][f'temperatura_ug{self.id}_fase_t'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict['UG'][f'temperatura_ug{self.id}_mancal_guia'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict['UG'][f'temperatura_ug{self.id}_mancal_casq_comb'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict['UG'][f'temperatura_ug{self.id}_nucleo_gerador_1'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict['UG'][f'temperatura_ug{self.id}_patins_mancal_comb_1'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict['UG'][f'temperatura_ug{self.id}_patins_mancal_comb_2'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict['UG'][f'temperatura_ug{self.id}_mancal_guia_interno_1'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict['UG'][f'temperatura_ug{self.id}_mancal_guia_interno_2'] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict['UG'][f'temperatura_ug{self.id}_mancal_contra_esc_comb'] = np.random.normal(25, 1 * self.escala_ruido)

    def controle_etapas(self) -> None:
        # COMPORTAMENTO self.ETAPAS
        self.etapa_alvo = self.dict['UG'][f'etapa_alvo_ug{self.id}']

        # self.ETAPA UP
        if self.etapa_atual == ETAPA_UP:
            self.potencia = 0
            
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.dict['UG'][f'etapa_alvo_ug{self.id}'] = self.etapa_alvo

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
                self.dict['UG'][f'etapa_alvo_ug{self.id}'] = self.etapa_alvo

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
                self.dict['UG'][f'etapa_alvo_ug{self.id}'] = self.etapa_alvo

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
                self.dict['UG'][f'etapa_alvo_ug{self.id}'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo

                if (self.tempo_na_transicao >= TEMPO_TRANS_UPS_US and self.dict['DJ']['dj52L_fechado']):
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
                self.dict['UG'][f'etapa_alvo_ug{self.id}'] = self.etapa_alvo

                if (self.dict['DJ']['dj52L_fechado'] and not self.dict['DJ']['dj52L_trip']):
                    self.potencia = min(self.potencia, POT_MAX)
                    self.potencia = max(self.potencia, POT_MIN)

                    if self.setpoint > self.potencia:
                        self.potencia += 10.4167 * self.segundos_por_passo

                    else:
                        self.potencia -= 10.4167 * self.segundos_por_passo

                    self.potencia = np.random.normal(self.potencia, 1 * self.escala_ruido)

                if self.dict['DJ']['dj52L_aberto'] or self.dict['DJ']['dj52L_trip']:
                    self.potencia = 0
                    self.etapa_atual = ETAPA_UVD
                    self.etapa_alvo = ETAPA_US
                    self.dict['UG'][f'etapa_alvo_ug{self.id}'] = self.etapa_alvo
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.potencia -= 10.4167 * self.segundos_por_passo

                if (self.tempo_na_transicao <= -TEMPO_TRANS_US_UPS and self.potencia <= 0):
                    self.potencia = 0
                    self.etapa_atual = ETAPA_UPS
                    self.tempo_na_transicao = 0

        self.dict['UG'][f'etapa_atual_ug{self.id}'] = self.etapa_atual
        # FIM COMPORTAMENTO self.ETAPAS
    
        if self.dict['UG']['thread_comp_aberta_ug1'] == True:
            Thread(target=lambda: self.set_abertura_comporta_ug1()).start()
            self.dict['UG']['thread_comp_aberta_ug1'] = False
    
        if self.dict['UG']['thread_comp_fechada_ug1'] == True:
            Thread(target=lambda: self.set_fechamento_comporta_ug1()).start()
            self.dict['UG']['thread_comp_fechada_ug1'] = False
    
        if self.dict['UG']['thread_comp_cracking_ug1'] == True:
            Thread(target=lambda: self.set_cracking_comporta_ug1()).start()
            self.dict['UG']['thread_comp_cracking_ug1'] = False
        
        if self.dict['UG']['thread_comp_aberta_ug2'] == True:
            Thread(target=lambda: self.set_abertura_comporta_ug2()).start()
            self.dict['UG']['thread_comp_aberta_ug2'] = False
    
        if self.dict['UG']['thread_comp_fechada_ug2'] == True:
            Thread(target=lambda: self.set_fechamento_comporta_ug2()).start()
            self.dict['UG']['thread_comp_fechada_ug2'] = False
    
        if self.dict['UG']['thread_comp_cracking_ug2'] == True:
            Thread(target=lambda: self.set_cracking_comporta_ug2()).start()
            self.dict['UG']['thread_comp_cracking_ug2'] = False

    def set_abertura_comporta_ug1(self):
        if self.dict['UG']['comporta_operando_ug2'] == True:
            logger.info('Não é possível realizar a abertura da comporta 1 pois a comporta 2 está em operação.')

        elif self.dict['UG']['limpa_grades_operando'] == True:
            logger.info('Não é possível realizar a abertura da comporta 1 pois o limpa grades se encontra em operação.')

        elif self.dict['UG']['permissao_abrir_comporta_ug1'] == False:
            logger.info('As permissões de abertura da comporta 1 ainda não foram ativadas.')

        elif self.dict['UG']['comporta_cracking_ug1'] == True and self.dict['UG']['comporta_fechada_ug1'] == False:
            self.dict['UG']['comporta_operando_ug1'] = True
            while self.dict['UG']['progresso_ug1'] <= 100:
                self.dict['UG']['progresso_ug1'] += 0.00001
            self.dict['UG']['comporta_operando_ug1'] = False
            self.dict['UG']['comporta_fechada_ug1'] = False
            self.dict['UG']['comporta_aberta_ug1'] = True
            self.dict['UG']['comporta_cracking_ug1'] = False
            self.dict['UG']['equalizar_ug1'] = False

        elif self.dict['UG']['comporta_cracking_ug1'] == False and self.dict['UG']['comporta_fechada_ug1'] == True:
            logger.info('A comporta está fechada, execute a operação de cracking primeiro!')
        
        else:
            logger.info('A comporta já está aberta.')
        return True
    
    def set_fechamento_comporta_ug1(self):
        if self.dict['UG']['etapa_atual_ug1'] != ETAPA_UP:
            logger.warning('[UG1] A Unidade deve estar completamente parada para realizar o fechamento da comporta!')

        elif self.dict['UG']['comporta_aberta_ug1'] == True and self.dict['UG']['comporta_cracking_ug1'] == False:
            while self.dict['UG']['progresso_ug1'] >= 0:
                self.dict['UG']['progresso_ug1'] -= 0.00001
            self.dict['UG']['comporta_fechada_ug1'] = True
            self.dict['UG']['comporta_aberta_ug1'] = False
            self.dict['UG']['comporta_cracking_ug1'] = False

        elif self.dict['UG']['comporta_cracking_ug1'] == True and self.dict['UG']['comporta_aberta_ug1'] == False:
            while self.dict['UG']['progresso_ug1'] >= 0:
                self.dict['UG']['progresso_ug1'] -= 0.00001
            self.dict['UG']['comporta_fechada_ug1'] = True
            self.dict['UG']['comporta_aberta_ug1'] = False
            self.dict['UG']['comporta_cracking_ug1'] = False
        
        else:
            logger.info('A comporta já está fechada.')
        return True

    def set_cracking_comporta_ug1(self):
        if self.dict['UG']['comporta_operando_ug2'] == True:
            logger.info('Não é possível realizar o cracking da comporta 1 pois a comporta 2 está em operação.')
        
        elif self.dict['UG']['limpa_grades_operando'] == True:
            logger.info('Não é possível realizar o cracking da comporta 1 pois o limpa grades se encontra em operação.')

        elif self.dict['UG']['comporta_fechada_ug1'] == True and self.dict['UG']['comporta_aberta_ug1'] == False:
            self.dict['UG']['comporta_operando_ug1'] = True
            while self.dict['UG']['progresso_ug1'] <= 20:
                self.dict['UG']['progresso_ug1'] += 0.00001
            self.dict['UG']['comporta_operando_ug1'] = False
            self.dict['UG']['comporta_fechada_ug1'] = False
            self.dict['UG']['comporta_aberta_ug1'] = False
            self.dict['UG']['comporta_cracking_ug1'] = True
            Thread(target=lambda: self.timer_equalizacao_cracking_ug1()).start()
        
        elif self.dict['UG']['comporta_aberta_ug1'] == True and self.dict['UG']['comporta_fechada_ug1'] == False:
            logger.info('A comporta já está aberta.')
        
        else:
            logger.info('A comporta já está na posição de cracking.')
        return True
    
    def set_abertura_comporta_ug2(self):
        if self.dict['UG']['comporta_operando_ug1'] == True:
            logger.info('Não é possível realizar a abertura da comporta 2 pois a comporta 1 está em operação.')
        
        elif self.dict['UG']['limpa_grades_operando'] == True:
            logger.info('Não é possível realizar a abertura da comporta 2 pois o limpa grades se encontra em operação.')
        
        elif self.dict['UG']['permissao_abrir_comporta_ug2'] == False:
            logger.info('As permissões de abertura da comporta 2 ainda não foram ativadas.')

        elif self.dict['UG']['comporta_cracking_ug2'] == True and self.dict['UG']['comporta_fechada_ug2'] == False:
            self.dict['UG']['comporta_operando_ug2'] = True
            while self.dict['UG']['progresso_ug2'] <= 100:
                self.dict['UG']['progresso_ug2'] += 0.00001
            self.dict['UG']['comporta_operando_ug2'] = False
            self.dict['UG']['comporta_fechada_ug2'] = False
            self.dict['UG']['comporta_aberta_ug2'] = True
            self.dict['UG']['comporta_cracking_ug2'] = False
            self.dict['UG']['equalizar_ug2'] = False
        
        elif self.dict['UG']['comporta_cracking_ug2'] == False and self.dict['UG']['comporta_fechada_ug2'] == True:
            logger.info('A comporta está fechada, execute a operação de cracking primeiro!')
        
        else:
            logger.info('A comporta já está aberta.')
        return True
    
    def set_fechamento_comporta_ug2(self):
        if self.dict['UG']['etapa_atual_ug2'] != ETAPA_UP:
            logger.warning('[UG2] A Unidade deve estar completamente parada para realizar o fechamento da comporta!')

        elif self.dict['UG']['comporta_aberta_ug2'] == True and self.dict['UG']['comporta_cracking_ug2'] == False:
            while self.dict['UG']['progresso_ug2'] >= 0:
                self.dict['UG']['progresso_ug2'] -= 0.00001
            self.dict['UG']['comporta_fechada_ug2'] = True
            self.dict['UG']['comporta_aberta_ug2'] = False
            self.dict['UG']['comporta_cracking_ug2'] = False
        
        elif self.dict['UG']['comporta_cracking_ug2'] == True and self.dict['UG']['comporta_aberta_ug2'] == False:
            while self.dict['UG']['progresso_ug2'] >= 0:
                self.dict['UG']['progresso_ug2'] -= 0.00001
            self.dict['UG']['comporta_fechada_ug2'] = True
            self.dict['UG']['comporta_aberta_ug2'] = False
            self.dict['UG']['comporta_cracking_ug2'] = False
        
        else:
            logger.info('A comporta já está fechada.')
        return True
    
    def set_cracking_comporta_ug2(self):
        if self.dict['UG']['comporta_operando_ug1'] == True:
            logger.info('Não é possível realizar o cracking da comporta 2 pois a comporta 1 está em operação.')
        
        elif self.dict['UG']['limpa_grades_operando'] == True:
            logger.info('Não é possível realizar o cracking da comporta 2 pois o limpa grades se encontra em operação.')

        elif self.dict['UG']['comporta_fechada_ug2'] == True and self.dict['UG']['comporta_aberta_ug2'] == False:
            self.dict['UG']['comporta_operando_ug2'] = True
            while self.dict['UG']['progresso_ug2'] <= 20:
                self.dict['UG']['progresso_ug2'] += 0.00001
            self.dict['UG']['comporta_operando_ug2'] = False
            self.dict['UG']['comporta_fechada_ug2'] = False
            self.dict['UG']['comporta_aberta_ug2'] = False
            self.dict['UG']['comporta_cracking_ug2'] = True
            Thread(target=lambda: self.timer_equalizacao_cracking_ug2()).start()
        
        elif self.dict['UG']['comporta_aberta_ug2'] == True and self.dict['UG']['comporta_fechada_ug2'] == False:
            logger.info('A comporta já está aberta.')
        
        else:
            logger.info('A comporta já está na posição de cracking.')
        return True

    def timer_equalizacao_cracking_ug1(self):
        delay = 20
        logger.debug('Aguardando equalização de pressão da UG.')
        tempo_equalizacao = time() + delay
        while time() <= tempo_equalizacao:
            if self.dict['UG']['equalizar_ug1'] == True:
                logger.info('A unidade foi equalizada, permissão para abrir comporta ativada!')
                self.dict['UG']['permissao_abrir_comporta_ug1'] = True
                return True

        logger.warning('Não foi possível equalizar a unidade! Fechando comporta e adicionando condicionador')
        self.dict['UG']['trip_ug1'] = True
        self.dict['UG']['condicao_falha_cracking_ug1'] = True
        self.dict['UG']['thread_comp_fechada_ug1'] = True
        return False
    
    def timer_equalizacao_cracking_ug2(self):
        delay = 20
        logger.debug('Aguardando equalização de pressão da UG.')
        tempo_equalizacao = time() + delay
        while time() <= tempo_equalizacao:
            if self.dict['UG']['equalizar_ug2'] == True:
                logger.info('A unidade foi equalizada, permissão para abrir comporta ativada!')
                self.dict['UG']['permissao_abrir_comporta_ug2'] = True
                return True

        logger.warning('Não foi possível equalizar a unidade! Fechando comporta e adicionando condicionador')
        self.dict['UG']['trip_ug2'] = True
        self.dict['UG']['condicao_falha_cracking_ug2'] = True
        self.dict['UG']['thread_comp_fechada_ug2'] = True
        return False
