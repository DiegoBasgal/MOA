from datetime import datetime
import os
import json
import field_connector
import logging

logger = logging.getLogger('__main__')

# carrega as configurações
config_file = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_file, 'r') as file:
    cfg = json.load(file)
    
fc = field_connector.FieldConnector(cfg)

UG_ESTADO_UP = 0
UG_ESTADO_UPGM = 1
UG_ESTADO_UVD = 2
UG_ESTADO_UPS = 3
UG_ESTADO_US = 4

class UnidadeDeGeracao:

    def __init__(self, id_ug, con):
        
        # Vars de inicialização
        self.id_da_ug = id_ug
        self.con = con
        self.ts_tentativa_normalizar = datetime.now()
        self.tentativas_de_normalizar = 0

        # Vars internas da UG
        self.indisponivel = False
        self.bloqueada = False
        self.estado_atual = 0

        # Perda na grade, alertas e limites
        self.perda_na_grade = 0
        self.perda_alerta_na_grade = 0
        self.perda_limite_na_grade = 0

        # Temperaturas, alertas e limites
        self.temperatura_enrolamento_fase_r = 0
        self.temperatura_enrolamento_fase_s = 0
        self.temperatura_enrolamento_fase_t = 0
        self.temperatura_mancal_la_casquilho = 0
        self.temperatura_mancal_la_contra_escora_1 = 0
        self.temperatura_mancal_la_contra_escora_2 = 0
        self.temperatura_mancal_la_escora_1 = 0
        self.temperatura_mancal_la_escora_2 = 0
        self.temperatura_mancal_lna_casquilho = 0
        self.temperatura_alerta_enrolamento_fase_r = 0
        self.temperatura_alerta_enrolamento_fase_s = 0
        self.temperatura_alerta_enrolamento_fase_t = 0
        self.temperatura_alerta_mancal_la_casquilho = 0
        self.temperatura_alerta_mancal_la_contra_escora_1 = 0
        self.temperatura_alerta_mancal_la_contra_escora_2 = 0
        self.temperatura_alerta_mancal_la_escora_1 = 0
        self.temperatura_alerta_mancal_la_escora_2 = 0
        self.temperatura_alerta_mancal_lna_casquilho = 0  
        self.temperatura_limite_enrolamento_fase_r = 0
        self.temperatura_limite_enrolamento_fase_s = 0
        self.temperatura_limite_enrolamento_fase_t = 0
        self.temperatura_limite_mancal_la_casquilho = 0
        self.temperatura_limite_mancal_la_contra_escora_1 = 0
        self.temperatura_limite_mancal_la_contra_escora_2 = 0
        self.temperatura_limite_mancal_la_escora_1 = 0
        self.temperatura_limite_mancal_la_escora_2 = 0
        self.temperatura_limite_mancal_lna_casquilho = 0

    def reconhece_reset_alermes(self):
        """ Reconehce e reseta os alarmes da usina. """
        raise NotImplementedError
    
    def indisponibilizar(self):
        """ Para a Unidade Geradora e então aciona a emergencia 86H via CLP e elétricamente via painel. """
        raise NotImplementedError

    def bloquear(self):
        """ Para a Unidade Geradora e passa a ignora-lá até que seja desbloqueada via software. """
        # Se a UG estiver bloqueada, não faça nada e retorne True
        if self.bloqueada:
            return True
        else:
            # Bloqueia a UG
            logger.info("Bloqueando UG{}".format(self.id_da_ug))
            # Para a UG antes de bloquear a mesma
            self.parar()
            self.bloqueada = True
            # Retorna True ao bloquear com sucesso
            return True
        
    def desbloquear(self):
        """ Limpa o bloqueio via software. """
        # Se a UG não estiver bloqueada, não faça nada e retorne True
        if not self.bloqueada:
            return True
        else:
            # Desloqueia a UG
            logger.info("Desbloqueando UG{}".format(self.id_da_ug))
            self.bloqueada = False
            # Retorna True ao desbloquear com sucesso
            return True

    def partir(self):
        """ Envia os comandos necessários para partir a Unidade Geradora. """
        # Se a UG estiver bloqueada, não faça nada e retorne False
        if self.bloqueada:
            return False
        else:
            logger.info("Partindo UG{}".format(self.id_da_ug))
            # Escreve etapa alvo
            self.con = field_connector.FieldConnector(cfg)
            if self.id_da_ug == 1: self.con.partir_ug1()

            
    def parar(self):
        """ Envia os comandos necessários para parar a Unidade Geradora. """
        raise NotImplementedError

    def alterar_setpoint(self):
        """ Envia os comandos necessários para alterar o setpoint da Unidade Geradora. """
        raise NotImplementedError

    def atualizar_estado_interno(self):
        """ Atualiza o estado interno da Unidade Geradora, verifica flags, alarmes e limites. """
        raise NotImplementedError
