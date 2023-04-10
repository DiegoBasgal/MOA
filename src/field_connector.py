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

        if not cfg:
            raise ValueError("Arquivo de configurção \"config.json\" não carregado.")
        else:
            self.cfg = cfg

        self.clp_sa = ModbusClient(
            host=self.cfg["USN_slave_ip"],
            port=self.cfg["USN_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
        )
        self.clp_tda = ModbusClient(
            host=self.cfg["TDA_slave_ip"],
            port=self.cfg["TDA_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
        )
        self.clp_ug1 = ModbusClient(
            host=self.cfg["UG1_slave_ip"],
            port=self.cfg["UG1_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
        )
        self.clp_ug2 = ModbusClient(
            host=self.cfg["UG2_slave_ip"],
            port=self.cfg["UG2_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
        )
        self.clp_ug3 = ModbusClient(
            host=self.cfg["UG3_slave_ip"],
            port=self.cfg["UG3_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
        )

        self.TDA_Offline = False

    def modifica_controles_locais(self):
        if not self.TDA_Offline:
            self.clp_tda.write_single_coil(REG_TDA_CD_ResetGeral, 1)
            self.clp_tda.write_single_coil(REG_TDA_CD_Hab_Nivel, 0)
            self.clp_tda.write_single_coil(REG_TDA_CD_Desab_Nivel, 1)
            self.clp_tda.write_single_coil(REG_TDA_CD_Hab_Religamento52L, 0)
            self.clp_tda.write_single_coil(REG_TDA_CD_Desab_Religamento52L, 1)
        else:
            logger.debug("Não é possível modificar os controles locais pois o CLP da TDA se encontra offline")

    def open(self):
        logger.debug("Opening Modbus")
        if not self.clp_ug1.open():
            raise ModbusClientFailedToOpen(f"Modbus client ({self.cfg['UG1_slave_ip']}:{self.cfg['UG1_slave_porta']}) failed to open.")

        if not self.clp_ug2.open():
            raise ModbusClientFailedToOpen(f"Modbus client ({self.cfg['UG2_slave_ip']}:{self.cfg['UG2_slave_porta']}) failed to open.")

        if not self.clp_ug3.open():
            raise ModbusClientFailedToOpen(f"Modbus client ({self.cfg['UG3_slave_ip']}:{self.cfg['UG3_slave_porta']}) failed to open.")

        if not self.clp_sa.open():
            raise ModbusClientFailedToOpen(f"Modbus client ({self.cfg['USN_slave_ip']}:{self.cfg['USN_slave_porta']}) failed to open.")

        if not self.clp_tda.open():
            raise ModbusClientFailedToOpen(f"Modbus client ({self.cfg['TDA_slave_ip']}:{self.cfg['TDA_slave_porta']}) failed to open.")

        logger.debug("Openned Modbus")
        return self

    def close(self):
        logger.debug("Closing Modbus")
        self.clp_ug1.close()
        self.clp_ug2.close()
        self.clp_ug3.close()
        self.clp_sa.close()
        self.clp_tda.close()
        logger.debug("Closed Modbus")

    def fechaDj52L(self):
        if self.get_flag_falha52L():
            return False
        else:
            # utilizar o write_single_coil para o ambiente em produção e write_single_register para a simulação
            response = self.clp_sa.write_single_coil(REG_SA_CD_Liga_DJ1, 1)
            return response

    def normalizar_emergencia(self):
        logger.debug("Reconhecendo alarmes, resetando usina e fechando Dj52L")
        logger.debug("Reconhece/Reset alarmes")
        self.clp_ug1.write_single_coil(UG[f"REG_UG1_CD_ResetGeral"], 1)
        self.clp_ug2.write_single_coil(UG[f"REG_UG2_CD_ResetGeral"], 1)
        self.clp_ug3.write_single_coil(UG[f"REG_UG3_CD_ResetGeral"], 1)
        self.clp_sa.write_single_coil(REG_SA_CD_ResetGeral, 1)
        self.clp_tda.write_single_coil(REG_TDA_CD_ResetGeral, 1) if not self.TDA_Offline else logger.debug("CLP TDA Offline, não há como realizar o reset geral")
        self.clp_ug1.write_single_coil(REG_UG1_CD_Cala_Sirene, 1)
        self.clp_ug2.write_single_coil(REG_UG2_CD_Cala_Sirene, 1)
        self.clp_ug3.write_single_coil(REG_UG3_CD_Cala_Sirene, 1)
        self.clp_sa.write_single_coil(REG_SA_CD_Cala_Sirene, 1)
        logger.debug("Fecha Dj52L")
        self.fechaDj52L()

    def somente_reconhecer_emergencia(self):
        logger.debug("Somente reconhece alarmes não implementado em SEB")
        self.clp_ug1.write_single_coil(REG_UG1_CD_Cala_Sirene, 1)
        self.clp_ug2.write_single_coil(REG_UG2_CD_Cala_Sirene, 1)
        self.clp_ug3.write_single_coil(REG_UG3_CD_Cala_Sirene, 1)
        self.clp_sa.write_single_coil(REG_SA_CD_Cala_Sirene, 1)

    def acionar_emergencia(self):
        logger.warning("FC: Acionando emergencia")
        self.clp_ug1.write_single_coil(REG_UG1_CD_EmergenciaViaSuper, 1)
        self.clp_ug2.write_single_coil(REG_UG2_CD_EmergenciaViaSuper, 1)
        self.clp_ug3.write_single_coil(REG_UG3_CD_EmergenciaViaSuper, 1)
        sleep(5)
        self.clp_ug1.write_single_coil(REG_UG1_CD_EmergenciaViaSuper, 0)
        self.clp_ug2.write_single_coil(REG_UG2_CD_EmergenciaViaSuper, 0)
        self.clp_ug3.write_single_coil(REG_UG3_CD_EmergenciaViaSuper, 0)

    def get_flag_falha52L(self):
        # adicionar estado do disjuntor
        flag = 0

        if self.clp_sa.read_discrete_inputs(REG_SA_ED_SA_DisjDJ1_SuperBobAbert1)[0] == 0:
            logger.debug("DisjDJ1_SuperBobAbert1")
            flag += 1

        if self.clp_sa.read_discrete_inputs(REG_SA_ED_SA_DisjDJ1_SuperBobAbert2)[0] == 0:
            logger.debug("DisjDJ1_SuperBobAbert2")
            flag += 1

        if self.clp_sa.read_discrete_inputs(REG_SA_ED_SA_DisjDJ1_Super125VccCiMot)[0] == 0:
            logger.debug("DisjDJ1_Super125VccCiMot")
            flag += 1

        if self.clp_sa.read_discrete_inputs(REG_SA_ED_SA_DisjDJ1_Super125VccCiCom)[0] == 0:
            logger.debug("DisjDJ1_Super125VccCiCom")
            flag += 1

        if self.clp_sa.read_discrete_inputs(REG_SA_ED_SA_DisjDJ1_AlPressBaixa)[0] == 1:
            logger.debug("DisjDJ1_AlPressBaixa")
            flag += 1

        if self.clp_sa.read_discrete_inputs(REG_SA_RD_DJ1_FalhaInt)[0] == 1:
            logger.debug("MXR_DJ1_FalhaInt")
            flag += 1

        if self.clp_sa.read_discrete_inputs(REG_SA_ED_SA_DisjDJ1_BloqPressBaixa)[0] == 1:
            logger.debug("DisjDJ1_BloqPressBaixa")
            flag += 1

        if self.clp_sa.read_discrete_inputs(REG_SA_ED_SA_DisjDJ1_Sup125VccBoFeAb1)[0] == 0:
            logger.debug("DisjDJ1_Sup125VccBoFeAb1")
            flag += 1

        if self.clp_sa.read_discrete_inputs(REG_SA_ED_SA_DisjDJ1_Sup125VccBoFeAb2)[0] == 0:
            logger.debug("DisjDJ1_Sup125VccBoFeAb2")
            flag += 1

        if self.clp_sa.read_discrete_inputs(REG_SA_ED_SA_DisjDJ1_Local)[0] == 1:
            logger.debug("DisjDJ1_Local")
            flag += 1

        if self.clp_sa.read_discrete_inputs(REG_SA_ED_SA_DisjDJ1_MolaDescarregada)[0] == 1:
            logger.debug("DisjDJ1_MolaDescarregada")
            flag += 1

        if flag > 0:
            logger.warning(f"Foram detectados bloqueios ao fechar o Dj52L. Número de bloqueios: \"{flag}\".")
            return True
        else:
            return False
