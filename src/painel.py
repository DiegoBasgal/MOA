#!/usr/bin/env python3
import os.path
import threading
from pyModbusTCP.client import ModbusClient
import RPi.GPIO as gpio
import time
import json
import logging
from codes import *
from mensageiro.mensageiro_log_handler import MensageiroHandler
from sys import stdout

import socket # simul

# Set-up logging
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler("logs/MOA.log")  # log para arquivo
ch = logging.StreamHandler(stdout)  # log para linha de comando
mh = MensageiroHandler()  # log para telegram e voip
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [PAINEL] %(message)s")
logFormatterSimples = logging.Formatter("[%(levelname)-5.5s] [PAINEL] %(message)s")
fh.setFormatter(logFormatter)
ch.setFormatter(logFormatter)
mh.setFormatter(logFormatterSimples)
fh.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)
mh.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(mh)


# DEFINE GPIO PINS AND MODE
GPIO_MODE = gpio.BCM
gpio.setmode(GPIO_MODE)

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

class Painel(threading.Thread):

    def __init__(self):
        super().__init__()
        
        logger.info("Iniciando painel...")
        
        self.stop_signal = False
        self.delay = 0.100

        try:
            gpio.cleanup()
            for pin_number in INPUTS:
                gpio.setup(pin_number, gpio.IN)
            for pin_number in OUTPUTS:
                gpio.setup(pin_number, gpio.OUT)
                gpio.output(pin_number, True)
        except Exception as e:
            logger.error("Erro ao iniciar GPIO.")
            raise e
    
        for _ in range(5):
            self.blink(0.1, pin=[OUT_01, OUT_04])

        # carrega as configurações
        self.cfg = []
        config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(config_file, 'r') as file:
                self.cfg = json.load(file)
        except Exception as e:
            logger.error("Erro ao ler configuração.")
            raise e

        try:
            self.modbus = ModbusClient(host='localhost', port=5003, unit_id=1)
        except Exception as e:
            logger.error("Erro ao criar leitor ModBus.")
            raise e
        

    def blink(self, t=0.5, pin=OUT_02):
        if pin is list:
            pins = pin
        else:
            pins = [pin]
        for p in pins:    
            gpio.output(pin, True)
        time.sleep(t)
        for p in pins:    
            gpio.output(pin, False)
        time.sleep(t)

    def stop(self):
        self.stop_signal = True

    def run(self):
        
        panel_was_updated = False
        autonomous_mode_activated = False
        tentativas = 0
        while not self.stop_signal:
            try:    
                tentativas += 1
                # Open modbus con
                if self.modbus.open():
                    if tentativas > 1:
                        logger.info("Comunicação do painel normalizada.")
                    tentativas = 0
                    # Read moa output registers
                    reg_value = self.modbus.read_holding_registers(self.cfg['REG_MOA_OUT_MODE'])[0]
                    if reg_value == MOA_ACTIVATED_AUTONOMOUS_MODE:
                        autonomous_mode_activated = True 
                    elif reg_value == MOA_DEACTIVATED_AUTONOMOUS_MODE:
                        autonomous_mode_activated = False 
                    else:
                        logger.warning("Leitura incorreta do registrador 'REG_MOA_OUT_MODE'.")

                    reg_value = self.modbus.read_holding_registers(self.cfg['REG_MOA_OUT_BLOCK_UG1'])[0]
                    if reg_value == 0 or reg_value == 1:
                        block_ug1_activated = True if  reg_value == 1 else False
                    else:
                        logger.warning("Leitura incorreta do registrador 'REG_MOA_OUT_BLOCK_UG1'.")

                    reg_value = self.modbus.read_holding_registers(self.cfg['REG_MOA_OUT_BLOCK_UG2'])[0]
                    if reg_value == 0 or reg_value == 1:
                        block_ug2_activated = True if  reg_value == 1 else False
                    else:
                        logger.warning("Leitura incorreta do registrador 'REG_MOA_OUT_BLOCK_UG2'.")

                    reg_value = self.modbus.read_holding_registers(self.cfg['REG_PAINEL_LIDO'])[0]
                    if reg_value == 0 or reg_value == 1:
                        panel_was_updated = True if  reg_value == 1 else False
                    else:
                        logger.warning("Leitura incorreta do registrador 'REG_PAINEL_LIDO'.")
                    
                    # Replicate panel on INPUTS 
                    if gpio.input(IN_01):
                        logger.info("Comando recebido: desabilitar modo autonomo.")
                        self.modbus.write_single_register(self.cfg['REG_MOA_IN_DESABILITA_AUTO'], 1)
                        self.modbus.write_single_register(self.cfg['REG_MOA_IN_HABILITA_AUTO'], 0)
                        self.modbus.write_single_register(self.cfg['REG_PAINEL_LIDO'], 0)
                        panel_was_updated = False

                    elif gpio.input(IN_02):
                        logger.info("Comando recebido: habilitar modo autonomo.")
                        self.modbus.write_single_register(self.cfg['REG_MOA_IN_DESABILITA_AUTO'], 0)
                        self.modbus.write_single_register(self.cfg['REG_MOA_IN_HABILITA_AUTO'], 1)
                        self.modbus.write_single_register(self.cfg['REG_PAINEL_LIDO'], 0)
                        panel_was_updated = False                    
                    
                    if gpio.input(IN_03):
                        logger.info("Comando recebido: emergencia.")
                        self.modbus.write_single_register(self.cfg['REG_MOA_IN_EMERG'], 1)
                        self.modbus.write_single_register(self.cfg['REG_PAINEL_LIDO'], 0)
                        panel_was_updated = False
                        #################################################################### simul
                        try:
                            wa_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            wa_sock.connect(('127.0.0.1',10100))
                            wa_sock.send(b'1')
                            wa_sock.close()
                        except Exception as e:
                            print(e)
                            pass
                        #################################################################### simul                   

                    # Close modbus con
                    self.modbus.close()

                    if panel_was_updated:
                        gpio.output(OUT_04, not autonomous_mode_activated) # inverted output
                    else:
                        self.blink(pin=OUT_04)
                    
                    if autonomous_mode_activated:
                        gpio.output(OUT_02, not block_ug1_activated)
                        gpio.output(OUT_03, not block_ug2_activated)
                    elif not autonomous_mode_activated: #If on manual, dont trip UGS
                        gpio.output(OUT_02, True)
                        gpio.output(OUT_03, True)
                   
                else:
                    logger.error("Comunicação com o MOA falhou. Modbus did not open.")
                    self.blink(pin=[OUT_01,OUT_04])

                time.sleep(self.delay)
                # Cicle end
            except Exception as e:
                self.blink(t=1, pin=[OUT_01,OUT_04])
                logger.error("Comunicação com o MOA falhou... {}".format(tentativas, repr(e)))
                if tentativas > 3:
                    logger.error("Esse erro não será mais exibito até que a situação seja normalizada")               
                continue


if __name__ == "__main__":
    # Iniciao o painel
    th_painel = Painel()
    th_painel.start()
