class StateMachine:

    def __init__(self, initial_state):
        self.state = initial_state

    def run(self):
        self.state = self.state.run()


class State:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def run(self) -> object:
        return self


class HaltState(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nome_do_estado = "HALT"

    def run(self):
        while True:
            pass
