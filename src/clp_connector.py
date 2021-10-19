from pyModbusTCP.client import ModbusClient


class Clp:
    """Classe para tratar a comunicação com os controladores logicos programavaeis da usina"""

    def __init__(self, ip, port):
        self.modbus_clp = ModbusClient(host=ip, port=port, timeout=0.1, unit_id=1)

    def is_online(self):
        if self.modbus_clp.read_holding_registers(0):
            return True
        else:
            return False

    def write_to_single(self, register, value):
        """Escreve apenas um valor na clp, retorna True no sucesso, pode dar Connection Error"""
        if self.modbus_clp.open():
            self.modbus_clp.write_single_register(register, int(value))
            self.modbus_clp.close()
            return True
        else:
            raise ConnectionError

    def read_sequential(self, fisrt, quantity):
        """Lê da clp de maneira sequencial, retorna lista, pode dar Connection Error"""
        self.modbus_clp.open()
        result = self.modbus_clp.read_holding_registers(fisrt, quantity)
        self.modbus_clp.close()
        if result:
            return result
        else:
            raise ConnectionError
