__version__ = "0.2"
__authors__ = "Diego Basgal", " Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da máquina de estados das Unidades de Geração."

from threading import Thread
from abc import abstractmethod

from usina import *
from unidade_geracao import UnidadeGeracao

logger = logging.getLogger("__main__")

class State:
    def __init__(self, parent: UnidadeGeracao | None = ...) -> ...:
        if not parent:
            raise ValueError("[UG-SM] Não foi possível carregar a instânica da Unidade de Geração.")
        else:
            self.parent = parent

        self.cfg = parent.cfg

    @abstractmethod
    def step(self) -> "State":
        pass

class StateManual(State):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.codigo_state = UG_SM_MANUAL

        self.borda_parar = False

        logger.info(f"[UG{self.parent.id}] Entrando no estado: \"Manual\". Para retornar a operação autônoma, favor agendar na interface web")

    def step(self) -> State:
        self.parent.setpoint = self.parent.leitura_potencia
        return self

class StateIndisponivel(State):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.codigo_state = UG_SM_INDISPONIVEL

        self.borda_parar = True if self.borda_parar else False

        logger.info(f"[UG{self.parent.id}] Entrando no estado: \"Indisponível\". Para retornar a operação autônoma, favor agendar na interface web")

    def step(self) -> State:
        self.bloquear_ug()
        logger.debug(f"[UG{self.parent.id}] Unidade Indisponível.")

        return self

class StateRestrito(State):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.codigo_state = UG_SM_RESTRITA

        self.parar_timer: bool = False
        self.borda_parar = True if self.borda_parar else False

        logger.info(f"[UG{self.parent.id}] Entrando no estado restrito.")

    def step(self) -> State:
        self.bloquear_ug()
        self.parent.controle_limites_operacao()
        flag = self.parent.verificar_condicionadores()

        if flag == CONDIC_INDISPONIBILIZAR:
            logger.warning(f"[UG{self.parent.id}] UG detectou condicionadores com gravidade alta, indisponibilizando UG.")
            self.parar_timer = True
            return StateIndisponivel()

        elif flag == CONDIC_IGNORAR:
            logger.info(f"[UG{self.parent.id}] A UG não possui mais condicionadores ativos, normalizando e retornando para o estado disponível")
            self.parar_timer = True
            self.parent.reconhece_reset_alarmes()
            return StateDisponivel()

        if self.parent.norma_agendada:
            logger.info(f"[UG{self.parent.id}] Normalização por tempo acionada -> Tempo definido: {self.parent.tempo_normalizar}")
            self.parent.norma_agendada = False
            Thread(terget=lambda: self.espera_normalizar(self.parent.tempo_normalizar)).start()

        elif self.parar_timer:
            return self if self.normalizar_ug() else StateIndisponivel()

        else:
            logger.debug(f"[UG{self.parent.id}] Aguardando normalização sem tempo pré-definido")
            return self

        return self

    def espera_normalizar(self, delay: int) -> None:
        while not self.parar_timer:
            sleep(max(0, time() + delay - time()))
            self.parar_timer = True
            return

class StateDisponivel(State):
    def __init__(self, parent: UnidadeGeracao):
        super().__init__(parent)
        self.release_sinc = True
        self.release_press = True
        self.parent.codigo_state = UG_SM_DISPONIVEL
        logger.info(f"[UG{self.parent.id}] Entrando no estado disponível.")

    def step(self) -> State:
        self.parent.controle_limites_operacao()
        flag = self.parent.verificar_condicionadores()

        if flag == CONDIC_INDISPONIBILIZAR:
            logger.warning(f"[UG{self.parent.id}] Indisponibilizando UG.")
            return StateIndisponivel()

        elif flag == CONDIC_AGUARDAR:
            logger.warning(f"[UG{self.parent.id}] Entrando no estado Restrito até normalização da condição.")
            return StateRestrito()

        elif flag == CONDIC_NORMALIZAR:
            return self if self.normalizar_ug() else StateIndisponivel()

        else:
            logger.debug(f"[UG{self.parent.id}] Etapa atual: \"{self.parent.etapa_atual}\" / Etapa alvo: \"{self.parent.etapa_alvo}\"")

            if self.parent.limpeza_grade:
                self.parent.setpoint = self.cfg["pot_minima"] = self.parent.cfg["pot_limpeza_grade"]
            else:
                self.parent.atenuacao_carga()

            self.parent.controle_etapas()

            return self
