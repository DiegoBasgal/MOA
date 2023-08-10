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

        # Incia os servidores
        self.server_MB = ModbusServer(host='localhost', port=5002, no_block=True)
        self.server_MB.start()

        for n, l in MB.items():
            if isinstance(l, list):
                ESC.escrever_bit(l, valor=0)
            else:
                DB.set_words(l, [0])

    def run(self) -> "None":

        self.tda.volume = self.tda.calcular_montante_volume(self.dict['TDA']['nv_montante'])
        self.se.abrir_dj()

        # Loop principal
        while not self.dict['GLB']['stop_sim']:
            self.dict['GLB']['stop_sim'] = self.dict['GLB']['stop_gui']

            try:
                t_inicio_passo = datetime.now()
                lock.acquire()

                # Acerto temportal
                self.dict['GLB']['tempo_simul'] += self.segundos_por_passo

                # Leituras de registradores MB
                if LEI.ler_bit(MB['DJL_CMD_FECHAR']) == 1:
                    ESC.escrever_bit(MB['DJL_CMD_FECHAR'], valor=0)
                    print('[CF]  Comando de Fechamento do Disjuntor da Subestação acionado via \"MODBUS\"')
                    self.se.fechar_dj()

                if LEI.ler_bit(MB['BARRA_CA_RST_FLH']) == 1:
                    ESC.escrever_bit(MB['BARRA_CA_RST_FLH'], valor=0)
                    print('[CF]  Comando de Reset de Falhas na Barra CA acionado via \"MODBUS\"')
                    self.se.resetar_se()

                if (self.dict['USN']['trip_condic'] and self.dict['USN'][f'aux_borda{1}'] == 0) \
                    or (DB.get_words(MB['USN_CONDICIONADOR'][0])[0] == 1 and self.dict['USN'][f'aux_borda{1}'] == 0):
                    self.dict['USN'][f'aux_borda{1}'] = 1
                    DB.set_words(MB['USN_CONDICIONADOR'][0], [1])

                elif (not self.dict['USN']['trip_condic'] and self.dict['USN'][f'aux_borda{1}'] == 1) \
                    or (DB.get_words(MB['USN_CONDICIONADOR'][0]) == 0 and self.dict['USN'][f'aux_borda{1}'] == 1):
                    self.dict['USN'][f'aux_borda{1}'] = 0
                    self.dict['USN']['trip_condic'] = False
                    DB.set_words(MB['USN_CONDICIONADOR'][0], [0])
                    self.se.resetar_se()

                # Se
                self.bay.passo()
                self.se.passo()

                # UGs
                for ug in self.ugs:
                    # Leitura do dicionário compartilhado
                    self.dict[f'UG{ug.id}'][f'setpoint'] = DB.get_words(MB[f'UG{ug.id}_SETPONIT'])[0]

                    if self.dict[f'UG{ug.id}'][f'debug_setpoint'] >= 0:
                        self.dict[f'UG{ug.id}'][f'setpoint'] = self.dict[f'UG{ug.id}'][f'debug_setpoint']
                        DB.set_words(MB[f'UG{ug.id}_SETPONIT'], [self.dict[f'UG{ug.id}'][f'setpoint']])

                    if self.dict['TDA'][f'cp{ug.id}_permissao_abertura'] and self.dict['USN'][f'aux_borda{ug.id + 4}'] == 0:
                        ESC.escrever_bit(MB[f'CP{ug.id}_PERMISSIVOS_OK'], valor=1)
                        self.dict['USN'][f'aux_borda{ug.id + 4}'] = 1

                    elif not self.dict['TDA'][f'cp{ug.id}_permissao_abertura'] and self.dict['USN'][f'aux_borda{ug.id + 4}'] == 1:
                        ESC.escrever_bit(MB[f'CP{ug.id}_PERMISSIVOS_OK'], valor=0)
                        self.dict['USN'][f'aux_borda{ug.id + 4}'] = 0

                    # Leitura de registradores MB
                    if LEI.ler_bit(MB[f'UG{ug.id}_PARTIDA_CMD_SINCRONISMO']) == 1:
                        ESC.escrever_bit(MB[f'UG{ug.id}_PARTIDA_CMD_SINCRONISMO'], valor=0)
                        ug.partir()

                    elif LEI.ler_bit(MB[f'UG{ug.id}_PARADA_CMD_DESABILITA_UHLM']) == 1:
                        ESC.escrever_bit(MB[f'UG{ug.id}_PARADA_CMD_DESABILITA_UHLM'], valor=0)
                        ug.parar()

                    if LEI.ler_bit(MB[f'CP{ug.id}_CMD_FECHAMENTO']) == 1 and self.dict['TDA'][f'cp{ug.id}_borda_f'] == 0:
                        ESC.escrever_bit(MB[f'CP{ug.id}_CMD_FECHAMENTO'], valor=0)
                        ESC.escrever_bit(MB[f'CP{ug.id}_OPERANDO'], valor=1)
                        self.dict['TDA'][f'cp{ug.id}_borda_f'] = 1
                        self.dict['TDA'][f'cp{ug.id}_thread_fechada'] = True

                        if self.dict['TDA'][f'cp{ug.id}_fechada']:
                            ESC.escrever_bit(MB[f'CP{ug.id}_OPERANDO'], valor=0)

                    elif LEI.ler_bit(MB[f'CP{ug.id}_CMD_FECHAMENTO']) == 0 and self.dict['TDA'][f'cp{ug.id}_borda_f'] == 1:
                        self.dict['TDA'][f'cp{ug.id}_borda_f'] = 0

                    if LEI.ler_bit(MB[f'CP{ug.id}_CMD_ABERTURA_TOTAL']) == 1 and self.dict['TDA'][f'cp{ug.id}_borda_a'] == 0:
                        ESC.escrever_bit(MB[f'CP{ug.id}_CMD_ABERTURA_TOTAL'], valor=0)
                        ESC.escrever_bit(MB[f'CP{ug.id}_OPERANDO'], valor=1)
                        self.dict['TDA'][f'cp{ug.id}_borda_a'] = 1
                        self.dict['TDA'][f'cp{ug.id}_thread_aberta'] = True

                        if self.dict['TDA'][f'cp{ug.id}_aberta']:
                            ESC.escrever_bit(MB[f'CP{ug.id}_OPERANDO'], valor=0)

                    elif LEI.ler_bit(MB[f'CP{ug.id}_CMD_ABERTURA_TOTAL']) == 0 and self.dict['TDA'][f'cp{ug.id}_borda_a'] == 1:
                        self.dict['TDA'][f'cp{ug.id}_borda_a'] = 0

                    if LEI.ler_bit(MB[f'CP{ug.id}_CMD_ABERTURA_CRACKING']) == 1 and self.dict['TDA'][f'cp{ug.id}_borda_c'] == 0:
                        ESC.escrever_bit(MB[f'CP{ug.id}_CMD_ABERTURA_CRACKING'], valor=0)
                        ESC.escrever_bit(MB[f'CP{ug.id}_OPERANDO'], valor=1)
                        self.dict['TDA'][f'cp{ug.id}_borda_c'] = 1
                        self.dict['TDA'][f'cp{ug.id}_thread_cracking'] = True

                        if self.dict['TDA'][f'cp{ug.id}_cracking']:
                            ESC.escrever_bit(MB[f'CP{ug.id}_OPERANDO'], valor=0)

                    elif LEI.ler_bit(MB[f'CP{ug.id}_CMD_ABERTURA_CRACKING']) == 0 and self.dict['TDA'][f'cp{ug.id}_borda_c'] == 1:
                        self.dict['TDA'][f'cp{ug.id}_borda_c'] = 0

                for ug in self.ugs:
                    ug.passo()

                self.dict['SE']['potencia_se'] = sum([ug.potencia for ug in self.ugs]) * 0.995 + np.random.normal(0, 0.001 * self.escala_ruido)

                self.bay.atualizar_mp_mr()

                self.tda.passo()

                self.bay.atualizar_modbus()

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