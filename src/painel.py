#!/usr/bin/env python3
from pyModbusTCP.client import ModbusClient
import RPi.GPIO as gpio
import time
from pyModbusTCP.server import DataBank
import database_connector
db = database_connector.Database()

IN_01 = 17
IN_02 = 4
IN_03 = 22
IN_04 = 27

OUT_01 = 11
OUT_02 = 5
OUT_03 = 6
OUT_04 = 13
OUT_05 = 19
OUT_06 = 26
OUT_07 = 21
OUT_08 = 20
OUT_09 = 16
OUT_10 = 12

INS = [IN_01, IN_02, IN_03, IN_04]
OUTS = [OUT_01, OUT_02, OUT_03, OUT_04, OUT_05, OUT_06, OUT_07, OUT_08, OUT_09, OUT_10]

IN_PINS = {'IN_01': IN_01,
           'IN_02': IN_02,
           'IN_03': IN_03,
           'IN_04': IN_04 }

OUT_PINS = {'OUT_01': OUT_01,
            'OUT_02': OUT_02,
            'OUT_03': OUT_03,
            'OUT_04': OUT_04,
            'OUT_05': OUT_05,
            'OUT_06': OUT_06,
            'OUT_07': OUT_07,
            'OUT_08': OUT_08,
            'OUT_09': OUT_09,
            'OUT_10': OUT_10}
            
gpio.setmode(gpio.BCM)
for pin_name, pin_number in IN_PINS.items():
    gpio.setup(pin_number, gpio.IN)
    print('Pin {} ({}) set as INPUT'.format(pin_name, pin_number))
        
for pin_name, pin_number in OUT_PINS.items():
    gpio.setup(pin_number, gpio.OUT)
    print('Pin {} ({}) set as OUTPUT'.format(pin_name, pin_number))
            

modbus = ModbusClient(host='localhost', port=5002, unit_id=1)

while True:
    time.sleep(0.1)
    modbus.open()
    if not modbus.open():
        modbus.close()
        raise Exception("Modbus client failed to open.")
    db.dbopen()
    if gpio.input(IN_02):
        db.update_habilitar_autonomo()
        print("habilitar modo autonomo")
    if gpio.input(IN_01):
        db.update_desabilitar_autonomo()
        print("desabilitar modo autonomo")
    if gpio.input(IN_03):
        print("emergencia_modbus = 1")
        modbus.write_single_register(40200, 1)
    db.close()

    ug1_block = False if modbus.read_holding_registers(40020)[0] == 0 else True
    ug2_block = False if modbus.read_holding_registers(40030)[0] == 0 else True
    gpio.output(OUT_07, ug1_block)
    gpio.output(OUT_08, ug2_block)
    print("TRIP MODBUS: ", modbus.read_holding_registers(40100)[0])
    modbus.close()
