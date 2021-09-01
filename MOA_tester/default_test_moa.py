import json
import logging
import os
import subprocess
import traceback
from datetime import datetime
from sys import stdout
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
logger.setLevel(logging.DEBUG)
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

simulation_speed = 6

logger.info("[PRE] Setting world up for simulations ({}x real time).".format(simulation_speed))
# 1 thread para simular o reservatorio
th_world_abstraction = world_abstraction.world_abstraction(simulation_speed=simulation_speed)
th_world_abstraction.start()
# 1 thread para interagir com a simulação
th_simulation_interface = simulation_interface.simulation_interface()
th_simulation_interface.start()
logger.info("[PRE] World model and clp model is running.")

# Carrega o arquivo de configuração inicial
config_file = os.path.join('..', 'src', 'config.json')
with open(config_file, 'r') as file:
    temp_cfg = json.load(file)

# Executar testes
logger.info("[TEST] Running tests")
# Todo testes
# Comunicação modbus -> CLP ok?
try:
    modbus_client = ModbusClient(host=temp_cfg['clp_ip'], port=temp_cfg['clp_porta'], timeout=5, unit_id=1, auto_open=True, auto_close=True)
    if modbus_client.open():
        logger.debug("[TEST] Connect to Modbus slave on ({}:{}) PASSED".format(temp_cfg['clp_ip'], temp_cfg['clp_porta']))
    else:
        raise ConnectionError()
    modbus_client.close()
except Exception as e:
    logger.info("[TEST] Connect to Modbus slave on ({}:{}) FAILLED".format(temp_cfg['clp_ip'], temp_cfg['clp_porta']))
    logger.debug("[TEST] Fail caused by: {}".format(repr(e)))

# Modbus server liga ok?
try:
    modbus_server = ModbusServer(host=temp_cfg['moa_slave_ip'], port=temp_cfg['moa_slave_porta'], no_block=True)
    modbus_server.start()
    if modbus_server.is_run:
        logger.debug("[TEST] Opening Modbus slave on ({}:{}) PASSED".format(temp_cfg['moa_slave_ip'], temp_cfg['moa_slave_porta']))
    else:
        raise ConnectionError()
    modbus_server.stop()
except Exception as e:
    logger.info("[TEST] Opening Modbus slave on ({}:{}) FAILLED".format(temp_cfg['moa_slave_ip'], temp_cfg['moa_slave_porta']))
    logger.debug("[TEST] Fail caused by: {}".format(repr(e)))

# Comunicação -> DB local ok?
try:
    with Database() as db:
        db_conf = "{}@{}".format(db.config['user'], db.config['host'])
        res = db.query("SELECT NOW();")
        if res:
            logger.info("[TEST] Connect to Local Database on ({}) PASSED".format(db_conf))
        else:
            raise Exception("Query 'NOW()' returned '{}' ({}).".format(res, type(res)))
except Exception as e:
    logger.info("[TEST] Connect to Local Database on ({}) FAILLED".format(db_conf))
    logger.debug("[TEST] Fail caused by: {}".format(repr(e)))

# Comunicação -> Medidores ok?
logger.info("[TEST] Connect to medidores FAILLED (TEST NOT IMPLEMENTED)")

# Emergência aciona vars corretas?
# As entradas fisicas funcionam?
#   Se sim, gatilho de leitura dispara rotina de leitura?
#   Habilita/Desabilita MOA conforme painel?
# Maquinas bloqueiam quando ordenado?
#   Pelo CLP
#   Pelo contato eletrico
#
# Comporta ok?
# Prioridades das ugs ok?
# Agendamentos ok?
#   Verifica anteriores e trata?
#   Verifica atual e executa?
#   Verifica futuro e sabe?

logger.info("[TEST] Finished running tests")

# Simular comportamento completo
logger.info("[SIMUL] Running operador_autonomo_sm ({}x real time)".format(simulation_speed))
try:
    # Inicia o MOA
    subprocess.Popen(['python', '../src/operador_autonomo_sm.py', '{}'.format(simulation_speed)])

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

