__author__ = "Diego Basgal"
__credits__ = "Lucas Lavratti" , "Diego Basgal"

__version__ = "0.1"
__status__ = "Development"
__maintainer__ = "Diego Basgal"
__email__ = "diego.garcia@ritmoenergia.com.br"
__description__ = "Este módulo corresponde a implementação de escrita nos registradores de campo."

from opcua import ua
from opcua import Client as OpcClient

# Classe de Escrita Base
class EscritaBase:
    def __init__(
            self,
            client: OpcClient | None = ...
        ) -> ...:

        if client is None:
            raise ValueError(f"[ESC] Não foi possível carregar a conexão com o cliente (\"{type(client).__name__}\").")
        elif not type(client):
            raise TypeError(f"[ESC] Tipagem de argumento inválida. O argumento \"cliente\" deve ser \"OpcClient\".")
        else:
            self.__client = client

    def escrever(self, registrador: str | int | None = ... , valor: int | float | None = ...) -> bool:
        if registrador is None:
            raise ValueError("[ESC] A Escrita precisa de um valor para o argumento \"registrador\".")
        elif not type(registrador):
            raise TypeError("[ESC] Tipagem de argumento inválida. O registrador deve ser \"str\" ou \"int\".")

        if valor is None:
            raise ValueError("[ESC] A Escrita precisa de um valor para o argumento \"valor\".")
        elif not type(valor):
            raise TypeError("[ESC] Tipagem de argumento inválida. O argumento \"valor\" deve ser \"int\" ou \"float\".")

        raise NotImplementedError("[ESC] O método deve ser implementado na classe filho")


# Classes de Escrita OPC
class EscritaOpc(EscritaBase):
    def __init__(self, client) -> ...:
        EscritaBase.__init__(self, client)

    def escrever(self, registrador: str, valor) -> bool:
        try:
            node = self.__client.get_node(registrador)
            return node.set_value(ua.DataValue(ua.Variant(valor, ua.VariantType.Int32)))

        except ConnectionError("[ESC-OPC] Erro ao conectar no cliente Opc.") \
            or ValueError("[ESC-OPC] Erro ao carregar dado \"raw\" do cliente Opc"):
            return False

class EscritaOpcBit(EscritaOpc):
    def __init__(self, client) -> ...:
        EscritaOpc.__init__(self, client)

    def escrever(self, registrador: str, valor: int[0 | 1], bit: int[range(31)] | None = ...) -> bool:
        if bit is None:
            raise ValueError("[ESC-OPC] A escrita precisa de um valor para o argumento \"bit\".")
        elif not type(bit):
            raise TypeError("[ESC-OPC] Tipagem de argumento inválida. O argumento \"bit\" deve ser \"int\" de \"0 a 31\".")
        else:
            try:
                raw = self.__client.get_node(registrador).get_value()
                bin = [int(x) for x in list('{0:0b}'.format(raw))]

                for i in range(len(bin)):
                    if bit == i:
                        bin[i] = valor
                        break

                v = sum(val*(2**x) for x, val in enumerate(reversed(bin)))
                client_node = self.__client.get_node(registrador)
                client_node_dv = ua.DataValue(ua.Variant(v, ua.VariantType.Int32))
                return client_node.set_value(client_node_dv)

            except ConnectionError("[ESC-OPC] Erro ao conectar no cliente Opc.") \
                or ValueError("[ESC-OPC] Erro ao carregar dado \"raw\" do cliente Opc"):
                return False