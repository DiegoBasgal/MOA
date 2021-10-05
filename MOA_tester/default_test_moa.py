import json
import logging
import os
import subprocess
import traceback
from datetime import datetime
from sys import stdout
from time import sleep

from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import ModbusServer

from src.mensageiro.mensageiro_log_handler import MensageiroHandler
import world_abstraction
import simulation_interface
from src.database_connector import Database

# SILENCIANDO O LOOGER ROOT
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.CRITICAL)
# Inicializando o logger principal
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not os.path.exists("logs/"):
    os.mkdir("logs/")
if not os.path.exists("logs/imgs/"):
    os.mkdir("logs/imgs/")
fh = logging.FileHandler("logs/{}-test.log".format(datetime.now().strftime("%Y-%m-%d %H:%M")))  # log para arquivo
ch = logging.StreamHandler(stdout)  # log para linha de comando
mh = MensageiroHandler()  # log para telegram e voip
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s")
logFormatterSimples = logging.Formatter("[%(levelname)-5.5s] %(message)s")
fh.setFormatter(logFormatter)
ch.setFormatter(logFormatter)
mh.setFormatter(logFormatterSimples)
fh.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)
mh.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(mh)

simulation_speed = 600

logger.info("[PRE] Setting world up for simulations ({}x real time).".format(simulation_speed))
# 1 thread para simular o reservatorio
th_world_abstraction = world_abstraction.world_abstraction(simulation_speed=simulation_speed)
# 1 thread para interagir com a simulação
th_simulation_interface = simulation_interface.simulation_interface()

# Simular comportamento completo
logger.info("[SIMUL] Running operador_autonomo_sm ({}x real time)".format(simulation_speed))
try:
    # Inicia o MOA
    subprocess.Popen(['python', '../src/operador_autonomo_sm.py', '{}'.format(simulation_speed)])
    if not th_world_abstraction.is_alive():
        th_world_abstraction.start()
    if not th_simulation_interface.is_alive():
        th_simulation_interface.start()
    # Join e sair
    th_world_abstraction.join()
    th_simulation_interface.join()

except KeyboardInterrupt:
    logger.info("[SIMUL] Soft stopping simulation (user command)")
    th_world_abstraction.stop()
    th_simulation_interface.stop()
    th_world_abstraction.join()
    th_simulation_interface.join()

except Exception as e:
    logger.error("[SIMUL] Rrror during simulation:\n{}".format(traceback.format_exc()))

finally:
    logger.info("[SIMUL] Finished full run simulation")

