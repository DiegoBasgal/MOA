import RPi.GPIO as gpio
import time

# DEFINE GPIO PINS AND MODE
GPIO_MODE = gpio.BCM
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

INPUTS = [IN_01, IN_02, IN_03, IN_04]
OUTPUTS = [OUT_01, OUT_02, OUT_03, OUT_04, OUT_05, OUT_06, OUT_07, OUT_08, OUT_09, OUT_10]

gpio.setmode(GPIO_MODE)

for pin_number in INPUTS:
    gpio.setup(pin_number, gpio.IN)

for pin_number in OUTPUTS:
    gpio.setup(pin_number, gpio.OUT)
    gpio.output(pin_number, False)

while True:
    for pin_number in OUTPUTS:
        gpio.output(pin_number, True) 
    time.sleep(1)
    for pin_number in OUTPUTS:
        gpio.output(pin_number, False) 
    time.sleep(1)
