import logging

import src.unidade_geracao as u

from threading import Thread

from src.dicionarios.const import *


logger = logging.getLogger("logger")


class State:
    def __init__(self, parent: "u.UnidadeDeGeracao"=None):

        # VERIFICAÇÃO DE ARGUENTOS
        if not parent:
            logger.error("[UG-SM] Houve um erro ao importar a classe Unidade de Geração")
            raise ImportError
        else:
            self.parent = parent

    def step(self) -> "object":
        pass


class StateManual(State):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent.codigo_state = UG_SM_MANUAL
        self.parent.borda_parar = False

        logger.debug("")
        logger.info(f"[UG{self.parent.id}] Entrando no estado:                 \"Manual\". Para retornar a operação autônoma, favor agendar na interface web")
        logger.debug(f"[UG{self.parent.id}] Tentativas de normalização:         {self.parent.tentativas_de_normalizacao}/{self.parent.limite_tentativas_de_normalizacao}")
        logger.debug("")


    def step(self) -> "State":
        self.parent.setpoint = self.parent.potencia
        return self


class StateIndisponivel(State):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent.codigo_state = UG_SM_INDISPONIVEL

        self.parent.borda_parar = True if self.parent.borda_parar else False

        logger.debug("")
        logger.info(f"[UG{self.parent.id}] Entrando no estado:                 \"Indisponível\". Para retornar a operação autônoma, favor agendar na interface web")
        logger.debug(f"[UG{self.parent.id}] Tentativas de normalização:         {self.parent.tentativas_de_normalizacao}/{self.parent.limite_tentativas_de_normalizacao}")
        logger.debug("")


    def step(self) -> "State":
        self.parent.bloquear_unidade()
        return self


class StateRestrito(State):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent.codigo_state = UG_SM_RESTRITA

        self.parent.parar_timer = False
        self.parent.borda_parar = True if self.parent.borda_parar else False

        logger.debug("")
        logger.info(f"[UG{self.parent.id}] Entrando no estado                  \"Restrito\"")
        logger.debug(f"[UG{self.parent.id}] Tentativas de normalização:         {self.parent.tentativas_de_normalizacao}/{self.parent.limite_tentativas_de_normalizacao}")
        logger.debug("")


    def step(self) -> "State":
        self.parent.bloquear_unidade()
        self.parent.controlar_limites_operacao()
        flag = self.parent.verificar_condicionadores()

        if flag == CONDIC_INDISPONIBILIZAR:
            logger.warning(f"[UG{self.parent.id}] UG detectou condicionadores com gravidade alta, indisponibilizando UG.")
            self.parent.parar_timer = True
            return StateIndisponivel(self.parent)

        elif flag == CONDIC_IGNORAR:
            logger.info(f"[UG{self.parent.id}] A UG não possui mais condicionadores ativos, normalizando e retornando para o estado disponível")
            self.parent.parar_timer = True
            self.parent.reconhece_reset_alarmes()
            return StateDisponivel(self.parent)

        if self.parent.normalizacao_agendada:
            logger.info(f"[UG{self.parent.id}] Normalização por tempo acionada -> Tempo definido: {self.parent.tempo_normalizar}")
            self.parent.normalizacao_agendada = False
            Thread(target=lambda: self.parent.espera_normalizar(self.parent.tempo_normalizar)).start()

        elif self.parent.parar_timer:
            return self if self.parent.normalizar_unidade() else StateIndisponivel(self.parent)

        else:
            logger.debug(f"[UG{self.parent.id}] Aguardando normalização sem tempo pré-definido")
            return self


class StateDisponivel(State):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent.codigo_state = UG_SM_DISPONIVEL
        logger.debug("")
        logger.info(f"[UG{self.parent.id}] Entrando no estado:                 \"Disponível\"")
        self.parent.tentativas_de_normalizacao = 0
        logger.debug(f"[UG{self.parent.id}] Tentativas de normalização:         {self.parent.tentativas_de_normalizacao}/{self.parent.limite_tentativas_de_normalizacao}")
        logger.debug("")

        self.parent.borda_parar = False

    def step(self) -> State:
        self.parent.oco.controlar_limites_operacao()
        flag = self.parent.oco.verificar_condicionadores()

        if flag == CONDIC_INDISPONIBILIZAR:
            logger.warning(f"[UG{self.parent.id}] Indisponibilizando UG.")
            return StateIndisponivel(self.parent)

        elif flag == CONDIC_AGUARDAR:
            logger.warning(f"[UG{self.parent.id}] Entrando no estado Restrito até normalização da condição.")
            return StateRestrito(self.parent)

        elif flag == CONDIC_NORMALIZAR:
            return self if self.parent.normalizar_unidade() else StateIndisponivel(self.parent)

        else:
            self.parent.controle_etapas()

            return self