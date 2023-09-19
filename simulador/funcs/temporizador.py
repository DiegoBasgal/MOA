import pytz

from datetime import datetime


class Temporizador:
    def __init__(self, dict_comp: "dict", velocidade: "int"=1, escala_ruido: "float"=0.1, passo: "float"=1) -> "None":

        self.dict = dict_comp

        self.velocidade = velocidade
        self.passo_simulacao = passo
        self.escala_ruido = escala_ruido
        self.segundos_por_passo = self.passo_simulacao * self.velocidade


    def get_time(self) -> "datetime":
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    def run(self) -> "None":
        while not self.dict["GLB"]["stop_sim"]:
            try:
                self.t_inicio = self.get_time()
                self.dict["GLB"]["tempo_simul"] += self.segundos_por_passo

            except KeyboardInterrupt:
                self.dict["GLB"]["stop_sim"] = True
                break
        return
