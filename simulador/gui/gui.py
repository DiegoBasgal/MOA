import sys
import threading
import traceback

from time import time
from math import floor
from gui.ui import Ui_Form
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame

from dicts.const import *


lock = threading.Lock()


class Window(QMainWindow, Ui_Form):
    def __init__(self, dict):
        super().__init__()
        self.setupUi(self)

        self.dict = dict

        self.sinc_timer = QTimer()
        self.sinc_timer.setInterval(100)
        self.sinc_timer.timeout.connect(self.sincro)
        self.sinc_timer.start()


    def sincro(self):
        try:
            segundos = floor(self.dict['GLB']['tempo_simul'] % 60)
            minutos = floor((self.dict['GLB']['tempo_simul'] / 60) % 60)
            horas = floor(self.dict['GLB']['tempo_simul'] / 3600)
            self.label_contador_tempo.setText(f"{horas:02d}:{minutos:02d}:{segundos:02d}")

            # TDA
            self.progressBar_cp1_ug1.setValue(int(self.dict['TDA']['cp1_posicao']))
            self.progressBar_cp2_ug2.setValue(int(self.dict['TDA']['cp2_posicao']))
            self.progressBar_cp3_ug3.setValue(int(self.dict['TDA']['cp3_posicao']))
            self.progressBar_cp4_ug4.setValue(int(self.dict['TDA']['cp4_posicao']))

            if self.dict['TDA']['cp1_fechada'] and not self.dict['TDA']['cp1_aberta']:
                self.lcdNumber_etapa_cp1_ug1.display('F')
            elif not self.dict['TDA']['cp1_fechada'] and not self.dict['TDA']['cp1_aberta']:
                self.lcdNumber_etapa_cp1_ug1.display('C')
            elif not self.dict['TDA']['cp1_fechada'] and self.dict['TDA']['cp1_aberta']:
                self.lcdNumber_etapa_cp1_ug1.display('A')

            if self.dict['TDA']['cp2_fechada'] and not self.dict['TDA']['cp2_aberta']:
                self.lcdNumber_etapa_cp2_ug2.display('F')
            elif not self.dict['TDA']['cp2_fechada'] and not self.dict['TDA']['cp2_aberta']:
                self.lcdNumber_etapa_cp2_ug2.display('C')
            elif not self.dict['TDA']['cp2_fechada'] and self.dict['TDA']['cp2_aberta']:
                self.lcdNumber_etapa_cp2_ug2.display('A')

            if self.dict['TDA']['cp3_fechada'] and not self.dict['TDA']['cp3_aberta']:
                self.lcdNumber_etapa_cp3_ug3.display('F')
            elif not self.dict['TDA']['cp3_fechada'] and not self.dict['TDA']['cp3_aberta']:
                self.lcdNumber_etapa_cp3_ug3.display('C')
            elif not self.dict['TDA']['cp3_fechada'] and self.dict['TDA']['cp3_aberta']:
                self.lcdNumber_etapa_cp3_ug3.display('A')

            if self.dict['TDA']['cp4_fechada'] and not self.dict['TDA']['cp4_aberta']:
                self.lcdNumber_etapa_cp4_ug4.display('F')
            elif not self.dict['TDA']['cp4_fechada'] and not self.dict['TDA']['cp4_aberta']:
                self.lcdNumber_etapa_cp4_ug4.display('C')
            elif not self.dict['TDA']['cp4_fechada'] and self.dict['TDA']['cp4_aberta']:
                self.lcdNumber_etapa_cp4_ug4.display('A')

            self.lcdNumber_nv_montante.display(f"{self.dict['TDA']['nv_montante']:3.4f}")
            self.lcdNumber_q_liquida.display(f"{self.dict['TDA']['q_liquida']:2.3f}")
            self.lcdNumber_q_alfuente.display(f"{self.dict['TDA']['q_alfuente']:2.3f}")
            self.lcdNumber_q_vertimento.display(f"{self.dict['TDA']['q_vertimento']:2.3f}")


            # AD
            # CP1
            self.lcdNumber_q_cp1_ad.display(f"{self.dict['AD']['cp1_q']:2.3f}")
            self.checkBox_manual_cp1_ad.setChecked(self.dict['AD']['cp1_manual'])
            self.progressBar_cp1_ad.setValue(int(self.dict['AD']['cp1_setpoint']))

            # CP2
            self.lcdNumber_q_cp2_ad.display(f"{self.dict['AD']['cp2_q']:2.3f}")
            self.checkBox_manual_cp2_ad.setChecked(self.dict['AD']['cp2_manual'])
            self.progressBar_cp2_ad.setValue(int(self.dict['AD']['cp2_setpoint']))


            # SE
            self.checkBox_djl_trip.setChecked(self.dict['SE']['dj_trip'])
            self.checkBox_djl_aberto.setChecked(self.dict['SE']['dj_aberto'])
            self.checkBox_djl_fechado.setChecked(self.dict['SE']['dj_fechado'])
            self.checkBox_djl_condicao.setChecked(self.dict['SE']['dj_condicao'])
            self.checkBox_djl_falta_vcc.setChecked(self.dict['SE']['dj_falta_vcc'])
            self.checkBox_djl_mola.setChecked(self.dict['SE']['dj_mola_carregada'])

            self.lcdNumber_lt.display(f'{int(self.dict["SE"]["tensao_rs"])}')
            self.lcdNumber_mu.display(f'{int(self.dict["SE"]["potencia_se"])}')


            # UG1
            self.checkBox_condic_ug1.setChecked(self.dict['UG1']['condic'])

            self.lcdNumber_etapa_alvo_ug1.display(self.dict['UG1']['etapa_alvo'])
            self.lcdNumber_etapa_atual_ug1.display(self.dict['UG1']['etapa_atual'])
            self.lcdNumber_q_ug1.display(f'{self.dict["UG1"]["q"]:2.3f}')
            self.lcdNumber_potencia_ug1.display(f'{int(self.dict["UG1"]["potencia"]):d}')
            self.lcdNumber_setpoint_ug1.display(f'{int(self.dict["UG1"]["setpoint"]):d}')
            self.lcdNumber_pressao_ug1.display(f'{self.dict["UG1"]["pressao_turbina"]:1.2f}')
            self.lcdNumber_temp_1_ug1.display(f'{self.dict["UG1"]["temp_fase_r"]:3.1f}')
            self.lcdNumber_temp_2_ug1.display(f'{self.dict["UG1"]["temp_fase_s"]:3.1f}')
            self.lcdNumber_temp_3_ug1.display(f'{self.dict["UG1"]["temp_fase_t"]:3.1f}')
            self.lcdNumber_temp_4_ug1.display(f'{self.dict["UG1"]["temp_mancal_gerador_la_1"]:3.1f}')
            self.lcdNumber_temp_5_ug1.display(f'{self.dict["UG1"]["temp_mancal_gerador_la_2"]:3.1f}')
            self.lcdNumber_temp_6_ug1.display(f'{self.dict["UG1"]["temp_mancal_gerador_lna_1"]:3.1f}')
            self.lcdNumber_temp_7_ug1.display(f'{self.dict["UG1"]["temp_mancal_gerador_lna_2"]:3.1f}')
            self.lcdNumber_temp_8_ug1.display(f'{self.dict["UG1"]["temp_mancal_turbina_radial"]:3.1f}')
            self.lcdNumber_temp_9_ug1.display(f'{self.dict["UG1"]["temp_mancal_turbina_escora"]:3.1f}')
            self.lcdNumber_temp_10_ug1.display(f'{self.dict["UG1"]["temp_mancal_turbina_contra_escora"]:3.1f}')


            # UG2
            self.checkBox_condic_ug2.setChecked(self.dict['UG2']['condic'])

            self.lcdNumber_etapa_alvo_ug2.display(self.dict['UG2']['etapa_alvo'])
            self.lcdNumber_etapa_atual_ug2.display(self.dict['UG2']['etapa_atual'])
            self.lcdNumber_q_ug2.display(f'{self.dict["UG2"]["q"]:2.3f}')
            self.lcdNumber_potencia_ug2.display(f'{int(self.dict["UG2"]["potencia"]):d}')
            self.lcdNumber_setpoint_ug2.display(f'{int(self.dict["UG2"]["setpoint"]):d}')
            self.lcdNumber_pressao_ug2.display(f'{self.dict["UG2"]["pressao_turbina"]:1.2f}')
            self.lcdNumber_temp_1_ug2.display(f'{self.dict["UG2"]["temp_fase_r"]:3.1f}')
            self.lcdNumber_temp_2_ug2.display(f'{self.dict["UG2"]["temp_fase_s"]:3.1f}')
            self.lcdNumber_temp_3_ug2.display(f'{self.dict["UG2"]["temp_fase_t"]:3.1f}')
            self.lcdNumber_temp_4_ug2.display(f'{self.dict["UG2"]["temp_mancal_gerador_la_1"]:3.1f}')
            self.lcdNumber_temp_5_ug2.display(f'{self.dict["UG2"]["temp_mancal_gerador_la_2"]:3.1f}')
            self.lcdNumber_temp_6_ug2.display(f'{self.dict["UG2"]["temp_mancal_gerador_lna_1"]:3.1f}')
            self.lcdNumber_temp_7_ug2.display(f'{self.dict["UG2"]["temp_mancal_gerador_lna_2"]:3.1f}')
            self.lcdNumber_temp_8_ug2.display(f'{self.dict["UG2"]["temp_mancal_turbina_radial"]:3.1f}')
            self.lcdNumber_temp_9_ug2.display(f'{self.dict["UG2"]["temp_mancal_turbina_escora"]:3.1f}')
            self.lcdNumber_temp_10_ug2.display(f'{self.dict["UG2"]["temp_mancal_turbina_contra_escora"]:3.1f}')


            # UG3
            self.checkBox_condic_ug3.setChecked(self.dict['UG3']['condic'])
            self.lcdNumber_etapa_alvo_ug3.display(self.dict['UG3']['etapa_alvo'])
            self.lcdNumber_etapa_atual_ug3.display(self.dict['UG3']['etapa_atual'])
            self.lcdNumber_q_ug3.display(f'{self.dict["UG3"]["q"]:2.3f}')
            self.lcdNumber_potencia_ug3.display(f'{int(self.dict["UG3"]["potencia"]):d}')
            self.lcdNumber_setpoint_ug3.display(f'{int(self.dict["UG3"]["setpoint"]):d}')
            self.lcdNumber_pressao_ug3.display(f'{self.dict["UG3"]["pressao_turbina"]:1.2f}')
            self.lcdNumber_temp_1_ug3.display(f'{self.dict["UG3"]["temp_fase_r"]:3.1f}')
            self.lcdNumber_temp_2_ug3.display(f'{self.dict["UG3"]["temp_fase_s"]:3.1f}')
            self.lcdNumber_temp_3_ug3.display(f'{self.dict["UG3"]["temp_fase_t"]:3.1f}')
            self.lcdNumber_temp_4_ug3.display(f'{self.dict["UG3"]["temp_mancal_gerador_la_1"]:3.1f}')
            self.lcdNumber_temp_5_ug3.display(f'{self.dict["UG3"]["temp_mancal_gerador_la_2"]:3.1f}')
            self.lcdNumber_temp_6_ug3.display(f'{self.dict["UG3"]["temp_mancal_gerador_lna_1"]:3.1f}')
            self.lcdNumber_temp_7_ug3.display(f'{self.dict["UG3"]["temp_mancal_gerador_lna_2"]:3.1f}')
            self.lcdNumber_temp_8_ug3.display(f'{self.dict["UG3"]["temp_mancal_turbina_radial"]:3.1f}')
            self.lcdNumber_temp_9_ug3.display(f'{self.dict["UG3"]["temp_mancal_turbina_escora"]:3.1f}')
            self.lcdNumber_temp_10_ug3.display(f'{self.dict["UG3"]["temp_mancal_turbina_contra_escora"]:3.1f}')


            # UG4
            self.checkBox_condic_ug4.setChecked(self.dict['UG4']['condic'])
            self.lcdNumber_etapa_alvo_ug4.display(self.dict['UG4']['etapa_alvo'])
            self.lcdNumber_etapa_atual_ug4.display(self.dict['UG4']['etapa_atual'])
            self.lcdNumber_q_ug4.display(f'{self.dict["UG4"]["q"]:2.3f}')
            self.lcdNumber_potencia_ug4.display(f'{int(self.dict["UG4"]["potencia"]):d}')
            self.lcdNumber_setpoint_ug4.display(f'{int(self.dict["UG4"]["setpoint"]):d}')
            self.lcdNumber_pressao_ug4.display(f'{self.dict["UG4"]["pressao_turbina"]:1.2f}')
            self.lcdNumber_temp_1_ug4.display(f'{self.dict["UG4"]["temp_fase_r"]:3.1f}')
            self.lcdNumber_temp_2_ug4.display(f'{self.dict["UG4"]["temp_fase_s"]:3.1f}')
            self.lcdNumber_temp_3_ug4.display(f'{self.dict["UG4"]["temp_fase_t"]:3.1f}')
            self.lcdNumber_temp_4_ug4.display(f'{self.dict["UG4"]["temp_mancal_gerador_la_1"]:3.1f}')
            self.lcdNumber_temp_5_ug4.display(f'{self.dict["UG4"]["temp_mancal_gerador_la_2"]:3.1f}')
            self.lcdNumber_temp_6_ug4.display(f'{self.dict["UG4"]["temp_mancal_gerador_lna_1"]:3.1f}')
            self.lcdNumber_temp_7_ug4.display(f'{self.dict["UG4"]["temp_mancal_gerador_lna_2"]:3.1f}')
            self.lcdNumber_temp_8_ug4.display(f'{self.dict["UG4"]["temp_mancal_turbina_radial"]:3.1f}')
            self.lcdNumber_temp_9_ug4.display(f'{self.dict["UG4"]["temp_mancal_turbina_escora"]:3.1f}')
            self.lcdNumber_temp_10_ug4.display(f'{self.dict["UG4"]["temp_mancal_turbina_contra_escora"]:3.1f}')

        except Exception:
            print(traceback.format_exc())
            pass


    def closeEvent(self, event):
        self.dict['GLB']['stop_sim'] = True
        self.sinc_timer.stop()
        return super().closeEvent(event)


    # TDA
    def mudar_q_afluente(self):
        self.dict['TDA']['q_alfuente'] = (10 ** (self.horizontalSlider_q_afluente.value() / 75) - 1) * 2


    # AD
    def acionar_manual_cp1(self):
        if not self.dict['AD']['cp1_manual']:
            self.dict['AD']['cp1_manual'] = True
        else:
            self.dict['AD']['cp1_manual'] = False

    def acionar_manual_cp2(self):
        if not self.dict['AD']['cp2_manual']:
            self.dict['AD']['cp2_manual'] = True
        else:
            self.dict['AD']['cp2_manual'] = False

    # SE
    def set_trip_djl(self):
        if self.dict['SE']['dj_trip']:
            self.dict['SE']['debug_dj_reset'] = True

        elif not self.dict['SE']['dj_trip']:
            self.dict['SE']['tensao_linha'] = 0
            self.dict['SE']['dj_trip'] = True

    def alterar_estado_djl(self):
        if self.dict['SE']['dj_aberto'] and not self.dict['SE']['dj_fechado']:
            self.dict['SE']['debug_dj_fechar'] = True

        elif self.dict['SE']['dj_fechado'] and not self.dict['SE']['dj_aberto']:
            self.dict['SE']['debug_dj_abrir'] = True

    def set_trip_lt(self):
        self.dict['SE']['tensao_rs'] = 0

    def reset_trip_lt(self):
        self.dict['SE']['tensao_rs'] = 138000


    # UG1
    def partir_ug1(self):
        self.dict['UG1']['debug_partir'] = True

    def parar_ug1(self):
        self.dict['UG1']['debug_parar'] = True

    def set_condic_ug1(self):
        self.dict['UG1']['condic'] = True

    def reset_condic_ug1(self):
        self.dict['UG1']['condic'] = False

    def set_pressao_ug1(self):
        if not self.dict['UG1']['set_pressao']:
            self.horizontalSlider_pressao_ugs.setSliderPosition(0)
            self.dict['UG1']['pressao_turbina'] = 1.5
            self.dict['UG1']['set_pressao'] = True
            self.dict['UG2']['set_pressao'] = False
            self.dict['UG3']['set_pressao'] = False
            self.dict['UG4']['set_pressao'] = False
            self.lcdNumber_pressao_ug1.setFrameShadow(QFrame.Plain)
            self.lcdNumber_pressao_ug2.setFrameShadow(QFrame.Sunken)
            self.lcdNumber_pressao_ug3.setFrameShadow(QFrame.Sunken)
            self.lcdNumber_pressao_ug4.setFrameShadow(QFrame.Sunken)
        elif self.dict['UG1']['set_pressao']:
            self.dict['UG1']['set_pressao'] = False
            self.horizontalSlider_pressao_ugs.setSliderPosition(0)
            self.lcdNumber_pressao_ug1.setFrameShadow(QFrame.Sunken)

    def mudar_setpoint_ug1(self):
        self.dict['UG1']['debug_setpoint'] = self.horizontalSlider_sp_ug1.value()


    # UG2
    def partir_ug2(self):
        self.dict['UG2']['debug_partir'] = True

    def parar_ug2(self):
        self.dict['UG2']['debug_parar'] = True

    def set_condic_ug2(self):
        self.dict['UG2']['condic'] = True

    def reset_condic_ug2(self):
        self.dict['UG2']['condic'] = False

    def set_pressao_ug2(self):
        if not self.dict['UG2']['set_pressao']:
            self.horizontalSlider_pressao_ugs.setSliderPosition(0)
            self.dict['UG2']['pressao_turbina'] = 1.5
            self.dict['UG2']['set_pressao'] = True
            self.dict['UG1']['set_pressao'] = False
            self.dict['UG3']['set_pressao'] = False
            self.dict['UG4']['set_pressao'] = False
            self.lcdNumber_pressao_ug2.setFrameShadow(QFrame.Plain)
            self.lcdNumber_pressao_ug1.setFrameShadow(QFrame.Sunken)
            self.lcdNumber_pressao_ug3.setFrameShadow(QFrame.Sunken)
            self.lcdNumber_pressao_ug4.setFrameShadow(QFrame.Sunken)
        elif self.dict['UG2']['set_pressao']:
            self.dict['UG2']['set_pressao'] = False
            self.horizontalSlider_pressao_ugs.setSliderPosition(0)
            self.lcdNumber_pressao_ug2.setFrameShadow(QFrame.Sunken)

    def mudar_setpoint_ug2(self):
        self.dict['UG2']['debug_setpoint'] = self.horizontalSlider_sp_ug2.value()


    # UG3
    def partir_ug3(self):
        self.dict['UG3']['debug_partir'] = True

    def parar_ug3(self):
        self.dict['UG3']['debug_parar'] = True

    def set_condic_ug3(self):
        self.dict['UG3']['condic'] = True

    def reset_condic_ug3(self):
        self.dict['UG3']['condic'] = False

    def set_pressao_ug3(self):
        if not self.dict['UG3']['set_pressao']:
            self.horizontalSlider_pressao_ugs.setSliderPosition(0)
            self.dict['UG3']['pressao_turbina'] = 1.5
            self.dict['UG3']['set_pressao'] = True
            self.dict['UG1']['set_pressao'] = False
            self.dict['UG2']['set_pressao'] = False
            self.dict['UG4']['set_pressao'] = False
            self.lcdNumber_pressao_ug3.setFrameShadow(QFrame.Plain)
            self.lcdNumber_pressao_ug1.setFrameShadow(QFrame.Sunken)
            self.lcdNumber_pressao_ug2.setFrameShadow(QFrame.Sunken)
            self.lcdNumber_pressao_ug4.setFrameShadow(QFrame.Sunken)
        elif self.dict['UG3']['set_pressao']:
            self.dict['UG3']['set_pressao'] = False
            self.horizontalSlider_pressao_ugs.setSliderPosition(0)
            self.lcdNumber_pressao_ug3.setFrameShadow(QFrame.Sunken)

    def mudar_setpoint_ug3(self):
        self.dict['UG3']['debug_setpoint'] = self.horizontalSlider_sp_ug3.value()


    # UG4
    def partir_ug4(self):
        self.dict['UG4']['debug_partir'] = True

    def parar_ug4(self):
        self.dict['UG4']['debug_parar'] = True

    def set_condic_ug4(self):
        self.dict['UG4']['condic'] = True

    def reset_condic_ug4(self):
        self.dict['UG4']['condic'] = False

    def set_pressao_ug4(self):
        if not self.dict['UG4']['set_pressao']:
            self.horizontalSlider_pressao_ugs.setSliderPosition(0)
            self.dict['UG4']['pressao_turbina'] = 1.5
            self.dict['UG4']['set_pressao'] = True
            self.dict['UG1']['set_pressao'] = False
            self.dict['UG2']['set_pressao'] = False
            self.dict['UG3']['set_pressao'] = False
            self.lcdNumber_pressao_ug4.setFrameShadow(QFrame.Plain)
            self.lcdNumber_pressao_ug1.setFrameShadow(QFrame.Sunken)
            self.lcdNumber_pressao_ug2.setFrameShadow(QFrame.Sunken)
            self.lcdNumber_pressao_ug3.setFrameShadow(QFrame.Sunken)
        elif self.dict['UG4']['set_pressao']:
            self.dict['UG4']['set_pressao'] = False
            self.horizontalSlider_pressao_ugs.setSliderPosition(0)
            self.lcdNumber_pressao_ug4.setFrameShadow(QFrame.Sunken)

    def mudar_setpoint_ug4(self):
        self.dict['UG4']['debug_setpoint'] = self.horizontalSlider_sp_ug4.value()


    # UGs
    def mudar_pressao_ugs(self):
        if self.dict['UG1']['set_pressao']:
            self.dict['UG1']['pressao_turbina'] = self.horizontalSlider_pressao_ugs.value() * 0.1
        elif self.dict['UG2']['set_pressao']:
            self.dict['UG2']['pressao_turbina'] = self.horizontalSlider_pressao_ugs.value() * 0.1
        elif self.dict['UG3']['set_pressao']:
            self.dict['UG3']['pressao_turbina'] = self.horizontalSlider_pressao_ugs.value() * 0.1
        elif self.dict['UG4']['set_pressao']:
            self.dict['UG4']['pressao_turbina'] = self.horizontalSlider_pressao_ugs.value() * 0.1



def start_gui(dict):
    app = QApplication(sys.argv)
    win = Window(dict)
    win.show()
    app.exec()
