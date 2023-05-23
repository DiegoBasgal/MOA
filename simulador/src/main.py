import logging
import traceback
import dicionarios.dict as d

from sys import stdout
from threading import Thread

from dj52L import Dj52L
from planta import Planta
from ug import Ug

from dicionarios.reg import *
from dicionarios.const import *

from gui.gui import start_gui
from temporizador import Temporizador

rootLogger = logging.getLogger()
if rootLogger.hasHandlers():
    rootLogger.handlers.clear()
rootLogger.setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)
if logger.hasHandlers():
    logger.handlers.clear()
logger.setLevel(logging.NOTSET)

ch = logging.StreamHandler(stdout)
ch.setFormatter(logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [SIMUL] %(message)s"))
ch.setLevel(logging.INFO)

logger.addHandler(ch)

if __name__ == "__main__":
    logger.info("Iniciando abstraço e GUI.")

    try:
        logger.info("Carregando dicionário compartilhado.")

        sd = d.shared_dict

    except Exception as e:
        logger.exception(f"Houve um erro ao abrir o dicionário compartilhado. Exception: \"{repr(e)}\"")
        logger.debug(f"Traceback: {traceback.format_exc()}")
    try:
        logger.info("Iniciando Thread do controlador de tempo da simulação.")

        time_handler = Temporizador(sd)

    except Exception as e:
        logger.exception(f"Houve um erro ao iniciar a classe controladora de tempo. Exception: \"{repr(e)}\"")
        logger.debug(f"Traceback: {traceback.format_exc()}")

    try:
        logger.info("Instanciando classes da Usina (Ug, Dj52L, Planta)")

        dj52L = Dj52L(sd, time_handler)

        ug1 = Ug(1, sd, time_handler)
        ug2 = Ug(2, sd, time_handler)
        ugs = [ug1, ug2]

    except Exception as e:
        logger.exception(f"Houve um erro ao instanciar as classes de UGs, Dj52L. Exception: \"{repr(e)}\"")
        logger.debug(f"Traceback: {traceback.format_exc()}")

    try:
        logger.info("Iniciando execução.")

        th_th = Thread(target = time_handler.run, args=())
        th_usina = Thread(target = Planta(sd, dj52L, ugs, time_handler).run, args=())
        th_gui = Thread(target = start_gui, args=(sd,))

        # th_ctl = threading.Thread(target=controlador.Controlador(shared_dict).run)

        th_th.start()
        th_usina.start()
        th_gui.start()
        # th_ctl.start()

        logger.info("Rodando simulador")

        th_th.join()
        th_usina.join()
        th_gui.join()
        # th_ctl.join()

        logger.info("Fim da simulação")

    except Exception as e:
        logger.exception(f"Houve um erro ao iniciar as Threads de excução do simulador. Exception: \"{repr(e)}\"")
        logger.debug(f"Traceback: {traceback.format_exc()}")
