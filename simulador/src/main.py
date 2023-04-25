import logging
import traceback

from sys import stdout
from threading import Thread

import dicionarios.dict as d

from ug import *
from dj52L import *
from planta import *
from gui.ui import start_gui
from time_handler import TimeHandler

rootLogger = logging.getLogger()

if rootLogger.hasHandlers():
    rootLogger.handlers.clear()

rootLogger.setLevel(logging.NOTSET)
logger = logging.getLogger(__name__)

if logger.hasHandlers():
    logger.handlers.clear()

logger.setLevel(logging.NOTSET)
logFormatter = logging.Formatter('%(asctime)s [%(levelname)-5.5s] [SIM] %(message)s')

ch = logging.StreamHandler(stdout)
ch.setFormatter(logFormatter)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

fh = logging.FileHandler('Simulador.log')
fh.setFormatter(logFormatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

if __name__ == '__main__':
    logger.info('Iniciando abstraço e GUI.')

    try:
        shared_dict = d.shared_dict
    except Exception as e:
        logger.exception(f'Houve um erro ao abrir o dicionário compartilhado. Exception: \"{repr(e)}\"')
        logger.exception(f'Traceback:{traceback.print_stack}')

    try:
        logger.info('Iniciando Thread do controlador de tempo da simulação')
        time_handler = TimeHandler(shared_dict)
    except Exception:
        logger.exception(f'Houve um erro ao iniciar a classe controladora de tempo. Exception: \"{repr(e)}\"')
        logger.exception(f'Traceback:{traceback.print_stack}')

    try:
        logger.info('Instanciando classes da Usina (Ug, Dj52L, Planta)')
        dj52L = Dj52L(shared_dict, time_handler)
        ug1 = Ug(1, shared_dict, time_handler)
        ug2 = Ug(2, shared_dict, time_handler)
        ugs = [ug1, ug2]
    except Exception as e:
        logger.exception(f'Houve um erro ao instanciar as classes de UGs, Dj52L. Exception: \"{repr(e)}\"')
        logger.exception(f'Traceback:{traceback.print_stack}')

    try:
        logger.info('Iniciando execução.')
        th_th = Thread(target = time_handler.run, args=())
        th_usina = Thread(target = Planta(shared_dict, dj52L, ugs, time_handler).run, args=())
        th_gui = Thread(target = start_gui, args=(shared_dict,))
        # th_ctl = threading.Thread(target=controlador.Controlador(shared_dict).run, args=())

        th_th.start()
        th_usina.start()
        th_gui.start()
        # th_ctl.start()
        logger.info('Rodando simulador')

        th_th.join()
        th_usina.join()
        th_gui.join()
        # th_ctl.join()
        logger.info('Fim da simulação')
    except Exception as e:
        logger.exception(f'Houve um erro ao iniciar as Threads de excução do simulador. Exception: \"{repr(e)}\"')
        logger.exception(f'Traceback:{traceback.print_stack}')
