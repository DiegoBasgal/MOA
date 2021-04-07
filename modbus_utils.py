from time import sleep
from pyModbusTCP.client import ModbusClient

UG1_slave_ip = '192.168.70.10'
UG1_slave_porta = 502
UG1_slave = ModbusClient(host=UG1_slave_ip, port=UG1_slave_porta, timeout=5, unit_id=1, auto_open=True, auto_close=True)

UG2_slave_ip = '192.168.70.13'
UG2_slave_porta = 502
UG2_slave = ModbusClient(host=UG2_slave_ip, port=UG2_slave_porta, timeout=5, unit_id=1, auto_open=True, auto_close=True)

USN_slave_ip = '192.168.70.16'
USN_slave_porta = 502
USN_slave = ModbusClient(host=USN_slave_ip, port=USN_slave_porta, timeout=5, unit_id=1, auto_open=True, auto_close=True)

def ler_todos():

        ug1_regs = []
        ug2_regs = []
        usn_regs = []

        # UG1
        aux = []
        aux += UG1_slave.read_holding_registers(12289, 73)
        aux += UG1_slave.read_holding_registers(13569, 92)
        aux += UG1_slave.read_holding_registers(14199, 16)
        aux += UG1_slave.read_holding_registers(12764, 124)
        aux += UG1_slave.read_holding_registers(12564, 32)
        aux += UG1_slave.read_holding_registers(14279, 128)
        aux += UG1_slave.read_holding_registers(12766, 4)
        for a in aux:
            if a >= 2**15:
                a = -a + 2**15
            ug1_regs.append(a)

        # UG2
        aux = []
        aux += UG2_slave.read_holding_registers(12289, 73)
        aux += UG2_slave.read_holding_registers(13569, 92)
        aux += UG2_slave.read_holding_registers(14199, 16)
        aux += UG2_slave.read_holding_registers(12764, 124)
        aux += UG2_slave.read_holding_registers(12564, 32)
        aux += UG2_slave.read_holding_registers(14279, 128)
        aux += UG2_slave.read_holding_registers(12766, 4)
        for a in aux:
            if a >= 2 ** 15:
                a = -a + 2 ** 15
            ug2_regs.append(a)

        # USN
        aux = []
        aux += USN_slave.read_holding_registers(12764, 220)
        aux += USN_slave.read_holding_registers(12289, 53)
        aux += USN_slave.read_holding_registers(14199, 16)
        aux += USN_slave.read_holding_registers(14279, 128)
        aux += USN_slave.read_holding_registers(13569, 77)
        aux += USN_slave.read_holding_registers(12564, 64)
        aux += USN_slave.read_holding_registers(12766, 4)
        for a in aux:
            if a >= 2 ** 15:
                a = -a + 2 ** 15
            usn_regs.append(a)

        return usn_regs, ug1_regs, ug2_regs

def ack_rst_alarmes():

    UG1_slave.write_single_register(12288+8, 1)  # desliga em
    UG1_slave.write_single_register(12288+1, 1)  # reconehce
    UG1_slave.write_single_register(12288+0, 1)  # reset

    UG2_slave.write_single_register(12288+8, 1)  # desliga em
    UG2_slave.write_single_register(12288+1, 1)  # reconehce
    UG2_slave.write_single_register(12288+0, 1)  # reset

    USN_slave.write_single_register(12288+3, 1)  # desliga em
    USN_slave.write_single_register(12288+1, 1)  # reconehce
    USN_slave.write_single_register(12288+0, 1)  # reset
    USN_slave.write_single_register(12288+5, 11)  # dj52L

ack_rst_alarmes()