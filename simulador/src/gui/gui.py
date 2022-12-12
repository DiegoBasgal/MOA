from pathlib import Path
import sys
import threading
from math import floor
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from .ui_geral import Ui_Form

lock = threading.Lock()


class Window(QMainWindow, Ui_Form):
    def __init__(self, shared_dict, parent=None):

        super().__init__(parent)
        self.setupUi(self)

        self.shared_dict = shared_dict
        # Timer de sincronização com o processo de simulação!
        self.sinc_timer = QTimer()
        self.sinc_timer.setInterval(100)
        self.sinc_timer.timeout.connect(self.sincro)
        self.sinc_timer.start()
        self.aux1=0
        self.aux2=0 
        self.aux3=0
        self.shared_dict["trip_condic_usina"]=False
        self.shared_dict["trip_condic_ug1"]=False
        self.shared_dict["trip_condic_ug2"]=False
        self.shared_dict["set_press_cx_espiral_ug1"] = False
        self.shared_dict["set_press_cx_espiral_ug2"] = False

    def sincro(self):
        try:
            segundos = floor(self.shared_dict["tempo_simul"] % 60)
            minutos = floor((self.shared_dict["tempo_simul"] / 60) % 60)
            horas = floor(self.shared_dict["tempo_simul"] / 3600)
            self.label_tempo_simul.setText("{:02d}:{:02d}:{:02d}".format(horas, minutos, segundos))

            self.lcdNumber_tensao_linha.display(self.shared_dict["tensao_na_linha"])
            self.lcdNumber_potencia_se.display("{:3.1f}".format(self.shared_dict["potencia_kw_se"]))
            self.lcdNumber_MP.display("{:1.3f}".format(self.shared_dict["potencia_kw_mp"] / 1000))
            self.lcdNumber_MR.display("{:1.3f}".format(self.shared_dict["potencia_kw_mr"] / 1000))

            self.checkBox_sinal_trip_condic_usina.setChecked(self.shared_dict["trip_condic_usina"])

            self.checkBox_52L_aberto.setChecked(self.shared_dict["dj52L_aberto"])
            self.checkBox_52L_fechado.setChecked(self.shared_dict["dj52L_fechado"])
            self.checkBox_52L_inconsistente.setChecked(self.shared_dict["dj52L_inconsistente"])
            self.checkBox_52L_trip.setChecked(self.shared_dict["dj52L_trip"])
            self.checkBox_52L_mola_carregada.setChecked(self.shared_dict["dj52L_mola_carregada"])
            self.checkBox_52L_falta_vcc.setChecked(self.shared_dict["dj52L_falta_vcc"])
            self.checkBox_52L_condicao_fechamento.setChecked(self.shared_dict["dj52L_condicao_de_fechamento"])

            self.lcdNumber_nv_montante.display("{:3.2f}".format(self.shared_dict["nv_montante"]))
            self.lcdNumber_q_alfuente.display("{:2.3f}".format(self.shared_dict["q_alfuente"]))
            self.lcdNumber_q_liquida.display("{:2.3f}".format(self.shared_dict["q_liquida"]))
            self.lcdNumber_q_sanitaria.display("{:2.3f}".format(self.shared_dict["q_sanitaria"]))
            self.lcdNumber_q_vertimento.display("{:2.3f}".format(self.shared_dict["q_vertimento"]))

            self.checkBox_sinal_trip_ug1.setChecked(self.shared_dict["trip_ug1"])
            self.checkBox_sinal_trip_condic_ug1.setChecked(self.shared_dict["trip_condic_ug1"])

            self.lcdNumber_potencia_ug1.display(self.shared_dict["potencia_kw_ug1"])
            self.lcdNumber_setpoint_ug1.display(self.shared_dict["setpoint_kw_ug1"])

            if self.shared_dict["etapa_alvo_ug1"] is None:
                self.lcdNumber_etapa_alvo_ug1.setHexMode()
                self.lcdNumber_etapa_alvo_ug1.display(15)

            else:
                self.lcdNumber_etapa_alvo_ug1.setDecMode()
                self.lcdNumber_etapa_alvo_ug1.display("{:d}".format(self.shared_dict["etapa_alvo_ug1"]))

            self.lcdNumber_etapa_atual_ug1.display("{:d}".format(self.shared_dict["etapa_atual_ug1"]))
            self.lcdNumber_bitsalarme_ug1.display("{:08b}".format(self.shared_dict["flags_ug1"]))
            self.lcdNumber_q_ug1.display("{:2.3f}".format(self.shared_dict["q_ug1"]))
            self.lcdNumber_caixa_espiral_ug1.display("{:03.2f}".format(self.shared_dict["pressao_caixa_espiral_ug1"]))
            self.lcdNumber_temperatura_ug1_fase_r.display("{:03.1f}".format(self.shared_dict["temperatura_ug1_fase_r"]))
            self.lcdNumber_temperatura_ug1_fase_s.display("{:03.1f}".format(self.shared_dict["temperatura_ug1_fase_s"]))
            self.lcdNumber_temperatura_ug1_fase_t.display("{:03.1f}".format(self.shared_dict["temperatura_ug1_fase_t"]))
            self.lcdNumber_temperatura_ug1_nucleo_gerador_1.display("{:03.1f}".format(self.shared_dict["temperatura_ug1_nucleo_gerador_1"]))
            self.lcdNumber_temperatura_ug1_nucleo_gerador_2.display("{:03.1f}".format(self.shared_dict["temperatura_ug1_nucleo_gerador_2"]))
            self.lcdNumber_temperatura_ug1_nucleo_gerador_3.display("{:03.1f}".format(self.shared_dict["temperatura_ug1_nucleo_gerador_3"]))
            self.lcdNumber_temperatura_ug1_mancal_casq_rad.display("{:03.1f}".format(self.shared_dict["temperatura_ug1_mancal_casq_rad"]))
            self.lcdNumber_temperatura_ug1_mancal_casq_rad_comb.display("{:03.1f}".format(self.shared_dict["temperatura_ug1_mancal_casq_comb"]))
            self.lcdNumber_temperatura_ug1_mancal_esc_comb.display("{:03.1f}".format(self.shared_dict["temperatura_ug1_mancal_escora_comb"]))
            self.lcdNumber_perda_na_grade_ug1.display("{:03.1f}".format(self.shared_dict["nv_montante"] - self.shared_dict["nv_jusante_grade"]))
            
            self.checkBox_sinal_trip_ug2.setChecked(self.shared_dict["trip_ug2"])
            self.checkBox_sinal_trip_condic_ug2.setChecked(self.shared_dict["trip_condic_ug2"])

            self.lcdNumber_potencia_ug2.display(self.shared_dict["potencia_kw_ug2"])
            self.lcdNumber_setpoint_ug2.display(self.shared_dict["setpoint_kw_ug2"])

            if self.shared_dict["etapa_alvo_ug2"] is None:
                self.lcdNumber_etapa_alvo_ug2.setHexMode()
                self.lcdNumber_etapa_alvo_ug2.display(15)

            else:
                self.lcdNumber_etapa_alvo_ug2.setDecMode()
                self.lcdNumber_etapa_alvo_ug2.display("{:d}".format(self.shared_dict["etapa_alvo_ug2"]))

            self.lcdNumber_etapa_atual_ug2.display("{:d}".format(self.shared_dict["etapa_atual_ug2"]))
            self.lcdNumber_bitsalarme_ug2.display("{:08b}".format(self.shared_dict["flags_ug2"]))
            self.lcdNumber_q_ug2.display("{:2.3f}".format(self.shared_dict["q_ug2"]))
            self.lcdNumber_caixa_espiral_ug2.display("{:03.2f}".format(self.shared_dict["pressao_caixa_espiral_ug2"]))
            self.lcdNumber_temperatura_ug2_fase_r.display("{:03.1f}".format(self.shared_dict["temperatura_ug2_fase_r"]))
            self.lcdNumber_temperatura_ug2_fase_s.display("{:03.1f}".format(self.shared_dict["temperatura_ug2_fase_s"]))
            self.lcdNumber_temperatura_ug2_fase_t.display("{:03.1f}".format(self.shared_dict["temperatura_ug2_fase_t"]))
            self.lcdNumber_temperatura_ug2_nucleo_gerador_1.display("{:03.1f}".format(self.shared_dict["temperatura_ug2_nucleo_gerador_1"]))
            self.lcdNumber_temperatura_ug2_nucleo_gerador_2.display("{:03.1f}".format(self.shared_dict["temperatura_ug2_nucleo_gerador_2"]))
            self.lcdNumber_temperatura_ug2_nucleo_gerador_3.display("{:03.1f}".format(self.shared_dict["temperatura_ug2_nucleo_gerador_3"]))
            self.lcdNumber_temperatura_ug2_mancal_casq_rad.display("{:03.1f}".format(self.shared_dict["temperatura_ug2_mancal_casq_rad"]))
            self.lcdNumber_temperatura_ug2_mancal_casq_rad_comb.display("{:03.1f}".format(self.shared_dict["temperatura_ug2_mancal_casq_comb"]))
            self.lcdNumber_temperatura_ug2_mancal_esc_comb.display("{:03.1f}".format(self.shared_dict["temperatura_ug2_mancal_escora_comb"]))
            self.lcdNumber_perda_na_grade_ug2.display("{:3.1f}".format(self.shared_dict["nv_montante"] - self.shared_dict["nv_jusante_grade"]))

        except Exception as e:
            print("A", repr(e))
            pass

    def closeEvent(self, event):
        self.shared_dict["stop_sim"] = True
        self.sinc_timer.stop()
        return super().closeEvent(event)

    def mudar_q_afluente(self):
        self.shared_dict["q_alfuente"] = (10 ** (self.horizontalSlider_q_afluente.value() / 75) - 1) * 2

    def mudar_press_cx_espiral(self):
        if self.shared_dict["set_press_cx_espiral_ug1"] == True:
            self.shared_dict["pressao_caixa_espiral_ug1"] = self.horizontalSlider_press_cx_espiral.value() *0.01
            if self.shared_dict["pressao_caixa_espiral_ug1"] == 15.49:
                self.shared_dict["pressao_caixa_espiral_ug1"] = 0.0
        if self.shared_dict["set_press_cx_espiral_ug2"] == True:
            self.shared_dict["pressao_caixa_espiral_ug2"] = self.horizontalSlider_press_cx_espiral.value() * 0.01
            if self.shared_dict["pressao_caixa_espiral_ug2"] == 15.49:
                self.shared_dict["pressao_caixa_espiral_ug2"] = 0.0
    
    def set_trip_condic_usina(self):
        self.shared_dict["trip_condic_usina"] = True

    def reset_trip_condic_usina(self):
        self.shared_dict["trip_condic_usina"] = False
    
    def reset_geral_condic_usina(self):
        self.shared_dict["reset_geral_condic"] = True
        self.shared_dict["trip_condic_usina"] = False
        self.shared_dict["trip_condic_ug1"] = False
        self.shared_dict["trip_condic_ug2"] = False
        
        QTimer.singleShot(1000, self.aux_reset_geral_condic_usina)
    
    def aux_reset_geral_condic_usina(self):
        self.shared_dict["reset_geral_condic"] = False

    def pulse_trip_linha(self):
        self.set_trip_linha()
        QTimer.singleShot(2000, self.reset_trip_linha)
    
    def set_trip_linha(self):
        self.shared_dict["tensao_na_linha"] = 0

    def reset_trip_linha(self):
        self.shared_dict["tensao_na_linha"] = 34500

    def pulse_trip_52L(self):
        self.set_trip_52L()
        QTimer.singleShot(2000, self.reset_trip_52L)

    def set_trip_52L(self):
        self.shared_dict["trip_52L"] = True

    def reset_trip_52L(self):
        self.shared_dict["trip_52L"] = False

    # ug1
    def pulso_trip_ug1(self):
        self.set_trip_high_ug1()
        QTimer.singleShot(2000, self.set_trip_low_ug1)

    def set_trip_high_ug1(self):
        self.shared_dict["trip_ug1"] = True

    def set_trip_low_ug1(self):
        self.shared_dict["trip_ug1"] = False

    def set_trip_condic_ug1(self):
        self.shared_dict["trip_condic_ug1"] = True

    def reset_trip_condic_ug1(self):
        self.shared_dict["trip_condic_ug1"] = False

    def reconhece_reset_ug1(self):
        self.shared_dict["reconhece_reset_ug1"] = True

    def partir_ug1(self):
        self.shared_dict["debug_partir_ug1"] = True
        print("partir ug1 GUI")

    def parar_ug1(self):
        self.shared_dict["debug_parar_ug1"] = True

    def mudar_setpoint_ug1(self):
        self.shared_dict["debug_setpoint_kw_ug1"] = self.horizontalSlider_setpoint_ug1.value()

    def set_press_cx_esp_ug1(self):
        if self.shared_dict["set_press_cx_espiral_ug1"] == False:
            self.horizontalSlider_press_cx_espiral.setValue(1549)
            self.shared_dict["set_press_cx_espiral_ug1"] = True
            self.lcdNumber_caixa_espiral_ug1.setFrameShadow(QFrame.Plain)
            self.shared_dict["set_press_cx_espiral_ug2"] = False
            self.lcdNumber_caixa_espiral_ug2.setFrameShadow(QFrame.Sunken)
        elif self.shared_dict["set_press_cx_espiral_ug1"] == True:
            self.shared_dict["set_press_cx_espiral_ug1"] = False
            self.horizontalSlider_press_cx_espiral.setValue(1549)
            self.lcdNumber_caixa_espiral_ug1.setFrameShadow(QFrame.Sunken)

    # ug2
    def pulso_trip_ug2(self):
        self.set_trip_high_ug2()
        QTimer.singleShot(2000, self.set_trip_low_ug2)

    def set_trip_high_ug2(self):
        self.shared_dict["trip_ug2"] = True

    def set_trip_low_ug2(self):
        self.shared_dict["trip_ug2"] = False

    def set_trip_condic_ug2(self):
        self.shared_dict["trip_condic_ug2"] = True

    def reset_trip_condic_ug2(self):
        self.shared_dict["trip_condic_ug2"] = False

    def reconhece_reset_ug2(self):
        self.shared_dict["reconhece_reset_ug2"] = True

    def partir_ug2(self):
        self.shared_dict["debug_partir_ug2"] = True
        print("partir ug2 GUI")

    def parar_ug2(self):
        self.shared_dict["debug_parar_ug2"] = True

    def mudar_setpoint_ug2(self):
        self.shared_dict[
            "debug_setpoint_kw_ug2"
        ] = self.horizontalSlider_setpoint_ug2.value()

    def set_press_cx_esp_ug2(self):
        if self.shared_dict["set_press_cx_espiral_ug2"] == False:
            self.horizontalSlider_press_cx_espiral.setValue(1549)
            self.shared_dict["set_press_cx_espiral_ug1"] = False
            self.lcdNumber_caixa_espiral_ug1.setFrameShadow(QFrame.Sunken)
            self.shared_dict["set_press_cx_espiral_ug2"] = True
            self.lcdNumber_caixa_espiral_ug2.setFrameShadow(QFrame.Plain)
        elif self.shared_dict["set_press_cx_espiral_ug2"] == True:
            self.shared_dict["set_press_cx_espiral_ug2"] = False
            self.horizontalSlider_press_cx_espiral.setValue(1549)
            self.lcdNumber_caixa_espiral_ug2.setFrameShadow(QFrame.Sunken)

    # dj52L
    def alternar_estado_dj52L(self):
        if self.shared_dict["dj52L_aberto"]:
            self.shared_dict["debug_dj52L_fechar"] = True
        if self.shared_dict["dj52L_fechado"]:
            self.shared_dict["debug_dj52L_abrir"] = True

    def provocar_inconsistencia_dj52L(self):
        self.shared_dict["debug_dj52L_abrir"] = True
        self.shared_dict["debug_dj52L_fechar"] = True

    def reconhecer_reset_dj52L(self):
        self.shared_dict["debug_dj52L_reconhece_reset"] = True

def start_gui(shared_dict):
    app = QApplication(sys.argv)
    win = Window(shared_dict)
    win.show()
    app.exec()
