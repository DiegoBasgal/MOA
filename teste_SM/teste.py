import sys
from random import random
from time import sleep
from sm import State, StateMachine, HaltState


class EstadoA(State):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.paredes_restantes = args[0]
        self.nome_do_estado = "ESTADO-AMADORES"
        print("Temos que pintar {} paredes.".format(self.paredes_restantes))

    def run(self):

        if self.paredes_restantes <= 0:
            print("Tudo pintado.")
            return HaltState()

        n = random()
        if n > 0.2:
            n = random()
            if n > 0.8:
                self.paredes_restantes = max(0, self.paredes_restantes - 1)
                print("Pintamos 1, faltam {}".format(self.paredes_restantes))
            return self
        else:
            print("Vamos chamar o pintor.")
            return EstadoB(self.paredes_restantes)


class EstadoB(State):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.paredes_restantes = args[0]
        self.nome_do_estado = "ESTADO-PINTOR"
        print("O pintor entrou na casa")

    def run(self):
        self.paredes_restantes = max(0, self.paredes_restantes - 1)
        print("O pitnor terminou 1 parede, faltam {}".format(self.paredes_restantes))

        if self.paredes_restantes == 0:
            return EstadoA(self.paredes_restantes)

        n = random()
        if n < 0.8:
            return self
        else:
            print("O pintor vai sair da casa")
            return EstadoA(self.paredes_restantes)


sm = StateMachine(EstadoA(10))
while True:
    print("Rodando a sm. Estado = {}".format(sm.state.nome_do_estado))
    sm.run()
