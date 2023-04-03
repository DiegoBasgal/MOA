__version__ = "0.1"
__author__ = "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da conexão com servidore(s) e CLP(s)."


import logging
import traceback
import subprocess

import dicionarios.dict as Dicionarios

from opcua import Client as OpcClient
from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class ClientesUsina:
    dict_ips = Dicionarios.ips

    opc: OpcClient = OpcClient(dict_ips["opc_server"])

    clp: dict[str, ModbusClient]

    clp["MOA"] = ModbusClient(
        host=dict_ips["MOA_slave_ip"],
        port=dict_ips["MOA_slave_porta"],
        unit_id=1,
        timeout=0.5,
        auto_open=True,
        auto_close=True
    )
    clp["UG1"] = ModbusClient(
        host=dict_ips["UG1_slave_ip"],
        port=dict_ips["UG1_slave_porta"],
        unit_id=1,
        timeout=0.5,
        auto_open=True,
        auto_close=True
    )
    clp["UG2"]= ModbusClient(
        host=dict_ips["UG2_slave_ip"],
        port=dict_ips["UG2_slave_porta"],
        unit_id=1,
        timeout=0.5,
        auto_open=True,
        auto_close=True
    )

    @staticmethod
    def ping(host) -> bool:
        return [True if subprocess.call(["ping", "-c", "1", "-w", "1", host], stdout=subprocess.PIPE) == 0 else False for _ in range(2)]

    def open_all(cls) -> None:
        logger.debug("[CLI] Iniciando conexões OPC e ModBus...")
        if not cls.opc.connect():
            raise OpcClientFail(cls.opc)

        for _ , clp in cls.clp.items():
            raise ModBusClientFail(clp) if not clp.open() else ...
        logger.info("[CLI] Conexões inciadas.")

    def close_all(cls) -> None:
        logger.debug("[CLI] Encerrando conexões...")
        cls.opc.disconnect()
        [clp.close() for _ , clp in cls.clp.items()]
        logger.debug("[CLI] Conexões encerradas.")

    def ping_clients(cls) -> None:
        try:
            if not cls.ping(cls.dict_ips["opc_server"]):
                logger.warning("[CLI][OPC] O servidor OPC não respondeu a tentativa de comunicação!")

            if not cls.ping(cls.dict_ips["MOA_slave_ip"]):
                logger.warning("[CLI][MB] CLP MOA não respondeu a tentativa de comunicação!")

            if not cls.ping(cls.dict_ips["UG1_slave_ip"]):
                logger.warning("[CLI][MB] CLP UG1 não respondeu a tentativa de comunicação!")

            if not cls.ping(cls.dict_ips["UG2_slave_ip"]):
                logger.warning("[CLI][MB] CLP UG2 não respondeu a tentativa de comunicação!")

        except Exception as e:
            logger.exception(f"[CLI] Houve um erro ao enviar comando de ping dos clientes da usina. Exception: \"{repr(e)}\"")
            logger.exception(f"[CLI] Traceback: {traceback.print_stack}")


class ModBusClientFail(Exception):
    def __init__(self, clp: ModbusClient | None = ..., *args: object) -> None:
        super().__init__(*args)
        raise f"[CLI] Modbus client ({clp.host} : {clp.port}) failed to open."

class OpcClientFail(Exception):
    def __init__(self, opc_client: OpcClient | None = ..., *args: object) -> None:
        super().__init__(*args)
        raise f"[CLI] OPC client ({opc_client}) failed to open."
