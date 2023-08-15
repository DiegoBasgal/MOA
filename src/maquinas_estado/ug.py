__version__ = "0.2"
__author__ = "Diego Basgal", " Henrique Pfeifer", "Lucas Lavratti"
__description__ = "Este módulo corresponde a implementação da máquina de estados das Unidades de Geração."

import logging

from threading import Thread

from src.dicionarios.const import *

logger = logging.getLogger("logger")

class State:
    def __init__(self, parent=None) -> "None":

        # VERIFICAÇÃO DE ARGUENTOS

        if not parent:
            logger.error("[UG-SM] Houve um erro ao importar a classe pai da Unidade de Geração")
            raise ImportError

        else:
            self.parent = parent

    def step(self) -> "object":
        """
        Função abstrata para execução do passo da Máquina de Estados das Unidades
        de Geração.
        """

        pass

class StateManual(State):
    def __init__(self, parent) -> "None":
        super().__init__(parent)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.parent.codigo_state = UG_SM_MANUAL

        self.parent.borda_parar = False

        # FINALIZAÇÃO DO __INIT__

        logger.debug("")
        logger.info(f"[UG{self.parent.id}] Entrando no estado:                 \"Manual\". Para retornar a operação autônoma, favor agendar na interface web")
        logger.debug(f"[UG{self.parent.id}] Tentativas de normalização:         {self.parent.tentativas_normalizacao}/{self.parent.limite_tentativas_normalizacao}")


    def step(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados no modo Manual.

        Apenas atualiza o setpoint com a leitura de potência atual da Unidade.
        """

        self.parent.setpoint = self.parent.leitura_potencia
        return self


class StateIndisponivel(State):
    def __init__(self, parent) -> "None":
        super().__init__(parent)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.parent.codigo_state = UG_SM_INDISPONIVEL

        self.parent.borda_parar = True if self.parent.borda_parar else False

        # FINALIZAÇÃO DO __INIT__

        logger.debug("")
        logger.info(f"[UG{self.parent.id}] Entrando no estado:                 \"Indisponível\". Para retornar a operação autônoma, favor agendar na interface web")
        logger.debug(f"[UG{self.parent.id}] Tentativas de normalização:         {self.parent.tentativas_normalizacao}/{self.parent.limite_tentativas_normalizacao}")

    def step(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados no modo Indisponível.

        Apenas chama a função de bloqueio da Unidade da classe Pai.
        """

        self.parent.bloquear_unidade()
        return self


class StateRestrito(State):
    def __init__(self, parent) -> "None":
        super().__init__(parent)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.parent.codigo_state = UG_SM_RESTRITA

        self.parent.temporizar_normalizacao = False
        self.parent.borda_parar = True if self.parent.borda_parar else False

        # FINALIZAÇÃO DO __INIT__

        logger.debug("")
        logger.info(f"[UG{self.parent.id}] Entrando no estado                  \"Restrito\"")
        logger.debug(f"[UG{self.parent.id}] Tentativas de normalização:         {self.parent.tentativas_normalizacao}/{self.parent.limite_tentativas_normalizacao}")

    def step(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados no modo Restrito.

        O estado Restrito serve como um mecanismo de espera no caso do acionamento
        de uma ocorrência de gravidade AGUARDAR. Quando a Unidade entra no estado,
        fica realizando a verificação de Condicionadores até que não haja mais
        nenhum ativo, ou até o operador agendar um tempo para a Indisponibilização
        da máquina caso as ocorrências ainda estejam ativas no limite de tempo.
        Primeiramente chama a função de bloqueio da Unidade, para depois passar a
        verificar os Condicionadores ativos da Unidade.
        """

        self.parent.bloquear_unidade()
        self.parent.verificar_limites()
        flag = self.parent.verificar_condicionadores()

        if flag == CONDIC_INDISPONIBILIZAR:
            logger.warning(f"[UG{self.parent.id}] UG detectou condicionadores com gravidade alta, indisponibilizando UG.")
            self.parent.temporizar_normalizacao = False
            return StateIndisponivel(self.parent)

        elif flag == CONDIC_IGNORAR:
            logger.info(f"[UG{self.parent.id}] A UG não possui mais condicionadores ativos, normalizando e retornando para o estado disponível")
            self.parent.temporizar_normalizacao = False
            self.parent.reconhece_reset_alarmes()
            return StateDisponivel(self.parent)

        if self.parent.normalizacao_agendada:
            logger.info(f"[UG{self.parent.id}] Normalização por tempo acionada -> Tempo definido: {self.parent.tempo_normalizar}")
            self.parent.normalizacao_agendada = False
            Thread(target=lambda: self.parent.aguardar_normalizacao(self.parent.tempo_normalizar)).start()

        elif self.parent.temporizar_normalizacao:
            return self if self.parent.normalizar_unidade() else StateIndisponivel(self.parent)

        else:
            logger.debug(f"[UG{self.parent.id}] Aguardando normalização sem tempo pré-definido")
            return self

class StateDisponivel(State):
    def __init__(self, parent) -> "None":
        super().__init__(parent)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.parent.codigo_state = UG_SM_DISPONIVEL
        self.parent.tentativas_normalizacao = 0
        self.parent.borda_parar = False

        # FINALIZAÇÃO DO __INIT__

        logger.debug("")
        logger.info(f"[UG{self.parent.id}] Entrando no estado:                 \"Disponível\"")
        logger.debug(f"[UG{self.parent.id}] Tentativas de normalização:         {self.parent.tentativas_normalizacao}/{self.parent.limite_tentativas_normalizacao}")
        logger.debug("")


    def step(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados no modo Disponível.

        Realiza a verificação de Condicionadores para determinar o próximo passo
        no caso de algum estar ativo. Caso não haja ocorrências, passa a chamar a
        função de atenuação da Unidade, para depois chamar a função de controle
        de etapas.
        """

        # self.parent.verificar_limites()
        flag = self.parent.verificar_condicionadores()

        if flag == CONDIC_INDISPONIBILIZAR:
            logger.warning(f"[UG{self.parent.id}] Indisponibilizando UG.")
            return StateIndisponivel(self.parent)

        elif flag == CONDIC_AGUARDAR:
            logger.warning(f"[UG{self.parent.id}] Entrando no estado Restrito até normalização da condição.")
            return StateRestrito(self.parent)

        elif flag == CONDIC_NORMALIZAR:
            return self if self.parent.normalizar_unidade() else StateIndisponivel(self.parent)

        else:
            self.parent.controlar_etapas()

            return self
