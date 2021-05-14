"""
operador_autonomo_sm.py

Implementacao teste de uma versao do moa utilizando SM
"""

import logging
import time
import trace
from datetime import datetime
from sys import stdout
from time import sleep
from pyModbusTCP.server import ModbusServer
from mensageiro.mensageiro_log_handler import MensageiroHandler
import abstracao_usina

# Set-up logging
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("MOA.log")  # log para arquivo
ch = logging.StreamHandler(stdout)  # log para linha de comando
mh = MensageiroHandler()  # log para telegram e voip
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logFormatterSimples = logging.Formatter("[%(levelname)-5.5s]  %(message)s")
fh.setFormatter(logFormatter)
ch.setFormatter(logFormatter)
mh.setFormatter(logFormatterSimples)
fh.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)
mh.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(mh)

# Vars globais
usina = abstracao_usina.Usina
ESCALA_DE_TEMPO = 6

def controle_proporcional(Kp, erro_nivel):
    """
    Controle Proporcional do PID
    https://en.wikipedia.org/wiki/PID_controller#Proportional
    :param erro_nivel: Float
    :return: Sinal de controle proporcional
    """
    return Kp * erro_nivel


def controle_integral(Ki, erro_nivel, ganho_integral_anterior):
    """
    Controle Integral do PID
    https://en.wikipedia.org/wiki/PID_controller#Integral
    :param erro_nivel: Float
    :return: Float sinal de controle integral
    """
    res = (Ki * erro_nivel) + ganho_integral_anterior
    res = min(res, 0.8)  # Limite superior
    res = max(res, 0)  # Limite inferior = 0
    return res


def controle_derivativo(Kd, erro_nivel, erro_nivel_anterior):
    """
    Controle Derivativo do PID
    https://en.wikipedia.org/wiki/PID_controller#Derivative
    :param erro_nivel_anterior: Float
    :param erro_nivel: Float
    :return: Float: Sinal de controle derivativo
    """
    return Kd * (erro_nivel - erro_nivel_anterior)


class StateMachine:

    def __init__(self, initial_state):
        self.state = initial_state

    def exec(self):
        self.state = self.state.run()


class State:

    def __init__(self, *args, **kwargs):
        logger.debug("State {} called super().__init__()".format(str(self.__class__.__name__)))
        self.args = args
        self.kwargs = kwargs

    def run(self) -> object:
        return self


class NaoInicializado(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_tentativa = 0
        self.timeout = 30
        logger.info("Iniciando o MOA")

    def run(self):
        """
        Cuida da inicialização do módulo usina.py e do slave modbus do MOA.
        Tenta de novo 3x, se falhar, entra em modo de emergência
        :return: State
        """

        # Var global usina
        global usina

        self.n_tentativa += 1
        if self.n_tentativa > 3:
            return FalhaCritica()
        else:

            # Tenta conectar com a usina antes de tudo
            logger.debug("Iniciando classe Usina")
            try:
                usina = abstracao_usina.Usina()
                if usina.clp_online:
                    logger.debug("Conexão com a CLP ok.")
                else:
                    raise ConnectionError

            except ConnectionError as e:
                logger.error("A conexão com a CLP falhou. Tentando novamente em {}s (tentativa {}/3). Exception: {}.".format(self.timeout, self.n_tentativa, repr(e)))
                sleep(self.timeout)
                return self

            except AttributeError as e:
                logger.error("A conexão com a CLP falhou. Tentando novamente em {}s (tentativa {}/3). Exception: {}.".format(self.timeout, self.n_tentativa, repr(e)))
                sleep(self.timeout)
                return self

            except Exception as e:
                logger.error("Erro Inesperado. Tentando novamente em {}s (tentativa{}/3). Exception: {}.".format(self.timeout, self.n_tentativa, repr(e)))
                sleep(self.timeout)
                return self

            # Inicializando Servidor Modbus (para algumas comunicações com o Elipse)
            try:
                logger.debug("Iniciando Servidor/Slave Modbus MOA.")
                modbus_server = ModbusServer(host=usina.modbus_server_ip, port=usina.modbus_server_porta, no_block=True)
                modbus_server.start()
                if not modbus_server.is_run:
                    raise ConnectionError
            except ConnectionError as e:
                logger.error("Erro ao iniciar Modbus MOA. Tentando novamente em {}s (tentativa {}/3). Exception: {}.".format(self.timeout, self.n_tentativa, repr(e)))
                sleep(self.timeout)
                return self

            except Exception as e:
                logger.error("Erro Inesperado. Tentando novamente em {}s (tentativa{}/3). Exception: {}.".format(self.timeout, self.n_tentativa, repr(e)))
                sleep(self.timeout)
                return self

            logger.info("Inicialização completa, executando o MOA")
            return Pronto()


class FalhaCritica(State):
    """
    Lida com a falha na inicialização do MOA
    :return: None
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.critical("Falha crítica MOA.")
        raise RuntimeError


class Pronto(State):
    """
    MOA está pronto, agora ele deve atualizar a vars
    :return: State
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_tentativa = 0

    def run(self):
        global usina

        if self.n_tentativa >= 3:
            return FalhaCritica()
        else:

            try:
                usina.ler_valores()
                return ValoresInternosAtualizados()

            except Exception as e:
                self.n_tentativa += 1
                logger.error("Erro durante a comunicação do MOA com a usina. Tentando novamente em {}s (tentativa{}/3). Exception: {}.".format(usina.timeout_padrao, self.n_tentativa, repr(e)))
                sleep(usina.timeout_padrao)
                return self


class ValoresInternosAtualizados(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        "Decidir para qual modo de operação o sistema deve ir"
        global usina

        """
        Aqui a ordem do checks importa, e muito.
        """

        # Sempre lidar primeiro com a emergência.
        if usina.emergencia_acionada:
            return Emergencia()

        # Em seguida com o modo manual (não autonomo)
        if not usina.modo_autonomo:
            return ModoManualAtivado()

        # Se não foi redirecionado ainda,
        # assume-se que o MOA deve executar de modo autônomo

        # Verificamos se existem agendamentos
        if len(usina.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes()

        # Verifica-se então a situação do reservatório

        if usina.aguardando_reservatorio:
            if usina.nv_montante_recente > usina.nv_religamento:
                usina.aguardando_reservatorio = False
            return Pronto()

        if usina.nv_montante < usina.nv_minimo:
            return ReservatorioAbaixoDoMinimo()

        if usina.nv_montante >= usina.nv_maximo:
            return ReservatorioAcimaDoMaximo()

        # Se estiver tudo ok:
        return ReservatorioNormal()

# ToDo Implementar Emergência
class Emergencia(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):

        raise NotImplementedError


class ModoManualAtivado(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("Usina em modo manual, deve-se alterar via painel ou interface web.")

    def run(self):

        usina.heartbeat()
        usina.ler_valores()
        if usina.modo_autonomo:
            logger.info("Usina voltou para o modo Autonomo")
            return Pronto()

        return self


class AgendamentosPendentes(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        raise NotImplementedError


class ReservatorioAbaixoDoMinimo(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        usina.distribuir_potencia(0)
        return ControleRealizado()


class ReservatorioAcimaDoMaximo(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        usina.distribuir_potencia(usina.pot_maxima)
        usina.comporta.atualizar_estado(usina.nv_montante)
        return ControleRealizado()


class ReservatorioNormal(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):

        # Calcula PID
        logger.debug("Alvo: {:0.3f}, Recente: {:0.3f}, Anterior: {:0.3f}".format(usina.nv_alvo, usina.nv_montante_recente, usina.nv_montante_anterior))
        usina.controle_p = controle_proporcional(usina.kp, usina.erro_nv)
        usina.controle_i = controle_integral(usina.ki, usina.erro_nv, usina.controle_i)
        usina.controle_d = controle_derivativo(usina.kd, usina.erro_nv, usina.erro_nv_anterior)
        usina.saida_pid = usina.controle_p + usina.controle_i + usina.controle_d
        logger.debug("PID: {:0.3f}, P:{:0.3f}, I:{:0.3f}, D:{:0.3f}".format(usina.saida_pid, usina.controle_p, usina.controle_i, usina.controle_d))

        # Calcula o integrador de estabilidade e limita
        usina.saida_ie = usina.saida_pid * (usina.kie / ESCALA_DE_TEMPO) + usina.saida_ie
        usina.saida_ie = max(min(usina.saida_ie, 1), 0)

        # Arredondamento e limitação
        pot_alvo = round(usina.pot_maxima * usina.saida_ie, 2)
        pot_alvo = max(min(pot_alvo, usina.pot_maxima), usina.pot_minima)
        usina.distribuir_potencia(pot_alvo)

        return ControleRealizado()


class ControleRealizado(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        logger.debug("Escrevendo valores")
        usina.escrever_valores()
        logger.debug("HB")
        usina.heartbeat()
        return Pronto()


if __name__ == "__main__":

    sm = StateMachine(initial_state=NaoInicializado())
    while True:
        t_i = time.time()
        logger.debug("Proximo estado: {}".format(sm.state.__class__.__name__))
        try:
            sm.exec()
        except BaseException as e:
            logger.error("A SM falhou em mudar de estado para {}.".format(sm.state.__class__.__name__))
            logger.error("Exceção {}".format(repr(e)))
            sm.state = FalhaCritica()
        finally:
            t_restante = max(5 - (time.time() - t_i), 0)/ESCALA_DE_TEMPO
            sleep(t_restante)


