import logging

import dicionarios.dict as d

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class ClpClients:
    def __init__(self) -> None:
        self.dict = d.shared_dict

        self.clp_dict = {
            "clp_moa": ModbusClient(
                host=self.dict["IP"]["MOA_slave_ip"],
                port=self.dict["IP"]["MOA_slave_porta"],
                unit_id=1,
                timeout=0.5,
                auto_open=True,
                auto_close=True
            ),
            "clp_usn": ModbusClient(
                host=self.dict["IP"]["USN_slave_ip"],
                port=self.dict["IP"]["USN_slave_porta"],
                unit_id=1,
                timeout=0.5,
                auto_open=True,
                auto_close=True
            ),
            "clp_tda": ModbusClient(
                host=self.dict["IP"]["TDA_slave_ip"],
                port=self.dict["IP"]["TDA_slave_porta"],
                unit_id=1,
                timeout=0.5,
                auto_open=True,
                auto_close=True
            ),
            "clp_ug1": ModbusClient(
                host=self.dict["IP"]["UG1_slave_ip"],
                port=self.dict["IP"]["UG1_slave_porta"],
                unit_id=1,
                timeout=0.5,
                auto_open=True,
                auto_close=True
            ),
            "clp_ug2": ModbusClient(
                host=self.dict["IP"]["UG2_slave_ip"],
                port=self.dict["IP"]["UG2_slave_porta"],
                unit_id=1,
                timeout=0.5,
                auto_open=True,
                auto_close=True
            )
        }

    def open_all(self) -> None:
        logger.debug("[CLP] Iniciando conexões ModBus...")
        if not self.clp_dict["clp_moa"].open():
            raise ModBusClientFail(self.clp_dict["clp_moa"])
        if not self.clp_dict["clp_usn"].open():
            raise ModBusClientFail(self.clp_dict["clp_usn"])
        if not self.clp_dict["clp_tda"].open():
            raise ModBusClientFail(self.clp_dict["clp_tda"])
        if not self.clp_dict["clp_ug1"].open():
            raise ModBusClientFail(self.clp_dict["clp_ug1"])
        if not self.clp_dict["clp_ug2"].open():
            raise ModBusClientFail(self.clp_dict["clp_ug2"])
        logger.debug("[CLP] Conexão inciada.")

    def close_all(self) -> None:
        logger.debug("[CLP] Encerrando conexões ModBus...")
        self.clp_dict["clp_moa"].close()
        self.clp_dict["clp_usn"].close()
        self.clp_dict["clp_tda"].close()
        self.clp_dict["clp_ug1"].close()
        self.clp_dict["clp_ug2"].close()
        logger.debug("[CLP] Conexão encerrada.")


class ModBusClientFail(Exception):
    def __init__(self, clp: ModbusClient = None, *args: object) -> None:
        super().__init__(*args)
        raise f"[CLP] Modbus client ({clp.host} : {clp.port}) failed to open."
