from leitura import *
from opcua import Client, ua

class Escrita:
   def __init__(self) -> None:
      super().__init__()

class EscritaOPC(Escrita):
   def __init__(self, OPC_Client: Client, registrador: str, valor: int):
      super().__init__()
      self.__valor = valor
      self.__reg = registrador
      self.__client = OPC_Client
      self.escrita
   
   @property
   def escrita(self):
      node = self.__client.get_node(self.__reg)
      node.set_value(ua.DataValue(ua.Variant(self.__valor, ua.VariantType.Int32)))

class EscritaOPCBit(Escrita):
   def __init__(self, OPC_Client: Client, registrador: str, bit: int, valor: int):
      super().__init__()
      self.__bit = bit
      self.__valor = valor
      self.__reg = registrador
      self.__client = OPC_Client
      self.__raw = LeituraOPC(self.__client, self.__reg).raw
      self.escrita

   @property
   def escrita(self):
      bin = [int(x) for x in list('{0:0b}'.format(self.__raw))]
      
      for i in range(len(bin)):
         if self.__bit == i:
            bin[i] = self.__valor
            break

      v = sum(val*(2**x) for x, val in enumerate(reversed(bin)))
      print(v)
      client_node = self.__client.get_node(self.__reg)
      client_node_dv = ua.DataValue(ua.Variant(v, ua.VariantType.Int32))
      client_node.set_value(client_node_dv)


