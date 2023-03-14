import logging
import traceback

from time import sleep, time
from threading import Thread

from dicionarios.const import *
from src.ocorrencias import OcorrenciasUg
from src.unidade_geracao import UnidadeDeGeracao

logger = logging.getLogger("__main__")

class State:
    def __init__(self, parent: UnidadeDeGeracao=None, ocorrencias: OcorrenciasUg=None):
        if not parent:
            logger.error("[UG-SM] Houve um erro ao importar a instância da Unidade de Geração")
            raise ReferenceError
        else:
            self.parent = parent

        if not ocorrencias:
            logger.error("[UG-SM] Houve um erro ao importar a classe de Ocorrências.")
            raise ReferenceError
        else:
            self.oco = ocorrencias

    def step(self) -> object:
        pass

    def normalizar_ug(self) -> bool:
        if self.parent.tentativas_de_normalizacao > self.parent.limite_tentativas_de_normalizacao:
            logger.warning(f"[UG{self.parent.id}] A UG estourou as tentativas de normalização, indisponibilizando UG.")
            return False

        elif (self.parent.ts_auxiliar - self.parent.get_time).seconds > self.parent.tempo_entre_tentativas:
            self.parent.tentativas_de_normalizacao += 1
            self.parent.ts_auxiliar = self.parent.get_time
            logger.info(f"[UG{self.parent.id}] Normalizando UG (tentativa {self.parent.tentativas_de_normalizacao}/{self.parent.limite_tentativas_de_normalizacao})")
            self.parent.reconhece_reset_alarmes()
            return True

class StateManual(State):
    def __init__(self):
        super().__init__()
        self.parent.codigo_state = MOA_UNIDADE_MANUAL
        logger.info(f"[UG{self.parent.id}] Entrando no estado: \"Manual\". Para retornar a operação autônoma, favor agendar na interface web")

    def step(self) -> State:
        self.parent.setpoint = self.parent.leitura_potencia.valor
        return self

class StateIndisponivel(State):
    def __init__(self):
        super().__init__()
        self.parent.codigo_state = MOA_UNIDADE_INDISPONIVEL
        logger.info(f"[UG{self.parent.id}] Entrando no estado: \"Indisponível\". Para retornar a operação autônoma, favor agendar na interface web")

    def step(self) -> State:
        self.parent.acionar_trips() if self.parent.etapa_atual == UNIDADE_PARADA else self.parent.parar()
        return self

class StateRestrito(State):
    def __init__(self):
        super().__init__()
        self.parent.codigo_state = MOA_UNIDADE_RESTRITA

        self.release = False
        self.parar_timer = False
        self.deve_normalizar = False

        logger.info(f"[UG{self.parent.id}] Entrando no estado \"restrito\"")

    def step(self) -> State:
        self.parent.acionar_trips() if self.parent.etapa_atual == UNIDADE_PARADA else self.parent.parar()

        condicionadores_ativos = [condic for condics in [self.oco.condicionadores_essenciais, self.oco.condicionadores] for condic in condics if condic.ativo]
        deve_indisponibilizar = [True for condic in condicionadores_ativos if condic.gravidade == DEVE_INDISPONIBILIZAR]

        if condicionadores_ativos:
            if self.parent.norma_agendada and not self.release:
                logger.info(f"[UG{self.parent.id}] Normalização por tempo acionada -> Tempo definido: {self.parent.tempo_normalizar}")
                self.release = True
                Thread(target=lambda: self.espera_normalizar(self.parent.tempo_normalizar)).start()
            elif not self.release:
                logger.debug(f"[UG{self.parent.id}] Aguardando normalização sem tempo pré-definido")

            if deve_indisponibilizar:
                logger.warning(f"[UG{self.parent.id}] UG detectou condicionadores com gravidade alta, indisponibilizando UG.")
                self.parent.norma_agendada = False
                self.parar_timer = True
                self.release = False
                return StateIndisponivel(self.parent)

            elif self.deve_normalizar:
                return self if self.normalizar_ug() else StateIndisponivel(self.parent)

        else:
            logger.info(f"[UG{self.parent.id}] A UG não possui mais condicionadores ativos, normalizando e retornando para o estado disponível")
            self.parent.tentativas_de_normalizacao += 1
            self.parent.norma_agendada = False
            self.parar_timer = True
            self.release = False
            self.parent.reconhece_reset_alarmes()
            return StateDisponivel(self.parent)

        return self

    def espera_normalizar(self, delay):
        while not self.parar_timer:
            sleep(max(0, time() + delay - time()))
            break
        self.release = False
        self.deve_normalizar = True

class StateDisponivel(State):
    def __init__(self):
        super().__init__()

        self.parent.codigo_state = MOA_UNIDADE_DISPONIVEL

        self.release = False
        self.borda_partindo = False
        self.parent.tentativas_de_normalizacao = 0

        logger.info(f"[UG{self.parent.id}] Entrando no estado: \"Disponível\"")

    def step(self) -> State:
        self.parent.controle_limites_operacao()

        if self.oco.verificar_condicionadores():
            if self.oco.aguardar:
                logger.warning(f"[UG{self.parent.id}] Entrando no estado Restrito até normalização da condição.")
                return StateRestrito(self.parent)

            if self.oco.normalizar:
                return self if self.normalizar_ug() else StateIndisponivel(self.parent)

            if self.oco.indisponibilizar:
                logger.warning(f"[UG{self.parent.id}] UG detectou condicionadores com gravidade alta, indisponibilizando UG.")
                return StateIndisponivel(self.parent)

        else:
            logger.debug(f"[UG{self.parent.id}] Etapa atual: \"{self.parent.etapa_atual}\" / Etapa alvo: \"{self.parent.etapa_alvo}\"")
            logger.debug(f"[UG{self.parent.id}] Lendo condicionadores_atenuadores")

            if self.parent.limpeza_grade:
                self.parent.setpoint_minimo = self.parent.cfg["pot_limpeza_grade"]
                self.parent.setpoint = self.parent.setpoint_minimo
            else:
                self.atenuacao_carga()

            self.controle_etapas()

            if not self.parent.etapa_atual == UNIDADE_SINCRONIZADA:
                self.parent.aux_tempo_sincronizada = None

            return self

    def atenuacao_carga(self) -> None:
        atenuacao = 0
        for condic in self.parent.condicionadores_atenuadores:
            atenuacao = max(atenuacao, condic.valor)
            logger.debug(f"[UG{self.parent.id}] Atenuador \"{condic.descr}\" -> Atenuação: {atenuacao} / Leitura: {condic.leitura.valor}")

        ganho = 1 - atenuacao
        aux = self.parent.setpoint
        if (self.parent.setpoint > self.parent.setpoint_minimo) and (self.parent.setpoint * ganho) > self.parent.setpoint_minimo:
            self.parent.setpoint = self.parent.setpoint * ganho

        elif (self.parent.setpoint * ganho < self.parent.setpoint_minimo) and (self.parent.setpoint > self.parent.setpoint_minimo):
            self.parent.setpoint = self.parent.setpoint_minimo

        logger.debug(f"[UG{self.parent.id}] SP {aux} * GANHO {ganho} = {self.parent.setpoint}")

    def verificar_partindo(self) -> None:
        try:
            while time() < (time() + 600):
                if self.parent.etapa_atual == UNIDADE_SINCRONIZADA:
                    logger.debug(f"[UG{self.parent.id}] Unidade sincronizada. Verificar partindo encerrado.")
                    return
                elif self.parent.release_timer:
                    self.release = False
                    logger.debug(f"[UG{self.parent.id}] MOA entrou em modo manual. Verificar partindo encerrado.")
                    return
            self.release = False
            self.parent.clp_usn.write_single_coil([f"REG_UG{self.parent.id}_ComandosDigitais_MXW_EmergenciaViaSuper"], [1])
            logger.debug(f"[UG{self.parent.id}] Verificação de partida estourou o timer, acionando normalização.")

        except Exception as e:
            logger.exception(f"[UG{self.parent.id}] Erro na execução do timer de verificação de partida. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.parent.id}] Traceback: {traceback.print_stack}")

    def controle_etapas(self) -> None:
        # PARANDO
        if self.parent.etapa_alvo == UNIDADE_PARADA and not self.parent.etapa_atual == UNIDADE_PARADA:
            if self.parent.setpoint >= self.parent.setpoint_minimo:
                self.parent.enviar_setpoint(self.parent.setpoint)
            return

        # SINCRONIZANDO
        elif self.parent.etapa_alvo == UNIDADE_SINCRONIZADA and not self.parent.etapa_atual == UNIDADE_SINCRONIZADA:
            if not self.release and not self.borda_partindo:
                logger.debug(f"[UG{self.parent.id}] Iniciando o timer de verificação de partida")
                Thread(target=lambda: self.verificar_partindo()).start()
                self.borda_partindo = True

            self.parent.parar() if self.parent.setpoint == 0 else self.parent.enviar_setpoint(self.parent.setpoint)
            return

        # PARADA
        elif self.parent.etapa_atual == UNIDADE_PARADA:
            if self.parent.setpoint >= self.parent.setpoint_minimo:
                self.parent.partir()
                self.parent.enviar_setpoint(self.parent.setpoint)
            return

        # SINCRONIZADA
        elif self.parent.etapa_atual == UNIDADE_SINCRONIZADA:
            self.release = False
            self.borda_partindo = False
            if not self.parent.aux_tempo_sincronizada:
                self.parent.aux_tempo_sincronizada = self.parent.get_time

            elif (self.parent.get_time - self.parent.aux_tempo_sincronizada).seconds >= 300:
                self.parent.tentativas_de_normalizacao = 0

            self.parent.parar() if self.parent.setpoint == 0 else self.parent.enviar_setpoint(self.parent.setpoint)
            return