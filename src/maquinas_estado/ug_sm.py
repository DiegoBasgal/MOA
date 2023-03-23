import pytz
import logging

from threading import Thread
from datetime import datetime
from abc import abstractmethod

from dicionarios.dict import *
from dicionarios.const import *

from unidade_geracao import UnidadeGeracao

logger = logging.getLogger("__main__")

class State:
    def __init__(self, parent_ug: UnidadeGeracao):
        self.parent_ug = parent_ug

    @abstractmethod
    def step(self) -> object:
        pass

class StateManual(State):
    def __init__(self, parent_ug: UnidadeGeracao):
        super().__init__(parent_ug)
        self.parent_ug.codigo_state = UG_SM_MANUAL
        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado manual. Para retornar a operação autônoma da UG é necessário intervenção manual via interface web.")

    def step(self) -> State:
        self.parent_ug.setpoint = self.parent_ug.leitura_potencia.valor
        return self

class StateIndisponivel(State):
    def __init__(self, parent_ug: UnidadeGeracao):
        super().__init__(parent_ug)
        self.selo = False
        self.parent_ug._next_state = self
        self.parent_ug.codigo_state = UG_SM_INDISPONIVEL
        logger.warning(f"[UG{self.parent_ug.id}] Entrando no estado indisponível. Para retornar a operação autônoma da UG é necessário intervenção manual via interface web.")

    def step(self) -> State:
        logger.debug(f"[UG{self.parent_ug.id}] Etapa atual -> {self.parent_ug.etapa_atual}")
        if self.parent_ug.etapa_atual == UG_PARADA or self.selo:
            self.selo = True
            self.parent_ug.fechar_comporta()
            if self.parent_ug.etapa_comporta == CP_FECHADA:
                self.parent_ug.acionar_trip_logico()
                self.parent_ug.acionar_trip_eletrico()
            else:
                logger.debug("[UG{0}] A comporta {0} deve estar completamente fechada para acionar o bloqueio da UG")
        else:
            self.parent_ug.parar()
        return self

class StateRestrito(State):
    def __init__(self, parent_ug: UnidadeGeracao):
        super().__init__(parent_ug)
        self.parent_ug.codigo_state = UG_SM_RESTRITA
        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado restrito.")

    def step(self) -> State:
        CONDIC_INDISPONIBILIZAR = False
        condicionadores_ativos = []

        for condicionador_essencial in self.parent_ug.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.parent_ug.deve_ler_condicionadores = True

        if self.parent_ug.deve_ler_condicionadores:
            for condicionador_essencial in self.parent_ug.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade == CONDIC_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    CONDIC_INDISPONIBILIZAR = True

            for condicionador in self.parent_ug.condicionadores:
                if condicionador.ativo and condicionador.gravidade == CONDIC_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador)
                    CONDIC_INDISPONIBILIZAR = True
            self.parent_ug.deve_ler_condicionadores = False

        if CONDIC_INDISPONIBILIZAR:
            logger.warning(f"[UG{self.parent_ug.id}] UG em modo disponível detectou condicionadores ativos, indisponibilizando UG.\nCondicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
            return StateIndisponivel(self.parent_ug)

        elif self.parent_ug.etapa_atual == UG_PARADA or self.selo:
            self.selo = True
            self.parent_ug.fechar_comporta()
            if self.parent_ug.etapa_comporta == CP_FECHADA:
                self.parent_ug.acionar_trip_logico()
                self.parent_ug.acionar_trip_eletrico()
            else:
                logger.debug("[UG{0}] A comporta {0} deve estar completamente fechada para acionar o bloqueio da UG")
        else:
            self.parent_ug.parar()
        return self

class StateDisponivel(State):
    def __init__(self, parent_ug: UnidadeGeracao):
        super().__init__(parent_ug)
        self.release_sinc = True
        self.release_press = True
        self.parent_ug.codigo_state = UG_SM_DISPONIVEL
        logger.info(f"[UG{self.parent_ug.id}] Entrando no estado disponível.")

    def step(self) -> State:
        logger.debug(f"[UG{self.parent_ug.id}] (tentativas_de_normalizacao atual: {self.parent_ug.tentativas_de_normalizacao})")
        CONDIC_NORMALIZAR = False
        CONDIC_INDISPONIBILIZAR = False
        condicionadores_ativos = []
        self.parent_ug.controle_limites_operacao()

        for condicionador_essencial in self.parent_ug.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.parent_ug.deve_ler_condicionadores = True

        if self.parent_ug.deve_ler_condicionadores:
            for condicionador_essencial in self.parent_ug.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade == CONDIC_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    CONDIC_INDISPONIBILIZAR = True
                elif condicionador_essencial.ativo and condicionador_essencial.gravidade == CONDIC_NORMALIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    CONDIC_NORMALIZAR = True

            for condicionador in self.parent_ug.condicionadores:
                if condicionador.ativo and condicionador.gravidade == CONDIC_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador)
                    CONDIC_INDISPONIBILIZAR = True
                elif condicionador.ativo and condicionador.gravidade == CONDIC_NORMALIZAR:
                    condicionadores_ativos.append(condicionador)
                    CONDIC_NORMALIZAR = True
            self.parent_ug.deve_ler_condicionadores = False

        if CONDIC_INDISPONIBILIZAR or CONDIC_NORMALIZAR:
            logger.info(f"[UG{self.parent_ug.id}] UG em modo disponível detectou condicionadores ativos.\nCondicionadores ativos:")
            for d in condicionadores_ativos:
                logger.warning(f"Desc: {d.descr}; Gravidade: {CONDIC_STR_DCT[d.gravidade]}")

        if CONDIC_INDISPONIBILIZAR:
            logger.warning(f"[UG{self.parent_ug.id}] Indisponibilizando UG.")
            return StateIndisponivel(self.parent_ug)

        if CONDIC_NORMALIZAR:
            if (self.parent_ug.tentativas_de_normalizacao > self.parent_ug.limite_tentativas_de_normalizacao):
                logger.warning(f"[UG{self.parent_ug.id}] A UG estourou as tentativas de normalização, indisponibilizando UG. \n Condicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
                return StateIndisponivel(self.parent_ug)

            elif (self.parent_ug.ts_auxiliar - datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)).seconds > self.parent_ug.tempo_entre_tentativas:
                self.parent_ug.tentativas_de_normalizacao += 1
                self.parent_ug.ts_auxiliar = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
                logger.info(f"[UG{self.parent_ug.id}] Normalizando UG (tentativa {self.parent_ug.tentativas_de_normalizacao}/{self.parent_ug.limite_tentativas_de_normalizacao}).")
                self.parent_ug.reconhece_reset_alarmes()
                return self

            else:
                return self

        else:
            logger.debug(f"[UG{self.parent_ug.id}] Etapa atual: {self.parent_ug.etapa_atual}")
            atenuacao = 0
            logger.debug(f"[UG{self.parent_ug.id}] Lendo condicionadores_atenuadores")
            for condicionador in self.parent_ug.condicionadores_atenuadores:
                atenuacao = max(atenuacao, condicionador.valor)
                logger.debug(f"[UG{self.parent_ug.id}] Atenuador \"{condicionador.descr}\" -> leitura: {condicionador.leitura.valor}-> atenucao: {atenuacao}")

            ganho = 1 - atenuacao
            aux = self.parent_ug.setpoint
            if (self.parent_ug.setpoint > self.parent_ug.setpoint_minimo) and self.parent_ug.setpoint * ganho > self.parent_ug.setpoint_minimo:
                self.parent_ug.setpoint = self.parent_ug.setpoint * ganho

            elif self.parent_ug.limpeza_grade:
                self.parent_ug.setpoint_minimo = self.parent_ug.cfg["pot_limpeza_grade"]
                self.parent_ug.setpoint = self.parent_ug.setpoint_minimo

            elif (self.parent_ug.setpoint * ganho < self.parent_ug.setpoint_minimo) and (self.parent_ug.setpoint > self.parent_ug.setpoint_minimo):
                self.parent_ug.setpoint =  self.parent_ug.setpoint_minimo

            logger.debug(f"[UG{self.parent_ug.id}] SP {aux} * GAIN {ganho} = {self.parent_ug.setpoint}")

            if self.parent_ug.etapa_atual == UG_PARANDO:
                logger.debug(f"[UG{self.parent_ug.id}] Unidade parando")
                if self.parent_ug.leitura_potencia < 300:
                    self.parent_ug.fechar_comporta()

                elif self.parent_ug.setpoint >= self.parent_ug.setpoint_minimo:
                    if self.parent_ug.etapa_comporta == CP_FECHADA:
                        self.parent_ug.cracking_comporta()

                    elif self.parent_ug.etapa_comporta == CP_CRACKING:
                        if not self.parent_ug.timer_press and self.release_press:
                            Thread(target=lambda: self.parent_ug.verificar_pressao()).start()
                            self.release_press = False
                        elif self.parent_ug.timer_press and not self.release_press:
                            self.parent_ug.timer_press = False
                            self.release_press = True
                            self.parent_ug.abrir_comporta()

                    elif self.parent_ug.etapa_comporta == CP_ABERTA:
                        self.parent_ug.partir()
                        self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)
                        if not self.parent_ug.timer_sinc and self.release_sinc:
                            Thread(target=lambda: self.parent_ug.verificar_partindo()).start()
                            self.release_sinc = False
                        elif self.parent_ug.timer_sinc and not self.release_sinc:
                            self.parent_ug.timer_sinc = False
                            self.timer_sinc = True

                    elif self.parent_ug.etapa_comporta == CP_REMOTO:
                        logger.debug("[UG{0}] Comporta {0} em modo manual")
                        pass

                    else:
                        logger.debug("[UG{0}] Comporta {0} entre etapas/etapa inconsistente")

            elif self.parent_ug.etapa_atual == UG_SINCRONIZANDO:
                logger.debug(f"[UG{self.parent_ug.id}] Unidade sincronizando")
                if self.parent_ug.setpoint == 0:
                    logger.warning(f"[UG{self.parent_ug.id}] A UG estava sincronizando com SP zerado, parando a UG.")
                    self.parent_ug.parar()

            elif self.parent_ug.etapa_atual == UG_PARADA:
                logger.debug(f"[UG{self.parent_ug.id}] Unidade parada")
                if self.parent_ug.setpoint >= self.parent_ug.setpoint_minimo:

                    if self.parent_ug.etapa_comporta == CP_FECHADA:
                        self.parent_ug.cracking_comporta()

                    elif self.parent_ug.etapa_comporta == CP_CRACKING:
                        if not self.parent_ug.timer_press and self.release_press:
                            Thread(target=lambda: self.parent_ug.verificar_pressao()).start()
                            self.release_press = False
                        elif self.parent_ug.timer_press and not self.release_press:
                            self.parent_ug.timer_press = False
                            self.release_press = True
                            self.parent_ug.abrir_comporta()

                    elif self.parent_ug.etapa_comporta == CP_ABERTA:
                        self.parent_ug.partir()
                        self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)
                        if not self.parent_ug.timer_sinc and self.release_sinc:
                            Thread(target=lambda: self.parent_ug.verificar_partindo()).start()
                            self.release_sinc = False
                        elif self.parent_ug.timer_sinc and not self.release_sinc:
                            self.parent_ug.timer_sinc = False
                            self.timer_sinc = True

                    elif self.parent_ug.etapa_comporta == CP_REMOTO:
                        logger.debug("[UG{0}] Comporta {0} em modo manual")
                        pass

                    else:
                        logger.debug("[UG{0}] Comporta {0} entre etapas/etapa inconsistente")

            elif self.parent_ug.etapa_atual == UG_SINCRONIZADA:
                logger.debug(f"[UG{self.parent_ug.id}] Unidade sincronizada")
                if not self.parent_ug.aux_tempo_sincronizada:
                    self.parent_ug.aux_tempo_sincronizada = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

                elif (datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None) - self.parent_ug.aux_tempo_sincronizada).seconds >= 300:
                    self.parent_ug.tentativas_de_normalizacao = 0

                if self.parent_ug.setpoint == 0:
                    self.parent_ug.parar()
                else:
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif self.parent_ug.etapa_atual not in UG_LST_ETAPAS:
                logger.warning(f"[UG{self.parent_ug.id}] UG em etapa inconsistente. (etapa_atual:{self.parent_ug.etapa_atual})")

            if not self.parent_ug.etapa_atual == UG_SINCRONIZADA:
                self.parent_ug.aux_tempo_sincronizada = None

            return self
