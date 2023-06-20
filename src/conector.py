import logging
import traceback
import subprocess

import src.dicionarios.dict as d

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class ClientesUsina:

    borda_ping: "bool" = False

    clp: "dict[str, ModbusClient]" = {}

    clp["SA"] = ModbusClient(
        host=d.ips["SA_ip"],
        port=d.ips["SA_porta"],
        unit_id=1,
        timeout=0.5
    )
    clp["TDA"] = ModbusClient(
        host=d.ips["TDA_ip"],
        port=d.ips["TDA_porta"],
        unit_id=1,
        timeout=0.5
    )
    clp["UG1"] = ModbusClient(
        host=d.ips["UG1_ip"],
        port=d.ips["UG1_porta"],
        unit_id=1,
        timeout=0.5
    )
    clp["UG2"] = ModbusClient(
        host=d.ips["UG2_ip"],
        port=d.ips["UG2_porta"],
        unit_id=1,
        timeout=0.5
    )
    clp["UG3"] = ModbusClient(
        host=d.ips["UG3_ip"],
        port=d.ips["UG3_porta"],
        unit_id=1,
        timeout=0.5
    )
    clp["MOA"] = ModbusClient(
        host=d.ips["MOA_ip"],
        port=d.ips["MOA_porta"],
        unit_id=1,
        timeout=0.5
    )

    @staticmethod
    def ping(host) -> bool:
        return True if (subprocess.call(["ping", "-c", "1", "-w", "1", host], stdout=subprocess.PIPE) == 0 for _ in range(2)) else False

    @classmethod
    def open_all(cls) -> None:
        logger.debug("[CLI] Iniciando conexões ModBus...")
        for _ , clp in cls.clp.items():
            if not clp.open():
                raise ModBusClientFail(clp)
        logger.info("[CLI] Conexões inciadas.")

    @classmethod
    def close_all(cls) -> None:
        logger.debug("[CLI] Encerrando conexões...")
        for _ , clp in cls.clp.items():
            clp.close()
        logger.debug("[CLI] Conexões encerradas.")

    @classmethod
    def ping_clients(cls) -> None:
        if not cls.ping(d.ips["TDA_ip"]):
            d.glb["TDA_Offline"] = True
            if d.glb["TDA_Offline"] and not cls.borda_ping:
                cls.borda_ping = True
                logger.critical("CLP TDA não respondeu a tentativa de comunicação!")

        elif cls.ping(d.ips["TDA_ip"]) and cls.borda_ping:
            logger.info("Comunicação com o CLP TDA reestabelecida.")
            cls.borda_ping = False
            d.glb["TDA_Offline"] = False

        if not cls.ping(d.ips["SA_ip"]):
            logger.critical("CLP SA não respondeu a tentativa de ping!")
        if cls.clp["SA"].open():
            cls.clp["SA"].close()
        else:
            logger.critical("CLP SA não respondeu a tentativa de conexão ModBus!")
            cls.clp["SA"].close()

        if not cls.ping(d.ips["UG1_ip"]):
            logger.warning("CLP UG1 não respondeu a tentativa de ping!")
        if cls.clp["UG1"].open():
            cls.clp["UG1"].close()
        else:
            logger.warning("CLP UG1 não respondeu a tentativa de conexão ModBus!")

        if not cls.ping(d.ips["UG2_ip"]):
            logger.warning("CLP UG2 não respondeu a tentativa de ping!")
        if cls.clp["UG2"].open():
            cls.clp["UG2"].close()
        else:
            logger.warning("CLP UG2 não respondeu a tentativa de conexão ModBus!")

        if not cls.ping(d.ips["UG3_ip"]):
            logger.warning("CLP UG3 não respondeu a tentativa de ping!")
        if cls.clp["UG3"].open():
            cls.clp["UG3"].close()
        else:
            logger.warning("CLP UG3 não respondeu a tentativa de conexão ModBus!")

        if not cls.ping(d.ips["MOA_ip"]):
            logger.warning("CLP MOA não respondeu a tentativa de ping!")
        if cls.clp["MOA"].open():
            cls.clp["MOA"].close()
        else:
            logger.warning("CLP MOA não respondeu a tentativa de conexão ModBus!")


class ModBusClientFail(Exception):
    def __init__(cls, clp: ModbusClient = None, *args: object) -> None:
        super().__init__(*args)
        raise f"[CLI] Modbus client ({clp.host} : {clp.port}) failed to open."
