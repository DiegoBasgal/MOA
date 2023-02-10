from django.test import TestCase

from pyModbusTCP.client import ModbusClient


cleint = ModbusClient("10.101.2.215", 502, unit_id=1, timeout=0.5)

while True:
   try:
      cleint.read_holding_registers(99)[0]
   except Exception:
      print("deu certo")
# Create your tests here.
