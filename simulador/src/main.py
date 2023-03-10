import os
import json
import logging
import threading
import traceback

from sys import stdout

from dj52L import *
from planta import *
from unidade_geracao import *
from gui.gui import start_gui

rootLogger = logging.getLogger()

if rootLogger.hasHandlers():
    rootLogger.handlers.clear()

rootLogger.setLevel(logging.NOTSET)
logger = logging.getLogger(__name__)

if logger.hasHandlers():
    logger.handlers.clear()

logger.setLevel(logging.NOTSET)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [SIMUL] %(message)s")

ch = logging.StreamHandler(stdout)
ch.setFormatter(logFormatter)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

fh = logging.FileHandler("Simulador.log")
fh.setFormatter(logFormatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

if __name__ == "__main__":
    logger.info("Iniciando abstraço e GUI.")
    logger.info("Carregando arquivo de configuração \"dict.json\".")

    try:
        config_file = os.path.join(os.path.dirname(__file__), "dict.json")
        with open(config_file, "r") as file:
            shared_dict = json.load(file)
    except Exception as e:
        logger.exception(f"Houve um erro ao abrir o dicionário compartilhado. Exception: \"{repr(e)}\"")
        logger.exception(f"Traceback:{traceback.print_stack}")

    try:
        ug1 = Ug(1, shared_dict)
        ug2 = Ug(2, shared_dict)
        ugs = [ug1, ug2]
        dj52L = Dj52L(shared_dict)
    except Exception as e:
        logger.exception(f"Houve um erro ao instanciar as classes de UGs e Dj52L. Exception: \"{repr(e)}\"")
        logger.exception(f"Traceback:{traceback.print_stack}")

    try:
        th_gui = threading.Thread(target = start_gui, args=(shared_dict))
        th_world = threading.Thread(target = Planta(shared_dict, dj52L, ugs).run, args=())
        # th_ctl = threading.Thread(target=controlador.Controlador(shared_dict).run, args=())
    except Exception as e:
        logger.exception(f"Houve um erro ao iniciar as Threads de excução do simulador. Exception: \"{repr(e)}\"")
        logger.exception(f"Traceback:{traceback.print_stack}")

    th_gui.start()
    th_world.start()
    # th_ctl.start()
    logger.info("Rodando simulador")

    th_gui.join()
    th_world.join()
    # th_ctl.join()
    logger.info("Fim da simulação")
