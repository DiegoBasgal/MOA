__version__ = "0.1"
__author__ = "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da conexão com servidore(s), CLP(s) e RELÉ(s)."

import logging
import subprocess

import src.dicionarios.dict as d

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")

class Servidores:
    def __init__(self) -> "None":

        self.rv: "dict[str, ModbusClient]" = {}
        self.rt: "dict[str, ModbusClient]" = {}
        self.clp: "dict[str, ModbusClient]" = {}
        self.rele: "dict[str, ModbusClient]" = {}

        self.mp = ModbusClient(
            host=d.ips["MP_ip"],
            port=d.ips["MP_porta"],
            unit_id=1,
            timeout=0.5,
            auto_close=True,
            auto_open=True,
        )
        self.mr = ModbusClient(
            host=d.ips["MR_ip"],
            port=d.ips["MR_porta"],
            unit_id=1,
            timeout=0.5,
            auto_close=True,
            auto_open=True,
        )

        self.rv["UG1"] = ModbusClient(
            host=d.ips["RV_UG1_ip"],
            port=d.ips["RV_UG1_porta"],
            unit_id=11,
            timeout=0.5,
            auto_close=True,
            auto_open=True,
        )
        self.rv["UG2"] = ModbusClient(
            host=d.ips["RV_UG2_ip"],
            port=d.ips["RV_UG2_porta"],
            unit_id=21,
            timeout=0.5,
            auto_open=True,
            auto_close=True
        )

        self.rt["UG1"] = ModbusClient(
            host=d.ips["RT_UG1_ip"],
            port=d.ips["RT_UG1_porta"],
            unit_id=12,
            timeout=0.5,
            auto_close=True,
            auto_open=True,
        )
        self.rt["UG2"] = ModbusClient(
            host=d.ips["RT_UG2_ip"],
            port=d.ips["RT_UG2_porta"],
            unit_id=22,
            timeout=0.5,
            auto_close=True,
            auto_open=True,
        )

        self.clp["SA"] = ModbusClient(
            host=d.ips["SA_ip"],
            port=d.ips["SA_porta"],
            unit_id=1,
            timeout=0.5,
        )
        self.clp["TDA"] = ModbusClient(
            host=d.ips["TDA_ip"],
            port=d.ips["TDA_porta"],
            unit_id=1,
            timeout=5,
            auto_close=True,
            auto_open=True
        )
        self.clp["UG1"] = ModbusClient(
            host=d.ips["UG1_ip"],
            port=d.ips["UG1_porta"],
            unit_id=1,
            timeout=0.5,
        )
        self.clp["UG2"] = ModbusClient(
            host=d.ips["UG2_ip"],
            port=d.ips["UG2_porta"],
            unit_id=1,
            timeout=0.5,
        )
        self.clp["MOA"] = ModbusClient(
            host=d.ips["MOA_ip"],
            port=d.ips["MOA_porta"],
            unit_id=1,
            timeout=0.5,
        )

        self.rele["SE"] = ModbusClient(
            host=d.ips["RELE_SE_ip"],
            port=d.ips["RELE_SE_porta"],
            unit_id=1,
            timeout=0.5,
        )
        self.rele["TE"] = ModbusClient(
            host=d.ips["RELE_TE_ip"],
            port=d.ips["RELE_TE_porta"],
            unit_id=1,
            timeout=0.5,
        )
        self.rele["BAY"] = ModbusClient(
            host=d.ips["RELE_BAY_ip"],
            port=d.ips["RELE_BAY_porta"],
            unit_id=1,
            timeout=0.5,
        )
        self.rele["UG1"] = ModbusClient(
            host=d.ips["RELE_UG1_ip"],
            port=d.ips["RELE_UG1_porta"],
            unit_id=1,
            timeout=0.5,
        )
        self.rele["UG2"] = ModbusClient(
            host=d.ips["RELE_UG2_ip"],
            port=d.ips["RELE_UG2_porta"],
            unit_id=1,
            timeout=0.5,
        )

    @staticmethod
    def ping(host) -> "bool":
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        https://stackoverflow.com/questions/2953462/pinging-servers-in-python
        """

        return True if (subprocess.call(["ping", "-c", "1", "-w", "1", host], stdout=subprocess.PIPE) == 0 for _ in range(2)) else False


    def open_all(self) -> "None":
        """
        Função para abertura das conexões com CLPs da Usina.
        """

        logger.debug("[CLI] Iniciando conexões ModBus...")

        for _, clp in self.clp.items():
            clp.open()

        for _, rele in self.rele.items():
            rele.open()

        logger.debug("[CLI] Conexões inciadas.")


    def close_all(self) -> "None":
        """
        Função para fechamento das conexões com os CLPs da Usina.
        """

        logger.debug("[CLI] Encerrando conexões...")

        for _ , clp in self.clp.items():
            clp.close()

        for _, rele in self.rele.items():
            rele.close()

        logger.debug("[CLI] Conexões encerradas.")


    def ping_clients(self) -> "None":
        """
        Função para verificação de conexão com os CLPs das Usinas.

        Primeiramente envia o comando de ping para o CLP. Caso não haja resposta,
        avisa o operador sobre o erro de comunicação. Caso o CLP esteja on-line,
        tenta realizar a abertura de uma nova conexão. Caso não seja possível,
        avisa o operador, senão fecha a conexão.
        """
        return

        if not self.ping(d.ips["TDA_ip"]):
            logger.warning("[CLI] CLP TDA não respondeu a tentativa de comunicação!")

        if self.clp["TDA"].open():
            self.clp["TDA"].close()
        else:
            logger.critical("[CLI] CLP TDA não respondeu a tentativa de conexão ModBus!")
            self.clp["TDA"].close()

        if not self.ping(d.ips["SA_ip"]):
            logger.warning("[CLI] CLP SA não respondeu a tentativa de comunicação!")
        if self.clp["SA"].open():
            self.clp["SA"].close()
        else:
            logger.critical("[CLI] CLP SA não respondeu a tentativa de conexão ModBus!")
            self.clp["SA"].close()

        if not self.ping(d.ips["UG1_ip"]):
            logger.warning("[CLI] CLP UG1 não respondeu a tentativa de comunicação!")
        if self.clp["UG1"].open():
            self.clp["UG1"].close()
        else:
            logger.warning("[CLI] CLP UG1 não respondeu a tentativa de conexão ModBus!")

        if not self.ping(d.ips["UG2_ip"]):
            logger.warning("[CLI] CLP UG2 não respondeu a tentativa de comunicação!")
        if self.clp["UG2"].open():
            self.clp["UG2"].close()
        else:
            logger.warning("[CLI] CLP UG2 não respondeu a tentativa de conexão ModBus!")

        if not self.ping(d.ips["MOA_ip"]):
            logger.warning("[CLI] CLP MOA não respondeu a tentativa de comunicação!")
        if self.clp["MOA"].open():
            self.clp["MOA"].close()
        else:
            logger.warning("[CLI] CLP MOA não respondeu a tentativa de conexão ModBus!")
