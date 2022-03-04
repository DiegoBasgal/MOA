"""
operador_autonomo_sm.py

Implementacao teste de uma versao do moa utilizando SM
"""
from datetime import datetime
import logging
import logging.handlers as handlers
import os
import sys
import time
from sys import stdout, stderr
from time import sleep
import traceback
import json
from pyModbusTCP.server import DataBank, ModbusServer

import src.database_connector as database_connector
import src.abstracao_usina as abstracao_usina

# Set-up logging
rootLogger = logging.getLogger()
if (rootLogger.hasHandlers()):
    rootLogger.handlers.clear()
rootLogger.setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()
logger.setLevel(logging.NOTSET)

if not os.path.exists("logs/"):
    os.mkdir("logs/")
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [MOA-SM] %(message)s")
logFormatterSimples = logging.Formatter("[%(levelname)-5.5s] [MOA-SM] %(message)s")

ch = logging.StreamHandler(stderr)  # log para sdtout
ch.setFormatter(logFormatter)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

fh = handlers.TimedRotatingFileHandler("logs/MOA.log", when='midnight', interval=1, backupCount=7)  # log para arquivo
fh.setFormatter(logFormatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


class StateMachine:

    def __init__(self, initial_state):
        self.state = initial_state
        self.em_falha_critica = False

    def exec(self):
        try:
            if self.state is None:
                raise TypeError
            self.state = self.state.run()
        except TypeError as e:
            pass
        except Exception as e:
            logger.warning("Estado ({}) levantou uma exception: {}".format(self.state, repr(e)))
            logger.warning("Traceback: {}".format(traceback.format_exc()))
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
                             " Exception: {}.".format(self.usina.timeout_padrao * self.n_tentativa, self.n_tentativa, repr(e)))
                logger.critical("Traceback: {}".format(traceback.format_exc()))
                sleep(self.usina.timeout_padrao * self.n_tentativa)
                return self


class ValoresInternosAtualizados(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina
        DataBank.set_words(self.usina.cfg['REG_PAINEL_LIDO'], [1])


    def run(self):
        """Decidir para qual modo de operação o sistema deve ir"""

        """
        Aqui a ordem do checks importa, e muito.
        """
    
        if self.usina.clp_emergencia_acionada:
            return Emergencia(self.usina)

        if self.usina.db_emergencia_acionada:
            return Emergencia(self.usina)

         # Em seguida com o modo manual (não autonomo)
        if not self.usina.modo_autonomo:
            return ModoManualAtivado(self.usina)

        # Se não foi redirecionado ainda,
        # assume-se que o MOA deve executar de modo autônomo

        # TODO SEPARA FUNÇÃO
        self.usina.comporta.atualizar_estado(self.usina.nv_montante_recente)

        # Verificamos se existem agendamentos
        if len(self.usina.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes(self.usina)

        # Verifica-se então a situação do reservatório
        if self.usina.aguardando_reservatorio:
            if self.usina.nv_montante > self.usina.nv_alvo:
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
        self.em_sm_acionada = datetime.now()
        logger.warning("Usina entrado em estado de emergência (Timestamp: {})".format(self.em_sm_acionada))
        self.usina = instancia_usina
        self.n_tentativa = 0
        if not (
            self.usina.cfg["TENSAO_LINHA_BAIXA"] < self.usina.leituras.tensao_rs.valor < self.usina.cfg["TENSAO_LINHA_ALTA"] and 
            self.usina.cfg["TENSAO_LINHA_BAIXA"] < self.usina.leituras.tensao_st.valor < self.usina.cfg["TENSAO_LINHA_ALTA"] and 
            self.usina.cfg["TENSAO_LINHA_BAIXA"] < self.usina.leituras.tensao_tr.valor < self.usina.cfg["TENSAO_LINHA_ALTA"]):
            logger.info(
                "Tensão na linha: RS {:2.1f}kV ST{:2.1f}kV TR{:2.1f}kV.".format(
                    (datetime.now() - self.em_sm_acionada).seconds/60,
                    self.usina.leituras.tensao_rs.valor / 1000,
                    self.usina.leituras.tensao_st.valor / 1000,
                    self.usina.leituras.tensao_tr.valor / 1000,
                )
            )
        self.usina.distribuir_potencia(0)
        self.usina.escrever_valores()
        self.usina.heartbeat()
        self.nao_ligou = True

    def run(self):
        self.usina.heartbeat()
        self.n_tentativa += 1
        if self.n_tentativa > 3:
            logger.warning("Numero de tentaivas de normalização excedidas, entrando em modo manual.")
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
                    self.usina.ler_valores()
                    if not (
                        self.usina.cfg["TENSAO_LINHA_BAIXA"] < self.usina.leituras.tensao_rs.valor < self.usina.cfg["TENSAO_LINHA_ALTA"] and 
                        self.usina.cfg["TENSAO_LINHA_BAIXA"] < self.usina.leituras.tensao_st.valor < self.usina.cfg["TENSAO_LINHA_ALTA"] and 
                        self.usina.cfg["TENSAO_LINHA_BAIXA"] < self.usina.leituras.tensao_tr.valor < self.usina.cfg["TENSAO_LINHA_ALTA"]
                    ):
                        self.n_tentativa = 0

                        logger.debug(
                            "Sem tensão faz {} minutos. Tensão na linha: RS {:2.1f}kV ST{:2.1f}kV TR{:2.1f}kV.".format(
                                (datetime.now() - self.em_sm_acionada).seconds/60,
                                self.usina.leituras.tensao_rs.valor / 1000,
                                self.usina.leituras.tensao_st.valor / 1000,
                                self.usina.leituras.tensao_tr.valor / 1000,
                            )
                        )
                        if (datetime.now() - self.em_sm_acionada).seconds > 300:
                            if self.nao_ligou:
                                self.nao_ligou = False
                                logger.warning("Em emergência e sem tensão da mais de {:.1f} minutos".format((datetime.now() - self.em_sm_acionada).seconds/60))
                            else:
                                logger.debug("Em emergência e sem tensão da mais de {:.1f} minutos".format((datetime.now() - self.em_sm_acionada).seconds/60))
                                if (datetime.now() - self.em_sm_acionada).seconds > 60:
                                    logger.critical("Em emergência e sem tensão da mais de {:.1f} minutos".format((datetime.now() - self.em_sm_acionada).seconds/60))
                                    self.usina.entrar_em_modo_manual()
                                    return ModoManualAtivado(self.usina)
                        return self
                    logger.debug("Bela adormecida 10s")
                    sleep(10)
                    logger.info("Normalizando usina. (tentativa{}/3) (limite entre tentaivas: {}s)"
                                .format(self.n_tentativa, self.usina.cfg['timeout_normalizacao']))
                    self.usina.normalizar_emergencia()
                    self.usina.ler_valores()
                except Exception as e:
                    logger.error("Erro durante a comunicação do MOA com a usina. Exception: {}.".format(repr(e)))
                    logger.critical("Traceback: {}".format(traceback.format_exc()))
                return self
            else:
                logger.info("Usina normalizada")
                return ControleRealizado(self.usina)


class ModoManualAtivado(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina
        self.usina.modo_autonomo = False
        self.usina.escrever_valores()
        logger.info("Usina em modo manual, deve-se alterar via painel ou interface web.")

    def run(self):
        self.usina.ler_valores()
        DataBank.set_words(usina.cfg['REG_PAINEL_LIDO'], [1])
        self.usina.heartbeat()
        sleep(1/ESCALA_DE_TEMPO)
        if self.usina.modo_autonomo:
            logger.info("Usina voltou para o modo Autonomo")
            self.usina.db.update_habilitar_autonomo()
            self.usina.ler_valores()
            if self.usina.clp_emergencia_acionada == 1 or self.usina.db_emergencia_acionada == 1:
                self.usina.normalizar_emergencia()
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
        if self.usina.nv_montante_recente <= self.usina.nv_fundo_reservatorio:
            logger.critical("Nivel montante ({:3.2f}) atingiu o fundo do reservatorio!".format(self.usina.nv_montante_recente))
            return Emergencia(self.usina)
        return ControleRealizado(self.usina)


class ReservatorioAcimaDoMaximo(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        if self.usina.nv_montante_recente >= self.usina.nv_maximorum:
            self.usina.distribuir_potencia(0)
            logger.critical("Nivel montante ({:3.2f}) atingiu o maximorum!".format(self.usina.nv_montante_recente))
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
        for ug in self.usina.ugs:
            ug.step()
        self.usina.escrever_valores()
        logger.debug("HB")
        self.usina.heartbeat()
        return Pronto(self.usina)


if __name__ == "__main__":
    # A escala de tempo é utilizada para acelerar as simulações do sistema
    # Utilizar 1 para testes sérios e 120 no máximo para testes simples
    ESCALA_DE_TEMPO = 60
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
                usina.aguardando_reservatorio = 1
            except Exception as e:
                logger.error(
                    "Erro ao iniciar Classe Usina. Tentando novamente em {}s (tentativa {}/3). Exception: {}.".format(
                        timeout, n_tentativa, repr(e)))
                logger.critical("Traceback: {}".format(traceback.format_exc()))
                sleep(timeout)
                continue

            # Update class values for the first time
            usina.ler_valores()

            # Inicializando Servidor Modbus (para algumas comunicações com o Elipse)
            try:
                logger.debug("Iniciando Servidor/Slave Modbus MOA.")
                modbus_server = ModbusServer(host=usina.cfg['moa_slave_ip'], port=usina.cfg['moa_slave_porta'],
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
                logger.critical("Traceback: {}".format(traceback.format_exc()))
                sleep(timeout)
            except ConnectionError as e:
                logger.error(
                    "Erro ao iniciar Modbus MOA. Tentando novamente em {}s (tentativa {}/3). Exception: {}.".format(
                        timeout, n_tentativa, repr(e)))
                logger.critical("Traceback: {}".format(traceback.format_exc()))
                sleep(timeout)
            except PermissionError as e:
                logger.error("Não foi possível iniciar o Modbus MOA devido a permissão do usuário. Exception: {}.".format(repr(e)))
                logger.critical("Traceback: {}".format(traceback.format_exc()))
                prox_estado = FalhaCritica
            except Exception as e:
                logger.error("Erro Inesperado. Tentando novamente em {}s (tentativa{}/3). Exception: {}.".format(
                    timeout, n_tentativa, repr(e)))
                logger.critical("Traceback: {}".format(traceback.format_exc()))
                sleep(timeout)

    logger.info("Inicialização completa, executando o MOA \U0001F916")

    sm = StateMachine(initial_state=prox_estado(usina))
    while True:
        t_i = time.time()
        logger.debug("Executando estado: {}".format(sm.state.__class__.__name__))
        sm.exec()
        t_restante = max(1 - (time.time() - t_i), 0) / ESCALA_DE_TEMPO
        sleep(t_restante)
