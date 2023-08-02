__version__ = "0.1"
__author__ = "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da conexão com servidore(s), CLP(s) e RELÉ(s)."

import logging
import traceback
import subprocess

import src.dicionarios.dict as d

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("logger")

class ClientesUsina:

    # ATRIBUIÇÃO DE VARIÁVEIS

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
    clp["MOA"] = ModbusClient(
        host=d.ips["MOA_ip"],
        port=d.ips["MOA_porta"],
        unit_id=1,
        timeout=0.5
    )

    @staticmethod
    def ping(host) -> bool:
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        https://stackoverflow.com/questions/2953462/pinging-servers-in-python
        """

        return True if (subprocess.call(["ping", "-c", "1", "-w", "1", host], stdout=subprocess.PIPE) == 0 for _ in range(2)) else False

    @classmethod
    def open_all(cls) -> None:
        """
        Função para abertura das conexões com CLPs da Usina.
        """

        logger.debug("[CLI] Iniciando conexões ModBus...")
        for n , clp in cls.clp.items():
            if not clp.open():
                logger.error(f"[CLI] Erro ao iniciar conexão com o CLP - {n}")
        logger.debug("[CLI] Conexões inciadas.")

    @classmethod
    def close_all(cls) -> None:
        """
        Função para fechamento das conexões com os CLPs da Usina.
        """

        logger.debug("[CLI] Encerrando conexões...")
        for _ , clp in cls.clp.items():
            clp.close()
        logger.debug("[CLI] Conexões encerradas.")

    @classmethod
    def ping_clients(cls) -> None:
        """
        Função para verificação de conexão com os CLPs das Usinas.

        Primeiramente envia o comando de ping para o CLP. Caso não haja resposta,
        avisa o operador sobre o erro de comunicação. Caso o CLP esteja on-line,
        tenta realizar a abertura de uma nova conexão. Caso não seja possível,
        avisa o operador, senão fecha a conexão.
        """

        if not cls.ping(d.ips["TDA_ip"]) and not cls.borda_ping:
            cls.borda_ping = True
            d.glb["TDA_Offline"] = True
            logger.warning("[CLI] CLP TDA não respondeu a tentativa de comunicação!")

        elif cls.ping(d.ips["TDA_ip"]) and cls.borda_ping:
            logger.info("[CLI] Comunicação com o CLP TDA reestabelecida.")
            cls.borda_ping = False
            d.glb["TDA_Offline"] = False

        if not cls.ping(d.ips["SA_ip"]):
            logger.warning("[CLI] CLP SA não respondeu a tentativa de comunicação!")
        if cls.clp["SA"].open():
            cls.clp["SA"].close()
        else:
            logger.critical("[CLI] CLP SA não respondeu a tentativa de conexão ModBus!")
            cls.clp["SA"].close()

        if not cls.ping(d.ips["UG1_ip"]):
            logger.warning("[CLI] CLP UG1 não respondeu a tentativa de comunicação!")
        if cls.clp["UG1"].open():
            cls.clp["UG1"].close()
        else:
            logger.warning("[CLI] CLP UG1 não respondeu a tentativa de conexão ModBus!")

        # if not cls.ping(d.ips["MOA_ip"]):
        #     logger.warning("[CLI] CLP MOA não respondeu a tentativa de comunicação!")
        # if cls.clp["MOA"].open():
        #     cls.clp["MOA"].close()
        # else:
        #     logger.warning("[CLI] CLP MOA não respondeu a tentativa de conexão ModBus!")