import pytz
import logging
import threading
import traceback
import numpy as np

import simulador.dicionarios.dict as dct

from time import sleep
from datetime import datetime
from asyncio.log import logger
from pyModbusTCP.server import ModbusServer, DataBank

from simulador.dicionarios.reg import *
from simulador.dicionarios.const import *
from simulador.funcoes.escrita import Escrita
from simulador.funcoes.leitura import Leitura

from se import Dj52L
from ug import Unidade as UG
from simulador.funcoes.temporizador import Temporizador

lock = threading.Lock()
logger = logging.getLogger('__main__')

class Planta:
    def __init__(self, dj52L: "Dj52L", ugs: "list[UG]", time_handler: "Temporizador") -> None:
        self.ugs = ugs
        self.dj52L = dj52L
        self.dict = dct.compartilhado
        self.temporizador = time_handler

        self.escala_ruido = time_handler.escala_ruido
        self.passo_simulacao = time_handler.passo_simulacao
        self.segundos_por_passo = time_handler.segundos_por_passo

        self.borda_db_condic = False
        self.borda_usn_condic = False

        # Intância de servidores MB
        self.DB = DataBank()
        self.server_MB = ModbusServer(host='localhost', port=502, no_block=True)

        # Incia os servidores
        self.server_MB.start()

        # Inicia Classes de Leitura e Escrita customizadas
        self.leitura = Leitura(self.DB)
        self.escrita = Escrita(self.DB)

    def run(self):

        volume = self.nv_montate_para_volume(self.dict['USN']['nv_montante'])
        self.dj52L.abrir()

        # Loop principal
        while not self.dict['GLB']['stop_sim']:
            self.dict['GLB']['stop_sim'] = self.dict['GLB']['stop_gui']
            try:
                t_inicio_passo = datetime.now()
                lock.acquire()

                # Acerto temportal
                self.dict['GLB']['tempo_simul'] += self.segundos_por_passo

                # Leitura do dicionário compartilhado
                if self.dict['USN']['trip_condic_usina'] and self.dict['USN'][f'aux_borda{1}'] == 0:
                    self.dict['USN'][f'aux_borda{1}'] = 1
                    self.DB.set_words(MB['USN_CONDICIONADOR'], [1])

                elif not self.dict['USN']['trip_condic_usina'] and self.dict['USN'][f'aux_borda{1}'] == 1:
                    self.dict['USN'][f'aux_borda{1}'] = 0
                    self.DB.set_words(MB['USN_CONDICIONADOR'], [0])
                    self.dj52L.reconhece_reset()

                if self.dict['USN']['reset_geral_condic']:
                    self.DB.set_words(MB['UG1_CONDICIONADOR'], [0])
                    self.DB.set_words(MB['UG2_CONDICIONADOR'], [0])
                    self.DB.set_words(MB['USN_CONDICIONADOR'], [0])

                # Leituras de registradores MB
                if self.DB.get_words(MB['DJL_CMD_FECHAR'])[0] == 1:
                    self.DB.set_words(MB['DJL_CMD_FECHAR'], [1])
                    logger.info('Comando recebido, fechando DJ52L')
                    self.dj52L.fechar()

                if self.DB.get_words(MB['BARRA_CA_RST_FLH'])[0] == 1:
                    self.DB.set_words(MB['BARRA_CA_RST_FLH'], [0])
                    logger.info('Comando recebido: BARRA_CA_RST_FLH')
                    for ug in self.ugs:
                        ug.reconhece_reset()
                    self.dj52L.reconhece_reset()

                if self.DB.get_words(MB['USN_CONDICIONADOR'])[0] == 1 and self.dict['USN'][f'aux_borda{2}'] == 0:
                    self.dict['USN'][f'aux_borda{2}'] = 1

                elif self.DB.get_words(MB['USN_CONDICIONADOR']) == 0 and self.dict['USN'][f'aux_borda{2}'] == 1:
                    self.dict['USN'][f'aux_borda{2}'] = 0
                    self.DB.set_words(MB['USN_CONDICIONADOR'], [0])
                    self.dict['USN']['trip_condic_usina'] = False
                    self.dj52L.reconhece_reset()

                # dj52L
                self.dj52L.passo()


                # UGs
                for ug in self.ugs:
                    # Leitura do dicionário compartilhado
                    self.dict['UG'][f'setpoint_kw_ug{ug.id}'] = self.DB.get_words(MB[f'UG{ug.id}_SETPONIT'])[0]

                    if self.dict['UG'][f'debug_setpoint_kw_ug{ug.id}'] >= 0:
                        self.dict['UG'][f'setpoint_kw_ug{ug.id}'] = self.dict['UG'][f'debug_setpoint_kw_ug{ug.id}']
                        self.DB.set_words(MB[f'UG{ug.id}_SETPONIT'], [self.dict['UG'][f'setpoint_kw_ug{ug.id}']])
                        self.dict['UG'][f'debug_setpoint_kw_ug{ug.id}'] = -1

                    if self.dict['UG'][f'trip_condic_ug{ug.id}'] and self.dict['USN'][f'aux_borda{ug.id + 2}'] == 0:
                        self.dict['USN'][f'aux_borda{ug.id + 2}'] = 1
                        self.DB.set_words(MB[f'UG{ug.id}_CONDICIONADOR'], [1])

                    elif not self.dict['UG'][f'trip_condic_ug{ug.id}'] and self.dict['USN'][f'aux_borda{ug.id + 2}'] == 1:
                        self.dict['USN'][f'aux_borda{ug.id + 2}'] = 0
                        self.DB.set_words(MB[f'UG{ug.id}_CONDICIONADOR'], [0])


                    if self.dict['UG'][f'permissao_abrir_comporta_ug{ug.id}'] and self.dict['USN'][f'aux_borda{ug.id + 4}'] == 0:
                        self.DB.set_words(MB[f'CP{ug.id}_PERMISSIVOS_OK'], [1])
                        self.dict['USN'][f'aux_borda{ug.id + 4}'] = 1

                    elif not self.dict['UG'][f'permissao_abrir_comporta_ug{ug.id}'] and self.dict['USN'][f'aux_borda{ug.id + 4}'] == 1:
                        self.DB.set_words(MB[f'CP{ug.id}_PERMISSIVOS_OK'], [0])
                        self.dict['USN'][f'aux_borda{ug.id + 4}'] = 0


                    if self.dict['UG'][f'condicao_falha_cracking_ug{ug.id}'] and self.dict['USN'][f'aux_borda{ug.id + 6}'] == 0:
                        self.DB.set_words(MB[f'UG{ug.id}_CONDICIONADOR'], [1])
                        self.dict['USN'][f'aux_borda{ug.id + 6}'] = 1

                    elif self.dict['USN']['reset_geral_condic'] and self.dict['USN'][f'aux_borda{ug.id + 6}'] == 1:
                        self.DB.set_words(MB[f'UG{ug.id}_CONDICIONADOR'], [0])
                        self.dict['UG'][f'condicao_falha_cracking_ug{ug.id}'] = False
                        self.dict['USN'][f'aux_borda{ug.id + 6}'] = 0

                    # Leitura de registradores MB
                    if self.DB.get_words(MB[f'UG{ug.id}_PARTIDA_CMD_SINCRONISMO'])[0] == 1:
                        self.DB.set_words(MB[f'UG{ug.id}_PARTIDA_CMD_SINCRONISMO'], [0])
                        ug.partir()

                    elif self.DB.get_words(MB[f'UG{ug.id}_PARADA_CMD_EMERGENCIA'])[0] == 1:
                        self.DB.set_words(MB[f'UG{ug.id}_PARADA_CMD_EMERGENCIA'], [0])
                        ug.parar()


                    if self.DB.get_words(MB[f'CP{ug.id}_CMD_FECHAMENTO'])[0] == 1 and self.dict['UG'][f'aux_comp_f_ug{ug.id}'] == 0:
                        self.DB.set_words(MB[f'CP{ug.id}_CMD_FECHAMENTO'], [0])
                        self.DB.set_words(MB[f'CP{ug.id}_OPERANDO'], [1])
                        self.dict['UG'][f'aux_comp_f_ug{ug.id}'] = 1
                        self.dict['UG'][f'thread_comp_fechada_ug{ug.id}'] = True
                        if self.dict['UG'][f'comporta_fechada_ug{ug.id}'] == True:
                            self.DB.set_words(MB[f'CP{ug.id}_OPERANDO'], [0])

                    elif self.DB.get_words(MB[f'CP{ug.id}_CMD_FECHAMENTO'])[0] == 0 and self.dict['UG'][f'aux_comp_f_ug{ug.id}'] == 1:
                        self.dict['UG'][f'aux_comp_f_ug{ug.id}'] = 0


                    if self.DB.get_words(MB[f'CP{ug.id}_CMD_ABERTURA_TOTAL'])[0] == 1 and self.dict['UG'][f'aux_comp_a_ug{ug.id}'] == 0:
                        self.DB.set_words(MB[f'CP{ug.id}_CMD_ABERTURA_TOTAL'], [0])
                        self.DB.set_words(MB[f'CP{ug.id}_OPERANDO'], [1])
                        self.dict['UG'][f'aux_comp_a_ug{ug.id}'] = 1
                        self.dict['UG'][f'thread_comp_aberta_ug{ug.id}'] = True
                        if self.dict['UG'][f'comporta_aberta_ug{ug.id}']:
                            self.DB.set_words(MB[f'CP{ug.id}_OPERANDO'], [0])

                    elif self.DB.get_words(MB[f'CP{ug.id}_CMD_ABERTURA_TOTAL'])[0] == 0 and self.dict['UG'][f'aux_comp_a_ug{ug.id}'] == 1:
                        self.dict['UG'][f'aux_comp_a_ug{ug.id}'] = 0


                    if self.DB.get_words(MB[f'CP{ug.id}_CMD_ABERTURA_CRACKING'])[0] == 1 and self.dict['UG'][f'aux_comp_c_ug{ug.id}'] == 0:
                        self.DB.set_words(MB[f'CP{ug.id}_CMD_ABERTURA_CRACKING'], [0])
                        self.DB.set_words(MB[f'CP{ug.id}_OPERANDO'], [1])
                        self.dict['UG'][f'aux_comp_c_ug{ug.id}'] = 1
                        self.dict['UG'][f'thread_comp_cracking_ug{ug.id}'] = True
                        if self.dict['UG'][f'comporta_cracking_ug{ug.id}']:
                            self.DB.set_words(MB[f'CP{ug.id}_OPERANDO'], [0])

                    elif self.DB.get_words(MB[f'CP{ug.id}_CMD_ABERTURA_CRACKING'])[0] == 0 and self.dict['UG'][f'aux_comp_c_ug{ug.id}'] == 1:
                        self.dict['UG'][f'aux_comp_c_ug{ug.id}'] = 0


                    if self.DB.get_words(MB[f'UG{ug.id}_CMD_PARADA_EMERGENCIA'])[0] == 1 and self.dict['USN'][f'aux_borda{ug.id + 8}'] == 0:
                        self.DB.set_words(MB[f'UG{ug.id}_CMD_PARADA_EMERGENCIA'], [1])
                        ug.tripar(1, 'Operacao_EmergenciaLigar')
                        self.dict['USN'][f'aux_borda{ug.id + 8}'] = 1

                    elif self.DB.get_words(MB[f'UG{ug.id}_CMD_PARADA_EMERGENCIA'])[0] == 0 and self.dict['USN'][f'aux_borda{ug.id + 8}'] == 1:
                        self.DB.set_words(MB[f'UG{ug.id}_CMD_PARADA_EMERGENCIA'], [0])
                        ug.reconhece_reset()
                        self.dict['USN'][f'aux_borda{ug.id + 8}'] = 0

                    # UG passo
                    for ug in self.ugs:
                        ug.passo()

                    # Escrita dos registradores UG
                    self.DB.set_words(MB[f'UG{ug.id}_RV_ESTADO_OPERACAO'],[int(ug.etapa_atual)],)

                    self.DB.set_words(MB[f'UG{ug.id}_P'],[round(ug.potencia)],)
                    self.DB.set_words(MB[f'UG{ug.id}_HORIMETRO'],[np.floor(ug.horimetro_hora)],)
                    self.DB.set_words(MB[f'UG{ug.id}_GERADOR_FASE_A_TMP'],[round(self.dict['UG'][f'temperatura_ug{ug.id}_fase_r'])],)
                    self.DB.set_words(MB[f'UG{ug.id}_GERADOR_FASE_B_TMP'],[round(self.dict['UG'][f'temperatura_ug{ug.id}_fase_s'])],)
                    self.DB.set_words(MB[f'UG{ug.id}_GERADOR_FASE_C_TMP'],[round(self.dict['UG'][f'temperatura_ug{ug.id}_fase_t'])],)
                    self.DB.set_words(MB[f'UG{ug.id}_GERADOR_NUCL_ESTAT_TMP'],[round(self.dict['UG'][f'temperatura_ug{ug.id}_nucleo_gerador_1'])],)
                    self.DB.set_words(MB[f'UG{ug.id}_MANCAL_GUIA_TMP'],[round(self.dict['UG'][f'temperatura_ug{ug.id}_mancal_guia'])],)
                    self.DB.set_words(MB[f'UG{ug.id}_MANCAL_GUIA_INTE_1_TMP'],[round(self.dict['UG'][f'temperatura_ug{ug.id}_mancal_guia_interno_1'])],)
                    self.DB.set_words(MB[f'UG{ug.id}_MANCAL_GUIA_INTE_2_TMP'],[round(self.dict['UG'][f'temperatura_ug{ug.id}_mancal_guia_interno_2'])],)
                    self.DB.set_words(MB[f'UG{ug.id}_MANCAL_COMB_PATINS_1_TMP'],[round(self.dict['UG'][f'temperatura_ug{ug.id}_patins_mancal_comb_1'])],)
                    self.DB.set_words(MB[f'UG{ug.id}_MANCAL_COMB_PATINS_2_TMP'],[round(self.dict['UG'][f'temperatura_ug{ug.id}_patins_mancal_comb_2'])],)
                    self.DB.set_words(MB[f'UG{ug.id}_MANCAL_CASQ_COMB_TMP'],[round(self.dict['UG'][f'temperatura_ug{ug.id}_mancal_casq_comb'])],)
                    self.DB.set_words(MB[f'UG{ug.id}_MANCAL_CONT_ESCO_COMB_TMP'],[round(self.dict['UG'][f'temperatura_ug{ug.id}_mancal_contra_esc_comb'])],)
                    self.DB.set_words(MB[f'UG{ug.id}_ENTRADA_TURBINA_PRESSAO'],[round(10 * self.dict['UG'][f'pressao_turbina_ug{ug.id}'])],)

                # SE
                self.dict['USN']['potencia_kw_se'] = sum([ug.potencia for ug in self.ugs]) * 0.995 + np.random.normal(0, 0.001 * self.escala_ruido)

                # MEDIDORES
                self.dict['USN']['potencia_kw_mp'] = (np.random.normal(self.dict['USN']['potencia_kw_se'] * 0.98,10 * self.escala_ruido,)- 20)
                self.dict['USN']['potencia_kw_mr'] = (np.random.normal(self.dict['USN']['potencia_kw_se'] * 0.98,10 * self.escala_ruido,)- 20)

                # RESERVATORIO
                self.dict['USN']['q_liquida'] = 0
                self.dict['USN']['q_liquida'] += self.dict['USN']['q_alfuente']
                self.dict['USN']['q_liquida'] -= self.dict['USN']['q_sanitaria']
                self.dict['USN']['q_sanitaria'] = self.q_sanitaria(self.dict['USN']['nv_montante'])
                self.dict['USN']['q_vertimento'] = 0



                for ug in self.ugs:
                    self.dict['USN']['q_liquida'] -= self.dict['UG'][f'q_ug{ug.id}']

                self.dict['USN']['nv_montante'] = self.volume_para_nv_montate(volume + self.dict['USN']['q_liquida'] * self.segundos_por_passo)
                self.dict['USN']['nv_jusante_grade'] = self.dict['USN']['nv_montante'] - max(0, np.random.normal(0.1, 0.1 * self.escala_ruido))

                # Cálculo de enchimento do reservatório
                if self.dict['USN']['nv_montante'] >= USINA_NV_VERTEDOURO:
                    self.dict['USN']['q_vertimento'] = self.dict['USN']['q_liquida']
                    self.dict['USN']['q_liquida'] = 0
                    self.dict['USN']['nv_montante'] = (
                        0.0000021411 * self.dict['USN']['q_vertimento'] ** 3
                        - 0.00025189 * self.dict['USN']['q_vertimento'] ** 2
                        + 0.014859 * self.dict['USN']['q_vertimento']
                        + 462.37
                    )

                volume += self.dict['USN']['q_liquida'] * self.segundos_por_passo


                # Escrita de registradores USINA
                self.DB.set_words(MB['NV_MONTANTE'],[round((self.dict['USN']['nv_montante']) * 10000)])
                self.DB.set_words(MB['NV_JUSANTE_CP1'],[round((self.dict['USN']['nv_jusante_grade']) * 10000)])
                self.DB.set_words(MB['NV_JUSANTE_CP2'],[round((self.dict['USN']['nv_jusante_grade']) * 10000)])
                self.DB.set_words(MB['LT_P'],[round(self.dict['USN']['potencia_kw_se'])])
                self.DB.set_words(MB['LT_VAB'],[round(self.dict['USN']['tensao_na_linha'] / 1000)])
                self.DB.set_words(MB['LT_VBC'],[round(self.dict['USN']['tensao_na_linha'] / 1000)])
                self.DB.set_words(MB['LT_VCA'],[round(self.dict['USN']['tensao_na_linha'] / 1000)])
                self.DB.set_words(MB['USN_POTENCIA_KW_MP'], [round(max(0, self.dict['USN']['potencia_kw_mp']))])
                self.DB.set_words(MB['USN_POTENCIA_KW_MR'], [round(max(0, self.dict['USN']['potencia_kw_mr']))])

                # FIM COMPORTAMENTO USINA
                lock.release()
                tempo_restante = (self.passo_simulacao - (datetime.now() - t_inicio_passo).seconds)
                if tempo_restante > 0:
                    sleep(tempo_restante)
                else:
                    logger.warning('A simulação está demorando mais do que o permitido.')

            except KeyboardInterrupt:
                self.server_MB.stop()
                self.dict['GLB']['stop_gui'] = True
                continue

    # Métodos com cálculos de propriedades da USINA
    def volume_para_nv_montate(self, volume):
        return min(max(460, 460 + volume / 40000), 462.37)

    def nv_montate_para_volume(self, nv_montante):
        return 40000 * (min(max(460, nv_montante), 462.37) - 460)

    def q_sanitaria(self, nv_montante):
        if  self.ugs[0].etapa_atual != 1:
            return 0
        elif self.ugs[1].etapa_atual != 1:
            return 0
        else:
            return 2.33