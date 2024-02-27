import threading

from time import sleep
from datetime import datetime
from pyModbusTCP.server import ModbusServer
from pyModbusTCP.server import DataBank as DB

from dicts.reg import *

from se import Se
from tda import Tda
from ug import Unidade
from funcs.temporizador import Temporizador

lock = threading.Lock()

class Planta:
    def __init__(self, dict_comp: 'dict'=None, tempo: 'Temporizador'=None) -> 'None':

        self.dict = dict_comp

        self.se = Se(dict_comp, tempo)
        self.tda = Tda(dict_comp, tempo)
        self.ug1 = Unidade(1, dict_comp, tempo)
        self.ug2 = Unidade(2, dict_comp, tempo)

        self.ugs = [self.ug1, self.ug2]

        self.escala_ruido = tempo.escala_ruido
        self.passo_simulacao = tempo.passo_simulacao
        self.segundos_por_passo = tempo.segundos_por_passo

        self.server_MB = ModbusServer(host='0.0.0.0', port=502, no_block=True)
        self.server_MB.start()

        for v in REG_SASE.values():
            DB.set_words(v[0], [0]) if isinstance(v, list) else DB.set_words(v, [0])

        for v in REG_TDA.values():
            DB.set_words(v[0], [0]) if isinstance(v, list) else DB.set_words(v, [0])

        for n in REG_RTV.values():
            for v in n.values():
                DB.set_words(v[0], [0]) if isinstance(v, list) else DB.set_words(v, [0])

        for n in REG_UG.values():
            for v in n.values():
                DB.set_words(v[0], [0]) if isinstance(v, list) else DB.set_words(v, [0])


    def atualizar_modbus_geral(self) -> 'None':
        self.se.atualizar_modbus()
        self.tda.atualizar_modbus()
        self.ug1.atualizar_modbus()
        self.ug2.atualizar_modbus()


    def run(self) -> 'None':

        self.se.abrir_dj()

        while not self.dict['GLB']['stop_sim']:
            self.dict['GLB']['stop_sim'] = self.dict['GLB']['stop_gui']

            try:
                t_inicio = datetime.now()
                lock.acquire()
                self.dict['GLB']['tempo_simul'] += self.segundos_por_passo

                self.se.passo()
                self.tda.passo()
                self.ug1.passo()
                self.ug2.passo()

                self.atualizar_modbus_geral()

                lock.release()
                tempo_restante = (self.passo_simulacao - (datetime.now() - t_inicio).seconds)
                sleep(tempo_restante) if tempo_restante > 0 else print('A Simulação está demorando mais do que o permitido!')

            except KeyboardInterrupt:
                self.server_MB.stop()
                self.dict['GLB']['stop_gui'] = True
                return