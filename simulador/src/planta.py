from asyncio.log import logger
import logging
import numpy as np
import threading
from datetime import datetime
from sys import stdout
from time import sleep

from pyModbusTCP.server import DataBank, ModbusServer
from dj52L import Dj52L
from ug import Ug
import mapa_modbus 

REG = mapa_modbus.REG

lock = threading.Lock()

class Planta:

    def __init__(self, shared_dict):

        # Set-up logging
        rootLogger = logging.getLogger()
        if (rootLogger.hasHandlers()):
            rootLogger.handlers.clear()
        rootLogger.setLevel(logging.NOTSET)
        self.logger = logging.getLogger(__name__)

        if (self.logger.hasHandlers()):
            self.logger.handlers.clear()
        self.logger.setLevel(logging.NOTSET)
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-20.20s] [%(levelname)-5.5s] %(message)s")

        ch = logging.StreamHandler(stdout)  # log para sdtout
        ch.setFormatter(logFormatter)
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)

        fh = logging.FileHandler("simulacao.log")  # log para arquivo
        fh.setFormatter(logFormatter)
        fh.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)
        # Fim Set-up logging

        self.USINA_NV_VERTEDOURO = 821
        self.USINA_VAZAO_SANITARIA_COTA = 820.39
        self.USINA_NV_MINIMO_OPERACAO = 819
        self.USINA_TENSAO_MINIMA = 31050
        self.USINA_TENSAO_MAXIMA = 36200
        
        self.shared_dict = shared_dict
        self.escala_ruido = 0.1
        self.speed = 30
        self.passo_simulacao = 0.001
        self.segundos_por_passo = self.passo_simulacao * self.speed
        
        ug1 = Ug(1, self)
        ug2 = Ug(2, self)
        self.ugs = [ug1, ug2]

        self.dj52L = Dj52L(self)

        server = ModbusServer(host='0.0.0.0', port=5002, no_block=True)
        DataBank
        server.start()

    def run(self):

        # INICIO DECLARAÇÃO shared_dict
        self.shared_dict["nv_montante"] = 820.90
        self.shared_dict["potencia_kw_se"] = 0
        self.shared_dict["q_alfuente"] = 0
        self.shared_dict["q_liquida"] = 0
        self.shared_dict["q_sanitaria"] = 0
        self.shared_dict["q_vertimento"] = 0
        self.shared_dict["stop_gui"] = False
        self.shared_dict["stop_sim"] = False
        self.shared_dict["tempo_simul"] = 0
        self.shared_dict["tensao_na_linha"] = 34500
        self.shared_dict["potencia_kw_mp"] = 0
        self.shared_dict["potencia_kw_mr"] = 0

        volume = self.nv_montate_para_volume(self.shared_dict["nv_montante"])
        self.dj52L.abrir()
        
        # Loop principal
        while not self.shared_dict["stop_sim"]:
            self.shared_dict["stop_sim"] = self.shared_dict["stop_gui"]
            try:
                t_inicio_passo = datetime.now()
                lock.acquire()

                # Acerto temportal
                self.shared_dict["tempo_simul"] += self.segundos_por_passo

                # Lê do databank
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

                if DataBank.get_words(REG["REG_USINA_ReconheceAlarmes"])[0] == 1:
                    DataBank.set_words(REG["REG_USINA_ReconheceAlarmes"], [0])
                    logger.info("Comando modbus recebido: REG_USINA_ReconheceAlarmes ")
                    pass

                if DataBank.get_words(REG["REG_USINA_ResetAlarmes"])[0] == 1:
                    DataBank.set_words(REG["REG_USINA_ResetAlarmes"], [0])
                    logger.info("Comando modbus recebido: REG_USINA_ResetAlarmes ")
                    for ug in self.ugs:
                        ug.reconhece_reset_ug()
                    self.dj52L.reconhece_reset_dj52L()

                for ug in self.ugs:
                    self.shared_dict["setpoint_kw_ug{}".format(ug.id)] = DataBank.get_words(REG["REG_UG{}_CtrlPotencia_Alvo".format(ug.id)])[0]
                    if self.shared_dict["debug_setpoint_kw_ug{}".format(ug.id)] >= 0:
                        self.shared_dict["setpoint_kw_ug{}".format(ug.id)] = self.shared_dict["debug_setpoint_kw_ug{}".format(ug.id)]
                        DataBank.set_words(REG["REG_UG{}_CtrlPotencia_Alvo".format(ug.id)], [self.shared_dict["setpoint_kw_ug{}".format(ug.id)]])
                        self.shared_dict["debug_setpoint_kw_ug{}".format(ug.id)] = -1

                    if DataBank.get_words(REG["REG_UG{}_Operacao_EmergenciaDesligar".format(ug.id)])[0] == 1:
                        DataBank.set_words(REG["REG_UG{}_Operacao_EmergenciaDesligar".format(ug.id)], [0])
                        DataBank.set_words(REG["REG_UG{}_Operacao_EmergenciaLigar".format(ug.id)], [0])
                        ug.reconhece_reset_ug()

                    if DataBank.get_words(REG["REG_UG{}_Operacao_EmergenciaLigar".format(ug.id)])[0] == 1:
                        DataBank.set_words(REG["REG_UG{}_Operacao_EmergenciaDesligar".format(ug.id)], [0])
                        DataBank.set_words(REG["REG_UG{}_Operacao_EmergenciaLigar".format(ug.id)], [0])
                        ug.tripar(1, "Operacao_EmergenciaLigar via modbus")
                    
                    if DataBank.get_words(REG["REG_UG{}_Operacao_PCH_CovoReconheceAlarmes".format(ug.id)])[0] == 1:
                        DataBank.set_words(REG["REG_UG{}_Operacao_PCH_CovoReconheceAlarmes".format(ug.id)], [0])
                        pass
                    
                    if DataBank.get_words(REG["REG_UG{}_Operacao_PCH_CovoResetAlarmes".format(ug.id)])[0] == 1:
                        DataBank.set_words(REG["REG_UG{}_Operacao_PCH_CovoResetAlarmes".format(ug.id)], [0])
                        ug.reconhece_reset_ug()
                    
                    if DataBank.get_words(REG["REG_UG{}_Operacao_UP".format(ug.id)])[0] == 1:
                        DataBank.set_words(REG["REG_UG{}_Operacao_UP".format(ug.id)], [0])
                        ug.etapa_alvo = ug.ETAPA_UP
                        ug.shared_dict["etapa_alvo_ug{}".format(ug.id)] = ug.ETAPA_UP
                    
                    if DataBank.get_words(REG["REG_UG{}_Operacao_US".format(ug.id)])[0] == 1:
                        DataBank.set_words(REG["REG_UG{}_Operacao_US".format(ug.id)], [0])
                        ug.etapa_alvo = ug.ETAPA_US
                        ug.shared_dict["etapa_alvo_ug{}".format(ug.id)] = ug.ETAPA_US

                # dj52L
                self.dj52L.passo()

                # UGS
                for ug in self.ugs:
                    ug.passo()

                # SE
                self.shared_dict["potencia_kw_se"] = sum([ug.potencia for ug in self.ugs]) * 0.995 + np.random.normal(0, 0.001 * self.escala_ruido)

                # MEDIDORES
                self.shared_dict["potencia_kw_mp"] = np.random.normal(self.shared_dict["potencia_kw_se"] * 0.98 , 10 * self.escala_ruido) - 20
                self.shared_dict["potencia_kw_mr"] = np.random.normal(self.shared_dict["potencia_kw_se"] * 0.98 , 10 * self.escala_ruido) - 20

                # RESERVATORIO
                self.shared_dict["q_liquida"] = 0
                self.shared_dict["q_liquida"] += self.shared_dict["q_alfuente"]
                self.shared_dict["q_liquida"] -= self.shared_dict["q_sanitaria"]
                self.shared_dict["q_sanitaria"] = self.q_sanitaria(self.shared_dict["nv_montante"])
                self.shared_dict["q_vertimento"] = 0
                for ug in self.ugs:
                    self.shared_dict["q_liquida"] -= self.shared_dict["q_ug{}".format(ug.id)]

                self.shared_dict["nv_montante"] = self.volume_para_nv_montate(volume + self.shared_dict["q_liquida"] * self.segundos_por_passo)
                self.shared_dict["nv_jusante"] =  self.shared_dict["nv_montante"] - max(0, np.random.normal(1.0 , 0.5 * self.escala_ruido))
                
                if self.shared_dict["nv_montante"] > self.USINA_NV_VERTEDOURO:
                    self.shared_dict["q_vertimento"] = self.shared_dict["q_liquida"]
                    self.shared_dict["q_liquida"] = 0
                    self.shared_dict["nv_montante"] = 0.000005 * self.shared_dict["q_vertimento"]**3 - 0.0005*self.shared_dict["q_vertimento"]**2 + 0.0204*self.shared_dict["q_vertimento"] + 821

                volume += self.shared_dict["q_liquida"] * self.segundos_por_passo

                # Escreve no databank
                for ug in self.ugs:
                    DataBank.set_words(REG["REG_UG{}_Alarme01".format(ug.id)], [int(ug.flags)])
                    DataBank.set_words(REG["REG_UG{}_Gerador_PotenciaAtivaMedia".format(ug.id)], [round(ug.potencia)])
                    DataBank.set_words(REG["REG_UG{}_HorimetroEletrico_Low".format(ug.id)], [round(ug.horimetro)])
                    if ug.etapa_alvo  == ug.etapa_atual:
                        DataBank.set_words(REG["REG_UG{}_Operacao_EtapaAlvo".format(ug.id)], [int(ug.etapa_alvo)])
                    else:
                        DataBank.set_words(REG["REG_UG{}_Operacao_EtapaAlvo".format(ug.id)], [0b11111111])    
                    DataBank.set_words(REG["REG_UG{}_Operacao_EtapaAtual".format(ug.id)], [int(ug.etapa_atual)])
                    DataBank.set_words(REG["REG_UG{}_Temperatura_01".format(ug.id)], [round(self.shared_dict["temperatura_ug{}_fase_r".format(ug.id)])])
                    DataBank.set_words(REG["REG_UG{}_Temperatura_02".format(ug.id)], [round(self.shared_dict["temperatura_ug{}_fase_s".format(ug.id)])])
                    DataBank.set_words(REG["REG_UG{}_Temperatura_03".format(ug.id)], [round(self.shared_dict["temperatura_ug{}_fase_t".format(ug.id)])])
                    DataBank.set_words(REG["REG_UG{}_Temperatura_04".format(ug.id)], [round(self.shared_dict["temperatura_ug{}_escora_1".format(ug.id)])])
                    DataBank.set_words(REG["REG_UG{}_Temperatura_05".format(ug.id)], [round(self.shared_dict["temperatura_ug{}_escora_2".format(ug.id)])])
                    DataBank.set_words(REG["REG_UG{}_Temperatura_06".format(ug.id)], [round(self.shared_dict["temperatura_ug{}_la_casquilho".format(ug.id)])])
                    DataBank.set_words(REG["REG_UG{}_Temperatura_07".format(ug.id)], [round(self.shared_dict["temperatura_ug{}_contra_escora_1".format(ug.id)])])
                    DataBank.set_words(REG["REG_UG{}_Temperatura_08".format(ug.id)], [round(self.shared_dict["temperatura_ug{}_lna_casquilho".format(ug.id)])])
                    DataBank.set_words(REG["REG_UG{}_Temperatura_09".format(ug.id)], [round(self.shared_dict["temperatura_ug{}_contra_escora_2".format(ug.id)])])

                DataBank.set_words(REG["REG_USINA_NivelBarragem"], [round((self.shared_dict["nv_montante"]-819)*100)])
                DataBank.set_words(REG["REG_USINA_NivelCanalAducao"], [round((self.shared_dict["nv_jusante"]-819)*100)]) # TODO ?
                DataBank.set_words(REG["REG_USINA_Subestacao_PotenciaAtivaMedia"], [round(self.shared_dict["potencia_kw_se"])])
                DataBank.set_words(REG["REG_USINA_Subestacao_TensaoRS"], [round(self.shared_dict["tensao_na_linha"]/10)])
                DataBank.set_words(REG["REG_USINA_Subestacao_TensaoST"], [round(self.shared_dict["tensao_na_linha"]/10)])
                DataBank.set_words(REG["REG_USINA_Subestacao_TensaoTR"], [round(self.shared_dict["tensao_na_linha"]/10)])

                # FIM COMPORTAMENTO USINA
                lock.release()
                tempo_restante = self.passo_simulacao - \
                    (datetime.now()-t_inicio_passo).seconds
                if tempo_restante > 0:
                    sleep(tempo_restante)
                else:
                    self.logger.warning(
                        "A simulação está demorando mais do que o permitido.")

            except KeyboardInterrupt:
                self.shared_dict["stop_gui"] = True
                continue

    def volume_para_nv_montate(self, volume):
        return 817.2487 + 0.002746156*volume - 0.0000008093185*volume**2 + 0.0000000001036295*volume**3

    def nv_montate_para_volume(self, nv_montante):
        return 201090380 - 491550*nv_montante + 300.39*nv_montante**2

    def q_sanitaria(self, nv_montante):
        temp = (nv_montante - self.USINA_VAZAO_SANITARIA_COTA) if nv_montante > self.USINA_VAZAO_SANITARIA_COTA else 0
        return 0.22
