import logging
import traceback

from time import sleep

from usina import *
from dicionarios.reg import *
from dicionarios.const import *

logger = logging.getLogger("__main__")

class ConectorCampo(Usina):
    def __init__(self, cfg: dict=None, clp: "dict[str, ModbusClient]"=None):
        super().__init__(cfg, clp)

    def normalizar_emergencia(self) -> None:
        logger.info("[CON] Normalizando emergência...")
        self.resetar_emergencia()
        self.reconhecer_emergencia()
        self.fechaDj52L()

    def resetar_emergencia(self) -> None:
        try:
            logger.debug("[CON] Reset geral.")
            self.clp["SA"].write_single_coil(SA["SA_CD_ResetGeral"], [1])
            self.clp["UG1"].write_single_coil(UG["UG1_CD_ResetGeral"], [1])
            self.clp["UG2"].write_single_coil(UG["UG2_CD_ResetGeral"], [1])
            self.clp["TDA"].write_single_coil(TDA["TDA_CD_ResetGeral"], [1]) if not self.tda_offline else logger.debug("[CON] CLP TDA Offline, não há como realizar o reset geral")

        except Exception:
            logger.error(f"[CON] Houve um erro ao realizar o reset geral.")
            logger.debug(f"[CON] Traceback: {traceback.format_exc()}")

    def reconhecer_emergencia(self) -> None:
        try:
            logger.debug("[CON] Cala sirene.")
            self.clp["SA"].write_single_coil(SA["SA_CD_Cala_Sirene"], [1])
            self.clp["UG1"].write_single_coil(UG["UG1_CD_Cala_Sirene"], [1])
            self.clp["UG2"].write_single_coil(UG["UG2_CD_Cala_Sirene"], [1])

        except Exception:
            logger.error(f"[CON] Houve um erro ao reconhecer os alarmes.")
            logger.debug(f"[CON] Traceback: {traceback.format_exc()}")

    def acionar_emergencia(self) -> None:
        try:
            logger.warning("[CON] Acionando emergência.")
            self.clp["UG1"].write_single_coil(UG["UG1_CD_EmergenciaViaSuper"], [1])
            self.clp["UG2"].write_single_coil(UG["UG2_CD_EmergenciaViaSuper"], [1])
            sleep(5)
            self.clp["UG1"].write_single_coil(UG["UG1_CD_EmergenciaViaSuper"], [0])
            self.clp["UG2"].write_single_coil(UG["UG2_CD_EmergenciaViaSuper"], [0])

        except Exception:
            logger.error(f"[CON] Houve um erro ao acionar a emergência.")
            logger.debug(f"[CON] Traceback: {traceback.format_exc()}")

    def modifica_controles_locais(self) -> None:
        try:
            if not self.tda_offline:
                self.clp["TDA"].write_single_coil(TDA["TDA_CD_ResetGeral"], [1])
                self.clp["TDA"].write_single_coil(TDA["TDA_CD_Hab_Nivel"], [0])
                self.clp["TDA"].write_single_coil(TDA["TDA_CD_Desab_Nivel"], [1])
                self.clp["TDA"].write_single_coil(TDA["TDA_CD_Hab_Religamento52L"], [0])
                self.clp["TDA"].write_single_coil(TDA["TDA_CD_Desab_Religamento52L"], [1])
            else:
                logger.debug("[CON] Não é possível modificar os controles locais pois o CLP da TDA se encontra offline")

        except Exception:
            logger.error(f"[CON] Houve um erro ao modificar os controles locais.")
            logger.debug(f"[CON] Traceback: {traceback.format_exc()}")

    def fechaDj52L(self) -> bool:
        try:
            if self.get_falha52L():
                return False
            else:
                response = self.clp["SA"].write_single_register(SA["SA_CD_Liga_DJ1"], 1)
                return response

        except Exception:
            logger.error(f"[CON] Houver um erro ao fechar o Dj52L.")
            logger.debug(f"[CON] Traceback: {traceback.format_exc()}")
            return False

    def get_falha52L(self) -> bool:
        dict_flags: "dict[str, int]" = {
            SA["SA_RD_DJ1_FalhaInt"]: 1,
            SA["SA_ED_DisjDJ1_Local"]: 1,
            SA["SA_ED_DisjDJ1_AlPressBaixa"]: 1,
            SA["SA_ED_DisjDJ1_BloqPressBaixa"]: 1,
            SA["SA_ED_DisjDJ1_SuperBobAbert2"]: 0,
            SA["SA_ED_DisjDJ1_Sup125VccBoFeAb1"]: 0,
            SA["SA_ED_DisjDJ1_Super125VccCiMot"]: 0,
            SA["SA_ED_DisjDJ1_Super125VccCiCom"]: 0,
            SA["SA_ED_DisjDJ1_Sup125VccBoFeAb2"]: 0,
        }

        try:
            flags = 0
            for nome, valor in zip(dict_flags[0], dict_flags.values()):
                if self.clp["SA"].read_discrete_inputs(nome)[0] == valor:
                    logger.debug(f"[CON] Flag -> {nome.keys()}")
                    flags += 1

            logger.info(f"[CON] Foram detectadas Flags de bloqueio ao abrir o Dj52L. Número de bloqueios ativos: \"{flags}\"") if flags else ...
            return True if flags >= 1 else False

        except Exception:
            logger.error(f"[CON] Houve um erro ao ler as flags do Dj52L.")
            logger.debug(f"[CON] Traceback: {traceback.format_exc()}")
            return None