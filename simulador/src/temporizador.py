from simulador.main import *

logger = logging.getLogger("__main__")

class Temporizador:
    def __init__(self, shared_dict) -> None:

        self.dict = shared_dict

        self.velocidade = 50
        self.escala_ruido = 0.1
        self.passo_simulacao = 0.001
        self.segundos_por_passo = self.passo_simulacao * self.velocidade

    def get_time(self) -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def run(self) -> None:
        while not self.dict["GLB"]["stop_sim"]:
            try:
                self.t_inicio = self.get_time()
                self.dict["GLB"]["tempo_simul"] += self.segundos_por_passo

            except KeyboardInterrupt:
                self.dict["GLB"]["stop_sim"] = True
                break
        return
