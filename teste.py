from time import sleep
from pyModbusTCP.client import ModbusClient

client = ModbusClient("0.0.0.0","5002",timeout=0.5,unit_id=1)

client.open()

while True:
   try:
      regs = client.read_holding_registers(0,90)
      print(f"Estado UG1 {regs[61]}")
      print(f"Estado UG2 {regs[71]}")
      print(f"Estado UG3 {regs[81]}")
      print("\n")
      sleep(3)
      print(f"Etapa UG1 {regs[62]}")
      print(f"Etapa UG2 {regs[72]}")
      print(f"Etapa UG3 {regs[82]}")
      print("\n")
      sleep(3)
   
   except Exception as e:
      raise(e)