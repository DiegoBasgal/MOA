import logging
import numpy as np

from logging.config import fileConfig
from pyModbusTCP.server import DataBank

from dicts.const import *
from dicts.regs import REG
from funcs.temporizador import Temporizador


fileConfig("C:/opt/operacao-autonoma/logger_config.ini")
logger = logging.getLogger("sim")


class Ug:
    def __init__(self, id: "int", dict_comp: "dict", tempo: "Temporizador", data_bank: "DataBank") -> "None":
        self.id = id

        self.dict = dict_comp
        self.sim_db = data_bank
        self.escala_ruido = tempo.escala_ruido
        self.segundos_por_passo = tempo.segundos_por_passo

        self.flags = 0
        self.potencia = 0
        self.setpoint = 0
        self.etapa_alvo = 0
        self.etapa_atual = 1
        self.horimetro_hora = 0
        self.tempo_na_transicao = 0

        self.b_condic = False
        self.avisou_trip = False


    def passo(self) -> "None":
        self.setpoint = self.sim_db.get_words(REG[f"UG{self.id}_Setpoint"])[0]
        self.dict[f"UG{self.id}"]["setpoint"] = self.setpoint

        if self.dict[f"UG{self.id}"]["debug_setpoint"] >= 0:
            self.dict[f"UG{self.id}"]["setpoint"] = self.dict[f"UG{self.id}"]["debug_setpoint"]
            self.sim_db.set_words(REG[f"UG{self.id}_Setpoint"], [self.dict[f"UG{self.id}"]["setpoint"]])
            self.dict[f"UG{self.id}"]["debug_setpoint"] = -1

        if self.sim_db.get_words(REG[f"UG{self.id}_CMD_Partida"])[0] == 1 or self.dict[f"UG{self.id}"]["debug_partir"]:
            self.sim_db.set_words(REG[f"UG{self.id}_CMD_Partida"], [0])
            self.dict[f"UG{self.id}"]["debug_partir"] = False
            self.partir()

        if self.sim_db.get_words(REG[f"UG{self.id}_CMD_Parada"])[0] == 1 or self.dict[f"UG{self.id}"]["debug_parar"]:
            self.sim_db.set_words(REG[f"UG{self.id}_CMD_Parada"], [0])
            self.dict[f"UG{self.id}"]["debug_parar"] = False
            self.parar()

        if self.sim_db.get_words(REG[f"UG{self.id}_CMD_Emergencia"])[0] == 1 or self.dict[f"UG{self.id}"]["trip"]:
            self.sim_db.set_words(REG[f"UG{self.id}_CMD_Emergencia"], [0])
            self.tripar(1, "Comando de TRIP")

        if self.sim_db.get_words(REG[f"UG{self.id}_CMD_ResetGeral"])[0] == 1 or self.dict[f"UG{self.id}"]["reconhece_reset"]:
            self.sim_db.set_words(REG[f"UG{self.id}_CMD_ResetGeral"], [0])
            self.sim_db.set_words(REG[f"UG{self.id}_CMD_CalaSirene"], [0])
            self.reconhece_reset()
            self.flags = 0
            self.dict[f"UG{self.id}"]["trip"] = False
            self.dict[f"UG{self.id}"]["reconhece_reset"] = False

        if self.dict[f"UG{self.id}"]["condicionador"] and not self.b_condic:
            self.b_condic = True
            self.sim_db.set_words(REG[f"UG{self.id}_Condicionador"], [1])

        elif not self.dict[f"UG{self.id}"]["condicionador"] and self.b_condic:
            self.b_condic = False
            self.sim_db.set_words(REG[f"UG{self.id}_Condicionador"], [0])

        self.controlar_etapas()
        self.ajustar_horimetro()
        self.verificar_reservatorio()
        self.atualizar_modbus()


    def partir(self) -> "None":
        logger.info(f"[UG{self.id}] Comando de Partida")
        self.dict[f"UG{self.id}"]["etapa_alvo"] = self.etapa_alvo = ETAPA_US


    def parar(self) -> "None":
        logger.info(f"[UG{self.id}] Comando de Parada")
        self.dict[f"UG{self.id}"]["etapa_alvo"] = self.etapa_alvo = ETAPA_UP


    def reconhece_reset(self) -> "None":
        logger.info(f"[UG{self.id}] Comando de Reconhece e Reset")
        self.flags = 0
        self.avisou_trip = False


    def tripar(self, flag: "int", desc: "str"=None) -> "None":
        if not self.avisou_trip:
            self.avisou_trip = True
            logger.warning(f"[UG{self.id}] TRIP! Descrição: \"{desc}\"")

        self.flags = flag
        self.potencia = 0
        self.dict[f"UG{self.id}"]["etapa_alvo"] = self.etapa_alvo = ETAPA_UP
        self.dict[f"UG{self.id}"]["etapa_atual"] = self.etapa_atual = ETAPA_UP


    def calcular_q_ug(self, potencia_kW) -> "float":
        return 0.00065 * potencia_kW if potencia_kW > 1 else 0


    def ajustar_horimetro(self) -> "None":
        if self.etapa_atual > ETAPA_UP:
            self.horimetro_hora += self.segundos_por_passo / 3600


    def verificar_reservatorio(self) -> "None":
        if self.etapa_atual > ETAPA_UP and self.dict["TDA"]["nv_montante"] < USINA_NV_MINIMO_OPERACAO:
            self.potencia = 0
            self.dict[f"UG{self.id}"]["etapa_alvo"] = self.etapa_alvo = ETAPA_UP
            self.dict[f"UG{self.id}"]["etapa_atual"] = self.etapa_atual = ETAPA_UP

        self.dict[f"UG{self.id}"]["flags"] = self.flags
        self.dict[f"UG{self.id}"]["potencia"] = self.potencia
        self.dict[f"UG{self.id}"]["etapa_atual"] = self.etapa_atual
        self.dict[f"UG{self.id}"]["q"] = self.calcular_q_ug(self.potencia)


    def controlar_limites(self) -> "None":
        self.dict[f"UG{self.id}"]["tmp_fase_r"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"]["tmp_fase_s"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"]["tmp_fase_t"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"]["tmp_saida_ar"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"]["tmp_nucleo_estator"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"]["tmp_mancal_radial_dia_1"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"]["tmp_mancal_radial_dia_2"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"]["tmp_mancal_radial_tra_1"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"]["tmp_mancal_radial_tra_2"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"]["tmp_mancal_guia_escora"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"]["tmp_mancal_guia_radial"] = np.random.normal(25, 1 * self.escala_ruido)
        self.dict[f"UG{self.id}"]["tmp_mancal_guia_contra_escora"] = np.random.normal(25, 1 * self.escala_ruido)

        self.dict[f"UG{self.id}"]["pressao_cx_espiral"] = np.random.normal(20, 1 * self.escala_ruido)


    def controlar_etapas(self) -> "None":
        # Unidade Parada
        if self.etapa_atual == ETAPA_UP:
            self.potencia = 0
            self.dict[f"UG{self.id}"]["etapa_aux"] = UG_PARADA

            if self.etapa_alvo == self.etapa_atual:
                self.tempo_na_transicao = 0
                self.dict[f"UG{self.id}"]["etapa_alvo"] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo

                if self.tempo_na_transicao >= TEMPO_TRANS_US_UPS:
                    self.dict[f"UG{self.id}"]["etapa_atual"] = self.etapa_atual = ETAPA_UPGM
                    self.dict[f"UG{self.id}"]["etapa_aux"] = UG_SINCRONIZANDO
                    self.tempo_na_transicao = 0

        # Unidade Pronta para Giro Mecânico
        if self.etapa_atual == ETAPA_UPGM:
            self.potencia = 0

            if self.etapa_alvo == self.etapa_atual:
                self.tempo_na_transicao = 0
                self.dict[f"UG{self.id}"]["etapa_alvo"] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo

                if self.tempo_na_transicao >= TEMPO_TRANS_UPGM_UVD:
                    self.dict[f"UG{self.id}"]["etapa_atual"] = self.etapa_atual = ETAPA_UVD
                    self.dict[f"UG{self.id}"]["etapa_aux"] = UG_SINCRONIZANDO
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo

                if self.tempo_na_transicao <= -TEMPO_TRANS_UPGM_UP:
                    self.dict[f"UG{self.id}"]["etapa_atual"] = self.etapa_atual = ETAPA_UP
                    self.dict[f"UG{self.id}"]["etapa_aux"] = UG_PARANDO
                    self.tempo_na_transicao = 0

        # Unidade Vazio Desescitado
        if self.etapa_atual == ETAPA_UVD:
            self.potencia = 0

            if self.etapa_alvo == self.etapa_atual:
                self.tempo_na_transicao = 0
                self.dict[f'UG{self.id}']['etapa_alvo'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo

                if self.tempo_na_transicao >= TEMPO_TRANS_UVD_UPS:
                    self.dict[f'UG{self.id}']['etapa_atual'] = self.etapa_atual = ETAPA_UPS
                    self.dict[f"UG{self.id}"]["etapa_aux"] = UG_SINCRONIZANDO
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo

                if self.tempo_na_transicao <= -TEMPO_TRANS_UVD_UPGM:
                    self.dict[f'UG{self.id}']['etapa_atual'] = self.etapa_atual = ETAPA_UPGM
                    self.dict[f"UG{self.id}"]["etapa_aux"] = UG_PARANDO
                    self.tempo_na_transicao = 0

        # Unidade Pronta para Sincronismo
        if self.etapa_atual == ETAPA_UPS:
            self.potencia = 0

            if self.etapa_alvo == self.etapa_atual:
                self.tempo_na_transicao = 0
                self.dict[f'UG{self.id}']['etapa_alvo'] = self.etapa_alvo

            elif self.etapa_alvo > self.etapa_atual:
                self.tempo_na_transicao += self.segundos_por_passo

                if self.tempo_na_transicao >= TEMPO_TRANS_UPS_US and self.dict['SE']['dj_fechado']:
                    self.dict[f'UG{self.id}']['etapa_atual'] = self.etapa_atual = ETAPA_US
                    self.dict[f"UG{self.id}"]["etapa_aux"] = UG_SINCRONIZANDO
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo

                if self.tempo_na_transicao <= -TEMPO_TRANS_UPS_UVD:
                    self.dict[f'UG{self.id}']['etapa_atual'] = self.etapa_atual = ETAPA_UVD
                    self.dict[f"UG{self.id}"]["etapa_aux"] = UG_PARANDO
                    self.tempo_na_transicao = 0

        # Unidade Sincronizada
        if self.etapa_atual == ETAPA_US:
            if self.etapa_alvo == self.etapa_atual:
                self.tempo_na_transicao = 0
                self.dict[f"UG{self.id}"]["etapa_alvo"] = self.etapa_alvo

                if self.dict["SE"]["dj_fechado"]:
                    self.dict[f"UG{self.id}"]["etapa_aux"] = UG_SINCRONIZADA
                    self.dict[f"UG{self.id}"]["potencia"] = self.potencia = min(max(self.potencia, POT_MIN), POT_MAX)

                    if self.setpoint > self.potencia:
                        self.potencia += 10.4167 * self.segundos_por_passo
                    else:
                        self.potencia -= 10.4167 * self.segundos_por_passo

                    self.potencia = np.random.normal(self.potencia, 1 * self.escala_ruido)

                if self.dict["SE"]["dj_aberto"] or self.dict["SE"]["dj_trip"]:
                    self.dict[f"UG{self.id}"]["etapa_alvo"] = self.etapa_alvo = ETAPA_UP
                    self.tempo_na_transicao = 0

            elif self.etapa_alvo < self.etapa_atual:
                self.tempo_na_transicao -= self.segundos_por_passo
                self.potencia -= 10.4167 * self.segundos_por_passo
                self.dict[f"UG{self.id}"]["potencia"] = self.potencia

                if self.tempo_na_transicao <= -TEMPO_TRANS_US_UPS and self.potencia <= 0:
                    self.potencia = 0
                    self.dict[f"UG{self.id}"]["etapa_atual"] = self.etapa_atual = ETAPA_UPS
                    self.dict[f"UG{self.id}"]["etapa_aux"] = UG_PARANDO
                    self.tempo_na_transicao = 0


    def atualizar_modbus(self) -> "None":

        self.sim_db.set_words(REG[f"UG{self.id}_Potencia"], [round(self.potencia)])
        self.sim_db.set_words(REG[f"UG{self.id}_HorimetroHora"], [np.floor(self.horimetro_hora)])
        self.sim_db.set_words(REG[f"UG{self.id}_HorimetroMin"], [round((self.horimetro_hora - np.floor(self.horimetro_hora)) * 60, 0)])

        self.sim_db.set_words(REG[f"UG{self.id}_EtapaAtual"], [int(self.dict[f"UG{self.id}"]["etapa_aux"])])

        self.sim_db.set_words(REG[f"UG{self.id}_Temperatura_01"], [round(self.dict[f"UG{self.id}"]["tmp_fase_r"])])
        self.sim_db.set_words(REG[f"UG{self.id}_Temperatura_02"], [round(self.dict[f"UG{self.id}"]["tmp_fase_s"])])
        self.sim_db.set_words(REG[f"UG{self.id}_Temperatura_03"], [round(self.dict[f"UG{self.id}"]["tmp_fase_t"])])
        self.sim_db.set_words(REG[f"UG{self.id}_Temperatura_04"], [round(self.dict[f"UG{self.id}"]["tmp_nucleo_estator"])])
        self.sim_db.set_words(REG[f"UG{self.id}_Temperatura_05"], [round(self.dict[f"UG{self.id}"]["tmp_mancal_radial_dia_1"])])
        self.sim_db.set_words(REG[f"UG{self.id}_Temperatura_06"], [round(self.dict[f"UG{self.id}"]["tmp_mancal_radial_tra_1"])])
        self.sim_db.set_words(REG[f"UG{self.id}_Temperatura_07"], [round(self.dict[f"UG{self.id}"]["tmp_mancal_radial_dia_2"])])
        self.sim_db.set_words(REG[f"UG{self.id}_Temperatura_08"], [round(self.dict[f"UG{self.id}"]["tmp_mancal_radial_tra_2"])])
        self.sim_db.set_words(REG[f"UG{self.id}_Temperatura_09"], [round(self.dict[f"UG{self.id}"]["tmp_mancal_guia_radial"])])
        self.sim_db.set_words(REG[f"UG{self.id}_Temperatura_10"], [round(self.dict[f"UG{self.id}"]["tmp_saida_ar"])])
        self.sim_db.set_words(REG[f"UG{self.id}_Temperatura_11"], [round(self.dict[f"UG{self.id}"]["tmp_mancal_guia_escora"])])
        self.sim_db.set_words(REG[f"UG{self.id}_Temperatura_12"], [round(self.dict[f"UG{self.id}"]["tmp_mancal_guia_contra_escora"])])
        self.sim_db.set_words(REG[f"UG{self.id}_Pressao_CX_Espiral"], [round(10 * self.dict[f"UG{self.id}"]["pressao_cx_espiral"])])