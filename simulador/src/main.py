import logging
import threading

import planta
import controlador
import gui.gui as gui

from sys import stdout

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

fh = logging.FileHandler("MOA.log")
fh.setFormatter(logFormatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

logger.info("Iniciando abstraço e GUI.")
shared_dict = {}

th_gui = threading.Thread(target=gui.start_gui, args=(shared_dict))
th_world = threading.Thread(target=planta.Planta(shared_dict).run, args=())
# th_ctl = threading.Thread(target=controlador.Controlador(shared_dict).run, args=())

th_gui.start()
th_world.start()
# th_ctl.start()
logger.info("Rodando simulador")

th_gui.join()
th_world.join()
# th_ctl.join()
logger.info("Fim da simulação")
