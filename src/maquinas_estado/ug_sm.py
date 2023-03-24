__author__ = "Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal"
__credits__ = "Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal"

__version__ = "0.2"
__status__ = "Development"
__maintainer__ = "Diego Basgal"
__email__ = "diego.garcia@ritmoenergia.com.br"
__description__ = "Este módulo corresponde a implementação da máquina das Unidades de Geração."

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
    def __init__(self, parent: UnidadeGeracao | None = ...) -> ...:
        if not parent:
            raise ValueError("[UG-SM] Não foi possível carregar a instânica da Unidade de Geração.")
        else:
            self.parent = parent

        self.cfg = parent.cfg

    @abstractmethod
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
        self.parent.parar_timer = True
        if self.parent.etapa_atual == UG_PARADA:
            if self.parent.cp.etapa_comporta in (CP_ABERTA, CP_CRACKING):
                self.parent.cp.fechar_comporta()
            elif self.parent.cp.etapa_comporta == CP_FECHADA:
                self.parent.acionar_trips()
            else:
                logger.debug(f"[UG{self.parent.id}] A comporta {self.parent.id} deve estar completamente fechada para acionar o bloqueio da UG")
        elif not self.borda_parar and self.parent.parar():
            self.borda_parar = True
        else:
            logger.debug(f"[UG{self.parent.id}] Unidade parando.")

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

        self.borda_parar = True if self.borda_parar else False

        logger.info(f"[UG{self.parent.id}] Entrando no estado restrito.")

    def step(self) -> State:
        CONDIC_INDISPONIBILIZAR = False
        condicionadores_ativos = []

        for condicionador_essencial in self.parent.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.parent.deve_ler_condicionadores = True

        if self.parent.deve_ler_condicionadores:
            for condicionador_essencial in self.parent.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade == CONDIC_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    CONDIC_INDISPONIBILIZAR = True

            for condicionador in self.parent.condicionadores:
                if condicionador.ativo and condicionador.gravidade == CONDIC_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador)
                    CONDIC_INDISPONIBILIZAR = True
            self.parent.deve_ler_condicionadores = False

        if CONDIC_INDISPONIBILIZAR:
            logger.warning(f"[UG{self.parent.id}] UG em modo disponível detectou condicionadores ativos, indisponibilizando UG.\nCondicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
            return StateIndisponivel(self.parent)

        elif self.parent.etapa_atual == UG_PARADA or self.selo:
            self.selo = True
            self.parent.fechar_comporta()
            if self.parent.etapa_comporta == CP_FECHADA:
                self.parent.acionar_trip_logico()
                self.parent.acionar_trip_eletrico()
            else:
                logger.debug("[UG{0}] A comporta {0} deve estar completamente fechada para acionar o bloqueio da UG")
        else:
            self.parent.parar()
        return self

class StateDisponivel(State):
    def __init__(self, parent: UnidadeGeracao):
        super().__init__(parent)
        self.release_sinc = True
        self.release_press = True
        self.parent.codigo_state = UG_SM_DISPONIVEL
        logger.info(f"[UG{self.parent.id}] Entrando no estado disponível.")

    def step(self) -> State:
        logger.debug(f"[UG{self.parent.id}] (tentativas_de_normalizacao atual: {self.parent.tentativas_de_normalizacao})")
        CONDIC_NORMALIZAR = False
        CONDIC_INDISPONIBILIZAR = False
        condicionadores_ativos = []
        self.parent.controle_limites_operacao()

        for condicionador_essencial in self.parent.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.parent.deve_ler_condicionadores = True

        if self.parent.deve_ler_condicionadores:
            for condicionador_essencial in self.parent.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade == CONDIC_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    CONDIC_INDISPONIBILIZAR = True
                elif condicionador_essencial.ativo and condicionador_essencial.gravidade == CONDIC_NORMALIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    CONDIC_NORMALIZAR = True

            for condicionador in self.parent.condicionadores:
                if condicionador.ativo and condicionador.gravidade == CONDIC_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador)
                    CONDIC_INDISPONIBILIZAR = True
                elif condicionador.ativo and condicionador.gravidade == CONDIC_NORMALIZAR:
                    condicionadores_ativos.append(condicionador)
                    CONDIC_NORMALIZAR = True
            self.parent.deve_ler_condicionadores = False

        if CONDIC_INDISPONIBILIZAR or CONDIC_NORMALIZAR:
            logger.info(f"[UG{self.parent.id}] UG em modo disponível detectou condicionadores ativos.\nCondicionadores ativos:")
            for d in condicionadores_ativos:
                logger.warning(f"Desc: {d.descr}; Gravidade: {CONDIC_STR_DCT[d.gravidade]}")

        if CONDIC_INDISPONIBILIZAR:
            logger.warning(f"[UG{self.parent.id}] Indisponibilizando UG.")
            return StateIndisponivel(self.parent)

        if CONDIC_NORMALIZAR:
            if (self.parent.tentativas_de_normalizacao > self.parent.limite_tentativas_de_normalizacao):
                logger.warning(f"[UG{self.parent.id}] A UG estourou as tentativas de normalização, indisponibilizando UG. \n Condicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
                return StateIndisponivel(self.parent)

            elif (self.parent.ts_auxiliar - datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)).seconds > self.parent.tempo_entre_tentativas:
                self.parent.tentativas_de_normalizacao += 1
                self.parent.ts_auxiliar = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
                logger.info(f"[UG{self.parent.id}] Normalizando UG (tentativa {self.parent.tentativas_de_normalizacao}/{self.parent.limite_tentativas_de_normalizacao}).")
                self.parent.reconhece_reset_alarmes()
                return self

            else:
                return self

        else:
            logger.debug(f"[UG{self.parent.id}] Etapa atual: {self.parent.etapa_atual}")
            atenuacao = 0
            logger.debug(f"[UG{self.parent.id}] Lendo condicionadores_atenuadores")
            for condicionador in self.parent.condicionadores_atenuadores:
                atenuacao = max(atenuacao, condicionador.valor)
                logger.debug(f"[UG{self.parent.id}] Atenuador \"{condicionador.descr}\" -> leitura: {condicionador.leitura.valor}-> atenucao: {atenuacao}")

            ganho = 1 - atenuacao
            aux = self.parent.setpoint
            if (self.parent.setpoint > self.cfg["pot_minima"]) and self.parent.setpoint * ganho > self.cfg["pot_minima"]:
                self.parent.setpoint = self.parent.setpoint * ganho

            elif self.parent.limpeza_grade:
                self.parent.setpoint = self.cfg["pot_limpeza_grade"]

            elif (self.parent.setpoint * ganho < self.cfg["pot_minima"]) and (self.parent.setpoint > self.cfg["pot_minima"]):
                self.parent.setpoint =  self.cfg["pot_minima"]

            logger.debug(f"[UG{self.parent.id}] SP {aux} * GAIN {ganho} = {self.parent.setpoint}")

            if self.parent.etapa_atual == UG_PARANDO:
                logger.debug(f"[UG{self.parent.id}] Unidade parando")
                if self.parent.leitura_potencia < 300:
                    self.parent.cp.fechar_comporta()

                elif self.parent.setpoint >= self.cfg["pot_minima"]:
                    if self.parent.cp.etapa_comporta == CP_FECHADA:
                        self.parent.cp.cracking_comporta()

                    elif self.parent.cp.etapa_comporta == CP_CRACKING:
                        if not self.parent.timer_press and self.release_press:
                            Thread(target=lambda: self.parent.cp.verificar_pressao()).start()
                            self.release_press = False
                        elif self.parent.timer_press and not self.release_press:
                            self.parent.timer_press = False
                            self.release_press = True
                            self.parent.cp.abrir_comporta()

                    elif self.parent.cp.etapa_comporta == CP_ABERTA:
                        self.parent.partir()
                        self.parent.enviar_setpoint(self.parent.setpoint)
                        if not self.parent.timer_sinc and self.release_sinc:
                            Thread(target=lambda: self.parent.verificar_partindo()).start()
                            self.release_sinc = False
                        elif self.parent.timer_sinc and not self.release_sinc:
                            self.parent.timer_sinc = False
                            self.timer_sinc = True

                    elif self.parent.cp.etapa_comporta == CP_REMOTO:
                        logger.debug("[UG{0}] Comporta {0} em modo manual")
                        pass

                    else:
                        logger.debug("[UG{0}] Comporta {0} entre etapas/etapa inconsistente")

            elif self.parent.etapa_atual == UG_SINCRONIZANDO:
                logger.debug(f"[UG{self.parent.id}] Unidade sincronizando")
                if self.parent.setpoint == 0:
                    logger.warning(f"[UG{self.parent.id}] A UG estava sincronizando com SP zerado, parando a UG.")
                    self.parent.parar()

            elif self.parent.etapa_atual == UG_PARADA:
                logger.debug(f"[UG{self.parent.id}] Unidade parada")
                if self.parent.setpoint >= self.cfg["pot_minima"]:

                    if self.parent.cp.etapa_comporta == CP_FECHADA:
                        self.parent.cp.cracking_comporta()

                    elif self.parent.cp.etapa_comporta == CP_CRACKING:
                        if not self.parent.timer_press and self.release_press:
                            Thread(target=lambda: self.parent.cp.verificar_pressao()).start()
                            self.release_press = False
                        elif self.parent.timer_press and not self.release_press:
                            self.parent.timer_press = False
                            self.release_press = True
                            self.parent.cp.abrir_comporta()

                    elif self.parent.cp.etapa_comporta == CP_ABERTA:
                        self.parent.partir()
                        self.parent.enviar_setpoint(self.parent.setpoint)
                        if not self.parent.timer_sinc and self.release_sinc:
                            Thread(target=lambda: self.parent.verificar_partindo()).start()
                            self.release_sinc = False
                        elif self.parent.timer_sinc and not self.release_sinc:
                            self.parent.timer_sinc = False
                            self.timer_sinc = True

                    elif self.parent.cp.etapa_comporta == CP_REMOTO:
                        logger.debug(f"[UG{self.parent.id}] Comporta {self.parent.id} em modo manual")
                        pass

                    else:
                        logger.debug(f"[UG{self.parent.id}] Comporta {self.parent.id} entre etapas/etapa inconsistente")

            elif self.parent.etapa_atual == UG_SINCRONIZADA:
                logger.debug(f"[UG{self.parent.id}] Unidade sincronizada")
                if not self.parent.aux_tempo_sincronizada:
                    self.parent.aux_tempo_sincronizada = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

                elif (datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None) - self.parent.aux_tempo_sincronizada).seconds >= 300:
                    self.parent.tentativas_de_normalizacao = 0

                if self.parent.setpoint == 0:
                    self.parent.parar()
                else:
                    self.parent.enviar_setpoint(self.parent.setpoint)

            elif self.parent.etapa_atual not in UG_LST_ETAPAS:
                logger.warning(f"[UG{self.parent.id}] UG em etapa inconsistente. (Etapa atual:{self.parent.etapa_atual})")

            if not self.parent.etapa_atual == UG_SINCRONIZADA:
                self.parent.aux_tempo_sincronizada = None

            return self
