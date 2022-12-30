import numpy as np
from threading import Thread
from time import sleep, time


class Ug:
    def __init__(self, id, parent):
        self.id = id

        # COPIA DE INFORMACOES DA CLASSE SITE
        self.parent = parent
        self.USINA_NV_MINIMO_OPERACAO = self.parent.USINA_NV_MINIMO_OPERACAO
        self.logger = parent.logger
        self.segundos_por_passo = self.parent.segundos_por_passo
        self.shared_dict = parent.shared_dict
        self.escala_ruido = parent.escala_ruido

        self.tempo_na_transicao = 0
        self.avisou_trip = False
        self.etapa_alvo = 1
        self.etapa_atual = 1
        self.flags = 0
        self.potencia = 0
        self.setpoint = 0
        self.horimetro_hora = 0

        self.POT_MAX = 3037.5
        self.POT_MIN = 0.3 * self.POT_MAX

        self.ETAPA_UP = 1
        self.ETAPA_UPGM = 2
        self.ETAPA_UVD = 3
        self.ETAPA_UPS = 4
        self.ETAPA_US = 5

        self.UNIDADE_SINCRONIZADA = 1
        self.UNIDADE_PARANDO = 2
        self.UNIDADE_PARADA = 5
        self.UNIDADE_SINCRONIZANDO = 9

        self.TEMPO_TRANS_UP_UPGM = 20
        self.TEMPO_TRANS_UPGM_UVD = 20
        self.TEMPO_TRANS_UVD_UPS = 20
        self.TEMPO_TRANS_UPS_US = 20

        self.TEMPO_TRANS_US_UPS = 20
        self.TEMPO_TRANS_UPS_UVD = 20
        self.TEMPO_TRANS_UVD_UPGM = 20
        self.TEMPO_TRANS_UPGM_UP = 20

        self.TEMPO_ABERTURA_COMPORTA = 193
        self.TEMPO_FECHAMENTO_COMPORTA = 1
        self.TEMPO_CRACKING_COMPORTA = 106

        self.shared_dict["debug_parar_ug{}".format(self.id)] = False
        self.shared_dict["debug_partir_ug{}".format(self.id)] = False
        self.shared_dict["comporta_aberta_ug{}".format(self.id)] = False
        self.shared_dict["comporta_fechada_ug{}".format(self.id)] = True
        self.shared_dict["comporta_cracking_ug{}".format(self.id)] = False
        self.shared_dict["comporta_operando_ug{}".format(self.id)] = False
        self.shared_dict["equalizar_ug{}".format(self.id)] = None
        self.shared_dict["condicao_falha_cracking_ug{}".format(self.id)] = False
        self.shared_dict["permissao_abrir_comporta_ug{}".format(self.id)] = False
        self.shared_dict["limpa_grades_operando"] = False
        self.shared_dict["thread_comp_aberta_ug1"] = False
        self.shared_dict["thread_comp_fechada_ug1"] = False
        self.shared_dict["thread_comp_cracking_ug1"] = False
        self.shared_dict["thread_comp_aberta_ug2"] = False
        self.shared_dict["thread_comp_fechada_ug2"] = False
        self.shared_dict["thread_comp_cracking_ug2"] = False

        self.shared_dict["progresso_ug1"] = 0
        self.shared_dict["progresso_ug2"] = 0
        self.shared_dict["etapa_alvo_ug{}".format(self.id)] = 0
        self.shared_dict["etapa_atual_ug{}".format(self.id)] = 0
        self.shared_dict["etapa_aux_ug{}".format(self.id)] = 5
        self.shared_dict["flags_ug{}".format(self.id)] = 0
        self.shared_dict["potencia_kw_ug{}".format(self.id)] = 0
        self.shared_dict["q_ug{}".format(self.id)] = 0
        self.shared_dict["reconhece_reset_ug{}".format(self.id)] = False
        self.shared_dict["setpoint_kw_ug{}".format(self.id)] = 0
        self.shared_dict["debug_setpoint_kw_ug{}".format(self.id)] = 0
        self.shared_dict["trip_ug{}".format(self.id)] = False
        self.shared_dict["temperatura_ug{}_fase_r".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_fase_s".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_fase_t".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_nucleo_gerador_1".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_mancal_guia".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_mancal_guia_interno_1".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_mancal_guia_interno_2".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_patins_mancal_comb_1".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_patins_mancal_comb_2".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_mancal_casq_comb".format(self.id)] = 25
        self.shared_dict["temperatura_ug{}_mancal_contra_esc_comb".format(self.id)] = 25
        self.shared_dict["pressao_turbina_ug{}".format(self.id)] = 16.2
        
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
                self.shared_dict["etapa_aux_ug{}".format(self.id)] = self.UNIDADE_PARADA

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo
                self.shared_dict["etapa_aux_ug{}".format(self.id)] = self.UNIDADE_SINCRONIZANDO

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
                self.shared_dict["etapa_aux_ug{}".format(self.id)] = self.UNIDADE_SINCRONIZANDO

                if self.tempo_na_transicao >= self.TEMPO_TRANS_UPGM_UVD:
                    self.etapa_atual = self.ETAPA_UVD
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.shared_dict["etapa_aux_ug{}".format(self.id)] = self.UNIDADE_PARANDO

                if self.tempo_na_transicao <= -self.TEMPO_TRANS_UPGM_UP:
                    self.etapa_atual = self.ETAPA_UP
                    self.tempo_na_transicao = 0
                    self.shared_dict["etapa_aux_ug{}".format(self.id)] = self.UNIDADE_PARADA

        # self.ETAPA UVD
        if self.etapa_atual == self.ETAPA_UVD:
            self.potencia = 0

            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.shared_dict["etapa_alvo_ug{}".format(self.id)] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo
                self.shared_dict["etapa_aux_ug{}".format(self.id)] = self.UNIDADE_SINCRONIZANDO

                if self.tempo_na_transicao >= self.TEMPO_TRANS_UVD_UPS:
                    self.etapa_atual = self.ETAPA_UPS
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.shared_dict["etapa_aux_ug{}".format(self.id)] = self.UNIDADE_PARANDO

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
                self.shared_dict["etapa_aux_ug{}".format(self.id)] = self.UNIDADE_SINCRONIZANDO

                if (self.tempo_na_transicao >= self.TEMPO_TRANS_UPS_US and self.shared_dict["dj52L_fechado"]):
                    self.etapa_atual = self.ETAPA_US
                    self.tempo_na_transicao = 0
                    self.shared_dict["etapa_aux_ug{}".format(self.id)] = self.UNIDADE_SINCRONIZADA

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.shared_dict["etapa_aux_ug{}".format(self.id)] = self.UNIDADE_PARANDO

                if self.tempo_na_transicao <= -self.TEMPO_TRANS_UPS_UVD:
                    self.etapa_atual = self.ETAPA_UVD
                    self.tempo_na_transicao = 0

        # self.ETAPA US
        if self.etapa_atual == self.ETAPA_US:
            if (self.etapa_alvo is None) or (self.etapa_alvo == self.etapa_atual):
                self.tempo_na_transicao = 0
                self.etapa_alvo = None
                self.shared_dict["etapa_alvo_ug{}".format(self.id)] = self.etapa_alvo

                if (self.shared_dict["dj52L_fechado"] and not self.shared_dict["dj52L_trip"]):
                    self.potencia = min(self.potencia, self.POT_MAX)
                    self.potencia = max(self.potencia, self.POT_MIN)
                    self.shared_dict["etapa_aux_ug{}".format(self.id)] = self.UNIDADE_SINCRONIZADA

                    if self.setpoint > self.potencia:
                        self.potencia += 10.4167 * self.segundos_por_passo

                    else:
                        self.potencia -= 10.4167 * self.segundos_por_passo

                    self.potencia = np.random.normal(self.potencia, 1 * self.escala_ruido)

                if self.shared_dict["dj52L_aberto"] or self.shared_dict["dj52L_trip"]:
                    self.potencia = 0
                    self.etapa_atual = self.ETAPA_UVD
                    self.etapa_alvo = self.ETAPA_US
                    self.shared_dict["etapa_alvo_ug{}".format(self.id)] = self.etapa_alvo
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.potencia -= 10.4167 * self.segundos_por_passo
                self.shared_dict["etapa_aux_ug{}".format(self.id)] = self.UNIDADE_PARANDO

                if (self.tempo_na_transicao <= -self.TEMPO_TRANS_US_UPS and self.potencia <= 0):
                    self.potencia = 0
                    self.etapa_atual = self.ETAPA_UPS
                    self.tempo_na_transicao = 0

        # FIM COMPORTAMENTO self.ETAPAS

        self.shared_dict["temperatura_ug{}_fase_r".format(self.id)] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_fase_s".format(self.id)] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_fase_t".format(self.id)] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_nucleo_gerador_1".format(self.id)] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_mancal_guia".format(self.id)] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_mancal_guia_interno_1".format(self.id)] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_mancal_guia_interno_2".format(self.id)] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_patins_mancal_comb_1".format(self.id)] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_patins_mancal_comb_2".format(self.id)] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_mancal_casq_comb".format(self.id)] = np.random.normal(25, 1 * self.escala_ruido)
        self.shared_dict["temperatura_ug{}_mancal_contra_esc_comb".format(self.id)] = np.random.normal(25, 1 * self.escala_ruido)
       #self.shared_dict["pressao_turbina_ug{}".format(self.id)] = np.random.normal(20, 1 * self.escala_ruido)


        if self.etapa_atual > self.ETAPA_UP:
            self.horimetro_hora += self.segundos_por_passo / 3600

        if (self.etapa_atual > self.ETAPA_UP and self.shared_dict["nv_montante"] < self.USINA_NV_MINIMO_OPERACAO):
            # self.tripar(1, "Trip nível baixo.")
            # self.shared_dict["trip_ug{}".format(self.id)] = True
            self.potencia = 0
            self.etapa_atual = 1
            self.etapa_alvo = 1

        self.shared_dict["q_ug{}".format(self.id)] = self.q_ug(self.potencia)
        self.shared_dict["potencia_kw_ug{}".format(self.id)] = self.potencia
        self.shared_dict["etapa_atual_ug{}".format(self.id)] = self.etapa_atual
        self.shared_dict["flags_ug{}".format(self.id)] = self.flags
    
        if self.shared_dict["thread_comp_aberta_ug1"] == True:
            Thread(target=lambda: self.set_abertura_comporta_ug1()).start()
            self.shared_dict["thread_comp_aberta_ug1"] = False
    
        if self.shared_dict["thread_comp_fechada_ug1"] == True:
            Thread(target=lambda: self.set_fechamento_comporta_ug1()).start()
            self.shared_dict["thread_comp_fechada_ug1"] = False
    
        if self.shared_dict["thread_comp_cracking_ug1"] == True:
            Thread(target=lambda: self.set_cracking_comporta_ug1()).start()
            self.shared_dict["thread_comp_cracking_ug1"] = False
        
        if self.shared_dict["thread_comp_aberta_ug2"] == True:
            Thread(target=lambda: self.set_abertura_comporta_ug2()).start()
            self.shared_dict["thread_comp_aberta_ug2"] = False
    
        if self.shared_dict["thread_comp_fechada_ug2"] == True:
            Thread(target=lambda: self.set_fechamento_comporta_ug2()).start()
            self.shared_dict["thread_comp_fechada_ug2"] = False
    
        if self.shared_dict["thread_comp_cracking_ug2"] == True:
            Thread(target=lambda: self.set_cracking_comporta_ug2()).start()
            self.shared_dict["thread_comp_cracking_ug2"] = False

    def set_abertura_comporta_ug1(self):
        if self.shared_dict["comporta_operando_ug2"] == True:
            self.logger.info("Não é possível realizar a abertura da comporta 1 pois a comporta 2 está em operação.")

        elif self.shared_dict["limpa_grades_operando"] == True:
            self.logger.info("Não é possível realizar a abertura da comporta 1 pois o limpa grades se encontra em operação.")

        elif self.shared_dict["permissao_abrir_comporta_ug1"] == False:
            self.logger.info("As permissões de abertura da ug ainda não foram ativadas. Favor aguardar a equalização.")

        elif self.shared_dict["comporta_cracking_ug1"] == True and self.shared_dict["comporta_fechada_ug1"] == False:
            self.shared_dict["comporta_operando_ug1"] = True
            while self.shared_dict["progresso_ug1"] <= 100:
                self.shared_dict["progresso_ug1"] += 0.000001
            self.shared_dict["comporta_operando_ug1"] = False
            self.shared_dict["comporta_fechada_ug1"] = False
            self.shared_dict["comporta_aberta_ug1"] = True
            self.shared_dict["comporta_cracking_ug1"] = False
            self.shared_dict["equalizar_ug1"] = False

        elif self.shared_dict["comporta_cracking_ug1"] == False and self.shared_dict["comporta_fechada_ug1"] == True:
            self.logger.info("A comporta está fechada, execute a operação de cracking primeiro!")
        
        else:
            self.logger.info("A comporta já está aberta.")
        return True
    
    def set_fechamento_comporta_ug1(self):
        if self.shared_dict["comporta_aberta_ug1"] == True and self.shared_dict["comporta_cracking_ug1"] == False:
            while self.shared_dict["progresso_ug1"] >= 0:
                self.shared_dict["progresso_ug1"] -= 0.000001
            self.shared_dict["comporta_fechada_ug1"] = True
            self.shared_dict["comporta_aberta_ug1"] = False
            self.shared_dict["comporta_cracking_ug1"] = False

        elif self.shared_dict["comporta_cracking_ug1"] == True and self.shared_dict["comporta_aberta_ug1"] == False:
            while self.shared_dict["progresso_ug1"] >= 0:
                self.shared_dict["progresso_ug1"] -= 0.000001
            self.shared_dict["comporta_fechada_ug1"] = True
            self.shared_dict["comporta_aberta_ug1"] = False
            self.shared_dict["comporta_cracking_ug1"] = False
        
        else:
            self.logger.info("A comporta já está fechada.")
        return True

    def set_cracking_comporta_ug1(self):
        if self.shared_dict["comporta_operando_ug2"] == True:
            self.logger.info("Não é possível realizar o cracking da comporta 1 pois a comporta 2 está em operação.")
        
        elif self.shared_dict["limpa_grades_operando"] == True:
            self.logger.info("Não é possível realizar o cracking da comporta 1 pois o limpa grades se encontra em operação.")

        elif self.shared_dict["comporta_fechada_ug1"] == True and self.shared_dict["comporta_aberta_ug1"] == False:
            self.shared_dict["comporta_operando_ug1"] = True
            while self.shared_dict["progresso_ug1"] <= 30:
                self.shared_dict["progresso_ug1"] += 0.000001
            self.shared_dict["comporta_operando_ug1"] = False
            self.shared_dict["comporta_fechada_ug1"] = False
            self.shared_dict["comporta_aberta_ug1"] = False
            self.shared_dict["comporta_cracking_ug1"] = True
            Thread(target=lambda: self.timer_equalizacao_cracking()).start()
        
        elif self.shared_dict["comporta_aberta_ug1"] == True and self.shared_dict["comporta_fechada_ug1"] == False:
            self.logger.info("A comporta já está aberta.")
        
        else:
            self.logger.info("A comporta já está na posição de cracking.")
        return True
    
    def set_abertura_comporta_ug2(self):
        if self.shared_dict["comporta_operando_ug1"] == True:
            self.logger.info("Não é possível realizar a abertura da comporta 2 pois a comporta 1 está em operação.")
        
        elif self.shared_dict["limpa_grades_operando"] == True:
            self.logger.info("Não é possível realizar a abertura da comporta 2 pois o limpa grades se encontra em operação.")
        
        elif self.shared_dict["permissao_abrir_comporta_ug2"] == False:
            self.logger.info("As permissões de abertura da ug ainda não foram ativadas. Favor aguardar a equalização.")

        elif self.shared_dict["comporta_cracking_ug2"] == True and self.shared_dict["comporta_fechada_ug2"] == False:
            self.shared_dict["comporta_operando_ug2"] = True
            while self.shared_dict["progresso_ug2"] <= 100:
                self.shared_dict["progresso_ug2"] += 0.000001
            self.shared_dict["comporta_operando_ug2"] = False
            self.shared_dict["comporta_fechada_ug2"] = False
            self.shared_dict["comporta_aberta_ug2"] = True
            self.shared_dict["comporta_cracking_ug2"] = False
            self.shared_dict["equalizar_ug2"] = False
        
        elif self.shared_dict["comporta_cracking_ug2"] == False and self.shared_dict["comporta_fechada_ug2"] == True:
            self.logger.info("A comporta está fechada, execute a operação de cracking primeiro!")
        
        else:
            self.logger.info("A comporta já está aberta.")
        return True
    
    def set_fechamento_comporta_ug2(self):
        if self.shared_dict["comporta_aberta_ug2"] == True and self.shared_dict["comporta_cracking_ug2"] == False:
            while self.shared_dict["progresso_ug2"] >= 0:
                self.shared_dict["progresso_ug2"] -= 0.000001
            self.shared_dict["comporta_fechada_ug2"] = True
            self.shared_dict["comporta_aberta_ug2"] = False
            self.shared_dict["comporta_cracking_ug2"] = False
        
        elif self.shared_dict["comporta_cracking_ug2"] == True and self.shared_dict["comporta_aberta_ug2"] == False:
            while self.shared_dict["progresso_ug2"] >= 0:
                self.shared_dict["progresso_ug2"] -= 0.000001
            self.shared_dict["comporta_fechada_ug2"] = True
            self.shared_dict["comporta_aberta_ug2"] = False
            self.shared_dict["comporta_cracking_ug2"] = False
        
        else:
            self.logger.info("A comporta já está fechada.")
        return True
    
    def set_cracking_comporta_ug2(self):
        if self.shared_dict["comporta_operando_ug1"] == True:
            self.logger.info("Não é possível realizar o cracking da comporta 2 pois a comporta 1 está em operação.")
        
        elif self.shared_dict["limpa_grades_operando"] == True:
            self.logger.info("Não é possível realizar o cracking da comporta 2 pois o limpa grades se encontra em operação.")

        elif self.shared_dict["comporta_fechada_ug2"] == True and self.shared_dict["comporta_aberta_ug2"] == False:
            self.shared_dict["comporta_operando_ug2"] = True
            while self.shared_dict["progresso_ug2"] <= 30:
                self.shared_dict["progresso_ug2"] += 0.000001
            self.shared_dict["comporta_operando_ug2"] = False
            self.shared_dict["comporta_fechada_ug2"] = False
            self.shared_dict["comporta_aberta_ug2"] = False
            self.shared_dict["comporta_cracking_ug2"] = True
            Thread(target=lambda: self.timer_equalizacao_cracking()).start()
        
        elif self.shared_dict["comporta_aberta_ug2"] == True and self.shared_dict["comporta_fechada_ug2"] == False:
            self.logger.info("A comporta já está aberta.")
        
        else:
            self.logger.info("A comporta já está na posição de cracking.")
        return True

    def timer_equalizacao_cracking(self):
        delay = 120
        tempo_agora = time()
        tempo_equalizacao = time() + delay
        self.logger.debug("Equalizando UG pós cracking.")
        while tempo_agora < tempo_equalizacao:
            if self.shared_dict["equalizar_ug{}".format(self.id)] == True:
                self.logger.info("A unidade foi equalizada, permissão para abrir comporta ativada!")
                self.shared_dict["permissao_abrir_comporta_ug{}".format(self.id)] = True
                return True

            elif self.shared_dict["equalizar_ug{}".format(self.id)] == False:
                self.logger.warning("Não foi possível equalizar a unidade! Fechando comporta e adicionando condicionador")
                self.shared_dict["condicao_falha_cracking_ug{}".format(self.id)] = True
                self.shared_dict["thread_comp_fechada_ug{}".format(self.id)] = True
                return False

    def tripar(self, flag, desc=None):
        if not self.avisou_trip:
            self.avisou_trip = True
            self.logger.warning("[UG{}] Trip!. {}".format(self.id, desc))
        self.potencia = 0
        self.etapa_atual = 1
        self.etapa_alvo = 1
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
        if potencia_kW > 911:
            return 0.005610675 * potencia_kW
        else:
            return 0
