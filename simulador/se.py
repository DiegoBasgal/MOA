import logging
import numpy as np

from pyModbusTCP.server import DataBank

from dicts.const import *
from dicts.regs import REG
from funcs.temporizador import Temporizador


logger = logging.getLogger("__main__")


class Se:
    def __init__(self, dict_comp: "dict", tempo: "Temporizador", data_bank: "DataBank") -> "None":

        self.dict = dict_comp
        self.sim_db = data_bank
        self.escala_ruido = tempo.escala_ruido
        self.segundos_por_passo = tempo.segundos_por_passo

        self.aux_mola = 0
        self.tempo_carregamento_mola = 2

        self.avisou_trip = False

        self.abrir_dj()


    def passo(self) -> "None":

        self.verificar_tensao()
        self.verificar_mola_dj()
        self.verificar_condicao_dj()
        self.verificar_potencias()

        if self.sim_db.get_words(REG["SA_CMD_Fechar_Dj52L"])[0] == 1 or self.dict["SE"]["debug_dj_fechar"]:
            self.sim_db.set_words(REG["SA_CMD_Fechar_Dj52L"], [0])
            self.dict["SE"]["debug_dj_fechar"] = False
            self.fechar_dj()

        if self.dict["SE"]["debug_dj_fechar"] and self.dict["SE"]["debug_dj_abrir"]:
            self.dict["SE"]["debug_dj_abrir"] = False
            self.dict["SE"]["debug_dj_fechar"] = False
            self.dict["SE"]["dj_aberto"] = True
            self.dict["SE"]["dj_fechado"] = True
            self.tripar_dj()

        elif self.dict["SE"]["debug_dj_abrir"]:
            self.dict["SE"]["debug_dj_abrir"] = False
            self.abrir_dj()

        if self.dict["SE"]["debug_dj_reconhece_reset"]:
            self.reconhece_reset_dj()
            self.dict["SE"]["debug_dj_reconhece_reset"] = False

        if self.dict["SE"]["dj_aberto"] == self.dict["SE"]["dj_fechado"]:
            self.dict["SE"]["dj_inconsistente"] = True

        self.atualizar_modbus()


    def abrir_dj(self) -> "bool":
        logger.info("[SE]  Comando de Abertura Dj52L")

        if self.dict["SE"]["dj_mola_carregada"]:
            self.dict["SE"]["dj_aberto"] = True
            self.dict["SE"]["dj_fechado"] = False

        else:
            self.tripar_dj("A Mola do Dj52L não está carregada")
            return False

        self.dict["SE"]["dj_mola_carregada"] = False
        return True


    def fechar_dj(self) -> "bool":
        if self.dict["SE"]["dj_trip"]:
            self.dict["SE"]["dj_falha"] = True
            logger.warning("[SE]  Dj52L Picou!")
            return False

        else:
            if not self.dict["SE"]["dj_fechado"]:
                logger.info("[SE]  Comando de Fechamento Dj52L")

                if self.dict["SE"]["dj_condicao"]:
                    self.dict["SE"]["dj_aberto"] = False
                    self.dict["SE"]["dj_fechado"] = True

                else:
                    self.dict["SE"]["dj_falha"] = True
                    self.tripar_dj("Mandou antes de ter a condição de fechamento")
                    return False

                self.dict["SE"]["dj_mola_carregada"] = False
                return True


    def tripar_dj(self, desc: "str"=None) -> "None":
        if not self.avisou_trip:
            self.avisou_trip = True
            self.dict["SE"]["dj_trip"] = True
            self.dict["SE"]["dj_falha"] = True
            self.dict["SE"]["dj_aberto"] = True
            self.dict["SE"]["dj_fechado"] = False
            self.dict["SE"]["dj_mola_carregada"] = False

            logger.warning(f"[SE]  TRIP! {desc}")


    def reconhece_reset_dj(self) -> "None":
        logger.info("[SE]  Comando de Reconhece e Reset Dj52L")

        self.dict["SE"]["debug_dj_abrir"] = False
        self.dict["SE"]["debug_dj_fechar"] = False
        self.dict["SE"]["debug_dj_reconhece_reset"] = False

        self.dict["SE"]["dj_trip"] = False
        self.dict["SE"]["dj_falha"] = False
        self.dict["SE"]["dj_aberto"] = False
        self.dict["SE"]["dj_fechado"] = True
        self.dict["SE"]["dj_inconsistente"] = False
        self.avisou_trip = False


    def verificar_potencias(self) -> "None":
        self.dict["SE"]["potencia_se"] = (self.dict["UG1"]["potencia"]
                                        + self.dict["UG2"]["potencia"]
                                        + self.dict["UG3"]["potencia"]
                                        * 0.995)

        self.dict["SE"]["potencia_mp"] = (np.random.normal(self.dict["SE"]["potencia_se"] * 0.98, 10 * self.escala_ruido) - 20)
        self.dict["SE"]["potencia_mr"] = (np.random.normal(self.dict["SE"]["potencia_se"] * 0.98, 10 * self.escala_ruido) - 20)


    def verificar_tensao(self) -> "None":
        if not (USINA_TENSAO_MINIMA < self.dict["SE"]["tensao_linha"] < USINA_TENSAO_MAXIMA):
            self.dict["SE"]["dj_falta_vcc"] = True
            self.tripar_dj("Tensão fora dos limites")

        else:
            self.dict["SE"]["dj_falta_vcc"] = False


    def verificar_mola_dj(self) -> "None":
        if not self.dict["SE"]["dj_mola_carregada"]:
            self.aux_mola += self.segundos_por_passo

            if self.aux_mola >= self.tempo_carregamento_mola:
                self.aux_mola = 0
                self.dict["SE"]["dj_mola_carregada"] = True


    def verificar_condicao_dj(self) -> "None":
        if self.dict["SE"]["dj_trip"] \
            or self.dict["SE"]["dj_fechado"] \
            or self.dict["SE"]["dj_falta_vcc"] \
            or self.dict["SE"]["dj_inconsistente"] \
            or not self.dict["SE"]["dj_aberto"] \
            or not self.dict["SE"]["dj_mola_carregada"]:
            self.dict["SE"]["dj_condicao"] = False

        else:
            self.dict["SE"]["dj_condicao"] = True


    def atualizar_modbus(self) -> "None":
        self.sim_db.set_words(REG["SE_P"],[int(self.dict["SE"]["potencia_se"])])
        self.sim_db.set_words(REG["SE_R"],[int(self.dict["SE"]["tensao_linha"] / 1000)])
        self.sim_db.set_words(REG["SE_S"],[int(self.dict["SE"]["tensao_linha"] / 1000)])
        self.sim_db.set_words(REG["SE_T"],[int(self.dict["SE"]["tensao_linha"] / 1000)])