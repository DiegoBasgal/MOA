import sys
import traceback

import planta as p

import gui.gui as gui

from threading import Thread

from dicts.dict import compartilhado
from funcs.controlador import Controlador
from funcs.temporizador import Temporizador


if __name__ == '__main__':

    print("Iniciando Simulação...")

    try:
        print("Iniciando Classe controladora de Tempo da Simulação...")

        tempo = Temporizador()

    except Exception:
        print(f"Houve um erro ao iniciar a Classe controladora de Tempo.")
        print(traceback.format_exc())

    try:
        print("Iniciando Execução...")

        thread_temporizador = Thread(target = tempo.run, args=())
        thread_usina = Thread(target = p.Planta(compartilhado, tempo).run, args=())
        thread_gui = Thread(target = gui.start_gui, args=(compartilhado,))
        # thread_controlador = Thread(target=Controlador(compartilhado).run, args=())

        print("Rodando Simulador...")
        thread_temporizador.start()
        thread_usina.start()
        thread_gui.start()
        # thread_controlador.start()

        thread_temporizador.join()
        thread_usina.join()
        thread_gui.join()
        # thread_controlador.join()

        print("Fim da Simulação.")

        sys.exit(0)

    except Exception or KeyboardInterrupt:
        sys.exit(1)
        print(f"Houve um erro ao iniciar as Threads de excução do Simulador.")
        print(traceback.format_exc())
