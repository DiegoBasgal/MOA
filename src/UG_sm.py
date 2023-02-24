import pytz
import logging
import traceback

from time import sleep, time
from threading import Thread
from datetime import datetime
from abc import abstractmethod

from src.codes import *
from src.Leituras import *
from src.UG import UnidadeDeGeracao

# Class Stubs
class State:
    ...

class StateManual(State):
    ...

class StateIndisponivel(State):
    ...

class StateRestrito(State):
    ...

class StateDisponivel(State):
    ...

class State:
   def __init__(self, parent: UnidadeDeGeracao):
      self.parent = parent
      self.logger = logging.getLogger("__main__")

   @abstractmethod
   def step(self) -> State:
      pass

class StateManual(State):
   def __init__(self, parent: UnidadeDeGeracao):
      super().__init__(parent)
      self.parent.codigo_state = MOA_UNIDADE_MANUAL

      self.logger.info(f"[UG{self.parent.id}] Entrando no estado: \"Manual\". Para retornar a operação autônoma, favor agendar na interface web")

   def step(self) -> State:
      self.parent.setpoint = self.parent.leitura_potencia.valor
      return self

class StateIndisponivel(State):
   def __init__(self, parent: UnidadeDeGeracao):
      super().__init__(parent)
      self.parent.codigo_state = MOA_UNIDADE_INDISPONIVEL

      self.selo = False
      self.parent.__next_state = self
      self.logger.info("[UG{}] Entrando no estado: \"Indisponível\". Para retornar a operação autônoma, favor agendar na interface web")

   def step(self) -> State:
      if self.parent.etapa_atual == UNIDADE_PARADA or self.selo:
         self.selo = True
         self.parent.acionar_trip_logico()
         self.parent.acionar_trip_eletrico()
      else:
         self.parent.parar()
      return self

class StateRestrito(State):
   def __init__(self, parent: UnidadeDeGeracao):
      super().__init__(parent)
      self.parent.codigo_state = MOA_UNIDADE_RESTRITA

      self.release = False
      self.parar_timer = False
      self.deve_normalizar = False
      self.deve_indisponibilizar = False
      self.logger.info(f"[UG{self.parent.id}] Entrando no estado \"restrito\"")

   def step(self) -> State:
      condicionadores_ativos = []
      for condic in self.parent.condicionadores_essenciais:
         if condic.ativo and condic.gravidade == DEVE_INDISPONIBILIZAR:
            condicionadores_ativos.append(condic)
            self.deve_indisponibilizar = True
         elif condic.ativo and condic.gravidade == DEVE_AGUARDAR:
            condicionadores_ativos.append(condic)

      if condicionadores_ativos:
         if self.parent.norma_agendada and not self.release:
            self.logger.info(f"[UG{self.parent.id}] Normalização por tempo ativada")
            self.logger.info(f"[UG{self.parent.id}] Aguardando normalização por tempo -> Tempo definido: {self.parent.tempo_normalizar}")
            self.release = True
            Thread(target=lambda: self.espera_normalizar(self.parent.tempo_normalizar)).start()
         elif not self.release:
            self.logger.debug(f"[UG{self.parent.id}] Aguardando normalização sem tempo pré-definido")

      elif not condicionadores_ativos:
         self.logger.info(f"[UG{self.parent.id}] A UG não possui mais condicionadores ativos, normalizando e retornando para o estado disponível")
         self.parent.tentativas_de_normalizacao += 1
         self.parent.norma_agendada = False
         self.parar_timer = True
         self.release = False
         self.parent.reconhece_reset_alarmes()
         return StateDisponivel(self.parent)
      
      if self.deve_indisponibilizar:
         self.logger.warning(f"[UG{self.parent.id}] UG detectou condicionadores com gravidade alta, indisponibilizando UG.\nCondicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
         self.parent.norma_agendada = False
         self.parar_timer = True
         self.release = False
         return StateIndisponivel(self.parent)
      
      elif self.deve_normalizar:
         if (self.parent.tentativas_de_normalizacao > self.parent.limite_tentativas_de_normalizacao):
            self.logger.warning(f"[UG{self.parent.id}] A UG estourou as tentativas de normalização, indisponibilizando UG. \n Condicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
            self.parent.norma_agendada = False
            return StateIndisponivel(self.parent)
          
         elif (self.parent.ts_auxiliar - datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)).seconds > self.parent.tempo_entre_tentativas:
            self.parent.tentativas_de_normalizacao += 1
            self.logger.info(f"[UG{self.parent.id}] Normalizando UG (tentativa {self.parent.tentativas_de_normalizacao}/{self.parent.limite_tentativas_de_normalizacao})")
            self.parent.ts_auxiliar = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
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
      self.logger.debug(f"[UG{self.parent.id}] Aguardando para normalizar UG")
      while not self.parar_timer:
         sleep(max(0, tempo - time()))
         break
      self.release = False
      self.deve_normalizar = True

class StateDisponivel(State):
    def __init__(self, parent: UnidadeDeGeracao):

        super().__init__(parent)
        self.parent.codigo_state = MOA_UNIDADE_DISPONIVEL

        self.aux = 0
        self.release = False
        self.deve_ler_condicionadores = False
        self.parent.tentativas_de_normalizacao = 0
        self.logger.info("[UG{}] Entrando no estado: \"Disponível\"")

    def step(self) -> State:
        self.parent.controle_limites_operacao()
        deve_aguardar = False
        deve_normalizar = False
        deve_indisponibilizar = False
        condicionadores_ativos = []

        for condic in self.parent.condicionadores_essenciais:
            self.deve_ler_condicionadores = True if condic.ativo else False

        if self.deve_ler_condicionadores:
            for condic in self.parent.condicionadores_essenciais:
                if condic.ativo and condic.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condic)
                    deve_indisponibilizar = True
                elif condic.ativo and condic.gravidade == DEVE_AGUARDAR:
                    condicionadores_ativos.append(condic)
                    deve_aguardar = True
                elif condic.ativo and condic.gravidade == DEVE_NORMALIZAR:
                    condicionadores_ativos.append(condic)
                    deve_normalizar = True
            self.deve_ler_condicionadores = False

        if deve_indisponibilizar or deve_normalizar or deve_aguardar:
            self.logger.info(f"[UG{self.parent.id}] UG em modo disponível detectou condicionadores ativos.\nCondicionadores ativos:")
            for d in condicionadores_ativos:
                self.logger.warning(f"Desc: {d.descr}; Ativo: {d.ativo}; Valor: {d.valor}; Gravidade: {d.gravidade}")

        if deve_indisponibilizar:
            self.logger.warning(f"[UG{self.parent.id}] Indisponibilizando UG.")
            return StateIndisponivel(self.parent)

        if deve_aguardar:
            self.logger.warning(f"[UG{self.parent.id}] Entrando no estado Restrito até normalização da condição.")
            return StateRestrito(self.parent)

        if deve_normalizar:
            if (self.parent.tentativas_de_normalizacao > self.parent.limite_tentativas_de_normalizacao):
                self.logger.warning(f"[UG{self.parent.id}] A UG estourou as tentativas de normalização, indisponibilizando UG. \n Condicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
                return StateIndisponivel(self.parent)

            elif (self.parent.ts_auxiliar - datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)).seconds > self.parent.tempo_entre_tentativas:
                self.parent.tentativas_de_normalizacao += 1
                self.parent.ts_auxiliar = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
                self.logger.info(f"[UG{self.parent.id}] Normalizando UG (tentativa {self.parent.tentativas_de_normalizacao}/{self.parent.limite_tentativas_de_normalizacao})")
                self.parent.reconhece_reset_alarmes()
                return self
            
            else:
                return self

        else:
            self.logger.debug(f"[UG{self.parent.id}] Etapa atual: \"{self.parent.etapa_atual}\" / Etapa alvo: \"{self.parent.etapa_alvo}\"")

            if self.release == True and self.aux == 1:
                self.release = False
                self.aux = 0

            atenuacao = 0
            self.logger.debug(f"[UG{self.parent.id}] Lendo condicionadores_atenuadores")

            for condicionador in self.parent.condicionadores_atenuadores:
                atenuacao = max(atenuacao, condicionador.valor)
                self.logger.debug(f"[UG{self.parent_ug.id}] Atenuador \"{condicionador.descr}\" -> Atenuação: {atenuacao} / Leitura: {condicionador.leitura.valor}")

            ganho = 1 - atenuacao
            aux = self.parent.setpoint
            if (self.parent.setpoint > self.parent.setpoint_minimo) and self.parent.setpoint * ganho > self.parent.setpoint_minimo:
                self.parent.setpoint = self.parent.setpoint * ganho

            elif self.parent.limpeza_grade:
                self.parent.setpoint_minimo = self.parent.cfg["pot_limpeza_grade"]
                self.parent.setpoint = self.parent.setpoint_minimo

            elif (self.parent.setpoint * ganho < self.parent.setpoint_minimo) and (self.parent.setpoint > self.parent.setpoint_minimo):
                self.parent.setpoint =  self.parent.setpoint_minimo

            self.logger.debug(f"[UG{self.parent.id}] SP {aux} * GANHO {ganho} = {self.parent.setpoint}")

            # PARANDO
            if self.parent.etapa_alvo == UNIDADE_PARADA and not self.parent.etapa_atual == UNIDADE_PARADA:
                if self.parent.setpoint >= self.parent.setpoint_minimo:
                    self.parent.enviar_setpoint(self.parent.setpoint)

            # SINCRONIZANDO
            elif self.parent.etapa_alvo == UNIDADE_SINCRONIZADA and not self.parent.etapa_atual == UNIDADE_SINCRONIZADA:
                if self.release == False and self.aux == 0:
                    Thread(target=lambda: self.verificar_partindo()).start()
                    self.aux = 1
                if self.parent.setpoint == 0:
                    self.logger.warning(f"[UG{self.parent.id}] A UG estava sincronizando com SP zerado, parando a UG.")
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
                    self.parent.aux_tempo_sincronizada = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

                elif (datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None) - self.parent.aux_tempo_sincronizada).seconds >= 300:
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
        timer = time() + 600
        try:
            self.logger.debug(f"[UG{self.parent.id}] Iniciando o timer de verificação de partida")
            while time() < timer:
                if self.parent.etapa_atual == UNIDADE_SINCRONIZADA:
                    self.logger.debug("[UG{}] Unidade sincronizada. Saindo do timer de verificação de partida".format(self.parent.id))
                    self.release = True
                    return True
            self.logger.debug(f"[UG{self.parent.id}] A Unidade estourou o timer de verificação de partida, adicionando condição para normalizar")
            self.parent.clp_sa.write_single_coil([f"REG_UG{self.parent.id}_ComandosDigitais_MXW_EmergenciaViaSuper"], [1]) 
            self.release = True
        except Exception:
            self.logger.error(f"[UG{self.parent.id}] Erro na execução do timer de verificação de partida.\nException: {traceback.print_stack}")
        return False