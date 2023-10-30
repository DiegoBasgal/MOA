from django.test import TestCase
from pymodbus.constants import Endian
from pyModbusTCP.client import ModbusClient
from pymodbus.payload import BinaryPayloadDecoder as BPD

# Create your tests here.

clp_tda = ModbusClient("192.168.20.140", 2000, unit_id=1, timeout=0.5)

l_cp2_b0 = clp_tda.read_holding_registers(0, 2)
print(f"Leitura -> {l_cp2_b0}")

dec1_cp2_b0 = BPD.fromRegisters(l_cp2_b0, byteorder=Endian.LITTLE)
dec2_cp2_b0 = BPD.fromRegisters(l_cp2_b0, byteorder=Endian.LITTLE)
lbit = [int(bit) for bits in [reversed(dec1_cp2_b0.decode_bits(1)), reversed(dec2_cp2_b0.decode_bits(2))] for bit in bits]
lbit_r = [b for b in reversed(lbit)]

print(f"Lista Bits -> {lbit}")
print(f"Lista Bits Reversa -> {lbit_r}")

for i in range(len(lbit_r)):
    if i == 1 and lbit_r[i] == 1:
        print("Comporta 2 ABERTA")
    elif i == 2 and lbit_r[i] == 1:
        print("Comporta 2 FECHADA")
    elif i == 3 and lbit_r[i] == 1:
        print("Comporta 2 CRACKING")
    elif i == 9 and lbit_r[i] == 1:
        print("Comporta 2 REMOTO")