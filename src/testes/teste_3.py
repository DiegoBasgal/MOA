from pyModbusTCP.client import ModbusClient

rv = ModbusClient(
    host="192.168.10.120",
    port=502,
    unit_id=1,
    timeout=0.5,
    auto_open=True,
    auto_close=True
)

valor = rv.read_holding_registers(80)[0]

print(f"Valor: {valor}")