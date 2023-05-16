import logging

from time import sleep
from pyModbusTCP.client import ModbusClient
from src.banco_dados import Database

from src.usina import *
from src.dicionarios.regs import *

logger = logging.getLogger("__main__")

class ConectorCampo(Usina):
    def __init__(self, cfg=None, clp:"dict[str, ModbusClient]"=None):
        super().__init__(cfg, clp)

    def modifica_controles_locais(self):
        if not self.TDA_Offline:
            self.clp["TDA"].write_single_coil(REG["TDA_CD_ResetGeral"], [1])
            self.clp["TDA"].write_single_coil(REG["TDA_CD_Hab_Nivel"], [0])
            self.clp["TDA"].write_single_coil(REG["TDA_CD_Desab_Nivel"], [1])
            self.clp["TDA"].write_single_coil(REG["TDA_CD_Hab_Religamento52L"], [0])
            self.clp["TDA"].write_single_coil(REG["TDA_CD_Desab_Religamento52L"], [1])
        else:
            logger.debug("Não é possível modificar os controles locais pois o CLP da TDA se encontra offline")

    def fechaDj52L(self):
        if self.get_flag_falha52L():
            return False
        else:
            response = self.clp["SA"].write_single_coil(REG["SA_CD_Liga_DJ1"], [1])
            return response

    def normalizar_emergencia(self):
        logger.debug("Reconhecendo alarmes, resetando usina e fechando Dj52L")
        logger.debug("Reconhece/Reset alarmes")
        self.clp["UG1"].write_single_coil(REG["UG1_CD_ResetGeral"], [1])
        self.clp["UG2"].write_single_coil(REG["UG2_CD_ResetGeral"], [1])
        self.clp["UG3"].write_single_coil(REG["UG3_CD_ResetGeral"], [1])
        self.clp["SA"].write_single_coil(REG["SA_CD_ResetGeral"], [1])
        self.clp["TDA"].write_single_coil(REG["TDA_CD_ResetGeral"], [1]) if not self.TDA_Offline else logger.debug("CLP TDA Offline, não há como realizar o reset geral")
        self.clp["UG1"].write_single_coil(REG["UG1_CD_Cala_Sirene"], [1])
        self.clp["UG2"].write_single_coil(REG["UG2_CD_Cala_Sirene"], [1])
        self.clp["UG3"].write_single_coil(REG["UG3_CD_Cala_Sirene"], [1])
        self.clp["SA"].write_single_coil(REG["SA_CD_Cala_Sirene"], [1])
        logger.debug("Fecha Dj52L")
        self.fechaDj52L()

    def somente_reconhecer_emergencia(self):
        logger.debug("Somente reconhece alarmes não implementado em SEB")
        self.clp["UG1"].write_single_coil(REG["UG1_CD_Cala_Sirene"], [1])
        self.clp["UG2"].write_single_coil(REG["UG2_CD_Cala_Sirene"], [1])
        self.clp["UG3"].write_single_coil(REG["UG3_CD_Cala_Sirene"], [1])
        self.clp["SA"].write_single_coil(REG["SA_CD_Cala_Sirene"], [1])

    def acionar_emergencia(self):
        logger.warning("FC: Acionando emergencia")
        self.clp["UG1"].write_single_coil(REG["UG1_CD_EmergenciaViaSuper"], [1])
        self.clp["UG2"].write_single_coil(REG["UG2_CD_EmergenciaViaSuper"], [1])
        self.clp["UG3"].write_single_coil(REG["UG3_CD_EmergenciaViaSuper"], [1])
        sleep(5)
        self.clp["UG1"].write_single_coil(REG["UG1_CD_EmergenciaViaSuper"], [0])
        self.clp["UG2"].write_single_coil(REG["UG2_CD_EmergenciaViaSuper"], [0])
        self.clp["UG3"].write_single_coil(REG["UG3_CD_EmergenciaViaSuper"], [0])
        self.clp_emergencia_acionada = 1

    def get_flag_falha52L(self):
        flag = 0

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_SuperBobAbert1"])[0] == 0:
            logger.debug("DisjDJ1_SuperBobAbert1")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_SuperBobAbert2"])[0] == 0:
            logger.debug("DisjDJ1_SuperBobAbert2")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_Super125VccCiMot"])[0] == 0:
            logger.debug("DisjDJ1_Super125VccCiMot")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_Super125VccCiCom"])[0] == 0:
            logger.debug("DisjDJ1_Super125VccCiCom")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_AlPressBaixa"])[0] == 1:
            logger.debug("DisjDJ1_AlPressBaixa")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_RD_DJ1_FalhaInt"])[0] == 1:
            logger.debug("MXR_DJ1_FalhaInt")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_BloqPressBaixa"])[0] == 1:
            logger.debug("DisjDJ1_BloqPressBaixa")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_Sup125VccBoFeAb1"])[0] == 0:
            logger.debug("DisjDJ1_Sup125VccBoFeAb1")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_Sup125VccBoFeAb2"])[0] == 0:
            logger.debug("DisjDJ1_Sup125VccBoFeAb2")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_Local"])[0] == 1:
            logger.debug("DisjDJ1_Local")
            flag += 1

        if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_MolaDescarregada"])[0] == 1:
            logger.debug("DisjDJ1_MolaDescarregada")
            flag += 1

        if flag > 0:
            logger.warning(f"Foram detectados bloqueios ao fechar o Dj52L. Número de bloqueios: \"{flag}\".")
            return True
        else:
            return False
