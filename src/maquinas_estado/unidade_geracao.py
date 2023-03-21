import logging

from time import sleep, time
from threading import Thread

from dicionarios.const import *
from src.ocorrencias import OcorrenciasUg
from src.unidade_geracao import UnidadeDeGeracao

logger = logging.getLogger("__main__")

class State:
    def __init__(self, parent: UnidadeDeGeracao=None, ocorrencias: OcorrenciasUg=None):
        # VERIFICAÇÃO DE ARGUENTOS
        if not parent or not ocorrencias:
            logger.error("[UG-SM] Houve um erro ao importar as classes Unidade de Geração e Ocorrências")
            raise ImportError
        else:
            self.parent = parent
            self.oco = ocorrencias

        # VARIÁVEIS PRIVADAS
        self.borda_trips: bool = False
        self.borda_parar: bool = False

    def step(self) -> object:
        pass

    def normalizar_ug(self) -> bool:
        if self.parent.tentativas_de_normalizacao > self.parent.limite_tentativas_de_normalizacao:
            logger.warning(f"[UG{self.parent.id}] A UG estourou as tentativas de normalização, indisponibilizando UG.")
            return False

        elif (self.parent.ts_auxiliar - self.parent.get_time()).seconds > self.parent.tempo_entre_tentativas:
            self.parent.tentativas_de_normalizacao += 1
            self.parent.ts_auxiliar = self.parent.get_time()
            logger.info(f"[UG{self.parent.id}] Normalizando UG (Tentativa {self.parent.tentativas_de_normalizacao}/{self.parent.limite_tentativas_de_normalizacao})")
            self.parent.reconhece_reset_alarmes()
            return True

    def bloquear_ug(self) -> None:
        if self.parent.etapa_atual == UG_PARADA: 
            self.parent.acionar_trips()
        elif not self.borda_parar and self.parent.parar():
            self.borda_parar = True

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
        logger.info(f"[UG{self.parent.id}] Entrando no estado: \"Indisponível\". Para retornar a operação autônoma, favor agendar na interface web")

        self.borda_parar = True if self.borda_parar else False

    def step(self) -> State:
        self.bloquear_ug()
        logger.debug(f"[UG{self.parent.id}] Unidade Indisponível.")
        return self

class StateRestrito(State):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.codigo_state = UG_SM_RESTRITA
        logger.info(f"[UG{self.parent.id}] Entrando no estado \"restrito\"")

        self.parar_timer: bool = False

        self.borda_parar = True if self.borda_parar else False

    def step(self) -> State:
        self.bloquear_ug()
        self.oco.controle_limites_operacao()
        flag = self.oco.verificar_condicionadores()

        if flag == CONDIC_INDISPONIBILIZAR:
            logger.warning(f"[UG{self.parent.id}] UG detectou condicionadores com gravidade alta, indisponibilizando UG.")
            self.parar_timer = True
            return StateIndisponivel()

        elif flag == CONDIC_IGNORAR:
            logger.info(f"[UG{self.parent.id}] A UG não possui mais condicionadores ativos, normalizando e retornando para o estado disponível")
            self.parar_timer = True
            self.parent.reconhece_reset_alarmes()
            return StateDisponivel()

        if self.parent.normalizacao_agendada:
            logger.info(f"[UG{self.parent.id}] Normalização por tempo acionada -> Tempo definido: {self.parent.tempo_normalizar}")
            self.parent.normalizacao_agendada = False
            Thread(target=lambda: self.espera_normalizar(self.parent.tempo_normalizar)).start()

        elif self.parar_timer:
            return self if self.normalizar_ug() else StateIndisponivel()

        else:
            logger.debug(f"[UG{self.parent.id}] Aguardando normalização sem tempo pré-definido")
            return self

    def espera_normalizar(self, delay: int):
        while not self.parar_timer:
            sleep(max(0, time() + delay - time()))
            self.parar_timer = True
            return

class StateDisponivel(State):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.codigo_state = UG_SM_DISPONIVEL
        logger.info(f"[UG{self.parent.id}] Entrando no estado: \"Disponível\"")

        self.borda_parar = False
        self.borda_partindo = False
        self.parent.tentativas_de_normalizacao = 0

    def step(self) -> State:
        self.oco.controle_limites_operacao()
        flag = self.oco.verificar_condicionadores()

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
                self.parent.setpoint = self.parent.setpoint_minimo = self.parent.cfg["pot_limpeza_grade"]
            else:
                self.atenuacao_carga()

            self.controle_etapas()

            return self


# TODO mudar métodos para dentro da classe da unidade de geração
    def atenuacao_carga(self) -> None:
        logger.debug(f"[UG{self.parent.id}] Atenuador \"{condic.descr}\" -> Atenuação: {max(0, condic.valor)} / Leitura: {condic.leitura}" for condic in self.oco.condicionadores_atenuadores) 

        ganho = 1 - max(0, [condic.ativo for condic in self.oco.condicionadores_atenuadores])
        aux = self.parent.setpoint
        if (self.parent.setpoint > self.parent.setpoint_minimo) and (self.parent.setpoint * ganho) > self.parent.setpoint_minimo:
            self.parent.setpoint = self.parent.setpoint * ganho

        elif (self.parent.setpoint * ganho < self.parent.setpoint_minimo) and (self.parent.setpoint > self.parent.setpoint_minimo):
            self.parent.setpoint = self.parent.setpoint_minimo

        logger.debug(f"[UG{self.parent.id}] SP {aux} * GANHO {ganho} = {self.parent.setpoint}")

    def verificar_partindo(self) -> None:
        while time() < (time() + 600):
            if self.parent.etapa_atual == UG_SINCRONIZADA or self.parent.release_timer:
                logger.debug(f"[UG{self.parent.id}] {'Modo manual ativado' if self.parent.release_timer else 'Unidade Sincronizada'}. Verificação de partida encerrada.")
                return
        logger.debug(f"[UG{self.parent.id}] Verificação de partida estourou o timer, acionando normalização.")
        self.borda_partindo = False
        self.parent.clp_usn.write_single_coil([f"UG{self.parent.id}_CD_EmergenciaViaSuper"], [1])
        sleep(1)
        self.parent.clp_usn.write_single_coil([f"UG{self.parent.id}_CD_EmergenciaViaSuper"], [0])

    def controle_etapas(self) -> None:
        # PARANDO
        if self.parent.etapa_alvo == UG_PARADA and not self.parent.etapa_atual == UG_PARADA:
            if self.parent.setpoint >= self.parent.setpoint_minimo:
                self.parent.enviar_setpoint(self.parent.setpoint)

        # SINCRONIZANDO
        elif self.parent.etapa_alvo == UG_SINCRONIZADA and not self.parent.etapa_atual == UG_SINCRONIZADA:
            if not self.borda_partindo:
                logger.debug(f"[UG{self.parent.id}] Iniciando o timer de verificação de partida")
                Thread(target=lambda: self.verificar_partindo()).start()
                self.borda_partindo = True

            self.parent.parar() if self.parent.setpoint == 0 else self.parent.enviar_setpoint(self.parent.setpoint)

        # PARADA
        elif self.parent.etapa_atual == UG_PARADA:
            if self.parent.setpoint >= self.parent.setpoint_minimo:
                self.parent.partir()
                self.parent.enviar_setpoint(self.parent.setpoint)

        # SINCRONIZADA
        elif self.parent.etapa_atual == UG_SINCRONIZADA:
            self.borda_partindo = False
            if not self.parent.aux_tempo_sincronizada:
                self.parent.aux_tempo_sincronizada = self.parent.get_time()

            elif (self.parent.get_time() - self.parent.aux_tempo_sincronizada).seconds >= 300:
                self.parent.tentativas_de_normalizacao = 0

            self.parent.parar() if self.parent.setpoint == 0 else self.parent.enviar_setpoint(self.parent.setpoint)

        # CONTROLE TEMPO SINCRONIZADAS
        if not self.parent.etapa_atual == UG_SINCRONIZADA:
            self.parent.aux_tempo_sincronizada = None