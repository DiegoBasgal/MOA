import json
import logging
import os
import threading
import time
from cmath import sqrt
from datetime import datetime

from pyModbusTCP.server import DataBank

import field_connector

logger = logging.getLogger('__main__')

# carrega as configurações
config_file = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_file, 'r') as file:
    cfg = json.load(file)

fc = field_connector.FieldConnector(cfg)

###########################################
###########################################
###########################################
###########################################
###########################################


def threaded(fn):
    # Decorador para execução em thread separado
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


def curva_de_atenuacao(valor, alerta, limite):
    """ Curva de atenuação de valores conforme parametrização. Decaimento de quarta ordem"""
    ganho = 1
    if valor > alerta:
        ganho = max(min(sqrt(sqrt(1 - ((valor - alerta) / (limite - alerta)))).real, 1), 0)
    if valor > limite:
        ganho = 0
    return ganho


# COMANDOS MODBUS
UG_ESTADO_UP = 0
UG_ESTADO_UPGM = 1
UG_ESTADO_UVD = 2
UG_ESTADO_UPS = 3
UG_ESTADO_US = 4

# LEITURAS MODBUS
OPERACAO_ETAPA_ALVO_UP = 0
OPERACAO_ETAPA_ALVO_UPGM = 1
OPERACAO_ETAPA_ALVO_UMD = 2
OPERACAO_ETAPA_ALVO_UPS = 3
OPERACAO_ETAPA_ALVO_US = 4
OPERACAO_ETAPA_ATUAL_UP = 0
OPERACAO_ETAPA_ATUAL_UPGM = 1
OPERACAO_ETAPA_ATUAL_UMD = 2
OPERACAO_ETAPA_ATUAL_UPS = 3
OPERACAO_ETAPA_ATUAL_US = 4


class UnidadeDeGeracao:

    def __init__(self, id_ug, con, cfg):

        # Método de inicialização da UG. Ele roda quando a UG é criada, automaticamente.
        # Nesse caso ele é usado apenas para inicializar valores, mas poderia ter comportamentos mais complesxos.

        # - Valores internos
        self.bloqueada = False
        self.cfg = cfg
        self.con = con
        self.etapa_alvo = 0
        self.etapa_atual = 0
        self.flag_clp = 0
        self.id_da_ug = id_ug
        self.limite_tentativas_noramlizao = 3
        self.potencia_maxima = 0
        self.potencia_minima = 0
        self.tempo_base = 30
        self.tentativas_de_normalizar = 0
        self.ts_auxiliar = datetime.now()

        # - Sensores
        self.perda_na_grade = 0
        self.temperatura_enrolamento_fase_r = 0
        self.temperatura_enrolamento_fase_s = 0
        self.temperatura_enrolamento_fase_t = 0
        self.temperatura_mancal_la_casquilho = 0
        self.temperatura_mancal_la_contra_escora_1 = 0
        self.temperatura_mancal_la_contra_escora_2 = 0
        self.temperatura_mancal_la_escora_1 = 0
        self.temperatura_mancal_la_escora_2 = 0
        self.temperatura_mancal_lna_casquilho = 0

        # - Alertas
        self.alerta_perda_na_grade = 0
        self.alerta_temperatura_enrolamento_fase_r = 0
        self.alerta_temperatura_enrolamento_fase_s = 0
        self.alerta_temperatura_enrolamento_fase_t = 0
        self.alerta_temperatura_mancal_la_casquilho = 0
        self.alerta_temperatura_mancal_la_contra_escora_1 = 0
        self.alerta_temperatura_mancal_la_contra_escora_2 = 0
        self.alerta_temperatura_mancal_la_escora_1 = 0
        self.alerta_temperatura_mancal_la_escora_2 = 0
        self.alerta_temperatura_mancal_lna_casquilho = 0

        # - Limites
        self.limite_perda_na_grade = 0
        self.limite_temperatura_enrolamento_fase_r = 0
        self.limite_temperatura_enrolamento_fase_s = 0
        self.limite_temperatura_enrolamento_fase_t = 0
        self.limite_temperatura_mancal_la_casquilho = 0
        self.limite_temperatura_mancal_la_contra_escora_1 = 0
        self.limite_temperatura_mancal_la_contra_escora_2 = 0
        self.limite_temperatura_mancal_la_escora_1 = 0
        self.limite_temperatura_mancal_la_escora_2 = 0
        self.limite_temperatura_mancal_lna_casquilho = 0

    def normalizar(self):
        """ Normaliza a UG.

            Se a UG estiver bloqueada, não faça nada e Retornar False.
            Caso contrário:
                Se o ts_auxiliar não for recente: (se não acabou de indisponibilizar ou tentar normalizar):
                    Atualiza o ts_auxiliar
                    Remove emergência da UG via painel
                    Reconehce emergência via modbus
                    Retornar True
                Caso contrário:
                    Retornar False
        """

        if self.bloqueada:  # A UG está bloqueada, o moa não deve ordenar absolutamente nada.
            return False
        else:
            # Se o ts_auxiliar não for recente:
            agora = datetime.now()
            if (agora - self.ts_auxiliar).seconds < self.tempo_base:
                # Atualiza o ts_auxiliar para evitar problemas de temporização com os equipamentos
                self.ts_auxiliar = datetime.now()
                # Remove emergência da UG via painel
                if self.id_da_ug == 1:
                    DataBank.set_words(self.cfg['REG_MOA_OUT_BLOCK_UG1'], [0])
                if self.id_da_ug == 2:
                    DataBank.set_words(self.cfg['REG_MOA_OUT_BLOCK_UG2'], [0])
                # Reconehce emergência via modbus
                self.con.normalizar_emergencia()
                return True  # Tentou normalizar
            else:
                return False   # Não tentou normalizar

    @threaded  # ! Essa função é pode demorar bastante tempo e portanto é executada em um thread separado!
    def indisponibilizar(self):
        """ Atenção! Essa função é pode demorar bastante tempo e portanto é executada em um thread separado!

            Para a Unidade Geradora e então aciona a emergencia 86H via CLP e elétricamente via painel. 

            Atualiza o ts_auxiliar para evitar problemas de temporização com os equipamentos
            Enviar comando de parar UG
            Aguardar a UG parar <- PODE DEMORAR BASTANTE TEMPO !!!
            Aciona emergência da UG via modbus
            Aciona emergência da UG via painel
        """

        # Atualiza o ts_auxiliar para evitar problemas de temporização com os equipamentos
        self.ts_auxiliar = datetime.now()
        # Parar UG
        self.parar()

        # Aguardar a UG parar
        while not self.etapa_atual == OPERACAO_ETAPA_ATUAL_UP:
            time.sleep(1)

        # Aciona emergência da UG via modbus
        if self.id_da_ug == 1:
            self.con.acionar_emergencia_ug1()
        if self.id_da_ug == 2:
            self.con.acionar_emergencia_ug2()
        # Aciona emergência da UG via painel
        if self.id_da_ug == 1:
            DataBank.set_words(self.cfg['REG_MOA_OUT_BLOCK_UG1'], [1])
        if self.id_da_ug == 2:
            DataBank.set_words(self.cfg['REG_MOA_OUT_BLOCK_UG2'], [1])

    def bloquear(self):
        """ Para a Unidade Geradora e passa a ignora-lá até que seja desbloqueada via software. 

            Se a UG não estiver bloqueada: 
                Informar bloqueio
                Se a ug não estiver parada ou não estiver em processo de parada
                    Parar a UG 
            Retornar True
        """
        if not self.bloqueada:
            logger.info("[UG{}] Bloqueando UG.".format(self.id_da_ug))
            if (not self.etapa_alvo == OPERACAO_ETAPA_ALVO_UP or not self.etapa_atual == OPERACAO_ETAPA_ATUAL_UP):
                self.parar()
            self.bloqueada = True
        return True

    def desbloquear(self):
        """ Limpa o bloqueio via software. 

            Se a UG estiver bloqueada:
                Informar o desbloqueio
                Desbloquear a UG
            Returne True
        """
        if self.bloqueada:  # A UG está bloqueada, o moa não deve ordenar absolutamente nada.
            logger.info("[UG{}] Desbloqueando UG.".format(self.id_da_ug))
            self.bloqueada = False
        return True

    def partir(self):
        """ Envia os comandos necessários para partir a Unidade Geradora. 

            Se a UG estiver bloqueada, não faça nada e Retornar False.
            Caso contrário:
                Se a UG não estiver sincronizada e não estiver em processo de sincronização:
                    Informar a partida da UG
                    Partir a UG
                Retornar True
        """

        if self.bloqueada:  # A UG está bloqueada, o moa não deve ordenar absolutamente nada.
            return False
        else:
            # Se não está sincronizando e não está sincronizada:
            if (not self.etapa_alvo == OPERACAO_ETAPA_ALVO_US
                    or not self.etapa_atual == OPERACAO_ETAPA_ATUAL_US):
                logger.info("[UG{}] Partindo.".format(self.id_da_ug))
                if self.id_da_ug == 1:
                    self.con.partir_ug1()  # Comando via modbus UG_ESTADO_US <- 1
                if self.id_da_ug == 2:
                    self.con.partir_ug2()  # Comando via modbus UG_ESTADO_US <- 1
            return True

    def parar(self):
        """ Envia os comandos necessários para parar a Unidade Geradora.

            Se a UG estiver bloqueada, não faça nada e Retornar False.
            Caso contrário:
                Se a UG não estiver parada e não estiver em processo de parada:
                    Informar a parada da UG
                    Parar a UG
                Retornar True
        """
        if self.bloqueada:  # A UG está bloqueada, o moa não deve ordenar absolutamente nada.
            return False
        else:
            # Se não está parando e não está parada:
            if (not self.etapa_alvo == OPERACAO_ETAPA_ALVO_UP
                    or not self.etapa_atual == OPERACAO_ETAPA_ATUAL_UP):
                logger.info("[UG{}] Parando.".format(self.id_da_ug))
                if self.id_da_ug == 1:
                    self.con.parar_ug1()  # Comando via modbus UG_ESTADO_UP <- 1
                if self.id_da_ug == 2:
                    self.con.parar_ug2()  # Comando via modbus UG_ESTADO_UP <- 1
            return True

    def alterar_setpoint(self, setpoint):
        """ Envia os comandos necessários para alterar o setpoint da Unidade Geradora. 
            Desliga os modos de controle como o "controle conjunto"
            O Valor do setpoint deve ser escrito em kW
            O Valor passa por um tratamento antes de ser escrito para adequar a potência as condições da UG

            Se a UG estiver bloqueada, não faça nada e Retornar False
            Caso contrário:
                Calcular curvas de atenuação
                Limitar atenuação
                Calcular novo setpoint
                Se o novo setpoint for muito baixo e (a UG não estiver parada e não estiver parando):
                    Parar ug
                Enviar novo setpoint para a UG
                Returnar True
        """
        if self.bloqueada:  # A UG está bloqueada, o moa não deve ordenar absolutamente nada.
            return False
        else:

            # Curvas de atenuação
            lista_de_atenuadores = [1]  # Inicialização da lista com apenas o ganho unitário (1)

            # - temperatura_enrolamento_fase_r
            lista_de_atenuadores.append(curva_de_atenuacao(self.temperatura_enrolamento_fase_r,
                                                           self.alerta_temperatura_enrolamento_fase_r,
                                                           self.limite_temperatura_enrolamento_fase_r))

            # - temperatura_enrolamento_fase_s
            lista_de_atenuadores.append(curva_de_atenuacao(self.temperatura_enrolamento_fase_s,
                                                           self.alerta_temperatura_enrolamento_fase_s,
                                                           self.limite_temperatura_enrolamento_fase_s))

            # - temperatura_enrolamento_fase_t
            lista_de_atenuadores.append(curva_de_atenuacao(self.temperatura_enrolamento_fase_t,
                                                           self.alerta_temperatura_enrolamento_fase_t,
                                                           self.limite_temperatura_enrolamento_fase_t))

            # - temperatura_mancal_la_casquilho
            lista_de_atenuadores.append(curva_de_atenuacao(self.temperatura_mancal_la_casquilho,
                                                           self.alerta_temperatura_mancal_la_casquilho,
                                                           self.limite_temperatura_mancal_la_casquilho))

            # - temperatura_mancal_la_contra_escora_1
            lista_de_atenuadores.append(curva_de_atenuacao(self.temperatura_mancal_la_contra_escora_1,
                                                           self.alerta_temperatura_mancal_la_contra_escora_1,
                                                           self.limite_temperatura_mancal_la_contra_escora_1))

            # - temperatura_mancal_la_contra_escora_2
            lista_de_atenuadores.append(curva_de_atenuacao(self.temperatura_mancal_la_contra_escora_2,
                                                           self.alerta_temperatura_mancal_la_contra_escora_2,
                                                           self.limite_temperatura_mancal_la_contra_escora_2))

            # - temperatura_mancal_la_escora_1
            lista_de_atenuadores.append(curva_de_atenuacao(self.temperatura_mancal_la_escora_1,
                                                           self.alerta_temperatura_mancal_la_escora_1,
                                                           self.limite_temperatura_mancal_la_escora_1))

            # - temperatura_mancal_la_escora_2
            lista_de_atenuadores.append(curva_de_atenuacao(self.temperatura_mancal_la_escora_2,
                                                           self.alerta_temperatura_mancal_la_escora_2,
                                                           self.limite_temperatura_mancal_la_escora_2))

            # - temperatura_mancal_lna_casquilho
            lista_de_atenuadores.append(curva_de_atenuacao(self.temperatura_mancal_lna_casquilho,
                                                           self.alerta_temperatura_mancal_lna_casquilho,
                                                           self.limite_temperatura_mancal_lna_casquilho))

            # - perda_na_grade
            lista_de_atenuadores.append(curva_de_atenuacao(self.perda_na_grade,
                                                           self.perda_na_grade_alerta,
                                                           self.perda_na_grade_max))

            menor_ganho = min(lista_de_atenuadores)                             # Pega o menor ganho na lista
            ganho = max(0, min(menor_ganho, 1))                                 # Limita o ganho entre 0 e 1
            setpoint = int(setpoint * ganho)                                    # Aplica a atenuação no setpoint
            setpoint = min(setpoint,  self.potencia_maxima)                     # Limita o setpoint ao maximo da ug
            setpoint = 0 if setpoint < self.potencia_minima else setpoint       # Zera o setpoint se for < que a mínima

            if (setpoint < self.potencia_minima                                 # Se o setpoint ficou abaixo do mínimo:
                and (not self.estado_alvo == OPERACAO_ETAPA_ALVO_UP             # e a UG não está nem parada
                     or not self.estado_atual == OPERACAO_ETAPA_ATUAL_UP)):     # nem está parando
                logger.debug("[UG{}] Setpoint abaixo do mínima, parando.")      # Guardar no Log
                self.parar()                                                    # Parar a UG

            # Aqui ele deve ser "0" ou um valor entre o mínimo e o máximo da UG.
            # Guardar no Log
            logger.debug("[UG{}] Alterando setpoint para {:03d}"
                         " kW (ganho/atenuação: {:0.3f})"
                         .format(self.id_da_ug, setpoint, ganho))
            # Alterar de fato o setpoint.
            if self.id_da_ug == 1:
                self.con.set_ug1_setpoint(setpoint)  # Comando via modbus
            if self.id_da_ug == 2:
                self.con.set_ug2_setpoint(setpoint)  # Comando via modbus

            return True

    def atualizar_estado_interno(self):
        """ Atualiza o estado interno da Unidade Geradora, verifica flags, alarmes e limites. Tenta normalizar a UG

            Se estiver normalizada, reseta o contador de tentativas de normalização

            Se a UG estiver bloqueada, não faça nada e Retornar False

            Caso contrário:

                Verifica condições da UG, caso necessário, indizponibiliza a mesma.

                Se estiver com alguma flag

                    Se o ts_auxiliar não for recente: (se não acabou de indisponibilizar ou tentar normalizar):

                        Se o numero de tentativas de normalizar menor que o limite:
                        Informar a tentativa de noramlização da UG
                            Somar +1 ao contador de tentativas de normalização
                            Atualizar o ts_auxiliar para o instante atual
                            Tentar normalizar a UG

                        Caso contrário:
                            Informa o ocorrido
                            Bloqueia a UG

        """

        # Se estiver normalizada, reseta o contador de tentativas de normalização
        if not self.flag_clp and self.tentativas_de_normalizar >= 1:
            self.tentativas_de_normalizar = 0
            logger.info("[UG{}] A UG foi normalizada. (Tentativas de normalização zeradas).".format(self.id_da_ug))

        if self.bloqueada:  # A UG está bloqueada, o moa não deve ordenar absolutamente nada.
            return False
        else:
            # Verifica condições da UG, caso necessário, indizponibiliza a mesma.

            # - temperatura_enrolamento_fase_r
            if self.temperatura_enrolamento_fase_r > self.limite_temperatura_enrolamento_fase_r:
                logger.warning("[UG{}] temperatura_enrolamento_fase_r ({0.2f}) > limite  ({0.2f})."
                               .format(self.id_da_ug, self.temperatura_enrolamento_fase_r,
                                       self.limite_temperatura_enrolamento_fase_r))
                self.indisponibilizar()

            # - temperatura_enrolamento_fase_s
            if self.temperatura_enrolamento_fase_s > self.limite_temperatura_enrolamento_fase_s:
                logger.warning("[UG{}] temperatura_enrolamento_fase_s ({0.2f}) > limite  ({0.2f})."
                               .format(self.id_da_ug, self.temperatura_enrolamento_fase_s,
                                       self.limite_temperatura_enrolamento_fase_s))
                self.indisponibilizar()

            # - temperatura_enrolamento_fase_t
            if self.temperatura_enrolamento_fase_t > self.limite_temperatura_enrolamento_fase_t:
                logger.warning("[UG{}] temperatura_enrolamento_fase_t ({0.2f}) > limite  ({0.2f})."
                               .format(self.id_da_ug, self.temperatura_enrolamento_fase_t,
                                       self.limite_temperatura_enrolamento_fase_t))
                self.indisponibilizar()

            # - temperatura_mancal_la_casquilho
            if self.temperatura_mancal_la_casquilho > self.limite_temperatura_mancal_la_casquilho:
                logger.warning("[UG{}] temperatura_mancal_la_casquilho ({0.2f}) > limite  ({0.2f})."
                               .format(self.id_da_ug, self.temperatura_mancal_la_casquilho,
                                       self.limite_temperatura_mancal_la_casquilho))
                self.indisponibilizar()

            # - temperatura_mancal_la_contra_escora_1
            if self.temperatura_mancal_la_contra_escora_1 > self.limite_temperatura_mancal_la_contra_escora_1:
                logger.warning("[UG{}] temperatura_mancal_la_contra_escora_1 ({0.2f}) > limite  ({0.2f})."
                               .format(self.id_da_ug, self.temperatura_mancal_la_contra_escora_1,
                                       self.limite_temperatura_mancal_la_contra_escora_1))
                self.indisponibilizar()

            # - temperatura_mancal_la_contra_escora_2
            if self.temperatura_mancal_la_contra_escora_2 > self.limite_temperatura_mancal_la_contra_escora_2:
                logger.warning("[UG{}] temperatura_mancal_la_contra_escora_2 ({0.2f}) > limite  ({0.2f})."
                               .format(self.id_da_ug, self.temperatura_mancal_la_contra_escora_2,
                                       self.limite_temperatura_mancal_la_contra_escora_2))
                self.indisponibilizar()

            # - temperatura_mancal_la_escora_1
            if self.temperatura_mancal_la_escora_1 > self.limite_temperatura_mancal_la_escora_1:
                logger.warning("[UG{}] temperatura_mancal_la_escora_1 ({0.2f}) > limite  ({0.2f})."
                               .format(self.id_da_ug, self.temperatura_mancal_la_escora_1,
                                       self.limite_temperatura_mancal_la_escora_1))
                self.indisponibilizar()

            # - temperatura_mancal_la_escora_2
            if self.temperatura_mancal_la_escora_2 > self.limite_temperatura_mancal_la_escora_2:
                logger.warning("[UG{}] temperatura_mancal_la_escora_2 ({0.2f}) > limite  ({0.2f})."
                               .format(self.id_da_ug, self.temperatura_mancal_la_escora_2,
                                       self.limite_temperatura_mancal_la_escora_2))
                self.indisponibilizar()

            # - emperatura_mancal_lna_casquilho
            if self.temperatura_mancal_lna_casquilho > self.limite_temperatura_mancal_lna_casquilho:
                logger.warning("[UG{}] temperatura_mancal_lna_casquilho ({0.2f}) > limite  ({0.2f})."
                               .format(self.id_da_ug, self.temperatura_mancal_lna_casquilho,
                                       self.limite_temperatura_mancal_lna_casquilho))
                self.indisponibilizar()

            # - perda_na_grade
            if self.perda_na_grade > self.limite_perda_na_grade:
                logger.warning("[UG{}] perda_na_grade ({0.2f}) > limite  ({0.2f})."
                               .format(self.id_da_ug, self.perda_na_grade, self.limite_perda_na_grade))
                self.indisponibilizar()

            # Se estiver com alguma flag
            if self.flag_clp:

                agora = datetime.now()
                if self.ts_auxiliar > agora:
                    # Se a última atualização estiver no futuro, algo está errado.
                    logger.debug("[UG{}] ts_auxiliar > agora!".format(self.id_da_ug))
                    raise ValueError("[UG{}] ts_auxiliar > agora!".format(self.id_da_ug))

                # Se o ts_auxiliar não for recente: (se não acabou de indisponibilizar ou tentar normalizar):
                if (agora - self.ts_auxiliar).seconds < (self.tempo_base * self.tentativas_de_normalizar):
                    # Se o numero de tentativas de normalizar menor que o limite:
                    if self.tentativas_de_normalizar < self.limite_tentativas_noramlizao:
                        # Informar a tentativa de noramlização da UG
                        logger.info("[UG{}] Tentativa de normalização {}/{}."
                                    .format(self.id_da_ug, self.tentativas_de_normalizar + 1,
                                            self.limite_tentativas_noramlizao))
                        # Somar +1 ao contador de tentativas de normalização
                        self.tentativas_de_normalizar += 1
                        # Atualizar o ts_auxiliar para o instante atual
                        self.ts_auxiliar = datetime.now()
                        # Tentar normalizar a UG
                        self.normalizar()

                    # Caso contrário (passou do limite):
                    else:
                        logger.info("[UG{}] Tentativas de normalização excedidas, bloqueando a UG.".format(self.id_da_ug))
                        # Bloqueia a UG
                        self.bloqueada = True
