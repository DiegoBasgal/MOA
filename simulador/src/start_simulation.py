import logging
import threading
from sys import stdout
import threading
import gui.gui as gui
import planta
import controlador

# Set-up logging
rootLogger = logging.getLogger()
if (rootLogger.hasHandlers()):
    rootLogger.handlers.clear()
rootLogger.setLevel(logging.NOTSET)
logger = logging.getLogger(__name__)

if (logger.hasHandlers()):
    logger.handlers.clear()
logger.setLevel(logging.NOTSET)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [SIMUL] %(message)s")

ch = logging.StreamHandler(stdout)  # log para sdtout
ch.setFormatter(logFormatter)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

fh = logging.FileHandler("MOA.log")  # log para arquivo
fh.setFormatter(logFormatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
# Fim Set-up logging

logger.info("Iniciando abstraço e GUI.")
shared_dict = {}
# 1 thread para simular o reservatorio
th_world = threading.Thread(target=planta.Planta(shared_dict).run, args=())
# 1 thread para interagir com a simulação
th_gui = threading.Thread(target=gui.start_gui, args=(shared_dict,))
# 1 thread para controlar e gravar a simulação
th_ctl = threading.Thread(target=controlador.Controlador(shared_dict).run, args=())

# Simular comportamento completo
th_world.start()
th_ctl.start()
th_gui.start()
logger.info("Rodando simul.".format())


th_gui.join()
th_world.join()
th_ctl.join()
logger.info("Fim da simul.")
