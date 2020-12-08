from pyModbusTCP.client import ModbusClient

aflu = 0
SLAVE_IP = "172.21.15.13"   # ip da máquina que vai rodar o slave
SLAVE_PORT = 502            # porta do slave na máquina

while True:
    aflu = float(input("Digite a vazão afluente desejada:"))
    client = ModbusClient(host=SLAVE_IP, port=SLAVE_PORT, timeout=5, unit_id=1)
    client.open()
    client.write_single_register(7, int(aflu*1000))
    client.close()
    print("Nova vazão afluente: {}".format(aflu))
