import logging

from time import time, sleep
from threading import Thread
from abc import abstractmethod

from src.dicionarios.regs import *
from src.dicionarios.const import *
from src.unidade_geracao import UnidadeGeracao

logger = logging.getLogger("__main__")

class State:
    def __init__(self, parent_ug: UnidadeGeracao):
        self.parent_ug = parent_ug

    @abstractmethod
    def step(self) -> "State":
        pass

class StateManual(State):
    def __init__(self, parent_ug):
        super().__init__(parent_ug)

        self.parent_ug.codigo_state = MOA_UNIDADE_MANUAL

        self.parent_ug.borda_parar = False

        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado: \"Manual\". Para retornar a operação autônoma, favor agendar na interface web")

    def step(self) -> "State":
        self.parent_ug.setpoint = self.parent_ug.leitura_potencia.valor
        return self

class StateIndisponivel(State):
    def __init__(self, parent_ug):
        super().__init__(parent_ug)

        self.parent_ug.codigo_state = MOA_UNIDADE_INDISPONIVEL

        self.parent_ug.parar_timer = True
        self.parent_ug.borda_parar = True if self.parent_ug.borda_parar else False

        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado: \"Indisponível\". Para retornar a operação autônoma, favor agendar na interface web")

    def step(self) -> "State":
        self.parent_ug.bloquear_ug()
        logger.debug(f"[UG{self.parent_ug.id}] Unidade Indisponível")
        return self

class StateRestrito(State):
    def __init__(self, parent_ug):
        super().__init__(parent_ug)

        self.parent_ug.codigo_state = MOA_UNIDADE_RESTRITA

        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado: \"Restrito\"")

    def step(self) -> "State":
        self.parent_ug.bloquear_ug()
        self.parent_ug.controle_limites_operacao()
        flag = self.parent_ug.verificar_condicionadores()

        if flag == DEVE_INDISPONIBILIZAR:
            logger.warning(f"[UG{self.parent_ug.id}] UG detectou condicionadores com gravidade alta, indisponibilizando UG.")
            self.parar_timer = True
            return StateIndisponivel()

        elif flag == DEVE_IGNORAR:
            logger.info(f"[UG{self.parent_ug.id}] A UG não possui mais condicionadores ativos, normalizando e retornando para o estado disponível")
            self.parar_timer = True
            self.parent_ug.reconhece_reset_alarmes()
            return StateDisponivel()

        if self.parent_ug.norma_agendada:
            logger.info(f"[UG{self.parent_ug.id}] Normalização por tempo acionada -> Tempo definido: {self.parent_ug.tempo_normalizar}")
            self.parent_ug.norma_agendada = False
            Thread(terget=lambda: self.espera_normalizar(self.parent_ug.tempo_normalizar)).start()

        elif self.parar_timer:
            return self if self.parent_ug.normalizar_ug() else StateIndisponivel()

        else:
            logger.debug(f"[UG{self.parent_ug.id}] Aguardando normalização sem tempo pré-definido")
            return self

        return self

    def espera_normalizar(self, delay: int) -> None:
        while not self.parar_timer:
            sleep(max(0, time() + delay - time()))
            self.parar_timer = True
            return

class StateDisponivel(State):
    def __init__(self, parent_ug):
        super().__init__(parent_ug)

        self.parent_ug.codigo_state = MOA_UNIDADE_DISPONIVEL

        self.parent_ug.release = False
        self.parent_ug.borda_partindo = False
        self.parent_ug.tentativas_de_normalizacao = 0

        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado: \"Disponível\"")

    def step(self) -> "State":
        self.parent_ug.controle_limites_operacao()
        flag = self.parent_ug.verificar_condicionadores()

        if flag == DEVE_INDISPONIBILIZAR:
            logger.warning(f"[UG{self.parent_ug.id}] Indisponibilizando UG.")
            return StateIndisponivel(self.parent_ug)

        elif flag == DEVE_AGUARDAR:
            logger.warning(f"[UG{self.parent_ug.id}] Entrado no estado Restrito até a normalização do condicionador.")
            return StateRestrito(self.parent_ug)

        if flag == DEVE_NORMALIZAR:
            return self if self.parent_ug.normalizar_ug() else StateIndisponivel(self.parent_ug)

        else:
            logger.debug(f"[UG{self.parent_ug.id}] Etapa atual: \"{UNIDADE_DICT_ETAPAS[self.parent_ug.etapa_atual]}\"")

            if self.parent_ug.limpeza_grade:
                self.parent_ug.setpoint_minimo = self.parent_ug.cfg["pot_limpeza_grade"]
                self.parent_ug.setpoint = self.parent_ug.setpoint_minimo
            else:
                self.parent_ug.ajuste_ganho_cx_espiral()

            self.parent_ug.controle_etapas()

            return self
