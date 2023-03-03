import logging
import threading
import numpy as np

from sys import stdout
from time import sleep
from datetime import datetime
from asyncio.log import logger
from pyModbusTCP.server import ModbusServer, DataBank

from REG import *
from DICT import *
from dj52L import *
from unidade_geracao import *

lock = threading.Lock()

class Planta:
    def __init__(self, shared_dict):
        rootLogger = logging.getLogger()
        if rootLogger.hasHandlers():
            rootLogger.handlers.clear()
        rootLogger.setLevel(logging.NOTSET)
        self.logger = logging.getLogger(__name__)

        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.setLevel(logging.NOTSET)
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-20.20s] [%(levelname)-5.5s] %(message)s")

        ch = logging.StreamHandler(stdout)
        ch.setFormatter(logFormatter)
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)

        fh = logging.FileHandler("simulacao.log")
        fh.setFormatter(logFormatter)
        fh.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)

        self.borda_db_condic = False
        self.borda_usn_condic = False
        self.borda_ug1_condic = False
        self.borda_ug2_condic = False
        self.shared_dict = shared_dict
        self.escala_ruido = 0.1
        self.speed = 50
        self.passo_simulacao = 0.001
        self.segundos_por_passo = self.passo_simulacao * self.speed

        ug1 = Ug(1, self)
        ug2 = Ug(2, self)
        self.ugs = [ug1, ug2]

        self.dj52L = Dj52L(self)

        self.server = ModbusServer(host="10.101.2.215", port=5003, no_block=True)
        self.server.start()
        for R in REG:
            DataBank.set_words(int(REG[R]), [0])

    def run(self):
        self.shared_dict["nv_montante"] = 821
        self.shared_dict["potencia_kw_se"] = 0
        self.shared_dict["q_alfuente"] = 0
        self.shared_dict["q_liquida"] = 0
        self.shared_dict["q_sanitaria"] = 0
        self.shared_dict["q_vertimento"] = 0
        self.shared_dict["tempo_simul"] = 0
        self.shared_dict["tensao_na_linha"] = 34500
        self.shared_dict["potencia_kw_mp"] = 0
        self.shared_dict["potencia_kw_mr"] = 0
        self.shared_dict["nv_jusante_grade"] = 0
        self.shared_dict["stop_sim"] = False
        self.shared_dict["stop_gui"] = False
        self.shared_dict["trip_condic_ug1"] = False
        self.shared_dict["trip_condic_ug2"] = False
        self.shared_dict["trip_condic_usina"] = False
        self.shared_dict["reset_geral_condic"] = False

        volume = self.nv_montate_para_volume(self.shared_dict["nv_montante"])
        self.dj52L.abrir()

        # Loop principal
        while not self.shared_dict["stop_sim"]:
            self.shared_dict["stop_sim"] = self.shared_dict["stop_gui"]
            try:
                t_inicio_passo = datetime.now()
                lock.acquire()

                self.shared_dict["tempo_simul"] += self.segundos_por_passo

                if DataBank.get_words(REG["REG_USINA_Disj52LFechar"])[0] == 1:
                    DataBank.set_words(REG["REG_USINA_Disj52LFechar"], [0])
                    logger.info("Comando modbus recebido: REG_USINA_Disj52LFechar ")
                    self.dj52L.fechar()

                if DataBank.get_words(REG["REG_USINA_EmergenciaDesligar"])[0] == 1:
                    DataBank.set_words(REG["REG_USINA_EmergenciaDesligar"], [0])
                    logger.info("Comando modbus recebido: REG_USINA_EmergenciaDesligar ")
                    pass

                if DataBank.get_words(REG["REG_USINA_EmergenciaLigar"])[0] == 1:
                    DataBank.set_words(REG["REG_USINA_EmergenciaLigar"], [0])
                    logger.info("Comando modbus recebido: REG_USINA_EmergenciaLigar ")
                    for ug in self.ugs:
                        ug.tripar(1, "REG_USINA_EmergenciaLigar via modbus")
                    self.dj52L.tripar("REG_USINA_EmergenciaLigar via modbus")

                if DataBank.get_words(REG["REG_USINA_ResetAlarmes"])[0] == 1:
                    DataBank.set_words(REG["REG_USINA_ResetAlarmes"], [0])
                    DataBank.set_words(REG["REG_USINA_ReconheceAlarmes"], [0])
                    logger.info("Comando modbus recebido: REG_USINA_ReconheceAlarmes ")
                    logger.info("Comando modbus recebido: REG_USINA_ResetAlarmes ")
                    for ug in self.ugs:
                        ug.reconhece_reset_ug()
                    self.dj52L.reconhece_reset_dj52L()

                if self.shared_dict["trip_condic_usina"] and not self.borda_usn_condic:
                    self.borda_usn_condic = True
                    DataBank.set_words(REG["REG_USINA_AUX_CondicionadoresE"], [1])
                    DataBank.set_words(REG["REG_USINA_AUX_Condicionadores1"], [1])
                
                elif not self.shared_dict["trip_condic_usina"] and self.borda_usn_condic:
                    self.borda_usn_condic = False
                    DataBank.set_words(REG["REG_USINA_AUX_CondicionadoresE"], [0])
                    DataBank.set_words(REG["REG_USINA_AUX_Condicionadores1"], [0])
                    self.dj52L.reconhece_reset_dj52L()

                if self.shared_dict["trip_condic_ug1"] and not self.borda_ug1_condic:
                    self.borda_ug1_condic = True
                    DataBank.set_words(REG["REG_UG1_AUX_Condicionadores"], [1])
                    DataBank.set_words(REG["REG_UG1_Emergencia_Condicionadores1"], [1])
                
                elif not self.shared_dict["trip_condic_ug1"] and self.borda_ug1_condic:
                    self.borda_ug1_condic = False
                    DataBank.set_words(REG["REG_UG1_AUX_Condicionadores"], [0])
                    DataBank.set_words(REG["REG_UG1_Emergencia_Condicionadores1"], [0])

                if self.shared_dict["trip_condic_ug2"] and not self.borda_ug2_condic:
                    self.borda_ug2_condic = True
                    DataBank.set_words(REG["REG_UG2_AUX_Condicionadores"], [1])
                    DataBank.set_words(REG["REG_UG2_Emergencia_Condicionadores2"], [1])
                    
                elif not self.shared_dict["trip_condic_ug2"] and self.borda_ug2_condic:
                    self.borda_ug2_condic = False
                    DataBank.set_words(REG["REG_UG2_AUX_Condicionadores"], [0])
                    DataBank.set_words(REG["REG_UG2_Emergencia_Condicionadores2"], [0])

                if self.shared_dict["reset_geral_condic"]:
                    DataBank.set_words(REG["REG_USINA_AUX_CondicionadoresE"], [0])
                    DataBank.set_words(REG["REG_USINA_AUX_Condicionadores1"], [0])
                    DataBank.set_words(REG["REG_UG1_AUX_Condicionadores"], [0])
                    DataBank.set_words(REG["REG_UG1_Emergencia_Condicionadores1"], [0])
                    DataBank.set_words(REG["REG_UG2_AUX_Condicionadores"], [0])
                    DataBank.set_words(REG["REG_UG2_Emergencia_Condicionadores2"], [0])

                if DataBank.get_words(REG["REG_USINA_AUX_CondicionadoresE"])[0] == 1 and not self.borda_db_condic:
                    self.borda_db_condic = True
                elif DataBank.get_words(REG["REG_USINA_AUX_CondicionadoresE"])[0] == 0 and self.borda_db_condic:
                    self.borda_db_condic = False
                    DataBank.set_words(REG["REG_USINA_AUX_CondicionadoresE"], [0])
                    DataBank.set_words(REG["REG_USINA_AUX_Condicionadores1"], [0])
                    self.shared_dict["trip_condic_usina"] = False
                    self.dj52L.reconhece_reset_dj52L()

                for ug in self.ugs:
                    self.shared_dict[f"setpoint_kw_ug{ug.id}"] = DataBank.get_words(REG[f"REG_UG{ug.id}_CtrlPotencia_Alvo"])[0]
                    if self.shared_dict[f"debug_setpoint_kw_ug{ug.id}"] >= 0:
                        self.shared_dict[f"setpoint_kw_ug{ug.id}"] = self.shared_dict[f"debug_setpoint_kw_ug{ug.id}"]
                        DataBank.set_words(REG[f"REG_UG{ug.id}_CtrlPotencia_Alvo"],[self.shared_dict[f"setpoint_kw_ug{ug.id}"]],)
                        self.shared_dict[f"debug_setpoint_kw_ug{ug.id}"] = -1

                    if DataBank.get_words(REG[f"REG_UG{ug.id}_Operacao_EmergenciaDesligar"])[0] == 1:
                        DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_EmergenciaDesligar"], [0])
                        DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_EmergenciaLigar"], [0])
                        ug.reconhece_reset_ug()

                    if DataBank.get_words(REG[f"REG_UG{ug.id}_Operacao_EmergenciaLigar"])[0] == 1:
                        DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_EmergenciaDesligar"], [0])
                        DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_EmergenciaLigar"], [0])
                        ug.tripar(1, "Operacao_EmergenciaLigar via modbus")

                    if DataBank.get_words(REG[f"REG_UG{ug.id}_Operacao_ResetAlarmes"])[0] == 1:
                        DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_ReconheceAlarmes"], [0])
                        DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_ResetAlarmes"], [0])
                        ug.reconhece_reset_ug()

                    if DataBank.get_words(REG[f"REG_UG{ug.id}_Operacao_UP"])[0] == 1:
                        DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_UP"], [0])
                        ug.parar()
                        pass

                    if DataBank.get_words(REG[f"REG_UG{ug.id}_Operacao_US"])[0] == 1:
                        DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_US"], [0])
                        ug.partir()
                        pass

                self.dj52L.passo()

                for ug in self.ugs:
                    ug.passo()

                self.shared_dict["potencia_kw_se"] = sum([ug.potencia for ug in self.ugs]) * 0.995 + np.random.normal(0, 0.001 * self.escala_ruido)

                self.shared_dict["potencia_kw_mp"] = (np.random.normal(self.shared_dict["potencia_kw_se"] * 0.98,10 * self.escala_ruido,) - 20)
                self.shared_dict["potencia_kw_mr"] = (np.random.normal(self.shared_dict["potencia_kw_se"] * 0.98,10 * self.escala_ruido,) - 20)

                self.shared_dict["q_liquida"] = 0
                self.shared_dict["q_liquida"] += self.shared_dict["q_alfuente"]
                self.shared_dict["q_liquida"] -= self.shared_dict["q_sanitaria"]
                self.shared_dict["q_sanitaria"] = self.q_sanitaria(self.shared_dict["nv_montante"])
                self.shared_dict["q_vertimento"] = 0

                for ug in self.ugs:
                    self.shared_dict["q_liquida"] -= self.shared_dict[f"q_ug{ug.id}"]

                self.shared_dict["nv_montante"] = self.volume_para_nv_montate(volume + self.shared_dict["q_liquida"] * self.segundos_por_passo)
                self.shared_dict["nv_jusante_grade"] = self.shared_dict["nv_montante"] - max(0, np.random.normal(0.1, 0.1 * self.escala_ruido))

                if self.shared_dict["nv_montante"] >= USINA_NV_VERTEDOURO:
                    self.shared_dict["q_vertimento"] = self.shared_dict["q_liquida"]
                    self.shared_dict["q_liquida"] = 0
                    self.shared_dict["nv_montante"] = (
                        0.000000027849 * self.shared_dict["q_vertimento"] ** 3
                        - 0.00002181 * self.shared_dict["q_vertimento"] ** 2
                        + 0.0080744 * self.shared_dict["q_vertimento"]
                        + 821
                    )

                volume += self.shared_dict["q_liquida"] * self.segundos_por_passo

                for ug in self.ugs:
                    DataBank.set_words(REG[f"REG_UG{ug.id}_Alarme01"], [int(ug.flags)])

                    DataBank.set_words(REG[f"REG_UG{ug.id}_Gerador_PotenciaAtivaMedia"],[round(ug.potencia)],)
                    DataBank.set_words(REG[f"REG_UG{ug.id}_HorimetroEletrico_Hora"],[np.floor(ug.horimetro_hora)],)
                    DataBank.set_words(REG[f"REG_UG{ug.id}_HorimetroEletrico_Frac"],[round((ug.horimetro_hora - np.floor(ug.horimetro_hora)) * 60, 0)],)

                    if ug.etapa_alvo == ug.etapa_atual:
                        DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_EtapaAlvo"],[int(ug.etapa_alvo)],)
                    else:
                        DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_EtapaAlvo"],[0b11111111],)

                    DataBank.set_words(REG[f"REG_UG{ug.id}_Etapa_AUX"], [int(self.shared_dict[f"etapa_aux_ug{ug.id}"])])
                    DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_EtapaAtual"],[int(ug.etapa_atual)],)
                    
                    DataBank.set_words(REG[f"REG_UG{ug.id}_Pressao_CX_Espiral"],[round(10 * self.shared_dict[f"pressao_caixa_espiral_ug{ug.id}"])],)
                    DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_01"],[round(self.shared_dict[f"temperatura_ug{ug.id}_fase_r"])],)
                    DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_02"],[round(self.shared_dict[f"temperatura_ug{ug.id}_fase_s"])],)
                    DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_03"],[round(self.shared_dict[f"temperatura_ug{ug.id}_fase_t"])],)
                    DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_04"],[round(self.shared_dict[f"temperatura_ug{ug.id}_nucleo_gerador_1"])],)
                    DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_05"],[round(self.shared_dict[f"temperatura_ug{ug.id}_nucleo_gerador_2"])],)
                    DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_06"],[round(self.shared_dict[f"temperatura_ug{ug.id}_nucleo_gerador_3"])],)
                    DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_07"],[round(self.shared_dict[f"temperatura_ug{ug.id}_mancal_casq_rad"])],)
                    DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_08"],[round(self.shared_dict[f"temperatura_ug{ug.id}_mancal_casq_comb"])],)
                    DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_09"],[round(self.shared_dict[f"temperatura_ug{ug.id}_mancal_escora_comb"])],)

                DataBank.set_words(REG["REG_USINA_NivelBarragem"],[round((self.shared_dict["nv_montante"]) * 10000)],)
                DataBank.set_words(REG["REG_USINA_NivelCanalAducao"],[round((self.shared_dict["nv_jusante_grade"]) * 10000)],)  # TODO ?
                DataBank.set_words(REG["REG_USINA_Subestacao_PotenciaAtivaMedia"],[round(self.shared_dict["potencia_kw_se"])],)
                DataBank.set_words(REG["REG_USINA_Subestacao_TensaoRS"],[round(self.shared_dict["tensao_na_linha"] / 1000)],)
                DataBank.set_words(REG["REG_USINA_Subestacao_TensaoST"],[round(self.shared_dict["tensao_na_linha"] / 1000)],)
                DataBank.set_words(REG["REG_USINA_Subestacao_TensaoTR"],[round(self.shared_dict["tensao_na_linha"] / 1000)],)
                DataBank.set_words(REG["REG_USINA_potencia_kw_mp"],[round(max(0, self.shared_dict["potencia_kw_mp"]))],)
                DataBank.set_words(REG["REG_USINA_potencia_kw_mr"],[round(max(0, self.shared_dict["potencia_kw_mr"]))],)

                lock.release()
                tempo_restante = (self.passo_simulacao - (datetime.now() - t_inicio_passo).seconds)
                if tempo_restante > 0:
                    sleep(tempo_restante)
                else:
                    self.logger.warning("A simulação está demorando mais do que o permitido.")

            except KeyboardInterrupt:
                self.shared_dict["stop_gui"] = True
                continue

    def volume_para_nv_montate(self, volume):
        return min(max(820.50, 820.50 + volume / 11301.84), 821)

    def nv_montate_para_volume(self, nv_montante):
        return 11301.84 * (min(max(820.50, nv_montante), 820.50) - 820.50)

    def q_sanitaria(self):
        return 0.22
