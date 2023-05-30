"""
    Módulo de Operação Autônoma (MOA)
"""
__version__ = "2.0"
__status__ = "Desenvolvimento"
__description__ = "Módulo de Operação Autônoma"

__maintainers__ = "Diego Basgal", "Henrique Pfeifer"
__emails__ = "diego.garcia@ritmoenergia.com.br", "henrique@ritmoenergia.com.br"

__authors__ = "Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal"
__credits__ = ["Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal", ...]


import os
import sys
import time
import json
import threading
import traceback

from sys import stderr
from logging import handlers
from time import time, sleep

from src.dicionarios.const import *
from src.maquinas_estado.moa import *

from src.clients import ClientesUsina

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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ESCALA_DE_TEMPO = int(sys.argv[1])

    t_i = time()
    t_restante = 1
    n_tentativa = 0
    executar = False
    prox_estado = None

    logger.debug("Debug is ON")
    logger.info("Iniciando MOA...")
    logger.debug(f"ESCALA_DE_TEMPO: {ESCALA_DE_TEMPO}")

    while not executar:
        n_tentativa += 1
        if n_tentativa == 3:
            prox_estado = FalhaCritica
        else:
            try:
                logger.info("Carregando arquivo de configuração.")

                arquivo = os.path.join(os.path.dirname("/opt/operacao-autonoma/src/dicionarios/"), "cfg.json")
                with open(arquivo, "r") as file:
                    cfg = json.load(file)

                arquivo = os.path.join(os.path.dirname("/opt/operacao-autonoma/src/dicionarios/"), "cfg.json.bkp")
                with open(arquivo, "w") as file:
                    json.dump(cfg, file, indent=4)

            except Exception:
                logger.exception(f"Erro ao carregar arquivo de configuração. Tentando novamente em \"{TIMEOUT_MAIN}s\" (Tentativa: {n_tentativa}/3).")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(TIMEOUT_MAIN)
                continue

            try:
                logger.info("Iniciando conexões com o servidores \"Modbus\".")

                ClientesUsina.open_all()

            except Exception:
                logger.exception(f"Erro ao iniciar classes de conexão com servidores. Tentando novamente em \"{TIMEOUT_MAIN}s\" (Tentativa: {n_tentativa}/3).")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(TIMEOUT_MAIN)
                continue

            try:
                logger.info("Iniciando instância da classe Usina.")
                usn: Usina = Usina(cfg)

            except Exception:
                logger.exception(f"Erro ao instanciar a classe Usina. Tentando novamente em \"{TIMEOUT_MAIN}s\" (Tentativa: {n_tentativa}/3).")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(TIMEOUT_MAIN)
                continue

            try:
                logger.info("Finalizando inicialização com intâncias da máquina de estados e Threads paralelas.")

                threading.Thread(target=lambda: usn.leitura_periodica()).start()
                sm = StateMachine(initial_state=Pronto(usn=usn))

                executar = True

            except Exception:
                logger.exception(f"Erro ao finalizar a incialização do MOA. Tentando novamente em \"{TIMEOUT_MAIN}s\" (Tentativa: {n_tentativa}/3).")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(TIMEOUT_MAIN)
                continue

    logger.info("Inicialização completa, executando o MOA \U0001F916")

    while True:
        try:
            logger.debug("")
            logger.debug(f"Executando estado: \"{sm.state.__class__.__name__}\"")
            sm.exec()

            if usn.estado_moa == MOA_SM_CONTROLE_DADOS:
                t_restante = max(TEMPO_CICLO_TOTAL - (time() - t_i), 0) / ESCALA_DE_TEMPO
                t_i = time()
            else:
                t_restante = 1

            if t_restante == 0:
                """logger.warning("\n\"ATENÇÃO!\"")
                logger.warning("O ciclo está demorando mais que o permitido!")
                logger.warning("\"ATENÇÃO!\"\n")"""
            else:
                sleep(t_restante)

        except Exception as e:
            logger.exception(f"Houve um erro na execução do loop principal da main do MOA. Exception: {repr(e)}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            ClientesUsina.close_all()
            break

        except KeyboardInterrupt:
            logger.warning("Execução do loop principal da main do MOA interrompido por comando de teclado.")
            ClientesUsina.close_all()
            break
