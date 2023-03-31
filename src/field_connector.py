import logging
from pyModbusTCP.client import ModbusClient
from src.modbus_mapa_antigo import *
from time import sleep

logger = logging.getLogger('__main__')

class ModbusClientFailedToOpen(Exception):
    pass

class ModbusFailedToFetch(Exception):
    pass

class FieldConnector:

    def __init__(self, cfg=None):

        if cfg is None:
            raise Exception("A cfg dict is required")
        else:
            self.ug1_ip = cfg["UG1_slave_ip"]
            self.ug1_port = cfg["UG1_slave_porta"]
            self.ug2_ip = cfg["UG2_slave_ip"]
            self.ug2_port = cfg["UG2_slave_porta"]
            self.usn_ip = cfg["USN_slave_ip"]
            self.usn_port = cfg["USN_slave_porta"]
            self.ug1_clp = ModbusClient(host=self.ug1_ip, port=self.ug1_port, timeout=5, unit_id=1, auto_open=True, auto_close=True)
            self.ug2_clp = ModbusClient(host=self.ug2_ip, port=self.ug2_port, timeout=5, unit_id=1, auto_open=True, auto_close=True)
            self.usn_clp = ModbusClient(host=self.usn_ip, port=self.usn_port, timeout=5, unit_id=1, auto_open=True, auto_close=True)


            
        self.warned_ug1 = False
        self.warned_ug2 = False

    def desliga_controles_locais(self):
        self.usn_clp.write_single_register(REG_USINA_CtrlPotencia_ReligamentoLigar, 0)
        self.usn_clp.write_single_register(REG_USINA_CtrlPotencia_ModoNivelLigar, 0)
        self.usn_clp.write_single_register(REG_USINA_CtrlPotencia_ReligamentoDesligar, 1)
        self.usn_clp.write_single_register(REG_USINA_CtrlPotencia_ModoNivelDesligar, 1)
        self.ug1_clp.write_single_register(REG_UG1_CtrlPotencia_ModoPotenciaLigar, 0)
        self.ug1_clp.write_single_register(REG_UG1_CtrlPotencia_ModoNivelLigar, 0)
        self.ug1_clp.write_single_register(REG_UG1_CtrlPotencia_ModoPotenciaDesligar, 1)
        self.ug1_clp.write_single_register(REG_UG1_CtrlPotencia_ModoNivelDesligar, 1)
        self.ug2_clp.write_single_register(REG_UG2_CtrlPotencia_ModoPotenciaLigar, 0)
        self.ug2_clp.write_single_register(REG_UG2_CtrlPotencia_ModoNivelLigar, 0)
        self.ug2_clp.write_single_register(REG_UG2_CtrlPotencia_ModoPotenciaDesligar, 1)
        self.ug2_clp.write_single_register(REG_UG2_CtrlPotencia_ModoNivelDesligar, 1)

    def open(self):
        logger.debug("Opening Modbus")
        if not self.ug1_clp.open():
            raise ModbusClientFailedToOpen(f"Modbus client ({self.ug1_ip}:{self.ug2_port}) failed to open.")
        
        if not self.ug2_clp.open():
            raise ModbusClientFailedToOpen(f"Modbus client ({self.ug2_ip}:{self.ug2_port}) failed to open.")
        
        if not self.usn_clp.open():
            raise ModbusClientFailedToOpen(f"Modbus client ({self.usn_ip}:{self.usn_port}) failed to open.")
        
        logger.debug("Openned Modbus")
        return self

    def close(self):
        logger.debug("Closing Modbus")
        self.ug1_clp.close()
        self.ug2_clp.close()
        self.usn_clp.close()
        logger.debug("Closed Modbus")

    def fechaDj52L(self):
        if self.get_flag_falha52L():
            return False
        else:
            if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**1:
                response = True
            else:
                response = self.usn_clp.write_single_register(REG_USINA_Disj52LFechar, 1)
            return response

    def normalizar_emergencia(self):
        logger.info("Reconehce, reset, fecha Dj52L")
        logger.debug("Desliga emergencia")
        self.ug1_clp.write_single_register(REG_UG1_Operacao_EmergenciaLigar, 0)
        self.ug2_clp.write_single_register(REG_UG2_Operacao_EmergenciaLigar, 0)
        self.usn_clp.write_single_register(REG_USINA_EmergenciaLigar, 0)
        self.ug1_clp.write_single_register(REG_UG1_Operacao_EmergenciaDesligar, 1)
        self.ug2_clp.write_single_register(REG_UG2_Operacao_EmergenciaDesligar, 1)
        self.usn_clp.write_single_register(REG_USINA_EmergenciaDesligar, 1)
        sleep(1)
        logger.debug("Reconhece alarmes")
        self.usn_clp.write_single_register(REG_USINA_ReconheceAlarmes, 1) 
        self.ug1_clp.write_single_register(REG_UG1_Operacao_PCH_CovoReconheceAlarmes, 1)
        self.ug2_clp.write_single_register(REG_UG2_Operacao_PCH_CovoReconheceAlarmes, 1)
        sleep(1)
        logger.debug("Reset alarmes")
        self.usn_clp.write_single_register(REG_USINA_ResetAlarmes, 1)
        self.ug1_clp.write_single_register(REG_UG1_Operacao_PCH_CovoResetAlarmes, 1)
        self.ug2_clp.write_single_register(REG_UG2_Operacao_PCH_CovoResetAlarmes, 1)
        sleep(5)
        logger.debug("Fecha Dj52L")  
        self.fechaDj52L()
    
    def somente_reconhecer_emergencia(self):
        logger.debug("Somente reconhece alarmes")
        self.usn_clp.write_single_register(REG_USINA_ReconheceAlarmes, 1) 
        self.ug1_clp.write_single_register(REG_UG1_Operacao_PCH_CovoReconheceAlarmes, 1)
        self.ug2_clp.write_single_register(REG_UG2_Operacao_PCH_CovoReconheceAlarmes, 1)

    def acionar_emergencia(self):
        logger.warning("FC: Acionando emergencia")
        self.usn_clp.write_single_register(REG_UG1_Operacao_EmergenciaLigar, 1)
        self.ug1_clp.write_single_register(REG_UG2_Operacao_EmergenciaLigar, 1)
        self.ug2_clp.write_single_register(REG_USINA_EmergenciaLigar, 1)
        sleep(1)
        self.usn_clp.write_single_register(REG_UG1_Operacao_EmergenciaLigar, 0)
        self.ug1_clp.write_single_register(REG_UG2_Operacao_EmergenciaLigar, 0)
        self.ug2_clp.write_single_register(REG_USINA_EmergenciaLigar, 0)
        #sleep(1)
        #self.usn_clp.write_single_register(REG_USINA_EmergenciaDesligar, 1)
        #self.ug1_clp.write_single_register(REG_UG1_Operacao_EmergenciaDesligar, 1)
        #self.ug2_clp.write_single_register(REG_UG2_Operacao_EmergenciaDesligar, 1)

    def get_flag_falha52L(self):
        
        #dj52L_aberto
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**0:
            pass
        
        #dj52L_fechado
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**1:
            pass
        
        #dj52L_inconsistente
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**2:
            logger.info("dj52L_inconsistente")
            return True
        
        #dj52L_trip
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**3:
            logger.info("dj52L_trip")
            return True

        #Subestacao_Disj52LModoLocal: 
        #if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**4:
        #    return True
        
        #Subestacao_Disj52LModoRemoto: 
        #if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**5:
        #    return True

        #dj52L_mola_carregada
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**6:
            pass

        #Subestacao_Disj52LPressaoSF6Alarme
        #if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**7:
        #    return True

        #dj52L_falta_vcc
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**8:
            logger.info("dj52L_falta_vcc")
            return True
        
        #dj52L_condicao_de_fechamento
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**9:
            pass

        #Subestacao_Disj52LAbriu:
        #if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**10:
        #    return True
                
        #Subestacao_Disj52LFechou:
        #if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**11:
        #    return True

        #dj52L_falha_fechamento
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**12:
            logger.info("dj52L_falha_fechamento")
            return True
        
        #Subestacao_Disj52LPressaoSF6Trip:
        #if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L)[0] & 2**13:
        #    return True
        return False
