import numpy as np 



class Ug:

    def __init__(self, id, parent):
        self.id = id

        # COPIA DE INFORMACOES DA CLASSE SITE
        self.parent = parent
        self.USINA_NV_MINIMO_OPERACAO = self.parent.USINA_NV_MINIMO_OPERACAO
        self.logger = parent.logger
        self.segundos_por_passo = self.parent.segundos_por_passo
        self.shared_dict = parent.shared_dict
        self.escala_ruido=  parent.escala_ruido
        
        self.shared_dict["debug_parar_ug{}".format(self.id)] = False
        self.shared_dict["debug_partir_ug{}".format(self.id)] = False
        self.shared_dict["etapa_alvo_ug{}".format(self.id)] = 0
        self.shared_dict["etapa_atual_ug{}".format(self.id)] = 0
        self.shared_dict["flags_ug{}".format(self.id)] = 0
        self.shared_dict["potencia_kw_ug{}".format(self.id)] = 0
        self.shared_dict["q_ug{}".format(self.id)] = 0
        self.shared_dict["reconhece_reset_ug{}".format(self.id)] = False
        self.shared_dict["setpoint_kw_ug{}".format(self.id)] = 0
        self.shared_dict["debug_setpoint_kw_ug{}".format(self.id)] = 0
        self.shared_dict["trip_ug{}".format(self.id)] = False
        self.shared_dict["temperatura_ug{}_contra_escora_1".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_contra_escora_2".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_escora_1".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_escora_2".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_fase_r".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_fase_s".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_fase_t".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_la_casquilho".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_lna_casquilho".format(self.id)] = 25

        self.tempo_na_transicao = 0
        self.avisou_trip = False
        self.etapa_alvo = 0
        self.etapa_atual = 0
        self.flags = 0
        self.potencia = 0
        self.setpoint = 0
        self.horimetro = 0
        self.ETAPA_UP = 0
        self.ETAPA_UPGM = 1
        self.ETAPA_UVD = 2
        self.ETAPA_UPS = 3
        self.ETAPA_US = 4

        self.TEMPO_TRANS_UP_UPGM = 20
        self.TEMPO_TRANS_UPGM_UVD = 20
        self.TEMPO_TRANS_UVD_UPS = 20
        self.TEMPO_TRANS_UPS_US = 20

        self.TEMPO_TRANS_US_UPS = 20
        self.TEMPO_TRANS_UPS_UVD = 20
        self.TEMPO_TRANS_UVD_UPGM = 20
        self.TEMPO_TRANS_UPGM_UP = 20

    def passo(self):
        # DEBUG VIA GUI
        self.setpoint = self.shared_dict["setpoint_kw_ug{}".format(self.id)]
        if self.shared_dict["reconhece_reset_ug{}".format(self.id)]:
            self.shared_dict["reconhece_reset_ug{}".format(self.id)] = False
            self.reconhece_reset_ug()
            self.shared_dict["trip_ug{}".format(self.id)] = False
            self.flags = 0
        if self.shared_dict["trip_ug{}".format(self.id)]:
            self.tripar(1, "Trip Elétrico/CLP.")
        if self.shared_dict["debug_partir_ug{}".format(self.id)]:
            self.shared_dict["debug_partir_ug{}".format(self.id)] = False
            self.partir()
        if self.shared_dict["debug_parar_ug{}".format(self.id)]:
            self.shared_dict["debug_parar_ug{}".format(self.id)] = False
            self.parar()
        # FIM DEBUG VIA GUI

        # COMPORTAMENTO self.ETAPAS
        self.etapa_alvo = self.shared_dict["etapa_alvo_ug{}".format(self.id)]

        # self.ETAPA UP
        if self.etapa_atual == self.ETAPA_UP:
            self.potencia = 0
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.shared_dict["etapa_alvo_ug{}".format(self.id)] = self.etapa_alvo
            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo
                if self.tempo_na_transicao >= self.TEMPO_TRANS_US_UPS:
                    self.etapa_atual = self.ETAPA_UPGM
                    self.tempo_na_transicao = 0
              
        # self.ETAPA UPGM
        if self.etapa_atual == self.ETAPA_UPGM:
            self.potencia = 0
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.shared_dict["etapa_alvo_ug{}".format(self.id)] = self.etapa_alvo
            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo
                if self.tempo_na_transicao >= self.TEMPO_TRANS_UPGM_UVD:
                    self.etapa_atual = self.ETAPA_UVD
                    self.tempo_na_transicao = 0
            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                if self.tempo_na_transicao <= -self.TEMPO_TRANS_UPGM_UP:
                    self.etapa_atual = self.ETAPA_UP
                    self.tempo_na_transicao = 0        
        
        # self.ETAPA UVD
        if self.etapa_atual == self.ETAPA_UVD:
            self.potencia = 0
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.shared_dict["etapa_alvo_ug{}".format(self.id)] = self.etapa_alvo
            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo
                if self.tempo_na_transicao >= self.TEMPO_TRANS_UVD_UPS:
                    self.etapa_atual = self.ETAPA_UPS
                    self.tempo_na_transicao = 0
            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                if self.tempo_na_transicao <= -self.TEMPO_TRANS_UVD_UPGM:
                    self.etapa_atual = self.ETAPA_UPGM
                    self.tempo_na_transicao = 0          
        
        # self.ETAPA UPS
        if self.etapa_atual == self.ETAPA_UPS:
            self.potencia = 0
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.shared_dict["etapa_alvo_ug{}".format(self.id)] = self.etapa_alvo
            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo
                if self.tempo_na_transicao >= self.TEMPO_TRANS_UPS_US and self.shared_dict["dj52L_fechado"]:
                    self.etapa_atual = self.ETAPA_US
                    self.tempo_na_transicao = 0
            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                if self.tempo_na_transicao <= -self.TEMPO_TRANS_UPS_UVD:
                    self.etapa_atual = self.ETAPA_UVD
                    self.tempo_na_transicao = 0         

        # self.ETAPA US     
        if self.etapa_atual == self.ETAPA_US:
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.shared_dict["etapa_alvo_ug{}".format(self.id)] = self.etapa_alvo
                if self.shared_dict["dj52L_fechado"] and not self.shared_dict["dj52L_trip"]:
                    self.potencia = min(self.potencia, 2600)
                    if self.setpoint[0] > self.potencia:
                        self.potencia += 10.4167 * self.segundos_por_passo
                    else:
                        self.potencia -= 10.4167 * self.segundos_por_passo
                    self.potencia = np.random.normal(self.potencia , 1 * self.escala_ruido)
                if self.shared_dict["dj52L_aberto"] or self.shared_dict["dj52L_trip"]:
                    self.potencia = 0
                    self.etapa_atual = self.ETAPA_UVD
                    self.etapa_alvo = self.ETAPA_US
                    self.shared_dict["etapa_alvo_ug{}".format(self.id)] = self.etapa_alvo
                    self.tempo_na_transicao = 0
            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.potencia -= 10.4167 * self.segundos_por_passo
                if self.tempo_na_transicao <= -self.TEMPO_TRANS_US_UPS and self.potencia <= 0:
                    self.potencia = 0
                    self.etapa_atual = self.ETAPA_UPS
                    self.tempo_na_transicao = 0   
        # FIM COMPORTAMENTO self.ETAPAS


        self.shared_dict["temperatura_ug{}_contra_escora_1".format(self.id)] = np.random.normal(25 , 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_contra_escora_2".format(self.id)] = np.random.normal(25 , 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_escora_1".format(self.id)] = np.random.normal(25 , 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_escora_2".format(self.id)] = np.random.normal(25 , 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_fase_r".format(self.id)] = np.random.normal(25 , 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_fase_s".format(self.id)] = np.random.normal(25 , 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_fase_t".format(self.id)] = np.random.normal(25 , 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_la_casquilho".format(self.id)] = np.random.normal(25 , 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_lna_casquilho".format(self.id)] = np.random.normal(25 ,1 * self.escala_ruido)

        if self.etapa_atual > self.ETAPA_UP:
            self.horimetro += self.segundos_por_passo/3600

        if self.etapa_atual > self.ETAPA_UP and self.shared_dict["nv_montante"] < self.USINA_NV_MINIMO_OPERACAO:
            self.tripar(1, "Trip nível baixo.")
            self.shared_dict["trip_ug{}".format(self.id)] = True

        self.shared_dict["q_ug{}".format(self.id)] = self.q_ug(self.potencia)
        self.shared_dict["potencia_kw_ug{}".format(self.id)] = self.potencia
        self.shared_dict["etapa_atual_ug{}".format(self.id)] = self.etapa_atual
        self.shared_dict["flags_ug{}".format(self.id)] = self.flags

    def tripar(self, flag, desc=None):
        if not self.avisou_trip:
            self.avisou_trip = True
            self.logger.warning("[UG{}] Trip!. {}".format(self.id, desc))
        self.potencia = 0
        self.etapa_atual = 0
        self.etapa_alvo = None
        self.shared_dict["etapa_alvo_ug{}".format(self.id)] = self.etapa_alvo
        self.flags = flag

    def reconhece_reset_ug(self):
        self.logger.info("[UG{}] Reconhece Reset.".format(self.id))
        self.avisou_trip = False
        self.flags = 0

    def partir(self):
        self.logger.info("[UG{}] partir(): etapa_alvo -> 4.".format(self.id))
        self.etapa_alvo = self.ETAPA_US
        self.shared_dict["etapa_alvo_ug{}".format(self.id)] = self.etapa_alvo

    def parar(self):
        self.logger.info("[UG{}] parar(): etapa_alvo -> 0.".format(self.id))
        self.etapa_alvo = self.ETAPA_UP
        self.shared_dict["etapa_alvo_ug{}".format(self.id)] = self.etapa_alvo

    def q_ug(self, potencia_kW):
        if potencia_kW > 1:
            return 2.51 * (potencia_kW / 1000) + 1.59
        else:
            return 0
