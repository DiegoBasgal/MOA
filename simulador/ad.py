import numpy as np

from time import time
from threading import Thread
from pyModbusTCP.server import DataBank as DB

from dicts.reg import *
from dicts.const import *
from funcs.escrita import Escrita as ESC
from funcs.temporizador import Temporizador


class Ad:
    def __init__(self, dict_comp: 'dict'=None, tempo: 'Temporizador'=None) -> 'None':

        self.dict = dict_comp

        self.escala_ruido = tempo.escala_ruido
        self.passo_simulacao = tempo.passo_simulacao
        self.segundos_por_passo = tempo.segundos_por_passo


    def passo(self) -> 'None':
        return