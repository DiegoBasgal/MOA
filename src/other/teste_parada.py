import json
import os
from pyModbusTCP.client import ModbusClient

# carrega as configurações
config_file = os.path.join(os.path.dirname(__file__), "..", "..", "config.json")
with open(config_file, "r") as file:
    cfg = json.load(file)

clp_ip = cfg["UG1_slave_ip"]
clp_port = cfg["UG1_slave_porta"]
clp = ModbusClient(
    host=clp_ip,
    port=clp_port,
    timeout=5,
    unit_id=1,
    auto_open=True,
    auto_close=True,
)

clp.write_single_register(12290, 1)