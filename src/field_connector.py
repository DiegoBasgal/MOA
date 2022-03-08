import logging
from pyModbusTCP.client import ModbusClient
from modbus_com import *
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
            self.ug1_clp = ModbusClient(host=self.ug1_ip, port=self.ug1_port, timeout=5, unit_id=1, auto_open=True, auto_close=False)
            self.ug2_clp = ModbusClient(host=self.ug2_ip, port=self.ug2_port, timeout=5, unit_id=1, auto_open=True, auto_close=False)
            self.usn_clp = ModbusClient(host=self.usn_ip, port=self.usn_port, timeout=5, unit_id=1, auto_open=True, auto_close=False)
            
        self.warned_ug1 = False
        self.warned_ug2 = False

    def open(self):
        logger.debug("Opening Modbus")
        if not self.ug1_clp.open():
            raise ModbusClientFailedToOpen("Modbus client ({}:{}) failed to open.".format(self.ug1_ip, self.ug1_port))
        
        if not self.ug2_clp.open():
            raise ModbusClientFailedToOpen("Modbus client ({}:{}) failed to open.".format(self.ug2_ip, self.ug2_port))
        
        if not self.usn_clp.open():
            raise ModbusClientFailedToOpen("Modbus client ({}:{}) failed to open.".format(self.usn_ip, self.usn_port))
        
        logger.debug("Openned Modbus")
        return self

    def close(self):
        logger.debug("Closing Modbus")
        self.ug1_clp.close()
        self.ug2_clp.close()
        self.usn_clp.close()
        logger.debug("Closed Modbus")

    def get_flag_falha52L(self):
        
        #dj52L_aberto
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 2**0:
            pass
        
        #dj52L_fechado
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 2**1:
            pass
        
        #dj52L_inconsistente
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 2**2:
            logger.info("dj52L_inconsistente")
            return True
        
        #dj52L_trip
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 2**3:
            logger.info("dj52L_trip")
            return True

        #Subestacao_Disj52LModoLocal: 
        #if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 2**4:
        #    return True
        
        #Subestacao_Disj52LModoRemoto: 
        #if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 2**5:
        #    return True

        #dj52L_mola_carregada
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 2**6:
            pass

        #Subestacao_Disj52LPressaoSF6Alarme
        #if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 2**7:
        #    return True

        #dj52L_falta_vcc
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 2**8:
            logger.info("dj52L_falta_vcc")
            return True
        
        #dj52L_condicao_de_fechamento
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 2**9:
            pass

        #Subestacao_Disj52LAbriu:
        #if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 2**10:
        #    return True
                
        #Subestacao_Disj52LFechou:
        #if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 2**11:
        #    return True

        #dj52L_falha_fechamento
        if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 2**12:
            logger.info("dj52L_falha_fechamento")
            return True
        
        #Subestacao_Disj52LPressaoSF6Trip:
        #if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 2**13:
        #    return True
        return False

    def get_dj52L_fechado(self):
        response = True if self.usn_clp.read_holding_registers(REG_USINA_Subestacao_Disj52L - 1)[0] & 0b10 else False
        return response

    def fechaDj52L(self):
        if self.get_flag_falha52L():
            return False
        else:
            if self.get_dj52L_fechado():
                response = True
            else:
                response = self.usn_clp.write_single_register(REG_USINA_Disj52LFechar - 1, 1)
            return response
            
    def get_emergencia_acionada(self):
        # return int(self.usn_clp.read_holding_registers(REG_USINA_Usina_Emergencia_Info - 1)[0])
        # PCH_Covo.Driver.USINA.Alarmes.Alarme01.Bit00 01.00 - Botão de Emergência Pressionado
        # PCH_Covo.Driver.USINA.Alarmes.Alarme01.Bit01 01.01 - Emergência Supervisório Pressionada
        # PCH_Covo.Driver.USINA.Alarmes.Alarme01.Bit03 01.03 - Relé 86BF Atuado (Falha Disjuntores)
        # PCH_Covo.Driver.USINA.Alarmes.Alarme01.Bit04 01.04 - Relé 86TE Atuado (falha Trafo Elevador)
        # PCH_Covo.Driver.USINA.Alarmes.Alarme01.Bit13 01.13 - PACP - Relé Proteção SEL787 - Trip Atuado
        return 0

    def set_pos_comporta(self, pos_comporta):
        pass

    def get_nv_montante(self):
        nv = round(self.usn_clp.read_holding_registers(REG_USINA_NivelBarragem - 1)[0] / 100, 3)
        logger.debug("Nv montante: {}".format(nv))
        return nv

    def get_pot_medidor(self):
        return round(self.usn_clp.read_holding_registers(REG_USINA_Subestacao_PotenciaAtivaMedia - 1)[0] * 0.001, 3)

    def get_tensao_na_linha(self):
        rs = self.usn_clp.read_holding_registers(REG_USINA_Subestacao_TensaoRS - 1)[0]*10
        st = self.usn_clp.read_holding_registers(REG_USINA_Subestacao_TensaoST - 1)[0]*10
        tr = self.usn_clp.read_holding_registers(REG_USINA_Subestacao_TensaoTR - 1)[0]*10
        return float(min(rs, st, tr))

    def normalizar_emergencia(self):
        logger.info("Reconehce, reset, fecha Dj52L")
        logger.debug("Desliga emergencia")
        self.ug1_clp.write_single_register(REG_UG1_Operacao_EmergenciaLigar - 1, 0)
        self.ug2_clp.write_single_register(REG_UG2_Operacao_EmergenciaLigar - 1, 0)
        self.usn_clp.write_single_register(REG_USINA_EmergenciaLigar - 1, 0)
        self.ug1_clp.write_single_register(REG_UG1_Operacao_EmergenciaDesligar - 1, 1)
        self.ug2_clp.write_single_register(REG_UG2_Operacao_EmergenciaDesligar - 1, 1)
        self.usn_clp.write_single_register(REG_USINA_EmergenciaDesligar - 1, 1)
        sleep(1)
        logger.debug("Reconhece alarmes")
        self.usn_clp.write_single_register(REG_USINA_ReconheceAlarmes - 1, 1) 
        self.ug1_clp.write_single_register(REG_UG1_Operacao_PCH_CovoReconheceAlarmes - 1, 1)
        self.ug2_clp.write_single_register(REG_UG2_Operacao_PCH_CovoReconheceAlarmes - 1, 1)
        sleep(1)
        logger.debug("Reset alarmes")
        self.usn_clp.write_single_register(REG_USINA_ResetAlarmes - 1, 1)
        self.ug1_clp.write_single_register(REG_UG1_Operacao_PCH_CovoResetAlarmes - 1, 1)
        self.ug2_clp.write_single_register(REG_UG2_Operacao_PCH_CovoResetAlarmes - 1, 1)
        sleep(5)
        logger.debug("Fecha Dj52L")  
        self.fechaDj52L()
    
    def acionar_emergencia(self):
        logger.warning("Acionando emergencia")
        self.ug1_clp.write_single_register(REG_USINA_EmergenciaLigar - 1, 1)
        sleep(1)
        self.ug1_clp.write_single_register(REG_USINA_EmergenciaLigar - 1, 0)
        sleep(1)
        self.ug1_clp.write_single_register(REG_USINA_EmergenciaDesligar - 1, 1)

    #UG1
    def get_flag_ug1(self):
        
        all_low = True
       
        # PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit00 01.00 - Emergência Supervisório Pressionada
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme01 - 1)[0] & (2**0) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit00 01.00 - Emergência Supervisório Pressionada")

       # PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit01 01.01 - PCP-U1 - Botão de Emergência Pressionado
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme01 - 1)[0] & (2**1) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit01 01.01 - PCP-U1 - Botão de Emergência Pressionado")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit02 01.02 - Q49 - Botão de Emergência Pressionado
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme01 - 1)[0] & (2**2) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit02 01.02 - Q49 - Botão de Emergência Pressionado")
        
        # PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit02 04.02 - Reg Velocidade - TRIP
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme04 - 1)[0] & (2**2) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit02 04.02 - Reg Velocidade - TRIP")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit05 04.05 - Dispositivo de SobreVelocidade Mecânico Atuado
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme04 - 1)[0] & (2**5) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit05 04.05 - Dispositivo de SobreVelocidade Mecânico Atuado")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit12 04.12 - Reg Tensão - TRIP
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme04 - 1)[0] & (2**12) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit12 04.12 - Reg Tensão - TRIP")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit06 05.06 - Relé de Bloqueio 86M Trip Atuado 
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme05 - 1)[0] & (2**6) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit06 05.06 - Relé de Bloqueio 86M Trip Atuado")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit07 05.07 - Relé de Bloqueio 86M Trip Atuado Temporizado
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme05 - 1)[0] & (2**7) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit07 05.07 - Relé de Bloqueio 86M Trip Atuado Temporizado")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit08 05.08 - Relé de Bloqueio 86M Trip Atuado pelo CLP
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme05 - 1)[0] & (2**8) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit08 05.08 - Relé de Bloqueio 86M Trip Atuado pelo CLP")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit09 05.09 - Relé de Bloqueio 86E Trip Atuado
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme05 - 1)[0] & (2**9) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit09 05.09 - Relé de Bloqueio 86E Trip Atuado")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit10 05.10 - Relé de Bloqueio 86E Trip Atuado Temporizado
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme05 - 1)[0] & (2**10) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit10 05.10 - Relé de Bloqueio 86E Trip Atuado Temporizado")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit11 05.11 - Relé de Bloqueio 86E Trip Atuado pelo CLP
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme05 - 1)[0] & (2**11) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit11 05.11 - Relé de Bloqueio 86E Trip Atuado pelo CLP")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit12 05.12 - Relé de Bloqueio 86H Trip Atuado
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme05 - 1)[0] & (2**12) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit12 05.12 - Relé de Bloqueio 86H Trip Atuado")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit13 05.13 - Relé de Bloqueio 86H Trip Atuado pelo CLP
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme05 - 1)[0] & (2**13) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit13 05.13 - Relé de Bloqueio 86H Trip Atuado pelo CLP")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme06.Bit00 06.00 - Relé de Proteção do Gerador - Trip Atuado
        if not self.ug1_clp.read_holding_registers(REG_UG1_Alarme06 - 1)[0] & (2**0) == 0:
            all_low = False
            if not self.warned_ug1:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme06.Bit00 06.00 - Relé de Proteção do Gerador - Trip Atuado")
        
        self.warned_ug1 = not all_low 
        if all_low:
            return False
        else:
            return True

    def get_potencia_ug1(self):
        return round(self.ug1_clp.read_holding_registers(REG_UG1_Gerador_PotenciaAtivaMedia - 1)[0] * 0.001, 3)

    def get_horas_ug1(self):
        high = self.ug1_clp.read_holding_registers(REG_UG1_HorimetroEletrico_High - 1)[0]
        low = self.ug1_clp.read_holding_registers(REG_UG1_HorimetroEletrico_Low - 1)[0]
        return low

    def get_perda_na_grade_ug1(self):
        montante_grade = round(self.usn_clp.read_holding_registers(REG_UG1_NivelBarragem - 1)[0] / 100, 3)
        jusantante_grade = round(self.usn_clp.read_holding_registers(REG_USINA_NivelCanalAducao - 1)[0] / 100, 3)
        perda_na_grade = max(0, montante_grade - jusantante_grade)
        return perda_na_grade

    def get_temperatura_do_mancal_ug1(self):
        temperatura_max_mancal = max(self.ug1_clp.read_holding_registers(REG_UG1_Temperatura_04 - 1, 5))
        return round(temperatura_max_mancal)

    def get_sincro_ug1(self):
        response = self.ug1_clp.read_holding_registers(REG_UG1_Operacao_EtapaAtual - 1)[0]
        return True if response == 4 else False

    def get_ug1_parada(self):
        response = self.ug1_clp.read_holding_registers(REG_UG1_Operacao_EtapaAtual - 1)[0]
        response = True if response == 0 else False
        logger.debug("get_ug1_parada: {}".format(response))
        return response

    def partir_ug1(self):
        #if not self.get_sincro_ug1():
        if self.fechaDj52L():
            response = self.ug1_clp.write_single_register(REG_UG1_Operacao_US - 1, 1)
        else:
            response = False
        logger.debug("REG_UG1_Operacao_US(1): {}".format(response))       

    def parar_ug1(self):      
        response = self.ug1_clp.write_single_register(REG_UG1_Operacao_UP - 1, 1)
        logger.debug("REG_UG1_Operacao_UP(1) {}".format(response))       

    def set_ug1_setpoint(self, setpoint):
        response = self.ug1_clp.write_single_register(REG_UG1_Operacao_US - 1, 1)
        logger.debug("get_sincro_ug1 response: {}".format(self.get_sincro_ug1()))
        logger.debug("get_etapa_alvo_up_ug1 response: {}".format(self.get_etapa_alvo_up_ug1()))
        if self.get_sincro_ug1() and not self.get_etapa_alvo_up_ug1():
            response = self.ug1_clp.write_single_register(REG_UG1_RegV_ColocarCarga - 1, 1)
            logger.debug("write_single_register REG_UG1_RegV_ColocarCarga({}) response: {}".format(1, response))
        self.fechaDj52L()
        sleep(1)
        response = self.usn_clp.write_single_register(REG_USINA_CtrlPotencia_ModoNivelDesligar - 1, 1)
        response = self.usn_clp.write_single_register(REG_USINA_CtrlPotencia_ReligamentoDesligar - 1, 1)
        response = self.ug1_clp.write_single_register(REG_UG1_CtrlPotencia_ModoNivelDesligar - 1, 1)
        response = self.ug1_clp.write_single_register(REG_UG1_CtrlPotencia_ModoPotenciaDesligar - 1, 1)
        response = self.ug1_clp.write_single_register(REG_UG1_CtrlPotencia_Alvo, int(setpoint))
        logger.debug("REG_UG1_CtrlPotencia_Alvo({}) response: {}".format(setpoint, response))

    def get_etapa_alvo_up_ug1(self):
        response = (self.ug1_clp.read_holding_registers(REG_UG1_Operacao_EtapaAlvo - 1)[0] >> 0 & 1)
        return True if response == 1 else False

    def acionar_emergencia_ug1(self):
        logger.warning("Acionando emergencia UG1")
        self.ug1_clp.write_single_register(REG_UG1_Operacao_EmergenciaLigar - 1, 1)
        sleep(1)
        self.ug1_clp.write_single_register(REG_UG1_Operacao_EmergenciaLigar - 1, 0)
        sleep(1)
        self.ug1_clp.write_single_register(REG_UG1_Operacao_EmergenciaDesligar - 1, 1)

    def get_temperatura_enrolamento_fase_r_ug1(self):
        # Gerador 1 - Enrolamento fase R
        return self.ug1_clp.read_holding_registers(REG_UG1_Temperatura_01 - 1, 1)[0]
    
    def get_temperatura_enrolamento_fase_s_ug1(self):
        # Gerador 1 - Enrolamento Fase S
        return self.ug1_clp.read_holding_registers(REG_UG1_Temperatura_02 - 1, 1)[0]
    
    def get_temperatura_enrolamento_fase_t_ug1(self):
        # Gerador 1 - Enrolamento fase T
        return self.ug1_clp.read_holding_registers(REG_UG1_Temperatura_03 - 1, 1)[0]
    
    def get_temperatura_mancal_la_escora_1_ug1(self):
        # Gerador 1 - Mancal L.A. Escora 01
        return self.ug1_clp.read_holding_registers(REG_UG1_Temperatura_04 - 1, 1)[0]
    
    def get_temperatura_mancal_la_escora_2_ug1(self):
        # Gerador 1 - Mancal L.A. Escora 02
        return self.ug1_clp.read_holding_registers(REG_UG1_Temperatura_05 - 1, 1)[0]
        
    def get_temperatura_mancal_la_contra_escora_1_ug1(self):
        # Gerador 1 - Mancal L. A. Contra Escora 01
        return self.ug1_clp.read_holding_registers(REG_UG1_Temperatura_07 - 1, 1)[0]

    def get_temperatura_mancal_la_contra_escora_2_ug1(self):
        # Gerador 1 - Mancal L. A. Contra Escora 02
        return self.ug1_clp.read_holding_registers(REG_UG1_Temperatura_09 - 1, 1)[0]

    def get_temperatura_mancal_la_casquilho_ug1(self):
        # Gerador 1 - Mancal L. A. Casquilho
        return self.ug1_clp.read_holding_registers(REG_UG1_Temperatura_06 - 1, 1)[0]

    def get_temperatura_mancal_lna_casquilho_ug1(self):
        # Gerador 1 - Mancal L.N.A. Casquilho
        return self.ug1_clp.read_holding_registers(REG_UG1_Temperatura_08 - 1, 1)[0]

    #UG2
    def get_flag_ug2(self):
        
        all_low = True
       
        # PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit00 01.00 - Emergência Supervisório Pressionada
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme01 - 1)[0] & (2**0) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit00 01.00 - Emergência Supervisório Pressionada")

       # PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit01 01.01 - PCP-U1 - Botão de Emergência Pressionado
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme01 - 1)[0] & (2**1) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit01 01.01 - PCP-U1 - Botão de Emergência Pressionado")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit02 01.02 - Q49 - Botão de Emergência Pressionado
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme01 - 1)[0] & (2**2) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit02 01.02 - Q49 - Botão de Emergência Pressionado")
        
        # PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit02 04.02 - Reg Velocidade - TRIP
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme04 - 1)[0] & (2**2) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit02 04.02 - Reg Velocidade - TRIP")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit05 04.05 - Dispositivo de SobreVelocidade Mecânico Atuado
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme04 - 1)[0] & (2**5) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit05 04.05 - Dispositivo de SobreVelocidade Mecânico Atuado")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit12 04.12 - Reg Tensão - TRIP
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme04 - 1)[0] & (2**12) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit12 04.12 - Reg Tensão - TRIP")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit06 05.06 - Relé de Bloqueio 86M Trip Atuado 
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme05 - 1)[0] & (2**6) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit06 05.06 - Relé de Bloqueio 86M Trip Atuado")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit07 05.07 - Relé de Bloqueio 86M Trip Atuado Temporizado
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme05 - 1)[0] & (2**7) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit07 05.07 - Relé de Bloqueio 86M Trip Atuado Temporizado")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit08 05.08 - Relé de Bloqueio 86M Trip Atuado pelo CLP
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme05 - 1)[0] & (2**8) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit08 05.08 - Relé de Bloqueio 86M Trip Atuado pelo CLP")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit09 05.09 - Relé de Bloqueio 86E Trip Atuado
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme05 - 1)[0] & (2**9) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit09 05.09 - Relé de Bloqueio 86E Trip Atuado")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit10 05.10 - Relé de Bloqueio 86E Trip Atuado Temporizado
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme05 - 1)[0] & (2**10) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit10 05.10 - Relé de Bloqueio 86E Trip Atuado Temporizado")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit11 05.11 - Relé de Bloqueio 86E Trip Atuado pelo CLP
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme05 - 1)[0] & (2**11) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit11 05.11 - Relé de Bloqueio 86E Trip Atuado pelo CLP")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit12 05.12 - Relé de Bloqueio 86H Trip Atuado
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme05 - 1)[0] & (2**12) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit12 05.12 - Relé de Bloqueio 86H Trip Atuado")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit13 05.13 - Relé de Bloqueio 86H Trip Atuado pelo CLP
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme05 - 1)[0] & (2**13) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit13 05.13 - Relé de Bloqueio 86H Trip Atuado pelo CLP")

        # PCH_Covo.Driver.UG01.Alarmes.Alarme06.Bit00 06.00 - Relé de Proteção do Gerador - Trip Atuado
        if not self.ug2_clp.read_holding_registers(REG_UG2_Alarme06 - 1)[0] & (2**0) == 0:
            all_low = False
            if not self.warned_ug2:
                logger.warning("PCH_Covo.Driver.UG01.Alarmes.Alarme06.Bit00 06.00 - Relé de Proteção do Gerador - Trip Atuado")
        
        self.warned_ug2 = not all_low 
        if all_low:
            return False
        else:
            return True

    def get_potencia_ug2(self):
        return round(self.ug2_clp.read_holding_registers(REG_UG2_Gerador_PotenciaAtivaMedia - 1)[0] * 0.001, 3)

    def get_horas_ug2(self):
        high = self.ug2_clp.read_holding_registers(REG_UG2_HorimetroEletrico_High - 1)[0]
        low = self.ug2_clp.read_holding_registers(REG_UG2_HorimetroEletrico_Low - 1)[0]
        return low

    def get_perda_na_grade_ug2(self):
        montante_grade = round(self.usn_clp.read_holding_registers(REG_UG2_NivelBarragem - 1)[0] / 100, 3)
        jusantante_grade = round(self.usn_clp.read_holding_registers(REG_USINA_NivelCanalAducao - 1)[0] / 100, 3)
        perda_na_grade = max(0, montante_grade - jusantante_grade)
        return perda_na_grade

    def get_temperatura_do_mancal_ug2(self):
        temperatura_max_mancal = max(self.ug2_clp.read_holding_registers(REG_UG2_Temperatura_04 - 1, 5))
        return round(temperatura_max_mancal)

    def get_sincro_ug2(self):
        response = self.ug2_clp.read_holding_registers(REG_UG2_Operacao_EtapaAtual - 1)[0]
        return True if response == 4 else False

    def get_ug2_parada(self):
        response = self.ug2_clp.read_holding_registers(REG_UG2_Operacao_EtapaAtual - 1)[0]
        response = True if response == 0 else False
        logger.debug("get_ug2_parada: {}".format(response))
        return response        

    def partir_ug2(self):
        #if not self.get_sincro_ug2():
        if self.fechaDj52L():
            response = self.ug2_clp.write_single_register(REG_UG2_Operacao_US - 1, 1)
        else:
            response = False
        logger.debug("REG_UG2_Operacao_US(1): {}".format(response))       

    def parar_ug2(self):      
        response = self.ug2_clp.write_single_register(REG_UG2_Operacao_UP - 1, 1)
        logger.debug("REG_UG2_Operacao_UP(1) {}".format(response))       

    def set_ug2_setpoint(self, setpoint):
        response = self.ug2_clp.write_single_register(REG_UG2_Operacao_US - 1, 1)
        logger.debug("get_sincro_ug2 response: {}".format(self.get_sincro_ug2()))
        logger.debug("get_etapa_alvo_up_ug2 response: {}".format(self.get_etapa_alvo_up_ug2()))
        if self.get_sincro_ug2() and not self.get_etapa_alvo_up_ug2():
            response = self.ug2_clp.write_single_register(REG_UG2_RegV_ColocarCarga - 1, 1)
            logger.debug("write_single_register REG_UG2_RegV_ColocarCarga({}) response: {}".format(1, response))
        self.fechaDj52L()
        sleep(1)
        response = self.usn_clp.write_single_register(REG_USINA_CtrlPotencia_ModoNivelDesligar - 1, 1)
        response = self.usn_clp.write_single_register(REG_USINA_CtrlPotencia_ReligamentoDesligar - 1, 1)
        response = self.ug2_clp.write_single_register(REG_UG2_CtrlPotencia_ModoNivelDesligar - 1, 1)
        response = self.ug2_clp.write_single_register(REG_UG2_CtrlPotencia_ModoPotenciaDesligar - 1, 1)
        response = self.ug2_clp.write_single_register(REG_UG2_CtrlPotencia_Alvo - 1, int(setpoint))
        logger.debug("REG_UG2_CtrlPotencia_Alvo({}) response: {}".format(setpoint, response))

    def get_etapa_alvo_up_ug2(self):
        response = (self.ug2_clp.read_holding_registers(REG_UG2_Operacao_EtapaAlvo - 1)[0] >> 0 & 1)
        return True if response == 1 else False

    def acionar_emergencia_ug2(self):
        logger.warning("Acionando emergencia UG2")
        self.ug2_clp.write_single_register(REG_UG2_Operacao_EmergenciaLigar - 1, 1)
        sleep(1)
        self.ug2_clp.write_single_register(REG_UG2_Operacao_EmergenciaLigar - 1, 0)
        sleep(1)
        self.ug2_clp.write_single_register(REG_UG2_Operacao_EmergenciaDesligar - 1, 1)

    def get_temperatura_enrolamento_fase_r_ug2(self):
        # Gerador 1 - Enrolamento fase R
        return self.ug2_clp.read_holding_registers(REG_UG2_Temperatura_01 - 1, 1)[0]
    
    def get_temperatura_enrolamento_fase_s_ug2(self):
        # Gerador 1 - Enrolamento Fase S
        return self.ug2_clp.read_holding_registers(REG_UG2_Temperatura_02 - 1, 1)[0]
    
    def get_temperatura_enrolamento_fase_t_ug2(self):
        # Gerador 1 - Enrolamento fase T
        return self.ug2_clp.read_holding_registers(REG_UG2_Temperatura_03 - 1, 1)[0]
    
    def get_temperatura_mancal_la_escora_1_ug2(self):
        # Gerador 1 - Mancal L.A. Escora 01
        return self.ug2_clp.read_holding_registers(REG_UG2_Temperatura_04 - 1, 1)[0]
    
    def get_temperatura_mancal_la_escora_2_ug2(self):
        # Gerador 1 - Mancal L.A. Escora 02
        return self.ug2_clp.read_holding_registers(REG_UG2_Temperatura_05 - 1, 1)[0]
        
    def get_temperatura_mancal_la_contra_escora_1_ug2(self):
        # Gerador 1 - Mancal L. A. Contra Escora 01
        return self.ug2_clp.read_holding_registers(REG_UG2_Temperatura_07 - 1, 1)[0]

    def get_temperatura_mancal_la_contra_escora_2_ug2(self):
        # Gerador 1 - Mancal L. A. Contra Escora 02
        return self.ug2_clp.read_holding_registers(REG_UG2_Temperatura_09 - 1, 1)[0]

    def get_temperatura_mancal_la_casquilho_ug2(self):
        # Gerador 1 - Mancal L. A. Casquilho
        return self.ug2_clp.read_holding_registers(REG_UG2_Temperatura_06 - 1, 1)[0]

    def get_temperatura_mancal_lna_casquilho_ug2(self):
        # Gerador 1 - Mancal L.N.A. Casquilho
        return self.ug2_clp.read_holding_registers(REG_UG2_Temperatura_08 - 1, 1)[0]
