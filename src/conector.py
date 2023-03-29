__version__ = "0.1"
__author__ = "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da conexão com servidore(s) e CLP(s)."


import logging
import traceback
import subprocess

from opcua import Client as OpcClient
from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class ClientesUsina:
    def __init__(self, d_comp: dict[str, dict[str, any]] | None = ...) -> ...:
        if not d_comp:
            logger.warning("[CLI] Houve um erro ao carregar o dicionário compartilhado.")
            raise ValueError
        else:
            self.dict = d_comp

        self.borda_ping: bool = False

        self.cliente_opc: OpcClient = OpcClient(self.dict["IP"]["opc_server"])
        self.clp: dict[str, ModbusClient] = {}

        self.clp["MOA"] = ModbusClient(
            host=self.dict["IP"]["MOA_slave_ip"],
            port=self.dict["IP"]["MOA_slave_porta"],
            unit_id=1,
            timeout=0.5,
            auto_open=True,
            auto_close=True
        )
        self.clp["UG1"] = ModbusClient(
            host=self.dict["IP"]["UG1_slave_ip"],
            port=self.dict["IP"]["UG1_slave_porta"],
            unit_id=1,
            timeout=0.5,
            auto_open=True,
            auto_close=True
        )
        self.clp["UG2"]= ModbusClient(
            host=self.dict["IP"]["UG2_slave_ip"],
            port=self.dict["IP"]["UG2_slave_porta"],
            unit_id=1,
            timeout=0.5,
            auto_open=True,
            auto_close=True
        )

    def ping(self, host) -> bool:
        return [True if subprocess.call(["ping", "-c", "1", "-w", "1", host], stdout=subprocess.PIPE) == 0 else False for _ in range(2)]

    def open_all(self) -> None:
        logger.debug("[CLI] Iniciando conexões OPC e ModBus...")
        if not self.cliente_opc.connect():
            raise OpcClientFail(self.cliente_opc)

        for _ , clp in self.clp.items():
            raise ModBusClientFail(clp) if not clp.open() else ...
        logger.info("[CLI] Conexões inciadas.")

    def close_all(self) -> None:
        logger.debug("[CLI] Encerrando conexões...")
        self.cliente_opc.disconnect()
        [clp.close() for _ , clp in self.clp.items()]
        logger.debug("[CLI] Conexões encerradas.")

    def ping_clients(self) -> None:
        try:
            if not self.ping(self.dict["IP"]["opc_server"]):
                logger.warning("[CLI][OPC] O servidor OPC não respondeu a tentativa de comunicação!")

            if not self.ping(self.dict["IP"]["MOA_slave_ip"]):
                logger.warning("[CLI][MB] CLP MOA não respondeu a tentativa de comunicação!")

            if not self.ping(self.dict["IP"]["UG1_slave_ip"]):
                logger.warning("[CLI][MB] CLP UG1 não respondeu a tentativa de comunicação!")

            if not self.ping(self.dict["IP"]["UG2_slave_ip"]):
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
