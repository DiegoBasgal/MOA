from asyncio.log import logger
import logging
from tkinter import E
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

        self.USINA_NV_VERTEDOURO = 643.5
        self.USINA_VAZAO_SANITARIA_COTA = 641
        self.USINA_NV_MINIMO_OPERACAO = 642.95
        self.USINA_TENSAO_MINIMA = 31050
        self.USINA_TENSAO_MAXIMA = 36200
        
        self.shared_dict = shared_dict
        self.escala_ruido = 1
        self.speed = 60
        self.passo_simulacao = 0.001
        self.segundos_por_passo = self.passo_simulacao * self.speed
        
        ug1 = Ug(1, self)
        ug2 = Ug(2, self)
        self.ugs = [ug1, ug2]

        self.dj52L = Dj52L(self)

        server = ModbusServer(host='localhost', port=502, no_block=True)
        self.db = DataBank()
        server.start()

    def run(self):

        # INICIO DECLARAÇÃO shared_dict
        self.shared_dict["nv_montante"] = 643.25
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
                if self.db.get_holding_registers(REG["REG_USINA_Disj52LFechar"]) == [1]:
                    self.db.set_holding_registers(REG["REG_USINA_Disj52LFechar"], [int(0)])
                    logger.info("Comando modbus recebido: REG_USINA_Disj52LFechar ")
                    self.dj52L.fechar()
                
                if self.db.get_holding_registers(REG["REG_USINA_EmergenciaDesligar"]) == [1]:
                    self.db.set_holding_registers(REG["REG_USINA_EmergenciaDesligar"], [int(0)])
                    logger.info("Comando modbus recebido: REG_USINA_EmergenciaDesligar ")
                    pass
                
                if self.db.get_holding_registers(REG["REG_USINA_EmergenciaLigar"]) == [1]:
                    self.db.set_holding_registers(REG["REG_USINA_EmergenciaLigar"], [int(0)])
                    logger.info("Comando modbus recebido: REG_USINA_EmergenciaLigar ")
                    for ug in self.ugs:
                        ug.tripar(1, "REG_USINA_EmergenciaLigar via modbus")
                    self.dj52L.tripar("REG_USINA_EmergenciaLigar via modbus")
                
                if self.db.get_holding_registers(REG["REG_USINA_ReconheceAlarmes"]) == [1]:
                    self.db.set_holding_registers(REG["REG_USINA_ReconheceAlarmes"], [int(0)])
                    logger.info("Comando modbus recebido: REG_USINA_ReconheceAlarmes ")
                    pass
                
                if self.db.get_holding_registers(REG["REG_USINA_ResetAlarmes"]) == [1]:
                    self.db.set_holding_registers(REG["REG_USINA_ResetAlarmes"], [int(0)])
                    logger.info("Comando modbus recebido: REG_USINA_ResetAlarmes ")
                    for ug in self.ugs:
                        ug.reconhece_reset_ug()
                    self.dj52L.reconhece_reset_dj52L()
                
                for ug in self.ugs:
                    self.shared_dict["setpoint_kw_ug{}".format(ug.id)] = self.db.get_holding_registers(REG["REG_UG{}_CtrlPotencia_Alvo".format(ug.id)])
                    if self.shared_dict["debug_setpoint_kw_ug{}".format(ug.id)] >= 0:
                        self.shared_dict["setpoint_kw_ug{}".format(ug.id)] = self.shared_dict["debug_setpoint_kw_ug{}".format(ug.id)]
                        self.db.set_holding_registers(REG["REG_UG{}_CtrlPotencia_Alvo".format(ug.id)], [self.shared_dict["setpoint_kw_ug{}".format(ug.id)]])
                        self.shared_dict["debug_setpoint_kw_ug{}".format(ug.id)] = -1
                    
                    if self.db.get_holding_registers(REG["REG_UG{}_Operacao_EmergenciaDesligar".format(ug.id)]) == [1]:
                        self.db.set_holding_registers(REG["REG_UG{}_Operacao_EmergenciaDesligar".format(ug.id)], [int(0)])
                        self.db.set_holding_registers(REG["REG_UG{}_Operacao_EmergenciaLigar".format(ug.id)], [int(0)])
                        ug.reconhece_reset_ug()
                    
                    if self.db.get_holding_registers(REG["REG_UG{}_Operacao_EmergenciaLigar".format(ug.id)]) == [1]:
                        self.db.set_holding_registers(REG["REG_UG{}_Operacao_EmergenciaDesligar".format(ug.id)], [int(0)])
                        self.db.set_holding_registers(REG["REG_UG{}_Operacao_EmergenciaLigar".format(ug.id)], [int(0)])
                        ug.tripar(1, "Operacao_EmergenciaLigar via modbus")
                    
                    if self.db.get_holding_registers(REG["REG_UG{}_Operacao_PCH_CovoReconheceAlarmes".format(ug.id)]) == [1]:
                        self.db.set_holding_registers(REG["REG_UG{}_Operacao_PCH_CovoReconheceAlarmes".format(ug.id)], [int(0)])
                        pass
                    
                    if self.db.get_holding_registers(REG["REG_UG{}_Operacao_PCH_CovoResetAlarmes".format(ug.id)]) == [1]:
                        self.db.set_holding_registers(REG["REG_UG{}_Operacao_PCH_CovoResetAlarmes".format(ug.id)], [int(0)])
                        ug.reconhece_reset_ug()
                    
                    if self.db.get_holding_registers(REG["REG_UG{}_Operacao_UP".format(ug.id)]) == [1]:
                        self.db.set_holding_registers(REG["REG_UG{}_Operacao_UP".format(ug.id)], [int(0)])
                        ug.etapa_alvo = ug.ETAPA_UP
                        ug.shared_dict["etapa_alvo_ug{}".format(ug.id)] = ug.ETAPA_UP

                    if self.db.get_holding_registers(REG["REG_UG{}_Operacao_US".format(ug.id)]) == [1]:
                        self.db.set_holding_registers(REG["REG_UG{}_Operacao_US".format(ug.id)], [int(0)])
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

                self.shared_dict["nv_jusante"] = self.shared_dict["nv_montante"] - max(0, np.random.normal(1.0 , 0.5 * self.escala_ruido))
                
                if self.shared_dict["nv_montante"] >= self.USINA_NV_VERTEDOURO:
                    self.shared_dict["q_vertimento"] = self.shared_dict["q_liquida"]
                    self.shared_dict["q_liquida"] = 0
                    self.shared_dict["nv_montante"] = self.USINA_NV_VERTEDOURO + ((self.shared_dict["q_vertimento"] / ((1.66 + 0.0017336 * self.shared_dict["q_vertimento"]) * 110)) ** (2 / 3))
                
                volume += self.shared_dict["q_liquida"] * self.segundos_por_passo
                
                # Escreve no databank
                for ug in self.ugs:
                    self.db.set_holding_registers(REG["REG_UG{}_Alarme01".format(ug.id)], [int(ug.flags)])
                    self.db.set_holding_registers(REG["REG_UG{}_Gerador_PotenciaAtivaMedia".format(ug.id)], [int(ug.potencia)])
                    self.db.set_holding_registers(REG["REG_UG{}_HorimetroEletrico_Low".format(ug.id)], [int(ug.horimetro)])
                    
                    if ug.etapa_alvo  == ug.etapa_atual:
                        self.db.set_holding_registers(REG["REG_UG{}_Operacao_EtapaAlvo".format(ug.id)], [int(ug.etapa_alvo)])
                        
                    else:
                        self.db.set_holding_registers(REG["REG_UG{}_Operacao_EtapaAlvo".format(ug.id)], [0b11111111])    
                        self.db.set_holding_registers(REG["REG_UG{}_Operacao_EtapaAtual".format(ug.id)], [int(ug.etapa_atual)])
                        self.db.set_holding_registers(REG["REG_UG{}_Temperatura_01".format(ug.id)], [int(self.shared_dict["temperatura_ug{}_fase_r".format(ug.id)])])
                        self.db.set_holding_registers(REG["REG_UG{}_Temperatura_02".format(ug.id)], [int(self.shared_dict["temperatura_ug{}_fase_s".format(ug.id)])])
                        self.db.set_holding_registers(REG["REG_UG{}_Temperatura_03".format(ug.id)], [int(self.shared_dict["temperatura_ug{}_fase_t".format(ug.id)])])
                        self.db.set_holding_registers(REG["REG_UG{}_Temperatura_04".format(ug.id)], [int(self.shared_dict["temperatura_ug{}_escora_1".format(ug.id)])])
                        self.db.set_holding_registers(REG["REG_UG{}_Temperatura_05".format(ug.id)], [int(self.shared_dict["temperatura_ug{}_escora_2".format(ug.id)])])
                        self.db.set_holding_registers(REG["REG_UG{}_Temperatura_06".format(ug.id)], [int(self.shared_dict["temperatura_ug{}_la_casquilho".format(ug.id)])])
                        self.db.set_holding_registers(REG["REG_UG{}_Temperatura_07".format(ug.id)], [int(self.shared_dict["temperatura_ug{}_contra_escora_1".format(ug.id)])])
                        self.db.set_holding_registers(REG["REG_UG{}_Temperatura_08".format(ug.id)], [int(self.shared_dict["temperatura_ug{}_lna_casquilho".format(ug.id)])])
                        self.db.set_holding_registers(REG["REG_UG{}_Temperatura_09".format(ug.id)], [int(self.shared_dict["temperatura_ug{}_contra_escora_2".format(ug.id)])])
                

                #nv_mont = complex.real(self.shared_dict["nv_montante"]*100)

                self.db.set_holding_registers(REG["REG_USINA_NivelBarragem"], [int(self.shared_dict["nv_montante"]*100)])
                self.db.set_holding_registers(REG["REG_USINA_NivelCanalAducao"], [int(self.shared_dict["nv_jusante"]*100)]) # TODO ?
                self.db.set_holding_registers(REG["REG_USINA_Subestacao_PotenciaAtivaMedia"], [int(self.shared_dict["potencia_kw_se"])])
                self.db.set_holding_registers(REG["REG_USINA_Subestacao_TensaoRS"], [int(self.shared_dict["tensao_na_linha"]/10)])
                self.db.set_holding_registers(REG["REG_USINA_Subestacao_TensaoST"], [int(self.shared_dict["tensao_na_linha"]/10)])
                self.db.set_holding_registers(REG["REG_USINA_Subestacao_TensaoTR"], [int(self.shared_dict["tensao_na_linha"]/10)])
                
                aux = 0
                if self.shared_dict["dj52L_aberto"]:
                    aux += 2**0

                if self.shared_dict["dj52L_fechado"]:
                    aux += 2**1
                
                if self.shared_dict["dj52L_inconsistente"]: 
                    aux += 2**2
                
                if self.shared_dict["dj52L_trip"]: 
                    aux += 2**3

                #if Subestacao_Disj52LModoLocal: 
                #    aux += 2**4
                #if Subestacao_Disj52LModoRemoto: 
                #    aux += 2**5	
                if self.shared_dict["dj52L_mola_carregada"]: 
                    aux += 2**6
                
                #if Subestacao_Disj52LPressaoSF6Alarme:
                #    aux += 2**7
                if self.shared_dict["dj52L_falta_vcc"]:
                    aux += 2**8
                	
                if self.shared_dict["dj52L_condicao_de_fechamento"]:
                    aux += 2**9
                
                #if Subestacao_Disj52LAbriu:
                #    aux += 2**10
                #if Subestacao_Disj52LFechou:
                #    aux += 2**11
                if self.shared_dict["dj52L_falha_fechamento"]:
                    aux += 2**12
                
                #if Subestacao_Disj52LPressaoSF6Trip:
                #    aux += 2**13
                self.db.set_holding_registers(REG["REG_USINA_Subestacao_Disj52L"], [int(aux)])
                
                # FIM COMPORTAMENTO USINA
                lock.release()
                
                tempo_restante = self.passo_simulacao - \
                    (datetime.now()-t_inicio_passo).seconds
                
                if tempo_restante > 0:
                    sleep(tempo_restante)
                else:
                    self.logger.warning("A simulação está demorando mais do que o permitido.")
                

            except KeyboardInterrupt:
                self.shared_dict["stop_gui"] = True
                continue
                
    def volume_para_nv_montate(self, volume):
        return 1.224 * (10 ** -5) * volume + 640.85
        # return min(max(643.00, 643.00 + volume / 43 * (10 ** 3)), 643.00)


    def nv_montate_para_volume(self, nv_montante):
        return 81699.3 * (nv_montante - 640.85)

    def q_sanitaria(self, nv_montante):
        temp = (nv_montante - self.USINA_VAZAO_SANITARIA_COTA) if nv_montante > self.USINA_VAZAO_SANITARIA_COTA else 0
        return 0.07474 * ((19.62*temp)**(1/2))
