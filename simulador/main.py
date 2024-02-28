import sys
import logging
import traceback
import logging.handlers as handlers

import planta as p
import gui.gui as gui

from threading import Thread
from sys import stdout, stderr

from dicts.dict import compartilhado
from funcs.controlador import Controlador
from funcs.temporizador import Temporizador

rootLogger = logging.getLogger()
if (rootLogger.hasHandlers()):
    rootLogger.handlers.clear()
rootLogger.setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()
logger.setLevel(logging.NOTSET)

logFormatter = logging.Formatter("%(asctime)s [SIM] %(message)s")

ch = logging.StreamHandler(stderr)  # log para sdtout
ch.setFormatter(logFormatter)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

fh = handlers.TimedRotatingFileHandler(filename="C:/Users/cog/Documents/Diego/XAV/operacao-autonoma/simulador/logs/SIM.log", when='midnight', interval=1, backupCount=7)
fh.setFormatter(logFormatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


if __name__ == '__main__':

    logger.debug("Iniciando Simulação...")

    try:
        logger.debug("Iniciando Classe controladora de Tempo da Simulação...")

        tempo = Temporizador()

    except Exception:
        logger.debug(f"Houve um erro ao iniciar a Classe controladora de Tempo.")
        logger.debug(traceback.format_exc())

    try:
        logger.debug("Iniciando Execução...")

        thread_temporizador = Thread(target = tempo.run, args=())
        thread_usina = Thread(target = p.Planta(compartilhado, tempo).run, args=())
        thread_gui = Thread(target = gui.start_gui, args=(compartilhado,))
        thread_controlador = Thread(target=Controlador(compartilhado).run, args=())

        logger.debug("Rodando Simulador...")
        logger.debug('')
        thread_temporizador.start()
        thread_usina.start()
        thread_gui.start()
        thread_controlador.start()

        thread_temporizador.join()
        thread_usina.join()
        thread_gui.join()
        thread_controlador.join()

        logger.debug('')
        logger.debug("Fim da Simulação.")

        sys.exit(0)

    except Exception or KeyboardInterrupt:
        sys.exit(1)
        logger.debug(f"Houve um erro ao iniciar as Threads de excução do Simulador.")
        logger.debug(traceback.format_exc())