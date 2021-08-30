import logging
import subprocess
import traceback
from datetime import datetime
from sys import stdout
from src.mensageiro.mensageiro_log_handler import MensageiroHandler
import world_abstraction
import simulation_interface
# SILENCIANDO O LOOGER ROOT
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.CRITICAL)
# Inicializando o logger principal
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("logs/{}-test.log".format(datetime.now().strftime("%Y-%m-%d %H:%M")))  # log para arquivo
ch = logging.StreamHandler(stdout)  # log para linha de comando
mh = MensageiroHandler()  # log para telegram e voip
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logFormatterSimples = logging.Formatter("[%(levelname)-5.5s]  %(message)s")
fh.setFormatter(logFormatter)
ch.setFormatter(logFormatter)
mh.setFormatter(logFormatterSimples)
fh.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)
mh.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(mh)

# Executar testes
logger.info("Running tests")
# Todo nehum teste definido ainda
logger.info("Finished running tests")

# Simular comportamento completo
simulation_speed = 60
logger.info("Running full run simulation ({}x real time)".format(simulation_speed))
try:
    # 1 thread para simular de facto
    th_world_abstraction = world_abstraction.world_abstraction(simulation_speed=simulation_speed)
    th_world_abstraction.start()

    # 1 thread para interagir com a simulação
    th_simulation_interface = simulation_interface.simulation_interface()
    th_simulation_interface.start()

    # Inicia o MOA
    subprocess.Popen(['python', '../src/operador_autonomo_sm.py', '{}'.format(simulation_speed)])

    # Join e sair
    th_world_abstraction.join()
    th_simulation_interface.join()

except KeyboardInterrupt:
    logger.info("Soft stopping simulation (user command)")
    th_world_abstraction.stop()
    th_simulation_interface.stop()
    th_world_abstraction.join()
    th_simulation_interface.join()

except Exception as e:
    logger.error("Error during simulation:\n{}".format(traceback.format_exc()))

finally:
    logger.info("Finished full run simulation")

