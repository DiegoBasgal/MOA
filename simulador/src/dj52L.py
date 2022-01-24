class Dj52L:

    def __init__(self, parent):

        # COPIA DE INFORMACOES DA CLASSE SITE
        self.parent = parent
        self.logger = self.parent.logger
        self.shared_dict = parent.shared_dict
        self.segundos_por_passo = self.parent.segundos_por_passo
        self.USINA_TENSAO_MINIMA = self.parent.USINA_TENSAO_MINIMA
        self.USINA_TENSAO_MAXIMA = self.parent.USINA_TENSAO_MAXIMA
        self.shared_dict["debug_dj52L_abrir"] = False
        self.shared_dict["debug_dj52L_fechar"] = False
        self.shared_dict["debug_dj52L_reconhece_reset"] = False
        self.shared_dict["dj52L_aberto"] = True
        self.shared_dict["dj52L_fechado"] = False
        self.shared_dict["dj52L_inconsistente"] = False
        self.shared_dict["dj52L_trip"] = False
        self.shared_dict["dj52L_mola_carregada"] = True
        self.shared_dict["dj52L_falta_vcc"] = False
        self.shared_dict["dj52L_condicao_de_fechamento"] = True

        self.avisou_trip = False
        self.aux_mola = 0
        self.tempo_carregamento_mola = 2

    def passo(self):
        
        if self.shared_dict["debug_dj52L_fechar"] and self.shared_dict["debug_dj52L_abrir"]:
            self.shared_dict["debug_dj52L_abrir"] = False
            self.shared_dict["debug_dj52L_fechar"] = False
            self.shared_dict["dj52L_aberto"] = True
            self.shared_dict["dj52L_fechado"] = True
            self.tripar()
        elif self.shared_dict["debug_dj52L_fechar"]:
            self.shared_dict["debug_dj52L_fechar"] = False
            self.fechar()        
        elif self.shared_dict["debug_dj52L_abrir"]:
            self.shared_dict["debug_dj52L_abrir"] = False
            self.abrir()
        if self.shared_dict["debug_dj52L_reconhece_reset"]:
            self.reconhece_reset_dj52L()
            self.shared_dict["debug_dj52L_reconhece_reset"] = False


        if not self.shared_dict["dj52L_mola_carregada"]:
            self.aux_mola += self.segundos_por_passo
            if self.aux_mola >= self.tempo_carregamento_mola:
                self.aux_mola = 0
                self.shared_dict["dj52L_mola_carregada"] = True

        if not (self.USINA_TENSAO_MINIMA < self.shared_dict["tensao_na_linha"] < self.USINA_TENSAO_MAXIMA):
            self.tripar("Tensão fora dos limites")
        
        if self.shared_dict["dj52L_aberto"] == self.shared_dict["dj52L_fechado"]:
            self.shared_dict["dj52L_inconsistente"] = True

        self.shared_dict["dj52L_condicao_de_fechamento"] = True
        if not self.shared_dict["dj52L_aberto"]: self.shared_dict["dj52L_condicao_de_fechamento"] = False
        if not self.shared_dict["dj52L_mola_carregada"]: self.shared_dict["dj52L_condicao_de_fechamento"] = False
        if self.shared_dict["dj52L_fechado"]: self.shared_dict["dj52L_condicao_de_fechamento"] = False
        if self.shared_dict["dj52L_trip"]: self.shared_dict["dj52L_condicao_de_fechamento"] = False
        if self.shared_dict["dj52L_inconsistente"]: self.shared_dict["dj52L_condicao_de_fechamento"] = False
        if self.shared_dict["dj52L_falta_vcc"]: self.shared_dict["dj52L_condicao_de_fechamento"] = False

    def tripar(self, desc=None):
        if not self.avisou_trip:
            self.avisou_trip = True
            self.shared_dict["dj52L_trip"] = True
            self.shared_dict["dj52L_aberto"] = True
            self.shared_dict["dj52L_fechado"] = False
            self.shared_dict["dj52L_mola_carregada"] = False
            self.logger.warning("[dj52L] Trip!. {}".format(desc))
            return True

    def reconhece_reset_dj52L(self):
        self.logger.info("[dj52L] Reconhece Reset.")
        self.shared_dict["debug_dj52L_abrir"] = False
        self.shared_dict["debug_dj52L_fechar"] = False
        self.shared_dict["debug_dj52L_reconhece_reset"] = False
        self.shared_dict["dj52L_aberto"] = True
        self.shared_dict["dj52L_fechado"] = False
        self.shared_dict["dj52L_inconsistente"] = False
        self.shared_dict["dj52L_trip"] = False
        self.avisou_trip = False
        return True

    def abrir(self):
        self.logger.info("[dj52L] Abrir.")
        if self.shared_dict["dj52L_mola_carregada"]:
            self.shared_dict["dj52L_aberto"] = True
            self.shared_dict["dj52L_fechado"] = False
        else:
            self.tripar("Mandou antes de carregar a mola")
            return False
        self.shared_dict["dj52L_mola_carregada"] = False
        return True
    
    def fechar(self):
        if self.shared_dict["dj52L_trip"]:
            self.logger.warning("[dj52L] Picou!")
            return False
        else:
            self.logger.info("[dj52L] Fechar.")
            if self.shared_dict["dj52L_condicao_de_fechamento"]:
                self.shared_dict["dj52L_aberto"] = False
                self.shared_dict["dj52L_fechado"] = True
            else:
                self.tripar("Mandou antes de ter a condição de fechamento")
                return False
        self.shared_dict["dj52L_mola_carregada"] = False
        return True
  
    