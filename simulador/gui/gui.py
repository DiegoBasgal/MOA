import sys
import threading

from math import floor
from pathlib import Path
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame

from gui.ui import Ui_Form

lock = threading.Lock()

class Window(QMainWindow, Ui_Form):
    def __init__(self, shared_dict):

        super().__init__()
        self.setupUi(self)

        self.dict = shared_dict
        # Timer de sincronização com o processo de simulação!
        self.sinc_timer = QTimer()
        self.sinc_timer.setInterval(100)
        self.sinc_timer.timeout.connect(self.sincro)
        self.sinc_timer.start()

    def sincro(self):
        try:
            segundos = floor(self.dict["GLB"]["tempo_simul"] % 60)
            minutos = floor((self.dict["GLB"]["tempo_simul"] / 60) % 60)
            horas = floor(self.dict["GLB"]["tempo_simul"] / 3600)
            self.label_tempo_simul.setText(f"{horas:02d}:{minutos:02d}:{segundos:02d}")

            self.lcdNumber_tensao_linha.display(self.dict['SE']["tensao_vab"])
            self.lcdNumber_potencia_se.display(f"{self.dict['SE']['potencia_se']:0.0f}")
            self.lcdNumber_MP.display(f"{self.dict['SE']['potencia_se']:0.0f}")
            self.lcdNumber_MR.display(f"{self.dict['SE']['potencia_se']:0.0f}")

            self.checkBox_sinal_trip_condic_usina.setChecked(self.dict["USN"]["trip_condic_usina"])

            self.checkBox_52L_aberto.setChecked(self.dict["SE"]["dj_aberto"])
            self.checkBox_52L_fechado.setChecked(self.dict["SE"]["dj_fechado"])
            self.checkBox_52L_inconsistente.setChecked(self.dict["SE"]["dj_inconsistente"])
            self.checkBox_52L_trip.setChecked(self.dict["SE"]["dj_trip"])
            self.checkBox_52L_mola_carregada.setChecked(self.dict["SE"]["dj_mola_carregada"])
            self.checkBox_52L_falta_vcc.setChecked(self.dict["SE"]["dj_falta_vcc"])
            self.checkBox_52L_condicao_fechamento.setChecked(self.dict["SE"]["dj_condicao"])

            self.lcdNumber_nv_montante.display(f"{self.dict['TDA']['nv_montante']:3.2f}")
            self.lcdNumber_q_alfuente.display(f"{self.dict['TDA']['q_alfuente']:2.3f}")
            self.lcdNumber_q_liquida.display(f"{self.dict['TDA']['q_liquida']:2.3f}")
            self.lcdNumber_q_sanitaria.display(f"{self.dict['TDA']['q_sanitaria']:2.3f}")
            self.lcdNumber_q_vertimento.display(f"{self.dict['TDA']['q_vertimento']:2.3f}")

            self.checkBox_sinal_trip_ug1.setChecked(self.dict["UG1"]["trip"])
            self.checkBox_sinal_trip_condic_ug1.setChecked(self.dict["UG1"]["trip_condic"])

            self.lcdNumber_potencia_ug1.display(f'{self.dict["UG1"]["potencia"]:0.0f}')
            self.lcdNumber_setpoint_ug1.display(f'{self.dict["UG1"]["setpoint"]:0.0f}')

            if self.dict["UG1"]["etapa_alvo"] is None:
                self.lcdNumber_etapa_alvo_ug1.setHexMode()
                self.lcdNumber_etapa_alvo_ug1.display(15)

            else:
                self.lcdNumber_etapa_alvo_ug1.setDecMode()
                self.lcdNumber_etapa_alvo_ug1.display(f"{self.dict['UG1']['etapa_alvo']:d}")

            self.lcdNumber_etapa_atual_ug1.display(f"{self.dict['UG1']['etapa_atual']:d}")
            self.lcdNumber_bitsalarme_ug1.display(f"{self.dict['UG1']['flags']:08b}")
            self.lcdNumber_q_ug1.display(f"{self.dict['UG1']['q']:2.3f}")
            self.lcdNumber_temperatura_1_ug1.display(f"{self.dict['UG1']['temp_fase_r']:03.1f}")
            self.lcdNumber_temperatura_2_ug1.display(f"{self.dict['UG1']['temp_fase_s']:03.1f}")
            self.lcdNumber_temperatura_3_ug1.display(f"{self.dict['UG1']['temp_fase_t']:03.1f}")
            self.lcdNumber_temperatura_4_ug1.display(f"{self.dict['UG1']['temp_nucleo_gerador_1']:03.1f}")
            self.lcdNumber_temperatura_5_ug1.display(f"{self.dict['UG1']['temp_nucleo_gerador_2']:03.1f}")
            self.lcdNumber_temperatura_6_ug1.display(f"{self.dict['UG1']['temp_nucleo_gerador_3']:03.1f}")
            self.lcdNumber_temperatura_7_ug1.display(f"{self.dict['UG1']['temp_mancal_guia_casq']:03.1f}")
            self.lcdNumber_temperatura_8_ug1.display(f"{self.dict['UG1']['temp_mancal_casq_comb']:03.1f}")
            self.lcdNumber_temperatura_9_ug1.display(f"{self.dict['UG1']['temp_mancal_esc_comb']:03.1f}")
            self.lcdNumber_temperatura_9_ug1.display(f"{self.dict['UG1']['temp_mancal_contra_esc_comb']:03.1f}")
            self.lcdNumber_perda_na_grade_ug1.display(f"{self.dict['TDA']['nv_montante'] - self.dict['TDA']['nv_jusante_grade']:03.1f}")

            self.checkBox_sinal_trip_ug2.setChecked(self.dict['UG2']["trip"])
            self.checkBox_sinal_trip_condic_ug2.setChecked(self.dict['UG2']["trip_condic"])

            self.lcdNumber_potencia_ug2.display(f'{self.dict["UG2"]["potencia"]:0.0f}')
            self.lcdNumber_setpoint_ug2.display(f'{self.dict["UG2"]["setpoint"]:0.0f}')

            if self.dict['UG2']["etapa_alvo"] is None:
                self.lcdNumber_etapa_alvo_ug2.setHexMode()
                self.lcdNumber_etapa_alvo_ug2.display(15)

            else:
                self.lcdNumber_etapa_alvo_ug2.setDecMode()
                self.lcdNumber_etapa_alvo_ug2.display(f"{self.dict['UG2']['etapa_alvo']:d}")

            self.lcdNumber_etapa_atual_ug2.display(f"{self.dict['UG2']['etapa_atual']:d}")
            self.lcdNumber_bitsalarme_ug2.display(f"{self.dict['UG2']['flags']:08b}")
            self.lcdNumber_q_ug2.display(f"{self.dict['UG2']['q']:2.3f}")
            self.lcdNumber_temperatura_1_ug2.display(f"{self.dict['UG2']['temp_fase_r']:03.1f}")
            self.lcdNumber_temperatura_2_ug2.display(f"{self.dict['UG2']['temp_fase_s']:03.1f}")
            self.lcdNumber_temperatura_3_ug2.display(f"{self.dict['UG2']['temp_fase_t']:03.1f}")
            self.lcdNumber_temperatura_4_ug2.display(f"{self.dict['UG2']['temp_nucleo_gerador_1']:03.1f}")
            self.lcdNumber_temperatura_5_ug2.display(f"{self.dict['UG2']['temp_nucleo_gerador_2']:03.1f}")
            self.lcdNumber_temperatura_6_ug2.display(f"{self.dict['UG2']['temp_nucleo_gerador_3']:03.1f}")
            self.lcdNumber_temperatura_7_ug2.display(f"{self.dict['UG2']['temp_mancal_guia_casq']:03.1f}")
            self.lcdNumber_temperatura_8_ug2.display(f"{self.dict['UG2']['temp_mancal_casq_comb']:03.1f}")
            self.lcdNumber_temperatura_9_ug2.display(f"{self.dict['UG2']['temp_mancal_esc_comb']:03.1f}")
            self.lcdNumber_temperatura_9_ug2.display(f"{self.dict['UG2']['temp_mancal_contra_esc_comb']:03.1f}")
            self.lcdNumber_perda_na_grade_ug2.display(f"{self.dict['TDA']['nv_montante'] - self.dict['TDA']['nv_jusante_grade']:3.1f}")

        except Exception as e:
            print("A", repr(e))
            pass

    def closeEvent(self, event):
        self.dict["GLB"]["stop_sim"] = True
        self.sinc_timer.stop()
        return super().closeEvent(event)

    def mudar_q_afluente(self):
        self.dict["TDA"]["q_alfuente"] = (10 ** (self.horizontalSlider_q_afluente.value() / 75) - 1) * 2

    def set_trip_condic_usina(self):
        self.dict["USN"]["trip_condic_usina"] = True

    def reset_trip_condic_usina(self):
        self.dict["USN"]["trip_condic_usina"] = False

    def reset_geral_condic_usina(self):
        self.dict["USN"]["reset_geral_condic"] = True
        self.dict["USN"]["trip_condic_usina"] = False
        self.dict["UG1"]["trip_condic"] = False
        self.dict["UG2"]["trip_condic"] = False

        QTimer.singleShot(1000, self.aux_reset_geral_condic_usina)

    def aux_reset_geral_condic_usina(self):
        self.dict["USN"]["reset_geral_condic"] = False

    def pulse_trip_linha(self):
        self.set_trip_linha()
        QTimer.singleShot(2000, self.reset_trip_linha)

    def set_trip_linha(self):
        self.dict["SE"]["tensao_vab"] = 0
        self.dict["SE"]["tensao_vbc"] = 0
        self.dict["SE"]["tensao_vca"] = 0

    def reset_trip_linha(self):
        self.dict["SE"]["tensao_vab"] = 34500
        self.dict["SE"]["tensao_vbc"] = 34500
        self.dict["SE"]["tensao_vca"] = 34500

    def pulse_trip_52L(self):
        self.set_trip_52L()
        QTimer.singleShot(2000, self.reset_trip_52L)

    def set_trip_52L(self):
        self.dict["SE"]["dj_trip"] = True

    def reset_trip_52L(self):
        self.dict["SE"]["dj_trip"] = False

    # ug1
    def pulso_trip_ug1(self):
        self.set_trip_high_ug1()
        QTimer.singleShot(2000, self.set_trip_low_ug1)

    def set_trip_high_ug1(self):
        self.dict["UG1"]["trip"] = True

    def set_trip_low_ug1(self):
        self.dict["UG1"]["trip"] = False

    def set_trip_condic_ug1(self):
        self.dict["UG1"]["trip_condic"] = True

    def reset_trip_condic_ug1(self):
        self.dict["UG1"]["trip_condic"] = False

    def reconhece_reset_ug1(self):
        self.dict["UG1"]["reconhece_reset"] = True

    def partir_ug1(self):
        self.dict["UG1"]["debug_partir"] = True

    def parar_ug1(self):
        self.dict["UG1"]["debug_parar"] = True

    def mudar_setpoint_ug1(self):
        self.dict["UG1"]["debug_setpoint"] = self.horizontalSlider_setpoint_ug1.value()

    # ug2
    def pulso_trip_ug2(self):
        self.set_trip_high_ug2()
        QTimer.singleShot(2000, self.set_trip_low_ug2)

    def set_trip_high_ug2(self):
        self.dict["UG2"]["trip"] = True

    def set_trip_low_ug2(self):
        self.dict["UG2"]["trip"] = False

    def set_trip_condic_ug2(self):
        self.dict["UG2"]["trip_condic"] = True

    def reset_trip_condic_ug2(self):
        self.dict["UG2"]["trip_condic"] = False

    def reconhece_reset_ug2(self):
        self.dict["UG2"]["reconhece_reset"] = True

    def partir_ug2(self):
        self.dict["UG2"]["debug_partir"] = True

    def parar_ug2(self):
        self.dict["UG2"]["debug_parar"] = True

    def mudar_setpoint_ug2(self):
        self.dict["UG2"]["debug_setpoint"] = self.horizontalSlider_setpoint_ug2.value()

    # dj52L
    def alternar_estado_dj52L(self):
        if self.dict["SE"]["dj_aberto"]:
            self.dict["SE"]["debug_dj_fechar"] = True
        if self.dict["SE"]["dj_fechado"]:
            self.dict["SE"]["debug_dj_abrir"] = True

    def provocar_inconsistencia_dj52L(self):
        self.dict["SE"]["debug_dj_abrir"] = True
        self.dict["SE"]["debug_dj_fechar"] = True

    def reconhecer_reset_dj52L(self):
        self.dict["SE"]["debug_dj_reset"] = True

def start_gui(shared_dict):
    app = QApplication(sys.argv)
    win = Window(shared_dict)
    win.show()
    app.exec()
