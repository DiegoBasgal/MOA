"""
Testes de Leituras para ajustes do MOA
"""

# ------------------------------------------------------------------------------------------------------------------- #
### Teste de Leitura de Nível Montante PPN utilizando float -> Big Endian (Decoder 32 bits)

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pyModbusTCP.client import ModbusClient

tda = ModbusClient(
    host="192.168.10.105",
    port=502,
    unit_id=1,
    timeout=0.5,
    auto_close=True,
    auto_open=True
)


montante = tda.read_holding_registers(12350, 2)

decoder = BinaryPayloadDecoder.fromRegisters(montante, byteorder=Endian.Big, wordorder=Endian.Little)

print(montante)

print(decoder.decode_32bit_float())


# ------------------------------------------------------------------------------------------------------------------- #
### Teste de Leitura do Status do Disjuntor da Subestação PPN -> Big Endian (Decoder 32 bits)

# from pymodbus.constants import Endian
# from pymodbus.payload import BinaryPayloadDecoder
# from pyModbusTCP.client import ModbusClient

# sa = ModbusClient(
#     host="192.168.10.109",
#     port=502,
#     unit_id=1,
#     timeout=0.5,
#     auto_close=True,
#     auto_open=True
# )

# djl1 = sa.read_holding_registers(12308)
# djl2 = sa.read_holding_registers(12309)

# decoder1 = BinaryPayloadDecoder.fromRegisters(djl1, byteorder=Endian.Big, wordorder=Endian.Little)
# decoder2 = BinaryPayloadDecoder.fromRegisters(djl1, byteorder=Endian.Big, wordorder=Endian.Little)
# decoder3 = BinaryPayloadDecoder.fromRegisters(djl2, byteorder=Endian.Big, wordorder=Endian.Little)
# decoder4 = BinaryPayloadDecoder.fromRegisters(djl2, byteorder=Endian.Big, wordorder=Endian.Little)

# print('')
# print(f'Lista de 32 Bits dos REGs: 12308, 12309 -> bit 0 ao 31:')
# print(f'Lista -> {[int(b) for bits in [decoder2.decode_bits(2), decoder1.decode_bits(1), decoder4.decode_bits(2), decoder3.decode_bits(1)] for b in bits]}')
# print('')
# print('')