from pyModbusTCP.client import ModbusClient

ENDERECO_CLP_NV_MONATNTE = 40000
ENDERECO_CLP_MEDIDOR = 40001
ENDERECO_CLP_TENSAO_NA_LINHA = 40002
ENDERECO_CLP_COMPORTA_FLAGS = 40010
ENDERECO_CLP_COMPORTA_POS = 40011
ENDERECO_CLP_UG1_FLAGS = 40020
ENDERECO_CLP_UG1_MINUTOS = 40023
ENDERECO_CLP_UG1_PERGA_GRADE = 40025
ENDERECO_CLP_UG1_POTENCIA = 40021
ENDERECO_CLP_UG1_SETPOINT = 40022
ENDERECO_CLP_UG1_T_MANCAL = 40024
ENDERECO_CLP_UG2_FLAGS = 40030
ENDERECO_CLP_UG2_MINUTOS = 40033
ENDERECO_CLP_UG2_PERGA_GRADE = 40035
ENDERECO_CLP_UG2_POTENCIA = 40031
ENDERECO_CLP_UG2_SETPOINT = 40032
ENDERECO_CLP_UG2_T_MANCAL = 40034
ENDERECO_CLP_USINA_FLAGS = 40100
ENDERECO_LOCAL_NV_MONATNTE = 40009
ENDERECO_LOCAL_NV_ALVO = 40010
ENDERECO_LOCAL_NV_RELIGAMENTO = 40011
ENDERECO_LOCAL_UG1_POT = 40019
ENDERECO_LOCAL_UG1_SETPOINT = 40020
ENDERECO_LOCAL_UG1_DISP = 40021
ENDERECO_LOCAL_UG2_POT = 40029
ENDERECO_LOCAL_UG2_SETPOINT = 40030
ENDERECO_LOCAL_UG2_DISP = 40031
ENDERECO_LOCAL_CLP_ONLINE = 40099
ENDERECO_LOCAL_STATUS_MOA = 40100

class ModbusClientFailedToOpen(Exception):
    pass


class FieldConnector:

    def __init__(self, ip_A, port_A, ip_B, port_B, cfg=None):

        self.ip_A = ip_A
        self.port_A = port_A
        self.ip_B = ip_B
        self.port_B = port_B
        self.modbus_clp_A = ModbusClient(host=self.ip_A, port=self.port_A, timeout=0.1, unit_id=1)
        #self.modbus_clp_B = ModbusClient(host=self.ip_B, port=self.port_B, timeout=0.1, unit_id=1)

    def open(self):
        if not self.modbus_clp_A.open():
            self.close()
            raise ModbusClientFailedToOpen("Modbus client ({}:{}) failed to open.".format(self.ip_A, self.port_A))
        #if not self.modbus_clp_B.open():
        #    self.close()
        #    raise ModbusClientFailedToOpen("Modbus client ({}:{}) failed to open.".format(self.ip_A, self.port_A))
        return self

    def close(self):
        self.modbus_clp_A.close()
        #self.modbus_clp_B.close()

    def get_emergencia_acionada(self):
        return int(self.modbus_clp_A.read_holding_registers(ENDERECO_CLP_USINA_FLAGS)[0])

    def get_nv_montante(self):
        return round(self.modbus_clp_A.read_holding_registers(ENDERECO_CLP_NV_MONATNTE)[0] * 0.001 + 620, 2)

    def get_pot_medidor(self):
        return round(self.modbus_clp_A.read_holding_registers(ENDERECO_CLP_MEDIDOR)[0] * 0.001, 3)

    def get_flags_ug1(self):
        return self.modbus_clp_A.read_holding_registers(ENDERECO_CLP_UG1_FLAGS)[0]
    
    def get_potencia_ug1(self):
        return self.modbus_clp_A.read_holding_registers(ENDERECO_CLP_UG1_POTENCIA)[0]/1000
    
    def get_horas_ug1(self):
        return self.modbus_clp_A.read_holding_registers(ENDERECO_CLP_UG1_MINUTOS)[0]/60
    
    def  get_perda_na_grade_ug1(self):
        return self.modbus_clp_A.read_holding_registers(ENDERECO_CLP_UG1_PERGA_GRADE)[0]/100
    
    def get_temperatura_do_mancal_ug1(self):
        return self.modbus_clp_A.read_holding_registers(ENDERECO_CLP_UG1_T_MANCAL)[0]/10

    def get_flags_ug2(self):
        return self.modbus_clp_A.read_holding_registers(ENDERECO_CLP_UG2_FLAGS)[0]
    
    def get_potencia_ug2(self):
        return self.modbus_clp_A.read_holding_registers(ENDERECO_CLP_UG2_POTENCIA)[0]/1000
    
    def get_horas_ug2(self):
        return self.modbus_clp_A.read_holding_registers(ENDERECO_CLP_UG2_MINUTOS)[0]/60
    
    def get_perda_na_grade_ug2(self):
        return self.modbus_clp_A.read_holding_registers(ENDERECO_CLP_UG2_PERGA_GRADE)[0]/100

    def get_temperatura_do_mancal_ug2(self):
        return self.modbus_clp_A.read_holding_registers(ENDERECO_CLP_UG2_T_MANCAL)[0]/10

    def get_tensao_na_linha(self):
        return self.modbus_clp_A.read_holding_registers(ENDERECO_CLP_TENSAO_NA_LINHA)[0]

    def set_ug1_flag(self, flags):
        self.modbus_clp_A.write_single_register(ENDERECO_CLP_UG1_FLAGS, flags)

    def set_ug1_setpoint(self, setpoint):
        self.modbus_clp_A.write_single_register(ENDERECO_CLP_UG1_SETPOINT, int(setpoint))

    def set_ug2_flag(self, flags):
        self.modbus_clp_A.write_single_register(ENDERECO_CLP_UG2_FLAGS, flags)

    def set_ug2_setpoint(self, setpoint):
        self.modbus_clp_A.write_single_register(ENDERECO_CLP_UG2_SETPOINT, int(setpoint))

    def set_pos_comporta(self, pos_comporta):
        self.modbus_clp_A.write_single_register(ENDERECO_CLP_COMPORTA_POS, int(pos_comporta))

    def acionar_emergencia(self, flags=1):
        if flags == 0:
            self.modbus_clp_A.write_single_register(ENDERECO_CLP_USINA_FLAGS, 1)
            raise ValueError("A emergencia deve ser acionada com uma flag válida. Recebido: {}".format(flags))
        else:
            self.modbus_clp_A.write_single_register(ENDERECO_CLP_USINA_FLAGS, flags)

    def normalizar_emergencia(self):
        self.modbus_clp_A.write_single_register(ENDERECO_CLP_USINA_FLAGS, 0)
        self.modbus_clp_A.write_single_register(ENDERECO_CLP_UG1_FLAGS, 0)
        self.modbus_clp_A.write_single_register(ENDERECO_CLP_UG2_FLAGS, 0)
