import logging
import traceback
import subprocess

import dicionarios.dict as d

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class ClientesUsina:

    clp: "dict[str, ModbusClient]"

    clp["SA"] = ModbusClient(
        host=d.ips["SA_ip"],
        port=d.ips["SA_porta"],
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
    """
    clp["MOA"] = ModbusClient(
        host=d.ips["MOA_ip"],
        port=d.ips["MOA_porta"],
        unit_id=1,
        timeout=0.5
    )
    """

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
        try:
            if not cls.ping(d.ips["SA_ip"]):
                logger.warning("[CLI] O CLP do Serviço Auxiliar não respondeu a tentativa de comunicação!")

            if not cls.ping(d.ips["UG1_ip"]):
                logger.warning("[CLI] O CLP da Unidade Geradora 1 não respondeu a tentativa de comunicação!")

            if not cls.ping(d.ips["UG2_ip"]):
                logger.warning("[CLI] O CLP da Unidade Geradora 2 não respondeu a tentativa de comunicação!")

            if not cls.ping(d.ips["MOA_ip"]):
                logger.warning("[CLI] O CLP do MOA não respondeu a tentativa de comunicação!")

        except Exception:
            logger.error(f"[CLI] Houve um erro ao enviar comando de ping dos clientes da usina.")
            logger.debug(f"[CLI] Traceback: {traceback.format_exc()}")


class ModBusClientFail(Exception):
    def __init__(self, clp: ModbusClient = None, *args: object) -> None:
        super().__init__(*args)
        raise f"[CLI] Modbus client ({clp.host} : {clp.port}) failed to open."
