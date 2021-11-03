"""
operador_autonomo_sm.py

Implementacao teste de uma versao do moa utilizando SM
"""
import logging
import os
import sys
from threading import Thread
import time
from sys import stdout
from time import sleep

import json

from pyModbusTCP.server import DataBank, ModbusServer

from mensageiro.mensageiro_log_handler import MensageiroHandler
import clp_connector, database_connector, abstracao_usina

DEBUG = True

# Set-up logging
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)
if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
if not os.path.exists("logs/"):
    os.mkdir("logs/")
fh = logging.FileHandler("logs/MOA.log")  # log para arquivo
ch = logging.StreamHandler(stdout)  # log para linha de comando
mh = MensageiroHandler()  # log para telegram e voip
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [MOA-SM] %(message)s")
logFormatterSimples = logging.Formatter("[%(levelname)-5.5s] [MOA-SM] %(message)s")
fh.setFormatter(logFormatter)
ch.setFormatter(logFormatter)
mh.setFormatter(logFormatterSimples)
fh.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)
mh.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(mh)


class StateMachine:

    def __init__(self, initial_state):
        self.state = initial_state
        self.em_falha_critica = False

    def exec(self):
        try:
            if self.state is None:
                raise TypeError
            self.state = self.state.run()
        except Exception as e:
            logger.critical("Estado ({}) levantou uma exception: {}".format(self.state, repr(e)))
            self.em_falha_critica = True
            self.state = FalhaCritica()


class State:

    def __init__(self, *args, **kwargs):
        logger.debug("State {} called super().__init__()".format(str(self.__class__.__name__)))
        self.args = args
        self.kwargs = kwargs

    def run(self) -> object:
        return self


class FalhaCritica(State):
    """
    Lida com a falha na inicialização do MOA
    :return: None
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.critical("Falha crítica MOA.")

    def run(self):
        logger.critical("Falha crítica MOA. Exiting...")
        sys.exit(1)


class Pronto(State):
    """
    MOA está pronto, agora ele deve atualizar a vars
    :return: State
    """

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_tentativa = 0
        self.usina = instancia_usina
        self.usina.state_moa = 3

    def run(self):

        if self.n_tentativa >= 3:
            return FalhaCritica()
        else:

            try:
                self.usina.ler_valores()
                return ValoresInternosAtualizados(self.usina)

            except Exception as e:
                self.n_tentativa += 1
                logger.error("Erro durante a comunicação do MOA com a usina. Tentando novamente em {}s (tentativa{}/3)."
                             " Exception: {}.".format(self.usina.timeout_padrao, self.n_tentativa, repr(e)))
                sleep(self.usina.timeout_padrao)
                return self


class ValoresInternosAtualizados(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina
        DataBank.set_words(cfg['REG_PAINEL_LIDO'], [1])


    def run(self):
        """Decidir para qual modo de operação o sistema deve ir"""

        """
        Aqui a ordem do checks importa, e muito.
        """

        # Sempre lidar primeiro com a emergência.
        if self.usina.clp_emergencia_acionada:
            return Emergencia(self.usina)

        if self.usina.db_emergencia_acionada:
            return Emergencia(self.usina)

        # Em seguida com o modo manual (não autonomo)
        if not self.usina.modo_autonomo:
            return ModoManualAtivado(self.usina)

        # Se não foi redirecionado ainda,
        # assume-se que o MOA deve executar de modo autônomo

        # Atualizar os estados
        for ug in self.usina.ugs:
            ug.atualizar_estado()

        # TODO SEPARA FUNÇÃO
        self.usina.comporta.atualizar_estado(self.usina.nv_montante)

        # Verificamos se existem agendamentos
        if len(self.usina.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes(self.usina)

        # Verifica-se então a situação do reservatório
        if self.usina.aguardando_reservatorio:
            if self.usina.nv_montante_recente > self.usina.nv_religamento:
                logger.info("Reservatorio dentro do nivel de trabalho")
                self.usina.aguardando_reservatorio = 0
            return Pronto(self.usina)

        if self.usina.nv_montante < self.usina.nv_minimo:
            self.usina.aguardando_reservatorio = 1
            logger.info("Reservatorio abaixo do nivel de trabalho")
            return ReservatorioAbaixoDoMinimo(self.usina)

        if self.usina.nv_montante >= self.usina.nv_maximo:
            return ReservatorioAcimaDoMaximo(self.usina)

        # Se estiver tudo ok:
        return ReservatorioNormal(self.usina)


class Emergencia(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina
        self.n_tentativa = 0
        logger.warning("Usina entrado em estado de emergência")
        self.usina.distribuir_potencia(0)
        self.usina.escrever_valores()
        self.usina.acionar_emergencia()
        self.usina.heartbeat()

    def run(self):
        self.usina.heartbeat()
        self.n_tentativa += 1
        if self.n_tentativa > 3:
            logger.warning("Numeor de tentaivas de normalização excedidas, entrando em modo manual.")
            self.usina.entrar_em_modo_manual()
            self.usina.heartbeat()
            return ModoManualAtivado(self.usina)
        else:
            if self.usina.db_emergencia_acionada:
                logger.info("Emergencia acionada via Django/DB, aguardando Reset/Reco pela interface web ou pelo CLP")
                while self.usina.db_emergencia_acionada:
                    self.usina.ler_valores()
                    if not self.usina.clp.em_emergencia():
                        self.usina.db.update_emergencia(0)
                        self.usina.db_emergencia_acionada = 0

            if self.usina.clp_emergencia_acionada:
                try:
                    logger.info("Normalizando usina. (tentativa{}/3) (limite entre tentaivas: {}s)"
                                .format(self.n_tentativa, self.usina.cfg['timeout_normalizacao']))
                    self.usina.normalizar_emergencia()
                    # sleep(self.usina.cfg['timeout_normalizacao']/ESCALA_DE_TEMPO)
                    self.usina.ler_valores()
                except Exception as e:
                    logger.error("Erro durante a comunicação do MOA com a usina. Tentando novamente em {}s. "
                                 "Exception: {}.".format(self.usina.cfg['timeout_normalizacao'], repr(e)))
                return self
            else:
                logger.info("Usina normalizada")
                self.usina.heartbeat()
                return ControleRealizado(self.usina)


class ModoManualAtivado(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina
        logger.info("Usina em modo manual, deve-se alterar via painel ou interface web.")

    def run(self):
        self.usina.ler_valores()
        DataBank.set_words(cfg['REG_PAINEL_LIDO'], [1])
        self.usina.heartbeat()
        if self.usina.modo_autonomo:
            logger.info("Usina voltou para o modo Autonomo")
            self.usina.ler_valores()
            for ug in self.usina.ugs:
                ug.voltar_a_tentar_resetar()
            self.usina.heartbeat()
            return Pronto(self.usina)

        return self


class AgendamentosPendentes(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        logger.info("Tratando agendamentos")
        self.usina.verificar_agendamentos()
        return Pronto(self.usina)


class ReservatorioAbaixoDoMinimo(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        self.usina.distribuir_potencia(0)
        if self.usina.nv_montante <= self.usina.nv_fundo_reservatorio:
            logger.critical("Nivel montante ({:3.2f}) atingiu o fundo do reservatorio!".format(self.usina.nv_montante))
            return Emergencia(self.usina)
        return ControleRealizado(self.usina)


class ReservatorioAcimaDoMaximo(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        if self.usina.nv_montante >= self.usina.nv_maximorum:
            self.usina.distribuir_potencia(0)
            logger.critical("Nivel montante ({:3.2f}) atingiu o maximorum!".format(self.usina.nv_montante))
            return Emergencia(self.usina)
        else:
            self.usina.distribuir_potencia(self.usina.cfg['pot_maxima_usina'])
            self.usina.controle_ie = 0.5
            self.usina.controle_i = 0.5
            return ControleRealizado(self.usina)


class ReservatorioNormal(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):

        self.usina.controle_normal()
        return ControleRealizado(self.usina)


class ControleRealizado(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        logger.debug("Escrevendo valores")
        self.usina.escrever_valores()
        logger.debug("HB")
        self.usina.heartbeat()
        return Pronto(self.usina)


if __name__ == "__main__":
    # A escala de tempo é utilizada para acelerar as simulações do sistema
    # Utilizar 1 para testes sérios e 120 no máximo para testes simples
    ESCALA_DE_TEMPO = 1
    if len(sys.argv) > 1:
        ESCALA_DE_TEMPO = int(sys.argv[1])

    n_tentativa = 0
    timeout = 10
    logger.info("Iniciando o MOA_SM")
    logger.debug("Debug is ON")

    prox_estado = 0
    usina = None
    while prox_estado == 0:
        n_tentativa += 1
        if n_tentativa > 3:
            prox_estado = FalhaCritica
        else:
            # carrega as configurações
            config_file = os.path.join(os.path.dirname(__file__), 'config.json')
            with open(config_file, 'r') as file:
                cfg = json.load(file)

            # Inicia o conector do banco
            db = database_connector.Database()
            # Tenta iniciar a classe usina
            logger.debug("Iniciando classe Usina")
            try:
                usina = abstracao_usina.Usina(cfg, db)
            except Exception as e:
                logger.error(
                    "Erro ao iniciar Classe Usina. Tentando novamente em {}s (tentativa {}/3). Exception: {}.".format(
                        timeout, n_tentativa, repr(e)))
                sleep(timeout)
                continue

            # Update class values for the first time
            usina.ler_valores()

            # Inicializando Servidor Modbus (para algumas comunicações com o Elipse)
            try:
                logger.debug("Iniciando Servidor/Slave Modbus MOA.")
                modbus_server = ModbusServer(host=cfg['moa_slave_ip'], port=cfg['moa_slave_porta'],
                                             no_block=True)
                modbus_server.start()
                sleep(1)
                if not modbus_server.is_run:
                    raise ConnectionError
                prox_estado = Pronto

            except TypeError as e:
                logger.error(
                    "Erro ao iniciar abstração da usina. Tentando novamente em {}s (tentativa {}/3). Exception: {}."
                    "".format(timeout, n_tentativa, repr(e)))
                sleep(timeout)
            except ConnectionError as e:
                logger.error(
                    "Erro ao iniciar Modbus MOA. Tentando novamente em {}s (tentativa {}/3). Exception: {}.".format(
                        timeout, n_tentativa, repr(e)))
                sleep(timeout)
            except PermissionError as e:
                logger.error("Não foi possível iniciar o Modbus MOA devido a permissão do usuário. Exception: {}.".format(repr(e)))
                prox_estado = FalhaCritica
            except Exception as e:
                if DEBUG:
                    raise e
                logger.error("Erro Inesperado. Tentando novamente em {}s (tentativa{}/3). Exception: {}.".format(
                    timeout, n_tentativa, repr(e)))
                sleep(timeout)

    logger.info("Inicialização completa, executando o MOA \U0001F916")

    sm = StateMachine(initial_state=prox_estado(usina))
    while True:
        t_i = time.time()
        logger.debug("Executando estado: {}".format(sm.state.__class__.__name__))
        sm.exec()
        t_restante = max(5 - (time.time() - t_i), 0) / ESCALA_DE_TEMPO
        sleep(t_restante)
