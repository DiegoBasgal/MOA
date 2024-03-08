import sys
import threading
import traceback

from math import floor
from gui.ui import Ui_Form
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow

lock = threading.Lock()

class Window(QMainWindow, Ui_Form):
    def __init__(self, shared_dict):
        super().__init__()
        self.setupUi(self)

        self.dict = shared_dict

        self.sinc_timer = QTimer()
        self.sinc_timer.setInterval(100)
        self.sinc_timer.timeout.connect(self.sincro)
        self.sinc_timer.start()

    def sincro(self):
        try:
            segundos = floor(self.dict['GLB']['tempo_simul'] % 60)
            minutos = floor((self.dict['GLB']['tempo_simul'] / 60) % 60)
            horas = floor(self.dict['GLB']['tempo_simul'] / 3600)
            self.label_tempo.setText(f"{horas:02d}:{minutos:02d}:{segundos:02d}")

            # SE
            self.checkBox_djl_trip.setChecked(self.dict['SE']['dj_trip'])
            self.checkBox_djl_aberto.setChecked(self.dict['SE']['dj_aberto'])
            self.checkBox_djl_fechado.setChecked(self.dict['SE']['dj_fechado'])
            self.checkBox_djl_condicao.setChecked(self.dict['SE']['dj_condicao'])
            self.checkBox_djl_falta_vcc.setChecked(self.dict['SE']['dj_falta_vcc'])
            self.checkBox_djl_mola.setChecked(self.dict['SE']['dj_mola_carregada'])

            self.lcdNumber_lt.display(self.dict['SE']['tensao_vab'])
            self.lcdNumber_mu.display(f"{self.dict['SE']['potencia_se']:4.1f}")

            self.lcdNumber_mp.display(f"{self.dict['SE']['potencia_se']:4.1f}")
            self.lcdNumber_mr.display(f"{self.dict['SE']['potencia_se']:4.1f}")

            # TDA
            self.lcdNumber_montante.display(f"{self.dict['TDA']['nv_montante']:3.4f}")
            self.lcdNumber_Q_afluente.display(f"{self.dict['TDA']['q_alfuente']:2.3f}")
            self.lcdNumber_Q_liquida.display(f"{self.dict['TDA']['q_liquida']:2.3f}")
            self.lcdNumber_Q_sanitaria.display(f"{self.dict['TDA']['q_sanitaria']:2.3f}")
            self.lcdNumber_Q_vertimento.display(f"{self.dict['TDA']['q_vertimento']:2.3f}")

            self.lcdNumber_lg_status.display("O") if self.dict['TDA']['lg_operando'] else self.lcdNumber_lg_status.display("P")

            # UG1
            self.lcdNumber_potencia_ug1.display(f"{int(self.dict['UG1']['potencia']):d}")
            self.lcdNumber_setpoint_ug1.display(f"{int(self.dict['UG1']['setpoint']):d}")
            self.lcdNumber_etapa_alvo_ug1.display(self.dict['UG1']['etapa_alvo'])
            self.lcdNumber_etapa_atual_ug1.display(self.dict['UG1']['etapa_atual'])

            # UG2
            self.lcdNumber_potencia_ug2.display(f"{int(self.dict['UG2']['potencia']):d}")
            self.lcdNumber_setpoint_ug2.display(f"{int(self.dict['UG2']['setpoint']):d}")
            self.lcdNumber_etapa_alvo_ug2.display(self.dict['UG2']['etapa_alvo'])
            self.lcdNumber_etapa_atual_ug2.display(self.dict['UG2']['etapa_atual'])

            # CP1
            self.progressBar_cp1.setValue(int(self.dict['CP1']['progresso']))

            if self.dict['CP1']['aberta']:
                self.lcdNumber_etapa_cp1.display("A")
            elif self.dict['CP1']['fechada']:
                self.lcdNumber_etapa_cp1.display("F")
            elif self.dict['CP1']['cracking']:
                self.lcdNumber_etapa_cp1.display("C")
            else:
                self.lcdNumber_etapa_cp1.display("-")

            # CP2
            self.progressBar_cp2.setValue(int(self.dict['CP2']['progresso']))

            if self.dict['CP2']['aberta']:
                self.lcdNumber_etapa_cp2.display("A")
            elif self.dict['CP2']['fechada']:
                self.lcdNumber_etapa_cp2.display("F")
            elif self.dict['CP2']['cracking']:
                self.lcdNumber_etapa_cp2.display("C")
            else:
                self.lcdNumber_etapa_cp2.display("-")

        except Exception:
            print(traceback.format_exc())
            pass

    def closeEvent(self, event):
        self.dict['GLB']['stop_sim'] = True
        self.sinc_timer.stop()
        return super().closeEvent(event)


    # GERAL
    def set_trip_condic(self):
        if self.dict['USN']['trip_condic']:
            self.dict['USN']['trip_condic'] = False

        elif self.dict['USN']['trip_condic']:
            self.dict['USN']['trip_condic'] = False

    # SE
    def set_trip_djSe(self):
        if self.dict['SE']['dj_trip']:
            self.dict['SE']['debug_dj_reset'] = True

        elif not self.dict['SE']['dj_trip']:
            self.dict['SE']['tensao_linha'] = 0
            self.dict['SE']['dj_trip'] = True

    def alterar_estado_djSe(self):
        if self.dict['SE']['dj_aberto'] and not self.dict['SE']['dj_fechado']:
            self.dict['SE']['debug_dj_fechar'] = True

        elif self.dict['SE']['dj_fechado'] and not self.dict['SE']['dj_aberto']:
            self.dict['SE']['debug_dj_abrir'] = True

    # SE
    def set_trip_linha(self):
        if self.dict['SE']['tensao_vab'] != 0:
            self.dict['SE']['tensao_vab'] = 0
            self.dict['SE']['tensao_vab'] = 0

    def reset_trip_linha(self):
        self.dict['SE']['tensao_vab'] = 34500

    def set_trip_djSE(self):
        if self.dict['SE']['dj_trip']:
            self.dict['SE']['debug_dj_reset'] = True

        elif not self.dict['SE']['dj_trip']:
            self.dict['SE']['dj_trip'] = True

    def alterar_estado_djSE(self):
        if self.dict['SE']['dj_aberto'] and not self.dict['SE']['dj_fechado']:
            self.dict['SE']['debug_dj_fechar'] = True

        elif self.dict['SE']['dj_fechado'] and not self.dict['SE']['dj_aberto']:
            self.dict['SE']['debug_dj_abrir'] = True

    # TDA
    def mudar_q_afluente(self):
        self.dict['TDA']['q_alfuente'] = (10 ** (self.horizontalSlider_Q_afluente.value() / 75) - 1) * 2

    def operar_lg(self):
        if self.dict['CP1']['operando'] or self.dict['CP2']['operando']:
            print("[TDA] Não é possível Operar o Limpa Grades pois as comportas estão em operação!")

        elif not self.dict['TDA']['lg_operando']:
            self.dict['TDA']['lg_operando'] = True

    def parar_lg(self):
        if self.dict['CP1']['operando'] or self.dict['CP2']['operando']:
            print("[TDA] Não é possível Parar o Limpa Grades pois as comportas estão em operação!")

        elif self.dict['TDA']['lg_operando']:
            self.dict['TDA']['lg_operando'] = False

    # UG1
    def partir_ug1(self):
        self.dict['UG1']['debug_partir'] = True

    def parar_ug1(self):
        self.dict['UG1']['debug_parar'] = True

    def mudar_setpoint_ug1(self):
        self.dict['UG1']['debug_setpoint'] = self.horizontalSlider_sp_ug1.value()

    # UG2
    def partir_ug2(self):
        self.dict['UG2']['debug_partir'] = True

    def parar_ug2(self):
        self.dict['UG2']['debug_parar'] = True

    def mudar_setpoint_ug2(self):
        self.dict['UG2']['debug_setpoint'] = self.horizontalSlider_sp_ug2.value()

    # CP1
    def set_abertura_cp1(self):
        self.dict['CP1']['thread_aberta'] = True

    def set_fechamento_cp1(self):
        self.dict['CP1']['thread_fechada'] = True

    def set_cracking_cp1(self):
        self.dict['CP1']['thread_cracking'] = True

    def trip_cracking_cp1(self):
        if self.dict['CP1']['cracking']:
            self.dict['CP1']['trip'] = True
        else:
            print("[UG2-CP1] O Comando de teste de TRIP de equalização só é possível na posição de Cracking!")

    # CP2
    def set_abertura_cp2(self):
        self.dict['CP2']['thread_aberta'] = True

    def set_fechamento_cp2(self):
        self.dict['CP2']['thread_fechada'] = True

    def set_cracking_cp2(self):
        self.dict['CP2']['thread_cracking'] = True

    def trip_cracking_cp2(self):
        if self.dict['CP2']['cracking']:
            self.dict['CP2']['trip'] = True
        else:
            print("[UG2-CP2] O Comando de teste de TRIP de equalização só é possível na posição de Cracking!")


def start_gui(shared_dict):
    app = QApplication(sys.argv)
    win = Window(shared_dict)
    win.show()
    app.exec()
