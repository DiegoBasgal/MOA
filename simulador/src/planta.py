import re
import logging
import threading
import SIM_REG
import numpy as np

from sys import stdout
from time import sleep
from opcua import Server, ua
from datetime import datetime
from asyncio.log import logger
from pyModbusTCP.server import ModbusServer, DataBank

from UG import Ug
from Dj52L import Dj52L

REG_MB = SIM_REG.REG_MB
REG_OPC = SIM_REG.REG_OPC

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
        self.build_server()
        
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
                    self.escrita_MB(REG_MB["REG_USINA_Condicionadores"], 1)

                elif self.shared_dict["trip_condic_usina"] == False and self.shared_dict["aux_borda{}".format(1)] == 1:
                    self.shared_dict["aux_borda{}".format(1)] = 0
                    self.escrita_MB(REG_MB["REG_USINA_Condicionadores"], 0)
                    self.dj52L.reconhece_reset_dj52L()

                if self.shared_dict["reset_geral_condic"] == True:
                    self.escrita_MB(REG_MB["REG_UG1_Condicionadores"], 0)
                    self.escrita_MB(REG_MB["REG_UG2_Condicionadores"], 0)
                    self.escrita_MB(REG_MB["REG_USINA_Condicionadores"], 0)

                # Leituras de registradores OPC e MB
                if self.leiturabit_OPC(REG_OPC["CMD_SE_FECHA_52L"], 4) == True:
                    self.escritabit_OPC(REG_OPC["CMD_SE_FECHA_52L"], 4, 1)
                    logger.info("Comando OPC recebido, fechando DJ52L")
                    self.dj52L.fechar()
                    
                if self.leiturabit_OPC(REG_OPC["RESET_FALHAS_BARRA_CA"], 0) == True:
                    self.escritabit_OPC(REG_OPC["RESET_FALHAS_BARRA_CA"], 0, 0)
                    logger.info("Comando OPC recebido: RESET_FALHAS_BARRA_CA")
                    for ug in self.ugs:
                        ug.reconhece_reset_ug()
                    self.dj52L.reconhece_reset_dj52L()

                if self.leitura_MB(REG_MB["REG_USINA_Condicionadores"]) == 1 and self.shared_dict["aux_borda{}".format(2)] == 0:
                    self.shared_dict["aux_borda{}".format(2)] = 1

                elif self.leitura_MB(REG_MB["REG_USINA_Condicionadores"]) == 0 and self.shared_dict["aux_borda{}".format(2)] == 1:
                    self.shared_dict["aux_borda{}".format(2)] = 0
                    self.escrita_MB(REG_MB["REG_USINA_Condicionadores"], 0)
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
                        self.escrita_MB(REG_MB["REG_UG{}_Condicionadores".format(ug.id)], 1)

                    elif self.shared_dict["trip_condic_ug{}".format(ug.id)] == False and self.shared_dict["aux_borda{}".format(ug.id + 2)] == 1:
                        self.shared_dict["aux_borda{}".format(ug.id + 2)] = 0
                        self.escrita_MB(REG_MB["REG_UG{}_Condicionadores".format(ug.id)], 0)


                    if self.shared_dict["permissao_abrir_comporta_ug{}".format(ug.id)] == True and self.shared_dict["aux_borda{}".format(ug.id + 4)] == 0:
                        self.escritabit_OPC(REG_OPC["CP{}_PERMISSIVOS_OK"].format(ug.id), 31, 1)
                        self.shared_dict["aux_borda{}".format(ug.id + 4)] = 1

                    elif self.shared_dict["permissao_abrir_comporta_ug{}".format(ug.id)] == False and self.shared_dict["aux_borda{}".format(ug.id + 4)] == 1:
                        self.escritabit_OPC(REG_OPC["CP{}_PERMISSIVOS_OK"].format(ug.id), 31, 0)
                        self.shared_dict["aux_borda{}".format(ug.id + 4)] = 0


                    if self.shared_dict["condicao_falha_cracking_ug{}".format(ug.id)] == True and self.shared_dict["aux_borda{}".format(ug.id + 6)] == 0:
                        self.escrita_MB(REG_MB["REG_UG{}_Condicionadores".format(ug.id)], 1)
                        self.shared_dict["aux_borda{}".format(ug.id + 6)] = 1

                    elif self.shared_dict["reset_geral_condic"] == True and self.shared_dict["aux_borda{}".format(ug.id + 6)] == 1:
                        self.escrita_MB(REG_MB["REG_UG{}_Condicionadores".format(ug.id)], 0)
                        self.shared_dict["condicao_falha_cracking_ug{}".format(ug.id)] = False
                        self.shared_dict["aux_borda{}".format(ug.id + 6)] = 0

                    # Leitura de registradores OPC e MB
                    if self.leiturabit_OPC(REG_OPC["UG{}_CMD_PARTIDA_CMD_SINCRONISMO".format(ug.id)], 10) == True:
                        self.escritabit_OPC(REG_OPC["UG{}_CMD_PARTIDA_CMD_SINCRONISMO".format(ug.id)], 10, 0)
                        ug.partir()

                    elif self.leiturabit_OPC(REG_OPC["UG{}_CMD_PARADA_CMD_PARA_RV_APLICA_FREIO".format(ug.id)], 13) == True:
                        self.escritabit_OPC(REG_OPC["UG{}_CMD_PARADA_CMD_PARA_RV_APLICA_FREIO".format(ug.id)], 13, 0)
                        ug.parar()


                    if self.leiturabit_OPC(REG_OPC["CP{}_CMD_FECHAMENTO".format(ug.id)], 3) == True and self.shared_dict["aux_comp_f_ug{}".format(ug.id)] == 0:
                        self.escritabit_OPC(REG_OPC["CP{}_CMD_FECHAMENTO".format(ug.id)], 3, 0)
                        self.escritabit_OPC(REG_OPC["CP{}_COMPORTA_OPERANDO".format(ug.id)], 0, 1)
                        self.shared_dict["aux_comp_f_ug{}".format(ug.id)] = 1
                        self.shared_dict["thread_comp_fechada_ug{}".format(ug.id)] = True
                        if self.shared_dict["comporta_fechada_ug{}"] == True:
                            self.escritabit_OPC(REG_OPC["CP{}_COMPORTA_OPERANDO".format(ug.id)], 0, 0)

                    elif self.leiturabit_OPC(REG_OPC["CP{}_CMD_FECHAMENTO".format(ug.id)], 3) == False and self.shared_dict["aux_comp_f_ug{}".format(ug.id)] == 1:
                        self.shared_dict["aux_comp_f_ug{}".format(ug.id)] = 0


                    if self.leiturabit_OPC(REG_OPC["CP{}_CMD_ABERTURA_TOTAL".format(ug.id)], 2) == True and self.shared_dict["aux_comp_a_ug{}".format(ug.id)] == 0:
                        self.escritabit_OPC(REG_OPC["CP{}_CMD_ABERTURA_TOTAL".format(ug.id)], 2, 0)
                        self.escritabit_OPC(REG_OPC["CP{}_COMPORTA_OPERANDO".format(ug.id)], 31, 1)
                        self.shared_dict["aux_comp_a_ug{}".format(ug.id)] = 1
                        self.shared_dict["thread_comp_aberta_ug{}".format(ug.id)] = True
                        if self.shared_dict["comporta_aberta_ug{}"] == True:
                            self.escritabit_OPC(REG_OPC["CP{}_COMPORTA_OPERANDO".format(ug.id)], 31, 0)

                    elif self.leiturabit_OPC(REG_OPC["CP{}_CMD_ABERTURA_TOTAL".format(ug.id)], 2) == False and self.shared_dict["aux_comp_a_ug{}".format(ug.id)] == 1:
                        self.shared_dict["aux_comp_a_ug{}".format(ug.id)] = 0
                    

                    if self.leiturabit_OPC(REG_OPC["CP{}_CMD_ABERTURA_CRACKING".format(ug.id)], 1) == True and self.shared_dict["aux_comp_c_ug{}".format(ug.id)] == 0:
                        self.escritabit_OPC(REG_OPC["CP{}_CMD_ABERTURA_CRACKING".format(ug.id)], 1, 0)
                        self.escritabit_OPC(REG_OPC["CP{}_COMPORTA_OPERANDO".format(ug.id)], 31, 1)
                        self.shared_dict["aux_comp_c_ug{}".format(ug.id)] = 1
                        self.shared_dict["thread_comp_cracking_ug{}".format(ug.id)] = True
                        if self.shared_dict["comporta_cracking_ug{}"] == True:
                            self.escritabit_OPC(REG_OPC["CP{}_COMPORTA_OPERANDO".format(ug.id)], 31, 0)

                    elif self.leiturabit_OPC(REG_OPC["CP{}_CMD_ABERTURA_CRACKING".format(ug.id)], 1) == False and self.shared_dict["aux_comp_c_ug{}".format(ug.id)] == 1:
                        self.shared_dict["aux_comp_c_ug{}".format(ug.id)] = 0


                    if self.leiturabit_OPC(REG_OPC["UG{}_CMD_PARADA_EMERGENCIA".format(ug.id)], 4) == True and self.shared_dict["aux_borda{}".format(ug.id + 8)] == 0:
                        self.escritabit_OPC(REG_OPC["UG{}_CMD_PARADA_EMERGENCIA".format(ug.id)], 4, 1)
                        ug.tripar(1, "Operacao_EmergenciaLigar via OPC")
                        self.shared_dict["aux_borda{}".format(ug.id + 8)] = 1

                    elif self.leiturabit_OPC(REG_OPC["UG{}_CMD_PARADA_EMERGENCIA".format(ug.id)], 4) == False and self.shared_dict["aux_borda{}".format(ug.id + 8)] == 1:
                        self.escritabit_OPC(REG_OPC["UG{}_CMD_PARADA_EMERGENCIA".format(ug.id)], 4, 0)
                        ug.reconhece_reset_ug()
                        self.shared_dict["aux_borda{}".format(ug.id + 8)] = 0
                    
                    # UG passo
                    ug.passo()
                    
                    # Escrita dos registradores UG
                    self.escrita_MB(REG_MB["UG{}_RV_ESTADO_OPERACAO".format(ug.id)],[int(ug.etapa_atual)],)
                    self.escrita_OPC(REG_OPC["UG{}_UG_P".format(ug.id)],[round(ug.potencia)],)
                    self.escrita_OPC(REG_OPC["UG{}_UG_HORIMETRO".format(ug.id)],[np.floor(ug.horimetro_hora)],)
                    self.escrita_OPC(REG_OPC["UG{}_TEMP_GERADOR_FASE_A".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_fase_r".format(ug.id)])],)
                    self.escrita_OPC(REG_OPC["UG{}_TEMP_GERADOR_FASE_B".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_fase_s".format(ug.id)])],)
                    self.escrita_OPC(REG_OPC["UG{}_TEMP_GERADOR_FASE_C".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_fase_t".format(ug.id)])],)
                    self.escrita_OPC(REG_OPC["UG{}_TEMP_GERADOR_NUCLEO".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_nucleo_gerador_1".format(ug.id)])],)
                    self.escrita_OPC(REG_OPC["UG{}_TEMP_MANCAL_GUIA_GERADOR".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_mancal_guia".format(ug.id)])],)
                    self.escrita_OPC(REG_OPC["UG{}_TEMP_1_MANCAL_GUIA_INTERNO".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_mancal_guia_interno_1".format(ug.id)])],)
                    self.escrita_OPC(REG_OPC["UG{}_TEMP_2_MANCAL_GUIA_INTERNO".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_mancal_guia_interno_2".format(ug.id)])],)
                    self.escrita_OPC(REG_OPC["UG{}_TEMP_1_PATINS_MANCAL_COMBINADO".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_patins_mancal_comb_1".format(ug.id)])],)
                    self.escrita_OPC(REG_OPC["UG{}_TEMP_2_PATINS_MANCAL_COMBINADO".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_patins_mancal_comb_2".format(ug.id)])],)
                    self.escrita_OPC(REG_OPC["UG{}_TEMP_CASQ_MANCAL_COMBINADO".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_mancal_casq_comb".format(ug.id)])],)
                    self.escrita_OPC(REG_OPC["UG{}_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO".format(ug.id)],[round(self.shared_dict["temperatura_ug{}_mancal_contra_esc_comb".format(ug.id)])],)
                    self.escrita_OPC(REG_OPC["UG{}_PRESSAO_ENTRADA_TURBINA".format(ug.id)],[round(10 * self.shared_dict["pressao_turbina_ug{}".format(ug.id)])],)

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
                self.escrita_OPC(REG_OPC["NIVEL_MONTANTE"],[round((self.shared_dict["nv_montante"]) * 10000)])
                self.escrita_OPC(REG_OPC["NIVEL_JUSANTE_GRADE_COMPORTA_1"],[round((self.shared_dict["nv_jusante_grade"]) * 10000)])
                self.escrita_OPC(REG_OPC["NIVEL_JUSANTE_GRADE_COMPORTA_2"],[round((self.shared_dict["nv_jusante_grade"]) * 10000)])
                self.escrita_OPC(REG_OPC["LT_P"],[round(self.shared_dict["potencia_kw_se"])])
                self.escrita_OPC(REG_OPC["LT_VAB"],[round(self.shared_dict["tensao_na_linha"] / 1000)])
                self.escrita_OPC(REG_OPC["LT_VBC"],[round(self.shared_dict["tensao_na_linha"] / 1000)])
                self.escrita_OPC(REG_OPC["LT_VCA"],[round(self.shared_dict["tensao_na_linha"] / 1000)])
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

    def escrita_OPC(self, registrador, valor) -> int:
        escrita_OPC = self.server_OPC.get_node(registrador).set_value(valor)
        return escrita_OPC
    
    def leiturabit_OPC(self, registrador, bit) -> bool:
        leitura = self.leitura_OPC(registrador)
        return leitura & 2**bit

    def escritabit_OPC(self, registrador, bit, valor) -> int:
        leitura = self.leitura_OPC(registrador)
        bin = [int(x) for x in list('{0:0b}'.format(leitura))]
        for i in range(len(bin)):
            if bit == i:
                bin[i] = valor
                break
        v = sum(val*(2**x) for x, val in enumerate(reversed(bin)))
        return self.server_OPC.get_node(registrador).set_value(v)

    def leitura_MB(self, registrador):
        leitura_MB = self.DB.get_words(registrador)[0]
        return leitura_MB

    def escrita_MB(self, registrador, valor):
        escrita_MB = self.DB.set_words(registrador, [valor])
        return escrita_MB

    def build_server(self):
        for i in REG_MB:
            self.DB.set_words(REG_MB[i], [0])

        objects = self.server_OPC.get_objects_node()

        reg_sa_f = objects.add_folder("ns=7;s=CLP_SA", "Serviço Auxiliar")
        reg_sa_c = reg_sa_f.add_folder("ns=7;s=CLP_SA.SA.DB_COMANDOS", "Comandos")
        reg_sa_cd = reg_sa_c.add_object("ns=7;s=CLP_SA.SA.DB_COMANDOS.DIGITAIS" , "Digitais")
        reg_sa_s = reg_sa_f.add_folder("ns=7;s=CLP_SA.SA.DB_STATUS", "Retornos")
        reg_sa_sm = reg_sa_s.add_object("ns=7;s=CLP_SA.SA.DB_STATUS.MULTIMEDIDOR_LT", "Multimedidor LT")

        reg_tda_f = objects.add_folder("ns=7;s=CLP_TA", "Tomada da Água")
        reg_tda_c = reg_tda_f.add_folder("ns=7;s=CLP_TA.STA.DB_COMANDOS", "Comandos")
        reg_tda_cd = reg_tda_c.add_object("ns=7;s=CLP_TA.TA.DB_COMANDOS.DIGITAIS" , "Digitais")
        reg_tda_s = reg_tda_f.add_folder("ns=7;s=CLP_TA.TA.DB_STATUS", "Retornos")
        reg_tda_sd = reg_tda_s.add_object("ns=7;s=CLP_TA.TA.DB_STATUS.DIGITAIS", "Digitais")
        reg_tda_sa = reg_tda_s.add_object("ns=7;s=CLP_TA.TA.DB_STATUS.ANALOGICOS", "Analógicos")

        reg_ug1_f = objects.add_folder("ns=7;s=CLP_UG1", "UG1")
        reg_ug1_c = reg_ug1_f.add_folder("ns=7;s=CLP_UG1.UG1.DB_COMANDOS", "Comandos")
        reg_ug1_cd = reg_ug1_c.add_object("ns=7;s=CLP_UG1.UG1.DB_COMANDOS.DIGITAIS", "Digitais")
        reg_ug1_s = reg_ug1_f.add_folder("ns=7;s=CLP_UG1.UG1.DB_STATUS", "Retornos")
        reg_ug1_sa = reg_ug1_s.add_object("ns=7;s=CLP_UG1.UG1.DB_STATUS.ANALOGICAS", "Analógicos")
        reg_ug1_sm = reg_ug1_s.add_object("ns=7;s=CLP_UG1.UG1.DB_STATUS.MULTIMEDIDOR", "Multimedidor")
        reg_ug1_sh = reg_ug1_s.add_object("ns=7;s=CLP_UG1.UG1.DB_STATUS.HORIMETROS", "Horimetros")

        reg_ug2_f = objects.add_folder("ns=7;s=CLP_UG2", "UG2")
        reg_ug2_c = reg_ug2_f.add_folder("ns=7;s=CLP_UG2.UG2.DB_COMANDOS", "Comandos")
        reg_ug2_cd = reg_ug2_c.add_object("ns=7;s=CLP_UG2.UG2.DB_COMANDOS.DIGITAIS", "Digitais")
        reg_ug2_s = reg_ug2_f.add_folder("ns=7;s=CLP_UG2.UG2.DB_STATUS", "Retornos")
        reg_ug2_sa = reg_ug2_s.add_object("ns=7;s=CLP_UG2.UG2.DB_STATUS.ANALOGICAS", "Analógicos")
        reg_ug2_sm = reg_ug2_s.add_object("ns=7;s=CLP_UG2.UG2.DB_STATUS.MULTIMEDIDOR", "Multimedidor")
        reg_ug2_sh = reg_ug2_s.add_object("ns=7;s=CLP_UG2.UG2.DB_STATUS.HORIMETROS", "Horimetros")


        for i in REG_OPC:
           if re.search("ns=7;s=CLP_SA.SA.DB_COMANDOS", REG_OPC[i]):
              try:
                 reg_sa_cd.add_variable(REG_OPC[i], re.split("[.]", REG_OPC[i])[-1], 0, ua.VariantType.Int32).\
                    set_writable(True) if re.search("DIGITAIS", REG_OPC[i]) else print("")
              except ua.UaError:
                 pass
           elif re.search("ns=7;s=CLP_SA.SA.DB_STATUS", REG_OPC[i]):
              try:
                 reg_sa_sm.add_variable(REG_OPC[i], re.split("[.]", REG_OPC[i])[-1], 0, ua.VariantType.Int32).\
                    set_writable(True) if re.search("MULTIMEDIDOR_LT", REG_OPC[i]) else print("")
              except ua.UaError:
                 pass
             
           if re.search("ns=7;s=CLP_TA.TA.DB_COMANDOS", REG_OPC[i]):
              try:
                 reg_tda_cd.add_variable(REG_OPC[i], re.split("[.]", REG_OPC[i])[-1], 0, ua.VariantType.Int32).\
                    set_writable(True) if re.search("DIGITAIS", REG_OPC[i]) else print("")
              except ua.UaError:
                 pass
           elif re.search("ns=7;s=CLP_TA.TA.DB_STATUS", REG_OPC[i]):
              try:
                 reg_tda_sd.add_variable(REG_OPC[i], re.split("[.]", REG_OPC[i])[-1], 0, ua.VariantType.Int32).\
                    set_writable(True) if re.search("DIGITAIS", REG_OPC[i]) else print("")
                 reg_tda_sa.add_variable(REG_OPC[i], re.split("[.]", REG_OPC[i])[-1], 0, ua.VariantType.Int32).\
                    set_writable(True) if re.search("ANALOGICOS", REG_OPC[i]) else print("")
              except ua.UaError:
                 pass
             
           if re.search("ns=7;s=CLP_UG1.UG1.DB_COMANDOS", REG_OPC[i]):
              try:
                 reg_ug1_cd.add_variable(REG_OPC[i], re.split("[.]", REG_OPC[i])[-1], 0, ua.VariantType.Int32).\
                    set_writable(True) if re.search("DIGITAIS", REG_OPC[i]) else print("")
              except ua.UaError:
                 pass
           elif re.search("ns=7;s=CLP_UG1.UG1.DB_STATUS", REG_OPC[i]):
              try:
                 reg_ug1_sm.add_variable(REG_OPC[i], re.split("[.]", REG_OPC[i])[-1], 0, ua.VariantType.Int32).\
                    set_writable(True) if re.search("MULTIMEDIDOR", REG_OPC[i]) else print("")
                 reg_ug1_sa.add_variable(REG_OPC[i], re.split("[.]", REG_OPC[i])[-1], 0, ua.VariantType.Int32).\
                    set_writable(True) if re.search("ANALOGICAS", REG_OPC[i]) else print("")
                 reg_ug1_sh.add_variable(REG_OPC[i], re.split("[.]", REG_OPC[i])[-1], 0, ua.VariantType.Int32).\
                    set_writable(True) if re.search("HORIMETROS", REG_OPC[i]) else print("")
              except ua.UaError:
                 pass
             
           if re.search("ns=7;s=CLP_UG2.UG2.DB_COMANDOS", REG_OPC[i]):
              try:
                 reg_ug2_cd.add_variable(REG_OPC[i], re.split("[.]", REG_OPC[i])[-1], 0, ua.VariantType.Int32).\
                    set_writable(True) if re.search("DIGITAIS", REG_OPC[i]) else print("")
              except ua.UaError:
                 pass
           elif re.search("ns=7;s=CLP_UG2.UG2.DB_STATUS", REG_OPC[i]):
              try:
                 reg_ug2_sm.add_variable(REG_OPC[i], re.split("[.]", REG_OPC[i])[-1], 0, ua.VariantType.Int32).\
                    set_writable(True) if re.search("MULTIMEDIDOR", REG_OPC[i]) else print("")
                 reg_ug2_sa.add_variable(REG_OPC[i], re.split("[.]", REG_OPC[i])[-1], 0, ua.VariantType.Int32).\
                    set_writable(True) if re.search("ANALOGICAS", REG_OPC[i]) else print("")
                 reg_ug2_sh.add_variable(REG_OPC[i], re.split("[.]", REG_OPC[i])[-1], 0, ua.VariantType.Int32).\
                    set_writable(True) if re.search("HORIMETROS", REG_OPC[i]) else print("")
              except ua.UaError:
                 pass
             
        return True