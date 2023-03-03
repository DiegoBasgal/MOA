import numpy as np

from DICT import *

class Ug:
    def __init__(self, id, parent):
        self.id = id

        self.parent = parent
        self.logger = parent.logger
        self.segundos_por_passo = self.parent.segundos_por_passo
        self.shared_dict = parent.shared_dict
        self.escala_ruido = parent.escala_ruido

        self.tempo_na_transicao = 0
        self.avisou_trip = False
        self.etapa_alvo = 0
        self.etapa_atual = 0
        self.flags = 0
        self.potencia = 0
        self.setpoint = 0
        self.horimetro_hora = 100

        self.shared_dict[f"debug_parar_ug{self.id}"] = False
        self.shared_dict[f"debug_partir_ug{self.id}"] = False
        self.shared_dict[f"etapa_alvo_ug{self.id}"] = 0
        self.shared_dict[f"etapa_atual_ug{self.id}"] = 0
        self.shared_dict[f"etapa_aux_ug{self.id}"] = 5
        self.shared_dict[f"flags_ug{self.id}"] = 0
        self.shared_dict[f"potencia_kw_ug{self.id}"] = 0
        self.shared_dict[f"q_ug{self.id}"] = 0
        self.shared_dict[f"reconhece_reset_ug{self.id}"] = False
        self.shared_dict[f"setpoint_kw_ug{self.id}"] = 0
        self.shared_dict[f"debug_setpoint_kw_ug{self.id}"] = 0
        self.shared_dict[f"trip_ug{self.id}"] = False
        self.shared_dict[f"temperatura_ug{self.id}_fase_r"] = 25
        self.shared_dict[f"temperatura_ug{self.id}_fase_s"] = 25
        self.shared_dict[f"temperatura_ug{self.id}_fase_t"] = 25
        self.shared_dict[f"temperatura_ug{self.id}_nucleo_gerador_1"] = 25
        self.shared_dict[f"temperatura_ug{self.id}_nucleo_gerador_2"] = 25
        self.shared_dict[f"temperatura_ug{self.id}_nucleo_gerador_3"] = 25
        self.shared_dict[f"temperatura_ug{self.id}_mancal_casq_rad"] = 25
        self.shared_dict[f"temperatura_ug{self.id}_mancal_casq_comb"] = 25
        self.shared_dict[f"temperatura_ug{self.id}_mancal_escora_comb"] = 25
        self.shared_dict[f"pressao_caixa_espiral_ug{self.id}"] = 16.2
        
    def passo(self):
        self.setpoint = self.shared_dict[f"setpoint_kw_ug{self.id}"]

        if self.shared_dict[f"reconhece_reset_ug{self.id}"]:
            self.shared_dict[f"reconhece_reset_ug{self.id}"] = False
            self.reconhece_reset_ug()
            self.shared_dict[f"trip_ug{self.id}"] = False
            self.flags = 0

        if self.shared_dict[f"trip_ug{self.id}"]:
            self.tripar(1, "Trip Elétrico/CLP.")

        if self.shared_dict[f"debug_partir_ug{self.id}"]:
            self.shared_dict[f"debug_partir_ug{self.id}"] = False
            self.partir()

        if self.shared_dict[f"debug_parar_ug{self.id}"]:
            self.shared_dict[f"debug_parar_ug{self.id}"] = False
            self.parar()

        self.etapa_alvo = self.shared_dict[f"etapa_alvo_ug{self.id}"]

        if self.etapa_atual == ETAPA_UP:
            self.potencia = 0
            
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.shared_dict[f"etapa_alvo_ug{self.id}"] = self.etapa_alvo
                self.shared_dict[f"etapa_aux_ug{self.id}"] = UNIDADE_PARADA

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo
                self.shared_dict[f"etapa_aux_ug{self.id}"] = UNIDADE_SINCRONIZANDO

                if self.tempo_na_transicao >= TEMPO_TRANS_US_UPS:
                    self.etapa_atual = ETAPA_UPGM
                    self.tempo_na_transicao = 0

        # self.ETAPA UPGM
        if self.etapa_atual == ETAPA_UPGM:
            self.potencia = 0

            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.shared_dict[f"etapa_alvo_ug{self.id}"] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo
                self.shared_dict[f"etapa_aux_ug{self.id}"] = UNIDADE_SINCRONIZANDO

                if self.tempo_na_transicao >= TEMPO_TRANS_UPGM_UVD:
                    self.etapa_atual = ETAPA_UVD
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.shared_dict[f"etapa_aux_ug{self.id}"] = UNIDADE_PARANDO

                if self.tempo_na_transicao <= -TEMPO_TRANS_UPGM_UP:
                    self.etapa_atual = ETAPA_UP
                    self.tempo_na_transicao = 0
                    self.shared_dict[f"etapa_aux_ug{self.id}"] = UNIDADE_PARADA

        # Etapa VAZIO DESEXITADO
        if self.etapa_atual == ETAPA_UVD:
            self.potencia = 0

            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.shared_dict[f"etapa_alvo_ug{self.id}"] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo
                self.shared_dict[f"etapa_aux_ug{self.id}"] = UNIDADE_SINCRONIZANDO

                if self.tempo_na_transicao >= TEMPO_TRANS_UVD_UPS:
                    self.etapa_atual = ETAPA_UPS
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.shared_dict[f"etapa_aux_ug{self.id}"] = UNIDADE_PARANDO

                if self.tempo_na_transicao <= -TEMPO_TRANS_UVD_UPGM:
                    self.etapa_atual = ETAPA_UPGM
                    self.tempo_na_transicao = 0

        # Etapa PRONTA PARA SINCRONISMO
        if self.etapa_atual == ETAPA_UPS:
            self.potencia = 0

            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.shared_dict[f"etapa_alvo_ug{self.id}"] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo
                self.shared_dict[f"etapa_aux_ug{self.id}"] = UNIDADE_SINCRONIZANDO

                if (self.tempo_na_transicao >= TEMPO_TRANS_UPS_US and self.shared_dict["dj52L_fechado"]):
                    self.etapa_atual = ETAPA_US
                    self.tempo_na_transicao = 0
                    self.shared_dict[f"etapa_aux_ug{self.id}"] = UNIDADE_SINCRONIZADA

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.shared_dict[f"etapa_aux_ug{self.id}"] = UNIDADE_PARANDO

                if self.tempo_na_transicao <= -TEMPO_TRANS_UPS_UVD:
                    self.etapa_atual = ETAPA_UVD
                    self.tempo_na_transicao = 0

        # Etapa UNIDADE SINCRONIZADA
        if self.etapa_atual == ETAPA_US:
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.shared_dict[f"etapa_alvo_ug{self.id}"] = self.etapa_alvo

                if (self.shared_dict["dj52L_fechado"] and not self.shared_dict["dj52L_trip"]):
                    self.potencia = min(self.potencia, POT_MAX)
                    self.potencia = max(self.potencia, POT_MIN)
                    self.shared_dict[f"etapa_aux_ug{self.id}"] = UNIDADE_SINCRONIZADA

                    if self.setpoint > self.potencia:
                        self.potencia += 10.4167 * self.segundos_por_passo
                    else:
                        self.potencia -= 10.4167 * self.segundos_por_passo

                    self.potencia = np.random.normal(self.potencia, 1 * self.escala_ruido)

                if self.shared_dict["dj52L_aberto"] or self.shared_dict["dj52L_trip"]:
                    self.potencia = 0
                    self.etapa_atual = ETAPA_UVD
                    self.etapa_alvo = ETAPA_US
                    self.shared_dict[f"etapa_alvo_ug{self.id}"] = self.etapa_alvo
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.potencia -= 10.4167 * self.segundos_por_passo
                self.shared_dict[f"etapa_aux_ug{self.id}"] = UNIDADE_PARANDO

                if (self.tempo_na_transicao <= -TEMPO_TRANS_US_UPS and self.potencia <= 0):
                    self.potencia = 0
                    self.etapa_atual = ETAPA_UPS
                    self.tempo_na_transicao = 0

        self.shared_dict[f"temperatura_ug{self.id}_fase_r"] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict[f"temperatura_ug{self.id}_fase_s"] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict[f"temperatura_ug{self.id}_fase_t"] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict[f"temperatura_ug{self.id}_nucleo_gerador_1"] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict[f"temperatura_ug{self.id}_nucleo_gerador_2"] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict[f"temperatura_ug{self.id}_nucleo_gerador_3"] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict[f"temperatura_ug{self.id}_mancal_casq_rad"] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict[f"temperatura_ug{self.id}_mancal_casq_comb"] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict[f"temperatura_ug{self.id}_mancal_escora_comb"] = np.random.normal(25, 1 * self.escala_ruido)
       #self.shared_dict["pressao_caixa_espiral_ug{}"] = np.random.normal(20, 1 * self.escala_ruido)


        if self.etapa_atual > ETAPA_UP:
            self.horimetro_hora += self.segundos_por_passo / 3600

        if (self.etapa_atual > ETAPA_UP and self.shared_dict["nv_montante"] < USINA_NV_MINIMO_OPERACAO):
            # self.tripar(1, "Trip nível baixo.")
            # self.shared_dict["trip_ug{}"] = True
            self.potencia = 0
            self.etapa_atual = 1
            self.etapa_alvo = 1

        self.shared_dict[f"q_ug{self.id}"] = self.q_ug(self.potencia)
        self.shared_dict[f"potencia_kw_ug{self.id}"] = self.potencia
        self.shared_dict[f"etapa_atual_ug{self.id}"] = self.etapa_atual
        self.shared_dict[f"flags_ug{self.id}"] = self.flags

    def tripar(self, flag, desc=None):
        if not self.avisou_trip:
            self.avisou_trip = True
            self.logger.warning(f"[UG{self.id}] Trip!. {self.id}")
        self.potencia = 0
        self.etapa_atual = 1
        self.etapa_alvo = 1
        self.shared_dict[f"etapa_alvo_ug{self.id}"] = self.etapa_alvo
        self.flags = flag

    def reconhece_reset_ug(self):
        self.logger.info(f"[UG{self.id}] Reconhece Reset.")
        self.avisou_trip = False
        self.flags = 0

    def partir(self):
        self.logger.info(f"[UG{self.id}] partir(): etapa_alvo -> 4.")
        self.etapa_alvo = ETAPA_US
        self.shared_dict[f"etapa_alvo_ug{self.id}"] = self.etapa_alvo

    def parar(self):
        self.logger.info(f"[UG{self.id}] parar(): etapa_alvo -> 0.")
        self.etapa_alvo = ETAPA_UP
        self.shared_dict[f"etapa_alvo_ug{self.id}"] = self.etapa_alvo

    def q_ug(self, potencia_kW):
        if potencia_kW > 200:
            return 0.0106 * potencia_kW
        else:
            return 0
