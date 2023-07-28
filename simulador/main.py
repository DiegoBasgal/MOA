import logging
import traceback

from threading import Thread
from logging.config import fileConfig

from se import *
from ug import *
from simulador.cf import *

from gui.ui import start_gui
from simulador.funcoes.temporizador import Temporizador

fileConfig("/opt/operacao-autonoma/logger_cfg.ini")
logger = logging.getLogger("sim_logger")

if __name__ == '__main__':

    logger.info("Iniciando Simulação...")

    try:
        logger.info("Iniciando Thread do controlador de tempo da simulação")

        tempo = Temporizador()

    except Exception:
        logger.error(f"Houve um erro ao iniciar a classe controladora de tempo.")
        logger.error(f"Traceback: {traceback.format_exc()}")

    try:
        logger.debug("Instanciando classes da Usina (UGs, Dj52L, Planta)")

        dj52L = Dj52L(tempo)

        ug1 = UG(1, tempo)
        ug2 = UG(2, tempo)

        ugs = [ug1, ug2]

    except Exception:
        logger.error(f"Houve um erro ao instanciar as classes de UGs, Dj52L.")
        logger.error(f"Traceback: {traceback.format_exc()}")

    try:
        logger.info("Iniciando execução.")

        thread_temporizador = Thread(target = tempo.run, args=())

        thread_usina = Thread(target = Planta(dj52L, ugs, tempo).run, args=())

        thread_gui = Thread(target = start_gui, args=())

        # thread_controlador = threading.Thread(target=controlador.Controlador(dct.compartilhado).run, args=())

        logger.info("Rodando simulador...")
        thread_temporizador.start()
        thread_usina.start()
        thread_gui.start()
        # thread_controlador.start()


        thread_temporizador.join()
        thread_usina.join()
        thread_gui.join()
        # thread_controlador.join()

        logger.info("Fim da simulação.")

    except Exception:
        logger.error(f"Houve um erro ao iniciar as Threads de excução do simulador.")
        logger.error(f"Traceback: {traceback.format_exc()}")
