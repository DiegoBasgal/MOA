import logging
import traceback
import subprocess

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class ClpClients:
    def __init__(self, sd: dict=None) -> None:
        if not sd:
            logger.warning("[CLP] Houve um erro ao carregar o dicionário compartilhado.")
            raise ValueError
        else:
            self.dict = sd

        self.borda_ping: bool = False

        self.clp_dict: dict[str, ModbusClient] = {}

        self.clp_dict["clp_moa"] = ModbusClient(
            host=self.dict["IP"]["MOA_slave_ip"],
            port=self.dict["IP"]["MOA_slave_porta"],
            unit_id=1,
            timeout=0.5,
            auto_open=True,
            auto_close=True
        )
        self.clp_dict["clp_usn"] = ModbusClient(
            host=self.dict["IP"]["USN_slave_ip"],
            port=self.dict["IP"]["USN_slave_porta"],
            unit_id=1,
            timeout=0.5,
            auto_open=True,
            auto_close=True
        )
        self.clp_dict["clp_tda"] = ModbusClient(
            host=self.dict["IP"]["TDA_slave_ip"],
            port=self.dict["IP"]["TDA_slave_porta"],
            unit_id=1,
            timeout=0.5,
            auto_open=True,
            auto_close=True
        )
        self.clp_dict["clp_ug1"] = ModbusClient(
            host=self.dict["IP"]["UG1_slave_ip"],
            port=self.dict["IP"]["UG1_slave_porta"],
            unit_id=1,
            timeout=0.5,
            auto_open=True,
            auto_close=True
        )
        self.clp_dict["clp_ug2"] = ModbusClient(
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

    def ping_clps(self) -> None:
        try:
            if not self.ping(self.dict["IP"]["TDA_slave_ip"]):
                self.dict["GLB"]["tda_offline"] = True
                if self.dict["GLB"]["tda_offline"] and not self.borda_ping:
                    self.borda_ping = True
                    logger.warning("[CLP] CLP TDA não respondeu a tentativa de comunicação!")

            elif self.ping(self.dict["IP"]["TDA_slave_ip"]) and self.borda_ping:
                logger.info("[CLP] Comunicação com o CLP TDA reestabelecida.")
                self.borda_ping = False
                self.dict["GLB"]["tda_offline"] = False

            if not self.ping(self.dict["IP"]["USN_slave_ip"]):
                logger.warning("[CLP] CLP SA não respondeu a tentativa de comunicação!")

            if not self.ping(self.dict["IP"]["UG1_slave_ip"]):
                logger.warning("[CLP] CLP UG1 não respondeu a tentativa de comunicação!")

            if not self.ping(self.dict["IP"]["UG2_slave_ip"]):
                logger.warning("[CLP] CLP UG2 não respondeu a tentativa de comunicação!")

        except Exception as e:
            logger.exception(f"[CLP] Houve um erro ao executar o ping dos CLPs da usina. Exception: \"{repr(e)}\"")
            logger.exception(f"[CLP] Traceback: {traceback.print_stack}")

class ModBusClientFail(Exception):
    def __init__(self, clp: ModbusClient = None, *args: object) -> None:
        super().__init__(*args)
        raise f"[CLP] Modbus client ({clp.host} : {clp.port}) failed to open."
