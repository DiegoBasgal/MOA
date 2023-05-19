import logging
import traceback

import simulador.src.dicionarios.dict as d

from sys import stdout
from threading import Thread
from asyncio.log import logger

from simulador.src.dj52L import *
from simulador.src.planta import *
from simulador.src.unidade_geracao import *

from simulador.src.dicionarios.reg import *
from simulador.src.dicionarios.const import *

from simulador.src.gui.gui import start_gui
from simulador.src.temporizador import Temporizador

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

        shared_dict = d.shared_dict

    except Exception as e:
        logger.exception(f"Houve um erro ao abrir o dicionário compartilhado. Exception: \"{repr(e)}\"")
        logger.debug(f"Traceback: {traceback.format_exc()}")

    try:
        logger.info("Iniciando Thread do controlador de tempo da simulação.")

        time_handler = Temporizador(shared_dict)

    except Exception:
        logger.exception(f"Houve um erro ao iniciar a classe controladora de tempo. Exception: \"{repr(e)}\"")
        logger.debug(f"Traceback: {traceback.format_exc()}")

    try:
        logger.info("Instanciando classes da Usina (Ug, Dj52L, Planta)")

        dj52L = Dj52L(shared_dict, time_handler)

        ug1 = Ug(1, shared_dict, time_handler)
        ug2 = Ug(2, shared_dict, time_handler)
        ugs = [ug1, ug2]

    except Exception as e:
        logger.exception(f"Houve um erro ao instanciar as classes de UGs, Dj52L. Exception: \"{repr(e)}\"")
        logger.debug(f"Traceback: {traceback.format_exc()}")

    try:
        logger.info("Iniciando execução.")

        th_th = Thread(target = time_handler.run)
        th_usina = Thread(target = Planta(shared_dict, dj52L, ugs, time_handler).run)
        th_gui = Thread(target = start_gui, args=(shared_dict))

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
