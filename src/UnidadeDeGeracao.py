"""
Unidade de geração.

Esse módulo corresponde a implementação das unidades de geração e
da máquina de estado que rege a mesma.
"""
__version__ = "0.1"
__author__ = "Lucas Lavratti"

import pytz
import logging
import traceback

from src.codes import *
from src.Leituras import *
from time import sleep, time
from threading import Thread
from datetime import datetime
from abc import abstractmethod
from src.Condicionadores import *

# Class Stubs
class UnidadeDeGeracao:
    ...


class State:
    ...


class StateDisponivel(State):
    ...


class StateIndisponivel(State):
    ...


class StateManual(State):
    ...


class StateRestrito(State):
    ...


class UnidadeDeGeracao:
    """
    Unidade de geração.
    Esse módulo corresponde a implementação das unidades de geração.
    """

    def __init__(self, id: int):
        """
        Args:
            id (int): [description]
        """
        self.logger = logging.getLogger("__main__")

        # Variavéis internas (não são lidas nem escritas diretamente)
        self.__id = id
        self.__prioridade = 0
        self.__etapa_atual = 0
        self.__tempo_entre_tentativas = 0
        self.__limite_tentativas_de_normalizacao = 3
        self.__setpoint = 0
        self.__setpoint_minimo = 0
        self.__setpoint_maximo = 0
        self.__tentativas_de_normalizacao = 0
        self.ts_auxiliar = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        self.__next_state = StateDisponivel(self)
        # Condicionadores devem ser adcionados após o init
        self.__condicionadores_essenciais = []
        self.__condicionadores = []
        self.__condicionadores_atenuadores = []
        self.aux_tempo_sincronizada = None
        self.deve_ler_condicionadores = False
        self.codigo_state = self.__codigo_state

    def debug_set_etapa_atual(self, var):
        self.__etapa_atual = var

    def modbus_update_state_register(self):
        raise NotImplementedError

    def carregar_parametros(self, parametros: dict):
        """
        Carrega os parametros/vars iniciais.

        Args:
            parametros (dict): Os parametros a serem carregados
        """

        for key, val in parametros.items():
            while not key[0:1] == "__":
                key = "_" + key[:]
            setattr(self, key, val)
            self.logger.debug(
                "[UG{}] Variavél carregada: {} = {}.".format(self.id, key, val)
            )

    def interstep(self) -> None:
        raise NotImplementedError
    
    def leituras_por_hora(self) -> None:
        raise NotImplementedError
        
    def step(self) -> None:
        """
        Função que rege a máquina de estados.

        Raises:
            e: Exceptions geradas ao executar um estado
        """
        try:
            self.logger.debug("[UG{}] Step.".format(self.id))
            self.interstep()
            self.__next_state = self.__next_state.step()
            self.modbus_update_state_register()

        except Exception as e:
            self.logger.error(
                "[UG{}] Erro na execução da sm. Traceback: {}".format(
                    self.id, traceback.format_exc()
                )
            )
            raise e

    def forcar_estado_disponivel(self) -> bool:
        """
        Força a máquina de estados a entrar no estado disponível na proxima execução

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.reconhece_reset_alarmes()
            sleep(1)
            self.__next_state = StateDisponivel(self)
        except Exception as e:
            self.logger.error(
                "[UG{}] {} Não foi possivel forcar_estado_disponivel. {}".format(
                    self.id, traceback.print_stack
                )
            )
            return False
        else:
            return True

    def forcar_estado_indisponivel(self) -> bool:
        """
        Força a máquina de estados a entrar no estado indisponível na proxima execução

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.__next_state = StateIndisponivel(self)
        except Exception as e:
            self.logger.error(
                "[UG{}] {} Não foi possivel forcar_estado_indisponivel. {}".format(
                    self.id, traceback.print_stack
                )
            )
            return False
        else:
            return True

    def forcar_estado_manual(self) -> bool:
        """
        Força a máquina de estados a entrar no estado manual na proxima execução

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.__next_state = StateManual(self)
        except Exception as e:
            self.logger.error(
                "[UG{}] {} Não foi possivel forcar_estado_manual. {}".format(
                    self.id, traceback.print_stack
                )
            )
            return False
        else:
            return True

    def forcar_estado_restrito(self) -> bool:
        """
        Força a máquina de estados a entrar no estado restrito na proxima execução

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.__next_state = StateRestrito(self)
        except Exception as e:
            self.logger.error(
                "[UG{}] {} Não foi possivel forcar_estado_restrito. {}".format(
                    self.id, traceback.print_stack
                )
            )
            return False
        else:
            return True

    @property
    def id(self) -> int:
        """
        Id da unidade de deração

        Returns:
            int: id
        """
        return self.__id

    @property
    def prioridade(self) -> int:
        """
        Prioridade da unidade de deração

        Returns:
            int: id
        """
        return self.__prioridade

    @prioridade.setter
    def prioridade(self, var) -> None:
        self.__prioridade = var

    @property
    def condicionadores_essenciais(self) -> list([CondicionadorBase]):
        """
        Lista de condicionadores (objetos) essenciais que deverão ser lidos SEMPRE

        Returns:
            list: lista de condicionadores (objetos)
        """
        return self.__condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: list([CondicionadorBase])):
        self.__condicionadores_essenciais = var

    @property
    def condicionadores(self) -> list([CondicionadorBase]):
        """
        Lista de condicionadores (objetos) que deverão ser lidaos no caso de uma chamada

        Returns:
            list: lista de condicionadores (objetos)
        """
        return self.__condicionadores

    @condicionadores.setter
    def condicionadores(self, var: list([CondicionadorBase])):
        self.__condicionadores = var

    @property
    def condicionadores_atenuadores(self) -> list([CondicionadorBase]):
        """
        Lista de condicionadores_atenuadores (objetos) relacionados com a unidade de geração

        Returns:
            list: lista de condicionadores_atenuadores (objetos)
        """
        return self.__condicionadores_atenuadores

    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: list([CondicionadorBase])):
        self.__condicionadores_atenuadores = var

    @property
    def etapa_atual(self) -> int:
        """
        Etapa atual, esta chamada deve recuperar a informação diratamente da unidade de geração por meio dos drivers de comunicação

        Verifique a lista UNIDADE_LISTA_DE_ETAPAS para as constantes retornadas por esta chamda.
        Returns:
            int: ETAPA_ATUAL
        """
        self.logger.debug(
            "[UG{}] etapa_atual = __etapa_atual <- {}".format(
                self.id, self.__etapa_atual
            )
        )
        return self.__etapa_atual

    @property
    def tempo_entre_tentativas(self) -> int:
        """
        Limite mínimo de tempo entre tentaivas de normalização da unidade de geração
        Este valor deve ser carregado com o restante dos parâmetros da unidade de geração utilizando a função carregar_parametros()
        Valor recomendado: 30 segundos

        Returns:
            int: tempo_entre_tentativas [s]
        """
        return self.__tempo_entre_tentativas

    @property
    def limite_tentativas_de_normalizacao(self) -> int:
        """
        Limite máximo do número de tentativas de normalização da unidade de geração
        Este valor deve ser carregado com o restante dos parâmetros da unidade de geração utilizando a função carregar_parametros()
        Valor recomendado: 3 tentativas

        Returns:
            int: limite_tentativas_de_normalizacao
        """
        return self.__limite_tentativas_de_normalizacao

    @property
    def setpoint(self) -> int:
        """
        Setpoint da unidade de geração

        Quando escrito:
            Caso o setpoint estiver abixo do limte, ele retornará 0 kW.
            Caso o setpoint estiver acima do limte, ele retornará o limite.

        Returns:
            int: setpoint [kW]
        """
        return self.__setpoint

    @setpoint.setter
    def setpoint(self, var: int):
        if var < self.setpoint_minimo:
            self.__setpoint = 0
        elif var > self.setpoint_maximo:
            self.__setpoint = self.setpoint_maximo
        else:
            self.__setpoint = int(var)
        self.logger.debug("[UG{}] SP<-{}".format(self.id, var))

    @property
    def setpoint_minimo(self) -> int:
        """
        Setpoint mínimo da unidade de geração
        Este valor deve ser carregado com o restante dos parâmetros da unidade de geração utilizando a função carregar_parametros()

        Returns:
            int: setpoint_minimo [kW]
        """
        return self.__setpoint_minimo

    @setpoint_minimo.setter
    def setpoint_minimo(self, var: int):
        self.__setpoint_minimo = var

    @property
    def setpoint_maximo(self) -> int:
        """
        Setpoint máximo da unidade de geração
        Este valor deve ser carregado com o restante dos parâmetros da unidade de geração utilizando a função carregar_parametros()

        Returns:
            int: setpoint_maximo [kW]
        """
        return self.__setpoint_maximo

    @setpoint_maximo.setter
    def setpoint_maximo(self, var: int):
        self.__setpoint_maximo = var

    @property
    def tentativas_de_normalizacao(self) -> int:
        """
        Contador de tentativas de normalização realizadas

        Returns:
            int: tentativas_de_normalizacao ( sempre >= 0 )
        """
        return self.__tentativas_de_normalizacao

    @tentativas_de_normalizacao.setter
    def tentativas_de_normalizacao(self, var: int):
        if 0 <= var and var == int(var):
            self.__tentativas_de_normalizacao = int(var)
        else:
            raise ValueError("Valor deve se um inteiro positivo")

    @property
    def disponivel(self) -> bool:
        """
        Retrofit
        """
        return isinstance(self.__next_state, StateDisponivel)

    @property
    def codigo_state(self) -> int:
        return self.__codigo_state

    @codigo_state.setter
    def codigo_state(self, var) -> int:
        self.__codigo_state = var

    def partir(self) -> bool:
        """
        Envia o comando de parida da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.info(
                "[UG{}] Enviando comando de partida.".format(self.id)
            )
            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return True

    def parar(self) -> bool:
        """
        Envia o comando de parada da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.info("[UG{}] Enviando comando de parada.".format(self.id))

            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return True

    def reconhece_reset_alarmes(self) -> bool:
        """
        Envia o comando de reconhece e reset dos alarmes da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.info(
                "[UG{}] Enviando comando de reconhecer e resetar alarmes.".format(self.id)
            )
            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return True

    def enviar_setpoint(self, setpoint_kw: int) -> bool:
        """
        Envia o setpoint desejado para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.debug(
                "[UG{}] Enviando setpoint {}kW.".format(self.id, setpoint_kw)
            )
            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return True


class State:
    """
    Classe implementa a base para estados. É "Abstrata" assim por se dizer...
    """

    def __init__(self, parent_ug: UnidadeDeGeracao):
        self.parent_ug = parent_ug
        self.logger = logging.getLogger("__main__")

    @abstractmethod
    def step(self) -> State:
        pass


class StateManual(State):
    """
    Implementação do estado StateManual

    Neste estado a máquina deve estar comletamente sobre controle do operador.
    O estado só será alterado utilizando as funções que forçam o estado.
    """

    def __init__(self, parent_ug: UnidadeDeGeracao):
        super().__init__(parent_ug)
        self.parent_ug.codigo_state = MOA_UNIDADE_MANUAL

        self.logger.info("[UG{}] Entrando no estado manual. Para retornar a operação autônoma da UG é necessário intervenção manual via interface web.".format(self.parent_ug.id))

    def step(self) -> State:
        self.parent_ug.setpoint = self.parent_ug.leitura_potencia.valor
        self.parent_ug.codigo_state = MOA_UNIDADE_MANUAL
        return self


class StateIndisponivel(State):
    """
    Implementação do estado StateIndisponivel

    Neste estado a máquina deve estar indisponibilizada, acionando os trips lógicos e elétricos da unidade de geração.
    O estado só será alterado utilizando as funções que forçam o estado.
    """

    def __init__(self, parent_ug: UnidadeDeGeracao):

        super().__init__(parent_ug)
        self.parent_ug.codigo_state = MOA_UNIDADE_INDISPONIVEL

        self.selo = False
        self.logger.warning("[UG{}] Entrando no estado indisponível. Para retornar a operação autônoma da UG é necessário intervenção manual via interface web.".format(self.parent_ug.id))
        self.parent_ug.__next_state = self

    def step(self) -> State:
        self.parent_ug.codigo_state = MOA_UNIDADE_INDISPONIVEL
        # Se as unidades estiverem paradas, ou o selo estiver ativo
        self.logger.debug(
            "[UG{}] self.parent_ug.etapa_atual -> {}".format(
                self.parent_ug.id, self.parent_ug.etapa_atual
            )
        )
        if self.parent_ug.etapa_atual == UNIDADE_PARADA or self.selo:
            # Ativar o selo interno do moa
            self.selo = True
            # Travar a unidade por sinal de TRIP
            self.parent_ug.acionar_trip_logico()
            self.parent_ug.acionar_trip_eletrico()
        else:
            # Caso contrário, deve parar a unidade
            self.parent_ug.parar()
        return self

class StateRestrito(State):
    """
    Implementação do estado StateRestrito

    Neste estado a máquina deve estar restrita para operação.
    A ug estará com trips acionados para garantir que a máquina permanecerá parada
    O estado pode ser alterado atumoaticamente.
    O perador não tem controle sobre a UG.
    """

    def __init__(self, parent_ug: UnidadeDeGeracao):

        super().__init__(parent_ug)
        self.parent_ug.codigo_state = MOA_UNIDADE_RESTRITA
        self.logger.info("[UG{}] Entrando no estado restrito.".format(self.parent_ug.id))

    def step(self) -> State:
        self.parent_ug.codigo_state = MOA_UNIDADE_RESTRITA
        # Ler condiconadores

        # Devemos estudar quais os condicionadores que serão lidos no modo restrito para poder re-colocar a leitura de condicionadores abaixo.
        
        deve_indisponibilizar = False
        deve_normalizar = False
        condicionadores_ativos = []

        if self.parent_ug.deve_ler_condicionadores:
            for condicionador_essencial in self.parent_ug.condicionadores_essenciais:
                if condicionador_essencial.ativo:
                    if condicionador_essencial >= DEVE_INDISPONIBILIZAR:
                        condicionadores_ativos.append(condicionador_essencial)
                        deve_indisponibilizar = True
                    elif condicionador_essencial.gravidade>=DEVE_NORMALIZAR:
                        condicionadores_ativos.append(condicionador_essencial)
                        self.parent_ug.deve_ler_condicionadores = False
                        deve_normalizar = True

            for condicionador in self.parent_ug.condicionadores:
                if condicionador.ativo: 
                    if condicionador.gravidade>=DEVE_INDISPONIBILIZAR:
                        condicionadores_ativos.append(condicionador)
                        deve_indisponibilizar = True
                    elif condicionador.gravidade>=DEVE_NORMALIZAR:
                        condicionadores_ativos.append(condicionador)
                        self.parent_ug.deve_ler_condicionadores = False
                        deve_normalizar = True

        # Se algum condicionador deve gerar uma indisponibilidade
        if deve_indisponibilizar:
            # Logar os condicionadores ativos
            self.logger.warning("[UG{}] UG em modo disponível detectou condicionadores ativos, indisponibilizando UG.\nCondicionadores ativos:\n{}".format(self.parent_ug.id, [d.descr for d in condicionadores_ativos]))
            # Vai para o estado StateIndisponivel
            return StateIndisponivel(self.parent_ug)

        # Se a unidade estiver parada, travar a mesma por sinal de TRIP
        if self.parent_ug.etapa_atual == UNIDADE_PARADA:
            self.parent_ug.acionar_trip_logico()
            self.parent_ug.acionar_trip_eletrico()
        # Caso contrário, deve parar a unidade
        else:
            self.parent_ug.parar()
        return self


class StateDisponivel(State):
    """
    Implementação do estado StateDisponivel

    Neste estado a máquina deve estar disponivel para operação.
    O estado pode ser alterado atumoaticamente.
    O perador não tem controle sobre a UG.
    """

    def __init__(self, parent_ug: UnidadeDeGeracao):

        super().__init__(parent_ug)
        self.aux = 0
        self.release = False
        self.parent_ug.codigo_state = MOA_UNIDADE_DISPONIVEL
        self.logger.info("[UG{}] Entrando no estado disponível.".format(self.parent_ug.id))

    def step(self) -> State:
        self.parent_ug.codigo_state = MOA_UNIDADE_DISPONIVEL

        self.logger.debug("[UG{}] (tentativas_de_normalizacao atual: {})".format(self.parent_ug.id, self.parent_ug.tentativas_de_normalizacao))

        # Ler condiconadores, verifica e armazena os ativos
        deve_indisponibilizar = False
        deve_normalizar = False
        condicionadores_ativos = []
        
        self.parent_ug.controle_limites_operacao()

        for condicionador_essencial in self.parent_ug.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.parent_ug.deve_ler_condicionadores = True

        if self.parent_ug.deve_ler_condicionadores:
            for condicionador_essencial in self.parent_ug.condicionadores_essenciais:
                if condicionador_essencial.ativo:
                    if condicionador_essencial.gravidade >= DEVE_INDISPONIBILIZAR:
                        condicionadores_ativos.append(condicionador_essencial)
                        deve_indisponibilizar = True
                    elif condicionador_essencial.gravidade>=DEVE_NORMALIZAR:
                        condicionadores_ativos.append(condicionador_essencial)
                        self.parent_ug.deve_ler_condicionadores = False
                        deve_normalizar = True

            for condicionador in self.parent_ug.condicionadores:
                if condicionador.ativo: 
                    if condicionador.gravidade>=DEVE_INDISPONIBILIZAR:
                        condicionadores_ativos.append(condicionador)
                        deve_indisponibilizar = True
                    elif condicionador.gravidade>=DEVE_NORMALIZAR:
                        condicionadores_ativos.append(condicionador)
                        self.parent_ug.deve_ler_condicionadores = False
                        deve_normalizar = True

        # Logar os condicionadores ativos
        if deve_indisponibilizar or deve_normalizar:
            self.logger.info("[UG{}] UG em modo disponível detectou condicionadores ativos.\nCondicionadores ativos:".format(self.parent_ug.id))
            for d in condicionadores_ativos:
                self.logger.warning("Desc: {}; Ativo: {}; Valor: {}; Gravidade: {}".format(d.descr, d.ativo, d.valor, d.gravidade))

        # Se algum condicionador deve gerar uma indisponibilidade
        if deve_indisponibilizar:
            self.logger.warning("[UG{}] Indisponibilizando UG.".format(self.parent_ug.id))
            # Vai para o estado StateIndisponivel
            return StateIndisponivel(self.parent_ug)

        # Se algum condicionador deve gerar uma tentativa de normalizacao
        if deve_normalizar:
            # Se estourou as tentativas de normalização, vai para o estado StateIndisponivel
            if (self.parent_ug.tentativas_de_normalizacao > self.parent_ug.limite_tentativas_de_normalizacao):
                # Logar o ocorrido
                self.logger.warning("[UG{}] A UG estourou as tentativas de normalização, indisponibilizando UG. \n Condicionadores ativos:\n{}".format(self.parent_ug.id,[d.descr for d in condicionadores_ativos],))
                # Vai para o estado StateIndisponivel
                return StateIndisponivel(self.parent_ug)

            # Se não estourou as tentativas de normalização, e já se passou tempo suficiente, deve tentar normalizar
            elif (self.parent_ug.ts_auxiliar - datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)).seconds > self.parent_ug.tempo_entre_tentativas:
                # Adciona o contador
                self.parent_ug.tentativas_de_normalizacao += 1
                # Atualiza o timestamp
                self.parent_ug.ts_auxiliar = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
                # Logar o ocorrido
                self.logger.info("[UG{}] Normalizando UG (tentativa {}/{}).".format(self.parent_ug.id,self.parent_ug.tentativas_de_normalizacao,self.parent_ug.limite_tentativas_de_normalizacao,))
                # Reconhece e reset
                self.parent_ug.reconhece_reset_alarmes()
                return self

            # Caso contrário (se ainda não deu o tempo), não faz nada
            else:
                return self

        # Se não detectou nenhum condicionador ativo:
        else:

            self.logger.debug("[UG{}] Etapa atual: '{}', etapa_alvo: '{}'".format(self.parent_ug.id, self.parent_ug.etapa_atual, self.parent_ug.etapa_alvo))

            if self.release == True and self.aux == 1:
                self.release = False
                self.aux = 0

            # Calcula a atenuação devido aos condicionadores antes de prosseguir
            atenuacao = 0
            # Para cada condicionador
            self.logger.debug(f"[UG{self.parent_ug.id}] Lendo condicionadores_atenuadores")
            for condicionador in self.parent_ug.condicionadores_atenuadores:
                atenuacao = max(atenuacao, condicionador.valor)
                self.logger.debug(f"[UG{self.parent_ug.id}] Atenuador \"{condicionador.descr}\" -> leitura: {condicionador.leitura.valor}-> atenucao: {atenuacao}")

            # A atenuação já vem normalizada de 0 a 1, portanto
            # para ter o ganho é necessário apenas subtrair a atenuação
            ganho = 1 - atenuacao
            aux = self.parent_ug.setpoint
            if (self.parent_ug.setpoint > self.parent_ug.setpoint_minimo) and self.parent_ug.setpoint * ganho > self.parent_ug.setpoint_minimo:
                self.parent_ug.setpoint = self.parent_ug.setpoint * ganho

            elif self.parent_ug.limpeza_grade:
                self.parent_ug.setpoint_minimo = self.parent_ug.cfg["pot_limpeza_grade"]
                self.parent_ug.setpoint = self.parent_ug.setpoint_minimo

            elif (self.parent_ug.setpoint * ganho < self.parent_ug.setpoint_minimo) and (self.parent_ug.setpoint > self.parent_ug.setpoint_minimo):
                self.parent_ug.setpoint =  self.parent_ug.setpoint_minimo

            self.logger.debug(
                "[UG{}] SP {} * GAIN {} = {}".format(
                    self.parent_ug.id,
                    aux,
                    ganho,
                    self.parent_ug.setpoint,
                )
            )
            # O comportamento da UG conforme a etapa em que a mesma se encontra

            if self.parent_ug.etapa_alvo == UNIDADE_PARADA and not self.parent_ug.etapa_atual == UNIDADE_PARADA:
                # Unidade parando
                self.logger.debug("[UG{}] Unidade parando".format(self.parent_ug.id))
                # Se o setpoit for acima do mínimo
                if self.parent_ug.setpoint >= self.parent_ug.setpoint_minimo:
                    # Deve partir a UG
                    self.parent_ug.partir()
                    # E em seguida mandar o setpoint novo (boa prática)
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif self.parent_ug.etapa_alvo == UNIDADE_SINCRONIZADA and not self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                # Unidade sincronizando
                self.logger.debug("[UG{}] Unidade sincronizando".format(self.parent_ug.id))
                if self.release == False and self.aux == 0:
                    Thread(target=lambda: self.verificar_partindo()).start()
                    self.aux = 1
                # Se potência = 0, impedir,
                if self.parent_ug.setpoint == 0:
                    self.logger.warning("[UG{}] A UG estava sincronizando com SP zerado, parando a UG.".format(self.parent_ug.id))
                    self.parent_ug.parar()
                else:
                    self.parent_ug.partir()
                # Se não fazer nada

            elif self.parent_ug.etapa_atual == UNIDADE_PARADA:
                # Unidade parada
                self.logger.debug("[UG{}] Unidade parada".format(self.parent_ug.id))
                # Se o setpoit for acima do mínimo
                if self.parent_ug.setpoint >= self.parent_ug.setpoint_minimo:
                    # Deve partir a UG
                    self.parent_ug.partir()
                    # E em seguida mandar o setpoint novo (boa prática)
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                # Unidade sincronizada
                self.logger.debug("[UG{}] Unidade sincronizada".format(self.parent_ug.id))

                # Unidade sincronizada significa que ela está normalizada, logo zera o contador de tentativas
                if not self.parent_ug.aux_tempo_sincronizada:
                    self.parent_ug.aux_tempo_sincronizada = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

                elif (datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None) - self.parent_ug.aux_tempo_sincronizada).seconds >= 300:
                    self.parent_ug.tentativas_de_normalizacao = 0
                # Se o setpoit estiver abaixo do mínimo
                if self.parent_ug.setpoint == 0:
                    # Deve manter a UG
                    self.parent_ug.parar()
                else:
                    # Caso contrário, mandar o setpoint novo
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif self.parent_ug.etapa_atual not in UNIDADE_LISTA_DE_ETAPAS:
                # Etapa inconsistente
                # Logar o ocorrido
                self.logger.warning("[UG{}] UG em etapa inconsistente. (etapa_atual:{})".format(self.parent_ug.id,self.parent_ug.etapa_atual,))

                # Vai para o estado StateIndisponivel
                # return StateIndisponivel(self.parent_ug)

            if not self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                self.parent_ug.aux_tempo_sincronizada = None

            return self
    
    def verificar_partindo(self) -> bool:
        timer = time() + 600
        try:
            self.logger.debug("Iniciando o timer de verificação de partida")
            while time() < timer:
                if self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                    self.logger.debug("[UG{}] Unidade sincronizada. Saindo do timer de verificação de partida".format(self.parent_ug.id))
                    self.release = True
                    return True
            self.logger.debug("[UG{}] A Unidade estourou o timer de verificação de partida, adicionando condição para normalizar".format(self.parent_ug.id))
            self.parent_ug.clp.write_single_coil(REG_UG1_ComandosDigitais_MXW_EmergenciaViaSuper, [1 if self.parent_ug.id==1 else 0]) 
            self.parent_ug.clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_EmergenciaViaSuper, [1 if self.parent_ug.id==2 else 0])
            self.release = True

        except Exception as e:
            raise e

        return False
