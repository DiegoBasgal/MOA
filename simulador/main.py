import sys
import traceback

import planta as p

import gui.gui as gui

from threading import Thread

from se import Se
from tda import Tda
from bay_c import Bay
from ug import Unidade as UG

from dicts.dict import compartilhado
from funcs.temporizador import Temporizador


if __name__ == '__main__':

    print("Iniciando Simulação...")

    try:
        print("Iniciando Classe controladora de Tempo da Simulação...")

        tempo = Temporizador()

    except Exception:
        print(f"Houve um erro ao iniciar a Classe controladora de Tempo.")
        print(f"Traceback: {traceback.format_exc()}")

    try:
        print("Iniciando Execução...")

        bay = Bay(tempo)
        se = Se(tempo)
        tda = Tda(tempo)

        ug1 = UG(1, tempo)
        ug2 = UG(2, tempo)
        ugs = [ug1, ug2]

        thread_temporizador = Thread(target = tempo.run, args=())
        thread_usina = Thread(target = p.Planta(bay, se, tda, ugs, tempo).run, args=())
        thread_gui = Thread(target = gui.start_gui, args=(compartilhado,))
        # thread_controlador = threading.Thread(target=controlador.Controlador(compartilhado).run, args=())

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
        sys.exit(1)


    except Exception:
        print(f"Houve um erro ao iniciar as Threads de excução do Simulador.")
        print(f"Traceback: {traceback.format_exc()}")
