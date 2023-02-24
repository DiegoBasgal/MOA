    def controle_limites_operacao(self) -> None:

        
        if fase_r[0] >= fase_r[1]:
            self.logger.warning(f"[UG{self.id}] A temperatura de Fase R da UG passou do valor base! ({fase_r[1]}C) | Leitura: {fase_r[0].valor}C")
        if fase_r[0] >= 0.9*(fase_r[2] - fase_r[1]) + fase_r[1]:
            self.logger.critical(f"[UG{self.id}] A temperatura de Fase R da UG está muito próxima do limite! ({fase_r[2]}C) | Leitura: {fase_r[0].valor}C")
        
        if fase_s[0] >= fase_s[1]:
            self.logger.warning(f"[UG{self.id}] A temperatura de Fase S da UG passou do valor base! ({fase_s[1]}C) | Leitura: {fase_s[0].valor}C")
        if fase_s[0] >= 0.9*(fase_s[2] - fase_s[1]) + fase_s[1]:
            self.logger.critical(f"[UG{self.id}] A temperatura de Fase S da UG está muito próxima do limite! ({fase_s[2]}C) | Leitura: {fase_s[0].valor}C")
        
        if fase_t[0] >= fase_t[1]:
            self.logger.warning(f"[UG{self.id}] A temperatura de Fase T da UG passou do valor base! ({fase_t[1]}C) | Leitura: {fase_t[0].valor}C")
        if fase_t[0] >= 0.9*(fase_t[2] - fase_t[1]) + fase_t[1]:
            self.logger.critical(f"[UG{self.id}] A temperatura de Fase T da UG está muito próxima do limite! ({fase_t[2]}C) | Leitura: {fase_t[0].valor}C")
        
        if nucleo_1[0] >= nucleo_1[1]:
            self.logger.warning(f"[UG{self.id}] A temperatura do Núcleo Gerador 1 da UG passou do valor base! ({nucleo_1[1]}C) | Leitura: {nucleo_1[0].valor}C")
        if nucleo_1[0] >= 0.9*(nucleo_1[2] - nucleo_1[1]) + nucleo_1[1]:
            self.logger.critical(f"[UG{self.id}] A temperatura do Núcleo Gerador 1 da UG está muito próxima do limite! ({nucleo_1[2]}C) | Leitura: {nucleo_1[0].valor}C")
        
        if nucleo_2[0] >= nucleo_2[1]:
            self.logger.warning(f"[UG{self.id}] A temperatura do Núcleo Gerador 2 da UG passou do valor base! ({nucleo_2[1]}C) | Leitura: {nucleo_2[0].valor}C")
        if nucleo_2[0] >= 0.9*(nucleo_2[2] - nucleo_2[1]) + nucleo_2[1]:
            self.logger.critical(f"[UG{self.id}] A temperatura do Núcleo Gerador 2 da UG está muito próxima do limite! ({nucleo_2[2]}C) | Leitura: {nucleo_2[0].valor}C")
        
        if nucleo_3[0] >= nucleo_3[1]:
            self.logger.warning(f"[UG{self.id}] A temperatura do Núcleo Gerador 3 da UG passou do valor base! ({nucleo_3[1]}C) | Leitura: {nucleo_3[0].valor}C")
        if nucleo_3[0] >= 0.9*(nucleo_3[2] - nucleo_3[1]) + nucleo_3[1]:
            self.logger.critical(f"[UG{self.id}] A temperatura do Núcleo Gerador 3 da UG está muito próxima do limite! ({nucleo_3[2]}C) | Leitura: {nucleo_3[0].valor}C")
        
        if mancal_CR[0] >= mancal_CR[1]:
            self.logger.warning(f"[UG{self.id}] A temperatura do Mancal Casquilho Radial da UG passou do valor base! ({mancal_CR[1]}C) | Leitura: {mancal_CR[0].valor}C")
        if mancal_CR[0] >= 0.9*(mancal_CR[2] - mancal_CR[1]) + mancal_CR[1]:
            self.logger.critical(f"[UG{self.id}] A temperatura do Mancal Casquilho Radial da UG está muito próxima do limite! ({mancal_CR[2]}C) | Leitura: {mancal_CR[0].valor}C")
        
        if mancal_CC[0] >= mancal_CC[1]:
            self.logger.warning(f"[UG{self.id}] A temperatura do Mancal Casquilho Combinado da UG passou do valor base! ({mancal_CC[1]}C) | Leitura: {mancal_CC[0].valor}C")
        if mancal_CC[0] >= 0.9*(mancal_CC[2] - mancal_CC[1]) + mancal_CC[1]:
            self.logger.critical(f"[UG{self.id}] A temperatura do Mancal Casquilho Combinado da UG está muito próxima do limite! ({mancal_CC[2]}C) | Leitura: {mancal_CC[0].valor}C")
        
        if mancal_EC[0] >= mancal_EC[1]:
            self.logger.warning(f"[UG{self.id}] A temperatura do Mancal Escora Combinado da UG passou do valor base! ({mancal_EC[1]}C) | Leitura: {mancal_EC[0].valor}C")
        if mancal_EC[0] >= 0.9*(mancal_EC[2] - mancal_EC[1]) + mancal_EC[1]:
            self.logger.critical(f"[UG{self.id}] A temperatura do Mancal Escora Combinado da UG está muito próxima do limite! ({mancal_EC[2]}C) | Leitura: {mancal_EC[0].valor}C")
        
        if caixa_espiral[0] <= caixa_espiral[1] and caixa_espiral[0] != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            self.logger.warning(f"[UG{self.id}] A pressão Caixa Espiral da UG passou do valor base! ({caixa_espiral[1]:03.2f} KGf/m2) | Leitura: {caixa_espiral[0].valor:03.2f}")
        if caixa_espiral[0] <= caixa_espiral[2]+0.9*(caixa_espiral[1] - caixa_espiral[2]) and caixa_espiral[0] != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            self.logger.critical(f"[UG{self.id}] A pressão Caixa Espiral da UG está muito próxima do limite! ({caixa_espiral[2]:03.2f} KGf/m2) | Leitura: {caixa_espiral[0].valor:03.2f} KGf/m2")