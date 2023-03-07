import pytz
import logging
import traceback

from time import sleep, time
from threading import Thread
from datetime import datetime

from conector import *
from leituras import *
from condicionadores import *
from dicionarios.reg import *
from dicionarios.const import *
from src.ocorrencias import Ocorrencias
from src.unidade_geracao import UnidadeDeGeracao

class State:
    def __init__(self, parent: UnidadeDeGeracao=None, ocorrencias: Ocorrencias=None):
        if not parent:
            logger.error("HOuve um erro ao importar a instância da Unidade de Geração")
            raise ReferenceError
        else:
            self.parent = parent
        
        if not ocorrencias:
            logger.error("Houve um erro ao importar a classe de Ocorrências.")
            raise ReferenceError
        else:
            self.ocorrencias = ocorrencias

    def step(self) -> object:
        pass

    @property
    def get_time(self):
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

class StateManual(State):
    def __init__(self):
        super().__init__(parent=None, ocorrencias=None)

        self.parent.codigo_state = MOA_UNIDADE_MANUAL
        logger.info(f"[UG{self.parent.id}] Entrando no estado: \"Manual\". Para retornar a operação autônoma, favor agendar na interface web")

    def step(self) -> State:
        self.parent.setpoint = self.parent.leitura_potencia.valor
        return self

class StateIndisponivel(State):
    def __init__(self):
        super().__init__(parent=None, ocorrencias=None)

        self.parent.codigo_state = MOA_UNIDADE_INDISPONIVEL

        self.selo = False
        self.parent.__next_state = self
        logger.info(f"[UG{self.parent.id}] Entrando no estado: \"Indisponível\". Para retornar a operação autônoma, favor agendar na interface web")

    def step(self) -> State:
        if self.parent.etapa_atual == UNIDADE_PARADA or self.selo:
            self.selo = True
            self.parent.acionar_trip_logico()
            self.parent.acionar_trip_eletrico()
        else:
            self.parent.parar()
        return self

class StateRestrito(State):
    def __init__(self):
        super().__init__(parent=None, ocorrencias=None)

        self.parent.codigo_state = MOA_UNIDADE_RESTRITA
        self.release = False
        self.parar_timer = False
        logger.info(f"[UG{self.parent.id}] Entrando no estado \"restrito\"")

    def step(self) -> State:
        condicionadores_ativos = self.ocorrencias.verificar_condicionadores_ug_restrito()

        if condicionadores_ativos:
            if self.parent.norma_agendada and not self.release:
                logger.info(f"[UG{self.parent.id}] Normalização por tempo ativada")
                logger.info(f"[UG{self.parent.id}] Aguardando normalização por tempo -> Tempo definido: {self.parent.tempo_normalizar}")
                self.release = True
                Thread(target=lambda: self.espera_normalizar(self.parent.tempo_normalizar)).start()
            elif not self.release:
                logger.debug(f"[UG{self.parent.id}] Aguardando normalização sem tempo pré-definido")

        elif not condicionadores_ativos:
            logger.info(f"[UG{self.parent.id}] A UG não possui mais condicionadores ativos, normalizando e retornando para o estado disponível")
            self.parent.tentativas_de_normalizacao += 1
            self.parent.norma_agendada = False
            self.parar_timer = True
            self.release = False
            self.parent.reconhece_reset_alarmes()
            return StateDisponivel(self.parent)

        if self.ocorrencias.deve_indisponibilizar_ug:
            logger.warning(f"[UG{self.parent.id}] UG detectou condicionadores com gravidade alta, indisponibilizando UG.\nCondicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
            self.parent.norma_agendada = False
            self.parar_timer = True
            self.release = False
            return StateIndisponivel(self.parent)

        elif self.deve_normalizar:
            if self.parent.tentativas_de_normalizacao > self.parent.limite_tentativas_de_normalizacao:
                logger.warning(f"[UG{self.parent.id}] A UG estourou as tentativas de normalização, indisponibilizando UG. \n Condicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
                self.parent.norma_agendada = False
                return StateIndisponivel(self.parent)

            elif (self.parent.ts_auxiliar - self.get_time).seconds > self.parent.tempo_entre_tentativas:
                self.parent.tentativas_de_normalizacao += 1
                logger.info(f"[UG{self.parent.id}] Normalizando UG (tentativa {self.parent.tentativas_de_normalizacao}/{self.parent.limite_tentativas_de_normalizacao})")
                self.parent.ts_auxiliar = self.get_time
                self.parent.reconhece_reset_alarmes()
                return self

        if self.parent.etapa_atual == UNIDADE_PARADA:
            self.parent.acionar_trip_logico()
            self.parent.acionar_trip_eletrico()
        else:
            self.parent.parar()
        return self

    def espera_normalizar(self, delay):
        tempo = time() + delay
        logger.debug(f"[UG{self.parent.id}] Aguardando para normalizar UG")
        while not self.parar_timer:
            sleep(max(0, tempo - time()))
            break
        self.release = False
        self.deve_normalizar = True

class StateDisponivel(State):
    def __init__(self):
        super().__init__(parent=None, ocorrencias=None)

        self.parent.codigo_state = MOA_UNIDADE_DISPONIVEL
        self.release = False
        self.borda_partindo = False
        self.parent.tentativas_de_normalizacao = 0
        logger.info(f"[UG{self.parent.id}] Entrando no estado: \"Disponível\"")

    def step(self) -> State:
        self.parent.controle_limites_operacao()
        condicionadores_ativos = []

        if self.ocorrencias.deve_indisponibilizar_ug or self.ocorrencias.deve_normalizar_ug or self.ocorrencias.deve_aguardar_ug:
            logger.info(f"[UG{self.parent.id}] UG em modo disponível detectou condicionadores ativos.\nCondicionadores ativos:")
            for d in condicionadores_ativos:
                logger.warning(f"Desc: {d.descr}; Ativo: {d.ativo}; Valor: {d.valor}; Gravidade: {d.gravidade}")

        if self.ocorrencias.deve_indisponibilizar_ug:
            logger.warning(f"[UG{self.parent.id}] Indisponibilizando UG.")
            return StateIndisponivel(self.parent)

        if self.ocorrencias.deve_aguardar_ug:
            logger.warning(f"[UG{self.parent.id}] Entrando no estado Restrito até normalização da condição.")
            return StateRestrito(self.parent)

        if self.ocorrencias.deve_normalizar_ug:
            if self.parent.tentativas_de_normalizacao > self.parent.limite_tentativas_de_normalizacao:
                logger.warning(f"[UG{self.parent.id}] A UG estourou as tentativas de normalização, indisponibilizando UG. \n Condicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
                return StateIndisponivel(self.parent)

            elif (self.parent.ts_auxiliar - self.get_time).seconds > self.parent.tempo_entre_tentativas:
                self.parent.tentativas_de_normalizacao += 1
                self.parent.ts_auxiliar = self.get_time
                logger.info(f"[UG{self.parent.id}] Normalizando UG (tentativa {self.parent.tentativas_de_normalizacao}/{self.parent.limite_tentativas_de_normalizacao})")
                self.parent.reconhece_reset_alarmes()
                return self

            else:
                return self

        else:
            if self.release and self.borda_partindo:
                self.release = False
                self.borda_partindo = False

            logger.debug(f"[UG{self.parent.id}] Etapa atual: \"{self.parent.etapa_atual}\" / Etapa alvo: \"{self.parent.etapa_alvo}\"")
            logger.debug(f"[UG{self.parent.id}] Lendo condicionadores_atenuadores")

            atenuacao = 0
            for condicionador in self.parent.condicionadores_atenuadores:
                atenuacao = max(atenuacao, condicionador.valor)
                logger.debug(f"[UG{self.parent.id}] Atenuador \"{condicionador.descr}\" -> Atenuação: {atenuacao} / Leitura: {condicionador.leitura.valor}")

            ganho = 1 - atenuacao
            aux = self.parent.setpoint
            if (self.parent.setpoint > self.parent.setpoint_minimo) and (self.parent.setpoint * ganho) > self.parent.setpoint_minimo:
                self.parent.setpoint = self.parent.setpoint * ganho

            elif self.parent.limpeza_grade:
                self.parent.setpoint_minimo = self.parent.self.dict["IP"]["pot_limpeza_grade"]
                self.parent.setpoint = self.parent.setpoint_minimo

            elif (self.parent.setpoint * ganho < self.parent.setpoint_minimo) and (self.parent.setpoint > self.parent.setpoint_minimo):
                self.parent.setpoint =  self.parent.setpoint_minimo

            logger.debug(f"[UG{self.parent.id}] SP {aux} * GANHO {ganho} = {self.parent.setpoint}")

            # PARANDO
            if self.parent.etapa_alvo == UNIDADE_PARADA and not self.parent.etapa_atual == UNIDADE_PARADA:
                if self.parent.setpoint >= self.parent.setpoint_minimo:
                    self.parent.enviar_setpoint(self.parent.setpoint)

            # SINCRONIZANDO
            elif self.parent.etapa_alvo == UNIDADE_SINCRONIZADA and not self.parent.etapa_atual == UNIDADE_SINCRONIZADA:
                if not self.release and not self.borda_partindo:
                    Thread(target=lambda: self.verificar_partindo()).start()
                    self.borda_partindo = True
                if self.parent.setpoint == 0:
                    logger.warning(f"[UG{self.parent.id}] A UG estava sincronizando com SP zerado, parando a UG.")
                    self.parent.parar()
                else:
                    self.parent.enviar_setpoint(self.parent.setpoint)

            # PARADA
            elif self.parent.etapa_atual == UNIDADE_PARADA:
                if self.parent.setpoint >= self.parent.setpoint_minimo:
                    self.parent.partir()
                    self.parent.enviar_setpoint(self.parent.setpoint)

            # SINCRONIZADA
            elif self.parent.etapa_atual == UNIDADE_SINCRONIZADA:
                if not self.parent.aux_tempo_sincronizada:
                    self.parent.aux_tempo_sincronizada = self.get_time

                elif (self.get_time - self.parent.aux_tempo_sincronizada).seconds >= 300:
                    self.parent.tentativas_de_normalizacao = 0
                
                if self.parent.setpoint == 0:
                    self.parent.parar()
                else:
                    self.parent.enviar_setpoint(self.parent.setpoint)

            elif self.parent.etapa_atual not in UNIDADE_LISTA_DE_ETAPAS:
                pass

            if not self.parent.etapa_atual == UNIDADE_SINCRONIZADA:
                self.parent.aux_tempo_sincronizada = None

            return self

    def verificar_partindo(self) -> bool:
        try:
            logger.debug(f"[UG{self.parent.id}] Iniciando o timer de verificação de partida")
            while time() < (time() + 600):
                if self.parent.etapa_atual == UNIDADE_SINCRONIZADA:
                    logger.debug(f"[UG{self.parent.id}] Unidade sincronizada. Saindo do timer de verificação de partida")
                    self.release = True
                    return True
                elif self.parent.release_timer:
                    logger.debug(f"[UG{self.parent.id}] MOA entrou em modo manua. Saindo do timer de verificação de partida.")
                    self.release = True
                    return False
            logger.debug(f"[UG{self.parent.id}] A Unidade estourou o timer de verificação de partida, adicionando condição para normalizar")
            self.parent.clp_sa.write_single_coil([f"REG_UG{self.parent.id}_ComandosDigitais_MXW_EmergenciaViaSuper"], [1]) 
            self.release = True
        except Exception:
            logger.error(f"[UG{self.parent.id}] Erro na execução do timer de verificação de partida.\nException: {traceback.print_stack}")
        return False
