from pyModbusTCP.utils import *
from pyModbusTCP.client import ModbusClient

from src.dicionarios.reg import *


clp = ModbusClient(
    host="192.168.10.109",
    port=502,
    unit_id=1,
    timeout=0.5,
    auto_open=True,
    auto_close=True
)

leitura_1 = clp.read_holding_registers(12308)[0]
leitura_2 = clp.read_holding_registers(12309)[0]


leitura_bits_1 = get_bits_from_int(leitura_1)
leitura_bits_2 = get_bits_from_int(leitura_2)

lista_total = leitura_bits_2 + leitura_bits_1
int_conv = []

for i in lista_total:
    aux = 1 if i else 0
    int_conv.append(aux)

print(f"Lista bit int: {int_conv}")

print(f"\nValor extraído do Registrador: {leitura_1} (12308)")
print(f"\nValor extraído do Registrador: {leitura_2} (12309)")
print(f"\nLista de bits 1: {leitura_bits_1}")
print(f"\nLista de bits 2: {leitura_bits_2}")
print(f"\nLista de bits total: {lista_total}")