import math

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

        self.cp1 = self.Cp(1, self.dict, tempo)
        self.cp2 = self.Cp(2, self.dict, tempo)
        self.cps: 'list[Ad.Cp]' = [self.cp1, self.cp2]


    class Cp:
        def __init__(self, id: 'int', dict_comp: 'dict'=None, tempo: 'Temporizador'=None) -> 'None':
            
            self.id = id

            self.dict = dict_comp

            self.escala_ruido = tempo.escala_ruido
            self.passo_simulacao = tempo.passo_simulacao
            self.segundos_por_passo = tempo.segundos_por_passo

            self.setpoint = 0
            self.setpoint_anterior = 0

            self.operando = False


        def passo(self) -> 'None':
            self.setpoint = DB.get_words(MB['AD'][f'CP_0{self.id}_SP_POS'])[0]

            if DB.get_words(MB['AD'][f'CMD_CP_0{self.id}_BUSCAR'])[0]:
                DB.set_words(MB['AD'][f'CMD_CP_0{self.id}_BUSCAR'], [0])

                if not self.dict['AD'][f'cp{self.id}_manual'] and not self.operando:
                    self.operando = True

                    if self.setpoint > self.setpoint_anterior:
                        self.setpoint_anterior = self.setpoint
                        Thread(target=lambda: self.abrir(self.setpoint)).start()

                    elif self.setpoint < self.setpoint_anterior:
                        self.setpoint_anterior = self.setpoint
                        Thread(target=lambda: self.fechar(self.setpoint)).start()

            self.dict['AD'][f'cp{self.id}_q'] = self.calcular_q_cp(self.setpoint)


        def abrir(self, setpoint) -> 'None':
            while self.setpoint < setpoint:
                if self.setpoint > setpoint:
                    break
                self.setpoint += setpoint * self.segundos_por_passo
            self.operando = False


        def fechar(self, setpoint) -> 'None':
            while self.setpoint > setpoint:
                if self.setpoint < setpoint:
                    break
                self.setpoint -= setpoint * self.segundos_por_passo
            self.operando = False


        def calcular_q_cp(self, abertura) -> 'int':
            q = abertura/1000 * ADCP_LARGURA * math.sqrt(2 * 9.80665 * ((self.dict['TDA']['nv_montante'] - ADCP_SOLEIRA) - abertura/1000 / 2))
            return max(0, q)


        def atualizar_modbus(self) -> 'None':
            DB.set_words(MB['AD'][f'CP_0{self.id}_POSICAO'], [round(self.setpoint)])

            if self.dict['AD'][f'cp{self.id}_manual'] and not self.dict['BRD'][f'cp{self.id}ad_manual']:
                ESC.escrever_bit(MB['AD'][f'CP_0{self.id}_ACION_LOCAL'], valor=1)

            elif not self.dict['AD'][f'cp{self.id}_manual'] and self.dict['BRD'][f'cp{self.id}ad_manual']:
                ESC.escrever_bit(MB['AD'][f'CP_0{self.id}_ACION_LOCAL'], valor=0)


    def passo(self) -> 'None':
        for cp in self.cps:
            cp.passo()


    def atualizar_modbus(self) -> 'None':
        for cp in self.cps:
            cp.atualizar_modbus()

        if self.dict['AD']['condic'] and not self.dict['BRD']['ad_condic']:
            ESC.escrever_bit(MB['AD']['Alarme28_00'], valor=1)

        elif not self.dict['AD']['condic'] and self.dict['BRD']['ad_condic']:
            ESC.escrever_bit(MB['AD']['Alarme28_00'], valor=0)