import pytz
import logging
import traceback

from time import time
from threading import Thread
from datetime import datetime
from abc import abstractmethod

from src.dicionarios.const import *
from src.dicionarios.regs import *

logger = logging.getLogger("__main__")

class State:
    def __init__(self, parent_ug):
        self.parent_ug = parent_ug

    @abstractmethod
    def step(self) -> "State":
        pass

class StateManual(State):
    def __init__(self, parent_ug):
        super().__init__(parent_ug)
        self.parent_ug.codigo_state = MOA_UNIDADE_MANUAL
        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado: \"Manual\". Para retornar a operação autônoma, favor agendar na interface web")

    def step(self) -> State:
        self.parent_ug.setpoint = self.parent_ug.leitura_potencia.valor
        return self

class StateIndisponivel(State):
    def __init__(self, parent_ug):
        super().__init__(parent_ug)
        self.parent_ug.codigo_state = MOA_UNIDADE_INDISPONIVEL

        self.selo = False
        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado: \"Indisponível\". Para retornar a operação autônoma, favor agendar na interface web")
        self.parent_ug.__next_state = self
        self.parent_ug.release_timer = True

    def step(self) -> State:
        logger.debug(f"[UG{self.parent_ug.id}] Etapa atual: \"{UNIDADE_DICT_ETAPAS[self.parent_ug.etapa_atual]}\"")

        if self.parent_ug.etapa_atual == UNIDADE_PARADA or self.selo:
            self.selo = True
            self.parent_ug.acionar_trip_logico()
            self.parent_ug.acionar_trip_eletrico()
        else:
            self.parent_ug.parar()
        return self

class StateRestrito(State):
    def __init__(self, parent_ug):
        super().__init__(parent_ug)
        self.parent_ug.codigo_state = MOA_UNIDADE_RESTRITA
        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado: \"Restrito\"")

    def step(self) -> State:
        deve_indisponibilizar = False
        condicionadores_ativos = []

        for condic in self.parent_ug.condicionadores_essenciais:
            if condic.ativo:
                self.parent_ug.deve_ler_condicionadores = True
                break

        if self.parent_ug.deve_ler_condicionadores:
            for condic in self.parent_ug.condicionadores_essenciais:
                if condic.ativo:
                    deve_indisponibilizar = True if condic.gravidade == DEVE_INDISPONIBILIZAR else ...
                    condicionadores_ativos.append(condic)

            for condic in self.parent_ug.condicionadores:
                if condic.ativo:
                    deve_indisponibilizar = True if condic.gravidade == DEVE_INDISPONIBILIZAR else ...
                    condicionadores_ativos.append(condic)

        if deve_indisponibilizar:
            logger.warning(f"[UG{self.parent_ug.id}] UG em modo Restrito detectou condicionadores ativos, indisponibilizando UG.")
            for d in condicionadores_ativos:
                logger.info(f"[UG{self.parent_ug.id}] Registrador: \"{d.descr}\", Gravidade: \"{CONDIC_STR_DCT[d.gravidade] if d.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
            return StateIndisponivel(self.parent_ug)

        if self.parent_ug.etapa_atual == UNIDADE_PARADA:
            self.parent_ug.acionar_trip_logico()
            self.parent_ug.acionar_trip_eletrico()

        else:
            self.parent_ug.parar()

        return self


class StateDisponivel(State):
    def __init__(self, parent_ug):
        super().__init__(parent_ug)
        self.parent_ug.codigo_state = MOA_UNIDADE_DISPONIVEL
        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado: \"Disponível\"")

        self.release = False
        self.borda_partindo = False
        self.parent_ug.tentativas_de_normalizacao = 0

    def step(self) -> State:
        self.parent_ug.controle_limites_operacao()

        deve_normalizar = False
        deve_indisponibilizar = False
        condicionadores_ativos = []

        for condic in self.parent_ug.condicionadores_essenciais:
            if condic.ativo:
                self.parent_ug.deve_ler_condicionadores = True
                break

        if self.parent_ug.deve_ler_condicionadores:
            for condicionador_essencial in self.parent_ug.condicionadores_essenciais:
                if condicionador_essencial.ativo:
                    if condicionador_essencial == DEVE_INDISPONIBILIZAR:
                        condicionadores_ativos.append(condicionador_essencial)
                        deve_indisponibilizar = True
                    elif condicionador_essencial.gravidade == DEVE_NORMALIZAR:
                        condicionadores_ativos.append(condicionador_essencial)
                        self.parent_ug.deve_ler_condicionadores = False
                        deve_normalizar = True

            for condicionador in self.parent_ug.condicionadores:
                if condicionador.ativo: 
                    if condicionador.gravidade == DEVE_INDISPONIBILIZAR:
                        condicionadores_ativos.append(condicionador)
                        deve_indisponibilizar = True
                    elif condicionador.gravidade == DEVE_NORMALIZAR:
                        condicionadores_ativos.append(condicionador)
                        self.parent_ug.deve_ler_condicionadores = False
                        deve_normalizar = True

        if deve_indisponibilizar or deve_normalizar:
            logger.info(f"[UG{self.parent_ug.id}] UG em modo disponível detectou condicionadores ativos:")
            for d in condicionadores_ativos:
                logger.info(f"[UG{self.parent_ug.id}] Registrador: \"{d.descr}\", Gravidade: \"{CONDIC_STR_DCT[d.gravidade] if d.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")

        if deve_indisponibilizar:
            logger.warning(f"[UG{self.parent_ug.id}] Indisponibilizando UG por gravidade.")
            self.parent_ug.deve_ler_condicionadores = False
            return StateIndisponivel(self.parent_ug)

        if deve_normalizar:
            if (self.parent_ug.tentativas_de_normalizacao > self.parent_ug.limite_tentativas_de_normalizacao):
                logger.warning(f"[UG{self.parent_ug.id}] Indisponibilizando UG por tentativas de normalização.")
                self.parent_ug.deve_ler_condicionadores = False
                return StateIndisponivel(self.parent_ug)

            elif self.parent_ug.etapa_atual == UNIDADE_PARANDO or self.parent_ug.etapa_atual == UNIDADE_SINCRONIZANDO:
                logger.debug(f"[UG{self.parent_ug.id}] Esperando para normalizar")
                self.parent_ug.deve_ler_condicionadores = False
                return self

            elif (self.parent_ug.ts_auxiliar - self.parent_ug.get_time()).seconds > self.parent_ug.tempo_entre_tentativas:
                self.parent_ug.tentativas_de_normalizacao += 1
                self.parent_ug.ts_auxiliar = self.parent_ug.get_time()
                logger.info(f"[UG{self.parent_ug.id}] Normalizando UG (tentativa {self.parent_ug.tentativas_de_normalizacao}/{self.parent_ug.limite_tentativas_de_normalizacao}).")
                self.parent_ug.reconhece_reset_alarmes()
                self.parent_ug.deve_ler_condicionadores = False
                return self

            else:
                self.parent_ug.deve_ler_condicionadores = False
                return self

        else:
            logger.debug(f"[UG{self.parent_ug.id}] Etapa atual: \"{UNIDADE_DICT_ETAPAS[self.parent_ug.etapa_atual]}\"")

            # Ajuste de ganho CX Espiral
            atenuacao = 0
            for condicionador in self.parent_ug.condicionadores_atenuadores:
                atenuacao = max(atenuacao, condicionador.valor)
                logger.debug(f"[UG{self.parent_ug.id}] Atenuador \"{condicionador.descr}\" -> Atenuação: {atenuacao} / Leitura: {condicionador.leitura.valor}")

            ganho = 1 - atenuacao
            aux = self.parent_ug.setpoint
            if (self.parent_ug.setpoint > self.parent_ug.setpoint_minimo) and self.parent_ug.setpoint * ganho > self.parent_ug.setpoint_minimo:
                self.parent_ug.setpoint = self.parent_ug.setpoint * ganho

            elif self.parent_ug.limpeza_grade:
                self.parent_ug.setpoint_minimo = self.parent_ug.cfg["pot_limpeza_grade"]
                self.parent_ug.setpoint = self.parent_ug.setpoint_minimo

            elif (self.parent_ug.setpoint * ganho < self.parent_ug.setpoint_minimo) and (self.parent_ug.setpoint > self.parent_ug.setpoint_minimo):
                self.parent_ug.setpoint =  self.parent_ug.setpoint_minimo

            logger.debug(f"[UG{self.parent_ug.id}] SP {aux} * GANHO {ganho} = {self.parent_ug.setpoint}")

            # Controle de etapas
            if self.parent_ug.etapa_atual == UNIDADE_PARANDO:
                if self.parent_ug.setpoint >= self.parent_ug.setpoint_minimo:
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif self.parent_ug.etapa_atual == UNIDADE_SINCRONIZANDO:
                if not self.release and not self.borda_partindo:
                    Thread(target=lambda: self.verificar_partindo()).start()
                    self.borda_partindo = True

                if self.parent_ug.setpoint == 0:
                    logger.warning(f"[UG{self.parent_ug.id}] A UG estava sincronizando com SP zerado, parando a UG.")
                    self.parent_ug.parar()
                else:
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif self.parent_ug.etapa_atual == UNIDADE_PARADA:
                if self.parent_ug.setpoint >= self.parent_ug.setpoint_minimo:
                    self.parent_ug.partir()
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                self.borda_partindo = False
                if not self.parent_ug.aux_tempo_sincronizada:
                    self.parent_ug.aux_tempo_sincronizada = self.parent_ug.get_time()

                elif (self.parent_ug.get_time() - self.parent_ug.aux_tempo_sincronizada).seconds >= 300:
                    self.parent_ug.tentativas_de_normalizacao = 0

                if self.parent_ug.setpoint == 0:
                    self.parent_ug.parar()
                else:
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            if self.parent_ug.etapa_atual not in UNIDADE_LISTA_DE_ETAPAS:
                self.parent_ug.inconsistente = True

            if not self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                self.parent_ug.aux_tempo_sincronizada = None

            return self

    def verificar_partindo(self) -> None:
        timer = time() + 600
        try:
            logger.debug(f"[UG{self.parent_ug.id}] Iniciando o timer de verificação de partida")
            while time() < timer:
                if self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA or self.parent_ug.release_timer:
                    logger.debug(f"[UG{self.parent_ug.id}] Condição ativada! Saindo do timer de verificação de partida")
                    self.parent_ug.release_timer = False
                    self.release = True
                    return

            logger.debug(f"[UG{self.parent_ug.id}] A Unidade estourou o timer de verificação de partida, adicionando condição para normalizar")
            self.parent_ug.clp[f"UG{self.parent_ug.id}"].write_single_coil(REG[f"UG{self.parent_ug.id}_CD_EmergenciaViaSuper"], [1])
            self.borda_partindo = False
            self.release = True

        except Exception:
            logger.error(f"[UG{self.parent_ug.id}] Erro no timer de verificação de partida.")
            logger.debug(f"[UG{self.parent_ug.id}] Traceback: {traceback.format_exc()}")
