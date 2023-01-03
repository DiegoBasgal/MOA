"""
Leituras.

Versão 0.1 -> Utiliza o protocolo ModBusTCP
Versão 0.2 -> Utiliza o protocolo OPC

Esse módulo corresponde a implementação das leituras, dos valores de campo.
"""
__version__ = "0.2"
__authors__ = "Lucas Lavratti", "Diego Basgal"

import logging
from opcua import Client, ua

from src.VAR_REG import *

class LeituraBase:
    """
    Classe implementa a base para leituras. É "Abstrata" assim por se dizer...
    """

    def __init__(self, descr: str) -> None:
        self.__descr = descr
        self.__valor = None
        self.logger = logging.getLogger("__main__")

    def __str__(self):
        return "Leitura {}, Valor: {}, Raw: {}".format(
            self.__descr, self.valor, self.raw
        )

    @property
    def valor(self):
        raise NotImplementedError("Deve ser implementado na classe herdeira.")

    @property
    def raw(self):
        raise NotImplementedError("Deve ser implementado na classe herdeira.")

    @property
    def descr(self) -> str:
        """
        Descrição do limite em questão.

        Returns:
            str: descr
        """
        return self.__descr

class LeituraOPC(LeituraBase):
    def __init__(self, descr: str, opc_client: Client, registrador: str):
        super().__init__(descr)
        self.__descr = descr
        self.__opc_client = opc_client
        self.__registrador = registrador
   
    @property
    def raw(self) -> int:
        try:
            self.__opc_client.connect()
            aux = self.__opc_client.get_node(self.__registrador)
            valor = aux.get_value()
            if valor is not None:
                return valor
            else:
                return 0
        except:
            return 0
   
    @property
    def valor(self) -> float:
        return self.raw

class LeituraSoma(LeituraBase):
    def __init__(
        self,
        descr: str,
        leitura_A: LeituraBase,
        leitura_B: LeituraBase,
        min_is_zero=True,
    ):
        super().__init__(descr)
        self.__leitura_A = leitura_A
        self.__leitura_B = leitura_B
        self.__min_is_zero = min_is_zero

    @property
    def valor(self) -> float:
        """
        Valor

        Returns:
            float: leitura_A + leitura_B
        """
        if self.__min_is_zero:
            return max(0, self.__leitura_A.valor + self.__leitura_B.valor)
        else:
            return self.__leitura_A.valor + self.__leitura_B.valor

class LeiturasUSN:
    def __init__(self, cfg):
        self.opc_server = Client("opc.tcp://EOP:4845")

        self.nv_montante = LeituraOPC(
            "Nível Montante",
            self.opc_server,
            "ns=7;s=CLP_TA.TA.DB_STATUS.ANALOGICOS.NIVEL_MONTANTE"
        )
        
        self.tensao_rs = LeituraOPC(
            "Tensão RS",
            self.opc_server,
            "ns=7;s=CLP_SA."
        )

        self.tensao_st = LeituraOPC(
            "Tensão ST",
            self.opc_server,
            "ns=7;s=CLP_SA.",
        )

        self.tensao_tr = LeituraOPC(
            "Tensão TR",
            self.opc_server,
            "ns=7;s=CLP_SA."
        )
        
        self.potencia_ativa_kW = LeituraOPC(
            "Potências de MP e MR",
            self.opc_server,
            "ns=7;s=CLP_SA."
        )

def read_input_value(client, node_id):
   client_node = client.get_node(node_id)
   client_node_value = client_node.get_value()
   return client_node_value