import sys
import threading
import traceback

from math import floor
from pathlib import Path
from gui.ui import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap

lock = threading.Lock()


class Window(QMainWindow, Ui_Form):
    def __init__(self, shared_dict):
        super().__init__()
        self.setupUi(self)

        self.shared_dict = shared_dict
        # Timer de sincronização com o processo de simulação!
        self.sinc_timer = QTimer()
        self.sinc_timer.setInterval(100)
        self.sinc_timer.timeout.connect(self.sincro)
        self.sinc_timer.start()

    def sincro(self):
        try:
            segundos = floor(self.shared_dict['GLB']['tempo_real'] % 60)
            minutos = floor((self.shared_dict['GLB']['tempo_real'] / 60) % 60)
            horas = floor(self.shared_dict['GLB']['tempo_real'] / 3600)
            self.label_tempo.setText(f"{horas:02d}:{minutos:02d}:{segundos:02d}")

            self.lcdNumber_tensaoLinha.display(self.shared_dict['BAY']['tensao_linha'])
            self.lcdNumber_tensaoSE.display(self.shared_dict['SE']['tensao_linha'])
            self.lcdNumber_medidorSE.display(f"{self.shared_dict['SE']['potencia_se']:4.1f}")
            self.lcdNumber_MP.display(f"{self.shared_dict['BAY']['potencia_mp']:4.1f}")
            self.lcdNumber_MR.display(f"{self.shared_dict['BAY']['potencia_mr']:4.1f}")

            self.checkBox_condics.setChecked(self.shared_dict['USN']['trip_condic'])

            self.checkBox_DjSE_aberto.setChecked(self.shared_dict['SE']['dj_aberto'])
            self.checkBox_DjSE_fechado.setChecked(self.shared_dict['SE']['dj_fechado'])
            self.checkBox_DjSE_trip.setChecked(self.shared_dict['SE']['dj_trip'])
            self.checkBox_DjSE_mola.setChecked(self.shared_dict['SE']['dj_mola_carregada'])
            self.checkBox_DjSE_falta_vcc.setChecked(self.shared_dict['SE']['dj_falta_vcc'])
            self.checkBox_DjSE_condicao.setChecked(self.shared_dict['SE']['dj_condicao'])

            self.checkBox_DjBay_aberto.setChecked(self.shared_dict['BAY']['dj_aberto'])
            self.checkBox_DjBay_fechado.setChecked(self.shared_dict['BAY']['dj_fechado'])
            self.checkBox_DjBay_trip.setChecked(self.shared_dict['BAY']['dj_trip'])
            self.checkBox_DjBay_mola.setChecked(self.shared_dict['BAY']['dj_mola_carregada'])
            self.checkBox_DjBay_seccionadora.setChecked(self.shared_dict['BAY']['dj_secc'])
            self.checkBox_DjBay_condicao.setChecked(self.shared_dict['BAY']['dj_condicao'])

            self.lcdNumber_montante.display(f"{self.shared_dict['TDA']['nv_montante']:3.2f}")
            self.lcdNumber_Q_afluente.display(f"{self.shared_dict['TDA']['q_alfuente']:2.3f}")
            self.lcdNumber_Q_liquida.display(f"{self.shared_dict['TDA']['q_liquida']:2.3f}")
            self.lcdNumber_Q_sanitaria.display(f"{self.shared_dict['TDA']['q_sanitaria']:2.3f}")
            self.lcdNumber_Q_vertimento.display(f"{self.shared_dict['TDA']['q_vertimento']:2.3f}")

            self.lcdNumber_ug1_potencia.display(f"{self.shared_dict['UG1']['potencia']}")
            self.lcdNumber_ug1_setpoint.display(f"{self.shared_dict['UG1']['setpoint']}")

            if self.shared_dict['UG1']['etapa_alvo'] is None:
                self.lcdNumber_ug1_etapa_alvo.setHexMode()
                self.lcdNumber_ug1_etapa_alvo.display(15)

            else:
                self.lcdNumber_ug1_etapa_alvo.setDecMode()
                self.lcdNumber_ug1_etapa_alvo.display(f"{self.shared_dict['UG1']['etapa_alvo']:d}")

            self.lcdNumber_ug1_etapa_atual.display(f"{self.shared_dict['UG1']['etapa_atual']:d}")


            self.lcdNumber_ug2_potencia.display(f"{self.shared_dict['UG2']['potencia']}")
            self.lcdNumber_ug2_setpoint.display(f"{self.shared_dict['UG2']['setpoint']}")

            if self.shared_dict['UG2']['etapa_alvo'] is None:
                self.lcdNumber_ug2_etapa_alvo.setHexMode()
                self.lcdNumber_ug2_etapa_alvo.display(15)

            else:
                self.lcdNumber_ug2_etapa_alvo.setDecMode()
                self.lcdNumber_ug2_etapa_alvo.display(f"{self.shared_dict['UG2']['etapa_alvo']:d}")

            self.lcdNumber_ug2_etapa_atual.display(f"{self.shared_dict['UG2']['etapa_atual']:d}")

            self.progressBar_cp1.setValue(int(self.shared_dict['TDA']['cp1_progresso']))
            self.progressBar_cp2.setValue(int(self.shared_dict['TDA']['cp2_progresso']))

            if self.shared_dict['TDA']['lg_operando']:
                self.lcdNumber_lg_status.display("O")
            else:
                self.lcdNumber_lg_status.display("P")

            if self.shared_dict['TDA']['cp1_aberta']:
                self.lcdNumber_status_cp1.display("A")
            elif self.shared_dict['TDA']['cp1_fechada']:
                self.lcdNumber_status_cp1.display("F")
            elif self.shared_dict['TDA']['cp1_cracking']:
                self.lcdNumber_status_cp1.display("C")
            else:
                self.lcdNumber_status_cp1.display("-")

            if self.shared_dict['TDA']['cp2_aberta']:
                self.lcdNumber_status_cp2.display("A")
            elif self.shared_dict['TDA']['cp2_fechada']:
                self.lcdNumber_status_cp2.display("F")
            elif self.shared_dict['TDA']['cp2_cracking']:
                self.lcdNumber_status_cp2.display("C")
            else:
                self.lcdNumber_status_cp2.display("-")

        except Exception:
            print(traceback.format_exc())
            pass

    def closeEvent(self, event):
        self.shared_dict['GLB']['stop_sim'] = True
        self.sinc_timer.stop()
        return super().closeEvent(event)

    def mudar_Q_afluente(self):
        self.shared_dict['TDA']['q_alfuente'] = (10 ** (self.horizontalSlider_Q_afluente.value() / 75) - 1) * 2

    def set_trip_condic_usina(self):
        if not self.shared_dict['USN']['trip_condic']:
            self.shared_dict['USN']['trip_condic'] = True
        else:
            self.shared_dict['USN']['trip_condic'] = False

    # UG1
    def partir_ug1(self):
        self.shared_dict['UG1']['debug_partir'] = True

    def parar_ug1(self):
        self.shared_dict['UG1']['debug_parar'] = True

    def mudar_setpoint_ug1(self):
        self.shared_dict['UG1']['debug_setpoint'] = self.horizontalSlider_ug1_setpoint.value()

    def set_thread_cp1_aberta(self):
        self.shared_dict['TDA']['cp1_thread_aberta'] = True

    def set_thread_cp1_fechada(self):
        self.shared_dict['TDA']['cp1_thread_fechada'] = True

    def set_thread_cp1_cracking(self):
        self.shared_dict['TDA']['cp1_thread_cracking'] = True

    def trip_cp1_cracking(self):
        if self.shared_dict['TDA']['cp1_cracking']:
            self.shared_dict['TDA']['cp1_trip'] = True
        else:
            print("[UG1-CP1] O Comando de teste de TRIP de equalização só é possível na posição de Cracking!")

    # UG2
    def partir_ug2(self):
        self.shared_dict['UG2']['debug_partir'] = True

    def parar_ug2(self):
        self.shared_dict['UG2']['debug_parar'] = True

    def mudar_setpoint_ug2(self):
        self.shared_dict['UG2']['debug_setpoint'] = self.horizontalSlider_setpoint_ug2.value()

    def set_thread_cp2_aberta(self):
        self.shared_dict['TDA']['cp2_thread_aberta'] = True

    def set_thread_cp2_fechada(self):
        self.shared_dict['TDA']['cp2_thread_fechada'] = True

    def set_thread_cp2_cracking(self):
        self.shared_dict['TDA']['cp2_thread_cracking'] = True

    def trip_cp2_cracking(self):
        if self.shared_dict['TDA']['cp2_cracking']:
            self.shared_dict['TDA']['cp2_trip'] = True
        else:
            print("[UG2-CP2] O Comando de teste de TRIP de equalização só é possível na posição de Cracking!")

    # djSe
    def set_trip_djSe(self):
        self.shared_dict['SE']['dj_trip'] = True

    def reset_trip_djSe(self):
        self.shared_dict['SE']['dj_trip'] = False

    def alternar_estado_djSe(self):
        if self.shared_dict['SE']['dj_aberto']:
            self.shared_dict['SE']['debug_dj_fechar'] = True

        if self.shared_dict['SE']['dj_fechado']:
            self.shared_dict['SE']['debug_dj_abrir'] = True

    def reset_djSe(self):
        self.shared_dict['SE']['debug_dj_reset'] = True

    # djBay
    def set_trip_linha(self):
        self.shared_dict['BAY']['tensao_linha'] = 0
        self.shared_dict['SE']['tensao_linha'] = 0

    def reset_trip_linha(self):
        self.shared_dict['BAY']['tensao_linha'] = 23100

    def alternar_estado_djBay(self):
        if self.shared_dict['BAY']['dj_aberto']:
            self.shared_dict['BAY']['debug_dj_fechar'] = True

        if self.shared_dict['BAY']['dj_fechado']:
            self.shared_dict['BAY']['debug_dj_abrir'] = True

    def reset_djBay(self):
        self.shared_dict['BAY']['debug_dj_reset'] = True

    # limpa grades
    def operar_limpa_grades(self):
        if self.shared_dict['TDA']['cp1_operando'] or self.shared_dict['TDA']['cp2_operando']:
            print("[TDA] Não é possível Operar o Limpa Grades pois as comportas estão em operação!")

        elif not self.shared_dict['TDA']['lg_operando']:
            self.shared_dict['TDA']['lg_operando'] = True

        else:
            print("[TDA] O Limpa Grades já está em Operação!")

    def parar_limpa_grades(self):
        if self.shared_dict['TDA']['cp1_operando'] or self.shared_dict['TDA']['cp2_operando']:
            print("[TDA] Não é possível Parar o Limpa Grades pois as comportas estão em operação!")

        elif self.shared_dict['TDA']['lg_operando']:
            self.shared_dict['TDA']['lg_operando'] = False

        else:
            print("[TDA] O Limpa Grades já está Parado!")

def start_gui(shared_dict):
    app = QApplication(sys.argv)
    win = Window(shared_dict)
    win.show()
    app.exec()
