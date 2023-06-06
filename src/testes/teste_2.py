from pyModbusTCP.client import ModbusClient

clp = ModbusClient(
    host="192.168.10.109",
    port=502,
    unit_id=1,
    timeout=0.5,
    auto_open=True,
    auto_close=True
)

reg_1 = clp.read_holding_registers(12308)
reg_2 = clp.read_holding_registers(12309)

print(f"Valor do reg 12308: {reg_1}")
print(f"Valor do reg 12309: {reg_2}")