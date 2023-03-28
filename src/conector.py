__version__ = "0.1"
__author__ = "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da conexão com servidore(s) e CLP(s)."


import logging
import traceback
import subprocess

from opcua import Client as OpcClient
from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class ClientsUsn:
    def __init__(self, dicionario: dict | None = ...) -> ...:
        if not dicionario:
            logger.warning("[CLN] Houve um erro ao carregar o dicionário compartilhado.")
            raise ValueError
        else:
            self.dict = dicionario

        self.borda_ping: bool = False

        self.opc_client = OpcClient(self.dict["IP"]["opc_server"])

        self.clp_moa = ModbusClient(
            host=self.dict["IP"]["MOA_slave_ip"],
            port=self.dict["IP"]["MOA_slave_porta"],
            unit_id=1,
            timeout=0.5,
            auto_open=True,
            auto_close=True
        )
        self.clp_ug1 = ModbusClient(
            host=self.dict["IP"]["UG1_slave_ip"],
            port=self.dict["IP"]["UG1_slave_porta"],
            unit_id=1,
            timeout=0.5,
            auto_open=True,
            auto_close=True
        )
        self.clp_ug2 = ModbusClient(
            host=self.dict["IP"]["UG2_slave_ip"],
            port=self.dict["IP"]["UG2_slave_porta"],
            unit_id=1,
            timeout=0.5,
            auto_open=True,
            auto_close=True
        )

        self.lista_clps = [self.clp_moa, self.clp_ug1, self.clp_ug2]

    def ping(self, host) -> bool:
        return [True if subprocess.call(["ping", "-c", "1", "-w", "1", host], stdout=subprocess.PIPE) == 0 else False for _ in range(2)]

    def open_all(self) -> None:
        logger.debug("[CLN] Iniciando conexões OPC e ModBus...")
        if not self.opc_client.connect():
            raise OpcClientFail(self.opc_client)

        for clp in self.lista_clps:
            raise ModBusClientFail(clp) if not clp.open() else ...
        logger.info("[CLN] Conexões inciadas.")

    def close_all(self) -> None:
        logger.debug("[CLN] Encerrando conexões...")
        self.opc_client.disconnect()
        [clp.close() for clp in self.lista_clps]
        logger.debug("[CLN] Conexões encerradas.")

    def ping_clients(self) -> None:
        try:
            if not self.ping(self.dict["IP"]["opc_server"]):
                logger.warning("[CLN][OPC] O servidor OPC não respondeu a tentativa de comunicação!")

            if not self.ping(self.dict["IP"]["MOA_slave_ip"]):
                logger.warning("[CLN][MB] CLP MOA não respondeu a tentativa de comunicação!")

            if not self.ping(self.dict["IP"]["UG1_slave_ip"]):
                logger.warning("[CLN][MB] CLP UG1 não respondeu a tentativa de comunicação!")

            if not self.ping(self.dict["IP"]["UG2_slave_ip"]):
                logger.warning("[CLN][MB] CLP UG2 não respondeu a tentativa de comunicação!")

        except Exception as e:
            logger.exception(f"[CLN] Houve um erro ao enviar comando de ping dos clientes da usina. Exception: \"{repr(e)}\"")
            logger.exception(f"[CLN] Traceback: {traceback.print_stack}")

class ModBusClientFail(Exception):
    def __init__(self, clp: ModbusClient | None = ..., *args: object) -> None:
        super().__init__(*args)
        raise f"[CLN][MB] Modbus client ({clp.host} : {clp.port}) failed to open."

class OpcClientFail(Exception):
    def __init__(self, opc_client: OpcClient | None = ..., *args: object) -> None:
        super().__init__(*args)
        raise f"[CLN][OPC] OPC client ({opc_client}) failed to open."
