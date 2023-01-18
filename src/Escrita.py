from opcua import Client, ua

class Escrita:
   def __init__(self) -> None:
      super().__init__()


   def write_value_int(self, client, node_id, value):
      client_node = client.get_node(node_id)
      client_node_value = value
      client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Int16))
      client_node.set_value(client_node_dv)
   
   def write_value_float(self, client, node_id, value):
      client_node = client.get_node(node_id)
      client_node_value = value
      client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Float))
      client_node.set_value(client_node_dv)

   def write_value_bool(self, client, node_id, value):
      client_node = client.get_node(node_id)
      client_node_value = value
      client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Boolean))
      client_node.set_value(client_node_dv)

