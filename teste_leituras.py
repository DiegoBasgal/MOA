"""
Testes de Leituras para ajustes do MOA
"""

# ------------------------------------------------------------------------------------------------------------------- #
### Teste de Leitura de Nível Montante PPN (Exemplo) utilizando float -> Big Endian (Decoder 32 bits)

# from pymodbus.constants import Endian
# from pymodbus.payload import BinaryPayloadDecoder
# from pyModbusTCP.client import ModbusClient

# tda = ModbusClient(
#     host="192.168.10.105",
#     port=502,
#     unit_id=1,
#     timeout=0.5,
#     auto_close=True,
#     auto_open=True
# )


# montante = tda.read_holding_registers(12350, 2)

# decoder = BinaryPayloadDecoder.fromRegisters(montante, byteorder=Endian.Big, wordorder=Endian.Little)

# print(montante)

# print(decoder.decode_32bit_float())


# ------------------------------------------------------------------------------------------------------------------- #
### Teste de Leitura do Status do Disjuntor da Subestação PPN (Exemplo) -> Big Endian (Decoder 32 bits)

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

# lbit = [int(b) for bits in [reversed(decoder3.decode_bits(1)), reversed(decoder4.decode_bits(2))] for b in bits]
# lbit_r = [b for b in reversed(lbit)]


# print('')
# print('Lista de 16 Bits do REG 12309:')
# print('')
# print(f'Lista -> {lbit}')
# print(f'Lista Reversa -> {lbit_r}')
# print('')


# print('')
# print(f'Valor Decimal REG 12309 (Lista Reversa): {sum(val*(2**x) for x, val in enumerate(lbit_r))}')
# print('')
# print('')

# print('')
# print(f'Lista de 32 Bits dos REGs: 12308, 12309 -> bit 0 ao 31:')
# print(f'Lista -> {[int(b) for bits in [decoder2.decode_bits(2), decoder1.decode_bits(1), decoder4.decode_bits(2), decoder3.decode_bits(1)] for b in bits]}')
# print('')
# print('')


# ------------------------------------------------------------------------------------------------------------------- #
### Teste de Incremento de Valores no Dicionário de Registradores para uso na Simulação

# import regex as re
# from src.dicionarios.reg import *

# for n, d in REG_CLP.items():
#     if n == "TDA":
#         for n, l in d.items():
#             if re.search('^CP1', n):
#                 if isinstance(l, list):
#                     l[0] += 1000
#                     print(f'N: {n}, REG: {l[0]}')
#                 else:
#                     l += 1000
#                     print(f'N: {n}, REG: {l}')

#             elif re.search('^CP2', n):
#                 if isinstance(l, list):
#                     l[0] += 2000
#                     print(f'N: {n}, REG: {l[0]}')
#                 else:
#                     l += 2000
#                     print(f'N: {n}, REG: {l}')

#     elif n == "UG1":
#         for l in d.values():
#             if isinstance(l, list):
#                 l[0] += 10000
#                 print(f'REG: {l[0]}')
#             else:
#                 l += 10000
#                 print(f'REG: {l}')

#     elif n == "UG2":
#         for l in d.values():
#             if isinstance(l, list):
#                 l[0] += 20000
#                 print(f'REG: {l[0]}')
#             else:
#                 l += 20000
#                 print(f'REG: {l}')
#     else:
#         pass


# ------------------------------------------------------------------------------------------------------------------- #
### Teste de Leitura de Nível Montante XAV

# from src.funcoes.leitura import *
# from src.dicionarios.reg import *

# from pymodbus.constants import Endian
# from pymodbus.payload import BinaryPayloadDecoder
# from pyModbusTCP.client import ModbusClient

# tda = ModbusClient(
#     host="192.168.20.140",
#     port=2000,
#     unit_id=1,
#     timeout=0.5
# )

# nivel = LeituraModbusFloat(
#     client=tda,
#     registrador=REG_CLP["TDA"]["NV_MONTANTE"]
# )



# raw = tda.read_holding_registers(31, 2)

# dec = BPD.fromRegisters(raw, byteorder=Endian.Big, wordorder=Endian.Little)

# print('')
# print(f'Leitura Nível Módulo MB: {dec.decode_32bit_float()}')
# print('')


# print('')
# print(f"Leitura de Nível Classe Python: {nivel.valor}")
# print('')

ETAPA = 99

dicio = {
    "T": {
        "etapa": 0,
    }
}

etapa = None

dicio["T"]["etapa"] = etapa = ETAPA

print(dicio["T"]["etapa"])

print(etapa)