import logging
import traceback
import subprocess

from src.dicionarios.dict import IP

from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("logger")

class Servidores:

    # ATRIBUIÇÃO DE VARIÁVEIS

    rv: "dict[str, ModbusClient]" = {}
    rt: "dict[str, ModbusClient]" = {}
    clp: "dict[str, ModbusClient]" = {}
    rele: "dict[str, ModbusClient]" = {}

    rv[f"UG1"] = ModbusClient(
        host=IP["RV_UG1_ip"],
        port=IP["RV_UG1_porta"],
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )
    rv[f"UG2"] = ModbusClient(
        host=IP["RV_UG2_ip"],
        port=IP["RV_UG2_porta"],
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )
    rt[f"UG1"] = ModbusClient(
        host=IP["RT_UG1_ip"],
        port=IP["RT_UG1_porta"],
        unit_id=2,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )
    rt[f"UG2"] = ModbusClient(
        host=IP["RT_UG2_ip"],
        port=IP["RT_UG2_porta"],
        unit_id=2,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )

    """rele[f"SE"] = ModbusClient(
        host=IP["RELE_SE_ip"],
        port=IP["RELE_SE_porta"],
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )"""
    rele[f"UG1"] = ModbusClient(
        host=IP["RELE_UG1_ip"],
        port=IP["RELE_UG1_porta"],
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )
    rele[f"UG2"] = ModbusClient(
        host=IP["RELE_UG2_ip"],
        port=IP["RELE_UG2_porta"],
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )

    clp["SA"] = ModbusClient(
        host=IP["SA_ip"],
        port=IP["SA_porta"],
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )
    clp["TDA"] = ModbusClient(
        host=IP["TDA_ip"],
        port=IP["TDA_porta"],
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )
    clp["UG1"] = ModbusClient(
        host=IP["UG1_ip"],
        port=IP["UG1_porta"],
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )
    clp["UG2"] = ModbusClient(
        host=IP["UG2_ip"],
        port=IP["UG2_porta"],
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )
    """
    clp["MOA"] = ModbusClient(
        host=IP["MOA_ip"],
        port=IP["MOA_porta"],
        unit_id=1,
        timeout=0.5,
        auto_close=True,
        auto_open=True
    )
    """

    @staticmethod
    def ping(host) -> "bool":
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        https://stackoverflow.com/questions/2953462/pinging-servers-in-python
        """

        return True if (subprocess.call(["ping", "-c", "1", "-w", "1", host], stdout=subprocess.PIPE) == 0 for _ in range(2)) else False

    @classmethod
    def open_all(cls) -> "None":
        """
        Função para abertura das conexões com CLPs da Usina.
        """

        logger.debug("[CLI] Iniciando conexões ModBus...")
        for n , clp in cls.clp.items():
            if not clp.open():
                logger.error(f"[CLI] Conexão com o servidor Modbus do CLP: {n}, falhou!")

        for n , rv in cls.rv.items():
            if not rv.open():
                logger.error(f"[CLI] Conexão com o servidor Modbus do RV: {n}, falhou!")

        for n , rt in cls.rt.items():
            if not rt.open():
                logger.error(f"[CLI] Conexão com o servidor Modbus do RT: {n}, falhou!")

        for n , rele in cls.rele.items():
            if not rele.open():
                logger.error(f"[CLI] Conexão com o servidor Modbus do RELÉ: {n}, falhou!")
        logger.info("[CLI] Conexões inciadas.")

    @classmethod
    def close_all(cls) -> "None":
        """
        Função para fechamento das conexões com os CLPs da Usina.
        """

        logger.debug("[CLI] Encerrando conexões...")
        for _ , clp in cls.clp.items():
            clp.close()

        for _ , rv in cls.rv.items():
            rv.close()

        for _ , rt in cls.rt.items():
            rt.close()

        for _ , rele in cls.rele.items():
            rele.close()
        logger.debug("[CLI] Conexões encerradas.")

    @classmethod
    def ping_clients(cls) -> "None":
        """
        Função para verificação de conexão com os CLPs das Usinas.

        Primeiramente envia o comando de ping para o CLP. Caso não haja resposta,
        avisa o operador sobre o erro de comunicação. Caso o CLP esteja on-line,
        tenta realizar a abertura de uma nova conexão. Caso não seja possível,
        avisa o operador, senão fecha a conexão.
        """

        try:
            if not cls.ping(IP["SA_ip"]):
                logger.warning("[CLI] O CLP do Serviço Auxiliar não respondeu a tentativa de comunicação!")

            if not cls.ping(IP["TDA_ip"]):
                logger.warning("[CLI] O CLP da Tomada da Água não respondeu a tentativa de comunicação!")

            if not cls.ping(IP["RELE_SE_ip"]):
                logger.warning("[CLI] O Relé da Subestação não respondeu a tentativa de comunicação!")

            if not cls.ping(IP["UG1_ip"]):
                logger.warning("[CLI] O CLP da Unidade Geradora 1 não respondeu a tentativa de comunicação!")

            if not cls.ping(IP["RV_UG1_ip"]):
                logger.warning("[CLI] O Regualdor de Velocidade da Unidade Geradora 1 não respondeu a tentativa de comunicação!")

            if not cls.ping(IP["RELE_UG1_ip"]):
                logger.warning("[CLI] O Relé da Unidade Geradora 1 não respondeu a tentativa de comunicação!")

            if not cls.ping(IP["UG2_ip"]):
                logger.warning("[CLI] O CLP da Unidade Geradora 2 não respondeu a tentativa de comunicação!")

            if not cls.ping(IP["RV_UG2_ip"]):
                logger.warning("[CLI] O Regulador de Velocidade da Unidade Geradora 2 não respondeu a tentativa de comunicação!")

            if not cls.ping(IP["RELE_UG2_ip"]):
                logger.warning("[CLI] O Relé da Unidade Geradora 2 não respondeu a tentativa de comunicação!")

            """
            if not cls.ping(IP["MOA_ip"]):
                logger.warning("[CLI] O CLP do MOA não respondeu a tentativa de comunicação!")
            """

        except Exception:
            logger.error(f"[CLI] Houve um erro ao enviar comando de ping dos clientes da usina.")
            logger.debug(f"{traceback.format_exc()}")