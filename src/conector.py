__version__ = "0.1"
__author__ = "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da conexão com servidore(s), CLP(s) e RELÉ(s)."

import logging
import traceback
import subprocess

import dicionarios.dict as Dicionarios

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class ClientesUsina:
    dict_ips = Dicionarios.ips

    clp: dict[str, ModbusClient]
    rele: dict[str, ModbusClient]

    clp["SA"] = ModbusClient(
        host=dict_ips["SA_slave_ip"],
        port=dict_ips["SA_slave_porta"],
        unit_id=1,
        timeout=0.5
    )
    clp["TDA"] = ModbusClient(
        host=dict_ips["TDA_slave_ip"],
        port=dict_ips["TDA_slave_porta"],
        unit_id=1,
        timeout=0.5
    )
    clp["UG1"] = ModbusClient(
        host=dict_ips["UG1_slave_ip"],
        port=dict_ips["UG1_slave_porta"],
        unit_id=1,
        timeout=0.5
    )
    clp["UG2"] = ModbusClient(
        host=dict_ips["UG2_slave_ip"],
        port=dict_ips["UG2_slave_porta"],
        unit_id=1,
        timeout=0.5
    )
    clp["MOA"] = ModbusClient(
        host=dict_ips["MOA_slave_ip"],
        port=dict_ips["MOA_slave_porta"],
        unit_id=1,
        timeout=0.5
    )

    rele["SE"] = ModbusClient(
        host=dict_ips["RELE_SE_slave_ip"],
        port=dict_ips["RELE_SE_slave_porta"],
        unit_id=1,
        timeout=0.5
    )
    rele["TE"] = ModbusClient(
        host=dict_ips["RELE_TE_slave_ip"],
        port=dict_ips["RELE_TE_slave_porta"],
        unit_id=1,
        timeout=0.5
    )
    rele["BAY"] = ModbusClient(
        host=dict_ips["RELE_BAY_slave_ip"],
        port=dict_ips["RELE_BAY_slave_porta"],
        unit_id=1,
        timeout=0.5
    )
    rele["UG1"] = ModbusClient(
        host=dict_ips["RELE_UG1_slave_ip"],
        port=dict_ips["RELE_UG1_slave_porta"],
        unit_id=1,
        timeout=0.5
    )
    rele["UG2"] = ModbusClient(
        host=dict_ips["RELE_UG2_slave_ip"],
        port=dict_ips["RELE_UG2_slave_porta"],
        unit_id=1,
        timeout=0.5
    )

    @staticmethod
    def ping(host) -> bool:
        return [True if subprocess.call(["ping", "-c", "1", "-w", "1", host], stdout=subprocess.PIPE) == 0 else False for _ in range(2)]

    @classmethod
    def open_all(cls) -> None:
        logger.debug("[CLI] Iniciando conexões ModBus...")
        for _ , clp in cls.clp.items():
            raise ModBusClientFail(clp) if not clp.open() else ...
        for _ , rele in cls.rele.items():
            raise ModBusClientFail(rele) if not rele.open() else ...
        logger.info("[CLI] Conexões inciadas.")

    @classmethod
    def close_all(cls) -> None:
        logger.debug("[CLI] Encerrando conexões...")
        [clp.close() for _ , clp in cls.clp.items()]
        [rele.close() for _ , rele in cls.rele.items()]
        logger.debug("[CLI] Conexões encerradas.")

    @classmethod
    def ping_clients(cls) -> None:
        try:
            if not cls.ping(cls.dict_ips["SA_slave_ip"]):
                logger.warning("[CLI] CLP UG1 não respondeu a tentativa de comunicação!")
            
            if not cls.ping(cls.dict_ips["TDA_slave_ip"]):
                logger.warning("[CLI] CLP UG1 não respondeu a tentativa de comunicação!")
            
            if not cls.ping(cls.dict_ips["UG1_slave_ip"]):
                logger.warning("[CLI] CLP UG1 não respondeu a tentativa de comunicação!")

            if not cls.ping(cls.dict_ips["UG2_slave_ip"]):
                logger.warning("[CLI] CLP UG2 não respondeu a tentativa de comunicação!")
            
            if not cls.ping(cls.dict_ips["MOA_slave_ip"]):
                logger.warning("[CLI] CLP MOA não respondeu a tentativa de comunicação!")
            
            if not cls.ping(cls.dict_ips["RELE_SE_slave_ip"]):
                logger.warning("[CLI] RELE SE não respondeu a tentativa de comunicação!")
            
            if not cls.ping(cls.dict_ips["RELE_TE_slave_ip"]):
                logger.warning("[CLI] RELE TE não respondeu a tentativa de comunicação!")
            
            if not cls.ping(cls.dict_ips["RELE_BAY_slave_ip"]):
                logger.warning("[CLI] RELE BAY não respondeu a tentativa de comunicação!")
            
            if not cls.ping(cls.dict_ips["RELE_UG1_slave_ip"]):
                logger.warning("[CLI] RELE UG1 não respondeu a tentativa de comunicação!")
            
            if not cls.ping(cls.dict_ips["RELE_UG2_slave_ip"]):
                logger.warning("[CLI] RELE UG2 não respondeu a tentativa de comunicação!")
            
        except Exception as e:
            logger.exception(f"[CLI] Houve um erro ao enviar comando de ping dos clientes da usina. Exception: \"{repr(e)}\"")
            logger.debug(f"[CLI] Traceback: {traceback.format_exc()}")


class ModBusClientFail(Exception):
    def __init__(self, clp: ModbusClient | None = ..., *args: object) -> None:
        super().__init__(*args)
        raise f"[CLI] Modbus client ({clp.host} : {clp.port}) failed to open."
