from asyncio.log import logger
import logging
import numpy as np
import threading
from datetime import datetime
from sys import stdout
from time import sleep

from pyModbusTCP.server import ModbusServer, DataBank
from dj52L import Dj52L
from ug import Ug
import mapa_modbus

REG = mapa_modbus.REG

lock = threading.Lock()


class Planta:

    def __init__(self, shared_dict):
        # Set-up logging
        rootLogger = logging.getLogger()
        if rootLogger.hasHandlers():
            rootLogger.handlers.clear()
        rootLogger.setLevel(logging.NOTSET)
        self.logger = logging.getLogger(__name__)

        if self.logger.hasHandlers():
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

        # Declaração de variáveis padrão da usina
        self.USINA_NV_VERTEDOURO = 462.37
        self.USINA_VAZAO_SANITARIA_COTA = 461.37
        self.USINA_NV_MINIMO_OPERACAO = 461.37
        self.USINA_TENSAO_MINIMA = 23100 * 0.95
        self.USINA_TENSAO_MAXIMA = 23100 * 1.05
        self.aux=0
        self.aux1=0
        self.aux2=0
        self.aux3=0
        self.aux4=0
        self.shared_dict = shared_dict
        self.escala_ruido = 0.1
        self.speed = 50
        self.passo_simulacao = 0.001
        self.segundos_por_passo = self.passo_simulacao * self.speed

        ug1 = Ug(1, self)
        ug2 = Ug(2, self)
        self.ugs = [ug1, ug2]

        self.dj52L = Dj52L(self)

        self.cust_data_bank = DataBank()
        self.server = ModbusServer(host="10.101.2.215", port=5003, no_block=True)
        self.server.start()
        for R in REG:
            self.cust_data_bank.set_words(int(REG[R]), [0])

    def run(self):
        # INICIO DECLARAÇÃO shared_dict
        self.shared_dict["nv_montante"] = 461.9
        self.shared_dict["potencia_kw_se"] = 0
        self.shared_dict["q_alfuente"] = 0
        self.shared_dict["q_liquida"] = 0
        self.shared_dict["q_sanitaria"] = 0
        self.shared_dict["q_vertimento"] = 0
        self.shared_dict["stop_gui"] = False
        self.shared_dict["stop_sim"] = False
        self.shared_dict["tempo_simul"] = 0
        self.shared_dict["tensao_na_linha"] = 23100
        self.shared_dict["potencia_kw_mp"] = 0
        self.shared_dict["potencia_kw_mr"] = 0
        self.shared_dict["nv_jusante_grade"] = 0
        self.shared_dict["trip_condic_usina"] = False
        self.shared_dict["trip_condic_ug1"] = False
        self.shared_dict["trip_condic_ug2"] = False
        self.shared_dict["reset_geral_condic"] = False

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

                # Lê do self.cust_data_bank
                if (self.cust_data_bank.get_words(REG["REG_USINA_Disj52LFechar"])[0] == 1):
                    self.cust_data_bank.set_words(REG["REG_USINA_Disj52LFechar"], [0])
                    logger.info("Comando modbus recebido: REG_USINA_Disj52LFechar ")
                    self.dj52L.fechar()

                if (self.cust_data_bank.get_words(REG["REG_USINA_EmergenciaDesligar"])[0] == 1):
                    self.cust_data_bank.set_words(REG["REG_USINA_EmergenciaDesligar"], [0])
                    logger.info("Comando modbus recebido: REG_USINA_EmergenciaDesligar ")
                    pass

                if (self.cust_data_bank.get_words(REG["REG_USINA_EmergenciaLigar"])[0] == 1):
                    self.cust_data_bank.set_words(REG["REG_USINA_EmergenciaLigar"], [0])
                    logger.info("Comando modbus recebido: REG_USINA_EmergenciaLigar ")
                    for ug in self.ugs:
                        ug.tripar(1, "REG_USINA_EmergenciaLigar via modbus")
                    self.dj52L.tripar("REG_USINA_EmergenciaLigar via modbus")
                    
                if (self.cust_data_bank.get_words(REG["REG_USINA_ResetAlarmes"])[0]== 1):
                    self.cust_data_bank.set_words(REG["REG_USINA_ResetAlarmes"], [0])
                    self.cust_data_bank.set_words(REG["REG_USINA_ReconheceAlarmes"], [0])
                    logger.info("Comando modbus recebido: REG_USINA_ReconheceAlarmes ")
                    logger.info("Comando modbus recebido: REG_USINA_ResetAlarmes ")
                    for ug in self.ugs:
                        ug.reconhece_reset_ug()
                    self.dj52L.reconhece_reset_dj52L()

                if self.shared_dict["trip_condic_usina"]==True and self.aux==0:
                    self.aux = 1
                    self.cust_data_bank.set_words(REG["REG_USINA_AUX_CondicionadoresE"], [int(1)])
                    self.cust_data_bank.set_words(REG["REG_USINA_AUX_Condicionadores1"], [int(1)])
                
                elif self.shared_dict["trip_condic_usina"]==False and self.aux==1:
                    self.aux = 0
                    self.cust_data_bank.set_words(REG["REG_USINA_AUX_CondicionadoresE"], [0])
                    self.cust_data_bank.set_words(REG["REG_USINA_AUX_Condicionadores1"], [0])
                    self.dj52L.reconhece_reset_dj52L()

                if self.shared_dict["trip_condic_ug1"]==True and self.aux1==0:
                    self.aux1 = 1
                    self.cust_data_bank.set_words(REG["REG_UG1_AUX_Condicionadores"], [int(1)])
                    self.cust_data_bank.set_words(REG["REG_UG1_Emergencia_Condicionadores1"], [int(1)])
                
                elif self.shared_dict["trip_condic_ug1"]==False and self.aux1==1:
                    self.aux1 = 0
                    self.cust_data_bank.set_words(REG["REG_UG1_AUX_Condicionadores"], [int(0)])
                    self.cust_data_bank.set_words(REG["REG_UG1_Emergencia_Condicionadores1"], [int(0)])

                if self.shared_dict["trip_condic_ug2"]==True and self.aux2==0:
                    self.aux2 = 1
                    self.cust_data_bank.set_words(REG["REG_UG2_AUX_Condicionadores"], [int(1)])
                    self.cust_data_bank.set_words(REG["REG_UG2_Emergencia_Condicionadores2"], [int(1)])
                    
                elif self.shared_dict["trip_condic_ug2"]==False and self.aux2==1:
                    self.aux2 = 0
                    self.cust_data_bank.set_words(REG["REG_UG2_AUX_Condicionadores"], [int(0)])
                    self.cust_data_bank.set_words(REG["REG_UG2_Emergencia_Condicionadores2"], [int(0)])

                if self.shared_dict["reset_geral_condic"]==True:
                    self.cust_data_bank.set_words(REG["REG_USINA_AUX_CondicionadoresE"], [int(0)])
                    self.cust_data_bank.set_words(REG["REG_USINA_AUX_Condicionadores1"], [int(0)])
                    self.cust_data_bank.set_words(REG["REG_UG1_AUX_Condicionadores"], [int(0)])
                    self.cust_data_bank.set_words(REG["REG_UG1_Emergencia_Condicionadores1"], [int(0)])
                    self.cust_data_bank.set_words(REG["REG_UG2_AUX_Condicionadores"], [int(0)])
                    self.cust_data_bank.set_words(REG["REG_UG2_Emergencia_Condicionadores2"], [int(0)])

                if self.cust_data_bank.get_words(REG["REG_USINA_AUX_CondicionadoresE"])[0] == 1 and self.aux4==0:
                    self.aux4 = 1
                elif self.cust_data_bank.get_words(REG["REG_USINA_AUX_CondicionadoresE"])[0] == 0 and self.aux4==1:
                    self.aux4 = 0
                    self.cust_data_bank.set_words(REG["REG_USINA_AUX_CondicionadoresE"], [0])
                    self.cust_data_bank.set_words(REG["REG_USINA_AUX_Condicionadores1"], [0])
                    self.shared_dict["trip_condic_usina"]=False
                    self.dj52L.reconhece_reset_dj52L()

                for ug in self.ugs:
                    self.shared_dict["setpoint_kw_ug{}".format(ug.id)] = self.cust_data_bank.get_words(REG["REG_UG{}_CtrlPotencia_Alvo".format(ug.id)])[0]
                    if self.shared_dict["debug_setpoint_kw_ug{}".format(ug.id)] >= 0:
                        self.shared_dict["setpoint_kw_ug{}".format(ug.id)] = self.shared_dict["debug_setpoint_kw_ug{}".format(ug.id)]
                        self.cust_data_bank.set_words(REG["REG_UG{}_CtrlPotencia_Alvo".format(ug.id)],[self.shared_dict["setpoint_kw_ug{}".format(ug.id)]],)
                        self.shared_dict["debug_setpoint_kw_ug{}".format(ug.id)] = -1

                    if (self.cust_data_bank.get_words(REG["REG_UG{}_Operacao_EmergenciaDesligar".format(ug.id)])[0]== 1):
                        self.cust_data_bank.set_words(REG["REG_UG{}_Operacao_EmergenciaDesligar".format(ug.id)],[0],)
                        self.cust_data_bank.set_words(REG["REG_UG{}_Operacao_EmergenciaLigar".format(ug.id)], [0])
                        ug.reconhece_reset_ug()

                    if (self.cust_data_bank.get_words(REG["REG_UG{}_Operacao_EmergenciaLigar".format(ug.id)])[0]== 1):
                        self.cust_data_bank.set_words(REG["REG_UG{}_Operacao_EmergenciaDesligar".format(ug.id)], [0],)
                        self.cust_data_bank.set_words(REG["REG_UG{}_Operacao_EmergenciaLigar".format(ug.id)], [0])
                        ug.tripar(1, "Operacao_EmergenciaLigar via modbus")

                    if (self.cust_data_bank.get_words(REG["REG_UG{}_Operacao_ResetAlarmes".format(ug.id)])[0]== 1):
                        self.cust_data_bank.set_words(REG["REG_UG{}_Operacao_ReconheceAlarmes".format(ug.id)],[0],)
                        self.cust_data_bank.set_words(REG["REG_UG{}_Operacao_ResetAlarmes".format(ug.id)],[0],)
                        ug.reconhece_reset_ug()


                    if (self.cust_data_bank.get_words(REG["REG_UG{}_Operacao_UP".format(ug.id)])[0] == 1):
                        self.cust_data_bank.set_words(REG["REG_UG{}_Operacao_UP".format(ug.id)], [0])
                        ug.parar()
                        pass

                    if (self.cust_data_bank.get_words(REG["REG_UG{}_Operacao_US".format(ug.id)])[0] == 1):
                        self.cust_data_bank.set_words(REG["REG_UG{}_Operacao_US".format(ug.id)], [0])
                        ug.partir()
                        pass

                # dj52L
                self.dj52L.passo()

                # UGS
                for ug in self.ugs:
                    ug.passo()

                # SE
                self.shared_dict["potencia_kw_se"] = sum([ug.potencia for ug in self.ugs]) * 0.995 + np.random.normal(0, 0.001 * self.escala_ruido)

                # MEDIDORES
                self.shared_dict["potencia_kw_mp"] = (np.random.normal(self.shared_dict["potencia_kw_se"] * 0.98,10 * self.escala_ruido,)- 20)
                self.shared_dict["potencia_kw_mr"] = (np.random.normal(self.shared_dict["potencia_kw_se"] * 0.98,10 * self.escala_ruido,)- 20)

                # RESERVATORIO
                self.shared_dict["q_liquida"] = 0
                self.shared_dict["q_liquida"] += self.shared_dict["q_alfuente"]
                self.shared_dict["q_liquida"] -= self.shared_dict["q_sanitaria"]
                self.shared_dict["q_sanitaria"] = self.q_sanitaria(self.shared_dict["nv_montante"])
                self.shared_dict["q_vertimento"] = 0
                for ug in self.ugs:
                    self.shared_dict["q_liquida"] -= self.shared_dict["q_ug{}".format(ug.id)]

                self.shared_dict["nv_montante"] = self.volume_para_nv_montate(volume + self.shared_dict["q_liquida"] * self.segundos_por_passo)
                self.shared_dict["nv_jusante_grade"] = self.shared_dict["nv_montante"] - max(0, np.random.normal(0.1, 0.1 * self.escala_ruido))

                if self.shared_dict["nv_montante"] >= self.USINA_NV_VERTEDOURO:
                    self.shared_dict["q_vertimento"] = self.shared_dict["q_liquida"]
                    self.shared_dict["q_liquida"] = 0
                    self.shared_dict["nv_montante"] = (
                        0.0000021411 * self.shared_dict["q_vertimento"] ** 3
                        - 0.00025189 * self.shared_dict["q_vertimento"] ** 2
                        + 0.014859 * self.shared_dict["q_vertimento"]
                        + 462.37
                    )

                volume += self.shared_dict["q_liquida"] * self.segundos_por_passo

                # Escreve no self.cust_data_bank
                for ug in self.ugs:
                    self.cust_data_bank.set_words(REG["REG_UG{}_Alarme01".format(ug.id)], [int(ug.flags)])

                    self.cust_data_bank.set_words(REG["REG_UG{}_Gerador_PotenciaAtivaMedia".format(ug.id)],[round(ug.potencia)],)
                    self.cust_data_bank.set_words(REG["REG_UG{}_HorimetroEletrico_Hora".format(ug.id)],[np.floor(ug.horimetro_hora)],)
                    self.cust_data_bank.set_words(REG["REG_UG{}_HorimetroEletrico_Frac".format(ug.id)],[round((ug.horimetro_hora - np.floor(ug.horimetro_hora)) * 60, 0)],)
                    
                    if ug.etapa_alvo == ug.etapa_atual:
                        self.cust_data_bank.set_words(REG["REG_UG{}_Operacao_EtapaAlvo".format(ug.id)],[int(ug.etapa_alvo)],)
                    else:
                        self.cust_data_bank.set_words(REG["REG_UG{}_Operacao_EtapaAlvo".format(ug.id)],[0b11111111],)

                    self.cust_data_bank.set_words(REG["REG_UG{}_Etapa_AUX".format(ug.id)], [int(self.shared_dict["etapa_aux_ug{}".format(ug.id)])])
                    self.cust_data_bank.set_words(REG["REG_UG{}_Operacao_EtapaAtual".format(ug.id)],[int(ug.etapa_atual)],)
                    
                    self.cust_data_bank.set_words(REG["REG_UG{}_Pressao_Turbina".format(ug.id)],[round(10 * self.shared_dict["pressao_turbina_ug{}".format(ug.id)])],)
                    self.cust_data_bank.set_words(REG["REG_UG{}_Temperatura_01".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_fase_r".format(ug.id)])],)
                    self.cust_data_bank.set_words(REG["REG_UG{}_Temperatura_02".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_fase_s".format(ug.id)])],)
                    self.cust_data_bank.set_words(REG["REG_UG{}_Temperatura_03".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_fase_t".format(ug.id)])],)
                    self.cust_data_bank.set_words(REG["REG_UG{}_Temperatura_04".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_nucleo_gerador_1".format(ug.id)])],)
                    self.cust_data_bank.set_words(REG["REG_UG{}_Temperatura_05".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_mancal_guia".format(ug.id)])],)
                    self.cust_data_bank.set_words(REG["REG_UG{}_Temperatura_06".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_mancal_guia_interno_1".format(ug.id)])],)
                    self.cust_data_bank.set_words(REG["REG_UG{}_Temperatura_07".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_mancal_guia_interno_2".format(ug.id)])],)
                    self.cust_data_bank.set_words(REG["REG_UG{}_Temperatura_08".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_patins_mancal_comb_1".format(ug.id)])],)
                    self.cust_data_bank.set_words(REG["REG_UG{}_Temperatura_09".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_patins_mancal_comb_2".format(ug.id)])],)
                    self.cust_data_bank.set_words(REG["REG_UG{}_Temperatura_10".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_mancal_casq_comb".format(ug.id)])],)
                    self.cust_data_bank.set_words(REG["REG_UG{}_Temperatura_11".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_mancal_contra_esc_comb".format(ug.id)])],)
                    

                self.cust_data_bank.set_words(REG["REG_USINA_NivelBarragem"],[round((self.shared_dict["nv_montante"]) * 10000)],)
                self.cust_data_bank.set_words(REG["REG_USINA_NivelCanalAducao"],[round((self.shared_dict["nv_jusante_grade"]) * 10000)],)  # TODO ?
                self.cust_data_bank.set_words(REG["REG_USINA_Subestacao_PotenciaAtivaMedia"],[round(self.shared_dict["potencia_kw_se"])],)
                self.cust_data_bank.set_words(REG["REG_USINA_Subestacao_TensaoRS"],[round(self.shared_dict["tensao_na_linha"] / 1000)],)
                self.cust_data_bank.set_words(REG["REG_USINA_Subestacao_TensaoST"],[round(self.shared_dict["tensao_na_linha"] / 1000)],)
                self.cust_data_bank.set_words(REG["REG_USINA_Subestacao_TensaoTR"],[round(self.shared_dict["tensao_na_linha"] / 1000)],)
                self.cust_data_bank.set_words(REG["REG_USINA_potencia_kw_mp"],[round(max(0, self.shared_dict["potencia_kw_mp"]))],)
                self.cust_data_bank.set_words(REG["REG_USINA_potencia_kw_mr"],[round(max(0, self.shared_dict["potencia_kw_mr"]))],)

                # FIM COMPORTAMENTO USINA
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
        return min(max(461.37, 461.37 + volume / 190000), 462.37)

    def nv_montate_para_volume(self, nv_montante):
        return 190000 * (min(max(461.37, nv_montante), 462.37) - 461.37)

    def q_sanitaria(self, nv_montante):
        return 2.33
