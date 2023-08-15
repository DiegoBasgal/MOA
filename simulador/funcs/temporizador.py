import pytz

from datetime import datetime

from dicts.dict import compartilhado

class Temporizador:
    def __init__(self) -> "None":
        self.dict = compartilhado

        self.speed = 50
        self.escala_ruido = 0.1
        self.passo_simulacao = 0.001
        self.segundos_por_passo = self.passo_simulacao * self.speed


    def get_time(self) -> "datetime":
        return datetime.now(pytz.timezone('Brazil/East')).replace(tzinfo=None)


    def run(self) -> "None":
        while not self.dict['GLB']['stop_sim']:
            try:
                self.t_inicio = self.get_time()
                self.dict['GLB']['tempo_real'] += 20 * 0.00001
                self.dict['GLB']['tempo_simul'] += self.segundos_por_passo

            except KeyboardInterrupt:
                self.dict['GLB']['stop_sim'] = True
                break
