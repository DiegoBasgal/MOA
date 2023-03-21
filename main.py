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

import usina as usina
import conector as conector
import src.mensageiro.voip as voip

from sys import stderr
from time import sleep
from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.dict import *
from src.dicionarios.const import *
from src.maquinas_estado.moa_sm import *
from src.mensageiro.mensageiro_log_handler import MensageiroHandler

# Criar pasta para logs
if not os.path.exists(os.path.join(os.path.dirname(__file__), "logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

# Método para conversão de data/horário GMT:-03:00 (Brasil)
def timeConverter() -> datetime:
    tz = pytz.timezone("Brazil/East")
    return datetime.now(tz).timetuple()

# Método para criar logger principal
def criar_logger() -> logging:
    logger = logging.getLogger(__name__)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(logging.NOTSET)

    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [MOA-SM] %(message)s")
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

    return logger

# Método de leitura do arquivo de dados json
def leitura_json() -> dict:
    arquivo = os.path.join(os.path.dirname(__file__), "dados.json")
    with open(arquivo, "r") as file:
        return json.load(file)

# Método de escrever no arquivo de dados json após mudanças
def escrita_json(valor) -> None:
    arquivo = os.path.join(os.path.dirname(__file__), "dados.json")
    with open(arquivo, "w") as file:
        json.dump(valor, file, indent=4)

# Método de leitura por período
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
                ug.leituras_por_hora()
            time.sleep(max(0, proxima_leitura - time.time()))
            
        except Exception:
            logger.debug("Houve um problema ao executar a leitura por hora")

        proxima_leitura += (time.time() - proxima_leitura) // delay * delay + delay

# Método para acionamento voip
def acionar_voip():
    V_VARS = voip.VARS
    try:
        if usina.acionar_voip:
            for i, j in zip(voip, V_VARS):
                if i == j and VOIP[i]:
                    V_VARS[j][0] = VOIP[i]
            voip.enviar_voz_auxiliar()
            usina.acionar_voip = False

        elif usina.avisado_em_eletrica:
            voip.enviar_voz_emergencia()
            usina.avisado_em_eletrica = False

    except Exception:
        logger.warning("Houve um problema ao ligar por Voip")

if __name__ == "__main__":

    ESCALA_DE_TEMPO = 3
    if len(sys.argv) > 1:
        ESCALA_DE_TEMPO = int(sys.argv[1])
    
    logger = criar_logger()
    aux = 0
    deve_normalizar = None
    normalizacao_geral_teste = 0
    usina = None
    timeout = 10
    prox_estado = 0
    n_tentativa = 0

    logger.debug("Debug is ON")
    logger.info("Iniciando MOA...")
    logger.debug("Iniciando o MOA_SM ESCALA_DE_TEMPO:{}".format(ESCALA_DE_TEMPO))
    logger.debug("Inciando Threads de Leitura temporizada e acionamento por voip")

    while prox_estado == 0:
        n_tentativa += 1
        if n_tentativa > 2:
            prox_estado = FalhaCritica
        else:
            # carrega as configurações
            """
            config_file = os.path.join(os.path.dirname(__file__), "config.json")
            with open(config_file, "r") as file:
            """
            cfg = CFG # json.load(file)

            # bkp das configurações
            config_file = os.path.join(os.path.dirname(__file__), "config.json.bkp")
            with open(config_file, "w") as file:
                json.dump(cfg, file, indent=4)

            # Inicia o conector do banco
            db = conector.Database()
            # Tenta iniciar a classe usina
            logger.debug("Iniciando classe Usina")
            try:
                usina = usina.Usina(cfg, db)
                usina.ler_valores()
                usina.aguardando_reservatorio = 0
            except Exception as e:
                logger.error(
                    "Erro ao iniciar Classe Usina. Tentando novamente em {}s (tentativa {}/2). Exception: {}.".format(
                        timeout, n_tentativa, repr(e)
                    )
                )
                logger.debug("Traceback: {}".format(traceback.format_exc()))
                sleep(timeout)
                continue

            # Inicializando Servidor Modbus (para algumas comunicações com o Elipse)
            try:
                logger.debug("Iniciando Servidor/Slave Modbus MOA.")
                modbus_server = ModbusServer(
                    host=usina.cfg["moa_slave_ip"],
                    port=usina.cfg["moa_slave_porta"],
                    no_block=True,
                )
                modbus_server.start()
                sleep(1)
                if not modbus_server.is_run:
                    raise ConnectionError
                prox_estado = Pronto

            except TypeError as e:
                logger.error(
                    "Erro ao iniciar abstração da usina. Tentando novamente em {}s (tentativa {}/2). Exception: {}."
                    "".format(timeout, n_tentativa, repr(e))
                )
                logger.error("Traceback: {}".format(traceback.format_exc()))
                sleep(timeout)
            except ConnectionError as e:
                logger.error(
                    "Erro ao iniciar Modbus MOA. Tentando novamente em {}s (tentativa {}/2). Exception: {}.".format(
                        timeout, n_tentativa, repr(e)
                    )
                )
                logger.error("Traceback: {}".format(traceback.format_exc()))
                sleep(timeout)
            except PermissionError as e:
                logger.error(
                    "Não foi possível iniciar o Modbus MOA devido a permissão do usuário. Exception: {}.".format(
                        repr(e)
                    )
                )
                logger.error("Traceback: {}".format(traceback.format_exc()))
                prox_estado = FalhaCritica
            except Exception as e:
                logger.error(
                    "Erro Inesperado. Tentando novamente em {}s (tentativa{}/2). Exception: {}.".format(
                        timeout, n_tentativa, repr(e)
                    )
                )
                logger.error("Traceback: {}".format(traceback.format_exc()))
                sleep(timeout)

    logger.info("Inicialização completa, executando o MOA \U0001F916")

    threading.Thread(target=lambda: leitura_temporizada()).start()

    sm = StateMachine(initial_state=prox_estado(usina))
    while True:
        print("")
        t_i = time.time()
        logger.debug("Executando estado: {}".format(sm.state.__class__.__name__))
        sm.exec()
        t_restante = max(30 - (time.time() - t_i), 0) / ESCALA_DE_TEMPO
        if t_restante == 0:
            print("######################################################\n######################################################\nCiclo está demorando mais que o permitido\n######################################################\n######################################################")
        sleep(t_restante)
