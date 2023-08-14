import numpy as np
from tkinter import E

from threading import Thread

from time import time
from pyModbusTCP.server import DataBank as DB

from funcs.escrita import Escrita as ESC
from funcs.temporizador import Temporizador

from dicts.reg import *
from dicts.const import *
from dicts.dict import compartilhado

class Tda:
    def __init__(self, tempo: Temporizador) -> "None":
        self.dict = compartilhado

        self.volume = 0

        self.escala_ruido = tempo.escala_ruido
        self.passo_simulacao = tempo.passo_simulacao
        self.segundos_por_passo = tempo.segundos_por_passo

        self.b_uh = False
        self.b_lg = True
        self.b_vb = False

        self.b_vb_calc = False

        self.b_cp1_fechada = False
        self.b_cp2_fechada = False

        self.b_cp1_aberta = False
        self.b_cp2_aberta = False

        self.b_cp1_cracking = False
        self.b_cp2_cracking = False

        self.b_cp1_pressao = False
        self.b_cp2_pressao = False

        self.b_cp1_permissao = False
        self.b_cp2_permissao = False

        self.b_cp1_bloqueio = False
        self.b_cp2_bloqueio = False

        self.b_cp1_aguardando_a = False
        self.b_cp2_aguardando_a = False

    def passo(self) -> "None":
        self.calcular_vazao()
        self.calcular_enchimento_reservatorio()

    def calcular_volume_montante(self, volume) -> "float":
        return min(max(460, 460 + volume / 40000), 462.37)

    def calcular_montante_volume(self, nv_montante) -> "float":
        return 40000 * (min(max(460, nv_montante), 462.37) - 460)

    def calcular_q_sanitaria(self, nv_montante) -> "float":
        if self.dict['UG1']['etapa_atual'] in (ETAPA_UP, None) and self.dict['UG2']['etapa_atual'] in (ETAPA_UP, None):
            if self.b_vb_calc:
                self.b_vb_calc = False
                Thread(target=lambda: self.operar_vb()).start()
                return 2.33
            else:
                return 2.33
        else:
            if not self.b_vb_calc:
                self.b_vb_calc = True
                Thread(target=lambda: self.operar_vb()).start()
                return 0
            else:
                return 0

    def operar_vb(self) -> "None":
        print('[TDA] Operando Válvula Borboleta de Vazão Sanitária')
        delay = time() + 5
        while time() <= delay:
            self.dict["TDA"]["vb_operando"] = True

        self.dict["TDA"]["vb_operando"] = False
        print('[TDA] Operação Válvula Borboleta Finalizada')

    def calcular_vazao(self) -> "None":
        self.dict['TDA']['q_liquida'] = 0
        self.dict['TDA']['q_liquida'] += self.dict['TDA']['q_alfuente']
        self.dict['TDA']['q_liquida'] -= self.dict['TDA']['q_sanitaria']
        self.dict['TDA']['q_sanitaria'] = self.calcular_q_sanitaria(self.dict['TDA']['nv_montante'])
        self.dict['TDA']['q_vertimento'] = 0

        ug = 0
        for _ in range(2):
            ug += 1
            self.dict['TDA']['q_liquida'] -= self.dict[f'UG{ug}'][f'q']

    def calcular_enchimento_reservatorio(self) -> "None":
        self.dict['TDA']['nv_montante'] = self.calcular_volume_montante(self.volume + self.dict['TDA']['q_liquida'] * self.segundos_por_passo)
        self.dict['TDA']['nv_jusante_grade'] = self.dict['TDA']['nv_montante'] - max(0, np.random.normal(0.1, 0.1 * self.escala_ruido))

        if self.dict['TDA']['nv_montante'] >= USINA_NV_VERTEDOURO:
            self.dict['TDA']['q_vertimento'] = self.dict['TDA']['q_liquida']
            self.dict['TDA']['q_liquida'] = 0
            self.dict['TDA']['nv_montante'] = (
                0.0000021411 * self.dict['TDA']['q_vertimento'] ** 3
                - 0.00025189 * self.dict['TDA']['q_vertimento'] ** 2
                + 0.014859 * self.dict['TDA']['q_vertimento']
                + 462.37
            )

        self.volume += self.dict['TDA']['q_liquida'] * self.segundos_por_passo

    def atualizar_modbus(self) -> "None":
        
        # CP1 Permissão
        if self.dict['TDA']['cp1_permissao_abertura'] and not self.b_cp1_permissao:
            self.b_cp1_permissao = True
            ESC.escrever_bit(MB["TDA"][f"CP1_PERMISSIVOS_OK"], valor=0)

        elif not self.dict['TDA']['cp1_permissao_abertura'] and self.b_cp1_permissao:
            self.b_cp1_permissao = False
            ESC.escrever_bit(MB["TDA"][f"CP1_PERMISSIVOS_OK"], valor=1)

        # CP2 Permissão
        if self.dict['TDA']['cp2_permissao_abertura'] and not self.b_cp2_permissao:
            self.b_cp2_permissao = True
            ESC.escrever_bit(MB["TDA"][f"CP2_PERMISSIVOS_OK"], valor=0)

        elif not self.dict['TDA']['cp2_permissao_abertura'] and self.b_cp2_permissao:
            self.b_cp2_permissao = False
            ESC.escrever_bit(MB["TDA"][f"CP2_PERMISSIVOS_OK"], valor=1)
        
        # CP1 Aguardando Abertura
        if self.dict['TDA']['cp1_aguardando_abertura'] and not self.b_cp1_aguardando_a:
            self.b_cp1_aguardando_a = True
            ESC.escrever_bit(MB["TDA"][f"CP1_AGUARDANDO_CMD_ABERTURA"], valor=1)

        elif not self.dict['TDA']['cp1_aguardando_abertura'] and self.b_cp1_aguardando_a:
            self.b_cp1_aguardando_a = False
            ESC.escrever_bit(MB["TDA"][f"CP1_AGUARDANDO_CMD_ABERTURA"], valor=2)

        # CP2 Aguardando Abertura
        if self.dict['TDA']['cp2_aguardando_abertura'] and not self.b_cp2_aguardando_a:
            self.b_cp2_aguardando_a = True
            ESC.escrever_bit(MB["TDA"][f"CP2_AGUARDANDO_CMD_ABERTURA"], valor=1)

        elif not self.dict['TDA']['cp2_aguardando_abertura'] and self.b_cp2_aguardando_a:
            self.b_cp2_aguardando_a = False
            ESC.escrever_bit(MB["TDA"][f"CP2_AGUARDANDO_CMD_ABERTURA"], valor=0)

        # CP1 Bloqueio
        if self.dict['TDA']['cp1_trip'] and not self.b_cp1_bloqueio:
            self.b_cp1_bloqueio = True
            ESC.escrever_bit(MB["TDA"][f"CP1_BLQ_ATUADO"], valor=1)

        elif not self.dict['TDA']['cp1_trip'] and self.b_cp1_bloqueio:
            self.b_cp1_bloqueio = False
            ESC.escrever_bit(MB["TDA"][f"CP1_BLQ_ATUADO"], valor=0)

        # CP2 Bloqueio
        if self.dict['TDA']['cp2_trip'] and not self.b_cp2_bloqueio:
            self.b_cp2_bloqueio = True
            ESC.escrever_bit(MB["TDA"][f"CP2_BLQ_ATUADO"], valor=1)

        elif not self.dict['TDA']['cp2_trip'] and self.b_cp2_bloqueio:
            self.b_cp2_bloqueio = False
            ESC.escrever_bit(MB["TDA"][f"CP2_BLQ_ATUADO"], valor=0)

        # CP Fechada
        if self.dict["TDA"]["cp1_fechada"] and not self.b_cp1_fechada:
            self.b_cp1_fechada = True
            ESC.escrever_bit(MB["TDA"]["CP1_FECHADA"], valor=1)

        elif not self.dict["TDA"]["cp1_fechada"] and self.b_cp1_fechada:
            self.b_cp1_fechada = False
            ESC.escrever_bit(MB["TDA"]["CP1_FECHADA"], valor=0)

        if self.dict["TDA"]["cp2_fechada"] and not self.b_cp2_fechada:
            self.b_cp2_fechada = True
            ESC.escrever_bit(MB["TDA"]["CP2_FECHADA"], valor=1)

        elif not self.dict["TDA"]["cp2_fechada"] and self.b_cp2_fechada:
            self.b_cp2_fechada = False
            ESC.escrever_bit(MB["TDA"]["CP2_FECHADA"], valor=0)

        # CP Aberta
        if self.dict["TDA"]["cp1_aberta"] and not self.b_cp1_aberta:
            self.b_cp1_aberta = True
            ESC.escrever_bit(MB["TDA"]["CP1_ABERTA"], valor=1)

        elif not self.dict["TDA"]["cp1_aberta"] and self.b_cp1_aberta:
            self.b_cp1_aberta = False
            ESC.escrever_bit(MB["TDA"]["CP1_ABERTA"], valor=0)

        if self.dict["TDA"]["cp2_aberta"] and not self.b_cp2_aberta:
            self.b_cp2_aberta = True
            ESC.escrever_bit(MB["TDA"]["CP2_ABERTA"], valor=1)

        elif not self.dict["TDA"]["cp2_aberta"] and self.b_cp2_aberta:
            self.b_cp2_aberta = False
            ESC.escrever_bit(MB["TDA"]["CP2_ABERTA"], valor=0)

        # CP Cracking
        if self.dict["TDA"]["cp1_cracking"] and not self.b_cp1_cracking:
            self.b_cp1_cracking = True
            ESC.escrever_bit(MB["TDA"]["CP1_CRACKING"], valor=1)

        elif not self.dict["TDA"]["cp1_cracking"] and self.b_cp1_cracking:
            self.b_cp1_cracking = False
            ESC.escrever_bit(MB["TDA"]["CP1_CRACKING"], valor=0)

        if self.dict["TDA"]["cp2_cracking"] and not self.b_cp2_cracking:
            self.b_cp2_cracking = True
            ESC.escrever_bit(MB["TDA"]["CP2_CRACKING"], valor=1)

        elif not self.dict["TDA"]["cp2_cracking"] and self.b_cp2_cracking:
            self.b_cp2_cracking = False
            ESC.escrever_bit(MB["TDA"]["CP2_CRACKING"], valor=0)
        
        # CP Pressao Equalizada
        if self.dict["TDA"]["cp1_pressao_equalizada"] and not self.b_cp1_pressao:
            self.b_cp1_pressao = True
            ESC.escrever_bit(MB["TDA"]["CP1_PRESSAO_EQUALIZADA"], valor=1)

        elif not self.dict["TDA"]["cp1_pressao_equalizada"] and self.b_cp1_pressao:
            self.b_cp1_pressao = False
            ESC.escrever_bit(MB["TDA"]["CP1_PRESSAO_EQUALIZADA"], valor=0)

        if self.dict["TDA"]["cp2_pressao_equalizada"] and not self.b_cp2_pressao:
            self.b_cp2_pressao = True
            ESC.escrever_bit(MB["TDA"]["CP2_PRESSAO_EQUALIZADA"], valor=1)

        elif not self.dict["TDA"]["cp2_pressao_equalizada"] and self.b_cp2_pressao:
            self.b_cp2_pressao = False
            ESC.escrever_bit(MB["TDA"]["CP2_PRESSAO_EQUALIZADA"], valor=0)


        # Limpa Grades
        if not self.dict["TDA"]["lg_operando"] and self.b_lg:
            self.b_lg = False
            ESC.escrever_bit(MB["TDA"]["LG_OPE_MANUAL"], valor=0)

        elif self.dict["TDA"]["lg_operando"] and not self.b_lg:
            self.b_lg = True
            ESC.escrever_bit(MB["TDA"]["LG_OPE_MANUAL"], valor=1)

        # Válvula Borboleta
        if self.dict["TDA"]["vb_operando"] and not self.b_vb:
            self.b_vb = True
            ESC.escrever_bit(MB["TDA"]["VB_FECHANDO"], valor=1)

        elif not self.dict["TDA"]["vb_operando"] and self.b_vb:
            self.b_vb = False
            ESC.escrever_bit(MB["TDA"]["VB_FECHANDO"], valor=0)

        if self.dict["TDA"]["uh_disponivel"] and not self.b_uh:
            self.b_uh = True
            ESC.escrever_bit(MB["TDA"]["UH_DISPONIVEL"], valor=1)

        elif not self.dict["TDA"]["uh_disponivel"] and self.b_uh:
            self.b_uh = False
            ESC.escrever_bit(MB["TDA"]["UH_DISPONIVEL"], valor=0)