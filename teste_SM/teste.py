import sys
from random import random
from time import sleep


class StateMachine:

    def __init__(self, initial_state):
        self.state = initial_state

    def run(self):
        self.state = self.state.run()


class State:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.nome_do_estado = "Estado Genérico"
    def run(self) -> object:
        return self


class EstadoA(State):

    def __init__(self, *args, **kargs):
        self.paredes_restantes = args[0]
        self.nome_do_estado = "ESTADO-AMADORES"
        print("Temos que pintar {} paredes.".format(self.paredes_restantes))

    def run(self):

        if self.paredes_restantes <= 0:
            print("Tudo pintado.")
            return HaltSM()

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


class HaltSM(State):

    def __init__(self):
        self.nome_do_estado = "HALT"

    def run(self):
        while True:
            sleep(1)


sm = StateMachine(initial_state=EstadoA(10))
while True:
    print("Rodando a sm. Estado = {}".format(sm.state.nome_do_estado))
    sm.run()
