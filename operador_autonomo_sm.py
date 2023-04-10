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
from time import sleep, time
from datetime import datetime

from src.codes import *
from src.maquinas_estado.moa import *

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


def leitura_temporizada():
    delay = 1800
    proxima_leitura = time() + delay
    logger.debug("Iniciando o timer de leitura por hora.")
    while True:
        logger.debug("Inciando nova leitura...")
        try:
            if usina.leituras_por_hora() and usina.acionar_voip:
                acionar_voip()
            for ug in usina.ugs:
                if ug.leituras_por_hora() and ug.acionar_voip:
                    acionar_voip()
            sleep(max(0, proxima_leitura - time()))

        except Exception:
            logger.debug("Houve um problema ao executar a leitura por hora")

        proxima_leitura += (time() - proxima_leitura) // delay * delay + delay

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
                logger.debug(f"Traceback: {print(e)}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando classes de conexão com Banco de Dados e Campo")

                db = Database()
                con = FieldConnector(cfg)

            except Exception as e:
                logger.error(f"Erro ao iniciar classes de conexão com Banco de Dados e Campo. Tentando novamente em {timeout}s (tentativa {n_tentativa}/2). Exception: \"{repr(e)}\".")
                logger.debug(f"Traceback: {print(e)}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando classe da Usina.")

                usina = Usina(cfg, db)

            except Exception as e:
                logger.error(f"Erro ao iniciar classe da Usina. Tentando novamente em {timeout}s (tentativa {n_tentativa}/2). Exception: \"{repr(e)}\".")
                logger.debug(f"Traceback: {print(e)}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando Thread de leitura periódica (30 min).")

                threading.Thread(target=lambda: leitura_temporizada()).start()

            except Exception as e:
                logger.error(f"Erro ao iniciar Thread de leitura periódica. Tentando novamente em {timeout}s (tentativa {n_tentativa}/2). Exception: \"{repr(e)}\".")
                logger.debug(f"Traceback: {print(e)}")
                sleep(timeout)
                continue

    logger.info("Inicialização completa, executando o MOA \U0001F916")

    prox_estado = Pronto
    sm = StateMachine(initial_state=prox_estado(usina))

    while True:
        try:
            t_i = time()
            logger.debug("")
            logger.debug(f"Executando estado: \"{sm.state.__class__.__name__}\"")
            sm.exec()
            t_restante = max(30 - (time() - t_i), 0) / ESCALA_DE_TEMPO
            if t_restante == 0:
                logger.warning("\n\"ATENÇÃO!\"")
                logger.warning("O ciclo está demorando mais que o permitido!")
                logger.warning("\"ATENÇÃO!\"\n")
                sleep(t_restante)
        except Exception as e:
            logger.debug(f"Houve um erro no loop principal. Exception: \"{repr(e)}\"")
