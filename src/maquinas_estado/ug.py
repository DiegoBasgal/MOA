import logging

from threading import Thread

from src.dicionarios.const import *
from src.unidade_geracao import UnidadeDeGeracao

logger = logging.getLogger("__main__")

class State:
    def __init__(self, parent: UnidadeDeGeracao=None):
        # VERIFICAÇÃO DE ARGUENTOS
        if not parent:
            logger.error("[UG-SM] Houve um erro ao importar a classe Unidade de Geração")
            raise ImportError
        else:
            self.parent = parent

    def step(self) -> object:
        pass

class StateManual(State):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent.codigo_state = UG_SM_MANUAL
        logger.info(f"[UG{self.parent.id}] Entrando no estado: \"Manual\". Para retornar a operação autônoma, favor agendar na interface web")

        self.parent.borda_parar = False

    def step(self) -> State:
        self.parent.setpoint = self.parent.leitura_potencia
        return self

class StateIndisponivel(State):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent.codigo_state = UG_SM_INDISPONIVEL
        logger.info(f"[UG{self.parent.id}] Entrando no estado: \"Indisponível\". Para retornar a operação autônoma, favor agendar na interface web")

        self.parent.borda_parar = True if self.parent.borda_parar else False

    def step(self) -> State:
        self.parent.bloquear_unidade()
        logger.debug(f"[UG{self.parent.id}] Unidade Indisponível.")
        return self

class StateRestrito(State):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent.codigo_state = UG_SM_RESTRITA
        logger.info(f"[UG{self.parent.id}] Entrando no estado \"restrito\"")

        self.parent.parar_timer = False
        self.parent.borda_parar = True if self.parent.borda_parar else False

    def step(self) -> State:
        self.parent.bloquear_unidade()
        self.parent.oco_ug.controle_limites_operacao(self.parent)
        flag = self.parent.oco_ug.verificar_condicionadores(self.parent)

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
        logger.info(f"[UG{self.parent.id}] Entrando no estado: \"Disponível\"")

        self.parent.tentativas_de_normalizacao = 0

        self.parent.borda_parar = False

    def step(self) -> State:
        self.parent.oco_ug.controle_limites_operacao(self.parent)
        flag = self.parent.oco_ug.verificar_condicionadores(self.parent)

        if flag == CONDIC_INDISPONIBILIZAR:
            logger.warning(f"[UG{self.parent.id}] Indisponibilizando UG.")
            return StateIndisponivel(self.parent)

        elif flag == CONDIC_AGUARDAR:
            logger.warning(f"[UG{self.parent.id}] Entrando no estado Restrito até normalização da condição.")
            return StateRestrito(self.parent)

        elif flag == CONDIC_NORMALIZAR:
            return self if self.parent.normalizar_unidade() else StateIndisponivel(self.parent)

        else:
            logger.debug(f"[UG{self.parent.id}] Etapa atual: \"{self.parent.etapa_atual}\" / Etapa alvo: \"{self.parent.etapa_alvo}\"")

            if self.parent.limpeza_grade:
                self.parent.setpoint = self.parent.setpoint_minimo = self.parent.cfg["pot_limpeza_grade"]

            self.parent.controle_etapas()

            return self