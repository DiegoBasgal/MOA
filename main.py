import os
import sys
import time
import json
import logging
import traceback
import logging.handlers as handlers

import src.dicionarios.dict as d

from sys import stderr
from threading import Thread
from time import sleep, time

from src.usina import *
from src.clients import *
from src.conector import *
from src.ocorrencias import *
from src.agendamentos import *
from src.condicionadores import *
from src.dicionarios.const import *
from src.maquinas_estado.moa import *
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
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [MOA-SM] %(message)s")
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
)
fh.setFormatter(logFormatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

mh = MensageiroHandler()
mh.setFormatter(logFormatterSimples)
mh.setLevel(logging.INFO)
logger.addHandler(mh)

if __name__ == "__main__":
    timeout = 10
    prox_estado = 0
    n_tentativa = 0

    if len(sys.argv) > 1:
        ESCALA_DE_TEMPO = int(sys.argv[1])

    logger.info("Iniciando \"Módulo de Operação Autônoma (MOA)\"...")
    logger.debug(f"Escala de tempo -> \"{ESCALA_DE_TEMPO}\"")

    while prox_estado == 0:
        n_tentativa += 1

        if n_tentativa == 3:
            prox_estado = FalhaCritica
        else:
            try:
                logger.info("Carregando arquivos de configuração \"cfg.json\" e \"shared_dict\".")

                sd = d.shared_dict

                config_file = os.path.join(os.path.dirname(__file__), "cfg.json")
                with open(config_file, "r") as file:
                    cfg = json.load(file)

                config_file = os.path.join(os.path.dirname(__file__), "cfg.json.bkp")
                with open(config_file, "w") as file:
                    json.dump(cfg, file, indent=4)

            except Exception:
                logger.exception(f"Erro ao carregar arquivo de configuração e dicionário compartilhado. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando classe de conexão com os CLPs da usina.")

                clp = ClpClients(sd)
                clp.open_all()

            except Exception:
                logger.exception(f"Erro ao iniciar conexão com os CLPs da usina. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando classes de conexão com campo e banco de dados.")

                con = ConectorCampo(clp)
                db = ConectorBancoDados()

            except Exception:
                logger.exception(f"Erro ao iniciar classes de conexão. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando instâncias de classe Unidade de Geração.")

                ug1 = UnidadeDeGeracao(1, cfg, clp, con, db)
                ug2 = UnidadeDeGeracao(2, cfg, clp, con, db)
                ugs = [ug1, ug2]

                ug1.lista_ugs = ugs
                ug2.lista_ugs = ugs

                CondicionadorBase.ugs = ugs

            except Exception:
                logger.exception(f"Erro ao instanciar classes das Unidades de Geração. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando classe Ocorrências (Leitura de TRIPs e Alarmes).")

                oco = Ocorrencias(sd, clp, ugs)

            except Exception:
                logger.exception(f"Erro ao inciar classe Ocorrências. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando classe Usina.")

                usn = Usina(sd, cfg, clp, con, db, ugs, oco)

            except Exception:
                logger.exception(f"Erro ao iniciar classe Usina. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando classe Agendamentos.")

                agn = Agendamentos(cfg, db, usn, ugs)

            except Exception:
                logger.exception(f"Erro ao inciar classe Agendamentos. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando Thread de leitura temporizada.")

                th_lt = Thread(target=lambda: oco.leitura_periodica(1800)).start()

            except Exception:
                logger.exception(f"Erro ao iniciar Threads de leituras temporizadas e leituras de condicionadores. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Inciando máquina de estados do MOA.")

                State(sd, cfg, usn, agn, oco, db, ugs)
                sm = StateMachine(initial_state=Pronto())

            except Exception:
                logger.exception(f"Erro ao instanciar máquina de estados do MOA. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

    logger.info("Inicialização completa!") 
    logger.info("Executando o MOA \U0001F916")

    while True:
        try:
            logger.debug(f"Executando estado: \"{sm.state.__class__.__name__}\"")

            t_i = time()
            sm.exec()
            if usn.estado_moa == MOA_SM_CONTROLE_DADOS:
                t_restante = max(30 - (time() - t_i), 0) / ESCALA_DE_TEMPO

                if t_restante == 0:
                    logger.warning("\n\"ATENÇÃO!\"")
                    logger.warning("O ciclo está demorando mais que o permitido!")
                    logger.warning("\"ATENÇÃO!\"\n")
                sleep(t_restante)

        except Exception as e:
            logger.exception(f"Houve um erro na execução do loop principal da main do MOA. Exception: {repr(e)}")
            logger.exception(f"Traceback: {traceback.print_stack}")
            clp.close_all()
            break

        except KeyboardInterrupt:
            logger.warning("Execução do loop principal da main do MOA interrompido por comando de teclado.")
            clp.close_all()
            break