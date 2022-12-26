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
from src.UnidadeDeGeracao import StateManual
from threading import Thread

import src.database_connector as database_connector
import src.abstracao_usina as abstracao_usina
from src.codes import *

# Set-up logging
from src.mensageiro.mensageiro_log_handler import MensageiroHandler
rootLogger = logging.getLogger()
if (rootLogger.hasHandlers()):
    rootLogger.handlers.clear()
rootLogger.setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()
logger.setLevel(logging.NOTSET)

if not os.path.exists(os.path.join(os.path.dirname(__file__),"logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__),"logs"))
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [MOA-SM] %(message)s")
logFormatterSimples = logging.Formatter("[%(levelname)-5.5s] %(message)s")

ch = logging.StreamHandler(stderr)  # log para sdtout
ch.setFormatter(logFormatter)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

fh = handlers.TimedRotatingFileHandler(os.path.join(os.path.dirname(__file__),"logs","MOA.log"), when='midnight', interval=1, backupCount=7)  # log para arquivo
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
            logger.warning("Estado ({}) levantou uma exception: {}".format(self.state, repr(e)))
            logger.warning("Traceback: {}".format(traceback.format_exc()))
            self.em_falha_critica = True
            self.state = FalhaCritica()


class State:

    def __init__(self, *args, **kwargs):
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

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_tentativa = 0
        self.usina = instancia_usina
        self.usina.state_moa = 3

    def run(self):

        if self.n_tentativa >= 2:
            return FalhaCritica()
        else:

            try:
                self.usina.ler_valores()
                return ValoresInternosAtualizados(self.usina)

            except Exception as e:
                self.n_tentativa += 1
                logger.error("Erro durante a comunicação do MOA com a usina. Tentando novamente em {}s (tentativa{}/3)."
                             " Exception: {}.".format(self.usina.cfg["timeout_padrao"] * self.n_tentativa, self.n_tentativa, repr(e)))
                logger.critical("Traceback: {}".format(traceback.format_exc()))
                sleep(self.usina.cfg["timeout_padrao"] * self.n_tentativa)
                return self


class ValoresInternosAtualizados(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina
        DataBank.set_words(self.usina.cfg['REG_PAINEL_LIDO'], [1])
        self.habilitar_emerg_condic_c=False

    def run(self):
        """Decidir para qual modo de operação o sistema deve ir"""

        """
        Aqui a ordem do checks importa, e muito.
        """
        global aux
        global deve_normalizar

        # atualizar arquivo das configurações
        with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'w') as file:
            json.dump(self.usina.cfg, file)

        if self.usina.avisado_em_eletrica:
            for condicionador in self.usina.condicionadores:
                if condicionador.ativo and condicionador.gravidade >= DEVE_INDISPONIBILIZAR:
                    self.habilitar_emerg_condic_c=True
                elif condicionador.ativo and condicionador.gravidade == DEVE_NORMALIZAR:
                    self.habilitar_emerg_condic_c=False
                    deve_normalizar=True
                else:
                    deve_normalizar=False
                    self.habilitar_emerg_condic_c=False
            
            if self.habilitar_emerg_condic_c:
                logger.info("Condicionadores ativos com gravidade alta!")
                return Emergencia(self.usina)

        if deve_normalizar:
            if (not self.usina.normalizar_emergencia()) and self.usina.tensao_ok==False and aux==0:
                logger.warning("Tensão da linha fora do limite ")
                aux = 1
                Thread(target=lambda: self.usina.aguardar_tensao(600)).start()

            elif self.usina.timer_tensao:
                aux = 0
                deve_normalizar = None
                self.usina.timer_tensao = None

            elif self.usina.timer_tensao==False:
                aux = 0
                deve_normalizar = None
                self.usina.timer_tensao = None
                logger.critical("O tempo de normalização da linha excedeu o limite! (10 min)")
                return Emergencia(self.usina)

        if self.usina.clp_emergencia_acionada:
            return Emergencia(self.usina)

        if self.usina.db_emergencia_acionada:
            return Emergencia(self.usina)

        # Verificamos se existem agendamentos
        if len(self.usina.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes(self.usina)

         # Em seguida com o modo manual (não autonomo)
        if not self.usina.modo_autonomo:
            return ModoManualAtivado(self.usina)

        # Se não foi redirecionado ainda,
        # assume-se que o MOA deve executar de modo autônomo

        for ug in self.usina.ugs:
            ug.step()

        # Verifica-se então a situação do reservatório
        if self.usina.aguardando_reservatorio:
            if self.usina.nv_montante > self.usina.cfg["nv_alvo"]:
                logger.info("Reservatorio dentro do nivel de trabalho")
                self.usina.aguardando_reservatorio = 0
            return Pronto(self.usina)

        if self.usina.nv_montante < self.usina.cfg["nv_minimo"]:
            self.usina.aguardando_reservatorio = 1
            logger.info("Reservatorio abaixo do nivel de trabalho")
            return ReservatorioAbaixoDoMinimo(self.usina)

        if self.usina.nv_montante >= self.usina.cfg["nv_maximo"]: 
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
        self.usina.escrever_valores()
        self.usina.heartbeat()
        self.nao_ligou = True

    def run(self):
        self.usina.heartbeat()
        self.n_tentativa += 1
        if self.n_tentativa > 2:
            logger.warning("Numero de tentaivas de normalização excedidas, entrando em modo manual.")
            self.usina.entrar_em_modo_manual()
            self.usina.heartbeat()
            for ug in self.usina.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()
            return ModoManualAtivado(self.usina)
        else:
            if self.usina.db_emergencia_acionada:
                logger.info("Emergencia acionada via Django/DB, aguardando Reset/Reco pela interface web ou pelo CLP")
                while self.usina.db_emergencia_acionada:
                    self.usina.ler_valores()
                    if not self.usina.clp.em_emergencia():
                        self.usina.db.update_emergencia(0)
                        self.usina.db_emergencia_acionada = 0


            self.usina.ler_valores()
            # Ler condiconadores
            deve_indisponibilizar = False
            deve_normalizar = False
            deve_super_normalizar = False
            condicionadores_ativos = []
            for condicionador in self.usina.condicionadores:
                if condicionador.ativo:
                    if condicionador.gravidade == DEVE_INDISPONIBILIZAR:
                        condicionadores_ativos.append(condicionador)
                        deve_indisponibilizar = True
                    elif condicionador.gravidade == DEVE_NORMALIZAR:
                        condicionadores_ativos.append(condicionador)
                        deve_normalizar = True
                    elif condicionador.gravidade == DEVE_SUPER_NORMALIZAR:
                        condicionadores_ativos.append(condicionador)
                        deve_super_normalizar = True
                        
            if deve_super_normalizar:
                deve_indisponibilizar = False
                deve_normalizar = True
                
            if self.usina.clp_emergencia_acionada or deve_normalizar or deve_indisponibilizar:
                try:
                   
                    # Se algum condicionador deve gerar uma indisponibilidade
                    if deve_indisponibilizar:
                        # Logar os condicionadores ativos
                        logger.critical(
                            "[USN] USN detectou condicionadores ativos, passando USINA para manual e ligando por VOIP.\nCondicionadores ativos:\n{}".format(
                                [d.descr for d in condicionadores_ativos]
                            )
                        )
                        # Vai para o estado StateIndisponivel
                        self.usina.entrar_em_modo_manual()
                        return ModoManualAtivado(self.usina)
                    
                    elif deve_normalizar:
                        logger.debug("Bela adormecida 5s")
                        sleep(5)
                        logger.info("Normalizando usina. (tentativa{}/2) (limite entre tentaivas: {}s)"
                                .format(self.n_tentativa, self.usina.cfg['timeout_normalizacao']))
                        self.usina.normalizar_emergencia()
                        self.usina.ler_valores()
                        return self    

                    else:
                        logger.debug("Nenhum condicionador relevante ativo...")
                        self.usina.ler_valores()
                        return ControleRealizado(self.usina)
                   
                except Exception as e:
                    logger.error("Erro durante a comunicação do MOA com a usina. Exception: {}.".format(repr(e)))
                    logger.critical("Traceback: {}".format(traceback.format_exc()))
                return self
            else:
                self.usina.ler_valores()
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

        if len(self.usina.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes(self.usina)
        
        return self


class AgendamentosPendentes(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        logger.debug("Tratando agendamentos")
        self.usina.verificar_agendamentos()
        return Pronto(self.usina)


class ReservatorioAbaixoDoMinimo(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        self.usina.distribuir_potencia(0)
        if self.usina.nv_montante_recente <= self.usina.cfg["nv_fundo_reservatorio"]:
            logger.critical("Nivel montante ({:3.2f}) atingiu o fundo do reservatorio!".format(self.usina.nv_montante_recente))
            return Emergencia(self.usina)
        return ControleRealizado(self.usina)


class ReservatorioAcimaDoMaximo(State):

    def __init__(self, instancia_usina, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usina = instancia_usina

    def run(self):
        if self.usina.nv_montante_recente >= self.usina.cfg["nv_maximorum"]:
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

def leitura_temporizada():
    delay = 1800
    proxima_leitura = time.time() + delay
    while True:
        try:
            if usina.leituras_por_hora():
                acionar_voip()
                
            for ug in usina.ugs:
                ug.leituras_por_hora():
                    
        time.sleep(max(0, proxima_leitura - time.time()))
        except Exception:
            logger.debug("Houve um problema ao executar a leitura por hora")

        proxima_leitura += (time.time() - proxima_leitura) // delay * delay + delay

def acionar_voip():
    try:
        if usina.acionar_voip:
            voip.falha_abertura_comp = True if usina.falha_abertura_comp else False
            voip.falha_fechamento_comp = True if usina.falha_fechamento_comp else False
            voip.alarme_temp_oleo_trafo = True if usina.alarme_temp_oleo_trafo else False
            voip.alarme_temp_enrol_trafo = True if usina.alarme_temp_enrol_trafo else False
            voip.falha_part_grupo_diesel = True if usina.falha_part_grupo_diesel else False
            voip.falha_fechamento_DJ52L = True if usina.falha_fechamento_DJ52L else False
            voip.enviar_voz_auxiliar()
            usina.acionar_voip = False

        if usina.avisado_em_eletrica:
            voip.enviar_voz_emergencia()
            usina.acionar_voip = False

    except Exception:
        logger.warning("Houve um problema ao ligar por Voip")

if __name__ == "__main__":
    # A escala de tempo é utilizada para acelerar as simulações do sistema
    # Utilizar 1 para testes sérios e 120 no máximo para testes simples
    ESCALA_DE_TEMPO = 1
    if len(sys.argv) > 1:
        ESCALA_DE_TEMPO = int(sys.argv[1])

    aux = 0
    deve_normalizar = None
    n_tentativa = 0
    timeout = 10
    logger.info("Iniciando o MOA_SM ESCALA_DE_TEMPO:{}".format(ESCALA_DE_TEMPO))
    logger.debug("Debug is ON")

    prox_estado = 0
    usina = None
    while prox_estado == 0:
        n_tentativa += 1
        if n_tentativa > 2:
            prox_estado = FalhaCritica
        else:
            # carrega as configurações
            config_file = os.path.join(os.path.dirname(__file__), 'config.json')
            with open(config_file, 'r') as file:
                cfg = json.load(file)
                
            # bkp das configurações
            config_file = os.path.join(os.path.dirname(__file__), 'config.json.bkp')
            with open(config_file, 'w') as file:
                json.dump(cfg, file)

            # Inicia o conector do banco
            db = database_connector.Database()
            # Tenta iniciar a classe usina
            logger.debug("Iniciando classe Usina")
            try:
                usina = abstracao_usina.Usina(cfg, db)
                usina.aguardando_reservatorio = 0
            except Exception as e:
                logger.error(
                    "Erro ao iniciar Classe Usina. Tentando novamente em {}s (tentativa {}/2). Exception: {}.".format(
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
                    "Erro ao iniciar abstração da usina. Tentando novamente em {}s (tentativa {}/2). Exception: {}."
                    "".format(timeout, n_tentativa, repr(e)))
                logger.error("Traceback: {}".format(traceback.format_exc()))
                sleep(timeout)
            except ConnectionError as e:
                logger.error(
                    "Erro ao iniciar Modbus MOA. Tentando novamente em {}s (tentativa {}/2). Exception: {}.".format(
                        timeout, n_tentativa, repr(e)))
                logger.error("Traceback: {}".format(traceback.format_exc()))
                sleep(timeout)
            except PermissionError as e:
                logger.error("Não foi possível iniciar o Modbus MOA devido a permissão do usuário. Exception: {}.".format(repr(e)))
                logger.error("Traceback: {}".format(traceback.format_exc()))
                prox_estado = FalhaCritica
            except Exception as e:
                logger.error("Erro Inesperado. Tentando novamente em {}s (tentativa{}/2). Exception: {}.".format(
                    timeout, n_tentativa, repr(e)))
                logger.error("Traceback: {}".format(traceback.format_exc()))
                sleep(timeout)

    logger.info("Inicialização completa, executando o MOA \U0001F916")

    sm = StateMachine(initial_state=prox_estado(usina))
    while True:
        t_i = time.time()
        logger.debug("Executando estado: {}".format(sm.state.__class__.__name__))
        sm.exec()
        t_restante = max(5 - (time.time() - t_i), 0) / ESCALA_DE_TEMPO
        logger.debug("Tempo gasto no ciclo: {} s".format(float(time.time() - t_i)))
        if t_restante == 0:
            logger.debug("Ciclo está demorando mais que o permitido!")
        sleep(t_restante)
