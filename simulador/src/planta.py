import pytz
import logging
import threading
import traceback
import numpy as np

from time import sleep
from datetime import datetime
from pyModbusTCP.server import ModbusServer, DataBank

from dicionarios.reg import *
from dicionarios.const import *
from unidade_geracao import Ug
from dj52L import Dj52L
from temporizador import Temporizador

lock = threading.Lock()
logger = logging.getLogger("__main__")

class Planta:
    def __init__(self, shared_dict, dj52L: Dj52L, ugs: "list[Ug]", time_handler: Temporizador) -> None:

        self.ugs = ugs
        self.dj52L = dj52L
        self.dict = shared_dict
        self.temporizador = time_handler

        self.escala_ruido = time_handler.escala_ruido
        self.passo_simulacao = time_handler.passo_simulacao
        self.segundos_por_passo = time_handler.segundos_por_passo

        self.borda_db_condic = False
        self.borda_usn_condic = False

        self.server = ModbusServer(host="10.101.2.215", port=5003, no_block=True).start()
        for R in REG: DataBank.set_words(int(REG[R]), [0])

    def get_time(self) -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def run(self):
        volume = self.nv_montate_para_volume(self.dict["USN"]["nv_montante"])
        self.dj52L.abrir()

        while not self.dict["GLB"]["stop_sim"]:
            self.dict["GLB"]["stop_sim"] = self.dict["GLB"]["stop_gui"]

            try:
                t_inicio = self.get_time()
                lock.acquire()

                self.dj52L.passo()
                self.leitura_modbus_usn()

                for ug in self.ugs:
                    self.leitura_modbus_ug(ug)
                    self.controle_setpoint(ug)
                    self.acionar_trips_ug(ug)
                    ug.passo()

                self.controle_potencia()
                self.controle_afluente()
                self.controle_nivel(volume)

                volume += self.dict["USN"]["q_liquida"] * self.segundos_por_passo

                self.escrita_data_bank()

                lock.release()
                t_restante = (self.passo_simulacao - (self.get_time() - t_inicio).seconds)
                if t_restante > 0:
                    sleep(t_restante)
                else:
                    logger.warning("A simulação está demorando mais do que o permitido.")

            except KeyboardInterrupt:
                self.dict["GLB"]["stop_gui"] = True
                continue

    def volume_para_nv_montate(self, volume) -> float:
        return min(max(820.50, 820.50 + volume / 11301.84), 821)

    def nv_montate_para_volume(self, nv_montante) -> float:
        return 11301.84 * (min(max(820.50, nv_montante), 820.50) - 820.50)

    def q_sanitaria(self, nv_montante) -> float:
        return 0.22

    def controle_potencia(self) -> None:
        self.dict["USN"]["potencia_kw_se"] = sum([ug.potencia for ug in self.ugs]) * 0.995 + np.random.normal(0, 0.001 * self.escala_ruido)
        self.dict["USN"]["potencia_kw_mp"] = (np.random.normal(self.dict["USN"]["potencia_kw_se"] * 0.98,10 * self.escala_ruido,) - 20)
        self.dict["USN"]["potencia_kw_mr"] = (np.random.normal(self.dict["USN"]["potencia_kw_se"] * 0.98,10 * self.escala_ruido,) - 20)
    
    def controle_setpoint(self, ug: Ug) -> None:
        if self.dict["UG"][f"debug_setpoint_kw_ug{ug.id}"] >= 0:
            self.dict["UG"][f"setpoint_kw_ug{ug.id}"] = self.dict["UG"][f"debug_setpoint_kw_ug{ug.id}"]
            DataBank.set_words(REG[f"REG_UG{ug.id}_CtrlPotencia_Alvo"], [self.dict["UG"][f"setpoint_kw_ug{ug.id}"]])
            self.dict["UG"][f"debug_setpoint_kw_ug{ug.id}"] = -1

    def controle_afluente(self) -> None:
        self.dict["USN"]["q_liquida"] = 0
        self.dict["USN"]["q_liquida"] += self.dict["USN"]["q_alfuente"]
        self.dict["USN"]["q_liquida"] -= self.dict["USN"]["q_sanitaria"]
        self.dict["USN"]["q_sanitaria"] = self.q_sanitaria(self.dict["USN"]["nv_montante"])
        self.dict["USN"]["q_vertimento"] = 0

        for ug in self.ugs:
            self.dict["USN"]["q_liquida"] -= self.dict["UG"][f"q_ug{ug.id}"]

    def controle_nivel(self, volume) -> None:
        self.dict["USN"]["nv_montante"] = self.volume_para_nv_montate(volume + self.dict["USN"]["q_liquida"] * self.segundos_por_passo)
        self.dict["USN"]["nv_jusante_grade"] = self.dict["USN"]["nv_montante"] - max(0, np.random.normal(0.1, 0.1 * self.escala_ruido))

        if self.dict["USN"]["nv_montante"] >= USINA_NV_VERTEDOURO:
            self.dict["USN"]["q_vertimento"] = self.dict["USN"]["q_liquida"]
            self.dict["USN"]["q_liquida"] = 0
            self.dict["USN"]["nv_montante"] = (
                0.000000027849 * self.dict["USN"]["q_vertimento"] ** 3
                - 0.00002181 * self.dict["USN"]["q_vertimento"] ** 2
                + 0.0080744 * self.dict["USN"]["q_vertimento"]
                + 821
            )

    def acionar_trips_usn(self) -> None:
        if self.dict["USN"]["trip_condic_usina"] and not self.borda_usn_condic:
            DataBank.set_words(REG["REG_USINA_Emergencia_Condicionadores"], [1])
            self.borda_usn_condic = True

        elif not self.dict["USN"]["trip_condic_usina"] and self.borda_usn_condic:
            DataBank.set_words(REG["REG_USINA_Emergencia_Condicionadores"], [0])
            self.borda_usn_condic = False
            self.dj52L.reconhece_reset()

        if self.dict["USN"]["reset_geral_condic"]:
            DataBank.set_words(REG["REG_USINA_Emergencia_Condicionadores"], [0])
            DataBank.set_words(REG["REG_UG1_Emergencia_Condicionadores"], [0])
            DataBank.set_words(REG["REG_UG2_Emergencia_Condicionadores"], [0])

    def acionar_trips_ug(self, ug: Ug) -> None:
        if self.dict["UG"][f"trip_condic_ug{ug.id}"] and not self.dict["BORDA"][f"ug{ug.id}_condic"]:
            DataBank.set_words(REG[f"REG_UG{ug.id}_Emergencia_Condicionadores"], [1])
            self.dict["BORDA"][f"ug{ug.id}_condic"] = True

        elif not self.dict["UG"][f"trip_condic_ug{ug.id}"] and self.dict["BORDA"][f"ug{ug.id}_condic"]:
            DataBank.set_words(REG[f"REG_UG{ug.id}_Emergencia_Condicionadores"], [0])
            self.dict["BORDA"][f"ug{ug.id}_condic"] = False

    def leitura_modbus_usn(self) -> None:
        if DataBank.get_words(REG["REG_USINA_Disj52LFechar"])[0] == 1:
            DataBank.set_words(REG["REG_USINA_Disj52LFechar"], [0])
            logger.info("[SIM] Comando modbus recebido: REG_USINA_Disj52LFechar")
            self.dj52L.fechar()

        if DataBank.get_words(REG["REG_USINA_EmergenciaDesligar"])[0] == 1:
            DataBank.set_words(REG["REG_USINA_EmergenciaDesligar"], [0])
            logger.info("[SIM] Comando modbus recebido: REG_USINA_EmergenciaDesligar")
            pass

        if DataBank.get_words(REG["REG_USINA_EmergenciaLigar"])[0] == 1:
            DataBank.set_words(REG["REG_USINA_EmergenciaLigar"], [0])
            logger.info("[SIM] Comando modbus recebido: REG_USINA_EmergenciaLigar")
            for ug in self.ugs:
                ug.tripar("REG_USINA_EmergenciaLigar via modbus")
            self.dj52L.tripar("REG_USINA_EmergenciaLigar via modbus")

        if DataBank.get_words(REG["REG_USINA_ResetAlarmes"])[0] == 1:
            DataBank.set_words(REG["REG_USINA_ResetAlarmes"], [0])
            DataBank.set_words(REG["REG_USINA_ReconheceAlarmes"], [0])
            logger.info("[SIM] Comando modbus recebido: REG_USINA_ReconheceAlarmes")
            logger.info("[SIM] Comando modbus recebido: REG_USINA_ResetAlarmes")
            for ug in self.ugs:
                ug.reconhece_reset()
            self.dj52L.reconhece_reset()

        if DataBank.get_words(REG["REG_USINA_Emergencia_Condicionadores"])[0] == 1 and not self.borda_db_condic:
            self.borda_db_condic = True
        elif DataBank.get_words(REG["REG_USINA_Emergencia_Condicionadores"])[0] == 0 and self.borda_db_condic:
            DataBank.set_words(REG["REG_USINA_Emergencia_Condicionadores"], [0])
            self.borda_db_condic = False
            self.dict["USN"]["trip_condic_usina"] = False
            self.dj52L.reconhece_reset()

    def leitura_modbus_ug(self, ug: Ug) -> None:
        self.dict["UG"][f"setpoint_kw_ug{ug.id}"] = DataBank.get_words(REG[f"REG_UG{ug.id}_CtrlPotencia_Alvo"])[0]

        if DataBank.get_words(REG[f"REG_UG{ug.id}_Operacao_EmergenciaDesligar"])[0] == 1:
            DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_EmergenciaDesligar"], [0])
            DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_EmergenciaLigar"], [0])
            ug.reconhece_reset()

        if DataBank.get_words(REG[f"REG_UG{ug.id}_Operacao_EmergenciaLigar"])[0] == 1:
            DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_EmergenciaDesligar"], [0])
            DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_EmergenciaLigar"], [0])
            ug.tripar("Operacao_EmergenciaLigar via modbus")

        if DataBank.get_words(REG[f"REG_UG{ug.id}_Operacao_ResetAlarmes"])[0] == 1:
            DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_ReconheceAlarmes"], [0])
            DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_ResetAlarmes"], [0])
            ug.reconhece_reset()

        if DataBank.get_words(REG[f"REG_UG{ug.id}_Operacao_UP"])[0] == 1:
            DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_UP"], [0])
            ug.parar()

        if DataBank.get_words(REG[f"REG_UG{ug.id}_Operacao_US"])[0] == 1:
            DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_US"], [0])
            ug.partir()

    def escrita_data_bank(self) -> None:
        try:
            for ug in self.ugs:

                if ug.etapa_alvo == ug.etapa_atual:
                    DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_EtapaAlvo"], [int(ug.etapa_alvo)],)
                else:
                    DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_EtapaAlvo"], [0b11111111],)

                DataBank.set_words(REG[f"REG_UG{ug.id}_Etapa_AUX"], [int(self.dict["UG"][f"etapa_aux_ug{ug.id}"])])
                DataBank.set_words(REG[f"REG_UG{ug.id}_Operacao_EtapaAtual"], [int(ug.etapa_atual)],)

                DataBank.set_words(REG[f"REG_UG{ug.id}_Gerador_PotenciaAtivaMedia"], [round(ug.potencia)],)
                DataBank.set_words(REG[f"REG_UG{ug.id}_HorimetroEletrico_Hora"], [np.floor(ug.horimetro_hora)],)
                DataBank.set_words(REG[f"REG_UG{ug.id}_HorimetroEletrico_Frac"], [round((ug.horimetro_hora - np.floor(ug.horimetro_hora)) * 60, 0)],)

                DataBank.set_words(REG[f"REG_UG{ug.id}_Pressao_CX_Espiral"], [round(10 * self.dict["UG"][f"pressao_caixa_espiral_ug{ug.id}"])],)
                DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_01"], [round(self.dict["UG"][f"temperatura_ug{ug.id}_fase_r"])],)
                DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_02"], [round(self.dict["UG"][f"temperatura_ug{ug.id}_fase_s"])],)
                DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_03"], [round(self.dict["UG"][f"temperatura_ug{ug.id}_fase_t"])],)
                DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_04"], [round(self.dict["UG"][f"temperatura_ug{ug.id}_nucleo_gerador_1"])],)
                DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_05"], [round(self.dict["UG"][f"temperatura_ug{ug.id}_nucleo_gerador_2"])],)
                DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_06"], [round(self.dict["UG"][f"temperatura_ug{ug.id}_nucleo_gerador_3"])],)
                DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_07"], [round(self.dict["UG"][f"temperatura_ug{ug.id}_mancal_casq_rad"])],)
                DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_08"], [round(self.dict["UG"][f"temperatura_ug{ug.id}_mancal_casq_comb"])],)
                DataBank.set_words(REG[f"REG_UG{ug.id}_Temperatura_09"], [round(self.dict["UG"][f"temperatura_ug{ug.id}_mancal_escora_comb"])],)

            DataBank.set_words(REG["REG_USINA_NivelBarragem"], [round((self.dict["USN"]["nv_montante"]) * 10000)])
            DataBank.set_words(REG["REG_USINA_NivelCanalAducao"], [round((self.dict["USN"]["nv_jusante_grade"]) * 10000)])  # TODO ?
            DataBank.set_words(REG["REG_USINA_Subestacao_PotenciaAtivaMedia"], [round(self.dict["USN"]["potencia_kw_se"])])
            DataBank.set_words(REG["REG_USINA_Subestacao_TensaoRS"], [round(self.dict["USN"]["tensao_na_linha"] / 1000)])
            DataBank.set_words(REG["REG_USINA_Subestacao_TensaoST"], [round(self.dict["USN"]["tensao_na_linha"] / 1000)])
            DataBank.set_words(REG["REG_USINA_Subestacao_TensaoTR"], [round(self.dict["USN"]["tensao_na_linha"] / 1000)])
            DataBank.set_words(REG["REG_USINA_potencia_kw_mp"], [round(max(0, self.dict["USN"]["potencia_kw_mp"]))])
            DataBank.set_words(REG["REG_USINA_potencia_kw_mr"], [round(max(0, self.dict["USN"]["potencia_kw_mr"]))])

        except Exception as e:
            logger.exception(f"[SIM] Houve um erro ao escrever os valores no DataBank interno. Exception: \"{repr(e)}\"")
            logger.exception(f"[SIM] Traceback: {traceback.format_exc()}")
