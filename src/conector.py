import logging
import traceback
import subprocess

import src.dicionarios.dict as d

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class ClientesUsina:

    rv: "dict[str, ModbusClient]" = {}
    clp: "dict[str, ModbusClient]" = {}
    rele: "dict[str, ModbusClient]" = {}

    rv[f"UG1"] = ModbusClient(
        host=d.ips["RV_UG1_ip"],
        port=d.ips["RV_UG1_porta"],
        unit_id=1,
        timeout=0.5
    )
    rv[f"UG2"] = ModbusClient(
        host=d.ips["RV_UG2_ip"],
        port=d.ips["RV_UG2_porta"],
        unit_id=1,
        timeout=0.5
    )

    """rele[f"SE"] = ModbusClient(
        host=d.ips["RELE_SE_ip"],
        port=d.ips["RELE_SE_porta"],
        unit_id=1,
        timeout=0.5
    )"""
    rele[f"UG1"] = ModbusClient(
        host=d.ips["RELE_UG1_ip"],
        port=d.ips["RELE_UG1_porta"],
        unit_id=1,
        timeout=0.5
    )
    rele[f"UG2"] = ModbusClient(
        host=d.ips["RELE_UG2_ip"],
        port=d.ips["RELE_UG2_porta"],
        unit_id=1,
        timeout=0.5
    )

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

        for _ , rv in cls.rv.items():
            if not rv.open():
                raise ModBusClientFail(rv)

        for _ , rele in cls.rele.items():
            if not rele.open():
                raise ModBusClientFail(rv)
        logger.info("[CLI] Conexões inciadas.")

    @classmethod
    def close_all(cls) -> None:
        logger.debug("[CLI] Encerrando conexões...")
        for _ , clp in cls.clp.items():
            clp.close()
        
        for _ , rv in cls.rv.items():
            rv.close()
        
        for _ , rele in cls.rele.items():
            rele.close()
        logger.debug("[CLI] Conexões encerradas.")

    @classmethod
    def ping_clients(cls) -> None:
        try:
            if not cls.ping(d.ips["SA_ip"]):
                logger.warning("[CLI] O CLP do Serviço Auxiliar não respondeu a tentativa de comunicação!")

            if not cls.ping(d.ips["TDA_ip"]):
                logger.warning("[CLI] O CLP da Tomada da Água não respondeu a tentativa de comunicação!")

            if not cls.ping(d.ips["RELE_SE_ip"]):
                logger.warning("[CLI] O Relé da Subestação não respondeu a tentativa de comunicação!")

            if not cls.ping(d.ips["UG1_ip"]):
                logger.warning("[CLI] O CLP da Unidade Geradora 1 não respondeu a tentativa de comunicação!")
            
            if not cls.ping(d.ips["RV_UG1_ip"]):
                logger.warning("[CLI] O Regualdor de Velocidade da Unidade Geradora 1 não respondeu a tentativa de comunicação!")
            
            if not cls.ping(d.ips["RELE_UG1_ip"]):
                logger.warning("[CLI] O Relé da Unidade Geradora 1 não respondeu a tentativa de comunicação!")

            if not cls.ping(d.ips["UG2_ip"]):
                logger.warning("[CLI] O CLP da Unidade Geradora 2 não respondeu a tentativa de comunicação!")
            
            if not cls.ping(d.ips["RV_UG2_ip"]):
                logger.warning("[CLI] O Regulador de Velocidade da Unidade Geradora 2 não respondeu a tentativa de comunicação!")
            
            if not cls.ping(d.ips["RELE_UG2_ip"]):
                logger.warning("[CLI] O Relé da Unidade Geradora 2 não respondeu a tentativa de comunicação!")

            """
            if not cls.ping(d.ips["MOA_ip"]):
                logger.warning("[CLI] O CLP do MOA não respondeu a tentativa de comunicação!")
            """

        except Exception:
            logger.error(f"[CLI] Houve um erro ao enviar comando de ping dos clientes da usina.")
            logger.debug(f"{traceback.format_exc()}")


class ModBusClientFail(Exception):
    def __init__(self, clp: ModbusClient = None, *args: object) -> None:
        super().__init__(*args)
        raise f"[CLI] Modbus client ({clp.host} : {clp.port}) failed to open."
