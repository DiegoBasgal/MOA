import logging
import traceback
import subprocess

import src.dicionarios.dict as d

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class ClientesUsina:

    TDA_Offline = False

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
        if not cls.ping(d.ips["TDA_slave_ip"]):
            cls.TDA_Offline = True
            if cls.TDA_Offline and cls.hb_borda_emerg_ping == 0:
                cls.hb_borda_emerg_ping = 1
                logger.critical("CLP TDA não respondeu a tentativa de comunicação!")

        elif cls.ping(d.ips["TDA_slave_ip"]) and cls.hb_borda_emerg_ping == 1:
            logger.info("Comunicação com o CLP TDA reestabelecida.")
            cls.hb_borda_emerg_ping = 0
            cls.TDA_Offline = False

        if not cls.ping(d.ips["USN_slave_ip"]):
            logger.critical("CLP SA não respondeu a tentativa de ping!")
        if cls.clp["SA"].open():
            cls.clp["SA"].close()
        else:
            logger.critical("CLP SA não respondeu a tentativa de conexão ModBus!")
            cls.clp["SA"].close()

        if not cls.ping(d.ips["MOA_slave_ip"]):
            logger.warning("CLP MOA não respondeu a tentativa de ping!")
        if cls.clp["MOA"].open():
            cls.clp["MOA"].close()
        else:
            logger.warning("CLP MOA não respondeu a tentativa de conexão ModBus!")

        """for ug in cls.ugs:
            if not cls.ping(d.ips[f"UG{ug.id}_slave_ip"]):
                logger.critical(f"CLP UG{ug.id} não respondeu a tentativa de ping!")
                ug.forcar_estado_manual()
            if cls.clp[f"UG{ug.id}"].open():
                cls.clp[f"UG{ug.id}"].close()
            else:
                ug.forcar_estado_manual()
                logger.critical(f"CLP UG{ug.id} não respondeu a tentativa de conexão ModBus!")"""


class ModBusClientFail(Exception):
    def __init__(cls, clp: ModbusClient = None, *args: object) -> None:
        super().__init__(*args)
        raise f"[CLI] Modbus client ({clp.host} : {clp.port}) failed to open."
