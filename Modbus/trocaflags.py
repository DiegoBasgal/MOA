from time import sleep
from pyModbusTCP.client import ModbusClient

client = ModbusClient(host="172.21.15.13",
                      port=502,
                      auto_open=True,
                      auto_close=True,
                      timeout=5,
                      unit_id=1)
while True:
    flags = client.read_holding_registers(6, 1)[0]
    print("Flags atuais: 15, 14 , ... , 1, 0 \n{:016b}".format(flags))
    n = 2**int(input("Qual bit mudar (15->0)? "))
    client.write_single_register(6, (flags ^ n))


