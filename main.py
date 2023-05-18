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

from src.dicionarios.const import *
from src.maquinas_estado.moa import *

from src.usina import Usina
from src.banco_dados import Database
from src.mensageiro.mensageiro_log_handler import MensageiroHandler

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

ch = logging.StreamHandler(stderr)
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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ESCALA_DE_TEMPO = int(sys.argv[1])

    t_i = time()
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

                config_file = os.path.join(os.path.dirname('/opt/operacao-autonoma/src/dicionarios/'), "cfg.json")
                with open(config_file, "r") as file:
                    cfg = json.load(file)

            except Exception as e:
                logger.error(f"Erro ao iniciar carregar arquivo \"config.json\". Tentando novamente em {timeout}s (tentativa {n_tentativa}/2). Exception: \"{repr(e)}\".")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando classe de conexão com Banco de Dados")

                db = Database("moa")

            except Exception as e:
                logger.error(f"Erro ao iniciar classe de conexão com Banco de Dados. Tentando novamente em {timeout}s (tentativa {n_tentativa}/2). Exception: \"{repr(e)}\".")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando classe da Usina.")

                usina = Usina(cfg, db)

            except Exception as e:
                logger.error(f"Erro ao iniciar classe da Usina. Tentando novamente em {timeout}s (tentativa {n_tentativa}/2). Exception: \"{repr(e)}\".")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando Thread de leitura periódica (30 min).")

                threading.Thread(target=lambda: usina.leitura_periodica(delay=1800)).start()

            except Exception as e:
                logger.error(f"Erro ao iniciar Thread de leitura periódica. Tentando novamente em {timeout}s (tentativa {n_tentativa}/2). Exception: \"{repr(e)}\".")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(timeout)
                continue

            prox_estado = Pronto

    logger.info("Inicialização completa, executando o MOA \U0001F916")

    sm = StateMachine(initial_state=prox_estado(usina))

    while True:
        try:
            logger.debug("")
            logger.debug(f"Executando estado: \"{sm.state.__class__.__name__}\"")
            sm.exec()
            if usina._state_moa == MOA_SM_CONTROLE_DADOS:
                t_restante = max(TEMPO_CICLO_TOTAL - (time() - t_i), 0) / ESCALA_DE_TEMPO
                t_i = time()
            else:
                t_restante = 1

            if t_restante == 0:
                """logger.warning("\"ATENÇÃO!\"\n")
                logger.warning("O ciclo está demorando mais que o permitido!")
                logger.warning("\"ATENÇÃO!\"\n")"""
                pass
            else:
                sleep(t_restante)

        except Exception as e:
            logger.debug(f"Houve um erro no loop principal. Exception: \"{repr(e)}\"")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            usina.close_modbus()
