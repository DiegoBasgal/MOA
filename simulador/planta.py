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

                self.dict['GLB']['tempo_simul'] += self.segundos_por_passo

                self.bay.passo()
                self.se.passo()
                self.tda.passo()

                # UGs
                for ug in self.ugs:
                    # Leitura do dicionário compartilhado
                    self.dict[f'UG{ug.id}'][f'setpoint'] = DB.get_words(MB[f'UG{ug.id}']['SETPONIT'])[0]

                    ug.passo()

                self.dict['SE']['potencia_se'] = sum([ug.potencia for ug in self.ugs]) * 0.995 + np.random.normal(0, 0.001 * self.escala_ruido)

                self.atualizar_mb_geral()

                if self.dict['USN']['trip_condic'] and not self.dict['BRD']['condic']:
                    self.dict['BRD']['condic'] = True
                    DB.set_words(MB['GERAL']['USN_CONDICIONADOR'][0], [1])

                elif not self.dict['USN']['trip_condic'] and self.dict['BRD'][f'condic']:
                    self.dict['BRD'][f'condic'] = False
                    DB.set_words(MB['GERAL']['USN_CONDICIONADOR'][0], [0])

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