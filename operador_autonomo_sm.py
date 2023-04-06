"""
operador_autonomo_sm.py

Implementacao teste de uma versao do moa utilizando SM
"""

import os
import sys
import time
import json
import pytz
import logging
import threading
import traceback
import logging.handlers as handlers

from sys import stderr
from time import sleep
from datetime import datetime
from pyModbusTCP.server import DataBank, ModbusServer

from src.codes import *
from src.mensageiro import voip
from src.abstracao_usina import Usina
from src.database_connector import Database
from src.field_connector import FieldConnector
from src.mensageiro.mensageiro_log_handler import MensageiroHandler

# Set-up logging
rootLogger = logging.getLogger()
if rootLogger.hasHandlers():
    rootLogger.handlers.clear()
rootLogger.setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)
if logger.hasHandlers():
    logger.handlers.clear()
logger.setLevel(logging.NOTSET)

if not os.path.exists(os.path.join(os.path.dirname(__file__), "logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

def timeConverter(*args):
    return datetime.now(tz).timetuple()

tz = pytz.timezone("Brazil/East")
thread_id = threading.get_native_id()
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12s] [%(levelname)-5.5s] [MOA] %(message)s")
logFormatterSimples = logging.Formatter("[%(levelname)-5.5s] %(message)s")
logFormatter.converter = timeConverter

ch = logging.StreamHandler(stderr)  # log para sdtout
ch.setFormatter(logFormatter)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

fh = handlers.TimedRotatingFileHandler(
    os.path.join(os.path.dirname(__file__), "logs", "MOA.log"),
    when="midnight",
    interval=1,
    backupCount=7,
)  # log para arquivo
fh.setFormatter(logFormatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

mh = MensageiroHandler()
mh.setFormatter(logFormatterSimples)
mh.setLevel(logging.INFO)
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
            logger.warning(f"Estado ({self.state}) levantou uma exception: \"{repr(e)}\"")
            logger.debug(f"Traceback: {traceback.print_stack}")
            self.em_falha_critica = True
            self.state = FalhaCritica()

class State:
    def __init__(self, usina: Usina, *args, **kwargs):
        if not usina:
            raise ValueError("Erro ao carregar classe Usina na máquina de estados.")
        else:
            self.usn = usina

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
        logger.critical("Falha crítica MOA. Exiting...")
        sys.exit(1)


class Pronto(State):
    """
    MOA está pronto, agora ele deve atualizar a vars
    :return: State
    """

    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.n_tentativa = 0
        self.usn.state_moa = 3

    def run(self):
        self.usn.heartbeat()
        if self.n_tentativa >= 2:
            return FalhaCritica()
        else:
            try:
                self.usn.ler_valores()
                return OperacaoTDAOffline() if self.usn.TDA_Offline else ValoresInternosAtualizados()

            except Exception as e:
                self.n_tentativa += 1
                logger.error(f"Erro durante a comunicação do MOA com a usina. Tentando novamente em {self.usn.cfg['timeout_padrao'] * self.n_tentativa}s (tentativa{self.n_tentativa}/3). \
                            Exception: \"{repr(e)}\".")
                logger.debug(f"Traceback: {traceback.print_stack}")
                sleep(self.usn.cfg["timeout_padrao"] * self.n_tentativa)
                return self


class ValoresInternosAtualizados(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        DataBank.set_words(self.usn.cfg["REG_PAINEL_LIDO"], [1])
        self.deve_ler_condicionadores=False
        self.habilitar_emerg_condic_e=False
        self.habilitar_emerg_condic_c=False

    def run(self):
        self.usn.heartbeat()
        """Decidir para qual modo de operação o sistema deve ir"""

        """
        Aqui a ordem do checks importa, e muito.
        """

        # atualizar arquivo das configurações
        global aux
        global deve_normalizar
        self.usn.TDA_Offline = False

        with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as file:
            json.dump(self.usn.cfg, file, indent=4)

        for condicionador_essencial in self.usn.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.deve_ler_condicionadores=True

        if self.usn.avisado_em_eletrica or self.deve_ler_condicionadores==True:
            for condicionador_essencial in self.usn.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade >= DEVE_INDISPONIBILIZAR:
                    self.habilitar_emerg_condic_e=True
                elif condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_NORMALIZAR:
                    deve_normalizar=True
                    self.habilitar_emerg_condic_e=False
                else:
                    deve_normalizar=False
                    self.habilitar_emerg_condic_e=False

            for condicionador in self.usn.condicionadores:
                if condicionador.ativo and condicionador.gravidade >= DEVE_INDISPONIBILIZAR:
                    self.habilitar_emerg_condic_c=True
                elif condicionador.ativo and condicionador.gravidade == DEVE_NORMALIZAR:
                    self.habilitar_emerg_condic_c=False
                    deve_normalizar=True
                else:
                    deve_normalizar=False
                    self.habilitar_emerg_condic_c=False

            if self.habilitar_emerg_condic_e or self.habilitar_emerg_condic_c:
                logger.warning("Foram detectados Condicionadores ativos com gravidade: \"Indisponibilizar\"!")
                return Emergencia(self.usn)

        if deve_normalizar:
            if (not self.usn.normalizar_emergencia()) and self.usn.tensao_ok==False and aux==0:
                logger.warning("Tensão da linha fora do limite")
                aux = 1
                threading.Thread(target=lambda: self.usn.aguardar_tensao(600)).start()

            elif self.usn.timer_tensao:
                aux = 0
                deve_normalizar = None
                self.usn.timer_tensao = None

            elif self.usn.timer_tensao==False:
                aux = 0
                deve_normalizar = None
                self.usn.timer_tensao = None
                logger.critical("O tempo de normalização da linha excedeu o limite! (10 min)")
                return Emergencia(self.usn)

        if self.usn.clp_emergencia_acionada or self.usn.db_emergencia_acionada:
            logger.warning("Comando recebido: habilitando modo de emergencia.")
            sleep(2)
            return Emergencia(self.usn)

        # Verificamos se existem agendamentos
        if len(self.usn.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes(self.usn)

        # Em seguida com o modo manual (não autonomo)
        if not self.usn.modo_autonomo:
            logger.debug("Comando recebido: desabilitar modo autonomo.")
            sleep(2)
            return ModoManualAtivado(self.usn)

        # Se não foi redirecionado ainda,
        # assume-se que o MOA deve executar de modo autônomo

        # Verifica-se então a situação do reservatório
        if self.usn.aguardando_reservatorio:
            if self.usn.nv_montante > self.usn.cfg["nv_alvo"]:
                logger.debug("Reservatorio dentro do nivel de trabalho")
                self.usn.aguardando_reservatorio = 0
                return ReservatorioNormal(self.usn)

        if self.usn.nv_montante < self.usn.cfg["nv_minimo"]:
            self.usn.aguardando_reservatorio = 1
            logger.info("Reservatorio abaixo do nivel de trabalho")
            return ReservatorioAbaixoDoMinimo(self.usn)

        if self.usn.nv_montante >= self.usn.cfg["nv_maximo"]:
            return ReservatorioAcimaDoMaximo(self.usn)

        # Se estiver tudo ok:
        return ReservatorioNormal(self.usn)


class Emergencia(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.em_sm_acionada = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        logger.warning(f"Usina entrado em estado de emergência (Timestamp: {self.em_sm_acionada})")
        self.usn = usina
        self.n_tentativa = 0
        self.usn.escrever_valores()
        self.nao_ligou = True

    def run(self):
        self.usn.heartbeat()
        self.n_tentativa += 1
        if self.n_tentativa > 2:
            logger.warning("Numero de tentaivas de normalização excedidas, entrando em modo manual.")
            for ug in self.usn.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()
            return ModoManualAtivado(self.usn)
        else:
            # TODO revisar lógica
            if self.usn.db_emergencia_acionada:
                logger.warning("Emergencia acionada via Interface WEB/DB, aguardando Reset/Reconhecimento pela interface ou CLP")
                while self.usn.db_emergencia_acionada:
                    self.usn.ler_valores()
                    if not self.usn.clp.em_emergencia():
                        self.usn.db.update_emergencia(0)
                        self.usn.db_emergencia_acionada = 0

            self.usn.ler_valores()
            # Ler condiconadores
            deve_indisponibilizar = False
            deve_normalizar = False
            condicionadores_ativos = []

            for condicionador_essencial in self.usn.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    deve_indisponibilizar = True
                elif condicionador_essencial.gravidade == DEVE_NORMALIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    deve_normalizar = True

            for condicionador in self.usn.condicionadores:
                if condicionador.ativo and condicionador.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador)
                    deve_indisponibilizar=True
                elif condicionador.gravidade == DEVE_NORMALIZAR:
                    condicionadores_ativos.append(condicionador)
                    deve_indisponibilizar=False

            if (self.usn.clp_emergencia_acionada or deve_normalizar or deve_indisponibilizar):
                try:

                    # Se algum condicionador deve gerar uma indisponibilidade
                    if deve_indisponibilizar:
                        # Logar os condicionadores ativos
                        logger.critical(f"[USN] USN detectou condicionadores ativos, passando USINA para manual e ligando por VOIP.\nCondicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
                        return ModoManualAtivado(self.usn)

                    elif deve_normalizar:
                        logger.debug("Aguardando antes de tentar normalizar novamente (5s)")
                        sleep(5)
                        logger.info(f"Normalizando usina. (tentativa{self.n_tentativa}/2) (limite entre tentaivas: {self.usn.cfg['timeout_normalizacao']}s)")
                        self.usn.deve_normalizar_forcado=True
                        self.usn.normalizar_emergencia()
                        self.usn.ler_valores()
                        return self

                    else:
                        logger.debug("Nenhum condicionador relevante ativo...")
                        self.usn.ler_valores()
                        return ControleRealizado(self.usn)

                except Exception as e:
                    logger.error(f"Erro durante a comunicação do MOA com a usina. Exception: {repr(e)}.")
                    logger.debug(f"Traceback: {traceback.print_stack}")
                return self
            else:
                self.usn.ler_valores()
                logger.info("Usina normalizada")
                return ControleRealizado(self.usn)


class ModoManualAtivado(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn = usina
        self.usn.modo_autonomo = False
        self.usn.escrever_valores()
        logger.info("Usina em modo manual, deve-se alterar via painel ou interface web.")

    def run(self):
        self.usn.heartbeat()
        self.usn.ler_valores()
        for ug in self.usn.ugs:
            ug.release_timer = True
        DataBank.set_words(usina.cfg["REG_PAINEL_LIDO"], [1])
        self.usn.ug1.setpoint = self.usn.ug1.leitura_potencia.valor
        self.usn.ug2.setpoint = self.usn.ug2.leitura_potencia.valor
        self.usn.ug3.setpoint = self.usn.ug3.leitura_potencia.valor

        self.usn.controle_ie = (self.usn.ug1.setpoint + self.usn.ug2.setpoint + self.usn.ug3.setpoint) / self.usn.cfg["pot_maxima_alvo"]
        self.usn.controle_i = max(min(self.usn.controle_ie - (self.usn.controle_i * self.usn.cfg["ki"]) - self.usn.cfg["kp"] * self.usn.erro_nv - self.usn.cfg["kd"] * (self.usn.erro_nv - self.usn.erro_nv_anterior), 0.8), 0)

        self.usn.escrever_valores()
        sleep(1 / ESCALA_DE_TEMPO)
        if self.usn.modo_autonomo:
            logger.debug("Comando recebido: habilitar modo autonomo.")
            sleep(2)
            logger.info("Usina voltou para o modo Autonomo")
            self.usn.ler_valores()
            if 1 in (self.usn.clp_emergencia_acionada, self.usn.db_emergencia_acionada):
                self.usn.normalizar_emergencia()
            return ControleRealizado(self.usn)

        if len(self.usn.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes(self.usn)

        return self


class AgendamentosPendentes(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn = usina

    def run(self):
        logger.debug("Tratando agendamentos")
        self.usn.verificar_agendamentos()
        return ControleRealizado(self.usn)


class ReservatorioAbaixoDoMinimo(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn = usina

    def run(self):
        self.usn.heartbeat()
        if self.usn.nv_montante_recente <= self.usn.cfg["nv_fundo_reservatorio"]:
            if not self.usn.ping(self.usn.cfg["TDA_slave_ip"]):
                logger.warning("Sem comunicação com CLP TDA, entrando no modo de operação Offline")
                self.usn.TDA_Offline = True
                return OperacaoTDAOffline(self.usn)
            else:
                self.usn.distribuir_potencia(0)
                for ug in self.usn.ugs:
                    ug.step()
                logger.critical(f"Nivel montante ({self.usn.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                return Emergencia(self.usn)

        return ControleRealizado(self.usn)


class ReservatorioAcimaDoMaximo(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn = usina

    def run(self):
        self.usn.heartbeat()
        if self.usn.nv_montante_recente >= self.usn.cfg["nv_maximorum"]:
            self.usn.distribuir_potencia(0)
            logger.critical(f"Nivel montante ({self.usn.nv_montante_recente:3.2f}) atingiu o maximorum!")
            return Emergencia(self.usn)
        else:
            self.usn.controle_ie = 1
            self.usn.controle_i = 0.8
            self.usn.distribuir_potencia(self.usn.cfg["pot_maxima_alvo"])
            for ug in self.usn.ugs:
                ug.step()
            return ControleRealizado(self.usn)


class ReservatorioNormal(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn = usina

    def run(self):

        self.usn.controle_normal()
        for ug in self.usn.ugs:
            ug.step()
        return ControleRealizado(self.usn)

class OperacaoTDAOffline(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn = usina
        self.deve_ler_condicionadores = False
        self.habilitar_emerg_condic_e = False
        self.habilitar_emerg_condic_c = False

    def run(self):
        self.usn.heartbeat()
        global aux
        global deve_normalizar
        self.usn.TDA_Offline = True

        for condicionador_essencial in self.usn.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.deve_ler_condicionadores=True

        if self.usn.avisado_em_eletrica or self.deve_ler_condicionadores==True:
            for condicionador_essencial in self.usn.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade >= DEVE_INDISPONIBILIZAR:
                        self.habilitar_emerg_condic_e=True
                elif condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_NORMALIZAR:
                    deve_normalizar=True
                    self.habilitar_emerg_condic_e=False
                else:
                    deve_normalizar=False
                    self.habilitar_emerg_condic_e=False

            for condicionador in self.usn.condicionadores:
                if condicionador.ativo and condicionador.gravidade >= DEVE_INDISPONIBILIZAR:
                    self.habilitar_emerg_condic_c=True
                elif condicionador.ativo and condicionador.gravidade == DEVE_NORMALIZAR:
                    self.habilitar_emerg_condic_c=False
                    deve_normalizar=True
                else:
                    deve_normalizar=False
                    self.habilitar_emerg_condic_c=False

            if self.habilitar_emerg_condic_e or self.habilitar_emerg_condic_c:
                logger.warning("Foram detectados Condicionadores ativos com gravidade: \"Indisponibilizar\"!")
                return Emergencia(self.usn)

        if deve_normalizar:
            if (not self.usn.normalizar_emergencia()) and self.usn.tensao_ok==False and aux==0:
                logger.warning("Tensão da linha fora do limite ")
                aux = 1
                threading.Thread(target=lambda: self.usn.aguardar_tensao(20)).start()

            elif self.usn.timer_tensao:
                aux = 0
                deve_normalizar = None
                self.usn.timer_tensao = None

            elif self.usn.timer_tensao==False:
                aux = 0
                deve_normalizar = None
                self.usn.timer_tensao = None
                logger.warning("O tempo de normalização da linha excedeu o limite! (10 min)")
                return Emergencia(self.usn)

        if not self.usn.modo_autonomo:
            logger.info("Comando recebido: desabilitar modo autonomo.")
            sleep(2)
            return ModoManualAtivado(self.usn)

        if len(self.usn.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes(self.usn)

        for ug in self.usn.ugs:
            ug.controle_cx_espiral()
            ug.step()

        return ControleRealizado(self.usn)

class ControleRealizado(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn = usina

    def run(self):
        logger.debug("Heartbeat")
        self.usn.heartbeat()
        self.usn.escrever_valores()
        return Pronto(self.usn)

def leitura_temporizada():
    delay = 1800
    proxima_leitura = time.time() + delay
    logger.debug("Iniciando o timer de leitura por hora.")
    while True:
        logger.debug("Inciando nova leitura...")
        try:
            if usina.leituras_por_hora() and usina.acionar_voip:
                acionar_voip()
            for ug in usina.ugs:
                if ug.leituras_por_hora() and ug.acionar_voip:
                    acionar_voip()
            time.sleep(max(0, proxima_leitura - time.time()))

        except Exception:
            logger.debug("Houve um problema ao executar a leitura por hora")

        proxima_leitura += (time.time() - proxima_leitura) // delay * delay + delay

def acionar_voip():
    try:
        if usina.acionar_voip:
            voip.TDA_FalhaComum=[True if usina.TDA_FalhaComum else False]
            voip.BombasDngRemoto=[True if usina.BombasDngRemoto else False]
            voip.Disj_GDE_QCAP_Fechado=[True if usina.Disj_GDE_QCAP_Fechado else False]
            voip.enviar_voz_auxiliar()
            usina.acionar_voip = False
        elif usina.avisado_em_eletrica:
            voip.enviar_voz_emergencia()
            usina.avisado_em_eletrica = False

        for ug in usina.ugs:
            if ug.acionar_voip:
                ug.acionar_voip = False

    except Exception:
        logger.debug("Houve um problema ao ligar por Voip")

if __name__ == "__main__":
    # A escala de tempo é utilizada para acelerar as simulações do sistema
    # Utilizar 1 para testes sérios e 120 no máximo para testes simples
    ESCALA_DE_TEMPO = 2
    if len(sys.argv) > 1:
        ESCALA_DE_TEMPO = int(sys.argv[1])

    aux = 0
    deve_normalizar = None
    usina = None
    timeout = 10
    prox_estado = 0
    n_tentativa = 0

    logger.debug("Debug is ON")
    logger.info("Iniciando MOA...")
    logger.debug(f"Escala de tempo: {ESCALA_DE_TEMPO}")

    while prox_estado == 0:
        n_tentativa += 1

        if n_tentativa >= 3:
            prox_estado = FalhaCritica
        else:
            try:
                logger.info("Carregando arquivo de configuração \"config.json\".")

                config_file = os.path.join(os.path.dirname(__file__), "config.json")
                with open(config_file, "r") as file:
                    cfg = json.load(file)

                config_file = os.path.join(os.path.dirname(__file__), "config.json.bkp")
                with open(config_file, "w") as file:
                    json.dump(cfg, file, indent=4)

            except Exception as e:
                logger.error(f"Erro ao iniciar carregar arquivo \"config.json\". Tentando novamente em {timeout}s (tentativa {n_tentativa}/2). Exception: \"{repr(e)}\".")
                logger.debug(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando classes de conexão com Banco de Dados e Campo")

                db = Database()
                con = FieldConnector(cfg)

            except Exception as e:
                logger.error(f"Erro ao iniciar classes de conexão com Banco de Dados e Campo. Tentando novamente em {timeout}s (tentativa {n_tentativa}/2). Exception: \"{repr(e)}\".")
                logger.debug(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando classe da Usina.")

                usina = Usina(cfg, db)

            except Exception as e:
                logger.error(f"Erro ao iniciar classe da Usina. Tentando novamente em {timeout}s (tentativa {n_tentativa}/2). Exception: \"{repr(e)}\".")
                logger.debug(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando Thread de leitura periódica (30 min).")

                threading.Thread(target=lambda: leitura_temporizada()).start()

            except Exception as e:
                logger.error(f"Erro ao iniciar Thread de leitura periódica. Tentando novamente em {timeout}s (tentativa {n_tentativa}/2). Exception: \"{repr(e)}\".")
                logger.debug(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

    logger.info("Inicialização completa, executando o MOA \U0001F916")

    sm = StateMachine(initial_state=prox_estado(usina))
    while True:
        t_i = time.time()
        logger.debug("")
        logger.debug(f"Executando estado: \"{sm.state.__class__.__name__}\"")
        sm.exec()
        t_restante = max(30 - (time.time() - t_i), 0) / ESCALA_DE_TEMPO
        if t_restante == 0:
            logger.warning("\n\"ATENÇÃO!\"")
            logger.warning("O ciclo está demorando mais que o permitido!")
            logger.warning("\"ATENÇÃO!\"\n")
            sleep(t_restante)
