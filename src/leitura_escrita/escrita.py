__version__ = "0.1"
__authors__ = "Diego Basgal", "Henrique Pfeifer"
__description__ = "Este módulo corresponde a implementação de escrita em registradores."

from opcua import ua
from opcua import Client as OpcClient

# Classes de Escrita OPC
class EscritaOpc:
    def __init__(self) -> ...:
        self.__client: OpcClient = None

    @property
    def client(self) -> OpcClient:
        return self.__client

    @client.setter
    def client(self, cln: OpcClient) -> None:
        self.__client = cln

    def escrever(self, registrador: str, valor) -> bool:
        try:
            node = self.__client.get_node(registrador)
            return node.set_value(ua.DataValue(ua.Variant(valor, ua.VariantType.Int32)))

        except ConnectionError("[ESC-OPC] Erro ao conectar no cliente Opc.") \
            or ValueError("[ESC-OPC] Erro ao carregar dado \"raw\" do cliente Opc"):
            return False

class EscritaOpcBit(EscritaOpc):
    def __init__(self) -> ...:
        super().__init__(self)

    def escrever_bit(self, registrador: str, valor: int[0 | 1], bit: int[range(31)] | None = ...) -> bool:
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