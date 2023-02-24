import logging
from time import sleep
from src.mapa_modbus import *
from pyModbusTCP.client import ModbusClient

logger = logging.getLogger("__main__")


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
            self.ug3_ip = cfg["UG3_slave_ip"]
            self.ug3_port = cfg["UG3_slave_porta"]
            self.usn_ip = cfg["USN_slave_ip"]
            self.usn_port = cfg["USN_slave_porta"]
            self.tda_ip = cfg["TDA_slave_ip"]
            self.tda_port = cfg["TDA_slave_porta"]
            self.ug1_clp = ModbusClient(
                host=self.ug1_ip,
                port=self.ug1_port,
                timeout=0.5,
                unit_id=1,
                auto_open=True,
            )
            self.ug2_clp = ModbusClient(
                host=self.ug2_ip,
                port=self.ug2_port,
                timeout=0.5,
                unit_id=1,
                auto_open=True,
            )
            self.ug3_clp = ModbusClient(
                host=self.ug3_ip,
                port=self.ug3_port,
                timeout=0.5,
                unit_id=1,
                auto_open=True,
            )
            self.usn_clp = ModbusClient(
                host=self.usn_ip,
                port=self.usn_port,
                timeout=0.5,
                unit_id=1,
                auto_open=True,
            )
            self.tda_clp = ModbusClient(
                host=self.tda_ip,
                port=self.tda_port,
                timeout=0.5,
                unit_id=1,
                auto_open=True,
            )

        self.warned_ug1 = False
        self.warned_ug2 = False
        self.warned_ug3 = False
        self.TDA_Offline = False

    def modifica_controles_locais(self):
        if not self.TDA_Offline:
            self.tda_clp.write_single_coil(REG_TDA_ComandosDigitais_MXW_ResetGeral, 1)
            self.tda_clp.write_single_coil(REG_TDA_ComandosDigitais_MXW_Hab_Nivel, 0)
            self.tda_clp.write_single_coil(REG_TDA_ComandosDigitais_MXW_Desab_Nivel, 1)
            self.tda_clp.write_single_coil(REG_TDA_ComandosDigitais_MXW_Hab_Religamento52L, 0)
            self.tda_clp.write_single_coil(REG_TDA_ComandosDigitais_MXW_Desab_Religamento52L, 1)
        else:
            logger.debug("Não é possível modificar os controles locais pois o CLP da TDA se encontra offline")

    def open(self):
        logger.debug("Opening Modbus")
        if not self.ug1_clp.open():
            raise ModbusClientFailedToOpen("Modbus client ({}:{}) failed to open.".format(self.ug1_ip, self.ug1_port))

        if not self.ug2_clp.open():
            raise ModbusClientFailedToOpen("Modbus client ({}:{}) failed to open.".format(self.ug2_ip, self.ug2_port))

        if not self.ug3_clp.open():
            raise ModbusClientFailedToOpen("Modbus client ({}:{}) failed to open.".format(self.ug3_ip, self.ug3_port))

        if not self.usn_clp.open():
            raise ModbusClientFailedToOpen("Modbus client ({}:{}) failed to open.".format(self.usn_ip, self.usn_port))

        if not self.tda_clp.open():
            raise ModbusClientFailedToOpen("Modbus client ({}:{}) failed to open.".format(self.tda_ip, self.tda_port))

        logger.debug("Openned Modbus")
        return self

    def close(self):
        logger.debug("Closing Modbus")
        self.ug1_clp.close()
        self.ug2_clp.close()
        self.ug3_clp.close()
        self.usn_clp.close()
        self.tda_clp.close()
        logger.debug("Closed Modbus")

    def fechaDj52L(self):
        if self.get_flag_falha52L():
            return False
        else:
            # utilizar o write_single_coil para o ambiente em produção e write_single_register para a simulação
            response = self.usn_clp.write_single_coil(REG_SA_ComandosDigitais_MXW_Liga_DJ1, 1)
            return response

    def normalizar_emergencia(self):
        logger.info("Reconhecendo alarmes, resetando usina e fechando Dj52L")
        logger.debug("Reconhece/Reset alarmes")
        self.ug1_clp.write_single_coil(REG_UG1_ComandosDigitais_MXW_ResetGeral, 1)
        self.ug2_clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_ResetGeral, 1)
        self.ug3_clp.write_single_coil(REG_UG3_ComandosDigitais_MXW_ResetGeral, 1)
        self.usn_clp.write_single_coil(REG_SA_ComandosDigitais_MXW_ResetGeral, 1)
        self.tda_clp.write_single_coil(REG_TDA_ComandosDigitais_MXW_ResetGeral, 1) if not self.TDA_Offline else logger.debug("CLP TDA Offline, não há como realizar o reset geral")
        self.ug1_clp.write_single_coil(REG_UG1_ComandosDigitais_MXW_Cala_Sirene, 1)
        self.ug2_clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_Cala_Sirene, 1)
        self.ug3_clp.write_single_coil(REG_UG3_ComandosDigitais_MXW_Cala_Sirene, 1)
        self.usn_clp.write_single_coil(REG_SA_ComandosDigitais_MXW_Cala_Sirene, 1)
        logger.debug("Fecha Dj52L")
        self.fechaDj52L()

    def somente_reconhecer_emergencia(self):
        logger.debug("Somente reconhece alarmes não implementado em SEB")
        self.ug1_clp.write_single_coil(REG_UG1_ComandosDigitais_MXW_Cala_Sirene, 1)
        self.ug2_clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_Cala_Sirene, 1)
        self.ug3_clp.write_single_coil(REG_UG3_ComandosDigitais_MXW_Cala_Sirene, 1)
        self.usn_clp.write_single_coil(REG_SA_ComandosDigitais_MXW_Cala_Sirene, 1)

    def acionar_emergencia(self):
        logger.warning("FC: Acionando emergencia")
        self.ug1_clp.write_single_coil(REG_UG1_ComandosDigitais_MXW_EmergenciaViaSuper, 1)
        self.ug2_clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_EmergenciaViaSuper, 1)
        self.ug3_clp.write_single_coil(REG_UG3_ComandosDigitais_MXW_EmergenciaViaSuper, 1)
        sleep(5)
        self.ug1_clp.write_single_coil(REG_UG1_ComandosDigitais_MXW_EmergenciaViaSuper, 0)
        self.ug2_clp.write_single_coil(REG_UG2_ComandosDigitais_MXW_EmergenciaViaSuper, 0)
        self.ug3_clp.write_single_coil(REG_UG3_ComandosDigitais_MXW_EmergenciaViaSuper, 0)

    def get_flag_falha52L(self):
        # adicionar estado do disjuntor
        if self.usn_clp.read_discrete_inputs(REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert1)[0] == 0:
            logger.info("DisjDJ1_SuperBobAbert1")
            return True

        if self.usn_clp.read_discrete_inputs(REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert2)[0] == 0:
            logger.info("DisjDJ1_SuperBobAbert2")
            return True

        if self.usn_clp.read_discrete_inputs(REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiMot)[0] == 0:
            logger.info("DisjDJ1_Super125VccCiMot")
            return True

        if self.usn_clp.read_discrete_inputs(REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiCom)[0] == 0:
            logger.info("DisjDJ1_Super125VccCiCom")
            return True

        if self.usn_clp.read_discrete_inputs(REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa)[0] == 1:
            logger.info("DisjDJ1_AlPressBaixa")
            return True

        if self.usn_clp.read_discrete_inputs(REG_SA_RetornosDigitais_MXR_DJ1_FalhaInt)[0] == 1:
            logger.info("MXR_DJ1_FalhaInt")
            return True

        if self.usn_clp.read_discrete_inputs(REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa)[0] == 1:
            logger.info("DisjDJ1_BloqPressBaixa")
            return True

        if self.usn_clp.read_discrete_inputs(REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb1)[0] == 0:
            logger.info("DisjDJ1_Sup125VccBoFeAb1")
            return True

        if self.usn_clp.read_discrete_inputs(REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb2)[0] == 0:
            logger.info("DisjDJ1_Sup125VccBoFeAb2")
            return True

        if self.usn_clp.read_discrete_inputs(REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Local)[0] == 1:
            logger.info("DisjDJ1_Local")
            return True

        if self.usn_clp.read_discrete_inputs(REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_MolaDescarregada)[0] == 1:
            logger.info("DisjDJ1_MolaDescarregada")
            return True

        return False
