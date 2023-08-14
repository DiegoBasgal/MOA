import pytz
import threading
import traceback
import numpy as np

import dicts.dict as dct

from time import sleep
from datetime import datetime
from pyModbusTCP.server import DataBank as DB
from pyModbusTCP.server import ModbusServer

from dicts.reg import *
from dicts.const import *
from funcs.escrita import Escrita as ESC
from funcs.leitura import Leitura as LEI

from se import Se
from tda import Tda
from bay_c import Bay
from ug import Unidade

from funcs.temporizador import Temporizador

lock = threading.Lock()

class Planta:
    def __init__(self, bay: "Bay"=None, se: "Se"=None, tda: "Tda"=None, ugs: "list[Unidade]"=None, temporizador: "Temporizador"=None) -> "None":
        self.dict = dct.compartilhado
        self.tempo = temporizador
        self.se = se
        self.bay = bay
        self.tda = tda
        self.ugs = ugs

        self.escala_ruido = temporizador.escala_ruido
        self.passo_simulacao = temporizador.passo_simulacao
        self.segundos_por_passo = temporizador.segundos_por_passo

        self.volume = 0
        self.b_djse = False
        self.b_djbay = False

        # Incia os servidores
        self.server_MB = ModbusServer(host='0.0.0.0', port=5000, no_block=True)
        self.server_MB.start()

        for n, d in MB.items():
            for l in d.values():
                if isinstance(l, list):
                    DB.set_words(l[0], [0])
                else:
                    DB.set_words(l, [0])

    def run(self) -> "None":

        self.tda.volume = self.tda.calcular_montante_volume(self.dict['TDA']['nv_montante'])
        self.se.abrir_dj()
        self.bay.abrir_dj()

        # Loop principal
        while not self.dict['GLB']['stop_sim']:
            self.dict['GLB']['stop_sim'] = self.dict['GLB']['stop_gui']

            try:
                t_inicio_passo = datetime.now()
                lock.acquire()

                # Acerto temportal
                self.dict['GLB']['tempo_simul'] += self.segundos_por_passo

                self.atualizar_mb_geral()

                if (self.dict['USN']['trip_condic'] and self.dict['USN'][f'aux_borda{1}'] == 0) \
                    or (DB.get_words(MB['GERAL']['USN_CONDICIONADOR'][0])[0] == 1 and self.dict['USN'][f'aux_borda{1}'] == 0):
                    self.dict['USN'][f'aux_borda{1}'] = 1
                    DB.set_words(MB['GERAL']['USN_CONDICIONADOR'][0], [1])

                elif (not self.dict['USN']['trip_condic'] and self.dict['USN'][f'aux_borda{1}'] == 1) \
                    or (DB.get_words(MB['GERAL']['USN_CONDICIONADOR'][0]) == 0 and self.dict['USN'][f'aux_borda{1}'] == 1):
                    self.dict['USN'][f'aux_borda{1}'] = 0
                    self.dict['USN']['trip_condic'] = False
                    DB.set_words(MB['GERAL']['USN_CONDICIONADOR'][0], [0])
                    self.se.resetar_se()

                # Se
                self.bay.passo()
                self.se.passo()
                self.tda.passo()

                # UGs
                for ug in self.ugs:
                    # Leitura do dicionário compartilhado
                    self.dict[f'UG{ug.id}'][f'setpoint'] = DB.get_words(MB[f'UG{ug.id}']['SETPONIT'])[0]

                    if self.dict[f'UG{ug.id}'][f'debug_setpoint'] >= 0:
                        self.dict[f'UG{ug.id}'][f'setpoint'] = self.dict[f'UG{ug.id}'][f'debug_setpoint']
                        DB.set_words(MB[f'UG{ug.id}']['SETPONIT'], [self.dict[f'UG{ug.id}']['setpoint']])
                        self.dict[f'UG{ug.id}'][f'debug_setpoint'] = -1

                    # Leitura de registradores MB
                    if LEI.ler_bit(MB[f'UG{ug.id}']['PARTIDA_CMD_SINCRONISMO']):
                        ESC.escrever_bit(MB[f'UG{ug.id}']['PARTIDA_CMD_SINCRONISMO'], valor=0)
                        ug.partir()

                    elif LEI.ler_bit(MB[f'UG{ug.id}']['PARADA_CMD_DESABILITA_UHLM']):
                        ESC.escrever_bit(MB[f'UG{ug.id}']['PARADA_CMD_DESABILITA_UHLM'], valor=0)
                        ug.parar()

                    if LEI.ler_bit(MB['TDA'][f'CP{ug.id}_CMD_FECHAMENTO']) and not self.dict['TDA'][f'cp{ug.id}_borda_f']:
                        ESC.escrever_bit(MB['TDA'][f'CP{ug.id}_CMD_FECHAMENTO'], valor=0)
                        self.dict['TDA'][f'cp{ug.id}_borda_f'] = True
                        self.dict['TDA'][f'cp{ug.id}_thread_fechada'] = True

                    elif not LEI.ler_bit(MB['TDA'][f'CP{ug.id}_CMD_FECHAMENTO']) and self.dict['TDA'][f'cp{ug.id}_borda_f']:
                        self.dict['TDA'][f'cp{ug.id}_borda_f'] = False

                    if LEI.ler_bit(MB['TDA'][f'CP{ug.id}_CMD_ABERTURA_TOTAL']) and not self.dict['TDA'][f'cp{ug.id}_borda_a']:
                        ESC.escrever_bit(MB['TDA'][f'CP{ug.id}_CMD_ABERTURA_TOTAL'], valor=0)
                        self.dict['TDA'][f'cp{ug.id}_borda_a'] = True
                        self.dict['TDA'][f'cp{ug.id}_thread_aberta'] = True

                    elif not LEI.ler_bit(MB['TDA'][f'CP{ug.id}_CMD_ABERTURA_TOTAL']) and self.dict['TDA'][f'cp{ug.id}_borda_a']:
                        self.dict['TDA'][f'cp{ug.id}_borda_a'] = False

                    if LEI.ler_bit(MB['TDA'][f'CP{ug.id}_CMD_ABERTURA_CRACKING']) and not self.dict['TDA'][f'cp{ug.id}_borda_c']:
                        ESC.escrever_bit(MB['TDA'][f'CP{ug.id}_CMD_ABERTURA_CRACKING'], valor=0)
                        self.dict['TDA'][f'cp{ug.id}_borda_c'] = True
                        self.dict['TDA'][f'cp{ug.id}_thread_cracking'] = True

                    elif not LEI.ler_bit(MB['TDA'][f'CP{ug.id}_CMD_ABERTURA_CRACKING']) and self.dict['TDA'][f'cp{ug.id}_borda_c']:
                        self.dict['TDA'][f'cp{ug.id}_borda_c'] = False

                    ug.passo()

                    if self.dict["TDA"][f"cp{ug.id}_operando"] and not self.dict['TDA'][f'cp{ug.id}_borda_o']:
                        self.dict['TDA'][f'cp{ug.id}_borda_o'] = True
                        ESC.escrever_bit(MB["TDA"][f"CP{ug.id}_OPERANDO"], valor=1)

                    elif not self.dict["TDA"][f"cp{ug.id}_operando"] and self.dict['TDA'][f'cp{ug.id}_borda_o']:
                        self.dict['TDA'][f'cp{ug.id}_borda_o'] = False
                        ESC.escrever_bit(MB["TDA"][f"CP{ug.id}_OPERANDO"], valor=0)

                    DB.set_words(MB[f'UG{ug.id}']['RV_ESTADO_OPERACAO'], [int(ug.etapa_atual)])
                    DB.set_words(MB[f'UG{ug.id}']['RV_ESTADO_OPERACAO_2'], [0 if ug.etapa_alvo == None else int(ug.etapa_alvo)])
                    DB.set_words(MB[f'UG{ug.id}']['P'], [round(ug.potencia)])
                    DB.set_words(MB[f'UG{ug.id}']['HORIMETRO'], [np.floor(ug.horimetro_hora)])
                    DB.set_words(MB[f'UG{ug.id}']['GERADOR_FASE_A_TMP'], [round(ug.dict[f'UG{ug.id}'][f'temp_fase_r'])])
                    DB.set_words(MB[f'UG{ug.id}']['GERADOR_FASE_B_TMP'], [round(ug.dict[f'UG{ug.id}'][f'temp_fase_s'])])
                    DB.set_words(MB[f'UG{ug.id}']['GERADOR_FASE_C_TMP'], [round(ug.dict[f'UG{ug.id}'][f'temp_fase_t'])])
                    DB.set_words(MB[f'UG{ug.id}']['GERADOR_NUCL_ESTAT_TMP'], [round(ug.dict[f'UG{ug.id}'][f'temp_nucleo_gerador_1'])])
                    DB.set_words(MB[f'UG{ug.id}']['MANCAL_GUIA_TMP'], [round(ug.dict[f'UG{ug.id}'][f'temp_mancal_guia'])])
                    DB.set_words(MB[f'UG{ug.id}']['MANCAL_GUIA_INTE_1_TMP'], [round(ug.dict[f'UG{ug.id}'][f'temp_mancal_guia_interno_1'])])
                    DB.set_words(MB[f'UG{ug.id}']['MANCAL_GUIA_INTE_2_TMP'], [round(ug.dict[f'UG{ug.id}'][f'temp_mancal_guia_interno_2'])])
                    DB.set_words(MB[f'UG{ug.id}']['MANCAL_COMB_PATINS_1_TMP'], [round(ug.dict[f'UG{ug.id}'][f'temp_patins_mancal_comb_1'])])
                    DB.set_words(MB[f'UG{ug.id}']['MANCAL_COMB_PATINS_2_TMP'], [round(ug.dict[f'UG{ug.id}'][f'temp_patins_mancal_comb_2'])])
                    DB.set_words(MB[f'UG{ug.id}']['MANCAL_CASQ_COMB_TMP'], [round(ug.dict[f'UG{ug.id}'][f'temp_mancal_casq_comb'])])
                    DB.set_words(MB[f'UG{ug.id}']['MANCAL_CONT_ESCO_COMB_TMP'], [round(ug.dict[f'UG{ug.id}'][f'temp_mancal_contra_esc_comb'])])
                    DB.set_words(MB[f'UG{ug.id}']['ENTRADA_TURBINA_PRESSAO'], [round(10 * ug.dict[f'UG{ug.id}'][f'pressao_turbina'])])

                self.dict['SE']['potencia_se'] = sum([ug.potencia for ug in self.ugs]) * 0.995 + np.random.normal(0, 0.001 * self.escala_ruido)

                self.bay.atualizar_mp_mr()

                DB.set_words(MB['TDA']['NV_MONTANTE'], [self.dict['TDA']['nv_montante'] * 100],)
                DB.set_words(MB['TDA']['NV_JUSANTE_CP1'], [round((self.dict['TDA']['nv_jusante_grade']) * 10000)],)
                DB.set_words(MB['TDA']['NV_JUSANTE_CP2'], [round((self.dict['TDA']['nv_jusante_grade']) * 10000)],)

                DB.set_words(MB['BAY']['LT_VAB'], [round(self.dict['BAY']['tensao_linha'] / 1000)])
                DB.set_words(MB['BAY']['LT_VBC'], [round(self.dict['BAY']['tensao_linha'] / 1000)])
                DB.set_words(MB['BAY']['LT_VCA'], [round(self.dict['BAY']['tensao_linha'] / 1000)])

                DB.set_words(MB['SE']['LT_P'], [round(self.dict['SE']['potencia_se'])])
                DB.set_words(MB['SE']['LT_VAB'], [round(self.dict['SE']['tensao_linha'] / 1000)])
                DB.set_words(MB['SE']['LT_VBC'], [round(self.dict['SE']['tensao_linha'] / 1000)])
                DB.set_words(MB['SE']['LT_VCA'], [round(self.dict['SE']['tensao_linha'] / 1000)])

                self.atualizar_mb_geral()

                # FIM COMPORTAMENTO USINA
                lock.release()
                tempo_restante = (self.passo_simulacao - (datetime.now() - t_inicio_passo).seconds)

                if tempo_restante > 0:
                    sleep(tempo_restante)
                else:
                    print('A Simulação está demorando mais do que o permitido!')

            except KeyboardInterrupt:
                self.server_MB.stop()
                self.dict['GLB']['stop_gui'] = True
                continue

    def atualizar_mb_geral(self) -> "None":
        self.se.atualizar_modbus()
        self.bay.atualizar_modbus()
        self.tda.atualizar_modbus()