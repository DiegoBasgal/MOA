#!/usr/bin/env python3
from pyModbusTCP.client import ModbusClient
import RPi.GPIO as gpio
import time
import socket
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
            

modbus = ModbusClient(host='localhost', port=5003, unit_id=1)
painel_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
painel_sock.bind(("127.0.0.1", 10200))
painel_sock.listen(5)
painel_sock.setblocking(0)

ug1_flag = False
ug2_flag = False
modo_auto = False
while True:
    
    time.sleep(0.1)
    
    if modbus.open():
        modo_auto = True if modbus.read_holding_registers(40100)[0] else False
        ug1_flag = True if modbus.read_holding_registers(40022)[0] else False
        ug2_flag = True if modbus.read_holding_registers(40032)[0] else False
        modbus.close()
    
    if gpio.input(IN_02):
        db.update_habilitar_autonomo()
        print("habilitar modo autonomo")
    
    if gpio.input(IN_01):
        db.update_desabilitar_autonomo()
        print("desabilitar modo autonomo")
    
    if gpio.input(IN_03):
        print("emergencia eletrica = 1")
        try:
            wa_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            wa_sock.connect(('127.0.0.1',10100))
            wa_sock.send(b'1')
            wa_sock.close()
        except Exception as e:
            print(e)
            pass

    gpio.output(OUT_06, not modo_auto)
    gpio.output(OUT_07, not ug1_flag)
    gpio.output(OUT_08, not ug2_flag)
    