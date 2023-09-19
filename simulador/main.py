import sys
import logging
import threading
import traceback

from logging.config import fileConfig
from pyModbusTCP.server import ModbusServer, DataBank

import usn as usn
import gui.gui as gui
import funcs.controlador as controlador

from dicts.regs import REG
from dicts.dict import compartilhado
from funcs.temporizador import Temporizador


fileConfig("/opt/operacao-autonoma/logger_config.ini")
logger = logging.getLogger("sim")


if __name__ == '__main__':

    logger.debug("Iniciando Simulação...")

    try:
        logger.debug("Iniciando Servidor Modbus...")
        sim_db = DataBank()

        server = ModbusServer(host="localhost", port=5003, no_block=True)
        server.start()

        for R in REG:
            sim_db.set_words(int(REG[R]), [0])

    except Exception:
        logger.debug(f"Houve um erro ao iniciar o Servidor Modbus.")
        logger.debug(traceback.format_exc())


    try:
        logger.debug("Iniciando Classe controladora de Tempo da Simulação...")

        tempo = Temporizador(compartilhado, 60, 0.1, 0.001)

    except Exception:
        logger.debug(f"Houve um erro ao iniciar a Classe controladora de Tempo.")
        logger.debug(traceback.format_exc())


    try:
        logger.debug("Iniciando Execução...")

        thread_temporizador = threading.Thread(target = tempo.run, args=())
        thread_usina = threading.Thread(target = usn.Usn(compartilhado, sim_db, tempo).run, args=())
        thread_gui = threading.Thread(target = gui.start_gui, args=(compartilhado,))
        # thread_controlador = threading.Thread(target=controlador.Controlador(compartilhado).run, args=())

        logger.debug("Rodando Simulador...")
        thread_temporizador.start()
        thread_usina.start()
        thread_gui.start()
        # thread_controlador.start()

        thread_temporizador.join()
        thread_usina.join()
        thread_gui.join()
        # thread_controlador.join()

        logger.debug("Fim da Simulação.")

        sys.exit(0)

    except Exception or KeyboardInterrupt:
        sys.exit(1)
        logger.debug(f"Houve um erro ao iniciar as Threads de excução do Simulador.")
        logger.debug(traceback.format_exc())
