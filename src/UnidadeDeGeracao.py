"""
Unidade de geração.

Esse módulo corresponde a implementação das unidades de geração e
da máquina de estado que rege a mesma.
"""
__version__ = "0.1"
__author__ = "Lucas Lavratti"

import inspect
import logging
import traceback

from src.field_connector import FieldConnector
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
        self.__etapa_alvo = 0
        self.__etapa_atual = 0
        self.__tempo_entre_tentativas = 0
        self.__limite_tentativas_de_normalizacao = 3
        self.__setpoint = 0
        self.__setpoint_minimo = 0
        self.__setpoint_maximo = 0
        self.__tentativas_de_normalizacao = 0
        self.ts_auxiliar = datetime.now()
        self.__next_state = StateDisponivel(self)
        # Condicionadores devem ser adcionados após o init
        self.__condicionadores = []
        self.aux_tempo_sincronizada = None
        self.codigo_state = MOA_UNIDADE_RESTRITA

    def debug_set_etapa_alvo(self, var):
        self.__etapa_alvo = var

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
            self.logger.debug(f"[UG{self.id}] Variavél carregada: {key} = {val}.")

    def step(self) -> None:
        """
        Função que rege a máquina de estados.

        Raises:
            e: Exceptions geradas ao executar um estado
        """
        try:
            self.logger.debug(f"[UG{self.id}] Step.")
            self.__next_state = self.__next_state.step()
            self.modbus_update_state_register()

        except Exception as e:
            self.logger.error(f"[UG{self.id}] Erro na execução da sm. Traceback: {traceback.format_exc()}")
            raise e

    def forcar_estado_disponivel(self) -> bool:
        """
        Força a máquina de estados a entrar no estado disponível na proxima execução

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            caller = inspect.getframeinfo(inspect.stack()[1][0])
            self.logger.debug(f"[UG{self.id}] Executando comando de forçar estado -> DISPONÍVEL. {caller.filename}:{caller.function}:{caller.lineno}")
            self.reconhece_reset_alarmes()
            sleep(1)
            self.__next_state = StateDisponivel(self)
            return True
        except Exception as e:
            self.logger.error(f"[UG{self.id}] Não foi possivel exectuar comando de forçar estado -> DISPONÍVEL. {traceback.print_stack}")
            return False

    def forcar_estado_indisponivel(self) -> bool:
        """
        Força a máquina de estados a entrar no estado indisponível na proxima execução

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            caller = inspect.getframeinfo(inspect.stack()[1][0])
            self.logger.debug(f"[UG{self.id}] Executando comando de forçar estado -> INDISPONÍVEL. {caller.filename}:{caller.function}:{caller.lineno}")
            self.__next_state = StateIndisponivel(self)
            self.step()
            return True
        except Exception as e:
            self.logger.error(f"[UG{self.id}] Não foi possivel executar comando de forçar estado -> INDISPONÍVEL. {traceback.print_stack}")
            return False

    def forcar_estado_manual(self) -> bool:
        """
        Força a máquina de estados a entrar no estado manual na proxima execução

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            caller = inspect.getframeinfo(inspect.stack()[1][0])
            self.logger.debug(f"[UG{self.id}] Executando comando de forçar estado -> MANUAL. {caller.filename}:{caller.function}:{caller.lineno}")
            self.__next_state = StateManual(self)
            return True
        except Exception as e:
            self.logger.error(f"[UG{self.id}] Não foi possivel executar comando de forçar estado -> MANUAL. {traceback.print_stack}")
            return False

    def forcar_estado_restrito(self) -> bool:
        """
        Força a máquina de estados a entrar no estado restrito na proxima execução

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            caller = inspect.getframeinfo(inspect.stack()[1][0])
            self.logger.debug(f"[UG{self.id}] Executando comando de forçar estado -> RESTRITO. {caller.filename}:{caller.function}:{caller.lineno}")
            self.__next_state = StateRestrito(self)
            return True
        except Exception as e:
            self.logger.error(f"[UG{self.id}] Não foi possivel executar comando de forçar estado -> RESTRITO. {traceback.print_stack}")
            return False

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
    def condicionadores(self) -> list([CondicionadorBase]):
        """
        Lista de condicionadores (objetos) relacionados com a unidade de geração

        Returns:
            list: lista de condicionadores (objetos)
        """
        return self.__condicionadores

    @condicionadores.setter
    def condicionadores(self, var: list([CondicionadorBase])):
        self.__condicionadores = var

    @property
    def etapa_alvo(self) -> int:
        """
        Etapa alvo, esta chamada deve recuperar a informação diratamente da unidade de geração por meio dos drivers de comunicação

        Verifique a lista UNIDADE_LISTA_DE_ETAPAS para as constantes retornadas por esta chamda.
        Returns:
            int: ETAPA_ALVO
        """
        return self.__etapa_alvo

    @property
    def etapa_atual(self) -> int:
        """
        Etapa atual, esta chamada deve recuperar a informação diratamente da unidade de geração por meio dos drivers de comunicação

        Verifique a lista UNIDADE_LISTA_DE_ETAPAS para as constantes retornadas por esta chamda.
        Returns:
            int: ETAPA_ATUAL
        """
        self.logger.debug(f"[UG{self.id}] etapa_atual = __etapa_atual <- {self.__etapa_atual}")
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
        self.logger.debug(f"[UG{self.id}] SP<-{var}")


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

    def acionar_trip_logico(self) -> bool:
        """
        Envia o comando de acionamento do TRIP para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.info(f"[UG{self.id}] Acionando sinal TRIP -> Lógico.")
            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False

    def remover_trip_logico(self) -> bool:
        """
        Envia o comando de remoção do TRIP para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.info(f"[UG{self.id}] Removendo sinal de TRIP -> Lógico.")
            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False

    def acionar_trip_eletrico(self) -> bool:
        """
        Aciona o TRIP elétricamente via painel

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.info(f"[UG{self.id}] Acionando sinal de TRIP -> Elétrico.")
            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False

    def remover_trip_eletrico(self) -> bool:
        """
        Remove o TRIP elétricamente via painel

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.info(f"[UG{self.id}] Removendo sinal de TRIP -> Elétrico.")
            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False

    def partir(self) -> bool:
        """
        Envia o comando de parida da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.info(
                f"[UG{self.id}] Enviando comando de partida."
            )
            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False

    def parar(self) -> bool:
        """
        Envia o comando de parada da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.info(f"[UG{self.id}] Enviando comando de parada.")
            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False

    def reconhece_reset_alarmes(self) -> bool:
        """
        Envia o comando de reconhece e reset dos alarmes da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.info(f"[UG{self.id}] Enviando comando de reconhece e reset alarmes.")
            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False

    def enviar_setpoint(self, setpoint_kw: int) -> bool:
        """
        Envia o setpoint desejado para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.debug(f"[UG{self.id}] Enviando setpoint {setpoint_kw}kW.")
            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False


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
        self.codigo_state = MOA_UNIDADE_MANUAL

        self.logger.warning(f"[UG{self.parent_ug.id}] Entrando no estado manual. Para retornar a operação autônoma da UG é necessário intervenção manual via interface web.")

    def step(self) -> State:
        self.codigo_state = MOA_UNIDADE_MANUAL
        return self


class StateIndisponivel(State):
    """
    Implementação do estado StateIndisponivel

    Neste estado a máquina deve estar indisponibilizada, acionando os trips lógicos e elétricos da unidade de geração.
    O estado só será alterado utilizando as funções que forçam o estado.
    """

    def __init__(self, parent_ug: UnidadeDeGeracao):

        super().__init__(parent_ug)
        self.codigo_state = MOA_UNIDADE_INDISPONIVEL

        self.selo = False
        self.logger.critical(f"[UG{self.parent_ug.id}] Entrando no estado indisponível. Para retornar a operação autônoma da UG é necessário intervenção manual via interface web.")

        self.parent_ug.__next_state = self

    def step(self) -> State:
        self.codigo_state = MOA_UNIDADE_INDISPONIVEL
        # Se as unidades estiverem paradas, ou o selo estiver ativo
        self.logger.debug(f"[UG{self.parent_ug.id}] Unidade indisponível (Etapa atual -> {self.parent_ug.etapa_atual})")

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
        self.codigo_state = MOA_UNIDADE_RESTRITA
        self.logger.info(f"[UG{self.parent_ug.id}] Entrando no estado restrito.")

    def step(self) -> State:
        self.codigo_state = MOA_UNIDADE_RESTRITA
        # Ler condiconadores
        deve_indisponibilizar = False
        deve_normalizar = False

        if [condic.ativo for condic in self.parent_ug.condicionadores]:
            condics_ativos = [condic.ativo for condic in self.parent_ug.condicionadores]
            deve_normalizar = [True for condic in condics_ativos if condic.gravidade == DEVE_NORMALIZAR]
            deve_super_normalizar = [True for condic in condics_ativos if condic.gravidade == DEVE_SUPER_NORMALIZAR]
            deve_indisponibilizar = [True for condic in condics_ativos if condic.gravidade == DEVE_INDISPONIBILIZAR]

        if deve_indisponibilizar or deve_normalizar or deve_super_normalizar:
            # Logar os condicionadores ativos
            self.logger.warning(f"[UG{self.parent_ug.id}] UG em modo restrito detectou condicionadores ativos:\n\n")
            self.logger.info(f"Descrição: {d.descr};\n Gravidade: {LISTA_GRAVIDADES[d.gravidade]}" for d in condics_ativos)

            # Se algum condicionador deve gerar uma indisponibilidade
            if deve_indisponibilizar:
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
        self.codigo_state = MOA_UNIDADE_DISPONIVEL
        self.logger.info(f"[UG{self.parent_ug.id}] Entrando no estado disponível.")

    def step(self) -> State:
        self.codigo_state = MOA_UNIDADE_DISPONIVEL

        self.logger.debug(f"[UG{self.parent_ug.id}] Step. (Tentativas de normalização: {self.parent_ug.tentativas_de_normalizacao}/{self.parent_ug.limite_tentativas_de_normalizacao})")

        # Ler condiconadores, verifica e armazena os ativos
        deve_indisponibilizar = False
        deve_normalizar = False
        deve_super_normalizar = False

        if [condic.ativo for condic in self.parent_ug.condicionadores]:
            condics_ativos = [condic.ativo for condic in self.parent_ug.condicionadores]
            deve_normalizar = [True for condic in condics_ativos if condic.gravidade == DEVE_NORMALIZAR]
            deve_super_normalizar = [True for condic in condics_ativos if condic.gravidade == DEVE_SUPER_NORMALIZAR]
            deve_indisponibilizar = [True for condic in condics_ativos if condic.gravidade == DEVE_INDISPONIBILIZAR]

        if deve_indisponibilizar or deve_normalizar or deve_super_normalizar:
            # Logar os condicionadores ativos
            self.logger.warning(f"[UG{self.parent_ug.id}] UG em modo restrito detectou condicionadores ativos:\n\n")
            self.logger.info(f"Descrição: {d.descr};\n Gravidade: {LISTA_GRAVIDADES[d.gravidade]}" for d in condics_ativos)

            # Se algum condicionador deve gerar uma indisponibilidade
            if deve_indisponibilizar:
                # Vai para o estado StateIndisponivel
                return StateIndisponivel(self.parent_ug)

            # Se algum condicionador deve gerar uma tentativa de normalizacao
            if deve_normalizar:

                # Se estourou as tentativas de normalização, vai para o estado StateIndisponivel
                if (
                    self.parent_ug.tentativas_de_normalizacao
                    > self.parent_ug.limite_tentativas_de_normalizacao
                ):
                    # Logar o ocorrido
                    self.logger.warning(f"[UG{self.parent_ug.id}] A UG estourou as tentativas de normalização, indisponibilizando UG.")
                    # Vai para o estado StateIndisponivel
                    return StateIndisponivel(self.parent_ug)

                # Se não estourou as tentativas de normalização, e já se passou tempo suficiente, deve tentar normalizar
                elif (self.parent_ug.ts_auxiliar - datetime.now()
                ).seconds > self.parent_ug.tempo_entre_tentativas:
                    # Adciona o contador
                    self.parent_ug.tentativas_de_normalizacao += 1
                    # Atualiza o timestamp
                    self.parent_ug.ts_auxiliar = datetime.now()
                    # Logar o ocorrido
                    self.logger.info(f"[UG{self.parent_ug.id}] Normalizando UG (Tentativa {self.parent_ug.tentativas_de_normalizacao}/{self.parent_ug.limite_tentativas_de_normalizacao}).")

                    # Reconhece e reset
                    self.parent_ug.reconhece_reset_alarmes()
                    self.parent_ug.con.fechaDj52L()
                    return self

                # Caso contrário (se ainda não deu o tempo), não faz nada
                else:
                    return self

        # Se não detectou nenhum condicionador ativo:
        else:
            self.logger.debug(f"[UG{self.parent_ug.id}] Etapa atual: \"{self.parent_ug.etapa_atual}\" | Etapa alvo: \"{self.parent_ug.etapa_alvo}\"")
            if self.release == True and self.aux == 1:
                self.release = False
                self.aux = 0

            # Calcula a atenuação devido aos condicionadores antes de prosseguir
            atenuacao = 0
            # Para cada condicionador
            for condicionador in self.parent_ug.condicionadores:
                # Se ele não deve ser ignorado, verificar
                if not condicionador.gravidade == DEVE_IGNORAR:
                    atenuacao = max(atenuacao, condicionador.valor)
                # Se ele deve ser ignorado, ignorar
                else:
                    pass

            # A atenuação já vem normalizada de 0 a 1, portanto
            # para ter o ganho é necessário apenas subtrair a atenuação
            ganho = 1 - atenuacao
            if (
                self.parent_ug.setpoint > self.parent_ug.setpoint_minimo
            ) and self.parent_ug.setpoint * ganho > self.parent_ug.setpoint_minimo:
                self.parent_ug.setpoint = self.parent_ug.setpoint * ganho

            self.logger.debug(f"[UG{self.parent_ug.id}] SP {self.parent_ug.setpoint} * GANHO {ganho} = {self.parent_ug.setpoint}.")
            # O comportamento da UG conforme a etapa em que a mesma se encontra

            if (
                self.parent_ug.etapa_alvo == UNIDADE_PARADA
                and not self.parent_ug.etapa_atual == UNIDADE_PARADA
            ):
                # Unidade parando
                self.logger.debug(f"[UG{self.parent_ug.id}] Unidade parando")
                # Se o setpoit for acima do mínimo
                if self.parent_ug.setpoint >= self.parent_ug.setpoint_minimo:
                    # Deve partir a UG
                    self.parent_ug.partir()
                    # E em seguida mandar o setpoint novo (boa prática)
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif (
                self.parent_ug.etapa_alvo > UNIDADE_PARADA
                and not self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA
            ):
                # Unidade sincronizando
                self.logger.debug(f"[UG{self.parent_ug.id}] Unidade sincronizando")
                if self.release == False and self.aux == 0:
                    Thread(target=lambda: self.verificar_partindo()).start()
                    self.aux = 1

                # Se potência = 0, impedir,
                if self.parent_ug.setpoint == 0:
                    self.logger.warning(f"[UG{self.parent_ug.id}] A UG estava sincronizando com SP zerado, parando a UG.")
                    self.parent_ug.parar()
                else:
                    self.parent_ug.partir()
                # Se não fazer nada

            elif self.parent_ug.etapa_atual == UNIDADE_PARADA:
                # Unidade parada
                self.logger.debug(f"[UG{self.parent_ug.id}] Unidade parada")
                # Se o setpoit for acima do mínimo
                if self.parent_ug.setpoint >= self.parent_ug.setpoint_minimo:
                    # Deve partir a UG
                    self.parent_ug.partir()
                    # E em seguida mandar o setpoint novo (boa prática)
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                # Unidade sincronizada
                self.logger.debug(f"[UG{self.parent_ug.id}] Unidade sincronizada")

                # Unidade sincronizada significa que ela está normalizada, logo zera o contador de tentativas
                if not self.parent_ug.aux_tempo_sincronizada:
                    self.parent_ug.aux_tempo_sincronizada = datetime.now()
                elif (
                    datetime.now() - self.parent_ug.aux_tempo_sincronizada
                ).seconds >= 300:
                    self.parent_ug.tentativas_de_normalizacao = 0
                # Se o setpoit estiver abaixo do mínimo
                if self.parent_ug.setpoint == 0:
                    # Deve manter a UG
                    self.parent_ug.parar()
                else:
                    # Caso contrário, mandar o setpoint novo
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif (
                self.parent_ug.etapa_atual not in UNIDADE_LISTA_DE_ETAPAS
                and self.parent_ug.etapa_alvo not in UNIDADE_LISTA_DE_ETAPAS
            ):
                # Etapa inconsistente
                # Logar o ocorrido
                self.logger.warning(f"[UG{self.parent_ug.id}] UG em etapa inconsistente. (Etapa atual: \"{self.parent_ug.etapa_atual}\")")
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
                    self.logger.debug(f"[UG{self.parent_ug.id}] Unidade sincronizada. Saindo do timer de verificação de partida")
                    self.release = True
                    return True
            self.logger.debug(f"[UG{self.parent_ug.id}] A Unidade estourou o timer de verificação de partida, adicionando condição para normalizar")
            self.parent_ug.clp.write_single_coil(REG_UG1_Operacao_EmergenciaLigar, [1 if self.parent_ug.id==1 else 0])
            self.parent_ug.clp.write_single_coil(REG_UG2_Operacao_EmergenciaLigar, [1 if self.parent_ug.id==2 else 0])
            self.release = True

        except Exception as e:
            raise e

        return False
