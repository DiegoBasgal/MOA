import re
import logging
import threading
import numpy as np

import mapa_modbus

from sys import stdout
from time import sleep
from opcua import Server
from datetime import datetime
from asyncio.log import logger
from pyModbusTCP.server import ModbusServer, DataBank

from ug import Ug
from dj52L import Dj52L

REG_MB = mapa_modbus.REG_MB
REG_OPC = mapa_modbus.REG_OPC

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
        self.shared_dict = shared_dict

        self.USINA_NV_VERTEDOURO = 462.37
        self.USINA_NV_MINIMO_OPERACAO = 461.00
        self.USINA_VAZAO_SANITARIA_COTA = 461.37
        self.USINA_TENSAO_MINIMA = 23100 * 0.95
        self.USINA_TENSAO_MAXIMA = 23100 * 1.05

        self.speed = 50
        self.escala_ruido = 0.1
        self.passo_simulacao = 0.001
        self.segundos_por_passo = self.passo_simulacao * self.speed

        self.dj52L = Dj52L(self)

        self.ug1 = Ug(1, self)
        self.ug2 = Ug(2, self)
        self.ugs = [self.ug1, self.ug2]

        # Intância de servidores OPC e MB
        self.DB = DataBank()
        self.server_MB = ModbusServer(host="localhost", port=5003, no_block=True)

        self.server_OPC = Server()
        self.server_OPC.set_endpoint("opc.tcp://localhost:4840")
        self.server_OPC.register_namespace("Simulador XAV")

        # Adiciona os registradores do mapa aos servidores OPC e MB
        objects = self.server_OPC.get_objects_node()
        self.reg_ug1 = objects.add_object("ns=7;s=CLP_UG1", "Registradores UG1")
        self.reg_ug2 = objects.add_object("ns=7;s=CLP_UG2", "Registradores UG2")
        self.reg_tda = objects.add_object("ns=7;s=CLP_TDA", "Registradores TDA")
        self.reg_sa_se = objects.add_object("ns=7;s=CLP_SA", "Registradores SA/SE")

        for i in zip(REG_MB, REG_OPC):

            self.DB.set_words(int(REG_MB[i]), [0])

            if re.search("^REG_UG1", i):
                self.reg_ug1.add_variable("ns=7;s={}".format(i), "{}".format(re.sub("REG_UG1_", "", i)), REG_OPC[i])

            if re.search("^REG_UG2", i):
                self.reg_ug2.add_variable("ns=7;s={}".format(i), "{}".format(re.sub("REG_UG2_", "", i)), REG_OPC[i])
        
            if re.search("^REG_USINA", i):
                self.reg_usina.add_variable("ns=7;s={}".format(i), "{}".format(re.sub("REG_USINA_", "", i)), REG_OPC[i])
        
        # Incia os servidores
        self.server_MB.start()
        self.server_OPC.start()

    def run(self):
        # INICIO DECLARAÇÃO shared_dict
        self.shared_dict["q_liquida"] = 0
        self.shared_dict["q_alfuente"] = 0
        self.shared_dict["q_sanitaria"] = 0
        self.shared_dict["tempo_simul"] = 0
        self.shared_dict["q_vertimento"] = 0
        self.shared_dict["potencia_kw_se"] = 0
        self.shared_dict["potencia_kw_mp"] = 0
        self.shared_dict["potencia_kw_mr"] = 0
        self.shared_dict["nv_montante"] = 461.9
        self.shared_dict["nv_jusante_grade"] = 0
        self.shared_dict["tensao_na_linha"] = 23100

        self.shared_dict["stop_sim"] = False
        self.shared_dict["stop_gui"] = False
        self.shared_dict["trip_condic_usina"] = False
        self.shared_dict["reset_geral_condic"] = False

        for i in range(12):
            self.shared_dict["aux_borda{}".format(i)] = 0
        
        for ug in self.ugs:
            self.shared_dict["aux_comp_a_ug{}".format(ug.id)] = 0
            self.shared_dict["aux_comp_c_ug{}".format(ug.id)] = 0
            self.shared_dict["aux_comp_f_ug{}".format(ug.id)] = 0

            self.shared_dict["trip_condic_ug{}".format(ug.id)] = False 
            self.shared_dict["condicao_falha_cracking_ug{}".format(ug.id)] = False
            self.shared_dict["permissao_abrir_comporta_ug{}".format(ug.id)] = False

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

                # Leitura do dicionário compartilhado
                if self.shared_dict["trip_condic_usina"] == True and self.shared_dict["aux_borda{}".format(1)] == 0:
                    self.shared_dict["aux_borda{}".format(1)] = 1
                    self.escrita_OPC("ns=3;s=REG_USINA_Condicionadores", 1)

                elif self.shared_dict["trip_condic_usina"] == False and self.shared_dict["aux_borda{}".format(1)] == 1:
                    self.shared_dict["aux_borda{}".format(1)] = 0
                    self.escrita_OPC("ns=3;s=REG_USINA_Condicionadores", 0)
                    self.dj52L.reconhece_reset_dj52L()

                if self.shared_dict["reset_geral_condic"] == True:
                    self.escrita_OPC("ns=1;s=REG_UG1_Condicionadores", 0)
                    self.escrita_OPC("ns=2;s=REG_UG2_Condicionadores", 0)
                    self.escrita_OPC("ns=3;s=REG_USINA_Condicionadores", 0)

                # Leituras de registradores OPC e MB
                if self.leitura_OPC("ns=3;s=REG_USINA_Disj52LFechar") == True:
                    self.escrita_OPC("ns=3;s=REG_USINA_Disj52LFechar", False)
                    logger.info("Comando OPC recebido, fechand DJ52L")
                    self.dj52L.fechar()
                    
                if self.leitura_OPC("ns=3;s=REG_USINA_ResetAlarmes") == True:
                    self.escrita_OPC("ns=3;s=REG_USINA_ResetAlarmes", False)
                    logger.info("Comando OPC recebido: ns=3;s=REG_USINA_ResetAlarmes ")
                    for ug in self.ugs:
                        ug.reconhece_reset_ug()
                    self.dj52L.reconhece_reset_dj52L()

                if self.leitura_OPC("ns=3;s=REG_USINA_Condicionadores") == 1 and self.shared_dict["aux_borda{}".format(2)] == 0:
                    self.shared_dict["aux_borda{}".format(2)] = 1

                elif self.leitura_OPC("ns=3;s=REG_USINA_Condicionadores") == 0 and self.shared_dict["aux_borda{}".format(2)] == 1:
                    self.shared_dict["aux_borda{}".format(2)] = 0
                    self.escrita_OPC("ns=3;s=REG_USINA_Condicionadores", 0)
                    self.shared_dict["trip_condic_usina"] = False
                    self.dj52L.reconhece_reset_dj52L()

                # dj52L
                self.dj52L.passo()

                # UGs
                for ug in self.ugs:
                    # Leitura do dicionário compartilhado
                    self.shared_dict["setpoint_kw_ug{}".format(ug.id)] = self.leitura_MB(REG_MB["REG_UG{}_CtrlPotencia_Alvo".format(ug.id)])

                    if self.shared_dict["debug_setpoint_kw_ug{}".format(ug.id)] >= 0:
                        self.shared_dict["setpoint_kw_ug{}".format(ug.id)] = self.shared_dict["debug_setpoint_kw_ug{}".format(ug.id)]
                        self.escrita_MB(REG_MB["REG_UG{}_CtrlPotencia_Alvo".format(ug.id)], self.shared_dict["setpoint_kw_ug{}".format(ug.id)])
                        self.shared_dict["debug_setpoint_kw_ug{}".format(ug.id)] = -1


                    if self.shared_dict["trip_condic_ug{}".format(ug.id)] and self.shared_dict["aux_borda{}".format(ug.id + 2)] == 0:
                        self.shared_dict["aux_borda{}".format(ug.id + 2)] = 1
                        self.escrita_OPC("ns={0};s=REG_UG{0}_Condicionadores".format(ug.id), 1)

                    elif self.shared_dict["trip_condic_ug{}".format(ug.id)] == False and self.shared_dict["aux_borda{}".format(ug.id + 2)] == 1:
                        self.shared_dict["aux_borda{}".format(ug.id + 2)] = 0
                        self.escrita_OPC("ns={0};s=REG_UG{0}_Condicionadores".format(ug.id), 0)


                    if self.shared_dict["permissao_abrir_comporta_ug{}".format(ug.id)] == True and self.shared_dict["aux_borda{}".format(ug.id + 4)] == 0:
                        self.escrita_OPC("ns={0};s=REG_UG{0}_Permissao_Comporta".format(ug.id), 1)
                        self.shared_dict["aux_borda{}".format(ug.id + 4)] = 1

                    elif self.shared_dict["permissao_abrir_comporta_ug{}".format(ug.id)] == False and self.shared_dict["aux_borda{}".format(ug.id + 4)] == 1:
                        self.escrita_OPC("ns={0};s=REG_UG{0}_Permissao_Comporta".format(ug.id), 0)
                        self.shared_dict["aux_borda{}".format(ug.id + 4)] = 0


                    if self.shared_dict["condicao_falha_cracking_ug{}".format(ug.id)] == True and self.shared_dict["aux_borda{}".format(ug.id + 6)] == 0:
                        self.escrita_OPC("ns={0};s=REG_UG{0}_Condicionadores".format(ug.id), 1)
                        self.shared_dict["aux_borda{}".format(ug.id + 6)] = 1

                    elif self.shared_dict["reset_geral_condic"] == True and self.shared_dict["aux_borda{}".format(ug.id + 6)] == 1:
                        self.escrita_OPC("ns={0};s=REG_UG{0}_Condicionadores".format(ug.id), 0)
                        self.shared_dict["condicao_falha_cracking_ug{}".format(ug.id)] = False
                        self.shared_dict["aux_borda{}".format(ug.id + 6)] = 0

                    # Leitura de registradores OPC e MB
                    if self.leitura_OPC("ns={0};s=REG_UG{0}_Operacao_ResetAlarmes".format(ug.id)) == 1:
                        self.escrita_OPC("ns={0};s=REG_UG{0}_Operacao_ResetAlarmes".format(ug.id), 0)
                        ug.reconhece_reset_ug()


                    if self.leitura_OPC("ns={0};s=REG_UG{0}_Operacao_UP".format(ug.id)) == 1:
                        self.escrita_OPC("ns={0};s=REG_UG{0}_Operacao_UP".format(ug.id), 0)
                        ug.parar()

                    elif self.leitura_OPC("ns={0};s=REG_UG{0}_Operacao_US".format(ug.id)) == 1:
                        self.escrita_OPC("ns={0};s=REG_UG{0}_Operacao_US".format(ug.id), 0)
                        ug.partir()


                    if self.leitura_OPC("ns={0};s=REG_UG{0}_Status_Comporta".format(ug.id)) == 0 and self.shared_dict["aux_comp_f_ug{}".format(ug.id)] == 0:
                        self.escrita_OPC("ns={0};s=REG_UG{0}_Status_Comporta".format(ug.id), 0)
                        self.shared_dict["aux_comp_f_ug{}".format(ug.id)] = 1
                        self.shared_dict["thread_comp_fechada_ug{}".format(ug.id)] = True

                    elif self.leitura_OPC("ns={0};s=REG_UG{0}_Status_Comporta".format(ug.id)) != 0 and self.shared_dict["aux_comp_f_ug{}".format(ug.id)] == 1:
                        self.shared_dict["aux_comp_f_ug{}".format(ug.id)] = 0
                    

                    if self.leitura_OPC("ns={0};s=REG_UG{0}_Status_Comporta".format(ug.id)) == 1 and self.shared_dict["aux_comp_a_ug{}".format(ug.id)] == 0:
                        self.escrita_OPC("ns={0};s=REG_UG{0}_Status_Comporta".format(ug.id), 0)
                        self.shared_dict["aux_comp_a_ug{}".format(ug.id)] = 1
                        self.shared_dict["thread_comp_aberta_ug{}".format(ug.id)] = True

                    elif self.leitura_OPC("ns={0};s=REG_UG{0}_Status_Comporta".format(ug.id)) != 1 and self.shared_dict["aux_comp_a_ug{}".format(ug.id)] == 1:
                        self.shared_dict["aux_comp_a_ug{}".format(ug.id)] = 0
                    

                    if self.leitura_OPC("ns={0};s=REG_UG{0}_Status_Comporta".format(ug.id)) == 2 and self.shared_dict["aux_comp_c_ug{}".format(ug.id)] == 0:
                        self.escrita_OPC("ns={0};s=REG_UG{0}_Status_Comporta".format(ug.id), 0)
                        self.shared_dict["aux_comp_c_ug{}".format(ug.id)] = 1
                        self.shared_dict["thread_comp_cracking_ug{}".format(ug.id)] = True

                    elif self.leitura_OPC("ns={0};s=REG_UG{0}_Status_Comporta".format(ug.id)) != 2 and self.shared_dict["aux_comp_c_ug{}".format(ug.id)] == 1:
                        self.shared_dict["aux_comp_c_ug{}".format(ug.id)] = 0


                    if self.leitura_OPC("ns={0};s=REG_UG{0}_Operacao_EmergenciaLigar".format(ug.id)) == 1 and self.shared_dict["aux_borda{}".format(ug.id + 8)] == 0:
                        self.escrita_OPC("ns={0};s=REG_UG{0}_Operacao_EmergenciaLigar".format(ug.id), 1)
                        ug.tripar(1, "Operacao_EmergenciaLigar via OPC")
                        self.shared_dict["aux_borda{}".format(ug.id + 8)] = 1

                    elif self.leitura_OPC("ns={0};s=REG_UG{0}_Operacao_EmergenciaLigar".format(ug.id)) != 1 and self.shared_dict["aux_borda{}".format(ug.id + 8)] == 1:
                        self.escrita_OPC("ns={0};s=REG_UG{0}_Operacao_EmergenciaLigar".format(ug.id), 0)
                        ug.reconhece_reset_ug()
                        self.shared_dict["aux_borda{}".format(ug.id + 8)] = 0
                    
                    # UG passo
                    ug.passo()

                    # Escrita dos registradores UG
                    self.escrita_OPC("ns={0};s=REG_UG{0}_Operacao_EtapaAtual".format(ug.id),[int(ug.etapa_atual)],)
                    self.escrita_OPC("ns={0};s=REG_UG{0}_Gerador_PotenciaAtivaMedia".format(ug.id),[round(ug.potencia)],)
                    self.escrita_OPC("ns={0};s=REG_UG{0}_HorimetroEletrico_Hora".format(ug.id),[np.floor(ug.horimetro_hora)],)
                    self.escrita_OPC("ns={0};s=REG_UG{0}_Temperatura_01".format(ug.id),[round(self.shared_dict["temperatura_ug{}_fase_r".format(ug.id)])],)
                    self.escrita_OPC("ns={0};s=REG_UG{0}_Temperatura_02".format(ug.id),[round(self.shared_dict["temperatura_ug{}_fase_s".format(ug.id)])],)
                    self.escrita_OPC("ns={0};s=REG_UG{0}_Temperatura_03".format(ug.id),[round(self.shared_dict["temperatura_ug{}_fase_t".format(ug.id)])],)
                    self.escrita_OPC("ns={0};s=REG_UG{0}_Temperatura_04".format(ug.id),[round(self.shared_dict["temperatura_ug{}_nucleo_gerador_1".format(ug.id)])],)
                    self.escrita_OPC("ns={0};s=REG_UG{0}_Temperatura_05".format(ug.id),[round(self.shared_dict["temperatura_ug{}_mancal_guia".format(ug.id)])],)
                    self.escrita_OPC("ns={0};s=REG_UG{0}_Temperatura_06".format(ug.id),[round(self.shared_dict["temperatura_ug{}_mancal_guia_interno_1".format(ug.id)])],)
                    self.escrita_OPC("ns={0};s=REG_UG{0}_Temperatura_07".format(ug.id),[round(self.shared_dict["temperatura_ug{}_mancal_guia_interno_2".format(ug.id)])],)
                    self.escrita_OPC("ns={0};s=REG_UG{0}_Temperatura_08".format(ug.id),[round(self.shared_dict["temperatura_ug{}_patins_mancal_comb_1".format(ug.id)])],)
                    self.escrita_OPC("ns={0};s=REG_UG{0}_Temperatura_09".format(ug.id),[round(self.shared_dict["temperatura_ug{}_patins_mancal_comb_2".format(ug.id)])],)
                    self.escrita_OPC("ns={0};s=REG_UG{0}_Temperatura_10".format(ug.id),[round(self.shared_dict["temperatura_ug{}_mancal_casq_comb".format(ug.id)])],)
                    self.escrita_OPC("ns={0};s=REG_UG{0}_Temperatura_11".format(ug.id),[round(self.shared_dict["temperatura_ug{}_mancal_contra_esc_comb".format(ug.id)])],)
                    self.escrita_OPC("ns={0};s=REG_UG{0}_Pressao_Turbina".format(ug.id),[round(10 * self.shared_dict["pressao_turbina_ug{}".format(ug.id)])],)

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

                # Cálculo de enchimento do reservatório
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

                # Escrita de registradores USINA
                self.escrita_OPC("ns=3;s=REG_USINA_NivelBarragem",[round((self.shared_dict["nv_montante"]) * 10000)])
                self.escrita_OPC("ns=3;s=REG_USINA_NivelCanalAducao",[round((self.shared_dict["nv_jusante_grade"]) * 10000)])
                self.escrita_OPC("ns=3;s=REG_USINA_NivelCanalAducao",[round((self.shared_dict["nv_jusante_grade"]) * 10000)])
                self.escrita_OPC("ns=3;s=REG_USINA_Subestacao_PotenciaAtivaMedia",[round(self.shared_dict["potencia_kw_se"])])
                self.escrita_OPC("ns=3;s=REG_USINA_Subestacao_TensaoRS",[round(self.shared_dict["tensao_na_linha"] / 1000)])
                self.escrita_OPC("ns=3;s=REG_USINA_Subestacao_TensaoST",[round(self.shared_dict["tensao_na_linha"] / 1000)])
                self.escrita_OPC("ns=3;s=REG_USINA_Subestacao_TensaoTR",[round(self.shared_dict["tensao_na_linha"] / 1000)])
                self.escrita_MB(REG_MB["REG_USINA_potencia_kw_mp"], round(max(0, self.shared_dict["potencia_kw_mp"])))
                self.escrita_MB(REG_MB["REG_USINA_potencia_kw_mr"], round(max(0, self.shared_dict["potencia_kw_mr"])))

                # FIM COMPORTAMENTO USINA
                lock.release()
                tempo_restante = (self.passo_simulacao - (datetime.now() - t_inicio_passo).seconds)
                if tempo_restante > 0:
                    sleep(tempo_restante)
                else:
                    self.logger.warning("A simulação está demorando mais do que o permitido.")

            except KeyboardInterrupt:
                self.server_MB.stop()
                self.server_OPC.stop()
                self.shared_dict["stop_gui"] = True
                continue

    # Métodos com cálculos de propriedades da USINA
    def volume_para_nv_montate(self, volume):
        return min(max(460, 460 + volume / 40000), 462.37)

    def nv_montate_para_volume(self, nv_montante):
        return 40000 * (min(max(460, nv_montante), 462.37) - 460)

    def q_sanitaria(self, nv_montante):
        if  self.ug1.etapa_atual != 1:
            return 0
        elif self.ug2.etapa_atual != 1:
            return 0
        else:
            return 2.33

    # Métodos de leitura e escrita OPC/MB
    def leitura_OPC(self, registrador):
        leitura_OPC = self.server_OPC.get_node(registrador).get_value()
        return leitura_OPC

    def escrita_OPC(self, registrador, valor) -> bool:
        escrita_OPC = self.server_OPC.get_node(registrador).set_value(valor)
        return escrita_OPC

    def leitura_MB(self, registrador):
        leitura_MB = self.DB.get_words(registrador)[0]
        return leitura_MB

    def escrita_MB(self, registrador, valor):
        escrita_MB = self.DB.set_words(registrador, [valor])
        return escrita_MB